from typing import List, Tuple

import pymupdf
from google.genai import types
from sqlalchemy.orm import Session

from app.models.cat_pi_resume import CatPIResume
from app.models.user import User
from app.services.gemini_key_manager import gemini_key_manager

RESUME_OCR_PROMPT = """
You are extracting the full text of a resume from a PDF that has no usable text layer (it is
scanned or image-based).

Read every page carefully.

Extract the COMPLETE visible content, preserving structure such as:
- Name and contact details
- Summary / objective
- Education
- Work experience / internships (titles, organizations, dates, bullet points)
- Extracurriculars, achievements, certifications
- Skills
- Links (LinkedIn, portfolio, etc.)

Do NOT summarize.

Do NOT invent missing information.

Do NOT add information that is not visible.

Return only the extracted resume text.
"""


def _get_background_color(page: "pymupdf.Page") -> Tuple[int, int, int]:
    """Estimates the page's background color by sampling its four corners - resume content
    essentially never starts exactly at the page edge, so this is a cheap, reliable stand-in
    for a full background-detection pass."""
    pixmap = page.get_pixmap()
    width, height = pixmap.width, pixmap.height
    margin = 5

    sample_points = [
        (margin, margin),
        (max(width - margin - 1, 0), margin),
        (margin, max(height - margin - 1, 0)),
        (max(width - margin - 1, 0), max(height - margin - 1, 0)),
    ]

    samples = [
        pixmap.pixel(x, y)[:3]
        for x, y in sample_points
        if 0 <= x < width and 0 <= y < height
    ]

    if not samples:
        return (255, 255, 255)

    return (
        sum(sample[0] for sample in samples) // len(samples),
        sum(sample[1] for sample in samples) // len(samples),
        sum(sample[2] for sample in samples) // len(samples),
    )


def _color_distance(first: Tuple[int, int, int], second: Tuple[int, int, int]) -> float:
    return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


def _is_visible_span(span: dict, page_rect: "pymupdf.Rect", background: Tuple[int, int, int]) -> bool:
    """Filters out text a human reading the rendered PDF would never see - near-zero-size
    text, text positioned off the page, or text colored to match the background - so a
    hidden prompt-injection payload embedded in an uploaded resume can't reach the PI prompt."""
    if span.get("size", 0) < 1:
        return False

    bbox = pymupdf.Rect(span["bbox"])
    if not bbox.intersects(page_rect):
        return False

    color_int = span.get("color", 0)
    text_color = ((color_int >> 16) & 255, (color_int >> 8) & 255, color_int & 255)

    if _color_distance(text_color, background) < 12:
        return False

    return True


def _group_into_visual_lines(spans: List[dict]) -> List[Tuple[str, "pymupdf.Rect"]]:
    """Groups spans by vertical position (rather than PyMuPDF's own "line" grouping, which
    some resume templates fragment into multiple objects per printed line), sorts each
    group left to right, and returns (text, bbox) pairs."""
    if not spans:
        return []

    ordered = sorted(
        spans,
        key=lambda span: ((span["bbox"][1] + span["bbox"][3]) / 2, span["bbox"][0]),
    )

    lines: List[List[dict]] = []
    for span in ordered:
        y_center = (span["bbox"][1] + span["bbox"][3]) / 2
        tolerance = max(span["bbox"][3] - span["bbox"][1], 1) / 2

        if lines:
            last_line = lines[-1]
            last_y_center = sum(
                (item["bbox"][1] + item["bbox"][3]) / 2 for item in last_line
            ) / len(last_line)
            if abs(y_center - last_y_center) <= tolerance:
                last_line.append(span)
                continue

        lines.append([span])

    results: List[Tuple[str, "pymupdf.Rect"]] = []
    for line in lines:
        ordered_spans = sorted(line, key=lambda span: span["bbox"][0])
        text = "".join(span["text"] for span in ordered_spans)
        bbox = pymupdf.Rect(ordered_spans[0]["bbox"])
        for span in ordered_spans[1:]:
            bbox |= pymupdf.Rect(span["bbox"])
        results.append((text, bbox))

    return results


def _attach_links(lines: List[Tuple[str, "pymupdf.Rect"]], links: List[dict]) -> List[str]:
    """Matches each hyperlink annotation to the visible line it overlaps, appending the URL
    inline - otherwise links (LinkedIn, GitHub, portfolio) are invisible to plain text
    extraction since they're stored separately from the visible text."""
    if not links:
        return [text for text, _ in lines]

    results = [text for text, _ in lines]
    attached_uris: set = set()

    for link in links:
        uri = link.get("uri")
        if not uri:
            continue

        link_rect = pymupdf.Rect(link["from"])
        best_index = None
        best_overlap = 0.0

        for index, (_, bbox) in enumerate(lines):
            intersection = bbox & link_rect
            if intersection.is_empty:
                continue
            overlap = intersection.get_area()
            if overlap > best_overlap:
                best_overlap = overlap
                best_index = index

        if best_index is not None:
            results[best_index] += f" ({uri})"
            attached_uris.add(uri)
        elif uri not in attached_uris:
            results.append(f"[Link: {uri}]")
            attached_uris.add(uri)

    return results


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts visible text from an in-memory PDF (no file is written to disk - the raw
    bytes are never persisted, only this extracted text is)."""
    extracted_text = ""

    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
        for page in document:
            background = _get_background_color(page)
            page_dict = page.get_text("dict", sort=True)

            visible_spans = [
                span
                for block in page_dict.get("blocks", [])
                for line in block.get("lines", [])
                for span in line.get("spans", [])
                if span.get("text") and _is_visible_span(span, page.rect, background)
            ]

            visual_lines = [
                (text, bbox)
                for text, bbox in _group_into_visual_lines(visible_spans)
                if text.strip()
            ]

            page_lines = _attach_links(visual_lines, page.get_links())

            if page_lines:
                extracted_text += "\n".join(page_lines) + "\n"

    return extracted_text


def extract_text_via_gemini_ocr(pdf_bytes: bytes) -> str:
    """Fallback for scanned/image-only PDFs with no usable text layer."""
    result = gemini_key_manager.generate_content(
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            RESUME_OCR_PROMPT,
        ],
        purpose="cat_pi_resume_ocr",
    )
    text = (result or "").strip()
    if not text:
        raise ValueError("Could not extract text from the resume.")
    return text


def extract_resume_text(pdf_bytes: bytes) -> str:
    text = extract_text_from_pdf(pdf_bytes)
    if text.strip():
        return text
    return extract_text_via_gemini_ocr(pdf_bytes)


def create_resume(db: Session, user: User, filename: str, pdf_bytes: bytes) -> CatPIResume:
    extracted_text = extract_resume_text(pdf_bytes)
    resume = CatPIResume(
        user_id=user.id,
        original_filename=filename,
        extracted_text=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def list_resumes(db: Session, user: User) -> List[CatPIResume]:
    return (
        db.query(CatPIResume)
        .filter(CatPIResume.user_id == user.id)
        .order_by(CatPIResume.created_at.desc())
        .all()
    )


def delete_resume(db: Session, user: User, resume_id: int) -> None:
    resume = (
        db.query(CatPIResume)
        .filter(CatPIResume.id == resume_id, CatPIResume.user_id == user.id)
        .first()
    )
    if resume is None:
        return
    db.delete(resume)
    db.commit()

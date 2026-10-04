"""Parser for the CAT 2020 Slot 2 DILR paper specifically - the DILR
sibling of pyq_varc_parser_qheader.py. Like that VARC case, this is the
one DILR paper with no official solutions PDF (only the question-only PDF
exists, and it's a scanned image with no text layer, so it needed
tesseract OCR rather than pdftotext).

This template is actually cleaner than most: data sets are introduced by
an explicit "Set N:" marker (100% reliable, unlike every other legacy
DILR template this session had to reverse-engineer), and questions use
unambiguous "Q.N." headers. Options are "A. B. C. D." (bare letter + dot,
no parens) - OCR noise occasionally mangles the trailing punctuation
(stray quotes/semicolons, "D:" instead of "D."), so the option matcher is
deliberately a little loose on what follows the letter.

No "Correct Answer:"/"Solution:"/"Quick Tip" exists anywhere (it's a
question-only paper) - nothing to anchor against, but none needed either,
since "Set N:" and "Q.N." are already unambiguous.

Usage:
    python3 pyq_dilr_parser_qheader.py <text_file> <year> <slot>
"""
import json
import re
import sys

SET_RE = re.compile(r"^Set\s*(\d+)\s*:\s*$", re.IGNORECASE)
HEADER_RE = re.compile(r"^Q\.\s*(\d+)\.?\s*(.*)$")
OPTION_RE = re.compile(r"^([A-D])[.:;]\s*(.*)$")
PAGE_NOISE_RE = re.compile(
    r"^\s*\d+\s*$|^PAP collegedunia\s*$|^India.s largest Student Review Platform\s*$",
    re.IGNORECASE,
)


def clean_lines(raw_text):
    raw_text = raw_text.replace("\f", "\n")
    lines = raw_text.split("\n")
    return [ln.rstrip() for ln in lines if not PAGE_NOISE_RE.match(ln)]


def parse(text, year, slot):
    lines = clean_lines(text)

    set_markers = []  # (line_idx, set_number)
    for i, ln in enumerate(lines):
        m = SET_RE.match(ln.strip())
        if m:
            set_markers.append((i, int(m.group(1))))

    headers = []  # (line_idx, number, first_line_text)
    for i, ln in enumerate(lines):
        m = HEADER_RE.match(ln.strip())
        if m:
            headers.append((i, int(m.group(1)), m.group(2)))

    questions = []
    set_idx_ptr = 0
    current_group_id = None
    current_set_num = None

    for h_idx, (line_idx, number, first_text) in enumerate(headers):
        while set_idx_ptr < len(set_markers) and set_markers[set_idx_ptr][0] < line_idx:
            current_set_num = set_markers[set_idx_ptr][1]
            current_group_id = f"cat{year}_dilr_{slot}_set{current_set_num}"
            set_idx_ptr += 1

        end_idx = headers[h_idx + 1][0] if h_idx + 1 < len(headers) else len(lines)
        # Don't run into the NEXT set's passage if this is the last
        # question of a set (no further "Q." header before it).
        next_set_idx = next(
            (s[0] for s in set_markers if s[0] > line_idx and s[0] < end_idx), None
        )
        if next_set_idx is not None:
            end_idx = next_set_idx

        body_lines = [first_text] + lines[line_idx + 1 : end_idx]
        question_text, options = split_lettered_options(body_lines)
        question_text = normalize_text(question_text)

        questions.append(
            {
                "number": str(number),
                "group_id": current_group_id,
                "passage_text": None,  # filled in below
                "question_text": question_text,
                "question_type": "TITA" if options is None else "MCQ",
                "options": options,
                "correct_answer_raw": None,
            }
        )

    # Passage text for each set = everything between its "Set N:" marker
    # and the first question header that follows it.
    set_passages = {}
    for i, (marker_idx, set_num) in enumerate(set_markers):
        first_q = next((h for h in headers if h[0] > marker_idx), None)
        end = first_q[0] if first_q else len(lines)
        passage = normalize_text("\n".join(lines[marker_idx + 1 : end]))
        set_passages[set_num] = passage

    for q in questions:
        set_num = int(q["group_id"].rsplit("set", 1)[1]) if q["group_id"] else None
        if set_num is not None:
            q["passage_text"] = set_passages.get(set_num)

    return {"flagged_sets": [], "questions": questions}


def split_lettered_options(body_lines):
    option_start = None
    for i, ln in enumerate(body_lines):
        if i == 0:
            continue
        if OPTION_RE.match(ln.strip()):
            option_start = i
            break
    if option_start is None:
        return "\n".join(body_lines).strip(), None

    question_lines = body_lines[:option_start]
    option_lines = body_lines[option_start:]

    options = []
    current = None
    for ln in option_lines:
        stripped = ln.strip()
        if not stripped:
            continue
        m = OPTION_RE.match(stripped)
        if m:
            if current is not None:
                options.append(current.strip())
            current = m.group(2)
        elif current is not None:
            current += " " + stripped
    if current is not None:
        options.append(current.strip())

    return "\n".join(question_lines).strip(), options if options else None


def normalize_text(text):
    paragraphs = re.split(r"\n\s*\n", text)
    out = []
    for p in paragraphs:
        words = " ".join(l.strip() for l in p.split("\n") if l.strip())
        if words:
            out.append(words)
    return "\n\n".join(out)


if __name__ == "__main__":
    path = sys.argv[1]
    year = sys.argv[2]
    slot = sys.argv[3]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    result = parse(text, year, slot)
    print(json.dumps(result, indent=2, ensure_ascii=False))

"""Parser for the CAT 2020 Slot 2 VARC paper specifically - this is the one
VARC paper with no official solutions PDF (only the question-only PDF
exists, and that PDF is a scanned image with no text layer, so it needed
tesseract OCR rather than pdftotext).

This template uses unambiguous "Q1", "Q2", ... headers (never colliding
with its lettered "a./A." options), so unlike pyq_varc_parser_legacy.py it
needs no Correct-Answer-anchoring trick - headers are matched directly.

Every new RC passage (except the standalone "passage given below is
followed by four alternate summaries" items, which are self-contained
single questions) is introduced by the exact fixed boilerplate line "The
passage below is accompanied by a set of questions. Choose the best answer
to each question." - this is a reliable, document-specific anchor for
passage-group boundaries, and also for where a trailing option's text
should be truncated (OCR produces no blank line before this marker, so a
naive "collect continuation lines until the next lettered option" approach
over-swallows the next passage into the last option of the previous
question without this explicit stop signal).

Usage:
    python3 pyq_varc_parser_qheader.py <text_file> <year> <slot>
"""
import json
import re
import sys

HEADER_RE = re.compile(r"^Q(\d+)\s+(.*)$")
OPTION_RE = re.compile(r"^[A-Za-z]\.\s*(.*)$")
PAGE_NOISE_RE = re.compile(
    r"^\s*\d+\s*$|^PAP collegedunia\s*$|^India.s largest Student Review Platform\s*$",
    re.IGNORECASE,
)
BOILERPLATE_RE = re.compile(
    r"^The passage below is accompanied by a set of questions\.\s*"
    r"(Choose the best answer to each\s*)?$",
    re.IGNORECASE,
)
BOILERPLATE_CONT_RE = re.compile(r"^question\.\s*$", re.IGNORECASE)
STANDALONE_RE = re.compile(
    r"four sentences|five jumbled|followed by four alternate summaries",
    re.IGNORECASE,
)


def clean_lines(raw_text):
    raw_text = raw_text.replace("\f", "\n")
    lines = raw_text.split("\n")
    return [ln.rstrip() for ln in lines if not PAGE_NOISE_RE.match(ln)]


def find_boilerplate_starts(lines):
    """Return the set of line indices where a boilerplate marker begins."""
    starts = set()
    for i, ln in enumerate(lines):
        if BOILERPLATE_RE.match(ln.strip()):
            starts.add(i)
    return starts


def parse(text, year, slot):
    lines = clean_lines(text)
    boilerplate_starts = find_boilerplate_starts(lines)

    headers = []  # (line_idx, number, first_line_text)
    for i, ln in enumerate(lines):
        m = HEADER_RE.match(ln)
        if m:
            headers.append((i, int(m.group(1)), m.group(2)))

    questions = []
    rc_set_counter = 0
    current_group_id = None

    for h_idx, (line_idx, number, first_text) in enumerate(headers):
        prev_header_end = headers[h_idx - 1][0] if h_idx > 0 else 0
        end_idx = headers[h_idx + 1][0] if h_idx + 1 < len(headers) else len(lines)

        # A boilerplate marker between the previous header and this one
        # (inclusive of this question's own body) means a new RC passage
        # starts right after it and runs up to this header.
        passage_text = None
        marker_idx = next(
            (b for b in sorted(boilerplate_starts) if prev_header_end <= b < line_idx),
            None,
        )
        if marker_idx is not None:
            passage_start = marker_idx + 1
            if BOILERPLATE_CONT_RE.match(lines[passage_start].strip()):
                passage_start += 1
            rc_set_counter += 1
            current_group_id = f"cat{year}_varc_{slot}_rc{rc_set_counter}"
            passage_text = normalize_text("\n".join(lines[passage_start:line_idx]))
        elif h_idx == 0:
            # Doc intro before Q1 is RC1's passage even without the marker
            # (it follows the general-instructions block, not a question).
            rc_set_counter += 1
            current_group_id = f"cat{year}_varc_{slot}_rc{rc_set_counter}"
            passage_text = normalize_text("\n".join(lines[:line_idx]))
        elif STANDALONE_RE.search(first_text):
            # Para-jumble / odd-sentence / summary-choice questions are
            # self-contained (own mini-passage folded into question_text,
            # if any) - never part of a shared RC group.
            current_group_id = None
        # else: no marker and not a standalone type -> this question
        # continues the current RC group, so current_group_id (and
        # passage_text via the backfill pass below) carries forward as-is.

        # A boilerplate marker can also appear *after* this header, inside
        # this question's own body/options span (introducing the *next*
        # question's passage) - that's where the previous bug leaked text
        # into this question's last option. Truncate the body there.
        body_end = end_idx
        trailing_marker = next(
            (b for b in sorted(boilerplate_starts) if line_idx < b < end_idx), None
        )
        if trailing_marker is not None:
            body_end = trailing_marker

        body_lines = [first_text] + lines[line_idx + 1 : body_end]
        question_text, options = split_lettered_options(body_lines)
        question_text = normalize_text(question_text)

        questions.append(
            {
                "number": str(number),
                "group_id": current_group_id,
                "passage_text": passage_text,
                "question_text": question_text,
                "question_type": "TITA" if options is None else "MCQ",
                "options": options,
                "correct_answer_raw": None,
            }
        )

    last_passage = {}
    for q in questions:
        if q["group_id"] is None:
            continue
        if q["passage_text"]:
            last_passage[q["group_id"]] = q["passage_text"]
        elif q["group_id"] in last_passage:
            q["passage_text"] = last_passage[q["group_id"]]

    return questions


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
            current = m.group(1)
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

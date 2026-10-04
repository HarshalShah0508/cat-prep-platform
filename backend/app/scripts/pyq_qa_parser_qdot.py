"""Parser for the CAT 2021 Slot 2 QA solutions PDF template - a second QA
template, different from pyq_qa_parser.py in header/option shape only:

    Q. 1. <question text>

    Solution:
    ...
    (1) 8
    (2) ...
    Correct Answer: ...

Headers are "Q. N." (unambiguous - never collides with anything in
solution prose) and options are parenthesized digits "(1)-(4)", not
lettered. Reuses the same Correct-Answer-anchored header validation as
pyq_qa_parser.py (some solutions number their own steps, which would
otherwise false-match), and the same garbage-gap detection for
embedded-math image content pdftotext couldn't recover.

Usage:
    python3 pyq_qa_parser_qdot.py <text_file> <year> <slot>
"""
import json
import re
import sys

HEADER_RE = re.compile(r"^Q\.\s*(\d+)\.\s*(.*)$")
OPTION_RE = re.compile(r"^\((\d+)\)\s*(.*)$")
CORRECT_ANSWER_RE = re.compile(r"^Correct Answer:\s*(.*)$")
# Not every question here has a "Correct Answer:" line (some TITA answers
# are only stated in free-form solution prose, e.g. "...is: 5.") - but
# every single question's solution ends with a "Quick Tip" box, so that's
# the reliable universal anchor for header validation.
QUICK_TIP_RE = re.compile(r"^\s*Quick Tip\s*$")
SOLUTION_RE = re.compile(r"^Solution:\s*$")
PAGE_FOOTER_RE = re.compile(r"^\s*\d+\s*$|^\s*Page \d+ of \d+\s*$")
GARBAGE_GAP_RE = re.compile(r"\S\s{3,}\S|^\s*$")


def clean_lines(raw_text):
    raw_text = raw_text.replace("\f", "\n")
    lines = raw_text.split("\n")
    out = []
    for ln in lines:
        if PAGE_FOOTER_RE.match(ln):
            continue
        out.append(ln.rstrip())
    return out


def find_headers(lines):
    raw = []
    for i, ln in enumerate(lines):
        m = HEADER_RE.match(ln.strip())
        if m:
            raw.append((i, int(m.group(1)), m.group(2)))

    answer_positions = [i for i, ln in enumerate(lines) if QUICK_TIP_RE.match(ln)]

    headers = []
    cand_ptr = 0
    last_candidate_before = None
    for ans_idx in answer_positions:
        while cand_ptr < len(raw) and raw[cand_ptr][0] < ans_idx:
            last_candidate_before = raw[cand_ptr]
            cand_ptr += 1
        if last_candidate_before is not None and (
            not headers or last_candidate_before[0] > headers[-1][0]
        ):
            headers.append(last_candidate_before)
    return headers


def extract_body(lines, start_idx, first_line_text, end_idx):
    """Stop collecting the question's own text/options at whichever comes
    first: a "Correct Answer:" line (most questions), or a "Solution:"
    line (the few TITA questions whose answer is only stated in free-form
    solution prose, with no "Correct Answer:" line at all). Whatever comes
    after - the worked solution, up to the "Quick Tip" box - is captured
    separately as the raw material for a simplified explanation."""
    body_lines = [first_line_text] if first_line_text else []
    correct_answer = None
    solution_start = None
    for i in range(start_idx + 1, end_idx):
        ln = lines[i]
        m = CORRECT_ANSWER_RE.match(ln)
        if m:
            correct_answer = m.group(1).strip()
            solution_start = i + 1
            break
        if SOLUTION_RE.match(ln):
            solution_start = i + 1
            break
        body_lines.append(ln)

    solution_raw = None
    if solution_start is not None:
        sol_lines = []
        for i in range(solution_start, end_idx):
            ln = lines[i]
            if QUICK_TIP_RE.match(ln):
                break
            m = SOLUTION_RE.match(ln)
            if m:
                continue
            sol_lines.append(ln)
        if sol_lines:
            solution_raw = normalize_text("\n".join(sol_lines))

    return body_lines, correct_answer, solution_raw


def split_options(body_lines):
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

    question_text = "\n".join(l for l in question_lines).strip()
    return question_text, options if options else None


def normalize_text(text):
    paragraphs = re.split(r"\n\s*\n", text)
    out = []
    for p in paragraphs:
        words = " ".join(l.strip() for l in p.split("\n") if l.strip())
        if words:
            out.append(words)
    return "\n\n".join(out)


ANSWER_INDEX_RE = re.compile(r"^\[(\d+)\]\s*(.*)$")
ANSWER_PAREN_INDEX_RE = re.compile(r"^\((\d+)\)\s*(.*)$")


def resolve_answer(correct_answer_raw, options):
    """Correct Answer lines here look like "[1] 8" or "(1) 8" (bracketed
    or parenthesized option index + the value - this paper is inconsistent
    about which) for MCQ, or a bare value for TITA. Either way the
    trailing value is already the real option text - just strip the
    index marker if present."""
    if not correct_answer_raw:
        return None
    raw = correct_answer_raw.strip()
    m = ANSWER_INDEX_RE.match(raw) or ANSWER_PAREN_INDEX_RE.match(raw)
    if m:
        return m.group(2).strip() or None
    return raw


def is_garbage(question_text, options):
    if GARBAGE_GAP_RE.search(question_text):
        return True
    if len(question_text) < 15:
        return True
    if options is not None:
        for o in options:
            if o.strip() == "" or GARBAGE_GAP_RE.search(o):
                return True
    return False


def parse(text, year, slot):
    lines = clean_lines(text)
    headers = find_headers(lines)

    questions = []
    flagged = []

    for idx, (line_idx, number, first_text) in enumerate(headers):
        end_idx = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        body_lines, correct_answer, solution_raw = extract_body(
            lines, line_idx, first_text, end_idx
        )
        question_text, options = split_options(body_lines)
        question_text = normalize_text(question_text)
        if options:
            options = [normalize_text(o) for o in options]

        if is_garbage(question_text, options):
            flagged.append(str(number))
            continue

        resolved_answer = resolve_answer(correct_answer, options)

        questions.append(
            {
                "number": str(number),
                "question_text": question_text,
                "question_type": "TITA" if options is None else "MCQ",
                "options": options,
                "correct_answer_raw": correct_answer,
                "correct_answer": resolved_answer,
                "solution_raw": solution_raw,
            }
        )

    return {"flagged": flagged, "questions": questions}


if __name__ == "__main__":
    path = sys.argv[1]
    year = sys.argv[2]
    slot = sys.argv[3]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    result = parse(text, year, slot)
    print(json.dumps(result, indent=2, ensure_ascii=False))

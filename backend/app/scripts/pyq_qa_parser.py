"""Parse a CAT QA (Quantitative Aptitude) "Question Paper with Solutions"
PDF (already converted to plain text via `pdftotext -layout`) into
structured question data - same vendor template as pyq_varc_parser.py /
pyq_dilr_parser.py, but flat numbering only (QA questions aren't grouped
under a shared passage):

    1. <question text>
    (A) ...
    (B) ...
    (C) ...
    (D) ...
    Correct Answer: (B) ...

Known limitation (why QA was deferred originally): roughly half of CAT QA
questions embed their actual math (equations, fractions, exponents) as a
rendered image rather than text, which pdftotext cannot recover - that
shows up as a run of several consecutive spaces where the image used to
be, or an entirely empty option. Rather than load a visibly broken
question, GARBAGE_RE flags any question where the text or an option has
that signature, and those are skipped (not fabricated), same policy as the
chart-dependent DILR sets.

Usage:
    python3 pyq_qa_parser.py <text_file> <year> <slot>

Prints {"flagged": [...], "questions": [...]} - flagged entries are
skipped, not included in `questions`.
"""
import json
import re
import sys

HEADER_RE = re.compile(r"^(\d+)\.\s*(.*)$")
OPTION_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
CORRECT_ANSWER_RE = re.compile(r"^Correct Answer:\s*(.*)$")
SOLUTION_RE = re.compile(r"^\s*Solution:\s*(.*)$")
QUICK_TIP_RE = re.compile(r"^\s*Quick Tip\s*$")
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
    """Some QA solutions number their OWN worked-solution steps (e.g.
    "1. Let the Variables Represent", "2. Total Persons in the Queue",
    "3. Calculate Maximum Number Ahead of Pinky") - blank-line-preceded
    just like a real question header, so that alone isn't enough to tell
    them apart (unlike VARC, where this is rare), and several of these
    false candidates can cluster together before the real next header, so
    a simple "is there an answer before the *next* candidate" lookahead
    isn't robust enough.

    The reliable anchor instead: every real question is terminated by
    exactly one "Correct Answer:" line (even TITA questions carry a "--"
    placeholder there). Solution-step false headers always appear BEFORE
    the real header they're attached to (as part of explaining the
    *previous* question) - so for each Correct Answer line, the real
    header is the LAST header-shaped candidate seen before it; any earlier
    candidates in that span are solution-step false positives."""
    raw = []
    for i, ln in enumerate(lines):
        preceded_by_blank = i == 0 or lines[i - 1].strip() == ""
        if not preceded_by_blank:
            continue
        m = HEADER_RE.match(ln)
        if m:
            raw.append((i, int(m.group(1)), m.group(2)))

    answer_positions = [i for i, ln in enumerate(lines) if CORRECT_ANSWER_RE.match(ln)]

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
    body_lines = [first_line_text] if first_line_text else []
    correct_answer = None
    answer_line_idx = None
    for i in range(start_idx + 1, end_idx):
        ln = lines[i]
        m = CORRECT_ANSWER_RE.match(ln)
        if m:
            correct_answer = m.group(1).strip()
            answer_line_idx = i
            break
        body_lines.append(ln)

    solution_raw = None
    if answer_line_idx is not None:
        sol_lines = []
        started = False
        for i in range(answer_line_idx + 1, end_idx):
            ln = lines[i]
            if QUICK_TIP_RE.match(ln):
                break
            m = SOLUTION_RE.match(ln)
            if m:
                started = True
                if m.group(1).strip():
                    sol_lines.append(m.group(1).strip())
                continue
            if started:
                sol_lines.append(ln)
        if sol_lines:
            solution_raw = normalize_text("\n".join(sol_lines))

    return body_lines, correct_answer, solution_raw


def split_options(body_lines):
    option_start = None
    for i, ln in enumerate(body_lines):
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


ANSWER_LETTER_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
ANSWER_NUM_INDEX_RE = re.compile(r"^\((\d+)\)\s*(.*)$")


def resolve_answer(correct_answer_raw, options):
    """correct_answer in the DB must match an exact entry in `options`
    (how scoring compares selected vs. correct), not a bare letter - so
    "(B) 40" needs mapping to options[1]'s actual text.

    Some questions here (mostly 2021 Slot 1) have their options embedded
    inline in the question stem rather than split into a real options
    list (the OPTION_RE lettered pattern never matches numeric "(1)(2)"
    inline choices, so these parse as TITA with options=None) - for those,
    "Correct Answer: (1) 17" should resolve to the bare value "17", not
    the literal "(1) 17" with its index still attached."""
    if not correct_answer_raw:
        return None
    raw = correct_answer_raw.strip()
    m = ANSWER_LETTER_RE.match(raw)
    if m and options:
        idx = ord(m.group(1)) - ord("A")
        if 0 <= idx < len(options):
            return options[idx]
        return None
    m = ANSWER_NUM_INDEX_RE.match(raw)
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

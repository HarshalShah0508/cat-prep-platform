"""Parse a CAT DILR "Question Paper with Solutions" PDF (already converted
to plain text via `pdftotext -layout`) into structured question data - the
DILR sibling of pyq_varc_parser.py, reusing the exact same nested-numbering
template these vendor solutions PDFs share across sections:

    1. <data-set intro + full passage/data description>
    Correct Answer: —

    1.1. <question text>
    (A) ...
    (B) ...
    (C) ...
    (D) ...
    Correct Answer: (B) ...

    1.2. ...

Some DILR sets are genuinely chart/diagram-dependent - the passage text
only says "Given above is the schematic map of ..." etc. with no actual
chart data recoverable from the text layer. Those sets are detected via
CHART_REF_RE and flagged (not silently loaded with a broken/incomplete
passage) so they can be filled in later once the user supplies the actual
chart images.

Usage:
    python3 pyq_dilr_parser.py <text_file> <year> <slot>

Prints a JSON array of {"flagged_sets": [...], "questions": [...]}.
"""
import json
import re
import sys

HEADER_SUB_RE = re.compile(r"^(\d+)\.(\d+)\.\s*(.*)$")
HEADER_TOP_RE = re.compile(r"^(\d+)\.\s*(.*)$")
OPTION_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
CORRECT_ANSWER_RE = re.compile(r"^Correct Answer:\s*(.*)$")
PAGE_FOOTER_RE = re.compile(r"^\s*Page \d+ of \d+\s*$")
SOLUTION_RE = re.compile(r"^\s*Solution:\s*(.*)$")
QUICK_TIP_RE = re.compile(r"^\s*Quick Tip\s*$")
ANSWER_LETTER_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
ANSWER_BARE_LETTER_RE = re.compile(r"^([A-D])\s*$")
ANSWER_NUM_INDEX_RE = re.compile(r"^\((\d+)\)\s*(.*)$")
CHART_REF_RE = re.compile(
    r"\b(given|shown|depicted|illustrated|represented)\s+(above|below)\b|"
    r"\b(above|below)\s+is\b|"
    r"\b(figure|chart|diagram|graph|map|plot|network)\s+(above|below)\b|"
    r"\bthe\s+(following|below)\s+(figure|chart|diagram|graph|map|plot|image)\b|"
    r"\bas\s+(shown|depicted|illustrated)\b|"
    r"\bimage\d+-\d+\.png\b",
    re.IGNORECASE,
)


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
    """DILR solutions often include a numbered breakdown INSIDE the solution
    text itself (e.g. "1. Total goals scored..." "2. ..."), which - unlike
    VARC - can false-positive match a bare top-level "N." header even with
    the blank-line-preceded requirement. The reliable disambiguator: a real
    set/passage header is always terminated by the literal placeholder
    "Correct Answer: --" (an em dash - the set intro itself is never scored)
    - a solution-internal list never is. So top-level candidates are
    validated against their immediately-following "Correct Answer:" value;
    nested "N.M." sub-question headers are structurally specific enough
    (never used inside solution prose) to accept outright."""
    raw = []
    for i, ln in enumerate(lines):
        preceded_by_blank = i == 0 or lines[i - 1].strip() == ""
        if not preceded_by_blank:
            continue
        m_sub = HEADER_SUB_RE.match(ln)
        if m_sub:
            raw.append((i, "sub", int(m_sub.group(1)), int(m_sub.group(2)), m_sub.group(3)))
            continue
        m_top = HEADER_TOP_RE.match(ln)
        if m_top:
            raw.append((i, "top", int(m_top.group(1)), None, m_top.group(2)))

    headers = []
    for idx, cand in enumerate(raw):
        line_idx, kind, main, sub, first_text = cand
        if kind == "sub":
            headers.append(cand)
            continue
        end_idx = raw[idx + 1][0] if idx + 1 < len(raw) else len(lines)
        answer = None
        for i in range(line_idx + 1, end_idx):
            m = CORRECT_ANSWER_RE.match(lines[i])
            if m:
                answer = m.group(1).strip()
                break
        if answer is not None and answer.strip(" -—") == "":
            headers.append(cand)
        # else: false positive (a solution-internal numbered list item) -
        # silently dropped, its lines stay part of the preceding question's
        # body/solution text (already discarded past "Correct Answer:").
    return headers


def resolve_answer(correct_answer_raw, options):
    if not correct_answer_raw:
        return None
    raw = correct_answer_raw.strip()
    m = ANSWER_LETTER_RE.match(raw) or ANSWER_BARE_LETTER_RE.match(raw)
    if m and options:
        idx = ord(m.group(1)) - ord("A")
        if 0 <= idx < len(options):
            return options[idx]
        return None
    m = ANSWER_NUM_INDEX_RE.match(raw)
    if m:
        if options:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(options):
                return options[idx]
        return m.group(2).strip() or raw
    return raw


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
        for i in range(answer_line_idx + 1, end_idx):
            ln = lines[i]
            if QUICK_TIP_RE.match(ln.strip()):
                break
            m = SOLUTION_RE.match(ln.strip())
            if m:
                if m.group(1).strip():
                    sol_lines.append(m.group(1).strip())
                continue
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
        text = "\n".join(l for l in body_lines).strip()
        return text, None

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


def parse(text, year, slot):
    lines = clean_lines(text)
    headers = find_headers(lines)

    questions = []
    passage_text_by_main = {}
    flagged_sets = set()

    for idx, (line_idx, kind, main, sub, first_text) in enumerate(headers):
        end_idx = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        body_lines, correct_answer, solution_raw = extract_body(lines, line_idx, first_text, end_idx)
        question_text, options = split_options(body_lines)
        question_text = normalize_text(question_text)
        if options:
            options = [normalize_text(o) for o in options]
        resolved_answer = resolve_answer(correct_answer, options)

        if kind == "top":
            has_subs = any(h[1] == "sub" and h[2] == main for h in headers)
            if has_subs:
                passage_text_by_main[main] = question_text
                if CHART_REF_RE.search(question_text):
                    flagged_sets.add(main)
                continue
            questions.append(
                {
                    "number": f"{main}",
                    "group_id": None,
                    "passage_text": None,
                    "question_text": question_text,
                    "question_type": "TITA" if options is None else "MCQ",
                    "options": options,
                    "correct_answer_raw": correct_answer,
                    "correct_answer": resolved_answer,
                    "solution_raw": solution_raw,
                }
            )
        else:
            group_id = f"cat{year}_dilr_{slot}_set{main}"
            questions.append(
                {
                    "number": f"{main}.{sub}",
                    "group_id": group_id,
                    "set_main": main,
                    "passage_text": passage_text_by_main.get(main),
                    "question_text": question_text,
                    "question_type": "TITA" if options is None else "MCQ",
                    "options": options,
                    "correct_answer_raw": correct_answer,
                    "correct_answer": resolved_answer,
                    "solution_raw": solution_raw,
                }
            )

    return {"flagged_sets": sorted(flagged_sets), "questions": questions}


if __name__ == "__main__":
    path = sys.argv[1]
    year = sys.argv[2]
    slot = sys.argv[3]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    result = parse(text, year, slot)
    print(json.dumps(result, indent=2, ensure_ascii=False))

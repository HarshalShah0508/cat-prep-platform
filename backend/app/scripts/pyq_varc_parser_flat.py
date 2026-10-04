"""Parser for the CAT 2020 Slot 1 / Slot 3 VARC solutions PDF template - a
third distinct VARC template, different from both pyq_varc_parser.py
(2022-2025, nested "N."/"N.M." headers + lettered options) and
pyq_varc_parser_legacy.py (2021/2020-Slot2, flat numbering + NUMERIC
options that collide with header numbering).

This template uses flat "N." headers (1, 2, 3, ... with no passage-holder
sub-numbering) combined with LETTERED "(A)-(D)" options - so unlike the
2021 legacy template there is zero collision risk between header numbers
and option markers, and every "^\\d+\\.\\s" line can be trusted as a real
header outright, no anchoring trick needed.

Passage boundaries are marked by the same fixed boilerplate sentence used
in CAT 2020 Slot 2 ("The passage below is accompanied by a set of
questions. Choose the best answer to each question.") - always on its own
line(s) right before a new RC passage, never inside a question body.

Usage:
    python3 pyq_varc_parser_flat.py <text_file> <year> <slot>
"""
import json
import re
import sys

HEADER_RE = re.compile(r"^(\d+)\.\s+(.*)$")
OPTION_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
CORRECT_ANSWER_RE = re.compile(r"^Correct Answer:\s*(.*)$")
SOLUTION_RE = re.compile(r"^\s*Solution:\s*(.*)$")
QUICK_TIP_RE = re.compile(r"^\s*Quick Tip\s*$")
ANSWER_LETTER_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
ANSWER_BARE_LETTER_RE = re.compile(r"^([A-D])\s*$")
PAGE_FOOTER_RE = re.compile(r"^\s*\d+\s*$|^\s*Page \d+ of \d+\s*$")
MARKER_RE = re.compile(
    r"The passage below is accompanied by a set of questions\.", re.IGNORECASE
)
MARKER_CONT_RE = re.compile(r"^(each\s+)?question\.?\s*$", re.IGNORECASE)
STANDALONE_RE = re.compile(
    r"four sentences|five jumbled|followed by four alternate summaries",
    re.IGNORECASE,
)


def clean_lines(raw_text):
    raw_text = raw_text.replace("\f", "\n")
    lines = raw_text.split("\n")
    return [ln.rstrip() for ln in lines if not PAGE_FOOTER_RE.match(ln)]


def parse(text, year, slot):
    lines = clean_lines(text)

    marker_starts = [i for i, ln in enumerate(lines) if MARKER_RE.search(ln)]

    # Some papers' source PDFs have a stray General-Instructions numbered
    # list (1., 2., 3., ... copy-pasted from a different section's template)
    # before the real content starts - real questions never begin before
    # the first passage marker, so headers found earlier are discarded.
    first_marker = marker_starts[0] if marker_starts else 0

    headers = []  # (line_idx, number, first_line_text)
    for i, ln in enumerate(lines):
        if i < first_marker:
            continue
        m = HEADER_RE.match(ln.strip())
        if m:
            headers.append((i, int(m.group(1)), m.group(2)))

    questions = []
    rc_set_counter = 0
    current_group_id = None
    marker_ptr = 0

    for h_idx, (line_idx, number, first_text) in enumerate(headers):
        prev_header_end = headers[h_idx - 1][0] if h_idx > 0 else 0
        passage_text = None
        while marker_ptr < len(marker_starts) and marker_starts[marker_ptr] < line_idx:
            m_idx = marker_starts[marker_ptr]
            if m_idx >= prev_header_end:
                p_start = m_idx + 1
                if p_start < len(lines) and MARKER_CONT_RE.match(lines[p_start].strip()):
                    p_start += 1
                rc_set_counter += 1
                current_group_id = f"cat{year}_varc_{slot}_rc{rc_set_counter}"
                passage_text = normalize_text("\n".join(lines[p_start:line_idx]))
            marker_ptr += 1

        if passage_text is None and STANDALONE_RE.search(first_text):
            current_group_id = None

        end_idx = headers[h_idx + 1][0] if h_idx + 1 < len(headers) else len(lines)
        body_lines = [first_text]
        correct_answer = None
        answer_line_idx = None
        for i in range(line_idx + 1, end_idx):
            m = CORRECT_ANSWER_RE.match(lines[i].strip())
            if m:
                correct_answer = m.group(1).strip()
                answer_line_idx = i
                break
            body_lines.append(lines[i])

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

        question_text, options = split_lettered_options(body_lines)
        question_text = normalize_text(question_text)

        resolved_answer = resolve_answer(correct_answer, options)

        questions.append(
            {
                "number": str(number),
                "group_id": current_group_id,
                "passage_text": passage_text,
                "question_text": question_text,
                "question_type": "TITA" if options is None else "MCQ",
                "options": options,
                "correct_answer_raw": correct_answer,
                "correct_answer": resolved_answer,
                "solution_raw": solution_raw,
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
    return raw


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

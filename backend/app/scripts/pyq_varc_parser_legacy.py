"""Parser variant for the older CAT 2020/2021 VARC solutions PDF template,
which differs from 2022+ in two structural ways:

1. RC passages are introduced by a bare "Comprehension:" line (not a numbered
   question of their own) - the passage text follows directly, then the
   first real question of that set begins immediately.
2. Answer choices are numbered "1. 2. 3. 4." (not lettered "(A)(B)(C)(D)"),
   which collides visually with question numbering - a question header and
   its own answer choices use the identical "N." pattern.

   A strictly-increasing-number heuristic does NOT work here: a question's
   own answer choices (e.g. "2. tea drinking was...") can themselves equal
   "last confirmed header + 1" and get wrongly promoted to a fake new
   header, which then desyncs the expected-next counter for the rest of
   the document (confirmed bug on 2021 Slot 1 Q1).

   The reliable signal instead: every real question body ends with a
   "Correct Answer:" line (always present, one per question, never
   appears inside an answer choice). So each question's header is simply
   the first "N." line that appears AFTER the previous question's
   "Correct Answer:" line (skipping over "Solution:" / "Quick Tip" text in
   between) - and the very first header is the first "N." line in the
   whole document. This needs no number-continuity assumption at all.

Usage:
    python3 pyq_varc_parser_legacy.py <text_file> <year> <slot>

Prints a JSON array of question dicts to stdout, same shape as
pyq_varc_parser.py's output.
"""
import json
import re
import sys

NUM_LINE_RE = re.compile(r"^(\d+)\.\s+(.*)$")
PAREN_NUM_LINE_RE = re.compile(r"^\((\d+)\)\s*(.*)$")
CORRECT_ANSWER_RE = re.compile(r"^Correct Answer:\s*(.*)$")
SOLUTION_RE = re.compile(r"^\s*Solution:\s*(.*)$")
QUICK_TIP_RE = re.compile(r"^\s*Quick Tip\s*$")
ANSWER_PAREN_INDEX_RE = re.compile(r"^\((\d+)\)\s*(.*)$")
ANSWER_ROMAN_INDEX_RE = re.compile(r"^\((i|ii|iii|iv)\)\s*(.*)$", re.IGNORECASE)
ROMAN_TO_INDEX = {"i": 0, "ii": 1, "iii": 2, "iv": 3}
PAGE_FOOTER_RE = re.compile(r"^\s*\d+\s*$|^\s*Page \d+ of \d+\s*$")


def resolve_answer(correct_answer_raw, options):
    """Correct Answer lines here look like "(3) tea became the leading..." -
    but when that text wraps across physical lines, only the first line is
    ever captured (truncated mid-sentence). The index is still reliable
    though (options are numbered 1-4 in the same document order), so look
    the FULL option text up by position instead of trusting the raw
    (possibly truncated) trailing text."""
    if not correct_answer_raw:
        return None
    raw = correct_answer_raw.strip()
    m = ANSWER_PAREN_INDEX_RE.match(raw)
    if m:
        if options:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(options):
                return options[idx]
        return m.group(2).strip() or None
    m = ANSWER_ROMAN_INDEX_RE.match(raw)
    if m:
        idx = ROMAN_TO_INDEX[m.group(1).lower()]
        if options and 0 <= idx < len(options):
            return options[idx]
        return m.group(2).strip() or None
    return raw
COMPREHENSION_RE = re.compile(r"^Comprehension:\s*$", re.IGNORECASE)
# 2021 Slot 2's template: no "Comprehension:" line at all - a new RC set is
# introduced by "Instruction for questions N to M:" followed by a
# "Direction for Reading Comprehension: ... passage." sentence, then the
# passage itself.
INSTRUCTION_MARKER_RE = re.compile(
    r"^Instruction for questions\s+\d+\s+to\s+\d+\s*:\s*$", re.IGNORECASE
)
DIRECTION_RC_RE = re.compile(
    r"^Direction for Reading Comprehension:.*?passage\.\s*", re.IGNORECASE | re.DOTALL
)
STANDALONE_RE = re.compile(
    r"four sentences|five jumbled|followed by four alternate summaries",
    re.IGNORECASE,
)
# 2021 Slot 3 specifically: every header inlines a redundant
# "Comprehension: The passage below is accompanied..." label (see
# pyq_varc_parser_inline.py's docstring for why) - harmless to strip
# wherever it happens to appear verbatim at the start of a body.
INLINE_LABEL_PREFIX_RE = re.compile(
    r"^(Comprehension|Para Formation|Summary)\s*:\s*"
    r"(The passage below is accompanied by a set of questions\.\s*"
    r"Choose the best answer to each question\.\s*)?",
    re.IGNORECASE,
)


def clean_lines(raw_text):
    raw_text = raw_text.replace("\f", "\n")
    lines = raw_text.split("\n")
    return [ln.rstrip() for ln in lines if not PAGE_FOOTER_RE.match(ln)]


def parse(text, year, slot):
    lines = clean_lines(text)

    # Locate real question headers: the first "N." line in the doc, then
    # the first "N." line following each "Correct Answer:" line.
    headers = []  # (line_idx, number, first_line_text)

    def first_num_line_after(start_idx):
        for i in range(start_idx, len(lines)):
            m = NUM_LINE_RE.match(lines[i])
            if m:
                return i, int(m.group(1)), m.group(2)
        return None

    first = first_num_line_after(0)
    if first:
        headers.append(first)

    for i, ln in enumerate(lines):
        if CORRECT_ANSWER_RE.match(ln):
            nxt = first_num_line_after(i + 1)
            if nxt:
                headers.append(nxt)

    # Locate "Comprehension:" markers (or, in the template with no such
    # line, "Instruction for questions N to M:" markers) to know which
    # questions share a passage.
    comp_markers = [
        i
        for i, ln in enumerate(lines)
        if COMPREHENSION_RE.match(ln.strip()) or INSTRUCTION_MARKER_RE.match(ln.strip())
    ]

    questions = []
    rc_set_counter = 0
    current_group_id = None
    comp_idx_ptr = 0

    for h_idx, (line_idx, number, first_text) in enumerate(headers):
        # Does a "Comprehension:" marker fall between the previous header
        # (or doc start) and this one? If so, this question starts a new
        # passage group, and the passage text is everything between the
        # marker and this header.
        prev_line_idx = headers[h_idx - 1][0] if h_idx > 0 else -1
        passage_text = None
        while comp_idx_ptr < len(comp_markers) and comp_markers[comp_idx_ptr] < line_idx:
            if comp_markers[comp_idx_ptr] > prev_line_idx:
                passage_lines = lines[comp_markers[comp_idx_ptr] + 1 : line_idx]
                passage_raw = "\n".join(passage_lines)
                passage_raw = DIRECTION_RC_RE.sub("", passage_raw.strip(), count=1)
                passage_text = normalize_text(passage_raw)
                rc_set_counter += 1
                current_group_id = f"cat{year}_varc_{slot}_rc{rc_set_counter}"
            comp_idx_ptr += 1

        if passage_text is None and STANDALONE_RE.search(first_text):
            current_group_id = None

        first_text = INLINE_LABEL_PREFIX_RE.sub("", first_text)

        end_idx = headers[h_idx + 1][0] if h_idx + 1 < len(headers) else len(lines)
        body_lines = [first_text]
        correct_answer = None
        answer_line_idx = None
        for i in range(line_idx + 1, end_idx):
            m = CORRECT_ANSWER_RE.match(lines[i])
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

        question_text, options = split_numeric_options(body_lines)
        question_text = normalize_text(question_text)

        questions.append(
            {
                "number": str(number),
                "group_id": current_group_id,
                "passage_text": passage_text,  # only set on the first question of each set; filled in below
                "question_text": question_text,
                "question_type": "TITA" if options is None else "MCQ",
                "options": options,
                "correct_answer_raw": correct_answer,
                "correct_answer": resolve_answer(correct_answer, options),
                "solution_raw": solution_raw,
            }
        )

    # Backfill passage_text onto every question in a group (only the first
    # question of each set carries it from the loop above).
    last_passage = {}
    for q in questions:
        if q["passage_text"]:
            last_passage[q["group_id"]] = q["passage_text"]
        elif q["group_id"] in last_passage:
            q["passage_text"] = last_passage[q["group_id"]]

    return questions


def split_numeric_options(body_lines):
    """Options here are usually plain '1. text' / '2. text' lines (same
    NUM_LINE_RE pattern as headers, but local to this question's body -
    already isolated from other questions by the caller). A minority of
    question types ("Directions for Summary", paragraph-summary picks) use
    parenthesized '(1) text' options instead - try both patterns."""
    for pattern in (NUM_LINE_RE, PAREN_NUM_LINE_RE):
        result = _split_with_pattern(body_lines, pattern)
        if result[1] is not None:
            return result

    # Rare case: options embedded inline mid-paragraph, e.g.
    # "...collections. (2) This is in response..." - no option starts its
    # own line at all, so fall back to splitting the whole body on "(N)".
    full_text = " ".join(l.strip() for l in body_lines if l.strip())
    inline = re.split(r"\((\d)\)\s*", full_text)
    if len(inline) >= 9:  # question_text + 4 x (marker, option_text)
        question_text = inline[0].strip()
        opts = [inline[i].strip() for i in range(2, len(inline), 2)]
        return question_text, opts if opts else None

    return _split_with_pattern(body_lines, NUM_LINE_RE)


def _split_with_pattern(body_lines, pattern):
    option_start = None
    for i, ln in enumerate(body_lines):
        if i == 0:
            continue  # first line is the question header's own text
        if pattern.match(ln.strip()):
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
        m = pattern.match(stripped)
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

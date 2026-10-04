"""Parser for the older CAT 2020/2021 DILR solutions PDF template - the
DILR sibling of pyq_varc_parser_legacy.py:

    Comprehension:
    <data-set description, often including an ASCII-rendered table AND its
    own embedded numbered "additional facts" list ("1. ... 2. ...") - this
    is what breaks a naive "first/next N. line" header search, since those
    clue-list items are themselves blank-line-preceded "N." lines>

    1. <question text>
    (1) ...
    (2) ...
    (3) ...
    (4) ...
    Correct Answer: (4) ...

    2. ...

Header-finding uses the same fix built for pyq_qa_parser.py: a question's
own numeric answer choices (or a passage's own numbered clue list) can
collide with flat "N." header numbering, and several such false
candidates can cluster together (a whole clue list before the real first
question of a set) - so instead of guessing from raw number adjacency,
each real question is anchored to the "Quick Tip" line that universally
ends every question's solution (far more reliable here than "Correct
Answer:", which a meaningful fraction of these older papers omit for some
TITA questions): the real header is the LAST "N."-shaped candidate seen
before each "Quick Tip" line.

Some data sets are diagram/network-dependent (text only describes "the
figure above" etc.) - flagged via CHART_REF_RE, same as pyq_dilr_parser.py,
rather than silently loaded with a broken passage.

Usage:
    python3 pyq_dilr_parser_legacy.py <text_file> <year> <slot>
"""
import json
import re
import sys

from pyq_varc_parser_legacy import split_numeric_options

NUM_LINE_RE = re.compile(r"^(\d+)\.\s+(.*)$")
QDOT_LINE_RE = re.compile(r"^Q\.\s*(\d+)\s+(.*)$")
LETTER_OPTION_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
MIN_PASSAGE_CHARS = 150
# A DILR paper never has more than ~25 questions - this rejects obvious
# false matches like a year ("2017.") inside a solution sentence.
MAX_QUESTION_NUM = 25
CORRECT_ANSWER_RE = re.compile(r"^Correct Answer:\s*(.*)$")
SOLUTION_RE = re.compile(r"^Solution:\s*$")
QUICK_TIP_RE = re.compile(r"^\s*Quick Tip\s*$")
ANSWER_LETTER_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
ANSWER_PAREN_INDEX_RE = re.compile(r"^\((\d+)\)\s*(.*)$")
ANSWER_LETTER_DOT_RE = re.compile(r"^([A-D])\.\s*(.*)$")
STRICT_ANSWER_PHRASE_RE = re.compile(r"[Tt]he correct answer is\s+([^.\n]+)\.")
CONCLUSION_ANSWER_RE = re.compile(
    r"(?:is|total(?: number)? of [^,.\n]+ is)\s+([^.\n]+)\.\s*$",
    re.MULTILINE,
)
BARE_NUMBER_LINE_RE = re.compile(r"^\s*[\d,.\s\-–]+\s*$")


def resolve_answer(correct_answer_raw, options):
    if not correct_answer_raw:
        return None
    raw = correct_answer_raw.strip()
    m = ANSWER_LETTER_RE.match(raw) or ANSWER_LETTER_DOT_RE.match(raw)
    if m:
        if options:
            idx = ord(m.group(1)) - ord("A")
            if 0 <= idx < len(options):
                return options[idx]
        return m.group(2).strip() or None
    m = ANSWER_PAREN_INDEX_RE.match(raw)
    if m:
        if options:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(options):
                return options[idx]
        return m.group(2).strip() or raw
    return raw
PAGE_FOOTER_RE = re.compile(r"^\s*\d+\s*$|^\s*Page \d+ of \d+\s*$")
COMPREHENSION_RE = re.compile(r"^Comprehension:\s*$", re.IGNORECASE)
INSTRUCTION_MARKER_RE = re.compile(
    r"^Instruction for questions\s+\d+\s+to\s+\d+\s*:\s*$", re.IGNORECASE
)
CHART_REF_RE = re.compile(
    r"\b(given|shown|depicted|illustrated|represented)\s+(above|below)\b|"
    r"\b(above|below)\s+is\b|"
    r"\b(figure|chart|diagram|graph|map|plot|network)\s+(above|below)\b|"
    r"\bthe\s+(following|below)\s+(figure|chart|diagram|graph|map|plot|image)\b|"
    r"\bas\s+(shown|depicted|illustrated)\b|"
    r"\bimage\d+-\d+\.png\b",
    re.IGNORECASE,
)


BARE_DIGIT_LINE_RE = re.compile(r"^\s*\d+\s*$")


def clean_lines(raw_text):
    raw_text = raw_text.replace("\f", "\n")
    raw_lines = [ln.rstrip() for ln in raw_text.split("\n")]
    out = []
    for i, ln in enumerate(raw_lines):
        if BARE_DIGIT_LINE_RE.match(ln):
            # A lone number is usually a stripped page footer, but this
            # exact template also states a TITA answer as its own bare
            # line right before "Quick Tip" (no "Correct Answer:" label
            # for those questions) - never drop a bare number sitting
            # immediately before the Quick Tip marker.
            nxt = next((raw_lines[j].strip() for j in range(i + 1, min(i + 4, len(raw_lines))) if raw_lines[j].strip()), "")
            if QUICK_TIP_RE.match(nxt):
                out.append(ln)
                continue
            continue
        if PAGE_FOOTER_RE.match(ln):
            continue
        out.append(ln)
    return out


def parse(text, year, slot):
    lines = clean_lines(text)

    raw_candidates = []  # (line_idx, number, first_line_text)
    for i, ln in enumerate(lines):
        m = QDOT_LINE_RE.match(ln) or NUM_LINE_RE.match(ln)
        if m and int(m.group(1)) <= MAX_QUESTION_NUM:
            raw_candidates.append((i, int(m.group(1)), m.group(2)))

    anchor_positions = [i for i, ln in enumerate(lines) if QUICK_TIP_RE.match(ln)]

    # Real DILR questions are numbered increasing WITHIN a data set - some
    # papers (2021) number continuously through the whole paper, others
    # (2020) reset to 1 at the start of each new set. Combined with the
    # per-anchor window, "increasing since last_number" also rejects stray
    # number-shaped matches (a year like "2017." inside a solution
    # sentence). A reset is only trusted when the candidate is preceded by
    # a substantial block of new prose (a real passage, not just another
    # question's solution text) - otherwise a solution-internal "1. ..."
    # list would falsely look like a fresh set starting over.
    headers = []
    cand_ptr = 0
    window_start = 0
    last_number = 0
    for anchor_idx in anchor_positions:
        best = None
        while cand_ptr < len(raw_candidates) and raw_candidates[cand_ptr][0] < anchor_idx:
            cand = raw_candidates[cand_ptr]
            if cand[0] >= window_start:
                if cand[1] > last_number:
                    best = cand
                else:
                    gap_text = "\n".join(
                        l for l in lines[window_start : cand[0]] if l.strip()
                    ).strip()
                    if len(gap_text) > MIN_PASSAGE_CHARS:
                        best = cand
            cand_ptr += 1
        window_start = anchor_idx
        if best is not None:
            headers.append(best + (anchor_idx,))
            last_number = best[1]

    comp_markers = [
        i
        for i, ln in enumerate(lines)
        if COMPREHENSION_RE.match(ln.strip()) or INSTRUCTION_MARKER_RE.match(ln.strip())
    ]
    use_gap_heuristic = not comp_markers

    questions = []
    set_counter = 0
    current_group_id = None
    comp_idx_ptr = 0
    flagged_sets = set()
    for h_idx, (line_idx, number, first_text, _own_anchor_idx) in enumerate(headers):
        prev_line_idx = headers[h_idx - 1][0] if h_idx > 0 else -1
        passage_text = None

        if use_gap_heuristic:
            # No "Comprehension:"/"Instruction for questions" marker exists
            # anywhere in this file - fall back to detecting a new data set
            # by a substantial block of prose between the end of the
            # PREVIOUS question's Quick Tip box and this header. That span
            # starts with the tip's own short paragraph (always present,
            # never the passage) - drop it, then whatever's left is the
            # candidate passage.
            gap_start = headers[h_idx - 1][3] if h_idx > 0 else 0
            gap_paragraphs = [
                p for p in re.split(r"\n\s*\n", "\n".join(lines[gap_start:line_idx])) if p.strip()
            ]
            gap_text = "\n\n".join(gap_paragraphs[1:]) if len(gap_paragraphs) > 1 else ""
            if len(gap_text) > MIN_PASSAGE_CHARS:
                passage_text = normalize_text(gap_text)
                set_counter += 1
                current_group_id = f"cat{year}_dilr_{slot}_set{set_counter}"
                if CHART_REF_RE.search(passage_text):
                    flagged_sets.add(current_group_id)
        else:
            while comp_idx_ptr < len(comp_markers) and comp_markers[comp_idx_ptr] < line_idx:
                if comp_markers[comp_idx_ptr] > prev_line_idx:
                    passage_lines = lines[comp_markers[comp_idx_ptr] + 1 : line_idx]
                    passage_text = normalize_text("\n".join(passage_lines))
                    set_counter += 1
                    current_group_id = f"cat{year}_dilr_{slot}_set{set_counter}"
                    if CHART_REF_RE.search(passage_text):
                        flagged_sets.add(current_group_id)
                comp_idx_ptr += 1

        end_idx = headers[h_idx + 1][0] if h_idx + 1 < len(headers) else len(lines)
        body_lines = [first_text]
        correct_answer = None
        answer_line_idx = None
        solution_break_idx = None
        for i in range(line_idx + 1, end_idx):
            m = CORRECT_ANSWER_RE.match(lines[i])
            if m:
                correct_answer = m.group(1).strip()
                answer_line_idx = i
                break
            if SOLUTION_RE.match(lines[i]):
                solution_break_idx = i
                break
            body_lines.append(lines[i])
        prev_body_end = end_idx

        solution_raw = None
        if answer_line_idx is not None:
            sol_lines = []
            for i in range(answer_line_idx + 1, end_idx):
                ln = lines[i]
                if QUICK_TIP_RE.match(ln.strip()):
                    break
                m = SOLUTION_RE.match(ln.strip())
                if m:
                    continue
                sol_lines.append(ln)
            if sol_lines:
                solution_raw = normalize_text("\n".join(sol_lines))
        elif solution_break_idx is not None:
            # No "Correct Answer:" line exists for this question (some TITA
            # items in this template only state the answer inline at the
            # end of the solution prose, e.g. "The correct answer is 4.") -
            # capture the solution block anyway and pull the answer out of it.
            sol_lines = []
            for i in range(solution_break_idx + 1, end_idx):
                ln = lines[i]
                if QUICK_TIP_RE.match(ln.strip()):
                    break
                sol_lines.append(ln)
            if sol_lines:
                solution_raw = normalize_text("\n".join(sol_lines))
                bare_idx = [
                    i for i, ln in enumerate(sol_lines)
                    if ln.strip() and BARE_NUMBER_LINE_RE.match(ln.strip())
                ]
                if bare_idx:
                    # The real stated answer comes right after the solution's
                    # concluding sentence; a second bare-digit line after it
                    # (before Quick Tip) is a stray page-number artifact that
                    # slipped past clean_lines' footer filter - so prefer the
                    # FIRST bare-digit line, not the last.
                    correct_answer = sol_lines[bare_idx[0]].strip()
                else:
                    m = STRICT_ANSWER_PHRASE_RE.search(solution_raw) or CONCLUSION_ANSWER_RE.search(solution_raw)
                    if m:
                        correct_answer = m.group(1).strip().rstrip(".")

        question_text, options = split_options_multi(body_lines)
        question_text = normalize_text(question_text)

        if is_garbage(question_text):
            continue

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
        if q["passage_text"]:
            last_passage[q["group_id"]] = q["passage_text"]
        elif q["group_id"] in last_passage:
            q["passage_text"] = last_passage[q["group_id"]]

    return {"flagged_sets": sorted(flagged_sets), "questions": questions}


def is_garbage(question_text):
    """A header-boundary bug occasionally lands on a stray number inside
    solution prose rather than a real header - "Quick Tip" leaking into
    the question's own text (truncation never fired) or a "Try x = ..."/
    "Step N" guess-and-check opener are reliable tells."""
    if "Quick Tip" in question_text:
        return True
    if re.match(r"^(Try\s|Step\s\d|-\s)", question_text.strip()):
        return True
    if len(question_text.strip()) < 15:
        return True
    return False


def split_options_multi(body_lines):
    """Try numeric/parenthesized-numeric options first (split_numeric_options,
    shared with the VARC legacy template), then lettered "(A)-(D)" options
    (the 2020 Slot 1/3 DILR template uses these instead)."""
    question_text, options = split_numeric_options(body_lines)
    if options is not None:
        return question_text, options

    option_start = None
    for i, ln in enumerate(body_lines):
        if i == 0:
            continue
        if LETTER_OPTION_RE.match(ln.strip()):
            option_start = i
            break
    if option_start is None:
        return question_text, options

    question_lines = body_lines[:option_start]
    option_lines = body_lines[option_start:]
    options = []
    current = None
    for ln in option_lines:
        stripped = ln.strip()
        if not stripped:
            continue
        m = LETTER_OPTION_RE.match(stripped)
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

"""Parse a CAT VARC "Question Paper with Solutions" PDF (already converted to
plain text via `pdftotext -layout`) into structured question data, with zero
LLM transcription needed for the clean-text majority of VARC content.

These solutions PDFs follow a consistent structure for RC passages:
    1. <passage intro boilerplate + full passage text>
    Correct Answer: —

    1.1. <question text>
    (A) ...
    (B) ...
    (C) ...
    (D) ...
    Correct Answer: (B) ...

    1.2. ...

and standalone VA questions (para-jumbles etc.) as plain top-level numbers
with no sub-numbering:
    5. <question text>
    (A) ...
    Correct Answer: ...

Everything from "Correct Answer:" onward (the answer key + worked solution +
Quick Tip box) is discarded - this is a questions-only extraction pass.

Usage:
    python3 pyq_varc_parser.py <text_file> <year> <slot> [--topic-prefix X]

Prints a JSON array of question dicts to stdout. Run a human/visual spot
check on a sample before trusting the output wholesale - this handles the
consistent, common-case formatting; any file that deviates (different vendor
template, OCR artifacts) should be flagged for manual handling instead of
silently producing wrong data.
"""
import json
import re
import sys

HEADER_SUB_RE = re.compile(r"^(\d+)\.(\d+)\.\s*(.*)$")
HEADER_TOP_RE = re.compile(r"^(\d+)\.\s*(.*)$")
OPTION_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
CORRECT_ANSWER_RE = re.compile(r"^Correct Answer:\s*(.*)$")
SOLUTION_RE = re.compile(r"^\s*Solution:\s*(.*)$")
QUICK_TIP_RE = re.compile(r"^\s*Quick Tip\s*$")
ANSWER_LETTER_RE = re.compile(r"^\(([A-D])\)\s*(.*)$")
ANSWER_BARE_LETTER_RE = re.compile(r"^([A-D])\s*$")
PAGE_FOOTER_RE = re.compile(r"^\s*Page \d+ of \d+\s*$")


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


def clean_lines(raw_text):
    # pdftotext inserts a raw form-feed (page break) with no newline before
    # the next page's first character, which silently defeats '^' anchors on
    # that line (e.g. "\f1.1. All of..." - the "1.1." isn't at column 0).
    raw_text = raw_text.replace("\f", "\n")
    lines = raw_text.split("\n")
    out = []
    for ln in lines:
        if PAGE_FOOTER_RE.match(ln):
            continue
        out.append(ln.rstrip())
    return out


def find_headers(lines):
    """Return list of (index, kind, main, sub, first_line_text). A line only
    counts as a real question header if preceded by a blank line - this is
    what distinguishes a real "1.1." question header from an embedded
    sentence-list item inside a para-jumble question body (e.g. "1. What
    precisely are..." "2. It might be...") which runs on with no blank-line
    paragraph break before each numbered sentence."""
    headers = []
    for i, ln in enumerate(lines):
        preceded_by_blank = i == 0 or lines[i - 1].strip() == ""
        if not preceded_by_blank:
            continue
        m_sub = HEADER_SUB_RE.match(ln)
        if m_sub:
            headers.append((i, "sub", int(m_sub.group(1)), int(m_sub.group(2)), m_sub.group(3)))
            continue
        m_top = HEADER_TOP_RE.match(ln)
        if m_top:
            headers.append((i, "top", int(m_top.group(1)), None, m_top.group(2)))
    return headers


def extract_body(lines, start_idx, first_line_text, end_idx):
    """Body text from a header (inclusive of its own first-line remainder) up
    to the first 'Correct Answer:' line within [start_idx, end_idx). Also
    captures the raw solution text (from "Solution:" to "Quick Tip") as
    source material for a hand-rewritten explanation."""
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
    """Pull out (A)-(D) option lines (with wrapped continuations) from the
    end of a body; return (question_text_lines, options_or_None)."""
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
    # Collapse the line-wrap artifacts from -layout mode into flowing prose,
    # but keep explicit blank-line paragraph breaks.
    paragraphs = re.split(r"\n\s*\n", text)
    out = []
    for p in paragraphs:
        words = " ".join(l.strip() for l in p.split("\n") if l.strip())
        if words:
            out.append(words)
    return "\n\n".join(out)


def parse(text, year, slot, topic_prefix="VARC"):
    lines = clean_lines(text)
    headers = find_headers(lines)
    # Drop anything before the first real header (title/instructions block).
    headers = [h for h in headers if h[0] >= 0]

    questions = []
    passage_text_by_main = {}
    rc_set_counter = 0

    for idx, (line_idx, kind, main, sub, first_text) in enumerate(headers):
        end_idx = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        body_lines, correct_answer, solution_raw = extract_body(lines, line_idx, first_text, end_idx)
        question_text, options = split_options(body_lines)
        question_text = normalize_text(question_text)
        if options:
            options = [normalize_text(o) for o in options]
        resolved_answer = resolve_answer(correct_answer, options)

        if kind == "top":
            # Does this top-level number have sub-questions following it?
            has_subs = any(h[1] == "sub" and h[2] == main for h in headers)
            if has_subs:
                passage_text_by_main[main] = question_text
                rc_set_counter += 1
                continue  # not a real scored question itself
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
        else:  # sub-question under a passage
            group_id = f"cat{year}_varc_{slot}_rc{main}"
            questions.append(
                {
                    "number": f"{main}.{sub}",
                    "group_id": group_id,
                    "passage_text": passage_text_by_main.get(main),
                    "question_text": question_text,
                    "question_type": "TITA" if options is None else "MCQ",
                    "options": options,
                    "correct_answer_raw": correct_answer,
                    "correct_answer": resolved_answer,
                    "solution_raw": solution_raw,
                }
            )

    return questions


if __name__ == "__main__":
    path = sys.argv[1]
    year = sys.argv[2]
    slot = sys.argv[3]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    result = parse(text, year, slot)
    print(json.dumps(result, indent=2, ensure_ascii=False))

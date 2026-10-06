SECTION_GUIDANCE = {
    "VARC": (
        "Write either (a) a short 150-250 word reading-comprehension passage on a substantive "
        "topic (society, science, economics, culture, history, environment, or philosophy) "
        "followed by ONE question testing inference, main idea, tone, or the author's argument, "
        "or (b) a standalone verbal ability question of one of these types: a para-jumble "
        "(arrange 4 shuffled sentences into a coherent paragraph), a paragraph summary question, "
        "an odd-sentence-out question (one sentence among 5 that does not fit the paragraph), or "
        "a sentence-insertion question (a sentence is given, and a short paragraph has 4 marked "
        "blanks - identify which blank the given sentence best fits into). Pick the type that "
        "matches the requested topic below."
    ),
    "DILR": (
        "Write a compact data set (a short table, a set of logical conditions/clues, or a "
        "brief scenario with numeric data) followed by ONE question that requires "
        "interpreting or reasoning over that data set to arrive at a single answer."
    ),
    "QA": (
        "Write a standalone quantitative aptitude problem (arithmetic, algebra, number "
        "systems, geometry/mensuration, or modern math) that can be solved exactly using only "
        "the information given in the question."
    ),
}


# Appended to the base prompt when the caller asks for the harder "challenging" style
# (multi-step, disguised, non-direct) rather than the default "standard" style. Worded
# per-section since "tough" means something different for a math problem vs a passage.
CHALLENGING_STYLE_INSTRUCTIONS: dict[str, str] = {
    "QA": """
Make this question deliberately tough, lengthy to solve, and non-direct, matching the hardest
style of real CAT questions:
- Require at least 2-4 distinct logical/algebraic steps to reach the answer - never a single
  formula plugged in directly.
- Disguise the underlying technique inside a word problem or unfamiliar framing rather than
  stating it outright (e.g. don't say "find the HCF of..." - embed it in a scenario that
  requires the solver to first recognize HCF is what's needed).
- For MCQ, make the 3 incorrect options plausible results of common sign errors, off-by-one
  mistakes, or a wrong intermediate step - not just random nearby numbers a solver could rule
  out by estimation alone.
- The given information must be fully self-consistent - every stated condition must hold
  simultaneously for the one correct answer. Double-check this before finalizing.
""",
    "VARC": """
Make this question deliberately tough and non-direct, matching the hardest style of real CAT
VARC questions:
- For a Reading Comprehension question, write a denser passage (more nuanced argument,
  qualifications, or a shift in the author's position partway through) and ask a question that
  requires inference or synthesis across the whole passage - never a question answerable by
  spotting one directly-stated sentence.
- Make incorrect MCQ options plausible: each should be a partially-true restatement, an
  over-generalization of something the passage actually says, or a statement that reverses a
  subtle qualifier - not an option obviously unrelated to the passage.
- For para-jumble / sentence-insertion / odd-sentence-out questions, make the connecting logic
  depend on subtle transition words, pronoun references, or thematic continuity rather than an
  obvious topical mismatch a solver could spot without reading carefully.
- The correct answer must be unambiguous and fully defensible from the passage/paragraph text
  alone - double-check this before finalizing.
""",
    "DILR": """
Make this question deliberately tough and non-direct, matching the hardest style of real CAT
DILR questions:
- Build a data set or set of clues where the answer requires cross-referencing at least 2-3
  conditions together - never a single direct lookup in a table or a single clue read in
  isolation.
- For a puzzle, require at least one non-obvious case split or deduction step before the
  arrangement becomes fully determined - avoid puzzles solvable by filling slots in a single
  obvious pass.
- Make incorrect options plausible: each should be the result of satisfying all but one
  constraint, or of a common misreading of one clue - not a value with no connection to the
  data at all.
- The given data/clues must be fully self-consistent and must pin down exactly one correct
  answer - double-check this before finalizing.
""",
}


def build_cat_question_prompt(
    section: str,
    topic: str,
    difficulty: str,
    question_type: str,
    style: str = "standard",
    avoid_questions: list[str] | None = None,
) -> str:
    guidance = SECTION_GUIDANCE.get(section, SECTION_GUIDANCE["QA"])

    if question_type == "MCQ":
        options_instruction = (
            'Provide exactly 4 answer options in the "options" field as a list of 4 strings '
            '(only one of which is correct), and set "correct_answer" to the exact text of '
            "the correct option."
        )
    else:
        options_instruction = (
            'This is a TITA (Type In The Answer) question with no answer options: set '
            '"options" to null, and set "correct_answer" to the exact numeric or short-text '
            "answer that a candidate would type in."
        )

    style_instruction = (
        CHALLENGING_STYLE_INSTRUCTIONS.get(section, CHALLENGING_STYLE_INSTRUCTIONS["QA"])
        if style == "challenging"
        else ""
    )

    avoid_instruction = ""
    if avoid_questions:
        listed = "\n".join(f"- {q}" for q in avoid_questions)
        avoid_instruction = (
            "\nDo not repeat or closely paraphrase any of these previously-asked questions "
            f"(write a genuinely different question, even on the same topic):\n{listed}\n"
        )

    return f"""You are an expert CAT (Common Admission Test) question setter for the Indian MBA
entrance exam. Generate ONE original, high-quality {difficulty}-difficulty {question_type}
question for the {section} section, on the topic "{topic}".

{guidance}

{options_instruction}
{style_instruction}
{avoid_instruction}
Match the real CAT exam's style, tone, and difficulty calibration used by IIMs. Do not copy any
well-known published question verbatim; write an original question. Make sure the question is
fully self-contained and has exactly one correct, unambiguous answer.

Respond with ONLY a single JSON object with exactly these fields, and no other text:
{{
  "question_text": "<the full question, including any passage/data set it depends on>",
  "options": <a list of 4 strings for MCQ, or null for TITA>,
  "correct_answer": "<the correct answer, as exact text or a number>",
  "explanation": "<a clear, step-by-step explanation of why this is the correct answer>",
  "topic": "{topic}",
  "difficulty": "{difficulty}"
}}
"""


def build_verification_prompt(question_text: str, options: list[str] | None, claimed_answer: str) -> str:
    options_block = ""
    if options:
        lettered = "\n".join(f"({chr(65+i)}) {opt}" for i, opt in enumerate(options))
        options_block = f"\nOptions:\n{lettered}\n"

    return f"""You are an expert CAT exam solver. Solve the following question completely
independently, from scratch, showing your own reasoning - do not assume the claimed answer
below is correct.

Question:
{question_text}
{options_block}
Someone claims the correct answer is: {claimed_answer}

Solve the question yourself step by step, then state your own final answer, then compare it to
the claimed answer.

Respond with ONLY a single JSON object with exactly these fields, and no other text:
{{
  "computed_answer": "<the final answer you independently computed>",
  "matches": <true if your computed_answer is equivalent to the claimed answer, false otherwise>
}}
"""

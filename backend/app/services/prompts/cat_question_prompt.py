SECTION_GUIDANCE = {
    "VARC": (
        "Write either (a) a short 150-250 word reading-comprehension passage on a substantive "
        "topic (society, science, economics, culture, history, or philosophy) followed by ONE "
        "question testing inference, main idea, tone, or the author's argument, or (b) a "
        "standalone verbal ability question such as a para-jumble (arrange 4 shuffled "
        "sentences into a coherent paragraph), a paragraph summary question, or an "
        "odd-sentence-out question (one sentence among 5 that does not fit the paragraph)."
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


def build_cat_question_prompt(section: str, topic: str, difficulty: str, question_type: str) -> str:
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

    return f"""You are an expert CAT (Common Admission Test) question setter for the Indian MBA
entrance exam. Generate ONE original, high-quality {difficulty}-difficulty {question_type}
question for the {section} section, on the topic "{topic}".

{guidance}

{options_instruction}

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

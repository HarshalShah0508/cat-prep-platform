def build_cat_pi_model_answer_prompt(question_text: str) -> str:
    """Builds the prompt for a short, plain-language model answer to a PI question - shown
    to the candidate when their own answer scored below 7/10, so they have something concrete
    to learn from, not just critique."""
    return f"""
You are an experienced IIM Personal Interview (PI) panel member writing a strong model answer
to a PI question, for a candidate who scored below 7/10 on their own attempt.

Answer the question below directly yourself, the way a well-prepared, confident candidate
would answer it in a real admissions interview.

PI Question:
{question_text}

Rules:

- Write the answer in 5-6 short lines - no more.
- Use simple, plain words - the candidate should be able to read it once and understand it
  immediately.
- Write it as a direct first-person answer to the question, not as feedback or advice about
  the candidate's own answer - you were not given their answer and must not reference it.
- Do NOT add a preamble like "Here's a model answer:" - return only the answer text itself.
- Do NOT include markdown, headers, or bullet points - plain sentences.

Return ONLY the answer text.
""".strip()

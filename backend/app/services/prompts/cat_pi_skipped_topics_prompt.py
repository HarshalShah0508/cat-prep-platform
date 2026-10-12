from typing import List

from pydantic import BaseModel


class SkippedTopicsResponse(BaseModel):
    """Structured-output schema for build_cat_pi_skipped_topics_prompt's response - one
    topic per skipped question, in the same order."""

    topics: List[str]


def build_cat_pi_skipped_topics_prompt(question_texts: List[str]) -> str:
    """Builds a prompt that identifies, for each skipped PI question, the single specific
    topic the candidate should prepare. Batched into one request for every skipped question
    in a session, instead of one Gemini call per skipped question."""
    numbered_questions = "\n\n".join(
        f"Question {index + 1}:\n{text}" for index, text in enumerate(question_texts)
    )

    return f"""
You are helping an MBA candidate understand exactly what they should prepare after skipping
Personal Interview (PI) questions.

For EACH question below, identify ONE specific topic the candidate should prepare to be able
to answer it.

Rules:

- Return exactly one topic per question, in the same order as the questions.
- The topic must be a specific, concrete thing to prepare - not vague advice.
- Keep each topic short: roughly 2-6 words.

Do NOT return generic advice such as:
- Prepare better
- Improve communication
- Practice more
- Review fundamentals

Instead name the exact thing being tested.

Examples:

Question: Why do you want to pursue an MBA right now?
Topic: Why-MBA Narrative

Question: What's your view on India's current inflation trend?
Topic: India Inflation/RBI Policy

Question: Tell me about a time you led a team through a conflict.
Topic: Leadership/Conflict Story

Return ONLY valid JSON. Do not include markdown, code fences, or any text outside the JSON.

The JSON must be an array of exactly {len(question_texts)} strings, one topic per question,
in the same order as the questions below:

["Topic 1", "Topic 2", ...]

Questions:

{numbered_questions}
""".strip()

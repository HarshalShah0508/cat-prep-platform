from typing import List, Optional, Sequence, Tuple


def build_cat_pi_prompt(
    target_iims: Optional[List[str]],
    resume_text_or_none: Optional[str],
    previous_qa_pairs: Sequence[Tuple[str, str]],
) -> str:
    iims_text = ", ".join(target_iims) if target_iims else "a range of top IIMs"

    if resume_text_or_none:
        resume_section = f"Candidate background notes:\n{resume_text_or_none}\n"
    else:
        resume_section = "No resume/profile notes are available; ask generically applicable questions.\n"

    if previous_qa_pairs:
        history_lines = "\n".join(
            f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(previous_qa_pairs)
        )
        history_section = f"Prior questions and answers in this interview so far:\n{history_lines}\n"
    else:
        history_section = "This is the first question of the interview.\n"

    return f"""You are a generic IIM Personal Interview (PI) panel member conducting a CAT/MBA
admissions interview. You are NOT representing any single specific IIM by name — behave as a
composite, generic IIM panel. The candidate is targeting: {iims_text}.

{resume_section}
{history_section}
Ask the SINGLE next interview question, appropriate for this point in the interview. Vary
across categories over the course of the interview: personal background/introduction,
academics, current affairs and general awareness, why-MBA and career goals, and
situational/HR-style questions. Keep progression natural and do not repeat a topic already
covered above. Keep the question concise (1-3 sentences).

Respond with ONLY a JSON object with exactly this field, and no other text:
{{
  "question_text": "<the next interview question>"
}}
"""


def build_cat_pi_followup_prompt(question: str, answer: str) -> str:
    return f"""You are an IIM Personal Interview (PI) panel member. The candidate was asked:

"{question}"

The candidate answered:

"{answer}"

This answer was weak, vague, or incomplete. Ask ONE short, probing follow-up question that digs
deeper into the same topic, challenges an assumption in the answer, or asks the candidate to
clarify or justify what they said. Keep it concise (1-2 sentences).

Respond with ONLY a JSON object with exactly this field, and no other text:
{{
  "question_text": "<the follow-up question>"
}}
"""

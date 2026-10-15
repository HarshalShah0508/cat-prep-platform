from typing import Dict, Optional

BASE_QUESTION_COUNT = 8


def build_cat_pi_batch_prompt(
    target_percentile_min: Optional[float],
    target_percentile_max: Optional[float],
    resume_text_or_none: Optional[str],
    count: int = BASE_QUESTION_COUNT,
) -> str:
    """Builds a single prompt that asks Gemini for ALL questions of a PI session at once
    (batch-upfront, mirroring InterviewAI's generate-questions call), instead of the old
    one-question-at-a-time live generation."""
    if target_percentile_min and target_percentile_max:
        if target_percentile_min == target_percentile_max:
            percentile_text = (
                f"The candidate is targeting roughly the {target_percentile_min:.0f}th percentile.\n"
            )
        else:
            percentile_text = (
                f"The candidate is targeting roughly the {target_percentile_min:.0f}-"
                f"{target_percentile_max:.0f}th percentile range.\n"
            )
    else:
        percentile_text = ""

    if resume_text_or_none:
        resume_section = (
            "The candidate's resume/profile notes are below. Reference specific details from "
            "it (academic background, work experience, projects, extracurriculars) in at "
            "least 2-3 of the questions, the way a real panel would probe a candidate's "
            "actual profile - but keep the other questions generically applicable so the "
            "interview doesn't become a resume-only Q&A.\n\n"
            f"Resume/profile notes:\n{resume_text_or_none}\n"
        )
    else:
        resume_section = "No resume/profile notes are available; ask generically applicable questions.\n"

    return f"""You are a generic IIM Personal Interview (PI) panel conducting a CAT/MBA
admissions interview. You are NOT representing any single specific IIM by name - behave as a
composite, generic IIM panel.
{percentile_text}
{resume_section}
Generate EXACTLY {count} interview questions for this PI session, covering a natural spread
across these categories (don't label the categories, just vary across them naturally):
1. Personal background / "tell me about yourself" / introduction
2. Academic background (degree, subjects, academic performance)
3. Current affairs, general awareness, and business/economy knowledge
4. Why MBA, career goals, and why these target institutes
5. Situational, ethical, or HR-style questions (leadership, conflict, ambiguity)

Rules:
- Order the questions so the interview flows naturally (start with background/introduction,
  end with why-MBA/goals), without being mechanically "one question per category."
- Keep each question concise (1-3 sentences).
- Do not repeat a topic across questions.
- Do not number categories or explain your choices - only output the questions.

Return ONLY a numbered plain-text list, exactly in this format (no markdown, no extra
commentary before or after):

1. <first question>
2. <second question>
...
{count}. <last question>
"""


def build_cat_pi_followup_prompt(
    question: str,
    answer: str,
    evaluation: Optional[Dict] = None,
) -> str:
    evaluation_section = ""
    if evaluation:
        strengths = ", ".join(evaluation.get("strengths") or []) or "none noted"
        improvements = ", ".join(evaluation.get("improvements") or []) or "none noted"
        evaluation_section = f"""
This answer scored {evaluation.get("score")}/10.
Feedback given: {evaluation.get("feedback")}
Strengths noted: {strengths}
Areas to improve: {improvements}
"""

    return f"""You are an IIM Personal Interview (PI) panel member. The candidate was asked:

"{question}"

The candidate answered:

"{answer}"
{evaluation_section}
This answer was weak, vague, or incomplete. Ask ONE short, probing follow-up question that digs
deeper into the same topic, challenges an assumption in the answer, or asks the candidate to
clarify or justify what they said. Stay on exactly the same topic - do not introduce a new one.
Keep it concise (1-2 sentences).

Return ONLY the follow-up question text, no JSON, no preamble, no quotes.
"""

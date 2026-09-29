from typing import List

from pydantic import BaseModel

FOLLOW_UP_SCORE_THRESHOLD = 5
MAX_FOLLOW_UP_DEPTH = 2


class PIAnswerEvaluation(BaseModel):
    score: float
    feedback: str
    strengths: List[str]
    improvements: List[str]


def build_cat_pi_evaluation_prompt(question: str, answer: str) -> str:
    return f"""You are an experienced IIM Personal Interview (PI) panel member evaluating a
candidate's spoken answer during an MBA admissions interview.

Question asked:
"{question}"

Candidate's answer:
"{answer}"

Evaluate the answer on a scale of 1 to 10 (1 = very poor, 10 = excellent), considering clarity,
substance, structure, honesty, and relevance to the question that was asked. Give specific,
constructive feedback a real admissions panel might give.

Respond with ONLY a JSON object with exactly these fields, and no other text:
{{
  "score": <a float between 1 and 10>,
  "feedback": "<2-4 sentences of overall feedback>",
  "strengths": ["<specific strength>", "..."],
  "improvements": ["<specific area to improve>", "..."]
}}
"""

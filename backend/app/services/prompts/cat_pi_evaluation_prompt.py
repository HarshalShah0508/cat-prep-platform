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

Evaluate the answer on a scale of 1 to 10, considering clarity, substance, structure, honesty,
and relevance to the question that was asked. Give specific, constructive feedback a real
admissions panel might give.

Scoring bands:
- 1-3: Evasive, incoherent, or fails to address the question at all.
- 4-6: Partially addresses the question but is vague, unstructured, or thin on substance.
- 7-8: Clear, relevant, reasonably structured answer with only minor gaps.
- 9-10: Confident, well-structured, substantive answer that directly and fully addresses the
  question, with no notable gaps.

Respond with ONLY a JSON object with exactly these fields, and no other text:
{{
  "score": <a float between 1 and 10>,
  "feedback": "<2-4 sentences of overall feedback, written as advice from an experienced panel>",
  "strengths": ["<specific strength, 2-5 words, e.g. 'Clear structure'>", "..."],
  "improvements": ["<specific area to improve, 2-5 words, e.g. 'Lacked concrete examples'>", "..."]
}}

Return between 1 and 4 strengths and between 1 and 4 improvements. Avoid generic labels like
"good communication" or "needs more detail" - name the specific thing that was strong or weak.
"""

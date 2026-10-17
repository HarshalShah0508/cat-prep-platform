"""Backfill correct_answer for the 1 remaining unanswered CAT 2022 QA Slot 2
row (id 909), a TITA question, not covered by the earlier
backfill_qa_2022_slot2_answers.py / backfill_qa_2022_slot2_missing_questions.py
scripts. Matched directly by id, guarded so an already-filled correct_answer
is never overwritten.

Sourced from pyq-source/2022/QUANT_SLOT2_CAT_2022_SOLUTIONS.pdf, Q19: "The
number of integer solutions of the equation (x^2-10)^(x^2-3x-10) = 1 is".
The PDF's own solution is incomplete/sloppy - it lists x = +/-sqrt(11) as
"solutions" (from base = 1) even though those are irrational, not integers,
and it never explores the base = -1 (with even exponent) case at all, so its
narrative cannot be trusted verbatim. Re-derived independently instead:
  - base = 1: x^2 = 11 -> irrational, not integer solutions (excluded,
    since the question asks for INTEGER solutions).
  - base = -1 with even exponent: x^2 - 10 = -1 -> x = +/-3; exponent at
    x=3 is 9-9-10=-10 (even, valid), at x=-3 is 9+9-10=8 (even, valid).
  - exponent = 0 with base != 0: x^2-3x-10=0 -> x=5 (base 15, valid) or
    x=-2 (base -6, valid).
  Integer solutions: {3, -3, 5, -2} -> count = 4.

Run with:
    python -m app.scripts.backfill_qa_2022_slot2_remaining_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot2"

ANSWERS = [
    (909, "4"),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, correct_answer in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "QA",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={question_id}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} remaining answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

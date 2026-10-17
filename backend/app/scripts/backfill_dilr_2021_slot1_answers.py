"""Backfill missing correct_answer/explanation for CAT 2021 DILR Slot 1 PYQ rows.

Source: pyq-source/2021/DILR_SLOT1_CAT_2021_SOLUTIONS.pdf (question 15 of the
"Juice business" set - milk units used by three women).

Matched by id directly (ids were pulled from a DB query for
source='pyq' AND source_year=2021 AND source_slot='slot1' AND section='DILR'
AND correct_answer IS NULL). Every update is guarded by
`correct_answer.is_(None)` so an already-answered row can never be clobbered.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot1"

# id -> (correct_answer, explanation)
ANSWERS = {
    499: (
        "Either 18 or 19 or 20 units.",
        "Four of the five products (mango, apple, banana and mixed-fruit smoothie) use one "
        "unit of milk each, and only fruit salad does not. Working out each woman's profit per "
        "product from the per-unit costs and matching it against their four-hour revenue totals "
        "(Ganga = 103, Kaveri = 98, Narmada = 104) while respecting the 'no banana leftover' and "
        "'exactly one leftover of a non-banana item' constraints pins the total initial milk down "
        "to a range of 18, 19 or 20 units - no single exact value can be determined.",
    ),
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, (correct_answer, explanation) in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH / already answered: id={question_id}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

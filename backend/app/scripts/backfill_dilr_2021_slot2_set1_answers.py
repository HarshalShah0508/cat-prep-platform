"""Backfill correct_answer for CAT 2021 DILR Slot 2 Set 1 (shipping-categories
Gantt chart set, group_id cat2021_dilr_slot2_set1), matched by (source_year,
source_slot, section, question_text).

Only Q3 is backfilled here - its answer is explicitly stated as "Correct
Answer: (1) Art, Binders, Paper, Phones" in the official solutions PDF. Q1,
Q2, and Q4 are NOT backfilled: no answer key (marked checkmark or stated
"Correct Answer") was ever seen for any of them, and this slot's solutions
PDF is known low-quality (Q2's own solution explicitly says it can't compute
the answer without extracting chart data), so nothing is guessed.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot2_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot2"

ANSWERS = [
    (
        "The sequence of categories -- Art, Binders, Paper and Phones -- in decreasing order "
        "of average processing time of their orders in this period is:",
        "Art, Binders, Paper, Phones",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.question_text == question_text,
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

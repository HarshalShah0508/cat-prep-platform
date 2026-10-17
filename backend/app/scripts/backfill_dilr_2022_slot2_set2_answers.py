"""Backfill correct_answer for CAT 2022 DILR Slot 2 Set 2 (delivery-route
set, group_id cat2022_dilr_slot2_set2), id 569 only - the one row in this
set left unanswered. Matched directly by id, guarded so an already-filled
correct_answer is never overwritten.

Sourced from pyq-source/2022/DILR_SLOT2_CAT_2022_SOLUTIONS.pdf, Q2.1: "If
the last location visited is Ahmednagar, then what is the total distance
covered in the route (in km)?" -> route order C-B-D-A, distances
12 + 4 + 12 + 7 = 35 km.

Run with:
    python -m app.scripts.backfill_dilr_2022_slot2_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot2"

ANSWERS = [
    (569, "35"),
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
                    CatQuestion.section == "DILR",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

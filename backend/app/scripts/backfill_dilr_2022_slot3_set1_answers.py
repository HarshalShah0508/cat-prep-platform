"""Backfill correct_answer for CAT 2022 DILR Slot 3 Set 1 (mortality-tracking
set, group_id cat2022_dilr_slot3_set1), ids 584-588. Matched directly by id,
guarded so an already-filled correct_answer is never overwritten.

Sourced from pyq-source/2022/DILR_SLOT3_CAT_2022_SOLUTIONS.pdf:
  - Q1.1 (id 584): "In 2000, what was the ratio of the number of dead
    males to dead females..." -> Correct Answer: (B) 71 : 69
  - Q1.2 (id 585): "...30 and 40 years of age in 1980 survived until
    2010?" -> Correct Answer: (C) 190
  - Q1.3 (id 586): "...less than 30 years of age in 1980 survived until
    2020?" -> Correct Answer: (A) 470
  - Q1.4 (id 587, TITA): "...males...between 20 and 30...died in the
    period 2000 to 2010?" -> 210 alive in 2000 minus 170 alive in 2010 = 40
  - Q1.5 (id 588, TITA): "...females...between 20 and 30...died between
    the ages of 50 and 60?" -> 210 alive at 50-60 (2010) minus 180 alive at
    60-70 (2020) = 30

Run with:
    python -m app.scripts.backfill_dilr_2022_slot3_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot3"

ANSWERS = [
    (584, "71 : 69"),
    (585, "190"),
    (586, "470"),
    (587, "40"),
    (588, "30"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

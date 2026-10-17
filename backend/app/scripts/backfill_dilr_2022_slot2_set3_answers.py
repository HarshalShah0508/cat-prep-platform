"""Backfill correct_answer for CAT 2022 DILR Slot 2 Set 3 (company
profit/loss set, group_id cat2022_dilr_slot2_set3), ids 574-578. Matched
directly by id, guarded so an already-filled correct_answer is never
overwritten.

Sourced from pyq-source/2022/DILR_SLOT2_CAT_2022_SOLUTIONS.pdf:
  - Q3.1 (id 574): "Considering all three years, which company had the
    highest annual profit?" -> Company C (profit 85)
  - Q3.2 (id 575): "Which of the four companies experienced the highest
    annual loss in any of the years?" -> Correct Answer: (D) Company D
  - Q3.3 (id 576): "...lowest value of this ratio in 2019?" -> Correct
    Answer: (D) Company A
  - Q3.4 (id 577): "total number of employees lost in 2019 and 2020 was
    the least for" -> Correct Answer: (B) Company B
  - Q3.5 (id 578): "...which of the four companies had the highest profit
    per employee?" -> Correct Answer: (A) Company B

Run with:
    python -m app.scripts.backfill_dilr_2022_slot2_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot2"

ANSWERS = [
    (574, "Company C"),
    (575, "Company D"),
    (576, "Company A"),
    (577, "Company B"),
    (578, "Company B"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

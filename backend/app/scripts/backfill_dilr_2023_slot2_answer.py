"""Backfill the 1 CAT 2023 DILR Slot 2 answer missing from the DB (id 359).
Run with: python -m app.scripts.backfill_dilr_2023_slot2_answer
"""
from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion


def backfill() -> None:
    db = SessionLocal()
    try:
        row = db.query(CatQuestion).filter(CatQuestion.id == 359).first()
        row.question_type = "TITA"
        row.correct_answer = "9"
        row.explanation = (
            "Working through the 3x3 grid of boxes (each with 3 sacks, row/column sums of 45, box "
            "totals divisible by 3, and the median/minimum/count-above-5 clues in the two given tables), "
            "exactly 9 of the 27 sacks end up holding exactly one coin."
        )
        db.commit()
        print("Backfilled id=359.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

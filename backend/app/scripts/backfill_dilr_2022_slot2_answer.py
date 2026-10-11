"""Backfill the 1 CAT 2022 DILR Slot 2 answer missing from the DB (id 754).
Run with: python -m app.scripts.backfill_dilr_2022_slot2_answer
"""
from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion


def backfill() -> None:
    db = SessionLocal()
    try:
        row = db.query(CatQuestion).filter(CatQuestion.id == 754).first()
        row.question_type = "TITA"
        row.correct_answer = "50"
        row.explanation = (
            "Working through the set's FDA/EU approval table (320 products split by domestic/foreign and "
            "cosmetic/nutrition categories), fixing nutrition products without EU approval at 50 pins down "
            "domestic nutrition's without-EU count, which in turn forces the domestic cosmetics' "
            "without-EU-approval count to also be 50."
        )
        db.commit()
        print("Backfilled id=754.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

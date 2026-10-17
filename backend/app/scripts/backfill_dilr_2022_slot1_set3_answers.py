"""Backfill correct_answer for CAT 2022 DILR Slot 1 Set 3 (token-funding set,
group_id cat2022_dilr_slot1_set3), ids 555 and 558. Matched directly by id,
guarded so an already-filled correct_answer is never overwritten.

Sourced from pyq-source/2022/DILR_SLOT1_CAT_2022_SOLUTIONS.pdf:
  - Q3.2 (id 555): "Who among the following definitely received a token
    from Bithi but not from Dhanavi?" -> Correct Answer: (C) Pragnyaa
  - Q3.5 (id 558): "Which of the following could be the amount of funding
    that Tantra received? (a) Rs. 66,000 (b) Rs. 165,000" -> Correct
    Answer: (C) Both (a) and (b)

Run with:
    python -m app.scripts.backfill_dilr_2022_slot1_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot1"

ANSWERS = [
    (555, "Pragnyaa"),
    (558, "Both (a) and (b)"),
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

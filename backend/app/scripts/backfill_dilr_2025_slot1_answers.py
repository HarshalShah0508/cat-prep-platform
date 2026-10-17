"""Backfill missing correct_answer/explanation for CAT 2025 DILR Slot 1.

Source: pyq-source/2025/DILR_SLOT1_CAT_2025_SOLUTIONS.pdf

Matched by id directly (safer than text match for TITA questions with
short/plain wording). Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        708,
        "4",
        "Dolly, Falguni, Bunty and Eklavya all have Q3 scores forced by the clues "
        "(constant ratings, the Q2 demotion/given rating, and Eklavya's Elite-trio "
        "constraint); only Asha's and Chintu's Q1 Elite ratings remain free, so "
        "exactly 4 employees have a Quarter 3 score that can be determined with certainty.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH for id={qid}")
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

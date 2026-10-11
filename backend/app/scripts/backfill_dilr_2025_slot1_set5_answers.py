"""Backfill correct_answer for CAT 2025 DILR Slot 1 Set 5 (tapping-game
logic puzzle, group_id cat2025_slot1_set5), matched by (source_year,
source_slot, section, question_text).

Solved from scratch via the full 5x4 response matrix (fully determined by
systematic elimination from the 6 given facts). Confidence is high: the
derived total taps per person (Alia=6, Badal=6, Clive=8, Dilshan=11,
Ehsaan=9) sum to exactly 40 and match facts 1/2 exactly (Alia=6, Dilshan=11,
Ehsaan=9 all given directly), fact 6 (Clive>Badal, 8>6) is what broke the
one remaining tie in the derivation, and fact 4 (nobody "Yes" more than
twice) holds for all five people in the final matrix - independent
cross-checks all passed.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot1_set5_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How many taps did Clive receive for his question?", "7"),
    ("Which two people tapped an equal number of times in total?", "Alia and Badal"),
    ("What was Clive's response to Ehsaan's question?", "No"),
    ("How many \"Yes\" responses were received across all the questions?", "6"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 5 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill correct_answer for CAT 2025 DILR Slot 2 Set 1 (balls and hoops
puzzle, group_id cat2025_slot2_set1), matched by (source_year, source_slot,
section, question_text).

Solved via size-ordering deduction: hoop order works out to H2 < H3 < H4 <
H1 (derived via chained comparisons through B1 and B4/B2's ping patterns),
which lands exactly on one of Q3's four given options - a strong
independent check. Q1, Q4 computed from the full 6x4 ping grid; Q2 found
by checking each option's two inequalities against what's actually forced
versus merely possible.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot2_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("What was the total number of pings made by B1, B2, and B3?", "6"),
    (
        "Which of the following statements about the relative sizes of the balls is NOT "
        "NECESSARILY true?",
        "B1 < B6 < B3",
    ),
    (
        "Which of the following statements about the relative sizes of the hoops is true?",
        "H2 < H3 < H4 < H1",
    ),
    (
        "What BEST can be said about the total number of pings from all the tests "
        "undertaken?",
        "12 or 13",
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

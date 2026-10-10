"""Backfill correct_answer for CAT 2024 DILR Slot 2 Set 2 (staircase grid
number-placement set, group_id cat2024_slot2_dilr_set2), matched by
(source_year, source_slot, section, question_text).

Answers come from a user-supplied answer-key screenshot (all 5 questions had
a stated "Correct Answer" / "Possible Answer"). Previously this set was
skipped entirely as "grid shape ambiguous"; the same screenshots resolved
that ambiguity too: Row 1 has 4 slots, Row 2 has 3, Row 3 has 2, Row 4 has 1.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot2_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot2"

ANSWERS = [
    (
        "What is the row number which has the least sum of numbers placed in that row?",
        "4",
    ),
    (
        "Which of the following statements MUST be true?\n"
        "I. 10 is placed in a slot in Row 1.\n"
        "II. 1 is placed in a slot in Row 4.",
        "Both I and II",
    ),
    (
        "Which of the following statements MUST be true?\n"
        "I. 2 is placed in a slot in Column 2.\n"
        "II. 3 is placed in a slot in Column 3.",
        "Neither I nor II",
    ),
    (
        "For how many slots in the grid, placement of numbers CANNOT be determined with "
        "certainty?",
        "2",
    ),
    ("What is the sum of the numbers placed in Column 4?", "26"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill correct_answer for CAT 2020 DILR Slot 3 Set 1 (mango/teak/pine
tree-distribution set, group_id cat2020_dilr_slot3_set1), matched by
(source_year, source_slot, section, question_text). Answers come from a
user-supplied answer-key screenshot (all 6 questions had a stated
"Correct Answer").

Run with:
    python -m app.scripts.backfill_dilr_2020_slot3_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("How many mango trees were there in total?", "98"),
    (
        "Which of the following is the correct sequence of trees received by Abha, Bina, "
        "Chitra, and Dipti in that order?",
        "50, 69, 30, 56",
    ),
    ("How many pine trees did Chitra receive?", "18"),
    (
        "Who got the plot with the smallest number of trees and how many trees did that plot "
        "have?",
        "Bina, 3 trees",
    ),
    ("Which of the following statements is NOT true?", "Bina got 32 pine trees."),
    ("Which column had the highest number of trees?", "4"),
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

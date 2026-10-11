"""Backfill correct_answer for CAT 2025 DILR Slot 1 Set 1 (circular-table
seating puzzle, group_id cat2025_slot1_set1), matched by (source_year,
source_slot, section, question_text).

Solved from scratch from the passage's own constraints (no external answer
key available). Chair layout derived: Aslam=6, Bashir=4, Chhavi=7, Davies=2
initially (chairs 1,3,5 empty). Move sequence forced almost entirely by the
"adjacent only at end of Turn 2 and Turn 6" constraint, which eliminates all
but one branch at each ambiguous choice point except the very last move
(C's Turn 7 direction), which stays genuinely undetermined by the given
facts - but both of its branches land on the same answer for the question
that depends on it (Q4), so that residual ambiguity doesn't affect any
answer here.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot1_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("What is the number of the chair initially occupied by Bashir?", "4"),
    ("Who sits on the chair numbered 4 at the end of Turn 3?", "No one"),
    (
        "Which of the chairs are occupied at the end of Turn 6?",
        "Chairs numbered 4, 5, 6, and 7",
    ),
    (
        "Which of the following BEST describes the friends sitting on chairs adjacent to "
        "the one occupied by Bashir at the end of Turn 7?",
        "Davies only",
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

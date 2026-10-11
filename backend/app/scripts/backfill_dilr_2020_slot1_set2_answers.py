"""Backfill correct_answer for CAT 2020 DILR Slot 1 Set 2 (institutes/vendors
contracts set, group_id cat2020_dilr_slot1_set2), matched by (source_year,
source_slot, section, question_text).

Solved from scratch (no solutions PDF available for this slot - see
seed_cat_pyq_2020_dilr.py's docstring). Unique solution found by exhaustive
branch elimination on which two institutes' multi-year contracts pair with
vendor Z (needs to cover all 10 years 2010-2019) vs vendor X (needs to cover
exactly 2010-2015): the only internally consistent assignment, respecting
"D had no contract in 2010" and "C had no contract in 2011", is:
  A: 3yr multi with X (2010-2012), single with W (2012)
  B: 7yr multi with Z (2010-2016), single with Y (2010)
  C: 3yr multi with Z (2017-2019), single with W (2012)
  D: 4yr multi with X (2012-2015), single with Y (2019)
This reproduces all 7 given facts exactly, including the "5 contracts active
in 2012" count, and every answer below lands cleanly on one of the given
MCQ options.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot1_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("In which of the following years were there two or more contracts?", "2015"),
    (
        "Which of the following is true?",
        "D had a contract with Y in 2019",
    ),
    ("In how many years during this period was there only one contract?", "3"),
    (
        "What BEST can be concluded about the number of contracts in 2010?",
        "exactly 3",
    ),
    (
        "Which institutes had multiple contracts during the same year?",
        "A and B only",
    ),
    (
        "Which institutes and vendors had more than one contract in any year?",
        "A, B, W, and X",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

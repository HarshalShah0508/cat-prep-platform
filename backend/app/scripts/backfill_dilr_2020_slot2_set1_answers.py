"""Backfill correct_answer for CAT 2020 DILR Slot 2 Set 1 (25-bead
grid-colouring set, group_id cat2020_dilr_slot2_set1), matched by
(source_year, source_slot, section, question_text).

Solved from scratch (no solutions PDF available for this slot - questions
recovered via OCR earlier this session). Only 2 of the 4 questions are
backfilled here:

Q1 (2-colour configurations): proven that Red can never be one of only two
colours used (a 2-colour grid is forced into a checkerboard by rule 1,
which puts multiple Reds in every line with nothing but the other colour
between them, violating rule 3's requirement for both a Blue and a Green
between any two Reds). So the only viable 2-colour pair is Blue+Green,
giving exactly 2 checkerboard phases. Answer: 2.

Q2 (max Red beads): proven that two Reds in the same row/column need a gap
of at least 3 cells (to fit both a Blue and a Green between them), capping
any line at 2 Reds, and that two lines can share a Red-column/row pair only
if those lines are themselves >=3 apart (so rows 1&4, 1&5, or 2&5 can reuse
the same pair of columns, but row 3 can never share a column with any other
row, capping it at 1). Construction: rows 1 and 4 use columns {1,4}, rows 2
and 5 use columns {2,5}, row 3 uses column 3 alone - 2+2+2+2+1 = 9 Reds,
and this is provably the maximum (row 3 cannot be pushed to 2 without
freeing a second column nobody else touches, which only loses more Reds
elsewhere than it gains). Answer: 9.

Q3 (min Blue beads) and Q4 (extra Reds from a partial placement) require a
full valid 2D grid construction that was not reached with confidence in the
time available - left unanswered rather than guessed.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot2_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("The total number of possible configurations using beads of only two colours Is:", "2"),
    (
        "What is the maximum possible number of Red beads that can appear in any "
        "configuration?",
        "9",
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

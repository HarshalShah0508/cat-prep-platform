"""Backfill correct_answer for CAT 2020 DILR Slot 1 Set 5 (1000-patient
medicine-treatment Venn set, group_id cat2020_dilr_slot1_set5), matched by
(source_year, source_slot, section, question_text).

Solved from scratch (no solutions PDF available for this slot). Treatment
group size = 500 (half of 1000). Working through the given region values:
A-only=25, C-only=20, D-only=10, B-only=75-25-20-10=20 (exactly-one total
is 75). ABC(not D)=40, ACD(not B)=20 given; exactly-three total=100, so
ABD+BCD=40. Using A's total (250) to solve ABD=30, hence BCD=10. Using C's
total (210) to solve BC-only=20. Assuming every treatment-group patient
received at least one medicine (so all regions sum to exactly 500, matching
why they were put in the treatment group at all) gives the one remaining
unknown, BD-only=150.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot1_set5_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How many patients were treated with medicine type B?", "340"),
    (
        "The number of patients who were treated with medicine types B, C, and D, but "
        "not type A was:",
        "10",
    ),
    ("How many patients were treated with medicine types B and D only?", "150"),
    ("The number of patients who were treated with medicine type D was:", "325"),
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

"""Backfill correct_answer/explanation for CAT 2020 DILR Slot 1 Set 1
(APP-CAB drivers' rating/bonus set, group_id cat2020_dilr_slot1_set1).
Matched by primary key id (safer than text matching given the set's short,
similar-looking question stems). Answers come from
DILR_SLOT1_CAT_2020_SOLUTIONS.pdf in pyq-source/2020/.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot1_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        413,
        "3.6",
        "To not get a bonus, Damodaran must have a rating of 1 in at least one of his five "
        "parameters. Maximizing his final rating subject to that constraint, per the official "
        "key, gives a maximum possible final rating of 3.6.",
    ),
    (
        414,
        "3.0",
        "For Eman to qualify for a bonus he needs a rating of 5 in at least one parameter. "
        "Minimizing his final rating subject to that constraint, per the official key, gives a "
        "minimum possible final rating of 3.0.",
    ),
    (
        415,
        "1600",
        "Comparing each driver's fixed payment plus bonus (bonus rate x final rating) when all "
        "five drivers qualify for a bonus, the smallest possible total monthly payment across "
        "the five drivers, per the official key, is Rs.1600.",
    ),
    (
        416,
        "2050",
        "The maximum possible monthly payment occurs when a driver's final rating is pushed to "
        "its highest possible value (5) under the constraints; per the official key, the "
        "largest possible monthly payment across the five drivers is Rs.2050.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, correct_answer, explanation in ANSWERS:
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
                print(f"NO MATCH (or already set): id={question_id}")
                continue
            if row.options and correct_answer not in row.options:
                print(f"WARNING: answer {correct_answer!r} not in options for id={question_id}: {row.options}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

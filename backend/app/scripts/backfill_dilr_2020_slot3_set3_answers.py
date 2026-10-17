"""Backfill correct_answer/explanation for CAT 2020 DILR Slot 3 Set 3
(XYZ grocery delivery set, group_id cat2020_dilr_slot3_set3). Matched by
primary key id. Answers come from DILR_SLOT3_CAT_2020_SOLUTIONS.pdf in
pyq-source/2020/.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot3_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot3"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        473,
        "15th",
        "The fraction of lost orders for a day is (orders lost that day) / (orders booked that "
        "day). Computing this for each candidate day from the cumulative booked/lost figures, "
        "the 15th has the largest fraction of orders lost.",
    ),
    (
        474,
        "13th",
        "Orders booked on a given day equal the cumulative-booked figure for that day minus the "
        "cumulative-booked figure for the previous day. Among the candidate days, the 13th had "
        "the highest number of orders booked.",
    ),
    (
        475,
        "14th",
        "The delivery ratio is (orders delivered the next day) / (orders delivered the day "
        "after). Computing this for each candidate day using the next-day and second-day "
        "delivery counts, the 14th has the highest delivery ratio.",
    ),
    (
        476,
        "14th",
        "The average delivery time uses the formula (x+2y)/(x+y), where x is orders delivered "
        "the next day and y is orders delivered the day after. Evaluating this for each "
        "candidate day, the 14th gives the least average delivery time.",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

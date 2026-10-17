"""Backfill correct_answer/explanation for CAT 2020 DILR Slot 3 Set 4
(600-schools OTLP-facilities set, group_id cat2020_dilr_slot3_set4).
Matched by primary key id. Answers come from
DILR_SLOT3_CAT_2020_SOLUTIONS.pdf in pyq-source/2020/.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot3_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot3"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        477,
        "200",
        "Using the inclusion-exclusion breakdown of the 600 schools (80 with none, 40 with "
        "all four, fixed counts for exactly-one-facility schools, and the fact that the "
        "exactly-three-facilities count is the same for every choice of three), the total "
        "number of schools with exactly three of the four facilities is 200.",
    ),
    (
        478,
        "185",
        "Applying the inclusion-exclusion principle with the given totals for F2 overall, "
        "F1-and-F2, all-four-facilities, and the only-F2-and-F3 count, the number of schools "
        "having both F2 and F4 works out to 185.",
    ),
    (
        479,
        "42",
        "Using the known only-one-facility counts together with the inclusion-exclusion "
        "relationships among the facility totals, the number of schools having only F1 and F3 "
        "(and neither F2 nor F4) works out to 42.",
    ),
    (
        480,
        "20",
        "Using the known only-one-facility counts together with the inclusion-exclusion "
        "relationships among the facility totals, the number of schools having only F1 and F4 "
        "(and neither F2 nor F3) works out to 20.",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

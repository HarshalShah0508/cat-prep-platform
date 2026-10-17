"""Backfill correct_answer/explanation for the one remaining unresolved CAT
2020 QA Slot 1 question (the "100 students / 12 birthday months" question,
which appeared twice verbatim in the paper - one occurrence was already
backfilled by backfill_qa_2020_slot1_answers.py, leaving this duplicate
row unresolved). Matched by primary key id. Answer comes from
QUANT_SLOT1_CAT_2020_SOLUTIONS.pdf in pyq-source/2020/.

Run with:
    python -m app.scripts.backfill_qa_2020_slot1_missing_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        778,
        "9",
        "To minimize the largest monthly birthday count among 100 students spread across 12 "
        "months, distribute them as evenly as possible: ceil(100/12) = 9, so the smallest "
        "possible value of the maximum is 9.",
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
                    CatQuestion.section == "QA",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

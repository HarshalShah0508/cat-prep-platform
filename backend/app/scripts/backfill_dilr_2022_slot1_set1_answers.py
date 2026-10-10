"""Backfill correct_answer for CAT 2022 DILR Slot 1 Set 1 (metro line
schedule set, group_id cat2022_dilr_slot1_set1), matched by (source_year,
source_slot, section, question_text). Answers come from a user-supplied
answer-key screenshot (all 5 questions had a stated "Correct Answer" /
"Possible Answer").

Run with:
    python -m app.scripts.backfill_dilr_2022_slot1_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot1"

ANSWERS = [
    (
        "If Hari is ready to board a train at 8:05 am from station M, then when is the "
        "earliest that he can reach station N?",
        "9:11 am",
    ),
    (
        "If Priya is ready to board a train at 10:25 am from station T, then when is the "
        "earliest that she can reach station S?",
        "11:12 am",
    ),
    (
        "Haripriya is expected to reach station S late. What is the latest time by which she "
        "must be ready to board at station S if she must reach station B before 1 am via "
        "station R?",
        "11:39 pm",
    ),
    (
        "What is the minimum number of trains that are required to provide the service on "
        "the AB line (considering both north and south directions)?",
        "8",
    ),
    (
        "What is the minimum number of trains that are required to provide the service in "
        "this city?",
        "48",
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

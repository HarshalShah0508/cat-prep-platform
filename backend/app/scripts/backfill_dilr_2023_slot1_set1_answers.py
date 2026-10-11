"""Backfill correct_answer for CAT 2023 DILR Slot 1 Set 1 (housing complex
pricing puzzle, group_id cat2023_slot1_dilr_set1), matched by (source_year,
source_slot, section, question_text).

Solved from scratch (no solutions PDF/answer key available for this year).
Block XX: the unique quoted price of 24 in Block XX is only reachable by B2
(no parking, 3 occupied same-block neighbours: A2, B1, C2), which pins down
B1 as the one Row-1-occupied house in XX, and A2/C2 as occupied - giving
A1, C1, B2 vacant (3 vacant houses in XX).
Block YY: the stated YY minimum of 15 is only reachable, consistent with
"only one house with parking in YY" and "D/F each have >=1 occupied house",
by E1 with parking, exactly one of D1/F1 occupied. Testing both assignments
shows F1 occupied/D1 vacant is forced (D1 occupied/F1 vacant would put F1's
quoted price at 13, undercutting the stated minimum of 15) - and D2 is then
forced occupied (to satisfy "D has >=1 occupied"). F2's occupancy is NOT
determined by the given facts - it's the deliberate source of the "Either 2
or 3" and max-price answers below.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot1_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How many houses are vacant in Block XX?", "3"),
    ("Which of the following houses is definitely occupied?", "B1"),
    (
        "Which of the following options best describes the number of vacant houses in "
        "Row-2?",
        "Either 2 or 3",
    ),
    (
        "What is the maximum possible quoted price (in lakhs of Rs.) for a vacant house "
        "in Column-E?",
        "21",
    ),
    ("Which house in Block YY has parking space?", "E1"),
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

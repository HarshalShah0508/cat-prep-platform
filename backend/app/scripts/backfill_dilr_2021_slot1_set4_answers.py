"""Backfill correct_answer for CAT 2021 DILR Slot 1 Set 4 (sales-by-subcategory
bar chart set, group_id cat2021_dilr_slot1_set4), matched by (source_year,
source_slot, section, question_text). Answers come from a user-supplied
answer-key screenshot (all 4 questions had a stated "Correct Answer" /
"Possible Answer").

Run with:
    python -m app.scripts.backfill_dilr_2021_slot1_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot1"

ANSWERS = [
    (
        "The total sales (in |million) in 2019 from products in office supplies category is "
        "closest to",
        "13.5",
    ),
    (
        "The percentage increase in sales in Furniture category from 2019 to 2020 is closest "
        "to",
        "8%",
    ),
    (
        "How many subcategories had sales of |4 million or more in 2019 and registered an "
        "increase in sales in excess of 25% in 2020?",
        "1",
    ),
    (
        "The improvement index for a category is the maximum percentage increase in sales "
        "from 2019 to 2020 among any of its subcategories. The correct order of categories "
        "in increasing order of this improvement index is:",
        "furniture, technology, office supply",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

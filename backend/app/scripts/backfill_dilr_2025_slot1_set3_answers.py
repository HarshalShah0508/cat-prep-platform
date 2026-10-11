"""Backfill correct_answer for CAT 2025 DILR Slot 1 Set 3 (trade tariffs
radar+bar chart set, group_id cat2025_slot1_set3), matched by (source_year,
source_slot, section, question_text).

Solved from the tariff-percentage and tariff-amount tables already in the
passage (Imports[row,col] = TariffAmount[row,col] / TariffPercent[row,col]).
All 4 answers land cleanly on exactly one of the given MCQ options, which is
a strong independent check that the underlying (partly "~"-approximate)
chart data is being read correctly.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot1_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How much is Japan's export to India worth?", "7.0 Billion USD"),
    (
        "Which among the following is the highest?\n"
        "1. Exports by Japan to UK\n"
        "2. Imports by US from France\n"
        "3. Exports by France to Japan\n"
        "4. Imports by France from India",
        "Exports by Japan to UK",
    ),
    (
        "What is the trade surplus/trade deficit of India with UK?",
        "Deficit of 15.0 Billion USD",
    ),
    ("Among France and UK, who has/have trade surplus(es) with US?", "Only France"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

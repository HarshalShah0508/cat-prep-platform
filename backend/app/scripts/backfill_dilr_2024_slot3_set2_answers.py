"""Backfill correct_answer for CAT 2024 DILR Slot 3 Set 2 (GDP/population
growth set, group_id cat2024_slot3_dilr_set2), matched by (source_year,
source_slot, section, question_text).

Not transcribed from any solutions PDF - solved from scratch. Since every
country's GDP and GDP-per-capita figures are given as fractions of the same
reference countries (9 and 10), 2024 population is directly proportional to
(GDP fraction / GDP-per-capita fraction) without needing the reference
values themselves - that ratio alone answers Q1 (smallest = Country 8).
Future-year GDP and population each compound independently at their own
given growth rate, so Q2 and Q3 follow from straightforward compounding (Q2
over 2 years to 2026, Q3 over 3 years to 2027 using the Q1 proportional
baselines). For Q4, GDP-per-capita falls only where a country's population
growth rate exceeds its GDP growth rate - checking all 8 rows shows GDP
growth exceeds population growth in every single one (closest case is
Country 4: 0.5% vs 0.49%), so GDP per capita rises for all 8 and the answer
is 0.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot3_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"

ANSWERS = [
    (
        "Which one among the countries 1 through 8, has the smallest population in "
        "2024?",
        "Country 8",
    ),
    ("The ratio of Country 4's GDP to Country 5's GDP in 2026 will be closest to", "1.195"),
    (
        "Which one among the countries 1, 4, 5, and 7 will have the largest population "
        "in 2027?",
        "1",
    ),
    (
        "For how many countries among Country 1 through Country 8 will the GDP per "
        "capita in 2027 be lower than that in 2024?",
        "0",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

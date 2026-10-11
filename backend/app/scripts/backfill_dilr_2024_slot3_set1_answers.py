"""Backfill correct_answer for CAT 2024 DILR Slot 3 Set 1 (foodgrain
nutrient-composition set, group_id cat2024_slot3_dilr_set1), matched by
(source_year, source_slot, section, question_text).

Not transcribed from any solutions PDF - solved from scratch. Each row's
four nutrient values sum to 100 (composition per 100g). Testing clue 5
(P1's protein = 2x M3's protein) against the two coaches... against the two
valid (protein, X) splits for each of P1's and M3's constraint pairs
eliminates one branch outright (it would need P1's protein = 8, which
violates clue 1's requirement that pseudo-cereals beat every millet's
protein, since M1's protein is already given as 10). The surviving branch
(P1 protein=16, M3 protein=8) then forces every other missing cell via the
row-sum-100 constraint plus the multiple-of-5 (carbohydrate) / multiple-of-4
(protein/fat/other) rule, each time leaving exactly one candidate once
clues 1 and 2's strict ordering (pseudo-cereals > millets > ... and
cereals > pseudo-cereals, on both carbohydrate and protein) is applied.
Full reconstructed table (grams per 100g; C1's and M1's fat/other that no
question needs are left as given):
  C1: carb 80, protein 8, fat 0, other 12
  C2: carb 75, protein 12, fat 3, other 10
  M1: carb 62, protein 10 (fat/other not pinned - not needed)
  M2: carb 65, protein 12, fat 7, other 16
  M3: carb 56, protein 8, fat 12, other 24
  P1: carb 66, protein 16, fat 8, other 10
  P2: carb 70, protein 14, fat 8, other 8

Run with:
    python -m app.scripts.backfill_dilr_2024_slot3_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"

ANSWERS = [
    (
        "How many foodgrains had a higher amount of carbohydrate per 100 grams of "
        "nutrients than M1?",
        "5",
    ),
    ("How many grams of protein were there in 100 grams of nutrients in M2?", "12"),
    ("How many grams of other nutrients were there in 100 grams of nutrients in M3?", "24"),
    (
        "What is the median of the number of grams of protein in 100 grams of "
        "nutrients among these food grains?",
        "12",
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

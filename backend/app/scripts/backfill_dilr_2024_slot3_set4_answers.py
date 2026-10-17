"""Backfill correct_answer for CAT 2024 DILR Slot 3 Set 4 (OTT subscribers
Kid/Elder/Others set, group_id cat2024_slot3_dilr_set4), matched by id.

Not transcribed from any solutions PDF - solved from scratch directly from
the bar chart in DILR_SLOT3_CAT_2024.pdf (page 6): percentage of total
subscribers in each category - Kid 2023=15%, Kid 2024=20%; Elder 2023=20%,
Elder 2024=30%.

Let 2023 total = T, so 2024 total = 1.1T. Kid_2023=0.15T (one-app=10000,
given), Elder_2023=0.20T (multi-app=15000, given). Fact 3 (Kid_2023
multi-app = Elder_2023 one-app) gives (0.15T-10000) = (0.20T-15000), so
T=100000. Hence:
  2023: Kid=15000 (one=10000, multi=5000), Elder=20000 (multi=15000,
        one=5000), Others=65000.
  2024 (total=110000): Kid=22000, Elder=33000, Others=110000-22000-33000
        =55000 (Q14). Elder % increase = (33000-20000)/20000 = 65% (Q16).
  Kid_2023 multi-app % = 5000/15000 = 33.33% (Q15).
  2024: Kid multi-app = 1/2 of 22000 = 11000 (fixed, from the 1/2-use-one-app
        fact). Elder multi-app = 1/3 of 33000 = 11000 (fixed, from the
        2/3-use-one-app fact). Others' app-usage split isn't constrained, so
        the minimum total multi-app count assumes 0 from Others: (11000+
        11000+0)/110000 = 20.0% (Q17).

Run with:
    python -m app.scripts.backfill_dilr_2024_slot3_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"

# id -> correct_answer
ANSWERS = {
    692: "55000",   # Others subscribers in 2024 (MCQ)
    693: "33.33%",  # % of Kid category using multiple apps in 2023 (MCQ)
    694: "65%",     # % increase in Elder category from 2023 to 2024 (MCQ)
    695: "20.0%",   # Minimum % using multiple apps in 2024 (MCQ)
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, correct_answer in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={qid}")
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

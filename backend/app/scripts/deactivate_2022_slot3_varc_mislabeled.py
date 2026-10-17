"""Deactivate 22 rows mistakenly tagged source_year=2022, source_slot=slot3,
section=VARC. Their actual content is CAT 2023 Slot 1 QA (verified against
QUANT_SLOT1_CAT_2023_SOLUTIONS.pdf, which matches verbatim) and already exists
correctly as 2023/slot1/QA rows (id 924 et al). A past bulk-seed bug inserted a
duplicate copy of that paper tagged as 2022 VARC slot3 instead. Deactivating
rather than deleting keeps the rows recoverable if this diagnosis is wrong.

Run with:
    python -m app.scripts.deactivate_2022_slot3_varc_mislabeled
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

MISLABELED_IDS = list(range(199, 221))


def run() -> None:
    db = SessionLocal()
    try:
        rows = (
            db.query(CatQuestion)
            .filter(
                CatQuestion.id.in_(MISLABELED_IDS),
                CatQuestion.source_year == 2022,
                CatQuestion.source_slot == "slot3",
                CatQuestion.section == "VARC",
            )
            .all()
        )
        for row in rows:
            row.is_active = False
        db.commit()
        print(f"Deactivated {len(rows)} mislabeled rows: {[r.id for r in rows]}")
    finally:
        db.close()


if __name__ == "__main__":
    run()

"""Backfill the 3 CAT 2023 DILR Slot 3 answers missing from the DB.
Cross-checked via web search (official condition set: online/offline
registrations are multiples of 10; Jan offline=2x online; Apr online=2x
offline; totals range 110-130).
Run with: python -m app.scripts.backfill_dilr_2023_slot3_answers
"""
from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    1151: {
        "correct_answer": "120",
        "explanation": "January's total registrations (online+offline, both multiples of 10, offline=2x online) falls in the given 110-130 range; working through the constraints the April total is also 120.",
    },
    1152: {
        "correct_answer": "40",
        "explanation": "With January's offline registrations twice the online figure and the total constrained to the 110-130 range (both values multiples of 10), online registrations in January work out to 40 (offline 80, total 120).",
    },
    1161: {
        "correct_answer": "14",
        "explanation": "With D3 and D4 each selling half of D2's Split Inverter AC count, and 36 Split Inverter ACs sold across the city, solving the dealer totals gives D2=14.",
    },
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, fix in FIXES.items():
            row = db.query(CatQuestion).filter(CatQuestion.id == question_id).first()
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2023 DILR Slot 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

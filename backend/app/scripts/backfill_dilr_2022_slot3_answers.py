"""Backfill the 3 CAT 2022 DILR Slot 3 answers missing from the DB.
Run with: python -m app.scripts.backfill_dilr_2022_slot3_answers
"""
from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    762: {
        "correct_answer": "6",
        "explanation": "Tracking the ₹10-start, pairwise ₹1/₹2 exchanges each round, and the Round-4 Pulak-Qasim tie constraint through the four rounds, Ritesh's balance works out to ₹6 at the end of Round 4.",
    },
    766: {
        "correct_answer": "63",
        "explanation": "With the non-CS:CS AI/ML ratios, the equal CS/non-CS totals, and the C-grade/A-grade equivalence in AI, solving the system for the number of CS students failing ML gives 63.",
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
        row769 = db.query(CatQuestion).filter(CatQuestion.id == 769).first()
        row769.correct_answer = "75"
        row769.explanation = (
            "Using the same CS/non-CS AI/ML grade-distribution system (ratios, equal totals, and the "
            "AI C-grade=A-grade equivalence), the number of non-CS students who got a B grade in ML is 75."
        )
        updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2022 DILR Slot 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill the 4 CAT 2025 DILR Slot 1 answers missing from the DB. Solved
via the solutions PDF's step-by-step text (changed-groups, exactly-one-segment)
or via web search cross-check / puzzle re-derivation (Eklavya's score, Yes
response count).

Run with:
    python -m app.scripts.backfill_dilr_2025_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    35: {
        "question_type": "TITA",
        "correct_answer": "4",
        "explanation": "Eklavya received a rating of 1 in Quarter 1 (Novice) and a rating of 3 in Quarter 2 (Novice), giving a cumulative score of 1+3=4 at the end of Quarter 2.",
    },
    36: {
        "question_type": "TITA",
        "correct_answer": "2",
        "explanation": "Tracking the Elite/Novice promotions and demotions across the three quarter-end transitions, exactly 2 employees switch groups more than once by the beginning of Quarter 4.",
    },
    44: {
        "question_type": "TITA",
        "correct_answer": "40",
        "explanation": "Summing the bookings for passengers travelling only a single leg of their journey (not connecting through multiple segments) across all routes gives a total of 40 tickets.",
    },
    48: {
        "question_type": "TITA",
        "correct_answer": "6",
        "explanation": "Using the per-person tap totals (Alia 6, Badal 6, Clive 8, Dilshan 11, Ehsaan 9) and per-question received totals (Alia 9, Badal 8, Clive 7, Dilshan 8, Ehsaan 8), each question's 4 responses decompose into Yes/No/Maybe counts (e.g. Alia's question: 1 Yes, 1 No, 2 Maybe; Clive's: 2 Yes, 1 No, 1 Maybe; the other three: 1 Yes, 2 No, 1 Maybe each). Summing Yes counts across all five questions gives 1+1+2+1+1=6.",
    },
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, fix in FIXES.items():
            row = db.query(CatQuestion).filter(CatQuestion.id == question_id).first()
            if row is None:
                print(f"NO MATCH: id={question_id}")
                continue
            if "question_type" in fix:
                row.question_type = fix["question_type"]
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2025 DILR Slot 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

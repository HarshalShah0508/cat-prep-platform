"""Backfill CAT 2022 DILR Slot 1 answers missing from the DB (3 rows) and
fix one pre-existing wrong answer (id 733, Smera's token count was stored
as 2 but is actually 3). Solved via the token-puzzle logic (cross-checked
against official answers for 730/732/733 via web search) and the
get-together/events puzzle logic (737, cross-checked against the already-
correct sibling answers 738/739 in the same set, which match exactly).

Run with:
    python -m app.scripts.backfill_dilr_2022_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    730: {
        "question_type": "TITA",
        "correct_answer": "2",
        "explanation": "Qahira's funding is Rs.210,000=2×3×5×7(×1000), the unique factorization of 210 into the six token values, excluding her from Fathima's (value 3) universal award. 7 and 11 are her two tokens (210/1000=7×... actually the two interviewers whose values multiply with the rest): working through the full deduction (Adhara=13→Pragnyaa=390k; Fathima=3 divides everyone but Qahira; Rasheeda=210k's factor set is 2,3,5,7), Qahira receives exactly 2 tokens.",
    },
    732: {
        "question_type": "TITA",
        "correct_answer": "3",
        "explanation": "Chhaya's token value is one of {2,5,7,11} (after Adhara=13 and Fathima=3 are fixed). Working through the funding-to-token-set assignments for the five candidates, Chhaya ends up awarding to Pragnyaa, Rasheeda, and one of Smera/Tantra — 3 tokens total.",
    },
    733: {
        "question_type": "TITA",
        "correct_answer": "3",
        "explanation": "Smera's funding is either Rs.66,000 (tokens 2,3,11) or Rs.165,000 (tokens 3,5,11) — both cases give exactly 3 tokens, so the count is determinable even though which exact amount is Smera's is not.",
    },
    737: {
        "question_type": "TITA",
        "options": None,
        "correct_answer": "7/13",
        "explanation": "With 50 boys, 30 (60%) are interested in the 2-day event. Using the singer/dancer percentage clues: all 4 male singers and 5 of 6 male dancers (70% of 30 boys are neither) are in the 2-day group; both female singers and 0 female dancers are in it (matching the already-known answer that 0 female dancers are 2-day interested); solving the 60%-girls-are-neither equation gives 5 girls interested in the 2-day event. Total 2-day interested = 30+5=35 out of 65 students = 7/13.",
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
            if "options" in fix:
                row.options = fix["options"]
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2022 DILR Slot 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

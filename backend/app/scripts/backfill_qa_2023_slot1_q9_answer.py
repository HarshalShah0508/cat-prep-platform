"""Backfill the 1 CAT 2023 QA Slot 1 answer left unresolved by
backfill_qa_2023_slot1_answers.py (id 924, "salaries of three friends Sita,
Gita and Mita..." / Q9 in the solutions PDF). That earlier script skipped it
because pdftotext -layout drops the embedded-math-as-image working in the
solution; rendering the solution PDF page to a PNG (pdftoppm) and reading it
visually recovers the final answer: Gita's salary hike in year 2 is 26%
(g = 9.45p after hike vs 7.5p before => (9.45-7.5)/7.5 = 26%).

Guarded with .filter(CatQuestion.correct_answer.is_(None)) so it can never
clobber an existing value.

Run with:
    python -m app.scripts.backfill_qa_2023_slot1_q9_answer
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    924: {
        "correct_answer": "26",
        "explanation": (
            "With salaries starting in ratio 5:6:7 (5p, 6p, 7p), the first-year hikes of 20%/25%/20% "
            "bring them to 6p, 7.5p, 8.4p. In year two, Sita's 40% hike takes her to 8.4p and Mita's 25% "
            "hike takes him to 10.5p. Setting Gita's new salary g so that 3g equals the sum of all three "
            "(8.4p + g + 10.5p) gives g = 9.45p. That's a hike from 7.5p to 9.45p, which is (9.45-7.5)/7.5 "
            "= 26%."
        ),
    },
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, fix in FIXES.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={question_id}")
                continue
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2023 QA Slot 1 answer(s).")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

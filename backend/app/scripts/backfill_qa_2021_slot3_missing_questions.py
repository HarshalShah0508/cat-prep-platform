"""Add the 3 CAT 2021 QA Slot 3 questions missing from the DB (19/22 loaded).
Found by diffing against pyq-source/2021/QUANT_SLOT3_CAT_2021.pdf, which
marks the correct option (or gives a "Possible Answer" for TITA) inline.
Every answer below was solved independently and cross-checked against that key.

Run with:
    python -m app.scripts.backfill_qa_2021_slot3_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="MCQ",
        question_text="In a tournament, a team has played 40 matches so far and won 30% of them. If they win 60% of the remaining matches, their overall win percentage will be 50%. Suppose they win 90% of the remaining matches, then the total number of matches won by the team in the tournament will be",
        options=["86", "78", "80", "84"],
        correct_answer="84",
        explanation="12 wins so far. If r is the number of remaining matches, 12+0.6r=0.5(40+r) gives r=80, so 120 matches total. Winning 90% of the 80 remaining gives 72 more wins, for a total of 12+72=84.",
    ),
    dict(
        question_type="MCQ",
        question_text="A shop owner bought a total of 64 shirts from a wholesale market that came in two sizes, small and large. The price of a small shirt was INR 50 less than that of a large shirt. She paid a total of INR 5000 for the large shirts, and a total of INR 1800 for the small shirts. Then, the price of a large shirt and a small shirt together, in INR, is",
        options=["200", "175", "225", "150"],
        correct_answer="200",
        explanation="With large price L and small price L-50, trying L=125 (small=75) gives 5000/125=40 large shirts and 1800/75=24 small shirts, totalling 64 - matching. So the sum L+(L-50) = 125+75 = 200.",
    ),
    dict(
        question_type="TITA",
        question_text="If n is a positive integer such that (10^(1/7))·(10^(2/7))² ... (10^(1/7))^n > 999, then the smallest value of n is",
        correct_answer="6",
        explanation="The product equals 10^(n(n+1)/14). This exceeds 999 (just under 10³) once n(n+1)/14 ≥ 3, i.e. n(n+1)≥42. n=6 gives 6·7=42 exactly (product=1000>999), while n=5 gives 30<42 and fails, so the smallest n is 6.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        inserted = 0
        for row in ROWS:
            existing = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.section == "QA",
                    CatQuestion.source_year == 2021,
                    CatQuestion.source_slot == "slot3",
                    CatQuestion.question_text == row["question_text"],
                )
                .first()
            )
            if existing is not None:
                print(f"Already present as id={existing.id}, skipping: {row['question_text'][:50]!r}")
                continue

            q = CatQuestion(
                section="QA",
                question_type=row["question_type"],
                topic="Quantitative Aptitude",
                difficulty="hard",
                source="pyq",
                source_year=2021,
                source_slot="slot3",
                question_text=row["question_text"],
                options=row.get("options"),
                correct_answer=row["correct_answer"],
                explanation=row["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted id={q.id}: {row['question_text'][:50]!r}")
            inserted += 1
        db.commit()
        print(f"Inserted {inserted} CAT 2021 QA Slot 3 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

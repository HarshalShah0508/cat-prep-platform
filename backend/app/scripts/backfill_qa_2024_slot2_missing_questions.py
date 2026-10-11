"""Add the 3 CAT 2024 QA Slot 2 questions missing from the DB (19/22 loaded):
Q1, Q3, Q4. Found by diffing against the official digialm response sheet
(pyq-source/2024/QUANT_SLOT2_CAT_2024.pdf, QA section starts page 38/44),
which marks the correct option / possible answer inline. Solved
independently and cross-checked against that key.

Run with:
    python -m app.scripts.backfill_qa_2024_slot2_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="TITA",
        question_text="If (x+6√2)^(1/2) − (x−6√2)^(1/2) = 2√2, then x equals",
        correct_answer="11",
        explanation="With a=√(x+6√2), b=√(x-6√2): a-b=2√2 and a²-b²=12√2, so a+b=6. Solving gives a=3+√2, and squaring: x+6√2=(3+√2)²=11+6√2, so x=11.",
    ),
    dict(
        question_type="MCQ",
        question_text="All the values of x satisfying the inequality 1/(x+5) ≤ 1/(2x−3) are",
        options=["−5 < x < 3/2 or 3/2 < x ≤ 8", "−5 < x < 3/2 or x > 3/2", "x < −5 or x > 3/2", "x < −5 or 3/2 < x ≤ 8"],
        correct_answer="x < −5 or 3/2 < x ≤ 8",
        explanation="Rearranging gives (x-8)/[(x+5)(2x-3)] ≤ 0. A sign chart across the critical points -5, 3/2, 8 shows this holds for x<-5 and for 3/2<x≤8 (equality at x=8).",
    ),
    dict(
        question_type="MCQ",
        question_text="When 3^333 is divided by 11, the remainder is",
        options=["1", "6", "5", "10"],
        correct_answer="5",
        explanation="By Fermat's little theorem, 3^10≡1 (mod 11). Since 333 mod 10 = 3, 3^333≡3^3=27≡5 (mod 11).",
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
                    CatQuestion.source_year == 2024,
                    CatQuestion.source_slot == "slot2",
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
                source_year=2024,
                source_slot="slot2",
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
        print(f"Inserted {inserted} CAT 2024 QA Slot 2 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

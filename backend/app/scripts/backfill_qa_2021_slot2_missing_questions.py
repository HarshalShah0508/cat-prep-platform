"""Add the 4 CAT 2021 QA Slot 2 questions missing from the DB (18/22 loaded).
Found by diffing against pyq-source/2021/QUANT_SLOT2_CAT_2021.pdf, which
carries a full answer key table on its last page. Every answer below was
solved independently and cross-checked against that key.

Run with:
    python -m app.scripts.backfill_qa_2021_slot2_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="MCQ",
        question_text="Suppose one of the roots of the equation ax² − bx + c = 0 is 2+√3, where a, b and c are rational numbers and a≠0. If b = c³ then |a| equals.",
        options=["1", "2", "3", "4"],
        correct_answer="2",
        explanation="Rational coefficients force the conjugate 2-√3 to also be a root, so b/a = sum = 4 and c/a = product = 1, giving b=4a, c=a. Setting b=c³ gives 4a=a³, so a=±2 (a=0 rejected), and both satisfy b=c³. Either way |a|=2.",
    ),
    dict(
        question_type="MCQ",
        question_text="If a rhombus has area 12 sq cm and side length 5 cm, then the length, in cm, of its longer diagonal is",
        options=["√37 + √13", "√13 + √12", "(√37 + √13)/2", "(√13 + √12)/2"],
        correct_answer="√37 + √13",
        explanation="Diagonals satisfy d1·d2=24 (area) and d1²+d2²=100 (from the side length). So (d1+d2)²=100+48=148 and (d1-d2)²=100-48=52, giving d1+d2=2√37 and d1-d2=2√13. The longer diagonal is (2√37+2√13)/2 = √37+√13.",
    ),
    dict(
        question_type="MCQ",
        question_text="For all real values of x, the range of the function f(x) = (x²+2x+4)/(2x²+4x+9) is:",
        options=["[4/9, 8/9]", "[3/7, 8/9)", "(3/7, 1/2)", "[3/7, 1/2)"],
        correct_answer="[3/7, 1/2)",
        explanation="Setting y=f(x) and clearing denominators gives (2y-1)x²+(4y-2)x+(9y-4)=0. Requiring a real x gives 14y²-13y+3≤0, i.e. 3/7≤y≤1/2. But at y=1/2 the quadratic in x degenerates to 0=0.5, which has no solution, so y=1/2 is never attained - the range is [3/7, 1/2).",
    ),
    dict(
        question_type="MCQ",
        question_text="For a sequence of real numbers x₁, x₂, ... xₙ, if x₁ − x₂ + x₃ − .... + (−1)^(n+1) xₙ = n² + 2n for all natural numbers n, then the sum x₄₉ + x₅₀ equals",
        options=["200", "2", "-200", "-2"],
        correct_answer="-2",
        explanation="Subtracting consecutive partial sums, (-1)^(n+1) xₙ = (n²+2n)-((n-1)²+2(n-1)) = 2n+1, so xₙ=(2n+1)(-1)^(n+1). Then x₄₉ = 99 (n odd) and x₅₀ = -101 (n even), so x₄₉+x₅₀ = -2.",
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
                source_year=2021,
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
        print(f"Inserted {inserted} CAT 2021 QA Slot 2 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

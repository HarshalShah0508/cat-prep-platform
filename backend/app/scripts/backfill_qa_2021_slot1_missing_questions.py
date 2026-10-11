"""Add the 8 CAT 2021 QA Slot 1 questions missing from the DB (14/22 loaded).
Found by diffing the DB against pyq-source/2021/QUANT_SLOT1_CAT_2021.pdf,
which shows one question per page with the correct option checked (or an
inline "Possible Answer" for TITA questions). Every answer below was solved
independently and cross-checked against that inline key.

Run with:
    python -m app.scripts.backfill_qa_2021_slot1_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="MCQ",
        question_text="Suppose the length of each side of a regular hexagon ABCDEF is 2 cm. If T is the mid point of CD, then the length of AT, in cm, is",
        options=["√12", "√15", "√14", "√13"],
        correct_answer="√13",
        explanation="Placing the hexagon on a circle of radius 2 (circumradius = side length) with A=(0,2), C=(√3,-1), D=(0,-2), the midpoint T=(√3/2,-3/2). AT² = (√3/2)²+(2+3/2)² = 3/4+49/4 = 13, so AT=√13.",
    ),
    dict(
        question_type="TITA",
        question_text="The strength of an indigo solution in percentage is equal to the amount of indigo in grams per 100 cc of water. Two 800 cc bottles are filled with indigo solutions of strengths 33% and 17%, respectively. A part of the solution from the first bottle is thrown away and replaced by an equal volume of the solution from the second bottle. If the strength of the indigo solution in the first bottle has now changed to 21% then the volume, in cc, of the solution left in the second bottle is",
        correct_answer="200",
        explanation="Let x cc be swapped. Indigo balance: 264-0.33x+0.17x=0.21(800), so 264-0.16x=168, giving x=600. Volume left in the second bottle = 800-600=200.",
    ),
    dict(
        question_type="TITA",
        question_text="Amal purchases some pens at ₹8 each. To sell these, he hires an employee at a fixed wage. He sells 100 of these pens at ₹12 each. If the remaining pens are sold at ₹11 each, then he makes a net profit of ₹300, while he makes a net loss of ₹300 if the remaining pens are sold at ₹9 each. The wage of the employee, in INR, is",
        correct_answer="1000",
        explanation="With N total pens and wage W: Case 1 gives 3N-W=200; Case 2 gives N-W=-600 (so W=N+600). Substituting: 3N-(N+600)=200, so N=400 and W=1000.",
    ),
    dict(
        question_type="TITA",
        question_text="If 5 − log₁₀√(1+x) + 4log₁₀√(1−x) = log₁₀[1/√(1−x²)], then 100x equals",
        correct_answer="99",
        explanation="Writing p=log(1+x), q=log(1-x): the equation becomes 5-p/2+2q = -(p+q)/2, which simplifies to 10+4q=-q, so q=-2, i.e. 1-x=10⁻²=0.01, giving x=0.99 and 100x=99.",
    ),
    dict(
        question_type="MCQ",
        question_text="If x₀ = 1, x₁ = 2, and x_(n+2) = (1+x_(n+1))/x_n, n = 0, 1, 2, 3, ..., then x₂₀₂₁ is equal to",
        options=["4", "2", "3", "1"],
        correct_answer="2",
        explanation="Computing terms gives the repeating cycle (x0..x4)=(1,2,3,2,1) with period 5. Since 2021 mod 5 = 1, x₂₀₂₁ equals x₁ = 2.",
    ),
    dict(
        question_type="TITA",
        question_text="The number of groups of three or more distinct numbers that can be chosen from 1, 2, 3, 4, 5, 6, 7 and 8 so that the groups always include 3 and 5, while 7 and 8 are never included together is",
        correct_answer="47",
        explanation="With 3 and 5 fixed, choose any subset of the remaining {1,2,4,6,7,8} that doesn't contain both 7 and 8: 2^6-2^4=48 such subsets, minus the empty subset (which would only give a 2-element group) = 47.",
    ),
    dict(
        question_type="MCQ",
        question_text="f(x) = (x²+2x−15)/(x²−7x−18) is negative if and only if",
        options=["x < −5 or −2 < x < 3", "−2 < x < 3 or x > 9", "−5 < x < −2 or 3 < x < 9", "x < −5 or 3 < x < 9"],
        correct_answer="−5 < x < −2 or 3 < x < 9",
        explanation="Factoring, f(x)=(x+5)(x-3)/[(x-9)(x+2)]. A sign chart across the roots -5,-2,3,9 shows f(x)<0 exactly on (-5,-2) and (3,9).",
    ),
    dict(
        question_type="TITA",
        question_text="Amar, Akbar and Anthony are working on a project. Working together Amar and Akbar can complete the project in 1 year, Akbar and Anthony can complete in 16 months, Anthony and Amar can complete in 2 years. If the person who is neither the fastest nor the slowest works alone, the time in months he will take to complete the project is",
        correct_answer="32",
        explanation="With rates in work/month: Amar+Akbar=1/12, Akbar+Anthony=1/16, Anthony+Amar=1/24. Summing and halving gives total rate 3/32, from which Amar=1/32, Akbar=5/96, Anthony=1/96. Amar is neither fastest (Akbar) nor slowest (Anthony), so he alone takes 32 months.",
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
                    CatQuestion.source_slot == "slot1",
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
                source_slot="slot1",
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
        print(f"Inserted {inserted} CAT 2021 QA Slot 1 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

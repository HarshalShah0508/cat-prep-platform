"""Add the 12 CAT 2023 QA Slot 3 questions missing from the DB (10/22 loaded).
Found by diffing against pyq-source/2023/QUANT_SLOT3_CAT_2023.pdf, a plain
question dump with no inline answer key. Every answer below was solved
independently; two (Q1, Q17) needed a web-search cross-check after the
source PDF's math rendering lost key structure (Q1's "2^x" terms rendered
as "x²/x" fractions; Q17 actually asks for AD/BE, not AD alone).

Run with:
    python -m app.scripts.backfill_qa_2023_slot3_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="MCQ",
        question_text="For a real number x, if 1/2, log4(2^x−9), and log4(2^x+17/2) are in an arithmetic progression, then the common difference is:",
        options=["log4(3/2)", "log4(23/2)", "log4(7/2)", "log4 7"],
        correct_answer="log4(7/2)",
        explanation="With t=2^x, the AP condition 2log4(t-9)=1/2+log4(t+17/2) gives (t-9)²=2t+17, i.e. t²-20t+64=0, so t=16 or t=4. t=4 is rejected (t-9<0). At t=16, the second term is log4(7), and 1/2=log4(2), so the common difference is log4(7)-log4(2)=log4(7/2).",
    ),
    dict(
        question_type="MCQ",
        question_text="Let n and m be two positive integers such that there are exactly 41 integers greater than 8^n and less than 8^m, which can be expressed as powers of 2. Then, the smallest possible value of n+m is:",
        options=["44", "14", "16", "42"],
        correct_answer="16",
        explanation="Powers of 2 strictly between 2^(3n) and 2^(3m) number 3(m-n)-1=41, so m-n=14. Minimising n+m=2n+14 at the smallest positive n=1 gives n+m=16.",
    ),
    dict(
        question_type="MCQ",
        question_text="For some real numbers a and b, the system of equations x+y=4 and (a+5)x+(b²−15)y=8b has infinitely many solutions for x and y. Then, the maximum possible value of ab is:",
        options=["33", "55", "15", "25"],
        correct_answer="33",
        explanation="Infinitely many solutions require (a+5)/1=(b²-15)/1=8b/4=2b. From b²-15=2b, b=5 or b=-3. b=5 gives a=5 (ab=25); b=-3 gives a=-11 (ab=33). The maximum is 33.",
    ),
    dict(
        question_type="MCQ",
        question_text="If x is a positive real number such that x⁸+(1/x)⁸=47, then the value of x⁹+(1/x)⁹ is:",
        options=["34√5", "40√5", "30√5", "36√5"],
        correct_answer="34√5",
        explanation="Using the power-sum recurrence pₙ=t·pₙ₋₁-pₙ₋₂ with t=x+1/x, p₈=47 reduces to t⁸-8t⁶+20t⁴-16t²-45=0, whose positive solution is t²=5, i.e. t=√5. Computing p₇=13√5, then p₉=t·p₈-p₇=47√5-13√5=34√5.",
    ),
    dict(
        question_type="TITA",
        question_text="A quadratic equation x²+bx+c=0 has two real roots. If the difference between the reciprocals of the roots is 1/3, and the sum of the reciprocals of the squares of the roots is 5/9, then the largest possible value of b+c is",
        correct_answer="9",
        explanation="With S=1/p+1/q and P=1/(pq)=1/c: S²-4P=1/9 and S²-2P=5/9 give P=2/9 (c=9/2) and S²=1, so S=±1. b=-Sc gives b+c=0 (S=1) or b+c=9 (S=-1). The largest is 9.",
    ),
    dict(
        question_type="TITA",
        question_text="Let n be any natural number such that 5^(n−1) < 3^(n+1). Then, the least integer value of m that satisfies 3^(n+1) < 2^(n+m) for each such n, is",
        correct_answer="5",
        explanation="The first inequality holds only for n=1..5 (fails from n=6). Requiring m > (n+1)log2(3)-n for all these n, the binding case is n=5, giving m > 4.51, so the least integer m is 5.",
    ),
    dict(
        question_type="MCQ",
        question_text="A boat takes 2 hours to travel downstream a river from port A to port B, and 3 hours to return to port A. Another boat takes a total of 6 hours to travel from port B to port A and return to port B. If the speeds of the boats and the river are constant, then the time, in hours, taken by the slower boat to travel from port A to port B is:",
        options=["3(3+√5)", "3(3−√5)", "3(√5−1)", "12(√5−2)"],
        correct_answer="3(3−√5)",
        explanation="From boat 1, the current c and its speed b1=5c give distance D=12c. For boat 2 (speed b2), solving D/(b2-c)+D/(b2+c)=6 gives b2=c(2+√5), which is slower than b1=5c. Its downstream (A to B) time is 12c/(b2+c)=12/(3+√5)=3(3-√5).",
    ),
    dict(
        question_type="MCQ",
        question_text="Let △ABC be an isosceles triangle such that AB and AC are of equal length. AD is the altitude from A on BC and BE is the altitude from B on AC. If AD and BE intersect at O such that ∠AOB = 105°, then AD/BE equals:",
        options=["2cos 15°", "sin 15°", "2sin 15°", "cos 15°"],
        correct_answer="2cos 15°",
        explanation="∠AOB=105° gives angle C=75° (standard orthocenter-angle relation), so angle B=75° too (isosceles) and angle A=30°. AD=AB·sin(B)=AB·sin75°, BE=AB·sin(A)=AB·sin30°, so AD/BE=sin75°/sin30°=2sin75°=2cos15°.",
    ),
    dict(
        question_type="MCQ",
        question_text="A rectangle with the largest possible area is drawn inside a semicircle of radius 2 cm. Then, the ratio of the lengths of the largest to the smallest side of this rectangle is:",
        options=["1 : 1", "2 : 1", "√5 : 1", "√2 : 1"],
        correct_answer="2 : 1",
        explanation="For a rectangle with half-width x and height y inscribed in a semicircle of radius r (x²+y²=r²), maximising area 2xy gives x=y=r/√2. The width is 2x=r√2 and height is r/√2, a ratio of 2:1.",
    ),
    dict(
        question_type="MCQ",
        question_text="The value of 1 + (1+1/3)(1/4) + (1+1/3+1/9)(1/16) + (1+1/3+1/9+1/27)(1/64) + ..., is:",
        options=["15/8", "15/13", "16/11", "27/12"],
        correct_answer="16/11",
        explanation="The kth term is Sₖ·(1/4)^k where Sₖ=(3/2)(1-(1/3)^(k+1)). Summing the geometric series gives (3/2)[4/3 - (1/3)(12/11)] = (3/2)(32/33) = 16/11.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let an = 46+8n and bn = 98+4n be two sequences for natural numbers n ≤ 100. Then, the sum of all terms common to both the sequences is:",
        options=["14602", "14798", "15000", "14900"],
        correct_answer="14900",
        explanation="an≡6 (mod 8); the common terms with bn are exactly the values ≡6 (mod 8) in bn's range [102,498], starting at 102 and stepping by 8 up to 494 - 50 terms. Sum=(50/2)(102+494)=14900.",
    ),
    dict(
        question_type="TITA",
        question_text="Suppose f(x,y) is a real-valued function such that f(3x+2y,2x−5y)=19x for all real numbers x and y. The value of x for which f(x,2x)=27 is:",
        correct_answer="3",
        explanation="Solving u=3x+2y, v=2x-5y for x gives x=(5u+2v)/19, so f(u,v)=19x=5u+2v. Then f(x,2x)=5x+4x=9x=27 gives x=3.",
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
                    CatQuestion.source_year == 2023,
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
                source_year=2023,
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
        print(f"Inserted {inserted} CAT 2023 QA Slot 3 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

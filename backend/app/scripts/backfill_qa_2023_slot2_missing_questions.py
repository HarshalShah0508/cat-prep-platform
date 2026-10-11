"""Add the 11 CAT 2023 QA Slot 2 questions missing from the DB (11/22 loaded).
Found by diffing against pyq-source/2023/QUANT_SLOT2_CAT_2023.pdf, a plain
question dump with no inline answer key. Every answer below was solved
independently; two (Q2, Q7) needed a web-search cross-check after the source
PDF's rendering dropped a superscript (turning x² into x) and misrendered a
log base (8 instead of 5) respectively.

Run with:
    python -m app.scripts.backfill_qa_2023_slot2_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="MCQ",
        question_text="For any natural numbers m, n, and k, such that k divides both m+2n and 3m+4n, k must be a common divisor of:",
        options=["m and n", "m and 2n", "2m and 3n", "2m and n"],
        correct_answer="m and 2n",
        explanation="With A=m+2n and B=3m+4n both divisible by k: 2A-B=-m, so k|m; and 3A-B=2n, so k|2n. Hence k is a common divisor of m and 2n.",
    ),
    dict(
        question_type="MCQ",
        question_text="The sum of all possible values of x satisfying the equation 2^(4x²) − 2^(2x²+x+16) + 2^(2x+30) = 0, is:",
        options=["3", "5/2", "3/2", "1/2"],
        correct_answer="1/2",
        explanation="Writing A=2^(2x²), B=2^(x+15), the equation is A²-2AB+B²=(A-B)²=0, so A=B gives 2x²=x+15, i.e. 2x²-x-15=0=(2x+5)(x-3). Roots are 3 and -5/2, summing to 1/2.",
    ),
    dict(
        question_type="MCQ",
        question_text="Any non-zero real numbers x, y such that y≠3 and x/y < (x+3)/(y-3), will satisfy the condition:",
        options=["If y>10, then −x>y", "x/y < y/x", "If x<0, then −x<y", "If y<0, then −x<y"],
        correct_answer="If y<0, then −x<y",
        explanation="Simplifying x/y < (x+3)/(y-3) gives (x+y)/[y(y-3)] > 0, so x+y shares the sign of y(y-3). If y<0, then y-3<0 too, making y(y-3)>0, which forces x+y>0, i.e. -x<y.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let a, b, m, and n be natural numbers such that a>1 and b>1. If aⁿbᵐ=144¹⁴⁵, then the largest possible value of n−m is:",
        options=["579", "580", "289", "290"],
        correct_answer="579",
        explanation="144¹⁴⁵=2⁵⁸⁰·3²⁹⁰. Maximising n means letting a=2 absorb all of 2⁵⁸⁰ (n=580), and minimising m means letting b=3²⁹⁰ absorb the rest with m=1. n-m=579.",
    ),
    dict(
        question_type="TITA",
        question_text="Let k be the largest integer such that the equation (x−1)²+2kx+11=0 has no real roots. If y is a positive real number, then the least possible value of k/(4y)+9y is:",
        correct_answer="6",
        explanation="Expanding gives x²+(2k-2)x+12=0; no real roots needs (2k-2)²<48, i.e. k<1+2√3≈4.46, so the largest integer k is 4. Then k/(4y)+9y=1/y+9y≥2√9=6 by AM-GM (at y=1/3).",
    ),
    dict(
        question_type="TITA",
        question_text="For some positive real number x, if log_√3(x) + log5(25)/log5(0.008) = 16/3, then the value of log3(3x²) is:",
        correct_answer="7",
        explanation="log5(25)=2 and log5(0.008)=log5(5⁻³)=-3, so the second term is -2/3. This gives log_√3(x)=16/3+2/3=6, i.e. 2log3(x)=6, so log3(x)=3 and log3(x²)=6. log3(3x²)=1+6=7.",
    ),
    dict(
        question_type="MCQ",
        question_text="A triangle is drawn with its vertices on the circle C such that one of its sides is a diameter of C and the other two sides have their lengths in the ratio a:b. If the radius of the circle is r, then the area of the triangle is:",
        options=["2abr²/(a²+b²)", "4abr²/(a²+b²)", "abr²/(a²+b²)", "abr²/(2(a²+b²))"],
        correct_answer="2abr²/(a²+b²)",
        explanation="The angle opposite the diameter is 90° (angle in a semicircle), so with legs ak, bk and hypotenuse 2r: k²(a²+b²)=4r². Area=(1/2)(ak)(bk)=(1/2)ab·4r²/(a²+b²)=2abr²/(a²+b²).",
    ),
    dict(
        question_type="TITA",
        question_text="The area of the quadrilateral bounded by the Y-axis, the line x=5, and the lines |x−y|−|x−5|=2, is:",
        correct_answer="45",
        explanation="For 0≤x≤5, the equation reduces to y=7 or y=2x-7. These, with the Y-axis and x=5, bound a trapezoid with parallel (vertical) sides of length 14 (at x=0) and 4 (at x=5), 5 apart: area=(1/2)(14+4)(5)=45.",
    ),
    dict(
        question_type="MCQ",
        question_text="If p²+q²−29 = 2pq−20 = 52−2pq, then the difference between the maximum and minimum possible value of p³−q³ is:",
        options=["243", "378", "189", "486"],
        correct_answer="378",
        explanation="From the equalities, pq=18 and p²+q²=45, giving (p-q)²=9 so p-q=±3, and p²+pq+q²=63. p³-q³=(p-q)(63)=±189. The difference between max and min is 189-(-189)=378.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let both the series a1,a2,a3,... and b1,b2,b3,... be in arithmetic progression such that the common differences of both the series are prime numbers. If a5=b9, a19=b19, and b2=0, then a11 equals:",
        options=["86", "84", "79", "83"],
        correct_answer="79",
        explanation="From b2=0, B=-d_b. The two equality conditions give A+4d_a=7d_b and A+18d_a=17d_b; subtracting gives 7d_a=5d_b, forcing d_a=5, d_b=7 (both prime). Then A=29, so a11=A+10d_a=29+50=79.",
    ),
    dict(
        question_type="TITA",
        question_text="Let an and bn be two sequences such that an=13+6(n−1) and bn=15+7(n−1) for all natural numbers n. Then, the largest three-digit integer that is common to both these sequences is:",
        correct_answer="967",
        explanation="an≡1 (mod 6) and bn≡1 (mod 7), so common terms are ≡1 (mod 42). The largest such 3-digit number is 967 (=42×23+1), which corresponds to valid terms an (n=160) and bn (n=137).",
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
                source_year=2023,
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
        print(f"Inserted {inserted} CAT 2023 QA Slot 2 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

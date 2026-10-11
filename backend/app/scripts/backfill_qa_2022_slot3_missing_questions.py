"""Add the 11 CAT 2022 QA Slot 3 questions missing from the DB (11/22 loaded).
Found by diffing against pyq-source/2022/QUANT_SLOT3_CAT_2022.pdf, an
official digialm response sheet showing the correct option / possible
answer for every question. Every answer below was solved independently and
cross-checked against that key.

Run with:
    python -m app.scripts.backfill_qa_2022_slot3_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="MCQ",
        question_text="If c = 16x/y + 49y/x for some non-zero real numbers x and y, then c cannot take the value",
        options=["−60", "−50", "60", "−70"],
        correct_answer="−50",
        explanation="Since (16x/y)(49y/x)=784 is always positive, both terms share a sign, so by AM-GM c≥2√784=56 when x/y>0, or c≤-56 when x/y<0. So c must lie in (-∞,-56]∪[56,∞); -50 falls strictly inside the forbidden gap, so it is unreachable.",
    ),
    dict(
        question_type="MCQ",
        question_text="If (3+2√2) is a root of the equation ax²+bx+c=0, and (4+2√3) is a root of the equation ay²+my+n=0, where a, b, c, m and n are integers, then the value of (b/m + (c−2b)/n) is",
        options=["0", "3", "4", "1"],
        correct_answer="4",
        explanation="Rational coefficients force the conjugate roots 3-2√2 and 4-2√3. Sum/product give b=-6a, c=a, m=-8a, n=4a. Then b/m=3/4 and (c-2b)/n=(a+12a)/4a=13/4, summing to 4.",
    ),
    dict(
        question_type="MCQ",
        question_text="A glass contains 500 cc of milk and a cup contains 500 cc of water. From the glass, 150 cc of milk is transferred to the cup and mixed thoroughly. Next, 150 cc of this mixture is transferred from the cup to the glass. Now, the amount of water in the glass and the amount of milk in the cup are in the ratio",
        options=["1 : 1", "10 : 3", "10 : 13", "3 : 10"],
        correct_answer="1 : 1",
        explanation="After the first transfer the cup has 650cc (3/13 milk, 10/13 water). Transferring 150cc of that back leaves the glass with 1500/13 cc water and the cup with 1500/13 cc milk - an exact 1:1 ratio.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let r be a real number and f(x) = 2x−r if x≥r, and f(x) = r if x<r. Then the equation f(x) = f(f(x)) holds for all real values of x where",
        options=["x ≤ r", "x > r", "x ≥ r", "x ≠ r"],
        correct_answer="x ≤ r",
        explanation="For x≥r, f(f(x))=f(2x-r)=4x-3r, so f(x)=f(f(x)) forces x=r. For x<r, f(x)=r and f(f(x))=f(r)=r, so the equation holds for every x<r. Combined: x≤r.",
    ),
    dict(
        question_type="MCQ",
        question_text="Nitu has an initial capital of ₹20,000. Out of this, she invests ₹8,000 at 5.5% in bank A, ₹5,000 at 5.6% in bank B and the remaining amount at x% in bank C, each rate being simple interest per annum. Her combined annual interest income from these investments is equal to 5% of the initial capital. If she had invested her entire initial capital in bank C alone, then her annual interest income, in rupees, would have been",
        options=["900", "800", "1000", "700"],
        correct_answer="800",
        explanation="Interest from A and B is 440+280=720. Total needed is 5% of 20000=1000, so interest from the remaining 7000 (bank C) is 280, giving x=4%. Investing the full 20000 at 4% gives 800.",
    ),
    dict(
        question_type="MCQ",
        question_text="The minimum possible value of (x²−6x+10)/(3−x), for x < 3, is",
        options=["−2", "2", "1/2", "−1/2"],
        correct_answer="2",
        explanation="Substituting t=3-x>0, the numerator becomes t²+1, so the expression is t+1/t, which by AM-GM has minimum 2 at t=1 (x=2).",
    ),
    dict(
        question_type="TITA",
        question_text="If (√(7/5))^(3x−y) = 875/2401 and (4a/b)^(6x−y) = (2a/b)^(y−6x), for all non-zero real values of a and b, then the value of x+y is",
        correct_answer="14",
        explanation="875/2401=(7/5)^(-3), giving (3x-y)/2=-3, i.e. 3x-y=-6. The second equation holding for all a,b forces its exponent to vanish: 6x-y=0, i.e. y=6x. Solving together gives x=2, y=12, so x+y=14.",
    ),
    dict(
        question_type="MCQ",
        question_text="A group of N people worked on a project. They finished 35% of the project by working 7 hours a day for 10 days. Thereafter, 10 people left the group and the remaining people finished the rest of the project in 14 days by working 10 hours a day. Then the value of N is",
        options=["150", "36", "140", "23"],
        correct_answer="140",
        explanation="Person-hours for 35% = 70N; for the remaining 65% = 140(N-10). Since work is proportional to person-hours, 140(N-10)/65 = 70N/35 = 2N, giving 140N-1400=130N, so N=140.",
    ),
    dict(
        question_type="MCQ",
        question_text="In a triangle ABC, AB = AC = 8 cm. A circle drawn with BC as diameter passes through A. Another circle drawn with center at A passes through B and C. Then the area, in sq. cm, of the overlapping region between the two circles is",
        options=["16(π−1)", "32π", "32(π−1)", "16π"],
        correct_answer="32(π−1)",
        explanation="BC as diameter passing through A forces ∠BAC=90°, so BC=8√2. With A=(0,0), B=(8,0), C=(0,8), circle1 (center (4,4), r=4√2) and circle2 (center A, r=8) intersect at B,C. The standard lens-area formula gives 16π+16π-32 = 32(π-1).",
    ),
    dict(
        question_type="MCQ",
        question_text="Suppose k is any integer such that the equation 2x²+kx+5=0 has no real roots and the equation x²+(k−5)x+1=0 has two distinct real roots for x. Then, the number of possible values of k is",
        options=["7", "9", "8", "13"],
        correct_answer="9",
        explanation="No real roots needs k²<40, i.e. -6≤k≤6 (13 integers). Two distinct real roots needs (k-5)²>4, i.e. k<3 or k>7. Combined with k≤6, only k<3 applies, giving k∈{-6,...,2} - 9 values.",
    ),
    dict(
        question_type="TITA",
        question_text="A school has less than 5000 students and if the students are divided equally into teams of either 9 or 10 or 12 or 25 each, exactly 4 are always left out. However, if they are divided into teams of 11 each, no one is left out. The maximum number of teams of 12 each that can be formed out of the students in the school is",
        correct_answer="150",
        explanation="N=900k+4 (LCM of 9,10,12,25 is 900) with N<5000 gives k=0..5. Requiring N divisible by 11 gives k≡2 (mod 11), so k=2 and N=1804. Dividing by 12 gives 150 full teams (with 4 left over).",
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
                    CatQuestion.source_year == 2022,
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
                source_year=2022,
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
        print(f"Inserted {inserted} CAT 2022 QA Slot 3 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

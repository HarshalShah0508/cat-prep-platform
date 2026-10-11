"""Add the 13 CAT 2022 QA Slot 2 questions missing from the DB (9/22 loaded).
Found by diffing against pyq-source/2022/QUANT_SLOT2_CAT_2022.pdf, a plain
question dump with no inline answer key. Every answer below was solved
independently; the two riskiest (Q1's time-and-work and Q5's sequence
puzzle) were cross-checked against a web search, the rest via clean Vieta's/
geometry/algebra derivations.

Run with:
    python -m app.scripts.backfill_qa_2022_slot2_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="TITA",
        question_text="Working alone, the times taken by Anu, Tanu and Manu to complete any job are in the ratio 5 : 8 : 10. They accept a job which they can finish in 4 days if they all work together for 8 hours per day. However, Anu and Tanu work together for the first 6 days, working 6 hours 40 minutes per day. Then, the number of hours that Manu will take to complete the remaining job working alone is",
        correct_answer="6",
        explanation="Individual rates (work/hour) are proportional to 1/5, 1/8, 1/10; scaling to match the combined rate W/32 (4 days x 8h) gives rate_Anu=W/68, rate_Tanu=5W/544, rate_Manu=W/136. In 40 hours (6 days x 6h40m), Anu+Tanu complete 65W/68, leaving 3W/68, which Manu (rate W/136) finishes in 6 hours.",
    ),
    dict(
        question_type="TITA",
        question_text="Mr. Pinto invests one-fifth of his capital at 6%, one-third at 10% and the remaining at 1%, each rate being simple interest per annum. Then, the minimum number of years required for the cumulative interest income from these investments to equal or exceed his initial capital is",
        correct_answer="20",
        explanation="Annual interest as a fraction of capital: (1/5)(0.06)+(1/3)(0.10)+(7/15)(0.01) = 0.05, i.e. 1/20 of the capital per year. Reaching 100% of the capital in interest therefore takes 20 years.",
    ),
    dict(
        question_type="TITA",
        question_text="Regular polygons A and B have number of sides in the ratio 1 : 2 and interior angles in the ratio 3 : 4. Then the number of sides of B equals",
        correct_answer="10",
        explanation="With sides n and 2n, the interior angle ratio [(n-2)/n] / [(n-1)/n] = (n-2)/(n-1) = 3/4 gives n=5, so B has 2n=10 sides.",
    ),
    dict(
        question_type="TITA",
        question_text="The average of a non-decreasing sequence of N numbers a1,a2,......,aN is 300. If a1 is replaced by 6a1, the new average becomes 400. Then, the number of possible values of a1 is",
        correct_answer="14",
        explanation="From the two averages, 5a1=100N, so a1=20N. Since a1 is the minimum of a non-decreasing sequence, a1≤300, giving N≤15; N=1 is impossible (it would force a1=300≠20). So N ranges from 2 to 15, giving 14 possible values of a1.",
    ),
    dict(
        question_type="MCQ",
        question_text="The length of each side of an equilateral triangle ABC is 3 cm. Let D be a point on BC such that the area of triangle ADC is half the area of triangle ABD. Then the length of AD, in cm, is",
        options=["√7", "√6", "√8", "√5"],
        correct_answer="√7",
        explanation="Since ABD and ADC share the same height from A, their areas are proportional to BD and DC. Area ABD = 2 x Area ADC gives BD=2, DC=1. By the law of cosines in triangle ABD (angle B=60°): AD²=9+4-2(3)(2)(0.5)=7, so AD=√7.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let f(x) be a quadratic polynomial in x such that f(x) ≥0 for all real numbers x. If f(2)=0 and f(4)=6, then f(−2) is equal to",
        options=["36", "12", "24", "6"],
        correct_answer="24",
        explanation="f≥0 everywhere with f(2)=0 forces a double root at x=2: f(x)=k(x-2)². f(4)=4k=6 gives k=1.5, so f(-2)=1.5(16)=24.",
    ),
    dict(
        question_type="MCQ",
        question_text="In an election, there were four candidates and 80% of the registered voters casted their votes. One of the candidates received 30% of the casted votes while the other three candidates received the remaining casted votes in the proportion 1 : 2 : 3. If the winner of the election received 2512 votes more than the candidate with the second highest votes, then the number of registered voters was",
        options=["62800", "50240", "40192", "60288"],
        correct_answer="62800",
        explanation="With V registered voters, 0.8V cast votes: one candidate gets 0.24V, the other three split 0.56V in ratio 1:2:3, i.e. 0.0933V, 0.1867V, 0.28V. The winner (0.28V) beats the runner-up (0.24V) by 0.04V=2512, giving V=62800.",
    ),
    dict(
        question_type="MCQ",
        question_text="There are two containers of the same volume, first container half-filled with sugar syrup and the second container half-filled with milk. Half the content of the first container is transferred to the second container, and then the half of this mixture is transferred back to the first container. Next, half the content of the first container is transferred back to the second container. Then the ratio of sugar syrup and milk in the second container is",
        options=["6 : 5", "5 : 6", "4 : 5", "5 : 4"],
        correct_answer="5 : 6",
        explanation="Tracking volumes through each transfer (with container volume V): after all three steps, container two ends up with 5V/16 syrup and 6V/16 milk, a ratio of 5:6.",
    ),
    dict(
        question_type="MCQ",
        question_text="For some natural number n, assume that (15,000)! is divisible by (n!)!. The largest possible value of n is",
        options=["5", "4", "6", "7"],
        correct_answer="7",
        explanation="(n!)! divides 15000! exactly when n!≤15000. Since 7!=5040≤15000 but 8!=40320>15000, the largest valid n is 7.",
    ),
    dict(
        question_type="TITA",
        question_text="Suppose for all integers x, there are two functions f and g such that f(x) + f(x−1)−1=0 and g(x)=x². If f(x²− x) = 5, then the value of the sum f(g(5))+g(f(5)) is",
        correct_answer="12",
        explanation="f(x)=1-f(x-1) gives f(x)=f(x-2), so f depends only on parity. Since x²-x is always even, f(even)=5, so f(odd)=1-5=-4. g(5)=25 (odd), so f(g(5))=-4; f(5)=-4 (odd), so g(f(5))=16. Sum=-4+16=12.",
    ),
    dict(
        question_type="MCQ",
        question_text="In triangle ABC, altitudes AD and BE are drawn to the corresponding bases. If ∠BAC = 45° and ∠ABC = θ, then AD/BE equals",
        options=["√2cos θ", "1", "√2sin θ", "(sin θ+cos θ)/√2"],
        correct_answer="√2sin θ",
        explanation="AD=AB sin(θ) (from right triangle ABD) and BE=AB sin(45°) (from right triangle ABE), so AD/BE = sinθ/sin45° = √2 sinθ.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let r and c be real numbers. If r and -r are roots of 5x³ +cx² −10x + 9 = 0, then c equals",
        options=["4", "−4", "−9/2", "9/2"],
        correct_answer="−9/2",
        explanation="With the third root s, Vieta's gives sum of pairwise products -r²=-10/5=-2, so r²=2; product of roots -r²s=-9/5 gives s=9/10; sum of roots s=-c/5 gives c=-5s=-9/2.",
    ),
    dict(
        question_type="MCQ",
        question_text="Consider the arithmetic progression 3,7,11,… and let An denote the sum of the first n terms of this progression. Then the value of (1/25)·Σ(n=1 to 25) An is",
        options=["442", "404", "455", "415"],
        correct_answer="455",
        explanation="An=n(2n+1)=2n²+n. Summing for n=1 to 25: 2·Σn²+Σn = 2(5525)+325=11375. Dividing by 25 gives 455.",
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
                source_year=2022,
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
        print(f"Inserted {inserted} CAT 2022 QA Slot 2 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

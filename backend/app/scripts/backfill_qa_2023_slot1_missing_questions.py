"""Add the 11 CAT 2023 QA Slot 1 questions missing from the DB (11/22 loaded).
Found by diffing against pyq-source/2023/QUANT_SLOT1_CAT_2023.pdf, a plain
question dump with no inline answer key. Every answer below was solved
independently; three (Q4, Q18, Q20) were cross-checked against a web search
after the source PDF's math rendering turned out to have OCR errors (wrong
log base, wrong circle equation, and a misread nested radical respectively)
that didn't match the real official question.

Run with:
    python -m app.scripts.backfill_qa_2023_slot1_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="MCQ",
        question_text="Let n be the least positive integer such that 168 is a factor of 1134^n. If m is the least positive integer such that 1134^n is a factor of 168^m, then m+n equals:",
        options=["24", "12", "9", "15"],
        correct_answer="15",
        explanation="168=2³·3·7 and 1134=2·3⁴·7. For 168 | 1134^n, the binding constraint is the factor of 2³, needing n≥3, so n=3. Then 1134³=2³·3¹²·7³; for this to divide 168^m=2^(3m)·3^m·7^m, the binding constraint is 3^12, needing m≥12, so m=12. m+n=15.",
    ),
    dict(
        question_type="MCQ",
        question_text="If √(5x+9) + √(5x−9) = 3(2+√2), then √(10x+9) is equal to:",
        options=["3√31", "2√7", "3√7", "4√5"],
        correct_answer="3√7",
        explanation="With a=√(5x+9), b=√(5x-9): a+b=6+3√2, and a²-b²=18 gives a-b=18/(6+3√2)=6-3√2. Adding, 2a=12 so a=6, giving 5x+9=36, x=27/5. Then 10x+9=63, so √(10x+9)=√63=3√7.",
    ),
    dict(
        question_type="MCQ",
        question_text="If x and y are positive real numbers such that log_x(x²+12)=4 and 3 log_y x = 1, then x + y equals:",
        options=["10", "68", "20", "11"],
        correct_answer="10",
        explanation="log_x(x²+12)=4 gives x²+12=x⁴, i.e. (x²-4)(x²+3)=0, so x=2 (positive root). From 3log_y x=1, log_y x=1/3 so x=y^(1/3), giving y=x³=8. x+y=10.",
    ),
    dict(
        question_type="TITA",
        question_text="The number of integer solutions of the equation 2|x|(x²+1)=5x² is:",
        correct_answer="3",
        explanation="x=0 trivially works. For x≠0, setting t=|x|>0 gives 2t³-5t²+2t=0, i.e. t(2t-1)(t-2)=0, so t=2 or t=0.5. Only t=2 gives integers (x=±2). Total integer solutions: x=0,2,-2 - three.",
    ),
    dict(
        question_type="TITA",
        question_text="The equation x³+(2r+1)x²+(4r−1)x+2=0 has −2 as one of the roots. If the other two roots are real, then the minimum possible non-negative integer value of r is:",
        correct_answer="2",
        explanation="Dividing by (x+2) gives the other factor x²+(2r-1)x+1=0 (x=-2 is a root for every r). Real roots require (2r-1)²≥4, i.e. r≥1.5 or r≤-0.5. The smallest non-negative integer satisfying this is r=2.",
    ),
    dict(
        question_type="TITA",
        question_text="Let α and β be the two distinct roots of the equation 2x²−6x+k=0, such that (α+β) and αβ are the distinct roots of the equation x²+px+p=0. Then, the value of 8(k−p) is:",
        correct_answer="6",
        explanation="α+β=3 and αβ=k/2 are the roots of x²+px+p=0, so their sum 3+k/2=-p and product 3k/2=p. Solving gives k=-3/2 and p=-9/4, so 8(k-p)=8(3/4)=6.",
    ),
    dict(
        question_type="MCQ",
        question_text="The minor angle between the hour hand and the minute hand of a clock was observed at 8:48 am. The minimum duration, in minutes, after 8:48 am when this angle increases by 50% is:",
        options=["24/11", "36/11", "4", "2"],
        correct_answer="24/11",
        explanation="At 8:48, the minute hand is at 288° and hour hand at 264°, a gap of 24°. The gap grows at 5.5°/min (minute hand gains on hour hand), so reaching 36° (a 50% increase) takes 12/5.5=24/11 minutes.",
    ),
    dict(
        question_type="MCQ",
        question_text="Gita sells two objects A and B at the same price such that she makes a profit of 20% on object A and a loss of 10% on object B. If she increases the selling price such that objects A and B are still sold at an equal price and a profit of 10% is made on object B, then the profit made on object A will be nearest to:",
        options=["42%", "49%", "45%", "47%"],
        correct_answer="47%",
        explanation="With cost Ca=S/1.2 and Cb=S/0.9 from the original equal price S, the new price S'=1.1Cb. The profit on A is (S'-Ca)/Ca = 7/15 ≈ 46.67%, nearest to 47%.",
    ),
    dict(
        question_type="MCQ",
        question_text="A quadrilateral ABCD is inscribed in a circle such that AB:CD = 2:1 and BC:AD = 5:4. If AC and BD intersect at the point E, then AE:CE equals:",
        options=["2 : 1", "1 : 2", "8 : 5", "5 : 8"],
        correct_answer="8 : 5",
        explanation="Similar triangles AEB~DEC give AE/DE=BE/CE=AB/CD=2. Similar triangles AED~BEC give AE/BE=DE/CE=AD/BC=4/5. Combining these ratios gives AE:CE = 8:5.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let C be the circle given by the equation: x²+y²+4x−6y−3=0, and let L be the locus of the point of intersection of a pair of tangents to C with the angle between the two tangents equal to 60°. Then, find the point at which L touches the line x=6.",
        options=["(6,6)", "(6,4)", "(6,8)", "(6,3)"],
        correct_answer="(6,3)",
        explanation="Circle C has center (-2,3) and radius 4. The locus L is concentric with radius R=r/sin30°=8. Since the distance from (-2,3) to the line x=6 is exactly 8=R, the line is tangent to L at the point directly across: (6,3).",
    ),
    dict(
        question_type="MCQ",
        question_text="For some positive and distinct real numbers x, y and z, if 1/(√y+√z) is the arithmetic mean of 1/(√x+√z) and 1/(√x+√y), then the relationship which will always hold true is:",
        options=["x, y, and z are in arithmetic progression", "√x, √y, and √z are in arithmetic progression", "y, x, and z are in arithmetic progression", "√x, √z, and √y are in arithmetic progression"],
        correct_answer="y, x, and z are in arithmetic progression",
        explanation="Setting a=√x,b=√y,c=√z and clearing denominators in 2/(b+c)=1/(a+c)+1/(a+b) simplifies to 2a²=b²+c², i.e. 2x=y+z - so x is the mean of y and z, meaning y,x,z are in AP.",
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
                source_year=2023,
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
        print(f"Inserted {inserted} CAT 2023 QA Slot 1 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

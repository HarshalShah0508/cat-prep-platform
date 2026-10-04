"""Backfill correct_answer/explanation for CAT 2021 QA Slot 2, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are rewritten in plain language, not copied verbatim. Only questions with a
resolvable "Correct Answer:" line are covered - several TITA questions in
this paper state their answer only in free-form solution prose with no
clean marker, so are left ungraded rather than guessed.

Run with:
    python -m app.scripts.backfill_qa_2021_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("Three positive integers x, y, z are in arithmetic progression. If y − x > 2 and xyz = 5(x + y + z), then z − x equals:", "8", "With y=x+d and z=x+2d (arithmetic progression), substituting into xyz=5(x+y+z) and solving shows x=4, d=4 works, giving z−x = 2d = 8."),
    ("Raj invested 10000 in a fund. At the end of the first year, he incurred a loss, but his balance was more than 5000. This balance, when invested for another year, grew and the percentage of growth in the second year was five times the percentage of loss in the first year. If the gain of Raj from the initial investment over the two-year period is 35%, then the per- centage of loss in the first year is:", "15", "Letting the first-year loss be x% and the second-year gain be 5x%, the overall 35% two-year gain condition sets up an equation in x whose valid solution (consistent with the balance staying above 5000 after the loss) gives a first-year loss of 15%."),
    ("Two trains A and B were moving in opposite directions, their speeds being in the ratio 5:3. The front end of A crossed the rear end of B 46 seconds after the front ends of the trains had crossed each other. It took another 69 seconds for the rear ends of the trains to cross each other. The ratio of the length of train A to that of train B is:", "5:3", "With the trains' speeds in ratio 5:3, comparing the 46-second front-to-front crossing and 69-second front-to-rear crossing gives equal train lengths, so the length ratio is simply 5:3 as well."),
    ("The sides AB and CD of a trapezium ABCD are parallel, with AB being the smaller side. P is the midpoint of CD and ABPD is a parallelogram. If the difference between the areas of the parallelogram ABPD and the triangle BPC is 10 sq cm, then the area, in sq cm, of the trapezium ABCD is:", "40", "Since ABPD is a parallelogram, its area is half the trapezium's area; the triangle BPC's area is a different half-based expression. Setting their difference to 10 sq cm and solving gives the trapezium's full area as 40 sq cm."),
    ("For a real number x, the condition |3x − 201 + 13x − 40| = 20 necessarily holds. Then, the value of x lies in the range:", "7 < x < 12", "Simplifying the absolute value condition reduces it to |16x−241|=20, and solving the two resulting cases pins the valid range of x down to 7 < x < 12."),
    ("Anil can paint a house in 60 days while Bimal can paint it in 84 days. Anil starts painting and after 10 days, Bimal and Charu join him. Together, they complete the painting in 14 more days. If they are paid a total of 21000 for the job, then the share of Charu, in INR, proportionate to the work done by him, is:", "9100", "Anil works alone for 10 days, then all three work together for the remaining 14 days to finish the job. Solving for Charu's work rate and splitting the payment proportionally gives Charu's share as ₹9100."),
    ("A person buys tea of three different qualities at 800, 500, and 300 per kg, respectively, and the amounts bought are in the proportion 2:3:5. She mixes all the tea and sells one-sixth\n\nof the mixture at 700 per kg. The price, in INR per kg, at which she should sell the remaining tea, to make an overall profit of 50%, is:", "688", "Mixing the three teas in ratio 2:3:5 gives an average cost of ₹460/kg. Selling one-sixth of it at ₹700/kg and needing an overall 50% profit, solving for the remaining five-sixths' selling price gives ₹688/kg."),
    ("Consider the pair of equations: x2 − xy − x = 22 and y 2 − xy + y = 34. If x > y , then x − y equals:", "4", "Subtracting the two given equations and factoring leads to (x−y)(x+y−1) = −12, while adding them and substituting (x−y)² gives another relation - solving these together shows x−y = 4."),
    ("Anil, Bobby, and Chintu jointly invest in a business and agree to share the overall profit in proportion to their investments. Anil’s share of investment is 70%. His share of profit decreases by 420 if the overall profit goes down from 18% to 15%. Chintu’s share of profit increases by 80 if the overall profit goes up from 15% to 17%. The amount, in INR, invested by Bobby is:", "2000", "Anil's profit changes by ₹420 when the profit rate shifts by 3 percentage points on his 70% share, which pins the total investment at ₹20,000. Using Chintu's ₹80 profit change at a 2-point rate shift gives his investment as ₹4000, leaving Bobby with ₹6000−₹4000 = ₹2000."),
    ("Two pipes A and B are attached to an empty water tank. Pipe A fills the tank while pipe B drains it. If pipe A is opened at 2 pm and pipe B is opened at 3 pm, then the tank becomes full at 10 pm. Instead, if pipe A is opened at 2 pm and pipe B is opened at 4 pm, then the tank becomes full at 6 pm. If pipe B is not opened at all, then the time, in minutes, taken to fill the tank is:", "144", "Setting up the fill/drain equations for both opening-time scenarios and solving for pipe A's rate shows it alone would fill the tank in 2.4 hours - that's 144 minutes."),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "QA",
                    CatQuestion.question_text == question_text,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

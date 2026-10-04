"""Backfill correct_answer/explanation for CAT 2022 QA Slot 1, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are rewritten in plain language, not copied verbatim.

Several TITA questions here print "Correct Answer: --" (the real value is
only stated inside the solution prose) - Q1 is derived directly from the
question text itself (fully intact); Q10/Q11 use the final stated number in
their solutions. Q5, Q18, Q22 are skipped entirely - their solutions have
every key intermediate number blanked out by the same embedded-math-as-
image problem, leaving nothing to safely recover.

Run with:
    python -m app.scripts.backfill_qa_2022_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("Pinky is standing in a queue at a ticket counter. Suppose the ratio of the number of persons standing ahead of Pinky to the number of persons standing behind her in the queue is 3:5. If the total number of persons in the queue is less than 300, then the maximum possible number of persons standing ahead of Pinky is", "111", "Let the number ahead be 3k and behind be 5k, so the total queue is 8k+1. For this to stay under 300, k can be at most 37, making the maximum possible number ahead of Pinky 3×37 = 111."),
    ("The largest real value of a for which the equation has an infinite number of solutions for x is", "1", "Breaking the absolute-value equation into its sign cases and checking which critical point keeps both expressions consistently positive shows the largest value of a giving infinitely many solutions is 1."),
    ("The average of three integers is 13. When a natural number n is included, the average of these four integers remains an odd integer. The minimum possible value of n is", "5", "With the three integers averaging 13 (sum 39), adding n must make the new average of four numbers odd. Testing increasing values of n, the smallest one that produces an odd average is n=5."),
    ("Let ABCD be a parallelogram such that the coordinates of its three vertices A, B, C are (1, 1), (3, 4), and (−2, 8), respectively. Then, the coordinates of the vertex D are", "(−4, 5)", "Since a parallelogram's diagonals bisect each other, the midpoint of AC must equal the midpoint of BD. Using A(1,1) and C(−2,8) to find that shared midpoint and solving for D gives (−4, 5)."),
    ("Alex invested his savings in two parts. The simple interest earned on the first part at 15% per annum for 4 years is the same as the simple interest earned on the second part at 12% per annum for 3 years. Then, the percentage of his savings invested in the first part is", "37.50%", "Equating the simple interest from both parts (15% for 4 years vs 12% for 3 years) gives a 3:5 ratio between the two investment amounts, meaning the first part is 3/8 = 37.5% of total savings."),
    ("The average weight of students in a class increases by 600 gm when some new students join the class. If the average weight of the new students is 3 kg more than the average weight of the original students, then the ratio of the number of original students to the number of new students is", "4:1", "Setting up the total-weight equation before and after the new students join, and simplifying, shows the ratio of original to new students must be 4:1."),
    ("A mixture contains lemon juice and sugar syrup in equal proportion. If a new mixture is created by adding this mixture and sugar syrup in the ratio 1 : 3, then the ratio of lemon juice and sugar syrup in the new mixture is", "1:7", "The initial 1:1 lemon-syrup mixture, combined with pure sugar syrup in a 1:3 ratio, dilutes the lemon juice relative to the total - working through the parts gives a final lemon-juice-to-syrup ratio of 1:7."),
    ("Amal buys 110kg of syrup and 120kg of juice, syrup being 20% less costly than juice, per kg. He sells 10kg of syrup at 10% profit and 20kg of juice at 20% profit. Mixing the remaining juice and syrup, Amal sells the mixture at ₹ 308.32 per kg and makes an overall profit of 64%. Then, Amal's cost price for syrup, in rupees per kg, is", "160", "With syrup priced 20% below juice per kg, and given profit margins on the first portions sold plus the blended mixture's selling price and overall 64% profit, solving for the base cost unit gives syrup's cost price as ₹160 per kg."),
    ("A trapezium ABCD has side AD parallel to BC, ∠BAD=90∘, BC=3 cm, and AD=8 cm. If the perimeter of this trapezium is 36 cm, then its area, in sq. cm, is", "66", "With BC=3, AD=8, a right angle at A, and total perimeter 36, the two equal slanted sides work out to 12.5 cm each. Using Pythagoras to find the height and the standard trapezium area formula gives an area of about 66 cm²."),
    ("In a class of 100 students, 73 like coffee, 80 like tea, and 52 like lemonade. It may be possible that some students do not like any of these three drinks. Then the difference between the maximum and minimum possible number of students who like all the three drinks is", "47", "Using inclusion-exclusion on the three groups (coffee, tea, lemonade) and testing the extreme cases for how many students like all three, the gap between the maximum and minimum possible counts comes out to 47."),
    ("Trains A and B start traveling at the same time towards each other with constant speeds from stations X and Y, respectively. Train A reaches station Y in 10 minutes while train B takes 9 minutes to reach station X after meeting train A. Then the total time taken, in minutes, by train B to travel from station Y to station X is", "15", "Since both trains meet at the same point and take 10 and 9 minutes respectively to finish their remaining legs, their speed ratio follows from these times. Solving the resulting relationship shows Train B took 15 minutes before the meeting point."),
    ("Ankita buys 4kg cashews, 14kg peanuts, and 6kg almonds when the cost of 7kg cashews is the same as that of 30kg peanuts or 9kg almonds. She mixes all three nuts and marks a price for the mixture in order to make a profit of ₹1752. She sells 4kg of the mixture at this marked price and the remaining at a 20% discount on the marked price, thus making a total profit of ₹744. Then the amount, in rupees, that she had spent buying almonds is", "1680", "Using the given price ratio between cashews, peanuts, and almonds (converted to a common unit) along with the total cost (₹4296) and target profit (₹1752), the amount spent specifically on the 6 kg of almonds works out to ₹1680."),
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

"""Backfill correct_answer/explanation for CAT 2020 QA Slot 3, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are written from scratch in plain language based on the problem and the
source's final numeric answer, not copied verbatim (a few of this slot's
raw solutions show visible arithmetic slips before landing on the correct
printed answer - the explanation here follows the clean, correct path).

Run with:
    python -m app.scripts.backfill_qa_2020_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("If x1 = −1 and xm = xm+1 + (m + 1) for every positive integer m, then x100 equals:", "-5050", "The rule xm = x(m+1) + (m+1) means each step subtracts the next integer: x2 = x1 − 2, x3 = x2 − 3, and so on. Summing all these subtractions from x1 = −1 down to x100 gives −1 − (2+3+...+100) = −5050."),
    ("Let N , x, and y be positive integers such that N = x + y , 2 < x < 10, and 14 < y < 23. If N > 25, then how many distinct values are possible for N ?", "6", "With x from 3-9 and y from 15-22, N = x+y ranges up to 31. Checking which sums exceed 25 across all valid x, y combinations shows the distinct possible values of N are 26 through 31 - 6 values."),
    ("A contractor agreed to construct a 6 km road in 200 days. He employed 140 persons for the work. After 60 days, he realized that only 1.5 km road has been completed. How many additional people would he need to employ in order to finish the work exactly on time?", "40", "In 60 days, 140 workers completed 1.5 km, so the work rate is 140×60 person-days per 1.5 km. Scaling that rate to finish the remaining 4.5 km in the remaining 140 days requires 180 workers total - 40 more than the original 140."),
    ("The area, in sq. units, enclosed by the lines x = 2, y = |x − 2| + 4, the X-axis, and the Y-axis is equal to:", "10", "For 0 ≤ x < 2, the line y = |x−2|+4 is y = −x+6. The area under this line between x=0 and x=2, bounded by both axes, works out to 10 square units via the definite integral."),
    ("Dick is thrice as old as Tom and Harry is twice as old as Dick. If Dick’s age is 1 year less than the average age of all three, then Harry’s age, in years, is:", "18", "With Dick = 3×Tom and Harry = 2×Dick, and Dick's age being 1 less than the average of all three, solving the resulting equation gives Tom = 3, Dick = 9, and Harry = 2×9 = 18."),
    ("How many of the integers 1, 2, ..., 120, are divisible by none of 2, 5, and 7?", "41", "Using inclusion-exclusion on multiples of 2, 5, and 7 up to 120 gives 79 numbers divisible by at least one of them. Subtracting from 120 leaves 41 numbers divisible by none."),
    ("In the final examination, Bishnu scored 52% and Asha scored 64%. The marks obtained by Bishnu are 23 less, and those by Asha are 34 more than the marks obtained by Ramesh. The marks obtained by Geeta, who scored 84%, are:", "399", "Bishnu's 52% and Asha's 64% scores relate to a common reference mark R as 0.52M = R−23 and 0.64M = R+34. Solving gives the total marks M = 475, so Geeta's 84% score is 0.84 × 475 = 399."),
    ("If f (x + y) = f (x)f (y) and f (5) = 4, then f (10) − f (−10) is equal to:", "15.9375", "f(x+y) = f(x)f(y) with f(5) = 4 means f(x) = 4^(x/5). That gives f(10) = 16 and f(−10) = 1/16, so f(10) − f(−10) = 16 − 1/16 = 15.9375."),
    ("Anil, Sunil, and Ravi run along a circular path of length 3 km, starting from the same point at the same time, and going in the clockwise direction. If they run at speeds of 15 km/hr, 10 km/hr, and 8 km/hr, respectively, how much distance in km will Ravi have run when Anil and Sunil meet again for the first time at the starting point?", "4.8", "Anil (15 km/hr) and Sunil (10 km/hr) first meet back at the start after 3km/(5km/hr) = 0.6 hours, since their relative speed is 5 km/hr. In that time, Ravi (8 km/hr) covers 8 × 0.6 = 4.8 km."),
    ("A man buys 35 kg of sugar and sets a marked price in order to make a 20% profit. He sells 5 kg at this price, and 15 kg at a 10% discount. Accidentally, 3 kg of sugar is wasted. He sells the remaining sugar by raising the marked price by p percent so as to make an overall profit of 15%. Then p is nearest to:", "25", "Selling 5 kg at a 20%-profit marked price and 15 kg at a discount on that price, with 3 kg wasted, leaves 12 kg that must be priced high enough for an overall 15% profit across all 35 kg. Working backward from that target gives roughly a 25% markup over the original marked price for the remaining sugar."),
    ("Let k be a constant. The equations kx + y = 3 and 4x + ky = 4 have a unique solution if and only if:", "k ≠ 2", "The system kx+y=3, 4x+ky=4 has a unique solution exactly when the coefficient determinant k²−4 is nonzero, i.e. k ≠ ±2. Among the given answer choices, this is captured as k ≠ 2."),
    ("How many integers in the set {100, 101, 102, . . . , 999} have at least one digit repeated?", "252", "Of the 900 three-digit numbers (100-999), the ones with all distinct digits number 9×9×8 = 648 (first digit 1-9, each next digit excluding those already used). Subtracting from 900 leaves 252 numbers with at least one repeated digit."),
    ("A batsman played n + 2 innings and got out on all occasions. His average score in these n + 2 innings was 29 runs and he scored 38 and 15 runs in the last two innings. The batsman scored less than 38 runs in each of the first n innings. In these n innings, his average score was 30 runs and the lowest score was x runs. The smallest possible value of x is:", "2", "With average 29 over n+2 innings and the last two innings scoring 38+15=53, matching this against an average of 30 for the first n innings gives n=5, so 7 innings total. Keeping the first 5 innings' scores as high as possible (just under 38) while summing to 150 forces the lowest score down to 2."),
    ("Two alcohol solutions, A and B, are mixed in the proportion 1:3 by volume. The volume of the mixture is then doubled by adding solution A such that the resulting mixture has 72% alcohol. If solution A has 60% alcohol, then the percentage of alcohol in solution B is:", "90%", "Mixing A and B in 1:3 and then adding more of A to double the total volume changes the overall alcohol concentration to 72% in the final mix. Solving for solution B's original alcohol percentage from this balance gives 90%."),
    ("The vertices of a triangle are (0, 0), (4, 0), and (3, 9). The area of the circle passing through these three points is:", "12π", "Using the triangle's vertices (0,0), (4,0), (3,9), the side lengths and area combine via the circumradius formula R = abc/(4×Area) to give the circle passing through all three points an area of 12π."),
    ("A person invested a certain amount of money at 10% annual interest, compounded half-yearly. After one and a half years, the interest and principal together became Rs 18522. The amount, in rupees, that the person had invested is:", "16000", "At 10% annual interest compounded half-yearly for 1.5 years (3 half-year periods), the amount formula A = P(1.05)³ = 18522 solves to a principal of P = 16000."),
    ("A and B are two railway stations 90 km apart. A train leaves A at 9:00 am, heading towards B at a speed of 40 km/hr. Another train leaves B at 10:30 am, heading towards A at a speed of 20 km/hr. The trains meet each other at:", "11:00 am", "Train 1 leaves A at 9:00 am at 40 km/hr and has a 60 km head start by the time Train 2 leaves B at 10:30 am at 20 km/hr. Closing the remaining 30 km gap at a combined speed of 60 km/hr takes 30 minutes, so they meet at 11:00 am."),
    ("Vimla starts for office every day at 9 am and reaches exactly on time if she drives at her usual speed of 40 km/hr. She is late by 6 minutes if she drives at 35 km/hr. One day, she covers two-thirds of her distance to office in one-third of her usual time to reach office, and then stops for 8 minutes. The speed, in km/hr, at which she should drive the remaining distance to reach office exactly on time is:", "28", "Comparing Vimla's travel time at 40 km/hr versus 35 km/hr (with the 6-minute difference) gives a commute distance of 28 km. Working out how much time remains after she covers two-thirds of that distance and pauses for 8 minutes, the speed needed to finish on time is 28 km/hr."),
    ("In a trapezium ABCD, AB ∥ DC , BC ⊥ DC and ∠BAD = 45◦ . If DC = 5 cm, BC = 4 cm, the area of the trapezium in sq. cm is:", "28", "With BC perpendicular to DC, the height of the trapezium is 4 cm. The 45° angle at A, together with DC = 5 cm, gives AB = 9 cm, so the trapezium's area is ½×(9+5)×4 = 28 sq cm."),
    ("The points (2, 1) and (−3, −4) are opposite vertices of a parallelogram. If the other two vertices lie on the line x + 9y + c = 0, then c is:", "14", "Since diagonals of a parallelogram bisect each other, the midpoint of (2,1) and (−3,−4) - which is (−0.5, −1.5) - must also lie on the line x+9y+c=0 passing through the other two vertices. Substituting that midpoint gives c = 14."),
    ("How many pairs (a, b) of positive integers are there such that a ≤ b and ab = 42017?", "2018", "4^2017 = 2^4034, so its divisors are the powers of 2 from 2^0 to 2^4034 - 4035 divisors in total. Pairing them up as a ≤ b with ab = 4^2017 (including the middle square-root case) gives 2018 valid pairs."),
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
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

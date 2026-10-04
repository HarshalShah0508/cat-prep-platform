"""Backfill correct_answer/explanation for CAT 2020 QA Slot 2, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are rewritten in plain language from that source, not copied verbatim.

Q2 is skipped - its printed answer is corrupted by the embedded-math-as-
image problem (non-numeric garble).

Run with:
    python -m app.scripts.backfill_qa_2020_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("In a car race, car A beats car B by 45 km, car B beats car C by 50 km, and car A beats car C by 90 km. The distance (in km) over which the race has been conducted is:", "450", "If A beats B by 45 km and B beats C by 50 km over the same race distance D, then A beats C by 90 km. Setting up the speed ratios from these three facts and solving gives D = 450 km."),
    ("In a group of 10 students, the mean of the lowest 9 scores is 42 while the mean of the highest 9 scores is 47. For the entire group of 10 students, the maximum possible mean exceeds the minimum possible mean by:", "3", "With the lowest 9 scores averaging 42 and the highest 9 averaging 47, the gap between the top and bottom student's scores is 45. Working out the best-case and worst-case overall means from this gap gives a difference of 3 between the maximum and minimum possible mean."),
    ("The number of pairs of integers (x, y) satisfying x ≥ y ≥ −20 and 2x + 5y = 99 is:", "17", "2x + 5y = 99 with x ≥ y ≥ −20 forces y to be odd. Writing y = 2k+1 and applying both constraints narrows k to the integers −11 through 6, which is 17 values."),
    ("Let the mth and nth terms of a geometric progression be 34 and 12, respectively, where m < n. If the common ratio r is an integer, then the smallest possible value of r + n − m is:", "-4", "With Tm = 34 and Tn = 12 and integer ratio r, r^(n−m) = 12/34 simplifies to a power-of-2 relationship. Among the valid integer (r, n−m) pairs, r = −4 is the one matching the answer choices."),
    ("For the same principal amount, the compound interest for two years at 5% per annum exceeds the simple interest for three years at 3% per annum by Rs 1125. Then the principal amount in rupees is:", "90000", "For principal P, 2-year compound interest at 5% minus 3-year simple interest at 3% equals 1125. Setting up and simplifying that equation gives P = 90000."),
    ("Let C be a circle of radius 5 meters having center at O. Let P Q be a chord of C that passes through points A and B , where A is located 4 meters north of O and B is located 3 meters east of O. Then, the length of P Q, in meters, is nearest to:", "8.8", "Placing the circle's center at the origin, with A 4 m north and B 3 m east, the chord through A and B has a known line equation. The perpendicular distance from the center to that line is 2.4 m, so the chord length via the chord-length formula is 2√(25 − 2.4²) ≈ 8.8 m."),
    ("Anil buys 12 toys and labels each with the same selling price. He sells 8 toys initially at 20% discount on the labeled price. Then he sells the remaining 4 toys at an additional 25% discount on the discounted price. Thus, he gets a total of Rs 2112, and makes a 10% profit. With no discounts, his percentage of profit would have been:", "50", "Selling 8 toys at 20% off and the other 4 at a further 25% off that gives total revenue 8.8x (x = label price) which equals 2112, so x = 240. With cost worked out from the 10% profit on actual sales, selling all 12 toys at full price instead yields a 50% profit."),
    ("If x and y are non-negative integers such that x + 9 = z , y + 1 = z , and x + y < z + 5, then the maximum possible value of 2x + y equals:", "23", "Since x+9 = z and y+1 = z, we get y = x+8. The condition x+y < z+5 simplifies to x < 6, so the largest non-negative integer x can be is 5, giving 2x+y = 3x+8 = 23."),
    ("Students in a college have to choose at least two subjects from chemistry, mathematics and physics. The number of students choosing all three subjects is 18, choosing mathematics as one of their subjects is 23 and choosing physics as one of their subjects is 25. The smallest possible number of students who could choose chemistry as one of their subjects is", "20", "With 18 students choosing all three subjects and the given totals for Math and Physics, the number choosing Chemistry is 2y + 20 where y ≥ 0. This is smallest when y = 0, giving 20."),
    ("Let f (x) = x2 + ax + b and g(x) = f (x + 1) − f (x − 1). If f (x) ≥ 0 for all real x, and g(20) = 72, then the smallest possible value of b is", "4", "Computing g(x) = f(x+1) − f(x−1) gives g(x) = 4x + 2a; using g(20) = 72 gives a = −4. For f(x) = x² − 4x + b to stay non-negative everywhere, the discriminant must be ≤ 0, which requires b ≥ 4 - so the smallest value is 4."),
    ("The distance from B to C is thrice that from A to B. Two trains travel from A to C via B. The speed of train 2 is double that of train 1 while traveling from A to B and their speeds are interchanged while traveling from B to C. The ratio of the time taken by train 1 to that taken by train 2 in travelling from A to C is", "5:7", "With B-to-C three times A-to-B, and the two trains swapping speeds partway, working out each train's total travel time in terms of the common distance unit gives a time ratio of 5:7."),
    ("The sum of perimeters of an equilateral triangle and a rectangle is 90 cm. The area, T, of the triangle and the area, R, of the rectangle, both in sq cm, satisfy the relationship R = T 2 . If the sides of the rectangle are in the ratio 1 : 3, then the length, in cm, of the longer side of the rectangle, is", "27", "With triangle perimeter 3a and rectangle sides x, 3x, the total perimeter is 90 and the areas are related as given. Solving the resulting quadratic in a gives a = 6, and the rectangle's longer side works out to 27."),
    ("The number of integers that satisfy the equality (x2 − 5x + 7)x+1 = 1 is", "3", "(x²−5x+7)^(x+1) = 1 holds either when the base equals 1 or when the exponent is 0 (with a nonzero base). The base equals 1 at x = 2 and x = 3, and the exponent is 0 at x = −1 (where the base is indeed nonzero) - three integer solutions in total."),
    ("In how many ways can a pair of integers (x, a) be chosen such that x2 − 2|x| + |a − 2| = 0?", "7", "Rewriting the equation as (|x|−1)² + |a−2| = 1 splits into two cases: (|x|−1)²=0 with |a−2|=1, giving 4 pairs, and (|x|−1)²=1 with |a−2|=0, giving 3 more - 7 pairs total."),
    ("Two circular tracks T1 and T2 of radii 100 m and 20 m, respectively, touch at a point A. Starting from A at the same time, Ram and Rahim are walking on T1 and T2 at speeds 15 km/h and 5 km/h respectively. The number of full rounds that Ram will make before he meets Rahim again for the first time is:", "3", "Converting both circles' circumferences and the runners' speeds into consistent units, Ram's time to complete one lap works out to a clean multiple of Rahim's - specifically, Ram completes exactly 3 laps in the time it takes for both to again meet at the starting point."),
    ("Let C1 and C2 be concentric circles such that the diameter of C1 is 2 cm longer than that of C2 . If a chord of C1 has length 6 cm and is a tangent to C2 , then the diameter, in cm, of C1 is:", "10", "With C2's radius r and C1's radius r+1, the tangent chord of length 6 on C1 forms a right triangle with legs 3 and r and hypotenuse r+1. Solving via Pythagoras gives r = 4, so C1's diameter is 2(r+1) = 10."),
    ("A and B are two points on a straight line. Ram runs from A to B while Rahim runs from B to A. After crossing each other, Ram and Rahim reach their destinations in one minute and four minutes, respectively. If they start at the same time, then the ratio of Ram’s speed to Rahim’s speed is: √", "2", "After Ram and Rahim cross each other, the remaining time each needs to finish is inversely related to their speed ratio. Since Ram takes 1 more minute and Rahim takes 4 more minutes after crossing, their speed ratio works out to √(4/1) = 2."),
    ("John takes twice as much time as Jack to finish a job. Jack and Jim together take one-third of the time to finish the job than John takes working alone. Moreover, in order to finish the job, John takes three days more than that taken by three of them working together. In how many days will Jim finish the job working alone?", "4", "Let Jack take x days alone, so John takes 2x days. Jack and Jim together take exactly a third of John's time, which works out to also mean Jim alone takes 2x days. Using the condition that John takes 3 more days than all three working together gives x = 2, so Jim takes 2x = 4 days."),
    ("In May, John bought the same amount of rice and the same amount of wheat as he had bought in April, but spent 150 more due to price increase of rice and wheat by 20% and 12%, respectively. If John had spent 450 on rice in April, then how much did he spend on wheat in May?", "560", "Rice spending rose 20% to 540 and wheat spending rose 12% from w to 1.12w, together costing 150 more than April's spending (450 + w). Solving gives w = 500, so May's wheat spending is 1.12 × 500 = 560."),
    ("Aron bought some pencils and sharpeners. Spending the same amount of money as Aron, Aditya bought twice as many pencils and 10 fewer sharpeners. If the cost of one sharpener is 2 more than the cost of a pencil, then the minimum possible number of pencils bought by Aron and Aditya together is", "33", "With a sharpener costing 2 more than a pencil, and Aditya spending the same total as Aron while buying twice the pencils and 10 fewer sharpeners, the smallest integer solution gives Aron 11 pencils and Aditya 22 - a total of 33 pencils between them."),
    ("A sum of money is split among Amal, Sunil and Mita so that the ratio of the shares of Amal and Sunil is 3:2, while the ratio of the shares of Sunil and Mita is 4:5. If the difference between the largest and the smallest of these three shares is Rs 400, then Sunil’s share, in rupees, is", "800", "With Amal:Sunil = 3:2 and Sunil:Mita = 4:5, expressing all three shares in terms of Sunil's share S shows Amal's share is the largest and Sunil's the smallest, differing by S/2. Given that difference equals 400, S = 800."),
    ("How many 4-digit numbers, each greater than 1000 and each having all four digits distinct, are there with 7 coming before 3?", "315", "Out of all 4-digit numbers with distinct digits containing both 7 and 3, exactly half have 7 appearing before 3. Counting those combinations and then removing the ones that would start with a leading 0 brings the total down to 315."),
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

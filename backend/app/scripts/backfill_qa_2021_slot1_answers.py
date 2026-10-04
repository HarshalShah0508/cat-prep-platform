"""Backfill correct_answer/explanation for CAT 2021 QA Slot 1, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are rewritten in plain language, not copied verbatim.

Run with:
    python -m app.scripts.backfill_qa_2021_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("If r is a constant such that |x2 − 4x − 13| = r has exactly three distinct real roots, then the value of r is (1) 17 (2) 15 (3) 21 (4) 18", "17", "f(x) = x²−4x−13 is a parabola with minimum value −17 at x=2. For |f(x)|=r to have exactly 3 roots, one branch must just touch the vertex (1 root) while the other gives 2 roots - which happens exactly when r = 17."),
    ("A basket of 2 apples, 4 oranges and 6 mangoes costs the same as a basket of 1 apple, 4 oranges and 8 mangoes, or a basket of 8 oranges and 7 mangoes. Then the number of mangoes in a basket of mangoes that has the same cost as the other baskets is (1) 13 (2) 10\n\n(3) 11 (4) 12", "13", "Comparing the three equal-cost baskets pairwise gives a = 2m and o = 3m/4 (in terms of mango cost m). Plugging these into any basket's cost shows it equals 13m, so a basket of just mangoes needs 13 mangoes."),
    ("Identical chocolate pieces are sold in boxes of two sizes, small and large. The large box is sold for twice the price of the small box. If the selling price per gram of chocolate in the large box is 12% less than that in the small box, then the percentage by which the weight of chocolate in the large box exceeds that in the small box is nearest to (1) 124 (2) 135 (3) 144 (4) 127", "127", "Let the small box have price-per-gram x/w. The large box's price-per-gram is 12% less, which works out to a weight increase of about 127% over the small box's weight for the same doubled price."),
    ("How many three-digit numbers are greater than 100 and increase by 198 when the three digits are arranged in the reverse order?", "70", "If the number is 100a+10b+c and its reverse is 100c+10b+a, the 198 increase condition simplifies to c−a=2. Counting valid digits (a from 1-7, b from 0-9, c=a+2) gives 7×10 = 70 numbers."),
    ("Two trains cross each other in 14 seconds when running in opposite directions along parallel tracks. The faster train is 160 m long and crosses a lamp post in 12 seconds. If the speed of the other train is 6 km/h less than the faster one, its length (in meters) is:\n\n(1) 190\n\n(2) 184\n\n(3) 180\n\n(4) 192", "190", "The faster train's speed comes from its length and time to pass a lamp post, and the slower train's speed from the given speed difference. Combining lengths and relative speed for the 14-second crossing gives the slower train's length as 190 m."),
    ("Suppose hospital A admitted 21 less Covid infected patients than hospital B, and all eventually recovered. The sum of recovery days for patients in hospitals A and B were 200 and 152, respectively. If the average recovery days for patients admitted in hospital A was 3 more than the average in hospital B, then the number admitted in hospital A was", "35", "Let hospital B have x patients (so A has x−21). Setting up the given relation between average recovery days and solving the resulting quadratic gives x = 56, so hospital A admitted 56−21 = 35 patients."),
    ("Onion is sold for 5 consecutive months at the rate of |10, 20, 25, 25, and 50 per kg, respectively. A family spends a fixed amount of money on onion for each of the first three months, and then spends half that amount on onion for each of the next two months. The average expense for onion, in rupees per kg, for the family over these 5 months is closest to (1) 26\n\n(2) 20 (3) 16 (4) 18", "18", "Assuming a fixed amount spent each month, the quantity bought varies with price; averaging the total money spent over the total quantity bought across all 5 months gives roughly ₹18 per kg."),
    ("If the area of a regular hexagon is equal to the area of an equilateral triangle of side 12 cm, then the length, in cm, of each side of the hexagon is √ (1) 6 6 √ (2) 2 6 √ (3)  6 √ (4) 4 6 √", "2√6", "Equating the hexagon's area formula to the triangle's area (36√3, from a 12 cm side) and solving for the hexagon's side length gives a = 2√6 cm."),
    ("A circle of diameter 8 inches is inscribed in a triangle ABC where ∠ABC = 90◦ . If BC = 10 inches then the area of the triangle in square inches is", "120", "For a right triangle with the circle's radius (4 in) and hypotenuse BC=10, using Area = r × semi-perimeter directly (rather than solving for the legs individually) gives the triangle's area as 120 sq in."),
    ("The number of integers n that satisfy the inequalities |n − 60| < |n − 100| < |n − 20| is (1) 18 (2) 20 (3) 19 (4) 21", "19", "Breaking the number line into ranges around 20, 60, and 100 and checking each against |n−60|<|n−100|<|n−20|, only 60<n<80 satisfies both inequalities - that's 19 integers."),
    ("The amount Neeta and Geeta together earn in a day equals what Sita alone earns in 6 days. The amount Sita and Neeta together earn in a day equals what Geeta alone earns in 2 days. The ratio of the daily earnings of the one who earns the most to that of the one who earns the least is\n\n(1) 11 : 7 (2) 11 : 3 (3) 7 : 3 (4) 3 : 2", "11 : 3", "From N+G=6S and S+N=2G, solving gives G=7S/3 and N=11S/3, making Neeta the highest earner and Sita the lowest - a ratio of 11:3."),
    ("The natural numbers are divided into groups as (1), (2, 3, 4), (5, 6, 7, 8, 9), . . . .. and so on. Then, the sum of the numbers in the 15th group is equal to\n\n(1) 6119 (2) 4941 (3) 6090 (4) 7471", "6119", "Each group n has 2n−1 numbers, so the first 14 groups together hold 14²=196 numbers, meaning group 15 starts at 197 and runs for 29 numbers (197 to 225). Summing that range gives 6119."),
    ("Anil invests some money at a fixed rate of interest, compounded annually. If the interests accrued during the second and third year are 806.25 and 866.72 respectively, the interest accrued, in INR, during the fourth year is nearest to:\n\n(1) 934.65 (2) 929.48 (3) 926.84 (4) 931.72", "931.72", "Dividing the 3rd-year interest by the 2nd-year interest isolates the rate as 7.5%; working back to find the principal (₹10,000) and applying the rate for year 4 gives an interest of ₹931.72."),
    ("Anu, Vinu and Manu can complete a work alone in 15 days, 12 days and 20 days, respectively. Vinu works every day. Anu works only on alternate days starting from the first day while Manu works only on alternate days starting from the second day. Then, the number of days needed to complete the work is: (1) 6 (2) 5 (3) 8 (4) 7", "7", "With Anu, Vinu, and Manu working at 4, 5, and 3 units/day (out of 60 total), and Anu/Manu alternating days while Vinu works daily, each pair of days nets 9+8=17 units. The 60 units of work finish partway through day 7."),
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

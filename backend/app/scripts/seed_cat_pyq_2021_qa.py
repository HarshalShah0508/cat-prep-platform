"""Seed real CAT 2021 QA questions, generated from the official
solutions PDFs via pdftotext + pyq_qa_parser.py (automated text-layer
extraction, not LLM transcription).

Roughly half of CAT QA questions embed their math as a rendered image pdftotext can't recover (shows up as a run of blank space where an 
equation used to be, or an empty option) - those are intentionally omitted here, not fabricated. See stderr from the generation step for 
which question numbers were skipped per slot.

`correct_answer`/`explanation` are intentionally left blank for now - the answer key
is loaded separately once transcribed from the solutions PDFs.

Run with:
    python -m app.scripts.seed_cat_pyq_2021_qa
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021


def q(slot, qtype, text, options=None):
    return {
        "section": "QA",
        "question_type": qtype,
        "topic": "Quantitative Aptitude",
        "difficulty": "hard",
        "source": "pyq",
        "source_year": SOURCE_YEAR,
        "source_slot": slot,
        "group_id": None,
        "passage_text": None,
        "question_text": text,
        "options": options,
    }


QUESTIONS = []

# ============================================================ SLOT 1 ====
_slot = "slot1"
QUESTIONS += [
    q(_slot, "TITA", "If r is a constant such that |x2 − 4x − 13| = r has exactly three distinct real roots, then the value of r is (1) 17 (2) 15 (3) 21 (4) 18", options=None),
    q(_slot, "TITA", "A basket of 2 apples, 4 oranges and 6 mangoes costs the same as a basket of 1 apple, 4 oranges and 8 mangoes, or a basket of 8 oranges and 7 mangoes. Then the number of mangoes in a basket of mangoes that has the same cost as the other baskets is (1) 13 (2) 10\n\n(3) 11 (4) 12", options=None),
    q(_slot, "TITA", "Identical chocolate pieces are sold in boxes of two sizes, small and large. The large box is sold for twice the price of the small box. If the selling price per gram of chocolate in the large box is 12% less than that in the small box, then the percentage by which the weight of chocolate in the large box exceeds that in the small box is nearest to (1) 124 (2) 135 (3) 144 (4) 127", options=None),
    q(_slot, "TITA", "How many three-digit numbers are greater than 100 and increase by 198 when the three digits are arranged in the reverse order?", options=None),
    q(_slot, "TITA", "Two trains cross each other in 14 seconds when running in opposite directions along parallel tracks. The faster train is 160 m long and crosses a lamp post in 12 seconds. If the speed of the other train is 6 km/h less than the faster one, its length (in meters) is:\n\n(1) 190\n\n(2) 184\n\n(3) 180\n\n(4) 192", options=None),
    q(_slot, "TITA", "Suppose hospital A admitted 21 less Covid infected patients than hospital B, and all eventually recovered. The sum of recovery days for patients in hospitals A and B were 200 and 152, respectively. If the average recovery days for patients admitted in hospital A was 3 more than the average in hospital B, then the number admitted in hospital A was", options=None),
    q(_slot, "TITA", "Onion is sold for 5 consecutive months at the rate of |10, 20, 25, 25, and 50 per kg, respectively. A family spends a fixed amount of money on onion for each of the first three months, and then spends half that amount on onion for each of the next two months. The average expense for onion, in rupees per kg, for the family over these 5 months is closest to (1) 26\n\n(2) 20 (3) 16 (4) 18", options=None),
    q(_slot, "TITA", "If the area of a regular hexagon is equal to the area of an equilateral triangle of side 12 cm, then the length, in cm, of each side of the hexagon is √ (1) 6 6 √ (2) 2 6 √ (3)  6 √ (4) 4 6 √", options=None),
    q(_slot, "TITA", "A circle of diameter 8 inches is inscribed in a triangle ABC where ∠ABC = 90◦ . If BC = 10 inches then the area of the triangle in square inches is", options=None),
    q(_slot, "TITA", "The number of integers n that satisfy the inequalities |n − 60| < |n − 100| < |n − 20| is (1) 18 (2) 20 (3) 19 (4) 21", options=None),
    q(_slot, "TITA", "The amount Neeta and Geeta together earn in a day equals what Sita alone earns in 6 days. The amount Sita and Neeta together earn in a day equals what Geeta alone earns in 2 days. The ratio of the daily earnings of the one who earns the most to that of the one who earns the least is\n\n(1) 11 : 7 (2) 11 : 3 (3) 7 : 3 (4) 3 : 2", options=None),
    q(_slot, "TITA", "The natural numbers are divided into groups as (1), (2, 3, 4), (5, 6, 7, 8, 9), . . . .. and so on. Then, the sum of the numbers in the 15th group is equal to\n\n(1) 6119 (2) 4941 (3) 6090 (4) 7471", options=None),
    q(_slot, "TITA", "Anil invests some money at a fixed rate of interest, compounded annually. If the interests accrued during the second and third year are 806.25 and 866.72 respectively, the interest accrued, in INR, during the fourth year is nearest to:\n\n(1) 934.65 (2) 929.48 (3) 926.84 (4) 931.72", options=None),
    q(_slot, "TITA", "Anu, Vinu and Manu can complete a work alone in 15 days, 12 days and 20 days, respectively. Vinu works every day. Anu works only on alternate days starting from the first day while Manu works only on alternate days starting from the second day. Then, the number of days needed to complete the work is: (1) 6 (2) 5 (3) 8 (4) 7", options=None),
]

# ============================================================ SLOT 2 ====
_slot = "slot2"
QUESTIONS += [
    q(_slot, "TITA", "For all possible integers n satisfying 2.25 ≤ 2 + 2n + 2 ≤ 202, then the number of integer values of 3 + 3n + 1 is:", options=None),
    q(_slot, "MCQ", "Three positive integers x, y, z are in arithmetic progression. If y − x > 2 and xyz = 5(x + y + z), then z − x equals:", options=["8", "12", "14", "10"]),
    q(_slot, "TITA", "For a 4-digit number, the sum of its digits in the thousands, hundreds, and tens places is 14, the sum of its digits in the hundreds, tens, and units places is 15, and the tens place digit is 4 more than the units place digit. Then the highest possible 4-digit number satisfying the above conditions is:", options=None),
    q(_slot, "MCQ", "Raj invested 10000 in a fund. At the end of the first year, he incurred a loss, but his balance was more than 5000. This balance, when invested for another year, grew and the percentage of growth in the second year was five times the percentage of loss in the first year. If the gain of Raj from the initial investment over the two-year period is 35%, then the per- centage of loss in the first year is:", options=["5", "15", "17", "10"]),
    q(_slot, "TITA", "The number of ways of distributing 15 identical balloons, 6 identical pencils, and 3 identical erasers among 3 children, such that each child gets at least four balloons and one pencil, is:", options=None),
    q(_slot, "MCQ", "Two trains A and B were moving in opposite directions, their speeds being in the ratio 5:3. The front end of A crossed the rear end of B 46 seconds after the front ends of the trains had crossed each other. It took another 69 seconds for the rear ends of the trains to cross each other. The ratio of the length of train A to that of train B is:", options=["3:2", "5:3", "2:3", "2:1"]),
    q(_slot, "TITA", "From a container filled with milk, 9 litres of milk are drawn and replaced with water. Next, from the same container, 9 litres are drawn and again replaced with water. If the vol- umes of milk and water in the container are now in the ratio of 16:9, then the capacity of the container, in litres, is:", options=None),
    q(_slot, "TITA", "If log2 (3 + log4 (4 + log(x − 1))) − 2 = 0, then 4x equals:", options=None),
    q(_slot, "MCQ", "The sides AB and CD of a trapezium ABCD are parallel, with AB being the smaller side. P is the midpoint of CD and ABPD is a parallelogram. If the difference between the areas of the parallelogram ABPD and the triangle BPC is 10 sq cm, then the area, in sq cm, of the trapezium ABCD is:", options=["30", "40", "25", "20"]),
    q(_slot, "MCQ", "For a real number x, the condition |3x − 201 + 13x − 40| = 20 necessarily holds. Then, the value of x lies in the range:", options=["10 < x < 15", "9 < x < 14", "7 < x < 12", "6 < x < 11"]),
    q(_slot, "MCQ", "Anil can paint a house in 60 days while Bimal can paint it in 84 days. Anil starts painting and after 10 days, Bimal and Charu join him. Together, they complete the painting in 14 more days. If they are paid a total of 21000 for the job, then the share of Charu, in INR, proportionate to the work done by him, is:", options=["9000", "9200", "9100", "9150"]),
    q(_slot, "TITA", "A box has 450 balls, each either white or black, there being as many metallic white balls as metallic black balls. If 40% of the white balls and 50% of the black balls are metallic, then the number of non-metallic balls in the box is:", options=None),
    q(_slot, "TITA", "In a football tournament, a player has played a certain number of matches and 10 more matches are to be played. If he scores a total of one goal over the next 10 matches, his overall average will be 0.15 goals per match. On the other hand, if he scores a total of two goals over the next 10 matches, his overall average will be 0.2 goals per match. The number of matches he has played is:", options=None),
    q(_slot, "MCQ", "A person buys tea of three different qualities at 800, 500, and 300 per kg, respectively, and the amounts bought are in the proportion 2:3:5. She mixes all the tea and sells one-sixth\n\nof the mixture at 700 per kg. The price, in INR per kg, at which she should sell the remaining tea, to make an overall profit of 50%, is:", options=["653", "688", "692", "675"]),
    q(_slot, "MCQ", "Consider the pair of equations: x2 − xy − x = 22 and y 2 − xy + y = 34. If x > y , then x − y equals:", options=["6", "4", "7", "8"]),
    q(_slot, "TITA", "Let D and E be points on sides AB and AC, respectively, of a triangle ABC, such that AD : BD = 2 : 1 and AE : CE = 2 : 3. If the area of the triangle ADE is 8 sq cm, then the area of the triangle ABC, in sq cm, is:", options=None),
    q(_slot, "MCQ", "Anil, Bobby, and Chintu jointly invest in a business and agree to share the overall profit in proportion to their investments. Anil’s share of investment is 70%. His share of profit decreases by 420 if the overall profit goes down from 18% to 15%. Chintu’s share of profit increases by 80 if the overall profit goes up from 15% to 17%. The amount, in INR, invested by Bobby is:", options=["2000", "2400", "2200", "1800"]),
    q(_slot, "MCQ", "Two pipes A and B are attached to an empty water tank. Pipe A fills the tank while pipe B drains it. If pipe A is opened at 2 pm and pipe B is opened at 3 pm, then the tank becomes full at 10 pm. Instead, if pipe A is opened at 2 pm and pipe B is opened at 4 pm, then the tank becomes full at 6 pm. If pipe B is not opened at all, then the time, in minutes, taken to fill the tank is:", options=["144", "140", "264", "120"]),
]

# ============================================================ SLOT 3 ====
_slot = "slot3"
QUESTIONS += [
    q(_slot, "TITA", "Bank A offers 6% interest rate per annum compounded half yearly. Bank B and Bank C offer simple interest but the annual interest rate offered by Bank C is twice that offered by Bank B. Raju invests a certain amount in Bank B for a certain period and Rupa invests 10,000 in Bank C for twice that period. The interest that would accrue to Raju during that period is equal to the interest that would have accrued had he invested the same amount in Bank A for one year. The interest accrued, in INR, to Raju is: (1) 1.1436 (2) 2.2436 (3) 3.3436 (4) 4.2346", options=None),
    q(_slot, "TITA", "If f (x) = x2 − 7x and g(x) = x + 3, then the minimum value of f (g(x)) − 3x is: (1) -15 (2) -20 (3) -16 (4) -12", options=None),
    q(_slot, "TITA", "In a tournament, a team has played 40 matches so far and won 30% of them. If they win 60% of the remaining matches, their overall win percentage will be 50%. Suppose they win 90% of the remaining matches, then the total number of matches won by the team in the tournament will be: (1) 86 (2) 78 (3) 80 (4) 84", options=None),
    q(_slot, "TITA", "If 3x + 2|y| + y = 7 and x + |x| + 3y = 1, then x + 2y is: (1) −4\n\n(2) 38 (3) 1 (4) None of these", options=None),
    q(_slot, "TITA", "A shop owner bought a total of 64 shirts from a wholesale market that came in two sizes, small and large. The price of a small shirt was INR 50 less than that of a large shirt. She paid a total of INR 5000 for the large shirts, and a total of INR 1800 for the small shirts. Then, the price of a large shirt and a small shirt together, in INR, is: (1) 200 (2) 175\n\n(3) 225 (4) 150", options=None),
    q(_slot, "TITA", "Mira and Amal walk along a circular track, starting from the same point at the same time. If they walk in the same direction, then in 45 minutes, Amal completes exactly 3 more rounds than Mira. If they walk in opposite directions, then they meet for the first time exactly after 3 minutes. The number of rounds Mira walks in one hour is: (1) 8 (2) 6 (3) 9 (4) 10", options=None),
    q(_slot, "TITA", "If a certain weight of an alloy of silver and copper is mixed with 3 kg of pure silver, the resulting alloy will have 90% silver by weight. If the same weight of the initial alloy is mixed with 2 kg of another alloy which has 90% silver by weight, the resulting alloy will have 84% silver by weight. Then, the weight of the initial alloy, in kg, is (1) 1.3 (2) 5 (3) 3.3 (4) 2.5", options=None),
    q(_slot, "TITA", "The number of distinct pairs of integers (m, n) satisfying |1 + mn| < |m + n| < 5 is", options=None),
    q(_slot, "TITA", "One day, Rahul started a work at 9 AM and Gautam joined him two hours later. They then worked together and completed the work at 5 PM the same day. If both had started at 9 AM and worked together, the work would have been completed 30 minutes earlier. Working alone, the time Rahul would have taken, in hours, to complete the work is (1) 12 (2) 12.5 (3) 11.5 (4) 10", options=None),
    q(_slot, "TITA", "Anil can paint a house in 12 days while Barun can paint it in 16 days. Anil, Barun, and Chandu undertake to paint the house for INR 24000, and the three of them together complete the painting in 6 days. If Chandu is paid in proportion to the work done by him, then the amount in INR received by him is (1) 3000 (2) 4000 (3) 3600 (4) 3200", options=None),
    q(_slot, "TITA", "The cost of fencing a rectangular plot is 200 per ft along one side, and 100 per ft along the three other sides. If the area of the rectangular plot is 60000 sq. ft, then the lowest possible cost of fencing all four sides, in INR, is (1) 120000 (2) 100000 (3) 160000 (4) 90000", options=None),
    q(_slot, "TITA", "A four-digit number is formed by using only the digits 1, 2, and 3 such that both 2 and 3 appear at least once. The number of all such four-digit numbers is (1) 50 (2) 54 (3) 60 (4) 48", options=None),
    q(_slot, "TITA", "In a triangle ABC , ∠BCA = 50◦ . D and E are points on AB and AC , respectively, such that AD = DE . If F is a point on BC such that BD = DF , then ∠F DE , in degrees, is equal to (1) 72 (2) 100 (3) 80 (4) 90", options=None),
    q(_slot, "TITA", "Consider a sequence of real numbers x1 , x2 , x3 , . . . such that xn+1 = xn + n − 1 for all n ≥ 1. If x1 = −1, then x100 is equal to (1) 4850 (2) 4950 (3) 4849 (4) 4949", options=None),
    q(_slot, "TITA", "A tea shop offers tea in cups of three different sizes. The product of the prices, in INR, of three different sizes is equal to 800. The prices of the smallest size and the medium size are in the ratio 2:5. If the shop owner decides to increase the prices of the smallest and the medium ones by INR 6, keeping the price of the largest size unchanged, the product then changes to 3200. The sum of the original prices of three different sizes, in INR, is (1) 30 (2) 32 (3) 36 (4) 34", options=None),
    q(_slot, "TITA", "A park is shaped like a rhombus and has area 96 sq m. If 40 m of fencing is needed to enclose the park, the cost, in INR, of laying electric wires along its two diagonals, at the rate of 125 per m, is", options=None),
    q(_slot, "TITA", "One part of a hostel’s monthly expenses is fixed, and the other part is proportional to the number of its boarders. The hostel collects 1600 per month from each boarder. When the number of boarders is 50, the profit of the hostel is 200 per boarder, and\n\nwhen the number of boarders is 75, the profit of the hostel is 250 per boarder. When the number of boarders is 80, the total profit of the hostel, in INR, will be (1) 20800 (2) 20500 (3) 20200 (4) 20000", options=None),
    q(_slot, "TITA", "The total of male and female populations in a city increased by 25% from 1970 to 1980. During the same period, the male population increased by 40%, while the female population increased by 20%. From 1980 to 1990, the female population increased by 25%. In 1990, if the female population is twice the male population, then the percentage increase in the total population from 1970 to 1990 is (1) 68.75 (2) 68.25 (3) 69.25 (4) 67.75", options=None),
    q(_slot, "TITA", "The arithmetic mean of scores of 25 students in an examination is 50. Five of these students top the examination with the same score. If the scores of the other students are distinct integers with the lowest being 30, then the maximum possible score of the toppers is (1) 78 (2) 80 (3) 77 (4) 76", options=None),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = (
            db.query(CatQuestion)
            .filter(CatQuestion.source_year == SOURCE_YEAR, CatQuestion.section == "QA")
            .count()
        )
        if existing > 0:
            print(f"CAT {SOURCE_YEAR} QA PYQs already seeded ({existing} rows); skipping.")
            return

        for item in QUESTIONS:
            db.add(
                CatQuestion(
                    section=item["section"],
                    question_type=item["question_type"],
                    topic=item["topic"],
                    difficulty=item["difficulty"],
                    source=item["source"],
                    source_year=item["source_year"],
                    source_slot=item["source_slot"],
                    group_id=item["group_id"],
                    passage_text=item["passage_text"],
                    question_text=item["question_text"],
                    options=item["options"],
                    correct_answer=None,
                    explanation=None,
                    is_active=True,
                )
            )
        db.commit()
        print(f"Seeded {len(QUESTIONS)} CAT {SOURCE_YEAR} QA PYQ questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

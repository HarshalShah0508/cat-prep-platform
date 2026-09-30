"""Seed real CAT 2025 QA (Quantitative Aptitude) questions, all 3 slots,
retyped from the official question papers in pyq-source/2025/. All QA
questions are standalone (no shared passage), unlike VARC/DILR.

`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

Source note: the plain question-paper PDFs (QUANT_SLOTn_CAT_2025.pdf) were
used as the primary source since they're much shorter than the combined
solutions PDFs. A handful of questions render fractions/square-roots/
exponents as images that pdftotext can't extract as text (garbled or
missing options) - for those specific questions, the matching combined
SOLUTIONS PDF was read visually (page-by-page) to get the clean option
text; the plain paper's own printed question numbers/stems were otherwise
used as-is. Slot 2's plain paper mislabels its questions 2-23 (a genuine
off-by-one printing error, confirmed against the solutions PDF's own
correct 1-22 numbering) - handled here by just using positional order.

Run with:
    python -m app.scripts.seed_cat_pyq_2025_qa
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025


def q(slot, topic, qtype, text, options=None):
    return {
        "section": "QA",
        "question_type": qtype,
        "topic": topic,
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
    q(_slot, "Simple/Compound Interest & Mixtures", "TITA",
      "Kamala divided her investment of Rs 100000 between stocks, bonds, and gold. Her "
      "investment in bonds was 25% of her investment in gold. With annual returns of 10%, "
      "6%, 8% on stocks, bonds, and gold, respectively, she gained a total amount of Rs 8200 "
      "in one year. The amount, in rupees, that she gained from the bonds, was:"),
    q(_slot, "Algebra - Linear Equations", "MCQ",
      "If a - 6b + 6c = 4 and 6a + 3b - 3c = 50, where a, b and c are real numbers, the value "
      "of 2a + 3b - 3c is:", ["18", "20", "15", "14"]),
    q(_slot, "Coordinate Geometry", "MCQ",
      "The (x, y) coordinates of vertices P, Q and R of a parallelogram PQRS are (-3, -2), "
      "(1, -5) and (9, 1), respectively. If the diagonal SQ intersects the x-axis at (a, 0), "
      "then the value of a is:", ["29/9", "27/9", "29/7", "9/29"]),
    q(_slot, "Simple & Compound Interest", "MCQ",
      "At a certain simple rate of interest, a given sum amounts to Rs 13920 in 3 years, and "
      "to Rs 18960 in 6 years and 6 months. If the same given sum had been invested for 2 "
      "years at the same rate as before but with interest compounded every 6 months, then "
      "the total interest earned, in rupees, would have been nearest to:",
      ["3096", "3221", "3180", "3150"]),
    q(_slot, "Number Systems - Greatest Integer Function", "MCQ",
      "Let 3 ≤ x ≤ 6 and [x²] = [x]², where [x] is the greatest integer not "
      "exceeding x. If set S represents all feasible values of x, then which of the "
      "following is a possible subset of S?",
      ["(3, √10) ∪ [5, √26) ∪ {6}", "(4, √10) ∪ [5, √27) ∪ {6}",
       "[3, √10] ∪ [5, √26]", "[3, √10] ∪ [4, √17] ∪ {6}"]),
    q(_slot, "Quadratic Equations", "TITA",
      "The number of non-negative integer values of k for which the quadratic equation "
      "x² - 5x + k = 0 has only integer roots, is:"),
    q(_slot, "Profit, Loss & Discount", "TITA",
      "A shopkeeper offers a discount of 22% on the marked price of each chair, and gives 13 "
      "chairs to a customer for the discounted price of 12 chairs to earn a profit of 26% on "
      "the transaction. If the cost price of each chair is Rs 100, then the marked price, in "
      "rupees, of each chair is:"),
    q(_slot, "Permutation and Combination", "MCQ",
      "A cafeteria offers 5 types of sandwiches. Moreover, for each type of sandwich, a "
      "customer can choose one of 4 breads and opt for either small or large sized "
      "sandwich. Optionally, the customer may also add up to 2 out of 6 available sauces. "
      "The number of different ways in which an order can be placed for a sandwich, is:",
      ["600", "840", "880", "800"]),
    q(_slot, "Logarithms", "MCQ",
      "The number of distinct integers n for which log(1/4)(n² - 7n + 11) > 0 is:",
      ["1", "2", "20", "infinite"]),
    q(_slot, "Exponents & Inequalities", "MCQ",
      "For any natural number k, let ak = 3^k. The smallest natural number m for which "
      "(a1)^1 × (a2)^2 × ··· × (a20)^20 < a21 × a22 × "
      "··· × a(20+m) is:", ["58", "59", "57", "56"]),
    q(_slot, "Inequalities - Integer Solutions", "TITA",
      "The number of distinct pairs of integers (x, y) satisfying the inequalities x > y ≥ 3 "
      "and x + y < 14 is:"),
    q(_slot, "Geometry - Circles", "MCQ",
      "In a circle with center C and radius 6√2 cm, PQ and SR are two parallel chords "
      "separated by one of the diameters. If ∠PQC = 45°, and the ratio of the "
      "perpendicular distance of PQ and SR from C is 3 : 2, then the area, in sq. cm, of the "
      "quadrilateral PQRS is:",
      ["20(3 + √14)", "20(3√2 + √7)", "4(3 + √14)", "4(3√2 + √7)"]),
    q(_slot, "Ratios & Portfolio", "TITA",
      "Stocks A, B and C are priced at rupees 120, 90 and 150 per share, respectively. A "
      "trader holds a portfolio consisting of 10 shares of stock A, and 20 shares of stocks "
      "B and C put together. If the total value of her portfolio is rupees 3300, then the "
      "number of shares of stock B that she holds is:"),
    q(_slot, "Functions - Maxima/Minima", "MCQ",
      "A value of c for which the minimum value of f(x) = x² - 4cx + 8c is greater than "
      "the maximum value of g(x) = -x² + 3cx - 2c, is:", ["1/2", "-1/2", "-2", "2"]),
    q(_slot, "Time Speed Distance - Arithmetic Progression", "MCQ",
      "Shruti travels a distance of 224 km in four parts for a total travel time of 3 hours. "
      "Her speeds in these four parts follow an arithmetic progression, and the "
      "corresponding time taken to cover these four parts follow another arithmetic "
      "progression. If she travels at a speed of 960 meters per minute for 30 minutes to "
      "cover the first part, then the distance, in meters, she travels in the fourth part is:",
      ["72000", "80000", "86400", "90000"]),
    q(_slot, "Number Systems - Factors", "TITA",
      "In a 3-digit number N, the digits are non-zero and distinct such that none of the "
      "digits is a perfect square, and only one of the digits is a prime number. Then, the "
      "number of factors of the minimum possible value of N is:"),
    q(_slot, "Ratio & Proportion", "MCQ",
      "The ratio of the number of students in the morning shift and afternoon shift of a "
      "school was 13 : 9. After 21 students moved from the morning shift to the afternoon "
      "shift, this ratio became 19 : 14. Next, some new students joined the morning and "
      "afternoon shifts in the ratio 3 : 8 and then the ratio of the number of students in "
      "the morning shift and the afternoon shift became 5 : 4. The number of new students "
      "who joined is:", ["88", "12", "11", "99"]),
    q(_slot, "Geometry - Rhombus", "TITA",
      "If the length of a side of a rhombus is 36 cm and the area of the rhombus is 396 sq. "
      "cm, then the absolute value of the difference between the lengths, in cm, of the "
      "diagonals of the rhombus is:"),
    q(_slot, "Number Series", "MCQ",
      "In the set of consecutive odd numbers {1, 3, 5, . . . , 57}, there is a number k such "
      "that the sum of all the elements less than k is equal to the sum of all the elements "
      "greater than k. Then, k equals?", ["37", "41", "39", "43"]),
    q(_slot, "Mixtures and Alligations", "MCQ",
      "A container holds 200 litres of a solution of acid and water, having 30% acid by "
      "volume. Atul replaces 20% of this solution with water, then replaces 10% of the "
      "resulting solution with acid, and finally replaces 15% of the solution thus obtained, "
      "with water. The percentage of acid by volume in the final solution obtained after "
      "these three replacements, is nearest to?", ["25", "27", "29", "23"]),
    q(_slot, "Time and Work", "MCQ",
      "Arun, Varun and Tarun, if working alone, can complete a task in 24, 21, and 15 days, "
      "respectively. They charge Rs 2160, Rs 2400, and Rs 2160 per day, respectively, even "
      "if they are employed for a partial day. On any given day, any of the workers may or "
      "may not be employed to work. If the task needs to be completed in 10 days or less, "
      "then the minimum possible amount, in rupees, required to be paid for the entire task "
      "is?", ["34400", "38400", "47040", "38880"]),
    q(_slot, "Percentages", "TITA",
      "In a class, there were more than 10 boys and a certain number of girls. After 40% of "
      "the girls and 60% of the boys left the class, the remaining number of girls was 8 "
      "more than the remaining number of boys. Then, the minimum possible number of "
      "students initially in the class was?"),
]

# ============================================================ SLOT 2 ====
_slot = "slot2"
QUESTIONS += [
    q(_slot, "Geometric Progression", "MCQ",
      "Let an be the nth term of a decreasing infinite geometric progression. If "
      "a1 + a2 + a3 = 52 and a1a2 + a2a3 + a3a1 = 624, then the sum of this geometric "
      "progression is:", ["57", "63", "54", "60"]),
    q(_slot, "Geometry - Circles & Tangents", "TITA",
      "Two tangents drawn from a point P touch a circle with center O at points Q and R. "
      "Points A and B lie on PQ and PR, respectively, such that AB is also a tangent to the "
      "same circle. If ∠AOB = 50°, then ∠APB, in degrees, equals:"),
    q(_slot, "Geometry - Hexagon", "MCQ",
      "Let ABCDEF be a regular hexagon and P and Q be the midpoints of AB and CD, "
      "respectively. Then, the ratio of the areas of trapezium PBCQ and hexagon ABCDEF is:",
      ["6 : 19", "5 : 24", "6 : 25", "7 : 24"]),
    q(_slot, "Number Systems", "TITA",
      "Suppose a, b, c are three distinct natural numbers, such that 3ac = 8(a + b). Then, "
      "the smallest possible value of 3a + 2b + c is:"),
    q(_slot, "Ratio - Income & Expenditure", "MCQ",
      "The ratio of expenditures of Lakshmi and Meenakshi is 2 : 3, and the ratio of income "
      "of Lakshmi to expenditure of Meenakshi is 6 : 7. If excess of income over expenditure "
      "is saved by Lakshmi and Meenakshi, and the ratio of their savings is 4 : 9, then the "
      "ratio of their incomes is:", ["7 : 8", "3 : 5", "2 : 1", "5 : 6"]),
    q(_slot, "Logarithms", "MCQ",
      "If log64(x²) + log8(√y) + 3·log512(√(yz)) = 4, where x, y and z are "
      "positive real numbers, then the minimum possible value of (x + y + z) is:",
      ["24", "36", "96", "48"]),
    q(_slot, "Exponential Equations", "MCQ",
      "If 9^(x²+2x-3) - 4·3^(x²+2x-2) + 27 = 0, then the product of all possible "
      "values of x is:", ["2", "4", "10", "20"]),
    q(_slot, "Averages", "TITA",
      "The average number of copies of a book sold per day by a shopkeeper is 60 in the "
      "initial seven days and 63 in the initial eight days, after the book launch. On the "
      "ninth day, she sells 11 copies less than the eighth day, and the average number of "
      "copies sold per day from the second day to the ninth day becomes 66. The number of "
      "copies sold on the first day of the book launch is:"),
    q(_slot, "Compound Interest", "MCQ",
      "A loan of Rs 1000 is fully repaid by two installments of Rs 530 and Rs 594, paid at "
      "the end of the first and second year, respectively. If the interest is compounded "
      "annually, then the rate of interest, in percentage, is:", ["6%", "7%", "8%", "9%"]),
    q(_slot, "Inequalities - Modulus", "MCQ",
      "The set of all real values of x for which (x² - |x + 9| + x) > 0 is:",
      ["(-∞, -9) ∪ (3, ∞)", "(-∞, -3) ∪ (9, ∞)",
       "(-∞, -3) ∪ (3, ∞)", "(-9, -3) ∪ (3, 9)"]),
    q(_slot, "Quadratic Equations - Common Root", "MCQ",
      "The equations 3x² - 5x + p = 0 and 2x² - 2x + q = 0 have one common root. The "
      "sum of the other roots of these two equations is:",
      ["5/3 - p + q", "8/3 + p - q", "8/3 - p + (3/2)q", "p + q - 1"]),
    q(_slot, "Profit, Loss & Discount", "MCQ",
      "An item with a cost price of Rs. 1650 is sold at a certain discount on a fixed marked "
      "price to earn a profit of 20% on the cost price. If the discount was doubled, the "
      "profit would have been Rs. 110. The rate of discount, in percentage, at which the "
      "profit percentage would be equal to the rate of discount, is nearest to:",
      ["12", "13", "14", "15"]),
    q(_slot, "Ratio & Proportion", "MCQ",
      "A certain amount of money was divided among Pinu, Meena, Rinu, and Seema. Pinu "
      "received 20% of the total amount and Meena received 40% of the remaining amount. If "
      "Seema received 20% less than Pinu, the ratio of the amounts received by Pinu and "
      "Rinu is:", ["4 : 5", "5 : 8", "3 : 5", "2 : 3"]),
    q(_slot, "Functions - Domain", "MCQ",
      "Let f(x) = x/(2x - 1) and g(x) = x/(x - 1). Then, the domain of the function "
      "h(x) = f(g(x)) + g(f(x)) is all real numbers except:",
      ["1/2, 1, 3/2", "1/2, 1", "-1/2, 1/2, 1", "-1, 1/2, 1"]),
    q(_slot, "Number Systems - Divisors", "MCQ",
      "The number of divisors of (2^6 × 3^5 × 5^3 × 7^2), which are of the form "
      "(3r + 1), where r is a non-negative integer, is:", ["42", "36", "56", "24"]),
    q(_slot, "Number Systems - Digit Sum", "TITA",
      "The sum of digits of the number (625)^65 × (128)^36 is:"),
    q(_slot, "Time and Work", "TITA",
      "Ankita is twice as efficient as Bipin, while Bipin is twice as efficient as Chandan. "
      "All three of them start together on a job, and Bipin leaves the job after 20 days. If "
      "the job got completed in 60 days, the number of days needed by Chandan to complete "
      "the job alone, is:"),
    q(_slot, "Algebra", "MCQ",
      "If m and n are integers such that (m + 2n)(2m + n) = 27, then the maximum possible "
      "value of 2m - 3n is:", ["9", "13", "15", "17"]),
    q(_slot, "Geometry - Triangles", "MCQ",
      "In a △ABC, points D and E are on the sides BC and AC, respectively. BE and AD "
      "intersect at point T such that AD : AT = 4 : 3, and BE : BT = 5 : 4. Point F lies on "
      "AC such that DF is parallel to BE. Then, BD : CD is:",
      ["15 : 4", "11 : 4", "9 : 4", "7 : 4"]),
    q(_slot, "Mixtures and Alligations", "MCQ",
      "A mixture of coffee and cocoa, 16% of which is coffee, costs Rs 240 per kg. Another "
      "mixture of coffee and cocoa, of which 36% is coffee, costs Rs 320 per kg. If a new "
      "mixture of coffee and cocoa costs Rs 376 per kg, then the quantity, in kg, of coffee "
      "in 10 kg of this new mixture is:", ["2.5", "5", "4", "6"]),
    q(_slot, "Time Speed Distance - Boats & Streams", "TITA",
      "Rita and Sneha can row a boat at 5 km/h and 6 km/h in still water, respectively. In a "
      "river flowing with a constant velocity, Sneha takes 48 minutes more to row 14 km "
      "upstream than to row the same distance downstream. If Rita starts from a certain "
      "location in the river, and returns downstream to the same location, taking a total "
      "of 100 minutes, then the total distance, in km, Rita will cover is:"),
    q(_slot, "Algebra - Minimization", "TITA",
      "If a, b, c and d are integers such that their sum is 46, then the minimum possible "
      "value of (a - b)² + (a - c)² + (a - d)² is:"),
]

# ============================================================ SLOT 3 ====
_slot = "slot3"
QUESTIONS += [
    q(_slot, "Number Systems - Digits", "MCQ",
      "For a 4-digit number (greater than 1000), sum of the digits in the thousands, "
      "hundreds, and tens places is 15. Sum of the digits in the hundreds, tens, and units "
      "places is 16. Also, the digit in the tens place is 6 more than the digit in the units "
      "place. The difference between the largest and smallest possible value of the number "
      "is", ["40", "78", "811", "735"]),
    q(_slot, "Geometry - Trapezium & Incircle", "MCQ",
      "ABCD is a trapezium in which AB is parallel to DC, AD is perpendicular to AB, and "
      "AB = 3DC. If a circle inscribed in the trapezium touching all the sides has a radius "
      "of 3 cm, then the area, in sq. cm, of the trapezium is",
      ["54", "30√3", "48", "36√2"]),
    q(_slot, "Mixtures and Alligations", "TITA",
      "Vessels A and B contain 60 litres of alcohol and 60 litres of water, respectively. A "
      "certain volume is taken out from A and poured into B. After stirring, the same "
      "volume is taken out from B and poured into A. If the resultant ratio of alcohol and "
      "water in A is 15 : 4, then the volume, in litres, initially taken out from A is"),
    q(_slot, "Sets - Venn Diagrams", "MCQ",
      "In a class of 150 students, 75 students chose physics, 111 students chose "
      "mathematics and 40 students chose chemistry. All students chose at least one of the "
      "three subjects and at least one student chose all three subjects. The number of "
      "students who chose both physics and chemistry is equal to the number of students who "
      "chose both chemistry and mathematics, and this is half the number of students who "
      "chose both physics and mathematics. The maximum possible number of students who "
      "chose physics but not mathematics, is", ["30", "55", "35", "40"]),
    q(_slot, "Geometry - Triangles", "MCQ",
      "In △ABC, AB = AC = 12 cm and D is a point on side BC such that AD = 8 cm. If AD "
      "is extended to a point E such that ∠ACB = ∠AEB, then the length, in cm, of "
      "AE is", ["18", "16", "20", "14"]),
    q(_slot, "Algebra - Higher Powers", "MCQ",
      "If x² + 1/x² = 25 and x > 0, then the value of x⁷ + 1/x⁷ is",
      ["44859√3", "44853√3", "44850√3", "44856√3"]),
    q(_slot, "Time Speed Distance", "MCQ",
      "Rahul starts on his journey at 5 pm at a constant speed so that he reaches his "
      "destination at 11 pm the same day. However, on his way, he stops for 20 minutes, and "
      "after that, increases his speed by 3 km per hour to reach on time. If he had stopped "
      "for 10 minutes more, he would have had to increase his speed by 5 km per hour to "
      "reach on time. His initial speed, in km per hour, was", ["20", "15", "12", "18"]),
    q(_slot, "Logarithms", "MCQ",
      "The sum of all possible real values of x for which "
      "log(x-3)(x² - 9) = log(x-3)(x + 1) + 2, is",
      ["-3", "√33", "(3 + √33)/2", "3"]),
    q(_slot, "Ratio & Proportion", "TITA",
      "The ratio of the number of coins in boxes A and B was 17:7. After 108 coins were "
      "shifted from box A to box B, this ratio became 37:20. The number of coins that needs "
      "to be shifted further from A to B, to make this ratio 1:1, is"),
    q(_slot, "Time and Work - Pipes & Cisterns", "MCQ",
      "The rate of water flow through three pipes A, B and C are in the ratio 4 : 9 : 36. An "
      "empty tank can be filled up completely by pipe A in 15 hours. If all the three pipes "
      "are used simultaneously to fill up this empty tank, the time, in minutes, required to "
      "fill up the entire tank completely is nearest to", ["76", "78", "73", "71"]),
    q(_slot, "Time and Work", "MCQ",
      "Teams A, B, and C consist of five, eight, and ten members, respectively, such that "
      "every member within a team is equally productive. Working separately, teams A, B, "
      "and C can complete a certain job in 40 hours, 50 hours, and 4 hours, respectively. "
      "Two members from team A, three members from team B, and one member from team C "
      "together start the job, and the member from team C leaves after 23 hours. The number "
      "of additional member(s) from team B, that would be required to replace the member "
      "from team C, to finish the job in the next one hour, is", ["1", "2", "3", "4"]),
    q(_slot, "Time Speed Distance", "TITA",
      "Ankita walks from A to C through B, and runs back through the same route at a speed "
      "that is 40% more than her walking speed. She takes exactly 3 hours 30 minutes to walk "
      "from B to C as well as to run from B to A. The total time, in minutes, she would take "
      "to walk from A to B and run from B to C, is"),
    q(_slot, "Number Systems - Exponential Equations", "TITA",
      "If 12^(12x) × 4^(24x+12) × 5^(2y) = 8^(4z) × 20^(12x) × 243^(3x-6), "
      "where x, y and z are natural numbers, then x + y + z equals"),
    q(_slot, "Number Systems - Digit Sum", "MCQ",
      "The sum of all the digits of the number (10^50 + 10^25 - 123), is",
      ["21", "221", "324", "255"]),
    q(_slot, "Algebra - Roots", "MCQ",
      "If f(x) = (x² + 3x)(x² + 3x + 2), then the sum of all real roots of the "
      "equation √(f(x) + 1) = 9701, is", ["6", "-3", "-6", "3"]),
    q(_slot, "Functions - Range", "MCQ",
      "For real values of x, the range of the function f(x) = (2x - 3)/(2x² + 4x - 6) is",
      ["(-∞, 1/8] ∪ [1, ∞)", "(-∞, 1/8] ∪ [1/2, ∞)",
       "(-∞, 1/4] ∪ [1/2, ∞)", "(-∞, 1/4] ∪ [1, ∞)"]),
    q(_slot, "Profit, Loss & Discount", "MCQ",
      "The monthly sales of a product from January to April were 120, 135, 150 and 165 "
      "units, respectively. The cost price of the product was Rs. 240 per unit, and a fixed "
      "marked price was used for the product in all the four months. Discounts of 20%, 10% "
      "and 5% were given on the marked price per unit in January, February and March, "
      "respectively, while no discounts were given in April. If the total profit from "
      "January to April was Rs. 138825, then the marked price per unit, in rupees, was",
      ["525", "510", "520", "515"]),
    q(_slot, "Geometry - Triangles & Altitudes", "TITA",
      "A triangle ABC is formed with AB = AC = 50 cm and BC = 80 cm. Then, the sum of the "
      "lengths, in cm, of all three altitudes of the triangle ABC is"),
    q(_slot, "Number Systems - Optimization", "TITA",
      "Let p, q and r be three natural numbers such that their sum is 900, and r is a "
      "perfect square whose value lies between 150 and 500. If p is not less than 0.3q and "
      "not more than 0.7q, then the sum of the maximum and minimum possible values of p is"),
    q(_slot, "Averages", "MCQ",
      "The average salary of 5 managers and 25 engineers in a company is 60000 rupees. If "
      "each of the managers received 20% salary increase while the salary of the engineers "
      "remained unchanged, the average salary of all 30 employees would have increased by "
      "5%. The average salary, in rupees, of the engineers is",
      ["40000", "54000", "50000", "45000"]),
    q(_slot, "Optimization", "TITA",
      "In a school with 1500 students, each student chooses any one of the streams out of "
      "science, arts, and commerce, by paying a fee of Rs 1100, Rs 1000, and Rs 800, "
      "respectively. The total fee paid by all the students is Rs 15,50,000. If the number "
      "of science students is not more than the number of arts students, then the maximum "
      "possible number of science students in the school is"),
    q(_slot, "Arithmetic Progression", "TITA",
      "In an arithmetic progression, if the sum of fourth, seventh and tenth terms is 99, "
      "and the sum of the first fourteen terms is 497, then the sum of first five terms is"),
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
            print(f"CAT 2025 QA PYQs already seeded ({existing} rows); skipping.")
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
        print(f"Seeded {len(QUESTIONS)} CAT 2025 QA PYQ questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

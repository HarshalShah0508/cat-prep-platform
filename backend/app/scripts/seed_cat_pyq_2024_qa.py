"""Seed real CAT 2024 QA (Quantitative Aptitude) questions, all 3 slots,
retyped from the official question papers (via the combined SOLUTIONS
PDFs) in pyq-source/2024/.

`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

Source note: Slot 1's source file is named QUANT_SLOT1_CAT_2025_SOLUTIONS.pdf
(a filename typo in the source folder) but its content is confirmed CAT
2024 QA Slot 1 - tagged source_year=2024 here regardless of filename.
Slot 2 and Slot 3 use their correctly-named QUANT_SLOTn_CAT_2024_SOLUTIONS.pdf
files. All three are the combined question+solution format (full verbatim
question text, options, then a worked solution).

IMPORTANT QUALITY NOTE: same as the 2024 DILR set - several of this
year's "collegedunia" worked solutions are internally inconsistent or
contain guess-and-check filler that doesn't actually derive the printed
answer (e.g. Slot 1 Q1, Q5, Q9 solutions visibly go off the rails before
landing on the printed answer; Slot 3 Q4's solution explicitly says "There
appears to be an error in the calculations" and never corrects it). The
question TEXT and printed options/answer are transcribed as-is and are
reliable; the worked-solution prose should not be trusted without
independent verification in the eventual solutions pass. Not a blocker
for this questions-only load since correct_answer/explanation aren't
loaded here anyway.

Exact per-slot question counts (confirmed from each paper's own
instructions page - CAT's QA question count is not fixed year to year):
Slot 1 = 22, Slot 2 = 19, Slot 3 = 22. Every question in all three slots
was cleanly recoverable; nothing skipped in this section.

Run with:
    python -m app.scripts.seed_cat_pyq_2024_qa
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024


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

# ============================================================ SLOT 1 (22) ====
_slot = "slot1"
QUESTIONS += [
    q(_slot, "Word Problem - Successive Fractions", "MCQ",
      "A shop wants to sell a certain quantity (in kg) of grains. It sells half the "
      "quantity and an additional 3 kg of these grains to the first customer. Then, it "
      "sells half of the remaining quantity and an additional 3 kg of these grains to "
      "the second customer. Finally, when the shop sells half of the remaining quantity "
      "and an additional 3 kg of these grains to the third customer, there are no grains "
      "left. The initial quantity, in kg, of grains is",
      ["42", "18", "36", "50"]),
    q(_slot, "Profit and Loss", "MCQ",
      "The selling price of a product is fixed to ensure 40% profit. If the product had "
      "cost 40% less and had been sold for 5 rupees less, then the resulting profit "
      "would have been 50%. The original selling price, in rupees, of the product is",
      ["10", "20", "14", "15"]),
    q(_slot, "Surds", "MCQ",
      "If (a + b√n) is the positive square root of (29 − 12√5), where a and b are "
      "integers, and n is a natural number, then the maximum possible value of (a + b + n) is ?",
      ["4", "22", "18", "6"]),
    q(_slot, "Mixtures - Successive Dilution", "MCQ",
      "A glass is filled with milk. Two-thirds of its content is poured out and replaced "
      "with water. If this process of pouring out two-thirds the content and replacing "
      "with water is repeated three more times, then the final ratio of milk to water in "
      "the glass, is",
      ["1:80", "1:27", "1:26", "1:81"]),
    q(_slot, "Time and Work", "TITA",
      "Renu would take 15 days working 4 hours per day to complete a certain task "
      "whereas Seema would take 8 days working 5 hours per day to complete the same "
      "task. They decide to work together to complete this task. Seema agrees to work "
      "for double the number of hours per day as Renu, while Renu agrees to work for "
      "double the number of days as Seema. If Renu works 2 hours per day, then the "
      "number of days Seema will work, is"),
    q(_slot, "Arithmetic Progression", "MCQ",
      "Suppose x1, x2, x3, ..., x100 are in arithmetic progression such that x5 = −4 and "
      "2x6 + 2x9 = x11 + x13. Then, x100 equals ?",
      ["206", "-196", "204", "-194"]),
    q(_slot, "Functions - Onto/Surjective", "MCQ",
      "Consider two sets A = {2, 3, 5, 7, 11, 13} and B = {1, 8, 27}. Let f be a function "
      "from A to B such that for every element b in B, there is at least one element a "
      "in A such that f(a) = b. Then, the total number of such functions f is",
      ["537", "540", "667", "665"]),
    q(_slot, "Algebra - Simultaneous Equations", "MCQ",
      "Let x, y, and z be real numbers satisfying 4(x² + y² + z²) = a, "
      "4(x − y − z) = 3 + a. Then a equals ?",
      ["3", "4", "1", "1 1/3"]),
    q(_slot, "Indices and Exponents", "MCQ",
      "The sum of all real values of k for which (1/8)^k × (1/32768)^(4/3) = "
      "1/8 × (1/32768)^(k/3) is",
      ["4/3", "-4/3", "2/3", "-2/3"]),
    q(_slot, "Percentages - Ratios", "MCQ",
      "In September, the incomes of Kamal, Amal and Vimal are in the ratio 8 : 6 : 5. "
      "They rent a house together, and Kamal pays 15%, Amal pays 12% and Vimal pays 18% "
      "of their respective incomes to cover the total house rent in that month. In "
      "October, the house rent remains unchanged while their incomes increase by 10%, "
      "12% and 15%, respectively. In October, the percentage of their total income that "
      "will be paid as house rent, is nearest to",
      ["14.84", "13.26", "15.18", "12.75"]),
    q(_slot, "Quadratic Equations - Common Root", "TITA",
      "If the equations x² + mx + 9 = 0, x² + nx + 17 = 0, and "
      "x² + (m+n)x + 35 = 0 have a common negative root, then the value of "
      "(2m + 3n) is ?"),
    q(_slot, "Functions - Floor Function Summation", "TITA",
      "Let an be the largest integer not exceeding √n. Then the value of "
      "a1 + a2 + ⋯ + a50 is"),
    q(_slot, "Number Systems - Remainders", "MCQ",
      "When 10^100 is divided by 7, the remainder is ?",
      ["6", "3", "1", "4"]),
    q(_slot, "Ratios - Word Problem", "TITA",
      "A fruit seller has a total of 187 fruits consisting of apples, mangoes and "
      "oranges. The number of apples and mangoes are in the ratio 5 : 2. After she "
      "sells 75 apples, 26 mangoes and half of the oranges, the ratio of number of "
      "unsold apples to number of unsold oranges becomes 3 : 2. The total number of "
      "unsold fruits is"),
    q(_slot, "Time Speed Distance", "MCQ",
      "Two places A and B are 45 kms apart and connected by a straight road. Anil goes "
      "from A to B while Sunil goes from B to A. Starting at the same time, they cross "
      "each other in exactly 1 hour 30 minutes. If Anil reaches B exactly 1 hour 15 "
      "minutes after Sunil reaches A, the speed of Anil, in km per hour, is",
      ["12", "16", "14", "18"]),
    q(_slot, "Averages", "TITA",
      "There are four numbers such that average of first two numbers is 1 more than the "
      "first number, average of first three numbers is 2 more than average of first two "
      "numbers, and average of first four numbers is 3 more than average of first three "
      "numbers. Then, the difference between the largest and the smallest numbers, is"),
    q(_slot, "Geometry - Incircle", "TITA",
      "ABCD is a rectangle with sides AB = 56 cm and BC = 45 cm, and E is the midpoint "
      "of side CD. Then, the length, in cm, of radius of incircle of △ADE is"),
    q(_slot, "Permutations - Digit Sum", "TITA",
      "The sum of all four-digit numbers that can be formed with the distinct non-zero "
      "digits a, b, c, and d, with each digit appearing exactly once in every number, "
      "is 153310 + n, where n is a single digit natural number. Then, the value of "
      "(a + b + c + d) is ?"),
    q(_slot, "Mensuration - Sphere and Cuboid", "MCQ",
      "The surface area of a closed rectangular box, which is inscribed in a sphere, is "
      "846 sq cm, and the sum of the lengths of all its edges is 144 cm. The volume, in "
      "cubic cm, of the sphere is ?",
      ["1125π√2", "750π", "750π√2", "1125π"]),
    q(_slot, "Coordinate Geometry - Circles", "MCQ",
      "In the XY-plane, the area, in sq. units, of the region defined by the "
      "inequalities y ≥ x + 4 and −4 ≤ x² + y² + 4(x − y) ≤ 0 is",
      ["2π", "3π", "π", "4π"]),
    q(_slot, "Logarithms", "TITA",
      "Let x be a positive real number such that 4 log10 x + 4 log100 x + 8 log1000 x = "
      "13, then the greatest integer not exceeding x. is"),
    q(_slot, "Simple Interest", "MCQ",
      "An amount of Rs 10000 is deposited in bank A for a certain number of years at a "
      "simple interest of 5% per annum. On maturity, the total amount received is "
      "deposited in bank B for another 5 years at a simple interest of 6% per annum. If "
      "the interests received from bank A and bank B are in the ratio 10 : 13, then the "
      "investment period, in years, in bank A is",
      ["5", "3", "6", "4"]),
]

# ============================================================ SLOT 2 (19) ====
_slot = "slot2"
QUESTIONS += [
    q(_slot, "Number Systems - Prime Factorization", "MCQ",
      "If m and n are natural numbers such that n > 1, and m^n = 2^25 × 3^40, then "
      "m − n equals",
      ["209942", "209947", "209932", "209937"]),
    q(_slot, "Quadratic Equations - Roots", "MCQ",
      "The roots α, β of the equation 3x² + λx − 1 = 0, satisfy "
      "1/α² + 1/β² = 15. The value of (α³ + β³)² is",
      ["16", "9", "1", "4"]),
    q(_slot, "Algebra - Absolute Value Equations", "MCQ",
      "If x and y satisfy the equations |x| + x + y = 15 and x + |y| − y = 20, then "
      "(x − y) equals",
      ["5", "10", "20", "15"]),
    q(_slot, "Compound Interest", "MCQ",
      "Anil invests Rs 22000 for 6 years in a scheme with 4% interest per annum, "
      "compounded half-yearly. Separately, Sunil invests a certain amount in the same "
      "scheme for 5 years, and then reinvests the entire amount he receives at the end "
      "of 5 years, for one year at 10% simple interest. If the amounts received by both "
      "at the end of 6 years are equal, then the initial investment, in rupees, made by "
      "Sunil is",
      ["20640", "20808", "20860", "20480"]),
    q(_slot, "Mixtures", "MCQ",
      "A vessel contained a certain amount of a solution of acid and water. When 2 "
      "litres of water was added to it, the new solution had 50% acid concentration. "
      "When 15 litres of acid was further added to this new solution, the final "
      "solution had 80% acid concentration. The ratio of water and acid in the "
      "original solution was",
      ["3:5", "5:3", "4:5", "5:4"]),
    q(_slot, "Time Speed Distance", "MCQ",
      "A bus leaves the bus stand at 9 am and travels at a constant speed of 60 km/h. "
      "It reaches its destination 3.5 hours later than its original time. The next "
      "day, it travels 2/3 of its route within 1/3 of its initial time and travels the "
      "rest of the route within 40 minutes. At what time does it reach its destination "
      "normally?",
      ["1:15 PM", "1:17 PM", "3:12 PM", "1:25 PM"]),
    q(_slot, "Geometry - Incircle of Right Triangle", "TITA",
      "The coordinates of the three vertices of a triangle are: (1, 2), (7, 2), and "
      "(1, 10). Then the radius of the incircle of the triangle is"),
    q(_slot, "Profit and Loss - Chain", "TITA",
      "Bina incurs 19% loss when she sells a product at Rs. 4860 to Shyam, who in turn "
      "sells this product to Hari. If Bina would have sold this product to Shyam at "
      "the purchase price of Hari, she would have obtained 17% profit. Then, the "
      "profit, in rupees, made by Shyam is"),
    q(_slot, "Time and Work", "TITA",
      "Amal and Vimal together can complete a task in 150 days, while Vimal and Sunil "
      "together can complete the same task in 100 days. Amal starts working on the "
      "task and works for 75 days, then Vimal takes over and works for 135 days. "
      "Finally, Sunil takes over and completes the remaining task in 45 days. If Amal "
      "had started the task alone and worked on all days, Vimal had worked on every "
      "second day, and Sunil had worked on every third day, then the number of days "
      "required to complete the task would have been"),
    q(_slot, "Functions - Functional Equation", "MCQ",
      "A function f maps the set of natural numbers to whole numbers, such that "
      "f(xy) = f(x)f(y) + f(x) + f(y) for all x, y and f(p) = 1 for every prime "
      "number p. Then, the value of f(160000) is",
      ["4095", "8191", "2047", "1023"]),
    q(_slot, "Ages", "MCQ",
      "When Rajesh's age was same as the present age of Garima, the ratio of their "
      "ages was 3 : 2. When Garima's age becomes the same as the present age of "
      "Rajesh, the ratio of the ages of Rajesh and Garima will become",
      ["5:4", "2:1", "4:3", "3:2"]),
    q(_slot, "Sequences and Series - Infinite Geometric Series", "MCQ",
      "The sum of the infinite series (1/5)(1/5 − 1/7) + (1/5)²(1/5 − 1/7)² "
      "− (1/7)² + (1/5)³(1/5 − 1/7)³ + … is equal to",
      ["7/408", "5/408", "7/816", "5/816"]),
    q(_slot, "Percentages - Stock Word Problem", "TITA",
      "A fruit seller has a stock of mangoes, bananas, and apples with at least one "
      "fruit of each type. At the beginning of a day, the number of mangoes makes up "
      "40% of his stock. That day, he sells half of the mangoes, 96 bananas, and 40% "
      "of the apples. At the end of the day, he ends up selling 50% of the fruits. "
      "What is the smallest possible total number of fruits in the stock at the "
      "beginning of the day?"),
    q(_slot, "Geometry - Circles Tangent to Three Circles", "MCQ",
      "Three circles of equal radii touch (but not cross) each other externally. Two "
      "other circles, X and Y, are drawn such that both touch (but not cross) each of "
      "the three previous circles. If the radius of X is more than that of Y, the "
      "ratio of the radii of X and Y is",
      ["4 + √3 : 1", "2 + √3 : 1", "4 + 2√3 : 1", "7 + 4√3 : 1"]),
    q(_slot, "Averages - Weighted", "MCQ",
      "A company has 40 employees whose names are listed in a certain order. In the "
      "year 2022, the average bonus of the first 30 employees was Rs. 40000, of the "
      "last 30 employees was Rs. 60000, and of the first 10 and last 10 employees "
      "together was Rs. 50000. Next year, the average bonus of the first 10 employees "
      "increased by 100%, of the last 10 employees increased by 200% and of the "
      "remaining employees was unchanged. Then, the average bonus, in rupees, of all "
      "the 40 employees together in the year 2023 was",
      ["90000", "95000", "85000", "80000"]),
    q(_slot, "Geometry - Trapezium", "MCQ",
      "ABCD is a trapezium in which AB is parallel to CD. The sides AD and BC when "
      "extended, intersect at point E. If AB = 2 cm, CD = 1 cm, and perimeter of ABCD "
      "is 6 cm, then the perimeter, in cm, of ΔAEB is",
      ["10", "9", "8", "7"]),
    q(_slot, "Algebra - Completing the Square", "TITA",
      "If x and y are real numbers such that 4x² + 4y² − 4xy − 6y + 3 = 0, "
      "then the value of (4x + 5y) is"),
    q(_slot, "Permutations and Combinations - Graph Paths", "TITA",
      "P, Q, R and S are four towns. One can travel between P and Q along 3 direct "
      "paths, between Q and S along 4 direct paths, and between P and R along 4 direct "
      "paths. There is no direct path between P and S, while there are few direct "
      "paths between Q and R, and between R and S. One can travel from P to S either "
      "via Q, or via R, or via Q followed by R, respectively, in exactly 62 possible "
      "ways. One can also travel from Q to R either directly, or via P, or via S, in "
      "exactly 27 possible ways. Then, the number of direct paths between Q and R is"),
    q(_slot, "Logarithms", "TITA",
      "If a, b, and c are positive real numbers such that a > 10 ≥ b ≥ c and "
      "log8(a+b)/log2 c + log27(a−b)/log3 c = 2/3, then the greatest possible "
      "integer value of a is"),
]

# ============================================================ SLOT 3 (22) ====
_slot = "slot3"
QUESTIONS += [
    q(_slot, "Geometry - Circle Chord and Sector", "MCQ",
      "A circular plot of land is divided into two regions by a chord of length "
      "10√3 meters such that the chord subtends an angle of 120° at the "
      "center. Then, the area, in square meters, of the smaller region is",
      ["20(4π/3 + √3)", "20(4π/3 − √3)",
       "25(4π/3 + √3)", "25(4π/3 − √3)"]),
    q(_slot, "Surds", "MCQ",
      "If (a + b√3)² = 52 + 30√3, where a and b are natural numbers, "
      "then a + b equals ?",
      ["8", "10", "9", "7"]),
    q(_slot, "Algebra - Max/Min and Absolute Value", "TITA",
      "The number of distinct real values of x, satisfying the equation "
      "max{x, 2} - min{x, 2} = |x + 2| - |x - 2|, is"),
    q(_slot, "Averages", "TITA",
      "The average of three distinct real numbers is 28. If the smallest number is "
      "increased by 7 and the largest number is reduced by 10, the order of the "
      "numbers remains unchanged, and the new arithmetic mean becomes 2 more than the "
      "middle number, while the difference between the largest and the smallest "
      "numbers becomes 64. Then, the largest number in the original set of three "
      "numbers is"),
    q(_slot, "Compound Interest", "TITA",
      "Aman invests Rs 4000 in a bank at a certain rate of interest, compounded "
      "annually. If the ratio of the value of the investment after 3 years to the "
      "value of the investment after 5 years is 25 : 36, then the minimum number of "
      "years required for the value of the investment to exceed Rs 20000 is"),
    q(_slot, "Ratios - Word Problem", "MCQ",
      "Rajesh and Vimal own 20 hectares and 30 hectares of agricultural land, "
      "respectively, which are entirely covered by wheat and mustard crops. The "
      "cultivation area of wheat and mustard in the land owned by Vimal are in the "
      "ratio of 5 : 3. If the total cultivation area of wheat and mustard are in the "
      "ratio 11 : 9, then the ratio of cultivation area of wheat and mustard in the "
      "land owned by Rajesh is",
      ["7:9", "3:7", "1:1", "4:3"]),
    q(_slot, "Number Systems - Remainders", "MCQ",
      "10^68 is divided by 13, the remainder is",
      ["9", "4", "5", "8"]),
    q(_slot, "Algebra - Absolute Value Equations", "TITA",
      "The number of distinct integer solutions (x, y) of the equation "
      "|x + y| + |x - y| = 2, is"),
    q(_slot, "Time Speed Distance", "MCQ",
      "A train travelled a certain distance at a uniform speed. Had the speed been 6 "
      "km per hour more, it would have needed 4 hours less. Had the speed been 6 km "
      "per hour less, it would have needed 6 hours more. The distance, in km, "
      "travelled by the train is",
      ["800", "640", "720", "780"]),
    q(_slot, "Sequences - Recurrence Relation", "MCQ",
      "Consider the sequence t1 = 1, t2 = −1 and tn = ((n−3)/(n−1))t(n−2) "
      "for n ≥ 3. Then, the value of the sum "
      "1/t2 + 1/t4 + 1/t6 + ....... + 1/t2022 + 1/t2024, is",
      ["-1024144", "-1023132", "-1026169", "-1022121"]),
    q(_slot, "Logarithms - Chained Exponents", "TITA",
      "If 3^a = 4, 4^b = 5, 5^c = 6, 6^d = 7, 7^e = 8 and 8^f = 9, then the value of "
      "the product abcdef is"),
    q(_slot, "Percentages - Successive Increments", "MCQ",
      "After two successive increments, Gopal's salary became 187.5% of his initial "
      "salary. If the percentage of salary increase in the second increment was twice "
      "of that in the first increment, then the percentage of salary increase in the "
      "first increment was",
      ["27.5", "30", "25", "20"]),
    q(_slot, "Functions - Functional Equation", "MCQ",
      "For any non-zero real number x, let f(x) + 2f(1/x) = 3x. Then, the sum of all "
      "possible values of x for which f(x) = 3, is",
      ["3", "-3", "-2", "2"]),
    q(_slot, "Mixtures - Replacement", "TITA",
      "A certain amount of water was poured into a 300 litre container and the "
      "remaining portion of the container was filled with milk. Then an amount of "
      "this solution was taken out from the container which was twice the volume of "
      "water that was earlier poured into it, and water was poured to refill the "
      "container again. If the resulting solution contains 72% milk, then the amount "
      "of water, in litres, that was initially poured into the container was"),
    q(_slot, "Sets - Overlapping Groups", "MCQ",
      "In a group of 250 students, the percentage of girls was at least 44% and at "
      "most 60%. The rest of the students were boys. Each student opted for either "
      "swimming or running or both. If 50% of the boys and 80% of the girls opted for "
      "swimming while 70% of the boys and 60% of the girls opted for running, then the "
      "minimum and maximum possible number of students who opted for both swimming "
      "and running, are",
      ["75 and 90, respectively", "72 and 80, respectively",
       "72 and 88, respectively", "75 and 96, respectively"]),
    q(_slot, "Logarithms and Exponents", "MCQ",
      "The sum of all distinct real values of x that satisfy the equation "
      "10^x + 4/10^x = 81/2 is",
      ["3 log10 2", "log10 2", "4 log10 2", "2 log10 2"]),
    q(_slot, "Geometry - Regular Octagon", "MCQ",
      "A regular octagon ABCDEFGH has sides of length 6 cm each. Then the area, in "
      "sq. cm, of the square ACEG is",
      ["36(1+√2)", "72(2+√2)", "72(1+√2)", "36(2+√2)"]),
    q(_slot, "Algebra - System of Linear Equations", "MCQ",
      "For some constant real numbers p, k and a, consider the following system of "
      "linear equations in x and y: px - 4y = 2, 3x + ky = a. A necessary condition "
      "for the system to have no solution for (x, y), is",
      ["ap - 6 = 0", "kp + 12 ≠ 0", "ap + 6 = 0", "2a + k ≠ 0"]),
    q(_slot, "Profit and Loss - Discount", "MCQ",
      "Gopi marks a price on a product in order to make 20% profit. Ravi gets 10% "
      "discount on this marked price, and thus saves Rs 15. Then, the profit, in "
      "rupees, made by Gopi by selling the product to Ravi, is",
      ["20", "25", "15", "10"]),
    q(_slot, "Geometry - Medians and Midpoints", "TITA",
      "The midpoints of sides AB, BC, and AC in ΔABC are M, N, and P, "
      "respectively. The medians drawn from A, B, and C intersect the line segments "
      "MP, MN and NP at X, Y, and Z, respectively. If the area of ΔABC is 1440 sq "
      "cm, then the area, in sq cm, of ΔXYZ is"),
    q(_slot, "Number Systems - Non-repeating Digits", "TITA",
      "The number of all positive integers up to 500 with non-repeating digits is"),
    q(_slot, "Time and Work - Cyclic Pattern", "MCQ",
      "Sam can complete a job in 20 days when working alone. Mohit is twice as fast "
      "as Sam and thrice as fast as Ayana in the same job. They undertake a job with "
      "an arrangement where Sam and Mohit work together on the first day, Sam and "
      "Ayana on the second day, Mohit and Ayana on the third day, and this three-day "
      "pattern is repeated till the work gets completed. Then, the fraction of total "
      "work done by Sam is",
      ["3/20", "3/10", "1/5", "1/20"]),
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
            print(f"CAT 2024 QA already seeded ({existing} rows); skipping.")
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
        print(f"Seeded {len(QUESTIONS)} CAT 2024 QA PYQ questions across 3 slots.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

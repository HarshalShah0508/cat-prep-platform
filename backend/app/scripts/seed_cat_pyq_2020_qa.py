"""Seed real CAT 2020 QA questions, generated from the official
solutions PDFs via pdftotext + pyq_qa_parser.py (automated text-layer
extraction, not LLM transcription).

Roughly half of CAT QA questions embed their math as a rendered image pdftotext can't recover (shows up as a run of blank space where an 
equation used to be, or an empty option) - those are intentionally omitted here, not fabricated. See stderr from the generation step for 
which question numbers were skipped per slot.

`correct_answer`/`explanation` are intentionally left blank for now - the answer key
is loaded separately once transcribed from the solutions PDFs.

Run with:
    python -m app.scripts.seed_cat_pyq_2020_qa
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020


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
    q(_slot, "TITA", "How many 3-digit numbers are there, for which the product of their digits is more than 2 but less than 7?", options=None),
    q(_slot, "MCQ", "If f (5 + x) = f (5 − x) for every real x and f (x) = 0 has four distinct real roots, then the sum of the roots is", options=["0", "40", "10", "20"]),
    q(_slot, "TITA", "Veeru invested Rs 10000 at 5% simple annual interest, and exactly after two years, Joy invested Rs 8000 at 10% simple annual interest. How many years after Veeru’s investment, will their balances be equal?", options=None),
    q(_slot, "MCQ", "A train traveled at one-third of its usual speed, reaching the destination 30 minutes late. On its return journey, it traveled at usual speed for 5 minutes but stopped for 4 minutes. The percentage increase in speed needed to reach on time is nearest to:", options=["58", "67", "50", "61"]),
    q(_slot, "MCQ", "A straight road connects points A and B. Car 1 travels from A to B and Car 2 travels from B to A, both leaving at the same time. After meeting each other, they take 45 minutes and 20 minutes, respectively, to complete their journeys. If Car 1 travels at the speed of 60 km/hr, then the speed of Car 2, in km/hr, is", options=["90", "80", "70", "100"]),
    q(_slot, "MCQ", "Let A, B, and C be three positive integers such that the sum of A and the mean of B and C is 5. In addition, the sum of B and the mean of A and C is 7. Then the sum of A and B is", options=["6", "4", "7", "5"]),
    q(_slot, "MCQ", "If x = (4096)r+ 3 , then which of the following equals 64?\n\nn Options: (A) xx1/2 r", options=["xx1/2 r/s", "xx2/3 r", "xx2/3 r/s"]),
    q(_slot, "MCQ", "The mean of all 4-digit even natural numbers of the form ’aabb’, where a > 0, is", options=["5544", "4466", "4864", "5050"]),
    q(_slot, "MCQ", "The number of distinct real roots of the equation (x + 1/x)2 − 3(x + 1/x) + 2 = 0 equals:", options=["0", "1", "2", "3"]),
    q(_slot, "MCQ", "A person spent Rs 50000 to purchase a desktop computer and a laptop computer. He sold the desktop at 20", options=["20000", "25000", "30000", "35000"]),
    q(_slot, "MCQ", "Among 100 students, x1 have birthdays in January, x2 have birthdays in February, and so on. If x0 = max(x1 , x2 , . . . , x12 ), then the smallest possible value of x0 is", options=["8", "10", "12", "9"]),
    q(_slot, "MCQ", "Among 100 students, x1 have birthdays in January, x2 have birthdays in February, and so on. If x0 = max(x1 , x2 , . . . , x12 ), then the smallest possible value of x0 is", options=["8", "10", "12", "9"]),
    q(_slot, "MCQ", "How many distinct positive integer-valued solutions exist to the equation (x2 − 7x + 11)2 − 13x + 42 = 1?", options=["6", "2", "4", "8"]),
    q(_slot, "MCQ", "The area of the region satisfying the inequalities |x| − y ≤ 1, y ≥ 0, and y ≤ 1 is", options=["6", "2", "4", "3"]),
    q(_slot, "MCQ", "A solid right circular cone of height 27 cm is cut into 2 pieces along a plane parallel to its base at a height of 18 cm from the base. If the difference in the volume of the two pieces is 225 cc, the volume, in cc, of the original cone is", options=["264", "232", "243", "256"]),
    q(_slot, "MCQ", "A circle is inscribed in a rhombus with diagonals 12 cm and 16 cm. The ratio of the area of the circle to the area of the rhombus is", options=["2π", "6π", "3π", "5π"]),
    q(_slot, "MCQ", "Leaving home at the same time, Amal reaches office at 10:15 am if he travels at 8 kmph, and at 9:40 am if he travels at 15 kmph. Leaving home at 9:10 am, at what speed, in kmph, must he travel so as to reach office exactly at 10:00 am?", options=["12", "11", "13", "14"]),
    q(_slot, "MCQ", "If a, b, and c are positive integers such that ab = 432, bc = 96 and c < 9, then the smallest possible value of a + b + c is", options=["56", "49", "46", "59"]),
    q(_slot, "MCQ", "If y is a negative number such that 2y 2 log 35 = 5 log 23 , then y equals", options=["log2 31 \u0001", "log2 15 \u0001", "− log2 13 \u0001", "− log2 15 \u0001 \u0001"]),
    q(_slot, "MCQ", "On a rectangular metal sheet of area 135 sq in, a circle is painted such that the circle touches opposite two sides. If the area of the sheet left unpainted is two-thirds of the painted area, then the perimeter of the rectangle in inches is", options=["3π(5 + 12 π)", "3π(4 + 10 π)", "4π(5 + 13 π)", "2π(5 + π8 )"]),
    q(_slot, "MCQ", "An alloy is prepared by mixing metals A, B, C in the proportion 3 : 4 : 7 by volume. Weights of the same volume of metals A, B, C are in the ratio 5 : 2 : 6. In 130 kg of the alloy, the weight, in kg, of the metal C is", options=["84", "48", "96", "70"]),
    q(_slot, "MCQ", "In 130 kg of the alloy, the weight, in kg, of the metal C is", options=["84", "48", "96", "70"]),
    q(_slot, "MCQ", "A solution, of volume 40 litres, has dye and water in the proportion 2 : 3. Water is added to the solution to change this proportion to 2 : 5. If one-fourth of this diluted solution is taken out, how many litres of dye must be added to the remaining solution to bring the proportion back to 2 : 3?", options=["8", "6", "10", "4"]),
    q(_slot, "MCQ", "The number of real-valued solutions of the equation 2x + 22x = 2 − (x − 2)2 is", options=["infinite", "0", "1", "2"]),
    q(_slot, "MCQ", "In a group of people, 28% of the members are young while the rest are old. If 65% of the members are literates, and 25% of the literates are young, then the percentage of old people among the illiterates is nearest to", options=["59", "62", "66", "55"]),
]

# ============================================================ SLOT 2 ====
_slot = "slot2"
QUESTIONS += [
    q(_slot, "MCQ", "In a car race, car A beats car B by 45 km, car B beats car C by 50 km, and car A beats car C by 90 km. The distance (in km) over which the race has been conducted is:", options=["550", "475", "500", "450"]),
    q(_slot, "MCQ", "From the interior point of an equilateral triangle, perpendiculars are drawn on all three sides. The sum of the lengths of the perpendiculars is ’s’. Then the area of the triangle is:", options=["2s√3", "√s 3 √", "s 2 3", "2s √"]),
    q(_slot, "MCQ", "In a group of 10 students, the mean of the lowest 9 scores is 42 while the mean of the highest 9 scores is 47. For the entire group of 10 students, the maximum possible mean exceeds the minimum possible mean by:", options=["5", "3", "4", "2"]),
    q(_slot, "TITA", "The number of pairs of integers (x, y) satisfying x ≥ y ≥ −20 and 2x + 5y = 99 is:", options=None),
    q(_slot, "MCQ", "Let the mth and nth terms of a geometric progression be 34 and 12, respectively, where m < n. If the common ratio r is an integer, then the smallest possible value of r + n − m is:", options=["-4", "-2", "6", "2"]),
    q(_slot, "TITA", "For the same principal amount, the compound interest for two years at 5% per annum exceeds the simple interest for three years at 3% per annum by Rs 1125. Then the principal amount in rupees is:", options=None),
    q(_slot, "MCQ", "Let C be a circle of radius 5 meters having center at O. Let P Q be a chord of C that passes through points A and B , where A is located 4 meters north of O and B is located 3 meters east of O. Then, the length of P Q, in meters, is nearest to:", options=["6.6", "7.2", "8.8", "7.8"]),
    q(_slot, "MCQ", "Anil buys 12 toys and labels each with the same selling price. He sells 8 toys initially at 20% discount on the labeled price. Then he sells the remaining 4 toys at an additional 25% discount on the discounted price. Thus, he gets a total of Rs 2112, and makes a 10% profit. With no discounts, his percentage of profit would have been:", options=["60", "50", "55", "54"]),
    q(_slot, "MCQ", "If x and y are non-negative integers such that x + 9 = z , y + 1 = z , and x + y < z + 5, then the maximum possible value of 2x + y equals:", options=["21", "22", "23", "20"]),
    q(_slot, "MCQ", "Students in a college have to choose at least two subjects from chemistry, mathematics and physics. The number of students choosing all three subjects is 18, choosing mathematics as one of their subjects is 23 and choosing physics as one of their subjects is 25. The smallest possible number of students who could choose chemistry as one of their subjects is", options=["22", "19", "20", "21"]),
    q(_slot, "MCQ", "Let f (x) = x2 + ax + b and g(x) = f (x + 1) − f (x − 1). If f (x) ≥ 0 for all real x, and g(20) = 72, then the smallest possible value of b is", options=["16", "1", "4", "0"]),
    q(_slot, "MCQ", "The distance from B to C is thrice that from A to B. Two trains travel from A to C via B. The speed of train 2 is double that of train 1 while traveling from A to B and their speeds are interchanged while traveling from B to C. The ratio of the time taken by train 1 to that taken by train 2 in travelling from A to C is", options=["7:5", "4:1", "1:4", "5:7"]),
    q(_slot, "MCQ", "The sum of perimeters of an equilateral triangle and a rectangle is 90 cm. The area, T, of the triangle and the area, R, of the rectangle, both in sq cm, satisfy the relationship R = T 2 . If the sides of the rectangle are in the ratio 1 : 3, then the length, in cm, of the longer side of the rectangle, is", options=["27", "18", "21", "24"]),
    q(_slot, "MCQ", "The number of integers that satisfy the equality (x2 − 5x + 7)x+1 = 1 is", options=["5", "4", "3", "2"]),
    q(_slot, "MCQ", "In how many ways can a pair of integers (x, a) be chosen such that x2 − 2|x| + |a − 2| = 0?", options=["7", "6", "4", "5"]),
    q(_slot, "MCQ", "Two circular tracks T1 and T2 of radii 100 m and 20 m, respectively, touch at a point A. Starting from A at the same time, Ram and Rahim are walking on T1 and T2 at speeds 15 km/h and 5 km/h respectively. The number of full rounds that Ram will make before he meets Rahim again for the first time is:", options=["5", "3", "4", "2"]),
    q(_slot, "MCQ", "Let C1 and C2 be concentric circles such that the diameter of C1 is 2 cm longer than that of C2 . If a chord of C1 has length 6 cm and is a tangent to C2 , then the diameter, in cm, of C1 is:", options=["10", "8", "12", "6"]),
    q(_slot, "MCQ", "A and B are two points on a straight line. Ram runs from A to B while Rahim runs from B to A. After crossing each other, Ram and Rahim reach their destinations in one minute and four minutes, respectively. If they start at the same time, then the ratio of Ram’s speed to Rahim’s speed is: √", options=["2", "2", "√12", "12"]),
    q(_slot, "MCQ", "John takes twice as much time as Jack to finish a job. Jack and Jim together take one-third of the time to finish the job than John takes working alone. Moreover, in order to finish the job, John takes three days more than that taken by three of them working together. In how many days will Jim finish the job working alone?", options=["3", "4", "6", "5"]),
    q(_slot, "MCQ", "In May, John bought the same amount of rice and the same amount of wheat as he had bought in April, but spent 150 more due to price increase of rice and wheat by 20% and 12%, respectively. If John had spent 450 on rice in April, then how much did he spend on wheat in May?", options=["590", "580", "560", "570"]),
    q(_slot, "MCQ", "Aron bought some pencils and sharpeners. Spending the same amount of money as Aron, Aditya bought twice as many pencils and 10 fewer sharpeners. If the cost of one sharpener is 2 more than the cost of a pencil, then the minimum possible number of pencils bought by Aron and Aditya together is", options=["33", "27", "30", "36"]),
    q(_slot, "MCQ", "A sum of money is split among Amal, Sunil and Mita so that the ratio of the shares of Amal and Sunil is 3:2, while the ratio of the shares of Sunil and Mita is 4:5. If the difference between the largest and the smallest of these three shares is Rs 400, then Sunil’s share, in rupees, is", options=["600", "500", "700", "800"]),
    q(_slot, "MCQ", "How many 4-digit numbers, each greater than 1000 and each having all four digits distinct, are there with 7 coming before 3?", options=["312", "330", "315", "324"]),
]

# ============================================================ SLOT 3 ====
_slot = "slot3"
QUESTIONS += [
    q(_slot, "MCQ", "If x1 = −1 and xm = xm+1 + (m + 1) for every positive integer m, then x100 equals:", options=["-5050", "-5051", "-5150", "-5151"]),
    q(_slot, "MCQ", "Let N , x, and y be positive integers such that N = x + y , 2 < x < 10, and 14 < y < 23. If N > 25, then how many distinct values are possible for N ?", options=["6", "7", "8", "9"]),
    q(_slot, "MCQ", "A contractor agreed to construct a 6 km road in 200 days. He employed 140 persons for the work. After 60 days, he realized that only 1.5 km road has been completed. How many additional people would he need to employ in order to finish the work exactly on time?", options=["40", "50", "60", "70"]),
    q(_slot, "MCQ", "The area, in sq. units, enclosed by the lines x = 2, y = |x − 2| + 4, the X-axis, and the Y-axis is equal to:", options=["12", "8", "6", "10"]),
    q(_slot, "MCQ", "Dick is thrice as old as Tom and Harry is twice as old as Dick. If Dick’s age is 1 year less than the average age of all three, then Harry’s age, in years, is:", options=["16", "18", "20", "22"]),
    q(_slot, "MCQ", "How many of the integers 1, 2, ..., 120, are divisible by none of 2, 5, and 7?", options=["41", "42", "40", "43"]),
    q(_slot, "MCQ", "In the final examination, Bishnu scored 52% and Asha scored 64%. The marks obtained by Bishnu are 23 less, and those by Asha are 34 more than the marks obtained by Ramesh. The marks obtained by Geeta, who scored 84%, are:", options=["399", "439", "357", "417"]),
    q(_slot, "MCQ", "If f (x + y) = f (x)f (y) and f (5) = 4, then f (10) − f (−10) is equal to:", options=["3", "0", "14.0625", "15.9375"]),
    q(_slot, "MCQ", "Anil, Sunil, and Ravi run along a circular path of length 3 km, starting from the same point at the same time, and going in the clockwise direction. If they run at speeds of 15 km/hr, 10 km/hr, and 8 km/hr, respectively, how much distance in km will Ravi have run when Anil and Sunil meet again for the first time at the starting point?", options=["4.6", "4.2", "4.8", "5.2"]),
    q(_slot, "MCQ", "A man buys 35 kg of sugar and sets a marked price in order to make a 20% profit. He sells 5 kg at this price, and 15 kg at a 10% discount. Accidentally, 3 kg of sugar is wasted. He sells the remaining sugar by raising the marked price by p percent so as to make an overall profit of 15%. Then p is nearest to:", options=["35", "31", "22", "25"]),
    q(_slot, "MCQ", "Let k be a constant. The equations kx + y = 3 and 4x + ky = 4 have a unique solution if and only if:", options=["k = 2", "k = 1", "k ̸= 2", "k = 2"]),
    q(_slot, "MCQ", "How many integers in the set {100, 101, 102, . . . , 999} have at least one digit repeated?", options=["252", "248", "256", "230"]),
    q(_slot, "MCQ", "A batsman played n + 2 innings and got out on all occasions. His average score in these n + 2 innings was 29 runs and he scored 38 and 15 runs in the last two innings. The batsman scored less than 38 runs in each of the first n innings. In these n innings, his average score was 30 runs and the lowest score was x runs. The smallest possible value of x is:", options=["1", "3", "2", "4"]),
    q(_slot, "MCQ", "Two alcohol solutions, A and B, are mixed in the proportion 1:3 by volume. The volume of the mixture is then doubled by adding solution A such that the resulting mixture has 72% alcohol. If solution A has 60% alcohol, then the percentage of alcohol in solution B is:", options=["94%", "92%", "90%", "89%"]),
    q(_slot, "MCQ", "The vertices of a triangle are (0, 0), (4, 0), and (3, 9). The area of the circle passing through these three points is:", options=["14", "12π", "205", "12π"]),
    q(_slot, "MCQ", "A person invested a certain amount of money at 10% annual interest, compounded half-yearly. After one and a half years, the interest and principal together became Rs 18522. The amount, in rupees, that the person had invested is:", options=["16000", "15000", "14000", "17000"]),
    q(_slot, "MCQ", "A and B are two railway stations 90 km apart. A train leaves A at 9:00 am, heading towards B at a speed of 40 km/hr. Another train leaves B at 10:30 am, heading towards A at a speed of 20 km/hr. The trains meet each other at:", options=["11:20 am", "11:00 am", "10:45 am", "11:45 am"]),
    q(_slot, "MCQ", "Vimla starts for office every day at 9 am and reaches exactly on time if she drives at her usual speed of 40 km/hr. She is late by 6 minutes if she drives at 35 km/hr. One day, she covers two-thirds of her distance to office in one-third of her usual time to reach office, and then stops for 8 minutes. The speed, in km/hr, at which she should drive the remaining distance to reach office exactly on time is:", options=["27", "28", "29", "26"]),
    q(_slot, "MCQ", "In a trapezium ABCD, AB ∥ DC , BC ⊥ DC and ∠BAD = 45◦ . If DC = 5 cm, BC = 4 cm, the area of the trapezium in sq. cm is:", options=["28", "30", "32", "34"]),
    q(_slot, "MCQ", "The points (2, 1) and (−3, −4) are opposite vertices of a parallelogram. If the other two vertices lie on the line x + 9y + c = 0, then c is:", options=["15", "13", "14", "12"]),
    q(_slot, "MCQ", "How many pairs (a, b) of positive integers are there such that a ≤ b and ab = 42017?", options=["2019", "2018", "2020", "2017"]),
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

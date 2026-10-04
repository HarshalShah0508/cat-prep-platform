"""Seed real CAT 2023 QA questions, generated from the official
solutions PDFs via pdftotext + pyq_qa_parser.py (automated text-layer
extraction, not LLM transcription).

Roughly half of CAT QA questions embed their math as a rendered image pdftotext can't recover (shows up as a run of blank space where an 
equation used to be, or an empty option) - those are intentionally omitted here, not fabricated. See stderr from the generation step for 
which question numbers were skipped per slot.

`correct_answer`/`explanation` are intentionally left blank for now - the answer key
is loaded separately once transcribed from the solutions PDFs.

Run with:
    python -m app.scripts.seed_cat_pyq_2023_qa
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023


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
    q(_slot, "MCQ", "If x and y are real numbers such that x2 + (x-2y-1)2 = 4y(x+y), here the value x-2y is?", options=["1", "2", "0", "-1"]),
    q(_slot, "MCQ", "In an examination, the average marks of 4 girls and 6 boys is 24 . Each of the girls has the same marks while each of the boys has the same marks. If the marks of any girl is at most double the marks of any boy, but not less than the marks of any boy, then the number of possible distinct integer values of the total marks of 2 girls and 6 boys is", options=["20", "22", "21", "19"]),
    q(_slot, "TITA", "The salaries of three friends Sita, Gita and Mita are initially in the ratio 5:6:7 respectively. In the first year, they get salary hikes of 20%, 25% and 20% , respectively. In the second year, Sita and Mita get salary hikes of 40% and 25% , respectively, and the salary of Gita becomes equal to the mean salary of the three friends. The salary hike of Gita in the second year is", options=None),
    q(_slot, "MCQ", "Brishti went on a 8-hour trip in a car, before the trip the car had traveled a total of x kms till then, where x is a whole number and is palindromic, At the end of his trip the car had had traveled a total of 26862 km. If Bristi never drove at more than 110 km/h, then the greatest possible average speed at which see dove is?", options=["90", "80", "110", "100"]),
    q(_slot, "MCQ", "A mixture P is formed by removing a certain amount of coffee from a coffee jar and replacing the same amount with cocoa powder and the same amount is again removed from P and replaced with the same amount of cocoa powder to form a mixture Q. If the ratio of coffee and cocoa in Q=16:9. Then the ratio of coca in with P:Q is?", options=["1:3", "4:9", "1:2", "5:9"]),
    q(_slot, "MCQ", "Anil invests Rs. 22000 for 6 years in a certain scheme with 4% interest per annum, compounded half-yearly. Sunil invests in the same scheme for 5 years, and then reinvests the entire amount received at the end of 5 years for one year at 10% simple interest. If the amounts received by both at the end of 6 years are same, then the initial investment made by Sunil, in rupees, is", options=["40008", "20008", "20808", "10808"]),
    q(_slot, "TITA", "The amount of job that Amal, Sunil and Kamal can individually do in a day, are in harmonic progression. Kamal takes twice as much time as Amal to do the same amount of job. If Amal and Sunil work for 4 days and 9 days, respectively, Kamal needs to work for 16 days to finish the remaining job. Then the number of days Sunil will take to finish the job working alone, is", options=None),
    q(_slot, "MCQ", "Arvind travels from town A to town B, and Surbhi from town B to town A, both starting at the same time along the same route. After meeting each other, Arvind takes 6 hours to reach town B while Surbhi takes 24 hours to reach town A. If Arvind travelled at a speed of 54 km/h, then the distance, in km, between town A and town B is [This question was asked as TITA]", options=["982 Kms", "970 Kms", "974 Kms", "972 Kms"]),
    q(_slot, "MCQ", "In a right-angled triangle Δ ABC , the altitude AB is 5 cm , and the base BC is 12 cm . P and Q are two points on BC such that the areas of ΔABP, ΔABQ , and Δ ABC are in arithmetic progression. If the area of Δ ABC is 1.5 times the area of Δ ABP , the length of PQ , in cm , is", options=["2", "1", "0", "3"]),
    q(_slot, "MCQ", "The number of all natural numbers up to 1000 with non-repeating digits is", options=["648", "585", "504", "738"]),
    q(_slot, "MCQ", "A lab experiment measures the number of organisms at 8 am every day. Starting with 2 organisms on the first day, the number of organisms on any day is equal to 3 more than twice the number on the previous day. If the number of organisms on the nth day exceeds one million, then the lowest possible value of n is", options=["15", "17", "19", "23"]),
]

# ============================================================ SLOT 2 ====
_slot = "slot2"
QUESTIONS += [
    q(_slot, "TITA", "The number of positive integers less than 50, having exactly two distinct factors other than 1 and itself, is", options=None),
    q(_slot, "MCQ", "Pipes A and C are fill pipes while Pipe B is a drain pipe of a tank. Pipe B empties the full tank in one hour less than the time taken by Pipe A to fill the empty tank. When pipes A, B and C are turned on together, the empty tank is filled in two hours. If pipes B and C are turned on together when the tank is empty and Pipe B is turned off after one hour, then Pipe C takes another one hour and 15 minutes to fill the remaining tank. If Pipe A can fill the empty tank in less than five hours, then the time taken, in minutes, by Pipe C to fill the empty tank is", options=["75", "120", "60", "90"]),
    q(_slot, "MCQ", "Anil borrows Rs 2 lakhs at an interest rate of 8% per annum, compounded half-yearly. He repays Rs 10320 at the end of the first year and closes the loan by paying the outstanding amount at the end of the third year. Then, the total interest, in rupees, paid over the three years is nearest to", options=["33130", "40991", "51311", "51311"]),
    q(_slot, "MCQ", "Ravi is driving at a speed of 40 km/h on a road. Vijay is 54 meters behind Ravi and driving in the same direction as Ravi. Ashok is driving along the same road from the opposite direction at a speed of 50 km/h and\n\nis 225 meters away from Ravi. The speed, in km/h, at which Vijay should drive so that all the three cross each other at the same time, is", options=["67.2", "64.4", "61.6", "58.8"]),
    q(_slot, "MCQ", "Minu purchases a pair of sunglasses at Rs.1000 and sells to Kanu at 20% profit. Then, Kanu sells it back to Minu at 20% loss. Finally, Minu sells the same pair of sunglasses to Tanu. If the total profit made by Minu from\n\nall her transactions is Rs.500, then the percentage of profit made by Minu when she sold the pair of sunglasses to Tanu is", options=["26%", "35.42%", "52%", "31.25%"]),
    q(_slot, "MCQ", "The price of a precious stone is directly proportional to the square of its weight. Sita has a precious stone weighing 18 units. If she breaks it into four pieces with each piece having distinct integer weight, then the difference between the highest and lowest possible values of the total price of the four pieces will be 288000. Then, the price of the original precious stone is", options=["1620000", "1296000", "1944000", "972000"]),
    q(_slot, "MCQ", "In a company, 20% of the employees work in the manufacturing department. If the total salary obtained by all the manufacturing employees is one-sixth of the total salary obtained by all the employees in the company, then the ratio of the average salary obtained by the\n\nmanufacturing employees to the average salary obtained by the non- manufacturing employees is", options=["6 : 5", "4 : 5", "5 : 4", "5 : 6"]),
    q(_slot, "MCQ", "A container has 40 liters of milk. Then, 4 liters are removed from the container and replaced with 4 liters of water. This process of replacing 4 liters of the liquid in the container with an equal volume of water is continued repeatedly. The smallest number of times of doing this process,\n\nafter which the volume of milk in the container becomes less than that of water, is", options=["5", "7", "4", "None of Above"]),
    q(_slot, "MCQ", "If a certain amount of money is divided equally among n persons, each one receives Rs 352 . However, if two persons receive Rs 506 each and the remaining amount is divided equally among the other persons, each of them receive less than or equal to Rs 330 . Then, the maximum possible value of n is", options=["15", "17", "16", "None of Above"]),
    q(_slot, "MCQ", "Jayant bought a certain number of white shirts at the rate of Rs 1000 per piece and a certain number of blue shirts at the rate of Rs 1125 per piece. For each shirt, he then set a fixed market price which was 25% higher than the average cost of all the shirts. He sold all the shirts at a discount of 10% and made a total profit of Rs 51000. If he bought both colors of shirts, then the maximum possible total number of shirts that he could have bought is", options=["395", "407", "413", "None of Above"]),
    q(_slot, "MCQ", "In a rectangle ABCD, AB = 9 cm and BC = 6 cm. P and Q are two points on BC such that the areas of the figures ABP, APQ, and AQCD are in geometric progression. If the area of the figure AQCD is four times the area of triangle ABP, then BP : PQ : QC is", options=["1 : 1 : 2", "1 : 2 : 1", "1 : 2 : 4", "2 : 4 : 1"]),
]

# ============================================================ SLOT 3 ====
_slot = "slot3"
QUESTIONS += [
    q(_slot, "MCQ", "The sum of the first two natural numbers, each having 15 factors (including 1 and the number itself), is", options=["348", "412", "468", "None of Above"]),
    q(_slot, "MCQ", "A merchant purchases a cloth at a rate of Rs. 100 per meter and receives 5 cm length of cloth free for every 100 cm length of cloth purchased by him. He sells the same cloth at a rate of Rs.110 per meter but cheats his\n\ncustomers by giving 95 cm length of cloth for every 100 cm length of cloth purchased by the customers. If the merchant provides a 5% discount, the resulting profit earned by him is", options=["9.7%", "16%", "4.2%", "15.5%"]),
    q(_slot, "MCQ", "There are three persons A B, and C in a room. If a person D joins the room, the average weight of the persons in the room reduces by x kg . Instead of D , if person E joins the room, the average weight of the persons in the room increases by 2 kg x . If the weight of E is 12 kg more than that of D , then the value of x is", options=["1.5", "0.5", "1", "2"]),
    q(_slot, "TITA", "In 2021, the population was 100000. In 2022 it is decreased by x%. In 2023, it will increase by y%. The population in 2023 is more than that of\n\n2021 and difference between x and y is 10. Minimum population in 2021 was?", options=None),
    q(_slot, "MCQ", "Anil mixes cocoa with sugar in the ratio 3: 2 to prepare mixture A , and coffee with sugar in the ratio 7: 3 to prepare mixture B . He combines mixtures A and B in the ratio 2: 3 to make a new mixture C . If he mixes C with an equal amount of milk to make a drink, then the percentage of sugar in this drink will be", options=["16", "24", "17", "21"]),
    q(_slot, "MCQ", "Rahul, Rakshita and Gurmeet, working together, would have taken more than 7 days to finish a job. On the other hand, Rahul and Gurmeet, working together would have taken less than 15 days to finish the job. However, they all worked together for 6 days, followed by Rakshita, who worked alone for 3 more days to finish the job. If Rakshita had worked alone on the job then the number of days she would have taken to finish the job, cannot be", options=["16", "21", "17", "20"]),
    q(_slot, "MCQ", "The number of coins collected per week by two coin-collectors A and B are in the ratio 3 : 4. If the total number of coins collected by A in 5 weeks is a multiple of 7, and the total number of coins collected by B in 3 weeks is a multiple of 24, then the minimum possible number of coins collected by A in one week is", options=["20", "42", "66", "None of Above"]),
    q(_slot, "MCQ", "Gautam and Suhani, working together, can finish a job in 20 days. If Gautam does only 60% of his usual work on a day, Suhani must do 150% of her usual work on that day to exactly make up for it. Then, the number of days required by the faster worker to complete the job working alone is", options=["30", "36", "70", "None of Above"]),
    q(_slot, "MCQ", "A fruit seller has a stock of mangoes, bananas and apples with at least one fruit of each type. At the beginning of a day, the number of mangoes make up 40% of his stock. That day, he sells half of the mangoes, 96 bananas and 40% of the apples. At the end of the day, he ends up selling 50% of the fruits. The smallest possible total number of fruits in the stock at the beginning of the day is", options=["100", "240", "340", "None of Above"]),
    q(_slot, "MCQ", "In a regular polygon, any interior angle exceeds the exterior angle by 120 degrees. Then, the number of diagonals of this polygon is", options=["30", "54", "64", "None of Above"]),
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

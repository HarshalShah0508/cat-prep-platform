"""Backfill correct_answer/explanation for CAT 2023 QA Slot 2, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF (resolved via
the printed option letter, which is more reliable than this paper's often-
garbled solution prose - e.g. Q13's solution text says "4:15" but the
actual lettered option it selects reads "4 : 5"); explanations are rewritten
in plain language, not copied verbatim.

Run with:
    python -m app.scripts.backfill_qa_2023_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("The number of positive integers less than 50, having exactly two distinct factors other than 1 and itself, is", "15", "Numbers with exactly two distinct factors besides 1 and itself are either cubes of a prime (2 such cubes under 50) or products of two distinct primes (13 such products under 50) - 15 numbers in total."),
    ("Pipes A and C are fill pipes while Pipe B is a drain pipe of a tank. Pipe B empties the full tank in one hour less than the time taken by Pipe A to fill the empty tank. When pipes A, B and C are turned on together, the empty tank is filled in two hours. If pipes B and C are turned on together when the tank is empty and Pipe B is turned off after one hour, then Pipe C takes another one hour and 15 minutes to fill the remaining tank. If Pipe A can fill the empty tank in less than five hours, then the time taken, in minutes, by Pipe C to fill the empty tank is", "90", "With pipe A filling, B draining, and C filling, setting up the \"all three open, fills in 2 hours\" equation alongside the \"B for 1 hour, C for 2.25 hours\" scenario and solving the system gives pipe C's fill time as 90 minutes."),
    ("Anil borrows Rs 2 lakhs at an interest rate of 8% per annum, compounded half-yearly. He repays Rs 10320 at the end of the first year and closes the loan by paying the outstanding amount at the end of the third year. Then, the total interest, in rupees, paid over the three years is nearest to", "51311", "The loan grows to ₹216,320 after year one (8% compounded half-yearly), then Anil's ₹10,320 repayment leaves ₹206,000 outstanding. Compounding that balance for two more years gives a final amount of about ₹240,991 - a total interest of ₹51,311 across all three years."),
    ("Ravi is driving at a speed of 40 km/h on a road. Vijay is 54 meters behind Ravi and driving in the same direction as Ravi. Ashok is driving along the same road from the opposite direction at a speed of 50 km/h and\n\nis 225 meters away from Ravi. The speed, in km/h, at which Vijay should drive so that all the three cross each other at the same time, is", "61.6", "Ravi and Ashok, 225 m apart and closing at a combined 25 m/s, meet in 9 seconds. In that time Ravi covers enough ground that Vijay - starting 54 m behind Ravi - must match Ravi's total distance, which converts to a speed of 61.6 km/h."),
    ("Minu purchases a pair of sunglasses at Rs.1000 and sells to Kanu at 20% profit. Then, Kanu sells it back to Minu at 20% loss. Finally, Minu sells the same pair of sunglasses to Tanu. If the total profit made by Minu from\n\nall her transactions is Rs.500, then the percentage of profit made by Minu when she sold the pair of sunglasses to Tanu is", "31.25%", "Minu buys for ₹1000, sells to Kanu for ₹1200 (20% profit = ₹200 banked), then buys back from Kanu at a 20% loss on ₹1200, i.e. ₹960. To hit her overall ₹500 profit target, she needs ₹300 more from the final sale, which on a ₹960 cost works out to a 31.25% profit margin."),
    ("The price of a precious stone is directly proportional to the square of its weight. Sita has a precious stone weighing 18 units. If she breaks it into four pieces with each piece having distinct integer weight, then the difference between the highest and lowest possible values of the total price of the four pieces will be 288000. Then, the price of the original precious stone is", "1296000", "With price proportional to weight², comparing the total value of the four broken pieces when their weights are close together (3,4,5,6) versus spread apart (1,2,3,12) gives a value difference of 288,000, which pins down the original stone's value at ₹12,96,000."),
    ("In a company, 20% of the employees work in the manufacturing department. If the total salary obtained by all the manufacturing employees is one-sixth of the total salary obtained by all the employees in the company, then the ratio of the average salary obtained by the\n\nmanufacturing employees to the average salary obtained by the non- manufacturing employees is", "4 : 5", "With manufacturing (20% of staff) earning one-sixth of total payroll, computing each department's average salary from these proportions and comparing them gives a manufacturing-to-non-manufacturing average salary ratio of 4:5."),
    ("A container has 40 liters of milk. Then, 4 liters are removed from the container and replaced with 4 liters of water. This process of replacing 4 liters of the liquid in the container with an equal volume of water is continued repeatedly. The smallest number of times of doing this process,\n\nafter which the volume of milk in the container becomes less than that of water, is", "7", "Each 4-liter replacement out of 40 liters multiplies the milk concentration by 0.9. Finding the smallest number of repetitions for 0.9ⁿ to drop below 50% (via logarithms) gives n = 7."),
    ("If a certain amount of money is divided equally among n persons, each one receives Rs 352 . However, if two persons receive Rs 506 each and the remaining amount is divided equally among the other persons, each of them receive less than or equal to Rs 330 . Then, the maximum possible value of n is", "16", "If the total amount divided among n people gives ₹352 each, but reserving ₹506 for two people and splitting the rest among the remaining (n−2) caps each share at ₹330, solving the resulting inequality shows the largest possible n is 16."),
    ("Jayant bought a certain number of white shirts at the rate of Rs 1000 per piece and a certain number of blue shirts at the rate of Rs 1125 per piece. For each shirt, he then set a fixed market price which was 25% higher than the average cost of all the shirts. He sold all the shirts at a discount of 10% and made a total profit of Rs 51000. If he bought both colors of shirts, then the maximum possible total number of shirts that he could have bought is", "407", "With the selling price set 25% above the blended average cost and total profit fixed at ₹51,000, maximizing the total shirt count (by minimizing the blue-shirt count consistent with the integer constraints) gives a maximum of 407 shirts."),
    ("In a rectangle ABCD, AB = 9 cm and BC = 6 cm. P and Q are two points on BC such that the areas of the figures ABP, APQ, and AQCD are in geometric progression. If the area of the figure AQCD is four times the area of triangle ABP, then BP : PQ : QC is", "2 : 4 : 1", "With the three regions' areas in geometric progression (k, 2k, 4k) and a line drawn from A to C to relate them to triangle areas, working out the proportional relationship between BP, PQ, and QC along BC gives a ratio of 2:4:1."),
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

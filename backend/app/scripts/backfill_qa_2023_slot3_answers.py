"""Backfill correct_answer/explanation for CAT 2023 QA Slot 3, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF (resolved via
the printed option letter where available); explanations are rewritten in
plain language, not copied verbatim.

Run with:
    python -m app.scripts.backfill_qa_2023_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("The sum of the first two natural numbers, each having 15 factors (including 1 and the number itself), is", "468", "A number has 15 factors when its prime factorization exponents multiply (after adding 1 to each) to 15 - either p¹⁴ or p²q⁴ or p⁴q² for distinct primes p, q. Checking the smallest two numbers of this form and adding them gives 468."),
    ("A merchant purchases a cloth at a rate of Rs. 100 per meter and receives 5 cm length of cloth free for every 100 cm length of cloth purchased by him. He sells the same cloth at a rate of Rs.110 per meter but cheats his\n\ncustomers by giving 95 cm length of cloth for every 100 cm length of cloth purchased by the customers. If the merchant provides a 5% discount, the resulting profit earned by him is", "15.5%", "Getting 105 cm for every 100 cm paid drops the effective cost per cm to about ₹0.952, while shortchanging customers on the sell side (95 cm per 100 cm charged) and then applying a 5% discount pushes the effective selling price to about ₹1.10 per cm - a profit margin of roughly 15.5%."),
    ("There are three persons A B, and C in a room. If a person D joins the room, the average weight of the persons in the room reduces by x kg . Instead of D , if person E joins the room, the average weight of the persons in the room increases by 2 kg x . If the weight of E is 12 kg more than that of D , then the value of x is", "1", "Setting up the average-weight-change equations for D joining (average drops by x) and E joining (average rises by y, with y=2x given) and equating the resulting expressions for the combined weight of A, B, C shows x = 1."),
    ("In 2021, the population was 100000. In 2022 it is decreased by x%. In 2023, it will increase by y%. The population in 2023 is more than that of\n\n2021 and difference between x and y is 10. Minimum population in 2021 was?", "73000", "With population falling by y% then rising by x% (x−y=10) and the 2022 figure exceeding the 2020 one, maximizing y within that constraint gives y=27, making the 2021 population 100000×(100−27)/100 = 73000."),
    ("Anil mixes cocoa with sugar in the ratio 3: 2 to prepare mixture A , and coffee with sugar in the ratio 7: 3 to prepare mixture B . He combines mixtures A and B in the ratio 2: 3 to make a new mixture C . If he mixes C with an equal amount of milk to make a drink, then the percentage of sugar in this drink will be", "17", "Mixing 200 ml of mixture A (3:2 cocoa:sugar) with 300 ml of mixture B (7:3 coffee:sugar) gives a combined sugar amount; diluting that further with an equal volume of milk brings the final sugar percentage down to 17%."),
    ("Rahul, Rakshita and Gurmeet, working together, would have taken more than 7 days to finish a job. On the other hand, Rahul and Gurmeet, working together would have taken less than 15 days to finish the job. However, they all worked together for 6 days, followed by Rakshita, who worked alone for 3 more days to finish the job. If Rakshita had worked alone on the job then the number of days she would have taken to finish the job, cannot be", "21", "Working together for 6 days then Rakshita finishing alone for 3 more days completes the job, while the given constraints bound how long the three (or just Rahul and Gurmeet) would take together. Combining these constraints pins Rakshita's solo time at 21 days."),
    ("The number of coins collected per week by two coin-collectors A and B are in the ratio 3 : 4. If the total number of coins collected by A in 5 weeks is a multiple of 7, and the total number of coins collected by B in 3 weeks is a multiple of 24, then the minimum possible number of coins collected by A in one week is", "42", "With A and B's weekly coin counts in ratio 3:4, A's 5-week total must be divisible by 7 and B's 3-week total by 24. Testing multiples that satisfy both conditions simultaneously, the smallest valid weekly count for A is 42 coins."),
    ("Gautam and Suhani, working together, can finish a job in 20 days. If Gautam does only 60% of his usual work on a day, Suhani must do 150% of her usual work on that day to exactly make up for it. Then, the number of days required by the faster worker to complete the job working alone is", "36", "Comparing the combined one-day work rate at normal effort (finishing in 20 days) against the scenario where Gautam works at 60% and Suhani at 150% gives a relationship between their individual efficiencies. Solving shows Gautam alone would take 36 days."),
    ("A fruit seller has a stock of mangoes, bananas and apples with at least one fruit of each type. At the beginning of a day, the number of mangoes make up 40% of his stock. That day, he sells half of the mangoes, 96 bananas and 40% of the apples. At the end of the day, he ends up selling 50% of the fruits. The smallest possible total number of fruits in the stock at the beginning of the day is", "340", "With mango, banana, and apple stock tied together by given ratios and a fraction of the total needing to divide evenly, the smallest total stock satisfying both the \"multiple of 3\" and \"multiple of 5\" conditions leads to an initial total of 340 fruits."),
    ("In a regular polygon, any interior angle exceeds the exterior angle by 120 degrees. Then, the number of diagonals of this polygon is", "54", "If the interior angle exceeds the exterior angle by 120°, and interior+exterior always sum to 180° per vertex, each exterior angle is 30° - meaning the polygon has 360/30 = 12 sides. A 12-sided polygon has 12×9/2 = 54 diagonals."),
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

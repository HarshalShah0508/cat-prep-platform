"""Backfill correct_answer/explanation for CAT 2024 QA Slot 1, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF (resolved via
the printed option letter, which is more reliable than this paper's often-
garbled solution prose); explanations are rewritten in plain language and
independently re-verified, not copied verbatim.

Run with:
    python -m app.scripts.backfill_qa_2024_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("A shop wants to sell a certain quantity (in kg) of grains. It sells half the quantity and an additional 3 kg of these grains to the first customer. Then, it sells half of the remaining quantity and an additional 3 kg of these grains to the second customer. Finally, when the shop sells half of the remaining quantity and an additional 3 kg of these grains to the third customer, there are no grains left. The initial quantity, in kg, of grains is", "42", "Working backward from zero grains left after the third sale (each sale takes half the remaining plus 3 kg), the remaining amount before each sale was 6, then 18, then 42 kg - so the shop started with 42 kg."),
    ("The selling price of a product is fixed to ensure 40% profit. If the product had cost 40% less and had been sold for 5 rupees less, then the resulting profit would have been 50%. The original selling price, in rupees, of the product is", "14", "With cost price C and a 40% profit giving selling price 1.4C, reducing the cost by 40% (to 0.6C) and the selling price by ₹5 while still making 50% profit sets up an equation that solves to an original selling price of ₹14."),
    ("A glass is filled with milk. Two-thirds of its content is poured out and replaced with water. If this process of pouring out two-thirds the content and replacing with water is repeated three more times, then the final ratio of milk to water in the glass, is", "1:80", "Each round of pouring out two-thirds and refilling with water leaves 1/3 of the milk behind. After four rounds, the milk fraction is (1/3)⁴ = 1/81, making the milk-to-water ratio 1:80."),
    ("Consider two sets A = {2, 3, 5, 7, 11, 13} and B = {1, 8, 27}. Let f be a function from A to B such that for every element b in B, there is at least one element a in A such that f(a) = b. Then, the total number of such functions f is", "540", "Counting onto (surjective) functions from a 6-element set to a 3-element set uses the formula with Stirling numbers of the second kind: 3! × S(6,3) = 6 × 90 = 540."),
    ("In September, the incomes of Kamal, Amal and Vimal are in the ratio 8 ∶ 6 ∶ 5. They rent a house together, and Kamal pays 15%, Amal pays 12% and Vimal pays 18% of their respective incomes to cover the total house rent in that month. In October, the house rent remains unchanged while their incomes increase by 10%, 12% and 15%, respectively. In October, the percentage of their total income that will be paid as house rent, is nearest to", "13.26", "Setting up each person's rent contribution as a percentage of their September income, then applying October's income increases to each person separately and recomputing the combined rent-to-income percentage, gives approximately 13.26%."),
    ("Two places A and B are 45 kms apart and connected by a straight road. Anil goes from A to B while Sunil goes from B to A. Starting at the same time, they cross each other in exactly 1 hour 30 minutes. If Anil reaches B exactly 1 hour 15 minutes after Sunil reaches A, the speed of Anil, in km per hour, is", "12", "With Anil and Sunil together covering the full 45 km in 1.5 hours before crossing, and Anil needing 1 hour 15 minutes longer than Sunil to finish after crossing, solving the resulting system of speed equations gives Anil's speed as 12 km/hr."),
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

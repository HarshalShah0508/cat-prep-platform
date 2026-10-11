"""Add the 2 CAT 2021 DILR Slot 1 questions missing from the DB (18/20
loaded): the 4th question of the smoothie-scheduling set, and the 3rd
question of the sales-subcategory set. Found by diffing against the
solutions PDF text and a web search cross-check for the one question the
solutions PDF dropped entirely.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot1_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SMOOTHIE_PASSAGE = (
    "Ganga, Kaveri, and Narmada are three women who buy four raw materials (Mango, Apple, Banana and "
    "Milk) and sell five finished products (Mango smoothie, Apple smoothie, Banana smoothie, Mixed fruit "
    "smoothie and Fruit salad). One unit of a finished product requires one unit of each of the raw "
    "materials: Mango smoothie (Mango, Milk), Apple smoothie (Apple, Milk), Banana smoothie (Banana, "
    "Milk), Mixed fruit smoothie (Mango, Apple, Banana, Milk), Fruit salad (Mango, Apple, Banana). One "
    "unit of milk, mango, apple, and banana cost ₹5, ₹3, ₹2, and ₹1 respectively. Each unit of a finished "
    "product is sold for a profit equal to two times the number of raw materials used to make that "
    "product. Leftover raw materials are sold during the last business hour of the day for a loss of ₹1 "
    "per unit. The amount, in rupees, received from sales (revenue) for each woman in each of the four "
    "business hours: Hour 1 - Ganga 23, Kaveri 19, Narmada 31; Hour 2 - Ganga 21, Kaveri 22, Narmada 21; "
    "Hour 3 - Ganga 29, Kaveri 30, Narmada 29; Hour 4 (last hour) - Ganga 30, Kaveri 27, Narmada 22.\n\n"
    "The following additional facts are known:\n"
    "1. No one except possibly Ganga sold any Mango smoothie.\n"
    "2. Each woman sold either zero or one unit of any single finished product in any hour.\n"
    "3. Each woman had exactly one unit each of two different raw materials as leftovers.\n"
    "4. No one had any banana leftover."
)

SALES_PASSAGE = (
    "The horizontal bars in the above diagram represent 2020 aggregate sales (in ₹ million) of a company "
    "for the different subcategories of its products. The top four product subcategories (Bookcases, "
    "Chairs, Furnishings, Tables) belong to the furniture product category; the bottom four product "
    "subcategories (Accessories, Copiers, Machines, Phones) belong to the technology product category; "
    "while all other product subcategories belong to the office supply product category. For each of the "
    "product subcategories, there is a vertical line indicating the sales of the corresponding "
    "subcategory in 2019."
)

ROWS = [
    dict(
        group_id="cat2021_dilr_slot1_set3",
        question_type="TITA",
        passage_text=SMOOTHIE_PASSAGE,
        question_text="If it is known that three leftover units of mangoes were sold during the last business hour, how many apple smoothies were sold during the day?",
        options=None,
        correct_answer="6",
        explanation="With 3 leftover mango units sold at Hour 4, working back through the revenue figures and the raw-material cost/profit structure for each woman pins down the day's product mix, giving a total of 6 apple smoothies sold.",
    ),
    dict(
        group_id="cat2021_dilr_slot1_set4",
        question_type="TITA",
        passage_text=SALES_PASSAGE,
        question_text="How many subcategories had sales of ₹4 million or more in 2019 and registered an increase in sales in excess of 25% in 2020?",
        options=None,
        correct_answer="1",
        explanation="Checking each subcategory against both thresholds (≥₹4 million in 2019, >25% increase into 2020) from the chart, only Phones (≈₹6.0M in 2019, rising to ≈₹7.7M, a ≈28% increase) satisfies both conditions.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        inserted = 0
        for row in ROWS:
            existing = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.section == "DILR",
                    CatQuestion.source_year == 2021,
                    CatQuestion.source_slot == "slot1",
                    CatQuestion.question_text == row["question_text"],
                )
                .first()
            )
            if existing is not None:
                print(f"Already present as id={existing.id}, skipping: {row['question_text'][:50]!r}")
                continue
            q = CatQuestion(
                section="DILR",
                question_type=row["question_type"],
                topic="Logical Reasoning",
                difficulty="hard",
                source="pyq",
                source_year=2021,
                source_slot="slot1",
                group_id=row["group_id"],
                passage_text=row["passage_text"],
                question_text=row["question_text"],
                options=row["options"],
                correct_answer=row["correct_answer"],
                explanation=row["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted id={q.id}: {row['question_text'][:50]!r}")
            inserted += 1
        db.commit()
        print(f"Inserted {inserted} CAT 2021 DILR Slot 1 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

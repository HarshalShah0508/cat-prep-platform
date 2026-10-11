"""Add the 4 CAT 2021 DILR Slot 2 questions missing from the DB (16/20
loaded) - an entire set ("order booking/dispatch bar chart") that was never
loaded at all. Solved from the solutions PDF text (Q1, Q3, Q4) and a web
search cross-check for Q2, which the solutions PDF left unsolved.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot2_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

PASSAGE = (
    "The different bars in the diagram provide information about different orders in various "
    "categories (Art, Binders, etc.) that were booked in the first two weeks of September for a "
    "store's client. The colour and pattern of a bar denotes the ship mode (First Class / Second "
    "Class / Standard Class). The left endpoint of a bar indicates the booking day of the order, "
    "while the right endpoint indicates the dispatch day. The difference between the dispatch day "
    "and the booking day (in days) is called the processing time of the order. For the same "
    "category, an order is considered for booking only after the previous order of the same "
    "category is dispatched. No two consecutive orders of the same category had identical ship "
    "mode during this period.\n\n"
    "For example, there were only two orders in the furnishing category during this period. The "
    "first was shipped Second Class, booked Sep 1 and dispatched Sep 5. The second was shipped "
    "Standard Class, booked Sep 5 and dispatched Sep 12 - processing times of 4 and 7 days "
    "respectively."
)

ROWS = [
    dict(
        question_type="TITA",
        question_text="How many days between Sep 1 and Sep 14 (both inclusive) had no booking from this client considering all the above categories?",
        options=None,
        correct_answer="1",
        explanation="Listing the booking (left-endpoint) days across all categories from Sep 1 to Sep 14 covers every day except Sep 12, which has no bookings - so the answer is 1 day.",
    ),
    dict(
        question_type="TITA",
        question_text="What was the average processing time of all orders in the categories which had only one type of ship mode?",
        options=None,
        correct_answer="11",
        explanation="Only two categories (Accessories and Envelopes) used a single ship mode throughout the period, with processing times of 18 and 4 days respectively, averaging (18+4)/2=11 days.",
    ),
    dict(
        question_type="MCQ",
        question_text="The sequence of categories - Art, Binders, Paper, and Phones - in decreasing order of average processing time of their orders in this period is:",
        options=["Art, Binders, Paper, Phones", "Phones, Art, Binders, Paper", "Phones, Binders, Art, Paper", "Paper, Binders, Art, Phones"],
        correct_answer="Art, Binders, Paper, Phones",
        explanation="Reading each category's order processing times off the chart and averaging them, Art has the highest average, followed by Binders, then Paper, then Phones.",
    ),
    dict(
        question_type="MCQ",
        question_text="Approximately what percentage of orders had a processing time of one day during the period Sep 1 to Sep 22 (both dates inclusive)?",
        options=["22%", "16%", "20%", "25%"],
        correct_answer="20%",
        explanation="Counting the orders with exactly a 1-day gap between booking and dispatch across all categories in this period, and dividing by the total number of orders, gives approximately 20%.",
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
                    CatQuestion.source_slot == "slot2",
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
                source_slot="slot2",
                group_id="cat2021_dilr_slot2_set1",
                passage_text=PASSAGE,
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
        print(f"Inserted {inserted} CAT 2021 DILR Slot 2 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

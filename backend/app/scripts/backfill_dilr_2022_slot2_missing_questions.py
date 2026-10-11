"""Add the 5 CAT 2022 DILR Slot 2 questions missing from the DB (15/20
loaded) - an entire set ("widget supplier routing") that was never loaded
at all. Found via the solutions PDF, which had unusually clean, internally
consistent reasoning for this particular set (distances and demand figures
recoverable directly from the worked solutions, even though the source
figure itself is an image).

Run with:
    python -m app.scripts.backfill_dilr_2022_slot2_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

PASSAGE = (
    "Every day a widget supplier supplies widgets from the warehouse (W) to four locations - "
    "Ahmednagar (A), Bikrampore (B), Chitrachak (C), and Deccan Park (D). The daily demand for "
    "widgets in each location is uncertain and independent of the others. Each location has two "
    "possible demand levels with given probabilities - for example, there is a 40% chance that "
    "Ahmednagar's demand is 50 units and a 60% chance it is 70 units (similarly, C has demand "
    "70 or 100 units, D has demand 30 or 50 units, and B has demand 40 or 60 units, each with its "
    "own probabilities shown in the figure). Roads are two-way with given distances: Warehouse-A "
    "5 km, Warehouse-C 12 km, A-C 17 km, C-B 4 km, B-D 12 km, A-B 6 km, and a Warehouse route "
    "connecting D and A (via the warehouse, 7 km).\n\n"
    "Every day, once the supplier learns the day's demand values, they plan a route starting from "
    "the warehouse and visiting all four locations exactly once, in decreasing order of demand "
    "(ties broken by visiting the nearer location first). Between any two locations, the supplier "
    "takes the direct path if available, or the path via the warehouse, whichever is shorter."
)

ROWS = [
    dict(
        question_type="TITA",
        question_text="If the last location visited is Ahmednagar, then what is the total distance covered in the route (in km)?",
        options=None,
        correct_answer="35",
        explanation="With A visited last, its demand must be the lowest (50 units), forcing the visiting order C-B-D-A. Distances: Warehouse-C (12) + C-B (4) + B-D (12) + D-A via warehouse (7) = 35 km.",
    ),
    dict(
        question_type="TITA",
        question_text="If the total number of widgets delivered in a day is 250 units, then what is the total distance covered in the route (in km)?",
        options=None,
        correct_answer="38",
        explanation="Matching demand combinations that sum to 250 units (A=70, C=70, B=60, D=50) gives the visiting order A-C-B-D. Distances: Warehouse-A (5) + A-C (17) + C-B (4) + B-D (12) = 38 km.",
    ),
    dict(
        question_type="MCQ",
        question_text="What is the chance that the total number of widgets delivered in a day is 260 units and the route ends at Bikrampore?",
        options=["7.56%", "17.64%", "10.80%", "33.33%"],
        correct_answer="7.56%",
        explanation="The only demand combination totalling 260 with B visited last is C=100, A=70, D=50, B=40. Multiplying their individual probabilities (0.7 x 0.6 x 0.6 x 0.3) gives 0.0756 = 7.56%.",
    ),
    dict(
        question_type="MCQ",
        question_text="If the first location visited from the warehouse is Ahmednagar, then what is the chance that the total distance covered in the route is 40 km?",
        options=["18%", "5.4%", "30%", "3.24%"],
        correct_answer="18%",
        explanation="With A visited first, A and C must both be at their higher demand (70 each), fixing the first two legs at 22 km (Warehouse-A-C). Reaching exactly 40 km total requires D=50 and B=40, whose probabilities (0.6 x 0.3) multiply to 18%.",
    ),
    dict(
        question_type="MCQ",
        question_text="If Ahmednagar is not the first location to be visited in a route and the total route distance is 29 km, then which of the following is a possible number of widgets delivered on that day?",
        options=["210", "220", "200", "250"],
        correct_answer="210",
        explanation="With A excluded from being first, C must be first, giving the order C-B-A-D with a 29 km route. The matching demand combination is C=70, B=60, A=50, D=30, totalling 210 units.",
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
                    CatQuestion.source_year == 2022,
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
                source_year=2022,
                source_slot="slot2",
                group_id="cat2022_dilr_slot2_set2",
                passage_text=PASSAGE,
                question_text=row["question_text"],
                options=row.get("options"),
                correct_answer=row["correct_answer"],
                explanation=row["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted id={q.id}: {row['question_text'][:50]!r}")
            inserted += 1
        db.commit()
        print(f"Inserted {inserted} CAT 2022 DILR Slot 2 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

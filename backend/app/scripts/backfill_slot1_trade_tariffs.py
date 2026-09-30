"""One-off backfill: adds the CAT 2025 Slot 1 DILR trade-tariff set (Q10-13,
group cat2025_slot1_set3) that was originally skipped because its source PDF
had a placeholder image instead of the real radar/bar charts. The user later
supplied the actual chart images; values below are cross-checked against the
official solutions PDF (exact where the solution states a plain number,
"~" where the solution itself only approximates from the chart).

Idempotent: skips if the group already exists. Safe to re-run.

Run with:
    python -m app.scripts.backfill_slot1_trade_tariffs
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

GROUP_ID = "cat2025_slot1_set3"

PASSAGE = (
    "Five countries engage in trade with each other. Each country levies import "
    "tariffs on the other countries. The import tariff levied by Country X on "
    "Country Y is calculated by multiplying the corresponding tariff percentage "
    "with the total imports of Country X from Country Y. The radar chart below "
    "depicts different import tariff percentages charged by each of the five "
    "countries on the others. For example, US (the blue line in the chart) "
    "charges 20%, 40%, 30%, and 30% import tariff percentages on imports from "
    "France, India, Japan, and UK, respectively. The bar chart depicts the "
    "import tariffs levied by each country on other countries. For example, US "
    "charged import tariff of 3 billion USD on UK.\n\n"
    "Assume that imports from one country to another equal the exports from "
    "the latter to the former. The trade surplus of Country X with Country Y "
    "is defined as follows: Trade surplus = Exports from Country X to Country "
    "Y - Imports to Country X from Country Y. A negative trade surplus is "
    "called a trade deficit.\n\n"
    "Import tariff percentage charged by row country on column country "
    "(from the radar chart; ~ marks a value the original chart only allows "
    "an approximate read of):\n\n"
    "| Charges -> | US | France | India | Japan | UK |\n"
    "|---|---|---|---|---|---|\n"
    "| US | - | 20% | 40% | 30% | 30% |\n"
    "| France | ~35% | - | 40% | ~20% | ~40% |\n"
    "| India | ~40% | ~45% | - | 50% | ~20% |\n"
    "| Japan | ~40% | 40% | ~35% | - | ~35% |\n"
    "| UK | ~20% | ~35% | 20% | 30% | - |\n\n"
    "Import tariff amount in Billion USD, charged by row country on column "
    "country (from the bar chart; same ~ convention):\n\n"
    "| Charges -> | US | France | India | Japan | UK |\n"
    "|---|---|---|---|---|---|\n"
    "| US | - | 6 | ~4.5 | ~7 | 3 |\n"
    "| France | 5 | - | 5 | ~4 | ~4.5 |\n"
    "| India | ~9 | ~5 | - | 3.5 | ~6 |\n"
    "| Japan | ~4 | 3 | ~8 | - | ~3 |\n"
    "| UK | 3 | ~4 | 3 | 6 | - |"
)

QUESTIONS = [
    {
        "question_text": "How much is Japan's export to India worth?",
        "question_type": "MCQ",
        "options": ["8.5 Billion USD", "16.0 Billion USD", "7.0 Billion USD", "1.75 Billion USD"],
    },
    {
        "question_text": (
            "Which among the following is the highest?\n"
            "1. Exports by Japan to UK\n"
            "2. Imports by US from France\n"
            "3. Exports by France to Japan\n"
            "4. Imports by France from India"
        ),
        "question_type": "MCQ",
        "options": [
            "Exports by Japan to UK",
            "Imports by US from France",
            "Exports by France to Japan",
            "Imports by France from India",
        ],
    },
    {
        "question_text": "What is the trade surplus/trade deficit of India with UK?",
        "question_type": "MCQ",
        "options": [
            "Surplus of 15.0 Billion USD",
            "Deficit of 15.0 Billion USD",
            "Surplus of 10.0 Billion USD",
            "Deficit of 10.0 Billion USD",
        ],
    },
    {
        "question_text": "Among France and UK, who has/have trade surplus(es) with US?",
        "question_type": "MCQ",
        "options": ["Neither France nor UK", "Both France and UK", "Only UK", "Only France"],
    },
]


def backfill() -> None:
    db = SessionLocal()
    try:
        existing = db.query(CatQuestion).filter(CatQuestion.group_id == GROUP_ID).count()
        if existing > 0:
            print(f"{GROUP_ID} already present ({existing} rows); skipping.")
            return

        for item in QUESTIONS:
            db.add(
                CatQuestion(
                    section="DILR",
                    question_type=item["question_type"],
                    topic="Trade Tariffs Radar+Bar Chart DI",
                    difficulty="hard",
                    source="pyq",
                    source_year=2025,
                    source_slot="slot1",
                    group_id=GROUP_ID,
                    passage_text=PASSAGE,
                    question_text=item["question_text"],
                    options=item["options"],
                    correct_answer=None,
                    explanation=None,
                    is_active=True,
                )
            )
        db.commit()
        print(f"Backfilled {len(QUESTIONS)} questions into {GROUP_ID}.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

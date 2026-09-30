"""One-off backfill: adds CAT 2025 Slot 2's two remaining DILR sets (research
papers Q10-13, sustainability index Q14-17) that were originally skipped
because their source PDF had placeholder images instead of the real charts.

The user supplied clear, precisely-readable chart images for both (two bar
charts for the research-papers set, a scatter plot for the sustainability
set), so - unlike the Slot 1/3 backfills - these values are direct reads,
not estimates. One internal consistency check passed: the "papers by
author" bar totals (5+8+12+10=35) exactly match the "papers by type" bar
totals weighted by co-author count (10x1 + 4x2 + 3x3 + 2x4 = 35).

Idempotent: skips a group if it already exists. Safe to re-run.

Run with:
    python -m app.scripts.backfill_slot2_charts
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

RESEARCH_GROUP_ID = "cat2025_slot2_set3"
SI_GROUP_ID = "cat2025_slot2_set4"

RESEARCH_PASSAGE = (
    "The following charts depict details of research papers written by four "
    "authors, Arman, Brajen, Chintan, and Devon. The papers were of four "
    "types, single-author, two-author, three-author, and four-author, that "
    "is, written by one, two, three, or all four of these authors, "
    "respectively. No other authors were involved in writing these papers.\n\n"
    "The following additional facts are known.\n"
    "1. Each of the authors wrote at least one of each of the four types of "
    "papers.\n"
    "2. The four authors wrote different numbers of single-author papers.\n"
    "3. Both Chintan and Devon wrote more three-author papers than Brajen.\n"
    "4. The number of single-author and two-author papers written by Brajen "
    "were the same."
)

RESEARCH_CHART_DATA = [
    {
        "type": "bar",
        "title": "Number of papers by each author",
        "x_label": "Author",
        "y_label": "Number of papers",
        "categories": ["Arman", "Brajen", "Chintan", "Devon"],
        "values": [5, 8, 12, 10],
        "y_max": 14,
        "color": "#4338ca",
    },
    {
        "type": "bar",
        "title": "Number of papers by type",
        "x_label": "Paper type",
        "y_label": "Number of papers",
        "categories": ["Single-author", "Two-author", "Three-author", "Four-author"],
        "values": [10, 4, 3, 2],
        "y_max": 12,
        "color": "#0f9d8b",
    },
]

RESEARCH_QUESTIONS = [
    {
        "question_text": "What was the total number of two-author and three-author papers written by Brajen?",
        "question_type": "TITA",
        "options": None,
    },
    {
        "question_text": (
            "Which of the following statements is/are NECESSARILY true?\n"
            "i. Chintan wrote exactly three two-author papers.\n"
            "ii. Chintan wrote more single-author papers than Devon."
        ),
        "question_type": "MCQ",
        "options": ["Neither i nor ii", "Both i and ii", "Only i", "Only ii"],
    },
    {
        "question_text": (
            "Which of the following statements is/are NECESSARILY true?\n"
            "i. Arman wrote three-author papers only with Chintan and Devon.\n"
            "ii. Brajen wrote three-author papers only with Chintan and Devon."
        ),
        "question_type": "MCQ",
        "options": ["Only ii", "Neither i nor ii", "Both i and ii", "Only i"],
    },
    {
        "question_text": (
            "If Devon wrote more than one two-author papers, then how many "
            "two-author papers did Chintan write?"
        ),
        "question_type": "TITA",
        "options": None,
    },
]

SI_PASSAGE = (
    "The Sustainability Index (SI) of a country at a point in time is an "
    "integer between 1 and 100. This question is related to SI of six "
    "countries - A, B, C, D, E, and F - at three different points in time - "
    "2016, 2020, and 2024. The plot represents the exact changes in their "
    "SI, with X-coordinate representing % increase in 2020 from 2016, i.e., "
    "(SI in 2020 minus SI in 2016) / (SI in 2016), and Y-coordinate "
    "representing % increase in 2024 from 2020. At any point in time, the "
    "country with highest SI is ranked 1, while the country with the lowest "
    "SI is ranked 6.\n\n"
    "The following additional facts are known.\n"
    "1. In 2016, B, C, E, and A had ranks 1, 2, 3, and 4 respectively.\n"
    "2. F had lower SI than any other country in 2016, 2020, and 2024.\n"
    "3. In 2024, E was the only country with SI of 90.\n"
    "4. The range of SI of the six countries was 60 in 2016 as well as in "
    "2024."
)

SI_CHART_DATA = [
    {
        "type": "scatter",
        "title": "% change in Sustainability Index",
        "x_label": "% increase in index in 2020 from 2016",
        "y_label": "% increase in index in 2024 from 2020",
        "x_min": -40,
        "x_max": 100,
        "y_min": -30,
        "y_max": 60,
        "color": "#1e3a8a",
        "points": [
            {"label": "A", "x": 25, "y": 50},
            {"label": "B", "x": -25, "y": -25},
            {"label": "C", "x": -20, "y": 40},
            {"label": "D", "x": 100, "y": 20},
            {"label": "E", "x": 25, "y": 20},
            {"label": "F", "x": 100, "y": -25},
        ],
    }
]

SI_QUESTIONS = [
    {"question_text": "What was the SI of E in 2016?", "question_type": "TITA", "options": None},
    {"question_text": "What was the SI of F in 2020?", "question_type": "TITA", "options": None},
    {"question_text": "What was the SI of C in 2024?", "question_type": "TITA", "options": None},
    {
        "question_text": "What was the SI of B in 2024?",
        "question_type": "MCQ",
        "options": ["60", "45", "54", "80"],
    },
]


def _insert_group(db, group_id, topic, passage, chart_data, questions):
    existing = db.query(CatQuestion).filter(CatQuestion.group_id == group_id).count()
    if existing > 0:
        print(f"{group_id} already present ({existing} rows); skipping.")
        return

    for item in questions:
        db.add(
            CatQuestion(
                section="DILR",
                question_type=item["question_type"],
                topic=topic,
                difficulty="hard",
                source="pyq",
                source_year=2025,
                source_slot="slot2",
                group_id=group_id,
                passage_text=passage,
                chart_data=chart_data,
                question_text=item["question_text"],
                options=item["options"],
                correct_answer=None,
                explanation=None,
                is_active=True,
            )
        )
    print(f"Backfilled {len(questions)} questions into {group_id}.")


def backfill() -> None:
    db = SessionLocal()
    try:
        _insert_group(
            db,
            RESEARCH_GROUP_ID,
            "Research Papers by Author/Type Bar Chart DI",
            RESEARCH_PASSAGE,
            RESEARCH_CHART_DATA,
            RESEARCH_QUESTIONS,
        )
        _insert_group(
            db,
            SI_GROUP_ID,
            "Sustainability Index Scatter Plot DI",
            SI_PASSAGE,
            SI_CHART_DATA,
            SI_QUESTIONS,
        )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

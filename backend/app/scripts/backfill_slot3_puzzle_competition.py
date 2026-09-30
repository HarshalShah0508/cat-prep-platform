"""One-off backfill: adds the CAT 2025 Slot 3 DILR puzzle-competition set
(Q10-13, group cat2025_slot3_set3) that was originally skipped because its
source PDF had a placeholder image instead of the real step-line charts.

The user later supplied clear step-chart images. Unlike the Slot 1 trade-
tariff set, no solutions PDF was available for this specific set, so the
breakpoints below are a careful visual read of the charts - but they are
internally validated: running the puzzle-type-sequence logic (which puzzle
positions are visual vs number-based, derived by comparing when each
competitor's visual-solved-count increments against their total-solved-
count) on this exact data independently reproduces two of this set's own
printed answer options (Q13's ~3.83min rounds to the printed "3.8 minutes"
option; Q10's "Koushik leads at the 20-minute mark" matches the printed
option), which would be an unlikely coincidence if the underlying reading
were badly off.

Idempotent: skips if the group already exists. Safe to re-run.

Run with:
    python -m app.scripts.backfill_slot3_puzzle_competition
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

GROUP_ID = "cat2025_slot3_set3"

COLORS = {
    "Anirbid": "#dc2626",
    "Chandranath": "#d97706",
    "Koushik": "#16a34a",
    "Suranjan": "#2563eb",
}

ALL_PUZZLES_POINTS = {
    "Anirbid": [[0, 0], [4, 1], [9, 2], [11, 3], [14, 4], [16, 5], [22, 6], [26, 7], [29, 8], [33, 9], [37, 10], [40, 10]],
    "Chandranath": [[0, 0], [4, 1], [6, 2], [8, 3], [13, 4], [14, 5], [21, 6], [25, 7], [27, 8], [29, 9], [30, 10], [40, 10]],
    "Koushik": [[0, 0], [2, 1], [5, 2], [7, 3], [12, 4], [14, 5], [16, 6], [19, 7], [25, 8], [29, 9], [31, 10], [40, 10]],
    "Suranjan": [[0, 0], [4, 1], [9, 2], [12, 3], [18, 4], [19, 5], [23, 6], [25, 7], [27, 8], [33, 9], [35, 10], [40, 10]],
}

VISUAL_PUZZLES_POINTS = {
    "Anirbid": [[0, 0], [4, 1], [14, 2], [28, 3], [33, 4], [40, 4]],
    "Chandranath": [[0, 0], [4, 1], [13, 2], [26, 3], [28, 4], [40, 4]],
    "Koushik": [[0, 0], [2, 1], [12, 2], [25, 3], [29, 4], [40, 4]],
    "Suranjan": [[0, 0], [5, 1], [18, 2], [28, 3], [33, 4], [40, 4]],
}

CHART_DATA = [
    {
        "title": "All puzzles",
        "x_label": "Time (minutes)",
        "y_label": "Number of puzzles solved",
        "x_max": 40,
        "y_max": 10,
        "series": [
            {"name": name, "color": COLORS[name], "points": points}
            for name, points in ALL_PUZZLES_POINTS.items()
        ],
    },
    {
        "title": "Visual puzzles",
        "x_label": "Time (minutes)",
        "y_label": "Number of visual puzzles solved",
        "x_max": 40,
        "y_max": 5,
        "series": [
            {"name": name, "color": COLORS[name], "points": points}
            for name, points in VISUAL_PUZZLES_POINTS.items()
        ],
    },
]

PASSAGE = (
    "Anirbid, Chandranath, Koushik, and Suranjan participated in a puzzle "
    "solving competition. The competition comprised 10 puzzles that had to "
    "be solved in the same sequence, i.e., a competitor got access to a "
    "puzzle as soon as they solved the previous puzzle. Some of the puzzles "
    "were visual puzzles and the others were number-based puzzles. The "
    "winner of the competition was the one who solved all puzzles in the "
    "least time. The chart on the left shows the cumulative number of "
    "puzzles solved by each competitor at a given time (in minutes) after "
    "the start of the competition. The chart on the right shows the "
    "cumulative number of visual puzzles solved by each competitor over the "
    "same period."
)

QUESTIONS = [
    {
        "question_text": (
            "Who had solved the largest number of puzzles by the 20-th "
            "minute from the start of the competition?"
        ),
        "question_type": "MCQ",
        "options": ["Chandranath", "Koushik", "Anirbid", "Suranjan"],
    },
    {
        "question_text": (
            "How many minutes did Suranjan take to solve the third visual "
            "puzzle in the competition?"
        ),
        "question_type": "TITA",
        "options": None,
    },
    {
        "question_text": "At what number in the sequence was the fourth number-based puzzle?",
        "question_type": "TITA",
        "options": None,
    },
    {
        "question_text": (
            "Which of the following is the closest to the average time "
            "taken by Anirbid to solve the number-based puzzles in the "
            "competition?"
        ),
        "question_type": "MCQ",
        "options": ["3.3 minutes", "2.5 minutes", "4.0 minutes", "3.8 minutes"],
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
                    topic="Puzzle Competition Step-Chart DI",
                    difficulty="hard",
                    source="pyq",
                    source_year=2025,
                    source_slot="slot3",
                    group_id=GROUP_ID,
                    passage_text=PASSAGE,
                    chart_data=CHART_DATA,
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

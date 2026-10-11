"""Add the 5 CAT 2023 DILR Slot 3 questions missing from the DB (15/20
loaded) - an entire set ("police team patrol routes") that was never loaded
at all. Found via the solutions PDF, which gives a complete, internally
consistent team-movement table for this set.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot3_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

PASSAGE = (
    "Four teams of police patrol the streets of a city connecting six stations: A, B, C, D, E and "
    "F. The teams need 30 minutes to cross a street connecting one police station to another. All "
    "four teams start from Station A at 09:00 hrs and must return to Station A by 12:00 hrs. They "
    "can also pass via Station A at any point on their journeys.\n\n"
    "The following facts are known:\n"
    "1. None of the streets has more than one team traveling along it in any direction at any "
    "point in time.\n"
    "2. Teams 2 and 3 are the only ones in stations E and D respectively at 10:00 hrs.\n"
    "3. Teams 1 and 3 are the only ones in station E at 10:30 hrs.\n"
    "4. Teams 1 and 4 are the only ones in stations B and E respectively at 11:30 hrs.\n"
    "5. Team 1 and Team 4 are the only teams that patrol the street connecting stations A and E.\n"
    "6. Team 4 never passes through Stations B, D or F.\n\n"
    "(The resulting unique movement table: Team 1: A,B,A,E,A,B,A; Team 2: A,F,E,F,A/E,F,A; "
    "Team 3: A,C,D,E,D,C,A; Team 4: A,E,A,C,A,E,A, at times 09:00, 09:30, 10:00, 10:30, 11:00, "
    "11:30, 12:00 respectively.)"
)

ROWS = [
    dict(
        question_type="MCQ",
        question_text="Which one among the following stations is visited the largest number of times?",
        options=["Station F", "Station D", "Station E", "Station C"],
        correct_answer="Station E",
        explanation="From the team movement table, Station E is visited by Team 1 (twice), Team 2 (at least once), Team 3 (once), and Team 4 (twice) - more than any other station.",
    ),
    dict(
        question_type="TITA",
        question_text="How many times do the teams pass through Station B in a day?",
        options=None,
        correct_answer="2",
        explanation="Only Team 1 passes through Station B, doing so at 9:30 and again at 11:30 - twice in total.",
    ),
    dict(
        question_type="MCQ",
        question_text="Which team patrols the street connecting Stations D and E at 10:15 hrs?",
        options=["Team 4", "Team 1", "Team 3", "Team 2"],
        correct_answer="Team 3",
        explanation="Team 3 is at Station D at 10:00 hrs and at Station E at 10:30 hrs, so it is travelling the D-E street at 10:15 hrs.",
    ),
    dict(
        question_type="TITA",
        question_text="How many times does Team 4 pass through Station E in a day?",
        options=None,
        correct_answer="2",
        explanation="From the movement table, Team 4's route is A,E,A,C,A,E,A - passing through Station E twice (at 09:30 and 11:30).",
    ),
    dict(
        question_type="MCQ",
        question_text="How many teams pass through Station C in a day?",
        options=["2", "4", "3", "1"],
        correct_answer="2",
        explanation="From the movement table, only Team 3 (at 09:30 and 11:30) and Team 4 (at 10:30) pass through Station C - 2 teams in total.",
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
                    CatQuestion.source_year == 2023,
                    CatQuestion.source_slot == "slot3",
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
                source_year=2023,
                source_slot="slot3",
                group_id="cat2023_dilr_slot3_set2",
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
        print(f"Inserted {inserted} CAT 2023 DILR Slot 3 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

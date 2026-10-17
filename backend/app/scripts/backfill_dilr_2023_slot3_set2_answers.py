"""Backfill correct_answer for CAT 2023 DILR Slot 3 Set 2 (police patrol
routes puzzle, group_id cat2023_dilr_slot3_set2), matched by id.

These 5 rows were already present in the DB (loaded by
seed_cat_pyq_2023_dilr_slot3.py) but without a correct_answer.
backfill_dilr_2023_slot3_missing_questions.py independently solved this set
and derived a complete, internally-consistent team-movement table, but that
script only INSERTs rows for question_text it can't find - since these rows
already existed, it silently skipped them without ever setting their
answers. This script applies those already-derived answers (now also cross-
checked against the official solutions PDF's team movement table, which
matches exactly) to the existing rows.

Movement table (verified against DILR_SLOT3_CAT_2023_SOLUTIONS.pdf):
  Team 1: A,B,A,E,A,B,A
  Team 2: A,F,E,F,A/E,F,A
  Team 3: A,C,D,E,D,C,A
  Team 4: A,E,A,C,A,E,A
  (at times 09:00, 09:30, 10:00, 10:30, 11:00, 11:30, 12:00 respectively)

Run with:
    python -m app.scripts.backfill_dilr_2023_slot3_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    1088: {
        "answer_contains": "Station E",
        "explanation": (
            "From the team movement table, Station E is visited by Team 1 (twice), Team 2 (at least "
            "once), Team 3 (once), and Team 4 (twice) - more than any other station."
        ),
    },
    1089: {
        "correct_answer": "2",
        "explanation": "Only Team 1 passes through Station B, doing so at 9:30 and again at 11:30 - twice in total.",
    },
    1090: {
        "answer_contains": "Team 3",
        "explanation": (
            "Team 3 is at Station D at 10:00 hrs and at Station E at 10:30 hrs, so it is travelling the "
            "D-E street at 10:15 hrs."
        ),
    },
    1091: {
        "correct_answer": "2",
        "explanation": (
            "From the movement table, Team 4's route is A,E,A,C,A,E,A - passing through Station E "
            "twice (at 09:30 and 11:30)."
        ),
    },
    1092: {
        "answer_contains": "2",
        "explanation": (
            "From the movement table, only Team 3 (at 09:30 and 11:30) and Team 4 (at 10:30) pass "
            "through Station C - 2 teams in total."
        ),
    },
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, fix in FIXES.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={question_id}")
                continue

            if "correct_answer" in fix:
                row.correct_answer = fix["correct_answer"]
            else:
                needle = fix["answer_contains"]
                options = row.options or []
                if needle in options:
                    match = needle
                else:
                    candidates = [opt for opt in options if needle in opt]
                    match = candidates[0] if len(candidates) == 1 else None
                if match is None:
                    print(f"NO OPTION MATCH for id={question_id} (needle={needle!r}, options={row.options})")
                    continue
                row.correct_answer = match

            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2023 DILR Slot 3 Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill correct_answer for CAT 2021 DILR Slot 3 Set 4 (Gantt-chart
employee-schedule set, group_id cat2021_dilr_slot3_set4), matched by
(source_year, source_slot, section, question_text). Answers come from a
user-supplied answer-key screenshot.

Q17 ("Which of the following statements is/are true?") is deliberately
NOT backfilled here: its screenshot showed all three visible options
marked wrong with no checkmark on any option (the correct one was below
the crop), so the true answer was never actually seen - only the other
three options' invalidity was. correct_answer stays None for that row
rather than guessing.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot3_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot3"

ANSWERS = [
    (
        "Which employees did not work in multiple projects for any of the months in 2020?",
        "Only Abani, Bahni and Danni",
    ),
    (
        "The project duration, measured in terms of the number of months, is the time during "
        "which at least one employee worked in the project. Which of the following pairs of "
        "the projects had the same duration?",
        "Project 3, Project 4",
    ),
    (
        "The list of employees in decreasing order of annual completion index is:",
        "Danni, Tinni, Abani, Bahni",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.question_text == question_text,
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

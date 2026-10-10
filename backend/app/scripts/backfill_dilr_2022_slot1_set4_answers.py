"""Backfill correct_answer for CAT 2022 DILR Slot 1 Set 4 (graduating-students
get-together set, Q16-20, group_id cat2022_dilr_slot1_set4), matched by
(source_year, source_slot, section, question_text). Answers come from a
user-supplied answer-key screenshot, not derived independently.

Run with:
    python -m app.scripts.backfill_dilr_2022_slot1_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How many boys are there in the class?", "50"),
    (
        "Which of the following can be determined from the given information? I. The number "
        "of boys who are interested in attending a 1-day event and\n\nare neither dancers nor "
        "singers. II. The number of female dancers who are interested in attending a 1-day "
        "event.",
        "Only II",
    ),
    ("What fraction of the class are interested in attending a 2-day event?", "7/13"),
    (
        "What BEST can be concluded about the number of male dancers who are interested in "
        "attending a 1-day event?",
        "5 or 6",
    ),
    ("How many female dancers are interested in attending a 2-day event?", "0"),
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

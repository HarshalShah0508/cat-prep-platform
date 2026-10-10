"""Backfill correct_answer for CAT 2020 DILR Slot 3 Set 5 (blood-test vial
pooling set, group_id cat2020_dilr_slot3_set5), matched by (source_year,
source_slot, section, question_text). Answers come from a user-supplied
answer-key screenshot (all 4 questions had a stated "Correct Answer").

This set was previously miscategorised: three of its four questions were
split across two different group_ids (set5/set6), and a fourth question
("Which of the following combinations of test results is NOT possible?")
was missing from the seed entirely. All four are now under the single
group_id cat2020_dilr_slot3_set5, matching the real exam's single Set 5.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot3_set5_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot3"

ANSWERS = [
    (
        "Suppose vial C tests positive and vials A, E and H test negative. Which patient has "
        "the disease?",
        "Patient 6",
    ),
    (
        "Suppose vial A tests positive and vials D and G test negative. Which of the "
        "following vials should we test next to identify the patient with the disease?",
        "Vial E",
    ),
    (
        "Which of the following combinations of test results is NOT possible?",
        "Vials A and E positive, vials C and D negative",
    ),
    (
        "Suppose one of the lab assistants accidentally mixed two patients’ blood "
        "samples before they were distributed to the vials. Which of the following "
        "correctly represents the set of all possible numbers of positive test results out "
        "of the eight vials?",
        "{4, 5, 6, 7, 8}",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 5 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

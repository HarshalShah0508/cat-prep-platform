"""Backfill correct_answer/explanation for CAT 2020 DILR Slot 1 Set 3
(board-examination marks set, group_id cat2020_dilr_slot1_set3). Matched
by primary key id. Answers come from DILR_SLOT1_CAT_2020_SOLUTIONS.pdf in
pyq-source/2020/.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot1_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        423,
        "Alva",
        "The student who missed the Mathematics exam is the one whose Mathematics marks were "
        "computed as an average (rather than a real score) and did not miss any other exam. "
        "Per the official key this is Alva.",
    ),
    (
        424,
        "Cannot be determined",
        "Given only the facts stated about who missed Hindi, Mathematics and Science, there is "
        "not enough information to pin down exactly which two students missed the English "
        "exam, so per the official key the answer is 'Cannot be determined'.",
    ),
    (
        425,
        "Alva and Esha",
        "One student who missed Hindi missed no other exam, and the other missed both Hindi "
        "and Science; working through the marks table against these constraints, per the "
        "official key the best conclusion is that Alva and Esha are the two who missed Hindi.",
    ),
    (
        426,
        "Bithi and one out of Alva and Deep",
        "The student who missed Hindi and Science together is one of the two Hindi-missers; "
        "combined with the rest of the marks table, per the official key the best conclusion "
        "is that Bithi, along with one of Alva or Deep, missed the Science exam.",
    ),
    (
        427,
        "4",
        "Of the six students, those who missed exactly one exam are the ones whose marks in "
        "that one subject were filled in as the average of their best three other scores; per "
        "the official key, 4 of the six students missed exactly one exam.",
    ),
    (
        428,
        "3",
        "Combining the marks table with the stated facts, the exact set of missed exams can be "
        "pinned down with certainty for only some of the six students; per the official key, "
        "this is possible for 3 of them.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already set): id={question_id}")
                continue
            if row.options and correct_answer not in row.options:
                print(f"WARNING: answer {correct_answer!r} not in options for id={question_id}: {row.options}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill missing correct_answer/explanation for CAT 2025 DILR Slot 3.

Source: pyq-source/2025/DILR_SLOT3_CAT_2025_SOLUTIONS.pdf

Matched by id directly. Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered.
Also verifies the answer string is one of the row's options before writing,
since the app does an exact string match at scoring time.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot3"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        752,
        "8",
        "Both Brins and Crowns are pegged to Zentars via the citizens' Travel-Cost "
        "statements; working out each currency's Zentar value and taking the "
        "ratio gives 1 Brin = 8 Crowns.",
    ),
    (
        753,
        "Jano spent 2000 in Aurevia",
        "Building each traveler's local-currency spends from the citizens' "
        "statements and the Travel Cost totals shows Jano actually spent 1000 (not "
        "2000) in Aurevia, making that the one statement that is NOT true.",
    ),
    (
        758,
        "Eshan",
        "Locking the seating from the recorded Buck passes and reading clockwise "
        "(the children face inward) from Bina's seat gives Eshan as her immediate "
        "right-hand neighbour.",
    ),
    (
        759,
        "Chirag",
        "Counting three seats anticlockwise ('to the left') from Eshan's fixed "
        "seat in the completed circle lands on Chirag.",
    ),
    (
        760,
        "Immediately to the right",
        "The pass-type counts are linked by the total-passes and total-displacement "
        "equations, which leave three of the four pass-type counts free to vary "
        "across valid arrangements - only the count of 'immediately to the right' "
        "passes comes out the same in every one, so it is the uniquely determined type.",
    ),
    (
        761,
        "Gaurav",
        "Checking every valid arrangement consistent with the recorded passes, "
        "Bina, Eshan and Farhan can each receive the Buck a different number of "
        "times depending on the path taken, but Gaurav's reception count stays "
        "fixed in all of them.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH for id={qid}")
                continue
            if row.options and correct_answer not in row.options:
                print(f"WARNING: answer not in options for id={qid}: {correct_answer!r} not in {row.options!r}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

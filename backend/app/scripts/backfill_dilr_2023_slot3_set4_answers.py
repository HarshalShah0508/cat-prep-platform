"""Backfill correct_answer for CAT 2023 DILR Slot 3 Set 4 (AC dealers D1-D4
puzzle, group_id cat2023_dilr_slot3_set4), matched by id. Answers come from
the official solutions PDF (DILR_SLOT3_CAT_2023_SOLUTIONS.pdf). id 1098 in
this group ("How many Split Inverter ACs did D2 sell?") already has a
correct_answer in the DB and is left untouched - out of scope for a
backfill script that only ever fills NULLs.

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot3_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    1099: {
        "answer_contains": "25%",
        "explanation": (
            "With 25% of all ACs being Window and 20% of all Inverter ACs being Window, working "
            "through the two equations alongside the given 6 Window Non-inverter and 36 Split Inverter "
            "totals gives 60 ACs sold in total, 36 Inverter and 24 Non-inverter - 24/60 = 25%."
        ),
    },
    1100: {
        "correct_answer": "33",
        "explanation": (
            "Solving the full dealer-wise breakdown gives D1=15 and D3=12 ACs sold (27 together); out "
            "of the 60 total ACs sold in the city, that leaves D2 and D4 with 60-27 = 33 between them."
        ),
    },
    1101: {
        "answer_contains": "D1 and D3 together sold more ACs as compared to D2 and D4 together.",
        "explanation": (
            "D2 clearly sells more than D1 or D3 individually (it has the largest Window and Split "
            "Inverter shares by construction), so D2 and D4 together necessarily outsell D1 and D3 "
            "together - making the opposite claim necessarily false."
        ),
    },
    1102: {
        "answer_contains": "5",
        "explanation": (
            "If D3 and D4 sell equal numbers of ACs, working through the Window/Split and "
            "Inverter/Non-inverter splits for D2 - 2 Window Non-inverter plus 3 Split Non-inverter - "
            "gives D2 a total of 5 Non-inverter ACs sold."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 3 Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

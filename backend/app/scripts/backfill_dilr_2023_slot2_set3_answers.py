"""Backfill correct_answer for CAT 2023 DILR Slot 2 Set 3 (Akhil/Bimal/
Chatur random-draw scoring puzzle, group_id cat2023_slot2_dilr_set3),
matched by id. Answers come from the official solutions PDF
(DILR_SLOT2_CAT_2023_SOLUTIONS.pdf); explanations are rewritten in plain
language, not copied verbatim.

Base-case daily scores (verified against the given day totals, 2-day
averages, and all stated constraints):
  Day 1: Chatur=3, Akhil=7, Bimal=5
  Day 2: Chatur=9, Akhil=4, Bimal=2
  Day 3: Chatur=6, Akhil=5, Bimal=5
  Day 4: Chatur=6, Akhil=3, Bimal=7
  Day 5: Chatur=9, Akhil=4, Bimal=5
  Totals: Akhil=23, Bimal=24, Chatur=33

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot2_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    634: {
        "answer_contains": "7",
        "explanation": "In the base-case day-by-day score assignment, Akhil's Day 1 score is 7.",
    },
    635: {
        "answer_contains": "Chatur",
        "explanation": (
            "Totalling each participant's five daily scores gives Akhil 23, Bimal 24, and Chatur 33 - "
            "Chatur attains the maximum total score."
        ),
    },
    636: {
        "correct_answer": "25",
        "explanation": (
            "Checking every valid day-by-day score assignment consistent with the given ranks, day "
            "totals and 2-day averages, the lowest total score Bimal can end up with is 25."
        ),
    },
    637: {
        "answer_contains": "4",
        "explanation": (
            "Forcing Bimal's total to a multiple of 3 (27) pins Akhil's total at 23, with his "
            "day-by-day scores working out to 7, 4, 5, 3, 4 - so Akhil's Day 2 score is 4."
        ),
    },
    638: {
        "correct_answer": "26",
        "explanation": (
            "If Akhil's total is fixed at 24, working back through the day totals and rank constraints "
            "gives Bimal a total score of 26."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 2 Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

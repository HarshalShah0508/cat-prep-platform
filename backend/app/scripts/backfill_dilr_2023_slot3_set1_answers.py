"""Backfill correct_answer for CAT 2023 DILR Slot 3 Set 1 (coaching class
online/offline registrations puzzle, group_id cat2023_dilr_slot3_set1),
matched by id. Answers come from the official solutions PDF
(DILR_SLOT3_CAT_2023_SOLUTIONS.pdf); explanations are rewritten in plain
language, not copied verbatim. ids 1083/1084 in this group already had
correct_answer filled; this script only covers the three MCQ questions that
were still NULL.

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot3_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    1085: {
        "answer_contains": "Only I",
        "explanation": (
            "With May having the largest online registrations and the offline minimum sitting at 30, "
            "it's possible for May's offline count to be the smallest - so statement I can be true. "
            "Nothing in the given data forces February specifically to have the smallest total, so "
            "statement II isn't supported."
        ),
    },
    1086: {
        "answer_contains": "50",
        "explanation": (
            "The median offline registration figure across the five months is 50, and nothing in the "
            "given facts excludes February from holding that median value - so 50 is the value that "
            "can be concluded for February."
        ),
    },
    1087: {
        "answer_contains": "Both I and II",
        "explanation": (
            "The total registrations' median of 120 is consistent with January and April both sitting "
            "at 120, and separately with February and May landing on a matching value too - so both "
            "pairings can hold simultaneously."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 3 Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

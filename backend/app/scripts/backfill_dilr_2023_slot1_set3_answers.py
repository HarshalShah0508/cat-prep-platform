"""Backfill correct_answer for CAT 2023 DILR Slot 1 Set 3 (five restaurants
rating five gig workers, group_id cat2023_slot1_dilr_set3), matched by id.
Answers come from the official solutions PDF (DILR_SLOT1_CAT_2023_SOLUTIONS.pdf);
explanations are rewritten in plain language, not copied verbatim.

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot1_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

# id -> {"correct_answer": "<value>"} for TITA, or {"answer_contains": "<substring>"} for MCQ
FIXES = {
    614: {
        "correct_answer": "0",
        "explanation": (
            "Reconstructing the full 5x5 ratings table from the given row/column means and the partial "
            "1s and 5s leaves no ambiguity anywhere - every remaining cell is forced by the row and "
            "column totals, so 0 individual ratings are left undetermined."
        ),
    },
    615: {
        "correct_answer": "0",
        "explanation": (
            "Once the ratings table is fully reconstructed, R2's row of ratings is 1, 1, 2, 2, 5 - it "
            "never awarded a 4 to anyone, so the answer is 0 workers."
        ),
    },
    616: {
        "correct_answer": "3",
        "explanation": (
            "Filling in the ratings table from the given means and partial 1s/5s, R1's rating for "
            "Xavier works out to 3."
        ),
    },
    617: {
        "correct_answer": "4",
        "explanation": (
            "R3's column of ratings across the five workers comes out to 4, 4, 5, 5, 1; sorted that's "
            "1, 4, 4, 5, 5, so the median is 4."
        ),
    },
    618: {
        "answer_contains": "R4",
        "explanation": (
            "Checking each restaurant's median rating against how many workers actually received that "
            "exact value: R2's median (2) went to 2 workers, R5's median (4) went to 2 workers, R3's "
            "median (4) went to 2 workers, but R4's median (3) went to only 1 worker."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 1 Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill correct_answer for CAT 2023 DILR Slot 2 Set 4 (nine boxes of
coin sacks, group_id cat2023_slot2_dilr_set4), matched by id.

The solutions PDF's "Correct Answer:" labels and raw grid data for this set
are reliable, but its prose explanations are garbled/reused from an
unrelated set (the random-draw puzzle) - likely an artifact of how the PDF
was generated. Rather than trust the prose, the full coin grid was
reconstructed directly from the passage's two tables and independently
verified consistent with every given median, >5-coin count, and condition
flag (see grid below). id 1098 (same group, "How many sacks have exactly
one coin?") already has a correct_answer in the DB and is left untouched -
out of scope for a backfill script that only ever fills NULLs.

Reconstructed grid (rows x columns), each cell is a box's 3 sack coin counts:
    R1: C1=(1,1,7) C2=(3,9,9) C3=(1,6,8)
    R2: C1=(1,2,9) C2=(1,2,3) C3=(9,9,9)
    R3: C1=(7,8,9) C2=(1,8,9) C3=(1,1,1)
This matches every given median (Table 1), every given >5-coin count and
condition-flag (Table 2), and gives identical row/column coin totals of 45.

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot2_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    639: {
        "answer_contains": "45",
        "explanation": (
            "Row 3's three boxes hold (7,8,9), (1,8,9) and (1,1,1) - 24 + 18 + 3 = 45 coins in total, "
            "matching every row's fixed total."
        ),
    },
    640: {
        "answer_contains": "5",
        "explanation": (
            "Checking each box's three sack counts, a 9-coin sack appears in (3,9,9), (1,2,9), (9,9,9), "
            "(7,8,9) and (1,8,9) - 5 boxes in total."
        ),
    },
    641: {
        "correct_answer": "4",
        "explanation": (
            "Comparing each box's average to its median: (1,2,3) has average 2 = median 2, (9,9,9) has "
            "average 9 = median 9, (7,8,9) has average 8 = median 8, and (1,1,1) has average 1 = median "
            "1 - 4 boxes where the two match."
        ),
    },
    643: {
        "correct_answer": "5",
        "explanation": (
            "Boxes where all three sacks hold different counts are (1,6,8), (1,2,9), (1,2,3), (7,8,9) "
            "and (1,8,9) - 5 boxes in total."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 2 Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

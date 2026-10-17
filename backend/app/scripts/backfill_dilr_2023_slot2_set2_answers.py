"""Backfill correct_answer for CAT 2023 DILR Slot 2 Set 2 (Anjali/Bipasha/
Chitra amusement park rides puzzle, group_id cat2023_slot2_dilr_set2),
matched by id. Answers come from the official solutions PDF
(DILR_SLOT2_CAT_2023_SOLUTIONS.pdf); explanations are rewritten in plain
language, not copied verbatim.

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot2_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    629: {
        "answer_contains": "110",
        "explanation": (
            "Bipasha's full schedule works out to Ride-2 (Rs 50), Ride-1 (Rs 20), and Ride-4 (Rs 40) - "
            "a total ticket spend of Rs 110."
        ),
    },
    630: {
        "answer_contains": "Ride-1, Ride-2, and Ride-3",
        "explanation": (
            "Reconstructing Anjali's schedule (Ride-1 at 11am, Ride-3 at 12pm, Ride-2 at 1pm, Ride-4 at "
            "2pm) shows that by 2:00 pm she had completed Ride-1, Ride-3, and Ride-2 - i.e. Ride-1, "
            "Ride-2, and Ride-3."
        ),
    },
    631: {
        "answer_contains": "Ride-1",
        "explanation": (
            "Chitra took Ride-3 then Ride-1, Anjali took Ride-1, Ride-3, Ride-2 and Ride-4, and Bipasha "
            "took Ride-2, Ride-1 and Ride-4 - Ride-1 is the only ride all three of them took."
        ),
    },
    632: {
        "correct_answer": "6",
        "explanation": (
            "Anjali's full schedule has her taking 4 rides (Ride-1, Ride-3, Ride-2, Ride-4) and "
            "Chitra's has her taking 2 (Ride-3, Ride-1) - 4 + 2 = 6 rides between them."
        ),
    },
    633: {
        "correct_answer": "140",
        "explanation": (
            "Anjali's full schedule is Ride-1 (Rs 20), Ride-3 (Rs 30), Ride-2 (Rs 50), and Ride-4 (Rs "
            "40) - a total ticket spend of Rs 140."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 2 Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

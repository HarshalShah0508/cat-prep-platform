"""Backfill correct_answer for CAT 2023 DILR Slot 1 Set 4 (visa processing
office, group_id cat2023_slot1_dilr_set4), matched by id. Answers come from
the official solutions PDF (DILR_SLOT1_CAT_2023_SOLUTIONS.pdf); explanations
are rewritten in plain language, not copied verbatim.

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot1_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    619: {
        "correct_answer": "0",
        "explanation": (
            "With 5 US, at least 3 Schengen (Ira/Vijay/Nandini all in one slot) and at least 2 Others "
            "(Mahira/Osman in one slot) applicants fixed per 10-application slot, no room is left for "
            "any UK applicants - so 0 UK applications were scheduled that day."
        ),
    },
    620: {
        "correct_answer": "200",
        "explanation": (
            "With 20 slots and at least 2 Others applicants per slot, there are 40 Others applications "
            "in total; at the category's maximum processing time of 5 minutes each, that comes to at "
            "most 40 x 5 = 200 minutes."
        ),
    },
    621: {
        "answer_contains": "9:45am",
        "explanation": (
            "Working out the Schengen counter schedule, Nandini is 6th in the Schengen queue and her "
            "processing finishes closest to 9:45 am."
        ),
    },
    622: {
        "answer_contains": "Mahira started after Nandini",
        "explanation": (
            "Mahira starts her Others-category ride at 9:30 am, while Nandini (6th in the Schengen "
            "queue) only starts at 9:32:30 am - so Mahira actually started before Nandini, making the "
            "statement that she started after Nandini the false one."
        ),
    },
    623: {
        "answer_contains": "2:05 pm",
        "explanation": (
            "With 5 US applications per slot across all 20 slots (100 total) processed across 4 "
            "counters at 10 minutes each, working through the counter schedule shows the last US "
            "applicant finishes at 2:05 pm."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 1 Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

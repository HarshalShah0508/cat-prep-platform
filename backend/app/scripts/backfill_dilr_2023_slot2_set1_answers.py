"""Backfill correct_answer for CAT 2023 DILR Slot 2 Set 1 (Odsville firms
fundraising puzzle, group_id cat2023_slot2_dilr_set1), matched by id.
Answers come from the official solutions PDF (DILR_SLOT2_CAT_2023_SOLUTIONS.pdf);
explanations are rewritten in plain language, not copied verbatim.

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot2_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    624: {
        "answer_contains": "Only Czechy and Drjbna",
        "explanation": (
            "Working through the possible first-year-to-last-year raise sequences for each firm (each "
            "starting/ending at Rs 1 crore, changing by 1 or 2 crores a year, never repeating "
            "consecutively), only Czechy and Drjbna have a single valid sequence each - every other "
            "firm has more than one way to hit its given total, so only their year-by-year amounts can "
            "be pinned down with certainty."
        ),
    },
    625: {
        "answer_contains": "either Rs. 7 crores or Rs. 8 crores.",
        "explanation": (
            "Testing the valid raise sequences for Bzygoo and Drjbna (the two firms active in 2015) "
            "against the other fixed totals shows 2015's combined total can only come out to Rs 7 "
            "crore or Rs 8 crore, depending on which valid sequence each firm followed."
        ),
    },
    626: {
        "correct_answer": "17",
        "explanation": (
            "Taking the highest valid 2013 contribution from each of the firms active that year "
            "(Alfloo, Bzygoo, Czechy, Drjbna, Elavalaki) under their respective valid raise sequences "
            "gives a combined maximum of Rs 17 crore."
        ),
    },
    627: {
        "answer_contains": "11",
        "explanation": (
            "With Elavalaki raising Rs 3 crore in 2013, its total of Rs 13 crore forces a specific "
            "year-by-year pattern that pins 2012 at Rs 5 crore for Elavalaki. Taking the smallest valid "
            "2012 contribution for each of the other active firms (Alfloo, Bzygoo, Drjbna; Czechy "
            "hadn't started yet) and adding them up gives a minimum combined total of Rs 11 crore."
        ),
    },
    628: {
        "answer_contains": "Bzygoo raised the same amount of money as Elavalaki in 2013.",
        "explanation": (
            "With the 2014 total fixed at Rs 12 crore, checking each statement against the firms' "
            "valid raise sequences shows every option except one is achievable; Bzygoo's possible "
            "2013 values never line up with Elavalaki's possible 2013 values under this constraint, "
            "making that match the one impossible statement."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 2 Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill correct_answer for CAT 2023 DILR Slot 3 Set 3 (Amala/Koli/Rini/
Biman/Mathew/Shyamal project-and-test scoring puzzle, group_id
cat2023_dilr_slot3_set3), matched by id. Answers come from the official
solutions PDF (DILR_SLOT3_CAT_2023_SOLUTIONS.pdf), cross-checked against two
independent derivations in that PDF which agree exactly:

    Student  Test  Project  Aggregate(0.6T+0.4P)  Project pair
    Amala     60      80           68             Amala & Mathew
    Koli      80      40           64             Koli & Biman
    Rini      60      60           60             Rini & Shyamal
    Biman     50      40           46             Biman & Koli
    Mathew    40      80           56             Mathew & Amala
    Shyamal   70      60           66             Shyamal & Rini

For MCQ rows, the correct option text is looked up at runtime via a unique
substring match against that row's own `options` list (instead of retyping
it by hand) so the stored value is guaranteed to be character-for-character
identical to one of the options, as scoring requires.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot3_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    1093: {
        "correct_answer": "60",
        "explanation": "In the final scoring table, Rini's project score is 60 (she was paired with Shyamal).",
    },
    1094: {
        "answer_contains": "0.60",
        "explanation": (
            "Working through the aggregate = (project weight)xP + (test weight)xT formula against "
            "Amala's, Koli's and Shyamal's known test/project/aggregate relationships, the test weight "
            "that makes everything consistent is 0.60 (with the project weight at 0.40)."
        ),
    },
    1095: {
        "answer_contains": "68",
        "explanation": "In the final scoring table, Amala's aggregate of 68 is the highest among all six students.",
    },
    1096: {
        "correct_answer": "40",
        "explanation": "In the final scoring table, Mathew's test score is 40 (paired with Amala in the project, scoring 80 there).",
    },
    1097: {
        "answer_contains": "Neither (i) nor (ii)",
        "explanation": (
            "The actual project pairings are Amala & Mathew, Koli & Biman, and Rini & Shyamal - so "
            "neither \"Amala and Biman\" nor \"Koli and Mathew\" were paired together."
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
        print(f"Backfilled {updated} CAT 2023 DILR Slot 3 Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

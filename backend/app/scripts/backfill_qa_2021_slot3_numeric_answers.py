"""Backfill missing correct_answer/explanation for CAT 2021 QA Slot 3 TITA rows
that were left over after backfill_qa_2021_slot3_answers.py (that earlier
script covered a different subset of questions; these ids were still NULL).

Source: pyq-source/2021/QUANT_SLOT3_CAT_2021_SOLUTIONS.pdf, cross-checked by
re-deriving each answer independently. Note: the rhombus-fencing question
(id 883) has a "Correct Answer: 1250" header in that PDF that contradicts its
own worked solution (which arrives at 28 m of total diagonal length, i.e.
28 x 125 = 3500) before wandering off into an unrelated, seemingly erroneous
tangent. 3500 was used here since it is independently verified by direct
computation and matches the PDF's own shown arithmetic.

Matched by id directly (ids pulled from a DB query for source='pyq' AND
source_year=2021 AND source_slot='slot3' AND section='QA' AND
correct_answer IS NULL). Every update is guarded by `correct_answer.is_(None)`
so an already-answered row can never be clobbered.

Run with:
    python -m app.scripts.backfill_qa_2021_slot3_numeric_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot3"

# id -> (correct_answer, explanation)
ANSWERS = {
    871: (
        "None of these",
        "Checking all four sign cases for x and y: x<0 forces y=1/3 (from the second equation), "
        "which then forces x=2 in the first equation - contradicting x<0, so that case (and "
        "likewise x<0,y<0) is invalid. x>=0,y>=0 gives 2x+3y=1 and 3x+3y=7, so x=6, y=-11/3, "
        "contradicting y>=0 - also invalid. The only consistent case is x>=0,y<0: 2x+3y=1 and "
        "3x-y=7 solve to x=2, y=-1 (check: 3(2)+2(1)+(-1)=7 and 2+2+3(-1)=1, both hold). So "
        "x+2y = 2-2 = 0, which is not among -4, 38 or 1 - the solutions PDF's stated 'Correct "
        "Answer: (3) 1' does not match its own equations, so 'None of these' is used here "
        "instead based on independent verification.",
    ),
    883: (
        "3500",
        "Area = d1*d2/2 = 96, so d1*d2 = 192. Perimeter = 40 means each side s = 10, and since "
        "the diagonals bisect each other at right angles, d1^2 + d2^2 = 4s^2 = 400. Then "
        "(d1+d2)^2 = d1^2 + d2^2 + 2*d1*d2 = 400 + 384 = 784, so d1 + d2 = 28 m - the combined "
        "length of both diagonals. Cost = 28 x 125 = INR 3500.",
    ),
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, (correct_answer, explanation) in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH / already answered: id={question_id}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

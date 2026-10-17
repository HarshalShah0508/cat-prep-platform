"""Backfill missing correct_answer/explanation for CAT 2021 QA Slot 2 TITA rows
that were left over after backfill_qa_2021_slot2_answers.py (that earlier
script covered a different subset of questions; these ids were still NULL).

Source: pyq-source/2021/QUANT_SLOT2_CAT_2021_SOLUTIONS.pdf, cross-checked by
re-deriving each answer independently.

Matched by id directly (ids pulled from a DB query for source='pyq' AND
source_year=2021 AND source_slot='slot2' AND section='QA' AND
correct_answer IS NULL). Every update is guarded by `correct_answer.is_(None)`
so an already-answered row can never be clobbered.

Run with:
    python -m app.scripts.backfill_qa_2021_slot2_numeric_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot2"

# id -> (correct_answer, explanation)
ANSWERS = {
    850: (
        "5",
        "Per the solutions PDF's reading of the (OCR-garbled) exponent expressions, the "
        "bounding inequality restricts n to 0-7, and checking which of the resulting values "
        "stay within the stated upper bound leaves 5 valid integers: 5, 7, 13, 31, 85.",
    ),
    852: (
        "3384",
        "Let the number be abcd. a+b+c=14, b+c+d=15 and c=d+4 give a+b+d=10 and b+2d=11, so "
        "a=d-1. Testing d=4,3,2,1 gives candidates 3384, 2573, 1762 and (invalid) 0951 - the "
        "highest valid one is 3384.",
    ),
    854: (
        "1000",
        "Give each child the required minimum (4 balloons, 1 pencil) first, leaving 3 balloons, "
        "3 pencils and 3 erasers to distribute freely among 3 children. Each of these is a "
        "stars-and-bars count of C(3+3-1, 3-1) = 10, so the total is 10 x 10 x 10 = 1000.",
    ),
    856: (
        "45",
        "After two 9-litre draw-and-replace operations, the fraction of milk left is "
        "((C-9)/C)^2. Setting this equal to the given 16:25 ratio gives (C-9)/C = 4/5, so "
        "C - 9 = 4C/5, i.e. C/5 = 9, so C = 45 litres.",
    ),
    857: (
        "8",
        "log2(3 + log4(4 + log(x-1))) = 2 gives 3 + log4(4 + log(x-1)) = 4, so "
        "log4(4 + log(x-1)) = 1, so 4 + log(x-1) = 4, so log(x-1) = 0, so x - 1 = 1, x = 2. "
        "Then 4x = 4 x 2 = 8.",
    ),
    861: (
        "250",
        "With w + b = 450 and 0.4w = 0.5b (equal metallic counts), w = 5b/4, so 9b/4 = 450, "
        "b = 200 and w = 250. Metallic balls = 0.4(250) + 0.5(200) = 100 + 100 = 200, so "
        "non-metallic balls = 450 - 200 = 250.",
    ),
    862: (
        "10",
        "With m matches played and g goals so far: (g+1)/(m+10) = 0.15 and (g+2)/(m+10) = 0.2. "
        "Subtracting gives 1/(m+10) = 0.05, so m+10 = 20, m = 10.",
    ),
    865: (
        "30",
        "AD:BD = 2:1 makes AB = 3k (AD = 2k); AE:CE = 2:3 makes AC = 5m (AE = 2m). Since "
        "triangles ADE and ABC share angle A, area(ADE)/area(ABC) = (AD x AE)/(AB x AC) = "
        "(2k x 2m)/(3k x 5m) = 4/15. With area(ADE) = 8, area(ABC) = 8 x 15/4 = 30 sq cm.",
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

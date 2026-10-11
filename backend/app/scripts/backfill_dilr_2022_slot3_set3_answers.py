"""Backfill correct_answer for CAT 2022 DILR Slot 3 Set 3 (AI/ML course
grades set, group_id cat2022_dilr_slot3_set3), matched by (source_year,
source_slot, section, question_text).

NOT transcribed from any solutions PDF - solved from scratch via the
passage's 8 facts. Let k be a scale unit: non-CS-AI=2k, non-CS-ML=5k,
CS=7k (since non-CS "either AI or ML" count equals CS count per fact 2).
Facts 3+5+7+8 pin down non-CS-fail (f)=18 and CS-fail-ML=12, giving
CS-C-ML=36 (fact 3), which via fact 6's CS ML ratio 4:5:2 fixes 1 unit=18,
so CS total=210 (=7k, k=30). AI total=9k=270, ML total=12k=360.

Fact 6's CS AI ratio 3:5:2 on CS=210 gives CS-A-AI=63, CS-C-AI=42; fact 5
(no non-CS student gets an A in AI) plus fact 4 (A=C counts for AI
overall) forces non-CS-C-AI=21 and overall A-AI=63. Fact 4's "50% of
passers get B" check for AI reproduces exactly (126 = 105 CS-B-AI +
21 non-CS-B-AI), confirming the derivation. The same approach for ML
(fact 4's A:C=3:2 ratio, 50%-get-B check) gives non-CS-A-ML=27 and
non-CS-B-ML=75.

Confidence: three of the five answers are MCQ and all three land exactly
on one of the four given options (270, 63, 75) - strong independent
validation since these numbers were derived from the constraint system,
not reverse-engineered from the option lists.

Run with:
    python -m app.scripts.backfill_dilr_2022_slot3_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("How many students took AI?", "270"),
    ("How many CS students failed in ML?", "12"),
    ("How many non-CS students got A grade in ML?", "27"),
    ("How many students got A grade in AI?", "63"),
    ("How many non-CS students got B grade in ML?", "75"),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.question_text == question_text,
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill correct_answer for CAT 2024 DILR Slot 1 Set 3 (Amiya/Ramya
election-campaign percentage-logic set, group_id cat2024_slot1_dilr_set3),
matched by (source_year, source_slot, section, question_text).

Not transcribed from any solutions PDF - solved from scratch from the
passage's own rules. Baseline (both focus on issues, levels a,r in {1,2}):
turnout = 20(a+r)% of all students, split 20a% to Amiya / 20r% to Ramya.
Each attack rule then redistributes a fixed fraction of the attacker's own
baseline voters (not all students): A-attacks-only loses 10% to Ramya + 10%
abstain; R-attacks-only loses 20% to Amiya + 5% abstain; both-attack each
lose 10% to abstention only (no switching). All 4 regimes reduce to clean
linear formulas in a and r; all 5 answers below land exactly on one of the
question's own multiple-choice options, which is strong independent
confirmation the algebra is right.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot1_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot1"

ANSWERS = [
    (
        "If both of them run staid campaigns attacking the other, then what percentage "
        "of students will vote in the election?",
        "36%",
    ),
    (
        "What is the minimum percentage of students who will vote in the election?",
        "36%",
    ),
    (
        "If Amiya runs a campaign focusing on issues, then what is the maximum "
        "percentage of votes that she can get?",
        "48%",
    ),
    (
        "If Ramya runs a campaign attacking Amiya, then what is the minimum percentage "
        "of votes that she is guaranteed to get?",
        "15%",
    ),
    (
        "What is the maximum possible voting margin with which one of the candidates "
        "can win?",
        "29%",
    ),
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

"""Backfill correct_answer for CAT 2021 DILR Slot 1 Set 3 (smoothies/fruit
salad set, group_id cat2021_dilr_slot1_set3), matched by (source_year,
source_slot, section, question_text).

Solved from scratch (no solutions PDF/answer key available for this slot).
Pricing: Mango smoothie=12, Apple smoothie=11, Banana smoothie=10, Mixed
fruit smoothie=19, Fruit salad=12 (same price as Mango smoothie - the
source of this set's genuine ambiguity). Each woman's hourly revenue
uniquely determines her Hours 1-3 product mix by subset-sum (only one
combination of distinct products fits each target), except Ganga's Hour 1
genuinely cannot be pinned down further: paying 23 could be Apple+Mango
smoothie OR Apple+Fruit salad (both price 12), and working the raw
material balance through to Hour 4 shows BOTH are internally consistent -
this is a real, irreducible ambiguity in the puzzle, not a solving gap.

Q3 ("total units of milk the three women had in the beginning") is NOT
backfilled: computing it requires summing Ganga's possible milk purchases
(7 or 8, depending on the Hour-1 ambiguity above) with Kaveri's (6 or 7,
a similar independent Hour-4 ambiguity) and Narmada's (6, uniquely
determined) - giving three possible totals {19, 20, 21}, which doesn't
cleanly match any of the four given options. Rather than force-fit the
closest-looking option, this one is left unanswered - there's likely a
small reasoning error on the milk-purchase side, but it wasn't found after
checking the material balances twice.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot1_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot1"

ANSWERS = [
    (
        "What BEST can be concluded about the number of units of fruit salad sold in "
        "the first hour?",
        "Either 1 or 2.",
    ),
    (
        "Which of the following is NECESSARILY true?",
        "Ganga did not sell any leftover apples.",
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
                    CatQuestion.group_id == "cat2021_dilr_slot1_set3",
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

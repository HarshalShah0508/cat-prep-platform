"""Backfill correct_answer/explanation for CAT 2020 DILR Slot 3 Set 2
(Hi-Lo game set, group_id cat2020_dilr_slot3_set2). Matched by primary key
id. Answers come from DILR_SLOT3_CAT_2020_SOLUTIONS.pdf in
pyq-source/2020/.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot3_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot3"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        467,
        "Hi, Lo, Lo, Hi",
        "Working from the round-3 and round-6 cumulative scores and the rule that an only-Hi "
        "bidder gains 3 points while the three Lo bidders each lose 1, the first-round bids "
        "that fit all the given facts are Arun: Hi, Bankim: Lo, Charu: Lo, Dipak: Hi.",
    ),
    (
        468,
        "4",
        "Using the scoring rules together with the given round-3 and round-6 cumulative "
        "scores and the fact that Arun was the sole Hi-bidder in exactly two rounds, Arun's "
        "total number of Hi bids across all six rounds works out to 4.",
    ),
    (
        469,
        "4",
        "Bankim's final score of -1 point after six rounds, combined with the scoring rules, "
        "implies he lost more rounds than he won; working through the constraints, Bankim bid "
        "Lo in 4 of the six rounds.",
    ),
    (
        470,
        "2",
        "A round where all four players bid identically (all Hi or all Lo) is distinct from "
        "the two rounds where Arun was the sole Hi bidder; working through the remaining "
        "rounds against the scoring constraints, all four players bid identically in 2 rounds.",
    ),
    (
        471,
        "1",
        "Dipak gains exactly 1 point only when exactly two players (including him) bid Hi; "
        "cross-checking this against Dipak's round-by-round score pattern implied by the "
        "given facts, this happens in 1 round.",
    ),
    (
        472,
        "Second",
        "Of the two rounds where Arun was definitely the sole Hi bidder, matching this against "
        "the round-3 cumulative scores and the fact that Dipak's third-round score was between "
        "his first- and second-round scores pins the second round as one where Arun was "
        "definitely the only player to bid Hi.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already set): id={question_id}")
                continue
            if row.options and correct_answer not in row.options:
                print(f"WARNING: answer {correct_answer!r} not in options for id={question_id}: {row.options}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill correct_answer for CAT 2020 DILR Slot 1 Set 4 (ten musicians -
tabla/mridangam/ghatam - set, group_id cat2020_dilr_slot1_set4), matched by
(source_year, source_slot, section, question_text).

Solved from scratch (no solutions PDF available for this slot). Category
sizes from the passage: tabla-only=3, mridangam-only=3, ghatam-only=1,
tabla+mridangam(not ghatam)=2, tabla+ghatam(not mridangam)=1 (=D, from
fact 2), mridangam+ghatam=0, all-three=0.

From facts 4-5: I is not tabla (fact 4) and not mridangam (fact 5), so I
must be the unique ghatam-only member; J is then forced into
mridangam-only (fact 4, with ghatam-only taken). H is not mridangam (fact
5) and (with ghatam-only/tabla+ghatam already taken by I/D) is forced into
tabla-only.

The tabla+mridangam pair (2 people) must be {one of A/B} + {one of F/G}
(facts 1 and 3) - C and E never reach that category, which answers Q3
directly. Q4's extra conditions (C has mridangam, F does not) pin down the
full assignment: C->mridangam-only, F->tabla-only, G->tabla+mridangam,
E->tabla-only (filling the last tabla-only slot alongside H and F).

Run with:
    python -m app.scripts.backfill_dilr_2020_slot1_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

ANSWERS = [
    (
        "Who among the following is DEFINITELY an expert in tabla but not in either "
        "mridangam or ghatam?",
        "H",
    ),
    (
        "Who among the following is DEFINITELY an expert in mridangam but not in either "
        "tabla or ghatam?",
        "J",
    ),
    (
        "Which of the following pairs CANNOT have any musician who is an expert in both "
        "tabla and mridangam but not in ghatam?",
        "C and E",
    ),
    (
        "If C is an expert in mridangam and F is not, then which are the three musicians "
        "who are experts in tabla but not in either mridangam or ghatam?",
        "E, F and H",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

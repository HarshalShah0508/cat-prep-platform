"""Backfill correct_answer for CAT 2021 DILR Slot 2 Set 3 (Chango
championship set, group_id cat2021_dilr_slot2_set3), matched by
(source_year, source_slot, section, question_text).

Solved from scratch (no solutions PDF/answer key available for this slot).
Chain of deduction: fact3's game counts force the champion and runner-up to
both be rank-1 players (reaching the final needs only 3 games from rank 1,
but 4 from rank 2/3 - and nobody plays 4 games). The two "didn't play"
clues (Aruna-Arif, Brij-Brinda) identify Aruna as rank 1 in Group A and
pin Group B's winner as Biju. Chetan's game count (2) only works if Chitra
is rank 1 in Group C; Dipen's game count (3) only works if he is rank 2/3
in Group D. That gives semifinals Aruna-beats-Biju and Chitra-beats-Dipen,
and since fact1 rules out Chitra as champion, Aruna wins the final.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot2_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot2"

ANSWERS = [
    (
        "Who among the following was DEFINITELY NOT ranked first in his/her group?",
        "Dipen",
    ),
    (
        "Which of the following pairs must have played against each other in the "
        "championship?",
        "Chitra, Dipen",
    ),
    ("Who won the championship?", "Aruna"),
    (
        "Who among the following did NOT play against Chitra in the championship?",
        "Biju",
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
                    CatQuestion.group_id == "cat2021_dilr_slot2_set3",
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

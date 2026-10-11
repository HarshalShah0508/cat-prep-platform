"""Backfill correct_answer for CAT 2021 DILR Slot 1 Set 1 (friends/
acquaintances/strangers set, group_id cat2021_dilr_slot1_set1), matched by
(source_year, source_slot, section, question_text).

Not transcribed from a solutions PDF - solved from scratch. The seed's
passage text has the table's numbers collapsed into one garbled line, so
the original PDF page was re-rendered as an image to confirm exact column
alignment (Amudha: Acquaintances=1, Strangers=4; Chandran: Acquaintances=1;
Dhinesh: Strangers=2; Ezhil: Strangers=1; Fani: Friends=1; Gowtham:
Acquaintances=3, Strangers=2; Bharatan: nothing given).

With each person relating to the other 6 (Friends+Acquaintances+Strangers=6
always), the 5 given facts pin down all 21 pairwise relationships uniquely:
Amudha's one friend is forced to be Ezhil (fact 2 + Amudha's F=1), and
facts 4/5 tie Amudha's single acquaintance to Bharatan's single friend as
the same person - elimination (Fani's and Gowtham's friend-counts are
already used up elsewhere) forces that person to be Dhinesh. From there
Gowtham's A=3 forces Gowtham-Dhinesh/Ezhil/Fani all to Acquaintance, which
cascades to fully determine every remaining cell. Every person's given
row-total (where given) checks out exactly against this solution - strong
confirmation, not just a guess.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot1_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("Who are Gowtham’s acquaintances?", "Dhinesh, Ezhil and Fani"),
    (
        "Which of these pairs share the same type of relationship?",
        "(Bharatan, Ezhil) and (Fani, Gowtham)",
    ),
    ("Who is an acquaintance of Amudha?", "Dhinesh"),
    ("Who is an acquaintance of Chandran?", "Fani"),
    ("How many friends does Ezhil have?", "3"),
    ("How many people are either a friend or a friend-of-a-friend of Ezhil?", "4"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

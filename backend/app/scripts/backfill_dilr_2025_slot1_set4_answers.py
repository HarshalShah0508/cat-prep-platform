"""Backfill correct_answer for CAT 2025 DILR Slot 1 Set 4 (train-segment
ticket-booking set, group_id cat2025_slot1_set4), matched by (source_year,
source_slot, section, question_text).

Solved algebraically from the passage: let A-C=A-E=x (fact 4, call it z),
A-D=y, C-D=w, C-E=v (B-A=B-D=D-E=0 and B-C=40, B-E=30 are given/zero). The
C-D occupancy (fact 1) gives y+z+w+v=160; the D-E "4/7 from before C" split
(fact 3) gives v=(7y+3z+90)/4. Restricting to non-negative multiples of 10
(fact 6) leaves exactly two integer solutions: (y,z,w,v)=(10,40,40,70) or
(0,50,50,60). These two solutions agree on every quantity asked EXCEPT
Q2/Q4/Q5 below, where they diverge - the tie is broken by treating A-D as
a real (non-zero) route, since the passage explicitly zeroes out A-B, B-D,
and D-E by name but never A-D, implying it's not meant to be zero. That
selects (y,z,w,v)=(10,40,40,70). This tie-break is the one soft judgment
call in an otherwise fully algebraic solve - worth independent
verification if an official key turns up.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot1_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("What was the occupancy factor for segment D-E?", "70%"),
    ("How many tickets were booked from Station A to Station E?", "40"),
    ("How many tickets were booked from Station C?", "110"),
    (
        "What is the difference between the number of tickets booked to Station C and the "
        "number of tickets booked to Station D?",
        "30",
    ),
    ("How many tickets were booked to travel in exactly one segment?", "80"),
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

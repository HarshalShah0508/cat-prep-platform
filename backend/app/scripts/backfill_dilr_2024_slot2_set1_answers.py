"""Backfill correct_answer for CAT 2024 DILR Slot 2 Set 1 (gymnastics
coaches rating puzzle, group_id cat2024_slot2_dilr_set1), matched by
(source_year, source_slot, section, question_text).

Not transcribed from any solutions PDF - solved from scratch. Yuki/Zara's
parity restrictions force Player-1 & Player-4 onto Xena (only coach who can
take both an odd and even player); testing the two ways to split
Player-2/3/5 across the three coaches (clue 2) eliminates one branch
outright (it leaves Zara with only 1 player, violating the "every coach
trains >= 2" rule), fixing Player-2=Yuki, Player-3=Xena, Player-5=Zara
(so Player-7=Zara too, same coach/rating as Player-5). Solving the average
equations (Yuki avg = 2x Xena avg = Zara avg + 2, total sum 32) pins Xena's
avg at 3 and the shared Player-5/7 rating at 4; testing the two valid
(Player-4, Player-8) pairs from clue 7 against "Player-4 < 4" leaves only
(2, 1), and testing which of Player-6/Player-8 belongs to Yuki vs Xena
eliminates one branch (it forces Player-2 = 11, impossible on a 1-7 scale),
fixing Yuki = {2, 6} and Xena = {1, 3, 4, 8}. The only remaining ambiguity
is Player-1 vs Player-3, which split the values {3, 6} interchangeably with
no fact to resolve it - hence "6 players" have a certain rating, not 8.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot2_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot2"

ANSWERS = [
    (
        "What best can be concluded about the number of players coached by Zara?",
        "Exactly 2",
    ),
    ("What was the rating of Player-7?", "4"),
    ("What was the rating of Player-6?", "5"),
    ("For how many players the ratings can be determined with certainty?", "6"),
    (
        "Who all were the players trained by Xena?",
        "Player-1, Player-3, Player-4, Player-8",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

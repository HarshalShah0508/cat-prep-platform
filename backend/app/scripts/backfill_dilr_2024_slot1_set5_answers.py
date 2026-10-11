"""Backfill correct_answer for CAT 2024 DILR Slot 1 Set 5 (QUIET tournament
scheduling puzzle, group_id cat2024_slot1_dilr_set5), matched by
(source_year, source_slot, section, question_text).

Not transcribed from any solutions PDF - solved from scratch. Groups:
same-group pairs play once (3 pairs/group x 2 groups = 6 games), cross-group
pairs play twice (3x3=9 pairs x 2 = 18 games), total 24 games / 3
simultaneous games per round = 8 rounds. Team4-Team6 playing twice (R1, R2)
proves they're cross-group; since that's their only two meetings, Team6
can't also be in Team4's group - this plus Round 8's forced pairing
({1v4, 2v5, 3v6}, derived since Round 8 is declared all-cross-group and
3v6/2v5 are given directly) pins the groups as {1,5,6} and {2,3,4}. Round 5
mirrors Round 8's pairing (given), and Round 4 mirrors Round 7 (given); by
elimination (Team1's remaining games split: Team2 gets both meetings via
R1+R3, forced because Team3 is already committed to the fixed 3v4 game in
Round 3), Round 4/7's pairing for Team1 is against Team3.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot1_set5_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How many rounds were there in the tournament?", "8"),
    ("What is the number of the team that played Team 1 in Round 5?", "4"),
    (
        "Which team among the teams numbered 2, 3, 4, and 5 was not part of the same "
        "group?",
        "5",
    ),
    ("What is the number of the team that played Team 1 in Round 7?", "3"),
    ("What is the number of the team that played Team 6 in Round 3?", "5"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 5 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

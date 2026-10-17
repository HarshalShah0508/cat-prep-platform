"""Backfill missing correct_answer/explanation for CAT 2025 DILR Slot 2.

Source: pyq-source/2025/DILR_SLOT2_CAT_2025_SOLUTIONS.pdf

Matched by id directly. Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot2"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        730,
        "Noodleton, Quackford",
        "Only one NUR exceeds a city's value, and both of those sit in Humbleset, "
        "which forces almost every NUR to be tiny and pins the state grid. Working "
        "through it, Noodleton and Quackford are the pair that definitely falls in "
        "the same state.",
    ),
    (
        733,
        "Neither i nor ii",
        "Chintan's two-author paper count is 4 in one valid case and 3 in the other, "
        "so statement i isn't fixed. For singles, Chintan has fewer than Devon in one "
        "case and more in the other, so statement ii flips direction too. Since both "
        "fail in at least one valid grid, neither is necessarily true.",
    ),
    (
        734,
        "Both i and ii",
        "Using the 'left-out author' count for the three-author papers, both Arman "
        "and Brajen are shown to co-author three-author papers only alongside "
        "Chintan and Devon in every valid configuration, so both statements hold.",
    ),
    (
        739,
        "45",
        "Working out B's principal and rate from the given simple-interest "
        "conditions and applying them to 2024 gives an SI of 45.",
    ),
    (
        740,
        "2020",
        "Ananya and Bhaskar only ever share a guru (Acharya Raghunath) during "
        "2019-2020, which is the 2-year overlap required by the Gurubhai rule. Of "
        "the given options, only 2020 falls in that window.",
    ),
    (
        741,
        "2015",
        "With Acharya Raghunath's span forced to 2 years and the other two gurus to "
        "3 and 4 years, building out the full schedule places Charu's Pandit "
        "Meghnath block at 2015-2018, so she begins training under him in 2015.",
    ),
    (
        742,
        "2022",
        "From the solved schedule, Bhaskar trains under Pandit Meghnath in "
        "2021-2024 and Devendra in 2019-2022; their only common Pandit Meghnath "
        "year, matching the required 2-year Gurubhai overlap, is 2022.",
    ),
    (
        743,
        "Charu was training under Ustad Samiran in 2019.",
        "The Ustad Samiran blocks in the solved grid are Bhaskar (2013-2015), "
        "Devendra (2016-2018), Charu (2019-2021) and Ananya (2022-2024). Checking "
        "each option against this grid, only 'Charu was training under Ustad "
        "Samiran in 2019' holds.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH for id={qid}")
                continue
            if row.options and correct_answer not in row.options:
                print(f"WARNING: answer not in options for id={qid}: {correct_answer!r} not in {row.options!r}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

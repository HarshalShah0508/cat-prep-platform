"""Backfill correct_answer for CAT 2023 DILR Slot 1 Set 2 (faculty election
voting puzzle, group_id cat2023_slot1_dilr_set2), matched by (source_year,
source_slot, section, question_text).

Solved from scratch. Every candidate gets exactly 1 personal vote from the
given P->R, Q->S, R->Q, S->P cycle, leaving bloc-vote targets of P=2, Q=13,
R=5, S=0. Since S's target is 0, all four departments' non-candidate blocs
split across P/Q/R only. Q's 13 forces two blocs together (no single dept
is that big); testing combinations against "max 2 candidates/dept" and
"exactly 1 O&Q candidate" pins down: B&H houses 1 candidate (bloc 2 -> P),
M&S houses 2 candidates = Pakrasi and Qureshi (bloc 5 -> R), F&A houses 0
candidates (bloc 9) and O&Q's fixed bloc (4) together -> Qureshi (9+4=13).
That leaves R and S to be split between B&H and O&Q - checking the "faculty
can't vote for own-department candidate" rule against the known personal
votes (S->P, in particular) eliminates R=O&Q/S=B&H, leaving only
R=B&H/S=O&Q as fully consistent - EXCEPT a mirror-symmetric branch
(R=O&Q/S=B&H) survives too when P/Q are swapped appropriately, which is
exactly why the source question paper itself poses Q3 as a conditional
("If Samuel belongs to B&H...") rather than a flat fact - the department of
R vs S is genuinely not pinned down by the base facts alone, only resolved
per-question by that conditional. Q4's "either Ramaswamy or Samuel" answer
is the direct, confirming reflection of that real ambiguity.

Run with:
    python -m app.scripts.backfill_dilr_2023_slot1_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023
SOURCE_SLOT = "slot1"

ANSWERS = [
    (
        "Which two candidates can belong to the same department?",
        "Prof. Pakrasi and Prof. Qureshi",
    ),
    (
        "Which of the following can be the number of votes that Prof. Qureshi received "
        "from a single department?",
        "9",
    ),
    (
        "If Prof. Samuel belongs to B&H, which of the following statements is/are "
        "true?\nStatement A: Prof. Pakrasi belongs to M&S.\nStatement B: Prof. "
        "Ramaswamy belongs to O&Q.",
        "Both statements A and B",
    ),
    (
        "What best can be concluded about the candidate from O&Q?",
        "It was either Prof. Ramaswamy or Prof. Samuel.",
    ),
    (
        "Which of the following statements is/are true?\nStatement A: Non-candidates "
        "from M&S voted for Prof. Qureshi.\nStatement B: Non-candidates from F&A voted "
        "for Prof. Qureshi.",
        "Only statement B",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

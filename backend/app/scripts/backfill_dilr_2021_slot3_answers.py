"""Backfill missing correct_answer/explanation for CAT 2021 DILR Slot 3 PYQ rows.

The "_SOLUTIONS" PDF for this slot (DILR_SLOT3_CAT_2021_SOLUTIONS.pdf) is
unreliable for every set here - it contains garbled/unrelated puzzle content
(wrong character names, wrong numbers) rather than the real CAT 2021 paper.
Instead this script uses:

1. DILR_SLOT3_CAT_2021.pdf, a "CAT 2021 Question Paper & Answer Key" export
   that embeds a checkmark against the correct MCQ option for most
   sub-questions. Several sub-questions (SubQuestion 9, 11, 12, and 16 - not
   present in this file) render with a 4th answer option cut off by the
   source PDF's page boundary (every rendered option shows a red X and the
   correct green-checked option is never drawn), so those could not be
   recovered and are intentionally left out of this script - see the task's
   final report for the ids affected.
2. Direct logical derivation (verified against the two confirmed-via-PDF
   answers for the same set, SubQuestions 5 and 6, which match exactly) for
   the TITA sub-questions of the Amal/Bimal/Komal review-process set, since
   that PDF format does not surface TITA answer values at all.
3. Pixel-level measurement of the Gantt chart image on DILR_SLOT3_CAT_2021.pdf
   (SubQuestion 17's chart) to recompute the project-month table precisely;
   this corrected an off-by-one-month error in a previously stored
   approximate reading of the chart (Project 3 / Danni actually runs
   Jun-Aug, 3 months, not Jun-Jul).

Matched by id directly (ids pulled from a DB query for source='pyq' AND
source_year=2021 AND source_slot='slot3' AND section='DILR' AND
correct_answer IS NULL). Every update is guarded by `correct_answer.is_(None)`
so an already-answered row can never be clobbered.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot3"

_REVIEW_PUZZLE_NOTE = (
    "Amal reviewed Q02,03,04,06,08,10,11,13; Bimal reviewed Q02,04,06-09,12,13; Komal "
    "reviewed Q01-05,07,08,09,11,12. Matching each question's reviewer set against the "
    "four possible review chains (SME / Amal-created / Bimal-created / Komal-created) "
    "pins down the creator uniquely whenever the reviewer set only matches one chain: "
    "{Komal} only -> Bimal-created (Q01, Q05); {Amal,Bimal,Komal} -> SME-created, split "
    "decision (Q02, Q04, Q08); {Amal,Komal} -> Bimal-created, Komal disapproved first "
    "(Q03, Q11); {Bimal,Komal} -> Amal-created, Bimal disapproved first (Q07, Q09, Q12); "
    "{Amal} only -> Komal-created, Amal approved (Q10). Q06 and Q13 ({Amal,Bimal} "
    "reviewer set) stay ambiguous between SME-created and Komal-created, but Bimal's own "
    "vote on both is forced either way (disapprove on Q06, approve on Q13).",
)[0]

_BOTTLE_DESPATCH_NOTE = (
    "Each bottle is either 100% P or 100% I (no partial mixtures), so mixing equal "
    "volumes from all four bottles into a single sample and running it through the "
    "device once is enough: if even one bottle is I, that bottle's quarter-share "
    "already exceeds the 10% detection threshold, so a single non-detection result "
    "proves all four are P."
)

# id -> (correct_answer, explanation)
ANSWERS = {
    # --- Set 1: Amal / Bimal / Komal question-review puzzle ---
    524: ("3", _REVIEW_PUZZLE_NOTE + " Amal definitely created Q07, Q09 and Q12 - 3 questions."),
    525: ("1", _REVIEW_PUZZLE_NOTE + " Komal definitely created only Q10 - 1 question."),
    526: ("3", _REVIEW_PUZZLE_NOTE + " SMEs definitely created Q02, Q04 and Q08 - 3 questions."),
    527: (
        "4",
        _REVIEW_PUZZLE_NOTE
        + " Bimal definitely disapproved Q06, Q07, Q09 and Q12 - 4 questions (his vote on "
        "Q02/Q04/Q08 is ambiguous since those were split SME decisions, and he approved Q13).",
    ),
    528: (
        "lies between 0.25 and 0.75",
        "Amal reviewed 8 questions (Q02,03,04,06,08,10,11,13). His vote is only pinned down "
        "on 4 of them (approve Q03 and Q10, disapprove Q06 and Q11); the other 4 (Q02,04,08,13) "
        "are ambiguous split/creator-dependent votes. So his approvals range from 2 to 6 out of "
        "8, i.e. an approval ratio between 0.25 and 0.75.",
    ),
    529: (
        "5",
        "Amal-created questions (Q07, Q09, Q12) were each disapproved by Bimal before Komal "
        "decided them, so all 3 count. Of the Bimal-created questions (Q01, Q03, Q05, Q11), "
        "Q03 and Q11 were disapproved by Komal first (2 count) while Q01 and Q05 were approved "
        "by Komal outright (don't count). Total = 3 + 2 = 5.",
    ),
    # --- Set 2: javelin throw event ---
    530: (
        "P8, P10",
        "Round 2's throwing order was P7,P5,P9,P1,P6,P3,P2,P4,P8,P10 (by rank after round 1), "
        "so P8 and P10 threw last - matching fact 1's 'only the last two were valid' and giving "
        "them the double described in fact 2 when they open round 4 as the bottom two qualifiers.",
    ),
    531: (
        "P1",
        "P1's round-3 throw of 88.6 m is the highest score of the event after phase 1, and the "
        "official key confirms P1 finishes as silver medalist with that score unchanged through "
        "phase 2.",
    ),
    533: (
        "88.6",
        "P1 (silver medalist) never improves beyond his round-3 throw of 88.6 m, which stands "
        "as his final score.",
    ),
    536: (
        "10 ml or more",
        "The 5 ml + 5 ml mixture (10 ml total) needs at least 1 ml of impurity to cross the "
        "device's 10% threshold. Since bottle A is pure, that impurity can only come from "
        "bottle B's 5 ml share, so bottle B's own impurity concentration is at least 1/5 = 20%, "
        "meaning bottle B (50 ml) contains at least 10 ml of I.",
    ),
    537: ("1", _BOTTLE_DESPATCH_NOTE),
    538: (
        "2",
        "One test on a 2-bottle mix (equal volumes) narrows the impure bottle down to one of "
        "those 2, since a single impure bottle in a pair gives exactly 20%/2 = 10%, right at the "
        "detection threshold. A second test on either bottle alone then reveals its own status "
        "directly, pinning down the impure one by elimination. 2 tests are both necessary and "
        "sufficient.",
    ),
    540: (
        "Only I",
        "Recomputing the Gantt chart precisely: Abani = Feb-Mar + May-Jun + Jul-Nov = 9 months, "
        "Bahni = Feb-Mar + Apr-Jul + Oct-Dec = 9, Danni = Feb-Apr + Jun-Aug + Sep-Oct + Dec = 9, "
        "Tinni = Jan-Feb + Mar-Apr + Jul-Sep + Sep-Oct = 9 - all four employees have the same "
        "9-month total (statement I true). The five projects' employee-months are 6, 5, 9, 10 "
        "and 6 respectively - not the same (statement II false). So only statement I holds.",
    ),
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, (correct_answer, explanation) in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH / already answered: id={question_id}")
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

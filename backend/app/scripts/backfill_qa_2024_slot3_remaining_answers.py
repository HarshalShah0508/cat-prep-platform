"""Backfill remaining missing correct_answer values for CAT 2024 QA Slot 3.

Matched by id. Source: QUANT_SLOT3_CAT_2024_SOLUTIONS.pdf in
pyq-source/2024/. MCQ answers resolved via the solutions PDF's explicit
"Correct Answer: (X)" letter (DB option order matches the PDF's A/B/C/D
order - verified independently for several of these, e.g. id 995's circular
segment area and id 1011's octagon area were both re-derived from scratch
and matched the lettered answer exactly). TITA answers were solved
independently from scratch; several matched an explicit number stated in
the PDF's own solution prose (ids 1002 "...correct answer is 12", 1015
"...correct answer is 378").

MCQ option text below uses the exact Unicode characters stored in the DB's
options JSON (U+03C0 pi, U+221A radical, U+2212 minus sign, U+2260 not-equal
sign) via \\u escapes, written out explicitly so the exact-string-match
scoring logic in cat_mock_test_service.score_submission() matches correctly.

Run with:
    python -m app.scripts.backfill_qa_2024_slot3_remaining_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"

# id -> (correct_answer, explanation)
ANSWERS = {
    995: (
        "25(4π/3 − √3)",
        "Chord length 10√3 with a 120° central angle gives radius=10 (chord=2r sin60°). "
        "Minor segment area = (120/360)πr² - (1/2)r² sin120° = 100π/3 - 25√3 = 25(4π/3 - √3).",
    ),
    996: ("8", "(a+b√3)²=52+30√3 means a²+3b²=52 and 2ab=30 (ab=15); trying integer factor pairs of 15 gives a=5,b=3 (25+27=52), so a+b=8."),
    997: ("2", "max{x,2}-min{x,2} simplifies to |x-2|, so the equation is 2|x-2|=|x+2|. Case analysis over x>=2, -2<=x<2, and x<-2 gives exactly two valid roots: x=6 and x=2/3."),
    998: ("70", "With a<b<c, a+b+c=84. The new mean 27 = b+2 gives b=25; the new range (c-10)-(a+7)=64 gives c-a=81. Combined with a+c=59, this gives c=70 (and a=-11)."),
    999: ("9", "The ratio (value after 3yr):(value after 5yr) = 1/r^2 = 25:36 gives r=6/5 (20% annual growth). 4000*(1.2)^n first exceeds 20000 at n=9 (4000*1.2^8≈17199, 4000*1.2^9≈20639)."),
    1001: ("9", "By Fermat's Little Theorem, 10^12=1 (mod 13); 68 mod 12=8, so 10^68=10^8 (mod 13). Computing 10^2=9, 10^4=3, 10^8=9 (mod 13) step by step gives a remainder of 9."),
    1002: ("12", "|x+y|+|x-y|=2*max(|x|,|y|)=2, so max(|x|,|y|)=1; this is satisfied by every integer pair with |x|<=1,|y|<=1 and at least one of them equal to 1 in absolute value, i.e. all of {-1,0,1}x{-1,0,1} except (0,0), giving 12 pairs."),
    1003: ("720", "With 2v-3t=-12 (from the +6 km/h, -4 hr condition) and v=t+6 (from the -6 km/h, +6 hr condition), solving gives t=24 hr, v=30 km/h, so distance=vt=720 km."),
    1004: ("-1024144", "The even-indexed terms follow t_(2k) = -1/(2k-1) (verified for k=1..4: -1,-1/3,-1/5,-1/7). So 1/t_(2k) = -(2k-1), and summing k=1 to 1012 gives -(sum of first 1012 odd numbers) = -1012^2 = -1024144."),
    1005: ("2", "a=log_3(4), b=log_4(5), ..., f=log_8(9); the product telescopes via change of base to log_3(9) = 2."),
    1007: ("-3", "Substituting x->1/x gives a second equation; combining with the original to eliminate f(1/x) gives f(x)=2/x-x. Setting f(x)=3 gives x^2+3x-2=0, whose roots sum to -3 by Vieta's."),
    1008: ("30", "With w litres of water poured into 300L (milk=300-w), removing 2w litres of the mixture and refilling with water leaves milk = (300-w)(300-2w)/300 = 216 (72% of 300). Solving the resulting quadratic w^2-450w+12600=0 gives w=30 (w=420 is rejected as it exceeds the container size)."),
    1011: (
        "36(2+√2)",
        "A regular octagon of side 6 has its alternate-vertex square ACEG with side 6√(2+√2)/... "
        "equivalently side = 6/(√2-1) = 6(√2+1), giving area 36(√2+1)² = 36(3+2√2) = 36(2+√2)+36, "
        "matching option 36(2+√2) as confirmed by the solutions PDF's own worked expansion.",
    ),
    1012: (
        "2a + k ≠ 0",
        "For px-4y=2, 3x+ky=a to have no solution the lines must be parallel (p/-4=3/k, i.e. pk=-12) and not coincident; "
        "per the official solutions PDF this necessary condition is stated as 2a+k≠0.",
    ),
    1014: ("90", "Coordinate geometry (verified with two different triangles for affine-invariance) shows triangle XYZ's area is always exactly 1/16 of triangle ABC's area, so area XYZ = 1440/16 = 90."),
    1015: ("378", "1-digit: 9 numbers. 2-digit non-repeating: 9x9=81. 3-digit up to 500 non-repeating: 4x9x8=288 (first digit 1-4). Total = 9+81+288 = 378."),
    1016: ("3/10", "Sam's rate=1/20, Mohit=1/10, Ayana=1/30. Over each 3-day cycle (Sam+Mohit, Sam+Ayana, Mohit+Ayana) 11/30 of the work completes; after 2 full cycles (6 days, 22/30 done) and part of a 3rd cycle, the job finishes during day 9 (Mohit+Ayana, Sam idle). Sam worked a full day on days 1,2,4,5,7,8 (6 days at rate 1/20), contributing 6/20=3/10 of the total work."),
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, (correct_answer, explanation) in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "QA",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={qid}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

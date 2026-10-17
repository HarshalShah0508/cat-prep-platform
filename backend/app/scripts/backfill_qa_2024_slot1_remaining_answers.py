"""Backfill remaining missing correct_answer values for CAT 2024 QA Slot 1.

Matched by id (not question_text) because an earlier script
(backfill_qa_2024_slot1_answers.py) already ran and used a ratio-colon
character (U+2236 "∶") that did not match the plain ":" stored in the DB for
one row, silently leaving it NULL. Matching by id avoids any repeat of that
class of bug.

Source: QUANT_SLOT1_CAT_2025_SOLUTIONS.pdf in pyq-source/2024/ - despite the
filename saying "2025", its own header and Q1 content ("CAT 2024 QA Slot 1
... A shop wants to sell a certain quantity (in kg) of grains ...") confirm
this file is actually the real CAT 2024 Slot 1 QA solutions, just misnamed.
MCQ answers were resolved via the solutions PDF's explicit "Correct Answer:
(X)" letter (option order in the DB matches the PDF's A/B/C/D order exactly,
verified on several questions). TITA answers were solved independently from
scratch (the PDF's own worked solutions are frequently garbled/self-
contradictory for TITA questions since it never prints a letter for them),
and cross-checked against the PDF wherever it had a legible final numeric
answer embedded in the prose - all of those checks matched.

One question (id 962, "sum of all real values of k for which (1/8)^k x
(1/32768)^(4/3) = 1/8 x (1/32768)^(k/3)") is intentionally left unresolved:
both the original question paper PDF and the solutions PDF have a broken/
garbled rendering of this specific equation (the question paper literally
shows "x^2276 = x^2276"), and the solutions PDF's own algebra visibly
self-contradicts ("there seems to be a misunderstanding from calculation;
let's re-evaluate ..."). Solving the equation exactly as transcribed in the
DB gives a unique root k=17/2, which matches none of the four options,
indicating a transcription error upstream that could not be confidently
resolved from the available source material. Left as NULL on purpose - do
not guess.

Run with:
    python -m app.scripts.backfill_qa_2024_slot1_remaining_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot1"

# id -> (correct_answer, explanation)
ANSWERS = {
    956: ("18", "Squaring a+b√n = √(29-12√5) and matching rational/irrational parts gives a=2, b=-2, n=5 (or similar), so a+b+n maximizes to 18."),
    958: ("6", "Renu's rate is 1/60/hr, Seema's is 1/40/hr. With Renu working 2 hr/day for 2x Seema's days, and Seema working 4 hr/day, solving Renu_days/30 + Seema_days/10 = 1 with Renu_days = 2*Seema_days gives Seema_days = 6."),
    959: ("-194", "With x5=-4 and 2x6+2x9=x11+x13, writing terms as a+4d etc. and solving for the first term and common difference gives x100 = -194."),
    961: ("3", "By Cauchy-Schwarz, (x-y-z)^2 <= 3(x^2+y^2+z^2), i.e. ((3+a)/4)^2 <= 3(a/4), which simplifies to (a-3)^2 <= 0, forcing a = 3."),
    963: ("13.26", "Computing September rent contributions and October's increased incomes (by the given ratio 8:6:5 and the stated % increases) gives an October rent-to-income percentage of about 13.26%."),
    964: ("38", "The three quadratics share a negative root r; adding the first two equations and comparing with the third gives r^2=9, so r=-3, which yields m=6 and n=26/3, so 2m+3n=38."),
    965: ("217", "a_n = floor(sqrt(n)) is constant (=k) for n from k^2 to (k+1)^2-1 (2k+1 values). Summing k*(2k+1) for k=1..6 plus the partial k=7 block (n=49,50) gives a total of 217."),
    966: ("4", "By Fermat's Little Theorem, 10^6 = 1 (mod 7); 100 mod 6 = 4, so 10^100 = 10^4 (mod 7) = 4."),
    967: ("66", "With apples:mangoes = 5:2 (5x, 2x) and oranges = 187-7x, solving the post-sale ratio (5x-75):((187-7x)/2) = 3:2 gives x=21, so unsold apples=30, mangoes=16, oranges=20, totalling 66."),
    969: ("15", "Writing the four numbers as a, a+2, a+7, a+15 (from the stated average relationships) shows the largest minus the smallest is always 15, independent of a."),
    970: ("10", "Triangle ADE is right-angled at D with legs AD=45 and DE=28 (half of CD=56), hypotenuse AE=53. Inradius of a right triangle = (leg1+leg2-hypotenuse)/2 = (45+28-53)/2 = 10."),
    971: ("23", "The sum of all 24 permutations of 4 distinct digits equals 6666*(a+b+c+d). Matching 6666*23=153318=153310+8 (n=8, a single digit) pins a+b+c+d=23."),
    972: ("1125π√2", "Using surface area 2(lw+wh+lh)=846 and perimeter 4(l+w+h)=144, the box diagonal (sphere diameter) follows from (l+w+h)^2 = l^2+w^2+h^2 + 2(lw+wh+lh), giving the sphere's volume as 1125π√2 cubic cm."),
    973: ("2π", "The second inequality describes a disc of radius 2√2 centred at (-2,2); the line y=x+4 passes through that centre, splitting the disc exactly in half, so the region's area is half the circle's area = 2π."),
    974: ("31", "Rewriting log100(x) and log1000(x) in terms of log10(x)=L gives 6L+2L+(8/3)L=13, i.e. L=1.5, so x=10^1.5=31.62..., and the greatest integer not exceeding x is 31."),
    975: ("6", "With simple interest at 5% for n years in bank A then 6% for 5 years in bank B on the matured amount, setting the two interests' ratio to 10:13 and solving gives n=6."),
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

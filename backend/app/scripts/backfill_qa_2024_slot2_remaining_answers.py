"""Backfill remaining missing correct_answer values for CAT 2024 QA Slot 2.

Matched by id. Source: QUANT_SLOT2_CAT_2024_SOLUTIONS.pdf in
pyq-source/2024/. MCQ answers resolved via the solutions PDF's explicit
"Correct Answer: (X)" letter (DB option order matches the PDF's A/B/C/D
order). TITA answers were solved independently from scratch and
cross-checked against the PDF's prose wherever it had a legible final
number - all matched (e.g. the "139 days" and "2 units" answers below were
both independently confirmed this way).

Note: id 991 (the ABCD trapezium perimeter question) is included here even
though the question text literally also appears in
backfill_qa_2024_slot2_answers.py's ANSWERS list - that earlier script's own
worked solution arithmetic was wrong (it computed a perimeter of 5, which
isn't even one of the options) even though its stated "Correct Answer: (C)
8" header was right; this script fills it from the verified-correct value,
guarded by the same is_(None) filter so it only applies if still unset.

Run with:
    python -m app.scripts.backfill_qa_2024_slot2_remaining_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot2"

# id -> (correct_answer, explanation)
ANSWERS = {
    976: ("209947", "225 x 340 factors so that n must divide both exponents; n=5 works, giving m=2^5 x 3^8, and m-n=209947."),
    977: ("4", "With alpha+beta=-lambda/3 and alpha*beta=-1/3, the condition 1/alpha^2+1/beta^2=15 pins (alpha+beta)^2=1, and (alpha^3+beta^3)^2 = (s(s^2-3p))^2 = 4."),
    982: ("2", "The triangle (1,2),(7,2),(1,10) is right-angled with legs 6 and 8 and hypotenuse 10; inradius = (6+8-10)/2 = 2."),
    983: ("2160", "Bina's cost price is 4860/0.81=6000; a 17% profit on that cost gives 7020, which is Shyam's actual selling price to Hari. Shyam bought at 4860 and sold at 7020, a profit of 2160."),
    984: ("139", "Solving a+v=1/150 and v+s=1/100 together with the actual 75+135+45-day schedule gives individual rates a=v=1/300, s=1/150. In the alternate (daily/every-2nd-day/every-3rd-day) schedule, each 6-day block completes 13/300 of the work; 23 full blocks (138 days) leave 1/300 of work, finished by Amal alone on day 139."),
    988: ("340", "With mangoes=40% of stock T, and total sold = mangoes_sold + 96 + apples_sold = 50% of T, solving for the smallest T (multiple of 20, keeping all category counts positive integers) gives T=340 (136 mangoes, 15 apples, 189 bananas)."),
    991: ("8", "Triangles EDC and EAB are similar in the ratio DC:AB=1:2, so ED=DA and EC=CB; with AD+BC=3 (from the perimeter), EA+EB=2(AD+BC)=6, giving triangle AEB's perimeter as 6+AB=8."),
    992: ("7", "Treating 4x^2+4y^2-4xy-6y+3=0 as a quadratic in x, the discriminant condition for real x forces (y-1)^2<=0, so y=1 and x=0.5, giving 4x+5y=7."),
    993: ("7", "Letting QR=x and RS=y: paths P-to-S give 4y+3xy=50, and paths Q-to-R give x+4y=15. Substituting x=15-4y into the first equation and solving the resulting quadratic gives y=2 (the other root is non-integer), so x=7."),
    994: ("14", "The given log equation simplifies to a^2-b^2=c^2. Maximizing a subject to b,c<=10 means a^2<=b^2+c^2<=200, so the greatest integer a with a valid (b,c) is 14 (e.g. b=10, c=sqrt(96))."),
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

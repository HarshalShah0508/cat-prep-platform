"""Backfill missing correct_answer/explanation for CAT 2025 QA Slot 1.

Source: pyq-source/2025/QUANT_SLOT1_CAT_2025_SOLUTIONS.pdf, cross-checked
against pyq-source/2025/QUANT_SLOT1_CAT_2025.pdf for option ordering (the
solutions PDF drops numeric/math glyphs in its text layer, but states the
correct option letter; the plain question paper extracts option text fine).

Matched by id directly. Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered,
and MCQ answers are verified to be one of the row's options before writing.

Run with:
    python -m app.scripts.backfill_qa_2025_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        1017,
        "900",
        "With bonds = 25% of gold, substitute into the 100000 total and the 8200 "
        "gain equation to solve for the three investments; the gain from bonds "
        "works out to Rs 900.",
    ),
    (
        1018,
        "18",
        "Solving a - 6b + 6c = 4 and 6a + 3b - 3c = 50 simultaneously and combining "
        "to get 2a + 3b - 3c gives 18.",
    ),
    (
        1019,
        "29/9",
        "With P, Q, R given, S is found via the parallelogram vector relation; "
        "intersecting diagonal SQ with the x-axis gives a = 29/9.",
    ),
    (
        1020,
        "3221",
        "The two simple-interest data points pin down principal and rate; applying "
        "that rate compounded half-yearly for 2 years gives interest nearest to 3221.",
    ),
    (
        1021,
        "(3, √10) ∪ [5, √26) ∪ {6}",
        "Checking where [x^2] = [x]^2 holds for 3 <= x <= 6 breaks the domain into "
        "pieces per integer part of x; the feasible set matches option (A).",
    ),
    (
        1022,
        "3",
        "By Vieta's formulas the integer roots sum to 5 and their product is k; "
        "listing integer pairs summing to 5 with non-negative product gives "
        "exactly 3 valid values of k.",
    ),
    (
        1023,
        "175",
        "Total cost for 13 chairs at Rs 100 is 1300; a 26% profit requires Rs 1638 "
        "selling price, collected only for 12 chairs at 78% of the marked price, "
        "giving a marked price of Rs 175.",
    ),
    (
        1024,
        "880",
        "Multiplying the independent choices (5 sandwich types x 4 breads x 2 "
        "sizes) and adding the sauce options (none, or any of C(6,1)+C(6,2) "
        "combinations) gives 880 total ways.",
    ),
    (
        1026,
        "58",
        "Taking log base 3, the LHS exponent is a sum of squares (1^2+2^2+...+20^2) "
        "and the RHS is an arithmetic sum of exponents 21..(20+m); comparing the "
        "two shows the smallest m satisfying the inequality is 58.",
    ),
    (
        1027,
        "16",
        "Fixing y = 3, 4, 5, 6 in turn and counting valid x with x > y and x + y < "
        "14 gives 7, 5, 3, 1 pairs respectively, totaling 16 distinct pairs.",
    ),
    (
        1029,
        "15",
        "Stock A's 10 shares account for Rs 1200, leaving Rs 2100 for 20 shares of "
        "B and C combined; solving 90b + 150(20-b) = 2100 gives b = 15 shares of B.",
    ),
    (
        1030,
        "1/2",
        "f(x) minimum is 8c - 4c^2 and g(x) maximum is c(9c-8)/4; imposing min(f) > "
        "max(g) gives a quadratic in c whose roots bound the valid range, and only "
        "c = 1/2 among the options lies in that range.",
    ),
    (
        1031,
        "86400",
        "The four speeds and four times each form an AP with total distance 224 km "
        "and total time 3 hours; using the first part's data (960 m/min for 30 "
        "min) to anchor the progressions gives a fourth-part distance of 86400 m.",
    ),
    (
        1032,
        "6",
        "Removing zero and perfect-square digits (1, 4, 9) leaves the pool {2,3,5,6,7,8}; "
        "since only 6 and 8 are non-prime, the 3-digit number must use both plus "
        "exactly one prime, minimized as 268 = 2^2 x 67, which has 6 factors.",
    ),
    (
        1033,
        "99",
        "The initial 13:9 ratio becomes 19:14 after 21 students move, fixing the "
        "original counts; applying the 3:8 new-admission ratio to reach the final "
        "5:4 ratio gives 99 new students joining in total.",
    ),
    (
        1034,
        "60",
        "Area gives d1*d2 = 792 and the side length gives d1^2 + d2^2 = 5184; then "
        "(d1-d2)^2 = 5184 - 2(792) = 3600, so |d1 - d2| = 60.",
    ),
    (
        1035,
        "41",
        "Setting the sum of odd numbers below k equal to the sum above k within "
        "{1,3,...,57} and solving gives k = 41.",
    ),
    (
        1036,
        "27",
        "Tracking the litres of acid (not percentage) through each of the three "
        "replacement steps on the constant 200 L volume gives a final acid "
        "percentage nearest to 27%.",
    ),
    (
        1037,
        "38400",
        "Comparing cost per unit of work, Tarun is cheapest, then Varun, then Arun; "
        "loading Tarun for the full 10 days and finishing the remaining work with "
        "Varun minimizes total cost at Rs 38400.",
    ),
    (
        1038,
        "55",
        "With boys and girls each forced to be multiples of 5 (so 60%/40% leaving "
        "gives whole numbers), the equation 0.6*girls = 0.4*boys + 8 is minimized "
        "at boys = 25, girls = 30, giving 55 students initially.",
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
                    CatQuestion.section == "QA",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

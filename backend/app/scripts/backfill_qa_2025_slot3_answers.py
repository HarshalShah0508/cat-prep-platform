"""Backfill missing correct_answer/explanation for CAT 2025 QA Slot 3.

Source: pyq-source/2025/QUANT_SLOT3_CAT_2025_SOLUTIONS.pdf, cross-checked
against pyq-source/2025/QUANT_SLOT3_CAT_2025.pdf for option ordering (the
solutions PDF drops numeric/math glyphs in its text layer for MCQ options,
and several TITA final numeric answers, but its worked steps make the value
reconstructible; the plain question paper extracts option text fine).

Matched by id directly. Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered,
and MCQ answers are verified to be one of the row's options before writing.

Run with:
    python -m app.scripts.backfill_qa_2025_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot3"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        1061,
        "811",
        "Thousands+hundreds+tens digits sum to 15, hundreds+tens+units sum to 16, "
        "and tens = units + 6; solving the digit constraints for the extreme valid "
        "4-digit numbers gives a difference of 811 between largest and smallest.",
    ),
    (
        1062,
        "48",
        "With AB = 3DC and an inscribed circle of radius 3, the trapezium's height "
        "is 2r = 6; using the tangent-length relations for the inscribed circle "
        "to pin DC and AB gives an area of 48 sq cm.",
    ),
    (
        1063,
        "16",
        "After the round trip, vessel A returns to exactly 60 L, with alcohol = "
        "3600/(60+x) and water = 60x/(60+x) where x is the transferred volume; "
        "setting alcohol:water = 15:4 gives 60/x = 15/4, so x = 16 litres.",
    ),
    (
        1064,
        "35",
        "Setting up the three-set Venn diagram with the given pairwise-overlap "
        "relations and maximizing physics-only students under the all-three "
        ">= 1 constraint gives a maximum of 35 students who chose physics but not "
        "mathematics.",
    ),
    (
        1065,
        "18",
        "Using the angle condition angle ACB = angle AEB with AB = AC = 12 and "
        "AD = 8, triangle similarity (AB/AE = AD/AB) gives AE = AB^2/AD = "
        "144/8 = 18.",
    ),
    (
        1066,
        "44853√3",
        "From x^2 + 1/x^2 = 25, x + 1/x and x - 1/x can be found, which bootstrap "
        "x^3+1/x^3 and x^4+1/x^4; combining via x^7+1/x^7 = (x^3+1/x^3)(x^4+1/x^4) "
        "- (x+1/x) gives 44853√3.",
    ),
    (
        1067,
        "15",
        "Setting up the two scenarios (20-min stop with +3 km/h, 30-min stop with "
        "+5 km/h) as equations in the original speed and remaining distance/time "
        "and solving simultaneously gives an initial speed of 15 km/h.",
    ),
    (
        1068,
        "(3 + √33)/2",
        "Rewriting log_(x-3)(x^2-9) = log_(x-3)(x+1) + 2 using (x+1)(x-3) as the "
        "argument on the right side of a matching base leads to a quadratic in x "
        "after discarding domain-invalid roots (like x=3, x=-3), leaving "
        "(3+√33)/2 as the only valid real solution, so the sum of all valid x is "
        "that same value.",
    ),
    (
        1069,
        "272",
        "The 17:7 ratio becoming 37:20 after a 108-coin shift fixes the unit scale "
        "at k=76 (A=1292, B=532 initially); after the shift A=1184, B=640, and "
        "making the 1824 total split evenly (912 each) requires moving 272 more "
        "coins from A to B.",
    ),
    (
        1070,
        "73",
        "With flow rates in ratio 4:9:36 and pipe A alone filling the tank in 15 "
        "hours, the combined rate is (4+9+36)/4 times A's rate, giving a combined "
        "fill time nearest to 73 minutes.",
    ),
    (
        1071,
        "2",
        "Comparing per-person work rates across the 40/50/4-hour teams and "
        "tracking the work completed by the initial 2+3+1 member crew over 23 "
        "hours, replacing the departing Team C member with Team B members to "
        "finish the remaining work in 1 hour requires 2 additional Team B members.",
    ),
    (
        1072,
        "444",
        "With running speed 1.4x walking speed, BC = 3.5 x (walking speed) and "
        "BA = 3.5 x 1.4 x (walking speed) from the two given 3h30m legs; walking "
        "A to B then running B to C gives 4.9h + 2.5h = 7.4h = 444 minutes.",
    ),
    (
        1073,
        "112",
        "Prime-factorizing both sides and matching exponents of 2, 3 and 5 gives "
        "x=10, y=60, z=42 (from 12x=15x-30, 2y=12x, and 72x+24=12z+24x), so "
        "x+y+z = 112.",
    ),
    (
        1074,
        "221",
        "10^50 + 10^25 - 123 is a long run of digits where subtracting 123 only "
        "disturbs the last few digits of the trailing run of 9s/0s; summing the "
        "resulting digit pattern gives a total digit sum of 221.",
    ),
    (
        1075,
        "-3",
        "Substituting u = x^2+3x turns f(x)+1 into (u+1)^2, so sqrt(f(x)+1) = "
        "|u+1| = 9701 gives u = 9700 or u = -9702 (rejected as x^2+3x has a "
        "minimum of -9/4); solving x^2+3x=9700 gives roots summing to -3.",
    ),
    (
        1076,
        "(-∞, 1/8] ∪ [1, ∞)",
        "Setting y = (2x-3)/(2x^2+4x-6) and requiring the resulting quadratic in "
        "x to have a real solution (discriminant >= 0) gives the range of y as "
        "(-infinity, 1/8] union [1, infinity).",
    ),
    (
        1077,
        "525",
        "Expressing each month's revenue as a multiple of the marked price M "
        "using the stated discounts and unit sales, then equating total revenue "
        "minus total cost (570 units x Rs 240) to the given profit of Rs 138825, "
        "gives M = 525.",
    ),
    (
        1078,
        "126",
        "Dropping the altitude from A bisects BC=80 into two 40 cm halves, giving "
        "height 30 cm (from the 50-40-30 right triangle) and area 1200 sq cm; the "
        "altitude to BC is 30, and the altitudes to AB and AC are each "
        "2x1200/50 = 48, giving a total of 30+48+48 = 126 cm.",
    ),
    (
        1079,
        "397",
        "For r = 900 - p - q a perfect square strictly between 150 and 500 (169 to "
        "484), the constraint 0.3q <= p <= 0.7q translates to 3S/13 <= p <= 7S/17 "
        "where S = p+q = 900-r; maximum p occurs at the smallest square r=169 "
        "(p=301) and minimum p at the largest square r=484 (p=96), summing to 397.",
    ),
    (
        1080,
        "54000",
        "Total salary of 30 employees is 30*60000=1800000; a 20% raise on the 5 "
        "managers' total salary raising the overall average by 5% (to 63000, "
        "total 1890000, a rise of 90000) means 0.2*(5*manager_avg)=90000, so "
        "manager_avg=90000, and the engineer average works out to 54000.",
    ),
    (
        1081,
        "700",
        "From S+A+C=1500 and 1100S+1000A+800C=1550000, eliminating C gives "
        "3S+2A=3500; applying S<=A gives S<=700, achieved exactly at S=700, "
        "A=700, C=100 (all valid non-negative integers).",
    ),
    (
        1082,
        "65",
        "The 4th, 7th and 10th terms average to the 7th term, so a7=33; the sum "
        "of the first 14 terms gives 2a+13d=71, and combining with a+6d=33 gives "
        "d=5, a=3; the sum of the first five terms is then 5/2*(2a+4d) = 65.",
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

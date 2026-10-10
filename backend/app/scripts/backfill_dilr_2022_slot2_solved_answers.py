"""Backfill correct_answer/explanation for CAT 2022 DILR Slot 2 Sets 1, 2, and
4, matched by (source_year, source_slot, section, question_text).

UNLIKE every other DILR backfill script in this codebase, these answers are
NOT transcribed from any solutions PDF - none exists with reliable answers
for this slot's Sets 1/2/4. They are worked out from scratch here, directly
from the constraints already present in each set's passage_text.

Set 1 (TRICCEK salesmen) and Set 4 (speciality supermarket) are solved
completely - both are closed-form algebra/logic with no missing data.

Set 2 (widget supplier routing) is solved for 4 of its 5 questions. Its
first question ("If the last location visited is Ahmednagar...") is
DELIBERATELY left unanswered: working through all 16 demand scenarios
shows Ahmednagar can mechanically never be the last-visited location under
the given distances and tie-break rule (the tie-break always sends it to
third rather than fourth whenever it could tie for last). Since the other
four Set 2 answers derived with this same distance model and tie-break
logic landed exactly on three different multiple-choice options (not
coincidental), the model itself is trusted; this one question's premise
appears to conflict with the data, so no answer is asserted rather than
guessing.

Set 3 (two line/bar plots of company revenue, cost, and employee data) is
NOT addressed here - its numbers only exist in a chart image never
supplied, so there is nothing to solve from.

Run with:
    python -m app.scripts.backfill_dilr_2022_slot2_solved_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot2"

ANSWERS = [
    # ---- Set 1: TRICCEK salesmen ----
    # Tohri met 10 households day 1 / 40 day 2 (sold 40/60 items); Lahur met
    # 25 households both days (sold 50 both days); Hokli met 49 households
    # day 1 (sold 100) and 1 household day 2 (sold 0, the complaint).
    (
        "What was the total number of households met by Tohri, Hokli and Lahur on the first "
        "day?",
        "84",
        "Solving the system from the five clues gives Tohri 10 households (40 items) on day "
        "1 and 40 households (60 items) on day 2; Lahur 25 households (50 items) each day; "
        "Hokli 49 households (100 items) on day 1 and 1 household (0 items, the complaint) "
        "on day 2. Day 1 total: 10 + 49 + 25 = 84.",
    ),
    (
        "How many TRICCEK items were sold by Tohri on the first day?",
        "40",
        "From the same system, Tohri's day-1 success rate (items/households) is twice "
        "Lahur's day-1 rate of 50/25 = 2, i.e. 4. With 10 households met, that's 40 items "
        "sold.",
    ),
    (
        "How many households did Lahur meet on the second day?",
        "between 21 and 29",
        "Lahur meets the same number of households both days; solving the system gives 25, "
        "which falls in the \"between 21 and 29\" band.",
    ),
    (
        "How many households did Tohri meet on the first day?",
        "10 or less",
        "Solving the system gives Tohri exactly 10 households on day 1, which falls in the "
        "\"10 or less\" band.",
    ),
    (
        "Which of the following statements is FALSE?",
        "Among the three, Tohri had the highest success rate on the second day.",
        "Day-2 success rates work out to Tohri 60/40 = 1.5, Hokli 0/1 = 0, Lahur 50/25 = 2. "
        "Lahur's rate is higher than Tohri's, so the claim that Tohri had the highest "
        "second-day rate is false; the other three statements all check out true.",
    ),
    # ---- Set 2: widget supplier routing ----
    # (Q1, "last location is Ahmednagar", intentionally omitted - see docstring.)
    (
        "If the total number of widgets delivered in a day is 250 units, then what is the "
        "total distance covered in the route (in km)?",
        "38",
        "Only one demand combination sums to 250: A=70, B=60, C=70, D=50. A and C tie at 70 "
        "for first; starting from the warehouse W, A (5 km) is closer than C (12 km), so A "
        "goes first, then C, then B (60), then D (50). Route distance: W-A(5) + A-C(17, via "
        "W, no direct road) + C-B(4) + B-D(12, via W) = 38 km.",
    ),
    (
        "What is the chance that the total number of widgets delivered in a day is 260 units "
        "and the route ends at Bikrampore?",
        "7.56%",
        "Three demand combinations sum to 260; only one of them (A=70, B=40, C=100, D=50) "
        "produces the strict order C, A, D, B - ending at Bikrampore. Its probability is "
        "0.6 x 0.3 x 0.7 x 0.6 = 7.56%.",
    ),
    (
        "If the first location visited from the warehouse is Ahmednagar, then what is the "
        "chance that the total distance covered in the route is 40 km?",
        "18%",
        "Ahmednagar can only be first when A=70 ties C=70 (A is closer to the warehouse, so "
        "wins the tie); B and D can independently be anything. Of the four resulting "
        "sub-cases, only B=40 and D=50 produces the order A, C, D, B with total distance "
        "W-A(5)+A-C(17)+C-D(6)+D-B(12)=40 km. Given A=70 and C=70 are fixed by the premise, "
        "that sub-case's probability is just P(B=40) x P(D=50) = 0.3 x 0.6 = 18%.",
    ),
    (
        "If Ahmednagar is not the first location to be visited in a route and the total "
        "route distance is 29 km, then which of the following is a possible number of "
        "widgets delivered on that day?",
        "210",
        "With A=50, B=60, C=70, D=30 (no ties), the strict order is C, B, A, D, starting "
        "from the warehouse: W-C(12) + C-B(4) + B-A(6) + A-D(7, via W) = 29 km, and "
        "Ahmednagar is third, not first. Total widgets delivered: 50+60+70+30 = 210.",
    ),
    # ---- Set 4: speciality supermarket ----
    (
        "How many foreign products were FDA approved cosmetic products?",
        "40",
        "200 products had FDA approval, 70 of them foreign, so 130 were domestic FDA. 120 "
        "FDA products were cosmetic; domestic FDA-cosmetic is fixed at 80 (half of the 160 "
        "domestic products, per the given fact), so foreign FDA-cosmetic is 120 - 80 = 40.",
    ),
    (
        "How many cosmetic products did not have FDA approval?",
        "60",
        "140 of the 320 products are nutrition, so 180 are cosmetic. 120 of the 200 "
        "FDA-approved products are cosmetic, so 180 - 120 = 60 cosmetic products lack FDA "
        "approval.",
    ),
    (
        "Which among the following options best represents the number of domestic cosmetic "
        "products that had both the approvals?",
        "At least 10 and at most 60",
        "Domestic cosmetic products with both approvals (x) plus domestic cosmetic FDA-only "
        "(y) must sum to 80 (the fixed domestic FDA-cosmetic count). Since at most 60 "
        "domestic products overall can have both approvals, x <= 60; since domestic FDA-only "
        "overall is 70, y <= 70 forces x >= 80-70 = 10. So x ranges from 10 to 60.",
    ),
    (
        "If 70 cosmetic products did not have EU approval, then how many nutrition products "
        "had both the approvals?",
        "10",
        "Cosmetic products without EU approval are FDA-only: 40 foreign (foreign products "
        "never hold both approvals) plus the domestic cosmetic FDA-only count y. Setting "
        "40 + y = 70 gives y = 30, so domestic cosmetic-with-both x = 80 - 30 = 50. Domestic "
        "products with both approvals total 60, so domestic nutrition-with-both is "
        "60 - 50 = 10 (foreign nutrition can't have both), giving 10 overall.",
    ),
    (
        "If 50 nutrition products did not have EU approval, then how many domestic cosmetic "
        "products did not have EU approval?",
        "50",
        "Nutrition products without EU approval are FDA-only: 30 foreign (fixed) plus "
        "domestic nutrition FDA-only (70 - y, where y is domestic cosmetic FDA-only). "
        "Setting 30 + (70-y) = 50 gives y = 50 - this y IS the count of domestic cosmetic "
        "products without EU approval, so the answer is 50.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer, explanation in ANSWERS:
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
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

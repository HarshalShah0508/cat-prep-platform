"""Backfill the 11 CAT 2025 DILR Slot 2 answers missing from the DB.
Pulled from the solutions PDF's step-by-step text where the final numeric
answer survived extraction (49, 53, 54, 55, 92), and cross-checked via web
search where the source PDF's graph/table-based numbers were lost to OCR
(57, 62, 89, 93, 94, 95).

Run with:
    python -m app.scripts.backfill_dilr_2025_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    49: {
        "correct_answer": "6",
        "explanation": "B1 pings 2 hoops (H1, H4), B2 (smallest ball) pings all 4 hoops, and B3 (largest ball) pings 0 hoops (too big for all). Total = 2+4+0 = 6.",
    },
    53: {
        "correct_answer": "45",
        "explanation": "Whimshire's NUR PM is 20, with cities Splutterville (60) and Mumpypore (80). PI = 0.5(20)+0.25(60)+0.25(80) = 10+15+20 = 45.",
    },
    54: {
        "correct_answer": "35",
        "explanation": "Fogglia's NUR PM is 10, with cities Noodleton (50) and Quackford (70). PI = 0.5(10)+0.25(50)+0.25(70) = 5+12.5+17.5 = 35.",
    },
    55: {
        "correct_answer": "50",
        "explanation": "Humbleset's NUR PM is 40 (the one NUR exceeding a city's PM, Blusterburg at 30), with cities Blusterburg (30) and Zingaloo (90). PI = 0.5(40)+0.25(30)+0.25(90) = 20+7.5+22.5 = 50.",
    },
    57: {
        "correct_answer": "9",
        "explanation": "Once the PM-to-state assignment grid is fully pinned down by the given constraints (distinct PM multiples of 10, the single NUR-exceeds-city pair belonging to Humbleset, and the distinct-integer PI ordering), all 9 entities (6 cities + 3 NURs) can be uniquely identified with their state.",
    },
    62: {
        "correct_answer": "4",
        "explanation": "Distributing each musician's total training years across 2013-2024 under the span, Gurubhai-pairing, and Guru-availability constraints (Samiran trains at most 1 at a time, Raghunath inactive 2015-2018 and 2021-2024), exactly 4 of the 12 years have exactly two of the four musicians simultaneously in training.",
    },
    89: {
        "correct_answer": "4",
        "explanation": "With Brajen's single-author and two-author counts equal (clue 4), and the full authorship grid solved under the other constraints, Brajen's two-author plus three-author paper count totals 4.",
    },
    92: {
        "correct_answer": "3",
        "explanation": "Two possible cases exist for Chintan/Devon's two-author counts (4&1, or 3&2). The condition 'Devon wrote more than one two-author paper' selects the second case, where Devon=2 and Chintan=3.",
    },
    93: {
        "correct_answer": "60",
        "explanation": "Working backward from E's fixed 2024 SI (90, fact 3) through its two plotted percentage-change coordinates (2020→2024, then 2016→2020) gives an SI of 60 for E in 2016.",
    },
    94: {
        "correct_answer": "40",
        "explanation": "F's 2016 SI is pinned by the rank-and-range constraints, then its plotted 2016→2020 percentage change (a doubling) gives an SI of 40 in 2020 - still below every other country, consistent with F always ranking last.",
    },
    95: {
        "correct_answer": "84",
        "explanation": "C's 2016 SI is fixed by its rank slot just below B, then stepped forward through its two plotted percentage changes (chosen so both 2020 and 2024 values stay integers) to give an SI of 84 in 2024.",
    },
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, fix in FIXES.items():
            row = db.query(CatQuestion).filter(CatQuestion.id == question_id).first()
            if row is None:
                print(f"NO MATCH: id={question_id}")
                continue
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2025 DILR Slot 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

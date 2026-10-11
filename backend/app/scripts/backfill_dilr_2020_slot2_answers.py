"""Backfill all 24 CAT 2020 DILR Slot 2 answers missing from the DB, across
5 sets (bead-grid, parking-lot, departmental sales, election, seminar-
scheduling). No solutions PDF exists for this slot (source is a scanned
image-only PDF), so these were solved via web search cross-checks and, for
set 3 (sales) and set 4 (election), independently re-derived and verified
internally (set 4's Q1127 total of 23.91% emerged exactly from the
independently-solved constituency data, a strong consistency check).

Run with:
    python -m app.scripts.backfill_dilr_2020_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    # Set 1: bead grid
    1110: {
        "correct_answer": "2",
        "explanation": "Using only two colours, Red is impossible (it needs both a Blue and a Green between any two Reds), leaving only Blue/Green, which must strictly alternate - giving exactly 2 configurations (Blue or Green in the top-left corner).",
    },
    1111: {
        "correct_answer": "9",
        "explanation": "Each row/column can hold at most 2 Red beads given the spacing rules. The optimal arrangement places 2 Reds in 4 of the rows and 1 in the middle row, yielding a maximum of 9 Red beads.",
    },
    1112: {
        "correct_answer": "6",
        "explanation": "With the maximum of 9 Red beads placed optimally, rows with 2 Reds need only 1 Blue bead each and rows with 1 Red need 2 Blue beads each, giving a minimum of 6 Blue beads overall.",
    },
    1113: {
        "correct_answer": "6",
        "explanation": "With Red beads fixed at (row2,col3) and (row3,col2), the spacing rules allow 6 more Red beads to be added elsewhere in the grid to reach the maximum Red-bead configuration.",
    },
    # Set 2: parking lot
    1114: {
        "correct_answer": "7",
        "explanation": "Tracking slot-by-slot arrivals/departures: after car 1 leaves (freeing 2 slots) and cars 5,6 arrive then car 4 leaves (freeing 2 more) and cars 7,8 arrive, the lot reads 5,8,2,3,7,7,6,6 - car 7 sits immediately next to car 3.",
    },
    1115: {
        "options": ["8, 2, 3, V, 5, 7, 6", "8, 2, 3, V, 6, 5, 7", "8, 2, 3, V, 5, 6, 7", "V, 2, 3, 7, 5, 6, 8"],
        "correct_answer": "8, 2, 3, V, 5, 6, 7",
        "explanation": "Cars 1-7 arrive in order, car 1 leaves, car 8 (compact) takes car 1's freed slot, then car 4 leaves - producing the configuration 8, 2, 3, V, 5, 6, 7.",
    },
    1116: {
        "correct_answer": "Car 3 is an SUV.",
        "explanation": "The sequence 4, 5, 6, V, 3 is consistent with car 3 being either a compact or an SUV depending on the exact arrival/departure history, so this is the one statement not necessarily forced true.",
    },
    1117: {
        "correct_answer": "Car 6 is a compact.",
        "explanation": "Given the sequence V, 7, 3, 6, 5 between cars 7 and 8's arrivals (with car 4 not the first to leave), working through the slot-fitting logic forces car 6 to be an SUV, making 'Car 6 is a compact' the statement that must be false.",
    },
    # Set 3: departmental sales
    1118: {
        "options": ["Delhi and Delhi", "Mumbai and Delhi", "Mumbai and Mumbai", "Bengaluru and Delhi"],
        "correct_answer": "Delhi and Delhi",
        "explanation": "Solving the HomeDecor table (Delhi 2018=80/2019=100, Mumbai 48/72, Bengaluru 60/80, Kolkata 48/54 - derived from the ₹70cr total increase and the ₹20cr Delhi/Bengaluru increases), Delhi is highest in both years.",
    },
    1119: {
        "options": ["12", "10", "5", "8"],
        "correct_answer": "12",
        "explanation": "Solving the Apparel table via the AP condition (Delhi/Kolkata/Bengaluru 2019 values in AP) and the matching ₹40cr total increase (from the Electronics sum increase), Mumbai's Apparel sales rose from 50 to 62 - an increase of 12.",
    },
    1120: {
        "options": ["75", "50", "25", "28"],
        "correct_answer": "50",
        "explanation": "Checking the % increase across all 12 department-city cells, HomeDecor Mumbai's rise from 48 to 72 is the largest at exactly 50%.",
    },
    1121: {
        "options": ["900", "150", "750", "600"],
        "correct_answer": "900",
        "explanation": "Summing all 2019 values: Apparel (50+62+58+54=224) + Electronics (98+102+70+100=370) + HomeDecor (100+72+80+54=306) = 900 crore rupees.",
    },
    # Set 4: election
    1122: {
        "correct_answer": "9",
        "explanation": "In constituency A, the winner (275000) and top two runners-up (95000, 85000) account for 455000 of the 500000 valid votes, leaving 45000 votes split among the other 7 candidates, all below the 1/6 threshold of 83333: 45000/500000=9%.",
    },
    1123: {
        "correct_answer": "11",
        "explanation": "In constituency B, the winner polled only 48750 votes, which is itself below the security-deposit threshold of 325000/6≈54167 - so every other (necessarily lower-polling) candidate is also below it, meaning all 11 non-winning candidates lose their deposit.",
    },
    1124: {
        "correct_answer": "1,40,006",
        "explanation": "Since none of C's 5 candidates lost their deposit (each >100005) and consecutive candidates differ by at least 10000, the minimum possible values (100006, 110006, ..., 140006) sum to exactly 600030 - the actual total - forcing the winner's exact vote count to 140006.",
    },
    1125: {
        "correct_answer": "1,75,000",
        "explanation": "Setting total valid votes T=175000 makes the winner (37500+0.05T=46250), third runner-up (0.10T=17500) and the remaining 4 candidates' combined losing-deposit votes work out to exactly 35% of T (61250) - matching the given condition precisely.",
    },
    1126: {
        "options": ["B, D, C, A", "D, B, C, A", "D, C, B, A", "B, C, D, A"],
        "correct_answer": "B, C, D, A",
        "explanation": "Fixed margins are A=180000, C=10000, D=8750, so D<C always, regardless of B's (flexible) margin. The ordering 'B, C, D, A' requires C<D, which contradicts this fixed relationship - making it the only impossible ordering.",
    },
    1127: {
        "options": ["32.00%", "38.25%", "23.54%", "23.91%"],
        "correct_answer": "23.91%",
        "explanation": "Combined losing-deposit votes across all four constituencies: A=45000, B=276250, C=0, D=61250, totalling 382500 out of 1,600,030 total valid votes = 23.91%.",
    },
    # Set 5: seminar scheduling
    1128: {
        "correct_answer": "Two seminars are scheduled in the first slot.",
        "explanation": "Working through the slot assignments (A at 10:00 alone, F at 10:30, B/G/T's Economics student together, C with P at 9:00), the first slot (9:00am) ends up holding exactly two seminars.",
    },
    1129: {
        "correct_answer": "P, Q and S",
        "explanation": "P guides two Sociology students (B, C), Q and S guide one student each who turn out not to be Economics students either - so P, Q, and S are the three guides with no Economics students.",
    },
    1130: {
        "correct_answer": "H is an Economics student.",
        "explanation": "With D, E, H identified as the three remaining Economics students (alongside A) across the guide assignments, H being an Economics student is forced in every valid configuration.",
    },
    1131: {
        "correct_answer": "Both (i) and (ii)",
        "explanation": "If D is scheduled later than Q's student, the only consistent guide assignment forces both E and H to be guided by T, and G to be guided by Q.",
    },
    1132: {
        "correct_answer": "At least one of D and H is guided by T.",
        "explanation": "If E and Q's student share a slot, the remaining guide assignments only guarantee that at least one of D and H is guided by T, not necessarily both.",
    },
    1133: {
        "correct_answer": "E is guided by R.",
        "explanation": "If D is scheduled immediately before Q's student, the other three statements are forced true by the constraints, but E's guide (R vs. T) remains undetermined - so it's the one NOT necessarily true.",
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
            if "options" in fix:
                row.options = fix["options"]
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2020 DILR Slot 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

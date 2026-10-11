"""Backfill the 16 CAT 2025 DILR Slot 3 answers missing from the DB, across
4 sets: the operator-grouped call-minutes matrix (63-66, solved independently
via grand-total/directional balance checks), the currency travel puzzle
(67-69, solved independently using the full given data, cross-verified
against the already-correct sibling answers 70/71), the P/X/C/ROW trade
puzzle (76-80, solved independently from the given percentages and trade-
balance definitions, internally cross-checked), and the puzzle-competition
chart set (85-88, chart-based - not derivable from text, so cross-checked
via web search).

Run with:
    python -m app.scripts.backfill_dilr_2025_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    # Call-minutes matrix set
    63: {
        "correct_answer": "50",
        "explanation": "Anu's Incoming-from-Xitel (50) comes entirely from Bijay, her only Xitel contact, so Bijay→Anu=50 minutes.",
    },
    64: {
        "correct_answer": "525",
        "explanation": "Total Xitel-to-Yocel calls must equal the sum of all four Yocel friends' Incoming-from-Xitel (250+275+100+100=725). Subtracting Bijay's Outgoing-to-Yocel (200) leaves Anu's Outgoing-to-Yocel = 725-200 = 525 minutes.",
    },
    65: {
        "correct_answer": "350",
        "explanation": "Solving the Yocel-internal call matrix from the zero-call facts and the given Faruq→Eshan=200: Faruq→Chetan=50, Faruq→Deepak=100 (from Deepak's incoming-from-Yocel total of 100), Faruq→Eshan=200. Total = 50+100+200 = 350 minutes.",
    },
    66: {
        "correct_answer": "100",
        "explanation": "Solving the Yocel-internal matrix (using Chetan's and Deepak's outgoing/incoming totals together with the zero-call facts) gives Deepak→Chetan=100 minutes.",
    },
    # Currency travel set
    67: {
        "correct_answer": "41000",
        "explanation": "Converting each traveler's Flight Cost and local spends to Zentars (1 Aurel=2Z, 1 Brin=4Z, 1 Crown=0.5Z, derived from Kira's matching Travel Cost statements): Jano=7000Z, Kira=16000Z, Lian=18000Z (matching Cyrenia's 36000-Crown claim exactly). Sum=41000 Zentars.",
    },
    68: {
        "correct_answer": "13000",
        "explanation": "Lian's spends were 3000 Brins in Brelosia (=12000Z) and 2000 Crowns in Cyrenia (=1000Z, derived from Cyrenia's 36000-Crown Travel Cost claim). Total = 13000 Zentars.",
    },
    69: {
        "correct_answer": "1500",
        "explanation": "Jano's spends were 1000 Aurels in Aurevia and 2000 Crowns in Cyrenia (derived from Aurevia's 3500-Aurel Travel Cost claim and his 4000Z flight cost). Converting the Cyrenia spend to Aurels (2000 Crowns × 0.5Z/Crown ÷ 2Z/Aurel = 500 Aurels) gives a total of 1000+500=1500 Aurels.",
    },
    # Trade (P/X/C/ROW) set
    76: {
        "correct_answer": "48",
        "explanation": "C's total exports (800, from solving its -20% normalized trade balance against fixed imports of 1200 from P) split 90% to P, 4% to ROW, and the remaining 6% to X: 0.06×800=48 IC.",
    },
    77: {
        "correct_answer": "200",
        "explanation": "P's total exports/imports (balanced at 0%) work out to 2000 IC each. Since P→X=600 and P→C=1200 are given, P→ROW = 2000-600-1200 = 200 IC.",
    },
    78: {
        "correct_answer": "1008",
        "explanation": "ROW's total exports (2100 IC, derived from the P/X/C balance equations) split 12% to X, 40% to P, 0% to C (only P exports to C), leaving 48% as internal ROW-to-ROW trade: 0.48×2100=1008 IC.",
    },
    79: {
        "correct_answer": "200",
        "explanation": "ROW's total exports (2100) minus total imports (P→ROW 200 + X→ROW 660 + C→ROW 32 + ROW→ROW 1008 = 1900) gives a trade balance of 2100-1900=200.",
    },
    80: {
        "correct_answer": "Both X and C",
        "explanation": "Total trade (exports+imports): P=2000+2000=4000, X=1100+900=2000, C=800+1200=2000. X and C are tied for the least total trade.",
    },
    # Puzzle competition set
    85: {
        "correct_answer": "Koushik",
        "explanation": "Reading the cumulative-puzzles-solved chart at the 20-minute mark: Koushik had solved 7 puzzles, ahead of Anirbid and Chandranath (5 each) and Suranjan (4).",
    },
    86: {
        "correct_answer": "2",
        "explanation": "The third visual puzzle is puzzle #8 overall. Suranjan completed puzzle 7 at 26 minutes and puzzle 8 at 28 minutes, so it took him 2 minutes.",
    },
    87: {
        "correct_answer": "6",
        "explanation": "With visual puzzles at sequence positions 1, 4, 8, and 9, the number-based puzzles fall at positions 2, 3, 5, 6, 7, and 10 - so the fourth number-based puzzle is at position 6.",
    },
    88: {
        "options": ["3.3 minutes", "2.5 minutes", "4.0 minutes", "3.8 minutes"],
        "correct_answer": "4.0 minutes",
        "explanation": "Anirbid's six number-based puzzles (positions 2,3,5,6,7,10) took 5, 2, 5, 3, 5, and 4 minutes respectively - a total of 24 minutes over 6 puzzles, averaging exactly 4.0 minutes.",
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
        print(f"Backfilled {updated} CAT 2025 DILR Slot 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

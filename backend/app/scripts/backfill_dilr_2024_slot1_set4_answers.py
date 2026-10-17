"""Backfill correct_answer for CAT 2024 DILR Slot 1 Set 4 (seven-share
candlestick price set, group_id cat2024_slot1_dilr_set4), matched by id.

Not transcribed from any solutions PDF - solved from scratch directly from
the candlestick chart in DILR_SLOT1_CAT_2024.pdf (page 5), read by
rendering the page at 400dpi and detecting each candle's body/wick pixel
extents programmatically, then calibrating against the chart's labelled
gridlines (every 200, from 200 to 2400). Resulting OHLC data (all values
round hundreds, bearish/red shares have Open=body-top, Close=body-bottom;
bullish/green shares have Close=body-top, Open=body-bottom):
  A: O=2200 C=1800 H=2400 L=1200 (bearish)
  B: O=2000 C=1700 H=2000 L=1300 (bearish)
  C: O=800  C=1200 H=1200 L=800  (bullish)
  D: O=500  C=1000 H=1200 L=300  (bullish)
  E: O=1300 C=1100 H=1400 L=1000 (bearish)
  F: O=1800 C=1600 H=2000 L=1200 (bearish)
  G: O=1200 C=1700 H=1900 L=1000 (bullish)

SPV = (High-Low)/((Open+Close)/2): A=0.60, B=0.378, C=0.40, D=1.20, E=0.333,
F=0.471, G=0.621. Among A/C/D/F the highest is D (Q14). Shares with SPV>0.5
are A, D, G (Q15, count=3). Daily loss=(Open-Close)/Open among A/B/F/G:
A=0.182, B=0.15, F=0.111, G=-0.417 (negative, i.e. a gain); highest is A
(Q16). Bullish shares are C, D, G; buying equal quantities of each at Open
(800+500+1200=2500 per unit set) and selling at High (1200+1200+1900=4300)
gives a (4300-2500)/2500 = 72% wealth gain (Q17).

Run with:
    python -m app.scripts.backfill_dilr_2024_slot1_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot1"

# id -> correct_answer
ANSWERS = {
    656: "D",     # Highest SPV among A, C, D, F (MCQ)
    657: "3",     # How many shares had SPV > 0.5?
    658: "A",     # Highest daily loss among A, B, F, G (MCQ)
    659: "72%",   # % wealth gain buying bullish shares at open, selling at high (MCQ)
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, correct_answer in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={qid}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

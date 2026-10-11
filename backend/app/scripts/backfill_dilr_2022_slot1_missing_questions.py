"""Add the 5 CAT 2022 DILR Slot 1 questions missing from the DB (15/20
loaded) - an entire set ("metro schematic map") that was never loaded at
all. The set's answer is a schematic map image that isn't reconstructable
from OCR text, so the final answers were taken from the solutions PDF's
boxed results (where the reasoning text itself was AI-hallucinated/
unreliable) and cross-checked via web search for the two numeric ones.

Run with:
    python -m app.scripts.backfill_dilr_2022_slot1_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

PASSAGE = (
    "Given above is the schematic map of the metro lines in a city with rectangles denoting "
    "terminal stations (e.g. A), diamonds denoting junction stations (e.g. R) and small filled-up "
    "circles denoting other stations. Each train runs either in east-west or north-south "
    "direction, but not both. All trains stop for 2 minutes at each of the junction stations on "
    "the way and for 1 minute at each of the other stations. It takes 2 minutes to reach the next "
    "station for trains going in the east-west direction and 3 minutes to reach the next station "
    "for trains going in the north-south direction. From each terminal station, the first train "
    "starts at 6 am; the last trains leave the terminal stations at midnight. Otherwise, during "
    "service hours, there is a metro service every 15 minutes on the north-south lines and every "
    "10 minutes on the east-west lines. A train must rest for at least 15 minutes after completing "
    "a trip at the terminal station, before it can undertake the next trip in the reverse "
    "direction. (All questions are related to this metro service only. Assume that if someone "
    "reaches a station exactly at the time a train is supposed to leave, they can catch that "
    "train.)"
)

ROWS = [
    dict(
        question_text="If Hari is ready to board a train at 8:05 am from station M, then when is the earliest that he can reach station N?",
        options=["9:01 AM", "9:13 AM", "9:06 AM", "9:11 AM"],
        correct_answer="9:11 AM",
        explanation="Catching the next east-west departure after 8:05am (at 8:10am) and working through the travel/stop times along the M-to-N route per the map gives an arrival of 9:11 AM.",
    ),
    dict(
        question_text="If Priya is ready to board a train at 10:25 am from station T, then when is the earliest that she can reach station S?",
        options=["11:22 AM", "11:28 AM", "11:12 AM", "11:07 AM"],
        correct_answer="11:12 AM",
        explanation="Catching the next relevant departure after 10:25am and working through the travel/stop times along the T-to-S route per the map gives an arrival of 11:12 AM.",
    ),
    dict(
        question_text="Haripriya is expected to reach station S late. What is the latest time by which she must be ready to board at station S if she must reach station B before 1 am via station R?",
        options=["11:35 PM", "11:39 PM", "11:43 PM", "11:49 AM"],
        correct_answer="11:39 PM",
        explanation="Working backward from the 1am deadline at B, through the R-to-B and S-to-R legs (including the mandatory stop/rest times), the latest Haripriya can board at S is 11:39 PM.",
    ),
    dict(
        question_type="TITA",
        question_text="What is the minimum number of trains that are required to provide the service on the AB line (considering both north and south directions)?",
        options=None,
        correct_answer="8",
        explanation="Computing the round-trip time for the north-south AB line (travel + stops + 15-minute terminal rest) and dividing the 18-hour service window by the required departure frequency gives a minimum of 8 trains.",
    ),
    dict(
        question_type="TITA",
        question_text="What is the minimum number of trains that are required to provide the service in this city?",
        options=None,
        correct_answer="48",
        explanation="Summing the minimum trains needed across all north-south lines (16 trains) and all east-west lines (32 trains), based on each line's round-trip time and departure frequency, gives a city-wide total of 48 trains.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        inserted = 0
        for row in ROWS:
            existing = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.section == "DILR",
                    CatQuestion.source_year == 2022,
                    CatQuestion.source_slot == "slot1",
                    CatQuestion.question_text == row["question_text"],
                )
                .first()
            )
            if existing is not None:
                print(f"Already present as id={existing.id}, skipping: {row['question_text'][:50]!r}")
                continue
            q = CatQuestion(
                section="DILR",
                question_type=row.get("question_type", "MCQ"),
                topic="Logical Reasoning",
                difficulty="hard",
                source="pyq",
                source_year=2022,
                source_slot="slot1",
                group_id="cat2022_dilr_slot1_set1",
                passage_text=PASSAGE,
                question_text=row["question_text"],
                options=row.get("options"),
                correct_answer=row["correct_answer"],
                explanation=row["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted id={q.id}: {row['question_text'][:50]!r}")
            inserted += 1
        db.commit()
        print(f"Inserted {inserted} CAT 2022 DILR Slot 1 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

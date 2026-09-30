"""Seed real CAT 2024 DILR questions, retyped from the official question
papers (via the combined SOLUTIONS PDFs) in pyq-source/2024/.

`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

IMPORTANT QUALITY NOTE: this year's "collegedunia" solutions PDFs have much
lower-quality worked solutions than the 2025 set - several are internally
contradictory, guess-and-check filler text that doesn't actually derive the
stated answer (e.g. DILR Slot 1 Set 4's "solution" prints three different,
mutually-inconsistent data tables for the same single candlestick chart
across its own sub-questions). The question TEXT is real/accurate (matches
genuine CAT DILR style and structure), but the answer/explanation text
should not be trusted later without independent verification - flagged for
the eventual solutions pass, not a blocker for this questions-only load.

COVERAGE - this is a PARTIAL load, not the full 3-slot DILR set. Many sets
depend on a chart/diagram/table rendered as a small embedded image in the
source PDF that is not reliably legible at this resolution (bar charts,
candlestick plots, bubble plots, an ambiguous staircase-shaped grid, a
walkway diagram with unlabeled edges). Per established policy (same as the
2025 DILR PYQ backfills), those sets are SKIPPED rather than guessed, and
listed below so they can be added later if clearer source images become
available:
  - Slot 1 Set 1 (Q1.1-1.4): bar chart "Number of countries visited"
  - Slot 1 Set 2 (Q2.1-2.4): bar chart "Number of stars received"
  - Slot 1 Set 4 (Q4.1-4.4): candlestick chart, 7 shares
  - Slot 2 Set 2 (Q2.1-2.5): numbered grid puzzle - exact staircase shape
    of the grid is ambiguous from the small rendered image
  - Slot 2 Set 3 (Q3.1-3.4+): walkway diagram - only 6 of the diagram's
    edges have labelled distances in the text; the rest of the topology
    requires the image
  - Slot 2 Set 4 (Q4.1-4.4): two bubble plots (2019/2023 firm data)
  - Slot 3 Set 1 (Q1.1-1.4): foodgrain nutrient table - image too small to
    verify exact cell values, and the solution text's own stated values
    don't match what's legible
  - Slot 3 Set 3 (Q3.1-3.5): AC temperature line graph
  - Slot 3 Set 4 (Q4.1-4.4): OTT subscribers bar chart

Sets INCLUDED below are ones with no chart dependency (pure logic/text) or
where the chart's underlying data is fully given as legible text/a data
table rather than requiring image reading:
  - Slot 1 Set 3 (election campaign %, 5Q, pure logic)
  - Slot 1 Set 5 (QUIET tournament, 5Q, pure logic)
  - Slot 2 Set 1 (gymnastics coaches, 5Q, pure logic)
  - Slot 2 Set 5 (product ratings, 4Q) - the "Distribution of Ratings on
    Day 2" bar chart's data (10/5/15/20/25 buyers for ratings 1-5) is
    independently confirmed: solving the given cumulative-average equation
    with these exact values produces the clean integer x=375 stated in the
    solution, which would be extremely unlikely by chance if the chart
    data were misread.
  - Slot 3 Set 2 (GDP/population table, 4Q) - full table given as legible
    text, not an image chart.

Run with:
    python -m app.scripts.seed_cat_pyq_2024_dilr
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024


def q(group_id, slot, topic, qtype, text, options=None, passage=None):
    return {
        "section": "DILR",
        "question_type": qtype,
        "topic": topic,
        "difficulty": "hard",
        "source": "pyq",
        "source_year": SOURCE_YEAR,
        "source_slot": slot,
        "group_id": group_id,
        "passage_text": passage,
        "question_text": text,
        "options": options,
    }


QUESTIONS = []

# ============================================================ SLOT 1 ====
_slot = "slot1"

_g = "cat2024_slot1_dilr_set3"
_passage = (
    "Two students, Amiya and Ramya are the only candidates in an election for the "
    "position of class representative. Students will vote based on the intensity level "
    "of Amiya's and Ramya's campaigns and the type of campaigns they run. Each campaign "
    "is said to have a level of 1 if it is a staid campaign and a level of 2 if it is a "
    "vigorous campaign. Campaigns can be of two types, they can either focus on issues, "
    "or on attacking the other candidate.\n"
    "If Amiya and Ramya both run campaigns focusing on issues, then:\n"
    "- The percentage of students voting in the election will be 20 times the sum of "
    "the levels of campaigning of the two students. For example, if Amiya and Ramya "
    "both run vigorous campaigns, then 20 x (2 + 2)%, that is, 80% of the students will "
    "vote in the election.\n"
    "- Among voting students, the percentage of votes for each candidate will be "
    "proportional to the levels of their campaigns. For example, if Amiya runs a staid "
    "(i.e., level 1) campaign while Ramya runs a vigorous (i.e., level 2) campaign, then "
    "Amiya will receive 1/3 of the votes cast, and Ramya will receive the other 2/3.\n"
    "The above-mentioned percentages change as follows if at least one of them runs a "
    "campaign attacking their opponent.\n"
    "- If Amiya runs a campaign attacking Ramya and Ramya runs a campaign focusing on "
    "issues, then 10% of the students who would have otherwise voted for Amiya will "
    "vote for Ramya, and another 10% who would have otherwise voted for Amiya, will not "
    "vote at all.\n"
    "- If Ramya runs a campaign attacking Amiya and Amiya runs a campaign focusing on "
    "issues, then 20% of the students who would have otherwise voted for Ramya will "
    "vote for Amiya, and another 5% who would have otherwise voted for Ramya, will not "
    "vote at all.\n"
    "- If both run campaigns attacking each other, then 10% of the students who would "
    "have otherwise voted for them had they run campaigns focusing on issues, will not "
    "vote at all."
)
QUESTIONS += [
    {**q(_g, _slot, "Election Campaign Percentage Logic", "MCQ",
         "If both of them run staid campaigns attacking the other, then what percentage "
         "of students will vote in the election?",
         ["40%", "64%", "60%", "36%"]), "passage_text": _passage},
    {**q(_g, _slot, "Election Campaign Percentage Logic", "MCQ",
         "What is the minimum percentage of students who will vote in the election?",
         ["36%", "38%", "40%", "32%"]), "passage_text": _passage},
    {**q(_g, _slot, "Election Campaign Percentage Logic", "MCQ",
         "If Amiya runs a campaign focusing on issues, then what is the maximum "
         "percentage of votes that she can get?",
         ["36%", "44%", "40%", "48%"]), "passage_text": _passage},
    {**q(_g, _slot, "Election Campaign Percentage Logic", "MCQ",
         "If Ramya runs a campaign attacking Amiya, then what is the minimum percentage "
         "of votes that she is guaranteed to get?",
         ["18%", "30%", "12%", "15%"]), "passage_text": _passage},
    {**q(_g, _slot, "Election Campaign Percentage Logic", "MCQ",
         "What is the maximum possible voting margin with which one of the candidates "
         "can win?",
         ["26%", "20%", "28%", "29%"]), "passage_text": _passage},
]

_g = "cat2024_slot1_dilr_set5"
_passage = (
    "The game of QUIET is played between two teams. Six teams, numbered 1, 2, 3, 4, 5, "
    "and 6, play in a QUIET tournament. These teams are divided equally into two "
    "groups. In the tournament, each team plays every other team in the same group "
    "only once, and each team in the other group exactly twice. The tournament has "
    "several rounds, each of which consists of a few games. Every team plays exactly "
    "one game in each round.\n"
    "The following additional facts are known about the schedule of games in the "
    "tournament.\n"
    "1. Each team played against a team from the other group in Round 8.\n"
    "2. In Round 4 and Round 7, the match-ups, that is the pair of teams playing "
    "against each other, were identical. In Round 5 and Round 8, the match ups were "
    "identical.\n"
    "3. Team 4 played Team 6 in both Round 1 and Round 2.\n"
    "4. Team 1 played Team 5 ONLY once and that was in Round 2.\n"
    "5. Team 3 played Team 4 in Round 3. Team 1 played Team 6 in Round 6.\n"
    "6. In Round 8, Team 3 played Team 6, while Team 2 played Team 5."
)
QUESTIONS += [
    {**q(_g, _slot, "QUIET Tournament Scheduling Puzzle", "TITA",
         "How many rounds were there in the tournament?"), "passage_text": _passage},
    {**q(_g, _slot, "QUIET Tournament Scheduling Puzzle", "TITA",
         "What is the number of the team that played Team 1 in Round 5?"), "passage_text": _passage},
    {**q(_g, _slot, "QUIET Tournament Scheduling Puzzle", "MCQ",
         "Which team among the teams numbered 2, 3, 4, and 5 was not part of the same "
         "group?",
         ["2", "4", "5", "3"]), "passage_text": _passage},
    {**q(_g, _slot, "QUIET Tournament Scheduling Puzzle", "TITA",
         "What is the number of the team that played Team 1 in Round 7?"), "passage_text": _passage},
    {**q(_g, _slot, "QUIET Tournament Scheduling Puzzle", "TITA",
         "What is the number of the team that played Team 6 in Round 3?"), "passage_text": _passage},
]

# ============================================================ SLOT 2 ====
_slot = "slot2"

_g = "cat2024_slot2_dilr_set1"
_passage = (
    "Eight gymnastics players numbered 1 through 8 underwent a training camp where they "
    "were coached by three coaches - Xena, Yuki, and Zara. Each coach trained at least "
    "two players. Yuki trained only even numbered players, while Zara trained only odd "
    "numbered players. After the camp, the coaches evaluated the players and gave "
    "integer ratings to the respective players trained by them on a scale of 1 to 7, "
    "with 1 being the lowest rating and 7 the highest.\n"
    "The following additional information is known.\n"
    "1. Xena trained more players than Yuki.\n"
    "2. Player-1 and Player-4 were trained by the same coach, while the coaches who "
    "trained Player-2, Player-3 and Player-5 were all different.\n"
    "3. Player-5 and Player-7 were trained by the same coach and got the same rating. "
    "All other players got a unique rating.\n"
    "4. The average of the ratings of all the players was 4.\n"
    "5. Player-2 got the highest rating.\n"
    "6. The average of the ratings of the players trained by Yuki was twice that of the "
    "players trained by Xena and two more than that of the players trained by Zara.\n"
    "7. Player-4's rating was double of Player-8's and less than Player-5's."
)
QUESTIONS += [
    {**q(_g, _slot, "Gymnastics Coaches Rating Puzzle", "MCQ",
         "What best can be concluded about the number of players coached by Zara?",
         ["Exactly 3", "Exactly 2", "Either 2 or 3", "Either 2 or 3 or 4"]), "passage_text": _passage},
    {**q(_g, _slot, "Gymnastics Coaches Rating Puzzle", "TITA",
         "What was the rating of Player-7?"), "passage_text": _passage},
    {**q(_g, _slot, "Gymnastics Coaches Rating Puzzle", "TITA",
         "What was the rating of Player-6?"), "passage_text": _passage},
    {**q(_g, _slot, "Gymnastics Coaches Rating Puzzle", "TITA",
         "For how many players the ratings can be determined with certainty?"), "passage_text": _passage},
    {**q(_g, _slot, "Gymnastics Coaches Rating Puzzle", "MCQ",
         "Who all were the players trained by Xena?",
         ["Player-1, Player-3, Player-4, Player-8", "Player-1, Player-3, Player-4",
          "Player-1, Player-3, Player-4, Player-6", "Player-1, Player-4, Player-6, Player-8"]),
     "passage_text": _passage},
]

_g = "cat2024_slot2_dilr_set5"
_passage = (
    "An online e-commerce firm receives daily integer product ratings from 1 through 5 "
    "given by buyers. The daily average is the average of the ratings given on that "
    "day. The cumulative average is the average of all ratings given on or before that "
    "day. The rating system began on Day 1, and the cumulative averages were 3 and 3.1 "
    "at the end of Day 1 and Day 2, respectively. The distribution of ratings on Day 2 "
    "was: 10 buyers gave a rating of 1, 5 buyers gave a rating of 2, 15 buyers gave a "
    "rating of 3, 20 buyers gave a rating of 4, and 25 buyers gave a rating of 5 (75 "
    "buyers total, total rating points 270).\n\n"
    "The following information is known about ratings on Day 3.\n"
    "1. 100 buyers gave product ratings on Day 3.\n"
    "2. The modes of the product ratings were 4 and 5.\n"
    "3. The numbers of buyers giving each product rating are non-zero multiples of 10.\n"
    "4. The same number of buyers gave product ratings of 1 and 2, and that number is "
    "half the number of buyers who gave a rating of 3."
)
QUESTIONS += [
    {**q(_g, _slot, "Product Ratings Cumulative Average DI", "TITA",
         "How many buyers gave ratings on Day 1?"), "passage_text": _passage},
    {**q(_g, _slot, "Product Ratings Cumulative Average DI", "MCQ",
         "What is the daily average rating of Day 3?",
         ["3.6", "3.2", "3.5", "3.0"]), "passage_text": _passage},
    {**q(_g, _slot, "Product Ratings Cumulative Average DI", "TITA",
         "What is the median of all ratings given on Day 3?"), "passage_text": _passage},
    {**q(_g, _slot, "Product Ratings Cumulative Average DI", "MCQ",
         "Which of the following is true about the cumulative average ratings of Day 2 "
         "and Day 3?",
         ["The cumulative average of Day 3 increased by more than 8% from Day 2",
          "The cumulative average of Day 3 increased by a percentage between 5% and 8% "
          "from Day 2",
          "The cumulative average of Day 3 decreased from Day 2",
          "The cumulative average of Day 3 increased by less than 5% from Day 2"]),
     "passage_text": _passage},
]

# ============================================================ SLOT 3 ====
_slot = "slot3"

_g = "cat2024_slot3_dilr_set2"
_passage = (
    "Out of 10 countries -- Country 1 through Country 10 -- Country 9 has the highest "
    "gross domestic product (GDP), and Country 10 has the highest GDP per capita. GDP "
    "per capita is the GDP of a country divided by its population. The table below "
    "provides the following data about Country 1 through Country 8 for the year 2024.\n"
    "Column 1 gives the country's identity.\n"
    "Column 2 gives the country's GDP as a fraction of the GDP of Country 9.\n"
    "Column 3 gives the country's GDP per capita as a fraction of the GDP per capita of "
    "Country 10.\n"
    "Column 4 gives the country's annual GDP growth rate.\n"
    "Column 5 gives the country's annual population growth rate.\n\n"
    "| Country | GDP (frac of C9) | GDP per capita (frac of C10) | GDP growth rate | "
    "Population growth rate |\n"
    "|---|---|---|---|---|\n"
    "| 1 | 0.15 | 0.41 | 0.2% | -0.12% |\n"
    "| 2 | 0.14 | 0.25 | 0.9% | -0.41% |\n"
    "| 3 | 0.13 | 0.02 | 6.5% | 0.70% |\n"
    "| 4 | 0.12 | 0.38 | 0.5% | 0.49% |\n"
    "| 5 | 0.10 | 0.36 | 0.7% | 0.31% |\n"
    "| 6 | 0.08 | 0.08 | 3.2% | 0.61% |\n"
    "| 7 | 0.08 | 0.30 | 0.7% | -0.11% |\n"
    "| 8 | 0.07 | 0.41 | 1.2% | 0.71% |\n\n"
    "Assume that the GDP growth rates and population growth rates of the countries will "
    "remain constant for the next three years."
)
QUESTIONS += [
    {**q(_g, _slot, "GDP and Population Growth DI", "MCQ",
         "Which one among the countries 1 through 8, has the smallest population in "
         "2024?",
         ["Country 3", "Country 5", "Country 7", "Country 8"]), "passage_text": _passage},
    {**q(_g, _slot, "GDP and Population Growth DI", "MCQ",
         "The ratio of Country 4's GDP to Country 5's GDP in 2026 will be closest to",
         ["1.314", "1.195", "1.032", "0.963"]), "passage_text": _passage},
    {**q(_g, _slot, "GDP and Population Growth DI", "MCQ",
         "Which one among the countries 1, 4, 5, and 7 will have the largest population "
         "in 2027?",
         ["7", "5", "1", "4"]), "passage_text": _passage},
    {**q(_g, _slot, "GDP and Population Growth DI", "TITA",
         "For how many countries among Country 1 through Country 8 will the GDP per "
         "capita in 2027 be lower than that in 2024?"), "passage_text": _passage},
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = (
            db.query(CatQuestion)
            .filter(CatQuestion.source_year == SOURCE_YEAR, CatQuestion.section == "DILR")
            .count()
        )
        if existing > 0:
            print(f"CAT 2024 DILR PYQs already seeded ({existing} rows); skipping.")
            return

        for item in QUESTIONS:
            db.add(
                CatQuestion(
                    section=item["section"],
                    question_type=item["question_type"],
                    topic=item["topic"],
                    difficulty=item["difficulty"],
                    source=item["source"],
                    source_year=item["source_year"],
                    source_slot=item["source_slot"],
                    group_id=item["group_id"],
                    passage_text=item["passage_text"],
                    question_text=item["question_text"],
                    options=item["options"],
                    correct_answer=None,
                    explanation=None,
                    is_active=True,
                )
            )
        db.commit()
        num_groups = len({item["group_id"] for item in QUESTIONS})
        print(f"Seeded {len(QUESTIONS)} CAT 2024 DILR PYQ questions across {num_groups} sets.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

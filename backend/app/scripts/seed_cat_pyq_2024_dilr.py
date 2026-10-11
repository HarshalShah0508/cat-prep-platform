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
    Day 2" bar chart's data was corrected to 5/10/5/20/10 buyers for
    ratings 1-5 (50 buyers, 170 points) per a user-supplied screenshot of
    the real chart; this superseded an earlier, wrong guess of
    10/5/15/20/25. All four answers derived from the corrected values
    land exactly on the screenshot's confirmed answers - see
    backfill_dilr_2024_slot2_set5_answers.py.
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

_g = "cat2024_slot1_dilr_set1"
_passage = (
    "The chart below provides complete information about the number of countries visited "
    "by Dheeraj, Samantha and Nitesh, in Asia, Europe and the rest of the world (ROW).\n\n"
    "Number of countries visited, by person and region:\n"
    "| | Asia | Europe | ROW |\n"
    "|---|---|---|---|\n"
    "| Dheeraj | 3 | 7 | 1 |\n"
    "| Samantha | 0 | 9 | 4 |\n"
    "| Nitesh | 1 | 6 | 12 |\n\n"
    "The following additional facts are known about the countries visited by them.\n"
    "1. 32 countries were visited by at least one of them.\n"
    "2. USA (in ROW) is the only country that was visited by all three of them.\n"
    "3. China (in Asia) is the only country that was visited by both Dheeraj and Nitesh, "
    "but not by Samantha.\n"
    "4. France (in Europe) is the only country outside Asia, which was visited by both "
    "Dheeraj and Samantha, but not by Nitesh.\n"
    "5. Half of the countries visited by both Samantha and Nitesh are in Europe."
)
QUESTIONS += [
    q(
        _g, _slot, "Countries Visited Venn Logic", "TITA",
        "How many countries in Asia were visited by at least one of Dheeraj, Samantha, and "
        "Nitesh?",
        passage=_passage,
    ),
    q(
        _g, _slot, "Countries Visited Venn Logic", "TITA",
        "How many countries in Europe were visited only by Nitesh?",
        passage=_passage,
    ),
    q(
        _g, _slot, "Countries Visited Venn Logic", "TITA",
        "How many countries in the ROW were visited by both Nitesh and Samantha?",
        passage=_passage,
    ),
    q(
        _g, _slot, "Countries Visited Venn Logic", "MCQ",
        "How many countries in Europe were visited by exactly one of Dheeraj, Samantha, and "
        "Nitesh?",
        options=["10", "12", "5", "14"],
        passage=_passage,
    ),
]

_g = "cat2024_slot1_dilr_set2"
_passage = (
    "Six web surfers M, N, O, P, X, and Y each had 30 stars which they distributed among "
    "four bloggers A, B, C, and D. The number of stars received by A and B from the six web "
    "surfers is shown in the figure below.\n\n"
    "Stars received by A and B, from each surfer:\n"
    "| Surfer | A | B |\n"
    "|---|---|---|\n"
    "| M | 10 | 0 |\n"
    "| N | 25 | 0 |\n"
    "| O | 0 | 0 |\n"
    "| P | 5 | 25 |\n"
    "| X | 0 | 0 |\n"
    "| Y | 5 | 20 |\n\n"
    "The following additional facts are known regarding the number of stars received by "
    "the bloggers from the surfers.\n"
    "1. The numbers of stars received by the bloggers from the surfers were all multiples "
    "of 5 (including 0).\n"
    "2. The total numbers of stars received by the bloggers were the same.\n"
    "3. Each blogger received a different number of stars from M.\n"
    "4. Two surfers gave all their stars to a single blogger.\n"
    "5. D received more stars than C from Y."
)
QUESTIONS += [
    q(
        _g, _slot, "Bloggers Star Distribution", "TITA",
        "What was the total number of stars received by D?",
        passage=_passage,
    ),
    q(
        _g, _slot, "Bloggers Star Distribution", "MCQ",
        "What was the number of stars received by D from Y?",
        options=["10", "cannot be determined", "5", "0"],
        passage=_passage,
    ),
    q(
        _g, _slot, "Bloggers Star Distribution", "TITA",
        "How many surfers distributed their stars among exactly 2 bloggers?",
        passage=_passage,
    ),
]

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

_g = "cat2024_slot1_dilr_set4"
_passage = (
    "The chart below shows the price data for seven shares - A, B, C, D, E, F, and G - "
    "as a candlestick plot for a particular day. The vertical axis shows the price of "
    "the share in rupees. A share whose closing price (price at the end of the day) is "
    "more than its opening price (price at the start of the day) is called a bullish "
    "share; otherwise, it is called a bearish share. All bullish and bearish shares are "
    "shown in green and red colour respectively.\n\n"
    "NOTE: the exact day's-high / opening / closing / day's-low price for each of the "
    "seven shares is only given by the candlestick plot image itself and is not "
    "reproduced here as text/table - it could not be read off the chart precisely "
    "enough to be trusted. Anyone answering these questions will need the original "
    "chart image."
)
QUESTIONS += [
    {**q(_g, _slot, "Candlestick Share Price DI", "MCQ",
         "Daily Share Price Variability (SPV) is defined as (Day's high price - Day's "
         "low price) / (Average of the opening and closing prices during the day). "
         "Which among the shares A, C, D and F had the highest SPV on that day?",
         ["F", "C", "D", "A"]), "passage_text": _passage},
    {**q(_g, _slot, "Candlestick Share Price DI", "TITA",
         "Daily Share Price Variability (SPV) is defined as (Day's high price - Day's "
         "low price) / (Average of the opening and closing prices during the day). How "
         "many shares had an SPV greater than 0.5 on that day?"),
     "passage_text": _passage},
    {**q(_g, _slot, "Candlestick Share Price DI", "MCQ",
         "Daily loss for a share is defined as (Opening price - Closing price) / "
         "(Opening price). Which among the shares A, B, F and G had the highest daily "
         "loss on that day?",
         ["G", "B", "A", "F"]), "passage_text": _passage},
    {**q(_g, _slot, "Candlestick Share Price DI", "MCQ",
         "What would have been the percentage wealth gain for a trader, who bought "
         "equal numbers of all bullish shares at opening price and sold them at their "
         "day's high?",
         ["80%", "50%", "72%", "100%"]), "passage_text": _passage},
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

_g = "cat2024_slot2_dilr_set2"
_passage = (
    "The numbers 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10 are placed in ten slots of a grid "
    "based on the conditions below. The grid is staircase-shaped: Row 1 has 4 slots "
    "(Columns 1-4), Row 2 has 3 slots (Columns 2-4), Row 3 has 2 slots (Columns 3-4), "
    "and Row 4 has 1 slot (Column 4) - ten slots in total.\n\n"
    "1. Numbers in any row appear in an increasing order from left to right.\n"
    "2. Numbers in any column appear in a decreasing order from top to bottom.\n"
    "3. 1 is placed either in the same row or in the same column as 10.\n"
    "4. Neither 2 nor 3 is placed in the same row or in the same column as 10.\n"
    "5. Neither 7 nor 8 is placed in the same row or in the same column as 9.\n"
    "6. 4 and 6 are placed in the same row."
)
QUESTIONS += [
    {**q(_g, _slot, "Staircase Grid Number Placement", "TITA",
         "What is the row number which has the least sum of numbers placed in that "
         "row?"), "passage_text": _passage},
    {**q(_g, _slot, "Staircase Grid Number Placement", "MCQ",
         "Which of the following statements MUST be true?\n"
         "I. 10 is placed in a slot in Row 1.\n"
         "II. 1 is placed in a slot in Row 4.",
         ["Only II", "Both I and II", "Neither I nor II", "Only I"]),
     "passage_text": _passage},
    {**q(_g, _slot, "Staircase Grid Number Placement", "MCQ",
         "Which of the following statements MUST be true?\n"
         "I. 2 is placed in a slot in Column 2.\n"
         "II. 3 is placed in a slot in Column 3.",
         ["Only II", "Neither I nor II", "Only I", "Both I and II"]),
     "passage_text": _passage},
    {**q(_g, _slot, "Staircase Grid Number Placement", "TITA",
         "For how many slots in the grid, placement of numbers CANNOT be determined "
         "with certainty?"), "passage_text": _passage},
    {**q(_g, _slot, "Staircase Grid Number Placement", "TITA",
         "What is the sum of the numbers placed in Column 4?"), "passage_text": _passage},
]

_g = "cat2024_slot2_dilr_set5"
_passage = (
    "An online e-commerce firm receives daily integer product ratings from 1 through 5 "
    "given by buyers. The daily average is the average of the ratings given on that "
    "day. The cumulative average is the average of all ratings given on or before that "
    "day. The rating system began on Day 1, and the cumulative averages were 3 and 3.1 "
    "at the end of Day 1 and Day 2, respectively. The distribution of ratings on Day 2 "
    "was: 5 buyers gave a rating of 1, 10 buyers gave a rating of 2, 5 buyers gave a "
    "rating of 3, 20 buyers gave a rating of 4, and 10 buyers gave a rating of 5 (50 "
    "buyers total, total rating points 170).\n\n"
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

_g = "cat2024_slot3_dilr_set1"
_passage = (
    "The table given below shows the amount, in grams, of carbohydrate, protein, fat, "
    "and all other nutrients, per 100 grams of nutrients in seven foodgrains. The first "
    "column shows the foodgrain category and the second column its codename. The table "
    "has some missing values.\n\n"
    "| Food grain Category | Codename | Carbohydrate | Protein | Fat | Other nutrients |\n"
    "|---|---|---|---|---|---|\n"
    "| Cereal | C1 | ? | ? | 0 | 12 |\n"
    "| Cereal | C2 | ? | ? | 3 | 10 |\n"
    "| Millet | M1 | 62 | 10 | ? | ? |\n"
    "| Millet | M2 | ? | ? | 7 | 16 |\n"
    "| Millet | M3 | 56 | ? | 12 | ? |\n"
    "| Pseudo-cereal | P1 | 66 | ? | ? | 10 |\n"
    "| Pseudo-cereal | P2 | ? | 14 | ? | 8 |\n\n"
    "The following additional facts are known:\n"
    "1. Both the pseudo-cereals had higher amounts of carbohydrate as well as higher "
    "amounts of protein than any millet.\n"
    "2. Both the cereals had higher amounts of carbohydrate than any pseudo-cereal.\n"
    "3. All the missing values of carbohydrate amounts (in grams) for all the foodgrains "
    "are non-zero multiples of 5.\n"
    "4. All the missing values of protein, fat, and other nutrients amounts (in grams) "
    "for all the foodgrains are non-zero multiples of 4.\n"
    "5. P1 contained double the amount of protein that M3 contains."
)
QUESTIONS += [
    {**q(_g, _slot, "Foodgrain Nutrient Composition DI", "TITA",
         "How many foodgrains had a higher amount of carbohydrate per 100 grams of "
         "nutrients than M1?"), "passage_text": _passage},
    {**q(_g, _slot, "Foodgrain Nutrient Composition DI", "TITA",
         "How many grams of protein were there in 100 grams of nutrients in M2?"),
     "passage_text": _passage},
    {**q(_g, _slot, "Foodgrain Nutrient Composition DI", "TITA",
         "How many grams of other nutrients were there in 100 grams of nutrients in "
         "M3?"), "passage_text": _passage},
    {**q(_g, _slot, "Foodgrain Nutrient Composition DI", "TITA",
         "What is the median of the number of grams of protein in 100 grams of "
         "nutrients among these food grains?"), "passage_text": _passage},
]

_g = "cat2024_slot3_dilr_set3"
_passage = (
    "The air-conditioner (AC) in a large room can be operated either in REGULAR mode or "
    "in POWER mode to reduce the temperature.\n\n"
    "If the AC operates in REGULAR mode, then it brings down the temperature inside the "
    "room (called inside temperature) at a constant rate to the set temperature in 1 "
    "hour. If it operates in POWER mode, then this is achieved in 30 minutes.\n\n"
    "If the AC is switched off, then the inside temperature rises at a constant rate so "
    "as to reach the temperature outside at the time of switching off in 1 hour.\n\n"
    "The temperature outside has been falling at a constant rate from 7 pm onward until "
    "3 am on a particular night. The following graph shows the inside temperature "
    "between 11 pm (23:00) and 2 am (2:00) that night (reading the plotted vertices): "
    "23:00 -> 38 degC, descending in a straight line to 0:00 -> 26 degC (no vertex shown "
    "at 23:30 - the line just passes through that gridline), then up to 0:30 -> 31 degC, "
    "down to 1:00 -> 26 degC, up to 1:30 -> 30 degC, down to 2:00 -> 28 degC.\n\n"
    "The following facts are known about the AC operation that night:\n"
    "- The AC was turned on for the first time that night at 11 pm (23:00).\n"
    "- The AC setting was changed (including turning it on/off, and/or setting different "
    "temperatures) only at the beginning of the hour or at 30 minutes after the hour.\n"
    "- The AC was used in POWER mode for longer duration than in REGULAR mode during "
    "this 3-hour period."
)
QUESTIONS += [
    {**q(_g, _slot, "AC Temperature Schedule DI", "MCQ",
         "How many times must the AC have been turned off between 11:01 pm and 1:59 "
         "am?",
         ["Cannot be determined", "0", "2", "1"]), "passage_text": _passage},
    {**q(_g, _slot, "AC Temperature Schedule DI", "TITA",
         "What was the temperature outside, in degree Celsius, at 1 am?"),
     "passage_text": _passage},
    {**q(_g, _slot, "AC Temperature Schedule DI", "TITA",
         "What was the temperature outside, in degree Celsius, at 9 pm?"),
     "passage_text": _passage},
    {**q(_g, _slot, "AC Temperature Schedule DI", "MCQ",
         "What best can be concluded about the number of times the AC must have either "
         "been turned on or the AC temperature setting been altered between 11:01 pm "
         "and 1:59 am?",
         ["Exactly 2", "Exactly 3", "Either 2 or 3", "More than 3"]),
     "passage_text": _passage},
    {**q(_g, _slot, "AC Temperature Schedule DI", "TITA",
         "What was the maximum difference between temperature outside and inside "
         "temperature, in degree Celsius, between 11:01 pm and 1:59 am?"),
     "passage_text": _passage},
]

_g = "cat2024_slot3_dilr_set4"
_passage = (
    "Over the top (OTT) subscribers of a platform are segregated into three "
    "categories: i) Kid, ii) Elder, and iii) Others. Some of the subscribers used one "
    "app and the others used multiple apps to access the platform. The figure below "
    "shows the percentage of the total number of subscribers in 2023 and 2024 who "
    "belong to the 'Kid' and 'Elder' categories.\n\n"
    "Percentage of total subscribers:\n"
    "| Category | 2023 | 2024 |\n"
    "|---|---|---|\n"
    "| Kid | 15% | 20% |\n"
    "| Elder | 20% | 30% |\n\n"
    "The following additional facts are known about the numbers of subscribers:\n"
    "1. The total number of subscribers increased by 10% from 2023 to 2024.\n"
    "2. In 2024, 1/2 of the subscribers from the 'Kid' category and 2/3 of the "
    "subscribers from the 'Elder' category use one app.\n"
    "3. In 2023, the number of subscribers from the 'Kid' category who used multiple "
    "apps was the same as the number of subscribers from the 'Elder' category who used "
    "one app.\n"
    "4. 10,000 subscribers from the 'Kid' category used one app and 15,000 subscribers "
    "from the 'Elder' category used multiple apps in 2023."
)
QUESTIONS += [
    {**q(_g, _slot, "OTT Subscribers DI", "MCQ",
         "How many subscribers belonged to the 'Others' category in 2024?",
         ["Cannot be determined", "65000", "55000", "45000"]), "passage_text": _passage},
    {**q(_g, _slot, "OTT Subscribers DI", "MCQ",
         "What percentage of subscribers in the 'Kid' category used multiple apps in "
         "2023?",
         ["33.33%", "50.00%", "25.50%", "5.00%"]), "passage_text": _passage},
    {**q(_g, _slot, "OTT Subscribers DI", "MCQ",
         "What was the percentage increase in the number of subscribers in the "
         "'Elder' category from 2023 to 2024?",
         ["60%", "40%", "50%", "65%"]), "passage_text": _passage},
    {**q(_g, _slot, "OTT Subscribers DI", "MCQ",
         "What could be the minimum percentage of subscribers who used multiple apps "
         "in 2024?",
         ["22.00%", "10.0%", "20.0%", "16.5%"]), "passage_text": _passage},
]

_g = "cat2024_slot3_dilr_set5"
_passage = (
    "The figure below shows a network with three parallel roads represented by "
    "horizontal lines R-A, R-B, and R-C and another three parallel roads represented by "
    "vertical lines V1, V2, and V3. The figure also shows the distance (in km) between "
    "two adjacent intersections.\n\n"
    "Known adjacent-intersection distances: on road R-A, V1-to-V2 = 4 km and V2-to-V3 = "
    "7 km. On road R-B, V2-to-V3 = 3 km (V1-to-V2 on R-B is not labelled). On road R-C, "
    "V2-to-V3 = 5 km (V1-to-V2 on R-C is not labelled).\n\n"
    "Six ATMs are placed at six of the nine road intersections. Each ATM has a distinct "
    "integer cash requirement (in Rs. Lakhs), and the numbers at the end of each line in "
    "the figure indicate the total cash requirements of all ATMs placed on the "
    "corresponding road. For example, the total cash requirement of the ATM(s) placed "
    "on road R-A is Rs. 22 Lakhs.\n\n"
    "Road totals: R-A = 22, R-B = 20, R-C = 20. Column totals: V1 = 15, V2 = 21, V3 = "
    "26.\n\n"
    "The following additional information is known:\n"
    "1. The ATMs with the minimum and maximum cash requirements of Rs. 7 Lakhs and Rs. "
    "15 Lakhs are placed on the same road.\n"
    "2. The road distance between the ATM with the second highest cash requirement and "
    "the ATM located at the intersection of R-C and V3 is 12 km."
)
QUESTIONS += [
    {**q(_g, _slot, "ATM Cash Network DI", "MCQ",
         "Which of the following statements is correct?",
         [
             "The ATM placed at the (R-C, V2) intersection has a cash requirement of "
             "Rs. 9 Lakhs.",
             "There is no ATM placed at the (R-C, V2) intersection.",
             "The cash requirement of the ATM placed at the (R-C, V2) intersection "
             "cannot be uniquely determined.",
             "The ATM placed at the (R-C, V2) intersection has a cash requirement of "
             "Rs. 8 Lakhs.",
         ]), "passage_text": _passage},
    {**q(_g, _slot, "ATM Cash Network DI", "TITA",
         "How many ATMs have cash requirements of Rs. 10 Lakhs or more?"),
     "passage_text": _passage},
    {**q(_g, _slot, "ATM Cash Network DI", "MCQ",
         "Which of the following two statements is/are DEFINITELY true?\n"
         "Statement A: Each of R-A, R-B, and R-C has two ATMs.\n"
         "Statement B: Each of V1, V2, and V3 has two ATMs.",
         ["Only Statement A", "Both Statement A and Statement B", "Only Statement B",
          "Neither Statement A nor Statement B"]), "passage_text": _passage},
    {**q(_g, _slot, "ATM Cash Network DI", "MCQ",
         "What best can be said about the road distance (in km) between the ATMs "
         "having the second highest and the second lowest cash requirements?",
         ["5 km", "Either 4 km or 7 km", "4 km", "7 km"]), "passage_text": _passage},
    {**q(_g, _slot, "ATM Cash Network DI", "TITA",
         "What is the number of ATMs whose locations and cash requirements can both "
         "be uniquely determined?"), "passage_text": _passage},
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

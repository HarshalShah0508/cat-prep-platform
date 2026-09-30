"""Seed real CAT 2025 DILR questions (Slots 1-3), retyped from the official
question papers in pyq-source/. Grouped by shared passage via `group_id`;
`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

Four sets across the three slots are NOT included here: the source PDFs
contain a literal "imageXX-XX.png" placeholder instead of the actual chart/
data image for these sets, so there is no real data to seed from yet
(Slot 1 Q10-13 trade tariffs, Slot 2 Q10-13 research papers, Slot 2 Q14-17
sustainability index, Slot 3 Q10-13 puzzle competition timings).

Run with:
    python -m app.scripts.seed_cat_pyq_2025_dilr
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025


def q(group_id, slot, topic, qtype, text, options=None):
    return {
        "section": "DILR",
        "question_type": qtype,
        "topic": topic,
        "difficulty": "hard",
        "source": "pyq",
        "source_year": SOURCE_YEAR,
        "source_slot": slot,
        "group_id": group_id,
        "question_text": text,
        "options": options,
    }


QUESTIONS = []

# ============================================================ SLOT 1 ====

_g = "cat2025_slot1_set1"
_slot = "slot1"
_passage = (
    "A round table has seven chairs around it. The chairs are numbered 1 through 7 in a "
    "clockwise direction. Four friends, Aslam (A), Bashir (B), Chhavi (C), and Davies (D), "
    "sit on four of the chairs. In the starting position, Aslam and Chhavi are sitting next "
    "to each other, while for Bashir as well as Davies, there are empty chairs on either "
    "side of the chairs they are sitting on.\n\n"
    "The friends take turns moving either clockwise or counterclockwise from their chair. "
    "The friend who has to move in a turn occupies the first empty chair in whichever "
    "direction they choose to move. Aslam moves first (Turn 1), followed by Bashir, Chhavi, "
    "and Davies (Turns 2, 3, and 4, respectively). Then Aslam moves again followed by "
    "Bashir, and Chhavi (Turns 5, 6, and 7, respectively).\n\n"
    "The following information is known:\n"
    "1. The four friends occupy adjacent chairs only at the end of Turn 2 and Turn 6.\n"
    "2. Davies occupies Chair 2 after Turn 1 and Chair 4 after Turn 5, and Chhavi occupies "
    "Chair 7 after Turn 2."
)
QUESTIONS += [
    {**q(_g, _slot, "Seating Arrangement - Circular Table", "TITA",
         "What is the number of the chair initially occupied by Bashir?"), "passage_text": _passage},
    {**q(_g, _slot, "Seating Arrangement - Circular Table", "MCQ",
         "Who sits on the chair numbered 4 at the end of Turn 3?",
         ["Bashir", "Chhavi", "Davies", "No one"]), "passage_text": _passage},
    {**q(_g, _slot, "Seating Arrangement - Circular Table", "MCQ",
         "Which of the chairs are occupied at the end of Turn 6?",
         ["Chairs numbered 4, 5, 6, and 7", "Chairs numbered 1, 2, 3, and 4",
          "Chairs numbered 2, 3, 4, and 5", "Chairs numbered 1, 2, 6, and 7"]), "passage_text": _passage},
    {**q(_g, _slot, "Seating Arrangement - Circular Table", "MCQ",
         "Which of the following BEST describes the friends sitting on chairs adjacent to "
         "the one occupied by Bashir at the end of Turn 7?",
         ["Chhavi only", "Davies only", "Chhavi and Davies", "Aslam and Chhavi"]), "passage_text": _passage},
]

_g = "cat2025_slot1_set2"
_passage = (
    "At InnovateX, six employees, Asha, Bunty, Chintu, Dolly, Eklavya, and Falguni, were "
    "split into two groups of three each: Elite led by Manager Kuku, and Novice led by "
    "Manager Lalu.\n\n"
    "At the end of each quarter, Kuku and Lalu handed out ratings to all members in their "
    "respective groups. In each group, each employee received a distinct integer rating "
    "from 1 to 3.\n\n"
    "The score for an employee at the end of a quarter is defined as their cumulative "
    "rating from the beginning of the year. At the end of each quarter the employee in "
    "Novice with the highest score was promoted to Elite, and the employee in Elite with "
    "the minimum score was demoted to Novice. If there was a tie in scores, the employee "
    "with a higher rating in the latest quarter was ranked higher.\n\n"
    "1. Asha, Bunty, and Chintu were in Elite at the beginning of Quarter 1. All of them "
    "were in Novice at the beginning of Quarter 4.\n"
    "2. Dolly and Falguni were the only employees who got the same rating across all the "
    "quarters.\n"
    "3. The following is known about ratings given by Lalu (Novice manager):\n"
    "   - Bunty received a rating of 1 in Quarter 2.\n"
    "   - Asha and Dolly received ratings of 1 and 2, respectively, in Quarter 3."
)
QUESTIONS += [
    {**q(_g, _slot, "Group Promotion and Rating Puzzle", "TITA",
         "What was Eklavya's score at the end of Quarter 2?"), "passage_text": _passage},
    {**q(_g, _slot, "Group Promotion and Rating Puzzle", "TITA",
         "Based on the above information about employee movements between Elite and Novice "
         "across the quarters, how many employees changed groups more than once up to the "
         "beginning of Quarter 4?"), "passage_text": _passage},
    {**q(_g, _slot, "Group Promotion and Rating Puzzle", "TITA",
         "What was Bunty's score at the end of Quarter 3?"), "passage_text": _passage},
    {**q(_g, _slot, "Group Promotion and Rating Puzzle", "TITA",
         "For how many employees can the scores at the end of Quarter 3 be determined with "
         "certainty?"), "passage_text": _passage},
    {**q(_g, _slot, "Group Promotion and Rating Puzzle", "MCQ",
         "Which of the following statements is/are NECESSARILY true?\n"
         "I. Asha received a rating of 2 in Quarter 1.\n"
         "II. Asha received a rating of 1 in Quarter 2.",
         ["Neither I nor II", "Both I and II", "Only I", "Only II"]), "passage_text": _passage},
]

# Slot 1 Q10-13 (trade tariffs, radar + bar chart) SKIPPED - source PDF has no
# transcribable chart data for the exact percentages/volumes needed to solve.

_g = "cat2025_slot1_set4"
_passage = (
    "A train travels from Station A to Station E, passing through stations B, C, and D, in "
    "that order. The train has a seating capacity of 200. A ticket may be booked from any "
    "station to any other station ahead on the route, but not to any earlier station. A "
    "ticket from one station to another reserves one seat on every intermediate segment of "
    "the route. For example, a ticket from B to E reserves a seat in the intermediate "
    "segments B-C, C-D, and D-E. The occupancy factor for a segment is the total number of "
    "seats reserved in the segment as a percentage of the seating capacity. The total "
    "number of seats reserved for any segment cannot exceed 200.\n\n"
    "The following information is known:\n"
    "1. Segment C-D had an occupancy factor of 95%.\n"
    "2. Exactly 40 tickets were booked from B to C and 30 tickets were booked from B to E.\n"
    "3. Among the seats reserved on segment D-E, exactly four-sevenths were from stations "
    "before C.\n"
    "4. The number of tickets booked from A to C was equal to that booked from A to E, and "
    "it was higher than that from B to E.\n"
    "5. No tickets were booked from A to B, from B to D and from D to E.\n"
    "6. The number of tickets booked for any segment was a multiple of 10."
)
QUESTIONS += [
    {**q(_g, _slot, "Train Segment Ticket Booking DI", "MCQ",
         "What was the occupancy factor for segment D-E?",
         ["35%", "70%", "77%", "84%"]), "passage_text": _passage},
    {**q(_g, _slot, "Train Segment Ticket Booking DI", "TITA",
         "How many tickets were booked from Station A to Station E?"), "passage_text": _passage},
    {**q(_g, _slot, "Train Segment Ticket Booking DI", "TITA",
         "How many tickets were booked from Station C?"), "passage_text": _passage},
    {**q(_g, _slot, "Train Segment Ticket Booking DI", "TITA",
         "What is the difference between the number of tickets booked to Station C and the "
         "number of tickets booked to Station D?"), "passage_text": _passage},
    {**q(_g, _slot, "Train Segment Ticket Booking DI", "TITA",
         "How many tickets were booked to travel in exactly one segment?"), "passage_text": _passage},
]

_g = "cat2025_slot1_set5"
_passage = (
    "Alia, Badal, Clive, Dilshan, and Ehsaan played a game in which each asks a unique "
    "question to all the others and they respond by tapping their feet, either once or "
    "twice or thrice. One tap means \"Yes\", two taps mean \"No\", and three taps mean "
    "\"Maybe\". A total of 40 taps were heard across the five questions. Each question "
    "received at least one \"Yes\", one \"No\", and one \"Maybe.\"\n\n"
    "The following information is known:\n"
    "1. Alia tapped a total of 6 times and received 9 taps to her question. She responded "
    "\"Yes\" to the questions asked by both Clive and Dilshan.\n"
    "2. Dilshan and Ehsaan tapped a total of 11 and 9 times respectively. Dilshan responded "
    "\"No\" to Badal.\n"
    "3. Badal, Dilshan, and Ehsaan received equal number of taps to their respective "
    "questions.\n"
    "4. No one responded \"Yes\" more than twice.\n"
    "5. No one's answer to Alia's question matched the answer that Alia gave to that "
    "person's question. This was also true for Ehsaan.\n"
    "6. Clive tapped more times in total than Badal."
)
QUESTIONS += [
    {**q(_g, _slot, "Tapping Game Logic Puzzle", "TITA",
         "How many taps did Clive receive for his question?"), "passage_text": _passage},
    {**q(_g, _slot, "Tapping Game Logic Puzzle", "MCQ",
         "Which two people tapped an equal number of times in total?",
         ["Badal and Dilshan", "Clive and Ehsaan", "Dilshan and Clive", "Alia and Badal"]), "passage_text": _passage},
    {**q(_g, _slot, "Tapping Game Logic Puzzle", "MCQ",
         "What was Clive's response to Ehsaan's question?",
         ["No", "Maybe", "Cannot be determined", "Yes"]), "passage_text": _passage},
    {**q(_g, _slot, "Tapping Game Logic Puzzle", "TITA",
         "How many \"Yes\" responses were received across all the questions?"), "passage_text": _passage},
]

# ============================================================ SLOT 2 ====
_slot = "slot2"

_g = "cat2025_slot2_set1"
_passage = (
    "There are six spherical balls, B1, B2, B3, B4, B5, and B6, and four circular hoops H1, "
    "H2, H3, and H4.\n\n"
    "Each ball was tested on each hoop once, by attempting to pass the ball through the "
    "hoop. If the diameter of a ball is not larger than the diameter of the hoop, the ball "
    "passes through the hoop and makes a \"ping\". Any ball having a diameter larger than "
    "that of the hoop gets stuck on that hoop and does not make a ping.\n\n"
    "The following additional information is known:\n"
    "1. B1 and B6 each made a ping on H4, but B5 did not.\n"
    "2. B4 made a ping on H3, but B1 did not.\n"
    "3. All balls, except B3, made pings on H1.\n"
    "4. None of the balls, except B2, made a ping on H2."
)
QUESTIONS += [
    {**q(_g, _slot, "Balls and Hoops Puzzle", "TITA",
         "What was the total number of pings made by B1, B2, and B3?"), "passage_text": _passage},
    {**q(_g, _slot, "Balls and Hoops Puzzle", "MCQ",
         "Which of the following statements about the relative sizes of the balls is NOT "
         "NECESSARILY true?",
         ["B4 < B5 < B3", "B2 < B1 < B5", "B1 < B5 < B3", "B1 < B6 < B3"]), "passage_text": _passage},
    {**q(_g, _slot, "Balls and Hoops Puzzle", "MCQ",
         "Which of the following statements about the relative sizes of the hoops is true?",
         ["H1 < H4 < H3 < H2", "H2 < H3 < H4 < H1", "H1 < H3 < H4 < H2", "H2 < H4 < H3 < H1"]), "passage_text": _passage},
    {**q(_g, _slot, "Balls and Hoops Puzzle", "MCQ",
         "What BEST can be said about the total number of pings from all the tests "
         "undertaken?",
         ["13 or 14", "At least 9", "12 or 13", "12 or 13 or 14"]), "passage_text": _passage},
]

_g = "cat2025_slot2_set2"
_passage = (
    "The two most populous cities and the non-urban region (NUR) of each of three states, "
    "Whimshire, Fogglia, and Humbleset, are assigned Pollution Measures (PMs). These nine "
    "PMs are all distinct multiples of 10, ranging from 10 to 90. The six cities in "
    "increasing order of their PMs are: Blusterburg, Noodleton, Splutterville, Quackford, "
    "Mumpypore, Zingaloo.\n\n"
    "The Pollution Index (PI) of a state is a weighted average of the PMs of its NUR and "
    "cities, with a weight of 50% for the NUR, and 25% each for its two cities.\n\n"
    "There is only one pair of an NUR and a city (considering all cities and all NURs) "
    "where the PM of the NUR is greater than that of the city. That NUR and the city both "
    "belong to Humbleset.\n\n"
    "The PIs of all three states are distinct integers, with Humbleset and Fogglia having "
    "the highest and the lowest PI respectively."
)
QUESTIONS += [
    {**q(_g, _slot, "Pollution Index Weighted Average DI", "TITA",
         "What is the PI of Whimshire?"), "passage_text": _passage},
    {**q(_g, _slot, "Pollution Index Weighted Average DI", "TITA",
         "What is the PI of Fogglia?"), "passage_text": _passage},
    {**q(_g, _slot, "Pollution Index Weighted Average DI", "TITA",
         "What is the PI of Humbleset?"), "passage_text": _passage},
    {**q(_g, _slot, "Pollution Index Weighted Average DI", "MCQ",
         "Which pair of cities definitely belong to the same state?",
         ["Noodleton, Quackford", "Splutterville, Quackford", "Mumpypore, Zingaloo",
          "Blusterburg, Mumpypore"]), "passage_text": _passage},
    {**q(_g, _slot, "Pollution Index Weighted Average DI", "TITA",
         "For how many of the cities and NURs is it possible to identify their PM and the "
         "state they belong to?"), "passage_text": _passage},
]

# Slot 2 Q10-13 (research papers chart) and Q14-17 (sustainability index scatter
# plot) SKIPPED - source PDF has literal "imageXX-XX.png" placeholders instead
# of the actual chart images; no data available to seed from.

_g = "cat2025_slot2_set5"
_passage = (
    "Ananya Raga, Bhaskar Tala, Charu Veena, and Devendra Sur are four musicians. Each of "
    "them started and completed their training as students under each of three Gurus - "
    "Pandit Meghnath, Ustad Samiran, and Acharya Raghunath between 2013 and 2024, including "
    "both the years. Each Guru trains any student for consecutive years only, for a span of "
    "2, 3, or 4 years, with each Guru having a different span. During some of these years, "
    "a student may not have trained under these Gurus; however, they never trained under "
    "multiple Gurus in the same year.\n\n"
    "In none of these years, any of these Gurus trained more than two of these students at "
    "the same time. When two students train under the same Guru at the same time, they are "
    "referred to as Gurubhai, irrespective of their gender.\n\n"
    "The following additional facts are known:\n"
    "1. Ustad Samiran never trained more than one of these students in the same year.\n"
    "2. Acharya Raghunath did not train any of these students during 2015-2018, as well as "
    "during 2021-24.\n"
    "3. Ananya and Devendra were never Gurubhai; neither were Bhaskar and Charu. All other "
    "pairs of musicians were Gurubhai for exactly 2 years.\n"
    "4. In 2013, Ananya and Bhaskar started their trainings under Pandit Meghnath and under "
    "Ustad Samiran, respectively."
)
QUESTIONS += [
    {**q(_g, _slot, "Musicians and Gurus Scheduling Puzzle", "MCQ",
         "In which of the following years were Ananya and Bhaskar Gurubhai?",
         ["2020", "2021", "2018", "2014"]), "passage_text": _passage},
    {**q(_g, _slot, "Musicians and Gurus Scheduling Puzzle", "MCQ",
         "In which year did Charu begin her training under Pandit Meghnath?",
         ["2015", "2016", "2017", "2021"]), "passage_text": _passage},
    {**q(_g, _slot, "Musicians and Gurus Scheduling Puzzle", "MCQ",
         "In which of the following years were Bhaskar and Devendra Gurubhai?",
         ["2022", "2020", "2018", "2015"]), "passage_text": _passage},
    {**q(_g, _slot, "Musicians and Gurus Scheduling Puzzle", "MCQ",
         "Which of the following statements is TRUE?",
         ["Charu was training under Ustad Samiran in 2019.",
          "Ananya was training under Ustad Samiran in 2018.",
          "Charu was training under Ustad Samiran in 2018.",
          "Ananya was training under Ustad Samiran in 2015."]), "passage_text": _passage},
    {**q(_g, _slot, "Musicians and Gurus Scheduling Puzzle", "TITA",
         "In how many of the years between 2013-24, were only two of these four musicians "
         "training under these three Gurus?"), "passage_text": _passage},
]

# ============================================================ SLOT 3 ====
_slot = "slot3"

_g = "cat2025_slot3_set1"
# NOTE: this table was transcribed from a small rendered image in the source PDF -
# double-check the figures against the original before treating them as exam-accurate.
_passage = (
    "Anu, Bijay, Chetan, Deepak, Eshan, and Faruq are six friends. Each of them uses a "
    "mobile number from exactly one of the two mobile operators - Xitel and Yocel. During "
    "the last month, the six friends made several calls to each other. The table below "
    "summarizes the number of minutes of calls that each of the six made to (outgoing "
    "minutes) and received from (incoming minutes) these friends, grouped by the operators. "
    "Some of the entries are missing.\n\n"
    "| Friend | Operator | Outgoing to Xitel | Outgoing to Yocel | Incoming from Xitel | "
    "Incoming from Yocel |\n"
    "|---|---|---|---|---|---|\n"
    "| Anu | Xitel | 100 | ? | 50 | 225 |\n"
    "| Bijay | Xitel | ? | 200 | ? | 125 |\n"
    "| Chetan | Yocel | 50 | 175 | 250 | 150 |\n"
    "| Deepak | Yocel | 100 | 150 | 275 | 100 |\n"
    "| Eshan | Yocel | ? | 100 | 100 | 375 |\n"
    "| Faruq | Yocel | 0 | ? | 100 | 150 |\n\n"
    "It is known that the duration of calls from Faruq to Eshan was 200 minutes.\n"
    "Also, there were no calls from:\n"
    "i. Bijay to Eshan,\n"
    "ii. Chetan to Anu and Chetan to Deepak,\n"
    "iii. Deepak to Bijay and Deepak to Faruq,\n"
    "iv. Eshan to Chetan and Eshan to Deepak."
)
QUESTIONS += [
    {**q(_g, _slot, "Mobile Call Minutes Data Table DI", "TITA",
         "What was the duration of calls (in minutes) from Bijay to Anu?"), "passage_text": _passage},
    {**q(_g, _slot, "Mobile Call Minutes Data Table DI", "TITA",
         "What was the total duration of calls (in minutes) made by Anu to friends having "
         "mobile numbers from Operator Yocel?"), "passage_text": _passage},
    {**q(_g, _slot, "Mobile Call Minutes Data Table DI", "TITA",
         "What was the total duration of calls (in minutes) made by Faruq to friends having "
         "mobile numbers from Operator Yocel?"), "passage_text": _passage},
    {**q(_g, _slot, "Mobile Call Minutes Data Table DI", "MCQ",
         "What was the duration of calls (in minutes) from Deepak to Chetan?",
         ["0", "125", "100", "50"]), "passage_text": _passage},
]

_g = "cat2025_slot3_set2"
_passage = (
    "Aurevia, Brelosia, Cyrenia and Zerathania are four countries with their currencies "
    "being Aurels, Brins, Crowns, and Zentars, respectively. The currencies have different "
    "exchange values. Crown's currency exchange rate with Zentars = 0.5, i.e., 1 Crown is "
    "worth 0.5 Zentars.\n\n"
    "Three travelers, Jano, Kira, and Lian set out from Zerathania visiting exactly two of "
    "the countries. Each country is visited by exactly two travelers. Each traveler has a "
    "unique Flight Cost, which represents the total cost of airfare in traveling to both "
    "the countries and back to Zerathania. The Flight Cost of Jano was 4000 Zentars, while "
    "that of the other two travelers were 5000 and 6000 Zentars, not necessarily in that "
    "order.\n\n"
    "When visiting a country, a traveler spent either 1000, 2000 or 3000 in the country's "
    "local currency. Each traveler had different spends (in the country's local currency) "
    "in the two countries he/she visited. Across all the visits, there were exactly two "
    "spends of 1000 and exactly one spend of 3000 (in the country's local currency).\n\n"
    "The total \"Travel Cost\" for a traveler is the sum of his/her Flight Cost and the "
    "money spent in the countries visited.\n\n"
    "The citizens of the four countries with knowledge of these travels made a few "
    "observations, with spends measured in their respective local currencies:\n"
    "i. Aurevia citizen: Jano and Kira visited our country, and their Travel Costs were "
    "3500 and 8000, respectively.\n"
    "ii. Brelosia citizen: Kira and Lian visited our country, spending 2000 and 3000, "
    "respectively. Kira's Travel Cost was 4000.\n"
    "iii. Cyrenia citizen: Lian visited our country and her Travel Cost was 36000."
)
QUESTIONS += [
    {**q(_g, _slot, "Currency Exchange Travel Cost Puzzle", "TITA",
         "What is the sum of Travel Costs for all travelers in Zentars?"), "passage_text": _passage},
    {**q(_g, _slot, "Currency Exchange Travel Cost Puzzle", "TITA",
         "How many Zentars did Lian spend in the two countries he visited?"), "passage_text": _passage},
    {**q(_g, _slot, "Currency Exchange Travel Cost Puzzle", "TITA",
         "What was Jano's total spend in the two countries he visited, in Aurels?"), "passage_text": _passage},
    {**q(_g, _slot, "Currency Exchange Travel Cost Puzzle", "MCQ",
         "One Brin is equivalent to how many Crowns?",
         ["4", "0.5", "8", "0.125"]), "passage_text": _passage},
    {**q(_g, _slot, "Currency Exchange Travel Cost Puzzle", "MCQ",
         "Which of the following statements is NOT true about money spent in the local "
         "currency?",
         ["Kira spent 1000 in Aurevia", "Jano spent 2000 in Aurevia",
          "Jano spent 2000 in Cyrenia", "Lian spent 2000 in Cyrenia"]), "passage_text": _passage},
]

# Slot 3 Q10-13 (puzzle competition step-line charts) SKIPPED - exact per-minute
# values aren't reliably readable from the source image, so no confident data
# to seed from.

_g = "cat2025_slot3_set4"
# NOTE: table transcribed from a small rendered image - double-check against
# the original PDF before treating the '?' placements as exam-accurate.
_passage = (
    "Seven children, Aarav, Bina, Chirag, Diya, Eshan, Farhan, and Gaurav, are sitting in a "
    "circle facing inside (not necessarily in the same order) and playing a game of "
    "'Passing the Buck'.\n\n"
    "The game is played over 10 rounds. In each round, the child holding the Buck must pass "
    "it directly to a child sitting in one of the following positions:\n"
    "- Immediately to the left;\n"
    "- Immediately to the right;\n"
    "- Second to the left; or\n"
    "- Second to the right.\n\n"
    "The game starts with Bina passing the Buck and ends with Chirag receiving the Buck. "
    "The table below provides some information about the pass types and the child "
    "receiving the Buck. Some information is missing and labelled as '?'.\n\n"
    "| Round | Position | Name |\n"
    "|---|---|---|\n"
    "| 1 | Immediately to the left | Aarav |\n"
    "| 2 | Second to the right | ? |\n"
    "| 3 | Immediately to the right | Diya |\n"
    "| 4 | ? | ? |\n"
    "| 5 | ? | Aarav |\n"
    "| 6 | Second to the left | ? |\n"
    "| 7 | Immediately to the left | Gaurav |\n"
    "| 8 | Immediately to the left | ? |\n"
    "| 9 | ? | Farhan |\n"
    "| 10 | ? | Chirag |"
)
QUESTIONS += [
    {**q(_g, _slot, "Passing the Buck Circular Puzzle", "MCQ",
         "Who is sitting immediately to the right of Bina?",
         ["Chirag", "Aarav", "Farhan", "Eshan"]), "passage_text": _passage},
    {**q(_g, _slot, "Passing the Buck Circular Puzzle", "MCQ",
         "Who is sitting third to the left of Eshan?",
         ["Aarav", "Chirag", "Gaurav", "Diya"]), "passage_text": _passage},
    {**q(_g, _slot, "Passing the Buck Circular Puzzle", "MCQ",
         "For which of the following pass types can the total number of occurrences be "
         "uniquely determined?",
         ["Second to the right", "Second to the left", "Immediately to the left",
          "Immediately to the right"]), "passage_text": _passage},
    {**q(_g, _slot, "Passing the Buck Circular Puzzle", "MCQ",
         "For which of the following children is it possible to determine how many times "
         "they received the Buck?",
         ["Bina", "Gaurav", "Farhan", "Eshan"]), "passage_text": _passage},
]

_g = "cat2025_slot3_set5"
_passage = (
    "Three countries — Pumpland (P), Xiland (X) and Cheeseland (C) — trade among themselves "
    "and with the (other countries in) Rest of World (ROW). All trade volumes are given in "
    "IC (international currency). The following terminology is used:\n"
    "- Trade balance = Exports - Imports\n"
    "- Total trade = Exports + Imports\n"
    "- Normalized trade balance = Trade balance / Total trade, expressed in percentage "
    "terms\n\n"
    "The following information is known:\n"
    "1. The normalized trade balances of P, X and C are 0%, 10%, and -20%, respectively.\n"
    "2. 40% of exports of X are to P; 22% of imports of P are from X.\n"
    "3. 90% of exports of C are to P; 4% are to ROW.\n"
    "4. 12% of exports of ROW are to X, 40% are to P.\n"
    "5. The export volumes of P, in IC, to X and C are 600 and 1200, respectively. P is the "
    "only country that exports to C."
)
QUESTIONS += [
    {**q(_g, _slot, "International Trade Balance DI", "TITA",
         "How much is exported from C to X, in IC?"), "passage_text": _passage},
    {**q(_g, _slot, "International Trade Balance DI", "TITA",
         "How much is exported from P to ROW, in IC?"), "passage_text": _passage},
    {**q(_g, _slot, "International Trade Balance DI", "TITA",
         "How much is exported from ROW to ROW, in IC?"), "passage_text": _passage},
    {**q(_g, _slot, "International Trade Balance DI", "MCQ",
         "What is the trade balance of ROW?",
         ["200", "100", "0", "-200"]), "passage_text": _passage},
    {**q(_g, _slot, "International Trade Balance DI", "MCQ",
         "Which among the countries P, X, and C has/have the least total trade?",
         ["Both X and C", "Only X", "Only C", "Only P"]), "passage_text": _passage},
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
            print(f"CAT 2025 DILR PYQs already seeded ({existing} rows); skipping.")
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
        print(f"Seeded {len(QUESTIONS)} CAT 2025 DILR PYQ questions across {num_groups} sets.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

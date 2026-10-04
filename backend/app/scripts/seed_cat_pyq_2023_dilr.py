"""Seed real CAT 2023 DILR questions, retyped from the official question
papers (via the combined SOLUTIONS PDFs) in pyq-source/2023/.

`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

Slot 1 (20 questions, 4 sets) is fully loaded - no chart dependency at all;
the one set with an illustrative diagram (Set 1, housing complex layout)
has its layout fully specified in text (6 columns, 2 rows, 2 blocks),
so the diagram is purely illustrative, not load-bearing.

Slots 2 and 3 are written incrementally below (same file, checkpointed
after each slot while under extraction).

Run with:
    python -m app.scripts.seed_cat_pyq_2023_dilr
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023


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

_g = "cat2023_slot1_dilr_set1"
_passage = (
    "The schematic diagram below shows 12 rectangular houses in a housing complex. "
    "House numbers are mentioned in the rectangles representing the houses. The houses "
    "are located in six columns - Column-A through Column-F, and two rows - Row-1 and "
    "Row-2. The houses are divided into two blocks - Block XX (Columns A, B, C) and "
    "Block YY (Columns D, E, F). Each column has one house in Row-1 (named <column>1, "
    "e.g. A1) and one house in Row-2 (named <column>2, e.g. A2). A road passes in front "
    "of the houses in Row-2, and another road runs between the two blocks (between "
    "Column-C and Column-D).\n\n"
    "Some of the houses are occupied. The remaining ones are vacant and are the only "
    "ones available for sale.\n"
    "The road adjacency value of a house is the number of its sides adjacent to a road. "
    "For example, the road adjacency values of C2, F2, and B1 are 2, 1, and 0, "
    "respectively. The neighbour count of a house is the number of sides of that house "
    "adjacent to occupied houses in the same block. For example, E1 and C1 can have the "
    "maximum possible neighbour counts of 3 and 2, respectively.\n"
    "The base price of a vacant house is Rs. 10 lakhs if the house does not have a "
    "parking space, and Rs. 12 lakhs if it does. The quoted price (in lakhs of Rs.) of a "
    "vacant house is calculated as (base price) + 5 x (road adjacency value) + 3 x "
    "(neighbour count).\n"
    "The following information is also known.\n"
    "1. The maximum quoted price of a house in Block XX is Rs. 24 lakhs. The minimum "
    "quoted price of a house in block YY is Rs. 15 lakhs, and one such house is in "
    "Column-E.\n"
    "2. Row-1 has two occupied houses, one in each block.\n"
    "3. Both houses in Column-E are vacant. Each of Column-D and Column-F has at least "
    "one occupied house.\n"
    "4. There is only one house with parking space in Block YY."
)
QUESTIONS += [
    {**q(_g, _slot, "Housing Complex Pricing Puzzle", "TITA",
         "How many houses are vacant in Block XX?"), "passage_text": _passage},
    {**q(_g, _slot, "Housing Complex Pricing Puzzle", "MCQ",
         "Which of the following houses is definitely occupied?",
         ["D2", "A1", "B1", "F2"]), "passage_text": _passage},
    {**q(_g, _slot, "Housing Complex Pricing Puzzle", "MCQ",
         "Which of the following options best describes the number of vacant houses in "
         "Row-2?",
         ["Either 2 or 3", "Exactly 3", "Exactly 2", "Either 3 or 4"]), "passage_text": _passage},
    {**q(_g, _slot, "Housing Complex Pricing Puzzle", "TITA",
         "What is the maximum possible quoted price (in lakhs of Rs.) for a vacant house "
         "in Column-E?"), "passage_text": _passage},
    {**q(_g, _slot, "Housing Complex Pricing Puzzle", "MCQ",
         "Which house in Block YY has parking space?",
         ["E2", "F2", "E1", "F1"]), "passage_text": _passage},
]

_g = "cat2023_slot1_dilr_set2"
_passage = (
    "Faculty members in a management school can belong to one of four departments - "
    "Finance and Accounting (F&A), Marketing and Strategy (M&S), Operations and Quants "
    "(O&Q) and Behaviour and Human Resources (B&H). The numbers of faculty members in "
    "F&A, M&S, O&Q and B&H are 9, 7, 5 and 3 respectively. Prof. Pakrasi, Prof. Qureshi, "
    "Prof. Ramaswamy and Prof. Samuel are four members of the school's faculty who were "
    "candidates for the post of the Dean of the school. Only one of the candidates was "
    "from O&Q. Every faculty member, including the four candidates, voted for the post. "
    "In each department, all the faculty members who were not candidates voted for the "
    "same candidate. The rules for the election are listed below.\n"
    "1. There cannot be more than two candidates from a single department.\n"
    "2. A candidate cannot vote for himself/herself.\n"
    "3. Faculty members cannot vote for a candidate from their own department.\n"
    "After the election, it was observed that Prof. Pakrasi received 3 votes, Prof. "
    "Qureshi received 14 votes, Prof. Ramaswamy received 6 votes and Prof. Samuel "
    "received 1 vote. Prof. Pakrasi voted for Prof. Ramaswamy, Prof. Qureshi for Prof. "
    "Samuel, Prof. Ramaswamy for Prof. Qureshi and Prof. Samuel for Prof. Pakrasi."
)
QUESTIONS += [
    {**q(_g, _slot, "Faculty Election Voting Puzzle", "MCQ",
         "Which two candidates can belong to the same department?",
         ["Prof. Pakrasi and Prof. Qureshi", "Prof. Qureshi and Prof. Ramaswamy",
          "Prof. Pakrasi and Prof. Samuel", "Prof. Ramaswamy and Prof. Samuel"]),
     "passage_text": _passage},
    {**q(_g, _slot, "Faculty Election Voting Puzzle", "MCQ",
         "Which of the following can be the number of votes that Prof. Qureshi received "
         "from a single department?",
         ["7", "8", "6", "9"]), "passage_text": _passage},
    {**q(_g, _slot, "Faculty Election Voting Puzzle", "MCQ",
         "If Prof. Samuel belongs to B&H, which of the following statements is/are "
         "true?\nStatement A: Prof. Pakrasi belongs to M&S.\nStatement B: Prof. "
         "Ramaswamy belongs to O&Q.",
         ["Only statement A", "Both statements A and B", "Neither statement A nor statement B",
          "Only statement B"]), "passage_text": _passage},
    {**q(_g, _slot, "Faculty Election Voting Puzzle", "MCQ",
         "What best can be concluded about the candidate from O&Q?",
         ["It was either Prof. Ramaswamy or Prof. Samuel.", "It was Prof. Samuel.",
          "It was either Prof. Pakrasi or Prof. Qureshi.", "It was Prof. Ramaswamy."]),
     "passage_text": _passage},
    {**q(_g, _slot, "Faculty Election Voting Puzzle", "MCQ",
         "Which of the following statements is/are true?\nStatement A: Non-candidates "
         "from M&S voted for Prof. Qureshi.\nStatement B: Non-candidates from F&A voted "
         "for Prof. Qureshi.",
         ["Neither statement A nor statement B", "Both statements A and B",
          "Only statement A", "Only statement B"]), "passage_text": _passage},
]

_g = "cat2023_slot1_dilr_set3"
_passage = (
    "Five restaurants, coded R1, R2, R3, R4 and R5 gave integer ratings to five gig "
    "workers - Ullas, Vasu, Waman, Xavier and Yusuf, on a scale of 1 to 5. The means of "
    "the ratings given by R1, R2, R3, R4 and R5 were 3.4, 2.2, 3.8, 2.8 and 3.4 "
    "respectively.\n"
    "The summary statistics of these ratings for the five workers is given below.\n\n"
    "| | Ullas | Vasu | Waman | Xavier | Yusuf |\n"
    "|---|---|---|---|---|---|\n"
    "| Mean rating | 2.2 | 3.8 | 3.4 | 3.6 | 2.6 |\n"
    "| Median rating | 2 | 4 | 4 | 4 | 3 |\n"
    "| Mode rating | 2 | 4 | 5 | 5 | 1 and 4 |\n"
    "| Range of rating | 3 | 3 | 4 | 4 | 3 |\n\n"
    "* Range of ratings is defined as the difference between the maximum and minimum "
    "ratings awarded to a worker.\n"
    "The following is partial information about ratings of 1 and 5 awarded by the "
    "restaurants to the workers.\n"
    "(a) R1 awarded a rating of 5 to Waman, as did R2 to Xavier, R3 to Waman and "
    "Xavier, and R5 to Vasu.\n"
    "(b) R1 awarded a rating of 1 to Ullas, as did R2 to Waman and Yusuf, and R3 to "
    "Yusuf."
)
QUESTIONS += [
    {**q(_g, _slot, "Restaurant Worker Ratings DI", "TITA",
         "How many individual ratings cannot be determined from the above information?"),
     "passage_text": _passage},
    {**q(_g, _slot, "Restaurant Worker Ratings DI", "TITA",
         "To how many workers did R2 give a rating of 4?"), "passage_text": _passage},
    {**q(_g, _slot, "Restaurant Worker Ratings DI", "TITA",
         "What rating did R1 give to Xavier?"), "passage_text": _passage},
    {**q(_g, _slot, "Restaurant Worker Ratings DI", "TITA",
         "What is the median of the ratings given by R3 to the five workers?"),
     "passage_text": _passage},
    {**q(_g, _slot, "Restaurant Worker Ratings DI", "MCQ",
         "Which among the following restaurants gave its median rating to exactly one "
         "of the workers?",
         ["R3", "R5", "R4", "R2"]), "passage_text": _passage},
]

_g = "cat2023_slot1_dilr_set4"
_passage = (
    "A visa processing office (VPO) accepts visa applications in four categories - US, "
    "UK, Schengen, and Others. The applications are scheduled for processing in twenty "
    "15-minute slots starting at 9:00 am and ending at 2:00 pm. Ten applications are "
    "scheduled in each slot.\n"
    "There are ten counters in the office, four dedicated to US applications, and two "
    "each for UK applications, Schengen applications and Others applications. Applicants "
    "are called in for processing sequentially on a first-come-first-served basis "
    "whenever a counter gets freed for their category. The processing time for an "
    "application is the same within each category. But it may vary across categories. "
    "Each US and UK application requires 10 minutes of processing time. Depending on the "
    "number of applications in a category and time required to process an application "
    "for that category, it is possible that an applicant for a slot may be processed "
    "later.\n"
    "On a particular day, Ira, Vijay and Nandini were scheduled for Schengen visa "
    "processing in that order. They had a 9:15 am slot but entered the VPO at 9:20 am. "
    "When they entered the office, exactly six out of the ten counters were either "
    "processing applications, or had finished processing one and ready to start "
    "processing the next.\n"
    "Mahira and Osman were scheduled in the 9:30 am slot on that day for visa processing "
    "in the Others category.\n"
    "The following additional information is known about that day.\n"
    "1. All slots were full.\n"
    "2. The number of US applications was the same in all the slots. The same was true "
    "for the other three categories.\n"
    "3. 50% of the applications were US applications.\n"
    "4. All applicants except Ira, Vijay and Nandini arrived on time.\n"
    "5. Vijay was called to a counter at 9:25 am."
)
QUESTIONS += [
    {**q(_g, _slot, "Visa Application Processing DI", "TITA",
         "How many UK applications were scheduled on that day?"), "passage_text": _passage},
    {**q(_g, _slot, "Visa Application Processing DI", "TITA",
         "What is the maximum possible value of the total time (in minutes, nearest to "
         "its integer value) required to process all applications in the Others "
         "category on that day?"), "passage_text": _passage},
    {**q(_g, _slot, "Visa Application Processing DI", "MCQ",
         "Which of the following is the closest to the time when Nandini's application "
         "process got over?",
         ["9:45am", "9:50am", "9:35am", "9:37am"]), "passage_text": _passage},
    {**q(_g, _slot, "Visa Application Processing DI", "MCQ",
         "Which of the following statements is false?",
         ["The application process of Osman was completed before 9:45 am",
          "The application process of Mahira started after Nandini's.",
          "The application process of Mahira was completed before Nandini's.",
          "The application process of Osman was completed before Vijay's."]),
     "passage_text": _passage},
    {**q(_g, _slot, "Visa Application Processing DI", "MCQ",
         "When did the application processing for all US applicants get over on that "
         "day?",
         ["3:40 pm", "2:00 pm", "2:25 pm", "2:05 pm"]), "passage_text": _passage},
]


# ============================================================ SLOT 2 ====
_slot = "slot2"

_g = "cat2023_slot2_dilr_set1"
_passage = (
    "Odsville has five firms - Alfloo, Bzygoo, Czechy, Drjbna, and Elavalaki. Each of "
    "these firms was founded in some year and also closed down a few years later.\n"
    "Each firm raised Rs. 1 crore in its first and last year of existence. The amount "
    "each firm raised every year increased until it reached a maximum, and then "
    "decreased until the firm closed down. No firm raised the same amount of money in "
    "two consecutive years. Each annual increase and decrease was either by Rs. 1 crore "
    "or by Rs. 2 crores.\n"
    "The table below provides partial information about the five firms.\n\n"
    "| Firm | First year of existence | Last year of existence | Total amount raised "
    "(Rs. crores) |\n"
    "|---|---|---|---|\n"
    "| Alfloo | 2009 | 2016 | 21 |\n"
    "| Bzygoo | 2012 | 2015 | ? |\n"
    "| Czechy | 2013 | ? | 9 |\n"
    "| Drjbna | 2011 | 2015 | 10 |\n"
    "| Elavalaki | 2010 | ? | 13 |"
)
QUESTIONS += [
    {**q(_g, _slot, "Firm Fundraising Trajectory DI", "MCQ",
         "For which firm(s) can the amounts raised by them be concluded with certainty "
         "in each year?",
         ["Only Czechy", "Only Bzygoo and Czechy and Drjbna", "Only Drjbna",
          "Only Czechy and Drjbna"]), "passage_text": _passage},
    {**q(_g, _slot, "Firm Fundraising Trajectory DI", "MCQ",
         "What best can be concluded about the total amount of money raised in 2015?",
         ["It is either Rs. 7 crores or Rs. 8 crores or Rs. 9 crores.",
          "It is either Rs. 7 crores or Rs. 8 crores.", "It is exactly Rs. 8 crores.",
          "It is either Rs. 8 crores or Rs. 9 crores."]), "passage_text": _passage},
    {**q(_g, _slot, "Firm Fundraising Trajectory DI", "TITA",
         "What is the largest possible total amount of money (in Rs. crores) that could "
         "have been raised in 2013?"), "passage_text": _passage},
    {**q(_g, _slot, "Firm Fundraising Trajectory DI", "MCQ",
         "If Elavalaki raised Rs. 3 crores in 2013, then what is the smallest possible "
         "total amount of money (in Rs. crores) that could have been raised by all the "
         "companies in 2012?",
         ["10", "9", "12", "11"]), "passage_text": _passage},
    {**q(_g, _slot, "Firm Fundraising Trajectory DI", "MCQ",
         "If the total amount of money raised in 2014 is Rs. 12 crores, then which of "
         "the following is not possible?",
         ["Alfloo raised the same amount of money as Drjbna in 2013.",
          "Bzygoo raised more money than Elavalaki in 2014.",
          "Bzygoo raised the same amount of money as Elavalaki in 2013.",
          "Alfloo raised the same amount of money as Bzygoo in 2014."]),
     "passage_text": _passage},
]

_g = "cat2023_slot2_dilr_set2"
_passage = (
    "Anjali, Bipasha, and Chitra visited an entertainment park that has four rides. "
    "Each ride lasts one hour and can accommodate one visitor at one point. All rides "
    "begin at 9 am and must be completed by 5 pm except for Ride-3, for which the last "
    "ride has to be completed by 1 pm. Ride gates open every 30 minutes, e.g. 10 am, "
    "10:30 am, and so on. Whenever a ride gate opens, and there is no visitor inside, "
    "the first visitor waiting in the queue buys the ticket just before taking the "
    "ride. The ticket prices are Rs. 20, Rs. 50, Rs. 30, and Rs. 40 for Rides 1 to 4, "
    "respectively. Each of the three visitors took at least one ride and did not "
    "necessarily take all rides. None of them took the same ride more than once. The "
    "movement time from one ride to another is negligible, and a visitor leaves the "
    "ride immediately after the completion of the ride. No one takes a break inside the "
    "park unless mentioned explicitly.\n"
    "The following information is also known.\n"
    "1. Chitra never waited in the queue and completed her visit by 11 am after "
    "spending Rs. 50 to pay for the ticket(s).\n"
    "2. Anjali took Ride-1 at 11 am after waiting for 30 mins for Chitra to complete "
    "it. It was the only ride where Anjali waited.\n"
    "3. Bipasha began her first of three rides at 11:30 am. All three visitors "
    "incurred the same amount of ticket expense by 12:15 pm.\n"
    "4. The last ride taken by Anjali and Bipasha was the same, where Bipasha waited 30 "
    "mins for Anjali to complete her ride. Before standing in the queue for that ride, "
    "Bipasha took a 1-hour coffee break after completing her previous ride."
)
QUESTIONS += [
    {**q(_g, _slot, "Entertainment Park Rides Scheduling DI", "MCQ",
         "What was the total amount spent on tickets (in Rs.) by Bipasha?",
         ["110", "100", "90", "120"]), "passage_text": _passage},
    {**q(_g, _slot, "Entertainment Park Rides Scheduling DI", "MCQ",
         "Which were all the rides that Anjali completed by 2:00 pm?",
         ["Ride-1 and Ride-3", "Ride-1, Ride-2, and Ride-4", "Ride-1 and Ride-4",
          "Ride-1, Ride-2, and Ride-3"]), "passage_text": _passage},
    {**q(_g, _slot, "Entertainment Park Rides Scheduling DI", "MCQ",
         "Which ride was taken by all three visitors?",
         ["Ride-1", "Ride-3", "Ride-2", "Ride-4"]), "passage_text": _passage},
    {**q(_g, _slot, "Entertainment Park Rides Scheduling DI", "TITA",
         "How many rides did Anjali and Chitra take in total?"), "passage_text": _passage},
    {**q(_g, _slot, "Entertainment Park Rides Scheduling DI", "TITA",
         "What was the total amount spent on tickets (in Rs.) by Anjali?"),
     "passage_text": _passage},
]

_g = "cat2023_slot2_dilr_set3"
_passage = (
    "Three participants - Akhil, Bimal, and Chatur participate in a random draw "
    "competition for five days. Every day, each participant randomly picks up a ball "
    "numbered between 1 and 9. The number on the ball determines his score on that "
    "day. The total score of a participant is the sum of his scores attained in the "
    "five days. The total score of a day is the sum of participants' scores on that "
    "day. The 2-day average on a day, except on Day 1, is the average of the total "
    "scores of that day and of the previous day. For example, if the total scores of "
    "Day 1 and Day 2 are 25 and 20, then the 2-day average on Day 2 is calculated as "
    "22.5. Table 1 gives the 2-day averages for Days 2 through 5.\n\n"
    "| | Day 2 | Day 3 | Day 4 | Day 5 |\n|---|---|---|---|---|\n"
    "| 2-day average | 15 | 15.5 | 16 | 17 |\n\n"
    "Participants are ranked each day, with the person having the maximum score being "
    "awarded the minimum rank (1) on that day. If there is a tie, all participants "
    "with the tied score are awarded the best available rank. For example, if on a day "
    "Akhil, Bimal, and Chatur score 8, 7 and 7 respectively, then their ranks will be "
    "1, 2 and 2 respectively on that day. These ranks are given in Table 2.\n\n"
    "| | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 |\n|---|---|---|---|---|---|\n"
    "| Akhil | 1 | 2 | 2 | 3 | 3 |\n"
    "| Bimal | 2 | 3 | 2 | 1 | 1 |\n"
    "| Chatur | 3 | 1 | 1 | 2 | 2 |\n\n"
    "The following information is also known:\n"
    "1. Chatur always scores in multiples of 3. His score on Day 2 is the unique "
    "highest score in the competition. His minimum score is observed only on Day 1, "
    "and it matches Akhil's score on Day 4.\n"
    "2. The total score on Day 3 is the same as the total score on Day 4.\n"
    "3. Bimal's scores are the same on Day 1 and Day 3."
)
QUESTIONS += [
    {**q(_g, _slot, "Random Draw Scoring Competition DI", "MCQ",
         "What is Akhil's score on Day 1?",
         ["7", "6", "5", "8"]), "passage_text": _passage},
    {**q(_g, _slot, "Random Draw Scoring Competition DI", "MCQ",
         "Who attains the maximum total score?",
         ["Bimal", "Chatur", "Cannot be determined", "Akhil"]), "passage_text": _passage},
    {**q(_g, _slot, "Random Draw Scoring Competition DI", "TITA",
         "What is the minimum possible total score of Bimal?"), "passage_text": _passage},
    {**q(_g, _slot, "Random Draw Scoring Competition DI", "MCQ",
         "If the total score of Bimal is a multiple of 3, what is the score of Akhil "
         "on Day 2?",
         ["Cannot be determined", "5", "6", "4"]), "passage_text": _passage},
    {**q(_g, _slot, "Random Draw Scoring Competition DI", "TITA",
         "If Akhil attains a total score of 24, then what is the total score of "
         "Bimal?"), "passage_text": _passage},
]

_g = "cat2023_slot2_dilr_set4"
_passage = (
    "There are nine boxes arranged in a 3x3 array as shown in Tables 1 and 2. Each box "
    "contains three sacks. Each sack has a certain number of coins, between 1 and 9, "
    "both inclusive.\n"
    "The average number of coins per sack in the boxes are all distinct integers. The "
    "total number of coins in each row is the same. The total number of coins in each "
    "column is also the same.\n"
    "Table 1 gives information regarding the median of the numbers of coins in the "
    "three sacks in a box for some of the boxes. In Table 2, each box has a number "
    "which represents the number of sacks in that box having more than 5 coins. That "
    "number is followed by a * if the sacks in that box satisfy exactly one among the "
    "following three conditions, and it is followed by ** if two or more of these "
    "conditions are satisfied.\n"
    "The conditions are as follows:\n"
    "i) The minimum among the numbers of coins in the three sacks in the box is 1.\n"
    "ii) The median of the numbers of coins in the three sacks is 1.\n"
    "iii) The maximum among the numbers of coins in the three sacks in the box is 9.\n\n"
    "Table 1 (median of the three sacks in each box; '?' = not given):\n"
    "| | Column 1 | Column 2 | Column 3 |\n|---|---|---|---|\n"
    "| Row 1 | ? | 9 | 6 |\n"
    "| Row 2 | 2 | ? | ? |\n"
    "| Row 3 | 8 | ? | ? |\n\n"
    "Table 2 (count of sacks with more than 5 coins, with condition flags):\n"
    "| | Column 1 | Column 2 | Column 3 |\n|---|---|---|---|\n"
    "| Row 1 | 1** | 2* | 2* |\n"
    "| Row 2 | 1** | 0* | 3* |\n"
    "| Row 3 | 3* | 2** | 0** |"
)
QUESTIONS += [
    {**q(_g, _slot, "Coin Boxes Grid Puzzle DI", "MCQ",
         "What is the total number of coins in all the boxes in the 3rd row?",
         ["36", "30", "15", "45"]), "passage_text": _passage},
    {**q(_g, _slot, "Coin Boxes Grid Puzzle DI", "MCQ",
         "How many boxes have at least one sack containing 9 coins?",
         ["3", "8", "5", "4"]), "passage_text": _passage},
    {**q(_g, _slot, "Coin Boxes Grid Puzzle DI", "TITA",
         "For how many boxes are the average and median of the numbers of coins "
         "contained in the three sacks in that box the same?"), "passage_text": _passage},
    {**q(_g, _slot, "Coin Boxes Grid Puzzle DI", "TITA",
         "How many sacks have exactly one coin?"), "passage_text": _passage},
    {**q(_g, _slot, "Coin Boxes Grid Puzzle DI", "TITA",
         "In how many boxes do all three sacks contain different numbers of coins?"),
     "passage_text": _passage},
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_group_ids = {
            row[0]
            for row in db.query(CatQuestion.group_id)
            .filter(CatQuestion.source_year == SOURCE_YEAR, CatQuestion.section == "DILR")
            .distinct()
            .all()
        }

        inserted = 0
        for item in QUESTIONS:
            if item["group_id"] in existing_group_ids:
                continue
            inserted += 1
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
        print(f"Seeded {inserted} new CAT 2023 DILR PYQ questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

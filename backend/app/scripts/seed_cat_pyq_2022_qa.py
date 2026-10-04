"""Seed real CAT 2022 QA questions, generated from the official
solutions PDFs via pdftotext + pyq_qa_parser.py (automated text-layer
extraction, not LLM transcription).

Roughly half of CAT QA questions embed their math as a rendered image pdftotext can't recover (shows up as a run of blank space where an 
equation used to be, or an empty option) - those are intentionally omitted here, not fabricated. See stderr from the generation step for 
which question numbers were skipped per slot.

`correct_answer`/`explanation` are intentionally left blank for now - the answer key
is loaded separately once transcribed from the solutions PDFs.

Run with:
    python -m app.scripts.seed_cat_pyq_2022_qa
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022


def q(slot, qtype, text, options=None):
    return {
        "section": "QA",
        "question_type": qtype,
        "topic": "Quantitative Aptitude",
        "difficulty": "hard",
        "source": "pyq",
        "source_year": SOURCE_YEAR,
        "source_slot": slot,
        "group_id": None,
        "passage_text": None,
        "question_text": text,
        "options": options,
    }


QUESTIONS = []

# ============================================================ SLOT 1 ====
_slot = "slot1"
QUESTIONS += [
    q(_slot, "TITA", "Pinky is standing in a queue at a ticket counter. Suppose the ratio of the number of persons standing ahead of Pinky to the number of persons standing behind her in the queue is 3:5. If the total number of persons in the queue is less than 300, then the maximum possible number of persons standing ahead of Pinky is", options=None),
    q(_slot, "MCQ", "The largest real value of a for which the equation has an infinite number of solutions for x is", options=["-1", "0", "1", "2"]),
    q(_slot, "MCQ", "The average of three integers is 13. When a natural number n is included, the average of these four integers remains an odd integer. The minimum possible value of n is", options=["3", "4", "5", "1"]),
    q(_slot, "TITA", "In a village, the ratio of number of males to females is 5:4. The ratio of number of literate males to literate females is 2:3. The ratio of the number of illiterate males to illiterate females is 4:3. If 3600 males in the village are literate, then the total number of females in the village is", options=None),
    q(_slot, "MCQ", "Let ABCD be a parallelogram such that the coordinates of its three vertices A, B, C are (1, 1), (3, 4), and (−2, 8), respectively. Then, the coordinates of the vertex D are", options=["(−4, 5)", "(4, 5)", "(−3, 4)", "(0, 11)"]),
    q(_slot, "MCQ", "Alex invested his savings in two parts. The simple interest earned on the first part at 15% per annum for 4 years is the same as the simple interest earned on the second part at 12% per annum for 3 years. Then, the percentage of his savings invested in the first part is", options=["62.50%", "37.50%", "60%", "40%"]),
    q(_slot, "MCQ", "The average weight of students in a class increases by 600 gm when some new students join the class. If the average weight of the new students is 3 kg more than the average weight of the original students, then the ratio of the number of original students to the number of new students is", options=["1:2", "3:1", "1:4", "4:1"]),
    q(_slot, "MCQ", "A mixture contains lemon juice and sugar syrup in equal proportion. If a new mixture is created by adding this mixture and sugar syrup in the ratio 1 : 3, then the ratio of lemon juice and sugar syrup in the new mixture is", options=["1:6", "1:4", "1:5", "1:7"]),
    q(_slot, "TITA", "Amal buys 110kg of syrup and 120kg of juice, syrup being 20% less costly than juice, per kg. He sells 10kg of syrup at 10% profit and 20kg of juice at 20% profit. Mixing the remaining juice and syrup, Amal sells the mixture at ₹ 308.32 per kg and makes an overall profit of 64%. Then, Amal's cost price for syrup, in rupees per kg, is", options=None),
    q(_slot, "TITA", "A trapezium ABCD has side AD parallel to BC, ∠BAD=90∘, BC=3 cm, and AD=8 cm. If the perimeter of this trapezium is 36 cm, then its area, in sq. cm, is", options=None),
    q(_slot, "MCQ", "In a class of 100 students, 73 like coffee, 80 like tea, and 52 like lemonade. It may be possible that some students do not like any of these three drinks. Then the difference between the maximum and minimum possible number of students who like all the three drinks is", options=["48", "53", "47", "52"]),
    q(_slot, "MCQ", "Trains A and B start traveling at the same time towards each other with constant speeds from stations X and Y, respectively. Train A reaches station Y in 10 minutes while train B takes 9 minutes to reach station X after meeting train A. Then the total time taken, in minutes, by train B to travel from station Y to station X is", options=["15", "12", "6", "10"]),
    q(_slot, "MCQ", "Ankita buys 4kg cashews, 14kg peanuts, and 6kg almonds when the cost of 7kg cashews is the same as that of 30kg peanuts or 9kg almonds. She mixes all three nuts and marks a price for the mixture in order to make a profit of ₹1752. She sells 4kg of the mixture at this marked price and the remaining at a 20% discount on the marked price, thus making a total profit of ₹744. Then the amount, in rupees, that she had spent buying almonds is", options=["1440", "1176", "1680", "2520"]),
    q(_slot, "TITA", "For natural numbers x,y, and z, if xy+yz=19 and yz+xz=51, then the minimum possible value of xyz is", options=None),
    q(_slot, "TITA", "The number of ways of distributing 20 identical balloons among 4 children such that each child gets some balloons but no child gets an odd number of balloons, is", options=None),
]

# ============================================================ SLOT 2 ====
_slot = "slot2"
QUESTIONS += [
    q(_slot, "TITA", "The number of distinct integer values of n satisfying , is", options=None),
    q(_slot, "MCQ", "If a and b are non-negative real numbers such that a+2b=6, then the average of the maximum and minimum possible values of (a+b) is", options=["4", "4.5", "3.5", "3"]),
    q(_slot, "MCQ", "The number of integers greater than 2000 that can be formed with the digits 0,1,2,3,4,5 using each digit at most once,is", options=["1440", "1200", "1420", "1480"]),
    q(_slot, "MCQ", "Manu earns ₹4000 per month and wants to save an average of ₹550 per month in a year. In the first nine months, his monthly expense was ₹3500, and he foresees that, tenth month onward, his monthly expense will increase to ₹3700. In order to meet his yearly savings target, his monthly earnings, in rupees, from the tenth month onward should be", options=["4200", "4400", "4300", "4350"]),
    q(_slot, "MCQ", "On day one,there are 100 particles in a laboratory experiment.On day n,where n≥2,one out of every n particles produces another particle.If the total number of particles in the laboratory experiment increases to 1000 on day m,then m equals", options=["19", "16", "17", "18"]),
    q(_slot, "MCQ", "Five students,including Amit,appear for an examination in which possible marks are integers between 0 and 50,both inclusive.The average marks for all the students is 38 and exactly three students got more than 32.If no two students got the same marks and Amit got the least marks among the five students,then the difference between the highest and lowest possible marks of Amit is", options=["21", "24", "20", "22"]),
    q(_slot, "MCQ", "Two ships meet mid-ocean,and then,one ship goes south and the other ship goes west,both travelling at constant speeds.Two hours later,they are 60 km apart.If the speed of one of the ships is 6km per hour more than the other one,then the speed,in km per hour,of the slower ship is", options=["12", "18", "20", "24"]),
    q(_slot, "TITA", "The number of integer solutions of the equation is", options=None),
    q(_slot, "TITA", "In an examination,there were 75 questions.3 marks were awarded for each correct answer,1 mark was deducted for each wrong answer and 1 mark was awarded for each unattempted question.Rayan scored a total of 97 marks in the examination.If the number of unattempted questions was\n\nhigher than the number of attempted questions,then the maximum number of correct answers that Rayan could have given in the examination is", options=None),
]

# ============================================================ SLOT 3 ====
_slot = "slot3"
QUESTIONS += [
    q(_slot, "TITA", "A donation box can receive only cheques of ₹100,₹250 and ₹500. On one good day,the donation box was found to contain exactly 100 cheques amounting to a total sum of ₹15250. Then, the maximum possible number of cheques of ₹500 that the donation box may have contained,is", options=None),
    q(_slot, "TITA", "Suppose the medians BD and CE of a triangle ABC intersect at a point O. If area of triangle ABC is 108 sq. cm, then, the area of the triangle EOD, in sq. cm, is", options=None),
    q(_slot, "TITA", "Bob can finish a job in 40 days,if he works alone. Alex is twice as fast as Bob and thrice as fast as Cole in the same job.Suppose Alex and Bob work together on the first day,Bob and Cole work together on the second day,Cole and Alex work together on the third day and then,they continue the work by repeating this three-day roster,with Alex and Bob working together on the fourth day and so on.Then,the total number of days Alex would have worked when the job gets finished,is", options=None),
    q(_slot, "MCQ", "Consider six distinct natural numbers such that the average of the two smallest numbers is 14 and the average of the two largest numbers is 28. Then,the maximum possible value of the average of these six numbers is", options=["22.5", "23.5", "24", "23"]),
    q(_slot, "MCQ", "Two ships are approaching a port along straight routes at constant speeds. Initially,the two ships and the port formed an equilateral triangle with sides of length 24 km. When the slower ship travelled 8 km,the triangle formed by the new positions of the two ships and the port became right-angled. When the faster ship reaches the port, the distance,in km,between the other ship and the port will be", options=["4", "6", "12", "8"]),
    q(_slot, "TITA", "In an examination,the average marks of students in sections A and B are 32 and 60,respectively. The number of students in section A is 10 less than that in section B. If the average marks of all the students across both\n\nthe sections combined is an integer,then the difference between the maximum and minimum possible number of students in section A is", options=None),
    q(_slot, "TITA", "Moody takes 30 seconds to finish riding an escalator if he walks on it at his normal speed in the same direction.He takes 20 seconds to finish riding the escalator if he walks at twice his normal speed in the same direction.If Moody decides to stand still on the escalator,then the time,in seconds,needed to finish riding the escalator is", options=None),
    q(_slot, "MCQ", "The arithmetic mean of all the distinct numbers that can be obtained by rearranging the digits in 1421, including itself, is", options=["2442", "2222", "3333", "2592"]),
    q(_slot, "MCQ", "The lengths of all four sides of a quadrilateral are integer valued.If three of its sides are of length 1cm,2cm and 4cm,then the total number of possible lengths of the fourth side is", options=["6", "4", "5", "3"]),
    q(_slot, "MCQ", "Two cars travel from different locations at constant speeds. To meet each other after starting at the same time, they take 1.5 hours if they travel towards each other, but 10.5 hours if they travel in the same direction. If the speed of the slower car is 60km/hr, then the distance traveled, in km,\n\nby the slower car when it meets the other car while traveling towards each other, is", options=["150", "100", "90", "120"]),
    q(_slot, "TITA", "The average of all 3-digit terms in the arithmetic progression 38,55,72,...,is", options=None),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = (
            db.query(CatQuestion)
            .filter(CatQuestion.source_year == SOURCE_YEAR, CatQuestion.section == "QA")
            .count()
        )
        if existing > 0:
            print(f"CAT {SOURCE_YEAR} QA PYQs already seeded ({existing} rows); skipping.")
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
        print(f"Seeded {len(QUESTIONS)} CAT {SOURCE_YEAR} QA PYQ questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

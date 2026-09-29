"""Seed the cat_questions table with ~30 hand-written, CAT-style PYQ-style questions
spread across VARC, DILR, and QA.

Run with:
    python -m app.scripts.seed_cat_questions
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

QUESTIONS = [
    # ---------------------------------------------------------------- VARC (10) ----
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Reading Comprehension",
        "difficulty": "easy",
        "question_text": (
            "Passage: Urban trees do far more than decorate a street. A mature tree can "
            "intercept several hundred litres of rainwater during a storm, easing the load on "
            "city drains. Its canopy lowers the surrounding air temperature by several degrees "
            "in summer, cutting the energy cities spend on cooling. Yet municipal budgets "
            "routinely treat trees as cosmetic line items, the first to be cut when funds run "
            "short, rather than as pieces of infrastructure with a measurable economic return.\n\n"
            "Question: According to the passage, city budgets tend to undervalue urban trees "
            "primarily because they are viewed as:"
        ),
        "options": [
            "Too expensive to plant at scale",
            "Merely decorative rather than functional infrastructure",
            "A cause of drainage problems during storms",
            "Less effective than mechanical cooling systems",
        ],
        "correct_answer": "Merely decorative rather than functional infrastructure",
        "explanation": (
            "The passage explicitly contrasts trees' measurable functions (stormwater "
            "interception, cooling) with municipalities treating them as 'cosmetic line "
            "items' rather than infrastructure, so option 2 restates the passage's claim "
            "directly; the other options are not supported by the text."
        ),
    },
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Reading Comprehension",
        "difficulty": "medium",
        "question_text": (
            "Passage: The printing press is usually credited with democratizing knowledge, but "
            "its earliest effect was closer to the opposite. Because Latin manuscripts had been "
            "prohibitively expensive to copy by hand, only a narrow class could afford books at "
            "all; the press initially served this same class more cheaply, before vernacular "
            "printing and rising literacy widened the audience over the following two centuries. "
            "The technology's democratizing power, in other words, was not immediate but was "
            "realized gradually, and only once other social conditions caught up with it.\n\n"
            "Question: The author's main point is that the printing press:"
        ),
        "options": [
            "Had no effect on the spread of knowledge in Europe",
            "Democratized knowledge only after a considerable delay, once literacy and vernacular printing spread",
            "Was rejected by the educated class that had previously relied on hand-copied manuscripts",
            "Was less important to history than is commonly believed",
        ],
        "correct_answer": "Democratized knowledge only after a considerable delay, once literacy and vernacular printing spread",
        "explanation": (
            "The passage says the press's democratizing effect 'was not immediate but was "
            "realized gradually' once literacy and vernacular printing caught up — matching "
            "the second option exactly. The passage does not claim the press was unimportant "
            "or rejected."
        ),
    },
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Reading Comprehension",
        "difficulty": "medium",
        "question_text": (
            "Passage: Behavioural economists have shown that people weigh potential losses "
            "roughly twice as heavily as equivalent gains, a pattern called loss aversion. This "
            "asymmetry explains many decisions that look irrational under classical economic "
            "theory: an investor holding a losing stock far longer than a winning one, or a "
            "negotiator rejecting a fair deal because it is framed as a concession rather than a "
            "gain. Loss aversion is not a flaw to be corrected so much as a stable feature of "
            "how the human mind evaluates risk, one that any realistic model of decision-making "
            "must accommodate.\n\n"
            "Question: The passage suggests that classical economic theory struggles to explain "
            "certain investor and negotiator behaviours because it:"
        ),
        "options": [
            "Assumes people evaluate gains and losses symmetrically",
            "Ignores the existence of financial markets",
            "Was developed before negotiation theory existed",
            "Overestimates how rational investors are about long-term holdings",
        ],
        "correct_answer": "Assumes people evaluate gains and losses symmetrically",
        "explanation": (
            "Classical theory treats gains and losses of equal size as equally significant; "
            "loss aversion (weighing losses about twice as heavily) breaks that assumption, "
            "which is why loss-averse behaviour looks 'irrational' under the classical model."
        ),
    },
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Reading Comprehension",
        "difficulty": "hard",
        "question_text": (
            "Passage: It is tempting to treat memory as a recording device, storing experience "
            "faithfully for later playback. Neuroscience suggests something closer to the "
            "opposite: each act of recall is also an act of reconstruction, subtly rewriting the "
            "memory in light of present knowledge and emotion. This is why eyewitness testimony, "
            "however sincerely given, is among the least reliable forms of evidence a court can "
            "consider — not because witnesses lie, but because the very act of remembering "
            "alters what is remembered.\n\n"
            "Question: It can be inferred from the passage that the unreliability of eyewitness "
            "testimony stems chiefly from:"
        ),
        "options": [
            "Witnesses deliberately distorting events to suit their interests",
            "The reconstructive nature of memory itself, not dishonesty",
            "Courts failing to cross-examine witnesses rigorously enough",
            "The long delay between an event and a witness's testimony",
        ],
        "correct_answer": "The reconstructive nature of memory itself, not dishonesty",
        "explanation": (
            "The passage explicitly states testimony is unreliable 'not because witnesses lie, "
            "but because the very act of remembering alters what is remembered' — directly "
            "supporting the second option and ruling out dishonesty as the cause."
        ),
    },
    {
        "section": "VARC",
        "question_type": "TITA",
        "topic": "Para-jumbles",
        "difficulty": "medium",
        "question_text": (
            "The four sentences below, labelled 1, 2, 3, and 4, can be arranged into a coherent "
            "paragraph. Type the correct order as a sequence of numbers (e.g., 3421).\n\n"
            "1. As a result, coral reefs that took centuries to form can bleach and die within a "
            "single unusually warm summer.\n"
            "2. Coral polyps host colourful algae that supply them with food through "
            "photosynthesis, in exchange for shelter.\n"
            "3. When ocean temperatures rise even slightly above normal, the polyps expel these "
            "algae in a stress response known as bleaching.\n"
            "4. Without their algae, the corals lose both their colour and their primary food "
            "source, leaving them pale and vulnerable to starvation."
        ),
        "options": None,
        "correct_answer": "2341",
        "explanation": (
            "Sentence 2 introduces the coral-algae relationship; sentence 3 introduces the "
            "stress response (bleaching) triggered by warming; sentence 4 explains the "
            "immediate consequence (loss of colour and food); sentence 1 states the ultimate "
            "consequence (reef death). The logical chain is therefore 2-3-4-1."
        ),
    },
    {
        "section": "VARC",
        "question_type": "TITA",
        "topic": "Para-jumbles",
        "difficulty": "hard",
        "question_text": (
            "The four sentences below, labelled 1, 2, 3, and 4, can be arranged into a coherent "
            "paragraph. Type the correct order as a sequence of numbers (e.g., 3421).\n\n"
            "1. Yet this same amygdala response, when chronically triggered by modern "
            "stressors like financial anxiety or social media conflict, produces no such "
            "useful outlet.\n"
            "2. The amygdala, a small almond-shaped structure deep in the brain, evolved "
            "primarily to detect physical threats and trigger a rapid fight-or-flight response.\n"
            "3. For most of human history, that response was adaptive: it prepared the body to "
            "outrun a predator or fend off an attacker.\n"
            "4. The result is a body primed repeatedly for action it never takes, which "
            "researchers increasingly link to chronic stress-related illness."
        ),
        "options": None,
        "correct_answer": "2314",
        "explanation": (
            "Sentence 2 introduces the amygdala and its evolved function; sentence 3 explains "
            "why that function was historically adaptive; sentence 1 pivots ('Yet') to how the "
            "same response misfires today; sentence 4 states the resulting harm. Order: "
            "2-3-1-4."
        ),
    },
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Paragraph Summary",
        "difficulty": "medium",
        "question_text": (
            "Paragraph: Microfinance was once hailed as a near-complete solution to poverty, on "
            "the theory that small loans would let the poor start businesses and lift themselves "
            "out of hardship. Two decades of rigorous field studies have complicated that story: "
            "borrowers do gain more flexibility to manage cash flow and cope with emergencies, "
            "but average incomes and business growth rise only modestly, if at all. Microfinance, "
            "it now appears, is a useful financial tool rather than a standalone engine of "
            "economic transformation.\n\n"
            "Question: Which summary best captures the paragraph?"
        ),
        "options": [
            "Microfinance has been proven entirely ineffective at helping the poor.",
            "Microfinance improves cash-flow flexibility but is not, by itself, the powerful anti-poverty engine it was once believed to be.",
            "Field studies show microfinance dramatically increases average incomes.",
            "Microfinance was designed only to help the poor manage emergencies, not grow businesses.",
        ],
        "correct_answer": "Microfinance improves cash-flow flexibility but is not, by itself, the powerful anti-poverty engine it was once believed to be.",
        "explanation": (
            "The paragraph concedes a real but modest benefit (cash-flow flexibility) while "
            "explicitly downgrading microfinance from 'near-complete solution' to 'useful "
            "financial tool' — the second option captures both halves; the others overstate "
            "or misstate the paragraph's claims."
        ),
    },
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Paragraph Summary",
        "difficulty": "hard",
        "question_text": (
            "Paragraph: Antibiotic resistance is often described as bacteria 'learning' to "
            "survive our drugs, as though resistance were a response invented for the occasion. "
            "In reality, resistance genes are ancient, predating human antibiotic use by millions "
            "of years, having evolved in soil microbes competing with each other for resources. "
            "What antibiotics do is not create resistance but select for it: bacteria that "
            "already happened to carry a resistance gene survive and multiply, while susceptible "
            "ones die off, shifting the population's genetic makeup over time.\n\n"
            "Question: Which summary best captures the paragraph?"
        ),
        "options": [
            "Antibiotics directly cause bacteria to invent new resistance genes.",
            "Resistance genes are a recent phenomenon caused entirely by human antibiotic overuse.",
            "Antibiotics select for pre-existing, ancient resistance genes rather than causing bacteria to newly develop them.",
            "Soil microbes are immune to all forms of antibiotic treatment.",
        ],
        "correct_answer": "Antibiotics select for pre-existing, ancient resistance genes rather than causing bacteria to newly develop them.",
        "explanation": (
            "The paragraph's central correction is that antibiotics 'select for' resistance "
            "that already existed in ancient genes, rather than causing bacteria to invent it — "
            "exactly the third option; the others contradict the passage's explicit claims."
        ),
    },
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Odd Sentence Out",
        "difficulty": "medium",
        "question_text": (
            "Five sentences numbered 1-5 are given below. Four of them, when arranged in the "
            "right order, form a coherent paragraph. Identify the sentence that does NOT fit.\n\n"
            "1. Venice was built on more than a hundred small islands in a marshy lagoon, a "
            "site chosen precisely because it was difficult to attack.\n"
            "2. Its early settlers were refugees fleeing invasions on the Italian mainland in "
            "the fifth and sixth centuries.\n"
            "3. Modern Venice attracts over twenty million tourists a year, straining its "
            "fragile infrastructure.\n"
            "4. Over the following centuries, this defensible position allowed Venice to grow "
            "into a major maritime trading power.\n"
            "5. By the height of its power, Venetian ships controlled much of the trade route "
            "between Europe and the East."
        ),
        "options": ["Sentence 1", "Sentence 2", "Sentence 3", "Sentence 5"],
        "correct_answer": "Sentence 3",
        "explanation": (
            "Sentences 2, 1, 4, and 5 trace a continuous historical narrative — founding, "
            "site choice, rise to power, peak trade dominance. Sentence 3 jumps to modern "
            "tourism, breaking that historical thread, so it is the odd one out."
        ),
    },
    {
        "section": "VARC",
        "question_type": "MCQ",
        "topic": "Odd Sentence Out",
        "difficulty": "hard",
        "question_text": (
            "Five sentences numbered 1-5 are given below. Four of them, when arranged in the "
            "right order, form a coherent paragraph. Identify the sentence that does NOT fit.\n\n"
            "1. Deep-sea hydrothermal vents release water heated by magma to several hundred "
            "degrees Celsius.\n"
            "2. Around these vents live entire ecosystems that derive energy not from sunlight "
            "but from chemical reactions involving dissolved minerals.\n"
            "3. Coral reefs, by contrast, depend almost entirely on sunlight reaching shallow "
            "tropical waters.\n"
            "4. Bacteria at the base of the vent food chain convert hydrogen sulfide into "
            "usable energy through a process called chemosynthesis.\n"
            "5. Tube worms and vent crabs then feed on these bacteria, forming a food web "
            "entirely independent of the sun."
        ),
        "options": ["Sentence 1", "Sentence 3", "Sentence 4", "Sentence 5"],
        "correct_answer": "Sentence 3",
        "explanation": (
            "Sentences 1, 2, 4, and 5 build a single continuous explanation of sunlight-"
            "independent vent ecosystems. Sentence 3 introduces coral reefs, an unrelated, "
            "sunlight-dependent ecosystem used only as a contrast, which breaks the paragraph's "
            "internal flow — making it the odd one out."
        ),
    },
    # ---------------------------------------------------------------- DILR (10) ----
    {
        "section": "DILR",
        "question_type": "MCQ",
        "topic": "Data Table Interpretation",
        "difficulty": "easy",
        "question_text": (
            "The table below shows the number of units sold by four salespersons in three "
            "months:\n\n"
            "Salesperson | Jan | Feb | Mar\n"
            "P           | 120 | 150 | 90\n"
            "Q           | 100 | 130 | 140\n"
            "R           | 160 | 110 | 120\n"
            "S           | 90  | 140 | 130\n\n"
            "Question: Who sold the highest total number of units across the three months?"
        ),
        "options": ["P", "Q", "R", "S"],
        "correct_answer": "R",
        "explanation": (
            "Totals: P = 120+150+90 = 360; Q = 100+130+140 = 370; "
            "R = 160+110+120 = 390; S = 90+140+130 = 360. R's total of 390 is the highest."
        ),
    },
    {
        "section": "DILR",
        "question_type": "MCQ",
        "topic": "Linear Arrangement",
        "difficulty": "medium",
        "question_text": (
            "Five students P, Q, R, S, T sit in a row of five seats (numbered 1 to 5, left to "
            "right), facing north. Q sits second from the left end. R sits immediately to the "
            "right of Q. T sits at the right end. S sits immediately to the left of T. P sits "
            "somewhere to the left of R.\n\n"
            "Question: Who sits exactly in the middle (3rd position) of the row?"
        ),
        "options": ["P", "Q", "R", "S"],
        "correct_answer": "R",
        "explanation": (
            "Q is 2nd from the left, so Q is in seat 2. R is immediately right of Q, so R is "
            "in seat 3. T is at the right end, seat 5. S is immediately left of T, so S is in "
            "seat 4. The only seat left, seat 1, goes to P, which is indeed left of R — "
            "consistent. The full order is P, Q, R, S, T, so seat 3 (the middle) is R."
        ),
    },
    {
        "section": "DILR",
        "question_type": "TITA",
        "topic": "Venn Diagrams",
        "difficulty": "medium",
        "question_text": (
            "In a class of 60 students, 35 play cricket, 30 play football, and 12 play neither "
            "sport. How many students play both cricket and football?"
        ),
        "options": None,
        "correct_answer": "17",
        "explanation": (
            "Students playing at least one sport = 60 - 12 = 48. By the union formula, "
            "Cricket + Football - Both = 48, so 35 + 30 - Both = 48, giving Both = 17."
        ),
    },
    {
        "section": "DILR",
        "question_type": "TITA",
        "topic": "Logical Reasoning",
        "difficulty": "easy",
        "question_text": (
            "In a class test, Meera ranks 7th from the top and 15th from the bottom. How many "
            "students are there in the class, assuming no ties?"
        ),
        "options": None,
        "correct_answer": "21",
        "explanation": (
            "Total students = (rank from top - 1) + (rank from bottom - 1) + 1 (for Meera "
            "herself) = 6 + 14 + 1 = 21."
        ),
    },
    {
        "section": "DILR",
        "question_type": "MCQ",
        "topic": "Blood Relations",
        "difficulty": "medium",
        "question_text": (
            "Pointing to a photograph, Rohan said, 'She is the daughter of my grandfather's "
            "only son.'\n\n"
            "Question: How is the girl in the photograph related to Rohan?"
        ),
        "options": ["Sister", "Daughter", "Niece", "Cousin"],
        "correct_answer": "Sister",
        "explanation": (
            "Rohan's grandfather's only son must be Rohan's own father (since it is the only "
            "son). The daughter of Rohan's father is Rohan's sister."
        ),
    },
    {
        "section": "DILR",
        "question_type": "MCQ",
        "topic": "Coding-Decoding",
        "difficulty": "easy",
        "question_text": (
            "In a certain code, each letter of a word is replaced by the next letter of the "
            "English alphabet, so 'TABLE' is written as 'UBCMF'.\n\n"
            "Question: Using the same coding pattern, how is 'CHAIR' written?"
        ),
        "options": ["DIBJS", "DIBJT", "DHBIS", "DIAJS"],
        "correct_answer": "DIBJS",
        "explanation": (
            "Shifting each letter of CHAIR forward by one: C->D, H->I, A->B, I->J, R->S, "
            "giving DIBJS."
        ),
    },
    {
        "section": "DILR",
        "question_type": "TITA",
        "topic": "Data Table Interpretation",
        "difficulty": "easy",
        "question_text": (
            "A student scored the following marks (out of 100) in five subjects: "
            "Maths 88, Physics 76, Chemistry 82, English 70, Economics 84.\n\n"
            "What is the student's average score across all five subjects?"
        ),
        "options": None,
        "correct_answer": "80",
        "explanation": "Sum = 88+76+82+70+84 = 400. Average = 400 / 5 = 80.",
    },
    {
        "section": "DILR",
        "question_type": "TITA",
        "topic": "Number Series",
        "difficulty": "medium",
        "question_text": "Look at this series: 3, 6, 11, 18, 27, ... What number should come next?",
        "options": None,
        "correct_answer": "38",
        "explanation": (
            "The differences between consecutive terms are 3, 5, 7, 9 — consecutive odd "
            "numbers. The next difference is 11, so the next term is 27 + 11 = 38."
        ),
    },
    {
        "section": "DILR",
        "question_type": "MCQ",
        "topic": "Logical Reasoning",
        "difficulty": "hard",
        "question_text": (
            "Four friends A, B, C, D each ordered a different beverage (Tea, Coffee, Juice, "
            "Soda) and a different snack (Sandwich, Burger, Fries, Salad). It is known that:\n"
            "1. A did not order Tea.\n"
            "2. B ordered Coffee.\n"
            "3. C ordered Juice.\n"
            "4. D ordered Sandwich.\n"
            "5. C ordered Fries.\n"
            "6. B did not order Salad.\n\n"
            "Question: What did A order to drink and eat?"
        ),
        "options": ["Soda and Salad", "Soda and Burger", "Tea and Salad", "Juice and Burger"],
        "correct_answer": "Soda and Salad",
        "explanation": (
            "Drinks: B=Coffee, C=Juice, so Tea and Soda remain for A and D; since A did not "
            "order Tea, A=Soda and D=Tea. Snacks: D=Sandwich, C=Fries, so Burger and Salad "
            "remain for A and B; since B did not order Salad, B=Burger and A=Salad. So A "
            "ordered Soda to drink and Salad to eat."
        ),
    },
    {
        "section": "DILR",
        "question_type": "TITA",
        "topic": "Data Table Interpretation",
        "difficulty": "medium",
        "question_text": (
            "A survey of 200 people found that 45% prefer tea, 30% prefer coffee, and the rest "
            "prefer neither. How many people prefer neither tea nor coffee?"
        ),
        "options": None,
        "correct_answer": "50",
        "explanation": (
            "Percentage preferring neither = 100% - 45% - 30% = 25%. 25% of 200 = 50 people."
        ),
    },
    # ------------------------------------------------------------------ QA (10) ----
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Number Systems",
        "difficulty": "easy",
        "question_text": "What is the remainder when 7^100 is divided by 5?",
        "options": None,
        "correct_answer": "1",
        "explanation": (
            "7 mod 5 = 2, so 7^100 mod 5 = 2^100 mod 5. Since 2^4 = 16 ≡ 1 (mod 5), and "
            "100 = 4 x 25, 2^100 ≡ 1^25 = 1 (mod 5). The remainder is 1."
        ),
    },
    {
        "section": "QA",
        "question_type": "MCQ",
        "topic": "Percentages",
        "difficulty": "medium",
        "question_text": (
            "A shopkeeper marks his goods 40% above cost price and then gives a discount of "
            "15% on the marked price. What is his overall profit percentage?"
        ),
        "options": ["17%", "19%", "21%", "25%"],
        "correct_answer": "19%",
        "explanation": (
            "Let CP = 100. Marked price = 140. Discount = 15% of 140 = 21, so SP = 140 - 21 "
            "= 119. Profit = SP - CP = 19, i.e., a profit of 19%."
        ),
    },
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Time Speed Distance",
        "difficulty": "medium",
        "question_text": (
            "Two trains, 150 m and 120 m long, run in opposite directions on parallel tracks at "
            "speeds of 54 km/h and 36 km/h respectively. How long (in seconds) will they take to "
            "completely cross each other?"
        ),
        "options": None,
        "correct_answer": "10.8",
        "explanation": (
            "Relative speed (opposite directions) = 54 + 36 = 90 km/h = 25 m/s. Total distance "
            "to be covered = 150 + 120 = 270 m. Time = 270 / 25 = 10.8 seconds."
        ),
    },
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Algebra",
        "difficulty": "hard",
        "question_text": "If x + 1/x = 3, what is the value of x^3 + 1/x^3?",
        "options": None,
        "correct_answer": "18",
        "explanation": (
            "x^3 + 1/x^3 = (x + 1/x)^3 - 3(x + 1/x) = 3^3 - 3(3) = 27 - 9 = 18."
        ),
    },
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Geometry",
        "difficulty": "medium",
        "question_text": (
            "The area of an equilateral triangle is 16√3 cm^2. What is the perimeter of the "
            "triangle, in cm?"
        ),
        "options": None,
        "correct_answer": "24",
        "explanation": (
            "Area of an equilateral triangle with side a is (√3/4) a^2. Setting (√3/4) a^2 = "
            "16√3 gives a^2 = 64, so a = 8 cm. Perimeter = 3a = 24 cm."
        ),
    },
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Mixtures and Alligations",
        "difficulty": "hard",
        "question_text": (
            "A vessel contains a mixture of milk and water in the ratio 5:3. If 16 litres of "
            "the mixture is replaced with pure water, the ratio of milk to water becomes 5:7. "
            "What was the initial quantity of the mixture, in litres?"
        ),
        "options": None,
        "correct_answer": "48",
        "explanation": (
            "Let the initial quantity be 8x litres (milk = 5x, water = 3x). Removing 16 litres "
            "of mixture removes 10 litres of milk and 6 litres of water (in the 5:3 ratio), "
            "leaving milk = 5x - 10 and water = 3x - 6 + 16 = 3x + 10 (16 litres of pure water "
            "is added back). Setting (5x - 10)/(3x + 10) = 5/7 and cross-multiplying: "
            "7(5x - 10) = 5(3x + 10) => 35x - 70 = 15x + 50 => 20x = 120 => x = 6. Initial "
            "quantity = 8x = 48 litres."
        ),
    },
    {
        "section": "QA",
        "question_type": "MCQ",
        "topic": "Number Systems",
        "difficulty": "hard",
        "question_text": "How many factors of 720 are perfect squares?",
        "options": ["4", "6", "8", "9"],
        "correct_answer": "6",
        "explanation": (
            "720 = 2^4 x 3^2 x 5^1. A factor is a perfect square only if every prime's "
            "exponent in it is even. For 2^4: exponent can be 0, 2, or 4 (3 choices). For "
            "3^2: exponent can be 0 or 2 (2 choices). For 5^1: exponent must be 0 (1 choice, "
            "since 1 is odd and unavailable as an even exponent). Total perfect-square "
            "factors = 3 x 2 x 1 = 6."
        ),
    },
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Time and Work",
        "difficulty": "medium",
        "question_text": (
            "A can complete a work in 12 days and B can complete it in 18 days. They work "
            "together for 4 days, after which A leaves. In how many more days will B alone "
            "complete the remaining work?"
        ),
        "options": None,
        "correct_answer": "8",
        "explanation": (
            "A's rate = 1/12 per day, B's rate = 1/18 per day. Combined rate = 1/12 + 1/18 = "
            "5/36 per day. In 4 days, work done = 4 x 5/36 = 20/36 = 5/9. Remaining work = "
            "4/9. B alone takes (4/9) / (1/18) = (4/9) x 18 = 8 days."
        ),
    },
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Permutation and Combination",
        "difficulty": "hard",
        "question_text": (
            "In how many ways can the letters of the word 'MOBILE' be arranged so that the "
            "vowels always come together?"
        ),
        "options": None,
        "correct_answer": "144",
        "explanation": (
            "MOBILE has vowels O, I, E and consonants M, B, L. Treating the 3 vowels as a "
            "single block gives 4 units (the block plus 3 consonants) to arrange: 4! = 24 "
            "ways. Within the block, the 3 vowels can be arranged in 3! = 6 ways. Total = "
            "24 x 6 = 144."
        ),
    },
    {
        "section": "QA",
        "question_type": "TITA",
        "topic": "Simple and Compound Interest",
        "difficulty": "easy",
        "question_text": (
            "What is the compound interest (in Rs.) on Rs. 25,000 at 8% per annum for 2 years, "
            "compounded annually?"
        ),
        "options": None,
        "correct_answer": "4160",
        "explanation": (
            "CI = P[(1 + r)^n - 1] = 25000 x [(1.08)^2 - 1] = 25000 x [1.1664 - 1] = "
            "25000 x 0.1664 = Rs. 4160."
        ),
    },
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_count = db.query(CatQuestion).count()
        if existing_count > 0:
            print(f"cat_questions already has {existing_count} rows; skipping seed.")
            return

        for q in QUESTIONS:
            db.add(
                CatQuestion(
                    section=q["section"],
                    question_type=q["question_type"],
                    topic=q["topic"],
                    difficulty=q["difficulty"],
                    source="pyq",
                    source_year=None,
                    source_slot=None,
                    question_text=q["question_text"],
                    options=q["options"],
                    correct_answer=q["correct_answer"],
                    explanation=q["explanation"],
                    is_active=True,
                )
            )
        db.commit()
        print(f"Seeded {len(QUESTIONS)} CAT questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

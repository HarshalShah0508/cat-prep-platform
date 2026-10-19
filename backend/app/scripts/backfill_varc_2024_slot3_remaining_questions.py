"""Add the 23 CAT 2024 VARC Slot 3 questions missing from the DB.

`seed_cat_pyq_2024_varc.py` only ever wrote slot1/slot2 - slot3 was never
authored, except for the one Paragraph Summary question added separately by
`backfill_varc_2024_slot3_missing_question.py` (id 1201, the lyric-poetry/
Marxism summary - skipped here to avoid a duplicate).

Transcribed verbatim from pyq-source/2024/VARC_SLOT3_CAT_2024.pdf (question
text, options, RC passages) with correct_answer/explanation cross-checked
against pyq-source/2024/VARC_SLOT3_CAT_2024_SOLUTIONS.pdf (every answer
confirmed against that key - the solutions PDF's lettered options also
confirmed the real on-paper option order used for the three sentence-
insertion questions, which the source question PDF itself leaves unordered).

Run with:
    python -m app.scripts.backfill_varc_2024_slot3_remaining_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"


def q(group_id, topic, qtype, text, options, correct_answer, explanation, passage=None):
    return {
        "section": "VARC",
        "question_type": qtype,
        "topic": topic,
        "difficulty": "hard",
        "source": "pyq",
        "source_year": SOURCE_YEAR,
        "source_slot": SOURCE_SLOT,
        "group_id": group_id,
        "passage_text": passage,
        "question_text": text,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation,
    }


QUESTIONS = []

# ---- Q1: Odd Sentence Out ----
QUESTIONS.append(q(
    None, "Odd Sentence Out", "TITA",
    "Five jumbled up sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the odd "
    "sentence and key in the number of that sentence as your answer.\n"
    "1. To create a synapse, the neuron has specialized structures, often seen as tiny "
    "swellings, at its terminal end of the axon where it stores the chemicals that are "
    "emitted to transmit a signal to the next neuron.\n"
    "2. This fetal warm-up act—the soldering of neural connections before the eyes "
    "actually function—is crucial to the performance of the visual system.\n"
    "3. The reasons for this paring back of synapses is a mystery, but synaptic pruning is "
    "thought to sharpen and reinforce the “correct” synapses, while removing the "
    "weak and unnecessary ones.\n"
    "4. Neural connections between the eyes and the brain are formed long before birth, "
    "establishing the wiring and the circuitry that allow a child to begin visualizing the "
    "world the minute she emerges from the womb.\n"
    "5. During this rehearsal period, synapses—points of chemical connection—between "
    "nerve cells are generated in great excess, only to be pruned back during later "
    "development.",
    None,
    "1",
    "Sentences 2, 4, 5, 3 form a clean chain on fetal visual-system wiring: connections form "
    "before birth (4) as a warm-up for vision (2), synapses are over-produced during this "
    "rehearsal (5) and then pruned back (3). Sentence 1 shifts to the physical structure of a "
    "synapse in general, unrelated to the fetal-development narrative - it's the odd one out.",
))

# ---- Q2: Paragraph Summary (tradwife) ----
QUESTIONS.append(q(
    None, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "When the tradwife puts on that georgic, pinstriped dress, she is not just admiring the "
    "visual cues of a fantastical past. She takes these dreams of storybook bliss literally, "
    "tracing them backward in time until she reaches a logical conclusion that satisfies "
    "her. And by doing so, she ends up delivering an unhappy reminder of just how much our "
    "lives consist of artifice and playacting. The tradwife outrages people because of her "
    "deliberately regressive ideals. And yet her behaviour is, on some level, "
    "indistinguishable from the nontradwife's. The tradwife's trollish genius is to beat us "
    "at our own dress-up game. By insisting that the idyllic cottage daydream should be "
    "real, right down to the primitive gender roles, she leaves others feeling hollow, "
    "cheated. The hullabaloo and headaches she causes may be the price we pay for taking "
    "too many things at face value: our just deserts, served Instagram-perfect by a "
    "manicured hand on a gorgeous ceramic dish, with fat, mouthwatering maraschino cherries "
    "on top.",
    [
        "By promoting an idealized past, the tradwife exposes the artifice of contemporary "
        "values and mocks societal norms.",
        "The tradwife, with her vintage dress and traditional roles, highlights the "
        "superficiality of modern life and challenges current societal norms.",
        "The tradwife's commitment to outdated gender roles and retro fashion critiques the "
        "superficiality of today's societal ideals.",
        "The tradwife's vintage dress and adherence to traditional roles reveal the "
        "artificial nature of modern life and its superficial values.",
    ],
    "The tradwife, with her vintage dress and traditional roles, highlights the "
    "superficiality of modern life and challenges current societal norms.",
    "The passage's core move is that the tradwife's literal commitment to a fantasy "
    "\"outrages\" and \"challenges\" people precisely because the rest of us play the same "
    "dress-up game less honestly - she exposes that artifice by insisting hers is real. "
    "Option 2 is the only one that keeps both halves: the vintage/traditional performance, "
    "and its active role in challenging (not just revealing) modern norms. Options 1, 3 and "
    "4 drop or flatten the \"challenges/outrages\" dynamic into a passive \"reveals\".",
))

# ---- Q3: Paragraph Summary (biotech regulation) ----
QUESTIONS.append(q(
    None, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "Humans have managed to tweak the underlying biology of various plants and animals to "
    "produce high-tech crops and microbes. But regulating these entities is complicated, as "
    "the framework of policies and procedures are outdated and not flexible enough to adapt "
    "to emerging technology. The question is whether regulation will ever be able to keep "
    "up with human innovation, to regulate living things, which are apt to be unpredictable "
    "and unique; to capture all the potential risks when new biological entities are "
    "introduced, or when they pass on variations of their genes?",
    [
        "Current regulation of biotechnology is outdated, but it is debatable if we can "
        "create a framework, imaginative and flexible, to cover all contingencies in this "
        "fast-changing area.",
        "The mercurial nature of biological entities calls for scientists to shape the "
        "regulations governing emerging technology, with regular calibration to handle "
        "variations in the field.",
        "The problem with formulating regulation for innovation in the scientific arena is "
        "that it is impossible to imagine the outcomes or risks related to the outcomes of "
        "all the research.",
        "A new framework of rules and procedures for regulating the most recent research "
        "emerging from biotechnology is urgently needed, to keep up with this rapidly "
        "changing discipline.",
    ],
    "Current regulation of biotechnology is outdated, but it is debatable if we can create "
    "a framework, imaginative and flexible, to cover all contingencies in this fast-changing "
    "area.",
    "The passage is framed as an open question (\"whether regulation will ever be able to "
    "keep up\"), not a settled claim. Option 1 preserves that uncertainty (\"it is "
    "debatable\") alongside the outdated-framework point. Options 3 and 4 overstate the "
    "passage into a flat claim of impossibility or urgency the text doesn't make, and "
    "option 2 wrongly assigns the regulation-shaping job to scientists rather than policy.",
))

# ---- Q4: Odd Sentence Out (forecasting) ----
QUESTIONS.append(q(
    None, "Odd Sentence Out", "TITA",
    "Five jumbled up sentences (labelled 1, 2, 3, 4, and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the odd "
    "sentence and key in the number of that sentence as your answer.\n"
    "1. Part of the appeal of forecasting is not just that it seems to work, but that you "
    "don't seem to need specialized expertise to succeed at it.\n"
    "2. The tight connection between forecasting and building a model of the world helps "
    "explain why so much of the early interest in the idea came from the intelligence "
    "community.\n"
    "3. This was true even though the latter had access to classified intelligence.\n"
    "4. One frequently cited study found that accurate forecasters' predictions of "
    "geopolitical events, when aggregated using standard scientific methods, were more "
    "accurate than the forecasts of members of the US intelligence community who answered "
    "the same questions in a confidential prediction market.\n"
    "5. The aggregated opinions of non-experts doing forecasting have proven to be a better "
    "guide to the future than the aggregated opinions of experts.",
    None,
    "2",
    "Sentences 1, 4, 3, 5 chain together on one theme - non-experts outperforming experts at "
    "forecasting, with sentence 4 giving the study, 3 noting the experts still had classified "
    "access, and 5 generalising the finding. Sentence 2 instead talks about forecasting's "
    "link to the intelligence community's early interest in the idea - a different, tangential "
    "point that doesn't feed the non-experts-beat-experts thread.",
))

# ---- Q5: Sentence Insertion (Napalm Girl) ----
QUESTIONS.append(q(
    None, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph and "
    "decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: Taken outside the village of Trang Bang on June 8, 1972, the picture captured "
    "the trauma and indiscriminate violence of a conflict that claimed, by some estimates, a "
    "million or more civilian lives.\n"
    "Paragraph: The horrifying photograph of children fleeing a deadly napalm attack has "
    "become a defining image not only of the Vietnam War but the 20th century. ___(1)___. "
    "Dark smoke billowing behind them, the young subjects' faces are painted with a mixture "
    "of terror, pain, and confusion. ___(2)___. Soldiers from the South Vietnamese army's "
    "25th Division follow helplessly behind. ___(3)___. The picture was officially titled "
    "“The Terror of War,” but the photo is better known by the nickname given to "
    "naked 9-year-old at its centre “Napalm Girl”. ___(4)___.",
    ["Option 1", "Option 2", "Option 3", "Option 4"],
    "Option 3",
    "The missing sentence supplies the date/location/death-toll context that belongs right "
    "before the photo is named - it reads as scene-setting background, not a continuation of "
    "the visual description (ruling out 1, 2) and not a trailing afterthought (ruling out 4). "
    "Placed at (3), it bridges the soldiers-following-behind detail and the \"officially "
    "titled\" sentence that follows.",
))

# ---- Q6: SKIPPED - already in DB as id 1201 (lyric poetry / Marxism summary) ----

_AI_PASSAGE = (
    "Fears of artificial intelligence (AI) have haunted humanity since the very beginning of "
    "the computer age. Hitherto these fears focused on machines using physical means to "
    "kill, enslave or replace people. But over the past couple of years new AI tools have "
    "emerged that threaten the survival of human civilisation from an unexpected direction. "
    "AI has gained some remarkable abilities to manipulate and generate language, whether "
    "with words, sounds or images. AI has thereby hacked the operating system of our "
    "civilisation.\n\n"
    "Language is the stuff almost all human culture is made of. Human rights, for example, "
    "aren't inscribed in our DNA. Rather, they are cultural artefacts we created by telling "
    "stories and writing laws. Gods aren't physical realities. Rather, they are cultural "
    "artefacts we created by inventing myths and writing scriptures....What would happen "
    "once a non-human intelligence becomes better than the average human at telling "
    "stories, composing melodies, drawing images, and writing laws and scriptures? When "
    "people think about Chatgpt and other new AI tools, they are often drawn to examples "
    "like school children using AI to write their essays. What will happen to the school "
    "system when kids do that? But this kind of question misses the big picture. Forget "
    "about school essays. Think of the next American presidential race in 2024, and try to "
    "imagine the impact of AI tools that can be made to mass-produce political content, "
    "fake-news stories and scriptures for new cults...\n\n"
    "Through its mastery of language, AI could even form intimate relationships with "
    "people, and use the power of intimacy to change our opinions and worldviews. Although "
    "there is no indication that AI has any consciousness or feelings of its own, to foster "
    "fake intimacy with humans it is enough if the AI can make them feel emotionally "
    "attached to it....\n\n"
    "What will happen to the course of history when AI takes over culture, and begins "
    "producing stories, melodies, laws and religions? Previous tools like the printing "
    "press and radio helped spread the cultural ideas of humans, but they never created new "
    "cultural ideas of their own. AI is fundamentally different. AI can create completely "
    "new ideas, completely new culture....\n\n"
    "Of course, the new power of AI could be used for good purposes as well. I won't dwell "
    "on this, because the people who develop AI talk about it enough....\n\n"
    "We can still regulate the new AI tools, but we must act quickly. Whereas nukes cannot "
    "invent more powerful nukes, AI can make exponentially more powerful AI.... Unregulated "
    "AI deployments would create social chaos, which would benefit autocrats and ruin "
    "democracies. Democracy is a conversation, and conversations rely on language. When AI "
    "hacks language, it could destroy our ability to have meaningful conversations, thereby "
    "destroying democracy....And the first regulation I would suggest is to make it "
    "mandatory for AI to disclose that it is an AI. If I am having a conversation with "
    "someone, and I cannot tell whether it is a human or an AI—that's the end of "
    "democracy. This text has been generated by a human. Or has it?"
)
_g = "cat2024_varc_slot3_rc1"
QUESTIONS += [
    q(_g, "Reading Comprehension - AI and the hacking of language", "MCQ",
      "We can infer that the author is most likely to agree with which of the following "
      "statements?",
      [
          "One of the biggest casualties from the spread of unregulated AI is likely to be "
          "the democratic process.",
          "Apart from its drawbacks, AI tools have been beneficial in boosting "
          "technological and industrial advance worldwide.",
          "The commonly expressed fear that future AI developments will fatally harm "
          "humans is unfounded.",
          "People's fears of the dangers of students using ChatGPT and other new AI tools "
          "are unfounded.",
      ],
      "One of the biggest casualties from the spread of unregulated AI is likely to be the "
      "democratic process.",
      "The entire final section argues AI hacking language would \"ruin democracies\" and "
      "\"destroy our ability to have meaningful conversations, thereby destroying "
      "democracy\" - that's the passage's central, explicit worry, not a side point. The "
      "other options either praise AI (2), or dismiss fears the author clearly holds (3, 4).",
      passage=_AI_PASSAGE),
    q(_g, "Reading Comprehension - AI and the hacking of language", "MCQ",
      "The tone of the passage could best be described as",
      [
          "Alarmist, because the passage discusses scenarios of the influence of new AI "
          "tools on language and human emotions.",
          "Cautionary, because the author lays out some adverse effects of the "
          "proliferation of unregulated AI tools.",
          "Prescient, as the author analyses the future impact of the use of new AI tools "
          "on crucial areas of our society and culture.",
          "Quizzical, as the passage poses several questions, concluding with the question "
          "of whether or not the passage content has been generated by AI.",
      ],
      "Cautionary, because the author lays out some adverse effects of the proliferation of "
      "unregulated AI tools.",
      "The author isn't just describing risks dramatically (alarmist) or merely posing "
      "open questions (quizzical) - the piece builds to a concrete call to \"regulate the "
      "new AI tools\" and a specific proposed rule, which is the hallmark of a cautionary, "
      "not alarmist or quizzical, tone.",
      passage=_AI_PASSAGE),
    q(_g, "Reading Comprehension - AI and the hacking of language", "MCQ",
      "The author terms language “the operating system of our civilization” for "
      "all the following reasons EXCEPT that it",
      [
          "Has laid the foundation for the creation of cultural artefacts through writing "
          "and telling of stories.",
          "Is the basis of AI tools like ChatGPT which can be used to generate academic "
          "content and opinion.",
          "Can influence political views and opinions as it engenders close emotional ties "
          "among people.",
          "Is fundamental to the articulation and spread of human values and culture in our "
          "society.",
      ],
      "Is the basis of AI tools like ChatGPT which can be used to generate academic content "
      "and opinion.",
      "The \"operating system\" framing is about language being the substrate of human "
      "culture, rights, myths and values (options 1, 3, 4 all restate this). Option 2 "
      "inverts the relationship - it's about AI being built on language, not language's own "
      "civilizational role - making it the one reason not actually given for the label.",
      passage=_AI_PASSAGE),
    q(_g, "Reading Comprehension - AI and the hacking of language", "MCQ",
      "The author identifies all of the following as dire outcomes of the capture of "
      "language by AI EXCEPT that it could",
      [
          "Eventually subvert democratic processes through the mass creation and spread of "
          "fake political content and news.",
          "Apply its mastery of language to create strong emotional ties which could "
          "exacerbate the polarization of political views.",
          "Spawn a completely new culture through its ability to create new ideas and "
          "opinions.",
          "Out-strip human creativity and endeavours in the spheres such as art and music "
          "and, in the formulation of laws.",
      ],
      "Apply its mastery of language to create strong emotional ties which could exacerbate "
      "the polarization of political views.",
      "The passage does say AI can form fake intimate relationships to \"change our "
      "opinions and worldviews\" - but it never frames that as exacerbating political "
      "polarization specifically; that linkage is invented. Options 1, 3 and 4 all restate "
      "outcomes the passage states directly (subverting democracy, creating new culture, "
      "out-creating humans).",
      passage=_AI_PASSAGE),
]

_MARS_PASSAGE = (
    "There is a group in the space community who view the solar system not as an "
    "opportunity to expand human potential but as a nature preserve, forever the provenance "
    "of an elite group of scientists and their sanitary robotic probes. These planetary "
    "protection advocates [call] for avoiding “harmful contamination” of celestial "
    "bodies. Under this regime, NASA incurs great expense sterilizing robotic probes in "
    "order to prevent the contamination of entirely theoretical biospheres. . . .\n\n"
    "Transporting bacteria would matter if Mars were the vital world once imagined by "
    "astronomers who mistook optical illusions for canals. Nobody wants to expose Martians "
    "to measles, but sadly, robotic exploration reveals a bleak, rusted landscape, lacking "
    "oxygen and flooded with radiation ready to sterilize any Earthly microbes. Simple life "
    "might exist underground, or down at the bottom of a deep canyon, but it has been very "
    "hard to find with robots. . . . The upsides from human exploration and development of "
    "Mars clearly outweigh the welfare of purely speculative Martian fungi. . . .\n\n"
    "The other likely targets of human exploration, development, and settlement, our moon "
    "and the asteroids, exist in a desiccated, radiation-soaked realm of hard vacuum and "
    "extreme temperature variations that would kill nearly anything. It's also important to "
    "note that many international competitors will ignore the demands of these protection "
    "extremists in any case. For example, China recently sent a terrarium to the moon and "
    "germinated a plant seed—with, unsurprisingly, no protest from its own scientific "
    "community. In contrast, when it was recently revealed that a researcher had "
    "surreptitiously smuggled super-resilient microscopic tardigrades aboard the ill-fated "
    "Israeli Beresheet lunar probe, a firestorm was unleashed within the space community. . "
    ". .\n\n"
    "NASA's previous human exploration efforts made no serious attempt at sterility, with "
    "little notice. As the Mars expert Robert Zubrin noted in the National Review, U.S. "
    "lunar landings did not leave the campsites cleaner than they found it. Apollo's "
    "bacteria-infested litter included bags of feces. Forcing NASA's proposed Mars "
    "exploration to do better, scrubbing everything and hauling out all the trash, would "
    "destroy NASA's human exploration budget and encroach on the agency's other "
    "directorates, too. Getting future astronauts off Mars is enough of a challenge, "
    "without trying to tote weeks of waste along as well.\n\n"
    "A reasonable compromise is to continue on the course laid out by the U.S. government "
    "and the National Research Council, which proposed a system of zones on Mars, some for "
    "science only, some for habitation, and some for resource exploitation. This approach "
    "minimizes contamination, maximizes scientific exploration . . . Mars presents a stark "
    "choice of diverging human futures. We can turn inward, pursuing ever more limited "
    "futures while we await whichever natural or manmade disaster will eradicate our "
    "species and life on Earth. Alternatively, we can choose to propel our biosphere "
    "further into the solar system, simultaneously protecting our home planet and providing "
    "a backup plan for the only life we know exists in the universe. Are the lives on Earth "
    "worth less than some hypothetical microbe lurking under Martian rocks?"
)
_g = "cat2024_varc_slot3_rc2"
QUESTIONS += [
    q(_g, "Reading Comprehension - planetary protection vs Mars exploration", "MCQ",
      "The contrasting reactions to the Chinese and Israeli “contaminations” of "
      "lunar space",
      [
          "Are evidence of China's reasonable approach towards space contamination.",
          "Are valid as the contamination of the lunar environment from animal sources is "
          "far greater than from plants.",
          "Indicate that national scientists may have different sensitivities to issues of "
          "biosphere protection.",
          "Reveal global biases prevalent in attitudes towards different countries.",
      ],
      "Indicate that national scientists may have different sensitivities to issues of "
      "biosphere protection.",
      "China's plant seed drew no protest from its own scientists while Israel's smuggled "
      "tardigrades caused a \"firestorm\" - the passage uses this purely as a contrast in "
      "how seriously different scientific communities take contamination, not as a verdict "
      "on which country is \"reasonable\" (1) or a claim about bias between countries (4) or "
      "plant-vs-animal contamination severity (2), none of which the passage argues.",
      passage=_MARS_PASSAGE),
    q(_g, "Reading Comprehension - planetary protection vs Mars exploration", "MCQ",
      "The author's overall tone in the first paragraph can be described as",
      [
          "Equivocal about the reasons extended by the group of scientists seeking to limit "
          "space exploration.",
          "Indifferent to the elitism of a few scientists aiming to corner space "
          "exploration.",
          "Approving of the amount of money NASA spends to restrict the spread of "
          "contamination in space.",
          "Sceptical about the excessive efforts to sanitise planets where life has not yet "
          "been proven to exist.",
      ],
      "Sceptical about the excessive efforts to sanitise planets where life has not yet "
      "been proven to exist.",
      "Phrases like \"entirely theoretical biospheres\" signal open scepticism, not "
      "indifference or approval - the author is clearly needling the planetary-protection "
      "position from the first paragraph, which rules out options 2 and 3 outright and is "
      "too pointed to be merely \"equivocal\" (1).",
      passage=_MARS_PASSAGE),
    q(_g, "Reading Comprehension - planetary protection vs Mars exploration", "MCQ",
      "The author mentions all of the following reasons to dismiss concerns about "
      "contaminating Mars EXCEPT:",
      [
          "Efforts to contain contamination on Mars are likely to be derailed as "
          "competitor countries may not follow similar restrictions.",
          "The use of similar probes on astronomical bodies like the moon have had little "
          "effect on the environment.",
          "The lack of evidence of living organisms on Mars makes possible contamination "
          "from earthly microbes a moot point.",
          "Earlier explorations have already contaminated pristine space environments.",
      ],
      "The use of similar probes on astronomical bodies like the moon have had little "
      "effect on the environment.",
      "The passage never assesses probes' environmental effect on the moon - it instead "
      "says NASA's past missions weren't sterile and drew \"little notice\", a point about "
      "public reaction, not environmental impact. Options 1, 3 and 4 are all stated "
      "directly (competitors ignoring rules, no evidence of Mars life, Apollo's litter).",
      passage=_MARS_PASSAGE),
    q(_g, "Reading Comprehension - planetary protection vs Mars exploration", "MCQ",
      "The author is unlikely to disagree with any of the following EXCEPT:",
      [
          "The exorbitant costs of continuing to keep the space environment pristine may be "
          "unsustainable.",
          "That while NASA's earlier missions were not ideal in their approach to space "
          "contamination, they likely did no grave damage.",
          "The proposal for a zonal segregation of the Martian landscape into regions for "
          "different purposes.",
          "Space contamination should be minimised until the possibility of life on the "
          "astronomical body being explored is ruled out.",
      ],
      "Space contamination should be minimised until the possibility of life on the "
      "astronomical body being explored is ruled out.",
      "The question asks which statement the author IS likely to disagree with (the one "
      "\"EXCEPT\" the author's general agreement). Options 1-3 all match positions the "
      "author endorses (costs are unsustainable, past missions were fine, zonal plan is a "
      "reasonable compromise). Option 4's precautionary standard is exactly the "
      "planetary-protection stance the whole passage argues against.",
      passage=_MARS_PASSAGE),
]

# ---- Q15: Sentence Insertion (return-to-office costs) ----
QUESTIONS.append(q(
    None, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph and "
    "decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: This reality is putting stress on employees who have to pay for transport, "
    "desk lunches, more childcare, clothing and that after-work socialisation – costs "
    "they haven't incurred for nearly two years.\n"
    "Paragraph: ___(1)___. Prices are rising at their fastest rate in 40 years, "
    "consequently, return-to-office-related costs have shot up – think petrol and "
    "food, for instance. ___(2)___. Yet wages haven't kept up with inflation – even "
    "despite the salary growth many workers have enjoyed during a favourable pandemic "
    "labour market. ___(3)___. This is especially jarring for workers who were able to "
    "save during remote work, when these expenditures weren't a factor. ___(4)___. In April "
    "2022, Umus, a London university lecturer, told BBC Worklife that they were spending "
    "nearly a quarter of what they made every day on return-to-work costs.",
    ["Option 3", "Option 2", "Option 4", "Option 1"],
    "Option 3",
    "The missing sentence names the specific costs (transport, lunches, childcare) that "
    "follow logically right after the wages-vs-inflation gap is raised, and right before the "
    "paragraph pivots to how \"especially jarring\" this is for remote-work savers - so it "
    "slots between those two ideas, at (3).",
))

_MOUTAI_PASSAGE = (
    "Moutai has been the global booze sensation of the decade. A bottle of its Flying Fairy "
    "which sold in the 1980s for the equivalent of a dollar now retails for $400. Moutai's "
    "listed shares have soared by almost 600% in the past five years, outpacing the likes "
    "of Amazon. . . . It does this while disregarding every Western marketing mantra. It is "
    "not global, has meagre digital sales and does not appeal to millennials. It scores "
    "pitifully on environmental, social and governance measures. In the Boy Scout world of "
    "Western business it would leave a bad taste, in more ways than one.\n\n"
    "Moutai owes its intoxicating success to three factors—not all of them easy to "
    "emulate. First, it profits from Chinese nationalism. Moutai is known as the "
    "“national liquor”. It was used to raise spirits and disinfect wounds in "
    "Mao's Long March. It was Premier Zhou Enlai's favourite tipple, shared with Richard "
    "Nixon in 1972. Its centuries-old craftsmanship—it is distilled eight times and "
    "stored for years in earthenware jars—is a source of national pride. It also "
    "claims to be hangover-proof, which would make it an invention to rival gunpowder....\n\n"
    "Second, it chose to serve China's super-rich rather than its middle class. Markets are "
    "littered with the corpses of firms that could not compete in the cut-throat battle for "
    "Chinese middle-class wallets. And the country's premium market is massive—at "
    "73m-strong, bigger than the population of France, notes Euan McLeish of Bernstein, an "
    "investment firm, and still less crowded with prestige brands than advanced economies. "
    "Moutai is to these well-heeled drinkers what vintage champagne is to the rest of the "
    "world.....\n\n"
    "Third, Moutai looks beyond affluent millennials and digital natives. The elderly and "
    "the middle-aged, it found, can be just as lucrative. Its biggest market now is (male) "
    "drinkers in their mid-30s. Many have no siblings, thanks to four decades of China's "
    "one-child policy—which also means their elderly parents can splash out on "
    "weddings and banquets. Moutai is often a guest of honour.\n\n"
    "Moutai has succeeded thanks to nationalism, elitism and ageism, in other words—not "
    "in spite of this unholy trinity. But it faces risks. The government is its largest "
    "shareholder—and a meddlesome one. It appears to want prices to remain stable. "
    "Exorbitantly priced booze is at odds with its professed socialist ideals. Yet minority "
    "investors—including many foreign funds—lament that Moutai's wholesale price "
    "is a third of what it sells for in shops. Raising it could boost the company's profits "
    "further. Instead, in what some see as a travesty of corporate governance, its majority "
    "owner has plans to set up its own sales channel.....\n\n"
    "In the long run, its biggest risk may be millennials. As they grow older, health "
    "concerns, work-life balance and the desire for more wholesome pursuits than "
    "binge-drinking may curb the “Ganbei!” toasting culture [heavy drinking] on "
    "which so much of the demand for Moutai rests. For the time being, though, the party "
    "goes on."
)
_g = "cat2024_varc_slot3_rc3"
QUESTIONS += [
    q(_g, "Reading Comprehension - Moutai's unconventional marketing success", "MCQ",
      "The phrase “would make it an invention to rival gunpowder” has been used "
      "in the passage in a sense that is",
      ["Synonymical.", "Metaphorical.", "Substantive.", "Literal."],
      "Metaphorical.",
      "Moutai being hangover-proof is obviously not actually comparable to gunpowder as an "
      "invention - the phrase borrows gunpowder's stature as a historic Chinese invention "
      "purely for rhetorical effect, which is the definition of a metaphorical (not literal, "
      "synonymous, or substantive) usage.",
      passage=_MOUTAI_PASSAGE),
    q(_g, "Reading Comprehension - Moutai's unconventional marketing success", "MCQ",
      "Which one of the following is both a reason for Moutai's success as well as a "
      "possible threat to that success?",
      [
          "Its appeal to the rich.",
          "Chinese love of liquor-filled celebration.",
          "Government involvement in its business.",
          "Its appeal to the older age group.",
      ],
      "Its appeal to the older age group.",
      "The passage credits older/middle-aged drinkers for current success but separately "
      "flags millennials ageing into health-consciousness as the \"biggest risk\" in the "
      "long run - the same demographic factor (age skew) is both the engine and the future "
      "threat. The other options are each discussed as only a success factor or only a "
      "risk, not both.",
      passage=_MOUTAI_PASSAGE),
    q(_g, "Reading Comprehension - Moutai's unconventional marketing success", "MCQ",
      "In the context of the passage, we can infer that to succeed in the liquor industry "
      "in China, a marketing firm must consider all of the following factors affecting the "
      "Chinese liquor market EXCEPT that",
      [
          "There are few competitors to meet the demands of high-end liquor consumers.",
          "There is money to be made from marketing to the middle class.",
          "The government may control the pricing of products.",
          "The competition for winning over the middle class is very stiff.",
      ],
      "There is money to be made from marketing to the middle class.",
      "The passage explicitly says Moutai succeeded by choosing the super-rich \"rather "
      "than its middle class\", since that market is a \"cut-throat battle\" littered with "
      "corpses of failed firms - the opposite of an easy money-maker. Options 1, 3 and 4 "
      "are each directly supported by the passage.",
      passage=_MOUTAI_PASSAGE),
    q(_g, "Reading Comprehension - Moutai's unconventional marketing success", "MCQ",
      "In the context of the passage, it is most likely that the author refers to Moutai's "
      "marketing strategy as “the unholy trinity” because",
      [
          "It exposes the firm to long-term risks.",
          "There is nothing holy about marketing techniques for liquor.",
          "It contradicts the Western strategy of marketing.",
          "It profits from Chinese nationalist feelings.",
      ],
      "It contradicts the Western strategy of marketing.",
      "\"Unholy\" plays off the passage's opening framing - Moutai succeeds by "
      "\"disregarding every Western marketing mantra\" and would \"leave a bad taste\" in "
      "the \"Boy Scout world of Western business\". The trinity (nationalism, elitism, "
      "ageism) is unholy specifically relative to that Western yardstick, not because of "
      "long-term risk (1, which is a separate later point) or liquor marketing generally (2).",
      passage=_MOUTAI_PASSAGE),
]

# ---- Q20: Sentence Insertion (Somalia drought) ----
QUESTIONS.append(q(
    None, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph and "
    "decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: Many have had to leave their homes behind, with more than 1.3 million people "
    "being displaced due to the drought.\n"
    "Passage: Somalia has been dealing with an enormous humanitarian catastrophe, driven by "
    "the longest and most severe drought the country has experienced in at least 40 years. "
    "___(1)___. Five consecutive rainy seasons have failed, causing more than 8 million "
    "people - almost half of the country's population – to experience acute food "
    "insecurity. ___(2)___. More than 43,000 people are believed to have lost their lives, "
    "with half of the lives lost likely being children under five. The damage the drought "
    "has caused is far-reaching. ___(3)___. Farmers have lost all their agricultural "
    "income, while pastoralists have lost more than 3 million livestock, impoverishing "
    "entire communities, and leaving them on the brink of famine. ___(4)___. Some, like the "
    "pastoralists, may never be able to go back as their livelihoods have been irreversibly "
    "wiped out.",
    ["Option 4", "Option 2", "Option 1", "Option 3"],
    "Option 4",
    "The sentence's \"leave their homes behind\" claim needs the agricultural/livestock "
    "losses already on the table to make sense as a consequence, and it must precede the "
    "closing line about pastoralists never going back - so it fits only at (4), right "
    "between the livelihood-loss sentence and that closing line.",
))

_LANG_PASSAGE = (
    "Languages become endangered and die out for many reasons. Sadly, the physical "
    "annihilation of communities of native speakers of a language is all too often the "
    "cause of language extinction. In North America, European colonists brought death and "
    "destruction to many Native American communities. This was followed by US federal "
    "policies restricting the use of indigenous languages, including the removal of native "
    "children from their communities to federal boarding schools where native languages and "
    "cultural practices were prohibited. As many as 75 percent of the languages spoken in "
    "the territories that became the United States have gone extinct, with slightly better "
    "language survival rates in Central and South America . . .\n\n"
    "Even without physical annihilation and prohibitions against language use, the language "
    "of the “dominant” cultures may drive other languages into extinction; young "
    "people see education, jobs, culture and technology associated with the dominant "
    "language and focus their attention on that language. The largest language "
    "“killers” are English, Spanish, Portuguese, French, Russian, Hindi, and "
    "Chinese, all of which have privileged status as dominant languages threatening "
    "minority languages.\n\n"
    "When we lose a language, we lose the worldview, culture and knowledge of the people "
    "who spoke it, constituting a loss to all humanity. People around the world live in "
    "direct contact with their native environment, their habitat. When the language they "
    "speak goes extinct, the rest of humanity loses their knowledge of that environment, "
    "their wisdom about the relationship between local plants and illness, their "
    "philosophical and religious beliefs as well as their native cultural expression (in "
    "music, visual art and poetry) that has enriched both the speakers of that language and "
    "others who would have encountered that culture. . . .\n\n"
    "As educators deeply immersed in the liberal arts, we believe that educating students "
    "broadly in all facets of language and culture . . . yields immense rewards. Some "
    "individuals educated in the liberal arts tradition will pursue advanced study in "
    "linguistics and become actively engaged in language preservation, setting out for the "
    "Amazon, for example, with video recording equipment to interview the last surviving "
    "elders in a community to record and document a language spoken by no children.\n\n"
    "Certainly, though, the vast majority of students will not pursue this kind of "
    "activity. For these students, a liberal arts education is absolutely critical from the "
    "twin perspectives of language extinction and global citizenship. When students study "
    "languages other than their own, they are sensitized to the existence of different "
    "cultural perspectives and practices. With such an education, students are more likely "
    "to be able to articulate insights into their own cultural biases, be more empathetic to "
    "individuals of other cultures, communicate successfully across linguistic and cultural "
    "differences, consider and resolve questions in a way that reflects multiple cultural "
    "perspectives, and, ultimately extend support to people, programs, practices, and "
    "policies that support the preservation of endangered languages.\n\n"
    "There is ample evidence that such preservation can work in languages spiraling toward "
    "extinction. For example, Navajo, Cree and Inuit communities have established schools "
    "in which these languages are the language of instruction and the number of speakers of "
    "each has increased."
)
_g = "cat2024_varc_slot3_rc4"
QUESTIONS += [
    q(_g, "Reading Comprehension - language extinction and liberal arts education", "MCQ",
      "It can be inferred from the passage that it is likely South America had a slightly "
      "better language survival rate than North America for all of the following reasons "
      "EXCEPT:",
      [
          "The colonial government was unable to mainstream the locals.",
          "Locals were provided job opportunities in the colonial administration.",
          "European colonists allowed children of native speakers to stay at home with "
          "their families.",
          "Not many native speakers were killed by European colonists.",
      ],
      "Locals were provided job opportunities in the colonial administration.",
      "The passage's reasons for language survival are all about avoiding "
      "annihilation/suppression (fewer killings, no forced removal of children, weaker "
      "colonial control) - nothing about colonial-administration jobs is mentioned "
      "anywhere, making it the invented, unsupported option.",
      passage=_LANG_PASSAGE),
    q(_g, "Reading Comprehension - language extinction and liberal arts education", "MCQ",
      "The author believes that a liberal arts education combined with participation in "
      "language preservation empowers students in all of the following ways EXCEPT that "
      "they will",
      [
          "Overcome cultural barriers to communication.",
          "Establish schools to preserve languages spiralling towards extinction.",
          "Learn different languages.",
          "Develop a better understanding of their own culture.",
      ],
      "Establish schools to preserve languages spiralling towards extinction.",
      "The passage explicitly says the \"vast majority of students will not pursue this "
      "kind of activity\" (fieldwork/preservation work like founding schools) - that's "
      "reserved for the few who go into linguistics. The broader empowerment the author "
      "describes for most students is cultural empathy, language learning, and "
      "self-awareness (options 1, 3, 4), not founding preservation schools themselves.",
      passage=_LANG_PASSAGE),
    q(_g, "Reading Comprehension - language extinction and liberal arts education", "MCQ",
      "In the context of the passage, which one of the following hypothetical scenarios, "
      "if true, is NOT an example of the kind of loss that occurs when a language becomes "
      "extinct?",
      [
          "The Andamanese language has a word to describe someone who has lost a "
          "step-sister. When the language dies, we will lose the concept of the word and "
          "the emotions it evokes.",
          "The Lamkangs of Manipur have only 3 remaining native speakers of the language. "
          "When they die, we will lose one more group from the government list of "
          "indigenous tribes.",
          "The Inuits of Alaska have 35 different words to describe the texture of snow. "
          "When the language becomes extinct, we will lose that understanding of nature.",
          "The Nicobarese language describes 20 different moods of the ocean. By the time "
          "the last speaker is educated in a Central Board school, they will have forgotten "
          "their language.",
      ],
      "The Lamkangs of Manipur have only 3 remaining native speakers of the language. When "
      "they die, we will lose one more group from the government list of indigenous tribes.",
      "The passage's notion of loss is cultural/conceptual/environmental knowledge "
      "(worldview, wisdom about nature, cultural expression) - options 1, 3 and 4 each lose "
      "exactly that kind of knowledge. Losing an entry on a \"government list of indigenous "
      "tribes\" is a bureaucratic bookkeeping loss, not the knowledge-loss the passage "
      "describes.",
      passage=_LANG_PASSAGE),
    q(_g, "Reading Comprehension - language extinction and liberal arts education", "MCQ",
      "Which one of the following hypothetical scenarios, if true, would most strongly "
      "undermine the central ideas of the passage?",
      [
          "Schools that teach endangered languages can preserve the language only for a "
          "generation.",
          "Most liberal arts students will pursue jobs in publishing and human resource "
          "management rather than doctorates in linguistics.",
          "Recording a dying language that has only a few remaining speakers freezes it in "
          "time: it stops evolving further.",
          "A liberal arts education requires that, in addition to being fluent in English, "
          "students gain fluency in two of the top five most spoken languages globally.",
      ],
      "A liberal arts education requires that, in addition to being fluent in English, "
      "students gain fluency in two of the top five most spoken languages globally.",
      "The passage's whole argument is that liberal arts education should expose students "
      "to languages, including endangered minority ones, to build empathy and support "
      "preservation. A requirement to instead learn more of the dominant \"language "
      "killers\" (Spanish, Hindi, Chinese, etc.) directly inverts that goal. Options 1-3 are "
      "mild caveats consistent with, not contradictory to, the passage's case.",
      passage=_LANG_PASSAGE),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        added = 0
        skipped = 0
        for item in QUESTIONS:
            exists = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.section == "VARC",
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.question_text == item["question_text"],
                )
                .first()
            )
            if exists is not None:
                print(f"Already present as id={exists.id}, skipping.")
                skipped += 1
                continue
            db.add(CatQuestion(is_active=True, **item))
            added += 1
        db.commit()
        print(f"Added {added} CAT 2024 VARC Slot 3 questions ({skipped} already present).")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

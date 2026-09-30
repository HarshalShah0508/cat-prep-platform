"""Seed real CAT 2025 VARC questions, all 3 slots, retyped from the official
question papers in pyq-source/2025/. Reading-comprehension questions are
grouped by shared passage via `group_id` + `passage_text`, same convention
as the DILR sets; standalone VA questions (para-jumbles, sentence-insertion,
odd-sentence-out, single-paragraph summary questions) get `group_id=None`.

`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

Source note: the plain question-paper PDFs (VARC_SLOTn_CAT_2025.pdf) were
used as the primary source. Two real gaps were found and fixed by reading
the matching combined SOLUTIONS PDF instead:
  - Slot 1 Q7 and Q8 (sentence-insertion): the plain paper's PDF text layer
    had a font/kerning bug that ran the paragraph text together with no
    spaces at all (unreadable). Recovered cleanly from the solutions PDF.
  - Slot 1 Q9-12 and Q20-23 (two RC sets): the plain paper's question paper
    genuinely omits the underlying passage text before the questions (a
    real gap in that PDF, not an extraction artifact). Recovered from the
    solutions PDF, which embeds the full passage.
Slots 2 and 3 extracted cleanly from the plain papers with no issues.

Run with:
    python -m app.scripts.seed_cat_pyq_2025_varc
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025


def q(group_id, slot, topic, qtype, text, options=None, passage=None):
    return {
        "section": "VARC",
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

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled sentences (labelled 1, 2, 3, 4, and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence out and key in the number of that sentence as your answer.\n"
    "1. Developments both technological and sociocultural have afforded us far greater "
    "freedom over death than we had in the past, and while we are still adapting ourselves "
    "to that freedom, we now appreciate the moral importance of this freedom.\n"
    "2. But I believe that a type of freedom we can call freedom over death - that is, a "
    "freedom in which we shape the timing and circumstances of how we die - should be "
    "central to this conversation.\n"
    "3. Legalising assisted dying is but a further step in realising this freedom over "
    "death.\n"
    "4. Many people endorse, through their opinions or their choices, our freedom over "
    "death encompassing a right to medical assistance in hastening our deaths.\n"
    "5. Freedom is a notoriously complex and contested philosophical notion, and I won't "
    "pretend to settle any of the big controversies it raises."))

_g = "cat2025_varc_slot1_rc1"
_p = (
    "Often the well intentioned music lover or the traditionally-minded professional "
    "composer asks two basic questions when faced with the electronic music phenomena: "
    "(1) . . . is this type of artistic creation music at all? and, (2) given that the "
    "product is accepted as music of a new type or order, is not such music \"inhuman\"? "
    ". . . As Lejaren Hiller points out in his book Experimental Music (co-author Leonard "
    "M. Isaacson), two questions which often arise when music is discussed are: (a) the "
    "substance of musical communication and its symbolic and semantic significance, if "
    "any, and (b) the particular processes, both mental and technical, which are involved "
    "in creating and responding to musical composition. The ever-present popular concept "
    "of music as a direct, open, emotional expression and as a subjective form of "
    "communication from the composer, is, of course still that of the nineteenth century, "
    "when composers themselves spoke of music in those terms . . . But since the third "
    "decade of our century many composers have preferred more objective definitions of "
    "music, epitomized in Stravinsky's description of it as \"a form of speculation in "
    "terms of sound and time\". An acceptance of this more characteristic twentieth-"
    "century view of the art of musical composition will of course immediately bring the "
    "layman closer to an understanding of, and sympathetic response to, electronic music, "
    "even if the forms, sounds and approaches it uses will still be of a foreign nature to "
    "him.\n\n"
    "A communication problem however will still remain. The principal barrier that "
    "electronic music presents at large, in relation to the communication process, is that "
    "composers in this medium are employing a new language of forms . . . where terms like "
    "'densities', 'indefinite pitch relations', 'dynamic serialization', 'permutation', "
    "etc., are substitutes (or remote equivalents) for the traditional concepts of "
    "harmony, melody, rhythm, etc. . . . When the new structural procedures of electronic "
    "music are at last fully understood by the listener the barriers between him and the "
    "work he faces will be removed. . . .\n\n"
    "The medium of electronic music has of course tempted many kinds of composers to try "
    "their hand at it . . . But the serious-minded composer approaches the world of "
    "electronic music with a more sophisticated and profound concept of creation. Although "
    "he knows that he can reproduce and employ melodic, rhythmic patterns and timbres of a "
    "traditional nature, he feels that it is in the exploration of sui generis languages "
    "and forms that the aesthetic magic of the new medium lies. And, conscientiously, he "
    "plunges into this search.\n\n"
    "The second objection usually levelled against electronic music is much more innocent "
    "in nature. When people speak-sometimes very vehemently-of the 'inhuman' quality of "
    "this music they seem to forget that the composer is the one who fires the machines, "
    "collects the sounds, manipulates them, pushes the buttons, programs the computer, "
    "filters the sounds, establishes pitches and scales, splices tape, thinks of forms, "
    "and rounds up the over-all structure of the piece, as well as every detail of it."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Electronic Music", "MCQ",
      "The goal of the author over the course of this passage is to:",
      ["differentiate the modern composer from the nineteenth century composer.",
       "differentiate between electronic music and other forms of music.",
       "defend the \"serious-minded composer\" from Lejaren Hill and Stravinsky.",
       "defend electronic music from certain common charges."], _p),
    q(_g, _slot, "Reading Comprehension - Electronic Music", "MCQ",
      "What relation does the \"communication problem\" mentioned in paragraph 2 have to "
      "the questions that the author recounts at the beginning of the passage?",
      ["Unfamiliar forms and terms might get in the way of our seeing electronic music as "
       "music, but this can be overcome.",
       "Its unfamiliar \"language of forms\" and novel terms mean that we cannot see "
       "electronic music as music since it does not employ traditional musical concepts.",
       "None; they are unrelated to one another and form parts of different discussions.",
       "The communication problem is what allows us to see electronic music as music "
       "because music must be difficult to understand."], _p),
    q(_g, _slot, "Reading Comprehension - Electronic Music", "MCQ",
      "The mention of Stravinsky's description of music in the first paragraph does all "
      "the following EXCEPT:",
      ["help us determine which sounds are musical and which are not.",
       "respond to and expand upon earlier understandings of music.",
       "complicate our notion of what is communicated through music.",
       "allow us to classify electronic music as music."], _p),
    q(_g, _slot, "Reading Comprehension - Electronic Music", "MCQ",
      "From the context in which it is placed, the phrase \"sui generis\" in paragraph 3 "
      "suggests which one of the following?",
      ["Particular", "Generic", "Unaesthetic", "Indescribable"], _p),
]

QUESTIONS.append(q(None, _slot, "Sentence Sequencing", "TITA",
    "The four sentences (labelled 1, 2, 3, and 4) given below, when properly sequenced, "
    "would yield a coherent paragraph. Decide on the proper sequencing of the four "
    "sentences and key in the sequence of the four numbers as your answer.\n"
    "1. It can in fact be integrated into any function (education, medical treatment, "
    "production, punishment); it can increase the effect of this function, by being linked "
    "closely with it; it can constitute a mixed mechanism in which relations of power (and "
    "of knowledge) may be precisely adjusted, in the smallest detail, to the processes "
    "that are to be supervised; it can establish a direct proportion between 'surplus "
    "power' and 'surplus production'.\n"
    "2. It's a case of 'it's easy once you've thought of it' in the political sphere.\n"
    "3. The panoptic mechanism is not simply a hinge, a point of exchange between a "
    "mechanism of power and a function; it is a way of making power relations function in "
    "a function, and of making a function function through these power relations.\n"
    "4. In short, it arranges things in such a way that the exercise of power is not "
    "added on from the outside, like a rigid, heavy constraint, to the functions it "
    "invests, but is so subtly present in them as to increase their efficiency by itself "
    "increasing its own points of contact."))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "The given sentence is missing in the paragraph below. Decide where it best fits "
    "among the options 1, 2, 3, or 4 indicated in the paragraph.\n"
    "Sentence: \"Everything is old-world, traditional techniques from Mexico,\" Ava "
    "emphasizes.\n\n"
    "Paragraph: The sisters embrace the ways their great-grandfather built and repaired "
    "instruments. ____(1)____. When crafting a Mexican guitarrón used in mariachi music, "
    "they use tacote wood for the top of the instrument. Once the wood is cut, they carve "
    "the neck and heel from a single block using tools like hand saws, chisels and "
    "sandpaper rather than modern power tools - and believe that this traditional method "
    "improves the tone of the instrument. ____(2)____.\n"
    "Their store has a three-year waitlist for instruments that take months to create. "
    "____(3)____.\n"
    "The family's artisanship has attracted stars like Los Lobos, who own custom guitars "
    "made by all three generations of the Delgado family. ____(4)____.\n"
    "For the sisters, involvement in the family business started at an early age. They "
    "each built their first instruments at age 9.",
    ["Option 1", "Option 4", "Option 2", "Option 3"]))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "The given sentence is missing in the paragraph below. Decide where it best fits "
    "among the options 1, 2, 3, or 4 indicated in the paragraph.\n"
    "Sentence: Historically, silver has been, and still is, an important element in the "
    "business of 'show' visible in private houses, churches, government and diplomacy.\n\n"
    "Paragraph: ____(1)____. Timothy Schroder put it succinctly in suggesting that "
    "electric light and eating in the kitchen eroded this need. As he explained to the "
    "author, 'Silver, when illuminated by flickering candlelight, comes alive and almost "
    "dances before the eyes, but when lit by electric light it becomes flat and dead.' "
    "____(2)____. Domestic and economic changes may have worked against the market, but "
    "the London silver trade remained buoyant, thanks to the competition of collectors "
    "seeking grand display silver at the top end, and the buyers of 'collectables', like "
    "spoons and wine labels and 'novelties', at the bottom. ____(3)____. Another factor "
    "that came into play was the systematic collection building of certain American "
    "museums over the period. Boston, Huntington Art Gallery and Williamsburg, among "
    "others, were largely supplied by London dealers. ____(4)____.",
    ["Option 4", "Option 1", "Option 3", "Option 2"]))

_g = "cat2025_varc_slot1_rc2"
_p = (
    "Understanding the key properties of complex systems can help us clarify and deal "
    "with many new and existing global challenges, from pandemics to poverty . . . A "
    "recent study in Nature Physics found transitions to orderly states such as schooling "
    "in fish (all fish swimming in the same direction), can be caused, paradoxically, by "
    "randomness, or 'noise' feeding back on itself. That is, a misalignment among the fish "
    "causes further misalignment, eventually inducing a transition to schooling. Most of "
    "us wouldn't guess that noise can produce predictable behaviour. The result invites us "
    "to consider how technology such as contact-tracing apps, although informing us "
    "locally, might negatively impact our collective movement. If each of us changes our "
    "behaviour to avoid the infected, we might generate a collective pattern we had aimed "
    "to avoid - higher levels of interaction between the infected and susceptible, or "
    "high levels of interaction among the asymptomatic.\n\n"
    "Complex systems also suffer from a special vulnerability to events that don't follow "
    "a normal distribution or 'bell curve'. When events are distributed normally, most "
    "outcomes are familiar and don't seem particularly striking. Height is a good example: "
    "it's pretty unusual for a man to be over 7 feet tall; most adults are between 5 and 6 "
    "feet, and there is no known person over 9 feet tall. But in collective settings where "
    "contagion shapes behaviour - a run on the banks, a scramble to buy toilet paper - the "
    "probability distributions for possible events are often heavy-tailed. There is a much "
    "higher probability of extreme events, such as a stock market crash or a massive surge "
    "in infections. These events are still unlikely, but they occur more frequently and "
    "are larger than would be expected under normal distributions.\n\n"
    "What's more, once a rare but hugely significant 'tail' event takes place, this raises "
    "the probability of further tail events. We might call them second-order tail events; "
    "they include stock market gyrations after a big fall and earthquake aftershocks. The "
    "initial probability of second-order tail events is so tiny it's almost impossible to "
    "calculate - but once a first-order tail event occurs, the rules change, and the "
    "probability of a second-order tail event increases.\n\n"
    "The dynamics of tail events are complicated by the fact that they result from "
    "cascades of other unlikely events. When COVID-19 first struck, the stock market "
    "suffered stunning losses followed by an equally stunning recovery. Some of these "
    "dynamics are potentially attributable to former sports bettors, with no sports to bet "
    "on, entering the market as speculators rather than investors. The arrival of these "
    "new players might have increased inefficiencies and allowed savvy long-term investors "
    "to gain an edge over bettors with different goals. . . .\n\n"
    "One reason a first-order tail event can induce further tail events is that it changes "
    "the perceived costs of our actions and changes the rules that we play by. This "
    "game-change is an example of another key complex systems concept: nonstationarity. A "
    "second, canonical example of nonstationarity is adaptation, as illustrated by the "
    "arms race involved in the coevolution of hosts and parasites [in which] each has to "
    "'run' faster, just to keep up with the novel solutions the other one presents as "
    "they battle it out in evolutionary time."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Complex Systems", "MCQ",
      "All of the following inferences are supported by the passage EXCEPT that:",
      ["examples like runs on banks and toilet paper scrambles illustrate how contagion "
       "can amplify local choices into system-wide cascades that surprise participants "
       "and lead to patterns they did not intend to create.",
       "learning can change the rules that actors face. So, a rare shock can alter "
       "payoffs and raise the odds of subsequent large disturbances within the same "
       "system, which supports the idea of second-order tail events.",
       "heavy-tailed events make extreme outcomes more frequent and larger than bell "
       "curve expectations. This complicates forecasting and risk management in "
       "collective settings shaped by contagion and copying behaviour.",
       "the text attributes the COVID-19 pandemic rebound in financial markets solely to "
       "displaced sports bettors and treats their entry as the overriding cause of the "
       "rapid recovery across assets and time horizons."], _p),
    q(_g, _slot, "Reading Comprehension - Complex Systems", "MCQ",
      "Which one of the options below best summarises the passage?",
      ["The passage explains how social outcomes generally follow normal distributions. "
       "So, extreme events are negligible, and policy should stabilise averages rather "
       "than learn from large shocks in fast-changing collective settings.",
       "The passage explains how noise can create order, then shows why complex systems "
       "with contagion are vulnerable to heavy-tailed cascades. It also explains why "
       "early shocks change rules through nonstationarity with a market illustration "
       "during the COVID-19 disruption.",
       "The passage explains how speculative entrants always produce inefficiency after "
       "health shocks. Therefore, long-term investors invariably profit when new "
       "participants push prices away from fundamentals under pandemic conditions and "
       "comparable crises.",
       "The passage explains how nonstationarity works in evolutionary biology and "
       "rejects applications in markets or public health because adaptation is exclusive "
       "to parasite-host systems and cannot arise in technology-mediated social "
       "dynamics."], _p),
    q(_g, _slot, "Reading Comprehension - Complex Systems", "MCQ",
      "Which one of the following observations would most strengthen the passage's claim "
      "that a first-order tail event raises the probability of further tail events in "
      "complex systems?",
      ["In epidemic networks, initial super-spreading episodes are isolated spikes after "
       "which outbreak sizes match the baseline distribution from independent contact "
       "models across comparable cities with no rise in the frequency or size of later "
       "extreme clusters.",
       "River discharge records show water levels fit a normal distribution with thin "
       "tails that match laboratory data, regardless of storms or floods.",
       "After a major equity crash, researchers find dense clusters of large daily moves "
       "for several weeks, with extreme days occurring far more often than in normal "
       "circumstances for assets with customarily low volatility profiles.",
       "Following large earthquakes, regional seismic activity returns to baseline "
       "within hours with no aftershock sequence once data are adjusted for reporting "
       "effects, which suggests independence across events rather than any elevation in "
       "subsequent tail probabilities."], _p),
    q(_g, _slot, "Reading Comprehension - Complex Systems", "MCQ",
      "The passage suggests that contact-tracing apps could inadvertently raise risky "
      "interactions by altering local behaviour. Which one of the assumptions below is "
      "most necessary for that suggestion to hold?",
      ["Most users uninstall apps within a week, which leaves only highly exposed "
       "individuals participating. This neutralises any systematic bias in routing "
       "decisions and prevents any predictable change in aggregate contact patterns.",
       "Individuals base movement choices partly on observed infections and on the "
       "behaviour of others. So, local responses interact, which turns many small "
       "adjustments into large scale patterns that can frustrate the intended aim of "
       "risk reduction.",
       "App alerts always include precise location to within one metre and deliver real "
       "time updates for all users, which ensures that the data feed is perfectly "
       "accurate regardless of privacy settings, power limits, or network conditions.",
       "Urban networks have uniform traffic conditions at all hours, which allows "
       "perfectly predictable routing independent of personal choices, social signals, "
       "or crowd reactions and, therefore, makes interdependence negligible in city "
       "movement decisions."], _p),
]

QUESTIONS.append(q(None, _slot, "Sentence Sequencing", "TITA",
    "The four sentences (labelled 1, 2, 3, and 4) given below, when properly sequenced, "
    "would yield a coherent paragraph. Decide on the proper sequencing of the order of "
    "the sentences and key in the sequence of the four numbers as your answer.\n"
    "1. But man, woman or otherwise, there is no denying that the quality of our life and "
    "character will be significantly shaped by the way we handle our anger.\n"
    "2. Once the taboos have been broken, women usually experience letting their fists "
    "fly as intensely liberating.\n"
    "3. Though this might seem a stereotype, women-unlike men, who are frequently "
    "applauded for unbridled aggression-are often socialized to keep a lid on their ire.\n"
    "4. Many of them are so at odds with their aggressive feelings that, as a coach, I "
    "often have to stop them from pulling their punches and encourage them to extend "
    "their arms so their blows might actually reach their fleshy target."))

QUESTIONS.append(q(None, _slot, "RC Summary", "MCQ",
    "The passage given below is followed by four summaries. Choose the option that best "
    "captures the essence of the passage.\n"
    "Zombie cells may contribute to age-related chronic inflammation: this finding could "
    "help scientists understand more about the aging process and why the immune system "
    "becomes less effective as we get older. Zombie or \"senescent\" cells are damaged "
    "cells that can no longer divide and grow like normal cells. Scientists think that "
    "these cells can contribute to chronic health problems when they accumulate in the "
    "body. In younger people, the immune system is more effective at clearing senescent "
    "cells from the body through a process called apoptosis, but as we age this process "
    "becomes less efficient. As a result, there is an accumulation of senescent cells in "
    "different organs in the body, either through increased production or reduced "
    "clearance by the immune system. The zombie cells continue to use energy though they "
    "do not divide, and often secrete chemicals that cause inflammation, which if "
    "persistent for longer periods of time can damage healthy cells leading to chronic "
    "diseases.",
    ["Senescent \"zombie\" cells are inactive or malfunctioning cells that can be found "
     "throughout the body.",
     "A younger person's immune system is healthy and is able to clear the damaged "
     "cells, but as people age, the zombie cells resist apoptosis, and start "
     "accumulating in the body.",
     "Aging leads to less effective apoptosis, and therefore zombie cells start to "
     "accumulate in the body, causing inflammation, which accelerates aging and leads to "
     "chronic diseases.",
     "Dead cells accelerate chronic inflammation weakening the immune system and lead to "
     "aging."]))

_g = "cat2025_varc_slot1_rc3"
_p = (
    "How can we know what someone else is thinking or feeling, let alone prove it in "
    "court? In his 1863 book, A General View of the Criminal Law of England, James "
    "Fitzjames Stephen, among the most celebrated legal thinkers of his generation, was of "
    "the opinion that the assessment of a person's mental state was an inference made with "
    "\"little consciousness.\" In a criminal case, jurors, doctors, and lawyers could watch "
    "defendants-scrutinizing clothing, mannerisms, tone of voice-but the best they could "
    "hope for were clues. . . . Rounding these clues up to a judgment about a defendant's "
    "guilt, or a defendant's life, was an act of empathy and imagination. . . . The closer "
    "the resemblance between defendants and their judges, the easier it was to overlook "
    "the gap that inference filled. Conversely, when a defendant struck officials as "
    "unlike themselves, whether by dint of disease, gender, confession, or race, the "
    "precariousness of judgments about mental state was exposed. In the nineteenth "
    "century, physicians who specialized in the study of madness and the care of the "
    "insane held themselves out as experts in the new field of mental science. Often "
    "called alienists or mad doctors, they were the predecessors of modern psychiatrists, "
    "neurologists, and psychologists. . . . The opinions of family and neighbors had once "
    "been sufficient to sift the sane from the insane, but a growing belief that insanity "
    "was a subtle condition that required expert, medical diagnosis pushed physicians "
    "into the witness box. . . . Lawyers for both prosecution and defense began to recruit "
    "alienists to assess defendants' sanity and to testify to it in court.\n\n"
    "Irresponsibility and insanity were not identical, however. Criminal responsibility "
    "was a legal concept and not, fundamentally, a medical one. Stephen explained: \"The "
    "question 'What are the mental elements of responsibility?' is, and must be, a legal "
    "question. It cannot be anything else, for the meaning of responsibility is liability "
    "to punishment.\" . . . Nonetheless, medical and legal accounts of what it meant to be "
    "mentally sound became entangled and mutually referential throughout the nineteenth "
    "century. Lawyers relied on medical knowledge to inform their opinions and arguments "
    "about the sanity of their clients. Doctors commented on the legal responsibility of "
    "their patients. Ultimately, the fields of criminal law and mental science were both "
    "invested in constructing an image of the broken and damaged psyche that could be "
    "contrasted with the whole and healthy one. This shared interest, and the shared "
    "space of the criminal courtroom, made it nearly impossible to consider "
    "responsibility without medicine, or insanity without law. . . .\n\n"
    "Physicians and lawyers shared more than just concern for the mind. Class, race, and "
    "gender bound these middle-class, white, professional men together, as did family "
    "ties, patriotism, Protestantism, business ventures, the alumni networks of elite "
    "schools and universities, and structures of political patronage. But for all their "
    "affinities, men of medicine and law were divided by contests over the borders of "
    "criminal responsibility, as much within each profession as between them. Alienists "
    "steadily pushed the boundaries of their field, developing increasingly complex and "
    "capacious definitions of insanity. Eccentricity and aggression came to be classified "
    "as symptoms of mental disease, at least by some."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Alienists & Criminal Law", "MCQ",
      "The last paragraph of the passage refers to \"middle-class, white, professional "
      "men\". Which one of the following qualities best describes the connection among "
      "them?",
      ["The borders of criminal responsibility.", "The opinions of family and "
       "neighbours.", "Eccentricity and aggression.", "Empathy and imagination."], _p),
    q(_g, _slot, "Reading Comprehension - Alienists & Criminal Law", "MCQ",
      "According to the passage, who or what was an \"alienist\"?",
      ["Professionals who pushed the boundaries of their fields till they became "
       "unrecognisable in the nineteenth century.",
       "Physicians who specialised in the study of madness and the care of the insane in "
       "the nineteenth century.",
       "Physicians and lawyers who were responsible for the condition of immigrants or "
       "'aliens' in the nineteenth century.",
       "Physicians and lawyers who were responsible for examining accounts of "
       "extraterrestrials or 'aliens' in the nineteenth century."], _p),
    q(_g, _slot, "Reading Comprehension - Alienists & Criminal Law", "MCQ",
      "Study the following sets of concepts and identify the set that is conceptually "
      "closest to the concerns and arguments of the passage.",
      ["Empathy, Prosecution, Knowledge, Business.", "Judgement, Belief, Accounts, "
       "Patronage.", "Assessment, Empathy, Prosecution, Patriotism.",
       "Judgement, Insanity, Punishment, Responsibility."], _p),
    q(_g, _slot, "Reading Comprehension - Alienists & Criminal Law", "MCQ",
      "\"Conversely, when a defendant struck officials as unlike themselves, whether by "
      "dint of disease, gender, confession, or race, the precariousness of judgments "
      "about mental state was exposed.\" Which one of the following best describes the "
      "use of the word \"confession\" in this sentence?",
      ["Referring to the practice of 'confession' in some faiths, here it is a metaphor "
       "for the religion of the defendant.",
       "Referring to the gender, race or disease claimed as a defence by the defendant, "
       "here it is a synonym for 'professing' a gender, race, or disease.",
       "Referring to the defendant's confession of his or her crime as false, because "
       "'dint' is an archaic form of 'didn't' or 'did not'.",
       "The defendants struck out at the officials and then confessed to the act."], _p),
]

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled sentences (labelled 1, 2, 3, 4, and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence out and key in the number of that sentence as your answer.\n"
    "1. The Bayeux tapestry was, therefore, an obvious way to tell people about the "
    "downfall of the English and the rise of the Normans.\n"
    "2. So if we take expert in Anglo-Saxon culture Gale Owen-Crocker's idea that the "
    "tapestry was originally hung in a square with certain scenes facing each other, "
    "people would have stood in the centre.\n"
    "3. Art historian Linda Neagley has argued that pre-Renaissance people interacted "
    "with art visually, kinaesthetically (sensory perception through bodily movement) and "
    "physically.\n"
    "4. That would make it an 11th-century immersive space with scenes corresponding and "
    "echoing each other, drawing the viewer's attention, playing on their senses and "
    "understanding of the story they thought they knew.\n"
    "5. The Bayeux tapestry would have been hung at eye level to enable this."))

_g = "cat2025_varc_slot1_rc4"
_p = (
    "Studies showing that income inequality plays a positive role in economic growth are "
    "largely based on three arguments. The first argument focuses on investment "
    "indivisibilities wherein large sunk costs are required when implementing new "
    "fundamental innovations. Without stock markets and financial institutions to "
    "mobilize large sums of money, a high concentration of wealth is needed for "
    "individuals to undertake new industrial activities accompanied by high sunk costs.\n\n"
    "One study shows the relation between economic growth and income inequality for 45 "
    "countries during 1966-1995. (It was found) that the increase in income inequality "
    "has a significant positive relationship with economic growth in the short and medium "
    "term. Using system GMM, another study estimated the relation between income "
    "inequality and economic growth for 106 countries during 1965-2005 period. The "
    "results show that income inequality has a positive impact on economic growth in the "
    "short run, but a two or more negatively correlated in the long run. The second "
    "argument is related to moral hazard and incentives. Because economic performance is "
    "determined by the unobservable level of effort that agents make, paying "
    "compensations without taking into account the economic performance achieved would "
    "reduce the overall optimum effort from the agents. Thus, certain income inequalities "
    "contribute to growth by enhancing worker motivation and by giving motivation to "
    "innovators and entrepreneurs. Finally, some points out that the concentration of "
    "wealth or stock ownership in relation to corporate governance contributes to growth. "
    "If stock ownership is distributed and owned by a large number of shareholders, it is "
    "not easy to make quick decisions due to the conflicting interests among shareholders, "
    "and this may also cause a free-rider problem in terms of monitoring and supervising "
    "managers and workers.\n\n"
    "Various studies have examined the relationships between income inequality and "
    "economic growth, and most of these assert that a negative correlation exists between "
    "the two. Analyzing 159 countries for 1980-2012, they conclude that there exists a "
    "negative relation between income inequality and economic growth; when the income "
    "share of the richest 20% of population increases by 1%, the GDP decreases by 0.8%; "
    "whereas when the income share of the poorest 20% of population increases by 1%, the "
    "GDP increases by 0.38%. Some studies find that inequality has a negative impact on "
    "growth due to poor human capital accumulation and low fertility rates, while others "
    "point out that inequality creates political instability, resulting in lower "
    "investment. Some economists argue that widening income inequality has a negative "
    "impact on economic growth because it negatively affects social consensus or social "
    "capital formation.\n\n"
    "One important research topic is the correlation between democratization and income "
    "redistribution. Some scholars explain that social pressure for income redistribution "
    "rises as income inequality increases in a democratic society. In other words, "
    "democratization extends suffrage to wider class of people; the increased political "
    "power of low- and middle-income voters results in broader support for income "
    "redistribution and social welfare expansion. However, if the rich have more "
    "political influence than the poor, the democratic system actually worsens income "
    "inequality rather than improving it."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Income Inequality & Growth", "MCQ",
      "Which one of the options below best summarises the passage?",
      ["The passage claims that evaluating the effect of income inequality on economic "
       "growth without considering both short- and long- term consequences is misguided.",
       "The passage confines its discussion to financing gaps and corporate control "
       "while undercutting cross-country evidence and overlooking the significance of "
       "concerns regarding human capital accumulation, fertility rates, and income "
       "redistribution under democratisation.",
       "The passage argues that income inequality accelerates economic growth while "
       "also emphasising the significance of concerns regarding human capital "
       "accumulation, fertility rates, and political instability.",
       "The passage outlines investment, incentive, and governance channels through "
       "which income inequality may support economic growth and reports short-term "
       "gains while noting long-term drawbacks."], _p),
    q(_g, _slot, "Reading Comprehension - Income Inequality & Growth", "MCQ",
      "The passage refers to \"democratization\". Choose the one option below that comes "
      "closest to the opposite of this process.",
      ["After the emergency decree, the regime shifted toward authoritarianism as "
       "suffrage narrowed and opposition parties were deregistered.",
       "Corporate donations were capped and parties received public funding which was "
       "portrayed as establishing an oligarchy.",
       "Municipalities adopted participatory budgeting and recall elections which a "
       "press release called totalitarianism.",
       "The coalition imposed term limits and strengthened judicial review in order to "
       "further entrench autocratic rule."], _p),
    q(_g, _slot, "Reading Comprehension - Income Inequality & Growth", "MCQ",
      "The primary function of the three-part case for a positive income "
      "inequality-economic growth link in the first half of the passage is to show that:",
      ["inequality boosts growth in every period and type of economy, regardless of "
       "finance or governance conditions.",
       "mature stock markets make wealth concentration unnecessary, yet they might still "
       "be harmful to investment.",
       "inequality can aid short-term growth in settings with high sunk costs, incentive "
       "alignment, and concentrated ownership.",
       "dispersed ownership speeds corporate decision-making and removes free rider "
       "problems."], _p),
    q(_g, _slot, "Reading Comprehension - Income Inequality & Growth", "MCQ",
      "According to the incentive or moral hazard argument, which one of the designs "
      "below is most consistent with the claim that some inequality can raise growth?",
      ["Pay rewards on verifiable performance for highly productive workers.",
       "Rents protected by market power that enlarge top incomes without linking pay to "
       "results.",
       "Wages are determined by tenure rather than output to ensure equity.",
       "A regime that concentrates stock ownership in relation to corporate governance."],
      _p),
]

QUESTIONS.append(q(None, _slot, "RC Summary", "MCQ",
    "The passage given below is followed by four summaries. Choose the option that best "
    "captures the essence of the passage.\n"
    "Artists in a globalised world must navigate between drawing inspiration from diverse "
    "cultures respectfully and cultural appropriation that involves borrowing without "
    "proper acknowledgement which has broader societal impacts including perpetuating "
    "power imbalances.",
    ["Artists in a globalised world must navigate between drawing inspiration from "
     "diverse cultures respectfully and cultural appropriation that involves borrowing "
     "without proper acknowledgement which has broader societal impacts including "
     "perpetuating power imbalances.",
     "In today's world of creativity, artists have to decide between respectfully "
     "acknowledging works that are inspired by diverse cultures and appropriating "
     "elements without respect for their contexts.",
     "In a globalised world, artists must draw from diverse cultural influences to "
     "create works that appeal to all, and this results in instances of both "
     "inspiration and cultural appropriation.",
     "Artists must navigate the thin line between inspiration and cultural "
     "appropriation, where respectful inspiration fosters cultural understanding whereas "
     "appropriation involves borrowing without acknowledgement leading to "
     "commodification and reinforcement of stereotypes."]))

# ============================================================ SLOT 2 ====
_slot = "slot2"

QUESTIONS.append(q(None, _slot, "RC Summary", "MCQ",
    "The passage given below is followed by four summaries. Choose the option that best "
    "captures the essence of the passage.\n"
    "For millennia, in the process of opening up land for agriculture, gardens, grazing "
    "and hunting, humans have created ecological \"mosaics\", or \"patchworks\": "
    "landscapes holding a mixture of habitats, like meadows, gardens and forests. These "
    "were not designed as nature reserves, but often catered to hugely diverse animal "
    "life. Research indicates that European hay meadows cultivated for animal feed were "
    "actually more successful at preserving a vast array of species than meadows "
    "explicitly cultivated for biodiversity. Studying the early Holocene, researchers "
    "have found that human presence was about as likely to increase biodiversity as "
    "reduce it. Of course, not all human-created landscapes have the same value. A paved "
    "subdivision with astroturfed lawns is very different to a village with diverse "
    "vegetable and flower gardens. But scientists continue to find evidence that the old "
    "idea of humans as antithetical to nature is also wrong-headed, and that rosy visions "
    "of thriving, human-free environments are more imaginary than real.",
    ["Contrary to the idea that humans always hurt nature and that it thrives in their "
     "absence, a lot of human action across history has been equally likely to increase "
     "biodiversity than reduce it, often creating varied ecological landscapes that "
     "support a vast array of species.",
     "In our attempts to shape the world around us to our needs, humans have often "
     "created landscapes like meadows, gardens, and forests, which support hugely "
     "diverse species, and are more successful at preserving them than parks created "
     "specifically for this.",
     "Studying the early Holocene and human practices over millennia, researchers say "
     "that while agricultural meadows, gardens, and forests were not explicitly "
     "designed as nature reserves, they actually preserved a vast array of species, "
     "belying the idea that humans harm nature.",
     "In terms of preserving biodiversity, scientists are finding increasing evidence "
     "that human action is not always antithetical to nature, but often assists the "
     "preservation of meadows, landscapes, and flourishing of species."]))

_g = "cat2025_varc_slot2_rc1"
_p = (
    "This book takes the position that setting in literature is more than just backdrop, "
    "that important insight into literary texts can be made by paying close attention to "
    "how authors craft place, as well as to how place functions in a narrative. The "
    "authors included in this reference work engage deeply with either real or imagined "
    "geographies. They care about how human decisions have shaped landscapes and how "
    "landscapes have shaped human practices and values. Some of the best writing is "
    "highly vivid, employing the language of the senses because this is the primary means "
    "through which humans know physical space. Literature can offer valuable perspectives "
    "on physical and cultural geography. Unlike scientific reports, a literary narrative "
    "can provide the emotional component missing from the scientific record. In human "
    "experience, geographical places have a spiritual or emotional component in addition "
    "to and as part of a physical layout and topography. This emotional component, "
    "although subjective, is no less \"real\" than a surveyor's map. Human consciousness "
    "of place is experienced in a multi-modal manner. Histories of places live on in many "
    "forms, one of which is the human memory or imagination.\n\n"
    "Both real and imaginary landscapes provide insight into the human experience of "
    "place. The pursuit of such a topic speaks to the valuable knowledge produced from "
    "bridging disciplines and combining material from both the arts and the sciences to "
    "better understand the human condition. The perspectives that most concern cultural "
    "geographers are often those regarding movement and migration, cultivation of natural "
    "resources, and organization of space. The latter two reflect concerns of the built "
    "environment, a topic shared with the field of architectural study. Many of these "
    "concerns are also reflected in work sociologists do. Scholars from literary studies "
    "can contribute an aesthetic dimension to what might otherwise be a purely "
    "ideological approach.\n\n"
    "Literature can bring together material that spans different branches of science. For "
    "example, a literary description of place may involve not only the environment and "
    "geography but the noises and quality of light, or how people from different races or "
    "classes can experience the same place in different ways linked to those racial or "
    "class disparities. Literary texts can also account for the way in which "
    "absence-of other people, animals, and so on-affects a human observer or inhabitant. "
    "Both literary and scientific approaches to place are necessary, working in unison, "
    "to achieve a complete record of an environment. It is important to note that the "
    "interdisciplinary nature of this work teaches us that landscapes are not static, "
    "that they are not unchanged by human culture. At least part of their identity "
    "derives from the people who inhabit them and from the way space can alter and "
    "inspire human perspective. The intersection of scientific and literary expression "
    "that happens in the study of literary geography is of prime importance due to the "
    "complexity of the personal and political ways that humans experience place."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Literary Geography", "MCQ",
      "Which one of the following is a valid conclusion to draw from the author's "
      "statement that, \"The pursuit of such a topic speaks to the valuable knowledge "
      "produced from bridging disciplines and combining material from both the arts and "
      "the sciences to better understand the human condition\"?",
      ["The literary descriptions of the emotions we experience in the places we visit "
       "can contribute to our understanding of the arts and sciences.",
       "A comprehensive understanding of the human condition can best be achieved by "
       "combining the findings of disciplines from the arts and the sciences.",
       "A comprehensive bridging of the human condition can best be achieved by a "
       "disciplined pursuit of human understanding.",
       "A comprehensive understanding of the valuable knowledge produced by the arts "
       "and sciences can best be achieved by studying the human condition."], _p),
    q(_g, _slot, "Reading Comprehension - Literary Geography", "MCQ",
      "All of the following statements, if false, would contradict the arguments in the "
      "passage, EXCEPT that:",
      ["Highly vivid writing, employing the language of the senses, can capture the "
       "multi-modal manner in which humans experience places.",
       "Literature provides us with deep insights into the ways in which movement and "
       "migration affect physical geography.",
       "Humans do not interact with places in subjective, emotional ways because places "
       "are only physical topography.",
       "Descriptions of places do not need satellite imagery or other visual aids to "
       "give a \"real\" sense of the place."], _p),
    q(_g, _slot, "Reading Comprehension - Literary Geography", "MCQ",
      "The author uses the example of the literary description of place to illustrate "
      "that:",
      ["Literature can convey how different people experience the same place "
       "differently.",
       "Architects use diverse methods to calibrate the noises and lights of a given "
       "place.",
       "Scientific approaches to place are more accurate than literary ones.",
       "The absence of other people, animals, and so on in a place can profoundly "
       "affect its inhabitants."], _p),
    q(_g, _slot, "Reading Comprehension - Literary Geography", "MCQ",
      "Which one of the following is not true of the argument in the second paragraph?",
      ["The spiritual experience of a place may be considered as real as the physical "
       "experience of it.",
       "Literary accounts of places can be filled with histories, manifested as memory "
       "or imagination.",
       "Analyzing the literary descriptions of a place can give us a sense of how people "
       "relate emotionally to it.",
       "The emotional and spiritual experience of a place can replace a surveyor's "
       "map."], _p),
]

_g = "cat2025_varc_slot2_rc2"
_p = (
    "In my book \"Searches,\" I chronicle how big technology companies have exploited "
    "human language for their gain. We let this happen, I argue, because we also benefit "
    "somewhat from using the products. It's a dynamic that makes up big tech's "
    "accumulation of wealth and power: we're both victims and beneficiaries. I describe "
    "this complicity, but I also enact it, through my own internet archives: my Google "
    "searches, my Amazon product reviews, and my ChatGPT dialogues. . . .\n\n"
    "People often describe chatbots' output as \"bland\" or \"generic\" - the linguistic "
    "equivalent of a beige office building. OpenAI's products are built to \"sound like a "
    "colleague\", as OpenAI puts it, using language that, coming from a person, would "
    "sound \"polite\", \"empathetic\", \"kind\", \"rationally optimistic\" and "
    "\"engaging\", among other qualities. OpenAI describes these strategies as helping "
    "its products seem \"professional\" and \"approachable\". This appears to be bound up "
    "with making us feel safe . . .\n\n"
    "Trust is a challenge for artificial intelligence (AI) companies, partly because "
    "their products regularly produce falsehoods and reify sexist, racist, US-centric "
    "cultural norms. While the companies are working on these problems, they persist: "
    "OpenAI found that its latest systems generate errors at a higher rate than its "
    "previous system. In the book, I wrote about the inaccuracies and biases and also "
    "demonstrated them with the products. When I prompted Microsoft's Bing Image Creator "
    "to produce a picture of engineers and space explorers, it gave me an entirely male "
    "cast of characters; when my father asked ChatGPT to edit his writing, it "
    "transmuted his perfectly correct Indian English into American English. Those "
    "weren't flukes. Research suggests that both tendencies are widespread.\n\n"
    "In my own ChatGPT dialogues, I wanted to enact how the product's veneer of collegial "
    "neutrality could lull us into absorbing false or biased responses without much "
    "critical engagement. Over time, ChatGPT seemed to be guiding me to write a more "
    "positive book about big tech - including editing my description of OpenAI's CEO, "
    "Sam Altman, to call him \"a visionary and a pragmatist\". I'm not aware of research "
    "on whether ChatGPT tends to favor big tech, OpenAI or Altman, and I can only guess "
    "why it seemed that way in our conversation. OpenAI explicitly states that its "
    "products shouldn't attempt to influence users' thinking. When I asked ChatGPT about "
    "some of the issues, it blamed biases in its training data - though I suspect my "
    "arguably leading questions played a role too. When I queried ChatGPT about its "
    "rhetoric, it responded: \"The way I communicate is designed to foster trust and "
    "confidence in my responses, which can be both helpful and potentially misleading.\" "
    ". . .\n\n"
    "OpenAI has its own goals, of course. Among them, it emphasizes wanting to build AI "
    "that \"benefits all of humanity\". But while the company is controlled by a "
    "non-profit with that mission, its funders still seek a return on their investment. "
    "That will presumably require getting people using products such as ChatGPT even "
    "more than they already are - a goal that is easier to accomplish if people see "
    "those products as trustworthy collaborators."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - AI & Big Tech", "MCQ",
      "The author of the passage is least likely to agree with which one of the "
      "following claims?",
      ["When we use AI, we become accomplices to the exploitative practices of big tech "
       "companies.",
       "The neutrality of AI is conducive to critical thinking.",
       "The neutrality of AI is motivated by economic considerations.",
       "ChatGPT favours AI companies and their officials, like Sam Altman, in its "
       "responses."], _p),
    q(_g, _slot, "Reading Comprehension - AI & Big Tech", "MCQ",
      "On the basis of the purpose of the examples in the passage, pick the odd one out "
      "from the following AI-generated responses mentioned in the passage:",
      ["\"When I prompted Microsoft's Bing Image Creator to produce a picture of "
       "engineers and space explorers, it gave me an entirely male cast of "
       "characters . . .\"",
       "\". . . when my father asked ChatGPT to edit his writing, it transmuted his "
       "perfectly correct Indian English into American English.\"",
       "\"When I queried ChatGPT about its rhetoric, it responded: 'The way I "
       "communicate is designed to foster trust and confidence in my responses, which "
       "can be both helpful and potentially misleading.'\"",
       "\"Over time, ChatGPT seemed to be guiding me to write a more positive book "
       "about big tech - including editing my description of OpenAI's CEO, Sam Altman, "
       "to call him 'a visionary and a pragmatist'.\""], _p),
    q(_g, _slot, "Reading Comprehension - AI & Big Tech", "MCQ",
      "All of the following statements from the passage affirm the disjunct between the "
      "claims about AI made by tech companies and what AI actually does EXCEPT:",
      ["\"I'm not aware of research on whether ChatGPT tends to favor big tech, OpenAI "
       "or Altman, and I can only guess why it seemed that way in our conversation.\"",
       "\"It's a dynamic that makes us complicit in big tech's accumulation of wealth "
       "and power: we're both victims and beneficiaries.\"",
       "\"When I prompted Microsoft's Bing Image Creator to produce a picture of "
       "engineers and space explorers, it gave me an entirely male cast of "
       "characters . . .\"",
       "\"In my own ChatGPT dialogues, I wanted to enact how the product's veneer of "
       "collegial neutrality could lull us into absorbing false or biased responses "
       "without much critical engagement.\""], _p),
    q(_g, _slot, "Reading Comprehension - AI & Big Tech", "MCQ",
      "The author compares AI-generated texts with \"a beige office building\" for all "
      "of the following reasons EXCEPT:",
      ["AI generates generalized responses that lack specificity and nuance.",
       "AI-generated texts often exhibit a warm, polite, and collegial tone.",
       "AI aims to foster a feeling of trust and credibility among its users.",
       "AI tends to blame its training data when scrutinized for its biases."], _p),
]

_g = "cat2025_varc_slot2_rc3"
_p = (
    "Time and again, whenever a population of [Mexican tetra fish] was swept into a cave "
    "and survived long enough for natural selection to have its way, the caves adapted. "
    "\"But it's not that they have been losing their vision,\" as one of the authors of "
    "the study explains. \"Studies have found that cave-dwelling fish can detect lower "
    "levels of amino acids than surface fish can. They have also more tastebuds and a "
    "higher density of sensitive cells alongside their bodies that let them sense water "
    "pressure and flow . . .\"\n\n"
    "Killing the processes that support the formation of the eye is quite literally what "
    "happens. Just like non-cave-dwelling members of the species, all cavefish embryos "
    "start making eyes. But after a few hours, cells in the developing eye get tiny until "
    "the entire structure has disappeared. (Developmental biologist Melody Riddle thinks "
    "this apparent inefficiency may be unavoidable: \"The development of the brain and "
    "the eye are completely intertwined-so when eyes disappear, it impacts the entire "
    "biology of the animal. It's hard to tell exactly how they happen together,\" she "
    "says. That means the last step in survival for eye-less animals may be to start "
    "making an eye and then get rid of it. . . .\n\n"
    "It's easy to see why cavefish would be at a disadvantage if they were to maintain "
    "excessive tissues they aren't using. Since relatively little lives or grows in "
    "their caves, the fish are likely surviving on a meager diet of mostly bat feces and "
    "organic waste that washes in during the rainy season. Researchers keeping cavefish "
    "in labs have discovered that cavefish are exquisitely adapted to absorbing and "
    "using nutrients. . . .\n\n"
    "Cells can be toxic for tissues, [evolutionary physiologist Nicolas] Rohner "
    "explains, so they are stored in fat cells. \"But when these cells get too big, they "
    "can burst, which is why we often see chronic inflammation in humans and other "
    "animals that have stored a lot of fat in their tissues.\" Yet a 2020 study by "
    "Riddle, Rohner and their colleagues revealed that even very well-fed cavefish had "
    "fewer signs of inflammation in their fat tissues than surface fish do. Even in "
    "their sparse cave conditions, wild cavefish can sometimes get very fat, says "
    "Riddle. This is presumably because, whenever food piles up in the cave, the fish "
    "eat as much of it as possible, since there might not be enough for a long time to "
    "come. Intriguingly, Riddle says, their fat is usually bright yellow, because of "
    "high levels of carotenoids, the substance in the carrots that your grandmother "
    "used to tell you were good for your...eyes. \"The first thing that came to our "
    "mind, of course, was that they were accumulating these compounds because they "
    "don't have eyes,\" says Riddle. In this species, such ideas can be tested: "
    "Scientists can cross surface fish (with eyes) and cavefish (without eyes) and look "
    "at what their offspring are like. When that's done, Riddle says, researchers see "
    "no link between eye presence or size and the accumulation of carotenoids. Some "
    "eyeless cavefish had fat that was completely white, indicating lower carotenoid "
    "levels. Instead, Riddle thinks these carotenoids may be another adaptation to "
    "suppress inflammation, which might be important in the wild, as cavefish are "
    "likely eating whenever food arrives."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Cavefish Adaptation", "MCQ",
      "All of the following statements from the passage describe adaptation in Mexican "
      "tetra cavefish EXCEPT:",
      ["Since relatively little lives or grows in their caves, the fish are likely "
       "surviving on a meager diet of mostly bat feces and organic waste that washes in "
       "during the rainy season.",
       "Even in their sparse cave conditions, wild cavefish can sometimes get very fat, "
       "says Riddle.",
       "It's easy to see why cavefish would be at a disadvantage if they were to "
       "maintain excessive tissues they aren't using.",
       "But when these cells get too big, they can burst, which is why we often see "
       "chronic inflammation in humans and other animals that have stored a lot of fat "
       "in their tissues."], _p),
    q(_g, _slot, "Reading Comprehension - Cavefish Adaptation", "MCQ",
      "On the basis of the information in the passage, what is the most likely function "
      "of carotenoids in Mexican tetra cavefish?",
      ["To act as a substitute for eyes.",
       "To control inflammation from the bursting of fat cells.",
       "To render bright yellow colour to the cavefish.",
       "To help the fat cells store nutrients."], _p),
    q(_g, _slot, "Reading Comprehension - Cavefish Adaptation", "MCQ",
      "Which one of the following results for the cross between surface fish (with eyes) "
      "and cavefish (without eyes) would invalidate Riddle's inference from the "
      "experiment?",
      ["Some offspring with eyes had white fat.",
       "Only eyeless offspring had yellow fat.",
       "Some offspring with eyes had yellow fat.",
       "Some eyeless offspring had white fat."], _p),
    q(_g, _slot, "Reading Comprehension - Cavefish Adaptation", "MCQ",
      "Which one of the following best explains why the \"apparent inefficiency\" is "
      "\"unavoidable\"?",
      ["The lack of light in the caves kills the eye cells in the developing Mexican "
       "tetra cavefish embryo.",
       "The inefficiency resulting from eyelessness is compensated by enhancements like "
       "more tastebuds in Mexican tetra cavefish.",
       "The caves have poor and inconsistent availability of food and nutrition for "
       "Mexican tetra cavefish.",
       "Mexican tetra cavefish are similar to non-cave-dwelling variants in their early "
       "stages of development."], _p),
]

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "The given sentence is missing in the paragraph below. Decide where it best fits "
    "among the options 1, 2, 3, or 4 indicated in the paragraph.\n"
    "Sentence: The region's Western customers found it hard to believe that Dhaka muslin "
    "could possibly have been made by human hands - there were rumours that it was woven "
    "by mermaids, fairies and even ghosts.\n\n"
    "Once upon the silty banks of the Meghna River, a miracle was spun - a fabric so "
    "light it was called \"baft-hawa\", or woven air. This was Dhaka Muslin - the "
    "world's most coveted cloth. ____(1)____. Handspun from a rare cotton called Phuti "
    "Karpas, found nowhere else on Earth, and woven with a 16-step sacred ritual - "
    "beginning with cleaning the cotton using the teeth of a river catfish! ____(2)____. "
    "Every spring, the maple-like leaves pushed up through the grey, silty soil to "
    "produce a single daffodil-yellow flower twice a year, which gave way to a snowy "
    "floret of cotton fibres. ____(3)____. Spun at dawn on boats by sharp-eyed young "
    "women, its threads were so fine the elderly could barely see them. Motifs of "
    "wildflowers, river breeze, and soul were etched into each piece - some so sleek, a "
    "91-metre bolt could pass through a ring, or a 60' length fit inside a snuffbox. It "
    "draped Greek goddesses, Roman nobles, Mughal emperors, and European aristocrats. "
    "Marie Antoinette, Empress Joséphine - even Jane Austen adored its floating grace. "
    "____(4)____.",
    ["Option 2", "Option 4", "Option 1", "Option 3"]))

_g = "cat2025_varc_slot2_rc4"
_p = (
    "Different sciences exhibit different science cultures and practices. For example, "
    "in astronomy, observation - until what is today called the new astronomy - had "
    "always been limited to what could be seen within the limits of optical light. "
    "Indeed, until early modernity the limits to optical light were also limits of what "
    "humans could immerse themselves with their limited and relative perceptual spectrum "
    "of human vision. With early modernity and the invention of lenses for optical "
    "instruments - telescopes - astronomers could begin to observe phenomena never seen "
    "before. Magnification and resolution began to allow what was previously "
    "imperceptible to be perceived - but within the familiar limits of optical vision. "
    "Galileo, having learned of the Dutch invention of a telescope by Hans Lippershey, "
    "went on to build some hundred of his own, improving from the Dutch to nearly 30x "
    "telescopes - which turn out to be the limit of magnificational power without "
    "chromatic distortion. And it was with his own telescopes that he made the "
    "observations launching early modern astronomy (phases of Venus, satellites of "
    "Jupiter, etc.). Isaac Newton's later improvement with reflecting telescopes "
    "expanded upon the magnification-resolution capacity of optical observation; and, "
    "from Newton to the twentieth century, improvement continued to the later very "
    "large array of light telescopes today - following the usual technological "
    "trajectory of \"more-is-better\" but still remaining within the limits of the light "
    "spectrum. Today's astronomy has now had the benefit of some four centuries of "
    "optical telescope. The \"new astronomy,\" however, opens the full known "
    "electromagnetic spectrum to observation, beginning with the accidental discovery of "
    "radio astronomy early in the twentieth century, and leading today to the diverse "
    "variety of EMS telescopes which can explore the range from gamma to radio waves. "
    "Thus, astronomy, now outfitted with new instruments, \"smart\" adaptive optics, "
    "very large arrays, etc., illustrates one style of instrumentally embodied science - "
    "a technoscience. Of course astronomy, with the very recent exceptions of probes to "
    "solar system bodies (Moon, Mars, Venus, asteroids), remains largely a \"receptive\" "
    "science, dependent upon instrumentation which can detect and receive emissions.\n\n"
    "Contemporary biology displays a quite different instrument array and, according to "
    "Evelyn Fox-Keller, also a different scientific culture. She cites her own "
    "experience, coming from mathematical physics into microbiology, and takes account "
    "of the distinctive instrumental culture in her Making Sense of Life (2002). Here, "
    "particularly with the development of biotechnology, instrumentation is far more "
    "interventional than in the astronomy case. Microscopic instrumentation can be and "
    "often is interventional in style: \"gene-splicing\" and other techniques of "
    "biotechnology, while still in their infancy, are clearly part of the interventional "
    "trajectory of biological instrumentation. Yet, in both disciplines, the sciences "
    "involved are today highly instrumentalized and could not progress successfully "
    "without constant improvements upon the respective instrumental trajectories. So, "
    "minimalistically, one may conclude that the sciences are technologically, "
    "instrumentally embodied. But the styles of embodiment differ, and perhaps the last "
    "of the scientific disciplines to move into such technical embodiment is "
    "mathematics, which only contemporary has come to rely more and more upon the "
    "computational machinery now in common use."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Science & Instrumentation", "MCQ",
      "To which one of the following instruments would the characterisations of "
      "instruments in the passage be least applicable?",
      ["Milestone", "Scalpel", "Saxophone", "Kitchen oven"], _p),
    q(_g, _slot, "Reading Comprehension - Science & Instrumentation", "MCQ",
      "Which one of the following observations is a valid conclusion to draw from the "
      "statement that \"the sciences involved are today highly instrumentalised and "
      "could not progress successfully without constant improvements upon the "
      "respective instrumental trajectories\"?",
      ["In both astronomy and microbiology, progress has been the consequence of "
       "improvements in the instruments they use.",
       "Highly instrumentalised work in the sciences has resulted in the progressive "
       "improvement of scientific constants.",
       "The growth of scientific technologies has led to the embodiment of progress in "
       "the trajectories of improvement.",
       "The use of instruments in scientific trajectories must be respected in order to "
       "see successful progress in them."], _p),
    q(_g, _slot, "Reading Comprehension - Science & Instrumentation", "MCQ",
      "None of the following statements, if true, contradicts the arguments in the "
      "passage EXCEPT:",
      ["Some scientific instruments may be classified as both receptive and "
       "interventional in their functions.",
       "Isaac Newton's discovery of gravity was accomplished without the help of "
       "instruments.",
       "Like telescopes, microscopy has also sought to move beyond the visible spectrum "
       "to be able to detect objects that are invisible in that spectrum.",
       "Because of the relatively recent entry of computational machinery in "
       "mathematics, the field is only now beginning to develop a scientific culture."],
      _p),
    q(_g, _slot, "Reading Comprehension - Science & Instrumentation", "MCQ",
      "All of the following statements may be rejected as valid inferences from the "
      "passage EXCEPT:",
      ["The author distinguishes between the receptive and interventionist uses of "
       "instruments in the sciences by comparing astronomy and biology, respectively.",
       "Interventionist instruments, or instruments that intervene directly in "
       "scientific inquiry, are different from embodied instruments, or instruments "
       "that embody scientific inquiry.",
       "Isaac Newton's experiments with reflecting telescopes were the earliest "
       "versions of the \"new astronomy\" referred to in the passage.",
       "The advances in telescope made by Newton with reflecting telescopes allowed "
       "early modern astronomers to observe the phases of Venus and the satellites of "
       "Jupiter."], _p),
]

QUESTIONS.append(q(None, _slot, "Sentence Sequencing", "TITA",
    "The four sentences (labelled 1, 2, 3, and 4) given below, when properly sequenced, "
    "would yield a coherent paragraph. Decide on the proper sequencing of the order of "
    "the sentences and key in the sequence of the four numbers as your answer.\n"
    "1. \"Literature on screen\" suggests something more capacious and defining than "
    "citation: the possibility that literary adaptations are at once cinema and "
    "literature.\n"
    "2. Even though a growing number of films eligible for Academy Awards for Best "
    "Screenplay Based on Material from Another Medium borrow that material from print "
    "journalism, franchise characters, television series, comic books, video games and "
    "toys, academic studies of adaptation remain stubbornly attached to literature as "
    "cinema's natural progenitor.\n"
    "3. It is as if adaptation studies, by borrowing the cultural cachet of literature, "
    "sought to claim its institutional respectability and gravitas even while insuring "
    "adaptation's enduring aesthetic and methodological subordination to literature "
    "proper.\n"
    "4. Beneath this contradictory notion of film adaptations as not merely hybrid texts "
    "but texts holding dual citizenship in two modes of presentation is an even more "
    "pervasive legacy that haunts adaptation studies: the assumption that the primary "
    "context within which adaptations are to be studied is literature."))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "The given sentence is missing in the paragraph below. Decide where it best fits "
    "among the options 1, 2, 3, or 4 indicated in the paragraph.\n"
    "Sentence: While taste is related to judgment, with thinkers at the time often "
    "writing, for example, about \"judgments of taste\" or using the two terms "
    "interchangeably, taste retains a vital link to pleasure, embodiment, and personal "
    "specificity that is too often elided in post-Kantian ideas about judgment-a link "
    "that Arendt herself was working to restore.\n\n"
    "Paragraph: ____(1)____ Denneny focused on taste rather than judgment in order to "
    "highlight what he believed was a crucial but neglected historical change. "
    "____(2)____ Over the course of the seventeenth century and early eighteenth "
    "century, across Western Europe, the word taste took on a new extension of meaning, "
    "no longer referring specifically to gustatory sensation and the delights of the "
    "palate but becoming, for a time, one of the central categories for aesthetic-and "
    "ethical-thinking. ____(3)____ Tracing the history of taste in Spanish, French, and "
    "British aesthetic theory, as Denneny did, also provides a means to recover the "
    "compelling and relevant writing of a set of thinkers who have been largely "
    "neglected by professional philosophy. ____(4)____",
    ["Option 1", "Option 3", "Option 4", "Option 2"]))

QUESTIONS.append(q(None, _slot, "RC Summary", "MCQ",
    "The passage given below is followed by four summaries. Choose the option that best "
    "captures the essence of the passage.\n"
    "In 1903, left-wing feminist Elizabeth Magie invented The Landlord's Game, the "
    "original version of what became Monopoly. It was designed as a powerful teaching "
    "tool to illustrate the dangers of monopolies and how wealth could concentrate in "
    "the hands of a few. The game featured a circular path, properties, and a \"Go to "
    "Jail\" space. Magie created two rule sets: one \"monopolist\" version where players "
    "crushed opponents through accumulation, and another, more radical \"Prosperity\" "
    "version, where everyone shared in the wealth, promoting fairness and equity. Years "
    "later, unemployed Charles Darrow sold a simplified version to Parker Brothers. They "
    "paid Magie only 500 Dollar for her patent-without royalties-and credited Darrow as "
    "the sole inventor. For decades, his tale of inventing the game in his basement "
    "remained the official story, while Magie's name and her original, anti-capitalist "
    "message were left in the shadows.",
    ["Celebrated icons of the gaming industry, Charles Darrow and Parker Brothers, "
     "snatched the feminist icon Elizabeth Magie's original design and transformed "
     "Monopoly into a worldwide phenomenon, while barely acknowledging her.",
     "Parker Brothers' capitalist intent led to them acquiring from Charles Darrow a "
     "simplified version of Elizabeth Magie's original game, transforming it into a "
     "widespread commercial success while providing her only minimal financial "
     "compensation and granting scant public recognition.",
     "It is ironic that a left-wing feminist lost credit for the Landlord's Game to an "
     "unemployed man, who plagiarised and sold one version of the twin game to Parker "
     "Brothers for a meagre sum, denying her royalties.",
     "Only one version of Monopoly became famous because of Charles Darrow's relentless "
     "basement work, carefully refining Elizabeth Magie's original idea into an "
     "engaging and entertaining pastime that he successfully patented and sold, "
     "symbolizing what many regarded as the ultimate triumph of individual ingenuity."]))

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled sentences (labelled 1, 2, 3, 4, and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence out and key in the number of that sentence as your answer.\n"
    "1. Pfas are a class of about 15,000 compounds most frequently used to make products "
    "water-, stain- and grease-resistant.\n"
    "2. New research suggests exposure to some common perfluoroalkyl and polyfluoroalkyl "
    "substances (Pfas) cause changes to gene activity and that these changes are linked "
    "to health problems including multiple cancers, neurological disorders and "
    "autoimmune disease.\n"
    "3. These Pfas compounds are dubbed \"forever chemicals\" because they do not "
    "naturally break down in the environment.\n"
    "4. The research may also point toward other diseases potentially caused by Pfas "
    "that have not yet been identified.\n"
    "5. The findings are a major step toward determining the mechanism by which the "
    "chemicals cause disease and could help doctors identify, detect and treat health "
    "problems for those exposed to Pfas before the issues advance."))

QUESTIONS.append(q(None, _slot, "Sentence Sequencing", "TITA",
    "The four sentences (labelled 1, 2, 3, and 4) given below, when properly sequenced, "
    "would yield a coherent paragraph. Decide on the proper sequencing of the order of "
    "the sentences and key in the sequence of the four numbers as your answer.\n"
    "1. As books age, the cellulose and lignin in the paper begin to break down, "
    "releasing a mix of volatile organic compounds into the air.\n"
    "2. Old books carry a scent that many people instantly recognize-and even love.\n"
    "3. These compounds are benzaldehyde, which gives off an almond-like scent, "
    "vanillin, which smells like vanilla, ethyl hexanol (floral scent), toluene (sweet), "
    "and furfural (which has a slightly bready scent).\n"
    "4. This familiar aroma isn't just dust or mildew; it's actually a result of slow "
    "chemical changes happening inside the paper and ink."))

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled sentences (labelled 1, 2, 3, 4, and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence out and key in the number of that sentence as your answer.\n"
    "1. Sporting a copper-coloured pixie cut and a pair of pink feather antlers, Torres "
    "himself resembles a child's doodle.\n"
    "2. His casual millennial delivery, peppered with \"um's\" and \"ah's\", makes "
    "surreal concepts sound like items on a brunch menu.\n"
    "3. Though he may have failed so far in his colour-scouting mission (he hasn't yet "
    "found a new one, he admits), this hour leaves you tickled pink.\n"
    "4. Like his previous show, My Favourite Shapes, this is an hour of sit-down comedy "
    "aided by an overhead camera which relays Torres's theories - illustrated with "
    "crayon squiggles - on to a screen behind him.\n"
    "5. His inquisitive mind produces interconnected ideas about Catholicism, the "
    "blandness of Pixar and what orange sounds like, while his insights train us to "
    "spot \"highly purple behaviour\"."))

# ============================================================ SLOT 3 ====
_slot = "slot3"

_g = "cat2025_varc_slot3_rc1"
_p = (
    "Imagine a world in which artificial intelligence is entrusted with the highest "
    "moral responsibilities: sentencing criminals, allocating medical resources, and "
    "even mediating conflicts between nations. This might seem like the pinnacle of "
    "human progress: an entity unburdened by emotion, prejudice or inconsistency, "
    "making ethical decisions with impeccable precision. . . .\n\n"
    "Yet beneath this vision of an idealised moral arbiter lies a fundamental question: "
    "can a machine understand morality as humans do, or is it confined to a simulacrum "
    "of ethical reasoning? AI might replicate human decisions without improving on "
    "them, carrying forward the same biases, blind spots and cultural distortions from "
    "human moral judgment. In trying to emulate us, it might only reproduce our "
    "limitations, not transcend them. But there is a deeper concern. Moral judgment "
    "draws on intuition, historical awareness and context - qualities that resist "
    "formalisation. Ethics may be so embedded in lived experience that any attempt to "
    "encode it into formal structures risks flattening its most essential features. If "
    "so, AI would merely reflect human shortcomings; it would strip morality of the "
    "very depth that makes ethical reflection possible in the first place.\n\n"
    "Still, many have tried to formalise ethics, by treating certain moral claims not "
    "as conclusions, but as starting points. A classic example comes from "
    "utilitarianism, which often takes as a foundational axiom the principle that one "
    "should act to maximise overall wellbeing. From this, more specific principles can "
    "be derived, for example, that it is right to benefit the greatest number, or that "
    "actions should be judged by their consequences for total happiness. As "
    "computational resources increase, AI becomes increasingly well-suited to the task "
    "of starting from fixed ethical assumptions and reasoning through their "
    "implications in complex situations.\n\n"
    "But, what exactly, does it mean to formalise something like ethics? The question "
    "is easier to grasp by looking at fields in which formal systems have long played a "
    "central role. Physics, for instance, has relied on formalisation for centuries. "
    "There is no single physical theory that explains everything. Instead, we have "
    "many physical theories, each designed to describe specific aspects of the "
    "Universe: from the behaviour of quarks and electrons to the motion of galaxies. "
    "These theories often diverge. Aristotelian physics, for instance, explained "
    "falling objects in terms of natural motion toward Earth's centre; Newtonian "
    "mechanics replaced this with a universal force of gravity. These explanations are "
    "not just different; they are incompatible. Yet both share a common structure: "
    "they begin with basic postulates - assumptions about motion, force or mass - and "
    "derive increasingly complex consequences. . . .\n\n"
    "Ethical theories have a similar structure. Like physical theories, they attempt to "
    "describe a domain - in this case, the moral landscape. They aim to answer "
    "questions about which actions are right or wrong, and why. These theories also "
    "diverge, and even when they recommend similar actions, such as giving to charity, "
    "they justify them in different ways. Ethical theories also often begin with a "
    "small set of foundational principles or claims, from which they reason about more "
    "complex moral problems."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - AI & Ethics", "MCQ",
      "All of the following can reasonably be inferred from the passage EXCEPT:",
      ["The appeal of an AI judge rests on immunity to bribery, partiality, and "
       "fatigue; yet the text questions whether procedural cleanliness amounts to "
       "moral understanding without lived context and interpretive depth.",
       "By analogy with physics, compact postulates can yield broad predictions across "
       "incompatible theories and ethics can likewise share structure while continuing "
       "to diverge rather than close on a single comprehensive framework.",
       "Encoding ethics into fixed structures risks stripping away intuition, history, "
       "and context and, if that occurs, the depth that enables reflective judgment "
       "disappears. So, machines would mirror our limits rather than exceed them.",
       "With fixed moral starting points and expanding computational resources, the "
       "argument forecasts convergence on one ethical system and treats contextual "
       "judgment as unnecessary once formal reasoning scales across domains and "
       "cultures."], _p),
    q(_g, _slot, "Reading Comprehension - AI & Ethics", "MCQ",
      "Which one of the options below best summarises the passage?",
      ["The passage highlights administrative gains from automation. It treats "
       "reproducing human moral judgment as progress and argues that, as computational "
       "resources increase, AI can be responsible for decision-making across varied "
       "institutional settings.",
       "The passage weighs the appeal of an impersonal AI judge against doubts about "
       "moral grasp. It warns that codification can erode case-sensitive judgment, "
       "allow axiom-led reasoning at scale, and use a physics analogy to model "
       "structured plurality.",
       "The passage weighs the appeal of an impersonal AI judge against doubts about "
       "moral grasp. It claims codified schemes retain case nuance at scale and uses a "
       "physics analogy to predict convergence on a unified framework.",
       "The passage rejects formal methods in principle. It holds that moral judgment "
       "cannot be expressed in disciplined terms and concludes that AI should not "
       "serve in courts, medicine, or diplomacy under any conditions."], _p),
    q(_g, _slot, "Reading Comprehension - AI & Ethics", "MCQ",
      "The passage compares ethics to physics, where different theories apply to "
      "different aspects of a domain and says AI can reason from fixed starting points "
      "in complex cases. Which one of the assumptions below must hold for that "
      "comparison to guide practice?",
      ["Real cases never straddle different areas, so a case always fits exactly one "
       "framework without any overlap whatsoever.",
       "Once formalised, all ethical frameworks yield the same recommendation in every "
       "case, so selection among them is unnecessary.",
       "A single master framework replaces all others after translation into one code, "
       "so domain boundaries disappear in application.",
       "There is a principled way to decide which ethical framework applies to which "
       "class of cases, so the system can select the relevant starting points before "
       "deriving a recommendation."], _p),
    q(_g, _slot, "Reading Comprehension - AI & Ethics", "MCQ",
      "Choose the one option below that comes closest to being the opposite of "
      "\"utilitarianism\".",
      ["The committee adopted a non-egoist framework, ranking policies by their "
       "contribution to overall social welfare and treating self-interest as a "
       "derivative concern within institutional evaluation.",
       "The council followed a priorititarian approach, assigning greater moral weight "
       "to improvements for the worst-off rather than to maximising total welfare "
       "across the affected population.",
       "The authors advocated an absolutist stance, following exceptionless rules "
       "regardless of outcomes and evaluating choices by broadest societal benefit.",
       "The policy was cast as deontological ethics, selecting the option that "
       "delivered the highest total benefit to citizens while presenting duty as a "
       "secondary consideration in public decision-making."], _p),
]

_g = "cat2025_varc_slot3_rc2"
_p = (
    "In 1982, a raging controversy broke out over a forest act drafted by the "
    "Government of India. This act sought to strengthen the already extensive powers "
    "enjoyed by the forest bureaucracy in controlling the extraction, disposal and sale "
    "of forest produce. It also gave forest officials greater powers to strictly "
    "regulate the entry of any person into reserved forest areas. While forest "
    "officials justified the act on the grounds that it was necessary to stop the "
    "continuing deforestation, it was bitterly opposed by representatives of grassroots "
    "organisations, who argued that it was a major violation of the rights of peasants "
    "and tribals living in and around forest areas. . . .\n\n"
    "The debate over the draft forest act fuelled a larger controversy over the "
    "orientation of state forest policy. It was pointed out, for example, that the "
    "draft act was closely modelled on its predecessor, the Forest Act of 1878. The "
    "earlier Act rested on a usurpation of rights of ownership by the colonial state "
    "which had little precedent in precolonial history. It was further argued that the "
    "system of forestry introduced by the British-and continued, with little "
    "modification, after 1947-emphasised revenue generation and commercial "
    "exploitation, while its policing orientation excluded villagers who had the most "
    "longstanding claim on forest resources. Critics called for a complete overhaul of "
    "forest administration, pressing the government to formulate policy and "
    "legislation more appropriate to present needs. . . .\n\n"
    "That debate is not over yet. The draft act was shelved, though it has not as yet "
    "been formally withdrawn. Meanwhile, the 1878 Act (as modified by an amendment in "
    "1927) continues to be in operation. In response to its critics, the government has "
    "made some important changes in forest policy, e.g., no longer treating forests as "
    "a source of revenue, and stopping ecologically hazardous practices such as the "
    "clearfelling of natural forests. At the same time, it has shown little inclination "
    "to meet the major demand of the critics of forest policy-namely, abandoning the "
    "principle of state monopoly over forest land by handing over areas of degraded "
    "forests to individuals and communities for afforestation.\n\n"
    ". . . [The] 1878 Forest Act itself was passed only after a bitter and prolonged "
    "debate within the colonial bureaucracy, in which protagonists put forward "
    "arguments strikingly similar to those being advanced today. As well known, the "
    "Indian Forest Department owes its origin to the requirements of railway companies. "
    "The early years of the expansion of the railway network, c. 1853 onwards, led to "
    "tremendous deforestation in peninsular India owing to the railway's requirements "
    "of fuelwood and construction timber. Huge quantities of durable timbers were also "
    "needed for use as sleepers across the new railway tracks. Inexperienced in "
    "forestry, the British called in German experts to commence systematic forest "
    "management. The Indian Forest Department was started in 1864, with Dietrich "
    "Brandis, formally a Lecturer in Botany, as the first Inspector General of Forests. "
    "The early years of the forest department, even as it grew, continued to meet the "
    "railway needs for timber and wood. These systems first emerged as part of the "
    "needs of the expanding empire."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Forest Policy in India", "MCQ",
      "Which one of the following best encapsulates the reason for the \"raging "
      "controversy\" developing into a \"larger controversy\"?",
      ["The 1982 draft forest act further enabled the commercial exploitation of "
       "forest resources by the forest bureaucracy.",
       "The 1982 draft forest act violated the rights of tribals and peasants who "
       "lived in and around forest areas.",
       "The 1982 draft forest act replicated colonial measures of control and "
       "regulation of forest resources.",
       "The 1982 draft forest act was unjustifiably defended by forest officials in "
       "the face of bitter opposition by grassroots organisations."], _p),
    q(_g, _slot, "Reading Comprehension - Forest Policy in India", "MCQ",
      "According to the passage, which one of the following reforms is yet to happen "
      "in India's forest policies?",
      ["Involving local people in cultivating forests.",
       "Recognising the significance of forests to ecology.",
       "A ban on deforestation.",
       "Recognising the state's claim to forest land use."], _p),
    q(_g, _slot, "Reading Comprehension - Forest Policy in India", "MCQ",
      "According to the passage, which one of the following is not common to the 1878 "
      "Forest Act and the 1982 draft forest act?",
      ["Both resulted in large scale deforestation.",
       "Both sparked controversy and debate among the various stakeholders.",
       "Both sought to establish the state's monopoly over forest resources.",
       "Both reflect a colonial mindset."], _p),
    q(_g, _slot, "Reading Comprehension - Forest Policy in India", "MCQ",
      "All of the following, if true, would weaken the narrative presented in the "
      "passage EXCEPT that:",
      ["Before British rule, peasants and tribal groups were denied access to forest "
       "resources by Indian rulers and their administrations.",
       "Certain tribal groups in India are responsible for climate change because "
       "their sustenance has historically depended on mass scale deforestation.",
       "The timber requirement for railway works in nineteenth century India was met "
       "through import from China, in exchange for spices.",
       "Nineteenth century German forestry experts were infamous for violating the "
       "rights of indigenous communities that lived in forest regions."], _p),
]

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "The given sentence is missing in the paragraph below. Decide where it best fits "
    "among the options 1, 2, 3, or 4 indicated in the paragraph.\n"
    "Sentence: In each of the affected males, the genetic defect was located to the X "
    "chromosome in the region of p11-12.\n\n"
    "Paragraph: The first suggested evidence of a human genetic mutation associated "
    "with aggressive behaviour came from a study in 1993. ____(1)____. Genetic and "
    "metabolic studies were conducted on a large Dutch family in which several of the "
    "males has a syndrome of borderline mental retardation and abnormal behaviour. "
    "____(2)____. The undesirable behaviour included impulsive aggression, arson and "
    "exhibitionism. ____(3)____. A point mutation was identified in the eighth exon of "
    "the monoamine oxidase A (MAOA) structural gene which changes glutamine to a "
    "termination codon. ____(4)____.",
    ["Option 1", "Option 2", "Option 3", "Option 4"]))

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled sentences (labelled 1, 2, 3, 4, and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence out and key in the number of that sentence as your answer.\n"
    "1. About half of all the oxygen we breathe is made near the surface of the ocean "
    "by phytoplankton that photosynthesize just like land-dwelling plants.\n"
    "2. A team of scientists that includes Boston University experts has discovered "
    "they also produce oxygen on the seafloor.\n"
    "3. The research team used deep-sea chambers that land on the seafloor and enclose "
    "the seawater, sediment, polymetallic nodules, and living organisms.\n"
    "4. The discovery is a surprise considering oxygen is typically created by plants "
    "and organisms with help from the sun-not by rocks on the ocean floor.\n"
    "5. The deep-sea rocks, called polymetallic nodules, don't only host a surprising "
    "number of sea critters."))

QUESTIONS.append(q(None, _slot, "Sentence Sequencing", "TITA",
    "The four sentences (labelled 1, 2, 3, and 4) given below, when properly sequenced, "
    "would yield a coherent paragraph. Decide on the proper sequencing of the order of "
    "the sentences and key in the sequence of the four numbers as your answer.\n"
    "1. When I ask the distinguished LGBTQ activist and writer Cherie Moraga whether "
    "she uses Latinx to refer to herself, she tells me, 'I worked too hard for the "
    "\"a\" in Latina to give it up! I refer to myself as Xicana.'\n"
    "2. Of our accumulated ethnic population, only a third use Hispanic to identify "
    "themselves, a mere 14 percent use Latino, and less than 2 percent recognize "
    "Latinx.\n"
    "3. They have done this, although gender in languages is grammatical, not "
    "sociological or sexual, and found in linguistic families throughout the world, "
    "from French to Russian to Japanese.\n"
    "4. More recently, activists seeking to render our name gender neutral, out of "
    "respect for our LGBTQ members, have devised yet another name for us: Latinx."))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "The given sentence is missing in the paragraph below. Decide where it best fits "
    "among the options 1, 2, 3, or 4 indicated in the paragraph.\n"
    "Sentence: Productivity gains, once expected to feed through to broader living "
    "standards, now primarily serve to enhance returns to wealth.\n\n"
    "Paragraph: Economists now argue that inequality is no longer a by-product of "
    "growth but a condition of it. ____(1)____. Unlike wages, wealth reflects not just "
    "income but also access to assets, favourable institutional conditions-such as low "
    "interest rates-and public policies like low taxes and housing shortages. "
    "____(2)____. In other words, wealth depends on political choices in ways that "
    "income currently does not. It's not just the inequality itself that is the issue "
    "but the erosion of mechanisms that once constrained it. ____(3)____. Wealth and "
    "income inequality are linked, but where wages have stagnated and collective "
    "bargaining has weakened, capital income-derived from profits, rents and "
    "interest-has been boosted by design. ____(4)____.",
    ["Option 1", "Option 2", "Option 3", "Option 4"]))

QUESTIONS.append(q(None, _slot, "RC Summary", "MCQ",
    "The passage given below is followed by four summaries. Choose the option that best "
    "captures the essence of the passage.\n"
    "The return to the tailor is the juxtaposition of three key things for the mindful "
    "Indian shopper. The first is the conscious shift away from the homogeneity of "
    "fast fashion, the idea of a hundred other people owning exactly the same Zara "
    "trench coat or H&M pleated skirt. The second is an actual understanding of the "
    "waste behind the fast fashion market, and wanting not to contribute to that "
    "anymore. The last is the shift toward customisation and fit-the idea of having "
    "imaginations brought to life and to have them fit exactly; without paying "
    "exorbitant rates for that bespoke tailoring. For the individual with a keen "
    "fashion sense and a genuine desire to move away from the waste and uniformity of "
    "fast fashion without paying the premium for it that indie brands would invariably "
    "demand, the tailor is the perfect crossover.",
    ["The mindful Indian shopper is shifting away from convenience and uniformity of "
     "clothing, and waste in fashion, to customisation and less exorbitantly priced "
     "clothing.",
     "In the Indian retail market, people believe that expensive branded clothes are "
     "wasteful and, therefore, are returning to the neighbourhood tailor.",
     "The mindful Indian shoppers are returning to the tailor with a genuine desire to "
     "wear clothes which are less expensive, fit them well and are yet fashionable.",
     "All Indian shoppers are opting for customisation and a shift away from "
     "homogeneity over expensive clothing brands like Zara and H&M."]))

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled sentences (labelled 1, 2, 3, 4, and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence out and key in the number of that sentence as your answer.\n"
    "1. The profound emotional impact of music has inspired ongoing research into its "
    "relationship with emotions.\n"
    "2. Music is a universal phenomenon that utilizes a myriad brain resources.\n"
    "3. This inherent connection to musical expression is deeply intertwined with "
    "human identity and experience.\n"
    "4. The proclivity to create and appreciate music is ubiquitous among humans, "
    "permeating daily life across diverse societies.\n"
    "5. Engaging with music is among the most cognitively demanding tasks a human can "
    "undergo, and it is identified across cultures."))

QUESTIONS.append(q(None, _slot, "Sentence Sequencing", "TITA",
    "The four sentences (labelled 1, 2, 3, and 4) given below, when properly sequenced, "
    "would yield a coherent paragraph. Decide on the proper sequencing of the order of "
    "the sentences and key in the sequence of the four numbers as your answer.\n"
    "1. The effigy of a candidate establishes a personal link between him and the "
    "voters; the candidate does not only offer a programme for judgement, he suggests "
    "a physical climate, a set of daily choices expressed in a morphology, a way of "
    "dressing, a posture.\n"
    "2. Some candidates for Parliament adorn their electoral prospectus with a "
    "portrait; this presupposes that photography has a power to convert which must be "
    "analysed.\n"
    "3. Inasmuch as photography is an ellipse of language and a condensation of an "
    "'ineffable' social whole, it constitutes an anti-intellectual weapon and tends to "
    "spirit away 'politics' (that is to say a body of problems and solutions) to the "
    "advantage of a 'manner of being', a socio-moral status.\n"
    "4. Photography tends to restore the paternalistic nature of elections, whose "
    "elitist essence has been disrupted by proportional representation and the rule of "
    "parties (The Right seems to use it more than the Left)."))

_g = "cat2025_varc_slot3_rc3"
_p = (
    "Over the course of the twentieth century, humans built, on average, one large dam "
    "a day, hulking structures of steel and concrete designed to control flooding, "
    "facilitate irrigation, and generate electricity. Dams were also lucrative "
    "contracts, large-scale employers, and the physical instantiation of a messianic "
    "drive to conquer territories and control nature. Some of the results of that "
    "drive were charismatic mega-infrastructure-the Hoover on the Colorado River or the "
    "Aswan on the Nile-but most of the tens of thousands of dams that dot the Earth's "
    "landscape have drawn little attention. These are the smaller, though not "
    "inconsequential, barriers that today impede the flow of water on nearly "
    "two-thirds of the world's large waterways. Chances are, what your map calls a "
    "\"lake\" is actually a reservoir, and that thin blue line that emerges from it "
    "once flowed very differently.\n\n"
    "Damming a river is always a partisan act. Even when explicit infrastructure "
    "goals-irrigation, flood control, electrification-were met, other consequences "
    "were significant and often deleterious. Across the world, river control displaced "
    "millions of people, threatening livelihoods, foodways, and cultures. In the "
    "western United States, dams were often an instrument of colonialism, used to "
    "dispossess Indigenous people and subsidize settler agriculture. And as dams "
    "slowed the flow of water, inhibited the movement of nutrients, and increased the "
    "amount of toxic algae and other parasites, they snuffed out entire river "
    "ecologies. Declining fish populations are the most evident effect, but dams also "
    "threaten a host of other animals-from birds and reptiles to fungi and "
    "plants-with extinction. Every major dam, then, is also a sacrifice zone, a place "
    "where lives, livelihoods, and ways of life are eliminated so that new sorts of "
    "landscapes can support water-intensive agriculture and cities that sprout "
    "downstream of new reservoirs.\n\n"
    "Such sacrifices have been justified as offerings at the temples of modernity. "
    "Justified by-and for-whom, though? Over the course of the twentieth century, "
    "rarely were the costs and benefits weighed thoughtfully and decided "
    "democratically. As Kader Asmal, chair of the landmark 2000 World Commission on "
    "Dams, concluded, \"There have been precious few, if any, comprehensive, "
    "independent analyses as to why dams came about, how dams perform over time, and "
    "whether we are getting a fair return from our 2 trillion Dollar investment.\" A "
    "quarter-century later, Asmal's words ring ever truer. A litany of dams built in "
    "the mid-twentieth century are approaching the end of their expected lives, with "
    "worrying prospects for their durability. Droughts, magnified and multiplied by "
    "the effects of climate change, have forced more and more to run below capacity. "
    "If ever there were a time to rethink the mania for dams, it would be now.\n\n"
    "There is some evidence that a combination of opposition, alternative energy "
    "sources, and a lack of viable projects has slowed the construction of major dams. "
    "But a wave of recent and ongoing construction, from India and China to Ethiopia "
    "and Canada, continues to tilt the global balance firmly in favor of water "
    "impoundment."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Dams & Displacement", "MCQ",
      "What does the author wish to communicate by referring to the Hoover and Aswan "
      "dams in the first paragraph?",
      ["The Colorado and Nile rivers may be seen as thin blue lines on a map.",
       "The designers and builders of these mega-structures were highly charismatic "
       "individuals.",
       "The drive to control nature is evident not only in mega-infrastructures like "
       "the Hoover and Aswan dams, but in smaller dams as well.",
       "By building dams like the Hoover and Aswan dams, large-scale employers became "
       "messianic figures."], _p),
    q(_g, _slot, "Reading Comprehension - Dams & Displacement", "MCQ",
      "The word \"instantiation\" is used in the first paragraph. Which one of the "
      "following pairs of terms would be the best substitute for it in the context of "
      "its usage in the paragraph?",
      ["Exemplification and manifestation", "Development and construction",
       "Durability and timeliness", "Concreteness and viability"], _p),
    q(_g, _slot, "Reading Comprehension - Dams & Displacement", "MCQ",
      "All of the following statements may be considered valid inferences from the "
      "passage EXCEPT that:",
      ["Despite increasing evidence of opposition to dams as well as alternatives to "
       "them, they continue to be built.",
       "Dam-building has proved to be an extremely costly enterprise that may not be "
       "justifiable.",
       "Processes of colonisation have used dam-building to make people vacate their "
       "territories.",
       "Smaller, though not inconsequential, dams are safer than large dam projects."],
      _p),
    q(_g, _slot, "Reading Comprehension - Dams & Displacement", "MCQ",
      "Which one of the following sets of terms is closest to mapping the key "
      "arguments of the passage?",
      ["Mega-infrastructure - Sacrifice zone - Worshipping modernity - Water "
       "impoundment",
       "Partisan act - Threatened livelihoods - Toxic algae - Quarter century",
       "Lucrative contracts - Sacrifice zone - Expected lives - Global balance",
       "Physical instantiation - Partisan act - Decided democratically - Alternative "
       "energy"], _p),
]

_g = "cat2025_varc_slot3_rc4"
_p = (
    "Once a society accepts a secular mode of creativity, within which the creator "
    "replaces God, imaginative transactions assume a self-conscious form. The tribal "
    "imagination, on the other hand, is still to a large extent dreamlike and "
    "hallucinatory. It admits fusion between various planes of existence and levels of "
    "time in a natural and artless manner. In tribal stories, oceans fly in the sky as "
    "birds, mountains swim in water as fish, animals speak as humans and stars grow "
    "like plants. Spatial order and temporal sequence do not restrict the narrative. "
    "This is not to say that tribal creations have no conventions or rules, but simply "
    "that they admit the principle of association between emotion and the narrative "
    "motif. Thus stars, seas, mountains, trees, men and animals can be angry, sad or "
    "happy.\n\n"
    "It might be said that tribal artists work more on the basis of their racial and "
    "sensory memory than on the basis of a cultivated imagination. In order to "
    "understand this distinction, we must understand the difference between "
    "imagination and memory. In the animate world, consciousness meets two immediate "
    "material realities: space and time. We put meaning into space by perceiving it in "
    "terms of images. The image-making faculty is a genetic gift to the human mind-this "
    "power of imagination helps us understand the space that envelops us. With regard "
    "to time, we make connections with the help of memory; one remembers being the "
    "same person today as one was yesterday.\n\n"
    "The tribal mind has a more acute sense of time than the sense of space. Somewhere "
    "along the history of human civilization, tribal communities seem to have realized "
    "that domination over territorial space was not their lot. Thus, they seem to have "
    "turned almost obsessively to gaining domination over time. This urge is "
    "substantiated in their ritual of conversing with their dead ancestors: year after "
    "year, tribals in many parts of India worship terracotta or carved-wood objects "
    "representing their ancestors, aspiring to enter a trance in which they can "
    "converse with the dead. Over the centuries, an amazingly sharp memory has helped "
    "tribals classify material and natural objects into a highly complex system of "
    "knowledge. . .\n\n"
    "One of the main characteristics of the tribal arts is their distinct manner of "
    "constructing space and imagery, which might be described as 'hallucinary'. In "
    "both oral and visual forms of representation, tribal artists seem to interpret "
    "verbal or pictorial art as demarcated by an extremely flexible 'frame'. The "
    "boundaries between art and non-art become almost invisible. A tribal epic can "
    "begin its narration from a trivial everyday event; tribal paintings merge with "
    "living space as if the two were one and the same. And within the narrative "
    "itself, or within the painted imagery, there is no deliberate attempt to follow a "
    "sequence. The episodes retold and the images created take on the apparently "
    "chaotic shapes of dreams. In a way, the syntax of language and the grammar of "
    "painting are the same, as if literature were painted words and painting were a "
    "song of images."
)
QUESTIONS += [
    q(_g, _slot, "Reading Comprehension - Tribal Imagination", "MCQ",
      "Non-human living forms exhibit human emotions in tribal narratives because "
      "tribal narratives:",
      ["accommodate existential fluidity.", "abandon all rules and regulations.",
       "have a self-conscious form.", "are rudimentary and underdeveloped."], _p),
    q(_g, _slot, "Reading Comprehension - Tribal Imagination", "MCQ",
      "On the basis of the passage, which one of the following explains the main "
      "difference between imagination and memory?",
      ["Imagination helps humans make sense of space while memory helps them "
       "understand time.",
       "Tribal groups value memory over imagination when it comes to creating art and "
       "literature.",
       "Imagination needs to be cultivated whereas memory is more intuitive because it "
       "is racial and sensory.",
       "Imagination is a genetic gift to humans whereas memory is central to human "
       "consciousness."], _p),
    q(_g, _slot, "Reading Comprehension - Tribal Imagination", "MCQ",
      "All of the following statements may be considered valid inferences from the "
      "passage EXCEPT that:",
      ["Tribal art excludes the depiction of the mundane reality of everyday life and "
       "objects.",
       "Shamanic rituals involving conversing with the dead often feature in tribal "
       "stories.",
       "Tribal narratives exhibit a chronological beginning, middle, and end.",
       "Tribal stories depict the natural world in accordance with rational scientific "
       "knowledge."], _p),
    q(_g, _slot, "Reading Comprehension - Tribal Imagination", "MCQ",
      "Which one of the following best explains why tribals in India worship their "
      "dead ancestors?",
      ["Tribals seek territorial domination over the spaces that they inhabit.",
       "For tribals, conversing with the dead becomes a way of seeking control over "
       "time.",
       "Tribals show respect to their ancestors through terracotta and carved-wood "
       "objects.",
       "Tribals possess a sophisticated knowledge system that is based on memory."],
      _p),
]

QUESTIONS.append(q(None, _slot, "RC Summary", "MCQ",
    "The passage given below is followed by four summaries. Choose the option that best "
    "captures the essence of the passage.\n"
    "In investigating memory-beliefs, there are certain points which must be borne in "
    "mind. In the first place, everything constituting a memory-belief is happening "
    "now, not in that past time to which the belief is said to refer. It is not "
    "logically necessary to the existence of a memory-belief that the event remembered "
    "should have occurred, or even that the past should have existed at all. There is "
    "no logical impossibility in the hypothesis that the world sprang into being five "
    "minutes ago, exactly as it then was, with a population that \"remembered\" a "
    "wholly unreal past. There is no logically necessary connection between events at "
    "different times; therefore nothing that is happening now or will happen in the "
    "future can disprove the hypothesis that the world began five minutes ago. Hence "
    "the occurrences which are CALLED knowledge of the past are logically independent "
    "of the past; they are wholly analysable into present contents, which might, "
    "theoretically, be just what they are even if no past had existed.",
    ["When we discuss the concept of memory-beliefs, we must understand that it is not "
     "logically impossible for the event remembered to have never happened at all; it "
     "could just be a figment of our imagination.",
     "Memory-beliefs depend wholly on what is remembered in the present, and not on "
     "anything else; just as it is not logically impossible that the world came into "
     "being five minutes ago, and that everyone now just remembers a wholly imaginary "
     "past for it.",
     "When investigating memory beliefs, we must keep in mind that an actual past "
     "event is not a prerequisite for a memory-belief to exist, and that what we know "
     "of the past could theoretically need a past at all.",
     "That which we call \"knowledge of the past\" is logically independent of the "
     "past, since the act of remembering which forms memory-beliefs happens in the "
     "present, and does not need to be based in real past occurrences, or even need a "
     "past at all."]))


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = (
            db.query(CatQuestion)
            .filter(CatQuestion.source_year == SOURCE_YEAR, CatQuestion.section == "VARC")
            .count()
        )
        if existing > 0:
            print(f"CAT 2025 VARC PYQs already seeded ({existing} rows); skipping.")
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
        num_groups = len({item["group_id"] for item in QUESTIONS if item["group_id"]})
        print(f"Seeded {len(QUESTIONS)} CAT 2025 VARC PYQ questions across {num_groups} RC sets.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

"""Seed real CAT 2024 VARC questions, all 3 slots, retyped from the official
question papers in pyq-source/2024/. Reading-comprehension questions are
grouped by shared passage via `group_id` + `passage_text`, same convention
as prior years; standalone VA questions (odd-sentence-out, para-summary,
sentence-insertion) get `group_id=None`, full passage embedded directly in
`question_text` (matching the 2025 VARC convention for these types).

`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

Source: the combined `_SOLUTIONS.pdf` files (VARC_SLOTn_CAT_2024_SOLUTIONS.pdf),
which embed full verbatim question text before each worked solution. Slot 1
is confirmed 24 questions (matches its own instructions page exactly: 4 RC
passages x 4 sub-questions = 16, plus 8 standalone VA questions = 24).

Run with:
    python -m app.scripts.seed_cat_pyq_2024_varc
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024


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

_g = "cat2024_varc_slot1_rc1"
_passage = (
    "In the summer of 2022, subscribers to the US streaming service HBO MAX were "
    "alarmed to discover that dozens of the platform's offerings - from the Covid-themed "
    "heist thriller Locked Down to the recent remake of The Witches - had been quietly "
    "removed from the service . . . The news seemed like vindication to those who had "
    "long warned that streaming was more about controlling access to the cultural commons "
    "than expanding it, as did reports (since denied by the show's creators) that Netflix "
    "had begun editing old episodes of Stranger Things to retroactively improve their "
    "visual effects.\n\n"
    "What's less clear is whether the commonly prescribed cure for these cultural ills - "
    "a return to the material pleasures of physical media - is the right one. While the "
    "makers of Blu-ray discs claim they have a shelf life of 100 years, such statistics "
    "remain largely theoretical until they come to pass, and are dependent on storage "
    "conditions, not to mention the continued availability of playback equipment. The "
    "humble DVD has already proved far less resilient, with many early releases already "
    "beginning to deteriorate in quality. Digital movie purchases provide even less "
    "security. Any film \"bought\" on iTunes could disappear if you move to another "
    "territory with a different rights agreement and try to redownload it. It's a bold "
    "new frontier in the commodification of art: the birth of the product recall. After a "
    "man took to Twitter to bemoan losing access to Cars 2 after moving from Canada to "
    "Australia, Apple clarified that users who downloaded films to their devices would "
    "retain permanent access to those downloads, even if they relocated to a hemisphere "
    "where the [content was] subject to a different set of rights agreements. Thanks to "
    "the company's ironclad digital rights management technology, however, such files "
    "cannot be moved or backed up, locking you into watching with your Apple account.\n\n"
    "Anyone who does manage to acquire Digital Rights Management free (DRM-free) copies "
    "of their favourite films must nonetheless grapple with ever-changing file format "
    "standards, not to mention data decay - the gradual process by which electronic "
    "information slowly but surely corrupts. Only the regular migration of files from "
    "hard drive to hard drive can delay the inevitable, in a sisyphean battle against the "
    "ravages of digital time.\n\n"
    "In a sense, none of this is new. Charlie Chaplin burned the negative of his 1926 "
    "film A Woman of the Sea as a tax write-off. Many more films have been lost through "
    "accident, negligence or plain indifference. During a heatwave in July 1937, a Fox "
    "film vault in New Jersey burned down, destroying a majority of the silent films "
    "produced by the studio.\n\n"
    "Back then, at least, cinema was defined by its ephemerality: the sense that a film "
    "was as good as gone once it left your local cinema. Today, with film studios keen to "
    "stress the breadth of their back catalogues (or to put in Hollywood terms, the value "
    "of their IPs), audiences may start to wonder why those same studios seem happy to set "
    "the vault alight themselves if it'll help next quarter's numbers."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - digital media preservation", "MCQ",
         "Which one of the following statements about art best captures the arguments made "
         "in the passage?",
         ["In the age of online subscription services, it is time to change our "
          "understanding of classic works of art being primarily immutable and easily "
          "available to the public.",
          "Accepting retroactive changes to works of art is dangerous because it will "
          "encourage creators to not put enough effort into the original attempt, given "
          "that they can always edit or update their work later.",
          "Works of art belong to the cultural commons and hence must remain available in "
          "perpetuity, irrespective of who pays for access to them.",
          "As art is increasingly created, stored and distributed digitally, access to it "
          "is counterintuitively likely to be made more difficult by the rapid churn in "
          "technology and the whims of host platforms."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - digital media preservation", "MCQ",
         "“Netflix had begun editing old episodes of Stranger Things to retroactively "
         "improve their visual effects.” What is the purpose of this example used in the "
         "passage?",
         ["To show a practice that justifies the fears of people who feel streaming "
          "services cannot be trusted to be custodians of cultural artefacts like film.",
          "To show that streaming services are controlling access to the cultural commons "
          "rather than expanding it.",
          "To show how unsubstantiated reports are leading to an increase in the level of "
          "distrust towards streaming services.",
          "To show that art in the digital age, specifically film, is no longer sacrosanct, "
          "and may be changed to suit changing tastes or technology."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - digital media preservation", "MCQ",
         "Which one of the following statements, if true, would best invalidate the main "
         "argument of the passage?",
         ["Improved cloud storage services have made it possible for movie collections to "
          "now be preserved in perpetuity, without the need to keep migrating the files.",
          "When moving to a different geographical location, customers can easily use "
          "Virtual Private Networks (VPNs) to bypass geo-blocking and regain access to "
          "their content on any streaming service.",
          "Recent research has irrefutably proven that Blu-Ray discs have a shelf life of "
          "at least 100 years.",
          "Studios and streaming services have committed to giving customers perpetual and "
          "platform independent access to the original digital content they have paid "
          "for."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - digital media preservation", "MCQ",
         "Which of the following statements is suggested by the sentence “Back then, at "
         "least, cinema was defined by its ephemerality: the sense that a film was as good "
         "as gone once it left your local cinema”?",
         ["Cinema is now no longer as ephemeral as it used to be earlier, because the "
          "technology used for creating and preserving films has improved manifold.",
          "Presently, there is no reason why film studios should remove access to films "
          "once they have left the local cinema.",
          "Today, films are expected to be available for a long time, since they are no "
          "longer tied solely to their stay at the local cinema.",
          "Around a century ago, people were more accepting of not having access to films "
          "once they left the local cinema."]), "passage": _passage},
]

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled up sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the odd "
    "sentence and key in the number of that sentence as your answer.\n"
    "1. Urbanites also have more and better options for getting around: Uber is "
    "ubiquitous; easy-to-rent dockless bicycles are spreading; battery-powered scooters "
    "will be next.\n"
    "2. When more people use buses or trains the service usually improves because "
    "public-transport agencies run more buses and trains.\n"
    "3. Worsening services on public transport, terrorist attacks in some urban metros and "
    "a rise in fares have been blamed for this trend.\n"
    "4. It seems more likely that public transport is being squeezed structurally as "
    "people's need to travel is diminishing as a result of smartphones, video "
    "conferencing, online shopping and so on.\n"
    "5. There has been a puzzling decline in the use of urban public transport in many "
    "countries in the west, despite the growth in urban populations and rising "
    "employment."))

_g = "cat2024_varc_slot1_rc2"
_passage = (
    ". . . [T]he idea of craftsmanship is not simply nostalgic. . . . Crafts require "
    "distinct skills, an all round approach to work that involves the whole product, "
    "rather than individual parts, and an attitude that necessitates devotion to the job "
    "and a focus on the communal interest. The concept of craft emphasises the human touch "
    "and individual judgment.\n\n"
    "Essentially, the crafts concept seems to run against the preponderant ethos of "
    "management studies which, as the academics note, have long prioritised efficiency "
    "and consistency. . . . Craft skills were portrayed as being primitive and "
    "traditionalist.\n\n"
    "The contrast between artisanship and efficiency first came to the fore in the 19th "
    "century when British manufacturers suddenly faced competition from across the "
    "Atlantic as firms developed the “American system” using standardised parts. . . . the "
    "worldwide success of the Singer sewing machine showed the potential of a "
    "mass-produced device. This process created its own reaction, first in the form of "
    "the Arts and Crafts movement of the late 19th century, and then again in the “small "
    "is beautiful” movement of the 1970s. A third crafts movement is emerging as people "
    "become aware of the environmental impact of conventional industry.\n\n"
    "There are two potential markets for those who practise crafts. The first stems from "
    "the existence of consumers who are willing to pay a premium price for goods that are "
    "deemed to be of extra quality. . . . The second market lies in those consumers who "
    "wish to use their purchases to support local workers, or to reduce their "
    "environmental impact by taking goods to craftspeople to be mended, or recycled.\n\n"
    "For workers, the appeal of craftsmanship is that it allows them the autonomy to make "
    "creative choices, and thus makes a job far more satisfying. In that sense, it could "
    "offer hope for the overall labour market. Let the machines automate dull and "
    "repetitive tasks and let workers focus purely on their skills, judgment and "
    "imagination. As a current example, the academics cite the “agile” manifesto in the "
    "software sector, an industry at the heart of technological change. The pioneers "
    "behind the original agile manifesto promised to prioritise “individuals and "
    "interactions over processes and tools”. By bringing together experts from different "
    "teams, agile working is designed to improve creativity.\n\n"
    "But the broader question is whether crafts can create a lot more jobs than they do "
    "today. Demand for crafted products may rise but will it be easy to retrain workers in "
    "sectors that might get automated (such as truck drivers) to take advantage? In a "
    "world where products and services often have to pass through regulatory hoops, large "
    "companies will usually have the advantage.\n\n"
    "History also suggests that the link between crafts and creativity is not automatic. "
    "Medieval craft guilds were monopolies which resisted new entrants. They were also "
    "highly hierarchical with young men required to spend long periods as apprentices and "
    "journeymen before they could set up on their own; by that time the innovative spirit "
    "may have been knocked out of them. Craft workers can thrive in the modern era, but "
    "only if they don't get too organised."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - craftsmanship vs mass production", "MCQ",
         "The author questions the ability of crafts to create substantial employment "
         "opportunities presently because",
         ["the low scale of crafts production will not be able to absorb the mass of "
          "redundant labour.",
          "regulatory requirements could make it difficult for small crafts outfits to "
          "compete.",
          "workers made redundant by automation are unlikely to opt for crafts-related "
          "work.",
          "crafts guilds tend to resist new entrants and are unlikely to accept large "
          "numbers of trainees."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - craftsmanship vs mass production", "MCQ",
         "We can infer from the passage that medieval crafts guilds resembled mass "
         "production in that both",
         ["did not necessarily promote creativity.",
          "did not always employ egalitarian production processes.",
          "focused excessively on product quality.",
          "discouraged innovation by restricting entry through strict rules."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - craftsmanship vs mass production", "MCQ",
         "The most recent revival of interest in the crafts is a result of the emergence of "
         "all of the following EXCEPT:",
         ["a greater interest in buying locally produced goods.",
          "concerns about the environmental impact of mass production.",
          "support for individual creations as opposed to mass-produced objects.",
          "a niche market for discerning buyers of quality products."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - craftsmanship vs mass production", "MCQ",
         "Which one of the following statements is NOT inconsistent with the views stated "
         "in the passage?",
         ["The Arts and Crafts movement was initially inspired by the “American system” of "
          "production.",
          "We need to support the crafts; only then can we retain the creativity intrinsic "
          "to their production.",
          "The agile movement in software is a throwback to the tenets of the medieval "
          "crafts guilds.",
          "Creativity in the crafts could be stifled if the market for artisan goods "
          "becomes too organised."]), "passage": _passage},
]

QUESTIONS.append(q(None, _slot, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "Scientific research shows that many animals are very intelligent and have sensory "
    "and motor abilities that dwarf ours. Dogs are able to detect diseases such as cancer "
    "and diabetes and warn humans of impending heart attacks and strokes. Elephants, "
    "whales, hippopotamuses, giraffes, and alligators use low-frequency sounds to "
    "communicate over long distances, often miles. Many animals also display wide-ranging "
    "emotions, including joy, happiness, empathy, compassion, grief, and even resentment "
    "and embarrassment. It's not surprising that animals share many emotions with us "
    "because we also share brain structures, located in the limbic system, that are the "
    "seat of our emotions.",
    ["Animals are more intelligent than us in sensing danger and detecting diseases.",
     "The similarity in brain structure explains why animals show emotions typically "
     "associated with humans.",
     "Animals can show emotions which are typically associated with humans.",
     "The advanced sensory and motor abilities of animals is the reason why they can "
     "display wide-ranging emotions."]))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph and "
    "decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: Understanding central Asia's role helps developments make more sense not "
    "only across Asia but in Europe, the Americas and Africa.\n"
    "Paragraph: The nations of the Silk Roads are sometimes called 'developing countries', "
    "but they are actually some of the world's most highly developed countries, the very "
    "crossroads of civilization, in advanced states of disrepair. ___(1)___. These "
    "countries lie at the centre of global affairs: they have since the beginning of "
    "history. Running across the spine of Asia, they form a web of connections fanning out "
    "in every direction, routes along which pilgrims and warriors, nomads and merchants "
    "have travelled, goods and produce have been bought and sold, and ideas exchanged, "
    "adapted and refined. ___(2)___. They have carried not only prosperity, but also death "
    "and violence, disease and disaster. ___(3)___. The Silk Roads are the world's central "
    "nervous system, connecting otherwise far-flung peoples and places…. ___(4)___. It "
    "allows us to see patterns and links, causes and effects that remain invisible if one "
    "looks only at Europe, or North America.",
    ["Option 1", "Option 2", "Option 4", "Option 3"]))

QUESTIONS.append(q(None, _slot, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "Cartographers design and create maps to communicate information about phenomena "
    "located somewhere on our planet. In the past, cartographers did not worry too much "
    "about who was going to read their maps. Although some simple “usability” research "
    "was done—like comparing whether circle or bar symbols worked best—cartographers knew "
    "how to make maps. This has changed now, however, due to all kinds of societal and "
    "technological developments. Today, map readers are more demanding—mostly because of "
    "the tools they use to read maps. Cartographers, who are also influenced by these "
    "trends, are now more interested in seeing if their products are efficient, "
    "effective, and appreciated.",
    ["Today, cartographers also need to look into the usability of maps because of the "
     "new technological developments.",
     "New technological developments have prompted cartographers to experiment with their "
     "maps by applying these new innovations.",
     "Maps are being used for a variety of reasons and therefore map readers have become "
     "more demanding.",
     "Modern mapmakers evaluate a map's effectiveness efficiency and satisfaction of the "
     "user through a series of experiments."]))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph and "
    "decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: The brain isn't organized the way you might set up your home office or "
    "bathroom medicine cabinet.\n"
    "Paragraph: ___(1)___. You can't just put things anywhere you want to. The evolved "
    "architecture of the brain is haphazard and disjointed, and incorporates multiple "
    "systems, each of which has a mind of its own. ___(2)___. Evolution doesn't design "
    "things and it doesn't build systems—it settles on systems that, historically, "
    "conveyed a survival benefit. There is no overarching, grand planner engineering the "
    "systems so that they work harmoniously together. ___(3)___. The brain is more like a "
    "big, old house with piecemeal renovations done on every floor, and less like new "
    "construction. ___(4)___.",
    ["Option 2", "Option 4", "Option 1", "Option 3"]))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph and "
    "decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: Comprehending a wide range of emotions, Renaissance music nevertheless "
    "portrayed all emotions in a balanced and moderate fashion.\n"
    "Paragraph: A volume of translated Italian madrigals were published in London during "
    "the year of 1588. This sudden public interest facilitated a surge of English Madrigal "
    "writing as well as a spurt of other secular music writing and publication. ___(1)___. "
    "This music boom lasted for thirty years and was as much a golden age of music as "
    "British literature was with Shakespeare and Queen Elizabeth I. ___(2)___. The rebirth "
    "in both literature and music originated in Italy and migrated to England; the English "
    "madrigal became more humorous and lighter in England as compared to Italy. "
    "Renaissance music was mostly polyphonic in texture. ___(3)___. Extreme use of and "
    "contrasts in dynamics, rhythm, and tone colour do not occur. ___(4)___. The rhythms "
    "in Renaissance music tend to have a smooth, soft flow instead of a sharp, "
    "well-defined pulse of accents.",
    ["Option 1", "Option 2", "Option 3", "Option 4"]))

_g = "cat2024_varc_slot1_rc3"
_passage = (
    "Oftentimes, when economists cross borders, they are less interested in learning from "
    "others than in invading their garden plots. Gary Becker, for instance, pioneered the "
    "idea of human capital. To do so, he famously tackled topics like crime and "
    "domesticity, applying methods honed in the study of markets to domains of nonmarket "
    "life. He projected economics outward into new realms: for example, by revealing the "
    "extent to which humans calculate marginal utilities when choosing their spouses or "
    "stealing from neighbors. At the same time, he did not let other ways of thinking "
    "enter his own economic realm: for example, he did not borrow from anthropology or "
    "history or let observations of nonmarket economics inform his homo economicus. Becker "
    "was a picture of the imperial economist in the heyday of the discipline's bravura. "
    "Times have changed for the once almighty discipline. Economics has been taken to "
    "task, within and beyond its ramparts. Some economists have reached out, imported, "
    "borrowed, and collaborated—been less imperial, more open. Consider Thomas Piketty "
    "and his outreach to historians. The booming field of behavioral economics—the fusion "
    "of economics and social psychology—is another case. Having spawned active subfields, "
    "like judgment, decision making and a turn to experimentation, the field aims to go "
    "beyond the caricature of Rational Man to explain how humans make decisions…. It is "
    "important to underscore how this flips the way we think about economics. For "
    "generations, economists have presumed that people have interests—“preferences,” in "
    "the neoclassical argot—that get revealed in the course of peoples' choices. Interests "
    "come before actions and determine them. If you are hungry, you buy lunch; if you are "
    "cold, you get a sweater. If you only have so much money and can't afford to deal with "
    "both your growling stomach and your shivering, which need you choose to meet using "
    "your scarce savings reveals your preference. Psychologists take one look at this "
    "simple formulation and shake their heads. Increasingly, even some mainstream "
    "economists have to admit that homo economicus doesn't always behave like the "
    "textbook maximizer; irrational behavior can't simply be waved away as extra economic "
    "expressions of passions over interests, and thus the domain of other disciplines…. "
    "This is one place where the humanist can help the economist. If narrative economics "
    "is going to help us understand how rivals duke it out, who wins and who loses, we are "
    "going to need much more than lessons from epidemiological studies of viruses or "
    "intracranial stimuli. Above all, we need politics and institutions. Shiller [the "
    "Nobel prize winning economist] connects perceptions of narratives to changes in "
    "behavior and thence to social outcomes. He completes a circle that was key to "
    "behavioral economics and brings in storytelling to make sense of how perceptions get "
    "framed. This cycle (perception to behavior to society) was once mediated or "
    "dominated by institutions: the political parties, lobby groups, and media "
    "organizations that played a vital role in legitimating, representing, and excluding "
    "interests. Yet institutions have been stripped from Shiller's account, to reveal a "
    "bare dynamic of emotions and economics, without the intermediating place of politics."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - economics and interdisciplinarity", "MCQ",
         "We can infer from the passage that the term “homo economicus” refers to someone "
         "who",
         ["believes in borrowing and collaborating with other disciplines in their work.",
          "maximises their opportunities based on nonmarket choices.",
          "makes rational decisions based on their own preferences.",
          "is not influenced by the preferences and choices of others."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - economics and interdisciplinarity", "MCQ",
         "“Times have changed for the once almighty discipline.” We can infer from this "
         "statement and the associated paragraph that the author is being",
         ["sarcastic about how economists, who earlier shunned other disciplines, are now "
          "beginning to incorporate them in their analyses.",
          "critical of economists' openly borrowing and collaborating across disciplines "
          "to explain how humans make decisions.",
          "disparaging of economists' inability to precisely predict market behaviour, and "
          "are now borrowing from other disciplines to remedy this.",
          "judgemental about the ability of economic tools to accurately manage crises "
          "leading to the downfall of this lofty science."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - economics and interdisciplinarity", "MCQ",
         "In the first paragraph the author is making the point that economists like "
         "Becker",
         ["benefitted from the application of their principles and concepts to "
          "non-economic phenomena.",
          "used economics to analyse non-market behaviour, without incorporating "
          "perspectives from other areas of inquiry.",
          "tended to guard their discipline from poaching by academics from other subject "
          "areas.",
          "had begun to borrow concepts from other disciplines but were averse to the "
          "latter applying economic principles."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - economics and interdisciplinarity", "MCQ",
         "The author critiques Schiller's approach to behavioural economics for",
         ["linking emotions and rational behaviour without considering the mediation of "
          "social institutions.",
          "denigrating the role of institutions while creating a link between behavioural "
          "economics and perceptions.",
          "relying excessively on storytelling as the main influence on the formation of "
          "perceptions.",
          "ignoring the marginal role that media and politics play in influencing people's "
          "behaviour."]), "passage": _passage},
]

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled up sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence and key in the number of that sentence as your answer.\n"
    "1. Animals have an interest in fulfilling their basic needs, but also in avoiding "
    "suffering, and thus we ought to extend moral consideration.\n"
    "2. Singer viewed himself as a utilitarian, and presents a direct moral theory "
    "concerning animal rights, in contrast to indirect positions, such as welfarist "
    "views.\n"
    "3. He argued for extending moral consideration to animals because, similar to "
    "humans, animals have certain significant interests.\n"
    "4. The event that publicly announced animal rights as a legitimate issue within "
    "contemporary philosophy was Peter Singer's Animal Liberation text in 1975.\n"
    "5. As such, we ought to view their interests alongside and equal to human interests, "
    "which results in humans having direct moral duties towards animals."))

QUESTIONS.append(q(None, _slot, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "Certain codes may, of course, be so widely distributed in a specific language "
    "community or culture, and be learned at so early an age, that they appear not to be "
    "constructed – the effect of an articulation between sign and referent – but to be "
    "'naturally' given. Simple visual signs appear to have achieved a 'near-universality' "
    "in this sense: though evidence remains that even apparently 'natural' visual codes "
    "are culture specific. However, this does not mean that no codes have intervened; "
    "rather, that the codes have been profoundly naturalized. The operation of "
    "naturalized codes reveals not the transparency and 'naturalness' of language but the "
    "depth, the habituation and the near-universality of the codes in use. They produce "
    "apparently 'natural' recognitions. This has the (ideological) effect of concealing "
    "the practices of coding which are present.",
    ["All codes, linguistic and visual, have a natural origin but some are so widespread "
     "that they become universal. This is what hides the mechanism of coding behind "
     "signs.",
     "Not all codes are natural but certain codes are naturalized and made to appear "
     "universal. Ideology aims to hide the mechanism of coding behind signs.",
     "Learning linguistic and visual signs at an early age makes all such codes appear "
     "natural. This naturalization of codes is the effect of ideology.",
     "Language and visual signs are codes. However, some of the codes are so widespread "
     "that they not only seem naturally given but also hide the mechanism of coding "
     "behind the signs."]))

_g = "cat2024_varc_slot1_rc4"
_passage = (
    "Landing in Australia, the British colonists weren't much impressed with the "
    "small-bodied, slender-snooted marsupials called bandicoots. “Their muzzle, which is "
    "much too long, gives them an air exceedingly stupid,” one naturalist noted in 1805. "
    "They nicknamed one type the “zebra rat” because of its black-striped rump.\n\n"
    "Silly-looking or not, though, the zebra rat—the smallest bandicoot, more commonly "
    "known today as the western barred bandicoot—exhibited a genius for survival in the "
    "harsh outback, where its ancestors had persisted for some 26 million years. Its "
    "births were triggered by rainfall in the bone-dry desert. It carried its "
    "breath-mint-size babies in a backward-facing pouch so mothers could forage for food "
    "and dig shallow, camouflaged shelters.\n\n"
    "Still, these adaptations did not prepare the western barred bandicoot for the "
    "colonial-era transformation of its ecosystem, particularly the onslaught of imported "
    "British animals, from cattle and rabbits that damaged delicate desert vegetation to "
    "ravenous house cats that soon developed a taste for bandicoots. Several of the "
    "dozen-odd bandicoot species went extinct, and by the 1940s the western barred "
    "bandicoot, whose original range stretched across much of the continent, persisted "
    "only on two predator-free islands in Shark Bay, off Australia's western coast.\n\n"
    "“Our isolated fauna had simply not been exposed to these predators,” says Reece "
    "Pedler, an ecologist with the Wild Deserts conservation program. Now Wild Deserts is "
    "using descendants of those few thousand island survivors, called Shark Bay "
    "bandicoots, in a new effort to seed a mainland bandicoot revival. They've imported 20 "
    "bandicoots to a preserve on the edge of the Strzelecki Desert, in the remote interior "
    "of New South Wales. This sanctuary is a challenging place, desolate much of the year, "
    "with one of the world's most mercurial rainfall patterns—relentless droughts "
    "followed by sudden drenching floods.\n\n"
    "The imported bandicoots occupy two fenced “exclosures,” cleared of invasive rabbits "
    "(courtesy of Pedler's sheepdog) and of feral cats (which slunk off once the rabbits "
    "disappeared). A third fenced area contains the program's Wild Training Zone, where "
    "two other rare marsupials (bilbies, a larger type of bandicoot, and mulgaras, a "
    "somewhat fearsome fuzzball known for sucking the brains out of prey) currently share "
    "terrain with controlled numbers of cats, learning to evade them. It's unclear whether "
    "the Shark Bay bandicoots, which are perhaps even more predator-naive than their "
    "now-extinct mainland bandicoot kin, will be able to make that kind of breakthrough.\n\n"
    "For now, though, a recent surge of rainfall has led to a bandicoot joey boom, raising "
    "the Wild Deserts population to about 100, with other sanctuaries adding to that "
    "number. There are also signs of rebirth in the landscape itself. With their constant "
    "digging, the bandicoots trap moisture and allow for seed germination so the "
    "cattle-damaged desert can restore itself.\n\n"
    "They have a new nickname—a flattering one, this time. “We call them ecosystem "
    "engineers,” Pedler says."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - bandicoot conservation", "MCQ",
         "Which one of the following options does NOT represent the characteristics of "
         "the western barred bandicoot?",
         ["Long thin nose, black striped back, pouch for joeys",
          "Shallow diggers having an elongated muzzle",
          "Smallest black striped marsupial that uses camouflage and dig",
          "Look of a rat but with a baby pouch and a slender snout"]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - bandicoot conservation", "MCQ",
         "The text uses the word 'exclosures' because Wild Deserts has adopted a measure "
         "of",
         ["restoring cattle damaged deserts to green landscapes.",
          "excluding animals to make the islands predator-free.",
          "barring the entry of invasive species.",
          "ridding the main desert of feral cats and large bilbies."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - bandicoot conservation", "MCQ",
         "Which one of the following statements provides a gist of this passage?",
         ["The onslaught of animals, such as cattle, rabbits and housecats, brought in by "
          "the British led to the extinction of the western barred bandicoot",
          "The negligent attitude of the British colonists towards these bandicoots "
          "evidenced by the names given to them led to their annihilation.",
          "A type of bandicoots was nearly wiped out by invasive species but rescuers now "
          "pin hopes on a remnant island population.",
          "Marsupials are going extinct due to the colonial era transformation of the "
          "ecosystem which also destroyed natural vegetation."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - bandicoot conservation", "MCQ",
         "According to the text, the western barred bandicoots now have a flattering name "
         "because they have",
         ["aided in altering an arid environment.",
          "led a revival in preserving the species.",
          "led to a surge and increase of rainfall.",
          "grown fivefold in terms of population."]), "passage": _passage},
]


# ============================================================ SLOT 2 ====
_slot = "slot2"

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled up sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence and key in the number of that sentence as your answer.\n"
    "1. The UK is a world leader in developing cultivated meat and the approval of a "
    "cultivated pet food is an important milestone.\n"
    "2. If we're to realise the full potential benefits of cultivated meat the government "
    "must invest in research and infrastructure.\n"
    "3. The first UK applications for cultivated meat produced for humans remain under "
    "assessment with the Food Standards Agency.\n"
    "4. The previous UK government had been looking at fast-tracking the approval of "
    "cultivated meat for human consumption."))

_g = "cat2024_varc_slot2_rc1"
_passage = (
    "The history of any major technological or industrial advance is inevitably shadowed "
    "by a less predictable history of unintended consequences and secondary effects — "
    "what economists sometimes call “externalities.” Sometimes those consequences are "
    "innocuous ones, or even beneficial. Gutenberg invents the printing press, and "
    "literacy rates rise, which causes a significant part of the reading public to "
    "require spectacles for the first time, which creates a surge of investment in "
    "lens-making across Europe, which leads to the invention of the telescope and the "
    "microscope.\n\n"
    "Oftentimes the secondary effects seem to belong to an entirely different sphere of "
    "society. When Willis Carrier hit upon the idea of air-conditioning, the technology "
    "was primarily intended for industrial use: ensuring cool, dry air for factories that "
    "required low-humidity environments. But…it touched off one of the largest "
    "migrations in the history of the United States, enabling the rise of metropolitan "
    "areas like Phoenix and Las Vegas that barely existed when Carrier first started "
    "tinkering with the idea in the early 1900s.\n\n"
    "Sometimes the unintended consequence comes about when consumers use an invention in "
    "a surprising way. Edison famously thought his phonograph, which he sometimes called "
    "“the talking machine,” would primarily be used to take dictation….But then later "
    "innovators… discovered a much larger audience willing to pay for musical recordings "
    "made on descendants of Edison's original invention. In other cases, the original "
    "innovation comes into the world disguised as a plaything…the way the animatronic "
    "dolls of the mid-1700s inspired Jacquard to invent the first “programmable” loom and "
    "Charles Babbage to invent the first machine that fit the modern definition of a "
    "computer, setting the stage for the revolution in programmable technology that "
    "would transform the 21st century in countless ways.\n\n"
    "We live under the gathering storm of modern history's most momentous unintended "
    "consequence….carbon-based climate change. Imagine the vast sweep of inventors whose "
    "ideas started the Industrial Revolution, all the entrepreneurs and scientists and "
    "hobbyists who had a hand in bringing it about. Line up a thousand of them and ask "
    "them all what they had been hoping to do with their work. Not one would say that "
    "their intent had been to deposit enough carbon in the atmosphere to create a "
    "greenhouse effect that trapped heat at the surface of the planet. And yet here we "
    "are.\n\n"
    "Ethyl (leaded fuel) and Freon belonged to the same general class of secondary "
    "effect: innovations whose unintended consequences stem from some kind of waste "
    "by-product that they emit. But the potential health threats of Ethyl (unleaded "
    "fuel) were visible in the 1920s, unlike, say, the long-term effects of atmospheric "
    "carbon build up in the early days of the Industrial Revolution….\n\n"
    "Indeed, it is reasonable to see CFCs (chlorofluorocarbons) as a forerunner of the "
    "kind of threat we will most likely face in the coming decades, as it becomes "
    "increasingly possible for individuals or small groups to create new scientific "
    "advances — through chemistry or biotechnology or materials science — setting off "
    "unintended consequences that reverberate on a global scale."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - unintended consequences of technology", "MCQ",
         "The author lists all of the following examples as “externalities” of major "
         "technical advances EXCEPT:",
         ["extension of the phonograph to large-scale recording of music",
          "application of the Jacquard loom to modern IT programming",
          "build-up of chlorofluorocarbons in the atmosphere",
          "cooling and de-humidifying of factories through air-conditioning"]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - unintended consequences of technology", "MCQ",
         "Carrier, Babbage, and Edison are mentioned in the passage to illustrate the "
         "author's point that",
         ["the secondary effect of past inventions mostly resulted in the creation of new "
          "inventions.",
          "inventions typically end up being used for entirely different purposes than "
          "the intended ones.",
          "despite the original intention, the unintended consequences of their "
          "inventions were largely beneficial.",
          "these inventors could not have visualised the eventual impact of their "
          "inventions on society."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - unintended consequences of technology", "MCQ",
         "We can assume that the author would support all of the following views EXCEPT:",
         ["The by-products of leaded fuel, rather than the fuel itself, were responsible "
          "for the build-up of carbon-related gases in the atmosphere.",
          "The emissions caused by the large-scale use of leaded fuel ought to have been "
          "addressed earlier than they were.",
          "While technological advances in the past have had innocuous or beneficial "
          "outcomes, more recent advances have the potential to be more threatening "
          "globally.",
          "It has become far easier for people today to bring out innovations with dire "
          "worldwide consequences than it was earlier."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - unintended consequences of technology", "MCQ",
         "Which of the following best conveys the main point of the first paragraph?",
         ["The full impact of technological advances cannot be estimated in the short run "
          "as the ripple effects often extend far beyond the original intent.",
          "The secondary effects of most major technological advances in the past, "
          "especially if they were unintended, have turned out to be beneficial.",
          "It is important to judge an invention not by its immediate outcomes, but by "
          "the holistic impact of its secondary effects.",
          "The entire impact of a technological advance should be evaluated by the boost "
          "its secondary effects gives to generating further technological advances."]), "passage": _passage},
]

QUESTIONS.append(q(None, _slot, "Odd Sentence Out", "TITA",
    "Five jumbled up sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given "
    "below. Four of them can be put together to form a coherent paragraph. Identify the "
    "odd sentence and key in the number of that sentence as your answer.\n"
    "1. No known real researcher of human behaviour would say that gender is all nature "
    "or all nurture\n"
    "2. The evidence for a biological basis for gender certainly doesn't mean we should be "
    "complacent in the face of sexism.\n"
    "3. Many people are uncomfortable with the idea that gender is not purely a social "
    "construct.\n"
    "4. Despite this empirical truth, researchers who study the biological basis of "
    "gender often face political pushback.\n"
    "5. There's a political preference for gender to be only a reflection of social "
    "factors and so entirely malleable."))

QUESTIONS.append(q(None, _slot, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "Recent important scientific findings have emerged from crossing the boundaries of "
    "scientific fields. They stem from physicists collaborating with biologists, "
    "sociologists and others, to answer questions about our world. But physicists and "
    "their potential collaborators often find their cultures out of sync. For one, "
    "physicists often discard a lot of information while extracting broad patterns; for "
    "other scientists, information is not readily disposed. Further, many non-physicists "
    "are uncomfortable with mathematical models. Still, the desire to work on something "
    "new and different is real, and there are clear benefits from the collision of "
    "views.",
    ["Physicists have successfully buried their differences on research methods applied "
     "in other fields in their desire to find answers to baffling scientific questions.",
     "Large data sets and mathematical models in physics research combined with the "
     "research methods of non-physicist collaborators have yielded important scientific "
     "findings.",
     "The desire to diversify their research and answer important questions has led to "
     "several collaborations between physicists and other social scientists.",
     "Despite differences in their research styles, physicists' research collaborations "
     "with scholars from other disciplines have yielded important research findings."]))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph "
    "and decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: [T]he Europeans did not invent globalization.\n"
    "Paragraph: The first phase of globalization occurred long before the introduction of "
    "either steam or electric power…Chinese consumers at all social levels consumed vast "
    "quantities of spices, fragrant woods and unusual plants. The peoples of Southeast "
    "Asia who lived in forests gave up their traditional livelihoods and completely "
    "reoriented their economies to supply Chinese consumers….___(1)___. These exchanges "
    "of the year 1000 opened some of the routes through which goods and peoples continued "
    "to travel after Columbus traversed the mid-Atlantic. ___(2)___. Yet the world of "
    "1000 differed from that of 1492 in important ways….the travellers who encountered "
    "one another in the year 1000 were much closer technologically. ___(3)___. They "
    "changed and augmented what was already there since 1000. ___(4)___. If globalization "
    "hadn't yet begun, Europeans wouldn't have been able to penetrate the markets in so "
    "many places as quickly as they did after 1492.",
    ["Option 4", "Option 3", "Option 2", "Option 1"]))

_g = "cat2024_varc_slot2_rc2"
_passage = (
    "(. . .) There are three other common drivers for carnivore-human attacks, some of "
    "which are more preventable than others. Natural aggression-based conflicts – such as "
    "those involving females protecting their young or animals protecting a food source – "
    "can often be avoided as long as people stay away from those animals and their "
    "food.\n\n"
    "Carnivores that recognise humans as a means to get food, are a different story. As "
    "they become more reliant on human food they might find at campsites or in rubbish "
    "bins, they become less avoidant of humans. Losing that instinctive fear response "
    "puts them into more situations where they could get into an altercation with a "
    "human, which often results in that bear being put down by humans. “A fed bear is a "
    "dead bear,” says Servheen, referring to a common saying among biologists and "
    "conservationists.\n\n"
    "Predatory or predation-related attacks are quite rare, only accounting for 17% of "
    "attacks in North America since 1955. They occur when a carnivore views a human as "
    "prey and hunts it like it would any other animal it uses for food. (. . .)\n\n"
    "Then there are animal attacks provoked by people taking pictures with them or "
    "feeding them in natural settings such as national parks which often end with animals "
    "being euthanised out of precaution. “Eventually, that animal becomes habituated to "
    "people, and [then] bad things happen to the animal. And the folks who initially "
    "wanted to make that connection don't necessarily realise that,” says Christine "
    "Wilkinson, a postdoctoral researcher at UC Berkeley, California, who's been studying "
    "coyote-human conflicts.\n\n"
    "After conducting countless postmortems on all types of carnivore-human attacks "
    "spanning 75 years, Penteriani's team believes 50% could have been avoided if humans "
    "reacted differently. A 2017 study co-authored by Penteriani found that engaging in "
    "risky behaviour around large carnivores increases the likelihood of an attack.\n\n"
    "Two of the most common risky behaviours are parents leaving their children to play "
    "outside unattended and walking an unleashed dog, according to the study. Wilkinson "
    "says 66% of coyote attacks involve a dog. “[People] end up in a situation where "
    "their dog is being chased, or their dog chases a coyote, or maybe they're walking "
    "their dog near a den that's marked, and the coyote wants to escort them away,” says "
    "Wilkinson.\n\n"
    "Experts believe climate change also plays a part in the escalation of "
    "human-carnivore conflicts, but the correlation still needs to be ironed out. “As "
    "finite resources become scarcer, carnivores and people are coming into more frequent "
    "contact, which means that more conflict could occur,” says Jen Miller, international "
    "programme specialist for the US Fish & Wildlife Service. For example, she says, "
    "there was an uptick in lion attacks in western India during a drought when lions and "
    "people were relying on the same water sources.\n\n"
    "(. . .) The likelihood of human-carnivore conflicts appears to be higher in areas of "
    "low-income countries dominated by vast rural landscapes and farmland, according to "
    "Penteriani's research. “There are a lot of working landscapes in the Global South "
    "that are really heterogeneous, that are interspersed with carnivore habitats, "
    "forests and savannahs, which creates a lot more opportunity for these encounters, "
    "just statistically,” says Wilkinson."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - carnivore-human conflict", "MCQ",
         "According to the passage, what is a significant factor that contributes to the "
         "habituation of carnivores to human presence?",
         ["The reduction in carnivores' instinctive fear response, resulting from their "
          "reliance upon human-provided food.",
          "The predatory perception of humans as potential prey within the carnivores' "
          "food chain.",
          "The increased scarcity of resources due to climate change, forcing carnivores "
          "to venture outside their natural habitats in search of sustenance.",
          "The natural aggression exhibited by carnivores, exacerbated by human "
          "interference, particularly when they are safeguarding their offspring or food "
          "sources."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - carnivore-human conflict", "MCQ",
         "Given the insights provided by Penteriani's research and Wilkinson's statement, "
         "which of the following conclusions can be drawn about the relationship between "
         "landscape heterogeneity and human-carnivore conflicts?",
         ["The diversity and interspersion of working landscapes with carnivore habitats "
          "in rural areas increase the statistical probability of encounters between "
          "humans and carnivores.",
          "Low-income countries with vast, contiguous wilderness areas are less prone to "
          "human-carnivore conflicts because these areas lack the human presence "
          "necessary for such encounters.",
          "Landscape heterogeneity, characterized by a mix of farmland and natural "
          "habitats, inherently reduces the chances of human-carnivore conflicts by "
          "providing more refuge for wildlife away from human activity.",
          "Homogeneous landscapes with uniform agricultural practices are more likely to "
          "experience high rates of human-carnivore conflicts due to the predictability "
          "of resources."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - carnivore-human conflict", "MCQ",
         "Which of the following statements, if false, would be inconsistent with the "
         "concerns raised in the passage regarding the drivers of carnivore-human "
         "conflicts?",
         ["Climate change has had negligible effects on the frequency of carnivore-human "
          "interactions in affected regions.",
          "Predatory attacks by carnivores are a common occurrence and have steadily "
          "increased over the past few decades.",
          "Human efforts to avoid risky behaviours around large carnivores have proven "
          "effective in reducing conflict incidents.",
          "Carnivores lose their instinctive fear of humans, when consistently exposed to "
          "human food sources."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - carnivore-human conflict", "MCQ",
         "According to the passage, which of the following scenarios would MOST likely "
         "exacerbate the frequency of carnivore-human conflicts?",
         ["Attempting to photograph wild animals from within secured viewing areas in "
          "national parks and protected zones.",
          "Implementing 'food waste' management strategies to prevent wild animals being "
          "attracted to human food sources.",
          "Unleashing dogs by pet owners in areas with known high concentrations of large "
          "carnivores.",
          "Addressing the impact of climate change on the availability of resources for "
          "wildlife."]), "passage": _passage},
]

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph "
    "and decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: Science has officially crowned us superior to our early-rising brethren.\n"
    "Paragraph: My fellow night owls, grab a strong cup of coffee and gather around: I "
    "have great news. ___(1)___. For a long time, our kind has been unfairly maligned. "
    "Stereotyped as lazy and undisciplined. Told we ought to be morning larks. Advised to "
    "go to bed early so we can wake before 5am and run a marathon before breakfast like "
    "all high-flyers seem to do. Now, however, we are having the last laugh. ___(2)___. "
    "It may be a tad more complicated than that. A study published last week, which you "
    "may have already seen while scrolling at 1am, suggests that staying up late could be "
    "good for brain power. ___(3)___. Is this study a thinly veiled PR exercise conducted "
    "by a caffeine-pill company? Nope, it's legit. ___(4)___. Research led by academics "
    "at Imperial College London studied data on more than 26,000 people and found that "
    "“self-declared 'night owls' generally tend to have higher cognitive scores”.",
    ["Option 3", "Option 4", "Option 1", "Option 2"]))

QUESTIONS.append(q(None, _slot, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "Different from individuals, states conduct warfare operations using the DIME "
    "model— “diplomacy, information, military, and economics.” Most states do everything "
    "they can to inflict pain and confusion on their enemies before deploying the "
    "military. In fact, attacks on vectors of information are a well-worn tactic of war "
    "and usually are the first target when the charge begins. It's common for telecom "
    "data and communications networks to be routinely monitored by governments, which is "
    "why the open data policies of the web are so concerning to many advocates of privacy "
    "and human rights. With the worldwide adoption of social media, more governments are "
    "getting involved in low-grade information warfare through the use of cyber troops. "
    "According to a study by the Oxford Internet Institute in 2020, cyber troops are "
    "“government or political party actors tasked with manipulating public opinion "
    "online.” The Oxford research group was able to identify 81 countries with active "
    "cyber troop operations utilizing many different strategies to spread false "
    "information, including spending millions on online advertising.",
    ["Using the DIME model, together with military operations, many governments "
     "simultaneously conduct information warfare with the help of cyber troops and "
     "routinely monitor telecom data and communications networks.",
     "Governments primarily use the DIME model to deploy cyber troops who practise low "
     "grade information warfare, seeking to manipulate public opinion with the objective "
     "of inflicting pain and confusion on their enemies.",
     "As part of conducting information warfare as per the DIME model, many governments "
     "routinely monitor telecom data and communications networks, and use cyber troops on "
     "social media to manipulate public opinion.",
     "Following the DIME model, many governments have taken advantage of open data "
     "policies of the web to deploy cyber troops who manipulate domestic public opinion, "
     "using advertising and other strategies to spread false information."]))

_g = "cat2024_varc_slot2_rc3"
_passage = (
    "[S]pices were a global commodity centuries before European voyages. There was a "
    "complex chain of relations, yet consumers had little knowledge of producers and vice "
    "versa. Desire for spices helped fuel European colonial empires to create political, "
    "military and commercial networks under a single power.\n\n"
    "Historians know a fair amount about the supply of spices in Europe during the "
    "medieval period – the origins, methods of transportation, the prices – but less "
    "about demand. Why go to such extraordinary efforts to procure expensive products "
    "from exotic lands? Still, demand was great enough to inspire the voyages of "
    "Christopher Columbus and Vasco Da Gama, launching the first fateful wave of European "
    "colonialism. . . .\n\n"
    "So, why were spices so highly prized in Europe in the centuries from about 1000 to "
    "1500? One widely disseminated explanation for medieval demand for spices was that "
    "they covered the taste of spoiled meat. . . . Medieval purchasers consumed meat much "
    "fresher than what the average city-dweller in the developed world of today has at "
    "hand. However, refrigeration was not available, and some hot spices have been shown "
    "to serve as an anti-bacterial agent. Salting, smoking or drying meat were other "
    "means of preservation. Most spices used in cooking began as medical ingredients, and "
    "throughout the Middle Ages spices were used as both medicines and condiments. Above "
    "all, medieval recipes involve the combination of medical and culinary lore in order "
    "to balance food's humeral properties and prevent disease. Most spices were hot and "
    "dry and so appropriate in sauces to counteract the moist and wet properties "
    "supposedly possessed by most meat and fish. . . .\n\n"
    "Where spices came from was known in a vague sense centuries before the voyages of "
    "Columbus. Just how vague may be judged by looking at medieval world maps . . . To "
    "the medieval European imagination, the East was exotic and alluring. Medieval maps "
    "often placed India close to the so-called Earthly Paradise, the Garden of Eden "
    "described in the Bible. Geographical knowledge has a lot to do with the perceptions "
    "of spices' relative scarcity and the reasons for their high prices. An example of "
    "the varying notions of scarcity is the conflicting information about how pepper is "
    "harvested. As far back as the 7th century Europeans thought that pepper in India "
    "grew on trees \"guarded\" by serpents that would bite and poison anyone who attempted "
    "to gather the fruit. The only way to harvest pepper was to burn the trees, which "
    "would drive the snakes underground. Of course, this bit of lore would explain the "
    "shrivelled black peppercorns, but not white, pink or other colors.\n\n"
    "Spices never had the enduring allure or power of gold and silver or the commercial "
    "potential of new products such as tobacco, indigo or sugar. But the taste for spices "
    "did continue for a while beyond the Middle Ages. As late as the 17th century, the "
    "English and the Dutch were struggling for control of the Spice Islands: Dutch New "
    "Amsterdam, or New York, was exchanged by the British for one of the Moluccan Islands "
    "where nutmeg was grown."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - history of the spice trade", "MCQ",
         "If a trader brought white peppercorns from India to medieval Europe, all of the "
         "following are unlikely to happen, EXCEPT:",
         ["Europeans would doubt the story of pepper harvesting.",
          "the price of spices would decrease.",
          "pepper would no longer be considered exotic.",
          "medieval maps would be used as navigational aids."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - history of the spice trade", "MCQ",
         "In the context of the passage, the people who heard the story of pepper trees "
         "being guarded by snakes would be least likely to arrive at the conclusion that",
         ["it is not advisable to go to India to harvest the pepper themselves.",
          "this is why pepper is so hot.",
          "it is no surprise that the pepper supply is so limited.",
          "pepper is costly for good reason."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - history of the spice trade", "MCQ",
         "It can be inferred that all of the following contributed to a decline in the "
         "allure of spices, EXCEPT:",
         ["increase in the availability of spices.",
          "changes in European cuisine.",
          "changes in the system of medical treatment.",
          "the development of refrigeration techniques."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - history of the spice trade", "MCQ",
         "In the context of the passage, which one of the following conclusions CANNOT be "
         "reached?",
         ["Colonialism was motivated by the demand for spices.",
          "Tobacco was more marketable than spices.",
          "The spice trade was a driver of colonial expansion.",
          "India was colonised for its spices and gold."]), "passage": _passage},
]

_g = "cat2024_varc_slot2_rc4"
_passage = (
    "The job of a peer reviewer is thankless. Collectively, academics spend around 70 "
    "million hours every year evaluating each other's manuscripts on the behalf of "
    "scholarly journals — and they usually receive no monetary compensation and little "
    "if any recognition for their effort. Some do it as a way to keep abreast with "
    "developments in their field; some simply see it as a duty to the discipline. Either "
    "way, academic publishing would likely crumble without them.\n\n"
    "In recent years, some scientists have begun posting their reviews online, mainly to "
    "claim credit for their work. Sites like Publons allow researchers to either share "
    "entire referee reports or simply list the journals for whom they've carried out a "
    "review….\n\n"
    "The rise of Publons suggests that academics are increasingly placing value on the "
    "work of peer review and asking others, such as grant funders, to do the same. While "
    "that's vital in the publish-or-perish culture of academia, there's also immense "
    "value in the data underlying peer review. Sharing peer review data could help "
    "journals stamp out fraud, inefficiency, and systemic bias in academic publishing…..\n\n"
    "Peer review data could also help root out bias. Last year, a study based on peer "
    "review data for nearly 24,000 submissions to the biomedical journal eLife found that "
    "women and non Westerners were vastly underrepresented among peer reviewers. Only "
    "around one in every five reviewers was female, and less than two percent of "
    "reviewers were based in developing countries…. Openly publishing peer review data "
    "could perhaps also help journals address another problem in academic publishing: "
    "fraudulent peer reviews. For instance, a minority of authors have been known to use "
    "phony email addresses to pose as an outside expert and review their own "
    "manuscripts….\n\n"
    "Opponents of open peer review commonly argue that confidentiality is vital to the "
    "integrity of the review process; referees may be less critical of manuscripts if "
    "their reports are published, especially if they are revealing their identities by "
    "signing them. Some also hold concerns that open reviewing may deter referees from "
    "agreeing to judge manuscripts in the first place, or that they'll take longer to do "
    "so out of fear of scrutiny….\n\n"
    "Even when the content of reviews and the identity of reviewers can't be shared "
    "publicly, perhaps journals could share the data with outside researchers for study. "
    "Or they could release other figures that wouldn't compromise the anonymity of "
    "reviews but that might answer important questions about how long the reviewing "
    "process takes, how many researchers editors have to reach out to on average to find "
    "one who will carry out the work, and the geographic distribution of peer "
    "reviewers.\n\n"
    "Of course, opening up data underlying the reviewing process will not fix peer review "
    "entirely, and there may be instances in which there are valid reasons to keep the "
    "content of peer reviews hidden and the identity of referees confidential. But the "
    "norm should shift from opacity in all cases to opacity only when necessary."
)
QUESTIONS += [
    {**q(_g, _slot, "Reading Comprehension - transparency in peer review", "MCQ",
         "All of the following are listed as reasons why academics choose to review other "
         "scholars' work EXCEPT:",
         ["It is seen as an opportunity to expand their influence in the academic "
          "community.",
          "Some use this as an opportunity to publicise their own review work.",
          "It is seen as a form of service to the academic community.",
          "It helps them keep current with cutting-edge ideas in their academic "
          "disciplines."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - transparency in peer review", "MCQ",
         "According to the passage, some are opposed to making peer reviews public for "
         "all the following reasons EXCEPT that it",
         ["makes reviewers reluctant to review manuscripts, especially if these are "
          "critical of the submitted work.",
          "delays the manuscript evaluation process as reviewers would take longer to "
          "write their reviews.",
          "deters reviewers from producing honest, if critical, reviews that are vital to "
          "the sound publishing process.",
          "leaves the reviewers unexposed to unwarranted and unjustified criticism or "
          "comments from others."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - transparency in peer review", "MCQ",
         "Based on the passage we can infer that the author would most probably support",
         ["greater transparency across the peer review process in academic publishing.",
          "preserving the anonymity of reviewers to protect them from criticism.",
          "publicising peer review data rather than the publication of actual reviews.",
          "more careful screening to ensure the recruitment of content-familiar peer "
          "reviewers."]), "passage": _passage},
    {**q(_g, _slot, "Reading Comprehension - transparency in peer review", "MCQ",
         "According to the passage, which of the following is the only reason NOT given "
         "in favour of making peer review data public?",
         ["It will deal with peer review fraud such as authors publishing bogus reviews "
          "of their work.",
          "It could address various inefficiencies and fraudulent practices that continue "
          "in academic publishing process.",
          "It can tackle the problem of selecting appropriately qualified reviewers for "
          "academic writing.",
          "It would highlight the gender and race biases currently existing in the "
          "selection of reviewers."]), "passage": _passage},
]

QUESTIONS.append(q(None, _slot, "Paragraph Summary", "MCQ",
    "The passage given below is followed by four alternate summaries. Choose the option "
    "that best captures the essence of the passage.\n"
    "John Cleese told Fox News Digital that comedians do not have the freedom to be "
    "funny in 2022. “There's always been limitations on what they're allowed to say,” "
    "Cleese said. “I think it's particularly worrying at the moment because you can only "
    "create in an atmosphere of freedom, where you're not checking everything you say "
    "critically before you move on. What you have to be able to do is to build without "
    "knowing where you're going because you've never been there before. That's what "
    "creativity is — you have to be allowed to build. And a lot of comedians now are "
    "sitting there and when they think of something, they say something like, 'Can I get "
    "away with it? I don't think so. So and so got into trouble, and he said that, oh, "
    "she said that.' You see what I mean? And that's the death of creativity.”",
    ["Comedians must not check what they think and say. They must go where no one has "
     "gone before.",
     "Comedians are being prevented from saying what they want and that is the death of "
     "this art form.",
     "Creativity and critical thinking cannot work together. Comedians must first be "
     "creative, and later be critical.",
     "Freedom and creativity are essential for comedy. Fear about offending people "
     "hinders originality."]))

QUESTIONS.append(q(None, _slot, "Sentence Insertion", "MCQ",
    "There is a sentence that is missing in the paragraph below. Look at the paragraph "
    "and decide where (option 1, 2, 3, or 4) the following sentence would best fit.\n"
    "Sentence: Yet each day the flock produced eggs with calcareous shells though they "
    "apparently had not ingested any calcium from land which was entirely lacking in "
    "limestone.\n"
    "Paragraph: Early in this century a young Breton schoolboy who preparing himself for "
    "a scientific career began to notice a strange fact about hens in his father's "
    "poultry yard. ___(1) ___. As they scratched the soil they constantly seemed to be "
    "pecking at specks of mica, a siliceous material dotting the ground. ___(2)___. No "
    "one could explain to Louis Kervran why the chickens selected the mica, or why each "
    "time a bird was killed for the family cooking pot no trace of the mica could be "
    "found in its gizzard. ___(3) ___. It took Kervran many years to establish that the "
    "chickens were transmuting one element into another. ___(4)___.",
    ["Option 3", "Option 2", "Option 4", "Option 1"]))


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
            print(f"CAT 2024 VARC already seeded ({existing} rows); skipping.")
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
        print(f"Seeded {len(QUESTIONS)} CAT 2024 VARC questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

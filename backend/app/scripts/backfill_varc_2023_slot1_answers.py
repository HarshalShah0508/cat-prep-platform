"""Backfill explanation for CAT 2023 VARC Slot 1 (correct_answer was already
resolved correctly by pyq_varc_parser.py at load time - this only adds the
explanation field, rewritten in plain language from the solutions PDF, not
copied verbatim). Matched against already-loaded rows by (source_year,
source_slot, section, question_text).

Q11 is skipped - its printed answer value did not resolve to anything usable.

Run with:
    python -m app.scripts.backfill_varc_2023_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("All of the following claims contribute to the \"remapping\" discussed by the passage, EXCEPT:", "cosmopolitanism originated in the West and travelled to the East through globalisation", "The passage's \"remapping\" is about reframing the Indian Ocean world as a long-connected region in its own right - not about cosmopolitanism originating in the West and spreading east via globalisation."),
    ("On the basis of the nature of the relationship between the items in each pair below, choose the odd pair out:", "postcolonial novels : Border-crossing", "Unlike the other pairs, which reflect genuine thematic links drawn in the passage, postcolonial novels aren't specifically characterised by \"border-crossing\" - making this the odd pair out."),
    ("All of the following statements, if true, would weaken the passage's claim about the relationship between mainstream English-language fiction and Indian Ocean novels EXCEPT:", "most mainstream English-language novels have historically privileged the Christian, white, male experience of travel and adventure.", "If mainstream English fiction had historically centered Christian, white, male travel narratives, that would support (not weaken) the passage's claim that it's distinct from Indian Ocean narratives."),
    ("Which one of the following statements is not true about migration in the Indian Ocean world?", "The Indian Ocean world's migration networks connected the global north with the global south.", "The passage never discusses migration networks linking the global north and south - it focuses on Indian Ocean connections, making this the one false statement about the region's migration."),
    ("The author of the passage mentions Galbraith's \"The Affluent Society\" to:", "show how Sahlins's views complemented Galbraith's criticism of the consumerism and inequality of contemporary society.", "The author invokes Galbraith's \"The Affluent Society\" to show how it echoes Sahlins's own critique of modern consumerism and inequality."),
    ("The author mentions Tanzania's Hadza community to illustrate:", "that forager communities' lifestyles derived not from ignorance about alternatives, but from their own choice.", "The Hadza example shows that forager communities live as they do by genuine choice, not because they're unaware of other ways of life."),
    ("The author of the passage criticises Sahlins's essay for its:", "cursory treatment of the effects of racism and colonialism on societies.", "The author faults Sahlins's essay for only briefly addressing how racism and colonialism have shaped these societies."),
    ("We can infer that Sahlins's main goal in writing his essay was to:", "hold a mirror to an acquisitive society, with examples of other communities that have chosen successfully to be non-materialistic.", "Sahlins wrote his essay to hold up a mirror to acquisitive modern society, using examples of communities that chose a non-materialistic way of life successfully."),
    ("Which one of the following has NOT contributed to the growing wolf population in Lozère?", "The shutting down of the royal office of the Luparii.", "Shutting down the old royal wolf-catching office didn't cause the wolves to return - it happened only after wolves were already wiped out, so it's not a contributing factor to today's resurgence."),
    ("The author presents a possible economic solution to an existing issue facing Lozère that takes into account the divergent and competing interests of:", "farmers and environmentalists.", "The proposed economic solution has to balance the competing interests of farmers (worried about livestock losses) and environmentalists/tourists (drawn by the wolves' return)."),
    ("The inhabitants of Lozère have to grapple with all of the following problems, EXCEPT:", "decline in the number of hunting licences.", "Residents worry about schools, jobs, connectivity, and wolf attacks on livestock - but a decline in hunting licences isn't one of the problems the passage raises."),
    ("Which one of the following statements, if true, would weaken the author's claims?", "Wolf attacks on tourists in Lozère are on the rise", "If wolf attacks on tourists were actually rising, that would undercut the author's more measured framing of the conflict as primarily about farmers' livestock losses."),
    ("The author criticises scholars who are not geographers for all of the following reasons EXCEPT:", "their outdated interpretations of past cultural and historical phenomena.", "The author's critique of non-geographer scholars covers several angles, but doesn't single out their interpretations of past phenomena as \"outdated\" - that's not one of the reasons given."),
    ("The examples of the Inuit and Aboriginal Australians are offered in the passage to show:", "how physical circumstances can dictate human behaviour and cultures.", "The Inuit and Aboriginal Australian examples illustrate how physical/environmental circumstances shape human behaviour and culture."),
    ("All of the following can be inferred from the passage EXCEPT:", "while most human phenomena result from culture and individual choice, some have biogeographic origins.", "The passage does allow that some human phenomena have biogeographic roots alongside cultural and individual-choice explanations - this is something the passage affirms, not an exception to it."),
    ("All of the following are advanced by the author as reasons why non- geographers disregard geographic influences on human phenomena EXCEPT their:", "dismissal of explanations that involve geographical causes for human behaviour.", "The author attributes non-geographers' dismissal of geographic influence to deeper, more specific reasons - not simply a blanket rejection of geography-based explanations."),
    ("There is a sentence that is missing in the paragraph below. Look at the paragraph and decide where (option 1,2,3, or 4) the following sentence would best fit. Sentence: The discovery helps to explain archeological similarities between the Paleolithic peoples of China, Japan, and the Americas. Paragraph: The researchers also uncovered an unexpected genetic link between Native Americans and Japanese people. (1)__ . During the\n\ndeglaciation period, another group branched out from northern coastal China and travelled to Japan. (2) _. \"We were surprised to find that this ancestral source also contributed to the Japanese gene pool, especially the indigenous Ainus,\" says Li. _ (3) _. They shared similarities in how they crafted stemmed projectile points for arrowheads and spears. __(4)__. \"This suggests that the Pleistocene connection among the Americas, China, and Japan was not confined to culture but also to genetics,\" says senior author Qing-Peng Kong, an evolutionary geneticist at the Chinese Academy of Sciences.", "Option 3", "The missing sentence about archaeological evidence fits best at the paragraph's third blank, right after the discovery about the ancestral source in the Japanese gene pool is introduced."),
    ("There is a sentence that is missing in the paragraph below. Look at the paragraph and decide where (option 1, 2, 3, or 4 ) the following sentence\n\nwould best fit. Sentence: This philosophical cut at one's core beliefs, values, and way of life is difficult enough. Paragraph: The experience of reading philosophy is often disquieting. When reading philosophy, the values around which one has heretofore organised one's life may come to look provincial, flatly wrong, or even evil. __(1)_. When beliefs previously held as truths are rendered implausible, new beliefs, values, and ways of living may be required. _ (2) . What's worse, philosophers admonish each other to remain unsutured until such time as a defensible new answer is revealed or constructed. Sometimes philosophical writing is even strictly critical in that it does not even attempt to provide an alternative after tearing down a cultural or conceptual citadel. (3). The reader of philosophy must be prepared for the possibility of this experience. While reading philosophy can help one clarify one's values, and even make one self-conscious for the first time of the fact that there are good reasons for believing what one believes, it can also generate un-remediated doubt that is difficult to live with.", "Option 2", "The sentence about philosophy cutting at one's core beliefs fits best at the paragraph's second blank, right as the disquieting nature of reading philosophy is being introduced."),
    ("Five jumbled up sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd sentence and key in the number of that sentence as your answer", "It is a ‘theory of mind’ though some scholars prefer to call it ‘mentalizing’ or ‘mindreading’, which is important for the development of one's cognitive abilities", "The odd sentence out drifts into discussing terminology like \"mentalizing\" or \"mindreading\" rather than staying with the paragraph's actual throughline about theory of mind's role in cognitive development."),
    ("Five jumbled up sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd sentence and key in the number of that sentence as your answer", "It can take children a while to learn all these words, and understand that \"fourteen\" is different from \"forty\".", "The odd sentence out, about children taking time to learn number words like \"fourteen\" vs \"forty,\" breaks from the other sentences' focus on the irregularities of English number-naming conventions."),
    ("The four sentences (labelled 1, 2, 3 and 4) given below, when properly sequenced, would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer. 1. What precisely are the \"unusual elements\" that make a particular case so attractive to a certain kind of audience? 2. It might be a particularly savage or unfathomable level of depravity, very often it has something to do with the precise amount of mystery involved. 3. Unsolved, and perhaps unsolvable cases offer something that \"ordinary\" murder doesn't. 4. Why are some crimes destined for perpetual re-examination and others locked into permanent obscurity?", "4123", "4, 1, 2, 3 - opening with why certain crimes hold lasting public fascination (4), narrowing into the specific unusual elements that draw interest (1), and building through to the conclusion."),
    ("The four sentences (labelled 1, 2, 3 and 4) given below, when properly sequenced, would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer. 1. Algorithms hosted on the internet are accessed by many, so biases in Al models have resulted in much larger impact, adversely affecting far larger groups of people. 2. Though \"algorithmic bias\" is the popular term, the foundation of such bias is not in algorithms, but in the data; algorithms are not biased, data is, as algorithms merely reflect persistent patterns that are present in the training data. 3. Despite their widespread impact, it is relatively easier to fix Al biases than human-generated biases, as it is simpler to identify the former than to try to make people unlearn behaviors learnt over generations. 4. The impact of biased decisions made by humans is localised and geographically confined, but with the advent of Al, the impact of such decisions is spread over a much wider scale.", "4123", "4, 1, 2, 3 - introducing how AI scales up the localized effects of biased human decisions (4), then elaborating further through the supporting sentences."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage. Manipulating information was a feature of history long before modern journalism established rules of integrity. A record dates back to ancient Rome, when Antony met Cleopatra and his political enemy Octavian launched a smear campaign against him with \"short, sharp slogans written upon coins.\" The perpetrator became the first Roman Emperor and \"fake news had allowed Octavian to hack the republican system once and for all\". But the 21st century has seen the weaponization of information on an unprecedented scale. Powerful new technology makes the fabrication of content simple, and social networks amplify falsehoods peddled by States, populist politicians, and dishonest corporate entities. The platforms have become fertile ground for computational propaganda, 'trolling' and 'troll armies'.", "Use of misinformation for attaining power, a practice that is as old as the Octavian era, is currently fueled by technology.", "The passage traces how misinformation has been used to gain power since the days of Octavian, a practice now supercharged by modern technology."),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "VARC",
                    CatQuestion.question_text == question_text,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} VARC {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()

"""Backfill explanation for CAT 2020 VARC Slot 1 (correct_answer was already
resolved correctly by pyq_varc_parser_flat.py at load time via the lettered
option mapping - this only adds the explanation field, rewritten in plain
language from the solutions PDF, not copied verbatim). Matched against
already-loaded rows by (source_year, source_slot, section, question_text).

Run with:
    python -m app.scripts.backfill_varc_2020_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("Which one of the following best expresses the similarity between American individualist anarchists and free-market liberals as well as the difference between the former and the latter?", "Both prioritise individual autonomy; but the former also emphasise mutual dependence, while the latter do not do so.", "American individualist anarchists and free-market liberals both value individual autonomy, but anarchists also stress mutual dependence between people - something free-market liberals don't emphasize."),
    ("The author makes all of the following arguments in the passage, EXCEPT:", "The popular perception of anarchism as espousing lawlessness and violence comes from a mainstream mistrust of collectivism.", "The passage never links anarchism's reputation for lawlessness to a general mistrust of collectivism - every other option is a claim the passage does make directly."),
    ("According to the passage, what is the one idea that is common to all forms of anarchism?", "They are all opposed to the centralisation of power in the state.", "Every form of anarchism discussed in the passage shares one core idea: opposition to centralized state power."),
    ("The author believes that the new ruling class of politicians betrayed the principles of the French Revolution, but does not specify in what way. In the context of the passage, which statement below is the likeliest explanation of that betrayal?", "The new ruling class rode to power on the strength of the workers’ revolutionary anger, but then turned to oppress that very class.", "The new political class rose to power on the back of workers' revolutionary anger, then turned around and oppressed that same working class once in control."),
    ("Of the following sets of concepts, identify the set that is conceptually closest to the con- cerns of the passage.", "Anarchism, State, Individual, Freedom.", "The passage's central concerns map most closely onto the concepts of anarchism, the state, the individual, and freedom."),
    ("Which one of the following conditions, if true, could have ensured that male northern ele- phant seal dialects did not disappear?", "Besides Isla Guadalupe, there was one more surviving colony with the same average male call tempo from which no migration took place.", "Dialects would have stayed intact only if another colony shared the same average call tempo and had no migration disrupting it - any migration would have blended or shifted the dialect."),
    ("All of the following can be inferred from Le Boeuf’s study as described in the passage EXCEPT that:", "changes in population and migration had no effect on the call pulse rate of individual male northern elephant seals.", "The passage actually shows migration DID affect call pulse rates (faster-calling seals moving in changed the average at Año Nuevo) - so claiming migration had no effect is the one inference the passage contradicts."),
    ("Which one of the following best sums up the overall history of transformation of male northern elephant seal calls?", "The calls have transformed from exhibiting simple composition, less individual variety, and great regional variety to complex composition, great individual variety, and less regional variety.", "Over time the seals' calls went from simple, low-individual-variety, high-regional-variety sounds to complex, highly individual, and less regionally distinct ones."),
    ("From the passage it can be inferred that the call pulse rate of male northern elephant seals in the southern rookeries was faster because:", "the male northern elephant seals of Isla Guadalupe with faster call pulse rates might have been the original settlers of the southern rookeries.", "The faster call pulse rates in the southern rookeries likely trace back to original settlers from Isla Guadalupe, who already had faster pulse rates."),
    ("In the context of the passage, which one of the following can be inferred with regard to the use of currency during the Tang era?", "Currency that deteriorated easily was not used for official work.", "Because textiles wore down more easily than coins, they weren't reliable enough to be used for official/formal transactions."),
    ("According to the passage, the modern currency system shares all the following features with that of the Tang, EXCEPT that:", "it uses different materials as currency.", "Modern currency, unlike the Tang system, doesn't rely on different physical materials (like textiles or grain) - it's the one feature that doesn't carry over."),
    ("When discussing textiles as currency in the Tang period, the author uses the words ”steady” and ”stable” to indicate all of the following EXCEPT:", "reliable transportation.", "\"Steady\" and \"stable\" describe the textiles' consistent size, supply, and quality - not anything about transportation, which the passage never mentions in this context."),
    ("During the Tang period, which one of the following would not be an economically sound decision for a small purchase in the local market that is worth one-eighth of a bolt of cloth?", "Cutting one-eighth of the fabric from a new bolt to pay the amount.", "Cutting a fraction off a new bolt of fabric to make a small payment would reduce its value significantly, making it a poor economic choice compared to using coins, grain, or an already-worn bolt."),
    ("Which one of the following quotes best captures the main concern of the passage?", "”Nouns and verbs are the two indispensable parts of writing. Without one of each, no group of words can be a sentence ...”", "The passage's core concern is captured by the idea that nouns and verbs are the two essential building blocks of a sentence."),
    ("Which one of the following statements, if false, could be seen as supporting the arguments in the passage?", "Regarding grammar, women writers tend to be more attentive to method and accuracy.", "The passage never claims women writers are more careful about grammar - this unfounded claim, if shown false, would actually support the passage's broader argument against grammar myths and bias."),
    ("All of the following statements can be inferred from the passage EXCEPT that:", "The primary purpose of grammar is to ensure that sentences remain simple.", "The passage frames grammar as a tool for making sentences make sense and communicate clearly - not specifically as a tool for keeping sentences simple, so that claim doesn't hold."),
    ("”Take any noun, put it with any verb, and you have a sentence. It never fails. Rocks\n\nexplode. Jane transmits. Mountains float.” None of the following statements can be seen as similar EXCEPT:", "A group of nouns arranged in a row becomes a sentence.", "The passage's point - that pairing any noun with any verb reliably produces a sentence - is best mirrored by the idea that a row of nouns (with a verb) becomes a sentence."),
    ("Inferring from the passage, the author could be most supportive of which one of the fol- lowing practices?", "A campaign demanding that a writer’s creative license should allow the breaking of gram- matical rules.", "The author's openness to breaking grammar rules for creative effect (when a writer knows what they're doing) aligns with supporting a campaign for creative license to break grammatical convention."),
    ("The four sentences (labelled A, B, C, D) below, when properly sequenced would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "(C, A, B, D)", "C, A, B, D - starting with South East Asia's general security picture (C), naming the countries involved (A), narrowing to China's military rise (B), and ending with outside powers' resulting interest (D)."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage.\n\nFor nearly a century most psychologists have embraced one view of intelligence. Individu- als are born with more or less intelligence potential (I.Q.); this potential is heavily in82uenced by heredity and difcult to alter; experts in measurement can determine a person’s intelligence early in life, currently from paper-and-pencil measures, perhaps eventually from examining the brain in action or even scrutinizing his/her genome. Recently, criticism of this conven- tional wisdom has mounted. Biologists ask if speaking of a single entity called ”intelligence” is coherent and question the validity of measures used to estimate heritability of a trait in hu- mans, who, unlike plants or animals, are not conceived and bred under controlled conditions.", "Biologists have questioned the long-standing view that ’intelligence’ is a single entity and the attempts to estimate its heritability.", "The passage's main thread is that biologists have challenged the long-held idea that intelligence is one single trait whose heritability can be reliably estimated."),
    ("The four sentences (labelled A, B, C, D) below, when properly sequenced would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "(A, C, B, D)", "A, C, B, D - opening with the difficulty of reading San folktales from narrative alone (A), introducing the spiritual conflict with shamans (C), explaining benign shamans' role (B), and closing out the argument (D)."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage.\n\nFor years, movies and television series like Crime Scene Investigation (CSI) paint an un- realistic picture of the ”science of voices.” In the 1994 movie Clear and Present Danger an expert listens to a brief recorded utterance and declares that the speaker is ”Cuban, aged 35 to 45, educated in the [ ... ] eastern United States.” The recording is then fed to a supercomputer that matches the voice to that of a suspect, concluding that the probability of correct iden- tification is 90%. This sequence sums up a good number of misimpressions about forensic phonetics, which have led to errors in real-life justice. Indeed, that movie scene exemplifies the so-called ”CSI effect”-the phenomenon in which judges hold unrealistic expectations of the capabilities of forensic science.", "Although voice recognition is often presented as evidence in legal cases, its scientific ba- sis can be shaky.", "The passage's point is that voice recognition, despite being treated as solid evidence in court, often rests on shaky scientific ground."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage.\n\nAs Soviet power declined, the world became to some extent multipolar, and Europe strove to define an independent identity. What a journey Europe has undertaken to reach this point. It had in every century changed its internal structure and invented new ways of thinking about the nature of international order. Now at the culmination of an era, Europe, in order to partic- ipate in it, felt obliged to set aside the political mechanisms through which it had conducted its affairs for three and a half centuries. Impelled also by the desire to cushion the emergent unification of Germany, the new European Union established a common currency in 2002 and a formal political structure in 2004. It proclaimed a Europe united, whole, and free, adjusting its differences by peaceful mechanisms.", "Europe has consistently changed in keeping with the changing world order and that has culminated in a united Europe.", "The passage traces how Europe kept adapting to a changing world order, a process that eventually led to a unified Europe."),
    ("The four sentences (labelled A, B, C, D) below, when properly sequenced would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "A, C, B, D", "A, C, B, D - starting with the historical use of poisons (A), moving to how microbiology opened new possibilities for biological weapons (C), then the international treaties banning poisoned weapons (B), and finishing with why those treaties ultimately failed (D)."),
    ("Five jumbled up sentences, related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd one out and key in the number of the sentence as your answer:", "The documentation of this realization was one of the earliest tasks undertaken by feminist critics.", "Sentences A, B, and C form a coherent passage about feminist readings of literature; sentence D - about documenting this realization - breaks that flow, making it the odd one out."),
    ("Five jumbled up sentences, related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd one out and key in the number of the sentence as your answer:", "Slaves came from societies in which oaths, orations, and invocations carried great potency, both between people and as a connection to the all-powerful spirit world.", "Sentences A, B, D, and E together build the argument about the subversive power of slave talk; sentence C instead focuses on the historical background of slave societies, making it the one that doesn't fit."),
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

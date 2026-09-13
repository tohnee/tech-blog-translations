---
title: "Predicting the past with Ithaca"
source: https://deepmind.google/blog/predicting-the-past-with-ithaca/
site: deepmind
date: 2022-03-09
authors: Yannis Assael, Thea Sommerschield, Brendan Shillingford, Nando de Freitas
crawled: 2026-09-13
---

Restoring, placing, and dating ancient texts through collaboration between AI and historians

The birth of human writing marked the dawn of [History](https://en.wikipedia.org/wiki/History#History_and_prehistory) and is crucial to our understanding of past civilisations and the world we live in today. For example, more than 2,500 years ago, the Greeks began writing on stone, pottery, and metal to document everything from leases and laws to calendars and oracles, giving a detailed insight into the Mediterranean region. Unfortunately, it’s an incomplete record. Many of the surviving inscriptions have been damaged over the centuries or moved from their original location. In addition, modern dating techniques, such as [radiocarbon dating](https://en.wikipedia.org/wiki/Radiocarbon_dating), cannot be used on these materials, making inscriptions difficult and time-consuming to interpret.

In line with [DeepMind’s mission](https://deepmind.com/about) of solving intelligence to advance science and humanity, we collaborated with the [Department of Humanities of Ca' Foscari University of Venice](https://www.unive.it/pag/27720/), the [Classics Faculty of the University of Oxford](https://www.classics.ox.ac.uk/), and the [Department of Informatics of the Athens University of Economics and Business](https://www.dept.aueb.gr/en/infotech-overview-en) to explore how machine learning can help historians better interpret these inscriptions – giving a richer understanding of ancient history and unlocking the potential for cooperation between AI and historians.

In a [paper](https://www.nature.com/articles/s41586-022-04448-z) published today in Nature, we jointly introduce Ithaca, the first deep neural network that can restore the missing text of damaged inscriptions, identify their original location, and help establish the date they were created. Ithaca is named after the Greek island in [Homer’s Odyssey](https://en.wikipedia.org/wiki/Odyssey) and builds upon and extends [Pythia](https://deepmind.com/research/publications/2019/Restoring-ancient-text-using-deep-learning-a-case-study-on-Greek-epigraphy), our previous system that focused on textual restoration. Our evaluations show that Ithaca achieves 62% accuracy in restoring damaged texts, 71% accuracy in identifying their original location, and can date texts to within 30 years of their ground-truth date ranges. Historians have already used the tool to reevaluate significant periods in Greek history.

To make our research widely available to researchers, educators, museum staff and others, we partnered with [Google Cloud](https://cloud.google.com/) and [Google Arts & Culture](https://artsandculture.google.com/) to launch a [free interactive version of Ithaca](https://ithaca.deepmind.com/). And to aid further research, we have also [open sourced](https://github.com/deepmind/ithaca) our code, the pretrained model, and an interactive Colaboratory notebook.

![An animation, showing how AI can use fragments of a pieced-together stone tablet to predict what content is missing or has been destroyed.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e47ba59f4a050e873f3a_Fig201animated.gif)

Figure 1. This restored inscription (IG I3 4B) records a decree concerning the Acropolis of Athens and dates 485/4 BCE. (CC BY-SA 3.0, WikiMedia).

![A diagram of the Ithaca neural network architecture, showing how characters and words in Greek input text are processed with positional information through a Torso block with sparse multi-head attention to generate outputs for text restoration, geographical attribution, and chronological attribution.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4946bcb81d92694d69a_Fig202.2.svg)

Figure 2. Ithaca's architecture. Damaged parts of a text are represented with a dash "-". Here, we artificially corrupted the characters "δημ." Provided with these inputs, Ithaca restores the text, and identifies the time and place in which the text was written.

## Collaborative tools

Ithaca is trained on the [largest digital dataset of Greek inscriptions](https://inscriptions.packhum.org/) from the [Packard Humanities Institute](https://packhum.org/). [Natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) models are commonly trained using words because the order in which they appear in sentences and the relationships between them provide extra context and meaning. For example, “once upon a time” has more meaning than each character or word seen separately. However, many of the inscriptions historians are interested in analysing with Ithaca are damaged and often missing chunks of text. To ensure our model still works when presented with one of these, we trained it using both words and the individual characters as inputs. The sparse self-attention mechanism at the model’s core evaluates these two inputs in parallel, allowing Ithaca to evaluate inscriptions as needed.

![An interface showcasing Ithaca’s predictions for text restoration, geographical attribution, and chronological attribution of an ancient Greek inscription.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4aed783c158e7bc03a1_Fig203.2.svg)

Figure 3. Ithaca’s outputs. (a) Restoration predictions for 6 missing characters (dashes) in an Athenian inscription (IG II2 116). The top restoration, in green, is correct (συμμαχία, "alliance"). Note how the following hypotheses (ἐκκλησία, "assembly" and προξενία, "treaty between State and foreigner"), highlighted in red, typically occur in Athenian political decrees, revealing Ithaca's receptivity to context. (b) Geographical attribution of an inscription from Amorgos (IG XII 7, 2). Ithaca's top prediction is correct, and the closest predictions are neighbouring regions. (c) Date distribution for an inscription from Delos (IG XI 4, 579). The ground-truth date interval 300-250 BCE is in grey; Ithaca's predicted distribution is in yellow and has a mean at 273 BCE (in green).

To maximise Ithaca's value as a research tool, we also created a number of visual aids to ensure Ithaca’s results are easily interpretable by historians:

- **Restoration hypotheses**: Ithaca generates several prediction hypotheses for the text restoration task for historians to choose from using their expertise.
- **Geographical attribution**: Ithaca shows its uncertainty by giving historians a probability distribution over all possible predictions – instead of just a single output. As a result, it returns probabilities for 84 different ancient regions representing its level of certainty. It visualises these results on a map to shed light on possible underlying geographical connections across the ancient world.
- **Chronological attribution**: When dating a text, Ithaca produces a distribution of predicted dates across all decades from 800 BCE to 800 CE. This can enable historians to visualise the model’s confidence for specific date ranges, which may offer valuable historical insights.
- **Saliency maps**: To convey the results to historians, Ithaca uses a technique commonly used in computer vision that identifies which input sequences contribute most to a prediction. The output highlights the words in different colour intensities that led to Ithaca’s predictions for missing text, location and dates.

![The top row of input text has six blank characters, represented by dashes. Below that, Ithaca restores one of the characters in each row. A translation of the output says "Gods. In the archonship of Nikophemos. Alliance of the Athenians and Thessalians for all time."](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4cfc0dd671ee8e1dc1b_Fig204.2.svg)

Figure 4. This text (IG II2 116, Athens 361/0 BCE) records an alliance between the people of Athens and Thessaly. By using saliency maps, we can visualise Ithaca "focusing" on the contextually important words ‘Athenians’ and ‘Thessalians’ when restoring the corrupted word ‘alliance’.

## Contributing to historical debates

Our experimental evaluation shows how Ithaca’s design decisions and visualisation aids make it easier for researchers to interpret results. The expert historians we worked with achieved 25% accuracy when working alone to restore ancient texts. But, when using Ithaca, their performance increases to 72%, surpassing the model’s individual performance and showing the potential for human-machine cooperation to advance historical interpretation, establish relative datings for historical events, and even contribute to current methodological debates.

For example, historians currently disagree on the date of a series of important [Athenian decrees](https://staff.mq.edu.au/teach/teaching-macquarie/ancient-history-for-schools/greece-resources/resources-for-year-12-ancient-greek-studies/three-bar-sigma) made at a time when notable figures such as Socrates and Pericles lived. The decrees have long been thought to have been written before 446/445 BCE, although new evidence suggests a date of the 420s BCE. Although it might seem like a small difference, these decrees are fundamental to our understanding of the political history of Classical Athens.

Our training dataset contains the earlier figure of 446/445 BCE. To test Ithaca’s predictions, we retrained it on a dataset that did not contain the dated inscriptions and then submitted these held-out texts for analysis. Remarkably, Ithaca’s average predicted date for the decrees is 421 BCE, aligning with the most recent dating breakthroughs and showing how machine learning can contribute to debates around one of the most significant moments in Greek history.

![A box plot comparing the dating error in years for PHI and Ithaca, showing a significantly lower median and mean error for Ithaca (under 10 years) compared to PHI (over 20 years).](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231e4e8ad33cf33f6d57c3c_Fig205.2.svg)

Figure 5. Ithaca's predictions vs Packard Humanities Institute (PHI) dataset's ground-truths compared to recent historical re-evaluations. PHI labels are on average 27 years off the re-evaluations, while Ithaca’s predictions are on average only 5 years off the newly proposed ground-truths.

We believe this is just the start for tools like Ithaca and the potential for collaboration between machine learning and the humanities. Ancient Greece plays an instrumental role in our understanding of the Mediterranean world, but it’s still only one part of a vast global picture of civilisations. To that end, we are currently working on versions of Ithaca trained on other ancient languages and historians can already use their datasets in the current architecture to study other ancient writing systems, from [Akkadian](https://en.wikipedia.org/wiki/Akkadian_language) to [Demotic](https://en.wikipedia.org/wiki/Demotic_(Egyptian)) and [Hebrew](https://en.wikipedia.org/wiki/Hebrew_language) to [Mayan](https://en.wikipedia.org/wiki/Mayan_languages). We hope that models like Ithaca can unlock the cooperative potential between AI and the humanities, transformationally impacting the way we study and write about some of the most significant periods in human history.

- Read the [paper](https://www.nature.com/articles/s41586-022-04448-z)
- Explore the interactive version of [Ithaca](https://ithaca.deepmind.com/)
- Get the [open source](https://github.com/deepmind/ithaca) code
- Read a [Greek language translation](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/restoring-and-attributing-ancient-texts-using-deep-neural-networks/Ancient_Texts_(Greek).pdf) of this blog

**Notes**

This work was done by a team including contributions from Yannis Assael, Thea Sommerschield, Brendan Shillingford, Mahyar Bordbar, John Pavlopoulos, Marita Chatzipanagiotou, Ion Androutsopoulos, Jonathan Prag, and Nando de Freitas. The Ithaca web interface was developed by Justin Grayston, Benjamin Maynard, and Ricardo Cardenas from Google Cloud.

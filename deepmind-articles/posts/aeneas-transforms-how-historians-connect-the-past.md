---
title: "Aeneas transforms how historians connect the past"
source: https://deepmind.google/blog/aeneas-transforms-how-historians-connect-the-past/
site: deepmind
date: 2025-07-23
authors: Aeneas team
crawled: 2026-09-13
---

Introducing the first model for contextualizing ancient inscriptions, designed to help historians better interpret, attribute and restore fragmentary texts.

Writing was everywhere in the Roman world — etched onto everything from imperial monuments to everyday objects. From political graffiti, love poems and epitaphs to business transactions, birthday invitations and magical spells, inscriptions offer modern historians rich insights into the diversity of everyday life across the Roman world.

Often, these texts are fragmentary, weathered or deliberately defaced. Restoring, dating and placing them is nearly impossible without contextual information, especially when comparing similar inscriptions.

Today, we’re publishing a [paper](https://www.nature.com/articles/s41586-025-09292-5) in Nature introducing [Aeneas](http://predictingthepast.com/?utm_source=&utm_medium=&utm_campaign=&utm_content=), the first artificial intelligence (AI) model for contextualizing ancient inscriptions.

When working with ancient inscriptions, historians traditionally rely on their expertise and specialized resources to identify “parallels” — which are texts that share similarities in wording, syntax, standardized formulas or provenance.

Aeneas greatly accelerates this complex and time-consuming work. It reasons across thousands of Latin inscriptions, retrieving textual and contextual parallels in seconds that allow historians to interpret and build upon the model’s findings.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Our model can also be adapted to other ancient languages, scripts and media, from papyri to coinage, expanding its capabilities to help draw connections across a wider range of historical evidence.

We co-developed Aeneas with the University of Nottingham, and in partnership with researchers at the Universities of Warwick, Oxford and Athens University of Economics and Business (AUEB). This work was part of a wider effort to explore how generative AI can help historians better identify and interpret parallels at scale.

We want this research to benefit as many people as possible, so we’re making an interactive version of Aeneas freely-available to researchers, students, educators, museum professionals and more at [predictingthepast.com](http://predictingthepast.com/?utm_source=&utm_medium=&utm_campaign=&utm_content=). To support further research, we’re also open-sourcing [our code and dataset](http://github.com/google-deepmind/predictingthepast).

## Aeneas’ advanced capabilities

Named after the wandering hero of Graeco-Roman mythology, Aeneas builds upon [Ithaca](https://deepmind.google/discover/blog/predicting-the-past-with-ithaca/), our earlier work using AI to restore, date and place ancient Greek inscriptions.

Aeneas goes a step further, helping historians interpret and contextualize a text, give meaning to isolated fragments, draw richer conclusions and piece together a better understanding of ancient history.

Our model’s advanced capabilities include:

- **Parallels search:** It searches for parallels across a vast collection of Latin inscriptions. By turning each text into a kind of historical fingerprint, Aeneas identifies deep connections that can help historians situate inscriptions within their broader historical context.
- **Processing multimodal input:** Aeneas is the first model to determine a text's geographical provenance using multimodal inputs. It analyzes both text and visual information, like images of an inscription.
- **Restoring gaps of unknown length:** For the first time, Aeneas can restore gaps in texts where the missing length is unknown. This makes it a more versatile tool for historians dealing with heavily damaged material.
- **State-of-the-art performance:** Aeneas sets a new state-of-the-art benchmark in restoring damaged texts and predicting when and where they were written.

![Dark, fragmented Roman bronze military diploma with incised Latin text against white background](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/bronze.gif)

Animation of a restored bronze military diploma from Sardinia 113/14 C.E. (*CIL* XVI, 60).

## How Aeneas works

Aeneas is a multimodal generative neural network that takes an inscription’s text and image as input. To train Aeneas, we curated a large and reliable dataset, drawing from decades of work by historians to create digital collections, especially the [Epigraphic Database Roma](https://zenodo.org/records/3575495) (EDR), [Epigraphic Database Heidelberg](https://zenodo.org/records/3575155) (EDH) and [Epigraphic Database Clauss Slaby](https://zenodo.org/records/7072337) (EDCS-ELT).

We cleaned, harmonized and linked these records into a single machine-actionable dataset that we refer to as the [Latin Epigraphic Dataset](http://github.com/google-deepmind/predictingthepast) (LED), comprising over 176,000 Latin inscriptions from across the ancient Roman world.

Our model uses a transformer-based decoder to process the textual input of an inscription. Specialized networks handle character restoration and dating using text, while geographical attribution also uses images of the inscriptions as input. The decoder retrieves similar inscriptions from the LED, ranked by relevance.

For each inscription, Aeneas’ contextualization mechanism retrieves a list of parallels using a technique called “embeddings” — encoding the textual and contextual information of each inscription into a kind of historical fingerprint containing details of what the text says, its language, when and where it came from, and how it relates to other inscriptions.

![Diagram showing the technical architecture of Aeneas, illustrating how it processes multimodal inputs (damaged text fragments and images of inscriptions) through a Torso decoder, Vision network, and specialized Task Heads to produce outputs like geographical province, date distribution, missing text restoration, and a list of contextual parallels ranked from a dataset.](https://lh3.googleusercontent.com/zQP7-nljtyONJHitREu1Xf_HqL0EI2QvFf28LGKsfBZw4WTGoETM1uqNPSYea3rS7aA4WAgYgfwvueQZ8Rkj80Jt-zN9UXcnd3kwQuRlnRe5LHPoMSQ=w1440)

Diagram of Aeneas’ architecture showing how the model takes text and image input to generate province, date and restoration predictions.

## State-of-the-art performance

Aeneas groups inscriptions by date of writing far more clearly than other general-purpose models also trained on Latin, as shown in the visualization below.

![Two scatter plots comparing the performance of Aeneas and a generic LLM in grouping Roman inscriptions by date. The Aeneas plot shows distinct, chronological clusters of color-coded data points ranging from 650 BCE to 800 CE, whereas the generic LLM plot shows a highly mixed, unorganized distribution.](https://lh3.googleusercontent.com/_fZt8LFZ8UCtCkFlgKZN7af848HnOY4KrM77JsxPCCwZ7xEk-t4SRwtrgXOqWcNhK9Nh0UPd8tHFgjPJMIHNo0xO0ZYd-iPilNcbfFf8kgAClcjD-w=w1440)

Uniform Manifold Approximation and Projection (UMAP) visualization illustrating the chronological attribution of Aeneas’ historically rich embeddings compared to generic large language model textual embeddings.

Aeneas restores damaged inscriptions with a Top-20 accuracy of 73% in gaps of up to ten characters. This only decreases to 58% when the restoration length is unknown - itself an incredibly challenging task. It also shows its reasoning in an interpretable way, providing saliency maps that highlight which parts of the inputs influenced its predictions. Thanks to its use of visual data, our model can attribute an inscription to one of 62 ancient Roman provinces with 72% accuracy. For dating, Aeneas places a text within 13 years of the date ranges provided by historians.

## A new lens on historical debates

To test Aeneas’ capabilities on an ongoing research debate, we gave it one of the most famous Roman inscriptions: the *Res Gestae Divi Augusti,* Emperor Augustus’ first-person account of his achievements.

Historians have long-argued about the dating of this inscription. Rather than predicting a single fixed date, Aeneas produced a detailed distribution of possible dates, showing two distinct peaks, with one smaller peak around 10-1  BCE and a larger, more confident peak between 10-20 CE. These results captured both prevailing dating hypotheses in a quantitative way.

![A probability distribution chart of the Res Gestae Divi Augusti dating, showing the model’s predictions in blue and the two main historical debate hypotheses highlighted in purple, with a peak model prediction at 15 CE.](https://lh3.googleusercontent.com/7U-MZdGGrZHfsnyLWFmrBTxDohuDGJDTZfgDMgqAhVKQ8omHx5ti8l_gZywERPdLdyxw9N20e0SNmz6TiiV5hFgUD5BH2zXTua_EUXIjbzQsBmTa9Q=w1440)

Histogram showing Aeneas’ chronological attribution prediction for the *Res Gestae*, which models scholarly debates around dating this famous inscription.

Aeneas based its predictions on subtle linguistic features and historical markers such as official titles and monuments mentioned in the text. By turning the dating question into a probabilistic estimate grounded in linguistic and contextual data, our model offers a new, quantitative way of engaging with long-standing historical debates.

Most importantly, Aeneas also retrieved many relevant parallels from imperial legal texts tied to Augustus’ legacy, highlighting how the ideology of empire was reproduced across media and geography.

## Advancing historical research collaboratively

To assess Aeneas’ impact as an aid for research, we conducted a large-scale Historian and AI collaborative study. We invited twenty-three historians who regularly work with inscriptions to restore, date and place a set of texts using Aeneas.

Our evaluation, summarized in the table below, shows how the most effective results were achieved when historians used Aeneas’ contextual information alongside its predictions for restoring and attributing Roman inscriptions.

![A table summarizing the performance evaluation of different methods—Onomastics baseline, Historian, Historian with Aeneas parallels, Historian with Aeneas parallels and predictions, and Aeneas alone—across metrics such as character error rate (CER) in restoration, province accuracy, date prediction distance, historian confidence, potential as a research starting point, and number of parallels added. It shows that combining historians with Aeneas’ parallels and predictions yields the best overall results.](https://lh3.googleusercontent.com/lj_ZyKrAdWJHzI78rd2RV2NzRlV_QgurcQDyvlN30cNg9VJNnbPXIW8NKxHvPCWC9U-vGhsis39WQ3Oj2pn0J5zKMUgks3BeKt5TLTyhbNitH22g998=w1440)

Table showing historians’ performance on three epigraphic tasks (restoration, geographical attribution, dating) using 60 inscriptions from our database test set. Tasks were first performed independently, then with Aeneas’ parallels information, or parallels and predictions together.

Aeneas helped the historians in our study identify new parallels and increased their confidence when tackling complex epigraphic tasks. Historians consistently highlighted Aeneas’ value in accelerating their work and expanding the range of most relevant parallel inscriptions.

> Aeneas’ parallels completely changed my perception of the inscription. It noticed details that made all the difference for restoring and chronologically attributing the text.

Anonymised historian from our study

## Sharing the tools, shaping the future

Aeneas is designed to integrate within historians' existing research workflows. By combining expert knowledge with machine learning, it opens up a collaborative process, offering interpretable suggestions that serve as valuable starting points for historical inquiry.

As part of today’s release, we’re upgrading [Ithaca](https://deepmind.google/discover/blog/predicting-the-past-with-ithaca/), our ancient Greek model, to be powered by Aeneas and include the contextualization function, restorations of unknown length and better performance overall.

We’ve also co-designed a new [teaching syllabus](https://www.robbewulgaert.be/education/predicting-the-past-aeneas) for bridging technical skills with historical thinking in the classroom. This syllabus aligns with AI literacy initiatives, including the European Commission's [Digital Competences Framework for Citizens](https://publications.jrc.ec.europa.eu/repository/handle/JRC128415) (DigComp 2.2), UNESCO’s [AI Competency Framework for Students](https://www.unesco.org/en/articles/ai-competency-framework-students), and the preview of European Commission and the Organization for Economic Cooperation and Development (OECD) [AILit Framework](https://ailiteracyframework.org/about/).

The Aeneas team is continuing to partner with diverse subject matter experts, using Aeneas to help shed light to our ancient past — with more to come.

**Learn more about Aeneas**

[Read our paper](https://www.nature.com/articles/s41586-025-09292-5)[Try Aeneas](http://predictingthepast.com/)[Get the code and dataset](http://github.com/google-deepmind/predictingthepast)[Read our blog in Italian](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/aeneas-transforms-how-historians-connect-the-past/aeneas-transforms-how-historians-connect-the-past-italian-version.pdf)[Read our blog in Greek](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/aeneas-transforms-how-historians-connect-the-past/aeneas-transforms-how-historians-connect-the-past-greek-version.pdf)

**Acknowledgements**

The research was co-led by Yannis Assael and Thea Sommerschield.

Contributors include: Alison Cooley, Brendan Shillingford, John Pavlopoulos, Priyanka Suresh, Bailey Herms, Jonathan Prag, Alex Mullen and Shakir Mohamed. The Aeneas web interface was developed by Justin Grayston, Benjamin Maynard, and Nicholas Dietrich, and is powered by Google Cloud.

The syllabus was developed by Robbe Wulgaert, Sint-Lievenscollege, Ghent, Belgium.

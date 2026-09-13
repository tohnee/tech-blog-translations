---
title: "Restoring ancient text using deep learning: a case study on Greek epigraphy"
source: https://deepmind.google/blog/restoring-ancient-text-using-deep-learning-a-case-study-on-greek-epigraphy/
site: deepmind
date: 2019-10-15
authors: Yannis Assael, Thea Sommerschield, Jonathan Prag
crawled: 2026-09-13
---

Historians rely on different sources to reconstruct the thought, society and history of past civilisations. Many of these sources are text-based – whether written on scrolls or carved into stone, the preserved records of the past help shed light on ancient societies. However, these records of our ancient cultural heritage are often incomplete: due to deliberate destruction, or erosion and fragmentation over time. This is the case for inscriptions: texts written on a durable surface (such as stone, ceramic, metal) by individuals, groups and institutions of the past, and which are the focus of the discipline called [epigraphy](https://en.wikipedia.org/wiki/Epigraphy). Thousands of inscriptions have survived to our day; but the majority have suffered damage over the centuries, and parts of the text are illegible or lost (Figure 1). The reconstruction ("restoration") of these documents is complex and time consuming, but necessary for a deeper understanding of civilisations past.

One of the issues with discerning meaning from incomplete fragments of text is that there are often multiple possible solutions. In many word games and puzzles, players guess letters to complete a word or phrase – the more letters that are specified, the more constrained the possible solutions become. But unlike these games, where players have to guess a phrase in isolation, historians restoring a text can estimate the likelihood of different possible solutions based on other context clues in the inscription – such as grammatical and linguistic considerations, layout and shape, textual parallels, and historical context. Now, by using machine learning trained on ancient texts, we’ve built a system that can furnish a more complete and systematically ranked list of possible solutions, which we hope will augment historians’ understanding of a text.

![Photograph of a damaged and fragmented ancient stone slab featuring carved Greek inscriptions, illustrating the challenge of restoring incomplete historical texts.](https://lh3.googleusercontent.com/6St-mHlvrbnx-TxQDdp4AaznvkIlsm796RI7l4prcpdjvvq-lde7ZdFiB_C8UTmDkEm9xUsaDUcV9rD6ilqG_T1jTiklcs3xGKJwuwfIwb9lsaE_8A=w1440)

Figure 1: Damaged inscription: a decree of the Athenian Assembly relating to the management of the Acropolis (dating 485/4 BCE). IG I3 4B. (CC BY-SA 3.0, WikiMedia)

## Pythia

Pythia – which takes its name from the woman who delivered the god Apollo's oracular responses at the Greek sanctuary of Delphi – is the first ancient text restoration model that recovers missing characters from a damaged text input using deep neural networks. Bringing together the disciplines of ancient history and deep learning, the present work offers a fully automated aid to the text restoration task, providing ancient historians with multiple textual restorations, as well as the confidence level for each hypothesis.

Pythia takes a sequence of damaged text as input, and is trained to predict character sequences comprising hypothesised restorations of ancient Greek inscriptions (texts written in the Greek alphabet dating between the seventh century BCE and the fifth century CE). The architecture works at both the character- and word-level, thereby effectively handling long-term context information, and dealing efficiently with incomplete word representations (Figure 2). This makes it applicable to all disciplines dealing with ancient texts ([philology](https://en.wikipedia.org/wiki/Philology), [papyrology](https://en.wikipedia.org/wiki/Papyrology), [codicology](https://en.wikipedia.org/wiki/Codicology)) and applies to any language (ancient or modern).

![A diagram of Pythia's neural network architecture, showing how character and word embeddings—including missing characters marked with red question marks—are processed through encoder states with attention mechanism to decode and predict the missing Greek characters, "gamma" and "alpha."](https://lh3.googleusercontent.com/ZeGSNfVOO6Qn4OPmLCh_8tQC5zH7A0m4f2Ut4bQoEAap58Bky9keEiiYgU4DgtNH3USXMw79_GaLIaEeCnTKpEQSAwjpZLK1TzPRmAaCnZdgZR_62Q=w1440)

Figure 2: Pythia processing the phrase μηδέν ἄγαν (Mēdèn ágan) "nothing in excess," a fabled maxim inscribed on Apollo’s temple in Delphi. The letters "γα" are the characters to be predicted, and are annotated with ‘?’. Since ἄ??ν is not a complete word, its embedding is treated as unknown (‘unk’). The decoder outputs correctly "γα".

## Experimental evaluation

To train Pythia, we wrote a non-trivial pipeline to convert the largest digital corpus of ancient Greek inscriptions ([PHI Greek Inscriptions](https://epigraphy.packhum.org/)) to machine actionable text, which we call PHI-ML. As shown in Table 1, Pythia’s predictions on PHI-ML achieve a 30.1% character error rate, compared to the 57.3% of evaluated human ancient historians (specifically, these were PhD students from Oxford). Moreover, in 73.5% of cases the ground-truth sequence was among the Top-20 hypotheses of Pythia, which effectively demonstrates the impact of this assistive method on the field of digital epigraphy, and sets the state-of-the-art in ancient text restoration.

![Table 1: A comparison of ancient text restoration methods showing Character Error Rate (CER) and Top-20 accuracy, where Pythia-Bi-Word achieves the lowest CER at 30.1% and the highest Top-20 accuracy at 73.5% compared to ancient historians at 57.3% CER.](https://lh3.googleusercontent.com/PrVvoB5lHweiZaiyCuboLb4Dl6PBVvUKwGWLJC1DaQJy7qWx7hC-UdcMulMla7_Y1TpzUT4-5AGuaQoGCJnbWlsWjuMAe-h8PvCfzNKExWR_BoJMLQ=w1440)

Table 1: Pythia's Predictive performance of on PHI-ML.

## The importance of context

To evaluate Pythia’s receptiveness to context information and visualise the attention weights at each decoding step, we experimented with the modified lines of an inscription from the city of Pergamon (in modern-day Turkey)\*. In the text of Figure 3, the last word is a Greek personal name ending in -ου. We set ἀπολλοδώρου ("Apollodorou") as the personal name, and hid its first 9 characters. This name was specifically chosen because it already appeared within the input text. Pythia attended to the contextually-relevant parts of the text - specifically, ἀπολλοδώρου. The sequence ἀπολλοδώρ was predicted correctly. As a litmus test, we substituted ἀπολλοδώρου in the input text with another personal name of the same length: ἀρτεμιδώρου ("Artemidorou"). The predicted sequence changed accordingly to ἀρτεμιδώρ, thereby illustrating the importance of context in the prediction process.

![A visualization of Pythia's attention weights across four decoding steps as it predicts the missing Greek characters—represented by question marks—for the name "Apollodorou" based on its prior appearance in the context.](https://lh3.googleusercontent.com/cW3PAl3WIEyX8rz_GCSscSWFj86CBaBj7B3gK2r8bEAU7vTFOQ45g7kSO_7Gj7FNMDGTnc9Yt25XVXeELyWTLZZa1uovntW6uhO5W-TAncFRXRbT=w1440)

Figure 3: Visualisation of the attention weights for the decoding of the first 4 missing characters. To aid visualisation, the weights within the area of the characters to be predicted (‘?’) are in green, and in blue for the rest of the text; the magnitude of the weights is represented by the colour intensity. The ground-truth text ἀπολλοδώρ appears in the input text, and Pythia attends to the relevant parts of the sequence.

## Future research

The combination of machine learning and epigraphy has the potential to impact meaningfully the study of inscribed texts, and widen the scope of the historian’s work. For this reason, we have open-sourced an online Python notebook, Pythia, and PHI-ML’s processing pipeline at <https://github.com/sommerschield/ancient-text-restoration>, collaborating with scholars at the University of Oxford. By so doing, we hope to aid future research and inspire further interdisciplinary work.

**Notes**

\*Specifically, lines b.8- c.5 of the inscription MDAI(A) 32 (1907) 428, 275.

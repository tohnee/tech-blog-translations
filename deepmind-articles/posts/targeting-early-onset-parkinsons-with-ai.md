---
title: "Targeting early-onset Parkinson’s with AI"
source: https://deepmind.google/blog/targeting-early-onset-parkinsons-with-ai/
site: deepmind
date: 2022-09-21
authors: 
crawled: 2026-09-13
---

AlphaFold predictions are paving the way towards new treatments that can impact over 10 million people worldwide

It was a source of hard-earned satisfaction after what had often felt like an uphill battle. David Komander and his colleagues had finally published the long-sought structure of PINK1. Mutations in the gene that encodes this protein cause early-onset Parkinson’s, a neurodegenerative disease with a wide range of progressive symptoms – particularly body tremors and difficulty in moving. But when other scientific teams published their own structures for the same protein, it became clear that something was amiss.

“The other two structures that came out looked very different to the structure that had been done by our group,” says Zhong Yan Gan, a PhD student in [Komander’s lab](https://www.wehi.edu.au/people/david-komander), co-supervised by Associate Professor Grant Dewson, at WEHI (the Walter and Eliza Hall Institute of Medical Research) in Melbourne, Australia. Theirs was the odd one out, with unique features that didn’t appear to exist in the others. The stakes were high: understanding PINK1 could help to unlock new treatments addressing the fundamental cause of Parkinson’s, which [affects more than 10 million people worldwide](https://www.parkinson.org/understanding-parkinsons/statistics).

While Komander’s team had confidence in their own findings, the contrasting results raised some big questions. And in a competitive research field, they knew they wouldn’t be alone in hunting for answers. “Not only were these really difficult nuts to crack, but, once they were cracked, you suddenly open this entire realm of everybody doing very similar things,” says Komander.

![Female and male scientist in a lab.](https://lh3.googleusercontent.com/rt-Hf8fOFHDki2h0US5p00_wuAUXrJTq1KP-II-ZQvwjJOn2BEf7f4c3DJVySHLDgIToSaXsjeP3GdCUeqQV7S4JS3BCQR6c7u2OF1sqtDrn9M7QgDw=w1440)

Credit: Jacinta Moore

The team eventually unraveled the mystery, but it took several more years of research, one chance discovery, and a helping hand from DeepMind’s protein-structure prediction system, AlphaFold.

The [symptoms of Parkinson’s](https://www.parkinsons.org.uk/information-and-support/what-parkinsons) develop when someone’s brain can no longer make enough of the chemical dopamine. Most people who get Parkinson’s won’t know the specific cause, but around 10% of patients can point to [a particular genetic mutation](https://www.michaeljfox.org/news/parkinsons-genetics). In these cases, Parkinson’s tends to develop early, affecting people [before they reach the age of 50](https://www.michaeljfox.org/news/young-onset-parkinsons-disease).

One of those genetic mutations is in the gene that encodes the [PINK1](https://en.wikipedia.org/wiki/PINK1) protein. PINK1 plays a key role in the breakdown and removal of mitochondria, often referred to as the powerhouses inside our cells. “As you age, mitochondria can become old and damaged,” says Gan. “PINK1 is part of the body’s mechanism to recycle old mitochondria to make way for new ones.”

When this mechanism falters, the damaged mitochondria build up, leading to the loss of dopamine-producing nerve cells, and eventually to Parkinson’s. So one avenue to finding better ways to treat the condition is to better [understand PINK1 and its role](https://molecularneurodegeneration.biomedcentral.com/articles/10.1186/s13024-020-00367-7).

![Two scientists performing a complex-looking task in a laboratory. They are surrounded by equipment.](https://lh3.googleusercontent.com/QkUaGq3uaj64nyePQgTltbvUgdbdwD6OOani-SD6TzjRggwEk2v3xc-U2htPJlpIk-MiQcg3XBzbGpeyCS19IZL2beNO9Jx7HFQs-C3Jm-3WAzW2Nzs=w1440)

Credit: Jacinta Moore

When researchers discovered that [PINK1 could cause Parkinson’s disease](https://www.science.org/doi/10.1126/science.1096284) in 2004, finding its structure became a key goal – but it was not forthcoming, in part because human PINK1 was too unstable to produce in the lab. Pushed to cast their net wider, scientists discovered that insect versions of PINK1 – such as that from human body lice – were stable enough to produce and study in the lab.

Which brings us back to our story’s start. Komander’s team published their [PINK1 structure](https://www.nature.com/articles/nature24645) in 2017. But when other researchers published different structures for the same protein from a different insect (flour beetles), they knew they only had part of the story. It wasn’t entirely surprising. After all, proteins are dynamic molecules. “They're like machines, and they can take different shapes,” says Gan. What if the published structure was just one of those shapes – a snapshot of PINK1 during a single stage of a longer process?

> We had these new structures and, at the time, we were the only people on the planet to know what PINK1 looks like during activation

David Komander

Biochemist

Gan took on the ambitious task of figuring out what PINK1 looks like during every step of its activation process as his PhD project. It was during this work that he spotted something odd: a molecule that looked far too big to be his target. “Normally you would disregard it as something that has just clumped together, like a scrambled egg white kind-of-thing,” says Komander.

But Gan had a hunch that this clump was worth investigating in greater detail, and decided, with the help of Dr Alisa Glukhova, to probe the molecule at the atomic scale using [cryo-electron microscopy](https://www.chemistryworld.com/news/explainer-what-is-cryo-electron-microscopy/3008091.article) (cryo-EM), whereby a frozen sample is examined using a beam of electrons. “I remember saying to Zhong, ‘Yeah, you can try it, but that's never gonna work’,” Komander admits.

Gan’s persistence paid off in spades. What he discovered was the very molecule the researchers were looking for: PINK1. But why so big? It turned out that PINK1 likes company. Instead of a single protein, it was grouped together into pairs of molecules known as dimers, which had arranged themselves into still larger formations. “Six dimers of PINK1 were assembling into large, bagel-shaped structures,” says Gan.

![A photograph of a people inside David Komander's office. We are looking through the glass from the corridor. Two people are standing behind Komander and watching what he is doing on the computer.](https://lh3.googleusercontent.com/pG_bDFJQqMT0yr9sQPV4usbcyQJx5sCWaf3wInbDMgS8OyLYgyXtiMo2h2s3oYU1YfY0OQdvXmaHowDCpInLLq2KgxigfguOJ0ZZdoYxA_S1qrVndpk=w1440)

Credit: Jacinta Moore

This chance discovery meant he could use cryo-EM, which wouldn’t work for a molecule as small as a single PINK1, to solve the protein’s physical structure. The team had their answer.

The previously published structures of PINK1 were no mistake – they were different forms that the protein takes at various stages of its activation process. But there was a catch. All of this experimental work had been done using PINK1 derived from insects. To understand the implications of their findings for humans with Parkinson’s, they would have to investigate whether their findings extended to the human version of the protein.

Komander and his team turned to AlphaFold. “We had these new structures and, at the time, we were the only people on the planet to know what PINK1 looks like during activation,” says Komander. So they used AlphaFold to call up its prediction for the structure of [human-sourced PINK1](https://alphafold.ebi.ac.uk/entry/Q9BXM7), and moments later there it was on the screen. It was “completely shocking” how accurate the AlphaFold predictions were, he says.

Later, when Gan put two protein sequences into AlphaFold to predict the structure of a PINK1 dimer in humans, the result was almost indistinguishable from his experimental work with the insect protein. “That dimer was basically showing exactly how these two proteins interact so that they can act and work together to form some of these complexes that we had seen,” says Komander.

> We can start to think about, 'What kind of drugs do we have to develop to fix the protein, rather than just deal with the fact that it's broken'

David Komander

This close alignment between several experimental results and AlphaFold’s predicted structures gave the team confidence that the AI system could deliver meaningful knowledge beyond their empirical work. They went on to use AlphaFold to model what effect certain mutations would have on the formation of the dimer – to explore how those mutations might lead to Parkinson’s, and their suspicions were confirmed.

“We were able to immediately generate some real insights for people who have these particular mutations,” says Komander. These insights could ultimately lead to new treatments. "We can start to think about, 'What kind of drugs do we have to develop to fix the protein, rather than just deal with the fact that it's broken,'" says Komander.

They submitted their findings on the [activation mechanism of PINK1](https://www.nature.com/articles/s41586-021-04340-2) to the journal Nature in August 2021 and the paper was accepted in early December 2021. It turned out that researchers at the Trempe Lab in Montreal, Canada, had arrived at similar conclusions, and when that team's paper was published in December 2021, the WEHI authors had to fast-track final revisions. “We were told to finish the paper three days before Christmas, so that it could be published in 2021,” says Komander. “It was a brutal timeline.”

![David Komander showing his colleagues work on his computer screen. He looks very pleased with the work.](https://lh3.googleusercontent.com/d1ev982yS5u65xrJ2MZZ3dsIbr1NXk4dhYQH24Fuj_qw70P5J7vYz0C9YWeTDHI3ktNQ8DxfQBNpY66xWNMB5xvjpT_99L9Gey0MjGFyIUB_EeBk=w1440)

Credit: Jacinta Moore

In the end, these [high-profile papers](https://www.nature.com/articles/s41594-022-00733-7) came out within weeks of each other, both contributing vital insights into the molecular basis of Parkinson’s.

Plenty of questions remain for researchers in the field, of course, and AlphaFold is freely available to help them reach some of the answers. For example, Sylvie Callegari, a senior postdoctoral researcher in Komander’s lab, has used AlphaFold to find the structure of a large protein called VPS13C – known to cause Parkinson’s – by piecing together smaller fragments of protein.

“Now, we can start asking different questions,” she says. “Instead of ‘What does it look like?’ we can start asking, ‘How does it work?’, ‘How do mutations in this protein cause disease?'"

One of the many goals of AlphaFold is to accelerate medical research, and it is also being applied at WEHI to the gene sequences of people with early-onset Alzheimer’s to allow researchers to investigate the causes of individual cases. “AlphaFold allows us to do that based on fantastic and correct human models,” says Komander. “That is very powerful.”

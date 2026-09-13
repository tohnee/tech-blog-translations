---
title: "How our principles helped define AlphaFold’s release"
source: https://deepmind.google/blog/how-our-principles-helped-define-alphafolds-release/
site: deepmind
date: 2022-09-14
authors: Koray Kavukcuoglu, Pushmeet Kohli, Lila Ibrahim, Dawn Bloxwich, Sasha Brown
crawled: 2026-09-13
---

Reflections and lessons on sharing one of our biggest breakthroughs with the world

Putting our mission of solving intelligence to advance science and benefit humanity into practice comes with crucial responsibilities. To help create a positive impact for society, we must proactively evaluate the ethical implications of our research and its applications in a rigorous and careful way. We also know that every new technology has the potential for harm, and we take long and short term risks seriously. We’ve built our foundations on pioneering responsibly from the outset – especially focused on responsible governance, research, and impact.

This starts with setting clear principles that help realise the benefits of artificial intelligence (AI), while mitigating its risks and potential negative outcomes. Pioneering responsibly is a collective effort, which is why we’ve contributed to many AI community standards, such as those developed by [Google](https://ai.google/principles/), the [Partnership on AI](https://partnershiponai.org/about/#tenets), and the [OECD](https://oecd.ai/en/ai-principles) (Organisation for Economic Co-operation and Development).

Our [Operating Principles](https://www.deepmind.com/about/operating-principles) have come to define both our commitment to prioritising widespread benefit, as well as the areas of research and applications we refuse to pursue. These principles have been at the heart of our decision making since DeepMind was founded, and continue to be refined as the AI landscape changes and grows. They are designed for our role as a research-driven science company and consistent with Google’s AI Principles.

![An abstract purple and white circular infographic representing DeepMind's Operating Principles, showing a central brain-shaped tree of knowledge surrounded by icons of humans, science, ethics, and social benefit, with a matrix of dots and pathways underneath.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6320ad58719cb46c966a7b59_Op_Fig_1.svg)

## From principles to practice

Written principles are only part of the puzzle – how they’re put into practice is key. For complex research being done at the frontiers of AI, this brings significant challenges: How can researchers predict potential benefits and harms that may occur in the distant future? How can we develop better ethical foresight from a wide range of perspectives? And what does it take to explore hard questions alongside scientific progress in realtime to prevent negative consequences?

We’ve spent many years developing our own skills and processes for responsible governance, research, and impact across DeepMind, from creating internal toolkits and publishing papers on sociotechnical issues to supporting efforts to increase deliberation and foresight across the AI field. To help empower DeepMind teams to pioneer responsibly and safeguard against harm, our interdisciplinary Institutional Review Committee (IRC) meets every two weeks to carefully evaluate DeepMind projects, papers, and collaborations.

Pioneering responsibly is a collective muscle, and every project is an opportunity to strengthen our joint skills and understanding. We’ve carefully designed our review process to include rotating experts from a wide range of disciplines, with machine learning researchers, ethicists, and safety experts sitting alongside engineers, security experts, policy professionals, and more. These diverse voices regularly identify ways to expand the benefits of our technologies, suggest areas of research and applications to change or slow, and highlight projects where further external consultation is needed.

While we’ve made a lot of progress, many aspects of this lie in uncharted territory. We won’t get it right every time and are committed to continual learning and iteration. We hope sharing our current process will be useful to others working on responsible AI, and encourage feedback as we continue to learn, which is why we’ve detailed reflections and lessons from one of our most complex and rewarding projects: AlphaFold. Our AlphaFold AI system solved the 50-year-old challenge of protein structure prediction – and we’ve been thrilled to see scientists using it to accelerate progress in fields such as sustainability, food security, drug discovery, and fundamental human biology since releasing it to the wider community last year.

![An abstract circular infographic on a light purple background representing DeepMind's Operating Principles, showing a central globe surrounded by icons representing green energy, education, health, science, and social benefit. Underneath, text reads: "We commit to: 1. Social Benefit, 2. Scientific excellence and integrity".](https://lh3.googleusercontent.com/NgIB9WAq4ZS7aLmtFZMs_PAl0qfpsbI21BzykZh3wE45U7RVOmyyeHrg3rnMzazVR7C_hzfmmEZNiLStP9K3VprflHEtWE5JFIOsm_O2BdqXTb_VcA=w1440)

## Focusing on protein structure prediction

Our team of machine learning researchers, biologists, and engineers had long seen the protein-folding problem as a remarkable and unique opportunity for AI-learning systems to create a significant impact. In this arena, there are standard measures of success or failure, and a clear boundary to what the AI system needs to do to help scientists in their work – predict the three-dimensional structure of a protein. And, as with many biological systems, protein folding is far too complex for anyone to write the rules for how it works. But an AI system might be able to learn those rules for itself.

Another important factor was the biennial assessment, known as [CASP](https://predictioncenter.org/) (the Critical Assessment of protein Structure Prediction), which was [founded by Professor John Moult and Professor Krzysztof Fidelis](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.340230303). With each gathering, CASP provides an exceptionally robust assessment of progress, requiring participants to predict structures that have only recently been discovered through experiments. The results are a great catalyst for ambitious research and scientific excellence.

![An abstract purple and white circular infographic representing DeepMind's Operating Principles, showing a central set of balance scales representing safety and ethics, surrounded by icons of humans, shields, and graphs. Underneath, text reads: "We commit to: 3. Safety and ethics, 4. Accountability to people. We will not pursue: 7. Technologies that cause or are likely to cause overall harm... 8. Weapons... 9. Technologies that gather or use information for surveillance... 10. Technologies whose purpose contravenes... international law and human rights."](https://lh3.googleusercontent.com/JxzOruBnwCI7w3fZwsYOj4v9ocD7Kah-XSzaDirprLFp7KnxuGhYeW00THiHZTRGYf9ZOKkJP_s9GM11ejGN-N55hf7MJCyfWy0vhKnHlF6r1KFGL1c=w1440)

## Understanding practical opportunities and risks

As we prepared for the CASP assessment in 2020, we realised that AlphaFold showed great potential for solving the challenge at hand. We spent considerable time and effort analysing the practical implications, questioning: How could AlphaFold accelerate biological research and applications? What might be the unintended consequences? And how could we share our progress in a responsible way?

This presented a wide range of opportunities and risks to consider, many of which were in areas where we didn’t necessarily have strong expertise. So we sought out external input from over 30 field leaders across biology research, biosecurity, bioethics, human rights, and more, with a focus on diversity of expertise and background.

**Many consistent themes came up throughout these discussions:**

1. **Balancing widespread benefit with the risk of harm.** We started with a cautious mindset about the risk of accidental or deliberate harm, including how AlphaFold might interact with both future advances and existing technologies. Through our discussions with external experts, it became clearer that AlphaFold would not make it meaningfully easier to cause harm with proteins, given the many practical barriers to this – but that future advances would need to be evaluated carefully. Many experts argued strongly that AlphaFold, as an advance relevant to many areas of scientific research, would have the greatest benefit through free and widespread access.
2. **Accurate confidence measures are essential for responsible use.** Experimental biologists explained how important it would be to understand and share well-calibrated and usable confidence metrics for each part of AlphaFold’s predictions. By signalling which of AlphaFold’s predictions are likely to be accurate, users can estimate when they can trust a prediction and use it in their work – and when they should use alternative approaches in their research. We had initially considered omitting predictions for which AlphaFold had low confidence or high predictive uncertainty, but the external experts we consulted proved why this was especially important to retain these predictions in our release, and advised us on the most useful and transparent ways to present this information.
3. **Equitable benefit could mean extra support for underfunded fields.** We had many discussions about how to avoid inadvertently increasing disparities within the scientific community. For example, so-called [neglected tropical diseases](https://www.who.int/health-topics/neglected-tropical-diseases#tab=tab_1), which disproportionately affect poorer parts of the world, often receive less research funding than they should. We were strongly encouraged to prioritise hands-on support and proactively look to partner with groups working on these areas.

![An abstract circular infographic on a light purple background representing DeepMind's Operating Principles, showing a central speech bubble representing communication and consultation surrounded by icons representing global collaboration, diversity, science, and social benefit. Underneath, text reads: "We commit to: 5. Sharing knowledge responsibly, 6. Diversity, equity, and inclusion".](https://lh3.googleusercontent.com/P2OnwM-DLFotFuH3yxSEgr1r7PQG7015l-BZIAElBfkcd4d20jKO5DeMP_Lv9OQsLkenczjmw2QyEIeIGJk2NrxSa46WouwEKfldzcpKwAdURgW9BA=w1440)

## Establishing our release approach

**Based on the input above, the IRC endorsed a set of AlphaFold releases to address multiple needs, including:**

- **Peer-reviewed publications and open source code,** including [two](https://www.nature.com/articles/s41586-021-03819-2) [papers](https://www.nature.com/articles/s41586-021-03828-1) in Nature, accompanied by [open source code](https://github.com/deepmind/alphafold/), to enable researchers to more easily implement and improve on AlphaFold. Soon after, we added a [Google Colab](https://colab.sandbox.google.com/github/deepmind/alphafold/blob/main/notebooks/AlphaFold.ipynb) allowing anyone to input a protein sequence and receive a predicted structure, as an alternative to running the open source code themselves.
- **A major release of protein structure predictions** in partnership with [EMBL-EBI](https://www.ebi.ac.uk/) (EMBL’s European Bioinformatics Institute), the established community leader. As a public institution, EMBL-EBI enables anyone to look up protein structure predictions as easily as a Google search. The initial release included predicted shapes for every protein in the human body, and our [most recent update](https://deepmind.google/blog/alphafold-reveals-the-structure-of-the-protein-universe/) included predicted structures for nearly all catalogued proteins known to science. This totals over 200 million structures, all freely available on EMBL-EBI’s website with open access licences, accompanied by support resources, such as [webinars](https://www.ebi.ac.uk/training/events/how-interpret-alphafold-structures/) on interpreting these structures.
- **Building 3D visualisations into the database,** with prominent labelling for high-confidence and low-confidence areas of the prediction, and, in general, aiming to be as clear as possible about AlphaFold’s strengths and limitations in our documentation. We also designed the database to be as accessible as possible, for example, considering the needs of people with colour vision deficiency.
- **Forming deeper partnerships with research groups working on underfunded areas,** such as neglected diseases and topics critical to global health. This includes [DNDi](https://dndi.org/) (Drugs for Neglected Disease initiative), which is advancing research into Chagas disease and leishmaniasis, and the [Centre for Enzyme Innovation](https://www.port.ac.uk/research/research-centres-and-groups/centre-for-enzyme-innovation) which is developing plastic-eating enzymes to help reduce plastic waste in the environment. Our growing public engagement teams are continuing to work on these partnerships to support more collaborations in the future.

## How we’re building upon this work

Since our initial release, hundreds of thousands of people from over 190 countries have visited the [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/) and used the [AlphaFold open source code](https://github.com/deepmind/alphafold/) since launch. We’ve been honoured to hear of ways in which AlphaFold’s predictions have accelerated important scientific efforts and are working to tell some of these stories with our [Unfolded](https://unfolded.deepmind.com/) project. So far, we’re not aware of any misuse or harm related to AlphaFold, though we continue to pay close attention to this.

While AlphaFold was more complex than most DeepMind research projects, we’re using elements of what we’ve learned and incorporating this into other releases.

**We’re building upon this work by:**

- **Increasing the range of input from external experts** at every stage of the process, and exploring mechanisms for participatory ethics at greater scale.
- **Widening our understanding of AI for biology** in general, beyond any individual project or breakthrough, to develop a stronger view of the opportunities and risks over time.
- **Finding ways to expand our partnerships** with groups in fields that are underserved by current structures.

Just like our research, this is a process of continual learning. The development of AI for widespread benefit is a community effort that spans far beyond DeepMind.

We’re making every effort to be mindful of how much hard work there still is to do in partnership with others – and how we pioneer responsibly going forward.

---
title: "AI achieves silver-medal standard solving International Mathematical Olympiad problems"
source: https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/
site: deepmind
date: 2024-07-25
authors: AlphaProof team, AlphaGeometry team
crawled: 2026-09-13
---

Breakthrough models AlphaProof and AlphaGeometry 2 solve advanced reasoning problems in mathematics

*Note: This blog was first published on July 25, 2024. On November 12, 2025, we published the methodology behind AlphaProof in an* [*article in Nature*](https://www.nature.com/articles/s41586-025-09833-y)

Artificial general intelligence (AGI) with advanced mathematical reasoning has the potential to unlock new frontiers in science and technology.

We’ve made great progress building AI systems that help mathematicians discover [new insights](https://deepmind.google/discover/blog/exploring-the-beauty-of-pure-mathematics-in-novel-ways/), [novel algorithms](https://deepmind.google/discover/blog/discovering-novel-algorithms-with-alphatensor/) and answers to [open problems](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/). But current AI systems still struggle with solving general math problems because of limitations in reasoning skills and training data.

Today, we present AlphaProof, a new reinforcement-learning based system for formal math reasoning, and AlphaGeometry 2, an improved version of our [geometry-solving system](https://deepmind.google/discover/blog/alphageometry-an-olympiad-level-ai-system-for-geometry/). Together, these systems solved four out of six problems from this year’s [International Mathematical Olympiad](https://www.imo2024.uk/) (IMO), achieving the same level as a silver medalist in the competition for the first time.

## Breakthrough AI performance solving complex math problems

The IMO is the oldest, largest and most prestigious competition for young mathematicians, held annually since 1959.

Each year, elite pre-college mathematicians train, sometimes for thousands of hours, to solve six exceptionally difficult problems in algebra, combinatorics, geometry and number theory. Many of the winners of the [Fields Medal](https://www.mathunion.org/imu-awards/fields-medal), one of the highest honors for mathematicians, have represented their country at the IMO.

More recently, the annual IMO competition has also become widely recognised as a grand challenge in machine learning and an aspirational benchmark for measuring an AI system’s advanced mathematical reasoning capabilities.

This year, we applied our combined AI system to the competition problems, provided by the IMO organizers. Our solutions were scored according to the IMO’s point-awarding rules by prominent mathematicians [Prof Sir Timothy Gowers](https://www.dpmms.cam.ac.uk/~wtg10/), an IMO gold medalist and Fields Medal winner, and [Dr Joseph Myers](https://www.polyomino.org.uk/), a two-time IMO gold medalist and Chair of the IMO 2024 Problem Selection Committee.

> The fact that the program can come up with a non-obvious construction like this is very impressive, and well beyond what I thought was state of the art.

Prof Sir Timothy Gowers

IMO gold medalist and Fields Medal winner

First, the problems were manually translated into formal mathematical language for our systems to understand. In the official competition, students submit answers in two sessions of 4.5 hours each. Our systems solved one problem within minutes and took up to three days to solve the others.

AlphaProof solved two algebra problems and one number theory problem by determining the answer and proving it was correct. This included the hardest problem in the competition, solved by only five contestants at this year’s IMO. AlphaGeometry 2 proved the geometry problem, while the two combinatorics problems remained unsolved.

[See our system's IMO 2024 solutions](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/imo-2024-solutions/index.html)

Each of the six problems can earn seven points, with a total maximum of 42. Our system achieved a final score of 28 points, earning a perfect score on each problem solved — equivalent to the top end of the [silver-medal category](https://www.imo-official.org/year_info.aspx?year=2024). This year, the gold-medal threshold starts at 29 points, and was achieved by [58 of 609 contestants](https://www.imo-official.org/year_individual_r.aspx?year=2024) at the official competition.

![Colored graph showing our AI system’s performance relative to human competitors earning bronze, silver and gold at IMO 2024. Our system earned 28 out of 42 total points, achieving the same level as a silver medalist in the competition and nearly reaching the gold-medal threshold starting at 29 points.](https://lh3.googleusercontent.com/iSMHpqQhw2pxSwyQiqpDGchZpJpOatzY0at6ok3Br8SvKYUun75o59u1ad32zgjOTcu9g5ZKAgZc0rDBcJXAU4tE6cph7dRf5svD4SEXV4aa827gyr0=w1440)

Graph showing performance of our AI system relative to human competitors at IMO 2024. We earned 28 out of 42 total points, achieving the same level as a silver medalist in the competition.

## AlphaProof: a formal approach to reasoning

AlphaProof is a system that trains itself to prove mathematical statements in the formal language [Lean](https://lean-lang.org/). It couples a pre-trained language model with the [AlphaZero](https://deepmind.google/discover/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/) reinforcement learning algorithm, which previously taught itself how to master the games of chess, shogi and Go.

Formal languages offer the critical advantage that proofs involving mathematical reasoning can be formally verified for correctness. Their use in machine learning has, however, previously been constrained by the very limited amount of human-written data available.

In contrast, natural language based approaches can hallucinate plausible but incorrect intermediate reasoning steps and solutions, despite having access to orders of magnitudes more data. We established a bridge between these two complementary spheres by fine-tuning a [Gemini](https://deepmind.google/technologies/gemini/#introduction) model to automatically translate natural language problem statements into formal statements, creating a large library of formal problems of varying difficulty.

When presented with a problem, AlphaProof generates solution candidates and then proves or disproves them by searching over possible proof steps in Lean. Each proof that was found and verified is used to reinforce AlphaProof’s language model, enhancing its ability to solve subsequent, more challenging problems.

We trained AlphaProof for the IMO by proving or disproving millions of problems, covering a wide range of difficulties and mathematical topic areas over a period of weeks leading up to the competition. The training loop was also applied during the contest, reinforcing proofs of self-generated variations of the contest problems until a full solution could be found.

![Process infographic of AlphaProof’s reinforcement learning training loop: Around one million informal math problems are translated into a formal math language by a formalizer network. Then a solver network searches for proofs or disproofs of the problems, progressively training itself via the AlphaZero algorithm to solve more challenging problems](https://lh3.googleusercontent.com/-zGoVZij6MXIV2t6Pl2k1-pKPmVibDbCmhW1mkGu3jreGSirseXSrSedUWdzM_hlEihbrRA2yfdeKRvkMRqVCcFffPTZsikNwBczD6dKJXH5ISaC=w1440)

Process infographic of AlphaProof’s reinforcement learning training loop: Around one million informal math problems are translated into a formal math language by a formalizer network. Then a solver network searches for proofs or disproofs of the problems, progressively training itself via the AlphaZero algorithm to solve more challenging problems.

## A more competitive AlphaGeometry 2

AlphaGeometry 2 is a significantly improved version of [AlphaGeometry](https://deepmind.google/discover/blog/alphageometry-an-olympiad-level-ai-system-for-geometry/). It’s a neuro-symbolic hybrid system in which the language model was based on [Gemini](https://deepmind.google/technologies/gemini/#introduction) and trained from scratch on an order of magnitude more synthetic data than its predecessor. This helped the model tackle much more challenging geometry problems, including problems about movements of objects and equations of angles, ratio or distances.

AlphaGeometry 2 employs a symbolic engine that is two orders of magnitude faster than its predecessor. When presented with a new problem, a novel knowledge-sharing mechanism is used to enable advanced combinations of different search trees to tackle more complex problems.

Before this year’s competition, AlphaGeometry 2 could solve 83% of all historical IMO geometry problems from the past 25 years, compared to the 53% rate achieved by its predecessor. For IMO 2024, AlphaGeometry 2 [solved Problem 4](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/imo-2024-solutions/P4/index.html?utm_source=&utm_medium=&utm_campaign=&utm_content=) within 19 seconds after receiving its formalization.

![A geometric diagram featuring a triangle ABC inscribed in a larger circle, with various points, lines, and another smaller circle intersecting the triangle. Point A is the apex, with lines connecting it to points L and K on the larger circle, and point E inside the triangle. Points T1 and T2 lie on the lines AB and AC respectively. The smaller circle is centered at point I, the incenter of triangle ABC, and intersects the larger circle at points L and K. Points X, D, and Y lie on lines AB, BC, and AC, respectively, and a blue angle is formed at point P, below the triangle. The diagram is labeled with the letters A, B, C, D, E, I, K, L, O, P, T1, T2, X, and Y.](https://lh3.googleusercontent.com/L-zlwf9gzrCfAB9CRGtYvDTIGjCT-9t06W_SgPQXx4SKTlZVClb3UKueU5GgmJxYvZ-Nf6N-aSlvdhLMNk36WeVuYF-X9JpviMWtouNeUTq1K_sPzdM=w1440)

Illustration of Problem 4, which asks to prove the sum of ∠KIL and ∠XPY equals 180°. AlphaGeometry 2 proposed to construct E, a point on the line BI so that ∠AEB = 90°. Point E helps give purpose to the midpoint L of AB, creating many pairs of similar triangles such as ABE ~ YBI and ALE ~ IPC needed to prove the conclusion.

## New frontiers in mathematical reasoning

As part of our IMO work, we also experimented with a natural language reasoning system, built upon [Gemini](https://deepmind.google/technologies/gemini/#introduction) and our latest research to enable advanced problem-solving skills. This system doesn’t require the problems to be translated into a formal language and could be combined with other AI systems. We also tested this approach on this year’s IMO problems and the results showed great promise.

Our teams are continuing to explore multiple AI approaches for advancing mathematical reasoning and we have released more technical details on AlphaProof in a [Nature paper](https://www.nature.com/articles/s41586-025-09833-y).

We’re excited for a future in which mathematicians work with AI tools to explore hypotheses, try bold new approaches to solving long-standing problems and quickly complete time-consuming elements of proofs — and where AI systems like [Gemini](https://deepmind.google/technologies/gemini/#introduction) become more capable at math and broader reasoning.

**Acknowledgements**

We thank the International Mathematical Olympiad organization for their support.

AlphaProof development was led by Thomas Hubert, Rishi Mehta and Laurent Sartran; AlphaGeometry 2 and natural language reasoning efforts were led by Thang Luong.

AlphaProof was developed with key contributions from Hussain Masoom, Aja Huang, Miklós Z. Horváth, Tom Zahavy, Vivek Veeriah, Eric Wieser, Jessica Yung, Lei Yu, Yannick Schroecker, Julian Schrittwieser, Ottavia Bertolli, Borja Ibarz, Edward Lockhart, Edward Hughes, Mark Rowland, Grace Margand. Alex Davies and Daniel Zheng led the development of informal systems such as final answer determination, with key contributions from Iuliya Beloshapka, Ingrid von Glehn, Yin Li, Fabian Pedregosa, Ameya Velingker and Goran Žužić. Oliver Nash, Bhavik Mehta, Paul Lezeau, Salvatore Mercuri, Lawrence Wu, Calle Soenne, Thomas Murrills, Luigi Massacci and Andrew Yang advised and contributed as Lean experts. Past contributors include Amol Mandhane, Tom Eccles, Eser Aygün, Zhitao Gong, Richard Evans, Soňa Mokrá, Amin Barekatain, Wendy Shang, Hannah Openshaw, Felix Gimeno. This work was advised by David Silver and Pushmeet Kohli.

The development of AlphaGeometry 2 was led by Trieu Trinh and Yuri Chervonyi, with key contributions by Mirek Olšák, Xiaomeng Yang, Hoang Nguyen, Junehyuk Jung, Dawsen Hwang and Marcelo Menegali. The development of the natural language reasoning system was led by Golnaz Ghiasi, Garrett Bingham, YaGuang Li, with key contributions by Swaroop Mishra, Nigamaa Nayakanti, Sidharth Mudgal, Qijun Tan, Junehyuk Jung, Hoang Nguyen, Alex Zhai, Dawsen Hwang, Mingyang Deng, Clara Huiyi Hu, Jarrod Kahn, Maciej Kula, Cosmo Du. Both AlphaGeometry and natural language reasoning systems were advised by Quoc Le.

David Silver, Quoc Le, Demis Hassabis, and Pushmeet Kohli coordinated and managed the overall project.

We’d also like to thank Insuk Seo, Evan Chen, Zigmars Rasscevskis, Kari Ragnarsson, Junhwi Bae, Jeonghyun Ahn, Jimin Kim, Hung Pham, Nguyen Nguyen, Son Pham, and Pasin Manurangsi who helped evaluate the quality of our language reasoning system. Jeff Stanway, Jessica Lo, Erica Moreira, Petko Yotov and Kareem Ayoub for their support for compute provision and management. Prof Gregor Dolinar and Dr Geoff Smith MBE from the IMO Board, for the support and collaboration; and Tu Vu, Hanzhao Lin, Chenkai Kuang, Vikas Verma, Yifeng Lu, Xinyun Chen, Denny Zhou, Vihan Jain, Henryk Michalewski, Xavier Garcia, Arjun Kar, Lampros Lamprou, Kaushal Patel, Kelvin Xu, Ilya Tolstikhin, Olivier Bousquet, Anton Tsitsulin, Dustin Zelle, CJ Carey, Sam Blackwell, Abhi Rao, Vahab Mirrokni, Behnam Neyshabur, Ethan Dyer, Keith Rush, Moritz Firsching, Dan Shved, Ihar Bury, Divyanshu Ranjan, Hadi Hashemi, Alexei Bendebury, Soheil Hassas Yeganeh, Shibl Mourad, Simon Schmitt, Satinder Baveja, Chris Dyer, Jacob Austin, Wenda Li, Heng-tze Cheng, Ed Chi, Koray Kavukcuoglu, Oriol Vinyals, Jeff Dean and Sergey Brin for their support and advice.

Finally, we’d like to thank the many contributors to the Lean and Mathlib projects, without whom AlphaProof wouldn’t have been possible.

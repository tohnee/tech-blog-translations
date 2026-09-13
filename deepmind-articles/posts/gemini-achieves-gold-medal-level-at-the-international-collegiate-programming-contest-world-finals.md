---
title: "Gemini achieves gold-medal level at the International Collegiate Programming Contest World Finals"
source: https://deepmind.google/blog/gemini-achieves-gold-medal-level-at-the-international-collegiate-programming-contest-world-finals/
site: deepmind
date: 2025-09-17
authors: Hanzhao (Maggie) Lin, Heng-Tze Cheng
crawled: 2026-09-13
---

Gemini 2.5 Deep Think achieves breakthrough performance at the world’s most prestigious computer programming competition, demonstrating a profound leap in abstract problem solving.

An advanced version of [Gemini 2.5 Deep Think](https://blog.google/products/gemini/gemini-2-5-deep-think/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) has achieved gold-medal level performance at [the 2025 International Collegiate Programming Contest (ICPC) World Finals](https://worldfinals.icpc.global/).

This milestone builds directly on Gemini 2.5 Deep Think's [gold-medal win at the International Mathematical Olympiad (IMO)](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) just two months ago. Innovations from these efforts will continue to be integrated into future versions of Gemini Deep Think, expanding the frontier of advanced AI capabilities accessible to students and researchers.

Solving complex tasks at these competitions requires deep abstract reasoning, creativity, the ability to synthesize novel solutions to problems never seen before and a genuine spark of ingenuity.

Together, these breakthroughs in competitive programming and mathematical reasoning demonstrate Gemini’s profound leap in abstract problem-solving — marking a significant step on our path toward artificial general intelligence (AGI).

## ICPC sets a global standard for excellence

The ICPC is globally recognized as the oldest, largest and most prestigious algorithmic programming competition at college level. This is a step up from high school level olympiads such as the IMO. Every year, participants from nearly 3000 universities and over 103 countries compete in solving real-world coding problems.

This year’s world finals took place in Baku, Azerbaijan on September 4, and brought together the top teams from earlier phases of the competition. Over a five-hour period, each team tackled a set of complex algorithmic problems. Final rankings hinged on two unforgiving principles: only perfect solutions earned points, and every minute counted. From the 139 competing teams, [only the top four teams won gold medals](https://worldfinals.icpc.global/scoreboard/2025/finals/index.html).

## Gemini solved 10 of 12 problems, achieving gold-medal level

An advanced version of Gemini 2.5 Deep Think competed live in a remote online environment following [ICPC rules](https://icpc.global/worldfinals/rules), under the guidance of the competition organizers. It started 10 minutes after the human contestants and correctly solved 10 out of 12 problems, achieving gold-medal level performance under the same five-hour time constraint. See our solutions [here](https://github.com/google-deepmind/gemini_icpc2025).

Gemini solved eight problems within just 45 minutes and two more problems within three hours, using a wide variety of advanced data structures and algorithms to generate its solutions. By solving 10 problems in a combined total time of 677 minutes, Gemini 2.5 Deep Think would be ranked in 2nd place overall, if compared with the university teams in the competition.

Dr. Bill Poucher, ICPC Global Executive Director, stated: “The ICPC has always been about setting the highest standards in problem solving. Gemini successfully joining this arena, and achieving gold-level results, marks a key moment in defining the AI tools and academic standards needed for the next generation. Congratulations to Google DeepMind; this work will help us fuel a digital renaissance for the benefit of all.”

![A bar chart comparing Gemini's solve times (in blue) against the fastest university team (in gray) for ICPC World Finals problems A through L, highlighting that Gemini solved Problem C in 30 minutes while no university team solved it.](https://lh3.googleusercontent.com/vERQLYOhZ0OcRqtPl7xZNtlXrlOW5_4PAlIo7tsV6O_ymsWS3G6v_nhmwk8mGBkQ7ZNhsU9Qo-CeL7G-m55etR9uYopr2-b5ipjZnMjUenfkPxPdMQ=w1440)

Bar graph showing the time used to solve each of the 12 problems at the 2025 ICPC World Finals. Gemini’s time is shown in blue and the fastest university team’s time is shown in gray.

## Gemini solved a problem no university team solved

In an unprecedented moment, our model successfully and efficiently solved [Problem C](https://worldfinals.icpc.global/problems/2025/finals/problems/C-brideofpipestream.pdf) within the first half hour — which no university teams in the contest solved.

Problem C required finding a solution for distributing liquid through a network of interconnected ducts to a set of reservoirs, with the goal of finding a configuration of these ducts that fills all the reservoirs as quickly as possible. There are an infinite number of possible configurations, as each duct may be open, closed or even partially open, making it very difficult to search for the optimal configuration.

Gemini found an effective solution with a clever insight: it first assumed each reservoir has a "priority value" representing how much each reservoir should be favored compared to the others. When given a set of priority values, the best configuration of the ducts can be found using a dynamic programming algorithm. Gemini discovered that by applying the minimax theorem, the original problem can be approached by finding the priority values that make the resulting flow most constrained. Leveraging the relationship between priority values and optimal flows, Gemini used nested ternary searches to quickly find optimal priority values in the bowl-like convex solution space, and solved Problem C.

## Gemini’s performance brings together a series of advances

Our milestone performance brings together a series of advances across pretraining, post-training, novel reinforcement learning techniques, multi-step reasoning and parallel thinking. These innovations helped Gemini explore different ways of solving complex problems, verifying solutions and continuously iterating before responding.

For example, during the course of reinforcement learning, we trained Gemini to reason and generate code for some of the most difficult problems coders have faced, to learn from feedback on results and evolve its approaches. To tackle a problem, multiple Gemini agents each propose their own solutions, use terminals to execute code and tests, and then iterate the solutions based on all attempts.

Our internal studies show that a similar version of Gemini 2.5 Deep Think can also achieve gold-medal level performance in the 2023 and 2024 ICPC World Finals, performing as well as the world's top 20 competitive coders.

> Gemini successfully joining this arena, and achieving gold-level results, marks a key moment in defining the AI tools and academic standards needed for the next generation.

Dr. Bill Poucher

ICPC Global Executive Director

## Exploring Gemini's potential as a collaborator

Achieving gold-medal level at the ICPC has immediate, practical consequences for software development and shows that AI can act as a true problem-solving partner for programmers. If the best AI and human solutions in the competition were combined, all 12 problems would have been solved completely and correctly. This shows the potential for AI to provide unique, novel contributions that complement the skills and knowledge of human experts.

Beyond math and coding, our achievement demonstrates a powerful new capability in abstract reasoning. The skills needed for the ICPC — understanding a complex problem, devising a multi-step logical plan and implementing it flawlessly — are the same skills needed in many scientific and engineering fields, such as designing new drugs or microchips. It shows that AI is moving from just processing information to actually helping solve some of the world's most difficult reasoning problems in ways that could benefit humanity.

Gemini users with [Google AI Ultra subscriptions](https://one.google.com/about/google-ai-plans/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) can already use a lightweight version of Gemini 2.5 Deep Think in the [Gemini app](https://gemini.google/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=). And in the near future, much smarter AI coding assistants could help developers tackle increasingly complex engineering challenges. From logistics and debugging to scientific research, solutions to some of the hardest, most unsolvable problems may soon be within reach by using AI as a collaborative tool.

**Learn more**

[Download the Gemini app](https://gemini.google/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)[Read about Gemini 2.5 Pro](https://deepmind.google/models/gemini/pro/)[See our 2025 ICPC solutions](https://github.com/google-deepmind/gemini_icpc2025)

We thank the International Collegiate Programming Contest (ICPC) for their support.

This project was a large-scale collaboration, and its success is due to the combined efforts of many individuals and teams. Hanzhao (Maggie) Lin led the overall technical direction for Gemini competitive programming and ICPC 2025 efforts, and co-led with Heng-Tze Cheng on the overall research and execution.

The leads and key contributors of the ICPC 2025 team are the following: Chenkai Kuang, Yuan Liu, Zhaoqi Leng, Jieming Mao, Lalit Jain, Chenjie Gu, Goran Žužić, Adams Yu, YaGuang Li, Xiaomeng Yang, Yang Xiao, Adam Zhang, Alex Vitvitskyi, Ashkan Norouzi Fard, Blanca Huergo, Evan Liu, Golnaz Ghiasi, Huan Gui, John Aslanides, Jonathan Lee, Kuba Lacki, Larisa Markeeva, Luheng He, Nigamaa Nayakanti, Nikos Parotsidis, Paul Covington, Petar Veličković, Qijun Tan, Ragha Kotikalapudi, Renshen Wang, Sasan Tavakkol, Shuang Liu, Sidharth Mudgal, Steve Li, Vincent Cohen-Addad, Xianghong Luo, Xinying Song, Yiming Li and Zicheng Xu.

The advanced Gemini Deep Think for ICPC was built on foundational research jointly from the Gemini post-training, Thinking and Coding areas including: Aja Huang, Andreas Kirsch, Ankesh Anand, Archit Sharma, Betty Chan, Chenxi Liu, Cosmo Du, Dawsen Hwang, Dustin Tran, Edward Lockhart, Feryal Behbahani, Fred Zhang, Garrett Bingham, Hao Zhou, Hoang Nguyen, Irene Cai, Jian Li, Jarrod Kahn, Junehyuk Jung, Junsu Kim, Kate Baumli, Kefan Xiao, Le Hou, Lei Yu, Maciej Kula, Mahan Malihi, Marcelo Menegali, Miklós Z. Horváth, Mirek Olšák, Nate Kushman, Pei Sun, Pol Moreno, Rosemary Ke, Sahitya Potluri, Shane Gu, Shubha Raghvendra, Siamak Shakeri, Sid Lall, Steven Zheng, Thang Luong, Theophane Weber, Tong He, Tianhe (Kevin) Yu, Trieu Trinh, Vikas Yadav, Vinay Ramasesh, Vinh Tran, Weiyue Wang, Wilfried Bounsi, Xiyang Luo, Yangsibo Huang, Yi Tay, Yong Cheng, Yuan Zhang, Yuri Chervonyi and Yujing Zhang.

This effort was advised by Quoc Le and Vahab Mirrokni, with program and operation management from Kristen Chiafullo, Eric Ni, Srinivas Tadepalli, Jessica Lo and Sajjad Zafar.

We’d also like to thank our competitive programming experts for providing insights: Alexander Grushetsky, Chun-Sung Ferng, Ilya Kornakov, Liang Bai, Petr Mitrichev and Sergey Rogulenko.

We want to extend our deepest gratitude to the Gemini serving team: Abhijit Karmarkar, Cip Baetu, Emanuel Taropa, Evan Senter, Federico Lebron, Girish Ramchandra Rao, Greg Anielak, Hamish Tomlinson, Hayden Jeune, Jia Zhao, Joe Stanton, Ashish Shenoy, Jonathan Kairupan, Juliette Love, Justin Mao-Jones, Kashyap Krishnakumar, Ken Franko, Mahesh Palekar, Minh Giang, Nikhil Sethi, Rohan Jain, Rohit Varkey Thankachan, Soheil Hassas Yeganeh, Thomas Jimma and Vitor Rodrigues.

Further thanks to the following people for support, collaboration, and advice: Benoit Schillings, Ed Chi, Koray Kavukcuoglu, Jeff Dean, Oriol Vinyals, Noam Shazeer, James Manyika, Yossi Matias, Philipp Schindler, Pushmeet Kohli, Demis Hassabis, Sergey Brin, Melvin Johnson, Omer Levy, Timothy Lillicrap, Anca Dragan, Slav Petrov, Ya Xu, Madhavi Sewak, Erika Gemzer, Eugénie Rives, Erica Moreira, Tulsee Doshi, Alex Goldin, Jane Labanowski, Andy Forbes, Sean Nakamoto, Yifeng Lu, Denny Zhou, Alexander Novikov, Cristy Hayner, Hanada Tatsuki, Harsh Dhand, Ritu Ghai, Hiroki Kayama, Jenny Rizk Nicholls, Jo Chick, Song Zuo, Pratyusha Mukherjee, Shibo Wang, Carlos Guia, Xiaofan Zhang, …

Finally, we thank Dr. Bill Poucher from the ICPC global for the support and endorsement.

The ICPC global has confirmed that our submitted solutions are complete and accepted. It is important to note that their review does not extend to validating our system, processes, or underlying model.

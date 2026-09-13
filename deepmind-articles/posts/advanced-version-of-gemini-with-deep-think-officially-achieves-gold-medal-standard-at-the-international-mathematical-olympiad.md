---
title: "Advanced version of Gemini with Deep Think officially achieves gold-medal standard at the International Mathematical Olympiad"
source: https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/
site: deepmind
date: 2025-07-21
authors: Thang Luong, Edward Lockhart
crawled: 2026-09-13
---

The International Mathematical Olympiad (“IMO”) is the world’s most prestigious competition for young mathematicians, and has been held annually since 1959. Each country taking part is represented by six elite, pre-university mathematicians who compete to solve six exceptionally difficult problems in algebra, combinatorics, geometry, and number theory. Medals are awarded to the top half of contestants, with approximately 8% receiving a prestigious gold medal.

Recently, the IMO has also become an aspirational challenge for AI systems as a test of their advanced mathematical problem-solving and reasoning capabilities. Last year, Google DeepMind’s combined AlphaProof and AlphaGeometry 2 systems [achieved the silver-medal standard](https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=), solving four out of the six problems and scoring 28 points. Making use of specialist formal languages, this breakthrough demonstrated that AI was beginning to approach elite human mathematical reasoning.

This year, we were amongst an inaugural cohort to have our model results officially graded and certified by IMO coordinators using the same criteria as for student solutions. Recognizing the significant accomplishments of this year’s student-participants, we’re now excited to share the news of Gemini’s breakthrough performance.

## Breakthrough Performance at IMO 2025 with Gemini Deep Think

An advanced version of Gemini [Deep Think](https://blog.google/technology/google-deepmind/google-gemini-updates-io-2025/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=#deep-think) solved five out of the six IMO problems perfectly, earning 35 total points, and achieving gold-medal level performance. The solutions can be found online [here](https://storage.googleapis.com/deepmind-media/gemini/IMO_2025.pdf?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=).

> We can confirm that Google DeepMind has reached the much-desired milestone, earning 35 out of a possible 42 points — a gold medal score. Their solutions were astonishing in many respects. IMO graders found them to be clear, precise and most of them easy to follow.

IMO President Prof. Dr. Gregor Dolinar

This achievement is a significant advance over last year’s breakthrough result. At IMO 2024, AlphaGeometry and AlphaProof required experts to first translate problems from natural language into domain-specific languages, such as Lean, and vice-versa for the proofs. It also took two to three days of computation. This year, our advanced Gemini model operated end-to-end in natural language, producing rigorous mathematical proofs directly from the official problem descriptions – all within the 4.5-hour competition time limit.

![A diagram showing the progression of Google DeepMind's mathematical AI systems: a box on the left for "IMO 2024" features "Formal mathematics" using "AlphaProof & AlphaGeometry," with a blue arrow pointing to a box on the right for "IMO 2025" featuring "Informal mathematics" using "Advanced Gemini with Deep Think" represented by a blue four-pointed star.](https://lh3.googleusercontent.com/-iKXOVjrAdBjkxjgGNECAk9O0y8aHyyJWC02MZ2GuCtV_C_OrBNLZ5EVenO5HwhBzpljpRuhE1Ea8h75ajpBBHbSO0n0AWCum0x1apWw_Qw4EbotDdI=w1440)

## Making the most of Deep Think mode

We achieved this year’s result using an advanced version of Gemini Deep Think – an enhanced reasoning mode for complex problems that incorporates some of our latest research techniques, including parallel thinking. This setup enables the model to simultaneously explore and combine multiple possible solutions before giving a final answer, rather than pursuing a single, linear chain of thought.

To make the most of the reasoning capabilities of Deep Think, we additionally trained this version of Gemini on novel reinforcement learning techniques that can leverage more multi-step reasoning, problem-solving and theorem-proving data. We also provided Gemini with access to a curated corpus of high-quality solutions to mathematics problems, and added some general hints and tips on how to approach IMO problems to its instructions.

We will be making a version of this Deep Think model available to a set of trusted testers, including mathematicians, before rolling it out to Google AI Ultra subscribers.

## The Future of AI and Mathematics

Google DeepMind has ongoing collaborations with the mathematical community, but we are still only [at the start](https://www.youtube.com/watch?v=TgS0nFeYul8&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) of AI’s potential to contribute to mathematics. By teaching our systems to reason more flexibly and intuitively, we are getting closer to building AI that can solve more complex and advanced mathematics.

While our approach this year was based purely on natural language with Gemini, we also continue making progress on our formal systems, AlphaGeometry and AlphaProof. We believe agents that combine natural language fluency with rigorous reasoning - including verified reasoning in formal languages - will become invaluable tools for mathematicians, scientists, engineers, and researchers, helping us advance human knowledge on the path to AGI.

[Explore IMO-Bench highlights](https://imobench.github.io/)[Read more about the IMO-Bench paper](https://arxiv.org/abs/2511.01846)[Access the IMO-Bench datasets](https://github.com/google-deepmind/superhuman/tree/main/imobench)

**Acknowledgements**

We thank the International Mathematical Olympiad organization for their support.

This project was a large-scale collaboration, and its success is due to the combined efforts of many individuals and teams. Thang Luong led the overall technical direction for IMO 2025 effort and co-led with Edward Lockhart on the overall coordination.

The leads and key contributors of the IMO 2025 team are the following; Dawsen Hwang, Junehyuk Jung, Jonathan Lee, Nate Kushman, Pol Moreno, Yi Tay, Lei Yu, Golnaz Ghiasi, Garrett Bingham, Lalit Jain, Vincent Cohen-Addad and Theophane Weber, Ankesh Anand, Steven Zheng, Vinh Tran, Vinay Ramasesh, Andreas Kirsch, Jieming Mao, Zicheng Xu, Wilfried Bounsi, Vahab Mirrokni, Hoang Nguyen, Fred Zhang, Mahan Malihi, Yangsibo Huang, Yuri Chervonyi, Trieu Trinh, Junsu Kim, Mirek Olšák, Marcelo Menegali, Xiaomeng Yang, Richard Song, Miklós Z. Horváth, Aja Huang, Goran Žužić.

The advanced Gemini model with Deep Think for IMO was built on foundational research from the Deep Think team with sponsorship of the GDM Thinking area, and corresponding post-training efforts including; Archit Sharma, Shubha Raghvendra, Tong He, Pei Sun, Tianhe (Kevin) Yu, Eric Ni, Siamak Shakeri, Hanzhao (Maggie) Lin, Cosmo Du, Sid Lall, Le Hou, Yuan Zhang, Yujing Zhang, Yong Cheng, Luheng He, and Chenxi Liu.

This effort was advised by Quoc Le and Pushmeet Kohli, with program management from Kristen Chiafullo and Alex Goldin.

We’d also like to thank our experts for providing data and evaluations: Insuk Seo (lead), Jiwon Kang, Donghyun Kim, Junsu Kim, Jimin Kim, Seongbin Jeon, Yoonho Na, Seunghwan Lee, Jihoo Lee, Younghun Jo, Yongsuk Hur, Seongjae Park, Kyuhyeon Choi, Minkyu Choi, Su-Hyeok Moon, Seojin Kim, Yueun Lee, Taehun Kim, Jeeho Ryu, Seungwoo Lee, Dain Kim, Sanha Lee, Hyunwoo Choi, Aiden Jung, Youngbeom Jin, Jeonghyun Ahn, Junhwi Bae, Gyumin Kim, Nam Dung Tran, Quoc Ba Can Vo, Van Huyen Nguyen, Tuan Anh Nguyen, Thanh Dat Vo, Nguyen Nam Hung Tran, Van Khai Luong, Son Vu, Son Tra Dao, Dai Dinh Phong Tran, Thanh Dat Le, Cheng-Chiang Tsai, Kari Ragnarsson, Kiat Chuan Tan, Yahya Tabesh, Hamed Mahdavi, Azin Nazari, Chu-Lan Kao, Steven Creech, Tony Feng, Daogao Liu, and Ciprian Manolescu.

Further thanks to the following people for support, collaboration, and advice; Omer Levy, Timothy Lillicrap, Jack Rae, Yifeng Lu, Heng-tze Cheng, Denny Zhou, Ed Chi, Vahab Mirrokni, Tulsee Doshi, Madhavi Sewak, Melvin Johnson, Fernando Pereira, Benoit Schillings, Koray Kavukcuoglu, Oriol Vinyals, Jeff Dean, Demis Hassabis, Sergey Brin, Jessica Lo, Sajjad Zafar, Tom Simpson, Jane Labanowski, Andy Forbes, Sean Nakamoto, Jonathan Lai, Fabian Pedregosa, Samuel Albanie, Alex Zhai, Sara Javanmardi, Divy Thakkar, YaGuang Li, Nigamaa Nayakanti, Chenjie Gu, Chenkai Kuang, Swaroop Mishra, Filipe Miguel de Almeida, Silvio Lattanzi, Ashkan Norouzi Fard, Tal Schuster, Ziwei Ji, Honglu Fan, Xuezhi Wang, Aditi Mavalankar, Tom Schaul, Rosemary Ke, Xiangzhuo Ding, Adam Brown, Emanuel Taropa, Charlie Chen, Joe Stanton, Cip Baetu, Alvin Abdagic, Federico Lebron, Ioana Mihailescu, Soheil Hassas Yeganeh, Ashish Shenoy, and Minh Giang

Finally, we thank Prof Gregor Dolinar from the IMO Board for the support and endorsement.

The IMO have confirmed that our submitted answers are complete and correct solutions. It is important to note that their review does not extend to validating our system, processes, or underlying model (see [more](https://imo2025.au/wp-content/uploads/2025/07/IMO-2025_ClosingDayStatement-19072025.pdf)).

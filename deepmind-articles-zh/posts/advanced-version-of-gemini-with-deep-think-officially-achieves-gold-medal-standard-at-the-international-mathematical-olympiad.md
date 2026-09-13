---
title: "搭载 Deep Think 的 Gemini 进阶版本正式达到国际数学奥林匹克竞赛金牌水准"
title_en: "Advanced version of Gemini with Deep Think officially achieves gold-medal standard at the International Mathematical Olympiad"
source: https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/
site: deepmind
date: 2025-07-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 搭载 Deep Think 的 Gemini 进阶版本正式达到国际数学奥林匹克竞赛金牌水准

> 原文：[Advanced version of Gemini with Deep Think officially achieves gold-medal standard at the International Mathematical Olympiad](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) · Google DeepMind

国际数学奥林匹克竞赛（IMO）是全球最具声望的青年数学家赛事，自 1959 年起每年举办。每个参赛国家由六名精英大学前数学选手代表，角逐解答代数、组合、几何与数论六个极难题目。奖牌颁发给排名前一半的选手，其中约 8% 能获得宝贵的金牌。

近来，IMO 也成为了 AI 系统的进阶挑战目标，用以检验其高级数学问题求解与推理能力。去年，Google DeepMind 的 AlphaProof 与 AlphaGeometry 2 组合系统[达到了银牌水准](https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)，解出六道题中的四道，得 28 分。这一突破借助了专门的形式化语言，表明 AI 开始接近人类精英水平的数学推理。

今年，我们成为首批由 IMO 协调员按照与学生解答相同的标准，对模型结果进行正式评分与认证的团队之一。在祝贺今年学生参赛者取得出色成绩的同时，我们如今很高兴地分享 Gemini 突破性表现的新闻。

## Gemini Deep Think 在 IMO 2025 的突破性表现

Gemini [Deep Think](https://blog.google/technology/google-deepmind/google-gemini-updates-io-2025/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=#deep-think) 的一个进阶版本完美解出了六道 IMO 试题中的五道，总分 35 分，达到金牌水准的表现。解答可在[这里](https://storage.googleapis.com/deepmind-media/gemini/IMO_2025.pdf?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)在线查阅。

> 我们可以确认，Google DeepMind 达成了众人期盼的里程碑，在满分 42 分中获得 35 分——这是一个金牌分数。他们的解答在许多方面都令人惊叹。IMO 评分员认为这些解答清晰、精确，且大多数易于跟随。

IMO 主席 Gregor Dolinar 教授

这一成就较去年的突破性结果有了重大进展。在 IMO 2024 上，AlphaGeometry 和 AlphaProof 需要专家先把题目从自然语言翻译成 Lean 等领域专用语言，证明结果还需再翻译回来；计算也耗时两到三天。今年，我们的 Gemini 进阶模型以自然语言端到端运行，直接从官方题目描述出发生成严格的数学证明——全部在 4.5 小时的比赛时限之内完成。

![一张示意图，展示 Google DeepMind 数学 AI 系统的演进：左侧的方框标注「IMO 2024」，展示使用「AlphaProof & AlphaGeometry」的「Formal mathematics（形式化数学）」；一支蓝色箭头指向右侧标注「IMO 2025」的方框，展示使用「Advanced Gemini with Deep Think」的「Informal mathematics（非形式化数学）」，以一个蓝色四角星表示。](https://lh3.googleusercontent.com/-iKXOVjrAdBjkxjgGNECAk9O0y8aHyyJWC02MZ2GuCtV_C_OrBNLZ5EVenO5HwhBzpljpRuhE1Ea8h75ajpBBHbSO0n0AWCum0x1apWw_Qw4EbotDdI=w1440)

## 充分发挥 Deep Think 模式

我们今年的成绩是使用 Gemini Deep Think 的进阶版本取得的——这是面向复杂问题的增强推理模式，融入了我们部分最新的研究技术，包括并行思考（parallel thinking）。这一设置使模型能够同时探索并组合多个可能的解，然后才给出最终答案，而不是沿着单一的线性思维链推进。

为了充分发挥 Deep Think 的推理能力，我们还用新颖的强化学习技术额外训练了这一版 Gemini，以利用更多的多步推理、问题求解和定理证明数据。我们向 Gemini 提供了一个经过整理的高质量数学问题解答语料库，并在其指令中加入了一些关于如何应对 IMO 问题的通用提示与技巧。

我们将先向包括数学家在内的一组可信测试者开放这一 Deep Think 模型版本，之后再向 Google AI Ultra 订阅用户推送。

## AI 与数学的未来

Google DeepMind 与数学界有着持续的合作，但在 AI 为数学做出贡献的潜力方面，我们仍仅处于[起点](https://www.youtube.com/watch?v=TgS0nFeYul8&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)。通过教会我们的系统更灵活、更直观地进行推理，我们正逐步接近能够求解更复杂、更高深数学的 AI。

虽然我们今年的方法完全基于与 Gemini 的自然语言，我们也在持续推进 AlphaGeometry 和 AlphaProof 等形式化系统的进展。我们相信，兼具自然语言流畅性与严格推理——包括形式语言中经过验证的推理——的智能体，将成为数学家、科学家、工程师和研究人员的无价工具，帮助我们在通往 AGI 的道路上推进人类知识。

[探索 IMO-Bench 亮点](https://imobench.github.io/)[进一步了解 IMO-Bench 论文](https://arxiv.org/abs/2511.01846)[获取 IMO-Bench 数据集](https://github.com/google-deepmind/superhuman/tree/main/imobench)

**致谢**

我们感谢国际数学奥林匹克竞赛组织方的支持。

本项目是一次大规模协作，其成功归功于众多个人与团队的共同努力。Thang Luong 领导了 IMO 2025 工作的总体技术方向，并与 Edward Lockhart 共同负责整体协调。

IMO 2025 团队的负责人与核心贡献者如下：Dawsen Hwang、Junehyuk Jung、Jonathan Lee、Nate Kushman、Pol Moreno、Yi Tay、Lei Yu、Golnaz Ghiasi、Garrett Bingham、Lalit Jain、Vincent Cohen-Addad、Theophane Weber、Ankesh Anand、Steven Zheng、Vinh Tran、Vinay Ramasesh、Andreas Kirsch、Jieming Mao、Zicheng Xu、Wilfried Bounsi、Vahab Mirrokni、Hoang Nguyen、Fred Zhang、Mahan Malihi、Yangsibo Huang、Yuri Chervonyi、Trieu Trinh、Junsu Kim、Mirek Olšák、Marcelo Menegali、Xiaomeng Yang、Richard Song、Miklós Z. Horváth、Aja Huang、Goran Žužić。

面向 IMO 的搭载 Deep Think 的 Gemini 进阶模型，建立在 Deep Think 团队的基础研究之上，由 GDM Thinking 领域提供支持，相应后训练工作包括：Archit Sharma、Shubha Raghvendra、Tong He、Pei Sun、Tianhe (Kevin) Yu、Eric Ni、Siamak Shakeri、Hanzhao (Maggie) Lin、Cosmo Du、Sid Lall、Le Hou、Yuan Zhang、Yujing Zhang、Yong Cheng、Luheng He 和 Chenxi Liu。

这项工作由 Quoc Le 和 Pushmeet Kohli 担任顾问，Kristen Chiafullo 和 Alex Goldin 负责项目管理。

我们还要感谢提供数据与评测的专家们：Insuk Seo（负责人）、Jiwon Kang、Donghyun Kim、Junsu Kim、Jimin Kim、Seongbin Jeon、Yoonho Na、Seunghwan Lee、Jihoo Lee、Younghun Jo、Yongsuk Hur、Seongjae Park、Kyuhyeon Choi、Minkyu Choi、Su-Hyeok Moon、Seojin Kim、Yueun Lee、Taehun Kim、Jeeho Ryu、Seungwoo Lee、Dain Kim、Sanha Lee、Hyunwoo Choi、Aiden Jung、Youngbeom Jin、Jeonghyun Ahn、Junhwi Bae、Gyumin Kim、Nam Dung Tran、Quoc Ba Can Vo、Van Huyen Nguyen、Tuan Anh Nguyen、Thanh Dat Vo、Nguyen Nam Hung Tran、Van Khai Luong、Son Vu、Son Tra Dao、Dai Dinh Phong Tran、Thanh Dat Le、Cheng-Chiang Tsai、Kari Ragnarsson、Kiat Chuan Tan、Yahya Tabesh、Hamed Mahdavi、Azin Nazari、Chu-Lan Kao、Steven Creech、Tony Feng、Daogao Liu 和 Ciprian Manolescu。

此外还要感谢以下人士提供的支持、协作与建议：Omer Levy、Timothy Lillicrap、Jack Rae、Yifeng Lu、Heng-tze Cheng、Denny Zhou、Ed Chi、Vahab Mirrokni、Tulsee Doshi、Madhavi Sewak、Melvin Johnson、Fernando Pereira、Benoit Schillings、Koray Kavukcuoglu、Oriol Vinyals、Jeff Dean、Demis Hassabis、Sergey Brin、Jessica Lo、Sajjad Zafar、Tom Simpson、Jane Labanowski、Andy Forbes、Sean Nakamoto、Jonathan Lai、Fabian Pedregosa、Samuel Albanie、Alex Zhai、Sara Javanmardi、Divy Thakkar、YaGuang Li、Nigamaa Nayakanti、Chenjie Gu、Chenkai Kuang、Swaroop Mishra、Filipe Miguel de Almeida、Silvio Lattanzi、Ashkan Norouzi Fard、Tal Schuster、Ziwei Ji、Honglu Fan、Xuezhi Wang、Aditi Mavalankar、Tom Schaul、Rosemary Ke、Xiangzhuo Ding、Adam Brown、Emanuel Taropa、Charlie Chen、Joe Stanton、Cip Baetu、Alvin Abdagic、Federico Lebron、Ioana Mihailescu、Soheil Hassas Yeganeh、Ashish Shenoy 和 Minh Giang。

最后，我们感谢 IMO 理事会的 Gregor Dolinar 教授给予的支持与认可。

IMO 已确认我们提交的答案是完整且正确的解答。需要说明的是，他们的评审并不包括对我们系统、流程或底层模型的验证（详见[更多信息](https://imo2025.au/wp-content/uploads/2025/07/IMO-2025_ClosingDayStatement-19072025.pdf)）。

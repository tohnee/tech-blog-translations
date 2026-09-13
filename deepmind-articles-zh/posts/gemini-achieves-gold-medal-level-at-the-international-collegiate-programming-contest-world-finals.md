---
title: "Gemini 在国际大学生程序设计竞赛全球总决赛上达到金牌水平"
title_en: "Gemini achieves gold-medal level at the International Collegiate Programming Contest World Finals"
source: https://deepmind.google/blog/gemini-achieves-gold-medal-level-at-the-international-collegiate-programming-contest-world-finals/
site: deepmind
date: 2025-09-17
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 在国际大学生程序设计竞赛全球总决赛上达到金牌水平

> 原文：[Gemini achieves gold-medal level at the International Collegiate Programming Contest World Finals](https://deepmind.google/blog/gemini-achieves-gold-medal-level-at-the-international-collegiate-programming-contest-world-finals/) · Google DeepMind

Gemini 2.5 Deep Think 在全球最负盛名的计算机编程竞赛中取得突破性成绩，展示了在抽象问题求解上的深刻跃迁。

[Gemini 2.5 Deep Think](https://blog.google/products/gemini/gemini-2-5-deep-think/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=) 的一个先进版本在 [2025 年国际大学生程序设计竞赛（ICPC）全球总决赛](https://worldfinals.icpc.global/)上达到了金牌水平。

这一里程碑直接建立在 Gemini 2.5 Deep Think 两个月前[在国际数学奥林匹克竞赛（IMO）中摘得金牌](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)的基础之上。这些努力中的创新成果将继续融入未来版本的 Gemini Deep Think，扩展学生和研究者可用的先进 AI 能力边界。

在这些竞赛中求解复杂任务，需要深度的抽象推理、创造力、为前所未见的问题综合出全新解法的能力，以及真正的聪明才智之光。

竞技编程与数学推理上的这些突破合在一起，展示了 Gemini 在抽象问题求解上的深刻跃迁——标志着我们迈向通用人工智能（AGI）道路上的重要一步。

## ICPC 树立全球卓越标准

ICPC 被全球公认为历史最悠久、规模最大、最负盛名的大学生算法编程竞赛。它比 IMO 这类高中阶段奥林匹克竞赛高出一个层级。每年，来自近 3000 所大学、103 个以上国家的参赛者同场竞技，求解真实世界的编程问题。

今年的全球总决赛于 9 月 4 日在阿塞拜疆巴库举行，汇聚了此前各阶段比赛中的顶尖队伍。在五个小时内，每支队伍都要攻克一组复杂的算法问题。最终排名取决于两条毫不留情的原则：只有完全正确的解才能得分，而且每一分钟都算数。在 139 支参赛队伍中，[只有前四名队伍获得金牌](https://worldfinals.icpc.global/scoreboard/2025/finals/index.html)。

## Gemini 解出 12 道题中的 10 道，达到金牌水平

Gemini 2.5 Deep Think 的一个先进版本在竞赛组织者的指导下，遵循 [ICPC 规则](https://icpc.global/worldfinals/rules)，在远程在线环境中实时参赛。它比人类选手晚 10 分钟开始，在同样的五小时时限内正确解出 12 道题中的 10 道，达到金牌水平。我们的解法见[这里](https://github.com/google-deepmind/gemini_icpc2025)。

Gemini 在短短 45 分钟内解出 8 道题，又在 3 小时内再解出 2 道，期间运用了多种多样的高级数据结构与算法来生成解法。以总计 677 分钟解出 10 道题的成绩，若与参赛的大学生队伍相比，Gemini 2.5 Deep Think 将排在总榜第 2 位。

ICPC 全球执行总监 Bill Poucher 博士表示：「ICPC 一贯以最高标准要求问题求解。Gemini 成功进入这一赛场并取得金牌成绩，是定义下一代所需 AI 工具与学术标准的关键时刻。祝贺 Google DeepMind；这项工作将帮助我们推动一场惠及所有人的数字复兴。」

![一张柱状图，对比 Gemini（蓝色）与最快大学生队（灰色）在 ICPC 全球总决赛 A 至 L 各题上的解题用时，突出显示 Gemini 在 30 分钟内解出了 C 题，而没有任何大学生队解出该题。](https://lh3.googleusercontent.com/vERQLYOhZ0OcRqtPl7xZNtlXrlOW5_4PAlIo7tsV6O_ymsWS3G6v_nhmwk8mGBkQ7ZNhsU9Qo-CeL7G-m55etR9uYopr2-b5ipjZnMjUenfkPxPdMQ=w1440)

柱状图展示 2025 年 ICPC 全球总决赛 12 道题各自的解题用时。Gemini 的用时以蓝色显示，最快大学生队的用时以灰色显示。

## Gemini 解出了一道没有任何大学生队伍解出的题

在一个前所未有的时刻，我们的模型在开赛后半小时内成功且高效地解出了 [C 题](https://worldfinals.icpc.global/problems/2025/finals/problems/C-brideofpipestream.pdf)——本届赛事没有任何大学生队伍解出此题。

C 题要求找到把液体通过相互连接的管道网络分配到一组储液罐的方案，目标是找到一组管道配置，使所有储液罐尽快被充满。可能的配置有无限多种，因为每根管道都可以是打开、关闭甚至部分打开的，这使得寻找最优配置极其困难。

Gemini 凭借一个巧妙的洞见找到了有效解法：它首先假设每个储液罐都有一个「优先级值」，表示相对于其他储液罐应如何偏待它。给定一组优先级值后，可以用动态规划算法找到管道的最优配置。Gemini 发现，通过应用极小极大定理（minimax theorem），原问题可以转化为寻找使所得流最受限的那组优先级值。利用优先级值与最优流之间的关系，Gemini 使用嵌套三元搜索在这个碗状凸解空间中快速找到最优优先级值，解出了 C 题。

## Gemini 的表现汇聚了一系列进展

我们的里程碑成绩汇聚了预训练、后训练、新型强化学习技术、多步推理与并行思考等方面的一系列进展。这些创新帮助 Gemini 探索解决复杂问题的不同路径、验证解法，并在作答前持续迭代。

例如，在强化学习过程中，我们训练 Gemini 对程序员所面对过的一些最难的问题进行推理并生成代码，从结果的反馈中学习并改进其方法。处理一道题时，多个 Gemini 智能体各自提出自己的解法，使用终端执行代码与测试，然后基于所有尝试对解法进行迭代。

我们的内部研究表明，一个类似的 Gemini 2.5 Deep Think 版本也能在 2023 年和 2024 年 ICPC 全球总决赛上达到金牌水平，与全球排名前 20 的竞技程序员表现相当。

> Gemini 成功进入这一赛场并取得金牌成绩，是定义下一代所需 AI 工具与学术标准的关键时刻。

Bill Poucher 博士

ICPC 全球执行总监

## 探索 Gemini 作为协作者的潜力

在 ICPC 达到金牌水平对软件开发具有直接的实际意义，并表明 AI 可以成为程序员真正的问题求解伙伴。如果把本次竞赛中最佳的 AI 解法与人类解法合在一起，全部 12 道题都能被完整、正确地解出。这展示了 AI 提供独特、新颖贡献、与人类专家的技能和知识互补的潜力。

在数学和编程之外，我们的成绩展示了一项强大的新抽象推理能力。ICPC 所需的技能——理解复杂问题、设计多步骤的逻辑方案并完美实现它——正是许多科学与工程领域所需的技能，例如设计新药物或微芯片。这表明 AI 正在从单纯处理信息，转向真正帮助解决世界上一些最困难的推理问题，并以可能造福人类的方式做到这一点。

拥有 [Google AI Ultra 订阅](https://one.google.com/about/google-ai-plans/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)的 Gemini 用户已经可以在 [Gemini 应用](https://gemini.google/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)中使用 Gemini 2.5 Deep Think 的轻量版本。而在不久的将来，更聪明的 AI 编程助手可以帮助开发者应对日益复杂的工程挑战。从物流和调试到科学研究，借助 AI 作为协作工具，一些最难、最无解的问题的答案可能很快触手可及。

**了解更多**

[下载 Gemini 应用](https://gemini.google/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)[了解 Gemini 2.5 Pro](https://deepmind.google/models/gemini/pro/)[查看我们的 2025 ICPC 解法](https://github.com/google-deepmind/gemini_icpc2025)

我们感谢国际大学生程序设计竞赛（ICPC）的支持。

本项目是一次大规模协作，其成功有赖于许多个人和团队的共同努力。Hanzhao (Maggie) Lin 领导了 Gemini 竞技编程与 ICPC 2025 工作的整体技术方向，并与 Heng-Tze Cheng 共同领导整体研究与执行。

ICPC 2025 团队的负责人与关键贡献者如下：Chenkai Kuang、Yuan Liu、Zhaoqi Leng、Jieming Mao、Lalit Jain、Chenjie Gu、Goran Žužić、Adams Yu、YaGuang Li、Xiaomeng Yang、Yang Xiao、Adam Zhang、Alex Vitvitskyi、Ashkan Norouzi Fard、Blanca Huergo、Evan Liu、Golnaz Ghiasi、Huan Gui、John Aslanides、Jonathan Lee、Kuba Lacki、Larisa Markeeva、Luheng He、Nigamaa Nayakanti、Nikos Parotsidis、Paul Covington、Petar Veličković、Qijun Tan、Ragha Kotikalapudi、Renshen Wang、Sasan Tavakkol、Shuang Liu、Sidharth Mudgal、Steve Li、Vincent Cohen-Addad、Xianghong Luo、Xinying Song、Yiming Li 和 Zicheng Xu。

ICPC 专用的高级 Gemini Deep Think 构建在 Gemini 后训练、思考与编程领域的基础研究之上，这些研究者包括：Aja Huang、Andreas Kirsch、Ankesh Anand、Archit Sharma、Betty Chan、Chenxi Liu、Cosmo Du、Dawsen Hwang、Dustin Tran、Edward Lockhart、Feryal Behbahani、Fred Zhang、Garrett Bingham、Hao Zhou、Hoang Nguyen、Irene Cai、Jian Li、Jarrod Kahn、Junehyuk Jung、Junsu Kim、Kate Baumli、Kefan Xiao、Le Hou、Lei Yu、Maciej Kula、Mahan Malihi、Marcelo Menegali、Miklós Z. Horváth、Mirek Olšák、Nate Kushman、Pei Sun、Pol Moreno、Rosemary Ke、Sahitya Potluri、Shane Gu、Shubha Raghvendra、Siamak Shakeri、Sid Lall、Steven Zheng、Thang Luong、Theophane Weber、Tong He、Tianhe (Kevin) Yu、Trieu Trinh、Vikas Yadav、Vinay Ramasesh、Vinh Tran、Weiyue Wang、Wilfried Bounsi、Xiyang Luo、Yangsibo Huang、Yi Tay、Yong Cheng、Yuan Zhang、Yuri Chervonyi 和 Yujing Zhang。

这项工作由 Quoc Le 和 Vahab Mirrokni 担任顾问，项目与运营管理来自 Kristen Chiafullo、Eric Ni、Srinivas Tadepalli、Jessica Lo 和 Sajjad Zafar。

我们还要感谢为这项工作提供洞见的竞技编程专家：Alexander Grushetsky、Chun-Sung Ferng、Ilya Kornakov、Liang Bai、Petr Mitrichev 和 Sergey Rogulenko。

我们要向 Gemini 服务团队致以最深的谢意：Abhijit Karmarkar、Cip Baetu、Emanuel Taropa、Evan Senter、Federico Lebron、Girish Ramchandra Rao、Greg Anielak、Hamish Tomlinson、Hayden Jeune、Jia Zhao、Joe Stanton、Ashish Shenoy、Jonathan Kairupan、Juliette Love、Justin Mao-Jones、Kashyap Krishnakumar、Ken Franko、Mahesh Palekar、Minh Giang、Nikhil Sethi、Rohan Jain、Rohit Varkey Thankachan、Soheil Hassas Yeganeh、Thomas Jimma 和 Vitor Rodrigues。

进一步感谢以下人士的支持、协作与建议：Benoit Schillings、Ed Chi、Koray Kavukcuoglu、Jeff Dean（杰夫·迪恩）、Oriol Vinyals、Noam Shazeer、James Manyika、Yossi Matias、Philipp Schindler、Pushmeet Kohli、Demis Hassabis（德米斯·哈萨比斯）、Sergey Brin、Melvin Johnson、Omer Levy、Timothy Lillicrap、Anca Dragan、Slav Petrov、Ya Xu、Madhavi Sewak、Erika Gemzer、Eugénie Rives、Erica Moreira、Tulsee Doshi、Alex Goldin、Jane Labanowski、Andy Forbes、Sean Nakamoto、Yifeng Lu、Denny Zhou、Alexander Novikov、Cristy Hayner、Hanada Tatsuki、Harsh Dhand、Ritu Ghai、Hiroki Kayama、Jenny Rizk Nicholls、Jo Chick、Song Zuo、Pratyusha Mukherjee、Shibo Wang、Carlos Guia、Xiaofan Zhang 等。

最后，我们感谢 ICPC 全球组织的 Bill Poucher 博士的支持与认可。

ICPC 全球组织已确认我们提交的解法完整且被接受。需要说明的是，他们的审查并不涵盖对我们系统、流程或底层模型的验证。

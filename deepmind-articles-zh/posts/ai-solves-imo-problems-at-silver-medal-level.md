---
title: "AI 解出国际数学奥林匹克竞赛题目，达到银牌水准"
title_en: "AI achieves silver-medal standard solving International Mathematical Olympiad problems"
source: https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/
site: deepmind
date: 2024-07-25
crawled: 2026-09-13
translated: 2026-09-13
---

# AI 解出国际数学奥林匹克竞赛题目，达到银牌水准

> 原文：[AI achieves silver-medal standard solving International Mathematical Olympiad problems](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/) · Google DeepMind

突破性模型 AlphaProof 和 AlphaGeometry 2 解出数学领域的高级推理问题

*注：本博客最初发布于 2024 年 7 月 25 日。2025 年 11 月 12 日，我们在《自然》（Nature）的[一篇文章](https://www.nature.com/articles/s41586-025-09833-y)中发表了 AlphaProof 背后的方法论。*

拥有高级数学推理能力的通用人工智能（AGI）有望开启科学技术的新前沿。

我们在构建帮助数学家发现[新洞见](https://deepmind.google/discover/blog/exploring-the-beauty-of-pure-mathematics-in-novel-ways/)、[新算法](https://deepmind.google/discover/blog/discovering-novel-algorithms-with-alphatensor/)以及[开放问题](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)答案的 AI 系统方面已经取得了长足进步。但由于推理能力和训练数据的局限，当前的 AI 系统在求解一般数学问题上仍然吃力。

今天，我们推出 AlphaProof——一个基于强化学习的形式化数学推理新系统，以及 AlphaGeometry 2——我们[几何求解系统](https://deepmind.google/discover/blog/alphageometry-an-olympiad-level-ai-system-for-geometry/)的改进版本。这两个系统共同解出了今年[国际数学奥林匹克竞赛](https://www.imo2024.uk/)（IMO）六道题中的四道，首次达到了与该竞赛银牌得主相当的水平。

## 求解复杂数学问题的 AI 突破性表现

IMO 是面向青年数学家的历史最悠久、规模最大、声望最高的赛事，自 1959 年起每年举办。

每年，顶尖的大学前数学选手都要训练——有时长达数千小时——去求解代数、组合、几何和数论中的六个极难题目。数学家最高荣誉之一的[菲尔兹奖](https://www.mathunion.org/imu-awards/fields-medal)的许多得主，都曾代表自己的国家参加 IMO。

近来，一年一度的 IMO 竞赛也被广泛视为机器学习领域的一项重大挑战，以及衡量 AI 系统高级数学推理能力的标杆。

今年，我们把组合 AI 系统应用于 IMO 组委会提供的竞赛题目。我们的解答由著名数学家按 IMO 的得分规则评分：他们是 IMO 金牌得主、菲尔兹奖得主 [Timothy Gowers 爵士教授](https://www.dpmms.cam.ac.uk/~wtg10/)，以及两届 IMO 金牌得主、IMO 2024 选题委员会主席 [Joseph Myers 博士](https://www.polyomino.org.uk/)。

> 这个程序能想出这样一个非显而易见的构造，令人印象非常深刻，远超我所认为的最先进水平。

Timothy Gowers 爵士教授

IMO 金牌得主、菲尔兹奖得主

首先，题目被人工翻译成形式化数学语言，供我们的系统理解。在正式比赛中，学生分两场各 4.5 小时提交答案。我们的系统在几分钟内解出了其中一题，其余题目最多花了三天。

AlphaProof 通过确定答案并证明其正确性，解出了两道代数题和一道数论题，其中包括今年 IMO 中只有五名参赛者解出的最难题目。AlphaGeometry 2 证明了那道几何题，而两道组合题仍未被解出。

[查看我们系统的 IMO 2024 解答](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/imo-2024-solutions/index.html)

六道题每题可得 7 分，满分 42 分。我们的系统最终得分为 28 分，每一道解出的题都拿到了满分——相当于[银牌区间](https://www.imo-official.org/year_info.aspx?year=2024)的上限。今年，金牌线从 29 分起步，在正式竞赛中由 [609 名参赛者中的 58 人](https://www.imo-official.org/year_individual_r.aspx?year=2024)达到。

![彩色图表，展示我们的 AI 系统相对于在 IMO 2024 中获得铜牌、银牌和金牌的人类参赛者的表现。我们的系统在总分 42 分中获得 28 分，达到与竞赛银牌得主相当的水平，并接近从 29 分起步的金牌线。](https://lh3.googleusercontent.com/iSMHpqQhw2pxSwyQiqpDGchZpJpOatzY0at6ok3Br8SvKYUun75o59u1ad32zgjOTcu9g5ZKAgZc0rDBcJXAU4tE6cph7dRf5svD4SEXV4aa827gyr0=w1440)

图表展示我们的 AI 系统相对于 IMO 2024 人类参赛者的表现。我们在总分 42 分中获得 28 分，达到与竞赛银牌得主相当的水平。

## AlphaProof：一种形式化的推理方法

AlphaProof 是一个自我训练、用形式语言 [Lean](https://lean-lang.org/) 证明数学命题的系统。它将一个预训练语言模型与 [AlphaZero](https://deepmind.google/discover/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/) 强化学习算法相结合——后者此前曾自学掌握了国际象棋、将棋和围棋。

形式语言提供了一项关键优势：涉及数学推理的证明可以被形式化地验证正确性。不过，由于人类书写的形式化数据量极为有限，形式语言在机器学习中的运用此前一直受到制约。

相比之下，基于自然语言的方法尽管可以访问多得多的数据（高出数个数量级），却可能幻觉出貌似合理但错误的中间推理步骤和解。我们通过微调一个 [Gemini](https://deepmind.google/technologies/gemini/#introduction) 模型自动把自然语言题面翻译成形式化命题，在两个互补的世界之间架起了一座桥梁，建立了一个涵盖不同难度的大型形式化问题库。

当面对一个问题时，AlphaProof 生成候选解，然后通过在 Lean 中搜索可能的证明步骤来证明或反驳它们。每一个被发现并验证的证明都会被用来强化 AlphaProof 的语言模型，增强其求解后续更困难问题的能力。

我们通过证明或反驳数百万道题目来为 IMO 训练 AlphaProof，这些题目覆盖广泛的难度和数学主题领域，训练持续到比赛前的数周。这一训练循环也在竞赛期间持续运行，强化针对竞赛题目的自生成变体的证明，直到找到完整解答。

![AlphaProof 强化学习训练循环的流程信息图：约一百万道非形式化数学题由一个形式化网络（formalizer network）翻译为形式化数学语言。随后一个求解器网络（solver network）搜索这些问题的证明或反驳，通过 AlphaZero 算法逐步训练自己以求解更具挑战性的问题。](https://lh3.googleusercontent.com/-zGoVZij6MXIV2t6Pl2k1-pKPmVibDbCmhW1mkGu3jreGSirseXSrSedUWdzM_hlEihbrRA2yfdeKRvkMRqVCcFffPTZsikNwBczD6dKJXH5ISaC=w1440)

AlphaProof 强化学习训练循环的流程信息图：约一百万道非形式化数学题由一个形式化网络翻译为形式化数学语言。随后一个求解器网络搜索这些问题的证明或反驳，通过 AlphaZero 算法逐步训练自己以求解更具挑战性的问题。

## 更具竞争力的 AlphaGeometry 2

AlphaGeometry 2 是 [AlphaGeometry](https://deepmind.google/discover/blog/alphageometry-an-olympiad-level-ai-system-for-geometry/) 的大幅改进版本。它是一个神经-符号混合系统，其中的语言模型基于 [Gemini](https://deepmind.google/technologies/gemini/#introduction)，并从头开始在前辈模型多出一个数量级的合成数据上训练。这帮助模型应对更具挑战性的几何问题，包括涉及物体运动以及角度、比例或距离方程的问题。

AlphaGeometry 2 采用的符号引擎比其前代快两个数量级。面对新问题时，一种新颖的知识共享机制被用来支持不同搜索树的高级组合，以应对更复杂的问题。

在今年比赛之前，AlphaGeometry 2 能解出过去 25 年全部历史 IMO 几何题中的 83%，而其前代的解出率为 53%。对于 IMO 2024，AlphaGeometry 2 在收到第 4 题的形式化表述后 19 秒内[将其解出](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/imo-2024-solutions/P4/index.html?utm_source=&utm_medium=&utm_campaign=&utm_content=)。

![一幅几何图形：三角形 ABC 内接于一个大圆，图中有多个点、线段以及另一个与大圆相交的小圆。点 A 是顶点，有连线将它与大圆上的点 L 和 K 相连，三角形内部还有点 E。点 T1 和 T2 分别位于线段 AB 和 AC 上。小圆以三角形 ABC 的内心点 I 为圆心，与大圆相交于点 L 和 K。点 X、D、Y 分别位于线段 AB、BC、AC 上，三角形下方点 P 处形成一个蓝色角。图中标注了字母 A、B、C、D、E、I、K、L、O、P、T1、T2、X 和 Y。](https://lh3.googleusercontent.com/L-zlwf9gzrCfAB9CRGtYvDTIGjCT-9t06W_SgPQXx4SKTlZVClb3UKueU5GgmJxYvZ-Nf6N-aSlvdhLMNk36WeVuYF-X9JpviMWtouNeUTq1K_sPzdM=w1440)

第 4 题示意图：要求证明 ∠KIL 与 ∠XPY 之和等于 180°。AlphaGeometry 2 提出构造点 E——线段 BI 上使 ∠AEB = 90° 的一点。点 E 让 AB 的中点 L 发挥了作用，创造出许多对相似三角形，如证明结论所需的 ABE ~ YBI 和 ALE ~ IPC。

## 数学推理的新前沿

作为 IMO 工作的一部分，我们还试验了一个自然语言推理系统，它建立在 [Gemini](https://deepmind.google/technologies/gemini/#introduction) 与我们最新研究之上，具备高级问题求解能力。该系统不需要把题目翻译成形式语言，并且可以与其他 AI 系统结合。我们也在今年的 IMO 题目上测试了这一方法，结果显示出巨大前景。

我们的团队正在继续探索推进数学推理的多种 AI 方法，我们已在[一篇《自然》论文](https://www.nature.com/articles/s41586-025-09833-y)中发布了关于 AlphaProof 的更多技术细节。

我们期待这样一个未来：数学家与 AI 工具携手探索假说、大胆尝试解决长期悬而未决问题的新方法、快速完成证明中耗时的部分——而像 [Gemini](https://deepmind.google/technologies/gemini/#introduction) 这样的 AI 系统也在数学与更广泛的推理上变得更强。

**致谢**

我们感谢国际数学奥林匹克竞赛组织方的支持。

AlphaProof 的开发由 Thomas Hubert、Rishi Mehta 和 Laurent Sartran 领导；AlphaGeometry 2 与自然语言推理工作由 Thang Luong 领导。

AlphaProof 的开发有赖于以下关键贡献者：Hussain Masoom、Aja Huang、Miklós Z. Horváth、Tom Zahavy、Vivek Veeriah、Eric Wieser、Jessica Yung、Lei Yu、Yannick Schroecker、Julian Schrittwieser、Ottavia Bertolli、Borja Ibarz、Edward Lockhart、Edward Hughes、Mark Rowland、Grace Margand。Alex Davies 和 Daniel Zheng 领导了最终答案判定等非形式化系统的开发，关键贡献者包括 Iuliya Beloshapka、Ingrid von Glehn、Yin Li、Fabian Pedregosa、Ameya Velingker 和 Goran Žužić。Oliver Nash、Bhavik Mehta、Paul Lezeau、Salvatore Mercuri、Lawrence Wu、Calle Soenne、Thomas Murrills、Luigi Massacci 和 Andrew Yang 作为 Lean 专家提供建议并做出贡献。过往贡献者包括 Amol Mandhane、Tom Eccles、Eser Aygün、Zhitao Gong、Richard Evans、Soňa Mokrá、Amin Barekatain、Wendy Shang、Hannah Openshaw、Felix Gimeno。这项工作由 David Silver 和 Pushmeet Kohli 担任顾问。

AlphaGeometry 2 的开发由 Trieu Trinh 和 Yuri Chervonyi 领导，关键贡献者包括 Mirek Olšák、Xiaomeng Yang、Hoang Nguyen、Junehyuk Jung、Dawsen Hwang 和 Marcelo Menegali。自然语言推理系统的开发由 Golnaz Ghiasi、Garrett Bingham、YaGuang Li 领导，关键贡献者包括 Swaroop Mishra、Nigamaa Nayakanti、Sidharth Mudgal、Qijun Tan、Junehyuk Jung、Hoang Nguyen、Alex Zhai、Dawsen Hwang、Mingyang Deng、Clara Huiyi Hu、Jarrod Kahn、Maciej Kula、Cosmo Du。AlphaGeometry 与自然语言推理系统均由 Quoc Le 担任顾问。

David Silver、Quoc Le、Demis Hassabis（德米斯·哈萨比斯）和 Pushmeet Kohli 协调并管理了整个项目。

我们还要感谢帮助评估我们语言推理系统质量的 Insuk Seo、Evan Chen、Zigmars Rasscevskis、Kari Ragnarsson、Junhwi Bae、Jeonghyun Ahn、Jimin Kim、Hung Pham、Nguyen Nguyen、Son Pham 和 Pasin Manurangsi；感谢为算力供应与管理提供支持的 Jeff Stanway、Jessica Lo、Erica Moreira、Petko Yotov 和 Kareem Ayoub；感谢 IMO 理事会的 Gregor Dolinar 教授和 Geoff Smith MBE 博士的支持与协作；并感谢 Tu Vu、Hanzhao Lin、Chenkai Kuang、Vikas Verma、Yifeng Lu、Xinyun Chen、Denny Zhou、Vihan Jain、Henryk Michalewski、Xavier Garcia、Arjun Kar、Lampros Lamprou、Kaushal Patel、Kelvin Xu、Ilya Tolstikhin、Olivier Bousquet、Anton Tsitsulin、Dustin Zelle、CJ Carey、Sam Blackwell、Abhi Rao、Vahab Mirrokni、Behnam Neyshabur、Ethan Dyer、Keith Rush、Moritz Firsching、Dan Shved、Ihar Bury、Divyanshu Ranjan、Hadi Hashemi、Alexei Bendebury、Soheil Hassas Yeganeh、Shibl Mourad、Simon Schmitt、Satinder Baveja、Chris Dyer、Jacob Austin、Wenda Li、Heng-tze Cheng、Ed Chi、Koray Kavukcuoglu、Oriol Vinyals、Jeff Dean 和 Sergey Brin 的支持与建议。

最后，我们感谢 Lean 和 Mathlib 项目的众多贡献者——没有他们，AlphaProof 不可能诞生。

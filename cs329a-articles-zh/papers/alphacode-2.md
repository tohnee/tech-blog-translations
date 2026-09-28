---
title: "AlphaCode 2 技术报告"
title_en: "AlphaCode 2 Technical Report"
source: https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf
crawled: 2026-09-23
translated: 2026-09-23
---

# AlphaCode 2 技术报告

> 原文：[AlphaCode 2 Technical Report](https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf) · DeepMind 技术报告（CS329A 指定阅读）

2023-12-06
AlphaCode 2 技术报告
AlphaCode Team, Google DeepMind

AlphaCode（Li et al., 2022）是首个在竞赛编程中达到中位参赛者水平的 AI 系统——这是一项涉及高等数学、逻辑与计算机科学的困难推理任务。本文介绍 AlphaCode 2——一个由 Gemini（Gemini Team, Google, 2023）驱动、性能大幅提升的新增强系统。AlphaCode 2 依赖强大语言模型与定制搜索及重排序机制的组合。在与原版 AlphaCode 相同的平台上评估，我们发现 AlphaCode 2 解出的问题数是原来的 1.7 倍，并优于 85% 的比赛参赛者。

通讯作者：remileblond@google.com
© 2023 Google DeepMind. 版权所有

## 引言

竞赛编程是编程能力的终极试金石之一。参与者在有限时间内编写代码，解决需要批判性思维、逻辑以及对算法、编程与自然语言理解的复杂问题。因此，它是高级推理与问题求解能力的绝佳基准。

AlphaCode（Li et al., 2022）是首个在该任务上达到竞争水平的 AI 系统。其继任者 AlphaCode 2 利用多个基于 Gemini（Gemini Team, Google, 2023）的模型，构成一个大幅改进的系统。在竞赛编程的主要平台 Codeforces 上评估时，AlphaCode 2 在 10 次尝试内解出 43% 的问题，接近原版 AlphaCode（25%）的两倍。其前身处于中位参赛者水平，而我们估计 AlphaCode 2 平均达到第 85 百分位。

采用 Gemini 作为 AlphaCode 2 全部组件的基础模型，是达到这一性能水平的关键。AlphaCode 2 的成功凸显了 Gemini 的灵活性与适应性：我们得以对它进行微调，并在代码生成与代码重排序等多个不同任务上优化性能。

## 系统总览

AlphaCode 2 依赖强大的大语言模型，结合为竞赛编程量身定制的高级搜索与重排序机制。如图 1 所示，其主要组件包括：

- 一族为每道问题生成代码样本的策略模型；
- 一种鼓励生成高度多样代码样本、以搜索可能程序空间的采样机制；
- 一种移除不符合题目描述的代码样本的过滤机制；
- 一种对语义相似的代码样本分组的聚类算法，使我们能避免冗余；
- 一个评分模型，用于从 10 个最大的代码样本簇中各自选出最佳候选。

AlphaCode 2 Technical Report

Problem
Submit!
C++
C++
C++C++C++C++
C++C++C++C++C++C++
C++
C++C++
Codeforces
AlphaCode 2
models
Massive
sampling
Execution
& filtering
Clustering Reranking
# In this
# problem
...
C++C++C++C++C++C++C++C++ C++C++C++C++C++C++
Scoring model
Intermediate
AlphaCode 2
models
AlphaCode 2
models
Gemini Pro
Fine-Tuning
Sampling & Evaluation
Problem
Solution
CodeContests
v2
Problem
Solution
Higher quality
dataset
Scoring model

图 1|AlphaCode 2 系统的高层概览。

## 策略与微调

我们的起点是 Gemini Pro 模型（Gemini Team, Google, 2023），并在其上以 GOLD（Pang and He, 2020）为训练目标连续进行两轮微调。首先，我们在更新版 CodeContests 数据集（包含更多问题、更多解法，以及验证集上更高质量的人工整理测试）上微调。该数据集约含 1.5 万道问题与 3000 万个人类代码样本。我们通过变化超参数生成多个微调模型，最终得到一族微调模型。其次，我们在另一个更高质量的数据集上再做少量额外微调步骤。依靠一族而非单一策略，使我们能最大化多样性——这仍是攻克难题的关键。

## 采样

我们的采样方法与 AlphaCode 相近。每道问题最多生成一百万个代码样本，对每个样本使用随机化的温度参数以鼓励多样性。我们还随机化提示中包含的目标元数据，例如题目难度评分及其类别标签。

我们把采样预算均匀分给微调模型族。虽然 AlphaCode 同时用 Python 与 C++ 采样，AlphaCode 2 只使用 C++ 样本，因为我们发现其质量更高。

大规模采样使我们能彻底搜索模型分布并生成大量多样的代码样本，最大化至少生成若干正确样本的可能性。鉴于样本数量庞大，过滤与重排序对整个系统的性能至关重要，因为我们每道问题最多只提交 10 个代码样本。

## 过滤

每道竞赛编程问题至少包含一个公开的输入/输出测试，指示代码样本应如何表现。我们在相应的测试输入上执行每个代码样本，过滤掉所有不产生预期输出（因而不可能正确）的样本，以及不到 5% 无法编译的样本。平均而言，该过滤移除约 95% 的样本。

## 聚类

过滤后，每道问题平均留下 5 万个候选，而我们只限于 10 次提交。为进一步削减候选，我们基于样本的运行时行为进行聚合：与 AlphaCode 一样，我们训练一个单独的模型为每道问题生成新的测试输入，然后在这些新输入上执行剩余样本。产生的输出构成一个签名，我们用它把相似的代码样本分组为簇。随后按簇的大小排序，只保留最大的 10 个。

聚类的意义在于避免冗余：由于同一簇中的代码样本行为相似，我们可以每簇只向在线评判提交一个样本，以获得最佳结果。

## 评分模型

我们微调了第二个 Gemini Pro 模型，为代码样本赋予 0 到 1 之间的估计正确性分数。使用该评分模型，我们为剩余各簇中的每个代码样本计算分数；然后基于该预测分数从每个簇中选出最佳候选样本，构成我们最终的 10 个提交列表。

## 评估

我们在 Codeforces 上评估 AlphaCode 2——与原版 AlphaCode 相同的平台。我们选择了 12 场近期、每场超过 8000 名参赛者的比赛，来自 division 2 或更难的「1+2」组别。共计 77 道问题。对每道问题，我们采样一百万个候选，并按上述流程选择并排序、最多提交 10 个解法，直到找到正确解或候选用尽。

我们发现 AlphaCode 2 解出了 43% 的比赛问题，较此前创造纪录的 AlphaCode 系统（解出 25%）接近 2 倍的改进。映射到比赛排名，我们估计 AlphaCode 2 平均处于第 85 百分位——即优于 85% 的参赛者，在 Codeforces 上恰好位于「Expert」与「Candidate Master」类别之间。这相对只超过约 46% 参赛者的 AlphaCode 是显著进步。在它表现最好的两场比赛中，AlphaCode 2 超过了 99.5% 以上的比赛参与者！

AlphaCode 2 Technical Report

0% 20% 40% 60% 80% 100%　87%　46%
Percentile of contestants below score
0%
25%
50%
75%
100%　Average normalized score
AlphaCode 2
AlphaCode (estimated)
Human contestants

图 2|AlphaCode 2 的估计排名。我们把人类参赛者的 Codeforces 分数（除以每场比赛最佳人类分数、归一化到 [0, 1]）对其排名作图，并在我们评估的 12 场比赛上取平均。然后计算 AlphaCode 2 的平均归一化分数并标注在排名轴上，使其稳居第 85 百分位之上。该排名计入模拟的时间罚分，假设 AlphaCode 2 按难度递增的顺序处理问题，并在 2 小时整完成最后一道问题的采样。

我们评估了增加每题样本数量的影响。与 AlphaCode 的情况一样，我们发现性能随样本数大致对数线性增长。AlphaCode 2 只需约 100 个样本即可达到 AlphaCode 用一百万个样本的性能水平，使其样本效率提升超过 10000 倍。

## 讨论与结论

竞赛编程与其他编码任务非常不同：后者通常遵循命令式范式——用户给出明确指令，模型输出所需代码。相比之下，竞赛编程问题是开放式的。要解决它们，在编写代码实现之前，需要理解、分析并推理问题，这涉及高等数学与计算机科学概念。

这解释了为什么通用 AI 系统在该基准上表现不佳。AlphaCode 2 在竞赛编程比赛中的成功，代表了这一极难推理任务上的显著跃升。

采用 Gemini Pro 作为基础模型，使系统两个关键组件的性能显著提升：生成代码样本的策略模型，以及用于从中选出最佳的评分模型。我们能把 Gemini 微调到在这两个截然不同的任务上都高性能，足见其惊人的灵活性。我们推测改用编码与推理能力更强的 Gemini Ultra 作为基础模型，将使整体 AlphaCode 2 方法进一步提升。

尽管 AlphaCode 2 成果可观，在出现能可靠达到最佳人类程序员水平的系统之前，还有很多工作要做。我们的系统需要大量试错，且大规模运行仍然过于昂贵。此外，它严重依赖能否过滤掉明显糟糕的代码样本。

AlphaCode 2 Technical Report

100 101 102 103 104 105 106
Sampling budget per problem
0%
20%
40%　Solve rate　AlphaCode 2
AlphaCode (1M samples)

图 3|12 场近期比赛上的解题率随每题样本数的变化。

这为系统与人类程序员之间的积极互动打开了大门：人类可以指定额外的过滤属性；在这种 AlphaCode 2 + 人类的设定下，我们的得分超过第 90 百分位！我们希望这种交互式编程将成为编程的未来——程序员把能力强大的 AI 模型当作协作工具，帮助其对问题进行推理、提出代码设计并协助实现。我们正致力于把 AlphaCode 2 的独特能力带入我们的 Gemini 基础模型，作为让这一新编程范式惠及所有人的第一步。

## 参考文献

Gemini Team, Google. Gemini: A Family of Highly Capable Multimodal Models. 2023. URL
https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf.
Leblond et al. AlphaCode 2 Technical Report. 2023. URLhttps://storage.googleapis.com/
deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf.
Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling, F. Gimeno,
A. D. Lago, T. Hubert, P. Choy, C. de Masson d'Autume, I. Babuschkin, X. Chen, P.-S. Huang,
J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S. Robson, P. Kohli, N. de Freitas,
K. Kavukcuoglu, and O. Vinyals. Competition-level code generation with alphacode.Science, 2022.
URL https://www.science.org/doi/abs/10.1126/science.abq1158.
R. Y. Pang and H. He. Text generation by learning from demonstrations. arXiv preprint
arXiv:2009.07839, 2020. URLhttps://arxiv.org/pdf/2009.07839.pdf.

## 引用本工作

这是 Google DeepMind 提供的开放获取论文。本工作的最终版本已在线发表。引用格式：
Leblond et al. AlphaCode 2 Technical Report. 2023. URLhttps://storage.googleapis.com/
deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf.

## 贡献与致谢

**负责人**

Felix Gimeno，技术负责人
Florent Altché，技术负责人
Rémi Leblond，负责人

**核心贡献者**

Alaa Saade
Anton Ruddock
Corentin Tallec
George Powell
Jean-Bastien Grill
Maciej Mikuła
Matthias Lochbrunner
Michael Mathieu
Paul Caron

**贡献者**

Disha Shrivastava
Eric Mitchell

**贡献者**

Grace Margand
Jacob Kelly
Jakub Sygnowski
James Keeling
Junyoung Chung
Nate Kushman
Nikolay Savinov
Petko Yotov
Tobenna Peter Igwe
Wojciech Stokowiec
Yujia Li

**战略顾问**

Koray Kavukcuoglu
Nando de Freitas
Oriol Vinyals
Pushmeet Kohli
Satinder Baveja

AlphaCode 2 Technical Report

每种角色内的作者按字母顺序排列；排序不代表贡献程度。

我们衷心感谢 Google DeepMind 同事的支持，尤其是 Gemini 团队、原 AlphaCode 团队与硬件团队，没有他们就不可能有 AlphaCode 2。

我们感谢 Eleanor Tomlisen 与 Gaby Pearl 提供的精美 AlphaCode 2 系统概览图。

我们感谢我们的领导、审阅者与同事在本报告上的宝贵讨论与反馈——Aakanksha Chowdhery、Aliya Ahmad、Antonia Paterson、Arielle Bier、Ben Bariach、Dawn Bloxwich、Demis Hassabis、Eli Collins、Emily Hossellman、Fred Alcober、Jeff Dean、Joel Moss、Jon Small、Koray Kavukcuoglu、Lily Lin、Megha Goel、Oriol Vinyals、Petar Veličković、Rebecca Bland、Sanah Choudhry 与 Tessa Lueth。

AlphaCode 2 演示中使用的问题——展示于 Gemini 主网页——经 Codeforces 许可使用。Codeforces 是一个定期举办比赛的平台，世界各地的参与者前来检验自己的编程技能。该问题来自 CodeTON Round 4 比赛。

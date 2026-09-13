---
title: "AlphaGeometry：达到奥林匹克竞赛水平的几何 AI 系统"
title_en: "AlphaGeometry: An Olympiad-level AI system for geometry"
source: https://deepmind.google/blog/alphageometry-an-olympiad-level-ai-system-for-geometry/
site: deepmind
date: 2024-01-17
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaGeometry：达到奥林匹克竞赛水平的几何 AI 系统

> 原文：[AlphaGeometry: An Olympiad-level AI system for geometry](https://deepmind.google/blog/alphageometry-an-olympiad-level-ai-system-for-geometry/) · Google DeepMind

我们的 AI 系统超越了最先进的几何问题解法，推进了 AI 在数学中的推理能力

呼应古希腊的奥林匹克精神，[国际数学奥林匹克竞赛](https://www.imo-official.org/)（IMO）是当今世界上最聪明的高中数学家的竞技场。这项赛事不仅展示青年才俊，还已成为先进 AI 系统在数学与推理方面的试验场。

在今天发表于《Nature》的[论文](https://www.nature.com/articles/s41586-023-06747-5)中，我们介绍 AlphaGeometry——一个以接近人类奥林匹克金牌得主水平求解复杂几何问题的 AI 系统，这是 AI 性能上的一项突破。在一项包含 30 道奥林匹克几何问题的基准测试中，AlphaGeometry 在标准奥林匹克时限内解出 25 道。作为对比，此前最先进的系统解出了其中 10 道几何问题，而人类金牌得主的平均解题数为 25.9 道。

![一幅标题为「接近奥林匹克金牌得主水准」的柱状图，显示在 30 道几何问题中解出的数量。此前最先进系统解出 10 道，铜牌得主解出 19.3 道，银牌得主解出 22.9 道，AlphaGeometry 解出 25 道，金牌得主解出 25.9 道。](https://lh3.googleusercontent.com/fl7Tr2po9Y9Cc_qcKPxMZ69-4xgvqCMBX8PO-EzZgudxJZT8Tl44FnYC0yVFOmI1fJ4gO01I-K-WlhKDfetfWzDbTM0M9dfn8PAccdaaExhox1I0=w1440)

在我们由 2000 年至 2022 年奥林匹克竞赛题目汇编而成的 30 道奥林匹克几何问题基准集（IMO-AG-30）中，AlphaGeometry 在竞赛时限内解出 25 道。这已接近人类金牌得主在同一组问题上的平均得分。此前被称为「吴方法」（Wu's method）的最先进方法解出了 10 道。

由于缺乏推理技能和训练数据，AI 系统在几何和数学的复杂问题上常常举步维艰。AlphaGeometry 系统将神经语言模型的预测能力与受规则约束的演绎引擎相结合，二者协同工作以找到解答。通过开发一种可生成海量合成训练数据的方法——1 亿个独特样例——我们无需任何人类示范即可训练 AlphaGeometry，绕开了数据瓶颈。

借助 AlphaGeometry，我们展示了 AI 日益增强的逻辑推理、发现和验证新知识的能力。求解奥林匹克竞赛水平的几何问题，是在迈向更先进、更通用的 AI 系统的道路上发展深度数学推理的重要里程碑。我们正在开源 [AlphaGeometry 的代码与模型](https://github.com/google-deepmind/alphageometry)，希望它与合成数据生成和训练方面的其他工具与方法一道，为数学、科学和 AI 领域开辟新的可能。

> 现在我完全理解了，AI 研究者为何首先尝试 IMO 几何问题，因为为这些问题寻找解答在某种程度上有点像国际象棋：在每一步我们可供选择的合理走法数量都相当有限。但他们真的能把它做成，仍然令我惊叹。这是一项了不起的成就。

Ngô Bảo Châu

菲尔兹奖得主、IMO 金牌得主

## AlphaGeometry 采用神经符号方法

AlphaGeometry 是一个神经符号系统，由一个神经语言模型和一个符号演绎引擎组成，二者协同为复杂几何定理寻找证明。正如「[思考，快与慢](https://kahneman.scholar.princeton.edu/publications)」的理念：一个系统提供快速的、「直觉式」的想法，另一个则进行更审慎、理性的决策。

语言模型擅长识别数据中的普遍模式与关系，因此能快速预测可能有用的构造，但往往缺乏严格推理或解释自身决策的能力。符号演绎引擎则基于形式逻辑，使用清晰的规则得出结论。它们理性且可解释，但可能「缓慢」而缺乏灵活性——尤其是独自处理大型复杂问题时。

AlphaGeometry 的语言模型引导其符号演绎引擎朝着几何问题的可能解前进。奥林匹克几何问题基于图形，在求解之前需要添加新的几何构造，例如点、线或圆。AlphaGeometry 的语言模型从无穷多的可能性中预测添加哪些新构造最有用。这些线索帮助填补空白，让符号引擎能够对图形做进一步的演绎推理，逼近解答。

![一幅示意图，说明 AlphaGeometry 如何结合语言模型与符号引擎求解几何问题。流程从「一个简单问题」（证明等腰三角形 ABC 的底角相等）进入「AlphaGeometry」。在 AlphaGeometry 中，语言模型预测有用的添加（「添加一个构造」），引导「符号引擎」证明定理。最终的「解答」面板显示构造出的中点 D 与线段 AD，以及逐步的逻辑证明。](https://lh3.googleusercontent.com/nihKc4w8ggrUy7JMo24eF1Hdt_bnHuCIhI_zqubWxY98QWmcV7qYc8iZHPD6VNM6nsvCWjOYqIKSkqNeo0gPvcaCJZc9jcoZvItr9v8Yd6kGOfEPkZo=w1440)

AlphaGeometry 求解一个简单问题：给定问题图形及其定理前提（左），AlphaGeometry（中）首先使用其符号引擎对图形演绎出新命题，直到找到解答或新命题穷尽。如果没有找到解答，AlphaGeometry 的语言模型会添加一个可能有用的新构造（蓝色），为符号引擎开辟新的演绎路径。这一循环持续进行，直到找到解答（右）。在本例中，只需要一个构造。

![一幅示意图，展示 AlphaGeometry 求解 2015 年国际数学奥林匹克竞赛（IMO）第 3 题。左侧显示问题的几何图形与文字描述。标注「AlphaGeometry」的箭头指向右侧面板，其中展示了逐步的符号证明，以及一幅包含系统为求解定理而添加的三个蓝色构造点（D、G 和 E）及其相应辅助线的最终图形。](https://lh3.googleusercontent.com/Bw1hvpT952TdCWTEgFfLn8qkXXGItR-UonHR9CFl9CNm84rF-5f76or9tSKtRIvcoMROhi6TljgqL1ay9mP3wzWeQp6UMN37A7YlaVzMrcpsfZch8g=w1440)

AlphaGeometry 求解一道奥林匹克问题：2015 年国际数学奥林匹克竞赛第 3 题（左）以及 AlphaGeometry 解答的精简版本（右）。蓝色元素为添加的构造。AlphaGeometry 的解答共含 109 个逻辑步骤。

[查看完整解答](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphageometry-an-olympiad-level-ai-system-for-geometry%20/AlphaGeometry%20solution.pdf)

## 生成 1 亿条合成数据样例

几何学依赖于对空间、距离、形状和相对位置的理解，是艺术、建筑、工程和许多其他领域的基础。人类可以用纸笔学习几何：审视图形，并运用已有知识去发现新的、更精妙的几何性质与关系。我们的合成数据生成方法大规模地模拟了这一知识构建过程，使我们能够从零开始训练 AlphaGeometry，无需任何人类示范。

利用高度并行化的计算，该系统首先生成了 10 亿个随机几何图形，并穷举推导出每个图形中点与线之间的所有关系。AlphaGeometry 找出每个图形中蕴含的全部证明，然后回溯推究需要哪些额外的构造（如果需要的话）才能得到这些证明。我们将这一过程称为「符号演绎与回溯」。

![八幅在纯白背景上由相交黑色线条、三角形和蓝色圆圈构成的复杂随机生成几何图形示例。](https://lh3.googleusercontent.com/yqGiQa3-G5FSQoBJRbW16SugZnCAyN7StfMp-7kwnaIHHPifHW4XyEjFYw0J5PaMhNgzY5CTY0kmNk0Dpy7sD0tZxXSldkRcPFsoezowHbeu2kocEA=w1440)

AlphaGeometry 所生成合成数据的可视化表示

这一庞大的数据池经过过滤以剔除相似样例，最终形成了包含 1 亿个不同难度独特样例的训练数据集，其中 900 万个含有添加构造。有了这么多关于这些构造如何导向证明的样例，AlphaGeometry 的语言模型在面对奥林匹克几何问题时能够就新构造提出很好的建议。

### 用 AI 开创数学推理

AlphaGeometry 给出的每道奥林匹克问题解答都经过了计算机的检查与验证。我们还将其结果与以往的 AI 方法以及人类在奥林匹克竞赛中的表现进行了比较。此外，数学教练、前奥林匹克金牌得主 Evan Chen 为我们评估了 AlphaGeometry 的一批解答。

Chen 表示：「AlphaGeometry 的输出令人印象深刻，因为它既可验证又干净利落。过去 AI 对证明类竞赛题的解答时好时坏（输出有时才正确，且需要人工检查）。AlphaGeometry 没有这个弱点：它的解答具有机器可验证的结构。尽管如此，它的输出仍然是人类可读的。人们可以想象一个通过暴力坐标系求解几何问题的计算机程序：想想连篇累牍的枯燥代数计算。AlphaGeometry 不是那样。它像学生一样使用包含角度和相似三角形的经典几何法则。」

> AlphaGeometry 的输出令人印象深刻，因为它既可验证又干净利落……它像学生一样使用包含角度和相似三角形的经典几何法则。

Evan Chen

数学教练、奥林匹克金牌得主

由于每届奥林匹克竞赛共有六道题，其中通常只有两道聚焦几何，AlphaGeometry 在一届竞赛中只能应用于三分之一的问题。尽管如此，仅凭其几何能力，它就已成为世界上第一个能够达到 2000 年和 2015 年 IMO 铜牌门槛的 AI 模型。

在几何领域，我们的系统已接近 IMO 金牌得主的水平，但我们的目光落在更大的目标上：为下一代 AI 系统推进推理能力。鉴于用大规模合成数据从零训练 AI 系统的更广泛潜力，这一方法或将塑造未来 AI 系统在数学及其他领域发现新知识的方式。

AlphaGeometry 建立在 Google DeepMind 与 Google Research 用 AI 开创数学推理的工作之上——从[探索纯数学之美](https://deepmind.google/blog/exploring-the-beauty-of-pure-mathematics-in-novel-ways/)，到[用语言模型求解数学与科学问题](https://blog.research.google/2022/06/minerva-solving-quantitative-reasoning.html?utm_source=&utm_medium=&utm_campaign=&utm_content=)。而最近，我们推出了 [FunSearch](https://deepmind.google/blog/active-offline-policy-selection/)，它利用大语言模型首次在数学科学的开放问题上取得了发现。

我们的长期目标依然是构建能够跨数学领域泛化的 AI 系统，发展通用 AI 系统所依赖的复杂问题求解与推理能力，同时不断拓展人类知识的边界。

进一步了解 AlphaGeometry

[阅读我们发表在 Nature 上的论文](https://www.nature.com/articles/s41586-023-06747-5)[访问 AlphaGeometry 的 GitHub](https://github.com/google-deepmind/alphageometry)

**致谢**

本项目是 Google DeepMind 团队与纽约大学计算机科学系之间的合作。本工作的作者包括 Trieu Trinh、Yuhuai Wu、Quoc Le、He He 和 Thang Luong。我们感谢 Rif A. Saurous、Denny Zhou、Christian Szegedy、Delesley Hutchins、Thomas Kipf、Hieu Pham、Petar Veličković、Edward Lockhart、Debidatta Dwibedi、Kyunghyun Cho、Lerrel Pinto、Alfredo Canziani、Thomas Wies、He He 的研究组、Evan Chen、Mirek Olsak、Patrik Bak 的帮助与支持。我们还要感谢 Google DeepMind 管理层的支持，尤其是 Ed Chi、Koray Kavukcuoglu、Pushmeet Kohli 和 Demis Hassabis。

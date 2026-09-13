---
title: "从噪声数据中学习可解释规则"
title_en: "Learning explanatory rules from noisy data"
source: https://deepmind.google/blog/learning-explanatory-rules-from-noisy-data/
site: deepmind
date: 2018-01-29
crawled: 2026-09-13
translated: 2026-09-13
---

# 从噪声数据中学习可解释规则

> 原文：[Learning explanatory rules from noisy data](https://deepmind.google/blog/learning-explanatory-rules-from-noisy-data/) · Google DeepMind

假设你在踢足球。球来到你脚下，你决定把球传给无人盯防的前锋。这个看似简单的动作，其实需要两种不同的思维。

首先，你识别出脚下有一个足球。这种识别需要直觉式的感知思维——你很难说清楚自己是怎么知道脚下有球的，你就是「看见」它在那里。其次，你决定把球传给某位前锋。这一决定需要概念性思维。你的决定伴随着一个理由——你把球传给这位前锋，是因为她无人盯防。

我们之所以对这一区分感兴趣，是因为这两种思维恰好对应机器学习的两条不同路径：深度学习与[符号程序合成](http://www.inductive-programming.org/intro.html)。深度学习专注于直觉式的感知思维，而符号程序合成则聚焦于概念性的、基于规则的思维。两者各有优劣——深度学习系统对噪声数据鲁棒，但难以解释且需要大量数据训练；符号系统更容易解释、所需训练数据更少，却难以应对噪声数据。人类认知可以[无缝结合](https://davidbarber.github.io/blog/2017/11/07/Learning-From-Scratch-by-Thinking-Fast-and-Slow-with-Deep-Learning-and-Tree-Search/)这两种截然不同的思维方式，但能否在单一 AI 系统中复现这一点、又该如何复现，却远没有那么清楚。

我们[近期发表于 JAIR](https://www.jair.org/index.php/jair) 的新论文证明，系统可以做到将直觉式感知与可解释的概念推理相结合。我们所描述的系统 ∂ILP 对噪声鲁棒、数据高效，并能产出可解释的规则。

![一张对比表：深度学习对噪声鲁棒、能从非符号数据中学习，但数据效率低且不可解释；相反，符号程序合成不具备噪声鲁棒性、也无法从非符号数据中学习，但数据高效且可解释。与两者都不同的是，我们提出的系统 ∂ILP 成功满足了全部四项标准。](https://lh3.googleusercontent.com/W4Jgfh694UAVnMCdIxxNr0oTgJB4qNhQbrm9JD5MrnKg-_b_G1CUBIDkXl2ZwqbIIbUZu4RPuWLFO5OWYk_Rf8PBg0Vzdrj8J-fUyqGhNua1lIux2Q=w1440)

我们用一个归纳任务展示 ∂ILP 的工作方式：它收到一对表示数字的图像，需要输出一个标签（0 或 1），表明左图中的数字是否小于右图中的数字。解决这一问题需要两种思维：你需要直觉式感知思维来把图像识别为某个具体数字的表征，也需要概念性思维来完整地理解「小于」关系的一般性。

![「小于」归纳任务的示意：展示成对手写数字图像，用小于号进行比较，并根据左边的数字是否小于右边的数字标注「TRUE」或「FALSE」。](https://lh3.googleusercontent.com/X_kfXD_VMZVmHbQNxxtS3Bm2O_HUpjohSQvlE9k0LTZWwIafaQXYPZ_1MV6kCKc0NKt4Z8glfsHtmYLWJv8WV0_Bwc4BhHdM4Dy4Geq2vg4piT47=w1440)

一个归纳任务示例

如果给标准深度学习模型（例如带 MLP 的卷积神经网络）足够的训练数据，它能有效学会解决这一任务。训练完成后，你可以给它一对从未见过的新图像，它会正确分类。然而，只有当你给它的每一对数字组合都有多个样例时，它才能正确泛化。这个模型擅长视觉泛化：在测试集中的每一对数字都见过的情况下，泛化到新图像（见下方绿色框）。但它不具备符号泛化能力：无法泛化到从未见过的新数字组合（见下方蓝色框）。[Gary Marcus](https://arxiv.org/abs/1801.00631) 和 [Joel Grus](https://joelgrus.com/2016/05/23/fizz-buzz-in-tensorflow/) 等研究者已在近期发人深省的文章中指出这一点。

![图示视觉泛化与符号泛化的区别。训练区块展示了观察到的数字对「4 < 5」「5 < 6」以及未观察的「4 < 6」。测试阶段，「视觉泛化」（Visual Generalisation）指向一个绿色框，内含「新数字、已知关系」（「4 < 5」「5 < 6」），而「符号泛化」（Symbolic Generalisation）指向一个蓝色框，内含训练期间未观察到的关系「Not observed during training」（「4 < 6」）。](https://lh3.googleusercontent.com/DI_hrSF5nDVhoeok1eOhiOY6Bda7exdLMeRnwgwpgyeFX5BvYZAJcRvUq9dAEH4-sIGmUbbtnQ997IWkicDfp0DqfOGveXzqwjCV4kiJv6bIxgtluQ=w1440)

∂ILP 与标准神经网络的不同之处在于它能够进行符号泛化；与标准符号程序的不同之处在于它能够进行视觉泛化。它从样例中学习显式的程序，这些程序可读、可解释、可验证。∂ILP 得到一个部分的样例集合（期望结果），并生成一个满足这些结果的程序。它使用梯度下降在程序空间中搜索。如果程序的输出与参考数据中的期望输出冲突，系统会修改程序以更好地匹配数据。

![展示 ∂ILP 训练过程的流程图：「期望结果」（Desired Results）作为输入送入「显式程序」（Explicit Program）区块，其中包含「lessThan」「foo」「bar」函数的代码。程序预测输出到「预测结果」（Predicted Results）区块，并与「期望结果」进行校验。训练循环根据预测结果不断修正「显式程序」。](https://lh3.googleusercontent.com/po1ukeb5r66BRIkEz9luHxQ0_kp25k-M29dU3lukLctKdCT2vdRgNRbkfiTr6OyUHO8pwADegqP9GDjo3mmM8uAkvDWB8Qw4rgPvn9qygWWkfPnvNA=w1440)

此图展示了 ∂ILP 的训练循环

我们的系统 ∂ILP 能够进行符号泛化。一旦它见过足够多的 x < y、y < z、x < z 示例，它就会考虑「<」关系可能是传递性的。一旦领悟了这一通用规则，它就能把它应用到从未见过的新数字对上。

![折线图：测试误差相对于训练期间未见数字对比例的关系，比较标准深度学习「基线」（baseline，蓝色线）与「∂ILP」（绿色线）。当未见数字对的比例从 0.0 增加到 0.9 时，基线的测试误差急剧上升至 0.40 以上，而 ∂ILP 的测试误差保持在低得多的水平，展示了它对未见数据的符号泛化能力。](https://lh3.googleusercontent.com/75244dLexhVjIalezJdZzl66It7Qnfr2SzQRZz5JCeO7W_HBgSCKZJJGH3bpwTHuBT2Mv7Rhpn1UoEX4mhb06e0tANixuVNeLVZUf4IXkGD1jDE2kDk=w1440)

上图概括了我们的「小于」实验：标准深度神经网络（蓝色曲线）无法正确泛化到未见过的数字对。相比之下，∂ILP（绿色线）在只见过 40% 的数字对时仍能取得较低的测试误差；这表明它具备符号泛化能力。

我们相信，我们的系统在一定程度上回答了「深度神经网络能否实现符号泛化」这一问题。在未来的工作中，我们计划把类 ∂ILP 的系统集成到强化学习智能体和更大的深度学习模块中。我们希望借此赋予我们的系统既能推理、又能反应的能力。

**注**

论文可在[此处](https://www.jair.org/index.php/jair)阅读。

---
title: "更深入理解动量在非凸优化中的作用"
title_en: "A deeper understanding of the role of momentum in non-convex optimization"
date: 2020-10-16
source: https://ai.facebook.com/blog/a-deeper-understanding-of-the-role-of-momentum-in-non-convex-optimization
crawled: 2026-09-22
translated: 2026-09-22
---

# 更深入理解动量在非凸优化中的作用

> 原文：[A deeper understanding of the role of momentum in non-convex optimization](https://ai.facebook.com/blog/a-deeper-understanding-of-the-role-of-momentum-in-non-convex-optimization) · Meta AI（Wayback 存档）

**研究内容：**理解何时以及为何加入动量（momentum）能让机器学习模型的优化更高效。优化算法是现代机器学习的关键，它们决定模型如何在训练期间吸收信息，并在下一次尝试中调整以表现得更好。在这些优化算法中，带动量的随机梯度下降法（SGD+M）是许多子领域（包括计算机视觉）中最常用的算法之一。但尽管 SGD+M 应用广泛，理论上对它的理解仍然薄弱。动量的实际好处毋庸置疑，但迄今为止，限定学习速度（即收敛速度）的最好已知理论给 SGD+M 的评价低于不带动量的 SGD，这与现实世界中的表现相矛盾。我们的工作建立了一个更紧的收敛速率界，提供了对动量如何起作用的更完整理解，从而回答了何时 SGD+M 是最高效的优化算法。

**工作原理：**我们对 SGD+M 的分析依赖一个关键想法：动量在以随机原始平均（stochastic primal averaging，SPA）形式实现时更容易理解。SPA 方程形式在功能上与 SGD+M 等价，但在数学上更容易分析。使用 SPA 形式使我们能够得出比以往研究更紧的收敛速率界。我们确定，在对梯度的一个合理假设下，我们理论的收敛速率界几乎与 SGD 一样紧，仅多出一个对任何合理的动量和步长选择都可以忽略的因子。在不做额外假设的情况下，SGD 与 SGD+M 的界之间的差距在最终收敛速率上缩小到只有根号 2 倍的因子。

由于 SPA 更容易分析，我们可以推导出关于动量对深度学习问题影响的诸多洞见——这些洞见用标准形式的 SGD+M 是无法得到的。例如，我们发现，当梯度缓冲区与真实梯度正相关时，动量会加速收敛，从而抵消噪声对收敛速率界的影响。经验上已经证明这种情况发生在训练的早期迭代中。由于这些早期迭代也最不稳定，这解释了为什么动量在早期迭代中更能加速学习，而在优化过程后期作用随之减弱。

通过 SPA 形式分析 SGD+M 还为研究者提供了训练期间如何最有效调整学习率的洞见。传统上，学习率参数会定期降低，让模型自我微调以达到最佳性能。在使用 SPA 形式时，这种常见方案实际上不再合理。相反，我们的理论支持一种修改后的方案：通过降低动量参数而非学习率参数来获得最佳结果。

**为什么重要：**动量是现代深度学习训练的关键组件，更好地理解它对改进优化算法至关重要。使用 SPA 形式使我们能够拆解此前只能在实际中观察到的动量性质。我们的发现表明，在向更先进的优化方法添加动量时，关键是使用 SPA 形式中的那种平均——即对步长的平均，而不是对梯度的平均。这一洞见让我们几乎可以把动量应用于任何现有的优化方法，以潜在地提升其性能。更好的优化算法的发展直接带来 AI 系统更快的训练，加速研究并让更多人受益。

阅读完整论文：Understanding the role of momentum in non-convex optimization: Practical insights from a Lyapunov analysis

**作者**

- Aaron Defazio，研究科学家

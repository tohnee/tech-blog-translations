---
title: "DeepMind 在 NeurIPS 2022 上的最新研究"
title_en: "DeepMind’s latest research at NeurIPS 2022"
source: https://deepmind.google/blog/deepminds-latest-research-at-neurips-2022/
site: deepmind
date: 2022-11-25
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 NeurIPS 2022 上的最新研究

> 原文：[DeepMind’s latest research at NeurIPS 2022](https://deepmind.google/blog/deepminds-latest-research-at-neurips-2022/) · Google DeepMind

推进一流的大型模型、计算最优的强化学习智能体，以及更透明、合乎伦理且公平的 AI 系统

第三十六届神经信息处理系统大会（[NeurIPS 2022](https://nips.cc/Conferences/2022)）将于 2022 年 11 月 28 日至 12 月 9 日以线上线下混合形式举行，主会场设在美国新奥尔良。

NeurIPS 是全球最大的人工智能（AI）与机器学习（ML）会议，我们很荣幸能以钻石赞助商的身份支持这一盛会，助力 AI 与 ML 社区交流研究进展。

来自 DeepMind 各团队的学者将展示 47 篇论文，其中包括 35 项外部合作，以线上分论坛与海报形式呈现。以下是我们所展示研究的简要介绍：

## 一流的大型模型

大型模型（LM）——在海量数据上训练的生成式 AI 系统——已在语言、文本、音频和图像生成等领域取得令人惊叹的表现。它们成功的一部分要归功于自身的庞大规模。

然而，在 Chinchilla 中，我们打造了一个[参数量为 700 亿、却胜过许多更大模型的](https://www.deepmind.com/publications/an-empirical-analysis-of-compute-optimal-large-language-model-training)语言模型，其中包括 Gopher。我们更新了大型模型的标度律（scaling law），表明此前训练的模型相对于所进行的训练量而言过于庞大。这项工作已经影响了遵循这些更新规则的其他模型，催生出更精简、更出色的模型，并在本届会议上获得了[主会杰出论文奖](https://blog.neurips.cc/2022/11/21/announcing-the-neurips-2022-awards/)。

在 Chinchilla 以及我们的多模态模型 NFNets 和 Perceiver 的基础上，我们还展示了 [Flamingo——一个少样本学习视觉语言模型家族](https://arxiv.org/abs/2204.14198)。Flamingo 同时处理图像、视频和文本数据，是纯视觉模型与纯语言模型之间的一座桥梁。单个 Flamingo 模型就在广泛的开放式多模态任务上刷新了少样本学习的最优纪录（state of the art）。

然而，对于基于 transformer 的模型的能力而言，规模与架构并非仅有的重要因素。数据属性同样举足轻重，我们将在关于[促进 transformer 模型上下文学习的数据属性](https://openreview.net/forum?id=lHj-q9BSRjF)的报告中展开讨论。

## 优化强化学习

强化学习（RL）作为一种创建能够应对广泛复杂任务的通用 AI 系统的方法，已展现出巨大前景。它带来了从围棋到数学等众多领域的突破，我们也在不断寻找让强化学习智能体更聪明、更精简的方法。

我们介绍了一种新方法，通过[大幅扩展可供智能体检索的信息规模](https://arxiv.org/abs/2206.05314)，以计算高效的方式提升强化学习智能体的决策能力。

我们还将展示一种概念简单而通用的方法，用于在视觉复杂的环境中进行好奇心驱动的探索——一个名为 [BYOL-Explore](https://openreview.net/pdf?id=qHGCH75usg) 的强化学习智能体。它在具备超强性能的同时对噪声保持鲁棒，而且比以往的工作简洁得多。

## 算法进展

从压缩数据到运行天气预报模拟，算法是现代计算的基本组成部分。因此，在大规模运行时，渐进式的改进就能产生巨大影响，帮助节省能源、时间和金钱。

我们分享一种全新的、高度可扩展的[计算机网络自动配置](https://www.deepmind.com/publications/learning-to-configure-computer-networks-with-neural-algorithmic-reasoning)方法，该方法基于神经算法推理（neural algorithmic reasoning）。结果表明，我们高度灵活的方案比当前最优方法最快可达 490 倍，同时满足大部分输入约束。

在同一个分论坛中，我们还对此前停留在理论层面的"算法对齐"（algorithmic alignment）概念进行了严谨的探索，[凸显了图神经网络与动态规划之间微妙的关系](https://www.deepmind.com/publications/graph-neural-networks-are-dynamic-programmers)，以及如何最优地结合二者以优化分布外性能。

## 负责任地开拓

DeepMind 使命的核心，是我们在 AI 领域扮演负责任开拓者的承诺。我们致力于开发透明、合乎伦理且公平的 AI 系统。

解释和理解复杂 AI 系统的行为，是创建公平、透明、准确系统的重要一环。我们提出[一组体现这些目标的要求（desiderata），并描述了满足这些要求的切实途径](https://openreview.net/pdf?id=bk8vkdQfBS)：训练一个 AI 系统为自身构建因果模型，使它能够以有意义的方式解释自己的行为。

要在世界中安全、合乎伦理地行动，AI 智能体必须能够对伤害进行推理并避免有害行为。我们将介绍一项关于名为[反事实伤害](https://arxiv.org/abs/2204.12993)（counterfactual harm）的新统计度量的合作研究，并演示它如何克服标准方法的缺陷，从而避免推行有害的策略。

最后，我们将展示我们的新论文，其中提出了[诊断并缓解由分布偏移引起的模型公平性失效的方法](https://www.deepmind.com/publications/diagnosing-failures-of-fairness-transfer-across-distribution-shift-in-real-world-medical-settings)，说明这些问题对于在医疗环境中部署安全的机器学习技术有多么重要。

在[这里](https://deepmind.events/events/neurips2022/resources)查看我们在 NeurIPS 2022 上工作的完整清单。

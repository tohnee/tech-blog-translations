---
title: "DeepMind 在 ICML 2017 的论文（第一部分）"
title_en: "DeepMind papers at ICML 2017 (part one)"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-one/
site: deepmind
date: 2017-08-04
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 ICML 2017 的论文（第一部分）

> 原文：[DeepMind papers at ICML 2017 (part one)](https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-one/) · Google DeepMind

本系列共三篇，这是第一篇，简要介绍我们将在澳大利亚悉尼 ICML 2017 大会上展示的论文。

## Decoupled Neural Interfaces using Synthetic Gradients（使用合成梯度的解耦神经接口）

**作者：** Max Jaderberg, Wojciech Marian Czarnecki, Simon Osindero, Oriol Vinyals, Alex Graves, David Silver, Koray Kavukcuoglu

训练神经网络时，各个模块（层）是相互锁定的：它们只能在反向传播之后才能更新。我们通过引入一个学到的误差梯度模型——合成梯度（Synthetic Gradients）——来消除这一约束，这意味着我们可以在没有完整反向传播的情况下更新网络。我们展示了如何将其应用于前馈网络（使每一层都能异步训练）、循环神经网络（RNN，延长模型能够记忆的时间跨度），以及多网络系统（使它们能够相互通信）。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1608.05343)。

**ICML 会场信息：**

Monday 07 August, 10:30-10:48 @ Darling Harbour Theatre（口头报告）

Monday 07 August, 18:30-22:00 PM @ Gallery #1（海报）

## Parallel Multiscale Autoregressive Density Estimation（并行多尺度自回归密度估计）

**作者：** Scott Reed, Aäron van den Oord, Nal Kalchbrenner, Ziyu Wang, Dan Belov, Nando de Freitas

并行多尺度自回归密度估计器可以生成高分辨率（512x512）图像，相比其他自回归模型有数个数量级的加速。我们在类别条件图像生成、文本到图像合成以及动作条件视频生成上评估了该模型，结果表明，在允许高效采样的非像素自回归密度模型中，我们的模型取得了最佳结果。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1703.03664)。

**ICML 会场信息：**

Monday 07 August, 10:48-11:06 @ Parkside 1（口头报告）

Monday 07 August, 18:30-20:00 @ Gallery #10（海报）

## Understanding Synthetic Gradients and Decoupled Neural Interfaces（理解合成梯度与解耦神经接口）

**作者：** Wojtek Czarnecki, Grzegorz Świrszcz, Max Jaderberg, Simon Osindero, Oriol Vinyals, Koray Kavukcuoglu

合成梯度已在经验上被证明在前馈与循环两种情形下都能奏效。这项工作聚焦于它究竟为什么以及如何起作用——论文证明，在温和的假设下，临界点得以保留；并且在线性模型这一最简单的情形中，基于合成梯度进行的学习确实收敛到全局最优。另一方面，我们通过经验展示，训练得到的模型可能与使用反向传播得到的模型存在定性上的差异。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1703.00522)。

**ICML 会场信息：**

Monday 07 August, 10:48-11:06 @ Darling Harbour Theatre（口头报告）

Monday 07 August, 18:30-20:00 @ Gallery #9（海报）

## Minimax Regret Bounds for Reinforcement Learning（强化学习的极小极大后悔界）

**作者：** Mohammad Gheshlaghi Azar, Ian Osband, Remi Munos

我们研究强化学习在有限时域 MDP 上可证明最优探索的问题。我们证明，对价值迭代做乐观化修改，可以达到量级为 (HSAT)^(1/2)（相差一个对数因子）的后悔界，其中 H 是时域长度，S 是状态数，A 是动作数，T 是时间步数。这一结果改进了此前已知的最优界 HS(AT)^(1/2)，后者由 [Jaksch, Ortner, Auer, 2010] 的 UCRL2 算法取得。我们新结果的关键意义在于：当 T 较大时，我们算法的样本复杂度匹配 Ω(HSAT)^(1/2) 的最优下界。我们的分析包含两个关键洞见：一是将集中不等式谨慎地应用于作为整体的最优价值函数，而非转移概率（以改进关于 S 的标度）；二是定义了基于 Bernstein 的「探索加成」（exploration bonuses），它使用下一状态估计值的经验方差（以改进关于 H 的标度）。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1703.05449)。

**ICML 会场信息：**

Monday 07 August, 10:48-11:06 @ C4.5（口头报告）

Monday 07 August, 18:30-22:00 @ Gallery #12（海报）

## Video Pixel Networks（视频像素网络）

**作者：** Nal Kalchbrenner, Aaron van den Oord, Karen Simonyan, Ivo Danihelka, Oriol Vinyals, Alex Graves, Koray Kavukcuoglu

预测视频帧的后续内容，是无监督学习中的一项标志性任务。我们提出一个概率化的视频模型 VPN，它能够对未来视频帧做出准确而锐利的预测。VPN 首次在 Moving MNIST 数据集上取得了近乎满分的成绩，并能对手臂运动的未来生成多达 18 帧的合理预测。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1610.00527)。

**ICML 会场信息：**

Monday 07 August, 11:06-11:24 @ Parkside 1（口头报告）

Monday 07 August, 18:30-22:00 @ Gallery #18（海报）

## Sharp Minima Can Generalize For Deep Nets（深度网络中的尖锐极小值也能泛化）

**作者：** Laurent Dinh (Univ. Montreal), Razvan Pascanu, Samy Bengio (Google Brain), Yoshua Bengio (Univ. Montreal)

从经验上看，深度网络即使具备对数据过拟合的容量，也能很好地泛化。此外，随机梯度下降（SGD）似乎能产生比批量方法泛化得更好的模型。解释这一现象的一种假说是：SGD 的噪声帮助模型找到了宽阔的极小值，它们比尖锐（狭窄）的极小值泛化得更好。在这项工作中，我们尝试加深对这一假说的理解。我们证明，由于神经网络自身的结构，这一假说在已有的宽度或锐度定义下并不成立。这提示批次大小与泛化之间并不存在因果关系。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1703.04933)。

**ICML 会场信息：**

Monday 07 August, 11:06-11:24 @ C4.8（口头报告）

Tuesday 08 August, 18:30-22:00 @ Gallery #3（海报）

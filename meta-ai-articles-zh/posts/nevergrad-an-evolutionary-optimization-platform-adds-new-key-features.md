---
title: "演化优化平台 Nevergrad 新增多项关键特性"
title_en: "Nevergrad, an evolutionary optimization platform, adds new key features"
date: 2019-03-15
source: https://ai.facebook.com/blog/nevergrad-an-evolutionary-optimization-platform-adds-new-key-features
crawled: 2026-09-22
translated: 2026-09-22
---

# 演化优化平台 Nevergrad 新增多项关键特性

> 原文：[Nevergrad, an evolutionary optimization platform, adds new key features](https://ai.facebook.com/blog/nevergrad-an-evolutionary-optimization-platform-adds-new-key-features) · Meta AI（Wayback 存档）

**这是什么**：我们为 Nevergrad——Facebook AI 的无导数与演化优化开源 Python3 库——添加了一系列值得注意的新特性。这些增强使研究者和工程师能够处理多个目标（多目标优化）或带约束的问题。这类用法在自然语言处理等领域很常见，例如一个翻译模型可能需要同时在多个指标或基准上优化。由于 Nevergrad 通过易用的开放 Python 源码提供前沿算法，任何人都可以用它轻松测试和比较针对特定问题的不同方法，或使用知名基准来评估某个方法与当前最先进水平的对比。为进一步改进 Nevergrad，我们与 IOH Profiler 合作创办了开放优化竞赛（Open Optimization Competition）。竞赛同时接受新的优化算法以及对 Nevergrad 核心工具的改进投稿。参赛作品须在 9 月 30 日前提交方可参与评奖，更多信息见此处。

**它做什么**：Nevergrad 是一个面向 AI 研究者的易用优化工具箱，包括那些不是 Python 极客的人。优化任何函数只需几行代码：

```
import nevergrad as ng

def square(x):
    return sum((x - .5)**2)

optimizer = ng.optimizers.OnePlusOne(instrumentation=2, budget=100)
recommendation = optimizer.minimize(square)
print(recommendation.value)  # 最优 args 与 kwargs
>>> array([0.500, 0.499])
```

该平台为使用各种各样的无导数算法提供了单一、一致的接口，包括演化策略、差分进化、粒子群优化、Cobyla 和贝叶斯优化。该平台也便于对新的无导数优化方法进行研究，新算法可以轻松并入平台。通过与 IOH 的联合努力以及 Dagstuhl 黑箱优化会议上研究者的意见，我们对 Nevergrad 做出了多项值得注意的改进：

- **多目标优化**。
- **约束优化**。
- **简化的问题参数化**。指定一个 0.001 到 1.0 之间对数分布的变量只需 `ng.p.Log(lower=0.001, upper=1.0)`。
- **能力图（competence map）优化器**。我们提供自动选择最佳优化方法的算法，综合考虑你的计算预算、维度、变量类型和并行度。（题图说明：该图展示了在非常多样的一组示例问题上的结果。数字和颜色对应某个优化器胜过其他算法的概率。算法（NGO、Shiva、CMA 等）按性能排序，最优算法在左侧。左侧还列出了表现最好的 6 种算法。）NGO 和 Shiva 是该测试床中表现最好的两种优化器，是手工设计、极为通用的能力图优化方法。
- **链式组合优化算法与问题分解的工具**——把不同变量分配给不同优化器，从而把问题拆分为多个子问题。
- **与 HiPlot（Facebook AI 的轻量交互式可视化工具）的接口**。这让研究者可以轻松探索优化过程，或在 Jupyter notebook 中使用交互式图表观察差异很大的算法的行为。（题图说明：对一个最优值在 (100,100)、初始猜测在 (0,0) 附近（标准差为 1）的二维绝对值之和函数的优化示例。不同算法以不同方式适应，找到远离初始猜测的最优值（蓝色为前几次迭代，红色为后续迭代）。）

作为一项实验性功能，我们会定期比较各优化器的性能并在此发布结果。AI 研究者可以轻松地用新基准或新优化器扩展 Nevergrad 并在本地运行，或在 GitHub 上创建 pull request，把他们的贡献合并进来并纳入这些自动化测试。

**为什么重要**：大多数机器学习任务——从自然语言处理到图像分类再到翻译等众多领域——都依赖无导数优化来调优模型中的参数和/或超参数。Nevergrad 让研究者和工程师可以轻松找到最佳做法，并开发更新更好的技术。多目标优化（此例详述了 Nevergrad 中的用法）在每个人的生活中都很常见。例如，有人想购买某样东西时，可能希望选项同时便宜、离得近、相关且高质量。自首次发布以来，Nevergrad 已成为广泛使用的研究工具。我们现在分享的新特性使其可以用于更多用例，如多智能体电力系统、物理学（光子学或防反射涂层）以及游戏控制。Nevergrad 还提供了能更好适应特定问题结构的通用算法，包括通过新的参数化系统在演化算法中使用特定的变异或重组。

**获取地址**：

- GitHub：https://github.com/facebookresearch/nevergrad
- 文档：https://facebookresearch.github.io/nevergrad/index.html
- Pypi：`pip install nevergrad`

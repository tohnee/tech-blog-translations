---
title: "开源 TRFL：强化学习基础组件库"
title_en: "Open sourcing TRFL: a library of reinforcement learning building blocks"
source: https://deepmind.google/blog/open-sourcing-trfl-a-library-of-reinforcement-learning-building-blocks/
site: deepmind
date: 2018-10-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 开源 TRFL：强化学习基础组件库

> 原文：[Open sourcing TRFL: a library of reinforcement learning building blocks](https://deepmind.google/blog/open-sourcing-trfl-a-library-of-reinforcement-learning-building-blocks/) · Google DeepMind

今天，我们开源了一个[新的库](https://github.com/deepmind/trfl/)，其中包含用于在 TensorFlow 中编写强化学习（RL）智能体的实用基础组件。它被命名为 TRFL（发音同「truffle」），汇集了我们内部在众多最成功的智能体（如 DQN、DDPG 和 Importance Weighted Actor Learner Architecture）中使用的关键算法组件。

一个典型的深度强化学习智能体由大量相互作用的组件构成：至少包括环境和某种表示价值或策略的深度网络，但通常还包括诸如学到的环境模型、伪奖励函数或回放系统等组件。

这些部分往往以微妙的方式相互作用（论文中往往缺乏充分记录，正如 [Henderson 等人](https://arxiv.org/pdf/1709.06560.pdf)所指出的），因此很难在这种庞大的计算图中定位 bug。OpenAI 最近的一篇[博客文章](https://openai.com/blog/openai-baselines-dqn/)凸显了这一问题：他们分析了最流行的几个开源强化学习智能体实现，发现 10 个中有 6 个「存在由社区成员发现并经作者确认的微妙 bug」。

解决这一问题、并帮助研究界试图复现论文结果的人的一种方法，是开源完整的智能体实现。例如，我们最近[开源了 v-trace 智能体的可扩展分布式实现](https://deepmind.com/blog/article/impala-scalable-distributed-deeprl-dmlab-30)。这些大型智能体代码库对复现研究非常有用，但也难以修改和扩展。另一种与之互补的方法，是提供可靠、经过充分测试的通用基础组件实现，可用于各种不同的 RL 智能体。此外，将这些核心组件以一致的 API 抽象到单一库中，也让组合来自不同论文的想法变得更加简单。

TRFL 库既包含实现经典 RL 算法的函数，也包含更前沿的技术。这里提供的损失函数和其他操作均以纯 TensorFlow 实现。它们不是完整的算法，而是构建功能完备的 RL 智能体时所需的 RL 专用数学运算的实现。

对于基于价值的强化学习，我们提供了在离散动作空间中学习的 TensorFlow 算子，如 TD 学习、Sarsa、Q 学习及其变体，以及实现连续控制算法（如 DPG）的算子。我们还包含用于学习分布式价值函数的算子。这些算子支持批处理，并返回一个可交给 TensorFlow 优化器最小化的损失。有些损失作用于转移批（如 Sarsa、Q 学习等），另一些则作用于轨迹批（如 Q lambda、Retrace 等）。对于基于策略的方法，我们提供了可以轻松实现 A2C 等在线方法的工具，同时支持 v-trace 等离策略修正技术。还支持在连续动作空间中计算策略梯度。最后，TRFL 还提供了 UNREAL 所使用的辅助伪奖励函数的实现，我们发现它们能在多种领域提高数据效率。

这不是一次性的发布。由于这个库在 DeepMind 内部被广泛使用，我们将持续维护它，并随时间推移添加新功能。我们也热切期待更广泛的 RL 社区[向该库贡献代码](https://github.com/deepmind/trfl/blob/master/CONTRIBUTING.md)。

这个库由 DeepMind 的研究工程团队创建。

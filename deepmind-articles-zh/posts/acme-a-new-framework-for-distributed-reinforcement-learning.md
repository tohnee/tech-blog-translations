---
title: "Acme：一个新的分布式强化学习框架"
title_en: "Acme: A new framework for distributed reinforcement learning"
source: https://deepmind.google/blog/acme-a-new-framework-for-distributed-reinforcement-learning/
site: deepmind
date: 2020-06-01
crawled: 2026-09-13
translated: 2026-09-13
---

# Acme：一个新的分布式强化学习框架

> 原文：[Acme: A new framework for distributed reinforcement learning](https://deepmind.google/blog/acme-a-new-framework-for-distributed-reinforcement-learning/) · Google DeepMind

总体而言，Acme 的高层目标如下：

1. 实现我们的方法和结果的可复现性——这有助于澄清究竟是什么让一个 RL 问题变难或变易，而这一点往往并不明显。
2. 简化我们（以及整个社区）设计新算法的方式——我们希望下一个 RL 智能体对每个人来说都更容易编写！
3. 提升 RL 智能体的可读性——从论文过渡到代码时不应该有任何隐藏的意外。

为实现这些目标，Acme 的设计还弥合了大规模、中规模和小规模实验之间的鸿沟。我们是通过在许多不同尺度上仔细思考智能体的设计来做到这一点的。

在最抽象的层面上，我们可以把 Acme 看作一个经典的 RL 接口（任何 RL 入门教材中都有），它把一个 actor（即选择动作的智能体）连接到一个环境。这个 actor 是一个简单的接口，具有选择动作、进行观测和自我更新的方法。在内部，学习型智能体会把问题进一步拆分为「执行动作」和「从数据中学习」两个组件。从表面上看，这让我们可以在许多不同的智能体之间复用执行动作的部分。但更重要的是，它提供了一个关键的边界，可以在其上拆分和并行化学习过程。我们甚至可以由此向下扩展，无缝应对不存在环境、只有固定数据集的批量 RL（batch RL）设定。这些不同复杂度层次的图示如下：

![一个经典强化学习接口的示意图：Actor 向下向 Environment 发送动作，Environment 又把观测和奖励向上送回 Actor。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228c6b6b755e529e96ea6c6_Fig201.gif)

这种设计让我们可以轻松地在小规模场景中创建、测试和调试新型智能体，然后再将其扩大规模——而全程使用同一套执行与学习代码。Acme 还提供了许多实用工具，从检查点保存、快照到底层计算辅助工具。这些工具往往是任何 RL 算法默默无闻的英雄，在 Acme 中我们力求让它们尽可能简单易懂。

为了支撑这一设计，Acme 还使用了 [Reverb](https://deepmind.com/research/open-source/Reverb)：一个新颖、高效的专为机器学习（和强化学习）数据打造的数据存储系统。Reverb 主要用作分布式强化学习算法中的经验回放系统，但它也支持其他数据结构表示，例如 FIFO 队列和优先级队列。这让我们可以把它无缝用于 on-policy 和 off-policy 算法。Acme 与 Reverb 从一开始就是为了让彼此良好协作而设计的，但 Reverb 也完全可以独立使用，欢迎去一探究竟！

除了基础设施之外，我们还发布了用 Acme 构建的多款智能体的单进程版本，涵盖连续控制（D4PG、MPO 等）、离散 Q-learning（DQN 和 R2D2）等。只需极少量的改动——沿执行/学习边界拆分——我们就能以分布式方式运行这些相同的智能体。我们的首个版本聚焦于单进程智能体，因为这是学生和研究人员最常使用的形态。

我们还对上述智能体在多个环境中做了细致的基准测试，分别是 [control suite](https://github.com/google-deepmind/dm_control)、[Atari](https://github.com/mgbellemare/Arcade-Learning-Environment) 和 [bsuite](https://github.com/google-deepmind/bsuite)。

## 展示使用 Acme 框架训练的智能体的视频播放列表

虽然更多结果可以在我们的[论文](https://arxiv.org/abs/2006.00979)中找到，我们在下图中比较了单个智能体（D4PG）在连续控制任务上的性能，分别以 actor 步数和实际耗时（wall clock time）为度量。由于我们限制了数据插入回放缓冲区的速率（更深入的讨论见论文），在比较智能体获得的奖励与其与环境交互的次数（actor 步数）时，可以看到大致相同的性能。然而，随着智能体进一步并行化，我们看到智能体学习速度上的收益。在观测被限制在较小特征空间的相对较小的领域上，即使只是适度增加并行度（4 个 actor），也会让智能体学会最优策略所需的时间缩短到一半以下：

![两张折线图，展示 D4PG 智能体在 humanoid:run 任务上使用 1、2、4 个 actor 时的性能。左图显示，各配置下回合回报随 actor 步数（百万）的变化保持一致。右图显示，随并行度增加，回合回报相对学习器实际耗时（小时）显著改善，4 个 actor 用不到单进程一半的时间就达到了最高回报。](https://lh3.googleusercontent.com/T7CeRTWA5ZdRUG4BNtLrIxMsvhmcrCGYnj2HzGq2rZhoOe6Qa0f46WYEtEOyWmKj9fgWw7ZqgXdaLnoTD3H01IKskjsdQurSwDQnEaamjubefWYyiQ=w1440)

但对于更复杂的领域——其观测是生成成本相对较高的图像——我们看到的收益要大得多：

![两张折线图，展示 D4PG 智能体在 walker:run 任务上使用 1、2、8、16 个 actor 时的性能。左图显示，各配置下回合回报随 actor 步数（百万）的变化保持一致。右图显示，随并行度增加，回合回报相对学习器实际耗时（小时）显著改善，8 和 16 个 actor 用远少于单进程或 2 个 actor 配置的时间就达到了高回报。](https://lh3.googleusercontent.com/3DqYCeu-j5A6MjC0UVjSZeYj7LwR3ekHX0roObF97p0JLxer7DV1OlERGz5iB4L43SVhsDPW6prd6djs1F5d-GkauWh0CE-LTM8WMbNVvvdHF9mX-w=w1440)

而在 Atari 游戏这类数据采集成本更高、学习过程通常更长的领域，收益还可以更大。不过需要注意的是，这些结果在分布式与非分布式设定下共用同一套执行与学习代码。因此，在较小规模上试验这些智能体和结果是完全可行的——事实上，在开发新智能体时我们一直就是这么做的！

关于这一设计的更详细描述，以及基线智能体的更多结果，请参见我们的[论文](https://arxiv.org/abs/2006.00979)。或者更好的是，去看看我们的 [GitHub 仓库](https://github.com/deepmind/acme)，了解如何开始使用 Acme 来简化你自己的智能体！

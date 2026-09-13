---
title: "Decoupled DiLoCo：韧性分布式 AI 训练的新前沿"
title_en: "Decoupled DiLoCo: A new frontier for resilient, distributed AI training"
source: https://deepmind.google/blog/decoupled-diloco/
site: deepmind
date: 2026-04-23
crawled: 2026-09-13
translated: 2026-09-13
---

# Decoupled DiLoCo：韧性分布式 AI 训练的新前沿

> 原文：[Decoupled DiLoCo: A new frontier for resilient, distributed AI training](https://deepmind.google/blog/decoupled-diloco/) · Google DeepMind

我们的新分布式架构有助于在相距遥远的数据中心之间训练大语言模型——带宽更低，硬件韧性更强。

传统上，训练一个前沿 AI 模型依赖于一个大型的、紧耦合的系统，其中相同的芯片必须保持近乎完美的同步。这种方法对当今最先进的模型非常有效，但当我们着眼于未来几代的规模时，在数千个芯片之间维持这种级别的同步将成为一项重大的工程挑战。

今天，在一篇[新论文](https://arxiv.org/abs/2604.21428v1)中，我们很高兴分享针对这一问题的一种新方法，称为 Decoupled DiLoCo（分布式低通信，Distributed Low-Communication）。通过将大型训练任务拆分到相互解耦的「孤岛」算力上、并在它们之间流动异步数据，这一架构将局部中断隔离开来，使系统的其他部分能够继续高效学习。

其结果是一种更具韧性、更灵活的方式，可以在全球分布的数据中心之间训练先进模型。至关重要的是，Decoupled DiLoCo 不会遭受数据并行（Data-Parallel）等先前分布式方法在全球规模下不切实际的通信延迟。

随着前沿模型在规模和复杂性上持续增长，我们正在探索多种多样的方法，在更多的算力、更多的地点和更多样的硬件上训练模型。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

图 1：将训练任务解耦为独立的「孤岛」算力（学习单元，learner units），即便在同等水平的硬件故障下也能保持大体上不间断的训练，因为这些故障的影响被隔离开了。

## 在大规模下开发更具容错性的异步训练

Decoupled DiLoCo 建立在两项早期进展之上：[Pathways](https://blog.google/innovation-and-ai/products/introducing-pathways-next-generation-ai-architecture/) 引入了基于异步数据流的分布式 AI 系统；[DiLoCo](https://arxiv.org/abs/2311.08105) 则大幅降低了分布式数据中心之间所需的带宽，使跨遥远地点训练大语言模型成为现实。

Decoupled DiLoCo 将这些想法结合在一起，在大规模下更灵活地训练 AI 模型。它构建于 Pathways 之上，支持跨相互独立的算力孤岛（称为学习单元，learner units）进行异步训练，使某一区域的芯片故障不会打断其他区域的进展。

这套基础设施还具备自愈能力。在测试中，我们使用了一种名为「混沌工程（chaos engineering）」的方法，在训练运行期间人为引入硬件故障。Decoupled DiLoCo 在整个学习单元丢失后仍继续训练过程，并在它们重新上线时将其无缝重新纳入。

使用 Gemma 4 模型对 Decoupled DiLoCo 的测试表明，当硬件发生故障时，系统比更传统的训练方法保持了更高的学习集群可用性——同时最终达到相同的机器学习（ML）基准性能水平。

![三张并排的柱状图，比较 Data-Parallel（灰色）与 Decoupled DiLoCo（蓝色）在三项指标上的表现。「所需带宽」以对数刻度显示，在 8 个数据中心上 Data-Parallel 为 198 Gbps，Decoupled DiLoCo 为 0.84 Gbps。「有效产出（Goodput）」显示在硬件高故障率下 Data-Parallel 为 27%，Decoupled DiLoCo 为 88%。「ML 基准」显示平均准确率 Data-Parallel 为 64.4%，Decoupled DiLoCo 为 64.1%。](https://lh3.googleusercontent.com/dgWXJe3CEYV3TND6RvRPANNZ_YsErtYAWmFYC1BjQCn1QVLWx2mfBqyyUqAwaGPfBKV_81M6yE2IwV866_0EMu0Azx4_QFE3283E0Vz7dONAR7F5wA=w1440)![三张并排的柱状图，比较 Data-Parallel（灰色）与 Decoupled DiLoCo（蓝色）在三项指标上的表现。「所需带宽」以对数刻度显示，在 8 个数据中心上 Data-Parallel 为 198 Gbps，Decoupled DiLoCo 为 0.84 Gbps。「有效产出（Goodput）」显示在硬件高故障率下 Data-Parallel 为 27%，Decoupled DiLoCo 为 88%。「ML 基准」显示平均准确率 Data-Parallel 为 64.4%，Decoupled DiLoCo 为 64.1%。](https://lh3.googleusercontent.com/mnCZCyP0c3sdhYWFJ5ElGFfTnnEiwRCHHQz4t1VdJlLt4XoN6YnbYzdFL-edBXdwy0apZ9ZWSPDnrRxSHQke7ikyUTrtoTgluIHfa6GP3s28B55cHGE=w1440)

图 2：**左图**：Decoupled DiLoCo 方法所需的带宽比传统训练方法少几个数量级，因此非常高效。**中图**：随着硬件故障等级的升高，Decoupled DiLoCo 持续提供高水平的「有效产出（goodput）」，即有效训练，而其他方法的产出则急剧下滑。（前两张图基于模拟训练运行。）**右图**：在真实实验中，使用 Decoupled DiLoCo 训练的 Gemma 4 模型的基准 ML 性能与采用传统训练方法所达到的性能相当。

Decoupled DiLoCo 不仅对故障更有韧性，而且可用于执行生产级的、完全分布式的预训练。我们成功地在美国四个相互独立的地区，以 2-5 Gbps 的广域网带宽训练了一个 120 亿参数模型（这一水平利用数据中心设施之间现有的互联网连接相对容易实现，而无需在设施之间新建定制网络基础设施）。值得注意的是，该系统取得这一训练结果的速度比传统同步方法快 20 倍以上。这是因为我们的系统将必要的通信纳入更长的计算时段，避免了系统一部分必须等待另一部分的「阻塞」瓶颈。

## 推动 AI 训练基础设施的演进

在 Google，我们对 AI 训练采取全栈方法，涵盖硬件、软件基础设施和研究。越来越多的收益来自重新思考这些层次如何相互配合。

Decoupled DiLoCo 就是一例。通过支持以互联网规模的带宽运行训练任务，它可以利用任何闲置的算力——无论它位于何处——将搁浅的资源转化为有用的容量。

除了效率与韧性之外，这一训练范式还解锁了在单次训练中混用不同硬件世代的能力，例如 TPU v6e 与 TPU v5p。这种方法不仅延长了现有硬件的使用寿命，还增加了可用于模型训练的总算力。在我们的实验中，来自不同世代、以不同速度运行的芯片仍然达到了与单一芯片类型训练运行相当的 ML 性能，确保即使是较旧的硬件也能切实加速 AI 训练。

更重要的是，由于新一代硬件不会同时到达所有地方，能够跨世代训练可以缓解反复出现的后勤与容量瓶颈。

当我们今天推进 AI 基础设施的前沿时，我们将继续探索实现韧性系统的方法，以解锁下一代 AI。

[阅读我们的技术报告](https://arxiv.org/abs/2604.21428v1)

## 致谢

这项工作由来自 Google DeepMind 和 Google Research 的成员组成的团队完成。

Decoupled DiLoCo 的负责人与核心贡献者是 Arthur Douillard, Keith Rush, Yani Donchev, Zachary Charles, Ayush Dubey, Blake Woodworth, Ionel Gog, Josef Dean, Nova Fallen, Zachary Garrett。运营支持由 Nate Keating 和 Jenny Bishop 完成。

我们还感谢以下人员提供的额外支持与建议：Jeff Dean（杰夫·迪恩）, Marc'Aurelio Ranzato, Raia Hadsell, Arthur Szlam, Edouard Yvinec, Henry Prior, Paul Barham, Michael Isard, Daniel Ramage, Brendan McMahan, Chase Hensel 和 Zoltan Egyed。

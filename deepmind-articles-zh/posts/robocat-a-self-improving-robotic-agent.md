---
title: "RoboCat：一个自我改进的机器人智能体"
title_en: "RoboCat: A self-improving robotic agent"
source: https://deepmind.google/blog/robocat-a-self-improving-robotic-agent/
site: deepmind
date: 2023-06-20
crawled: 2026-09-13
translated: 2026-09-13
---

# RoboCat：一个自我改进的机器人智能体

> 原文：[RoboCat: A self-improving robotic agent](https://deepmind.google/blog/robocat-a-self-improving-robotic-agent/) · Google DeepMind

新的基础智能体学会操作不同的机械臂，仅凭 100 个演示就能解决任务，并能从自我生成的数据中改进。

机器人正迅速成为我们日常生活的一部分，但它们通常只是被编程为把特定任务做好。虽然利用最近的 AI 进展有望带来能在更多方面提供帮助的机器人，但构建通用机器人的进展较慢，部分原因在于收集真实世界训练数据需要大量时间。

[我们的最新论文](https://arxiv.org/abs/2306.11706)介绍了一个面向机器人学的自我改进 AI 智能体 RoboCat，它学会在不同机械臂上执行多种任务，然后自我生成新的训练数据来改进自己的技术。

此前的研究已经探索了如何开发[能够大规模学习多任务的机器人](https://ai.googleblog.com/2022/12/rt-1-robotics-transformer-for-real.html)，以及如何[将语言模型的理解力与辅助机器人的真实世界能力相结合](https://sites.research.google/palm-saycan)。RoboCat 是第一个解决并适应多种任务、并且是在不同的真实机器人上做到这一点的智能体。

RoboCat 的学习速度远快于其他最先进模型。由于它汲取自一个庞大而多样的数据集，它可以仅凭 100 个演示就学会一个新任务。这种能力将有助于加速机器人学研究，因为它减少了对人工监督训练的需求，也是迈向通用机器人的重要一步。

## RoboCat 如何自我改进

RoboCat 基于我们的多模态模型 [Gato](https://deepmind.google/blog/a-generalist-agent/)（西班牙语意为「猫」），后者可以在模拟和物理环境中处理语言、图像和动作。我们将 Gato 的架构与一个大型训练数据集相结合，其中包含各种机械臂解决数百个不同任务的图像与动作序列。

在第一轮训练之后，我们让 RoboCat 进入一组此前未见任务的「自我改进」训练循环。每个新任务的学习遵循五个步骤：

1. 使用由人类操控的机械臂，为一个新任务或新机器人收集 100–1000 个演示。
2. 在这个新任务/机械臂上微调 RoboCat，创建一个特化的派生智能体。
3. 该派生智能体在新任务/机械臂上平均练习 10000 次，生成更多训练数据。
4. 将演示数据和自我生成的数据并入 RoboCat 现有的训练数据集。
5. 在新的训练数据集上训练新版本的 RoboCat。

![一张可视化图，展示 RoboCat 自我改进所采取的步骤列表。](https://lh3.googleusercontent.com/fkvWSJIvd2LNhRFhQDeGcKTNNmsI__N2nU05Y876K0G2rGsYbm3-Mf9oiSy1rWROhygrPgMTGQfjJh1zo1N10-48B9YmRgu515zTNh2QSZmhlTGEE3I=w1440)

RoboCat 的训练循环，其自主生成额外训练数据的能力为其提供了助力。

所有这些训练叠加起来，意味着最新版的 RoboCat 建立在数百万条轨迹的数据集之上，这些轨迹来自真实和模拟的机械臂，包括自我生成的数据。我们使用了四种不同类型的机器人和众多机械臂，收集了代表 RoboCat 将被训练执行的任务的视觉数据。

![三段 RoboCat 的视频：真实、模拟和自我生成形式。第一段视频显示一个真实机械臂拾取齿轮，第二段是模拟机械臂堆叠积木，第三段显示 RoboCat 用机械臂拿起一根黄瓜。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6491af73bf4b23fea70312cf_6490352e82d96885abfec100_z9I3J43_HYsCvaW04QpU3Sfm.gif)

RoboCat 从多样化的训练数据类型和任务中学习：真实机械臂拾取齿轮的视频、模拟机械臂堆叠积木的视频，以及 RoboCat 用机械臂拿起黄瓜的视频。

## 学会操作新的机械臂并解决更复杂的任务

凭借多样化的训练，RoboCat 在几个小时内就学会了操作不同的机械臂。虽然它的训练对象是带双爪夹持器的机械臂，但它能够适应一台更复杂的机械臂——后者带三指夹持器，可控输入是前者的两倍。

![左图显示 RoboCat 学会控制的新机械臂。旁边是 RoboCat 用该机械臂拾取齿轮的视频。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6491af726c741ebb048f88ba_6491a345181cdaa42e86ec2f_Copy2520of2520Fig25204.gif)

**左：** RoboCat 学会控制的新机械臂
**右：** RoboCat 用该机械臂拾取齿轮的视频

在观察了仅需数小时即可收集的 1000 个人工操控演示之后，RoboCat 就能足够灵巧地指挥这台新机械臂，成功拾取齿轮的比率达 86%。在相同数量的演示下，它还能适应解决那些兼具精确性与理解力的任务，例如从碗中取出正确的水果、完成形状配对拼图——这些是执行更复杂控制所必需的。

![两段 RoboCat 完成任务的视频。左侧，机械臂在做儿童拼图，把木块放入形状正确的孔中。右侧，机械臂正从水果碗中拿出一个柠檬。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6491af73441ad51e4b9fc18c_6491a374441ad51e4b945df3_Copy2520of2520Fig2520525.gif)

RoboCat 在 500–1000 个演示后能够适应解决的任务示例。

## 自我改进的通才

RoboCat 拥有一个良性的训练循环：它学到的新任务越多，学习更多新任务的能力就越强。RoboCat 的初始版本在每任务学习 500 个演示后，对此前未见任务的成功率仅为 36%。而在更多样化任务上训练过的最新版 RoboCat，在相同任务上的成功率翻了一倍多。

![一张条形图，比较 RoboCat 在 500 个演示后完成新任务的成功率。初始版 RoboCat 的平均成功率为 36%。最终版 RoboCat 的平均成功率为 74%。](https://lh3.googleusercontent.com/Okfaiq6fpxBb8wC7k_jyelj_3SID_e_rWrLmrrUsT8rsbSjyU78xKi5vRnfQcApxS7hXmK0uu5IaFi6qVkI98DouyKWpxMUF6v1DApRGDUD-DfYSCw=w1440)

初始版 RoboCat（一轮训练）与最终版（包含自我改进的大规模多样化训练）在均在 500 个此前未见任务演示上微调之后的巨大性能差异。

这些提升源于 RoboCat 日益丰富的经验广度，就像人们随着在某一领域学习的深入而发展出更多样的技能一样。RoboCat 独立学习技能并快速自我改进的能力——尤其是应用于不同机器人设备时——将有助于为新一代更有用、更通用的机器人智能体铺平道路。

[在 arXiv 上阅读我们的论文](https://arxiv.org/abs/2306.11706)

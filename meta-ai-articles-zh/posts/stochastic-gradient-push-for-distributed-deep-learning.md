---
title: "用随机梯度推送（Stochastic Gradient Push）加速分布式训练"
title_en: "Accelerating distributed training with Stochastic Gradient Push"
date: 2019-06-06
source: https://ai.facebook.com/blog/stochastic-gradient-push-for-distributed-deep-learning
crawled: 2026-09-22
translated: 2026-09-22
---

# 用随机梯度推送（Stochastic Gradient Push）加速分布式训练

> 原文：[Accelerating distributed training with Stochastic Gradient Push](https://ai.facebook.com/blog/stochastic-gradient-push-for-distributed-deep-learning) · Meta AI（Wayback 存档）

2019 年 6 月 6 日

**这项研究是什么：** 一种名为随机梯度推送（Stochastic Gradient Push，SGP）的分布式优化方法的新变体，用于利用大型 GPU 集群在大规模数据集上训练深度神经网络（DNN）。该方法对在大型集群上训练时常见的问题具有韧性，包括某些节点比其他节点运行慢或某些通信链路不可靠。我们的方法使分布式算法在通信受限的环境中运行显著快于使用 AllReduce 同步的并行随机梯度下降（SGD）。在这种环境中，它还能用更少时间训练出比 SGD 更好的模型。例如，SGP 的一个变体训练出的模型，其最终 top-1 验证准确率比标准并行 SGD 高一个百分点，而时间只有一半。对于想要复现或在此基础上继续构建的研究者，我们已在此处公开我们的代码。

**工作原理：** 我们提出并分析了一种名为 Overlap SGP 的 SGP 变体，它把通信与计算重叠以隐藏通信开销。SGP 是一种把并行 SGD 与用于近似分布式平均的 push-sum 操作相融合的算法。用于训练 DNN 的分布式数据并行方法旨在利用并行计算资源并发处理多个数据点来加速训练。这涉及一些同步所有计算节点模型所需的通信开销。标准并行 SGD 使用 AllReduce 操作进行同步，但 AllReduce 是阻塞操作，意味着所有节点必须等待操作完成才能进行下一步，因此一个慢节点或一条慢通信链路就会拖累整个系统。相比之下，push-sum 是一种基于 gossip 的消息传递算法，可以非阻塞、异步的方式运行。在 gossip 协议中，每个节点与系统中一小部分其他节点收发消息，信息在网络中逐渐扩散。使用 push-sum，节点无需等待任何操作完成即可进入算法的下一步。SGP 通过在每个节点上把一次本地 SGD 更新与一次 push-sum 迭代交替执行得到。SGP（以及 Overlap SGP）收敛到光滑非凸函数的驻点。在训练 DNN 场景中被探索的现有基于 gossip 的方法被限制为使用对称通信（又称 push-pull）。例如，如果节点 i 发送给节点 j，那么 i 在继续之前也必须从 j 接收。这本质上需要死锁避免和更多同步，使这些方法更慢、对掉队者更敏感。我们的方法则使用定向消息传递（仅推送）。这使我们可以使用可能是定向（非对称）、稀疏且随时间变化的通用通信拓扑。为了隐藏通信开销，我们可以把梯度计算与通信重叠。节点在每次更新后向其出邻居发送消息（非阻塞）。它们也可以随时接收传入消息，并在下一次更新前将其并入。异步算法通常运行更快，但可能引入妨碍性能的额外误差，从而带来权衡。我们可以在 SGP 中显式控制异步程度：如果某节点在一定迭代次数后尚未收到某个入邻居的消息，那么它会等待收到消息后再继续。我们在多种计算基础设施上研究这些方法，并在图像分类和神经机器翻译任务上提供评估。

**为什么重要：** 深度学习很大程度上是一个实证领域，SGD 及相关一阶方法一直是训练神经网络的主力。随着研究者继续探索越来越大的模型，通信开销仍将是分布式训练的瓶颈。我们的新方法有助于用异步分布式数据并行算法加速 DNN 模型训练。能够更快地训练模型，将使更频繁地重训模型、更快速地探索新模型成为可能，进而提升构建预测更准确、更相关的模型的潜力。通过这项研究和代码公开发布，我们希望 AI 社区能在此基础上继续构建，最终更快地推进科学。

**阅读完整论文：** Stochastic Gradient Push for Distributed Deep Learning。获取本工作所用代码。

**作者**
Michael Babbat，研究科学家
Nicolas Ballas，研究科学家

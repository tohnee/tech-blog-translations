---
title: "AlphaQubit 攻克量子计算最大的挑战之一"
title_en: "AlphaQubit tackles one of quantum computing’s biggest challenges"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphaqubit-quantum-error-correction/
site: google-blog
date: 2024-11-20
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaQubit 攻克量子计算最大的挑战之一

> 原文：[AlphaQubit tackles one of quantum computing’s biggest challenges](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphaqubit-quantum-error-correction/) · Google

量子计算机有潜力彻底改变药物发现、材料设计和基础物理学——前提是，我们能让它们可靠地运转。

某些问题，传统计算机需要数十亿年才能解决，量子计算机却只需几个小时。然而，这些新型处理器比传统处理器更容易受到噪声影响。如果我们想让量子计算机更可靠——尤其是在大规模下——我们就需要准确地识别并纠正这些误差。

在[今天发表于《自然》（Nature）的论文](https://www.nature.com/articles/s41586-024-08148-8)中，我们介绍了 AlphaQubit——一个基于 AI 的解码器，它能以最先进的准确率识别量子计算误差。这项合作汇集了 Google DeepMind 的机器学习专业知识和 Google Quantum AI 的量子纠错专长，以加速构建可靠量子计算机的进程。

准确地识别误差，是让量子计算机能够大规模执行长时运算的关键一步，它将为科学突破和众多新的探索领域敞开大门。

## 纠正量子计算误差

量子计算机利用最小尺度上物质所独有的特性——例如叠加（superposition）和纠缠（entanglement）——以远少于经典计算机的步骤来解决某些类型的复杂问题。这项技术依赖量子比特（qubit），它能借助量子干涉在庞大的可能性集合中进行筛选，最终找到答案。

量子比特的自然量子态非常脆弱，可能被各种因素干扰：硬件中的微观缺陷、热量、振动、电磁干扰，甚至无处不在的宇宙射线。

量子纠错提供了一条前进之路，其方法是基于冗余：把多个量子比特组合成一个逻辑量子比特（logical qubit），并定期对它执行一致性检查。解码器（decoder）利用这些一致性检查来识别逻辑量子比特中的误差，从而对其加以纠正，以此保全量子信息。

这里我们示意了在边长为 3（码距，code distance）的量子比特网格中，九个物理量子比特（灰色小圆圈）如何构成一个逻辑量子比特。在每个时间步，另有 8 个量子比特执行一致性检查（方形与半圆形区域，失败时显示为蓝色和品红色，否则为灰色），其结果输入神经网络解码器（AlphaQubit）。在实验结束时，AlphaQubit 判断发生了哪些错误。

## 打造基于神经网络的解码竞争者

AlphaQubit 是一个基于神经网络的解码器，它借鉴了 [Transformer](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/)——一种在 Google 开发的深度学习架构，支撑着今天的许多大语言模型。它以一致性检查作为输入，任务是正确预测逻辑量子比特在实验结束时被测量时，是否已从其制备状态发生翻转。

我们首先训练模型去解码 [Sycamore 量子处理器](https://research.google/blog/suppressing-quantum-errors-by-scaling-a-surface-code-logical-qubit/)中一组 49 个量子比特的数据——它是量子计算机的核心计算单元。为了让 AlphaQubit 学会一般性的解码问题，我们使用量子模拟器在各种设置和误差水平下生成了数亿个样本。然后，我们用一个特定 Sycamore 处理器提供的数千个实验样本对 AlphaQubit 针对特定解码任务进行微调。

在新的 Sycamore 数据上测试时，与以往领先的解码器相比，AlphaQubit 创立了准确率的新标准。在最大规模的 Sycamore 实验中，AlphaQubit 比张量网络方法[（准确度极高但速度慢得不切实际）](https://www.nature.com/articles/s41586-022-05434-1)少犯 6% 的错误。AlphaQubit 还比[关联匹配（correlated matching）](https://arxiv.org/abs/1310.0863)——一种准确且速度快到可以扩展的解码器——少犯 30% 的错误。

小型和大型 Sycamore 实验的解码准确率（码距 3 = 17 个物理量子比特，码距 5 = 49 个物理量子比特）。AlphaQubit 比张量网络（TN，一种预计无法在大型实验中扩展的方法）和关联匹配（一种准确且具备扩展所需速度的解码器）都更准确。

![折线图，比较三种量子解码器随码距变化的准确率，AlphaQubit 在全程保持最高准确率](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Figure_2.gif)

## 让 AlphaQubit 面向未来的系统扩展

我们预计量子计算机将超越当今的水平。为了考察 AlphaQubit 在误差水平更低、规模更大的设备上的适应能力，我们使用了最多 241 个量子比特的模拟量子系统的数据来训练它，因为这超出了 Sycamore 平台现有的规模。

再一次，AlphaQubit 的表现超过了领先的算法解码器，这表明它在未来同样能适用于中等规模的量子设备。

不同扩展/模拟实验的解码准确率，从码距 3（17 个量子比特）到码距 11（241 个量子比特）。张量网络解码器未出现在本图中，因为它在大码距下运行速度过慢。随着码距增大（即使用更多物理量子比特），另外两个解码器的准确率都会提高。在每个码距下，AlphaQubit 都比关联匹配更准确。

![折线图，显示两种解码器的准确率随码距提高，在更大规模下接近 100%，其中 AlphaQubit 最佳](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Figure_3.gif)

我们的系统还展示了一些高级特性，例如对输入和输出接受并报告置信度水平的能力。这些信息丰富的接口可以进一步提升量子处理器的性能。

当我们在包含最多 25 轮纠错的样本上训练 AlphaQubit 后，它在最多 100,000 轮的模拟实验中仍保持了良好性能，这展示了它向训练数据之外的场景泛化的能力。

## 迈向实用的量子计算

AlphaQubit 代表了在量子纠错中运用机器学习的一个重要里程碑。但我们在速度和可扩展性方面仍面临重大挑战。

例如，在快速的超导量子处理器中，每一次一致性检查每秒要被测量一百万次。虽然 AlphaQubit 在准确识别误差方面表现出色，但它的速度还不足以在超导处理器中实时纠正误差。随着量子计算向商业相关应用所需的、可能多达数百万个量子比特的规模发展，我们还需要找到训练基于 AI 的解码器时数据效率更高的方法。

我们的团队正在结合机器学习与量子纠错领域的开创性进展来克服这些挑战——为能够应对世界上一些最复杂问题的可靠量子计算机铺平道路。

[*欢迎阅读我们发表在《自然》上的论文*](https://www.nature.com/articles/s41586-024-08148-8)*。*

---
title: "认识 Willow：我们最先进的量子芯片"
title_en: "Meet Willow, our state-of-the-art quantum chip"
source: https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/
site: google-blog
date: 2024-12-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 认识 Willow：我们最先进的量子芯片

> 原文：[Meet Willow, our state-of-the-art quantum chip](https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/) · Google

*最后更新：2025 年 6 月 12 日*

今天，我很高兴地宣布 Willow 问世——我们最新的量子芯片。Willow 在多项指标上都达到了业界最先进的水平，并带来了两项重大成就。

- 第一，Willow 在我们使用*更多*量子比特进行扩展时，能够实现误差的指数级降低。这攻克了量子纠错领域的一个关键挑战，该领域为解决这一问题已奋斗了近 30 年。
- 第二，Willow 在不到五分钟的时间里完成了一项标准基准计算，而当今[最快的超级计算机](https://www.olcf.ornl.gov/frontier/)之一需要 10 的 25 次方年（10 septillion，即 10²⁵ 年）才能完成——这个数字远远超过了宇宙的年龄。

Willow 芯片是一段始于十多年前的旅程中的重要一步。当我在 2012 年创立 Google Quantum AI 时，愿景是打造一台有用的大规模量子计算机，利用量子力学——就我们今天所知，它是自然界的"操作系统"——通过推进科学发现、开发[有用的应用](https://quantumai.google/applications)以及应对社会上一些最重大的挑战来造福社会。作为 Google Research 的一部分，我们团队制定了长期[路线图](https://quantumai.google/roadmap)，而 Willow 使我们在通往商业相关应用的道路上大幅前进。

## 指数级量子纠错——低于阈值（below threshold）！

误差是量子计算面临的最大挑战之一。量子比特是量子计算机的计算单元，它们倾向于与环境快速交换信息，使得保护完成计算所需的信息变得非常困难。通常，你使用的量子比特越多，出现的误差就越多，系统就会退化为经典系统。

今天我们在《自然》（[Nature](https://www.nature.com/articles/s41586-024-08449-y)）上发表的研究结果表明：[**在 Willow 中，我们使用的量子比特越多，就越能***减少***误差，系统也变得越发"量子"**](https://research.google/blog/making-quantum-error-correction-work/)。我们测试了越来越大的物理量子比特阵列，从 3x3 的编码量子比特网格扩展到 5x5，再到 7x7——每一次，凭借量子纠错方面的最新进展，我们都能将错误率减半。换句话说，我们实现了错误率的指数级下降。这一历史性成就在该领域被称为"低于阈值（below threshold）"——即在增加量子比特数量的同时把误差压低。你必须展示出低于阈值的表现，才能证明在纠错上取得了真正的进步；而自 Peter Shor 于 1995 年提出[量子纠错](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.52.R2493)以来，这一直是一个悬而未决的挑战。

这项成果还包含其他多项科学上的"首次"。例如，它也是超导量子系统上实时纠错的首批令人信服的实例之一——这对任何有用的计算都至关重要，因为如果你不能足够快地纠正错误，它们会在计算完成之前将其毁掉。同时，这也是一次"超越盈亏平衡（beyond breakeven）"的演示：我们的量子比特阵列拥有比单个物理量子比特更长的寿命，这是纠错正在整体改善系统的一个无法伪造的标志。

作为首个低于阈值的系统，这是迄今构建的最具说服力的可扩展逻辑量子比特原型。它有力地表明，有用的、超大规模的量子计算机确实可以被建造出来。Willow 让我们更接近于运行那些传统计算机无法复现的、实用的、与商业相关的算法。

## 当今最快超级计算机需要 10 的 25 次方年

作为衡量 Willow 性能的标尺，我们使用了[随机线路采样（random circuit sampling，RCS）基准](https://research.google/blog/validating-random-circuit-sampling-as-a-benchmark-for-measuring-quantum-progress/)。RCS 由我们团队开创，如今已被广泛用作该领域的标准，它是当前量子计算机上可以执行的、经典计算最难应对的基准。你可以把它视为量子计算的入门门槛——它检验的是量子计算机是否在做经典计算机做不到的事情。任何构建量子计算机的团队都应该首先检验它能否在 RCS 上击败经典计算机；否则，就有充分理由怀疑它能否应对更复杂的量子任务。我们一直在使用这一基准来评估芯片代际之间的进展——我们在 [2019 年 10 月](https://blog.google/technology/ai/what-our-quantum-computing-milestone-means/)报告过 Sycamore 的结果，最近又在 [2024 年 10 月](https://www.nature.com/articles/s41586-024-07998-6)再次报告。

Willow 在这一基准上的表现令人震惊：它用不到五分钟完成了一项计算，而当今[最快的超级计算机](https://www.olcf.ornl.gov/frontier/)之一需要 10²⁵ 年，也就是 10 的 25 次方年。如果你想把它写出来，那是 10,000,000,000,000,000,000,000,000 年。这个令人难以置信的数字超出了物理学中已知的时间尺度，也远远超过宇宙的年龄。它为"量子计算发生在许多平行宇宙中"这一观点提供了佐证，与我们生活在多元宇宙中的想法相一致——这是 David Deutsch 最早做出的[预言](https://en.wikipedia.org/wiki/The_Fabric_of_Reality)。

如下图所示，Willow 的这些最新结果是我们迄今为止最好的成绩，但我们会继续取得进展。

计算成本在很大程度上受可用内存的影响。因此，我们的估算考虑了一系列情景，从内存无限的理想情形（▲）到更现实的、在 GPU 上高度可并行化的实现（⬤）。

![一张比较不同量子计算平台在随机线路采样（RCS）任务上性能的图表。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image_8_dUczXnV.width-1200.format-webp.webp)

我们对 Willow 如何超越世界上最强大的经典超级计算机之一 [Frontier](https://www.olcf.ornl.gov/frontier/) 的评估基于保守的假设。例如，我们假设可以完全访问二级存储（即硬盘）且没有任何带宽开销——这对 Frontier 来说是一个慷慨且不切实际的宽限。当然，正如我们在 2019 年宣布首次[超经典计算（beyond-classical computation）](https://blog.google/technology/ai/what-our-quantum-computing-milestone-means/)之后所发生的那样，我们预计经典计算机会在这一基准上持续改进，但迅速扩大的差距表明，量子处理器正在以双指数速率拉开距离，并且随着我们继续扩展规模，它们将持续大幅超越经典计算机。

## 最先进的性能

Willow 是在我们位于圣巴巴拉（Santa Barbara）的新建顶尖制造工厂生产的——全世界从头为这一目的建造的设施屈指可数。在设计和制造量子芯片时，系统工程是关键：芯片的所有组件，例如单量子比特门和双量子比特门、量子比特重置和读出，都必须同时得到良好的工程化并集成在一起。如果任何一个组件落后，或者两个组件无法良好协同，就会拖累整个系统的性能。因此，最大化系统性能指导着我们流程的方方面面，从芯片架构和制造到门开发和校准。我们所报告的成就是对量子计算系统的整体评估，而不是每次只看一个因素。

我们注重质量，而不仅仅是数量——因为如果量子比特的质量不够高，仅仅生产更多的量子比特也无济于事。Willow 拥有 105 个量子比特，在上述两项系统基准（量子纠错和随机线路采样）上都实现了同类最佳的性能。这类算法基准是衡量芯片整体性能的最佳方式。其他更具体的性能指标同样重要；例如，我们的 T1 时间——衡量量子比特能将激发态（关键的量子计算资源）保持多久的指标——现在已接近 100 µs（微秒）。与上一代芯片相比，这是约 5 倍的显著提升。如果你想评估量子硬件并在不同平台之间进行比较，这里有一份关键规格表：

Willow 在多项指标上的表现。

![一张标题为"Willow System Metrics"的表格图，列中展示了量子比特数量（105）和平均连接度（3.47）等细节](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/KW_Fig3.width-1200.format-webp.webp)

## Willow 之后，下一步是什么

该领域的下一个挑战，是在当今的量子芯片上展示首次与真实世界应用相关的"有用的超经典"计算。我们乐观地认为，Willow 这一代芯片能帮助我们实现这一目标。迄今为止，已有两类彼此独立的实验。一方面，我们运行了 RCS 基准，它衡量的是与经典计算机相比的性能，但还没有已知的真实世界应用。另一方面，我们做了在科学上有趣的量子系统模拟，这些模拟带来了新的科学发现，但仍在经典计算机的能力范围之内。我们的目标是同时做到这两点——踏入那些既超出经典计算机能力范围、**又**对真实世界和商业相关问题有用的算法领域。

随机线路采样（RCS）虽然对经典计算机而言极具挑战性，但尚未展示出实际的商业应用。

![一张题为"Random Circuit Sampling (RCS): in context"的图示图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/KW_Fig2.width-1200.format-webp.webp)

我们邀请研究人员、工程师和开发者加入这段旅程：了解我们的[开源软件](https://quantumai.google/software)和教育资源，包括我们在 Coursera 上的[新课程](https://coursera.org/learn/quantum-error-correction)，开发者可以在那里学习量子纠错的要点，并帮助我们创建能够解决未来问题的算法。

![一张写着"Our quantum computing roadmap"的图示卡片，以及一条展示从"Beyond classical"到"Large error-corrected quantum computer"共 6 个里程碑的时间线](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/KW_Fig4.width-1200.format-webp.webp)

我的同事有时会问我，为什么我离开了蓬勃发展的 AI 领域，转而专注于量子计算。我的回答是：两者都将被证明是我们这个时代最具变革性的技术，而先进的 AI 将显著受益于量子计算。正因如此，我把我们的实验室命名为 Quantum AI。量子算法拥有根本性的标度律（scaling law）优势，正如我们在 RCS 中所看到的。对于许多对 AI 至关重要的基础计算任务，也存在类似的标度优势。因此，量子计算对于收集经典机器无法获取的训练数据、训练和优化某些学习架构，以及对量子效应至关重要的系统建模来说，将是不可或缺的。这包括帮助我们发现新药、为电动汽车设计更高效的电池，以及加速聚变和新型能源替代方案的进展。这些未来改变游戏规则的应用中，有许多在经典计算机上是不可行的；它们正等待着被量子计算解锁。

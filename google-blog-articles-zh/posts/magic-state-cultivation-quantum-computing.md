---
title: "见证魔力：Google 攻克量子计算的一大瓶颈"
title_en: "Bringing the magic: Google breaks open a bottleneck in quantum computing"
source: https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/
site: google-blog
date: 2026-10-15
crawled: 2026-10-16
translated: 2026-10-16
---

# 见证魔力：Google 攻克量子计算的一大瓶颈

> 原文：[Bringing the magic: Google breaks open a bottleneck in quantum computing](https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/) · Google

Google Quantum AI 已经通过实际演示打开了量子计算的一个关键瓶颈：我们证明了「魔态培育」（magic state cultivation）可以在我们的 Willow 处理器上实际运行，与不使用该技术相比，错误降低了约 40 倍。这项今日发表于 [Science](https://www.science.org/doi/10.1126/science.aee7961) 的突破，是量子计算扩展到实用规模的关键一步。

## 「魔态」瓶颈

自 2004 年起——远在量子计算成为一项实际的工程事业之前——研究人员就预见到了一个特别棘手的瓶颈。

要实现「通用」量子计算并执行有用的程序，你需要能够运行（并对一组特定的量子操作进行[纠错](https://research.google/blog/making-quantum-error-correction-work/)）。为此，可以先创建所谓的「魔态」（magic states）——之所以如此命名，是因为它们能帮助你构造出超越经典计算所需的操作。

但问题在于：创建高质量、经过纠错的魔态需要消耗极其庞大的资源。一些估算表明，量子计算机的全部算力中多达 95% 可能都要投入到制造魔态上，留给实际计算的空间所剩无几。另一个额外的挑战是，魔态一经使用便无法重复利用，这使得魔态成为一种稀缺资源。

因此，20 年来，研究人员一直在一点点削减这种「魔法」的成本，把它降得越来越低。

## 我们如何实现这一突破

2024 年，Google Quantum AI 的研究人员 Craig Gidney、Noah Shutty 和 Cody Jones 从文献中汲取了一个想法，加以改进，发展出我们如今所说的「魔态培育」。他们的方法有望带来特别大幅度的成本降低。其思路是：培育过程会像一个过滤器那样运作——你把一个含噪声的态注入量子芯片上的一小块区域，然后运行一系列高度协调的测量来检查错误、剔除所有有缺陷的尝试。Craig 和团队展示了这如何让你培育出一个极其纯净、低错误的量子态，并且能同时把它适配转换成一种更大、更有用的编码。

在纸面上，这一切看起来很美好。如果我们能让这个想法真正在我们的量子硬件上运行，就可以大幅缩小实用任务所需的量子计算机的规模。

而在实践中——这与开发许多新技术时的情形如出一辙——它需要一整套的技术创新与工程攻关。

仅举一例：在最初测试培育协议时，Google Quantum AI 研究科学家 Emma Rosenfeld 看到的数据似乎违背了物理定律。经过数月的困惑、仿真、与同事的讨论以及一致性核查，她发现这源自团队惯用测量技术中一个错误的假设。具体来说，实验室中由电气设备漂移和温度变化引起的某类噪声，干扰了基准测试的有效性。解决方案要求我们在理论和工程两条路线上都做出调整：团队为系统增加了额外控制来降低该噪声的影响，还发明了一种全新的基准测试技术，通过让「培育」充当测量自身的工具，从更根本的层面解决了这个问题。

凭借这项以及更多算法创新和工程方案，我们在量子计量学领域确立了新的最先进水平。在 Google Quantum AI 的 Willow 处理器上，我们的协议相对于未培育的态实现了高达 40 倍的错误降低，并得到了逻辑保真度达 99.99% 的创纪录 T 态。

这项工作现已发表于 [Science](https://www.science.org/doi/10.1126/science.aee7961)，是针对量子计算最严峻的资源瓶颈之一的首个实用解决方案演示。它在真实硬件上证明：我们能够高效地创建这些关键的魔态。

## 我们的发现与未来

我们还迈出了第一步，证明 Craig 等人的理论与我们的量子计算架构相兼容。我们学会了如何在「颜色码」（color codes，一种较新的量子纠错类型，非常适合培育）与「表面码」（surface codes，另一种更为成熟的方法）之间成功切换，将量子态从距离为 3 的颜色码嫁接到距离为 5 的表面码。这一嫁接协议最初在 2024 年的理论论文中提出，如今在实践中证明：经过纯化的态能够在我们的硬件中存活并顺利转移。

当然，要让魔态培育对实用量子计算真正可行，我们仍需要在更大规模上进行演示，大量技术挑战依然存在。但这一成果把一个关键的理论想法变成了经过实验验证的现实。它让我们离 [Google Quantum AI](http://quantumai.google/) 的目标更近了一步：建造一台有用的、经过纠错的量子计算机，去解决那些原本无解的问题。

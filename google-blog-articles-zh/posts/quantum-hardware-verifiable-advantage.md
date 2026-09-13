---
title: "我们的量子硬件：可验证量子优势的引擎"
title_en: "Our quantum hardware: the engine for verifiable quantum advantage"
source: https://blog.google/innovation-and-ai/technology/research/quantum-hardware-verifiable-advantage/
site: google-blog
date: 2025-10-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们的量子硬件：可验证量子优势的引擎

> 原文：[Our quantum hardware: the engine for verifiable quantum advantage](https://blog.google/innovation-and-ai/technology/research/quantum-hardware-verifiable-advantage/) · Google

今天，依托我们的高性能量子芯片 [Willow](https://blog.google/technology/research/google-willow-quantum-chip/)，我们实现了[有史以来首次可验证量子优势的演示](https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/)。这一里程碑是实现实用量子计算道路上的关键一步，而这一成就的达成，离不开我们量子硬件系统在精度与速度上的精心设计。

### Willow：打造一流性能

Willow 是我们最先进的量子芯片，由超导量子电路构成。这一研究领域始于 1985 年对宏观量子效应的开创性发现——这一成就让 John Clarke、Michel Devoret 与 John Martinis 荣获 2025 年诺贝尔物理学奖。借助这些电路，超导量子比特作为宏观的"人造原子"运行。过去 40 年间，在成熟的集成电路制造工艺以及学术界与产业界的持续研究推动下，这些量子比特展现出性能与可扩展性的出色平衡，使其成为建造容错量子计算机的领先平台。

在这一领先平台的基础上，我们着力在一个复杂而实际的应用中展示其威力，让量子计算更接近为人们带来现实益处。为了揭示量子系统（例如分子）内部动力学的隐藏信息，我们成功执行了 Quantum Echoes 算法。该算法依赖于在量子计算机中逆转量子数据流的演化，这反过来对 Willow 在系统规模上的性能提出了极高要求。它需要以大量量子门和高频次的量子测量来运行 Willow 芯片——这两大要素是从背景噪声中提炼有用信号的关键。

得益于发布后的持续改进，当前一代 Willow 芯片在大规模运行下展现出一流的性能。在其全部 105 个量子比特阵列上，单比特门保真度达 99.97%，纠缠门保真度达 99.88%，读取保真度达 99.5%，同时保持在数十至数百纳秒的无与伦比的速度。

![一块深色矩形微芯片静置于反射式晶圆衬底上，衬底上标有 "Quantum AI" 和 "Willow" 字样，并呈现精细蚀刻的线路与图案。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumWIllow_Chip.width-1200.format-webp.webp)

这些高精度量子门使我们得以执行高度复杂的 Quantum Echoes 算法——其中涉及大规模的量子干涉与纠缠。它切实地将我们的成果推入了经典计算机能力所不及的领域。

此外，与这种精度相匹配的，是我们的系统能够在短短几十秒内完成数百万次 Quantum Echoes 测量。这一速度在整个项目期间实现了惊人的 1 万亿次测量——这占了*所有*量子计算机上有史以来执行的*全部*测量中的相当大一部分。这让我们的工作稳居量子计算史上最复杂实验之列。

![量子计算机低温恒温器结构复杂的多层金色与黄铜器件，由数百根密集的黑色波纹同轴电缆连接。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumComputer.width-1200.format-webp.webp)

### 通往容错之路：我们的战略路线图

自创立以来，我们始终全力投入 Google Quantum AI 路线图，朝着建造容错量子计算机的目标迈进。我们已经以头两个里程碑的完成证明了进展：2019 年的超越经典计算，以及 2023 年的量子纠错原型。随着 Willow 于 2024 年发布，我们沿着路线图进一步推进，展示了低于阈值的量子纠错，迈向里程碑 3。

![量子计算路线图信息图时间线，展示从物理量子芯片到大型纠错量子计算机的六个里程碑。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumWillow_Roadmap.width-1200.format-webp.webp)

今天的可验证量子优势演示，标志着又一个关键性前进。它不仅彰显了我们在探索实用量子应用方面的持续努力，也增强了我们使用超导量子比特进行大规模、复杂量子计算的信心。

在我们迈向下一个里程碑——长寿命逻辑量子比特——的进程中，我们深知前方挑战重重。要实现最终目标，系统性能与规模需要数个数量级的提升，数以百万计的元器件有待开发与成熟。尽管障碍重重，我们依然坚定地走好这条路。

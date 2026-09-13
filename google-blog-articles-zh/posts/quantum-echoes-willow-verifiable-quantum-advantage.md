---
title: "我们的 Quantum Echoes 算法是量子计算迈向实际应用的一大步"
title_en: "Our Quantum Echoes algorithm is a big step toward real-world applications for quantum computing"
source: https://blog.google/innovation-and-ai/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/
site: google-blog
date: 2025-10-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们的 Quantum Echoes 算法是量子计算迈向实际应用的一大步

> 原文：[Our Quantum Echoes algorithm is a big step toward real-world applications for quantum computing](https://blog.google/innovation-and-ai/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/) · Google

**编者注：***今天，我们宣布一项研究成果，它有史以来第一次表明，量子计算机能够在硬件上成功运行一个可验证的算法，甚至超越最快的经典超级计算机（快 13,000 倍）。它可以计算分子的结构，并为实际应用铺平道路。今天的进展建立在数十年的工作以及六年的重大突破之上。早在 2019 年，我们就*[ *演示过* ](https://blog.google/technology/ai/what-our-quantum-computing-milestone-means/)*量子计算机可以解决一个最快的经典超级计算机需要数千年才能解决的问题。随后在去年底（2024 年），我们全新的*[ *Willow 量子芯片* ](https://blog.google/technology/research/google-willow-quantum-chip/)*展示了如何大幅抑制错误，解决了困扰科学家近 30 年的一个重大难题。今天的突破让我们离能够推动医学和材料科学等领域重大发现的量子计算机更近了一步。*

想象一下，你正在寻找沉没在海底的一艘失事船只。声纳技术可能会给你一个模糊的轮廓，并告诉你："下面有一艘沉船。"但如果你不仅能找到这艘船，还能读出船体上的铭牌呢？

这正是我们刚刚用 Willow 量子芯片实现的前所未有的精度。今天，我们宣布一项重大的算法突破，它标志着向首个实际应用迈出的重要一步。这项成果刚刚[发表于《自然》（Nature）](https://www.nature.com/articles/s41586-025-09526-6)：我们运行乱序时间关联器（OTOC）算法——我们称之为 Quantum Echoes——演示了[史上首个可验证量子优势（verifiable quantum advantage）](https://research.google/blog/a-verifiable-quantum-advantage/)。

![Sundar Pichai 站在量子计算机旁的照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/QuantumSundar_Inline.width-1200.format-webp.webp)

Quantum Echoes 可用于探究自然界中各类系统的结构——从分子到磁体再到黑洞。我们已经证明，它在 Willow 上的运行速度，比世界上最快超级计算机之一上的最佳经典算法快 13,000 倍。

在另一项原理验证实验[《Quantum computation of molecular geometry via many-body nuclear spin echoes》](https://quantumai.google/static/site-assets/downloads/quantum-computation-molecular-geometry-via-nuclear-spin-echoes.pdf)（将于今天晚些时候发布在 arXiv 上）中，我们展示了我们的新技术——一把"分子标尺"——如何测量比现有方法更长的距离，利用核磁共振（NMR）数据获得更多关于化学结构的信息。

### Quantum Echoes 算法：可验证量子优势

这是历史上首次有量子计算机成功运行超越超级计算机能力的可验证算法。量子可验证性意味着该结果可以在我们的量子计算机上——或任何同级别设备上——重复运行并得到相同答案，从而确认结果。这种可重复的超经典计算是可扩展验证的基础，让量子计算机距离成为实用工具更近一步。

我们的新技术就像一种高度先进的回声。我们向量子系统（Willow 芯片上的量子比特）发送一个精心构造的信号，扰动其中一个量子比特，然后精确地逆转信号的演化，倾听返回的"回声"。

这种量子回声的特殊之处在于，它会因相长干涉而被放大——这是一种量子波叠加后变强的现象。这使得我们的测量极其灵敏。

这张图展示了在我们 105 量子比特阵列上创建量子回声的四步过程：正向运行操作、扰动一个量子比特、逆向运行操作，然后测量结果。信号的重叠揭示了扰动如何在 Willow 芯片上传播。

Quantum Echoes 算法的这一实现，得益于 Willow 芯片在[量子硬件](https://blog.google/technology/research/quantum-hardware-verifiable-advantage/)方面的进展。去年，Willow 通过我们的随机线路采样（Random Circuit Sampling）基准测试证明了自己的实力，这是一项旨在测量最大量子态复杂度的测试。Quantum Echoes 算法则代表了一类全新的挑战，因为它模拟的是一个物理实验。这意味着该算法不仅测试复杂度，还测试最终计算的精度。正因如此，我们称之为"量子可验证"——结果可以由另一台类似质量的量子计算机进行交叉基准测试并加以验证。要同时做到精度与复杂度，硬件必须具备两个关键特性：极低的错误率和高速运行能力。

![一只戴着白手套的手拿着一个方形电子传感器或微芯片。图片上叠加了白色的 Willow 标志和一个风格化的几何图形。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WillowChip_4k_Render_02.width-1200.format-webp.webp)

### 迈向实际应用

量子计算机将在模拟量子力学现象方面发挥重要作用，例如原子与粒子的相互作用以及分子的结构（或形状）。科学家用来理解化学结构的工具之一是核磁共振（NMR），它正是 MRI 技术背后的科学。NMR 如同一台分子显微镜，强大到足以让我们看到原子的相对位置，从而帮助我们理解分子的结构。对分子形状与动力学的建模是化学、生物学和材料科学的基础，而帮助我们在这方面做得更好的进展，支撑着从生物技术到太阳能再到核聚变等领域的进步。

在与加州大学伯克利分校（The University of California, Berkeley）合作进行的一项[原理验证实验](https://quantumai.google/static/site-assets/downloads/quantum-computation-molecular-geometry-via-nuclear-spin-echoes.pdf)中，我们在 Willow 芯片上运行 Quantum Echoes 算法来研究两个分子——一个有 15 个原子，另一个有 28 个原子——以验证这一方法。量子计算机上的结果与传统 NMR 的结果吻合，并且揭示了通常无法从 NMR 中获得的信息，这是对我们方法的一次关键验证。

正如望远镜和显微镜开辟了前所未见的新世界，这项实验是迈向"量子镜"（quantum-scope）的一步——一种能够测量以往不可观测的自然现象的仪器。量子计算增强的 NMR 有望成为药物发现中的强大工具，帮助确定候选药物如何与靶点结合；也可用于材料科学，表征聚合物、电池组件，甚至构成我们量子比特（qubit）的材料等新材料的分子结构。

### 接下来

我们用 Quantum Echoes 算法对史上首个可验证量子优势的演示，标志着向量子计算首个实际应用迈出的重要一步。

随着我们向完整规模的量子纠错计算机扩展，我们预计会有更多这样有用的实际应用被发明出来。现在，我们的重点是在[量子硬件路线图](https://quantumai.google/roadmap)上实现里程碑 3——长寿命逻辑量子比特。

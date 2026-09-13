---
title: "打造超导与中性原子量子计算机"
title_en: "Building superconducting and neutral atom quantum computers"
source: https://blog.google/innovation-and-ai/technology/research/neutral-atom-quantum-computers/
site: google-blog
date: 2026-03-24
crawled: 2026-09-13
translated: 2026-09-13
---

# 打造超导与中性原子量子计算机

> 原文：[Building superconducting and neutral atom quantum computers](https://blog.google/innovation-and-ai/technology/research/neutral-atom-quantum-computers/) · Google

在 Google Quantum AI，我们的[使命](https://quantumai.google/#mission)始终清晰：为那些别无他法可解的问题打造量子计算。十多年来，我们在超导量子比特（qubit）的研发上开拓前行，实现了[超经典计算性能](https://blog.google/innovation-and-ai/technology/ai/what-our-quantum-computing-milestone-means/)、[量子纠错](https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/)和[可验证的量子计算优越性](https://blog.google/innovation-and-ai/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/)等曾看似尚需数十年的里程碑。如今，我们越来越有信心：基于超导技术、具备商业价值的量子计算机将在这十年结束前成为现实。

今天，我们高兴地宣布：Google Quantum AI 正在扩展我们的量子计算布局，纳入中性原子量子计算——一种以单个原子作为量子比特的技术路线。

## 量子计算的两种前景可期的路线

Google 将利用这两种技术路线互补的优势，加快我们达成近期里程碑的时间表，并扩大我们的影响力。超导量子比特已经扩展到拥有数百万次门操作与测量循环的电路，每个循环仅需一微秒。中性原子方面，则已扩展到约一万个量子比特的阵列。它们的循环时间较慢——以毫秒计——但以灵活的任意互连拓扑加以弥补，从而支持高效的算法和纠错码。前方的道路正反映了这些不同的起点：中性原子路线仍有待攻克的一个挑战是演示多循环的深度电路，而超导路线的下一项任务，则是演示拥有数万个量子比特的计算架构。用专家的行话说，我们常说超导处理器更容易在时间维度（电路深度）上扩展，而中性原子更容易在空间维度（量子比特数量）上扩展。同时投资两种路线，增强了我们更早兑现使命的能力。通过双线并进，我们让研究与工程的突破相互滋养，并能够提供针对不同问题类型量身打造的多样化平台。

## 一套完整的研究计划

我们的中性原子计划建立在三大关键支柱之上：

- 量子纠错（Quantum Error Correction，QEC）：让纠错适配中性原子阵列的连接结构，从而为容错架构带来低空间与时间开销。
- 建模与仿真：利用 Google 世界一流的算力资源和基于模型的设计，仿真硬件架构、优化错误预算并细化部件指标。
- 实验硬件研发：实现操纵原子量子比特所需的硬件能力，在应用规模上达到容错性能。

为了领衔这一实验攻坚，我们很高兴欢迎 [Adam Kaufman 博士](https://jila.colorado.edu/kaufman)加入 Google Quantum AI。Adam 表示：「能够加入 Google 世界领先的量子计算计划，并将这一领先优势拓展到中性原子这一全新且极具前景的平台，我感到非常兴奋。」Adam 将常驻科罗拉多州博尔德——全球原子、分子与光物理学（Atomic, Molecular and Optical，AMO）的重镇——领导 Google 不断壮大的中性原子硬件团队。他将继续担任 [JILA](https://jila.colorado.edu/) Fellow 以及科罗拉多大学博尔德分校（CU Boulder）教职，隶属于该校物理系。

我们也期待与我们的投资组合公司 [QuEra](https://x.com/GoogleQuantumAI/status/1846209669502550046?s=20) 继续开展富有成效的合作——QuEra 的研究人员开创了该领域的基础方法，并正在持续推进中性原子计算的发展。

## 来自量子生态的洞见

通过吸纳来自科罗拉多大学博尔德分校、JILA 和 [NIST 博尔德](https://www.nist.gov/states/colorado)等机构的杰出人才，我们正把自己的努力嵌入世界上最精深的物理与工程生态之一。科罗拉多大学博尔德分校、NIST 和 [Elevate Quantum](https://www.elevatequantum.org/) 的领导者们都强调，Adam 和 Google 有机会依托长期建立的伙伴关系，进一步增强博尔德乃至美国的量子生态。

「我们非常高兴 Google Quantum AI 邀请 Adam Kaufman 在博尔德领导这项重要工作，」科罗拉多大学博尔德分校科研与创新高级副校长兼研究所所长 Massimo Ruzzene 说，「Adam 的工作体现了科罗拉多大学博尔德分校量子生态的远见与卓越——从 JILA 和我们的物理系，到 CUbit Quantum Initiative 和 Colorado Quantum Incubator 等项目。这一合作将巩固博尔德在全国公认的量子版图，其背后有着重大联邦投资的支持，包括 [NSF Q‑SEnSE 研究所](https://www.colorado.edu/research/qsense/home)、[National Quantum Nanofab](https://www.colorado.edu/facility/national-quantum-nanofab/home) 和 [U.S. EDA Quantum TechHub](https://www.eda.gov/funding/programs/regional-technology-and-innovation-hubs/2023/Elevate-Quantum-Tech-Hub)。」[NIST 物理测量实验室](https://www.nist.gov/pml/about-pml)主任 James Kushmerick 指出：「像 Adam 这样富有创造力和影响力的研究者离开 NIST，总是令人惋惜。但这样的人事流动，正是 NIST 助力强化美国产业的方式之一。对 NIST 而言这是一个损失，但对博尔德的量子生态乃至整个美国量子产业而言，这是一种收获。」Massimo 和 James 都期待在 Adam 于 Google 履新后与他继续保持合作。

## 激动人心的前路

我们对自己有能力解决通往大规模量子计算之路上剩余的物理与工程问题充满信心；面对这一挑战的规模，我们心怀敬畏，也倍感振奋。

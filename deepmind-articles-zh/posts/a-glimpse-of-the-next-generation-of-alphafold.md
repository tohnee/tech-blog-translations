---
title: "下一代 AlphaFold 一瞥"
title_en: "A glimpse of the next generation of AlphaFold"
source: https://deepmind.google/blog/a-glimpse-of-the-next-generation-of-alphafold/
site: deepmind
date: 2023-10-31
crawled: 2026-09-13
translated: 2026-09-13
---

# 下一代 AlphaFold 一瞥

> 原文：[A glimpse of the next generation of AlphaFold](https://deepmind.google/blog/a-glimpse-of-the-next-generation-of-alphafold/) · Google DeepMind

进展更新：我们最新的 AlphaFold 模型显示出显著提升的准确度，并把覆盖范围从蛋白质扩展到包括配体在内的其他生物分子

自 2020 年发布以来，[AlphaFold](https://deepmind.google/technologies/alphafold/) 已经彻底改变了人们理解蛋白质及其相互作用的方式。Google DeepMind 与 [Isomorphic Labs](https://www.isomorphiclabs.com/) 一直在合作，为一个更强大的 AI 模型奠定基础——它将覆盖范围从蛋白质扩展到全部生物学相关分子。

今天，我们[分享一份进展更新](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-glimpse-of-the-next-generation-of-alphafold/alphafold_latest_oct2023.pdf)，介绍下一代 AlphaFold 的进展。我们最新的模型现在可以为 [Protein Data Bank](https://www.wwpdb.org/)（PDB）中的几乎所有分子生成预测，并常常达到原子级精度。

它开启了新的理解，并显著提升了多个关键生物分子类别的预测精度，包括配体（小分子）、蛋白质、核酸（DNA 和 RNA），以及包含翻译后修饰（PTM）的分子。这些不同的结构类型与复合物对理解细胞内的生物学机制至关重要，而此前要以高精度预测它们一直很有挑战。

该模型扩展后的能力与性能可以帮助加速生物医学突破，开启「数字生物学」的下一个时代——为疾病通路的功能机制、基因组学、生物可再生材料、植物免疫、潜在治疗靶点、药物设计机制，以及支持蛋白质工程与合成生物学的新平台提供新的洞见。

我们最新 AlphaFold 模型的一系列预测结构与基准真值（白色）的对比。

## 超越蛋白质折叠

[AlphaFold](https://deepmind.google/discover/blog/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology/) 是单链蛋白质预测的根本性突破。[AlphaFold-Multimer](https://www.biorxiv.org/content/10.1101/2021.10.04.463034v2) 随后扩展到多蛋白质链的复合物，接着是 AlphaFold2.3——它提升了性能并把覆盖范围扩大到更大的复合物。

2022 年，与欧洲生物信息学研究所（EMBL's European Bioinformatics Institute，EMBL-EBI）合作，AlphaFold 对科学界已知几乎所有[已编目蛋白质](https://deepmind.google/discover/blog/alphafold-reveals-the-structure-of-the-protein-universe/)的结构预测通过 [AlphaFold 蛋白质结构数据库](https://alphafold.ebi.ac.uk/)免费开放。

迄今为止，超过 190 个国家和地区的 140 万用户访问了 AlphaFold 数据库，世界各地的科学家利用 AlphaFold 的预测推进了各类研究——从加速新型[疟疾疫苗](https://deepmind.google/discover/blog/stopping-malaria-in-its-tracks/)开发、推进[癌症药物发现](https://deepmind.google/discover/blog/understanding-the-faulty-proteins-linked-to-cancer-and-autism/)，到开发应对污染的[「吃塑料」酶](https://deepmind.google/discover/blog/creating-plastic-eating-enzymes-that-could-save-us-from-pollution/)。

在这里，我们展示 AlphaFold 在超越蛋白质折叠之外预测精确结构的出色能力：在配体、蛋白质、核酸和翻译后修饰上都生成高精度的结构预测。

![四张柱状图，展示下一代 AlphaFold 模型在蛋白质-配体复合物（左上）、蛋白质（右上）、核酸（左下）和共价修饰（右下）上的表现。](https://lh3.googleusercontent.com/U_EZzsp4FXouG5u-mxbBb76Fn9XHCUvZl4ANHe6ULwm8gWnoTejYNvGT4BUahhDWR0ZPzfMEjLw3fGqvfzAgclzh-ZYS6Pr-eu8L5yIKemLFUWCNvg=w1440)

在蛋白质-配体复合物（a）、蛋白质（b）、核酸（c）和共价修饰（d）上的表现。

## 加速药物发现

早期分析还显示，在与药物发现相关的一些蛋白质结构预测问题上（比如抗体结合），我们的模型大幅超越 AlphaFold2.3。此外，精确预测蛋白质-配体结构是药物发现的极有价值的工具，因为它可以帮助科学家识别和设计可能成为药物的新分子。

当前的行业惯例是使用「对接方法（docking methods）」来确定配体与蛋白质之间的相互作用。这些对接方法需要一个刚性的参考蛋白结构，以及配体结合位置的预设。

我们最新的模型超越了已报道的最佳对接方法，且无需参考蛋白结构或配体口袋的位置——为蛋白质-配体结构预测设立了新标准——使得对此前从未进行过结构表征的全新蛋白质进行预测成为可能。

它还能联合建模所有原子的位置，从而表达蛋白质和核酸在与其他分子相互作用时完整的内在柔性——这是对接方法无法做到的。

例如，这里有三个近期发表的、具有治疗相关性的案例，我们最新模型预测的结构（彩色显示）与实验测定的结构（灰色显示）高度吻合：

1. [PORCN](https://doi.org/10.1038/s41586-022-04952-2)：一个临床阶段的抗癌分子与其靶点结合，并伴随另一个蛋白。
2. [KRAS](https://doi.org/10.1126/science.adg9652)：一个重要癌症靶点与共价配体（一种分子胶）形成的三元复合物。
3. [PI5P4Kγ](https://doi.org/10.1021/acs.jmedchem.1c01819)：一种脂质激酶的选择性别构抑制剂，与包括癌症和免疫疾病在内的多种疾病相关。

![PORCN（左）、KRAS（中）和 PI5P4Kγ（右）三个结构预测的数字渲染图。](https://lh3.googleusercontent.com/r0AZfPC_RpSbxkc0UWlC_-xjhPqmX8HdjvvOx7hlNer4ZNjkrrDAHSF-BmNdq_huCuFvCV9h_4g7ytyd4Byw72EE4e6j-IEQPxFxe8JGdgKF6q2Ac1U=w1440)

PORCN（1）、KRAS（2）和 PI5P4Kγ（3）的预测。

Isomorphic Labs 正在把这一下一代 AlphaFold 模型应用于治疗性药物设计，帮助快速、精确地表征多种对治疗疾病至关重要的高分子结构。

## 对生物学的新理解

通过解锁对蛋白质与配体结构、核酸以及含翻译后修饰分子的联合建模，我们的模型为考察基础生物学提供了一个更快速、更精确的工具。

一个例子涉及 [CasLambda 与 crRNA 及 DNA 结合的结构](https://www.rcsb.org/structure/8DC2)，它是 [CRISPR 家族](https://doi.org/10.1016/j.cell.2022.10.020)的一部分。CasLambda 具有与 [CRISPR-Cas9 系统](https://www.nobelprize.org/prizes/chemistry/2020/press-release/)相同的基因组编辑能力——后者通常被称为「基因剪刀」，研究人员可以用它改变动物、植物和微生物的 DNA。CasLambda 更小的体积可能使其在基因组编辑中的应用更高效。

![CasLambda（Cas12l）与 crRNA 及 DNA 结合的预测结构的数字渲染图，它是 CRISPR 子系统的一部分。](https://lh3.googleusercontent.com/btCM7mAXfuNJflMWIp_xUcCMOW4IU6fpS8xXlC7ZLsBDyN4sNpFAyO3rX_DM-CqDHdbAfmdN65M6_P6nO6DBXLXOqCFgG_uNwap1z77Cn0gWNG5WiA=w1440)

CasLambda（Cas12l）与 crRNA 及 DNA 结合的预测结构，它是 CRISPR 子系统的一部分。

最新版 AlphaFold 对这类复杂系统的建模能力告诉我们，AI 可以帮助我们更好地理解这些类型的机制，并加速它们在治疗应用中的使用。更多例子可在我们的[进展更新](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-glimpse-of-the-next-generation-of-alphafold/alphafold_latest_oct2023.pdf)中查看。

## 推进科学探索

我们模型性能的巨大飞跃表明，AI 有潜力极大增强我们对构成人体的分子机器——以及更广阔的自然世界——的科学理解。

AlphaFold 已经在世界范围内催化了重大的科学进步。如今，下一代 AlphaFold 有潜力以数字速度推进科学探索。

我们 Google DeepMind 与 Isomorphic Labs 的专门团队已经在这项关键工作上取得长足进步，我们期待分享持续的进展。

[阅读我们的进展更新](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-glimpse-of-the-next-generation-of-alphafold/alphafold_latest_oct2023.pdf)

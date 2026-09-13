---
title: "AlphaFold：用 AI 推动科学发现"
title_en: "AlphaFold: Using AI for scientific discovery"
source: https://deepmind.google/blog/alphafold-using-ai-for-scientific-discovery-2020/
site: deepmind
date: 2020-01-15
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaFold：用 AI 推动科学发现

> 原文：[AlphaFold: Using AI for scientific discovery](https://deepmind.google/blog/alphafold-using-ai-for-scientific-discovery-2020/) · Google DeepMind

更新：2022 年 7 月，我们发布了 AlphaFold 对科学界已知的几乎所有已编目蛋白质的蛋白质结构预测。最新博客请见[这里](https://deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe)。

在[发表于《自然》（Nature）的研究](https://rdcu.be/b0mtx)中，我们展示了人工智能研究如何能够驱动并加速新的科学发现。我们组建了一支专门的跨学科团队，希望利用 AI 推动基础研究向前发展：汇聚结构生物学、物理学和机器学习领域的专家，运用前沿技术，仅根据蛋白质的基因序列来预测其三维结构。

我们的系统 AlphaFold——相关论文已通过同行评审，分别发表在 [Nature](https://rdcu.be/b0mtx) 和 [PROTEINS](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.25834) 上——是多年工作的结晶，并建立在数十年来利用大规模基因组数据集预测蛋白质结构的研究基础之上。AlphaFold 生成的蛋白质三维模型在准确度上远超以往任何模型，标志着生物学核心挑战之一取得了重大进展。在 CASP13 上使用的 AlphaFold 代码已在 Github 上[开源](https://github.com/deepmind/deepmind-research/tree/master/alphafold_casp13)，供任何想深入了解或复现我们结果的人使用。令我们兴奋的是，这项工作已经启发了其他独立实现，包括[这篇论文](https://www.biorxiv.org/content/10.1101/846279v1.full.pdf)中描述的模型，以及一个由社区构建的[开源实现](https://github.com/dellacortelab/prospr)（见[这里](https://www.biorxiv.org/content/10.1101/830273v1)的介绍）。

## 什么是蛋白质折叠问题？

蛋白质是对一切生命都至关重要的大型复杂分子。人体执行的几乎所有功能——肌肉收缩、感知光线，或将食物转化为能量——都依赖于蛋白质，以及它们的运动和变化方式。任何一个蛋白质能做什么，取决于其独特的三维结构。例如，免疫系统所使用的抗体蛋白呈「Y 形」，会形成独特的钩状结构。通过钩住病毒和细菌，这些抗体蛋白能够识别疾病致病微生物并将其标记出来以便清除。胶原蛋白则呈绳索状，在软骨、韧带、骨骼和皮肤之间传递张力。其他类型的蛋白质还包括：Cas9，它以 CRISPR 序列为向导，像剪刀一样对 DNA 片段进行剪切和粘贴；抗冻蛋白，其三维结构使它们能够与冰晶结合，防止生物体被冻住；以及核糖体，它像一个可编程的装配流水线，帮助构建蛋白质本身。

这些蛋白质的「配方」——即基因——编码在我们的 DNA 中。基因配方中的错误可能导致蛋白质畸形，进而可能导致生物体患病或死亡。因此，许多疾病从根本上与蛋白质相关。但知道了一个蛋白质的基因配方，并不意味着你就自动知道了它的形状。蛋白质由氨基酸链（也称为氨基酸残基）构成，而 DNA 只包含氨基酸序列的信息——并不包含它们如何折叠成形状的信息。蛋白质越大，建模就越困难，因为需要考虑的氨基酸之间的相互作用更多。正如[列文塔尔佯谬（Levinthal's paradox）](https://en.wikipedia.org/wiki/Levinthal%27s_paradox)所展示的：若要随机穷举一个典型蛋白质所有可能的构型，直到找到真实的三维结构，所需时间将超过已知宇宙的年龄——然而蛋白质本身却能在几毫秒内自发完成折叠。预测这些链如何折叠成蛋白质复杂的三维结构，就是所谓的「蛋白质折叠问题」——科学家们已经为之奋斗了数十年的挑战。这个尚未解决的问题已经催生了无数进展：从推动 IBM 在超级计算上的投入（[BlueGene](https://en.wikipedia.org/wiki/IBM_Blue_Gene)），到新颖的公民科学项目（[Folding@Home](https://foldingathome.org/) 和 [FoldIt](https://fold.it/portal/)），再到诸如合理蛋白质设计这样的新工程领域。

## 为什么蛋白质折叠如此重要？

> 我认为，通过研究构成人体的分子——包括异常分子——我们将能够更透彻地理解疾病的一般本质；这种理解将使……我们能够以更直接的方式攻克疾病问题，从而开发出新的治疗方法。

Linus Pauling（莱纳斯·鲍林）

1960 年

科学家们长期以来一直致力于测定蛋白质的结构，因为人们认为蛋白质的形态决定了它的功能。一旦理解了蛋白质的形状，就可以推测它在细胞内的作用，科学家也能据此开发出与该蛋白质独特形状相配合的药物。

在过去五十年里，研究人员已经能够在实验室中借助[冷冻电子显微镜](https://en.wikipedia.org/wiki/Cryogenic_electron_microscopy)、[核磁共振](https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance)和 [X 射线晶体学](https://en.wikipedia.org/wiki/X-ray_crystallography)等实验技术测定蛋白质的形状，但每种方法都依赖大量的反复试错，可能耗费数年的工作，每个蛋白质结构的成本高达数万甚至数十万美元。正因如此，对于难以处理的蛋白质，生物学家正转向 AI 方法，以替代这种漫长而费力的流程。仅凭基因序列就以计算方式预测蛋白质形状的能力——而不必通过昂贵的实验来测定——可以帮助加速研究。

![一幅四步示意图，展示蛋白质如何折叠：从氨基酸序列出发，形成 α 螺旋和折叠片等局部形状，再折叠成复杂的三维蛋白质结构，最后与其他蛋白质相互作用。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273f8719ed3b2a84c8fd13_Fig201.svg)

图 1：复杂的三维形状由一串氨基酸演变而来。

## AI 能带来什么改变？

幸运的是，得益于基因测序成本的快速下降，基因组学领域的数据相当丰富。因此，过去几年里，依赖基因组数据来解决预测问题的深度学习[方法](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005324)日益流行。为了推动研究并衡量提高预测准确度的新方法的进展，1994 年设立了一项名为 CASP（[蛋白质结构预测关键评估](http://predictioncenter.org/)）的两年一度的全球竞赛，如今已成为评估预测技术的黄金标准。我们感念 CASP 组织者数十年的前期工作，也感念成千上万名为这类评估提供结构数据的实验科学家。

DeepMind 在这个问题上的工作成果就是 AlphaFold，我们将其提交到了 CASP13。我们很自豪能参与其中——CASP 组织者称其为「计算方法预测蛋白质结构能力的前所未有的进步」——我们在参赛队伍排名中位列[第一](http://predictioncenter.org/casp13/zscores_final.cgi?formula=assessors)（我们的参赛编号是 A7D）。

我们的团队专注于从零开始对目标形状进行建模的问题，而不使用先前已解析的蛋白质作为模板。我们在预测蛋白质结构的物理性质方面达到了很高的准确度，然后使用两种不同的方法来构建完整蛋白质结构的预测。

## 利用神经网络预测物理性质

这两种方法都依赖于深度神经网络，这些网络经过训练，能够从基因序列预测蛋白质的性质。我们的网络所预测的性质是：(a) 氨基酸对之间的距离，以及 (b) 连接这些氨基酸的化学键之间的角度。第一项进展是对常用技术的改进——以往的技术只能估计氨基酸对是否彼此接近。

我们训练了一个神经网络来预测蛋白质中每一对残基之间距离的分布（见图 2 的可视化）。随后，这些概率被合并成一个分数，用于估计所提出的蛋白质结构的准确程度。我们还训练了另一个独立的神经网络，它汇总所有距离，来估计所提出的结构与正确答案的接近程度。

![梯度下降法为 CASP13 靶标 T1008 预测结构的动画。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622692c5f70ee10657e72050_AlphaFold202.gif)

## 利用神经网络预测物理性质

这两种方法都依赖于深度神经网络，这些网络经过训练，能够从基因序列预测蛋白质的性质。我们的网络所预测的性质是：(a) 氨基酸对之间的距离，以及 (b) 连接这些氨基酸的化学键之间的角度。第一项进展是对常用技术的改进——以往的技术只能估计氨基酸对是否彼此接近。

我们训练了一个神经网络来预测蛋白质中每一对残基之间距离的分布（见图 2 的可视化）。随后，这些概率被合并成一个分数，用于估计所提出的蛋白质结构的准确程度。我们还训练了另一个独立的神经网络，它汇总所有距离，来估计所提出的结构与正确答案的接近程度。

![真实结构与 AlphaFold 对三个蛋白质靶标（T0954、T0965 和 T0955）平均预测距离的对比。上方各行展示了高度吻合的热图，表示残基对之间的距离；下方一行展示了折叠蛋白质的三维带状模型，绿色的真实结构与蓝色的 AlphaFold 预测结构几乎完全重合。](https://lh3.googleusercontent.com/anpBtYTh5VH53TPliYMyaHg8s_eb2bOGY8ouE8zSyEaPbEMb7F6p1de40adBWBfXF-pDYo8Zqsa7NH2bf6KSDcy1NMh5sgvMj8Gq4jMJUlMj5MxzWw=w1440)

图 2：可视化 AlphaFold 预测准确度的两种方式。上图为三个蛋白质的距离矩阵。每个像素的亮度代表构成该蛋白质的序列中氨基酸之间的距离——像素越亮，这一对氨基酸越接近。上排显示的是真实的、经实验测定的距离，下排显示的是 AlphaFold 预测距离分布的平均值。重要的是，它们在全局和局部尺度上都吻合得很好。下方的面板用三维模型呈现了同样的对比，展示了 AlphaFold 对相同三个蛋白质的预测（蓝色）与真实数据（绿色）。

利用这些评分函数，我们得以在蛋白质构象空间中搜索，寻找与我们预测相匹配的结构。第一种方法建立在结构生物学中常用的技术之上，反复用新的蛋白质片段替换蛋白质结构中的局部片段。我们训练了一个生成式神经网络来创造新片段，用这些片段持续提升所提出的蛋白质结构的分数。

![一张流程图，展示 AlphaFold 如何预测蛋白质结构：以蛋白质序列为输入，经过由数据库信息辅助的神经网络，输出距离预测和角度预测，再通过梯度下降评分进行优化，最终生成预测的三维蛋白质结构。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227400ac14721b5286ae553_AF2004.svg)

第二种方法通过[梯度下降](https://en.wikipedia.org/wiki/Gradient_descent)来优化分数——这是机器学习中常用的一种数学技术，用于进行小的增量式改进——最终得到了高度准确的结构。这项技术被应用于整条蛋白质链，而不是先分别折叠各个片段再组装成更大的结构，从而简化了预测过程。

在 CASP13 上使用的 AlphaFold 版本已在 [Github](https://github.com/deepmind/deepmind-research/tree/master/alphafold_casp13) 上开源，供任何想深入了解或复现我们蛋白质折叠结果的人使用。

## 接下来会怎样？

虽然我们为蛋白质折叠模型的成功感到兴奋，但在蛋白质生物学领域仍有许多工作要做，我们也很期待继续在这一领域努力。我们致力于探索 AI 能够为基础科学发现做出贡献的途径，希望产生真实世界的影响。这种路径最终可能帮助我们更好地理解人体及其运作方式，使科学家能够更高效地针对疾病设计新的有效疗法。科学家们目前只为人类细胞产生的约一半蛋白质绘制了结构图。一些罕见疾病涉及单个基因的突变，导致蛋白质畸形，进而可能对整个生物体的健康产生深远影响。像 AlphaFold 这样的工具可以帮助罕见病研究者快速而经济地预测目标蛋白质的形状。随着科学家通过模拟和模型对蛋白质的形状及其运作方式积累更多认识，这种方法最终可能帮助我们实现高效的药物发现，同时降低与实验相关的成本。我们希望 AI 能对疾病研究有所帮助，并最终改善全世界数百万患者的生活质量。

潜在的收益并不局限于健康领域——理解蛋白质折叠将助力蛋白质设计，这可能解锁巨大的[潜在收益](https://science.sciencemag.org/content/338/6110/1042)。例如，蛋白质设计可以推动可生物降解酶的进步，帮助处理塑料和石油等污染物，以更环保的方式帮助我们分解废弃物。事实上，研究人员已经开始[改造细菌](https://www.bbc.co.uk/news/science-environment-43783631)，使其分泌能让废弃物可生物降解、更易处理的蛋白质。

我们首次涉足蛋白质折叠的成功表明，机器学习系统能够整合多样化的信息来源，帮助科学家快速地为复杂问题想出创造性的解决方案。正如我们已经看到 AI 如何通过 [AlphaGo](https://deepmind.com/research/alphago/) 和 [AlphaZero](https://deepmind.google/blog/alphago-zero-starting-from-scratch/) 等系统帮助人们掌握复杂博弈，我们同样希望有一天，AI 的突破也能成为一个平台，增进我们对基础科学问题的理解。

看到蛋白质折叠领域这些早期的进展迹象，见证 AI 对科学发现的价值，令人振奋。尽管在我们能够对治疗疾病、处理废弃物等方面产生可量化的影响之前，还有大量工作要做，但我们深知其潜力巨大。随着一支[专门团队](https://deepmind.com/about/science)专注于探究机器学习如何推动科学世界的发展，我们期待看到我们的技术在诸多方面发挥作用。

欢迎收听我们的[播客](https://deepmind.com/blog/article/podcast-episode-5-out-of-the-lab)，了解这项工作背后的研究者。

本博文基于以下工作

[AlphaFold: Improved protein structure prediction using potentials from deep learning](https://rdcu.be/b0mtx)（Nature）

[Protein structure prediction using multiple deep neural networks in CASP13](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.25834)（PROTEINS）

在 CASP13 上使用的 AlphaFold 版本已在 [Github](https://github.com/deepmind/deepmind-research/tree/master/alphafold_casp13) 上开源，供任何想深入了解或复现我们蛋白质折叠结果的人使用。

这项工作由 Andrew Senior、Richard Evans、John Jumper、James Kirkpatrick、Laurent Sifre、Tim Green、Chongli Qin、Augustin Žídek、Sandy Nelson、Alex Bridgland、Hugo Penedones、Stig Petersen、Karen Simonyan、Steve Crossan、Pushmeet Kohli、David Jones、David Silver、Koray Kavukcuoglu 和 Demis Hassabis（德米斯·哈萨比斯）合作完成。

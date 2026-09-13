---
title: "AlphaFold：用 AI 推动科学发现"
title_en: "AlphaFold: Using AI for scientific discovery"
source: https://deepmind.google/blog/alphafold-using-ai-for-scientific-discovery/
site: deepmind
date: 2022-01-15
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaFold：用 AI 推动科学发现

> 原文：[AlphaFold: Using AI for scientific discovery](https://deepmind.google/blog/alphafold-using-ai-for-scientific-discovery/) · Google DeepMind

2022 年 7 月，我们发布了 AlphaFold 对科学界已知的几乎所有已编目蛋白质的结构预测。请[在此](https://deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe)阅读最新博客。

我们很高兴分享 DeepMind 的第一个重要里程碑，它展示了人工智能研究如何驱动并加速新的科学发现。凭借高度跨学科的工作方式，DeepMind 汇聚了结构生物学、物理学和机器学习领域的专家，运用前沿技术，仅根据蛋白质的基因序列来预测其三维结构。

我们的系统 **AlphaFold** 是我们过去两年持续攻关的成果，它建立在多年来利用海量基因组数据预测蛋白质结构的研究基础之上。AlphaFold 生成的蛋白质三维模型比以往任何模型都精确得多——在生物学的核心挑战之一上取得了重大进展。

## 什么是蛋白质折叠问题？

蛋白质是维持生命所必需的大型复杂分子。我们身体执行的几乎每一项功能——肌肉收缩、感知光线，或是把食物转化为能量——都可以追溯到一种或多种蛋白质及其运动和变化的方式。这些蛋白质的「配方」——即基因——编码在我们的 DNA 中。

一种给定的蛋白质能做什么，取决于其独特的三维结构。例如，构成我们免疫系统的抗体蛋白呈「Y 形」，类似于独特的挂钩。通过钩住病毒和细菌，抗体蛋白能够检测并标记致病的微生物，以便将其消灭。类似地，胶原蛋白呈绳索状，在软骨、韧带、骨骼和皮肤之间传递张力。其他类型的蛋白质还包括 Cas9，它以 CRISPR 序列为向导，像剪刀一样对 DNA 片段进行剪切和粘贴；抗冻蛋白，其三维结构使它们能够与冰晶结合，防止生物体被冻住；还有核糖体，它像一个程序化的装配线，帮助构建蛋白质本身。

但仅凭基因序列推算蛋白质的三维形状，是一项复杂的工作，几十年来一直令科学家感到棘手。挑战在于，DNA 只包含蛋白质「积木」——氨基酸残基——的排列顺序信息，这些残基构成长长的链条。预测这些链条如何折叠成蛋白质复杂的三维结构，就是所谓的「蛋白质折叠问题」。

蛋白质越大，建模就越复杂、越困难，因为需要考虑的氨基酸之间的相互作用也更多。正如 [Levinthal 悖论](https://en.wikipedia.org/wiki/Levinthal%27s_paradox)所指出的，若要枚举一个典型蛋白质的所有可能构型，直到找到正确的三维结构，所需时间将超过宇宙的年龄。

![一段展示梯度下降方法为 CASP13 靶点 T1008 预测结构的动画。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622692c5f70ee10657e72050_AlphaFold202.gif)

## 为什么蛋白质折叠很重要？

预测蛋白质形状的能力对科学家很有用，因为这是理解蛋白质在体内作用的基础，也有助于诊断和治疗被认为由错误折叠的蛋白质引起的疾病，例如[阿尔茨海默病](https://www.ncbi.nlm.nih.gov/pubmed/25230234)、[帕金森病](https://www.nature.com/news/misfolded-protein-transmits-parkinson-s-from-cell-to-cell-1.11838)、[亨廷顿病](https://cen.acs.org/articles/95/i39/Revised-view-Huntingtons-protein-misfolding.html)和[囊性纤维化](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5137970/)。

让我们尤为兴奋的是，它如何能增进我们对身体及其运作方式的理解，使科学家能够更高效地设计新的、有效的疾病疗法。随着我们通过模拟和模型获得更多关于蛋白质形状及其运作方式的知识，药物发现中的新潜力将被打开，同时还能降低实验相关成本。这最终可能改善全球数百万患者的生活质量。

对蛋白质折叠的理解还将助力蛋白质设计，这可能释放巨大的收益。例如，可生物降解酶的进步——这可以由蛋白质设计来实现——有助于治理塑料和石油等污染物，帮助我们以对环境更友好的方式分解废弃物。事实上，研究者已经开始[改造细菌](https://www.bbc.co.uk/news/science-environment-43783631)，使其分泌能让废弃物可生物降解、更易处理的蛋白质。

为了催化研究并衡量提高预测精度的最新方法的进展，1994 年设立了一项名为 CASP（[蛋白质结构预测关键评估](http://predictioncenter.org/)）的全球两年一度的竞赛，现已成为评估相关技术的黄金标准。

## AI 如何发挥作用？

在过去五十年里，科学家一直能够在实验室中使用[冷冻电子显微镜](https://en.wikipedia.org/wiki/Cryogenic_electron_microscopy)、[核磁共振](https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance)或 [X 射线晶体学](https://en.wikipedia.org/wiki/X-ray_crystallography)等实验技术测定蛋白质的形状，但每种方法都依赖大量试错，可能耗时数年，每个结构的成本高达数万美元。这正是生物学家们转而求助 AI 方法，以替代这一针对困难蛋白质的漫长而费力的过程的原因。

幸运的是，得益于基因测序成本的快速下降，基因组学领域的数据相当丰富。因此，近几年来，依赖基因组数据、用深度学习[解决](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005324)预测问题的方法日益流行。DeepMind 在这一问题上的工作催生了 AlphaFold，我们在今年将其提交给了 CASP。我们很自豪能成为 CASP 组织者所称的「计算方法预测蛋白质结构能力的前所未有的进步」的一部分，在参赛队伍中排名[第一](http://predictioncenter.org/casp13/zscores_final.cgi?formula=assessors)（我们的参赛编号为 A7D）。

我们的团队专门攻克了从零开始建模目标形状的难题，不使用已解析的蛋白质作为模板。我们在预测蛋白质结构物理性质方面达到了很高的精度，然后用两种不同的方法构建完整蛋白质结构的预测。

## 用神经网络预测物理性质

这两种方法都依赖于经过训练、能从基因序列预测蛋白质性质的深度神经网络。我们的网络预测的性质是：（a）氨基酸对之间的距离，以及（b）连接这些氨基酸的化学键之间的角度。第一项进展是对常用技术的改进，此前那些技术只能估计氨基酸对是否彼此邻近。

我们训练了一个神经网络，来预测蛋白质中每一对残基之间距离的独立分布。这些概率随后被组合成一个分数，用以估计某个候选蛋白质结构的精确程度。我们还训练了另一个神经网络，将所有距离汇总起来，估计候选结构与正确答案的接近程度。

![三组热图对比，将实验真实值（上排）与 AlphaFold 对蛋白质 T0954、T0965 和 T0955 的平均预测残基间距离矩阵（下排）进行比较，在深紫色背景上显示出几乎相同的绿色与黄色接触点图案。](https://lh3.googleusercontent.com/H6btdWbPuU5xavowlbbGgTpsYd2o1kkHc98ZmsKQTC_AsMzoKUzfo1U5rtSQKbXWC8mkaDDCP76KdodJEmTt9DLOAOynrsaZDuovQHjQzmmqehwL=w1440)

![三组三维蛋白质结构对比，将绿色表示的实验真实值与蓝色表示的 AlphaFold 预测结构（针对靶点 T0954、T0965 和 T0955）进行比较，展示出预测折叠与实际折叠近乎完美的一致。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6226930ed46fcbf3760027c2_AlphaFold204.gif)

## 构建蛋白质结构预测的新方法

利用这些评分函数，我们得以在蛋白质构象空间中搜索与我们的预测相匹配的结构。第一种方法建立在结构生物学常用技术的基础上，反复用新的蛋白质片段替换蛋白质结构的某些部分。我们训练了一个生成式神经网络来「发明」新片段，用它们持续提升候选蛋白质结构的得分。

![一张展示 AlphaFold 预测流程的流程图：蛋白质序列（Protein Sequence）输入经过神经网络与数据库，生成距离预测（Distance Predictions）和角度预测（Angle Predictions），二者组合成评分（Score），再通过梯度下降（Gradient Descent）优化，最终得到三维蛋白质结构（Structure）。](https://lh3.googleusercontent.com/4bH9gO00fzVL7jHerTJdZBP3arZk2LwDg4Dpwc_gl7dh5-kERioLl8Zzs2I5oOnFskLrN0CBvEsOPNhfNAXxKArFvgJFVieCpbd8JDnBJRVkdA-ojvM=w1440)

第二种方法通过[梯度下降](https://en.wikipedia.org/wiki/Gradient_descent)来优化评分——这是机器学习中常用的一种数学技术，用于进行小的、渐进式的改进——从而得到了高度精确的结构。该技术被应用于整条蛋白质链，而不是必须先分别折叠再组装的片段，从而降低了预测过程的复杂度。

## 接下来会怎样？

我们首次进军蛋白质折叠领域取得的成果，表明机器学习系统可以整合多种来源的信息，帮助科学家快速地为复杂问题找到富有创造性的解决方案。正如我们已经看到 AI 如何通过 [AlphaGo](https://deepmind.com/research/alphago/) 和 [AlphaZero](https://deepmind.com/blog/alphago-zero-learning-scratch/) 等系统帮助人们掌握复杂的博弈，我们也同样希望，有朝一日 AI 的突破也能帮助我们掌握基础科学问题。

看到蛋白质折叠领域这些早期的进展迹象，见证 AI 在科学发现中的实用性，令人振奋。尽管在能够对治疗疾病、管理环境等方面产生可量化的影响之前，还有很多工作要做，但我们知道其潜力是巨大的。拥有一支专注于探究机器学习如何推动科学世界的专职团队，我们期待看到我们的技术在众多方面发挥作用。

**附注**

在我们发表关于这项工作的论文之前，请引用如下：

**De novo structure prediction with deep-learning based scoring**

R.Evans, J.Jumper, J.Kirkpatrick, L.Sifre, T.F.G.Green, C.Qin, A.Zidek, A.Nelson, A.Bridgland, H.Penedones, S.Petersen, K.Simonyan, S.Crossan, D.T.Jones, D.Silver, K.Kavukcuoglu, D.Hassabis, A.W.Senior

发表于 Thirteenth Critical Assessment of Techniques for Protein Structure Prediction (Abstracts)，2018 年 12 月 1-4 日。全文取自[此处](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphafold-using-ai-for-scientific-discovery/A7D_AlphaFold.pdf)。

这项工作由以下人员合作完成：Richard Evans、John Jumper、James Kirkpatrick、Laurent Sifre、Tim Green、Chongli Qin、Augustin Zidek、Sandy Nelson、Alex Bridgland、Hugo Penedones、Stig Petersen、Karen Simonyan、Steve Crossan、David Jones、David Silver、Koray Kavukcuoglu、Demis Hassabis 和 Andrew Senior。

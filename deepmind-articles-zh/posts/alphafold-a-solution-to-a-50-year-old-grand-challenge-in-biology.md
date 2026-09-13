---
title: "AlphaFold：生物学 50 年重大挑战的解决方案"
title_en: "AlphaFold: a solution to a 50-year-old grand challenge in biology"
source: https://deepmind.google/blog/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology/
site: deepmind
date: 2020-11-30
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaFold：生物学 50 年重大挑战的解决方案

> 原文：[AlphaFold: a solution to a 50-year-old grand challenge in biology](https://deepmind.google/blog/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology/) · Google DeepMind

2022 年 7 月，我们发布了针对科学界已知的几乎所有已编目蛋白质的 AlphaFold 蛋白质结构预测。请[在此](https://deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe)阅读最新博文。

蛋白质对生命至关重要，支撑着几乎所有的生命功能。它们是由氨基酸链组成的大型复杂分子，[一种蛋白质的功能很大程度上取决于其独特的 3D 结构](https://www.youtube.com/watch?v=wvTv8TqWC48)。弄清楚蛋白质会折叠成什么形状，被称为「蛋白质折叠问题」（protein folding problem），在过去 50 年里一直是生物学的一项重大挑战。在一项重大科学进展中，我们的 AI 系统 [AlphaFold](https://deepmind.com/research/case-studies/alphafold) 的最新版本已被两年一度的蛋白质结构预测关键评估（[CASP](https://predictioncenter.org/)）的组织者认定为这一重大挑战的解决方案。这一突破展示了 AI 能够对科学发现产生的影响，以及它极大加速那些解释并塑造我们世界的最基础领域进展的潜力。

蛋白质的形状与其功能密切相关，预测这一结构的能力让我们能更深入地理解蛋白质做什么以及如何运作。世界上许多最重大的挑战——例如开发疾病治疗方法或找到能分解工业废物的酶——从根本上都与蛋白质及其扮演的角色相关。

> 我们在这个问题上——蛋白质如何折叠——已经卡了将近 50 年。看到 DeepMind 给出一个解决方案，对于在这个问题上亲自耕耘如此之久、经历无数次停顿与重启、一度怀疑能否走到这一步的我而言，是一个非常特别的时刻。

John Moult 教授

CASP 联合创始人兼主席，马里兰大学

多年来，这一直是密集科学研究的焦点，人们使用多种实验技术来检验和测定蛋白质结构，例如核磁共振和 X 射线晶体学。这些技术以及冷冻电子显微镜等较新的方法，都依赖大量的反复试错——解析每个结构可能需要数年艰苦而费力的工作，并且需要使用价值数百万美元的专用设备。

## 「蛋白质折叠问题」

Christian Anfinsen 在其 1972 年诺贝尔化学奖获奖演说中[提出了一个著名论断](https://www.nobelprize.org/uploads/2018/06/anfinsen-lecture.pdf)：理论上，蛋白质的[氨基酸序列](https://en.wikipedia.org/wiki/Protein_primary_structure)应该完全决定其结构。这一假说开启了一场长达五十年的探索：仅凭蛋白质的一维氨基酸序列，通过计算来预测其 3D 结构，作为这些昂贵且耗时的实验方法的补充替代。然而，一个主要挑战在于，蛋白质在最终落入其 3D 结构之前，理论上可能的折叠方式数量是天文数字。1969 年，Cyrus Levinthal 指出，用暴力计算列举一个典型蛋白质的所有可能构型所需的时间将超过已知宇宙的年龄——Levinthal 估计一个典型蛋白质有 [10^300 种可能的构象](https://web.archive.org/web/20110523080407/http://www-miller.ch.cam.ac.uk/levinthal/levinthal.html)。然而在自然界中，蛋白质会自发折叠，有些甚至在几毫秒内完成——这一矛盾有时被称为 [Levinthal 悖论](https://en.wikipedia.org/wiki/Levinthal%27s_paradox)。

## CASP14 评估的结果

1994 年，[John Moult 教授和 Krzysztof Fidelis 教授创立了 CASP](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.340230303)，作为一个两年一度的盲测评估，旨在催化研究、监测进展并确立蛋白质结构预测的最先进水平。它既是评估预测技术的黄金标准，也是一个建立在共同事业之上的独特全球社区。关键在于，CASP 选择的蛋白质目标都是仅在不久前才被实验测定的结构（有些在评估时仍在等待测定）；这些结构不会提前公布。参赛者必须盲测预测蛋白质的结构，随后这些预测会在实验数据可得时与之比对。我们深深感激 CASP 的组织者和整个社区，尤其是那些其解析的结构使这种严格评估成为可能的实验科学家们。

CASP 用于衡量预测准确性的主要指标是[全局距离测试（GDT，Global Distance Test）](https://en.wikipedia.org/wiki/Global_distance_test)，取值范围 0-100。简单来说，GDT 大致可以理解为：处于距正确位置某一阈值距离之内的氨基酸残基（蛋白质链上的珠子）所占的百分比。根据 [Moult 教授](https://youtu.be/gg7WjuFs8F4?t=144)的说法，GDT 达到 90 分左右通常被认为与实验方法获得的结果具有竞争力。

在今天发布的第 14 届 CASP 评估的[结果](https://predictioncenter.org/casp14/zscores_final.cgi)中，我们最新的 AlphaFold 系统在所有目标上取得 92.4 GDT 的总体中位数分数。这意味着我们的预测的平均误差（[RMSD](https://en.wikipedia.org/wiki/Root-mean-square_deviation_of_atomic_positions)）约为 1.6 [埃](https://en.wikipedia.org/wiki/Angstrom)，大致相当于一个原子的宽度（即 0.1 纳米）。即使对于最困难的蛋白质目标——最具挑战性的[自由建模（free-modelling）类别](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.25823)中的目标——AlphaFold 也取得了 87.0 GDT 的中位数分数（[数据见此](https://predictioncenter.org/decoysets2019/results.cgi)）。

![条形图：显示 CASP7-12、AlphaFold 与 AlphaFold 2 的自由建模中位数精度。](https://lh3.googleusercontent.com/SmuK-HbKkIWFcO2VGbrm1rEMlLVhC9b9MoSLVmqRXOZo4Cw1mZHwJ9QnOxUIdtdL0QDNq2I25-GRphERwbFq0__xRu7NZ566QW362B8J0F1LJEWXJg=w1440)

历届 CASP 中最佳团队在自由建模类别预测中位数的精度提升，按 best-of-5 GDT 衡量。

![3D 蛋白质目标旋转 360 度的动画。实验结果以绿色线条显示，计算预测为蓝色。两组线条几乎完全一致。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277caa7b7ddd67e5c7a0ad_Fig202.gif)

自由建模类别中两个蛋白质目标的示例。AlphaFold 预测出与实验结果相比高度精确的结构。

这些激动人心的结果让生物学家有机会将计算结构预测用作科学研究的核心工具。我们的方法对于某些重要类别的蛋白质可能尤为有用，例如[膜蛋白](https://en.wikipedia.org/wiki/Membrane_protein)——它们极难结晶，因而通过实验测定颇具挑战。

> 这项计算工作代表了蛋白质折叠问题——一项有 50 年历史的生物学重大挑战——上的惊人进展。它的到来比该领域许多人预测的要早几十年。看到它将以多少种方式从根本上改变生物学研究，将是一件令人兴奋的事情。

Venki Ramakrishnan 教授

诺贝尔奖得主，英国皇家学会主席

## 我们应对蛋白质折叠问题的方法

我们于 2018 年首次参加 [CASP13](https://www.predictioncenter.org/casp13)，携[AlphaFold 的初始版本](https://deepmind.com/blog/article/AlphaFold-Using-AI-for-scientific-discovery)在参赛者中取得了最高精度。此后，我们在《自然》（Nature）上[发表](https://www.nature.com/articles/s41586-019-1923-7.epdf?author_access_token=Z_KaZKDqtKzbE7Wd5HtwI9RgN0jAjWel9jnR3ZoTv0MCcgAwHMgRx9mvLjNQdB2TlQQaa7l420UCtGo8vYQ39gg8lFWR9mAZtvsN_1PrccXfIbc6e-tGSgazNL_XdtQzn1PHfy21qdcxV7Pw-k3htw%3D%3D)了关于我们 CASP13 方法的论文及相应[代码](https://github.com/deepmind/deepmind-research/tree/master/alphafold_casp13)，这些工作随后启发了[其他研究](https://www.pnas.org/content/117/3/1496)和社区开发的开源[实现](https://github.com/dellacortelab/prospr)。如今，我们开发的新型深度学习架构推动了 CASP14 方法的变革，使我们达到了无与伦比的精度水平。这些方法从生物学、物理学和机器学习领域汲取灵感，当然也汲取了过去半个世纪蛋白质折叠领域众多科学家工作的养分。

折叠的蛋白质可以被看作一张「空间图」（spatial graph）：残基是节点，边连接空间上相近的残基。这张图对于理解蛋白质内部的物理相互作用及其演化历史都很重要。对于在 CASP14 使用的最新版 AlphaFold，我们创建了一个基于注意力的神经网络系统，进行端到端训练，试图解读这张图的结构，同时对其正在构建的隐式图进行推理。它利用演化相关的序列、多序列比对（MSA）以及氨基酸残基对的表示来精化这张图。

通过迭代这一过程，系统能够对蛋白质的底层物理结构形成强有力的预测，并在数天之内确定高度精确的结构。此外，AlphaFold 还能借助内部置信度度量，预测每个预测蛋白质结构中哪些部分是可靠的。

我们在公开可得的数据上训练了这一系统，数据包括来自[蛋白质数据库](https://www.rcsb.org/)（PDB）的约 170,000 个蛋白质结构，以及包含未知结构蛋白质序列的[大型数据库](https://www.uniprot.org/)。训练大约使用了 16 个 [TPUv3](https://cloud.google.com/tpu/docs/types-zones)（即 128 个 TPUv3 核心，大致相当于约 100-200 个 GPU），运行数周——在当今机器学习大多数大型最先进模型的背景下，这是相对适中的算力。与我们的 CASP13 AlphaFold 系统一样，我们正在准备一篇关于该系统的论文，并将适时提交给同行评审期刊。

![流程图：展示 AlphaFold 的神经网络架构，说明输入的蛋白质序列如何经过遗传搜索、MSA 嵌入、序列-残基边和残基-残基边的处理，最终预测出折叠的 3D 蛋白质结构。](https://lh3.googleusercontent.com/oJ8Woucr8FeT6a7HIAqU0dZ4u-C4ypy5HqLPwaugm5wT7W2CJYgPVPnFVF9mFb8s5my1JBMgTOJP-Ix6FaLI59G583KTZrmK1joTO_cBeIBgD9inXA=w1440)

主要神经网络模型架构概览。模型在演化相关的蛋白质序列以及氨基酸残基对上运行，在两种表示之间迭代传递信息以生成结构。

## 现实世界影响的潜力

当 DeepMind 十年前起步时，我们希望有一天 AI 突破能帮助成为一个平台，以推进我们对基础科学问题的理解。如今，经过 4 年打造 AlphaFold 的努力，我们开始看到这一愿景成为现实，其影响波及药物设计与环境可持续性等领域。

马克斯·普朗克发育生物学研究所所长、CASP 评估员 Andrei Lupas 教授告诉我们：「AlphaFold 惊人精确的模型使我们解决了一个卡了近十年的蛋白质结构问题，重新启动了我们理解信号如何穿越细胞膜的工作。」

我们对 AlphaFold 能为生物学研究和更广阔的世界带来的影响持乐观态度，并期待在未来几年与他人合作，进一步了解其潜力。在撰写同行评审论文的同时，我们也在探索如何以可扩展的方式让更多人使用这一系统。

与此同时，我们还在与少数专业团队合作，研究蛋白质结构预测如何帮助我们理解特定疾病，例如帮助识别功能失常的蛋白质，并推理它们之间的相互作用。这些洞见可以让药物开发工作更加精准，与现有实验方法互补，更快找到有前景的疗法。

> AlphaFold 是一代人一遇的进展，以不可思议的速度和精度预测蛋白质结构。这一飞跃展示了计算方法如何蓄势变革生物学研究，并为加速药物发现进程带来巨大希望。

Arthur D. Levinson

博士，Calico 创始人兼 CEO，Genentech 前董事长兼 CEO

我们也已经看到迹象表明，蛋白质结构预测未来可能在疫情应对工作中发挥作用，成为科学界开发的众多工具之一。今年早些时候，我们[预测了 SARS-CoV-2 病毒的多个蛋白质结构](https://deepmind.com/research/open-source/computational-predictions-of-protein-structures-associated-with-COVID-19)，包括此前结构未知的 ORF3a。在 CASP14 中，我们预测了另一种冠状病毒蛋白 [ORF8](https://predictioncenter.org/casp14/gdtplot.cgi?group=205&models=first&target=T1064-D1) 的结构。实验科学家们以惊人的速度确认了 [ORF3a](https://www.biorxiv.org/content/10.1101/2020.06.17.156554v2) 和 [ORF8](https://www.biorxiv.org/content/10.1101/2020.08.27.270637v1) 两者的结构。尽管这两个目标极具挑战性且相关序列极少，与实验测定的结构相比，我们的两项预测都达到了很高的精度。

除了加速对已知疾病的理解，我们对这些技术在探索数亿个目前尚无模型的蛋白质方面的潜力感到兴奋——那是一片广阔的未知生物学疆域。由于 [DNA 编码了构成蛋白质结构的氨基酸序列](https://www.youtube.com/watch?v=gG7uCskUOrA)，[基因组学革命](https://www.genome.gov/About-Genomics/Introduction-to-Genomics)使得大规模读取自然界的蛋白质序列成为可能——通用蛋白质数据库（[UniProt](https://www.uniprot.org/)）中的蛋白质序列已达 1.8 亿条且仍在增加。相比之下，由于从序列到结构需要实验工作，蛋白质数据库（[PDB](http://pdb101.rcsb.org/)）中只有约 170,000 个蛋白质结构。在那些尚未测定结构的蛋白质中，可能有一些具有崭新而令人兴奋的功能——正如望远镜帮助我们看得更深入未知的宇宙，AlphaFold 这类技术或许能帮我们找到它们。

## 开启新的可能

AlphaFold 是我们迄今最重要的进展之一，但与所有科学研究一样，仍有许多问题有待解答。我们预测的每一个结构都不会尽善尽美。仍有许多东西需要学习，包括多个蛋白质如何形成复合物、它们如何与 [DNA](https://en.wikipedia.org/wiki/DNA)、[RNA](https://en.wikipedia.org/wiki/RNA) 或[小分子](https://en.wikipedia.org/wiki/Small_molecule)相互作用，以及我们如何确定所有氨基酸侧链的精确位置。与他人合作，在学习如何最好地将这些科学发现用于新药开发、环境治理等方面，也有许多工作要做。

对于所有在科学领域从事计算与机器学习方法研究的人而言，AlphaFold 这样的系统展示了 AI 作为辅助基础发现工具的惊人潜力。正如 50 年前 Anfinsen 提出了一个远超当时科学能力的挑战，我们宇宙中仍有许多未知的方面。今天宣布的进展让我们更有信心：AI 将成为人类拓展科学知识前沿最有用的工具之一，我们期待未来多年的努力与发现！

**注释**

在我们发表关于这项工作的论文之前，请引用：

High Accuracy Protein Structure Prediction Using Deep Learning

John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Kathryn Tunyasuvunakool, Olaf Ronneberger, Russ Bates, Augustin Žídek, Alex Bridgland, Clemens Meyer, Simon A A Kohl, Anna Potapenko, Andrew J Ballard, Andrew Cowie, Bernardino Romera-Paredes, Stanislav Nikolov, Rishub Jain, Jonas Adler, Trevor Back, Stig Petersen, David Reiman, Martin Steinegger, Michalina Pacholska, David Silver, Oriol Vinyals, Andrew W Senior, Koray Kavukcuoglu, Pushmeet Kohli, Demis Hassabis.

In Fourteenth Critical Assessment of Techniques for Protein Structure Prediction (Abstract Book), 30 November - 4 December 2020. Retrieved from [here](https://predictioncenter.org/casp14/doc/CASP14_Abstracts.pdf).

我们正处于探索如何最好地让其他团体使用我们结构预测的起步阶段，同时在准备一篇同行评审论文以供发表。虽然我们的团队无法回复每一个咨询，但如果 AlphaFold 可能与你的工作相关，请将简要介绍提交至 [alphafold@deepmind.com](mailto:alphafold@deepmind.com)。如有进一步探索的空间，我们会与你联系。

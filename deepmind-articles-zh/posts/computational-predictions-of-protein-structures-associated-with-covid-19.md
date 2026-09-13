---
title: "对与 COVID-19 相关的蛋白质结构的计算预测"
title_en: "Computational predictions of protein structures associated with COVID-19"
source: https://deepmind.google/blog/computational-predictions-of-protein-structures-associated-with-covid-19/
site: deepmind
date: 2020-08-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 对与 COVID-19 相关的蛋白质结构的计算预测

> 原文：[Computational predictions of protein structures associated with COVID-19](https://deepmind.google/blog/computational-predictions-of-protein-structures-associated-with-covid-19/) · Google DeepMind

科学界已对最近的 [COVID-19 疫情](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/)迅速行动起来，其基础是数十年来对这一病毒家族表征的基础研究。处于疫情响应前沿的实验室在[开放获取数据库](https://www.gisaid.org/)中[共享](https://www.nature.com/articles/d41587-020-00002-2)了病毒的基因组，使研究人员能够迅速开发出针对这种新型病原体的检测方法。其他实验室共享了一些[病毒蛋白](http://www.rcsb.org/news?year=2020&article=5e3c4bcba5007a04a313edcc)经实验测定和计算预测的结构，还有一些实验室共享了流行病学数据。我们希望通过发布若干与 SARS-CoV-2（引起 COVID-19 的病毒）相关、研究尚不充分的蛋白质的结构预测，以最新版本的 [AlphaFold 系统](https://deepmind.com/blog/article/AlphaFold-Using-AI-for-scientific-discovery)为科学事业贡献力量。我们要强调的是，这些结构预测尚未经过实验验证，但我们希望它们能帮助科学界探究病毒如何运作，并作为假说生成平台，为今后开发疗法提供实验工作的起点。我们深深得益于许多其他实验室的工作：没有全球研究人员以惊人的敏捷应对 COVID-19 疫情的努力，这项工作不可能完成。

了解蛋白质的结构为理解其功能提供了重要资源，但测定结构的实验可能需要数月甚至更久，有些实验还被证明难以进行。因此，研究人员一直在开发从氨基酸序列预测蛋白质结构的计算方法。在相似蛋白质的结构已被实验测定的情况下，基于「模板建模」的算法能够提供准确的蛋白质结构预测。AlphaFold 是我们[近期发表](https://rdcu.be/b0mtx)的深度学习系统，专注于在没有相似蛋白质结构可用时准确预测蛋白质结构，这被称为「自由建模」。自那篇论文发表以来，我们持续改进这些方法，并希望提供最有用的预测，因此我们正在分享使用我们新开发的方法为 SARS-CoV-2 中部分蛋白质生成的预测结构。

需要注意的是，我们的结构预测系统仍在开发中，我们无法确定所提供结构的准确性，尽管我们有信心该系统比我们早先的 [CASP13 系统](https://deepmind.com/blog/article/AlphaFold-Using-AI-for-scientific-discovery)更准确。我们确认，对于在[蛋白质数据库（Protein Data Bank）](https://www.rcsb.org/)中共享的[经实验测定](https://science.sciencemag.org/content/early/2020/02/19/science.abb2507)的 SARS-CoV-2 刺突蛋白结构，我们的系统给出了准确的预测，这让我们有信心认为模型对其他蛋白质的预测可能有价值。我们最近与英国 [Francis Crick 研究所](https://www.crick.ac.uk/)的多位同行（包括结构生物学家和病毒学家）分享了我们的结果，他们鼓励我们立即向整个科学界发布这些结构。我们的模型包含每个残基的置信度分数，以帮助标示结构中哪些部分更可能是正确的。我们只对缺乏合适模板或在模板建模中[较为困难](https://swissmodel.expasy.org/repository/species/2697049)的蛋白质提供预测。虽然这些研究不足的蛋白质并非当前治疗工作的主要焦点，但它们可能加深研究人员对 SARS-CoV-2 的理解。

通常我们会等待这项工作经过学术期刊同行评审后再发表。然而，考虑到[局势](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports)的严重性和时间敏感性，我们现在就把预测结构发布出来，采用[开放许可](https://creativecommons.org/licenses/by/4.0/)，任何人都可以使用。

感兴趣的研究人员可以在随数据附带的一份文档中阅读关于这些预测的更多技术细节。我们发布的蛋白质结构预测包括 SARS-CoV-2 膜蛋白、蛋白 3a、Nsp2、Nsp4、Nsp6 以及木瓜蛋白酶样蛋白酶（C 端结构域）。需要再次强调，这些是尚未经过实验验证的预测结构。我们对系统的工作仍在继续，并希望适时分享更多信息。

## 更新（2020 年 8 月 4 日）

在我们持续改进 AlphaFold 系统的同时，我们在此发布五个研究尚不充分的 SARS-CoV-2 靶点的最新预测（[这里](https://storage.googleapis.com/deepmind-com-v3-datasets/alphafold-covid19/structures_v3_4_8_2020.zip)，包括 SARS-CoV-2 膜蛋白、Nsp2、Nsp4、Nsp6 以及木瓜蛋白酶样蛋白酶（C 端结构域））。我们此前已在本网站以及 [CASP\_Commons](https://predictioncenter.org/caspcommons/) 网站上共享了预测，后者是 CASP（结构预测关键评估）社区成员协作运营的平台。CASP\_Commons 鼓励研究团队共享具有高生物学意义的蛋白质结构预测。今年春天，他们收集了多种 SARS-CoV-2 蛋白质的预测，我们提交了上述 5 个靶点外加 ORF3a 的多个模型。6 月 17 日，来自 UC Berkeley [Brohawn 实验室](http://www.brohawnlab.org/)的成员将 SARS-CoV-2 ORF3a 蛋白（蛋白 3a）的一个[实验测定结构](https://www.biorxiv.org/content/10.1101/2020.06.17.156554v1.full.pdf)[存入 PDB](http://www.rcsb.org/3d-view/6XDC)。这种蛋白形成一个离子通道，由于可用相关序列数量很少，它对结构预测极具挑战性。它还拥有一种此前未在 PDB 中出现过的全新折叠。我们对该蛋白的主模型拓扑大体正确，但未能正确放置跨膜螺旋或胞外结构域的某些部分。我们可能性第二高的模型（见下图，于 4 月初提交给 CASP\_Commons）与后来的实验工作非常吻合。自 4 月以来，我们改进了计算方法，最新模型始终能把更好的结构排为最可能的预测。因此，我们决定对其余 5 个尚未经实验测定的蛋白质发布一组新的预测。那篇实验论文证实了我们模型中起初让我们感到惊讶的若干方面（例如 C133 看起来位置不佳、难以形成链间二硫键，我们也很难看出我们的预测如何构成 C4 四聚体）。这增强了我们最初的期望：即便对非常困难的蛋白质，也有可能从 AlphaFold 的盲预测中得出与生物学相关的结论，从而加深我们对研究不足的生物系统的理解。

- 版本 3，发布于 2020 年 8 月 4 日，见[这里](https://storage.googleapis.com/deepmind-com-v3-datasets/alphafold-covid19/structures_v3_4_8_2020.zip)。
- 版本 2，发布于 2020 年 4 月 8 日，见[这里](https://storage.googleapis.com/deepmind-com-v3-datasets/alphafold-covid19/structures_v2_8_4_2020.zip)。
- 版本 1，发布于 2020 年 3 月 4 日，见[这里](https://storage.googleapis.com/deepmind-com-v3-datasets/alphafold-covid19/structures_4_3_2020.zip)。

引用格式：John Jumper, Kathryn Tunyasuvunakool, Pushmeet Kohli, Demis Hassabis, and the AlphaFold Team, “Computational predictions of protein structures associated with COVID-19”, Version 3, DeepMind website, 4 August 2020, <https://deepmind.com/research/open-source/computational-predictions-of-protein-structures-associated-with-COVID-19>

![一张 3D 蛋白质结构模型图，展示 AlphaFold 的预测结构（蓝色）与 SARS-CoV-2 蛋白 3a 的实验结构（绿色）的对齐情况。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228b4b73876ce2619d22060_fig_1.gif)

AlphaFold 在 CASP\_Commons 上的最佳预测以蓝色表示，实验结构以绿色表示。

[查看源代码](https://storage.googleapis.com/deepmind-com-v3-datasets/alphafold-covid19/structures_4_3_2020.zip)

---
title: "把 AlphaFold 的力量交到全世界手中"
title_en: "Putting the power of AlphaFold into the world’s hands"
source: https://deepmind.google/blog/putting-the-power-of-alphafold-into-the-worlds-hands/
site: deepmind
date: 2022-07-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 把 AlphaFold 的力量交到全世界手中

> 原文：[Putting the power of AlphaFold into the world’s hands](https://deepmind.google/blog/putting-the-power-of-alphafold-into-the-worlds-hands/) · Google DeepMind

2022 年 7 月，我们发布了科学界已知的几乎所有已编目蛋白质的 AlphaFold 蛋白质结构预测。请[在此](https://deepmind.com/blog/alphafold-reveals-the-structure-of-the-protein-universe)阅读最新博客。

今天，我无比自豪和激动地宣布：DeepMind 正在为人类对生物学的理解做出重大贡献。

去年 12 月当我们[公布 AlphaFold 2](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology) 时，它被誉为 50 年蛋白质折叠难题的解决方案。上周，我们发表了阐述如何构建这一高度创新系统的[科学论文](https://www.nature.com/articles/s41586-021-03819-2)和[源代码](https://github.com/deepmind/alphafold/)；而今天，我们将分享人体内每一个蛋白质形状的[高质量预测](https://alphafold.ebi.ac.uk/)，以及 20 种科学家赖以开展研究的其他生物的蛋白质预测。

当研究人员寻求疾病的治疗方法、并致力于解决人类面临的其他重大问题——包括抗生素耐药性、微塑料污染和气候变化——时，他们将受益于对蛋白质结构的新认识。蛋白质就像微小而精巧的生物机器。正如一台机器的结构告诉你它做什么一样，蛋白质的结构也能帮助我们理解它的功能。今天，我们正在分享[一批信息宝库](https://alphafold.ebi.ac.uk/)，它使[人类对人类蛋白质组的理解翻了一倍](https://www.nature.com/articles/s41586-021-03828-1)，并揭示了另外 20 种具有生物学意义的生物体中的蛋白质结构——从大肠杆菌到酵母，从果蝇到小鼠。

> 这将是自人类基因组图谱绘制以来最重要的数据集之一。

Ewan Birney

EMBL 副总干事兼 EMBL-EBI 所长

作为支持研究人员工作的强大工具，我们相信这是迄今为止 AI 在推进科学知识方面做出的最重大贡献，也是 AI 能为人类带来益处的一个绝佳例证。这些认识将为我们未来在理解生物学与医学方面的诸多激动人心的进展奠定基础。得益于 AlphaFold 团队五年不知疲倦的工作和大量巧思，以及过去几个月与[EMBL 欧洲生物信息学研究所（EMBL-EBI）](https://www.ebi.ac.uk/)伙伴的紧密合作，我们得以与全世界分享这一巨大而宝贵的资源。

![AlphaFold 预测的六个不同复杂蛋白质结构的三维渲染图，每个结构都展示了折叠的α螺旋、β折叠和环状结构，在浅灰色背景上以蓝色、黄色和橙色的渐变着色。](https://lh3.googleusercontent.com/rDmL1vjA-DDXpPoMVp6ugGzpkdD9n6jy-X9ij4cSB_pwzFUkHg_CiuB1D8EbnPkXuV7wu-j_Uy5seybyeKDJNAID2YwAWIf2MRjo1DJh5UWeWsDWxA=w1440)

蛋白质是精巧的生物机器，它们的三维结构往往既具有美学上的观赏性，又作为生命的基石在功能上至关重要。

这项最新工作建立在我们去年 12 月在 CASP14 会议上[宣布](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology)的成果之上。当时 DeepMind 推出了 AlphaFold 系统的全新重大版本，被该评估的主办方认定为攻克"理解蛋白质三维结构"这一 50 年宏大挑战的解决方案。通过实验测定蛋白质结构是一项耗时且艰辛的工作，但 AlphaFold 证明了 AI 能够大规模、在几分钟内、以原子级精度准确预测蛋白质的形状。在 [CASP](https://predictioncenter.org/casp14/index.cgi) 上，我们承诺分享我们的方法，并让这一知识体系被广泛获取。

![柱状图展示各届 CASP（CASP7、CASP8、CASP9、CASP10、CASP11、CASP12、CASP13 的 AlphaFold 与 CASP14 的 AlphaFold 2）在自由建模类别中的中位数准确率。从 CASP7 到 CASP12，GDT_TS 均低于 45；CASP13 在 50 多；CASP14 则高达 80 多。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227ad7f559b3d69b9a59624_Accuracy.svg)

各届 CASP 中最佳队伍在自由建模（free modelling）类别预测中位准确率的提升，以 5 次预测中的最佳 GDT 值衡量。

这个月，我们完成了兑现这一承诺所需的大量艰苦工作。我们在《自然》（Nature）上发表了两篇同行评审论文（[1](https://www.nature.com/articles/s41586-021-03819-2)、[2](https://www.nature.com/articles/s41586-021-03828-1)），并[开源了 AlphaFold 的代码](https://github.com/deepmind/alphafold/)。今天，与 [EMBL-EBI](https://www.ebi.ac.uk/) 合作，我们非常自豪地推出 [AlphaFold 蛋白质结构数据库](http://alphafold.ebi.ac.uk/%20)，它提供了迄今为止最完整、最准确的人类蛋白质组图景，使人类积累的高精度人类蛋白质结构知识增加了一倍以上。

![](https://lh3.googleusercontent.com/8CkXEzMIbwTRogjhcaZKNxh3o_bbix1H7EvI-fYo1vm0CpHruGkPXXAZM0NEidK7mjI1pz42OozVXBxyEWp_WqIYpAhLkHnvkmG-u0uUY4O8COVrW_4=w1440-h810-n-nu)

除了人类蛋白质组（人类基因组表达的约 2 万个蛋白质）之外，我们还开放了 [20 种其他具有生物学意义的生物体](https://www.alphafold.ebi.ac.uk/download)的蛋白质组，共计超过 35 万个蛋白质结构。针对这些生物体的研究是无数研究论文和众多重大突破的主题，并让我们对生命本身有了更深的理解。在接下来的几个月里，我们计划将覆盖范围大幅扩展**至科学界已知的几乎所有已测序蛋白质**——超过 1 亿个结构，涵盖 [UniProt 参考数据库](https://www.uniprot.org/help/uniref)的大部分内容。这将是一部名副其实的世界蛋白质年鉴。随着我们持续投入对 AlphaFold 的未来改进，该系统和数据库也会定期更新。

最令人兴奋的是，在世界各地科学家手中，这部新的蛋白质年鉴将促成并加速推进我们对这些生命基石的研究。通过早期的合作，我们已经看到研究人员在自己的工作中使用 AlphaFold 所取得的可喜进展。例如，[被忽视疾病药物研发倡议组织](https://dndi.org/)（DNDi）[已推进了](https://www.wired.co.uk/article/deepmind-alphafold-protein-diseases)针对那些对世界贫困地区影响尤为严重的疾病的研究，寻找救命的疗法；朴茨茅斯大学的[酶创新中心](https://www.port.ac.uk/research/research-centres-and-groups/centre-for-enzyme-innovation)（CEI）正在利用 AlphaFold 帮助设计更快的酶，以回收一些污染最严重的一次性塑料。对于依赖实验测定蛋白质结构的科学家来说，AlphaFold 的预测帮助他们加速了研究。另一个例子是，[科罗拉多大学博尔德分校](https://www.colorado.edu/)的一个团队发现利用 AlphaFold 预测来研究抗生素耐药性大有希望，而[加州大学旧金山分校](https://www.ucsf.edu/)的一个团队则利用这些预测[增进了对 SARS-CoV-2 生物学的理解](https://www.biorxiv.org/content/10.1101/2021.05.10.443524v1)。而这仅仅是我们所期待的结构生物信息学革命的开始。随着 AlphaFold 走向世界，现在有一座数据宝库正等待转化为未来的进展。

> AlphaFold 开辟了新的研究视野。看到强大的前沿 AI 让那些几乎只困扰贫困人群的疾病研究得以推进，令人深受鼓舞。

Ben Perry

被忽视疾病药物研发倡议组织（DNDi）发现开放创新负责人

对于 DeepMind 的 AlphaFold 团队而言，这项工作代表着五年巨大努力的结晶，其中包括创造性地克服许多艰难挫折，最终破解这一难题所需的一系列全新精巧的算法创新。它建立在几代科学家发现的基础上——从蛋白质成像和晶体学的早期先驱，到此后数以千计花费多年时间研究蛋白质的预测专家和结构生物学家。我们的梦想是，AlphaFold 通过提供这一基础性认识，能帮助更多科学家开展工作，并开辟全新的科学发现途径。

> 过去我们需要几个月甚至几年才能完成的工作，AlphaFold 一个周末就完成了。

John McGeehan 教授

朴茨茅斯大学生物结构学教授、酶创新中心（CEI）主任

在 DeepMind，我们的理念一直是：人工智能能够极大地加速许多科学领域的突破，进而推动人类进步。我们构建了 [AlphaFold](https://deepmind.com/research/case-studies/alphafold) 和 [AlphaFold 蛋白质结构数据库](https://alphafold.ebi.ac.uk/)，以支持和提升全世界科学家在重要工作中的努力。我们相信，AI 有潜力革新 21 世纪的科学研究方式，我们热切期待 AlphaFold 能帮助科学界解锁下一个发现。

欲了解更多，请访问《自然》（Nature）阅读我们经过同行评审的论文：[完整方法](https://www.nature.com/articles/s41586-021-03819-2)与[人类蛋白质组](https://www.nature.com/articles/s41586-021-03828-1)。你也可以在我们的[技术博客](https://deepmind.com/research/publications/enabling-high-accuracy-protein-structure-prediction-at-the-proteome-scale)中了解更多。如果你想探索我们的系统，这里有 [AlphaFold 的开源代码](https://github.com/deepmind/alphafold)和用于运行单个序列的 [Colab 笔记本](https://colab.sandbox.google.com/github/deepmind/alphafold/blob/main/notebooks/AlphaFold.ipynb)。要探索我们的结构，生物数据领域的世界领导者 EMBL-EBI 在[一个开放的、对所有人免费的、可检索的数据库](https://alphafold.ebi.ac.uk/)中托管了这些结构。

我们很乐意听到你的反馈，并了解 AlphaFold 如何在你的研究中发挥作用。请把你的故事发送到 [alphafold@deepmind.com](mailto:alphafold@deepmind.com)。

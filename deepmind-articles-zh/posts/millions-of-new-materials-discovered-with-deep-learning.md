---
title: "利用深度学习发现数百万种新材料"
title_en: "Millions of new materials discovered with deep learning"
source: https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/
site: deepmind
date: 2023-11-29
crawled: 2026-09-13
translated: 2026-09-13
---

# 利用深度学习发现数百万种新材料

> 原文：[Millions of new materials discovered with deep learning](https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/) · Google DeepMind

AI 工具材料发现模型 GNoME 找到 220 万种新晶体，其中包括 38 万种稳定材料，它们或将为未来技术提供动力

从计算机芯片、电池到太阳能电池板，现代技术都依赖无机晶体。要催生新技术，晶体必须稳定，否则会分解；而每一种新的稳定晶体背后，可能是长达数月的艰辛实验。

今天，我们在[发表于 Nature 的论文](https://www.nature.com/articles/s41586-023-06735-9)中分享了 220 万种新晶体的发现——相当于近 800 年的知识积累。我们介绍材料探索图网络（Graph Networks for Materials Exploration，GNoME），这是我们全新的深度学习工具，通过预测新材料的稳定性，大幅提升发现的速度与效率。

借助 GNoME，我们把人类已知的、具备技术可行性的材料数量翻了几倍。在其 220 万个预测中，有 38 万种是最稳定的，使它们成为有前景的实验合成候选材料。这些候选材料中，有一些有望催生未来的变革性技术——从为超级计算机提供动力的超导体，到提升电动汽车效率的下一代电池。

GNoME 展示了用 AI 大规模发现和开发新材料的潜力。世界各地实验室的外部研究人员已经在并行工作中实验合成了其中 736 种新结构。与 Google DeepMind 合作，劳伦斯伯克利国家实验室（Lawrence Berkeley National Laboratory）的一组研究人员也在 Nature 上发表了[第二篇论文](https://www.nature.com/articles/s41586-023-06734-w)，展示如何利用我们的 AI 预测实现自主材料合成。

我们已向研究界公开了 [GNoME 的预测结果](https://www.nature.com/articles/s41586-023-06735-9)。我们将把预测为稳定的 38 万种材料贡献给 Materials Project，该项目正在处理这些化合物，并将它们加入[其在线数据库](https://next-gen.materialsproject.org/)。我们希望这些资源能够推动无机晶体的研究，并释放机器学习工具作为实验指引的前景。

## 用 AI 加速材料发现

![一幅同心圆图，展示晶体材料发现的规模。最小的深蓝色圆圈代表「人类实验」，对应 2 万个发现；它嵌套在中蓝色圆圈「计算方法」中，对应 4.8 万个发现；后者又嵌套在一个巨大的浅蓝色圆圈「GNoME」中，对应 42.1 万个发现，凸显了 AI 驱动材料发现的惊人规模。](https://lh3.googleusercontent.com/eQQaMwaeVZIZ6W3FXvY4Fq9xdFvA2s5z94cSv74_GF8Ctdyn0Xtq5vOXBpuGNhx_PgmsmHz266aYV3KiAJCYxKxR2FbTyF-PwlJTY5fLweVHCWr15w=w1440)

ICSD 数据库中经实验确认的晶体约有 2 万种在计算上是稳定的。借鉴 Materials Project、Open Quantum Materials Database 和 WBM 数据库的计算方法将这一数字提升到 4.8 万种稳定晶体。GNoME 将人类已知的稳定材料数量扩展到 42.1 万种。

过去，科学家通过微调已知晶体或尝试新的元素组合来寻找新晶体结构——这是一个昂贵、反复试错的过程，即便要取得有限的结果也可能需要数月。过去十年，由 [Materials Project](https://materialsproject.org/) 和其他团队牵头的计算方法已帮助发现了 2.8 万种新材料。但直到现在，新的 AI 引导方法在准确预测实验可行的材料这一能力上仍遭遇根本性瓶颈。GNoME 发现的 220 万种材料相当于约 800 年的知识积累，并展示了前所未有的预测规模与精度水平。

例如，有 5.2 万种与石墨烯类似的新型层状化合物，有望通过超导体的开发变革电子学。此前，[只有约 1,000 种此类材料被确认](https://pubmed.ncbi.nlm.nih.gov/28191965/)。我们还发现了 528 种潜在的锂离子导体，是一项[先前研究](https://pubs.rsc.org/en/content/articlelanding/2017/ee/c6ee02697d)的 25 倍，它们可用于提升可充电电池的性能。

我们正在发布 38 万种预测材料的结构，它们最有可能在实验室成功制备并用于可行的应用。一种材料要被认为稳定，必须不会分解为能量更低的相似成分。例如，石墨烯状结构中的碳就比金刚石中的碳稳定。在数学上，这些材料位于凸包（convex hull）之上。本项目发现了 220 万种符合当前科学标准、且位于以往发现的凸包之下的新稳定晶体。其中，38 万种被认为最稳定，位于「最终」凸包之上——这是我们为材料稳定性设定的新标准。

## GNoME：利用图网络进行材料探索

![一幅流程图，展示 GNoME 的主动学习循环，分为「结构管线」和「成分管线」。两条管线均生成候选材料、将其表示为图，并使用 GNN 预测稳定性。这些预测经 DFT 验证后加入 GNoME 数据库，并用于输出「能量模型」「220 万种稳定」材料和「原子间势」，数据再反馈用于后续学习轮次。](https://lh3.googleusercontent.com/xdW-P8-xOUqjCJdtuZQcsdhLfNYcjOjSckg97qWuOeAflq0QJR_fUlv5gPIy7BDtwdKwtSFiY3TKfvDJs5Ka54Xne5GnSNXUmeoif8X5k8l4wdf9SZU=w1440)

GNoME 使用两条管线来发现低能量（稳定）材料。结构管线生成与已知晶体结构相似的候选材料，而成分管线遵循基于化学式的更随机的方式。两条管线的输出都用成熟的密度泛函理论（DFT）计算进行评估，结果被加入 GNoME 数据库，为下一轮主动学习提供信息。

GNoME 是一个最先进的图神经网络（GNN）模型。GNN 的输入数据采用图的形式，可以类比为原子之间的连接，这使得 GNN 特别适合发现新的晶体材料。

GNoME 最初通过 [Materials Project](https://next-gen.materialsproject.org/) 公开提供的晶体结构及其稳定性数据进行训练。我们用 GNoME 生成新颖的候选晶体，并预测它们的稳定性。为了在渐进式训练周期中评估模型的预测能力，我们反复使用成熟的计算技术——密度泛函理论（DFT）——来检验其表现。DFT 被用于物理学、化学和材料科学以理解原子结构，这对评估晶体的稳定性十分重要。

我们采用了一种称为「主动学习」（active learning）的训练过程，大幅提升了 GNoME 的性能。GNoME 会对新颖稳定晶体的结构生成预测，然后用 DFT 检验。所得的高质量训练数据再反馈到我们的模型训练中。

我们的研究将材料稳定性预测的发现率从约 50% 提升到 80%——依据的是 [MatBench Discovery](https://matbench-discovery.materialsproject.org/)，这是由以往最先进模型设立的外部基准。我们还通过把发现率从不足 10% 提升到 80% 以上来扩大模型的效率——这样的效率提升可能会对每次发现所需的算力产生重大影响。

## 新材料的 AI「配方」

GNoME 项目旨在降低发现新材料的成本。外部研究人员已在实验室独立制备出 GNoME 的 736 种新材料，证明我们的模型对稳定晶体的预测准确反映了现实。我们已向研究界发布新发现晶体的数据库。通过向科学家提供新候选材料中有前景「配方」的完整目录，我们希望这能帮助他们测试并可能制备出其中最好的材料。

![六种预测稳定晶体的 3D 分子结构，每种都标注了化学式：K2BiCl5、Li4MgGe2S7、Mo5GeB2、KV3Se3、Rb2HfSi3O9 和 Tm5Pd9P7。](https://lh3.googleusercontent.com/nUYwTkQmJC-_e956cSIIx9umzvDb4cWcpjJQUa-ikFg-1-mAV8X7YkK0yMy8xLjN-NoTINjDC_t7LhXcT2rs14-0aawWc-6cCc3apj44fqWn4LI_LQ=w1440)

在我们完成最新的发现工作后，我们检索了科学文献，发现我们的计算发现中有 736 种已被全球各地的外部团队独立实现。上图是六个例子，从首创的碱土金属类金刚石光学材料（Li4MgGe2S7）到一种潜在超导体（Mo5GeB2）。

基于这些晶体快速开发新技术，将取决于制造它们的能力。在我们伯克利实验室合作者主导的一篇论文中，研究者展示了一个机器人实验室可以用自动化合成技术快速制造新材料。借助来自 Materials Project 的材料和来自 GNoME 的稳定性洞见，这个自主实验室创建了新的晶体结构配方，并成功合成了 41 种以上新材料，为 AI 驱动的材料合成开辟了新的可能。

![一只自动化机械臂在玻璃封闭的合成实验装置内操作，四周摆满用于材料发现的样品瓶托盘和化学容器。](https://lh3.googleusercontent.com/n0q40AO2pID4Ke3smLEyZDzlXSsukFpl_pE1jX1kpnTTl4QPCg3vbSrZUui62TIL0L4YkpF7DV_J7mMFAehJOcXxOB0MAvJ8_bg4tdsha4PXxVkxxcA=w1440)

A-Lab，伯克利实验室的一处设施，人工智能在这里引导机器人制造新材料。图片来源：Marilyn Sargent/Berkeley Lab

## 为新技术提供新材料

要建设更可持续的未来，我们需要新材料。GNoME 已发现 38 万种稳定晶体，它们蕴藏着开发更环保技术的潜力——从为电动汽车配备更好的电池，到为更高效的计算提供超导体。

我们的研究——以及伯克利实验室、Google Research 和全球各地团队的合作者的研究——展示了用 AI 引导材料发现、实验和合成的潜力。我们希望 GNoME 与其他 AI 工具一道，能够帮助变革当今的材料发现，并塑造这一领域的未来。

**阅读我们发表在 Nature 上的论文**

[阅读我们发表在 Nature 上的论文](https://www.nature.com/articles/s41586-023-06735-9)[阅读伯克利实验室发表在 Nature 上的论文](https://www.nature.com/articles/s41586-023-06734-w)[下载数据集](https://github.com/google-deepmind/materials_discovery)

**致谢**

没有出色的合著者，这项工作不可能完成：Simon Batzner、Sam Schoenholz、Muratahan Aykol 和 Gowoon Cheon。我们还要感谢 Doug Eck、Jascha Sohl-dickstein、Jeff Dean、Joëlle Barral、Jon Shlens、Pushmeet Kohli 和 Zoubin Ghahramani 对项目的支持；感谢 Lizzie Dorfman 提供产品管理支持；Andrew Pierson 提供项目管理支持；Ousmane Loum 在计算资源上的帮助；Luke Metz 在基础设施上的帮助；Ernesto Ocampo 在 AIRSS 管线早期工作中的帮助；Austin Sendek、Bilge Yildiz、Chi Chen、Chris Bartel、Gerbrand Ceder、Joy Sun、JP Holt、Kristin Persson、Lusann Yang、Matt Horton 和 Michael Brenner 的深入讨论；以及 Google DeepMind 团队的持续支持。

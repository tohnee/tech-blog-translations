---
title: "Alex Berg 在 ICCV 上获颁 IEEE Helmholtz 奖"
title_en: "Alex Berg receives IEEE Helmholtz Prize at ICCV"
date: 2019-10-29
source: https://ai.meta.com/blog/alex-berg-receives-ieee-helmholtz-prize-at-iccv/
crawled: 2026-09-22
translated: 2026-09-22
---

# Alex Berg 在 ICCV 上获颁 IEEE Helmholtz 奖

> 原文：[Alex Berg receives IEEE Helmholtz Prize at ICCV](https://ai.meta.com/blog/alex-berg-receives-ieee-helmholtz-prize-at-iccv/) · Meta AI（Wayback 存档）

Facebook AI 研究科学家 Alex Berg 是 2019 年 Helmholtz 奖的获奖者之一，该奖项表彰其在计算机视觉领域的基础性贡献。这一奖项每两年在国际计算机视觉大会（ICCV）上颁发，本届 ICCV 本周正在韩国首尔举行。它表彰的是 10 年前发表、对计算机视觉研究产生重大影响的 ICCV 论文。Berg 与合著者 Neeraj Kumar、Peter N. Belhumeur 和 Shree K. Nayar 凭借论文「Attribute and Simile Classifiers for Face Verification」获奖，该论文于 2009 年在 ICCV 上发表。今年 ICCV 上，Berg 还将报告两篇论文，并联合组织多个研讨会，其中包括一个关于极限视觉建模的研讨会。（Facebook 研究者在 ICCV 工作的更多细节见此处。）

Berg 抽空分享了他对过去、当前和未来研究的思考，包括其研究的可能应用，以及计算机视觉领域近年来的进展。

**请介绍一下获得 Helmholtz 奖评审委员会认可的这项工作。**

这个奖是给论文「Attribute and Simile Classifiers for Face Verification」的，它发表于 ICCV 2009，当时我还是哥伦比亚大学的博士后。论文提出了两种鲁棒而精确的人脸表示方法：一种是学习识别可描述的高层人脸属性（attribute），另一种是把人脸的局部与其他人脸进行比较——为诸如拥有「贝蒂·戴维斯的眼睛」（正如那首歌所唱）这类说法建立计算版本。这项工作把当时新颖的机器学习方法（大数据——论文引入了一个人脸数据集）与真实世界图像中人脸识别这一基础性挑战结合了起来。

**是什么让你聚焦这个问题？你当时希望达成什么？**

那时候，探索计算机视觉识别任务的研究者正在尝试识别各种新东西，而属性（attributes）可以灵活组合，对于把可识别的范围扩展到简单类别之外很有吸引力。这篇论文是最早证明学习识别属性能够帮助提升一个被广泛研究的识别问题最优精度的论文之一。

**这项研究还有其他人参与吗？**

这是与博士生 Neeraj Kumar、Shree Nayar 教授和 Peter Belhumeur 教授的合作工作，他们当时都在哥伦比亚大学。

**研究共同体最初的反响如何？发表以来又产生了什么影响？**

这篇论文因若干原因获得认可。作为研究的一部分而整理的数据集 pub-fig，成为展示如何成功利用属性提升识别精度的范例。它还产出了一些有趣的结论，说明人类在人脸验证任务上与算法相比表现如何。

**自那篇论文发表以来，你的工作如何演进？现在专注于什么？**

我的一条研究主线一直在尝试扩展识别研究的目标范围：从包含一千个类别的 ImageNet 挑战赛，到层级式识别的工作，再到寻找「入门级」类别的计算方法，以及一般性地连接语言与视觉。

**论文发表以来，这个领域的研究演进最令你惊讶的是什么？哪些比你预想的更难或更容易？未来几年你希望看到什么？**

人脸识别持续受益于数据量的增长和模型的改进。如今的人脸识别方法准确性和鲁棒性之高，以至于人脸验证有时被用作手机解锁的主要方式。回过头看，我们当时基于属性的人脸工作依赖标注。如果这项工作能在自监督时代重做——算法自己识别潜在属性并无监督地学会识别它们——那将会很有意思。

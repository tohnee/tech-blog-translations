---
title: "Hateful Memes 挑战赛获胜者"
title_en: "Hateful Memes Challenge winners"
date: 2020-12-11
source: https://ai.facebook.com/blog/hateful-memes-challenge-winners
crawled: 2026-09-22
translated: 2026-09-22
---

# Hateful Memes 挑战赛获胜者

> 原文：[Hateful Memes Challenge winners](https://ai.facebook.com/blog/hateful-memes-challenge-winners) · Meta AI（Wayback 存档）

2020 年 12 月 11 日

AI 在检测仇恨言论方面已经取得进展，但重要而困难的技术挑战依然存在。2020 年 5 月，Facebook AI 携手 Getty Images 和 DrivenData 启动了 Hateful Memes 挑战赛——首个此类竞赛，奖金 10 万美元，旨在加速对图文结合的仇恨言论检测问题的研究。作为挑战赛的一部分，Facebook AI 创建了一个包含 10000 多个新多模态样本的独特数据集，采用 Getty Images 的授权图片，让研究者可以在自己的工作中方便地使用。来自世界各地的 3300 多名参赛者参加了 Hateful Memes 挑战赛，我们现在分享获奖作品的细节。

表现最佳的团队是：

- Ron Zhu——代码链接
- Niklas Muennighoff——代码链接
- HateDetectron 团队：Riza Velioglu 和 Jewgeni Rose——代码链接
- Kingsterdam 团队：Phillip Lippe、Nithin Holla、Shantanu Chandra、Santhosh Rajamanickam、Georgios Antoniou、Ekaterina Shutova 和 Helen Yannakoudakis——代码链接
- Vlad Sandulescu——代码链接

完整排行榜见此处。作为 NeurIPS 2020 竞赛赛道的一部分，前五名获胜者将介绍他们的解决方案，我们还组织了与世界各地参赛者的问答。这五个实现均已开源，现在即可获取。

Hateful Memes 数据集包含真实的仇恨言论。因此我们不展示数据集中的真实表情包，这里只展示一些「仅仅是刻薄」的示例。在下面每张示例表情包中，文字短语和图片单独看都是无害的，只有把文字短语和图片放在一起考虑时，表情包的语义内容才变得刻薄。

我们对这项困难任务所获得的参与度感到满意。最佳提交达到了 0.8450 的 AUC ROC，大幅超越了我们作为挑战赛一部分所提供的基线模型。参赛者使用公开数据集训练和测试模型，但最终在一个全新的、未见过的测试集上评估。

## 为什么仇恨表情包对 AI 是一个困难的挑战

仇恨言论有多种形式，包括图文结合的表情包。这类多模态内容对 AI 检测来说尤其困难，因为它需要对表情包的整体理解。在 Facebook AI 创建的一个示例中，文字「看看有多少人爱你」搭配了一张空旷沙漠的照片。分开来看，这句话和这张图各自都无害。AI 要检测出真实含义，必须对表情包进行整体分析。关于这项任务的难度，详见 Hateful Memes 论文。（流程图展示了数据集的创建过程。）

## 构建检测仇恨表情包 AI 的不同方法

前五名提交采用了多种不同方法，包括：1）最先进视觉-语言模型的集成，如 VILLA、UNITER、ERNIE-ViL、VL-BERT 等；2）基于规则的附加组件；3）外部知识，包括从公开目标检测管线导出的标签。

作为获奖资格的要求，获胜团队被要求开源全部代码，并撰写一篇说明如何复现其结果的学术论文。我们希望 AI 研究社区的其他人能在他们工作的基础上继续构建，改进自己的系统。我们还将分享来自挑战赛以及 NeurIPS 2020 上 Hateful Memes 讨论环节的经验。

## 接下来是什么

开放挑战赛和共享数据集是 AI 研究社区加速基础问题进展的最有效工具之一。仇恨言论仍然是一项重要挑战，而多模态仇恨言论尤其是一个困难的机器学习问题。例如，在 ACL 2021 举行、由 Facebook AI 研究者共同组织的线上辱骂与伤害研讨会（Workshop on Online Abuse and Harms，WOAH）将设立多模态仇恨言论专题。

Hateful Memes 挑战赛竞赛已经落幕，但真正的挑战远未解决：多模态 AI 研究仍有大量工作要做，我们希望这个数据集能在评估该领域提出的的新方案中发挥重要作用。该数据集的设计使其很适合评估下一代多模态预训练模型的威力，以及该领域尚未想象到的进展。我们希望 Hateful Memes 数据集将继续为未来的新思路和新方法提供参考。

作者：
- Douwe Kiela，研究科学家
- Hamed Firooz，研究科学家经理
- Tony Nelli，项目经理

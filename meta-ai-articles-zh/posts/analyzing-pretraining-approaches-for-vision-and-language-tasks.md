---
title: "分析视觉与语言任务的预训练方法"
title_en: "Analyzing pretraining approaches for vision and language tasks"
date: 2020-05-29
source: https://ai.facebook.com/blog/analyzing-pretraining-approaches-for-vision-and-language-tasks
crawled: 2026-09-22
translated: 2026-09-22
---

# 分析视觉与语言任务的预训练方法

> 原文：[Analyzing pretraining approaches for vision and language tasks](https://ai.facebook.com/blog/analyzing-pretraining-approaches-for-vision-and-language-tasks) · Meta AI（Wayback 存档）

2020 年 5 月 29 日

**研究内容：**我们展示了预训练中若干简单却少有探索的设计选择，如何帮助在结合语言与视觉理解的任务上取得高性能。这些改进无需对底层模型做任何架构改动。它们也与该领域更常见的性能提升方法（如专注于优化预训练目标函数和模型架构选择）形成互补。对于这类视觉—语言任务——例如视觉问答，AI 必须分析一张图像并正确回答关于图像内容的问题——模型首先要经过预训练来求解代理任务。我们的方法聚焦于通过改变预训练数据集域（文本域和视觉域）与下游域之间的相似度来提升性能。我们证明，这可以在不做任何架构改动的情况下，在下游任务上取得接近最优（state-of-the-art）的结果。我们正在把这项工作的代码作为开源多模态框架的一部分分享出来。

**工作原理：**

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

这张图展示了改变预训练数据集与下游数据集如何影响模型性能。

在视觉与语言研究中，「先预训练再微调」范式的细微差别与细节尚未被仔细研究。例如，大量近期研究因 Conceptual Captions 规模大而将其用作预训练数据集，但噪声更少的 COCO captions 或许是更合适的选择？在选择最有效的预训练数据集时，是否应考虑下游任务的域？与下游任务域更接近的合成数据，是不是比来自相关性较弱域的「自然」数据更好的预训练选择？

作为回答这些问题的第一步，我们精心挑选了一组预训练数据集和下游任务。我们选取的预训练数据集在文本域和视觉域上与下游任务有不同程度的相似性。然后，我们尝试通过拉近预训练数据集与下游任务的域来提高下游任务的准确性。我们通过生成一个域上更接近下游任务的合成数据集来实现这一点。有趣的是，我们的合成数据集在下游任务上的表现，优于一个域匹配度更差的、更「自然」的常用数据集。

**为什么重要：**视觉与语言交叉处的多模态理解问题，对从帮助视障人士、构建虚拟助手到检测仇恨内容等一系列应用都很重要。Facebook AI 正在多模态理解、视觉与语言、自监督学习等广泛相关的方向上开展研究。例如，我们最近发布了 Hateful Memes 数据集与挑战赛，以推动多模态仇恨言论检测的进展。除了分享 Hateful Memes 的基准数据，我们还通过多模态框架 MMF 发布了模型代码。本文讨论的视觉—语言预训练方法可以帮助研究者为此类任务开发更有效的模型。我们使用合成生成数据集的成功也很重要，因为它有望帮助研究者克服大规模成对标注数据集的稀缺——这类数据集用于预训练视觉—语言表示。这对低资源应用和可用训练数据有限的任务尤其有帮助，还可用于增强现有数据集。

阅读完整论文：https://arxiv.org/abs/2004.08744

**作者**

- Amanpreet Singh，软件工程师
- Vedanuj Goswami，软件工程师
- Devi Parikh，研究科学家

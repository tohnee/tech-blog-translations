---
title: "MMF 发布：面向多模态 AI 模型的框架"
title_en: "Announcing MMF: A framework for multimodal AI models"
date: 2020-06-11
source: http://ai.facebook.com/blog/announcing-mmf-a-framework-for-multimodal-ai-models
crawled: 2026-09-22
translated: 2026-09-22
---

# MMF 发布：面向多模态 AI 模型的框架

> 原文：[Announcing MMF: A framework for multimodal AI models](http://ai.facebook.com/blog/announcing-mmf-a-framework-for-multimodal-ai-models) · Meta AI（Wayback 存档）

2020 年 6 月 11 日

Pythia——我们面向视觉与语言多模态研究的开源模块化深度学习框架——现更名为 multimodal framework（MMF）。作为此次变更的一部分，我们重写了库的大部分内容，以改善开源社区的使用体验，并新增了视觉与语言领域多项最先进的模型和数据集。MMF 为多个多模态挑战赛提供了起始代码，包括 Hateful Memes、VQA、TextVQA 和 TextCaps 挑战赛。更多信息请见 MMF 官网和 GitHub。

新特性包括性能与用户体验改进、新的基于 BERT 的最先进多模态模型、新的视觉与语言多模态模型、预训练模型库（model zoo）、自动下载，以及基于 OmegaConf 重新打造的配置系统。重写整个库使我们能够让它高度模块化，研究者可以轻松引入 MMF 的各个独立组件。

MMF 旨在帮助研究者开发能将多种理解综合为更基于情境的多模态理解的自适应 AI。这项工作对机器而言极具挑战，因为机器无法把文本和图像分开分析，必须组合这些不同模态，并理解它们放在一起呈现时意义如何变化。

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

本月早些时候，我们通过 MMF 为近期的 Hateful Memes 挑战赛——由 DrivenData 承办的首创性线上竞赛——提供了起始代码和基线。作为该挑战赛的一部分，我们还分享了一个新数据集，专门帮助 AI 研究者开发识别多模态仇恨言论的新系统。除了这次开源发布，我们还计划持续添加工具、任务、数据集和参考模型。我们期待看到开源社区如何使用并为 MMF 做出贡献。

阅读更多关于 MMF 的内容

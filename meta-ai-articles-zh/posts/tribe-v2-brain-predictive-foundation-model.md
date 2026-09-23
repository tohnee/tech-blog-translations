---
title: "介绍 TRIBE v2：一个训练用于理解人脑如何处理复杂刺激的预测性基础模型"
title_en: "Introducing TRIBE v2: A Predictive Foundation Model Trained to Understand How the Human Brain Processes Complex Stimuli"
date: 2026-03-26
source: https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model
crawled: 2026-09-22
translated: 2026-09-22
---

# 介绍 TRIBE v2：一个训练用于理解人脑如何处理复杂刺激的预测性基础模型

> 原文：[Introducing TRIBE v2: A Predictive Foundation Model Trained to Understand How the Human Brain Processes Complex Stimuli](https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model) · Meta AI（Wayback 存档）

2026 年 3 月 26 日 · 2 分钟阅读

**要点**

- 我们正在介绍 TRIBE v2——我们的下一代模型，充当人类神经活动的数字孪生。与同类模型相比，它在预测大脑对几乎任何图像或声音的反应时，提供了前所未有的速度、准确度以及 70 倍的分辨率提升——让神经科学家和临床研究者无需人类受试者即可检验理论。
- 我们正在发布模型、代码库、论文和交互式 demo，帮助研究者拓展神经科学的边界、把大脑洞察应用于构建更好的 AI 系统，并利用计算模拟加速神经系统疾病治疗方面的突破。

理解人脑如何处理周围世界，是神经科学最大的开放挑战之一。这一领域的突破可以变革我们理解和治疗影响数亿人的神经系统疾病的方式，并通过直接以神经科学原理指导 AI 系统的开发来改进它们。

今天，我们宣布 TRIBE v2：我们首个针对人类大脑对图像、声音和语言响应的 AI 模型。在我们获得 Algonauts 2025 奖的模型（基于四名个体的低分辨率 fMRI 记录训练）基础上，我们利用了一个超过 700 名健康志愿者的大规模数据集——这些志愿者观看了多种多样的媒体内容，包括图像、播客、视频和文本。TRIBE v2 能可靠地预测高分辨率 fMRI 大脑活动——支持对新的受试者、语言和任务的零样本预测——并持续优于标准建模方法。

通过创建人脑的数字模型，研究者可以快速检验关于大脑底层功能的假设，而无需在每项实验中都使用人类受试者。为了加速神经科学发现的步伐并为临床实践开辟新途径，我们以 CC BY-NC 许可证分享研究论文以及模型权重和代码。我们也邀请所有人在我们的 demo 网站上体验 TRIBE v2。通过分享这项工作，我们希望助力加速神经科学研究，为更大的福祉解锁科学与临床突破。

体验 demo | 阅读论文 | 下载代码 | 下载模型

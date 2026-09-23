---
title: "SEER：迈向对每个人都有效的 AI 的重要一步"
title_en: "SEER: An important step toward AI that works well for everyone"
date: 2021-04-26
source: https://ai.facebook.com/blog/seer-an-important-step-toward-ai-that-works-well-for-everyone
crawled: 2026-09-22
translated: 2026-09-22
---

# SEER：迈向对每个人都有效的 AI 的重要一步

> 原文：[SEER: An important step toward AI that works well for everyone](https://ai.facebook.com/blog/seer-an-important-step-toward-ai-that-works-well-for-everyone) · Meta AI（Wayback 存档）

2021 年 4 月 26 日

用经过整理和标注的数据集训练 AI 系统，已经催生出在物体识别等任务上表现出色的专业化 AI 模型。但仅依赖这一方法也存在切实的局限，其中包括一个我们认为尤其需要解决的问题：这类系统可能难以识别那些对数十亿人的日常生活很常见、但在训练 AI 系统常用的数据中代表性不足的物体。特别是，关于用哪些图像训练以及如何标注它们所做出的选择，可能无意中引入偏见。例如，一个主要用美国和欧洲家庭图像训练的物体识别系统，在被要求识别尼泊尔一个家中的物体时，可能难以有同样好的表现。这正是我们对 SEER——我们新开发的高性能计算机视觉系统——感到兴奋的原因之一。通过利用自监督学习，SEER 可以从任意数字图像集合中学习，而不需要研究者去整理集合并标注每个物体。初步评估显示，在识别那些虽然代表数十亿人生活、但在用于训练 AI 系统的传统图像数据集中代表性不足的物体时，SEER 能够超越传统计算机视觉系统。我们希望我们在 SEER 上的工作能帮助 AI 对每个人都更好用，而不仅仅是让那些通常受益最多的人受益。

## 用来自全球不同地区的图像测试 AI

我们在 Dollar Street 数据集上测试了 SEER——该数据集也是我们 2019 年计算机视觉系统偏见研究所使用的。SEER 的结果显示出令人振奋的迹象：自监督学习可以让 AI 对世界各地的人们都更好地工作。例如，SEER 正确识别了这张来自尼泊尔一个家庭的图像中的物体，而传统系统没有。点击照片上的滑块可以比较两者的预测（按概率从高到低排列）。照片：Luc Forsyth 为 Dollar Street 拍摄，2015（CC BY 4.0 许可下可自由使用）

在这张来自中国一个家庭的照片中，SEER 正确识别出一个炉灶，而传统训练的系统没有。点击照片上的滑块可以比较它们的预测（同样按概率从高到低排列）。照片：Jianxing Cheng 为 Dollar Street 拍摄，2016（CC BY 4.0 许可下可自由使用）

这张照片展示的是印度的一条小街。点击照片上的滑块可以比较 SEER 与传统物体识别系统的预测（同样按概率从高到低排列）。照片：Zoriah Miller 为 Dollar Street 拍摄，2015（CC BY 4.0 许可下可自由使用）

## 迈向平等服务于每个人的 AI

自监督学习此前已在提升那些没有大量数字化文本可用作标注训练数据的语言和方言的性能上展现出巨大潜力。SEER 在上述例子中更好的物体识别能力是另一个激动人心的成果，因为该模型是在随机互联网图像上训练的，没有任何数据整理。这表明训练 SEER 所用的自监督方法，可能对构建有效服务全世界（而不仅仅是富裕人群）的 AI 系统的努力产生巨大影响。这些努力只是开始，但很显然我们正走在一条极其激动人心的进步之路上。

**作者**
Priya Goyal，技术负责人

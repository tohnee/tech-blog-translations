---
title: "衡量通往 AGI 的进程：一个认知框架"
title_en: "Measuring progress toward AGI: A cognitive framework"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/
site: google-blog
date: 2026-03-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 衡量通往 AGI 的进程：一个认知框架

> 原文：[Measuring progress toward AGI: A cognitive framework](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/) · Google

通用人工智能（AGI）有潜力加速科学发现，并帮助解决人类最紧迫的一些问题。但我们很难知道自己距离这一关键里程碑还有多远，因为目前缺乏评估系统通用智能的实证工具。追踪通往 AGI 的进程需要多种多样的方法与路径，我们相信认知科学为解开这道难题提供了重要的一块拼图。

正因如此，今天我们发布新论文《[Measuring Progress Toward AGI: A Cognitive Taxonomy](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf)》，为理解 AI 系统的认知能力提供一个科学基础。

与论文一同发布的，还有我们与 Kaggle 合作启动的[黑客马拉松](http://kaggle.com/competitions/kaggle-measuring-agi)，邀请研究社区帮助构建将这一框架付诸实践所需的评测。

## 解构通用智能

我们的框架借鉴了心理学、神经科学和认知科学数十年的研究，构建了一个认知分类法（cognitive taxonomy）。它识别出 10 项我们假设对 AI 系统的通用智能至关重要的核心认知能力：

1. **感知（Perception）**：从环境中提取并处理感官信息
2. **生成（Generation）**：产出文本、语音和动作等输出
3. **注意（Attention）**：将认知资源聚焦于重要的事物
4. **学习（Learning）**：通过经验与教导获取新知识
5. **记忆（Memory）**：跨时间存储与提取信息
6. **推理（Reasoning）**：通过逻辑推断得出有效结论
7. **元认知（Metacognition）**：对自身认知过程的认知与监控
8. **执行功能（Executive functions）**：计划、抑制与认知灵活性
9. **问题解决（Problem solving）**：为特定领域的问题寻找有效的解决方案
10. **社会认知（Social cognition）**：处理和解读社会信息，并在社交情境中做出恰当回应

![所有气泡都连接到中央的「认知能力（Cognitive faculties）」气泡。每个气泡列出一种认知能力。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agi_cognition_framework_blog_inl.width-1200.format-webp.webp)

为了理解 AI 在这些认知能力上的表现，我们提出一个三阶段评测协议，以人类能力为参照对系统表现进行基准测试：

1. 在覆盖每种能力的广泛认知任务套件上评估 AI 系统，并使用留出测试集（held-out test sets）防止数据污染
2. 从具有人口统计学代表性的成年人样本中，为相同的任务收集人类基线
3. 将每个 AI 系统的表现映射到每种能力上的人类表现分布之中

## 从理论走向实践

定义这些认知能力是关键的第一步，但要衡量进程，我们需要的不仅仅是一个框架。为了把这套理论付诸实践，我们正在启动一个新的 Kaggle 黑客马拉松——「[Measuring progress toward AGI: Cognitive abilities](http://kaggle.com/competitions/kaggle-measuring-agi)」。该黑客马拉松鼓励社区为评测差距最大的五种认知能力设计评测：学习、元认知、注意、执行功能和社会认知。

参赛者可以使用 Kaggle 新推出的 [Community Benchmarks](https://blog.google/innovation-and-ai/technology/developers-tools/kaggle-community-benchmarks/) 平台，针对一系列前沿模型构建并测试自己的评测。

我们提供总计 20 万美元的奖金池：五个赛道各设两个最高分提交作品奖，每个 1 万美元；另设四个 2.5 万美元大奖，颁给绝对最佳的整体提交作品。提交时间为 3 月 17 日至 4 月 16 日，结果将于 6 月 1 日公布。欢迎前往 [Kaggle 网站](http://kaggle.com/competitions/kaggle-measuring-agi)开始构建。

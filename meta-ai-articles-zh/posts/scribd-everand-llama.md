---
title: "用基于 Llama 的助手找到下一本完美读物"
title_en: "Finding the perfect book to read next with a Llama-based assistant"
date: 2024-12-20
source: https://ai.meta.com/blog/scribd-everand-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# 用基于 Llama 的助手找到下一本完美读物

> 原文：[Finding the perfect book to read next with a Llama-based assistant](https://ai.meta.com/blog/scribd-everand-llama) · Meta AI（Wayback 存档）

2024 年 12 月 20 日 · 3 分钟阅读

Scribd, Inc. 旗下的 Everand 阅读服务拥有一个包含数百万本电子书、有声书等内容的全球图书馆。为了让 Everand 的 AI 内容发现助手 Ask AI 升级到最新版本，Scribd, Inc. 设想了一种将 Everand 复杂的书目目录与对每位顾客的细致理解相结合的发现体验。团队使用了三个 Llama 模型来打造全新的 Ask AI：Llama 3.1 8B、70B 和 405B。除了打造一个直观且知识渊博的智能体（agentic）之外，团队还致力于优化性能并控制每类工作负载的成本。

「Llama 的开源特性让我们能够始终站在创新的前沿，快速调整模型以改进内容推荐，」Scribd, Inc. 高级机器学习工程师 Prabdheep Cheema 说，「对于像我们这样的公司来说，开源模型提供了灵活性，并支持快速实验来满足用户需求。」

在 Scribd, Inc. 引入 AI 之前，在 Everand 上查找某个书名或主题主要依赖关键词搜索。Scribd, Inc. 各品牌的内容总量超过 1.95 亿件，该服务每月 2 亿独立访客可以浏览推荐内容，但这些建议基于预先生成的主题，顾客无法更改。这使得查找特定内容、发现感兴趣的新书变得困难。

## 打造神奇的内容体验

借助全新的 Ask AI，Everand 顾客可以探索极其广泛的主题，并提出冷门问题，例如「古代武术技法是如何出现在现代爱情故事中的？」

「打造神奇的内容体验是最重要的因素，」Scribd, Inc. 生成式 AI 产品高级总监 Steve Neola 说。Llama 之所以脱颖而出，是因为它能够出色地理解用户的意图并快速给出准确的结果。

全新的 Ask AI 将发现体验扩展到了特定书名搜索之外。该服务核心处经过重新训练的 Llama 3.1 8B 模型对顾客意图和 Everand 图书馆有着细致入微的理解，能够基于情节类型、背景设定、题材以及用户喜欢的其他图书生成直观的推荐。

## 让 Llama 模型投入工作

为了开发新版本，团队使用 Llama 3.1 405B 为训练数据集创建合成数据，模拟了各种各样的消费者行为。借助 QLoRA/LoRA 的参数高效微调（PEFT）与有监督微调，Scribd, Inc. 得以打造出一个高度精确、高度定制化的 Llama 3.1 8B 版本。由于 Llama 是开源的，团队能够突破闭源模型的限制，实现更深度的定制。

重新训练后的模型能够准确识别顾客意图——包括理解不常见的问题——将顾客引导到最适合其请求的服务。微调 Llama 3.1 8B 帮助团队在 Ask AI 功能的实时组件上以极低延迟交付更好的结果，同时控制了模型的占用空间和计算需求。随着越来越多的图书出版并进入 Everand 图书馆，Llama 3.1 70B 会在后台为每件内容生成元数据，以改进发现效果和准确性。

Llama 灵活的部署选项也让团队能够在不对基础设施做任何重大改动的情况下，将模型集成到 Ask AI 助手的工作流中。Scribd, Inc. 使用 Amazon Web Services（AWS）和 Databricks 批量推理来分析海量数据并支持方案开发。该应用以 JSON 格式交付模型的结构化输出，以改进元数据提取并确保高质量的实时响应。

Scribd, Inc. 表示，随着时间推移，Ask AI 将成长为一个更高层次的发现智能体，有能力增强顾客留存、提升忠诚度，并为读者创造更高的终身价值。展望未来，Scribd, Inc. 计划将 Llama 集成到用户体验的更多领域中，并借助 Llama Guard 3 获得额外的内容信任与审核支持。

## 分享你的 Llama 故事

我们最新的动态会直接送达你的收件箱。订阅我们的新闻邮件，随时了解 Meta AI 的新闻、活动、研究突破等内容。与我们一起探索 AI 的无限可能。查看所有空缺职位

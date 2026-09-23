---
title: "NVIDIA 如何用结构化权重剪枝与知识蒸馏构建新的 Llama 模型"
title_en: "How NVIDIA is using structured weight pruning and knowledge distillation to build new Llama models"
date: 2024-08-14
source: https://ai.meta.com/blog/nvidia-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# NVIDIA 如何用结构化权重剪枝与知识蒸馏构建新的 Llama 模型

> 原文：[How NVIDIA is using structured weight pruning and knowledge distillation to build new Llama models](https://ai.meta.com/blog/nvidia-llama) · Meta AI（Wayback 存档）

像 Llama 这样的大语言模型，能够以惊人的速度和精度处理各种具有挑战性的任务，例如生成代码、解决数学问题，以及帮助医生做出挽救生命的医疗决策。开源模型已经在各学科带来不可思议的突破——然而它们的部署资源消耗很大。全行业协同努力、让人们更轻松地利用大语言模型的变革性潜力，这一点很重要。

上个月，我们发布了 Llama 3.1，包括我们迄今最大的模型 405B，以及参数量分别为 700 亿和 80 亿的两个较小模型。由较大模型派生的小模型通常更便宜、便于大规模部署，且在许多语言任务上表现良好。在一篇新研究论文中，我们的合作伙伴 NVIDIA 探索了如何用结构化权重剪枝和知识蒸馏把各种大模型变小——无需从头训练新模型。团队以 Llama 3.1 8B 为基础，分享了它如何创建 Llama-Minitron 3.1 4B——这是其在 Llama 3.1 开源家族中的第一项工作。阅读 NVIDIA 的博客文章，了解更多关于这项工作的信息，并获取剪枝与蒸馏策略及其他资源。

---
title: "PPL Bench：为概率编程语言基准测试建立标准"
title_en: "PPL Bench: Creating a standard for benchmarking probabilistic programming languages"
date: 2020-10-22
source: https://ai.facebook.com/blog/ppl-bench-creating-a-standard-for-benchmarking-probabilistic-programming-languages
crawled: 2026-09-22
translated: 2026-09-22
---

# PPL Bench：为概率编程语言基准测试建立标准

> 原文：[PPL Bench: Creating a standard for benchmarking probabilistic programming languages](https://ai.facebook.com/blog/ppl-bench-creating-a-standard-for-benchmarking-probabilistic-programming-languages) · Meta AI（Wayback 存档）

**新内容：**PPL Bench 是一个开源基准测试框架，用于评估统计建模所用的概率编程语言（PPL）。研究人员可以用 PPL Bench 构建自己的参考实现（已内置多种 PPL），并对它们进行同等条件的横向比较。它旨在为研究人员提供评估 PPL 改进的标准，并帮助研究人员和工程师为自己的应用选择最合适的 PPL。

**它是什么：**PPL 允许统计学家用形式化语言编写概率模型。大约在过去二十年间，研究人员和数据科学家可用的 PPL 数量爆发式增长，但每一种都各有利弊。一些 PPL 限制其能处理的模型范围，另一些则是通用语言，即支持任何可计算的概率分布。取决于性能需求，某些 PPL 比其他的更适合不同用例，这意味着 PPL 社区需要一个标准的基准测试流程来衡量推断性能。PPL Bench 通过使用预测对数似然作为标准度量做到了这一点。我们相信，无论引擎或模型表示如何，这是在所有类型的 PPL 之间衡量推断准确率和收敛速率最统一的方式。PPL Bench 还报告其他常用于评估统计模型的指标，包括有效样本量、R-hat 和推断时间。

**为什么重要：**作为 PPL 研究社区的一员，我们相信一个标准化的 PPL 比较机制将加速更好、更快的概率建模编程语言的开发。我们希望社区贡献能帮助 PPL Bench 成长和多样化，并鼓励 PPL 在工业界更广泛地部署。

**阅读完整论文：**PPL Bench: Evaluation framework for probabilistic programming languages

**GitHub 获取地址：**PPL Bench

**作者**

- Bradford Cottel，技术项目经理
- Kinjal Shah，软件工程师
- Nimar Arora，研究科学家

---
title: "BrowseComp：一个简单却极具挑战性的基准测试，用于衡量智能体浏览网页的能力"
title_en: "BrowseComp: a simple yet challenging benchmark for measuring the ability for agents to browse the web"
source: https://openai.com/index/browsecomp/
crawled: 2026-09-13
category: research
translated: 2026-09-13
---

# BrowseComp：一个简单却极具挑战性的基准测试，用于衡量智能体浏览网页的能力

> 原文：[BrowseComp: a simple yet challenging benchmark for measuring the ability for agents to browse the web](https://openai.com/index/browsecomp/) · OpenAI 博客

深度研究（deep research）是 AI 系统的一项新能力，涉及搜索网页、综合多个来源的信息，并撰写带有引用的长篇报告。为了衡量这一能力的进展，我们构建了 BrowseComp（Browsing Competence 的缩写）：一个评估起来很简单、却极难解决的基准测试，由 1,266 个问题组成，其答案需要坚持不解的多步骤网页浏览。

## 我们为什么构建 BrowseComp

现有的问答基准测试已大抵饱和：前沿模型能答对其中的大多数问题，而且常常根本不需要浏览网页。我们需要一个真正必须进行网页浏览的基准测试，其问题即便对拥有搜索能力的系统来说依然困难。

BrowseComp 的问题经过如下设计：

- 找到答案需要定位并整合散落在多个网页中的信息。
- 这些信息通常不会被索引，也不会通过搜索结果的链接直接呈现，这就要求智能体去挖掘一手来源。
- 验证很简单：每个问题都有一个简短、无歧义的答案（一个数字、日期、名字或短语），使自动评估十分容易。

每个问题都经过多轮人工审查，以确保答案可验证、问题表述严谨，并且解题确实需要浏览上的坚持与创造力。

## 是什么让 BrowseComp 如此困难

一道典型的 BrowseComp 问题表面上看很简单——"找出在 Z 年做了 Y 的那个 X 的名字"——但答案可能埋藏在一份存档的新闻报道、一个扫描版 PDF、一个区域性网站，或一个只有在查询恰当时才会浮现的数据库之中。解决这些问题要求智能体：

- 拟定许多搜索查询，并随着信息的积累调整策略。
- 阅读并综合一手来源的信息，而不只是搜索摘要。
- 在许多死胡同中坚持下来：所需的浏览操作平均次数很高，而且许多问题被刻意设计成只能通过间接路径才能找到。
- 维护候选答案，并与多个来源交叉核对。

**结果**

我们评测了一系列模型和智能体浏览系统。关键发现：

- 带浏览功能的 GPT-4o 只解出了不到 2% 的问题，尽管它在现有基准测试上表现出色。
- 带浏览功能的 o1 提升到约 9%。
- 我们的深度研究能力将推理与长时程的智能体浏览相结合，解出了约 51% 的问题——这是一个巨大的飞跃，但离全部解决还很远。
- 拥有网络访问权限的人类专家能解出大多数问题，但往往每个问题需要数小时；BrowseComp 的难度是有意设置在随意浏览所能达到的水平之上的。

这些结果揭示了一个更普遍的规律：构建起来很简单的基准测试，能够揭示表面表现相近的系统之间的巨大能力差距。

## 我们发布什么

我们正在发布 BrowseComp 数据集，包括：

- 完整的 1,266 个问题及其经过验证的答案。
- 我们的模型在问题样本上的推理轨迹（reasoning traces）与浏览轨迹，以帮助分析失败模式。
- 一个用于自动评估的评分执行框架（grading harness）。

我们希望 BrowseComp 能对构建智能体搜索系统的研究者有所帮助，也希望它所揭示的差距——介于今天可能做到的与专家级人类浏览所能达到的之间——能够迅速缩小。

**局限性**

BrowseComp 衡量的是坚持性与搜索技巧，而非深度研究的全部方面：它不测试写作质量、引用准确性或对主观判断的综合能力。我们也不声称这些问题代表了真实用户的提问；它们是刻意设计的对抗性问题。随着模型的进步，我们预期 BrowseComp 终将饱和，我们正在开发更难的后续版本。

## 引用

如在学术场合或书籍中引用，请按以下方式注明本文出处：

OpenAI, "BrowseComp: a simple yet challenging benchmark for measuring the ability for agents to browse the web", OpenAI, 2026.

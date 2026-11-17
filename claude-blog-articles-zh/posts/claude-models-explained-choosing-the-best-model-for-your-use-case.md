---
title: "Claude 模型详解：为你的使用场景选择最佳模型"
title_en: "Claude models explained: choosing the best model for your use case"
date: 2026-07-24
author: Michael Segner
source: https://claude.com/resources/articles/claude-models-explained-choosing-the-best-model-for-your-use-case
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude 模型详解：为你的使用场景选择最佳模型

> 原文：[Claude models explained: choosing the best model for your use case](https://claude.com/resources/articles/claude-models-explained-choosing-the-best-model-for-your-use-case) · Claude 博客

## **我们的建议：从最聪明的模型开始**

我们最常听到的问题之一就是"[针对这个工作负载，我该选哪个模型？](https://claude.dev/blog/which-claude-model-should-you-build-with/)"随着我们发布的模型类别和版本越来越多，答案也变得更需要细致分辨。

本文将涵盖这些细节，包括每一类模型的说明、选择模型时最该问的问题，以及其他最佳实践。

不过，暂且把那些细致分辨放在一边，我们的默认建议是：从最智能的、已正式可用的模型开始，再用 effort 等级（投入程度）来调节性能与成本。

更智能的模型往往每次任务的成本（[cost-per-task](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/)）更低，尤其是在较低的 effort 等级下——即使它的每 token 价格更高。这是因为能力更强的模型通常用更少的轮次和更少的思考时间就能把大多数任务做对。此外，从小模型起步还会让你更难区分"模型失败"和"配置失败"。

当然，当出现对延迟或成本更敏感的使用场景时，你可以测试低一档的模型，直到找到最合适的那个。

有些组织也可能选择从最具成本效益的模型起步，逐级上移，直到满足质量门槛。我们在关于模型选择的文档中收录了这两种方向性的做法（[链接](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)）。

## **Claude 模型家族**

Claude 模型家族是 Anthropic 的 AI 模型阵容——Fable、Opus、Sonnet 和 Haiku——它们在智能、速度与成本之间各有不同的平衡。选得好，意味着让模型与任务相匹配。

### **Mythos / Fable**

Mythos 是 Anthropic 能力最强的模型类别，在各领域都具备前沿能力。这一类模型尤其擅长编程、长时间运行的智能体任务，以及解决 AI 此前无法可靠处理的问题。

Mythos 类别以两种封装形式交付，底层是同一个模型。Claude **Mythos** 面向处理两用（dual-use）网络安全与生物学工作的[受信任组织](https://www.anthropic.com/glasswing)，而 Claude **Fable** 则附加了额外的安全防护，使该模型可安全地供公众使用。两者都需要[限制数据留存，以确保能被安全使用](https://privacy.claude.com/en/articles/15425996-data-retention-practices-for-covered-models)。

### **Opus**

Opus 是我们面向推理密集型（reasoning-intensive）企业任务的强力模型类别。Opus 模型在关键行业基准上持续位居领先模型之列，例如衡量知识工作的 GDPval-AA 和衡量智能体编程的 Terminal-Bench 2.1。

在 Opus 与 Fable 之间如何选择，表面上可能并不清晰，因为两者都擅长编程、长时间运行的智能体和知识工作。但在真实场景中，像 Fable 这样更大的模型往往表现出更多的智慧、创造力和写作能力，即使它在基准分数上与 Opus 这类模型相近。

一条通用的经验法则是：如果你的评测或内部测试显示 Opus 在某些任务上吃力，那么答案就是 Fable。如果 Opus 已经达到了质量门槛，那么它的速度与价格特性可能让它成为更好的选择。

### **Sonnet**

Sonnet 是我们面向日常任务的多用途模型类别。Sonnet 在性能、成本与速度之间取得平衡，适用于最广泛的通用场景，包括多智能体编排架构中高频调用的子智能体。

### **Haiku**

Haiku 是我们成本最低、速度最快的模型类别。Haiku 模型专为延迟和成本敏感的高频工作负载而设计。

## **如何为你的工作负载选出最佳的 Claude 模型**

我们的模型类别并不专门针对某一类工作。我们不会建议金融用这一类、科研用那一类。每一款 Claude 模型都被训练得能在编程、智能体任务和知识工作等领域表现出色。

各类模型之间的主要差别在于：它们能可靠承担的问题*有多难*，以及这种能力在价格和速度上要付出什么代价。选择模型时，请问自己：

**这个任务有多难？** 如果它通常耗时很长、涉及多个步骤，或者此前从未被解决，那就适合用能力更强的模型类别。

**对延迟的要求是什么？** 如果模型用于高频、面向客户的工作负载，那么 Sonnet 往往是最佳选择。

**有哪些访问限制？** Mythos 仅向参与 [Project Glasswing](https://www.anthropic.com/glasswing) 的组织开放。并非所有组织都会把所有模型类别开放给所有角色。

**单位经济性如何？** 生产量较大的场景可能更适合较低档的模型，尤其是当评测显示这些任务能被令人满意地完成时。各模型[按 token 定价不同](https://platform.claude.com/docs/en/about-claude/models/overview)，并且会根据自身能力和 effort 等级呈现不同的每任务成本。

effort 等级也会影响质量、速度与成本之间的平衡。更高档的模型配合更高的 effort，能提供最好的性能；而更高档的模型在较低 effort 下，有时比更小的模型更高效。

![](https://assets.claude.com/dfef391930320e0da39548b50d2b1e7b7ddfcd6c.png)

曲线仅作示意，并非由基准数据绘制。

![](https://assets.claude.com/8352a1d61d466c02e601b9d3cb8012cb75a676fb.png)

曲线仅作示意，并非由基准数据绘制。

了解更多，请阅读[《在 Claude Code 中选择 Claude 模型与 effort 等级》](https://claude.com/resources/articles/claude-model-and-effort-level-in-claude-code)。

## **用 advisor 策略组合各模型的长处**

[advisor 策略](https://claude.com/resources/articles/the-advisor-strategy)允许更快、成本更低的工作模型调用更智能的模型来检查自己的计划并评估自己的工作成果，从而提升表现。

这种方法只在需要时才给执行模型提供指导，能将表现提升相当可观的幅度。例如在 SWE-bench Pro 上，搭配 Fable 5 作为 advisor 的 Sonnet 5 得分与 Fable 5 相差不到 10%，而成本仅为整项任务全程使用 Fable 5 的 63%。

## **评测与基准如何帮助选型**

判断模型能力是否满足需求，有两种常见方式：使用标准基准测试，以及自定义评测。

基准测试是一组预先确定的任务或场景，通常针对某个特定领域，且答案已知。它们可以成为评估不同模型类别和不同厂商能力的有效方向性指引。挑战出现在评估强大的模型时——比如 Opus 和 Fable——它们几乎能解出测试中的所有题目（通常被称为"饱和"）。

在这种情况下，我们建议组织在真实工作负载上使用模型，或用自己的评测来测试它们，从而判断哪个模型才是正确选择。通常，评测是一组从生产环境中精心抽取的问题——包括当前工具力所不及的难题，成功标准则由你的团队定义。

![](https://assets.claude.com/322dd4e9db870a1f5b8c8935849bcf1164a90b56.png)

正是在这里，前沿模型的能力与创造力开始与同类拉开差距，也彼此分化。我们已就开发[自定义智能体评测](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)的最佳实践写过大量内容。

## **做出明智的选择**

AI 模型选型没有放之四海而皆准的方法，这也是我们提供多个模型类别的原因。归根结底，选择模型的最佳方式，是理解每一类模型的基本特性，并深入理解你自己的使用场景。这意味着要构建、维护并部署强有力的评测。

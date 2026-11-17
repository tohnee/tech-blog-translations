---
title: "Claude Managed Agents 新进展：dreaming、outcomes 与多智能体编排"
title_en: "New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration"
date: 2026-05-19
source: https://claude.com/resources/articles/new-in-claude-managed-agents
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Managed Agents 新进展：dreaming、outcomes 与多智能体编排

> 原文：[New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration](https://claude.com/resources/articles/new-in-claude-managed-agents) · Claude 博客

今天我们以研究预览形式在 [Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents)（托管智能体）中推出 dreaming。Dreaming 扩展了[记忆](https://claude.com/resources/articles/claude-managed-agents-memory)能力，通过回顾过往会话发现模式，帮助智能体自我改进。我们还向使用 Managed Agents 构建的开发者开放 outcomes、多智能体编排（multiagent orchestration）和 webhooks。这些更新合在一起，让智能体能够在极少人工引导下处理复杂任务。

## **用 dreaming 构建自我改进的智能体**

[Dreaming](https://platform.claude.com/docs/en/managed-agents/dreams) 是 Claude Managed Agents 中的一项定时流程，它回顾智能体会话和记忆存储，提取模式，并对记忆进行整理（curate），让智能体随时间不断改进。你可以决定要保留多少控制权：dreaming 可以自动更新记忆，也可以在你审查变更之后再生效。

![](https://assets.claude.com/a8c196506682d36e5adf571c13332dceb8243b1f.png)

Dreaming 能揭示单个智能体自己看不到的模式，包括反复出现的错误、智能体们逐渐趋同的工作流，以及团队内共享的偏好。它还会重构记忆结构，使其在演进过程中始终保持高信噪比。这对长周期运行的工作和多智能体编排尤其有用。

记忆与 dreaming 共同构成一套面向自我改进型智能体的健壮记忆系统。记忆让每个智能体*在工作过程中*记录所学内容；dreaming 则*在会话之间*提炼这些记忆，把跨智能体的共享经验汇聚起来，并保持其最新。

Dreaming 已在 Claude Platform 上的 Managed Agents 中提供；开发者可以在[此处申请访问权限](https://claude.com/form/claude-managed-agents)。

## **Outcomes：为智能体的工作定义质量标准**

使用 [outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes) 时，你写一份评分标准（rubric），描述成功是什么样子，智能体就会朝这个目标努力。一个独立的评分器（grader）在自己的上下文窗口中按你的标准评估输出，因此不受智能体自身推理的影响。当有不达标之处时，评分器会精确定位需要修改的地方，智能体再进行一轮尝试。

当智能体知道「好」是什么样子时，它们才能发挥出最好水平。例如：一个结构框架、一份演示标准，或一组必须满足的要求。有了 outcomes，智能体可以对照这个标准检查自己的工作并自我修正，直到输出足够好，而无需人工审阅每一次尝试。

Outcomes 对需要关注细节、覆盖要穷尽的任务尤其有用。它同样适用于主观质量，例如文案是否符合品牌语气、设计是否遵循视觉规范。在测试中，相比标准的提示循环，outcomes 将任务成功率最多提升了 10 个百分点，在最难的问题上收益最大。Outcomes 也提升了文件生成质量：在我们的内部基准测试中，docx 任务成功率提升 8.4%，pptx 提升 10.1%。

你现在还可以定义一个 outcome，让智能体自行运行，并在它完成时通过 [webhook](http://platform.claude.com/docs/en/managed-agents/webhooks) 收到通知。

## **多智能体编排：用多个智能体处理复杂任务**

当工作量超出单个智能体所能做好的范围时，[多智能体编排](https://platform.claude.com/docs/en/managed-agents/multi-agent)让一个主智能体（lead agent）把任务拆成若干块，分别委派给拥有各自模型、提示和工具的专家智能体。例如，主智能体可以主持一次排查，同时让多个子智能体分头深入部署历史、错误日志、指标和支持工单。

这些专家智能体在共享文件系统上并行工作，并把结果汇入主智能体的整体上下文。主智能体可以在工作流进行中随时与其他智能体再次沟通，因为事件是持久化的，每个智能体都记得自己做过什么。你还可以在 [Claude Console](https://platform.claude.com/) 中追踪每一步：哪个智能体做了什么、以什么顺序、为什么这么做，从而完全看清你的任务是如何被委派和执行的。

![](https://assets.claude.com/ee11ba25525a1b358935de9d9426a1f72df5314f.png)

## **团队在用它们构建什么**

各团队正在使用 dreaming、outcomes 和多智能体编排，交付能够自我验证工作、跨会话学习并并行处理复杂任务的智能体：

* [Harvey](https://www.harvey.ai/) 使用 Managed Agents 协调长篇起草和文档创建等复杂法律工作。借助 dreaming，他们的智能体能够记住跨会话学到的东西，包括文件类型的变通做法和特定工具的使用模式。在他们的测试中，任务完成率提升了约 6 倍。
* Netflix 的平台团队构建了一个分析智能体，处理来自不同来源、数百次构建产生的日志。当一次变更影响到数千个应用时，重要的是找出在众多应用中反复出现的问题。多智能体编排让该智能体并行分析各批次，只呈现出真正值得处理的模式。
* Every 旗下的 [Spiral](http://writewithspiral.com/) 正在用多智能体编排和 outcomes 支撑其新 API 与 CLI 背后的写作智能体。主智能体运行在 [Haiku](https://www.anthropic.com/claude/haiku) 上：它接收进来的请求，在需要时快速追问，然后把起草工作委派给运行在 [Opus](https://www.anthropic.com/claude/opus) 上的子智能体。当用户要求多份草稿时，子智能体并行运行。写作质量是 Spiral 的核心价值，因此他们用 outcomes 来把住这道关。每份草稿都会按一套评分标准打分，该标准由 Every 的编辑原则和用户的声音构成，二者都从记忆中提取。只有达标草稿才会被返回。
* [Wisedocs](https://www.wisedocs.ai/blogs/building-managed-agents-for-document-verification) 在 Managed Agents 上构建了一个文档质量检查智能体，用 outcomes 按内部指南为每次审阅评分。现在审阅速度提升了 50%，同时仍与团队的标准保持一致。

## **开始使用**

Dreaming 以研究预览形式提供；outcomes、多智能体编排与记忆作为 Managed Agents 的一部分，已进入公开测试版。要开始使用 dreaming，请在[此处申请访问权限](https://claude.com/form/claude-managed-agents)。查阅我们的[文档](https://platform.claude.com/docs/en/managed-agents/overview)了解更多，或前往 [Claude Console](https://platform.claude.com/) 部署你的第一个智能体。

---
title: "Cresta 如何把客户体验专长变成 Claude Agent SDK 上的智能体构建器"
title_en: "How Cresta turned CX expertise into an agent builder on the Claude Agent SDK"
date: 2026-10-05
source: https://claude.com/resources/articles/how-cresta-turned-cx-expertise-into-an-agent-builder-on-the-claude-agent-sdk
crawled: 2026-11-17
translated: 2026-11-17
---

# Cresta 如何把客户体验专长变成 Claude Agent SDK 上的智能体构建器

> 原文：[How Cresta turned CX expertise into an agent builder on the Claude Agent SDK](https://claude.com/resources/articles/how-cresta-turned-cx-expertise-into-an-agent-builder-on-the-claude-agent-sdk) · Claude 博客

看看 Cresta 如何在 Claude Agent SDK 上构建 Conductor——一个构建其他智能体的智能体——以及团队如何在每个新的 Claude 模型发布时对它进行评估。

*在我们的「初创公司如何用 Claude 构建产品」系列中，我们关注 AI 产品背后的决策。本文探讨 [Cresta](https://cresta.com/) 如何将其构建 AI 原生客户体验的专长，注入 [Conductor](https://cresta.com/blog/cresta-conductor-the-agent-for-ai-agent-development)——一个帮助开发者构建和改进其他智能体的智能体。*

| 快速概览 |
| --- |
| 名称 | Cresta |
| 成立时间 | 2017 |
| 首席执行官 | Ping Wu |
| 增长 | 融资超过 2.7 亿美元，ARR 超过 1 亿美元。帮助 United Airlines、CVS Health 和 Marriott 等组织交付卓越的客户体验 |

为客户体验（CX）用例构建企业级 AI 智能体，需要理解散落在大量客户交互中的上下文。例如，客户可能：

* 要求退款，却不说指的是哪笔购买；
* 在同一条消息里既报告账单问题，又报告登录问题；
* 在退货窗口关闭之后才申请退款。

要正确回应，智能体可能需要查询客户买了什么、退款政策、账户历史或支付状态。

Cresta 会大规模地接触这类交互。其平台驱动客户体验：AI 智能体自行处理对话，为并肩工作的人工坐席提供实时指导，并输出对话智能，让企业看清该在哪些方面改进。

构建和维护客户体验智能体，需要组织在运营要求上做出关键决策：智能体需要知道什么、必须访问哪些系统、其行为在哪些地方应保持灵活、在哪些地方应保持确定性。Cresta 希望让更多团队都能获得这种判断力，而不必每个人从零开始。

Conductor 正是这一想法的产物：一个自然语言智能体构建器，帮助团队把复杂的业务上下文变成可用于生产的智能体。用户描述自己想构建什么，Conductor 便引导工作从有据可依的蓝图，一路走到实现、评估与优化。

Cresta 最初用 Claude Sonnet 和 Claude Opus 构建了 Conductor 的早期版本，帮助内部团队支持客户部署。悬而未决的问题是：Cresta 能否把这套系统变成产品，让客户直接在平台*内部*构建智能体。

为了承担开放式的开发工作，Conductor 把 Claude Agent SDK 当作通用执行框架（general-purpose harness），用来收集上下文、使用工具、编写并运行代码，并根据结果做出调整。

“我们内部一直把 Claude Code 当作开发工具，因为它在构建智能体的软件开发环节非常有效，”Cresta Conductor 工程负责人 Renjie Li 说。“Claude Agent SDK 让我们能以编程方式使用同一套智能体开发框架。借助 Conductor，我们把它与 Cresta 深厚的对话智能、客户体验专长、评估体系和运行时连接起来，为用户提供我们从第一天起就希望拥有的智能体构建体验。”

Cresta 表示，在 Cresta 及其合作伙伴的早期用例中，Conductor 将初始部署时间缩短了大约一半。

![](https://assets.claude.com/d3e6b46a5afdbbb0de9809bf27193b2e583cb4be.png)

## **一个帮助构建下一个智能体的元智能体**

Conductor 是一个自我改进的元智能体，建立在客户体验智能体开发的既有最佳实践之上。随着团队用它构建和改进更多智能体，他们会沉淀自己验证过的模式、工作流和专家判断。这就形成了一个知识飞轮，让未来的开发更快、更一致。

上线之后，生产交互、工作流结果和反馈都会成为下一轮改进的新信号。

Conductor 帮助构建者把从一次智能体构建中学到的东西变成可复用的记忆产物（memory artifact），记录模式、业务规则和评估方法。随后他们可以把它作为技能（skill）分享给团队其他成员，让他人也能基于同样经过验证的实践来构建。

### **让重要决策变得更简单**

写第一个提示词，只是构建有用智能体的一部分。更难的决定之一是：对话在哪些地方应保持灵活，在哪些地方需要明确的业务规则和受控的工具行为。

“你不能太确定性，否则就会造出一棵巨大的决策树，试图穷举每一个可能的分支……但有些企业级关键工作流必须始终可靠运行，尤其是在风险容忍度很低的强监管行业，”Renjie 说。“Conductor 帮助发现并加固这些确定性需求和实现，同时保留足够的灵活性来改善整体体验。”

Conductor 借助历史对话帮助团队判断：哪些地方应保留人工在环，哪些地方可以给模型留出适应空间。边界一旦划定，开发者仍需针对这些确定性部分本应满足的要求进行测试，并在底层业务规则变化时更新这些测试。

## **Cresta 如何评估 Conductor**

Conductor 的衡量标准是它构建智能体的能力。为此，Cresta 让 Conductor 完成一组构建任务：

* 构建一个新智能体
* 为某个智能体编写测试用例
* 修改一个已存在的智能体
* 执行根因分析

完成任务并不是唯一标准。团队还会考察结果、Conductor 是如何达成结果的，以及过程中用了什么。

| 评估维度 | 回答的问题 |
| --- | --- |
| 结果 | Conductor 是否产出了所要求的、可用的产物？ |
| 执行路径 | 它是否使用了合适的工具和必需的上下文？ |
| 质量 | 结果与精选的参考结果相比如何？ |
| 资源消耗 | 该任务耗费了多少时间和模型用量？ |

这些任务同时充当安全网。每当新的 Claude 模型发布，或 Conductor 框架更新时，Cresta 都会重跑评估。它使用相同的任务和相同的评分，在任何人确认改动之前，找出哪些方面有所改进、哪些仍需完善。

![](https://assets.claude.com/143bea978f7e2b36bc434ba50a94c5707e2ac77d.png)![](https://assets.claude.com/ca86ab3aa537a03b22d7ebe65e64d764717443d0.png)![](https://assets.claude.com/d05fb8f0a249766b461668342d0091b0700d0cbb.png)

同一套评估纪律也内建在 Conductor 中，用户可以用它检查自己的智能体是否按预期运行。Conductor 会把构建阶段捕获的需求和边缘情况，转化为其评估模块中的测试。

这样一来，当策略、所连接的系统以及对话模式发生变化时，团队就能持续监控那些必须始终可靠运行的工作流。这为他们提供了一种实用方式：在业务变化时更新智能体，同时不损失已经加固过的工作流的可靠性。

## **在 Claude Agent SDK 上构建 Conductor**

Cresta 把 Conductor 设计为面向客户体验的智能体开发控制平面（control plane）。它汇集对话数据、领域专长和开发实践，并通过策略、可观测性、验证和反馈驱动的改进，来治理每一次智能体运行。

Claude Agent SDK 位于 Conductor 之下，作为通用执行框架。它负责收集上下文、调用工具、编写并运行代码；Conductor 则在其上叠加 Cresta 的客户体验工作流、工具和领域上下文。

团队围绕 Conductor 需要完成的工作来评估这套 SDK：多步骤任务、大量上下文、反复使用工具。评估范围涵盖数据隐私、租户架构、组织级密钥分发、控制措施，以及整个实现过程中的可观测性。

“Anthropic 为智能体软件开发提供了一个强大、通用的基础。这让我们能把工程投入放在 Cresta 能创造最持久客户价值的地方，”Cresta 工程副总裁 Xiangru Chen 说。

## **把 Cresta 的工程专长直接交到客户手中**

Conductor 最初诞生于 Cresta 内部，帮助其自己的前置部署团队弄清楚：哪些开发任务可以变成可复用的流程、上下文在何处最关键、构建者在过程中需要检查什么。它在这项内部工作中的成功，给了团队信心，把同样的能力带给客户和合作伙伴。

对于任何产品部署定制智能体的速度快于工程师手写速度的团队来说，Cresta 的做法都是一个有用的参照：无论是智能体还是元智能体，最初构建之后的工作往往才是最难的。

了解 [Conductor](https://cresta.com/blog/cresta-conductor-the-agent-for-ai-agent-development) 如何把业务上下文转化为更好的智能体设计、实现和持续改进。

| Cresta 团队的最佳实践 |
| --- |
| 内部先用自家产品 | Conductor 先作为内部工具运行，直到其产出与一位具备深厚 AI 专长的工程师所能构建的成果相匹配，才成为产品。 |
| 聚焦你独有的优势 | Cresta 在只有自己能带来的专长（他们的对话数据和对客户体验的理解）与可以直接从 Agent SDK 取用的能力之间划了一条硬线，并拒绝构建任何落在错误一侧的东西。 |
| 智能体的哪些部分需要是确定性的 | 加固那些绝不能出错的企业级关键工作流，其余部分保持灵活，否则你就得不到想要的交互式智能体体验。 |
| 上线只是容易的那部分 | 最初的构建只占约 20% 的工作量，另外 80% 是随后的测试、优化和持续改进，因此要围绕迭代循环而不是上线来设计你的工具链。 |

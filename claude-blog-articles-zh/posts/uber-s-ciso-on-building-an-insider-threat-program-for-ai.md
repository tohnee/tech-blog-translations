---
title: "Uber 首席信息安全官谈如何为 AI 构建内部威胁计划"
title_en: "Uber's CISO on building an insider threat program for AI"
date: 2026-10-13
source: https://claude.com/resources/articles/uber-s-ciso-on-building-an-insider-threat-program-for-ai
crawled: 2026-11-17
translated: 2026-11-17
---

# Uber 首席信息安全官谈如何为 AI 构建内部威胁计划

> 原文：[Uber's CISO on building an insider threat program for AI](https://claude.com/resources/articles/uber-s-ciso-on-building-an-insider-threat-program-for-ai) · Claude 博客

*Uber 首席信息安全官 Philip Martin 谈为 AI 智能体建立监控与可观测性的重要性，以及 Uber 的开源工具如何与 Enterprise Frontier Safeguards 协同工作。*

Uber 运营着全球最大的实时市场之一，每天处理超过 4,000 万次行程与配送订单。Uber 首席信息安全官（CISO）Philip Martin 带领的团队负责保护 Uber 的数据，以及在现实世界中使用该平台的乘客、司机和骑手。他的团队早在 Claude Code 问世之前就开始用 Claude 做威胁建模，当时还需要手工拼装上下文。如今，借助 Claude Fable，Claude 可以自行从代码、设计文档和工单历史中收集这些上下文。

[](https://assets.claude.com/f2bc047aa4369aea3fde5d2e73ed2c09c4fb8fdc.mp4)

Martin 认为，AI 智能体需要一套与企业现有员工内部威胁计划相同的机制。我们与他聊了这个想法、他为何如此关注意外误用，以及 Uber 的开源监控工具如何与 Enterprise Frontier Safeguards 配合。

**前沿模型正在如何改变你们安全团队的工作？**

以往模型与今天的前沿模型之间最大的区别，在于它们能够在长时间跨度内纳入更多上下文，并由此生成非常具体的输出。当我们为某个服务应用做安全审查或威胁建模时，可以让模型读取关于该服务的多得多的上下文——无论是代码本身、设计文档、Jira 中的 issue，还是关于该服务应做什么、与哪些系统交互的历史背景。

在智能体团队上，我也看到同样的趋势正在出现。我可以想象一个不远的未来：每个服务都配备一个非常了解该服务的智能体，这些智能体可以像生产环境中的服务那样相互对话，讨论威胁模型：这是我的威胁模型，这是我的数据来源。这种“智能体团队”效应会把我们的效率带到下一个层次。

**Uber 曾与我们的 Enterprise Frontier Safeguards 团队合作。这对 Uber 为什么重要？**

Anthropic 和 Uber 有一个共同点：都深入骨髓地重视安全，尽管所处语境截然不同。Uber 谈安全，谈的是乘客安全、个人数据保护。Anthropic 希望防止其前沿模型被滥用，而 Uber 需要保护客户数据、商业机密以及其他任何专有信息。Enterprise Frontier Safeguards 让我们得以取得这种平衡：保障措施到位，但未经我们许可，Anthropic 无法访问我们的数据。

它把数据控制权交给我们，也把风险缓解措施以及保障被触发后我们决定采取何种行动的控制权交给我们。我认为，我们共同肩负着一项责任：确保这些模型在世界上被安全、有效地使用。

当你们的团队向我们讲解设计方案时，能明显感觉到你们听取了我们的反馈。你们让我们坐在驾驶座上。这让我们既能保护数据，又能负责任地管理这些模型的能力。

**Enterprise Frontier Safeguards 与 Uber 已有的 AI 部署安全监控如何配合？**

从最开始，我们就围绕如何安全地在 Uber 内部署 AI 做了大量工作。我们最近开源了一款名为 [AI Detection and Response（ADR）（在新标签页中打开）](https://github.com/uber/ADR)的产品，旨在收集实时遥测数据，并在我们部署的智能体 harness 中实时采取行动。

它是对 Anthropic 保障措施的补充，因为我们现在能访问更丰富的数据，用来发现智能体何时越界，并实时响应。我们对自己这边的状况有独立视图，再加上 Anthropic 分类器的输出，两者都能接入我们整体的检测环境，很像传统网络安全的那套做法。核心在于有效拼装上下文，以尽可能快的速度、尽可能高的确定性做出决策。

我认为，我们会看到 Enterprise Frontier Safeguards 作为一种数据源接入 ADR。再加上我们的 LLM 网关——它构建了一道边界，控制 Uber 内部 AI 的使用方式——这些共同构成了我们整体的 AI 安全架构。

**就保障 AI 系统安全而言，你认为防御方接下来应优先关注什么？**

第一是实时检测与干预：尽可能贴近“人在 harness 中输入提示词”的那一刻，从而能够告诉他们：“你可能并不想这么做”，或者“这个模型即将调用的工具、即将连接的地方，可能并不是你希望发生的。”

第二是更好地理解新出现的模式。我们观察模型行为的趋势，发现我们此前不知道可能存在的全新行为。这会形成一个循环。我们查看数据——很多时候借助 LLM 的协助——在行为出现时发现它们，并把相应的保障措施构建回实时平台。随后，因为约束会催生新行为，又会有新行为出现，我们再去发现它们。

**对于那些对前沿模型所需监控心存犹豫的领导者，你想说什么？**

采用 AI 是商业上的必然要求。无论我们愿不愿意，它都在到来，并将为世界各地的企业和人们带来实实在在的好处。但同时也存在真实的潜在危害，而且随着模型能力增强、承担更复杂、更自主的工作，风险也在上升。

每家公司都已经为自己的员工运行着内部威胁计划。没有人会对此提出异议。我们接受有时颇为繁琐的数据留存要求，监控一些我们并不想监控的东西，因为我们知道，人会出于各种原因偶尔做出超出自身角色边界的行为。

前沿模型引入了同样的风险。这些模型可能被引导做出超出我们预期约束范围的行为。因此，我们需要为 AI 建立同等的能力。为模型设立的那套内部威胁计划，将是安全、稳妥地推广这些系统的关键。

*进一步了解 [Enterprise Frontier Safeguards（在新标签页中打开）](https://www.anthropic.com/news/enterprise-frontier-safeguards)。*

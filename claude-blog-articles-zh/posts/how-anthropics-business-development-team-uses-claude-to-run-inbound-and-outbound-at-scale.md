---
title: "Anthropic 业务拓展团队如何用 Claude 规模化运营入站线索与出站拓客"
title_en: "How Anthropic's business development team uses Claude to run inbound and outbound at scale"
date: 2026-08-07
author: John Albert
source: https://claude.com/resources/articles/how-anthropics-business-development-team-uses-claude-to-run-inbound-and-outbound-at-scale
crawled: 2026-11-17
translated: 2026-11-17
---

# Anthropic 业务拓展团队如何用 Claude 规模化运营入站线索与出站拓客

> 原文：[How Anthropic's business development team uses Claude to run inbound and outbound at scale](https://claude.com/resources/articles/how-anthropics-business-development-team-uses-claude-to-run-inbound-and-outbound-at-scale) · Claude 博客

*Anthropic 业务拓展代表 John Albert 分享他的团队如何用 Claude 研究客户名册、起草客户回复，并处理过去只能排队等数据团队的临时需求。*

我职业生涯早期做业务拓展时，客户经理会把包含数百家客户的名单交给我，我得逐家调查公司、找到对的人、挖出邮箱、起草外联内容。入站这一侧的工作流同样高度依赖人工、极其耗时。

去年夏天加入 Anthropic 时，我接手了管理销售收件箱的职责。除了管理自己负责的客户组合，我每天还要花大约 5 个小时人工回复潜在客户的入站咨询，常常是在回答关于我们产品的相同或相似问题。

如今，其中大量工作已经在 [Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) 中配置为 skills 与定时任务。个性化客户邮件会被准备成草稿，我只需审阅、调整后再发送。我的出站工作则从一份详尽的研究开始——这份研究不再需要我花几个小时去整理。

结果是，我和同事们花在手工重复工作上的时间更少，花在真正重要的事情上的时间更多：帮助我们的客户。

下面讲讲 Claude Cowork 如何提升 Anthropic 的业务拓展职能，让我们能把更多时间投入到战略性工作、理解客户问题，以及帮助客户了解 Claude 能如何解决这些问题。

## **自动化行政性与可重复任务**

BDR 处在销售流程的起点，负责甄别入站需求、为公司构建出站销售管道。在 Anthropic，这些动作如今会先经过 Claude Cowork。

我们入站体系的一个基础件是一份文档：我收集了销售收件箱里最常收到的问题，以及我们对这些问题的最佳答案。这份文档充当我们的销售知识库，Claude 在起草任何回复之前都会先读它。这份文档也是在 Claude 帮助下建成的（我只是把它指向相关的信息源）；现在它还会持续校验文档是否最新，标出可能已经过时的信息，由使用者确认。

建立在这份文档之上、负载最重的工作流是一个每小时运行的收件箱 skill：它扫描某位代表的收件箱，找出每一串需要该代表回复的线程，起草回复供其阅读、编辑并发送。这个 skill 由三部分组成：一份精简的系统提示词、作为上下文的知识库，以及该代表的写作风格画像（我们每个人也会用一个文风 skill 来生成它——那个 skill 会通读我们写过的文档、消息和邮件）。

![](https://assets.claude.com/1a738405809dbb5b81041ae63260632feed124db.png)

收件箱 skill 依赖一份精简的系统提示词、作为产品事实来源的团队销售知识库，以及为每位代表定制的文风画像。

![](https://assets.claude.com/4a5839915c64386cfa820e568caf757bd1c3522d.png)

收件箱 skill 扫描代表的收件箱，留下草稿回复供审阅。本预览中的所有信息均已为发布而匿名化处理。

我还会依赖两个较轻量的 skill 来处理行政工作。每个 BDR 都懂会议爽约和潜在客户失联的痛苦。为此，我构建了一个 skill 来盯住 Gmail 和 Google Calendar，一旦发生这种情况就通知我，让我能快速跟进。

另一个 skill 通过我们的 CRM 连接器扫描所有新线索，并起草个性化的首次触达内容。它全天按计划运行，确保我们不会让线索干等。

我们还有一个 skill 负责让 Salesforce 保持最新：它读取我们关于商机阶段的内部指引，并与 Gmail 和 Gong 中实际发生的情况比对。如果我们已经与客户见过面并进入价格问题，这个商机大概率该推进一个阶段。Claude 会为每条 Salesforce 更新附上依据并提出建议，然后等待批准。当我修改或驳回一条建议时，它会记录原因，避免重蹈覆辙。

![](https://assets.claude.com/f2c29cec44f8663d9bb00f388846400a7d1f53c5.png)

销售管道扫描 skill 提出 Salesforce 更新建议，由代表审批。此处展示的是演示数据，所有信息均已为发布而匿名化处理。

## **优化出站与营收工作**

我平均在任何时候都负责上百家客户。之所以能覆盖所有这些客户，靠的是一个在夜间作为定时任务运行的 skill。它会在我整个客户组合中拓客，观察每个客户的当前状态；比如，我们在和谁接触、他们目前如何使用 Claude、有哪些相关信号。为此，Claude 会连接 Salesforce、Apollo 和 Common Room 等销售工具、Gong 以及我们的数据仓库，执行深度研究，并对照团队整理出的出站指引和 ICP（理想客户画像）标准进行校验。

这些 skill 组件补充了上下文，让 Claude 的工作方式更接近 Anthropic 的 BDR。早上打开 Claude Cowork，我能看到每个客户的简报、评分和出站打法。

随着每位 BDR 都能对 Claude 的结果给出反馈、反馈再回流到 skill 中，这个工作流会越来越有用。该 skill 维护一个小型记忆文件与台账，避免重复或冗余的工作。

我们把这些研究用于后续对话，因此外联更有针对性；与客户交谈时，我们了解他们的业务，也足够贴近他们的问题，能够展开更深入的战略讨论。

需求探索电话是我们出站动作中另一块正在用 Claude 改进的部分。我们用一个 skill 对照需求探索电话手册评估 Gong 录音转写，为每次通话生成评分卡，并基于对话内容给出具体反馈。反馈包括：做得最好的三件事、最需改进的三个领域、按我们的标准给出的明确通过/不通过评分，以及下一步最该练习的一件最高杠杆的事。

![](https://assets.claude.com/9506ace15ed7c945f1fb71f4af45995528024911.png)

通话教练 skill 为我们的需求探索电话提供评分卡，并给出改进的具体建议。此处展示的是演示数据，所有信息均已为发布而匿名化处理。

## **精简一次性需求**

BDR 团队经常收到临时性需求，而 Claude 让我们能以更具战略性的方式与 AE（客户经理）协作。如果某位 AE 想了解某个头部客户的用量趋势，我们只需一句提示词，就能给出一份清晰易读、描述性强的仪表盘，突出相关趋势。

![](https://assets.claude.com/7319087ead08eda021ed8d1b911e880a15531cb2.png)

为目标客户生成的支出分析报告。

用 Claude 做数据分析与报告，在出站工作中同样派得上用场。我最喜欢的工作流之一，是运行一个“未发掘用量”提示。它会审视某位 AE 的整个客户组合，在账户层面找出那些有使用信号、但我们尚未建立销售商机的客户。这往往是一个很好的信号，提示我们该开始接触客户，与他们一起优化其 Claude 使用方式和体验。

![](https://assets.claude.com/ae33f6312f2086926039c7be80380081d705855a.png)

对某位 AE 客户组合做一次以产品为视角的扫描，会返回所有已经使用产品、却尚无对应商机的客户。此处展示的是演示数据，所有信息均已为发布而匿名化或修改。

我们也会用 Claude 做活动邀约。最近有位 AE 提到我们即将举办 [Claude Code for Data Engineering](https://claude.com/resources/webinars/claude-code-for-data-engineering) 网络研讨会，问我能否在他负责的客户组合里找出有兴趣参会的客户。我没有为此准备 skill，但这类需求一句提示词就够了。Claude 检查了整个组合中的用量数据与 CRM 历史，按我们的 ICP 给每个客户打分，并标出最匹配的客户以及值得邀请的联系人。

![](https://assets.claude.com/ec33abd421b4f2c528c84d923daf36240784608b.png)

当被要求找出适合受邀参会的客户时，Claude 横扫客户名册，并按团队的理想客户画像为每个客户打分。

这些 skill、定时任务，加上我们精心整理的上下文，共同把 Claude 变成了一位全天候的业务拓展伙伴。

> “支撑业务拓展报表的同一套受治理基础能力，在我们关于 Anthropic 如何用 Claude 实现自助式数据分析的文章中有详细描述。”

## **给业务拓展团队的 Claude Cowork 上手建议**

以下是一些给业务拓展团队的 Claude Cowork 上手建议：

* **先建知识库，再搭工作流。** 把团队反复回答的问题以及最佳答案汇集到一份对外文档中。你不必手写：把 Claude 指向相关的产品文档和团队频道，让它构建第一版。
* **给 Claude 提供团队工作方式的示例。** Claude 是依据你给的上下文来起草的。对出站工作而言，这可以包括成功消息的示例和你的理想客户画像。每位代表还可以让 Claude 学习自己的写作风格，这样草稿读起来就像本人写的。
* **每一次发送都保留人工把关。** Claude 可以生成草稿，但我们仍会阅读、编辑并发送。
* **在团队内共享 skill。** 我们团队把最常用的 skill 放在一个共享插件里；一旦确认代表们在日常工作中稳定使用某个 skill，就把它提升到那里。
* **让 skill 足够通用，以适配整个团队的工作方式。** 客户分层、客户组合和工作流因人而异，因此我们让共享 skill 保持足够通用、可适配，而不是只针对某个人的日常。
* **把反馈写回 skill 里。** 当你忽略一条 hook 提示或修正一份草稿时，让 Claude 把原因记录进 skill，避免它再犯同样的错误。

我最好的建议？直接开始试验。你给它的上下文和工具越多，它能替你完成的事就越多。

*欢迎观看 John 在 [Claude Cowork for Business Development Representatives](https://claude.com/resources/webinars/claude-for-business-development-representatives) 网络研讨会上的 skill 演示。*

*立即开始使用 [Claude Cowork](https://claude.com/product/cowork)。*

*本文所有界面示意图均使用合成数据，不代表任何真实公司或个人。*

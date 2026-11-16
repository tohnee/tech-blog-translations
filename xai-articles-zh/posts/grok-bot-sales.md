---
title: "你的下一位销售队友，应该是一名 Grok Bot"
title_en: "Your next sales teammate should be a Grok Bot"
date: 2026-10-27
source: https://x.ai/news/grok-bot-sales
crawled: 2026-11-16
translated: 2026-11-17
---

# 你的下一位销售队友，应该是一名 Grok Bot

> 原文：[Your next sales teammate should be a Grok Bot](https://x.ai/news/grok-bot-sales) · xAI

[返回新闻列表](/news)

2026 年 10 月 27 日

作者：Iris Wang、Joe Robertson、Micheal Sihavong、Palmi Angelova

SpaceXAI 销售团队为潜客开发、报价和交易评审打造了 Team Bot，让每位销售代表都能基于同一套最新的专业知识开展工作。

[下载 macOS 版](https://api2.cursor.sh/updates/download/stable/darwin-arm64/grok-bot-bd824e1890d8b96f)[联系销售](https://cursor.com/contact-sales?product=grok-bot)

SpaceXAI 销售团队最初采用 [Grok Bot](/bot) 时，销售代表们各自构建自己的 Bot，用来调研客户、准备会议和管理销售管道。这带来了一个机会：把每个人所做的最好的部分汇集起来，提供给整个团队。

我们开始创建 Team Bot，每个 Bot 专精于销售组织中已有的一个角色。最了解该岗位的人参与构建和维护这个 Bot，于是每个人都能受益于他们的专业经验，并基于同一套最新的业务知识开展工作。而且，当我们改进某个 Bot 时，所有使用者都会受益，无需各自更新自己的配置。

我们从三个 Team Bot 起步，每个负责交易周期中不同的环节。

* **Account Intel Bot** 帮助销售代表识别潜在客户、准备客户沟通，并让 Salesforce 保持最新。
* **Quote Bot** 使用 CPQ 工具生成定价方案并准备订单表。
* **Deal Bot** 帮助我们的 Deal Desk 团队评审非标准条款并审批交易。

每个 Bot 都为流程带来各自的专业能力，让我们可以把交易周期中更大的部分委派出去，同时让人专注于客户以及那些需要人来做判断的决策。

![SpaceXAI 销售团队如何用 Team Bot 自动化交易周期：Account Intel Bot 负责客户调研与跟进，Quote Bot 准备定价和订单表，Deal Bot 评审特殊条款与审批](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/sales-bot-diagram-light-6-b66d2e51.png)

![SpaceXAI 销售团队如何用 Team Bot 自动化交易周期：Account Intel Bot 负责客户调研与跟进，Quote Bot 准备定价和订单表，Deal Bot 评审特殊条款与审批](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/sales-bot-diagram-dark-6-5f6bb3a4.png)

## [我们如何看待 Team Bot](#how-we-think-about-team-bots)

Team Bot 是一种围绕超级智能组织工作的新方式。它们承担服务整个团队的明确角色，这要求我们审慎决定它们知道什么、能做什么，以及在何时需要人介入。

每个 Team Bot 都需要理解它所操作的系统，以及它遵循的业务规则。我们通过共享技能和连接内部权威数据源来赋予它们这些知识，让所有人遵循同一套最新规则。当流程发生变化，或我们找到更好的任务执行方式时，只需更新一次 Team Bot，所有人都会同步。

Team Bot 还需要对其行为设定边界。它们以每位用户自己的权限行事，对敏感操作还有额外限制。我们设置了速率限制，防止大规模的非预期改动，并把某些操作专门保留给特定的 Team Bot。例如，销售代表不能使用 Quote Bot 批准自己的折扣。

我们也为 Team Bot 何时可以独立行动划定了界限。目前，只要我们无法清晰定义某项决策的判断标准，或当 Team Bot 准备面向客户的沟通内容时，我们都会要求人工审核。随着我们衡量它们的工作质量、并对它们的决策建立信心，我们预期会赋予 Team Bot 更多责任。

## [Account Intel Bot 负责销售准备与跟进](#account-intel-bot-handles-sales-prep-and-follow-up)

我们的 Account Intel Bot 帮助销售代表识别有潜力的客户、准备会议并管理销售管道。每位代表都与同一个 Team Bot 进行私密对话，它调用公司共享知识，并以每位代表自己的权限行事。

我们的 GTM 工程团队一开始让 Grok Bot 分析 Salesforce 活动日志，找出最值得自动化的工作。分析显示，销售代表在客户通话后花了大量时间更新商机。于是我们给了 Account Intel 完成这些更新的工具，并教给它何时更新、如何更新的业务规则。

主动性是我们认为对 Team Bot 很重要的另一项原则。Account Intel 可以在客户会议前基于客户历史准备一份简报。会后，它可以读取 Gong 的通话转录，识别并完成必要的 Salesforce 更新，并草拟一封跟进邮件供代表审阅。

销售代表可以把这些工作流设置为自动运行，因此大量准备和跟进工作无需另行提出请求即可完成。

![Account Intel Bot 根据一次客户对话总结下一步行动，并更新 Salesforce 中的商机和客户计划](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/account-intel-01f2079e.png)

## [Quote Bot 生成报价和订单表](#quote-bot-generates-quotes-and-order-forms)

当销售代表准备与客户讨论价格时，一个名为 Quote Bot 的 Team Bot 便会接手。

销售代表可以请 Quote Bot 准备多个包含不同产品和折扣的方案。Quote Bot 把报价录入 Salesforce，并在 Grok Bot 应用中并排展示，这样代表无需进入 CPQ 工具，就能在选定方案前进行比较。

Quote Bot 还负责管理把报价转化为订单表所需的各个步骤。它提交报价进入审批流程、跟踪审批状态，并把例外情况转交给 Deal Bot（详见下文）。报价获批后，Quote Bot 可以在 Ironclad 中生成订单表、下载可签署的合同，并草拟一封邮件供代表发送给客户。代表可以在一段对话中完成这一流程的大部分工作，而不必在多个系统之间来回切换、等待其他团队更新状态。

我们构建 Quote Bot 来承担这些工作，同时不放弃对重要决策的控制。在改动 Salesforce 中的任何内容之前，它会向代表展示预览并请求确认。它也以代表本人的权限运行，因此需要 Deal Desk 权限的审批和例外处理仍归 Deal Desk 负责。

![Quote Bot 为同一客户并排展示三个 Salesforce 报价方案](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/grokbot_messagebuilder_wallpaper_2816x1832-e13f59e2.png)

## [Deal Bot 评审非标准条款与审批](#deal-bot-reviews-non-standard-terms-and-approvals)

当报价涉及特殊定价或非标准合同条款时，Quote Bot 会把工作交给 Deal Bot。这个 Team Bot 为我们的 Deal Desk 团队提供支持，后者负责评审例外情况，并决定企业愿意接受怎样的交易经济性与风险。

Deal Bot 会按照我们已批准的政策和合同措辞核查请求，然后准备推进交易所需的变更。它还可以监控并分诊销售代表在 Slack 中提交的请求，把请求转交给正确的跨职能负责人或审批人，并核查法务是否已经起草过类似条款。

![在移除营销措辞后，Deal Bot 与 Quote Bot 在 Slack 中协调修改订单表](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/slack-deal-2-1-f55e022f.png)

Deal Bot 拥有销售代表所不具备的权限，因此可以对报价做出需要 Deal Desk 权限的变更。对于需要人工判断的决策，它会准备一份建议，并在继续之前请 Deal Desk 专员批准。Deal Bot 处理大量例行流程，把需要商业专业知识和人工判断的决策留给 Deal Desk 团队。

![Deal Bot 请求 Deal Desk 专员批准将已获法务确认的措辞加入报价的特殊条款](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/slack-dealbot-2-1-6035cfbe.png)

Deal Bot 处理的每一次 Salesforce 审批都会在系统中留下记录，注明决策、决策依据，以及 Deal Bot 所支持的 DRI，以确保责任可追溯、流程可查，并符合公司政策。

## [迈向一支 AI 同事团队](#building-toward-a-team-of-ai-coworkers)

我们介绍的这三个 Bot 只是一支不断壮大的团队的一部分。我们还构建了 Competitive Intel Bot（保持我们的竞争情报最新，并帮助代表准备竞争性对话）和 Sales Training Bot（支持员工入职与技能发展）等 Team Bot。在整个销售组织里，人们还在为自己的工作构建和使用更多个人 Bot。

我们构建这套体系仍处于早期阶段。随着时间推移，我们预期 Team Bot 会承担更多职责，并在彼此之间协调更多工作。我们的目标是打造这样一个销售组织：人们可以专注于客户，而由最了解各岗位的人构建和维护的专业 Team Bot，则承担起支持他们的大量工作。

## 立即试用 Grok Bot

[下载 macOS 版](https://api2.cursor.sh/updates/download/stable/darwin-arm64/grok-bot-bd824e1890d8b96f)[联系销售](https://cursor.com/contact-sales?product=grok-bot)

【译者注：原文中公司名在 "SpaceXSI" 与 "SpaceX" 之间不一致，译文统一采用 "SpaceXAI"，与本目录既有译文保持一致。】

---
title: "让管理员对 Claude 支出拥有更强的可见性与控制力"
title_en: "Giving admins more visibility and control over Claude spend"
date: 2026-07-02
source: https://claude.com/resources/articles/giving-admins-more-visibility-and-control-over-claude-usage-and-spend
crawled: 2026-11-17
translated: 2026-11-17
---

# 让管理员对 Claude 支出拥有更强的可见性与控制力

> 原文：[Giving admins more visibility and control over Claude spend](https://claude.com/resources/articles/giving-admins-more-visibility-and-control-over-claude-usage-and-spend) · Claude 博客

面向 Claude Enterprise 的全新分析能力和成本控制现已可用。

我们为 [Claude Enterprise](https://claude.com/solutions/enterprise) 带来更丰富的管理员分析、模型级授权和支出提醒。随着 Claude 在整个组织中承担日益困难和复杂的智能体工作，其使用与成本模式已与标准聊天工具截然不同。这些控制项让管理员能够看清 Claude 是如何被使用的，并为他们提供管理成本的工具。

今天的这些新增功能建立在 Anthropic 已提供的控制手段之上：各层级的支出上限、访问与模型路由、带导出功能和分析 API 的使用分析仪表盘，以及投入程度控制。更丰富的分析和更精细的成本控制，是我们数月来持续构建的控制体系中最新加入的部分。

![](https://assets.claude.com/1ecfa597c6c46012e12defafc698a30b2f862634.png)

## 追踪采用情况与成本

面向管理员的[分析仪表盘](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans)现在可以按群组和按用户展示使用量与成本，并把创建的 Artifact、编辑的文件、使用过的技能和连接器等产出直接显示在其成本旁边。管理员可以按 IT 团队已在管理的 SCIM 群组进行筛选，因此细分维度与其既有组织结构保持一致。

Claude Code 在管理员控制台中获得两个新标签页，提供更深入的洞察，分别聚焦价值与使用情况。使用情况标签页展示组织内的活跃开发者、会话数量和热门命令，每日更新。价值标签页汇总使用量与成本数据，帮助管理员一眼看清 Claude Code 的价值，估算生产力提升、每次提交的成本和年度价值。标签页中每个公式都可见，输入项也可调整。

[分析对话（Analytics chat）](https://support.claude.com/en/articles/14729354-use-analytics-chat-to-ask-claude-about-usage)现在能回答范围广得多的问题，并生成内容更丰富、可供你深入探究的 Artifact。管理员可以用自然语言提问——比如"这个月哪些团队的 Claude 使用量翻倍了？"或"我们在哪里的人均价值最高？"——Claude 会返回可导出、可与相关方共享的图表。

使用量与成本数据可通过[分析 API（Analytics API）](https://platform.claude.com/docs/en/manage-claude/analytics-api)以编程方式获取，因此财务和 IT 团队可以把 Claude 的使用量与成本数据接入他们已在使用的工具——例如 Datadog Cloud Cost Management 和 CloudZero——并与其他云与 AI 支出并列查看。结果可按日期范围、团队、产品或模型进行筛选。技能会报告自身的使用量与成本，新的端点则可追踪插件采用情况和 Artifact 创建情况。

管理员可以把使用可见性延伸到单个用户——成本、产品与模型细分、以及对照支出限额的进度——这样就不会有人遭遇意外的用量中断。用户也可以查看自身使用量随时间变化的趋势，包括自己最依赖哪些产品、模型和技能，以及这些活动如何累积成支出。

## 管理支出的控制项

[模型默认值与授权](https://support.claude.com/en/articles/15694740-manage-model-access-for-your-organization)让管理员设定聊天、Cowork 和 Claude Code 中新对话默认使用哪个 Claude 模型，这样日常工作就不一定默认走最贵的选项。管理员可以控制哪些模型可供特定角色或整个组织使用。

支出阈值提醒会在触及组织级支出上限的 75% 和 90% 时通知管理员，让他们有时间在有人任务中途被拦下之前提高上限。用户会在 75% 和 95% 阈值时收到应用内通知，并且无需离开 Claude 即可直接向其管理员申请提高限额。

对于需要在多个群组间管理限额的组织，[Admin API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api#example-workflows) 把成本控制工作流搬进脚本，让控制措施随组织规模一起扩展。可以大规模自动化处理提额申请的审批、识别接近支出限额的成员，并标记使用量快速变化的团队。

![Datadog](https://assets.claude.com/0a17621af2bfc623c9104a3dd9fba2e6ebfc89d5.svg)

> "成本可见性不是每月做一次的功课。细粒度的支出数据和提醒会促使团队定期重新审视自己使用 Claude 的方式，而不是在计费周期结束时才发现意外。借助分析 API，我们可以把这些数据接入每天都在用的工具。"

Kyra Abbu，产品经理

![Workato](https://assets.claude.com/0f6a57d6672a2fd862b06d76095d954f0d34c9b0.svg)

> "我不会让那些驱动我们最佳季度业绩的人慢下来，我的 CFO 也没有要求我这么做。他要的是投资回报率。我们把接入企业 MCP 服务器的 Claude 与 4% 的收入增长关联了起来，而按团队把成本与业务影响并列呈现，正是我让这个论证站得住脚的方式。"

Carter Busse，首席信息官

![Nubank](https://assets.claude.com/ef096fe660d47f66be6ef25f7e1e376352e4748b.svg)

> "只看 token 用量说明不了什么。我真正想看的是，哪些技能在整个组织中被一次又一次地运行——那才是价值的真正信号。"

Ciro Yamada，产品总监

## 快速上手

对于在整个组织中管理 Claude 的管理员：在管理员控制台中查看使用量与成本细分，按群组设置模型默认值和支出限额，并配置支出阈值提醒以防超支。使用数据可在管理员仪表盘中查看，分析 API 则让财务和 IT 团队把同样的指标拉取到既有报表系统中，详情见[此处](https://support.claude.com/en/articles/13694757-get-started-with-the-claude-enterprise-analytics-api)。

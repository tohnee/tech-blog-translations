---
title: "把 Salesforce 引入 Claude"
title_en: "Bringing Salesforce into Claude"
date: 2026-09-15
source: https://claude.com/resources/articles/salesforce-in-claude
crawled: 2026-11-17
translated: 2026-11-17
---

# 把 Salesforce 引入 Claude

> 原文：[Bringing Salesforce into Claude](https://claude.com/resources/articles/salesforce-in-claude) · Claude 博客

借助全新的 Salesforce in Claude 插件，销售人员现在可以调研公司、准备通话、审视销售管道，并起草 CRM 更新。

今天我们发布 Salesforce in Claude 测试版。这是一个与 Salesforce 共同构建的插件，在销售人员既有的 Salesforce 权限范围内，把其客户账户、商机和销售管道带入 Claude。它包含 37 项[技能](https://claude.com/resources/articles/skills)，覆盖客户经理日常工作，包括客户调研、通话准备、销售管道审视和 CRM 更新。

销售人员常常要花上数小时做会议准备，或处理客户会议后的跟进工作——手动拼凑散落在 Salesforce、邮件、通话录音和 Slack 中的信息。有了这个新插件，Claude 会承担这些行政性工作，并在销售人员批准后更新 Salesforce。

该插件还包含两个连接器，管理员接好 Salesforce、销售人员登录后即可开始使用。借助 Salesforce 连接器，Claude 可以读取 Salesforce 数据并据此执行操作：总结客户账户历史、更新商机、记录通话或创建跟进任务。Slack 连接器则覆盖交易频道摘要和客户团队讨论串，技能可以读写这些内容。销售人员首次使用该插件时，一个设置技能会识别他们的工具和连接器，并创建一个针对其角色和业务组合量身定制的 Claude Artifact。

## 销售人员目前如何使用 Salesforce in Claude

**以一份简报开启一天。** 每天早上，Claude 会送上一份个性化简报，内容包括当天的会议、即将成交的交易、存在风险的商机，以及需要回复的未读讨论串。一经设定，它便在后台运行，你可以通过 Claude 在任何地方访问，包括在移动中使用 Claude 应用。从简报出发，销售人员可以指示 Claude 推迟成交日期、变更阶段或添加跟进任务，Claude 会在 Salesforce 中完成更新。每周五，简报会总结这一周，并为销售人员的经理起草一份更新。

**为通话做准备。** 销售人员可以请 Claude 为下一场会议做准备，它会从 Salesforce、Slack 和邮件中提取要点：进行中的商机及各自进展、客户团队本周讨论了什么、尚未回复的讨论串，以及此前通话中仍未解决的问题。如果它在这些讨论串里发现有尚未录入 Salesforce 的关键干系人，Claude 会把他们添加为该客户账户下的联系人。

**审视交易并制定成交计划。** 针对某个商机，Claude 会依照团队的方法论为该交易打分，考量资格审查缺口、尚未接触的关键干系人，以及可能导致成交日期延后的因素。让它继续，它会起草商业论证和一份标注日期的双方成交计划、填写资格审查字段，并把缺失的关键干系人添加为联系人角色。所有内容在通过审批后都会保存到该商机中。

**让每场会议结束时 Salesforce 都已更新。** 每次通话后，Claude 会把转录文本或销售人员的笔记整理成一封跟进邮件、一份发到 Slack 交易频道的摘要，并起草商机更新内容，如后续步骤、阶段和成交日期，供销售人员审阅。

**审视销售管道并共享预测。** 销售人员可以请求一份销售管道视图，Claude 会构建一个交互式仪表盘，呈现各阶段的覆盖率、最可能延期的交易及其原因，并可按客户账户下钻。在仪表盘上，销售人员可以指示 Claude 调整成交日期或变更阶段，Claude 会更新 Salesforce 中的记录。仪表盘可以与领导层或团队共享，Claude 还能按领导层期望的格式起草预测说明。销售负责人可以对整个团队运行同样的视图。

**建立在组织既有权限之上**
Salesforce 仍然是权威记录系统。销售人员用其 Salesforce 凭据登录，Claude 只读取其权限允许的内容。默认情况下，Claude 会在写入每一项拟议变更之前请销售人员批准。在 Team 和 Enterprise 套餐中，我们默认不会用你的数据训练模型。

管理员为整个组织一次性连接 Salesforce，并选择哪些群组可以使用该插件。

## **销售团队如何使用 Salesforce in Claude**

Anthropic 的客户 GitLab、Siemens 和 Legora 已在各自组织中部署 Salesforce in Claude，有 7,000 名 Salesforce 销售人员在工作中使用它。以下是他们向我们反馈的使用体验：

> "借助 Salesforce in Claude，我们的销售人员能在几秒内而非数小时内，把实时数据转化为会议简报。随着销售团队扩张，每一位新加入的代表都能一开始就全面了解我们所服务的律师事务所。" —— David Eckstein，Legora 首席财务官

> "借助 Salesforce in Claude，销售人员一开始工作，销售管道审视已经完成、客户账户历史也已经在手。这些时间直接回到了与客户的对话中。" —— Alexa Vignone，Salesforce 总裁兼首席营收官

## **快速上手**

Salesforce in Claude 已在所有付费 Claude 套餐中以测试版提供。[Salesforce MCP](https://claude.ai/directory/bundles/salesforce#directory/connectors/salesforce-headless-360) 现在即可通过市场直接安装。要安装该插件，管理员可通过 [AgentExchange](https://agentexchange.salesforce.com/sales-cloud-in-claude-beta-access) 申请访问权限，并为整个组织一次性连接 Salesforce。我们为管理员提供了[设置指南](https://support.claude.com/en/articles/16952184)，说明如何为你的组织启用此功能。对于销售负责人，我们提供了一份[关于如何用 Claude 打造高效销售组织的指南](https://claude.com/resources/articles/building-an-ai-native-revenue-organization)。

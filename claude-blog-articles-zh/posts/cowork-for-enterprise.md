---
title: "让 Claude Cowork 为进入企业做好准备"
title_en: "Making Claude Cowork ready for enterprise"
date: 2026-04-09
source: https://claude.com/resources/articles/cowork-for-enterprise
crawled: 2026-11-17
translated: 2026-11-17
---

# 让 Claude Cowork 为进入企业做好准备

> 原文：[Making Claude Cowork ready for enterprise](https://claude.com/resources/articles/cowork-for-enterprise) · Claude 博客

Claude Cowork 现已在所有付费方案上正式可用。在企业内部，Claude Cowork 已成为团队运作方式的关键组成部分：承接任务、起草项目交付物、让团队保持信息同步。

今天，我们推出了一系列组织级管控能力，帮助团队在全公司范围内部署 Claude Cowork：面向 Enterprise 的基于角色的访问控制、群组支出限额、扩展的 OpenTelemetry 可观测性，以及让管理员查看 Claude Cowork 采用情况的使用分析。

## 早期信号

Claude Code 帮助开发者从"把问题交给 Claude"转向"把整项任务交给 Claude"。而在整个组织中，我们看到 Claude Cowork 呈现出同样的模式：绝大多数 Claude Cowork 用量来自工程团队之外。更重要的是，运营、市场、财务、法务等职能并不是把核心工作交给 Claude，而是把围绕其最关键任务的那些工作交出去——项目进展更新、协作演示文稿、调研冲刺等等。

早期在企业中采用 Claude Cowork 的客户，一旦看到这一模式在某个团队中显现，往往就想把它推广到更大范围，随之而来的问题包括：谁能获得访问权限、如何管理支出，以及如何看清各团队的实际情况。

## 面向全组织部署的管控能力

要在整个组织中部署具备 Claude Cowork 能力的智能体，管理员团队就需要治理手段与可见性。今天，我们补充了组织所需的更多管控能力：

**基于角色的访问控制。** Claude Enterprise 的管理员现在可以将用户编入群组——手动操作，或通过身份提供商的 SCIM 同步——并为每个群组分配自定义角色，定义该群组成员可以使用哪些 Claude 能力。可以为特定团队开启 Claude Cowork，并随着采用范围扩大逐步调整。

**群组支出限额。** 可在管理员控制台中设置按团队划分的预算。成本可预测，并可根据对每个团队需求的了解进行调整。

**使用分析。** Claude Cowork 的活动现在会出现在管理员仪表盘和 Analytics API 中。管理员可以在仪表盘上按不同日期范围跟踪 Claude Cowork 会话数和活跃用户数。Analytics API 提供更细的数据：按用户划分的 Claude Cowork 活动、技能与连接器的调用次数，以及与现有 Chat 和 Claude Code 数据并列的 DAU/WAU/MAU。由此可以看清哪些团队在采用、哪些工作流真正落地、下一步该往哪里投入。

**扩展的 OpenTelemetry 支持。** Claude Cowork 现在会为工具与连接器调用、被读取或修改的文件、使用的技能，以及每个由 AI 发起的操作是手动批准还是自动批准发出事件。这些事件兼容 Splunk、Cribl 等标准 SIEM 管道，共享的用户账户标识符可用于将 OTEL 事件与 Compliance API 记录关联起来。OpenTelemetry 在 Team 和 Enterprise 方案中可用。

**Zoom MCP 连接器。** Claude Cowork 可与团队已经在用的工具集成。今天，Zoom 推出了一款连接器，把会议智能直接带入 Cowork 体验。Zoom 连接器提供 AI Companion 会议纪要与行动项，以及转录文本和智能录制——帮助团队把 Zoom 上的对话转化为 Cowork 中的智能体式工作流。可在 Claude 设置的连接器目录中添加 Zoom。

**按工具的连接器控制。** 管理员现在可以在整个组织范围内限制每个 MCP 连接器中可用的操作——例如允许读取访问但禁用写入操作。权限在整个组织范围生效，并在管理员控制台中配置。

## 组织如何使用 Claude Cowork

[Zapier](https://claude.com/customers/zapier-cowork-qa) 把 Cowork 连接到其组织数据库、Slack 和 Jira，以暴露工程瓶颈——最终得到一个仪表盘、逐团队的分析，以及一份带优先级的路线图，随后 Product and Design Ops 团队又照此复刻了自己的版本。[Jamf](https://claude.com/customers/jamf) 把一份包含七个维度的绩效评估，转化为一场 45 分钟的引导式自我评估，随后又为供应商评审和事件响应构建了类似的工作流。风险投资机构 [Airtree](https://claude.com/customers/airtree) 构建了一套董事会准备（board prep）工作流，从被投企业的 Drive、Slack 更新和竞争对手新闻中提取信息，并与上一轮的准备材料交叉比对。

![Jamf](https://assets.claude.com/6525757ec4c3fc79978ca32c81251db6edcf286d.svg)

> "组织上下都在用 Cowork 做数据融合、分析和仪表盘搭建。定制化仪表盘的需求非常大。以前需要 BI 工具或工程师帮忙的任务，现在人们自己几分钟就能完成。"

Nick Benyo，软件工程师

![Airtree](https://assets.claude.com/0a4af388f451cefedf61dba15d9f73962a46c700.png)

> "在多个团队之间使用 Claude Cowork，让它发挥出了数倍的价值。一个人构建的技能可以被所有人使用。Claude Cowork 成了事务所共享的基础设施，而不只是一个个人效率工具。"

Jackie Vullinghs，合伙人

![Thomson Reuters](https://assets.claude.com/3c80d8dc7dbf6556d1137977873dee26eaffae1d.svg)

> "Claude Cowork 帮助团队以过去难以论证的规模开展工作。人的角色变成了校验、打磨和决策，而不是重复返工。"

Joel Hron，首席技术官

![Zapier](https://assets.claude.com/76ec34d2d040fb1dd2dd94a7950788e0a82a09b6.svg)

> "从'有个想法'到'把东西交付出去'，这道门槛已经消失了。现在重要的能力不是知道每一步该怎么做，而是清楚地知道你想达成什么，并有能力把工作引向那个结果。执行仍然是实实在在的工作，但一个人能交付的上限已经大幅提升。我真的想不起来没有它的时候我是怎么工作的。"

Larisa Cavallaro，AI 自动化工程师

## 开始使用

Claude Cowork 和桌面版 Claude Code 现已在 macOS 和 Windows 的所有付费方案上正式可用。可在 [claude.com/download](http://claude.com/download) 下载 Claude 桌面应用。

对于要在整个组织内部署 Claude 的管理员：可在管理员控制台中[配置基于角色的访问控制](https://support.claude.com/en/articles/13930458-set-up-role-based-permissions-on-enterprise-plans)、群组支出限额和 [OpenTelemetry](https://claude.com/docs/cowork/monitoring)。Claude Cowork 的使用数据可在管理员仪表盘中查看，Analytics API 的文档见[此处](https://support.claude.com/en/articles/13694757-access-engagement-and-adoption-data-with-the-analytics-api)。

如需部署实操讲解，欢迎参加我们与 PayPal 于 4 月 16 日联合举办的[网络研讨会](https://claude.com/resources/webinars/deploying-cowork-across-the-enterprise-with-paypal)。

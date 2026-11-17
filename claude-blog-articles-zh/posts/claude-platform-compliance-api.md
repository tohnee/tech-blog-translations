---
title: "用 Compliance API 审计 Claude Platform 活动"
title_en: "Audit Claude Platform activity with the Compliance API"
date: 2026-03-30
source: https://claude.com/resources/articles/claude-platform-compliance-api
crawled: 2026-11-17
translated: 2026-11-17
---

# 用 Compliance API 审计 Claude Platform 活动

> 原文：[Audit Claude Platform activity with the Compliance API](https://claude.com/resources/articles/claude-platform-compliance-api) · Claude 博客

Compliance API 让管理员以编程方式访问其 Claude Platform 组织范围内的审计日志。

* 分类：[产品更新](/resources/product-updates)
* 产品：Claude Platform
* 日期：2026 年 3 月 30 日
* 阅读时长：3 分钟

## 用 Compliance API 审计 Claude Platform 活动

Compliance API 现已在 Claude Platform 上提供，让管理员以编程方式访问整个组织范围内的审计日志。安全与合规团队可以跟踪用户活动、监控配置变更，并把 Claude 的使用数据集成到现有的合规基础设施中。

## 面向组织的审计日志

受监管行业中的组织——如金融服务、医疗健康、法律——需要详细记录谁在何时访问了什么，以及发生了什么变更。如果无法以编程方式访问这些数据，合规团队就只能依赖手动导出和定期审查，而这无法规模化。

Compliance API 提供一个活动流，记录整个组织中与安全相关的事件。管理员可以按时间范围、特定用户或 API key 筛选并获取活动日志。

该 API 目前跟踪两类活动：

* **管理员与系统活动：** 修改资源访问权限或配置的操作，例如向工作区添加成员、创建 API key、更新账户设置或修改实体访问权限。
* **资源活动：** 由用户驱动、创建或修改资源数据的操作，例如创建文件、下载文件或删除 skill。这些操作涵盖可能影响数据、或允许资源访问敏感信息的动作，不包括与模型的直接交互。

两者合起来覆盖用户登录和登出事件、账户设置更新、工作区变更以及其他组织审计事件。该 API 不记录推理活动，例如用户与模型的交互或模型活动。

## 开始使用

联系你的客户团队为组织启用 Compliance API。启用后，创建一个管理员 API key，并用它查询活动流端点。请注意，日志记录从 API 启用之时开始——此前的历史活动不可用。

已经在 Claude Enterprise 中使用 Compliance API 的组织，可以把自己的 Claude API 组织添加到同一个父组织下，并在单一活动流中筛选两者的活动。

在 [Anthropic Trust Center](https://trust.anthropic.com/resources?s=tob70gqyan60x3dwb7nkap&name=anthropic-compliance-api) 阅读文档了解更多。

## 相关文章

探索更多产品动态，以及为使用 Claude 构建的团队准备的最佳实践。

*2026 年 11 月 12 日 · 文章*

### [在你的安全边界内运行 Claude Managed Agents](/resources/articles/self-hosted-claude-managed-agents)

推出自托管 Claude Managed Agents。现在，你可以在自己的环境中运行智能体，无论是自有云还是本地部署。智能体、凭证和会话历史都由你托管，并可自行选择向 Claude 发送请求的位置。

Claude Platform、Claude Managed Agents

*2026 年 11 月 12 日 · 文章*

### [推出 Claude for Manufacturing](/resources/articles/claude-for-manufacturing)

一个包含 17 项技能和四个连接器的新插件，帮助制造商基于现有系统起草报价、质量报告和供应商询价。

*2026 年 11 月 12 日 · 文章*

### [推出 Claude Meetings](/resources/articles/claude-meetings)

将 Claude 加入视频通话，一边交谈一边推进工作

*2026 年 11 月 10 日 · 文章*

### [你的应用现在可以在 Claude 中打开，Claude 也能在其中工作](/resources/articles/interactive-connectors-full-tool)

合作伙伴现在可以将应用直接嵌入 Claude，让你和 Claude 在同一工具、同一屏幕上协作，无需切换标签页。

Claude apps、MCP

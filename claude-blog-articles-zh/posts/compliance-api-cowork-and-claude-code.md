---
title: "Compliance API 的覆盖范围扩展至 Claude Cowork 和 Claude Code"
title_en: "Compliance API coverage extends to Claude Cowork and Claude Code"
date: 2026-08-11
source: https://claude.com/resources/articles/compliance-api-cowork-and-claude-code
crawled: 2026-11-17
translated: 2026-11-17
---

# Compliance API 的覆盖范围扩展至 Claude Cowork 和 Claude Code

> 原文：[Compliance API coverage extends to Claude Cowork and Claude Code](https://claude.com/resources/articles/compliance-api-cowork-and-claude-code) · Claude 博客

* 分类：[产品更新](/resources/product-updates)
* 产品：Claude Enterprise、Claude apps、Claude Code、Claude Cowork
* 日期：2026 年 8 月 11 日
* 阅读时长：3 分钟

***更新：Compliance API 对 Cowork（桌面、web 和移动端）以及 Claude Code（CLI 和桌面端）的覆盖现已正式发布；对 Microsoft 365 加载项（Excel、Word、PowerPoint 和 Outlook）以及 Claude Science 的覆盖处于测试阶段（2026 年 8 月 26 日）***

Claude 的 Compliance API 现在覆盖桌面应用、web 和移动端的 Cowork，以及 CLI 和桌面应用中的 Claude Code。该覆盖面向 Claude Enterprise 客户提供测试版。合规与安全团队可以通过他们已经用于 Claude 聊天的同一个 Compliance API 接口，从这两个产品中拉取会话内容和元数据。

新增端点是增量式的：你目前从 Compliance API 拉取的数据不会发生任何变化。

安全与合规团队依赖 Compliance API 来了解 Claude 在整个组织中的使用情况——用于审计和 eDiscovery——而无需为每个使用界面单独部署日志基础设施。把覆盖范围扩展到 Cowork 和 Claude Code 填补了一个缺口：这些会话现在会与 Claude 聊天一起呈现。

## 工作原理

新的会话端点会为每个 Cowork 和 Claude Code 会话返回一份统一的、由服务器托管的记录，因此提示词、响应和工具活动会一起包含在单条会话记录中。

每条会话记录包含两类数据：

* **会话内容：** 提示词与响应、工具调用内容（web 与 MCP），以及以记录文本形式捕获的 skills 和 artifacts 内容。
* **会话元数据：** 经验证的用户 ID 和电子邮件地址、组织 ID、会话 ID 和每条消息的 ID，以及时间戳。

该测试版不包括 Claude Code on the web、通过 Claude Platform 访问的 Claude Code，以及在 Amazon Bedrock、Google Cloud 的 Vertex AI 或 Microsoft Foundry 上运行的会话。

已经在导出 OpenTelemetry 数据的组织可以继续保留这套机制：Compliance API 可以与它并行工作，你这边无需任何基础设施。

## 开始使用

对 Cowork 和 Claude Code 的覆盖现已可用，并包含在你使用现有 Compliance Access Key 的 Compliance API 中——无需构建单独集成。如果你的组织已启用 Compliance API，可以直接查询新的会话端点。如果尚未启用，请查阅 Compliance API [文档](https://platform.claude.com/docs/en/manage-claude/compliance-api)进行启用。

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

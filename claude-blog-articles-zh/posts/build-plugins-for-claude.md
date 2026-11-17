---
title: "为 Claude 构建插件"
title_en: "Build plugins for Claude"
date: 2026-09-25
source: https://claude.com/resources/articles/build-plugins-for-claude
crawled: 2026-11-17
translated: 2026-11-17
---

# 为 Claude 构建插件

> 原文：[Build plugins for Claude](https://claude.com/resources/articles/build-plugins-for-claude) · Claude 博客

*你现在可以通过全新的开发者门户向 Claude 目录提交插件、跟踪审核进度，并在插件上线后查看使用分析。*

每天，数百万人将 Claude 连接到他们的应用、工作工具和数据。今天，我们让开发者更容易触达他们。

插件封装 MCP 连接器、Agent Skills，或两者兼有，是为 Claude 构建第三方扩展的主要方式。构建一个插件，通过新的目录提交门户提交，一旦获批，它就会出现在 [Claude 目录](https://claude.ai/directory)中。

## **在目录提交门户中提交并跟踪插件**

[目录提交门户](https://claude.ai/directory/manage/new)向付费 Claude 套餐的开发者开放。有两种方式提交插件并将其发布到 Claude 目录：

* **单个 MCP 连接器：** 指向你的远程 MCP 服务器。
* **插件包：** 组合 MCP 服务器和技能，托管在 GitHub 上，然后提交仓库。在 Claude Code 中，插件还可以包含 LSP、命令、钩子和智能体。

无论选择哪条路径，门户都会引导你从提交走到发布。你可以：

* **自动验证插件。** 每次提交后都会立即进行检查和安全扫描，让你尽早发现问题。
* **查看状态与反馈。** 了解插件处于审核流程的哪个阶段、安全扫描的结果以及建议的修改。
* **准备好时再发布。** 一旦获批，由你决定何时在 Claude 中发布插件。

![](https://assets.claude.com/032a9fa50ce34ebacad5fb53690eca559fea7a5a.png)

插件的审核状态与建议修改示意视图。数据仅为示例。

## **插件发布后进行监控与改进**

插件上线后，使用分析会显示各个产品界面和版本上的安装量，让你能为用户优先安排修复与功能。在发现方面，你可以看到列表被查看的频率，以及哪些搜索把人们引向了它，从而优化列表以触达新用户。

![](https://assets.claude.com/ab51ab12c2c9424ea16ccf140d534f35360038ba.png)

已发布插件的使用指标示意视图。数据仅为示例。

## **用 MCP 2.0 及其扩展为用户带来丰富体验**

Claude 支持最新的 MCP 规范，通常被称为 [MCP 2.0](https://modelcontextprotocol.io/specification/2026-07-28)，其中包含无状态核心。你可以通过两项 [MCP 扩展](https://modelcontextprotocol.io/extensions/overview)提升插件的使用体验：[MCP Apps](https://claude.com/docs/connectors/building/mcp-apps/getting-started)，用于对话内的交互式 UI；以及 [Enterprise Managed Auth](https://claude.com/docs/connectors/building/enterprise-managed-auth)，为企业用户提供零接触 OAuth。更多 MCP 特性和扩展的支持即将推出。

## **开始为 Claude 构建插件**

插件是第三方开发者为 Claude 创建扩展的主要方式。未来几周内，一套统一的发现体验将在 Claude 和 Claude Code 中推出。

技能和 MCP 连接器仍作为构建模块存在，Claude 目录也将继续列出它们。未来，开发者将能够把自己的连接器列表转化为插件。如果你在 Claude 目录上已有技能、连接器或插件，无需做任何更改。

要开始构建插件，请阅读我们的文档[了解如何构建插件](https://claude.com/docs/build/overview)，并[在此](https://claude.ai/directory/manage/new)提交你的插件。

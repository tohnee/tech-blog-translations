---
title: "你的应用现在可以在 Claude 中打开，Claude 也能在其中工作"
title_en: "Your apps can now open in Claude, and Claude can work in them"
date: 2026-11-10
source: https://claude.com/resources/articles/interactive-connectors-full-tool
crawled: 2026-11-17
translated: 2026-11-17
---

# 你的应用现在可以在 Claude 中打开，Claude 也能在其中工作

> 原文：[Your apps can now open in Claude, and Claude can work in them](https://claude.com/resources/articles/interactive-connectors-full-tool) · Claude 博客

我们的合作伙伴现在可以直接把应用嵌入 Claude，让你和 Claude 在同一个工具、同一个屏幕上工作，无需切换标签页。

今年早些时候，我们推出了[交互式连接器](https://claude.com/resources/articles/interactive-tools-in-claude)（在新标签页中打开），把工具的一小块实时视图带入 Claude。从今天起，在连接器支持的场景中，你可以把工具打开在对话旁边，或展开到全屏，并让 Claude 与你并肩工作、直接做出修改。

该功能正在 Web 和 Claude 桌面应用中向所有套餐推出，它是把聊天与 Cowork 结合在一起的[全新 Claude 体验](https://claude.com/resources/articles/cowork-is-now-claude)（在新标签页中打开）的一部分。当你的账号升级到新版 Claude，或你的组织开启后，你就会看到这些功能。

新增内容：

* **Claude 可以在你打开的工具中工作。**你可以让 Claude 修改你正打开的页面、行或文件，并像批准连接器操作那样批准它的操作。Claude 修改时，变化会实时显示在工具中，因此你可以与它并肩继续工作。
* **整个工具打开在对话旁边。**你可以在工具中工作，并隐藏聊天；需要空间时也可以全屏。对于 Confluence 或 Notion 这类工具，这意味着你得到的是登录你自己账号的完整编辑器，而不是一个受限的预览。
* **直接打开已连接的工具，无需撰写 Claude 提示词。**需要 Claude 帮忙时，在同一个屏幕里提出即可。
* **固定你最常用的工具。**你可以把它们排列在 [artifacts](https://claude.com/resources/articles/sheets-whiteboards-data) 旁边，通过侧边栏和 + 菜单一键访问。

## 在你使用的工具中与 Claude 协作

我们先从目录中的一小批工具开始，包括 Asana、Canva、Carta、Dropbox、monday.com、Smartsheet、Vercel 和 Webflow。

以下是目前 Claude 中部分工具可以做的事情：

* **Adobe。**让 Claude 修饰、编辑照片并添加效果；高亮、编辑和涂黑 PDF。
* **Atlassian。**在聊天旁边打开 Confluence 页面，让 Claude 撰写和编辑，并在页面上实时查看它的修改。
* **Box。**在聊天旁边打开 Box 文件，让 Claude 修改它，并在保留改动之前并排对比两个版本。
* **HubSpot。**确定销售管道任务和后续跟进的优先级，然后在 Claude 中处理它们。
* **Notion。**让 Claude 创建 Notion 文档或数据库。边聊边构建，或自行编辑，全程无需离开 Claude。

![支持 Claude 中交互式连接器的 13 个工具的标识](https://assets.claude.com/98d2cbf9c0392a81da0d53ea7666bf08528db80e.png)

Figma、Harvey 和 Shopify 也在构建集成，我们也鼓励其他开发者这样做。

## 面向开发者：构建于 MCP Apps 之上

交互式连接器运行在 MCP Apps 之上，这是 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)（在新标签页中打开）的开放扩展，让 MCP 服务器可以把自有的界面带入 AI 应用。你构建的 MCP App 并不局限于 Claude，它可以运行在任何支持该[扩展](https://modelcontextprotocol.io/extensions/apps/overview)（在新标签页中打开）的 AI 应用中。

在此之前，Claude 中的 MCP Apps 主要以对话中的交互式视图形式出现。现在 Claude 支持该扩展的更多部分，例如 app tools 以及嵌入式站点，因此开发者完整的应用可以在 Claude 内运行。

对这些能力的支持面向开发者处于公开预览阶段。开发者今天就可以开始基于它们构建。阅读我们的[文档](https://claude.com/docs/connectors/building/mcp-apps/getting-started)（在新标签页中打开）开始构建。

## 开始使用

你可以从[目录](https://claude.ai/directory/featured/interactive-connectors)（在新标签页中打开）连接上文提到的工具，然后从对话中打开任意工具，或将它固定到侧边栏。

**面向管理员：**如果你的组织已经允许某个连接器的全部工具，它的新功能会随着推出自动出现。管理员可以像现在一样限制连接器的工具。

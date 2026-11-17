---
title: "Claude 现已支持 Google Docs、Sheets 和 Slides"
title_en: "Claude now works with Google Docs, Sheets, and Slides"
date: 2026-10-06
source: https://claude.com/resources/articles/claude-now-works-in-google-docs-sheets-and-slides
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude 现已支持 Google Docs、Sheets 和 Slides

> 原文：[Claude now works with Google Docs, Sheets, and Slides](https://claude.com/resources/articles/claude-now-works-in-google-docs-sheets-and-slides) · Claude 博客

*使用 Google Workspace 的团队现在既可以把 Claude 请进他们的文件，也可以直接在 Claude 中处理这些文件——借助我们全新的加载项以及 Google Docs、Sheets 和 Slides 连接器（测试版）。*

Claude for Google Workspace™ 现已在所有付费 Claude 套餐中开启公开测试。它把 Claude 加入 Google Docs、Sheets 和 Slides，让你可以直接在打开的文件中与 Claude 协作。此外，我们还发布了新的 Google Docs、Sheets 和 Slides 连接器（测试版），Claude 可以使用它们直接从 Claude 中创建和编辑 Google 文件。

## Claude 在你工作的地方工作

借助该加载项，Claude 会在文件旁的侧边栏中打开，因此你在工作时无需在应用或浏览器标签页之间来回切换。Claude 可以读取你打开的文档、表格或演示文稿，看到你选中的文字、单元格或幻灯片，并直接在文件中做出修改。

**在 Docs 中**，例如，Claude 可以就地修改一个句子或调整标题样式，而不影响周围的格式。对于更大的改写，它可以以建议卡片的形式在侧边栏中提出修改。每张卡片都会高亮它将要改动的段落，你可以选择应用或忽略。你可以让 Claude 精简产品需求文档的执行摘要，并把后续步骤转成表格，Claude 会直接在文档中完成这两件事。

**在 Sheets 中**，Claude 可以编写公式、构建数据透视表和原生的 Sheets 图表，并新增标签页。对于数据连接或数据清洗，它可以把某个区域的数据拉进 Python 处理，再把结果写回表格。你可以从一张空表开始，附加源文件，要求生成一份 Q3 预算与实际支出报告，为每个团队各建一个标签页并配一张汇总图，Claude 还能标出任何超出预算的项目。

**在 Slides 中**，Claude 可以使用你演示文稿的版式和主题来构建新幻灯片，使其与演示文稿的其他部分保持一致。之后，它还能自行检查，并标出相互重叠或超出幻灯片边界的元素，或难以阅读的文字。

由你决定 Claude 可以自主完成多少工作。在默认的“编辑前询问”模式下，每项修改都会以一张审批卡片的形式呈现，并附上摘要，Claude 会等待你的批准后再执行修改。在“接受所有编辑”模式下，Claude 会推进任务并直接应用修改，不会中途停下。

## 你的连接器、技能与企业级管控如影随形

当你以自己的 Claude 账号登录时，侧边栏里提供的是你在 Claude 中使用的相同模型、[连接器（在新标签页中打开）](https://claude.com/marketplace/connectors-plugins)和[技能（在新标签页中打开）](https://claude.com/skills)。例如，如果你要一份面向客户的季度业务回顾（QBR）演示文稿，Claude 可以通过你的 Google Drive 连接器从 Salesforce 拉取客户历史记录，并调取近期的通话记录。如果你把 QBR 的格式保存为一项技能，你的团队就可以按照相同的格式和步骤构建下一份演示文稿。

在 Enterprise 套餐中，Compliance API、客户托管加密密钥（CMEK）和 OpenTelemetry 审计导出等管控措施同样适用于该加载项。

## 在 Claude 中编辑 Google 文件

借助同样处于测试版的 [Google Docs、Sheets 和 Slides 连接器（在新标签页中打开）](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)，你可以从 Claude 开始，让它在对话中创建和编辑你的 Google 文件。粘贴一个 Google 文件链接，或直接索要一个 Google 文档、表格或演示文稿，在受支持的配置下，它会在对话旁的窗格中打开。当你需要新建文件，或工作涉及多个文件时，从 Claude 开始最为合适。Claude 的访问权限与你现有的 Google 共享权限一致。

## 开始使用

[Claude for Google Workspace（在新标签页中打开）](https://claude.com/claude-for-google-workspace)已在所有付费套餐中进入测试阶段。

请从 [Google Workspace Marketplace（在新标签页中打开）](https://workspace.google.com/marketplace/app/claude/12459801340)安装，然后打开一个文件，依次进入 Extensions > Claude > Open Claude。管理员可以从 Google 管理控制台将其部署到整个域或选定的群组。[帮助中心指南涵盖了安装设置（在新标签页中打开）](https://support.claude.com/en/articles/16951679-use-claude-in-google-docs-sheets-and-slides)。

要从 Claude 中编辑 Google 文件，请开启 [Google Docs、Sheets 和 Slides 连接器（在新标签页中打开）](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)。在 Team 和 Enterprise 套餐中，需要先由所有者或主要所有者启用连接器。

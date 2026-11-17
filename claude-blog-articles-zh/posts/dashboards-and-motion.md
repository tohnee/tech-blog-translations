---
title: "用 Claude 构建实时仪表盘，制作动画讲解"
title_en: "Build live dashboards and animate explainers with Claude"
date: 2026-10-08
source: https://claude.com/resources/articles/dashboards-and-motion
crawled: 2026-11-17
translated: 2026-11-17
---

# 用 Claude 构建实时仪表盘，制作动画讲解

> 原文：[Build live dashboards and animate explainers with Claude](https://claude.com/resources/articles/dashboards-and-motion) · Claude 博客

Claude Dashboards 与 Claude Motion 现已进入测试版。Docs、Slides 和 Design 已结束测试，并在包括 Free 在内的所有 Claude 套餐中提供。

从今天起，Claude 可以把你的数据变成一个持续更新的仪表盘，也可以把你的想法变成供下一次演示使用的动画讲解。Claude Dashboards 可连接 BigQuery、Databricks、Snowflake 等数据平台，或 Salesforce 等 CRM 工具，现已在付费套餐中以测试版提供。Claude Motion 在 Team 和 Enterprise 套餐中以测试版提供。Claude Docs、Slides 和 Design 已结束测试，在所有套餐中可用，包括 Free。

[想就公司数据问一个问题](https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude)，通常意味着提工单或写 SQL。而本该用动态形式表达效果更好的想法，往往最终又变成一页静态幻灯片。于是人们要么等，要么干脆放弃。Claude 此前已经能帮上其中一部分。现在，你可以直接要一个仪表盘或一段动画，并看到 Claude 是如何做出来的。每张图表都会显示它背后的查询，每段动画都以可编辑的代码形式构建。Claude 做第一版，你决定分享什么。

## Claude Dashboards：快速向你公司的数据提问

连接你公司的数据平台，例如 Amazon Redshift、BigQuery、ClickHouse、Databricks 或 Snowflake，然后用自然语言提问。Claude 会从你的数据中取回答案、构建仪表盘，并在数据变化时保持其更新。它也能与你其他的连接器配合使用。例如，你可以要一个展示 Salesforce 商机情况的仪表盘。仪表盘很适合快速、探索性的问题，比如本周注册量相比上个月如何。点击任意数字可以看到它背后的查询，也可以让 Claude 解释。每张图表都会显示其数据最近一次刷新时间。

![Claude 用一整年的骑行数据搭建了一个共享单车仪表盘，包含骑行总量以及按天和按小时的骑行图表。](https://assets.claude.com/7688d4d3b888c17cf4b3553f537f291882a92656.png)

仪表盘与你的 BI 和分析工具并肩工作。当某个问题需要更深入的分析时，可以把仪表盘从 Claude 直接发送到 Amplitude、Grafana、Hex、Mixpanel、Omni、Perplexity、PostHog 或 Sigma，在那里继续分析；Databricks Genie、Looker、monday.com 和 Tableau 也即将支持。

## Claude Motion：用动画讲解你的想法

让 Claude 把一份季度报告变成用于全员大会的 30 秒讲解动画，给董事会演示中的图表加上动效，或为客户端产品入门制作一段产品导览。Claude 会依据你的提示构建动画，播放起来就像一段短视频。你可以在编辑器中调整，或让 Claude 直接修改，然后下载为 MP4 文件。

![在 Claude 消息框中输入「/motion」即可调出 Motion 选项。](https://assets.claude.com/46f88e8de631c732fa245ad453262e6ef35c0e73.png)

Claude Motion 是为讲解你自己的作品而构建的。Claude 编写代码来为你的文本、图表、形状和图片制作动画，因此你可以修改任何文字、数字或时间点。它不使用视频生成模型，所以没有生成的画面，也没有 AI 生成的人物。如果你想进一步加工，可以在 Adobe、Descript、HeyGen、Higgsfield、invideo、Luma AI 或 Runway 中打开，Canva 和 Captions 也即将支持。

## Docs、Slides 和 Design 已可用于日常工作

[自从我们在每个 Claude 对话中引入 Docs、Slides 和 Design（在新标签页打开）](https://claude.com/resources/articles/cowork-is-now-claude)以来，人们已经在 Claude 中创建了超过 4500 万份[文档、演示文稿和设计](https://claude.com/resources/articles/how-the-product-designer-who-built-claude-design-uses-it-to-explore-ideas-before-building-them)。此后我们发布的大部分内容都来自你们的反馈，让它们每天都更好用。所以我们决定摘掉测试版标签。

* **企业就绪。** Artifacts 现在支持 CMEK，管理员可以选择其组织使用哪些 Artifacts 模板。
* **与团队共同编辑。** 你的团队和 Claude 可以同时处理同一份文档、演示文稿、设计或仪表盘。
* **分享到团队之外。** 在管理员允许的情况下，可以把演示文稿、设计、仪表盘和动画分享给组织外部的人，或任何拿到链接的人。
* **导出保留原有格式。** 下载的 PowerPoint 和 PDF 与你在编辑器中所做的一致，演示文稿还可以[直接输出到 Google Slides](https://claude.com/resources/articles/claude-now-works-in-google-docs-sheets-and-slides)，作为可编辑文件。
* **在手机上编辑。** 在 Claude 移动应用中修改文档、演示文稿或设计。

## Claude Design 已并入 Claude

Claude Design 最初有自己的网址 claude.ai/design。自 9 月 16 日起，Design 也能在每个 Claude 对话内使用，在那里它可以调用你的上下文、文件和连接器。同时维护两个版本会拖慢双方的修复迭代，所以我们把独立站点并入 Claude。独立站点会继续在 [claude.ai/design（在新标签页打开）](http://claude.ai/design) 提供服务，直到 12 月 14 日，因此你有时间迁移过去。

* **今天就迁移你的设计系统。** 在 Claude 的 Artifacts 页面点击「Migrate team design systems」。一次迁移即可把你组织内的所有设计系统迁移过来，原始版本在独立站点关闭前保持不变。
* **你的项目暂时无需你做任何事。** 它们会在独立版本中继续正常工作，直到站点关闭。
* **保存你的聊天记录和评论。** 与 Claude 的对话以及你在项目上的评论留在独立版本中，站点关闭后将不可用。指向独立版本项目的公开链接届时也会失效。

更多信息请参阅[迁移指南（在新标签页打开）](https://support.claude.com/en/articles/17440474)。

## 开始使用

打开 Claude，直接说出你需要什么，比如「做一个本季度按地区划分的收入仪表盘」「把我们的定价方案对比做成动画，用于销售启动会」，或者「把这些笔记整理成周一要用的演示文稿」。就从一个你原本要排队等的仪表盘，或一份一页幻灯片装不下的报告开始。

**致 Enterprise 管理员：** Dashboards 和 Motion 默认关闭，你可以在「组织设置 > Artifacts」中开启。Docs、Slides 和 Design 将于 10 月 15 日默认开启，你也可以今天就开启。

---
title: "Claude for Excel 与 PowerPoint 进阶更新"
title_en: "Advancing Claude for Excel and PowerPoint"
date: 2026-03-11
source: https://claude.com/resources/articles/claude-excel-powerpoint-updates
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude for Excel 与 PowerPoint 进阶更新

> 原文：[Advancing Claude for Excel and PowerPoint](https://claude.com/resources/articles/claude-excel-powerpoint-updates) · Claude 博客

Claude for Excel 与 Claude for PowerPoint 现可在所有打开的文件之间共享完整上下文，技能（skills）则让任何工作流都能一键复用。

***更新：** Claude for Word 测试版现已在 Team 和 Enterprise 套餐中提供。（2026 年 4 月 10 日）*

从今天起，[Claude for Excel](https://claude.com/claude-in-excel) 与 [Claude for PowerPoint](https://claude.com/claude-in-powerpoint) 会在所有打开的文件之间共享完整的对话上下文——因此 Claude 在一个应用中所做的每一个动作，都以另一个应用中正在发生的事情为依据。

技能（Skills）现在也可在 Excel 和 PowerPoint 加载项内使用，并且 Claude for Excel 与 PowerPoint 已可通过三大主流云平台访问：Amazon Bedrock、Google Cloud 的 Vertex AI 和 Microsoft Foundry。

这些更新让 Claude 能够在任务、电子表格和幻灯片之间自由切换，使你以更高的效率和质量工作，无需在每一步都重新解释背景。

## 跨 Excel 与 PowerPoint 的一段连续对话

Claude 可以在一个连续的对话中，跨多个 Excel 和 PowerPoint 文件传递上下文——读取单元格数值、编写公式、合并数据集、编辑幻灯片，并把用户对话贯穿于所有打开的 Excel 与 PowerPoint 文件之间。

财务分析师可以从一个打开的工作簿和其他数据源中提取可比公司的财务数据。接着，他可以据此在 Excel 中搭建一张可比公司估值表，把估值摘要放进推介演示文稿，再起草发给董事总经理的邮件——全程无需切换标签页，也无需在每一步重新说明数据集。减少在工具之间的来回折腾，正是更快交付最终成果的关键。

## 用技能把最佳实践变成一键操作

[技能（Skills）](https://support.claude.com/en/articles/12512180-use-skills-in-claude)把完整的操作流程变成一键操作。当团队中有人摸索出运行差异分析或使用公司模板撰写客户演示文稿的正确方法时，把它保存为技能，就能让这一流程在今后即刻可复用。

![](https://assets.claude.com/744b20022fb320feea15ebffd9a86f712893f9af.png)

我们已发布一套预置的入门技能，覆盖最常见的 Excel 和 PowerPoint 使用场景。对于 Excel，入门技能覆盖财务分析中最常出现的工作流：

* 审计模型中的公式错误与资产负债表完整性
* 构建并填充 LBO、DCF 和三表模型模板
* 运行可比公司分析
* 清理杂乱的电子表格数据——可以是某个区域、当前工作表或整个文件

对于 PowerPoint，入门技能覆盖分析之后的演示文稿层面的工作：

* 构建竞争格局演示文稿，包括市场定位与同业深度分析
* 用新信息或补充数据更新现有演示文稿
* 审阅投资银行演示文稿，检查数字一致性、数据与叙事的一致性以及语言打磨

你已通过桌面端或网页端在 Claude 中设置的每一个技能——无论是个人的还是组织范围的——都能像 MCP 连接器那样，在加载项中开箱即用。Excel 和 PowerPoint 的入门技能也可通过[财务分析插件](https://github.com/anthropics/financial-services-plugins/tree/main/financial-analysis/skills)获取，该插件会在两个加载项中自动安装。此后向该插件新增的技能也无需任何额外配置即可使用。

最后，[指令（instructions）](https://support.claude.com/en/articles/12512180-use-skills-in-claude)用于处理那些应当始终生效的、应用层面的持久偏好。这可能包括：在 Excel 中始终使用公司的数字格式、让 PowerPoint 的项目符号保持单行，或标记出引用了硬编码假设的单元格。指令只需设置一次，之后无需额外提示即可自动应用。Claude 也可以帮你撰写和编辑指令。

## 部署灵活性

Claude for Excel 与 PowerPoint 现在能够在客户既有合规体系所在之处与其对接。组织可以使用 Claude 账户访问这两个加载项，也可以将流量经由现有的 LLM 网关路由到运行在 Amazon Bedrock、Google Cloud 的 Vertex AI 或 Microsoft Foundry 上的 Claude 模型。参见[指南](https://support.claude.com/en/articles/13945233-use-claude-in-excel-and-powerpoint-with-an-llm-gateway)，了解如何通过 LLM 网关使用 Claude for Excel 与 PowerPoint。

Claude 还为 [Excel 原生的 Agent Mode](https://support.microsoft.com/en-gb/topic/use-claude-with-agent-mode-in-excel-b2c3b3ec-154b-484b-84d0-914a80df395a) 提供支持，因此 Microsoft 365 Copilot 客户可以与 Copilot 并肩构建、编辑和分析工作簿。

## 快速上手

所有付费套餐的 Mac 和 Windows 用户都可以在测试版中体验 [Claude for Excel](https://claude.com/claude-in-excel)（[参见指南](https://support.claude.com/en/articles/12650343-use-claude-for-excel)）与 [Claude for PowerPoint](https://claude.com/claude-in-powerpoint)（[参见指南](https://support.claude.com/en/articles/13521390-use-claude-in-powerpoint)）之间改进后的互通能力。Excel 和 PowerPoint 中的技能也在所有付费套餐中提供。想了解充分利用这些新工具的最佳实践，请[报名参加我们的网络研讨会](https://claude.com/resources/webinars/best-practices-for-claude-in-excel-and-powerpoint)。

我们为与 Microsoft 的合作感到自豪，并希望帮助更多人一起体验 Microsoft 365 与 Claude 的强大能力。

‍

---
title: "用贡献度指标了解 Claude Code 的影响"
title_en: "Understand Claude Code’s impact with contribution metrics"
date: 2026-01-29
source: https://claude.com/resources/articles/contribution-metrics
crawled: 2026-11-17
translated: 2026-11-17
---

# 用贡献度指标了解 Claude Code 的影响

> 原文：[Understand Claude Code’s impact with contribution metrics](https://claude.com/resources/articles/contribution-metrics) · Claude 博客

今天，我们在 Claude Code 中推出贡献度指标（contribution metrics），目前处于公开 beta 阶段。工程团队现在可以衡量 Claude Code 对团队开发速度的影响，跟踪在 Claude 帮助下交付的 PR 和提交的代码。

## **我们在 Anthropic 是如何交付的**

Anthropic 的工程团队广泛使用 Claude Code，贡献数据也帮助我们量化了它的影响。随着 Claude Code 在内部采用率的提升，我们看到每位工程师每天合并的 PR 数量增长了 67%。在各团队中，如今 70%–90% 的代码是在 Claude Code 协助下编写的。

虽然单看拉取请求并不能完整衡量开发者速度，但我们发现它是一个相当贴近的代理指标，能够反映工程团队真正在意的事：更快地交付功能、修复缺陷、让用户满意。

Claude Code 中新增的贡献度指标，能帮助你在自己的组织中衡量这种影响。

## **用 Claude Code 衡量开发速度**

通过与 GitHub 集成，贡献度指标会呈现以下数据：

- **已合并的拉取请求**：跟踪有和没有 Claude Code 协助时创建的 PR
- **已提交的代码**：查看有和没有 Claude Code 协助时提交到仓库的代码行数
- **按用户划分的贡献数据**：识别团队内的采用模式

贡献数据的计算方式，是将 Claude Code 的会话活动与 GitHub 的提交和 PR 进行匹配。我们采用保守的统计方式，只有在我们高度确信 Claude Code 参与的情况下，相应代码才会被计为「协助」。

![](https://assets.claude.com/006b8b641d3888dd312c8bd9ff3aeb6cf8773323.png)![](https://assets.claude.com/b76efb0d26f9a49a9823e47bc9b4dd17284eaf87.png)

这些指标会显示在你现有的 Claude Code 分析仪表盘中，工作区管理员和所有者均可访问。无需外部工具或数据管道。只要安装我们的 GitHub App 并向组织的 GitHub 账户完成认证，指标就会自动填充到仪表盘中。

贡献度指标旨在补充你现有的工程 KPI。把它与 DORA 指标、冲刺速度或其他度量并用来观察，就能了解把 Claude Code 引入团队所带来的方向性变化。

## **开始使用**

代码贡献度指标现以 beta 形式向 Claude Team 和 Enterprise 客户提供。启用方式：

1. 为你的组织安装 [Claude GitHub App](https://github.com/apps/claude)
2. 进入[管理设置 > Claude Code](http://claude.ai/admin-settings/claude-code)，开启 GitHub Analytics
3. 向你的 GitHub 组织完成认证

随着团队使用 Claude Code，指标会自动开始填充。详细设置说明和指标解读指引，请参阅[文档](https://code.claude.com/docs/en/analytics)。

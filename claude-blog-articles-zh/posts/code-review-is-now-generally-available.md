---
title: "Code Review 正式发布"
title_en: "Code Review is now generally available"
date: 2026-10-15
source: https://claude.com/resources/articles/code-review-is-now-generally-available
crawled: 2026-11-17
translated: 2026-11-17
---

# Code Review 正式发布

> 原文：[Code Review is now generally available](https://claude.com/resources/articles/code-review-is-now-generally-available) · Claude 博客

在更多 bug 进入生产环境之前抓住它们。

* 分类：[产品更新](/resources/product-updates)
* 产品：Claude Code
* 日期：2026 年 10 月 15 日
* 阅读时长：3 分钟

Code Review 已结束研究预览，现面向 Claude Team 和 Enterprise 组织开放。

> 符合条件的 Claude Enterprise 组织可在 2027 年 1 月 15 日前申领至少 10,000 美元的 Code Review 额度。额度自申领之日起 30 天后过期。[适用相关条款。](https://support.claude.com/en/articles/17603594-free-code-review-promotional-credits-for-claude-enterprise)

### Code Review 的新变化

编程智能体不断提升团队编写代码的速度，而[审查瓶颈](https://claude.com/resources/articles/the-ai-native-sdlc-playbook)并未缓解。为正式发布，我们让 Code Review 更快、更擅长发现真正重要的 bug，也更容易按你的每个仓库进行调优。

自我们发布[研究预览](https://claude.com/resources/articles/code-review)以来，Code Review 变得更加敏锐，能抓住更多原本会进入生产环境的 bug。我们也在 Anthropic 内部的拉取请求上运行 Code Review，从中看到审查在哪些环节拖慢了自己的工程师。预览期间使用 Code Review 的团队告诉我们其余的问题：它确实能在人类审查者查看 PR 之前抓住真实问题，但他们希望审查更安静、按每次改动的大小进行适配，并且更快。以下是我们交付的改进：

* **速度：** 与预览期间相比，大多数审查现在完成速度快约 3 倍（从约 20 分钟降至 6–10 分钟）。
* **质量：** 发现更多真正重要的 bug，并以清晰简洁的发现说明问题是什么、由什么触发，以及用几句话给出修复方案。
* **灵活性：** 管理员可为每个仓库选择 Quick、Standard（默认）或 Deep，让日常代码库获得快速审查，最关键的项目则获得深度审查。每个级别都提供高质量的审查。

### 开始使用

Code Review 现已面向 Team 和 Enterprise 套餐正式发布。

* **管理员**：在 [Claude Code 设置](http://claude.ai/admin-settings/claude-code)中启用 Code Review，安装 GitHub App，并选择你希望运行审查的仓库。
* **开发者**：启用后，审查会在新的 PR 上自动运行，无需任何配置。

查阅[文档](http://code.claude.com/docs/en/code-review)了解更多信息。

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

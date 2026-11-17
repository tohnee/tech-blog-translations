---
title: "用 mods 定制 Claude Code"
title_en: "Customize Claude Code with mods"
date: 2026-10-01
source: https://claude.com/resources/articles/claude-code-mods
crawled: 2026-11-17
translated: 2026-11-17
---

# 用 mods 定制 Claude Code

> 原文：[Customize Claude Code with mods](https://claude.com/resources/articles/claude-code-mods) · Claude 博客

*用几行 TypeScript 改变 Claude Code 的行为与外观。*

今天我们推出 mods——用小型 TypeScript 函数来改变 Claude Code 的工作方式。一个 mod 可以重写提示词、添加新的界面、替换内置功能，或增加全新的功能。你可以自己编写 mod，也可以让 Claude Code 替你写。mods 随插件一起分发，因此你可以像安装和分享任何插件一样安装和分享它们。它们可在 Claude Code CLI 和桌面应用中工作。

mods 运行时对机器的访问权限与 Claude Code 本身相同。它们没有沙箱隔离，因此你只应从信任的来源安装 mods，就像你在电脑上安装任何代码一样。

想了解 mods 能做什么，请[阅读我们的第一个 mod 构建指南](https://claude.dev/blog/getting-started-with-claude-code-mods/)。

### 为什么我们要做 mods

开发者希望对自己的 Claude Code 工作方式有更多控制，而不必等待我们发布某个功能。[Hooks](https://code.claude.com/docs/en/hooks) 帮助用户获得了一部分控制能力，但 hooks 无法重写事件、绘制新界面或替换功能。mods 可以。

我们希望 Claude Code 用起来像是你自己的工具，让你能按自己的工作方式塑造它。在发布之前，我们[在 GitHub 上公开了 mods 的设计](https://github.com/anthropics/claude-code/issues/91870)，以收集开发者的反馈。感谢每一位参与讨论的人。

### mods 的工作原理

Claude Code 每次执行操作时都会发出一个事件。例子包括调用工具、请求权限，以及绘制屏幕的一部分。mod 就是挂接到这些事件之一的函数。mod 可以在事件之前运行、在事件之后运行，或替代该事件运行。它还可以包裹事件，在事件前后都执行代码。通过一个函数，mod 可以：

* 在提示词到达模型之前重写它。
* 阻止、重写或重试一次工具调用。
* 批准或拒绝一次权限请求。
* 在 Claude 读取工具输出之前，从中抹除密钥信息。

mod 还能改变你看到的内容。它可以编辑或替换 Claude Code 绘制的界面的一部分，例如某个工具结果或 Claude 的提问。它可以添加按钮和输入框，其他 mod 可以在你按下它们时做出响应。目前，一个 mod 可以针对终端、桌面应用或两者。

当多个 mod 挂接同一个事件时，它们按加载顺序运行。最先加载的 mod 最先看到事件，最后看到结果。这让你可以叠加来自不同作者的 mod。

你也可以用 Claude Code 来为 Claude Code 做 mod。请 Claude 创建一个 mod，它可以编写 TypeScript、安装它，并在你的会话中热重载。

### 用你自己的实现替换内置功能

Claude Code 的一些内置功能现在以 mod 形式提供。例如，内置的 `/diff` 功能现在就是一个 mod，因此你可以在 `/plugin` 中将它关闭，或用你自己的版本替换它。我们计划逐步把更多内置功能迁移为 mods，这样你就可以把 Claude Code 精简到一个很小的核心，只添加你需要的部分。

### 面向团队和企业的 mods

mods 随插件一起分发，因此你现有的插件管控措施同样适用。管理员可以允许或阻止插件市场。在 Team 和 Enterprise 套餐中，所有者可在管理控制台中设置。在 Claude API 和第三方 API 套餐中，管理员会向用户机器推送受管设置。

在 Team 和 Enterprise 套餐中，以及在任何配置了受管设置的机器上，一个名为 `sec-default`（“security default”，安全默认）的内置 mod 会最先加载。它会阻止用户安装的 mod 执行有风险的操作，例如覆盖你的权限拒绝规则。你可以[查看源代码](http://github.com/anthropics/claude-code/tree/main/mods)了解它限制了什么。管理员也可以改为先加载自己的 mods。如果你这样做，请把 `sec-default` 加入你的列表，以保留其限制。

团队还可以用 mods 构建自己的管控和功能。例如：

* **CI/CD 状态：** 某个 mod 可以在对话旁的窗格中显示流水线状态，并在构建通过或失败时更新。
* **生产环境防护**：某个 mod 可以要求在任何命令触及生产配置之前进行确认。
* **审计日志：** 一个最先加载的 mod 可以记录其他所有 mod 发起的每一次调用。

### 开始使用

mods 现已在 Claude Code CLI 和桌面应用中可用。可从 [Claude 目录](https://claude.ai/directory)安装包含 mods 的插件，或在 CLI 中运行 `/plugin`。要分享一个 mod，请将其打包进插件并[提交到目录](https://claude.ai/directory/manage)。

要构建你自己的 mods，请阅读我们的[入门指南](https://claude.dev/blog/getting-started-with-claude-code-mods/)或查看[文档](https://code.claude.com/docs/en/plugins/mods/overview)。

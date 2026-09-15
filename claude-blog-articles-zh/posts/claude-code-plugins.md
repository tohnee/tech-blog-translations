---
title: "用插件自定义 Claude Code"
title_en: "Customize Claude Code with plugins"
source: https://claude.com/blog/claude-code-plugins/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用插件自定义 Claude Code

> 原文：[Customize Claude Code with plugins](https://claude.com/blog/claude-code-plugins/) · Claude 博客

### 用插件分享你的 Claude Code 配置

斜杠命令（slash command）、agents、MCP 服务器和 hooks 都是你可以用来自定义 Claude Code 体验的扩展点。随着这些功能陆续推出，我们看到用户构建出越来越强大的配置，并希望与团队成员和更广泛的社区分享。我们打造了插件（plugin）来让这件事变得更容易。

插件是一种轻量级方式，可以打包并分享以下任意组合：

- **斜杠命令**：为常用操作创建自定义快捷方式
- **子智能体（subagent）**：安装为专门开发任务定制的智能体
- **MCP 服务器**：通过 Model Context Protocol 连接工具和数据源
- **hooks**：在 Claude Code 工作流的关键节点自定义其行为

你可以在 Claude Code 中使用 `/plugin` 命令直接安装插件，该功能现已进入公测（public beta）。插件可以按需开启和关闭：需要特定能力时启用它们，不需要时禁用，以减少系统提示上下文和复杂度。

今后，插件将成为我们打包和分享 Claude Code 定制的标准方式，并且随着更多扩展点的加入，我们会持续演进这一格式。

### 使用场景

插件帮助你围绕一组共享的最佳实践来标准化 Claude Code 环境。常见的插件使用场景包括：

- **执行标准：** 工程负责人可以使用插件确保特定 hooks 在代码评审或测试工作流中运行，从而在团队内保持一致性
- **支持用户**：例如，开源维护者可以提供帮助开发者正确使用其软件包的斜杠命令
- **分享工作流**：构建了提升生产力工作流（如调试环境、部署流水线或测试执行框架）的开发者可以轻松与他人分享
- **连接工具**：需要通过 MCP 服务器连接内部工具和数据源的团队，可以使用遵循相同安全和配置协议的插件来加速这一过程
- **打包定制**：框架作者或技术负责人可以把相互配合的多项定制打包，用于特定场景

### 插件市场

为了让这些定制更易于分享，任何人都可以构建和托管插件，并创建插件市场（plugin marketplace）——经过策划的插件集合，其他开发者可以在其中发现并安装插件。

你可以使用插件市场与社区分享插件、在组织内分发经过审核的插件，并针对常见开发难题在现有方案的基础上进行构建。

托管一个市场，你只需要一个 git 仓库、GitHub 仓库，或者一个带有格式正确的 `.claude-plugin/marketplace.json` 文件的 URL。详情请参阅我们的文档。

要使用市场中的插件，请运行 `/plugin marketplace add user-or-org/repo-name`，然后通过 `/plugin` 菜单浏览并安装插件。

### 发现新市场

插件市场放大了我们社区已经形成的最佳实践，社区成员正走在前列。例如，工程师 Dan Ávila 的[插件市场](https://www.aitmpl.com/plugins)提供面向 DevOps 自动化、文档生成、项目管理和测试套件的插件；工程师 Seth Hobson 则在他的 [GitHub 仓库](https://github.com/wshobson/agents)中精选了 80 多个专业化子智能体，开发者通过插件即可即时使用。

你还可以看看我们为 PR 评审、安全指导和 [Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) 开发准备的几个[示例插件](https://github.com/anthropics/claude-code)，其中甚至有一个用于创建新插件的元插件。

### 开始使用

插件现已面向所有 Claude Code 用户开放公测。使用 `/plugin` 命令安装后，它们可以在你的终端和 VS Code 中通用。

请查阅我们的文档，[开始使用](https://docs.claude.com/en/docs/claude-code/plugins-reference)、[构建你自己的插件](https://docs.claude.com/en/docs/claude-code/plugins)，或[发布一个市场](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)。想看看插件的实际效果，可以试试我们用来开发 Claude Code 的这个多智能体工作流：

`/plugin marketplace add anthropics/claude-code`

```
/plugin marketplace add anthropics/claude-code
```

```
/plugin install feature-dev
```

FAQ（常见问题）

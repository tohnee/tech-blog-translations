---
title: "使用 CLAUDE.md 文件：为你的代码库定制 Claude Code"
title_en: "Using CLAUDE.MD files: Customizing Claude Code for your codebase"
source: https://claude.com/blog/using-claude-md-files/
crawled: 2026-09-14
translated: 2026-09-14
---

# 使用 CLAUDE.md 文件：为你的代码库定制 Claude Code

> 原文：[Using CLAUDE.MD files: Customizing Claude Code for your codebase](https://claude.com/blog/using-claude-md-files/) · Claude 博客

如果你使用 AI 编码智能体，就会面临同样的挑战：如何在不重复自己的前提下，给它们足够的上下文来理解你的架构、约定和工作流？

随着代码库增长，这个问题会不断加剧。复杂的模块关系、领域特有的模式和团队约定并不容易浮现出来。你最终不得不在每次对话开始时，反复解释同样的架构决策、测试要求和代码风格偏好。

[CLAUDE.md](https://www.anthropic.com/engineering/claude-code-best-practices) 文件通过为 Claude 提供关于你项目的持久上下文来解决这个问题。可以把它看作一个配置文件，Claude 会自动把它纳入每一次对话，确保它始终了解你的项目结构、编码规范和偏好的工作流。

在本文中，我们将带你了解如何组织你的 [CLAUDE.md](http://claude.md)，分享最佳实践，以及如何使用它们来充分发挥 Claude Code 的效力。

## 什么是 CLAUDE.md 文件？

CLAUDE.md 是一个特殊的配置文件，位于你的仓库中，为 Claude 提供项目特定的上下文。你可以把它放在仓库根目录与团队共享，放在父目录中以适配单体仓库（monorepo）结构，或放在你的主文件夹中对所有项目全局生效。

下面是一个你的仓库中可能出现的 CLAUDE.md 示例：

```
# Project Context

When working with this codebase, prioritize readability over cleverness. Ask clarifying questions before making architectural changes.

## About This Project

FastAPI REST API for user authentication and profiles. Uses SQLAlchemy for database operations and Pydantic for validation.

## Key Directories

- `app/models/` - database models
- `app/api/` - route handlers
- `app/core/` - configuration and utilities

## Standards

- Type hints required on all functions
- pytest for testing (fixtures in `tests/conftest.py`)
- PEP 8 with 100 character lines

## Common Commands
```bash
uvicorn app.main:app --reload  # dev server
pytest tests/ -v               # run tests
```

## Notes

All routes use `/api/v1` prefix. JWT tokens expire after 24 hours.

```

一个配置得当的 CLAUDE.md 会改变 Claude 与你具体项目协作的方式。这个文件有多种用途：提供架构上下文、建立工作流、把 Claude 接入你的开发工具。每一处增补都应该解决你实际遇到过的问题，而不是出于"Claude 可能需要什么"的理论担忧。

这个文件可以记录常用的 bash 命令、核心工具、代码风格指南、测试说明、仓库约定、开发环境搭建，以及针对项目的警告事项。它没有固定的格式要求。建议保持文件简洁、人类可读，把它当作人类和 Claude 都需要快速理解的文档来对待。

你的 CLAUDE.md 文件会成为 Claude 系统提示的一部分。每一次对话开始时，这些上下文都已加载完毕，无需再反复解释项目的基本信息。

## **用 /init 起步**

从零创建一个 CLAUDE.md 可能让人望而生畏，尤其是在一个陌生的代码库里。

`/init` 命令可以自动化这一过程：它会分析你的项目并生成一份初始配置。

在任意 Claude Code 会话中运行 `/init`：

```
cd your-project
claude
/init
```

Claude 会检查你的代码库——阅读包文件、现有文档、配置文件和代码结构——然后生成一份为你项目量身定制的 CLAUDE.md。生成的文件通常包含它检测到的构建命令、测试说明、关键目录和编码约定。

把 `/init` 当作一个起点，而不是成品。生成的 CLAUDE.md 能捕捉明显的模式，但可能遗漏你的工作流特有的细节。请审阅 Claude 产出的内容，并根据团队的实际做法加以完善。

你也可以在已有 CLAUDE.md 的项目上使用 `/init`。Claude 会审阅现有文件，并根据探索代码库的所得提出改进建议。

运行 `/init` 之后，可以考虑这些后续步骤：

- 审阅生成内容的准确性
- 补充 Claude 推断不出的工作流说明（分支命名约定、部署流程、代码评审要求）
- 删除不适用于你项目的通用性指导
- 把文件提交到版本控制，让整个团队受益

`/init` 命令很适合快速上手，但真正的价值来自随时间不断迭代生成的文件。在使用 Claude Code 的过程中，用 `#` 键把那些你发现自己在反复交代的内容添加进去——这些补充会逐渐积累成一份真实反映你团队工作方式的 CLAUDE.md。

## 如何组织你的 CLAUDE.md

以下几节将向你展示如何组织内容以获得最大效果：驾驭复杂架构、跟踪多步任务的进度、集成自定义工具，以及通过一致的工作流防止返工。

### 给 Claude 一张地图

每个新任务都要解释一遍项目架构、关键库和编码风格，会变得十分繁琐。你需要 Claude 在无需人工反复强化的情况下，保持对你代码库结构的一致认知。

在你的 CLAUDE.md 中加入项目摘要和高层目录结构。这能让 Claude 在你的代码库中导航时立刻获得方向感。

一个展示关键目录的简单 tree 输出，能帮助 Claude 理解不同组件位于何处：

```
main.py
├── logs
│   ├── application.log
├── modules
│   ├── cli.py
│   ├── logging_utils.py
│   ├── media_handler.py
│   ├── player.py
```

附上关于主要依赖、架构模式以及任何非标准组织方式的信息。如果你使用领域驱动设计、微服务或特定框架，请写明。Claude 会利用这张地图来更好地判断去哪里找代码、在哪里做修改。

### 把 Claude 接入你的工具

Claude 会继承你的完整环境，但需要指引才能知道该使用哪些自定义工具和脚本。你的团队很可能有一些部署、测试或代码生成方面的专用工具，Claude 应当了解它们。

在 CLAUDE.md 中用使用示例记录你的自定义工具。包括工具名称、基本用法模式，以及何时调用它们。如果你的工具通过 `--help` 标志提供帮助文档，请提及这一点，让 Claude 知道要去查看。对于复杂工具，可以补充团队常用的调用示例。

Claude 作为 MCP（Model Context Protocol）客户端运行，连接到扩展其能力的 MCP 服务器。可以通过项目设置、全局配置或纳入版本控制的 `.mcp.json` 文件来配置它们。当工具没有按预期出现时，`--mcp-debug` 标志有助于排查连接问题。

例如，如果你的组织配置了一个 Slack MCP 服务器，而你需要 Claude 知道如何使用它，可以在 CLAUDE.md 中加入类似这样的内容：

```
### Slack MCP
- Posts to #dev-notifications channel only
- Use for deployment notifications and build failures
- Do not use for individual PR updates (those go through GitHub webhooks)
- Rate limited to 10 messages per hour
```

进一步了解 MCP 的[基础知识与最佳实践](https://www.anthropic.com/engineering/building-effective-mcp-servers)。

有关为 Claude Code 设置权限的更多信息，请参阅 [code.claude.com](https://code.claude.com/docs/en/settings) 上的 settings.json 文档。

### **定义标准工作流**

让 Claude 不做规划就直接动手改代码会导致返工。Claude 可能实现出偏离需求的方案、选错架构路线，或者做出破坏现有功能的修改。

你需要 Claude 三思而后行。在 CLAUDE.md 中定义 Claude 在处理不同类型任务时应遵循的标准工作流。一个可靠的默认工作流会在动手修改之前先回答四个问题：

1. 这是不是一个关于当前状态、需要先做调查的问题？
2. 这是否需要在实现之前制定详细计划？
3. 还缺少哪些额外信息？
4. 效果将如何验证？

具体的工作流可以包括：面向功能开发的 explore-plan-code-commit、面向算法工作的测试驱动开发，或面向 UI 改动的视觉迭代。把你的测试要求、提交信息格式以及任何审批步骤写进文档。当 Claude 事先了解你的工作流时，它会把工作组织得符合你团队的实际流程，而不是靠猜测。

一条工作流指令的示例可能是：

```
1) Before modifying code in the following locations: X, Y, Z
	- Consider how it might affect A, B, C
	- Construct an implementation plan
	- Develop a test plan that will validate the following functions...
```

## **与 Claude Code 协作的更多技巧**

除了配置 CLAUDE.md 文件之外，还有三种技巧可以改善你与 Claude Code 的协作方式。

### **保持上下文新鲜**

与 Claude Code 协作的时间久了，会积累起无关的上下文。早期任务的文件内容、不再重要的命令输出、以及偏题的对话，都会填满 Claude 的上下文窗口。随着信噪比下降，Claude 会难以保持对当前任务的专注。

在不同任务之间使用 `/clear` 来重置上下文窗口。这会清除累积的历史，同时保留你的 CLAUDE.md 配置，让 Claude 能带着新鲜上下文处理新问题。可以把它想象成结束一个工作时段、开启另一个。

当你调试完认证问题、转而实现一个新的 API 端点时，请清空上下文。认证的细节已经不再重要，只会干扰新工作。

### **在不同阶段使用子智能体**

长对话积累的上下文会干扰新任务。你刚调试完一个复杂的认证流程，现在需要对同一份代码做安全评审。调试的细节会影响 Claude 的安全分析，可能导致它忽略问题，或者纠结于已经解决的事情。

让 Claude 在不同的工作阶段使用[子智能体](https://code.claude.com/docs/en/sub-agents)。子智能体维护着相互隔离的上下文，能防止早期任务的信息干扰新的分析。实现完一个支付处理器之后，指示 Claude "用一个子智能体对那段代码执行安全评审"，而不是在同一对话中继续。

子智能体最适合用于每个阶段需要不同视角的多步工作流。实现工作需要架构上下文和功能需求；安全评审则需要只关注漏洞的全新视角。上下文分离能让两种分析都保持敏锐。

### **创建自定义命令**

重复的提示浪费时间。你发现自己一遍又一遍地输入"审查这段代码的安全问题"或"分析这段代码的性能问题"。每次都要记住能带来好结果的确切措辞。

自定义斜杠命令把这些内容保存为 markdown 文件，放在你的 `.claude/commands/` 目录下。创建一个名为 `performance-optimization.mm` 的文件，写上你偏好的性能优化提示，它就会在任何对话中以 `/performance-optimization` 的形式可用。命令支持通过 $ARGUMENTS 或 `$1`、`$2` 这类编号占位符传入参数，让你传递具体的文件或参数。

例如，`performance-optimization.md` 可能如下所示：

```
# Performance Optimization

Analyze the provided code for performance bottlenecks and optimization opportunities. Conduct a thorough review covering:

## Areas to Analyze

### Database & Data Access
- N+1 query problems and missing eager loading
- Lack of database indexes on frequently queried columns
- Inefficient joins or subqueries
- Missing pagination on large result sets
- Absence of query result caching
- Connection pooling issues

### Algorithm Efficiency
- Time complexity issues (O(n²) or worse when better exists)
- Nested loops that could be optimized
- Redundant calculations or repeated work
- Inefficient data structure choices
- Missing memoization or dynamic programming opportunities

### Memory Management
- Memory leaks or retained references
- Loading entire datasets when streaming is possible
- Excessive object instantiation in loops
- Large data structures kept in memory unnecessarily
- Missing garbage collection opportunities

### Async & Concurrency
- Blocking I/O operations that should be async
- Sequential operations that could run in parallel
- Missing Promise.all() or concurrent execution patterns
- Synchronous file operations
- Unoptimized worker thread usage

### Network & I/O
- Excessive API calls (missing request batching)
- No response caching strategy
- Large payloads without compression
- Missing CDN usage for static assets
- Lack of connection reuse

### Frontend Performance
- Render-blocking JavaScript or CSS
- Missing code splitting or lazy loading
- Unoptimized images or assets
- Excessive DOM manipulations or reflows
- Missing virtualization for long lists
- No debouncing/throttling on expensive operations

### Caching
- Missing HTTP caching headers
- No application-level caching layer
- Absence of memoization for pure functions
- Static assets without cache busting

## Output Format

For each issue identified:
1. **Issue**: Describe the performance problem
2. **Location**: Specify file/function/line numbers
3. **Impact**: Rate severity (Critical/High/Medium/Low) and explain expected performance degradation
4. **Current Complexity**: Include time/space complexity where applicable
5. **Recommendation**: Provide specific optimization strategy
6. **Code Example**: Show optimized version when possible
7. **Expected Improvement**: Quantify performance gains if measurable

If code is well-optimized:
- Confirm optimization status
- List performance best practices properly implemented
- Note any minor improvements possible

**Code to review:**
```
$ARGUMENTS
```
```

你不需要手动编写自定义命令文件。可以让 Claude 替你创建：

```
Create a custom slash command called /performance-optimization that analyzes code for database query issues, algorithm efficiency, memory management, and caching opportunities.

```

Claude 会把 markdown 文件写入 `.claude/commands/performance-optimization.md`，该命令立即可用。

## **从简单开始，有意识地扩展**

一上来就创建一份面面俱到的 CLAUDE.md 很有诱惑力。请克制这种冲动。

CLAUDE.md 每次都会被加入 Claude Code 的上下文，因此从[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)和[提示工程](https://www.anthropic.com/engineering/prompt-engineering-overview)的角度出发，请保持它简洁。一种做法：把信息拆分到单独的 markdown 文件里，在 CLAUDE.md 文件中引用它们。

不要包含敏感信息、API 密钥、凭据、数据库连接字符串或详细的安全漏洞信息——尤其是在你把文件提交到版本控制的情况下。既然 CLAUDE.md 会成为 Claude 系统提示的一部分，就请把它当作可能被公开分享的文档来对待。

## **让 CLAUDE.md 为你所用**

CLAUDE.md 文件把 Claude Code 从一个通用助手变成了一个专门为你的代码库配置的工具。从基本的项目结构和构建文档起步，再根据工作流中实际的摩擦点逐步扩展。

最有效的 CLAUDE.md 文件解决的是真实问题：它们记录你反复输入的命令，捕捉需要花十分钟才能讲清的架构上下文，并建立防止返工的工作流。你的文件应当反映你团队实际开发软件的方式——而不是那些听起来不错却不符现实的"理论最佳实践"。

把定制当作一项持续的实践，而不是一次性的配置任务。项目在变，团队会学到更好的模式，新工具也会进入你的工作流。一份维护良好的 CLAUDE.md 会随着你的代码库一起演进，持续降低在复杂软件上借助 AI 协作的摩擦。

***立即开始使用***[***Claude Code***](https://www.claude.com/product/claude-code)***。***

FAQ（常见问题）

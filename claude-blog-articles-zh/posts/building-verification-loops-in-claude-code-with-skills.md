---
title: "用 Skills 在 Claude Code 中构建验证回路"
title_en: "Building verification loops in Claude Code with skills"
source: https://claude.com/blog/building-verification-loops-in-claude-code-with-skills/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 Skills 在 Claude Code 中构建验证回路

> 原文：[Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills/) · Claude 博客

大多数[智能体编码](https://claude.com/blog/introduction-to-agentic-coding)会话都遵循一个循环：你提出修改需求，Claude 收集上下文、采取行动、验证结果，并在需要时回过头去收集更多上下文。

验证是智能体在给出回答之前检查自己工作的方式。Claude 已经会通过观察你代码库中的确定性信号来做一部分验证，包括类型检查器、linter、测试和运行时错误。而 Claude 无法推断出的部分，就变成了你手动检查功能时要执行的步骤。

不过，这些手动步骤可以转化为验证回路（verification loop）。在 [Claude Code](https://claude.com/product/claude-code) 中，验证回路是一个迭代过程，Claude 会在其中检查并尝试修复工作成果。

*智能体循环：1. 收集上下文，2. 采取行动，3. 验证结果。*

在本文中，我们将介绍最常见的几类验证回路，并展示我们在 Anthropic 内部的用法。然后我们会说明如何把你已经在做的手动检查编码为技能（skill），让 Claude 闭合自己的反馈回路，而你可以在它迭代时去忙别的事情。

刚接触智能体循环？请从 [loops 入门](https://claude.com/blog/getting-started-with-loops)读起。

## 什么是验证回路？

验证回路是一个不断重复的循环：AI 智能体检查自己的工作——运行测试、linter 或自定义检查——并在继续推进之前修复未通过的部分。在 Claude Code 中，验证回路可以打包为技能（skill），这样每次会话都会自动执行同样的检查，而不必依赖某个人记得去做。

## 内置验证回路

在深入设计自定义验证回路之前，先了解 Claude 对多种不同验证回路的内置支持会很有帮助。常见的功能和方法包括：

- **/verify 技能**：构建、运行并观察你的应用中的变更。
- **工具链（toolchain）**：Claude 会尽力捕捉并处理你提供的任何工具（例如 linter）给出的错误码和警告。一个良好的实践是在 CLAUDE.md 中列明确切的构建和测试命令，这样 Claude 就不必靠猜测。
- **Code Review（研究预览（research preview））**：一项托管的多智能体服务，会在你启用的仓库中对 PR 运行自动化评审。你可以手动修复发现的问题并推送，也可以通过在该发现下评论 @claude 来闭合回路（前提是你已经设置并配置了下文的 GitHub Actions）。
- **GitHub Actions**：定义一个调用 Claude 并使用验证技能的 job，你在本地运行的同样检查就会在每次推送或 PR 时自动触发。
- **Spec validation（规格校验）**：一种技能，帮助你对照仓库中的 markdown 规格文档验证每一处变更，并尝试修复违规之处。
- **Claude Managed Agents 中的评分规则（rubrics，beta）**：一项托管的智能体服务，允许你用一个单独的评分智能体（grader agent）对照评分规则验证结果。未通过的部分会自动回炉返工。

## 编写验证回路

如果你有一个现有项目，并且发现自己每次在 Claude 实现新功能后都要做同样的小修正，那就是时候把这些步骤变成你自己的自定义验证回路了。第一步，把你每次都在重复做的事情全部写下来。

如果你在启动一个新项目、需要想清楚项目应有的行为，道理也一样。用平实的英文写出最佳实践版本，就像第一天交接给新同事那样。

如果你难以把验证检查本身讲清楚，可以先让 Claude 给出最佳实践，再在其基础上修改。你的版本大概会在若干具体要点上有所不同，而这些差异恰恰是你想要捕捉的东西。

**专业提示**：能进入这里的检查不一定非得是定性判断。「拒绝任何在没有回填步骤的情况下删除列的数据库迁移」就是一条确定性规则——通用 linter 抓不住它，但项目专属的 linter 可以。任何你需要反复以手动检查的方式强制执行的事情，都有资格被捕获为回路。

## 把它做成技能

把重复步骤编码为验证回路的最常见方式，是把它写成[技能](https://claude.com/blog/complete-guide-to-building-skills-for-claude)，而创建技能最快的方式，是安装 skill-creator 插件并让 Claude 对你进行访谈：

示例：

```
/skill-creator Create a skill for verifying frontend changes end-to-end. Interview me about my workflow.
```

你也可以手写技能：在项目的 .claude/skills/ 目录下放入一个 markdown 文件即可。最简单的验证技能只需几行 frontmatter 加一段正文：

```
# .claude/skills/verify-log-hygiene/SKILL.md
---
name: verify-log-hygiene
description: Check that error logs include the request ID and never
  include the request body. Use when the diff touches error handling
  or logging.
allowed-tools: [Read, Edit, Grep]
---
Read the error-handling paths in the current diff.

For each log call on an error path, confirm it includes the request ID
and does not pass the request body, headers, or any user-supplied payload.

Report each violation with file:line, then fix it: add the request ID
where it's missing and strip the payload from the log call.

```

完整的 schema 及其背后的设计理念，请参阅我们的[构建技能完全指南](https://claude.com/blog/complete-guide-to-building-skills-for-claude)。

## 让检查匹配它运行的位置

接下来要确定的是验证回路如何启动：独立运行（standalone）、内嵌（embedded）、链式（chained），还是绑定到 PR。

### 独立运行

由你有意识地调用，在产物已经存在之后运行。独立技能的用武之地是那些并非每次都适用的横切检查：提交前的安全扫描、PR 前的可访问性审计、跨仓库的许可证头文件校验。凡是你希望在很多工作流中可用、但不希望每次代码变更都触发的检查，都适合这种形式。

代价是每次调用仍然是你必须记得去做的一步。当你发现自己每次变更后都在运行它时，就说明独立运行已经不够了。此时这套流程已经赢得了一个固定席位：把它内嵌或串联起来。

### 内嵌

作为产出型技能的一部分自动触发。检查属于某个特定的工作流，而该工作流现在无需你开口就会执行它。

最简单的形式是在产出型技能的正文末尾追加一行：

```
# .claude/skills/scaffold-component/SKILL.md
---
name: scaffold-component
description: Scaffold a new React component under src/components/, including the component file, its co-located test, and an index export. Use when the user asks to create a new component.
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# Scaffold a new React component

Given a component name (PascalCase), create the following under `src/components/<Name>/`:

1. `<Name>.tsx`: function component with a typed props interface and a default export.
2. `<Name>.test.tsx`: React Testing Library test that renders the component and asserts it mounts without throwing.
3. `index.ts`: re-export the default and any named exports.

Follow the patterns in `src/components/Button/` as the reference. Match the import alias style (`@/components/...`) used throughout the codebase.

# code continues...

After creating the component file, run eslint on it and
address any errors before reporting completion.

```

要验证内嵌是否生效，可以在一个新任务上调用该技能，并确认新增步骤作为输出的一部分运行了。如果没有，说明技能的 description 或前文指令没有把追加的检查带进来。

内嵌只对你可以编辑的技能有效：你自己编写的技能，或以项目级别安装、SKILL.md 文件由你掌控的技能。内置技能和由插件管理的技能（即更新时会被覆盖的那种）不适用这一模式；对它们，请改用链式方式。

跨工作流的检查请跳过内嵌；它们更适合独立运行，这样你可以在任何上下文中调用。

### 链式

一个技能在结尾调用另一个技能，多个经过验证的交接便端到端地运行起来。

Anthropic Claude Code 团队的成员在日常工作中使用这一模式：/code-review 搜寻 bug，/simplify 清理 diff，/verify 技能确认端到端行为，而当变更涉及 UI 时，自定义的 /design 技能会对照 DESIGN.md 文件中的准则进行检查。

链式也是你为无法修改的技能添加验证的方式：构建一个自定义包装技能，先调用原技能，再调用你的验证技能，如下所示：

```
# .claude/skills/safe-refactor/SKILL.md
Run /simplify on the current diff first.
When /simplify finishes, invoke /verify-no-public-api-changes.
```

原本是一种习惯（「我总是在 /simplify 之后运行 /verify」），现在变成了一份契约（「/simplify 完成时总会运行 /verify」）。这条链会自动跑完整个开发周期，只有在有事情升级交还给你时你才需要介入。

如果各步骤足够独立、你有时希望单独运行其中一个，那就可以跳过链式；链式是用灵活性换取自动化。链式验证回路可能增加 token 消耗，因此最好先测试这些回路，再大范围部署。

### 在每个 PR 上

一旦这条链在你的变更上稳定可靠，同一套流程就可以在每个 PR 上运行。同事的变更将经历与你的变更相同的关卡，无论他们是否记得调用这条链。这套基础设施与你已经写好的链是同一类东西，只是更进一步：同样的技能、同样的评分规则、同样的标准，不再依赖作者的自觉。

正是在这里，验证不再是个人基础设施，而成为[团队基础设施](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start)。你当初为每周省下两分钟而写下的检查，现在正在每次变更中为每个人每周省下两分钟。当这条链仍在频繁调整时，请暂缓部署 PR 级别的关卡；每一次调整都会成为团队可见的事件。

一旦你掌握了这套流程，就可以扩展你的回路工程了。无论你自动化的是什么、在什么环境中，验证回路的创建流程都是一致的：

1. 挑出你这周做得最多的一项手动后续操作。
2. 先试用内置的 /verify 技能，看看它是否有助于你的流程。
3. 用平实的英文写出这套流程，就像第一天交接给新同事那样。
4. 把它交给 skill-creator，或者自己把 markdown 文件放进 .claude/skills/。
5. 在一个新任务上调用它，确认检查作为输出的一部分运行，必要时迭代。
6. 尝试技能串联，打造端到端的验证流程。

你能为 Claude 编码的遵循规则越多，Claude 的回答就越有可能在第一次尝试时就贴近你的期望。那些你不再需要费心修正的问题，把你的注意力解放出来，投注到没有任何技能能替你写下的、专属于你个人的工作上。

***在 Claude Code 中开始使用验证回路***。

*本文由 Claude Code 团队成员 Delba de Oliveira 撰写。*

FAQ（常见问题）

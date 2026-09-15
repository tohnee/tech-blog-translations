---
title: "循环工程：loops 入门"
title_en: "Loop engineering: Getting started with loops"
source: https://claude.com/blog/getting-started-with-loops/
crawled: 2026-09-14
translated: 2026-09-14
---

# 循环工程：loops 入门

> 原文：[Loop engineering: Getting started with loops](https://claude.com/blog/getting-started-with-loops/) · Claude 博客

## loops 入门

现在有很多关于循环工程（loop engineering）或"设计循环"的讨论——不再是一句句提示你的编程智能体，而是设计循环。如果你花点时间在 X 上试图搞清楚 loop 到底是什么，你会遇到好几种不同的答案。

在 Claude Code 团队，我们把 **loops 定义为智能体不断重复工作循环，直到满足停止条件**。我们按照以下几点对循环进行分类：

- 如何被触发
- 如何被停止
- 使用了哪种 Claude Code 原语（primitive）
- 各自最适合哪类任务。

我们会介绍主要的循环类型、各自的使用时机，以及如何在管理 token 用量的同时保持代码质量。并非所有任务都需要复杂的循环；从最简单的方案开始，有选择地使用这些模式。

## **回合式循环（Turn-based loops）**

- **触发方式**：用户的一条提示。
- **停止条件**：Claude 判断自己已完成任务，或需要更多上下文。
- **最适合**：不属于常规流程或定时安排的较短任务。
- **用量管理方式**：编写具体的提示，并借助技能（skills）改进验证，以减少回合数。

你发出的每一条提示都会启动一个手动循环，由你指挥每一个回合。Claude 收集上下文、采取行动、检查自己的工作、必要时重复，然后给出回应。我们称之为智能体循环（agentic loop）。

例如，让 Claude 创建一个点赞按钮。它会阅读你的代码、做出修改、运行测试，然后交回一个它*认为*可用的结果。接下来由你手动检查这些工作，并写下下一条提示。

你可以改进验证这一步：把你的手动步骤编码为一个 SKILL.md，让 Claude 能够端到端地检查更多自己的工作。（关于这类自动化该如何在 skills、hooks 和 subagents 之间做选择，请参阅我们的[驾驭 Claude Code](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) 指南。）

其中应当包含能让 Claude *看到*、*度量*或*交互*结果的工具或连接器。检查越量化，Claude 就越容易自我验证。

例如，你可以在 SKILL.md 文件中这样写：

```
--- 
name: verify-frontend-change 
description: Verify any UI change end-to-end before declaring it done. 
--- 

# Verifying frontend changes 
Never report a UI change as complete based on a successful edit alone. Verify it the way a human reviewer would: 

1. Start the dev server and open the edited page in the browser. 

2. Interact with the change directly. For a new control (button, input, toggle): click it, confirm the expected state change, and screenshot before/after. 

3. Check the browser console: zero new errors or warnings. 

4. Use the Chrome Devtools MCP, run a performance trace and audit Core Web Vitals.

If any step fails, fix the issue and rerun from step 1 — do not hand back partially verified work.

```

## **基于目标的循环（/goal）**

- **触发方式**：实时的手动提示。
- **停止条件**：目标达成，或达到最大回合数。
- **最适合**：具有可验证退出条件的任务。
- **用量管理方式**：设定明确的完成标准和显式的回合上限，比如"试 5 次就停"。

有时候，单个回合并不够，尤其是对更复杂的任务。能迭代时智能体的表现会更好。你可以用 /goal 定义"完成"是什么样子，从而延长 Claude 持续迭代的时间。

当你定义了成功标准，Claude 就不必自行判断什么算"足够好"而过早结束循环。每当 Claude 试图停下时，一个评估者模型（evaluator model）会检查你设定的条件，并把它送回去继续工作，直到目标达成，或达到你定义的回合数。

这就是为什么确定性的标准——比如通过的测试数量，或是否越过某个分数阈值——如此有效。

例如：

```
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
```

## **基于时间的循环（/loop 和 /schedule）**

- **触发方式**：指定的时间间隔。
- **停止条件**：你取消它，或工作完成（PR 合并、队列清空）。
- **最适合**：周期性工作，或与外部环境/系统对接。
- **用量管理方式**：设置更长的间隔，或改为基于事件而非时间来响应。

有些智能体工作是周期性的：任务本身不变，只有输入在变。例如每天早上总结 Slack 消息。另一些工作则依赖外部系统，与其对接的一个简单办法就是按间隔检查它，并对变化作出响应。例如一个可能收到代码评审或 CI 失败的 PR。

针对这些情况，你可以在 Claude 运行时用 `/loop` 来触发，它按固定间隔重复运行一条提示。例如：

```
/loop 5m check my PR, address review comments, and fix failing CI
```

`/loop` 在你的电脑上运行，所以一旦你关机，它就停了。你可以用 `/schedule` 创建一个例行任务（routine），把循环搬到云端。

## **主动式循环（Proactive loops）**

- **触发方式**：事件或定时计划，无需人实时在场。
- **停止条件**：每个任务在目标达成后退出。例行任务本身持续运行，直到你把它关掉。
- **最适合**：源源不断、定义清晰的工作：bug 报告、issue 分诊、迁移、依赖升级等。
- **用量管理方式**：把例行任务路由到更小、更快的模型，把判断性决策留给最强的模型。

上述原语，加上 **auto mode** 和**动态工作流（dynamic workflows）**（研究预览）等其他 Claude Code 功能，可以组合成一个面向长时间运行工作的循环。

例如，要处理源源不断的反馈，你可以使用：

1. **`/schedule`**（研究预览）运行一个例行任务，检查新的报告
2. **`/goal`** 定义"完成"是什么样子，并用 **skills** 记录如何验证
3. **动态工作流**编排智能体，对每份报告进行分诊、修复并评审修复
4. **Auto mode** 让例行任务无需停下来请求权限即可运行

组合起来，一条提示可以是这样的：

```
/schedule every hour: check #project-feedback for bug reports. /goal: don't stop until every report found this run is triaged, actioned, and responded to. When fixing a bug, use a workflow to explore three solutions in parallel worktrees and have a judge adversarially review them.
```

## **保持代码质量**

循环产出的质量取决于它周围的系统。设计这个系统时：

- **保持代码库本身干净**：Claude 会遵循你代码库中已有的模式与约定。
- **给 Claude 提供验证自己工作的手段**：用 [skills](https://code.claude.com/docs/en/skills) 把"好"对你和你的团队意味着什么编码下来。
- **让文档易于获取**：框架和库的文档里有最新的最佳实践。
- **用第二个智能体做代码评审**：拥有全新上下文的评审者偏见更少，不会受主智能体推理的影响。你可以使用内置的 `/code-review` 技能，或面向 GitHub 的 [Code Review](https://code.claude.com/docs/en/code-review)。写代码的循环需要检查代码的循环——参见 [Anthropic 如何保障 AI 原生的 SDLC](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle)。

当某一次结果不达标时，不要止步于修复单个问题，而要尝试把它编码进系统，让之后所有轮次都受益。

## **管理 token 用量**

要管理 token 用量，循环应当有清晰的边界：

- **为任务选择合适的原语和模型**：小任务不需要多个智能体或循环。有些任务可以用更便宜、更快的模型。
- **定义清晰的成功与停止标准**：明确说明"完成"是什么样子，让 Claude 更快（但不过早）得出解决方案。
- **大规模运行前先试点**：动态工作流可能生成数百个智能体。先在一小部分工作上估一估用量。
- **确定性工作用脚本完成**：运行脚本比让模型逐步推理更便宜。例如，一个 PDF 技能可以附带一个表单填写脚本，让 Claude 每次直接运行，而不必重新推导代码。
- **不要超出需要的频率运行例行任务**：让间隔与你所关注对象的变化频率相匹配
- **审查用量**：`/usage` 命令按 skills、subagents 和 MCP 拆解近期用量；不带参数的 `/goal` 会显示当前回合数与 token 用量；`/workflows` 显示每个智能体的 token 用量，并且你随时可以停止某个智能体。

你的[模型与努力等级（effort level）](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)选择，是影响循环成本的最大杠杆之一。

## **开始使用**

总结如下：

| Loop（循环） | 你交出去的是 | 何时使用 | 用什么 |
|---|---|---|---|
| 回合式 | 检查环节 | 你在探索或决策时 | 自定义验证技能 |
| 目标式 | 停止条件 | 你清楚"完成"是什么样子 | `/goal` |
| 时间式 | 触发时机 | 工作按计划发生在你项目之外 | `/loop`、`/schedule` |
| 主动式 | 提示本身 | 工作是周期性且定义清晰的 | 以上全部，外加动态工作流 |

要开始使用 loops，请审视你已经在做的工作。挑一件你是瓶颈的任务，问自己哪一部分可以交出去：你能写出验证检查吗？目标是否足够清晰？工作是否按固定节奏到来？

有了想法之后，就把循环跑起来，观察结果——它在哪里卡住、在哪里越界——并且不要害怕对它进行迭代。

更多信息请阅读 Claude Code 文档中关于[并行运行智能体](https://code.claude.com/docs/en/agents)的内容，以及 [loop](https://code.claude.com/docs/en/goal)、[schedule](https://code.claude.com/docs/en/routines)、[goal](https://code.claude.com/docs/en/goal) 和[动态工作流](https://code.claude.com/docs/en/workflows#orchestrate-subagents-at-scale-with-dynamic-workflows)页面。要让你的检查在不同会话间可复用，请参阅[用 Skills 在 Claude Code 中构建验证回路](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)。

*本文由 Delba de Oliveira 和 Michael Segner 撰写*

FAQ（常见问题）

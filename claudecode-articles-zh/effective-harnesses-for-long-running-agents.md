---
title: "面向长时运行智能体的高效执行框架"
title_en: "Effective harnesses for long-running agents"
source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
published: 2025-11-26
crawled: 2026-09-11
translated: 2026-09-11
---

# 面向长时运行智能体的高效执行框架

> 原文：[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · Anthropic Engineering Blog

随着 AI 智能体能力增强，开发者越来越多地让它们承担需要连续工作数小时甚至数天的复杂任务。然而，让智能体跨多个上下文窗口保持稳定进展，仍是一个未解问题。

长时运行智能体的核心挑战在于：它们必须以离散的会话工作，而每个新会话开始时对之前发生的一切毫无记忆。想象一个由轮班工程师组成的软件项目——每位新工程师上岗时对上一班发生的事情一无所知。由于上下文窗口有限，且大多数复杂项目无法在单个窗口内完成，智能体需要一种在编码会话之间架桥的方法。

我们开发了一个双重方案，让 [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 能跨许多上下文窗口高效工作：一个在首次运行时搭建环境的**初始化智能体**，以及一个**编码智能体**——它的任务是在每个会话中取得增量进展，同时为下一个会话留下清晰的产物。代码示例见配套的 [quickstart。](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)

## 长时运行智能体问题

Claude Agent SDK 是一个强大的通用智能体执行框架（harness），精通编码以及其他需要模型使用工具收集上下文、规划并执行的任务。它具备上下文管理能力，例如压缩（compaction），让智能体无需耗尽上下文窗口就能持续处理任务。理论上，在这种配置下，智能体应当可以在任意长的时间内持续做有用的工作。

然而，光靠压缩并不够。开箱即用的情况下，即使是 Opus 4.5 这样的前沿编码模型，以 Claude Agent SDK 在多个上下文窗口上循环运行，如果只给它一个高层提示——比如「做一个 [claude.ai](http://claude.ai/redirect/website.v1.cca96f39-8fde-483c-b6f9-cf40c0acc3e1) 的克隆」——也难以构建出生产质量的 web 应用。

Claude 的失败呈现两种模式。第一，智能体倾向于一次做太多——本质上想一口气 one-shot 整个应用。这常常导致模型在实现中途耗尽上下文，让下一个会话面对一个实现了一半、又没有任何文档的功能。智能体只能猜测发生过什么，再花大量时间让基础应用重新跑起来。即使有压缩也会发生这种情况——压缩并不总能给下一个智能体传递完美清晰的指示。

第二种失败模式通常出现在项目后期。在一些功能已经建成之后，后续的智能体实例环顾四周，看到进展已现，就宣布大功告成。

由此，问题可以分解为两部分。第一，我们需要搭建一个初始环境，为给定提示所要求的*全部*功能打好地基，让智能体得以逐步、逐功能地推进。第二，我们应当提示每个智能体朝目标取得增量进展，同时在会话结束时把环境留在干净状态。所谓「干净状态」，指的是适合合并进主分支的代码：没有重大 bug，代码井然有序、文档完善，总之开发者可以轻松开始一个新功能，而不必先收拾一个不相干的烂摊子。

在内部实验中，我们用两部分的方案解决了这些问题：

1. 初始化智能体：第一个智能体会话使用专门的提示，要求模型搭建初始环境：一个 `init.sh` 脚本、一个记录智能体所作所为日志的 claude-progress.txt 文件，以及一个显示添加了哪些文件的初始 git 提交。
2. 编码智能体：之后每个会话都要求模型取得增量进展，然后留下结构化的更新记录。1

这里的关键洞见是找到一种办法，让智能体在带着全新上下文窗口启动时能快速理解工作状态——这靠 claude-progress.txt 文件配合 git 历史实现。这些实践的灵感来自对高效软件工程师日常做法的了解。

## 环境管理

在更新版 [Claude 4 提示指南](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices#multi-context-window-workflows)中，我们分享了多上下文窗口工作流的一些最佳实践，包括「为第一个上下文窗口使用不同提示」的 harness 结构。这个「不同的提示」要求初始化智能体搭建环境，配置好未来编码智能体高效工作所需的全部上下文。这里我们深入剖析这种环境的几个关键组件。

### 功能清单

为了解决智能体一口气 one-shot 整个应用、或过早宣布项目完成的问题，我们提示初始化智能体编写一份全面的功能需求文件，把用户的初始提示展开。在 [claude.ai](http://claude.ai/redirect/website.v1.cca96f39-8fde-483c-b6f9-cf40c0acc3e1) 克隆的例子里，这意味着超过 200 个功能，比如「用户可以打开新会话、输入查询、按回车、看到 AI 回复」。这些功能最初全部标记为「failing」（未通过），让后续的编码智能体对完整功能的样貌有清晰的轮廓。

```
{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
  }
```

我们提示编码智能体只能通过修改 passes 字段的状态来编辑这个文件，并且使用措辞强硬的指令：「删除或编辑测试是不可接受的，因为这可能导致功能缺失或有 bug。」经过一些实验，我们决定使用 JSON——与 Markdown 文件相比，模型更不容易不当修改或覆盖 JSON 文件。

### 增量进展

有了初始环境脚手架，下一版编码智能体被要求一次只做一个功能。这种增量方式对纠正智能体「一次做太多」的倾向至关重要。

增量工作之后，同样关键的是模型在做出代码改动后把环境留在干净状态。在实验中，我们发现引出这一行为的最佳方式，是要求模型用描述性的提交信息把进展提交到 git，并在进度文件中写进展摘要。这让模型可以用 git 回滚糟糕的代码改动、恢复代码库的正常状态。

这些做法还提升了效率，因为智能体不再需要猜测发生过什么、把时间浪费在让基础应用重新跑起来上。

### 测试

我们观察到的最后一个主要失败模式，是 Claude 倾向于不做充分测试就把功能标记为完成。没有显式提示时，Claude 往往改完代码、甚至用单元测试或对开发服务器跑 `curl` 命令做了些测试，但意识不到功能端到端并不工作。

在构建 web 应用的场景中，一旦明确提示 Claude 使用浏览器自动化工具、像人类用户那样做全部测试，它在端到端验证功能上大多表现良好。

![ Screenshots taken by Claude through the Puppeteer MCP server as it tested the claude.ai clone. ](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Ff94c2257964fb2d623f1e81f874977ebfc0986bc-1920x1080.gif&w=3840&q=75)

Claude 通过 Puppeteer MCP 服务器测试 claude.ai 克隆时的截图。

给 Claude 提供这类测试工具极大提升了表现，因为智能体能够发现并修复仅凭代码看不出来 bug。

仍有一些问题存在，例如 Claude 的视觉能力和浏览器自动化工具的局限，使其难以识别每一类 bug。比如，Claude 无法通过 Puppeteer MCP 看到浏览器原生的 alert 弹窗，依赖这些弹窗的功能因此更容易出 bug。

## 快速进入状态

以上全部就位后，每个编码智能体都被提示执行一系列步骤来进入状态，有些步骤相当基础但依然有用：

1. *运行 `pwd` 查看你所在的目录。你只能编辑这个目录下的文件。*
2. *阅读 git 日志和进度文件，了解最近做了什么。*
3. *阅读功能清单文件，选择优先级最高且尚未完成的功能来做。*

这种做法在每个会话中都为 Claude 省下一些 token，因为它不必自己琢磨如何测试代码。让初始化智能体写一个能启动开发服务器的 init.sh 脚本，并在实现新功能之前先跑一遍基础端到端测试，也很有帮助。

在 claude.ai 克隆的例子里，这意味着智能体总是先启动本地开发服务器，并用 Puppeteer MCP 开始一个新会话、发送一条消息、收到一个回复。这确保 Claude 能快速判断应用是否被留在了损坏状态，并立即修复任何既有 bug。如果智能体直接开始实现新功能，多半会让问题更糟。

综上，一个典型的会话以如下助手消息开场：

```
[Assistant] I'll start by getting my bearings and understanding the current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart the servers.
<Starts the development server>
[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.
<Tests basic functionality>
[Assistant] Based on my verification testing, I can see that the fundamental functionality is working well. The core chat features, theme switching, conversation loading, and error handling are all functioning correctly. Now let me review the tests.json file more comprehensively to understand what needs to be implemented next.
<Starts work on a new feature>
```

智能体失败模式与解决方案

| **问题** | **初始化智能体的行为** | **编码智能体的行为** |
| --- | --- | --- |
| Claude 过早宣布整个项目胜利。 | 搭建功能清单文件：根据输入规格，建立含端到端功能描述列表的结构化 JSON 文件。 | 会话开始时阅读功能清单文件。选择单个功能开始做。 |
| Claude 留下的环境有 bug 或没有进展记录。 | 写入初始 git 仓库和进度笔记文件。 | 以阅读进度笔记和 git 提交日志开始会话，并在开发服务器上跑基础测试以捕捉未记录的 bug。以一次 git 提交和进度更新结束会话。 |
| Claude 过早把功能标记为完成。 | 搭建功能清单文件。 | 自我验证所有功能。只有经过仔细测试后才把功能标记为「passing」。 |
| Claude 得花时间琢磨怎么运行应用。 | 写一个能启动开发服务器的 `init.sh` 脚本。 | 以阅读 `init.sh` 开始会话。 |

总结长时运行 AI 智能体中的四种常见失败模式及解决方案。

## 后续工作

本研究展示了长时运行智能体执行框架中一套可行的方案，让模型跨多个上下文窗口取得增量进展。但仍存在开放问题。

最值得注意的是：单个通用编码智能体跨上下文表现最佳，还是多智能体架构能带来更好表现，目前仍不清楚。像测试智能体、质量保证智能体或代码清理智能体这样的专门智能体，或许能在软件开发生命周期的子任务上做得更好。

此外，本 demo 针对全栈 web 应用开发做了优化。一个未来方向是把这些发现推广到其他领域。其中的部分或全部经验，很可能可以应用于科研、金融建模等场景所需的长时运行智能体任务。

### 致谢

作者：Justin Young。特别感谢 David Hershey、Prithvi Rajasakeran、Jeremy Hadfield、Naia Bouscal、Michael Tingley、Jesse Mu、Jake Eaton、Marius Buleandara、Maggie Vo、Pedram Navid、Nadine Yasser 和 Alex Notov 的贡献。

这项工作凝聚了 Anthropic 多个团队的集体努力，是他们让 Claude 得以安全地进行长周期自主软件工程——尤其是 code RL 与 Claude Code 团队。欢迎有兴趣贡献的候选人到 [anthropic.com/careers](http://anthropic.com/careers) 投递申请。

### 脚注

1. 我们在这里称它们为不同的智能体，仅仅因为它们的初始用户提示不同。除此之外，系统提示、工具集和整体智能体执行框架完全相同。

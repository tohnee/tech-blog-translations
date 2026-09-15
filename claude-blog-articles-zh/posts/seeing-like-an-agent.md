---
title: "像智能体一样看世界：我们在 Claude Code 中如何设计工具"
title_en: "Seeing like an agent: how we design tools in Claude Code"
source: https://claude.com/blog/seeing-like-an-agent/
crawled: 2026-09-14
translated: 2026-09-14
---

# 像智能体一样看世界：我们在 Claude Code 中如何设计工具

> 原文：[Seeing like an agent: how we design tools in Claude Code](https://claude.com/blog/seeing-like-an-agent/) · Claude 博客

构建智能体执行框架（harness）最难的部分之一，就是打造它的工具。

Claude 完全通过[工具调用（tool calling）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)来行动，而在 Claude API 中，可以用 [bash](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool)、[skills](https://code.claude.com/docs/en/skills) 和[代码执行](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)等原语以多种方式构建工具。（关于 Claude API 上的程序化工具调用，你可以阅读 [@RLanceMartin 的新文章](https://x.com/RLanceMartin/status/2027450018513490419)。）

那么，你该如何设计智能体的工具？是给它一个 bash 或代码执行这样的通用工具？还是五十个专用工具，每个用例一个？

不妨设身处地站在模型的视角：想象你拿到一道很难的数学题。你会希望有什么工具来解它？这取决于你自身的技能水平！

纸笔是最低配置，但你会受限于手工计算。计算器更好，但你得知道如何使用那些更高级的功能。最快最强大的选择是计算机，但你必须懂得如何用它编写和执行代码。

这是设计智能体的一个实用框架：你要给它与其自身能力相匹配的工具。但你怎么知道它有哪些能力？留心观察、阅读它的输出、反复实验。你要学会像智能体一样看世界。

如果你在构建智能体，就会遇到与我们相同的问题：何时增加一个工具，何时移除一个，以及如何区分这两种时机。下面是我们在构建 Claude Code 过程中给出的答案，也包括我们最初搞错的地方。

## 用 AskUserQuestion 工具改进引导式提问

在构建 AskUserQuestion 工具时，我们的目标是提升 Claude 提问的能力（通常称为引导式提问，elicitation）。

虽然 Claude 可以直接用纯文本提问，但我们发现回答这些问题似乎要花掉不必要的时间。如何降低这种摩擦、提高用户与 Claude 之间的沟通带宽？

### 第一次尝试：改造 ExitPlanTool

我们尝试的第一种方法，是给 ExitPlanTool 增加一个参数，让它在提交计划的同时附带一组问题。这是最容易实现的方案，但它会让 Claude 混乱，因为我们同时在要求一份计划和一组针对计划的问题。如果用户的回答与计划内容冲突怎么办？Claude 需要调用两次 ExitPlanTool 吗？我们知道这个策略行不通，于是推倒重来。（关于我们为什么要做 ExitPlanTool，可以阅读[我们关于提示缓存（prompt caching）的帖子](https://x.com/trq212/status/2024574133011673516)。）

### 第二次尝试：改变输出格式

接下来，我们尝试更新 Claude 的输出指令，让它按一种稍加修改的 markdown 格式提问。例如，我们可以要求它输出一组项目符号式的问题，选项放在方括号里。然后我们把这些问题解析并渲染成 UI 呈现给用户。

Claude 通常能产出这种格式，但并不可靠。它会附加多余的句子、漏掉选项，或者干脆放弃整个结构。于是转向下一种方案。

### 第三次尝试：AskUserQuestion 工具

最后，我们决定创建一个 Claude 可以随时调用的工具，并且在计划模式（plan mode）下会特别提示它调用。工具触发时，我们会弹出一个模态框显示问题，并阻塞智能体循环，直到用户作答。

这个工具让我们得以要求 Claude 输出结构化内容，也帮助我们确保 Claude 给用户提供多个选项。它还让用户可以组合使用这一功能，例如在 [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 中调用它，或在 skills 中引用它。

最重要的是，Claude 似乎很喜欢调用这个工具，我们发现它的输出效果很好。毕竟，设计再精良的工具，如果 Claude 不理解如何调用，也无法发挥作用。

这就是 Claude Code 中引导式提问的最终形态吗？我们对此表示怀疑。随着 Claude 能力越来越强，服务它的工具也必须跟着演进。下一节展示的正是这样一个案例：一个曾经有益的工具开始碍事了。

### 随能力升级而更新：tasks 与 todos

Claude Code 最初发布时，我们意识到模型需要一个[待办清单（todo list）](https://platform.claude.com/docs/en/agent-sdk/todo-tracking)来保持正轨。待办可以在开始时写下，随模型推进逐项勾选。为此我们给 Claude 提供了 TodoWrite 工具，用于写入或更新待办并向用户展示。

但即便如此，我们仍常看到 Claude 忘记自己该做什么。作为应对，我们每 5 轮插入一条系统提醒，让 Claude 想起自己的目标。

随着模型进步，它们开始觉得待办清单是一种束缚。反复收到待办清单提醒，会让 Claude 认为自己必须死守清单，而不是在意识到需要改变方向时去修改清单。我们还看到 Opus 4.5 在使用子智能体（subagent）方面也进步很大，但子智能体如何在一个共享待办清单上协同呢？

有鉴于此，我们用 [Task 工具](https://x.com/trq212/status/2014480496013803643)取代了 TodoWrite 功能。待办关注的是让模型不跑偏，而任务（task）帮助智能体之间相互沟通。任务可以包含依赖关系、在多个子智能体之间共享进展，模型也可以修改和删除它们。

随着模型能力增强，你的模型曾经需要的工具现在可能正在束缚它们。持续重审关于需要哪些工具的既有假设非常重要。这也是为什么坚持支持一小套能力画像相当接近的模型会很有用。

## 设计搜索接口

我们构建过的最重要的工具，是那些让 Claude 自己找到上下文的工具。

Claude Code 最初在内部发布时，我们用的是 RAG（检索增强生成）：由向量数据库预先为代码库建立索引，执行框架在每次响应前检索相关代码片段并递给 Claude。RAG 虽然强大且快速，但需要建索引和配置，而且在各种不同环境下可能很脆弱。最重要的是，上下文是*递到* Claude 手里的，而不是它自己找来的。

但既然 Claude 能搜索网络，为什么不能搜索你的代码库？给 Claude 一个 Grep 工具，我们就可以让它自己搜索文件、自己构建上下文。

随着 Claude 越来越聪明，只要给对工具，它构建自身上下文的能力就越来越强。

当我们推出 [Agent Skills](https://agentskills.io/home) 时，我们将渐进式披露（progressive disclosure）的理念正式化：让智能体通过探索逐步发现相关上下文。

Claude 现在可以读取 skill 文件，而这些文件又可以引用其他文件，供模型递归读取。实际上，skills 的一个常见用途就是为 Claude 增加更多搜索能力，比如告诉它如何调用某个 API 或查询数据库。

一年之间，Claude 从基本无法自己构建上下文，进化到能够跨数层文件做嵌套搜索，找到它所需的精确上下文。

渐进式披露如今是我们不新增工具就能添加新功能的常用手法。下一节我们解释原因。

## 渐进式披露：Claude Code Guide 智能体

Claude Code 目前有约 20 个工具，我们的团队会经常回顾：为了让 Claude 发挥最大效力，是否每个都需要。新增工具的门槛很高，因为那意味着模型又多了一个需要考虑的选项。

例如，我们注意到 Claude 对如何使用 Claude Code 了解得不够。如果你问它如何添加 MCP、斜杠命令是干什么的，它可能答不上来。

我们本可以把这些信息全部塞进系统提示，但鉴于用户很少问起，那样做只会加剧上下文腐化（context rot），干扰 Claude Code 的本职工作：写代码。

于是我们尝试渐进式披露：给 Claude 一个指向自身文档的链接，需要时它可以加载并搜索。这确实有效，但 Claude 为了找一个用户一句话就能得到的答案，会把大段大段的文档拉进上下文。

于是我们构建了 Claude Code Guide——每当用户问到 Claude Code 本身时，Claude 就会调用的一个子智能体。这个子智能体在自己的上下文里完成文档搜索，按照关于如何搜索、提取什么的详细指示行事，最后只把答案交回来。主智能体的上下文保持干净。

虽然这不是完美方案（当你问 Claude 如何配置它自己时，它仍可能犯迷糊），但我们确实做到了在不新增工具的情况下扩展 Claude 的行动空间。

### 像智能体一样看世界是一门艺术，而非科学

为你的模型设计工具，既是科学，也是艺术。它在很大程度上取决于你使用的模型、智能体的目标，以及它运行所处的环境。

我们最好的建议？勤于实验、细读输出、大胆尝试新事物。最重要的是，努力像智能体一样看世界。

*立即开始使用 [Claude Code](https://claude.com/product/claude-code)。*

***关于作者：**Thariq Shihipar 是 Anthropic 的技术成员（member of technical staff），从事 Claude Code 的开发工作。*

FAQ（常见问题）

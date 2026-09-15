---
title: "面向 Claude 5 代模型的上下文工程新规则"
title_en: "The new rules of context engineering for Claude 5 generation models"
source: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/
crawled: 2026-09-14
translated: 2026-09-14
---

# 面向 Claude 5 代模型的上下文工程新规则

> 原文：[The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/) · Claude 博客

我此前写过如何以最佳方式[提示最新一代 Claude 5 模型](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)，并与它们迭代协作，发现你真正想构建的东西。

但当你向 Claude 发送一条消息时，提示词只是它获得的上下文中很小的一部分。你的大部分上下文由系统提示、Skills、CLAUDE.md 文件、记忆以及其他来源组装而成。我们把这称为[上下文工程（context engineering）](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，它对你使用 Claude Code 或构建自己的智能体时得到的结果有着巨大影响。

与提示词不同，上下文通常在许多请求之间通用，因此不可能那么具体。你如何为 Claude 构建这些通用的提示与指引，尤其是在你不知道用户的提示可能是什么的时候？

随着 Claude 自身能力的演进，这件事可能出奇地困难。最近，我们注意到在提示最新一代 Claude 模型的方式上出现了一次大幅跃迁。对于 Claude Opus 5 与 Claude Fable 5 这类模型，我们删掉了 Claude Code 系统提示中超过 80% 的内容，而我们的编码评估中没有可测量的损失。

以下是我们学到的关于提示这类新模型的经验，以及你如何利用它来更新自己的上下文工程。我们已把这些最佳实践内置到 `claude doctor` 中：在 Claude Code 里使用 /doctor 命令，为你的 skills 与 CLAUDE.md 文件找到合适的尺寸。

## 解开对 Claude 的束缚

总体而言，我们发现自己此前对 Claude Code 的约束过度了——无论是通过系统提示，还是通过 CLAUDE.md 文件和 skills。

例如，当我们阅读自己内部使用 Claude Code 的对话记录时，会在单个请求中看到好几条相互冲突的指令，比如"按需酌情处理文档"或"不要添加注释"——我们的系统提示、skills 与用户请求彼此打架。

通常，Claude 能够解读用户意图并得出正确答案，但它必须更加仔细地思考这些重叠冲突的指令，然后才能决定怎么做。

虽然这些约束曾经是避免最坏情况所必需的，但我们后来发现，可以删掉其中许多，让模型转而利用周围的上下文和判断力。

此外，Claude Code 现在拥有的工具多得多。过去 Claude 依赖 CLAUDE.md 作为记忆、信息与指引的来源。现在我们有了记忆（memory）、artifacts 和 skills，Claude 可以用它们创造出跨会话加载与共享上下文的新方式。

## 昔与今

过去有不少上下文工程最佳实践已经变成了迷思。包括：.

### 过去：给 Claude 立规则

### 现在：让 Claude 运用判断力

我们最初上线 Claude Code 时，必须确保 Claude 避开最坏情况，例如删除文件。这意味着我们会给出一些非常强硬、却未必总是正确的指引。例如，我们过去的系统提示中这样写：

*在代码中：默认不写任何注释。绝不写多段 docstring 或多行注释块——最多一行短句。除非用户要求，否则不要创建规划、决策或分析文档——从对话上下文中工作，而不是依赖中间文件。*

但对某一部分提示词来说，这种指引会是错的。以文档为例，用户可能有自己的偏好，或者非常复杂代码的特定部分可能需要多行注释块。

不过，对旧模型而言，没有这些防护栏，Claude 写的注释在很多情况下就会出错，我们只能接受这个取舍。而新模型拥有更好的判断力，无需显式规则也能把这些决策处理得很好。

在新的系统提示中，我们这样写：*让代码读起来像周围的代码：匹配它的注释密度、命名与惯用写法。*

### 过去：给 Claude 示例

### 现在：设计接口

工具使用的头号规则是给 Claude 提供使用示例。而在最新模型上，我们发现给示例实际上会把它们约束在一个特定的探索空间里。

与其用示例，不如多想想你的工具、脚本和文件的设计——Claude 拥有哪些参数？它们如何能更有表达力？

例如，在 Todo 工具的示例中，仅仅把状态列为 pending、in_progress 与 completed 之间的枚举，就向 Claude 暗示了该如何使用它。关于同一时间只保留一个 in_progress 项的指令，则帮助定义了我们期望的行为。

### 过去：把一切都放在最前面

### 现在：使用渐进式披露

由于 Claude Code 专注编码，我们的系统提示中包含了关于如何做代码评审与验证的详细信息。这些内容并非总是需要，但需要时就是至关重要的信息。

从那以后，Claude Code 已经非常擅长使用渐进式披露（progressive disclosure）——在正确的时机加载正确的上下文。例如，我们把验证与代码评审移进了各自独立的 skills，供 Claude Code 选择性调用。

但渐进式披露不只适用于 skills，我们也把它用在工具上。我们的一些工具是"延迟加载"（deferred loading）的，这意味着智能体必须先通过 ToolSearch 搜索到它们的完整定义才能使用。这让我们得以拥有更多工具（例如我们的 Task 工具），而不让它们在被需要之前占用上下文。

同样的思路也适用于你自己的 CLAUDE.md 与 Skill.md 文件。一个常见的迷思是：要把这些文件做成一个存放所有"可能"会遇到的已知实践的中心仓库，因为否则 Claude 就找不到它们。相反，[可以考虑构建一棵能在正确时机加载的文件树](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)。

### 过去：重复自己

### 现在：简洁的工具描述

较早的 Claude 模型有时需要重复的指令，或者更容易听进上下文窗口末尾而非开头的指令。这意味着我们的系统提示有时会在主系统提示里提及工具，同时在工具描述里又写一遍指令。

我们发现可以删掉这些重复的示例，把如何使用工具的指令放进工具描述里，而不是系统提示里。

### 过去：记忆存在 CLAUDE.md 文件里

### 现在：自动记忆

我们过去鼓励用户把内容存入 Claude 的记忆，方法是使用 # 快捷键自动写入他们的 [CLAUDE.md](http://claude.md)。现在，Claude 会自动保存与工作相关、与你相关的记忆。

### 过去：简单的规格说明

### 现在：丰富的引用

在计划模式中，Claude Code 高度依赖存有计划的 markdown 文件。把这些文件作为计划存放，有助于 Claude 在需要时引用它们。另一个类似的最佳实践是把规格说明存放在代码库中，供 Claude 在跨越较长时间的项目中工作时参考。

但我们发现，Claude 能够处理越来越复杂的引用。Claude 可以引用由我们新推出的 artifacts 功能创建的 HTML 工件，而不只是简单的 markdown 文件。

你也可以用代码的形式给 Claude 提供引用。一份规格说明也可以是一套详尽的测试套件，或者是另一个代码库中 Claude 可能移植过来的某个函数。

评分细则（rubric）是引用的另一种形式。评分细则让 Claude 能够尝试校验你在特定领域的品味（例如：好的 API 设计长什么样），方法是使用[动态工作流（dynamic workflows）](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)，并携带这些评分细则启动验证者智能体。

## 把这些应用到你的上下文中

把以上内容整合起来，组装上下文时究竟该怎么做？

### 系统提示

系统提示与产品上下文深度绑定。它告诉 Claude 自己运行在什么产品中、正在做什么。对于 Claude Code，你几乎永远不会修改它；但如果你在构建自己的智能体执行框架（harness），这正是你应当投入大量时间的地方。

### CLAUDE.md

让 CLAUDE.md 保持轻量，简要描述你的仓库是做什么的，然后把大部分 token 花在代码库内部的那些坑上。例如，你可能会把类型组织在一个单体文件中、其他地方一律不放。避免陈述那些 Claude 看一眼你的文件系统或仓库就该知道的"显而易见"的事。

大量使用渐进式披露：例如，如果你有多条关于如何验证工作的独特指令，就创建一个验证 skill，并在 CLAUDE.md 中引用它。

### Skills

把 skills 想象成轻量级的指南，让 Claude 在需要时找到信息。除非是在极其重要的领域，否则不要把约束定得过死。

对于较长的 skills，尽量多用渐进式披露——把它拆成多个文件并分开存放。

最理想的情况是：skills 编码的是专属于你、你的团队或产品的特定观点、知识或最佳实践。

### 引用

你可以通过 @ 提及文件，把它们作为引用纳入。引用让 Claude 能够参考关于当前计划的深度信息。

它们可能是规格文件、设计稿，甚至整个代码库。一般来说，你应当优先选择以代码形式存在的文件，因为它以 Claude 非常熟悉的一门语言，向它提供了清晰、高保真的指令。例如，一份设计的 HTML 样稿通常比一段对该设计的文字描述或一张截图产出更好的结果。

## 试着做减法

在你的系统提示、skills 和 CLAUDE.md 文件中，你可能需要像我们一样做简化。我们推出了一个名为 `claude doctor` 的新命令，它也能帮你自动完成这件事。想了解针对更先进模型的提示方法的具体细节，请查阅我们的 [Fable 实战指南](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)。

*本文由 Anthropic 技术成员（member of technical staff）Thariq Shihipar 撰写。*

FAQ（常见问题）

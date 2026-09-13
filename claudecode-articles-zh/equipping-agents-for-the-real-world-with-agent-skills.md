---
title: "用 Agent Skills 把智能体武装到现实世界"
title_en: "Equipping agents for the real world with Agent Skills"
source: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
published: 2025-10-16
crawled: 2026-09-11
translated: 2026-09-11
---

# 用 Agent Skills 把智能体武装到现实世界

> 原文：[Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) · Anthropic Engineering Blog

*更新：我们已将* [*Agent Skills*](https://agentskills.io/) *发布为跨平台可移植性的开放标准。（2025 年 12 月 18 日）*

随着模型能力提升，我们现在可以构建与完整计算环境交互的通用智能体。例如 [Claude Code](https://claude.com/product/claude-code) 可以借助本地代码执行和文件系统跨领域完成复杂任务。但随着这些智能体日益强大，我们需要更可组合、更可扩展、更可移植的方式，为它们装备领域专长。

这促使我们创造了 [**Agent Skills**](https://www.anthropic.com/news/skills)：一组组织良好的指令、脚本和资源文件夹，智能体可以发现并动态加载它们，从而在特定任务上表现更好。Skills 把你的专长打包成可组合的资源交付给 Claude，扩展 Claude 的能力，把通用智能体变成贴合你需求的专门智能体。

为智能体构建一个技能，就像为一位新员工编写一份入职指南。你不再需要为每个用例分别构建碎片化、定制化的智能体——任何人都可以通过捕捉和分享自己的程序性知识，用可组合的能力专门化自己的智能体。本文将解释 Skills 是什么、展示它们如何工作，并分享构建你自己的 Skills 的最佳实践。

![To activate skills, all you need to do is write a SKILL.md file with custom guidance for your agent.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fddd7e6e572ad0b6a943cacefe957248455f6d522-1650x929.jpg&w=3840&q=75)

一个技能是一个包含 SKILL.md 文件的目录，其中收纳了赋予智能体额外能力的指令、脚本和资源。

## 技能的解剖

要看 Skills 的实际运作，我们走一遍一个真实的例子：驱动 [Claude 最近上线的文档编辑能力](https://www.anthropic.com/news/create-files)的技能之一。Claude 已经很懂如何理解 PDF，但直接操纵 PDF（比如填写表单）的能力有限。这个 [PDF 技能](https://github.com/anthropics/skills/tree/main/document-skills/pdf)让我们把新能力交给 Claude。

最简单的形式下，技能就是一个包含 `SKILL.md` 文件的目录。该文件必须以 YAML frontmatter 开头，包含一些必需的元数据：`name` 和 `description`。启动时，智能体会把每个已安装技能的 `name` 和 `description` 预载入其系统提示。

这些元数据是渐进式披露（progressive disclosure）的**第一层**：它提供恰好够用的信息，让 Claude 知道每个技能何时该用，而不必把全部内容载入上下文。文件正文则是**第二层**细节。如果 Claude 认为该技能与当前任务相关，就会把完整的 `SKILL.md` 读入上下文，从而加载该技能。

![Anatomy of a SKILL.md file including the relevant metadata: name, description, and context related to the specific actions the skill should take.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F6f22d8913dbc6228e7f11a41e0b3c124d817b6d2-1650x929.jpg&w=3840&q=75)

SKILL.md 文件必须以 YAML Frontmatter 开头，包含文件名和描述，启动时会被载入系统提示。

随着技能复杂度增长，它可能包含多到装不进单个 `SKILL.md` 的上下文，或只在特定场景下相关的上下文。此时技能可以在技能目录内捆绑额外的文件，并在 `SKILL.md` 中按名称引用它们。这些额外的链接文件是**第三层**及更深的细节，Claude 只在需要时才去浏览和发现。

在下面展示的 PDF 技能中，`SKILL.md` 引用了两个额外文件（`reference.md` 和 `forms.md`），它们是技能作者选择与核心 `SKILL.md` 捆绑在一起的。通过把填表指令移到单独的文件（`forms.md`），技能作者得以保持技能核心的精简，并放心地让 Claude 只在填写表单时才去读 `forms.md`。

![How to bundle additional content into a SKILL.md file.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F191bf5dd4b6f8cfe6f1ebafe6243dd1641ed231c-1650x1069.jpg&w=3840&q=75)

你可以通过额外文件把更多上下文并入技能，由 Claude 根据系统提示触发使用。

渐进式披露是让 Agent Skills 灵活且可扩展的核心设计原则。就像一本组织良好的手册——从目录开始，然后是具体章节，最后是详细附录——技能让 Claude 只在需要时加载信息：

![This image depicts how progressive disclosure of context in Skills.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fa3bca2763d7892982a59c28aa4df7993aaae55ae-2292x673.jpg&w=3840&q=75)

拥有文件系统和代码执行工具的智能体，在处理特定任务时无需把整个技能读进上下文窗口。这意味着可以打包进一个技能的上下文数量实际上没有上限。

### 技能与上下文窗口

下图展示了当技能被用户消息触发时，上下文窗口发生的变化。

![This image depicts how skills are triggered in your context window.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F441b9f6cc0d2337913c1f41b05357f16f51f702e-1650x929.jpg&w=3840&q=75)

技能经由系统提示在上下文窗口中被触发。

图中展示的操作顺序：

1. 开始时，上下文窗口中有核心系统提示和每个已安装技能的元数据，以及用户的初始消息；
2. Claude 调用 Bash 工具读取 `pdf/SKILL.md` 的内容，从而触发 PDF 技能；
3. Claude 选择读取技能附带的 `forms.md` 文件；
4. 最后，Claude 已从 PDF 技能加载了相关指令，继续执行用户的任务。

### 技能与代码执行

技能还可以包含供 Claude 酌情作为工具执行的代码。

大语言模型擅长许多任务，但某些操作更适合传统的代码执行。例如，通过 token 生成来给一个列表排序，比直接跑一个排序算法昂贵得多。除了效率考量，许多应用还需要只有代码才能提供的确定性可靠性。

在我们的例子中，PDF 技能包含一个预写好的 Python 脚本，用于读取 PDF 并提取所有表单字段。Claude 可以运行这个脚本，而无需把脚本或 PDF 载入上下文。而且因为代码是确定性的，这个工作流稳定且可重复。

![This image depicts how code is executed via Skills.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fc24b4a2ff77277c430f2c9ef1541101766ae5714-1650x929.jpg&w=3840&q=75)

根据任务的性质，技能还可以包含供 Claude 酌情作为工具执行的代码。

## 开发与评估技能

以下是上手编写和测试技能的一些实用准则：

- **从评估入手：** 让智能体在代表性任务上运行，观察它们在哪里表现吃力或需要额外上下文，从而识别其能力的具体缺口。然后增量构建技能来弥补这些短板。
- **为扩展而设计：** 当 `SKILL.md` 文件变得臃肿时，把内容拆分到单独的文件并加以引用。如果某些上下文互斥或很少一起使用，让路径保持分离可以减少 token 用量。最后，代码既可以作为可执行工具，也可以充当文档。应当写清楚 Claude 应该直接运行脚本，还是把它们读入上下文作参考。
- **从 Claude 的视角思考：** 监控 Claude 在真实场景中如何使用你的技能，并基于观察迭代：留意意外的执行轨迹或对某些上下文的过度依赖。特别关注技能的 `name` 和 `description`。Claude 会依据它们决定是否针对当前任务触发该技能。
- **与 Claude 一起迭代：** 在与 Claude 协作任务时，让 Claude 把它成功的方法和常犯的错误捕捉为技能中可复用的上下文和代码。如果它在用某技能完成任务时跑偏了，让它自我反思哪里出了问题。这个过程会帮你发现 Claude 实际需要什么上下文，而不是试图提前臆测。

### 使用技能时的安全考量

技能通过指令和代码赋予 Claude 新能力。这让它们强大，但也意味着恶意技能可能在使用它的环境中引入漏洞，或指使 Claude 外泄数据、执行非预期动作。

我们建议只从可信来源安装技能。从可信度较低的来源安装技能时，务必先彻底审计再使用：先阅读技能捆绑文件的内容，了解它做什么，特别注意代码依赖以及图片、脚本等捆绑资源。同样，留意技能中指示 Claude 连接潜在不可信外部网络源的指令或代码。

## Skills 的未来

Agent Skills 目前已在 [Claude.ai](http://claude.ai/redirect/website.v1.a2696359-c7d7-460f-837c-1fb39bfea245)、Claude Code、Claude Agent SDK 和 Claude 开发者平台上[得到支持](https://www.anthropic.com/news/skills)。

未来几周，我们将继续添加支持创建、编辑、发现、共享和使用 Skills 全生命周期的功能。我们对 Skills 帮助组织和个人与 Claude 分享他们的上下文与工作流的机会尤为期待。我们还将探索 Skills 如何与[模型上下文协议](https://modelcontextprotocol.io/)（MCP）服务器互补，教会智能体涉及外部工具和软件的更复杂工作流。

展望更远的将来，我们希望让智能体能够自行创建、编辑和评估 Skills，让它们把自己的行为模式固化为可复用的能力。

Skills 是一个概念简单的想法，格式也相应地简单。这种简单性让组织、开发者和最终用户更容易构建定制化的智能体并赋予它们新能力。

我们期待看到人们用 Skills 构建的东西。立即开始：查看我们的 Skills [文档](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)与 [cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)。

## 致谢

作者：Barry Zhang、Keith Lazuka 和 Mahesh Murag——三个真的很喜欢文件夹的人。特别感谢 Anthropic 内外许多倡导、支持和构建 Skills 的同事。

---
title: "Skills 详解：Skills 与提示、Projects、MCP 和子智能体的对比"
title_en: "Skills explained: How Skills compares to prompts, Projects, MCP, and subagents"
source: https://claude.com/blog/skills-explained/
crawled: 2026-09-14
translated: 2026-09-14
---

# Skills 详解：Skills 与提示、Projects、MCP 和子智能体的对比

> 原文：[Skills explained: How Skills compares to prompts, Projects, MCP, and subagents](https://claude.com/blog/skills-explained/) · Claude 博客

自从推出 [Skills](https://www.anthropic.com/news/skills) 以来，很多人想了解 Claude 智能体生态的各个组件如何协同工作。

无论你是在 [Claude Code](https://www.claude.com/product/claude-code) 中构建复杂工作流、用 API 打造企业级解决方案，还是在 [Claude.ai](http://claude.ai) 上最大化自己的生产力，弄清该在何时选用哪个工具，都能改变你与 Claude 协作的方式。

本指南逐一拆解每个构建模块，说明何时该用什么，并展示如何把它们组合成强大的智能体工作流。

## **理解你的智能体构建模块**

### **什么是 Skills？**

Skills 是包含指令、脚本和资源的文件夹，当与任务相关时，Claude 会动态发现并加载它们。可以把它们想象成专门领域的培训手册，赋予 Claude 特定领域的专业能力——从操作 Excel 电子表格到遵循你组织的品牌规范。

**Skills 的工作方式：**当 Claude 遇到任务时，它会扫描可用的 Skills 以寻找相关匹配。Skills 采用渐进式披露（progressive disclosure）：先加载元数据（约 100 个 token），恰好足够 Claude 判断某个 Skill 何时相关；完整指令在需要时加载（不超过 5k token），捆绑的文件或脚本则只在需要时加载。

**何时使用 Skills：**当你需要 Claude 一致且高效地执行专门任务时，选择 Skills。它们尤其适合：

- **组织工作流**：品牌规范、合规流程、文档模板
- **领域专业知识：**Excel 公式、PDF 处理、数据分析
- **个人偏好：**笔记系统、编码模式、研究方法

**示例：**创建一个[品牌规范 Skill](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines)，收录你公司的配色方案、字体规则和版式规格。当 Claude 创建演示文稿或文档时，会自动应用这些标准，无需你每次解释。

[了解更多](https://support.claude.com/en/articles/12512176-what-are-skills)关于 Skills 的信息，并查看[我们不断扩充的 Skills 库](https://github.com/anthropics/skills)。

### **什么是提示（prompts）？**

[提示（prompts）](https://docs.claude.com/en/prompt-library/library)是你在对话中用自然语言提供给 Claude 的指令。它们是短暂的、对话式的、被动的——你在当下提供上下文和方向。

**何时使用提示：**提示适用于：

- 一次性请求："总结这篇文章"
- 对话式微调："把语气改得更专业一些"
- 即时上下文："分析这些数据并找出趋势"
- 临时指令："把这些内容排成项目符号列表"

**示例：**

*请对这段代码进行全面的安全审查。我想检查：*

*1. 常见漏洞，包括：*

- *注入缺陷（SQL、命令、XSS 等）*
- *认证与授权问题*
- *敏感数据泄露*
- *安全配置错误*
- *失效的访问控制*
- *加密机制失效*
- *输入验证问题*
- *错误处理与日志记录问题*

*2. 对于发现的每个问题，请提供：*

- *严重级别（严重/高/中/低）*
- *代码中的位置（行号或函数名）*
- *说明它为何构成安全风险以及可能如何被利用*
- *具体的修复建议，尽量附代码示例*
- *防止类似问题的最佳实践指导*

*3. 代码上下文：［描述代码的功能、所用语言/框架以及运行环境——例如"这是一个处理用户认证并处理支付数据的 Node.js REST API"］*

*4. 其他考虑事项：*

- *是否存在 OWASP Top 10 漏洞？*
- *代码是否遵循［具体框架/语言］的安全最佳实践？*
- *是否存在带有已知漏洞的依赖？*

*请按严重程度和潜在影响对发现的问题排定优先级。*

**小贴士：**提示是你与 Claude 互动的主要方式，但它们不会跨对话持久保留。对于重复性工作流或专门知识，可以考虑把提示沉淀为 Skills 或项目指令。

**何时改用 Skill：**当你发现自己在多个对话中反复输入同一段提示时，就该创建 Skill 了。把那些反复出现的指令——比如"使用 OWASP 标准审查这段代码的安全漏洞"或"按执行摘要、主要发现和建议的结构编排这份分析"——转化为 Skills。这能让你免去每次重复解释流程，并确保执行的一致性。

欢迎查看我们的[提示词库](https://docs.claude.com/en/prompt-library/library)、[提示最佳实践](http://claude.com/blog/prompt-engineering-best-practices)或[智能提示生成器](https://claude.ai/public/artifacts/3796db7e-4ef1-4cab-b70c-d045778f23ec)，即刻上手。

### **什么是 Projects？**

[Projects](https://support.claude.com/en/articles/9517075-what-are-projects) 是独立完整的工作区，拥有各自的聊天记录和知识库，面向所有 Claude 付费计划开放。每个项目都有一个 200K 上下文窗口，你可以在其中上传文档、提供上下文，并设置适用于该项目内所有对话的自定义指令。

**Projects 的工作方式：**你上传到项目知识库的所有内容，都会在该项目的所有聊天中可用。Claude 会自动利用这些上下文，给出更有依据、更相关的回答。当项目知识接近上下文上限时，Claude 会无缝启用检索增强生成（RAG）模式，将容量扩展至最多 10 倍。

**何时使用 Projects：**当你需要以下能力时，选择 Projects：

- **持久上下文：**应当影响每一次对话的背景知识
- **工作区组织：**为不同事务划分独立上下文
- **团队协作：**共享的知识和对话历史（Team 和 Enterprise 计划）
- **自定义指令：**项目专属的语气、视角或方法

**示例：**创建一个"Q4 产品发布"项目，放入市场调研、竞品分析和产品规格。该项目中的每次聊天都能使用这些知识，无需你重新上传或重新解释上下文。

**何时改用 Skill：**Projects 为某项具体工作——你公司的代码库、一个研究项目、一个进行中的客户合作——为 Claude 提供持久上下文；Skills 则教会 Claude 如何做某件事。一个 Project 可能包含产品发布的全部背景资料，而一个 skill 可以教 Claude 你们团队的写作规范或代码审查流程。当你发现自己在多个 Projects 之间复制同样的指令时，那就是该创建 skill 的信号。

[了解更多](https://support.claude.com/en/articles/9517075-what-are-projects)关于 Projects 的信息。

### **什么是子智能体（subagents）？**

[子智能体（subagents）](https://docs.claude.com/en/docs/claude-code/sub-agents)是拥有自己上下文窗口、自定义系统提示和特定工具权限的专门 AI 助手。子智能体在 Claude Code 和 Claude Agent SDK 中可用，它们独立处理分立任务，并把结果返回给主智能体。

**子智能体的工作方式：**每个子智能体都按自己的配置运行——你可以定义它做什么、如何处理问题、可以访问哪些工具。Claude 会根据描述自动把任务委派给合适的子智能体，你也可以显式指定某个子智能体。

**何时使用子智能体：**子智能体适用于：

- **任务专门化：**代码审查、测试生成、安全审计
- **上下文管理：**把专门工作外包出去，保持主对话聚焦
- **并行处理：**多个子智能体可以同时处理不同方面
- **工具限制：**把特定子智能体限制在安全操作上（如只读访问）

```
Create a code-reviewer subagent with access to Read, Grep, and Glob tools but not Write or Edit. When you modify code, Claude automatically delegates to this subagent for quality and security review without risking unintended code changes.
```

**何时改用 Skill：**当多个智能体或对话需要同样的专业知识——比如安全审查流程或数据分析方法——创建一个 Skill，而不是把这些知识分别内置到各个子智能体中。Skills 可移植、可复用，而子智能体是为特定工作流量身打造的。用 Skills 教授任何智能体都能应用的专业知识；当你需要带特定工具权限和上下文隔离的独立任务执行时，用子智能体。

[了解更多](https://code.claude.com/docs/en/sub-agents)关于子智能体的信息。

### **什么是 MCP？**

MCP 在 AI 应用与你现有的工具和数据源之间创建了一个通用连接层。

Model Context Protocol（MCP）是一个开放标准，用于把 AI 助手连接到数据所在的外部系统——内容仓库、业务工具、数据库和开发环境。

**MCP 的工作方式：**MCP 提供了一种把 Claude 连接到你的工具和数据源的标准化方式。你无需为每个数据源构建定制集成，只需针对单一协议开发。MCP 服务器暴露数据与能力；MCP 客户端（如 Claude）连接到这些服务器。

**何时使用 MCP：**当你需要 Claude 完成以下事情时，选择 MCP：

- 访问外部数据：Google Drive、Slack、GitHub、数据库
- 使用业务工具：CRM 系统、项目管理平台
- 连接开发环境：本地文件、IDE、版本控制
- 集成自研系统：你专有的工具和数据源

**示例：**通过 MCP 把 Claude 连接到你公司的 Google Drive。现在 Claude 可以搜索文档、读取文件、引用内部知识，无需手动上传——连接持续存在并自动更新。

**何时改用 Skill：**MCP 把 Claude 连接到数据；Skills 教 Claude 如何处理这些数据。如果你在解释*如何*使用某个工具或遵循某套流程——比如"查询我们的数据库时，务必先按日期范围过滤"或"用这些特定公式编排 Excel 报表"——那就是 Skill。如果你首先需要 Claude *访问*数据库或 Excel 文件，那就是 MCP。两者配合使用：MCP 负责连接，Skills 负责流程性知识。

[了解更多](https://www.anthropic.com/news/model-context-protocol)关于 MCP 的信息，并查阅关于如何构建 MCP 服务器的[文档](https://modelcontextprotocol.io/docs/develop/build-server)。

## **它们如何协同工作**

当你把这些构建模块组合起来，真正的威力才会显现。每个模块各司其职，组合在一起则能构建复杂的智能体工作流。

### **对比：选择合适的工具**

| 特性 | Skills | 提示（Prompts） | Projects | 子智能体 | MCP |
|---|---|---|---|---|---|
| **提供什么** | 流程性知识 | 即时指令 | 背景知识 | 任务委派 | 工具连接 |
| **持久性** | 跨对话 | 单次对话 | 项目内 | 跨会话 | 持续连接 |
| **包含内容** | 指令 + 代码 + 资源 | 自然语言 | 文档 + 上下文 | 完整智能体逻辑 | 工具定义 |
| **何时加载** | 按需动态加载 | 每一轮 | 项目内始终在场 | 被调用时 | 始终可用 |
| **能否包含代码** | 是 | 否 | 否 | 是 | 是 |
| **最适合** | 专门领域知识 | 快速请求 | 集中式上下文 | 专门任务 | 数据访问 |

### **智能体工作流示例：研究智能体**

我们来构建一个组合多个构建模块的综合研究智能体。这个示例展示如何为竞争分析组装并激活一个智能体。

**第 1 步：设置你的 Project**

创建一个"竞争情报"项目并上传：

- 行业报告和市场分析
- 竞品产品文档
- 来自 CRM 的客户反馈
- 以往的研究摘要

添加项目指令：

*从我们产品战略的视角分析竞争对手。聚焦差异化机会和新兴市场趋势。以具体证据和可执行的建议呈现研究发现。*

**第 2 步：通过 MCP 连接数据源**

为以下服务启用 MCP 服务器：

- Google Drive（访问共享研究文档）
- GitHub（查看竞品开源仓库）
- 网页搜索（获取实时市场信息）

**第 3 步：创建专门的 Skills**

创建一个 "competitive-analysis" skill：

```
# My Company GDrive Navigation Skill

## Overview
Optimized search and retrieval strategy for Meridian Tech's Google Drive structure. Use this skill to efficiently locate internal documents, research, and strategic materials.

## Drive Organization

**Top-level structure:**
- `/Strategy & Planning/` - OKRs, quarterly plans, board decks
- `/Product/` - PRDs, roadmaps, technical specs
- `/Research/` - Market research, competitive intel, user studies
- `/Sales & Marketing/` - Case studies, pitch decks, campaign materials
- `/Customer Success/` - Implementation guides, success metrics
- `/Company Ops/` - Policies, org charts, team directories

**Naming conventions:**
- Format: `YYYY-MM-DD_DocumentName_vX`
- Final versions marked with `_FINAL`
- Drafts include `_DRAFT` or `_WIP`

## Search Best Practices

1. **Start broad, then filter** - Use folder context + keywords
2. **Target document owners** - Sales materials from Sales/, not root
3. **Check recency** - Prioritize documents from last 6 months for current strategy
4. **Look for "source of truth"** - Files with `_FINAL`, `_APPROVED`, or in `/Archives/Official/`

## Research Agent Workflow

1. Identify topic category (product, market, customer)
2. Search relevant folder with targeted keywords
3. Retrieve 3-5 most recent/relevant documents
4. Cross-reference with `/Strategy & Planning/` for context
5. Cite sources with file names and dates
```

**第 4 步：配置子智能体（仅限 Claude Code/SDK）**

创建专门的子智能体：

`market-researcher` 子智能体：

```
name: market-researcher
description: Research market trends, industry reports, and competitive landscape data. Use proactively for competitive analysis.
tools: Read, Grep, Web-search
---
You are a market research analyst specializing in competitive intelligence.

When researching:
1. Identify authoritative sources (Gartner, Forrester, industry reports)
2. Gather quantitative data (market share, growth rates, funding)
3. Analyze qualitative insights (analyst opinions, customer reviews)
4. Synthesize trends and patterns

Present findings with citations and confidence levels.
```

`technical-analyst` 子智能体：

```
name: technical-analyst
description: Analyze technical architecture, implementation approaches, and engineering decisions. Use for technical competitive analysis.
tools: Read, Bash, Grep
---
You are a technical architect analyzing competitor technology choices.

When analyzing:
1. Review public repositories and technical documentation
2. Assess architecture patterns and technology stack
3. Evaluate scalability and performance approaches
4. Identify technical strengths and limitations

Focus on actionable technical insights that inform our product decisions.
```

**第 5 步：激活你的研究智能体**

现在，当你问 Claude："分析我们前三名竞争对手如何为他们的新 AI 功能定位，并找出我们可以利用的空白"

接下来会发生：

1. **Project 上下文加载**：Claude 访问你上传的研究文档，并遵循项目指令
2. **MCP 连接激活**：Claude 在你的 Google Drive 中搜索近期竞品简报，并拉取 GitHub 数据
3. **Skills 介入**：competitive-analysis Skill 提供分析框架
4. **子智能体执行**（在 Claude Code 中）：market-researcher 收集行业数据，technical-analyst 审查技术实现
5. **提示细化**：你通过对话给出引导："特别关注医疗行业的企业客户"

**结果：**一份综合竞争分析，汇聚多个数据源、遵循你的分析框架、利用专门知识，并在整个研究项目中保持上下文。

## **常见问题**

#### **Skills 是如何工作的？**

Skills 使用[渐进式披露](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)保持 Claude 的高效。处理任务时，Claude 首先扫描 Skill 元数据（描述和摘要）以找出相关匹配。如果某个 Skill 匹配，Claude 就加载完整指令。最后，如果该 Skill 包含可执行代码或参考文件，它们只在需要时加载。

这种架构意味着你可以配置大量 Skills，而不会压垮 Claude 的上下文窗口。Claude 恰好在需要时获取恰好需要的内容。

#### **Skills 与子智能体：何时用哪个**

**使用 Skills 的时机：**你希望任何 Claude 实例都能加载和使用的能力。Skills 就像培训材料——它们让 Claude 在所有对话中都更擅长特定任务。

**使用子智能体的时机：**你需要为特定目的设计、能独立处理工作流的完整独立智能体。子智能体就像拥有自己上下文和工具权限的专门员工。

**两者结合的时机：**你希望子智能体具备专门知识。例如，一个代码审查子智能体可以使用针对特定语言最佳实践的 Skills，把子智能体的独立性与 Skills 的可移植知识结合起来。

#### **Skills 与提示：何时用哪个**

**使用提示的时机：**你在给出一次性指令、提供即时上下文，或进行对话式往复交流。提示是被动的、短暂的。

**使用 Skills 的时机：**你拥有需要反复使用的流程或知识。Skills 是主动的——Claude 知道何时应用它们——并且跨对话持久存在。

**两者结合：**提示与 Skills 天然互补。用 Skills 提供基础知识，再用提示为每个任务提供具体上下文和微调。

#### **Skills 与 Projects：何时用哪个**

**使用 Projects 的时机：**你需要应当影响关于某个具体事项的所有对话的背景知识和上下文。Projects 提供始终加载的静态参考资料。

**使用 Skills 的时机：**你需要只在相关时才激活的流程性知识和可执行代码。Skills 提供按需加载的动态知识，为你的上下文窗口节省空间。

**两者结合的时机：**你既需要持久上下文，也需要专门能力。例如，一个包含产品规格和用户研究的"产品开发"项目，配合用于创建技术文档和分析用户反馈数据的 Skills。

**关键区别：**Projects 说的是"这是你需要了解的"；Skills 说的是"这是做事的方法"。Projects 提供你置身其中的知识库；Skills 提供随处可用的能力——任何对话、任何项目。

#### **子智能体可以使用 Skills 吗？**

可以。在 Claude Code 和 Agent SDK 中，子智能体可以像主智能体一样访问和使用 Skills。这创造了强大的组合：专门的子智能体利用可移植的知识。

例如，你的 python-developer 子智能体可以使用 pandas-analysis Skill 按照团队约定执行数据转换，而 documentation-writer 子智能体使用 technical-writing skill 保持 API 文档格式的一致性。

## **开始使用**

准备好用 Skills 构建了吗？从这里开始：

[**Claude.ai**](https://Claude.ai)**用户：**

- 在 Settings → Features 中启用 Skills
- 在 claude.ai/projects 创建你的第一个项目
- 在下一个分析任务中尝试把项目知识与 Skills 结合使用

**API 开发者：**

- 在[文档](https://docs.anthropic.com)中探索 Skills 端点
- 查看我们的 [skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

**Claude Code 用户：**

- 通过[插件市场（plugin marketplaces）](https://code.claude.com/docs/en/plugin-marketplaces)安装 Skills
- 查看我们的 [skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)

## Agent Skills

立即开始在 Claude 中使用 Skills，构建更强大的应用。

FAQ（常见问题）

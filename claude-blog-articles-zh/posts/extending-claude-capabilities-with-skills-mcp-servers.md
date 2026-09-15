---
title: "用 Skills 与 MCP 扩展 Claude 的能力"
title_en: "Extending Claude's capabilities with skills and MCP"
source: https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 Skills 与 MCP 扩展 Claude 的能力

> 原文：[Extending Claude's capabilities with skills and MCP](https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers/) · Claude 博客

***更新：我们已将 [Agent Skills](https://agentskills.io) 作为开放标准发布，以实现跨平台可移植。（2025 年 12 月 18 日）***

自[发布 Skills](https://claude.com/blog/skills) 以来，我们从客户那里听到的最大的两个问题是："Skills 和 MCP 如何协同工作？什么时候该用这一个，什么时候该用另一个？"

[Model Context Protocol（MCP）](https://modelcontextprotocol.io/docs/getting-started/intro)将 Claude 与第三方工具连接起来，而 Skills 则教会 Claude 如何用好这些工具。把两者结合起来，你就能构建出遵循你团队工作流的智能体，而不是那些需要不断纠正的通用流程。

举个例子，一条连接 Notion 的 MCP 连接能让 Claude 搜索你的工作区。再添加一个用于会议准备的技能，Claude 就知道该从*哪些*页面提取内容、*如何*排版准备文档，以及你们团队交付会议记录的*标准*是什么。这条连接就不再是"仅仅可用"，而是真正有用了。

在本文中，我们将拆解 Skills 与 MCP 之间的关系，说明如何把两者结合起来、构建遵循你的工作流并能产出一致结果的智能体，并通过几个真实案例展示它们在实践中如何协同运作。

## **理解 Skills 与 MCP**

你走进一家五金店，想修好一个坏掉的柜子。店里应有尽有（木工胶、夹钳、替换铰链），但知道该买哪些东西、怎么用，则是另一回事。

MCP 就像让你能走进货架通道随意取用；而 Skills 则像店员的专业知识。如果你不知道自己需要哪些物品、也不知道如何使用，再多的库存也帮不上忙。技能就像那位热心店员，陪你走完整个修理流程，为你指出合适的材料，并示范正确的手法。

说得更具体些：MCP 服务器让 Claude 能够访问你的外部系统、服务和平台，而 Skills 则提供 Claude 有效使用这些连接所需的上下文，教 Claude 在获得这些访问权限之后该做什么。

没有 Skills 提供的上下文，Claude 只能靠猜测来揣摩你的意图。有了技能，Claude 就能照着你的操作手册行事。

## **为什么 Skills 和 MCP 能很好地配合**

MCP 负责连接：对外部系统安全、标准化的访问。无论你连接的是 GitHub、Salesforce、Notion 还是自己内部的 API，MCP 服务器都让 Claude 有能力触达你的工具和数据。

Skills 负责专业知识：正是这些领域知识和工作流逻辑，把原始的工具访问转化为可靠的结果。一个技能知道何时查询你的 CRM、要在结果里找什么、如何排版输出，以及哪些边缘情况需要不同的处理方式。

这种分离让架构保持可组合。一个技能可以编排多个 MCP 服务器，而一个 MCP 服务器也可以支撑几十个不同的技能。新增一条连接，现有技能就能把它纳入进来；打磨一个技能，它就能在你所有已连接的工具上生效。

#### **当你把 Skills 和 MCP 结合起来，你会得到：**

**清晰的发现**：Claude 不必再猜测该去哪里找。一个会议准备技能可能会规定：先查项目页面，再看过往会议记录，然后看利益相关者档案。一个研究技能可能会说：先从共享网盘开始，与 CRM 交叉核对，再用网络搜索填补空白。技能把"哪些任务该用哪些信息源"这种机构知识（institutional knowledge）编码了下来。

**可靠的编排**：多步骤工作流变得可预测。没有技能时，Claude 可能会在确认信息是否齐全之前就把数据拉出来并排好版。技能把执行顺序明确地定义下来，于是 Claude 每次都以同样的方式执行工作流。

**一致的表现**：产出真正达到标准。通用的结果还需要人工修改。技能为你的团队定义了"完成"是什么样子：正确的结构、恰当的详略程度、面向受众的合适语气。

随着时间推移，团队会积累起一批相互关联的技能与连接，让 Claude 具备其特定领域的专业能力。

**延伸阅读**：Tim O'Reilly 谈 [MCP 和 Skills 对开源 AI 意味着什么](https://www.oreilly.com/radar/what-mcp-and-claude-skills-teach-us-about-open-source-for-ai/)

Skills 与 MCP 如何协同工作：MCP 提供工具访问，Skills 提供工作流逻辑。

#### **Skills 与 MCP 可能重叠的地方**

MCP 服务器可能包含一些指令，形式为工具使用提示和面向常见任务的提示词。这让工具相关的知识紧贴工具本身。不过，这些指令在设计上应保持通用。

经验法则是：MCP 的指令涵盖如何正确使用该服务器及其工具；技能的指令则涵盖如何在特定流程或多服务器工作流中使用它们。

例如，一个 Salesforce MCP 服务器可能规定了查询语法和 API 格式；而技能则会规定先检查哪些记录、如何把它们与 Slack 对话交叉核对以获取最新背景，以及如何为你们团队的 pipeline 评审组织输出结构。

在组合 MCP 服务器与技能时，要留意相互冲突的指令。如果你的 MCP 服务器要求返回 JSON，而你的技能要求排版成 markdown 表格，Claude 就得去猜哪个才是对的。让 MCP 负责连接，让技能负责呈现、排序和工作流逻辑。

**延伸阅读：** 了解技能如何利用[渐进式披露（progressive disclosure）](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)按需加载上下文，以及如何利用[程序化工具调用](https://www.anthropic.com/engineering/advanced-tool-use)高效编排 MCP 工具。

## **Skills 与 MCP 结合使用的真实案例**

现在我们来看看 Skills 和 MCP 在真实工作流中如何结合。我们将走完两个例子：金融分析师为公司估值拉取实时市场数据，以及项目经理使用 Notion 的 Meeting Intelligence 技能做会议准备。

在这两个案例中，MCP 服务器提供对工具的访问，而技能则定义拿这些工具做什么。

#### **财务分析：自动化公司估值的技能**

[Anthropic 发布了一套预构建技能](https://www.anthropic.com/news/advancing-claude-for-financial-services)，覆盖常见的金融工作流，其中包括可比公司分析（comparable company analysis）。可比公司分析是一种标准估值方法。做可比公司分析的分析师要花上数小时从多个数据源拉取财务指标、套用同一套估值方法论，并把输出排版成符合合规标准的格式。这类工作重复、易错，也正是最能受益于 Skills 与 MCP 协同的工作流。

**技能（Skill）**：[可比公司分析](https://www.anthropic.com/news/advancing-claude-for-financial-services)将这一估值工作流自动化，从多个数据源拉取数据、套用一致的方法论，并按特定标准排版输出。

**MCP 服务器**：连接 S&P Capital IQ、Daloopa 和 Morningstar，获取实时市场数据

**工作流**：

1. 技能确定要查询哪些数据源（发现，Discovery）
2. MCP 连接拉取实时财务数据
3. 技能套用方法论并排版输出（编排，Orchestration）
4. 技能对照合规要求进行校验（表现，Performance）

#### **会议准备：Notion 的 Meeting Intelligence 技能**

会议准备很繁琐。你需要从多个地方汇集背景信息——项目文档、过往会议记录、利益相关者信息——再把它们综合成一份预读材料和一份议程。这种多步骤流程，你往往每次都得重新解释一遍。

**技能（Skill）**：[Meeting Intelligence](https://notiondevs.notion.site/notion-skills-for-claude) 定义了要搜索哪些页面、如何组织输出结构、应包含哪些章节

**MCP 服务器**：Notion 连接，可搜索、读取并创建页面

1. 技能确定要搜索的相关页面，包括项目、过往会议、利益相关者信息（发现，Discovery）
2. MCP 连接在 Notion 中搜索并取回内容
3. 技能组织出两份文档：内部预读材料和对外议程（编排，Orchestration）
4. MCP 连接把两份文档保存到 Notion，归类并建立链接
5. 技能确保输出符合排版标准（表现，Performance）

## **何时用 Skills，何时用 MCP**

Skills 和 MCP 解决的是不同的问题，但针对某个具体工作流该用哪一个，并不总是显而易见。

#### **什么场景该用 Skills**

技能承载的是那些原本只存在于你脑中的知识，或者是每次有新人加入团队都要重新解释一遍的知识。它们最适合：

- **涉及工具的多步骤工作流**：如会议准备，从多个来源汇集信息，然后创建结构化文档
- **一致性攸关的流程**：如必须每次都遵循同一方法论的季度财务分析、带有强制检查点的合规审查
- **你想要沉淀并分享的领域专业知识**：如研究方法论、代码评审标准、写作规范
- **团队成员离开后仍应延续的工作流**：以可复用指令编码的机构知识

#### **什么场景该用 MCP 服务器**

MCP 扩展了 Claude 能访问和使用的东西。当你需要以下能力时，就用 MCP：

- **实时数据访问**：搜索 Notion 页面、读取 Slack 消息、查询数据库
- **在外部系统中执行动作**：创建 GitHub issue、更新项目管理工具、发送通知
- **文件操作**：读写 Google Drive、访问本地文件系统
- **API 集成**：连接尚无 Claude 原生支持的服务

如果你在解释某件事*怎么做*，那就是技能；如果你需要 Claude *访问*某个东西，那就是 MCP。

#### **速查表：Skills 与 MCP 的区别**

|  | Skills | MCP |
|---|---|---|
| **它是什么** | 程序性知识 | 工具连接能力 |
| **它的作用** | 教 Claude *如何*做某件事 | 让 Claude 能够*访问*某样东西 |
| **何时加载** | 按需加载，需要时才载入 | 一旦连接即始终可用 |
| **包含什么** | 指令、脚本、模板、资源文件 | 工具、资源、提示 |
| **Token 行为** | 按需加载，节省上下文 | 定义预先加载 |
| **最适合** | 工作流、规范、方法论 | 数据访问、API 调用、外部操作 |

## **常见问题**

#### **Skills 会取代 MCP 吗？**

不会。Skills 和 MCP 解决的是不同的问题。MCP 提供通往外部工具和数据的连接；Skills 提供如何有效利用这些连接的程序性知识。最强大的工作流往往两者并用。

#### **一个技能可以使用多个 MCP 服务器吗？**

可以。单个技能可以同时协调多个 MCP 服务器。例如一个技术竞品分析技能，可以在 Google Drive 中搜索内部研究资料、从 GitHub 拉取竞品代码仓库，并通过网络搜索收集市场数据。

#### **我可以为一个 MCP 服务器构建多个技能吗？**

可以。技能能够提升你从单个 MCP 连接中获得的价值。Notion 就演示了这种模式：为会议准备、研究、知识沉淀和规格落地（spec-to-implementation）分别提供了独立的技能——可在[这里](https://claude.com/connectors/notion)查看。

## **开始使用**

准备好用 Skills *和* MCP 来构建了吗？以下是上手方法：

**使用 Skills：**

- 在 [claude.ai](https://claude.ai) 的 Settings → Capabilities 中启用 Skills
- 浏览[技能库](https://github.com/anthropics/skills)，查看预构建示例
- 阅读 [Skills 文档](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)

**使用 MCP：**

- 浏览适用于你所用工具的 [MCP 服务器](https://github.com/modelcontextprotocol/servers)
- 阅读 [MCP 文档](https://modelcontextprotocol.io/introduction)
- 按照 [MCP 快速上手](https://modelcontextprotocol.io/quickstart)构建你自己的服务器

**两者结合：**

- 连接一个 MCP 服务器，然后添加一个使用它的技能

FAQ（常见问题）

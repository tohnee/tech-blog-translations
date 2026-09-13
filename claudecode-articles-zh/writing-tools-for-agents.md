---
title: "为智能体编写高效工具——用智能体来写"
title_en: "Writing effective tools for agents — with agents"
source: https://www.anthropic.com/engineering/writing-tools-for-agents
published: 2025-09-11
crawled: 2026-09-11
translated: 2026-09-11
---

# 为智能体编写高效工具——用智能体来写

> 原文：[Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents) · Anthropic Engineering Blog

[模型上下文协议（Model Context Protocol，MCP）](https://modelcontextprotocol.io/docs/getting-started/intro)可以赋予 LLM 智能体多达数百个工具来解决现实世界的任务。但我们如何让这些工具发挥最大效力？

本文描述我们在各类智能体 AI 系统1中改进表现的最有效技术。

我们先介绍如何：

- 构建并测试工具原型
- 用智能体创建并运行全面的工具评估
- 与 Claude Code 这样的智能体协作，自动提升工具的表现

最后，我们总结一路走来确定的高质量工具编写原则：

- 选择实现（以及不实现）哪些工具
- 用命名空间（namespacing）划分清晰的功能边界
- 让工具把有意义上下文返回给智能体
- 以 token 效率为目标优化工具响应
- 对工具描述和规格做提示工程

![This is an image depicting how an engineer might use Claude Code to evaluate the efficacy of agentic tools.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fcdc027ad2730e4732168bb198fc9363678544f99-1920x1080.png&w=3840&q=75)

构建一个评估，让你能系统性地度量工具的表现。然后可以用 Claude Code 针对这个评估自动优化你的工具。

## 什么是工具？

在计算中，确定性系统在给定相同输入时每次都产生相同输出，而*非确定性*系统——比如智能体——即使起始条件相同也可能生成不同的响应。

传统上写软件时，我们是在确定性系统之间建立契约。例如，`getWeather(“NYC”)` 这样的函数调用，每次被调用都会以完全相同的方式获取纽约市的天气。

工具是一种新型软件，体现的是确定性系统与非确定性智能体之间的契约。当用户问「今天要带伞吗？」，智能体可能调用天气工具、凭借常识回答，甚至先反问一句地点在哪。偶尔，智能体也可能产生幻觉，甚至搞不懂如何使用某个工具。

这意味着为智能体编写软件时，需要从根本上重新思考我们的方法：不能再像为其他开发者或系统写函数和 API 那样写工具和 [MCP 服务器](https://modelcontextprotocol.io/)，而要为智能体设计它们。

我们的目标是扩大智能体的有效作用面，让它能借助工具尝试各种成功策略，解决广泛的任务。所幸，根据我们的经验，对智能体最「符合人机工程学」的工具，最终往往对人类来说也出奇地直观易懂。

## 如何编写工具

本节描述如何与智能体协作，既编写工具、也改进你交给它们的工具。先快速搭一个工具原型并在本地测试；接着运行一次全面评估来度量后续改动的效果。与智能体并肩工作，你可以重复「评估—改进」的过程，直到你的智能体在真实任务上取得强劲表现。

### 构建原型

不上手实操，很难预料智能体会觉得哪些工具顺手、哪些不顺手。先快速搭一个工具原型。如果你在用 [Claude Code](https://www.anthropic.com/claude-code) 写工具（甚至可能一次成型），给它提供工具所依赖的软件库、API 或 SDK 的文档（可能包括 [MCP SDK](https://modelcontextprotocol.io/docs/sdk)）会很有帮助。对 LLM 友好的文档通常能在官方文档站的扁平 `llms.txt` 文件里找到（比如我们 [API 的](https://docs.anthropic.com/llms.txt)）。

把你的工具包进一个[本地 MCP 服务器](https://modelcontextprotocol.io/docs/develop/connect-local-servers)或 [Desktop 扩展](https://www.anthropic.com/engineering/desktop-extensions)（DXT），就能在 Claude Code 或 Claude Desktop 应用里连接并测试它们。

要把本地 MCP 服务器连接到 Claude Code，运行 `claude mcp add <name> <command> [args...]`。

要把本地 MCP 服务器或 DXT 连接到 Claude Desktop 应用，分别进入 `Settings > Developer` 或 `Settings > Extensions`。

工具也可以直接传入 [Anthropic API](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) 调用，做程序化测试。

自己动手测试工具，找出毛刺。收集用户反馈，围绕你期望工具支撑的用例和提示建立直觉。

### 运行评估

接下来，你需要通过运行评估来度量 Claude 使用你工具的水平。先基于真实世界用途生成大量评估任务。我们建议与一个智能体协作，帮你分析结果并确定如何改进工具。完整流程见我们的[工具评估 cookbook](https://platform.claude.com/cookbook/tool-evaluation-tool-evaluation)。

![This graph measures the test set accuracy of human-written vs. Claude-optimized Slack MCP servers.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F6e810aee67f3f3c955832fb7bf9033ffb0102000-1920x1080.png&w=3840&q=75)

我们内部 Slack 工具在留出测试集（held-out test set）上的表现

**生成评估任务**

有了早期原型，Claude Code 可以快速探索你的工具并创建几十对提示-响应对。提示应从真实用例出发，基于真实的数据源和服务（例如内部知识库和微服务）。我们建议避免过于简单、表面的「沙箱」环境——它们不足以用足够的复杂度压测你的工具。强的评估任务可能需要多次工具调用——甚至几十次。

下面是一些强任务的例子：

- 安排下周与 Jane 开会讨论我们最新的 Acme Corp 项目。附上我们上次项目规划会议的记录，并预订一间会议室。
- 客户 ID 9182 反馈一次购买被扣了三次款。找出所有相关日志条目，判断是否有其他客户受到同一问题影响。
- 客户 Sarah Chen 刚提交了取消请求。准备一个挽留方案。请确定：(1) 她离开的原因，(2) 哪种挽留方案最有吸引力，(3) 出方案前我们应留意的风险因素。

再来看一些弱任务：

- 下周与 jane@acme.corp 安排一次会议。
- 在支付日志里搜索 `purchase_complete` 和 `customer_id=9182`。
- 按客户 ID 45892 找到取消请求。

每个评估提示都应配一个可验证的响应或结果。你的验证器可以简单到对 ground truth 与采样响应做精确字符串比较，也可以复杂到请 Claude 来评判响应。避免过于严苛的验证器——它们会因格式、标点或合法的替代措辞这类无谓差异而拒绝正确响应。

对每对提示-响应，你还可以选择性地指定你期望智能体解决任务时调用的工具，以度量智能体在评估中能否领会每个工具的用途。但由于正确解任务可能有多条有效路径，尽量避免过度规定或对特定策略过拟合。

**运行评估**

我们建议用直接的 LLM API 调用、以程序化方式运行评估。使用简单的智能体循环（把交替的 LLM API 调用和工具调用包进 `while` 循环）：每个评估任务一个循环。每个评估智能体应得到单个任务提示和你的工具。

在评估智能体的系统提示中，我们建议指示智能体不仅输出结构化响应块（供验证），还输出推理与反馈块。指示智能体在工具调用与响应块*之前*输出这些内容，可以触发思维链（CoT）行为，提升 LLM 的有效智力。

如果你用 Claude 跑评估，可以打开[交错思考（interleaved thinking）](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#interleaved-thinking)开箱即用地获得类似功能。这能帮你探查智能体为何调用（或不调用）某些工具，并凸显工具描述与规格中具体的改进点。

除了总体准确率，我们建议收集其他指标：单个工具调用与任务的总运行时长、工具调用总数、token 总消耗量、工具错误数。跟踪工具调用有助于揭示智能体常走的路径，也为工具合并提供线索。

![This graph measures the test set accuracy of human-written vs. Claude-optimized Asana MCP servers.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F3f1f47e80974750cd924bc51e42b6df1ad997fab-1920x1080.png&w=3840&q=75)

我们内部 Asana 工具在留出测试集上的表现

**分析结果**
智能体是你发现问题的好帮手，从自相矛盾的工具描述、低效的工具实现到混乱的工具 schema，都能给你反馈。但请记住：智能体在反馈和响应中*省略*的东西，往往比它说出的更重要。LLM 并不总是[想到什么就说什么](https://www.anthropic.com/research/tracing-thoughts-language-model)。

观察你的智能体在哪里卡壳或困惑。通读评估智能体的推理与反馈（或 CoT），找出毛刺。审查原始记录（包括工具调用与工具响应），捕捉 CoT 中没有明说的行为。要读出言外之意——记住你的评估智能体并不知道正确答案和策略。

分析你的工具调用指标。大量冗余的工具调用可能意味着该调整分页或 token 上限参数了；大量因参数无效导致的工具错误，可能意味着工具需要更清晰的描述或更好的示例。我们发布 Claude 的[网页搜索工具](https://www.anthropic.com/news/web-search)时，发现 Claude 会在工具的 `query` 参数后面多余地追加 `2025`，带偏搜索结果、拉低表现（我们通过改进工具描述把 Claude 引回了正轨）。

### 与智能体协作

你甚至可以让智能体替你分析结果、改进工具。只需把评估智能体的记录拼接起来，粘贴进 Claude Code。Claude 是分析记录、一次重构大量工具的专家——例如确保在新的改动做出后，工具实现与描述保持自洽。

事实上，本文的大部分建议都来自我们用 Claude Code 反复优化内部工具实现的过程。我们的评估构建在内部工作区之上，复刻了内部工作流的复杂度，包括真实的项目、文档和消息。

我们依赖留出测试集来确保没有对「训练」评估过拟合。这些测试集表明，即便超出我们用「专家级」工具实现取得的成绩，仍有额外的性能提升空间——无论那些工具是我们的研究员手写的，还是 Claude 自己生成的。

下一节，我们将分享从这一过程中学到的一些东西。

## 编写高效工具的原则

本节把我们的经验提炼成几条编写高效工具的指导原则。

### 为智能体选择合适的工具

工具越多并不总带来越好的结果。我们观察到的一个常见错误是：工具只是包装了现有软件功能或 API 端点，而不考虑这些工具是否适合智能体。原因在于智能体与传统软件有着不同的「可供性」（affordance）——也就是说，它们感知「能用这些工具做什么」的方式不同。

LLM 智能体的「上下文」有限（即一次能处理的信息量有上限），而计算机内存又便宜又充裕。设想在通讯录里查找一个联系人：传统软件程序可以高效地逐个存储和处理联系人列表，逐个检查后再看下一个。

然而，如果一个 LLM 智能体使用的工具返回*全部*联系人，然后不得不逐个逐 token 读下去，它就是在把宝贵的上下文空间浪费在无关信息上（想象你在自己的通讯录里找一个联系人，从第一页到最后一页逐页通读——也就是暴力搜索）。更好、也更自然的做法（对智能体和人类都一样）是先跳到相关的那一页（比如按字母序找到它）。

我们建议先构建少数几个深思熟虑、针对特定高影响工作流、并与你的评估任务相匹配的工具，再从这里扩展。在通讯录的例子里，你或许该实现 `search_contacts` 或 `message_contact`，而不是 `list_contacts`。

工具可以整合功能，在底层一次性处理多个离散操作（或 API 调用）。例如，工具可以在响应中补充相关元数据，或把频繁串联的多步任务合并进一次工具调用。

举几个例子：

- 与其实现 `list_users`、`list_events` 和 `create_event` 三个工具，不如实现一个 `schedule_event` 工具：查找空闲时间并安排日程。
- 与其实现 `read_logs` 工具，不如实现一个 `search_logs` 工具：只返回相关的日志行和少量上下文。
- 与其实现 `get_customer_by_id`、`list_transactions` 和 `list_notes` 三个工具，不如实现一个 `get_customer_context` 工具：一次性汇总某客户全部近期相关信息。

确保你构建的每个工具都有清晰、独特的用途。工具应让智能体以与人类（在获得相同底层资源时）大致相同的方式细分并解决任务，同时省掉原本会被中间输出消耗的上下文。

工具太多或功能重叠也会分散智能体追求高效策略的注意力。对你的工具（或工具的缺席）做精心的选择性规划，回报丰厚。

### 给工具加命名空间

你的 AI 智能体将接入几十个 MCP 服务器和几百个不同工具——包括其他开发者的工具。当工具功能重叠或用途含糊时，智能体会搞不清该用哪个。

命名空间（把相关工具归到共同前缀之下）有助于在大量工具之间划定边界；MCP 客户端有时默认就这样做。例如，按服务命名空间（`asana_search`、`jira_search`）和按资源命名空间（`asana_projects_search`、`asana_users_search`），能帮智能体在正确的时机选对工具。

我们发现，前缀式与后缀式命名空间的选择对工具使用评估有不小的影响。效果因 LLM 而异，我们鼓励你根据自己的评估来选择命名方案。

智能体可能调错工具、用错误的参数调用正确的工具、调用过少的工具，或错误地处理工具响应。通过有选择地实现那些名字反映任务自然切分的工具，你同时减少了装入智能体上下文的工具和工具描述数量，把智能体的计算从上下文卸载回工具调用本身。这降低了智能体犯错的整体风险。

### 让工具返回有意义的上下文

同理，工具实现应小心只把高信号信息返回给智能体。它们应优先考虑上下文相关性而非灵活性，并避免返回底层技术标识符（例如 `uuid`、`256px_image_url`、`mime_type`）。`name`、`image_url`、`file_type` 这类字段更可能直接指导智能体的后续动作和响应。

智能体处理自然语言名称、术语或标识符的成功率，也显著高于处理晦涩标识符。我们发现，仅把任意的字母数字 UUID 解析为更具语义、更可解释的语言（甚至只是 0 起始的 ID 方案），就能通过减少幻觉显著提升 Claude 在检索任务中的精确率。

某些情况下，智能体可能需要同时与自然语言和技术标识符输出交互的灵活性——哪怕只是为了触发下游工具调用（例如 `search_user(name=’jane’)` → `send_message(id=12345)`）。你可以两者兼得：在工具中暴露一个简单的 `response_format` 枚举参数，让智能体控制工具返回 `“concise”`（简明）还是 `“detailed”`（详细）响应（见下图）。

你可以添加更多格式获得更大灵活性，类似 GraphQL 里可以精确选择想接收哪些信息。下面是一个控制工具响应详略程度的 ResponseFormat 枚举示例：

```
enum ResponseFormat {
   DETAILED = "detailed",
   CONCISE = "concise"
}
```

下面是一个详细工具响应的例子（206 token）：

![This code snippet depicts an example of a detailed tool response.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5ed0d30526bf68624f335d075b8c1541be3bb595-1920x1006.png&w=3840&q=75)

下面是一个简明工具响应的例子（72 token）：

![This code snippet depicts a concise tool response.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fd4f649a66482efb5a80cf14ea85e84974ede1c49-1920x725.png&w=3840&q=75)

Slack 的会话串（thread）和串内回复用唯一的 `thread_ts` 标识，获取串内回复必须用到它。`thread_ts` 和其他 ID（`channel_id`、`user_id`）可以从 `“detailed”` 工具响应中取得，供需要它们的后续工具调用使用。`“concise”` 工具响应只返回会话串内容、不含 ID。在这个例子里，`“concise”` 响应只用了约 1/3 的 token。

连工具响应的结构——XML、JSON 还是 Markdown——都会影响评估表现：没有放之四海而皆准的方案。这是因为 LLM 基于下一 token 预测训练，格式越贴近其训练数据表现往往越好。最优响应结构因任务和智能体而异。我们鼓励你基于自己的评估选择最佳响应结构。

### 以 token 效率为目标优化工具响应

优化上下文的*质量*很重要。优化工具响应返回给智能体的上下文*数量*同样重要。

对于任何可能耗尽大量上下文的工具响应，我们建议组合使用分页、范围选择、过滤和/或截断，并配备合理的默认参数值。对 Claude Code，我们默认把工具响应限制在 25,000 token。我们预计智能体的有效上下文长度会随时间增长，但对上下文高效工具的需求会一直存在。

如果你选择截断响应，务必用有用的指示引导智能体。你可以直接鼓励智能体采取更省 token 的策略，比如在知识检索任务中做多次小型、有针对性的搜索，而不是一次宽泛的大搜索。同样，当工具调用报错时（例如输入校验失败），你可以在错误响应上做提示工程，清晰地传达具体、可执行的改进建议，而不是给出晦涩的错误码或堆栈。

下面是一个被截断的工具响应示例：

![This image depicts an example of a truncated tool response.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fe440d6a69d0ca80e71f3bec5c2d00906ff03ce6d-1920x1162.png&w=3840&q=75)

下面是一个无益的错误响应示例：

![This image depicts an example of an unhelpful tool response. ](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F2445187904704fec8c50af0b950e310ba743fac2-1920x733.png&w=3840&q=75)

下面是一个有益的错误响应示例：

![This image depicts an example of a helpful error response.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F810661bd44a35fb273806ae95160040155978c3e-1920x850.png&w=3840&q=75)

工具截断与错误响应可以把智能体引向更省 token 的工具使用行为（使用过滤器或分页），或给出正确格式化工具输入的示例。

### 对工具描述做提示工程

现在来到改进工具最有效的方法之一：对工具描述和规格做提示工程。它们会被装入智能体的上下文，因此可以共同引导智能体形成有效的工具调用行为。

编写工具描述和规格时，想一想你会怎么向团队新入职的同事描述这个工具。把你可能默认带入的上下文——专门的查询格式、小众术语的定义、底层资源之间的关系——都显式写出来。通过清晰描述（并用严格的数据模型强制）预期的输入和输出来避免歧义。特别是，输入参数的命名应毫无歧义：与其叫 `user`，不如叫 `user_id`。

有了评估，你就能更有把握地度量提示工程的影响。哪怕对工具描述做很小的打磨，也可能带来戏剧性的改进。在我们对工具描述做了精确打磨之后，Claude Sonnet 3.5 在 [SWE-bench Verified](https://www.anthropic.com/engineering/swe-bench-sonnet) 评估上取得了最先进的成绩：错误率大幅下降，任务完成率上升。

更多工具定义的最佳实践见我们的[开发者指南](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#best-practices-for-tool-definitions)。如果你在为 Claude 构建工具，我们也建议了解工具是如何被动态加载进 Claude 的[系统提示](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#tool-use-system-prompt)的。最后，如果你在为 MCP 服务器编写工具，[工具注解（tool annotations）](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)有助于声明哪些工具需要开放世界访问或会做破坏性修改。

## 展望

要为智能体构建高效工具，我们需要把软件开发实践从可预测的确定性模式转向非确定性模式。

通过本文描述的迭代式、评估驱动的过程，我们确定了工具成功的稳定规律：高效的工具被有意识地、清晰地定义，审慎地使用智能体上下文，可以在多样工作流中组合使用，并让智能体凭直觉解决真实世界的任务。

未来，我们预计智能体与世界交互的具体机制会持续演化——从 MCP 协议的更新到底层 LLM 本身的升级。以系统化、评估驱动的方法改进智能体工具，我们就能确保：当智能体变得更强，它们使用的工具也随之进化。

## 致谢

作者：Ken Aizawa，感谢来自各部门同事的宝贵贡献——研究团队（Barry Zhang、Zachary Witten、Daniel Jiang、Sami Al-Sheikh、Matt Bell、Maggie Vo）、MCP 团队（Theodora Chu、John Welsh、David Soria Parra、Adam Jones）、产品工程（Santiago Seira）、市场（Molly Vorwerck）、设计（Drew Roper）与应用 AI（Christian Ryan、Alexander Bricken）。

1 指训练底层 LLM 本身之外的改进。

![Interlocking puzzle piece with complex geometric shape and detailed surface texture](https://www-cdn.anthropic.com/images/4zrzovbb/website/43abe7e54b56a891e74a8542944dfbd33f07f49c-1000x1000.svg)

### 想了解更多？

浏览我们的课程：<https://anthropic.skilljar.com/>

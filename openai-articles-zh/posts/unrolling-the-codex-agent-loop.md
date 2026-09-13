---
title: "展开 Codex 智能体循环"
title_en: "Unrolling the Codex agent loop"
source: https://openai.com/index/unrolling-the-codex-agent-loop/
crawled: 2026-09-13
category: engineering
translated: 2026-09-13
---

# 展开 Codex 智能体循环

> 原文：[Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) · OpenAI 博客

[Codex CLI](https://developers.openai.com/codex/cli) 是我们的跨平台本地软件智能体，旨在安全高效地在你的机器上运行的同时，产出高质量、可靠的软件变更。自[我们四月首次发布 CLI](https://openai.com/index/introducing-o3-and-o4-mini/) 以来，我们在如何构建世界级软件智能体方面学到了大量东西。为了剖析这些洞见，本文是一个持续系列的第一篇，我们将探讨 Codex 工作方式的方方面面，以及来之不易的经验教训。（如果你想更细粒度地了解 Codex CLI 是如何构建的，请查看我们的开源代码库 [https://github.com/openai/codex](https://github.com/openai/codex)。我们设计决策的许多细节都记录在 GitHub issues 和 pull request 中，欢迎深入了解。）

作为开篇，我们将聚焦于*智能体循环*（agent loop），它是 Codex CLI 中的核心逻辑，负责协调用户、模型以及模型为完成有意义的软件工作而调用的工具之间的交互。我们希望这篇文章能让你清楚地看到，我们的智能体（或称「执行框架」（harness））在利用 LLM 时所扮演的角色。

在深入之前，先快速说明一下术语：在 OpenAI，「Codex」涵盖一整套软件智能体产品，包括 Codex CLI、Codex Cloud 和 Codex VS Code 扩展。本文聚焦于 Codex *执行框架*（harness），它提供支撑所有 Codex 体验的核心智能体循环与执行逻辑，并通过 Codex CLI 呈现。为行文方便，下文我们将混用「Codex」与「Codex CLI」这两个词。

## 智能体循环

每个 AI 智能体的核心都是所谓的「智能体循环」。智能体循环的简化示意如下：

首先，智能体接收用户的*输入*（input），将其纳入为模型准备的一组文本指令之中，这组指令称为*提示词*（prompt）。

下一步是查询模型：把指令发送给模型并让它生成响应，这一过程称为*推理*（inference）。在推理过程中，文本提示词首先被翻译成一串输入 [token](https://platform.openai.com/docs/concepts#tokens)——即索引到模型词表中的整数。这些 token 随后被用来对模型采样，产生一串新的输出 token。

输出 token 被翻译回文本，成为模型的响应。由于 token 是增量产生的，这一翻译可以在模型运行的同时进行，这也是许多基于 LLM 的应用展示流式输出的原因。在实践中，推理通常被封装在一个以文本为操作对象的 API 之后，把分词（tokenization）的细节抽象掉。

作为推理步骤的结果，模型要么（1）针对用户的原始输入产生最终响应，要么（2）请求一次*工具调用*（tool call），由智能体代为执行（例如「运行 `ls` 并报告输出」）。在情况（2）中，智能体执行该工具调用，并把其输出追加到原始提示词之后。这个输出被用来生成新的输入，用于再次查询模型；智能体随后可以把这些新信息纳入考量并再次尝试。

这一过程不断重复，直到模型不再发出工具调用，而是产生一条面向用户的消息（在 OpenAI 模型中称为*助手消息*（assistant message））。在许多情况下，这条消息直接回答了用户的原始请求，但也可能是向用户的后续追问。

由于智能体可以执行会修改本地环境的工具调用，它的「输出」并不限于助手消息。在许多情况下，软件智能体的主要输出是它在你的机器上编写或修改的代码。尽管如此，每一轮始终以一条助手消息结束——例如「我添加了你要的 `architecture.md`」——它标志着智能体循环中的一个终止状态。从智能体的角度看，它的工作已经完成，控制权交还给用户。

图中所示的从*用户输入*到*智能体响应*的过程被称为对话的一个*轮次*（turn）（在 Codex 中是一个 *thread*）。这个*对话轮次*可以在**模型推理**与**工具调用**之间经历多次迭代。每当你向已有对话发送新消息时，对话历史都会作为新轮次提示词的一部分被包含进来，其中包括来自之前轮次的消息和工具调用：

这意味着随着对话的增长，用于对模型采样的提示词长度也在增长。这个长度很重要，因为每个模型都有一个*上下文窗口*（context window），即单次推理调用可使用的最大 token 数。注意这个窗口同时计入输入*和*输出 token。可以想见，智能体可能在单个轮次中发起数百次工具调用，从而可能耗尽上下文窗口。因此，*上下文窗口管理*是智能体众多职责中的一项。现在，让我们深入看看 Codex 是如何运行智能体循环的。

## 模型推理

Codex CLI 向 [Responses API](https://platform.openai.com/docs/api-reference/responses) 发送 HTTP 请求来运行模型推理。我们将考察信息如何流经 Codex——它使用 Responses API 来驱动智能体循环。

Codex CLI 使用的 Responses API 端点是[可配置的](https://developers.openai.com/codex/config-advanced#custom-model-providers)，因此它可以与任何[实现了 Responses API](https://www.openresponses.org) 的端点配合使用：

- [通过 ChatGPT 登录](https://github.com/openai/codex/blob/d886a8646cb8d3671c3029d08ae8f13fa6536899/codex-rs/core/src/model_provider_info.rs#L141)使用 Codex CLI 时，它使用 `https://chatgpt.com/backend-api/codex/responses` 作为端点
- [使用 API 密钥认证](https://github.com/openai/codex/blob/d886a8646cb8d3671c3029d08ae8f13fa6536899/codex-rs/core/src/model_provider_info.rs#L143)访问 OpenAI 托管的模型时，它使用 `https://api.openai.com/v1/responses` 作为端点
- 以 `--oss` 运行 Codex CLI，配合 [ollama 0.13.4+](https://github.com/openai/codex/pull/8798) 或 [LM Studio 0.3.39+](https://lmstudio.ai/blog/openresponses) 使用 [gpt-oss](https://openai.com/index/introducing-gpt-oss/) 时，它默认使用你电脑上本地运行的 `http://localhost:11434/v1/responses`
- Codex CLI 也可以与 Azure 等云提供商托管的 Responses API 一起使用

让我们看看 Codex 如何为对话中的第一次推理调用创建提示词。

### 构建初始提示词

作为最终用户，你在查询 Responses API 时并不会逐字指定用于采样模型的提示词。相反，你在查询中指定各种输入类型，而 Responses API 服务器会决定如何把这些信息组织成模型被设计为消费的提示词。你可以把提示词想象成一个「条目列表」；本节将解释你的查询如何被转换成这个列表。

在初始提示词中，列表中的每个条目都关联一个角色。`role` 表示关联内容的权重应该有多高，取以下值之一（按优先级从高到低）：`system`、`developer`、`user`、`assistant`。

[Responses API](https://platform.openai.com/docs/api-reference/responses/create) 接受一个带有很多参数的 JSON 负载。我们将聚焦于其中三个：

- [`instructions`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-instructions)：插入模型上下文的 system（或 developer）消息
- [`tools`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-tools)：模型在生成响应时可以调用的工具列表
- [`input`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-input)：给模型的文本、图像或文件输入的列表

在 Codex 中，如果指定了 `instructions` 字段，会从 `~/.codex/config.toml` 中的 [`model_instructions_file`](https://github.com/openai/codex/blob/338f2d634b2360ef3c899cac7e61a22c6b49c94f/codex-rs/core/src/config/mod.rs#L1474-L1483) 读取；否则使用[与模型关联的 `base_instructions`](https://github.com/openai/codex/blob/338f2d634b2360ef3c899cac7e61a22c6b49c94f/codex-rs/core/src/codex.rs#L279-L288)。模型专属的指令存放在 Codex 代码库中并打包进 CLI（例如 [`gpt-5.2-codex_prompt.md`](https://github.com/openai/codex/blob/e958d0337e98f6398771917867d7de689dab3b7a/codex-rs/core/gpt-5.2-codex_prompt.md)）。

`tools` 字段是一个符合 Responses API 所定义 schema 的工具定义列表。对 Codex 而言，其中包括由 Codex CLI 提供的工具、由 Responses API 提供给 Codex 使用的工具，以及由用户提供的工具（通常通过 MCP 服务器）：

#### JavaScript

```
1[2  // Codex's default shell tool for spawning new processes locally.3  {4    "type": "function",5    "name": "shell",6    "description": "Runs a shell command and returns its output...",7    "strict": false,8    "parameters": {9      "type": "object",10      "properties": {11        "command": {"type": "array", "description": "The command to execute", ...},12        "workdir": {"description": "The working directory...", ...},13        "timeout_ms": {"description": "The timeout for the command...", ...},14        ...15      },16      "required": ["command"],17    }18  }1920  // Codex's built-in plan tool.21  {22    "type": "function",23    "name": "update_plan",24    "description": "Updates the task plan...",25    "strict": false,26    "parameters": {27      "type": "object",28      "properties": {"plan":..., "explanation":...},29      "required": ["plan"]30    }31  },3233  // Web search tool provided by the Responses API.34  {35    "type": "web_search",36    "external_web_access": false37  },3839  // MCP server for getting weather as configured in the40  // user's ~/.codex/config.toml.41  {42    "type": "function",43    "name": "mcp__weather__get-forecast",44    "description": "Get weather alerts for a US state",45    "strict": false,46    "parameters": {47      "type": "object",48      "properties": {"latitude": {...}, "longitude": {...}},49      "required": ["latitude", "longitude"]50    }51  }52]
```

最后，JSON 负载中的 `input` 字段是一个条目列表。Codex 在添加用户消息之前，会[把以下条目插入](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L1387-L1415) `input`：

1. 一条 `role=developer` 的消息，描述仅*适用于 `tools` 部分定义的 Codex 自带*`shell`*工具*的沙箱。也就是说，其他工具（例如来自 MCP 服务器的工具）不受 Codex 的沙箱约束，需要自行执行各自的防护措施。

这条消息由一个模板构建，其中的关键内容来自打包进 Codex CLI 的 Markdown 片段，例如 [`workspace_write.md`](https://github.com/openai/codex/blob/1fc72c647fd52e3e73d4309c3b568d4d5fe012b5/codex-rs/protocol/src/prompts/permissions/sandbox_mode/workspace_write.md) 和 [`on_request.md`](https://github.com/openai/codex/blob/1fc72c647fd52e3e73d4309c3b568d4d5fe012b5/codex-rs/protocol/src/prompts/permissions/approval_policy/on_request.md)：

#### Plain Text

```
1<permissions instructions>2  - description of the sandbox explaining file permissions and network access3  - instructions for when to ask the user for permissions to run a shell command4  - list of folders writable by Codex, if any5</permissions instructions>
```

2. （可选）一条 `role=developer` 的消息，其内容是从用户 `config.toml` 文件中读取的 `developer_instructions` 值。

3. （可选）一条 `role=user` 的消息，其内容是「用户指令」（user instructions）。它们并非来自单个文件，而是[从多个来源聚合](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/project_doc.rs#L37-L42)而来。通常，越具体的指令出现得越靠后：

- `$CODEX_HOME` 中 `AGENTS.override.md` 与 `AGENTS.md` 的内容
- 在不超过上限（默认 32 KiB）的前提下，从 `cwd` 的 Git/项目根目录（如果存在）逐层向下到 `cwd` 本身，查看其中每个文件夹：加入其中任何 `AGENTS.override.md`、`AGENTS.md`，或 `config.toml` 中 `project_doc_fallback_filenames` 指定文件名的内容
- 如果配置了任何[技能（skills）](https://developers.openai.com/codex/skills/)：一段关于技能的简短前言、每个技能的[技能元数据](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/skills/model.rs#L6-L13)，以及一节关于[如何使用技能](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/skills/render.rs#L20)的说明

4. 一条 `role=user` 的消息，描述智能体当前运行所在的本地环境。它[指定了当前工作目录和用户的 shell](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/environment_context.rs#L51-L71)：

#### Plain Text

```
1<environment_context>2  <cwd>/Users/mbolin/code/codex5</cwd>3  <shell>zsh</shell>4</environment_context>
```

当 Codex 完成上述所有初始化 `input` 的计算后，它会追加用户消息以开始对话。

前面的例子聚焦于每条消息的内容，但请注意 `input` 的每个元素都是一个带有 `type`、[`role`](https://www.reddit.com/r/OpenAI/comments/1hgxcgi/what_is_the_purpose_of_the_new_developer_role_in/) 和 `content` 的 JSON 对象，如下所示：

#### JSON

```
1{2  "type": "message",3  "role": "user",4  "content": [5    {6      "type": "input_text",7      "text": "Add an architecture diagram to the README.md"8    }9  ]10}
```

当 Codex 组装好要发送给 Responses API 的完整 JSON 负载后，它会发出 HTTP POST 请求，并根据 `~/.codex/config.toml` 中 Responses API 端点的配置附上 `Authorization` 头（如果指定了额外的 HTTP 头和查询参数，也会一并加上）。

当 OpenAI 的 Responses API 服务器收到请求时，它会用这个 JSON 按如下方式推导出模型的提示词（当然，Responses API 的自定义实现可以做出不同的选择）：

可以看到，提示词中前三个条目的顺序由服务器决定，而非客户端。不过，在这三个条目中，只有 *system 消息*的内容也由服务器控制，因为 `tools` 和 `instructions` 由客户端决定。随后是 JSON 负载中的 `input`，共同构成完整的提示词。

有了提示词，我们就可以对模型进行采样了。

### 第一轮

这个发往 Responses API 的 HTTP 请求启动了 Codex 中对话的第一个「轮次」。服务器以 Server-Sent Events（[SSE](https://en.wikipedia.org/wiki/Server-sent_events)）流作为响应。每个事件的 `data` 是一个 JSON 负载，其 `"type"` 以 `"response"` 开头，可能类似于下面这样（完整的事件列表见我们的 [API 文档](https://platform.openai.com/docs/api-reference/responses-streaming)）：

#### Plain Text

```
1data: {"type":"response.reasoning_summary_text.delta","delta":"ah ", ...}2data: {"type":"response.reasoning_summary_text.delta","delta":"ha!", ...}3data: {"type":"response.reasoning_summary_text.done", "item_id":...}4data: {"type":"response.output_item.added", "item":{...}}5data: {"type":"response.output_text.delta", "delta":"forty-", ...}6data: {"type":"response.output_text.delta", "delta":"two!", ...}7data: {"type":"response.completed","response":{...}}
```

Codex [消费这一事件流](https://github.com/openai/codex/blob/2a68b74b9bf16b64e285495c1b149d7d6ac8bdf4/codex-rs/codex-api/src/sse/responses.rs#L334-L342)，并把它们重新发布为可供客户端使用的内部事件对象。像 `response.output_text.delta` 这样的事件用于支持 UI 中的流式输出，而 `response.output_item.added` 等其他事件则被转换为对象，追加到 `input` 中，供后续的 Responses API 调用使用。

假设对 Responses API 的第一个请求包含两个 `response.output_item.done` 事件：一个 `type=reasoning`，一个 `type=function_call`。当我们带着工具调用的响应再次查询模型时，这些事件必须体现在 JSON 的 `input` 字段中：

#### JavaScript

```
1[2  /* ... original 5 items from the input array ... */3  {4    "type": "reasoning",5    "summary": [6      "type": "summary_text",7      "text": "**Adding an architecture diagram for README.md**\n\nI need to..."8    ],9    "encrypted_content": "gAAAAABpaDWNMxMeLw..."10  },11  {12    "type": "function_call",13    "name": "shell",14    "arguments": "{\"command\":\"cat README.md\",\"workdir\":\"/Users/mbolin/code/codex5\"}",15    "call_id": "call_8675309..."16  },17  {18    "type": "function_call_output",19    "call_id": "call_8675309...",20    "output": "<p align=\"center\"><code>npm i -g @openai/codex</code>..."21  }22]
```

在后续查询中用于对模型采样的提示词将如下所示：

特别注意，旧提示词*是新提示词的精确前缀*。这是有意为之，因为它让后续请求高效得多——它使我们能够利用*提示词缓存*（prompt caching，我们将在下一节讨论性能时谈到）。

回看第一张智能体循环示意图，我们可以看到推理与工具调用之间可能有许多次迭代。提示词可能继续增长，直到我们最终收到一条助手消息，标志着本轮结束：

#### Plain Text

```
1data: {"type":"response.output_text.done","text": "I added a diagram to explain...", ...}2data: {"type":"response.completed","response":{...}}
```

在 Codex CLI 中，我们把助手消息呈现给用户，并让输入框获得焦点，以提示用户轮到他们「发言」继续对话。如果用户做出回应，那么上一轮的助手消息连同用户新的消息都必须被追加到 Responses API 请求的 `input` 中，以开启新一轮：

#### JavaScript

```
1[2  /* ... all items from the last Responses API request ... */3  {4    "type": "message",5    "role": "assistant",6    "content": [7      {8        "type": "output_text",9        "text": "I added a diagram to explain the client/server architecture."10      }11    ]12  },13  {14    "type": "message",15    "role": "user",16    "content": [17      {18        "type": "input_text",19        "text": "That's not bad, but the diagram is missing the bike shed."20      }21    ]22  }23]
```

同样地，由于我们在继续一个对话，发送给 Responses API 的 `input` 长度不断增加：

让我们看看这种不断增长的提示词对性能意味着什么。

### 性能考量

你可能会问自己：「等等，就整个对话过程中发送给 Responses API 的 JSON 总量而言，智能体循环岂不是*平方级*的？」你说得对。虽然 Responses API 确实支持一个可选的 [`previous_response_id`](https://platform.openai.com/docs/api-reference/responses/create#responses_create-previous_response_id) 参数来缓解这个问题，但 Codex 目前并不使用它，主要是为了让请求保持完全无状态，并支持零数据保留（Zero Data Retention，ZDR）配置。

不使用 `previous_response_id` 让 Responses API 提供方的实现更简单，因为它确保了每个请求都是*无状态*的。这也让支持已选择加入[零数据保留（ZDR）](https://platform.openai.com/docs/guides/migrate-to-responses#4-decide-when-to-use-statefulness)的客户变得直截了当，因为存储支持 `previous_response_id` 所需的数据会与 ZDR 相冲突。请注意，ZDR 客户并不会因此牺牲从先前轮次的专有推理消息（reasoning messages）中获益的能力，因为相关的 `encrypted_content` 可以在服务器上解密。（OpenAI 会保存 ZDR 客户的解密密钥，但不保存其数据。）Codex 为支持 ZDR 所做的相关改动参见 PR [#642](https://github.com/openai/codex/pull/642) 和 [#1641](https://github.com/openai/codex/pull/1641)。

一般来说，对模型采样的成本远高于网络流量的成本，这使采样成为我们效率优化的首要目标。这正是提示词缓存如此重要的原因：它让我们能够复用上一次推理调用的计算。当缓存命中时，*对模型的采样是线性的而非平方级的*。我们的[提示词缓存](https://platform.openai.com/docs/guides/prompt-caching#structuring-prompts)文档对此有更详细的解释：

*缓存命中只可能发生在提示词内的精确前缀匹配上。要获得缓存收益，请把指令和示例等静态内容放在提示词开头，把用户专属信息等可变内容放在末尾。图像和工具同理，它们在请求之间必须完全一致。*

记住这一点，我们来考虑哪些类型的操作可能在 Codex 中造成「缓存未命中」（cache miss）：

- 在对话进行中更改模型可用的 `tools`。
- 更改 Responses API 请求所针对的 `model`（在实践中，这会改变原始提示词中的第三个条目，因为其中包含模型专属指令）。
- 更改沙箱配置、审批模式或当前工作目录。

Codex 团队在向 Codex CLI 引入可能损害提示词缓存的新功能时必须格外小心。举个例子，我们最初对 MCP 工具的支持曾引入一个 [bug：未能以一致的顺序枚举工具](https://github.com/openai/codex/pull/2611)，从而导致缓存未命中。请注意，MCP 工具可能特别棘手，因为 MCP 服务器可以通过 [`notifications/tools/list_changed`](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#list-changed-notification) 通知动态更改其提供的工具列表。在长对话中途响应这一通知可能造成代价高昂的缓存未命中。

在可能的情况下，对于对话中途发生的配置变更，我们通过向 `input` 追加一条*新*消息来反映变更，而不是修改较早的消息：

- 如果沙箱配置或审批模式发生变化，我们会[插入](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L1037-L1057)一条新的 `role=developer` 消息，其格式与最初的 `<permissions instructions>` 条目相同。
- 如果当前工作目录发生变化，我们会[插入](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L1017-L1035)一条新的 `role=user` 消息，其格式与最初的 `<environment_context>` 相同。

为了性能，我们竭尽所能确保缓存命中。还有一个我们必须管理的关键资源：上下文窗口。

我们避免上下文窗口耗尽的总体策略是：一旦 token 数量超过某个阈值，就*压缩*（compact）对话。具体来说，我们把 `input` 替换为一个新的、更小的、能够代表这段对话的条目列表，让智能体在了解到目前为止发生了什么的前提下继续工作。早期的[压缩实现](https://github.com/openai/codex/pull/1527)需要用户手动调用 `/compact` 命令，它会使用现有对话加上用于[摘要](https://github.com/openai/codex/blob/e2c994e32a31415e87070bef28ed698968d2e549/SUMMARY.md)的自定义指令去查询 Responses API。Codex 把得到的包含摘要的助手消息[作为新的 `input`](https://github.com/openai/codex/blob/e2c994e32a31415e87070bef28ed698968d2e549/codex-rs/core/src/codex.rs#L1424)，用于后续的对话轮次。

此后，Responses API 已演进为支持一个特殊的 [`/responses/compact` 端点](https://platform.openai.com/docs/guides/conversation-state#compaction-advanced)，能更高效地执行压缩。它返回[一个条目列表](https://platform.openai.com/docs/api-reference/responses/compacted-object)，可以用来取代之前的 `input`，在释放上下文窗口的同时继续对话。这个列表包含一个特殊的 `type=compaction` 条目，带有一个不透明的 `encrypted_content` 字段，保存着模型对原始对话的潜在理解。现在，当超过 [`auto_compact_limit`](https://github.com/openai/codex/blob/99f47d6e9a3546c14c43af99c7a58fa6bd130548/codex-rs/core/src/codex.rs#L2558-L2560) 时，Codex 会自动使用这个端点来压缩对话。

## 接下来

我们介绍了 Codex 智能体循环，并梳理了 Codex 在查询模型时如何构建和管理上下文。在这一过程中，我们着重指出了对任何在 Responses API 之上构建智能体循环的人都适用的实用考量与最佳实践。

智能体循环为 Codex 提供了基础，但这只是开始。在后续文章中，我们将深入 CLI 的架构，探讨工具使用是如何实现的，并更仔细地审视 Codex 的沙箱模型。

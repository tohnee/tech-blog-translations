---
title: "Claude 开发者平台高级工具使用功能发布"
title_en: "Introducing advanced tool use on the Claude Developer Platform"
source: https://www.anthropic.com/engineering/advanced-tool-use
published: 2025-11-24
crawled: 2026-09-11
translated: 2026-09-11
---

# Claude 开发者平台高级工具使用功能发布

> 原文：[Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) · Anthropic Engineering Blog

AI 智能体的未来，是模型在成百上千个工具间无缝协作的未来：一个集成了 git 操作、文件操作、包管理器、测试框架和部署流水线的 IDE 助手；一个同时连接 Slack、GitHub、Google Drive、Jira、公司数据库和几十个 MCP 服务器的运营协调器。

要[构建高效智能体](https://www.anthropic.com/research/building-effective-agents)，它们需要与无限的工具库协作，而不是把每个定义都预先塞进上下文。我们关于[用 MCP 做代码执行](https://www.anthropic.com/engineering/code-execution-with-mcp)的文章讨论过，在智能体读取一个请求之前，工具结果和定义有时就要消耗 50,000+ token。智能体应当按需发现和加载工具，只保留与当前任务相关的内容。

智能体还需要能从代码中调用工具。用自然语言做工具调用时，每次调用都需要一次完整的推理，而中间结果无论有用与否都会在上下文中堆积。代码天然适合编排逻辑——循环、条件、数据变换。智能体需要根据手头任务在代码执行与推理之间灵活选择。

智能体还需要从示例中学习正确的工具用法，而不是只靠 schema 定义。JSON schema 能定义什么是结构合法的，却表达不了使用模式：何时包含可选参数、哪些组合才说得通、你的 API 期待什么约定。

今天，我们发布三个使之成为可能的功能：

- **Tool Search Tool（工具搜索工具）**：让 Claude 用搜索工具访问数千个工具，而不消耗其上下文窗口
- **Programmatic Tool Calling（程序化工具调用）**：让 Claude 在代码执行环境中调用工具，降低对模型上下文窗口的冲击
- **Tool Use Examples（工具使用示例）**：为演示如何有效使用给定工具提供通用标准

在内部测试中，我们发现这些功能帮我们造出了用传统工具使用模式无法实现的东西。例如，**[Claude for Excel](https://www.claude.com/claude-for-excel)** 用 Programmatic Tool Calling 读取和修改数千行的电子表格，而不撑爆模型的上下文窗口。

基于我们的经验，我们相信这些功能为你用 Claude 构建的东西打开了新的可能。

## Tool Search Tool

### 挑战

MCP 工具定义提供了重要上下文，但随着接入服务器增多，这些 token 会不断累积。设想一个五服务器配置：

- GitHub：35 个工具（约 26K token）
- Slack：11 个工具（约 21K token）
- Sentry：5 个工具（约 3K token）
- Grafana：5 个工具（约 3K token）
- Splunk：2 个工具（约 2K token）

对话还没开始，58 个工具已消耗约 55K token。再加上 Jira 这样的服务器（单它一个就要约 17K token），你很快逼近 100K+ token 的开销。在 Anthropic，我们见过优化前工具定义消耗 134K token 的情况。

但 token 成本不是唯一的问题。最常见的失败是选错工具和参数出错，尤其当工具名字相近时，比如 `notification-send-user` 与 `notification-send-channel`。

### 我们的方案

Tool Search Tool 不再预先加载所有工具定义，而是按需发现工具。Claude 只看到当前任务实际需要的工具。

![Tool Search Tool diagram](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Ff359296f770706608901eadaffbff4ca0b67874c-1999x1125.png&w=3840&q=75)

*与 Claude 传统方式的 122,800 token 相比，Tool Search Tool 保留了 191,300 token 的上下文。*

传统方式：

- 所有工具定义预先加载（50+ 个 MCP 工具约 72K token）
- 对话历史和系统提示争夺剩余空间
- 在任何工作开始前，总上下文消耗约 77K token

用 Tool Search Tool：

- 预先只加载 Tool Search Tool 本身（约 500 token）
- 工具按需发现（3-5 个相关工具，约 3K token）
- 总上下文消耗约 8.7K token，保住 95% 的上下文窗口

这意味着在保持完整工具库可访问的同时，token 用量减少 85%。内部测试显示，在大型工具库下的 MCP 评估中准确率显著提升：启用 Tool Search Tool 后，Opus 4 从 49% 提升到 74%，Opus 4.5 从 79.5% 提升到 88.1%。

### Tool Search Tool 的工作原理

Tool Search Tool 让 Claude 动态发现工具，而不是预先加载所有定义。你把全部工具定义提供给 API，但用 `defer_loading: true` 标记工具，使其可按需发现。被延迟加载的工具最初不进入 Claude 的上下文。Claude 只看到 Tool Search Tool 本身加上任何 `defer_loading: false` 的工具（你最关键、最常用的那些）。

当 Claude 需要特定能力时，它搜索相关工具。Tool Search Tool 返回匹配工具的引用，这些引用随后在 Claude 的上下文中展开为完整定义。

例如，如果 Claude 需要与 GitHub 交互，它搜索 "github"，于是只有 `github.createPullRequest` 和 `github.listIssues` 被加载——而不是你来自 Slack、Jira 和 Google Drive 的其他 50+ 个工具。

这样，Claude 拥有你完整工具库的访问权，却只为自己实际需要的工具支付 token 成本。

**提示缓存说明：** Tool Search Tool 不会破坏提示缓存，因为被延迟的工具被完全排除在初始提示之外。它们只在 Claude 搜索之后才加入上下文，因此你的系统提示和核心工具定义仍可被缓存。

**实现：**

```
{
  "tools": [
    // Include a tool search tool (regex, BM25, or custom)
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},

    // Mark tools for on-demand discovery
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "input_schema": {...},
      "defer_loading": true
    }
    // ... hundreds more deferred tools with defer_loading: true
  ]
}
```

对 MCP 服务器，你可以延迟加载整个服务器，同时让少数高频工具保持加载：

```
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true}, # defer loading the entire server
  "configs": {
    "search_files": {
"defer_loading": false
    }  // Keep most used tool loaded
  }
}
```

Claude 开发者平台开箱即用地提供基于正则和基于 BM25 的搜索工具，你也可以用嵌入或其他策略实现自定义搜索工具。

### 何时使用 Tool Search Tool

与任何架构决策一样，启用 Tool Search Tool 涉及权衡。该功能在工具调用前增加一个搜索步骤，因此当上下文节省与准确率提升超过额外延迟时，它的回报最高。

**适用场景：**

- 工具定义消耗超过 10K token
- 工具选择准确率出现问题
- 构建多服务器的 MCP 系统
- 可用工具超过 10 个

**收益较小：**

- 小型工具库（<10 个工具）
- 每个会话都频繁用到所有工具
- 工具定义本身很紧凑

## Programmatic Tool Calling

### 挑战

随着工作流复杂化，传统工具调用带来两个根本问题：

- **中间结果污染上下文**：当 Claude 分析一个 10MB 的日志文件找错误模式时，整个文件进入它的上下文窗口，尽管 Claude 只需要一个错误频率摘要。跨多张表取客户数据时，每条记录不管相关与否都在上下文中累积。这些中间结果消耗巨额 token 预算，甚至可能把重要信息完全挤出上下文窗口。
- **推理开销与手工综合**：每次工具调用都需要一次完整的模型推理。拿到结果后，Claude 必须「目测」数据、提取相关信息、推理各部分如何拼合、决定下一步——全部通过自然语言处理完成。一个五工具工作流意味着五次推理，外加 Claude 解析每个结果、比较数值、综合结论。又慢又容易出错。

### 我们的方案

Programmatic Tool Calling 让 Claude 通过代码编排工具，而不是通过一次次的 API 往返。Claude 不再逐个请求工具、每个结果都回到它的上下文，而是写出调用多个工具、处理其输出、并控制哪些信息真正进入上下文窗口的代码。

Claude 擅长写代码。让它用 Python 表达编排逻辑，而不是用自然语言逐个调用工具，你会得到更可靠、更精确的控制流。循环、条件、数据变换和错误处理都显式地写在代码里，而不是隐含在 Claude 的推理中。

#### 示例：预算合规检查

考虑一个常见的业务任务：「哪些团队成员超出了第三季度差旅预算？」

你有三个工具：

- `get_team_members(department)` - 返回带 ID 和级别的团队名单
- `get_expenses(user_id, quarter)` - 返回某用户的费用明细
- `get_budget_by_level(level)` - 返回某职级的预算上限

**传统方式**：

- 取团队名单 → 20 人
- 为每人取 Q3 费用 → 20 次工具调用，每次返回 50-100 条明细（机票、酒店、餐费、收据）
- 按职级取预算上限
- 以上全部进入 Claude 的上下文：2,000+ 条费用明细（50 KB+）
- Claude 手工汇总每人的费用，查询其预算，把费用与预算上限比较
- 更多模型往返，大量上下文消耗

**用 Programmatic Tool Calling**：

工具结果不再逐个返回给 Claude，而是由 Claude 写一个 Python 脚本编排整个工作流。脚本在 Code Execution 工具（一个沙箱环境）中运行，需要你工具的结果时暂停。你通过 API 返回工具结果后，它们由脚本处理而不是被模型消费。脚本继续执行，Claude 只看到最终输出。

![Programmatic tool calling flow](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F65737d69a3290ed5c1f3c3b8dc873645a9dcc2eb-1999x1491.png&w=3840&q=75)

Programmatic Tool Calling 让 Claude 通过代码而非逐次 API 往返来编排工具，并支持并行工具执行。

以下是 Claude 为预算合规任务写出的编排代码：

```
team = await get_team_members("engineering")

# Fetch budgets for each unique level
levels = list(set(m["level"] for m in team))
budget_results = await asyncio.gather(*[
    get_budget_by_level(level) for level in levels
])

# Create a lookup dictionary: {"junior": budget1, "senior": budget2, ...}
budgets = {level: budget for level, budget in zip(levels, budget_results)}

# Fetch all expenses in parallel
expenses = await asyncio.gather(*[
    get_expenses(m["id"], "Q3") for m in team
])

# Find employees who exceeded their travel budget
exceeded = []
for member, exp in zip(team, expenses):
    budget = budgets[member["level"]]
    total = sum(e["amount"] for e in exp)
    if total > budget["travel_limit"]:
        exceeded.append({
            "name": member["name"],
            "spent": total,
            "limit": budget["travel_limit"]
        })

print(json.dumps(exceeded))
```

Claude 的上下文只收到最终结果：超出预算的那两三个人。那 2,000+ 条明细、中间求和、预算查询统统不影响 Claude 的上下文——消耗从 200KB 的原始费用数据降到 1KB 的结果。

效率收益可观：

- **token 节省**：把中间结果挡在 Claude 上下文之外，PTC 大幅降低 token 消耗。平均用量从 43,588 降到 27,297 token——复杂研究任务上减少 37%。
- **降低延迟**：每次 API 往返都需要模型推理（数百毫秒到数秒）。当 Claude 在单个代码块中编排 20+ 个工具调用时，你省掉了 19+ 次推理。API 处理工具执行，无需每次回到模型。
- **准确率提升**：通过写显式的编排逻辑，Claude 比在自然语言中同时摆弄多个工具结果时出错更少。内部知识检索从 25.6% 提升到 28.5%；[GIA 基准](https://arxiv.org/abs/2311.12983)从 46.5% 提升到 51.2%。

生产工作流充满脏数据、条件逻辑和需要规模化的操作。Programmatic Tool Calling 让 Claude 以程序化方式驾驭这些复杂度，把注意力放在可行动的结果上，而不是原始数据处理。

### Programmatic Tool Calling 的工作原理

#### 1. 把工具标记为可从代码调用

在 tools 中加入 code_execution，并设置 allowed_callers 把工具加入程序化执行：

```
{
  "tools": [
    {
      "type": "code_execution_20250825",
      "name": "code_execution"
    },
    {
      "name": "get_team_members",
      "description": "Get all members of a department...",
      "input_schema": {...},
      "allowed_callers": ["code_execution_20250825"] # opt-in to programmatic tool calling
    },
    {
      "name": "get_expenses",
 	...
    },
    {
      "name": "get_budget_by_level",
	...
    }
  ]
}
```

API 会把这些工具定义转换成 Claude 可以调用的 Python 函数。

#### 2. Claude 编写编排代码

Claude 不再逐个请求工具，而是生成 Python 代码：

```
{
  "type": "server_tool_use",
  "id": "srvtoolu_abc",
  "name": "code_execution",
  "input": {
    "code": "team = get_team_members('engineering')\n..." # the code example above
  }
}
```

#### 3. 工具执行时不经过 Claude 的上下文

当代码调用 get_expenses() 时，你会收到一个带 caller 字段的工具请求：

```
{
  "type": "tool_use",
  "id": "toolu_xyz",
  "name": "get_expenses",
  "input": {"user_id": "emp_123", "quarter": "Q3"},
  "caller": {
    "type": "code_execution_20250825",
    "tool_id": "srvtoolu_abc"
  }
}
```

你提供结果，它在 Code Execution 环境中被处理，而不是进入 Claude 的上下文。这个请求-响应循环对代码中的每次工具调用重复进行。

#### 4. 只有最终输出进入上下文

代码运行结束后，只有代码的结果返回给 Claude：

```
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_abc",
  "content": {
    "stdout": "[{\"name\": \"Alice\", \"spent\": 12500, \"limit\": 10000}...]"
  }
}
```

这就是 Claude 看到的全部，而不是过程中处理的 2000+ 条费用明细。

### 何时使用 Programmatic Tool Calling

Programmatic Tool Calling 在工作流中增加一个代码执行环节。当 token 节省、延迟改进和准确率提升足够可观时，这份额外开销是值得的。

**收益最大：**

- 处理大型数据集，而你只需要聚合或摘要
- 运行含三个及以上相依工具调用的多步工作流
- 在 Claude 看到工具结果之前先行过滤、排序或转换
- 处理中间数据不应影响 Claude 推理的任务
- 对大量条目并行操作（例如检查 50 个端点）

**收益较小：**

- 简单的单工具调用
- 任务要求 Claude 看到并对所有中间结果做推理
- 快速查询且响应很小

## Tool Use Examples

### 挑战

JSON Schema 擅长定义结构——类型、必填字段、允许的枚举——但它表达不了使用模式：何时包含可选参数、哪些组合才说得通、你的 API 期待什么约定。

设想一个工单 API：

```
{
  "name": "create_ticket",
  "input_schema": {
    "properties": {
      "title": {"type": "string"},
      "priority": {"enum": ["low", "medium", "high", "critical"]},
      "labels": {"type": "array", "items": {"type": "string"}},
      "reporter": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "contact": {
            "type": "object",
            "properties": {
              "email": {"type": "string"},
              "phone": {"type": "string"}
            }
          }
        }
      },
      "due_date": {"type": "string"},
      "escalation": {
        "type": "object",
        "properties": {
          "level": {"type": "integer"},
          "notify_manager": {"type": "boolean"},
          "sla_hours": {"type": "integer"}
        }
      }
    },
    "required": ["title"]
  }
}
```

schema 定义了什么是合法的，却留下一堆关键问题没有回答：

- **格式歧义：** `due_date` 该用 "2024-11-06"、"Nov 6, 2024" 还是 "2024-11-06T00:00:00Z"？
- **ID 约定：** `reporter.id` 是 UUID、"USR-12345"，还是就是 "12345"？
- **嵌套结构用法：** Claude 何时该填 `reporter.contact`？
- **参数关联：** `escalation.level` 和 `escalation.sla_hours` 与 priority 什么关系？

这些歧义会导致格式错误的工具调用和不一致的参数使用。

### 我们的方案

Tool Use Examples 让你直接在工具定义中提供示例调用。不只依赖 schema，你向 Claude 展示具体的使用模式：

```
{
    "name": "create_ticket",
    "input_schema": { /* same schema as above */ },
    "input_examples": [
      {
        "title": "Login page returns 500 error",
        "priority": "critical",
        "labels": ["bug", "authentication", "production"],
        "reporter": {
          "id": "USR-12345",
          "name": "Jane Smith",
          "contact": {
            "email": "jane@acme.com",
            "phone": "+1-555-0123"
          }
        },
        "due_date": "2024-11-06",
        "escalation": {
          "level": 2,
          "notify_manager": true,
          "sla_hours": 4
        }
      },
      {
        "title": "Add dark mode support",
        "labels": ["feature-request", "ui"],
        "reporter": {
          "id": "USR-67890",
          "name": "Alex Chen"
        }
      },
      {
        "title": "Update API documentation"
      }
    ]
  }
```

从这三个例子中，Claude 学到：

- **格式约定**：日期用 YYYY-MM-DD，用户 ID 形如 USR-XXXXX，标签用 kebab-case
- **嵌套结构模式**：如何构造带嵌套 contact 对象的 reporter 对象
- **可选参数的关联规律**：critical 级 bug 带完整联系信息 + 紧迫 SLA 的升级配置；功能请求有 reporter 但无 contact/escalation；内部任务只有标题

在我们自己的内部测试中，工具使用示例把复杂参数处理的准确率从 72% 提升到 90%。

### 何时使用 Tool Use Examples

Tool Use Examples 会给工具定义增加 token，因此当准确率提升超过额外成本时最有价值。

**收益最大：**

- 复杂嵌套结构——合法 JSON 不等于正确用法
- 工具有大量可选参数、且包含模式很重要
- API 有 schema 表达不了的领域特定约定
- 相似工具之间需要示例澄清该用哪个（如 `create_ticket` vs `create_incident`）

**收益较小：**

- 用法显而易见的简单单参数工具
- Claude 已经理解的 URL、邮箱等标准格式
- 验证问题更适合由 JSON Schema 约束处理

## 最佳实践

构建能对现实世界采取行动的智能体，意味着同时应对规模、复杂度和精度。这三个功能协同工作，解决工具使用工作流中不同的瓶颈。以下是有效组合它们的方法。

### 有策略地分层启用

并非每个智能体在每个任务上都需要三个功能全开。从你最大的瓶颈入手：

- 工具定义导致上下文膨胀 → Tool Search Tool
- 大体量中间结果污染上下文 → Programmatic Tool Calling
- 参数错误与畸形调用 → Tool Use Examples

这种聚焦方式让你先解决限制智能体表现的具体约束，而不是预先堆叠复杂度。

然后按需叠加其他功能。它们是互补的：Tool Search Tool 确保找到对的工具，Programmatic Tool Calling 确保高效执行，Tool Use Examples 确保正确调用。

### 配置 Tool Search Tool 提升发现质量

工具搜索匹配名称和描述，所以清晰、描述性强的定义能提升发现准确率。

```
// Good
{
    "name": "search_customer_orders",
    "description": "Search for customer orders by date range, status, or total amount. Returns order details including items, shipping, and payment info."
}

// Bad
{
    "name": "query_db_orders",
    "description": "Execute order query"
}
```

在系统提示中加入指引，让 Claude 知道有什么可用：

```
You have access to tools for Slack messaging, Google Drive file management, 
Jira ticket tracking, and GitHub repository operations. Use the tool search 
to find specific capabilities.
```

把你最常用的三到五个工具设为始终加载，其余全部延迟。这样既保证常用操作的即时可用，又让其他一切按需发现。

### 配置 Programmatic Tool Calling 保证执行正确

既然 Claude 要写代码解析工具输出，就要把返回格式文档写清楚。这帮 Claude 写出正确的解析逻辑：

```
{
    "name": "get_orders",
    "description": "Retrieve orders for a customer.
Returns:
    List of order objects, each containing:
    - id (str): Order identifier
    - total (float): Order total in USD
    - status (str): One of 'pending', 'shipped', 'delivered'
    - items (list): Array of {sku, quantity, price}
    - created_at (str): ISO 8601 timestamp"
}
```

以下类型的工具适合加入程序化编排：

- 可以并行运行的工具（相互独立的操作）
- 重试安全的操作（幂等）

### 配置 Tool Use Examples 保证参数准确

精心打造示例，让行为清晰可辨：

- 用真实数据（真实城市名、合理价格，不要 "string" 或 "value"）
- 展示多样性：最小、部分、完整三种指定模式
- 保持精炼：每个工具 1-5 个示例
- 聚焦歧义（只在 schema 无法显而易见地推出正确用法的地方加示例）

## 上手指南

这些功能以 beta 提供。启用时加上 beta 头，并包含你需要的工具：

```
client.beta.messages.create(
    betas=["advanced-tool-use-2025-11-20"],
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {"type": "code_execution_20250825", "name": "code_execution"},
        # Your tools with defer_loading, allowed_callers, and input_examples
    ]
)
```

详细的 API 文档与 SDK 示例见我们的：

- Tool Search Tool 的[文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)与 [cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_search_with_embeddings.ipynb)
- Programmatic Tool Calling 的[文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)与 [cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/programmatic_tool_calling_ptc.ipynb)
- Tool Use Examples 的[文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use#providing-tool-use-examples)

这些功能把工具使用从简单的函数调用推向智能编排。随着智能体着手应对跨越几十个工具和大型数据集的更复杂工作流，动态发现、高效执行和可靠调用将成为基石。

期待看到你构建的东西。

## 致谢

作者：Bin Wu，Adam Jones、Artur Renault、Henry Tay、Jake Noble、Noah Picard、Sam Jiang 及 Claude 开发者平台团队亦有贡献。本工作建立在 Chris Gorgolewski、Daniel Jiang、Jeremy Fox 和 Mike Lambert 的基础研究之上。我们也从整个 AI 生态中获得启发，包括 [Joel Pobar 的 LLMVM](https://github.com/9600dev/llmvm)、[Cloudflare 的 Code Mode](https://blog.cloudflare.com/code-mode/) 和 [Code Execution as MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)。特别感谢 Andy Schumeister、Hamish Kerr、Keir Bradwell、Matt Bleifer 和 Molly Vorwerck 的支持。

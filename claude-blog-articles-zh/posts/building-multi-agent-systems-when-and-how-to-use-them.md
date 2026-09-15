---
title: "何时使用多智能体系统（以及何时不使用）"
title_en: "When to use multi-agent systems (and when not to)"
source: https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them/
crawled: 2026-09-14
translated: 2026-09-14
---

# 何时使用多智能体系统（以及何时不使用）

> 原文：[When to use multi-agent systems (and when not to)](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them/) · Claude 博客

## 什么是多智能体系统？

多智能体系统是一种架构：多个 LLM 实例各自运行在独立的会话上下文中，并通过代码进行协调。每个智能体负责任务中一个不同的切片——例如一个子智能体负责研究，而编排器负责规划——这样既能保护上下文、支持并行工作，也能实现单个智能体无法长期维持的专业化分工。

协调模式有多种（智能体蜂群、基于能力的系统、消息总线架构等），但本文聚焦于编排者-子智能体模式（orchestrator-subagent pattern）：一种分层模型，由主智能体为特定子任务生成并管理专业化的子智能体。这一模式提供了简单直接的协调模型，是初次接触多智能体系统的团队的良好起点。我们将在下一篇文章中详细探讨其他模式。

如今，多智能体系统常常被用在单一智能体反而表现更好的场景中——尽管随着模型进步，这笔账也在不断变化。在 Anthropic，我们见过团队投入数月构建精巧的多智能体架构，最后却发现，在单个智能体上改进提示就能取得同等效果。

在构建多智能体系统并与在生产环境中部署它们的团队合作之后，我们总结出多个智能体持续优于单个智能体的三种情形：上下文污染导致性能下降时、任务可以并行运行时，以及专业化分工能改善工具选择或任务专注度时。在这三种情形之外，协调成本通常大于收益。

在本文中，我们将分享如何识别单智能体的能力边界、辨析多智能体系统大显身手的三种场景，以及如何避免常见的实现错误。

## 先从单个智能体开始的理由

一个设计良好、配备了合适工具的单智能体，能完成的工作远超许多开发者的预期。

多智能体系统会引入额外开销。每增加一个智能体，就多一个潜在故障点、多一套需要维护的提示，也多一个意外行为的来源。

我们观察到一些团队构建了精巧的多智能体系统，分别为规划、执行、评审和迭代设置独立智能体，结果却发现它们在每次交接时都会丢失上下文，而且花在协调上的 token 比实际执行还多。在我们的测试中，完成同等任务时，多智能体实现通常比单智能体方案多消耗 3-10 倍的 token。这些开销来自跨智能体复制上下文、智能体之间的协调消息，以及为交接而做的结果摘要。

## 多智能体系统的决策框架

当多智能体架构能够解决单智能体无法克服的特定约束时，它才有价值。这意味着多智能体架构应当保留给那些收益明确、足以抵偿额外成本的场景。托管基础设施也可以替你处理这些（参见 [Claude Managed Agents 中的多智能体编排](https://claude.com/blog/new-in-claude-managed-agents)）。

下面这些模式，是我们持续观察到这项投入能带来正回报的场景。

### 上下文保护

大语言模型的上下文窗口是有限的，随着上下文增长，回答质量可能下降。当智能体的上下文中积累了来自某个子任务、却与后续子任务无关的信息时，就会发生上下文污染（context pollution）。子智能体提供了隔离——每个子智能体都在自己干净的上下文中运行，专注于各自的任务。

设想一个客户支持智能体，需要在诊断技术问题的同时查询订单历史。如果每次订单查询都会给上下文增加数千 token，智能体对技术问题的推理能力就会退化。

**单智能体方案：**

```
# Single agent accumulates everything in context
conversation_history = [
    {"role": "user", "content": "My order #12345 isn't working"},
    {"role": "assistant", "content": "Let me check your order..."},
    # Tool result adds 2000+ tokens of order history
    {"role": "user", "content": "... (order details, past purchases, shipping info) ..."},
    {"role": "assistant", "content": "Now let me diagnose the technical issue..."},
    # Context is now polluted with order details the agent doesn't need
]

```

智能体必须在上下文中保留 2000 多 token 的无关订单历史的同时推理技术问题，注意力被稀释，回答质量随之下降。

**多智能体方案：**

```
from anthropic import Anthropic

client = Anthropic()

class OrderLookupAgent:
    def lookup_order(self, order_id: str) -> dict:
        # Separate agent with its own context
        messages = [
            {"role": "user", "content": f"Get essential details for order {order_id}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=messages,
            tools=[get_order_details_tool]
        )
        # Returns only essential information
        return extract_summary(response)

class SupportAgent:
    def handle_issue(self, user_message: str):
        if needs_order_info(user_message):
            order_id = extract_order_id(user_message)
            # Get only what's needed, not full history
            order_summary = OrderLookupAgent().lookup_order(order_id)
            # Inject compact summary, not full context
            context = f"Order {order_id}: {order_summary['status']}, purchased {order_summary['date']}"
        
        # Main agent context stays clean
        messages = [
            {"role": "user", "content": f"{context}\n\nUser issue: {user_message}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            messages=messages
        )
        return response

```

订单查询智能体处理完整的订单历史并提取摘要。主智能体只接收它真正需要的 50-100 个 token，上下文保持聚焦。

当子任务产生大量上下文（超过 1000 token）而其中大部分信息与主任务无关时、当子任务定义清晰且明确规定了要提取哪些信息时，以及对于需要先过滤再使用的查询或检索操作，上下文隔离最为有效。

### 并行化

并行运行多个智能体，让你可以探索比单个智能体覆盖范围更大的搜索空间。这一模式在搜索和研究类任务中被证明尤其有价值。

Anthropic 的研究团队在[《我们如何构建多智能体研究系统》](https://www.anthropic.com/engineering/multi-agent-research-system)一文中记录了这一点。主智能体分析查询，并生成多个子智能体并行调查不同侧面。每个子智能体独立搜索，然后返回提炼后的发现。多智能体搜索能够在更大的信息空间中探索，因而在准确性上显著优于单智能体方案。

其核心实现是：把问题分解为相互独立的侧面，并发运行子智能体，然后综合结果。

```
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def research_topic(query: str) -> dict:
    # Lead agent breaks query into research facets
    facets = await lead_agent.decompose_query(query)
    
    # Spawn subagents to research each facet in parallel
    tasks = [
        research_subagent(facet) 
        for facet in facets
    ]
    results = await asyncio.gather(*tasks)
    
    # Lead agent synthesizes findings
    return await lead_agent.synthesize(results)

async def research_subagent(facet: str) -> dict:
    """Each subagent has its own context window"""
    messages = [
        {"role": "user", "content": f"Research: {facet}"}
    ]
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=messages,
        tools=[web_search, read_document]
    )
    return extract_findings(response)
```

这种覆盖面的提升是有代价的。完成同等任务时，多智能体系统通常比单智能体方案多消耗 3 到 10 倍的 token。原因在于：每个智能体都需要自己的上下文，智能体之间必须交换消息来协调，结果在智能体之间传递时必须做摘要。虽然与顺序执行所有工作相比，并行有助于缩短总执行时间，但由于总计算量的大幅增加，多智能体系统的整体耗时往往仍长于单智能体系统。

并行化的主要收益是彻底性，而非速度。当你需要在大型信息空间中搜索，或从多个角度调查一个复杂问题时，并行智能体能比受上下文限制的单个智能体覆盖更多领域。其权衡是：用更高的 token 消耗和往往更长的总执行时间，换取更全面的结果。

### 专业化

不同的任务有时需要不同的工具集、系统提示或专业领域知识。与其让单个智能体访问几十个工具，不如使用与其职责相匹配的精简工具集的专业化智能体，这样可以提高可靠性。

#### **工具集专业化**

当智能体可以访问的工具过多时，性能会受损。以下三个信号表明工具专业化会有帮助：

1. **数量。** 工具过多的智能体（通常是 20 个以上）难以选出合适的工具。
2. **领域混淆。** 当工具横跨多个互不相关的领域（数据库操作、API 调用、文件系统操作）时，智能体会搞不清某个任务适用哪个领域。
3. **性能退化。** 新增工具会导致既有任务上的性能下降，说明智能体已达到其工具管理能力的上限。

#### **系统提示专业化**

不同的任务有时需要不同的人设、约束或指令，而把它们组合在一起时会相互冲突。客户支持智能体需要富有同理心、有耐心；代码评审智能体需要精确、挑剔。合规检查智能体需要严格遵循规则；头脑风暴智能体需要创造性的灵活性。当单个智能体必须在相互冲突的行为模式之间切换时，拆分为配备定制系统提示的专业化智能体能产生更一致的结果。

每个专业化智能体都受制于其指令的质量——那些能改进单个智能体输出的[提示工程最佳实践](https://claude.com/blog/best-practices-for-prompt-engineering)，同样适用于每个子智能体的系统提示。

#### **领域专长专业化**

有些任务受益于深入的领域上下文，而这些内容会让一个通才型智能体不堪重负。法律分析智能体可能需要大量关于判例法和监管框架的上下文。医学研究智能体可能需要关于临床试验方法学的专业知识。与其把所有领域上下文都塞进单个智能体，不如让专业化智能体各自携带与其具体职责相关的聚焦专长。

**示例：多平台集成。** 设想一个集成系统，智能体需要跨 CRM、营销自动化和消息平台工作。每个平台有 10-15 个相关的 API 端点。一个拥有 40 多个工具的单智能体常常难以正确选择，会把不同平台上的相似操作搞混。拆分为配备聚焦工具集和定制提示的专业化智能体，可以解决选错工具的问题。

```
from anthropic import Anthropic

client = Anthropic()

# Specialized agents with focused toolsets and tailored prompts
class CRMAgent:
    """Handles customer relationship management operations"""
    system_prompt = """You are a CRM specialist. You manage contacts, 
    opportunities, and account records. Always verify record ownership 
    before updates and maintain data integrity across related records."""
    tools = [
        crm_get_contacts,
        crm_create_opportunity,
        # 8-10 CRM-specific tools
    ]

class MarketingAgent:
    """Handles marketing automation operations"""
    system_prompt = """You are a marketing automation specialist. You 
    manage campaigns, lead scoring, and email sequences. Prioritize 
    data hygiene and respect contact preferences."""
    tools = [
        marketing_get_campaigns,
        marketing_create_lead,
        # 8-10 marketing-specific tools
    ]

class OrchestratorAgent:
    """Routes requests to specialized agents"""
    def execute(self, user_request: str):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="""You coordinate platform integrations. Route requests to the appropriate specialist:
- CRM: Contact records, opportunities, accounts, sales pipeline
- Marketing: Campaigns, lead nurturing, email sequences, scoring
- Messaging: Notifications, alerts, team communication""",
            messages=[
                {"role": "user", "content": user_request}
            ],
            tools=[delegate_to_crm, delegate_to_marketing, delegate_to_messaging]
        )
        return response

```

这一模式如同高效的专业协作：工具与职责相匹配的专家，比试图在所有领域都维持专业水平的通才协作得更出色。不过，专业化会引入路由复杂度。编排器必须正确分类请求并委派给合适的智能体，路由错误会导致糟糕的结果。维护多个专业化智能体也会增加提示维护开销。当领域界限清晰可分、路由决策没有歧义时，专业化工作得最好。

## 超出单智能体架构的适用范围

除了上述通用框架之外，还有一些具体信号表明单智能体模式已经不够用了：

**接近上下文上限。** 如果智能体经常使用大量上下文且性能正在退化，上下文压力可能就是瓶颈。请注意，上下文管理的最新进展（[如 compaction 压缩](https://platform.claude.com/cookbook/tool-use-automatic-context-compaction)）正在削弱这一限制，让单智能体能在长得多的时间跨度内维持有效记忆。

**管理大量工具。** 当智能体拥有 15-20 个以上工具时，模型要花大量上下文和注意力来理解自己的选项。在采用多智能体架构之前，可以考虑使用 [Tool Search Tool](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/tool-search-tool)，它让 Claude 按需动态发现工具，而不是预先加载全部工具定义。这可以[将 token 用量最多降低 85%](https://www.anthropic.com/engineering/advanced-tool-use)，同时提高工具选择的准确性。

**可并行的子任务。** 当任务可以自然分解为相互独立的部分（跨多个来源的研究、针对多个组件的测试）时，并行子智能体能带来显著的加速。

这些阈值会随着模型进步而变化。当前的界限只是实用参考，并非根本性约束。

## 以上下文为中心的拆分

采用多智能体架构时，最重要的设计决策是如何在智能体之间划分工作。我们观察到，团队经常做出错误的选择，导致协调开销抵消了多智能体设计的收益。

关键洞见是：在拆分工作时采用**以上下文为中心的视角**，而不是以问题为中心的视角。

**以问题为中心的拆分（往往适得其反）。** 按工作类型划分（一个智能体写功能，另一个写测试，第三个评审代码）会带来持续的协调开销。每次交接都会丢失上下文。写测试的智能体不了解某些实现决策背后的原因，代码评审的智能体也缺少探索和迭代过程的上下文。

**以上下文为中心的拆分（通常有效）。** 按上下文边界划分意味着，负责某个功能的智能体也应负责它的测试，因为它已经拥有必要的上下文。只有当上下文能够被真正隔离时，才应该拆分工作。

这一原则来自对多智能体系统失败模式的观察。当智能体按问题类型拆分时，它们会陷入「传话游戏」（telephone game）：信息来回传递，每次交接都在损失保真度。在一个按软件开发角色（规划者、实现者、测试者、评审者）划分专业智能体的实验中，子智能体花在协调上的 token 比实际工作还多。

**有效的拆分边界包括：**

- **独立的研究路径。** 调查「亚洲市场趋势」与「欧洲市场趋势」可以并行推进，无需共享上下文。
- **接口清晰、彼此分离的组件。** 只要 API 契约定义明确，前端和后端工作就可以并行推进。
- **黑盒验证。** 只需运行测试并报告结果的验证者，不需要实现上下文。

**有问题的拆分边界包括：**

- **同一工作的先后阶段。** 同一功能的规划、实现和测试共享了太多上下文。
- **紧密耦合的组件。** 需要频繁来回沟通的组件应属于同一个智能体。
- **需要共享状态的工作。** 需要频繁同步认知的智能体应保持在一起。

## 验证子智能体模式

有一种多智能体模式在各领域都持续表现良好，那就是**验证子智能体**（verification subagent）。它是专门的智能体，唯一职责就是测试或验证主智能体的工作。

值得注意的是，能力更强的编排器模型（如 Claude Opus 4.5）已越来越能够直接评估子智能体的工作，而无需单独的验证步骤。不过，在使用能力较弱的编排器、验证需要专门的工具，或者你想在工作流中强制设置明确的验证检查点时，验证子智能体仍然很有价值。

验证子智能体之所以成功，是因为它们绕开了传话游戏问题。验证天然只需要极少的上下文传递，因此验证者可以对系统做黑盒测试，而无需了解系统是如何构建的完整历史。

### 实现多智能体系统

主智能体完成一个工作单元后，在继续推进之前，它会生成一个验证子智能体，并交给它待验证的产物、明确的成功标准，以及执行验证所需的工具。

验证者不需要理解产物为何被构建成这个样子，它只需要判断产物是否满足既定标准。

```
from anthropic import Anthropic

client = Anthropic()

class CodingAgent:
    def implement_feature(self, requirements: str) -> dict:
        """Main agent implements the feature"""
        messages = [
            {"role": "user", "content": f"Implement: {requirements}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            messages=messages,
            tools=[read_file, write_file, list_directory]
        )
        return {
            "code": response.content,
            "files_changed": extract_files(response)
        }

class VerificationAgent:
    def verify_implementation(self, requirements: str, files_changed: list) -> dict:
        """Separate agent verifies the work"""
        messages = [
            {"role": "user", "content": f"""
Requirements: {requirements}
Files changed: {files_changed}

Run the test suite and verify:
1. All existing tests pass
2. New functionality works as specified
3. No obvious errors or security issues

You MUST run the complete test suite before marking as passed.
Do not mark as passing after only running a few tests.
Run: pytest --verbose
Only mark as PASSED if ALL tests pass with no failures.
"""}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            messages=messages,
            tools=[run_tests, execute_code, read_file]
        )
        return {
            "passed": extract_pass_fail(response),
            "issues": extract_issues(response)
        }

def implement_with_verification(requirements: str, max_attempts: int = 3):
    for attempt in range(max_attempts):
        result = CodingAgent().implement_feature(requirements)
        verification = VerificationAgent().verify_implementation(
            requirements,
            result['files_changed']
        )
        
        if verification['passed']:
            return result
        
        requirements += f"\n\nPrevious attempt failed: {verification['issues']}"
    
    raise Exception(f"Failed verification after {max_attempts} attempts")
```

### 多智能体系统的应用场景

验证子智能体适用于：

- **质量保证。** 运行测试套件、对代码进行 lint、对照 schema 校验输出。
- **合规检查。** 验证文档符合政策要求，对照规则检查输出。
- **输出校验。** 在交付前确认生成的内容符合规格。
- **事实核查。** 由另一个独立智能体验证生成内容中的论断或引用。

### 过早宣告胜利问题

验证子智能体最严重的失败模式，是在没有充分测试的情况下就把输出标记为通过。验证者只运行一两个测试，看到通过，便宣告成功。

缓解策略包括：

- **具体的标准。** 明确要求「运行完整测试套件并报告所有失败」，而不是「确保它能用」。
- **全面的检查。** 要求验证者测试多个场景和边界情况。
- **反向测试。** 指示验证者尝试应当失败的输入，并确认它们确实失败。
- **明确的指令。** 「你必须先运行完整测试套件才能标记为通过」这条指令至关重要。如果没有对全面验证的明确要求，验证智能体会走捷径。

## 在单智能体与多智能体系统之间做选择

多智能体系统很强大，但并非放之四海而皆准。在引入多个协调智能体带来的复杂性之前，请确认：

1. **确实存在多智能体能解决的约束**，例如上下文限制、并行化机会，或专业化的需要。
2. **拆分依据是上下文，而不是问题类型。** 按工作所需的上下文来分组，而不是按工作的种类。
3. **存在清晰的验证点**，让子智能体无需完整上下文即可验证工作。

我们的建议是？从能用的最简单方案开始，只有证据支持时才增加复杂度。

*这是多智能体系统系列文章的第一篇。关于单智能体模式的更多内容，请参阅[*构建高效智能体*](https://www.anthropic.com/engineering/building-effective-agents)。关于上下文管理策略，请参阅[*面向 AI 智能体的高效上下文工程*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。关于我们如何构建多智能体研究系统的深入解析，请参阅[*我们如何构建多智能体研究系统*](https://www.anthropic.com/engineering/multi-agent-research-system)。*

## 致谢

本文由 Cara Phillips 撰写，Paul Chen、Andy Schumeister、Brad Abrams 和 Theo Chu 参与贡献。

FAQ（常见问题）

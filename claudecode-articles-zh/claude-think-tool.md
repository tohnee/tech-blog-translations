---
title: "「think」工具：让 Claude 在复杂工具使用场景中停下来思考"
title_en: "The \"think\" tool: Enabling Claude to stop and think in complex tool use situations"
source: https://www.anthropic.com/engineering/claude-think-tool
published: 2025-03-20
crawled: 2026-09-11
translated: 2026-09-11
---

# 「think」工具：让 Claude 在复杂工具使用场景中停下来思考

> 原文：[The "think" tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool) · Anthropic Engineering Blog

- 扩展思考更新

  2025 年 12 月 15 日

  扩展思考（extended thinking）能力自最初发布以来已有改进，在大多数情况下我们建议使用该特性而不是专门的 think 工具。扩展思考能提供类似的收益——给 Claude 空间对复杂问题进行推理——且集成度和性能更好。实现细节请参阅我们的扩展思考文档。

在持续增强 Claude 解决复杂问题能力的过程中，我们发现了一种特别有效的做法：一个「think」工具，在复杂任务中为结构化思考开辟专门的空间。

这项简单而强大的技术——正如下文将要解释的，它不同于 Claude 新的「[扩展思考](https://www.anthropic.com/research/visible-extended-thinking)」能力（[扩展思考实现细节](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)见此）——显著提升了 Claude 的智能体工具使用能力，包括遵循政策、做出一致决策和处理多步问题，而且实现开销极小。

本文将探讨如何在不同应用中实现「think」工具，并基于经验证的基准结果为开发者提供实用指导。

### 什么是「think」工具？

借助「think」工具，我们让 Claude 在得出最终答案的过程中，能够加入一个额外的思考步骤——并配有专属的空间。

它听起来与扩展思考相似，但概念不同。扩展思考关注的是 Claude 开始生成回答*之前*做什么：有了扩展思考，Claude 会在采取行动之前深入考虑并反复打磨自己的计划。而「think」工具是让 Claude 在开始生成回答*之后*，增加一个停下来思考的步骤，审视自己是否已具备继续推进所需的全部信息。这在执行长链工具调用或与用户进行长篇多步对话时尤其有用。

因此，「think」工具更适合这样的场景：Claude 无法仅凭用户查询就获得撰写回答所需的全部信息，需要处理外部信息（例如工具调用结果中的信息）。Claude 用「think」工具进行的推理不如扩展思考全面，而是更聚焦于模型*新发现*的信息。

我们建议在较简单的工具使用场景中使用扩展思考，比如非顺序工具调用或直接的指令遵循。当你不需要 Claude 调用工具时——例如编码、数学、物理等用例——扩展思考同样有用。「think」工具则更适合 Claude 需要调用复杂工具、需要在长链工具调用中仔细分析工具输出、需要在有详细准则的政策密集型环境中导航，或需要做出步步相依、错误代价高昂的顺序决策的场景。

下面是一个采用来自 [τ-Bench](https://arxiv.org/abs/2406.12045) 的标准工具规范格式的示例实现：

```
{
  "name": "think",
  "description": "Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": {
        "type": "string",
        "description": "A thought to think about."
      }
    },
    "required": ["thought"]
  }
}
```

### τ-Bench 上的表现

我们用 τ-bench（tau-bench）评估「think」工具。这是一个综合性基准，测试模型在真实客服场景中使用工具的能力，而「think」工具是该评估标准环境的一部分。

τ-bench 评估 Claude 以下几方面的能力：

- 与模拟用户进行真实对话
- 一致地遵循复杂的客服智能体政策准则
- 使用多种工具访问和操作环境数据库

τ-bench 的主要评估指标是 pass^*k*，它衡量的是：对给定任务，*k* 次独立任务试验全部成功的概率，再对所有任务取平均。与其他 LLM 评估常用的 pass@*k* 指标（衡量 *k* 次试验中至少一次成功）不同，pass^*k* 评估的是一致性与可靠性——对客服应用而言这是关键品质，因为始终如一地遵循政策至关重要。

#### 表现分析

我们的评估比较了几种不同配置：

1. 基线（无「think」工具，无扩展思考模式）
2. 仅扩展思考模式
3. 仅「think」工具
4. 「think」工具 + 优化提示（针对 airline 领域）

结果显示，当 Claude 3.7 在基准的「airline」和「retail」两个客服领域中有效使用「think」工具时，表现大幅提升：

- **airline 领域**：「think」工具加优化提示在 pass^1 指标上达到 0.570，而基线仅 0.370——相对提升 54%；
- **retail 领域**：仅用「think」工具达到 0.812，基线为 0.783。

![折线图展示 Claude 3.7 Sonnet 在 Tau-Bench 评估「airline」领域上的表现](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fff91e5c84be59ae71306bcc60adba9affed86484-2200x1300.jpg&w=3840&q=75)

四种不同配置下 Claude 3.7 Sonnet 在 Tau-Bench 评估「airline」领域上的表现。

Claude 3.7 Sonnet 在 Tau-Bench 评估「Airline」领域上的表现

| 配置 | *k*=1 | *k*=2 | *k*=3 | *k*=4 | *k*=5 |
| --- | --- | --- | --- | --- | --- |
| "Think" + 提示 | 0.584 | 0.444 | 0.384 | 0.356 | 0.340 |
| "Think" | 0.404 | 0.254 | 0.186 | 0.140 | 0.100 |
| 扩展思考 | 0.412 | 0.290 | 0.232 | 0.192 | 0.160 |
| 基线 | 0.332 | 0.206 | 0.148 | 0.116 | 0.100 |

四种配置下的评估结果。分数为比例值。

airline 领域的最佳表现，来自「think」工具与一段优化提示的组合——该提示给出了分析客户请求时应当采用何种推理方式的示例。下面是这段优化提示的示例：

```
## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness 

Here are some examples of what to iterate over inside the think tool:
<think_tool_example_1>
User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID, reason
- Check cancellation rules:
  * Is it within 24h of booking?
  * If not, check ticket class and insurance
- Verify no segments flown or are in the past
- Plan: collect missing info, verify rules, get confirmation
</think_tool_example_1>

<think_tool_example_2>
User wants to book 3 tickets to NYC with 2 checked bags each
- Need user ID to check:
  * Membership tier for baggage allowance
  * Which payments methods exist in profile
- Baggage calculation:
  * Economy class × 3 passengers
  * If regular member: 1 free bag each → 3 extra bags = $150
  * If silver member: 2 free bags each → 0 extra bags = $0
  * If gold member: 3 free bags each → 0 extra bags = $0
- Payment rules to verify:
  * Max 1 travel certificate, 1 credit card, 3 gift cards
  * All payment methods must be in profile
  * Travel certificate remainder goes to waste
- Plan:
1. Get user ID
2. Verify membership level for bag fees
3. Check which payment methods in profile and if their combination is allowed
4. Calculate total: ticket price + any bag fees
5. Get explicit confirmation for booking
</think_tool_example_2>
```

特别有意思的是几种方法的对比。「think」工具配合优化提示取得了显著优于扩展思考模式的成绩（扩展思考的表现与未经提示的「think」工具相近）。仅用「think」工具（不加提示）优于基线，但仍不及优化后的做法。

「think」工具加优化提示的组合以明显优势拿下最强表现，原因很可能在于基准中 [airline 政策](https://github.com/sierra-research/tau-bench/blob/main/tau_bench/envs/airline/wiki.md)部分复杂度极高——模型从「如何思考」的示例中获益最多。

在 retail 领域，我们也测试了多种配置，以了解每种方法的具体影响。

![折线图展示 Claude 3.7 Sonnet 在 Tau-Bench 评估「retail」领域上的表现](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5819616b4cc109d30f1a7d47ec8a32a6b839637b-7638x4513.jpg&w=3840&q=75)

三种不同配置下 Claude 3.7 Sonnet 在 Tau-Bench 评估「retail」领域上的表现。

Claude 3.7 Sonnet 在 Tau-Bench 评估「Retail」领域上的表现

| 配置 | *k*=1 | *k*=2 | *k*=3 | *k*=4 | *k*=5 |
| --- | --- | --- | --- | --- | --- |
| "Think" + 无提示 | 0.812 | 0.735 | 0.685 | 0.650 | 0.626 |
| 扩展思考 | 0.770 | 0.681 | 0.623 | 0.581 | 0.548 |
| 基线 | 0.783 | 0.695 | 0.643 | 0.607 | 0.583 |

三种配置下的评估结果。分数为比例值。

即便没有任何附加提示，「think」工具也拿到了 0.812 的最高 pass^1 分数。[retail 政策](https://github.com/sierra-research/tau-bench/blob/main/tau_bench/envs/retail/wiki.md)相比 airline 领域明显更好驾驭，Claude 仅仅拥有一个思考空间就足以带来提升，无需进一步指导。

#### τ-Bench 分析的关键洞见

我们的细致分析揭示了几个有助于有效实现「think」工具的规律：

1. **在困难领域，提示至关重要**。仅仅提供「think」工具或许能带来一些提升，但为困难领域搭配优化提示会产生显著更好的结果。不过，较容易的领域可能仅靠拥有「think」就够了。
2. **多次试验间的一致性提升**。「think」带来的提升在 pass^k 直到 k=5 时都得以保持，说明该工具帮助 Claude 更有效地处理了边界情况和异常场景。

### SWE-Bench 上的表现

在评估 Claude 3.7 Sonnet 时，我们的 SWE-bench 配置中也加入了一个类似的「think」工具，为其取得 0.623 的最先进成绩做出了贡献。改编后的「think」工具定义如下：

```
{
  "name": "think",
  "description": "Use the tool to think about something. It will not obtain new information or make any changes to the repository, but just log the thought. Use it when complex reasoning or brainstorming is needed. For example, if you explore the repo and discover the source of a bug, call this tool to brainstorm several unique ways of fixing the bug, and assess which change(s) are likely to be simplest and most effective. Alternatively, if you receive some test results, call this tool to brainstorm ways to fix the failing tests.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": {
        "type": "string",
        "description": "Your thoughts."
      }
    },
    "required": ["thought"]
  }
}
```

我们的实验（带「think」工具 *n*=30 个样本，不带 *n*=144 个样本）表明，单独加入这个工具就能让表现平均提升 1.6%（Welch's *t* 检验：*t*(38.89) = 6.71，*p* < .001，*d* = 1.47）。

### 何时使用「think」工具

基于这些评估结果，我们确定了 Claude 从「think」工具中获益最多的具体场景：

1. **工具输出分析**。当 Claude 需要在行动前仔细处理先前工具调用的输出，并且可能需要在方案上回溯时；
2. **政策密集型环境**。当 Claude 需要遵循详细准则并核实合规性时；
3. **顺序决策**。当每一步行动都建立在先前步骤之上、错误代价高昂时（常见于多步领域）。

## 实现最佳实践

要让 Claude 上的「think」工具发挥最大效用，我们基于 τ-bench 实验推荐以下实现实践。

#### 1. 用领域特定示例做策略性提示

最有效的做法是就何时以及如何使用「think」工具给出清晰指令，例如 τ-bench airline 领域所用的那段提示。提供针对你具体用例定制的示例，能显著改善模型使用「think」工具的效果，包括：

- 推理过程应达到的详细程度；
- 如何把复杂指令分解为可执行的步骤；
- 处理常见场景的决策树；
- 如何检查是否已收集全部必要信息。

#### 2. 把复杂指导放进系统提示

我们发现，当指令较长和/或复杂时，把关于「think」工具的说明放进系统提示比放在工具描述本身更有效。这种方式提供了更宽泛的语境，帮助模型把思考过程更好地融入整体行为。

### 何时不该使用「think」工具

虽然「think」工具能带来可观改进，但它并不适用于所有工具使用场景，而且要以增加提示长度和输出 token 为代价。具体来说，我们发现「think」工具在以下用例中没有带来任何改进：

1. **非顺序工具调用**。如果 Claude 只需单个工具调用或多个并行调用即可完成任务，加入「think」不太可能带来改进。
2. **简单指令遵循**。当 Claude 需要遵守的约束不多、其默认行为已足够好时，额外的「think」不太可能带来收益。

### 上手指南

「think」工具是对你的 Claude 实现的一个直接补充，只需几步就能带来有意义的改进：

1. **在智能体工具使用场景中测试。** 从有挑战性的用例入手——那些 Claude 目前在政策合规或长工具调用链复杂推理上表现吃力的场景。
2. **添加工具定义。** 实现一个针对你的领域定制的「think」工具。它只需极少的代码，却能带来更有结构的推理。同时考虑在系统提示中加入关于何时以及如何使用该工具的说明，并附上与你的领域相关的示例。
3. **监控与打磨。** 观察 Claude 在实践中如何使用该工具，调整提示以鼓励更有效的思考模式。

最妙的是，加入这个工具在表现结果上几乎没有 downside。它不会改变外部行为——除非 Claude 决定使用它——也不会干扰你现有的工具或工作流。

### 结语

我们的研究表明，「think」工具能显著增强 Claude 3.7 Sonnet 在复杂任务上的表现——这类任务需要在长工具调用链中坚持政策并进行推理。「think」并非万能解法，但对正确的用例能带来可观收益，而且实现复杂度极低。

期待看到你用「think」工具与 Claude 一起构建更有能力、更可靠、更透明的 AI 系统。

1. 虽然 τ-Bench 结果聚焦于「think」工具对 Claude 3.7 Sonnet 的改进，但我们的实验表明 Claude 3.5 Sonnet（新）在与 3.7 Sonnet 相同的配置下同样能取得性能提升，说明这一改进也能推广到其他 Claude 模型。

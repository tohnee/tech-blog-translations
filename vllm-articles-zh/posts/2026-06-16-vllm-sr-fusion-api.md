---
title: "超越单一模型：vLLM Semantic Router 中的 Fusion"
title_en: "Beyond One Model: Fusion in vLLM Semantic Router"
source: https://vllm.ai/blog/2026-06-16-vllm-sr-fusion-api
crawled: 2026-09-12
translated: 2026-09-13
---

# 超越单一模型：vLLM Semantic Router 中的 Fusion

> 原文：[Beyond One Model: Fusion in vLLM Semantic Router](https://vllm.ai/blog/2026-06-16-vllm-sr-fusion-api) · vLLM 博客

作者：vLLM Semantic Router 团队

[#生态系统](https://vllm.ai/blog/tags/ecosystem)

单模型服务已不再是生产级 AI 系统的上限。现代应用往往拥有一个模型组合：快速模型、廉价模型、私有模型、推理模型、提供商 API 与本地 vLLM 后端。难点在于判断什么时候一个模型就够了，什么时候一个请求应该变成一个协同工作的模型系统。

Fusion 正是为这样的世界准备的 vLLM Semantic Router 新原语。它让一条路由可以运行一个模型面板（panel），请一个评审模型（judge）分析一致性与分歧缺口，然后综合出一个面向用户的答案，同时把策略、配置与追踪都留在路由器内部。

[OpenRouter 的 Fusion 发布](https://openrouter.ai/blog/announcements/fusion-beats-frontier/)是一个有用的信号，说明为什么这件事现在重要：模型面板正在成为一种实际的服务模式，而不只是离线研究想法。本文不是要克隆一个托管端点，而是要把 Fusion 变成一个可编程、可观测的 vLLM-SR 原语，服务于混合模型（Mixture-of-Models）。

![图 1：Fusion API 把模型多样性变成 vLLM-SR 路由原语：面板、评审、综合、追踪。](https://vllm.ai/blog-assets/figures/2026-06-16-vllm-sr-fusion-api/hero-v2.png)

图 1：Fusion API 把模型多样性变成 vLLM-SR 路由原语：面板、评审、综合、追踪。

## vLLM-SR 的核心主张

多年来，默认的服务问题很简单：

> 哪一个单一模型应该服务这个请求？

这个问题仍然有用，但已经不够了。生产系统现在需要能够做到以下几点的策略：

- 把简单请求路由到快速、低成本的模型
- 把困难请求升级到更强的专家模型
- 在切换模型会损害上下文时保持会话连续性
- 在模型执行之前应用隐私、安全与租户策略
- 在分歧有价值时扇出到多个模型
- 记录决策路径，让运维人员可以调试并改进它

这就是 vLLM-SR 的核心观点：模型质量不只是检查点的属性，也是围绕检查点的服务系统的属性。

[Mixture-of-Models on AMD GPUs](https://vllm.ai/2026/01/23/mom-on-amd-gpu.html) 的工作为 vLLM-SR 引入了这种以路由器为中心的视角：捕获信号、选择模型、协调异构后端并暴露路由。ReMoM 把同一方向延伸到多轮模型协作。Fusion 则为那些值得为多次独立前向付出延迟代价的请求，增加了一种更直接的面板-评审-综合模式。

## Fusion 增加了什么

Fusion 不是混合模型的全部。它只是路由器工具箱中的一个算法。

在 vLLM-SR 中，Fusion 是路由策略的一部分，而不是一个固定的全局端点：

1. **信号**描述请求：领域、复杂度、上下文、安全、反馈或其他证据。
2. **决策**决定这个请求应走普通路由还是 Fusion 路由。
3. 使用 `model: "vllm-sr/fusion"` 的 **Fusion 专属入口**把匹配范围收窄到支持 Fusion 的决策，因此请求仍会得到智能路由，而不会悄悄回退到单模型路由。
4. **面板模型**产生独立的候选答案。
5. **评审模型**提炼共识、矛盾、部分覆盖、独特洞察与盲区。
6. **综合调用**返回一个面向用户的答案。
7. **追踪**记录了哪些模型参与以及发生了什么。

最后一点很重要。托管的模型 slug 把这些大多隐藏起来。vLLM-SR 把面板、评审、策略与追踪都显式化，让运维人员可以决定 Fusion 用在哪里，而不是为每个请求都支付代价。

## 为什么 OpenRouter 的结果是有用的信号

OpenRouter 的发布值得讨论，因为它为同一个系统思路提供了公开的证明点。在 [DRACO](https://ar5iv.labs.arxiv.org/html/2602.11685)——一个围绕困难开放式任务构建的深度研究基准——上，OpenRouter 报告融合面板优于单个模型。

这些是 OpenRouter 的数字，不是 vLLM-SR 基准。我们把它视为外部证据，说明模型组合理应成为一等的服务原语：

| OpenRouter 报告的配置 | 分数 |
| --- | --- |
| Fusion：Fable 5 + GPT-5.5，由 Opus 4.8 综合 | 69.0% |
| Fusion：Opus 4.8 + GPT-5.5 + Gemini 3.1 Pro，由 Opus 4.8 综合 | 68.3% |
| Fusion：Opus 4.8 + Opus 4.8，由 Opus 4.8 综合 | 65.5% |
| 单模型 Claude Fable 5 | 65.3% |
| Fusion：Gemini 3 Flash + Kimi K2.6 + DeepSeek V4 Pro，由 Opus 4.8 综合 | 64.7% |
| 单模型 DeepSeek V4 Pro | 60.3% |
| 单模型 Kimi K2.6 | 53.7% |
| 单模型 Gemini 3 Flash | 43.1% |

对 vLLM-SR 而言最有趣的一行是预算面板。它表明独立的模型多样性可以弥补单个更便宜模型所缺失的质量。这正是路由器应当掌控的那类权衡。

## Fusion 在 vLLM-SR 中如何工作

实现围绕一条原则设计：Fusion 应该是一种路由算法，而不是全局模型设置。

全局运行时配置只注册哪些模型 slug 应触发直接 Fusion 执行。实际的面板、评审、错误策略、模板与运行时旋钮都在匹配到的路由决策上，因为这些选择与工作负载相关。研究类路由可能想要三个多样化的提供商。代码评审路由可能想要两个本地专家模型加一个更强的综合模型。隐私敏感路由可能把整个面板都放在自托管的 vLLM 后端上。

![图 2：在 vLLM-SR 中 Fusion 由信号驱动。auto 路由可以选择任何决策；直接 Fusion 路由只在 Fusion 决策中选择；请求插件覆盖的是执行，而不是全局策略。](https://vllm.ai/blog-assets/figures/2026-06-16-vllm-sr-fusion-api/fusion-entry-modes.png)

图 2：在 vLLM-SR 中 Fusion 由信号驱动。auto 路由可以选择任何决策；直接 Fusion 路由只在 Fusion 决策中选择；请求插件覆盖的是执行，而不是全局策略。

vLLM-SR 支持三种进入同一算法的方式：

| 入口路径 | vLLM-SR 如何处理 |
| --- | --- |
| `model: "vllm-sr/auto"` | 运行完整的 vLLM-SR 信号与决策策略。只有被选中的决策使用 `algorithm.type: fusion` 时才执行 Fusion；否则匹配到的非 Fusion 路由正常运行。`auto` 与 `MoM` 等旧别名仍受支持。 |
| `model: "vllm-sr/fusion"` | 运行相同的信号提取，但把决策匹配限制在支持 Fusion 的决策内。如果没有匹配到 Fusion 决策，除非请求提供了面板覆盖，vLLM-SR 会返回明确的 no-match 错误。 |
| `plugins: [{ "id": "fusion", ... }]` | 为单个请求覆盖评审、面板与选定的运行时旋钮。如果没有匹配到 Fusion 决策但提供了 `analysis_models`，vLLM-SR 会构建一个请求范围的 `fusion_direct` 执行。 |

一旦请求进入 Fusion looper，执行就是显式且可观测的：

1. **解析策略。** vLLM-SR 合并决策级 Fusion 配置、决策模型引用与请求级插件覆盖。
2. **保护路由器。** 已注册的 Fusion slug 不能被用作评审或面板模型，因此 Fusion 请求不能递归调用 Fusion。
3. **运行面板。** 分析模型并发执行，受 `max_concurrent` 约束。
4. **按策略处理失败。** `on_error: skip` 允许不完整面板；`on_error: fail` 让提供商失败立即显现。
5. **分析分歧。** 评审模型产出结构化分析，覆盖共识、矛盾、部分覆盖、独特洞察与盲区。
6. **综合或调用工具。** 最终的评审/综合调用返回一个助手响应；当客户端提供了工具时，返回 OpenAI 兼容的 `tool_calls` 响应。
7. **返回追踪与统计。** 响应可以包含 Fusion 追踪数据、中间面板输出、失败模型记录，以及跨面板、评审与综合调用的聚合 token 用量。

最后一项也是路由器价值的一部分。调用方收到 OpenAI 兼容响应，而运维人员仍能看到系统级视图：哪个决策被触发、哪些模型参与、运行了多少轮迭代、什么失败了，以及整个多模型执行消耗了多少 token 用量。

本次发布聚焦于服务原语：策略控制的面板、显式的阶段契约、提供商互操作与可追踪执行。质量问题值得单独进行更大规模的公开评测，在共同任务上比较 Fusion、单模型基线与前沿面板。

## Fusion 是一种决策，不是默认值

Fusion 有用，是因为有些请求能从独立的模型视角获益。它昂贵，是因为它增加了面板调用、评审分析、综合，以及通常更多的延迟。生产中的问题不只是"我们能不能融合模型？"，而是"Fusion 什么时候值得？"

这正是 vLLM-SR 发挥作用的地方。`model: "vllm-sr/auto"` 让路由器决定一个请求是否需要用 Fusion。简单提示可以留在快速的单模型路由上。困难研究、模糊分析、高风险综合，或分歧有价值的任务，可以匹配 Fusion 决策。同一层信号-决策还可以在路由器付出延迟代价之前编码领域、租户、隐私、成本、会话或安全策略。

`model: "vllm-sr/fusion"` 是想要仅 Fusion 路由的客户端的显式路径。它仍使用 vLLM-SR 的信号与决策，但把匹配收窄到支持 Fusion 的决策，从而不会悄悄回退到普通的单模型路由。请求级 Fusion 插件则是需要为单次调用提供面板的客户端的覆盖路径。

![图 3：Fusion 是一种决策，不是默认值。vLLM-SR 用策略来判断额外的延迟是否值得。](https://vllm.ai/blog-assets/figures/2026-06-16-vllm-sr-fusion-api/fusion-decision-not-default.png)

图 3：Fusion 是一种决策，不是默认值。vLLM-SR 用策略来判断额外的延迟是否值得。

这为运维人员提供了一个比单个托管 Fusion slug 更有用的控制平面：

| 生产问题 | vLLM-SR 控制 |
| --- | --- |
| 这个请求是否应该使用 Fusion？ | `vllm-sr/auto` 配合信号与决策 |
| 应该应用哪条 Fusion 策略？ | 带优先级与规则的 Fusion 决策 |
| 哪些模型应该参与？ | 每决策的评审与面板配置 |
| 延迟与失败应如何处理？ | `max_concurrent`、`on_error` 与可选的 token 策略 |
| 模型可以运行在哪里？ | 本地 vLLM 后端、私有端点与公共提供商 |
| 运维人员如何调试路由？ | 决策元数据、Fusion 追踪、失败记录与聚合用量 |

## 决策之后：可追踪的 Fusion

一旦请求进入 Fusion 决策，vLLM-SR 会运行一个带显式阶段边界的小型多模型工作流。面板阶段返回独立的候选答案。评审阶段把这些候选转化为结构化分析。最后阶段消费该分析，产出一个助手答案；当客户端提供工具时，产出一次工具调用。

阶段契约让系统保持可检查。如果某个面板模型失败，`on_error: skip` 可以在记录失败模型的同时用部分证据继续；`on_error: fail` 则可以立即停止。如果结构化评审输出无法解析，vLLM-SR 会保留原始分析并标记解析失败，而不是把它隐藏。最终响应可以包含 Fusion 追踪、中间面板输出、失败模型记录，以及整个运行的总 token 用量。

![图 4：Fusion 使用显式阶段契约，让面板输出、评审分析、综合与追踪统计保持可检查。](https://vllm.ai/blog-assets/figures/2026-06-16-vllm-sr-fusion-api/fusion-stage-contracts.png)

图 4：Fusion 使用显式阶段契约，让面板输出、评审分析、综合与追踪统计保持可检查。

这就是 Fusion 超越一个功能的方式：它成为一个可编程混合模型控制平面的一种实现。

## 用 vLLM-SR 试试看

### 让路由器决定

当你希望路由器在所有已配置决策中选择时，使用 `vllm-sr/auto`：

```
{
  "model": "vllm-sr/auto",
  "messages": [
    {
      "role": "user",
      "content": "What are the strongest arguments for and against carbon taxes?"
    }
  ]
}
```

如果匹配到的决策使用 `algorithm.type: fusion`，请求进入 Fusion。如果匹配到的是普通路由，vLLM-SR 走普通的选定模型路径。

### 显式请求 Fusion

当客户端明确想要仅 Fusion 路由时，使用 `vllm-sr/fusion`。这仍会运行信号提取，但只有支持 Fusion 的决策符合条件：

```
{
  "model": "vllm-sr/fusion",
  "messages": [
    {
      "role": "user",
      "content": "What are the strongest arguments for and against carbon taxes?"
    }
  ]
}
```

### 为单个请求覆盖面板

请求也可以自定义面板。这种覆盖是请求范围的；它不会把评审或面板默认值搬进全局配置：

```
{
  "model": "vllm-sr/fusion",
  "messages": [{ "role": "user", "content": "..." }],
  "plugins": [{
    "id": "fusion",
    "model": "google/gemini-3-flash-preview",
    "analysis_models": [
      "google/gemini-3-flash-preview",
      "moonshotai/kimi-k2.6",
      "deepseek/deepseek-v4-pro"
    ]
  }]
}
```

### 在智能体循环中使用 Fusion

对智能体应用，继续使用同样的 OpenAI 兼容工具循环即可。Fusion 只把工具调用权限交给最终评审。面板模型与结构化评审分析调用都以纯文本运行：它们能看到对话历史，包括先前的工具结果，但不会收到 `tools` 或 `tool_choice`。

```
{
  "model": "vllm-sr/fusion",
  "messages": [
    {
      "role": "user",
      "content": "Find the latest benchmark result and explain whether it changes our launch plan."
    }
  ],
  "tools": [{
    "type": "function",
    "function": {
      "name": "web_search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": { "type": "string" }
        },
        "required": ["query"]
      }
    }
  }],
  "tool_choice": "auto"
}
```

在该请求中，面板产生独立的文本分析，评审比较面板输出，只有最终评审可以直接回答或返回标准的 OpenAI 兼容 `tool_calls`。非流式客户端收到常规的 Chat Completions JSON 形状；流式客户端收到带 `finish_reason: "tool_calls"` 的工具调用 SSE 块。客户端附加的工具结果会在下一个 Fusion 轮次中被保留，因此多轮智能体循环继续工作。

### 配置入口与决策

全局配置只注册 API 入口别名：

```
global:
  router:
    auto_model_names:
      - vllm-sr/auto
      - auto
      - MoM
```

Fusion slug 注册在 looper 集成之下：

```
global:
  integrations:
    looper:
      fusion:
        model_names:
          - vllm-sr/fusion
```

每决策配置持有路由语义、评审、面板与运行时旋钮：

```
routing:
  decisions:
    - name: deep-research-fusion
      description: Use model diversity for research prompts with high synthesis risk.
      rules:
        operator: AND
        conditions:
          - type: domain
            name: research
          - type: complexity
            name: needs_reasoning:hard
      algorithm:
        type: fusion
        fusion:
          model: google/gemini-3-flash-preview
          analysis_models:
            - google/gemini-3-flash-preview
            - moonshotai/kimi-k2.6
            - deepseek/deepseek-v4-pro
          max_concurrent: 3
          on_error: skip
```

这种分离是刻意的。`global` 是与路由无关的运行时状态。评审、面板、可选 token 预算、并发与路由语义属于决策。

当需要与现有客户端兼容时，运维人员可以选择加入 OpenRouter 风格的别名：

```
global:
  integrations:
    looper:
      fusion:
        model_names:
          - vllm-sr/fusion
          - openrouter/fusion
```

默认情况下，vLLM-SR 只注册 `vllm-sr/fusion`。

## 接下来做什么

OpenRouter 的 DRACO 结果是一个强有力的信号，说明模型面板值得认真评估。我们的下一步是让这类评估在 vLLM-SR 与混合模型系统中可复现：

- 跑超出冒烟覆盖范围的更大规模公开评测
- 比较 Fusion、ReMoM、AutoMix、Router-R1 与单模型基线
- 研究预算面板对比前沿模型面板
- 暴露针对分歧、覆盖缺失与评审行为的追踪级诊断
- 让路由策略决定额外的延迟何时是合理的

方向是明确的。最佳答案不会总是来自最大的模型；越来越多的情况下，它会来自最好的模型系统，而 vLLM-SR 正是让这个系统可编程的地方。

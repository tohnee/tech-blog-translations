---
title: "用 Responses API 中的 WebSocket 加速智能体工作流"
title_en: "Speeding up agentic workflows with WebSockets in the Responses API"
source: https://openai.com/index/speeding-up-agentic-workflows-with-websockets/
crawled: 2026-09-13
category: engineering
translated: 2026-09-13
---

# 用 Responses API 中的 WebSocket 加速智能体工作流

> 原文：[Speeding up agentic workflows with WebSockets in the Responses API](https://openai.com/index/speeding-up-agentic-workflows-with-websockets/) · OpenAI 博客

当你让 Codex 修复一个 bug 时，它会扫描你的代码库寻找相关文件，阅读它们以建立上下文，做出修改，然后运行测试来验证修复是否生效。在底层，这意味着几十次来回的 Responses API 请求：确定模型的下一步动作，在你的电脑上运行一个工具，把工具输出发回 API，如此往复。

所有这些请求累积起来，就是用户在等待 Codex 完成复杂任务时所花费的数分钟时间。从延迟角度看，Codex 智能体循环（agent loop）的时间主要花在三个阶段：API 服务内部的工作（用于验证和处理请求）、模型推理，以及客户端时间（运行工具和构建模型上下文）。推理是指模型在 GPU 上运行以生成新 token 的阶段。过去，在 GPU 上运行 LLM 推理是智能体循环中最慢的部分，因此 API 服务的开销很容易被掩盖。随着推理越来越快，一次智能体运行（rollout）累积的 API 开销就变得显眼得多。

在这篇文章中，我们将解释我们如何把使用 API 的智能体循环端到端提速 40%，让用户能够体验到推理速度从每秒 65 token 跃升至接近 1,000 token 的飞跃。我们通过缓存、消除不必要的网络跳数、改进安全防护机制以更快标记问题，以及——最重要的一点——构建一种与 Responses API 建立持久连接的方式，而不是每次都要发起一系列同步 API 调用，来实现这一目标。

## 当 API 成为瓶颈

在 Responses API 中，GPT‑5、GPT‑5.2 等此前的旗舰模型以大约每秒 65 个 token（TPS）的速度运行。对于 GPT‑5.3‑Codex‑Spark——一个快速的编程模型——的发布，我们的目标是快一个数量级：超过 1,000 TPS，由针对 LLM 推理优化的专用 Cerebras 硬件实现。为了让用户能够体验到这个新模型的真正速度，我们必须降低 API 开销。

2025 年 11 月前后，我们在 Responses API 上发起了一场性能冲刺，针对单个请求的关键路径延迟落地了许多优化：

- 在内存中缓存渲染后的 token 和模型配置，跳过多轮响应中昂贵的分词（tokenization）和网络调用
- 通过消除对中间服务的调用（例如图像处理分辨率）并直接调用推理服务本身，降低网络跳数延迟
- 改进安全防护机制，让我们能更快地运行某些分类器来标记对话

借助这些改进，我们看到首 token 时间（TTFT）提升了接近 45%——它反映的是 API 的响应灵敏程度——但对于 GPT‑5.3‑Codex‑Spark 来说，这些改进仍然不够快。即便有了这些改进，相对于模型的速度，Responses API 的开销还是太大——也就是说，用户必须先等待运行我们 API 的 CPU，然后才能用上为模型服务的 GPU。

更深层次的问题是结构性的：我们把每个 Codex 请求都当作独立的请求来处理，在每次后续请求中都重新处理对话状态和其他可复用的上下文。即使对话的大部分内容没有变化，我们仍然为与完整历史绑定的重复工作付费。随着对话越来越长，这种重复处理也变得越来越昂贵。

## 构建持久连接

为了收紧这一设计，我们重新思考了传输协议：能否保持一条持久连接并缓存状态，而不是每次后续请求都通过 HTTP 建立新连接并发送完整的对话历史？我们的想法是只发送需要验证和处理的新信息，并在连接的生命周期内把可复用的状态缓存在内存中。这将减少冗余工作带来的开销。

我们考虑了几种不同的方案，包括 WebSocket 和 gRPC 双向流。我们最终选择了 WebSocket，因为作为一个简单的消息传输协议，用户无需更改他们的 Responses API 输入和输出结构。它对开发者友好，并且几乎不需要改动就能融入我们现有的架构。

第一个 WebSocket 原型改变了我们对 Responses API 延迟可能性的认知。Codex 团队一位对整个 API 栈有深厚专长的工程师，让一个 Codex 智能体跑了一整夜，拼出了一个原型。

在那个原型中，智能体运行被建模为单个长时间运行的 Response。借助 `asyncio` 特性，Responses API 会在采样出一个工具调用后在采样循环中异步阻塞，并向客户端发回一个 `response.done` 事件。客户端执行完工具调用后，会发回一个带有工具结果的 `response.append` 事件，这将解除采样循环的阻塞，让模型继续运行。

这里有一个类比：把本地工具调用当作托管工具调用（hosted tool call）来处理。当模型调用 web search 时，推理循环会阻塞，调用一个网络搜索服务，并把服务的响应放入模型上下文。在我们的设计中，我们做了同样的事情；只不过我们不是调用远程服务，而是通过 WebSocket 把模型的工具调用发回客户端。当客户端响应后，我们把客户端的工具调用结果放入上下文并继续采样。

这个设计极其有效，因为它消除了智能体运行中反复出现的 API 工作。推理前的工作只做一次，暂停等待工具执行，最后再做一次推理后的工作。

遗憾的是，这付出了 API 结构变得陌生且更复杂的代价。我们希望开发者能够直接接入 WebSocket 支持，而不必围绕一种新的交互模式重写他们的 API 集成。

## 保持 API 的熟悉感，同时让调用栈做到增量处理

在我们最终发布的版本中，我们切换回了一种熟悉的形态：继续使用相同请求体的 `response.create`，并用 `previous_response_id` 从上一个响应的状态延续对话上下文。

在一条 WebSocket 连接上，服务端维护一个连接作用域的、内存中的先前响应状态缓存。当后续的 `response.create` 带有 `previous_response_id` 时，我们会从缓存中取出该状态，而不是从头重建完整对话。

缓存的状态包括：

- 先前的 `response` 对象
- 先前的输入与输出条目
- 工具定义与命名空间
- 可复用的采样产物，例如先前渲染过的 token

通过复用内存中的先前响应状态，我们得以落地几项重大优化：

- 让我们的部分安全分类器和请求校验器只处理新增输入，而不是每次都处理完整历史
- 维护一个可追加的已渲染 token 的内存缓存，从而跳过不必要的分词
- 跨请求复用我们成功的模型解析/路由逻辑
- 让计费等非阻塞的推理后工作与后续请求重叠执行

我们的目标是尽可能接近那个最小开销的原型，同时保留开发者已经理解并围绕其构建的 API 形态。

## 树立速度的新标杆

经过两个月的 WebSocket 模式构建冲刺，我们向几家关键的编程智能体初创公司发布了 alpha 版本，让它们把这一模式集成到自己的基础设施中并安全地放量。Alpha 用户非常喜欢它，报告称其智能体工作流[最高提升 40%](https://x.com/aisdk/status/2026031263925039591)。鉴于 alpha 阶段的积极反馈，我们准备好正式发布了。

发布的效果立竿见影。Codex 很快把大部分 Responses API 流量切换到了 WebSocket 模式，延迟显著改善。对于 GPT‑5.3‑Codex‑Spark，我们达成了 1,000 TPS 的目标，并观察到高达 4,000 TPS 的突发流量，这表明 Responses API 能够在真实生产流量中跟上快得多的推理速度。影响也很快在开发者社区中显现：

- Codex 很快把大部分流量切换到了 WebSocket。运行 [GPT‑5.3‑Codex](https://developers.openai.com/api/docs/models/gpt-5.3-codex)、[GPT‑5.4](https://developers.openai.com/api/docs/models/gpt-5.4) 等最新模型的 Codex 用户都能从 WebSocket 模式的提速中受益。
- Vercel 将 WebSocket 模式集成进了 AI SDK，延迟降低了[最高 40%](https://x.com/aisdk/status/2026031263925039591)。
- Cline 的多文件工作流[快了 39%](https://x.com/cline/status/2026031848791630033)。
- Cursor 中的 OpenAI 模型最高提速 [30%](https://x.com/leerob/status/2026030244407468259)。

WebSocket 模式是 Responses API 自 2025 年 3 月发布以来最重要的新能力之一。通过 OpenAI API 团队与 Codex 团队的紧密协作，我们仅用几周时间就完成了从想法到生产运行。它不仅大幅改善了智能体运行的延迟，还回应了开发者群体日益增长的需求：随着模型推理不断提速，围绕推理的服务与系统也需要随之加速，才能把这些收益传递给用户。

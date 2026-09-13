---
title: "告别重分词漂移：通过 OpenAI 兼容 API 返回 token ID 对智能体 RL 至关重要"
title_en: "No More Retokenization Drift: Returning Token IDs via the OpenAI Compatible API Matters in Agent RL"
source: https://vllm.ai/blog/2025-10-22-agent-lightning
crawled: 2026-09-12
translated: 2026-09-13
---

# 告别重分词漂移：通过 OpenAI 兼容 API 返回 token ID 对智能体 RL 至关重要

> 原文：[No More Retokenization Drift: Returning Token IDs via the OpenAI Compatible API Matters in Agent RL](https://vllm.ai/blog/2025-10-22-agent-lightning) · vLLM 博客

作者：Agent Lightning（AGL）团队

**TL;DR。** 智能体（Agent）通常通过 OpenAI 兼容端点调用 LLM，而此类端点此前只返回基于字符串的输入和输出。在**智能体 RL** 中，这会因我们称之为**重分词漂移（Retokenization Drift）**的现象而导致训练与推理之间的不一致。该现象的成因是：token 在推理期间被解码为文本，随后又在训练期间被重新分词；即使对应的字符串完全相同，两组 token 也可能不一致。现在，你可以让 vLLM 的 OpenAI 兼容端点为提示和生成的响应都返回**精确的 token ID**。在 `/v1/chat/completions` 或 `/v1/completions` 请求中传入 `"return_token_ids": true`，你就会在常规文本输出之外额外收到 `prompt_token_ids` 和 `token_ids`。这让**智能体 RL** 变得稳健，因为漂移不会再发生。这与 Agent Lightning 完美契合：每个模型调用都被视为独立、无需拼接的更新样本；只要开启 `return_token_ids` 并记录返回的 ID 即可。

相关链接：

- 文档：[OpenAI 兼容服务器](https://docs.vllm.ai/en/v0.10.2/serving/openai_compatible_server.html#api-reference)
- 可搭配此功能使用的项目：Agent Lightning（[GitHub](https://github.com/microsoft/agent-lightning)、[文档](https://microsoft.github.io/agent-lightning/latest/)）

---

### 为什么 token ID 对智能体 RL 至关重要

LLM 的强化学习是在 token 序列上训练的，因此训练器需要行为策略采样得到的精确 token ID。在单轮场景下这本来很简单，因为调用 vLLM 底层的 `generate` 会直接返回 token。

在智能体场景下，大多数智能体框架调用 OpenAI 风格的 `chat.completions` / `completions`。相比原始的 `generate`，智能体更青睐这些 API，因为它们提供了智能体技术栈赖以构建的高层能力，例如*聊天模板与角色*（system/user/assistant）、*工具/函数调用*、结构化输出等。这些 API 历史上只返回**字符串**，这可能在智能体 RL 中引发问题。此前，存储的文本必须在训练时重新分词，但由于**重分词漂移**，这种做法在实践中不稳定、也不够精确。

你在 RL 中会看到的症状包括：不稳定的学习曲线（如下图所示），以及你以为在优化的数据与模型实际采样的数据之间难以调试的偏差。

![](https://vllm.ai/blog-assets/figures/agent-lightning/1_rewards.png)
红线与蓝线是在相同设置下得到的（即在训练中存储文本并重新分词），黄线则直接使用来自推理引擎的 token。

漂移可能由以下三个原因造成。

- **非唯一的 "HAVING"**。实践中这种情况屡见不鲜：一个词在生成时可能被产出为两个 token（例如 `H` + `AVING`），但稍后在训练中对文本重新分词时却得到不同的切分（例如 `HAV` + `ING`）。文本看起来一模一样，但 *ID 不同*，导致你的学习器针对错误的序列进行优化。

![](https://vllm.ai/blog-assets/figures/agent-lightning/2_having.png)
"HAVING" 这个词对应不同的 token。

- **工具调用序列化**。生成的工具调用文本（如 `<tool_call>{ "name": ... }</tool_call>`）会被工具调用解析器解析成聊天补全 API 所需的对象。之后，该对象又被渲染回 `<tool_call>{ "name": ... }</tool_call>` 并再次分词。工具调用的解析与重新渲染可能造成空白与格式上的变化。在某些情况下，JSON 错误甚至可能被工具调用解析器自动修正。这掩盖了模型真实的生成错误，使其无法在训练中被消除。
- **聊天模板差异**。不同框架使用的聊天模板可能略有不同。例如，同一个 LLaMA 模型可以配合多种聊天模板工作（[vLLM](https://github.com/vllm-project/vllm/tree/1d165d6d859d3c50720f0c07209db2363c4fd33b/examples) 中有多种，[HuggingFace](https://huggingface.co/meta-llama) 中有一种）。当推理和训练使用不同框架时，这种差异会产生不同的 token。

这三个因素导致了重分词漂移，进而引发训练不稳定——原因可能在于它们造成了推理与训练之间的不一致，继而导致**离策略（off-policy）的 RL 更新**。在策略（on-policy）对稳定的 RL 训练至关重要，细微的变化也可能造成重大影响。由重分词漂移造成的离策略效应甚至不是 token 级别的，因此无法通过 token 级的重要性采样来纠正。

另一种做法是像单轮场景那样保存模型生成的 token ID。这要求智能体必须与推理引擎在 token 层面通信。然而，大多数智能体——尤其是用 LangChain 这类框架构建的——依赖 OpenAI 兼容 API，无法自行完成分词或解码。关于这一部分的更多讨论见[这里](https://microsoft.github.io/agent-lightning/stable/deep-dive/serving-llm/#token-ids-and-why-they-matter)。

---

### 解决方案与新特性

更好的方案是使用**直接返回 token ID 的 OpenAI 兼容 API**。Agent Lightning 团队与 vLLM 团队合作，把这一特性直接加入 [vLLM 核心](https://github.com/vllm-project/vllm/pull/22587)。从 vLLM v0.10.2 开始，OpenAI 兼容 API 包含一个 [`return_token_ids` 参数](https://docs.vllm.ai/en/v0.10.2/serving/openai_compatible_server.html#api-reference)，允许在请求聊天消息的同时请求 token ID。在请求中把它设为 `true` 时，响应会额外包含两个字段：

- `prompt_token_ids`：输入的 token ID（经过聊天模板处理之后的），以及
- `token_ids`：为补全（completion）生成的 token ID，通过 `completion.choices` 传递。

响应中的其他内容保持 OpenAI 兼容，因此现有客户端不受影响、继续可用。

---

### Agent Lightning（v0.2）简介

在 [Agent Lightning](https://github.com/microsoft/agent-lightning)（简称 AGL）的初始版本（v0.1）中，我们提供了一个灵活的训练框架，可以用 RL 训练任何智能体。它有以下几个核心特性：

- 与现有智能体无缝集成，几乎零代码改动！
- 可以使用任何智能体框架构建（LangChain、OpenAI Agent SDK、Microsoft Agent Framework 等）；甚至可以不使用智能体框架（纯 Python 程序）。
- 对 LLM 的输入没有任何约束，支持灵活的编排，例如摘要、多智能体协作及其他复杂工作流。

Agent Lightning 首次发布时，我们实现了一个[带插桩的 vLLM 服务器](https://github.com/microsoft/agent-lightning/blob/v0.1/agentlightning/instrumentation/vllm.py)，通过 monkey-patch vLLM 的 OpenAI 服务器来返回 token ID。现在，AGL 会自动为每个请求添加 `return_token_ids`，让引擎在响应中包含 token ID。随后，借助内置于 AGL 的[追踪（tracing）](https://microsoft.github.io/agent-lightning/latest/tutorials/traces/)能力，我们自动收集训练器一侧所需的数据，其中包括这些 token ID。

### 面向智能体优化的中间件

从更精确的数据收集这一视角出发，我们在 v0.2 中让 AGL 在智能体优化中的角色更加清晰。从概念上讲，Agent Lightning（即 AGL）为智能体优化（尤其是智能体 RL）引入了一个可持续的中间件层与标准化的数据协议。

![](https://vllm.ai/blog-assets/figures/agent-lightning/3_agl.png)
Agent Lightning 概念总览。

Agent Lightning 由一组模块化、可互操作的组件构成，共同实现可扩展、高效的智能体 RL。每个组件各司其职，通过标准化的数据协议与定义清晰的接口进行通信。

- **Agent Runner** — 负责执行智能体以完成分配的任务。它接收任务、将其委派给智能体执行、收集结果与中间数据，并将这些数据上报给数据存储。Agent Runner 与 LLM 侧分开运行，因此可以部署在不同的资源上（例如 CPU），并支持水平扩展以支撑大量并发的智能体实例。
- **算法（模型训练器，Model Trainer）** — 承载用于推理和训练的大语言模型（LLM）。该组件统筹整个 RL 循环，包括*任务采样*、*rollout 管理*以及基于收集到的经验数据进行*模型更新*。它通常运行在 GPU 资源上，并通过共享的数据协议与 Agent Runner 异步交互。
- [**数据存储（Data Store）**](https://microsoft.github.io/agent-lightning/latest/how-to/write-first-algorithm/#the-central-hub-the-lightningstore) — 作为中央仓库，管理智能体 RL 生态内所有的数据交换与存储。它提供标准化接口与统一的数据模式（schema），确保异构组件之间的互操作性。通过这一设计，算法侧与 Agent Runner 可以*间接但有效地*通信，实现灵活且可扩展的协作。例如，借助标准化的 [`rollouts`](https://microsoft.github.io/agent-lightning/latest/how-to/train-first-agent/#rollout)，算法侧可以异步地把任务委派给 Agent Runner，后者执行任务并通过 [`spans`](https://microsoft.github.io/agent-lightning/latest/how-to/train-first-agent/#span) 数据结构回报执行轨迹。

![](https://vllm.ai/blog-assets/figures/agent-lightning/4_tasks-spans-loop.svg)
Agent Lightning 中的训练循环。

在这一以数据存储为中心的设计理念下，所有智能体训练迭代都被抽象为两步：第一步是收集智能体运行数据（AGL 中的 spans）并存入数据存储；第二步是从存储中取出所需数据，发送给算法侧进行训练。

这一抽象视角带来诸多优势。首先，它提供了更大的算法灵活性：数据收集可以依赖[各种 tracer](https://microsoft.github.io/agent-lightning/latest/tutorials/traces/) 或[发送自定义消息](https://microsoft.github.io/agent-lightning/latest/tutorials/write-agents/#emitting-rewards-messages-and-more)，让定义不同的奖励或捕获任意中间变量都变得简单直接。在算法侧，所需数据可以通过 [query](https://microsoft.github.io/agent-lightning/latest/deep-dive/birds-eye-view/?h=query#putting-it-all-together-a-reinforcement-learning-example-verl) spans 获取，自定义的[适配器（adapter）](https://microsoft.github.io/agent-lightning/latest/deep-dive/birds-eye-view/#adapter)支持自由的数据变换。

这一设计还支持[算法定制](https://microsoft.github.io/agent-lightning/latest/algorithm-zoo/verl/#customization)，例如信用分配（credit assignment）、用部分数据训练辅助模型、通过数据调整改进训练等等。此外，在这一框架内，我们还可以扩展到更多类型的算法，例如[自动提示词调优（APO）](https://microsoft.github.io/agent-lightning/latest/algorithm-zoo/apo/)、[筛选高奖励数据并用 Unsloth 进行训练](https://microsoft.github.io/agent-lightning/latest/how-to/unsloth-sft/)。

这一设计的第二大优势在于，它能够通过模块化分离降低整体系统复杂度，同时让不同组件使用不同的资源与优化策略。智能体 RL 训练系统天然复杂，因为它依赖动态的、环境驱动的交互来实现模型从经验数据中的持续学习。一个典型的智能体 RL 技术栈由几个关键组件构成：智能体框架（如 LangChain、MCP）、LLM 推理引擎（如 vLLM）和训练框架（如 Megatron-LM）。如果没有解耦架构，这些组件的独立性与异构性会带来可观的整体复杂度。相比之下，解耦设计让系统能够容纳多样化的资源需求：例如，智能体侧可能需要更强的 CPU 能力，而 LLM 推理与训练通常高度依赖 GPU。这种模块化结构也便于各组件独立水平扩展，同时提升效率与可维护性。

更多资料：

- [完整文档](https://microsoft.github.io/agent-lightning/latest/)
- [全景概览（Birds Eye View）](https://microsoft.github.io/agent-lightning/latest/deep-dive/birds-eye-view/)
- [使用 verl 训练 SQL 智能体（含多智能体编排）](https://microsoft.github.io/agent-lightning/latest/how-to/train-sql-agent/)
- [使用自动提示词优化训练房间选择智能体](https://microsoft.github.io/agent-lightning/latest/how-to/train-first-agent/)，其中的提示词编排由 [POML](https://github.com/microsoft/poml/) 驱动。
- [使用 Unsloth 训练数学智能体（基于 OpenAI Agents SDK 与 MCP 构建）](https://microsoft.github.io/agent-lightning/latest/how-to/unsloth-sft/)

祝训练愉快！⚡

### 致谢

我们诚挚感谢 vLLM 的维护者们，包括 [Kaichao You](https://github.com/youkaichao)、[Nick Hill](https://github.com/njhill)、[Aaron Pham](https://github.com/aarnphm)、[Cyrus Leung](https://github.com/DarkLight1337)、[Robert Shaw](https://github.com/robertgshaw2-redhat) 和 [Simon Mo](https://github.com/simon-mo)。没有他们的支持与协作，这次集成不可能完成。

Agent Lightning 是微软研究院（Microsoft Research）的开源项目。我们衷心感谢 MSR 对这一开源探索的支持。[Yuge Zhang](https://github.com/ultmaster) 是这项工作的主要贡献者。

---
title: "我们为什么打造了 Responses API"
title_en: "Why we built the Responses API"
source: https://developers.openai.com/blog/responses-api/
crawled: 2026-09-14
translated: 2026-09-14
---

# 我们为什么打造了 Responses API

> 原文：[Why we built the Responses API](https://developers.openai.com/blog/responses-api/) · OpenAI 开发者博客

随着 GPT-5 面世，我们想就它的最佳集成方式、[Responses API](https://platform.openai.com/docs/api-reference/responses)，以及为什么 Responses 是为推理模型与智能体未来量身打造的，提供更多背景信息。

每一代 OpenAI API 都围绕同一个问题构建：*开发者与模型对话的最简单、最强大的方式是什么？*

我们的 API 设计始终以模型自身的运作方式为指引。最早的 `/v1/completions` 端点简单，但也有局限：你给模型一个提示（prompt），它只会顺着你的思路补全。借助少样本提示（few-shot prompting）等技术，开发者可以尝试引导模型输出 JSON、回答问题等，但这些模型的能力远不及我们今天习以为常的水平。

随后是 RLHF、ChatGPT 与后训练（post-training）时代的到来。模型不再只是补全你写到一半的文字——它们开始像对话伙伴一样*回应*你。为了跟上这一变化，我们打造了 `/v1/chat/completions`（[广为人知的是，它是在一个周末之内完成的](https://x.com/athyuttamre/status/1899541474297180664)）。通过引入 `system`、`user`、`assistant` 等角色，我们提供了脚手架，让开发者能够快速构建带有自定义指令和上下文的聊天界面。

我们的模型不断进步。很快，它们开始能看、能听、能说。2023 年底的函数调用（function calling）后来成为我们最受欢迎的功能之一。大约在同一时间，我们以测试版形式推出了 Assistants API：这是我们对完全智能体化接口的首次尝试，带有代码解释器、文件搜索等托管工具。一些开发者喜欢它，但由于其 API 设计相对 Chat Completions 而言局限性强、难以采用，它始终未能大规模普及。

到 2024 年底，我们显然需要一次统一：一个像 Chat Completions 一样平易近人、像 Assistants 一样强大，同时又为多模态与推理模型量身定制的方案。于是 `/v1/responses` 登场了。

## `/v1/responses` 是一个智能体循环

Chat Completions 给你的是一个简单的轮次式聊天接口，而 Responses 给你的是一个用于推理与行动的结构化循环。可以把它想象成与一位侦探共事：你提供证据，侦探展开调查，可能会咨询专家（工具），最后汇报结论。侦探会在各个步骤之间保留自己的私人笔记（推理状态），但绝不会把它们交给委托人。

这正是推理模型大放异彩之处：Responses 会在这些轮次之间保留模型的*推理状态*。在 Chat Completions 中，推理在两次调用之间会被丢弃，就像侦探每次离开房间就忘掉所有线索。Responses 则让笔记本始终摊开——逐步展开的思考过程能够真正延续到下一轮。这不仅体现在基准测试上（TAUBench 提升 5%），也体现在更高效的缓存利用率与延迟上。

Responses 还能输出多个输出项：不仅有模型*说了什么*，还有它*做了什么*。你会拿到凭证——工具调用、结构化输出、中间步骤。这就像既拿到写好的文章，又拿到草稿纸上的演算过程。这对调试、审计以及构建更丰富的 UI 都很有用。

```
{
  "message": {
    "role": "assistant",
    "content": "I'm going to use the get_weather tool to find the weather.",
    "tool_calls": [
      {
        "id": "call_88O3ElkW2RrSdRTNeeP1PZkm",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"location\":\"New York, NY\",\"unit\":\"f\"}"
        }
      }
    ],
    "refusal": null,
    "annotations": []
  }
}
```

```
  {
    "id": "rs_6888f6d0606c819aa8205ecee386963f0e683233d39188e7",
    "type": "reasoning",
    "summary": [
      {
        "type": "summary_text",
        "text": "**Determining weather response**\n\nI need to answer the user's question about the weather in San Francisco. ...."
      },
  },
  {
    "id": "msg_6888f6d83acc819a978b51e772f0a5f40e683233d39188e7",
    "type": "message",
    "status": "completed",
    "content": [
      {
        "type": "output_text",
        "text": "I\u2019m going to check a live weather service to get the current conditions in San Francisco, providing the temperature in both Fahrenheit and Celsius so it matches your preference."
      }
    ],
    "role": "assistant"
  },
  {
    "id": "fc_6888f6d86e28819aaaa1ba69cca766b70e683233d39188e7",
    "type": "function_call",
    "status": "completed",
    "arguments": "{\"location\":\"San Francisco, CA\",\"unit\":\"f\"}",
    "call_id": "call_XOnF4B9DvB8EJVB3JvWnGg83",
    "name": "get_weather"
  },
```

### 借助托管工具向技术栈上层迈进

在函数调用的早期，我们注意到一个关键模式：开发者既用模型调用 API，也用它检索文档库以引入外部数据源——也就是如今所说的 RAG（检索增强生成）。但对于刚起步的开发者来说，从零构建一条检索流水线是一项艰巨且昂贵的工程。在 Assistants 中，我们推出了首批*托管*（hosted）工具：`file_search` 和 `code_interpreter`，让模型能够执行 RAG 并编写代码来解决你提出的问题。在 Responses 中，我们走得更远，加入了网页搜索（web search）、图像生成（image gen）和 MCP。而且由于工具执行通过代码解释器或 MCP 等托管工具在服务端完成，你不必让每次调用都在自己的后端之间来回折返，从而获得更好的延迟和更低的往返成本。

### 安全地保留推理

那么，为什么要费这么大的周折来隐藏模型的原始思维链（CoT）？直接暴露 CoT、让客户端像对待其他模型输出一样对待它们，不是更简单吗？简短的回答是：暴露原始 CoT 带来诸多风险：例如幻觉、不会出现在最终回复中的有害内容，以及对 OpenAI 而言会打开竞争风险的大门。

去年年底我们发布 o1-preview 时，我们的首席科学家 Jakub Pachocki 在我们的博客中写道：

> 我们相信，隐藏的思维链为监控模型提供了独特的机会。假设它是忠实的且清晰可读，隐藏的思维链让我们得以「读取」模型的内心，理解它的思考过程。例如，未来我们可能希望监控思维链中是否存在操纵用户的迹象。然而，要做到这一点，模型必须能够以未加修饰的本来形式自由表达想法，因此我们不能在思维链上训练任何政策合规性或用户偏好。我们也不希望让未对齐的思维链直接暴露给用户。

Responses 通过以下方式解决这一问题：

- 在内部保留推理，经加密并对客户端隐藏。
- 通过 `previous_response_id` 或推理项（reasoning items）实现安全续接，而不暴露原始 CoT。

## 为什么 `/v1/responses` 是最佳的构建方式

我们将 Responses 设计为**有状态、多模态且高效**。

- **智能体工具调用（agentic tool-use）：** Responses API 让你可以借助 File Search、Image Gen、Code Interpreter 和 MCP 等工具，轻松增强智能体工作流。
- **默认有状态。** 对话与工具状态会被自动跟踪。这让推理与多轮工作流变得极为简单。通过 Responses 接入的 GPT-5 在 TAUBench 上的得分比 Chat Completions 高出 5%，而这完全得益于推理状态的保留。
- **从底层起就是多模态。** 文本、图像、音频、函数调用——全都是一等公民。我们没有把各种模态硬塞进一个文本 API，而是从第一天起就把房子设计出足够多的房间。
- **更低成本，更优性能。** 内部基准测试显示，与 Chat Completions 相比缓存利用率提升 40–80%。这意味着更低的延迟与更低的成本。
- **更好的设计：** 我们从 Chat Completions 与 Assistants API 中吸取了大量经验，并在 Responses API 与 SDK 中做了许多提升使用体验的小改进，包括：

  - 语义化流式事件（semantic streaming events）。
  - 内部标记的多态（internally-tagged polymorphism）。
  - SDK 中的 `output_text` 辅助方法（再也不用写 `choices.[0].message.content`）。
  - 多模态与推理参数的更清晰组织。

## 那 Chat Completions 呢？

Chat Completions 不会消失。如果它适合你，请继续使用。但如果你想要能够延续的推理、原生般自然的多模态交互，以及无需胶带拼凑的智能体循环——Responses 就是前进的方向。

## 展望未来

正如 Chat Completions 取代了 Completions，我们预计 Responses 将成为开发者基于 OpenAI 模型构建应用的默认方式。需要简单时它足够简单，需要强大时它足够强大，并且足够灵活，能够应对下一个范式抛给我们的任何挑战。

这就是我们在未来数年将持续构建其上的 API。

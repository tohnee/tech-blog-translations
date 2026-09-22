---
title: "Grok 4.1 Fast 与 Agent Tools API"
title_en: "Grok 4.1 Fast and Agent Tools API"
date: 2025-11-20
source: https://x.ai/news/grok-4-1-fast
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 4.1 Fast 与 Agent Tools API

> 原文：[Grok 4.1 Fast and Agent Tools API](https://x.ai/news/grok-4-1-fast) · xAI

2025 年 11 月 19 日

把下一代工具调用智能体带入 xAI API

---

预订智能体

你是一名酒店客服智能体，可以帮助客人创建和管理预订以及处理一般咨询。

可用工具

client-tool按邮箱查找客人

server-code获取预订详情

web-search查找可用房间

client-tool修改预订

你好，我想把当前的预订升级为行政套房。

好的，请稍等，我先找到你的预订……

正在查找你的账户……

正在搜索可用房间……

正在将预订升级为行政套房……

好了，全部完成。你已订入行政套房——祝入住愉快！

谢谢！

行动计划

1

确认客人身份

2

检查可用性

3

升级预订

client-tool按邮箱查找客人

输入

Email:john.doe@example.com

输出

User ID:1234567890

server-code获取预订详情

输入

User ID:1234567890

Date:01 Dec - 05 Dec, 2025

输出

Booking ID:BX-23929

web-search查找可用房间

输入

Date:01 Dec - 05 Dec, 2025

Room type:Executive Suite

输出

Room ID:2918482

client-tool修改预订

输入

Booking ID:BX-23929

Room ID:2918482

今天，我们很高兴为 xAI API 推出两项强大的新成员：

- **Grok 4.1 Fast**：我们最好的工具调用模型，拥有 2M 上下文窗口。它能快速而准确地推理并完成智能体（agentic）任务，在客户支持和金融等复杂真实世界用例中表现出色。
- **Agent Tools API**：让智能体可以访问实时 X 数据、网页搜索、远程代码执行等能力。

Grok 4.1 Fast 与 Agent Tools API 配合使用，让开发者能够构建专注于工具调用和智能体搜索的生产级智能体。

---

## [为真实世界而训练](#trained-for-the-real-world)

我们专为真实世界的企业用例构建了 Grok 4.1 Fast。

通过在模拟环境中进行 RL 训练，Grok 4.1 Fast 接触了覆盖数十个领域的多种工具。这种多样化的训练使 Grok 4.1 Fast 在 τ²-bench Telecom 上表现格外出色——这是一个在真实世界客服场景中评测智能体工具使用能力的严苛基准。

### τ²-bench Telecom

分数(%)

100%

总成本($)

$105

* 由 [Artificial Analysis](https://artificialanalysis.ai/evaluations/tau2-bench) 验证的独立评测

## [最先进的工具调用](#state-of-the-art-tool-calling)

随着开发者构建越来越强的自主智能体——它们需要进行长时程规划并独立运作，模型必须在提供智能的同时不牺牲速度和成本。

Grok 4.1 Fast 就是我们的答案：一个把前沿工具调用性能与极速推理、高性价比结合起来的模型。

### Berkeley Function Calling v4 基准

总体准确率(%)

72%

总成本($)

$400

*Gemini 3 Pro 的分数为独立评测方提供的估计值，等待官方结果。

智能体模型的一个常见难题是性能随上下文长度增加而下降。我们使用长时程强化学习训练 Grok 4.1 Fast，并特别强调多轮场景，确保其在其完整的 200 万 token 上下文窗口内保持稳定的性能。

### 多轮准确率

### 多轮长上下文

Grok 4.1 Fast

Grok 4 Fast

Grok 4

# [Agent Tools API](#agent-tools-api)

我们同时推出 Agent Tools API——一套强大的服务端工具，让 Grok 4.1 Fast 能够作为完全自主的智能体运作。

人们对 Tesla Robotaxi 的反应如何？

智能体

Grok 4.1 Fast

## Robotaxi 反应

对亚利桑那州获批和快速扩张表现出强烈兴奋，许多人称赞它比其他网约车服务更便宜、更平顺。𝕏 用户和公众整体呈积极态势。

正在浏览网页查找 Robotaxi 新闻

正在阅读 X 帖子以评估社区反响

正在用 Python 构建情绪图表

只需几行代码，开发者就能让 Grok 浏览网页、搜索 X 帖子、执行代码、检索上传的文档等。

  

python

```
import os
from xai_sdk import Client
from xai_sdk.tools import code_execution, web_search, x_search, collections_search, mcp

client = Client(api_key=os.getenv("XAI_API_KEY"))
chat = client.chat.create(
    model="grok-4-1-fast-reasoning",
    tools=[
        web_search(),
        x_search(),
        code_execution(),
        collections_search(collection_ids=["..."]),
        mcp(server_url="..."),
    ],
)
```

  

这些工具完全运行在 xAI 的基础设施上，开发者不再需要管理 API 密钥、速率限制、沙箱或检索管道。Grok 会决定何时以及如何使用它们，常常在多轮中并行调用多个工具，直到获得交付最终答案所需的一切。

## [功能齐全的工具集](#a-full-featured-toolset)

Agent Tools API 是一套多功能的工具集，可以显著扩展我们 Grok 基础模型的能力。主要功能包括：

[### 搜索工具](https://docs.x.ai/docs/guides/tools/search-tools)

利用实时 X 和互联网搜索，快速、全面地洞察时事与趋势。

[### 文件搜索](https://docs.x.ai/docs/guides/tools/collections-search-tool)

智能搜索并检索与你上传文件相关的文档，附带引用。

[### 代码执行](https://docs.x.ai/docs/guides/tools/code-execution-tool)

在安全沙箱中执行 Python 代码，用于分析数据和运行模拟。

[### MCP 工具](https://docs.x.ai/docs/guides/tools/remote-mcp-tools)

无缝连接外部 MCP 服务器，访问强大的自定义第三方工具。

## [深度研究的最佳智能体](#the-best-agent-for-deep-research)

实时信息检索和深度研究是 Grok 4.1 Fast 的核心强项。凭借与 X 生态的原生集成和强大的网页浏览能力，由 xAI API 驱动的搜索智能体在严苛的智能体搜索基准上处于最先进水平。

|  | Research-Eval Reka | | FRAMES | | X Browse* | |
| --- | --- | --- | --- | --- | --- | --- |
| 分数 | 平均成本 | 分数 | 平均成本 | 分数 | 平均成本 |
|  | | | | | | |
| Grok 4.1 Fast Agent Tools API | 63.9 | $0.046 | 87.6 | $0.048 | 56.3 | $0.091 |
| GPT-5 | 45.5 | $0.107 | 86.0 | $0.058 | 24.2 | $0.198 |
| Claude Sonnet 4.5 | 41.2 | $0.065 | 85.0 | $0.078 | 14.6 | $0.126 |
| Gemini 3 Pro | 55.9 | - | 90.9 | - | 26.5 | - |

*X Browse 是一个内部基准，评测智能体在 X 上进行多跳搜索与浏览的能力。

Grok 4.1 Fast 树立了事实性的新标准：在 FActScore 评测中，其幻觉率较 Grok 4 Fast 减半，同时性能仍与 Grok 4 相当。

## [开始构建](#start-building)

我们在 API 上发布两个 Grok 4.1 Fast 变体：

- `grok-4-1-fast-reasoning` 追求最强智能
- `grok-4-1-fast-non-reasoning` 追求即时响应

在**未来两周**内，我们的模型和工具将在指定平台免费提供：

- 我们与 OpenRouter 合作，免费提供 Grok 4.1 Fast 系列模型。
- 我们通过 xAI Agent Tools API 完全免费提供所有智能体工具。

### 输入定价

输入 token

$0.20 / 1M tokens

缓存输入 token

$0.05 / 1M tokens

### 输出定价

输出 token

$0.5 / 1M tokens

工具调用

低至 $5 / 1000 次成功调用

* xAI Agent Tools API 免费至 12 月 3 日

在 OpenRouter 上免费试用

Grok 4.1 Fast 将在 12 月 3 日前于 OpenRouter 独家免费提供

[![OpenRouter 徽标](/_next/static/media/open-router.cddd10e4.svg)

立即试用

OpenRouter](https://openrouter.ai/x-ai/grok-4.1-fast)

[### 创建 xAI API 密钥](https://console.x.ai/team/default/api-keys)

今天就通过 xAI API 开始用 Grok 4.1 Fast 构建。

[### API 文档](https://docs.x.ai/docs/guides/tools/overview)

查看我们关于如何使用智能体工具的文档。

我们迫不及待想看到你构建的作品。请在 X 上与社区分享你的创作和反馈！

在以下平台试用 Grok

[网页](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

产品

[Grok](/grok)

[𝕏](https://x.com)

[API](/api)

[Grok Enterprise](/grok/business)

[Grokipedia](https://grokipedia.com)

公司

[公司简介](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[文档](https://docs.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[安全性](/safety)

[法律](/legal)

[状态](https://status.x.ai)

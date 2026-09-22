---
title: "Grok Collections API"
title_en: "Grok Collections API"
date: 2026-01-01
source: https://x.ai/news/grok-collections-api
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Collections API

> 原文：[Grok Collections API](https://x.ai/news/grok-collections-api) · xAI

2025 年 12 月 22 日

直接内建于我们 API 的最先进 RAG 系统。

收听这篇博文

收听这篇博文

今天，我们很高兴地宣布 Collections API。借助 Collections，你可以上传并检索整个数据集。
从 PDF、Excel 表格到整个代码库，你可以把文件上传到一个支持精确而快速检索的知识库中。
这让开发者无需为管理索引和检索基础设施而头疼，即可构建 RAG 应用。

为了帮你起步，第一周的文件索引和存储免费*，检索按每 1,000 次搜索 2.50 美元的统一价格计费。

## [索引](#indexing)

- **强大的文档理解**：我们使用 OCR 和版面感知解析来提取文本，同时保留结构，例如 PDF 的版式、Excel 表格的层级或代码的语法。
- **智能文件管理**：轻松上传、更新和下载文件。当文件发生变化时，我们的系统会高效地重新索引，确保你的 collection 永不过期。
- **广泛的格式支持**：Collections 支持多种文件类型。[（查看完整列表）](https://docs.x.ai/docs/key-information/collections#supported-mime-types)

## [检索](#retrieval)

选择最适合你用例的检索方式：

- **语义检索**：基于查询背后的含义和意图进行搜索。
- **关键词检索**：用于精确的词条匹配。
- **混合检索**：为获得最高准确率，可结合关键词与语义检索。我们既支持专用重排序（reranker）模型，也支持倒数排序融合（reciprocal rank fusion）。

What is our financial forecast for Q1 2026?

Financial_plan_2026.txt

Our company's annual financial projections indicate a robust growth trajectory for the upcoming fiscal year, with expected revenue increases driven by expanded market share in emerging sectors. Analysts predict a 15% rise in Q1 2026, bolstered by strategic investments in technology and supply chain optimization. Key metrics such as EBITDA and net profit margins are forecasted to improve.

语义关键词混合

## [基准测试结果](#benchmark-results)

我们的 Collections API 交付了最先进的检索性能，在金融、法律和编码领域的真实 RAG 任务上比肩或超越领先模型。

这些领域尤其具有挑战性，因为文档冗长而密集。为避免幻觉并交付可靠的答案，模型必须检索到确切的段落并对其进行准确推理。

### 准确率*

（越高越好）

| 任务 | xAI Grok 4.1 Fast | Google Gemini Pro 3 | OpenAI GPT 5.1 |
| --- | --- | --- | --- |
| 金融 表格与数值类问题 | 93.0 | 85.9 | 84.7 |
| 法律 跨多个片段的复杂推理 | 73.9 | 74.5 | 71.2 |
| 编码 代码理解与大型文件系统 | 86 | 85 | 81 |

*内部数据来源。

### [金融分析](#financial-analysis)

仅靠语义检索，从文件中提取表格和数值数据颇具挑战。
混合检索让你能从 SEC 文件等文档中准确检索此类数据*，使模型能够精确引用信息。

### 

检索得分

xAI Collections & Grok 4.1

Google File Search & Gemini Pro 3**

OpenAI VS & GPT 5.1

*基于内部数据集。

**Gemini 不公开实际检索到的文件，因此该指标衡量的是 Gemini 引用的文件而非原始检索到的文件。我们将 Gemini 的默认 top k 设为 20 个段落。

### [法律分析（LegalBench）](#legal-analysis-legalbench)

[LegalBench 数据集](https://github.com/zeroentropy-ai/legalbenchrag) 测试对细腻法律语言和复杂交叉引用的检索与推理能力，
由来自多个数据集、涵盖大量真实商业合同的语料中抽取的 128 组高难度问答对构成。

### 

检索得分

xAI Collections & Grok 4.1

Google File Search & Gemini Pro 3*

OpenAI VS & GPT 5.1

*Gemini 不公开实际检索到的文件，因此该指标衡量的是 Gemini 引用的文件而非原始检索到的文件。我们将 Gemini 的默认 top k 设为 20 个段落。

### [代码库（DeepCodeBench）](#codebase-deepcodebench)

代码理解对代码摘要与生成等应用至关重要。
我们使用 [DeepCodeBench 数据集](https://huggingface.co/datasets/Qodo/deep_code_bench) 对此进行全面基准测试。
它包含取自真实开源仓库、API 用法和复杂算法问题的多样化任务。

### 端到端回答表现

准确率得分

Grok 4.1

Gemini Pro 3

GPT 5.1

*我们在 DeepCodeBench 的 232 个代码问答数据点（跨 8 个仓库、包含 8,000 个文件）上评测了智能体检索的代码理解能力。

## [数据隐私](#data-privacy)

除非用户同意，我们不会将存储在 Collections 上的用户数据用于模型训练。

## [开始构建](#start-building)

[![打开的书本图标](/_next/static/media/docs.a3d5de8a.svg)

阅读

Collections 概览](https://docs.x.ai/docs/key-information/collections)[![打开的书本图标](/_next/static/media/docs.a3d5de8a.svg)

阅读

Collections 指南](https://docs.x.ai/docs/guides/using-collections)

### [创建并检索 Collections](#creating-and-searching-collections)

py

```
from xai_sdk import Client

client = Client()
collection = client.collections.create(
    name="Research Papers",
    model_name="grok-embedding-small"
)

document = client.collections.upload_document(
    collection.collection_id,
    name="ml-fundamentals.txt",
    data=b"...",
)

results = client.collections.search(
    query="What is machine learning?",
    collection_ids=[collection.collection_id],
    retrieval_mode="hybrid",
)
```

### [在聊天中使用 Collections](#using-collections-in-chat)

py

```
from xai_sdk import Client
from xai_sdk.chat import user, system
from xai_sdk.tools import collections_search

client = Client()
chat = client.chat.create(
    model="grok-4-1-fast",
    messages=[
        system("You are a personal tutor teaching the Fundamentals of AI and ML, check our notes."),
        user("Explain to me the core concepts."),
    ],
    tools=[
        collections_search(
            collection_ids=["collection_27ce08b9-87fd-4d1a-a9e7-8a199107e54f"],
            retrieval_mode="hybrid",
        ),
    ],
)
```

### [直接调用 API](#direct-api-usage)

sh

```
curl -X POST https://api.x.ai/v1/documents/search \
        -H "Authorization: Bearer $XAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
        "query": "Fundamentals of AI and ML.",
        "source": {
            "collection_ids": [
                "collection_27ce08b9-87fd-4d1a-a9e7-8a199107e54f"
            ]
        },
        "retrieval_mode": { "type": "hybrid" }
    }'
```

*免费试用期结束后可能会产生费用。我们将随后提供更多信息。

在以下平台试用 Grok

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[X 上的 Grok](https://x.com/i/grok)

产品

[Grok](/grok)

[𝕏](https://x.com)

[API](/api)

[Grok 企业版](/grok/business)

[Grokipedia](https://grokipedia.com)

公司

[公司介绍](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[文档](https://docs.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[安全中心](/safety)

[法律](/legal)

[状态](https://status.x.ai)

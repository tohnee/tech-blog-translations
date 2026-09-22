---
title: "grok-collections-api"
date: 2026-01-01
source: https://x.ai/news/grok-collections-api
crawled: 2026-09-22
---

December 22, 2025

## Grok Collections API

State-of-the-art RAG system built directly into our API.

Listen to this blog post

Listen to this blog post

Today, we're excited to announce Collections API. With Collections, you can upload and search through entire datasets.
From PDFs and Excel sheets to entire codebases, you can upload your files into a knowledge base that supports precise and fast search.
This allows developers to build RAG applications without the headache of managing indexing and retrieval infrastructure.

To help you get started, we're making file indexing and storage free for the first week*, with retrieval priced at a flat rate of $2.50 per 1,000 searches.

## [Indexing](#indexing)

- **Powerful document understanding**: We use OCR and layout-aware parsing to extract text while preserving structure such as the layout of a PDF, hierarchy of an Excel table, or the syntax of code.
- **Smart file management**: Easily upload, update, and download files. And when a file changes, our system efficiently reindexes it to ensure your collection is never stale.
- **Broad format support**: Collections supports a wide range of file types. [(see full list)](https://docs.x.ai/docs/key-information/collections#supported-mime-types)

## [Retrieval](#retrieval)

Choose the retrieval method that best fits your use case:

- **Semantic search**: To search using the meaning and intent behind a query.
- **Keyword search**: For precise term matching.
- **Hybrid search**: For the highest accuracy, combine keyword and semantic search. We support both a dedicated reranker model and reciprocal rank fusion.

What is our financial forecast for Q1 2026?

Financial_plan_2026.txt

Our company's annual financial projections indicate a robust growth trajectory for the upcoming fiscal year, with expected revenue increases driven by expanded market share in emerging sectors. Analysts predict a 15% rise in Q1 2026, bolstered by strategic investments in technology and supply chain optimization. Key metrics such as EBITDA and net profit margins are forecasted to improve.

semantickeywordhybrid

## [Benchmark Results](#benchmark-results)

Our Collections API delivers state-of-the-art retrieval performance, matching or outperforming leading models in real-world RAG tasks across finance, legal, and coding domains.

These fields are especially challenging due to their long, dense documents. To avoid hallucinations and deliver reliable answers, models must retrieve the exact passages and reason over them accurately.

### Accuracy*

(Higher is better)

| Task | xAI Grok 4.1 Fast | Google Gemini Pro 3 | OpenAI GPT 5.1 |
| --- | --- | --- | --- |
| Finance Tabular and numerical questions | 93.0 | 85.9 | 84.7 |
| Legal Complex reasoning over multiple chunks | 73.9 | 74.5 | 71.2 |
| Coding Code understanding and large file systems | 86 | 85 | 81 |

*Internal source.

### [Financial Analysis](#financial-analysis)

Extracting tabular and numerical data from files can be challenging with semantic search alone.
Hybrid search enables you to accurately retrieve this data from documents such as SEC filings*, allowing the model to precisely reference information.

### 

Retrieval Score

xAI Collections & Grok 4.1

Google File Search & Gemini Pro 3**

OpenAI VS & GPT 5.1

*Based on an internal dataset.

**Gemini does not expose the actual retrieved files so this metric measures the files cited by Gemini rather than the raw retrieved files. We set the default top k for Gemini to be 20 passages.

### [Legal Analysis (LegalBench)](#legal-analysis-legalbench)

The [LegalBench dataset](https://github.com/zeroentropy-ai/legalbenchrag) tests retrieval and reasoning over nuanced legal language and complex cross-references,
consisting of 128 challenging question-answer pairs drawn from an extensive corpus of authentic commercial contracts across multiple datasets.

### 

Retrieval Score

xAI Collections & Grok 4.1

Google File Search & Gemini Pro 3*

OpenAI VS & GPT 5.1

*Gemini does not expose the actual retrieved files so this metric measures the files cited by Gemini rather than the raw retrieved files. We set the default top k for Gemini to be 20 passages.

### [Codebase (DeepCodeBench)](#codebase-deepcodebench)

Code understanding is crucial for applications such as code summarization and generation.
We use the [DeepCodeBench dataset](https://huggingface.co/datasets/Qodo/deep_code_bench) to comprehensively benchmark for this.
It features a diverse set of tasks drawn from real-world open-source repositories, API usage, and complex algorithmic problems.

### End to End Answer Performance

Accuracy Score

Grok 4.1

Gemini Pro 3

GPT 5.1

*We evaluated the code understanding capability of agentic search on 232 code Q&A datapoints from DeepCodeBench across 8 repositories containing 8,000 files.

## [Data Privacy](#data-privacy)

We do not use user data stored on Collections for model training purposes, unless the user has given consent.

## [Start Building](#start-building)

[![Open book icon](/_next/static/media/docs.a3d5de8a.svg)

Read

Collections Overview](https://docs.x.ai/docs/key-information/collections)[![Open book icon](/_next/static/media/docs.a3d5de8a.svg)

Read

Collections Guide](https://docs.x.ai/docs/guides/using-collections)

### [Creating and Searching Collections](#creating-and-searching-collections)

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

### [Using Collections in Chat](#using-collections-in-chat)

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

### [Direct API Usage](#direct-api-usage)

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

*You may be charged after the free trial period. We will follow up with more information.

Try Grok On

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

Products

[Grok](/grok)

[𝕏](https://x.com)

[API](/api)

[Grok Enterprise](/grok/business)

[Grokipedia](https://grokipedia.com)

Company

[Company](/company)

[Careers](/careers)

[Contact](/contact)

[News](/news)

Resources

[Documentation](https://docs.x.ai)

[Privacy policy](/privacy-policy)

[Security](/security)

[Safety](/safety)

[Legal](/legal)

[Status](https://status.x.ai)

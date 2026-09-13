---
title: "Gemini Embedding 2：我们首个原生多模态嵌入模型"
title_en: "Gemini Embedding 2: Our first natively multimodal embedding model"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/
site: gemini
date: 2026-03-10
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Embedding 2：我们首个原生多模态嵌入模型

> 原文：[Gemini Embedding 2: Our first natively multimodal embedding model](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/) · Google

今天，我们发布 Gemini Embedding 2——我们首个基于 Gemini 架构构建的全多模态嵌入（embedding）模型——通过 [Gemini API](https://ai.google.dev/gemini-api/docs/embeddings) 和 [Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/embedding-2) 以公开预览版（Public Preview）形式提供。

在我们此前纯文本模型的基础上进一步扩展，Gemini Embedding 2 将文本、图像、视频、音频和文档映射到单一、统一的嵌入空间中，并能捕捉超过 100 种语言的语义意图。这简化了复杂的处理管线，并增强了各类多模态下游任务——从检索增强生成（RAG）和语义搜索，到情感分析和数据聚类。

## 新模态与灵活的输出维度

该模型基于 Gemini 构建，并利用其一流的多模态理解能力，在以下方面创建高质量嵌入：

- **文本：** 支持高达 8192 个输入 token 的超长上下文
- **图像：** 每次请求最多可处理 6 张图像，支持 PNG 和 JPEG 格式
- **视频：** 支持长达 120 秒的 MP4 和 MOV 格式视频输入
- **音频：** 原生摄取并嵌入音频数据，无需中间的文本转录
- **文档：** 直接嵌入长达 6 页的 PDF

除了一次处理一种模态之外，该模型还能原生理解交错输入，因此你可以在单个请求中传入多种模态的输入（例如图像 + 文本）。这使模型能够捕捉不同媒体类型之间复杂而细微的关系，从而对复杂的真实世界数据实现更准确的理解。

与我们之前的嵌入模型一样，Gemini Embedding 2 采用了 Matryoshka Representation Learning（MRL，套娃表示学习）技术，通过动态缩减维度来「嵌套」信息。这使得输出维度可以从默认的 3072 灵活下调，让开发者能够在性能与存储成本之间取得平衡。我们推荐使用 3072、1536、768 维以获得最高质量。

想看看这些嵌入的实际效果，可以试试我们的轻量级多模态语义搜索[演示](https://findmemedia.lmm.ai/)。

## **最先进的性能**

Gemini Embedding 2 不仅仅是对旧模型的改进。它为多模态深度树立了新的性能标准，引入了强大的语音能力，并在文本、图像和视频任务上超越了领先模型。这种可衡量的提升与独特的多模态覆盖，恰好满足了开发者多样化的嵌入需求。

![Gemini embedding 2 基准测试](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-embedding-2-benchmarks.width-1200.format-webp.webp)

## **为数据解锁更深层的含义**

嵌入是支撑许多 Google 产品体验的技术。从嵌入在上下文工程中发挥关键作用的 RAG，到大规模数据管理和经典的搜索/分析，我们的一些早期合作方已经在使用 Gemini Embedding 2 来解锁高价值的多模态应用：

!["让我们的团队能够无缝搜索过去和现在的内容，这促使我们越来越多地转向向量搜索。起初，传统的大型文本嵌入（3,072 维）带来了很好的效果，但向量空间的拥挤很快就成了问题；正确的结果无法可靠地从噪声中浮现出来。Gemini 全新的 Embedding 2 模型彻底改变了局面。文本查询现在可以精确定位未经转录的微表情，我们甚至可以将现有媒体（如一张照片或一段 B-roll 视频片段）作为搜索输入，即时检索匹配的视频素材。这将我们的文本到视频 Recall@1 指标提升到了 85.3%。" Paramount Skydance 技术创新副总裁 Seth Georgian](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote6.width-100.format-webp.webp)

["我们选择 Gemini 嵌入来帮助法律专业人士在诉讼的取证（discovery）过程中找到关键信息——这是一个高风险环境中的高技术挑战，而 Gemini 正擅长于此。在我们最近的测试中，Gemini 的多模态嵌入模型在数百万条记录上提升了精确率和召回率，同时为图像和视频解锁了强大的全新搜索功能。对法律专业人士而言，这些新能力开辟了全新的途径，即使是在最大规模的案件中也能快速理解案件材料。" Everlaw CTO Max Christoff](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote1.width-100.format-webp.webp)

!["Gemini Embedding 2 是 Sparkonomy 创作者经济公平引擎的基础。其原生多模态能力通过省去 LLM 推理将我们的延迟降低了最多 70%，并将文本-图像和文本-视频对的语义相似度得分几乎翻倍——从 0.4 跃升至 0.8。这让我们的专有 Creator Genome 能够以前所未有的精度索引数百万分钟的视频，以及图像和文本——解锁无偏见的品牌合作，并让每一位创作者都能公平地获得经济上的成功。" Sparkonomy 联合创始人 Guneet Singh](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote2.width-100.format-webp.webp)

!["API 的延续性非常出色。Gemini Embedding 2 只需极少的改动就能直接嵌入我们现有的工作流程。我们正在测试将基于文本的对话记忆与音频和视觉嵌入一起嵌入的新方法，尤其是助手的问答对，并为我们的个人健康应用带来了 20% 的 top-1 召回率提升。" Mindlid 联合创始人 Ertuğrul Çavuşoğlu](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote3.width-100.format-webp.webp)

## **今天就开始构建**

通过 [Gemini API](https://ai.google.dev/gemini-api/docs/embeddings) 或 [Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings) 开始使用 Gemini Embedding 2 模型。

```py
from google import genai
from google.genai import types

# client = genai.Client(vertexai=True, project=PROJECT_ID, location='us-central1')

client = genai.Client()

with open("example.png", "rb") as f:
    image_bytes = f.read()

with open("sample.mp3", "rb") as f:
    audio_bytes = f.read()

# Embed text, image, and audio 
result = client.models.embed_content(
    model="gemini-embedding-2-preview",
    contents=[
        "What is the meaning of life?",
        types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png",
        ),
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/mpeg",
        ),
    ],
)

print(result.embeddings)
```

在我们交互式的 [Gemini API](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Embeddings.ipynb) 和 [Vertex AI](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/embedding/intro_gemini_embedding.ipynb) Colab notebook 中学习如何使用该模型。你也可以通过 [LangChain](https://docs.langchain.com/oss/python/integrations/text_embedding/google_generative_ai)、[LlamaIndex](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/)、[Haystack](https://haystack.deepset.ai/integrations/google-genai)、[Weaviate](https://docs.weaviate.io/weaviate/model-providers/google)、[QDrant](https://qdrant.tech/documentation/embeddings/gemini/)、[ChromaDB](https://docs.trychroma.com/integrations/embedding-models/google-gemini) 和 [Vector Search](https://docs.cloud.google.com/vertex-ai/docs/vector-search-2/overview) 来使用它。

通过为身边的多样化数据赋予语义含义，Gemini Embedding 2 为下一代先进 AI 体验提供了不可或缺的多模态基础。我们迫不及待想看到你的构建成果。

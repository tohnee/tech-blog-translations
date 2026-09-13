---
title: "Gemini Embedding 2: Our first natively multimodal embedding model"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/
site: gemini
date: 2026-03-10
authors: Min Choi
crawled: 2026-09-13
---

Today we’re releasing Gemini Embedding 2, our first fully multimodal embedding model built on the Gemini architecture, in Public Preview via the [Gemini API](https://ai.google.dev/gemini-api/docs/embeddings) and [Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/embedding-2).

Expanding on our previous text-only foundation, Gemini Embedding 2 maps text, images, videos, audio and documents into a single, unified embedding space, and captures semantic intent across over 100 languages. This simplifies complex pipelines and enhances a wide variety of multimodal downstream tasks—from Retrieval-Augmented Generation (RAG) and semantic search to sentiment analysis and data clustering.

## New modalities and flexible output dimensions

The model is based on Gemini and leverages its best-in-class multimodal understanding capabilities to create high-quality embeddings across:

- **Text:** supports an expansive context of up to 8192 input tokens
- **Images:** capable of processing up to 6 images per request, supporting PNG and JPEG formats
- **Videos:** supports up to 120 seconds of video input in MP4 and MOV formats
- **Audio:** natively ingests and embeds audio data without needing intermediate text transcriptions
- **Documents:** directly embed PDFs up to 6 pages long

Beyond processing one modality at a time, this model natively understands interleaved input so you can pass multiple modalities of input (e.g., image + text) in a single request. This allows the model to capture the complex, nuanced relationships between different media types, unlocking more accurate understanding of complex, real-world data.

Like our previous embedding models, Gemini Embedding 2 incorporates Matryoshka Representation Learning (MRL), a technique that “nests” information by dynamically scaling down dimensions. This enables flexible output dimensions scaling down from the default 3072 so developers can balance performance and storage costs. We recommend using 3072, 1536, 768 dimensions for highest quality.

To see these embeddings in action, try out our lightweight multimodal semantic search [demo](https://findmemedia.lmm.ai/).

## **State-of-the-art performance**

Gemini Embedding 2 doesn't just improve on legacy models. It establishes a new performance standard for multimodal depth, introducing strong speech capabilities and outperforming leading models in text, image, and video tasks. This measurable improvement and unique multimodal coverage give developers exactly what they need for their diverse embedding needs.

![Gemini embedding 2 benchmarks](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-embedding-2-benchmarks.width-1200.format-webp.webp)

## **Unlocking deeper meaning for data**

Embeddings are the technology that power experiences in many Google products. From RAG where embeddings can play a crucial role in context engineering to large-scale data management and classic search/analysis, some of our early access partners are already using Gemini Embedding 2 to unlock high-value multimodal applications:

!["Empowering our teams to seamlessly search past and present content has increasingly driven us to vector search. While initially seeing great results with traditional large text embeddings (3,072 dim), crowding in vector space quickly took over; the right results couldn't reliably surface their way up from the noise. Gemini's new Embedding 2 model completely changed the game. Text queries can now pinpoint untranscribed micro-expressions, and we can even leverage existing media, such as a photo or B-roll clip, as the search input to instantly retrieve matching video assets. This propelled our text-to-video Recall@1 rate to 85.3%." Seth Georgian, VP Technology Innovation, Paramount Skydance](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote6.width-100.format-webp.webp)

!["We chose Gemini embeddings to help legal professionals find critical information during the discovery process in litigation -- a highly technical challenge in a high-stakes setting, and one Gemini excels at. In our most recent tests, Gemini's multi-modal embedding model improves precision and recall across millions of records, while unlocking powerful new search functionality for images and videos. For legal professionals, these new capabilities open up entirely novel ways to quickly understand case materials in even the largest matters." Max Christoff, CTO at Everlaw](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote1.width-100.format-webp.webp)

!["Gemini Embedding 2 is the foundation for Sparkonomy’s Creator Economic Equality Engine. Its native multi-modality slashes our latency by up to 70% by removing LLM inference and nearly doubles semantic similarity scores for text-image and text-video pairs—leaping from 0.4 to 0.8. This powers our proprietary Creator Genome to index millions of minutes of video, alongside images and text, with unprecedented precision—unlocking unbiased brand collaborations and democratizing economic success for every creator." Guneet Singh, Co-founder at Sparkonomy](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote2.width-100.format-webp.webp)

!["The API continuity is excellent. Gemini Embedding 2 drops right into our existing workflow with minimal changes. We’re testing new ways to embed text-based conversational memories together with audio and visual embeddings, especially assistant question-and-answer pairs, and seeing a 20% lift in top-1 recall for our personal wellness app."  Ertuğrul Çavuşoğlu, Co-founder at Mindlid](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Quote3.width-100.format-webp.webp)

## **Start building today**

Get started with the Gemini Embedding 2 model through [Gemini API](https://ai.google.dev/gemini-api/docs/embeddings) or [Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings).

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

Learn how to use the model in our interactive [Gemini API](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Embeddings.ipynb) and [Vertex AI](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/embedding/intro_gemini_embedding.ipynb) Colab notebooks. You can also use it through [LangChain](https://docs.langchain.com/oss/python/integrations/text_embedding/google_generative_ai), [LlamaIndex](https://developers.llamaindex.ai/python/framework/integrations/embeddings/google_genai/), [Haystack](https://haystack.deepset.ai/integrations/google-genai), [Weaviate](https://docs.weaviate.io/weaviate/model-providers/google), [QDrant](https://qdrant.tech/documentation/embeddings/gemini/), [ChromaDB](https://docs.trychroma.com/integrations/embedding-models/google-gemini), and [Vector Search](https://docs.cloud.google.com/vertex-ai/docs/vector-search-2/overview).

By bringing semantic meaning to the diverse data around us, Gemini Embedding 2 provides the essential multimodal foundation for the next era of advanced AI experiences. We can’t wait to see what you build.

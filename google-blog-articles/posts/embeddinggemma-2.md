---
title: "EmbeddingGemma 2: an open, lightweight multimodal embedding model"
source: https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/
site: google-blog
date: 2026-10-06
authors: Sahil Dua
crawled: 2026-10-08
---

We introduced [EmbeddingGemma](https://developers.googleblog.com/en/introducing-embeddinggemma/) last year to provide a lightweight option for high-quality text embeddings, to help your apps organize, search, and connect information directly on consumer hardware. The developer community’s response blew past our expectations. With more than 20 million downloads, builders have used it to power smarter on-device search tools and privacy-first retrieval augmented generation (RAG) pipelines.

Today, we’re launching EmbeddingGemma 2**,** expanding beyond text to unify code, images, video, and audio in a shared embedding space. Built on the Gemma 4 architecture and released under a commercially permissive Apache 2.0 license, EmbeddingGemma 2 has 740 million parameters, making it optimal for on-device inference. It can help find a specific video clip from a voice memo, or search through hours of audio recordings based on a text query, all processed by a single, natively multimodal model.

Built from the same technology as Gemini Embedding models, EmbeddingGemma 2 is:

- **Best-in-class for its size:** Achieves leading scores among sub-1B multimodal embedders for its size across benchmarks like MTEB (Massive Text Embedding Benchmark) Code and MAEB (Massive Audio Embedding Benchmark), while matching or outperforming many larger models across text, vision, and audio tasks.
- **Modular by design:** Requires as little as 270M parameters for text-only workloads with optional vision (170M) and audio (300M) encoders for full multimodal support.
- **Storage-efficient:** Using Matryoshka Representation Learning (MRL), developers can dynamically truncate output vectors from 768 dimensions down to 512, 256, or 128 dimensions. This provides up to 6x storage reduction for local vector databases and memory usage.
- **Optimized for on-device performance:** Runs efficiently within tight resource constraints. With quantization, on a Google Pixel 11 Pro, EmbeddingGemma 2 requires as little as ~191MB active RAM for text-only weights and ~567MB for the full multimodal model.
- **Extended context ready:** Features an 8K token context window (4x larger than EmbeddingGemma 1), allowing it to process up to 5.5 minutes of audio, 29 images, 58 video frames, or interleaved combinations thereof directly on local hardware.

## Achieving top-tier quality for code, vision, and audio

EmbeddingGemma 2 matches the strong multilingual text performance of EmbeddingGemma while delivering a significant 9.92-point improvement on code performance (in MTEB Code, from 68.76 to 78.68), making it well-suited for local codebase indexing, semantic code search, and coding agent retrieval. Across image, video, documents, and audio, it sets a new standard in quality-per-parameter for sub-1B models and even outperforms some specialist models more than twice its size.

![Massive Text Embedding Benchmark (Code)](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Massive_Text_Embedding_Benchmark_.width-100.format-webp.webp)

![Massive Image Embedding Benchmark (Lite)](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Massive_Image_Embedding_Benchmark.width-100.format-webp.webp)

![Massive Audio Embedding Benchmark](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Massive_Audio_Embedding_Benchmark.width-100.format-webp.webp)

Find full evaluation metrics and model information in the [EmbeddingGemma 2 model card](https://ai.google.dev/gemma/docs/embeddinggemma/model_card_2).

## Enabling semantic search, routing, and retrieval, fully on-device

EmbeddingGemma 2 brings robust capabilities directly to edge hardware. Generating embeddings locally helps ensure data privacy, reduces pipeline latency, and empowers developers to build cross-modal search and retrieval that works entirely offline.

When paired with generative models such as Gemma 4, EmbeddingGemma 2 enables on-device RAG pipelines that understand complex multimodal data. Because EmbeddingGemma 2 is built on Gemma 4 and shares its text tokenizer and audio encoder, developers can run both models together in a unified pipeline with a lower combined total memory footprint.

Use text or an image to find the top matches in your media library based on semantic similarity. Try it in [Google AI Edge Gallery](https://developers.google.com/edge/gallery)’s Instant Media Search.

Locate specific moments in video using text or audio queries. Try it in [Google AI Edge Gallery](https://developers.google.com/edge/gallery)’s Video Moments Finder.

Pair EmbeddingGemma 2 for local file retrieval with Gemma 4 for contextual reasoning. Try it in the [Google AI Edge Foresight](https://developers.google.com/edge/foresight) app.

Create real-time decision engines leveraging multimodal context for classification, routing, and predictive capabilities via the [MediaPipe Decision Task API](https://developers.google.com/edge/mediapipe/solutions/decision/decision_maker).

To learn how to build on-device search and RAG systems with LiteRT, read the [Google AI Edge blog post](http://developers.googleblog.com/google-ai-edge-with-embeddinggemma-2).

## Getting started with EmbeddingGemma 2

We worked closely with the following partners to ensure EmbeddingGemma 2 works immediately where you build:

- **Download the models:** Find the model weights on [Hugging Face](https://huggingface.co/google/embeddinggemma-2) and [Kaggle](https://www.kaggle.com/models/google/embeddinggemma-2), with Gemini Enterprise Agent Platform Model Garden availability coming soon. Visit [LiteRT Community on Hugging Face](https://huggingface.co/litert-community) for models optimized for on-device.
- **On-device deployment:** Develop cross-platform apps with Google AI Edge [MediaPipe](https://developers.google.com/edge/mediapipe/solutions/decision/decision_maker) for turnkey embedding, retrieval & decision tasks or [LiteRT](https://developers.google.com/edge/litert-lm) for custom model integration. Build for the browser with transformers.js or [WebGPU](https://huggingface.co/spaces/webml-community/embeddinggemma-2-webgpu).
- **Use your favorite development tools**: Serve the model efficiently using transformers, sentence-transformers, [MLX](https://github.com/Blaizzy/mlx-vlm), vLLM, [llama.cpp](https://huggingface.co/ggml-org/embeddinggemma-2-GGUF), SGLang, [Ollama](http://ollama.com/library/embeddinggemma-2), and LMStudio. Store your embedding vectors with [Qdrant](https://qdrant.tech/blog/embeddinggemma-2/).
- **Fine-tuning:** Follow guidance by [Unsloth](https://unsloth.ai/docs/models/embeddinggemma-2) for how to fine-tune EmbeddingGemma 2 for your use cases.

Explore our [developer guide](https://developers.googleblog.com/en/embeddinggemma-2-the-developer-guide/), [documentation](https://ai.google.dev/gemma/docs/embeddinggemma), and guides for [inference](https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers) and [fine-tuning](https://ai.google.dev/gemma/docs/embeddinggemma/fine-tuning-embeddinggemma-with-sentence-transformers).

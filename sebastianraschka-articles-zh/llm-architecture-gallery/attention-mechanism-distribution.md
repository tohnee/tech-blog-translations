---
title: "LLM 架构画廊 - 注意力机制分布"
title_en: "LLM Architecture Gallery - Attention Mechanism Distribution"
source: https://sebastianraschka.com/llm-architecture-gallery/attention-mechanism-distribution/
crawled: 2026-09-06
translated: 2026-09-06
---

# LLM 架构画廊 - 注意力机制分布

> 原文：[LLM Architecture Gallery - Attention Mechanism Distribution](https://sebastianraschka.com/llm-architecture-gallery/attention-mechanism-distribution/)

[返回画廊](https://sebastianraschka.com/llm-architecture-gallery/)

[sebastianraschka.com/llm-architecture-gallery/](https://sebastianraschka.com/llm-architecture-gallery/)

# 注意力机制分布

以下统计覆盖 LLM 架构画廊中 102 张可见卡片。类别之间互不排斥：当一个模型组合了多种机制（例如 MLA 加 DeepSeek 稀疏注意力）时，它会在多行中同时计数。

| 机制或模式 | 数量 | 占比 | 对应模型 |
| --- | --- | --- | --- |
| GQA 系注意力 分组查询、多查询或 CCA/GQA 风格的注意力。 | 65 | 63.7% | Llama 3 8B Llama 3.2 1B Gemma 3 27B Mistral Small 3.1 24B Llama 4 Maverick Qwen3 0.6B Qwen3 235B-A22B Qwen3 30B-A3B Qwen3 32B Qwen3 4B Qwen3 8B SmolLM3 3B GLM-4.5 355B GPT-OSS 120B GPT-OSS 20B Gemma 3 270M Grok 2.5 270B MiniMax M2 230B OLMo 3 32B Nemotron 3 Nano 30B-A3B Nemotron 3.5 Lightning 30B-A3B GLM-4.7 355B Arcee AI Trinity Large 400B Nemotron 3 Super 120B-A12B Nemotron 3 Ultra 550B-A55B Gemma 4 31B Gemma 4 12B JetBrains Mellum2 Thinking 12B-A2.5B LFM2.5 350M LFM2.5 1.2B LFM2.5 8B-A1B Gemma 4 26B-A4B Phi-4 GLM-4.5-Air Qwen3 Coder Flash 30B-A3B Step 3.5 Flash 196B Nanbeige 4.1 3B MiniMax M2.5 230B Tiny Aya 3.35B Sarvam 30B Llama 3.2 3B INTELLECT-3 Nemotron 3 Nano 4B MiniMax M2.7 230B Gemma 4 E2B Gemma 4 E4B Tencent Hy3-preview 295B-A21B Xiaomi MiMo-V2.5-Pro 1.02T Laguna XS.2 Granite 4.1 30B ZAYA1-8B Command A+ 218B-A25B North Mini Code 30B-A3B MiniMax M3 428B VibeThinker-3B Inkling Soofi S 30B-A3B Nanbeige 4.2 3B Laguna XS 2.1 Laguna S 2.1 Antares 1B Solar Open 2 Muse Glimmer 30B Ornith 1.5 35B-A3B Qwen3.8-Flash-Next 125B-A6B |
| MLA 系注意力 多头潜在注意力（MLA）及其紧密相关的 MLA 变体。 | 24 | 23.5% | DeepSeek V3 DeepSeek R1 Kimi K2 Kimi Linear 48B-A3B DeepSeek V3.2 Mistral Large 3 GLM-5 744B Kimi K2.5 Ling 2.5 1T Sarvam 105B LongCat-Flash-Lite 68.5B-A3B Mistral Small 4 GLM-5.1 GLM-5.2 Kimi K2.6 Ling 2.6 1T DeepSeek V4-Flash DeepSeek V4-Pro Kimi K2.7 Code Motif 3 Beta Kimi K3 Ling 3.0 Flash GLM-5.3-Flash Tencent Hy4-preview 770B-A49B |
| 滑动窗口/全局模式 将局部/分块/滑动窗口层与全局/完整注意力层混合的架构。 | 27 | 26.5% | Gemma 3 27B Llama 4 Maverick GPT-OSS 120B GPT-OSS 20B Gemma 3 270M OLMo 3 32B OLMo 3 7B Xiaomi MiMo-V2-Flash 309B Arcee AI Trinity Large 400B Gemma 4 31B Gemma 4 12B JetBrains Mellum2 Thinking 12B-A2.5B Gemma 4 26B-A4B Step 3.5 Flash 196B Tiny Aya 3.35B Gemma 4 E2B Gemma 4 E4B Xiaomi MiMo-V2.5 310B Xiaomi MiMo-V2.5-Pro 1.02T Laguna XS.2 Command A+ 218B-A25B North Mini Code 30B-A3B Inkling Motif 3 Beta Laguna XS 2.1 Laguna S 2.1 Muse Glimmer 30B |
| DeltaNet / Lightning / Kimi Delta 将循环或线性注意力风格的层与注意力层搭配的混合架构。 | 15 | 14.7% | Qwen3 Next 80B-A3B Kimi Linear 48B-A3B Ling 2.5 1T Qwen3.5 397B Qwen3.6 35B-A3B Qwen3.6 27B Qwen3.8 27B Ling 2.6 1T BTL-3 27B Solar Open 2 Kimi K3 Ling 3.0 Flash Ornith 1.5 35B-A3B GLM-5.3-Flash Qwen3.8-Flash-Next 125B-A6B |
| Mamba / mLSTM 循环层 Mamba-2、mLSTM 或循环状态空间风格的模块。 | 7 | 6.9% | Nemotron 3 Nano 30B-A3B Nemotron 3.5 Lightning 30B-A3B Nemotron 3 Super 120B-A12B Nemotron 3 Ultra 550B-A55B xLSTM 7B Nemotron 3 Nano 4B Soofi S 30B-A3B |
| DeepSeek Sparse Attention 明确使用 DeepSeek Sparse Attention 变体的模型。 | 6 | 5.9% | DeepSeek V3.2 GLM-5 744B GLM-5.1 GLM-5.2 GLM-5.3-Flash Tencent Hy4-preview 770B-A49B |
| [Qwen Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/) 由 Qwen 的可学习索引器选择的微块稀疏注意力。 | 1 | 1.0% | Qwen3.8-Flash-Next 125B-A6B |
| [IndexShare / IndexCache](https://sebastianraschka.com/llm-architecture-gallery/indexshare/) 跨层复用 DSA top-k 索引器的选择结果。 | 2 | 2.0% | GLM-5.2 Tencent Hy4-preview 770B-A49B |
| MiniMax Sparse Attention 明确使用 MiniMax Sparse Attention 变体的模型。 | 1 | 1.0% | MiniMax M3 428B |
| MHA 系注意力 以经典多头注意力（不采用 GQA/MLA）作为主要机制。 | 4 | 3.9% | GPT-2 XL 1.5B OLMo 2 7B OLMo 3 7B Ouro-Thinking 2.6B |
| CSA/HCA DeepSeek V4 风格模型中的压缩稀疏或超压缩注意力变体。 | 2 | 2.0% | DeepSeek V4-Flash DeepSeek V4-Pro |
| CCA 压缩上下文注意力。 | 1 | 1.0% | ZAYA1-8B |
| 无自注意力 没有自注意力层的循环架构条目。 | 1 | 1.0% | xLSTM 7B |

**注意：**本表统计的是可见的画廊卡片，而不是去重后的模型家族。数据使用的是画廊中注意力、层配置和解码器类型等元数据字段。

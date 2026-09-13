---
title: "LLM Architecture Gallery - Attention Mechanism Distribution"
source: https://sebastianraschka.com/llm-architecture-gallery/attention-mechanism-distribution/
crawled: 2026-09-06
---

# LLM Architecture Gallery - Attention Mechanism Distribution

[Back to the Gallery](https://sebastianraschka.com/llm-architecture-gallery/)

[sebastianraschka.com/llm-architecture-gallery/](https://sebastianraschka.com/llm-architecture-gallery/)

# Attention Mechanism Distribution

Counts across 102 visible LLM Architecture Gallery cards. Categories are non-exclusive: one model can count in multiple rows when it combines mechanisms such as MLA plus DeepSeek Sparse Attention.

| Mechanism or pattern | Count | Share | Matching models |
| --- | --- | --- | --- |
| GQA-family attention Grouped-query, multi-query, or CCA/GQA-style attention. | 65 | 63.7% | Llama 3 8B Llama 3.2 1B Gemma 3 27B Mistral Small 3.1 24B Llama 4 Maverick Qwen3 0.6B Qwen3 235B-A22B Qwen3 30B-A3B Qwen3 32B Qwen3 4B Qwen3 8B SmolLM3 3B GLM-4.5 355B GPT-OSS 120B GPT-OSS 20B Gemma 3 270M Grok 2.5 270B MiniMax M2 230B OLMo 3 32B Nemotron 3 Nano 30B-A3B Nemotron 3.5 Lightning 30B-A3B GLM-4.7 355B Arcee AI Trinity Large 400B Nemotron 3 Super 120B-A12B Nemotron 3 Ultra 550B-A55B Gemma 4 31B Gemma 4 12B JetBrains Mellum2 Thinking 12B-A2.5B LFM2.5 350M LFM2.5 1.2B LFM2.5 8B-A1B Gemma 4 26B-A4B Phi-4 GLM-4.5-Air Qwen3 Coder Flash 30B-A3B Step 3.5 Flash 196B Nanbeige 4.1 3B MiniMax M2.5 230B Tiny Aya 3.35B Sarvam 30B Llama 3.2 3B INTELLECT-3 Nemotron 3 Nano 4B MiniMax M2.7 230B Gemma 4 E2B Gemma 4 E4B Tencent Hy3-preview 295B-A21B Xiaomi MiMo-V2.5-Pro 1.02T Laguna XS.2 Granite 4.1 30B ZAYA1-8B Command A+ 218B-A25B North Mini Code 30B-A3B MiniMax M3 428B VibeThinker-3B Inkling Soofi S 30B-A3B Nanbeige 4.2 3B Laguna XS 2.1 Laguna S 2.1 Antares 1B Solar Open 2 Muse Glimmer 30B Ornith 1.5 35B-A3B Qwen3.8-Flash-Next 125B-A6B |
| MLA-family attention Multi-head latent attention and closely related MLA variants. | 24 | 23.5% | DeepSeek V3 DeepSeek R1 Kimi K2 Kimi Linear 48B-A3B DeepSeek V3.2 Mistral Large 3 GLM-5 744B Kimi K2.5 Ling 2.5 1T Sarvam 105B LongCat-Flash-Lite 68.5B-A3B Mistral Small 4 GLM-5.1 GLM-5.2 Kimi K2.6 Ling 2.6 1T DeepSeek V4-Flash DeepSeek V4-Pro Kimi K2.7 Code Motif 3 Beta Kimi K3 Ling 3.0 Flash GLM-5.3-Flash Tencent Hy4-preview 770B-A49B |
| Sliding-window/global patterns Architectures that mix local/chunked/sliding-window layers with global/full attention layers. | 27 | 26.5% | Gemma 3 27B Llama 4 Maverick GPT-OSS 120B GPT-OSS 20B Gemma 3 270M OLMo 3 32B OLMo 3 7B Xiaomi MiMo-V2-Flash 309B Arcee AI Trinity Large 400B Gemma 4 31B Gemma 4 12B JetBrains Mellum2 Thinking 12B-A2.5B Gemma 4 26B-A4B Step 3.5 Flash 196B Tiny Aya 3.35B Gemma 4 E2B Gemma 4 E4B Xiaomi MiMo-V2.5 310B Xiaomi MiMo-V2.5-Pro 1.02T Laguna XS.2 Command A+ 218B-A25B North Mini Code 30B-A3B Inkling Motif 3 Beta Laguna XS 2.1 Laguna S 2.1 Muse Glimmer 30B |
| DeltaNet / Lightning / Kimi Delta Hybrid recurrent or linear-attention style layers paired with attention layers. | 15 | 14.7% | Qwen3 Next 80B-A3B Kimi Linear 48B-A3B Ling 2.5 1T Qwen3.5 397B Qwen3.6 35B-A3B Qwen3.6 27B Qwen3.8 27B Ling 2.6 1T BTL-3 27B Solar Open 2 Kimi K3 Ling 3.0 Flash Ornith 1.5 35B-A3B GLM-5.3-Flash Qwen3.8-Flash-Next 125B-A6B |
| Mamba / mLSTM recurrent layers Mamba-2, mLSTM, or recurrent state-space-style blocks. | 7 | 6.9% | Nemotron 3 Nano 30B-A3B Nemotron 3.5 Lightning 30B-A3B Nemotron 3 Super 120B-A12B Nemotron 3 Ultra 550B-A55B xLSTM 7B Nemotron 3 Nano 4B Soofi S 30B-A3B |
| DeepSeek Sparse Attention Explicit DeepSeek Sparse Attention variants. | 6 | 5.9% | DeepSeek V3.2 GLM-5 744B GLM-5.1 GLM-5.2 GLM-5.3-Flash Tencent Hy4-preview 770B-A49B |
| [Qwen Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/) Micro-block sparse attention selected by Qwen's learned indexer. | 1 | 1.0% | Qwen3.8-Flash-Next 125B-A6B |
| [IndexShare / IndexCache](https://sebastianraschka.com/llm-architecture-gallery/indexshare/) Cross-layer reuse of DSA top-k indexer selections. | 2 | 2.0% | GLM-5.2 Tencent Hy4-preview 770B-A49B |
| MiniMax Sparse Attention Explicit MiniMax Sparse Attention variants. | 1 | 1.0% | MiniMax M3 428B |
| MHA-family attention Classic multi-head attention without GQA/MLA as the main mechanism. | 4 | 3.9% | GPT-2 XL 1.5B OLMo 2 7B OLMo 3 7B Ouro-Thinking 2.6B |
| CSA/HCA Compressed sparse or hyper-compressed attention variants in DeepSeek V4-style models. | 2 | 2.0% | DeepSeek V4-Flash DeepSeek V4-Pro |
| CCA Compressed context attention. | 1 | 1.0% | ZAYA1-8B |
| No self-attention Recurrent architecture entries with no self-attention layers. | 1 | 1.0% | xLSTM 7B |

**Note:** this table counts visible gallery cards, not unique model families. It uses the gallery metadata fields for attention, layer mix, and decoder type.

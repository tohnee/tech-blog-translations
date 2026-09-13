---
title: "LLM Architecture Gallery - Percent Active Parameters"
source: https://sebastianraschka.com/llm-architecture-gallery/active-parameter-ratio/
crawled: 2026-09-06
---

# LLM Architecture Gallery - Percent Active Parameters

[Back to the Gallery](https://sebastianraschka.com/llm-architecture-gallery/)

[sebastianraschka.com/llm-architecture-gallery/](https://sebastianraschka.com/llm-architecture-gallery/)

# Percent Active Parameters per Token

| # | Model | Active % | Active params | Total params | Type | Date | Attention |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DeepSeek V4-Pro | 3.1% | 49B active | 1.6T | MoE | 2026-04-24 | CSA/HCA |
| 2 | Kimi K2 | 3.2% | 32B active | 1T | MoE | 2025-07-10 | MLA |
| 3 | Kimi K2.5 | 3.2% | 32B active | 1T | MoE | 2026-01-27 | MLA |
| 4 | Kimi K2.6 | 3.2% | 32B active | 1T | MoE | 2026-04-20 | MLA |
| 5 | Kimi K2.7 Code | 3.2% | 32B active | 1T | MoE | 2026-06-12 | MLA |
| 6 | Arcee AI Trinity Large 400B | 3.3% | 13B active | 400B | MoE | 2026-01-27 | 3:1 sliding-window/global gated GQA |
| 7 | Kimi K3 | 3.7% | 104B active | 2.8T | Hybrid MoE | 2026-07-27 | 3:1 Kimi Delta Attention and gated MLA |
| 8 | Qwen3 Next 80B-A3B | 3.8% | 3B active | 80B | Hybrid | 2025-09-09 | 3:1 Gated DeltaNet and Gated Attention |
| 9 | Xiaomi MiMo-V2.5-Pro 1.02T | 4.1% | 42B active | 1.02T | MoE | 2026-04-22 | GQA with 6:1 sliding-window/global attention |
| 10 | Motif 3 Beta | 4.1% | 13B active | 314B | MoE | 2026-07-21 | GDLA with 3:1 sliding-window/full attention |
| 11 | Ling 3.0 Flash | 4.1% | 5.1B active | 124B | Hybrid | 2026-08-04 | 5:1 Kimi Delta Attention and gated MLA |
| 12 | Inkling | 4.2% | 41B active | 975B | MoE | 2026-07-15 | 5:1 sliding-window/global GQA |
| 13 | Llama 4 Maverick | 4.3% | 17B active | 400B | MoE | 2025-04-05 | GQA |
| 14 | MiniMax M2 230B | 4.3% | 10B active | 230B | MoE | 2025-10-23 | GQA |
| 15 | MiniMax M2.5 230B | 4.3% | 10B active | 230B | MoE | 2026-02-12 | GQA |
| 16 | Qwen3.5 397B | 4.3% | 17B active | 397B | Hybrid | 2026-02-16 | 3:1 Gated DeltaNet and Gated Attention |
| 17 | MiniMax M2.7 230B | 4.3% | 10B active | 230B | MoE | 2026-03-18 | GQA |
| 18 | GPT-OSS 120B | 4.4% | 5.1B active | 117B | MoE | 2025-08-04 | Alternating sliding-window/global GQA |
| 19 | LongCat-Flash-Lite 68.5B-A3B | 4.4% | 3B active | 68.5B | MoE | 2026-01-28 | MLA |
| 20 | DeepSeek V4-Flash | 4.6% | 13B active | 284B | MoE | 2026-04-24 | CSA/HCA |
| 21 | Xiaomi MiMo-V2.5 310B | 4.8% | 15B active | 310B | MoE | 2026-04-22 | 5:1 sliding-window/global attention |
| 22 | Qwen3.8-Flash-Next 125B-A6B | 4.8% | 6B active | 125B core | Hybrid | 2026-08-26 | 3:1 Gated DeltaNet and Qwen Sparse Attention |
| 23 | Xiaomi MiMo-V2-Flash 309B | 4.9% | 15B active | 309B | MoE | 2025-12-16 | 5:1 sliding-window/global attention |
| 24 | GLM-5 744B | 5.4% | 40B active | 744B | MoE | 2026-02-11 | MLA with DeepSeek Sparse Attention |
| 25 | GLM-5.1 | 5.4% | 40B active | 744B | MoE | 2026-04-07 | MLA with DeepSeek Sparse Attention |
| 26 | GLM-5.2 | 5.4% | 40B active | 744B | MoE | 2026-06-17 | MLA with DeepSeek Sparse Attention and IndexShare |
| 27 | MiniMax M3 428B | 5.4% | 23B active | 428B | MoE | 2026-06-13 | GQA with MiniMax Sparse Attention |
| 28 | DeepSeek V3 | 5.5% | 37B active | 671B | MoE | 2024-12-26 | MLA |
| 29 | DeepSeek R1 | 5.5% | 37B active | 671B | MoE | 2025-01-20 | MLA |
| 30 | DeepSeek V3.2 | 5.5% | 37B active | 671B | MoE | 2025-12-01 | MLA with DeepSeek Sparse Attention |
| 31 | Step 3.5 Flash 196B | 5.6% | 11B active | 196B | MoE | 2026-02-01 | 3:1 sliding-window GQA |
| 32 | Mistral Small 4 | 5.6% | 6.63B active | 119B | MoE | 2026-03-16 | MLA |
| 33 | GLM-5.3-Flash | 5.6% | 18B active | 320B | Hybrid | 2026-08-26 | 3:1 Kimi Delta Attention and MLA/DSA |
| 34 | Solar Open 2 | 6% | 15B active | 250B | Hybrid | 2026-07-22 | 3:1 Kimi Delta Attention and gated GQA |
| 35 | Mistral Large 3 | 6.1% | 41B active | 673B | MoE | 2025-12-02 | MLA |
| 36 | Kimi Linear 48B-A3B | 6.3% | 3B active | 48B | Hybrid | 2025-10-30 | 3:1 Kimi Delta Attention and MLA |
| 37 | Ling 2.5 1T | 6.3% | 63B active | 1T | Hybrid | 2026-02-15 | Lightning Attention plus MLA |
| 38 | Ling 2.6 1T | 6.3% | 63B active | 1T | Hybrid | 2026-04-23 | Lightning Attention plus MLA |
| 39 | Tencent Hy4-preview 770B-A49B | 6.4% | 49B active | 770B | MoE | 2026-08-28 | Gated MLA with DeepSeek Sparse Attention and IndexCache |
| 40 | Laguna S 2.1 | 6.8% | 8B active | 118B | MoE | 2026-07-21 | 3:1 sliding-window/global gated GQA |
| 41 | Tencent Hy3-preview 295B-A21B | 7.1% | 21B active | 295B | MoE | 2026-04-23 | GQA |
| 42 | Sarvam 30B | 8% | 2.4B active | 30B | MoE | 2026-03-03 | GQA |
| 43 | Qwen3.6 35B-A3B | 8.6% | 3B active | 35B | Hybrid | 2026-04-15 | 3:1 Gated DeltaNet and Gated Attention |
| 44 | Ornith 1.5 35B-A3B | 8.6% | 3B active | 35B | Hybrid | 2026-08-23 | 3:1 Gated DeltaNet and Gated Attention |
| 45 | GLM-4.5 355B | 9% | 32B active | 355B | MoE | 2025-07-28 | GQA |
| 46 | GLM-4.7 355B | 9% | 32B active | 355B | MoE | 2025-12-22 | GQA |
| 47 | ZAYA1-8B | 9% | 760M active | 8.4B | MoE | 2026-05-06 | CCA with 4:1 GQA |
| 48 | Laguna XS.2 | 9.1% | 3B active | 33B | MoE | 2026-04-28 | 3:1 sliding-window/global gated GQA |
| 49 | Laguna XS 2.1 | 9.1% | 3B active | 33B | MoE | 2026-07-02 | 3:1 sliding-window/global gated GQA |
| 50 | Qwen3 235B-A22B | 9.4% | 22B active | 235B | MoE | 2025-04-28 | GQA |
| 51 | Sarvam 105B | 9.8% | 10.3B active | 105B | MoE | 2026-03-03 | MLA |
| 52 | Qwen3 30B-A3B | 10% | 3B active | 30B | MoE | 2025-04-28 | GQA |
| 53 | Nemotron 3 Nano 30B-A3B | 10% | 3B active | 30B | Hybrid MoE | 2025-12-04 | Mamba-2 + GQA |
| 54 | Nemotron 3.5 Lightning 30B-A3B | 10% | 3B active | 30B | Hybrid MoE | 2026-08-11 | Mamba-2 + GQA |
| 55 | Nemotron 3 Super 120B-A12B | 10% | 12B active | 120B | Hybrid MoE | 2026-03-11 | Mamba-2 + GQA |
| 56 | Nemotron 3 Ultra 550B-A55B | 10% | 55B active | 550B | Hybrid MoE | 2026-06-04 | Mamba-2 + GQA |
| 57 | North Mini Code 30B-A3B | 10% | 3B active | 30B | MoE | 2026-06-05 | 8:1 GQA with 3:1 sliding-window/global attention |
| 58 | Soofi S 30B-A3B | 10.1% | 3.2B active | 31.6B | Hybrid MoE | 2026-07-10 | Mamba-2 + GQA |
| 59 | Qwen3 Coder Flash 30B-A3B | 11% | 3.3B active | 30B | MoE | 2025-07-31 | GQA |
| 60 | GLM-4.5-Air | 11.3% | 12B active | 106B | MoE | 2025-07-28 | GQA |
| 61 | INTELLECT-3 | 11.3% | 12B active | 106B | MoE | 2025-11-26 | GQA |
| 62 | Command A+ 218B-A25B | 11.5% | 25B active | 218B | MoE | 2026-05-20 | 16:1 GQA with 3:1 sliding-window/global attention |
| 63 | Gemma 4 26B-A4B | 15.1% | 3.8B active | 25.2B | MoE | 2026-04-02 | 5:1 sliding-window/global GQA |
| 64 | GPT-OSS 20B | 17.1% | 3.6B active | 21B | MoE | 2025-08-04 | Alternating sliding-window/global GQA |
| 65 | LFM2.5 8B-A1B | 18.1% | 1.5B active | 8.3B | Hybrid MoE | 2026-05-28 | LIV convolution blocks plus GQA and MoE |
| 66 | JetBrains Mellum2 Thinking 12B-A2.5B | 20.8% | 2.5B active | 12B | MoE | 2026-06-01 | 3:1 sliding-window/full GQA |

**Caveat:** active parameter share is only one lens. It does not capture KV cache size, attention
pattern, context length, routing overhead, hardware efficiency, or training quality. But it is a helpful quick
check when comparing sparse models. For Qwen3.8-Flash-Next, the 4.8% ratio uses the 125B core and excludes the
additional 51B n-gram embedding and 4B MTP parameters. For Tencent Hy4-preview, the 6.4% ratio uses the 770B
backbone and excludes the additional 10B MTP layer.

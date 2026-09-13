---
title: "LLM 架构画廊 - 激活参数百分比"
title_en: "LLM Architecture Gallery - Percent Active Parameters"
source: https://sebastianraschka.com/llm-architecture-gallery/active-parameter-ratio/
crawled: 2026-09-06
translated: 2026-09-06
---

# LLM 架构画廊 - 激活参数百分比

> 原文：[LLM Architecture Gallery - Percent Active Parameters](https://sebastianraschka.com/llm-architecture-gallery/active-parameter-ratio/)

[返回画廊](https://sebastianraschka.com/llm-architecture-gallery/)

[sebastianraschka.com/llm-architecture-gallery/](https://sebastianraschka.com/llm-architecture-gallery/)

# 每个 token 的激活参数百分比

| # | 模型 | 激活比例 | 激活参数 | 总参数 | 类型 | 日期 | 注意力 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DeepSeek V4-Pro | 3.1% | 49B 激活 | 1.6T | MoE | 2026-04-24 | CSA/HCA |
| 2 | Kimi K2 | 3.2% | 32B 激活 | 1T | MoE | 2025-07-10 | MLA |
| 3 | Kimi K2.5 | 3.2% | 32B 激活 | 1T | MoE | 2026-01-27 | MLA |
| 4 | Kimi K2.6 | 3.2% | 32B 激活 | 1T | MoE | 2026-04-20 | MLA |
| 5 | Kimi K2.7 Code | 3.2% | 32B 激活 | 1T | MoE | 2026-06-12 | MLA |
| 6 | Arcee AI Trinity Large 400B | 3.3% | 13B 激活 | 400B | MoE | 2026-01-27 | 3:1 滑动窗口/全局门控 GQA |
| 7 | Kimi K3 | 3.7% | 104B 激活 | 2.8T | 混合 MoE | 2026-07-27 | 3:1 Kimi Delta Attention 和门控 MLA |
| 8 | Qwen3 Next 80B-A3B | 3.8% | 3B 激活 | 80B | 混合 | 2025-09-09 | 3:1 Gated DeltaNet 和门控注意力 |
| 9 | Xiaomi MiMo-V2.5-Pro 1.02T | 4.1% | 42B 激活 | 1.02T | MoE | 2026-04-22 | GQA，6:1 滑动窗口/全局注意力 |
| 10 | Motif 3 Beta | 4.1% | 13B 激活 | 314B | MoE | 2026-07-21 | GDLA，3:1 滑动窗口/完整注意力 |
| 11 | Ling 3.0 Flash | 4.1% | 5.1B 激活 | 124B | 混合 | 2026-08-04 | 5:1 Kimi Delta Attention 和门控 MLA |
| 12 | Inkling | 4.2% | 41B 激活 | 975B | MoE | 2026-07-15 | 5:1 滑动窗口/全局 GQA |
| 13 | Llama 4 Maverick | 4.3% | 17B 激活 | 400B | MoE | 2025-04-05 | GQA |
| 14 | MiniMax M2 230B | 4.3% | 10B 激活 | 230B | MoE | 2025-10-23 | GQA |
| 15 | MiniMax M2.5 230B | 4.3% | 10B 激活 | 230B | MoE | 2026-02-12 | GQA |
| 16 | Qwen3.5 397B | 4.3% | 17B 激活 | 397B | 混合 | 2026-02-16 | 3:1 Gated DeltaNet 和门控注意力 |
| 17 | MiniMax M2.7 230B | 4.3% | 10B 激活 | 230B | MoE | 2026-03-18 | GQA |
| 18 | GPT-OSS 120B | 4.4% | 5.1B 激活 | 117B | MoE | 2025-08-04 | 交替滑动窗口/全局 GQA |
| 19 | LongCat-Flash-Lite 68.5B-A3B | 4.4% | 3B 激活 | 68.5B | MoE | 2026-01-28 | MLA |
| 20 | DeepSeek V4-Flash | 4.6% | 13B 激活 | 284B | MoE | 2026-04-24 | CSA/HCA |
| 21 | Xiaomi MiMo-V2.5 310B | 4.8% | 15B 激活 | 310B | MoE | 2026-04-22 | 5:1 滑动窗口/全局注意力 |
| 22 | Qwen3.8-Flash-Next 125B-A6B | 4.8% | 6B 激活 | 125B 核心 | 混合 | 2026-08-26 | 3:1 Gated DeltaNet 和 Qwen Sparse Attention |
| 23 | Xiaomi MiMo-V2-Flash 309B | 4.9% | 15B 激活 | 309B | MoE | 2025-12-16 | 5:1 滑动窗口/全局注意力 |
| 24 | GLM-5 744B | 5.4% | 40B 激活 | 744B | MoE | 2026-02-11 | MLA 加 DeepSeek 稀疏注意力 |
| 25 | GLM-5.1 | 5.4% | 40B 激活 | 744B | MoE | 2026-04-07 | MLA 加 DeepSeek 稀疏注意力 |
| 26 | GLM-5.2 | 5.4% | 40B 激活 | 744B | MoE | 2026-06-17 | MLA 加 DeepSeek 稀疏注意力和 IndexShare |
| 27 | MiniMax M3 428B | 5.4% | 23B 激活 | 428B | MoE | 2026-06-13 | GQA 加 MiniMax 稀疏注意力 |
| 28 | DeepSeek V3 | 5.5% | 37B 激活 | 671B | MoE | 2024-12-26 | MLA |
| 29 | DeepSeek R1 | 5.5% | 37B 激活 | 671B | MoE | 2025-01-20 | MLA |
| 30 | DeepSeek V3.2 | 5.5% | 37B 激活 | 671B | MoE | 2025-12-01 | MLA 加 DeepSeek 稀疏注意力 |
| 31 | Step 3.5 Flash 196B | 5.6% | 11B 激活 | 196B | MoE | 2026-02-01 | 3:1 滑动窗口 GQA |
| 32 | Mistral Small 4 | 5.6% | 6.63B 激活 | 119B | MoE | 2026-03-16 | MLA |
| 33 | GLM-5.3-Flash | 5.6% | 18B 激活 | 320B | 混合 | 2026-08-26 | 3:1 Kimi Delta Attention 和 MLA/DSA |
| 34 | Solar Open 2 | 6% | 15B 激活 | 250B | 混合 | 2026-07-22 | 3:1 Kimi Delta Attention 和门控 GQA |
| 35 | Mistral Large 3 | 6.1% | 41B 激活 | 673B | MoE | 2025-12-02 | MLA |
| 36 | Kimi Linear 48B-A3B | 6.3% | 3B 激活 | 48B | 混合 | 2025-10-30 | 3:1 Kimi Delta Attention 和 MLA |
| 37 | Ling 2.5 1T | 6.3% | 63B 激活 | 1T | 混合 | 2026-02-15 | Lightning Attention 加 MLA |
| 38 | Ling 2.6 1T | 6.3% | 63B 激活 | 1T | 混合 | 2026-04-23 | Lightning Attention 加 MLA |
| 39 | Tencent Hy4-preview 770B-A49B | 6.4% | 49B 激活 | 770B | MoE | 2026-08-28 | 门控 MLA 加 DeepSeek 稀疏注意力和 IndexCache |
| 40 | Laguna S 2.1 | 6.8% | 8B 激活 | 118B | MoE | 2026-07-21 | 3:1 滑动窗口/全局门控 GQA |
| 41 | Tencent Hy3-preview 295B-A21B | 7.1% | 21B 激活 | 295B | MoE | 2026-04-23 | GQA |
| 42 | Sarvam 30B | 8% | 2.4B 激活 | 30B | MoE | 2026-03-03 | GQA |
| 43 | Qwen3.6 35B-A3B | 8.6% | 3B 激活 | 35B | 混合 | 2026-04-15 | 3:1 Gated DeltaNet 和门控注意力 |
| 44 | Ornith 1.5 35B-A3B | 8.6% | 3B 激活 | 35B | 混合 | 2026-08-23 | 3:1 Gated DeltaNet 和门控注意力 |
| 45 | GLM-4.5 355B | 9% | 32B 激活 | 355B | MoE | 2025-07-28 | GQA |
| 46 | GLM-4.7 355B | 9% | 32B 激活 | 355B | MoE | 2025-12-22 | GQA |
| 47 | ZAYA1-8B | 9% | 760M 激活 | 8.4B | MoE | 2026-05-06 | CCA 加 4:1 GQA |
| 48 | Laguna XS.2 | 9.1% | 3B 激活 | 33B | MoE | 2026-04-28 | 3:1 滑动窗口/全局门控 GQA |
| 49 | Laguna XS 2.1 | 9.1% | 3B 激活 | 33B | MoE | 2026-07-02 | 3:1 滑动窗口/全局门控 GQA |
| 50 | Qwen3 235B-A22B | 9.4% | 22B 激活 | 235B | MoE | 2025-04-28 | GQA |
| 51 | Sarvam 105B | 9.8% | 10.3B 激活 | 105B | MoE | 2026-03-03 | MLA |
| 52 | Qwen3 30B-A3B | 10% | 3B 激活 | 30B | MoE | 2025-04-28 | GQA |
| 53 | Nemotron 3 Nano 30B-A3B | 10% | 3B 激活 | 30B | 混合 MoE | 2025-12-04 | Mamba-2 + GQA |
| 54 | Nemotron 3.5 Lightning 30B-A3B | 10% | 3B 激活 | 30B | 混合 MoE | 2026-08-11 | Mamba-2 + GQA |
| 55 | Nemotron 3 Super 120B-A12B | 10% | 12B 激活 | 120B | 混合 MoE | 2026-03-11 | Mamba-2 + GQA |
| 56 | Nemotron 3 Ultra 550B-A55B | 10% | 55B 激活 | 550B | 混合 MoE | 2026-06-04 | Mamba-2 + GQA |
| 57 | North Mini Code 30B-A3B | 10% | 3B 激活 | 30B | MoE | 2026-06-05 | 8:1 GQA，3:1 滑动窗口/全局注意力 |
| 58 | Soofi S 30B-A3B | 10.1% | 3.2B 激活 | 31.6B | 混合 MoE | 2026-07-10 | Mamba-2 + GQA |
| 59 | Qwen3 Coder Flash 30B-A3B | 11% | 3.3B 激活 | 30B | MoE | 2025-07-31 | GQA |
| 60 | GLM-4.5-Air | 11.3% | 12B 激活 | 106B | MoE | 2025-07-28 | GQA |
| 61 | INTELLECT-3 | 11.3% | 12B 激活 | 106B | MoE | 2025-11-26 | GQA |
| 62 | Command A+ 218B-A25B | 11.5% | 25B 激活 | 218B | MoE | 2026-05-20 | 16:1 GQA，3:1 滑动窗口/全局注意力 |
| 63 | Gemma 4 26B-A4B | 15.1% | 3.8B 激活 | 25.2B | MoE | 2026-04-02 | 5:1 滑动窗口/全局 GQA |
| 64 | GPT-OSS 20B | 17.1% | 3.6B 激活 | 21B | MoE | 2025-08-04 | 交替滑动窗口/全局 GQA |
| 65 | LFM2.5 8B-A1B | 18.1% | 1.5B 激活 | 8.3B | 混合 MoE | 2026-05-28 | LIV 卷积块加 GQA 和 MoE |
| 66 | JetBrains Mellum2 Thinking 12B-A2.5B | 20.8% | 2.5B 激活 | 12B | MoE | 2026-06-01 | 3:1 滑动窗口/完整 GQA |

**注意：**激活参数占比只是观察模型的一个视角。它无法反映 KV 缓存大小、注意力模式、上下文长度、路由开销、硬件效率或训练质量。但在对比稀疏模型时，它是一个有用的快速检查手段。对于 Qwen3.8-Flash-Next，4.8% 的比例基于 125B 核心参数，未计入额外的 51B n-gram 嵌入和 4B MTP 参数。对于 Tencent Hy4-preview，6.4% 的比例基于 770B 主干，未计入额外的 10B MTP 层。

---
title: "Gemma 4 Architecture and Benchmark Notes"
source: https://sebastianraschka.com/blog/2026/gemma-4-release-notes.html
crawled: 2026-09-06
---

# Gemma 4 Architecture and Benchmark Notes

Flagship open-weight release days are always exciting. For Gemma 4, I started by putting the 31B configuration next to Gemma 3 27B. The family resemblance is easy to see, although there are a few long-context refinements worth separating from the parts that stayed the same.

The full [Gemma 4 family](https://ai.google.dev/gemma/docs/core/model_card_4) spans five sizes. This note focuses on the dense 31B model and the 26B-A4B mixture-of-experts variant. Both accept text and images. The smaller E2B, E4B, and 12B models cover somewhat different edge and multimodal use cases.

## The 31B text decoder

According to the [31B configuration](https://huggingface.co/google/gemma-4-31B-it/blob/main/config.json), the text decoder has 60 layers. Google lists the model at 30.7 billion parameters. The decoder’s embedding width is 5,376, and its feed-forward hidden dimension is 21,504. The vocabulary contains 262,144 tokens.

The attention schedule follows the familiar Gemma pattern. Five sliding-window layers are followed by one full-attention layer, repeated across the stack. This gives 50 local layers and 10 global layers. The final layer is global, and the local window covers 1,024 tokens.

Gemma 4 also keeps grouped-query attention, QK-Norm, and the unusual pre- and post-RMSNorm arrangement from Gemma 3. The local layers use 16 key-value heads. The global layers reduce that count to four, use unified keys and values, and apply proportional RoPE. The 256K [context window](https://sebastianraschka.com/glossary/#context-length "Context Length") is twice the 128K limit of Gemma 3 27B.

These are meaningful changes for long-context use, while the basic transformer block remains recognizable. Gemma 4 also ships with a dedicated draft model for multi-token prediction and speculative decoding. That auxiliary path is separate from the text-decoder diagram below.

The figure focuses on the language-model backbone. The complete 31B checkpoint includes a roughly 550M-parameter vision encoder for image input. It does not include the native audio encoder available in some smaller Gemma 4 variants.

## What the [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") jump tells us

The [Google model card](https://ai.google.dev/gemma/docs/core/model_card_4) reports a large improvement over Gemma 3 27B. Gemma 4 31B scores 85.2 on MMLU-Pro compared with 67.6 for Gemma 3. On LiveCodeBench v6, the reported scores are 80.0 and 29.1. GPQA Diamond moves from 42.4 to 84.3.

Those Gemma 4 results are close to the values in the [Qwen3.5-27B model card](https://huggingface.co/Qwen/Qwen3.5-27B) for several of the same benchmarks. Qwen reports 86.1 on MMLU-Pro, 80.7 on LiveCodeBench v6, and 85.5 on GPQA Diamond.

I would still treat this as a rough comparison. The Gemma and Qwen numbers come from their respective model providers rather than one independent evaluation harness. Google’s table also labels the Gemma 3 baseline as `no think`, whereas Gemma 4 has a configurable thinking mode. The chart therefore does not isolate architecture, data, [pretraining](https://sebastianraschka.com/glossary/#pretraining "Pretraining"), or post-training.

My guess is that the training data and recipe account for much of the improvement because the core decoder template changed less than the scores did. There is no ablation in the public release that lets us assign a percentage of the gain to one factor.

## The 26B-A4B [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") alternative

Gemma 4 also includes a [26B-A4B configuration](https://huggingface.co/google/gemma-4-26B-A4B-it/blob/main/config.json). It has 25.2 billion total parameters and uses about 3.8 billion for each token. Every MoE layer selects eight routed experts from a pool of 128 and also uses one shared expert.

The model has 30 decoder layers, arranged as 25 sliding-window and five global-attention layers. In other words, it keeps the same 5:1 attention schedule while replacing the dense feed-forward computation with sparse expert routing.

Its reported scores are only moderately below the dense 31B model on several tasks. MMLU-Pro is 82.6 versus 85.2, LiveCodeBench v6 is 77.1 versus 80.0, and GPQA Diamond is 82.3 versus 84.3. The practical attraction is lower active feed-forward compute, although the full expert weights still have to be stored.

I left the MoE architecture out of the main figure to keep it readable. Both models are available in the [LLM Architecture Gallery comparison](https://sebastianraschka.com/llm-architecture-gallery/?compare=gemma-4-31b,gemma-4-26b-a4b#architecture-diff-tool), and the [26B-A4B card](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-26b-a4b) links to its configuration and source material.

## License change

Gemma 4 is released under the [Apache License 2.0](https://ai.google.dev/gemma/docs/core/model_card_4). Gemma 3 used custom Gemma terms. Moving to a standard open-source license makes the usage conditions easier to evaluate for many research and commercial projects.

[![Gemma 4 31B architecture diagram and benchmark comparison](https://sebastianraschka.com/images/blog/2026/gemma-4-release-notes/hero.webp)](https://sebastianraschka.com/llm-architecture-gallery/?compare=gemma-4-31b,gemma-3-27b#architecture-diff-tool)

Figure 1. Gemma 4 31B keeps the 5:1 local-to-global attention schedule of Gemma 3 27B. The upper-right comparison shows the changed context length, layer recipe, and KV-cache estimate. The benchmark bars use provider-reported results rather than a shared evaluation run.

Source: expanded website version of my [Substack note](https://substack.com/@rasbt/note/c-237278550). For more detail, see the [Gemma 4 technical report](https://arxiv.org/abs/2607.02770).

---
title: "Muse Glimmer 30B Architecture Notes"
source: https://sebastianraschka.com/blog/2026/muse-glimmer-30b-architecture-notes.html
crawled: 2026-09-06
---

# Muse Glimmer 30B Architecture Notes

Whoa, Meta released a new open-weight LLM yesterday, something that hasn’t happened since the good old Llama days.

Their Meta Muse Glimmer model is a 30B multimodal reasoning model with a Gemma-like architecture design. (“Glimmer” is probably a wordplay on “Spark,” the more likely capable model from which Glimmer was distilled. Muse Spark is only available through Meta’s Model API, though.)

Architecture-wise, here are some of the main points:

1. “Only” a 131k context window, compared to Qwen3.6 and Gemma 4, which support 2x that natively; it’s reasonable, but maybe on the shorter end in the age of agent harnesses
2. It’s a dense model, not a mixture-of-experts. (So, it’s fairer to compare it to Qwen3.6 27B than Qwen3.6 30B-A3B.)
3. Hybrid attention with grouped-query attention (GQA) and sliding window attention (SWA); the SWA:GQA pattern is a 3:1 local:global ratio. Other models like Gemma 4, which uses similar components, have a 5:1 ratio for comparison.
4. It adopts gated attention for both GQA and SWA; gated attention has become quite common in recent months. It basically applies a sigmoid gate to the attention output to decide how much of the attention information enters the residual connection. The interesting point is that it uses relatively standard GQA and SWA rather than hybrid attention mechanisms such as Nemotron or Qwen3.6.
5. A very extreme GQA ratio: 32 query heads and only 2 KV heads; for comparison, Gemma 4 31B uses 32 Q / 16 KV in the local heads and 32 Q / 4 KV in the global heads. This means that Meta Glimmer has a very small KV cache.

Overall, the probably most similar architecture is Gemma 3 27B (including the Gemma-style pre/post RMSNorm placement) and Gemma 4 31B, but with some tweaks like SwiGLU instead of GeGLU activations, gated attention, and the more extreme GQA:SWA pattern mentioned before.

What stands out is its extreme KV-cache efficiency.

I.e., the KV CACHE / TOKEN ratios (in BF16) are:

- Muse Glimmer: 52 KiB (lower is better)
- Qwen3.6 27B: 64 KiB
- Gemma 4 31B: 840 KiB

Modeling-performance-wise, their own benchmarks show that it’s mostly ahead of Qwen3.6. According to the independent composite benchmarks on the Artificial Analysis Intelligence Index, it’s slightly behind Qwen3.6 (see figure below). So, a few days of using it will tell where it really ranks.

Overall, it looks like a solid model, particularly for agentic workflows. What stands out most is its very low memory footprint and also pretty fast prefill and decode speed. It’s also just great to see Meta releasing open weights again :).

![Composite figure showing the Meta Muse Glimmer 30B architecture, DGX Spark throughput and memory benchmarks, and the Artificial Analysis Agentic Index](https://sebastianraschka.com/images/blog/2026/muse-glimmer-30b-architecture-notes/muse-glimmer-30b.webp)

Figure 1. Meta Muse Glimmer 30B architecture, DGX Spark Ollama benchmarks, and the Artificial Analysis Agentic Index comparison. See [Muse Glimmer 30B](https://sebastianraschka.com/llm-architecture-gallery/#card-muse-glimmer-30b) in the architecture gallery for more details.

Source: website version of my [Substack note](https://substack.com/@rasbt/note/c-312570436).

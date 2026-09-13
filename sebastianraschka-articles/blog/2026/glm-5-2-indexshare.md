---
title: "GLM-5.2 IndexShare Architecture Note"
source: https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html
crawled: 2026-09-06
---

# GLM-5.2 IndexShare Architecture Note

[GLM-5.2](https://huggingface.co/zai-org/GLM-5.2) is a long-context update to Z.ai’s GLM-5 model family. It keeps most of the GLM-5 and GLM-5.1 architecture and adds a focused sparse-attention change called [IndexShare](https://sebastianraschka.com/glossary/#indexshare "IndexShare").

The inherited backbone is a large sparse mixture-of-experts model. According to the [GLM-5 technical report](https://arxiv.org/abs/2602.15763), this model family has 744 billion total parameters and activates about 40 billion per token. The [GLM-5.2 configuration](https://huggingface.co/zai-org/GLM-5.2/blob/main/config.json) lists 78 transformer layers with a hidden size of 6,144. The first three feed-forward blocks are dense. The remaining blocks use 256 routed experts, select 8 of them per token, and add one shared expert.

The attention stack combines [Multi-head Latent Attention](https://sebastianraschka.com/llm-architecture-gallery/mla/) with [DeepSeek Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/), or DSA. I covered that combination in more detail in my [DeepSeek V3 to V3.2 article](https://magazine.sebastianraschka.com/p/technical-deepseek). GLM-5.2 extends the configured [context length](https://sebastianraschka.com/glossary/#context-length "Context Length") from the earlier model’s 200K tokens to 1,048,576 tokens.

## Where the DSA indexer becomes expensive

DSA divides sparse attention into selection and computation. A lightweight indexer scores the earlier tokens for each query position and selects the top 2,048. The main attention operation then works on this selected subset.

If the sequence length is (L) and the number of selected tokens is (k), the core sparse attention scales as (O(Lk)). The indexer still compares each query with all preceding positions, so its scaling remains quadratic in (L). It is much cheaper per operation than the main attention module, but at very long context lengths the repeated indexer work across many layers becomes noticeable.

The [IndexCache study](https://arxiv.org/abs/2603.12201) measured 70% to 100% overlap between token selections in adjacent DSA layers. This means that nearby indexers often rediscover many of the same positions.

## What IndexShare reuses

IndexShare runs an indexer in one layer and reuses its selected token positions in three nearby layers. The repeating pattern is `full, shared, shared, shared`, after a few initial exceptions in the released configuration. Here, `full` means that the layer runs its own DSA indexer. It does not mean dense attention over the full context.

The shared layers still compute their own queries, attention weights, value combinations, output projections, and feed-forward updates. They reuse only the list of selected positions. This distinction is important because the hidden states and attention outputs continue to change from one layer to the next.

Z.ai introduced this pattern during continued mid-training with 128K-token sequences. Training with the reuse pattern gives each retained indexer a chance to adapt to the neighboring layers that depend on it. This differs from adding a cache to an already trained model at inference time.

The release reports a 2.9-fold reduction in per-token FLOPs at a one-million-token context. This is a compute estimate for the architecture at that context length. It should not be read as a 2.9-fold end-to-end speedup. Z.ai also notes that IndexShare does not reduce KV-cache memory in the same proportion. At one million tokens, cache capacity, long-context kernels, CPU scheduling, and cache transfers remain substantial serving costs.

The related IndexCache paper helps put this result in context. On a separate 30B DSA model at 200K tokens, retaining one quarter of the indexers produced up to a 1.82-fold prefill speedup and a 1.48-fold decode speedup. Those measurements use a different model and context length, so they are evidence for the reuse idea rather than direct GLM-5.2 latency numbers.

## Reuse in the MTP layer

The same release also changes the multi-token prediction layer used for speculative decoding. Its first draft step computes the indices, and later draft steps reuse both those indices and the earlier [KV cache](https://sebastianraschka.com/glossary/#kv-cache "KV Cache"). Z.ai combines this with rejection sampling and an end-to-end total-variation loss.

In the reported ablation, the complete set of MTP changes raises the average accepted draft length from 4.56 to 5.47 tokens, a 20% increase. The table adds the changes cumulatively, so it does not isolate how much of the final gain comes from IndexShare alone.

The local [IndexShare explainer](https://sebastianraschka.com/llm-architecture-gallery/indexshare/) includes a compact pseudocode version of the four-layer pattern. The [GLM-5.2 architecture card](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-2) tracks the model configuration, license, attention mechanism, and current [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") references.

[![GLM-5.2 architecture and benchmark overview](https://sebastianraschka.com/images/blog/2026/glm-5-2/hero.webp)](https://substack.com/@rasbt/note/c-278515750)

Figure 1: The upper panel shows GLM-5.2's inherited [MLA](https://sebastianraschka.com/glossary/#mla "Multi-Head Latent Attention (MLA)"), DSA, and sparse MoE structure. IndexShare changes how often DSA selects token positions. The lower panel preserves the release-time Artificial Analysis benchmark snapshot.

## Reading the benchmark snapshot

At release time, the [Artificial Analysis Coding Index](https://artificialanalysis.ai/) snapshot below placed GLM-5.2 at 68.8 and Claude Opus 4.8 (max) at 56.7. Z.ai’s own results also showed substantial gains over GLM-5.1, including 81.0 versus 63.5 on Terminal-Bench 2.1 and 62.1 versus 58.4 on SWE-bench Pro.

I would treat these as dated evaluation snapshots. Leaderboards, model providers, and harnesses change, and the Z.ai benchmark table uses task-specific context limits, prompts, and agent frameworks. The architectural claim is narrower and easier to evaluate: GLM-5.2 removes three quarters of the repeated DSA indexer calls in its regular four-layer groups while preserving sparse attention in every layer.

![Artificial Analysis Coding Index chart comparing GLM-5.2 and Claude Opus 4.8](https://sebastianraschka.com/images/blog/2026/glm-5-2/artificial-analysis-coding-index.webp)

Figure 2: Artificial Analysis Coding Index snapshot captured around the GLM-5.2 release. The values document that point in time and should not be interpreted as a permanent model ranking.

Sources: expanded website version of my [Substack note](https://substack.com/@rasbt/note/c-278515750), based on the [GLM-5.2 release post](https://huggingface.co/blog/zai-org/glm-52-blog), [model configuration](https://huggingface.co/zai-org/GLM-5.2/blob/main/config.json), [GLM-5 technical report](https://arxiv.org/abs/2602.15763), and [IndexCache paper](https://arxiv.org/abs/2603.12201).

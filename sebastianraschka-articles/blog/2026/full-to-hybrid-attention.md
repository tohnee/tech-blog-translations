---
title: "From Full to Hybrid Attention in LLMs"
source: https://sebastianraschka.com/blog/2026/full-to-hybrid-attention.html
crawled: 2026-11-16
---

# From Full to Hybrid Attention in LLMs

Currently working towards a bigger open LLM roundup. But in the meantime, just one of the interesting trends that stood out. I.e., looks like the transition from full to hybrid attention continues.

In 2025, there were still lots of full attention models, with a shift to “some full attention” hybrids.

In the first half of 2026, the trend towards “some full attention” hybrids continued.

And now, in the second half of 2026, we have a 50/50 split between “some full attention” hybrids and models that don’t use full attention at all anymore. And yes, there are also no full attention models anymore.

The plot legend here means,

* Full attention throughout = Global MHA, GQA, dense MLA, CCA in EVERY layer.
* Some full attention = Full global attn mixed with: sliding-window/chunked attention, Gated DeltaNet, KDA, Mamba-2, Lightning Attention, convolutions, sparse attention.
* No full attention = Zero dense global layers.

The main implication is that the trend goes towards making long contexts cheaper to use. This means, it makes the architectures more suitable for long documents and conversations, large code bases, and of course agent use cases that rely on a lot of tool calls.

In particular, there are two distinct efficiency gains here:

1. Less attention computation, since sparse attention and the like select tokens or blocks from the context and perform the expensive attention operation from only that subset. (Note that it can still retrieve information from distant positions.)
2. Less memory for retaining context in some architectures, meaning that recurrent layers such as Gated DeltaNet maintain a fixed-size state. Of course, this saves memory, but compressing the history creates challenges for exact retrieval, so they are usually intermixed with traditional attention methods (sparse or full).

[![Architecture diagrams for Mistral Small 4, Kimi K3, and MiniMax-M3.1-Flash above stacked bars comparing full-attention coverage across three groups of model releases](/images/blog/2026/full-to-hybrid-attention/full-to-hybrid-attention.webp)](/images/blog/2026/full-to-hybrid-attention/full-to-hybrid-attention.png)

Shares of models with full attention throughout, some full attention, or no full attention, with architecture examples from the [LLM Architecture Gallery](/llm-architecture-gallery/). Click the figure to view the full-resolution image.

Source: lightly edited website version of my [Substack note](https://substack.com/@rasbt/note/c-383850419).

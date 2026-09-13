---
title: "Layer-wise attention budgeting"
source: https://sebastianraschka.com/llm-architecture-gallery/attention-budgeting/
crawled: 2026-09-06
---

# Layer-wise attention budgeting

Layer-wise attention budgeting means varying the attention cost by layer instead of giving every transformer layer the same full attention budget. One recent example is Laguna XS.2, the first open-weight model by [Poolside](https://poolside.ai/), a Europe-based company focused on training LLMs for coding applications. Several of my former colleagues joined Poolside in recent years, and they have a great team with lots of talent. It’s just nice to see more companies also releasing some of their models as open-weight variants.

Anyways, the Laguna XS.2 architecture depicted below looks very standard at first glance. However, one detail that I didn’t show (/try to cram into there) is a concept we can refer to as “layer-wise attention budgeting”.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Article section](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A73-layer-wise-attention-budgeting-laguna-xs2)
[Laguna config](https://huggingface.co/poolside/Laguna-XS.2/blob/main/config.json#L142)

![Laguna XS.2 architecture](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/laguna-xs2-architecture.webp)

Figure 9: Poolside's Laguna XS.2 architecture. (Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

## Where the budgeting happens

Laguna has 40 layers, but they don’t all use the same attention setup. Thirty are sliding-window layers, where each token can look back over a local window of 512 tokens. The other ten use full attention and can access the whole context. These global layers are more expensive, whereas the sliding-window layers keep the KV cache and attention computation cheaper.

This mixed sliding-window and full-attention pattern isn’t unique to Laguna XS.2. Gemma 4, for example, uses both types as well.

But what’s new is the use of per-layer query-head counts. The Hugging Face [`config.json`](https://huggingface.co/poolside/Laguna-XS.2/blob/main/config.json#L142) includes a `num_attention_heads_per_layer` setting, so the number of query heads can change while the KV-cache shape stays compatible.

![Per-layer query-head budgeting in Laguna XS.2](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/laguna-xs2-attention-budgeting.webp)

Figure 10: Per-layer query-head budgeting in Laguna. Full-attention layers use 6 query heads per KV head,
while sliding-window layers use 8 query heads per KV head. (Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

## The head counts

The full-attention layers use 48 query heads. Sliding-window layers get 64. Both keep the KV-head count fixed at 8, which works out to 6 query heads per KV head for full attention and 8 for sliding-window attention.

That’s the layer-wise head budgeting encoded in Laguna’s config.

## Why vary the budget?

The broader idea of varying model capacity by layer goes back to (at least) Apple’s 2024 [OpenELM](https://arxiv.org/abs/2404.14619). And again, what’s the point of such a design?

Similar to KV sharing, the point is to spend attention capacity where it is most useful instead of giving every layer the same budget. Full-attention layers look across the whole context, so Laguna gives them fewer query heads than the cheaper sliding-window modules.

(Besides, another smaller implementation detail is that Laguna also applies per-head attention-output gating; this is somewhat similar to Qwen3-Next and others, which I omit here since I covered it in earlier articles.)

Sources

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A73-layer-wise-attention-budgeting-laguna-xs2)
[Laguna XS.2 config.json](https://huggingface.co/poolside/Laguna-XS.2/blob/main/config.json#L142)
[Poolside Laguna deep dive](https://poolside.ai/blog/laguna-a-deeper-dive)
[OpenELM](https://arxiv.org/abs/2404.14619)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)

---
title: "Kimi K3 Architecture Notes"
source: https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html
crawled: 2026-09-06
---

# Kimi K3 Architecture Notes

The Kimi K3 architecture figure for yesterday’s big open-weight model release, along with some observations and thoughts.

1. Yes, it looks relatively complicated, but it’s essentially a scaled-up production version of their [Kimi Linear model](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-linear-48b-a3b) they released last year (scaled up from 48B -> 2.8T; K3 is by far the biggest open-weight model right now)
2. The one new component compared to Kimi Linear is the [LatentMoE](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/). I omitted it in the figure below since it’s already very crowded, but that’s essentially the same LatentMoE as in Nemotron 3 Ultra (you can find it in my [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) if you are curious). The idea here is to compress (down-project) large linear layers similar to [multi-head latent attention](https://sebastianraschka.com/llm-architecture-gallery/mla/).
3. Kimi K3’s overall trend (similar to Nemotron 3, DeepSeek V4, and others) is also towards better inference efficiency. That is, there are many components that replace existing components with efficiency-tweaked versions. I.e., [MoE](https://sebastianraschka.com/llm-architecture-gallery/moe/) -> LatentMoE, regular attention -> multi-head latent attention and [Kimi Delta Attention](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/). (I also have short tutorials and write-ups in my [gallery](https://sebastianraschka.com/llm-architecture-gallery/) if you are curious about additional details).
4. The one component change that is not an efficiency tweak is [attention residuals](https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/). Like DeepSeek V4 improved the residual path with mHC (manifold-constrained Hyper-Connections), attention residuals are a way to improve the residual path, but it works a bit differently. I.e., mHC made the residual path wider. Attention residuals (also already part of Kimi Linear) connect the residuals across layers; the connection itself uses an attention score for an important/contribution weight. According to the report, it improves the validation loss and downstream performance (a bit) consistently and adds about 4% in training cost and 2% in inference cost.
5. Interestingly, Kimi K3 got rid of all RoPE layers and uses [NoPE](https://sebastianraschka.com/llm-architecture-gallery/nope/) (No Positional Embeddings) everywhere instead. (Again, this is inherited from Kimi Linear). In other architectures, the recent trend was towards RoPE in local attention layers (like [sliding window attention](https://sebastianraschka.com/llm-architecture-gallery/swa/)) and NoPE in the global layers. There were a few architectures that only used NoPE everywhere, but this is the first frontier-level one as far as I know.
6. Kimi K3 now also has native multimodal support, which is great!

There are several other interesting training tidbits in the technical report, but that’s it from the architecture front so far. A really great release overall.

![Composite Kimi K3 architecture diagram with Kimi Delta Attention, gated multi-head latent attention, Attention Residuals, LatentMoE, and benchmark comparisons](https://sebastianraschka.com/images/blog/2026/kimi-k3-architecture-notes/kimi-k3-architecture.webp)

Figure 1. Kimi K3 architecture and release-time benchmark comparisons. See [K3](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k3) in the architecture gallery for more details.

Source: website version of my [Substack note](https://substack.com/@rasbt/note/c-303378576).

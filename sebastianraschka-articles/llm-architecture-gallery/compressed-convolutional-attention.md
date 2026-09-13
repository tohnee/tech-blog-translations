---
title: "Compressed convolutional attention"
source: https://sebastianraschka.com/llm-architecture-gallery/compressed-convolutional-attention/
crawled: 2026-09-06
---

# Compressed convolutional attention

Compressed Convolutional Attention (CCA) performs the attention operation directly in a compressed latent space. ZAYA1-8B uses it together with grouped-query attention.

Similar to Laguna, ZAYA1-8B is another new player on the open-weight market. It is developed by [Zyphra](https://www.zyphra.com/post/zaya1-8b), and one of the interesting details around the release is that the model was trained on AMD GPUs rather than the more common NVIDIA GPU (or Google TPU) setup.

The main architecture detail, though, is CCA, used together with grouped-query attention. Unlike MLA-style designs that mainly use a latent representation as a compact KV-cache format, CCA performs the attention operation directly in the compressed latent space, but more on that later.

(Sidenote: the ZAYA1-8B [`config.json`](https://huggingface.co/Zyphra/ZAYA1-8B/blob/main/config.json) lists 80 alternating layer entries rather than 40 conventional transformer blocks. These entries alternate between CCA/GQA attention and MoE feed-forward layers. But for the architecture figure, it is more convenient to visualize this as 40 repeated attention plus MoE pairs, which is conceptually equivalent.)

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Article section](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A74-compressed-convolutional-attention-zaya1-8b)
[CCA paper](https://arxiv.org/abs/2510.04476)
[ZAYA1 config](https://huggingface.co/Zyphra/ZAYA1-8B/blob/main/config.json)

![ZAYA1-8B architecture with compressed convolutional attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/zaya1-cca-architecture.webp)

Figure 11. ZAYA1-8B with transformer blocks featuring compressed convolutional attention. (Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

## What is compressed convolutional attention?

As hinted at in the figure above, ZAYA1-8B uses CCA together with a 4:1 GQA layout. The key point is that its attention block is built around CCA rather than a standard sliding-window attention block.

I would say CCA is related in spirit to [Multi-head Latent Attention (MLA)](https://sebastianraschka.com/llm-architecture-gallery/mla/) in DeepSeek’s models, since both introduce a compressed latent representation into the attention block. However, they use that latent space differently. MLA mainly uses the latent representation to reduce the KV cache. In MLA, the KV tensors are stored compactly and then projected into the attention-head space for the actual attention computation.

![Multi-head latent attention and compressed convolutional attention side by side](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/zaya1-cca-mla-comparison.webp)

Figure 13. Multi-head Latent Attention (MLA) and Compressed Convolutional Attention (CCA) side by side.
(Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

## Where the convolution comes in

CCA compresses Q, K, and V and performs the attention operation directly in the compressed latent space. This is why CCA can reduce not only KV-cache size, but also attention FLOPs during prefill and training.

As Figure 13 illustrates, in CCA, the compressed latent representations enter the attention mechanism directly, and the resulting compressed attention vector is then up-projected.

Note that this is called Compressed Convolutional Attention, not just Compressed Attention, since there is an additional convolutional mixing happening on the latent K and Q representations. The convolutional mixing part is not shown in Figure 13, because it would have been too crammed, but it’s relatively straightforward.

As hinted at in Figure 13, the convolutional mixing happens directly on the compressed Q and K tensors. The point is that compression makes Q, K, and V narrower, which saves compute and cache, but it can also make attention less expressive. The convolutions are a cheap way to give the compressed Q and K vectors more local context before they are used to compute attention scores. (The convolutional mixing is only applied to Q and K, not V, because Q and K determine the attention scores, while V represents the content that gets averaged via these scores.)

![Sequence-mixing convolution on compressed queries and keys](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/zaya1-cca-convolutional-mixing.webp)

Figure 14. Conceptual overview of the sequence-mixing convolution. (Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

Next to the sequence mixing shown in Figure 14, there is also a channel-mixing component. It’s similar in principle, so I am omitting the illustration.

## What the paper reports

CCA appears to be a Zyphra-introduced attention mechanism that predates the ZAYA1-8B technical report. The standalone CCA paper, [Compressed Convolutional Attention: Efficient Attention in a Compressed Latent Space](https://arxiv.org/abs/2510.04476), was first posted in October 2025 and explicitly introduces CCA. ZAYA1-8B then uses this mechanism as one of its core pieces.

But the question is, “is it better than MLA”? According to the CCA paper’s own experiments, yes, they report CCA outperforming MLA under comparable compression settings.

Overall, the interesting part here is really the new attention mechanism. The model also uses a pretty extreme (= very sparse) MoE setup, with only one routed expert active per token, but that part is more familiar. CCA is more unusual because it performs the attention operation directly in a compressed latent space, and then uses convolutional mixing on the compressed Q and K representations to make this compressed attention less limiting. So, in short, ZAYA1-8B is not only trying to save compute in the feed-forward layers, but also in the attention mechanism itself.

Sources

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A74-compressed-convolutional-attention-zaya1-8b)
[Compressed Convolutional Attention paper](https://arxiv.org/abs/2510.04476)
[ZAYA1-8B technical report](https://arxiv.org/abs/2605.05365)
[ZAYA1-8B config.json](https://huggingface.co/Zyphra/ZAYA1-8B/blob/main/config.json)
[Zyphra ZAYA1-8B post](https://www.zyphra.com/post/zaya1-8b)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)

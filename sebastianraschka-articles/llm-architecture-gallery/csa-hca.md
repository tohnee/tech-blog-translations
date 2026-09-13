---
title: "CSA and HCA"
source: https://sebastianraschka.com/llm-architecture-gallery/csa-hca/
crawled: 2026-09-06
---

# CSA and HCA

Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA) reduce long-context costs by shortening the stored history. They pool groups of older tokens into fewer key-value (KV) entries. The attention layers then have fewer past entries to store and process.

The two mechanisms work at different compression rates and use different lookup strategies. CSA preserves more entries and reads a sparse selection. HCA makes the history much shorter and reads all of its compressed entries. [DeepSeek V4](https://arxiv.org/abs/2606.19348) combines both approaches for context lengths of up to one million tokens.

This sequence compression complements [Multi-Head Latent Attention (MLA)](https://sebastianraschka.com/llm-architecture-gallery/mla/). MLA makes the cached representation for each token smaller. It still retains one latent entry per token. CSA and HCA also reduce the number of entries along the sequence axis.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Article section](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A752-compressed-attention-via-csa-and-hca)
[DeepSeek V4 report](https://arxiv.org/abs/2606.19348)
[MLA explainer](https://sebastianraschka.com/llm-architecture-gallery/mla/)

![MLA-style cache, CSA, and HCA compared conceptually](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-csa-hca-cache-comparison.webp)

Figure 1. MLA makes each token's stored representation smaller. CSA and HCA also shorten the sequence
of stored entries. CSA combines moderate compression with sparse top-k selection, while HCA combines
stronger compression with dense attention over the resulting cache. (Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

What changes

Past tokens are summarized into fewer compressed KV entries

Practical benefit

The long-context cache becomes shorter, reducing memory and attention cost

Example architectures

[DeepSeek V4-Pro](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v4-pro) and
[DeepSeek V4-Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v4-flash)

## Compressing the sequence axis

A KV cache has two relevant sizes here. One is the width of the representation stored for each token. The other is the number of token positions kept in the cache. MLA primarily addresses the first. CSA and HCA address the second.

Suppose a model has processed a long document. A conventional cache gives every earlier token its own entry. With sequence compression, a block of neighboring tokens contributes to one compressed entry. This loses some fine-grained history, but it directly reduces the cache length and the number of locations considered during attention.

DeepSeek V4 applies this idea at two scales. CSA compresses every 4 token positions into one entry. A top-k indexer then chooses a sparse subset of these entries for attention. HCA compresses 128 positions into one entry. Since this leaves a far shorter history, the layer can attend densely over all compressed entries.

![CSA sparse selection and HCA dense attention over compressed history](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-csa-hca-attention-paths.webp)

Figure 2. CSA selects a sparse set of compressed history blocks. HCA attends densely over a smaller set
of more heavily compressed blocks. Both mechanisms retain a 128-token local window with uncompressed
KV entries for recent tokens. (Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

## Why use two compression rates?

CSA keeps a relatively detailed version of the older context. Its sparse lookup controls the cost of searching that history. HCA keeps a much coarser summary, so dense attention becomes affordable. The two paths give the model access to different resolutions of the same long sequence.

Recent tokens receive separate treatment. Both mechanisms include a 128-token local window with uncompressed KV entries. The model can therefore inspect the newest context at token-level resolution while using compressed summaries for distant text.

DeepSeek V4 interleaves CSA and HCA layers across the network. This avoids committing every layer to the same balance between retained detail and attention cost.

![DeepSeek V4 reported 1M-context FLOP and KV-cache savings](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-csa-hca-efficiency.webp)

Figure 3. Reported 1M-context efficiency numbers from the DeepSeek V4 paper, relative to DeepSeek V3.2.
DeepSeek V4-Pro is reported at 27% of the single-token inference FLOPs and 10% of the KV-cache size;
DeepSeek V4-Flash is reported at 10% of the FLOPs and 7% of the KV-cache size (Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

## How the pieces fit together

DeepSeek V4 combines sequence compression with MLA-style compact representations and shared-KV attention. The gallery uses the shorthand “MLA-style CSA/HCA” for this combination. MLA reduces the size of each entry, and CSA/HCA reduce how many historical entries remain.

CSA/HCA belong to the attention mechanism. [Manifold-Constrained Hyper-Connections (mHC)](https://sebastianraschka.com/llm-architecture-gallery/mhc/) address another part of the model. They change how information travels through the residual paths around attention and mixture-of-experts sublayers.

## Efficiency and limits

At a one-million-token context length, the DeepSeek V4 report compares both model variants with DeepSeek V3.2. DeepSeek V4-Pro uses 27% of the single-token inference FLOPs and 10% of the KV-cache size in that comparison. The corresponding figures for DeepSeek V4-Flash are 10% and 7%.

These savings have a clear cost. Older text is represented through compressed blocks, so some token-level detail disappears. HCA makes the sharper tradeoff because each entry summarizes a much larger block.

I would read the reported efficiency values as whole-model results. DeepSeek V4 also changes the training data, optimization method, residual connections, numerical precision, and system implementation. The comparison shows what the full design achieves. It does not isolate how much of the gain comes from CSA or HCA alone.

Sources

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A752-compressed-attention-via-csa-and-hca)
[DeepSeek V4 technical report](https://arxiv.org/abs/2606.19348)
[MLA explainer](https://sebastianraschka.com/llm-architecture-gallery/mla/)
[DeepSeek Sparse Attention explainer](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)
[A Visual Guide to Attention Variants](https://magazine.sebastianraschka.com/p/visual-attention-variants)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)

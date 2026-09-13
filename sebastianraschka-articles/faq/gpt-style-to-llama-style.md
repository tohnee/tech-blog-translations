---
title: "Architectural Changes from GPT-Style to Llama-Style Models"
source: https://sebastianraschka.com/faq/docs/gpt-style-to-llama-style.html
crawled: 2026-09-06
---

# Architectural Changes from GPT-Style to Llama-Style Models

Llama kept the basic GPT-style decoder and changed several components inside it. The token embeddings, causal transformer blocks, residual paths, next-token objective, and vocabulary output layer all remain. The main substitutions are RMSNorm, RoPE, SwiGLU, bias-free linear layers, and, in later variants, grouped-query attention.

For this comparison, “GPT-style” refers to the documented GPT-2 design rather than recent proprietary GPT models whose block-level details are not public.

![The repo's implementation follows the progression from a GPT-2-style decoder to Llama 2 and Llama 3 while keeping the same autoregressive transformer backbone](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

GPT-2 uses LayerNorm in its pre-normalization residual blocks. Llama replaces it with [RMSNorm](https://sebastianraschka.com/faq/docs/rmsnorm-vs-layernorm.html), which rescales activations by their root-mean-square magnitude and omits LayerNorm’s mean-centering operation. This is a small simplification repeated before every attention and feed-forward sublayer.

Position handling changes more visibly. GPT-2 learns one absolute position vector for each slot in its context window and adds that vector to the token embedding. Llama uses [rotary position embeddings](https://sebastianraschka.com/faq/docs/rope-vs-absolute-positional-embeddings.html), or RoPE, to rotate query and key vectors inside attention. The attention score then carries structured information about the distance between token positions. RoPE also avoids a learned input position table, although extending a model far beyond its trained context still requires care.

The feed-forward block changes from a GELU MLP to [SwiGLU](https://sebastianraschka.com/faq/docs/swiglu-modern-llms.html). A SwiGLU block computes a content projection and a gate, applies the SiLU activation to the gate, and multiplies the two paths before projecting back to the model width. Implementations adjust the intermediate dimension so that this extra gated path does not simply inflate the parameter count.

Llama also removes the learned bias vectors from most linear projections. This saves relatively few parameters compared with the weight matrices, but the omission is applied consistently throughout the stack. The [bias-term FAQ](https://sebastianraschka.com/faq/docs/bias-terms-modern-llms.html) discusses this choice in more detail.

The attention transition happened in stages. GPT-2 gives every query head its own key and value head. Llama 2 7B and 13B kept this standard multi-head attention design, while Llama 2 70B used [grouped-query attention](https://sebastianraschka.com/faq/docs/grouped-query-attention.html). Llama 3 uses GQA across its main model sizes. GQA retains multiple query heads while sharing fewer key and value heads, which reduces the KV cache during generation.

![The wider GPT and Llama comparison shows that the residual decoder stack stays recognizable while normalization, position handling, feed-forward layers, and attention sharing change across generations](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt-and-all-llamas.webp)

Tokenizer and vocabulary changes matter as well, although they sit outside the transformer block. Llama 3 expanded the vocabulary substantially compared with Llama 2 and GPT-2. That affects tokenization efficiency and the size of the embedding and output layers.

These architectural substitutions can change memory use, optimization, and inference cost. They do not explain model quality by themselves. Llama also differs from GPT-2 in scale, training data, context-length training, and the post-training recipe. A fair implementation comparison should keep those factors separate from the transformer-block design.

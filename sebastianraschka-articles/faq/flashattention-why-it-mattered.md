---
title: "How FlashAttention Speeds Up LLM Training"
source: https://sebastianraschka.com/faq/docs/flashattention-why-it-mattered.html
crawled: 2026-09-06
---

# How FlashAttention Speeds Up LLM Training

The original [FlashAttention paper](https://arxiv.org/abs/2205.14135) describes an IO-aware algorithm for exact scaled dot-product attention. Its main contribution is a different execution order that reduces reads and writes between the GPU’s high-bandwidth memory and its much smaller, faster on-chip memory.

In a straightforward implementation, attention first computes the score matrix \(QK^\top\). For a sequence of length \(n\), this matrix contains \(n^2\) entries for each attention head. The implementation then applies masking and softmax before multiplying the probabilities by \(V\). Writing these intermediates to GPU memory and reading them back can consume more time than the arithmetic itself.

FlashAttention splits the inputs into tiles that fit into on-chip memory. It computes one block of scores at a time and uses an online softmax procedure to maintain the running maximum and normalization terms. The output is accumulated block by block, so the complete score and probability matrices do not have to be stored in high-bandwidth memory.

![The multi-head attention benchmark figures in the repo compare faster PyTorch attention paths against the simpler from-scratch baseline](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/mha-benchmark/mha-comparison.webp)

The backward pass follows the same memory-conscious idea. It can recompute attention tiles from saved normalization statistics rather than storing the full probability matrix from the forward pass. This exchanges some arithmetic for a much smaller activation-memory footprint.

This is still standard attention. FlashAttention does not introduce sparsity, change the attention pattern, or approximate the softmax. Small numerical differences can arise from floating-point operation order, as they can with other optimized kernels.

The arithmetic complexity also remains quadratic in sequence length. FlashAttention removes the need to materialize an \(n \times n\) attention matrix in high-bandwidth memory, which greatly improves practical memory use. It does not make full attention a linear-time operation. Long contexts can therefore remain expensive even when they fit in memory.

![FlashAttention appears in the repo's optimization summary as a major turning point for both throughput and reserved memory](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

The repo’s training-speed experiments show the practical effect. Replacing a from-scratch attention implementation with PyTorch’s optimized path produced a large throughput increase and a substantial drop in reserved memory. The gain becomes especially relevant as sequence length and batch size grow.

In current PyTorch versions, `scaled_dot_product_attention` can dispatch to a FlashAttention-style backend when the device, data type, head dimension, and other settings are supported. A benchmark should confirm which backend actually ran, since an unsupported configuration may fall back to another implementation.

The largest benefits usually appear during training and long-prompt prefill, where many query positions are processed together. Token-by-token decoding has one new query at a time and is often limited by reading the KV cache, so its performance profile is different.

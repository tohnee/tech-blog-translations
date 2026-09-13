---
title: "DeepSeek Sparse Attention From Scratch"
source: https://sebastianraschka.com/blog/2026/deepseek-sparse-attention-from-scratch.html
crawled: 2026-09-06
---

# DeepSeek Sparse Attention From Scratch

I added a [DeepSeek Sparse Attention](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/09_dsa) from-scratch implementation to the LLMs-from-scratch repository, thanks to an excellent reader contribution.

The folder includes a README, a standalone GPT-style reference implementation, and tests:

1. [README.md](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/09_dsa/README.md)
2. [gpt\_with\_kv\_dsa.py](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/09_dsa/gpt_with_kv_dsa.py)
3. [test\_dsa.py](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/09_dsa/test_dsa.py)

The main idea behind [DeepSeek Sparse Attention](https://sebastianraschka.com/glossary/#deepseek-sparse-attention "DeepSeek Sparse Attention") is to replace a fixed sparse pattern with a learned sparse pattern. Instead of using only a local window, the mechanism uses a lightweight indexer and selector to decide which prior tokens are worth attending to.

For more background, I also have a local [DeepSeek Sparse Attention concept page](https://sebastianraschka.com/llms-from-scratch/ch04/15_deepseek_sparse_attention/) and a [gallery explainer](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/) that compare it with regular [causal attention](https://sebastianraschka.com/glossary/#causal-attention "Causal Attention") and sliding-window attention.

[![DeepSeek Sparse Attention implementation overview](https://sebastianraschka.com/images/blog/2026/deepseek-sparse-attention/hero.webp)](https://substack.com/@rasbt/note/c-264003632)

Screenshot from the original [Substack note](https://substack.com/@rasbt/note/c-264003632), showing the DeepSeek Sparse Attention implementation folder and README overview.

Source: lightly edited website version of my [Substack note](https://substack.com/@rasbt/note/c-264003632).

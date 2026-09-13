---
title: "Grouped-Query Attention (GQA)"
source: https://sebastianraschka.com/llm-architecture-gallery/gqa/
crawled: 2026-09-06
---

# Grouped-Query Attention (GQA)

Grouped-query attention is an attention variant derived from standard multi-head attention. It was introduced in the 2023 paper [*GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*](https://arxiv.org/abs/2305.13245) by Joshua Ainslie and colleagues.

Unlike MHA, where each head has its own set of keys and values, GQA groups multiple query heads to share the same key and value projections. This reduces how many keys and values have to be stored and retrieved from the [KV cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms) during inference.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[From-scratch code](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa)

![Comparison between multi-head attention and grouped-query attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-mha-vs-gqa.webp)

A comparison between MHA and GQA. Here, the group size is 2, where a key and value pair is shared among
2 query heads (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

What changes

Several query heads share the same key and value projections

Why use it

Fewer K/V heads make the [KV cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms) smaller and reduce memory bandwidth use

Example architectures

Dense:
[Llama 3 8B](https://sebastianraschka.com/llm-architecture-gallery/#card-llama-3-8b),
[Qwen3 4B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-4b),
[Gemma 3 27B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-3-27b),
[Mistral Small 3.1 24B](https://sebastianraschka.com/llm-architecture-gallery/#card-mistral-small-3-1-24b),
[SmolLM3 3B](https://sebastianraschka.com/llm-architecture-gallery/#card-smollm3-3b), and
[Tiny Aya 3.35B](https://sebastianraschka.com/llm-architecture-gallery/#card-tiny-aya-3-35b).
  
Sparse:
[Llama 4 Maverick](https://sebastianraschka.com/llm-architecture-gallery/#card-llama-4-maverick),
[Qwen3 235B-A22B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-235b-a22b),
[Step 3.5 Flash 196B](https://sebastianraschka.com/llm-architecture-gallery/#card-step-3-5-flash-196b), and
[Sarvam 30B](https://sebastianraschka.com/llm-architecture-gallery/#card-sarvam-30b).

## Why GQA became popular

The core idea behind GQA is to reduce the number of key and value heads by sharing them across multiple query heads. This (1) lowers the model’s parameter count and (2) reduces the memory bandwidth usage for key and value tensors during inference since fewer keys and values need to be stored and retrieved from the [KV cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms).

(If you are curious how GQA looks in code, see my [GPT-2 to Llama 3 conversion guide](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/07_gpt_to_llama/converting-llama2-to-llama3.ipynb) for a version without KV cache and my KV-cache variant [here](https://github.com/rasbt/LLMs-from-scratch/blob/main/pkg/llms_from_scratch/llama3.py).)

While GQA is mainly a computational-efficiency workaround for MHA, ablation studies (such as those in the [original GQA paper](https://arxiv.org/abs/2305.13245) and the [Llama 2 paper](https://arxiv.org/abs/2307.09288)) show it performs comparably to standard MHA in terms of LLM modeling performance.

## How the memory savings work

For bf16 keys and values, the per-layer cache size is:

```python
2 × sequence length × number of K/V heads × head dimension × 2 bytes
```

MHA uses as many K/V heads as query heads, whereas multi-query attention uses one. GQA is in between. This is also why the savings grow with sequence length.

![Memory savings of grouped-query attention versus multi-head attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-memory-savings.webp)

Lower is better. Once the context window grows, the
[KV-cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)
savings become more pronounced (Original source
[*LLMs-from-scratch* GQA materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa)).

## Why GQA still matters in 2026

More advanced variants such as [multi-head latent attention (MLA)](https://sebastianraschka.com/llm-architecture-gallery/mla/) can offer better modeling performance at the same KV efficiency levels, based on the ablation studies in the [DeepSeek-V2 paper](https://arxiv.org/abs/2405.04434). However, MLA is more complicated to implement.

GQA remains appealing because it is robust, easier to implement, and also easier to train (since there are fewer hyperparameter tunings necessary, based on my experience).

Among the releases in my [Spring Architectures](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight) article, only MiniMax M2.5 and Nanbeige 4.1 stayed very classic here, using GQA without any other efficiency tweak. The smaller Sarvam 30B model also uses classic GQA, whereas the larger 105B variant switched to DeepSeek-style MLA.

![Relative efficiency comparison between grouped-query attention, multi-head latent attention, and multi-head attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-vs-mla-relative-efficiency.webp)

GQA shares key and value heads, whereas MLA compresses the state stored in the cache. Both reduce the same
memory bottleneck in different ways (Original source
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)).

Sources

[Ainslie et al. (2023), *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*](https://arxiv.org/abs/2305.13245)
[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[LLMs-from-scratch GQA materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)

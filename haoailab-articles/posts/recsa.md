---
title: "RecSA: Million-Token Extrapolation at Logarithmic Cost"
date: 2026-11-17
source: https://haoailab.com/blogs/recsa/
crawled: 2026-11-19
---

# RecSA: Million-Token Extrapolation at Logarithmic Cost

> 原文：[RecSA: Million-Token Extrapolation at Logarithmic Cost](https://haoailab.com/blogs/recsa/) · Hao AI Lab @ UCSD

# RecSA: Million-Token Extrapolation at Logarithmic Cost

November 17, 2026 · 14 minRuitian Wang\*, Xinyu Yang\*, Minshen Zhang\*, Hao Zhang

[![Code](https://img.shields.io/badge/Code--white?style=social&logo=github)](https://github.com/skywong14/RecSA)
[![arXiv](https://img.shields.io/badge/arXiv-2611.07232-white.svg?style=social)](https://arxiv.org/abs/2611.07232)

**TL;DR:** Two problems keep a model trained at 32K from reading a million tokens: dense attention gets slower as the context grows, and beyond 32K the model meets relative distances it never saw in training. We present **RecSA (Recursive Sparse Attention)**, which builds a tree over the KV cache and lets each query search it level by level, so **both the selection cost and the number of entries a query reads grow as $O(\log L)$**. Nodes the query does not select still enter the same softmax as summaries, and **each entry’s RoPE position is its index among the candidates of its level**, which keeps relative distances within the range seen in training. Initialized from Qwen3-4B and trained on **0.62B tokens, all at 32K**, RecSA outperforms all baselines on RULER from 131K to 2M, scoring **60.5 at 1M** against 40.0 for the strongest baseline (Dense + DCA). On one H200, it speeds up prefill by **3.2×** and decoding by **3.8×** at 524K. **[Paper](https://arxiv.org/abs/2611.07232) | [Code](https://github.com/skywong14/RecSA)**

![RULER score of RecSA and four baselines, and decoding latency of RecSA and dense attention, from 32K to 2M](img/fig1_results.png#center)

**Figure 1.** RecSA and four baselines, all trained from Qwen3-4B at 32K. (a) RULER score, average of 13 tasks; every sparse method attends to the same number of entries as RecSA. From 131K on, RecSA leads every baseline, and the gap widens with length. (b) Decoding latency per token on one H200 with batch size 1, against dense FlashAttention in the same framework. RecSA stays near 6 ms from 131K to 524K, while the latency of Dense grows with the context. Hollow markers: with KV offloading.

## 1. Why Long Context Is Hard[#](#1-why-long-context-is-hard)

Dense attention reads the whole KV cache at every decoding step. For Qwen3-4B, the cache and the weights already exceed the 140 GiB of one H200 at 1M tokens, and at 2M the cache alone takes 275 GiB. If the overflow is kept in host memory, a dense decoding step takes 177 ms at 1M and 2.9 s at 2M. Trainable sparse attention such as [MoBA](https://arxiv.org/abs/2502.13189) and [DSA](https://arxiv.org/abs/2512.02556) reads only part of the cache, but to choose that part it scores every preceding block or token, so its selection cost per query is still $O(L)$.

These methods are also trained at the target length, and long training documents become scarcer as the length grows. A model trained at 32K fails beyond 32K, where the query meets distances to the keys that it never saw in training. Context extension methods such as [YaRN](https://arxiv.org/abs/2309.00071) and [DCA](https://arxiv.org/abs/2402.17463) delay this failure but do not remove it (Figure 1a).

Earlier work addresses one of the two problems. Methods such as [InfLLM](https://arxiv.org/abs/2402.04617) run far beyond their training length but still score every block, so their selection cost is $O(L)$. Hierarchical methods such as [HiP](https://arxiv.org/abs/2406.09827) bring the cost down to $O(\log L)$, but they keep each key’s original position and still need context extension. RecSA is the first sparse attention that does both: it selects at $O(\log L)$ cost per query, and it runs far beyond its training length after training only on short sequences.

## 2. Recursive Sparse Attention[#](#2-recursive-sparse-attention)

### 2.1 A Tree over the KV Cache, Searched Level by Level[#](#21-a-tree-over-the-kv-cache-searched-level-by-level)

In each attention layer, RecSA builds a tree over the KV cache of each KV head, and each query searches it from the top (Figure 2).

[](img/fig2_tree.mp4)

**Figure 2.** Each level scores its candidates and selects only the best few; the children of the selected nodes become the candidates of the next level. Each unselected node enters attention as one summary of its subtree, so each token is covered by exactly one entry, and the number of levels grows as log L.

* **The tree.** Every 16 consecutive tokens form a node one level up, and every 16 nodes form a node above them, until the top level has at most 4K nodes. Each node keeps one value, the mean of its children’s values, and one key from a small learned pooler (Section 2.3).
* **The search.** At the top level, the query selects 256 nodes: the one that contains it and the 255 with the highest scores. Their children, at most 4K, become the candidates of the next level, and the step repeats down to the tokens.
* **The summaries.** Unselected nodes are not dropped. Each one enters the same softmax as the exact tokens, as a single entry that summarizes its subtree, so every token is covered by exactly one entry.

Block-sparse attention such as MoBA does the same search on a fixed two-level tree, blocks above tokens. Adding levels as the context grows changes what each query has to score (Table 1).

|  | MoBA | RecSA |
| --- | --- | --- |
| Levels in the tree | 2 at any length | 2 up to 64K tokens, 4 at 2M |
| Candidates scored | every block, $O(L)$ | at most 4K per level, $O(\log L)$ in total |
| Unselected blocks or nodes | dropped | kept as summaries in the softmax |

**Table 1.** What one query does in block-sparse attention and in RecSA.

The node that contains the query is selected at every level, so the tokens right before the query are always read exactly, and RecSA uses no attention sink or local window. At 2M, a query attends to about 12K entries, roughly twice as many as at 32K.

### 2.2 Candidate-Local RoPE[#](#22-candidate-local-rope)

With standard RoPE, the relative distance between a query and a key is the difference of their positions in the sequence. A model trained at 32K has seen only distances below 32K, but at 2M the query is 2M tokens away from the start of the context.

RecSA counts candidates instead of tokens. At each level, every candidate, including the nodes that end up as summaries, takes its index in that level’s candidate list as its RoPE position, and the query takes the last index. The parts of the sequence skipped between candidates get no positions, so the candidates keep their order and only the gaps between them disappear. A level has at most 4K candidates, so the distance between the query and any candidate stays below 4K at any context length (Figure 3). When the backbone is trained on 32K sequences (Section 3), the bottom level already fills its candidate list with 4K tokens, so training covers every distance that occurs at inference.

![Relative distance to the query under RoPE, ReRoPE and candidate-local RoPE on a small tree](img/fig3_rope.png#center)

**Figure 3.** Relative distance to the query, the last of 64 tokens. (a) Standard RoPE counts every token, so distances grow with the context; [ReRoPE](https://github.com/bojone/rerope) puts every token beyond a window at the same distance. (b) Candidate-local RoPE on a small tree with 4 children per node and 2 selected nodes per level: each level numbers only its own candidates, in their order, so distances stay below 8. In RecSA a level holds at most 4,096 candidates, so every distance stays below 4,096 at any context length.

We compare candidate-local RoPE with a variant trained the same way but with standard RoPE at the original token positions (Figure 4). At 32K, the two score within one point of each other. Beyond 32K, standard RoPE fails right away. With YaRN, the failure comes later, but by 524K the score has collapsed as well. Candidate-local RoPE keeps most of its score at 1M.

![RULER score of candidate-local RoPE, standard RoPE and standard RoPE with YaRN](img/fig4_rope_ablation.png#center)

**Figure 4.** RULER score of RecSA and of a variant trained the same way with standard RoPE, evaluated with and without YaRN beyond 32K. Standard RoPE drops to 1.0 at 131K; YaRN delays the drop, but the score is 1.9 at 524K and 1M. Candidate-local RoPE keeps 60.5 at 1M.

### 2.3 Distilling the Pooler from Dense Attention[#](#23-distilling-the-pooler-from-dense-attention)

A node’s key does two jobs for every query: it decides whether the node is selected, and if not, it is the key of the node’s summary in the softmax. Mean pooling, a common choice, waters down a subtree that has one strong match among many weak ones (Figure 5). RecSA’s pooler starts from the mean of the child keys and adds two learned terms:

* one pulls the key toward the children that score highest along a learned direction, by an amount set by a learned gate;
* a small MLP adds a correction computed from the mean and this pull.

With both terms off, the pooler is plain mean pooling. Each attention layer has one pooler of about 25K parameters, shared by all its KV heads and all levels of their trees.

[](img/fig5_pooler.mp4)

**Figure 5.** One node and one query whose match is one of the node's 16 children. Mean pooling waters the match down, and the node is not selected; RecSA's pooler keeps it, so the node is selected and the search goes on into its children. Scores are illustrative.

**Distillation.** Selection is a hard top-k, so the language modeling loss would reach the pooler only through the summaries, never through which nodes get selected. We therefore distill the pooler from the frozen Qwen3-4B:

* At each level, a KL loss fits RecSA’s scores over the candidates to the teacher’s attention mass on their subtrees.
* Training uses only 32K sequences. Below the top level, the candidates come from RecSA’s own selection, as at inference.
* Distillation selects 64 nodes per level instead of 256, so even 32K sequences have three levels and the pooler learns to pool keys that are already pooled. The fourth level that appears at 2M reuses the same parameters.

**Shift penalty.** The MLP can take a shortcut. If it adds the same vector to every key at a level, candidate-local RoPE rotates that vector differently for each candidate, so the shift adds a score that depends on a candidate’s position in the list rather than on its subtree. The KL loss can then drop through this positional bias alone. We penalize the shift shared by all nodes of a level and leave the differences between nodes free. Without the penalty, the MLP barely helps; with it, removing the MLP hurts more the longer the context.

## 3. Train at 32K, Run at 2M[#](#3-train-at-32k-run-at-2m)

Both training stages use only 32K sequences. Stage 1 freezes the original model and distills the pooler (Section 2.3). Stage 2 freezes the pooler and trains the whole backbone under RecSA with the language modeling loss, selecting 256 nodes per level. Starting from Qwen3-4B, the two stages process 0.62B tokens of synthetic retrieval tasks, document question answering, books, code, and instructions with responses generated by the original model. As baselines, we train Dense, MoBA and DSA backbones on the same data and in the same way as Stage 2, and evaluate each with YaRN and with DCA. InfLLM and [InfiniteHiP](https://arxiv.org/abs/2502.08910) need no training. At every length, each sparse method attends to the same number of entries as RecSA.

RecSA scores highest on [RULER](https://arxiv.org/abs/2404.06654) at every length from 131K to 2M (Table 2), and its lead over the strongest baseline grows from about 3 points at 131K to about 20 at 1M. At 32K, it matches Dense. Bounded distances alone do not explain this lead: DSA + DCA also keeps every relative distance within the trained range, with the same token budget, yet at 1M it scores about 24 points below RecSA.

| Method | 32K | 131K | 262K | 524K | 1M | 2M |
| --- | --- | --- | --- | --- | --- | --- |
| *Token budget* | *5,888* | *8,192* | *8,704* | *9,728* | *11,575* | *11,990* |
| *% of context* | *18.0* | *6.25* | *3.32* | *1.86* | *1.16* | *0.60* |
| ***Training-free*** |  |  |  |  |  |  |
| InfLLM | 45.0 | 29.3 | 29.2 | 27.4 | 25.7 | 24.2 |
| InfiniteHiP | 79.6 | 63.7 | 57.7 | 49.4 | 36.6 | 34.0 |
| ***Trained at 32K*** |  |  |  |  |  |  |
| Dense + YaRN | 94.5 | 80.0 | 48.3 | 3.6 | 1.6 | 1.1 |
| Dense + DCA | 94.6 | 78.5 | 68.4 | 58.0 | 40.0 | 27.6 |
| MoBA + YaRN | 81.6 | 31.9 | 5.1 | 0.9 | 1.0 | 0.6 |
| MoBA + DCA | 81.8 | 37.9 | 23.8 | 18.1 | 12.5 | 7.2 |
| DSA + YaRN | **95.3** | 80.5 | 57.1 | 18.8 | 6.0 | 1.4 |
| DSA + DCA | 95.2 | 77.5 | 65.7 | 55.2 | 36.8 | 22.6 |
| **RecSA** | 94.7 | **83.3** | **75.9** | **69.7** | **60.5** | **49.3** |

**Table 2.** RULER score, average of 13 tasks. Token budget: the number of entries the query at the last position attends to, matched across all sparse methods at each length. RecSA leads at every length from 131K to 2M.

On nine [PG-19](https://arxiv.org/abs/1911.05507) books, the perplexity of RecSA stays nearly flat from 131K to 1M, while that of every baseline rises with length (Figure 6).

![Perplexity on PG-19 books from 32K to 1M](img/fig6_ppl.png#center)

**Figure 6.** Perplexity on nine PG-19 books. From 131K to 1M, RecSA stays between 10.9 and 11.1, while at 1M the DCA baselines reach 14.6–19.2 and Dense + YaRN 211.

On six short-context benchmarks (MMLU, ARC-C, GSM8K, IFEval, HumanEval and MBPP), RecSA stays within 2 points of the original Qwen3-4B. Most of these inputs are shorter than 4K tokens, where RecSA reduces to dense attention, so the differences there come from Stage 2 training.

## 4. Logarithmic Cost[#](#4-logarithmic-cost)

Section 2.1 showed that each query’s selection cost grows as $O(\log L)$. Here we check what this means for wall-clock time, on one H200 with batch size 1, against dense FlashAttention in the same framework.

Prefill with RecSA is slightly slower at 32K (1.6 s vs. 1.5 s) and faster from 64K on. At 524K, it takes 80 s, against 257 s for dense attention (Figure 7). At 1M and 2M, where RecSA keeps the exact tokens in host memory (Section 5), the gap widens further.

![Prefill time per token of RecSA and dense attention](img/fig7_prefill.png#center)

**Figure 7.** Prefill time per token on one H200 with batch size 1. At 524K, RecSA is 3.2× faster than dense FlashAttention in the same framework. Hollow markers: RecSA with KV offloading; arrows: Dense values above the axis range.

Decoding with RecSA is faster than dense attention at every length, including 32K (Figure 1b). From 131K to 524K, RecSA stays at about 6 ms per token, while dense decoding grows from about 9 ms to 23 ms, so at 524K RecSA is 3.8× faster. At 1M and 2M, RecSA takes about 8 and 11 ms. The dense KV cache no longer fits in GPU memory there, and dense decoding is more than 20× slower. Section 5 shows where the time of a decoding step goes.

## 5. Kernels[#](#5-kernels)

We implement RecSA in Triton and CUDA. This section covers the parts that differ from other sparse attention kernels, first in prefill and then in decoding.

### Prefill[#](#prefill)

Some block-sparse kernels let a group of adjacent queries walk through the union of their selected blocks and load each block only once, with its keys already rotated by RoPE. Under candidate-local RoPE, this breaks: a key has a different position in each query’s candidate list, so there is no single rotation to apply in advance.

We split the rotation between keys and queries. Call the $m$-th node that a query selects at a level its slot $m$. Child $c$ of slot $m$ then has index $16m + c$ in the next candidate list. Because the RoPE score depends only on the difference of the two positions, we can rotate the key by $c$ alone (0 to 15), which is the same for every query. The query takes the $16m$ part: it starts at the last index and rotates back 16 positions after each node it selected. The 16 adjacent queries of a thread block then share every KV block and load it once (Figure 8). On PG-19, each block loaded at the bottom level serves 4 to 8 of the 16 queries on average, depending on the context length.

![Prefill kernel: 16 queries of one thread block share each KV block](img/fig8_prefill_kernel.png#center)

**Figure 8.** Prefill. Rows are the 16 adjacent queries of one thread block and columns the union of the parent nodes they selected; numbers give the slot of each parent for each query. The key-side rotation does not depend on the slot, so the framed block of 16 children is loaded once and shared by every query that selected its parent.

### Decoding[#](#decoding)

* **Tree update.** Each step appends the new token’s key and value and recomputes only the last node of each level, from its 16 or fewer children.
* **Occupancy.** With batch size 1, one thread block per KV head would occupy only 8 of the 132 SMs of an H200. We split each level’s candidate list into 16 segments, score them in parallel, and merge the segments before taking the top 256.
* **One CUDA graph.** Each level has at most 4K candidates, so every kernel has a fixed launch grid, and the decoding step of all 36 attention layers is captured as one CUDA graph.
* **KV offloading.** At 1M and 2M, the KV cache does not fit in GPU memory (Section 1). RecSA keeps the exact tokens in pinned host memory and only the levels above them on the GPU, which take less than 7% of the cache. Selection runs entirely on the GPU. A gather kernel then copies only the exact tokens under the 256 selected level-1 nodes over PCIe, under 600 MiB per step at any context length. Spare GPU memory caches a suffix of the input, and the gather reads those blocks without crossing PCIe.

![One decoding step with KV offloading](img/fig9_decode_kernel.png#center)

**Figure 9.** One decoding step with KV offloading: (1) append the new token, (2) update the last node of each level with the pooler, (3) score each level in segments and take the top 256, (4) gather the selected exact tokens from the GPU cache or from host memory, and (5) compute one softmax over summaries and exact tokens. Blue: selected; orange: unselected candidates, which enter as summaries.

From 131K to 524K, a decoding step stays near 6 ms, and more than half of it is spent outside attention. At 1M and 2M, most of the added time is the gather (Figure 10).

![Decoding latency breakdown by component from 32K to 2M](img/fig10_decode_breakdown.png#center)

**Figure 10.** Time breakdown of one decoding step. From 131K to 524K the step stays near 6 ms; at 1M and 2M, most of the added time is the gather of the selected exact tokens.

## Conclusion[#](#conclusion)

RecSA builds a tree over the KV cache and searches it level by level, and the summaries of unselected nodes share one softmax with the exact tokens. Both the selection cost and the number of entries read per query grow as $O(\log L)$. Candidate-local RoPE keeps every relative distance within the range seen in training, so RecSA has no inherent limit on context length. Trained only at the original model’s 32K training length, RecSA outperforms all baselines on RULER from 131K to 2M and is faster than dense attention in prefill and decoding from 64K to 2M. Next, we will apply RecSA to larger models.

For details, see [our paper](https://arxiv.org/abs/2611.07232). The code, including the kernels, the Qwen3 integration, RULER evaluation and latency benchmarks, is at [skywong14/RecSA](https://github.com/skywong14/RecSA).

## Citation[#](#citation)

```
@article{wang2026recsa,
  title   = {Recursive Sparse Attention: Million-Token Length Extrapolation at Logarithmic Cost},
  author  = {Wang, Ruitian and Yang, Xinyu and Zhang, Minshen and Zhang, Hao},
  journal = {arXiv preprint arXiv:2611.07232},
  year    = {2026}
}
```

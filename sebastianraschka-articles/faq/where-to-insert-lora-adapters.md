---
title: "Where to insert LoRA adapters"
source: https://sebastianraschka.com/faq/docs/where-to-insert-lora-adapters.html
crawled: 2026-09-06
---

# Where to insert LoRA adapters

For a decoder-only LLM, I would use one of two starting points. Target the **query and value projections in every transformer block** when the adapter budget is tight. Target **all linear layers in the attention and MLP blocks** when the goal is the strongest general LoRA baseline and the larger adapter fits the training budget.

There is no module that always has the biggest impact. Placement controls which pretrained transformations LoRA can modify, while rank controls the capacity of each individual update. The useful comparison therefore depends on the task, architecture, and total trainable-parameter budget.

## What it means to insert LoRA into a layer

For a frozen linear weight matrix \(W \in \mathbb{R}^{d\_{out} \times d\_{in}}\), LoRA learns a low-rank update through two smaller matrices. The layer computes

\[y = Wx + sBAx,\]

where \(A \in \mathbb{R}^{r \times d\_{in}}\), \(B \in \mathbb{R}^{d\_{out} \times r}\), \(r\) is the rank, and \(s\) is the implementation’s scaling factor. Adding LoRA to this layer introduces

\[r(d\_{in} + d\_{out})\]

trainable parameters. The original matrix remains frozen.

![A LoRA wrapper adds a trainable low-rank path alongside one frozen linear transformation](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-3.webp)

This formula matters for placement. An MLP projection is often wider than an attention projection, so adapting it can add more parameters at the same rank. In a grouped-query-attention model, the key and value projections can be narrower than the query projection. A list of seven target-module names does not imply that all seven contribute the same adapter size.

## The common target-module groups

Llama-style implementations make the choices easy to name, although other codebases may fuse or rename the same projections.

| Target group | Common module names | What the adapter can change | Practical role |
| --- | --- | --- | --- |
| Query and value | `q_proj`, `v_proj` | Attention lookup and the content returned by attention | Small historical baseline |
| All attention | `q_proj`, `k_proj`, `v_proj`, `o_proj` | Attention scores, values, and output mixing | Broader attention adaptation |
| All transformer-block linear layers | All attention projections plus `gate_proj`, `up_proj`, `down_proj` | Attention behavior and MLP feature transformations | Strong general baseline |
| Embedding or language-model head | `embed_tokens`, `lm_head` | Input token representations or output logits | Specialized vocabulary or output adaptation |

The MLP layers account for a large share of a transformer’s parameters and computation. Excluding them constrains every learned update to the attention path. This can be sufficient when the pretrained model already has the required features and the task mainly needs a small behavioral adjustment. A larger domain shift may benefit from adapting the MLP transformations as well.

![LoRA can wrap the linear transformations throughout the repeated attention and feed-forward blocks while the remaining model stays frozen](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-4.webp)

## What the original LoRA and QLoRA studies found

The 2021 [LoRA paper](https://arxiv.org/abs/2106.09685) limited its main transformer study to attention matrices. Under a fixed 18-million-parameter budget for GPT-3 175B, adapting both query and value projections performed better overall on WikiSQL and MultiNLI than putting the entire budget into query or key projections. The comparison lowered the rank when more projection types were adapted, so it measured placement under a fixed budget.

This result is the source of the common `q_proj` and `v_proj` default. It is useful evidence for an efficient baseline. The paper did not test MLP LoRA in that experiment, and its two datasets do not establish that query and value are optimal for every modern instruction-tuning task.

The 2023 [QLoRA paper](https://arxiv.org/abs/2305.14314) reported a different ablation for Llama 7B on Alpaca. In that setup, applying LoRA to all linear layers in the transformer blocks was required to match the full-finetuning result. The paper used this all-linear configuration for its main experiments.

These findings answer different questions. Query-plus-value is a sensible low-parameter starting point. All-linear placement gives the adapter access to more of the model and is the stronger quality-oriented baseline for current decoder-only LLM finetuning.

## Apply the chosen modules across the stack

For a first experiment, I would target the selected module types in **every transformer block**. Adapting only the final few blocks saves parameters, but it also prevents LoRA from changing earlier representations. There is no general rule that the top layers contain all task-relevant changes.

The original LoRA study also found that, under its fixed budget, distributing lower-rank adapters across query and value projections worked better than using a higher rank on only one projection type. This suggests a useful order of operations. Expand module coverage before assigning a very large rank to a narrow subset.

Depth can still be an ablation variable. If the full-stack adapter is larger than the budget allows, compare uniform layer sampling, the upper half of the stack, and every block at a smaller rank. Keep the trainable-parameter count similar if the goal is to isolate placement rather than capacity.

## Embeddings and the output head are special cases

Token embeddings and the language-model head are usually left frozen during ordinary instruction finetuning. The pretrained vocabulary mapping already works, and these matrices can be large because one dimension equals the vocabulary size.

They become more relevant when the adaptation introduces new tokens, moves strongly into an underrepresented language, or requires a specialized output space. Weight tying needs attention here. Some models use the same weights for the input embedding and output head, while others keep them separate. Applying or merging an adapter on one side can violate the intended tying behavior if the implementation does not handle it explicitly.

For classification, a newly initialized classification head is usually trained directly rather than approximated with LoRA. LoRA can still adapt the transformer blocks beneath it.

Normalization scales and biases are not matrix multiplications of the same form. They can be unfrozen as a small auxiliary parameter set, but they are separate from the usual LoRA target-module choice.

## Model architecture changes the answer

Do not copy target names from another model without inspecting the module tree. GPT-style implementations may use fused names such as `c_attn`, and other models combine query, key, and value projections into one matrix. A mixture-of-experts model can expose many expert MLPs, making an all-linear adapter much larger than expected. Multimodal systems add projectors and encoders with their own placement choices.

Before training, I would print every matched module and group the added parameters by attention, MLP, embedding, and head. Then verify that only the intended LoRA matrices and explicitly selected auxiliary parameters have `requires_grad=True`. This catches a substring match that silently adapts the wrong layer or misses a fused projection.

## A practical ablation order

For an instruction-tuning project, I would compare these configurations on the same data split:

1. query and value projections in every transformer block
2. all four attention projections
3. all attention and MLP linear projections

There are two useful ways to run this comparison. Keeping the same rank shows what additional adapter capacity buys in practice. Adjusting the ranks so each configuration has a similar parameter count isolates placement more cleanly. Report both the rank and total trainable parameters, since rank alone does not describe the adapter budget.

If the all-linear run improves the held-out task metric enough to justify its larger optimizer state and checkpoint, keep it. If query-plus-value performs similarly, the smaller adapter is easier to train, store, and serve. When every well-tuned LoRA placement reaches the same performance ceiling, the next experiment may require more rank, better data, or [full finetuning](https://sebastianraschka.com/faq/docs/lora-vs-full-finetuning.html) rather than another module-name combination.

The [LoRA rank and alpha FAQ](https://sebastianraschka.com/faq/docs/lora-rank-alpha.html) covers adapter capacity and scaling conventions. The [full-finetuning cost FAQ](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html) explains which memory terms LoRA removes and which ones remain.

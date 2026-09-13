---
title: "Why MoE models have fewer active parameters"
source: https://sebastianraschka.com/faq/docs/why-moe-huge-params-lower-active-compute.html
crawled: 2026-09-06
---

# Why MoE models have fewer active parameters

A mixture-of-experts (MoE) model stores many feed-forward experts, while a router sends each token through only a small subset of them. **Total parameters** count every expert in the checkpoint. **Active parameters** count the selected experts plus the shared parts of the model that run for that token.

This gives MoE models a large gap between stored capacity and per-token computation. The comparison needs a clear baseline. An MoE model uses much less expert computation than a dense model with the same total parameter count. It is not guaranteed to match the speed or memory footprint of a dense model whose size equals the reported active count.

## Most of the extra parameters are in the experts

In a dense transformer block, every token passes through the same feed-forward network. An MoE block replaces that network with several alternative feed-forward networks called experts. Attention, normalization, residual connections, and the rest of the decoder usually remain shared.

For a token representation \(x\), the router calculates a score for each expert and keeps the top \(k\) choices. A simplified MoE layer is

\[\operatorname{MoE}(x) = \sum\_{i \in \operatorname{TopK}(x)} g\_i(x) E\_i(x),\]

where \(E\_i\) is expert \(i\) and \(g\_i(x)\) is its routing weight. Routing is performed for each token. Two neighboring tokens can therefore use different experts.

![A dense feed-forward block applies one network to every token, while an MoE block stores several experts and routes each token through a subset](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/1.webp)

The inactive experts remain part of the model. Their weights occupy checkpoint and device memory, but they do not participate in the feed-forward calculation for that token.

## A small parameter-count example

Suppose the shared parts of a model contain \(S\) parameters. Each MoE layer has eight experts with \(P\) parameters per expert, and the router selects two experts per token. Ignoring the small router for the moment, the expert contribution is

- total expert parameters: \(8P\)
- active expert parameters per token: \(2P\)

For the complete model, the relevant counts are closer to \(S + 8P\) total parameters and \(S + 2P\) active parameters. The ratio is therefore not simply eight divided by two, because the shared attention, embeddings, normalization layers, and output head are active in both cases.

The same accounting applies across all MoE layers. If the architecture contains \(L\) MoE layers, each layer stores its own expert set. Increasing the number of experts can raise the total parameter count quickly while the active expert count stays fixed when \(k\) is unchanged.

![Increasing the number of stored experts raises total parameters much faster than active parameters when the router keeps selecting only a few experts per token](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/2.webp)

Some architectures also include one or more **shared experts**. These experts run for every token alongside the routed experts. Their parameters belong in both the total and active counts.

## Active parameters are a proxy for compute

Parameter count and floating-point operations are related, especially for the large matrix multiplications inside each expert. They are not identical measurements. Exact FLOPs depend on expert dimensions, sequence length, attention design, reused weights, and the operations surrounding the experts.

It helps to keep five quantities separate.

| Quantity | What it describes | What it does not determine by itself |
| --- | --- | --- |
| Total parameters | All stored weights, including inactive experts | Per-token arithmetic |
| Active parameters | Weights on the routed path for one token | Exact FLOPs or latency |
| FLOPs per token | Arithmetic performed for a stated input shape | Memory movement or communication time |
| Weight memory | Capacity needed for the checkpoint at a chosen precision | KV-cache size |
| KV cache | Attention state retained for active sequences | Expert-weight storage |

Attention can become a substantial part of total work at long context lengths even when the expert path stays sparse. The router also has to score experts, dispatch tokens, and combine the returned outputs. These costs are usually smaller than evaluating every expert, but they are part of the runtime.

This is why a model with 22 billion active parameters does not necessarily behave like a dense 22-billion-parameter model. The two models can have different attention dimensions, numbers of layers, expert shapes, memory access patterns, and kernels.

## Why the extra capacity can still help

Although one token visits only a few experts, different tokens can use different routes. Across a batch and training dataset, all experts can receive updates. The model can therefore store more learned functions than a single dense feed-forward path with similar per-token arithmetic.

This conditional computation is the main reason to build an MoE model. Total capacity can grow faster than the compute assigned to one token. It does not guarantee higher quality. The training data, optimization, routing behavior, model dimensions, and post-training recipe still determine how useful that capacity becomes.

The term **expert** can also be misleading. Experts do not necessarily separate into clean human categories such as mathematics, code, and grammar. Specialization can overlap and may vary across layers or training stages.

## The systems costs remain substantial

Every expert weight has to reside somewhere. A single accelerator must hold the complete checkpoint assigned to it, or the experts must be distributed across several devices. Quantization can reduce this storage, although total parameters remain the correct starting point for the weight-memory calculation.

Distributed expert execution adds communication. After routing, token representations are sent to the devices that own the selected experts and returned to their original sequence positions. This all-to-all exchange can consume enough time to offset part of the arithmetic savings.

Batch shape matters too. Each expert processes the tokens routed to it. A large, balanced batch can form efficient expert matrix multiplications. A small batch or uneven routing can leave some experts idle and give others awkwardly small workloads. One batch may collectively touch many experts even though each individual token uses only a few.

Routers therefore need load-balancing mechanisms. Architectures may use an auxiliary objective, routing biases, expert-capacity limits, or other methods to prevent a small group of experts from receiving most tokens. Poor balance affects model training and hardware utilization.

![A shared expert runs for every token, while the router selects additional experts for the token-dependent path](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/3.webp)

During training, backpropagation follows the experts selected for each token. Sparse routing reduces expert arithmetic relative to activating all experts. Training still includes router learning, load balancing, activation storage, optimizer state for the full parameter set, and communication when experts are sharded.

## How to read reported MoE sizes

MoE model names often report total and active parameters together. A name such as `235B-A22B` indicates approximately 235 billion total parameters and about 22 billion active parameters per token. The full 235-billion-parameter checkpoint still has to be stored or distributed.

DeepSeek V3 provides another concrete example. It reports 671 billion total parameters and 37 billion active parameters per token. Its MoE layers use routed experts together with a shared expert, so the active count includes more than the router’s top-k choices alone.

These labels are useful summaries, but the convention is not perfectly standardized. Before comparing two MoE models, I would check whether the reported active count includes shared experts, dense layers, embeddings, and the output head. I would then compare measured FLOPs, memory use, latency, and throughput under the same context length, batch size, precision, runtime, and hardware.

The main accounting rule is simple. Use **total parameters** to estimate checkpoint storage and device capacity. Use **active parameters** as a first approximation of per-token compute. Use an actual benchmark to determine speed.

The broader [mixture-of-experts FAQ](https://sebastianraschka.com/faq/docs/mixture-of-experts.html) explains routing and load balancing in more detail. The [MoE architecture gallery page](https://sebastianraschka.com/llm-architecture-gallery/moe/) provides a visual comparison and a worked DeepSeek V3 example.

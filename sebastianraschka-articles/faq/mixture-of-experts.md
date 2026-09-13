---
title: "Mixture-of-Experts (MoE) vs. Dense LLMs"
source: https://sebastianraschka.com/faq/docs/mixture-of-experts.html
crawled: 2026-09-06
---

# Mixture-of-Experts (MoE) vs. Dense LLMs

A **mixture-of-experts (MoE)** LLM replaces some dense feed-forward blocks with several alternative feed-forward networks called experts. A learned router selects a small subset of these experts for each token. A dense LLM sends every token through the same feed-forward block instead.

Attention usually remains dense in both architectures. The MoE change is commonly applied to the feed-forward part of a transformer block because that part contains a large share of the model’s parameters.

![A dense feed-forward block uses one network for every token, whereas an MoE layer adds a router and several expert networks](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/1.webp)

For a token representation \(x\), the router produces a score for each expert. It keeps the top \(k\) experts and combines their outputs using the routing weights. A simplified expression is

\[\operatorname{MoE}(x) = \sum\_{i \in \operatorname{TopK}(x)} g\_i(x) E\_i(x),\]

where \(E\_i\) is expert \(i\) and \(g\_i(x)\) is its router weight. Routing is normally performed per token, so two tokens in the same sentence can use different experts.

This creates two useful parameter counts. **Total parameters** include every expert stored in the checkpoint. **Active parameters** include the selected experts and the shared parts of the model used for one token. Model names such as `235B-A22B` use this distinction, with the first number describing approximate total parameters and the second describing approximate active parameters.

The comparison needs some care. Suppose one dense feed-forward block has \(P\) parameters. An MoE layer with eight same-sized experts stores about \(8P\) expert parameters. If its router selects two experts, about \(2P\) expert parameters participate in the calculation for one token. This is much less than activating all \(8P\) parameters. It is also more expert compute than the original \(P\)-parameter dense block. MoE increases capacity without increasing per-token computation by the same factor as the stored parameter count.

![As the number of stored experts grows, total expert parameters can rise much faster than the parameters selected for one token](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/2.webp)

The router and experts learn together during training. Tokens routed to an expert provide its training signal. If the router sends most tokens to a few experts, those experts become overloaded while others receive little useful training. MoE systems therefore use a load-balancing mechanism, such as an auxiliary objective, routing bias, or expert-capacity constraints. The exact method differs across architectures.

Load balancing is also a systems concern. After routing, tokens assigned to the same expert are grouped into batches so the expert can process them efficiently. When experts are distributed across accelerators, token representations may have to move to the device that owns the selected expert and then return to their original sequence positions. This all-to-all communication can become a large part of training and serving time.

This is why active parameter count is only an approximation of runtime cost. Attention, embeddings, normalization layers, and the output head still run. Routing adds scoring, sorting, token movement, and memory-access overhead. A model with 22 billion active parameters will not necessarily have the same latency as a dense 22-billion-parameter model.

The full expert checkpoint must be stored somewhere as well. A single GPU needs room for all weights assigned to it, or the experts must be sharded across devices. Sparse activation lowers expert arithmetic per token relative to the total parameter count. The checkpoint still contains every expert, and the attention KV cache is largely unaffected because MoE changes the feed-forward path.

Some architectures add a **shared expert** that runs for every token alongside the routed experts. The shared expert can handle common patterns while leaving routed experts more room to specialize. Shared experts are optional, and the active count must include this path when one is present.

![A shared expert is always active, while the router selects additional experts for each token](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/3.webp)

Expert specialization is also less tidy than the name may suggest. One expert does not necessarily become a clean “math expert” while another handles grammar. Routing patterns can overlap, and specialization may differ by layer, token position, or training stage.

In practice, MoE is attractive when the training and serving system can distribute expert weights and route large token batches efficiently. A dense model is simpler to train, finetune, and serve on a small number of devices. MoE becomes more useful when additional total capacity is valuable and the hardware stack can handle sparse routing without losing the theoretical compute advantage to communication and poor utilization.

For a visual architecture example, see the [Mixture of experts gallery page](https://sebastianraschka.com/llm-architecture-gallery/moe/). The related FAQ [Why do MoE models have huge parameter counts but lower active compute per token?](https://sebastianraschka.com/faq/docs/why-moe-huge-params-lower-active-compute.html) focuses on interpreting reported model sizes.

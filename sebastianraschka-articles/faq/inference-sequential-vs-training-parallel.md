---
title: "Why is inference sequential while training is much more parallel?"
source: https://sebastianraschka.com/faq/docs/inference-sequential-vs-training-parallel.html
crawled: 2026-09-06
---

# Why is inference sequential while training is much more parallel?

Training can score many next-token predictions in one forward pass because the correct token sequence is already available in the training batch. Autoregressive inference does not know its continuation. It must select one token, append it to the context, and only then compute the distribution for the following token.

Consider the token sequence `[A, B, C, D]`. Causal-language-model training can use `[A, B, C]` as the input and `[B, C, D]` as the shifted targets. One model call produces three logits vectors. The first is scored against `B`, the second against `C`, and the third against `D`.

![A training sequence is shifted into inputs and targets so one forward pass provides a loss at many token positions](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/inputs-targets.webp)

The full input tensor is present on the accelerator, but each position does not get to read the entire sequence. A [causal mask](https://sebastianraschka.com/faq/docs/causal-attention.html) blocks later positions inside attention. The representation at `A` cannot use `B` or `C`, while the representation at `C` can use `A`, `B`, and `C`. Matrix operations for these different positions still run together. This training setup is often called teacher forcing because every position receives the actual preceding tokens from the dataset.

Parallelism also comes from the batch dimension. Many sequences can be processed together, and model computations can be distributed across accelerators. Training is not parallel in every direction. Transformer layers still depend on earlier layers, the backward pass follows the computation graph, and one optimizer step depends on the completed gradients from that batch.

Generation has a dependency across new tokens. If the current context ends with `A`, the model can produce logits for `B`. It cannot compute the correct distribution after `[A, B]` until `B` has been selected. If sampling chooses a different token, every later distribution may change.

![Autoregressive generation uses the final logits to select one token, appends that token, and then runs the next decoding step](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

Inference still contains substantial parallel work. The initial prompt-processing stage, usually called **prefill**, handles all prompt positions in one masked forward pass. Each forward pass uses parallel matrix operations, and a server can batch several requests. Once decoding begins, however, the new tokens for one sequence form an ordered chain.

A **KV cache** stores the keys and values from the prompt and earlier generated tokens. This avoids recomputing the complete prefix at every decoding step. It makes each step cheaper without making token `t+2` independent of token `t+1`.

Methods such as speculative decoding can propose or verify several tokens together and reduce wall-clock latency. They work around some hardware inefficiency, but the accepted output must still follow the model’s autoregressive conditional distributions. This is why training throughput measured in tokens per second can be high while the latency for producing one response remains constrained by consecutive decoding steps.

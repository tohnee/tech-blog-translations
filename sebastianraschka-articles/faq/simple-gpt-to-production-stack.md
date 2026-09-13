---
title: "From a simple GPT to production"
source: https://sebastianraschka.com/faq/docs/simple-gpt-to-production-stack.html
crawled: 2026-09-06
---

# From a simple GPT to production

A simple GPT implementation is best treated as an **executable reference**. It makes tokenization, causal attention, loss computation, and generation easy to inspect. A production stack should preserve this behavior while replacing educational code paths with tested data, training, inference, and service components.

I would not gradually turn the teaching implementation itself into the final server. Keep it small enough that a calculation can be checked line by line. Use it to test the optimized implementation and to understand failures.

For most applications, deployment also starts from a tested pretrained checkpoint rather than a GPT trained from scratch. Pretraining a generally useful model is a separate data and compute project. The from-scratch model still provides the right foundation for understanding the checkpoint and verifying its implementation.

The progression can be organized around six stages with an exit check for each one.

| Stage | What to add | Evidence before moving on |
| --- | --- | --- |
| Reference model | Tokenizer, embeddings, causal attention, feed-forward blocks, next-token loss, generation | Overfit a tiny batch, reproduce a saved checkpoint, and verify causal masking |
| Model-quality pipeline | Data validation, train-validation split, checkpoint metadata, task evaluations | Reproducible loss curves and held-out results for the intended tasks |
| Adaptation | Supervised finetuning, LoRA or full finetuning, optional preference training | A task-specific evaluation gain without unacceptable regressions |
| Inference runtime | Efficient loading, reduced precision, KV caching, batching, optimized attention | Numerical or output parity plus latency, throughput, and memory measurements |
| Service | Request schema, token limits, streaming, scheduling, timeouts, cancellation, access control | Load and failure tests under the expected concurrency and prompt lengths |
| Operations | Monitoring, release gates, canary rollout, versioning, rollback | A dashboard, a pinned previous release, and a rehearsed rollback path |

## Establish a trustworthy reference

The first implementation should remain intentionally plain. It needs the exact tokenizer and position handling, the input-target shift for next-token prediction, and a causal mask that prevents target leakage. A tiny-batch overfit test is especially useful. If the model cannot drive the loss down on a few sequences, a larger training run will be difficult to debug.

Save-and-load parity matters early. The same checkpoint, tokenizer, prompt, random seed, and decoding settings should reproduce the expected logits or tokens. Record the model configuration beside the weights so the number of layers, dimensions, vocabulary, normalization, and position method cannot drift silently.

![The from-scratch path builds the base model first, then adds finetuning, evaluation, and preference training as separate stages.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/final-overview.webp)

## Separate model development from serving

Training and serving have different responsibilities. The offline path prepares data, updates weights, evaluates checkpoints, and publishes an immutable model artifact. The online path loads that artifact, tokenizes requests, schedules inference, returns generated tokens, and reports operational metrics.

This separation makes releases reproducible. A model artifact should identify the checkpoint, tokenizer, chat template, configuration, code revision, and evaluation result. Changing the prompt template can change behavior even when the weights stay fixed, so it belongs in the versioned artifact or release configuration.

Finetuning should be driven by a measurable gap. Supervised finetuning teaches the desired response format and task behavior. LoRA can reduce training memory and checkpoint size when a full update is unnecessary. Preference methods such as DPO add another data and evaluation requirement, so I would use them only when pairwise preferences address a failure that supervised examples do not solve well.

## Modernize the architecture only when training allows it

RoPE, RMSNorm, SwiGLU, and grouped-query attention are architectural choices. They can be introduced one at a time in a model that will be trained with them. They cannot simply be inserted into an existing GPT-2 checkpoint while preserving its outputs because the learned weights depend on the original computation.

![The GPT-to-Llama progression keeps the decoder-only backbone while changing normalization, position handling, feed-forward blocks, and attention sharing.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

When loading an existing checkpoint, the implementation must match that checkpoint’s architecture. Modernization then happens in the runtime. Examples include fused attention kernels, a KV cache, lower-precision computation, memory-efficient weight loading, quantization, and request batching. Each change should be compared with the reference implementation on logits or a fixed generation set before it is judged by speed alone.

KV caching is one of the first useful inference changes. It avoids recomputing old keys and values during autoregressive decoding. The cache increases memory use, and its size grows with context length and active sequences. Dynamic or continuous batching can raise total throughput, although waiting to form or extend a batch may increase latency for an individual request.

Quantization is another measured tradeoff. It can reduce weight memory and sometimes improve throughput. Kernel support, hardware, batch size, and the chosen precision determine the actual gain. The quantized checkpoint should pass the same application evaluation as the original because small numerical changes can alter generated outputs.

## Add the service boundary last

A minimal service loads the model once and exposes a stable request schema. It validates the prompt and generation parameters, enforces context and output limits, and supports cancellation when a client disconnects. Streaming improves perceived responsiveness but does not reduce total generation work.

The scheduler controls concurrency and memory. It should reject or queue requests before they cause an out-of-memory failure. Request timeouts, rate limits, authentication, readiness checks, and bounded queues are ordinary service concerns that remain necessary around an LLM.

If the model can call tools, model output must be treated as untrusted input. Tool names and arguments need schema validation, and the runtime should grant the smallest required permissions. Prompt instructions should never become authorization to access secrets or unrelated resources.

## Measure the behavior users experience

Useful inference measurements include time to first token, inter-token latency, total response time, request throughput, queue time, peak accelerator memory, and KV-cache utilization. Report the prompt length, output length, batch size, model precision, and hardware with the result. Tokens per second without this context is difficult to compare.

Operational logs should identify the model release and error category without retaining sensitive prompts by default. Monitor invalid requests, timeouts, cancellations, out-of-memory events, and evaluation regressions. A new model or runtime should pass offline tests before a small canary deployment. Keep the previous version loadable so rollback is a configuration change rather than an emergency rebuild.

This order keeps failures local. If the optimized runtime disagrees with the reference logits, the problem is below the service layer. If offline evaluations pass but requests fail under concurrency, the scheduler or capacity limits deserve attention. A component should be added when its exit check shows that it solved the intended problem.

For the quality gate, see [Why is evaluating LLM outputs difficult, and what are common ways to evaluate them?](https://sebastianraschka.com/faq/docs/evaluating-llm-outputs.html). The inference path is covered in [What is a KV cache, and why does it make LLM inference faster?](https://sebastianraschka.com/faq/docs/kv-cache.html), while [What is memory-mapped weight loading, and when is it useful?](https://sebastianraschka.com/faq/docs/memory-mapped-weight-loading.html) discusses checkpoint startup memory.

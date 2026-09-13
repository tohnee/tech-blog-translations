---
title: "Why is full finetuning so expensive compared with LoRA?"
source: https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html
crawled: 2026-09-06
---

# Why is full finetuning so expensive compared with LoRA?

Full finetuning updates every trainable weight in the model. The memory cost therefore extends well beyond the checkpoint itself. Training also needs gradients and optimizer state for those weights, plus the activations required for backpropagation.

Adam makes the difference easy to see. It commonly maintains two moment estimates for each trainable parameter. These buffers are often stored in 32-bit precision even when the model weights use `bfloat16`. Some mixed-precision setups also keep a 32-bit master copy of the weights.

For a rough scale reference, 7 billion `bfloat16` parameters occupy about 14 GB. Two 32-bit Adam moment buffers add about 56 GB. Gradients and an optional master-weight copy can add tens of gigabytes more, before counting activations. The exact total depends on the optimizer, precision policy, and whether states are sharded or offloaded.

**LoRA** freezes the original matrix and learns a low-rank update through two smaller matrices. For a weight with shape \(d\_{out} \times d\_{in}\) and rank \(r\), the adapter contains roughly \(r(d\_{in}+d\_{out})\) trainable values instead of \(d\_{in}d\_{out}\) values. When \(r\) is small, gradients and optimizer states for the adapter are correspondingly small.

![The repo's LoRA introduction shows full finetuning of the original weights alongside a much smaller low-rank trainable path](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-1.webp)

This saves the memory associated with training the base weights, and it makes task-specific checkpoints much smaller. Several adapters can share one copy of the original model rather than storing a complete finetuned checkpoint for every task.

LoRA still has to load the frozen base model. Plain LoRA does not make those weights disappear or automatically quantize them. QLoRA combines low-rank adapters with a quantized frozen base and can reduce this part of the memory footprint further.

The activation cost also remains. Backpropagation must pass through the network to compute gradients for adapters placed in earlier layers. The large base-model matrix multiplications still run during the forward pass. As a result, the reduction in trainable parameters can be much larger than the reduction in step time or peak memory.

![LoRA can be inserted as a lightweight trainable wrapper around existing linear layers while retaining the frozen pretrained checkpoint](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-4.webp)

For deployment, the adapter can often remain separate or be merged into the base weights. Separate adapters are convenient when one server supports several tasks. Merging removes the extra adapter path for a fixed task, although it creates a new combined checkpoint.

Full finetuning remains useful when the data and compute budget justify updating the entire model or when a low-rank update is too restrictive. LoRA is especially attractive when optimizer memory, experiment storage, or maintaining many task-specific variants is the limiting cost.

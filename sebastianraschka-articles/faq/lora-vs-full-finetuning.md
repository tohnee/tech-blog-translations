---
title: "LoRA vs. Full Finetuning of Language Models"
source: https://sebastianraschka.com/faq/docs/lora-vs-full-finetuning.html
crawled: 2026-09-06
---

# LoRA vs. Full Finetuning of Language Models

**LoRA**, short for **Low-Rank Adaptation**, is often the practical starting point for adapting a large pretrained model. It keeps the original weights frozen and learns small updates for selected linear layers. Full finetuning instead allows all of the model’s trainable weights to change.

Suppose a linear layer contains the weight matrix \(W\). Full finetuning learns an updated version of \(W\) directly. LoRA expresses the change as the product of two smaller matrices,

\[W\_{adapted} = W + AB,\]

where the inner dimension of \(A\) and \(B\) is the LoRA rank. The pretrained matrix \(W\) stays frozen during training.

![Full finetuning updates the original weight matrix, whereas LoRA learns a separate low-rank update](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-1.webp)

This difference has a large effect on optimizer memory. Full finetuning stores gradients and optimizer states for every trainable model parameter. LoRA only needs these training-specific tensors for the adapter weights. For a matrix with shape \(d\_{out} \times d\_{in}\) and LoRA rank \(r\), the adapter contains approximately \(r(d\_{in}+d\_{out})\) parameters instead of \(d\_{in}d\_{out}\) parameters.

LoRA still has to load the frozen base model, and the forward pass still performs the large matrix multiplications in that model. It also retains much of the activation memory needed for backpropagation. Therefore, a 99% reduction in trainable parameters does not translate into a 99% reduction in peak memory or training time. QLoRA can reduce the base-model memory further by keeping the frozen weights in a quantized format.

![A LoRA wrapper adds a small trainable path alongside the frozen linear layer](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-3.webp)

Checkpoint storage is another strong reason to use LoRA. A team can keep one base model and save a small adapter for each task or customer. At inference time, the adapter can remain separate or be merged into a copy of the base weights. A full finetuning run produces a complete task-specific checkpoint, which is simpler to distribute as one artifact but much larger to store.

In terms of model quality, there is no automatic winner. LoRA can match full finetuning when the required weight changes are well represented by low-rank updates. This often makes it a good fit for instruction tuning, classification, and other adaptations where the pretrained model already has most of the required capability.

Full finetuning has more freedom because every weight can change independently. That freedom may help for a large domain shift, extensive continued training, or a task where LoRA has reached a clear performance ceiling. It also introduces many more trainable parameters. With a small dataset, those extra degrees of freedom do not guarantee a better validation result.

My practical decision process is straightforward. I would start with LoRA when GPU memory is limited, when I expect to maintain several task-specific variants, or when I want to compare training recipes quickly. If a well-tuned LoRA run still falls short and the compute budget is available, full finetuning becomes a useful next experiment. This gives the more expensive method a concrete performance target to beat.

The comparison should use the same data split and evaluation procedure. LoRA results also depend on the adapter rank, scaling factor, and target modules. A weak LoRA configuration is not evidence that parameter-efficient finetuning has reached its limit.

For related details, see [Why is full finetuning so expensive compared with LoRA?](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html), [How do rank and alpha affect LoRA behavior in practice?](https://sebastianraschka.com/faq/docs/lora-rank-alpha.html), and [Where should LoRA adapters be inserted in an LLM for the biggest impact?](https://sebastianraschka.com/faq/docs/where-to-insert-lora-adapters.html).

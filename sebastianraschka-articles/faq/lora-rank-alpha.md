---
title: "How do rank and alpha affect LoRA behavior in practice?"
source: https://sebastianraschka.com/faq/docs/lora-rank-alpha.html
crawled: 2026-09-06
---

# How do rank and alpha affect LoRA behavior in practice?

LoRA leaves a pretrained weight matrix \(W\) frozen and learns a low-rank update through two smaller matrices. If the input is \(x\), we can write the modified layer as

\[y = xW + s \cdot xAB,\]

where \(r\) is the shared inner dimension of \(A\) and \(B\), and \(s\) is a scaling factor. The rank \(r\) and the LoRA alpha hyperparameter affect different parts of this expression.

**Rank controls the size and capacity of the adapter.** For a weight matrix with shape \(d\_{out} \times d\_{in}\), a rank-\(r\) adapter adds approximately

\[r(d\_{in} + d\_{out})\]

trainable parameters. Consider a \(4096 \times 4096\) weight matrix. A rank-8 adapter adds 65,536 parameters, compared with 16,777,216 parameters in the original matrix. Increasing the rank from 8 to 16 doubles the adapter parameter count.

The higher rank gives the update more degrees of freedom. However, twice the rank does not imply twice the model quality. A small rank may already capture the changes required for a narrow task. Larger ranks become useful when the adaptation is more complex, but they also increase optimizer memory, checkpoint size, and the risk of fitting noise in a small dataset.

![The two LoRA matrices form a low-rank path, with the rank setting the width of the inner dimension](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-2.webp)

**Alpha controls the scale of the adapter update.** It is easy to confuse alpha with the optimizer learning rate, but they are separate hyperparameters. The learning rate controls the size of each optimization step. Alpha rescales the LoRA contribution when the layer runs.

Many LoRA libraries use

\[s = \frac{\alpha}{r}.\]

With this convention, rank 8 and alpha 16 give a scale of 2. If we change the rank to 16 while leaving alpha at 16, the scale drops to 1. This comparison changes the adapter capacity and its explicit scale at the same time.

For a cleaner rank comparison, I would keep \(\alpha/r\) fixed. For example, rank 8 with alpha 16 and rank 16 with alpha 32 both use a scale of 2. The second adapter still has twice as many trainable parameters, but the scale applied to its output stays the same.

The formula is an implementation detail worth checking. The small from-scratch LoRA layer used in the companion material multiplies the adapter output directly by `alpha`, without dividing by the rank. Other LoRA variants use their own rank-dependent normalization. Consequently, an alpha value of 16 does not necessarily mean the same thing across two codebases.

![A LoRA wrapper adds the scaled adapter path to the output of the frozen linear layer](https://sebastianraschka.com/images/LLMs-from-scratch-images/appendix-e_compressed/lora-3.webp)

LoRA implementations commonly initialize one adapter matrix with random values and the other with zeros. The product \(AB\) is then zero at the start, so adding the adapter does not immediately change the pretrained model’s output. Alpha starts to matter as the zero-initialized matrix learns nonzero values.

For practical experiments, I usually treat rank as the capacity choice and alpha as part of the optimization setup. I first compare modest ranks while holding the scaling convention, target modules, data, and optimizer settings constant. Then I tune alpha together with the learning rate on a validation set. If the adapter underfits, a higher rank may help. If training is unstable, I would inspect both alpha and the learning rate before concluding that the rank is the problem.

There is no universal best pair. The useful settings depend on the task, data volume, target modules, and the exact LoRA implementation. The main precaution is to record the effective scaling formula along with `rank` and `alpha`. This makes results easier to interpret and reproduce.

For the memory implications of changing the number of trainable parameters, see [Why is full finetuning so expensive compared with LoRA?](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html)

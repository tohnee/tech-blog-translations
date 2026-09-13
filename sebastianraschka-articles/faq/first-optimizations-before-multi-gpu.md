---
title: "Single-GPU Optimizations Before Multi-GPU Training"
source: https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html
crawled: 2026-09-06
---

# Single-GPU Optimizations Before Multi-GPU Training

Before adding more GPUs, I would first measure the single-GPU training loop. Useful baseline numbers include tokens per second, peak allocated memory, GPU utilization, and the time spent waiting for the next batch. The loss curve should also be recorded so that a faster implementation can be checked against the original training behavior.

This baseline tells us which optimization is likely to matter. A GPU with idle gaps may be waiting for data. A nearly full GPU running low-throughput attention may benefit from a better kernel. An out-of-memory error requires a memory change rather than a data-loader adjustment.

![The repo includes a direct comparison workflow for inspecting how the optimized single-GPU code differs from the baseline implementation](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/llm-training-speed/vs-code-compare.png)

On recent accelerators, **bfloat16 mixed precision** is usually a good first experiment. It reduces activation and gradient memory and lets supported matrix multiplications use tensor cores. The loss should be compared with the full-precision baseline, especially when changing precision settings or gradient scaling behavior.

The attention implementation often provides the next large opportunity. PyTorch’s scaled dot-product attention can select optimized backends, including FlashAttention-style kernels when the hardware, dtype, and tensor layout are supported. Fused optimizers and fused normalization or activation kernels can reduce launch and memory overhead elsewhere in the block.

`torch.compile` is worth testing after the model runs correctly with stable shapes. Compilation has startup cost and can recompile when shapes or control flow change, so I would measure a warmed-up training interval rather than the first few steps.

The input pipeline should keep up with the optimized model. Pinned host memory, asynchronous device transfers, an appropriate number of data-loader workers, and prefetching can help. These changes matter only when profiling shows that input preparation or transfer is on the critical path.

Batch size is easier to tune once the faster kernels and precision settings are in place. Increasing the microbatch can improve GPU utilization until memory or kernel efficiency stops improving. Gradient accumulation raises the effective batch size without increasing the per-step microbatch, while activation checkpointing saves activation memory by repeating part of the forward computation during backpropagation.

![The repo's optimization summary collects the single-GPU changes that should be measured before distributing the training loop](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

Multi-GPU training becomes appropriate when the optimized run is still too slow or the model state cannot fit on one device. The distinction matters. Distributed Data Parallel replicates the model and optimizer on every GPU, so each device still needs enough memory for a full copy. FSDP and ZeRO-style methods shard parameters, gradients, or optimizer state and can address model-fit limits.

After distribution, I would report scaling efficiency in addition to aggregate throughput. Two GPUs rarely provide exactly twice the single-GPU speed because gradient synchronization and communication consume time. The single-GPU baseline remains useful for deciding whether the added hardware and debugging complexity are paying off.

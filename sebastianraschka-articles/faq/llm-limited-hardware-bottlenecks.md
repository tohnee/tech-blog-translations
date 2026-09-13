---
title: "LLM Training and Inference Bottlenecks on Limited Hardware"
source: https://sebastianraschka.com/faq/docs/llm-limited-hardware-bottlenecks.html
crawled: 2026-09-06
---

# LLM Training and Inference Bottlenecks on Limited Hardware

The limiting resource depends on the workload. Inference may fit the model weights but run out of memory when the context or batch grows. Full finetuning can fail even at a short context because gradients and optimizer states exceed the available memory. A run can also fit comfortably and remain slow because the accelerator is waiting for data or moving tensors through a narrow memory path.

**Checkpoint and weight memory**

The raw weight requirement is approximately the parameter count multiplied by the bytes per parameter. A 7-billion-parameter model needs about 14 GB for bf16 weights before temporary buffers and framework overhead. Quantization reduces this storage, provided the hardware has efficient kernels for the selected format.

Loading has its own peak. A naive implementation may construct the model and load a separate state dictionary, briefly keeping two copies in host memory. Streaming shards, memory mapping, or initializing on a meta device can avoid this spike.

![Memory-efficient loading reduces the temporary RAM and VRAM copies created while a checkpoint is materialized](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/memory-efficient-loading/memory-efficient-loading.webp)

**Training-state memory**

Full finetuning stores gradients and optimizer state for every trainable parameter. Adam commonly keeps two 32-bit moment buffers, and some mixed-precision setups retain master weights as well. The [full-finetuning comparison](https://sebastianraschka.com/faq/docs/full-finetuning-vs-lora-cost.html) gives a concrete 7B example. LoRA reduces the trainable gradients and optimizer state, while QLoRA can also shrink the frozen base weights.

Activations are a separate cost. They grow with microbatch size, sequence length, model width, and layer count because tensors needed by backpropagation must be retained. Activation checkpointing saves memory by recomputing selected forward operations. Gradient accumulation increases the effective batch size, but it does not reduce the memory needed by one microbatch.

**Inference memory and latency**

Autoregressive inference needs model weights plus a KV cache for each active sequence. Cache memory grows with retained tokens, cache-producing layers, KV heads, and precision. The [long-context FAQ](https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html) shows how Qwen3 8B reaches about 4.5 GiB of logical bf16 cache at 32,768 tokens for one sequence.

Prompt prefill and token-by-token decoding also have different performance profiles. Prefill processes many positions together and can be compute-heavy. Decoding handles one new position per sequence and repeatedly reads weights and cached state, so memory bandwidth and batching often determine throughput. CPU or disk offload may make a model fit, although transfers over PCIe or storage can make it much slower.

**Kernel and input-pipeline utilization**

Low GPU utilization with visible idle gaps often points to data loading, host-to-device transfer, synchronization, or tiny workloads. High utilization with slow attention suggests a compute or kernel bottleneck. On supported hardware, bf16, fused operations, scaled dot-product attention, and FlashAttention-style kernels can improve speed or memory use. `torch.compile` can help stable workloads, but compilation time, recompilation, and extra memory should be measured.

![The PyTorch optimization notes collect precision, attention, compilation, optimizer, and data-pipeline changes that should be benchmarked against one baseline](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

I would diagnose limited hardware in this order. Record the phase that fails, peak device and host memory, tokens per second, and accelerator utilization. Then reduce one workload dimension such as model size, context length, or microbatch size. Next, test an appropriate precision and a phase-specific memory technique. Only after the run is stable would I add optimized kernels, offload, or multiple devices. The [single-GPU optimization FAQ](https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html) gives a more detailed measurement sequence.

The symptom should determine the fix. FlashAttention cannot solve an out-of-memory error caused by loading duplicate weight copies. LoRA does not address a large inference KV cache. Quantization may reduce capacity pressure without improving speed when the device lacks an optimized quantized kernel.

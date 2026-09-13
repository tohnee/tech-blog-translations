---
title: "torch.compile for LLM workloads"
source: https://sebastianraschka.com/faq/docs/torch-compile-llm-workloads.html
crawled: 2026-09-06
---

# torch.compile for LLM workloads

`torch.compile` can improve LLM training or inference speed when the same PyTorch computation runs many times. It captures regions of eager PyTorch code, specializes them for the observed inputs, and sends them to a compiler backend that can fuse operations or generate more efficient kernels.

The gain depends on the model, tensor shapes, device, and PyTorch version. Compilation does not reduce the number of model parameters, attention complexity, or KV-cache size. It also cannot repair a slow data loader or communication bottleneck. I therefore benchmark it as an execution optimization.

## What happens under the hood

In eager mode, Python dispatches PyTorch operations one at a time. `torch.compile` uses TorchDynamo to capture sequences of these operations in FX graphs. For training, AOTAutograd also constructs graph representations of the backward computation. TorchInductor is the default backend that lowers the captured graphs to optimized code.

The basic use remains one line.

```python
compiled_model = torch.compile(model)
```

Recent PyTorch versions also provide `model.compile()`, which compiles an `nn.Module` in place. The current arguments and modes are listed in the official [`torch.compile` API reference](https://docs.pytorch.org/docs/stable/generated/torch.compile.html).

Compilation can help in several places. It may fuse neighboring pointwise operations so intermediate tensors do not have to be written to and read from device memory. It can reduce Python dispatch and GPU kernel-launch overhead. It can also generate kernels specialized for the observed tensor properties.

These opportunities are workload dependent. A large matrix multiplication already handled efficiently by a tuned library leaves less room for improvement. The compiler may still optimize the normalization, activation, residual, and reshape operations around it. Likewise, a model already using an optimized scaled dot-product attention kernel may see a smaller additional gain than a model with many separate attention operations.

![A source comparison helps isolate implementation changes before the optimized eager model is benchmarked with compilation.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/llm-training-speed/vs-code-compare.png)

The compiled path preserves the intended computation. Compiled and eager results are still not guaranteed to be bitwise identical because kernel fusion can change the order of floating-point operations. I would compare losses, gradients, and task metrics against the eager baseline when enabling compilation for training.

## Training and generation stress the compiler differently

LLM training is often a good fit because the forward and backward passes repeat for many steps. Fixed microbatch and sequence lengths also make graph reuse easier. A short finetuning run may end before the one-time compilation cost is recovered, while a long pretraining run has many more steps over which to amortize it.

Inference contains two distinct phases. Prompt prefill processes many tokens in parallel and is often dominated by large matrix multiplications and attention kernels. Autoregressive decoding performs one token step at a time and may contain more launch and Python overhead relative to its tensor work. Compilation can therefore be useful for decoding, especially with batches of concurrent sequences.

The KV-cache implementation matters. A cache that grows by concatenating a new tensor on every step changes shapes and allocation behavior. A preallocated cache with stable tensor shapes is generally easier to compile and run efficiently. Variable prompt lengths and changing batch membership can still create several shape patterns, so production systems often group requests into a manageable set of buckets.

## Warm-up time must be measured separately

The first call to a compiled model includes graph capture and code generation. Some modes perform additional profiling or CUDA Graph warm-up. Timing that call together with steady-state execution can make a useful compiled path look slow. Ignoring it entirely can make a short job look better than it is.

I would report two numbers.

- **Cold-start time** includes compilation and any initial warm-up.
- **Steady-state time** measures repeated execution after the compiled path is ready.

The distinction was visible in my earlier [PyTorch 2.0 benchmark](https://sebastianraschka.com/blog/2023/pytorch-faster.html). Compilation did not help a short DistilBERT run when the startup work was included, although the warmed execution itself was faster. That exact result is specific to the older software and hardware setup, but the measurement issue still applies.

![In this single-A100 LLM training benchmark, compilation improved throughput after the model was already using optimized attention and other single-GPU changes.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

## Graph breaks and recompilation can erase the gain

TorchDynamo places guards on assumptions such as tensor shape, dtype, device, and relevant Python state. If a later call violates a guard, PyTorch may compile another version of the graph. LLM workloads can trigger this through changing sequence lengths, batch sizes, cache shapes, training modes, or control-flow paths.

PyTorch can represent some dimensions symbolically and reuse a graph across several sizes. Its default automatic behavior may first specialize a shape and then generalize a changing dimension after recompilation. Fully dynamic code can be harder to optimize, and some data-dependent behavior cannot be captured cleanly. The current [dynamic-shape documentation](https://docs.pytorch.org/docs/main/user_guide/torch_compiler/torch.compiler_dynamic_shapes.html) recommends targeted annotations for known dynamic dimensions. It warns against enabling every dimension dynamically without inspection.

A **graph break** occurs when Dynamo reaches code it cannot capture in the current graph. PyTorch normally runs the unsupported section in eager mode and resumes capture afterward. Correctness can remain intact, but the smaller compiled regions lose fusion opportunities and add transitions between compiled and eager execution. Data-dependent Python branches, side effects, unsupported operators, and calls into opaque extensions are common causes.

For a small reproduction, I usually begin with this command.

```python
TORCH_LOGS="graph_breaks,recompiles" python train.py
```

The `graph_breaks` output identifies where capture stopped. The `recompiles` output reports failed guards that caused another graph version. Setting `fullgraph=True` is also useful during debugging because it turns the first graph break into an error instead of silently creating several regions. PyTorch’s [compiler troubleshooting guide](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/torch.compiler_troubleshooting.html) covers these tools and `tlparse` for larger runs.

## When compilation is worth testing

| Workload property | Likely effect |
| --- | --- |
| Many repeated training steps with stable shapes | Compilation cost is easier to amortize |
| Batched decoding with a preallocated KV cache | Repeated small operations can benefit from lower launch overhead |
| Many pointwise operations around matrix multiplications | Fusion may reduce intermediate memory traffic |
| One-off execution or a very short run | Cold-start cost may exceed the saved runtime |
| Continually changing shapes or Python control flow | Recompilation and graph breaks can limit reuse |
| Input, storage, or multi-GPU communication bottleneck | Compiling the model does not address the limiting stage |

I would start with the default compile mode and a correct eager baseline. `mode="reduce-overhead"` can lower Python overhead through CUDA Graphs for supported CUDA workloads, particularly small batches, but it may use more memory. `mode="max-autotune"` spends additional compilation time searching kernel choices. Neither mode guarantees a faster result, so the default measurement should come first.

A fair test warms both paths, synchronizes the accelerator around timing, and runs enough iterations to reduce noise. It should cover the real mixture of batch sizes and sequence lengths. One convenient shape is insufficient. I would compare tokens per second, latency, peak memory, numerical outputs, and total wall-clock time including compilation. The [single-GPU optimization FAQ](https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html) places this experiment alongside mixed precision, optimized attention, and input-pipeline checks.

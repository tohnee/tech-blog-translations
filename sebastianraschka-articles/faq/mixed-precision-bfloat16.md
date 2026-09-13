---
title: "Why does mixed precision such as `bfloat16` help so much in practice?"
source: https://sebastianraschka.com/faq/docs/mixed-precision-bfloat16.html
crawled: 2026-09-06
---

# Why does mixed precision such as `bfloat16` help so much in practice?

Mixed precision can improve both memory use and throughput because many neural-network operations do not need 32-bit inputs. On hardware with native `bfloat16` support, lower-precision matrix multiplications are faster, and moving 16-bit tensors through memory requires half as many bytes as `float32`. The complete training job does not automatically become twice as fast or use half the memory, though, because some tensors and operations remain in 32-bit precision.

The numerical format explains why `bfloat16` is a popular choice. It uses one sign bit, eight exponent bits, and seven fraction bits. `Float32` also uses eight exponent bits, but it has 23 fraction bits. Standard `float16` allocates ten fraction bits and only five exponent bits.

![Bfloat16 keeps the eight exponent bits of float32 while reducing the number of fraction bits](https://sebastianraschka.com/images/blog/2023/llm-mixed-precision/bfloat16.webp)

As a result, `bfloat16` has approximately the same dynamic range as `float32`. Its values are spaced more coarsely because it carries fewer fraction bits. `Float16` represents nearby values more precisely within its range, but its smaller exponent can overflow or underflow much sooner. This is why `float16` training commonly uses loss scaling, whereas `bfloat16` usually works without a gradient scaler.

The word **mixed** is important here. In [PyTorch automatic mixed precision](https://docs.pytorch.org/docs/stable/amp.html), autocast chooses a dtype for each eligible operation. Matrix multiplications and convolutions can run with lower-precision inputs. Reductions and other numerically sensitive operations may run in `float32`. On accelerators such as TPUs, the multiplication can use `bfloat16` inputs while accumulation uses `float32`.

A minimal PyTorch training step looks like this:

```python
optimizer.zero_grad(set_to_none=True)

with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    logits = model(input_ids)
    loss = loss_fn(logits, targets)

loss.backward()
optimizer.step()
```

The forward pass and loss calculation are inside the autocast region. Backpropagation runs after leaving it. Unlike a typical `float16` AMP loop, this example does not use `GradScaler`. When autocast is enabled, I would also avoid manually calling `model.bfloat16()` or converting every input. Autocast is meant to make the operation-specific dtype choices.

The memory savings depend on what is actually stored in lower precision. Seven billion parameters require about 28 GB in `float32` and 14 GB in `bfloat16`, before any framework overhead. This halving applies if those parameters are stored in the corresponding dtype. A basic autocast setup often keeps the model parameters in `float32` and casts operands for selected operations. It can still save substantial activation memory without halving the parameter allocation.

Large-model training frameworks offer several precision policies. One may keep model parameters in `bfloat16` while retaining `float32` optimizer states or a master copy of the weights. Another may keep parameters in `float32` and use `bfloat16` only during the forward and backward computations. Gradients can also use either precision depending on the setup. Labels such as `bf16-mixed` and `bf16-true` therefore describe meaningfully different memory layouts.

This distinction matters for Adam. Its two moment buffers are commonly stored in `float32`, even when model computation uses `bfloat16`. If model parameters, master weights, and optimizer states remain in `float32`, the overall training-memory reduction will be much smaller than the reduction in activation memory. Inference is simpler because it has no optimizer states, so storing weights and the KV cache in 16-bit formats often produces a more direct memory saving.

![Mixed precision is one of several practical optimizations whose benefit should be measured on the target hardware](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

The speedup also depends on the bottleneck. A matrix-heavy LLM usually benefits when the accelerator has native `bfloat16` kernels. Smaller tensors reduce memory traffic, and specialized matrix units provide higher lower-precision throughput. An older device without native support may emulate the operations or fall back to slower kernels. A data-loading bottleneck will not disappear after changing the compute dtype.

The wider exponent range makes `bfloat16` forgiving, but it does not make numerical checks unnecessary. Its low fraction precision can round small updates or closely spaced values together. I would monitor the loss for `NaN` or infinity, compare validation metrics with a short `float32` baseline, and inspect any custom operations that autocast does not handle well.

In practice, `bfloat16` autocast is a good first experiment when the hardware supports it. Record peak memory and tokens per second using the same batch size as the `float32` baseline. If the run is stable, the saved memory can then be used for a larger microbatch, a longer context, or a larger model. The [single-GPU optimization checklist](https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html) puts this precision change in the broader order of training improvements.

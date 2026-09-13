---
title: "Why can model loading require much more memory than expected?"
source: https://sebastianraschka.com/faq/docs/model-loading-memory-than-expected.html
crawled: 2026-09-06
---

# Why can model loading require much more memory than expected?

Model loading can require much more memory than the final model because several copies or representations of the weights may coexist during startup. The checkpoint size is therefore a poor estimate of peak RAM or VRAM unless the loading path is known.

The common PyTorch sequence makes the main duplication easy to see:

```python
model = Model(config)
state_dict = torch.load(checkpoint_path, map_location="cpu")
model.load_state_dict(state_dict)
model = model.to("cuda")
```

Constructing `model` allocates and initializes its parameters. `torch.load` then materializes the checkpoint tensors in a separate state dictionary. `load_state_dict` copies those tensors into the existing parameters, and moving the model to a GPU creates device copies while the CPU objects may still be alive.

![A memory-efficient loading path avoids keeping a fully initialized model and a separate materialized checkpoint in memory at the same time](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/memory-efficient-loading/memory-efficient-loading.webp)

For a rough example, 7 billion `bfloat16` parameters require about 14 GB. If the model constructor creates its parameters in the default `float32` dtype, that destination model occupies about 28 GB. The 14 GB checkpoint and 28 GB initialized model can overlap at roughly 42 GB of host memory before counting Python objects, nonparameter buffers, or conversion workspaces. A `float32` checkpoint would make the overlap larger.

**Dtype conversion can add another peak.** Calling `.to(dtype=torch.bfloat16)` or moving a tensor to another device generally returns new storage. The old storage remains live until all references to it are released. A loader that first constructs `float32` weights, copies `float32` checkpoint values, and only then converts to `bfloat16` may briefly hold both precisions.

Quantized checkpoints have a related issue. A small file does not guarantee a small in-memory model. The loader may dequantize weights into `float16` or `bfloat16`, or it may allocate quantization scales, zero points, packing metadata, and temporary conversion buffers. The final representation depends on the runtime and kernel support rather than the filename alone.

**A checkpoint may contain more than model weights.** Training checkpoints often include optimizer moments, a gradient scaler, scheduler state, and other training metadata. Adam’s two moment tensors can be larger than the low-precision model weights if they are stored in `float32`. Loading the full training checkpoint when only inference weights are needed can therefore materialize much more data than expected.

Device placement matters too. PyTorch checkpoints remember the device tags of their tensor storages. Loading a checkpoint that was saved from a GPU can restore tensors to that GPU unless `map_location` overrides the behavior. The [PyTorch `torch.load` documentation](https://docs.pytorch.org/docs/stable/generated/torch.load.html) recommends `map_location="cpu"` when the goal is to avoid a GPU-memory surge and control the transfer explicitly.

**Sharding only helps when the loader streams the shards.** A model may be split across several files or devices, yet a naive process can still read every shard before discarding the weights assigned elsewhere. Multiple worker processes can also load their own CPU copy of the checkpoint. An efficient distributed loader reads one shard at a time or loads only the tensors owned by the current rank.

The memory number shown by a monitoring tool needs interpretation as well. PyTorch’s CUDA allocator keeps freed blocks in a cache so later allocations can reuse them quickly. `torch.cuda.memory_allocated()` reports memory occupied by live tensors, while `torch.cuda.memory_reserved()` includes the larger pool managed by the caching allocator. `nvidia-smi` can continue to show cached memory as used after a temporary tensor has been deleted.

Calling `torch.cuda.empty_cache()` releases unused cached blocks to other applications, but it does not free live tensors or increase the memory available to the same PyTorch job beyond what the allocator could already reuse. A large gap between allocated and reserved memory therefore has a different cause from a large live state dictionary.

I would measure loading in phases instead of relying on one number after startup. Record CPU resident memory and CUDA allocated and reserved memory after model construction, checkpoint loading, state assignment, dtype conversion, device transfer, and the first forward pass. The first forward pass may create kernel workspaces that are unrelated to checkpoint loading.

A useful CUDA check is:

```python
torch.cuda.reset_peak_memory_stats()

# Run one loading phase here.

print(torch.cuda.memory_allocated() / 2**30, "GiB allocated")
print(torch.cuda.memory_reserved() / 2**30, "GiB reserved")
print(torch.cuda.max_memory_allocated() / 2**30, "GiB peak")
```

Several loading techniques target different copies. Constructing on the `meta` device avoids allocating parameters that will be overwritten. `load_state_dict(..., assign=True)` can attach checkpoint tensors instead of copying them into preallocated parameters. Memory mapping avoids eagerly reading every checkpoint storage into CPU RAM. Sharded or sequential loading limits how many tensors are materialized at once.

These methods can be combined. The companion FAQ [What is memory-mapped weight loading, and when is it useful?](https://sebastianraschka.com/faq/docs/memory-mapped-weight-loading.html) shows the PyTorch pattern using `mmap=True`, meta-device construction, and `assign=True`.

The practical goal is to control both the loading peak and the final footprint. I would choose the target dtype before allocating the destination model, load only the state needed for the task, keep device placement explicit, and release the state dictionary as soon as no references to it remain.

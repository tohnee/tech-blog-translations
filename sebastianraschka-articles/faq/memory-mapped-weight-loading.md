---
title: "What is memory-mapped weight loading, and when is it useful?"
source: https://sebastianraschka.com/faq/docs/memory-mapped-weight-loading.html
crawled: 2026-09-06
---

# What is memory-mapped weight loading, and when is it useful?

**Memory-mapped weight loading** maps a checkpoint file into the process’s virtual address space instead of first reading every tensor storage into a separate CPU-memory buffer. The operating system brings file pages into physical memory when the program accesses them.

This is useful when a checkpoint is large enough that ordinary loading creates an uncomfortable RAM peak. It can also shorten the time before the program can inspect or process the first tensor, since it does not have to read the entire file up front.

![Large checkpoints benefit from loading methods that avoid holding several full copies of the weights in CPU memory](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/memory-efficient-loading/memory-efficient-loading.webp)

Consider the usual PyTorch loading sequence. `torch.load` materializes a state dictionary in CPU memory. Constructing the model allocates and initializes another set of parameters. `load_state_dict` then copies the checkpoint values into those parameters. For a large model, the state dictionary and initialized model can overlap in memory even though the initial parameter values are immediately overwritten.

For a checkpoint created with `torch.save`, current PyTorch versions support the following first step:

```python
state_dict = torch.load(
    "checkpoint.pth",
    mmap=True,
    weights_only=True,
    map_location="cpu",
)
```

With `mmap=True`, the tensor storages remain backed by the checkpoint file and are read as they are accessed. `weights_only=True` restricts the unpickler to tensors, primitive types, dictionaries, and explicitly allowed types. I would still load checkpoints only from trusted sources.

Memory mapping alone does not remove the allocation for the destination model. PyTorch’s [checkpoint-loading recipe](https://docs.pytorch.org/tutorials/recipes/recipes/module_load_state_dict_tips.html) combines it with construction on the `meta` device and assignment of the mapped tensors:

```python
state_dict = torch.load(
    "checkpoint.pth",
    mmap=True,
    weights_only=True,
    map_location="cpu",
)

with torch.device("meta"):
    model = Model(model_config)

model.load_state_dict(state_dict, assign=True)
```

A tensor on the `meta` device stores shape, dtype, and other metadata without allocating storage for its values. The `assign=True` argument replaces these placeholders with the tensors from the state dictionary. A normal in-place copy into a meta tensor would do nothing, which is why `assign=True` matters in this pattern.

If an optimizer will be used, it should usually be created after `load_state_dict(..., assign=True)`. Optimizers keep references to parameters, and assignment can replace the parameter objects those references were meant to track. Recent PyTorch versions provide an additional future flag for some conversion workflows, but creating the optimizer after loading remains the easy rule to remember.

The memory savings have a clear boundary. Mapping a 20 GB checkpoint does not compress it into a few megabytes. The process reserves virtual address space for the mapping, and accessed pages enter the operating system’s page cache. If inference eventually touches every weight, the system still has to read every required byte from storage. Moving the completed model to a GPU also requires its normal device memory.

The main improvement is the loading peak. Memory mapping avoids an eager CPU copy of all checkpoint storages. Meta-device construction avoids allocating parameters that will be overwritten. Assignment avoids copying from the state dictionary into a second set of model tensors. These three steps address different allocations.

Memory mapping is especially helpful when processing weights one tensor at a time. For example, a conversion script can access one tensor, cast or move it, write the result, and release the intermediate before continuing. It is also useful when CPU RAM is smaller than the checkpoint or when several model-loading processes start on the same host.

For a small checkpoint on a machine with ample RAM, ordinary loading is simpler and may be perfectly adequate. Memory mapping can introduce page-fault latency, and slow or remote storage can make on-demand access noticeable. Sharded checkpoints offer another practical option because a loader can process and release one shard at a time.

The file format and library matter as well. The `mmap=True` argument described here applies to compatible `torch.load` checkpoints. Formats such as Safetensors have their own memory-mapped loading paths. I would check the loader’s documentation instead of assuming that the same keyword and behavior apply everywhere.

For a broader breakdown of model-loading peaks, see [Why can loading an LLM use much more memory than the final model size?](https://sebastianraschka.com/faq/docs/model-loading-memory-than-expected.html).

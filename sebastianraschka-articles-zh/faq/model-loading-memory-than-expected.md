---
title: "为什么加载模型可能需要远超预期的内存？"
title_en: "Why can model loading require much more memory than expected?"
source: https://sebastianraschka.com/faq/docs/model-loading-memory-than-expected.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么加载模型可能需要远超预期的内存？

加载模型所需的内存可能远多于最终模型本身，因为在启动过程中，权重的多个副本或表示可能同时存在。因此，检查点（checkpoint）文件的大小并不能很好地估计峰值 RAM 或 VRAM，除非你了解具体的加载路径。

PyTorch 的常见流程让主要的重复占用一目了然：

```python
model = Model(config)
state_dict = torch.load(checkpoint_path, map_location="cpu")
model.load_state_dict(state_dict)
model = model.to("cuda")
```

构造 `model` 会分配并初始化其参数。接着 `torch.load` 会把检查点张量实体化到一个独立的状态字典中。`load_state_dict` 把这些张量复制到已存在的参数里，而把模型移动到 GPU 又会创建设备副本，与此同时 CPU 上的对象可能仍然存活。

![一条内存高效的加载路径可以避免让一个完整初始化的模型和一个单独实体化的检查点同时驻留内存](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/memory-efficient-loading/memory-efficient-loading.webp)

举一个粗略的例子：70 亿个 `bfloat16` 参数大约需要 14 GB。如果模型构造函数以默认的 `float32` dtype 创建参数，那么目标模型就会占用约 28 GB。在计入 Python 对象、非参数缓冲区或转换工作区之前，14 GB 的检查点与 28 GB 的已初始化模型可能叠加出大约 42 GB 的主机内存占用。若检查点本身是 `float32`，这个叠加还会更大。

**数据类型转换可能带来另一个峰值。**调用 `.to(dtype=torch.bfloat16)` 或把张量移到另一个设备通常会返回新的存储。旧的存储在对其的所有引用被释放之前会一直存活。一个先构造 `float32` 权重、复制 `float32` 检查点数值、最后才转换成 `bfloat16` 的加载器，可能会在短时间内同时持有两种精度。

量化检查点有类似的问题。文件小并不保证内存中的模型也小。加载器可能会把权重反量化成 `float16` 或 `bfloat16`，也可能会分配量化缩放系数（scale）、零点（zero point）、打包元数据以及临时转换缓冲区。最终的表示形式取决于运行时和内核支持情况，而不只是文件名。

**检查点包含的内容可能不止模型权重。**训练检查点通常还包括优化器矩（moment）、梯度缩放器、调度器状态以及其他训练元数据。如果 Adam 的两个矩张量以 `float32` 存储，它们可能比低精度的模型权重更大。因此，在只需要推理权重时加载完整的训练检查点，实体化的数据量可能远超预期。

设备放置同样重要。PyTorch 检查点会记住其张量存储的设备标签。加载一个从 GPU 保存的检查点时，除非 `map_location` 覆盖这一行为，否则张量会被恢复到那块 GPU 上。[PyTorch `torch.load` 文档](https://docs.pytorch.org/docs/stable/generated/torch.load.html)建议，当目标是避免 GPU 内存激增并显式控制传输时，使用 `map_location="cpu"`。

**只有当加载器以流式方式读取分片时，分片（sharding）才有帮助。**一个模型可能被拆分到多个文件或设备上，但一个天真的进程仍然可能在丢弃分配给别处的权重之前，把每个分片都读进来。多个 worker 进程也可能各自加载一份检查点的 CPU 副本。高效的分布式加载器会一次只读取一个分片，或者只加载当前 rank 所拥有的张量。

监控工具显示的内存数字也需要解读。PyTorch 的 CUDA 分配器会把已释放的块保留在缓存中，以便后续分配能快速复用。`torch.cuda.memory_allocated()` 报告的是存活张量占用的内存，而 `torch.cuda.memory_reserved()` 包含了缓存分配器管理的更大内存池。在一个临时张量被删除之后，`nvidia-smi` 仍可能把缓存内存显示为已使用。

调用 `torch.cuda.empty_cache()` 会把未使用的缓存块释放给其他应用程序，但它不会释放存活的张量，也不会让同一个 PyTorch 任务获得超出分配器本可复用范围的更多内存。因此，allocated 与 reserved 内存之间的巨大差距，与一个庞大的存活状态字典，原因是不同的。

我会分阶段测量加载过程，而不是只依赖启动后的某一个数字。在模型构造、检查点加载、状态赋值、数据类型转换、设备传输以及第一次前向传播之后，分别记录 CPU 常驻内存和 CUDA 的 allocated 与 reserved 内存。第一次前向传播可能会创建与检查点加载无关的内核工作区。

一个有用的 CUDA 检查代码是：

```python
torch.cuda.reset_peak_memory_stats()

# Run one loading phase here.

print(torch.cuda.memory_allocated() / 2**30, "GiB allocated")
print(torch.cuda.memory_reserved() / 2**30, "GiB reserved")
print(torch.cuda.max_memory_allocated() / 2**30, "GiB peak")
```

有若干种加载技术分别针对不同的副本。在 `meta` 设备上构造可以避免分配那些随后会被覆盖的参数。`load_state_dict(..., assign=True)` 可以直接挂接检查点张量，而不是把它们复制进预分配的参数。内存映射（memory mapping）可以避免急切地把所有检查点存储读入 CPU 内存。分片或顺序加载则限制了一次实体化的张量数量。

这些方法可以组合使用。配套的 FAQ [什么是内存映射权重加载，它何时有用？](https://sebastianraschka.com/faq/docs/memory-mapped-weight-loading.html)展示了使用 `mmap=True`、meta 设备构造和 `assign=True` 的 PyTorch 模式。

实际的目标是同时控制加载峰值和最终占用。我会在分配目标模型之前先确定目标数据类型，只加载任务所需的状态，保持设备放置显式，并在不再有引用时尽快释放状态字典。

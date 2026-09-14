---
title: "什么是内存映射的权重加载，它什么时候有用？"
title_en: "What is memory-mapped weight loading, and when is it useful?"
source: https://sebastianraschka.com/faq/docs/memory-mapped-weight-loading.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是内存映射的权重加载，它什么时候有用？

**内存映射（memory-mapped）的权重加载**是把检查点文件映射进进程的虚拟地址空间，而不是先把每个张量的存储（storage）完整读入一个单独的 CPU 内存缓冲区。当程序访问到某页文件时，操作系统才会把这页带入物理内存。

当检查点大到让普通加载方式产生令人不安的 RAM 峰值时，这种方法就很有用。它还可以缩短程序能够检查或处理第一个张量之前的等待时间，因为程序不必预先读完整个文件。

![大型检查点受益于避免在 CPU 内存中同时持有权重多份完整副本的加载方法](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/memory-efficient-loading/memory-efficient-loading.webp)

想一想 PyTorch 常规的加载流程。`torch.load` 会在 CPU 内存中实例化一个状态字典。构建模型会分配并初始化另一组参数。随后 `load_state_dict` 再把检查点的值拷贝进这些参数。对于大模型来说，即使初始参数值马上就会被覆盖，状态字典和初始化后的模型仍可能在内存中重叠存在。

对于用 `torch.save` 创建的检查点，当前的 PyTorch 版本支持把第一步写成这样：

```python
state_dict = torch.load(
    "checkpoint.pth",
    mmap=True,
    weights_only=True,
    map_location="cpu",
)
```

使用 `mmap=True` 时，张量的存储仍以检查点文件为后备，在被访问到时才读取。`weights_only=True` 把反序列化器（unpickler）限制为只能加载张量、基本类型、字典以及显式允许的类型。即便如此，我也只会从可信来源加载检查点。

仅靠内存映射并不能免去目标模型的内存分配。PyTorch 的[检查点加载配方](https://docs.pytorch.org/tutorials/recipes/recipes/module_load_state_dict_tips.html)把它与在 `meta` 设备上构建模型、以及赋值映射来的张量结合在一起：

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

位于 `meta` 设备上的张量只保存形状、dtype 等元数据，而不会为它的值分配存储。`assign=True` 参数会用状态字典中的张量替换掉这些占位符。对 meta 张量做普通的就地（in-place）拷贝不会产生任何效果，这正是这个模式中 `assign=True` 之所以关键的原因。

如果之后要用优化器，通常应当在 `load_state_dict(..., assign=True)` 之后创建它。优化器持有对参数的引用，而赋值操作可能会替换掉这些引用原本指向的参数对象。近期的 PyTorch 版本为某些转换工作流提供了一个额外的 future 开关，但「加载之后再创建优化器」仍然是那条最容易记住的规则。

内存节省有明确的边界。映射一个 20 GB 的检查点并不会把它压缩成几兆字节。进程只是为映射保留虚拟地址空间，被访问的页会进入操作系统的页缓存。如果推理最终会触及每一个权重，系统仍然必须从存储中读出所需的每一个字节。把加载完成的模型搬到 GPU 上同样需要正常的设备内存。

主要的改进在于加载峰值。内存映射避免了对所有检查点存储的急切 CPU 拷贝。meta 设备构建避免了为那些马上会被覆盖的参数分配内存。赋值避免了从状态字典向第二组模型张量的拷贝。这三步各自解决的是不同的内存分配。

内存映射在逐个张量地处理权重时尤其有帮助。例如，一个转换脚本可以访问一个张量、做类型转换或搬运、写出结果、释放中间量，然后继续处理下一个。当 CPU RAM 小于检查点大小，或同一台主机上会启动多个模型加载进程时，它也很有用。

对于内存充裕的机器上的小型检查点，普通加载更简单，而且可能完全够用。内存映射可能引入缺页（page-fault）延迟，而慢速或远程存储会让按需访问变得明显。分片（sharded）检查点提供了另一个实用的选项，因为加载器可以一次处理并释放一个分片。

文件格式和所用库也很重要。这里描述的 `mmap=True` 参数适用于兼容的 `torch.load` 检查点。Safetensors 等格式有它们自己的内存映射加载路径。我会去查阅所用加载器的文档，而不是假设同样的关键字和行为到处通用。

关于模型加载峰值的更全面拆解，参见[为什么加载一个 LLM 所用的内存可能远超模型最终大小？](https://sebastianraschka.com/faq/docs/model-loading-memory-than-expected.html)（Why can loading an LLM use much more memory than the final model size?）。

---
title: "面向 LLM 工作负载的 torch.compile"
title_en: "torch.compile for LLM workloads"
source: https://sebastianraschka.com/faq/docs/torch-compile-llm-workloads.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 面向 LLM 工作负载的 torch.compile

当同一段 PyTorch 计算要运行很多次时，`torch.compile` 可以提升 LLM 训练或推理速度。它捕获 eager 模式 PyTorch 代码的区域，针对观察到的输入做特化，然后交给可以融合运算或生成更高效核（kernel）的编译器后端。

收益取决于模型、张量形状、设备和 PyTorch 版本。编译不会减少模型参数量、注意力复杂度或 KV 缓存大小。它也无法修复缓慢的数据加载器或通信瓶颈。因此我把它当作一种执行层面的优化来测。

## 底层发生了什么

在 eager 模式下，Python 逐个分发 PyTorch 运算。`torch.compile` 使用 TorchDynamo 把这些运算序列捕获为 FX 图。对于训练，AOTAutograd 还会构建反向计算的图表示。TorchInductor 是默认后端，把捕获的图降级为优化后的代码。

基本用法仍只需一行。

```python
compiled_model = torch.compile(model)
```

较新的 PyTorch 版本还提供 `model.compile()`，可就地编译一个 `nn.Module`。当前的参数和模式见官方 [`torch.compile` API 参考](https://docs.pytorch.org/docs/stable/generated/torch.compile.html)。

编译可以在多个方面带来帮助。它可以融合相邻的逐元素运算，使中间张量不必写入再读出设备内存。它可以减少 Python 分发和 GPU 核启动开销。它还能针对观察到的张量属性生成特化核。

这些机会取决于工作负载。一个本已由高度调优的库高效处理的大型矩阵乘法，改进空间不大。但编译器仍可能优化它周围的归一化、激活、残差和重塑运算。同样，一个已经使用优化缩放点积注意力核的模型，相比一个由许多分散注意力运算组成的模型，额外收益可能更小。

![在把优化后的 eager 模型加上编译进行基准测试之前，源码对比有助于隔离实现层面的变化。](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/llm-training-speed/vs-code-compare.png)

编译后的路径保持预期的计算不变。但编译结果与 eager 结果并不保证按位一致，因为核融合可能改变浮点运算的顺序。在为训练启用编译时，我会对照 eager 基线比较损失、梯度和任务指标。

## 训练与生成对编译器的压力不同

LLM 训练往往很适合编译，因为前向和反向传播要在许多步中重复执行。固定的微批次和序列长度也让图复用更容易。一次简短的微调可能在一次性编译成本收回之前就结束了，而一次漫长的预训练则有更多的步骤来摊销它。

推理包含两个不同阶段。提示预填充（prefill）并行处理许多 token，通常由大型矩阵乘法和注意力核主导。自回归解码一次只执行一个 token 步，相对于其张量计算量可能包含更多启动和 Python 开销。因此编译对解码可能很有用，尤其是在并发序列成批的场景下。

KV 缓存的实现方式很重要。每一步都通过拼接新张量来增长的缓存会改变形状和分配行为。张量形状稳定的预分配缓存通常更容易被高效编译和执行。可变的提示长度和不断变化的批次成员仍可能产生多种形状模式，因此生产系统常把请求归入一组可控的桶（bucket）。

## 预热时间必须单独测量

对编译后模型的第一次调用包括图捕获和代码生成。某些模式还会做额外的性能剖析或 CUDA Graph 预热。把这次调用与稳态执行一起计时，可能让一条有用的编译路径显得很慢；完全忽略它，又可能让一个短任务显得比实际更好。

我会报告两个数字。

- **冷启动时间**包括编译和任何初始预热。
- **稳态时间**测量编译路径就绪后的重复执行。

在我早先的 [PyTorch 2.0 基准测试](https://sebastianraschka.com/blog/2023/pytorch-faster.html)中，这一区别清晰可见。把启动开销计入后，编译并没有让一次简短的 DistilBERT 运行受益，尽管预热后的执行本身更快了。那个具体结果只适用于当时的旧软硬件环境，但测量问题依然存在。

![在这项单卡 A100 的 LLM 训练基准中，在模型已使用优化注意力和其他单卡优化之后，编译进一步提升了吞吐量。](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/pytorch-tips/pytorch-tips.webp)

## 图中断与重编译可能抵消收益

TorchDynamo 会在张量形状、dtype、设备及相关 Python 状态等假设上放置守护（guard）。如果后续调用违反了某个守护，PyTorch 可能编译另一个版本的图。LLM 工作负载可能因序列长度、批次大小、缓存形状、训练模式或控制流路径的变化触发这种情况。

PyTorch 可以把某些维度符号化，并在多个尺寸之间复用一张图。默认的自动行为可能先特化某个形状，然后在重编译后把变化维度泛化。完全动态的代码更难优化，某些数据依赖的行为也无法干净地捕获。当前的[动态形状文档](https://docs.pytorch.org/docs/main/user_guide/torch_compiler/torch.compiler_dynamic_shapes.html)建议对已知的动态维度做有针对性的标注，并警告不要在未检查的情况下把所有维度都设为动态。

**图中断（graph break）**指 Dynamo 遇到无法在当前图中捕获的代码。PyTorch 通常会以 eager 模式运行不支持的部分，之后恢复捕获。正确性可以保持，但更小的编译区域会丧失融合机会，并增加编译与 eager 执行之间的切换。数据依赖的 Python 分支、副作用、不支持的运算符以及对不透明扩展的调用都是常见原因。

要做一个小的复现，我通常从这条命令开始。

```python
TORCH_LOGS="graph_breaks,recompiles" python train.py
```

`graph_breaks` 输出指出捕获在哪里停止。`recompiles` 输出报告导致另一个图版本的失败守护。调试时设置 `fullgraph=True` 也很有用，它把第一次图中断变成错误，而不是悄悄创建多个区域。PyTorch 的[编译器故障排查指南](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/torch.compiler_troubleshooting.html)介绍了这些工具以及面向较大运行的 `tlparse`。

## 什么时候值得测试编译

| 工作负载特征 | 可能的影响 |
| --- | --- |
| 形状稳定的大量重复训练步骤 | 编译成本更容易摊销 |
| 使用预分配 KV 缓存的批量解码 | 重复的小运算可受益于更低的启动开销 |
| 矩阵乘法周围有大量逐元素运算 | 融合可能减少中间内存流量 |
| 一次性执行或极短的运行 | 冷启动成本可能超过节省的运行时间 |
| 形状或 Python 控制流不断变化 | 重编译和图中断会限制复用 |
| 输入、存储或多卡通信瓶颈 | 编译模型解决不了受限阶段的问题 |

我会从默认编译模式和一个正确的 eager 基线开始。`mode="reduce-overhead"` 可以通过 CUDA Graphs 降低受支持 CUDA 工作负载（尤其是小批次）的 Python 开销，但可能占用更多内存。`mode="max-autotune"` 花费额外编译时间搜索核选择。两种模式都不保证更快，因此应先做默认测量。

公平的测试要对两条路径都预热，在计时处同步加速器，并运行足够多的迭代来降低噪声。它应覆盖真实的批次大小与序列长度组合，单一形状是不够的。我会比较每秒 token 数、延迟、峰值内存、数值输出，以及包含编译在内的总挂钟时间。[单卡优化 FAQ](https://sebastianraschka.com/faq/docs/first-optimizations-before-multi-gpu.html)把这项实验与混合精度、优化注意力和输入流水线检查放在一起讨论。

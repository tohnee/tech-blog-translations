---
title: "torch.compile 入门及其与 vLLM 的协同工作方式"
title_en: "Introduction to torch.compile and How It Works with vLLM"
source: https://vllm.ai/blog/2025-08-20-torch-compile
crawled: 2026-09-12
translated: 2026-09-13
---

# torch.compile 入门及其与 vLLM 的协同工作方式

> 原文：[Introduction to torch.compile and How It Works with vLLM](https://vllm.ai/blog/2025-08-20-torch-compile) · vLLM 博客

作者：Luka Govedič（Red Hat）、Richard Zou（Meta）、Addie Stevens（Red Hat）、Kaichao You（清华大学）、Michael Goin（Red Hat）、Saša Zelenović（Red Hat）

[#性能](https://vllm.ai/blog/tags/performance)

> **注意：** 本文源自我们每两周一次的 vLLM office hours——由 Red Hat 主办、vLLM 项目提交者与 UC Berkeley 团队参与的社区论坛。每次活动涵盖近期更新、嘉宾深度分享与开放式问答。[欢迎每隔一个周四加入我们](https://red.ht/office-hours)，时间为美东时间下午 2:00 / 美西时间上午 11:00（Google Meet），活动录像与幻灯片会发布在我们的 [YouTube 播放列表](https://www.youtube.com/playlist?list=PLbMP1JcGBmSHxp4-lubU5WYmJ9YgAQcf3)。

## 简介

如今，快速的大语言模型（LLM）推理要求模型在多样的硬件、工作负载和规模上都尽可能高效地执行。高效执行高度依赖经过充分优化的内核，而这些内核往往需要针对不同模型与平台进行手工调优。**torch.compile** 是 PyTorch 的即时（JIT）编译器，能够自动生成优化内核，使 PyTorch 代码显著提速，而无需开发者在所有受支持的硬件平台上手动优化内核。

对于 vLLM——事实上用于可移植、高效 LLM 推理的开源推理引擎——torch.compile 不只是性能增强器。它是一个核心组件，把优化的责任从模型开发者转移给了编译器。优化在编译期间应用，无需修改模型定义，从而实现更清晰的关注点分离，并达到极致性能。在这篇文章中，我们将介绍 torch.compile 的工作原理、它与 vLLM 的集成方式，以及 vLLM 如何利用自定义编译 pass 来最大化性能。我们还会讨论 vLLM 中 torch.compile 集成的进行中与未来工作，以进一步提升其易用性与性能。

## 什么是 torch.compile？

torch.compile 让你以最小的代价优化 PyTorch 代码：使用 torch.compile 就像给函数或 torch.nn.Module 加一个装饰器一样简单。torch.compile 会自动把张量操作捕获为计算图，然后为其生成优化代码。

在下面的示例中，torch.compile 为函数 `fn` 中的所有逐点（pointwise）操作生成单个融合内核。它会即时捕获并编译该函数，如果捕获条件（例如输入形状）发生变化，还可能重新编译。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure1.png)
**图 1**：torch.compile 是 PyTorch 代码的 JIT 编译器。你可以用 torch.compile 包裹函数、nn.Module 以及其他可调用对象。

使用 torch.compile 有多种方式。你可以把它当作内核生成器（如图 1 所示），编译一个函数。但你也可以把 torch.compile 应用于完整的 nn.Module 模型或其子模块。根据模型结构和你自己的需求（例如编译时间），[我们建议在不同的位置应用 torch.compile](https://docs.pytorch.org/docs/stable/torch.compiler_troubleshooting.html#setting-expectations)。

## 为什么要用 torch.compile？

优化模型的一种方式是编写自定义的 CPU/CUDA 算子，使其执行与模型中相同的操作但速度更快。为每个模型编写自定义内核非常耗时，并且需要对性能和硬件有深入理解。torch.compile 几乎不需要额外的工程投入，就能让你向峰值性能迈进相当可观的一段距离。例如，PyTorch 的[开源 TorchBench 基准测试套件](https://hud.pytorch.org/benchmark/compilers)显示，在 80 多个模型上实现了 1.8-2x 的几何平均加速。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure2.png)
**图 2**：torch.compile 为你提供快速的基线性能，为你省下调优模型性能的开发时间。

## torch.compile 的工作原理

torch.compile 流水线由两个主要阶段组成：前端（TorchDynamo）与后端（TorchInductor）。这里只做简要概述，更多细节请参阅 [PyTorch 2 官方论文](https://docs.pytorch.org/assets/pytorch2-2.pdf)。

### 1. 前端（TorchDynamo）：计算图捕获

torch.compile 的前端是一个自定义字节码解释器。它追踪任意 Python 函数，并提取仅由张量操作组成的直线型（straight-line）[torch.fx](https://docs.pytorch.org/docs/stable/fx.html) 计算图。**graph break（图中断）**是 torch.compile 得以良好覆盖各类 Python 代码的关键特性之一。每当 torch.compile 遇到不支持的操作时，它不会报错；相反，它会结束当前正在追踪的计算图，先执行该操作，然后开始追踪一张新的图。torch.compile 会把每张被追踪到的图发送给后端进行优化。

在下面的代码示例中，torch.save 是一个不支持的操作：torch.compile 不知道如何执行磁盘 I/O。对函数 `f` 应用 torch.compile 等价于分别对调用 torch.save 之前的计算区域和之后的区域应用 torch.compile。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure3.png)
**图 3**：torch.compile 捕获由张量操作组成的直线型计算图，并绕过 torch.save 这类不支持的操作。

### 2. 后端（TorchInductor）：优化与内核生成

torch.compile 的后端从前端接收计算图，通过图变换 pass 和向下编译（lowering）到优化后的 C++、triton 或其他内核来优化它们。它能够：

- 融合逐点操作与归约（reduction）操作
- 自动调优内核配置，例如块大小
- 在 matmul 的不同后端（cuBLAS、Triton、CUTLASS）之间选择，并执行 prologue 与 epilogue 融合。
- 使用 CUDA Graph 高效地缓存并重放内核启动

CUDA Graph 是"拥有编译器很有帮助"的一个例子。CUDA Graph 能减少启动开销，但对代码有某些前提假设（例如必须只使用 CUDA 操作，输入张量必须具有静态内存地址）。torch.compile 能够在不支持的操作处自动切分计算图，生成同样可以安全进行 CUDA Graph 捕获的更小的图，并自动管理静态输入缓冲区。

## vLLM 集成

vLLM V1 在在线与离线推理中都默认集成了 torch.compile。你可以用 `-O0` 或 `--enforce-eager` 禁用它，但对大多数用例而言，保持开启能带来性能收益。[更多细节请参阅文档](https://docs.vllm.ai/en/latest/design/v1/torch_compile.html)。

### 编译缓存

vLLM 在冷启动期间编译模型，并把产物（FX 图、Triton 内核）保存到缓存目录（默认为 `~/.cache/vllm/torch_compile_cache`）。热启动时会从缓存中取回产物。你可以通过 `VLLM_DISABLE_COMPILE_CACHE=1` 或删除缓存目录来禁用缓存。

编译产物与缓存在环境相同的不同机器之间可以复用。如果你有自动伸缩的使用场景，请确保生成一次缓存目录，并在实例之间共享。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure4.png)
**图 4**：编译产物在冷启动后被缓存，可在不同机器间复用，只要配置正确，就能保证快速、一致的启动。

### 动态批大小与特化

默认情况下，vLLM 编译一张采用动态批大小、支持所有可能批大小的计算图。这意味着一个产物可以服务不同的输入尺寸。不过，针对已知的批大小——例如 1、2 或 4——进行特化可以带来性能提升。

在配置中使用 `compile_sizes: [1, 2, 4]` 即可触发这种特化。其底层机制是告诉 torch.compile 针对这些静态尺寸进行编译，并可能执行更多自动调优以选出最佳内核。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure5_a.png)![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure5_b.png)
**图 5**：如何指定针对特定批大小的特化编译。

### 分段 CUDA Graph（Piecewise CUDA Graphs）

并非所有操作都与 CUDA Graph 兼容；例如[级联注意力（cascade attention）就不兼容](https://docs.vllm.ai/en/latest/design/v1/torch_compile.html#full-cudagraph-capture)。vLLM 的解决方式是把捕获到的图拆分为 CUDA Graph 安全与不安全的部分，并分别执行。这让我们在不牺牲正确性的前提下获得 CUDA Graph 的性能收益。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure6.png)
**图 6**：vLLM 中的分段 CUDA Graph 捕获并重放受支持的 GPU 内核序列以实现低开销执行，同时跳过级联注意力等不受支持的操作。

## vLLM 中的自定义编译 pass

虽然 torch.compile 内置了许多优化，但 vLLM 添加了自定义编译 pass，应用额外的优化以进一步提升性能。

### 为什么需要自定义 pass？

模型作者编写声明式、模块化的代码，专注于正确性并使用干净的抽象，把更高层的操作拆分为独立的子模块并按层分组。然而，要达到峰值性能往往需要打破这些抽象，例如跨子模块、跨层地融合操作。vLLM 的自定义 pass 不去重写模型，而是重写 torch.fx 计算图。

这些 pass 能够：

- 融合受内存带宽限制的自定义算子，例如激活函数与量化
- 添加 Inductor 中不存在的优化（例如消除多余的无操作 no-op）

### 示例：SiLU + 量化融合

量化 MLP 中的常见模式是 SiLU 激活后接一个量化的下投影（down-projection）线性层。该量化线性层由对输入的量化操作和一个量化矩阵乘法组成。单独来看，SiLU 与量化操作都很慢且受内存带宽限制。借助 Inductor 的模式匹配工具，vLLM 的 `ActivationFusionPass` 自定义 pass 将它们替换为单个融合内核，吞吐量最多提升 8%。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure7.png)
**图 7**：在量化为 FP8 的 Llama 3.1 405B 上（在 8x AMD MI300 上测试），融合内核（`fusion`，黄色）同时优于 `default`（RMSNorm 与 SiLU 使用 torch 算子、FP8 量化使用自定义内核）与 `custom`（未融合的自定义内核）。

![](https://vllm.ai/blog-assets/figures/2025-torch-compile/figure8.png)
**图 8**：上图 `fusion` 与 `default` 两种模式的吞吐量加速对比细节。如果通过融合消除了全部量化开销（8%），吞吐量的理论最大提升为 8%，可以看到某些情况下确实达到了这一提升。

> **注意：** 在 office hours 之后，我们增加了一个使用 torch 算子实现的量化方案，它（在由 Inductor 编译后）比自定义 CUDA/ROCm 内核更快。由于 Inductor 能够自动把这些 torch 算子与 SiLU 的 torch 算子融合，SiLU+quant 与 RMSNorm+quant pass 在某些情况下已不再必要。不过，任何涉及自定义算子的融合（注意力、集合通信、亚字节量化）仍然需要自定义 pass。为了与 office hours 的幻灯片和录像保持一致，我们这里展示 SiLU+Quant 示例，但其他融合 pass 的工作方式非常类似。

### 示例：序列并行 + Async TP

使用张量并行（TP）时，线性层对权重做分片，计算出不完整的矩阵乘法结果，这些结果需要在多个 GPU 之间同步。如果为计算与通信分别使用独立的内核，就会产生通信开销：GPU 在等待通信结果的网络延迟时处于空闲状态。

作为替代，我们可以使用融合的 GEMM+集合通信内核来重叠计算与通信。这类内核的例子包括 GEMM+reduce\_scatter 与 all\_gather+GEMM 内核。要使用这些内核，我们需要把 all\_reduce 集合通信操作分解为 reduce\_scatter 和 all\_gather，同时把 all\_gather 推迟到 layernorm 之后，使它能与随后的 GEMM 融合。

如果要在模型定义中实现这种优化，我们就得改动 vLLM 支持的每一个模型（数以百计！）。这会侵入性强、破坏抽象、增加开发者负担，而且一开始就不太可能被合入 vLLM。相反，通过在 torch.compile 中实现该优化，它只包含 2 个自定义 pass，可以用命令行标志开启，为 vLLM 支持的所有模型带来更好的性能。

> **注意：** 这项优化由社区成员 [@cascade812](https://github.com/cascade812) 完整实现，我们感谢这一了不起的贡献。关于 Async TP 的更多信息见 [PyTorch 博客](https://discuss.pytorch.org/t/distributed-w-torchtitan-introducing-async-tensor-parallelism-in-pytorch/209487)。

### 现有与即将推出的 pass

**现已可用：**

- 融合 pass：
  - RMSNorm + Quant（FP8）融合
  - SiLU-Mul + Quant（FP8）融合
  - Attention + Quant（FP8）融合（最高提升 7%）
  - AllReduce + RMSNorm 融合（最高提升 15%）
  - AllReduce + RMSNorm + Quant（FP8）融合（最高提升 8%）
  - AllReduce + RMSNorm + Quant（FP4）融合（最高提升 10%）
  - 序列并行与 Async TP（最高提升 10%）
- 其他 pass：
  - 无操作消除（No-op Elimination）：消除或简化冗余的 reshape 操作
  - 修复函数化（Fix Functionalization）：手动将 auto\_functionalized 操作重新就地化（re-inplace），以避免冗余拷贝和内存占用

**即将推出：**

- Attention + Quant（FP4）融合：[#22703](https://github.com/vllm-project/vllm/pull/22703)
- SiLU-Mul + Quant（FP4）融合：[#22448](https://github.com/vllm-project/vllm/pull/22448)

Pass 可以通过 `PostGradPassManager`、命令行（`--compilation-config`）或在离线模式下指定配置对象来添加。这让 vLLM 用户无需修改 vLLM 源代码即可执行其用例所需的自定义图变换（内核替换或其他操作）。

## 未来工作

vLLM 与 torch.compile 的集成已经走了很远。以下是未来六个月我们重点关注的一些方向。

**提升稳定性**
vLLM-torch.compile 集成使用了许多私有的（以下划线开头）torch.compile API，并依赖不稳定的实现细节。我们这样做是因为公共 torch.compile API 不足以满足我们的需求——vLLM 需要快速的服务性能，且在模型服务期间不发生重新编译。这导致了一些问题，例如奇怪的缓存问题，或者需要为某些模型禁用 vLLM 的 torch.compile 缓存。PyTorch 编译器团队正在把 vLLM（以及通用推理）相关的特性从 vLLM 上游化到 torch.compile，并将 vLLM 迁移到更稳定的 API。这些特性中的许多已经出现在 torch 2.8 中，[很快](https://github.com/vllm-project/vllm/pull/20358)就会进入 vLLM！

**改善启动时间**
我们听到很多反馈：启动时间是 vLLM 中 torch.compile 与 CUDAGraph 的一大痛点，尤其是在自动伸缩场景下——需要根据需求动态拉起新机器。我们计划显著缩短 vLLM 的冷启动（第一次）与热启动（第二次及以后）时间，特别是与 Dynamo 和 Inductor 编译相关的部分。请在 GitHub 上关注 [startup-ux 标签](https://github.com/vllm-project/vllm/issues?q=is%3Aissue%20state%3Aopen%20label%3Astartup-ux)，或加入 [vLLM Slack](http://slack.vllm.ai) 的 [#feat-startup-ux](https://vllm-dev.slack.com/archives/C0911AKUZQX) 频道来跟进进展！

一项重要的易用性改进是[计划中的 `-O` 命令行标志改版](https://github.com/vllm-project/vllm/issues/20283)。在 vLLM CLI 上指定 `-O<n>`（`n` 是 0-3 之间的整数），用户将能更直接地控制启动时间与性能之间的权衡。`-O0` 几乎不做优化、尽快启动；`-O3` 则耗时更长，但提供尽可能好的性能。

**自定义 pass 改进**
我们计划对自定义 pass 机制做一些广泛的改进，以提高其灵活性、使其更易编写，并提升所应用优化的最终性能：

- 编译多张动态形状的 `torch.fx` 图。这让我们能够根据批大小对前向传播图进行特化，而不必为每个静态尺寸分别编译。更多信息见 [RFC](https://github.com/vllm-project/vllm/issues/23113)。
- 支持匹配自定义算子的 torch 实现。目前，需要启用自定义算子（rms\_norm、quant 等）才能对它们进行模式匹配与融合，但可能有些自定义算子最终没有被融合（尤其是每层发生 4 次的量化）。这些算子比它们的 torch 等价实现更慢，削弱了融合的收益。我们已经有一个对自定义算子的 torch 实现做模式匹配的工作原型，有望带来进一步的性能提升。

**实验性的 torch.compile 后端集成**
我们还在探索实验性的 MPK/Mirage 编译器集成。MPK 是一个精确调度（precision-scheduling）的 megakernel 编译器，即为整个模型前向过程生成单个内核，与 CUDA Graph 相比可以进一步降低 CPU 开销并消除内核启动开销。关于该集成提案的更多信息见 [RFC](https://github.com/vllm-project/vllm/issues/22201)。

**其他性能改进**
vLLM torch.compile 集成的目标是提供良好的基线性能，避免编写和维护大量自定义内核。我们将持续维护并改进性能。一些进行中的工作亮点包括：

- 改进的 [FlexAttention](https://github.com/vllm-project/vllm/issues/19765) 支持。FlexAttention 是一个 API，允许使用不同的注意力变体而无需为每种变体编写自定义注意力内核。其底层使用 torch.compile 生成自定义 triton 模板。
- 对 Flash Attention v2 与 FlashInfer 的[完整 CUDA Graph](https://github.com/vllm-project/vllm/pull/20059) 支持。完整 CUDA Graph 的开销比分段 CUDA Graph 更低，应当能在那些高开销场景下改进性能。

## 结论

torch.compile 为加速 PyTorch 模型提供了一种强大且易于上手的方式。在 vLLM 中，它是推理流水线的核心组成部分。结合缓存、动态形状支持、CUDA Graph 和自定义 pass，它让高效、可扩展的 LLM 服务得以在任何环境中实现。

随着编译器技术栈的成熟和新硬件支持的扩展，torch.compile 与 vLLM 将继续突破推理性能的边界——同时保持模型开发的干净与模块化。
更多关于 torch.compile 的内容请阅读 [PyTorch 文档](https://docs.pytorch.org/docs/stable/generated/torch.compile.html)与 [vLLM 文档](https://docs.vllm.ai/en/latest/design/v1/torch_compile.html)，并欢迎加入 [vLLM Slack](http://slack.vllm.ai) 的 [#sig-torch-compile 频道](https://vllm-dev.slack.com/archives/C08K1FAHFPH)提问、分享反馈、贡献你自己的自定义 pass！

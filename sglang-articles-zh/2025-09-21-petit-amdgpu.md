---
title: "在 AMD GPU 上优化 FP4 混合精度推理"
title_en: "Optimizing FP4 Mixed-Precision Inference on AMD GPUs"
author: "Haohui Mai, Lei Zhang"
date: "September 21, 2025"
previewImg: /images/blog/petit/petit-facade.png
source: https://lmsys.org/blog/2025-09-21-petit-amdgpu/
translated: 2026-09-12
---

# 在 AMD GPU 上优化 FP4 混合精度推理

> 原文：[Optimizing FP4 Mixed-Precision Inference on AMD GPUs](https://lmsys.org/blog/2025-09-21-petit-amdgpu/) · LMSYS Blog · Haohui Mai, Lei Zhang

## 引言

随着前沿大语言模型（LLM）不断扩展到前所未有的规模，它们对 GPU 算力和内存带宽的需求也与日俱增。GPU 厂商和模型开发者都在转向低精度浮点格式。FP4（4-bit 浮点）量化已成为一种极具吸引力的方案——例如，FP4 量化的 [Llama 3.3 70B](https://huggingface.co/nvidia/Llama-3.3-70B-Instruct-FP4) 模型在将模型体积缩小 3.5 倍的同时，在 [MMLU](https://arxiv.org/abs/2009.03300) 等基准测试上仅出现极小的质量下降。

然而，当前的硬件支持存在一个关键缺口。尽管 NVIDIA（GB200）和 AMD（MI350）的下一代 GPU 已提供原生 FP4 矩阵乘法支持，但部署广泛的 AMD Instinct MI250 和 MI300 系列 GPU 却不具备这一能力。这一限制使得用户无法在已有的 AMD 硬件投资上使用高效的 FP4 模型。

为了弥合这一鸿沟，我们开发了 Petit——一组专为 AMD GPU 精心设计的优化 FP16/BF16 × FP4 混合精度 GPU 内核（kernel）。Petit 让 FP4 模型能够在 MI200 和 MI300 系列硬件上运行推理服务，而无需任何硬件升级。

Petit 带来了全面的显著性能提升：

* 使用 [SGLang](https://github.com/sgl-project/sglang) 时，Llama 3.3 70B 的端到端推理性能提升 1.74 倍
* 在等价的矩阵乘法运算上，相比 [hipBLASLt](https://rocm.docs.amd.com/projects/hipBLASLt/en/latest/)（AMD 最先进的 GEMM 库）执行速度最高提升 3.7 倍

Petit 以 BSD 许可证开源，并已自 0.4.10 版本起集成进 SGLang。你可以使用以下命令，在 AMD MI250/MI300x 上开始部署 Llama 3.3 70B 等稠密 FP4 模型：

```
 python -m sglang.launch_server --model-path nvidia/Llama-3.3-70B-Instruct-FP4 --host 0.0.0.0 --port 30000
```


本文将讲述我们的优化历程，以及让这些性能提升得以实现的技术。Petit 充分利用了 AMD 的开放软件生态，同时引入了包括离线重排（offline shuffling）和底层硬件专属增强在内的新颖优化。

## 结合硬件架构协同设计高性能 GPU 内核

现代 GPU 通过在单个晶片上堆叠简单而紧凑的计算单元（CU）来获得海量计算吞吐。然而，这种硬件设计哲学要求应用程序与底层架构进行显式的协同设计，才能发挥最佳性能。如图 1 所示，几条关键的协同设计原则贯穿了 Petit 的开发过程。

<figure>
<img src="/images/blog/petit/arch.svg" alt="Petit 优化总览" style="width:95%">
<figcaption style="text-align: center">图 1：Petit 优化总览。</figcaption>
</figure>

### 通过预处理实现高效反量化

Petit 高效利用 AMD GPU 上专用的 MatrixCore 硬件来加速矩阵乘法。MatrixCore 允许一个 wavefront（由 64 个线程组成的组）高效地协同完成两个 BF16/FP16 16×16 矩阵的相乘。然而，由于 AMD MI300x GPU 并不原生支持 FP4 权重的 MatrixCore 运算，Petit 必须将 FP4 权重反量化为 BF16/FP16 格式，同时还要保证从内存加载 FP4 权重以及将其准备为 MatrixCore 运算格式这两个环节都保持高效率。

这带来了一个根本性挑战：最优的内存加载与 MatrixCore 准备工作要求矩阵 B 处于不同的数据布局。为了内存效率，wavefront 应当加载连续的 1024 字节块；而 MatrixCore 则期望矩阵被切分为 16×16 的 tile，且数值分布到各个 wavefront 上。传统的 GPU 端数据重排会引入显著开销。

面向 NVIDIA GPU 的 [Marlin](https://github.com/IST-DASLab/marlin) 实现通过在磁盘上预先排布矩阵 B 的元素解决了这一问题，从而消除了 GPU 端的重排。将这一方法移植到 AMD GPU 时，我们把 8 个连续的 FP4 值打包进一个 32 位整数，反量化需要 31 条指令。  
Petit 更进一步，针对 AMD GPU 的能力量身定制了位打包格式：我们将前 4 个 FP4 元素按 BF8 布局重排，并把其余元素存入打包整数的剩余位中。借助 AMD 独有的 `v_bfrev_b32` 和 `v_cvt_pk_f32_bf8` 指令以及子双字寻址（SDWA）能力，Petit 仅用 15 条指令即可完成 8 个 FP4 值的反量化，使乘法运算性能提升 30%。

### 驾驭内存层次结构

像 MI300X 这样的 GPU 具有极高的算术密度（\>500），意味着计算单元必须对每个字节执行数百次运算才能达到峰值 FLOPS。因此，最大化有效内存带宽对高性能矩阵乘法内核至关重要。  
Petit 采用了经过验证的技术，例如使用本地数据存储（LDS）进行分块（tiling）和双缓冲，同时解决了若干 AMD 特有的问题：

*避免 LDS bank 冲突*。AMD GPU 的 LDS 被划分为 32 个 bank，每个周期允许对 32 个不同 bank 的并发访问。Bank 冲突会使访问串行化，形成性能瓶颈。由于 AMD GPU 的 wavefront 包含 64 个线程，这一挑战尤为突出。Petit 基于 [bank 设计](https://github.com/nod-ai/shark-ai/blob/main/docs/amdgpu_kernel_optimization_guide.md)实现了置换数据布局，以实现无冲突的 LDS 利用。

*Chiplet 与互连*。AMD MI300 GPU 的每个 chiplet（XCD）拥有 4MB 本地 L2 缓存，并通过互连（interconnect）在所有 XCD 之间共享 256MB L3 缓存。互连虽然提供了高带宽，但也引入了可观的延迟。Petit 实现了拓扑感知的工作负载划分，以最大限度减少互连流量；当性能分析显示互连开销超过收益时，宁可使用朴素的基于网格的划分而非全局条带划分。

### 生成高质量机器码

GPU 使用简单的顺序执行单元来最大化 CU 密度，但这种设计使得分支和流水线停顿的代价格外高昂。AMD GPU 提供条件移动（conditional move）和带边界限制的内存指令，可以彻底消除分支。例如，Petit 使用带指定内存区域范围的 buffer load/store 指令——GPU 会自动丢弃越界访问；同样，超出 64KB 限制的 LDS 访问也会被自动处理。这就在不付出性能代价的情况下消除了内存访问相关的分支。此外，Petit 还提供编译器提示，让 MFMA（矩阵融合乘加，Matrix Fused Multiply-Add）指令与内存访问重叠执行，从而将内存访问延迟有效隐藏在计算之后。

然而，标准编译器未必能充分利用高级的 GPU ISA 能力。例如，有意为之的越界访问属于未定义行为，编译器不会对其优化。这些优化需要细致的人工构建与验证。

## 性能测试结果

### 端到端推理性能

我们通过对比 FP4 与 BF16 模型的端到端推理性能，评估了 Petit 在真实场景中的效果。测试使用 Llama 3.3 70B 的两种变体和 SGLang v0.4.10，测量批大小（batch size）为 10 和 64 个请求时的输入与输出 token 吞吐量。评估在 AMD 开发者云的一台虚拟机上完成，该虚拟机配备 1× MI300X GPU、240 GB 内存和 5 TB SSD，操作系统为 Ubuntu 24.04.1，运行 ROCm 6.4.2。

<figure>
<img src="/images/blog/petit/petit-perf.svg" alt="SGLang 离线生成基准测试中输入与输出 token 的吞吐量" style="max-width:600px">
<figcaption style="text-align: center">图 2：SGLang 离线生成基准测试中输入与输出 token 的吞吐量。</figcaption>
</figure>

图 2 展示了离线生成基准测试的结果。该基准测试使用真实世界的 ShareGPT 轨迹作为输入，能够反映生产环境中的表现。总体而言，Petit 服务 Llama 3.3 70B FP4 模型比 SGLang 服务原始 BF16 模型分别快 1.74 倍和 1.60 倍。在生产环境的小批量场景下，性能受内存带宽限制，Petit 对体积缩小 3.5 倍的 FP4 模型的高效利用直接转化为更优的吞吐量。你可以使用以下命令复现基准测试结果：

```
 python -m sglang.bench_offline_throughput --model-path nvidia/Llama-3.3-70B-Instruct-FP4 --num-prompts 10
 python -m sglang.bench_offline_throughput --model-path nvidia/Llama-3.3-70B-Instruct-FP4 --num-prompts 64
```


## 详细性能分析

随后，我们将 Petit 的性能与 HipBLASLt 进行了对比。HipBLASLt 是 AMD 用底层汇编编写的最先进 GEMM 库。

需要注意的是，这两个库面向的工作负载略有不同：

- Petit：将 BF16 矩阵与 NVFP4 矩阵相乘（16 个元素共享 1 个 FP8 scale）
- HipBLASLt：将两个 BF16 矩阵相乘。

尽管工作负载并非完全相同，但这些结果仍能定量反映 Petit 的表现。我们考察了服务 Llama 3 70B 时实际权重矩阵的尺寸，分别在 m=16（解码负载）和 m=256（预填充负载）下测量性能，在 50 次预热迭代后取 100 次运行的平均值。两个库均调优至最优配置。

<figure>
<img src="/images/blog/petit/fig3a.svg" alt="m=16 时的 GEMM 性能" style="max-width: 60%;">
<br>
<img src="/images/blog/petit/fig3b.svg" alt="m=256 时的 GEMM 性能" style="max-width: 60%;">
<figcaption style="text-align: center">图 3：m=16（解码负载）和 m=256（预填充负载）下的 GEMM 性能。</figcaption>
</figure>

图 3a 和图 3b 展示了 Petit 与 HipBlasLt 的 GEMM 性能。Petit 表现高效：在 m=16（以解码为主的负载）下，Petit 比 HipBlasLt 最高快 3.7 倍，平均提升 2.56 倍；在 m=256（预填充负载）下，Petit 最高比 HipBlasLt 快 1.09 倍，平均性能大致相当。

Petit 在小 m 值下的卓越性能源于内存带宽优化——体积缩小 3.5 倍的 FP4 模型大幅降低了带宽需求。这使得 Petit 在 m 通常很小的真实推理场景中尤为高效，与生产部署模式完美契合。

我们通过逐项增量实现各项技术，研究了每项优化的贡献：高效反量化（Dequant）、消除 LDS bank 冲突（LDS）、拓扑感知的任务放置（Topo）以及高效指令调度（InstSchedule）。图 4 展示了在不同矩阵尺寸下各项优化带来的性能提升分解。

<figure>
<img src="/images/blog/petit/fig4.svg" alt="Petit 各项优化的影响" style="max-width: 600px">
<figcaption style="text-align: center">图 4：Petit 各项优化的影响。</figcaption>
</figure>

我们发现，高效反量化与 LDS 优化带来的收益最大：可带来 70-117% 的性能提升。拓扑感知调度对更大的 m 影响更明显。有意思的是，指令调度的优化效果并不稳定，并不总能带来性能提升。Petit 通过 `amdgcn_sched_group_barrier()` 内建函数（intrinsics）提供编译器提示。要控制 LLVM 内部的贪心调度算法以生成期望的指令序列并非易事，而指数求解器又因运行耗时过长而无法采用。

## 经验与教训

构建 Petit 的历程让我们获得了几点认识：

* 软硬件协同设计是根本。理解硬件架构并围绕其进行设计，应当是一切 GPU 内核优化工作的基础。若缺少恰当的协同设计，无论投入多少其他优化，大量性能潜力都将无从挖掘。  
* 编程语言与编译器支持弥足珍贵。像 [Triton](https://triton-lang.org) 这样的工具能极大提升原型开发和探索阶段的生产力。Petit 的 Tensor 抽象受 [CuTE](https://github.com/NVIDIA/cutlass/tree/main/include/cute) 启发，简化了偏移量计算，缩短了调试时间。尽管编译器可能无法充分利用独特的硬件特性，但暴露性能调优旋钮本身就具有重要价值。  
* 开放生态加速创新。能够接触开源代码库，相比黑盒方案具有巨大优势。研究、改造并在此基础上构建现有优化的能力，同时加速了开发和优化的进程。

## 结语

我们针对 AMD Instinct MI250 和 MI300 GPU 优化 Petit 的工作，展示了软硬件协同设计的变革性力量。通过对算法、内存层次结构优化和底层汇编技术的精心打磨，我们实现了相比最先进实现最高 3.7 倍的性能提升。

Petit 的技术与洞见并不局限于这一特定实现——它们代表了一种方法论：通过深思熟虑的协同设计与优化，从专用硬件中榨取最大性能。

Petit 的完整源代码见：[https://github.com/causalflow-ai/petit-kernel](https://github.com/causalflow-ai/petit-kernel)。

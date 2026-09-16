---
title: "NVIDIA 张量核心演进：从 Volta 到 Blackwell"
title_en: "NVIDIA Tensor Core Evolution: From Volta To Blackwell"
subtitle: "Amdahl 定律、强扩展、异步执行、Blackwell、Hopper、Ampere、Turing、Volta、TMA"
date: 2025-06-23
source: https://newsletter.semianalysis.com/p/nvidia-tensor-core-evolution-from-volta-to-blackwell
crawled: 2026-09-15
authors: ["Dylan Patel", "Kimbo Chen"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA 张量核心演进：从 Volta 到 Blackwell

> 原文：[NVIDIA Tensor Core Evolution: From Volta To Blackwell](https://newsletter.semianalysis.com/p/nvidia-tensor-core-evolution-from-volta-to-blackwell) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Amdahl 定律、强扩展、异步执行、Blackwell、Hopper、Ampere、Turing、Volta、TMA**

在去年年底的 [AI Scaling Laws 一文](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)中，我们讨论了多层叠加的 AI 缩放定律（scaling laws）如何持续推动 AI 产业前进：模型能力的增速超越摩尔定律，单 token 成本也以相称的速度快速下降。这些缩放定律由训练与推理的优化和创新驱动，但超越摩尔定律的算力进步同样功不可没。

在这一战线上，AI Scaling Laws 一文重新审视了围绕算力扩展长达数十年的争论：2000 年代末 Dennard 缩放（Dennard Scaling）走向终结，到 2010 年代末，经典摩尔定律节奏下每晶体管成本持续下降的时代也宣告结束。尽管如此，算力仍在快速提升，接力棒交到了其他技术手中，例如[先进封装](https://semianalysis.com/2021/12/15/advanced-packaging-part-1-pad-limited/)、[3D 堆叠](https://semianalysis.com/2025/02/05/iedm2024/)、[新型晶体管](https://semianalysis.com/2023/02/21/the-future-of-the-transistor/)以及 GPU 这样的专用架构。

![](https://substack-post-media.s3.amazonaws.com/public/images/ff787d2c-5a0d-482a-9e25-a90bcb570073_768x480.png)
*来源：Nvidia*

在 AI 和深度学习领域，GPU 算力的提升速度超过了摩尔定律，年复一年地交出令人瞩目的「[黄氏定律](https://en.wikipedia.org/wiki/Huang%27s_law)」（Huang's Law）性能提升。而驱动这一进步的核心技术，就是张量核心（Tensor Core）。

尽管张量核心无疑是现代 AI 与机器学习赖以奠基的基石，但即便是业内许多资深从业者，对它也谈不上真正理解。GPU 架构以及运行其上的编程模型演进太快，机器学习研究者与科学家越来越难跟上张量核心的最新变化，更难把握这些变化背后的含义。

![](https://substack-post-media.s3.amazonaws.com/public/images/3ef2767c-1f00-44f5-92d2-2cffc1e7152c_1642x972.png)
*来源：SemiAnalysis，HC2023-K2: Hardware for Deep Learning*

在本报告中，我们将介绍历代主流数据中心 GPU 的核心特性，先讲清性能工程中若干重要的第一性原理，随后梳理 Nvidia 张量核心架构与编程模型的演进脉络，重点剖析演进背后的动机。我们的最终目标，是提供一份理解 Nvidia GPU 架构的参考资料，并对其架构演进给出直观的洞见。只有在逐代讲清各代架构之后，我们才能讲透 Blackwell 张量核心之美及其全新的内存层级。

需要说明的是，扎实掌握计算机体系结构是跟上本文许多讲解与讨论的前提；本文会用一小节简要回顾 CUDA 编程作为温习，而不会从零讲解 GPU 架构的基础概念。相反，我们直接站在张量核心知识的前沿，通过详细讲解，把目前散落各处的「圈内口传知识」（tribal knowledge）整理成易懂、有结构的洞见，以此拓展读者对这项前沿技术的理解。

正如大学既开设 101 入门课也开设 4000 级的高阶课，SemiAnalysis 的不同文章也会照顾到读者对主题理解深浅的不同，以及不同职业与专业背景的读者。

我们要感谢以下合作者：

- [Jay Shah](https://research.colfax-intl.com)，Colfax Research：出色的 CUTLASS 教程，以及多次会议中逐字核对技术细节
- [Ben Spector](https://benjaminfspector.com/)，Stanford Hazy Research：对编程模型变迁提出精彩洞见，并给予写作建议
- [Tri Dao](https://tridao.me/)，Princeton 与 Together AI：审阅草稿并给出详细反馈
- [Neil Movva](https://www.neilmovva.com/about/)，Together AI：审阅草稿，并对 GPU kernel 编写提出洞见
- [Charles Frye](https://charlesfrye.github.io/about/)，Modal：教学性的 GPU 词汇表，以及对草稿的整体审阅
- [Simon Guo](https://simonguo.tech/)，Stanford 博士生：绘制封面插图并审阅草稿
- NVIDIA：分享张量核心设计演进的背景。相关人员包括：

  - CUDA 发明人 [Ian Buck](https://x.com/SemiAnalysis_/status/1916204055564849358)
  - GPU 架构与工程负责人 [Jonah Alben](https://x.com/SemiAnalysis_/status/1916204055564849358)
- 以及许多其他 GPU 高手

SemiAnalysis 将从下周开始在 [Instagram Reels](http://instagram.com/semianalysis) 和 [TikTok](https://www.tiktok.com/@semianalysis) 发布独家内容。欢迎关注我们的社交媒体，获取 AI 与 GPU 产业的最新洞见。

## 性能的第一性原理

### Amdahl 定律

对于固定规模的问题，Amdahl 定律给出了通过增加算力资源做并行化所能获得的最大加速比。具体来说，扩展算力资源只能压缩可并行部分的执行时间，因此性能提升的上限受制于串行部分。定量表达为，最大性能提升为：

![](https://substack-post-media.s3.amazonaws.com/public/images/76cfb0cd-a8b0-4083-9f41-87a653bb5eae_1919x522.png)

其中 S 为并行工作的执行时间，p 为可并行工作的加速倍数。在并行部分被完美并行化的理想世界里，加速比 p 可以达到处理单元的数量。

### 强扩展与弱扩展

强扩展（strong scaling）与弱扩展（weak scaling）描述的是在不同问题设定下扩展算力资源所带来的性能提升。强扩展指扩展算力资源去求解一个固定规模的问题，Amdahl 定律量化的正是强扩展的加速比。弱扩展则指扩展算力资源，在固定时间内求解更大的问题。例如，用 4 倍的算力资源在同一时间内处理一张大 4 倍的图像。更详细的解释推荐阅读[这篇博文](https://acenet-arc.github.io/ACENET_Summer_School_General/05-performance/index.html)。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1f3a8a8-bb25-4efc-bd49-52d8c84109b5_2560x1807.png)
*来源：SemiAnalysis，Performance and Scalability - SCENET Summer School*

强扩展与弱扩展在不同问题规模下意味着不同的性能提升。强扩展对任意问题规模都能带来加速，而弱扩展只有在我们用更多算力去求解更大问题时才保证性能提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/75450ff2-fd26-43fc-9fa5-f5b69e75340d_2115x1743.png)
*来源：SemiAnalysis*

### 数据搬运是头等大罪

数据搬运之所以是「罪」，是因为从运行时间和可扩展性角度看，计算廉价而数据搬运昂贵。数据搬运天生更慢：现代 DRAM 存储单元的工作时延在数十纳秒量级，而晶体管的开关速度是亚纳秒级。从扩展性看，虽然计算速度的增益自 2000 年代以来已经放缓，但[内存速度的改善更为缓慢](https://semianalysis.com/2024/09/03/the-memory-wall/)，由此形成了[内存墙](https://en.wikipedia.org/wiki/Random-access_memory#Memory_wall)（memory wall）。

## 张量核心架构演进

### 张量核心世代概览

本节介绍使用张量核心的主要 Nvidia GPU 架构，即 Tesla V100 GPU、A100 Tensor Core GPU、H100 Tensor Core GPU 以及 Blackwell GPU。我们还加入了张量核心之前的章节，作为 CUDA 编程模型的温习。我们会简要过一遍与理解张量核心相关的主要特性与变化，细节则交给各小节中链接的其他资料。

### 前张量核心时代

#### PTX 编程模型

并行线程执行（Parallel Thread Execution，PTX）是一套跨 GPU 世代抽象的虚拟指令集。一个 PTX 程序描述一个**内核函数（kernel）**，由大量 GPU 线程执行，这些线程运行在 GPU 的硬件执行单元、即 CUDA 核心上。**线程**被组织成网格（grid），一个**网格**由若干协作线程数组（**CTA**）组成。PTX 线程可以从多个状态空间访问数据，状态空间是特性各异的内存存储区域。具体来说，每个线程有私有的**寄存器**，同一 CTA 内的线程共享**共享内存（shared memory）**，所有线程都能访问**全局内存（global memory）**。更多信息请阅读 [CUDA 文档的这一节](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#programming-model)。

![](https://substack-post-media.s3.amazonaws.com/public/images/14486127-13d1-46c9-a425-092cd54e2370_573x164.png)
*来源：SemiAnalysis*

#### PTX 机器模型

GPU 架构围绕一组流式多处理器（**SM**）构建。一个 SM 由标量处理核心、多线程指令单元和片上共享内存组成。SM 把每个线程映射到一个标量处理核心（也称 CUDA 核心），多线程指令单元以 32 个并行线程为一组来管理线程，这样的组称为 **warp**。

指令发射时，指令单元选中一个 warp，并向该 warp 的线程发射一条指令。这种执行方式称为单指令多线程（**SIMT**）。与单指令多数据（**SIMD**）类似，SIMT 用一条指令控制多个处理单元；但与 SIMD 不同，SIMT 规定的是单个线程的行为，而非向量位宽。更多信息请阅读 [CUDA 文档的这一节](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#ptx-machine-model)。

![](https://substack-post-media.s3.amazonaws.com/public/images/fa110ab3-2276-452f-9258-ee49b6e38825_1606x1630.png)
*PTX 机器模型。来源：SemiAnalysis，PTX ISA 文档 - 图 4*

#### 流式汇编器（Streaming Assembler）

流式汇编器（Streaming Assembler，SASS）是 PTX 所虚拟化的、与具体架构绑定的指令集。详见 [CUDA 二进制工具文档](https://docs.nvidia.com/cuda/cuda-binary-utilities/index.html#instruction-set-reference)。遗憾的是，由于 NVIDIA 不愿向竞争对手透露其架构 ISA 细节，SASS 的文档十分匮乏。

### Volta

#### NVIDIA 为什么要加张量核心

随着深度学习日益兴盛，业界意识到机器学习负载需要硬件加速。2015 年初，Google 部署 TPUv1 加速其内部机器学习负载；2017 年，Nvidia 推出了面向矩阵运算的专用硬件。GPU 的硬件流水线简单，发射指令的功耗很低（约 30pJ），但 `HFMA` 这类简单浮点操作的功耗更低，只有 1.5pJ。这意味着指令本身的功耗开销，是浮点运算本身的 20 倍。因此，为矩阵乘法执行海量浮点运算在能效上并不划算。要摊薄指令开销，就需要能单条指令完成更多计算的复杂指令。为此，Nvidia 设计了**半精度矩阵乘累加指令（`HMMA`）**——一种执行半精度矩阵乘法的专用指令。执行这条指令的专用硬件就是张量核心，于 2017 年随 Volta 架构的 Tesla V100 GPU 面世。Volta 张量核心是在 Volta 架构开发后期才加入的，距流片只有几个月——足见 Nvidia 调整架构的速度之快。

![](https://substack-post-media.s3.amazonaws.com/public/images/9a4ea94b-3148-4fb8-99d0-46fa53a7adf6_797x226.png)
*来源：《Trends in Deep Learning Hardware: Specialized Instructions Amortize Overhead》*

#### MMA 指令概览

给定矩阵，乘累加（MMA）指令计算 D = A * B + C：

- A 是 M×K 矩阵
- B 是 K×N 矩阵
- C 和 D 是 M×N 矩阵

我们将矩阵形状记作 `mMnNkK` 或 MxNxK。

要完成整个计算，我们首先把矩阵 A、B 和 C 从共享内存加载到线程寄存器，让每个线程持有矩阵的片段（fragment）。其次，我们执行 MMA 指令，从线程寄存器读取矩阵、在张量核心上完成计算，并把结果存回线程寄存器。最后，我们把结果从线程寄存器写回共享内存。整个计算由多个线程协同完成，这意味着每一步都要求协作线程之间做同步。

![](https://substack-post-media.s3.amazonaws.com/public/images/b80e6b8a-9e01-442f-ab3d-9e6d8ecca9ef_2359x2221.png)
*来源：SemiAnalysis*

#### 第一代张量核心——warp 级 MMA

Tesla V100 GPU 的一个 SM 包含 8 个张量核心，按两个一组分区。每个张量核心每周期可完成相当于 4x4x4 矩阵乘法的计算，合计每 SM 每周期 1024 FLOPs。

![](https://substack-post-media.s3.amazonaws.com/public/images/87db8940-a658-48ee-b3bb-8b2a8afdd7c4_1398x784.png)
*来源：Volta Tensor Core Training*

NVIDIA 设计了 PTX 指令 mma 来对应底层的 `HMMA` 指令。在 Volta 架构上，一条 MMA 指令执行一次 8x8x4 矩阵乘法，由 8 个线程组成的 quadpair 协同参与，共同持有输入和输出矩阵。这里 T0 指线程 0，[T0, T1, T2, T3] 和 [T16, T17, T18, T19] 是线程组（threadgroup），两个线程组构成一个 quadpair。

![](https://substack-post-media.s3.amazonaws.com/public/images/85a9c390-e85e-4358-b882-f278ddd50e1e_983x975.png)
*来源：SemiAnalysis，使用 CUTLASS 可视化工具生成*

在数据类型方面，Volta 张量核心支持 FP16 输入、FP32 累加，与 NVIDIA 的[混合精度训练](https://arxiv.org/abs/1710.03740)技术相对应。这项技术证明，用更低精度训练模型也不会损失模型精度。

要完整理解 MMA 布局，请参阅 Citadel 的微基准测试论文[《Dissecting the NVIDIA Volta GPU Architecture via Microbenchmarking》](https://arxiv.org/abs/1804.06826)。要查看 Volta 张量核心 MMA 的交错（interleaved）布局模式，请阅读幻灯片[《Programming Tensor Cores: Native Tensor Cores with CUTLASS》](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9593-cutensor-high-performance-tensor-operations-in-cuda-v2.pdf)。关于 Volta 架构的其他信息，请参阅白皮书[《NVIDIA Tesla V100 GPU Architecture》](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)。

### Turing

Turing 架构包含**第二代张量核心**，是 Volta 张量核心的增强版，新增了 INT8 和 INT4 精度支持。Turing 张量核心支持新的 warp 级同步 MMA，我们将在下一节讨论。Turing 张量核心还催生了深度学习超采样（Deep Learning Super Sampling，DLSS），标志着 NVIDIA 开始把深度学习应用于游戏图形。感兴趣的读者可以参阅 NVIDIA 博客[《NVIDIA Turing Architecture In-Depth》](https://developer.nvidia.com/blog/nvidia-turing-architecture-in-depth/)与 [Turing 架构白皮书](https://images.nvidia.com/aem-dam/en-zz/Solutions/design-visualization/technologies/turing-architecture/NVIDIA-Turing-Architecture-Whitepaper.pdf)。

### Ampere

#### 异步数据拷贝

从 Ampere 开始，NVIDIA 引入了异步数据拷贝，一种以异步方式把数据从全局内存直接拷贝到共享内存的方法。在 Volta 上，要把数据从全局内存加载到共享内存，线程必须先把数据从全局内存加载到寄存器，再存入共享内存。然而 MMA 指令的寄存器占用很高，又必须与数据加载操作共享寄存器堆，造成很高的寄存器压力，并且为数据在寄存器堆的一进一出浪费了内存带宽。

异步数据拷贝从全局内存（DRAM）取数并直接存入共享内存（可选经过 L1），从而缓解这一问题，为 MMA 指令腾出更多寄存器。数据加载与计算可以异步进行——这在编程模型上更难，但能解锁更高性能。

该功能以 PTX 指令、线程级异步拷贝 cp.async 实现（[文档](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#data-movement-and-conversion-instructions-non-bulk-copy)）。对应的 SASS 指令是 LDGSTS，即异步的全局到共享内存拷贝。具体的同步方式是基于 async-group 与 mbarrier 的完成机制，详见[这里](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#data-movement-and-conversion-instructions-asynchronous-copy-completion-mechanisms)。

![](https://substack-post-media.s3.amazonaws.com/public/images/35ec2209-13ce-4a0e-8ff3-7cd5a45918df_1603x339.png)
*来源：NVIDIA A100 Tensor Core GPU 架构白皮书*

#### 第三代张量核心——warp 级同步 MMA

Ampere 每个 SM 有 4 个张量核心，每个张量核心每周期可执行 512 FLOPs，合计每 SM 每周期 2048 Dense FLOPs，性能是 Volta 的两倍。

Volta 需要 8 线程的 quadpair 参与 MMA 运算，而 Ampere 需要整整一个 32 线程的 warp。MMA 指令覆盖整个 warp 简化了 Ampere 的线程布局，并降低了寄存器堆压力。例如，下面是 16x8x16 形状混合精度浮点的线程与数据布局：

![](https://substack-post-media.s3.amazonaws.com/public/images/8e7f8f3e-0bda-4e4c-904f-c90c749dd783_806x1026.png)
*来源：SemiAnalysis，使用 CUTLASS 可视化工具生成*

NVIDIA 在 Ampere 中引入了 `ldmatrix`，一种增强的向量化加载操作。与 `mma` 一样，`ldmatrix` 是 warp 级的，即由一整个 warp 的线程协同加载一个矩阵。与发射多条加载指令相比，这减少了地址生成对寄存器的占用，降低了寄存器压力。更多信息见 [CUDA 文档](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-ldmatrix)。

`ldmatrix` 以与张量核心数据布局相匹配的布局把数据加载到寄存器。与 Volta 的交错模式（见[《Programming Tensor Cores: Native Tensor Cores with CUTLASS》](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9593-cutensor-high-performance-tensor-operations-in-cuda-v2.pdf)）相比，更简单的线程与数据布局大幅改善了编程体验。想深入了解 Ampere 的内存加载如何与张量核心保持一致，请观看 GTC 演讲[《Developing CUDA Kernels to Push Tensor Cores to the Absolute Limit on NVIDIA A100》](https://www.nvidia.com/en-us/on-demand/session/gtcsj20-s21745/)。

Ampere MMA 引入了脑浮点格式（Brain Floating Point Format，BF16），如今已成为半精度数据类型的事实标准。BF16 拥有与 FP32 相同的 8 位指数范围，尾数为 7 位，以一半的存储代价获得 FP32 级别的动态范围。BF16 还省去了混合精度训练中对 loss scaling 的需求。

### Hopper

#### 线程块集群

随着 SM 数量增长，单个 SM 与整颗 GPU 之间的规模差距越拉越大。为了在 CTA（映射到 SM）与网格（映射到整颗 GPU）之间提供更细粒度的控制，NVIDIA 在 Hopper 上新增了一个线程层级——**线程块集群（thread block cluster）**，它映射到物理上位于同一图形处理集群（GPC）内的一组 SM。线程块集群也称协作网格数组（cooperative grid array，CGA），在 CUDA 文档中称为 cluster（[更多信息见此](https://stackoverflow.com/questions/78510678/whats-cga-in-cuda-programming-model)）。

线程块集群内的各 CTA 保证被共同调度到同一 GPC 内的 SM 上，默认每个 SM 分配一个 CTA。这些 SM 的共享内存分区构成**分布式共享内存（DSMEM）**。线程可以通过专用的 SM 间网络（不必经过 L2 缓存）低延迟地访问其他 SM 的共享内存。通过把 GPC 硬件执行单元暴露给编程模型，程序员得以减少数据搬运、改善数据局部性。

![](https://substack-post-media.s3.amazonaws.com/public/images/c36abb58-a0b0-4fc4-8b77-f2636f9a9c61_2028x1004.png)
*来源：GTC 演讲《Inside the NVIDIA Hopper Architecture》*

#### 张量内存加速器

为提升取数效率，NVIDIA 为每个 Hopper SM 加入了张量内存加速器（Tensor Memory Accelerator，TMA）。TMA 是一个专用硬件单元，用于加速全局内存与共享内存之间大批量的异步数据传输（bulk 异步拷贝）。

CTA 中的单个线程即可发起一次 TMA 拷贝操作。TMA 把线程解放出来去执行其他独立工作，由它自己负责地址生成，并提供越界处理等额外好处。在 PTX 中对应的指令是 `cp.async.bulk`，详见 [CUDA 文档的这一节](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#data-movement-and-conversion-instructions-bulk-copy)。

不过，对于小请求，由于地址生成的开销，TMA 加载的时延反而高于常规异步数据拷贝。因此 NVIDIA 建议程序员用 TMA 做大数据拷贝来摊薄开销。例如在 LLM 推理中，TMA 不适合以小块加载 KV 缓存的负载，但当每块是 16 字节的整数倍时表现出色。更具体的例子见 [SGLang 前缀缓存](https://lmsys.org/blog/2024-01-17-sglang/)、论文 [FlashInfer](https://arxiv.org/abs/2501.01005) 第 3.2.1 节、论文 [Hardware-Efficient Attention for Fast Decoding](https://arxiv.org/abs/2505.21487v1) 第 4.2 节，以及 [ThunderKittens MLA decode](https://github.com/HazyResearch/ThunderKittens/blob/mla/kernels/attn/demo/mla_decode/template_mla_decode.cu#L117)。

TMA 还支持一种称为多播（multicast）的加载模式：由多播掩码指定，TMA 将数据从全局内存加载到线程块集群内多个 SM 的共享内存。多播用一次加载即可完成，而不必发射多条全局内存加载指令把同一份数据搬进多个 SM。具体来说，线程块集群内的多个 CTA 各自把一部分数据加载到对应的 SMEM，再通过 DSMEM 共享。这减少了 L2 缓存流量，进而减少 HBM 流量。更多细节推荐阅读 [Jay Shah 的 TMA 教程](https://research.colfax-intl.com/tutorial-hopper-tma/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/7080c7fe-1604-4142-b641-46c4382cc150_1955x1940.png)
*来源：SemiAnalysis，GTC 演讲《Developing Optimal CUDA Kernels on Hopper Tensor Cores》*

#### 第四代张量核心——warpgroup 级异步 MMA

NVIDIA 在 Hopper 上引入了新类型的 MMA——warpgroup 级 MMA（`wgmma`）。`wgmma` 是 warpgroup 级的，即由 4 个 warp 组成的 warpgroup 协同执行一次 MMA 运算。`wgmma` 支持更宽的形状范围。例如，混合精度 MMA 支持 `m64nNk16`，其中 N 可以是 8 到 256 之间 8 的倍数。`wgmma.mma_async` 会 lower 到一套新的 SASS 指令：`GMMA`。再比如，半精度 `wgmma` 指令 lower 到 `HGMMA`。MMA 形状与数据类型的细节见 [CUDA 文档的这一节](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#asynchronous-warpgroup-level-matrix-shape)。

虽然 warpgroup 中所有线程的寄存器共同持有输出矩阵，但 Hopper 张量核心可以直接从共享内存而非寄存器加载操作数，节省寄存器空间与带宽。具体来说，操作数矩阵 A 可以放在寄存器或共享内存中，而操作数矩阵 B 只能通过共享内存访问。`wgmma` 的完成机制、SMEM 布局等细节见 [CUDA 文档 wgmma 一节](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#asynchronous-warpgroup-level-matrix-instructions)。

![](https://substack-post-media.s3.amazonaws.com/public/images/0f36d6b6-04bf-4a81-9112-f31989ea1a08_2425x1903.png)
*来源：SemiAnalysis*

在 `wgmma` 数据类型方面，Hopper 引入了 8 位浮点数据类型（E4M3 与 E5M2），配 FP32 累加。实践中，[累加通路被实现为 22 位定点格式（13 位尾数加符号位与指数位）](https://arxiv.org/abs/2412.19437)，相比真正的 32 位累加限制了动态范围。由于张量核心精度降低，每 N_c 次累加就必须转到 CUDA 核心上执行，以免约束训练精度（[见该论文第 3.3.2 节](https://arxiv.org/abs/2412.19437)）。这种降精度累加提升了效率，但代价是精度。

关于 Hopper 架构的更多信息，请参见：

- GTC 演讲：[Inside the NVIDIA Hopper Architecture](https://www.nvidia.com/en-us/on-demand/session/gtcspring22-s42663/)
- NVIDIA 博客概览：[NVIDIA Hopper Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/)
- 白皮书：[NVIDIA H100 Tensor Core GPU Architecture](https://resources.nvidia.com/en-us-data-center-overview/gtc22-whitepaper-hopper)
- 微基准测试：[Benchmarking and Dissecting the Nvidia Hopper GPU Architecture](https://arxiv.org/abs/2402.13499)
- 微基准测试：[Dissecting the NVIDIA Hopper Architecture through Microbenchmarking and Multiple Level Analysis](https://arxiv.org/abs/2501.12084)

Hopper GPU 编程示例请见：

- GTC 演讲：[Optimizing Applications for Hopper Architecture](https://www.nvidia.com/en-us/on-demand/session/gtcspring23-s51119/?playlistId=playList-43cec6e2-ef10-488a-aba2-6ef775db065a)
- CUTLASS 演讲：[Developing Optimal CUDA Kernels on Hopper Tensor Cores](https://www.nvidia.com/en-us/on-demand/session/gtcspring23-s51413/)
- Colfax 博客：[CUTLASS Tutorial: Fast Matrix-Multiplication with WGMMA on NVIDIA Hopper GPUs](https://research.colfax-intl.com/cutlass-tutorial-wgmma-hopper/)

### Blackwell

#### 张量内存（Tensor Memory）

到 Hopper 这一代，极端的寄存器压力依然没有缓解，由此催生了**张量内存（Tensor Memory，TMEM）**——一块专为张量核心运算设计的新内存。每个 SM 上的 TMEM 有 128 行（lane）乘 512 列 4 字节单元，总计 256 KB，与一个 SM 的寄存器堆大小相同。

TMEM 的内存访问模式是受限的。具体来说，访问整个 TMEM 需要一个 warpgroup，warpgroup 中的每个 warp 只能访问特定的一组 lane。通过限制访问模式，硬件设计师得以减少访问端口数量，节省芯片面积。另一方面，这种设计也意味着 epilogue（收尾）操作需要一个 warpgroup 来执行。与共享内存不同，程序员必须显式管理 TMEM，包括分配、释放以及数据进出 TMEM 的拷贝。

![](https://substack-post-media.s3.amazonaws.com/public/images/fe3575c3-3361-4ba2-a568-a4724a6d8935_1080x1005.png)
*来源：GTC 演讲《Programming Blackwell Tensor Cores with CUTLASS》*

#### CTA 对（CTA Pair）

线程块集群内的两个 CTA，若它们在集群中的秩（rank）仅在最后一位上不同（例如 0 和 1、4 和 5），则构成一个 **CTA 对（CTA pair）**。一个 CTA 对映射到一个纹理处理集群（TPC），后者由两个 SM 组成，并与其他 TPC 一起构成一个 GPC。当 Blackwell 张量核心运算以 CTA 对的粒度执行时，两个 CTA 得以共享输入操作数。这种共享同时降低了 SMEM 容量与带宽需求。

#### 第五代张量核心 MMA

第五代张量核心 MMA 指令（PTX 中的 `tcgen05.mma`）彻底告别了用寄存器存放矩阵的做法。操作数如今驻留在共享内存和张量内存中。

具体来说，设 MMA 计算 D = A * B + D：不再使用线程寄存器，消除了复杂的数据布局，也把线程寄存器空间腾给 epilogue 操作等其他工作。与 `wgmma` 用一个 warpgroup 发起 MMA 运算不同，`tcgen05.mma` 是单线程语义，即由单个线程发起一次 MMA 运算。这把 warp 从 MMA 发射的环节中彻底移除了。

![](https://substack-post-media.s3.amazonaws.com/public/images/1f358583-9d8f-41f0-9d77-720c6907784d_1954x2178.png)
*来源：SemiAnalysis*

一个值得注意的 MMA 变体是 MMA.2SM，它使用 2 个 SM 协同执行一次 MMA 运算。MMA.2SM 以 CTA 对的粒度执行；由于 `tcgen05.mma` 是单线程语义，由 CTA 对中主 CTA（leader CTA）里的单个线程发起 MMA.2SM。这里我们展示数据通路组织的[布局 A](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#tcgen05-data-path-layout-a)。布局 A 显示，相比 1SM 版本（[布局 D](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#tcgen05-data-path-layout-d)），MMA.2SM 将 M 维翻倍，因此两个 SM 加载的是不同的矩阵 A 与 D 分块。此外，MMA.2SM 会拆分矩阵 B，令加载的数据量减半。

![](https://substack-post-media.s3.amazonaws.com/public/images/d86ade4d-5978-4cfc-9c97-a6dffc3f3431_2002x2560.png)
*来源：SemiAnalysis，GTC 演讲《Programming Blackwell Tensor Cores with CUTLASS》*

矩阵 B 在两个 SM 间共享，这意味着分块 B0 和 B1 需要经由 DSMEM 互通。尽管 DSMEM 与 SMEM 存在带宽差异，但由于加载的分块更小，对协同的影响微乎其微。话虽如此，我们猜测在 Blackwell 上，同一 TPC 内 SM 之间的通信带宽高于 DSMEM，MMA.2SM 正是利用了这一点来获得更好的性能。

除通用矩阵乘法外，第五代张量核心还能执行卷积。`tcgen05.mma` 借助收集缓冲区（collector buffer）支持权重驻留（weight stationary）模式，将矩阵 B 缓存以便复用。更多信息请参阅 [CUDA 文档](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#tcgen05-mma)及对应的[权重驻留 MMA 指令](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#tcgen05-mma-instructions-mma-ws)。

在支持的数据类型方面，Blackwell 支持微缩放浮点格式（microscaling floating-point format，MXFP），包括 MXFP8、MXFP6 和 MXFP4，细节见[这篇论文](https://arxiv.org/abs/2310.10537)。Blackwell 还支持 NVIDIA 自有的 NVFP4 格式，其以高于 MXFP4 的精度著称。这大概源于它更小的分块尺寸、不同的缩放因子数据格式，以及两级量化方法（见[这个 GitHub issue](https://github.com/NVIDIA/TensorRT-LLM/issues/3037)）。数据格式对比见[这篇论文](https://arxiv.org/abs/2505.19115)。

在 Blackwell 上，FP8 与 FP6 的理论吞吐相同，因此我们认为它们在张量核心中共用物理电路。相比之下，CDNA4 的 FP6 吞吐是 FP8 的 2 倍，因为其 FP6 单元与 FP4 共享数据通路。我们认为 UDNA 将转而让 FP6 单元与 FP8 共享。

### 侧记：结构化稀疏

Ampere 引入了 2:4 结构化稀疏，理论上可将张量核心吞吐翻倍。其做法是对权重矩阵剪枝，使每 4 个元素中有 2 个为零。在这种格式下，矩阵通过剔除零元素实现压缩，另有一张元数据索引矩阵记录零元素的位置，内存占用与带宽大约减半。

根据[几位硬核中国工程师的微基准测试论文](https://arxiv.org/abs/2501.12084)，Ampere 的结构化稀疏在指令层面可以为大形状 MMA 运算带来 2 倍加速。论文还表明，在 Hopper 上，结构化稀疏 `wgmma` 指令可达 2 倍加速，并将加载权重所用的内存带宽最多节省 2 倍。

遗憾的是，在 Hopper 上，2:4 结构化稀疏的 GEMM kernel 相比稠密版本远达不到 2 倍加速。原因在于：结构化剪枝难以维持模型精度、cuSPARSELt kernel 未充分优化，以及 TDP 限制。除了中国的 AI 实验室和数量有限的西方实验性[研究](https://arxiv.org/abs/2503.16672)[论文](https://developers.redhat.com/articles/2024/12/18/24-sparse-llama-fp8-sota-performance-nvidia-hopper-gpus)，大多数 AI 实验室在生产推理中无视 2:4 结构化稀疏，专注量化与蒸馏。Meta 正在 Llama 中试验，但在很多情况下这也是一条死路。

此外，目前缺乏任何闭源或开源模型，能在保持零精度损失的同时，借由 2:4 FP8 结构化稀疏或 4:8 FP4 结构化稀疏展现出性能提升；投入结构化剪枝的资源也[普遍不足](https://github.com/NVIDIA/TensorRT-Model-Optimizer/blame/main/modelopt/torch/sparsity/sparsegpt.py)。我们建议 NVIDIA 停止在主题演讲和营销材料中用「[Jensen 数学](https://semianalysis.com/2025/03/19/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman/#jensen-math-changes-every-year)」宣传结构化稀疏 FLOPS——除非他们能持续拿出利用结构化剪枝做推理的 SOTA 开源模型。一个好的第一步，是对 DeepSeek 做结构化稀疏，并证明其性能收益可以与蒸馏、量化（如 NVFP4）等其他技术叠加。

![](https://substack-post-media.s3.amazonaws.com/public/images/df23f81d-3638-4bc4-835b-6b45e888fa80_660x511.png)
*来源：NVIDIA*

在第五代张量核心中，NVIDIA 为 NVFP4 数据类型引入了成对（pair-wise）4:8 结构化稀疏。在该方案中，每 8 个元素被分成 4 个连续的元素对，其中恰好两对必须包含非零值，其余两对被剪为零。由于 NVFP4 是一种子字节（sub-byte）数据类型，我们认为正是这一约束促使 NVIDIA 采用成对 4:8 模式。尽管 4:8 稀疏看起来比早先的 2:4 模式更宽松，但新增的成对要求意味着，对于希望在剪枝的同时保住模型精度的机器学习工程师而言，它在实践中并不是一个更松的约束。

![](https://substack-post-media.s3.amazonaws.com/public/images/18969216-d3c3-440d-b503-b216c24bd9c7_809x355.png)
*来源：NVIDIA*

### 张量核心规模的增大

![](https://substack-post-media.s3.amazonaws.com/public/images/d9aa9938-e0cf-4bff-92e4-2ac1f73a0f34_1566x632.png)
*来源：SemiAnalysis，NVIDIA*

一代代演进下来，NVIDIA 扩大张量核心单个规模的力度远大于增加张量核心数量。NVIDIA 之所以选择扩大核心规模而非增加核心数量，是因为这更契合矩阵乘法的性能特征。具体来说，随着问题规模扩大，矩阵乘法的计算量呈三次方增长，而数据搬运量呈二次方增长，意味着算术强度（arithmetic intensity）线性增长。O(n) 的算术强度，叠加数据搬运比计算更昂贵这一事实，共同驱动了张量核心规模的增大。

![](https://substack-post-media.s3.amazonaws.com/public/images/c02c8a89-11eb-4d89-8e55-d84fd8139d11_882x350.png)
*来源：SemiAnalysis，NVIDIA*

然而，无论扩大核心规模还是增加核心数量，都要付出量化效应的代价。具体来说，核心数量多会受[分块量化效应](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html#tile-quant)（tile quantization）之苦，而单个核心规模大会导致[波量化效应](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html#wave-quant)（wave quantization）。当工作单元的数量不能被工作者数量整除时，就会发生波量化效应：处理最后一批较小的作业时利用率下降。增大张量核心规模本质上是在增大工作单元的尺寸，导致小矩阵场景下利用率低下（见这篇 [ThunderKittens 博文](https://hazyresearch.stanford.edu/blog/2025-03-15-tk-blackwell)）。

![](https://substack-post-media.s3.amazonaws.com/public/images/843361b2-221e-4114-a346-56a0d163e482_2560x988.png)
*来源：SemiAnalysis*

算术强度的线性增长也推动着 MMA 形状增大。更大的 MMA 形状提升了操作数共享的粒度。具体来说，发射更少、更大的分块会提高数据复用，节省寄存器堆和 SMEM 的内存占用与带宽。在 Blackwell 之前的架构上，这体现为协同执行一次 MMA 运算的线程数不断增加：从 8 线程的 quadpair（Volta），到 32 线程的 warp（Ampere），再到 128 线程的 warpgroup（Hopper）。

### 内存容量的增长

![](https://substack-post-media.s3.amazonaws.com/public/images/069490a4-6b85-41c1-b5da-4a4c4f1729c4_1464x432.png)
*来源：SemiAnalysis，NVIDIA*

共享内存几乎每一代都在增大，而寄存器堆大小保持不变。原因在于张量核心吞吐的增长需要更深的暂存缓冲。

由于张量核心消费数据的速度远快于全局内存的加载速度，我们用一块暂存内存来缓冲数据，让内存加载可以跑在 MMA 运算前面。**张量核心吞吐每代翻倍，但全局内存加载时延没有下降、反而上升。因此，我们需要更大的暂存内存来缓冲更多数据。**为实现这一点，NVIDIA 选择共享内存作为张量核心的暂存内存，这就解释了为什么共享内存不断增大而寄存器堆大小保持不变。

然而，Blackwell 的共享内存相比 Hopper 并没有增大。这是因为 tcgen05 MMA 可以调动 2 个 SM，每个 SM 的共享内存只需加载一半的操作数。因此，Blackwell 的共享内存实际上是翻倍的。

NVIDIA 对暂存内存的选择也解释了操作数位置为何逐渐从寄存器迁移到共享内存。话虽如此，NVIDIA 还是在 Blackwell 上新增了 TMEM，以支撑更高的张量核心吞吐。由于 TMEM 布置得离张量核心更近，它可以更省电。此外，一块独立的内存增加了总内存带宽，有助于喂饱张量核心。

在所有操作数中，矩阵 D 始终驻留在 TMEM。这一设计可以充分利用 TMEM 的能效优势，因为矩阵 D 的访问频率高于矩阵 A 和 B。例如，在朴素的分块矩阵乘法中计算一个分块，矩阵 D 的分块会被访问 2Kt 次（Kt 次读加 Kt 次写。Kt：K 维度上的分块数），而矩阵 A 和矩阵 B 的分块只被访问一次。

![](https://substack-post-media.s3.amazonaws.com/public/images/55a6a58d-8317-4267-a501-1d39961b4ce8_1476x474.png)
*来源：SemiAnalysis，NVIDIA*

### MMA 指令的异步性

![](https://substack-post-media.s3.amazonaws.com/public/images/b266ea7a-4b6c-4dce-89d8-c429887d75c6_882x270.png)
*来源：SemiAnalysis，NVIDIA*

`UTCHMMA、HGMMA、HMMA` 中的「H」代表半精度（16 位格式）；`QGMMA、UTCQMMA` 中的「Q」代表四分之一精度（8 位），因为 8 位是全精度（32 位）的四分之一；「O」代表「Octal」，即 32 位的八分之一，因为 `UTCOMMA` 是 FP4。

MMA 指令表面上是从同步一步跳到异步。实际上，MMA 指令是在 SASS 层面逐渐异步化的，起因是需要与 `LDSM` 指令做重叠。

在 SASS 层面，一次 MMA 运算要执行一条 `LDSM` 指令把矩阵分块从共享内存加载到寄存器堆，然后执行两条 `HMMA` 指令完成 MMA。执行过程中，两条 `HMMA` 指令异步发射，并通过硬件互锁（interlock）阻塞寄存器的使用。由于硬件互锁不允许 LDSM 指令与之重叠，一条 `LDSM` 加两条 `HMMA` 的顺序执行会在指令发射流水线中形成一个小气泡（bubble）。然而，张量核心已经快到这个气泡会造成不可忽视的性能损失，这就呼唤 MMA 的异步完成机制。

Hopper 为 `wgmma` 提供了异步完成机制 commit 与 fence。`HGMMA` 指令发射时，不再有硬件互锁保护寄存器使用。取而代之的是，编译器为下一次 MMA 调度 `LDSM`，并用 `FENCE` 指令让下一条 `HGMMA` 等待。到了 Blackwell，MMA 运算完全异步。加载到张量内存的指令（[tcgen05.ld /](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#tcgen05-memory-consistency-model-async-operations) [tcgen05.st](http://tcgen05.st) [/ tcgen05.cp](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html?highlight=tcgen05%2520cp#tcgen05-memory-consistency-model-async-operations)）全部显式异步。

![](https://substack-post-media.s3.amazonaws.com/public/images/af48362e-e494-4efe-8d03-17e28243e2fa_1868x1235.png)
*来源：SemiAnalysis*

### 数据类型精度降低

![](https://substack-post-media.s3.amazonaws.com/public/images/451a1b28-b226-4e4d-b778-8e674314e4da_1956x960.png)
*来源：SemiAnalysis，NVIDIA*

在 NVIDIA 张量核心的每一代演进中，NVIDIA 持续加入更低精度的数据类型，从 16 位一路降到 4 位。这是因为深度学习负载对低精度极其宽容。推理尤其如此——推理可以使用比训练更低的精度。低精度更省电、占用更少的芯片面积，并能实现更高的计算吞吐。在较新的几代中，我们还看到 NVIDIA 砍掉 FP64 支持，在芯片面积和功耗预算下优先低精度数据类型。

有趣的是，这种优先级也影响了对整数数据类型的支持。自 Hopper 起，INT4 数据类型被弃用；在 Blackwell Ultra 上，我们看到 INT8 计算吞吐下降。这是低精度整数数据类型普及滞后所致。尽管 Turing 早就支持 INT8 和 INT4，但直到 4 年之后，新的推理量化方法才得以利用 INT4 的紧凑性来服务 LLM。到那时，NVIDIA 已经在 Hopper `wgmma` 上弃用了 INT4。

接下来，我们将讨论编程模型的演进，包括从高占用率（high-occupancy）到单占用率（single-occupancy）的转变、显式异步执行的增多，以及这些设计与 NVIDIA 押注强扩展之间的关系。

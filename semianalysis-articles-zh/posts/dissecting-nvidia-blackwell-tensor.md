---
title: "解剖 NVIDIA Blackwell——张量核心、PTX 指令、SASS、Floorsweep 与良率"
title_en: "Dissecting Nvidia Blackwell - Tensor Cores, PTX Instructions, SASS, Floorsweep, Yield"
subtitle: "微基准测试、tcgen05、2SM MMA、UMMA、TMA、LDGSTS、UBLKCP、Speed of Light、分布式共享内存、GPC Floorsweep、SM 良率"
date: 2026-03-31
source: https://newsletter.semianalysis.com/p/dissecting-nvidia-blackwell-tensor
crawled: 2026-09-15
authors: ["Kimbo Chen", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 解剖 NVIDIA Blackwell——张量核心、PTX 指令、SASS、Floorsweep 与良率

> 原文：[Dissecting Nvidia Blackwell - Tensor Cores, PTX Instructions, SASS, Floorsweep, Yield](https://newsletter.semianalysis.com/p/dissecting-nvidia-blackwell-tensor) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**微基准测试、tcgen05、2SM MMA、UMMA、TMA、LDGSTS、UBLKCP、Speed of Light、分布式共享内存、GPC Floorsweep、SM 良率**

NVIDIA 的数据中心 Blackwell GPU（SM100）堪称一代人之内最重大的 GPU 微架构变革之一，然而至今没有一份详细的白皮书。直到今天，市面上也不存在针对数据中心 Blackwell 架构的公开微基准测试研究——针对 PTX 与 SASS 指令（如 UMMA 和 TMA）、并聚焦 AI 工作负载的那种。

在我们深度撰写的[《NVIDIA 张量核心演进：从 Volta 到 Blackwell》](https://newsletter.semianalysis.com/p/nvidia-tensor-core-evolution-from-volta-to-blackwell)一文之后，SemiAnalysis 又投入了数月的工程时间，深入剖析 Blackwell 架构并测量原始 PTX 指令性能，以确立坚实的实际性能上限，并将其与理论峰值对比。我们这样做是为了摸清单元级和指令级的硬件吞吐与延迟极限，从 ML 系统与内核（kernel）开发的角度提供一份有用的特性刻画。我们聚焦深度学习工作负载配置，例如对流行深度学习库 FlashInfer 所用异步内存拷贝方案的基准测试。

我们已在[此处](https://github.com/SemiAnalysisAI/microbench-blackwell)开源了我们的 Blackwell 微架构级基准测试仓库。如果对你有用，欢迎点个 star。

# 致谢

感谢 Nebius 和 Verda 为微基准测试提供 B200 节点。他们的 B200 节点启用了正确的硬件计数器，使 NCU 性能剖析成为可能。对于使用未启用 NCU 的云服务商的用户，GPU Mode 的 Mark Saroufim 给出了[一个变通方法](https://x.com/marksaroufim/status/2018739807363674373)。我们还要感谢 [Dissecting the NVIDIA Hopper Architecture through Microbenchmarking and Multiple Level Analysis](https://github.com/HPMLL/NVIDIA-Hopper-Benchmark) 和 [tcgen05 for dummies](https://github.com/gau-nernst/learn-cuda/tree/main/02e_matmul_sm100) 的作者们，我们的代码正是基于他们的工作构建的。

最后，感谢我们所有的审阅者与外部合作者：

- Kilian Haefeli - Cohere
- Benjamin Spector - Flappy Airplanes 与斯坦福（Stanford）
- Neil Movva - Sail Research
- Orian Leitersdorf - Decart AI
- Hardik Bishnoi - Arcee AI
- 以及众多匿名审阅者

![](https://substack-post-media.s3.amazonaws.com/public/images/7e5c8ca9-ca65-4217-94fb-3c5fd9946bc1_200x200.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/44d04885-53a0-4567-bd9f-d2ebb5a712c8_200x200.png)

# 后续工作

本文是探索 AI 加速器底层汇编与内核代码系列的第一篇。在后续篇章中，我们将扩展这项工作，对更多 Blackwell 与 Blackwell Ultra 的 PTX 指令进行基准测试，包括 EXP2 和 TensorMap 更新延迟。此外，我们已有具体计划对 TPU Pallas 内核、Trainium NKI 内核和 AMD CDNA4 汇编进行基准测试。尤其是 AMD CDNA4，由于[许多指令已有完善的文档](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/amd-instinct-cdna4-instruction-set-architecture.pdf)，基准测试在近期内就触手可及。

如果你想从事底层基准测试、ClusterMAX、推理模拟器或其他有趣的技术工作，欢迎加入我们。请将简历发送至 [letsgo@semianalysis.com](mailto:letsgo@semianalysis.com)，并附上 5 条要点展示你卓越的工程能力。请附上 GitHub 仓库链接、YouTube 演示、网站、博客等以支撑你的要点。

# Blackwell 特性

从 Hopper 到 Blackwell，NVIDIA 对架构做了若干渐进式改进，并调整了 MMA 相关指令的 PTX 抽象。我们在[《NVIDIA 张量核心演进》](https://newsletter.semianalysis.com/i/174558646/blackwell)一文中涵盖了其中大部分。主要显著变化如下：

- 引入张量内存（TMEM）来保存 MMA 累加器。线程不再隐式拥有 MMA 运算的结果，而是由软件在 MMA 作用域内对 TMEM 进行显式管理
- `tcgen05` 操作现在由单个线程代表整个 CTA 发出，而不再像前几代那样在 warp 或 warpgroup 作用域发出。你可以在 CuTe MMA atoms 中看到这一变化：[Blackwell 中](https://github.com/NVIDIA/cutlass/blob/main/include/cute/atom/mma_traits_sm100.hpp#L1045)现在使用 `ThrID = Layout<_1>`，而 [Hopper 的 warpgroup 作用域 MMA](https://github.com/NVIDIA/cutlass/blob/main/include/cute/atom/mma_traits_sm90_gmma.hpp#L491) 使用的是 `ThrID = Layout<_128>`
- 支持跨一对协同 CTA 的 TPC 作用域 TMA 与 MMA，在 PTX 中以 `cta_group::2` 暴露、在 SASS 中为 `2CTA`——组成一个 TPC 的两个 SM 可以对共享操作数执行 `tcgen05.mma`，通过降低每 CTA 的 SMEM 带宽需求来提供对更高运算强度（operational intensity）MMA 指令的访问。后文将证明，这种操作数共享是用满可用 MMA 吞吐的必要条件
- 原生支持带微缩放（micro-scaling）的子字节数据类型
- [Cluster Launch Control（CLC）](https://docs.nvidia.com/cutlass/latest/media/docs/cpp/blackwell_cluster_launch_control.html)作为持久 CTA（persistent-CTA）内核中动态工作调度的硬件支持（将在后续文章中介绍）
- [Programmatic dependent launch（PDL）](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/programmatic-dependent-launch.html)在 Hopper 中引入，用于隐藏背靠背内核的启动与设置延迟（将在后续文章中介绍）

# 集群（Cluster）、GPC 与 Floorsweep

自 Hopper 以来，NVIDIA 数据中心 GPU 支持一项可选特性，它有多个名字，比如「线程块集群（thread block clusters）」「CTA 集群（CTA clusters）」和「协同网格阵列（cooperative grid arrays，CGA）」，指的都是同一特性。集群是 CTA 的逻辑分组，其形状和大小可以按内核静态或动态指定。集群在编程模型中以一些有用的方式可见，其中之一是允许向同一集群内的多个 CTA 进行多播加载；我们稍后会在 TMA 多播的语境下讨论这一点。

重要的是，同一集群内的 CTA 保证会被共同调度到同一个 GPC 上。这对于每 SM 一个 CTA 的「持久 CTA」式 Blackwell 内核有一个重要后果：如果集群大小不能整除一个 GPC 内的 SM 数量，部分 SM 就会闲置。这一行为可能让内核作者感到困惑——他们在不了解文档稀缺的 GPC 的情况下，天真地在启用集群时启动与 SM 数量相等的持久 CTA，结果导致部分 CTA 被串行执行。

每个 GPC 因良率而被屏蔽的 SM 数量并不固定，同一芯片上各 GPC 之间也不相同，甚至同一封装内两颗裸片（die）之间也可能不对称。半导体制造会产生缺陷，而缺陷可能落在芯片的任何位置。因此，NVIDIA 必须在设计芯片时就做好工程处理，使得经过这种良率屏蔽之后，可用单元仍能以相对统一的方式呈现给软件。

我们让 Claude 写了一个实用工具，通过启动不同大小的集群并使用 PTX `%%smid` 记录哪些 SM 出现在同一 GPC 中，从而逆向推导 SM 到 GPC 的映射关系。结果是一份 TPC 到 GPC 的逻辑分组列表。这份列表比 Hopper/Blackwell 实际拥有的 8 个 GPC 要长，因为有一些 TPC 似乎独占一个逻辑 GPC，从不与其他 TPC 共同调度。

![](https://substack-post-media.s3.amazonaws.com/public/images/4647ae85-dc9e-4c79-a203-47909a997e1b_1184x268.png)

从 SM100 开始，NVIDIA 为这一量化（quantization）问题提供了解决方案，使内核既能获得更大集群的好处，又能用上所有可用 SM。内核可以用两种集群大小启动：首选集群大小（preferred）和回退集群大小（fallback）。一般来说，要想用满整颗 GPU，回退集群大小应为 2 或 1。

参考资料：

- [Cluster API](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-host-programming.html#launching-with-clusters-using-cudalaunchkernelex)
- [Cooperative groups API](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cooperative-groups.html)
- `CU_LAUNCH_ATTRIBUTE_PREFERRED_CLUSTER_DIMENSION`
- [CUTLASS Example 73](https://github.com/NVIDIA/cutlass/blob/main/examples/73_blackwell_gemm_preferred_cluster/blackwell_gemm_preferred_cluster.cu)

## 逻辑 GPC 与物理 GPC

上面给出的 TPC 到 GPC 分组是*逻辑*分组。它们代表软件视角下的 GPC，既不包含每个 GPC 中实际 20 个物理 SM 里哪些被启用的信息，也不包含每个物理 GPC 位于两颗裸片上的什么位置。实际上，逻辑配置相同的 B200 芯片，各 GPC 中因良率屏蔽的物理 SM 未必完全相同。这可能在软件看来完全相同的 GPU 之间造成潜在的性能不确定性。此外，SM 到 GPC 的逻辑分组也完全无法告诉我们 B200 封装中两颗裸片各包含哪些 GPC。

为了进一步探明 SM 的物理布局，我们让每个 SM 遍历一个填满 L2 缓存的指针追踪（pointer-chase）数组，并测量每次加载的延迟。对每个地址，我们将每个 SM 观察到的延迟与其他所有 SM 观察到的延迟进行比较，生成一张 SM<->SM 距离矩阵。X 轴和 Y 轴均为 SM ID。

![](https://substack-post-media.s3.amazonaws.com/public/images/59a90c5b-7a40-4984-9872-717122402fe0_1600x1353.png)

我们可以看到明显分开的两组 SM，它们到 L2 的平均延迟差距超过 300 个时钟周期；这必然就是裸片间互访（die-to-die crossing）。我们还用上一节识别出的逻辑 GPC 分组为 SM 打了标签；有趣的是，那些单例 TPC 彼此靠近，且在本基准测试中与 GPC0 相当吻合，因此可以猜测这些 TPC 物理上就位于 GPC0。

基于这些信息，我们可以细化每个 GPC 因良率屏蔽的 TPC 数量，不过其中的 5+3 仍然只是猜测。

**裸片 A**：[10, 10, 10, 9]

**裸片 B**：[9, 9, 9, 5+3]

此外，虽然方式有些迂回，我们可以得出裸片间互访的延迟惩罚约为 300 个时钟周期。从基准测试中单个 SM 的延迟剖面也能看出这一点（其中也包含大量 L2 拥塞的影响）：

![](https://substack-post-media.s3.amazonaws.com/public/images/bec3b195-e042-4f89-b7b7-52e79a20d31b_2048x1015.png)

感谢 Decart AI 的 Orian 为该基准测试提供的灵感。

# 内存子系统

在本节中，我们讨论内存子系统：在计算单元之间搬运数据的硬件单元。内存拷贝指令是使用内存子系统的操作，较新的几代 GPU 引入了异步拷贝指令（异步能力的演进可阅读[上一篇文章](https://newsletter.semianalysis.com/i/174558646/asynchronous-execution)）。这里我们聚焦两类异步拷贝指令：LDGSTS 和 TMA（Tensor Memory Accelerator）。

## 异步拷贝（Async Copy）

异步拷贝（PTX：`cp.async`，SASS：`LDGSTS`）在 Ampere 一代引入，该指令将数据从全局内存异步搬运到共享内存。异步拷贝是非阻塞的，允许内存加载与计算重叠。它还直接写入共享内存而不经过寄存器，从而降低寄存器压力。

参考 FlashInfer 的多头注意力（MHA）内核，我们用以下配置对异步拷贝进行基准测试：

- 每 SM 的 CTA 数：1、2、3、4
- 级数（Stages）：1、2、4
- 每 CTA 线程数：64、128、256
- 加载大小：4B、8B、16B

我们绘制了吞吐量与每 SM 在途字节数（bytes-in-flight，即并发内存加载指令正在加载的总字节数）的关系。

尽管不同加载大小在相同在途字节数下会收敛到相近的吞吐量，我们更偏好 16 字节加载。16 字节加载在相近的在途字节数下能取得略高的吞吐量，同时消耗更少的执行资源。例如，在 32 KiB 在途时，8B 加载需要 4 级，而 16B 加载只需 2 级。这省下了两个内存屏障对象的内存空间，并降低了指令发射压力。

![](https://substack-post-media.s3.amazonaws.com/public/images/763336d2-7438-44f3-879b-f3116360c0ac_1600x1033.png)

总体来看，`LDGSTS` 的内存吞吐量在 32 KiB 在途时饱和于约 6.6 TB/s。

我们还对多潜在注意力（MLA）内核所用的配置空间进行了基准测试：

- 每 SM 1 个 CTA
- 16B 加载
- 每 CTA 线程数：64、128、256
- 级数：4、8、12、16

实验表明，增加级数可以在更高的在途字节数下取得更高吞吐量；而增加每 CTA 线程数在所有配置下都严格改善性能。有趣的是，MLA 使用 2 个 warp 和 12 级，最终落在约 2.2 TB/s。我们认为这是因为 softmax 的 warp 需要的寄存器最多，而增加 warp 数量会减少每线程的寄存器分配。

![](https://substack-post-media.s3.amazonaws.com/public/images/337b9825-d13a-44ed-85f5-df0aec71ba9b_1600x684.png)

我们对同一组配置测量了延迟。可以看到 `LDGSTS` 的基线延迟约为 ~600 纳秒，在途字节数超过 8 KiB 后延迟近乎翻倍。这是因为要让 `LDGSTS` 达到高在途字节数，需要使用大量线程，导致大量 warp 因 MIO（内存输入输出）节流而停滞。

![](https://substack-post-media.s3.amazonaws.com/public/images/9381e20a-0318-4284-af11-d1cf13a4c450_1600x977.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/7888d3c1-270d-4d5e-a940-301c70813f89_1544x206.png)

## 张量内存加速器（TMA）

TMA（PTX：`cp.async.bulk.tensor`，SASS：`UTMALDG`）是 Hopper 一代引入的异步数据拷贝引擎，专用于将大量数据从全局内存搬运到共享内存。单个线程即可发起 TMA，由它完成地址生成、内存 swizzling 和越界处理，从而释放其他线程去执行独立工作。这里我们对 2D 张量版本（cp.async.bulk.tensor.2d）进行基准测试，以代表典型的 TMA 用法。

参考 FlashInfer 的注意力内核，我们对 TMA 进行基准测试：每 SM 只分配一个 CTA，但让每 CTA 的 1 到 4 个 warp 各出一个线程发射不同 box 大小的 TMA 指令。下图展示了每个在途字节数下的最佳吞吐量。

我们用以下配置对 TMA 进行基准测试：

- 每 SM 的 CTA 数：1
- 每 CTA 线程数：128（4 个 warp）
- TMA box 维度：从 32x8 逐渐增大到 128x128 的 2D 形状

![](https://substack-post-media.s3.amazonaws.com/public/images/7a47a042-7c59-4cc1-8459-665852a23321_1600x720.png)

TMA 达到峰值吞吐量的时点远晚于 `LDGSTS`。

## 异步拷贝与 TMA 对比

FlashInfer 等深度学习内核库在加载数据时同时使用 TMA 和异步拷贝。两者性能特性不同：TMA 擅长访问模式规整的大块加载，但延迟更高；异步拷贝能处理不规则的内存访问模式，但有大小限制。我们会解释在什么条件下应选择哪一个。这里我们对 FlashInfer 用于 MHA 和 MLA 内核的配置进行基准测试。

可以看到，在吞吐量方面，在途字节数低于 32 字节时异步拷贝略优于 TMA，但超过该值后 TMA 追了上来并可以继续扩展到 128 KiB。在延迟方面，在途字节数低于 12 KiB 时异步拷贝的延迟略低于 TMA，但超过该值后 TMA 的延迟大幅增加。

![](https://substack-post-media.s3.amazonaws.com/public/images/74e024c1-60ab-44e4-8acb-69760e4fcba2_1600x678.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/838e8420-6671-4ffe-afdd-66c2581ada03_1600x677.png)

在实际中，Blackwell 的 MLA 内核使用异步拷贝来动态加载页（page），而其 MHA 内核只使用 TMA。FlashInfer 的大部分 Blackwell MHA 内核由 TRT-LLM 贡献，因此我们只能通过研究二进制文件来推测这些内核的行为。我们发现与 Hopper 类似，所有 Blackwell TRT-LLM 内核都使用 TMA。我们猜测，在动态页加载方面，这些内核沿用了 Hopper 内核的做法：使用以页索引为最后一维的 4D TMA，并在需要时对 `TensorMap` 对象做索引。为了理解这些内核的确切机制，我们敦促 NVIDIA 开源 FlashInfer 的 TRT-LLM 内核，造福社区。

## TMA 多播

TMA 支持多播模式：单次加载即可将数据拷贝到多个 SM 的共享内存，由 CTA 掩码指定。多播常见于类 GEMM 模式，即处理不同输出 tile 的 SM 之间共享输入 tile。例如，多播对激活函数 SwiGLU 很有用，它采用双 GEMM 模式——两个 GEMM 运算共享一个输入矩阵。主要好处是减少 HBM 加载，降低有效带宽占用。它还能显著减少 L2 流量，因为多个 CTA 对共享数据的请求会被合并为一个请求。

根据 NCU 的信息，负责处理 TMA 多播请求的单元叫做 L2 Request Coalescer（LRC）：

L2 Request Coalescer（LRC）处理发往 L2 的传入请求，并在将读请求转发给 L2 缓存之前尝试合并它们。它还处理来自 SM 的程序化多播请求，并支持写入压缩。

听起来硬件可能会提供某种隐式多播行为——即便没有人显式请求，类似 miss status holding register 那样。我们对此进行了测试：运行同样的 TMA 多播基准，只是不再由一个 CTA 发出多播加载，而是所有 CTA 对同一数据各自发出普通 TMA 加载。

我们在此对比以下三种情形：

1. 每个 SM 加载不同的数据（基线）
2. TMA 多播（显式）——每个集群中的一个 CTA 向该集群内所有 CTA 发出多播加载
3. TMA 多播（隐式）——每个集群内的所有 CTA 对同一数据发出普通 TMA 加载

TMA 多播可以实现高得多的加载带宽来填充 SMEM 缓冲，即使数据尚未在 L2 中。对于已知的流量模式，显式 TMA 多播指令能完美消除 L2 流量，达到理想的「每 SMEM 字节对应 1 / cluster_size 的 L2 字节」。我们还观察到，在这个简单基准中，显式与隐式两种情形的 SMEM 填充吞吐量几乎相同。但 LRC 并不完美；隐式情形下 L2 会多接收一些流量，且总数据量越大越明显。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b833880-e9f9-4018-b7cf-d8f8cc9f95c7_1600x1309.png)
*隐式多播在有效内存吞吐方面与显式多播不相上下。但在降低 L2 缓存流量方面，隐式多播在在途字节数超过 64 字节后便失去效果。*

## DSMEM 与 SMEM

NVIDIA 在 Hopper 架构中引入了分布式共享内存（DSMEM）。DSMEM 允许集群内的 CTA 访问彼此的共享内存。这对跨 CTA 归约（reduction）等模式很有用。通过 DSMEM 读取对等 CTA 内存的吞吐量显著低于 SMEM 的每时钟周期 128 字节。

我们试验了几种与 DSMEM 交互的 PTX 模式。为 DSMEM 而非 SMEM 编写代码时有一个重要区别：DSMEM 加载的数据封包方式与全局加载类似，因此最优访问模式完全不像本地 SMEM 中那种避免 bank 冲突的交错访问，而更像是典型的对 GMEM 连续地址的合并（coalesced）访问。此外，我们观察到，要让本地 SMEM 达到完整的 128B/周期，必须使用不带 `::cluster` 的 `ld.shared`。这是我们在写基准测试时踩过的一个坑：当时简单地用 `ld.shared::cluster` 访问本地和远程 SMEM 地址。使用 `ld.shared` 时，编译器会生成 `LDS`，而 `ld.shared::cluster` 生成的是通用 `LD`，后者似乎无法让本地 SMEM 达到峰值吞吐。我们还尝试用 `ld.shared::cluster` 进一步提升吞吐但未能如愿，直到改用 `cp.async.bulk`（PTX）/ `UBLKCP`（SASS）以每条指令搬运更大数据量后，才通过 DSMEM 取得了略高的吞吐量。

下表给出了每种 PTX 模式下我们达到的峰值吞吐量，以每时钟周期字节数（B/clk）表示，以便与已知的 SM 本地 SMEM 最大可达值对齐。

![](https://substack-post-media.s3.amazonaws.com/public/images/d6c7444e-7004-4e9a-ab21-c0d92e2cbbe7_1512x284.png)

# 第五代张量核心 MMA

MMA 指令是执行矩阵乘法的核心运算。从 Hopper 到 Blackwell，MMA 性能越来越依赖形状（shape）。我们在此研究这一现象，扫遍不同形状和数据类型以量化性能差异。

Blackwell 带来了 2SM MMA——一种新类型的 MMA 指令（`.cta_group::2`），由一对 CTA 跨 2 个 SM 协同执行一次 MMA 运算。具体来说，输入矩阵 A 被复制，而矩阵 B 和 D 被分片（shard）到 2 个 SM 上，且这对 CTA 可以访问彼此的共享内存。这使得更大的 MMA 形状成为可能。我们研究了 2SM MMA 呈现弱扩展（weak scaling）、强扩展（strong scaling）还是两者皆有。

我们用以下的配置空间对 MMA 性能进行了基准测试：

![](https://substack-post-media.s3.amazonaws.com/public/images/3b115c81-e5c1-4904-a640-9d239536fbd1_1342x412.png)

## 吞吐量

NVIDIA 针对不同输入数据类型给出了具体的吞吐量性能指标，这里我们展示其在每种（格式 + CTA 组）下的官方声称值，并与最大可达吞吐量对比。我们证明，UMMA 在所有格式和 CTA 组下都能达到接近峰值的吞吐量，即使在协调开销可能成为顾虑的 2SM 版本上也是如此。

![](https://substack-post-media.s3.amazonaws.com/public/images/d489809c-16d0-40d2-a3a5-030760568f0f_1600x800.png)

对于 1SM MMA，在所有 N 尺寸下，较小的 M=64 最高只能达到理论峰值吞吐量的 50%，而较大的 M=128 接近 100%。这证实 M=64 只利用了一半数据通路。对于 2SM MMA，M=128 的吞吐量在 N=64 时从峰值的 90% 起步，在其余所有 N 尺寸下都接近 100%。M128N64 的吞吐量必然受限于另一个硬件单元，比如 TMEM、L2、SMEM 等。与此同时，M=256 在所有配置下都维持接近 100% 的峰值吞吐量，这是因为 M=256 相当于每 SM M=128，能够利用完整数据通路。我们注意到，相同数据类型位宽的不同格式吞吐量完全一致，微缩放数据类型几乎没有开销。

![](https://substack-post-media.s3.amazonaws.com/public/images/17602e21-9606-451d-a8bc-3899ae442688_1600x695.png)

MMA 支持两种不同的 AB 布局：两个输入矩阵都存放在 SMEM（SS），以及矩阵 A 存放在 TMEM、矩阵 B 存放在 SMEM（TS）。我们观察到，对 M=128，ABLayout=TS 可以达到接近峰值的吞吐量，而 ABLayout=SS 在较小的 N 尺寸下表现不佳，到 N=128 才追上来。

![](https://substack-post-media.s3.amazonaws.com/public/images/314106a3-52a8-427e-9fcf-8be00badccc9_1600x617.png)

我们可以证明，这是因为在 SS 模式下，N 低于 128 时指令本身受 SMEM 带宽限制。例如，对 FP16，我们知道硬件每 SM 每周期可完成 8192 MMA FLOPs，而 SMEM 带宽为 128 B/周期（每 SM）。因此对 M=128 N=64 K=16，有：

`A_bytes = 2*M*K = 4096; B_bytes = 2*N*K = 2048;`

`FLOPs = 2*M*N*K = 262144`

`SMEM Cycles = (A_bytes + B_bytes) / (128 B/clk) = 48 cycles`

`Math Cycles = FLOPs / (16384 FLOPs/clk) = 32 cycles`

我们对逐渐增大的 N 计算这一指标，发现从 N=128 的指令开始，才最终变为受算力（Math）限制。

![](https://substack-post-media.s3.amazonaws.com/public/images/3700253d-db8b-462b-bdaa-6b03e9c1578d_1188x562.png)

其他数据类型同理——两个操作数都存放在 SMEM 中的 MMA 指令，在 N 低于 128 时都受 SMEM 限制。

为进一步说明这一点，我们绘制了所有形状 FP8 1SM MMA 的 roofline（屋顶线）。可以清楚看到 N < 256 落在受内存限制的区域，斜率约为每周期 128 字节，即 SMEM 带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/2b6f6282-c294-432c-97fe-6646a3b9bacd_1517x948.png)

2SM MMA 在所有格式和形状下都实现了完美的弱扩展，当使用的计算资源是 1SM MMA 的 2 倍时，加速比达到 2 倍。在 ABLayout=SS 的较小形状中，我们观察到超过 2 倍的加速比，原因同样是 SS 模式下 N 低于 128 时指令受 SMEM 限制，而 2SM 版本把操作数 B 拆分到了两个 SM 上。

![](https://substack-post-media.s3.amazonaws.com/public/images/c143b70f-f950-4e8f-a9de-7ce2d956f605_1600x1020.png)
*SS 模式：N < 128 时因受 SMEM 限制而获得超过 2 倍加速*
![](https://substack-post-media.s3.amazonaws.com/public/images/76693f90-cbc0-428e-a2fd-84e872810fa8_1600x1020.png)
*TS 模式：接近完美的 2 倍加速*

这些实验表明，对给定的 SMEM tile 大小，应当始终使用可用的最大指令形状，以获得最大吞吐量。

## 延迟

我们对单条 MMA 指令的延迟进行了基准测试，并在下方绘制了对比。在所有配置中，延迟从 N=64 到 128 线性增长，N=256 处的尖峰很可能源于 128 到 256 的跳变。对单个 CTA 组的 MMA，1SM MMA 的 M=64 与 M=128 在各 N 尺寸下延迟相近；而在 2SM MMA 中，M=256 的延迟增长略快于 M=128，这与我们的理论估计相符。比较数据类型，1SM 几乎没有差别，但 2SM MMA 出现了明显的分化。

![](https://substack-post-media.s3.amazonaws.com/public/images/6a0575f8-c15a-4688-943c-2331a0a753ce_1600x695.png)

我们注意到一个虽小但一致的延迟排序规律：

> S8 < BF16 = E4M3 = F4 < MXF8 = MXF4

我们认为整数运算能效更高，因此 S8 最快；而缩放因子（scale factor）计算给 MXF8 和 MXF4 带来了轻微开销。

![](https://substack-post-media.s3.amazonaws.com/public/images/4812fa68-0ae7-40d9-920c-2eb1f55b2d51_1600x1020.png)

## 不同在途指令数下的吞吐量

在吞吐量基准测试中，我们将在途指令数设得很高（从 256 到 1024），以摊薄指令发射与提交等待的开销。然而，实际内核通常只有 1 到 4 条在途 MMA 指令。我们测量了在途指令数为 1 到 10 时的吞吐量，并在此讨论吞吐量的变化。

在所有配置中，相同的 N 与在途 MMA 数对应的 Speed-of-Light（SoL，光速占比）大体相似。值得注意的是，只有最大的 N 达到 90% SoL，而最小的 N 只能达到约 70%。对比 1SM 与 2SM MMA，1SM 的 SoL 吞吐量比对应的 2SM 高约 5%。对相同数据格式与 CTA 组的 MMA，较大 N 的吞吐量始终高于较小 N。最后，我们观察到 4 条在途 MMA 时吞吐量的 SoL 百分比上限为 78%-80%。

![](https://substack-post-media.s3.amazonaws.com/public/images/a662dd8a-5747-43e1-8fc4-8e0a73599bcf_1600x635.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/1c7ae14b-4955-43db-a8b2-5673ff661d72_1600x635.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/b1f518e0-ccbe-48de-ace9-1dd5264df6d5_1600x635.png)

下面我们将结合内核编写库 CUTLASS 讨论真实用例。我们还会讨论吞吐量、多播与裸片布局（floorplan）。

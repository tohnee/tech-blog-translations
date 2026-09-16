---
title: "Vera Rubin NVL72 对比 GB200 NVL72？推理 TCO 与架构分析"
title_en: "Vera Rubin NVL72 vs GB200 NVL72? Inference TCO & Architecture Analysis"
subtitle: "Rubin 基于 LUT 的张量核心、Feynman、机柜级设计、每兆瓦性能、每美元性能、软件改进、Rubin 公开软件、PyTorch、vLLM、OpenAI Triton"
date: 2026-07-23
source: https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference
crawled: 2026-09-15
authors: ["Alec Ibarra", "Bryan Shan", "Daniel Nishball", "Zane Fong", "Cam Quilici", "Kimbo Chen", "Jordan Nanos", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Vera Rubin NVL72 对比 GB200 NVL72？推理 TCO 与架构分析

> 原文：[Vera Rubin NVL72 vs GB200 NVL72? Inference TCO & Architecture Analysis](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Rubin 基于 LUT 的张量核心、Feynman、机柜级设计、每兆瓦性能、每美元性能、软件改进、Rubin 公开软件、PyTorch、vLLM、OpenAI Triton**

[Vera Rubin NVL72 是 NVIDIA 机柜级 Oberon 架构的第二代产品，其在推理上的收益来自极致协同设计（co-design）。](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)工程样片的早期结果令人鼓舞。目前，运行 DeepSeek R1 的 Vera Rubin NVL72 相比 GB200 NVL72 实现了每 MW 5.4 倍的性能和每美元 5 倍的性能，而与 GB200 NVL72 在 2025 年早期部署调通（bringup）时期的表现相比，差距还要更大。Vera Rubin 现在仍处于早期部署调通阶段，因此我们预计差距还会继续扩大。随着软件成熟，Rubin 的推理性能将持续提升——这正是我们在 [InferenceX 基准测试](https://github.com/SemiAnalysisAI/InferenceX)中为 Blackwell 展示过的模式，而且 Rubin 前面还有很长的提升跑道。

[NVIDIA 最近还随 CUDA13.4 发布了首个公开版本的 Rubin（SM_107）软件栈](https://docs.nvidia.com/cuda/developer-preview/13.4/cuda-toolkit-release-notes/index.html)，并已将 Rubin 相关 PR 上游提交到 PyTorch、vLLM 和 OpenAI Triton 编译器。Blackwell 无法复用 Hopper 的 WGMMA 内核，而 Rubin 可以复用 Blackwell 的内核，这让软件部署调通过程顺畅得多。要达到光速（speed of light，SOL）性能，工程师仍需调优和重写内核，但对于那些追求上市时间的人来说，Blackwell 内核可以直接复用。我们还将解释 Rubin 全新的 3 bit 可编程 LUT 张量核心。

NVIDIA 还在 GitHub 上披露了 Feynman 是 SM_140。[与 Blackwell 到 Rubin 的过渡不同，Rubin 到 Feynman 在内核层面的过渡将复杂得多。](https://semianalysis.com/accelerator-hbm-model/)

在 VR NVL72 上采集的早期指标来自 CoreWeave。我们尚未独立验证这些数据。NVIDIA 已承诺在 2026 年第三季度（Q3 CY2026）之前向 InferenceX 提交可验证的数字。Google 应该会在未来几个月内提交 TPUv7 的结果，AMD 也已承诺提交 MI455X UALoE72 的结果。一旦这些结果落地，整个生态系统就能获得跨系统的客观比较。

在这篇文章中，我们将把 NVIDIA 关于 Rubin 的宣称与多个基线逐一拆解对比，展示 Rubin 在哪些方面明显领先 Blackwell、哪些方面领先优势较薄。我们还将运用我们已有的 Rubin 总拥有成本（TCO）估算，来分析 Rubin 的单位总拥有成本性能。Rubin 及许多其他系统的 TCO 来自我们的 [AI TCO 模型，该模型跟踪不同 AI 芯片的总拥有成本，将资本开支（capex）、运营开支（opex）以及其他各类开支纳入考量。](https://semianalysis.com/ai-cloud-tco-model/) 我们还使用[来自我们数据中心模型的「全包公用事业供电估算」（All-in Utility Provisioned Power Estimates）](https://semianalysis.com/datacenter-industry-model/)来考量每瓦性能。

最后，我们将呈现 [VR NVL72 物料清单（BoM）的逐组件构建拆解，这将包含在我们即将推出的 SemiAnalysis 物料清单（BoM）模型中。](https://semianalysis.com/vr-nvl72-model/)

Rubin Oberon NVL72 将比 Blackwell Oberon NVL72 更胜一筹的另一个领域，是快得多的量产爬坡期。这要归功于 Rubin 更简单的无电缆计算托盘设计，以及 NVIDIA 从部署机柜级铜背板中汲取的经验教训——NVIDIA 曾投入大量精力解决 Blackwell 铜背板的各种问题。[我们的加速器模型按季度跟踪 Rubin 在封装层面和机柜层面的出货量。](https://semianalysis.com/accelerator-hbm-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/42660b70-c898-4e6b-a117-7490baf5ae4c_733x1702.png)
*来源：SemiAnalysis VR NVL72 BoM 模型*

# Rubin 芯片级微架构特性简要拆解

对 Rubin 微架构做一次完整拆解，得等到我们获得 Rubin 系统的 ssh 访问权限之后，届时我们可以运行[类似我们首次分析 Blackwell 时所做的那类基准测试](https://newsletter.semianalysis.com/p/dissecting-nvidia-blackwell-tensor)。不过，仍有几个有意思的点现在就可以谈。

我们预计，与从 Hopper 到 Blackwell 的过渡（工程师当时仅仅是为了把内核移植到 Blackwell 就耗费了大量精力）相比，Rubin 的部署调通将顺畅得多。这种简单性源于 Rubin 能够运行 Blackwell SM100 系列内核，覆盖 DeepGEMM、FlashMLA、CUTLASS 等所有重要内核库。从 Hopper 迁移到 Blackwell 意味着从头重写内核——Hopper 的内核根本无法在 Blackwell 上运行。

复用 Blackwell SM100 内核意味着明确的上市时间优势，但要达到光速（SOL）性能，工程师仍需专门针对 Rubin 架构调优和重写内核，不过内核复用为他们赢得了时间，可以更专注于内核调优。

再看架构细节：Rubin 的 SMEM 增加到了 328 KiB，而 Blackwell 为 228 KiB。虽然默认 SMEM 容量是 228 KiB，[但 Rubin 提供了超大共享内存模式](https://github.com/triton-lang/triton/blob/24fcd59d53e42c7fe7b696c235d12ce039af1015/third_party/nvidia/backend/driver.c#L984-L993)，允许提升到 328 KiB。此外，TMEM 从 Blackwell 的 228 KiB 增加到 256 KiB，因为列数从 512 增加到 576。新增的列可以用来存放块缩放因子（block scale factor），同时让累加器所在的 TMEM 区域与之保持分离。[这大大简化了块缩放内核的逻辑](https://x.com/ReubenConducts/status/2078514481261400109)：内核开发者不必再精心地以流水线方式安排并重叠 MMA 矩阵加载与块缩放因子加载。

![](https://substack-post-media.s3.amazonaws.com/public/images/729583a2-4a7d-482b-b86d-bc0f4b46165b_1446x400.png)
*来源：OpenAI*

Rubin 的 TMA 现在支持内联描述符更新（inline descriptor update）。这有大量用武之地。例如，在 MoE 层中，每个专家都是位于 HBM 中各自地址上的独立权重矩阵，因此每次切换专家时，TMA 描述符都必须指向新的位置。在 Blackwell 上，这意味着要在内存中重写描述符，并在下一次加载前做同步。而现在在 Rubin 上，每个专家的偏移量以内联方式传给 TMA 指令，这样一个描述符就能覆盖所有专家，中间无需内存重写。这消除了 token 分发过程中的开销，并提升了低批量下的解码速度。

![](https://substack-post-media.s3.amazonaws.com/public/images/10d63dbe-3c0a-4ab1-af16-311df88dc55e_2388x852.png)
*来源：Nvidia*

内联 TMA 描述符更新对应的是 [ISA 特性](https://docs.nvidia.com/cuda/developer-preview/13.4/parallel-thread-execution/index.html#data-movement-and-conversion-instructions-overriding-tensor-property-value) `.override` [限定符](https://docs.nvidia.com/cuda/developer-preview/13.4/parallel-thread-execution/index.html#data-movement-and-conversion-instructions-overriding-tensor-property-value)。TMA 指令需要一个指定布局和格式元数据的 `tensorMap` 对象。通过使用 `.override` 限定符，批量异步拷贝指令可以把 `tensorMap` 对象当模板复用，仅替换其中的某些元数据字段，例如步长（stride）。就 MoE 而言，各专家的权重具有相同的形状、数据类型和属性。通过覆盖全局地址，内核开发者在加载不同专家时可以避免复制或替换 `tensorMap` 对象。

Rubin 再次将每 SM 每时钟周期的 BF16/FP16 指数吞吐量翻倍，这有助于在注意力计算中让张量核心的工作与 softmax 重叠。FP32 吞吐量与 Blackwell Ultra 相比没有变化。

![](https://substack-post-media.s3.amazonaws.com/public/images/374c0103-f8ca-484c-88a3-7669ff9f63cb_1674x1314.png)
*来源：Nvidia*

Blackwell 的 NVFP4/MXFP4 张量核心只能接受 UE4M3/UE8M0 块缩放因子格式，相比之下，Rubin 的张量核心现在还能接受 UE5M3 的 8 bit 块缩放因子。这种额外的块缩放格式带来更大的灵活性，并且由于其数值范围更宽，在某些情况下量化误差更小。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e1122cc-b6a4-4d16-868f-5eb30f436322_1476x602.png)
*来源：NVIDIA PTX*

同样值得注意的是，借助计数写（counted write），SM 驱动的 NVLink 通信延迟得到了改善，减少了通过铜背板在 GPU 之间传输数据所需的往返消息数量。这一点意义重大，因为 Blackwell 的 NVLink 延迟是 TPU 和 Trainium 的数倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/75f99ec0-fa42-4e36-8f05-a83b0043cfc6_1926x936.png)
*来源：Nvidia*

与 Blackwell 相比，Rubin 张量核心的 FP8 和 FP4 吞吐量翻倍。推动这一变化的关键改动是 k 维度翻倍，这意味着理论上一个 GEMM 执行所需的时钟周期数减半。此外，Blackwell Ultra 上那套别扭的 K=96/3xFP4 指令仍然保留，但同时新增了 K=128 变体。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc9e28e3-954f-48e2-bad3-b44f85adda32_1830x1070.png)
*来源：Nvidia*

在 Blackwell 上，PDL 允许在网格（grid）级别重叠，即依赖网格需要等待上一个内核的所有线程块完成之后才能启动。这实现了某种程度的重叠，可以隐藏内核之间爬降（ramp-down）和爬升（ramp-up）的时间，但与当下流行的超大内核（megakernel）作者们追求的极细粒度重叠相去甚远。在 Rubin 上，实现了更细粒度的重叠：依赖内核可以在线程块级别与前一个内核同步。

![](https://substack-post-media.s3.amazonaws.com/public/images/4479f441-71ca-4062-afcb-8afdbb51c1ff_1992x1176.png)
*来源：Nvidia*

通过采用 3D 堆叠 HBM4 内存，Rubin 的全局内存带宽比 Blackwell Ultra 高 2.8 倍。Rubin 在内存系统延迟方面不太可能比 Blackwell 有任何改进。[我们的加速器与 HBM 模型对 Rubin 所用的内存容量估算及供应商做了完整拆解。](https://semianalysis.com/accelerator-hbm-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/e7b56e2c-d3ba-4a41-944b-cf10be152b97_1726x1258.png)
*来源：Nvidia*

Rubin 为激活值新增了 2:4 稀疏支持。每四个值为一组，保留两个、置零两个。该模式是规则的，因此张量核心知道幸存值在哪里，跳过其余部分，并以两倍速率运行 MMA。一个小的元数据字段记录哪些槽位被保留。

NVIDIA 早在 Ampere 时代就在权重上发布了 2:4，但无人使用，因为那意味着要对模型做剪枝并重新训练。Rubin 把它应用在运行时的激活值上，因此无需重新训练。在注意力中，QK^T 密集运行，随后得分在离开张量内存（Tensor Memory）时被压缩。softmax 只处理幸存值，接下来对 V 的 GEMM 以稀疏方式运行。输出保持密集，因此模型中的其他部分都不需要改变。它同样适用于 MLP 激活值。

NVIDIA 尚未公布任何精度数据，而且在 softmax 之前扔掉一半注意力得分显然未必是免费的。CoreWeave 的 DeepSeek R1 结果似乎也没有用到它，这使它成为又一个「硅片已就位、但背后尚无调优内核」的 Rubin 特性。

![](https://substack-post-media.s3.amazonaws.com/public/images/d15caa76-8148-4a55-ac11-7e82c0e86db4_1720x1436.png)
*来源：Nvidia*

## Rubin SM107 张量核心中的查找表权重解压

Rubin 新增了 LUT B，这是一种从查找表解压权重操作数的张量核心 MMA 模式。在该模式下，B 操作数是一个由索引构成的压缩矩阵。在标准推理 GEMM 中，B 操作数承载权重。权重值存放在张量内存的查找表中。张量核心读取每个索引，并在 MMA 内部重建权重值。没有单独的反量化步骤。查表之后，乘法以 FP8 运行。

在 LUT B 中，每个权重位置存储的是一个 3 bit 索引，而非完整的数值。该索引从该权重所属 8×64 块共享的查找表中选择 8 个 E4M3 值之一。例如，如果存储的索引是 5，张量核心就使用该块查找表中的第 5 号条目作为权重。查表发生在 MMA 内部，因此内核完全不必构建单独的解压权重矩阵。

![](https://substack-post-media.s3.amazonaws.com/public/images/a47edc6f-b509-4b65-aa1c-c5f73044ec3d_2192x1282.png)
*来源：图 280，Nvidia*

查找表（LUT）不必遵循传统均匀网格或浮点网格的间距。因此，量化算法可以把更多的值放在权重密集簇附近，对长尾采用不均匀间距，或者在正负权重分布不同时选用非对称码本。

这种灵活性带来了「每个存储 bit 更高精度」的可能。Rubin LUT B 的单个码字数量比 FP4 少，但它可以把这些码字放在特定权重组需要的位置，而不必接受 E2M1 的固定比例。不过，它并不自动比 MXFP4 或 NVFP4 更精确。一个码本由 512 个权重共享，而 NVFP4 在小得多的 16 个一组的分组上自适应调整缩放。最终结果将取决于码本拟合算法、校准数据、量化感知训练，以及敏感层是否保持在更高精度。

每个索引 3 bit，查找表有 8 个条目。每个条目一个字节，在参考内核中是一个 E4M3 8 bit 浮点数。算下来每个权重 3.125 bit：3 bit 索引，加上分摊到 512 个权重上的 64 bit 码本。码本与索引一起存放在 HBM 中，因此每权重 3.125 bit 就是全部的存储占用。

该指令将压缩权重加载到收集缓冲区（collector buffer）。张量核心可以把它们保存在那里，并在一连串激活值分块之间复用。这是一种权重驻留（weight stationary）模式。该模式也有限制：不支持 B 矩阵转置。

块缩放格式 NVFP4 和 MXFP 同样在 MMA 内部解压。但它们对每个块施加同一个均匀缩放，而不是码本。AWQ 等软件方法通过在矩阵乘法之前运行单独的反量化步骤来压低 bit 数，而 Rubin 是首个在 MMA 内部重建非均匀码本的 NVIDIA 张量核心输入格式。

![](https://substack-post-media.s3.amazonaws.com/public/images/f60b0243-309e-4ed7-a03d-0977dc045cb9_2856x782.png)
*来源：SemiAnalysis*

更低的 bit 率削减了权重所需的 HBM 容量，也削减了 GPU 为每个权重读取的字节数。在低批量下，权重带宽限制解码步骤，每权重字节更少就会提升解码吞吐量。在相同 bit 数下，非均匀码本也比均匀舍入更好地保住精度。这一特性还应能改善能效，因为每个 flop 需要在内存系统中搬运的 bit 更少了。

以 Kimi K3 2.8T 为例，在每权重约 4.5 bit 的水平下，MXFP4 存储 2.8e12 x 4.25 / 8 = 约 1,4875 GB（GB = 1e9 字节）。按每权重 3.125 bit 计，Rubin 查找表格式存储 2.8e12 x 3.125 / 8 = 约 1,094 GB（约 1.09 TB）。差额约 393.5 GB。这些数字仅覆盖原始权重负载，不包括 KV 缓存、激活值以及任何并行复制。按每个 Rubin 封装 288 GB HBM4 计算，仅权重大约就需要 6 个封装（NVFP4）和大约 4 个封装（新的 Rubin 格式）。

# Feynman 架构前瞻

从 Blackwell（SM100）/Blackwell Ultra 到 Rubin（SM107），微架构层面的跨越相对较小，因此 Rubin 可以被看作 Blackwell 的增强改良（kicker）架构。相比之下，Feynman（sm_140）是一个全新的架构家族。从 Rubin 到 Feynman 将需要重写大量内核，类似于当年从 Hopper WGMMA 到 Blackwell tcgen05 的情形。[我们的加速器与 HBM 模型提供了 Feynman 逐季度出货量估算的完整拆解。](https://semianalysis.com/accelerator-hbm-model/)

Feynman 的 3D 堆叠将与 AMD 自 CDNA3 的 MI300X 以来一直采用的 3D 堆叠方式类似。

Feynman 架构的新特性之一，是它将包含感知稀疏性的数据搬运操作。这些操作可用于稀疏 GEMM，通过避免无意义的加载、存储和 FMA 来提升性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/0a0880df-bf99-4b05-b28e-a82003b23ea1_1698x782.png)

# CoreWeave VR NVL72 结果中的细微之处

昨天，CoreWeave 发布了其基准测试的 Vera Rubin NVL72 推理结果，以单位功耗（MW）下的性能（token/秒）为单位表述。我们将拆解其数据中的细微之处，并以我们自己的 InferenceX 2026 年 7 月结果为基线，将其结果与 Blackwell 的性能进行比较。

![](https://substack-post-media.s3.amazonaws.com/public/images/36030902-acf3-4508-915b-74430673b5e7_2446x1380.png)
*来源：CoreWeave*

CoreWeave-NVIDIA 图表上第一个值得注意的宣称是：在约 150 tok/s/user 的同等交互性（iso-interactivity）下，VR NVL72 的每兆瓦 token 吞吐量比 GB200 NVL72 高 10 倍。这比今天前沿模型的「快速模式」还要快约 50%。

关于他们的图表，有三点要说明。该基准测试是单轮的，8k 输入、1k 输出。y 轴是每兆瓦的输出 token 吞吐量，而不是总吞吐量。而且他们的功耗数字涵盖了**预填充和解码两类 GPU**，即便只计输出 token。InferenceX 衡量输出吞吐量时只计**解码 GPU 的瓦数**，因此为了做这次比较，我们把自己的数据重新归一化以匹配他们的口径。

必须指出的是，CoreWeave 声称在其 GB200 NVL72 基线和 Rubin NVL72 性能结果上都启用了以下全部推理优化，包括但不限于：

- NVFP4 精度
- 投机解码（使用 MTP）
- 分离式服务（使用 Dynamo）
- 宽域专家并行
- 通过 TensorRT-LLM 实现

![](https://substack-post-media.s3.amazonaws.com/public/images/c31e0b77-8ec9-44c8-b992-a90451548afd_2496x958.png)
*来源：CoreWeave*

上述结果似乎表明，Rubin 一出场就在性能上大幅领先 Blackwell。不过，有几点细微之处值得展开。

首先，细心的读者会注意到，CoreWeave 是拿 Rubin 与**2025 年的 GB200 NVL72 基线**作比较。在某种意义上，用 GB200 NVL72 生命周期早期的性能来比较是公平的，因为 Rubin 的性能预计也会从其自身生命周期的早期阶段大幅提升。我们的分析同样会使用 2025 年 GB200 NVL72 的早期性能结果，但我们也会比较 GB200 NVL72 到 2026 年时的表现，以及当前最值得对比的 GPU：**GB300 NVL72**。我们将把 GB300 NVL72 在 2026 年初的性能与 Rubin 处于可类比的早期生命周期阶段的性能直接对比。

![](https://substack-post-media.s3.amazonaws.com/public/images/88e13e65-6627-4160-96e3-a9eecafd0bbc_1844x400.png)
*来源：CoreWeave*

CoreWeave 性能结果的第二个细微之处在于，他们使用的是 DeepSeek R1 671B——一个如今已不再被广泛使用的模型。人们或许会希望 CoreWeave 使用更现代的模型，比如 GLM5.2、Kimi K2.5、Qwen3.5 或 DeepSeek V4。更好的选择是 Kimi K3 或 Qwen3.8，这两者都[即将登陆 InferenceX](https://inferencemax.ai/)！至少 CoreWeave 没有[像 AMD 在 2026 年夏天为 MI455X UALoE72](https://github.com/ROCm/aiter/pull/3676) 性能指标所做的那样使用 GPTOSS 120B。我们预计，一旦 NVIDIA 开始在 2026 年第三季度用 InferenceX 在更现代的模型架构上对 Rubin 进行基准测试，这种用旧模型跑分制造的战争迷雾就会被驱散。

说来也怪，CoreWeave 选择 DeepSeek R1 671B 在理论上其实对 Blackwell 基线更有利，而不是对 Rubin。Rubin 的主要优势在于更大的 HBM 容量、更大的 CPU DRAM 容量和更高的 HBM 带宽，这意味着 Rubin 更适合 Fable 5、Gemini Pro、Kimi K3、Qwen3.8 2.4T 这类数万亿参数模型。

第三个值得注意的点是，CoreWeave 只使用了单轮 8k/1k 输入/输出 token。从理论上讲，智能体编程（Agentic Coding）这类多轮长上下文工作负载应该在 Rubin 上表现更好，因为 Rubin 的 HBM 容量和带宽更高，但简单的单轮基准测试无法体现这一点。[我们即将推出的 AgentX 基准场景由我们与 Weka、LMCache、vLLM/SGLang 社区、NVIDIA、AMD 以及社区中许多其他参与者协作创建，将提供真实的智能体工作负载来对推理性能进行基准测试。](https://inferencex.semianalysis.com/datasets/cc-traces-weka-062126) 我们鼓励所有人采用这套推理基准！

最后，我们注意到 CoreWeave 的测试是在一台没有横向扩展（scale-out）网络的预生产机柜上完成的。具体来说，CoreWeave 使用的是戴尔（Dell）工程样机（ES）机柜。我们确实认为这些结果很有价值，因为它们用到了宽域专家并行（EP）和预填充/解码分离（PD disagg），这会用到 NVL72 纵向扩展背板，并证明该背板运行良好。这块背板在 GB200 NVL72 Oberon 爬坡期间曾面临许多可靠性挑战，[正如我们在我们的加速器模型中指出的那样。](https://semianalysis.com/accelerator-hbm-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/42febd6b-f82f-4f19-b85f-522f109aac87_1098x1552.png)
*来源：CoreWeave*

## Rubin 与 Blackwell 的每兆瓦性能对比

NVIDIA 选择主打的指标是「每全包公用事业兆瓦的输出 token 每秒」，统计系统中的每一颗 GPU。为了做同类比较，我们把自己的 InferenceX 基准数据重新归一化到相同的全部 GPU 口径上。下面，我们将 VR NVL72 与我们官方的 GB200 和 GB300 2026 年 7 月基准进行对比，同时也与 CoreWeave 的 2025 年 GB200 基线对比。

NVIDIA 图表中那些抓人眼球的倍数全部来自 2025 年基线。在比较基准数据时，我们认为应该使用同一时期的数字，因此 2026 年 7 月的 GB200 和 GB300 基准才是更有用的比较对象。

理论上，Vera Rubin 的数据中心 PUE 可以更低，[因为 Vera Rubin 可以在定制数据中心里以 45 摄氏度的冷却液温度无冷水机组运行](https://blogs.nvidia.com/blog/liquid-cooling-ai-factories/)。不过，在我们的比较中，由于大多数数据中心的设计需要兼容种类繁多的系统，我们对这些冷板式液冷（DLC）芯片采用相同的 PUE。

下面的帕累托曲线绘制了每全部 GPU 兆瓦的输出吞吐量与交互性的关系。每条曲线都在其方案（recipe）前沿的尽头处停止。

![](https://substack-post-media.s3.amazonaws.com/public/images/3ee917ba-0028-459d-a335-ce66c295df01_2048x1293.png)
*来源：SemiAnalysis*

接下来，我们以表格形式提供同样的数据。当某个单元格写着「不可能」时，意思是该交互性已超出该方案的前沿，即该配置根本无法以那种速度服务该工作负载。

![](https://substack-post-media.s3.amazonaws.com/public/images/5a17747e-8857-443b-a4ab-218b517f1fdf_2048x593.png)
*来源：SemiAnalysis*

下面把同一前沿绘制成柱状图，覆盖 100 到 300 tok/s/user 区间。全部四种方案都有到 250 tok/s/user 的数据，只有 Rubin 和 GB300 能达到 300 tok/s/user。

![](https://substack-post-media.s3.amazonaws.com/public/images/a06afa4a-0f30-436d-959f-bcebe37606b4_2048x691.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/e07c6e89-f1a9-4b63-9ae2-dc951c74f6bf_1536x52.png)
*来源：SemiAnalysis*

先比较 Rubin 与 2026 年 7 月的 GB300 NVL72 基线。Rubin 的领先在低交互性处最小，并沿交互性曲线中部持续扩大。在 100 tok/s/user 以内，Rubin 的吞吐量接近 Blackwell 的 2 倍，随后在约 200 tok/s/user 处扩大到约 4 倍——差距在此达到峰值。之后，差距再度开始收窄。在 300 tok/s/user 处相对 GB300 的 5.4 倍性能头条数字，并不是 Rubin 进一步拉开了身位，而是 GB300 运行在其前沿上最后一个勉强可行的点上，导致比值被吹大。GB200 根本达不到 300 tok/s/user。在高交互性下，随着批量缩小，Blackwell 的每 GPU 吞吐量急剧下降，而 Rubin 仍处于其前沿较平缓的区段。

拿 Rubin 与 2025 年的 GB200 NVL72 基线比较则不一样，领先幅度在曲线中部最大。差距从低速下的不到 3 倍起步，在 150 tok/s/user 处增加到约 10 倍（正是 NVIDIA 在其图表中突出的那个点），随后在约 200 tok/s/user 处回落到 6 倍。那条线的数据是准确的，但正如我们已经提到的，它使用的是一年前的软件栈，不是你今天会实际运行的 GB200。

在交互性区间的最顶端，Blackwell 曲线掉头向下。到 350 tok/s/user 时，GB200 和 GB300 都完全无法服务这些工作负载，只剩 Rubin 还有一条真实存在的曲线，在 300 tok/s/user 交付 96,446 tok/s/MW，在 350 tok/s/user 交付 70,703。

显然，Rubin 将给我们带来比 Blackwell 多得多的「快速模式」。

## Rubin 与 Blackwell 的每 TCO 性能对比

每兆瓦性能只衡量性能与功耗之比。每百万输出 token 成本则把硬件的总拥有成本（TCO）折算进来，包括 IT 资本成本以及电力和数据中心成本。[我们的 TCO 模型对此做了全面拆解，提供跨服务器世代的资本成本和运营成本。](https://semianalysis.com/ai-cloud-tco-model/) 在这里，我们将每个 SKU 的全包 TCO 除以同样的重新归一化输出吞吐量，所以数值越低越好。Rubin 的每 GPU TCO 高于 Blackwell：在运营方自持（而非租赁价格）场景下为每 GPU 小时 3.57 美元，而 GB200 为 1.84 美元、GB300 为 2.36 美元。下面的图表将展示，Rubin 的每 token 美元领先幅度会比其每兆瓦领先幅度略小一些。

![](https://substack-post-media.s3.amazonaws.com/public/images/534cda1f-3982-4dd4-91bc-80abe38ed429_2048x331.png)
*来源：TCO 模型*

与每 MW 分析一样，2025 年 GB200 基线给 Rubin 带来最大的性能增幅，但对于今天购买算力的人来说，2026 年 7 月的 GB200 和 GB300 数字才是更相关的比较基线。

下面的帕累托曲线绘制了每百万输出 token 成本与交互性的关系。每条曲线都在其方案前沿的尽头处停止。

![](https://substack-post-media.s3.amazonaws.com/public/images/70c45703-725b-4176-aaef-86a34ca5e60d_2048x1293.png)
*来源：SemiAnalysis*

接下来是表格形式的同样数据，比值表示 Rubin 在每个交互性下便宜多少倍。同样，标记为「不可能」的单元格表示该方案的前沿无法达到的速度。

![](https://substack-post-media.s3.amazonaws.com/public/images/53bc9b0e-537e-40c6-9c26-f009011fc6af_2048x583.png)
*来源：SemiAnalysis，TCO 模型*

下面的图表把前沿绘制成 100 到 300 tok/s/user 区间的柱状图。全部四种方案都有到 250 tok/s/user 的数据，只有 Rubin 和 GB300 达到 300 tok/s/user。

![](https://substack-post-media.s3.amazonaws.com/public/images/20a9279d-57af-43bb-a36b-3f850e18f43b_2048x651.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/d1c63d4b-cf07-4f15-a990-e340a68cf9ff_1534x52.png)
*来源：SemiAnalysis*

对比 2026 年 7 月的 GB200 和 GB300，Rubin 在每一个交互性下都更便宜，而且差距随交互性上升而扩大。差距从 100 tok/s/user 以内比 GB200 便宜约 1.5 倍起步，到 200 tok/s/user 直至 250 tok/s/user 改善为 3 倍。在 300 tok/s/user 处对 GB300 的 5 倍优势则与每 MW 视图相同——GB300 在那里只能勉强出 token，而 GB200 在这个交互性水平下根本无法服务。

2025 年 GB200 NVL72 基线再次是更具戏剧性的那条，在曲线中部登顶。Rubin 在低速下便宜 2 倍多一点，在 150 tok/s/user 处达到接近 8 倍的峰值，随后在 200 tok/s/user 处回落到 5 倍。与每 MW 版本同样的评语：2025 年 GB200 基线衡量的是一年前的软件栈，不是你今天会实际运行的 GB200。

在区间最顶端，情况相同。GB200 在 250 tok/s/user 以上没有工作点，GB300 在 300 tok/s/user 以上没有工作点，因此到 350 tok/s/user 时只有 Rubin 还能提供服务，交付成本为每百万输出 token 4.18 美元。

在付费墙之后，我们将继续拆解 Rubin 与目前公开可得的最佳 MI355X 分布式推理性能的对比。我们还将简要分析 Triton 编译器、PyTorch、vLLM 和 Dynamo 软件将如何在 Rubin 上运行。

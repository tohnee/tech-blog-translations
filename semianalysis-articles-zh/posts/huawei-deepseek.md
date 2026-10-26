---
title: "华为与 DeepSeek 的共生关系"
title_en: "The Huawei-DeepSeek Symbiosis"
subtitle: "华为昇腾 950PR 深度解析与微基准测试、DSv4.1 Flash 分析、DeepSeek 对昇腾的支持、AICPU、TileLang 昇腾后端"
date: 2026-10-21
source: https://newsletter.semianalysis.com/p/huawei-deepseek
crawled: 2026-10-26
authors: ["Bryan Shan", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-10-26
---

# 华为与 DeepSeek 的共生关系

> 原文：[The Huawei-DeepSeek Symbiosis](https://newsletter.semianalysis.com/p/huawei-deepseek) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**华为昇腾 950PR 深度解析与微基准测试、DSv4.1 Flash 分析、DeepSeek 对昇腾的支持、AICPU、TileLang 昇腾后端**

就在中国国庆假期前夕，DeepSeek 为 [TileLang](https://github.com/tile-ai/tilelang)、[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM-Ascend)、[DeepEP](https://github.com/deepseek-ai/DeepEP-Ascend)、[TileKernels](https://github.com/deepseek-ai/TileKernels)、[FlashMLA](https://github.com/deepseek-ai/FlashMLA) 与 [DeepSelect](https://github.com/deepseek-ai/DeepSelect) 发布了昇腾（Ascend）支持。

两家公司都无法独自做到这一点。华为虽然拥有盘古（Pangu），却没有一个前沿实验室来证明自己的芯片能够训练或推理模型；DeepSeek 有模型，却买不到所需的算力。双方恰好补上对方所缺：华为提供硬件与原生软件栈；DeepSeek 则带来让这套硬件对自己的模型真正有用的负载与工程能力。9 月 30 日 DeepSeek 各仓库中发布的昇腾支持，正是这场交换的产物——而这场交换正是通过内核编写语言（kernel-authoring language）来完成的。

![](https://substack-post-media.s3.amazonaws.com/public/images/31b1b07c-129f-41be-a954-9806473f0d99_1764x1283.png)
*来源：SemiAnalysis——注意该图示为模拟结果。*

到 2028 年甚至 2027 年，DeepSeek 很可能将主要使用华为的技术栈——尤其是在建设全本土化中国生态的内外部压力之下。正如我们在本文及后续文章中所示，华为生态已经成熟且发展完善：昇腾时代打下了坚实的地基，DeepSeek 的工程师们正在其上继续添砖加瓦。

本文将首先剖析 Ascend 950PR 的架构，并对其算力与内存性能进行基准测试；随后探讨 DeepSeek 的软件发布——从 TileLang 的编译器能力，到面向硬件特性的内核优化与机柜级通信；最后分析 DeepSeek-V4.1-Flash 的执行画像（profile）。

# Ascend 950

我们曾在 [DeepSeek V4 Pro 一文](https://newsletter.semianalysis.com/i/199671399/cann)中深入剖析过 CANN 与 Ascend 950 的架构。自那以后，又披露了一些更有意思的细节。

![](https://substack-post-media.s3.amazonaws.com/public/images/a3363fa3-47b2-4528-bde4-0a86ba907d25_1456x926.png)
*来源：SemiAnalysis*

从芯片层面看，950PR/DT 已经出现了众多变体，核心数、HBM 堆栈层数与缓存容量各不相同。其中一些很可能只是虚拟化/仿真出来的，或者仅供测试之用。原因是：由于硬性缺陷以及功耗、性能上的参数性不达标，只有一部分裸片（die）和 HBM 堆栈能够达到目标规格，因此华为把算力和内存都按档位拆分成多个 SKU，并将较弱的内存与较弱的算力配对，而不像 Nvidia 那样只对算力做分档（binning）。

![](https://substack-post-media.s3.amazonaws.com/public/images/e97ec04e-772a-4f61-9984-c46af4e5720b_2047x917.png)
![](https://substackcdn.com/image/fetch/$s_!ntMN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F670401d3-ae2b-44ce-8bfe-b87f7eebd4bb_2677x533.png)
*来源：SemiAnalysis*

这并非新鲜事：910B 同样有 910B1、910B2、910B3、910B4 等变体。在下面的微基准测试中，我们使用的是一块 Ascend 950PR_9579，配备 28 个 Cube 核心与 128 GiB HBM。

```
root@cb3bb851f93f:/workspace# npu-smi info
+-------------------------------------------------------------------------------------------------+
| npu-smi 25.7.rc1.6                               Version: 25.7.rc1.6                            |
+--------+------------------+---------------+-----------------------------------------------------+
| NPU ID | Name             | Health        | Power(W)    Temp(C)           Hugepages-Usage(page) |
|        |                  | Bus-Id        | NPU Util(%) Memory-Usage(MB)  HBM-Usage(MB)         |
+========+==================+===============+=====================================================+
| 0      | Ascend950PR      | OK            | 203.3       56                0     / 0             |
|        |                  | 0000:12:00.0  | 0           0    / 0          5242  / 131072        |
+========+==================+===============+=====================================================+
+---------------------------+---------------+-----------------------------------------------------+
| NPU ID                    | Process id    | Process name             | Process memory(MB)       |
+===========================+===============+=====================================================+
| No running processes found in NPU 0                                                             |
+===========================+===============+=====================================================+
```

运行指针追踪（pointer chase）测试——每轮发射读取 16 KiB 整数载荷：block 数在 18 以内时，延迟稳定在 134ns 附近；到 56 时升至 182ns；到 64 时则跳升至 391ns。这与 56 个 Vector 核心之外还存在第二波调度的推断相吻合。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a315507-0998-4335-841e-994ed23ddd38_2048x754.png)
*来源：SemiAnalysis*

随后，我们在每一个 Cube 核心和 Vector 核心上分别运行标量指针追踪探针，在一条 128 MiB 的链路上记录各匹配地址处的加载耗时，得到下图。每个单元格的颜色代表两个核心地址画像之间的平均绝对差，由此划分出的两组恰好与解码出的裸片相吻合。

![](https://substack-post-media.s3.amazonaws.com/public/images/ff757e4d-1075-4230-9834-30076b620067_2048x1766.png)
*来源：SemiAnalysis*

更进一步：在一个 Vector 核心跑指针追踪的同时，让另一个核心执行内存流量负载或仅用寄存器的任务；由此产生的额外减速揭示了哪些子系统在共享资源，从而支持 {0,2,4} 与 {1,3,5} 这样的分组。通过混合发射 Cube/Vector 任务，可以识别出每个子系统下属的一个 Cube 与两个 Vector，我们在上述分组内把它们画在一起——图中物理位置仅为示意。

![](https://substack-post-media.s3.amazonaws.com/public/images/21a69dca-aa4a-493a-826c-5a553ab5b23c_2048x1156.png)
*来源：SemiAnalysis*

## NPU 之内的 CPU

每颗 950PR 都带有数量不定的 Linx816 AArch64 ELF AICPU。MIDR 编号表明，这些核心很可能与麒麟（Kirin）9000S/9010 中的中核相同。这些 AICPU 核心的指令集为：

```
fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid
asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve
asimdfhm dit uscat ilrcpc flagm ssbs sb paca pacg dcpodp flagm2
frint svei8mm svebf16 i8mm bf16 dgh rng ecv
```

在这个 SKU 上，配置了 7 个 AICPU 核心、可见 6 个、实际执行 5 个。除了设备控制之外，它还能提供 CPU 算子（operator）支持，例如 KV 元数据。对于那些 D2H（设备到主机）开销占大头、耗时很短的任务，AICPU 能派上用场。

对于 DSA，一个小型调度步骤会读取当前序列长度，并把索引器（indexer）工作分配给加速核心。随后 Cube/Vector 核心计算 INT8 索引得分并选出前 2,048 个索引。在 vLLM-Ascend 的实现中，这些规划、索引选择和收集（gather）步骤运行在 AICPU 上，我们将其性能与在主机 CPU 上运行的结果做了对比。

![](https://substack-post-media.s3.amazonaws.com/public/images/f134f741-de67-4f8a-8ee2-e5c8b23f19f6_2048x933.png)
*来源：SemiAnalysis*

由于算力有限，AICPU 只适合开销占主导的短任务，以及数据在 NPU 上产生、也在 NPU 上被消费的任务。

# 微基准测试

Ascend 950PR 面向预填充（prefill）与推荐场景设计，其内存带宽和核心配置都低于更大的兄弟产品 950DT。

下面的结果并非来自 DeepSeek 的贡献，而是昇腾上原生的 `torch.matmul`——它会解析到 `aclnnMatmul_MatMulV3Common_MatMulV3`。我们对比了来自多个开源模型的 1,055 个 BF16 GEMM 形状（shape）。华为最好的内核达到了性能天花板的 99.7%，这说明 DeepSeek 借助 [DeepGEMM 实现的 99%+](https://github.com/deepseek-ai/DeepGEMM-ascend#dense-gemm) 并非最大化利用率的唯一途径。华为工程师同样干得漂亮。

![](https://substack-post-media.s3.amazonaws.com/public/images/da5c0a0e-1d96-4cfa-82a1-4abc4e516e56_2048x729.png)
*来源：SemiAnalysis*

这一优势集中在计算受限（compute-bound）的工作上。在昇腾山脊点（ridge）以下的形状上，其 achieved/attainable 比例中位数为 41.5%，H100 为 46.8%。Nvidia 的部分结果受功耗限制，未能达到最高 SM 频率：功耗中位数约为 690-698 W（上限 700 W），采样到的 SM 频率中位数为 1335-1470 MHz，低于 1830 MHz 的最大值。华为则约为 599-600 W、1500-1550 MHz，对标称参考值 1650 MHz。

昇腾的 MXU 设计可能部分造就了这种高利用率：昇腾把矩阵操作数暂存于专用 L0A/L0B 缓冲、累加器放在 L0C 中，数据搬运、计算与结果处理可以相互重叠。华为将扩大的 L0C 与更灵活的分块（tiling）和复用联系起来。

但当然，950PR 在绝对数值上仍落后，大致介于 A100 与 MI300X 之间。

![](https://substack-post-media.s3.amazonaws.com/public/images/00c575fd-460d-478f-b8ca-13edcaa27da6_2048x729.png)
*来源：SemiAnalysis*

## 内存带宽（MemBW）

测量 HBM 内存带宽时可以看到：在每缓冲区小消息尺寸下，950PR 的有效带宽与带宽利用率均超过 H100；在大消息尺寸下，其带宽利用率也几乎追平 H100。

![](https://substack-post-media.s3.amazonaws.com/public/images/ee1944c9-44f6-4d56-8a57-cf906335c952_2048x759.png)
*来源：SemiAnalysis*

曲线上出现的下凹，源于[昇腾切换了拷贝方式](https://gitcode.com/cann/ops-math/blob/master/conversion/tensor_move/op_api/tensor_move.cpp#L81)——改用启动开销更大的 Vector 核心 TensorMove 内核，于是稍大一点的拷贝反而耗时更长。当拷贝规模非常大时，这笔额外开销相对变小，带宽随之回升。

需要注意，高 FLOPs 利用率与带宽利用率并不必然转化为高 MFU/MBU。训练——尤其是使用 FSDP 时——需要集合通信（collective）、checkpointing 与数据搬运，而这些往往难以与计算重叠。

正如我们在 Jalepeno 一文中所说，基准测试中的「一颗芯片」不过是一种社会建构——多颗裸片也可以被黏合（glue）成一颗更大的「芯片」。因此每瓦性能或总拥有成本（TCO）才是最好的比较基准。不过在中国，电力要便宜得多。我们将在后续文章中分析昇腾的单位 TCO 性能。

硬件抬高天花板，软件则让你够到天花板。尽管华为的硬件可能落后约 5 年以上（对比 A100），其软件却正站在最前沿。

# DeepSeek 开源

在获得昇腾支持的 6 个仓库（[TileLang](https://github.com/tile-ai/tilelang)、[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM-Ascend)、[DeepEP](https://github.com/deepseek-ai/DeepEP-Ascend)、[TileKernels](https://github.com/deepseek-ai/TileKernels)、[FlashMLA](https://github.com/deepseek-ai/FlashMLA)、[DeepSelect](https://github.com/deepseek-ai/DeepSelect)）中，截至撰稿时只有 TileLang 可用，CANN 9.2.0 也尚未发布。[DeepSeek 要求 CANN 9.2.0](https://github.com/deepseek-ai/DeepGEMM-Ascend#requirements)——该版本在本文撰写之后才发布——且需要 C++20 编译器，而 CANN 9.2.0-beta.2 并不提供。[HDK 计划于 10 月 15 日发布](https://github.com/deepseek-ai/DeepEP-Ascend#recommended-hdk-and-firmware)。这一切发生在 DeepSeek 2025 年的[开源周](https://github.com/deepseek-ai/open-infra-index/tree/main#202502-open-source-week)之后，当时这些仓库中的部分只提供了 Nvidia 支持。

从上述结果看，华为已经能够很好地执行各类算子；而这场共生关系要解决的，是让应用的其余部分及其支撑工作变得更高效、更可复用。

## 工程是双向的

华为的架构已经开始影响 DeepSeek 软件组织数据的方式。早期 FlashMLA 的 KV 缓存布局把量化值与其缩放因子（scaling factor）存放在不同区域。在昇腾上，取回一个 token 需要为它的值和缩放因子分别发起传输。[新实现](https://github.com/deepseek-ai/FlashMLA/blob/main/docs/20260930-ascend-prefill-deep-dive.md#decoding-kv-cache-layout-optimization)将二者放在一起，减少了内存传输引擎（MTE）发出的传输请求数量。

![](https://substack-post-media.s3.amazonaws.com/public/images/7f5a9ed8-ba46-4d20-9158-41641fb98a15_1850x1170.png)
*来源：SemiAnalysis*

## 从快速内核到可复用的内核工程

Ascend 950 后端已合并进 TileLang 主仓库，而不是只存在于华为单独的适配器里。它为昇腾的执行模型添加了原生编译、调度、同步与运行时集成。

TileLang 让编写昇腾内核更容易，但开发者仍需考虑硬件：由他们来选择计算、tile 尺寸以及数据存放位置；编译器则承担了 Cube 核心、Vector 核心与数据搬运之间的大部分协调工作。

深入实现之下、对比它与 CANN 及 Triton-Ascend 的性能：它在某些场景下可以追平甚至击败 CANN，首选实现随尺寸而变。这是一个暖缓存（warm-cache）下的简单朴素基准测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/09daeb23-5133-4316-a95c-afa2205f3165_2048x2032.png)
*来源：SemiAnalysis*

AutoSchedule 利用数据依赖与预估执行时间来规划哪些操作可以重叠。它还会在可用片上内存范围内选择使用多少个缓冲槽（buffer slot），从而让即将到来的数据能在当前 tile 处理期间加载。当默认调度不合适时，开发者也可以引导这些决策。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c33e708-9c7b-4a84-8cae-0eed766fcd77_1758x956.png)
*来源：SemiAnalysis*

在 950PR 上，AutoSchedule 对较小尺寸的帮助尤为明显，单个操作的执行时间最多可缩短 40%。

![](https://substack-post-media.s3.amazonaws.com/public/images/b7751b4a-8006-40e5-80f5-f877ccdd7edd_2048x793.png)
*来源：SemiAnalysis*

编译器还会插入同步，让操作等待其所需的数据，同时移除因其他依赖而变得多余的等待。它也会检查条件分支，因此当某个分支可能永远不会执行时，不会臆断其中的操作已经完成。这减少了程序员必须自行管理的同步工作。

## DeepEP

华为已加入 NVIDIA 的行列，将大规模纵向扩展（scale-up）AI 系统商业化：其昇腾超节点（supernode）把紧耦合的加速器互连跨越多个机柜延伸——从 910 时代的 CloudMatrix384 到 950 的 SuperPod——从而支持 wideEP 横向扩展（scale-out）。在 9 月 30 日的发布中，华为还公布了 950DT 超级节点（superpod）上基于 URMA 的 EP16 dispatch/combine 基准测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/c3b2f555-a8c0-45d8-b45d-fb31b5140b31_2048x767.png)
*来源：华为、DeepSeek、SemiAnalysis*

华为的 dispatch 由三个顺序算子组成（pre/URMA/post），而 GB300 是一次融合调用；其 post 工作包括接收完成确认——我们的测量包含了这一项，但也包含按专家（per-expert）展开的计算，而 GB300 的结果不包含后者。

DeepEP-Ascend 是 DeepEP V2.5 的移植版，Python API 相同，但底层调用 URMA 与 HCCL。2025 年 7 月，华为昇腾团队曾[在 `deepseek-ai` 下提议 DeepEP-Ascend](https://github.com/deepseek-ai/DeepEP/issues/332)[，但被一位 DeepEP 维护者婉拒](https://github.com/deepseek-ai/DeepEP/issues/332)。如今，DeepEP-Ascend 则以 DeepSeek 自己的组织名义发布。

昇腾分离的 Cube 与 Vector 执行路径为通信与计算的重叠创造了机会，但重叠并非没有代价。专家计算同样需要向量处理与数据搬运，而通信会争抢共享内存带宽。因此，能在不拖慢并行计算的前提下隐藏多少通信，存在一个权衡。

![](https://substack-post-media.s3.amazonaws.com/public/images/81ac9084-c2f0-4b72-bebc-3321ae01952c_1962x874.png)
*来源：华为*

这种资源平衡问题并非 DeepSeek 独有。华为的 Kimi K3 配方[明确限制向量单元的使用](https://gitcode.com/cann/cann-recipes-infer/blob/d5859e6f4d5887661266bf22629b1f323c088ad8/docs/models/kimi_k3/kimi_k3_inference_guide.md#%E5%A4%9A%E6%B5%81%E7%BC%96%E6%8E%92%E4%B8%8E-npu-%E4%BA%B2%E5%92%8C%E4%BC%98%E5%8C%96)，以便为并发工作留出余量，并根据需要重叠的内容在专用 CCU 与基于 Vector 的通信之间做出选择。单个操作跑得快并不够：各操作的资源需求还必须彼此契合。

[DeepEP-Ascend 的文档](http://deepep-ascend)指出了 combine 处理与 URMA 通信对 HBM 资源的争抢，并表示华为计划通过固件改进来缓解。这正是协同设计（co-design）的务实形态：模型暴露出瓶颈，实现随之调整，平台的开发优先级则回应剩余的问题。

## 一切早有规划

在 5 月一份未经证实的 DeepSeek 投资人会议纪要中，梁文锋表示：

> 「所以，谈到中美之间的芯片差距，我认为软件生态的差距最终会消失。但在硬件方面，我们面临两个相互独立的劣势：需要四张华为加速卡才能抵得上一张 NVIDIA 卡，而且华为把自己的硬件推向市场也大约落后两年。」

四个月后，生态差距确实收窄了。同一段纪要中还提到了 TileLang，以及帮助华为把生态做对这件事。

# DSv4.1 Flash 优化

DeepSeek-华为共生的另一面，是 DeepSeek 向华为提供权重，支撑 Day-0 优化版本发布，例如 DeepSeek V4 与 V4.1。

昇腾的累加器设计迫使注意力计算采取另一条路径。Cube 的 L0C 缓冲无法就地（in-place）对累加输出重新缩放，而要把重缩放后的输出写回 L0C，又需要代价高昂的单位矩阵乘法。DeepSeek 的做法是[把运行中的输出累加器保存在 Vector UB 中](https://github.com/deepseek-ai/FlashMLA/blob/main/docs/20260930-ascend-prefill-deep-dive.md)，在需要重缩放与累加时才从 L0C 传输部分和。Hopper 把累加器放在寄存器里，Blackwell 则提供了张量内存与寄存器之间的加载与存储，从而避开了这一限制。

![](https://substack-post-media.s3.amazonaws.com/public/images/3741c14f-30e9-4883-950f-4a1e32af842d_2048x664.png)
*来源：SemiAnalysis*

## 执行画像（Profile）

华为还发布了一份 profile：在一套 32 芯片的华为昇腾 950DT 部署上，单个 rank 的 DeepSeek-V4.1-Flash 运行画像，连同其主机线程。今年 6 月，我们分析过一个类似的 profile——DeepSeek V4 Pro 的。

许多组成部分是相似的，例如 AICPU 的使用，以及把部分层拆分到不同 stream 上。

![](https://substack-post-media.s3.amazonaws.com/public/images/780f172c-a874-4a1d-b705-b439d10e1312_2048x759.png)
*来源：SemiAnalysis*

执行顺序为：目标模型的 40 个层、目标 LM head、3 个 DSpark 起草器（drafter）块、草稿 LM head，以及 5 轮采样。主计算运行在 Stream 19 上；起草器的计算运行在 Stream 173 上。DSv4 Pro 轨迹中那些融合了计算与通信的 V2 MC² 内核再次出现——这次是 V3 版本。这就是为什么每步只出现 4 个由 AI CPU 发起的 HCCL 操作，而专家 dispatch 有 43 个：它们是目标与草稿词表头的 `hcom_allGather` 和 `hcom_alltoallv`——先聚合隐藏状态，跑 LM-head GEMM，再交换 logits。

起草器块只运行一次，为草稿位置生成基础 logits。其后的 Markov head 通过采样与嵌入反馈来建模 token 之间的依赖，并不会为每个提议重跑 transformer 块。每一步的结尾从 MoE 与注意力，变成了一串由小型投影和采样操作组成的串行链。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac3e578f-23de-4c3c-88b7-e625782f67ca_2048x831.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/9f8f988c-ff82-4a1f-b1b4-e5d6bba6b3ad_2048x843.png)
*来源：SemiAnalysis*

正如我们在过往文章中所提及并解释的，投机解码（speculative decoding）是一种无损方法：预测草稿 token，并用一次前向过程加以验证，从而摊薄权重加载成本。在上面的解码步骤图中，可以看到 DSpark 的 token 起草比验证步骤快了多少。

![](https://substack-post-media.s3.amazonaws.com/public/images/344fe07e-5770-415f-a19d-20302d364b1f_2048x831.png)
*来源：SemiAnalysis*

DSv4.1 Flash 也是首个使用 Engram 的 DeepSeek 模型——不过在 [Qwen](https://qwen.ai/blog?id=qwen3.8-flash-next) 和[美团 Longcat](https://huggingface.co/meituan-longcat/LongCat-Flash-Lite) 之后。

由于 Engram 以 token ID 作为输入，取数可以异步进行并与第 0 层的计算重叠。这使得把数据卸载（offload）到 DRAM 不会相对 HBM 产生性能损失，但卸载到 PCIe 4.0 SSD 则会使性能劣化。详见我们的 Engram 分析：

![](https://substack-post-media.s3.amazonaws.com/public/images/4941eee2-8e0e-4af5-a669-0c30d969f0a8_2048x688.png)
*来源：SemiAnalysis*

汇总稳态窗口内的内核时长：Stream 19 在窗口内的占用率为 88.8%，但由于其他 stream 与其重叠，它只贡献了设备时间总和的 72.6%。图中中部大片 `MIX_AIV` 与 `AI_VECTOR_CORE` 条带包含 dispatch/combine 以及量化。

昇腾通过 `MIX_AIC`、`MIX_AIV`、`AI_CORE` 与 `AI_VECTOR_CORE` 暴露了分别调度的 Cube 与 Vector 路径。每个事件都带有任务类型，因此时长的归账是一种划分（partition）。混合类型依然涉及超出单一物理单元的工作；这些名称并不能把内核耗时转化为实测的「仅 Cube」或「仅 Vector」利用率。

![](https://substack-post-media.s3.amazonaws.com/public/images/382a08c7-e8fa-4db1-9653-c8982c5ff491_2048x747.png)
*来源：SemiAnalysis*

一个一阶情景：把 Cube 吞吐翻倍而其他设备工作保持不变，每步可获得 1.32 倍的提升。该情景假设实测的 stream 重叠保持恒定、空闲时间不变。这是一个组合情景，而非对新芯片的预测：混合任务类型并不是排他性的利用率测量，带宽、依赖与调度都可能改变结果。

量化融合同样仍是机会：其吸引力在于反复出现的生产者到消费者边界，以及它在承载融合通信的 Vector 桶中所占的巨大份额。

# 生态缺口

但有一个问题：这种合作对 DeepSeek 可能运转得极好，却未必能让 Ascend 对其他所有人同样好用。

对 DeepSeek 来说，构建编译器、维护内核、调试厂商特定行为，会与模型研究和产品开发争夺资源——尽管这只是暂时的。

对其他所有人来说，一旦硬件配置与 DeepSeek 的不一致，就可能出问题。大多数优化都针对超节点，而截至 `vLLM-Ascend_0.26.0rc1`，在 x86 主机上使用 Ascend 仍存在诸多问题：

- x86 主机上不支持 DeepGEMM
- vLLM-Ascend 所依赖的 `memfabric_hybrid` 包含硬编码的 ARM 头文件，导致启动被阻断；vLLM-Ascend 无法开箱即用。
- vLLM-Ascend 在非 ARM CPU 上跳过了 CPU 绑定（CPU-binding）
- 没有 NPU + x86 的 CI，部分配方（recipe）[需要打补丁](https://github.com/hicann/cann-recipes-infer/blob/d5859e6f4d5887661266bf22629b1f323c088ad8/integration/vllm/dsv41-flash-single-npu-moe-offload/README.md)

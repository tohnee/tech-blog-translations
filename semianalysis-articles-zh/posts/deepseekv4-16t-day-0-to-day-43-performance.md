---
title: "DeepSeekV4 1.6T 从 Day 0 到 Day 43 性能随时间的变化——华为、GB300 NVL72、MI355X、B200"
title_en: "DeepSeekV4 1.6T Day 0 to Day 43 Performance Over Time - Huawei, GB300 NVL72, MI355X, B200"
subtitle: "Day 0 推理性能、InferenceX、26 天内 100 倍性能提升、每百万 token 成本、华为 950DT 推理 trace 分析"
date: 2026-06-09
source: https://newsletter.semianalysis.com/p/deepseekv4-16t-day-0-to-day-43-performance
crawled: 2026-09-15
authors: ["Bryan Shan", "Cam Quilici", "Kimbo Chen", "Alec Ibarra", "Dylan Patel", "Daniel Nishball", "Cheang Kang Wen"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# DeepSeekV4 1.6T 从 Day 0 到 Day 43 性能随时间的变化——华为、GB300 NVL72、MI355X、B200

> 原文：[DeepSeekV4 1.6T Day 0 to Day 43 Performance Over Time - Huawei, GB300 NVL72, MI355X, B200](https://newsletter.semianalysis.com/p/deepseekv4-16t-day-0-to-day-43-performance) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Day 0 推理性能、InferenceX、26 天内 100 倍性能提升、每百万 token 成本、华为 950DT 推理 trace 分析**

DeepSeek v4 的发布标志着开源模型社区又向前迈出了一步——毫不意外，它出自一家中国实验室之手。其性能随时间的演进对整个 AI 生态系统至关重要。[开源的 InferenceX 工程团队连熬多个通宵，在 Day 0、Day 1、Day 2 及之后持续测量该模型的性能结果，并将其带给全世界。](https://inferencex.semianalysis.com/)在本文中，我们将重点介绍 DeepSeek v4 的 Day 0 性能，并解释模型发布后随后几周内取得的重大改进。我们还将解释 DeepSeek v4 模型架构的核心组件，并讨论它是如何部分地针对华为昇腾（Ascend）推理进行协同设计的。

在我们这篇博文的第 2 节中，我们对 DeepSeek v4 在 Day 0 的华为昇腾 950DT 上的推理做了全面分析。本文是对昇腾 950DT 上 DeepSeek v4 推理的首个分析，我们拆解了计算<>通信的交错回环，以及华为为优化性能所采用的不同计算流。

InferenceX 的一个关键目标——尤其是在模型 Day 0 发布窗口期间——是使用开源镜像和配方（recipe），在尽可能多的框架上记录每个 SKU 的性能，无论这些镜像和配方的表现如何。这使我们能够跟踪性能随时间的改进，我们认为这最能反映每款芯片真实的、可部署的性能。下方的视频分别展示了 vLLM/SGLang 的非 MTP 配置从 Day 0 以来的迭代改进。[访问 inference.com 也可以查看从 Day 0 起的 MTP 配置](https://inferencemax.ai/)。

这些图表反映了投入到 DeepSeek v4 推理性能调优中的数千小时工程工作量，其中大部分优化已合并进 SGLang/vLLM 的主分支。InferenceX 的北极星目标之一，是突出展示性能随*时间*的迭代改进，而不仅是性能的快照——毕竟就工程而言，一路上学到的东西往往与最终结果同样重要。

在 DeepSeek v4 Pro 发布初期，CUDA 上的 vLLM、CUDA 上的 SGLang 以及 CUDA 上采用分离式预填充（disaggregated prefill）的 vLLM 都开箱即用地运行良好，证明了 vLLM 与 SGLang 开源生态的实力。这些推理引擎对全球 ML 生态如此重要，以至于两个团队都成立了自己的公司——Inferact 和 RadixArk，各自融资数亿美元，以持续为其开源推理引擎的发展提供燃料。

华为昇腾也在其文档中描述并演示了对 DeepSeekV4 的 Day 0 推理性能支持。中国目前主导着开源模型格局——[Kimi K2.6 在编码方面仍然击败了 Jensen（黄仁勋）的 Nemotron Committee Coalition 的 Nemotron 3 Ultra](https://x.com/SemiAnalysis_/status/2062942704296743164)。此外，[NVIDIA 自家的 TensorRT-LLM 在 DeepSeek v4 上表现不佳，我们 SemiAnalysis 不得不去修复他们开源的 mHC 内核启动代码](https://github.com/NVIDIA/TensorRT-LLM/pull/13710)。[感谢 NVIDIA 工程师 rebase 并合并了我们的补丁](https://github.com/NVIDIA/TensorRT-LLM/pull/13771)！

在 DeepSeek v4 发布的头几天，ROCm 的表现同样不佳。话虽如此，在 HaiShaw 的技术领导下，AMD SGLang 工程团队在第一个月里大幅提升了性能——到 Day 26 实现了超过 100 倍的性能提升。我们将在即将发布的全面文章《State of AMD 2026》中详细讨论 AMD 软件进展的好与坏。

所有性能跟踪都记录在我们的开源 GitHub 仓库中。如果你觉得这个仓库有用，欢迎给我们点个 star：<https://github.com/SemiAnalysisAI/InferenceX>。

![](https://substack-post-media.s3.amazonaws.com/public/images/fbe458ae-66a8-466f-b516-afef6ea66151_1242x663.png)
*来源：SemiAnalysis - InferenceX GitHub*

我们的完整 DeepSeekV4 性能看板也可以在[这里](https://inferencex.semianalysis.com/inference?preset=dsv4-launch)查看。

SemiAnalysis 的 InferenceX 推理计划得到了 ML 社区众多成员的支持，包括 OpenAI、Oracle、微软（Microsoft）、Weka、PyTorch Foundation、vLLM、SGLang 和 CoreWeave 等。

![](https://substack-post-media.s3.amazonaws.com/public/images/5972d24a-6a3f-495e-bc67-3589d33b3a0f_2338x694.png)
*来源：SemiAnalysis InferenceX 支持方*

InferenceX 团队衷心感谢 vLLM 社区维护者、Inferact，以及 RadixArk、Meta 和世界各地所有 SGLang 维护者持续进行的工程工作。我们还要特别鸣谢并感谢 NVIDIA 工程师 Kedar Potdar、Ankur Singh、Xin Li、Alec Flowers 以及许多其他 NVIDIA 工程师在本项目 Day 0 阶段提供的支持。我们也要向 AMD 工程团队表示感谢，感谢他们在 Day X 对 ROCm 技术栈上的 DeepSeek v4 Pro 提供的支持。

不巧的是，DeepSeek v4 发布时我们的 GB300 集群正好宕机。幸运的是，[CoreWeave 伸出了援手，为开源社区和维护者们贡献了算力——他们紧急腾出了两台备用的开发用 GB300 NVL72 机柜。](https://x.com/SemiAnalysis_/status/2048082151711641829)我们的 GB300 结果正是得益于他们的支持才得以实现，而且我们正在全天候使用这些设备来推动结果的进一步改进。

![](https://substack-post-media.s3.amazonaws.com/public/images/d1e2a9a7-3c85-455e-b5be-1362c5003fd2_2259x3000.png)
*来源：SemiAnalysis*

如果你想从事底层基准测试、InferenceX 或其他有趣的技术工作，请将简历发送至 [letsgo@semianalysis.com](mailto:letsgo@semianalysis.com)，并附上三条要点来展示你的工程能力。如果有的话，请附上 GitHub 仓库链接、网站或博客，以展示你的项目、工作和知识。

# 第 1 节：DeepSeekV4 Pro Day 0 性能

在本节中，我们将首先讨论 DeepSeek v4 Pro 在 Day 0 的开箱即用性能。我们将引用吞吐量-交互性曲线、不同并行策略如何在吞吐量与交互性之间取舍，以及 MTP 和分离式推理（disaggregated inference）等其他推理优化——这些内容已在 [InferenceX V2 文章](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs)中详细解释。

> 请注意，为了避免一场潜在的“推理第三次世界大战”，也为了防止[再来一轮 vLLM 与 SGLang 的推特骂战/说唱对决](https://x.com/EmbeddedLLM/status/1913854116545307094)，本文中我们不会在同一张图上同时展示同一硬件 SKU 的 vLLM 和 SGLang 结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/1525840f-9ddd-4528-87ae-d7233e6d1eec_485x574.png)
*来源：SemiAnalysis*

下面两张图展示了我们设法记录到的所有 Day 0 配方，其中大多数配方使用原生模型检查点，采用 FP4 MoE + FP8 Attention 的混合量化权重（H200 和 MI355X SKU 除外）。由于 DeepSeekV4 Pro 的原生 FP4+FP8 检查点在 Day 0 无法在 MI355X 上使用，我们只剩下使用全 FP8 非原生检查点这一个选项。

遗憾的是，AMD SGLang 和 AMD vLLM 的分布式推理在 DeepSeekV4 Pro 上仍然无法工作。

再看 [SGLang](https://github.com/sgl-project/sglang/pull/23600) 和 [vLLM](https://github.com/vllm-project/vllm/pull/40760)，两者在模型公开发布的那一刻就在 CUDA 平台上原生支持了 DeepSeek v4 Pro。大多数官方宣传的配方，尤其是针对 B200/B300 等较新 SKU 的配方，开箱即用，没有出现任何重大问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f10f07c-c986-453f-b95b-2924a6817149_2594x1448.png)
*来源：InferenceX*

下图展示了 SGLang 的 Day 0 性能：

![](https://substack-post-media.s3.amazonaws.com/public/images/ce1f48af-a25a-4a86-b371-63238b4d8c8c_2404x1464.png)
*来源：InferenceX*

现在让我们更深入地逐一分析每组 Day 0 结果。

## GB200 NVL72 上的 Day 0 多节点分离式预填充

![](https://substack-post-media.s3.amazonaws.com/public/images/5fed15e6-63a1-4963-bdb6-8052f2c104bf_2512x1424.png)
*来源：InferenceX*

vLLM 和 Nvidia 非常迅速地在 [srt-slurm](https://github.com/NVIDIA/srt-slurm/pull/71) 中交付了他们的 GB200 分布式推理 Dynamo vLLM 配方。分离式推理和宽专家并行（WideEP）是可以显著提升每美元性能的推理优化技术——读者可以在我们的 [InferenceX V2 文章](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs)中了解更多。该配方本身相当简陋：预填充采用 eager 模式，使用 NIXL 进行 KV 缓存传输。我们独立复现了该配方，在使用更低交互性配置的情况下，取得了比 B200 运行高出最多 5 倍的结果。

这是 CUDA 护城河发挥作用的一个绝佳例证：有了 CUDA，最新的开源模型往往在接近 Day 0 时就能获得分布式推理支持。

## Day 3 多 token 预测（MTP）投机解码

![](https://substack-post-media.s3.amazonaws.com/public/images/c5b8d644-e0f0-436a-99ac-ce90f0967c2b_2444x1458.png)
*来源：InferenceX*

针对 DeepSeek v4 的首个 MTP 支持来自 SGLang，于 Day 3 交付。使用 MTP 使较高交互性下的吞吐量获得了大幅提升。关于 MTP 的解释及其如何让受内存限制的小批量解码受益，请参阅我们的 [InferenceX V2 文章](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs)。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## Day 0 ROCm AMD MI355X 的失望

再看 AMD MI355X 上的 ROCm，我们在 Day 0 得到的 DeepSeek v4 结果令人困惑。开源生态系统中的大多数 AMD 用户也深陷困惑之中。MI355X 在 Day 0 只能运行 FP8，在下方总 Day 0 图表中处于左下角的位置。推理虽然在技术上跑通了，但体验完全不可用：每用户每秒仅 1-2 个 token 的交互性水平实在太低，远低于普通用户的阅读速度。

我们使用了由 AMD 的 HaiShaw 等人在一个 [SGLang PR](https://github.com/sgl-project/sglang/pull/23608#issuecomment-4311952977) 中提供的 Day 0 WIP（进行中）配方。这是我们在 Day 0 能找到的唯一可用配方。遗憾的是，其性能令人失望，而且原生 FP4+FP8 检查点无法工作——这很可能是由于 ROCm 生态还不够成熟。不过，正如我们将在本文后面谈到的，HaiShaw 的团队最终不负所望，通过经典的基于第一性原理的工程工作，在 Day 0 到 Day 26 之间将性能提升了超过 100 倍，干得非常出色。

![](https://substack-post-media.s3.amazonaws.com/public/images/fce65810-2ddc-4e79-aa75-a7f8dabb7438_2164x1326.png)
*来源：InferenceX*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## AMD ATOM 推理引擎的失望

ATOM 在交互性方面表现稍好，但在并发数大于 1 时仍然力不从心。在 DeepSeek v4 发布初期，我们使用的 [ATOM #650](https://github.com/ROCm/ATOM/pull/650) 硬编码了 `kv_cache[:1,...]`，这意味着 KV 缓存被固定在单个序列槽位上。由于只有一个可用槽位，第二个并发请求无处存放其 KV 状态。之所以如此，是因为支持批量处理的基础设施当时尚未就绪，所以我们只能以单用户的批量大小运行。

ATOM 还几乎在所有热路径上都以 fallback 方式运行：FP4 MoE 被迫落到 Triton，因为 AITER 的 `fused_moe` 在 GFX950 上坏了；mHC 预投影被补丁切到 Torch，因为 AITER 的内核会崩溃，从而被迫采用 eager 执行。

## NVIDIA TensorRT-LLM 的缺陷与 DeepSeekV4 Pro Day 0 支持的缺失

TensorRT 无法开箱即用地支持 DeepSeek v4，因为 `mhcFusedHcKernel.cu` 中有一个硬编码的 `FHC_HIDDEN = 4096` 常量。问题在于 SHAPE_K、residual/x 的 TMA 描述符以及 MMA 内核模板实例化都与该 hidden size 绑定。此前所有 DeepSeek 模型以及 DeepSeek v4 flash 的 hidden size 都是 4096，所以此前相安无事。但尝试对 DeepSeek v4 Pro 运行推理时，就会触发 `"mhcFusedHcLaunch: hidden_size=7168 not supported (only 4096)"` 的守护（guard）错误。

NVIDIA 工程师也遇到了这个守护错误，但他们没有添加代码来支持 DeepSeek v4 Pro 的 7168 hidden size，而是干脆[移除了这个守护检查](https://github.com/NVIDIA/TensorRT-LLM/commit/b3f45bb608aecca666a451ca5138b81470487f05)。不出任何人所料，错误随之消失了。

由于这个“修复”，在超过一周的时间里，除非设置环境变量 `TRTLLM_MHC_ENABLE_FUSED_HC=0`，否则该内核只会针对 4096 编译，而没有任何机制拒绝 7,168 的调用。在使用默认设置（fused HC 默认开启；B300 = SM10x → MMA 路径）时，原生的 trtllm-serve 部署 DeepSeek v4 Pro 会把 7,168 的张量喂进按 4,096 接线的内核。以这些设置运行推理[不会立即崩溃，但存在隐性后果：引擎最终会损坏 hidden states 并产生无效的生成结果](https://github.com/SemiAnalysisAI/InferenceX/actions/runs/25231354124/job/73987414247)。这一问题在[我们撰写的一个 PR](https://github.com/NVIDIA/TensorRT-LLM/pull/13710)中得到修复；令人意外的是，如此简单的问题花了整整一周才被注意到，而 PR 的批准又花了好几天。

等到我们诊断出问题并把范围缩小到 fused HC 的 hidden size 不匹配时，距离 DeepSeek v4 Pro 发布已经过去 9 天。这一事件是一个很好的案例研究，证明了开放的原生 SGLang 和原生 vLLM 引擎生态的实力。得益于这些健壮的生态，Day 0 支持总是先落到原生 SGLang 和原生 vLLM 上，然后才轮到 TensorRT-LLM 或 AMD 的 ATOM 引擎（顺便说一句，ATOM 目前的生产客户数量为零）。

在下面的图表中可以看到，截至今天，TRT-LLM 在较高批量大小下性能更优，但在较高交互性水平上往往落后。

# 第 1.5 节：性能随时间的变化

如本文前面所述，我们对各推理引擎和配方的 Day 0 性能拍摄了快照，作为衡量性能随时间改进的基线。有了这一基线性能，我们就能够测量并呈现以下分析性能随时间改进的数据。

## MI355X 上的 DeepSeek v4 Pro——不到 1 个月提升 100 倍

Day 0 时，DeepSeek v4 Pro 在 MI355X 上虽然技术上跑通了，但显然无法部署到任何生产工作流中。然而，此后的改进令人惊叹——由 HaiShaw 领导的 AMD 团队在 DeepSeek v4 发布后不到一个月的时间里，实现了超过 100 倍的吞吐量提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ef7031c-d08f-446b-9196-83cd997048dc_2396x1452.png)
*来源：InferenceX*

上图展示了吞吐量帕累托最优前沿的爬升：对比 4 月 25 日发布的 Day 0 FP8 版本结果与 5 月 27 日发布的 FP4 版本结果。性能增益几乎全部来自 AMD 用真正的 AITER、Triton、TileLang 和 FlyDSL 内核替换掉了 PyTorch 原生的 fallback 路径。

有两个步骤带来了绝大部分增益。幅度最大的百分比提升实际上来自基线 Day 0 提交之后的第一个 commit——团队摘掉了大量低垂的果实，使 FP8 基线之上的第一次迭代显著改善。第二大改进出现在几天之后，AMD 团队终于让 FP4 权重 MoE 跑通了，使我们得以将 MoE 专家从 FP8 切换到原生 FP4（MXFP4），提升了专家权重的带宽。这也让 FlashMLA 和稀疏注意力索引器从 torch fallback 迁移到 TileLang 内核，并启用了 HIP graphs。

我们看到的下一个重大改进来自 AITER mHC 内核的引入，它被用于每一层。这一改进使性能大幅提升，让我们首次看到 MI355X 在较低交互性水平上超越 H200 运行 DeepSeek v4 Pro 的性能。

窗口注意力（windowed-attention）内核在运行之前，需要知道每个 query 的窗口覆盖了哪些 KV 缓存槽位。这项工作由 SWA-prepare 完成，其 Triton 实现也为性能提升做出了贡献。

下一次大的跃升出现在 5 月 19 日，团队移除了剩余的 fallback：FlashMLA 从 TileLang 迁移到 Triton，同时 AITER FlyDSL FP4 MoE 内核落地。团队还启用了 fused hash-topk、DSv4 radix attention、fused store-cache、fused WQA/WKV projection 和 fused paged-compress，进一步提升了性能。并发扫描（concurrency sweep）范围也扩大到 1024，勾勒出此前并不存在的前沿曲线的高吞吐量、低交互性一端。

![](https://substack-post-media.s3.amazonaws.com/public/images/0caaf2b4-df76-4c1d-8646-c604d83dd4f8_2306x1424.png)
*ATOM 从左下角的一个点成长为覆盖完整前沿的曲线。H200 作为参照。来源：InferenceX*

ATOM 同样取得了巨大进步，从仅有一个 conc=1 的点扩展到在整个帕累托前沿都能交付不错的吞吐量，其中一些点甚至超过了 H200。第一项增益来自 [AITER 修复 #2916](https://github.com/ROCm/aiter/pull/2916)，它纠正了导致 mHC 崩溃的设备分配 bug，让 ATOM 得以恢复使用那个 AITER 内核。接着，FP4 专家迁移到 AITER 的 fused MoE 内核上（移除了 Triton override），稀疏注意力的 OOM 问题也被清除，从而可以去掉 eager 模式和单序列限制。批量处理支持也已实现，将扫描范围从 conc=1 扩大到 conc 1–512，性能也大幅改善。

### MI355X MTP

到第 4 周，MTP 已在 AMD 的所有框架上正常工作，在同等交互性下带来数倍的吞吐量提升。不过我们注意到一个一致的特性：MTP 在较高吞吐量下往往给出更差的结果。这是因为 MTP 利用的是受内存限制的解码中富余的算力，而对于受算力限制的大批量解码任务，MTP 的开销会超过草稿 token（draft token）所能带来的收益。

## B300

![](https://substack-post-media.s3.amazonaws.com/public/images/c3f1e203-f4a2-4554-a7e6-0709b4ca062a_2420x1478.png)
*来源：InferenceX*

对于 B300 上的 SGLang、DeepGEMM MegaMoE，我们的结果显示，在不到一周内性能提升了 3 倍，这得益于使用了分组式 FP4 MoE GEMM——它让专家常驻并执行一次 mega-dispatch，而不是为每个专家单独起内核——以及通过调优改用 EP4 而非 EP8。

## B200

B200 的表现与 B300 相对接近，其中 TRT 在 B200 上较低交互性区间更占优。但 TRT-LLM 无法开箱即用，而 CUDA vLLM 和 SGLang vLLM 则可以开箱即用。

## GB300 NVL72

![](https://substack-post-media.s3.amazonaws.com/public/images/5653824c-64c7-4af9-b4ec-026fd91f5db3_2578x1424.png)
*来源：InferenceX*

GB300 SGLang MTP 最显著的改进出现在 6 月 2 日，来自 W4A4（MXFP4）MegaMoE 的实现。与 5 月 7 日仍在使用的非 MTP 实现相比，6 月 2 日版本的主要改进完全来自对 GB300 解码拓扑的重写，而非改动内核或精度。Day 0 配方在大多数点上以狭窄的 EP=8 运行，由一两个预填充 worker 供给，并发上限为 16,384；而 5 月 20 日的运行将解码扩展到 EP=16，把每个解码 worker 对应的预填充 worker 扩展到四至十二个，并将并发推到 21,504。

基于上述图表和分析，我们可以看到，正如对更大 world size 推理系统所预期的那样，宽专家并行（Wide EP）是 GB300 出色性能的主要杠杆，其收益来自将权重加载摊销到更多 GPU 上。想了解更多关于 Wide EP 的内容，请阅读 [InferenceX V2](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs) 文章。

这些 GB300 结果只有在 CoreWeave 的支持下才成为可能。

感谢阅读 SemiAnalysis！本文为公开文章，欢迎分享。

[分享](https://newsletter.semianalysis.com/p/deepseekv4-16t-day-0-to-day-43-performance?utm_source=substack&utm_medium=email&utm_content=share&action=share)

# B200 每兆瓦（MW）token 数的改进

对于使用 vLLM 引擎的 B200，在 50 tok/s/user 交互性下，Day 0 时每全包 provisioning 市电兆瓦的 token 吞吐量达到每 MW 每秒 300,000 个 token，到 6 月 5 日已改进至接近每 MW 每秒 500,000 个 token。

![](https://substack-post-media.s3.amazonaws.com/public/images/319ea121-b85e-4114-9684-5ab909e5d33b_2048x1549.png)
*来源：InferenceX*

每全包 provisioning 市电 MW 的 token 数是评估机群级投资回报的最佳衡量指标：它在裸的每 GPU token 吞吐量之外提供了更多信息，因为它反映了 PUE 和数据中心开销。由于 B200 的全包市电功耗包络固定在约 2.17 kW/GPU，从约 300k 到约 500k tok/s/MW 的约 1.7 倍跃升反映的是纯粹的软件增益。

推动吞吐量前沿的同一类优化（MegaMoE 分组 FP4 GEMM、更宽的 EP、FP4 权重路径、调度器调优）可以直接转化为能效提升，因为以 MW 计的全包市电功耗保持不变。

许多组织从最大化稀缺的市电电力资源的角度来规划推理机群。问题在于，在给定的利用率和价格下，如何把已 provisioning 的 MW 转换为尽可能多的可计费 token。这类分析最好借助每 MW 营收、每全包市电 token 数、每 MW 资本开支（capex）等指标。这正是我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)所要解决的业务问题。

# 截至 2026 年 6 月 6 日的当前性能

让我们快速盘点各系统和各推理引擎的最佳性能，为本节关于性能改进的内容收尾。在使用 SGLang 时，GB300 继续碾压所有其他推理系统，展示了 GB300 NVL72 机柜级 world size 的优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c5f988b-3365-4d6e-992b-8a699a5a0982_2048x1117.png)
*来源：InferenceX*

开启 MTP 后，在我们分析的所有交互性水平上，用 GB300 做服务都无可匹敌。假设输入 8k token、输出 1k token，GB300 在 50 tok/s/user 下的每百万输出 token 成本达到 $0.156。关于我们如何计算总拥有成本（TCO），请参阅我们的 [TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)了解更多。

![](https://substack-post-media.s3.amazonaws.com/public/images/87b78bd3-2f68-40d5-9fdf-354d2f16de9b_2612x1682.png)
*来源：InferenceX TCO 计算器*

机柜级优势本质上是一个纵向扩展域（scale-up domain）的故事。NVL72 将 72 个 GPU 置于单一 NVLink 域中，使服务栈能够把专家并行铺得足够宽，让 DeepSeek V4 的 MoE dispatch/combine all-to-all 完全留在 NVLink 上，而不是溢出到更慢的横向扩展网络上，同时把专家权重加载摊销到多得多的 rank 上。

以 8-GPU NVLink 孤岛形式通过 InfiniBand 横向扩展的 B200 和 B300 会更早撞上这堵墙，而 MI355X 在纵向扩展域尺寸和集合通信栈成熟度两方面都更加落后。要把这些单机柜吞吐量优势转化为已部署的服务容量，则是另一个问题，取决于每个 SKU 实际有多少在线：按 SKU 划分的出货量和 ASP，再加上按客户划分的装机量和有效 FLOPS，逐季追踪——这些内容我们在 [Accelerator & HBM 模型](https://semianalysis.com/accelerator-hbm-model/)中跟踪。

## ROCm vLLM DeepSeek v4 Pro 的失望

说到 ROCm，原生 vLLM 的进展比原生 SGLang 慢得多。ROCm vLLM 的性能远远落后于其 CUDA vLLM 对应版本。部分问题在于，AMD 正把重心重新放到 ATOM（一个服务着 0 个生产 token 的推理引擎）上，而不是聚焦于原生 vLLM（一个被其众多大客户使用的推理引擎）。我们将在即将发布的《State of AMD 2026》文章中详细讨论这一点（涵盖 AMD 推理的好、坏与丑陋）。我们将报道的积极进展之一是：开源、开箱即用的上游 AMD vLLM 终于在非 DeepSeekv4 模型上实现了分布式推理的功能可用。走到这一步花了好几个月，AMD vLLM 团队前面还有很多路要走。

![](https://substack-post-media.s3.amazonaws.com/public/images/29b8bd8e-cee3-4d5c-8edb-8a1de8f3054d_2312x1424.png)
*来源：InferenceX*

# DeepSeek v4 的下一步是什么

## vLLM

vLLM 的计划在 [DeepSeek V4 路线图 issue（#40902）](https://github.com/vllm-project/vllm/issues/40902)中跟踪，已落地的代码在实现 PR #40860 中，其中还描述了针对 SemiAnalysis InferenceX 看板的基准测试。FP4 Indexer 和初步的 MegaMoE 支持已经实现，Hopper 现在也已受支持。vLLM 在 DeepSeek v4 上剩余的工作横跨五个领域：

- **核心模型支持**：持续推进 MegaMoE 工作（PR #40833）以及 NVFP4 支持。
- **运行时与并行**：Model Runner V2 集成、MTP 优化、预填充/解码（PD）优化以及流水线并行支持。
- **内核集成**：分页预填充（paged prefill）内核、快速 top-k 内核、更多横向融合、DeepEP V2，以及与 DeepSeek 自家 TileKernels 的集成。
- **KV 缓存**：KV 缓存卸载（offloading），涵盖 PD + CPU 卸载（PR #39654）以及分布式 KV 卸载。
- **硬件支持**：在已完成的 Hopper 支持之外，SM120 和 AMD 支持仍是关键待办事项。

这里的主题聚焦于周边系统：新的 model runner、流水线并行、KV 卸载以及更广的硬件覆盖。

InferenceX 即将推出的更新，以及 SemiAnalysis 开源且公开的 EcosystemX 看板，将可视化所有主要 AI 芯片（NVIDIA、AMD、TPU、Trainium、华为等）上所有主要 ML 开源库的软件演进、CI 覆盖和排队时间。

# SGLang

SGLang 的计划位于[性能优化跟踪器（#23666）](https://github.com/sgl-project/sglang/issues/23666)中，Nvidia 按照 DeepSeek v4 的网络结构图逐个模块地组织了这份清单；其中一些事项可能已由初始支持 PR（#23600）部分覆盖，也欢迎社区贡献。

这里反映了三个高层目标：解码的 CUDA graph 支持、预填充的分段（piecewise）CUDA graph 支持，以及取消运行时权重处理。此外，权重准备应只做一次，而不是每步都做。在这三个高层目标之下，清单按 V4 的组件分组：

- **mHC**：为 `fc_hc_fn` GEMM 尝试 TF32/BF16（其 N 维度较小，可能需要专用内核）、1/RMS + 乘法融合、单内核 `hc_split_sinkhorn` 与 `hc_post`，以及在 attention 和 MoE 模块中融合 MulSum + RMSNorm（+ FP8/MXFP8 量化）。
- **HCA（含 Compressor）**：将 `fc_qa` + `fc_kv` 横向融合为一个 FP8 GEMM、q-norm/k-norm 与 RMSNorm+RoPE 融合、一条省去 `topk_idx` 的非稀疏 MQA 路径、MQA 直接从压缩和 SWA KV 缓存中读取而无需拷贝/拼接、单内核 InvRoPE、融合的 Compressor 状态更新（kv-update + ape-Add + score-update），以及让 HCA（尤其是 Compressor）在解码时兼容 CUDA graph。
- **CSA（Indexer + Compressor）**：稀疏路径采用类似的直接缓存读取、（P1 可选项）fc_compressor + fc_idx_compressor 与 fc_qb + fc_idx_qb 的融合、（RoPE +）Hadamard + MXFP4 量化融合、高效的 MXFP4 BMM+ReLU 内核（可能与 MulSum 甚至 Top-1024 融合），以及 Indexer 和 Compressor 的 CUDA graph 兼容。
- **MoE**：为 router GEMM 尝试 TF32/BF16、将路由路径（softplus + sqrt + bias-add + Top-6 + gather + norm + multiply）折叠进尽可能少的内核、融合逐块 FP8 与 MXFP8 激活量化、确保共享专家和路由专家的 FC13 都是单内核，以及审查路由专家之前的那些小型排序内核。

SGLang 的重心是用单个融合内核替代小算子链、让新的注意力变体原地读取缓存，并把解码路径完整地纳入 CUDA graphs。

# 第 2 节：华为 950DT 的 Day 0 DeepSeek v4 分析

DeepSeek v4 是第一个在华为昇腾上获得一流 Day 0 支持的重磅开源模型，事实上，DeepSeek 官方 API 的一部分自 Day 0 起就一直在华为上提供服务。我们手上有 DeepSeek v4 在华为上的性能数据，并计划发布一篇后续文章，深入进行华为与 H200、B200 上推理的同类项（apples to apples）对比，使用相同的基准测试框架测量对比性能。

我们即将推出的公开开源 SemiAnalysis EcosystemX 看板将可视化所有主要 AI 芯片（包括昇腾技术栈）上所有主要 ML 开源库的软件演进和 CI 覆盖情况。

## CANN

CANN（Compute Architecture for Neural Networks）是华为用于在其自家昇腾芯片上运行 AI 工作负载的软件工具包。自 2025 年 8 月起，他们开源了 CANN，以吸引更多开发者，并一点点蚕食 Nvidia 的主导地位——尤其是在中国境内，因为美国政府严格限制 CUDA 芯片对华出口。

![](https://substack-post-media.s3.amazonaws.com/public/images/07e2734c-4e08-4b68-b70b-6734a0c4b9ee_1742x978.png)
*来源：CANN 幻灯片*

Day 0 当天，CANN 发布了一份针对昇腾芯片的优化指南和基准数据。透过它，我们可以看到华为的 CANN 战略：通过面向中国本土模型发布的全栈推理优化，让昇腾具备竞争力。华为想向中国生态证明：只要 DeepSeek 发布新架构，CANN 就能交付内核、图执行路径、量化、服务集成和部署配方。

在基准测试 MTP 时，我们观察到 CANN 团队有一个忍不住要提的有趣方法论，那就是他们如何处理 MTP 草稿 token 的 AR（接受率）或 AL（接受长度）。对 MTP 做基准测试并非易事，因为基准测试的 AR/AL 可能与用户的实际使用场景不同。例如，基准测试平均可能每 3 个草稿 token 接受 2 个，但由于部署场景千差万别，实际可能平均每 3 个只接受 1.5 个。

这意味着用户看到的性能可能低于基准测试结果，从而错误地得出自己的配置有问题的结论。我们在 [InferenceX v2 文章](https://newsletter.semianalysis.com/i/188090866/multi-token-prediction-mtp)中通过用 MTBench 对比 AR 解决了这个问题。我们基准测试的未来迭代将通过使用真实 trace 来全面弥补这一缺口。

为了应对这一特性，华为改为对齐到最后一个 MTP 模块来计时完整的解码步骤，从而[记录每个解码步骤的耗时而非每个 token 的耗时](https://gitcode.com/cann/cann-recipes-infer/blob/052e0ba122043bf46a2b5d17e16488e53e7b0b60/executor/core/engine/execution_engine.py#L451)。这样发布的最终基准测试结果需要用户乘以其使用场景的 MTP AL 才能得出可比的性能指标，这是一种非常优雅的性能比较方式。

## 嘿，NVIDIA 这位歌利亚——镇上来了新的大卫：昇腾 950

华为给昇腾 950 芯片起的内部代号是“David”（大卫），这个代号在 CANN 代码库中多次出现。毫无疑问，这是因为他们认为自己是 Nvidia 这位歌利亚（Goliath）面前的大卫。

![](https://substack-post-media.s3.amazonaws.com/public/images/d3617da3-8be7-4094-8d78-5c7340fbfe66_976x1532.png)
*来源：SemiAnalysis*

SIMT/SIMD 的 950 芯片有两个版本：950PR 和 950DT。PR 代表 Prefill（预填充）和 Recommendation（推荐），是性价比更好的低成本芯片。DT 代表 Decode（解码）和 Training（训练），该版本具有更高的内存带宽和更高的性能。两者都基于相同的昇腾 950 裸片（die），采用双 die UMA 架构，但各自搭配不同的内存封装。华为路线图上每款华为芯片的估算数据和季度产量可在 [SemiAnalysis Accelerator 模型](https://semianalysis.com/accelerator-hbm-model/)中查看。

![](https://substack-post-media.s3.amazonaws.com/public/images/48a04779-4743-4496-9e8e-59dc10f7595f_2048x1302.png)
*来源：CANN*

芯片架构中有两个值得讨论的重要组件：AIC（AI Cube）和 AIV（AI Vector）。AIC 是昇腾 AI Core 中**矩阵/张量核心**一侧，用于密集矩阵运算：GEMM、matmul、类卷积张量算子、注意力投影、FFN 线性层等。华为文档将 AIC 描述为分立式 AI Core 架构中的**矩阵计算**核心。AIV 则是**向量核心**一侧，负责逐元素/向量类工作：激活函数、各类归一化、掩码、规约（reduction）、类型转换、布局变换、matmul 周边的后处理等。

![](https://substack-post-media.s3.amazonaws.com/public/images/a4ed2c38-3636-4268-ba3a-f27eb63a45b7_1094x686.png)
*来源：CANN*

这与 TPU 的 MXU 类似。不过，昇腾把这两种功能的分立暴露得更直接——做成彼此独立的核，各自可以加载自己的代码段，并且具备“双主（dual-master）模式”：AIC 和 AIV 各自独立运行代码，而不是由 AIV 通过消息驱动 AIC。

AI CPU 是设备侧的 ARM64 执行单元，可直接访问设备内存。它作为 AI Core 的补充，承担那些难以映射到 SIMD/SIMT 核上的工作：重分支的控制流、标量逻辑、动态形状处理，以及内核运行前所需的依赖数值的调度/分块（tiling）元数据。由于 AI CPU 就在设备上，昇腾可以把这类不规则的控制型工作留在本地，而不必在主机 CPU 之间往返——后者是延迟和流水线气泡的主要来源。AI CPU 也是历史上位于旧的 AICore → AICPU → SDMA 通信编排路径上的单元，后来专门的 CCU 接管了这项工作。

与 TPU 和 Trainium 一样，昇腾 950 增加了专用的 CCU 通信引擎。该引擎与计算 die 并列，通过支持远端读 + 规约 + 本地写、本地读 + 远端写，在不消耗 AI Core 算力的情况下处理集合通信工作。其收益在于更低的通信延迟、更少的 HBM 流量、更少的用户缓冲区拷贝，以及把计算核从通信编排中解放出来，避开旧的 AICore -> AICPU -> SDMA 路径。

## 华为 DeepSeekV4 Pro 950DT 性能剖析

![](https://substack-post-media.s3.amazonaws.com/public/images/82802657-aff7-4387-8908-491645be8994_1732x862.png)
*来源：SemiAnalysis，华为*

上图展示了 DeepSeek flash v4 在昇腾 950DT 上的三步性能剖析（profile），采用 16-rank DP/EP 部署配置运行。图中可以看到 16-rank 的集合通信参与，以及活跃的 MoE dispatch/combine 流量。

正如如今大多数技术栈的标准做法，CANN 同样使用可在多条流上运行的独立计算与通信算子——通过控制 Cube 和 Vector 核的分配来避免资源争用，从而提升性能。Prolog、Compressor 和 LightningIndexer 等操作可以重叠执行，C4A Compressor 可以被完全隐藏，共享专家的计算也可以隐藏在路由专家的执行之下，同时不损害路由专家的性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e880870-472a-45c6-8357-d6b923fb1a52_2048x698.png)
*来源：SemiAnalysis，华为*

放大到某一个解码步骤，我们可以看到不同组件如何被拆分到各条流。当设备有空闲且合适的资源时，不同流上的操作可以并发运行。模型之所以使用多条流，是因为一层未必是一条单一的串行链，而可能包含若干分支，这些分支只需在结果合并时同步即可——例如共享专家计算与路由专家计算 100% 重叠。

上图中 145-148 号流对应元数据流。这些算子在每趟解码中触发一次，预计算依赖数值的调度/分块元数据，供后续内核复用。它们是解码步骤中仅有的 AI CPU 算子，只占总时间极小的一部分，并且与 AI Core 计算完全重叠。在更长上下文的基准测试中，其影响可能更大，因为需要预先解析的依赖序列长度和掩码的分块工作更多。

在 DeepSeek v4 中，华为把稀疏注意力和 LightningIndexer 的依赖数值的调度阶段移到了 AI CPU 上，而不是将其弹回主机。这些元数据算子根据运行时的序列长度、掩码和分页 KV（paged-KV）信息构建可复用的逐核分块张量；随后 `SparseAttnSharedkv` 和 `QuantLightningIndexer` 消费这些张量，决定每个 cube 核处理哪些 Batch/Head/Q-block/K-block 工作，以及相应的向量核规约任务。从概念上讲，这类似于 FlashInfer 在主机上为分页注意力所做的规划阶段：一个廉价的、感知动态形状的一次性设置步骤，因而可以在各层间摊销；唯一的区别在于，华为把同样的规划工作推到了设备上的 AI CPU 而不是主机上。

上图中的 152 号流包含 LM head、最后一层以及倒数第二层的 `o_proj` 和 MoE。这是 `npugraph_ex` 图编译器的决定，很可能是为了让 `npugraph_ex` 运行时认为 144 号流上的主图已经“完成”，而尾部工作继续异步执行。

![](https://substack-post-media.s3.amazonaws.com/public/images/c447cc9f-d4d1-4877-9a66-cc82948c5164_1814x630.png)
*来源：SemiAnalysis，华为*

CANN 还在 2024 年推出了 MC²（merged compute-communication，融合计算-通信）。这是一类融合算子，既不是普通内核，也不是 HCCL 集合通信，而是把通信和计算嵌入到同一个内核中。在 DeepSeek v4 解码中，我们可以看到 `MoeDistributeDispatchV2` 和 `MoeDistributeCombineV2` 这两个 MC² EP 算子被使用。

这里的主要结论是：昇腾在 Day 0 就为 DeepSeek v4 交付了可用的、经过优化的推理基础设施。华为 CANN 栈是仅有的两个对 DeepSeekV4 提供 Day 0 支持的技术栈之一，另一个是 Nvidia 的 CUDA。正如本文前面解释的，AMD 的栈不幸在 Day 0 表现不佳。这与去年 DeepSeek v3/R1 发布时形成鲜明对比。那时只有一个栈在 Day 0 正常工作：Nvidia CUDA 栈。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c5539e0-5765-4c9f-bb9d-6040c244fe99_2060x1062.png)
*来源：DeepSeek*

赋予昇腾 950 内部代号的那则圣经故事的结局，是巨人扑倒在地。但故事里的歌利亚是站着不动任由大卫投石的，而 Nvidia 这位歌利亚始终在移动，每年推出新架构并持续改进现有架构。华为已经证明自己能在 Day 0 投出石子；至于能否击倒一个移动中的巨人，仍有待观察。

# DeepSeek V4 架构深度解析与协同设计

![](https://substack-post-media.s3.amazonaws.com/public/images/e1225109-a178-4b90-95d4-a36412410f0a_1384x1478.png)
*来源：DSv4 技术报告*

## 面向 1M 上下文长度的推理优化

DeepSeek v4 采用了压缩稀疏注意力（Compressed Sparse Attention，CSA）和重度压缩注意力（Heavily Compressed Attention，HCA），告别了多头潜在注意力（Multi-head Latent Attention，MLA）。这一设计的最大动机是缩减 KV 缓存大小。

本质上，HCA 的 KV 缓存由一段 KV 嵌入的滑动窗口和一组压缩 KV 条目组成，每个条目将 key/value 压缩为一个，并跨越 m′ 个 token（DeepSeek V4 Pro 的 m′ = 128）。

![](https://substack-post-media.s3.amazonaws.com/public/images/25e34777-c0fc-4b37-9e47-495bf43b5fc2_1408x892.png)
*来源：DSv4 技术报告*

CSA 使用与 HCA 相同的 KV 缓存压缩技术，但压缩率更低（m=4）。CSA 还通过 lightning indexer 选取要关注的 token，在压缩 KV 条目上应用稀疏注意力。这种稀疏注意力继承了 DeepSeek v3.2 中的 DeepSeek Sparse Attention。

![](https://substack-post-media.s3.amazonaws.com/public/images/b6408570-ba32-4ab3-b68c-e8c62a45b2e2_2048x1012.png)
*来源：DSv4 技术报告*

通过交错使用 CSA 和 HCA，DeepSeek v4 大幅压缩了 KV 缓存大小，在 1M 上下文长度下实现了 50 倍的 KV 缓存缩减。

然而，CSA 和 HCA 的新颖性给服务框架带来了 KV 缓存管理上的挑战。例如，vLLM 的 KV 缓存内存分配器实现了复杂的策略，以确保高效的内存加载模式并支持前缀缓存（prefix caching）等服务特性。这包括设定一个能同时整除 CSA 和 HCA KV 压缩率的逻辑块大小，以及一套页大小分桶（bucketing）策略，以避免因存储每条目大小各不相同的 KV 缓存、compressor 状态和 indexer KV 而产生的内存碎片。

## 确定性

为了保证 RL 训练的稳定性，DeepSeek 全力押注于让计算具备确定性。这份投入在深入其 GPU 内核和 rollout 基础设施时可见一斑。DeepSeek 为所有运算编写了定制内核，通过强制执行特定的规约顺序来实现批不变性（batch invariance），无论批量大小如何。这包括批不变的 split KV 注意力前向、GEMM 和 MoE 反向内核。批不变内核会带来性能损失，因为使用它们就排除掉了许多无法保证确定性规约顺序的流行算法技术。DeepSeek 通过编写针对其工作负载量身定制的内核来缓解性能损失，例如按矩阵形状特化内核。在 rollout 基础设施方面，DeepSeek 专注于容错性，使所有 rollout 都可复现。DeepSeek 为每个生成请求构建了 token 粒度的预写日志（write-ahead log），这样任何在预填充或解码期间被抢占的请求都无需重新计算即可恢复。

# MegaMoE

DeepSeek V4 的发布还包含了一个新的融合 MoE 内核，它实现了 MoE 层中所有算子更好的重叠。采用专家并行的 MoE 首先执行 token dispatch all-to-all，随后是 Linear1、Activation、Linear 2，最后是 token combine all-to-all。Linear 1 和 Linear 2 是分组 GEMM 运算，某个 rank 上的每个专家将其权重应用到路由给它的 token 上。作者在 DeepSeek V4 论文中提到，其他实现会将 token dispatch 与 Linear 1、Combine 与 Linear 2 重叠/交错执行，但在算子边界处——即 Linear 1、Activation 和 Linear 2 之间——仍然存在一次跨所有专家的同步。MegaMoE 则把专家拆分成多个波（wave）并分别调度每一波，从而实现各算子更细粒度的重叠，让更多通信延迟得以隐藏。这让人联想到分布式 GEMM 之类的计算-通信融合：通过把工作负载切分成更小的分片并进行流水线化，让计算内核与依赖它的通信内核重叠，从而隐藏通信延迟。

论文声称，在 DeepSeek v4 Flash 配置下，其相对朴素内核的理论加速比为 1.92 倍——这意味着朴素内核必然有接近 50% 的时间花在了 Dispatch 和 Combine 通信上！

![](https://substack-post-media.s3.amazonaws.com/public/images/9c3b7042-b618-4550-acc9-de29e8ef0de4_2048x829.png)
*来源：DSv4 技术报告*

既然我们已经详细讨论了性能基准测试，接下来让我们讨论在 H200 和 GB200 NVL72 上运行 DeepSeek v4 时的总拥有成本和单 token 成本。

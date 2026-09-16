---
title: "InferenceX v2：NVIDIA Blackwell 对决 AMD 与 Hopper——原 InferenceMAX"
title_en: "InferenceX v2: NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX"
subtitle: "GB300 NVL72、MI355X、B200、H100、分离式服务、宽专家并行、大型混合专家模型、SGLang、vLLM、TRTLLM"
date: 2026-02-16
source: https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs
crawled: 2026-09-15
authors: ["Dylan Patel", "Cam Quilici", "Bryan Shan", "Alec Ibarra", "Kimbo Chen", "Daniel Nishball", "Cheang Kang Wen"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# InferenceX v2：NVIDIA Blackwell 对决 AMD 与 Hopper——原 InferenceMAX

> 原文：[InferenceX v2: NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**GB300 NVL72、MI355X、B200、H100、分离式服务（Disaggregated Serving）、宽专家并行、大型混合专家模型、SGLang、vLLM、TRTLLM**

InferenceXv2（原 InferenceMAX）建立在 InferenceMAXv1 打下的基础之上。InferenceMAXv1 是[我们的开源、持续更新的推理基准测试](https://github.com/SemiAnalysisAI/InferenceX)，为 AI 推理的性能与经济学设立了新标准。InferenceMAXv1 通过在数百款芯片和主流开源框架上持续运行测试，超越了静态的、单点时间快照式的基准。[免费数据看板请见这里。](https://inferencemax.ai/)

[我们的基准测试已被几乎每一位主要的算力买家广泛复现、验证和/或背书](https://inferencemax.semianalysis.com/quotes)，从 [Google Cloud](https://cloud.google.com/blog/products/compute/scaling-moe-inference-with-nvidia-dynamo-on-google-cloud-a4x) 到 [Microsoft Azure](https://blog.aks.azure.com/2025/10/24/dynamo-on-aks#enterprise-scale-inference-experiments--dynamo-with-gb200-running-on-aks) 再到 [Oracle、OpenAI](https://inferencemax.semianalysis.com/quotes)，以及更多。

InferenceXv2 在这一基础上继续扩展。它把覆盖范围扩大到大规模 DeepSeek MoE 分离式推理（disaggregated prefill，简称「disagg」）加宽专家并行（wide expert parallelism, wideEP）优化，覆盖**过去 4 年 NVIDIA 在西方市场推出的全部 6 款 GPU SKU**，以及过去 3 年 AMD 在西方市场发布的每一款 GPU SKU——InferenceXv2 跑一次覆盖所有 SKU 的完整基准，总共动用了接近 1000 颗前沿 GPU。

随着今天的发布，InferenceXv2 现在是第一个在整条帕累托前沿曲线上对 Blackwell Ultra GB300 NVL72 和 B300 进行基准测试的套件，也是第一个测试 disagg+wideEP 多节点 FP4 与 FP8 MI355X 性能的第三方基准。在 InferenceX 的后续迭代中，我们将继续把重心放在分离式服务加宽专家并行上，因为这正是 OpenAI、Anthropic、xAI、Google Deepmind、DeepSeek 等前沿 AI 实验室，以及 TogetherAI、Baseten、Fireworks 等先进 API 提供商在生产环境中部署的方案。在本文中，我们还会拆解[最新的 Claude Code Fast 模式功能](https://code.claude.com/docs/en/fast-mode)背后的系统工程原理与经济学。

我们的基准测试以 Apache 2.0 协议完全开源——这意味着我们能够以 AI 软件生态前进的同样速度快速推进。如果你喜欢我们的工作并想表达支持，[请在我们的 GitHub 上点个星标](https://github.com/SemiAnalysisAI/InferenceX)！我们还为整个 ML 社区提供免费的数据可视化工具 [https://inferencex.com](https://inferencex.semianalysis.com/)，人人都可以自行探索完整数据集。

我们将在 InferenceX 中以首日（day 0）支持的形式加入 DeepSeekv4 以及其他热门的中国前沿模型。过去 6 个月里，我们清理了大量技术债，如今已经能够[在稳定的基础设施上快速迭代](https://www.cnet.com/tech/mobile/zuckerberg-move-fast-and-break-things-isnt-how-we-operate-anymore/)。今年晚些时候，我们还会把 TPUv7 Ironwood 和 Trainium3 加入 InferenceX！如果你想为这一有影响力的使命做贡献，同时获得有竞争力的报酬，[欢迎在此申请](https://app.dover.com/apply/semianalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1)。

![](https://substack-post-media.s3.amazonaws.com/public/images/1e9a8353-ca83-4bd3-ab4a-3541132f6665_1680x1175.png)
*来源：InferenceMAX GitHub*

# 值得强调的关键观察与结果

在 FP8 下，AMD 的 MI355X disagg+wideEP SGLang 相比 FP8 B200 disagg+wideEP SGLang 取得了有竞争力的单位 TCO 性能（perf/TCO）结果；但与广泛使用的 Dynamo TRTLLM B200 FP8 相比，TRT 依旧处于碾压级领先。AMD 的 SGLang 分离式预填充+wideEP 在 FP8 下能够追平 NVIDIA 的 SGLang 性能，这是一个惊人的好消息。

我们还看到，在单节点聚合式（aggregated）服务场景下，FP8 的 AMD SGLang 交付了优于 NVIDIA SGLang 的 perf/TCO。[同样令人欣慰的是，AMD 已经弃用了他们那个二等公民式的 vllm 分支，转向更贴近上游、向一流体验更进一步。](https://x.com/vllm_project/status/2013928644302033208)敬请期待我们的《AMD 现状》（State of AMD）一文，其中会谈到 AMD 改进速度飞快的诸多领域，以及改进速度乏善可陈的那些领域。我们建议 NVIDIA 在其 TRTLLM 引擎之外，把更多重心放到 SGLang 与 vLLM 生态上。[Jensen 需要为 SGLang、vLLM 这类开放生态配备更多的资源与工程师](https://www.linkedin.com/in/akbarnurlybayev?trk=feed-detail_main-feed-card_feed-actor-image)。

至于最顶尖的前沿大规模推理服务所使用的最新推理技术（如 disagg prefill+wideEP+FP4），NVIDIA 凭借 B200、B300 以及那位「ASU 兄弟会会长」——机柜级 GB200/GB300 NVL72——在 SGLang 和 TRTLLM 两边都处于绝对碾压地位。在能效方面 NVIDIA GPU 同样占优：在所有工作负载下，每 token 的全口径配置能耗（皮焦耳，picoJoules）都要低得多。

转向 AMD，我们发现他们的系统和软件在推理上最大的问题是*[可组合性（composability）](https://en.wikipedia.org/wiki/Composability)*。也就是说，AMD 的许多推理优化实现单独运行时效果不错，但与其他优化组合到一起时，结果就不如预期那样有竞争力。具体来说，disagg prefill、wideEP 与 FP4 推理优化的可组合性亟需改善。

在 AMD 上只启用 SOTA 推理优化中的一个子集时，性能是有竞争力的；但实验室们实际会同时启用全部三项主要优化，此时 AMD 的性能目前敌不过 NVIDIA。我们强烈建议 AMD 把重心放在不同推理优化的可组合性上。我们获悉，AMD 将开始在整个软件栈层面聚焦 FP4+分布式推理的软件可组合性。这件事会在春节之后启动，因为他们大部分做 disagg prefill+wideEP 的 10x 推理工程师都在中国。

NVIDIA 的 GB300 NVL72 没有让人失望。即便面对一个强大的 H100 disagg+wideEP+MTP 基线，FP8 对 FP4 也实现了最高 100 倍的提升，FP8 对 FP8 也有 65 倍。在 H100 对比 GB200 NVL72 上，75 tok/s/user 交互性下我们看到最高 55 倍的实际性能差距。机柜级 Blackwell NVL72 正在碾压 Hopper，把 Hopper 衬得像是在小丑卖艺（jestermaxxing）。正如 Jensen 在 GTC 2025 上所说，[他是首席营收毁灭官。](https://newsletter.semianalysis.com/i/174558496/ai-total-cost-of-ownership-cost-declines)

在 GTC 2024 上，Jensen 宣称 Blackwell 的推理性能最高可达 H100 的 30 倍。Jensen 在 Blackwell 推理性能上承诺保守、交付超额。这应该能让分析师们消停一阵子，少讲些「Jensen Math（黄氏数学）」的段子。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ed3fe4a-93e9-4c47-8fb2-91f17da1b7c5_2392x1418.png)
*来源：SemiAnalysis InferenceX*

# 致谢与 InferenceX™（原 InferenceMAX）倡议支持者

我们要感谢 Jensen Huang 和 Ian Buck 对这个开源项目的支持，他们提供了最新的 GB300 NVL72 系统的访问权限，以及代表他们过去四年所产全部 GPU SKU 的服务器。感谢 NVIDIA 团队允许我们在这接近 1000 颗 GPU 上开展独立基准测试。感谢 Jatin Gangani、Kedar Potdar、Sridhar Ramaswamy、Ishan Dhanani、Sahithi Chigurupati 以及许多其他 NVIDIA 推理工程师帮助验证并优化 Blackwell 与 Hopper 配置。

我们同样感谢 Lisa Su 和 Anush Elangovan 对 InferenceMAX 的支持，感谢他们支持我们与数十位 AMD 工程师（如 Chun、Andy、Bill、Ramine、Theresa、Parth 等）的合作——这些工程师为 InferenceMAX 以及上游 vLLM/SGLang 的 bug 修复做出了贡献，也感谢他们在帮助调试和分诊 AMD 独有 bug、优化 AMD 性能方面的快速响应。

我们还要向 SGLang、vLLM 和 TensorRT-LLM 的维护者们致敬，感谢他们打造了世界级的软件栈并将其开源给全世界。你可以在这里查看他们关于 InferenceX 的文章：

- [SemiAnalysis InferenceMAX：vLLM 维护者与 NVIDIA 加速 Blackwell 推理](https://blog.vllm.ai/2025/10/09/blackwell-inferencemax.html)
- [GPT-OSS 性能优化：推高帕累托前沿](https://blog.vllm.ai/2026/02/01/gpt-oss-optimizations.html)
- [SGLang 与 NVIDIA 携手加速 SemiAnalysis InferenceMAX 与 GB200](https://lmsys.org/blog/2025-10-14-sa-inference-max/)

InferenceX 倡议还得到了许多主要算力买家和 ML 社区知名成员的支持，包括来自 OpenAI、Microsoft、vLLM、Tri Dao、PyTorch 基金会、Oracle 等的成员。[完整名单请见这里](https://inferencemax.semianalysis.com/quotes)。

# 重要技术概念入门

在本节中，我们将简要介绍一些技术概念，帮助读者更好地解读结果。部分读者可能不需要这些内容，可以直接跳到我们的结果分析。我们会在结果分析之后再对其中一些主题做更深入的探讨。

# 交互性与吞吐量的权衡

LLM 推理的根本权衡在于吞吐量与延迟。*交互性*（tok/s/user）描述系统中每个用户接收 token 的速度——它是每输出 token 耗时（TPOT）的倒数。*吞吐量*（tok/s）描述一个系统在所有用户身上总共能产出多少 token。通过批量处理请求可以获得更高的总吞吐量，但每个请求分到的 FLOPs 更少，因此完成得更慢。这类似于选择坐地铁公交还是坐赛车。地铁公交流载许多乘客，但也会频繁停靠、耗费时间，不过公交车的成本可以摊到许多乘客头上。赛车只能载一两个乘客，但几乎不会额外停靠，意味着整体行程时间更快，但人均乘坐成本要贵得多。周末去公园的人坐公交可能更合适，而送名人去目的地则赛车更好。没有万能方案。

![](https://substack-post-media.s3.amazonaws.com/public/images/18c9a3dd-3777-44d5-a3e2-b4d28140df38_2106x1380.png)
*来源：SemiAnalysis*

本文将展示的大多数基准结果中，InferenceX 给出的是一条曲线。重要的是在各个交互性/延迟水平上分析吞吐量，而不是只看最大可达吞吐量（后者通常只能在某个很低的交互性下达到）。推理没有放之四海而皆准的用例。所需的交互性与吞吐量水平取决于用例。例如，实时语音模型要求极低延迟，这样终端用户才能与 LLM 保持自然「对话」，而一个基础的问答聊天机器人则可以容忍更高的延迟。我们把判断留给读者：观察曲线并应用这一原则，找出你的用例落在吞吐量-交互性曲线的哪个位置。

单位 TCO 成本/性能与交互性/端到端延迟的关系曲线基本遵循吞吐量与交互性/端到端延迟的曲线：每小时产出的 token 越多，单 token 成本越低，因为固定的 $/小时成本被摊到了更多产出 token 上。

### 预填充与解码阶段

推理包含两个主要阶段：预填充（prefill）与解码（decode）。*预填充*发生在请求生命周期的第一次前向传播中。它是计算密集型的，因为请求中的所有 token 会被并行处理。这个阶段负责为一个序列「填满」KV 缓存。预填充之后，响应（即*解码*）一次生成一个 token。每次前向传播都要从 HBM 加载该序列的整个 KV 缓存，却只执行单个 token 的计算，因此解码是内存（带宽）密集型的。

当预填充与解码在同一个引擎上执行时，预填充会不断干扰解码批次，导致整体性能变差。

### 分离式预填充

分离式预填充（又称 PD 分离，或简称「disagg」）是把预填充与解码阶段拆分到不同 GPU 池或集群上的做法。这些独立的预填充池与解码池可以各自独立调优，并按工作负载的需求独立扩展。

# 张量并行、专家并行、数据并行（TP、EP、DP）

TP 能在小批量下实现最大交互性，但它必须在每一层执行一次 all-reduce。EP 对专家做分片，利用 MoE 稀疏性，代价是 MoE 层需要执行 all-to-all 集合通信（比 all-reduce 这类简单集合通信更昂贵），且在小批量下可能负载不均。DP 把整个模型（或模型的一部分，如注意力）复制到多组 GPU（rank）上，然后在各 rank 之间做请求负载均衡。它是最容易扩展的，但会重复加载权重，在大规模下可能造成浪费。

# 追踪性能随时间的改进

InferenceX 的主要目标之一是可视化性能随时间的改进。芯片大约以每年一次的节奏发布，而软件发布大约是每周一次的节奏。我们的目标是不断用最新最好的软件改进来更新配置方案（recipe），并对这些配置进行基准测试。

# DeepSeek R1

AMD 团队显著改进了 SGLang DeepSeek R1 FP4 所有配置的性能。在相同交互性下，AMD 在不到 2 个月的时间里把吞吐量几乎翻倍。此外，我们推动 AMD 把他们分支版 SGLang 镜像中的性能增强改动上游到官方 SGLang 镜像。从 2025 年 12 月到 2026 年 1 月，AMD 的软件性能提升最高达 2 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/d0bd5df8-c675-4dce-a853-dfa6f4d381af_1498x1102.png)
*来源：SemiAnalysis InferenceX*

为了继续向一流体验靠拢，AMD 需要加大对 vLLM 与 SGLang 维护者的支持——包括算力贡献与代码贡献——并让更多 AMD 员工担任 reviewer，以加快 AMD PR 进入上游的评审流程。

![](https://substack-post-media.s3.amazonaws.com/public/images/f7fc9e49-b04b-41b0-b0ec-df0d912c0a3c_800x434.jpeg)
*来源：SemiAnalysis*

另一方面，NVIDIA 的结果更加稳定，B200 SGLang 在类似时间段内只有小幅改进。

![](https://substack-post-media.s3.amazonaws.com/public/images/19e48a4c-0c1b-4681-b180-03ef0c8c2ce3_2346x1340.png)
*来源：SemiAnalysis InferenceX*

许多成熟 SKU 的改进微乎其微。例如 H200 TRT 单节点的性能自 10 月以来 4 个月里没有变化，但这是因为 Hopper 的支持从第一天起就非常出色，性能在这项工作负载上一直接近理论峰值，因此很难再交付增量性能提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/ca0fbb96-36c4-4040-a022-49f2185b661a_2074x1224.png)
*来源：SemiAnalysis InferenceX*

MI300X 和 MI325X 有所改进，主要来自最近一次 SGLang 发布。注意，在 InferenceX 历史的大部分时间里，AMD 使用的是未经上游化的「私有」ROCm 镜像，因此 2026 年 1 月以前的运行结果无法与更近期的结果直接对比。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b8c3b9b-7536-4cba-8b85-854d25169864_1922x1726.png)
*来源：SemiAnalysis InferenceX*

GB200 Dynamo TRT-LLM disagg 也有显著改进，最大吞吐量在 1 个多月里提升了 20%。我们在中等交互性区间（部署 wide EP 的区间）也看到了改进。这可能得益于 GB200 上 wide EP 内核的日趋成熟。

![](https://substack-post-media.s3.amazonaws.com/public/images/db4fa8dc-176c-4224-9ab5-6ebfe8f6af9c_1493x1280.png)
*来源：SemiAnalysis InferenceX*

自首次发布以来，B200 SGLang 在 FP4 和 FP8 场景下都保持了稳定且持续的改进，自去年 10 月以来部分交互性水平下每 GPU 吞吐量翻倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/1d5636b8-69d8-4676-9c3c-823da8d03514_2638x1840.png)
*来源：SemiAnalysis InferenceX*

对于 MI355X 分离式推理服务，AMD 推荐使用带 MoRI 的 SGLang。[MoRI 是 AMD 的 MoE dispatch/combine 集合通信与 KV 缓存传输库](https://github.com/ROCm/mori/tree/main)，由 AMD 驻中国的顶尖（cracked）10x 工程师团队从第一性原理构建。尽管 MoRI 还需要更多的开放 CI 与测试，我们强烈支持 MoRI 正在走的方向。这是因为 MoRI 没有采取 AMD 的历史做法——把 NVIDIA 的 NCCL 分叉成 RCCL——而是吸取 RCCL/NCCL 的经验教训，从零开始、按第一性原理构建了一个全新的软件包。一个多月以来，MoRI 的使用也带来了不错的加速，在 20-45 tok/s/user 交互性区间内每 GPU 吞吐量提升了超过 20%。

![](https://substack-post-media.s3.amazonaws.com/public/images/6b0d71aa-e6aa-425f-bbcc-25e2c1de2f4d_1900x1744.png)
*来源：SemiAnalysis InferenceX*

# GPT-OSS 120B

对于 MI300X 和 MI325X，我们看到全面的小幅改进。一些 AITER 优化在所有交互性下都改善了 MI300X 性能，切换到上游 vLLM ROCm 镜像也带来了提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/10e95c72-6372-415e-8e51-d8021815182c_2142x1784.png)
*来源：SemiAnalysis InferenceX*

就 MI325X 而言，下游 ROCm 分支镜像（用于 2025 年 10 月 5 日那次运行）中的性能增强似乎并未全部进入官方 vLLM ROCm 镜像。
遗憾的是，MI355X 目前仍在使用 vLLM 0.10.1 构建的一个分支（`rocm/7.0:rocm7.0_ubuntu_22.04_vllm_0.10.1_instinct_20250927_rc1`）。我们本来希望它早就更新了，但遗憾的是，当前的官方镜像（截至本文撰写时为 0.15.1）尚未针对 MI355X 优化，而且会碰到硬错误。我们在 MI355 上跑 vLLM 0.14 时也遇到过硬错误崩溃。坊间传闻，vLLM 0.16.0 将终于带来 MI355X 性能提升所需的全部改动。

![](https://substack-post-media.s3.amazonaws.com/public/images/1755b498-ab4d-4c02-b6fd-152ee538a34d_2126x1788.png)
*来源：SemiAnalysis InferenceX*

回到 NVIDIA 的系统，从 vLLM 0.11.2 到 0.13.0，Hopper 与 Blackwell 都实现了稳步的性能增长。很快，我们会把 NVIDIA GPU 的配置方案更新到最新版 vLLM，预计切换后会获得更大的性能提升。我们还观察到最新版 TRT-LLM 1.2.0 带来了一次性能跃升。

![](https://substack-post-media.s3.amazonaws.com/public/images/53a95093-3d25-4d01-9d64-64ea9e113749_2376x1760.png)
*来源：SemiAnalysis InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/77c591fb-74ef-46ce-bba2-9f82a52f5f6f_2362x1752.png)
*来源：SemiAnalysis InferenceX*

# 分离式推理框架

NVIDIA 的分离式推理设置使用 Dynamo。[Dynamo](https://docs.nvidia.com/dynamo/design-docs/overall-architecture) 是为多节点分布式推理设计的推理框架，具备预填充-解码分离、请求路由、KV 缓存卸载等技术。它与推理引擎无关，使我们可以在基准测试中使用 SGLang 和 TRT LLM 作为后端。对 AMD，我们使用 SGLang 搭配两种不同的 KV 缓存传输框架：MoRI 和 Mooncake。[MoRI](https://github.com/rocm/mori) 是一个聚焦 RDMA 与 GPU 集成的高性能通信接口，提供网络集合通信、专家并行内核等应用。Mooncake [最近加入了 PyTorch 生态](https://pytorch.org/blog/mooncake-joins-pytorch-ecosystem/)，支持预填充-解码分离以及许多容错多节点特性。

# DeepSeek Disagg+WideEP 结果深度解析

在几乎所有交互性水平上，disagg 在每 GPU 总 token 吞吐量上都优于聚合式推理（灰线）。多节点分离式预填充碾压单节点聚合式服务。

![](https://substack-post-media.s3.amazonaws.com/public/images/7ace6118-029a-44df-b0ef-2e7595e6f388_2032x1339.png)
*来源：SemiAnalysis InferenceX*

NVIDIA 持续为 B200/GB200 FP8 推送新更新。最新数据显示了 DeepSeek FP8 B200 TRT 单节点（启用/未启用 MTP）对比 GB200 Dynamo+TRT disagg（启用/未启用 MTP）。这表明他们在持续投入工程力量改进机柜级推理软件与 wideEP 内核。

![](https://substack-post-media.s3.amazonaws.com/public/images/29485790-238d-4e1d-aa48-0559c79c9855_2132x1247.png)
*来源：SemiAnalysis InferenceX*

对比 MI355X 的分离式推理与聚合式推理时，我们注意到一个相似的模式。分离式推理只在低交互性、大批量下反超聚合式推理。这一结论对 FP4 同样成立，原因很可能是内核优化不足。

![](https://substack-post-media.s3.amazonaws.com/public/images/25a7c41e-fa99-4117-8e49-ac121a22bf0f_2092x1241.png)
*来源：SemiAnalysis InferenceX*

在 MI355X 上把 disagg prefill+wideEP 与 FP4 组合起来时，我们观察到性能不尽如人意。

尽管理论建模显示 MI355X 上的 disagg 推理应当远好于单节点，但由于 ROCm 软件栈在把多项 SOTA 推理优化组合到一起时缺乏内核与集合通信优化，disagg 在更高交互性水平下的实际表现反而更差。

![](https://substack-post-media.s3.amazonaws.com/public/images/2d82d32f-089b-405d-b4ef-94b4956676ed_2078x1233.png)
*来源：SemiAnalysis InferenceX*

### NVIDIA TensorRT LLM 与 NVL72

TensorRT LLM 已经在 TogetherAI 等先进提供商的全球服务中每小时产出数十亿 token，它真正让 GB200 NVL72 和 GB300 NVL72 大放异彩，在高吞吐量下交付了超过两倍的性能。MTP 进一步放大了这些结果，充分发挥了芯片的全部潜力。

从成本图表看，NVL72 家族更大 world size 带来的好处也很明显。在 60 tok/s/user 的固定交互性下，每颗 GB200 NV GPU 产出的 token 数接近每颗 B200 的三倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/36087d46-94e1-4629-90cb-4b0dfad1a8c1_1856x827.png)
*来源：SemiAnalysis InferenceX*

随着交互性提高，这一差距缩小。在 130 tok/s/user 下，GB200 NVL72 几乎没有优势，按 $/百万 token 计甚至更贵。在低批量下，推理工作负载缩小到足以装进单个 HGX 节点的 NVLink 域（即 8 颗 GPU）内，GB200 NVL72 更大 scale-out 域的优势开始消失。

![](https://substack-post-media.s3.amazonaws.com/public/images/3e287d0e-947f-4fd7-9dc8-d697fad9ac7d_1781x822.png)
*来源：SemiAnalysis InferenceX*

# NVIDIA 对决 AMD：Disagg Prefill

随着今天 InferenceXv2 的发布，ML 社区第一次能看到开源 MI355X 分布式推理的完整帕累托前沿。我们展示了 B200 与 MI355X 启用与未启用 MTP 的帕累托曲线。

在 FP8 disagg prefill 上，MI355X（MoRI SGLang）与 B200（Dynamo SGLang）旗鼓相当。这两种配置都没有使用 wide EP，因为所有预填充/解码实例最多以 EP8 运行。在吞吐量与交互性帕累托前沿的两端，MI355X 都略落后于 B200。不过，在曲线中段的某些交互性水平上，MI355X disagg 略占优势。B200 和 MI355X 都从 MTP 中获益，且两颗芯片使用 MTP 带来的相对性能提升幅度相同。

![](https://substack-post-media.s3.amazonaws.com/public/images/99728443-e697-49cc-8416-7a380c60ad12_2147x1249.png)
*来源：SemiAnalysis InferenceX*

然而，如果只统计输出（解码）token 吞吐量，我们会看到在较低交互性水平下，B200 的输出 token 吞吐量远高于 MI355X。注意，在考察分离式推理配置的仅输出 token 吞吐量时，我们按解码 GPU 数量而非总 GPU 数量做归一化。在 B200 与 MI355X 上运行推理任务时，用于输出的 GPU 数量可能不同，但关键是：无论解码跑在什么配置上，B200 都更快地完成解码任务。

![](https://substack-post-media.s3.amazonaws.com/public/images/f67a92c3-b159-4b2a-bf87-ecbb7002b23c_2118x1306.png)
*来源：SemiAnalysis InferenceX*

尽管 MI355X 在 FP8 disagg 中有竞争力，其 FP4 性能却受可组合性问题拖累。AMD 单节点 FP4 性能尚可，但把 AMD FP4 disagg prefill 与 NVIDIA 相比，性能就不尽如人意，MI355X 被 NVIDIA 的 B200 彻底碾压（mogged）。在 1k1k 场景下，带 MTP 的 MI355X（MoRI SGLang）勉强胜过不带 MTP 的 B200（Dynamo SGLang）。

![](https://substack-post-media.s3.amazonaws.com/public/images/a5b9e7bc-c484-4400-9ffe-96ed4bbfb70f_2138x1236.png)
*来源：SemiAnalysis InferenceX*

一旦把 Dynamo TRT-LLM 纳入考量，B200 的性能进一步跃升，以至于 MI355X 即便启用 MTP 也追不上带 Dynamo TRT-LLM 和 MTP 的 B200。MI355X 只有靠 MTP 才能在性能上打平（不带 MTP 的）B200，且仅在约 60 tok/s/user 到约 120 tok/s/user 的交互性区间内成立。

![](https://substack-post-media.s3.amazonaws.com/public/images/0be8b8f5-b627-4dc9-938b-4a407ef19c34_2103x1233.png)
*来源：SemiAnalysis InferenceX*

把 Dynamo TRTLLM B200 disagg prefill 与 SGLang MoRI MI355 disagg prefill 相比，由于 TRTLLM 上的 disagg prefill 实现更成熟，AMD 被碾压得很惨。

![](https://substack-post-media.s3.amazonaws.com/public/images/89827e17-6cfd-42f1-b250-d7f07cbe6a09_2120x1242.png)
*来源：SemiAnalysis InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/c53a37b8-dd9f-4142-b114-60e6e2c7f3e7_3446x1946.png)
*来源：Dwarkesh Podcast 与 SemiAnalysis*

下图展示了构成 MI355X（MoRI SGLang）帕累托前沿的各类并行配置。注意，目前没有任何点使用 wide EP（即 EP 16、32 等配置）。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1b62a52-bd6a-4cd1-82e7-65b6903d82ac_2996x1774.png)
*来源：SemiAnalysis InferenceX*

# 拆解推理服务商的单位经济模型

下面是 OpenRouter 上所有提供 DeepSeek R1 0528 FP8 服务的推理提供商列表，以及各自的每百万输入/输出 token 成本与所列平均交互性。抛开 Chutes 不谈，中游服务商的交互性大约为 35 tok/s/user。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce79108c-8341-4100-86de-943d8ca3c34e_916x1190.png)
*来源：OpenRouter*

然后我们可以用 InferenceX 的真实数据，在 35 tok/sec/user 的交互性水平上插值出每百万输入/输出 token 的成本——鉴于上面的数据，这是一个合理的交互性水平。

正如我们在后文提到的，这些数据最好被理解为*基线*数据，并不能完全代表真实世界的推理，主要因为 InferenceX 用随机数据做基准并禁用了前缀缓存。换言之，真实世界的性能/成本*至少*会这么好。同样需要注意的是，并非*每颗 GPU* 在*每个*交互性水平上都有数据点，因此我们无法在每个交互性水平上做*精确*比较。尽管如此，我们认为下面呈现的柱状图对比是（非常）合理的插值，可替代精确数据点使用。

在这一交互性水平上比较 disagg+wideEP 配置，我们可以看到分布式推理技术在 perf/TCO 和总吞吐量两方面都极为有效。我们也看到大规模 scale-up 域（如 GB300 和 GB200 NVL72）在每 GPU 总吞吐量上占据绝对优势。

值得注意的是，在这一交互性水平下（8k1k 工作负载类型），启用 MTP 的 B200 能取得最佳 perf/TCO。下面我们还列出了每颗 GPU 的总拥有成本（TCO）（自持——超大规模云厂商口径）：

![](https://substack-post-media.s3.amazonaws.com/public/images/f200bfa6-02b5-464f-a4ea-ffe88cb6ed49_2520x81.png)
*来源：SemiAnalysis TCO 模型*

让我们用上述发现深入挖掘大规模 LLM 服务的单位经济模型。从上面的 OpenRouter 数据看，Crusoe 以 36 tok/sec/user 的交互性提供服务，输入 token $1.35/M，输出 token $5.40/M。如果我们假设没有缓存命中，且 Crusoe 至少使用 H200 并配备 MTP、disagg、wide EP 等 SOTA 推理技术，那么上述数据意味着他们的成本*不超过* $0.226/M 输入 token 和 $2.955/M 输出 token，对应输入 token 端最高 83% 的毛利率（折旧计入销货成本）、输出 token 端 45% 的毛利率。

当然，这些假设未必*完全*正确，这些计算也没有考虑停机或低利用率，但它展示了用 InferenceX 数据可以做的有趣数学。关于推理经济学的更多分析，请见 [SemiAnalysis Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

OpenRouter 数据还显示 Nebius AI Studio（Fast）以 167 tok/sec/user 的交互性提供 DeepSeek FP4 服务，输入 $2/M、输出 $6/M。在 InferenceX 中相应调整交互性水平后，我们得到以下数据。

在这么高的交互性下，必须采用 MTP 这类投机解码技术才能达到足够高的吞吐量，让推理具备经济性。幸运的是，MTP 能在整体模型精度风险相对较低的情况下提升吞吐量。我们将在本文后续章节进一步讨论 MTP，以及如何用它提升吞吐量/降低成本。

最后，我们再展示一张 125 tok/s/user 下 FP8 DeepSeek 工作负载的图表。这是另一个低延迟工作负载，MTP 显著改善了经济可行性。与前一例相同，我们注意到在这些更高的交互性区间，最便宜的配置全部使用了 MTP。

![](https://substack-post-media.s3.amazonaws.com/public/images/ccabb1a5-220a-4623-a615-245053808f24_2086x1738.png)
*来源：SemiAnalysis InferenceX*

### NVIDIA Disagg Prefill 与 WideEP

EP 需要 all-to-all 通信，即每颗 GPU 都要向其他每颗 GPU 发送 token。这对带宽的需求极高。回想一下，NVIDIA 的服务器有两个独立的网络域——NVLink 构成的 scale-up 域，以及通常采用 InfiniBand 或以太网作为网络协议的 scale-out 域。

- NVLink 域（NVL72 机柜内）：72 颗 GPU 通过 NVLink 互连，每颗 GPU 单向带宽 900 GB/s。这大约是基于 InfiniBand/以太网的 scale-out 网络带宽的 7-10 倍。
- InfiniBand/RoCEv2 以太网（NVL72 机柜之外）：通常每颗 GPU 单向 400-800 Gbit/s（50-100 GB/s）。注意，我们对 NVIDIA 的全部测试都在基于 InfiniBand 的集群上进行。

TP 把每一层的权重矩阵分片到各 GPU 上。这意味着每一层的每一个 token 最多需要两次 all-reduce 通信（一次在列并行 GEMM 之后，一次在行并行 GEMM 之后）。对 EP 来说，all-to-all 只在 MoE 层进行。每颗 GPU 只发送路由到各专家的 token。这意味着 EP 在所有层上的通信开销都低于 TP。

由于 EP 的 all-to-all 通信带宽需求随参与方数量增长，在被迫穿过更慢的 IB/以太网架构之前，留在高带宽 NVLink 域内是更优选择。有了 NVL72，跨 72 颗 GPU 的 EP 可以完全不离开 NVLink；而前几代（NVLink 域只有 8 颗 GPU）只能以 NVLink 速度跨 8 颗 GPU 做 EP，之后就会撞上更慢的 IB/以太网。

Wide EP 在权重加载效率上也有重大优势。对 DeepSeek R1 这类模型，解码受内存带宽限制：瓶颈在于 GPU 从 HBM 加载权重的速度。采用 wide EP（如 DEP32）时，32 颗 GPU 共同持有并加载一次 670B 权重，每颗只加载自己的分片（约 21B）。全部 32 颗芯片的总 HBM 带宽都用于加载单份模型副本。相比之下，用更窄的 EP 加更多 DP 副本（如 5xDEP8）时，5 个副本各需一份完整的 670B 权重，即全系统 5×670B = 3.35T 的冗余权重加载。EP 把权重摊薄到各芯片上；DP 则不断复制它们。这就是为什么 NVLink 这类高带宽互连所赋能的更宽 EP，能带来显著更高的每 GPU 吞吐量。

![](https://substack-post-media.s3.amazonaws.com/public/images/7ed2a472-3511-4b29-afbd-0c593795085a_2434x1430.png)
*来源：SemiAnalysis InferenceX*

总体而言，由于负载均衡的原因，低并发下更偏好 TP。小批量时，EP 会遭受 token 到专家路由不均的问题，导致部分 GPU 利用不足而另一些过载。TP 没有这个问题，因为每颗 GPU 持有每个专家的一个切片，总是分到等量工作。在较低并发下，这种负载不均衡的代价超过了 TP 额外的通信开销。

在更高并发下，这一权衡发生变化。专家激活在更大批量下分布更均匀，EP 的通信与权重加载优势压过了 TP 昂贵的逐层 all-reduce。在曲线中段，TP+EP 混合配置兼顾两者：在每个专家内部用小 TP 组做负载均衡，同时在更广的 GPU 集合上用 EP 摊薄权重并降低通信。

对更高交互性水平（小批量），大的 scale-up world size 往往带不来更强的性能。走 IB 的 B300 disagg 与 NVL72 的 GB300 性能相同，因为工作负载是延迟受限而非带宽受限。NVL72 巨大的 NVLink 带宽优势并不重要，因为在途 token 批量极小，连慢得多的 IB 链路都喂不饱。

预填充/解码分离同样功不可没。预填充计算重且突发性强；解码受内存带宽限制且是稳态负载。两者共享同一批 GPU 时会互相干扰，造成延迟抖动和容量浪费。把它们分到专用 GPU 池，各自运行与自身特性匹配的工作负载，可以提升有效利用率。这就是为什么分离式 B200 配置在吞吐量-交互性曲线中段优于单节点 B200。PD 分离加上跨更多 GPU 走 IB 的更宽 EP，比把两个阶段塞进单个 8-GPU 节点更高效地摊薄了权重。

[旁注：TogetherAI 的 10x 推理工程师注意到多轮流量的一种模式——第一轮预填充的要求与后续轮次的预填充大不相同——并据此做了分离，带来了更好的 TTFT 表现。](https://www.together.ai/blog/cache-aware-disaggregated-inference)

![](https://substack-post-media.s3.amazonaws.com/public/images/bfdcb99e-dc02-4468-bd72-b25a7be6c15d_2380x1386.png)
*来源：SemiAnalysis InferenceX*

# Jensen 承诺保守、交付超额——Hopper 对决 Blackwell 对决机柜级 NVL72

在 GTC 2024 上，Jensen 在台上承诺从 H100 到 GB200 NVL72 最多 30 倍的性能提升，[所有人都以为这是典型的营销美化（lookmaxxing），现实世界根本达不到。](https://newsletter.semianalysis.com/p/nvidia-blackwell-perf-tco-analysis)许多人还给他这种被视作「现实扭曲力场」的玩法起了各种标签，好多讲几句 Jensen Math 段子。的确——[我们也曾指出，这个 30 倍性能差距对比的是 H200 FP8 的最差情况](https://newsletter.semianalysis.com/i/175661150/benchmarking-the-h200-on-its-bad-hair-day)与 GB200 FP4 的合理情况。

![](https://substack-post-media.s3.amazonaws.com/public/images/4fec3378-2cf4-4c1c-a40d-bcbd788c9a70_3022x1964.jpeg)
*来源：NVIDIA GTC 2024*

但事实证明笑话落到了他们自己头上。快进将近两年，我们现在可以看到，那根本不是营销吹嘘，Jensen 对 Blackwell 性能其实一直承诺保守。根据我们的测试，即便与强大的 H100 disagg+wideEP FP8 基线相比，Blackwell 在大规模 MoE 推理上也是好得出奇：在 116 toks/s/user 下，GB200 NVL72 FP4 实现了高达 98 倍的性能提升，GB300 NVL72 FP4 更是高达 100 倍！也许新的 Jensen Math 法则是：token 吞吐量上他承诺多少，就交付双倍。花得越多，省得越多，诚不我欺！

![](https://substack-post-media.s3.amazonaws.com/public/images/70638c7e-69a6-43f2-96a4-23766bcabbd2_2121x1248.png)
*来源：SemiAnalysis InferenceX*

即使把 Blackwell 与 Blackwell Ultra 更高的总拥有成本算进去，相比 Hopper，我们在每美元 token 数上仍看到 9.7 倍（40 tok/s/user）到 65 倍（116 tok/s/user）的提升。[你可以在我们的免费网站上详细探索 Hopper 与 Blackwell 的性能对比](https://inferencemax.semianalysis.com/?i_seq=8k%2F1k&g_model=DeepSeek-R1-0528&g_rundate=2026-02-12&g_runid=21928999802&i_prec=fp4%2Cfp8&i_metric=y_costh&i_log=1#inference)。Blackwell 相比 Hopper 的性能好到我们需要给数据看板加上对数刻度才能可视化。

![](https://substack-post-media.s3.amazonaws.com/public/images/402b23af-7ad6-46e4-97af-a5698ea2bd87_2176x1416.png)
*来源：SemiAnalysis InferenceX*

如前文所述，B300 服务器用 900GByte/s/GPU 的 NVLink scale-up 网络最多连接 8 颗 GPU，而 GB300 NVL72 服务器用 NVLink scale-up 网络连接 72 颗 GPU。所以当推理设置需要 8 颗以上（但少于 72 颗）GPU 时，我们需要引入多台 B300 服务器节点组成推理系统，这意味着通信回落到较低的 InfiniBand XDR scale-out 网络，每 GPU 带宽 800Gbit/s（单向）。相比之下，机柜级 GB300 NVL72 通过 NVLink 连接 72 颗 GPU，每 GPU 带宽 900GByte/s（单向）。可以看到，机柜级服务器让推理系统中的 GPU 之间互相通信的带宽比多节点 B300 服务器方案高出 9 倍以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/8664f48c-037c-45cc-b6f8-1999ed0cee0e_2298x1430.png)
*来源：SemiAnalysis InferenceX*

诚然，GB300 NVL72 的每 GPU 全口径成本更高，但这也只是把带宽层面的性价比优势削弱到 8 倍领先。机柜级架构的带宽优势直接带来了低得多的单 token 成本。Google TPU、AWS Trainium 和 NVIDIA 是当今仅有的已部署机柜级系统设计的 AI 芯片。AMD 首个机柜级 MI455X UALoE72 系统的工程样片和小批量生产将在 2026 年下半年，而由于制造延期，量产爬坡和首批生产 token 要到 2027 年 Q2 才能在 MI455X UALoE72 上产生。

![](https://substack-post-media.s3.amazonaws.com/public/images/58c7b664-76a7-454b-ac99-036b0b6f4abb_2132x1456.png)
*来源：SemiAnalysis InferenceX*

# Blackwell 对决 Blackwell Ultra

纸面上，新发布的 Blackwell Ultra 与 Blackwell 内存带宽相同、FP8 性能相同，FP4 性能只高 1.5 倍；但实测我们发现 Blackwell Ultra 的 FP8 性能最高好 1.5 倍，而 FP4 只好 1.1 倍。这可能是因为 Blackwell Ultra 是新发布的 GPU，软件尚未充分优化。

# MI355X 对决 MI325X 对决 MI300X

在 AMD SKU 之间，我们看到 MI355X 相比 MI300X 最高 10 倍的性能提升。AMD 目前只让 DeepSeek SGLang 分离式推理在 MI355X 上跑通，尚未提交 MI300X 或 MI325X 的分离式推理结果，可能是因为老 SKU 上的软件问题仍在解决中。

![](https://substack-post-media.s3.amazonaws.com/public/images/d6dd3138-e228-4121-a061-4aa92c84d6a4_2334x1390.png)
*来源：SemiAnalysis InferenceX*

谈到成本：对 FP8 的 DeepSeekR1，在 24 tok/s/user 交互性下，MI355X 的推理成本比 MI325X 便宜略低于 3 倍。每 GPU 吞吐量是 MI325X 的略低于 4 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab1ad749-fe92-4209-9347-4456d22b0cfd_2088x1432.png)
*来源：SemiAnalysis InferenceX*

# AMD 在 FP4、分布式推理与宽专家并行上的可组合性问题

虽然 AMD 在单节点 FP4 上表现尚可，在 FP8 分布式推理上也能与 B200 SGLang 掰手腕，但当前 AMD 开源推理栈的问题在于：单项推理优化各自表现不错，而真实客户部署时会把多项优化组合起来使用。顶级 AI 实验室全都在同时使用 FP4 **加**分离式推理**加**宽专家并行，问题正出在这里。

AMD 的软件仍未达标。SemiAnalysis 和 AMD 内部的理论极限（speed-of-light）建模都显示：对 FP4 而言，带宽专家并行的分离式推理应该比单节点 MI355X 上的推理表现更好。遗憾的是，软件仍然是 AMD GPU 的巨大瓶颈。AMD 管理层需要继续收紧工程人才的资源分配，例如把工程资源从 ATOM 这类没人用的单人节点宠物项目上抽走，转而解决上述分离式推理、宽专家并行与 FP4 之间推理优化可组合性的问题。当前软件之所以差强人意，是因为缺乏聚焦、对行业所处阶段的优先级判断失误。所有顶级实验室都已经在用分离式推理和宽专家并行；AMD 需要停止聚焦单节点，转而为开源解决方案重度投入多节点推理。

在开源分布式推理、宽专家并行与 FP4 可组合性上，AMD 落后超过 6 个月——[NVIDIA 和 SGLang 团队六个月前就展示了他们在 DeepSeek 上的 NVFP4 性能](https://lmsys.org/blog/2025-09-25-gb200-part-2/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/eddd9541-ed5a-4e49-aab2-291d49fd7e68_2132x1252.png)
*来源：SemiAnalysis InferenceX*

# AMD ATOM 引擎

AMD 推出了名为 ATOM 的新推理引擎。ATOM 的单节点性能略好，但缺少大量功能，导致它无法用于真实工作负载。举个例子：它不支持 NVMe 或 CPU KVCache 卸载、工具解析（tool parsing）、宽专家并行，也不支持分离式服务。这导致它在生产环境中零客户使用。与 NVIDIA 的 TRTLLM 不同——后者在 TogetherAI 等公司全球每小时产出数十亿 token，并且[确实支持工具解析和其他功能](https://nvidia.github.io/TensorRT-LLM/commands/trtllm-serve/trtllm-serve.html#cmdoption-trtllm-serve-serve-tool_parser)——由于缺乏上述功能，目前没有任何 token 工厂在使用 ATOM。

此外，vLLM 等开源推理引擎的维护者对 AMD 感到失望，因为 AMD 提供的工程与 GPU 资源不足。例如，vLLM 首席维护者 Simon Mo 在这个 GitHub RFC 中指出，他至今没有一台可以加入 vLLM CI 的可用 MI355X，因此用户体验很差。目前 vLLM 上 MI355X 的测试数量为零，而 NVIDIA 的 B200 在 vLLM 上有很多测试。类似地，vLLM 上的 MI300X CI 机器也不够。上游 vLLM 至少还需要 20 台 MI300 机器、20 台 MI325 机器和 20 台 MI355X 机器，才能达到与 CUDA 同等的可用性水平。

我们 SemiAnalysis 一直在推动 AMD 为 vLLM 贡献更多算力，最近几周已经有一些成效。vLLM 将开始获得几台 MI355X 机器，使其 CI 测试覆盖率从 0% 提升到非 0%。关于 AMD 过去对 vLLM、SGLang、PyTorch CI 机器投入的疲软，以及 Anush 如何开始着手解决，我们将在即将发布的《AMD 现状》一文中详谈。在 SemiAnalysis，我们将搭建内部看板，追踪 AMD 与 NVIDIA 在 vLLM、SGLang、PyTorch 和 JAX 上运行的测试数量与测试质量。

更重要的是，vLLM 维护者表示，由于机器资源匮乏，他们无法为 ROCm 提供 vLLM 首日（day 0）支持。这种巨大的上市时间差距持续导致 ROCm 落后，也给 NVIDIA 留下了巨大的空间，让他们得以继续收取疯狂的 75% 毛利率（相对销货成本 4 倍加价）。

![](https://substack-post-media.s3.amazonaws.com/public/images/96fd0617-347d-49a1-a971-19e42faeab25_1435x1289.png)
*来源：Github*

最后，AMD 缺少足够的「通过功能牵引与代码所有权展现出持续上游参与」的 committer，也缺乏能够评审自家代码的 reviewer。这就是 ROCm vLLM 开发速度远慢于 CUDA vLLM 的原因。

AMD 有许多在 ATOM 上工作的天才 10x 工程师，我们鼓励 AMD 管理层考虑把这些 10x 工程师重新部署到人们真正使用的库和框架上，比如 vLLM 和 SGLang。

如前所述，AMD 还需要优先解决 FP4、wideEP 与分离式服务的可组合性问题，而不是过度聚焦于单节点 FP4 的优化。

![](https://substack-post-media.s3.amazonaws.com/public/images/da3b4a10-0f65-403d-a9f6-093b86753c02_2120x1258.png)
*来源：SemiAnalysis InferenceX*

# 多 token 预测（MTP）

投机解码通过用一个廉价的小型草稿模型提前提议若干 token，来降低自回归生成的成本。大模型随后在单次前向传播中校验这些被提议的 token，过程类似于一次预填充计算。对给定的输入序列长度，输入再多 N 个 token 时单次前向传播耗时大致相同。投机解码利用这一性质，在小模型上推理、为主模型草拟多个 token，让主模型用单次前向传播校验，在相近的时间预算内最多多产出 N 个 token。

![](https://substack-post-media.s3.amazonaws.com/public/images/b2b2aa12-c308-4f4b-84f7-969228600ce5_2296x1126.png)
*来源：Brendan Bycroft*

这一「相同时间预算下多产 token」的假设对稠密模型最为成立，因为批量校验可以在多个位置复用同一条权重流。对混合专家模型，不同 token 可能路由到不同专家，因此校验多个草稿 token 可能比单 token 解码激活更多专家，迫使额外的专家权重从内存中读取。正如 EAGLE 论文中 Mixtral 8x7B Instruct 模型的结果所示，这些额外的内存流量会侵蚀带宽节省，使校验的开销与标准解码步相当。

多 token 预测在不需要独立草稿模型的情况下追求类似收益。模型的架构中加入了辅助预测头，使单一模型能基于同一底层表示一次提议多个未来 token。由于提议来自最终为其打分的同一个模型，分布对齐性更好。多 token 预测也避免了额外服务一个模型带来的运维复杂度，同时仍能启用多 token 生成策略，但要求 MTP 头与主模型一起预训练。

![](https://substack-post-media.s3.amazonaws.com/public/images/27ee5a46-78b5-40dd-b76d-1f096e0ae06d_1755x1154.png)
*来源：SemiAnalysis InferenceX*

在所有 SKU 上，启用 MTP 都带来性能提升。通过利用通常闲置的 logits 来校验多出来的 token，只增加了极少的计算开销，省下了解码期间昂贵的额外权重加载。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb5fc8fa-d129-475c-bb87-664e08bc6179_1773x1151.png)
*来源：SemiAnalysis InferenceX*

大批量下，推理形态相比小批量受内存带宽的限制更轻。由于投机解码（含 MTP）的本质是用富余算力换取更少的内存受限解码步，来自投机 token 的额外校验工作未必能干净地塞进空隙，因此大批量下的改进幅度更小。

在成本方面，MTP 可以带来巨大的节省。在下表中我们看到，用 Dynamo TRT 跑 FP4 的 DeepSeek-R1-0528 每 million 总 token 成本为 $0.251，而启用 MTP 可以把成本大幅压低到每 million 总 token 仅 $0.057。

![](https://substack-post-media.s3.amazonaws.com/public/images/dcf44984-9cb9-49ae-b35a-aeb5b5d14244_1566x1778.png)
*来源：SemiAnalysis InferenceX*

在所有配置中，当其他条件不变时，对 DeepSeek R1 使用 MTP 能提升交互性，且对模型精度没有显著影响。这与 DeepSeek V3 技术报告的结论一致。

![](https://substack-post-media.s3.amazonaws.com/public/images/1143164c-b38f-4ca9-888a-e9e270d6ef48_1757x1187.png)
*来源：SemiAnalysis InferenceX*

关于 MTP 性能数据的有效性，有人可能质疑合成数据集的分布未必像真实数据。但对比 MTBench 与我们 1k1k 基准之间的 MTP 接受行为，我们看到非常相似的分布，证实了 InferenceX 基准是真实世界生产性能的良好代理。当然，InferenceX 并不完美，我们也一直在寻求改进。如果你想参与这项使命，[请在此申请加入我们的特别项目团队](https://app.dover.com/apply/semianalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1)。

![](https://substack-post-media.s3.amazonaws.com/public/images/6c4a7c01-3d56-486d-b959-cb4b6468f56f_2408x1390.png)
*来源：SemiAnalysis InferenceX*

# 精度评估

吞吐量优化有时会悄悄牺牲精度（例如激进放松接受率、解码参数调整、数值不稳定的内核，或端点配置错误）。没有评估环节的话，一台配置错误的服务器（截断、错误的解码、错误的端点参数）依然能跑出漂亮的吞吐量数字，但给出的答案是垃圾。例如，正是这层额外检查帮我们发现了 GPT-OSS 某个 DP attention 实现的问题。

现在，每个有代表性的吞吐量配置都附带一项数值精度检查。目前我们只用 GSM8k，但它是个非常简单的基准，评估分数可能不会因数值计算差异而变化太多，更难的基准在数值精度上可能表现出更大的差异。因此，我们计划未来扩展到更难的基准，如 GPQA、HLE、MATH-500、SWE-Bench verified。

另一种性能-精度权衡是量化。以更低精度服务模型可能导致模型输出变差。对 DeepSeek R1，FP8 的评估分数比 FP4 略高。注意 GSM8k 评估已饱和，而且 QAT/PAT 期间常常会针对常见的 GSM8k、MATH-500 等做校准，导致有时评估结果很好，而真实世界终端用户的评估不佳。如果你想加入团队、一起弄清如何正确评估推理引擎精度，[请在此申请加入这项使命](https://app.dover.com/apply/semianalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1)。

![](https://substack-post-media.s3.amazonaws.com/public/images/e58e6323-b5d1-4221-9c51-ff39b44d1f98_1779x1180.png)
*来源：SemiAnalysis InferenceX*

# Anthropic Fast 模式推理详解

Anthropic 最近随 Opus 4.6 一起发布了「[fast mode](https://code.claude.com/docs/en/fast-mode)」。其价值主张：模型质量相同，速度约 2.5 倍，价格约 6–12 倍。两个数字乍看都可能令人意外，一些用户猜测[这一定需要新硬件](https://x.com/Yuchenj_UW/status/2020214926133063705)。其实不需要。事实上，这只是根本性权衡的体现。任何模型都可以在很宽的交互性水平（每用户 tokens/秒）范围内被服务，每百万 token 成本（CPMT）也随之变化。沿用我们前面的比喻：梅赛德斯既造地铁公交，也造赛车。

只会盯着账本的人可能觉得 fast mode 更贵，但透过总拥有成本的镜头看，在某些情况下 fast mode 其实便宜得多。例如，一个 GB200 NVL72 机柜可能要花 330 万美元；如果 claude code 的智能体循环（生产环境跑在 Trainium 上）通过工具调用去调用 NVL72 机柜，而这些机柜的推理速度慢 2.5 倍，你就需要 2.5 倍的机柜来交付推理——意味着不启用 fast mode 会多花接近 500 万美元的额外开支。

![](https://substack-post-media.s3.amazonaws.com/public/images/cad37655-7b9a-4c86-81a8-3314ad0526fe_1694x348.png)
*来源：Anthropic*
![](https://substack-post-media.s3.amazonaws.com/public/images/4bb71482-fe77-4e33-b5cb-b7db512b61c1_1700x439.png)
*来源：Anthropic*

考虑一个跑在 B200 + TRT-LLM 上的 DeepSeek R1 0528 FP4 编程工作流。在 50 tok/sec/user 交互性下，推理成本约为 $0.56/M 输出 token。在 125 tok/sec/user 交互性下，升至约 $4/M 输出 token——速度提升 2.5 倍，价格上涨约 7 倍，与我们在 Anthropic fast mode 上看到的比例高度一致。注意这里假设 DeepSeek R1 与 Opus 4.6 相当，事实并非如此，但大原则依然成立。

![](https://substack-post-media.s3.amazonaws.com/public/images/66509f21-d3e5-435f-9163-50d9be56c789_1930x1162.png)
*来源：SemiAnalysis InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/6621150f-7da2-44ae-9695-493374487825_1972x1122.png)
*来源：SemiAnalysis InferenceX*

这直接源于 LLM 推理中延迟与吞吐量的根本权衡。大批量下，GPU 达到更高的利用率和更大的总 token 吞吐量，意味着并发服务的用户更多、单 token 成本更低。小批量、每请求并行度更高时，每个用户得到更快的响应，但总 token 吞吐量下降。由于[加速器的小时成本](https://semianalysis.com/ai-cloud-tco-model/)是固定的、与使用方式无关，吞吐量越低，可摊薄该成本的 token 就越少，因此每 token 价格更高。

简而言之，fast mode 未必是硬件故事，它不过是在同一批 GPU 上用吞吐量换延迟的自然结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/132f55e4-43c7-4df3-bb4e-1408d85c2782_2718x1796.png)
*来源：SemiAnalysis InferenceX*

此外，我们观察到如前文所解释的投机解码这类推理优化技术，可以直接带来更便宜的推理；不需要新芯片。

举下面这个例子：8k/1k 工作负载上的 DeepSeek R1 FP4。在 150 tok/sec/user 交互性水平下，GB300 Dynamo TRT 的基线每百万 token 成本约为 $2.35，而启用 MTP 把价格降到约 $0.11。在这个交互性水平下，仅仅通过采用一项推理优化技术，价格就下降了约 21 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/f88b30b6-aa73-4ad2-a008-b2e8f940cfd0_1958x1104.png)
*来源：SemiAnalysis InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/f6dfa226-93d7-4596-9dc5-feebd5ef1dce_1966x1098.png)
*来源：SemiAnalysis InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/8742f134-05d4-4a07-9257-8c93b4730cd7_2704x1790.png)
*来源：SemiAnalysis InferenceX*

把交互性水平固定在 50 tok/sec/user，我们进一步看到 MTP 能在多种芯片上把 CPMT 有效降低多少。

![](https://substack-post-media.s3.amazonaws.com/public/images/bc992849-b42d-4899-81a3-77105c86886b_1950x1250.png)
*来源：SemiAnalysis InferenceX*

# 宽专家并行（WideEP）与分离式预填充

在本节中，我们将更深入地讨论专家并行，并解释什么是*宽*专家并行。随后我们会解释分离式预填充的概念、它与 WideEP 有何不同，以及 WideEP 与分离式预填充如何协同使用以达到 SOTA 性能。

# WideEP（宽专家并行）

到现在，大多数前沿 AI 实验室都采用混合专家（MoE）模型架构而非稠密架构。在 MoE 架构中，每个 token 只激活一部分「专家」。例如 DeepSeek R1 总参数 671B，但激活参数只有 37B。具体来说，DeepSeek R1 有 256 个路由专家（外加 1 个共享专家），每个 token 被路由到 8 个不同的专家。这种架构天然适合专家并行（EP）：把专家权重均匀分布到若干 GPU 上。

考虑在单台 8-GPU 服务器上服务 DeepSeek R1。671B 参数规模下，必须采用某种并行方式才能把模型装进可用的 HBM。最朴素的方法是张量并行（TP），把每个权重矩阵分片到所有 GPU 上。这对稠密模型有效，但忽略了 MoE 的稀疏激活模式。TP=8 时，每个专家的权重被分片到全部 8 颗 GPU 上，意味着每次专家激活都需要一次跨全部 GPU 的 all-reduce，而且 GEMM 的归约维度变小导致算术强度降低——尽管每个 token 只激活 256 个专家中的 8 个。TP 把每个专家当成稠密层对待，付出全额的跨 GPU 通信成本，而模型的稀疏性完全未被利用。

专家并行采取了更合适的思路：把整个专家分配到单颗 GPU 上。EP=8 时，我们把每层的 256 个专家分到 8 颗 GPU 上，每颗 GPU 每层 32 个专家。每颗 GPU 持有约 1/8 的专家权重，加上一份完整的非专家权重副本（注意力投影、嵌入、归一化层和共享专家）。由于 DeepSeek R1 约 90% 以上的参数是路由专家权重，EP 拿到了大部分内存节省，而把剩下不到 30B 的非专家参数在全部 8 颗 GPU 上各复制一份的代价可以承受。

每层的前向传播分两个阶段进行。注意力阶段，每颗 GPU 作为独立的数据并行 rank，用自己复制的非专家权重处理自己那部分请求，不需要 GPU 间通信。MoE 阶段，轻量级路由器决定每个 token 需要哪些专家，token 通过 all-to-all 通信被派发到相应的 GPU。每颗 GPU 只对路由到自己的 token 执行本地专家计算，结果通过第二次 all-to-all 返回。

![](https://substack-post-media.s3.amazonaws.com/public/images/2f923fd4-57c0-418e-8b01-49025b9c48d5_8236x3544.png)
*DeepSeek R1 的 EP8 DP8 部署。每层的全部 256 个专家被均匀分配到 8 颗 GPU 上，而注意力及其他非专家权重（共享专家、门控网络、RMSNorm、LM head 等）则在全部 8 个 DP rank 上复制。来源：SemiAnalysis*

最直观的扩展方式是复制：跨 N 个节点部署 N 个独立的 EP8 实例。每个实例独立服务请求，没有跨节点通信。这样吞吐量线性扩展，但每颗 GPU 仍持有每层 32 个专家，每个 token 最多激活这 32 个本地专家中的 8 个。75% 的专家权重在 HBM 里坐冷板凳。

**宽专家并行**（WideEP）换了个思路：跨节点扩展 EP，而不是复制独立实例。在 64 颗 GPU 的集群（8 节点）上，DP64/EP64 让每颗 GPU 每层只放 256/64 = 4 个专家，同时每颗仍持有一份完整的非专家权重副本。MoE 阶段，来自全部 64 个 DP rank 的 token 通过 all-to-all 派发到承载其路由专家的 GPU 上。

相比单节点 EP8 基线，这带来三重叠加的收益。第一，每 GPU 的专家占用从 32 个降到 4 个，腾出大量 HBM 给 KV 缓存，直接提升每 GPU 批量容量。第二，64 个 DP rank 把 token 汇入每 GPU 更少的专家，提升了每专家 token 数，提高算术强度（每字节权重加载对应的 FLOPs 更多）并改善计算利用率。同一份专家权重每步服务 8 倍的 token。第三，聚合 HBM 带宽随 GPU 数量线性增长；64 颗 GPU 同时加载专家权重，提供单节点 8 倍的内存带宽，缓解内存瓶颈。

![](https://substack-post-media.s3.amazonaws.com/public/images/1ae2668e-28ef-4a1f-8ab1-0b5f1373a1d1_8476x3546.png)
*DeepSeek R1 的 WideEP EP64 DP64 部署。每层的全部 256 个专家被均匀分配到 64 颗 GPU（8 节点）上，注意力及其他非专家权重（共享专家、门控网络、RMSNorm、LM head 等）则在全部 64 个 DP rank 上复制。来源：SemiAnalysis*

上述配置只用了 DP+EP（也称 DEP），每颗 GPU 持有一份完整的非专家权重副本。随着 GPU 数量增长，这种复制越来越浪费。在 64-GPU 的 DP64/EP64 部署上，每颗 GPU 都存一份约 40B 非专家参数的相同副本。

在 GPU 组内加入张量并行可以解决这个问题。在 EP64/DP8/TP8 配置中，64 颗 GPU 被组织成 8 个 DP 组、每组 8 颗 GPU。每个 TP 组内，注意力投影、共享专家、归一化层和 LM head 被切成 8 份，因此每颗 GPU 只持有 1/8 的非专家权重。在整个集群层面，256 个专家仍像之前那样按每 4 颗 GPU 一个专家分布。

纯 DEP 只有一种通信模式：用于专家路由的 all-to-all。加入 TP 后，每个 TP 组内为注意力与非专家计算引入了第二种通信——all-reduce。关键设计原则是把 TP 组放在单个节点内，由 NVLink 或 MNNVL 提供高带宽互连，而让 EP/DP 跨节点运行，因为 all-to-all 通信模式可以容忍更高的延迟。

一如既往，权衡仍是吞吐量对延迟。组内 TP=8 意味着这 8 颗 GPU 共享一个批量、每个解码步都要同步，有效 DP 度从 64 降到 8。注意力侧每 GPU 的批处理独立性丢了。但每个 DP 组每步处理注意力的速度快了 8 倍，因为矩阵乘法被拆分到 TP 组的 8 份上。每 token 延迟下降，峰值并发也下降，使该配置相对纯 DEP 沿着延迟-吞吐量帕累托前沿滑动。

# 分离式预填充

分离式预填充，有时也称预填充-解码（PD）分离，是在不同节点上执行 LLM 推理的预填充与解码阶段的过程。预填充发生在请求首次被处理时，对所有 token 一次性计算前向传播，从而为该请求「预填充」KV 缓存。这是计算密集型操作，因为所有 token 并行通过前向传播。随后 token 一次一个地被生成或「解码」，每个解码步从 HBM 加载 KV 缓存。这是内存密集型过程，因为不断增长的 KV 缓存被持续加载。

传统单节点推理中，引擎在同一批 GPU 上交错执行预填充与解码。新来的预填充请求会阻塞在途的解码批次，既增加首 token 时间也增加 token 间延迟。分块预填充（chunked prefill）通过把长预填充拆成小块来缓解，但根本性的资源争用依然存在。分离式预填充则彻底消除了这个问题！

![](https://substack-post-media.s3.amazonaws.com/public/images/0bc87a96-aa31-4b37-99c6-603c98f332f3_1318x733.png)
*来源：DistServe*

分离还使两个阶段可以独立扩展与优化。有了独立节点，每个阶段可以各自调优：不同的并行策略、不同的批量大小、不同的内存分配比例。预填充与解码节点的比例也可以匹配工作负载的输入-输出长度比。例如，预填充主导的工作负载（长输入短输出，如摘要、RAG、大上下文窗口的智能体编程）分配更多预填充实例。解码主导的工作负载（短输入长输出，如思维链推理、长文生成）分配更多解码实例。缓存命中率高的工作负载也倾向于更多解码，因为来自共享系统提示或多轮对话历史的可复用 KV 缓存条目可以完全跳过预填充。

分离的关键代价是 KV 缓存传输。预填充完成后，该请求的完整 KV 缓存必须在第一个解码 token 生成之前从预填充节点传到解码节点。对 DeepSeek R1 这种 61 层、FP8 KV 缓存的模型，一次 8192-token 预填充产生约 500MB 需要跨网络传输的 KV 数据，直接计入 TTFT。传输通过 RDMA（通常是 RoCE 或 InfiniBand）进行，采用零拷贝的 GPU 到 GPU 数据搬运，无需 CPU 参与。NIXL（NVIDIA Inference Transfer Library）等库把数据搬运层抽象为统一的异步 API，并为 UCX、GPUDirect Storage 等传输方式提供可插拔后端。这将推理引擎与任何特定传输协议解耦，并支持跨异构硬件的分离部署——预填充与解码实例可以跨越不同的设备类型或互连。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b56d901-ef89-43c9-8d11-c18062f1b7b9_1165x1165.png)
*来源：Github*

# 用 Wide EP + 分离式服务优化推理

Wide EP 与分离式预填充是两种常常搭配使用以达到帕累托最优性能的独立技术。在本节中，我们通过 InferenceX 的真实结果建立直觉：在不同交互性水平下，哪种并行策略、wide EP 与分离式预填充的组合是合适的。

先了解单节点配置下哪些并行策略落在帕累托前沿的哪些位置会很有帮助。以单台 8-GPU B200 节点上跑 TRT-LLM 的 DeepSeek R1 FP4 8k/1k 为例。沿着前沿移动时，最优策略随之改变，主要驱动因素是批量大小及其对专家激活密度的影响。

在最高交互性水平（batch 1-16）下，纯 TP 优于任何含 EP 的配置。小批量时，每步只有一小部分专家激活。用 EP 的话，这些激活在 GPU 间分布不均：batch 4 时，256 个专家只有 32 个被触发，任意一颗 GPU 在某一层收到零个路由 token 的概率大约是百分之十几。TP 通过把每个专家分片到所有 GPU 上避免了这一点，因此无论路由器选了哪些专家，全部 8 颗 GPU 都均等参与每次专家计算。我们在剖析 DeepSeek R1 时收集了专家激活率与批量大小的数据，证实 batch 16 及以下时每层专家激活非常低。

![](https://substack-post-media.s3.amazonaws.com/public/images/5ca10b5a-f80e-45b4-8d22-e3134d30b54d_2232x1446.png)
*来源：SemiAnalysis*

移到略低的交互性区间，批量仍然足够小，专家权重仍用 TP 而非 EP 切分。交叉点大约在 batch 32，此时每层约 50-60% 的专家激活。在这个密度下，EP 的负载不均衡变得可以容忍，其 token 路由开销低于 TP 所需的逐专家 all-reduce。这一区间的配置使用 TEP：注意力用张量并行（所有 GPU 协作完成每次注意力计算），MoE 层用专家并行（专家分配到特定 GPU，all-to-all 路由）。在前沿最高吞吐、最低交互性的区域，批量很大（128+），配置转向纯 DEP：注意力权重作为独立数据并行 rank 在全部 GPU 上完整复制，专家经 EP 分布，以每 token 延迟为代价把批量容量最大化。(128+) 且注意力权重在全部 DP rank 上完整复制，最大化吞吐量。

![](https://substack-post-media.s3.amazonaws.com/public/images/d13280a5-ddc2-4610-84bb-bf470301cc8e_2086x1233.png)
*来源：SemiAnalysis InferenceX*

扩展到 wide EP 加分离式预填充时，我们观察到相同的总体模式。预填充与解码采用各自的并行策略和节点数量，两者都针对工作负载和目标交互性水平调优。以前沿高吞吐、低交互性端的 8k/1k 工作负载（预填充重）为例。预填充是瓶颈，因为每个请求需要对 8192 个输入 token 做一次前向传播，计算代价高昂。这一区间的配置方案给预填充分配比解码更多的节点（4P1D、7P2D、4P3D），以维持高预填充吞吐。这些预填充节点跑 DEP 配置，把注意力权重复制到独立的数据并行 rank 上，从而可以同时处理多个长上下文预填充。解码节点更少，但按与单节点相同的原理以大批量跑宽 DEP。

在前沿的低交互性端，在途并发请求较少，因此单个预填充实例就能跟上涌入的需求。然而每个请求仍需要 1024 个解码步，而在高交互性下这些步必须快。这一区间的配置方案转向比预填充更多的解码节点（1P3D、1P4D），每个解码实例以小批量跑 TEP。注意力上的张量并行把计算拆到实例内全部 GPU 上，最小化每步延迟；专家并行则在 EP 负载均衡已足够的适中批量下处理 MoE 路由。多个小批量解码实例（而非更少的大批量实例）把每 token 延迟保持在低位，同时仍提供足够的并发服务容量。

# 深入解析 DeepSeek R1 单节点结果

在 DeepSeek R1 FP8 1k1k 上，我们看到 MI355X 在单节点场景中与对手 B200 旗鼓相当，尽管在 FP4 多节点场景中被碾压。MI355X（SGLang）在较低交互性水平下的吞吐性能甚至击败 B200（SGLang）。而且从 perf/TCO 角度看，MI355X（SGLang）在多数情况下胜过 B200（TRT 和 SGLang）。

遗憾的是，如今已是 2026 年，大多数前沿实验室和推理提供商既不跑 FP8，也不跑单节点推理。

这一结果说明，AMD 的芯片很出色，只要软件跟得上，完全可以与 NVIDIA 极具竞争力地一较高下。速度才是护城河。

![](https://substack-post-media.s3.amazonaws.com/public/images/a4e8da6f-c4ee-4d39-96ae-9143459d3ea9_2102x1236.png)
*来源：SemiAnalysis InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/7ce2b96f-840d-411b-9c6c-2f821219fba5_2130x1444.png)
*来源：SemiAnalysis InferenceMAX*

也因此，我们看到 MI355X 在 FP4 上性能远落后于 B200：

![](https://substack-post-media.s3.amazonaws.com/public/images/dbc1dd2c-e15c-45b7-acf7-508d38ad1913_2406x1430.png)
*来源：SemiAnalysis InferenceX*

比较 H200（SGLang）与 MI325X（SGLang）之间的 DeepSeek R1 FP8 性能，自去年 10 月我们首次发布 InferenceXv1 以来没有太大变化。MI325X 数据采集于 2026 年 2 月 12 日，使用 SGLang 0.5.8；B200 数据采集于 2026 年 1 月 23 日，使用 SGLang 0.5.7。

我们注意到一点：MI325X 的交互性区间比 H200 小得多，H200 覆盖 30-90 tok/sec/user，而 MI325X 只有 13-35 tok/sec/user。这对希望在更宽交互性范围内服务用户的提供商来说是个问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/f3ba43db-8f65-4b28-a4a2-66282670449f_2117x1236.png)
*来源：SemiAnalysis InferenceX*

# GPT-OSS 120B 单节点

MI300X、MI325X、H200 和 H100 聚在吞吐量-交互性图的左下角，表明它们的权衡大体相似，NVIDIA 总体略占优势。再上一个台阶是 MI355X，在给定交互性水平下，其每 GPU token 吞吐量相对第一梯队高出约 2 倍多。在 MI355X 内部，ATOM 把曲线在低交互性端推向更高吞吐量，说明它把峰值吞吐的优先级放在了每用户响应速度之上。

再往上一个梯队是 NVIDIA 的 B200 和 GB200，它们在前沿各处都胜过 MI355X。虽然 B200 和 GB200 共用同样的 Blackwell 计算裸片，但 GB200 实现了更高的吞吐量-交互性曲线，因为该平台与服务栈在大规模下减少了非计算瓶颈（互连/拓扑、CPU-GPU 耦合、运行时调度），转化为有效的 scale-out 扩展和更低的每 token 开销。

![](https://substack-post-media.s3.amazonaws.com/public/images/478b3a9a-c57d-4766-bde1-c3ee1fef550a_2068x1178.png)
*来源：SemiAnalysis InferenceX*

如果把成本纳入考量，MI355X 变得更有竞争力：在高吞吐量下击败 B200。不过，最便宜选择的桂冠仍归 GB200。

![](https://substack-post-media.s3.amazonaws.com/public/images/028672d5-2c24-4dbd-974d-9f50d163df27_1796x1182.png)
*来源：SemiAnalysis InferenceX*

再回到 B200 与 GB200 NVL72 的对比，NVL72 的影响显而易见。我们在本文前文讨论过 GB200 NVL72 更大的 72-GPU scale-up world size 相对 B200 的 8-GPU scale-up world size 的影响。在约 100 tok/s/user 交互性区间，每 GPU 输出 token 吞吐量翻了一倍多，显示了 NVL72 更大 scale-up 域的影响。

![](https://substack-post-media.s3.amazonaws.com/public/images/0186cfbc-1b42-46ae-ae1a-0d7791afcb20_2081x1306.png)
*来源：SemiAnalysis InferenceX*

# InferenceX 代码库核心更新

我们对 InferenceX 代码库做了一些核心架构调整，让基准测试更容易理解和复现。此外，我们全面拥抱 AI 使用，以最大化生产力、提升开发速度。

# InferenceXv1 以来的核心变化

自 v1 以来我们的一项主要变化是执行全量扫描（sweep）的节奏。以前我们是在小丑式瞎忙（jestermaxing），每晚对每个配置做一次全量扫描。但随着我们加入更多芯片、分离式预填充、wide EP 和其他功能，我们意识到每晚都跑实在太耗时、太浪费。何况这根本没有必要——基准测试只需要在配置方案变更或新软件版本发布时重跑。

现在，我们基于代码库根目录 [changelog](https://github.com/InferenceMAX/InferenceMAX/blob/main/perf-changelog.yaml) 的新增条目来触发扫描。当开发者对某个配置做了影响性能的改动时，他们在 changelog 中加入一条记录，列出受影响的配置以及改动的简述。所有配置都在一个[主配置 YAML 文件](https://github.com/InferenceMAX/InferenceMAX/blob/main/.github/configs/nvidia-master.yaml)中定义，它是每个待扫描数据点的有状态表示，包含 ISL/OSL、EP、TP、DP、MTP 等核心设置。当包含 changelog 新增的 PR 被合并后，一个工作流会解析引用的配置键，从主配置中拉取对应的扫描定义，并把它们分发为独立的 GitHub Actions 任务。这些任务收集完整扫描的全部数据点，并把结果作为 artifacts 上传。

下面是 InferenceX 如何启动任务的高层示意图。

![](https://substack-post-media.s3.amazonaws.com/public/images/74936db5-88cb-418e-932a-e7a8693a6857_2904x2845.png)

# Klaud Cold（Claude Code）AI 用量

InferenceX v1 发布后不久，我们意识到在 InferenceX 开发中没有更充分地使用 AI，浪费了多少开发吞吐量。于是我们撸起袖子，决定拥抱 Claude Code，开始一个 token 一个 token 地吸收智能，以至于我们目前的消费已达到 $6,000/天 的运行速率。如果你想为「年化吸收 300 万美元 Claude 智能」这一 KPI 做贡献，[请在此申请加入使命。](https://app.dover.com/apply/semianalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1)我们的启蒙之旅始于发现 GitHub Copilot agent 是免费的——起初我们简直不敢相信这个功能居然不收钱！很快我们就发现 Copilot 糟糕透顶，也明白了 GitHub 为什么白送。你们恐怕得*倒贴钱*我们才肯继续用它。

Claude Code 自发布以来我们就一直在本地使用。但最近，我们把 Claude Code 集成进了 InferenceX 开发：既用于审查 PR 这类常规任务，也赋予了它在集群上执行扫描的能力。借助我们搭建的工作流，Claude 可以手动发起运行、查看结果并迭代。这让我们能通过 GitHub app 随时随地轻松部署快速修复。

另一个很酷的用例是用 Claude 为新的 vLLM/SGLang 镜像寻找配置方案。新镜像发布时，配置方案有时需要更新才能达到最优性能（新的环境变量、修改的引擎参数等）。有了 Claude Code 集成，我们只需开一个 issue，让 Claude 在镜像 changelog 的所有提交中搜索需要加入配置方案的变更。效果相当好，虽然并不*完美*，但常常能给出一个不错的起点。

# GitHub Actions

本着开源精神，所有运行都在 GitHub Actions 上进行，因此基准结果可验证、透明且可复现。然而，GitHub 的宕机最近一直是实现我们目标的持续障碍。[我们最近见到的独角兽比其他任何动物都多](https://github.com/503.html)（GitHub 的 503 报错页是一只独角兽）！不过，也许我们该出门接接地气了。

Microsoft/GitHub 自己也意识到了这一点，已经停止在状态页上更新综合正常运行时间数字，如今只剩下一个 9：过去 90 天为 97.36%。选择无视的话，问题并不会自己消失……

![](https://substack-post-media.s3.amazonaws.com/public/images/3b921859-49f3-4b0b-b02e-dd0bf7a36e2e_3000x975.png)
*来源：Outages 项目*
![](https://substack-post-media.s3.amazonaws.com/public/images/dd7aad58-ba30-4364-9565-980ae6464534_3000x975.png)
*来源：Outages 项目*

总而言之，GitHub Actions 也就那样。它给开发者提供的是一种平庸得令人痛苦的体验。它当然不是为在数百颗 GPU 的集群上启动数千个任务而生的。尽管如此，自发布以来我们与一些 GitHub Actions 工程师紧密合作，以更好地满足 InferenceX 的需求，我们可以放心地说，与他们合作是一件愉快的事。此外，我们的一个直接诉求是：点击某个工作流运行时对任务做懒加载。虽然花了些时间，[但他们最终实现了这个功能。](http://github.blog/changelog/2025-12-22-improved-performance-for-github-actions-workflows-page/)

# InferenceX 的未来

自 2025 年 10 月初首次发布以来，我们一直努力持续改进 InferenceX。发布后，我们花了一些时间重构代码库以提升可扩展性，如今新模型和推理技术可以以「即插即用」的方式加入。这些改动让我们无缝集成了 H100、H200、B200、B300、GB200、GB300 和 MI355X 的 PD-disagg 基准。我们还在默认基准管线中加入了精度评估，确保对所有配置的模型性能保持可见。

尽管发布以来我们做了许多改进，但要实现「提供尽可能贴近真实世界的推理基准」这一北极星目标，仍有大量工作要做。为实现这一目标，我们计划在真实数据集上做基准、新增智能体编程性能基准、纳入更多 SOTA 推理优化、测试更多模型等等。

# 迁移到真实多轮对话与智能体编程数据集

目前，InferenceX 使用完全随机的 token 作为基准输入。然后我们在 [ISL*0.8, ISL] 的分布内均匀变化 ISL/OSL，OSL 同理。由于数据是随机的，我们在所有基准中禁用前缀缓存，因为在完全随机数据上前缀缓存命中率的期望值是 0%。此外，所有随机数据都是单轮的，即每段对话只包含一个提示和一个回复。这提供了不错的基线帕累托前沿，但并不是一个模拟真实世界生产推理工作负载的实用基准设置。

近期内，我们将用 [allenai/WildChat-4.8M](https://huggingface.co/datasets/allenai/WildChat-4.8M) 这类数据集创建一个基础多轮基准，该数据集采集了真实用户的多轮对话。除了在所有场景启用前缀缓存外，我们还将启用 KV 缓存 CPU 卸载，因为这是我们在生产工作负载中实际看到的做法。这将更准确地评估各芯片的强项与弱项。例如，MI355X 有 288GB HBM3e，而 B200 是 192GB。因此我们预期 MI355X 在高并发多轮场景中表现更好，因为可以分配给 KV 缓存的内存更多。另一方面，在 GPU KV 缓存吃紧、数据块被卸载到 CPU 的场景中，我们预期 GB 系列胜出，因为这些芯片有 900GB/s 的双向 CPU-GPU 带宽，而分别搭载 PCIe 5.0 和 6.0 的 HGX 只有 128GB/s / 256GB/s。此外，目前我们看到 AMD 的 CPU 卸载软件很差，在相同场景中可能拖累性能。

关键在于：真实世界的多轮数据集会测试更多 SOTA 推理引擎特性，并能在所有芯片上捕获更细致、更鲁棒的性能数据。

随着 Claude Code、Codex 和 Kimi 的崛起，对智能体编程场景做性能基准测试变得越来越重要。与上面类似，这些场景是多轮的，但还包含超长上下文对话以及工具使用。未来几个月，我们计划创建一套基准，最准确地捕获开源模型在这些智能体编程场景中跨所有芯片的性能。

# 加入 TPU、Trainium 与更多模型

目前，我们持续对 DeepSeek R1 和 GPT OSS 120B（此前还有 Llama 3.1 70B）做基准测试。为跟上最新的模型架构，我们计划在未来几个月加入 DeepSeek V3.2（带 DSA）、首日（Day 0）支持 DeepSeek V4、Kimi K2.5、Qwen3、GLM5 等等。我们最终还会加入多模态模型，并使用 EPD 和 CFD（由 TogetherAI 发明）优化。

除新模型外，我们也在积极推进 TPU 和 Trainium 的加入。

# 总拥有成本（NVL72、Blackwell、Blackwell Ultra、MI355、Hopper、MI325、MI300）

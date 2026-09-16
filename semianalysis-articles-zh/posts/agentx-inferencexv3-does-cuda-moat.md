---
title: "AgentX - InferenceXv3：CUDA 护城河在智能体推理中还守得住吗？"
title_en: "AgentX - InferenceXv3: Does CUDA Moat Hold up in Agentic Inferencing?"
subtitle: "300 万美元数据集开源、100 万+ 上下文长度、多轮对话、子智能体 95%+ KV 缓存命中率、GB300 NVL72、MI355、B200"
date: 2026-08-24
source: https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat
crawled: 2026-09-15
authors: ["Cam Quilici", "Bryan Shan", "Alec Ibarra", "Daniel Nishball", "Zane Fong", "Kimbo Chen", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AgentX - InferenceXv3：CUDA 护城河在智能体推理中还守得住吗？

> 原文：[AgentX - InferenceXv3: Does CUDA Moat Hold up in Agentic Inferencing?](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**300 万美元数据集开源、100 万+ 上下文长度、多轮对话、子智能体 95%+ KV 缓存命中率、GB300 NVL72、MI355、B200**

自 2025 年 11 月的 [Claude Code 拐点](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point)以来，长上下文、多轮的智能体工作负载快速增长，如今已主导生产推理的流量。2026 年 4 月，OpenAI 的企业级智能体支出超过了 ChatGPT 支出。

智能体工作流已经明确接过了接力棒。**今天，我们发布 AgentX 1.0——全球首个完全开源、多轮、100 万上下文的智能体编码推理基准，以 Apache 2.0 许可证发布。[完整仪表盘请见此处。](https://inferencex.semianalysis.com/)**

![](https://substack-post-media.s3.amazonaws.com/public/images/864512bf-1feb-445d-a03a-bbf9f4f1b791_1928x1234.png)
*来源：SemiAnalysis*

过去，大多数性能测评基于固定序列长度的预填充和解码工作负载，但这并不是一种准确衡量工作负载的方式。真实场景是多轮、长上下文、高预填充复用，并伴随子智能体突发、KV 缓存卸载和大量工具调用。因此，我们的目标是为业界建立衡量 AI 软硬件性能的正确方法。

[为构建这一数据集我们已花费超过 300 万美元。今天，我们将一切开源。](https://inferencex.semianalysis.com/)InferenceXv3 实现了 AgentX——在既有“固定序列长度”场景（8k1k、1k1k、1k8k）之外新增的一个真实场景。它用智能体编码流量取代了此前 8k 输入、1k 输出 token 的单轮流量，从而改进了基准场景。

完整测试矩阵在约 2MW 持续运行的算力上运行，覆盖超过 1000 颗芯片、广泛的 SKU 范围，包括 MI355X、GB300 NVL72、GB200 NVL72、B300、B200、MI325、MI300X、H200 和 RTX Pro 服务器。Rubin 将于本月晚些时候到位，TPU 和 MI455X UALoE72 则在今年晚些时候到位。[如果您认为我们的免费开源工作有价值，请给我们点个 star。](https://github.com/SemiAnalysisAI/InferenceX)

很高兴看到 NVIDIA 和 AMD 在智能体工作负载上都有出色的表现。NVIDIA 在很多前沿模型上表现非常出色，而 AMD 在部分前沿模型的特定对比中也表现不错。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a065d23-de1d-4e2f-a3ae-7af724409c9d_1350x653.png)
*来源：SemiAnalysis GitHub*

AgentX 最初几个月产出的最有价值的东西并不是最初的结果，而是这个基准已经在业界产生的巨大影响。针对 vLLM、SGLang、TensorRT-LLM、ATOM、AITER、Dynamo、LMCache 和 Mooncake 上真实生产智能体工作负载的优化，已有**超过 70 个上游 PR** 将 AgentX 用作北极星基准代理。这些优化改进大多可以迁移到生产流量。我们将在文章后面对每项优化做深度解析。

![](https://substack-post-media.s3.amazonaws.com/public/images/193e605e-579b-4ed2-9637-5bfdbee5cf71_1286x1515.png)
*来源：SemiAnalysis*

开源是 InferenceX 的核心原则，因此我们开放的栈比大多数把这个词挂在嘴边的人更多。这包括开放前端、通过易于使用的 REST API 提供的公共数据库（**多个一线 AI 实验室的容量规划团队已经在使用**）、公开的 GitHub Actions CI 溯源、[日志](https://inferencex.semianalysis.com/inference/agentic/440193?i_seq=agentic-traces&i_xmode=interactivity&view=logs)，以及每个数据点上的精度验证。关键在于，我们的基准配置主要在上游镜像上跟踪 [recipes.vllm.ai](http://recipes.vllm.ai) 和 [SGLang cookbook](https://docs.sglang.io/cookbook/intro)，这样我们衡量的是真实客户正在体验的性能，而不是为跑分特化的镜像。

三到四周后，我们将发布一篇 AgentX 更新文章，涵盖智能体工作负载的进一步优化，以及 AMD 和 Nvidia 更新后的性能结果。需要理解的是，智能体工作负载的形态在快速变化。InferenceX 将继续快速行动，对相关的工作负载进行基准测试。

InferenceX 百分之百坚持开源——如果没有 OSS 伙伴的贡献和支持，这一切都不可能实现。我们感谢以下为 AgentX 1.0 发布做出巨大贡献的人：

- **Inferact/vLLM**：Roger Wang、Yifan Qiao、Simon Mo、Jeff Ma 以及许多其他人
- **RedHat/llm-d**：Michael Goin、Robert Shaw、Tyler Michael Smith
- **RadixArk/SGLang**：Baizhou Zhang、Yuwei An、Mingyi Lu 以及许多其他人
- **LMCache/TensorMesh**：Samuel Shen
- **Weka**：Callan Fox、Val Bercovici
- **MoonCake 维护者**：Teng Ma、Xu Wenjie、Ke Yang
- **AMD**：Thomas Wang、HaiShaw、Andy Luo、Seungrok Jung、Chun Fang、Parth Panchal、Bill He、Theresa Shan、Hongxia、Fangzhou、Gilbert Lei、Yanfei Wang、Duyi Wang、Peng Sun、Lingpeng Jin、Simon Danielsson、Xiaohu Guo、Haichen Zhang、Chang Liu、Doug Lehr、Poovaiah Palangappa，以及 AMD 上海研发中心的许多其他人
- **Nvidia**：Xin Li、Anthony Casagrande、Kedar Potdar、Ankur Singh、Ishan Dhanani、Nick Comly、Nvidia 上海 TensorRT-LLM 团队、Pete Sarabia，以及许多其他人
- **Anthropic 员工，他们迅速修复了多个 bug，才使实现 AgentX 成为可能**
- **GitHub**：Austen Stone 帮助提升了 AgentX 所用 GitHub Actions 的可靠性
- 以及许多其他人

[此外，我们感谢所有支持我们开源 InferenceX 计划的机构，包括 Meta、Microsoft、Oracle、OpenAI、MiniMax、Moonshot Kimi、阿里巴巴 Qwen 和智谱 GLM。](https://inferencex.semianalysis.com/quotes)

![](https://substack-post-media.s3.amazonaws.com/public/images/e97525a9-216a-4624-91c6-373ee7a3850e_1123x437.png)
*来源：InferenceX*

# 智能体工作负载简要概述

从高层次看，智能体工作负载有四个特征要素：

1. **多轮**：与聊天机器人场景中的寥寥数次相比，一次会话包含大量用户/助手交互（数十甚至数百次）。多轮、长上下文、高预填充复用，并伴随子智能体突发和大量工具调用。
2. **长上下文**：系统提示词、工具定义和大量的轮次使上下文快速累积。
3. **高前缀复用**：由于对话是线性推进的（通常是第 n-1 轮的输出被拼接到第 n 轮），大部分上下文可以直接由 KV 缓存提供服务而无须重算（这取决于可用于存储 KV 张量的存储容量）。随着 n 增大，缓存输入相对于未缓存输入的比例通常趋于 1。
4. **子智能体突发**：一次会话会启动多个具有全新上下文的短生命周期子智能体，从而造成突发式的 KV 缓存访问模式。

![](https://substack-post-media.s3.amazonaws.com/public/images/72b64a02-8a1f-4a19-929c-85c0ed4803cd_2048x909.png)
*来源：DeepSeek、SemiAnalysis*

考虑到上述特征，对这些工作负载做基准测试与既有的固定序列长度基准有着根本区别。也就是说，智能体推理本质上是一个*系统问题*。由于前缀复用极高，KV 张量必须跨节点/rank 高效传输（NIXL、MORI-IO、Mooncake）。此外，不同的对话应根据相应前缀所在的位置路由到不同的节点/rank，以最大化缓存命中率（LLM-d、Dynamo、vLLM/SGLang 路由器）。长上下文对话会对 KV 缓存的 HBM 容量造成压力，必须将 KV 张量卸载到不同层级的内存（DRAM、SSD），且这一过程必须高效完成（Mooncake Store、LMCache、vLLM Simple Offloading、SGLang HiCache）。

这与固定序列长度、单轮的工作负载形成鲜明对比——后者与前缀复用无关，推理性能很大程度上反映的是芯片/内核的基础性能。这并不是说 InferenceX 上大量的固定序列长度数据不重要。事实上，剥离智能体服务的复杂性，可以清楚地看到底层推理性能优化的进展。它也为 AgentX 的结果提供了重要的基线。

为了尽可能让 AgentX 工作负载贴近真实，我们收集了初始语料——[393 条 SemiAnalysis 内部匿名化的 Claude Code 轨迹](https://huggingface.co/datasets/semianalysisai/cc-traces-weka-062126)——用于回放。为了在匿名化内容的同时保留原始的前缀复用模式，我们采用了与 [Qwen-Bailian 数据集](https://github.com/alibaba-edu/qwen-bailian-usagetraces-anon)类似的方法，后者是最早的生产轨迹语料之一。然后我们使用 [AIPerf](https://github.com/ai-dynamo/aiperf) 按照原始的请求时间表，在不同并发客户端级别下重建这些轨迹。我们与 Anthropic 合作上线了两个 Claude Code 特性，使 AgentX 数据集成为可能。我们感谢 Anthropic 员工的帮助。

1. <https://github.com/anthropics/claude-code/issues/49207>
2. <https://github.com/anthropics/claude-code/issues/66761>

这段关于智能体工作负载的简短介绍应能让读者获得足够的背景来理解下一节的结果。在后面的章节中，我们将对方法论、回放工具和数据集做更深入的技术解析。

# 智能体编码推理性能

在看推理编码性能时，OpenAI、Anthropic、xAI 和其他前沿实验室关注三件事：每美元性能与交互性（TPOT）的权衡、TTFT（首 token 时间），以及整体端到端任务完成情况。每兆瓦性能也很重要，因为地面数据中心的电力是关键约束（金钱是一种社会建构，实验室们似乎有无限的资金，但在当今时代，电力在物理上很难获得）。[我们的数据中心模型按季度估算了电力供需的累积。](https://semianalysis.com/datacenter-industry-model/)

在本节中，我们重点介绍前沿模型上智能体性能的一些整体主题。我们强烈建议读者以此为指导[自行探究结果](https://inferencex.semianalysis.com/)。**所有数据都是开源的，社区有机会就真实世界推理性能的现状得出自己的结论。**

## DeepSeek V4 Pro 0813

DeepSeek V4 Pro 0813 是中国极受欢迎的前沿开放权重模型，拥有约 1.6 万亿参数、490 亿激活参数。

截至 8 月 21 日，下图展示了所有提交中每个 SKU 的最佳性能，按总拥有成本（TCO）归一化。

所有 DeepSeek v4 运行中*全部*请求的 ISL/OSL 分布如下：ISL p50=88k、p90=272k、p95=404k、p99=675k；OSL p50=413、p90=2.2k、p95=3.7k、p99=8.6k。

![](https://substack-post-media.s3.amazonaws.com/public/images/d8337140-b620-476a-abd3-59d6cc447d30_2048x1256.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/b5aee8b4-d11a-48d8-823c-1ca53412e689_2048x1253.png)
*来源：InferenceX*

总体而言，**必须同时考虑每用户每秒 token 数**（TPS，也称交互性）和 TTFT，**因为两者常常此消彼长**。例如，在上图中，一些 SKU 在不错的交互性下实现了很高的吞吐量，但 TTFT 严重劣化。什么算是“可接受”的 p90 TTFT 因应用而异。对于大多数服务智能体工作负载的生产系统，p90 TTFT 一般在 200-5,000ms 之间。超过 5-10 秒就逼近“在线推理”的边界了。曲线的超高吞吐量区段仍有实际用途——延迟不重要且希望系统利用率达到峰值的场景（批处理、*超*长时运行的智能体等）。

在单节点性能方面，MI355X 的开源性能（vLLM）落后于厂商专属的 ATOM（AMD 相当于 TensorRT LLM 的产品）。我们认为 AMD 用 ATOM 快速推进前沿值得赞赏，但我们鼓励他们把向 vLLM 上游合并这些改进的优先级提得更高。

![](https://substack-post-media.s3.amazonaws.com/public/images/d96697d9-bf24-4093-a7db-16d27a52aa08_2048x1200.png)
*来源：InferenceX*

过去六个月，AMD 的分布式推理（DI）团队在 8k1k 场景上取得了巨大进展。但要使 DI 成为真实工作负载的可行方案，该团队还有一段路要走。就每 GPU 吞吐量 vs. 交互性而言，我们观察到 1xDEP8+1xDEP8 分离式配置只在高吞吐场景中实现轻微的性能提升，而在低延迟场景中实际表现更差。

更糟的是，中高交互性配置下吞吐量的任何提升，都被 p90 TTFT 的显著飙升所掩盖。原因之一是在并发 64 以上使用了 SGLang 的 --enable-prefill-delayer 参数，[它推迟预填充准入，使 DP rank 能组成更满的批次](https://github.com/sgl-project/sglang/blob/v0.5.17/python/sglang/srt/server_args.py#L3180-L3194)（最多可推迟 30 次前向传播）。此外，这些数据点还将分块预填充大小从 8,192 提高到 65,536。

![](https://substack-post-media.s3.amazonaws.com/public/images/81475383-510e-4823-9373-751b8a3722e3_2048x1202.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/6254047b-173b-4b1b-9f43-2057eb720b05_2048x1200.png)
*来源：InferenceX*

在端到端延迟上，ATOM MI355X 胜过 B200 vLLM（但胜不过 B300 或 B200 SGLang）。问题在于，由于大量功能缺失，无论中国还是西方的大多数 AI 实验室都不愿在生产中使用 ATOM，只有阿里巴巴旗下一个很小的广告业务部门例外。阿里内部的 Qwen 主力 LLM 组织并未在生产中使用 ATOM。

![](https://substack-post-media.s3.amazonaws.com/public/images/e8d915c0-c962-4277-b62c-a1b08b8e7179_1924x1262.png)
*来源：InferenceX*

2026 年 8 月 21 日之前，AMD MI355X 上实力强劲的 SGLang 开发团队在端到端（e2e）性能的每美元性能上与 B200 vLLM 持平。

![](https://substack-post-media.s3.amazonaws.com/public/images/360a051c-6117-4860-a704-b50198f01521_1978x1246.png)
*来源：InferenceX*

然而，B300 vLLM 和 B200 SGLang 仍然胜过 AMD 的 MI355X。

![](https://substack-post-media.s3.amazonaws.com/public/images/9ec4708c-148e-42ee-a7c5-3bf4d9cbdfaa_1938x1246.png)
*来源：InferenceX*

2026 年 8 月 21 日之后，由于 Inferact 和 Nvidia 在 vLLM 上的优化，Nvidia B200 的每美元性能超过了 MI355X。这是一场势均力敌的竞赛，我们期待未来几周的性能优化。我们很快将发布 AgentX 更新文章。

[AMD 已列出他们的 DeepSeek v4 vLLM 优化项，其中包含许多可用于提升性能的激动人心的工作](https://github.com/vllm-project/vllm/issues/52911)。

![](https://substack-post-media.s3.amazonaws.com/public/images/9302da60-5bc1-46e1-9392-74e912b5c200_2024x1236.png)
*来源：SemiAnalysis*

现在来看 Nvidia。其最具竞争力的方案是 GB300 Dynamo TRTLLM 和 GB200 Dynamo vLLM。两种配置都依赖 PD 分离（disagg）来在合理的交互性下实现高吞吐。此外，GB300 配置采用宽 EP（DEP32）解码实例，以在前沿中部实现更高吞吐。

注意，与 TTFT 维度相比，2xDEP8+1xDEP12 的 GB200 数据点在 TPS 维度上明显更接近 3xDEP8+1xDEP16 的 GB300 数据点。再说一次，TTFT 通常对工作负载的“突发性”更敏感。由于 GB300 数据点实现了高得多的整体并发，它会产生更多子智能体流量，因而有更多冷预填充。我们可以在该数据点的 TTFT 图表中看到这一点：

![](https://substack-post-media.s3.amazonaws.com/public/images/96f9c9f9-eb86-4f87-8332-c85f23040836_2048x916.png)
*来源：InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/f79e53f5-c8ff-4ed0-a8a3-c05b9e0b4bab_2048x1191.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/512c6225-5816-493e-839d-e4f539e5b1c4_2048x1215.png)
*来源：InferenceX*

按 TCO 归一化后，B300 vLLM 与 B200 vLLM 的综合性能相当接近。主要区别在于 B300 凭借比 B200 高 50% 的 HBM 容量，可以“挤”出额外的吞吐量。

![](https://substack-post-media.s3.amazonaws.com/public/images/939b9197-321d-4869-ba13-f0b800343b7b_2048x1300.png)
*来源：InferenceX*

我们可以用 AgentX 新增的服务器指标可视化来进一步展示这一差异。

在 384 路并发智能体轨迹的负载下，B300 vLLM DEP8 通过 vLLM simple offloading 配备 3TB DRAM，实现了 91% 的 HBM 缓存命中率，另有 1.36% 的 DRAM 缓存命中率。这是因为该配置下 **HBM KV 缓存工作集大小**约为 43M token，而负载在任一时刻的在途 token 数都很少超过这一数值。

![](https://substack-post-media.s3.amazonaws.com/public/images/b7ff2d61-bdab-4c2f-96a0-ec5a52469489_2048x884.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/f86888c4-c1a7-47b0-a580-d1a74876cb9c_2048x898.png)
*来源：InferenceX*

在 B200 并发 196（其他所有参数保持不变）下，我们看到 HBM 缓存命中率仅为 73%，并更依赖 DRAM，卸载缓存命中率接近 20%。我们观察到 HBM KV 缓存工作集大小为 22M token，约为 B300 的一半。

DRAM KV 卸载通常实现为写穿（write-through）缓存，即写入 HBM 缓存的每个前缀也会写入 DRAM 缓存。因此，当可用于卸载的 DRAM 容量显著大于（1.5-3 倍）HBM KV 缓存容量时，它才最有效。

![](https://substack-post-media.s3.amazonaws.com/public/images/61956823-2928-44ec-b00c-8bb5581b8a13_2048x892.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/70a7a7c7-7918-459c-a4e0-f7fc1edca816_2048x887.png)
*来源：InferenceX*

H200 SGLang FP8 能在低并发下服务 DeepSeek v4，从每美元性能的角度看甚至可与 B200/MI355X SGLang 竞争。然而，由于 HBM 不足，它无法在高吞吐场景中与更新的 SKU 竞争。

![](https://substack-post-media.s3.amazonaws.com/public/images/770b205f-12a1-4d34-81a7-fb235742d005_2048x1305.png)
*来源：InferenceX*

此外，随着用户数量增加，更高并发下对 DRAM KV 卸载的依赖会导致不合理的延迟。

![](https://substack-post-media.s3.amazonaws.com/public/images/91dfd9ca-d13d-43e9-a57e-3be0fcc4a5cf_2048x1315.png)
*来源：InferenceX*

总体而言，与主要竞争对手 B200 和 B300 相比，MI355X 表现相当不错。在曲线的低吞吐/低延迟部分，性能最具可比性，那里只部署了张量并行和较为基础的内核。AMD 需要优化 MI355X 上的 DEP 内核，才能在高吞吐场景中更具竞争力，尤其是考虑到其 HBM 是 B200 的 1.5 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/ba6532b3-aa46-4477-be84-8979b1cce35d_2048x1297.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/29cfd340-d61b-46c4-8d87-e081d937b80c_2048x1303.png)
*来源：InferenceX*

## Kimi K3：2.8 万亿参数

Kimi K3 是中国的另一个前沿开放权重模型，总参数量达 2.8 万亿。就参数量而言，它与 Claude 的 Mythos/Fable5 模型架构处于同一量级。我们将其作为开放权重的代理模型架构。Kimi K3 模型太大，单个 B200 服务器根本装不下，必须使用宽 EP/宽 TP 或流水线并行才能容纳全部权重。在 vLLM 上，投机解码/DSPark 直到最近才能与流水线并行组合使用，因此 B200 在 Kimi K3 上的表现很糟糕，被 MI355X 碾压，因为 B200 无法在流水线并行下使用投机解码。

MI355X vLLM 在第 0 天就能开箱即用地跑短上下文单轮工作负载，但对于长上下文多轮工作负载，MI355X 的 AITER 和 Triton 内核在第一周就出了大乱子，上游 vLLM 在真实工作负载上对 MI355X 完全不可用。

![](https://substack-post-media.s3.amazonaws.com/public/images/a1440922-e1ea-4a74-ab62-f1263ae31ca0_2048x1473.png)
*来源：SemiAnalysis InferenceX*

Hopper 难以服务 Kimi K3 的 AgentX 工作负载，因为 Kimi 是一个庞大的模型，而且 vLLM 维护者/NVIDIA 一直没把精力放在为 Kimi K3 优化 Hopper 上。Hopper（SM90）需要为 K3 定制调优的内核，以及 TP32/EP32 调优形状，才能在高交互性下服务。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce2b58fc-b7b7-46c2-ae05-baa14419d233_2048x1459.png)
*来源：SemiAnalysis InferenceX*

我们认为 AMD 用 ATOM 快速推进 K3 性能值得称赞。但我们鼓励 AMD 进一步优先把这些改进上游到 vLLM。ATOM 目前是 AMD 表现最好的引擎，但对于使用上游开源服务栈的客户来说，vLLM 仍是更有意义的比较对象。

![](https://substack-post-media.s3.amazonaws.com/public/images/80eb810f-a9ea-4f01-a41b-e19e3409ce74_2048x1459.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/73ded698-c86e-411b-8e7c-f9bb125487b7_2048x1459.png)
*来源：SemiAnalysis InferenceX*

在曲线的 40 到 60 秒端到端延迟区间，MI355X ATOM 的每美元性能甚至胜过 GB300 NVL72 vLLM。

![](https://substack-post-media.s3.amazonaws.com/public/images/27a3f80e-7959-4651-90eb-f498989908a3_1934x1284.png)
*来源：SemiAnalysis InferenceX*

## MiniMax M3

在 MiniMax M3 432B 上，Nvidia 彻底碾压所有竞争对手。AMD 的软件性能在 MiniMax 上很糟糕，尤其是在高上下文长度下，原因是 AMD 工程管理层的激励机制只鼓励针对短上下文单轮工作负载调优，忽视长上下文多轮工作负载。

![](https://substack-post-media.s3.amazonaws.com/public/images/c5396c3d-1823-4818-83de-d89cd8242451_2048x1286.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/5179bd8e-c147-46c8-aeb4-b347049b28a7_2048x1303.png)
*来源：SemiAnalysis InferenceX*

B300 TRT-LLM TP2 拿下了 M3 的王座。DP 注意力的数据点较少，因为它在 M3 上并非最优——KV 缓存局部性会成为路由约束。这一点在后文有进一步解释。对于 GB200，在并发 40 时，TP4/EP4/DPA 的吞吐量只有纯 TP4 的 0.60 倍，而 p90 TTFT 却是 3 倍以上。在并发 32 时，缓存命中率为 28.8%，而理论值为 96.0%。每个 DP rank 私有占用缓存的四分之一；一个 300k token 的会话若重新落到错误的 rank 上，就要全部重算。M3 前沿上没有出现任何带 EP 的解码配置，可能是因为并发还不够高，不足以平衡所有专家的负载。

在 MiniMax M3 的 TCO 归一化吞吐量上，B200/B300 也完全胜过它们的机柜级对手。在 AgentX 上，机柜级优势并不那么明显，因为 Dynamo 路由器可能成为瓶颈——它的工作量随活跃前缀的数量和长度而增长。关于这一点的优化，以及几个带来两位数百分比吞吐提升的修复，将在文章后面讨论。此外，宽 EP、宽 DCP 和宽 TP 都没有经过良好调优的内核。由于 GB200/300 的 TCO 更高，在没有宽 EP/宽 DCP 的情况下，其单位 TCO 性能表现更差。

话虽如此，我们也期待 Nvidia 在其机柜级方案上针对该 SKU 的进一步优化。我们一定会在后续文章中重点介绍。

尽管 P90 ISL 达到 317k，目前没有任何提交使用上下文并行。由于只有 4 个 KV 头，即使在 TP8 下 DCP 也被限制在 2，而 MSA 索引器需要自己的上下文并行处理（已有一个 vLLM PR 打开），详见“上下文并行”一节对此话题的更多讨论。

![](https://substack-post-media.s3.amazonaws.com/public/images/aec34e63-34fd-4c42-87a1-97e5c14661ed_2048x1302.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/2b40624a-223c-44db-a403-0be563b2af82_2048x1298.png)
*来源：SemiAnalysis InferenceX*

Nvidia 所有帕累托最优点在并发 20 以上都包含 KV 卸载，而 AMD 的帕累托最优点没有一个使用到 DRAM 的 KV 卸载。在其他模型上，AMD 也比 Nvidia 更少使用 KV 卸载。原因在于 AMD vLLM 上用于 CPU KV 缓存卸载的 GPU 到 CPU 传输效率极低。hipMemcpyBatchAsync API 直到 ROCm 7.14 才出现。没有 hipMemcpyBatchAsync，vLLM 原生的 Simple CPUOffloading 只能做串行化的 CPU 到 GPU Memcpy，而无法把它们合并成更大的消息。

还值得一提的是，在吞吐量 vs. p90 交互性方面，vLLM 性能与 TRT-LLM 非常接近。此外，在吞吐量 vs. p90 TTFT 方面，vLLM 表现更好。

![](https://substack-post-media.s3.amazonaws.com/public/images/68f7ad68-3886-4980-9b01-390582728e47_2048x1292.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/729199d9-66c0-42b5-b1b8-f228503c1585_2048x1289.png)
*来源：SemiAnalysis InferenceX*

## Qwen3.5 397B

Qwen3.5 397B 每隔几层就使用 GatedDeltaNet 代替普通注意力。GatedDeltaNet 由 MIT/Nvidia Research 发明，理论上的状态存储需求是常数，而不是普通注意力的线性存储需求。这意味着与等效的稠密注意力模型相比，它的存储需求更低。与 Nemotron 灾难那样的端到端模型训练研究不同，Nvidia Research 擅长 GDN 和 LatentMoE 这类基础研究，它们已被用于前沿模型。

注意该模型的原生最大上下文长度为 262k token，因此我们使用[截断数据集](https://inferencex.semianalysis.com/agentx/cc-traces-weka-062126-256k)。这模拟了在较小模型上的工作负载——最大上下文长度会被频繁触及并伴随多次压缩（compaction），这才是用户实际使用该模型的方式。

在 SGLang 对 SGLang 的较量中，Qwen3.5 397B 是 NVIDIA 的坚固阵地，在 90 tok/s/user 下性能领先超过 20 倍。目前在 Qwen3.5 SGLang 上，AMD 的竞争为零。

![](https://substack-post-media.s3.amazonaws.com/public/images/c92da639-dcff-4e39-b9b5-49742677e93c_2048x1289.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/519a7cd0-ac51-4a5c-9c45-ba7c41f6d058_2048x1300.png)
*来源：SemiAnalysis InferenceX*

我们再次观察到 Nvidia 以牺牲 TTFT 为代价过度优化交互性，TRT-LLM 尤其如此。在上图中，与 TRT-LLM 相比，Nvidia 所有 SGLang 提交的 p90 TTFT 都低得多。

与 H100 相比，在 Qwen3.5 上，B300 FP4 的每美元性能好 12 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc2cf6c7-aa58-4a76-a0a2-ee0457d9243c_2048x1298.png)
*来源：SemiAnalysis InferenceX*

## GLM 5.3

GLM 5.3 在 GLM5.2 744B 的基础上进行了额外的后训练（post training）。这是一个前沿级模型。

在开源 SGLang 性能方面，这又是一个 Nvidia 在真实智能体推理性能上击败 AMD 的模型。在 150 tok/s/user 的 p90 交互性下，Nvidia 的成本效率最高好 5 倍。以 AMD 软件的现状，在 150 tok/s/user 下，Nvidia 的性能优势如此之大，以至于即使竞争对手的芯片硬件免费赠送（但提供商当然仍要支付数据中心托管、电力和其他运营成本），使用 Nvidia 的每 token 成本仍然更低。

我们期待几周后即将发布的 AgentX 更新文章中 AMD 的性能优化，其中还将包含一些非常激动人心的结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/f85bdb45-792c-4330-9745-674b38b03425_2048x1289.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/4a21d140-b588-4b33-941d-7c8090ac42b5_2048x1286.png)
*来源：SemiAnalysis InferenceX*

看 ATOM 的话，在 p90 E2E 归一化交互性的部分区间内，AMD 的每美元性能优于 GB300 NVL72 SGLang，甚至优于 TRTLLM。AMD 团队在这些结果上干得漂亮。再次强调，我们期待 AMD 把这些优化移植到 SGLang。我们也期待 NVIDIA 在未来几周内快速优化 GB300 NVL72。

![](https://substack-post-media.s3.amazonaws.com/public/images/9337ed5b-a320-49f7-b31b-cc4b5751e0ff_2048x1290.png)
*来源：SemiAnalysis InferenceX*

我们借此介绍一个实验性指标，称为 **E2E 归一化交互性（E2E Normalized Interactivity）**。从高层次看，该指标旨在综合 TTFT 和 TPS，评估用户感受到的响应速度。它定义为 OSL/E2EL。代入 E2EL 等于 TTFT 加上 OSL 乘 TPOT（实际上只解码 OSL - 1 个 token）这一事实，我们得到下面的等式。

这实际上就是交互性（1/TPOT 部分）加上一个与 TTFT 成正比的额外惩罚项。

![](https://substack-post-media.s3.amazonaws.com/public/images/9e472a49-d228-4d8d-876a-6bc0d59f9d97_746x594.png)
*来源：SemiAnalysis*

请注意，该指标是实验性的，并不完美。例如，它对高 TTFT 惩罚很重，也无法捕捉某些优化（如 PD 分离）的全部细节。AgentX v1.0 的所有提交分别针对常规交互性和 TTFT 进行优化。我们将继续研究能够反映现代智能体推理全部细节的新的北极星指标。

# AgentX 行业影响——智能体工作负载优化

AgentX 最初几个月最有影响力的成果不是产出开源数据集，而是 AgentX 伙伴们以它为北极星、针对真实世界智能体工作负载做优化而创造的 **50 多个上游 PR 带来的行业影响**。AgentX 的真实智能体流量不仅测试原始的预填充和解码内核，还测试端到端 token 生成的全过程——从 KV 缓存生命周期、混合注意力缓存的正确性、CPU KV 卸载、传输进度、路由亲和性，到增量 tokenization、请求序列化和调度器簿记。这些环节对每一个生产级智能体部署都很重要。

这只是我们持续使命的延续——帮助生态系统加速改进，实现软件的光速进步。一个很好的例子是 SemiAnalysis 与 AMD 软件开发团队多年的合作，我们持续提供反馈和意见，帮助其软件开发原则现代化。这不仅带来了许多加速 AMD 进展的变革，也对让 AMD 开源在智能体工作负载上接近一流水平起到了关键作用。

## 分布式推理生态简介

如前所述，智能体推理本质上是一个系统级问题，而不只是芯片/内核级问题。此外，当大型*分布式系统*处理数十万个智能体请求时，请求调度和 KV 缓存管理变得绝非小事，并对性能有实实在在的影响。例如，子智能体会带来突发式的 KV 缓存模式，若未妥善优化，就会错误地逐出主智能体的缓存。

下图从高层次展示了这个栈。顶层是路由器（有时称为“前端”），将请求路由到不同的 worker。例如，当服务器运行数据并行注意力时，每个 DP rank 都有独立的 KV 缓存。为了不让任何一个 KV 缓存发生颠簸，请求会按不同策略路由，例如[一致性哈希](https://github.com/vllm-project/router/blob/main/src/policies/consistent_hash.rs)，同一会话/子智能体的请求按其唯一 ID 路由。

![](https://substack-post-media.s3.amazonaws.com/public/images/58ac4a3a-cc05-4ff6-9d1e-b28dc0d0f760_1814x2048.png)
*来源：SemiAnalysis*

对大多数路由策略来说，各路由器实现没有本质差异。有的是独立组件，如 [vLLM router](https://github.com/vllm-project/router) 和 [llm-d router](https://github.com/llm-d/llm-d-router)；有的集成在引擎中，如 [SGLang model gateway](https://github.com/sgl-project/sglang/tree/main/sgl-model-gateway) 和 [ATOM Mesh](https://github.com/ROCm/ATOM/tree/main/atom/mesh)。

请求被路由后，由 vLLM、SGLang 等推理引擎的调度器处理。引擎负责实际执行推理并通过 API 返回结果。此外，每个引擎都有接口将引擎内部的 KV 缓存连接到外部 KV 缓存管理器。这就形成了一个“可插拔”的生态，不同的 KV 缓存管理器可以与多种推理引擎集成。

当前 AgentX 结果中使用的一个简单部署，是在同一节点上让 [Mooncake](https://pypi.org/project/mooncake-transfer-engine/) 与 vLLM 一起运行。每个 vLLM worker 内嵌一个 Mooncake Store 客户端，并将一部分主机 DRAM 贡献给外部 KV 缓存池。vLLM 通过 MooncakeStoreConnector 接口连接该池，将可复用的 KV 块加载到 GPU 内存，并将新计算的块保存回主机内存。Mooncake Store 管理外部缓存（包括放置和逐出），而 Mooncake Transfer Engine 执行 GPU 与 CPU 内存之间的实际数据搬运。

不同的 KV 缓存管理器可以使用不同的传输引擎在内存层级之间或机器之间物理搬运字节，例如在预填充和解码 worker 之间。例如 Mooncake Store 使用 [Mooncake Transfer Engine](https://github.com/kvcache-ai/Mooncake/tree/main/mooncake-transfer-engine) 在 GPU 内存、主机 DRAM 和远程节点之间搬运 KV 块。

一个部署可以用 Mooncake Store 将可复用的 KV 块卸载到主机 DRAM，同时用 NIXL 将请求专属的 KV 直接从预填充 GPU 传输到解码 GPU。Mooncake TE 负责 Mooncake Store 路径的搬运，而 NIXL 在支持的地方使用 UCX 和 GPUDirect RDMA 处理独立的预填充-解码路径。因此，多条 KV 管理与传输路径可以在同一推理引擎内共存。

该生态由许多独立组件构成，包括推理引擎、路由器、KV 缓存管理器、数据传输库和集群控制器。Nvidia Dynamo、llm-d 和 AMD Infera 等平台将这些组件的选定组合“打包”成完整的软件发行版。它们发布兼容的容器镜像、连接器、部署清单和编排逻辑，使这些组件可以作为一个系统部署和运维。最终产物通常是多个协同容器的集合，而不是单一的单体服务（例如：Dynamo、llm-d 和 Infera 通常部署在 k8s 上，协调大型分布式系统）。

![](https://substack-post-media.s3.amazonaws.com/public/images/af5c4776-221b-43b4-b2fd-d46e46f1ab38_1772x960.png)
*来源：RedHat / llm-d*

## 上下文并行

长上下文能让一些并行技术发挥作用，而固定 8k 提示词无法充分锻炼这些技术，因为在 8k 下没什么可分的，TTFT 本来就短。此外，TP 和 DP 注意力这类并行策略在更长的上下文长度下并非最优：TP 会导致完整 KV 被复制到每个 rank 上；DP 注意力虽然共享 KV，但在长上下文上会陷入停顿，因为长上下文工作负载还会导致可能的上下文长度方差更大。

![](https://substack-post-media.s3.amazonaws.com/public/images/1e2801db-53ff-4029-8b55-01b3c1a7037d_1632x1140.png)
*来源：SemiAnalysis*

上下文并行是一种把查询 token 拆分到多个 GPU 的并行技术。它有两种形式：PCP（prefill context parallelism，预填充上下文并行）和 DCP（decode context parallelism，解码上下文并行）。在 PCP 中，每个 rank 预填充自己的查询块（KV 以环传方式传递），由于预填充往往受计算限制，这能并行化 FLOPs，带来更快的预填充，且不会让某个 rank 出现巨型提示词的预填充尖峰。对于 DCP，每个 rank 扫描自己的 KV 分片，然后按 flash-decode 风格合并部分注意力结果。由于解码受内存带宽限制，并行的 KV 读取可以带来更高的 tok/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/a9544ced-f418-44e0-8910-0cbc63fa26ec_2048x768.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/512c3a96-2ab4-452f-be6a-4fa60900575c_2048x651.png)
*来源：SemiAnalysis*

这一并行技术部分由 Nvidia Research 发明。Nvidia Research 擅长这类基础研究，而在端到端训练研究方面，他们那糟糕的 Nemotron3 Ultra 模型正在让美国蒙羞——它目前甚至被小小的 Qwen3.8 27B 模型大幅击败。DCP/PCP 构成了 CUDA 护城河的一部分，因为 AMD 的 DCP/PCP 实现尚未优化。在 [vLLM 支持矩阵](https://docs.vllm.ai/en/latest/design/attention_backends/#standard-attention-mha-mqa-gqa-backends)中，AMD 的每一个后端都不支持。

接下来几节提到的部分改动正是围绕 DCP/PCP。

## vLLM 智能体优化

我们与来自 Inferact、Red Hat、NVIDIA 和 AMD 的 vLLM 维护者并肩工作，以 AgentX 的真实回放器为北极星，修复成果落到上游，其中大多数优化可以高度迁移到生产。举几个例子：

vLLM 改进了混合注意力的前缀缓存，使短生命周期的滑动窗口分配不会逐出有用的长上下文检查点。[选择性保留](https://github.com/vllm-project/vllm/pull/43447)保住了稀疏回放边界，在十四路并发、上下文高达一百万 token 的情况下报告前缀缓存命中率超过 95%。同样的可达性策略[被应用到 Mooncake](https://github.com/vllm-project/vllm/pull/44774)，并且[移除了不可达的滑动窗口查找](https://github.com/vllm-project/vllm/pull/45444)。更早的后续工作还[停止卸载永远无法复用的滑动窗口块](https://github.com/vllm-project/vllm/pull/42258)，并[将投机解码的前瞻块保留在留存前缀中](https://github.com/vllm-project/vllm/pull/44082)。

![](https://substack-post-media.s3.amazonaws.com/public/images/df1a505d-b8c3-45f9-b03c-a8798fba54c0_2048x632.png)
*来源：SemiAnalysis 与面向智能体工作负载的 vLLM GitHub PR*

高并发智能体的工作负载需要卸载。得益于前述 AgentX 的影响，vLLM 上已有多条工作流致力于让混合模型也能做 CPU KV 卸载，而不只限于统一的全注意力模型。这一区别很关键：统一模型每个 token 只有一种 KV 布局，连接器用单一块几何即可描述要保存什么；而混合模型同时携带多个缓存组，每个组的形状和生命周期都不同，假定单一统一布局的连接器无法表达某个块属于哪个组。因此，卸载在最需要长会话的模型上反而不可用。通用的 [SimpleCPU 连接器](https://github.com/vllm-project/vllm/pull/37160)最先落地，随后[在 ROCm 上启用](https://github.com/vllm-project/vllm/pull/40549)，然后[扩展到 DeepSeek-V4 混合注意力](https://github.com/vllm-project/vllm/pull/42296)——与前缀放不下 HBM 后重算相比，输出吞吐量提高 81.7%，平均端到端延迟降低 46.6%。

Mooncake 也获得了[等效的混合内存分配支持](https://github.com/vllm-project/vllm/pull/42828)。同样的布局问题在分离式服务中再次出现：一个[待合并改动](https://github.com/vllm-project/vllm/pull/51052)在 1P1D 预填充/解码分离下，通过 MoRI-IO 将 Kimi-K3 的 conv+ssm 循环状态随注意力 KV 一起传输；没有它，解码侧会从未初始化的循环状态启动。循环状态槽位复用现有的 remote-block-ids 通道，因此分离式路由器无需针对模型的改动，并且该路径已在 MI355X 上端到端验证，每条腿 TP8 跨节点 RDMA，两条腿均使用 DSpark 投机解码。

在剖析真实工作负载时，vLLM 维护者发现卸载期间成本转移到了存储（store）路径——写入太多、太频繁。三个新修复现已解决这一问题：
当相同传输已在进行时会[跳过存储](https://github.com/vllm-project/vllm/pull/41289)，共享同一前缀的并发会话只需付出一次代价，而不是各自一次。存储[只覆盖新生成的 KV 范围](https://github.com/vllm-project/vllm/pull/46412)，因此扩展历史的会话只写入增量，而不是每轮重写整个前缀。最后，存储不再[依赖相同块是否仍在 HBM 中](https://github.com/vllm-project/vllm/pull/46906)，因此当逐出发生在已调度工作之下时，已调度的工作不会被丢弃。

加载（load）路径单独调优，因为查找发生在每一次调度决策上，而不仅仅在数据真正移动时。让[调度器路径中的查找异步化](https://github.com/vllm-project/vllm/pull/45659)使连接器脱离 step 的关键路径，这样一步在准入工作前不再等待 CPU 侧的缓存查询。[紧凑的零拷贝查找键](https://github.com/vllm-project/vllm/pull/45969)、[并行接收侧加载](https://github.com/vllm-project/vllm/pull/45971)和[预构建的 Mooncake 键字符串](https://github.com/vllm-project/vllm/pull/46188)随后消除了残余的 CPU 和传输开销。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c2cfea4-a217-47ad-934b-dbd226bb248c_2048x837.png)
*来源：SemiAnalysis 与面向智能体工作负载的 vLLM GitHub PR*

长生命周期的混合状态还迫使一批固定形状请求很少触及的正确性与簿记修复。vLLM [按混合缓存组发出缓存事件](https://github.com/vllm-project/vllm/pull/44103)、[正确跨步分布式上下文存储](https://github.com/vllm-project/vllm/pull/45371)，并[在分布式上下文和预填充下正确计算查找前缀](https://github.com/vllm-project/vllm/pull/46855)。相关的[上下文并行簿记改动](https://github.com/vllm-project/vllm/pull/45340)使缓存所有权与分片 token 范围对齐。投机解码状态现在[跨合并的 Mooncake 组传播](https://github.com/vllm-project/vllm/pull/49069)并[通过 SimpleCPU 协调器传播](https://github.com/vllm-project/vllm/pull/49071)，防止多轮复用的缓存悄悄丢失 EAGLE 状态。

再看 vLLM 中智能体工作负载优化的 ROCm 一侧，工作在缓存层之下继续，那里剩余的成本是按层而不是按请求计的。一旦前缀得以存活并按时到达，剩下的就是解码步本身，而一个每会话运行数千次的解码步，会为每一次可避免的拷贝和每一个不匹配的内核付出代价。

三个开放中的改动攻向这一层：

- 一项 Kimi-K3 改动[将 KDA 解码结果直接写入层输出缓冲区](https://github.com/vllm-project/vllm/pull/51183)，为每个 KDA 层消除一次设备拷贝；单看节省很小，但它会在每个被解码 token 的每一层上重复兑现。

- 第二项改动[选择 AITER 稀疏 MLA 解码内核](https://github.com/vllm-project/vllm/pull/51714)取代通用路径，报告 AgentX 输出吞吐量提高 5.22%，inter-token 延迟显著降低。
- 第三项很好地说明了测量形状有多重要。一个配套改动[将全图注意力投影路由到调优的 AITER GEMM](https://github.com/vllm-project/vllm/pull/51713)，在低并发的固定序列上取得 2.3% 的提升。这说明一个内核级改动可以在均匀形状上显示干净的收益，然后在智能体轨迹上被该轨迹引入的缓存与调度波动所淹没。一个[待合并改动](https://github.com/vllm-project/vllm/pull/52882)把这种形状敏感性本身变成派发判据：它在 gfx950 上用 AITER/原生混合路径取代 DeepSeek V4 C4A 选择器的 ROCm top-k 瓶颈，短中等上下文走 AITER，长上下文走图安全的调优原生回退。它报告端到端选择器加速 1.21x 到 1.76x，在 84 种形状的矩阵上解码内核几何平均加速 1.2x 到 2.9x。

## SGLang 智能体优化

AgentX 团队一直与来自 RadixArk、Meta、Nvidia 和 AMD 的 SGLang 维护者紧密合作，推动 SGLang 上智能体工作负载的优化，带来了生产推理性能的巨大提升。下面更深入地讨论这些优化。

我们先从分配器角度解释 SGLang 的滑动窗口工作如何解决与 vLLM 保留策略相同的冲突。窗口页和前缀页来自同一个池，而窗口是更贪婪的消费者：它不断翻新，前缀则静止不动，于是在压力下，临时分配挤走了持久分配。

三项设计改进从不同角度攻克这一问题。其一[在页面离开窗口时主动释放](https://github.com/sgl-project/sglang/pull/26907)，而不是等逐出压力去找它们，让死掉的窗口状态不再为它已无法使用的页面竞争。其二[将计算锁限制在单个窗口](https://github.com/sgl-project/sglang/pull/27210)，限定一个在途请求一次能钉住多少池容量。其三[移除活得比其用处更久的过期全量 KV 条目](https://github.com/sgl-project/sglang/pull/29369)。

不过，主动释放有一个分叉形状的盲区：从共享前缀分叉出的请求仍可能持有可复用的全量 KV，而分叉点处的窗口状态已被释放，于是整个前缀只因缺少便宜的那一半而被全部重算。[开放中的工作](https://github.com/sgl-project/sglang/pull/34565)在这些分叉点保留 SWA 状态，让分叉继承窗口而不是重建它。

除此之外，[ROCm 环形缓存修复](https://github.com/sgl-project/sglang/pull/30339)是正确性而非容量改动：环形缓冲区天然会复用槽位，复用一个旧内容仍被引用的槽位会产出错误结果而不是慢结果。这些在单个 8k 提示词上完全看不出来——窗口从不会追上前缀，池也从不会被争抢。而在多轮混合会话中，正是这些改动决定了昂贵的全注意力历史在下一轮是否还在。

HiCache 是 SGLang 的一流内置卸载机制。它面对与 vLLM 连接器相同的混合问题，并用一种不对称性解决：[卸载全注意力缓存，回程时重建短的滑动窗口尾部](https://github.com/sgl-project/sglang/pull/29417)。只有昂贵的那一半值得跨总线搬运，便宜的那一半重建比取回更快。在 AMD 上，[分段写回](https://github.com/sgl-project/sglang/pull/28534)让搬运发生时不阻塞引擎。循环状态是剩下的缺口，因为它不能像窗口尾部那样从相邻 token 重建；[FlashInfer GDN 检查点](https://github.com/sgl-project/sglang/pull/29735)让它第一次能参与前缀复用，并在 92.4% 缓存命中率下把吞吐量从 47,771 提高到 53,004 tok/s/GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/078ad449-7657-4468-9ff9-3480a7999d89_2048x720.png)
*来源：SemiAnalysis*

另外两项改动解决变长流量对内核管线的影响。AgentX 真实会话往往以持续变化的上下文长度到达，生产流量中也观察到类似模式。一个对长度特化的朴素运行时几乎会为它见到的每个请求编译一个新内核。SGLang 维护者通过把[上下文长度作为运行时标量传递](https://github.com/sgl-project/sglang/pull/30255)解决了这个问题，将其折叠进一次编译，使 AgentX 并发 384 的输出吞吐量提升 26.75%、平均 TTFT 改善 36.25%——靠的是消除编译，而不是把任何东西算得更快。

![](https://substack-post-media.s3.amazonaws.com/public/images/3a807d67-383b-4aa9-93af-e8f3a68313f4_855x634.png)
*来源：GitHub*

本着同样的精神，[移除每步一次的设备到主机序列长度同步](https://github.com/sgl-project/sglang/pull/30365)消除了解码气泡——这个气泡的存在只是因为主机想知道一个设备早已知道的长度。

![](https://substack-post-media.s3.amazonaws.com/public/images/b29e003e-db43-45d4-93be-bac0be04d869_1209x646.png)
*来源：GitHub*

变长在注意力内核内部同样咬人。在 GB300 上，混合上下文的解码批要交“尾部税”：一次匹配剖析把 9.8 ms 解码步增量的 8.4 ms 归因于注意力，最长的请求拖长了持久内核的共享 wave。[开放中的工作](https://github.com/sgl-project/sglang/pull/34888)将 TRTLLM MHA 解码批拆分为按 KV 长度排序的组，让短请求不再等待最长的请求。

再往上一层，解码在调度器处同样可能被饿死，而不是在内核里。在 DP 注意力下，每个 rank 一边本地调度注意力工作，一边加入同一个 MoE 集合通信，于是一个不断被喂分块预填充续请求的 rank 总是赢得“预填充优先”的决策，而同伴 rank 上正在运行的批次只能干等——这在 AgentX 运行中观察到过。[预填充后的可配置解码间隔](https://github.com/sgl-project/sglang/pull/35017)强制在预填充之间插入解码轮次；在 AgentX DSv4 Pro 上，输出吞吐量提升 141%，p99 inter-token 延迟下降 97.3%，代价是中位 TTFT 从 36.5 秒升到 59 秒——用首 token 等待换取流的平滑。

![](https://substack-post-media.s3.amazonaws.com/public/images/47ce130f-13f2-4732-8431-17e26184b8c3_1846x806.png)
*来源：SemiAnalysis*

当一个请求不携带可复用历史（比如子智能体的启动）时，任何 worker 都行，负载均衡是唯一值得问的问题。而当请求携带 MB 级的缓存前缀时，把它发给一个不持有该前缀的空闲 worker 才是昂贵的选择，路由器需要知道状态已经在哪里。SGLang 增加了 [DP 缓存亲和](https://github.com/sgl-project/sglang/pull/26091)，让会话粘在持有其缓存的 rank 上。在这个 PR 中，同时实现了 [DP 感知的预填充与解码路由](https://github.com/sgl-project/sglang/pull/26245)，使分离式部署的两半一致地做出该决策，还有[以缓存均衡作为路由信号](https://github.com/sgl-project/sglang/pull/26293)，避免亲和退化为单个热 worker。路由器只能根据被告知的信息行动，因此混合缓存事件也变得[radix-cache 感知](https://github.com/sgl-project/sglang/pull/26387)和[滑动窗口感知](https://github.com/sgl-project/sglang/pull/26579)。

投机解码受到特别关注，因为 MTP 给每个请求增加了第二块更小的状态，它必须在主缓存经历的一切中存活下来。SGLang [修复了分离式服务中的草稿窗口传输](https://github.com/sgl-project/sglang/pull/30461)，使该状态完整跨越预填充到解码的边界；[为高并发在线解码增加了重叠调度](https://github.com/sgl-project/sglang/pull/30497)；[移除了一次空操作的 EAGLE 重归一化](https://github.com/sgl-project/sglang/pull/31294)；并[避免了 EAGLE 预填充期间的主机同步](https://github.com/sgl-project/sglang/pull/33662)。开放中的[资源租约调度工作](https://github.com/sgl-project/sglang/pull/32042)和[数据并行图元数据修复](https://github.com/sgl-project/sglang/pull/32196)延续同一努力：当请求可能被撤回和恢复而不是简单跑完时，让重叠变得安全。

对于预填充与解码拓扑异构的智能体工作负载，需要前缀感知的暂存（staging），而这正是前缀缓存与分离式架构相互作用不佳的地方。当两侧分片方式不一致时，KV 无法作为一条连续流拷贝过去；它必须按传输网格拆分，并在解码侧期望的偏移处重新组装。前缀命中让这件事更难而不是更简单，因为预填充 worker 现在只发送未缓存的剩余部分，而解码侧仍然期望一个完整、位置正确的缓存。[暂存缓冲区中的 radix-cache 支持](https://github.com/sgl-project/sglang/pull/30545)在该网格上拆分缓存发送，并散射到正确的解码偏移处。

![](https://substack-post-media.s3.amazonaws.com/public/images/88c2d49d-2612-4334-90c2-8a76ab55fd60_1418x1004.png)
*来源：SemiAnalysis*

然而，此前存在正确性问题。一个 127,500 token 共享前缀的测试从 128 根针中 2 根正确提升到 128 根全对，说明缓存此前一直悄悄落在错误的位置——吞吐量基准会把这种情况评为一个快速、自信但错误的答案。AgentX 对比还让每用户中位输出吞吐量提高 9.6%，而每 GPU 总吞吐量几乎不变。传输本身也带着死重：解码侧的 PREBUILT 批从不进入模型前向，但每个被传输的提示词仍被展平并拷贝进一个 CUDA 输入张量，而第一个解码步反正会从中继元数据重建它。[去掉这个无用的提示词传输](https://github.com/sgl-project/sglang/pull/35070)是最大的单项收益，在 AgentX GB300 上带来 +18.0% 每用户输出吞吐量和 +12.7% 每 GPU 解码吞吐量。一个[后续改动](https://github.com/sgl-project/sglang/pull/35071)把预填充 DP-rank 引导查询移出解码调度器的关键路径，重叠了此前在结果消费时同步支付的 HTTP 往返，在同一部署上再带来 +1.36% 每用户输出吞吐量。开放中的工作沿同一条缝继续：[UMBP 中的多池 DeepSeek-V4 支持](https://github.com/sgl-project/sglang/pull/30762)、[经 MoRI 携带的统一 KV HiSparse 状态](https://github.com/sgl-project/sglang/pull/32368)，以及[解码在无可见内容终止时保留预填充拥有的 token](https://github.com/sgl-project/sglang/pull/34216)。HiSparse 工作应被理解为长上下文的容量与正确性使能器，而不是高并发下的吞吐收益——目前还不是。

![](https://substack-post-media.s3.amazonaws.com/public/images/ed24f1b9-b591-4674-bc94-06394962d03f_2048x544.png)
*来源：SemiAnalysis*

## TensorRT-LLM 智能体优化

接下来解释 TensorRT-LLM 最近的几项优化。首先看 TRTLLM 针对重复聊天轮次的前端优化——这是一种只因工作负载是多轮才存在的成本。对话的每一轮都会重发全部历史加上一点点新内容，朴素实现会把全部内容重新做 tokenization。tokenization 按千字节算很便宜，但当同样 100,000 个 token 每轮都被重新 tokenize 时就是灾难。

显而易见的修复——只 tokenize 新的后缀——以一种容易忽视的方式是错的，因为字节对编码不是位置无关的。token 可以跨接缝合并，所以在边界处切开文本、拼接两段 token 序列，可能得到与整体 tokenize 不同的序列，从而悄悄偏离前缀缓存所基于的序列。

TRTLLM 实现了[边界感知的增量 tokenization](https://github.com/NVIDIA/TensorRT-LLM/pull/17462)：找到渲染文本的公共前缀，回退一个完整 token，使任何跨接缝的合并都被重算，然后只从那里开始 tokenize 变化的后缀。在 Qwen3.5 AgentX 轨迹上，它在全部 1,087 次转换上与全量 tokenization 一致——正确性主张经过实测而非假设——并把平均处理时间从 185.1 ms 降到 11.3 ms。

![](https://substack-post-media.s3.amazonaws.com/public/images/30a51cf2-e628-4c20-a4a5-5978234ca713_952x541.png)
*来源：GitHub*

固定的 8k1k 请求没有可复用的先前渲染轮次，所以这些在那里都不会出现。相关地，[聊天模板渲染被移入输入处理池](https://github.com/NVIDIA/TensorRT-LLM/pull/16231)，长模板不再把主请求循环串行地堵在后面。

![](https://substack-post-media.s3.amazonaws.com/public/images/00b459b8-9c4c-4c8c-8659-07e14bf5699f_2048x784.png)
*来源：SemiAnalysis*

MiniMax-M3 工作聚焦分离式 KV 搬运，其故障在于粒度。当预填充与解码在头布局上不一致时，一个逻辑请求的 KV 不再是少数几个大的连续区域，而变成数千个小的跨步片段，每个片段都成为自己的传输描述符。搬运的字节数没变；爆炸的是每描述符开销，而且恰恰在最要紧的长提示词上以最恶劣的方式爆炸！[修正的多池映射与分块 NIXL 弹跳路径](https://github.com/NVIDIA/TensorRT-LLM/pull/17518)通过一个有界的可复用 arena 合并这些片段，用一次额外暂存拷贝换取数量级更少的描述符。其 AgentX 诊断将请求关键 KV p99 在并发 5 下从 26.74 秒降到 125 ms，在并发 40 下从 10.15 秒降到 288 ms。

![](https://substack-post-media.s3.amazonaws.com/public/images/52bd05ab-914f-4dc5-9f16-a0ea1b495383_959x501.png)
*来源：GitHub*

[非阻塞上下文传输轮询](https://github.com/NVIDIA/TensorRT-LLM/pull/17428)通过在调度停顿时也收割已完成的传输来保护同一路径。这打破了一个反馈循环：已完成的 KV 块被钉住并阻止新请求准入。停顿本身也有一个[可移除的原因](https://github.com/NVIDIA/TensorRT-LLM/pull/16734)：避免 DeepSeek-V4 上下文稀疏注意力元数据中的隐式设备标量同步，消除了每步 18 次各强制一次 cudaStreamSynchronize 的 4 字节设备读取——发生在 GB300 分离式上下文 worker 上。该修复把主机侧计数作为普通 Python int 贯穿传递，使执行器线程不再在一步的大部分时间里持有 GIL，而 KV 传输和响应线程在后面干等。

TensorRT-LLM 还把不规则的长上下文工作移到更高效的执行路径上。[MiniMax-M3 的上下文图生产者](https://github.com/NVIDIA/TensorRT-LLM/pull/17473)捕获稳定的稀疏生产者，而让依赖请求的注意力保持 eager，其 AgentX 测试中每用户输出吞吐量提高 12.58%。一个开放中的[原生 KV 事件生产改动](https://github.com/NVIDIA/TensorRT-LLM/pull/16876)减少了 KV 感知路由路径上的分配和转换工作。

AgentX 还暴露了只有在规模和时长足够时才会出现的内核选择与调度器生命周期故障。其中两个关于选哪个内核。MiniMax-M3 [在 MXFP8 自动调优中加入 CuTeDSL 候选](https://github.com/NVIDIA/TensorRT-LLM/pull/17316)，拓宽候选集，在低并发聚合点上让每 GPU 输出吞吐量提升约 7% 到 10%。反方向上，TensorRT-LLM [禁用了损坏的 split-K MoE tactic](https://github.com/NVIDIA/TensorRT-LLM/pull/17105)，此前它在七次 AgentX 运行中让五次崩溃，之后七次匹配运行零崩溃。一个快而错的 tactic 比一个只是慢的更糟，除非把它从池中移除，否则自动调优器会热情地选中它。选择不是内核出错的唯一方式：MiniMax-M3 面向短查询的遗留稀疏注意力路径可能给 SM100 内核一个非连续、按头优先的块索引视图，而后者把它当作连续读取，选错 KV 页并产出错误或非有限的输出。[遵守块索引步长](https://github.com/NVIDIA/TensorRT-LLM/pull/17285)（q_len ≤ 32）在不物化张量、不增加内核的情况下修复了索引，之后 GB300 上五对匹配的完整 AgentX 运行零服务错误、无非有限标记。

![](https://substack-post-media.s3.amazonaws.com/public/images/f48290ac-3361-4b0c-a085-ff84dd3dce51_2048x1347.png)
*来源：TRT Github*

另外两个是生命周期 bug，是长时运行而非大规模运行的典型故障。[序列槽位余量与一致的按槽索引缓冲区大小](https://github.com/NVIDIA/TensorRT-LLM/pull/16279)处理完成中的请求与新准入请求同时需要一个槽位的瞬态重叠——这个窗口，稳定的到达与离开流会不断命中，而固定批永远碰不到。后来的[注意力数据并行哑请求修复](https://github.com/NVIDIA/TensorRT-LLM/pull/17278)让九个 Qwen3.5 分离式单元保持存活，而之前大多数单元几分钟内就挂了——这就是“能跑分”与“能撑过一个会话”的配置之间的差别。

两个开放中的传输改动针对超长的分离式提示词，它们一起展示了修复如何制造下一个瓶颈。默认安排下，解码 worker 必须等整个提示词预填充完再传输完才能开始，两个昂贵阶段背靠背运行，尽管第一个阶段是增量产出。[流水线化 KV 传输](https://github.com/NVIDIA/TensorRT-LLM/pull/15727)在每个预填充块一落成就开始发送，传输与预填充计算重叠，只有最后一块在关键路径上。

该改动让块处理变得频繁，从而暴露出过去只发生一次的工作。其后续改动[只检索属于当前块的 block ID](https://github.com/NVIDIA/TensorRT-LLM/pull/17526)，而不是每次检索整个提示词的块列表。对于一个切成 1,024 token 块的 128,000 token 提示词，这是“构建一次 4,096 项列表”与“为每个层组重建 128 次”的差别。一个随提示词总长度增长的每块成本，是一种会吃掉流水线化刚买来收益的成本形状。

![](https://substack-post-media.s3.amazonaws.com/public/images/e8eeb92e-1aad-4a97-b3c1-28409005809e_2048x769.png)
*来源：SemiAnalysis*

## AMD ATOM 智能体优化

AMD 的 ATOM 引擎最初只为单轮工作负载设计，而非真实世界的智能体多轮生产工作负载，因此需要对 ATOM 引擎核心和内核做大量改动，才能良好支持长上下文多轮工作负载。相对于 vLLM/SGLang 目前的水平，ATOM 在支持智能体工作负载上还有很长的路要走。AgentX 被用作 ATOM 面向智能体工作负载重构的真实北极星目标。我们要聊的第一个 ATOM 实现的优化，是为 DeepSeek-V4 分页滑动窗口注意力巧妙地使用稀疏检查点保留。[已合并的实现](https://github.com/ROCm/ATOM/pull/1640)让选定的窗口尾部保持存活，使分叉和回放请求能在有用的边界处恢复。其测量干净地分离了两种效应：在同一条 AgentX 轨迹、并发 48 下，实际前缀命中率从 5.6% 升至 96.45%，滑动窗口闸门处的损失从 91.35% 降至 0.16%。第二个数字是第一个数字背后的机制。十个前缀匹配中有九个被找到后却因缺少窗口尾部而被丢弃——缓存不是没命中，而是被否决了。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c880335-e1e3-44d9-a123-8e316c9c3808_822x555.png)
*来源：GitHub*

在这一切可被测量之前，必须先落地两个更早的缓存管理器修复，两者都值得注意，它们是“缓存自报健康却毫无作为”的例子。一个[阻止空闲池命中破坏共享缓存条目](https://github.com/ROCm/ATOM/pull/902)；另一个[延迟输出修复](https://github.com/ROCm/ATOM/pull/939)恢复了默认调度器模式下的前缀哈希，把重复的长提示词从零缓存 token 变为复用每个完整前缀块。另一个独立改动让前缀命中的预填充[留在优化的 sink 注意力内核上](https://github.com/ROCm/ATOM/pull/1345)而不是退回通用路径，使缓存命中不会悄悄消耗掉它省下的一部分。

混合模型还携带循环或压缩器状态，它与普通 KV 有一个决定性区别：无法从周围 token 重建。窗口尾部可以从相邻上下文重算，但循环状态是此前一切的累积结果，一旦被丢弃，唯一的恢复办法就是重放序列。ATOM [给这种每请求状态赋予内容寻址的检查点生命周期](https://github.com/ROCm/ATOM/pull/1771)，让已生成的轮次留下可复用的恢复点，而无须为它们预留单独的受保护缓存。在一次测试中，一个请求复用了 512 个已生成 token，只计算了一个 2 token 的后缀。

调优细节与功能本身同样重要。无条件发布检查点会让零命中流量损失 17.5% 吞吐量——这是每个一去不返的会话为帮助会回来的会话付出的代价。按 token 间隔布置检查点避免了这一惩罚，固定 1k1k 吞吐量保持在测量噪声之内，这才是相关的安全属性：一个面向智能体复用的特性不应惩罚永远不会用到它的工作负载。

ATOM 与 AgentX 相关的 CPU 路径从“卸载是否值得”的算术出发。[独立的 LMCache 卸载](https://github.com/ROCm/ATOM/pull/1318)从 CPU 重载一个 32,000 token 前缀约需 0.32 秒，而重算约需 2.5 秒，八倍的差距。这让在这些上下文长度下跨总线搬运是值得的，短提示词则不成立。

路径的其余部分关乎所有权和索引放置而非带宽。ATOM 借鉴了 vLLM 的[多连接器](https://github.com/ROCm/ATOM/pull/1406)设计，让预填充 worker 同时向远程解码 worker 发送 KV 并把相同前缀存到 CPU，在两个消费者都完成之前不释放块；同一块有两个独立读者，这是单轮场景不会遇到的情况。

[把恢复的块提升回 GPU 前缀索引](https://github.com/ROCm/ATOM/pull/1725)修复了一种更隐蔽的浪费：没有它，从 CPU 加载的前缀被使用后不会注册为驻留，下一轮再次跨总线取同一个热前缀，为一个已在 HBM 中的缓存反复支付传输。后续工作[一并修复了异步保存顺序、打包 KV 几何、未对齐交接和远程请求簿记](https://github.com/ROCm/ATOM/pull/1807)，在两轮、2,638 个请求的验证中消除了重载损坏。这个 bug 只在同一批块被多次保存、逐出和恢复时才会出现。

![](https://substack-post-media.s3.amazonaws.com/public/images/a7bb7f74-e5a3-4da3-b954-89905e54c4da_2048x420.png)
*来源：SemiAnalysis*

分布式路径在另一个代码库里重复着同样的模式，这个模式在 SGLang 和 Dynamo 中已经可见：路由必须知道状态在哪里。ATOM 的路由器叫 ATOMesh，是 SGLang 路由器去掉大多数特性的 fork。遗憾的是，ATOMesh 需要 SGLang 的缓存感知路由特性，所以该特性不得不被加回来。ATOM 获得了面向缓存感知路由器的 KV 生命周期事件，路由器才能知道状态在哪里。它还获得了多节点预填充与解码路由，以及会话粘性的数据并行路由。粘性策略是一个双面妥协，值得明确说明：会话回到持有其状态的健康 worker，但空闲分配会过期，使粘性不会为已经离开的会话永久性地让集群失衡。

分离式架构随后必须搬运模型实际保留的一切，而这不总是一块统一的缓存。DeepSeek-V4 [传输其 FP8 与 BF16 混合缓存布局的两个缓冲区](https://github.com/ROCm/ATOM/pull/1737)，EAGLE 分离[随目标缓存一起搬运草稿模型的独立 KV 缓存](https://github.com/ROCm/ATOM/pull/1331)——这是 TensorRT-LLM 和 SGLang 各自都不得不解决的同一个第二缓存问题。[远程 KV 准入与背压](https://github.com/ROCm/ATOM/pull/1647)补上了闭环：阻止解码侧接受超过其能安全恢复的停靠传输，这是“接受你完不成的工作”的分离式版本。

在 ATOM 上，[PCP 报告平均 TTFT 降低 35% 到 43%](https://github.com/ROCm/ATOM/pull/1220)，在 64,000 token 输入下总吞吐量提升最高约 49%——这一收益随输入长度而不是批大小增长。要让它在实践中可用，需要与一个会话依赖的其他一切可组合，因此 DCP 被改为[与前缀缓存、分块预填充和 FP8 KV 兼容](https://github.com/ROCm/ATOM/pull/1701)，随后又[扩展到 MTP](https://github.com/ROCm/ATOM/pull/1746)。一个不能与前缀缓存共存的并行技术，等于用一项长上下文胜利换另一项。同样的并行稀缺也存在于单块 GPU 内部：batch-1 的 MLA 解码没有头或查询维度可分散，只有 KV 遍历，而硬编码的 16 路 split 预算让这个遍历只跑在 gfx950 的 256 个 CU 中的 16 个上。一个[仍开放中的改动](https://github.com/ROCm/ATOM/pull/1911)停止覆盖内核自己的 split 推导，让 Aiter 把遍历切成机器拥有的 cluster 数那么多份。

[分块流水线并行预填充](https://github.com/ROCm/ATOM/pull/1552)从内存侧攻克同一问题，用流式的层-阶段交接取代重复的张量并行集合通信。它在高负载下的 GLM-5.2 结果是本节最完整的：输出吞吐量翻倍，中位首 token 时间从 28.6 秒降至 8.7 秒，每块预填充 GPU 容纳的 KV 块是原来的 3.68 倍。最后一个数字最该先读，因为每块预填充 GPU 的容量决定了部署撞上 HBM 悬崖之前能有多少长会话在途。

![](https://substack-post-media.s3.amazonaws.com/public/images/8184b9e6-883b-446c-884b-226b5e9fcca1_2048x549.png)
*来源：SemiAnalysis*

## ROCm AITER 智能体优化

ATOM/AMD vLLM/AMD SGLang 的长上下文执行依赖配套的底层 AITER 内核，因为引擎层的并行策略只有在内核能表达它时才成立。[预填充上下文并行进程组](https://github.com/ROCm/aiter/pull/3728)提供了预填充上下文并行所需的额外查询分片维度，并为超过 131,000 token 的提示词加宽了融合内核的行索引。[解码上下文并行](https://github.com/ROCm/aiter/pull/3267)（DCP）在既有的张量并行 GPU 之间分片 KV，使更长的序列或更大的批无须在每个 rank 上复制整个缓存就能容纳。

大型缓存还暴露出一类短固定请求基本永远触及不到的故障：地址位宽。32 位偏移完全够用——直到单个缓存池越过边界，此时算术回绕，内核寻址到错误的行且不报任何错误。AITER 增加了[批预填充超过 4 GB 时的运行时 64 位派发](https://github.com/ROCm/aiter/pull/2893)、[超过 2 GB 的 64 位 MLA 偏移](https://github.com/ROCm/aiter/pull/4474)，以及 [DeepSeek-V4 统一缓存路径全面的 64 位寻址](https://github.com/ROCm/aiter/pull/4680)——最后一项防止了在约 1.5 亿行的池中静默读写错误的行。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce356c05-883b-4c63-a359-8cfd72dddb63_1408x1046.png)
*来源：SemiAnalysis*

DeepSeek-V4 解码还获得了[面向 64 头和 128 头 MTP 打包的持久 MLA 内核](https://github.com/ROCm/aiter/pull/3459)。这两个头数正是普通解码和投机验证实际产生的，因此这给引擎的常见形状提供了专用的长上下文路径，而不是把它们当作为短上下文编写的内核的附带变体。这与上面 vLLM AITER 稀疏 MLA 选择是同一个论点：在长上下文中，通用路径不是温和的妥协，而是错误的内核。

## Dynamo 智能体工作负载优化

Nvidia 相当一部分提交使用 Dynamo 推理编排与路由系统。Dynamo 的 AgentX 系列表明，一旦引擎内核改善，分布式服务层本身可能成为瓶颈。路由器的工作量与活跃前缀的数量和长度成正比，而不是与生成的 token 数成正比，因此许多长、重叠、长寿命会话的工作负载对它的压力方式是固定形状流量永远不会有的。第一批 PR 降低了每次路由决策的成本：[查找热路径上更少的工作](https://github.com/ai-dynamo/dynamo/pull/10540)、[不再冗余的后缀失效](https://github.com/ai-dynamo/dynamo/pull/10836)，最后是[批量化的 KV 匹配、注册、所有权和终端解引用](https://github.com/ai-dynamo/dynamo/pull/11095)，报告在并发 512 下中位输出吞吐量提升 22.2%。批量化在这里有效的原因与在引擎中相同：每项开销此前主导了项本身。

![](https://substack-post-media.s3.amazonaws.com/public/images/7af8faf5-300e-4ee5-bc0c-040b7630e923_1016x671.png)
*来源：GitHub*

第二批 PR 改变了所有权的表示方式，这是底下更难的问题。每个缓存块都需要归属于依赖它的请求，使其在使用中不被释放、在所有人完成后不被钉住。当成千上万个并发会话共享重叠前缀时，簿记本身就变得可观。Dynamo 从[共享块链](https://github.com/ai-dynamo/dynamo/pull/11503)走到[arena 级所有权计数](https://github.com/ai-dynamo/dynamo/pull/11508)，最后到[后端专属的请求租约](https://github.com/ai-dynamo/dynamo/pull/12329)，每一步都让被跟踪的单元更粗。租约设计让 vLLM 后端的 AgentX 回放时间减少 23.7%，SGLang 减少 22.0%，同时降低峰值内存——这表明问题出在此前的表示方式而不是流量。

![](https://substack-post-media.s3.amazonaws.com/public/images/e3039950-98e0-4cd0-b7fe-929a120bd7d2_2048x576.png)
*来源：SemiAnalysis*

进一步的路由器剖析移除了同样形状的成本——周期性全量扫描或完整重算之所以曾经可接受，只是因为活跃状态过去很小。[分桶过期剪枝](https://github.com/ai-dynamo/dynamo/pull/10521)取代了与全部被跟踪对象成比例的扫描，让高流转 AgentX 吞吐量提升 13.7%。[仅增量的后缀清理](https://github.com/ai-dynamo/dynamo/pull/10676)只处理变化的部分，在同一窗口吸收了约 28 倍的存储和删除事件。[压缩提示词路径](https://github.com/ai-dynamo/dynamo/pull/11644)将前端 CPU 削减 35.3%，实质性改善了尾部首 token 时间——这很重要，因为该工作负载的提示词长且大量重复。过载状态现在[增量跟踪](https://github.com/ai-dynamo/dynamo/pull/10645)而非重算。

![](https://substack-post-media.s3.amazonaws.com/public/images/878dd41d-fc0f-407e-8421-ad05ad9e740c_1087x624.png)

一项路由改动是深思熟虑的权衡而非纯粹收益。Dynamo 现在[可以在路由评分中计入活跃解码请求](https://github.com/ai-dynamo/dynamo/pull/12158)，使一个已承接长时解码的 worker 看起来比仅凭队列深度更昂贵。在报告的调优点上，这以小的吞吐量代价改善了 AgentX 中位延迟——这种选择只在请求长时间占用 worker 时才会显现。一个[开放中的后续工作](https://github.com/ai-dynamo/dynamo/pull/13447)把该权衡打包成新的智能体路由器预设，沿同一方向更进一步：前缀重叠记 2 分、预填充负载乘 4、活跃解码请求权重 64。在该调优点上，权衡不再损失吞吐量：在 8xH200 AgentX 运行中，该预设相对默认成本函数把固定窗口已完成输出吞吐量提升 8.26%，将运行级 p95 首 token 时间削减 43.1%、p95 inter-token 延迟削减 22.6%，并多完成了一条完整轨迹。

接下来优化的是请求平面，因为智能体轨迹不是发一个请求收一个响应。它发送许多携带基本相同提示词的相关请求，并把每个 token 作为独立帧流式返回，因此序列化和拷贝按轮次和按 token 支付而不是一次性支付。切换到 [MessagePack 请求载荷](https://github.com/ai-dynamo/dynamo/pull/10437)在其 AgentX 测试中把吞吐量提升 8.1%、平均首 token 时间降低 9.7%，[直接 Python 转码](https://github.com/ai-dynamo/dynamo/pull/11104)则把中间值树从该路径中完全移除。

随后是一串都在消除拷贝而不是加速拷贝的改动：不拷贝 [MessagePack 事件载荷](https://github.com/ai-dynamo/dynamo/pull/11539)、不拷贝[接收到的 ZeroMQ 帧](https://github.com/ai-dynamo/dynamo/pull/11574)、不在每个 token 上支付完整的 [inter-token 延迟指标开销](https://github.com/ai-dynamo/dynamo/pull/11569)。[聊天流式热路径](https://github.com/ai-dynamo/dynamo/pull/10433)出于同样原因被缩短。单独看，这些都毫不起眼；但乘以每个并发会话的每个流式 token，它们决定了前端每秒能维持多少请求。

高并发剖析随后发现了与搬运数据无关的成本。[静态日志过滤器](https://github.com/ai-dynamo/dynamo/pull/11820)移除了共享的 span-matcher 锁——这是争用点而不是量的问题——将报告的前端吞吐量从每秒 932 提升到 1,133 个请求。[更简单的位置 radix 桶](https://github.com/ai-dynamo/dynamo/pull/12161)在 32 worker 运行中将 mocker 峰值内存降低 5.51 GiB。一个开放中的改动[每个响应只刷一次 detokenization 指标](https://github.com/ai-dynamo/dynamo/pull/12999)而不是在每个流式块上更新累计计数器，在其匹配的诊断剖析中大约把前端 CPU 时间减半。最后一项是这类问题最清晰的例子：仪器化本身每次调用很便宜，但每个 token 调用一次就是灾难。

## LMCache 智能体优化

LMCache 是一个位于 vLLM 等推理引擎之下的开源 KV 缓存层，按前缀哈希为键，把可复用的 KV 块存储在 CPU DRAM、本地 NVMe 和远程后端（Mooncake、Redis、S3）之上。LMCache 可作为 vLLM 原生卸载连接器的替代方案。

![](https://substack-post-media.s3.amazonaws.com/public/images/945da9bc-59ec-4084-9f3a-da58da04b3c5_2048x638.png)
*来源：SemiAnalysis*

LMCache 的多进程路径为智能体缓存搬运的体量和形状做了改动，先从一个不是变慢而是彻底停住的故障说起。当许多上下文超过 100,000 token 的请求各自在启动前为整个负载预留块时，池子被一群全在等待、无一推进的请求耗尽。[分块的外部缓存加载](https://github.com/LMCache/LMCache/pull/3382)改为按块预留，加载得以交错并排空。在并发 32 下，验证完成了 120 个请求，而旧路径在第 28 个后死锁；并发 48 持续运行，KV 池占用 98.5%。

其余改动减少搬运量以及运行时碍事的频率。只存储 DeepSeek-V4 混合组中有用的部分，把[每 token 存储量削减近二十倍](https://github.com/LMCache/LMCache/pull/3635)；滑动窗口预取现在[只加载活跃窗口](https://github.com/LMCache/LMCache/pull/3869)而不是永远不会被读的窗口状态——与 vLLM 用于卸载的可达性论证相同，只是从存储侧切入。[每个对象组一次原生传输调用](https://github.com/LMCache/LMCache/pull/3908)随后消除了跨暂存拷贝和内核启动的反复 Python 锁交接，这种开销与片段数量成正比而不是与其中字节数成正比。

两个当前的 LMCache 改动对 AgentX 尤其特定但尚未合并。[混合锁簿记修复](https://github.com/LMCache/LMCache/pull/4524)阻止一个请求释放另一个请求在共享滑动窗口或循环状态块上的读锁。多个请求必须共享相同块、簿记必须按块而不是按持有者、逐出必须真正启动。带 DRAM 卸载的 Kimi-K3 持续运行同时提供了这三个条件，在逐出开始后产生了数万条警告、损坏的生成，最终 GPU 崩溃。任何短于长时、共享、内存受压的运行都让它潜伏。

LMCache 的另一条平行工作线让上述一切在 AMD Instinct 硬件上可用。CacheBlend 的非前缀复用依赖 flashinfer，而后者仅支持 CUDA，因此[一个 Triton 块稀疏注意力后端](https://github.com/LMCache/LMCache/pull/3092)重新实现了它需要的三个内核：带 CSR 索引和 log-sum-exp 输出的块稀疏注意力、因果预填充，以及 log-sum-exp 输出混合。它随后在检测到 ROCm 或 flashinfer 缺失时自动路由过去。[ROCm Dockerfile](https://github.com/LMCache/LMCache/pull/3101)镜像了 CUDA 构建和轻量镜像。[AMD hipFile 后端](https://github.com/LMCache/LMCache/pull/3843)扩展了此前只能通过 NVIDIA cuFile 访问存储的 GDS L1 slab 文件层，通过 ctypes 绑定 ROCm 的 hipFile 并按 torch.version.hip 派发；cuFile 路径不变。

分发是剩下的缺口。CUDA 用户安装预构建 wheel；AMD 用户从源码构建。我们与 AMD 合作发布了[预构建的 gfx942 和 gfx950 wheel](https://github.com/LMCache/LMCache/pull/4273)，补上了这个缺口。它安装进上游镜像并在 MI350X 上通过全部 56 个 KV 传输内核测试，发布到 GitHub release 而非 PyPI，因此普通的 pip install lmcache 仍然是 CUDA 构建。[一行后续修复](https://github.com/LMCache/LMCache/pull/4363)把绑定挂载的仓库标记为 git safe directory，这只在 CI 中失败，因为容器以 root 身份运行在属于 runner 的 checkout 上，而 setup.py 的版本内省拒绝读取它。

![](https://substack-post-media.s3.amazonaws.com/public/images/89c2f79c-a704-4144-a900-ddd69ce306dd_1112x667.png)
*来源：GitHub*

[DCP 感知的 CPU 卸载](https://github.com/LMCache/LMCache/pull/3561)解决了一个直白的不兼容——长上下文使这两个特性必须同时启用。启用解码上下文并行后，每个 rank 只持有 KV 的一个跨步，任何单个 rank 能保存的都不是可用的前缀；该修复在保存前汇集跨步分片，加载后重新分发。没有它，启用上下文并行会悄悄禁用 CPU 缓存命中——恰恰是促使这两个特性出现的那些长前缀。其验证记录了超过 30,000 次 CPU 命中事件，单请求加载达到数十万 token。

## Mooncake 智能体优化

Mooncake 服务于 Moonshot 的 Kimi 生产流量以及许多实验室的生产流量，是分离式 vLLM 和 SGLang 配置之下的传输引擎。直到最近，Mooncake 的 AMD 支持在 RDMA 注册和可安装包两方面都有欠缺。

![](https://substack-post-media.s3.amazonaws.com/public/images/32c734aa-1f52-47af-a98e-334978b4e6fa_1778x1386.png)
*来源：SemiAnalysis*

在 Nvidia 上为 RDMA 注册 GPU 内存，要么使用 nvidia-peermem 内核模块，要么导出 dmabuf 文件描述符。AMD 没有 nvidia-peermem 的等价物，因此 GPU-direct RDMA 完全没有路径，部署只能退回经主机 DRAM 暂存 KV。[HIP dmabuf 注册分支](https://github.com/kvcache-ai/Mooncake/pull/2225)添加了现有 CUDA dmabuf 路径的镜像，通过 ROCm 而不是 CUDA 句柄调用导出，并且先解析真实的分配基址，因为缓存分配器会把张量打包在更大分配内部的偏移处。主机内存仍直接注册。

装不上的支持不算支持。Mooncake 发布了 CUDA 和 MUSA wheel 却没有 ROCm 包，AMD 用户只能在每个镜像里从源码构建引擎。[ROCm wheel、CI 和发布路径](https://github.com/kvcache-ai/Mooncake/pull/3184)将 mooncake-transfer-engine-rocm 与它们一起发布到 PyPI。这条来自 AMD 工程师 Andy Luo 的工作流，源于在用 AgentX 内部试跑智能体工作负载时注意到一个模式：在 ROCm 上从源码构建 Mooncake 不是一等公民的模式。

![](https://substack-post-media.s3.amazonaws.com/public/images/12cd94ca-2aa7-4e06-a4bd-3153982234c5_1220x680.png)
*来源：GitHub*

该传输引擎没有设备内核也不依赖 torch，因此一个架构无关的 wheel 即可覆盖 gfx942 和 gfx950，ROCm 运行时在加载时绑定而不是打包进来，这意味着同一个 wheel 无需修改即可在上游 vLLM ROCm 镜像和 SGLang ROCm 镜像中使用。这一点按完整交叉积验证：MI300X 和 MI355X，各自在 vllm/vllm-openai-rocm 和 lmsysorg/sglang 下，运行 master 二进制和带数据校验的 HIP 缓冲区传输测试。该 PR 增加了覆盖 Python 3.10 到 3.13 的按 tag 触发发布。一个开放中的后续工作[增加自托管的双节点 MI350X 外部预填充与解码层](https://github.com/kvcache-ai/Mooncake/pull/3338)，使 ROCm 分离式路径在真实硬件上得到锻炼而不是只被编译。

这些 PR 加在一起意味着，AMD 的 AgentX 运行现在可以从已发布的制品把传输引擎和 KV 缓存层安装到原版上游镜像中，并在 GPU 内存与互联网络（fabric）之间直接搬运 KV。

## 其他优化

上述改动针对长上下文成本：必须存活的前缀、必须保持正确的混合缓存、必须跟得上的传输。但还有一大堆第 0 天（day-zero）使能和正确性 bug，它们对请求的破坏与百万 token 会话一样严重。

MiniMax-M3 检验了那些 ROCm 工作能否累积成第 0 天就绪，[Advancing AI 一文](https://newsletter.semianalysis.com/p/can-amd-break-the-cuda-moat-amd-advancing)直接做了对比：AMD 首个公开的分离式方案 MI355X FP4 于 1 月才到达 InferenceX，落后 Nvidia 数月，而 M3 FP4 分离式在第 0 天就落地。相比 DeepSeek-R1 时期（对等用了数月），这是进步。三个 vLLM 修复位于这条第 0 天路径上，每一个都是正确性故障而非性能问题。

分离式首先被阻断。NixlConnector 的握手断言 SPLIT 区域的 block_len 随预填充到解码的 TP 比率缩放，但 block_len 实际上取决于每 rank 的 KV 头数。M3 有 4 个 KV 头，因此 TP4 预填充配 TP8 解码在两侧都被 GQA 限制为每 rank 一个头，两个长度相等，而断言却要求两倍。握手被拒绝，KV 没有移动，解码从头重生成一切，gsm8k 得 0 分。[按实际头数比率校验](https://github.com/vllm-project/vllm/pull/45879)修复了这个问题。

另外两个是平台分歧。M3 的稀疏注意力后端对每个 E4M3 配置都把字节支撑的 FP8 缓存读作 float8_e4m3fn。但 gfx942 的平台 dtype 是 e4m3fnuz，两种编码不同。K 和 V 因此在内核消费前被篡改。预填充和解码包装器也把 FNUZ 类型排除在 FP8 检查之外。[对缓存视图使用平台 dtype](https://github.com/vllm-project/vllm/pull/45720)同时修复了两半。另外，M3 以独立的 NVIDIA 和 AMD 模型文件发布，只有 NVIDIA 版实现了 EAGLE3 接口，因此投机解码在 ROCm 上引擎初始化时以“模型不支持”错误中止。[让 AMD 模型对等](https://github.com/vllm-project/vllm/pull/45546)恢复了它，MI355X 的 gsm8k 与非 EAGLE3 的 MI355X 运行以及 B200 持平。

上面的 TensorRT-LLM 一节涵盖了 M3 长上下文专属的工作：分离式 KV 传输中的描述符爆炸、上下文图捕获、稀疏块步长、自动调优器候选，以及必须从池中移除的损坏 split-K MoE tactic。

本地 AgentX 矩阵组合了会话感知或 KV 感知路由、长且可变的对话历史、MTP、混合注意力、聚合与分离式服务，以及跨越 HBM 容量悬崖的并发扫掠。它包括 GPU 驻留对比和通过 vLLM SimpleCPU、Mooncake、LMCache、SGLang HiCache 的 CPU DRAM 卸载。正是这一组合激活了上面的上游工作。旧的固定序列矩阵通常创建一个提示词、做一次预填充、解码一个固定续写、然后丢弃请求。因此它不衡量跨轮次的缓存存活、重复 tokenization、会话亲和、缓存事件流量、卸载扰动、调度器停顿期间的传输进度，或长生命周期的所有权簿记。

允许的优化策略把 CPU KV 卸载视为可选。厂商可以使用 vLLM 连接器、LMCache、SGLang HiCache、Mooncake、Dynamo KVBM 或其他 CPU DRAM 连接器，也可以在关闭卸载反而得到更好的延迟与吞吐点时禁用它。NVMe 卸载暂缓。CPU DRAM 必须随使用的 GPU 比例缩放，包括非标准化 DRAM 系统的 3 TB 上限。标准化 DRAM 系统没有硬上限但保留同一比例规则。本地生成器目前对每个 runner 都应用 3 TB 上限，因此尚未实现标准化 DRAM 例外。

净新增的优化面不只是更长的注意力，而是对不断增长的会话状态的保存、搬运、路由、重建和重复处理。AgentX 把这些成本放大到足以驱动 vLLM、SGLang、TensorRT-LLM、ATOM、AITER、Dynamo 和 LMCache 的通用上游改动。直接搜索 NIXL 和 Mooncake 未发现更多带 AgentX 标签的运行时 PR，因此它们的相关影响仍通过上面的引擎连接器改动体现。

# AgentX 方法论深度解析

AgentX 是开源真实世界长上下文多轮智能体轨迹回放的一次重大跃迁。我们在自有数据集中收集了价值超过 300 万美元的 token 的轨迹，由 Claude Code、OpenAI Codex 等的真实流量构成。除数据集外，我们还开发了一套完整的方法论来公平地回放这些流量模式。目标是尽可能忠实于有机流量，同时对 GPU 资源需求保持公平。

我们将深入解析智能体轨迹数据集、回放方法论以及总体上的智能体行为。推荐希望更好理解智能体工作负载整体形态以及编排器（harness）如何在底层编排请求的读者阅读。

## 300 万美元智能体流量轨迹采集器

最初设计 AgentX 时，我们的北极星目标是让基准在 KV 工作负载形状和 KV 复用模式上尽可能真实。我们开始尝试回放一些既有数据集，如 SWE-bench、Qwen-Bailian 以及 HuggingFace 上其他零散的 Claude Code 轨迹。当时这些数据集并不包含子智能体的重度使用、1M 上下文、压缩（compaction）、动态工作流等近期智能体轨迹的诸多决定性特征。在 SemiAnalysis，团队大多数成员都是 AI 重度用户，把智能体用于各种任务，包括编码、分析师研究、Excel 建模、社交媒体运营等等。因此我们决定，最可实现也最真实的轨迹可以在内部采集。

为采集大量轨迹，我们创建了一个拦截发往 Claude / Codex 的 HTTP 请求的代理。希望上传轨迹的用户只需在 Claude / Codex 配置中把 base URL 改为指向该代理。截至撰写时，我们已收集超过 8,000 个会话、340 万个请求、6,100 亿个 token，合计代表超过 300 万美元的支出。[我们为 AgentX v1.0 基准开源了其中有代表性的会话子集](https://huggingface.co/datasets/semianalysisai/cc-traces-weka-062126)。

虽然智能体编排器看起来复杂，但它们最终编排的是一连串 HTTP 请求。每个请求都包含系统指令、工具定义和累积对话历史的某种组合。随着会话推进，这段历史不断增长并被反复发回模型，形成 AgentX 旨在重现的长上下文和高前缀复用。

我们的代理实时记录这些请求和响应，还提取元数据/HTTP 头，如时间戳、会话 ID 和子智能体 ID，使我们能够还原对话的*结构*（请求顺序、并发分支以及每个会话的大致父/子结构）。正是这些元数据让我们能够大致按照原始 Anthropic API 服务器所见的样子回放轨迹。

为保护员工隐私，回放数据集不含原始提示词、源代码、工具参数或工具结果。我们把每个请求的内容 token 化后按 64 token 分组，再用会话作用域的链式哈希替换每个块。这样，匹配的提示词前缀产生匹配的哈希前缀，却不泄露内容（[这篇论文](https://arxiv.org/abs/2506.02634)更多讨论了这一策略）。回放时，这些哈希块可被替换为来自如编码数据集的 token。因此我们保留了原始工作负载近似的上下文增长和对话 KV 复用模式。

值得注意的是，这一过程必然不完美，主要因为在使用前沿模型提供商的 API 时，终端 LLM 服务器实际看到的大部分内容是隐藏的。例如，SOTA 模型的思考/推理内容现在在 HTTP 请求中被加密并被确定性哈希取代，以阻碍蒸馏攻击。不过，[这件事似乎没有像大实验室计划的那样完全奏效……](https://arxiv.org/html/2608.09867v1)

![](https://substack-post-media.s3.amazonaws.com/public/images/767f2f58-fa9d-40d3-8711-751d243cae9a_500x487.png)
*来源：SemiAnalysis*

此外，虽然我们能拿到用户/助手消息、系统提示词、工具使用等的全部原始*内容*，但 API 提供商会在服务端应用额外的聊天模板，这些并不透明。我们也无法观察 Anthropic 的专有 tokenizer 或服务端工具引入的上下文。图像和文档的线上表示与模型处理的 token 数之间也没有直接的对应关系。我们使用确定性占位符和经验校准的、按模型特定的填充，使重建的提示词长度最接近服务器实际看到的内容。

由于信息不完整，我们无法*完美*地按 Anthropic / OpenAI 服务器*实际所见*捕获和回放 Claude Code / Codex 轨迹，但可以相当接近。下图展示了在所有请求长度和模型上，哈希 token 数（经我们的近似/处理后）与 API 提供商真实 token 数的比值。

![](https://substack-post-media.s3.amazonaws.com/public/images/7123b5de-9942-4298-8ccd-1b69b8a71df0_2048x1799.png)
*来源：SemiAnalysis*

总结一下：由于信息不完整，以完全等同于在原始服务器上回放的方式采集真实 Claude Code 轨迹并不容易。但我们有足够的上下文来以极高的保真度采集和回放轨迹，匹配原始的流量模式、时序、前缀缓存和 DAG 模式。

## AgentX 300 万美元数据集

AgentX v1.0 使用的数据集可在 [HuggingFace](https://huggingface.co/datasets/semianalysisai/cc-traces-weka-062126) 找到。它是上一节提到的 8.3k 会话代理语料的 393 会话子集。此外，我们做了一些后处理来清理异常，例如：

- 移除 Claude Code 安全监视器（auto 模式）请求和标题生成请求，因为它们是 Claude Code 特有的，不一定代表一般智能体流量
- 移除重建输入长度大于 990k token 的请求（我们的近似在这些地方高估了）
- 移除重复请求（有时连接中断会导致代理收到相同请求）

此外，每个对话被格式化为 WEKA 轨迹格式，由 Callan Fox 在其 [kv-cache-tester](https://github.com/callanjfox/kv-cache-tester) 项目中提出。我们选择这一格式存储轨迹信息，主要因为我们在开发基准时与 Callan 紧密合作，并发现它存储按会话的轨迹很直观。总的来说，轨迹格式本身相当任意，我们的代理数据集也可以映射到其他格式，如 [Mooncake](https://docs.nvidia.com/aiperf/benchmark-modes/trace-replay-with-mooncake-traces)。

![](https://substack-post-media.s3.amazonaws.com/public/images/48045991-20d7-4685-863d-c9aa1d6d3142_1812x2048.png)
*来源：SemiAnalysis*

应用这些处理后，我们得到以下数据集。注意并非所有 X 轴都相同。

![](https://substack-post-media.s3.amazonaws.com/public/images/f22c9c7e-44ba-4ffd-bdc3-58fbbef8f30d_2048x2004.png)
*来源：SemiAnalysis*

ISL/OSL 和轮间延迟（在智能体工作中主要是工具使用耗时）的分布相对接近对数正态。ISL 中位数为 142k token，OSL 中位数为 444 token。轮间延迟（或“工具使用时间”）中位数为 3.84 秒。只有约 10% 的轮间延迟大于 1 分钟。这些很可能是编排器等待真人实际响应的间隔。

值得一提的是，这些请求分布会因所用编排器而不同，因为注入的上下文数量和类型不同（例如 Pi 的编排器注入上下文以极简著称，而 Claude Code 恰恰相反）。此外，ISL/OSL 分布还取决于模型，不同模型的 tokenizer 产生的 token 或多或少。不过，鉴于全球相当大一部分智能体编码流量经由 Claude Code，我们认为这一分布相当有代表性。

数据集中还有 175 个会话至少含有一个子智能体（约占全部会话的 44%）。数据集总共有 1,697 次子智能体展开（rollout），每会话中位数为 4 次。子智能体的中位墙上时间（第一个请求开始到最后一个请求结束）为 2.27 分钟。该分布同样相对接近对数正态。

![](https://substack-post-media.s3.amazonaws.com/public/images/f4792809-087e-431b-acce-aecdd3855b3b_2048x1390.png)
*来源：SemiAnalysis*

该数据集包含高达 1M 的上下文，用于测试较新的前沿开放权重模型。此外，我们还有[一个截断为 256k 上下文长度的数据集](https://huggingface.co/datasets/semianalysisai/cc-traces-weka-062126-256k)，用于对最大上下文长度 256k 或更小的模型回放。

## 智能体流量轨迹回放器

我们没有从零构建回放方案，而是决定与 [AIPerf](https://github.com/ai-dynamo/aiperf) 合作——这是 Nvidia 的厂商中立 HTTP 回放工具，已被业界广泛采用，包括 tenstorrent、AWS、AMD 等。虽然我们打算把 AgentX 特性集成到上游仓库，但我们维护一个单独的 [fork](https://github.com/SemiAnalysisAI/aiperf) 以更加厂商中立，从而掌控是否允许更多第三方贡献。再次感谢 AIPerf 团队，特别是 Anthony Casagrande，感谢他们为构建真实而有代表性的智能体基准所付出的帮助与投入。

一个智能体会话天然可以描述为有向无环图（DAG）。每个请求是一个节点，一条边表示边头部的请求必须等边尾部的请求完成才能发出。每条边还携带一个延迟，指定前置条件满足后再等多久。

最简单的会话完全是线性的：没有子智能体、没有并行请求，每个请求恰好依赖一个前驱。图退化为一条线，边唯一编码的是轮间延迟（即工具使用时间或“思考”时间），这是客户端本地的工作而非模型的。

![](https://substack-post-media.s3.amazonaws.com/public/images/20662be0-c311-49e9-8e39-0973d8a1865d_2048x1169.png)
*来源：SemiAnalysis*

在智能体轨迹中，还可能派生子智能体。子智能体是一条拥有自己上下文的独立请求流，通常用于执行一个聚焦的任务。多个子智能体可以并行运行以完成更多总工作量，某些情况下子智能体还能与主智能体并行。主智能体随后等待一组组子智能体完成，再把它们的输出并回主智能体的上下文（虽然并非*总是*如此，但这是最常见的模式）。

正是这种行为把上面的线性请求链变成了 DAG，其中某些请求依赖其他请求。当识别出属于某个子智能体的一组请求时，AIPerf 找到最近的主智能体前驱，将其指定为“派生”（spawning）请求。类似地，“汇合”（join）请求由子智能体组时长结束后随后的主智能体请求确定。

在下面的例子中，子智能体组只包含一个子智能体（001），它运行两个请求。主智能体的开场请求一完成，它的第一个请求就发出。该请求完成后，一个 2.2 秒的轮间延迟代表工具使用的墙上时间，然后子智能体的第二个请求发出。主智能体的第二个请求是子智能体 001 的汇合点。它只有在两个条件都满足时才发出：距主智能体第一次响应至少已过 17 秒，*且*子智能体 001 的第二个请求已完成。

一个小限制是 HTTP 时间戳揭示时序，却不总能揭示因果。在下面的例子中，如果子智能体 001 完成时距主智能体请求 2 的记录开始还有 7 秒，我们无法判断这 7 秒是子智能体返回后执行的工作，还是早已在进行的独立工作。因此 AIPerf 同时保留两个约束：请求 2 既等待其记录的主路径延迟，也等待子智能体 001 完成。这重现了观察到的时序和工作负载拓扑，但不含编排器内部隐藏的依赖。这些是我们希望在 AgentX 后续版本中改进的地方。

![](https://substack-post-media.s3.amazonaws.com/public/images/18adec21-15d9-40cd-af7d-0772da4a9af0_2048x1729.png)
*来源：SemiAnalysis*

一个请求也可以派生多个子智能体。在下面的例子中，子智能体 001 和 002 都把派生父节点识别为主智能体请求 1，然后在主智能体请求 2 处汇合。

AIPerf 还能识别“辅助”请求，即不与流中任何其他请求共享上下文的一次性请求。它们从主智能体分出且永不汇合。实际中，这类请求就像 Claude Code 的“总结本会话”请求，与会话上下文无关。另一个好例子是 Claude Code 的“/btw”特性。

![](https://substack-post-media.s3.amazonaws.com/public/images/3d5f01ad-1736-496b-91b4-31672002bf47_1920x2048.png)
*来源：SemiAnalysis*

下面的例子把它们全部综合起来。这是你在真实数据集中会看到的轨迹片段类型。五条并行流离开同一个主智能体请求，按它们汇合到的主智能体请求分成组。

子智能体 001 和 002 分别在第 20 和 23 秒完成，因此之后第一个于第 25 秒开始的主智能体请求是它们的汇合点。子智能体 003 和 004 在同一间隙派生但运行得更久，分别在第 46 和 50 秒完成，所以它们改在第 52 秒汇合。AIPerf 用（派生请求，汇合请求）这一对作为每个子智能体的键，这意味着这四条流坍缩为两个分支，尽管四条流都从同一节点离开。分支取其第一个成员的名字，这就是汇合边标注为子智能体 001 和子智能体 003 的原因。

这也是主智能体与自己的子智能体重叠的首个案例。第 25 秒的请求在 003 和 004 仍在运行时发出：主智能体只被汇合到它的组阻塞，而不是被每个在途子智能体阻塞。

辅助链挂接到它前面最近的主智能体请求，这里是第 52 秒的请求而不是开场请求。该节点因此同时做两件事——接收第二个子智能体组的汇合，并派生那个一次性请求。当然，辅助请求永不汇合。

![](https://substack-post-media.s3.amazonaws.com/public/images/d2f465f9-372c-4ee1-b42f-e79fa9fe352b_1677x2048.png)
*来源：SemiAnalysis*

## AgentX 进一步深度解析

### 帕累托前沿扫掠

在 AgentX 工作负载中，为生成帕累托前沿，我们对单个部署扫掠并发 Claude Code 会话的数量。由于每个对话都有真实的轮间延迟和子智能体使用，我们得到了更尖峰、更真实的流量模式。下面的例子是对运行 MiniMax M3 的 B200 TP4 vLLM 服务器回放 40 个并发客户端。

![](https://substack-post-media.s3.amazonaws.com/public/images/058757ed-531f-4cfb-a1ad-a06b1499ecbd_1360x612.png)
*来源：SemiAnalysis InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/43184e50-b71a-4a48-a569-98d6906cb259_2048x1167.png)
*来源：SemiAnalysis InferenceX*

最后值得讨论的一点是，评估智能体工作负载时哪些指标重要。我们认为交互性（TPS，每秒 token 数）和首 token 时间（TTFT）仍然重要，它们是评估 SLO 的行业标准。查看 AgentX 结果时，*极其重要*的是把 TPS 和 TTFT 放在一起考虑，因为有些推理优化会以牺牲一方为代价改善另一方。

我们目前正在定义一个以有意义的方式结合 TPS 和 TTFT 的新指标。它还应考虑到：在智能体工作负载中，人们往往更关心一个*任务*完成的端到端速度，而不是收到 token 的速度或 TTFT。

最后值得一提的是，当前形式的端到端延迟如今意义较小，因为端到端延迟与 OSL 成正比。因此 P90 端到端延迟受到最长输出序列长度那 10% 尾部的严重影响。虽然它仍可用来整体比较某些配置的总体性能，我们建议改为结合查看 TPS 与 TTFT。

### 预热、计时、确定性与会话复用

AgentX 的目标是对已处于稳态的系统做基准测试。对智能体工作负载而言，这意味着剖析应从部分上下文轨迹已被缓存的时刻开始。为模拟稳态，最好也不是所有会话都从第 0 轮开始，否则可能引发“[惊群](https://en.wikipedia.org/wiki/Thundering_herd_problem)”效应。

预热分两个阶段。首先，AIPerf 用固定随机种子在每个对话的 25% 到 75% 之间选择一个墙上时间点。在该时刻，它识别每条活跃请求流（包括主智能体和任何活跃子智能体），并发送每条流在所选时刻之前最近的那个请求。这些引导（primer）请求重建该时刻的会话状态并被一起派发。AIPerf 等它们排空后继续。

![](https://substack-post-media.s3.amazonaws.com/public/images/963dce62-c49b-4deb-afee-e8dd448526c5_2048x1322.png)
*来源：SemiAnalysis*

第二阶段，每条回放通道再推进 10 个请求，给 KV 缓存更多成形机会。所有预热请求省略轮间延迟并使用最大 1 个 token 的输出长度，大幅缩短预热时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/85116f5f-be0d-405b-a5d9-6a9237b44cc3_2048x895.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/fef10e0d-261e-4978-8650-b10304ec04d0_2048x897.png)
*来源：SemiAnalysis*

预热完成后，剖析开始并持续一小时。所有指标严格在这段时间内采集。为可复现性，AIPerf 接受一个种子，确保每次运行确定性地采样会话、会话从相同点开始、每个会话每次运行都用相同的合成内容重建。剖析期间，我们对每条流施加 5 分钟空闲时间上限，使长的轮间间隙不会在基准持续期间“占用”一条 worker 通道。我们强制这样做以便能在 1 小时内有效跑完基准。在后续包含 NVMe 卸载的 AgentX 版本中，我们可能会提高这一上限以测量更长的 TTL。目前 5 分钟是合理的，因为这是 [Anthropic 的默认 KV 缓存 TTL](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#:~:text=Check%20that%20calls%20are%20made%20within%20the%20cache%20lifetime%20(5%20minutes%20by%20default))。

这种程度的确定性保证了使用相同推理引擎、硬件、并发和服务器设置的运行可复现。但由于 AgentX 是[闭环基准](https://notpeerreviewed.com/blog/tail-latency/)，不同配置会以不同速率完成不同数量的请求，给它们遇到的工作负载带来一些自然变化。这在低并发时最明显——（天然）完成的请求更少，工作负载收敛到数据集整体分布的机会也更少。

剖析期间一个会话完成后，其回放通道从数据集采样器中选取另一个会话。每次回放获得一个唯一且确定的缓存击穿（cache-bust）标记，前置到每条独立前缀链，包括主智能体链和任何全新上下文的子智能体或一次性链。分叉的子智能体从父级继承标记。标记在同一次回放内保持不变，保留其 KV 复用模式，但在不同回放之间变化，以防止人为偏高的缓存命中率。这也使并发大于数据集会话数（393）的场景得以运行。

### AgentX 的公平投机解码方法论

如前所述，数据集在采集时即已匿名化。这意味着 64 token 哈希块在回放前必须用合成内容填充。AIPerf 通过从合成的编码/工具使用 token 池中确定性采样来完成。

重要的是，KV 复用模式和请求时序都得以保留，但合成请求数据确实带来一些额外考量。即：在合成数据上运行投机解码方法，与非合成数据相比，可能导致投机器（speculator）拒绝/接受异常数量的 token（因为投机器不是在合成数据上训练的）。

我们在 [InferenceX v2 文章](https://newsletter.semianalysis.com/i/188090866/multi-token-prediction-mtp)中谈过这一缺陷，此后改进了方法论。我们与社区紧密合作，确保大多数开源推理引擎中存在一种机制，允许用户强制指定从投机器接受多少草稿 token（即“接受长度”或“接受率”）。然后，对每个（模型、投机器、草稿长度、思考模式）组合，我们在 [SPEED-Bench](https://huggingface.co/datasets/nvidia/SPEED-Bench) 智能体编码数据集上[采集平均 AL](https://github.com/SemiAnalysisAI/InferenceX/tree/main/golden_al_distribution)——这是一个“旨在跨多样语义域和真实服务形态评估投机解码（SD）的统一基准”。

然后在运行时把这些真实的投机解码接受长度应用到 AgentX，以确保厂商中立的公平性。

![](https://substack-post-media.s3.amazonaws.com/public/images/c15f47a8-fcb3-4220-80ee-4b95bfa7b0b0_2048x1376.png)
*来源：GitHub*

## 探索智能体工作负载：详细遥测教程

AgentX 需要的不只是新的基准工具和数据集。[我们还花了一些时间重建了 InferenceX 可视化的部分功能，使智能体结果更易探索和消化](https://inferencex.semianalysis.com/inference/agentic/439903)。单个 AgentX 数据点代表数千个请求，横跨不断增长的会话、子智能体、预热期、缓存状态和动态变化的在途负载。因此，帕累托曲线上的单个点可能掩盖大量有用信息。正如我们多次说过的——推理服务从来没有一刀切的方案。

![](https://substack-post-media.s3.amazonaws.com/public/images/46159be7-8b5b-49d7-990f-2ce1cf1217d0_1110x687.png)
*来源：SemiAnalysis InferenceX*

我们的一项重大改动是曲线本身的构建方式。在之前的 InferenceX 版本中，投机解码启用与禁用的配置常被显示为两条分开的曲线。我们现在正远离这种做法。前端现在合并允许的推理优化，为每个模型、SKU 和推理引擎组合显示可用的最佳曲线。因此，单条曲线上的各个点可能使用不同的优化技术和配置，包括投机解码、分离式架构或 KV 缓存卸载。

我们的目标是展示每个软硬件栈可用的最佳生产性能，而不是为每种可能的优化组合创建单独曲线。不过，我们仍然公开每个点的底层配置和溯源。点击一个点会显示带详细视图的工具提示，准确展示是哪个配置产生了它，还有运行元数据、公开可见的 CI 溯源链接以及 AgentX 专属统计。在那里，“View charts”链接会打开带 AgentX 专属统计的完整数据点详情页。

![](https://substack-post-media.s3.amazonaws.com/public/images/add2d50c-a0be-4771-a00b-e6b4f1fe8502_2048x1256.png)
*来源：SemiAnalysis InferenceX*

数据点详情视图深入展示了选定的 AgentX 运行。它包括输入和输出序列长度分布、随时间变化的交互性与 TTFT、KV 缓存利用率、请求队列深度、前缀缓存命中率、输入与解码吞吐量、提示词 token 来源分解，以及随时间变化的唯一输入 token 数。这些指标让人更容易理解为什么两个总吞吐量相近的点在回放全程表现不同。

该页面还区分预热与剖析数据。读者可以在两个阶段之间切换，检查系统在缓存状态建立期间和基准运行所用剖析期间的行为。

![](https://substack-post-media.s3.amazonaws.com/public/images/91abef64-d639-4da8-8d7e-3499be750011_1001x1541.png)
*来源：SemiAnalysis InferenceX*

使用 KV 缓存卸载的点在主图上被额外的虚线圆圈包围，用于区分启用了 KV 卸载的点。选中其中一个点时，详情页会显示卸载类型、KV 卸载引擎、芯片缓存命中率和 CPU 缓存命中率。这样既能看到 KV 卸载在何处贡献了最佳曲线，又不必为每种卸载配置单独建一条曲线。

另一个新特性是请求时间线。该视图展示选定 AgentX 运行中回放的单个请求，可按会话或按 worker 组织。会话视图把子智能体归组到其对应的根会话之下，便于查看会话与子智能体何时重叠。预热与剖析请求也仍可分开查看。

![](https://substack-post-media.s3.amazonaws.com/public/images/c8fc6236-52bd-45ff-ac2e-539899c00d87_2048x1097.png)
*来源：SemiAnalysis InferenceX*

时间线上的每个请求都可点击，直接链接到 InferenceX 数据集页面上对应的会话和轮次。读者由此可以从帕累托曲线上的一个聚合点，跳到被回放的确切匿名请求。

[AgentX 页面](https://inferencex.semianalysis.com/datasets)还包含一个用于可视化单个会话结构的火焰图。每根条代表一轮，按该会话中最大一轮的比例缩放。条被分为缓存前缀 token、未缓存输入 token 和生成输出 token 三部分。这直观呈现了上下文在会话全程如何增长，以及每个请求有多少可以从 KV 缓存复用。

![](https://substack-post-media.s3.amazonaws.com/public/images/a0e991d9-6ab6-43e7-9cc9-93ac9ca5b7bd_2048x879.png)
*来源：SemiAnalysis InferenceX*

# InferenceX/AgentX 未来的下一步

我们很高兴继续推进让 AgentX 成为最真实、最有代表性基准的目标。在可预见的未来，我们会继续对当前 v1.0.x 工具做[小的 bug 修复](https://github.com/SemiAnalysisAI/aiperf/releases)，但计划在 v1.1 工具上做更大的改动。每个不同模型的提交将始终运行相同的小版本，以确保所有结果可比。

作为快速跟进，我们将增加 SSD/NVMe KV 卸载。这将支持比 DRAM 更大的 KV 缓存工作集，从而支撑帕累托曲线左侧的高吞吐区域。

我们还将采集更大、更多样、更新的智能体轨迹数据集，覆盖更多样的模型和编排器。下一个数据集将不再把每个请求表示为一段连续的哈希 ID 列表，而是保留系统指令、用户与助手消息、工具调用和工具结果之间的边界。这将使 AgentX 能够评估那些利用编排器可见但对推理引擎通常隐藏的信息的工作负载感知服务技术。例如，路由器可以把低复用的工具流量导向专用预填充 worker、在长工具调用期间保留智能体的前缀，或在子智能体分叉时预取和共享前缀。当前格式保留了请求大小和 KV 复用模式，但缺乏评估这些优化所需的结构。

Ishan 的这份 [SGLang RFC](https://github.com/sgl-project/sglang/issues/27574)提供了更丰富轨迹结构为何重要的具体例子。它提出一个由路由器发起的提示接口，利用会话生命周期、共享前缀边界、工具调用时长和子智能体状态等信息，告知引擎 KV 何时应共享、预取、降级、钉住或保留。捕获这种结构将使未来的 AgentX 版本能够评估这些工作负载感知的缓存策略，而不只是回放扁平的 token 前缀。

![](https://substack-post-media.s3.amazonaws.com/public/images/36899201-da3b-42ec-888f-2443c63980aa_2048x1260.png)
*来源：GitHub*

最后，我们正在采集细粒度和粗粒度的功率遥测数据，以更准确地了解不同软硬件栈的“每焦耳智能”效率。

我们有太多数据和太多可能的可视化。请告诉我们你想看到的可视化，以及任何更一般的功能需求！

[提交前端功能建议！](https://github.com/SemiAnalysisAI/InferenceX-app/issues/new/choose)

# 模型生命周期全程的性能

在接下来的章节中，我们转向历史单轮数据（8k1k），覆盖每个模型从发布之日起到我们将其退出主动测试为止。Nvidia 和 AMD 在这里都有强劲的结果，包括若干 MI355X 领先的固定序列长度配置。

AgentX 更好地代表了当今的智能体推理工作负载。但历史的固定序列 InferenceX 结果对跟踪性能随时间的变化仍然有用。8k1k 和 1k1k 这类工作负载剥离了大多数会话级行为，包括前缀复用、持久 KV 缓存状态和路由亲和。这使它们对当前生产流量的代表性较低，但对于跟踪推理性能随软件支持成熟而改进仍然有用。

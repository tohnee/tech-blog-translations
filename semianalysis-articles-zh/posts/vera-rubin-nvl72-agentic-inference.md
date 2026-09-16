---
title: "Vera Rubin NVL72 智能体推理：每美元性能提升 67 倍"
title_en: "Vera Rubin NVL72 Agentic Inference: 67x better Performance per Dollar"
subtitle: "黄仁勋再度藏拙性能、每吉瓦年利润翻倍、「买得越多，赚得越多」、AgentX、InferenceX、极致协同设计"
date: 2026-09-14
source: https://newsletter.semianalysis.com/p/vera-rubin-nvl72-agentic-inference
crawled: 2026-09-15
authors: ["Bryan Shan", "Alec Ibarra", "Cam Quilici", "Wenyao Gao", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Vera Rubin NVL72 智能体推理：每美元性能提升 67 倍

> 原文：[Vera Rubin NVL72 Agentic Inference: 67x better Performance per Dollar](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-agentic-inference) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**黄仁勋再度藏拙性能、每吉瓦年利润翻倍、「买得越多，赚得越多」、AgentX、InferenceX、极致协同设计**

[Rubin 是首个面向智能体时代、横跨六款产品协同设计的平台：Rubin GPU、Vera CPU、NVLink 6 交换机、ConnectX-9、BlueField-4 与 Spectrum-6。](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) 今天，我们将发布 Rubin 的首批经过验证的智能体推理结果，测量基于我们的智能体推理基准 AgentX。即便是在早期的预发布软件上，这些结果已经说明了为什么极致协同设计（extreme co-design）是必要的。

在 GTC 2026 上，黄仁勋展示了这张图，宣称在 O(1-3 万亿) 参数模型、约 200 TPS 下，VR NVL72 相比 Blackwell 实现了每 MW 3 倍的性能。但与预发布软件上 Rubin 的真实世界性能相比，我们已经看到每兆瓦 token 吞吐量最高提升至 7 倍。**黄仁勋真该停止在 GTC 上对性能宣称藏拙了**。[上一次他这么干是在 GTC 2024，当时他声称 GB200 NVL72 将带来 30 倍于 Hopper 的性能，但当我们实测时，它比 Hopper 性能好了 98 倍。](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs?open=false#%C2%A7jensen-under-promising-and-overdelivering-hopper-vs-blackwell-vs-rack-scale-nvl72)

我们对这些性能结果的估算显示，即便在早期软件版本上，Rubin 每吉瓦所能赚取的利润也已超过 Blackwell 平台的 2 倍。随着 Rubin 软件栈与内核库逐渐成熟，以及开发者社区积累针对 Rubin 的优化经验，我们预计这一差距还将进一步拉大。

![](https://substack-post-media.s3.amazonaws.com/public/images/c1af2573-7cff-4c99-beab-d0040b3a38ab_2048x1131.png)
*来源：NVIDIA GTC 2026，对 Rubin 性能藏拙*

我们使用名为 AgentX 的[行业标准智能体推理基准场景](https://vllm.ai/blog/2026-09-08-vllm-agentx)来评估性能。它会在我们覆盖数千颗芯片的集群上回放真实世界的智能体流量。因此，实际推理服务商与超大规模 AI 实验室可以整体参照这些结果，判断哪些芯片在哪些场景下效率最高。

[我们的基准已被几乎每一家主要算力买家广泛复现、验证和/或背书](https://inferencemax.semianalysis.com/quotes)——从 [Google Cloud](https://cloud.google.com/blog/products/compute/scaling-moe-inference-with-nvidia-dynamo-on-google-cloud-a4x) 到 [Microsoft Azure](https://blog.aks.azure.com/2025/10/24/dynamo-on-aks#enterprise-scale-inference-experiments--dynamo-with-gb200-running-on-aks)、[Oracle](https://inferencemax.semianalysis.com/quotes)、[Meta](https://inferencex.semianalysis.com/quotes) 等等。此外，它还获得了[包括 vLLM、LMCache、SGLang、PyTorch、Huggingface 在内的机器学习社区的支持](https://inferencex.semianalysis.com/quotes)，以及 [OpenAI、MiniMax、ZAI、Qwen、Moonshot Kimi 等主要实验室的支持](https://inferencex.semianalysis.com/quotes)。

![](https://substack-post-media.s3.amazonaws.com/public/images/2695f94b-f1f1-4dcb-b05c-d9ebff07a610_1964x680.png)
*来源：SemiAnalysis InferenceX*

感谢黄仁勋（Jensen Huang）、Ian Buck、Nick Comly、Kedar Potdar、Rohit Nagraj 以及中国大陆 TensorRT-LLM 团队帮助完成下一代 Rubin 软件的部署调通（bring up），并协助验证我们的智能体基准结果。

[如果你觉得这个开源基准和数据有用，请给 InferenceX 的 GitHub 仓库点星！](https://github.com/SemiAnalysisAI/InferenceX) InferenceX 是世界上唯一同时拥有 TPUv7、NVIDIA 与 AMD、且即将加入 SambaNova 和 Trainium 的推理基准。由于 AgentX 场景非常贴近真实世界的智能体推理工作负载，AMD 也已承诺在 MI455X UALoE72 上与我们展开合作。

![](https://substack-post-media.s3.amazonaws.com/public/images/f583ee2a-b5a3-47d4-b3d4-3fc68181f3e0_2142x1232.png)
*来源：GitHub*

# 智能体工作负载入门

从高层次看，智能体工作负载有四个特征要素：

1. 多轮（Multi-turn）：一个会话包含用户与助手之间数十乃至上百次交互，而聊天机器人场景只有寥寥数次。这类工作负载将长上下文、高预填充（prefill）复用，与子智能体突发调用以及大量工具调用结合在一起。
2. 长上下文：系统提示词、工具定义以及大量的轮次，使上下文迅速累积。
3. 高前缀复用：由于对话线性推进——第 n-1 轮的输出（通常）会被拼接到第 n 轮——大多数上下文可以直接由 KV 缓存提供而无需重算（这取决于可用于存储 KV 张量的存储容量）。随着 n 增大，缓存输入相对未缓存输入的比例通常趋于 1。
4. 子智能体突发：一个会话会启动多个带有全新上下文的短命子智能体，从而造成突发性的 KV 缓存模式。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a6ce1d1-5754-4021-88ca-812789d36bd9_2048x909.png)
*来源：SemiAnalysis、DeepSeek*

关于方法论的更多细节，请参阅我们的 AgentX 文章。

# Rubin 惊人的单位 TCO 性能

单位总拥有成本（TCO）性能是评估 AI 加速器性能最重要的角度之一。在下面的图表中，Y 轴是每 $1 TCO 的总 token 数。**实际而言，这告诉推理服务商：他们在算力上每花一美元能生成多少 token。** 计算方法是将某个场景的总吞吐量除以全包服务成本（$/芯片/小时 乘以 服务所用芯片数）。

在 InferenceX 上，我们为每个 SKU 提供几种不同的 TCO 数字，均来自 [SemiAnalysis AI 云 TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)。默认提供的场景如下：

- **超大规模采购量下的自持（Owning at Large Hyperscaler Volume）**：拥有并运营硬件的每 GPU 小时建模成本，包括按假定使用寿命分摊的服务器与网络资本开支（capex）、托管（colocation）、电力以及资本成本。该场景采用超大规模云厂商的采购与融资条款，包括批量折扣和定制服务器。
- **租赁——3 年期承诺（Rent - 3 Year Commit）**：基于 SemiAnalysis 租金价格调研，向云服务商支付三年期承诺预留的每 GPU 小时市场价格。

用户也可以在我们计算器中编辑算力成本，以匹配其实际支付的价格。[更多数字（例如按需市场租金率和更短期的租赁承诺）可在 AI 云 TCO 模型中找到](https://semianalysis.com/ai-cloud-tco-model/)，该模型来自我们每月对 100 多家 GPU 客户、GPU 新兴云（neocloud）和超大规模云厂商的市场调研。

**在每美元性能方面，Vera Rubin 相比 GB300 是一次实质性的跃升。** 在 170 TPS 下，在同等条件（Apples to Apples）的 TRTLLM NVFP4 Dense 上，采用自持成本假设时，Vera Rubin NVL72 的单位 TCO 总吞吐量约为 GB300 Dynamo TRTLLM 的 67 倍。此外，在多数服务商实际会服务该模型的前沿区间（60-100 TPS），Vera Rubin 的单位 TCO 吞吐量相比最新最强的 GB300 TRTLLM 配置达到 1.4 倍到 3 倍。

我们的机柜采用量产 SKU：每个计算托盘 2300W TDP 和 1.5TB CPU LPDDR5X。[关于 NVIDIA 为何不得不将 Vera 的内存砍半，我们在加速器与内存模型中有更多讨论。](https://semianalysis.com/accelerator-hbm-model/) 本文将讨论 TRTLLM 上的 Rubin 性能，但我们预计后续文章还会涵盖 vLLM Rubin 与 SGLang Rubin 在智能体推理工作负载上的性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac2da106-c1f2-4c85-ab6c-858908f06c05_2048x1322.png)
*来源：SemiAnalysis InferenceX*

Vera Rubin 的最大 P90 交互性比 GB300 Dynamo TRTLLM 高约 61%，分别达到 276.24 与 171.53 P90 TPS。不过，当使用开源的 SGLang 栈时，GB300 可以达到与 Vera Rubin 相当的交互性。

![](https://substack-post-media.s3.amazonaws.com/public/images/ed0a77f0-77a8-4240-885d-6fd85b30f2b5_2048x1322.png)
*来源：SemiAnalysis InferenceX*

我们认识到这是一个早期的 TRTLLM 预发布软件版本，性能只会越来越好，尤其是在前沿的「两端」（超高吞吐量/超低延迟）。推动前沿向前拓展、并着重呈现*随时间推移*的改进，正是 InferenceX 的终极目标。更多内容请阅读我们此前关于 InferenceX 的文章：

另请注意，在更高吞吐量的场景中，Vera Rubin 的 P90 端到端（E2E）延迟也显著更优。虽然交互性（TPS）常常是性能基准的头条指标，但 TTFT（首 token 时间）和 E2E 延迟这类延迟指标同样重要，而且是生产服务中事实上的 SLA 标准之一。

![](https://substack-post-media.s3.amazonaws.com/public/images/e5eb5ea2-fc05-4978-a15a-1a9882d1ba30_2048x1320.png)
*来源：SemiAnalysis InferenceX*

若考虑 3 年租赁成本——2026 年 7 月时 Rubin 超过 $8.5/小时/芯片、Blackwell Ultra NVL72 为 $5/小时/芯片——这次升级依然完全物有所值。在 80 TPS P90 交互性下，Vera Rubin 在相同租赁 TCO 下可多产出 62% 的总 token。在前沿交互性更高的区段，Vera Rubin 每 3 年租赁 TCO 的 token 数最高可达 16 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/850c28c6-035d-45cb-821c-27991c92ac36_2048x1331.png)
*来源：SemiAnalysis InferenceX*

**这里的结论非常简单：** 如果你有钱买或租 VR NVL72，那就应该出手——它生成的 token 将比次优的主流加速器便宜得多，因此也能让你多赚得多得多的钱。正如黄仁勋那句出了名的话所说：「买得越多，赚得越多」。

与单节点 Blackwell 和 MI355X 相比，整条曲线上的单位 TCO 性能差距进一步拉大。**在 80 TPS P90 SLA 下（再说一次，这对该模型而言相当现实），采用自持 TCO 数字时，推理服务商每美元所能服务的 token 数是 B300 的 10 倍。**

![](https://substack-post-media.s3.amazonaws.com/public/images/2b1f8c1b-fc2b-4d2f-8cf8-6c1527e5dd43_2048x1312.png)
*来源：SemiAnalysis InferenceX*

这一优势也延伸到 P90 端到端延迟。如下所示，在自持假设下每 TCO 美元 6000 万 token 的水平上，Vera Rubin 的 P90 端到端延迟约为 20 秒，而运行最新 vLLM 服务栈的 B200/B300 为 60 秒。在每美元 1.6 亿 token 的水平上，P90 端到端延迟差距扩大到约 6 倍：Vera Rubin 为 20 秒，对方为 120 秒。

![](https://substack-post-media.s3.amazonaws.com/public/images/e968ae77-746d-4a8a-9642-b3e25b255896_2048x1325.png)
*来源：SemiAnalysis InferenceX*

在智能体工作负载上，Vera Rubin 让 H200 显得大约和 TI-84 计算器一样有竞争力。在 80 TPS 的 P90 交互性目标下，Rubin 每美元产出的 token 数是 18 倍。在 120 P90 TPS 下，这一优势扩大到 39 倍。Rubin 的优势在离线批量推理上较小，而在训练上更大——这也正是我们看到各大实验室正逐步将 Hopper 迁移过去的方向。

![](https://substack-post-media.s3.amazonaws.com/public/images/96d8a330-0716-4e39-85a5-d74ab3f273ad_2048x1317.png)
*来源：SemiAnalysis InferenceX*
![Texas Instruments TI-84 Plus Graphing Calculator Teacher's Pack of 10 – Underwood Distributing Co.](https://substack-post-media.s3.amazonaws.com/public/images/2f2c6be2-d0ea-4e25-a145-3df3b49c2faa_2000x2000.png)
*来源：Texas Instruments*

# Rubin 单位功耗性能——黄仁勋再度藏拙

可供电数据中心的可用性常常是部署更多芯片的限制因素，因此能效极其重要。如果你能在每吉瓦内生成更多 token，[你就能在每吉瓦内创造更多营收和更多利润](https://semianalysis.com/datacenter-industry-model/)。

[SemiAnalysis 数据中心行业模型](mailto:sales@semianalysis.com)

在 GTC 2026 上，黄仁勋展示了这张在一个大型 2T MoE 模型上比较 Rubin 与 Blackwell 的图，宣称在一个万亿参数模型、约 200 TPS 下，VR NVL72 实现了每 MW 3 倍的性能。但与预发布软件上 Rubin 的真实世界性能相比，我们已经看到每兆瓦 token 吞吐量最高提升至 7 倍。**黄仁勋真该停止在 GTC 上对性能宣称藏拙了**。[上一次是在 GTC 2024 发布 GB200 NVL72 时，他声称它将比 Hopper 快 30 倍，但当我们实测时，它比 Hopper 性能好了 98 倍。](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs?open=false#%C2%A7jensen-under-promising-and-overdelivering-hopper-vs-blackwell-vs-rack-scale-nvl72)

![](https://substack-post-media.s3.amazonaws.com/public/images/fca74ac6-8331-4bd3-abb8-7058f4141ec8_2048x1131.png)
*来源：NVIDIA*

P90 交互性描述的是单条响应的流式速度，取 P90 全响应 token 间延迟的倒数。在固定的交互性目标下，曲线越高，意味着该部署能在相同功耗预算内服务更多总流量。在前述延迟分析中，等待首 token 的初始等待与整体响应时间仍是单独的考量项。

![](https://substack-post-media.s3.amazonaws.com/public/images/424235b9-f3a9-4875-8b91-d0875b715e7f_2048x1279.png)
*来源：SemiAnalysis InferenceX*

对于 DeepSeek V4 Pro 智能体工作负载，在下面比较的匹配目标下，Vera Rubin 每兆瓦的总 token 吞吐量大幅领先 GB300 和 MI355X。优势的大小取决于交互性目标以及用于比较的服务引擎。

在 100 TPS 下，Rubin 约提供 5940 万总 tok/s/MW，相比之下 GB300 Dynamo SGLang 为 2850 万、GB300 Dynamo TRTLLM 为 2110 万。相对该目标下更强的 GB300 引擎，优势为 2.09 倍。MI355X SGLang 达到 201 万 tok/s/MW，使 Rubin 在这一特定工作负载与快照上领先 29.5 倍。SGLang 是该目标下实测 MI355X 引擎中最强的一个。

在 100 TPS 下更宽范围的硬件比较中，B200 SGLang 为 695 万、B300 vLLM 为 556 万、H200 Dynamo SGLang 为 226 万 tok/s/MW。H200 使用 FP8；本比较中的其他配置均使用 FP4。这些是对实测硬件与软件配置的比较，包括各自的缓存与并行策略选择。

下表展示了优势沿曲线的变化情况，吞吐量单位为每电力 MW 的总 tok/s（百万）。这些数值是插值得到的，即在实测基准点之间进行估算，以便在相同速度目标下比较各引擎。N/A 表示该目标超出该引擎的实测范围。

![](https://substack-post-media.s3.amazonaws.com/public/images/13c07f83-d722-466e-bf23-49788022a6d3_1600x900.png)
*来源：SemiAnalysis InferenceX 预览版*

在 150 TPS 下，Rubin 仍保有近 3700 万 tok/s/MW，约为 GB300 SGLang 的 7.2 倍。随着速度要求进一步升高，优势收窄，在 200 时为 2.72 倍。最强的 GB300 引擎也随目标而变：在 75 时 TRTLLM 领先，而在此处展示的更高目标下则是 SGLang 领先。

这一区别在前面讨论过的工作点附近尤其重要。恰好 170 TPS 时，Rubin 每兆瓦总吞吐量是 GB300 TRTLLM 的 62.9 倍——后者的曲线此时已接近其最快实测端点。与相同目标下的 GB300 SGLang 相比，倍数为 5.56 倍。因此，在引用高交互性增益时，标明所用引擎至关重要。

Rubin 的另一大特性是一流的动态功率调度（dynamic power shifting）集成，称为「[DSX MaxLPS](https://docs.nvidia.com/dsx/maxlps/overview)」。这意味着 GPU 集群运营商无需再按最大整体 TDP 外加 10-20% 超订系数来配置供电，而是对其推理工作负载（以及未来工作负载的代理指标）做功耗画像，并根据实际功耗，在同一数据中心电力占用空间内装入更多 GPU。这是因为在推理工作负载期间——尤其是中速到高速档——GPU 并不会消耗满其功耗包络，因此在整个数据中心内智能地调配功率，就能装入更多 GPU。我们即将把 PowerX 集成进 InferenceX，届时将能对每吉瓦吞吐量做更细粒度的测量。

# 每吉瓦年营收与利润——买得越多，赚得越多

撰写本文时，DeepSeek V4 Pro 1.6T 已被 DeepSeek V4.1 Flash 所取代。不过，其规模使其可以充当 O(1-3T) 参数 LLM 的代理。由于 DeepSeek V4 Pro 以 MIT 许可证发布，因此没有许可费用。

在固定功耗预算下，Rubin 的优势不仅在于能处理更多 token。它让运营商无需争取额外的电网电力，就能获得更多将需求变现的容量。在 75 TPS 交互性、60% 稼动率且无模型许可费的情况下，Vera Rubin 每全包电网 GW 每年产生 $159.5B 营收和 $149.9B 建模利润。在这项年营收比较中最强的 GB300 配置 Dynamo SGLang 分别产生 $114.9B 和 $105.3B。因此，在相同电力配额下，Rubin 的营收约多 39%，建模利润约多 42%。

![](https://substack-post-media.s3.amazonaws.com/public/images/05f44b34-7b40-409d-ad6a-015be7cdadbe_2048x1336.png)
*来源：SemiAnalysis InferenceX*

绝对差额约为每 GW $44.6B 的额外年建模利润，按线性缩放折算到 10 MW 规模约合 $446M。由于这两种配置显示的每 GW 年成本相近，大部分增量营收直接转化为模型利润指标。

同样的优势也带来了定价空间。在工作负载组合、吞吐量与可计费稼动率保持不变的情况下，Rubin 可以对缓存输入、非缓存输入和输出 token 全面降价约 28%，同时仍能达到 GB300 Dynamo SGLang 在所示价格下的每 GW 营收。因此，运营商可以将效率收益留作额外利润，也可以用它打价格战，这取决于各模型的需求弹性。

下面我们将讨论每款 NVIDIA 芯片在整个机队生命周期内的总营收。

---
title: "AMD vs 英伟达推理基准测试：谁赢了？——性能与每百万 token 成本"
title_en: "AMD vs NVIDIA Inference Benchmark: Who Wins? - Performance &amp; Cost Per Million Tokens"
subtitle: "MI300X、MI325X、H100、H200、B200、MI355X、vLLM、SGLang、TRT-LLM、ROCm CI 覆盖不足、AMD 租赁价格虚高"
date: 2025-05-23
source: https://newsletter.semianalysis.com/p/amd-vs-nvidia-inference-benchmark-who-wins-performance-cost-per-million-tokens
crawled: 2026-09-15
authors: ["Kimbo Chen", "Dylan Patel", "Daniel Nishball", "Ivan Chiam"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD vs 英伟达推理基准测试：谁赢了？——性能与每百万 token 成本

> 原文：[AMD vs NVIDIA Inference Benchmark: Who Wins? - Performance &amp; Cost Per Million Tokens](https://newsletter.semianalysis.com/p/amd-vs-nvidia-inference-benchmark-who-wins-performance-cost-per-million-tokens) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**MI300X、MI325X、H100、H200、B200、MI355X、vLLM、SGLang、TRT-LLM、ROCm CI 覆盖不足、AMD 租赁价格虚高**

长久以来一直有说法称，AMD 的 AI 服务器在推理性能与总拥有成本（TCO）之比上优于英伟达（Nvidia）。过去六个月，我们通过对英伟达和 AMD 双方推理解决方案的全面分析与基准测试，调查并验证了这一说法。我们原以为会得到一个简单的答案，但结果远比预想更细腻，也更让我们意外。不同任务——例如聊天应用、文档处理/检索和推理（reasoning）——下的表现各不相同。

对于直接拥有并运营 GPU 的超大规模云厂商和企业，我们发现某些工作负载下英伟达的每美元性能（perf/$）更强，而另一些工作负载下 AMD 的 perf/$ 更强。对于从新兴 GPU 云（Neocloud）进行短中期租赁（6 个月以内）的客户，英伟达在每美元性能上总是赢家。这是因为缺少 AMD Neocloud，导致 MI300X、MI325X 的市场租金居高不下。相比之下，在英伟达 GPU 方面，有数百家 Neocloud 提供 H100、H200 等多种显卡，形成了有竞争力的市场租金。

背景信息：AMD MI355X 的定位是 B200 的竞争对手，而 MI325X 被视为 H200 的对手。不过，如下文将谈到的，MI325X 出货延迟，等到它上市时，大多数客户已决定跳过它转而选择 B200。

自 2024 年第三季度起——也就是在 2024 年 12 月我们的[AMD 训练基准文章](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/)之前——我们就一直与 AMD 密切合作。AMD 已采取行动改善其推理解决方案的开发者体验和质量，并添加了一些持续集成（CI）自动化测试。[近 6 个月过去](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/)，我们觉得是时候重新评估了。从我们的测试来看，[尽管 AMD 迄今已有实质性变化](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/)，我们仍认为改进空间很大；我们遇到的问题以及 CI 覆盖不足，将在文章后面讨论。

我们的最终目标是打造一个公开可用的统一仪表盘，每天用最新软件更新，展示多种硬件、多个领先模型在多个关键场景下的推理性能——例如长上下文文档任务、聊天机器人任务、推理任务和智能体工作流。该仪表盘将覆盖多个主流推理栈，包括 vLLM、SGLang、TensorRT LLM，以及未来的 Dynamo 集成。

## 核心要点

1. 对于购买硬件并使用 vLLM/SGLang 的客户，有时单节点 H200 部署的每美元性能（perf/$）更好，有时单节点 MI325X 的每美元性能更好，具体取决于工作负载和延迟要求。
2. 在大多数测试场景中，MI300X 无法与 H200 竞争，绝对性能和每美元性能都更差。而在 Llama3 405B 和 DeepSeekv3 670B 上，MI300X 的绝对性能和每美元性能都胜过 H100。
3. 对于以短中期合同（6 个月以内）租用 GPU 的客户，英伟达 GPU 的每美元性能总是更好，因为只有少数几家供应商提供短中期 AMD GPU 租赁。这造成了人为紧张的市场和虚高的价格。而英伟达生态有超过一百家 Neocloud 供应商提供短中期租赁。充足的供给形成了竞争性市场，压低了成本。
4. MI325X 本应是 H200 的竞争对手，但问题在于 MI325X 直到 2025 年第二季度才开始大规模出货，仅比 HGX B200 出货晚一个季度。这导致其销售不佳，大多数供应商选择了 HGX B200 而非 MI325X。
5. MI355X 将于 2025 年底开始出货，比 B200 出货晚两个季度。
6. B200 和 GB200 的软件仍不完善。例如，FP8 DeepSeek V3 在 TensorRT-LLM（TRT-LLM）、vLLM 或 SGLang 上都尚未完全正常工作。
7. 对于目前能在 B200 上部署的工作负载和模型，B200 占据压倒性优势。MI325 和 H200 在性能上完全无法与之相提并论。
8. 英伟达的 TRT-LLM 推理框架以开发者体验差著称。自 TRT-LLM 发布 PyTorch 后端、以及支持从 HuggingFace 模型字符串用类似 vLLM 的一行 CLI 命令启动服务以来，情况有所改善，但在开发者体验上仍远不及 vLLM 或 SGLang。
9. TRT-LLM 需要增加对 DeepSeek 的完整支持，并提供预构建的 TRT-LLM-serve 容器镜像。
10. 推理服务框架提供了太多配置开关，造成组合爆炸，使全面基准测试几乎不可能。AMD 还通过增加环境变量让情况更糟——尽管我们此前建议移除它们。大多数用户无法获得峰值性能，因为如果不针对每类工作负载做非常深入彻底的扫描测试，就不可能知道该用哪些开关和变量。
11. Anush 和他的团队正在努力让 ROCm 的 SGLang CI 覆盖率达到与英伟达持平，但前路仍长。目前与英伟达的覆盖率持平度还不到 10%。
12. AMD 应利用其雄厚的财务资源，增加内部集群资源的投入。上个季度，AMD 花了 7.49 亿美元回购股票，而内部研发集群资源只投入了约 1300 万美元。研发集群资源的匮乏，是其开发者体验弱于英伟达、以及 AI 软件持续落后于英伟达的关键原因之一。我们认为，哪怕只把可观的回购金额中的一部分转投于此，就能带来好得多的长期股东回报，同时不牺牲回购带来的短期股东满意度。
13. 由于缺少 CI 和数值精度内核，模型在 ROCm 上的各项评测得分不如 CUDA。

SemiAnalysis 正在招聘更多 Member of Technical Staff，帮助我们进一步推进开源基准测试和系统建模工作。这项工作影响力巨大，可获得当前最好硬件资源的支持，并对整个生态产生重大影响。[请在此投递简历及 5 条展示工程卓越能力的要点来申请](https://app.dover.com/apply/SemiAnalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1/?rs=76643084)。我们还在[韩国和新加坡招聘研究分析师](https://app.dover.com/apply/SemiAnalysis/b1e0bb81-dbcd-480b-93b1-6e841ed8bb59)。

我们非常感谢 AMD 和英伟达对我们独立分析的支持。他们在这整个过程中提供的技术支持极为宝贵。我们要特别鸣谢并感谢 Anush Elangovan（AMD AI 沙皇）及其团队，他们对我们上报的各种 bug 进行分诊和修复，并核查我们的结果以确保我们开启了正确的开关（AMD 的开关非常多）。英伟达方面，我们感谢 Ian Buck 的支持，也感谢 Kedar Pandurang Potdar 和 Sridhar Ramaswamy 对我们 bug 报告的分诊、修复和支持。

感谢 TensorWave、Nebius、Crusoe、DataCrunch、CoreWeave 和 Nscale 提供算力，并支持一个能让独立基准测试与分析成为可能的开放生态。

![](https://substack-post-media.s3.amazonaws.com/public/images/1a9535a0-be72-4bb0-b4be-f13f14248943_1311x661.png)
*来源：SemiAnalysis*

## H100 vs MI300X vs H200 vs MI325X vs B200 vs MI355X

推理的解码（decode）阶段往往受内存带宽限制。因此，真正重要的两项系统规格是 HBM 容量和 HBM 带宽。我们可以看到，单个 MI300 节点（HBM 容量 1,536GB）相对 H100 节点（HBM 容量 640GB）有明显优势，因为 H100 甚至无法在单节点内装下 DeepSeek V3 FP8。英伟达在 2024 年第三季度量产 H200 时补上了容量短板——H200 拥有 144GB 显存，而 H100 只有 80GB HBM 容量，并且在我们的测试中性能优于 MI300。AMD 对 H200 的回应是 MI325X，但遗憾的是它上市太晚，客户转而购买了 B200。

![](https://substack-post-media.s3.amazonaws.com/public/images/4645470f-3848-4bd9-ab96-250c30259b73_2560x647.png)
*来源：SemiAnalysis*

MI325X 原定于 2024 年第三季度出货（与 H200 开始出货的季度相同），但由于延迟，它直到 2025 年第二季度才开始规模出货。这使它与 2025 年第一季度开始向客户交付的 HGX x86 B200 SXM 正面相撞。大多数客户决定购买 B200 而非 MI325X，这就是为什么除 Meta 之外，MI325X 没有获得可观的超大规模云厂商出货量。

需要说明的是，生产延迟并非 AMD 独有的问题。英伟达方面，GB200 NVL72 也因 NVLink 背板集成的挑战以及集群运营商缺少可用的背板调试工具而大幅延迟。

## AMD 与英伟达数据中心 AI GPU 的市场份额

自 2023 年第一季度（Q1 CY2023）起，AMD 在数据中心 AI GPU 的市场份额稳步提升。然而 2025 年第一季度（Q1 CY2025），英伟达开启了大规模的 Blackwell 爬坡，而 AMD 对 Blackwell 的回应产品要到 2025 年第三季度才来，因此 AMD 的份额在 2025 年第一季度相应回落。我们预计 2025 年第二季度 AMD 份额将继续下滑。不过，随着 AMD MI355X 今年晚些时候上市以及 AMD 软件的快速改进，我们认为 AMD 有望在今年底或明年初夺回部分份额。

![](https://substack-post-media.s3.amazonaws.com/public/images/e3a4565b-b2d2-43c5-9dc0-a332baabd156_2544x1436.png)
*来源：SemiAnalysis 加速器模型、AMD 财报、英伟达财报*

## 推理基准测试方法论——在线吞吐量 vs 延迟

为了让基准测试尽可能接近真实世界的推理工作负载，我们的推理基准测试方法论强调分析给定配置下的在线吞吐量与单用户端到端延迟的关系，而非基于传统的离线基准测试。离线基准在理想条件下测量吞吐量，不考虑真实世界的延迟影响；与之不同，我们的方法明确刻画了系统并发处理的用户数量与每个用户所经历延迟之间的权衡。通过逐步增加并发用户数，我们测量延迟如何上升，从而得出能直接反映实际运行条件和用户体验的真实吞吐量指标。

我们先解释需要理解的关键指标及其定义。

**吞吐量（Throughput）**衡量给定时间内完成的工作量——例如每颗 GPU 每秒能处理多少 token。吞吐量越高，意味着系统能同时服务更多请求，提升整体容量、效率和收入。

**延迟（Latency）**指完成单个请求所需的时间——从请求发出的那一刻到最终响应交付。延迟越低意味着响应越快、用户体验越好。在我们的框架中，我们关注端到端（E2E）延迟，其定义见下文。

在推理基准测试中，这两个指标相互关联。通过增加并发请求来提高吞吐量，通常会抬高单个用户经历的延迟。这是因为当系统同时处理大量用户时，资源更加紧张，单个请求需要等待更久。反过来，针对低延迟优化往往会限制整体吞吐量，因为同时处理的请求数变少，才能保持快速响应。

理解吞吐量与延迟之间的平衡，对选择正确配置至关重要——交互式应用优先考虑低延迟以获得灵敏的响应体验，而批处理任务优先考虑更高吞吐量，即便单请求延迟因此上升。

**首 token 时间（Time to First Token，TTFT）**表示用户从发出请求到收到第一个生成 token 的初始延迟，反映了对整个输入提示词（prompt）token 进行预填充（prefill）所需的时间。

**输出 token 间隔时间（Time Between Output Tokens，TBOT）**量化了首个 token 生成之后相邻 token 之间的延迟，刻画稳态推理性能。

**端到端（E2E）延迟**的计算公式为：E2E 延迟 = TTFT +（输出序列长度 × TBOT）。它是我们分析用户体验的首选指标，因为它纳入了处理请求时各种来源的延迟。这与一些只比较每 GPU 吞吐量 vs TBOT 的分析形成对比。

![](https://substack-post-media.s3.amazonaws.com/public/images/313082ff-5815-4166-a20b-ca45216f6f34_2504x984.png)
*来源：SemiAnalysis*

传统离线基准忽略了这些延迟相互作用和并发效应，无法建模真实的用户条件，因此产生的吞吐量数字过于乐观，与真实运行环境脱节。当离线基准分析吞吐量 vs 批大小（batch size）时，结果并不准确，因为即使给定批大小下每 GPU 吞吐量相同，不同 AI 芯片的延迟也可能大相径庭。

![](https://substack-post-media.s3.amazonaws.com/public/images/51d56166-93e6-4516-a30b-33e44271510f_2560x1446.png)
*离线吞吐量基准，来源：Signal65*

## 推理基准测试方法论——模型选择

真实生产工作负载中的模型有两大类：稠密（Dense）架构和稀疏混合专家（Mixture-of-Experts，MoE）架构。

稠密模型方面，我们测试了 FP16 精度的 Llama3 70B（作为中等规模 FP16 部署的代表）和 FP8 精度的 Llama3 405B（代表大规模稠密场景）。

稀疏 MoE 模型方面，我们选择了 FP8 精度的 DeepSeekV3 670B。就算术强度、大致的激活/总参数量以及内存访问模式而言，DeepSeekV3 的模型架构与 OpenAI 的 4o/4.1/o1/o3/o4 等前沿闭源模型架构高度吻合。**因此，DeepSeek 是推断 OpenAI 内部模型架构大致样貌的最佳代理模型。**

## 推理基准测试方法论——输入/输出 token 长度

我们对三种不同的输入和输出 token 长度组合进行基准测试，以反映真实的推理场景和性能特征。

第一种是 **4K 输入、1K 输出**的 token 场景。它代表摘要类任务，特征是大规模预填充通用矩阵乘法（GEMM）运算。该场景高度受算力约束（compute-bound），有利于英伟达 GPU 这类在算力密集型预填充上一贯出色的架构。

第二种场景是 **1k 输入、1k 输出** token，与翻译或对话类工作负载高度契合，平衡预填充与解码的性能需求。

最后，我们测试 **1k 输入、4k 输出**的 token 场景。它代表输出大量推理 token 的推理密集型任务，意味着性能通常受内存带宽而非算力约束。评估这三种输入/输出长度场景，可以全面理解模型与硬件在多种推理工作负载下的表现。

随着工作负载演进和数据积累，我们未来会更新这些比例。

## 推理基准测试方法论——推理引擎

在 Llama3 70B 和 405B 的推理基准测试中，我们选择 vLLM 作为主推理引擎。尽管许多用户因性能更好而转向 QWEN，Llama3 仍是用得最多的模型。vLLM 是这些模型采用最广的推理框架，因其优化的性能、易用性和稳健性而得到英伟达和 AMD 双方的背书和积极推荐。在 H200 GPU 平台上，我们除 vLLM 外还评测了 TensorRT-LLM（TRT-LLM）serve。TensorRT-LLM 早期基于 C++ 实现，用户体验历来欠佳；英伟达在 12 月发布了基于 Python 的版本，功能和用法风格与 vLLM 和 SGLang 类似。然而，截至我们最新测试，这个 Python 版 TensorRT-LLM 实现的整体用户体验和成熟度仍落后于 vLLM，尽管持续改进正在缩小差距。为求完整，我们对两种实现都做了基准测试。

有了新的 Python PyTorch 后端、可用一行命令行界面启动推理实例，以及兼容 OpenAI 的 HTTP 服务器，TRT-LLM 的易用性已大幅提升。但它仍存在不少问题——例如 DeepSeek 在 TRT-LLM 上运行不佳，英伟达也尚未发布 Python 版 TRT-LLM-serve 的 Docker 镜像，[导致我们要浪费数小时从源码安装](https://nvidia.github.io/TensorRT-LLM/installation/build-from-source-linux.html)。我们建议 TRT-LLM 团队修复 DeepSeek V3 实现并发布 TRT-LLM-serve Docker 镜像。

![](https://substack-post-media.s3.amazonaws.com/public/images/52b7789b-e48a-4a0a-aedc-301e93b478e8_1654x422.png)
*来源：SemiAnalysis*

相比之下，对于规模大得多的 DeepSeek 670B 模型，我们选择 SGLang 作为推理引擎。SGLang 是 DeepSeek 670B 部署中最常被推荐和采用的推理框架，因能高效处理更大的模型规模以及 DeepSeek 级推理工作负载固有的复杂性，而获得英伟达和 AMD 的强力背书。

## 推理基准测试方法论——并行策略

在我们的基准测试方法论中，会系统评估每种 GPU 架构和测试场景所允许的所有可行张量并行（TP）配置。例如，在测试 405B 模型时，AMD 的 MI300X 同时支持 TP=4 和 TP=8 配置，而英伟达的 H100 由于内存和性能限制，通常只支持 TP=8。对每种并行配置，我们都测量吞吐量和延迟，构建性能屋顶线（roofline）——找出在给定延迟要求下实现最大吞吐量的最优张量并行策略。这种全面的方法确保我们为每种 GPU 平台和模型场景准确确定最高效、性能最好的并行设置。

请注意，我们只测试单节点场景——随着解码/预填充分离（disaggregated decode/prefill，所有主要 AI 实验室都已在生产中使用）的出现，多节点推理已成为事实上的前沿标准。遗憾的是，分离式解码/预填充目前在 AMD 的开放软件栈上尚不可用，只在英伟达的系统上可用。

## 推理基准测试方法论——如何解读数据

解读我们的推理基准数据，应着眼于每美元性能以及各 GPU 类型之间的相对性能。通过微优化（例如为 FP16 模型使用 FP8 KV 缓存，或微调 max-batch-tokens），每一种 GPU 的每个数据点的绝对性能都还有提升空间，但那只是优化单个数据点，而非整条曲线。因此我们建议读者关注各 GPU 类型之间的相对性能，而不是所达到的绝对性能。

另外请注意，在将 H200 与其余 GPU 类型比较时，我们同时提供 H200 使用 TRT-LLM 推理框架和使用 vLLM 的结果。TRT-LLM 性能更强，但开发者体验弱于 vLLM。我们建议同时看 vLLM H200 和 TRT-LLM H200 的数据点，而不是只看 TRT-LLM H200 的性能曲线。

我们的基准测试已发布在 [Docker Hub](https://hub.docker.com/r/semianalysiswork/inference-benchmark) 上，并附上我们使用的 vLLM 和 SGLang 精确版本，以便复现。

## Llama3 70B FP16 吞吐量 vs 延迟结果

![](https://substack-post-media.s3.amazonaws.com/public/images/32dad280-9240-41ae-ae84-bea137bbb33a_2222x1298.png)
*来源：SemiAnalysis*

上图展示了 LLaMA 3 70B 在 1k 输出/1k 输入场景（对应翻译和聊天应用）下的服务结果。可以看到，低延迟场景下 H100 和 H200（vLLM）均优于两款 AMD GPU，但在更大批大小/更高并发下，MI325X 勉强领先并反超英伟达配置。

就张量并行（TP）规模而言，TP=8 统治低延迟场景，而 TP=2 或 TP=4 在更大批大小/高并发时提供最高吞吐量。对 AMD GPU 来说，TP=1 从来不是最优选择，唯一的例外是高并发下的 MI325X。我们认为这是因为高并发时通信量足够大，以至于能看出从 HBM 加载数据与通过 NVLink 传输数据之间的性能差异。MI325X 的 TP=1 数据点展示了高 HBM 带宽的好处。

总体来看，搭配 TRT-LLM 的 H200（记作 H200-TRT）在该基准中大部分区域占优。我们将其归因于英伟达最了解自家硬件，并在性能调优上投入了大量精力。

![](https://substack-post-media.s3.amazonaws.com/public/images/014e51f7-a7cd-484a-9be2-e33d5b8c5414_2560x1297.png)
*来源：SemiAnalysis*

在 LLaMA 3 70B 的类推理工作负载（1k 输入、4k 输出）中，H100 严重落后于所有其他 GPU，每 GPU 吞吐量很快在约 900 token/秒处触及平台期。另一方面，MI325X 比其他所有 GPU 都更晚进入平台期，这意味着在约 450 秒延迟处它拥有最高吞吐量。这也解释了为什么 H200（vLLM）在低延迟区间表现不如 MI325X，但在高并发时能反超。在低于 300 秒延迟的场景下，性能排名（从优到差）清晰如下：H200（TensorRT-LLM）、H200、MI325X、MI300X、H100。

![](https://substack-post-media.s3.amazonaws.com/public/images/911030a8-dc54-4619-b4ef-9f7dc760a243_2478x1408.png)
*来源：SemiAnalysis*

在 LLaMA 3 70B 的类摘要工作负载（4k 输入、1k 输出）中，负载偏重预填充的特性总体上有利于英伟达 GPU。可以看到，延迟超过 30 秒后，H100 反超 MI300X，H200（vLLM）也领先 MI325X。不过，MI325X 的 TP=1 配置在高并发下再次闪光，超越了 H200（vLLM）。搭载 TensorRT LLM 的 H200 依旧无人能敌，从 20 秒标记起在每个数据点都提供最高吞吐量。

## Llama3 405B FP8 吞吐量 vs 延迟结果

![](https://substack-post-media.s3.amazonaws.com/public/images/cc95396d-e3cf-421a-bb4f-cfb3c8e19900_2496x1412.png)
*来源：SemiAnalysis*

在 LLaMA 3 405B 的 1k 输入、1k 输出服务中，大多数配置很快进入平台期。延迟低于 40 秒时，MI325X 和 MI300X 都优于 H100，也（出乎意料地）优于 H200（vLLM）。总体上，MI325X 稳定胜过 H200（vLLM）以及 MI300X 和 H100。在 150 秒延迟约束下，H100 勉强达到 400 token/秒。这显示了内存带宽在服务大型稠密模型时的重要性。

与此同时，搭载 TensorRT LLM 的 H200 再次碾压对手。它在 150 秒延迟内可达到每 GPU 近 1,000 token/秒的服务能力，且在更高并发下没有出现平台期迹象。我们认为这是因为 TensorRT-LLM 对内存使用的控制更好，因此能维持更高的内存利用率并提升性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/85ebc10f-ce06-43da-acd9-9d9089a1aec4_2500x1420.png)
*来源：SemiAnalysis*

LLaMA 3 405B 的推理工作负载（1k 输入、4k 输出）显现了受内存约束的影响。例如，H100 的服务吞吐量不到对手的一半。我们还看到 H200（vLLM）落后于 MI300X，只在高并发（计算量更大）时才重新反超。但这并不足以让 H200（vLLM）与 MI325X 竞争。MI325 在所有场景中都优于 H100、MI300X 和 H200（vLLM）。

搭配 TensorRT-LLM 的 H200 再次展现技术实力，在相近延迟下提供最高 1.5 倍于 MI325X 的吞吐量。这说明 vLLM 远非最优，也解释了为什么 vLLM 把 TensorRT-LLM 视为主要竞争对手。

![](https://substack-post-media.s3.amazonaws.com/public/images/3565374f-ec88-4bb8-9027-6da12e66af1b_2422x1366.png)
*来源：SemiAnalysis*

根据上图可以得出结论：服务大型稠密模型是 AMD GPU 的强项。具体而言，MI325X 在所有延迟场景中碾压对手，MI300X 甚至在约 250 秒延迟处超过 H200（vLLM）。另一边，H100 在约 350 token/秒触及平台，H200（vLLM）在 600 token/秒。与其他情况一样，搭载 TensorRT-LLM 的 H200 王者依旧，在 50 秒延迟标记之后显著领先所有其他配置。

尽管类摘要工作负载偏重预填充，大型稠密模型在这类负载下仍受内存约束，从图中可以清晰看到这一点。

这就是 AMD 选择用 MI300X 和 MI325X 做大模型服务的原因。

## DeepSeekV3 670B FP8 吞吐量 vs 延迟结果

对 DeepSeekv3 670B，我们使用 SGLang 推理框架，测试 H200、MI300、MI325X。我们不测试 H100，因为单节点装不下 DeepSeekV3 670B。

在翻译和聊天应用场景（1k 输入、1k 输出）中，H200 在所有延迟水平上都胜过 MI300X。MI325X 只在 25 到 35 秒这一小段延迟区间内能与 H200 抗衡，其余延迟范围内都是 H200 获胜。在高交互性的低延迟区间，当每个模型副本同时只有 4-16 个并发用户时，H200 是明显的赢家。

![](https://substack-post-media.s3.amazonaws.com/public/images/b52b1ce3-2257-4321-9153-3fb408d475ae_1832x1170.png)
*来源：SemiAnalysis*

在推理测试场景（1k 输入/4k 输出）中，H200 在所有延迟范围内都胜过 MI300。但当延迟超过 100 秒后，MI325X 反超 H200。延迟低于 100 秒时，H200 是明确的赢家。

![](https://substack-post-media.s3.amazonaws.com/public/images/737bf088-ab62-4cdc-993e-f095a6e86ede_2220x1348.png)
*来源：SemiAnalysis*

再看摘要任务场景（4k 输入、1k 输出），H200 与 MI300X 之间还是老剧情——H200 在所有延迟范围内碾压 MI300X。至于 MI325X，延迟超过 25 秒后开始反超 H200。而在更在线化的低延迟用例中，H200 胜过 MI300X 和 MI325X。

![](https://substack-post-media.s3.amazonaws.com/public/images/db40dfd7-17e1-486c-85ae-f1e03ef990d2_2224x1340.png)
*来源：SemiAnalysis*

在大多数应用所需的低、中延迟区间，H200 胜过我们的 MI300X 和 MI325X，因此 OpenAI 等实验室选择了它。

## 每 GPU 每小时 TCO——自持自营集群

在考虑总拥有成本（TCO）时，在 AMD 和英伟达 GPU 之间做选择，需要仔细评估资本开支和持续运营成本。与英伟达的 H100 和 H200 相比，AMD 的 MI300X 和 MI325X GPU 通常总每小时成本更低。

针对每个延迟和模型测试场景，我们以每百万 token 成本为单位计算了每美元性能，以刻画计入总拥有成本后 AMD 与英伟达的表现，如下表所示。请注意，下方的图表基于下表中的 TCO 生成，代表为自己使用而购买 GPU 的客户的总成本，并不代表从 Neocloud 租用 GPU 的租户的成本结构。

在文章末尾，我们将深入分析我们构建资本开支（capex）、运营开支（opex）和 TCO 计算背后的详细财务分析与策略考量。

![](https://substack-post-media.s3.amazonaws.com/public/images/af4815c0-77f8-4527-b5ea-fb96e44bc4c1_2560x445.png)
*来源：SemiAnalysis*

## Llama3 70B FP16 每百万 token 成本

![](https://substack-post-media.s3.amazonaws.com/public/images/e4e922ad-dd19-44a4-948e-80f4458c392c_2236x1306.png)
*来源：SemiAnalysis*

在超低延迟推理下，Llama3 70B 聊天和翻译任务（1k 输入/1k 输出）中，MI325X 和 MI300X 的每美元性能超过所有其他 GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/80788e72-f82c-4a2f-ae4c-db7136572a36_2226x1330.png)
*来源：SemiAnalysis*

把视野拉远、考虑更长的延迟区间后，当延迟大于 20 秒时开始出现价格分化。AMD GPU 的成本效益不如 H100 和 H200（vLLM），但随着延迟增加，凭借高并发下的出色表现，MI325X 变得比 H200 更经济。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b507d6e-c972-431e-8140-52ffab8d3c27_2512x1448.png)
*来源：SemiAnalysis*

转到推理场景（1k 输入、4k 输出），先看低延迟应用：MI325X 和 MI300X 在每 TCO 性能上胜出。

![](https://substack-post-media.s3.amazonaws.com/public/images/444b938e-c5e8-4e7d-9918-c11022970254_2482x1444.png)
*来源：SemiAnalysis*

把分析扩展到更长延迟区间，可以看到在 H100 上服务 LLaMA 3 70B 因性能孱弱而性价比最低。MI300X 和 MI325X 比 H200（vLLM 和 TensorRT LLM）更贵，但在更高延迟下变得更有竞争力。有趣的是，在 MI300X 上服务的成本与 MI325X 几乎相同，说明这种情况下 MI325X 的性能提升配不上它的涨价。

![](https://substack-post-media.s3.amazonaws.com/public/images/f94ab963-8fcb-40a9-880b-072572bcb71f_2478x1436.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/c7a4ef0d-b23c-425e-b954-3f1b1d976eb8_2484x1446.png)
*来源：SemiAnalysis*

摘要工作负载呈现类似趋势。AMD GPU 在低延迟区性价比最高，H100 落后于所有其他配置。H200（vLLM 和 TensorRT）在中延迟区最经济，而 MI325X 的每百万 token 成本降到低于 H200（vLLM），并与 H200（TensorRT）相当。

## Llama3 405B FP8 每百万 token 成本

![](https://substack-post-media.s3.amazonaws.com/public/images/5f82d4e7-fcbf-4d44-af90-323e6c16031d_2496x1442.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/aace9d33-171b-4140-9678-1520d0a71080_2474x1426.png)
*来源：SemiAnalysis*

先看聊天和翻译场景（1k 输入、1k 输出）：AMD GPU 价格更低、服务大型稠密模型性能更强，使成本效率差距更加明显。MI325X 的服务成本持续低于 H200（vLLM）和 H100，MI300X 也与使用 vLLM 的 H200 相当。不过，凭借更强的性能，H200（TensorRT LLM）在 60 秒延迟标记后再次胜出。

![](https://substack-post-media.s3.amazonaws.com/public/images/a87aabe1-1446-45e3-bcbe-780b2ccc33e7_2462x1424.png)
*来源：SemiAnalysis*

对于超低延迟的 405B 推理任务（1k 输入、4k 输出），MI325X 和 MI300X 毫无悬念地击败 H200（vLLM）和 H100（vLLM），甚至击败了 TRT-LLM 上的 H200！

![](https://substack-post-media.s3.amazonaws.com/public/images/7808e0ca-22f2-41ac-b2ee-5f8507bdc5ba_2468x1426.png)
*来源：SemiAnalysis*

再看推理任务场景的更长延迟区间：与此前所有服务大型稠密模型的配置一样，MI300X 和 MI325X 都比 H100 和 H200（vLLM）更具价格效率。但需要注意的是，H200（TensorRT LLM）仍是所有配置中成本效率最高的，因为它带来的性能提升超过了 H200 与 AMD GPU 之间的价差。

![](https://substack-post-media.s3.amazonaws.com/public/images/18ebaa27-0af1-46c1-af40-cbcc944bb1ca_2420x1376.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/78602e26-7442-43aa-96e5-f1d5d6ee7d53_2422x1370.png)
*来源：SemiAnalysis*

转到摘要场景（4k 输入、1k 输出），MI325X 是明显的赢家。低延迟时，MI325X 胜过包括 H200（TensorRT LLM）在内的所有配置，高延迟时也依然有竞争力。MI300X 在高延迟下的成本效率也击败 H200（vLLM），低延迟时接近 H200（TensorRT LLM）。令人意外的是，这一次 H200（TensorRT LLM）虽性能更强，却撑不起它的价格。

## DeepSeekv3 670B FP8 每百万 token 成本

![](https://substack-post-media.s3.amazonaws.com/public/images/b0e0acd2-58af-4d74-bfdf-e5f1b590b193_2234x1456.png)
*来源：SemiAnalysis*

在聊天和翻译任务（1k 输入、1k 输出）中，MI300X 的每美元性能无法与 H200 竞争；MI325X 在 25 到 40 秒延迟区间与 H200 尚有一战之力，但优势不大。每美元性能上这点微小的收益，不值得承受转向并采用 ROCm 的痛苦。

![](https://substack-post-media.s3.amazonaws.com/public/images/bf3e9dd2-6f29-473a-8601-41f28b49e89a_2246x1352.png)
*来源：SemiAnalysis*

在推理任务（1k 输入、4k 输出）中，延迟超过 100 秒后 MI325X 反超 H200——每美元性能最多比 H200 好 20%。但对低延迟/中高交互性场景（即延迟低于 100 秒），H200 依旧轻松获胜。MI300X 在推理任务的每美元性能上无法与 H200 竞争。

![](https://substack-post-media.s3.amazonaws.com/public/images/96afe6f1-0561-42b3-975c-5a51d81c43f4_2216x1334.png)
*来源：SemiAnalysis*

在摘要任务（4k 输入、1k 输出）中，H200 在低延迟/高交互性的每美元性能上获胜。

![](https://substack-post-media.s3.amazonaws.com/public/images/23cf4913-02ba-46dd-ad59-6bda2063a7d9_2224x1336.png)
*来源：SemiAnalysis*

继续看摘要任务的中高延迟区间：MI300X 已能与 H200 掰手腕，而 MI325X 的每美元性能比 H200 好 20-30%。

## 为什么除了超大规模云厂商，没人用 AMD？

上文的每 TCO 性能分析聚焦于直接采购场景——即大型超大规模云厂商或企业直接买断硬件（而非从 Neocloud 租用 GPU）时，AMD GPU 与购买英伟达 GPU 的比较。

一旦涉及租用 GPU，成本结构就完全不同了。相比英伟达，AMD 处于明显的竞争劣势，主要原因是供应有限、市场竞争不足。

目前有超过 100 家 Neocloud 供应商提供英伟达 GPU 的短期（6 个月以内）租赁，价格竞争把租金压了下来。相比之下，只有少数几家提供类似的短期 AMD GPU 租赁。

租赁市场的稀缺性导致 AMD GPU 租金被人为推高，侵蚀了 AMD GPU 的整体成本竞争力。**因此，在租赁市场中，无论延迟要求如何，英伟达的每美元性能始终优于 AMD。**这种失衡解释了为什么除主要超大规模云厂商之外，AMD GPU 的采用寥寥无几——超大规模云厂商通常直接进行长期 GPU 采购，既能利用 AMD 有利的硬件经济性，又不受 AMD 租赁市场价格约束的影响。

## 租金要降到多少，AMD GPU 才能在推理算力租赁市场与英伟达竞争？

[2025 年第二季度，当前 1 个月期合同下 H200 的市场租金约为 $2.5/hr/gpu](https://semianalysis.com/ai-cloud-tco-model/)，波动区间较大，低质量云的价格更低。MI325X 一个月期租赁合同根本不存在，而 MI300X 一个月期合同租金超过 $2.5/hr，这使 MI300X 在租赁上没有竞争力。下面我们计算了 MI300 和 MI325X 的 1 个月租金大约需要定在什么水平，MI300X 和 MI325X 才能与租用英伟达 H200 竞争。

![](https://substack-post-media.s3.amazonaws.com/public/images/2306584e-f271-4454-82c4-279da1ae0be4_1444x944.png)
*来源：SemiAnalysis*

翻译和聊天工作负载（1k 输入、1k 输出）下，MI300X 租金需定在 $1.9/hr 才能与 H200 竞争。MI325X 的 1 个月合同期租金需低于 $2.5/hr 才能与 H200 竞争。

![](https://substack-post-media.s3.amazonaws.com/public/images/87ffefca-6eb3-4ce7-86b5-2539231a8387_1600x954.png)
*来源：SemiAnalysis*

推理类任务（1k 输入、4k 输出）下，MI300X 的 1 个月合同租金需低于 $2.1-2.4/hr，才能与 H200 的每美元性能竞争。MI325 则需定价在 $2.75/hr/gpu 到 $3/hr/gpu 之间（视交互性而定）才有竞争力。

![](https://substack-post-media.s3.amazonaws.com/public/images/1128d01e-3933-4b1d-b019-959e41916f4e_1596x950.png)
*来源：SemiAnalysis*

摘要任务（4k 输入、1k 输出）下，MI325X 的 1 个月合同应定价 $2.75 到 $3/hr，而 MI300X 应定价在 $2.1 到 $2.4/hr 之间。

## B200 性能预览

由于目前软件支持不足，我们没有把 B200 纳入完整的基准测试。撰写本文时，大多数主流推理服务框架对 B200 GPU 尚无稳定支持。vLLM 的标准发布镜像还不支持 B200（[参考](https://github.com/vllm-project/vllm/issues/16336#issuecomment-2893918766)），SGLang 团队也未宣布明确的 B200 支持时间表。AMD 方面，我们没有测试 MI355X，因为量产版尚未就绪。虽然工程样片已经存在，但 bug 还没有完全解决，系统尚不具备测试条件。

虽然 TensorRT-LLM 支持 B200，但只针对一小部分模型做了优化，而这批模型列表中最明显缺少 DeepSeek V3 FP8。因此，我们用 TensorRT-LLM 在选定模型和场景上对 B200 做了基准测试，作为 B200 性能的预览。下图展示 LLaMA 70B 和 405B 在推理工作负载（1k 输入、4k 输出）下的表现。

![](https://substack-post-media.s3.amazonaws.com/public/images/881a9b7e-b324-428e-95bb-a3ec37a18703_2430x1368.png)
*来源：SemiAnalysis*

搭配 TensorRT LLM 的 B200（标记为 B200-TRT）在 LLaMA 70B 基准中全面占优，延迟更低、吞吐量更高。MI325X 和 MI300X 与 B200 的差距悬殊。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ad8e41b-0db7-45e2-bffc-410c2b78cdf3_2186x1214.png)
*来源：SemiAnalysis*

在 LLaMA 405B 上，B200 再次在每个延迟和吞吐量水平上碾压所有其他配置，甚至在我们测试的最高请求速率下仍未到达平台期。

在目前已跑的基准中，B200 展现了极高的性能。为了呈现完整图景，我们将在接下来几个月内发布 MI355X 以及 B200 训练与推理性能的报告。

## 推理过程中的 AMD 与英伟达 bug

基准测试过程中我们遇到了多重阻碍。

推理服务框架里大量的调优开关造成了组合爆炸级的配置数量。例如 vLLM 有 max-num-seq、max-num-batched-tokens、num-scheduler-steps 和 max-model-len；这些配置大多缺乏文档说明各开关对性能的单独影响。这让基准测试极其耗时，也意味着无法保证已找到实现最优性能的正确组合。结果就是，我们只能依靠英伟达和 AMD 的工程师提供他们的最佳配置。我们希望所有服务框架改进每个开关性能影响的文档说明，理想情况下实现自动调优。这件事值得 AMD 和英伟达专门投入 GPU 去做并公开服务。我们乐于合作。

服务框架代码更新速度太快，让我们很难拿到最新的性能结果。即便拿到了最佳配置，一种 GPU 类型的每轮基准测试也要花 60 到 120 小时，而服务框架几乎每周都在更新代码。因为 vLLM 从 v0 到 v1 的切换、[SGLang CUDA Graph 捕获失败](https://github.com/sgl-project/sglang/issues/6033)、[SGLang AMD 段错误（segmentation fault）](https://github.com/sgl-project/sglang/issues/5987)，我们不得不从头开始测试；在被要求重新配置开关时，也多次重启。更糟的是，AMD 多次要求我们启用那些在反馈循环**之间**新开发的功能，导致多轮重跑和软件版本不一致。我们希望未来通过发布实时基准测试网站来缓解这个问题。

基准测试耗时的另一个原因是我们无法跨机器并行实验。我们发现云服务商不同机器之间的吞吐量和延迟差异不可忽略，AMD 和英伟达因此要求我们重做所有实验。

最后，AMD 维护单独的仓库分支（fork）和配置造成了重大延误。由于 AMD 维护着一个独立的 vLLM fork，我们不得不另写一套基准测试设置。撰写本文时，AMD 已收尾并弃用了他们的 vLLM fork。我们欢迎这一改变，也希望 AMD 在其他软件上采取同样的做法。配置方面，他们增加了与 AITER 相关的环境变量，让我们梦回 PYTORCH_TUNABLE_OP 时代。我们已明确表达过对用环境变量启用功能的反感，希望这些变量能像 PYTORCH_TUNABLE_OP 那样被移除。

## AMD 的 SGLang CI 测试缺乏覆盖率对等

过去 5 个月，AMD 的整体持续集成（CI）进步很大。5 个月前，AMD 的 SGLang 推理 CI 为零，现在总算有了一些。遗憾的是，CI 测试覆盖离英伟达还差得很远。

三周前，Anush（AMD AI 沙皇）指派一名硬核工程师[实行 996 工作制](https://en.wikipedia.org/wiki/996_working_hour_system)来修 SGLang CI。AMD 有了一些进展，但遗憾的是仍有数十个单元测试缺失。没有完善的测试，AMD 的软件质量将持续落后、bug 层出不穷，导致更差的开发者体验和更慢的采用速度。

![](https://substack-post-media.s3.amazonaws.com/public/images/7ab425d6-5c96-4722-98ee-add1ec5485f5_1762x1572.png)
*来源：SemiAnalysis、SGLang、GitHub*
![](https://substack-post-media.s3.amazonaws.com/public/images/3d90ceea-bec9-4928-b825-6afd6fa628d2_1862x1548.png)
*来源：SemiAnalysis*

还缺失大量与 DeepSeekv3 相关的多 GPU 单元测试，例如 DP attention、MoE EP 测试等。

![](https://substack-post-media.s3.amazonaws.com/public/images/0eb8aec6-1ecd-41e0-9d1e-ccfede8e2ec0_1862x588.png)
*来源：SemiAnalysis*

## 用 ROCm 跑模型比 CUDA 上「更笨」

在每夜版（nightly）精度方面，直到三周前 SemiAnalysis 指出精度问题之前，AMD 的精度测试数量为零。在大多数模型上，我们观察到 AMD 上的精度表现逊于英伟达。25% 的受测模型在 AMD 上运行时未通过精度测试。

**这意味着同一个模型在 ROCm 上跑，你得到的回答比在英伟达上更「笨」。**

**AMD 需要派更多 996 工程师立即修复这个问题！**

![](https://substack-post-media.s3.amazonaws.com/public/images/e3a0f4f3-3d83-4c56-ae08-ffd4eda829b3_2088x708.png)
*来源：SemiAnalysis、SGLang、GitHub*

## 股票回购 vs 内部集群

2025 年第一季度（Q1 CY2025），AMD 在股票回购上花费约 7.5 亿美元，而我们估计其内部研发租用集群只花了 1300 万美元。尽管 ROCm 软件质量已有巨大改善，但软件质量、开发者体验以及功能完整度仍远不及英伟达。

例如，由于缺乏开发这一优化所需的内部集群级资源，分离式预填充（disaggregated prefill）推理优化至今没有来到 AMD 平台。

我们对 AMD 内部研发预算的估计来自以下事实：AMD 内部约有 4,000 颗 MI300X，他们从超大规模云厂商和 Neocloud 租用的成本为 $1.5/hr。$1.5/hr/gpu × 4000 GPU × 90 天/季度 × 24 小时/天 = 每季度 1300 万美元的研发集群支出。虽然他们在增加投入，但都是通过短期 GPU 租赁，而不是为团队和项目提供长期承诺的集群。

![](https://substack-post-media.s3.amazonaws.com/public/images/2d2a7041-2dc9-49de-9242-2cadddc6c979_2244x1304.png)
*来源：SemiAnalysis*

速度就是护城河。AMD 要想有一线机会，就必须跑得更快、下更大的注。更多内部集群资源将有助于加快内部开发和 CI 支持。

如果 AMD 自己都没有内部试用（dogfooding）、内部也只有 4k 颗 GPU，客户为什么要从 AMD 购买大型集群？他们在 MI325X 上有更大的计划，但这些并未锁定为长期合同，只有短期。

## AMD 缺失分离式预填充推理优化

尽管 AMD 在单节点推理中获胜，但 AMD 目前缺少对许多推理特性的支持，例如分离式预填充、智能路由（Smart Routing）和 NVMe KV 缓存分层。分离式服务已是行业标准多年，上个月英伟达开源了分布式推理框架 Dynamo，进一步普及了这一技术。分离式服务使用独立的计算实例处理请求的不同阶段，包括预填充和解码。

![](https://substack-post-media.s3.amazonaws.com/public/images/d0e50e4b-3fcf-42a2-a278-ad175748a2ad_1024x649.webp)
*来源：北京大学*

此外，英伟达还与 SGLang 合作，把分离式服务带进了 SGLang，而 AMD 的 SGLang 分离式服务根本不存在。由于 AMD 没有分离式预填充方案，英伟达在原始性能和每美元性能上都获胜。

AMD 计划向 LMSys 的 SGLang 维护团队提供一个 16 节点的 MI300X 集群，让他们开始研究合作事宜，并让分离式预填充也能在 ROCm 上运行。我们相信，一个使用英伟达 Dynamo 分支版本的 AMD 分离式预填充原型将在 6 月 12 日的 AMD Advancing AI 活动上演示。

![](https://substack-post-media.s3.amazonaws.com/public/images/4518d3e2-38c1-40f0-9f71-54099b0d1947_2560x1323.png)
*来源：LMSys*

AMD 与英伟达能力的差距还延伸到英伟达 Dynamo 的其他组成部分。

Dynamo Smart Router（智能路由器）在多 GPU 推理部署中智能地把每个 token 路由到可用实例。在预填充阶段，这意味着确保传入 token 被均衡地分发到服务预填充的不同 GPU，避免预填充阶段任何特定专家成为瓶颈。

同样，在解码阶段，重要的是确保序列长度和请求在服务解码的 GPU 之间分布均衡。流量较大的部分专家也可以由 Dynamo 提供的 GPU Planner 复制，以帮助保持负载均衡。

该路由器还能在服务模型的各个副本之间做负载均衡，这是 AMD 的 vLLM 以及许多其他推理引擎所不支持的。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa389642-b4fe-4ab7-8be6-1c82f2f75f8e_1024x611.webp)
*来源：英伟达*

Dynamo 的 GPU Planner 是预填充节点和解码节点的自动扩缩器，会随一天中自然出现的需求波动拉起额外节点。它可以在预填充节点和解码节点上对 MoE 模型中的众多专家实施一定程度的负载均衡。GPU Planner 会拉起额外的 GPU 为高负载专家提供更多算力，还能按需在预填充节点和解码节点之间动态重新分配节点，进一步提升资源利用率。

它还支持调整用于解码与预填充的 GPU 比例——这对 Deep Research 这类场景尤其有用：这些应用需要审阅海量上下文，但只生成相对少量的内容，因此需要的预填充多于解码。

遗憾的是，这一特性目前在 AMD 生态中并不可用。

![](https://substack-post-media.s3.amazonaws.com/public/images/33cc64af-15c3-4e82-ab6a-53135193b1ad_1170x633.webp)
*来源：SemiAnalysis*

英伟达 Dynamo 的 KVCache Offload Manager（KV 缓存卸载管理器）可以把先前用户会话的 KV 缓存保存到 NVMe 存储而不是直接丢弃，从而让预填充整体执行得更高效。

![](https://substack-post-media.s3.amazonaws.com/public/images/b73d568e-6789-4f4f-a6e2-9a2ec1f7ab30_1159x716.webp)
*来源：英伟达*

当用户与 LLM 进行多轮持续对话时，LLM 需要把对话中更早的问题和回答也纳入考量，将其作为输入 token。在朴素实现中，推理系统早已丢弃了当初用于生成那些早期问答的 KV 缓存，这意味着必须重新计算 KV 缓存，重复同一批计算。

而借助 Dynamo 的 NVMe KVCache 卸载功能，当用户离开时，KV 缓存可以卸载到 NVMe 存储系统，直到用户回到对话。当用户在对话中提出后续问题时，KV 缓存可以快速从 NVMe 存储系统取回，免去重新计算之需。

这释放了预填充节点的容量来处理更多流入流量，或者反过来可以缩减所需的预填充部署规模。用户体验也会好得多——首 token 时间更快，因为取回 KV 缓存所需的时间远少于重新计算。

![](https://substack-post-media.s3.amazonaws.com/public/images/d4fc943a-02ba-4aac-a118-5265dbdeb710_1014x683.webp)
*来源：英伟达*

随着 RLVR 和带工具调用的多智能体系统日益普及，这些 KVCache 卸载特性将越来越重要，这也是 AMD 需要探索的另一项关键特性。

除了英伟达 Dynamo，我们还看到越来越多的分布式服务库。例如，SGLang 团队在[复现 DeepSeek 推理系统](https://lmsys.org/blog/2025-05-05-large-scale-ep/)的尝试中，使用 [Mooncake Transfer Engine](https://kvcache-ai.github.io/Mooncake/design/transfer-engine.html) 进行 KV 缓存传输。Mooncake Transfer Engine 是一个高性能、零拷贝的数据传输库。它最初是作为 Mooncake 服务平台的一部分设计的，如今已作为后端插件集成进 NIXL。最近，[Red Hat AI 宣布了 llm-d](https://x.com/RedHat_AI/status/1924801638700568766)——一个 Kubernetes 原生的分布式推理框架，同样使用 NIXL 做 KV 缓存传输。NIXL 走红意味着英伟达 GPU 会获得一流且最新的支持。如果 AMD 不去支持这些开发者，同样的软件碎片化问题将重演。

AMD 工程师需要远比现在多的算力资源，才能探索并实现上述所有推理优化。

## 下一步与未来探索

我们将继续完善基准测试方法论。为此，长期来看，我们计划建立一个自动化定期基准测试的开源仓库（例如用 GitHub CI 每周运行），以跟上服务软件更新的步伐。这将为社区提供可审计的基准测试日志来验证结果。我们已获得多家行业合作方的承诺来支持这项工作。

为了让代理基准越来越接近真实生产工作负载，我们将进一步探索输入/输出序列长度比例，并收集包含多种输入/输出长度分布的多轮推理聊天日志数据集。最后，我们将呈现更多指标，包括首 token 时间（TTFT）、输出 token 间隔时间（TBOT）等。

我们希望本文能成为改进推理基准测试的一次呼吁，我们也乐于与行业伙伴和服务框架开发者合作。

在下文中，我们将对 MI300、MI325X、H100、H200、B200 和 MI355X 的资本开支、运营开支与总拥有成本进行详细分析。

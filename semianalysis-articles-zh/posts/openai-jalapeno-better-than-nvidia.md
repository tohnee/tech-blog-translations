---
title: "OpenAI Jalapeño：比 Nvidia Blackwell 更强"
title_en: "OpenAI Jalapeño: Better Than Nvidia Blackwell"
subtitle: "OpenAI 自研 ASIC 对比 Rubin、Jalapeño 的 TCO、每 MW 吞吐量，以及火辣细节"
date: 2026-08-25
source: https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia
crawled: 2026-09-15
authors: ["Bryan Shan", "Myron Xie", "Jordan Nanos", "Wega Chu", "Clara Ee", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# OpenAI Jalapeño：比 Nvidia Blackwell 更强

> 原文：[OpenAI Jalapeño: Better Than Nvidia Blackwell](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**OpenAI 自研 ASIC 对比 Rubin、Jalapeño 的 TCO、每 MW 吞吐量，以及火辣细节**

过去几年，OpenAI 一直在悄悄打造「Jalapeño」——一颗刚在 Hot Chips 上发布的推理芯片。关于其成功流片的传闻已经流传了一阵子。但现在我们有了细节。OpenAI 邀请我们了解他们的芯片、走进他们的实验室验证其真实成色，并用我们的 [InferenceX](https://inferencex.semianalysis.com/) 套件对它进行了[基准测试](https://openai.com/index/jalapeno-first-results/)。

今年 6 月，[OpenAI 公布了与 Broadcom 合作的芯片项目](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/)，从零开始、专为 LLM 推理而打造。[设计工作始于 2024 年年中](https://newsletter.semianalysis.com/p/openai-chip-team-is-now-serious)，从最初组建团队到制造流片只用了约 16 个月，是极其快速的 ASIC 开发周期。

一般来说，第一代芯片不具备竞争力，但 OpenAI 打破了这一规律，处于行业领先地位，在多个顶级开源模型上击败了我们测试过的每一颗 Nvidia、AMD 和 Google 芯片。OpenAI 靠的是极致的软硬件协同设计。令人惊讶的是，OpenAI 并没有过度专注于模型推理的某个特定环节，而是聚焦于做一颗在所有场景下都交付高性能的通用芯片。

在本文中，我们将深入介绍 Jalapeño 的架构细节、软件细节及其在 InferenceX 上的性能结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/c028f756-4748-4583-91b2-5c4a63893cb5_2048x1153.png)
*来源：OpenAI*

# 一颗通用推理芯片

所有人都说 OpenAI 的芯片专为 OpenAI 模型定制，但这是错的，OpenAI 做的是一颗面向 AI 推理的通用芯片。

这个时间表相当疯狂。它证明「用 AI 加速芯片设计」的说法是真的。撇开速度不谈，OpenAI 花了大把钱，做出了务实的设计决策，而且他们的团队极其强悍，所以这个结果并不令人意外。

只看规格，它一出场就是有力的竞争者：

![](https://substack-post-media.s3.amazonaws.com/public/images/e346a4e5-76cb-4fd9-be95-00321116b605_1846x510.png)
*来源：SemiAnalysis*

而对 HBM4 的使用，让它足以与 NVIDIA 和 AMD 的旗舰 GPU 比肩：

![](https://substack-post-media.s3.amazonaws.com/public/images/327f95f7-ab6b-44ae-9b8f-17c1ff5d296b_1712x1300.png)
*来源：OpenAI*

大量媒体报道跟着 OpenAI 几句随口一说的话，声称这颗芯片将以其他芯片做不到的方式针对他们的模型优化。这是错的。Jalapeño 是一颗通用推理芯片，能跑各种各样的模型和负载，包括我们的基准 InferenceX——我们和 OpenAI 工程师一起在实验室里跑了这个基准。OpenAI 甚至半开玩笑地给我们演示了它运行 Doom——那个游戏只用 Codex 的提示词就移植到了他们的芯片上。

下面是我们的核心 perf/W 结果，按「全计入」（All-in）口径下每 MW 电力对应的 token 吞吐量来看。**Jalapeño 把其他所有芯片都打得找不着北**。这一切都是在不使用多 token 预测（MTP）的情况下做到的，而图上其他芯片都是各自 SKU 表现最好的配置，且全部启用了 MTP。

![](https://substack-post-media.s3.amazonaws.com/public/images/19a7f45a-df8e-436e-ba04-df5d8610f3da_2048x1330.png)
*来源：SemiAnalysis*

Jalapeño 在几乎所有场景下的 perf/W 都胜过 Blackwell，而且没有针对曲线上的任何特定点做调优。它不仅擅长低延迟场景，也擅长高吞吐场景。更公平的比较是对着单 token 预测（Single Token Prediction）结果，此时它把所有对手都远远甩开。在低并发场景下，Jalapeño 展现出惊人的交互性，在 DeepSeek R1 模型上并发为 1 时达到每用户每秒超过 700 个 token。

难以置信的是，这一切都是用单 token 预测（STP）实现的——没有投机解码（speculative decoding），也没有预填充-解码分离。除了 DeepSeek R1，我们还看到了其他一些模型，包括 Kimi-K2.5 和 GPT-OSS，后两者跑到了约 1,400 tok/秒/用户。对所有模型，我们都确认 Jalapeño 的 GSM8k 评测结果与 Nvidia 芯片相当。

这里有几点需要说明。第一，所有数字都由 OpenAI 提供。我们在实验室亲自验证了 InferenceX 的运行，但我们既没有跑完整的 [InferenceX](https://inferencex.semianalysis.com/) 基准套件，也还没有看到 [AgentX](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) 的结果。在比较芯片性能时，我们更偏好 AgentX，因为其数据集的长上下文与多轮对话特性能够反映真实生产工作流的缓存行为。在 8k1k 上表现好的框架，在 AgentX 上可能更差，因为真实生产负载会考验路由器、前缀缓存机制、缓存管理、卸载基础设施等组件，而这些是单轮 8k1k 测不到的。更多内容见我们的 AgentX 文章。

第二，我们认为与 Blackwell 的对比有些不完整、也不太公平。Jalapeño 真正的对手是同样使用 HBM4 的 Rubin 这一代芯片。Vera Rubin 系统眼下正开始交付客户，而 OpenAI 距离拿出 Jalapeño 工程样片之外的东西还需要一段时间。

因此，性能其实应该与 Rubin 而不是 Blackwell 相比，而且在某种意义上，我们本来就预期 Jalapeño 这样的定制芯片会胜过 Blackwell。[正如我们上个月在分析 NVIDIA 与 CoreWeave 联合发布中的性能宣称的文章中所说](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference)，Vera Rubin NVL72 的 perf/MW 是 GB200 NVL72 的 5.4 倍。后文我们会把 Jalapeño 与 Vera Rubin 7 月的性能数字做对比。

第三，被测的模型并不在开源前沿之列。NVIDIA 和 AMD 已用 AgentX 发布了在 DeepSeek V4 Pro 和 Kimi K3 等更大模型上的结果。模型越大、发布越新，在一颗新芯片上把它们跑起来的复杂度就越高。话虽如此，OpenAI 在 Jalapeño 上跑通的这些模型也绝不算小。

# 性能分析

OpenAI 为 perf/W 而设计。原因很简单：OpenAI 当前的瓶颈是数据中心电力，而不是预算或机房面积，因此每 MW 产出的 token 至关重要。在 Computex 2026 上，Jensen 说 perf/W、可靠性和长寿命是未来 GPU 的核心特性。原话是：「如果你有 1 吉瓦电力，那么每瓦吞吐量就是营收」。他还提到，仅仅因为芯片更便宜就选错架构是不明智的。

![](https://substack-post-media.s3.amazonaws.com/public/images/69dc13f6-ffb1-4d56-8df7-b75b57280382_1980x1254.png)
*来源：Computex 2026 主题演讲*

Nvidia 在 Hot Chips 2026 的 Vera 演讲中展示了同一张营收曲线图，并强调了这一点：「如今数据中心受限于电力。」电力举足轻重，直接决定营收。

运营者没法简单搞到更多 MW，因为增加 GPU 与增加电网容量是在完全不同的时间尺度上发生的。数据中心的功耗包络受到公用事业并网、基础设施、散热能力和 UPS/备用发电设计等约束。电网的拖延一再跑赢硬件与建设工期，催生了对 BtM（表后，behind-the-meter）电力容量的需求：建在数据中心现场、就地安装的燃气轮机和自备发电机。这部分容量位于公用事业的电表之后，而不是从公共电网取电。它让运营者无需等待并网和公用事业升级就能给设施供电——这正是 xAI 的 Colossus 2 如此重度依赖 BtM、而其实际电网接入远远滞后的原因。更多信息见我们的[能源模型](https://semianalysis.com/energy-model/)。

正如我们在一条 X 帖子中所写，tok/s/MW 可以约化为每焦耳 token 数，因为一瓦特就是每秒一焦耳。这使得 tok/s/MW 能够代表一个系统的效率，即把能量转化为 token 的能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/c1a1da73-425c-4800-b396-01c7d2151be9_1200x1432.png)
*来源：SemiAnalysis*

在这一项上，即便是与 Rubin 相比，Jalapeño 也是赢家。OpenAI 的 Jalapeño 每 MW 的 STP 输出 token 吞吐量，超过了 [NVIDIA 与 CoreWeave 7 月公布的 Vera Rubin MTP 结果，也远超 GB200 的 2025 年 MTP 结果](https://www.coreweave.com/blog/nvidia-vera-rubin-nvl72-on-coreweave-10x-more-tokens-per-megawatt-than-blackwell)。如我们 Vera Rubin 一文所述，当时 VR 拿来与 2025 年的 GB200 结果对比，是因为两者处于相似的早期 bring-up 阶段，与 2025 年的 GB200 对比可以固定软件成熟度这一变量。沿用这一逻辑，我们对比了 Vera Rubin 2026 年 7 月的最新结果、GB200 2025 年的结果和今天 Jalapeño 的结果。这个对比非常站得住脚：这些是 Rubin 最好的公开数字，而 OpenAI 的芯片流片晚于 Rubin。OpenAI 和 Rubin 都尚未成熟，性能还会继续提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e8f9fd2-ec7f-45fa-80b9-dc132e32c661_2048x1450.png)
*来源：OpenAI、SemiAnalysis*

在 perf/TCO 上，Vera Rubin 与 Jalapeño 不相上下，每美元产出的输出 token 数几乎相同。然而，如前所述，**Jalapeño 的结果是在没有投机解码的情况下取得的**，而 Vera Rubin 的结果使用了投机解码。投机解码可使每 token 成本降低约 3-5 倍。等到 Jalapeño 上实现投机解码后，它将以更低的成本提供 token。当然，这一 TCO 优势有一部分来自把 Nvidia 的高利润率换成了 Broadcom 较低（虽然仍然很高）的利润率。但这并非全部——例如，Meta 和 Microsoft 的 AI ASIC 项目做了更久却始终没成气候，说明成本只是等式的一部分。Jalapeño 的完整 TCO 拆解见 [SemiAnalysis AI 云 TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/a6c58331-c05a-4823-9c4b-aae90705bb53_2048x1485.png)
*来源：OpenAI、SemiAnalysis*

在架构上，OpenAI 选择不把预填充与解码（PD）拆分到不同的芯片池。草稿模型和主模型共享同样的芯片与 fabric，这是一种用部分理论效率换取实际可运营性的设计哲学。动机在于负载构成会随时间变化，比如随着我们走过模型的三个时代（[知识、推理与智能体，参见我们近期的文章](https://newsletter.semianalysis.com/p/are-open-models-catching-up)），输入、缓存写入、缓存读取与输出 token 之间的比例已发生显著变化。因此，预先固定一批异构的预填充硅片和解码硅片，随时间推移可能导致低效。OpenAI 在这一架构中选择同构池，并力图让芯片在所有环节都表现出色。

它确实做到了。在 Kimi K2.5（Cursor Composer 2.5 的基础模型）上，Jalapeño 达到近 700 tok/s/用户，而表现次优的芯片只有 100 tok/s/用户，领先超过 9 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/3088f64c-9bee-46d9-a445-6818248ba573_2048x1366.png)
*来源：OpenAI、SemiAnalysis*

在 GPT-OSS 上，又是一场屠戮。Jalapeño 的等交互性每 MW 吞吐量接近 GB200 最高吞吐点的两倍，是 GB200 并发 1 数据点的 50 多倍。Jalapeño 并发较高的数据点使用了 EP8。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f245dd7-c6b7-48a3-9215-3976633bb77f_2048x1366.png)
*来源：OpenAI、SemiAnalysis*

这些结果令人印象深刻！不过我们还是要挑挑刺：这些只是 8k1k，一种容易调优得多的负载，而且还没有 [AgentX](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) 的运行结果。正如我们在 [AgentX](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) 文中所说，多轮、长上下文负载会考验服务栈多得多的方面，比如路由器和前缀缓存。要在智能体负载上出类拔萃，还需要多得多的优化。详见 [AgentX](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) 一文。

# 深挖规格与架构

所有这些结果都是在 Jalapeño 的 A0 步进上取得的，此时项目才启动 9 个月。但目前已有一款 B0 步进正在晶圆厂里流片！B0 带来的优化使其 perf/W 较早期的 A0 硅片提升约 25%。具体而言，B0 步进在单片光罩极限大小的计算裸片上提供 13.4 PFLOPs 的 MXFP4 算力，采用台积电（TSMC）N3P 工艺制造。作为对比，单片尺寸相近、工艺相同的 Rubin 计算裸片提供 17.5 PFLOPs 的稠密 NVFP4 算力。

考虑到 Jalapeño 的 TDP 仅为 700W，而 Rubin 每计算裸片为 900-1,150W，这个成绩就更拿得出手了。由于 Jalapeño 面向推理而非训练，OpenAI 无需为了最大化 FLOPs 而推高 TDP，这可以理解；但无论如何，上述数字表明 Jalapeño 的峰值理论 FLOPs 相当可观。

与其他加速器直接相比，Jalapeño 的每瓦 HBM 带宽最高，每瓦 FLOPs 也最高，可与 1,800W 的 Rubin Max-Q 配置相提并论：

![](https://substack-post-media.s3.amazonaws.com/public/images/c5795c45-d23b-403c-8bc4-f13d5ba6fb45_2048x394.png)
*来源：SemiAnalysis*

封装外 I/O 由一片 N3E 工艺的 I/O 小芯片（chiplet）提供，带 32 条 800G SerDes 通道，用于计算 fabric：其中 24 条（600GB/s）用于机柜内的本地纵向扩展，8 条（200GB/s）用于全局纵向扩展，即 2,048 XPU 的多机柜域。PCIe Gen 5 用于系统 I/O，连接 x86 主机 CPU。

Jalapeño 将搭载 HBM4 出货，使其成为继 Nvidia 和 AMD 之后相对较早采用 HBM4 的芯片之一，甚至跑在了成熟的 TPU 和 Trainium 项目前面。由于 Jalapeño 背后的关键架构原则之一就是把 HBM 带宽用到极致，任何次于最好的 HBM 的选择都与这一目标相悖。这带来了每封装 15.4TB/s 的内存带宽，超过所有在售的使用 HBM3E 的其他加速器。15.4TB/s 的带宽意味着其 HBM4 能跑到 10Gbps 的引脚速率，略胜 Nvidia 在 Rubin 上从其 HBM4 榨出的 9.6Gbps。这批 HBM 很可能由三星（Samsung）提供。

![](https://substack-post-media.s3.amazonaws.com/public/images/0d7d181a-2bb9-45d4-bd67-2f7e525ce6d1_1426x376.png)
*来源：OpenAI*

OpenAI 于 2025 年 11 月完成了 Jalapeño 的流片——更确切地说，流片的是整个 CoWoS 设计，而不只是顶层裸片硅片。距离 2025 年 11 月那次流片仅 9 个月、实际硅片上的 bring-up 只有 3 个月，OpenAI 就已经用 Jalapeño 交出了非常好的成绩。考虑到该团队的软件栈是从零起步，这就更了不起了。

与此同时，Rubin 的 CoWoS 流片于 2025 年 10 月完成，比它还早一个月，但我们迄今看到的早期结果只有来自 CoreWeave 工程样片的。Nvidia 没有像 OpenAI 那样让我们测试并发布基准，这表明他们的芯片软件尚未成熟。鉴于 OpenAI 能在自家硅片上如此快速地跑通新模型，CUDA 护城河可能已经死了。

双方都远未优化到位，而我们看到总体上 Jalapeño 交出了更好的数字。我们并不认为 Nvidia 硬件不行，更准确地说是 Jalapeño 的软件 bring-up 比 Nvidia 推进得更快。这印证了软硬件协同设计的威力，也是一个强悍的前沿实验室 ASIC 团队能够胜过老牌商用芯片厂商的主要方面。反直觉的是，从零开始可能反而帮了 OpenAI——它可以做出一张白纸式的架构决策，而不必担心向后兼容或旧版本软件。

虽然 OpenAI 手里已有 Jalapeño 的工程样片，但目前计划产量将在 2027 年逐步爬坡，大部分产出目前排在明年年底。[出货量与 ASP 的更多细节，见 SemiAnalysis 加速器模型](https://semianalysis.com/accelerator-hbm-model/)。

可以说，OpenAI Jalapeño 是一颗真正的大批量 ASIC。

与 Rubin 的时间表相比，Jalapeño 的速度快得惊人。如前所示，尽管 Rubin 起步更早，Jalapeño 的成绩仍然胜过 Rubin。

![](https://substack-post-media.s3.amazonaws.com/public/images/bb59cacc-1f16-4c6a-98a5-0f0db74dada7_2048x411.png)
*来源：SemiAnalysis*

## Jalapeño 架构

现在深入架构。这颗芯片的矩阵引擎使用 MXFP 数值格式和权重固定（weight-stationary）的脉动阵列，与 TPU 类似。但与 TPU 直接相比，它支持更小的形状/维度，这意味着它不会像更大的脉动阵列那样，被形状别扭的矩阵乘暴露出奇怪的性能悬崖。

它还有 64 位标量核心和 FP32/INT32 向量核心。OpenAI 也在托盘（tray）层级投入了冗余设计，并在核心级和通道级内置了良率收割（yield harvesting）。他们声称，芯片设计中的 AI 辅助使 SIMD 面积缩减了 8%，矩阵引擎面积缩减了 10%。虽然他们没有说明确切的工艺/电压/温度（PVT）条件，但他们也提到 AI 辅助的模块在时序和功耗上都优于初始版本的模块。

Jalapeño 的架构设计聚焦于消除 KVCache 与权重的数据搬运，以及固定的时延和开销，从而即便在小 batch 或小形状下，也能比其他加速器更接近裸片峰值 FLOPs/带宽。

核心与 HBM 被划分为多个 slice，每个核心 slice 对自己那一部分 HBM 拥有低延迟的本地视图。slice 之间的同步通过一条高带宽的专用集合通信网络完成。这种极简的内存层级已经让 Jalapeño 相对 GPU 拥有了一大潜在优势：GPU 的内存访问必须穿过复杂的内存系统，产生的大时延必须在更大的形状上摊销或隐藏。

这一选择之所以可行，是因为通过精心放置权重和 KV，核心间的同步可以限制在有限的、已知的高带宽通信上，比如可以与计算重叠的张量并行通信。

![](https://substack-post-media.s3.amazonaws.com/public/images/871631ee-8f0d-4fb6-869c-a6fb298e800e_2048x832.png)
*来源：OpenAI*

另外还有一条通用 NoC，负责一般通信以及对纵向扩展网络的访问。总体而言，与 Nvidia 和 Google 相比，OpenAI 用简化的 NoC 和内存子系统省下了大量功耗，并获得了可观的性能收益。

![](https://substack-post-media.s3.amazonaws.com/public/images/1f93df86-2ea2-4904-8fd1-e0e5eff4b410_1638x854.png)
*来源：OpenAI*

在核心层面，OpenAI 描述的是一个带 L1 缓存的乱序执行（OoO）核心。这与其他加速器的设计模式大相径庭——后者全部采用软件管理的暂存存储（scratchpad），并通常搭配某种异步 DMA 支持。这里的论点同样在于：这让 Jalapeño 得以避开栅栏时延（barrier latency）之类的固定开销；而在其他加速器（如 GPU）上，这些开销需要靠每核心更高的工作量来隐藏或摊销，也让人更难逼近裸片峰值带宽/FLOPs。

代价是 Jalapeño 因此依赖良好的预取来保证内存请求及时到达，而这更不可预测、更难推理。不过，让 Codex 处在一个好的执行框架里、又能访问详细的追踪信息，那么为给定形状找到预取策略最优的内核，很可能几乎不需要人工干预。我们认为这正是 OpenAI 能这么快跑通 DeepSeek R1、Kimi K2.5 和 GPT-OSS 的原因。

这些核心还支持「小」矩阵维度，这（取决于到底多小）应该能让它在不同模型和 batch 维度之间更加通用，对矩阵维度对齐、填充开销和分块低效更不敏感。举例来说，TPU、Trainium 和 Etched 的芯片都有非常大的脉动阵列，可能需要大 batch 或恰好可整除的模型维度，才能避免分块低效。

借助 Jalapeño，OpenAI 专注于消除系统中的固定时延，以便在 Pareto 曲线的所有区间都尽可能接近 roofline 性能。理论上，这可以让它在多个工作点上相对 GPU 取得优势：

- 在低延迟/小 batch 推理上高得多的性能上限——在 GPU 上，这受到启动时延、栅栏时延、内存系统时延等许多固定开销的限制
- 即便在大 batch 或长上下文下，也有一定潜力更接近硬件 roofline

但要提醒的是，即便理论上存在性能上限，要在真实内核上兑现它可能更难。所以他们的思路似乎是：

1. 为所有负载形状设计最高的性能上限
2. 让 Codex 去做找到触及该上限的内核这件苦差事

从 OpenAI 团队在 Jalapeño 上跑通 InferenceX 负载的极快速度来看，我们对这一路径持乐观态度。

如果 Jalapeño 成功，它将发出一个强烈信号：业界对编程模型和完美通用编译器的执念，已被前沿 AI 模型作废。

# 软件

OpenAI 像写汇编一样写 Jalapeño 内核。每个内核都有手工调优的代码，有些长达约 3,000 行，并辅以正确性检查和一个自制的 sanitizer。早期的内核工作是人在环（human-in-the-loop）而非全自动，但随着一个规模更大、更内部版的 Codex 出现，这一局面改变了——OpenAI 还计划把这个版本推向企业客户。内部推理引擎名为「Teacup」。有趣的是，**在用 InferenceX 对 DeepSeek 做基准测试之前，OpenAI 内部根本没有 MLA 内核的实现**。Codex 能在没有任何 OpenAI 内核工程师团队介入的情况下如此快速地写出功能正确且高效的内核，展示了这条软件流水线的开发能力。

OpenAI 用 Gluon 给 Jalapeño 编程。Gluon 是 OpenAI 的内核编程语言。它构建在 Triton 之上，保留了 Triton 的 SPMD（单程序多数据）编程模型，但暴露**底层编程抽象**。例如，对 NVIDIA GPU，它提供映射到 PTX 指令的 API，包括 MMA 指令、TMA 指令、mbarrier 机制等等。Gluon 提供的最独特抽象是**布局（layout）**。一般来说，布局定义了硬件资源（如 warp 9 的第 5 号寄存器）与张量元素（如第 6 行第 7 列的张量元素）之间的映射。Gluon 的布局抽象基于 [Linear Layouts](https://arxiv.org/abs/2505.23819)——一种 OpenAI 发明的布局代数。Linear Layouts 从数学上形式化了什么是布局，并提供了对布局进行运算的工具。由此带来许多能力，比如可证明正确的布局转换和最优的内存 swizzling。

就 Jalapeño 的编程模型而言，每个 Gluon 程序映射到一个持久线程。我们认为这暗示 Jalapeño 适合**持久内核（persistent kernel）编程模式**：每个程序在多个 tile 上执行，由程序员而非硬件调度器来分配工作。OpenAI 提到了 TensorInfo，一种显式编码布局的抽象。这很可能就是为 Jalapeño 设计的那套布局，并将由 Linear Layouts 驱动。最后，每个核心提供数据预取和解耦的乱序执行单元。例如，用户可以编程等待某个预取的数据，而它由一个信号量把关。

命运弄人：目前运行在 NVIDIA GPU 上的 GPT 5.6 Sol 等 OpenAI 模型，被用来设计一颗真正威胁 CUDA 护城河的芯片——NVIDIA 自己的 GPU 正在实时帮助迎接它们潜在的继任者。

纵向对比时间，也能看出 Jalapeño 的开发节奏：不到 2 周内，某些交互性点的吞吐量提升超过 2 倍。Jalapeño 团队发给我们的每一个压缩包里都藏着一个奇妙世界。

![](https://substack-post-media.s3.amazonaws.com/public/images/b38d958b-6d53-4ebe-b92f-c2cb58de05c2_2048x1485.png)
*来源：OpenAI、SemiAnalysis*

不仅内核性能在提升：在 8 天时间里，Jalapeño 团队在先前 TP8 配置的基础上启用了 TP32，并走出单系统，让完整的机柜级配置跑通了一个大模型。这样的开发速度实在惊人。

![](https://substack-post-media.s3.amazonaws.com/public/images/a18d5611-f7c1-4e34-8919-99b1c683054f_2048x1485.png)
*来源：OpenAI、SemiAnalysis*

为了在占用真实硬件之前验证性能，OpenAI 还有一个名为「chilisim」的模拟器，使用固定宽度的 trace 总线，精度与实测硬件相差不到 5%。A0 上的追踪能力有限，但在 B0 上已大幅改善，很可能得益于 A0 硅片实际运行的数据。工程师演示了 Codex CLI 运行内部模型（绰号「Raiku」或「5.3 Codex Spark」）达到 1.2ms 的 TPOT。

团队还演示了直接跑在芯片上的 Codex 编写的 demo：36 FPS 的 Doom、一个 FP32 流体动力学模拟，以及一个「Liquid Light」鼠标拖拽可视化。

![](https://substack-post-media.s3.amazonaws.com/public/images/d410878f-5f19-40bd-ad2c-d92ad45d65a9_1252x1232.png)
*来源：SemiAnalysis*

在模型侧，OpenAI 内部的超内核方案（绰号「gigakernel」）围绕单一超内核构建，在设备上循环运行，以降低 CPU 开销和启动时间。团队还在进一步押注测试时计算（test-time compute）策略，内部尤其关注如何有条不紊地使用 100 万次 rollout。

## 分离还是不分离，这是个问题

我们在前文提到，OpenAI 在这些芯片上没有使用预填充-解码分离。这让我们意外，因为即便在同构硬件上，NVIDIA 和 AMD 的 GPU 性能也能从 PDD 中显著受益。我们来挖一挖 Jalapeño 团队为什么走这条路。

当负载固定不变时，预填充-解码分离（PDD）看起来很有吸引力。预填充和解码对硬件的压榨方式不同，因此把每个阶段分配给各自单独调优的资源池，可以在某一个选定的输入/输出比上提升效率。然而，生产流量不会停留在一个比例上。输入与输出序列长度、并发度、缓存命中率、投机接受率、时延目标，全天都在变动。

一旦设备被划分成预填充池和解码池，预填充需求过多会让解码芯片闲置、请求排队；而解码需求过多则相反。运营者必须持续预测正确的配比、在两侧都预留冗余容量，并不断再平衡一个理想比例始终在移动的系统。

在统一系统里，某些资源可能在某个阶段利用不足，但每台设备都随时可用于服务下一个请求。而在分离式系统里，一整颗芯片可能仅仅因为它属于「错的池子」而闲置。局部利用率看着不错，全局利用率却可能很糟。

![](https://substack-post-media.s3.amazonaws.com/public/images/92d363ab-c391-4b9a-9f67-516dac22f534_1364x938.png)
*来源：SemiAnalysis*

分离还破坏了局部性。预填充 worker 产出大块 KV 缓存，而解码 worker 马上就需要它，于是系统必须先把这份状态通过网络传输过去，生成才能继续。这增加了带宽消耗、同步、排队，以及又一个故障域。成本还会随输入序列长度上升，因为 KV 缓存会变大。不过，避免 KV 搬运在很大程度上是一种功耗与时延优化；愿意搬一些 KV，可以换来硬件利用率的提升，代价是一些功耗和单请求时延。

![](https://substack-post-media.s3.amazonaws.com/public/images/5789e0ea-2d0d-4924-b338-f0559c7e7ee9_1928x1292.png)

一个可灵活调配的机群可以在对时延敏感的请求与面向吞吐的 batch 之间调配容量，而固定的切分则会在流量构成变化时困住硬件。此外，上下文长度会改变注意力与 FFN 工作量的配比，使任何固定的硬件比例只在其设计点附近才是高效的。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f3a37f8-0996-4dea-9631-02ade61d7fae_1358x938.png)
*来源：SemiAnalysis*

同样的约束也适用于投机解码。草稿模型必须以极低时延把候选 token 喂给验证模型。把两者拆到专门的池子里，会把一个紧耦合的解码循环变成一个分布式协议。额外的通信与协调可能吃掉草稿模型省下的时延。把两个模型放在同样的设备和低时延 fabric 上，才能保住让投机值得一做的那种局部性。

![](https://substack-post-media.s3.amazonaws.com/public/images/2eb19374-5a08-4d82-84a3-9875b3fc0f5b_1980x1220.png)
*来源：SemiAnalysis*

不过，当需求足够大、稳定且可预测时，分离仍然可以胜出，尤其是当传统 GPU 需要按阶段的大 batch 才能达到较好吞吐量时。但这不是免费午餐。

# 从日本菜到印度菜（从温和到火辣）：Katsu、Vindaloo 与 Chana——这些「咖喱菜」如何拼成一个机柜系统？

在机柜单元层面，Jalapeño 系统由一个 CPU 主机机柜和一个 ASIC 机柜组成。主机机柜容纳 16 个名为「Katsu」（日式炸猪排）的主机 CPU 托盘，与右侧 16 个名为「Vindaloo」（印度超辣咖喱）的 ASIC 托盘一一对应。每个主机搭载两颗 Turin 世代 AMD EPYC CPU、1.5TB DRAM，整个机柜配 2 块 E1.S 和 2 块 M.2 SSD。每个托盘还配备了 400G（2x200G）前端网络。每个 Katsu 托盘通过 8 根外置 PCIe DAC 线缆与对应的 Vindaloo 托盘相连，这些线缆在机柜前部横向敷设。系统级设计与 Celestica 合作完成。

ASIC 机柜由 16 个 Vindaloo 托盘和 8 个纵向扩展交换托盘（6 个本地 + 2 个全局）组成，后者名为「Chana」（鹰嘴豆咖喱）。每个 Vindaloo 托盘包含 8 颗 Jalapeño ASIC，每个机柜合计 128 颗。ASIC 通过铜缆背板连接到每个 Chana 交换托盘，与 Nvidia 的 Oberon 如出一辙。纵向扩展拓扑分为机柜内 128 颗 ASIC 的本地域和最多连接 16 个机柜（即 2,048 颗 ASIC）的全局域。带宽与拓扑的细节我们在下文详述。

旁挂主机柜的供电规划约为 50kW（生产环境 31kW），ASIC 机柜为 130kW，整个双机柜系统合计约 160kW。就功耗而言，这基本相当于一个双宽的 GB300 机柜。

![](https://substack-post-media.s3.amazonaws.com/public/images/596ca531-3bde-44fa-8d1b-34d04b8cc6b8_1304x1382.png)
*来源：SemiAnalysis、OpenAI*

OpenAI 可以在单一纵向扩展网络内连接最多 2,048 颗 Jalapeño XPU。该网络由两个域组成：一个本地域，通过机柜内背板连接全部 128 颗 XPU；一个全局域，通过铜与光的混合互连跨 16 个机柜连接 2,048 颗 XPU。每个机柜有 8 个 Chana 交换托盘。中间的 6 个 Chana 交换机属于本地域，每台搭载一颗 102.4T 的 Tomahawk 6 交换 ASIC。位于这组本地交换机上下两端的 2 个 Chana 交换机属于全局域，我们认为每个托盘可能由 2 颗 102.4T Tomahawk 6 组成，单托盘容量最高 204.8T。

在本地域中，128 颗 Jalapeño 芯片的每一颗都有 4.8Tb/s 的单 XPU 单向带宽，并以全互联（all-to-all）方式连接到 6 颗 102.4Tb/s 的 Tomahawk 6 ASIC。这意味着每颗 XPU 需要约 48 对差分对（DP）公母连接器，折合每个机柜总共 6,144 对用于本地纵向扩展的无源铜缆。

在全局域中，16 个机柜共 2,048 颗 XPU 通过铜背板、电信号的 204.8T TH6 交换机、1.6T 光模块和光路交换机（optical circuit switch）的组合连接在一起。每颗 XPU 的全局链路单向带宽为 1.6Tb/s，对应 XPU 与全局交换机之间背板上每颗 XPU 16 对差分对公母连接器。每个全局交换托盘（各含 2 颗 ASIC）流出的带宽在背板与前面板光口之间分摊。

本地域与全局域加起来，每个机柜的背板连接器数量达到每 XPU 64 对差分对，全机柜合计 8,192 对无源铜缆。

全局域采用纯轨道（rail-only）架构，整个全局域共 8 条轨道。我们认为 OpenAI 通过安装在每个机柜里的配线架来布放全局域的光链路。对每颗 XPU 而言，1.6Tb/s 的全局带宽经铜背板到达全局交换托盘，再经由 1.6T 光模块从交换机前面板引出，先到配线架，再离开机柜。由此，纵向扩展的世界规模（world size）扩大到 2,048 颗 XPU，由 16 个各含 128 颗 XPU 的机柜组成。

![](https://substack-post-media.s3.amazonaws.com/public/images/ae9b26b8-471a-43b2-a60c-cd99ce2b9b07_3480x1342.png)
*来源：SemiAnalysis*

由于纵向扩展网络只占系统总成本的大约 10%，这种灵活性为未来的 10–20 万亿参数模型或 200–400 万 token 上下文窗口买到了宝贵的可选择性。部署方面，OpenAI 正在与新兴 GPU 云（neocloud）合作，并在明年 1 月前与数据中心伙伴持续收集可靠性数据，同时优化从到货到上机柜（dock-to-rack）的部署时间。

# 接下来是什么

接下来我们谈谈 Jalapeño 的未来，它的第一个生产 token 即将到来。下一个目标是 100MW，届时障碍主要在硬件：产能能做多大、数据中心能部署和运营得多好、监控与容灾怎么处理等等。软件已被证明，而只要有内部模型，任何软件先发优势都很容易被追平。付费墙后，我们将讨论这对 NVIDIA、AMD、Cerebras 以及未来几年与 OpenAI 签约的其他芯片公司的影响。

[下一代芯片的产量、出货量与时间表，也收录在我们的加速器模型中](https://semianalysis.com/accelerator-hbm-model/)。

## 对 NVIDIA、AMD 和 Cerebras 的直接影响

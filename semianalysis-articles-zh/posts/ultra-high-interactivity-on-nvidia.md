---
title: "在 NVIDIA GPU 上实现超高交互性？——TileRT InferenceX"
title_en: "Ultra-High Interactivity on NVIDIA GPUs? - TileRT InferenceX "
subtitle: "在 NVIDIA GPU 上运行的 TileRT 软件能否与 Cerebras、Groq LPU、SambaNova 竞争？批大小 1、分离式引擎、高吞吐预填充引擎、高交互性解码引擎"
date: 2026-08-10
source: https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia
crawled: 2026-09-15
authors: ["Bryan Shan", "Daniel Nishball", "Cam Quilici", "Kimbo Chen", "Alec Ibarra", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 在 NVIDIA GPU 上实现超高交互性？——TileRT InferenceX

> 原文：[Ultra-High Interactivity on NVIDIA GPUs? - TileRT InferenceX](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**在 NVIDIA GPU 上运行的 TileRT 软件能否与 Cerebras、Groq LPU、SambaNova 竞争？批大小 1、分离式引擎、高吞吐预填充引擎、高交互性解码引擎**

高定价的「快速模式」正在证明：用户愿意为更低延迟、更快的 token 付费，这有可能带来更高的毛利率。因此，OpenAI 等前沿 AI 实验室正在评估专用推理系统，包括优先追求超高交互性而非最大批处理吞吐的 [Cerebras 和 NVIDIA Groq LPU](https://semianalysis.com/accelerator-hbm-model/)。超低延迟在交互式工作负载中最为关键，包括实时助手和全双工语音。例如 OpenAI GPT‑Live 可以同时听与说，使响应延迟被用户即刻感知，[其体验被形容为像钢铁侠的 JARVIS](https://x.com/OpenAI/status/2080378182469857576)。

GPU 在高吞吐、中低交互性场景下表现极为出色，但其架构并不太适合超低延迟推理。一台 8 GPU 的 HGX B200 服务器提供理论上合计 64 TB/s 的 HBM 内存带宽。在 batch size 1 下，NVFP4 精度的 GLM-5 每生成一个 token 仅需约 21 GB 的激活参数访存量。因此，若按 B200 的 HBM 带宽 roofline（屋顶线）计算，**在不使用投机解码的情况下最高应可达到 3,047 tokens/s/user。而在实践中，GPU 远远达不到这一极限。**

差距源于延迟而非带宽。传统 GPU 编程模型需要启动和同步大量相互独立的 kernel，其启动与收尾开销在超高交互性水平下变得非常可观。虽然在常规服务速度下这些延迟成本不那么显眼，但即使有 CUDA graphs，当 token 延迟逼近亚毫秒级的单 token 输出时间（TPOT）区间时，这些开销就会占据主导。[此外，尽管 GPU 内存带宽每代大约提升 2–3 倍，内存延迟却完全没有改善。](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference)

虽然换用替代硬件很流行，但也有办法用 GPU 做到这一点。这正是 [TileRT 持久化引擎](https://github.com/tile-ai/TileRT)的用武之地。TileRT 将整个解码图静态编译为 NVIDIA GPU 上的单个持久 kernel，最大化计算、内存读写与通信之间的重叠。**在单台 B200 解码服务器的 InferenceX GLM5 FP8 744B 基准测试中，TileRT 已被验证可达 500 tokens/s/user，比运行传统推理引擎的 GB300 NVL72 快约 3 倍。在每输出 token 成本相同（iso-cost）的前提下，TileRT 可以实现比传统引擎快至多 2 倍的交互性。**

我们感谢 TileRT 的维护者们协作完成 TileRT InferenceX 基准测试，也整体上感谢 vLLM 社区在 V1 connector 上的出色设计。TileRT 出自打造了[广受欢迎的 TileLang DSL](https://github.com/tile-ai/tilelang) 的同一社区维护者组织。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

借助 PD 分离（disaggregation）推理技术，高度特化的 TileRT 引擎负责延迟敏感的解码，而 vLLM、SGLang 等吞吐优化引擎继续承担预填充服务。TileRT 解码引擎已投入生产部署：[小米的 MiMo V2.5 Pro UltraSpeed](https://mimo.mi.com/docs/en-US/news/latest/1000tps) 和 [ZAI 的 GLM 5.1 HighSpeed](https://www.tilert.ai/)。

本文将深入解析 TileRT 的 InferenceX 成绩、TileRT 究竟是什么、它如何与现有推理生态组合，以及使用 TileRT 的权衡与挑战。

**我们还将详细阐述在标准 GPU 上使用 TileRT 与使用 NVIDIA Groq LPU、Cerebras、SambaNova 等超低延迟专用芯片之间的权衡**，并评判在 GPU 上运行的 TileRT 软件是否有潜力颠覆这些专用芯片的 TAM。[SemiAnalysis 加速器模型提供对 NVIDIA LPU30、LPU40、Cerebras WSE-3 与 WSE-4 出货量的逐季估算及更多内容。](https://semianalysis.com/accelerator-hbm-model/)

# InferenceX

[InferenceX 是我们的开源、厂商中立、持续更新的 AI 推理基准与研究平台。](https://inferencex.semianalysis.com/)我们在延迟–吞吐帕累托前沿（Pareto frontier）上测量主流模型、推理框架与硬件，追踪现实世界推理性能与经济性随时间的改善。

感谢阅读 SemiAnalysis！本文为公开文章，欢迎分享。

[分享](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[我们的基准已被几乎所有主要算力买家广泛复现、验证和/或支持](https://inferencemax.semianalysis.com/quotes)，从 [Google Cloud](https://cloud.google.com/blog/products/compute/scaling-moe-inference-with-nvidia-dynamo-on-google-cloud-a4x) 到 [Microsoft Azure](https://blog.aks.azure.com/2025/10/24/dynamo-on-aks#enterprise-scale-inference-experiments--dynamo-with-gb200-running-on-aks)、[Oracle](https://inferencemax.semianalysis.com/quotes)、[Meta](https://inferencex.semianalysis.com/quotes) 等等。此外，它还获得了 [vLLM、LMCache、SGLang、PyTorch、Huggingface 等 ML 社区的支持](https://inferencex.semianalysis.com/quotes)，以及 [OpenAI、MiniMax、ZAI、Qwen、Moonshot Kimi 等主要实验室的支持](https://inferencex.semianalysis.com/quotes)。

![](https://substack-post-media.s3.amazonaws.com/public/images/34551ca4-fab9-4df2-a393-dd07cff7cd42_1918x1046.png)
*来源：InferenceX*

[如果你觉得这个开源基准和数据有用，欢迎给 InferenceX 的 GitHub 仓库点星！](https://github.com/SemiAnalysisAI/InferenceX)。[如前文所述，](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference)NVIDIA 已承诺向 InferenceX 提交可验证的 Vera Rubin 数据。我们很快将发布 Google TPUv7 的结果，AMD 也已承诺今年内提交 MI455X UALoE72。

![](https://substack-post-media.s3.amazonaws.com/public/images/eab92435-d677-444d-a608-e36df90e85ac_2048x1098.png)
*来源：InferenceX GitHub*

## 吞吐–交互性曲线

每个推理系统都必须在两个相互竞争的目标之间取得平衡。

- **交互性（tok/s/user）**衡量单个用户接收 token 的速度，即单 token 输出时间（TPOT）的倒数。它决定响应给人的感觉是干脆利落还是迟钝拖沓。
- **吞吐（tok/s/GPU）**衡量系统在所有用户身上总共产出多少 token。它在很大程度上决定了单 token 成本。

批处理（batching）通过同时处理更多请求来提升总吞吐，但每个用户通常要为每个 token 等待更久。小批次则相反：提升单用户速度，同时降低每块 GPU 总体完成的有效工作量。

公交车把成本摊到许多乘客身上，但每位乘客都要为沿途共同停靠的站点等待；赛车只载一两个人、更快到达目的地，但每名乘客的成本高得多。推理面临同样的取舍：批处理改善总吞吐和单 token 成本，小批次改善单用户响应速度。不存在放之四海而皆准的工作点。

在下图所示配置中，将交互性从约 25 提高到 260 tokens/s/user，会使单 GPU 吞吐从约 5,900 降至 200 tokens/s/GPU。也就是说，单用户速度提升 10 倍，换来的是总吞吐约 30 倍的下降。

![](https://substack-post-media.s3.amazonaws.com/public/images/84e4f81e-2e8b-442f-a355-99ccfa905254_1456x954.png)
*来源：SemiAnalysis*

## TileRT 成绩

正如我们在下一节要讲到的，GPU 在高吞吐场景已经表现很好，但在高交互性场景中举步维艰。这一弱点为数据流（dataflow）芯片创造了整整一个细分市场。TileRT 瞄准的正是同一弱点，因此只专注于高交互性工作点。

B200 上的 TileRT 自成一档。在 8k/1k 输入/输出 token 场景下，TileRT 在一个 8 GPU B200 节点上达到 340 tokens/s/user。当前数据集中此前最快的成绩是 GB300 NVL72 在 NVFP4 加 MTP 下的 181.4 tokens/s/user，TileRT 在该指标上快 1.9 倍。当然——这是在 batch size 1 下，此时为 GB300 NVL72 搭建复杂铜背板所付出的那些额外功夫，对提升交互性完全没有用武之地。

与此同时，FP8 最快成绩是 B300 配合 MTP 的 113.6 tokens/s/user，即 TileRT 在同等精度下快 3.0 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/efef9b2d-1932-485d-afb9-f86374241a07_2368x1284.png)![](https://substack-post-media.s3.amazonaws.com/public/images/4f090f1c-aa93-4554-8e41-5bbf1f6108da_2048x310.png)
*来源：InferenceX*

在 1k/1k 输入/输出下，TileRT FP8 达到 494.2 tokens/s/user。这分别是使用 FP4 的最佳传统成绩 256.3 tokens/s/user 的 1.9 倍、最佳传统 FP8 成绩 136.3 tokens/s/user 的 3.6 倍。TileRT 尚不支持 FP4，但它已经在击败非 TileRT 的 FP4 实现！这一结果还值得注意的是，它来自一个 8 GPU B200 节点，而不是 GB200 或 GB300 NVL72 那种 72 GPU 的 NVLink 纵向扩展域。这里的比较针对单用户交互性，而非总吞吐或成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/85ffdd8c-6e1a-4b58-b29d-8aa5b023e6ff_2496x1348.png)
*来源：InferenceX*
![](https://substack-post-media.s3.amazonaws.com/public/images/3ae537c3-de75-4f18-9e0f-be32562eb2ed_2048x290.png)
*来源：InferenceX*

不过——推理永远有权衡！TileRT 的交互性优势伴随的是更低的总吞吐。随着并发上升，传统引擎可以把权重加载和固定 kernel 成本摊到更多用户头上。在 8K/1K 输入/输出下，GB300 FP4+MTP 在并发 12 时的工作点在保持 154 tokens/s/user 的同时交付约 240 总 tokens/s/GPU；TileRT 则在达到 340 tokens/s/user 的同时交付 160.4 总 tokens/s/GPU。

因此取舍是：TileRT 提供高得多的单用户速度，但传统 GB300 工作点在每 GPU 上完成的总工作量更多。截至发稿，TileRT 每个解码节点同一时刻只服务一个在途请求，这使其成为一个刻意特化的工作点，而非通用吞吐配置。于是，在只支持批大小为 1 个用户的情况下，TileRT 不仅仅是一辆赛车，更像是一艘只容得下一名乘客的私人火箭。让 TileRT 支持更多乘客或许有可能，但那是一个雄心勃勃的目标。

[给 InferenceX GitHub 点星](https://github.com/SemiAnalysisAI/InferenceX)

在端到端延迟方面，FP8 的 TileRT 在 1k/1k 上比此前记录的最佳 GLM-5.1 成绩快 4.5 倍，在 8k/1k 上快 3.0 倍。不出所料，TileRT 的首 token 时间（TTFT）不错但并不出奇。决定性优势来自解码尾部：3.01 秒，相比之下最佳 NVFP4 + MTP 竞品为 6.54 秒，MI355X 为 18.18 秒。

![](https://substack-post-media.s3.amazonaws.com/public/images/859e219f-77b1-422f-b1fe-86cae70580ba_2614x1424.png)
*来源：InferenceX*

# 但 TileRT 究竟是什么？

我们简要介绍了 TileRT 做什么、也展示了一些基准结果，但不妨停下来更深入地解释 TileRT 是什么、如何工作。传统服务引擎以接连启动的数千个相互独立的 GPU 程序 kernel 的方式运行。所有这些启动与收尾意味着 GPU 要花掉数量惊人的等待时间——虽然这些启动/收尾时间对中低交互性推理可能无足轻重，但对超高交互性推理（即低延迟推理）绝对举足轻重。更糟的是，每个 kernel 都要把半成品中间结果写到 HBM。在小批大小下问题更严重，因为 kernel 不够大，无法摊薄启动延迟、同步与调度开销。

[如前所述，在 batch size 1 下运行 TileRT 时](https://www.tilert.ai/blog/speed-as-the-next-scaling-law.html)，仅就单台 HGX H200 服务器（合计 HBM 内存带宽 38.4TB/s）而言，MXFP8 精度下每 token 的激活参数内存流量为 42GB。理论上，如果只受内存带宽约束，那么即使不用投机解码，推理也应能达到高达 1,000 tok/s/user 的交互性。现实世界显然不是这样！障碍在于 GPU 的编程与架构模型历来不是为低延迟而生的。[尽管每 GPU 的内存带宽每代提升 2-3 倍，内存延迟却毫无改善——哪怕 HBM 价格还在不断上涨！](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference)

![](https://substack-post-media.s3.amazonaws.com/public/images/e017de5a-1e20-4ac2-8510-582cd0e70533_778x773.png)
*来源：SemiAnalysis、Nvidia*

TileRT 不再连续不断地启动 kernel，而是让 GPU 持续执行一条持久流水线：把整个模型提前静态编译为一个持久引擎 Kernel（Engine Kernel）——主机端只启动一次，执行体在整个解码生命周期内常驻 GPU，大部分运行时编排被移入编译期。

这与 CUDA graphs 不同：CUDA graphs 把 kernel 启动与 memcpy 的 DAG（有向无环图）一次性捕获，然后用一次 cudaGraphLaunch 重放。但那些 kernel 本身仍是相互独立的 kernel，kernel 之间的边界仍带来设备侧开销，且片上状态在每个边界处都会被清空。**CUDA graph 优化的是 kernel 的启动，而 TileRT 干脆取消了 kernel 作为执行单元本身。**

![](https://substack-post-media.s3.amazonaws.com/public/images/a0124db3-2df8-46ff-becd-26a1a433773f_1578x1410.png)
*来源：SemiAnalysis*

此外，通过把工作分解为 tile 级任务并配合 warp 与 block 特化（specialization），运行时以高度重叠的方式动态重调度计算、I/O 与通信。在引擎 Kernel 内部，不同 warp group 承担不同工作：异步数据搬运、张量计算与通信彼此重叠。过去各阶段按 加载 → 屏障 → 计算 → 屏障 串行执行，现在它们在 tile 粒度上重叠，中间结果经由寄存器、共享内存和 L2 向前传递，而不是反复溢写到全局内存。实际上，每个 CTA（Cooperative Thread Array）都变成了一座小型异构工厂，而不是均一的 SIMT（Single Instruction Multiple Threads）工人。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e88cbba-8bac-443c-95cb-e64c0d32a40c_1280x720.png)
*来源：TileRT*

TileRT 引入的下一项优化是把特化扩展到整块 GPU。大多数 TP 框架假定所有 rank 同步执行相同逻辑，但稀疏路由、Top-K 选择、动态索引、长上下文注意力和 MTP 并不适合同构横向扩展；它们计算量不大，却依赖全局信息，强迫每个 rank 都执行它们只会增加冗余工作和同步放大。所以，warp 可以特化，GPU 也可以。在 GLM-5.1 的注意力层中，GPU 0 成为 Sparse Indexer 工人，负责 Top-K 选择、稀疏索引构建与路由，而 GPU 1 到 7 运行 MLA 工人，执行 RMSNorm、GEMM、flash sparse attention 和 AllReduce。

![](https://substack-post-media.s3.amazonaws.com/public/images/842be77f-67b3-418a-8d59-732fc994cedc_849x513.png)
*来源：TileRT*

最后，TileRT 不再把通信当作外部阶段，广播、规约与同步直接在 tile 级流内执行；在 TileRT 下，整个注意力层在主机端只对应一次 kernel 启动，执行模式从 计算 → 同步 → 计算 转向持续重叠的 计算 ↔ 通信 ↔ 计算 流水线。

# vLLM<>TileRT 的 PD 分离引擎

LLM 推理由两个截然不同的阶段组成：预填充（prefill）与解码（decode）。预填充并行处理输入提示词，主要是计算密集型，总吞吐是其关键性能指标。解码按顺序生成 token，并反复访问不断增长的 KV 缓存，因此是内存密集型且对单 token 延迟高度敏感。

![](https://substack-post-media.s3.amazonaws.com/public/images/79985d3a-7cda-4ec2-a7dd-e3c794861f58_1112x548.png)
*来源：DistServe*

TileRT 并不取代 vLLM：vLLM 仍是高吞吐预填充引擎及其外围服务层，包括调度器、分块预填充（chunked prefill）、前缀缓存、OpenAI 兼容 API 和运维工具。只有延迟关键的解码流量转移到 TileRT。TileRT 被设计成一艘单乘客火箭，而 vLLM 仍是飞机、汽车、公交和火车。

[给 InferenceX GitHub 点星](https://github.com/SemiAnalysisAI/InferenceX)

预填充与解码阶段可以分离到不同节点。采用分离（disagg）架构后，一个共享的 vLLM 预填充池可以同时喂给两个完全不同的解码池。

- 池 A：TileRT 超高交互性解码

  - 延迟关键型请求经过 TileRT PD Router，后者指示 vLLM 生成第一个 token，并在 kv_transfer_params 中为请求标记目标 TileRT 节点。
- 池 B：vLLM 解码的通用中低交互性解码

  - 通用流量继续经由 vLLM 原生分离代理进入常规 vLLM 解码池。

![](https://substack-post-media.s3.amazonaws.com/public/images/fab80368-f12c-43d4-b713-158068127bae_1780x1227.png)
*来源：vLLM 与 TileRT*

这通过 vLLM 的 MultiConnector API 实现，把 TileRTConnector 与其原生 connector 组合在一起。TileRT connector 只认领被标记的高交互性流量类别请求，对其余一切请求均为 no-op，这意味着两类流量可以共享同一个预填充服务器。在预填充与解码之间，TileRT 使用 Mooncake Transfer Engine 和 NIXL Transfer Engine 搬运 KVCache。在 TileRT v0.1.5 中，每个解码节点同一时刻只服务一个在途请求。路由器控制分发，并在节点被占用时施加背压（back-pressure）。

感谢阅读 SemiAnalysis！本文为公开文章，欢迎分享。

[分享](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia?utm_source=substack&utm_medium=email&utm_content=share&action=share)

# TileRT 与 Cerebras/Groq/SambaNova 相比如何？

专用推理芯片厂商多年前就发现了同样的执行瓶颈，只是把更多解决方案固化进了硬件。[SemiAnalysis 加速器模型包含我们对 NVIDIA LPU30、LPU40、Cerebras WSE-3 与 WSE-4 出货量的逐季估算。](https://semianalysis.com/accelerator-hbm-model/)

Groq 采用确定性、编译器编排的执行方式和庞大的片上 SRAM 层级。Cerebras 把计算空间映射到晶圆级处理器上；CS‑3 提供约 900,000 个核心、44 GB 片上 SRAM 和 21 PB/s 内存带宽。SambaNova 则把模型图映射到可重构数据流单元上，背后是 SRAM、HBM、DDR 分层的内存系统。

芯片各不相同，但这些系统共享同一思想：延迟敏感的推理受益于减少运行时调度、算子边界、同步以及经由外部内存的不必要搬运。在大批大小下，这些成本更容易摊薄；在 batch size 1 下，它们在每个 token 的延迟中占据的份额要大得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/e5a4d461-66d2-42e1-8cec-ca0c4b5dc73d_2048x1089.png)
*来源：SemiAnalysis*

TileRT 引入了若干数据流思想的软件对应物：AoT（ahead-of-time，提前编译）调度、持久执行、特化工人，以及计算与通信之间更紧密的重叠。这种相似是架构层面而非字面意义上的。TileRT 仍然运行在具有动态硬件调度、HBM 和按模型编译调度方案的 SIMT GPU 上。

[给 InferenceX GitHub 点星](https://github.com/SemiAnalysisAI/InferenceX)

不过，TileRT 终究只是软件：数据流是被强加到一台从未为此专门设计过的机器上的。GPU 带着动态 warp 调度器、SIMT 模型和 HBM 层级，TileRT 的成绩是靠投入巨大的编译器工程——通过静态展开的持久 kernel、手工雕琢的 warp 特化，以及针对锁定（pinned）驱动栈的逐模型编译——说服这套机构去假扮一条空间流水线。原生数据流芯片永远不会与自己的基底作对。专用加速器把更多执行模型固化在硬件里，可以避免一些 TileRT 只能靠软件掩盖的开销。它们的优势仍取决于模型、精度、内存层级、编译器质量、系统规模和服务配置。这正是为什么 Cerebras 服务稠密 70B 模型的速度是任何 8 GPU 节点无论如何调度都达不到的：软件可以逼近 HBM roofline，但抬不高它。

![](https://substack-post-media.s3.amazonaws.com/public/images/d5181aa5-0273-418f-8ee8-e90e2b1f7beb_2048x1217.png)
*来源：SemiAnalysis*

市场初期的答案是：纯粹性可以商量。TileRT 的解码引擎已经在小米 MiMo V2.5 Pro UltraSpeed 和 Z.ai 的 GLM-5.1 HighSpeed 背后投入生产，部署模式本身就说明了问题。两家公司都没有采购新的数据流芯片。他们从自己已在运行的加速器集群里切出了一个速度档位：vLLM 继续负责预填充、调度和 API，TileRT 在同一端点背后接管解码。在已经拥有的硬件上「够好」，往往胜过在必须购买的硬件上「架构纯粹」。

**这指向一个更深层的结构性问题：预填充–解码（PD）比例的可互换性与灵活性。**

GPU 池是一种单一的可流动资源：精于预填充、精于中大批解码，[如今在超高交互解码上也有了相当可信的实力](https://mimo.mi.com/docs/en-US/news/latest/1000tps)，容量在这些角色之间的转移只是软件调度器的决定，可以逐小时跟随需求。ASIC 机队恰恰相反：速度档容量与其他容量的比例，在采购订单签署那天就固化在硬件里了。要改变物理机队的比例，需要数月时间重新上架、重新布线。如果工作负载构成稳定且已知，这没什么问题。不幸的是，在估算需要普通对话级延迟的用户与愿意为极致交互性 SLO 付费的用户（越来越多是智能体）之间的比例时，牵涉的变量非常多。用 GPU 猜错了，用软件重新平衡即可；用专用芯片猜错了，你要么把资本闲置在空闲的速度机器里，要么把当初为之买进来的那批高价值流量拒之门外。雪上加霜的是——需求会随时间变化，所以猜对了也只在有限的时间段内是对的。

回到前面提到的共享预填充池：服务商不需要为全部流量支付 TileRT 的溢价。一般请求可以留在吞吐优化的 vLLM 或 SGLang 解码池，只有延迟关键型请求才路由到 TileRT 解码池。

![](https://substack-post-media.s3.amazonaws.com/public/images/5bf63cd1-c7e5-44a9-bd4e-682c52cfa2e9_1594x1078.png)
*来源：SemiAnalysis*

这一切并没有杀死速度市场的顶端。SRAM 的 roofline 仍然更好，某些规模的模型仍然偏向它，也总有一些工作负载不计代价地想要最大每秒 token 数。但 TileRT 重新框定了大多数买家需要的东西：不是一台速度机器，而是一个速度档位——从他们反正要拥有的机队中动态划分出来。Cerebras、Groq、SambaNova 不再是与一个笨拙的 kernel 启动器竞争，而是在与它们自己的执行模型竞争——那个执行模型跑在可互换的硬件上，靠一份配置文件完成重新分配。TileRT 或许是一艘单乘客火箭，但它让服务商可以直接给自家城际巴士绑上固体助推器，而不必设计一艘全新的运载火箭。

## 为什么 TileRT 开发缓慢？

GLM5.1 已落后一代，在 InferenceX 主线上已被弃用。TileRT 的模型目录非常有限，目前支持 GLM-5/5.1 和 DeepSeek-V3.2。MiMo-V2.5-Pro-UltraSpeed 是联合设计合作的成果，尚未开源。

TileRT 继承了 ASIC 厂商最大的弱点。静态提前编译意味着极小的模型目录（目前是 GLM-5/5.1 和 DeepSeek-V3.2）、硬性锁定的依赖，以及每种新架构都需要实实在在的工程投入。不存在完全通用的路径——持久引擎 kernel 意味着模型要提前静态展开成一个常驻程序，因此必须就 tile 形状、流水线深度、缓冲在寄存器/共享内存/L2 间的驻留、warp group 在加载/计算/通信之间的分工、集合通信融合进 tile 流的位置，以及哪些 GPU 承担特化角色（比如 GLM-5.1 专属的 sparse indexer rank）逐一做出决定。注意力机制或路由方案一变，这套调度的大部分就作废了。数据流芯片同样面临这个问题——优秀的编译器向来出了名地难做。

[分享 SemiAnalysis](https://newsletter.semianalysis.com/?utm_source=substack&utm_medium=email&utm_content=share&action=share)

业界正在努力简化这些工作，尤其是因为软件开发可以用 AI 加速。[TileOPs](https://github.com/tile-ai/TileOPs) 旨在减轻这一负担。每个算子都在一份机器可读的 manifest 中声明，其中规定其签名、工作负载和 roofline 模型。这份 manifest 驱动代码生成、测试，以及面向硬件极限而非仅仅面向早期实现的基准测试。

AI 编程智能体可以加速已知模板内的调优，但新颖的变换仍需要专家判断。单体式持久 kernel 也削弱了传统按 kernel 划分的 profiler 时间线的用处，使自动化反馈回路更难构建。

# TileRT<>InferenceX 的下一步

我们正在积极推进把 TileRT 基准测试从 InferenceX 的单轮 8k/1k 迁移到我们的新智能体编程基准 AgentX 上。该场景重放真实的 Claude Code 与 Codex 轨迹，包含长上下文、多轮请求、真实的子智能体活动和动态的工具使用延迟。其输入长度中位数为 140k token，而理论缓存命中率中位数 roofline 达到 99.2%。

![](https://substack-post-media.s3.amazonaws.com/public/images/9d1d6223-50bf-4f33-a87c-d44fce6604e3_2048x1654.png)
*来源：SemiAnalysis*

这一工作负载将考验整个 TileRT<>vLLM 系统，而不仅是解码速度，包括增量 KV 传输、前缀缓存复用、缓存保留与卸载、路由和调度。关键问题在于：TileRT 能否在轮次之间只传输新引入的上下文，同时保住其超高交互性优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/1b7a5496-b564-4bf0-830f-8cf2dd7f1bed_2048x1364.png)
*来源：DeepSeek*

第二步是走出 batch size 1。我们还将在 batch size 2、4、8 下对 TileRT 进行基准测试。目标是为它的吞吐–交互性帕累托前沿画出完整地图，并找出持久引擎 Kernel 延迟优势开始走平的拐点。

# TileRT 超快速度档的性能/TCO 比

接下来，我们深入分析 TileRT 在超高交互性下每百万输出 token 的成本，并与常规较低交互性工作点的解码对比。结果相当有趣：与传统引擎等成本（iso-cost）时，TileRT 的交互性最高快 1.9 倍。[我们以我们的 AI TCO 模型作为各芯片 SKU 资本开支与运营开支的基线。](https://semianalysis.com/ai-cloud-tco-model/)

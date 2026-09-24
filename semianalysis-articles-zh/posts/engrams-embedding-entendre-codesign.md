---
title: "Engram 嵌入双关：面向高效 DRAM/SSD 卸载的协同设计"
title_en: "Engrams Embedding Entendre: Codesign for Efficient DRAM/SSD Offloading"
subtitle: "新模型架构对 DRAM/NVMe TAM 的影响：DeepSeek V4.1 Flash、AgentX、InferenceX、NVMe 实验"
date: 2026-09-18
source: https://newsletter.semianalysis.com/p/engrams-embedding-entendre-codesign
crawled: 2026-09-15
authors: ["Bryan Shan", "Cam Quilici", "Alec Ibarra", "Kimbo Chen", "Myron Xie", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-23
---

# Engram 嵌入双关：面向高效 DRAM/SSD 卸载的协同设计

> 原文：[Engrams Embedding Entendre: Codesign for Efficient DRAM/SSD Offloading](https://newsletter.semianalysis.com/p/engrams-embedding-entendre-codesign) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**新模型架构对 DRAM/NVMe TAM 的影响：DeepSeek V4.1 Flash、AgentX、InferenceX、NVMe 实验**

Engram 用学习得到的多 token 查找对标准 token 嵌入（embedding）进行了扩展。反复出现的局部模式可以直接检索到向量，从而减少通过注意力和前馈层重建这些向量的需要。

**借助 Engram 模型架构优化，同等质量的模型所需的 HBM 容量得以降低。**[这并不意味着 HBM 不会出现疯狂的需求，只是说明模型架构将继续围绕约束条件不断创新。](https://semianalysis.com/memory-model/)

这一模型架构设计天然适合与参数卸载（offloading）协同设计：每个 token 访问少量嵌入行，这些行的地址取决于 token ID，而非隐藏状态（hidden state）。运行时可以在前面各层计算的同时，从主机 DRAM 预取这些行，从而把表放在 HBM 之外，又不必搬运整个权重矩阵。[我们的 Memory 模型包含我们对 HBM、DRAM 与 NAND 逐季度供需的最新估算。](https://semianalysis.com/memory-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/fa5373b8-e5c4-4254-b899-1195ac27e1a7_2048x769.png)
*来源：SemiAnalysis*

**卸载把 HBM 腾出来给模型权重和 KV 缓存，**从而可能支持更大的 batch 或更多并发会话。当 DRAM 成为下一个约束时，NVMe 提供了再下一层存储。推荐系统早已把高频或近期访问的嵌入行缓存在更快的内存中，而较冷的行则由 SSD 承载。[在 NVIDIA 因大幅削减规格——把 Rubin Ultra 从每芯片 1024GB HBM 降到如今约 ~200GB——而被迫调整路线图之后](https://semianalysis.com/accelerator-hbm-model/)，Engram 之类的模型架构优化或许能派上用场。

我们的 DeepSeek-V4.1-Flash 配置为 Engram 使用了约 189 GiB 内存。我们将其替换为一个内存映射（mmap）文件，并测量卸载到 SSD 之后的服务性能。

在报告的后文中，我们将展示 Engram 卸载实验，以及 [InferenceX 官方在 DeepSeekv4.1 Flash 等 Engram 模型上的智能体推理服务成绩，覆盖全部 6 款 NVIDIA GPU SKU 以及 MI355X。](https://inferencex.semianalysis.com/inference/deepseek-v41-flash) 毫不意外，在超人气模型 DeepSeekV4.1 Flash 上，CUDA 护城河依旧全面碾压 MI355X。

**我们还展示了：即便在大容量 HBM 的 SKU 上，把 Engram 卸载到 DRAM 在帕累托前沿（pareto）的大部分区间也能取得比把 Engram 留在 HBM 更好的性能。**

[我们的基准测试已被几乎所有主要算力买家广泛复现、验证和/或背书，](https://inferencemax.semianalysis.com/quotes)从 [Google Cloud](https://cloud.google.com/blog/products/compute/scaling-moe-inference-with-nvidia-dynamo-on-google-cloud-a4x) 到 [Microsoft Azure](https://blog.aks.azure.com/2025/10/24/dynamo-on-aks#enterprise-scale-inference-experiments--dynamo-with-gb200-running-on-aks) 再到 [Oracle](https://inferencemax.semianalysis.com/quotes)、[Meta](https://inferencex.semianalysis.com/quotes) 等等。此外，它还得到了 [包括 vLLM、LMCache、SGLang、PyTorch、Huggingface 在内的 ML 社区的支持](https://inferencex.semianalysis.com/quotes)，以及 [OpenAI、MiniMax、ZAI、Qwen、Moonshot Kimi 等主要实验室的支持](https://inferencex.semianalysis.com/quotes)。

![](https://substack-post-media.s3.amazonaws.com/public/images/33218ee5-8a7a-4fc6-962d-ef25f5005f72_1456x504.png)
*来源：InferenceX*

[如果你觉得这套开源基准测试和数据有用，欢迎给 InferenceX 的 GitHub 仓库加星！](https://github.com/SemiAnalysisAI/InferenceX) InferenceX 是世界上唯一一个覆盖 TPUv7、Jalapeño、Nvidia Rubin NVL72、AMD，且很快将加入 SambaNova 和 Trainium 的推理基准。由于 AgentX 场景对真实世界智能体推理工作负载的还原度极高，AMD 也已承诺在 MI455X UALoE72 上展开合作。

![](https://substack-post-media.s3.amazonaws.com/public/images/07c3ee14-7d6d-486b-b9cd-36aec3f971b7_1456x837.png)
*来源：SemiAnalysis*

# Engram 的收益

DeepSeek 并未放出原论文训练的那两个 Engram 模型。我们使用其公开的代码和训练超参数，在 fineweb-edu 上复现了该设置，估算每次训练约 6E18 FLOPs。我们观察到了相同的 U 形扩展规律：

![](https://substack-post-media.s3.amazonaws.com/public/images/6ec98796-a8c4-4cf8-9065-e9397c59fca1_1034x752.png)
*来源：SemiAnalysis*

相比纯 MoE 基线，Engram 带来了性能提升。我们还复现了 DeepSeek 的结果：加入 Engram 后，较早层的表征与较晚层的表征相似。

![](https://substack-post-media.s3.amazonaws.com/public/images/27447880-e621-4b06-8f26-79773780be2f_2272x1348.png)
*来源：SemiAnalysis*

# 被记住的到底是什么？

与 Engram 原论文一样，可以通过探测 Engram 的门控分数（gate score）来看 DeepSeek-V4.1-Flash 最常使用哪些 n-gram。我们的门控扫描发现了人名、代码片段、关系型措辞和样板文本。这些示例的挑选以趣味性优先、而非门控强度。

🔗 [[嵌入内容]](https://datawrapper.dwcdn.net/sw8uZ/5/)

一个出人意料的结果是 `Wright : Ace Attorney`。

![](https://substack-post-media.s3.amazonaws.com/public/images/0160b80e-a48a-4e36-9895-494f7ce158ba_1290x1080.png)
*来源：SemiAnalysis*

这些示例表明，学习得到的记忆优化的是训练目标，而不是在对「哪些事实值得存储」做判断。许可证、参考文献片段、API 脚手架和网页装潢都能提供预测捷径，因此额外 Engram 容量的价值可能取决于数据准备之后留下了什么。这并不说明表容量被「浪费」了：对评估语料库的扫描既无法确立训练时是否接触过这些内容，也无法确立各类内容分别占用了多少容量。

对卸载而言，高门控分数并不能识别缓存热行；低门控分数也不会自动省下读取：计算门控本身需要先取回 key，这会抵消融合 kernel 带来的性能收益。要想跳过读取，需要在检索之前有一个独立的有用性预测器。

# 移除 Engram

在[原论文的推理时消融实验](https://arxiv.org/pdf/2601.07372#page=17)中，事实知识类基准只保留了原有性能的 29–44%，而阅读理解类保留了 81–93%。这是训练与推理不匹配所致。因此，由此产生的性能退化衡量的是这个已训练模型对 Engram 的依赖程度，而非「用 Engram 训练」与「不用 Engram 训练」的模型之间的性能差异。

![](https://substack-post-media.s3.amazonaws.com/public/images/c292051e-b694-4612-9ee9-9e9b768d214f_1422x592.png)
*来源：DeepSeek*

在我们自己的消融实验中，压制 Engram 会在所有评估领域恶化 token 似然（likelihood），尤其是百科文本和若干代码语料。令人惊讶的是，GSM8K 准确率保持在测得的逐次运行波动范围之内，移除 Engram 没有产生影响。

Engram 并不是在一套原封不动的 MoE 旁边挂一本随手可拆的字典。移除它会改变下游特征和专家选择。

我们检验了重新路由（rerouting）究竟是有害还是补偿性的：在 CRUXEval 上做一个固定 token 的 teacher-forcing 实验，并对参考答案打分。CRUXEval 是一个由小型 Python 函数组成的代码推理基准，模型需要根据函数代码和一个输入预测函数的输出。

![](https://substack-post-media.s3.amazonaws.com/public/images/3d87e40d-2115-4d9e-9f8a-cbda552cd7f7_2126x696.png)
*来源：CRUXEval*

移除 Engram 使答案损失从 0.2848 升至 0.3093 bits/token。而强制消融后的模型沿用原始（Engram 开启时）的专家选择，结果更糟，达到 0.3375 bits/token。

![](https://substack-post-media.s3.amazonaws.com/public/images/e728edcc-e684-41c7-99f3-3de66b76d1ff_2048x841.png)
*来源：SemiAnalysis*

重新路由部分补偿了缺失的记忆。记忆特征与专家选择是协同工作的，而不是遵循「记忆存事实、专家做推理」这种泾渭分明的分工。

在同一个 CRUXEval 上，无论在哪个阶段移除 Engram，准确率都会下降、生成 token 数都会增加；全程移除的变化最大。

![](https://substack-post-media.s3.amazonaws.com/public/images/477584e8-1f01-4e67-90b4-a8f60d3b3b09_2048x666.png)
*来源：SemiAnalysis*

只在预填充（prefill）阶段保留 Engram 比只在解码（decode）阶段保留能得到更多正确答案，原因很可能是传给解码 worker 的 KV 缓存语义更丰富，从而缓解了一部分性能损失。

# 智能体推理服务性能

Engram 的表很大，但每次查找很小。DeepSeek-V4.1-Flash 在两个 Engram 层各请求 24 行，折合整个模型每个被处理的 token 位置约 12.4 KiB；拆分到 4 块 GPU 时，每块 GPU 约 3.1 KiB。

![](https://substack-post-media.s3.amazonaws.com/public/images/d3a4f36c-e9fd-4574-96dc-d26a0057bc07_1984x1602.png)
*来源：InferenceX*

截至模型发布后第 7 天，即使按 MI355X 更低的总拥有成本（TCO）归一化，MI355X 的每美元性能仍比 B200 差 2-4 倍。[我们完整的总拥有成本拆解来自我们的 AI Cloud TCO 模型，以及对 100 多家 GPU 云和 GPU 云客户的月度市场调研。](https://semianalysis.com/ai-cloud-tco-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/41711275-ca52-465c-8099-f8db46c916e3_1772x1602.png)
*来源：InferenceX*

在 DeepSeekv4.1 Flash 发布当天（Day 0），NVIDIA vLLM 在全部 6 款 SKU——H100、H200、B200、B300、GB200、GB300——上开箱即用、零问题！这要归功于 NVIDIA 与 Interact 团队的出色工作！相比之下，AMD vLLM 在发布当天无法运行 DeepSeekv4.1 Flash。来源：SemiAnalysis InferenceX

![](https://substack-post-media.s3.amazonaws.com/public/images/aef38cf0-904e-49b8-b45f-944f19793e84_1786x1434.png)
*来源：InferenceX*

AMD 的 vLLM 文档指向使用 vllm/vllm-openai-rocm:deepseekv41-flash-0909，但从模型发布的第 0 小时到第 23 小时，AMD 一直没有公开发布该镜像。AMD 宣称「速度就是护城河（SPEED IS THE MOAT）」，然而到第 23 小时它仍未发布。我们希望 AMD 团队今后为第 0 小时的模型发布准备更好的流程。

![](https://substack-post-media.s3.amazonaws.com/public/images/d87f68d4-6472-4aa2-8b98-fda4cf16e148_1918x1254.png)
*来源：vLLM AMD*
![](https://substack-post-media.s3.amazonaws.com/public/images/e40700af-36e7-41c7-82c7-b5eed85bec19_1700x1162.png)
*来源：vLLM，AMD，DockerHub*

等到他们最终公开发布「day 0」镜像支持之后，从性能上看，其每美元性能目前最高比 H200 差 14.8 倍、比 B200/B300 差 42 倍。

CUDA 护城河的威力在于 NVIDIA 与其多达 600 万开发者的社区生态的协作——包括 vLLM、SGLang 和 Tokenspeed 的大部分维护者——这意味着 CUDA 在发布当天就是优化好的。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab4a2258-63cd-4db1-aab0-5fde3e34bd8b_1706x1168.png)
*来源：InferenceX*

总体来看，AMD 确实做出了显著改进，但每美元性能目前仍比 B200 差 2-4 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/c34d6dbf-931a-45e0-ad71-5ddb810a7f25_1914x1602.png)
*来源：InferenceX*

## AgentX：Engram DRAM 卸载带来性能提升

HBM 和 DRAM 两种卸载方式使用同一个 GPU kernel 来选择行并反量化（dequantize）。表放在 HBM 时，它读取显存；借助统一虚拟寻址（UVA），它直接读取锁页（pinned）主机内存。

两者都支持完整的 decode 计算图。把表搬回 HBM 只加速了稀疏查找这一步，解码器的计算与通信保持不变，因而总体收益甚微，却占用了本可留给 KV 缓存的内存。

Engram 卸载到 DRAM 的另一个好处，是可以减少每个副本（replica）使用的 HBM GPU 数量，从而降低通信开销。例如，在 B300 上启用 Engram 卸载后，我们可以从 TP4 切换到 TP2，使帕累托曲线最多改善 1.6 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/a66eaf4d-e1c6-4967-bee8-5c3b995ef41d_1922x1214.png)
*来源：SemiAnalysis InferenceX*

在模型质量相同的前提下，由于 Engram 可以卸载到主机 DRAM，所需的 HBM 更少。因此 HBM 带宽远比 HBM 容量重要。对于内存带宽最要紧的推理工作负载，4 层堆叠（4-hi）HBM 提供最佳的每美元带宽，因而单 token 成本最低。如果中国继续做出越来越多革命性的模型架构创新，说不定很快就会出现 0 层堆叠（0Hi）的 HBM 了。

此外，在 B300 和第 0 周的软件栈上，把 Engram 表搬回 HBM 并未改善结果，差异仍在逐次运行波动范围内。这是对 DRAM 卸载所做的优化工作（如异步化、计算与传输重叠）的成果。

## SSD 卸载

在 B200 上，我们创建了一个未优化的 vLLM 分支，把 Engram 表存为本地 SSD 上的内存映射文件。文件后备（file backing）让操作系统可以在其他应用需要内存时回收表页面。已缓存在内存中的页面无需再次读取 SSD 即可服务。此外请注意，我们无法开启 GDS

未优化的 SSD 实现改变了数据行到达 GPU 的方式：它把行 ID 拷贝到 CPU，去重之后，把请求的行收集到锁页缓冲区，再把这些行拷回 GPU 并反量化。这些工作在 GPU 执行图的各段之间进行。而原生 UVA 直接在 GPU 上完成行选择与反量化，避免了 CPU 往返。

热的文件系统缓存可以消除物理 SSD 读取，但协调、行收集和传输仍然存在。这就是为什么一个已完全缓存在 RAM 中的文件，性能仍可能不如放在锁页 DRAM 中的表。这里的对比衡量的是完整的服务路径，并没有把各项操作的耗时单独拆开。

在每美元总 token 数和 P90 交互性两项指标上，B200 DRAM 全面压过两条实测的 SSD 服务曲线。在约 125 tokens/s/user 附近，DRAM 的每美元总 token 数为 1.21 亿，而 SSD 为 5,200 万。

![](https://substack-post-media.s3.amazonaws.com/public/images/3fcfe5b9-1ec1-44e2-9c21-be862536931c_1698x1504.png)
*来源：SemiAnalysis InferenceX*

对生产环境服务而言，SSD 卸载很可能不值得做这种权衡。在我们实测的 B200 配置上，SSD 卸载在两项指标上都落败：每一个观测到的 SSD 数据点，都有一个 DRAM 方案能同时提供更高的 P90 交互性和更多的每美元总 token 数。而唯一……

更便宜的存储并不会自动带来更便宜的推理服务。把 Engram 挪到 SSD 后，那四块昂贵的 GPU 和服务器的其余部分原封不动。回收 RAM 只有在能换来更便宜的服务器配置或额外的有效容量时，才会产生经济收益。当前未优化的路径两者都给不了，而且当表页面驻留内存时，文件系统缓存依然在消耗 RAM。

# 机制

接下来，我们将剖析 DeepSeekv4.1 Flash、LongCat、Qwen3.8 Flash Next 中 ngram 的机制与具体实现。

---
title: "GLM5.3 稀疏注意力如何影响 HBM 内存占用"
title_en: "How GLM5.3 Sparse Attention Affects HBM Memory Usage"
subtitle: "GLM-5.3、KV 缓存卸载、HiSparse、AgentX TileRT、InferenceX、DeepSeek 稀疏注意力、IndexShare、单 rollout 异步优化、网络安全"
date: 2026-09-28
source: https://newsletter.semianalysis.com/p/sparse-savings-persistent-demand-inside-glm53
crawled: 2026-09-15
authors: ["Kimbo Chen", "Alec Ibarra", "Wenyao Gao", "Pratt Bhatt", "Bryan Shan", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-29
---

# GLM5.3 稀疏注意力如何影响 HBM 内存占用

> 原文：[How GLM5.3 Sparse Attention Affects HBM Memory Usage](https://newsletter.semianalysis.com/p/sparse-savings-persistent-demand-inside-glm53) · SemiAnalysis
> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**GLM-5.3、KV 缓存卸载、HiSparse、AgentX TileRT、InferenceX、DeepSeek 稀疏注意力、IndexShare、单 rollout 异步优化、网络安全**

# 稀疏注意力如何影响 DRAM/NAND 内存

稀疏注意力如何影响包括 HBM 与 NAND 在内的内存总可服务市场（TAM）？稀疏注意力挑选最相关的 top-k 个 token 去做注意力计算，从而降低核心的缩放点积注意力（SDPA）运算中的内存消耗与带宽需求。然而，**这一效率提升在实践中并不会直接转化为整体内存的节省**。具体而言，top-k 选择运算通常要求完整上下文都驻留在 HBM 中，因此**稀疏注意力并没有消除内存容量瓶颈**。

![](https://substack-post-media.s3.amazonaws.com/public/images/4cd044d2-888a-4569-97ea-5354b07e4f62_1600x900.png)
*稀疏注意力的吞吐量受内存容量瓶颈制约。来源：HiSparse*

为了突破这一限制，SGLang 团队设计了 HiSparse——一套把 KV 缓存条目从设备端 HBM 主动卸载到主机端 DRAM 的层次化内存系统。**HiSparse 的行为类似一个 LRU（最近最少使用）缓存**：当 top-k 选择发生缓存未命中时，它把 token 从 DRAM 加载进 HBM；并依据 LRU 逐出策略把 token 从 HBM 卸载回 DRAM。为了降低缓存未命中延迟，HiSparse 把第 N 层的 KV 缓存加载与第 N-1 层的执行重叠起来（逐层重叠），这一做法源自 HiSparse 的前作 HiCache。

![](https://substack-post-media.s3.amazonaws.com/public/images/e5373e7c-4b2c-4741-8213-ec54052779cd_1126x174.png)
*逐层重叠。来源：CachedAttention*

借助 HiSparse，SGLang 在高并发、长上下文场景下大幅提升了吞吐量，代价是 top-k 缓存未命中带来的 I/O 开销。

**稀疏注意力在 SDPA 运算中减少了 KV 缓存的内存与带宽需求，但并未降低整体内存容量占用。** 此外，HiSparse 表明系统级优化能够克服稀疏注意力的内存容量限制，因此**单看稀疏注意力的内存画像并不足以刻画系统级 KV 缓存效率的全貌**。为了更完整地呈现稀疏注意力模型是如何被服务的，下面我们解释 Z.ai 的 GLM-5 系列模型的设计，以及它们在实践中如何被服务。

# GLM5.3 智能体推理服务

在我们的实时基准看板 InferenceX 中，GB300 在每秒 150 token 的响应速度下取得了本次对比中最低的建模服务成本。GB300 每 GPU 能处理更多 token，其更高的时租成本仍使其在成本效率上领先 GB200。GB300 的结果采用 Dynamo-TRT-LLM，而 GB200 的结果采用 Dynamo-SGLang。

我们使用 [9 月 28 日的 AgentX 快照](https://inferencex.semianalysis.com/inference/glm-5-3?g_model=GLM-5.2&g_rundate=2026-09-28&i_seq=agentic-traces&i_prec=fp4%2Cfp8&i_pctl=p90&i_best=0&i_optimal=1&i_metric=y_costh&i_xmode=interactivity)结果来帮助说明 GLM-5.3 的服务含义。我们使用 InferenceX 对超大规模云厂商自持并运营基础设施的成本模型来估算成本。总 token 数包括输入与生成的输出，其中包括跨轮次复用的缓存输入历史。流式速度以 p90 交互速度度量；首 token 延迟（TTFT）单独评估。

在每秒 150 token 下，GB200 每百万总 token 的成本约为 $0.044，相比之下运行 ATOM 的 MI355X 为 $0.049。在相同流式速度目标下约便宜 12%。这些数值由实测曲线估算得出，而非在恰好每秒 150 token 处单独测得。

本次对比中，我们使用 InferenceX 对超大规模云厂商自持并运营基础设施的估算成本。总 token 数包括输入与生成的输出，其中包括从缓存复用的输入历史。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/cd794226-78c0-4143-8b48-f632a507f676_2700x1900.png)
*来源：InferenceX | SemiAnalysis*

在 Dynamo-SGLang 的结果中，GB300 此处每 GPU 每秒服务约 13950 个总 token，相比 GB200 的 11873 个总 token 有 17.5% 的吞吐量优势。不过，我们假设 GB300 的每 GPU 时租为 $2.31，而 GB200 为 $1.86。在该目标下，更高的时租成本抵消并反超了 GB300 的吞吐量领先。

与 AMD 相比，在每秒 100 token 下 ATOM 比 GB200 便宜约 13%；在每秒 125 token 下 GB200 便宜约 5%，在每秒 150 token 下便宜 12%。在这三个目标下，两个系统都不具备一致的成本优势。

仅计生成的输出，在每秒 150 token 的响应速度下，GB200 每百万输出 token 的成本为 $5.92，比 MI355X ATOM 的 $6.68 低约 11%。这一指标适用于分析智能体负载下的成本——智能体反复复用长输入历史，而生成的相对较新的文本很少。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/5d4056ef-c9ad-424f-b93a-a67ca9574aac_2700x2160.png)
*来源：InferenceX | SemiAnalysis*

GB200 在每秒 150 token 目标两侧的测量，其 p90 首 token 延迟（TTFT）约为 14–19 秒，而 MI355X ATOM 约为 1.1–1.2 秒。GB200 部分成本最低的运行，等待首个 token 的时间要长得多。

因此我们做了第二个对比，只使用实际测试过、且达到至少每秒 150 token 同时 p90 TTFT 不超过两秒的配置。下图显示，配备 ATOM 的 MI355X 为每百万总 token $0.0607，而配备 Dynamo-SGLang 的 B200 为 $0.0666。在两秒首 token 限制下，ATOM 便宜约 9%。若把限制放宽到十秒，配备 Dynamo-TRT-LLM 的 GB300 便以 $0.0451 入围，比 ATOM 的 $0.0607 低约 26%。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/b2a4b342-0525-4274-af86-3e6d5e9f7fa8_2700x1800.png)
*来源：InferenceX | SemiAnalysis*

### 优化

在 GLM 的 5.2 / 5.3 模型中，其注意力架构降低了内存需求，而长时间运行的智能体仍需要保留较早的对话历史。GLM 以两种方式降低处理这段历史的成本：KV 压缩减少每个 token 缓存的状态量，稀疏注意力减少每次注意力运算读取的状态量。接下来由服务引擎决定缓存存储在哪里以及如何高效取回。

这些 B200 结果展示了有多少复用可以发生在 GPU 内存之外。当并发从 8 个请求增加到 16 个时，从 GPU 内存复用的 prompt token 份额从 90.3% 下降到 54.8%。其中大部分复用转移到了主机内存，后者从 6.0% 上升到 40.3%。GPU 缓存的下降大部分被来自主机内存的复用抵消，使整体缓存命中率在所有并发水平上都保持在 95% 以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/c49af533-cf97-4c90-8c33-0d5bee12e029_2048x1772.png)
*来源：SemiAnalysis InferenceX；InferenceX B200 行 440962、440961、440959；workflow run 33683520699*

除缓存管理外，服务引擎执行预填充与解码方式的改变也会改变性能。两项独立的 GLM-5.2 研究说明了这一点：

- vLLM 把第一个解码步保持在一致的 CUDA graph 执行路径上，在一项 [NVFP4 研究](https://github.com/vllm-project/vllm-project.github.io/blob/3be7020c6da40428eca107387d7faa8e58bd7074/_posts/2026-07-23-glm-5.2-nvfp4-b300-pd.md#22-optimization-speculative-padding-on-the-decode-side)中把平均每输出 token 时间（TPOT）从约 40 ms 降到 22 ms。
- 在另一项 8 卡 MI355X 长上下文负载中，ATOM 引擎跨流水线阶段分块处理预填充，使总吞吐量提高 98%，中位 TTFT 从 [28.6 秒降到 8.7 秒](https://github.com/ROCm/ATOM/pull/1552)。

## TileRT

对于 TileRT 上的 GLM5.3，AMD MI355X 最先得到支持。TileRT 是一个低延迟 LLM 推理引擎，它把解码编译成单个常驻内核（persistent kernel），减少启动开销，并让计算、访存与通信相互重叠。

它优先追求每个用户更快的 token 生成速度，而非最大化的批量吞吐量，同时由 vLLM 处理预填充。

在 AgentX 上，FP8 TileRT MI355X 达到的 p90 交互速度是最佳 FP4 MI335X 配置的 2 倍。与 GB300 NVL72 相比，它带来 40% 的交互速度提升。这些服务指标过去需要专用硬件才能实现。

![](https://substack-post-media.s3.amazonaws.com/public/images/22959305-42e4-48ef-afb2-913f9474f339_1582x1450.png)

不过，其 TTFT 仍非最优，还有继续开发的空间，例如优化 KV 传输、FP4 支持以及更大的批规模。

# DeepSeek 稀疏注意力

GLM-5（以及 GLM-5.x 系列模型）是一个总参数量 744B、激活参数量 40B 的专家混合（MoE）模型。对每个 token，它有 1 个共享专家，并从 256 个专家中路由经过 8 个，即稀疏度为 32。它采用 DeepSeek 稀疏注意力，本节将对此展开讨论。

DeepSeek 稀疏注意力（DSA）由 [DeepSeek V3.2](https://arxiv.org/abs/2512.02556) 引入，包含两个组件：一个选出 top K token 的**闪电索引器（lightning indexer）**，以及一个**稀疏多潜在注意力**（MLA）。

## 闪电索引器

闪电索引器在功能上类似一种**轻量级注意力机制**。查询与键被降维投影到更低维度，其中索引器查询为多头，索引器键为单头。由于选择 top K token 只需要查询-键关系得分（logits），索引器不需要 value 嵌入，也不需要用于归一化 logits 的 softmax 运算。取而代之，它计算查询-键点积，再接一个 ReLU 非线性。随后，索引器把每个 token 的索引器得分计算为所有查询头上 logits 的加权和，我们用它来选出 top K token。这意味着尽管索引器有多个头，**token 选择仍在多个注意力头之间共享**。选择 top K token 时，我们**把只注意到少于 K 个 token 的查询保留为稠密注意力**，否则选出 top K。

![](https://substack-post-media.s3.amazonaws.com/public/images/c3abe0c5-92c8-4912-ad2b-1b5ba3753580_1404x682.png)
*闪电索引器的概念示例。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/375d0869-c668-4145-bf66-3b019701c834_2048x2048.png)
*索引器得分是所有索引器查询头的加权和。来源：SemiAnalysis*

## 稀疏 MLA

[正如我们在 Kimi K3 一文中解释的](https://newsletter.semianalysis.com/i/209189055/multi-head-latent-attention)，MLA 有两种运行模式：多头注意力（MHA）模式与多查询注意力（MQA）模式。两者各有取舍：MHA 模式 FLOPs 更低但内存成本高 42 倍；MQA 模式内存成本更低但 FLOPs 最多高 3.4 倍。DSA 采用 MQA 模式，因为稀疏注意力只注意到更少的 token，缓解了更高的 FLOPs 消耗。不过实践中存在一个序列长度阈值：低于该阈值时，MHA 模式实际上比 MQA 模式更高效。直觉是：序列较短时，内存加载时间不占主导，FLOPs 更低的 MHA 模式可能占优。vLLM 实现了这一特性，为数据并行配置在序列长度 2K 到约 5K 区间使用 MHA 模式，张量并行则为 2K 到约 77K。2K 的下限是因为 top K 为 2048，而且如上所述，低于 2K 的注意力是稠密的。

![](https://substack-post-media.s3.amazonaws.com/public/images/f496f5be-6eff-4a54-ae7e-8d2555bc6716_1898x1265.png)
*MHA（绿）可能比 MQA（红）更快。来源：vLLM PR #48770*

## MLA 改动

对比 GLM-5 与 DeepSeek V3.2 的 MLA 维度配置，可以看到最显著的差异是**查询头数量**与**查询键头维度**。

![](https://substack-post-media.s3.amazonaws.com/public/images/c0857f2d-5a6a-45a5-accd-3ec332737582_1258x204.png)

[GLM-5 技术报告](https://arxiv.org/abs/2602.15763)提到，DeepSeek 是按照 H800 的 roofline 来选择查询头数量的。这很可能指的是：**解码期间 MLA 的 SDPA 算术强度大致处于 H800 的脊点（ridge point）上**。推导如下。设

- `L`：序列长度
- `d`：头维度
- `r`：RoPE 维度
- `H`：头数
- `b`：每参数字节数

MQA 模式下，FLOPs 为

```
2 * H * L * (d+r)  # P = Q [H, d+r] @ K.T [d+r, L]
2 * H * L * d      # O = P [H, L] @ V [L * d]
```

加载的内存为

```
b * H * (d+r)  # Q
b * L * (d+r)  # K and V
```

于是算术强度为

```
(2 * H * L * (2 * d + r)) / (b * (d+r) * (L + H))
= (2 * H * L * (2 * d + r)) / (b * L * (d + r))  # L >> H
= (2 * H * (2 * d + r)) / (b * (d + r))
```

代入 DeepSeek V3.2 的配置（`d` = 512、`r` = 64、`b` = 2），得到

```
(2 * H * (2 * 512 + 64) / (2 * (512 + 64)) ~= 2 * H
```

H800 的实际算术强度为 258.2 FLOP/B（实际峰值 865 TFLOP/s、带宽 3.35 TB/s，[据 DeepSeek](https://github.com/deepseek-ai/FlashMLA/blob/main/docs/20250422-new-kernel-deep-dive.md?utm_source=chatgpt.com#a-theoretical-analysis-of-the-mla-algorithm)），代入公式得 `H` ≈ 128。

GLM-5 的 H = 64、查询头数量减半，这意味着 GLM-5 可能是为不同的硬件设计的。若代入 GLM-5 的配置（d = 512、r = 64、b = 2、H = 64），得到算术强度 120.8 FLOP/B。因此我们怀疑 GLM-5 是针对摩尔线程（Moore Threads）MTT S4000 优化的，后者约为 128 FLOP/B。摩尔线程与 Z.ai 的合作，例如 [GLM-5.3-Flash 的 Day 0 支持](https://www.mthreads.com/news/341)，印证了我们的推断。

另外，GLM-5 把 QK NoPE 维度从 128 提高到 192，消融实验显示该配置在等 FLOP（iso-FLOP）与等参数约束下更优。这使 SDPA 头维度从 192 提高到 256，在计入头数减少之后，FLOPs 仍减少了 33%。

## IndexShare

随着上下文增长，索引器的延迟成本变得不可忽略。为缓解这一成本，Z.ai 在 GLM-5.2 中提出 IndexShare（又名 IndexCache）：每 4 层 DSA 共享一个索引器。

![](https://substack-post-media.s3.amazonaws.com/public/images/1afc9d13-969e-449a-91d1-cd3b310c779a_944x654.png)
*30B DSA 模型在不同上下文长度下的延迟成本。来源：IndexCache*

IndexShare 给训练与推理都带来了额外的复杂性。标准 DSA 训练分两个阶段：先是稠密预热阶段，此时除索引器外的所有模型权重冻结、注意力计算为稠密；随后是稀疏适配阶段，此时全模型以稀疏注意力训练。

![](https://substack-post-media.s3.amazonaws.com/public/images/88c2f29b-e00a-4240-92a0-2a1c30c7ee15_1258x264.png)

在训练目标上，索引器被训练为与各注意力头得分之和对齐，采用 KL 散度目标。IndexShare 把训练目标调整为：**让索引器 logit 分布与共享层上注意力得分的平均分布对齐**。

在推理方面，通常**索引器像注意力缓存 KV 一样缓存键**。由于多层共享一个索引器，我们还需要在完整层级额外缓存 top K 索引，以便在共享层复用 top K 选择信息。

这一设计把索引器缓存减少 75%，把索引器 FLOPs 减少 75%，并在不同上下文长度与预填充/解码下把吞吐量提升 1.5 到 1.8 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/f70d8106-0784-4721-b55f-e2285ce91f6d_2048x629.png)
*30B DSA 模型的基线 vs. GLM-5.2 配置（红）。来源：IndexCache*

# 训练后设计

## 流水线

预训练与中期训练之后，GLM-5 的训练后流水线从监督微调（SFT）开始，接着是**三个 RL 训练阶段**（推理 RL、智能体 RL 与通用 RL），最后以一次**同策略跨阶段蒸馏**收尾，把推理与通用 RL 蒸馏回 SFT 检查点。

![](https://substack-post-media.s3.amazonaws.com/public/images/b2665b55-e60e-4d73-ac0f-68b93e205460_2048x1432.png)
*GLM-5 训练后流水线。来源：SemiAnalysis*

这里我们强调两个细节。第一，技术报告称推理 RL 模型**完全以同策略（on-policy）方式训练**，这意味着它是同步训练的。同步 RL 训练系统效率较低，但 RL 训练稳定性更高。第二，**同策略跨阶段蒸馏类似于多教师同策略蒸馏（MOPD）**，即学生模型在多个教师模型之上进行带同策略蒸馏的 RL 训练。不过，MOPD 的目标是把多个专家教师模型合并为一个模型，而 GLM-5 这里似乎更多是为了**找回旧能力的损失**，即模型学习新能力时旧能力发生退化的问题。基于这一假设，我们不确定 Z.ai 为何只使用推理与通用 RL 检查点作为教师，而不是使用全部三个 RL 检查点。

根据[发布公告](https://z.ai/blog/glm-5.2)，GLM-5.2 可能已把同策略跨阶段蒸馏替换为标准的 MOPD 流水线，Z.ai 将其命名为并行 OPD 训练（parallel OPD training）。Z.ai 宣传了它的规模与训练效率：他们用约两天的训练把十多个专家模型合并为一个最终模型。

## RL 训练算法

Z.ai 在同步与异步 RL 阶段采用不同的 RL 算法。下面我们比较 RL 目标的主要差异。

同步 RL 阶段，Z.ai 采用基于组相对策略优化（GRPO）并做了现代化改造的 RL 算法，包括：

- **移除 KL 正则项**，提升系统效率并允许更激进的梯度更新
- **IcePop**：基于训练-推理失配比率施加 token 级掩码
- **Clip-Higher**：为重要性采样比率使用更高的上限阈值，以鼓励探索

相比之下，Z.ai 在异步 RL 阶段采用类 REINFORCE 的 RL 算法，并加入直接双边重要性采样（DIS）这一类似 IcePop 的裁剪机制。下面我们比较两个 RL 阶段的 token 级目标：

![](https://substack-post-media.s3.amazonaws.com/public/images/eab874c6-4338-4a58-b394-8de2794966dd_2048x472.png)
*两个 RL 阶段的 token 级目标。来源：SemiAnalysis*

重要性采样（IS）比率比较的是**每个采样动作在当前策略与行为策略下的概率**，并据此缩放每个动作对训练目标的贡献。对于 IS 比率，同步 RL 阶段使用**上一轮迭代的训练器策略**作为行为策略，而异步 RL 阶段则使用**推理策略**。在异步训练设定下，策略更新会在 rollout 期间发生多次，因此计算 IS 比率需要其间的每一个检查点版本。然而，由于高昂的内存与延迟开销，这并不可行。于是，Z.ai 出于效率与简洁的考虑选择使用推理策略，代价是数值稳定性方面的挑战。

![](https://substack-post-media.s3.amazonaws.com/public/images/db5823b7-0ac8-4326-af4f-5e3b3829f100_1654x484.png)
*两个 RL 阶段的 IS 比率。来源：SemiAnalysis*

最后，我们强调 RL 训练中优势计算、跨阶段蒸馏与长时程 RL 训练的主要差异。RL 训练采用 GRPO 标准的组归一化优势，跨阶段蒸馏使用反向 KL 散度。

![](https://substack-post-media.s3.amazonaws.com/public/images/855b6009-e0d8-4e01-bab5-d6abfdd5849b_2048x479.png)
*优势计算对比。来源：SemiAnalysis*

### 单 rollout 异步优化

长时程任务会产生极长的轨迹，而在 GRPO 的语境下，轨迹长度的高方差会带来不稳定的训练信号，并可能偏向更长的轨迹。更糟的是，由于 [RL rollout 负载对端到端延迟敏感](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching)，掉队 rollout 的尾延迟在长时程任务中会进一步恶化。为缓解这一问题，Z.ai 在 GLM-5.2 的长时程 RL 训练中引入了[单 rollout 异步优化](https://arxiv.org/abs/2607.07508)（SAO）。**SAO 用一个改进的广义优势估计（GAE）取代组归一化优势**，灵感来自[近端策略优化](https://arxiv.org/abs/1707.06347)（PPO）。GAE 只需要单条 rollout 即可计算优势。这免去了每个 prompt 做多条 rollout 的需要，缓解了 GRPO 的短板。

![](https://substack-post-media.s3.amazonaws.com/public/images/29bbbf45-36e4-470f-be0c-092db886317d_1255x669.png)
*生成节点请求训练节点等待 rollout 完成。来源：SAO*

GAE 的计算需要**价值**（RL 术语中即当前状态的期望回报），由一个**价值模型**来估计。具体而言，价值模型以 rollout 为输入，为每个 token 输出一个价值估计。SAO 通过把观测 token（即工具调用结果）从优化中移除，使 GAE 适配智能体 RL 训练。此前在 GLM-5 中，跳过这些 token 就足够了；而在 SAO 中，我们修改了优势估计公式来绕过观测 token。关于 Bellman 目标与消融实验的更多直觉，请读者参阅 [SAO 论文](https://arxiv.org/abs/2607.07508)及其附录 A.1。

在 SAO 中，**价值模型是一个与策略模型并行训练的独立 LLM**。这意味着训练早期由于价值模型较弱，优势计算容易受高方差影响。为应对这一点，SAO 提出了多种训练价值模型的技术：

- **双时间尺度更新规则**：价值模型的更新频率是策略模型的两倍。这意味着在策略训练的每一步，每个数据批次会被训练两次
- **注意力参数冻结**：冻结价值模型的全部注意力层，以提升训练稳定性
- **扩展预训练**：扩大价值模型的预训练语料来初始化价值模型，使其在训练早期能够稳健地估计价值。遗憾的是，Z.ai 并未披露预训练语料的规模信息

![](https://substack-post-media.s3.amazonaws.com/public/images/b83b1151-c583-4cb6-bd89-a247fb7f4f92_335x597.png)
*来源：SemiAnalysis*

以计算开销和内存占用翻倍为代价，SAO 用一个价值模型取代了分组采样，缓解了 GRPO 的延迟问题。

## 训练后基础设施

Z.ai 使用 *slime*——最好的开源 RL 训练框架之一——作为所有 GLM-5 模型的训练后基础设施。我们建议读者参阅 *[slime](https://github.com/THUDM/slime)* 的 [GitHub 仓库](https://github.com/THUDM/slime)以了解其设计与特性，这里我们强调两个特性。

RL rollout 的性能特征高度依赖任务，每个任务都配有不同的工具与奖励函数。为确保系统效率，Z.ai 设计了**基于服务器的多任务 rollout 编排器**。每个任务作为一个独立的微服务服务器，控制 rollout 与奖励逻辑。编排器负责**均衡整体性能**，控制各任务的 rollout 比例与生成速度。集中化还带来了跨任务的动态比例调整、细粒度进度监控等更多能力。Z.ai 称在训练 GLM-5 时，该编排器支持 1000 路并发 rollout。

![](https://substack-post-media.s3.amazonaws.com/public/images/749e2de3-ef84-4776-864e-846243d30d9e_2048x1039.png)
*多任务 rollout 编排器架构图。来源：SemiAnalysis*

在 [GLM-5.3 发布公告](https://z.ai/blog/glm-5.3)中，Z.ai 声称除主机内存外还使用本地存储作为缓存层，从而支持 **MOPD 的动态教师模型切换与预取**。*slime* [PR#1538](https://github.com/THUDM/slime/pull/1538) 通过引入 `TensorBackuper` 类实现教师切换，该类把教师权重存储为固定（pinned）在 CPU 内存中的 PyTorch 张量。当一个 rollout 被路由到某个教师时，一个 `TensorBackuper` 对象会把教师模型拷回 GPU 内存执行一次前向传播（[实现见此处](https://github.com/THUDM/slime/blob/main/slime/backends/megatron_utils/actor.py#L405-L425)）。不过，这是由 CPU 支撑的权重换入换出，我们尚未看到由存储支撑的实现。

在本文付费墙后的部分，我们将呈现对 GLM-5.3 网络安全能力的分析。

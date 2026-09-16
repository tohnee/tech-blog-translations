---
title: "RL 系统也要「小心空隙」：匹配训练器与生成器的吞吐量"
title_en: "RL Systems Mind the Gap: Matching Trainer and Generator Throughput"
subtitle: "RL 训练基础设施、GRPO、PipelineRL、异步 RL、策略陈旧（Policy Staleness）、RL 沙箱基础设施、CPU 需求、TCO 分析、Thinking Machines Tinker"
date: 2026-06-16
source: https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching
crawled: 2026-09-15
authors: ["Kimbo Chen", "Cheang Kang Wen", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# RL 系统也要「小心空隙」：匹配训练器与生成器的吞吐量

> 原文：[RL Systems Mind the Gap: Matching Trainer and Generator Throughput](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**RL 训练基础设施、GRPO、PipelineRL、异步 RL、策略陈旧（Policy Staleness）、RL 沙箱基础设施、CPU 需求、TCO 分析、Thinking Machines Tinker**

# 能力的代价

编程助手是世界上迄今最伟大的 B2B SaaS 应用：按我们的 [Tokenomics 模型](http://semianalysis.com/tokenomics-model)估算，如今六大玩家合计已是一个 $30B+ ARR 的市场，且有望在年底突破 $100B。

![](https://substack-post-media.s3.amazonaws.com/public/images/54113290-ca32-4a32-a202-64d43abf4c57_1780x1031.heic)
*来源：SemiAnalysis Tokenomics 模型估算*

这些助手的智能体编码能力并非仅来自预训练。后训练（post-training），尤其是强化学习（RL），才是从预训练模型中引出这些能力的关键。具体来说，Claude Opus 4.8 在 SWE-bench Pro 上得分 69.2%、在 Terminal-Bench 2.1 上得分 74.6%，而 RL 训练正是推动这一得分的主要因素之一。

Anthropic 的 CEO Dario Amodei 曾表示，RL 正呈现出预训练曾有过的那种扩展规律：性能随训练时长呈对数线性攀升（[链接](https://www.youtube.com/watch?v=n1E9IZfvGMA)）。但这种扩展极其昂贵，因此 RL 系统效率至关重要：它决定了你负担得起多少 RL，也决定了模型能力能走多远。

是什么决定 RL 训练系统的效率？在本文中，我们用开源 RL 框架在开放权重模型上做了 RL 训练实验，并与 Tinker 等托管 RL 训练方案比较了价格。我们将证明：系统效率归根结底在于让训练器（trainer）与生成器（generator）的吞吐量相匹配。

# 致谢

我们感谢以下各方在紧密合作上的支持：

- Prime Intellect：Matej Sirovatka、Ameen Patel、Sami Jaghouar、Johannes Hagemann。感谢他们提供训练配方（recipe）、硬件资源以及对文章的反馈
- Modal：Peyton Walters、Nan Jiang、Erik Dunteman。同时感谢 Modal 赞助的 API 额度
- vLLM / Inferact：Kaichao You、Ao Shen
- verl 开发者：Xibin Wu、Yuyang Ding、Yan Bai
- slime 开发者
- [Verda](https://verda.com/)：为实验提供了算力

我们还要感谢以下各位审阅并提供反馈：

- Linden Li，Applied Compute：给出了很好的建议，其 [AIE 演讲](https://www.youtube.com/watch?v=o15AaYl7Wu0)是本文的灵感来源
- Periodic Labs：Dennis van der Staay、Byron Hsu
- Randy Ardywibowo，Perplexity AI
- [λux](https://x.com/novasarc01)，Non-Euclidean Pasture
- Simon Guo，Thinking Machines Lab

# 三个角色

一套开源 RL 训练系统有三个角色：**生成器（generator）**、**RL 环境（RL environment）**和**训练器（trainer）**。**生成器**对来自数据集的提示词（prompt）做推理，生成一条 rollout：即一个提示词加上模型生成的回复。与预训练不同，数据集只提供提示词，不提供完整目标；训练信号由系统自己生成。生成 rollout 时，生成器与 **RL 环境**交互。RL 环境基于 rollout 给出奖励（reward）。例如，代码环境会在沙箱中执行生成的代码，并依据测试用例通过率给出奖励分数。随后，**训练器**消费生成器产出的 rollout 与奖励、训练模型、产出新的模型权重。最后，训练器把新权重推送给生成器，闭合一个 RL 训练步的循环。

![](https://substack-post-media.s3.amazonaws.com/public/images/07ee31f9-e887-424b-a1b1-d11c88e86a73_1046x795.jpeg)
*来源：SemiAnalysis*

# 刚好够用的 RL 算法知识

预训练最大化对数似然（log-likelihood），RL 训练则最大化期望奖励。**组相对策略优化（Group-Relative Policy Optimization，GRPO）**是开源界的事实标准，大多数开放权重模型都用它的某种变体训练。

GRPO 为每个提示词采样多个补全（completion），构成一组 **rollout**。我们为每条 rollout 赋一个**奖励**，即该 rollout 的得分。再计算每条 rollout 的**优势（advantage）**：其奖励相对组平均的差值，刻画它比该提示词下的典型 rollout 好多少或差多少。高于组平均的 rollout 被强化，低于组平均的被抑制。

如果组内每条 rollout 拿到相同奖励，那么每条都等于组平均，所有优势都为零，这一组就产生不了训练信号。这由该组的**奖励分布**决定：只有当组内 rollout 表现出不同行为时，这一组才能让模型学到东西。极端情况是均匀分布——任务太简单（每条 rollout 都通过）或太难（每条都失败）时就会出现，也就是解出率（solve rate）接近 100% 或接近 0% 的情形。

# 从同步 RL 到异步 RL

经典策略梯度算法（GRPO 正建立在其上）假设一组内的 rollout 来自同一个策略，即同一套权重的模型。放到训练系统的语境里，这意味着生成器必须等当前批次的 rollout 全部完成才能更新权重。于是，训练器做完一个训练步后就得等待生成器。这就导致训练与生成同步执行，严重拖累系统效率。

[PipelineRL](https://arxiv.org/abs/2509.19128) 向系统中引入了异步：允许训练器在 rollout 尚未完成时就把新权重推给生成器（在途权重更新，in-flight weight updates）。这样，训练器的执行就能与生成器的 rollout 相重叠。但这有代价。样本（sample）是训练器消费的基本单元，定义为一条 rollout 及 RL 环境为它打的奖励。有了在途权重更新，每个样本都由新旧策略混合生成。我们把这一现象称为策略陈旧（policy staleness）。

PipelineRL 证明 RL 算法能在一定程度上容忍策略陈旧。过于陈旧的样本会损害模型学习。而同步执行浪费的算力太多，大规模下并不现实，异步技术不可或缺。实际上，PipelineRL 就是一种带策略陈旧上限的吞吐量匹配方案。它允许训练器和生成器以不同速度运行，速度差的上限由样本允许的陈旧程度决定。这正是 PipelineRL 成为开源 RL 训练事实标准实现的原因。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c15bc58-352b-4213-a724-3482f50d1e6b_1130x691.jpeg)
*来源：Magistral，Mistral AI*

# RL 环境与沙箱

RL 环境向模型提供反馈，让模型学会如何完成一项任务。实践中，RL 环境实现为沙箱（sandbox）——一个容器化的代码执行运行时。视 RL 环境的复杂度而定，它可以是轻量的 Firecracker 微虚拟机（micro-Virtual Machines），也可以是完整的 QEMU 虚拟机。

服务于 RL 环境的沙箱有着独特的系统性挑战。生成器与 RL 环境之间的交互延迟对端到端 rollout 延迟至关重要，而沙箱启动延迟是主要开销之一。Modal 等沙箱服务公司用[内容寻址缓存](https://modal.com/blog/speeding-up-container-launches)等技术优化启动延迟。

大规模服务同样有挑战：沙箱数量随并发 rollout 数量扩展，而随着 rollout 被剪枝或完成，存活沙箱数量会剧烈波动。

最后，沙箱需要对系统故障保持健壮。学习过程中，模型的意外行为可能耗尽沙箱的配给资源。例如，创建上百万个文件可能让沙箱内存耗尽。沙箱编排必须能检测这些系统故障并从中恢复。

# 吞吐量匹配框架

## 量化训练器与生成器吞吐量

我们把 RL 训练系统看作一条队列：生成器把 rollout 生产进队列，训练器从队列中消费。当生成器比训练器慢时，队列被抽干、训练器「挨饿」，在训练步之间空转。当生成器更快时，队列膨胀、样本老化，带来策略陈旧问题。

我们从**生产者（生成器）与消费者（训练器）吞吐量相匹配**的视角来建模系统效率。理想的 RL 训练系统中，训练器消费速率应大致等于生成器生产速率。训练器消费样本、执行一个训练步、再把权重广播给生成器。我们测量训练步时间，包括等待新样本的空闲时间、计算时间和权重广播时间。我们进一步推导样本吞吐量（样本数 / 计算时间）来代表训练器消费速率。我们还计算每 GPU 的 FLOP/s 和模型 FLOPs 利用率（MFU）来刻画硬件效率。

生成器通过 LLM 推理和 RL 环境交互来生产样本。由于组内最长的 rollout——**拖尾样本（straggler）**——决定该组的完成时间，我们通过测量端到端延迟来估计平均样本吞吐量。由此可推导样本吞吐量（样本数 / 端到端延迟）来代表生成器生产速率。

我们进一步把延迟拆解为 LLM 推理时间和 RL 环境交互时间。RL 环境交互包括沙箱启动延迟和沙箱执行时间。

## 吞吐量约束

多个因素约束着吞吐量的上下界。训练器消费速率为**每步样本数 / 训练步时间**。

影响样本数的因素包括：

- **组大小（group size）**：每个提示词 N 个样本，N 通常为 8 或 16。视任务难度，我们会增大 N 以增强优势信号，例如[在 GPU kernel 编写任务中设 N=64](https://arxiv.org/abs/2601.16175)。更大的组会增加每步样本数
- **奖励分布与优势过滤**：rollout 组的奖励分布影响样本优势，并在不同优势过滤策略下减少每步样本数。例如任务难度：任务太简单或太难会导致均匀奖励分布（全零或满分），优势为零。如果我们丢弃零优势样本，就会减少每步样本数
- **批大小（batch size）**：存在一个能实现稳定学习的最小有效批大小。我们通常把训练器部署在足够多的 GPU 节点上以容纳这些批次

影响训练步时间的因素包括：

- **模型**：模型架构——包括模型规模、激活大小、模型精度——决定显存占用，从而设定了在不发生显存耗尽前提下执行前向与反向传播所需的最少 GPU 数量。它还决定 GPU 执行哪些运算，影响训练步时间
- **并行与显存配置**：张量/流水线/数据/专家并行、全分片数据并行（FSDP）、显存卸载、激活检查点（activation checkpointing）。它们受 GPU 数量影响，并决定系统效率和训练步时间

在生成器一侧，我们把生成器生产速率定义为**并发 rollout 数 / 端到端延迟**。

影响端到端延迟的因素包括：

- **推理吞吐量**：对推理引擎的配方调优，包括并行策略、KV 缓存量化、PD 分离（disaggregation）和投机解码（speculative decoding）
- **沙箱延迟**：沙箱启动时间与执行时间
- **奖励建模类型**：数学和编码任务可以用轻量验证器作为奖励模型，而写作任务可能使用 LLM 评审（judge）。奖励模型类型决定 rollout 评估延迟：轻量验证器快，LLM 评审相对慢
- **奖励形态**：过程奖励模型（PRM）可能逐轮评估 rollout，而有些奖励模型只评估完整 rollout。这决定了奖励赋分延迟

并发数，即并发 rollout 数量，受 KV 缓存显存空间和平均序列长度限制。生成节点的总显存容量减去模型权重和激活之后，剩下的就是 KV 缓存的空间。KV 缓存决定了生成器能容纳的最大 token 数，将其除以平均序列长度，即可估算最大并发数。

由于训练信号质量的差异，并非所有生成的样本都会被训练器消费。我们进一步把有效生成器生产速率定义为：接受率 × 生成器生产速率。影响接受率的因素包括：

- **[提前剪枝](https://arxiv.org/abs/2603.24840v1)（early pruning）**：我们依据启发式长度上限、价值函数或中间结果验证器检查，在 rollout 完成前将其剪掉。这会动态减少并发 rollout 数量
- **自适应采样**：我们依据标准拒绝 rollout，例如[在线优势过滤](https://www.primeintellect.ai/blog/intellect-2)

## 策略陈旧（Policy Staleness）

陈旧度指的是生成样本的策略版本与训练器施加梯度时所用的策略版本之间的差距。陈旧是异步训练的副产品：训练器在 rollout 生成过程中在途推送权重更新。

陈旧发生在不同粒度上。在轨迹（trajectory）层面，陈旧是 rollout 开始生成时所用的策略与训练器已更新到的较新策略之间的差距，例如训练器已在版本 t+k，而该轨迹从版本 t 开始。token 级陈旧发生在在途权重更新落在 rollout 中途时，于是 rollout 的不同部分由不同策略版本生成。策略陈旧也会发生在环境状态层面，我们会在「部分 rollout 与有状态沙箱设计」一节详细解释。

策略陈旧意味着训练器在 off-policy 信号上训练模型，这可能使训练失稳，因此我们通常设定一个策略陈旧预算（policy staleness budget）。该预算限定样本最多可以多陈旧，即允许生成器领先训练器多远，超出的样本将被拒绝。这反过来给生成器生产速率与训练器消费速率之差设了上限，也正是两者能以不同速度运行的原因。

策略陈旧预算限制了训练器消费速率与有效生成器生产速率之间的最大差距。具体而言，它限制生成器最多能领先训练器多少步，使 RL 算法能够容忍样本中的最大陈旧度。

## 移动的靶子：模型能力与行为

在 RL 训练中，模型能力和行为是一等公民级的系统变量。模型能力决定模型解任务的好坏，用**解出率（solve rate）**衡量：组内通过验证的 rollout 所占百分比。当解出率接近 0 或接近 100% 时，奖励分布趋于均匀，优势为零，训练信号坍塌。这会驱动**组大小**和**优势过滤策略**等决策，也塑造**课程（curriculum）**——即任务呈现给模型的顺序。课程的选取要让解出率维持在富有产出的中间区间，使任务相对模型当前能力既不过于简单也不过于困难。

模型的 token 使用行为影响输出长度，间接决定生成器中的最大并发 rollout 数。RL 训练通常会引出思维链（Chain-of-Thought）推理，使模型生成很长的推理轨迹。这一行为推高平均输出长度，进而增加 KV 缓存占用。在同样的显存预算下，这会减少最大并发 rollout 数，并拉长样本生成的端到端延迟。

模型的工具调用行为影响端到端延迟中的沙箱时间。具体而言，工具调用越多，沙箱时间越长，而意外的工具调用操作会给沙箱基础设施施压。我们用工具调用次数和沙箱错误率来度量工具调用行为。

在 RL 训练过程中，模型能力和行为都在变化：能力在提升，行为在漂移。各项约束也随之移动，训练系统必须随之调整以保证效率。

# 案例研究

我们做了实验来落地验证理论，并分享使用各开源 RL 框架的体验。

我们选取了如下配置：

- 模型：我们选择混合专家（MoE）模型，因为 SoTA 开源模型大多是 MoE
- RL 环境与任务：我们选择智能体编码任务，因其流行度高、沙箱工作负载复杂，便于观察沙箱的性能特征
- 节点数：我们以至少 10 个节点为目标开展实验，以展示训练器-生成器动态，并装得下 MoE 训练

## 超长模型回复与早期探索训练阶段

### 配置

- 模型：[Qwen3-235B-A22B-Thinking-2507](https://huggingface.co/Qwen/Qwen3-235B-A22B-Thinking-2507)。训练用 BF16 精度，样本生成用 FP8 变体——RL 训练中的常见配置
- 训练器：64 张 H200 GPU，FSDP、EP8，优化器状态与激活 CPU 卸载
- 生成器：192 张 GPU，24 个推理实例：每实例 DP1、TP8、EP8
- 批大小：512 个样本

  - 组大小：每题 16 条 rollout
  - 每批题目数：32 题
- 最大序列长度：32K
- 最大策略陈旧：16 步
- RL 环境：[Mini SWE Agent Plus](https://app.primeintellect.ai/dashboard/environments/primeintellect/mini-swe-agent-plus)，使用 Prime Intellect Sandboxes
- RL 框架：[Prime RL](https://github.com/PrimeIntellect-ai/prime-rl)
- 代码：配方即将进入仓库主分支。原始 commit 见[此处](https://github.com/PrimeIntellect-ai/prime-rl/pull/2344/changes/6849d5237354919ab8549435eaca8b0f2b96954b)

### 分析

本案例展示两个因素如何影响系统效率：模型如何产出带长思考轨迹的超长回复，以及模型学习该任务学得有多好。

模型的长回复行为是 LLM 推理时间的主要驱动因素，而推理时间占样本生成时间的大头。长回复的方差还会在每组 rollout 内造成严重的拖尾延迟，迫使系统层面采取缓解措施：过采样（oversampling）。采用过采样后，生成器发起的并发 rollout 数多于训练器每批所需，一达到目标数量就丢弃未完成或出错的 rollout。在本轮运行中，我们丢弃了多达 60% 的已派发 rollout——比例相当高，可见回复变长后延迟分布会变得多么倾斜。

![](https://substack-post-media.s3.amazonaws.com/public/images/e9715477-4da0-417a-bf7b-b4480f00434c_3591x2202.png)
*来源：SemiAnalysis*

在模型能力方面，课程对基座模型来说略偏难。我们观察到，产出零解的 rollout 组数量在第一个训练步后急剧跳升，但平均奖励和 pass@16 在缓慢回升。这些迹象表明：早期 RL 探索把策略从原本可解的问题上推开了，之后才逐步重新学会。

![](https://substack-post-media.s3.amazonaws.com/public/images/d19767ab-6774-4fea-a87a-293644ce54e0_3579x2202.png)
*来源：SemiAnalysis*

两者叠加的结果是一个**生成受限（generation-bound）系统**：队列被抽干，训练器挨饿。为缓解这一问题，我们用训练器效率换取生成器效率。训练器以 2.75 sample/s 消费样本，等待时间占挂钟时间的 30%，MFU 为 10.5%。而生成器交付 1.95 sample/s，使用的算力是训练器的 3 倍。这凸显了 RL 训练期间推理效率有多重要。

![](https://substack-post-media.s3.amazonaws.com/public/images/e437267a-2f94-4dc7-9aa5-06343b9c3d91_3579x2202.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/8b2db39e-0005-43af-b190-8acab5e2a7b4_3579x2202.png)
*来源：SemiAnalysis*

## 高频工具调用与简单任务

### 配置

- 模型：[GLM-5](https://huggingface.co/zai-org/GLM-5)。训练用 BF16 精度，样本生成用 FP8 变体
- 训练器：128 张 H200 GPU，FSDP、CP2、EP8，优化器状态 CPU 卸载
- 生成器：128 张 H200 GPU，2 组 64-GPU 推理副本

  - **PD 分离（disaggregation）：** 32 张预填充（prefill）GPU、32 张解码（decode）GPU，均为 DP32 和 EP32
  - 每节点 1TB KV 缓存卸载
- 批大小：512 个样本
- 组大小：每题 16 条 rollout
- 每批题目数：32 题
- 最大序列长度：64K
- 最大策略陈旧：16 步
- RL 环境：[Mini SWE Agent Plus](https://app.primeintellect.ai/dashboard/environments/primeintellect/mini-swe-agent-plus)，使用 Prime Intellect Sandboxes
- RL 框架：[Prime RL](https://github.com/PrimeIntellect-ai/prime-rl)
- 代码：配方即将进入仓库主分支。原始 commit 见[此处](https://github.com/PrimeIntellect-ai/prime-rl/pull/2344/changes/6849d5237354919ab8549435eaca8b0f2b96954b)

### 分析

本轮运行中，我们看到两个因素决定了系统效率：模型行为漂移，以及课程对模型来说太简单。

我们观察到，每轮平均回复长度与工具调用次数（从 20 到 51）在运行中都增长为约三倍。两者共同推高序列长度，并把工作负载推向以预填充为主（prefill-heavy）的形态。这印证了我们选择分离式服务（disaggregated serving）的正确性——它改善了预填充请求的最坏情况首 token 延迟（TTFT）。

![](https://substack-post-media.s3.amazonaws.com/public/images/7f210f78-d6f0-4caf-a608-740691e4f9e8_3579x2202.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/c3976923-3e66-4e9a-8b0b-cb95cdd40589_3591x2202.png)
*来源：SemiAnalysis*

在能力方面，课程对模型来说太简单。平均而言，55% 的题目解出率为 100%，即组内每条 rollout 都通过。一个所有 rollout 奖励相同的组产生零优势、不贡献任何训练信号。结果就是平均奖励持续走平。课程错配减少了有效训练样本，进而降低有效生成器生产速率。

![](https://substack-post-media.s3.amazonaws.com/public/images/3741248c-95ae-408d-a4a5-7a0a7912b1d4_3613x2202.png)
*来源：SemiAnalysis*

所有效应叠加成一个严重生成受限的系统。队列被迅速填满，但其中很大一部分被过滤掉，因此产出很低。LLM 推理主导端到端生成时间，且随着训练推进持续增长。训练器 74% 的挂钟时间花在等待上，其消费速率是生成器实际交付生产速率的 5 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/a064f122-e313-4234-85ef-ddd4ef563262_3579x2202.png)
*来源：SemiAnalysis*

## 沙箱扩展性挑战

### 配置

- 模型：Qwen3 235B A22B Instruct 2507，训练与生成均为 FP16
- 硬件：GB300
- RL 框架：verl + uni-agent rollout
- RL 环境：SWE-bench 风格环境，使用 Modal 沙箱
- 算法：GRPO
- 最大序列长度：128K

### 训练阶段

第一阶段：

- 训练器：32 张 GPU，TP16 / EP32，CPU 卸载
- 生成器：24 张 GPU，6 个副本，TP4
- 组大小：8
- 并发 rollout 数：96

第二 / 第三阶段：

- 训练器：48 张 GPU，TP4 / CP4 / PP3 / EP16，CPU 卸载
- 生成器：24 张 GPU，6 个副本，TP4
- 组大小：8
- 并发 rollout 数：256（第二阶段）/ 360（第三阶段）

### 分析

训练动态与我们其他 Qwen3 235B 训练运行基本一致。本轮为生成受限：训练器 30% 到 60% 的时间在空转。生成长度增长迅猛：3% 到 8% 的样本触及 128K 最大序列长度；出于类似原因，第 9 步出现一个明显拖尾样本，尾部延迟飙到 7500s。

本案例的独特之处在于我们推高了并发 rollout 数，从而遭遇沙箱扩展问题。扩展并发 rollout 对样本生成吞吐量至关重要：它支撑更大的批大小、更丰富的奖励信号方差，进而带来更好的训练信号。然而，每条 rollout 至少对应一个沙箱，扩展 rollout 并发对沙箱基础设施的可靠性构成考验。本案例中，我们在 96 到 960 的并发 rollout 范围内实验。在 960 时，一旦越过账户配置的限制，就会遇到沙箱初始化死锁报错，以及拖尾样本长达 1 小时的沙箱启动延迟；为缓解，我们缩减回 96，但随后又观察到 rollout 效率低下。这个实验说明，沙箱扩展对 RL 训练效率何其关键。

感谢 vLLM / Inferact 的 Ao Shen 与 Kaichao You 协助完成本实验。错误与尝试的详细记录见[此处](https://my.feishu.cn/wiki/PO4twjE1IivFvKk292rcRdbRnZg)，最终阶段训练的 WandB 日志见[此处](https://wandb.ai/aoshen524-purdue-university/Qwen3-235B-A22B-Instruct-2507-grpo-prod/reports/Qwen3-235B-SWE-bench-Solo-tail-step-16-20---VmlldzoxNzEzODcxNw?accessToken=p3rzkwxgpqhxavr92k7d9uy7w8ma10dbuldy9oam8kjohaoxcf5uia6h313152m3)，代码仓库在此（[verl](https://github.com/aoshen02/verl/tree/benchmark/semianalysis-verl)、[uni-agent](https://github.com/aoshen02/uni-agent/tree/benchmark/semianalysis-verl)）。

## 部分 rollout 与有状态沙箱设计

### 配置

- 模型：Qwen3-235B-A22B-Thinking-2507-FP8（FP8 生成，BF16 训练）
- 训练器：32 张 H200 GPU，TP4 / CP4 / PP2 / EP8
- 生成器：64 张 H200 GPU，8 个副本，TP8 / EP8
- 最大序列长度 32K，全局批大小 64
- 算法：GSPO，组大小 8
- RL 框架：slime
- 异步配置：完全异步 + 部分 rollout
- RL 环境：SWE-Bench Verified 与 Lite，使用 OpenHands harness 和 Modal 沙箱
- 代码仓库：[slime SWE Bench 示例](https://github.com/SemiAnalysisAI/slime/tree/feat/swe-env-example/examples/swe-bench)

### 分析

总体上，本实验的系统特征与其他 Qwen3 235B 运行相似：生成受限、训练器等待占比 60%、每轮回复长度长达 12K、每序列平均 12 次工具调用（中等水平）、解出率相对较低。

我们想重点介绍 slime 的部分 rollout（partial rollout）特性，以及沙箱设计为支持它而必须做出的调整。部分 rollout 允许把拖尾 rollout 存入缓冲区、留待后续批次重启。这缓解了拖尾 rollout 的长尾延迟，从而提升系统效率。

在 slime 中，部分 rollout 会把拖尾 rollout 标记为中止（aborted），保存到回放缓冲区（replay buffer），并放入未来批次的队列。这给沙箱带来了挑战：

- 沙箱需要跨 rollout 批次存活，因为 SWE-Bench 题目可能是有状态的：某条部分 rollout 可能正处于编辑文件的中途。这也意味着我们需要额外逻辑来跟踪沙箱 ID 与样本的映射
- 沙箱需要惰性创建：样本处理逻辑与沙箱创建耦合，但存在样本未能发出工具调用的情况，此时创建沙箱就是浪费
- 沙箱的抗故障能力：如果沙箱在样本被中止到被重启之间发生故障，我们需要额外逻辑保证正确性。由于我们没有找到在 Modal 上做故障恢复的方法，我们选择将样本标记为失败

slime 在两种情况下触发部分 rollout 中止：目标 rollout 批次凑满时（我们的配置为 64 个样本），以及训练器推送权重更新时。这让回放缓冲区中的部分 rollout 数量呈现出有趣的动态。我们看到该数量在第 5、10、15 步之后上升，因为我们每 5 个间隔更新一次权重。我们还看到数量在第 7 步和第 17 步出现尖峰，我们认为原因是前一步（第 6 步和第 16 步）一凑满目标 rollout 批就立即完成，留下了大量积压。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce05f337-9d5b-4d79-887c-653a9caa806c_3579x2202.png)
*来源：SemiAnalysis*

与 PipelineRL 不同，slime 的 SGLang 配置会驱逐被中止 rollout 的 KV 缓存。这意味着被恢复的 rollout 本质上是大型预填充请求——恰恰是最能从 PD 分离中受益的工作负载类型。

![](https://substack-post-media.s3.amazonaws.com/public/images/c6234326-fba2-4f30-9e4b-1363d671c004_747x588.jpeg)
*来源：Kimi Researcher，Moonshot AI*

部分 rollout 正是环境状态级陈旧显现之处。当一条被中止的 rollout 在后续批次中恢复时，训练器在此期间已推送了新权重，于是被恢复的 rollout 面对的不仅是策略差距，还有有状态环境特有的状态差距。在我们的 SWE-Bench 案例中，rollout 唤醒所处的沙箱并不是一个全新的仓库：沙箱里留着旧策略在之前轮次产生的改到一半的编辑、已创建的文件和工作目录状态。新策略现在必须从一种并非由它造成、它自己也未必会造成的局面继续。这会污染训练信号：训练时，优势被归因于一条当前策略只部分「拥有」的轨迹。看到权重更新后被恢复 rollout 数量之高，我们怀疑环境状态级陈旧是本轮解出率偏低的原因之一。

总结：部分 rollout 拯救了拖尾样本、维持了填满队列的吞吐量，但代价是有状态沙箱的复杂性以及显式的环境状态级策略陈旧。

## 软件使用体验

### Prime RL

Prime RL 的用户人机工程做得很好。用户用 uv 执行大多数命令，并在 .toml 文件里完成配置。Prime RL 还附带 agent skill 文件，让用户在该仓库上工作时能更顺畅地使用 AI 智能体。

在系统设计上，我们欣赏 Prime RL 设有一个「编排器（orchestrator）」角色，明确了由谁管理训练器-生成器动态。我们喜爱它的 RL 环境聚合平台 Environments Hub，并期待它继续成长。Prime RL 训练用 Torch Titan，生成用 vLLM，托管 RL 环境用其自研的 Prime Sandbox。Prime RL 还支持生成器的 PD 分离，对智能体 RL 训练的性能提升显著。总体而言，这个代码库精炼，且集成了大多数最先进的技术。

不过我们也遇到了一些毛边。Prime RL 对 uv 的重度依赖默认用户对 uv 非常熟悉。我们花了大量时间反复编译、重装 flash attention 3，因为搞不清楚为什么 uv 把它卸载了。我们鼓励 Prime Intellect 提供更多资源向用户讲清 uv 的工作原理，而不只是在文档里列出哪些 uv 命令不要执行。

尽管 Prime RL 默认运行在 SLURM 集群上，它却假定任务跑在裸金属而非 Pyxis 上。当我们遇到 DeepGEMM 库的 CUDA 库版本不匹配时，把任务放进容器里跑会更容易解决。

我们还有大量失败的运行，最后发现是 Prime Sandbox 故障。Prime Sandbox 的报错信息很难解析，而且故障往往发生在运行后期。

错误包括残留（dangling）沙箱耗尽沙箱配额、资源不足报错、额度用尽问题等，其中许多本可在启动运行前检测到。Prime Sandbox 仍在 beta 阶段，我们期待它未来改进。

感谢 Prime Intellect 对这项工作的支持，包括软件和硬件资源。Prime Intellect 提供的训练配方基于[这个 PR](https://github.com/PrimeIntellect-ai/prime-rl/pull/2344)（commit 哈希见[此处](https://github.com/PrimeIntellect-ai/prime-rl/pull/2344/changes/6849d5237354919ab8549435eaca8b0f2b96954b)）。

### slime

slime 以干净而极简的抽象著称，我们认为它名副其实。我们尤其喜欢 slime 的 hook 抽象：它让我们能为 rollout 处理、奖励函数和指标记录工具编写自定义函数。函数签名与契约清晰明了，开发过程中集成和添加新功能毫不费力。

我们还想强调 slime 开发团队的友好与热心。slime 的核心维护者 Zilin 在配置调优上给予了指导，并解答了 slime 的设计问题。

我们的主要不满是 slime 以共存（co-located）模式为中心，导致异步模式的文档很稀疏。async 与 fully async 的区别、部分 rollout 的机制，我们基本靠试错摸索出来。希望 slime 能就这些主题提供更好的文档。

### Modal

Modal 的 API 文档非常出色：在 slime 中实现沙箱集成时，我们大量参考了 Modal 的 Sandbox API，文档清晰实用。在我们的整个实验过程中，Modal 服务也相当稳健。小规模下 Modal 一直可靠，创建/终止沙箱简单且响应迅速。Modal 团队同样非常友好热心。Modal 在项目早期就提供了 API 额度支持，Modal 的 slime 集成团队 Peyton 和 Nan 对我们的实验结果给出了很好的建议和反馈。

Modal 的主要挑战出现在我们运行大量并发沙箱之时。如前文所述，我们遇到了初始化死锁报错和长尾沙箱启动延迟。我们怀疑这是我们自己误用 API，而非 Modal 的硬性限制，但训练期间我们无法在自己这端定位根因。后来我们联系了 Modal，合作排查问题。结果发现是我们账户上的资源限制；在 Modal 提高我们的限额后，我们验证了高沙箱并发下的稳定性（[复现代码在此](https://github.com/verl-project/uni-agent/tree/yy/modal_concurrency/reproduce)）。我们感谢 Modal 开发团队的快速响应，也希望 Modal 未来能提供更多沙箱可观测性工具，以及更多关于如何扩展沙箱规模的文档。

# 开源 RL 框架简史

DeepSeek R1 的发布点燃了开源社区复现其算法与基础设施的努力。早期成果之一是 OpenRLHF——一个大规模 RL 训练框架，先后实现了 PPO、REINFORCE++ 和 GRPO。OpenRLHF 深刻影响了后续 RL 框架的发展。众多 OpenRLHF 的维护者后来开发了流行的 RL 框架，包括 slime 和 verl。这些框架催生了活跃的中文 RL 训练社区，我们认为这为中国模型近期的进步做出了积极贡献。这些开源框架也让学术研究者得以开发新算法与新技术，让 RL 研究走进了学术界的可及范围。

感谢 Kaichao 分享这段历史——他主导了 vLLM 在 OpenRLHF、verl 等框架中的早期 RL 集成。我们希望这能说明：真诚的合作与共享，而非恶性竞争与信息封锁，才是推动科学前行的力量。

# 结论

RL 训练系统效率本质上是队列健康问题。过采样、提前剪枝和部分 rollout 控制什么进入队列；自适应采样和策略陈旧控制什么离开队列；在途权重更新则允许训练器和生成器以不同速率运行。

RL 训练既是算法问题，同样是基础设施问题。本文聚焦系统层面，解释系统设计与算法设计如何交织，并用真实实验加以落地。我们希望这能点燃对 RL 基础设施的兴趣，在 RL 算法研究者与系统工程师之间架起桥梁。

我们计划在后续文章中继续探索 RL 训练的系统与基础设施。我们将深入探讨 PD 分离、投机解码等技术，以及大规模 RL 训练的系统挑战，例如 Nemotron 3 Ultra 的训练。我们也在研究对沙箱基础设施做基准测试，以及分析模型 rollout 轨迹。

如果你对这些方向感兴趣，我们在招人！请联系 [letsgo@semianalysis.com](mailto:letsgo@semianalysis.com)。附上你的简历，也欢迎向我们提出关于本文的问题。

最后一节，我们给出 RL 训练的 TCO 分析，并将其与 Thinking Machines Lab 的 RL 训练平台 Tinker 比较。我们量化 Tinker 的成本效率高出多少，并对背后的原因提出假设。

## RL 训练 TCO 分析

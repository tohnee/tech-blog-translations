---
title: "从研究到生产：在 Vertex 上用 EAGLE-3 加速开源大语言模型"
title_en: "From research to production: Accelerate OSS LLM with EAGLE-3 on Vertex"
author: "Ivan Nardini, Charles Chen, Ying Wang"
date: "December 1, 2025"
previewImg: /images/blog/eagle3-vertex/cover.png
source: https://lmsys.org/blog/2025-12-01-eagle3-vertex/
translated: 2026-09-12
---

# 从研究到生产：在 Vertex 上用 EAGLE-3 加速开源大语言模型

> 原文：[From research to production: Accelerate OSS LLM with EAGLE-3 on Vertex](https://lmsys.org/blog/2025-12-01-eagle3-vertex/) · LMSYS Blog · Ivan Nardini, Charles Chen, Ying Wang

**TL;DR：** 投机解码可以提升 LLM 推理速度，但传统方法需要一个独立的、效率不高的草稿模型。Vertex AI 采用 EAGLE-3：在模型内部层上附加一个小型草稿头（draft head，约为目标模型大小的 2–5%），从而简化训练并获得约 2–3 倍的解码加速。**本文介绍我们的完整流水线：数据清洗、嵌入生成、训练，以及在 Vertex AI 上用 SGLang 大规模服务 EAGLE-3。**

<img src="/images/blog/eagle3-vertex/cover.png" alt="" width="50%" />
</p>

对大语言模型（LLM）从业者来说，"一次只能生成一个 token"的瓶颈再熟悉不过。标准的自回归生成天然是串行的。这造成了一个典型的访存受限（memory-bound）过程：速度的限制不是来自计算，而是来自**每一步**都要从显存中读取海量模型权重所花的时间，导致 GPU 算力利用率低下。

解决方案就是**投机解码**。这项优化技术通过引入草稿机制，加速大模型（目标模型）逐个 token 生成的缓慢串行过程。

草稿机制会一次性快速提出多个候选的下一个 token；随后大目标模型以单次并行批量验证这些提议，接受与自己预测相匹配的最长前缀，并从这个新位置继续生成。

但草稿机制并非都同样优秀。经典的"草稿-目标"（draft-target）方案使用一个独立的、更小的 LLM 作为草稿器（drafter），这意味着你必须托管和管理更多的服务资源，带来额外成本。

<p align="center">
  <img src="/images/blog/eagle3-vertex/draft_model.png" alt="" width="50%" />
</p>

这正是 [EAGLE-3](https://arxiv.org/abs/2503.01840)（Extrapolative Attention Guided LEarning）的用武之地。EAGLE-3 是一种更先进的方法：它不再使用一个完整的独立模型，而是将一个极其轻量的"草稿头"——仅为目标模型大小的 2–5%——直接挂载到目标模型的内部层上。这个草稿头同时在特征层和 token 层工作，吸收目标模型隐藏状态中的特征，外推并预测一棵未来 token 树。

结果如何？既收获了投机解码的全部好处，又免除了训练和运行第二个模型的开销。

与训练和维护一个独立的、参数量动辄数十亿的草稿模型这一复杂且资源密集的任务相比，EAGLE-3 的方法高效得多。你只需训练一个轻量的"草稿头"——仅为**目标模型大小的 2% 到 5%**——并将其作为附加部分加入现有模型。这一更简单、更高效的训练过程，可为 Llama 70B 这类模型带来**显著的 2–3 倍解码性能提升**（具体取决于负载类型，例如多轮对话、代码、长上下文等）。

<img src="/images/blog/eagle3-vertex/target_model_eagle3.png" alt="" width="50%" />
</p>

但要把如此精简的 EAGLE-3 方案从论文走向规模化、可用于生产的云服务，依然是一段实打实的工程历程。本文将分享我们的技术流水线、关键挑战，以及一路走来来之不易的经验教训。


## 挑战一：准备数据

EAGLE-3 草稿头需要训练。最直观的第一步是找一个公开可用的通用数据集。但大多数此类数据集都存在以下问题：

- **严格的使用条款：** 这些数据集由某些模型生成，其条款不允许用它们来开发与原提供方相竞争的模型。
- **PII 污染：** 部分数据集包含大量个人身份信息（PII），包括姓名、位置，甚至金融标识符。
- **质量无保证：** 一些数据集只在通用的"演示"场景下表现出色，却未必适合真实客户的专门化负载。

直接使用这些数据并不可行。

### 经验一：构建合成数据生成流水线

一个解决方案是构建合成数据生成流水线。根据客户的使用场景，我们选择的数据集不仅要质量高，还要与客户在各种不同负载下的生产流量**匹配度最高**。接着，只从这些数据集中抽取用户 prompt，并施加严格的 DLP（数据防泄漏，Data Loss Prevention）与 PII 过滤。这些干净的 prompt 套用聊天模板、完成分词后，即可送入你的目标模型（如 Llama 3.3 70B）以收集其响应。

这种方式得到的目标模型自生成数据，不仅合规、干净，而且与模型真实的输出分布高度匹配，是训练草稿头的理想数据。

<img src="/images/blog/eagle3-vertex/data_pipeline.png" alt="" width="50%" />
</p>

## 挑战二：搭建训练流水线

另一个关键决策是如何向 EAGLE-3 草稿头提供训练数据。有两条不同的路径：**在线训练**——嵌入"边训边生成"；以及**离线训练**——"嵌入在训练开始前预先生成"。

在我们的场景中，我们选择了**离线训练**，因为它所需的硬件资源远少于在线训练。这一流程会在训练 EAGLE-3 草稿头之前预先计算好所有特征和嵌入，并保存到 GCS，作为轻量 EAGLE-3 草稿头的训练数据。数据就绪后，训练本身很快：**由于 EAGLE-3 草稿头体积极小，使用我们原始数据集的初始训练在单台主机上只需约一天。**不过，随着数据集规模的扩大，训练时间也相应增加，如今已需要数天。

<img src="/images/blog/eagle3-vertex/training_pipeline.png" alt="" width="50%" />
</p>

这个过程让我们记住了两条不容忽视的经验。

### 经验二：聊天模板不是可选项

在为指令微调模型训练时我们发现，一旦聊天模板不对，EAGLE-3 的性能可能波动很大。在生成特征和嵌入之前，必须套用目标模型专属的聊天模板（例如 Llama 3 的模板）。如果只是简单拼接原始文本，嵌入就会出错，你的草稿头将学到错误的分布。

### 经验三：注意掩码

训练时，模型会同时接收 prompt 和**响应（response）**的表示。但 EAGLE-3 草稿头只应学习预测响应的表示。你必须在损失函数中手动将 prompt 部分掩掉。如果**不这样做**，草稿头会把容量浪费在学习预测"它本来就已拿到的 prompt"上，性能会因此受损。

<img src="/images/blog/eagle3-vertex/mind_mask.png" alt="" width="50%" />
</p>


## 挑战三：服务与扩展

训练好 EAGLE-3 草稿头之后，我们进入服务**阶段**。这个阶段带来了不小的规模化挑战。以下是我们最重要的心得。

### 经验四：推理服务框架是关键

通过与 SGLang 团队紧密合作，我们成功以最佳性能将 EAGLE-3 落地到生产环境。技术原因在于 SGLang 实现了一个关键的树注意力（tree attention）内核。这个特殊内核至关重要，因为 EAGLE-3 生成的是一棵由各种可能性组成的"草稿树"（而不只是一条简单的链），而 SGLang 的内核正是为在单步中并行验证所有这些分支路径而专门设计的。没有它，性能就会白白流失。

### 经验五：别让 CPU 成为 GPU 的瓶颈

即使已经用 EAGLE-3 加速了你的 LLM，你还可能撞上另一堵性能高墙：**CPU**。当 GPU 在运行 LLM 推理时，未经优化的软件会在 CPU 开销上浪费大量时间——例如 kernel 启动和元数据记账。在普通的同步调度器中，GPU 执行一步（如 Draft 草拟），随后在 CPU 完成记账并启动下一步 Verify 验证期间处于空闲。这些同步空泡不断累积，浪费掉大量宝贵的 GPU 时间。

<img src="/images/blog/eagle3-vertex/normal_scheduling.png" alt="" width="50%" />
</p>

我们通过 SGLang 的**零开销重叠调度器（Zero-Overhead Overlap Scheduler）**解决了这个问题。该调度器专门针对投机解码多步的 *Draft -> Verify -> Draft Extend* 工作流做了调优。关键在于让计算重叠：当 GPU 忙于执行当前的 Verify 步骤时，CPU 已经在并行准备启动下一步 Draft 和 Draft Extend 步骤的 kernel。借助 `FutureMap`——一种智能数据结构，让 CPU 在 GPU 仍在工作时就能准备好下一批任务——GPU 的下一个作业始终就绪，从而消除了空闲空泡。
<img src="/images/blog/eagle3-vertex/overlap_scheduling.png" alt="" width="50%" />
</p>

通过消除这部分 CPU 开销，重叠调度器为我们带来了全面的额外 **10%–20% 加速**。这证明了一个优秀的模型只是成功的一半；你还需要一个跟得上的运行时。

## 基准测试结果
走完这段历程，这一切值得吗？绝对值得。

我们使用 SGLang、以 Llama 4 Scout 17B Instruct 为对象，将训练好的 EAGLE-3 草稿头与非投机解码基线进行了对比测试。基准测试显示，视负载类型不同，可获得 **2–3 倍的解码延迟加速以及显著的吞吐量提升**。

完整细节请参见我们的综合 notebook，你也可以自行运行基准测试。

### 指标一：每输出 token 中位时间（TPOT）

<img src="/images/blog/eagle3-vertex/tpop_benchmark.png" alt="" width="50%" />
</p>

这张图展示了 EAGLE-3 更优的延迟表现。**每输出 token 时间（TPOT）图**显示，在所有测试并发级别下，经 EAGLE-3 加速的模型（绿线）始终比基线（蓝线）保持更低（更快）的延迟。

### 指标二：输出吞吐量

<img src="/images/blog/eagle3-vertex/output_throughput.png" alt="" width="50%" />
</p>

这张图进一步凸显了 EAGLE-3 的吞吐量优势。**token 吞吐量 vs. 并发图**清楚地表明，经 EAGLE-3 加速的模型（绿线）始终大幅优于基线模型（蓝线）。

尽管在更大的模型上也观察到类似结论，但值得注意的是，相比其他性能指标，首 token 延迟（TTFT）可能会有所上升。此外，这些性能表现因任务而异，如下例所示：

<img src="/images/blog/eagle3-vertex/output_speed.png" alt="" width="50%" />
</p>

## 结语：轮到你了
EAGLE-3 不只是一个研究概念，而是一种可投入生产的模式，能带来实打实的 2 倍解码延迟加速。但要让它规模化，需要扎实的工程投入。要为你的用户可靠地部署这项技术，你需要：

1. **构建**合规的合成数据流水线。
2. **正确处理**聊天模板和损失掩码，并在大规模数据集上训练模型。

在 Vertex AI 上，我们已经为你把整个流程精简化，提供了专为扩展你基于 LLM 的应用而设计的优化容器与基础设施。要开始使用，请查阅以下资源：
- [文档](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/self-deployed-models)
- [基准测试 notebook](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/open-models)


## 感谢阅读

欢迎就 Vertex AI 向我们反馈和提问。

- Ivan Nardini：[LinkedIn](https://www.linkedin.com/in/ivan-nardini/) 与 [X](https://twitter.com/IlNardo92)
- Charles Chen：[LinkedIn](https://www.linkedin.com/in/pengyu-charles-chen/)
- Ying Wang：[LinkedIn](https://www.linkedin.com/in/ynwang007/)
- Harrison Lim：[LinkedIn](https://www.linkedin.com/in/hongyun-harrison-lim/)

## 致谢
我们要向 [SGLang](https://github.com/sgl-project/sglang) 团队——特别是 Ying Sheng、Lianmin Zheng、Yineng Zhang、Xinyuan Tong、Liangsheng Yin——以及 [SGLang/SpecForge](https://github.com/sgl-project/SpecForge) 团队——特别是 Shenggui Li、Yikai Zhu——致以诚挚的感谢，感谢他们在整个项目中给予的宝贵支持。他们无私的帮助和深入的技术洞见，是本项目取得成功的关键。

---
title: "DGX Spark 本地 PyTorch 使用体验"
title_en: "DGX Spark for Local PyTorch"
source: https://sebastianraschka.com/blog/2025/dgx-impressions.html
crawled: 2026-09-06
translated: 2026-09-06
---

# DGX Spark 本地 PyTorch 使用体验

> 原文：[DGX Spark for Local PyTorch](https://sebastianraschka.com/blog/2025/dgx-impressions.html)

用于本地 LLM 推理和微调的 DGX Spark 最近是个热门话题。我自己上手玩了一台，主要用 PyTorch 来做和跑 LLM，收集了一些基准测试结果和心得体会。

![图 1：DGX 放在我的 Mac Mini 旁边，用一个茶壶（和一台 13 英寸 MacBook Air）作参照。两者大小差不多，而且都非常安静（这对办公室或桌面使用来说很棒）。](https://sebastianraschka.com/images/blog/2025/dgx-impressions/01.webp)

图 1：DGX 放在我的 Mac Mini 旁边，用一个茶壶（和一台 13 英寸 MacBook Air）作参照。两者大小差不多，而且都非常安静（这对办公室或桌面使用来说很棒）。

## 常见用例：本地推理

大多数人用 DGX Spark 配合 [Ollama](https://ollama.com) 之类的工具做本地推理。我之前在 Mac Mini 上也是这么做的。

DGX 在这方面的体验类似，但有一个重大差别：它有 128 GB 显存，因此可以运行比我常用的 `gpt-oss-20B` 更大的模型。

不过，若要做公平的对比：在 Ollama 中使用针对 [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") 模型优化的 `mxfp4` 精度时，DGX Spark 和 Mac Mini M4 Pro 运行 `gpt-oss-20B` 都能达到约 45 token/秒。

我下面的基准测试更侧重 PyTorch，但如果你对 Ollama 用例感兴趣，LMSYS 的[这篇博文](https://lmsys.org/blog/2025-10-13-nvidia-dgx-spark/)有更多细节。

话虽如此，对我来说更有意思的是把它当作我纯 PyTorch 项目的原型机和开发机。

下面是与我的 Mac Mini，以及我通常通过云服务商使用的 H100 和 A100 卡的若干[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")对比。

## 1. 用从零实现的 0.6B 模型做推理

在这一节，我让各台机器在同一个我用纯 PyTorch 从零实现的小型 0.6B LLM 上比拼。这是我目前在《Build a [Reasoning Model](https://sebastianraschka.com/glossary/#reasoning-model "Reasoning Model") (From Scratch)》（《从零构建推理模型》）一书中使用的模型。

具体来说，我让这个 0.6B 参数的模型为简单提示词生成回答，分别在使用和不使用 KV 缓存的情况下运行，结果如下所示。

![图 2：一个简单的推理任务，提示模型生成一段 30 token 的简短回答。](https://sebastianraschka.com/images/blog/2025/dgx-impressions/02.webp)

图 2：一个简单的推理任务，提示模型生成一段 30 token 的简短回答。

**注意：所有实验都在 PyTorch 2.9 下运行。我在 Mac GPU（PyTorch 中的 "mps" 后端）上运行编译模型时遇到的 `InductorError` 已在 2.9 中解决。**

DGX Spark 大幅领先于 Mac Mini M4 Pro，与贵 6 倍的 H100 数据中心 GPU 大致相当，这令人印象深刻。

遗憾的是，由于 PyTorch MPS 的限制，我无法在 Mac 上运行编译版本。MPS 在改进，但仍不及 CUDA。

题外话：顺便说一下，这是一个相对较小的模型，[KV 缓存](https://sebastianraschka.com/glossary/#kv-cache "KV Cache")是动态的、在运行时分配，以进一步减少内存占用。这意味着 KV 缓存会随回答长度增长，而不是使用预分配数组——预分配数组对 GPU 和编译来说更优。我特意把它实现成动态方式来降低内存需求，因为内存往往是大多数读者的主要瓶颈。这就是为什么你可能会在图中看到一些奇怪之处，比如 KV 缓存版本在 GPU 上比非 KV 缓存版本略慢。在这个实验里提示词足够短，所以在 GPU 上硬算一切并不是大问题（但你可以看到 Mac Mini 的 CPU 从 KV 缓存中受益很多）。

对于更长的提示词，KV 缓存版本在所有情况下都是明显的赢家。

你可以在下面找到复现这些结果的代码：<https://github.com/rasbt/reasoning-from-scratch/tree/main/ch02/01_main-chapter-code>

## 2. 在 MATH-500 上评估 0.6B 基座模型与推理模型

这个基准测试扩展了上一个，在一个[基座模型](https://sebastianraschka.com/glossary/#base-model "Base Model")和一个推理模型之间比较 500 个 MATH-500 提示词，这些提示词产生的回答长度差异巨大。（这里我使用未编译的 KV 缓存版本。）

下面的图展示了顺序运行（每次一个提示词）和批量运行（一次 128 个提示词）的评估结果。

![图 3：基座模型与推理模型在 MATH-500 上的对比。y 轴为总运行时间，越低越好。](https://sebastianraschka.com/images/blog/2025/dgx-impressions/03.webp)

图 3：基座模型与推理模型在 MATH-500 上的对比。y 轴为总运行时间，越低越好。

总体而言，推理模型比基座模型慢得多，因为它生成的回答长得多。基座模型的平均回答长度是 96.74 个 token，而推理模型的平均回答长度是 1361.21 个 token。

如图 3 所示，在顺序运行（2a）中，DGX Spark 甚至跑赢了贵 6 倍的 H100，这再次令人印象深刻。但在批量运行中，H100 是明显的赢家。这大概是因为它好得多的内存带宽。

注意我没有在我的 Mac Mini 上运行推理模型，因为它跑起来非常烫（据我使用的 [stats](https://github.com/exelban/stats) 工具显示超过 100 °C，也就是水的沸点）。我不想让它连续 3 个多小时保持那么高的温度，因为担心损坏它——它可是我的主力工作机。

DGX Spark（NVIDIA 借给我的）运行时也相当热，但我猜它就是为这种负载设计的。（另外，上面也没有什么重要数据。）

你可以在下面找到复现这些实验的代码：<https://github.com/rasbt/reasoning-from-scratch/tree/main/ch03/02_math500-verifier-scripts>

## 3. 训练 / 微调一个 355M 模型

前面我们看到，DGX Spark 很适合单序列生成，但与 H100 相比不大适合大批量推理。那么小规模的训练和后训练运行呢？

我运行了简短的预训练（3a）、[监督微调](https://sebastianraschka.com/glossary/#instruction-finetuning "Instruction Finetuning (SFT)")（3b）和 DPO 偏好微调（3c）来对比不同系统，如下图所示。

![图 4：预训练、监督微调与 DPO 偏好微调的对比。](https://sebastianraschka.com/images/blog/2025/dgx-impressions/04.webp)

图 4：预训练、监督微调与 DPO [偏好微调](https://sebastianraschka.com/glossary/#dpo "DPO (Direct Preference Optimization)")的对比。

注意，这些实验我是在 A100 而不是 H100 上跑的，因为当时手头没有 H100。

在这三类任务上，DGX Spark 和 A100 都明显快于 Mac Mini。

这些运行都很短，但它们表明 DGX 能够高效地处理较小规模的训练和微调任务。

复现这些运行的代码链接如下：

- 预训练（3a）：<https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/01_main-chapter-code>（但要把模型从 127M 改为 355M。）
- SFT 微调（3b）：<https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07/01_main-chapter-code>
- DPO 微调（3c）：<https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07/04_preference-tuning-with-dpo>

## 结论

总体而言，DGX Spark 似乎是一台可以安静地摆在 Mac Mini 旁边的小巧工作站。它体积同样小巧，但拥有更多 GPU 内存，当然（这一点很重要！）还有 CUDA 支持。

2018 年我曾有一台装了 4 块 GTX 1080Ti GPU 的 Lambda 工作站。我需要那台机器做研究，但它给办公室带来的噪音和热量让人难以忍受，这也是我最终把机器搬到 UW-Madison 专用机房的原因。在那之后，我再没考虑过买另一台 GPU 工作站，而是完全依赖云 GPU。（只有当我搬进带大地下室和独立隔间的房子时，也许才会重新考虑。）相比之下，DGX Spark 对办公室使用来说绝对够安静。即使在满负载下也几乎听不见。

它还附带了让远程使用无缝衔接的软件，你可以直接从 Mac 连接，无需额外外设，也不需要 SSH 隧道。这对全天随时做快速实验来说是一大加分项。

但当然，在大规模训练方面，它**不能替代 A100 或 H100 GPU**。
我更把它看作一台开发和原型系统，让我可以在不让 Mac 过热的情况下卸载实验。我把它当作一台中间定位的机器，用来做较小的运行，并在把模型放到云 GPU 上运行之前在 CUDA 环境中测试模型。

**简而言之：** 如果你不指望奇迹或完整的 A100/H100 级性能，DGX Spark 是一台适合在家做本地推理和小规模微调的好机器。

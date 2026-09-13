---
title: "Inkling 架构与基准测试笔记"
title_en: "Inkling Architecture and Benchmark Notes"
source: https://sebastianraschka.com/blog/2026/inkling-architecture-benchmark-notes.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Inkling 架构与基准测试笔记

> 原文：[Inkling Architecture and Benchmark Notes](https://sebastianraschka.com/blog/2026/inkling-architecture-benchmark-notes.html)

Thinking Machines Lab 发布了 [Inkling](https://thinkingmachines.ai/news/introducing-inkling/)，一个 975B 参数的开放权重专家混合（MoE）模型。它每个 token 激活 41B 参数，支持最高 1,048,576 token 的[上下文窗口](https://sebastianraschka.com/glossary/#context-length "Context Length")。

这些数字让 Inkling 与 Kimi K2.5 和 GLM-5.2 处于大致相同的规模级别。然而，它的架构里有一些我不太常见的细节，包括每个解码器块内部的短卷积（ShortConv），以及用可学习的相对位置偏置替代[旋转位置嵌入（RoPE）](https://sebastianraschka.com/glossary/#rope "Rotary Positional Embeddings (RoPE)")。

![Inkling 架构图与发布时的基准测试对比，对比对象包括 GLM-5.2、Nemotron 3 Ultra、Kimi K2.5、GPT 5.6 Sol 和 Claude Fable 5](https://sebastianraschka.com/images/blog/2026/inkling/hero.webp)

图 1：Inkling 架构与发布时的[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")对比。左图概括了 975B MoE 及其局部-全局注意力模式。基准测试面板使用 Thinking Machines Lab 于 2026 年 7 月 15 日发布的结果。所有 Inkling 结果均使用 0.99 的 effort 设定。更大的架构图可在 [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/#card-inkling) 中查看。

## 41B 的激活参数规模

Inkling 有 66 个解码器层，隐藏维度为 6,144。前两层使用稠密前馈模块。其余各层包含 256 个路由专家和 2 个共享专家。每个 token 选择 6 个路由专家，两个共享专家始终处于激活状态。

由此算来，激活比例约为 4.2%。作为对比，GLM-5.2 总参数 744B、激活 40B；Kimi K2.5 总参数 1T、激活 32B。因此，尽管 Inkling 的总参数比 GLM-5.2 多出 231B，其激活规模与 GLM-5.2 接近。

Inkling 还是一个原生多模态模型。图像和视频帧经过一个四层 hMLP，音频则使用 Thinking Machines Lab 提出的 dMel 表示。得到的表示与文本一起进入同一个解码器，模型输出文本。

## 局部与全局分组查询注意力

在 66 个解码器层中，55 层使用滑动窗口注意力，11 层使用全局注意力。这让 Inkling 呈现出以 5:1 循环的局部-全局模式。局部层有 512 token 的窗口，使用 64 个查询头和 16 个键值头，即 4:1 的[分组查询注意力（GQA）](https://sebastianraschka.com/glossary/#gqa "Grouped-Query Attention (GQA)")比例。全局层保留 64 个查询头，但只使用 8 个键值头，把 GQA 比例提高到 8:1。

不同寻常之处在于[位置信息](https://sebastianraschka.com/glossary/#positional-encoding "Positional Encoding")。Inkling 不用 RoPE，而是从查询和键的状态计算出一个可学习的、依赖于输入的相对位置偏置。它还在注意力之前对查询头和键头做 RMS 归一化。

该偏置在局部层覆盖完整的 512 token 跨度；在全局层，其配置的范围是 1,024 token。更靠前的 token 仍然可以被关注到，但它们不会获得显式的可学习相对位置项。只读发布文的话很容易漏掉这个细节。它可以在[配置文件](https://huggingface.co/thinkingmachines/Inkling/blob/main/config.json)和 [Transformers 实现](https://github.com/huggingface/transformers/blob/main/src/transformers/models/inkling/modular_inkling.py)中看到。

## 每层四个短卷积

每个解码器层包含四个核大小为 4 的因果卷积。其中两个直接在键和值的投影之后运行。另外两个则在注意力分支和 [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") 分支的输出汇入残差流之前处理它们。

这些小卷积为该块提供了一条在邻近 token 之间混合信息的显式通路。发布内容没有包含隔离其效果的消融实验，因此不清楚 Inkling 的质量或训练稳定性有多少来自这一选择。

还有一个归一化细节。在 token 嵌入查找之后、第一个解码器块之前，直接应用了一个单独的 [RMSNorm](https://sebastianraschka.com/glossary/#rmsnorm "Root Mean Square Layer Normalization (RMSNorm)")。这一嵌入归一化在发布的配置中是启用的，并在实现中表现为一个独立的操作。

## 训练与 effort 控制

Thinking Machines Lab 报告了 45T [预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining") token，涵盖文本、图像、音频和视频。训练设置对模型的大型矩阵参数使用 Muon，对其余参数使用 Adam。权重衰减与学习率的平方耦合。

后训练始于对来自开放权重教师模型（包括 Kimi K2.5）的合成数据做监督微调。随后，大部分后训练算力投入了跨越合成与人工创建环境的强化学习。根据发布内容，团队收集了超过 3000 万条 RL rollout。

一个实用产物是 effort 控制。系统消息告诉 Inkling 要投入多少 effort，同时训练期间的每 token 成本会鼓励更短或更长的回答。这有助于在不维护单独检查点的情况下，在输出长度与基准测试表现之间做权衡。

## 参差不齐的基准测试快照

报告的 GLM-5.2 对比展现了 Inkling 的整体基准测试面貌。Inkling 在 IFBench 上得 79.8，GLM-5.2 为 73.3；在 SimpleQA Verified 上为 43.9 对 38.1。GLM-5.2 则在无工具 HLE 上领先（40.1 对 29.7）、SWE-Bench Pro Public 上领先（62.1 对 54.3）、Terminal-Bench 2.1 上领先（82.7 对 63.8）。

我会把这些当作发布时点的快照。所有 Inkling 结果使用 0.99 的 effort 设定和 1.0 的[温度](https://sebastianraschka.com/glossary/#temperature "Temperature")。编程评估允许最多 256K token 的轨迹。若干对比值来自外部报告，而 Inkling 的 Terminal-Bench 结果使用内部执行框架（harness）。不同设置之间的小差距很难解读。

发布内容还展示了 effort 扫描，而不是单一运行点。在 Terminal-Bench 上，Thinking Machines Lab 报告 Inkling 以约三分之一的生成 token 量达到 Nemotron 3 Ultra 的分数。这是一个有用的结果，尽管服务方层面的吞吐量对比仍然需要相同的量化方式、批大小、专家并行设置、注意力算子和硬件。

对我来说，悬而未决的问题现在已经相当具体。我希望看到针对短卷积、嵌入归一化和相对位置偏置的受控消融实验。我还希望看到与 Kimi K2.5 和 GLM-5.2 直接可比的吞吐量测量。这些结果将有助于厘清 Inkling 的架构选择主要提升的是质量、长上下文行为、训练稳定性，还是服务效率。

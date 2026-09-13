---
title: "六个值得关注的开放权重模型架构笔记"
title_en: "Six Open-Weight Model Architecture Notes"
source: https://sebastianraschka.com/blog/2026/notable-open-weight-models-this-week.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 六个值得关注的开放权重模型架构笔记

> 原文：[Six Open-Weight Model Architecture Notes](https://sebastianraschka.com/blog/2026/notable-open-weight-models-this-week.html)

是的，开源/开放权重模型对一个健康的 AI 生态至关重要。正因为如此，我们才能验证事情、核查各家声明，并在封闭实验室之外保持跟进。此外，如果我们还不准备通过使用闭源实验室的模型而把个人数据和知识产权交给他们，开放权重也给了我们用自己的硬件运行 AI 的自由。（这并不是说专有模型不好——实际上我自己也常用它们——但一个没有任何替代选项的生态是不健康的。）

总之，在几乎所有人都在等待 Kimi K3 和 Ling 3.0 权重随时登陆模型平台的同时，过去一周还有不少其他有意思的新开放权重模型发布。是的，又是这样的一周！

所以，以下是这些模型的架构图，以及一些我认为最值得关注的点的笔记：

1) Nanbeige 4.2 3B 使用了[循环深度共享](https://sebastianraschka.com/glossary/#looped-depth-sharing "Looped Transformer")。这基本上意味着它把同一个 22 层（= transformer 块）堆叠运行两次。也就是说，它把 22 层架构扩展到了 44 层，但不复制权重。（transformer 块计算量翻倍，但内存占用不变。）

为什么要这样做？相关信息有点少，但 Nanbeige 4.2 技术报告的 2.1 节说，两次通过给出了最佳权衡，并保留了一个标准架构约 75% 的 token 效率。更多次通过几乎没有收益，却让训练慢得多、贵得多。

2) Laguna S 2.1 是 poolside 的 Laguna 模型的一个非常合适的尺寸：118B 稀疏 MoE，激活参数 8B，配有 1M token 的[上下文窗口](https://sebastianraschka.com/glossary/#context-length "Context Length")。除此之外架构相当标准：36 个滑动窗口层和 12 个全局（门控）GQA 层。不过，考虑到这个尺寸，以及它（勉强）能在我的 DGX Spark 上跑起来（占用不到 80 GB 内存），这是我目前个人最感兴趣的模型。它比 Qwen3.6 35B 大 3 倍，因此稍微慢一点，但也许是"日常主力 Qwen3.6 35B 替代品"的一个好候选。（不过仍在等更多独立的性能基准测试。）

3) Motif-3-Beta 是一个新的 314B-A13B 稀疏 MoE，在 mHC 和[潜在注意力](https://sebastianraschka.com/glossary/#mla "Multi-Head Latent Attention (MLA)")方面大体上以 DeepSeek V4 为基础。但它使用了一个新组件——Grouped Differential Latent Attention，其灵感来自多头潜在注意力。也许过段时间我该专门写一篇文章，现在先给出要点：常规 MLA 把键和值压缩到更小的潜在表示中，主要是为了减小 KV 缓存的大小。GDLA 做了类似的低秩压缩，但把注意力头分成组，并且为每组学习一个噪声头，噪声会被减去用于过滤……总之，这是改日再聊的话题！

4) Solar Open 2 是 Upstage 的新 250B-A15B 混合 MoE，把三个 Kimi Delta Attention 层与一个 [GQA](https://sebastianraschka.com/glossary/#gqa "Grouped-Query Attention (GQA)") 层交替排布。

5) Antares 1B 是 Cisco 的一个小模型（还有一个更小的 0.3B 变体），以 IBM Granite 4.0 1B 骨干为起点，使用 SFT 加 [GRPO](https://sebastianraschka.com/glossary/#grpo "GRPO (Group Relative Policy Optimization)") 做面向终端的网络安全任务。这是一个在真正的小模型上做任务特定后训练的好例子。

6) BTL-3 是一个用于 Qwen3.6-27B 的 rank-32 LoRA 适配器，面向编程智能体和结构化工具使用。它非常强的[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")表现说明，LoRA 适配器在 2026 年仍然是一个有用的工具/技术。

我把这六个模型都添加到了 [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/)，里面有更多细节。

![组合图：Nanbeige 4.2、Laguna S 2.1、Motif-3-Beta、Solar Open 2、Antares 1B 和 BTL-3 的架构图，以及 Laguna S 2.1 的速度与内存图表](https://sebastianraschka.com/images/blog/2026/notable-open-weight-models-this-week/hero.webp)

图 1. 六个模型的架构图，随后是 Laguna S 2.1 的吞吐量与内存实测。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-302083551) 的网页版，略有编辑。

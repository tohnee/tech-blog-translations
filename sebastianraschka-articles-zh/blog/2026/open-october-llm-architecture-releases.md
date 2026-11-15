---
title: "Open October：LLM 架构发布汇总"
title_en: "Open October LLM Architecture Roundup"
source: https://sebastianraschka.com/blog/2026/open-october-llm-architecture-releases.html
crawled: 2026-11-16
translated: 2026-11-16
---

# Open October：LLM 架构发布汇总

> 原文：[Open October LLM Architecture Roundup](https://sebastianraschka.com/blog/2026/open-october-llm-architecture-releases.html) · Sebastian Raschka's Blog

来补一下过去一个月里的 10 个（！）开放 LLM 架构发布。十月真是发生了不少事。

我想我们可以称之为「Open October」！

1. Kolibri-1（78B）：来自德国的一个值得关注的模型。采用经典的 Grouped Query Attention（GQA）和 Sliding Window Attention（SWA）注意力模块。
2. Ling 3.1 Flash（560B）：使用 Kimi Delta Attention，而第八个使用受 DeepSeek 启发的门控多头潜在注意力（Multi-head Latent Attention，MLA）。
3. Muse Spark Open（816B）：除 Muse Glimmer 之外，这是 Meta 自 Llama 以来首个重要的开放权重发布。采用经典 GQA + SWA，但加入了 LatentMoE。
4. Nemotron 3.5 Super VL（120B）：将 Mamba-2 层与仅八个注意力层结合，同样采用 LatentMoE。
5. Dory1.0（4B）：一种循环（looped）transformer 设计。
6. Reflection Beam（501B）：GQA+SWA 架构。
7. Recursive Flint（40B）：注意「Recursive」是公司名；架构是相当标准的 MoE，采用 GQA 和 SWA。
8. MiniMax M3.1-Flash（428B）：使用其自研的 MiniMax Sparse Attention 模块。
9. LFM3（1.7B）：混合架构，混合了短卷积与注意力。
10. Mistral Large 4（1T）：将 MLA 与稀疏注意力结合。

我计划在未来几周的下一篇 Substack 文章中更深入地介绍和讨论这些内容！

[![组合图：十个十月 LLM 发布的架构图与规格速览，从 Kolibri-1 到 Mistral Large 4](/images/blog/2026/open-october-llm-architecture-releases/open-october-architectures.webp)](/images/blog/2026/open-october-llm-architecture-releases/open-october-architectures.png)

十月这十个发布的[架构图与规格速览](/llm-architecture-gallery/)。点击图片查看全分辨率版本。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-377610833) 的网页版，略有编辑。

【译者注：第 2 条原文为 "Uses Kimi Delta Attention and the eighth uses gated Multi-head Latent Attention (MLA) inspired by DeepSeek"，其中 "the eighth" 指代不明，疑为原文笔误，译文照原文保留。】

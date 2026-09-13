---
title: "Gemma Scope 2：助力 AI 安全社区深入理解复杂语言模型行为"
title_en: "Gemma Scope 2: helping the AI safety community deepen understanding of complex language model behavior"
source: https://deepmind.google/blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/
site: deepmind
date: 2025-12-19
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemma Scope 2：助力 AI 安全社区深入理解复杂语言模型行为

> 原文：[Gemma Scope 2: helping the AI safety community deepen understanding of complex language model behavior](https://deepmind.google/blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/) · Google DeepMind

您的浏览器不支持 audio 元素。

**收听本文** 5 分钟

宣布一套全新的开放语言模型可解释性工具

大语言模型（LLM）能够完成令人惊叹的推理壮举，但其内部的决策过程在很大程度上仍不透明。当系统未能按预期运行时，由于缺乏对其内部工作机制的可见性，我们可能难以准确定位其行为的确切原因。去年，我们凭借 [Gemma Scope](https://deepmind.google/discover/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/) 推进了可解释性科学——这是一个工具包，旨在帮助研究人员理解 Gemma 2（我们轻量级开放模型系列）的内部工作机制。

今天，我们发布 [Gemma Scope 2](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/Gemma_Scope_2_Technical_Paper.pdf)：一套全面、开放的可解释性工具，覆盖从 270M 到 27B 参数的所有 [Gemma 3](https://deepmind.google/models/gemma/gemma-3/) 模型规格。这些工具能够让我们追踪潜在风险在模型整个「大脑」中的传播路径。

据我们所知，这是迄今为止 AI 实验室规模最大的可解释性工具开源发布。制作 Gemma Scope 2 涉及存储约 110 PB 的数据，并训练了总计超过 1 万亿的参数。

随着 AI 持续进步，我们期待 AI 研究社区使用 Gemma Scope 2 来调试涌现的模型行为，利用这些工具更好地审计和调试 AI 智能体，并最终加速开发实用、稳健的安全干预手段，以应对越狱、幻觉和谄媚等问题。

我们的[交互式 Gemma Scope 2](https://neuronpedia.org/gemma-scope-2) 演示由 Neuronpedia 提供，可供尝试。

## Gemma Scope 2 有何新意

可解释性研究旨在理解 AI 模型的内部工作机制和习得的算法。随着 AI 能力越来越强、结构越来越复杂，可解释性对于构建安全可靠的 AI 至关重要。

与上一代一样，Gemma Scope 2 充当 Gemma 语言模型家族的显微镜。通过结合稀疏自编码器（SAE）和转码器（transcoder），它让研究人员能够深入模型内部，观察模型正在思考什么，以及这些想法如何形成、如何与模型的行为相连接。这反过来又支持对越狱或其他与安全相关的 AI 行为进行更丰富的研究，例如模型的对外表述推理与其内部状态之间的差异。

虽然初代 Gemma Scope 已经支撑了安全关键领域的研究，例如[模型幻觉](https://openreview.net/forum?id=WCRQFlji2q)、[识别模型已知的秘密](https://arxiv.org/abs/2510.01070)和[训练更安全的模型](https://arxiv.org/abs/2507.16795)，但 Gemma Scope 2 通过几项重大升级支持更具雄心的研究：

- **大规模全覆盖**：我们为整个 Gemma 3 家族（最高 27B 参数）提供全套工具，这对研究只在大规模下才出现的涌现行为至关重要，例如此前由 27b 规模的 C2S Scale 模型发现的那种行为——它帮助发现了一条新的潜在癌症治疗通路。虽然 Gemma Scope 2 并未在该模型上训练，但这是这些工具或许能够理解的那类涌现行为的一个例子。
- **更精细的工具，用于解读复杂的内部行为**：Gemma Scope 2 包含在我们 Gemma 3 家族模型每一层上训练的 SAE 和转码器。[跳跃转码器](https://arxiv.org/abs/2501.18823)（Skip-transcoders）和[跨层转码器](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)（Cross-layer transcoders）让解读分布在模型各处的多步计算与算法变得更加容易。
- **先进的训练技术**：我们采用最先进的技术，尤其是[套娃训练技术](https://arxiv.org/abs/2503.17547)（Matryoshka），它帮助 SAE 检测更多有用的概念，并解决了 Gemma Scope 中发现的某些缺陷。
- **聊天机器人行为分析工具**：我们还提供面向针对聊天用例微调的 Gemma 3 版本的可解释性工具。这些工具能够分析复杂的多步行为，例如越狱、拒绝机制和思维链忠实度。

![可视化图示，演示 Gemma Scope 2 中的「网络诈骗与欺诈邮件特征」：高亮显示文本片段，其中特定的诈骗相关词语和短语（如「discounted（打折）」「Nigerian Prince（尼日利亚王子）」「defrauding（欺诈）」和「spot a scam（识破骗局）」）根据特征激活水平以不同深浅的蓝色着色。](https://lh3.googleusercontent.com/SAodJWaikLby_KETIdMf4JxhrsV1EVmwpDx-0-dG8Z_r4UyYGRBfkcTOKONYnL3fxvuiLsKES4cQqhV8mcCneh-FbFkGH5eesNOMwebMXbY1IcU_=w1440)![可视化图示，演示 Gemma Scope 2 中的「网络诈骗与欺诈邮件特征」：高亮显示文本片段，其中特定的诈骗相关词语和短语（如「discounted（打折）」「Nigerian Prince（尼日利亚王子）」「defrauding（欺诈）」和「spot a scam（识破骗局）」）根据特征激活水平以不同深浅的蓝色着色。](https://lh3.googleusercontent.com/wBRcx05qFoefApPsfuOyx_SvJmm_Xl50GIxgn32pGUhdVx018g-kx5SQpUXYaFi2Sjnqvkrzu17qmYXS1cyjq9otDLJEpdrew6ZaP3SnoEc1oVUURg=w1440)

这幅可视化展示了 Gemma Scope 2 如何利用稀疏自编码器和转码器，向研究人员呈现模型判定一封潜在欺诈邮件的过程。

## 推动领域前进

通过发布 Gemma Scope 2，我们旨在让 AI 安全研究社区能够使用一整套尖端的可解释性工具推动领域前进。这种全新水平的访问能力，对于解决只会在更大规模、更现代的 LLM 中出现的真实世界安全问题至关重要。

了解更多关于 Gemma Scope 的信息

[下载 Gemma Scope 2](https://huggingface.co/google/gemma-scope-2)[在 Neuronpedia 上查看我们的模型](https://www.neuronpedia.org/gemma-scope-2)[阅读我们的技术报告](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/Gemma_Scope_2_Technical_Paper.pdf)[试用我们的 Colab 教程](https://colab.sandbox.google.com/drive/1NhWjg7n0nhfW--CjtsOdw5A5J_-Bzn4r?usp=sharing)[查看我们的 Gemma Scope 页面](https://deepmind.google/models/gemma/gemma-scope/)

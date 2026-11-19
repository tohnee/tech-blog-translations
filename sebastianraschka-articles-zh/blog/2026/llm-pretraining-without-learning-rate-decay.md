---
title: "没有学习率衰减的预训练"
title_en: "Pre-Training Without Learning Rate Decay"
source: https://sebastianraschka.com/blog/2026/llm-pretraining-without-learning-rate-decay.html
crawled: 2026-11-19
translated: 2026-11-19
---

# 没有学习率衰减的预训练

> 原文：[Pre-Training Without Learning Rate Decay](https://sebastianraschka.com/blog/2026/llm-pretraining-without-learning-rate-decay.html) · Sebastian Raschka's Blog

这可能是新一轮预训练配方趋势的开端：不再有学习率（LR）衰减阶段。（在 Kolibri 中也能看到同样的做法。）

取而代之的是使用恒定学习率，并对最后 N 个检查点取平均（或使用滑动权重平均）。

我猜这在实践中会更方便，因为你不必事先确定总训练长度。

[![比较余弦衰减、warmup-stable-decay，以及带最后 N 个检查点权重平均的恒定学习率的学习率调度](/images/blog/2026/llm-pretraining-without-learning-rate-decay/pretraining-without-learning-rate-decay.webp)](/images/blog/2026/llm-pretraining-without-learning-rate-decay/pretraining-without-learning-rate-decay.jpg)

余弦衰减、warmup-stable-decay，以及带检查点平均的恒定学习率。点击图片查看全分辨率版本。

基于那些公开训练细节的模型做一点元分析。

* 经典余弦衰减：Llama 3、OLMo 2、OLMo 3、GLM-4.5、GLM-5、Kimi K3、Phi-4。
* WSD（「Warmup-Stable-Decay」，预热-稳定-衰减）：DeepSeek V3、DeepSeek V4、DeepSeek V4.1-Flash、Kimi K2、Kimi Linear、Nemotron 3 Nano、Nemotron 3 Super、SmolLM3、MiniMax M2。
* 无衰减（恒定学习率加检查点平均）：Kolibri-1（[在 LLM 图库中查看架构](/llm-architecture-gallery/#card-kolibri-1-78b)）、DatologyAI 的模型（[在 LLM 图库中查看架构](/llm-architecture-gallery/#card-datology-xl-30b-a3b)）。

来源：我那条 [X 帖子](https://x.com/rasbt/status/2122721652433715481) 的网站版本，略有编辑，其中引用了 [DatologyAI 关于权重平均的说明](https://x.com/datologyai/status/2122366636472869015)。

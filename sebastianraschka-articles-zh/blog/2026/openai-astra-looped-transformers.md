---
title: "OpenAI Astra 与循环 Transformer"
title_en: "OpenAI Astra and Looped Transformers"
source: https://sebastianraschka.com/blog/2026/openai-astra-looped-transformers.html
crawled: 2026-09-06
translated: 2026-09-06
---

# OpenAI Astra 与循环 Transformer

> 原文：[OpenAI Astra and Looped Transformers](https://sebastianraschka.com/blog/2026/openai-astra-looped-transformers.html)

围绕 OpenAI 的 Astra 模型是"循环深度或循环 transformer"的说法，炒作很多。我们来稍微澄清一下。

大约两个月前，我分享过 Nanbeige 的架构细节，其中有这样一句话："Nanbeige4.2-3B 从零开始在 28T token 上预训练，采用 Looped Transformer——通过复用层堆叠来增加容量，而不增加参数。"

是的，就是这样。循环 transformer 的想法只是在 transformer 块中复用层。

以 Nanbeige 为例，主要思路是把同一个 22 层堆叠（= transformer 块）运行两次而不是一次。这样实际上把 22 层架构扩展到了 44 层，但不复制权重。

简单来说，这大致把模型规模翻了一倍（如果我们暂时忽略嵌入层和输出层）。但它不需要 2 倍的存储和内存来承载这个模型——由于复用了组件，规模保持不变。不过，计算开销几乎翻倍，因为我们要把嵌入的文本送过几乎 2 倍数量的层。

为什么这么做？在 Nanbeige 4.2 技术报告中，研究人员发现两次通过给出了最佳权衡，并保留了标准架构约 75% 的 token 效率。（更多次通过几乎没有收益，却让训练慢得多、贵得多。）

虽然据我所知 Nanbeige 4.2 是第一个采用这一方法的知名开放权重模型，但这个想法可以追溯到 NeurIPS 论文 "Mixture-of-recursions: Learning dynamic recursive depths for adaptive token-level computation"。实际上，这篇论文提出的机制还要更精细一些：它增加了一个学习得到的路由器，决定每个 token 接受一次、两次还是更多次通过。这样，简单的 token 可以提前退出，而更难的 token 则获得额外的计算。

总之，Astra 可能是一个非常优秀的模型，但这不应该关乎"循环 transformer"这一点——它只是一个微小的架构调整。

另外，"这项新技术的工作方式会掩盖 AI 的部分或全部推理，也就是所谓的'思维链'"这一说法，就循环 transformer 方法而言并不一定成立。那位 The Information 的记者可能指的是某种其他技术，或者误解了循环 transformer 方法。

复用层本身并不会抑制可见的思维链。它只是在下一个 token 被生成之前，在隐藏状态中增加计算——和普通的 transformer 层做的事情一样。

但基于我们掌握的信息，唯一说得通的解释是：如果一个模型使用更多这类循环通过，它可能需要生成更少的中间推理 token。这样一来，它更多的计算发生在无法被读作文本的潜在激活中。但如果我们扩大模型规模，比如从 GPT 5.6 Luna 到 GPT 5.6 Sol，也会得到同样的效果。

![组合图：对比关于 OpenAI Astra 循环深度的说法、Nanbeige 4.2 的重复 transformer 层，以及 Mixture-of-Recursions 的路由机制](https://sebastianraschka.com/images/blog/2026/openai-astra-looped-transformers/openai-astra-looped-transformers.webp)

图 1. 关于 OpenAI Astra 循环深度的报道、Nanbeige 4.2 的循环 transformer，以及 Mixture-of-Recursions 中 token 级路由的对照。

关于循环深度和循环 transformer 的视频讲解，请看我下面的说明视频。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-328050608) 的网页版。

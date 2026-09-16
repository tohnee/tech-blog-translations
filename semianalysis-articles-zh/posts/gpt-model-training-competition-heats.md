---
title: "GPT 模型训练竞赛升温——Nvidia 遇到了货真价实的挑战者"
title_en: "GPT Model Training Competition Heats Up - Nvidia Has A Legitimate Challenger"
subtitle: "在训练 GPT 类大语言模型上，Cerebras 的成本已具竞争力"
date: 2022-12-01
source: https://newsletter.semianalysis.com/p/gpt-model-training-competition-heats
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# GPT 模型训练竞赛升温——Nvidia 遇到了货真价实的挑战者

> 原文：[GPT Model Training Competition Heats Up - Nvidia Has A Legitimate Challenger](https://newsletter.semianalysis.com/p/gpt-model-training-competition-heats) · SemiAnalysis

**在训练 GPT 类大语言模型上，Cerebras 的成本已具竞争力**

除非你一直住在与世隔绝的山洞里，否则都能看出大型语言 transformer 模型显然将改变世界。不信？去看看 [OpenAI 的 ChatGPT](https://openai.com/blog/chatgpt/)。它的能力令人惊叹，从[写代码](https://twitter.com/jasondebolt/status/1598243854343606273?s=20&t=kasqfQ4tE4S4VI_b52LEDQ)到[量子计算](https://twitter.com/quantumVerd/status/1598287336994967554?s=20&t=kasqfQ4tE4S4VI_b52LEDQ)到[搜索](https://twitter.com/jdjkelly/status/1598021488795586561?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw)到[艺术](https://twitter.com/GuyP/status/1598020781065527296?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw)到[创意写作](https://twitter.com/AndrewMayne/status/1598076165402419201?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw)到[黑客技术](https://twitter.com/moyix/status/1598081204846489600?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw)再到[医疗健康](https://twitter.com/RoxanaDaneshjou/status/1598170660186251264?s=20&t=m1Ds3k7SZSPq6hIuEZyPRw)。

如果你关注我们的新闻有一阵子了，你会知道我们的语法一向不怎么样，但过去几个月情况变了。我们甚至会在句子里用分号了！不，我们没雇编辑；我们用一个 GPT 类模型来检查语法并给出改写建议。一些公司甚至披露，语言模型的代码生成能力目前在其代码库的新增代码中占比高达 25%。

这些大语言模型让人难以下咽的苦果是训练成本。对于 OpenAI GPT3、Google Pathways、DeepMind Chinchilla、Nvidia Megatron 等大模型，需要一家财力雄厚的巨头来支付天价计算账单。自 GPT3 发布以来，讨论一直围绕几个指标展开：

1. [模型规模和数据集还能做多大？](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)
2. 训练要花多少钱？
3. 有没有人能打破 Nvidia 的护城河，毕竟它的 GPU 太贵了？

第一个问题的答案，请继续关注——就在这次的 NeurIPS 上，我们已经看到和听到了一些关于 OpenAI GPT4 以及 DeepMind 未来模型的疯狂传言。

至于第二和第三个问题，一些公司已经开始撬动这条护城河。虽然业内大多数玩家都在用 GPU，但 Google 和其姊妹公司 DeepMind 都在用自家的 TPU 训练大语言模型。此外，Google TPU 还有少数外部客户，其中之一便是 Cohere。Cohere 正在构建可通过 API 访问的大语言模型。

[Cerebras](https://www.cerebras.net/press-release/cerebras-unveils-andromeda-a-13.5-million-core-ai-supercomputer-that-delivers-near-perfect-linear-scaling-for-large-language-models) 这家制造[整片晶圆大小芯片](https://www.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes)的公司，发布了在其 Andromeda 系统上运行 GPT 风格模型的一些非常有说服力的基准测试。Andromeda 是一套由 16 台 CS-2 晶圆级系统组成的集群，合计拥有 1350 万个 AI 核心，由 284 颗 64 核 AMD EPYC Milan 处理器供数。这些系统通过其 SwarmX 互联链路连接在一起，提供超过 96.8 terabits 的带宽。

这是第一次有厂商在与 Nvidia 直接可比的关键 AI 训练战场——超大规模模型上——公布信息。很能说明问题的是：Intel、AMD、Graphcore、SambaNova 等公司都有训练专用芯片，却无法在搭载大模型的大规模集群上秀出他们所谓特别的硬件。

我们将 Cerebras 的结果与 [Mosaic ML](https://www.mosaicml.com/blog/gpt-3-quality-for-500k) 的结果做了对比。Mosaic ML 是一个机器学习训练编排平台。他们不绑定特定云和硬件，同时利用多个公有云以及自建数据中心来压低训练成本。作为「经过优化的 GPU 技术栈」的参照基准，Mosaic 很合适，而且它易于使用，因为用户不必去应付许多典型的硬件相关和扩展性问题。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6b85936b-aaa5-4ca3-ad71-6b9057905f23_1685x438.png)

在训练大型 GPT 风格模型上，Cerebras 与 Nvidia 的成本已经打平！

在较小的 GPT 模型上，Cerebras 落后于 Nvidia A100 GPU，但随着模型规模增大，它会逐渐追上来。

Cerebras 声称他们还能把效率提得更高，尤其是在引入[非结构化稀疏（unstructured sparsity）](https://www.cerebras.net/blog/harnessing-the-power-of-sparsity-for-large-gpt-ai-models)等技术之后。

Mosaic ML 也表示，凭借他们在后端实现的一些巧妙技术，他们现在还能做得更好。Mosaic 目前的目标是将训练一个 GPT-3 品质模型的成本从 $450k 降到 $100k。随着 Hopper 明年开始上市，它很可能带来显著的成本改善。

你在表格中可能还注意到另一项：训练天数。虽然我们确实列入了这一项，但建议不要太过较真。训练时间取决于你能拿到多大规模的芯片集群。除 batch size 问题外，GPU 和 Cerebras 晶圆级芯片的扩展性都近乎完美。Cerebras 最早的那批结果只用了 4 台 CS-2，最大规模的则用上了全部 16 台 CS-2。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cd750ee4-ce50-4c21-8fcc-5b65c08003a6_1366x617.png)

Cerebras 还提到长序列长度是「GPU 不可能做到的」。这话根本不成立。多家 LLM 公司和科技巨头都能用标准 GPU 毫不费力地处理长序列长度。

Cerebras 已与估值 $1.7B 的 AI 初创公司 Jasper 签署算力供应协议，这是个大新闻！

如果你喜欢这篇文章，请分享！

[分享](https://newsletter.semianalysis.com/p/gpt-model-training-competition-heats?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

[赠送订阅](https://newsletter.semianalysis.com/subscribe?&gift=true)

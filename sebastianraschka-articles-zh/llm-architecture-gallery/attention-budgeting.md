---
title: "逐层注意力预算"
title_en: "Layer-wise attention budgeting"
source: https://sebastianraschka.com/llm-architecture-gallery/attention-budgeting/
crawled: 2026-09-06
translated: 2026-09-06
---

# 逐层注意力预算

> 原文：[Layer-wise attention budgeting](https://sebastianraschka.com/llm-architecture-gallery/attention-budgeting/)

逐层注意力预算（layer-wise attention budgeting）指的是让不同层的注意力开销有所不同，而不是给每个 transformer 层都分配同样的完整注意力预算。一个近期的例子是 Laguna XS.2，它是 [Poolside](https://poolside.ai/)（一家专注于为编程场景训练大语言模型的欧洲公司）发布的第一款开放权重模型。近几年有几位我以前的同事加入了 Poolside，他们的团队人才济济。看到更多公司也开始以开放权重形式发布部分模型，是一件令人高兴的事。

言归正传，下图描绘的 Laguna XS.2 架构乍看之下非常标准。不过有一个细节我没有画出来（或者说，没能塞进这张图里），这就是我们可以称为"逐层注意力预算"的概念。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[文章章节](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A73-layer-wise-attention-budgeting-laguna-xs2)
[Laguna 配置](https://huggingface.co/poolside/Laguna-XS.2/blob/main/config.json#L142)

![Laguna XS.2 架构](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/laguna-xs2-architecture.webp)

图 9：Poolside 的 Laguna XS.2 架构。（原始出处：
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)。）

## 预算分配发生在哪里

Laguna 有 40 层，但它们并非都使用同样的注意力设置。其中 30 层是滑动窗口层，每个 token 只能回看 512 个 token 的局部窗口；另外 10 层使用完整注意力（full attention），可以访问整个上下文。这些全局层开销更大，而滑动窗口层则让 KV 缓存和注意力计算保持低廉。

这种滑动窗口与完整注意力混合的模式并非 Laguna XS.2 独有，例如 Gemma 4 也同时使用两种类型。

但新意在于逐层设置 query 头数量。Hugging Face 的 [`config.json`](https://huggingface.co/poolside/Laguna-XS.2/blob/main/config.json#L142) 中包含一个 `num_attention_heads_per_layer` 设置，因此 query 头的数量可以变化，而 KV 缓存的形状保持兼容。

![Laguna XS.2 中的逐层 query 头预算](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/laguna-xs2-attention-budgeting.webp)

图 10：Laguna 中的逐层 query 头预算。完整注意力层每个 KV 头对应 6 个 query 头，
而滑动窗口层每个 KV 头对应 8 个 query 头。（原始出处：
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)。）

## 头数配置

完整注意力层使用 48 个 query 头；滑动窗口层则为 64 个。两者的 KV 头数量都固定为 8，也就是说完整注意力是每个 KV 头对应 6 个 query 头，滑动窗口注意力是每个 KV 头对应 8 个 query 头。

这就是编码在 Laguna 配置中的逐层头预算。

## 为什么要改变预算？

按层改变模型容量的更宏观想法，至少可以追溯到 Apple 2024 年的 [OpenELM](https://arxiv.org/abs/2404.14619)。那么，这种设计的意义又是什么呢？

与 KV 共享类似，其要点在于把注意力容量花在最有用的地方，而不是给每一层相同的预算。完整注意力层要纵观整个上下文，因此 Laguna 给它们的 query 头反而比更廉价的滑动窗口模块更少。

（另外，还有一个较小的实现细节：Laguna 还应用了逐头的注意力输出门控，这与 Qwen3-Next 等模型有些类似；由于我在早前的文章中已经介绍过，这里就不再展开。）

参考资料

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A73-layer-wise-attention-budgeting-laguna-xs2)
[Laguna XS.2 config.json](https://huggingface.co/poolside/Laguna-XS.2/blob/main/config.json#L142)
[Poolside Laguna 深度解析](https://poolside.ai/blog/laguna-a-deeper-dive)
[OpenELM](https://arxiv.org/abs/2404.14619)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)

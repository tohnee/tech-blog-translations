---
title: "Muse Glimmer 30B 架构笔记"
title_en: "Muse Glimmer 30B Architecture Notes"
source: https://sebastianraschka.com/blog/2026/muse-glimmer-30b-architecture-notes.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Muse Glimmer 30B 架构笔记

> 原文：[Muse Glimmer 30B Architecture Notes](https://sebastianraschka.com/blog/2026/muse-glimmer-30b-architecture-notes.html)

哇，Meta 昨天发布了一个新的开放权重 LLM，这可是自美好的 Llama 时代以来头一回。

他们的 Meta Muse Glimmer 模型是一个 30B 多模态推理模型，采用类似 Gemma 的架构设计。（"Glimmer"很可能是对"Spark"的文字游戏——Spark 才是能力更强的那个模型，Glimmer 是从它蒸馏而来的。不过 Muse Spark 目前只能通过 Meta 的 Model API 使用。）

架构方面，以下是几个要点：

1. "只有" 131k 上下文窗口，而 Qwen3.6 和 Gemma 4 原生支持这一数字的两倍；这个尺寸还算合理，但在智能体执行框架（harness）的时代，可能偏短了一些。
2. 它是稠密模型，不是专家混合。（所以拿它与 Qwen3.6 27B 对比，比与 Qwen3.6 30B-A3B 对比更公平。）
3. 混合注意力，由分组查询注意力（GQA）和滑动窗口注意力（SWA）构成；SWA:GQA 的模式是 3:1 的局部:全局比例。作为对比，使用类似组件的 Gemma 4 等其他模型采用 5:1 的比例。
4. GQA 和 SWA 都采用门控注意力（gated attention）；门控注意力近几个月已相当常见。它基本上是对注意力输出施加一个 sigmoid 门，决定有多少注意力信息进入残差连接。有意思的一点是，它使用的是相对标准的 GQA 和 SWA，而不是 Nemotron 或 Qwen3.6 那类混合注意力机制。
5. 非常极端的 GQA 比例：32 个查询头，只有 2 个 KV 头；作为对比，Gemma 4 31B 在局部头使用 32 Q / 16 KV，在全局头使用 32 Q / 4 KV。这意味着 Meta Glimmer 的 KV 缓存非常小。

总体来看，最相似的架构大概是 Gemma 3 27B（包括 Gemma 风格的前置/后置 RMSNorm 摆放方式）和 Gemma 4 31B，但带有一些调整，比如用 SwiGLU 取代 GeGLU 激活函数、门控注意力，以及前面提到的更极端的 GQA:SWA 模式。

最突出的是它极高的 KV 缓存效率。

也就是说，KV CACHE / TOKEN 比率（BF16 下）为：

- Muse Glimmer：52 KiB（越低越好）
- Qwen3.6 27B：64 KiB
- Gemma 4 31B：840 KiB

建模性能方面，他们自己的基准测试显示它大多领先 Qwen3.6。而按照 Artificial Analysis Intelligence Index 上的独立综合基准，它略落后于 Qwen3.6（见下图）。所以，实际使用几天后才知道它真正的排名。

总体而言，它看起来是一个扎实的模型，尤其适合智能体工作流。最突出的是它极低的内存占用，以及相当快的 prefill 和解码速度。而且，能看到 Meta 再次发布开放权重，也着实令人高兴 :)。

![组合图：展示 Meta Muse Glimmer 30B 架构、DGX Spark 吞吐量与内存基准测试，以及 Artificial Analysis Agentic Index](https://sebastianraschka.com/images/blog/2026/muse-glimmer-30b-architecture-notes/muse-glimmer-30b.webp)

图 1. Meta Muse Glimmer 30B 架构、DGX Spark Ollama 基准测试，以及 Artificial Analysis Agentic Index 对比。更多细节请见架构图库中的 [Muse Glimmer 30B](https://sebastianraschka.com/llm-architecture-gallery/#card-muse-glimmer-30b)。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-312570436) 的网页版。

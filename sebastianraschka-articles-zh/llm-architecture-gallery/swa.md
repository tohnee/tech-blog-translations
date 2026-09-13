---
title: "滑动窗口注意力（SWA）"
title_en: "Sliding Window Attention (SWA)"
source: https://sebastianraschka.com/llm-architecture-gallery/swa/
crawled: 2026-09-06
translated: 2026-09-06
---

# 滑动窗口注意力（SWA）

> 原文：[Sliding Window Attention (SWA)](https://sebastianraschka.com/llm-architecture-gallery/swa/)

那么，什么是滑动窗口注意力？如果把常规自注意力视为一种*全局*注意力机制——因为每个序列元素都可以访问其他所有序列元素——那么滑动窗口注意力就可以视为*局部*注意力，因为它把上下文大小限制在当前 query 位置附近。

一些架构会把这类局部层与少量全局注意力层组合使用，让信息仍然能够传遍整个序列。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[从零实现章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa)

![全局注意力与滑动窗口注意力的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/swa-global-vs-local.webp)

常规注意力（左）与滑动窗口注意力（右）的对比（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)）。

变化点

被选中的层只关注最近的一个窗口，而不是整个上下文

为什么使用它

局部层计算量更小、保留的缓存上下文更少；少量全局层保留对完整上下文的访问

示例架构

[Gemma 3 27B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-3-27b)、
[OLMo 3 32B](https://sebastianraschka.com/llm-architecture-gallery/#card-olmo-3-32b)、
[Xiaomi MiMo-V2-Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-xiaomi-mimo-v2-flash-309b)、
[Arcee Trinity](https://sebastianraschka.com/llm-architecture-gallery/#card-arcee-ai-trinity-large-400b)、
[Step 3.5 Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-step-3-5-flash-196b) 与
[Tiny Aya](https://sebastianraschka.com/llm-architecture-gallery/#card-tiny-aya-3-35b)

## 以 Gemma 3 为参照

例如，Gemma 2 采用混合注意力机制，以 1:1 的比例组合滑动窗口（局部）注意力与全局注意力。每个 token 可以关注附近 4k token 的上下文窗口。

Gemma 2 是每隔一层使用一次滑动窗口注意力，而 Gemma 3 的比例为 5:1，即每 5 个局部层才配 1 个全注意力层。Gemma 3 还把滑动窗口大小从 4096 缩小到 1024。

根据 Gemma 3 的消融研究，这种更激进的滑动窗口注意力使用方式对建模性能的影响微乎其微。

![Gemma 3 滑动窗口消融实验，显示质量损失很小](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/swa-gemma-ablation.webp)

Gemma 3 的消融研究表明，更小的窗口与更激进的局部对全局比例对困惑度几乎没有影响。依据论文：[Gemma 3 文章](https://arxiv.org/abs/2503.19786)
（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)）。

## 比例与窗口大小

局部对全局的层模式与注意力窗口大小，决定了模型使用 SWA 的激进程度。画廊中有几个例子：

- Gemma 3 与 Xiaomi 使用 5:1 的局部对全局模式。
- OLMo 3 与 Arcee Trinity 使用 3:1 模式。
- Xiaomi 还使用了 128 的窗口大小，比 Gemma 的 1024 小得多，因而也更激进。

SWA 本质上是一个可以把激进度调高或调低的旋钮。

![滑动窗口注意力相对于完整注意力的内存节省](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/swa-memory-savings.webp)

长上下文下的节省来自把许多全注意力层换成局部层，从而减少这些层需要考虑的缓存上下文数量（原始出处：
[*LLMs-from-scratch* SWA 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa)）。

## 为什么它常与 GQA 搭配出现

请注意，滑动窗口注意力既可以与[多头注意力](https://sebastianraschka.com/llm-architecture-gallery/mha/)搭配使用，也可以与[分组查询注意力（GQA）](https://sebastianraschka.com/llm-architecture-gallery/gqa/)搭配使用；Gemma 3 使用的就是 GQA。

这两种机制作用于缓存的不同部分：SWA 限制每个局部层保留多少上下文；GQA 则减少每个 token 缓存的 key 头与 value 头数量。

来源

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[LLMs-from-scratch SWA 章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)

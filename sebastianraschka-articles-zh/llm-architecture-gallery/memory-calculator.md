---
title: "LLM 内存计算器"
title_en: "LLM Memory Calculator"
source: https://sebastianraschka.com/llm-architecture-gallery/memory-calculator/
crawled: 2026-09-06
translated: 2026-09-06
---

# LLM 内存计算器

> 原文：[LLM Memory Calculator](https://sebastianraschka.com/llm-architecture-gallery/memory-calculator/)

估算推理期间模型权重和 KV 缓存所占用的内存。调整上下文长度或批大小，观察缓存如何增长而权重保持不变。

这些是逻辑负载的估算值。运行中的模型还需要为激活值、临时缓冲区以及其他运行时状态分配内存。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[KV 缓存计算说明](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

请启用 JavaScript 以使用计算器。下方的公式与假设无需 JavaScript 即可查看。

## 权重 + KV 缓存

等待设置中

运行时开销之前的负载估算值。

### 权重内存

不可用

模型的一份常驻副本。

### KV 缓存内存

不可用

覆盖所有序列。

[模型规格速览](https://sebastianraschka.com/llm-architecture-gallery/)
模型配置

当你完成一个控件的调整后，设置会保存在页面 URL 中。复制地址即可分享该估算结果。

## 估算原理

计算器使用画廊中取整后的参数量和 BF16 缓存数值。M、B、T 分别表示百万、十亿、万亿参数。内存以 GiB（2³⁰ 字节）显示；GB 则按 10⁹ 字节计算。

**权重字节数** = 参数量 × 权重位数 ÷ 8

**KV 缓存字节数** = 每 token 的 BF16 缓存字节数 × 上下文 token 数 × 批大小 × 缓存位数 ÷ 16

例如，Qwen3 8B 在画廊中估算的 BF16 缓存为每 token 144 KiB。在 32,768 个 token、批大小为 1 时，KV 缓存约为 4.5 GiB。其 80 亿参数在每权重 16 位时约占用 14.90 GiB。

- **常驻权重。**所有被统计的参数都保留在内存中，包括每一个 MoE 专家。每 token 激活参数量描述的是计算量，不能替代总权重数。权重在批内各样本间共享。
- **保留 token。**每个序列维护自己的缓存，不考虑共享前缀或束搜索。滑动窗口和分块模型在这里按全量保留估算，因为画廊没有提供各层的保留上限。会淘汰旧条目的运行时实际占用会更少。
- **架构范围。**缓存数值遵循画廊的逻辑表示，不包含固定循环状态、稀疏注意力索引缓冲区，以及可选的多 token 预测路径。特殊情况会在结果旁单独注明。
- **精度。**所选位宽统一应用于被统计的权重或缓存。量化缩放因子、零点、填充，以及以更高精度保留的张量都会增加内存。在这里选择某种格式并不意味着特定模型或运行时支持该格式。
- **运行时内存。**激活值、预填充工作区、分配器预留以及其他服务缓冲区均不计入。CPU 卸载和多 GPU 分布也未建模。仅凭这个总和无法判断一个模型能否装进一块 GPU。

GQA、MLA、共享缓存和循环混合架构的逐层公式见[画廊的逐层公式页面](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)。Transformers 文档解释了[缓存的工作原理](https://huggingface.co/docs/transformers/cache_explanation)以及[缓存策略对内存的影响](https://huggingface.co/docs/transformers/kv_cache)。

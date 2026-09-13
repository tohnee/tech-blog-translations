---
title: "DeepSeek 稀疏注意力（DSA）"
title_en: "DeepSeek Sparse Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/
crawled: 2026-09-06
translated: 2026-09-06
---

# DeepSeek 稀疏注意力（DSA）

> 原文：[DeepSeek Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)

DeepSeek 稀疏注意力（DeepSeek Sparse Attention, DSA）使用一个索引器（indexer）和一个 token 选择器（token selector）来保留可见前缀中一个学习得到的子集。被选中的 token 可以远在固定局部窗口之外。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)

![GLM-5 与 GLM-4.5 架构对比，展示 DeepSeek 稀疏注意力的采用](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-glm5-vs-glm45.webp)

图 1. GLM-5 将 DeepSeek 稀疏注意力与[多头潜在注意力](https://sebastianraschka.com/llm-architecture-gallery/mla/)结合使用（原始出处：[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)）。

概述

学习得到一种稀疏注意力模式

实际收益

减少长上下文注意力计算量

示例架构

[DeepSeek V3.2](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v3-2)、
[GLM-5](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-744b)、
[GLM-5.2](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-2) 与
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## 学习得到的稀疏性与固定窗口的对比

![常规因果注意力、滑动窗口注意力与 DeepSeek 稀疏注意力的并排对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-comparison.webp)

图 2. 完整因果注意力读取全部可见前缀；[滑动窗口注意力](https://sebastianraschka.com/llm-architecture-gallery/swa/)保留一个局部块；DSA 则学习一个子集（原始出处：[*From DeepSeek V3 to V3.2: Architecture, Sparse Attention, and RL Updates*](https://magazine.sebastianraschka.com/p/technical-deepseek)）。

## 索引器与选择器

lightning indexer（闪电索引器）按如下方式为当前位置 `t` 对较早位置 `s` 打分：

\[I\_{t,s} = \sum\_{j=1}^{H^I} w\_{t,j}\,\operatorname{ReLU}\!\left(q\_{t,j}\cdot k\_s\right).\]

```python
# t = current position, s = earlier positions, j = indexer head
scores[s] = sum(w[t,j] * relu(dot(q[t,j], k[s])) for j in heads)
selected  = top_k(scores, k=2048)
output    = sparse_attention(query_t, selected)  # O(Lk) over the sequence
```

![来自 DeepSeek V3.2 文章的 DeepSeek 稀疏注意力流程图](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-flow.webp)

图 3. 索引器先为前缀打分，随后选择器保留分数最高的条目（原始出处：[*From DeepSeek V3 to V3.2: Architecture, Sparse Attention, and RL Updates*](https://magazine.sebastianraschka.com/p/technical-deepseek)）。

## DSA 与 MLA 如何配合

[MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/) 压缩 [KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)中存储的内容；DSA 改变注意力操作读取哪些已存储的位置。

![DeepSeek V3.2 架构图](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-deepseek-v3-2.webp)

图 4. DeepSeek V3.2 将 MLA 与 DSA 搭配使用（原始出处：[*From DeepSeek V3 to V3.2: Architecture, Sparse Attention, and RL Updates*](https://magazine.sebastianraschka.com/p/technical-deepseek)）。

top-`k` 中的 `k`（不要与公式中表示键的 `k` 混淆）在[公开发布的模型代码](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp/blob/main/inference/model.py#L90)中设为 2048。借助索引器和 token 选择器，每个 token 只关注模型学到的少数最相关的过去 token，而不是全部 token 或固定局部窗口。

其目标并不是超越稠密基线模型的性能，而是在受益于效率提升的同时，尽量减小稀疏注意力机制带来的性能退化。GLM-5 随后采用了 DSA 与 MLA；GLM-5.2 进一步加入 [IndexShare](https://sebastianraschka.com/llm-architecture-gallery/indexshare/)，让相邻层可以复用被选中的位置。

来源

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[DeepSeek V3.2 技术文章](https://magazine.sebastianraschka.com/p/technical-deepseek)
[DeepSeek V3.2 论文](https://arxiv.org/pdf/2512.02556)
[GLM-5 论文](https://arxiv.org/pdf/2602.15763)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)

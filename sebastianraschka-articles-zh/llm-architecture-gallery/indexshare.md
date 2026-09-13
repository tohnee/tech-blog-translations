---
title: "IndexShare"
title_en: "IndexShare"
source: https://sebastianraschka.com/llm-architecture-gallery/indexshare/
crawled: 2026-09-06
translated: 2026-09-06
---

# IndexShare

> 原文：[IndexShare](https://sebastianraschka.com/llm-architecture-gallery/indexshare/)

IndexShare 让相邻的层复用由 [DeepSeek 稀疏注意力（DSA）](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)索引器选出的 token 位置。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[GLM-5.2 说明](https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html)
[Z.ai 发布文章](https://huggingface.co/blog/zai-org/glm-52-blog)
[IndexCache 论文](https://arxiv.org/abs/2603.12201)

![标准 DSA 在每一层都计算 top-k token 索引，而 IndexShare 只计算一次，并在随后三层中复用](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/indexshare-four-layer-reuse.webp)

图 1. 一次完整的索引器结果为四个 GLM-5.2 层供货。

共享内容

被选中的 token 位置

GLM-5.2 模式

`full`、`shared`、`shared`、`shared`

示例架构

[GLM-5.2](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-2) 和
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## 被复用的 DSA 选择

top-`k` 中的 `k`（不要与 DSA 公式中表示键的 `k` 混淆）是一个超参数，在 [DeepSeek 模型代码](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp/blob/main/inference/model.py#L90)中被设为 2048。通过索引器和 token 选择器，每个 token 只需关注过去少数几个模型已学会认为最相关的 token，而不是所有 token 或一个固定的局部窗口。

其目标并不是超越稠密基线模型的性能，而是在享受稀疏注意力机制带来的效率提升的同时，减少其造成的性能损失。

## 四层复用模式

```python
indexer_type = [full, shared, shared, shared]

if indexer_type == full:
    selected = top_k(indexer(hidden_state))
else:
    selected = previous_selected

output = attention(hidden_state, selected)  # New output in every layer
```

![带有 MLA、DeepSeek 稀疏注意力与 IndexShare 的 GLM-5.2 架构图](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/glm-5.2.webp)

图 2. GLM-5.2 在其 78 层堆叠中把每个 DSA 索引器标记为 `full` 或 `shared`（原始出处：
[*GLM-5.2 and IndexShare for Long-Context Sparse Attention*](https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html)。）

## 证据与代价

| 项目 | 报告的细节 | 这意味着什么 |
| --- | --- | --- |
| 相邻层重合度 | [IndexCache 研究](https://arxiv.org/abs/2603.12201)测得相邻 top-`k` 集合之间有 70% 到 100% 的重合。 | 新的索引器往往只是重新找回了上一层刚选出的位置。 |
| GLM-5.2 训练 | 四层模式是在中期持续训练阶段引入的，序列长度为 128K token。 | 保留的索引器可以适应为后续层服务。 |
| GLM-5.2 结果 | [Z.ai 报告](https://huggingface.co/blog/zai-org/glm-52-blog)在百万 token 上下文下，每 token FLOPs 减少 2.9 倍。 | 所报告的收益仅针对 GLM-5.2 和这一上下文长度。 |
| IndexCache 结果 | 在 30B 的 DSA 模型上移除 75% 的索引器计算，带来了最高 1.82 倍的预填充加速和 200K 下 1.48 倍的解码加速。 | 这些是独立的系统测量，不应与 GLM-5.2 的 FLOPs 结果直接比较。 |
| 代价 | 共享层无法从自己当前的隐状态中挑选新的位置。 | 它使用最近一个完整层选出的位置，同时仍计算自己的注意力输出。 |

参考资料

[GLM-5.2 发布文章](https://huggingface.co/blog/zai-org/glm-52-blog)
[GLM-5.2 配置](https://huggingface.co/zai-org/GLM-5.2/blob/main/config.json)
[IndexCache 论文](https://arxiv.org/abs/2603.12201)
[GLM-5.2 简要说明](https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html)
[DeepSeek 稀疏注意力解读](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)

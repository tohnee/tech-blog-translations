---
title: "QK-Norm"
title_en: "QK-Norm"
source: https://sebastianraschka.com/llm-architecture-gallery/qk-norm/
crawled: 2026-09-06
translated: 2026-09-06
---

# QK-Norm

> 原文：[QK-Norm](https://sebastianraschka.com/llm-architecture-gallery/qk-norm/)

QK-Norm 看起来是一个相当不起眼的架构改动：它本质上只是在注意力机制内部为 query 和 key 各增加一个额外的 RMSNorm。但它已经成为一种较为流行的、能在一定程度上稳定训练的技术。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[Qwen3 从零实现 Nb](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/11_qwen3/standalone-qwen3.ipynb)
[OLMo 3 从零实现 Nb](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/13_olmo3/standalone-olmo3.ipynb)

![与 OLMo 2 归一化改动相关的训练稳定性对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/qk-norm-training-stability.webp)

在 OLMo 2 的章节中，重点并不是 QK-Norm 单独起作用，而是它属于一组让训练表现更平稳的小型归一化选择。这是原始
[OLMo 2 论文](https://arxiv.org/abs/2501.00656)的一张标注图。（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

上图是我能找到的最好的消融研究。不过，很难说损失尖峰的减少有多少来自从 Pre-Norm 换成 Post-Norm，又有多少来自加入 QK-Norm。

## 它是稳定器，不是效率技巧

QK-Norm 很容易被低估，因为它听起来"不过是又一个 RMSNorm 层"。但它的位置才是有趣之处：它位于注意力内部，在 RoPE 之前、在点积计算之前，对 query 和 key 的投影做归一化。这意味着它直接塑造了决定注意力分数的那些向量。

在代码中，这个改动就是额外的归一化层加上 `forward` 里的两行：

```python
class GroupedQueryAttention(nn.Module):
    def __init__(self, ..., qk_norm=True):
        # ...
        if qk_norm:
            self.q_norm = RMSNorm(head_dim, eps=1e-6)
            self.k_norm = RMSNorm(head_dim, eps=1e-6)
        else:
            self.q_norm = self.k_norm = None
        # ...
            
    def forward(self, x, mask, cos, sin):
        # Apply projections
        queries = self.W_query(x)
        keys = self.W_key(x)
        values = self.W_value(x)

        # ...

        # Optional QK normalization
        if self.q_norm:
            queries = self.q_norm(queries)
        if self.k_norm:
            keys = self.k_norm(keys)

        # Apply RoPE
        queries = apply_rope(queries, cos, sin)
        keys = apply_rope(keys, cos, sin)
        
        # ...
```

（完整可运行的示例见 [Qwen3 从零实现](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/11_qwen3/standalone-qwen3.ipynb)。）

因此，[GQA](https://sebastianraschka.com/llm-architecture-gallery/gqa/)、[MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/) 和 [SWA](https://sebastianraschka.com/llm-architecture-gallery/swa/) 关注的是推理效率，而 QK-Norm 主要关注的是让优化过程足够平稳，使大模型能够可靠地训练。

## 成为常规做法之后的变化

当 QK-Norm 成为默认配置之后，各团队开始对它进行微调，而不是争论要不要用它。MiniMax M2 使用了逐头变体；Qwen3-Next 则在其[门控注意力](https://sebastianraschka.com/llm-architecture-gallery/gated-attention/)块中转向了一种零中心化的变体。

而 Tiny Aya 出于相反的原因值得注意：Cohere 团队明确移除了它，因为他们发现它与长上下文行为可能发生不良相互作用（一位开发者向我指出了这一点）。

参考资料

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[Qwen3 实现笔记](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/11_qwen3/standalone-qwen3.ipynb)
[OLMo 3 实现笔记](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/13_olmo3/standalone-olmo3.ipynb)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)

---
title: "从零实现 DeepSeek 稀疏注意力"
title_en: "DeepSeek Sparse Attention From Scratch"
source: https://sebastianraschka.com/blog/2026/deepseek-sparse-attention-from-scratch.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 从零实现 DeepSeek 稀疏注意力

> 原文：[DeepSeek Sparse Attention From Scratch](https://sebastianraschka.com/blog/2026/deepseek-sparse-attention-from-scratch.html)

感谢一位读者的出色贡献，我在 LLMs-from-scratch 仓库中添加了一个 [DeepSeek 稀疏注意力](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/09_dsa)的从零实现。

该目录包含一个 README、一个独立的 GPT 风格参考实现，以及测试：

1. [README.md](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/09_dsa/README.md)
2. [gpt\_with\_kv\_dsa.py](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/09_dsa/gpt_with_kv_dsa.py)
3. [test\_dsa.py](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/09_dsa/test_dsa.py)

[DeepSeek 稀疏注意力](https://sebastianraschka.com/glossary/#deepseek-sparse-attention "DeepSeek Sparse Attention")背后的核心思想，是用一个学习得到的稀疏模式取代固定的稀疏模式。该机制不再只使用局部窗口，而是使用一个轻量级的索引器（indexer）和选择器（selector）来决定哪些先前的 token 值得关注。

更多背景资料，我还有本地的 [DeepSeek 稀疏注意力概念页](https://sebastianraschka.com/llms-from-scratch/ch04/15_deepseek_sparse_attention/)和一个[图库讲解](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)，将它与常规的[因果注意力](https://sebastianraschka.com/glossary/#causal-attention "Causal Attention")以及滑动窗口注意力（SWA）进行对比。

[![DeepSeek 稀疏注意力实现概览](https://sebastianraschka.com/images/blog/2026/deepseek-sparse-attention/hero.webp)](https://substack.com/@rasbt/note/c-264003632)

来自原始 [Substack note](https://substack.com/@rasbt/note/c-264003632) 的截图，展示 DeepSeek 稀疏注意力实现目录和 README 概览。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-264003632) 的网页版，略有编辑。

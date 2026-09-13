---
title: "LLMs From Scratch 突破 100,000 GitHub Stars"
title_en: "LLMs From Scratch at 100,000 GitHub Stars"
source: https://sebastianraschka.com/blog/2026/llms-from-scratch-reaches-100000-github-stars.html
crawled: 2026-09-06
translated: 2026-09-06
---

# LLMs From Scratch 突破 100,000 GitHub Stars

> 原文：[LLMs From Scratch at 100,000 GitHub Stars](https://sebastianraschka.com/blog/2026/llms-from-scratch-reaches-100000-github-stars.html)

刚看到 [LLMs-from-scratch 仓库](https://github.com/rasbt/LLMs-from-scratch)在 GitHub 上突破了 100,000 stars！

这太酷了，也特别令人振奋。看到这个开源仓库帮助了这么多人，我真的很高兴。

也感谢所有分享想法、提交改进 PR 的朋友们！

当然，我计划继续添加新内容，包括新的注意力变体和架构（而 RL 和 Reasoning From Scratch 这类更大的项目则放在它们各自的仓库中）。

我目前还在做一个更大的应用型定制"小"LLM 项目。这个月它让我忙得不可开交，不过我很快会在一篇即将发布的 Substack 长文中分享更多细节！这将是我迄今为止最长的一篇！

如果你还不了解这个仓库，它的一些亮点包括：

1. 当然是从[分词](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/01_main-chapter-code/ch02.ipynb)、[注意力](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch03/01_main-chapter-code/ch03.ipynb)到[预训练](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/01_main-chapter-code/ch05.ipynb)、[分类](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch06/01_main-chapter-code/ch06.ipynb)和[指令微调](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/01_main-chapter-code/ch07.ipynb)等的完整代码路径。全部从零实现！（RL 在配套仓库中。）
2. [Llama](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/07_gpt_to_llama/standalone-llama32.ipynb)、[Qwen](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/11_qwen3)、[Gemma](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/12_gemma3) 和 [Olmo](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/13_olmo3) 的从零实现（可在本地运行的较小变体，可直接接入训练脚本）。
3. 注意力替代方案和其他架构组件的从零实现，例如 [GQA](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa)、[MLA](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla)、[滑动窗口注意力](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa)、[Gated DeltaNet](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)、[DeepSeek 稀疏注意力](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/09_dsa)、[跨层 KV 共享](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)和[专家混合](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)。
4. 关于 [KV 缓存](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/03_kv-cache)、[训练性能](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/10_llm-training-speed)、[内存高效权重加载](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/08_memory_efficient_weight_loading/memory-efficient-state-dict.ipynb)、[DPO](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch07/04_preference-tuning-with-dpo/dpo-from-scratch.ipynb)、[评测](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch07/03_model-evaluation)和 [LoRA](https://github.com/rasbt/LLMs-from-scratch/blob/main/appendix-E/01_main-chapter-code/appendix-E.ipynb) 的材料。

所以，如果你周末还没有安排，欢迎来动手玩玩！

[![拼贴图：LLMs-from-scratch GitHub 仓库达到 101,000 stars，以及注意力机制图和内存基准测试图](https://sebastianraschka.com/images/blog/2026/llms-from-scratch-100k-stars/hero.webp)](https://substack.com/@rasbt/note/c-310007138)

[来自 LLMs-from-scratch 仓库的图](https://github.com/rasbt/LLMs-from-scratch)。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-310007138) 的网页版。

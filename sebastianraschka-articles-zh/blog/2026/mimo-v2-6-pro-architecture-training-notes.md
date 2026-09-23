---
title: "MiMo-V2.6 Pro 训练笔记"
title_en: "MiMo-V2.6 Pro Training Notes"
source: https://sebastianraschka.com/blog/2026/mimo-v2-6-pro-architecture-training-notes.html
crawled: 2026-09-23
translated: 2026-09-23
---

# MiMo-V2.6 Pro 训练笔记

> 原文：[MiMo-V2.6 Pro Training Notes](https://sebastianraschka.com/blog/2026/mimo-v2-6-pro-architecture-training-notes.html) · Sebastian Raschka's Blog

小米的新模型 MiMo-V2.6 Pro「简单」地成为了（目前）最好的模型。尽管架构设计朴素，它目前位列开放权重基准（加权平均）的第一名。

说「朴素」，我是指它用的是经典的[分组查询注意力（GQA）](https://sebastianraschka.com/llm-architecture-gallery/gqa/)加[滑动窗口注意力（SWA）](https://sebastianraschka.com/llm-architecture-gallery/swa/)，窗口尺寸仅有 128 token。

这印证了我近几个月反复强调的一个观点：大部分进步仍来自数据与后训练配方的改进。花哨的[注意力变体](https://magazine.sebastianraschka.com/p/visual-attention-variants)大多只是效率层面的微调。

训练数据与配方上有哪些改进？MiMo 团队分享了一份相当详细的[技术报告](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL/blob/main/MiMo_V2_6_technical_report.pdf)，有很多值得仔细消化的内容。简而言之，以下几点令我印象深刻：

1. 智能体任务占比提升；并跨不同执行框架（harness）训练（在保留 harness 上的 DeepSWE pass@1 平均准确率从约 50% 提升到 66%）。
2. 更好的奖励信号：他们用一个同时检查执行轨迹的智能体式评分器（agentic grader）取代了简单的正确性验证器。
3. 大批量 [RL](https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training)（1,568 个 prompt × 16 个 rollout = 25,088 条轨迹），每次更新消耗 27–37 亿训练 token（不过前代模型用了多少并不清楚）。

![对比 MiMo-V2.6 Pro 与 DeepSeek V4-Pro 架构、Artificial Analysis 智能指数得分与输出速度的合成图](https://sebastianraschka.com/images/blog/2026/mimo-v2-6-pro-architecture-training-notes/mimo-v2-6-pro-comparison.webp)

MiMo-V2.6 Pro 与 DeepSeek V4-Pro 架构对比，附发布时 Artificial Analysis 智能指数与输出速度比较。

来源：我的 [Substack 笔记](https://substack.com/@rasbt/note/c-343108099)的网站版。

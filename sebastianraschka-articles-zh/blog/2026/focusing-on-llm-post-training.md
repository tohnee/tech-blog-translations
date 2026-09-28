---
title: "聚焦后训练"
title_en: "Focusing on Post-Training"
source: https://sebastianraschka.com/blog/2026/focusing-on-llm-post-training.html
crawled: 2026-09-28
translated: 2026-09-28
---

# 聚焦后训练

> 原文：[Focusing on Post-Training](https://sebastianraschka.com/blog/2026/focusing-on-llm-post-training.html) · Sebastian Raschka's Blog

[Ember-1](https://sebastianraschka.com/llm-architecture-gallery/#card-ember-1) 是一个绝佳范例，展示了在现有开放权重 LLM 之上能做出什么。Fireworks 从 [Kimi K3](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k3) 出发，通过后训练让它生成更短的推理轨迹。根据 [Fireworks 的发布公告](https://fireworks.ai/blog/ember-1)，Ember-1 在各项评估中保持相当质量的同时，token 用量减少了约 40%。

最近我在一期播客中被即兴问到：假如有一笔想象中的数百万美元预算，我会如何在有限预算下开发一个前沿 LLM。我的建议是：从现有模型出发，把预算花在后训练上。（[这里是链接](https://www.youtube.com/watch?v=fpYG6OBKEZw)，不过抱歉，它是德语的；我唯一的一期德语播客。）

关键在于：即便是数百万美元，对于训练一个有竞争力的前沿 LLM（5000 亿参数及以上）来说也不算多。而既然市面上已有如此强大、优秀的开放权重模型可供选择，目前根本没有理由把钱全部花在重复造预训练的轮子上。

Ember-1 正是我想的那种改进的具体例证。当然，他们这里只聚焦于效率并保持既有能力，但 40% 的 token 用量削减已经非常可观。（另一个角度可以是保持现有模型的效率水平，同时在更新的执行框架（harness）上推高其能力。）

![Ember-1、Kimi K3 与其他 LLM 在 Bedside Benchmark 上的得分与单任务成本对比](https://sebastianraschka.com/images/blog/2026/focusing-on-llm-post-training/ember-1-bedside-benchmark.webp)

Specialized Intelligence Index Bedside Benchmark 上的得分（avg@3）与单任务成本。（原始来源：[Fireworks on X](https://x.com/FireworksAI_HQ/status/2102875211783970842)）

他们是如何实现 40% 的 token 用量削减的？他们训练模型生成更短的推理轨迹。这与我在《[控制 LLM 的推理努力](https://magazine.sebastianraschka.com/p/controlling-reasoning-effort-in-llms)》一文中介绍过的 token 高效与预算化强化学习方法一脉相承。

其一般思路是把 token 用量纳入训练目标。例如，我们可以设计一个同时考量答案正确性与响应长度的奖励，或者鼓励模型在指定的 token 预算内给出正确解答。难点在于削减不必要的推理，同时保留攻克困难问题的能力。

这正是我想在下图中阐明的关联。（但请注意，Fireworks 并未公开 Ember-1 足够多的训练配方来判定其确切算法，因此与这些方法的关联是概念层面的。）

![Ember-1 与 Kimi K3 及 token 高效推理方法的概念对比](https://sebastianraschka.com/images/blog/2026/focusing-on-llm-post-training/ember-1-post-training.webp)

Ember-1、Kimi K3 架构，以及控制推理努力的相关方法。训练方法层面的关联是概念性的。

PS：我与 Fireworks 没有任何关联；我只是觉得这是一个有趣的案例研究。

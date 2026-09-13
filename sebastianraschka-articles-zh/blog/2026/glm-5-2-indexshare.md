---
title: "GLM-5.2 IndexShare 架构笔记"
title_en: "GLM-5.2 IndexShare Architecture Note"
source: https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html
crawled: 2026-09-06
translated: 2026-09-06
---

# GLM-5.2 IndexShare 架构笔记

> 原文：[GLM-5.2 IndexShare Architecture Note](https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html)

[GLM-5.2](https://huggingface.co/zai-org/GLM-5.2) 是 Z.ai 的 GLM-5 模型家族的一次长上下文更新。它保留了 GLM-5 和 GLM-5.1 的大部分架构，并增加了一项聚焦稀疏注意力的改动，称为 [IndexShare](https://sebastianraschka.com/glossary/#indexshare "IndexShare")。

继承下来的骨干是一个大型稀疏专家混合（MoE）模型。根据 [GLM-5 技术报告](https://arxiv.org/abs/2602.15763)，该模型家族总参数量为 7440 亿，每个 token 激活约 400 亿。[GLM-5.2 配置](https://huggingface.co/zai-org/GLM-5.2/blob/main/config.json)列出了 78 层 transformer，隐藏维度为 6,144。前三个前馈模块是稠密的。其余模块使用 256 个路由专家，每个 token 选择其中 8 个，并增加 1 个共享专家。

注意力栈将[多头潜在注意力](https://sebastianraschka.com/llm-architecture-gallery/mla/)与 [DeepSeek 稀疏注意力](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)（DSA）结合在一起。我在[DeepSeek V3 到 V3.2 的文章](https://magazine.sebastianraschka.com/p/technical-deepseek)中更详细地介绍过这一组合。GLM-5.2 将配置的[上下文长度](https://sebastianraschka.com/glossary/#context-length "Context Length")从此前模型的 200K token 扩展到 1,048,576 token。

## DSA 索引器在哪里变得昂贵

DSA 把稀疏注意力拆分为选择和计算。一个轻量级索引器为每个查询位置对更早的 token 打分，并选出前 2,048 个。然后主注意力操作在这个被选中的子集上进行。

如果序列长度为 (L)、选中 token 数为 (k)，核心稀疏注意力的复杂度按 (O(Lk)) 增长。索引器仍要将每个查询与所有先前位置比较，因此其复杂度在 (L) 上仍是平方级的。它单次操作比主注意力模块便宜得多，但在非常长的上下文长度下，跨多个层的重复索引器工作会变得可观。

[IndexCache 研究](https://arxiv.org/abs/2603.12201)测得相邻 DSA 层的 token 选择有 70% 到 100% 的重叠。这意味着相邻的索引器常常会重新发现许多相同的位置。

## IndexShare 复用了什么

IndexShare 在某一层运行索引器，并在附近的三层中复用它选出的 token 位置。在发布配置中开头的少数几个例外之后，重复模式是 `full, shared, shared, shared`。这里的 `full` 意味着该层运行自己的 DSA 索引器，并不意味着对完整上下文做稠密注意力。

共享层仍然计算自己的查询、注意力权重、值组合、输出投影和前馈更新。它们只复用被选中位置的列表。这个区别很重要，因为隐藏状态和注意力输出会逐层持续变化。

Z.ai 在使用 128K token 序列继续进行中期训练（mid-training）时引入了这一模式。带着复用模式训练，让每个保留的索引器有机会去适应依赖它的相邻层。这不同于在推理时给已经训练好的模型加一个缓存。

发布报告称，在 100 万 token 上下文下每 token FLOPs 缩减至原来的约 1/2.9。这是该架构在该上下文长度下的计算量估计，不应被解读为端到端 2.9 倍加速。Z.ai 还指出，IndexShare 并不会按同样比例减少 KV 缓存内存。在 100 万 token 下，缓存容量、长上下文算子、CPU 调度和缓存传输仍然是可观的服务成本。

相关的 IndexCache 论文有助于把这个结果放到背景中看。在一个独立的 30B DSA 模型、200K token 的设置下，保留四分之一的索引器带来了最高 1.82 倍的预填充（prefill）加速和 1.48 倍的解码加速。那些测量使用的是不同的模型和上下文长度，所以它们是复用思路的证据，而不是直接的 GLM-5.2 延迟数字。

## MTP 层中的复用

同一次发布还修改了用于投机解码（speculative decoding）的多 token 预测层。它的第一个草稿步骤计算索引，后续草稿步骤同时复用这些索引和先前的 [KV 缓存](https://sebastianraschka.com/glossary/#kv-cache "KV Cache")。Z.ai 将其与拒绝采样和端到端全变差损失（total-variation loss）相结合。

在报告的消融实验中，整套 MTP 改动把平均接受草稿长度从 4.56 提升到 5.47 token，提高了 20%。表格中的改动是逐项累加的，因此无法单独区分最终收益中有多少来自 IndexShare。

本地的 [IndexShare 讲解](https://sebastianraschka.com/llm-architecture-gallery/indexshare/)包含这个四层模式的一个紧凑伪代码版本。[GLM-5.2 架构卡片](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-2)跟踪模型配置、许可证、注意力机制和当前的[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")参考。

[![GLM-5.2 架构与基准测试总览](https://sebastianraschka.com/images/blog/2026/glm-5-2/hero.webp)](https://substack.com/@rasbt/note/c-278515750)

图 1：上图画出了 GLM-5.2 继承的 [MLA](https://sebastianraschka.com/glossary/#mla "Multi-Head Latent Attention (MLA)")、DSA 和稀疏 MoE 结构。IndexShare 改变的是 DSA 选择 token 位置的频率。下图保留了发布时的 Artificial Analysis 基准测试快照。

## 如何看待基准测试快照

发布时，下面这张 [Artificial Analysis Coding Index](https://artificialanalysis.ai/) 快照给 GLM-5.2 打出 68.8 分，Claude Opus 4.8 (max) 为 56.7。Z.ai 自己的结果也显示相对 GLM-5.1 有大幅提升，包括 Terminal-Bench 2.1 上 81.0 对 63.5，以及 SWE-bench Pro 上 62.1 对 58.4。

我会把这些当作带时间戳的评估快照来看。排行榜、模型提供商和执行框架（harness）都会变化，而且 Z.ai 的基准测试表使用的是任务专属的上下文限制、提示词和智能体框架。架构层面的主张更窄、也更容易评估：GLM-5.2 在其常规的四层分组中去掉了四分之三的重复 DSA 索引器调用，同时每一层都保留稀疏注意力。

![Artificial Analysis Coding Index 图表，对比 GLM-5.2 与 Claude Opus 4.8](https://sebastianraschka.com/images/blog/2026/glm-5-2/artificial-analysis-coding-index.webp)

图 2：GLM-5.2 发布前后截取的 Artificial Analysis Coding Index 快照。这些数值记录的是那个时间点，不应被解读为永久性的模型排名。

来源：我 [Substack 笔记](https://substack.com/@rasbt/note/c-278515750)的扩展网站版，基于 [GLM-5.2 发布文](https://huggingface.co/blog/zai-org/glm-52-blog)、[模型配置](https://huggingface.co/zai-org/GLM-5.2/blob/main/config.json)、[GLM-5 技术报告](https://arxiv.org/abs/2602.15763)和 [IndexCache 论文](https://arxiv.org/abs/2603.12201)。

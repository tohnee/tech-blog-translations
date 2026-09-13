---
title: "并行到底：用投机解码超越单 token 生成"
title_en: "Parallel All the Way Down: Beyond Single-Token Generation with Speculative Decoding"
source: https://vllm.ai/blog/2026-07-28-speculators-parallel-drafting
crawled: 2026-09-12
translated: 2026-09-13
---

# 并行到底：用投机解码超越单 token 生成

> 原文：[Parallel All the Way Down: Beyond Single-Token Generation with Speculative Decoding](https://vllm.ai/blog/2026-07-28-speculators-parallel-drafting) · vLLM 博客

作者：Alexandre Marques、Megan Flynn、Helen Zhao、Krishna Teja Chitty Venkata、Chibueze Ukachi（Red Hat AI）

[#Speculators](https://vllm.ai/blog/tags/speculators)[#投机解码](https://vllm.ai/blog/tags/speculative_decoding)[#peagle](https://vllm.ai/blog/tags/peagle)[#dflash](https://vllm.ai/blog/tags/dflash)[#dspark](https://vllm.ai/blog/tags/dspark)

# 1. 引言

投机解码已成为缓解大语言模型（LLM）服务中内存带宽瓶颈的核心优化技术。通过在验证模型的一次前向传播中验证多个候选 token，它使生产系统能够获得可观的推理加速。

然而，随着服务基础设施的演进，传统投机框架面临一个结构性天花板，其根源在于草稿 token 的生成方式。今天，我们很高兴展示 [Speculators](https://github.com/vllm-project/speculators) 与 [vLLM](https://github.com/vllm-project/vllm) 如何突破这些限制：为三种最先进的并行起草算法提供完整的开源支持——[P-EAGLE](https://arxiv.org/abs/2602.01469)、[DFlash](https://arxiv.org/abs/2602.06036) 与 [DSpark](https://arxiv.org/abs/2607.05147)。

![图 1. 并行起草算法（如 P-EAGLE、DFlash 与 DSpark）相比 EAGLE-3 等自回归起草算法带来显著的性能提升。上述草稿模型可在 RedHatAI HuggingFace Hub 的 Speculators 合集中找到。](https://vllm.ai/blog-assets/figures/2026-07-28-speculators-parallel-drafting/compare_interactivity_qwen38b_math.png)

图 1. 并行起草算法（如 P-EAGLE、DFlash 与 DSpark）相比 EAGLE-3 等自回归起草算法带来显著的性能提升。上述草稿模型可在 RedHatAI HuggingFace Hub 的 Speculators 合集中找到。

![图 1. 并行起草算法（如 P-EAGLE、DFlash 与 DSpark）相比 EAGLE-3 等自回归起草算法带来显著的性能提升。上述草稿模型可在 RedHatAI HuggingFace Hub 的 Speculators 合集中找到。](https://vllm.ai/blog-assets/figures/2026-07-28-speculators-parallel-drafting/compare_interactivity_qwen330b_humaneval.png)

图 1. 并行起草算法（如 P-EAGLE、DFlash 与 DSpark）相比 EAGLE-3 等自回归起草算法带来显著的性能提升。上述草稿模型可在 RedHatAI HuggingFace Hub 的 Speculators 合集中找到。

![图 1. 并行起草算法（如 P-EAGLE、DFlash 与 DSpark）相比 EAGLE-3 等自回归起草算法带来显著的性能提升。上述草稿模型可在 RedHatAI HuggingFace Hub 的 Speculators 合集中找到。](https://vllm.ai/blog-assets/figures/2026-07-28-speculators-parallel-drafting/compare_interactivity_gemma431b_humaneval.png)

图 1. 并行起草算法（如 P-EAGLE、DFlash 与 DSpark）相比 EAGLE-3 等自回归起草算法带来显著的性能提升。上述草稿模型可在 RedHatAI HuggingFace Hub 的 Speculators 合集中找到。

# 2. 递归起草的局限

[EAGLE](https://arxiv.org/abs/2401.15077) 与 [MTP](https://arxiv.org/abs/2404.19737) 等框架的引入，标志着投机解码的一次重大范式转变。EAGLE 证明了草稿模型架构可以直接利用验证模型丰富的内部隐藏状态，从而大幅提高 token 接受率，而不必强迫草稿模型仅凭表层文本盲目猜测。

尽管有这一突破，[EAGLE-3](https://arxiv.org/abs/2503.01840) 等进阶版本仍在一条根本性约束下运行：**自回归起草**。要提出一串候选 token，草稿架构必须逐个顺序生成，为每一个 token 执行一次独立的前向传播。

这种自回归设计在生产中带来两大权衡：

- **模型规模受限：** 由于起草成本随投机长度线性增长，草稿模型被迫保持极小、极轻量，以免吃掉验证模型在验证环节省下的执行时间。
- **复杂的运维调参：** 线性扩展在实践中严重限制了草稿 token 的数量。选择最优投机长度（K）成为一个敏感变量，工程团队必须根据具体用例和实时服务器负载不断调整。

![图 2. 并行起草在一步中生成多个草稿 token，而自回归起草每步只生成一个草稿 token。](https://vllm.ai/blog-assets/figures/2026-07-28-speculators-parallel-drafting/ar_vs_parallel.jpg)

图 2. 并行起草在一步中生成多个草稿 token，而自回归起草每步只生成一个草稿 token。

# 3. 转向并行起草

并行起草从根本上重构了这一权衡：它把顺序执行从起草阶段彻底剔除。并行起草算法不再循环执行单 token 生成步骤，而是并发地预测整块候选 token。

通过把起草阶段压平为单次前向传播，生成提案的延迟与投机 token 的数量解耦。这一架构转变从两个方面简化了生产服务：

- **更具表达力：** 由于草稿模型每个块只需运行一次，开发者可以采用更大、更稳健、更具表达力的草稿架构。这些更深的草稿模型能捕捉更复杂的上下文，带来更高的接受率，而不会引入顺序执行的延迟惩罚。
- **简化参数调优：** 起草成本与块长度解耦，免除了根据波动的服务器负载反复精调投机参数的运维负担。

并行起草这一概念此前已被探索过——[Medusa](https://arxiv.org/abs/2401.10774) 和 [PARD](https://arxiv.org/abs/2504.18583) 是较早的著名例子。P-EAGLE、DFlash 与 DSpark 在此基础上，把并行执行与深层的验证器状态条件化相结合——正是后者的洞察成就了 EAGLE 的成功。

# 4. 内部机制：推理与训练架构

**P-EAGLE**、**DFlash** 与 **DSpark** 都基于验证模型的隐藏状态来并行生成草稿 token，但三者路径各异。图 3 并排展示了它们的架构。

![图 3. P-EAGLE、DFlash 与 DSpark 的对比。P-EAGLE 把验证器的隐藏状态作为草稿模型输入的一部分。DFlash 将隐藏状态投影进 KV 缓存。DSpark 在 DFlash 主干之上增加了顺序校正与置信度估计器。](https://vllm.ai/blog-assets/figures/2026-07-28-speculators-parallel-drafting/diagram.jpg)

图 3. P-EAGLE、DFlash 与 DSpark 的对比。P-EAGLE 把验证器的隐藏状态作为草稿模型输入的一部分。DFlash 将隐藏状态投影进 KV 缓存。DSpark 在 DFlash 主干之上增加了顺序校正与置信度估计器。

三者共同面临的挑战是训练。任何并行草稿模型都必须在训练序列的每个 token 位置上执行 next-K 预测。对于长度为 N 的序列和前瞻窗口 K，朴素地对整个矩阵计算损失会让内存与计算成本高得无法承受。每个算法都以不同方式应对这一问题。

## **P-EAGLE**

P-EAGLE 直接建立在 EAGLE 把验证模型隐藏状态用作输入特征的基础之上。它不把这些特征用于顺序预测 token，而是同时把它们映射到多个未来位置，在单个并行步骤中输出整段候选 token 序列。

为了让训练可控，P-EAGLE 实现了草稿块稀疏化：按衰减率沿前瞻维度（K）丢弃 token，把优化集中在最关键的近期 token 上，同时把遥远的未来位置从损失计算中剪除。

## **DFlash**

DFlash 对验证器特征的路由方式不同。它不把隐藏状态作为标准输入喂入，而是将其投影后直接注入草稿模型的 KV 缓存。这让草稿模型的注意力机制与验证器的精确状态紧密耦合，而无需扩展输入序列长度，使其能够通过块扩散生成高度准确的候选 token 块。

在训练上，DFlash 实现了序列长度稀疏化。它不在长度为 N 的序列的每个 token 位置计算块损失，而是沿时间轴随机选取锚点，只在这些交点处计算块预测——既保住 GPU 内存，又保持有代表性的覆盖。

## **DSpark**

DSpark 采用 DFlash 的并行主干，并在其上叠加了两项额外创新。第一，它为架构增加了一个轻量的自回归校正头，使未来 token 能更强地以前文 token 为条件。这将并行生成的吞吐优势与自回归精化的顺序连贯性结合在一起。

第二，DSpark 解决了一个下游瓶颈：验证成本。并行起草可以低成本生成大量草稿 token，但验证器仍须处理所有这些 token。DSpark 引入一个置信度头，在草稿 token 抵达验证器之前为其打分，只选择性地转发那些可能被接受的 token。这减少了浪费在验证上的算力，并提升端到端吞吐。

# 5. 推理性能

图 1 展示了并行起草算法相对 EAGLE-3 带来的性能提升。图中展示了三个不同的模型与并行起草算法：

| 模型 | 算法 | 用例 | 硬件 |
| --- | --- | --- | --- |
| Qwen3-8B | [P-EAGLE](https://huggingface.co/RedHatAI/Qwen3-8B-speculator.peagle) | 数学推理（GSM8k） | 1xA100 |
| Qwen3-30B-A3B | [DFlash](https://huggingface.co/RedHatAI/Qwen3-30B-A3B-speculator.dflash) | 编程（HumanEval） | 2xA100 |
| gemma-4-31B-it | [DSpark](https://huggingface.co/RedHatAI/gemma-4-31B-it-speculator.dspark) | 编程（HumanEval） | 2xA100 |

在所有情形下，并行起草都显著优于 EAGLE-3。性能会因模型、任务和硬件配置而异——我们鼓励社区在自己的工作负载上进行基准测试。

# 6. 用 vLLM 与 Speculators 进行生产服务

把最先进的并行起草算法集成进生产，需要一个稳定且经过优化的基础设施栈。Speculators 仓库提供了一个统一生态来训练和评估这些下一代模型，并与 **vLLM** 完全集成。

启动一个基于并行起草的投机引擎非常简单，只需在初始化时传入相应的配置标志：

```
vllm serve Qwen/Qwen3-30B-A3B \
  --tensor-parallel-size 2 \
  --reasoning-parser qwen3 \
  --speculative-config '{
    "model": "RedHatAI/Qwen3-30B-A3B-speculator.dflash",
    "num_speculative_tokens": 7,
    "method": "dflash"
  }'
```

从单 token 生成转向块级并行起草后，你的推理流水线就做到了并行到底——最大化硬件利用率，并带来持续、无损的加速。（投机解码通过拒绝采样精确保留验证模型的输出分布，因此质量在数学上与标准解码完全一致。）

# 7. 立即上手

并行起草如今已获得完整支持、开源且生产可用。我们邀请社区探索该仓库，利用文档化的训练路径构建你自己的并行草稿模型，并在 vLLM 中进行原生基准测试。

- 仓库：[Speculators](http://github.com/vllm-project/speculators)
- 预训练草稿模型：[HuggingFace 上的 Speculators 合集](https://huggingface.co/collections/RedHatAI/speculator-models)
- 训练指南：[Speculator 教程](https://github.com/vllm-project/speculators/blob/main/docs/user_guide/tutorials/index.md)

# 勘误

图 1 中的图表已于 2026 年 7 月 29 日更新。由于环境配置有误，原图中的数字与所述基准测试条件不符。不过，模型间的相对表现是一致的，博客中的结论不变。

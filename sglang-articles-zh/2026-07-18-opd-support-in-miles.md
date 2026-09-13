---
title: "Miles 新增 OPD（在线策略蒸馏）支持"
title_en: "OPD Support in Miles"
author: "Kaixi Hou & Miles Team"
date: "July 18, 2026"
previewImg: /images/blog/opd-support-in-miles/figure-1.png
source: https://lmsys.org/blog/2026-07-18-opd-support-in-miles/
translated: 2026-09-12
---

# Miles 新增 OPD（在线策略蒸馏）支持

> 原文：[OPD Support in Miles](https://lmsys.org/blog/2026-07-18-opd-support-in-miles/) · LMSYS Blog · Kaixi Hou & Miles Team

我们最近在 Miles 中实现了**一项重要特性：在线策略蒸馏（On-Policy Distillation，OPD）**。OPD 现已集成到 Miles 的 rollout 与训练流程中，用户既可以仅凭教师模型的引导来训练学生模型，也可以将教师引导与 GRPO/PPO 风格的强化学习目标相结合。

在本文中，我们将介绍 Miles 中的 OPD 实现、我们为避免不必要的稠密 logprob 负载而新增的稀疏教师打分工作流，以及在一个 **8×NVIDIA B200** 单节点上验证的 Qwen3.5-35B-A3B 自蒸馏初步实验。该实验表明，在没有任何任务特定奖励的情况下，OPD 也能把教师模型的更短推理行为迁移到基座学生模型上，同时保持学生模型的性能。

<img src="/images/blog/opd-support-in-miles/figure-1.png" alt="Miles 与 OPD 工作流" style="display:block; margin-left:auto; margin-right:auto; width:70%;"></img>

## OPD 作为 Miles 的训练原语

Miles 现已支持将 OPD 作为一种可叠加的反向 KL（reverse-KL）训练信号。这使得 OPD 能够支持两种重要模式。

- **纯蒸馏（pure distillation）**仅用教师信号训练学生。在这种设置下，任务奖励可以设为零，更新完全由逐 token 的师生反向 KL 信号驱动。
- **RL 增强的蒸馏（RL-augmented distillation）**将 OPD 信号与任务奖励以及 GRPO/PPO 风格的优势估计器相结合。这样，学生模型可以同时从环境反馈和教师引导中学习。

在 rollout 一侧，Miles 通过由 SGLang 托管的教师模型，同时支持采样 token OPD（sampled-token OPD）与 top-k OPD。在采样 token OPD 中，教师对学生在每个响应位置上实际采样得到的 token 进行打分。由于采样可能是随机的，该 token 未必是学生概率最高的 token。

top-k OPD 在此工作流基础上进行了扩展：在每个位置保留多个候选 token 及其学生 logprob。教师对同样的候选 token 打分，Miles 再将对应齐的学生 logprob 与教师 logprob 组合成训练中使用的逐 token 反向 KL 信号。

这一设计让 OPD 成为 Miles 中可复用的训练原语，而非一条独立的一次性蒸馏路径。

## Top-k OPD

Miles 支持 top-k OPD，以构建比单一采样 token 估计器更丰富的师生比较。

在学生 rollout 过程中，Miles 会在每个响应位置记录一组可配置的候选 token ID 及其学生 logprob。要对位置 t 的候选 token 打分，教师模型会以原始提示词（prompt）以及学生在位置 t 之前生成的 token 为条件，然后返回该位置所请求候选 token 的教师 logprob。

OPD 实现还支持可配置的 top-k 蒸馏策略。用户可以自定义候选集合的构建方式，以及在计算反向 KL 信号时候选 token 的加权方式。这样，不同的蒸馏配方（recipe）都能复用同一套 rollout、教师打分与训练基础设施。

## 稀疏的学生到教师打分

一项关键的系统改进是稀疏的学生到教师打分（student-to-teacher scoring）工作流。

在 OPD 中，学生 rollout 会产出一个按位置组织的 top-k 表。对于每个已生成的响应位置，Miles 都确切知道 KL 计算需要哪些候选 token ID 及学生 logprob。教师模型只需在相应的因果前缀（causal prefix）下对这些候选 token ID 打分即可。

在最初的 OPD 实现中，打分工作流必须先构建一个包含所有按位置 top-k token ID 的全局并集，再让教师在每个响应位置对整个并集打分。这样做保证了正确性，但会产生稠密的 **R × |U|** 中间负载，其中 **R** 为响应长度，**U** 为全局 token ID 并集。由于 **|U|** 可以增长到接近 **R × K**，旧路径可能要物化并解析一个 **O(R²K)** 规模的 JSON 响应，而最终的 OPD 计算其实只需要 **O(RK)** 个值。

新工作流用**按位置的稀疏候选 token 打分**取代了稠密的全局并集路径。Miles 向教师发送一张按位置组织的 token ID 表，教师只返回每个位置自身候选集所请求的 logprob。这使教师响应负载与实际的 OPD 计算保持一致：Miles 只承载 OPD 所需的稀疏 **R × K** 个值。

对于长响应推理负载而言，这一点很重要：教师打分不应被不必要的负载构建、传输或解析所主导。稀疏打分让 OPD 流水线更加直接，也更适合高吞吐量的 rollout 与训练。

## 验证：在 NVIDIA B200 上进行 Qwen3.5 自蒸馏

为了验证该实现，我们用 **Qwen3.5-35B-A3B** 进行了一项受控的自蒸馏实验。

教师模型先用可验证奖励强化学习（RLVR）进行训练，使其能用短得多的响应解出 DAPO 数学题。学生模型则是对应的 RL 训练前基座检查点（checkpoint）。我们选择这一设置，是因为直接蒸馏 DAPO 能力几乎看不到变化：基座 Qwen 学生模型在原任务上本已很强。于是我们反其道而行之，刻意在教师模型中制造出一个可度量的行为变化——推理更短但依然有效——然后检验 OPD 能否把这一行为迁移给尚未表现出该行为的学生模型。

为了隔离 OPD 的作用，我们运行了纯蒸馏。

- **任务奖励：** 零
- **训练信号：** top-1 师生反向 KL
- **教师：** 经 RLVR 训练的更短推理检查点
- **学生：** RL 训练前的基座检查点
- **硬件：** 单个 8×NVIDIA B200 节点
- **执行模式：** 学生 rollout、教师打分与学生训练共置（colocated），并在同一 GPU 资源池上分时共享

参考基准如下：

| 模型 / 阶段 | 留出集 DAPO | 平均响应长度 |
| --- | --- | --- |
| RLVR 教师 | 0.8870 | 6,248 |
| 初始基座学生 | 0.8457 | 18,675 |

教师用短得多的响应解出同样的 DAPO 题目，而基座学生生成的解法则明显长得多。通过这一实验，我们想回答以下问题：

**纯 OPD 能否在保持留出集 DAPO 性能的同时，把教师的高效推理行为迁移给学生？**

## 结果：推理更短，性能不下降

我们的结果提供了明确证据，表明 OPD 能够迁移高效推理行为。

留出集 DAPO 性能从 **0.8457** 提升到 **0.8945**。与此同时，采样 rollout 长度在第一次更新后骤降，从约 **18.6k token** 降到后续 rollout 中大多处于 **5.5k–6.7k token** 区间，期间仅出现一次短暂的随机尖峰。逐 token OPD 反向 KL 也从约 **0.045** 降至 **0.010**，说明在学生自己的 rollout 上，学生分布变得更接近教师分布。

三条学习曲线从不同角度讲述了同一个故事。

**留出集 DAPO 性能上升**，表明学生经过 OPD 后任务性能没有退化。

<img src="/images/blog/opd-support-in-miles/figure-2.png" alt="留出集 DAPO 性能随评估步骤的变化" style="display:block; margin-left:auto; margin-right:auto; width:60%;"></img>

**采样 rollout 长度迅速下降**，表明学生采纳了教师更短响应的行为。

<img src="/images/blog/opd-support-in-miles/figure-3.png" alt="采样 rollout 长度随 rollout 步骤的变化" style="display:block; margin-left:auto; margin-right:auto; width:60%;"></img>

**逐 token OPD 反向 KL 下降**，证实学生分布正在向教师分布靠近。

<img src="/images/blog/opd-support-in-miles/figure-4.png" alt="逐 token OPD 反向 KL 随 rollout 步骤的变化" style="display:block; margin-left:auto; margin-right:auto; width:60%;"></img>

由于本实验中原始任务奖励为零，这一行为变化完全由 OPD 教师信号驱动。核心结论是：**纯 OPD 将教师的高效推理行为迁移给了基座学生，而留出集 DAPO 性能不降反升**。

## 这对 Miles 意味着什么

OPD 的实现让 Miles 能够应用于仅靠可验证任务奖励还不够的后训练工作流。

许多实际工作流不仅要优化任务成功率，还要优化模型行为：推理长度、响应风格、领域特有习惯、与参考模型的分布对齐等。OPD 使 Miles 能够把这类目标表达为教师引导的训练信号，同时保持原有的 rollout 与 RL 训练流水线不变。

OPD 也为多教师整合开辟了一条路径。不同的专家教师可以为不同领域或能力提供引导，让单个学生模型吸收互补的行为，成为更全能的模型。由于 Miles 将 OPD 视为可复用的原语，同一套学生训练流水线即可支持不同的教师与蒸馏配方，无需为每个领域单独搭建训练系统。多教师 OPD 的验证仍是未来工作。

该实现还保持了 OPD 的可组合性。用户既可以运行纯蒸馏，也可以把 OPD 作为辅助信号与 GRPO/PPO 风格的目标结合使用。这对于教师引导与任务奖励需要协同工作的后训练工作流非常重要。

同样重要的是，该系统针对长响应负载做了优化。按位置的稀疏打分与 top-k OPD 有助于避免不必要的稠密教师打分负载，使流水线与蒸馏所需的实际计算更加匹配。

## 下一步计划

当前实现将 OPD 确立为 Miles 的一等能力，并在受控的 Qwen3.5 自蒸馏设置中验证了纯 OPD。接下来，我们计划在几个方向上扩展验证。

**验证 OPD 增强的 RL。**

我们已经验证了纯 OPD。下一步是验证 OPD 与 GRPO/PPO 任务奖励相结合的情况，即学生同时从奖励信号和教师分布引导中学习。

**更大规模的性能研究。**

目前学生 rollout 是主要开销，教师打分会带来额外负担。我们计划在更长、更高吞吐量的负载上对整条流水线进行基准测试，以更好地理解其扩展行为与瓶颈。

**多教师 OPD。**

一个很有前景的下一步，是评估领域专精教师能否共同指导同一个学生模型。这将检验 OPD 能否成为把互补的专家行为整合进单个更通用模型的机制。

**更多训练配方。**

Qwen3.5 实验聚焦于迁移更短的推理。未来的配方可以探索其他教师引导的行为，包括领域专精化、响应风格、工具使用模式以及智能体（agentic）数据。

## 总结

Miles 现已将 OPD 作为一等训练与 rollout 特性加以支持。实现内容包括可叠加的反向 KL 训练、SGLang 教师打分、top-k OPD、可配置的候选与加权策略，以及按位置的稀疏教师打分。

在单个 8×NVIDIA B200 节点上的 Qwen3.5-35B-A3B 自蒸馏初步实验中，纯 OPD 把更短推理行为从 RLVR 教师迁移到了基座学生。留出集 DAPO 性能从 **0.8457** 提升到 **0.8945**，采样 rollout 长度从约 **18.6k token** 降至大多处于 **5.5k–6.7k token** 区间，逐 token OPD 反向 KL 从约 **0.045** 降至 **0.010**。

这些初步结果表明，纯 OPD 能够迁移有用的行为特性——在本例中是显著更短的推理——同时保持强劲的留出集任务性能。要让这一结论在更多模型、任务和师生配置上成立，仍需更广泛的实验验证。

## 致谢

我们特别感谢 NVIDIA 的 Hunter Carlisle 和 Priya Sethuraman，感谢他们为促成这项工作提供的慷慨帮助与支持。

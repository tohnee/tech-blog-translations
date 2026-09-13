---
title: "VibeThinker-3B 后训练笔记"
title_en: "VibeThinker-3B Post-Training Notes"
source: https://sebastianraschka.com/blog/2026/vibethinker-3b-post-training.html
crawled: 2026-09-06
translated: 2026-09-06
---

# VibeThinker-3B 后训练笔记

> 原文：[VibeThinker-3B Post-Training Notes](https://sebastianraschka.com/blog/2026/vibethinker-3b-post-training.html)

根据报告的基准测试，[VibeThinker-3B](https://huggingface.co/WeiboAI/VibeThinker-3B) 在竞赛数学和编程任务上与体量大得多的模型惊人地接近。它在 AIME 2026 上达到 94.3，LiveCodeBench v6 上 80.2，IMO-AnswerBench 上 76.4。对一个稠密的 3B 参数模型来说，这些数字令人印象深刻。

架构是最不出人预料的部分。VibeThinker-3B 从 [Qwen2.5-Coder-3B](https://huggingface.co/Qwen/Qwen2.5-Coder-3B) 出发，其[配置](https://huggingface.co/WeiboAI/VibeThinker-3B/blob/main/config.json)保留了标准的 Qwen2 式解码器。它有 36 个 transformer 块、2,048 维嵌入空间和 11,008 维前馈隐藏层。注意力层使用 16 个查询头和 2 个键值头，即 8:1 的分组查询注意力比例。配置的[上下文长度](https://sebastianraschka.com/glossary/#context-length "Context Length")为 131,072 token。

有意思的是[技术报告](https://arxiv.org/abs/2606.16140)中描述的后训练配方。它把数据合成、两个[监督微调](https://sebastianraschka.com/glossary/#instruction-finetuning "Instruction Finetuning (SFT)")阶段、若干强化学习阶段、离线自蒸馏，以及最后一轮指令微调组合在一起。

## 两个监督微调阶段

监督数据涵盖数学、代码、STEM、通用对话和指令遵循。对数学和代码，作者从有可检验答案或可执行测试的问题出发。他们扩展这些种子问题，从教师模型采样多个解法，并用多数投票构造伪标签。同一问题的多条有效推理路径都被保留。

合成之后有一个可观的过滤步骤。流水线会去除重复的生成内容和与评估集重叠的部分，拒绝格式糟糕的问题，检查最终答案，并在沙箱中执行代码。这一部分很重要，因为由[验证器](https://sebastianraschka.com/glossary/#verifier "Verifier")驱动的 RL 的效果，取决于喂给它的提示词和奖励检查的质量。

第一个 SFT 阶段在完整的过滤混合数据上训练，以获得广泛覆盖。第二个阶段使用窄得多的子集。作者丢弃短于 5,000 token 的推理轨迹。他们还对每个问题运行 VibeThinker-1.5B 八次，剔除错误率低于 75% 的相对简单的问题。换句话说，第二个阶段聚焦于那些既长、又对参考模型困难的样本。

检查点的选择也不寻常。作者没有按验证损失挑选一个检查点，而是在领域专属的探针集（probe sets）上测量 Pass@K。他们挑选那些能为每个领域产出更宽的有效解集合的检查点，并在参数层面合并这些专项检查点。

## 能力边界附近的强化学习

VibeThinker-3B 使用 MaxEnt 引导的策略优化（MaxEnt-Guided Policy Optimization，MGPO）。它是从更早的 VibeThinker-1.5B 工作延续下来的一种 [GRPO](https://sebastianraschka.com/glossary/#grpo "GRPO (Group Relative Policy Optimization)") 风格方法。

核心思想很直观。假设模型为一个提示词采样多个答案。几乎全错的提示词可能太难，无法提供有用的学习信号；几乎全对的提示词则没什么可教的了。MGPO 给组准确率接近 50% 的提示词更大权重，在那里成功与失败的尝试并存。

RL 数据覆盖数学、代码和 STEM。每个领域使用合适的验证器：数学用最终答案检查，代码用沙箱测试，STEM 用答案或选项匹配。各阶段按数学、代码、STEM 的顺序依次运行。三者都使用 on-policy 采样。

另一个实用细节是上下文窗口。更早的 1.5B 工作在多个阶段中逐步扩展上下文长度。对这个模型，作者发现早期截断会损害长推理轨迹，而且模型在后期也无法完全恢复。因此他们直接用单一的 64K token 上下文窗口运行 RL。

数学阶段以一个 Long2Short 阶段收尾。正确回答之间的奖励被略微调整，向更短的解法倾斜，而错误解法的奖励保持不变。这鼓励模型在准确性导向的阶段已经学会解题之后，进行更简洁的推理。

## 蒸馏 RL 检查点

按领域顺序训练带来了另一个问题：较晚的检查点可能丢失较早阶段的有用行为。作者用离线自[蒸馏](https://sebastianraschka.com/glossary/#distillation "Distillation")来解决这个问题。他们从数学、代码和 STEM 检查点收集经过验证的轨迹，然后在过滤后的混合数据上微调一个学生模型。

他们的过滤评分偏向这样的正确轨迹：学生模型目前仍给它相对较低的似然。这是花费蒸馏容量的合理方式。一个学生模型已经能轻松预测出的正确解，包含的新信息少于它尚未吸收的解。

最后一步是指令 RL。基于规则的验证器为带显式格式、顺序、条目数量和关键词约束的提示词打分。基于评分标准（rubric）的奖励模型处理更开放的提示词。报告的 IFEval 93.4 分表明，漫长的推理流水线没有抹掉指令遵循能力。

## 如何理解[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")结果

这些数字由模型提供方报告，阅读时应牢记其评估协议。作者使用 1.0 的[温度](https://sebastianraschka.com/glossary/#temperature "Temperature")并对重复采样取平均：大多数数学基准测试用 64 次生成，编程用 8 次，知识类任务用 16 次。对比模型的分数来自已发布的报告、公开排行榜或官方评估记录，而不是同一个共享的评估框架。

标为 CLR 的更高分数使用了额外的[测试时计算](https://sebastianraschka.com/glossary/#reasoning-model "Reasoning Model")。对每个问题，声明级可靠性评估（Claim-Level Reliability Assessment）生成 32 条候选轨迹，从每条中提取五个与决策相关的声明，并让模型验证这些声明，然后使用由此得到的可靠性分数聚合答案。例如，报告的 AIME 2026 分数在启用 CLR 后从 94.3 升至 97.1。我会把这个结果与普通的 Pass@1 分数分开看待。

"前沿水平"这种宽泛描述也有其局限。VibeThinker-3B 在 GPQA-Diamond 上得 70.2，而报告中若干更大的模型得分超过 80。[模型卡](https://huggingface.co/WeiboAI/VibeThinker-3B)推荐将模型用于可验证的数学、编程和 STEM 任务，并明确说明该模型没有针对[工具调用](https://sebastianraschka.com/glossary/#tool-use "Tool Use")或智能体编程训练。

最后，报告没有披露总 GPU 时数或完整的成本拆解，也没有为流水线的每个阶段提供受控消融。我们能看到最终结果并理解配方，但无法把收益中精确的份额归因于 MGPO、Long2Short RL、自蒸馏或合成数据。不过，熟悉的 Qwen2.5-Coder 骨干仍让这个案例成为一个有用的研究样本：在具有可靠验证的任务上，精心的后训练能把一个小模型推到多远。

[![VibeThinker-3B 基准测试、架构与后训练总览](https://sebastianraschka.com/images/blog/2026/vibethinker-3b/hero.webp)](https://substack.com/@rasbt/note/c-277879621)

图 1：左图是选定的提供方报告数学分数，包括额外的 CLR 测试时扩展结果。右上图概括了熟悉的 Qwen2.5-Coder 式架构。下图追踪了从课程式 SFT、推理 RL、离线自蒸馏到指令 RL 的后训练阶段。

来源：我 [Substack 笔记](https://substack.com/@rasbt/note/c-277879621)的扩展网站版，基于 [VibeThinker-3B 技术报告](https://arxiv.org/abs/2606.16140)、[模型卡](https://huggingface.co/WeiboAI/VibeThinker-3B)和[模型配置](https://huggingface.co/WeiboAI/VibeThinker-3B/blob/main/config.json)。

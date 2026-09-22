---
title: "在策略蒸馏"
title_en: "On-Policy Distillation"
date: 2026-08-31
source: https://thinkingmachines.ai/blog/on-policy-distillation/
crawled: 2026-09-22
translated: 2026-09-22
---

# 在策略蒸馏

> 原文：[On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/) · Thinking Machines Lab

LLM 能够在专注领域中达到专家级表现，这是多项能力叠加的结果：输入感知、知识检索、方案选择以及可靠执行。这需要一整套训练方法，我们可以大致分为三个阶段：

- **预训练（Pre-training）**传授语言使用、广泛推理和世界知识等通用能力。
- **中期训练（Mid-training）**注入领域知识，如代码、医学数据库或公司内部文档。
- **后训练（Post-training）**激发定向行为，如指令遵循、推演数学问题或聊天。

经过更强训练的小模型往往在其受训的专业领域中胜过更大的通用模型。使用小模型有诸多好处：出于隐私或安全考虑可以本地部署，可以更轻松地持续训练和更新，并节省推理成本。要利用这些好处，需要为训练的后期阶段选择正确的方法。

对「学生」模型做后训练的方法可以分为两类：

- **在策略训练（on-policy training）**从学生模型自身采样 rollout，并赋予它们某种奖励。
- **离策略训练（off-policy training）**依赖学生学习模仿的外部来源目标输出。

例如，我们可能想训练一个紧凑模型来解决如下数学问题：

![](svgs/prompt.svg)

我们可以通过强化学习做在策略训练，依据每条学生 rollout 是否解出题目来打分。这个打分可以由人完成，也可以由一个能可靠得出正确答案的「教师」模型完成。

![](svgs/reinforcement-learning.svg)

在策略训练的优势在于：通过在自身采样的样本上训练，学生能以更直接的方式学会避免错误。但 RL 有一个重大缺点：它提供的反馈非常稀疏——无论使用的 token 数量多少，每个训练 episode 只教会[固定数量的比特](https://thinkingmachines.ai/blog/lora/#how-much-capacity-is-needed-by-supervised-and-reinforcement-learning)。在上面的例子中，学生知道「21」是错误答案，并更新以远离它刚才尝试的 rollout。但它不知道错误具体出在哪里——是运算顺序搞错了，还是算术本身算错了。反馈的稀疏性使 RL 在许多应用中效率低下。

离策略训练通常用监督微调（SFT）完成：在一组精选的、带标注的任务专项样本上训练。这些标注样本的来源可以是一个在该任务上已被证明表现良好的教师模型。

我们可以使用一种叫**蒸馏（distillation）**的机制：训练学生去匹配教师模型的输出分布。我们在教师**轨迹（trajectory）**上训练：即包括中间思考步骤在内的完整生成 token 序列。我们可以在每一步使用教师的完整下一 token 分布（常称「logit 蒸馏」），或者只是采样给定的序列。实践中，对序列采样提供了对教师分布的无偏估计，并达到同一目标。学生按自己生成该 token 的可能性成比例地向序列中的每个 token 更新（可能性越低，更新越大），如下例中颜色更深的 token 所示：

![](svgs/off-policy-distillation.svg)

从大模型教师蒸馏已被证明能有效训练小模型去[遵循指令](https://crfm.stanford.edu/2023/03/13/alpaca.html)（[Alpaca: A Strong, Replicable Instruction-Following Model](https://crfm.stanford.edu/2023/03/13/alpaca.html)（Taori et al, 2021））、[推理数学与科学](https://arxiv.org/abs/2506.04178)（[OpenThoughts: Data Recipes for Reasoning Models](https://arxiv.org/abs/2506.04178)（Guha et al, 2025））、从医学笔记[提取临床信息](https://arxiv.org/html/2501.00031v1)（[Distilling Large Language Models for Efficient Clinical Information Extraction](https://arxiv.org/abs/2501.00031)（Vedula et al, 2025）），以及[参与多轮聊天对话](https://arxiv.org/abs/2305.14233)（[Enhancing Chat Language Models by Scaling High-quality Instructional Conversations](https://arxiv.org/abs/2305.14233)（Ding et al, 2023））。用于这些及其他应用的蒸馏数据集往往已开源并公开发布。

离策略训练的缺点是：学生在教师常出没的上下文中学习，而不是学生自己会经常遇到的上下文。这可能导致复合误差：如果学生犯了一个教师从不犯的早期错误，它会发现自己离训练中观察到的状态越来越远。当我们关心学生在长序列上的表现时，这个问题变得尤为尖锐。为避免这种发散，学生必须学会从自己的错误中恢复。

离策略蒸馏中被观察到的另一个问题是：学生可能学会模仿教师的风格和自信，但[未必模仿到其事实准确性](https://arxiv.org/abs/2305.15717)。（[The False Promise of Imitating Proprietary LLMs](https://arxiv.org/abs/2305.15717)（Gudibande et al, 2023））

如果你在学下棋，在策略 RL 就像没有教练指导地对弈。输赢的反馈与你自己下的棋直接相关，但每局只收到一次，而且不告诉你哪些着法对结果贡献最大。离策略蒸馏则像观看特级大师下棋——你观察到极强的着法，但它们出现在新手棋手很少会遇到的局面中。

我们想把 RL 的在策略相关性与蒸馏的密集奖励信号结合起来。对学棋而言，这就像一位教师对你*自己*下的每一步棋按「严重失误」到「妙手」打分。对 LLM 后训练而言，这就是在策略蒸馏。

![](images/chess.png)

截图来自 [chess.com](https://www.chess.com/)。每步棋由分析引擎按颜色分级，标签分为失误（红）、错误（橙）、不精确（黄）或妙手（蓝）。

## 在策略蒸馏——两全其美

在策略蒸馏的核心思想是：从*学生*模型采样轨迹，并用一个高性能教师对每条轨迹的*每个 token* 打分。回到上面的数学例子，在策略蒸馏会给解答的每一步打分，惩罚导致学生得出错误答案的失误，同时强化执行正确的部分。

![](svgs/on-policy-distillation.svg)

在这篇文章中，我们探索在策略蒸馏在如下任务上的应用：训练一个数学推理模型，以及训练一个把领域知识与指令遵循结合起来的助手模型。我们把在策略蒸馏应用于已具备预训练和中期训练能力基础的模型。我们发现它是一种廉价而强大的后训练方法，把在策略训练的优势与密集奖励信号结合了起来。

| 方法 | 采样 | 奖励信号 |
| --- | --- | --- |
| 监督微调 | off-policy | 密集 |
| 强化学习 | on-policy | 稀疏 |
| 在策略蒸馏 | on-policy | 密集 |

我们在策略蒸馏方面的工作受 [DAGGER](https://arxiv.org/abs/1011.0686)（[A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://arxiv.org/abs/1011.0686)（Ross et al, 2010））启发，那是一个包含教师对学生访问状态进行评估的迭代 SFT 算法。它也类似于[过程奖励建模](https://arxiv.org/abs/2305.20050)（[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)（Lightman et al, 2023）），一种给学生模型思维链每一步打分的 RL 方法。我们扩展了 [Agarwal et al.](https://arxiv.org/abs/2306.13649)（[On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes](https://arxiv.org/abs/2306.13649)（Agarwal et al, 2023））、[Gu et al.](https://arxiv.org/abs/2306.08543)（[MiniLLM: Knowledge Distillation of Large Language Models](https://arxiv.org/abs/2306.08543)（Gu et al, 2023））以及 [Qwen3 团队](https://arxiv.org/abs/2505.09388)（[Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)（Qwen Team, 2025））的在策略蒸馏工作。使用 [Tinker 训练 API](https://thinkingmachines.ai/tinker/)，我们复现了 Qwen3 的结果：以远低于 RL 的成本，用在策略蒸馏在推理基准上取得同等表现。

## 实现

你可以在 [Tinker cookbook](https://github.com/thinking-machines-lab/tinker-cookbook/tree/main/tinker_cookbook/recipes/distillation) 中跟随实现的每一步。

### 损失函数：反向 KL

在策略蒸馏可以使用多种损失函数来给学生轨迹打分。（参见 Agarwal et al. 对各种损失函数选择的分析。）为简单起见，我们选择逐 token 反向 KL——在相同先前轨迹条件下，学生（π_θ）与教师（π_teacher）分布对每个 token 的散度：

KL(π_θ ∥ π_teacher) = E_{x~π_θ}[log π_θ(x_{t+1} | x_{1..t}) − log π_teacher(x_{t+1} | x_{1..t})]

我们的奖励函数最小化反向 KL，推动学生在它所处的每个状态中逼近教师的行为。当学生与教师行为一致时，反向 KL 为零。为简单起见，我们使用零折扣因子：在每个时间步（尽管数学上更正确，我们发现 > 0 的折扣因子在实践中并不能提升表现，因此为简单起见选择零。），学生只优化紧邻的下一个 token，不考虑未来 token。

反向 KL 与 RL 有天然协同，后者通常优化由奖励模型诱导的某种序列级反向 KL。然而，与实践中大多数奖励模型不同，反向 KL 是「不可被博弈（unhackable）」的：低 KL 总是对应从教师模型视角看高概率的期望行为。反向 KL 的另外两个有用性质是：它是「模式寻求（mode seeking）」的（参见 [Eric Jang 的文章](https://blog.evjang.com/2016/08/variational-bayes.html)了解更多关于模式寻求行为的讨论。）——它学习一种具体行为（教师的行为），而不是把分布摊薄到多个次优选项上；以及它能减少[暴露偏差（exposure bias）](https://arxiv.org/abs/1506.03099)（[Scheduled Sampling for Sequence Prediction with Recurrent Neural Networks](https://arxiv.org/abs/1506.03099)（Bengio et al, 2015）。参见 Gu et al. 的更多讨论。）

这一方法能显著节省算力。由于不需要等 rollout 完成采样就能计算奖励，我们可以用更短或不完整的 rollout 来训练。查询教师的对数概率也只需大模型做一次前向传播，而轨迹由更小、更便宜的学生生成。

我们也不需要单独的奖励模型或标注模型。把基于蒸馏的逐 token 奖励与序列级环境奖励结合可能有其优势；这是一个有趣的未来研究方向。

### 示例

下面是一个教师给错误学生轨迹打分的真实例子。例子来自 [SimpleBench](https://simple-bench.com/)，依赖模型做出一个关键观察——题目的前提很重要：正确答案是「B. 0」，因为冰块在煎锅里会融化。学生 [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) 错误地把它当作纯数学问题，完全没有考虑物理情境。

![](svgs/example-kl-illustration.svg)

教师模型打分的轨迹示例。颜色更红的 token 对应更高的反向 KL。

颜色更深代表受到教师模型（[Qwen3-235B-A22B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507)，它正确解决了这道题）更高惩罚的 token。我们看到，它惩罚那些开启导致学生误入歧途短语的 token，直观上对应引导推理的重要[「分叉 token」](https://arxiv.org/abs/2506.01939)（[Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning](https://arxiv.org/abs/2506.01939)（Wang et al, 2025））。最终答案虽然是错的，却没有被惩罚——在整个前序序列的条件下，它是完全可预测的。

### 伪代码

我们在 [Tinker 的 RL 脚本](https://github.com/thinking-machines-lab/tinker-cookbook/blob/main/tinker_cookbook/rl/train.py)之上实现在策略蒸馏，后者已经实现了采样、奖励计算和策略梯度式训练。（我们的实现实际上可以是对使用 KL 正则化的 RL 实现的一行改动：我们只是换掉正则化模型。）

1. *初始化教师客户端。*Tinker API 可以轻松为不同模型创建不同的客户端，而无需担心模型引擎的利用率。我们使用采样客户端，因为不需要通过教师模型反向传播 logprobs。
2. *采样轨迹。*我们像在 RL 中一样从学生采样 rollout。采样期间，RL 已经计算了学生的 logprobs log π_θ(x)，作为[重要性采样](https://tinker-docs.thinkingmachines.ai/losses#policy-gradient-importance_sampling)损失的一部分。
3. *计算奖励。*我们对采样轨迹调用 `compute_logprobs` 查询教师客户端，返回教师对学生采样的 token x 上的 logprobs log π_teacher(x)。（本文中，我们在所有实验里都不考虑 logit（top-k）蒸馏，后者可用于进一步提升计算效率。）然后我们用它计算反向 KL。
4. *用 RL 训练。*我们把逐 token 优势设为负的反向 KL，并调用 RL 重要性采样损失函数对学生模型执行训练更新。

```
# Initialize teacher client (main):
teacher_client = service_client.create_sampling_client(
    base_model=teacher_config.base_model,
    model_path=teacher_config.load_checkpoint_path,
)

# Sample trajectories (main):
trajectories = do_group_rollout(student_client, env_group_builder)
sampled_logprobs = trajectories.loss_fn_inputs["logprobs"]

# Compute reward (compute_teacher_reverse_kl):
teacher_logprobs = teacher_client.compute_logprobs(trajectories)
reverse_kl = sampled_logprobs - teacher_logprobs
trajectories["advantages"] = -reverse_kl

# Train with RL (train_step):
training_client.forward_backward(trajectories, loss_fn="importance_sampling")
```

在下面的实验中，我们通常把在策略蒸馏应用于已在特定领域知识上做过中期训练的模型。这种训练提高了学生在教师分布内生成 token 的概率，尽管它通常远不足以复制教师的表现。（使用前向 KL 的 SFT 会为新 token 添加[支撑集（support）](https://en.wikipedia.org/wiki/Support_(mathematics))。反向 KL 方法随后可以在初始化的支撑集内做模式寻求。）通常——正如我们在个性化示例中将看到的——由于学生缺乏任何相关领域知识，生成相关 token 的概率从零开始。

我们用在策略蒸馏做后训练，并将其与训练专家模型这一最后关键阶段的其他方法进行比较。

## 面向推理的蒸馏

我们用蒸馏在 [Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) 模型上训练数学推理，使用 [Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) 作为教师模型。教师（Qwen3-32B）和学生（Qwen3-8B-Base）今天都是 Tinker 的[支持模型](https://tinker-docs.thinkingmachines.ai/model-lineup)，因此你可以用 Tinker cookbook 复现我们的实验。（**更新（2026 年 6 月）：**此处使用的教师（Qwen3-32B）和学生（Qwen3-8B-Base）此后已[从 Tinker 模型阵容中退役](https://tinker-docs.thinkingmachines.ai/tinker/model-deprecations/)。[Tinker cookbook 中的蒸馏配方](https://github.com/thinking-machines-lab/tinker-cookbook/tree/main/tinker_cookbook/recipes/distillation)已更新为使用 [Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) 作为学生、[Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) 作为教师，因此实验仍然可复现。）

### 离策略蒸馏

如上所述，我们所有实验都以离策略蒸馏形式的中期训练开始——在教师生成的样本数据集上做监督微调。用于数学推理的数据集是 [OpenThoughts-3](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M)，一个由 [QwQ-32B](https://huggingface.co/Qwen/QwQ-32B)（与 Qwen3-32B 类似的推理模型）生成的推理提示与回答合集。

在 40 万条提示上对学生（Qwen3-8B-Base）做全量微调，在数学问题基准 AIME'24 上取得 60 分。我们也可以用 LoRA 训练（[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)（Hu et al, 2021）），但在大数据量上训练时落后于全量微调。在所有情形中，我们都观察到表现按对数-线性增长——前期的增益便宜，后期的增益昂贵。

![](svgs/experiment-off-policy-distillation.svg)

离策略蒸馏（SFT）过程中的 AIME'24 分数。在最初 5-10 万条提示之后，表现遵循可预测的对数-线性缩放曲线。正如 [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/) 所预测的，我们在以大批大小运行大规模 SFT 时观察到 LoRA 表现更差。

我们可以把在 40 万条提示上微调的模型当作一个检查点，然后再尝试各种后训练方法来提升其表现。我们可以比较把 AIME'24 基准的分数从 60 提升到 70 各需要多少投入。

默认做法是在更多提示上微调，继续离策略蒸馏的过程。按对数-线性趋势外推，我们估计模型在约 200 万条提示时会在 AIME'24 上达到 70。这一外推要求缩放定律持续成立而不停滞，这并非易事。不过，确实存在大规模离策略蒸馏把 8B 模型表现提升到 70 以上的例子，如 [OpenThoughts-3](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M) 和 [DeepSeek-R1-0528-Qwen3-8B](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B)。（DeepSeek-R1-0528-Qwen3-8B 在该基准上达到 86，训练提示数未披露。较旧的模型（Qwen2.5-7B、Qwen2.5-14B）在用 DeepSeek-R1 的 80 万条蒸馏提示训练后[分别达到 55.5 和 69.7](https://arxiv.org/abs/2501.12948)。）我们可以把这一外推作为离策略蒸馏成本-表现比的乐观估计。

### 强化学习

[Qwen3 技术报告](https://arxiv.org/pdf/2505.09388)在类似的 SFT 初始化之上，使用 17,920 GPU 小时的 RL 达到 67.6 的基准表现。这很难与蒸馏成本直接比较，但对 SFT 训练栈做一些合理假设后，它大致相当于在 200 万条离策略蒸馏提示上训练的成本。

| 方法 | AIME'24 | GPQA-Diamond | GPU 小时 |
| --- | --- | --- | --- |
| 离策略蒸馏 | 55.0% | 55.6% | 未报告 |
| + 强化学习 | 67.6% | 61.3% | 17,920 |
| + 在策略蒸馏 | 74.4% | 63.3% | 1,800 |

来自 [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)，表 21。

Qwen 团队还报告了用在策略蒸馏以十分之一于 RL 的成本在 AIME'24 上达到 74.4 的更高分数，这正是我们工作的灵感来源。下面我们在自己的基础设置中尝试复现它。

### 在策略蒸馏

作为离策略蒸馏或 RL 的替代，我们如上所述运行在策略蒸馏。（我们实际上使用 Qwen3-8B 作为教师，因为它的表现稍好。不过，为了比较计算量，我们仍可以按 32B 模型度量 FLOPs。）从 40 万 SFT 检查点出发，在策略蒸馏在大约 150 步内达到 70 的 AIME'24。（150 步对应约 7.7 万条提示；我们每条提示训练 4 个样本。）

![](svgs/experiment-on-policy-distillation-loras.svg)

在策略蒸馏过程中的 AIME'24。我们以训练 FLOPs 度量额外计算（见下文）。在策略蒸馏的计算效率显著高于 SFT，对 LoRA 模型尤其如此。在秩 = 32 时，LoRA 在 SFT 后落后全量微调 13%，但在策略蒸馏后仅落后 6%。

跨方法比较计算成本并不简单，因为训练、采样与对数概率计算的成本之比因实现而异。下面我们以 FLOPs 计算成本，这会惩罚那些能在 GPU 上高效并行的方法。特别是，它高估了计算 log-probs 的实际成本。

| 方法 | AIME'24 | 教师 FLOPs | 学生 FLOPs | 相对 SFT-2M 的成本效率 |
| --- | --- | --- | --- | --- |
| *初始化：SFT-400K* | 60% | 8.5 × 10²⁰ | 3.8 × 10²⁰ | – |
| SFT-2M（外推） | ~70%（外推） | 3.4 × 10²¹ | 1.5 × 10²¹ | 1× |
| 强化学习 | 68% | - | - | ≈1× |
| 在策略蒸馏 | 70% | 8.4 × 10¹⁹ | 8.2 × 10¹⁹ | 9-30× |

我们发现，当 SFT 数据集已给定（如我们 OpenThoughts-3 的例子）或其成本可摊销到多次训练运行时，基础成本降低为 9 倍。（CE =（学生 + 教师）/（学生）。此处我们不为离策略训练计入教师 FLOPs，但为在策略训练计入，因为我们必须运行教师模型来为学生轨迹计算 log-probs。由于这一计算可以在 GPU 间廉价并行，以 GPU 小时计的成本降低接近 18 倍。）

然而，我们常常想在一个没有现成离策略蒸馏数据集的新任务上训练小模型。如果把教师模型的全部成本都计入离策略蒸馏——即包括从教师模型采样的额外成本——总成本降低约为 30 倍。（CE =（学生 + 教师）/（学生 + 教师））

## 面向个性化的蒸馏

除了在常见任务上把小模型训练到高性能，蒸馏的另一个用例是个性化。例子包括在对话中遵循特定语气和输出格式，或工具使用、成本预算等能力。我们常常想把这类行为与新的领域知识结合起来训练。

同时训练二者通常很困难，轻量微调往往不足以达成这一目标（[Unfamiliar Finetuning Examples Control How Language Models Hallucinate](https://arxiv.org/abs/2403.05612)（Kang et al, 2024）），因而需要更大的中期训练。在 新知识之上学习后训练行为需要复杂的后训练栈，通常包含专有数据和奖励模型。虽然前沿实验室能做到这一点，但对其他从业者而言却可能难以复制或成本高得离谱。

在本节中，我们展示在策略蒸馏可以有效用于后训练专门化行为。该方法也适用于持续学习或「测试时训练」：在模型部署后更新它而不回退基础表现。我们以一个在我们内部公司文档上做中期训练的模型作为示例应用。

### 训练一个内部助手

定制模型的常见目标是充当助手：在某个领域具备专家知识，同时具备可靠的助手式行为。我们可能需要对二者分别训练，尤其是当专业领域无法仅从预训练数据学到、或学习它会干扰行为时。

我们的例子是一个内部公司助手，对它我们有两个期望：

1. 模型对领域（公司文档）**知识渊博**。预训练模型从未见过任何该公司的内部文档，因此无论模型规模如何都只能靠猜。我们将用内部知识回忆评测（「内部 QA」）来度量。
2. 模型展现出强大的**后训练**行为，即指令遵循。我们将用常用的 [IF-eval](https://arxiv.org/abs/2311.07911)（[Instruction-Following Evaluation for Large Language Models](https://arxiv.org/abs/2311.07911)（Zhou et al, 2023））来度量。

### 在新知识上训练会退化已学的行为

我们将从 Qwen3-8B 而非基座模型开始。Qwen3-8B 经过了助手所需技能的后训练，如指令遵循和 RL 推理。先前研究表明，这类强化学习只训练原模型的小型子网络（[Reinforcement Learning Finetunes Small Subnetworks in Large Language Models](https://arxiv.org/abs/2505.11711)（Mukherjee et al, 2025）），因此在网络上继续用大量数据训练时可能脆弱。我们研究这种情况发生的程度，以及期望的行为如何恢复。

为减少这种灾难性遗忘，中期训练中的一种常见做法是混入来自原模型预训练分布的「背景数据」。（[Midtraining Bridges Pretraining and Posttraining Distributions](https://arxiv.org/abs/2510.14865)（Liu et al, 2025））本例中，我们无法获取 Qwen3 的预训练分布。因此，我们考虑一个更强也更昂贵的基线：取 [Tulu3](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture)（[Tulu 3: Pushing Frontiers in Open Language Model Post-Training](https://arxiv.org/abs/2411.15124)（Ivison et al, 2024））提示——一个宽泛的聊天与指令遵循数据集——并用 Qwen3-8B 重新采样它们，充当聊天背景数据。

这一由 Qwen3-8B 采样的「在策略」背景数据充当前向 KL 正则化器，在整个中期训练中强化模型的原始行为。我们发现在整个中期训练中保持聊天能力方面，从 Qwen3-8B 采样优于从 Qwen3-32B 采样，这凸显了对数据源的敏感性；Chen et al. 也发现了类似的在策略 SFT 结果。（[Retaining by Doing: The Role of On-Policy Data in Mitigating Forgetting](https://arxiv.org/abs/2510.18874)（Chen et al, 2025））我们假设这一方法甚至可能比拥有原始预训练数据分布更有效，代价是必须采样一个大规模数据集。

然后我们在内部文档与聊天数据的不同混合比例上微调 Qwen3-8B。提高文档数据的比例会直接改善模型的知识。然而，尽管混入至少 30% 的聊天数据有助于保留大部分指令遵循能力，却没有任何权重能保持原始的 IF-eval 表现。（即使 SFT 数据集包含 100% 聊天数据也是如此。我们会在持续学习的讨论中进一步处理。）

![](svgs/experiment-personalization-midtrain.svg)

中期训练期间扫描内部文档与背景聊天数据的比例。虽然混入少量聊天数据有助于防止灾难性回退，但没有任何权重能保持原始 IF-eval 表现。

对任何给定的混合比例，我们都观察到 IF-eval 表现在微调期间下降。这损害了我们用更长训练进一步专门化模型的能力。（从方向上讲，我们可以预期一个在某些数据集上训练的过参数化模型只在该数据集的上下文中更新行为，而不影响它在其他上下文中的表现。但实践中我们没有观察到这一点：在原始文档数据上训练甚至使 QA 上下文中的表现也回退了。）

![](svgs/experiment-midtrain-if-eval.svg)

所有数据混合比例下，IF-eval 在中期训练期间都下降。当我们使用线性学习率（如图）时，退化最终趋平，并随学习率衰减缓慢开始恢复。然而，表现从未完全恢复。

另一种常用的方法是使用 LoRA 来约束参数更新，从而降低灾难性遗忘的可能性。然而，该方法仍不足以保持 IF-eval，而且 LoRA 学得更少。（[LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673)（Biderman et al, 2024））

![](svgs/experiment-midtrain-lora.svg)

当用于在后训练过的 Qwen3-8B 之上做我们的个性化中期训练时，LoRA 学得更少（知识），而且仍然遗忘其原始的后训练行为。

### 在策略蒸馏恢复后训练行为

接下来，我们寻求在内部文档微调之后恢复指令遵循行为。这一行为最初由 RL 训练，既昂贵、又如我们所见般脆弱。我们改为在 [Tulu3](https://huggingface.co/datasets/allenai/tulu-3-sft-mixture) 提示上运行在策略蒸馏，用该模型的早期版本 Qwen3-8B 作为教师。注意，这一训练阶段与内部文档数据毫无关系，专门用于恢复指令遵循。

用模型的早期版本作为教师来「重新唤起」微调中丢失的能力，使在策略蒸馏对持续学习非常有前景。我们可以在「新数据微调」与「恢复行为的蒸馏」两个阶段之间交替，让模型随时间学习并保持知识更新。这种阶段交替方法此前由 Cobbe et al. 探索过。（[Phasic Policy Gradient](https://arxiv.org/abs/2009.04416)（Cobbe et al, 2020））

在 70-30 的内部文档数据与聊天数据混合上微调后，在策略蒸馏恢复了几乎全部 IF-eval 表现而没有损失任何知识；我们还观察到聊天能力与模型在内部 QA 评测上的「知识」表现之间存在一些正迁移。

| 模型 | 内部 QA 评测（知识） | IF-eval（聊天） |
| --- | --- | --- |
| *Qwen3-8B* | 18% | 85% |
| *+ 中期训练 (100%)* | 43% | 45% |
| + 中期训练 (70%) | 36% | 79% |
| + 中期训练 (70%) + 蒸馏 | 41% | 83% |

中期训练后的领域特定（内部 QA 评测）与聊天（IF-eval）表现。虽然中期训练遗忘了 Qwen3-8B 的后训练行为，但它们可以通过在策略蒸馏廉价地恢复，同时保留中期训练学到的额外知识。

本质上，我们把语言模型自身当作了奖励模型，奖励高概率行为（[Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)（Rafailov et al, 2023））。这与逆 RL 有联系：在一个假定的底层偏好模型中，高概率行为对应有优势的奖励。（[Algorithms for Inverse Reinforcement Learning](https://ai.stanford.edu/~ang/papers/icml00-irl.pdf)（Ng and Russell, 2000））任何经过指令微调的开放权重模型都可以在这种意义上被用作奖励模型；我们只需要访问 `compute_logprobs` 函数。

蒸馏作为整合行为与知识的工具，也已在混合推理模型（[Qwen3](https://arxiv.org/abs/2505.09388)）和专家蒸馏（[DeepSeek-V3.2-Exp: Boosting Long-Context Efficiency with DeepSeek Sparse Attention](https://github.com/deepseek-ai/DeepSeek-V3.2-Exp/blob/main/DeepSeek_V3_2.pdf)（DeepSeek-AI Team, 2025））中被探索过。正如我们和 [Chen et al.](https://arxiv.org/abs/2510.18874) 的结果所暗示的，在策略学习可以成为增强类似基于蒸馏的「模型合并」设置的关键工具。

## 讨论

### 密集监督大幅提升计算效率

强化学习和在策略蒸馏都通过反向 KL 学习，剪除基策略中存在的动作空间。差别在于奖励的密度。在 [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/) 中，我们提出了信息论视角：强化学习每条 episode 只教 O(1) 比特。相比之下，蒸馏每条 episode 教 O(N) 比特，其中 N 是 token 数。我们能否量化更密集的奖励带来的训练效率提升？

我们做了一个直接比较二者的实验：

1. 从 Qwen3-8B-Base 开始（无额外 SFT）。
2. 在 DeepMath 上运行 RL，沿用我们在 [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/) 中的流程。我们使用 LoRA 秩 128。所得模型作为蒸馏的教师。
3. 把 RL 训练的模型 (2) 在策略蒸馏回基座模型 (1)。

![](svgs/experiment-self-distillation.svg)

从同一初始化出发，在策略蒸馏能以约少 7-10 倍的梯度步学会 RL 训练的策略，对应 50-100 倍的计算效率。

我们看到，在模型架构匹配（LoRA 秩 128）的情况下，蒸馏达到教师表现水平的速度比 RL 快约 7-10 倍。反向 KL 降至近零，AIME 分数在不到 10 个梯度步内恢复，而 RL 用了 70 步才达到该水平。

累计起来，所需计算的降低约为 50-100 倍：

- RL 要求在约等于评测上下文的长度上训练（以便策略学会上下文限制、不招致格式惩罚），而蒸馏在更短的上下文长度下也能合理学习，因为「已结束采样的轨迹」与「继续采样的轨迹」之间的奖励没有急剧截断。
- 当 SFT 初始化强时（即教师策略位于学生策略的支撑集内。当这不成立时——如「面向推理的蒸馏」中那样——我们需要显著更大的批大小。），在策略蒸馏用小得多的批大小就能有效工作，因为它每条 episode 提供显著更多的比特，从而降低梯度噪声。

尽管用过程监督训练强化学习模型通常很困难，这些结果表明，作为一个大方向，过程监督和密集奖励有潜力把学习效率提高一个数量级。这与 Lightman et al. 在 RL 研究中的早期结果相符。

### 蒸馏可以有效复用训练数据以提升数据效率

对从业者而言，收集大规模训练提示数据集困难且耗时。因此，我们希望能把同一提示在训练中复用多次。用 RL 训练时，对同一提示训练多个 epoch 往往导致对最终答案的简单记忆，大模型尤甚。（[“Reinforcement Learning for Reasoning in Large Language Models with One Training Example”](https://arxiv.org/abs/2504.20571)（Wang et al, 2025）不过在某些设置下提出了正面结果。）相比之下，在策略蒸馏通过最小化反向 KL 学会逼近教师的完整分布，而非记住单一答案。这让我们可以对同一提示训练多个样本。

我们重复上面在数学上训练 Qwen3-8B-Base 的实验，但这次只用从数据集中随机挑选的一条提示。（提示：“Evaluate the limit: lim_{x→∞} √x (∛(x+1) − ∛(x−1))”）

我们在这条提示上连续训练 20 步，每步一批 256 条 rollout，共 5120 条被评分的序列。我们以顺序方式对同一提示进行多步训练，这通常会导致过拟合。尽管这自然降低了计算效率，我们确实大致匹配了教师模型的表现——尽管只在一条提示上训练。

![](svgs/experiment-self-distillation-multiepoch.svg)

在本例中，在一条训练样本之上做多 epoch 训练足以蒸馏教师的 AIME'24 表现。我们的默认配置（也用于个性化实验）以每批 64 条提示、每条提示 4 个样本运行在策略蒸馏。所示所有方法均以每批 256 个样本训练。注意右图展示的是训练 KL，因此「总共 1 条提示」优于「每批 1 条提示」是自然的。

### RL 在语义策略空间中搜索

我们已经看到，在策略蒸馏可以用少得多的训练步数复刻 RL 提供的学习。对这一结果的一种解读是：与预训练不同，RL 并不把大量算力花在梯度步本身上。我们应当把 RL 视为把大部分算力花在*搜索*上——展开策略并分配功劳（credit）——而非做更新。（来自 [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)（Rich Sutton）：「突破性进展最终来自对立的方向，即通过**搜索**与**学习**来扩展计算」。）

通过随机梯度下降的预训练在高维参数空间中探索。预训练需要海量信息，而且非常难以蒸馏，部分原因是参数空间对每个网络来说多少是独一无二的。（[“The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks”](https://arxiv.org/abs/1803.03635)（Frankle and Carbin, 2018））预训练所需的梯度步计算极其昂贵和耗时。

相比之下，我们应当把 RL 看作在语义策略的空间中探索。（注意，策略上的探索与结果上的探索有微妙差别；RL 要求基模型一开始就有非零的成功率，因此已经「找到了结果」，但策略可以在 RL 过程中被不断打磨，使成功的结果更可能出现。）在每一步，RL 尝试对它过去发现的某个策略做一个小改动。它不是在参数空间中探索，而是靠运气「撞见」新策略——它在已有权重的集合中随机采样。

一旦找到好策略，蒸馏就充当学习它的捷径：在策略蒸馏不需要建模 RL 课程中的中间策略，而只需建模最终学到的策略。如果我们只关心最终策略（这在生产用例中很常见），就不必花费算力去建模所有中间策略。

考虑一个类比：在科学研究中，我们花费大量时间和资源寻找答案、探索新想法。一旦某个结果被发现，用自然语言把它教给别人要简单得多。我们可以把它与体育运动这类直觉性的身体技能对比：它们难教得多，因为知识以一种只被我们自己 readily 理解的内在语言（例如肌肉记忆）存在。运动只能通过反复练习学会。

### 在策略学习作为持续学习的工具

在「面向个性化的蒸馏」一节中，我们探索了在策略蒸馏把专门化的训练行为重新引入模型的能力。这可以推广到更广的一组持续学习任务：在不退化先前能力的前提下获取新知识。

以往工作发现在策略学习（RL）比离策略学习遗忘得更少。（[“RL's Razor: Why Online Reinforcement Learning Forgets Less”](https://arxiv.org/abs/2509.04259)（Shenfeld et al, 2025））然而，RL 只塑造行为——它不能很好地教授新知识，因此不足以支撑持续学习。

在上面一节中，我们看到 SFT（包括离策略蒸馏）无法支撑持续学习，因为它会使行为退化。我们更深入地调查了这一点，并用一个直接的例子加以证明。与上面类似，我们通过取 Tulu3 提示、以 `temperature = 1.0` 从 Qwen3-32B 采样、且不做进一步修改来构建数据集。因此，该数据集对 Qwen3-32B 的 KL 为零。（「真正在策略」KL=0 数据的重要性，也在我们之前的文章[击败 LLM 推理中的非确定性](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)中被探讨过。）

当我们在这个由模型自身样本构成的数据集上运行 SFT 会发生什么？我们看到，任何大于零的实用学习率都会导致指令遵循评测表现的退化！

![](svgs/experiment-sft-on-policy.svg)

在 Qwen3-32B 自身样本之上运行 SFT 会降低表现。我们使用与个性化一节相同的学习率——那是出于实际表现考量扫出来的。线性学习率可以防止前向 KL / IF-eval 无限回退，但在学习率衰减到零之前无法恢复表现。

一个可能的解释是：虽然 KL 散度在期望上为 0，但每个有限批次在实践中会呈现略有不同的分布。在这些有限批次上训练会引起非零的梯度更新，进而使更新后的模型策略偏离其原始状态。这一过程随时间推移，把「在自身样本上的训练」变成了离策略训练，导致与离策略训练相同的误差累积和长序列发散。

在策略蒸馏始终保持在策略，而且由于教师保持固定，学生收敛于教师的期望行为，在自蒸馏设置中不会像 SFT 那样发生退化。这使在策略蒸馏成为持续学习的一个非常有前景的工具。

## 结论

我们探索了在策略蒸馏在如下场景中的应用：训练一个数学推理小模型，或一个持续学习的助手。我们把在策略蒸馏与另外两种后训练方法进行了比较：离策略蒸馏和在策略 RL。我们发现，在策略蒸馏结合了两全其美：在策略训练的可靠表现，与密集奖励信号带来的成本效率。

后训练是达到前沿模型能力的关键一环。通过利用来自学生的在策略采样与来自教师的密集监督，在策略蒸馏配方以前沿高算力 RL 运行的一小部分成本达到了这些能力。

我们的实现可在 [Tinker cookbook](https://github.com/thinking-machines-lab/tinker-cookbook/tree/main/tinker_cookbook/recipes/distillation) 找到。我们的工作探索了在策略蒸馏的简单直接的实例化，以清晰展示其优势。我们希望继续研究蒸馏的新应用、改进教师监督的新方法，以及提升数据效率和持续学习的方式。

在 Thinking Machines，我们的使命是用兼具前沿性能与适应性、个性化的 AI 模型赋能人们。在策略蒸馏是实现这一目标的有力工具。

## 引用

请按如下方式引用本工作：

```
Lu, Kevin and Thinking Machines Lab, "On-Policy Distillation",
Thinking Machines Lab: Connectionism, Oct 2025.
```

或使用 BibTeX 引用：

```
@article{lu2025onpolicydistillation,
  author = {Kevin Lu and Thinking Machines Lab},
  title = {On-Policy Distillation},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  note = {https://thinkingmachines.ai/blog/on-policy-distillation},
  doi = {10.64434/tml.20251026},
}
```

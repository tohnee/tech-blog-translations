---
title: "无悔 LoRA"
title_en: "LoRA Without Regret"
date: 2026-08-31
source: https://thinkingmachines.ai/blog/lora/
crawled: 2026-09-22
translated: 2026-09-22
---

# 无悔 LoRA

> 原文：[LoRA Without Regret](https://thinkingmachines.ai/blog/lora/) · Thinking Machines Lab

当今领先的语言模型包含多达上万亿（trillion）参数，在数十万亿 token 上预训练。基础模型的性能随规模持续提升——这些万亿参数对于学习和表示书面人类知识中的全部模式是必要的。

相比之下，后训练（post-training）涉及的数据集更小，通常聚焦于更狭窄的知识领域和行为范围。用一太比特（terabit）的权重来表示来自一吉比特（gigabit）或一兆比特（megabit）训练数据的更新，显得很浪费。这一直觉催生了参数高效微调（parameter efficient fine-tuning，PEFT）：通过更新一个小得多的参数集合来调整大型网络。

领先的 PEFT 方法是低秩适应（low-rank adaptation），即 LoRA。LoRA 把原模型中的每个权重矩阵 W 替换为修改版 W′ = W + γBA，其中 B 和 A 是两个加起来参数量远少于 W 的矩阵，γ 是常数缩放因子。实际上，LoRA 为微调所带来的更新创建了一种低维表示。

LoRA 可能在后训练的成本和速度上具备优势，此外还有几个运维层面的理由使它优于全量微调（下文简称 FullFT）：

- **多租户服务。**由于 LoRA 训练的是适配器（即 A 和 B 矩阵）而保持原始权重不变，单个推理服务器可以在内存中保留许多适配器（不同模型版本），并以批处理方式同时从中采样。（[Punica: Multi-Tenant LoRA Serving](https://arxiv.org/abs/2310.18547)（Chen, Ye, et al, 2023））vLLM 和 SGLang 等现代推理引擎实现了这一功能。
- **训练的集群布局规模。**对整个模型微调时，优化器状态需要与原始权重一起存储，且往往以更高精度存储。（训练时除了存储权重，我们通常还需要为全部权重存储梯度和优化器矩；而且这些变量通常以比推理权重存储（bfloat16 或更低）更高的精度（float32）存储。）因此，FullFT 通常需要的加速卡数量比从同一模型采样高一个数量级，因而需要不同的集群布局。由于 LoRA 训练的权重大幅减少、内存占用大幅降低，它可以在只比采样所用略大的布局上训练。这让训练更可及，也往往更高效。
- **加载与迁移的便利性。**需要存储的权重更少，LoRA 适配器在不同机器之间设置或迁移都快速便捷。

这些理由足以解释自 2021 年原始 LoRA 论文发表以来其日益流行的原因。（[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)（Hu et al, 2021））然而，文献对于 LoRA 相对 FullFT 的表现并无定论。

各方一致同意的是，LoRA 在类似预训练的场景中表现不佳（[LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673)（Biderman et al, 2024）），即那些数据集非常大、超出 LoRA 参数存储容量的场景。但对于后训练中典型的数据集规模，LoRA 有足够容量存储关键信息。然而，这一事实对样本效率和计算效率没有任何保证。问题是：*LoRA 能否匹敌全量微调的表现？如果能，条件是什么？*

在我们的实验中，我们发现：只要把几个关键细节做对，LoRA 确实能以与 FullFT 相同的样本效率学习，并达到相同的最终性能。

## 对 LoRA 而言什么最重要

本文涵盖我们进行的一系列监督微调和强化学习实验，用于确定 LoRA 在何种条件下能匹敌 FullFT 的效率。为此，我们与以往的 LoRA 实验有几处不同：

- 我们研究了训练集规模与 LoRA 参数数量之间的一般关系，而非聚焦于特定数据集和任务。
- 在监督学习中，我们测量 *log loss* 而非采用基于采样的评测，同样出于通用性的考虑。log loss 测量在训练步数和训练参数的多个区间上给出了干净的结果和缩放定律（scaling law）。

我们发现：

- 在中小型指令微调与推理数据集上的监督微调中，LoRA 与全量微调表现相同。
- 对于超出 LoRA 容量的数据集，LoRA 不及 FullFT。损失并非触及一个无法突破的明显下限，而是 LoRA 带来更差的训练效率，取决于模型容量与数据集规模之间的关系。
- 在某些场景下，LoRA 对大批大小的容忍度低于全量微调——当批大小超过某个点后，它在损失上付出更大的惩罚。这一惩罚无法通过增大 LoRA 秩来缓解；它是矩阵乘积参数化的固有属性，其训练动态与优化原始权重矩阵不同。
- 即使在小数据场景中，把 LoRA 应用于所有权重矩阵（尤其是 MLP 和 MoE 层）效果也更好。仅注意力 LoRA 即使在我们通过用更高秩来匹配可训练参数数量的情况下也不及前者。
- 即使在小秩下，LoRA 在强化学习中也与 FullFT 表现相当。我们发现 RL 需要的容量非常低，这是我们基于信息论论证所预期的结果。

我们还研究了 LoRA 超参数对其相对全量微调学习率的影响。我们考察了初始化尺度和乘子等超参数的一些不变性，并解释了为什么 1/r 前置因子使最优学习率（LR）近似与秩无关。我们还通过实验展示了 LoRA 的最优 LR 与 FullFT 的最优 LR 之间的关系。

我们实验的成果是对一个「低悔区（low-regret regime）」的刻画：在该区域中，就数据集规模与 LoRA 参数而言，LoRA 表现与 FullFT 相近。我们发现该区域覆盖了大多数后训练场景，为在许多应用中使用高效微调打开了大门。

## 方法与结果

我们设计实验来细致测量 LoRA 相比 FullFT 在一系列条件下表现的差异。以下是实验设置的若干细节：

- 我们把 LoRA 秩在三个数量级范围内变化（秩介于 1 到 512 之间），并与全量微调比较。
- 为消除使用次优学习率带来的潜在混淆，我们对每个实验条件都扫了 LR。我们使用恒定学习率调度（无预热、无冷却）。
- 我们的实验使用 Llama 3 系列模型（[The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783)（Dubey et al, 2024））和 Qwen3 模型（[Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)（Qwen Team, 2025）），包括一个专家混合（MoE）模型。
- 主要监督学习实验使用 Tulu3（[Tulu 3: Pushing Frontiers in Open Language Model Post-Training](https://arxiv.org/abs/2411.15124)（Ivison et al, 2024））和 OpenThoughts3（[OpenThoughts: Data Recipes for Reasoning Models](https://arxiv.org/abs/2506.04178)（Guha et al, 2025））数据集，分别聚焦指令遵循和推理。两个数据集在范围、结构和应用上差异显著，支撑了我们结果的通用性。
- RL 实验使用数学推理任务，以答案正确性作为奖励。

### LoRA 秩

我们在 Tulu3 数据集和 OpenThoughts3 数据集的一个子集上训练单个 epoch。对每个数据集和模型规模，我们扫了 LoRA 秩和学习率。在下图中，我们为每个秩画一条彩色曲线，该曲线通过在每个训练步上取所有学习率的逐点最小值得到：

![](svg/fig1.svg)

图 1：在 Tulu3 和 OpenThoughts3 数据集上不同秩的 LoRA 训练曲线。FullFT 和高秩 LoRA 有相似的学习曲线，损失随步数的对数线性下降。低秩 LoRA 在适配器容量耗尽时偏离最小损失曲线。在下排图（1B 模型）中，高秩 LoRA 在一个数据集上优于 FullFT，在另一个上不如 FullFT。由于训练动态或泛化行为的差异，LoRA 在不同数据集上的表现可能存在一些随机波动。

我们看到 FullFT 和高秩 LoRA 有相似的学习曲线，损失随步数的对数线性下降。中低秩 LoRA 在某个与秩相关的步数阈值处偏离最小损失学习曲线。直观上，当适配器容量耗尽时学习变慢，而容量由秩决定。

接下来，我们绘制损失随 LR 的变化，以确认我们的扫描覆盖了每个秩的最佳学习率。

![](svg/fig2.svg)

图 2：Tulu3 上不同 LoRA 秩的学习率与最终损失。高秩 LoRA 与 FullFT 的最小损失大致相同。LoRA 的最优 LR 高 10 倍。

我们发现 FullFT 的最优学习率比高秩 LoRA 低 10 倍。（参见 Biderman et al. (2024) 图 S1，其使用采样评测的实验发现了类似的 10 倍比例。）我们稍后在讨论 LoRA 超参数时会回到这一点。

不同秩的 LoRA 运行的最优 LR 似乎相近；我们在下文给出这一发现的理论解释。不过确实存在一些对秩的依赖：rank=1 的最优 LR 低于更高秩的 LoRA。rank=4 与 rank=512 之间最优 LR 的变化小于 2 倍。

### 批大小效应

我们发现，在某些设置下，LoRA 对大批大小的容忍度低于 FullFT。性能差距随批大小增大而扩大，且与秩无关。在下一个实验中，我们使用了 OpenThoughts3 的一个 10,000 条样本的小子集。

![](svg/fig3.svg)

图 3：批大小对 LoRA 与 FullFT 表现的影响。左：不同批大小的学习曲线显示大批大小下 LoRA（虚线）与 FullFT（实线）之间存在持续差距。右：最终损失随批大小的变化显示 LoRA 为增大的批大小付出更大惩罚。

图 3 左图显示大批大小下 LoRA（虚线）与 FullFT（实线）学习曲线之间的持续差距。在批大小为 32 的较小设置下，差距更小且随时间缩小。

右图绘制最终损失随批大小的函数。我们看到 LoRA 与 FullFT 的损失差距随批大小增大而不断扩大。

大批次下的学习差距似乎与秩无关，而更像 LoRA 本身的属性。可能的原因是：矩阵乘积参数化（BA）在该数据集上的优化动态不如全矩阵（W）有利。不过，LoRA 和 FullFT 都在较小批大小下取得最佳损失，因此这一差距在实践中可能不那么重要。

## LoRA 应用于哪些层

我们研究了把 LoRA 应用于网络中不同层的效果。Hu et al. 的原始论文建议只把 LoRA 应用于注意力矩阵，许多后续论文照做，不过近来的趋势是应用于所有层。（与我们的结果类似，QLoRA 论文也发现仅注意力 LoRA 的表现不如 MLP 或 MLP+注意力，不过他们发现 MLP+注意力 > MLP > 注意力，而我们发现前两者大致相等。）的确，把 LoRA 应用于所有层（特别是 MLP（包括 MoE）层）时，我们取得了好得多的结果。事实上，把 LoRA 应用于注意力矩阵相比只应用于 MLP 没有额外收益。（Biderman et al. (2024) 得到了类似结果：仅注意力 LoRA 在仅 MLP 之上没有额外收益。）

![](svg/fig4.svg)

图 4：仅注意力 LoRA 明显不如仅 MLP LoRA，并且在仅 MLP 之上叠加注意力也不能进一步提升表现。该效应在稠密模型（Llama-3.1-8B）和稀疏 MoE（Qwen3-30B-A3B-Base）上均成立。

仅注意力 LoRA 的不佳表现无法用参数更少来解释。在这个具体案例中，秩 256 的仅注意力设置不如秩 128 的仅 MLP 设置，尽管二者参数量大致相同。（对比下表中加粗的数字。）

| LoRA 配置 | 参数量 |
| --- | --- |
| mlp, rank=256 | 0.49B |
| attn, rank=256 | **0.25B** |
| all, rank=256 | 0.70B |
| mlp, rank=128 | **0.24B** |

Llama-3.1-8B 上 LoRA 的参数数量

在 MoE 实验中，我们在每个专家上单独训练一个 LoRA，每个的秩等于总秩除以活跃专家数（Qwen3 MoE 为 8）。这一缩放使 MoE 层的 LoRA 参数与 FullFT 参数之比与其他层相同。

我们在另外两个设置中做了类似的、比较不同 LoRA 层的实验：(1) 在 OpenThoughts3 数据集小子集上以 rank=256 做监督学习；(2) 在 MATH 数据集上做强化学习。实验设置在下一节描述。仅注意力 LoRA 在这些设置下同样不如仅 MLP LoRA（后者表现与 MLP+注意力相近）。

![](svg/fig5.svg)

图 5：改变 LoRA 应用层时的学习率与最终损失或奖励。

### 强化学习

我们实验的一个关键发现是：在运行策略梯度算法的强化学习中，即使秩低至 1，LoRA 也完全匹敌 FullFT 的学习表现。

这些实验中，我们使用了带重要性采样校正的基本策略梯度算法；目标函数为 objective = Σ_t (p_learner / p_sampler) · Adv_t。（参见 [Your Efficient RL Framework Secretly Brings You Off-Policy RL Training](https://fengyao.notion.site/off-policy-rl)）我们使用了类 GRPO 的中心化方案（[DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300)（Shao et al, 2024））：对每道题采样多条补全，并减去每组的平均奖励。

图 6（下图）展示了在 MATH（[Measuring Mathematical Problem Solving With the MATH Dataset](https://arxiv.org/abs/2103.03874)（Hendrycks et al, 2021））和 GSM（[GSM8K: Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)（Cobbe et al, 2021））数据集上的 LR 扫描，各自采用典型超参数。我们使用 Llama-3.1-8B 基座模型，因为 Qwen2.5 和 Qwen3 已知在能提升数学表现的数据上预训练过（如 Qwen 技术报告所述，[Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115)（Qwen Team, 2024）），这会使测量仅在 RL 期间学到的东西变得更难。

LoRA 表现出更宽的表现良好的学习率区间，并达到与 FullFT（黑线）相同的峰值表现——至少在 RL 噪声所容许的精度范围内如此。

![](svg/fig5-.svg)

图 6：在小学数学（GSM，左）或 MATH（右）数据集上做 RL 时，学习率与最终奖励（准确率）的关系。

这一结果可以从信息论角度预见到。监督学习可以说每条 episode 提供 O(token 数) 比特的信息。相比之下，在策略梯度方法中，学习由优势函数驱动，每条 episode 只提供 O(1) 比特。当每条 episode 包含数千 token 时，RL 每个训练 token 吸收的信息比监督学习少约 1000 倍。

我们可以基于实验给出更精确的数字。在 MATH 例子中，我们在约 10,000 道题上训练，每题 32 个样本。假设每条补全产生 1 比特信息，整个训练过程只需吸收 320,000 比特。Llama-3.1-8B 的秩 1 LoRA 已有 3M 参数（我们通过对模型所有权重矩阵上的 rank·d_in（矩阵 A）与 rank·d_out（矩阵 B）求和计算得到。），几乎是该数字的 10 倍。即使秩为 1，LoRA 也有充裕的容量来吸收训练期间提供的全部信息。

作为另一个参照点，[DeepSeek-R1-Zero](https://www.nature.com/articles/s41586-025-09422-z) 在 5.3M 条 episode 上训练（训练进行了 10,400 步，每步 32 道独立题目，每题采样 16 次。），对应 5.3M 比特信息。这低于一个低秩 LoRA 的参数量，我们预测其结果可以用 LoRA 复现。

为了进一步验证 LoRA 在推理 RL 中有效性的发现，我们在 DeepMath 数据集（[DeepMath-103K: A Large-Scale, Challenging, Decontaminated, and Verifiable Mathematical Dataset for Advancing Reasoning](https://arxiv.org/abs/2504.11456)（He et al, 2025））上用 Qwen3-8b-base 做了更大规模的实验，因为它比 MATH 数据集大得多，且总体上包含更难的问题。为加速实验，我们把训练和评测的样本长度限制为 8192 token。这一样本长度允许回溯和推理，但相对更长的思维链会限制表现。

![](svg/fig6.svg)

图 7：Qwen3-8b-base 在 DeepMath 数据集上的实验。左图中我们展示不同秩与全量微调的学习曲线。对每种设置，我们展示能带来最高最终表现的最佳学习率。右图绘制学习率与最终表现的关系。与之前的数学实验一样，LoRA 似乎有更宽的近最优学习率区间。

![](svg/fig7.svg)

图 8：Qwen3-8b-Base 在 DeepMath 数据集上实验的补充图。左图展示在 AIME 测试集（比训练集更具挑战性）上的基准分数。右图展示思维链（CoT）长度随训练步数的变化，可视为学会推理的标志。

我们观察到，当为每种设置挑选最优学习率时，不同规模的 LoRA 与全量微调的训练进展几乎完全相同。此外，在 AIME 2024 和 AIME 2025 的留出问题上评测模型时，我们看到了类似的结果。此外，LoRA 和全量微调运行表现出相似的定性行为：二者都发展出回溯、自我验证和上下文内探索等高级推理行为，这从模型 CoT 变长中可见。

## 设置 LoRA 超参数

LoRA 推广的一个障碍是必须选择最优超参数，它们与针对 FullFT 优化的超参数不同。在本节中，我们表明这个问题并不像初看那么令人生畏，并讨论与超参数选择相关的发现。

### 最优学习率与秩

沿用 Hu et al.，我们考虑 LoRA 的如下参数化：

W′ = W + (α/r) · BA

其中 r 是 LoRA 秩，α 是 LoRA 缩放因子，A、B 是 LoRA 权重矩阵（秩为 r）。遵循其他实现的标准做法，本文实验使用 α = 32。

1/r 缩放因子使最优学习率近似与秩无关。事实上，一个更强的条件成立——在训练初期，无论秩是多少，学习曲线完全相同。这一效应非常显著：在我们的实验中，不同秩学习曲线的接近程度让我们一度担心某个 bug 导致 rank 参数被忽略了。由此可知，在短训练区间内，最优 LR 也与秩无关。然而，正如我们上面在学习率对损失的图（图 2）中所展示的，在较长训练区间内，最优 LR 存在一些对秩的依赖。

![](svg/fig8.svg)

图 9：这些图考察训练早期、相同学习率下不同秩学习曲线的差异。左侧展示学习曲线。右侧展示秩 16 与 256 之间的差异，该差异随时间增大。奇怪的是，前几步它是负的（尽管极小），因此曲线的那部分未显示在图中。

我们可以通过考察第一次训练更新后 LoRA 矩阵的期望更新来部分解释这一结果。我们可以把 LoRA 乘积 BA 看作 r 个秩 1 外积之和：BA = Σ_{i=1}^{r} b_i a_i^T = Σ_{i=1}^{r} Δ_i，其中定义 Δ_i = b_i a_i^T。这里，∂Loss/∂Δ_i 对所有 i 相同；然而梯度 ∂Loss/∂b_i 和 ∂Loss/∂a_i 会依赖于初始化（例如 ∂Loss/∂b_i 依赖于 a_i）。由于 a_i 和 b_i 的初始化不依赖秩，可以得出 E[Δ_i] 对所有 i 相同且不依赖秩。训练的第一步中，每一项的期望更新相等且与秩无关。由此可得，(1/r)·Σ_{i=1}^{r} Δ_i 只是 r 个具有相同期望的项的样本平均，因此平均的期望——即适配器 (1/r)BA 的变化——不依赖秩。

### 参数化不变性

LoRA 有四个潜在适用的超参数：

1. 出现在 α/r 中的缩放因子 α。
2. 降投影矩阵 A 的学习率 LR_A。
3. 升投影矩阵 B 的学习率 LR_B。
4. 矩阵 A 的初始化尺度 init_A。对随机初始化而言，这是 A 初始元素的标准差。矩阵 B 初始化为零，因此无需定义 init_B。

要调节四个不同参数似乎令人生畏。然而，训练动态中的不变性意味着其中两个是冗余的，学习行为由两个决定。我们通过如下观察来证明这一不变性：当使用 Adam 且 ε = 0 训练时（我们可以把该结果推广到 ε > 0；此时需要按 1/q 缩放，因为梯度按该因子缩放。），优化过程对以下双参数变换不变。

对 p, q > 0：

- α → (1/(pq)) · α
- init_A → p · init_A
- LR_A → p · LR_A
- LR_B → q · LR_B

由于四个自由度中的两个不影响学习过程，我们剩下一个 2D 参数空间。我们可以为这个 2D 空间选择不同的基，例如下面这个便于直观解释的基：

- α · init_A · LR_B。它决定初始更新的尺度，或者说学习曲线的初始斜率。由于 B 初始化为零，LR_A 以及对 A 的初始更新无关紧要。
- init_A / LR_A。由于 Adam 每步大约以 LR_A 的幅度更新 A 的元素，这个时间尺度参数决定了要显著改变 A、使其偏离初始状态所需的步数。

我们可以用这个基重新解读以往 LoRA 工作中的一些提议。

LoRA+（[LoRA+: Efficient Low Rank Adaptation of Large Models](https://arxiv.org/abs/2402.12354)（Hayou et al, 2024））提议对 A 和 B 使用不同 LR，B 的速率更高。用上面的基表述，增大 LR_B 等价于增大 init_A/LR_A，即让 A 在更长的时间尺度上变化。

[Unsloth 的 LoRA 超参数指南](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)建议对高秩 LoRA 使用更高的 α 值，例如避免 1/r 缩放。这同样等价于增大 init_A/LR_A。当我们增大 α 时，需要相应调低 LR_A 和 LR_B 以获得相同的更新幅度。这反过来只是让 LR_A 相对 init_A 更小。

在我们的实验中，我们使用 HuggingFace `peft` 库（[PEFT: State-of-the-art Parameter-Efficient Fine-Tuning methods](https://github.com/huggingface/peft)（Mangrulkar et al, 2022））中由 Hu et al. 提出的标准参数化：A 用尺度 1/√d_in 的均匀分布初始化，B 零初始化，二者使用相同 LR，且 α = 32。在实验中我们未能改进这些超参数。

### LoRA 与 FullFT 的最优学习率

我们的实验表明，在同一应用中，无论监督学习还是强化学习，LoRA 的最优 LR 一贯是 FullFT 的 10 倍。这体现在每一张以学习率为横轴、表现（损失或奖励）为纵轴的 U 形图中。这一观察应当能让把学习超参数从 FullFT 迁移到 LoRA 变得更直接。

我们尚无对这一观察的充分理论解释。我们可以尝试从两个事实推导这一结果：最优 LoRA LR 对秩不变，以及满秩 LoRA 可与 FullFT 直接比较。这一分析给出的 LR 比例为「模型隐藏尺寸除以 2·α」，这与最优比例固定为 10、与基座模型无关的实验结果不符。

在我们的实证分析中，我们对 14 个不同的 Llama 和 Qwen 模型在 Tulu3 数据集上分别做了 LoRA 和 FullFT 的 LR 扫描。从这些扫描中，我们拟合了一个函数，基于模型隐藏尺寸以及是否为 Llama 或 Qwen 的指示变量来预测最优学习率。使用的函数形式为：

LR = M_LoRA · (2000 / hidden_size)^(model pow + LoRA pow)

其中：

- M_LoRA 是使用 LoRA 时应用的乘子（FullFT 时为 1）
- model pow 是指数调整量，对每个模型来源（Llama 和 Qwen）分别计算
- LoRA pow 是 LoRA 的额外指数调整量
- hidden size 是模型残差流（residual stream）的维度。

我们用线性插值基于扫描数据预测损失来给预测学习率打分，并以 14 个问题上的预测损失之和来评级参数。我们的优化发现 LoRA 相对 FullFT 的乘子为 9.8，Qwen3 与 Llama 模型对 hidden_size 的依赖不同，但 LoRA LR 与 FullFT LR 对 hidden_size 的依赖相同，即优化发现 LoRA pow = 0。

### 短训练与长运行中的学习率

LoRA 的典型初始化为有效学习率创造了一个隐式调度。这导致短训练与长训练运行之间的差异，以及与 FullFT 相比学习曲线形状上的某些差异。

训练开始时，B 初始化为零。当 B 非常小时，A 的变化对加到原始网络权重上的适配器 BA 的影响可以忽略。随着 B 变大，对 A 的更新开始对网络输出产生更大影响；随着 B 的尺度接近 A，有效学习率在训练过程中不断提高。我们发现在 Tulu3 和 OpenThoughts 数据集的完整训练运行结束时，B 矩阵的谱范数大于 A 矩阵。

这意味着较短训练运行应设置更高的最优 LR。初步证据表明，短运行的优化乘子约为 FullFT 的 15 倍（依据经验观察，更高乘子在约 100 步以内有效。），较长运行则收敛到上述 10 倍乘子。

## 讨论

我们希望超越实证结果，讨论一些与 LoRA 表现和适用性相关的更广泛的考量，这些对研究者和构建者都有意义。

首先，让我们更深入地审视主要结果，即 LoRA 表现与全量微调相近的两个条件：

1. LoRA 应用于网络的所有层，尤其是容纳大部分参数的 MLP/MoE 层。
2. LoRA 在不受容量约束时表现良好，即可训练参数数量超过要学习的信息量，后者可以用数据集规模来估计。

当 (1) 满足时，我们在训练一开始就得到与 FullFT 相似的学习动态。随后，只要 (2) 成立，LoRA 会持续表现得像 FullFT，直到开始接近容量极限。

### 为什么 LoRA 可能需要应用于所有层

如前所述，如果只把 LoRA 放在注意力层，即使在小数据区间学习也更慢。

一种可能的解释来自把经验神经切核（eNTK）看作少量微调时发生情况的近似，遵循 Malladi et al.（[A Kernel-Based View of Language Model Fine-Tuning](https://arxiv.org/abs/2210.05643)（Malladi et al, 2022））。eNTK 基于梯度的点积，具体是梯度 g_i = ∂/∂θ log p(token_i | prefix_i) 与 K(i, j) = g_i · g_j。因此，参数最多的层通常对核的影响最大。该论文还指出，当训练所有层时，LoRA 的 eNTK 近似等于全量微调的 eNTK。所以 LoRA 训练 ≈ eNTK(LoRA) ≈ eNTK(FullFT) ≈ FullFT。近似 eNTK(LoRA) ≈ eNTK(FullFT) 只有在我们把 LoRA 应用于包含构成这些点积的大部分参数的层时才成立。

### 监督学习和强化学习各需要多少容量？

以往工作（[Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws](https://arxiv.org/abs/2404.05405)（Allen-Zhu and Li, 2024））表明，神经网络每个参数可以存储 2 比特。这些结果关于长训练极限下吸收的最大信息量，而非计算效率或学习速率。

每参数 2 比特的结果依赖于精心构造、信息量精确可控的合成数据集。估计某个现实学习问题所需的信息量并不那么直接。一个经典的观察是：在最小化 log-loss 时，训练第一个 epoch 期间测得的总 log-loss 提供了对数据集描述长度的度量，即完全记住该数据集所需比特数的上界。LLM 数据集通常每 token 损失约 1 比特（0.69 nats），具体取决于数据集和模型规模。

这一估计度量的是完美记住数据集所需的容量，它高估了降低测试数据 log-loss 的「可泛化」学习实际所需的容量。度量监督学习的容量需求及其与可训练参数量的交互，是未来工作的开放问题。

对于 RL，我们声称策略梯度算法每条 episode 大约学习 1 比特信息，因为 episode 结束时只有一个奖励值。这不是 RL 的基本属性，其他算法完全可能从每条 episode 学到更多。例如，基于模型的 RL 算法训练学习型智能体预测观察并构建世界模型，可能每条 episode 提取更多信息。「每 episode 1 比特」的说法可能只狭窄地适用于策略梯度算法。

我们可以用信息论术语进一步磨砺这一比特计数论证。把一条 episode——由轨迹 τ 和最终奖励组成——视为一条消息（即一个嘈杂信道），提供关于未知奖励函数 R 的某些信息。我们以当前策略和训练历史为条件，考察策略梯度估计量与 R 之间的互信息。REINFORCE 更新为 G = S · Adv，其中 S = ∇ log p_θ(τ)。给定历史时 S 与 R 独立，因此唯一依赖 R 的成分是标量优势（Advantage）。

由数据处理不等式：

I(G; R | history) ≤ I((S, Adv); R | history) = I(Adv; R | S, history) ≤ H(Adv)。

如果我们把优势量化为 B 个桶，那么 H(Adv) ≲ log(B)。也就是说，每条 episode 获得的有用信息比特数是 O(1)，与模型规模无关。这些比特告诉我们，我们处于离散奖励函数集合（或等价地，最优策略类别）中的哪一个。这一互信息分析与某些优化算法理论分析中所用的方法相似。（[Information Complexity of Black-Box Convex Optimization: A New Look via Feedback Information Theory](https://www.mit.edu/~rakhlin/papers/ibc_optimization.pdf)（Raginsky and Rakhlin, 2009））注意，这一估计是训练所吸收信息的*上界*；实际学到的量取决于策略初始化等细节。例如，如果我们用一个得不到任何奖励的策略初始化，那么优势的熵为零（不是 log(B)），什么也学不到。

### LoRA 的计算效率优势

上面的实验以训练步数为横轴度量学习进展，但我们可能也关注不同方法的*计算效率*。我们计算出，LoRA 每一遍前向-反向传播所用的 FLOPs 略高于全量微调的 ⅔。因此，它总体上往往在计算效率上优于 FullFT。

我们通过分析给定权重矩阵上前向-反向传播所用的 FLOPs 来推导这一 ⅔ 比例。这些运算占神经网络模型 FLOPs 的绝大多数。我们使用以下记号：

- W ∈ R^(N×N) 是权重矩阵
- x ∈ R^N 是输入向量
- y = Wx ∈ R^N 是输出向量
- x̄, ȳ ∈ R^N 是反向传播中计算的损失对 x 和 y 的梯度
- W̄ ∈ R^(N×N) 是损失对 W 的梯度

全量微调执行以下操作：

**前向**

1. y = Wx（N² 次乘加）

**反向**

2. x̄ = Wᵀȳ（N² 次乘加）
3. W̄ += xȳᵀ（N² 次乘加）

前向传播需要 N² 次乘加，反向传播再需 2·N² 次，合计 3N²。需要二者的训练因此使用仅前向推理 3 倍的 FLOPs。

使用 LoRA 时，我们把 W 替换为 W + BA，其中 B ∈ R^(N×R)、A ∈ R^(R×N)，且 R ≪ N。由于我们只更新 Ā 和 B̄，我们把第三步更新 W̄ 替换为便宜得多的运算。A 和 B 是 N·R 规模的矩阵，因此对它们各自做完整的前向-反向计算需要 3NR 次乘加，而非 W 的 3N²。两者合计 6NR。我们还要对 Wx 和 x̄ 做前向-反向传播，相当于 FullFT 的前两步。乘加总数为 2N² + 6NR。当 R ≪ N 时，这略高于 3N² 的 ⅔。

如果我们以 FLOPs 而非训练步数为横轴绘制 LoRA 的表现（该分析省略了注意力的 FLOPs，在长上下文设置中这部分可能显著。），它会显示出相对 FullFT 的明显优势。

### 开放问题

与我们结果相关的若干问题，我们很乐意看到未来被研究：

- 磨砺我们对 LoRA 表现的预测，及其匹敌全量微调的精确条件。我们已经粗略刻画了等表现区间，并能以 token 数或 episode 数估计所需容量，但尚无法做出精确预测。
- 我们对 LoRA 学习率和训练动态的理论理解有限。一个能解释 LoRA 与 FullFT 学习率之比的更完整理论将很有价值。
- PiSSA（[PiSSA: Principal Singular Values and Singular Vectors Adaptation of Large Language Models](https://arxiv.org/abs/2404.02948)（Meng, Wang & Zhang, 2024））等 LoRA 变体按本文的方法测量表现如何？
- 把 LoRA 应用于 MoE 层有多种选择。LoRA 用户将受益于对这些方法各自表现的调查，以及每种方法与张量并行、专家并行等对大型 MoE 模型很重要的方法的兼容性研究。

## 结语

在 Thinking Machines，我们相信微调的力量能让 AI 在许多专业领域提升实用性。我们对 LoRA 的兴趣源于一个目标：让这种力量广泛可及，并能轻松地针对特定需求定制。

除实际用途外，对 LoRA 的研究还引导我们更深入地研究模型容量、数据集复杂度和样本效率。考察学习速度和表现如何依赖容量，为研究机器学习的基本问题提供了一个透镜。我们期待未来推进这一研究。

## 致谢

我们感谢 Dan Alexander Biderman、Weizhu Chen、Daniel Han 和 Sadhika Malladi 对本文早期草稿提出的深刻反馈。

## 引用

请按如下方式引用本工作：

```
Schulman, John and Thinking Machines Lab, "LoRA Without Regret",
Thinking Machines Lab: Connectionism, Sep 2025.
```

或使用 BibTeX 引用：

```
@article{schulman2025lora,
  author = {John Schulman and Thinking Machines Lab},
  title = {LoRA Without Regret},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  note = {https://thinkingmachines.ai/blog/lora/},
  doi = {10.64434/tml.20250929},
}
```

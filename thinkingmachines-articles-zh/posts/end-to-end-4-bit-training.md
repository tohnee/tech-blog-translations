---
title: "端到端 4 比特训练"
title_en: "End-to-End 4-Bit Training"
date: 2026-11-10
source: https://thinkingmachines.ai/blog/end-to-end-4-bit-training/
crawled: 2026-11-16
translated: 2026-11-16
---

# 端到端 4 比特训练

> 原文：[End-to-End 4-Bit Training](https://thinkingmachines.ai/blog/end-to-end-4-bit-training/) · Thinking Machines Lab

训练大语言模型需要计算并存储大量数值。为每个数值使用更少的比特可以降低内存占用，并让 GPU 更快地完成计算。但这里存在权衡：比特数越少，可表示的数值也越少，舍入也就越激进。更低精度的表示会给计算引入误差，最终损害精度。

例如，假设我们要存储数值 3.2，但我们的数值格式能表示的最近取值是 3 和 4。舍入到 3 会引入 −0.2 的*量化误差*，即实际值与量化格式可表示的取值之间的差。单次这样的误差看起来很小，但在训练过程中，随着舍入在各层与各个优化步骤中反复发生，这些误差会不断累积，进而干扰学习过程。

这正是低精度训练的核心挑战：如何在享受更快算术运算的同时，不引入干扰学习的误差？

我们通过在训练中使用三种关键数值格式来管理这一权衡：BF16、MXFP8 和 NVFP4。每种格式的精度是固定的，但速度取决于所用硬件。我们在 NVIDIA 的 Grace Blackwell Ultra 平台 GB300 上训练，该平台专为用 NVFP4 加速矩阵乘法而设计。值得注意的是，NVFP4 的存储比特数比 BF16 少 3.6 倍，而在 GB300 上运行速度最高可快 6 倍。

**数值格式**

| 数值格式 | 每值比特数 | GB300 PFLOPS |
| --- | --- | --- |
| NVFP4 | (4 × 16 + 8) ÷ 16 = 4.5 | **15** |
| MXFP8 | (8 × 32 + 8) ÷ 32 = 8.25 | 5 |
| BF16 | 16 | 2.5 |

GB300 上的 NVFP4 加速在大批量推理中非常有用，那里的权衡更偏向速度。但相比 BF16 和 MXFP8，该格式会显著增大量化误差。这一误差在训练不同阶段的重要性不同，因此必须对每个阶段分别权衡：预训练与监督微调（SFT）中的前向与反向传播，强化学习（RL）中的采样与训练。

**我们在训练不同阶段的优先级**

|  | 风险 |  | 回报 |  |
| --- | --- | --- | --- | --- |
|  | 最小化误差 | 最小化偏差 | 提升速度 | 降低内存占用 |
| 预训练前向 | ✓✓✓ | — | ✓✓ | — |
| 预训练反向 | ✓ | ✓✓✓ | ✓✓ | — |
| RL 采样器 | ✓✓✓ | — | ✓✓✓ | ✓✓✓ |
| RL 训练器 | ✓ | ✓✓✓ | ✓ | — |

速度在高批量步骤中最重要：预训练要处理数万亿 token，RL 采样每次 rollout 要生成数万个 token。每采样一个 token 还需要从全局内存加载模型权重，其开销随存储权重所需的比特数增长。

更新权重的反向传播会对一个 batch 中的许多 token 求平均，从而稀释随机分布的舍入误差的影响。但反向传播对量化偏差非常敏感——当数值在量化时持续向上或向下舍入，就会引入这种偏差。这种偏差不会相互抵消，反而会跨层、跨样本、跨训练步骤累积。

在训练 Inkling 2 Small 时，我们做出了以下决策：

* 前向传播中专家层采用 NVFP4 精度，并由专用 kernel 提供支撑。
* 反向传播采用 MXFP8 精度，配合重量化与随机舍入这两种降低梯度偏差的技术。
* 用量化技术加速 GPU 通信，缓解了我们在提升计算速度后暴露出的瓶颈。

据我们所知，Inkling 2 Small 是用原生 4 比特（4-bit）前向传播*端到端*训练过的最大模型。从预训练开始到最终的 RL rollout，我们始终以相同方式配置数值格式。这让训练更简单，也免去了在训练结束时交付量化 checkpoint 所需的校准。在我们最大的训练任务中，相比全 MXFP8 训练，这套方案在预训练中带来 8% 的 wall-clock 加速，在 RL 中带来 20% 的加速。本文中，我们将解释让这一切成为可能的细节。

## 选择量化的目标

理想情况下，我们希望在对模型精度影响最小的地方降低精度，同时带来可观的整体加速。最符合这一特征的层是混合专家（MoE）层：它们的计算开销很大，而经验表明，量化它们对精度的损害往往小于其他层。

今年早些时候，我们实现了 MoE 层的全 MXFP8 训练，发现它几乎不影响模型的计算效率（compute efficiency, CE）——CE 衡量引入新技术时训练损失与评估损失的变化。[Recipes for Pre-training LLMs with MXFP8](https://arxiv.org/abs/2506.08027), Mishra et al., 2025, [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361), Kaplan et al., 2020 然而，我们最初用全 NVFP4 训练的实验对模型 CE 造成了非常大的损失，精度下降超出我们能接受的范围。

在分别隔离前向与反向传播中 NVFP4 量化的影响后，我们发现只量化前向传播通常在速度与精度之间提供更好的权衡。但仅量化前向传播会在与反向传播的交互、GPU 通信等方面带来一系列影响。为理解这些影响，我们先详细考察 NVFP4 的工作原理。

## Blackwell 上的低精度格式

4 比特最多能表示 16 个不同的值：对 FP4 而言，就是 ±{0, 0.5, 1, 1.5, 2, 3, 4, 6}。明显的局限是无法表示大于 6 的数，这通过*块缩放*（block scaling）解决：存储一个缩放因子，用它乘以连续块中的所有值。NVFP4 根据每 16 个连续值组成的块中的最大绝对值进行缩放。例如，若该值为 −54，它会被表示为 −6，缩放因子为 9，块中每个值都基于该缩放进行舍入。

Blackwell GPU 还提供微缩放（microscaling, MX）格式，如 MXFP4 和 MXFP8，它们按 32 个值一块进行缩放。[OCP Microscaling Formats (MX) Specification](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf/), Rouhani et al., 2023 缩放因子所用的格式也不同：NVFP4 的缩放因子是 E4M3，精度更高但范围有限；而 MXFP4/MXFP8 的缩放因子是 E8M0，精度低得多，但能表示非常宽的值域。E4M3 表示 8 位浮点格式，含 1 个隐式符号位、4 个指数位和 3 个尾数位。E8M0 有 8 个指数位，没有符号位，也没有尾数位。NVFP4 缩放因子提供的更高精度，往往能在 LLM 负载中更准确地表示输入数据，因此量化误差比 MXFP4 更小。

下面的工具演示了 NVFP4 块缩放如何工作，以及它如何导致量化误差。（本文所有图表均基于 Inkling 2 Small 制作。）

> **交互工具（JavaScript 禁用时的静态回退内容）**
>
> 高精度值：96×6=576
>
> 量化误差：−17.7
>
> E4M3 缩放因子：符号 0 · 指数 1101 · 尾数 100
>
> 公式：(−1₂)0₂ × 10₂(1101₂ − 0111₂) × 1.100₂ = 96
>
> E2M1 值：符号 0 · 指数 11 · 尾数 1
>
> 公式：(−1₂)0₂ × 10₂(11₂ − 01₂) × 1.1₂ = 6

JavaScript 已禁用，因此比特位、字段框和公式显示的是预先算好的示例（593.7 → 96 × 6 = 576），不可编辑。

一个由 FP4 数与 FP8 缩放因子重建的 NVFP4 值。可编辑输入或单个比特位来探索其表示方式。灵感来自 [float.exposed](https://float.exposed)。

FP4 与 FP8 的组合让 NVFP4 能表示低至 2⁻¹⁰、高至 2688 的量级。在实践中，我们经常需要表示此范围之外的值，因此 NVFP4 通常还配有一个保存在 FP32 中的外层缩放因子，作用于非常大的一组值，例如整个 tensor。这样每个量化值都可以重建为 $x_i^{\text{FP4}} \times x_{i//16}^{\text{FP8}} \times x^{\text{FP32}}$，相当于把可表示范围整体上移或下移。例如，将 $x^{\text{FP32}}$ 设为 2，可表示量级范围就从 [2⁻¹⁰, 2688] 移到 [2⁻⁹, 5376]；设为 0.5 则向相反方向移动。

## 块缩放下的反向传播

网络的前向传播将量化后的激活乘以量化后的权重：$y = x_q w_q^T$。用 NVFP4 计算点积时，取 $x_q$ 的一行中 16 个值和 $w_q^T$ 的一列中 16 个值组成块，两两相乘，再将和乘以每个块的缩放因子。

计算反向传播时，我们需要转置前向传播中的 tensor：$dx = g w_q$，$dw = g^T x_q$。此时块取自 $x_q$ 的*列*和 $w_q^T$ 的*行*中的 16 个值：每个值与 15 个不同的邻居分在一组，导致缩放因子不同、表示的量化值也不同。下图展示了块缩放从按行翻转为按列的影响——在这个例子里，大多数值被舍入为零。

> **图 2（交互工具，JavaScript 禁用时的静态回退内容）**
>
> 切换项：1×16 缩放因子 / 16×1 缩放因子
>
> 高精度（色标：0 1 4 16 64）
>
> 16×16 的高精度数据块
>
> NVFP4
>
> 1×16 分组：256 个值全部保留——每个行组都有自己的缩放因子
>
> 16×1 分组：大值所在行得以保留；另有 19 个小值保留，其余 221 个舍入为零
>
> 图例：保留 · 大值 · 舍入为零 · 缩放因子组

JavaScript 已禁用——切换视图需要它；上图显示的是预先算好的 1×16 分组。

对一个包含整行大值的类似数据块进行量化。每行使用独立的 1×16 缩放因子可保留所有值；若改为每列使用 16×1 缩放因子，大值所在行会决定每列的缩放因子，大多数小值被冲为零。高度为对数刻度，小值之间的差异被放大。

这会造成前向与反向传播所用 tensor 之间的不匹配，可能导致梯度计算不准确。对权重 tensor，NVIDIA 提出了一个直接的解决方案：不按每个 1×16 块计算缩放因子，而是根据每个 16×16 方块中的最大值计算单一缩放因子，使 tensor 转置后缩放因子保持一致。[Pretraining Large Language Models with NVFP4](https://arxiv.org/abs/2509.25149), NVIDIA et al., 2025；另见 [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) 中的 FP8 表述，DeepSeek-AI et al., 2024。

这种方法的主要缺点是会导致大量值下溢。把块大小从 16 个值增大到 256 个，会使其对离群值高度敏感：256 个值中只要有一个大值，就会把缩放因子推高，使其余值被舍入为零。

> **图 3（交互工具，JavaScript 禁用时的静态回退内容）**
>
> 切换项：1×16 缩放因子 / 16×16 缩放因子
>
> 高精度（色标：0 1 4 16 64）
>
> 16×16 的高精度数据块
>
> NVFP4
>
> 1×16 分组：256 个值中有 241 个保留——离群值所在的 1×16 组围绕它被舍入为零
>
> 16×16 分组：只有离群值保留——其余所有值都舍入为零
>
> 图例：保留 · 大值 · 舍入为零 · 缩放因子组

JavaScript 已禁用——切换视图需要它；上图显示的是预先算好的 1×16 分组。

对一个含单个大离群值的数据块进行量化。与整个 16×16 块共用一个缩放因子相比，为每个 1×16 组使用独立缩放因子可以限制小值的损失。高度为对数刻度，小值之间的差异被放大。

我们尝试过这种方法，但最终发现按 16×16 方块计算缩放因子过于粗糙，对 CE 的损害超出我们可接受的范围。要让 NVFP4 训练可行，我们需要用 1×16 缩放因子量化权重，同时避免块缩放转置带来的不匹配。

## 重量化与随机舍入

使用 16×16 方块可以消除这种不匹配，因为前向与反向传播之间能获得逐比特完全一致的表示——$w_q = (w_q^T)^T$——但严格的完全一致并非必要。关键要求是前向与反向传播所用的 tensor 在*期望*上相等：$E[w_q] = E[(w_q^T)^T]$。保持期望值相等即可解决反向传播中的偏差问题，而放宽逐比特一致性的约束，也为前面提出的转置问题提供了几种不同的解法。

我们选择了一个直接的方案：将前向传播的 tensor 反量化，以更高精度转置，然后用*随机舍入*（stochastic rounding, SR）重新量化。与标准量化（也称就近舍入量化）不同，SR 按概率向上或向下舍入每个值，概率与其到两个相邻取值的距离成反比。

例如，假设前向传播 tensor 中有一个值 5.4，在缩放因子为 9 的块中量化。5.4 除以 9 等于 0.6，就近舍入到最近的 FP4 值 0.5。前向传播中使用的量化值是 4.5，这正是我们希望在反向传播中（在期望意义上）恢复的值。

我们可以反量化这个值，使其以高精度表示，但在反向传播中它现在被分到了另一个块。假设新缩放因子为 2。若用 NVFP4 重新量化，$4.5 \div 2 = 2.25$ 现在需要量化到 FP4。确定性舍入会把它表示为 2，量化值为 $2 \cdot 2 = 4$。随机舍入则有四分之三的概率舍入到 2，四分之一的概率舍入到上方最近的邻居 3。重新量化后，前向传播的 4.5 在期望上得以保留：$2_{\text{scale}} \cdot (0.75 \cdot 2 + 0.25 \cdot 3) = 4.5$。关键的是，随机舍入在 Blackwell GPU 上也有硬件加速。

在设计这一方案时，我们受到了 TetraJet-v2 和 Quartet II 的启发，它们同样会对前向传播的 tensor 重新量化。[TetraJet-v2: Accurate NVFP4 Training for Large Language Models with Oscillation Suppression and Outlier Control](https://arxiv.org/abs/2510.27527), Chen et al., 2025, [Quartet II: Accurate LLM Pre-Training in NVFP4 by Improved Unbiased Gradient Estimation](https://arxiv.org/abs/2601.22813), Panferov et al., 2026 将 SR 直接作用于反量化后的值有一个好处：它让我们能在重新量化时选择任意精度。我们发现，把权重和激活随机重新量化到 MXFP8，再使用 MXFP8 矩阵乘法计算梯度，能在精度与速度之间取得最佳权衡。

> **图 4（量化线性层示意图）**
>
> 从第 i − 1 层 · BF16 激活 · 按 token 量化为 NVFP4（使用 4/6）· FPROP · NVFP4 GEMM · 到第 i + 1 层
>
> FP32 权重 · 按专家量化为 NVFP4 · 反量化 · 转置 · 用 SR 量化为 MXFP8 · DGRAD · MXFP8 GEMM
>
> WGRAD · MXFP8 GEMM · 优化器
>
> 从第 i + 1 层 · BF16 梯度 · 用 SR 量化为 MXFP8 · 转置 · 用 SR 量化为 MXFP8 · 到第 i − 1 层
>
> 图例：FP32 / BF16 / MXFP8 / NVFP4

我们量化后的线性层：前向传播用 NVFP4 计算，反向传播用 MXFP8 计算；在对保存的激活与权重重新量化时使用随机舍入。

## 量化通信

借助新的 NVFP4 矩阵乘法（GEMM），理论上我们的 MoE 层前向传播应比 MXFP8 实现快约三倍。但在降低精度后，我们注意到遇到了一个瓶颈：专家并行（expert parallelism）期间的通信。

由于 MoE 层通常非常大，将专家分布到不同 GPU 上是常见做法。计算 MoE 层时，一个小型 router 决定每个 token 应去向何处，随后 token 被*分发*（dispatch）到承载被路由专家的 GPU。GEMM 完成后，这些被路由专家的计算结果被送回源 GPU 并*合并*（combine），形成 MoE 层的最终输出。在 NVIDIA GB300 NVL72 系统上，token 通常通过 NVLink 传输，其每个方向的带宽为 900 GB/s。与此同时，NVFP4 GEMM 的运行速度最高可达 15 PFLOPS。两者相除，每块 GPU 在接收一个字节的时间内可以执行多达 16,000 次浮点运算。除非到达的每个字节至少伴随这么多计算，否则 Tensor Core 就会空闲等待 NVLink。

我们发现这种失衡造成了瓶颈：要么 MoE GEMM 因为等待接收分发的 token 而无法执行，要么后续操作（在 Inkling 2 Small 中是短卷积）因为等待接收合并后的 token 而无法开始。在分发阶段，我们通过以 NVFP4 分发 token 来避免这个问题。与 TetraJet-v2 和 Quartet II 一样，我们的反向传播使用前向传播中量化后的激活（而非高精度激活）来计算（参见[图 4](#fig:linear-layer-figure)中权重梯度 WGRAD 计算的输入），这减少了通过 NVLink 发送的数据量，足以缓解分发瓶颈。然而在合并阶段，输出激活必须保持更高精度（默认为 BF16），以免损害模型性能。

我们也对合并阶段传输的数据进行量化，以缓解通信瓶颈。我们最初尝试把合并后的激活量化为 MXFP8，但发现由于 MXFP8 对离群值的表示能力较差，这会严重损害性能。相反，我们发现先执行 32 维随机 Hadamard 变换（random Hadamard transform, RHT），再量化为块缩放的 S2F6（另一种 8 比特格式），在训练中没有带来可测量的精度下降。

> **图 5（专家重叠示意图）**
>
> 切换项：16 比特合并 / 8 比特合并
>
> 分发 → 计算 → 合并；w13 · Q · w2；专家波次 1 / 专家波次 2 / 专家波次 3
>
> 图例：
>
> * 分发 all-to-all
> * w13 GEMM
> * 量化
> * w2 GEMM
> * 合并 all-to-all

JavaScript 已禁用——当前显示的是 16 比特合并；切换视图需要 JavaScript。

细粒度重叠与专家波次，与 DeepSeek-V4 相同。[DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence](https://arxiv.org/abs/2606.19348), DeepSeek-AI et al., 2026 在合并阶段量化数据可以缩短图中右侧合并的尾部，从而加速 MoE。

RHT 施加一个旋转，倾向于把输入数据平滑化。当输入数据含离群值时，这可以降低量化误差。已有工作表明，在低精度下，整数格式表示经 RHT 变换的数据往往比浮点格式更准确。[INT v.s. FP: A Comprehensive Study of Fine-Grained Low-bit Quantization Formats](https://arxiv.org/abs/2510.25602), Chen et al., 2025, [Bridging the Gap Between Promise and Performance for Microscaling FP4 Quantization](https://arxiv.org/abs/2509.23202), Egiazarian et al., 2025。S2F6 是一种[定点格式](https://en.wikipedia.org/wiki/Fixed-point_arithmetic)，含 2 个有符号整数位和 6 个小数位，能表示从 −128/64 到 127/64 的线性插值取值，非常接近整数格式。下图展示了 Hadamard 变换如何平滑输入数据，使我们能用更小的缩放因子对其进行量化，从而降低量化误差。

> **图 6（交互工具，JavaScript 禁用时的静态回退内容）**
>
> 播放 / 正在播放… / 重放
>
> 高精度数据
>
> 经 RHT 之后
>
> 坐标轴：−500 −250 0 250 500
>
> 图例：数值 · 离群值（|v| ≥ 200）

随机 Hadamard 变换在保持总能量的同时让数值分布更均匀；作为正交变换，它之后可以被精确逆转以恢复原始数据。红色点追踪变换前属于离群值的那些取值。

方便的是，Blackwell GPU 包含专用 PTX 指令，可高效地在块缩放 S2F6（带 FP8 缩放因子）与其他格式之间转换数据：`cvt.rn.dst.src` 表示从 src 到 dst 的数据类型转换。详见 [PTX ISA](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html)。

```
cvt.frnd2.satfinite{.relu}{.scaled::n2::ue8m0}.s2f6x2.f32
    d, a, b{, scale-factor};
cvt.frnd2.satfinite{.relu}{.scaled::n2::ue8m0}.s2f6x2.bf16x2
    d, a{, scale-factor};
cvt.rn{.satfinite}{.relu}{.scaled::n2::ue8m0}.bf16x2.s2f6x2
    d, a{, scale-factor};
```

这使我们能为该数据类型实现非常高效的 kernel。在每块 GPU 上计算完 MoE 输出后，我们在 w2 分组 GEMM 的 epilogue 中高效地计算 RHT 并量化为块缩放 S2F6，每 32 个值共用一个缩放因子。数据接收过程中，它会被即时反量化并聚合，随后再执行 RHT 的逆变换。这使合并阶段传输的数据量从每值 16 比特降到每值 8.25 比特，缩短了合并的尾部，加速了 MoE 层，如[图 5](#fig:ep-overlap) 所示。

## 低精度训练的 kernel

要充分利用 NVFP4，需要专用 kernel，我们为低精度配方自研了这些 kernel。我们的 MoE 融合 kernel 栈代号为 BBBK，即 Big Beautiful Blackwell Kernel。它以峰值硬件利用率支撑训练与推理，同时保持完全确定性的计算。

MoE 层的计算过程通常由矩阵乘法主导。我们使用 GB300 独有的最大 2SM UMMA 指令（K=96）让 Tensor Core 饱和运转，其输入由 6 级被乘数流水线和 7 级缩放因子流水线供给。然而，我们的精度配方也对 GPU 的算术逻辑单元（ALU）提出了很高要求。即使 Tensor Core 已饱和，kernel 仍可能在 ALU 密集的步骤上停顿，例如计算缩放因子、重新量化权重、应用随机舍入以及合并数据传输。

为消除这些停顿，BBBK 尽可能让更多硬件流水线同时饱和。例如，我们把 RHT 与 S2F6 量化直接融合进 w2 GEMM 的 epilogue。更广泛地说，我们把激进的 epilogue 融合与 ALU 向量化、指令调度、寄存器规划与打包，以及投机式 megakernel 调度结合在一起。训练时，BBBK 同时让 NVLink、ALU 和 Tensor Core 饱和运转；在 RL 采样时，它则达到了由 NVLink 和 HBM 决定的延迟下限。

## 配方细节

我们借鉴了若干已有的 NVFP4 训练工作来完善配方。我们把最后 16.6% 的层保持更高精度，这些层我们以 MXFP8 而非 BF16 计算。NVIDIA 的配方把这一比例设为 15%，但在我们的预训练阶梯中，层数按 6 倍缩放，因此把比例设为 ⅙ 在我们的设置中很合适。量化激活时，我们使用 Four Over Six（4/6）——一种在 NVFP4 量化期间于两个缩放因子之间做选择以降低量化误差的技术。[Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling](https://arxiv.org/abs/2512.02010), Cook et al., 2025; 另见 [Ziang Li 的文章](https://humansand.ai/blog/nvfp4-rl?v=3#four-over-six-for-rl-weights-and-activations)，对该技术有很好的解释。量化权重时我们不使用 4/6。

借鉴 Composer 2 的做法，量化权重时我们使用按专家的外层缩放因子，量化激活时使用按 token 的外层缩放因子，从而实现更高效率、batch 不变性，且无需担心因果泄漏。[Composer 2 Technical Report](https://arxiv.org/abs/2603.24477), Cursor et al., 2026 在我们最大的训练任务中，这套配方在 SFT 和 RL 期间都无需改动即可工作。在预训练 Inkling 2 Small 时，它损失约 2% 的计算效率——意味着若用 MXFP8 训练，模型用约少 2% 的 FLOPs 就能达到相同的 loss——以此换取 NVFP4 带来的加速。在 RL 中收益则大得多：端到端显著加速，且 reward 没有可察觉的差别。

## 结语

十年前，神经网络能否用每个参数少于 32 比特来训练还是未知数：直到 2020 年 BF16 随 Ampere 首次进入 NVIDIA GPU 时，默认格式仍是 FP32。[NVIDIA Ampere Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-ampere-architecture-in-depth/), Krashinsky et al., 2020 今天，我们常常把 BF16 称为「高精度」，并且已经为 8 比特乃至 4 比特格式的训练找到了稳健的用例！NVIDIA 富有远见的硬件设计让这些进步成为可能，我们深受启发。我们将继续推进：我们正在积极探索让反向传播也用 FP4 计算的配方，以及我们的配方在 NVIDIA 最新的 Vera Rubin 系统上将如何演进。

我们预训练与后训练两方面的加速，源自科学与工程上一系列改进的汇聚——它们触及技术栈的每个部分，并相互叠加。几个月前，训练一个规模与 Inkling 2 Small 相近的模型需要数周；而 Inkling 2 Small 在 GB300 NVL72 机架上仅用 68 小时就完成了预训练。我们的数值配方只是众多改进中的一项，也是我们仍在持续迭代的一项。

每一次实验和训练都让我们学到新的经验，我们期待在未来的文章中分享更多。

## 引用

引用本文时请使用：

```
Cook, Jack and Thinking Machines Lab, "End‑to‑End 4‑Bit Training",
Thinking Machines Lab: Connectionism, Nov 2026.
```

或使用 BibTeX 引用：

```
@article{cook2026lowprecision,
  author = {Jack Cook and Thinking Machines Lab},
  title = {End‑to‑End 4‑Bit Training},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2026},
  note = {https://thinkingmachines.ai/blog/end-to-end-4-bit-training/},
}
```

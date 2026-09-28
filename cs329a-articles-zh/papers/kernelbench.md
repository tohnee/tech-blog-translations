---
title: "KernelBench：大语言模型能写出高效的 GPU 内核吗？"
title_en: "KernelBench: Can LLMs Write Efficient GPU Kernels?"
arxiv: 2502.10517
source: https://arxiv.org/abs/2502.10517
crawled: 2026-09-23
translated: 2026-09-23
---

# KernelBench：大语言模型能写出高效的 GPU 内核吗？

> 原文：[KernelBench: Can LLMs Write Efficient GPU Kernels?](https://arxiv.org/abs/2502.10517) · Stanford CS329A 指定阅读

Anne Ouyang（斯坦福大学）、Simon Guo（斯坦福大学）、Simran Arora（斯坦福大学）、Alex L. Zhang（普林斯顿大学）、William Hu（斯坦福大学）、Christopher Ré（斯坦福大学）、Azalia Mirhoseini（斯坦福大学）

注：* 表示同等贡献。联系方式：aco@stanford.edu、simonguo@stanford.edu。

###### 摘要

高效的 GPU 内核对构建高性能机器学习架构至关重要，但编写内核是一项耗时且需要大量专业知识的挑战；因此，我们探索使用语言模型（LM）来自动化内核生成。我们提出 KernelBench，一个用于评估 LM 在 250 个精心挑选的 PyTorch 机器学习工作负载上编写快速且正确内核之能力的开源框架。KernelBench 呈现了一个真实的工程环境，在该基准上的进展可以直接转化为更快的实用内核。我们提出一个新的评估指标 $\text{fast}_{p}$，它衡量生成的内核中既功能正确、又相对基线取得大于可调阈值 $p$ 加速的比例。我们对多种最先进模型与测试时方法的实验表明，前沿推理模型开箱即用时表现最佳，但总体上仍显不足，只在不到 20% 的情形中匹敌 PyTorch 基线。虽然我们表明可以通过在迭代改进中利用执行与性能剖析反馈来改进结果，KernelBench 仍是一个颇具挑战的基准，且随着加速阈值 $p$ 的提高，其难度还会进一步增加。

## 1 引言

AI 依赖高效的 GPU 内核来实现高性能以及成本与能耗的节省；然而，开发内核仍然充满挑战。机器学习架构经历了寒武纪大爆发式的增长（Tay et al., 2022；Peng et al., 2023；Dao & Gu, 2024），但它们可用的实现常常远逊于其峰值潜力。我们也在见证 AI 硬件的激增（NVIDIA, 2017b；NVIDIA, 2020；NVIDIA, 2022；Jouppi et al., 2023；Groq；Cerebras；Graphcore），每种硬件都有不同的规格与指令集，跨平台移植算法是一个痛点。一个关键例子是 FlashAttention 内核（Dao et al., 2022），它对运行现代 Transformer 模型至关重要——最初的内核于 2022 年发布，距 Transformer 提出已有五年；而从 NVIDIA Hopper GPU 发布到把该算法迁移到新硬件平台又花了两年。我们探索这个问题：语言模型能帮助编写正确且经过优化的内核吗？

![Refer to caption](2502.10517v1/figures/KernelBench-Flow-HD.png)

图 1：KernelBench 评估 LM 生成高性能 GPU 内核的能力。KernelBench 任务总览：KernelBench 要求 LM 为给定的目标 PyTorch 模型架构生成优化的 CUDA 内核，并执行自动化评估。

AI 工程师在开发内核时会使用丰富的信息，语言模型（LM）能否模仿这一工作流程尚不清楚。他们使用编译器反馈、性能剖析指标、硬件特定的规格与指令集，以及硬件效率技术方面的知识（例如分块、融合）。他们可以使用从汇编（例如 DeepSeek-AI（2025）中的 PTX）到更高级库（ThunderKittens（Spector et al., 2024）、Triton（Tillet et al., 2019））的各种编程工具。与现有的 LM 代码生成工作负载（Yang et al., 2024a）相比，内核编写需要大量且多样的信息。我们首先设计一个反映典型 AI 工程师工作流的环境，并支持向 LM 提供这些丰富信息。该环境应当：

- 自动化 AI 工程师的工作流。模型应当拥有完全的自由来决定优化哪些算子以及如何优化。

- 支持多样的 AI 算法、编程语言与硬件平台。

- 便于以程序化方式评估 LM 生成结果的性能与功能正确性。它还应能从生成的内核中捕获性能剖析与执行信息。

我们提出 KernelBench 来生成并评估内核，它回应了上述考量。KernelBench 在三个层级的 AI 工作负载上测试 LM 的优化能力：

1. 单个运算：我们纳入了各种 AI 算子，包括矩阵乘法、卷积、激活、归一化和损失。虽然 PyTorch 已经使用由专家优化过的闭源内核，使这成为一个颇有挑战性的基线，但如果 LM 能为这些运算生成开源内核，将是很有价值的。

2. 运算序列：我们提供包含 3-6 个单个运算的问题（例如 matmul 这样的主循环算子后接 ReLU 与 Bias 这样的逐元素算子）。这可以评估模型融合多个算子的能力。

3. 端到端架构：我们从 GitHub 上流行的 AI 仓库（包括 pytorch、huggingface/transformers 和 huggingface/pytorch-image-models）中选取架构。这些架构包含大量运算。

模仿 AI 研究者的工作流，LM 以 PyTorch 参考代码为输入，输出该代码的优化版本。与人类内核开发过程类似，我们的环境让 LM 能够借助编译器与性能剖析器的反馈进行迭代以改进性能。LM 可以自由使用任何编程语言，并自行决定优化 PyTorch 代码的哪些部分以及如何优化。我们的流水线允许向 LM 提供多样的信息，包括硬件特定信息、示例内核以及编译器/剖析器反馈。

我们观察到，前沿模型与开源模型在 KernelBench 上开箱即用的表现不佳，OpenAI-o1 与 DeepSeek-R1 在不到 20% 的任务上匹敌 PyTorch Eager 基线。这些模型生成的内核深受执行错误、功能正确性问题之苦，并且无法执行平台特定的优化。为了找出改进方向，我们开展了一系列实验与分析，并发现：

1. 编写功能正确的内核对模型而言仍然困难：虽然模型能够通过推理或多次尝试修复执行失败，但它们难以产出功能正确的代码。此外，我们观察到 LM 尝试更复杂的优化/小众硬件指令（例如张量核心 wmma）与产出无错内核之间存在权衡。我们推测这是因为 CUDA 在开源训练数据中是一种低资源语言——在流行的代码语料库 The Stack v1.2 中只占 0.073%（Li et al., 2023；Kocetkov et al., 2022）。

2. 模型展现了通过优化产出高性能内核的潜力：我们观察到若干 LM 做出算法级改进的实例——例如利用稀疏性、算子融合以及利用硬件特性。当我们显式地向 LM 提供硬件信息（例如带宽与 TFLOP 规格）以及硬件优化技术（例如分块、融合）的示例时，观察到了更多此类实例。虽然这些能力尚处萌芽，LM 确实展现了生成高性能内核的潜力。

3. 利用反馈对减少执行错误和发现更快解法很重要：通过在上下文中向 LM 提供执行结果与剖析器反馈，内核质量在多次改进后显著提升，$\text{fast}_{1}$ 分别从 12%、36% 和 12% 提升到 43%、72% 和 18%。

我们的发现凸显了要让 LM 用于内核编写所必须解决的技术挑战，包括但不限于：如何提升 LM 在低资源数据环境下的表现，以及如何从我们可提供给模型的丰富信息中做出选择。为应对这些挑战，我们贡献了：(1) 一个用于研究 LM 内核生成的开源框架，附带一套全面的评估问题；(2) 对当前 LM 所处位置以及如何实现「由模型生成高效内核」这一未来的分析。

## 2 相关工作

内核库与编译器。我们从自动化程度、覆盖广度与性能三个维度评估现有的内核编程方法。主流内核编程库如 cuDNN（NVIDIA, 2014）、CUTLASS（NVIDIA, 2017a）与 Apple MLX（Apple, 2020）是硬件特定的，并且需要人类专家投入大量工程 effort。其他库，如 ThunderKittens（Spector et al., 2024）与 Triton（Tillet et al., 2019），成功地帮助 AI 研究者编写大量快速且正确的内核（Arora et al., 2024；Yang & Zhang, 2024），但仍需人工编程。基于编译器的工具，如 torch.compile（Paszke et al., 2019）与 FlexAttention（PyTorch Team et al., 2024），自动提供窄范围的优化。与这些努力相反，我们提出的问题是：LM 能否为广泛的 AI 工作负载自动生成高性能内核。

面向性能优化代码生成的 LLM。过去一年中，已有多项工作构建能自动化算法编程（Chen et al., 2021；Shi et al., 2024；Li et al., 2022）、解决 GitHub issue（Yang et al., 2024a；Yang et al., 2024b）以及领域特定编程（Yin et al., 2022；Lai et al., 2022）的 LM。这些工作聚焦于产出正确且可用的代码，后续工作则探索了 LM 产出具有更优算法与渐近效率之解的能力（Nichols et al., 2024；Waghjale et al., 2024）。KernelBench 聚焦于实际耗时（wall-clock）效率。LM 生成高性能计算（HPC）代码，这需要理解底层硬件特性与设备指令集，以及并行处理器的常见性能特征。

HPC 代码生成方面的现有工作评估了 LM 在把任意 C++ 代码样本翻译为 CUDA（TehraniJamsaz et al., 2024；Wen et al., 2022）或生成 GEMM 等知名低级内核（Valero-Lara et al., 2023；Wijk et al., 2024）上的表现。KernelBench 则从真实、现代的深度学习工作负载中精选了 250 个多样的内核，其中许多并没有现成的人类编写实现——换句话说，解决 KernelBench 任务对真实深度学习 workload 有立竿见影的益处。

## 3 KernelBench：一个 AI 内核生成框架

KernelBench 是一个新框架，用于评估语言模型为广泛的 AI 工作负载生成高性能内核的能力。本节描述任务格式、内容与评估指标。

### 3.1 KernelBench 任务格式

KernelBench 包含 250 个任务，代表一系列 AI 工作负载，并且易于扩展到新工作负载。任务的端到端规格如图 1 所示，并在下文描述。

任务输入：给定一个 AI 工作负载，任务的输入是用 PyTorch 编写的参考实现。模仿 AI 研究者的工作流，PyTorch 代码包含一个派生自 torch.nn.Module() 的名为 Model 的类，其中标准的 __init__ 与 forward() 函数（以及任何辅助函数）由该 AI 工作负载的 PyTorch 运算填充。

AI 算法通常作用于大型张量数据。工作负载的最优内核取决于张量的大小与数据类型（例如 BF16、FP8）。因此，每个任务还包含 get_inputs() 与 get_init_inputs() 函数，用于指定内核需要处理的确切输入张量。

任务输出：给定输入，LM 需要输出一个新的派生自 torch.nn.Module() 的类 ModelNew，其中包含自定义优化。例如，LM 可以在 forward() 函数中通过 PyTorch 的 CUDA-C 扩展嵌入内联内核调用。

为了成功，LM 需要识别 (1) Model 类中哪些运算最能从优化中受益，以及 (2) 如何优化这些运算。LM 可以使用任何硬件效率技术（例如融合与分块）、专用指令（例如张量核心）以及任何编程库（例如 PTX、CUDA、CUTLASS、Triton、ThunderKittens）。

### 3.2 任务选择

KernelBench 的 250 个任务依据所含原语运算（即 PyTorch 库函数）的数量划分为三个层级：

- 层级 1（100 个任务）：单一原语运算。该层级包含 AI 的基础构件（例如卷积、矩阵-向量与矩阵-矩阵乘法、损失、激活与层归一化）。

  由于 PyTorch 底层调用若干经过高度优化且往往是闭源的内核，LM 要在这些原语运算上超越基线颇具挑战。但如果某个 LM 成功了，开源内核就可以成为闭源内核（例如 CuBLAS（NVIDIA, 2023））的一个有影响力的替代。

- 层级 2（100 个任务）：算子序列。该层级包含含多个原语运算的 AI 工作负载，这些运算可以融合进单一内核以提升性能（例如卷积、ReLU 与 bias 的组合）。

  由于 PyTorch 编译器这类基于编译器的工具在融合上很有效，LM 要超越它们颇具挑战。不过，LM 可能提出比编译器规则更复杂的算法。

- 层级 3（50 个任务）：完整机器学习架构。该层级包含驱动流行 AI 模型的架构，如 AlexNet 与 MiniGPT，收集自 GitHub 上流行的 PyTorch 仓库。

  鉴于现代模型的规模，在训练与推理时使用内核至关重要。不幸的是，AI 社区一直难以生成高性能内核。例如，从 Transformer 架构（Vaswani et al., 2017）发布到获得高性能内核（Dao et al., 2022）花了 5 年，更遑论如今的众多新架构。这些架构的峰值性能内核所需的算法修改往往超出了编译器的能力范围。

我们再次强调，每个任务都包含一组有意义的 AI 原语运算或架构，因此 LM 在任务上的成功可以直接带来现实世界的影响。

### 3.3 指标设计

我们描述 KernelBench 的评估方法以及如何比较不同 LM 的成功程度。

##### 评估方法

KernelBench 是一个仅用于评估的基准。我们不为任务提供真值（ground truth）内核，因为我们设想用户会在多种硬件平台（包括新平台）、输入类型与工作负载上进行基准测试。不过，KernelBench 在设计上是可以自动验证的。给定一个任务，我们随机生成规定形状与精度的输入张量，并收集 PyTorch Model 的输出。我们可以按如下方式评估 LM 生成结果是否正确且快速：

1. 正确性
   我们把 Model 的输出与 LM 生成的 ModelNew 的输出进行比较。
   我们对每个问题使用 5 个随机输入进行评估（细节见附录 B）。

2. 性能
   我们通过重复试验比较 Model 与 ModelNew 的实际耗时（wall-clock）执行时间，以排除计时波动的影响。

##### 在 KernelBench 上比较 LM

有些 LM 可能生成少量非常快的正确内核，而另一些 LM 生成大量相当慢的正确内核。在此，我们解释为在 KernelBench 上对 LM 质量排序所提出的统一指标。

为了同时捕捉正确性与性能这两个维度，我们提出一个名为 $\text{fast}_{p}$ 的新指标，定义为既正确又取得大于阈值 $p$ 的加速（计算为 PyTorch 实际耗时与生成内核耗时之比）的任务比例。形式化地：

$$\text{fast}_{p}=\frac{1}{N}\sum_{i=1}^{N}\mathbbm{1}(\text{correct}_{i}\land\{\text{speedup}_{i}>p\})$$

其中 $\text{fast}_{0}$ 等价于 LM 的正确率，因为它衡量的是无论速度如何、LM 代码在功能上正确的任务比例。

通过调整阈值参数 $p$，我们可以在不同加速阈值下评估内核性能并捕捉加速分布。在我们的评估中，我们以 $p=1$ 为起点，并随着未来内核生成方法的改进而可能提高 $p$。此外，在训练中使用 $p<1$ 是有价值的，因为 PyTorch 依赖复杂的优化内核，即便只匹敌其一部分性能也被认为是有益的。

## 4 KernelBench 基线评估

在本节中，我们研究一系列 LM 在 KernelBench 上开箱即用的表现，并探索它们的能力与失败模式。

### 4.1 单次尝试基线

我们使用一个包含一对 PyTorch Model 输入与 ModelNew 输出示例的提示来评估 LM，以突出任务格式。该示例很简单，只包含一个 add 算子（见附录 C.1）。给定这一上下文示例与待优化的 PyTorch 任务 Model，LM 通过贪心解码生成 ModelNew。我们在 NVIDIA L40S GPU 上剖析生成的代码，并在所有问题上测量 $\text{fast}_{p}$ 指标。图 2 显示，LM 生成的内核平均在不到 20% 的任务上相对 PyTorch Eager 取得加速。

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| $\text{fast}_{1}$ 相对于： | PyTorch Eager |  |  | torch.compile |  |  |
| KernelBench 层级 | 1 | 2 | 3 | 1 | 2 | 3 |
| GPT-4o | 4% | 5% | 0% | 18% | 4% | 4% |
| OpenAI o1 | 10% | 24% | 12% | 28% | 19% | 4% |
| DeepSeek V3 | 6% | 4% | 8% | 20% | 2% | 2% |
| DeepSeek R1 | 12% | 36% | 2% | 38% | 37% | 2% |
| Claude 3.5 Sonnet | 10% | 7% | 2% | 29% | 2% | 2% |
| Llama 3.1-70B Inst. | 3% | 0% | 0% | 11% | 0% | 0% |
| Llama 3.1-405B Inst. | 3% | 0% | 2% | 16% | 0% | 0% |

图 2：KernelBench 对当前 LM 而言是一个颇具挑战的基准。这里我们展示 $\text{fast}_{1}$，即模型生成的内核在 NVIDIA L40S 上快于 PyTorch Eager 与 torch.compile 基线（默认配置）的问题百分比。

![Refer to caption](2502.10517v1/figures/error_breakdown.png)

图 3：我们把内核代码的失败模式分为执行失败与功能正确性两类。在单次尝试基线中，推理模型生成有执行失败的内核更少，但所有模型在功能正确性上的挣扎程度相似。

注：torch.compile 基线的运行时间有时会比 Torch Eager 慢——这是由可复现的运行时开销（非编译时间）导致的，对层级 1 的小内核而言可能很显著。我们在后续分析中聚焦于 PyTorch Eager，其他基线详见附录 B。

### 4.2 正确性：错误分析

在图 3 中，我们分析了 LM 在各问题上的失败模式。可以看出，很大一部分模型生成的内核是不正确的。为了更好地理解模型生成的内核在哪里失败，我们将其正确性问题分解为执行失败（CUDA/nvcc/Python 编译期错误、CUDA 内存违规与运行时错误）与正确性错误（输出张量的形状与数值不匹配）。我们观察到，推理型 LM（o1、R1）产出错误解的比例（<55%）低于其他模型（>70%）。然而，我们发现这主要是因为它们的执行失败更少。所有 LM 在功能正确性上的挣扎程度相似。

### 4.3 性能：加速分布

一个关键关注点是功能正确的 LM 生成内核能否胜过 PyTorch 基线。图 4 展示了 $\text{fast}_{p}$ 随 $p$ 变化的分布，指示快于 PyTorch Eager 基线 $p$ 倍的内核百分比（图中右上方向更好）。在 $p=1$ 时，所有 KernelBench 层级上 LM 生成的内核胜过 PyTorch 的都不到 15%。推理型 LM 在提供加速方面总体上优于其他 LM。

![Refer to caption](2502.10517v1/figures/greedy_fastp.png)

图 4：大多数 LM 生成的内核都很慢。此图展示 $\text{fast}_{p}$ 指标随加速阈值 $p$（相对 PyTorch 基线）增大时的分布。$\text{fast}_{0}$ 表示无论速度如何的正确内核数量，$\text{fast}_{1}$ 表示取得至少 >1× 于 PyTorch 加速的正确内核数量。提高阈值 $p$ 会增加难度。

### 4.4 跨硬件的性能差异

我们的单次尝试基线不对底层硬件做任何假设，因此一个自然的问题是：我们对 LM 生成内核的分析能否推广到各种 GPU 类型。表 13 与图 9 显示，在 NVIDIA L40S 上层级 1 中胜过 PyTorch Eager 的内核，在其他 GPU 上相对基线也取得相近的加速。然而在层级 2 的问题上，LM 在不同 GPU 间的加速差异更大（图 10）：DeepSeek R1 生成的内核在层级 2 上于 NVIDIA L40S 取得 36% 的 $\text{fast}_{1}$，而在 NVIDIA A10G 上为 47%。这表明单次尝试的 LM 生成内核可能无法很好地跨硬件泛化。为了生成针对特定目标的内核，我们在第 5.2 节探索在上下文中提供硬件特定细节是否有帮助。

我们的分析揭示，当今最好的模型也难以生成胜过基线 PyTorch 速度的正确内核。LM 生成的内核经常因简单的编译器与运行时错误而失败。此外，仅凭简单的指令，LM 很难编写在多种硬件平台上都表现良好的内核。

## 5 模型能力分析

在上一节中，我们发现 KernelBench 对当今的模型而言是一个颇具挑战的基准。在本节中，我们通过案例研究来探索未来模型与 AI 系统的改进机会。

### 5.1 案例研究：在测试时利用 KernelBench 环境反馈

如第 4.2 节所观察到的，执行失败是 LM 生成内核中最频繁的失败模式。KernelBench 提供的环境允许我们收集丰富的信号，包括编译器错误、正确性检查与运行时剖析指标，所有这些都可以回喂给 LM 以帮助其解决内核失败。为探索 LM 能多好地利用这些反馈，我们评估并比较两个基线：(1) 对每个 KernelBench 任务从 LM 生成多个并行样本；(2) 对每个 KernelBench 任务顺序生成内核，允许 LM 利用执行反馈迭代改进。

#### 5.1.1 重复采样

KernelBench 环境支持对 LM 生成内核的程序化验证，使我们能够为每个任务收集并评估多个 LM 生成结果（Brown et al., 2024；Li et al., 2022；Grubisic et al., 2024）。我们使用 $\text{fast}_{p}@k$ 评估这一重复采样方法，它衡量在抽取 $k$ 个样本时，模型至少生成了一个功能正确且快于 PyTorch Eager $p$ 倍的内核的任务百分比。

重复采样帮助 LM 发现更多快速且正确的解。图 5 显示，对 DeepSeek-V3 与 Llama 3.1 70B，高温重复采样在所有三个层级上都随 $k$ 增加而提升 $\text{fast}_{1}$。值得注意的是，在层级 2 上，DeepSeek-V3 以 $k=100$ 个样本达到 37% 的 $\text{fast}_{1}$，而单次尝试基线仅为 4%。检视这些样本，我们发现高温采样有助于探索解空间，提高生成带有更优优化的无错内核的机会。然而，如果模型求解某任务的固有概率非常低，单纯增加采样预算的影响有限。例如，DeepSeek-V3 始终无法为层级 1 中一组 34 个卷积变体生成任何正确解，即便尝试 100 个样本也无济于事。

  

![Refer to caption](2502.10517v1/figures/monkey_fast1.png)

图 5：重复采样帮助发现更多正确且高性能的内核。随着重复样本数 $k$ 增加（最多 100），我们观察到 DeepSeek-V3 与 Llama 3.1-70B Instruct 在所有 3 个 KernelBench 层级上 $\text{fast}_{1}@k$ 均有提升。我们还观察到层级 2 内核的正确解数量增幅更大。

#### 5.1.2 生成结果的迭代改进

KernelBench 环境非常适合收集编译器反馈、执行错误以及用 PyTorch profiler 等工具做的计时分析作为真值信号。我们研究利用这些反馈能否帮助 LM 迭代改进其生成结果。

![Refer to caption](2502.10517v1/figures/multi-turn-workflow.png)

图 6：KernelBench 框架使模型能够在迭代改进期间接收并利用反馈。这些真值信号包括 NVCC 编译器错误信息、执行统计（例如正确性检查与实际耗时）以及 PyTorch profiler（算子计时分解）。

我们在一个多轮过程中，在每次生成后向模型提供反馈：初始生成之后，我们向模型提供其上一轮生成 $G$，以及针对当前生成结果的编译器/执行反馈 $E$ 和/或剖析器输出 $P$。我们把每次生成及随后的反馈定义为一轮，并让这一迭代改进过程运行 $N$ 轮。对每轮，我们测量 $\text{fast}_{p}@N$，即到第 $N$ 轮时模型至少生成了一个功能正确且快于 PyTorch Eager $p$ 倍的内核的任务百分比。

利用执行反馈有助于随时间减少错误并提升总体加速。我们考察第 $N=10$ 轮时的 $\text{fast}_{1}$ 行为（表 1），发现迭代改进在所有模型与 KernelBench 层级上一致地提升性能。DeepSeek-R1 在层级 2 上的改进最为显著：执行反馈 $E$ 与剖析器反馈 $P$ 的组合把 $\text{fast}_{1}$ 从 36% 提升到 72%（见图 7）。

此外，通过考察迭代改进轨迹，我们发现模型在执行反馈 $E$ 下能更有效地自我纠正，尤其是修复与执行错误相关的问题。DeepSeek-R1 在层级 1 和 2 上可以在 10 轮改进内在 >90% 的任务上生成一个可运行的内核（表 8）。然而，其余错误内核几乎总是因为功能不正确而失败，这可能是因为正确性反馈不如执行失败信息那样细粒度。我们在附录 D.4 中给出迭代改进轨迹的成功与失败示例。

![Refer to caption](2502.10517v1/figures/multi-turn-trend-by-k.png)

图 7：借助执行反馈 $E$ 与剖析信息 $P$ 的迭代改进使模型能够随轮次改进内核生成，如图中 DeepSeek-R1 在层级 2 上的 $\text{fast}_{1}@N$ 轨迹所示。到第 $N$ 轮为止最佳生成内核正确且快于 PyTorch Eager 的问题百分比随轮次一致增加。

#### 5.1.3 比较重复采样与迭代改进

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 方法 | 层级 1 |  |  | 层级 2 |  |  | 层级 3 |  |  |
|  | Llama-3.1 70B | DeepSeek V3 | Deepseek R1 | Llama-3.1 70B | Deepseek V3 | Deepseek R1 | Llama-3.1 70B | Deepseek V3 | Deepseek R1 |
| 单次尝试（基线） | 3% | 6% | 12% | 0% | 4% | 36% | 0% | 8% | 2% |
| 重复采样（@10） | 5% | 11% | N/A | 3% | 14% | N/A | 1% | 14% | N/A |
| 迭代改进（w G） | 9% | 9% | 18% | 0% | 7% | 44% | 0% | 14% | 4% |
| 迭代改进（w G+E） | 5% | 13% | 41% | 5% | 5% | 62% | 8% | 22% | 12% |
| 迭代改进（w G+E+P） | 7% | 19% | 43% | 4% | 6% | 72% | 2% | 14% | 18% |

表 1：与基线相比，重复采样与迭代改进都使模型能生成更多正确且快速的内核：这里我们展示两种测试时方法下 LM 生成内核正确且快于基线 Torch Eager 的问题百分比（$\text{Fast}_{1}$，%），两者使用相同的 10 次调用样本预算。我们进一步比较迭代改进中分别利用先前生成 $G$、执行结果 $E$ 与计时剖析 $P$ 所取得的性能。注意我们没有对 DeepSeek R1 做重复采样，因为其 API 端点不提供温度参数。

在表 1 中，我们在固定的 10 次推理调用预算下比较重复采样与迭代改进。两种方法相对单次尝试基线都提供了有意义的改进，其中迭代改进在 6 种情形中的 5 种里更有效。然而，最终我们发现测试时方法的有效性本质上取决于基座模型的质量。例如，在重复采样下，DeepSeek-V3 在所有三个层级上都一致胜过 Llama-3.1 70B。类似地，在迭代改进下，DeepSeek-R1 能持续借助反馈 $E$ 与 $P$ 改进，而 DeepSeek-V3 与 Llama-3.1 70B 并不总能从这些信息中受益。

### 5.2 案例研究：借助硬件知识生成硬件高效内核

显然，LM 在生成硬件高效内核上的成功有限。这可能是因为训练数据中内核代码稀缺，以及如第 4.4 节所讨论的，最优内核可能需要随硬件平台的特定属性而改变。在本案例研究中，我们探索提供 1) 内核工程最佳实践的上下文示例，以及 2) 上下文中的硬件规格细节。

#### 5.2.1 硬件感知的上下文示例

编写良好的内核往往使用融合、分块、重计算与异步等技术来最大化性能。我们发现第 4 节中评估的大多数单次尝试生成的内核往往没有使用这些技术。在此，我们探索提供显式使用这些技术的上下文示例能否帮助 LM 提升 KernelBench 上的表现。具体而言，我们纳入三个上下文示例：使用算子融合的 GeLU（Hendrycks & Gimpel, 2023）、使用分块的矩阵乘法（Mills, 2024），以及一个展示共享内存 I/O 管理的最小 Flash-Attention（Dao et al., 2022；Kim, 2024）内核。

上下文示例降低了 LM 的整体 $\text{fast}_{1}$ 分数，因为 LM 尝试更激进的优化策略，但导致更多执行失败。使用少样本示例时，OpenAI o1 的生成结果平均比第 4 节基线的生成长 25%。不过，在正确的解中，LM 应用了有趣的优化：我们发现在 KernelBench 层级 1 的 77% 的 GEMM 变体上，o1 应用了分块并相对单次尝试基线提升了速度（不过由于缺少张量核心的利用，仍慢于 PyTorch Eager）。在层级 2 上，o1 在 11 个问题上应用了激进的共享内存 I/O 管理，并能胜过 PyTorch Eager（见附录 F）。

#### 5.2.2 指定硬件信息

如第 4.4 节所讨论的，内核性能因硬件平台而异。例如，FlashAttention-2（Dao, 2024）从 NVIDIA A100 迁移到 H100 GPU 时硬件利用率下降 47%。FlashAttention-3（Shah et al., 2024）是为 H100 编写的完全不同的算法。在本研究中，我们探索 LM 能否利用 (1) 硬件规格，如 GPU 类型（H100、A100 等）、显存大小、带宽、TFLOPS，以及 (2) 硬件知识（例如线程、warp、线程块、流式多处理器的定义），在上下文中生成改进的内核（上下文的更多细节见附录 G）。

模型很少生成针对底层硬件优化的内核，这凸显了未来模型的改进空间。某些世代的 GPU（例如 H100）相较前代引入了各种新的硬件单元与指令。提供硬件信息对 Llama 3.1 70B 或 DeepSeek-V3 的输出没有显著影响。

有趣的是，我们发现 OpenAI o1 与 DeepSeek-R1 生成的内核中有一小部分使用了硬件特定的指令与优化。R1 尝试为约 50% 的层级 1 矩阵乘法问题生成 warp 矩阵乘累加（wmma）指令（图 11），尽管大多数无法通过编译。在功能正确的生成结果中，R1 与 o1 在每个层级上产出 1-3 个比第 4 节基线快 $\geq 2\times$ 的离群值。总体而言，我们发现相比硬件信息，LM 在获得第 5.2.1 节的少样本示例时更善于调整其方法。

## 6 讨论

### 6.1 有趣内核的深入剖析

在此，我们讨论几个出人意料、相对 PyTorch 基线取得显著加速的 LM 生成内核。详细示例见附录 D。

算子融合 GPU 拥有少量快速访问内存与大量慢速访问内存。融合可以通过对已载入快速访问内存的数据执行多个运算，帮助降低慢速访问 I/O 的成本。我们发现 LM 通过把计算融合进单一内核来优化 GELU（2.9 倍）与 Softsign（1.3 倍）算子。LM 生成了一个融合多个基础算子——矩阵乘法与除法、求和、缩放——的内核，取得 2.6 倍加速。总体而言，LM 还留有许多融合机会未被利用。

内存层次结构 高效的内核会显式管理有限的共享内存与寄存器内存的利用。在生成的内核中，我们发现使用 GPU 共享内存的内核——余弦相似度（2.8 倍）与三元组边界损失（2.0 倍）——取得了加速。我们没有发现对张量核心指令的成功使用，而后者对 AI 性能至关重要。

算法优化 内核可能需要算法上的修改才能更好地利用硬件特性。我们发现一个有趣的生成结果针对稠密矩阵与对角矩阵相乘的问题，内核对每一行（或列）做缩放，而不是载入对角矩阵的零元素，相对 PyTorch Eager 取得 13 倍加速。

### 6.2 结论

我们的贡献是：(1) 我们提出 KernelBench，一个为 LM 驱动的内核优化奠定基础的框架；(2) 我们评估了多样的模型与方法，分析其优势与局限，并为改进机会提供了洞见。

总体而言，虽然大多数基准最终会饱和，KernelBench 的设计使其能随着新 AI 工作负载的出现而动态演进。我们的 $\text{fast}_{p}$ 指标可以随时间调整，以衡量相对日益先进基线（即超出本文所用 PyTorch 基线）的加速阈值（$p$）。由于 PyTorch 可跨硬件平台兼容，KernelBench 中基于 PyTorch 的任务可以在每一个新硬件平台发布时进行评估。最后，与许多基准不同，在 KernelBench 上的成功直接对应生产价值与现实影响（大规模降低成本与减少能耗）。这些性质确保 KernelBench 在不断演进的 AI 版图中保持价值。

### 6.3 未来工作的机会

我们表明，鉴于目前可用的模型，KernelBench 上还有很大的改进空间。首先，未来工作可以探索先进的微调与推理技术的开发，包括智能体式工作流。由于 CUDA 是一种低资源语言，未来工作开源更多高质量数据将很有价值。其次，在我们的实验中 LM 生成的是原生 CUDA 代码。然而未来工作可以探索使用替代编程抽象（例如 ThunderKittens、CUTLASS、Triton 等提供的抽象）生成代码能否简化生成问题，例如让 LM 更容易利用张量核心指令。第三，我们的评估到目前为止仅限于 GPU，未来工作可以扩展到其他硬件加速器。

## 伦理声明

优化的 GPU 内核可以为大规模机器学习工作负载带来显著的节能，同时降低计算成本与环境影响。通过提供一个 AI 辅助性能调优的框架，KernelBench 有助于构建更节能的 AI 系统，与减少计算基础设施碳足迹的全球努力相一致。

KernelBench 不涉及人类研究，也不收集用户数据，消除了隐私方面的顾虑。它也避免使用专有或私有代码，仅依赖公开可用的 GitHub 仓库。

## 致谢

我们感谢 Google DeepMind、Google、IBM、Stanford HAI、PrimeIntellect 与 Modal 对本工作的支持。我们感谢 Aaryan Singhal、AJ Root、Allen Nie、Anjiang Wei、Benjamin Spector、Bilal Khan、Bradley Brown、Dylan Patel、Genghan Zhang、Hieu Pham、Hugh Leather、John Yang、Jon Saad-Falcon、Jordan Juravsky、Marcel Rød、Mark Saroufim、Michael Zhang、Minkai Xu、Ryan Ehrlich、Sahan Paliskara、Sahil Jain、Shicheng (George) Liu、Simran Arora、Suhas Kotha、Vikram Sharma Mailthody 与 Yangjun Ruan 在塑造本工作过程中的深入讨论与建设性反馈。

## 参考文献

- [1]

  Apple.
  Apple ml compute framework (mlx), 2020.
  URL <https://developer.apple.com/metal/>.
- [2]

  Simran Arora, Sabri Eyuboglu, Michael Zhang, Aman Timalsina, Silas Alberti, Dylan Zinsley, James Zou, Atri Rudra, and Christopher Ré.
  Simple linear attention language models balance the recall-throughput tradeoff.
  *International Conference on Machine Learning*, 2024.
- [3]

  Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré, and Azalia Mirhoseini.
  Large language monkeys: Scaling inference compute with repeated sampling, 2024.
  URL <https://arxiv.org/abs/2407.21787>.
- [4]

  Cerebras.
  Cerebras wafer-scale engine wse architecture.
  Online.
  <https://cerebras.ai/product-chip/>.
- [5]

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
  Evaluating large language models trained on code, 2021.
  URL <https://arxiv.org/abs/2107.03374>.
- [6]

  Tri Dao.
  FlashAttention-2: Faster attention with better parallelism and work partitioning.
  *International Conference on Learning Representations*, 2024.
- [7]

  Tri Dao and Albert Gu.
  Transformers are ssms: Generalized models and efficient algorithms through structured state space duality.
  *International Conference on Machine Learning (ICML)*, 2024.
- [8]

  Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré.
  FlashAttention: Fast and memory-efficient exact attention with IO-awareness.
  In *Advances in Neural Information Processing Systems*, 2022.
- [9]

  DeepSeek-AI.
  Deepseek-v3 technical report, 2025.
  URL <https://github.com/deepseek-ai/DeepSeek-V3>.
- [10]

  Graphcore.
  Graphcore IPU architecture.
  Online.
  <https://www.graphcore.ai/products/ipu>.
- [11]

  Groq.
  Groq architecture.
  Online.
  <https://groq.com/>.
- [12]

  Dejan Grubisic, Chris Cummins, Volker Seeker, and Hugh Leather.
  Priority sampling of large language models for compilers, 2024.
  URL <https://arxiv.org/abs/2402.18734>.
- [13]

  Dan Hendrycks and Kevin Gimpel.
  Gaussian error linear units (gelus), 2023.
  URL <https://arxiv.org/abs/1606.08415>.
- [14]

  Norman P. Jouppi, George Kurian, Sheng Li, Peter Ma, Rahul Nagarajan, Lifeng Nai, Nishant Patil, Suvinay Subramanian, Andy Swing, Brian Towles, Cliff Young, Xiang Zhou, Zongwei Zhou, and David Patterson.
  Tpu v4: An optically reconfigurable supercomputer for machine learning with hardware support for embeddings, 2023.
  URL <https://arxiv.org/abs/2304.01433>.
- [15]

  Peter Kim.
  Flashattention minimal.
  Online, 2024.
  <https://github.com/tspeterkim/flash-attention-minimal>.
- [16]

  Denis Kocetkov, Raymond Li, Loubna Ben Allal, Jia Li, Chenghao Mou, Carlos Muñoz Ferrandis, Yacine Jernite, Margaret Mitchell, Sean Hughes, Thomas Wolf, Dzmitry Bahdanau, Leandro von Werra, and Harm de Vries.
  The stack: 3 tb of permissively licensed source code, 2022.
  URL <https://arxiv.org/abs/2211.15533>.
- [17]

  Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang, Ruiqi Zhong, Luke Zettlemoyer, Scott Wen tau Yih, Daniel Fried, Sida Wang, and Tao Yu.
  Ds-1000: A natural and reliable benchmark for data science code generation, 2022.
  URL <https://arxiv.org/abs/2211.11501>.
- [18]

  Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennikoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue Zhuo, Thomas Wang, Olivier Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro, Oleh Shliazhko, Nicolas Gontier, Nicholas Meade, Armel Zebaze, Ming-Ho Yee, Logesh Kumar Umapathi, Jian Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy, Jason Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey, Zhihan Zhang, Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu, Swayam Singh, Sasha Luccioni, Paulo Villegas, Maxim Kunakov, Fedor Zhdanov, Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire Schlesinger, Hailey Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson, Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried, Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf, Arjun Guha, Leandro von
  Werra, and Harm de Vries.
  Starcoder: may the source be with you!, 2023.
  URL <https://arxiv.org/abs/2305.06161>.
- [19]

  Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittweser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
  Competition-level code generation with alphacode.
  *Science*, 378(6624):1092–1097, December 2022.
  ISSN 1095-9203.
  doi: 10.1126/science.abq1158.
  URL <http://dx.doi.org/10.1126/science.abq1158>.
- [20]

  Christian J. Mills.
  Cuda mode notes - lecture 004.
  Online, 2024.
  <https://christianjmills.com/posts/cuda-mode-notes/lecture-004/>.
- [21]

  Daniel Nichols, Pranav Polasam, Harshitha Menon, Aniruddha Marathe, Todd Gamblin, and Abhinav Bhatele.
  Performance-aligned llms for generating fast code, 2024.
  URL <https://arxiv.org/abs/2404.18864>.
- [22]

  NVIDIA.
  cudnn: Gpu-accelerated library for deep neural networks, 2014.
  URL <https://developer.nvidia.com/cudnn>.
- [23]

  NVIDIA.
  Cuda templates for linear algebra subroutines, 2017a.
  URL <https://github.com/NVIDIA/cutlass>.
- [24]

  NVIDIA.
  Nvidia Tesla V100 GPU architecture, 2017b.
- [25]

  NVIDIA.
  Nvidia A100 tensor core GPU architecture, 2020.
- [26]

  NVIDIA.
  Nvidia H100 tensor core GPU architecture, 2022.
- [27]

  NVIDIA.
  cuBLAS, 2023.
  URL <https://docs.nvidia.com/cuda/cublas/>.
- [28]

  Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Yang, Zach DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala.
  Pytorch: An imperative style, high-performance deep learning library, 2019.
  URL <https://arxiv.org/abs/1912.01703>.
- [29]

  Bo Peng, Eric Alcaide, Quentin Anthony, Alon Albalak, Samuel Arcadinho, Huanqi Cao, Xin Cheng, Michael Chung, Matteo Grella, Kranthi Kiran GV, Xuzheng He, Haowen Hou, Przemyslaw Kazienko, Jan Kocon, and Jiaming et al. Kong.
  Rwkv: Reinventing rnns for the transformer era.
  *Findings of the Association for Computational Linguistics: EMNLP 2023*, 2023.
- [30]

  Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri Dao.
  Flashattention-3: Fast and accurate attention with asynchrony and low-precision, 2024.
  URL <https://arxiv.org/abs/2407.08608>.
- [31]

  Quan Shi, Michael Tang, Karthik Narasimhan, and Shunyu Yao.
  Can language models solve olympiad programming?, 2024.
  URL <https://arxiv.org/abs/2404.10952>.
- [32]

  Benjamin Spector, Simran Arora, Aaryan Singhal, Daniel Fu, and Christopher Ré.
  Thunderkittens: Simple, fast, and adorable ai kernels.
  *International Conference on Learning Representations (ICLR)*, 2024.
- [33]

  Yi Tay, Mostafa Dehghani, Dara Bahri, and Donald Metzler.
  Efficient transformers: A survey.
  *ACM Computing Surveys*, 55(6):1–28, 2022.
- [34]

  Team PyTorch, Horace He, Driss Guessous, Yanbo Liang, and Joy Dong.
  FlexAttention: The flexibility of PyTorch with the performance of FlashAttention, 2024.
  URL <https://pytorch.org/blog/flexattention/>.
- [35]

  Ali TehraniJamsaz, Arijit Bhattacharjee, Le Chen, Nesreen K. Ahmed, Amir Yazdanbakhsh, and Ali Jannesari.
  Coderosetta: Pushing the boundaries of unsupervised code translation for parallel programming.
  In *The Thirty-eighth Annual Conference on Neural Information Processing Systems*, 2024.
  URL <https://openreview.net/forum?id=V6hrg4O9gg>.
- [36]

  Philippe Tillet, H. T. Kung, and David Cox.
  Triton: an intermediate language and compiler for tiled neural network computations.
  In *Proceedings of the 3rd ACM SIGPLAN International Workshop on Machine Learning and Programming Languages*, 2019.
- [37]

  Alan M. Turing.
  On computable numbers, with an application to the Entscheidungsproblem.
  *Proceedings of the London Mathematical Society*, 2(42):230–265, 1936.
  URL <http://www.cs.helsinki.fi/u/gionis/cc05/OnComputableNumbers.pdf>.
- [38]

  Pedro Valero-Lara, Alexis Huante, Mustafa Al Lail, William F. Godoy, Keita Teranishi, Prasanna Balaprakash, and Jeffrey S. Vetter.
  Comparing llama-2 and gpt-3 llms for hpc kernels generation, 2023.
  URL <https://arxiv.org/abs/2309.07103>.
- [39]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  *31st Conference on Neural Information Processing Systems (NIPS 2017)*, 2017.
- [40]

  Siddhant Waghjale, Vishruth Veerendranath, Zhiruo Wang, and Daniel Fried.
  ECCO: Can we improve model-generated code efficiency without sacrificing functional correctness?
  In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen (eds.), *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, pp. 15362–15376, Miami, Florida, USA, November 2024. Association for Computational Linguistics.
  doi: 10.18653/v1/2024.emnlp-main.859.
  URL <https://aclanthology.org/2024.emnlp-main.859/>.
- [41]

  Yuanbo Wen, Qi Guo, Qiang Fu, Xiaqing Li, Jianxing Xu, Yanlin Tang, Yongwei Zhao, Xing Hu, Zidong Du, Ling Li, Chao Wang, Xuehai Zhou, and Yunji Chen.
  BabelTower: Learning to auto-parallelized program translation.
  In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato (eds.), *Proceedings of the 39th International Conference on Machine Learning*, volume 162 of *Proceedings of Machine Learning Research*, pp. 23685–23700. PMLR, 17–23 Jul 2022.
  URL <https://proceedings.mlr.press/v162/wen22b.html>.
- [42]

  Hjalmar Wijk, Tao Lin, Joel Becker, Sami Jawhar, Neev Parikh, Thomas Broadley, Lawrence Chan, Michael Chen, Josh Clymer, Jai Dhyani, Elena Ericheva, Katharyn Garcia, Brian Goodrich, Nikola Jurkovic, Megan Kinniment, Aron Lajko, Seraphina Nix, Lucas Sato, William Saunders, Maksym Taran, Ben West, and Elizabeth Barnes.
  Re-bench: Evaluating frontier ai r&d capabilities of language model agents against human experts, 2024.
  URL <https://arxiv.org/abs/2411.15114>.
- [43]

  John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press.
  Swe-agent: Agent-computer interfaces enable automated software engineering.
  *arXiv:2405.15793*, 2024a.
- [44]

  John Yang, Carlos E. Jimenez, Alex L. Zhang, Kilian Lieret, Joyce Yang, Xindi Wu, Ori Press, Niklas Muennikoff, Gabriel Synnaeve, Karthik R. Narasimhan, Diyi Yang, Sida I. Wang, and Ofir Press.
  Swe-bench multimodal: Do ai systems generalize to visual software domains?, 2024b.
  URL <https://arxiv.org/abs/2410.03859>.
- [45]

  Songlin Yang and Yu Zhang.
  Fla: A triton-based library for hardware-efficient implementations of linear attention mechanism, January 2024.
  URL <https://github.com/sustcsonglin/flash-linear-attention>.
- [46]

  Pengcheng Yin, Wen-Ding Li, Kefan Xiao, Abhishek Rao, Yeming Wen, Kensen Shi, Joshua Howland, Paige Bailey, Michele Catasta, Henryk Michalewski, Alex Polozov, and Charles Sutton.
  Natural language to code generation in interactive data science notebooks, 2022.
  URL <https://arxiv.org/abs/2212.09248>.

## 附录 A KernelBench 任务示例

这里我们给出 KernelBench 的一个示例任务。每个任务包装在一个名为 Model 的类中。任务在 Model 类中包含两个关键函数 __init__ 与 forward；必要时还会包含辅助函数。我们固定输入的形状，并通过随机生成的张量改变数值。我们提供 get_inputs 与 get_init_inputs 两个函数，分别用于生成初始化模型和执行前向传播所需的随机参数。

PyTorch 参考架构：

```python
import torch
import torch.nn as nn

class Model(nn.Module):
    """
    Simple model that performs a single matrix multiplication (C = A * B) with a large K dimension
    """
    def __init__(self):
        super(Model, self).__init__()

    def forward(self, A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
        """
        Performs matrix multiplication of A and B.

        Args:
            A: Input tensor of shape (M, K)
            B: Input tensor of shape (K, N)

        Returns:
            Output tensor of shape (M, N)
        """
        return torch.matmul(A, B)

M = 256
N = 256
K = 131072

def get_inputs():
    A = torch.randn(M, K)
    B = torch.randn(K, N)
    return [A, B]

def get_init_inputs():
    return [] # No special initialization inputs needed
```

下面我们给出一个模型的示例输出，它试图优化上述任务规格。模型不仅负责生成内核代码，还负责生成把内核集成进 PyTorch 框架的外围代码。评估框架会像对待一个 PyTorch 算子那样运行该模型的前向传播，因此一种常见做法是内联 CUDA 代码。

```python
import torch
import torch.nn as nn
from torch.utils.cpp_extension import load_inline

# Define the custom CUDA kernel for matrix multiplication
matmul_source = """
#include <torch/extension.h>
#include <cuda_runtime.h>

__global__ void matmul_kernel(const float* A, const float* B, float* C, int M, int N, int K) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < M && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < K; ++k) {
            sum += A[row * K + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

torch::Tensor matmul_cuda(torch::Tensor A, torch::Tensor B) {
    int M = A.size(0);
    int N = B.size(1);
    int K = A.size(1);

    auto C = torch::zeros({M, N}, A.options());

    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks((N + threadsPerBlock.x - 1) / threadsPerBlock.x, (M + threadsPerBlock.y - 1) / threadsPerBlock.y);

    matmul_kernel<<<numBlocks, threadsPerBlock>>>(A.data_ptr<float>(), B.data_ptr<float>(), C.data_ptr<float>(), M, N, K);

    return C;
}
"""

matmul_cpp_source = (
    "torch::Tensor matmul_cuda(torch::Tensor A, torch::Tensor B);"
)

# Compile the inline CUDA code for matrix multiplication
matmul = load_inline(
    name="matmul",
    cpp_sources=matmul_cpp_source,
    cuda_sources=matmul_source,
    functions=["matmul_cuda"],
    verbose=True,
    extra_cflags=[""],
    extra_ldflags=[""],
)


class ModelNew(nn.Module):
    def __init__(self):
        super(ModelNew, self).__init__()
        self.matmul = matmul

    def forward(self, A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
        return self.matmul.matmul_cuda(A, B)
```

## 附录 B 评估方法与基线

除非另有说明（例如第 4.4 节的设备泛化实验与第 5.2 节的硬件案例研究），所有评估都在一块 Ada Lovelace 架构的裸金属 NVIDIA L40S GPU 上进行。该 NVIDIA L40S 拥有 48 GB HBM 显存，功率 300W。我们的环境使用 Python 3.10、PyTorch 2.5.0+cu124 与 CUDA 12.4，我们的 PyTorch Eager 与 torch.compile 基线也来源于此。

### B.1 内核评估设置

回顾 KernelBench 任务包含作为基线的 PyTorch 参考模块 Model，以及模型生成的带自定义内联 CUDA 内核的 PyTorch 架构 ModelNew。

在正确性方面，我们把 num_correctness 设为 5，即用 5 组随机化输入检查参考架构 Model 与带自定义内核的生成架构 ModelNew 之间输出的等价性。我们在附录 B.2 中详述这一选择的原因。

在性能方面，我们测量 Model 与 ModelNew 二者 nn.module.forward 的实际耗时执行时间。我们确保当前 GPU 上只评估一个内核（没有其他 CUDA 进程）。我们先预热 3 次迭代，然后把 num_profile 设为 100 次，测量 CUDA 事件 torch.cuda.Event 之间标记的执行耗时。我们取 100 次试验的均值，并同时记录其最大值、最小值与标准差。虽然每次试验的实际耗时可能波动，但我们注意到变异系数（CV）：$\text{std}/\text{mean}$ 始终 <3%，因此我们用两次测量到的实际耗时的均值做比较。

为计算生成架构相对基线架构在单个问题上的加速，我们对两者都使用均值：$\text{speedup}=T_{Model}/T_{ModelNew}$。例如，若 $T_{Model}=2$ ms 且 $T_{ModelNew}=1$ ms，则新生成的内核带来 2 倍加速。我们把这个加速与加速阈值参数 $p$（如第 3.3 节所述）比较以计算 $\text{fast}_{p}$ 分数。

### B.2 改变随机生成输入数量下的正确性分析

从形式意义上检查程序等价性是不可判定的。「停机问题」（Turing, 1936）表明，一般而言不可能判定一个给定程序是否对所有可能输入都会终止。这一问题自然延伸到等价性检查，因为要检查两个程序是否等价，必须检查它们在所有输入上的行为，包括其中一个或两个程序可能不终止的情形。由于判定一个程序在给定输入上是否停机是不可判定的（停机问题），检查等价性也随之不可判定。

实践中常用近似或启发式方法检查程序等价性。随机测试是最常见的实用做法：用多组随机选取的输入运行程序，并比较其输出。随机测试对 AI 内核尤其有效，因为其控制流较简单，关注点主要在数值正确性。通过使用多样的输入，它能以较高概率揭示计算或内存处理中的错误。更系统地评估正确性——尤其是在存在微妙硬件特定行为的情形下——是一个有待进一步探索的方向。未来工作可以研究形式化验证工具，以提供更强的等价性保证。

我们使用五组随机输入做正确性检查，这在发现错误的能力与效率之间是一个不错的折中。在一项包含 100 个生成内核的实验中，结果如下：50 个内核正确（全部 5/5 与 100/100），19 个输出数值不匹配（19 个 0/5 与 0/100），4 个输出形状不匹配，10 个遇到运行时错误，17 个有编译错误。值得注意的是，0/5 与 0/100 的失败表明没有观察到部分正确的情形。

### B.3 单次尝试基线的模型表现分布

这里我们考察（功能正确的）内核生成结果在众多模型上的质量。图 8 展示了不同层级与模型下各内核加速的分布。层级 1 与层级 3 的加速中位数都小于 1，层级 2 的加速中位数仅略高于 1。层级 1 的离群值最显著，其中一个案例的加速大于 10。我们在第 6 节中更详细地探讨了其中一些离群案例。

推理优化模型（OpenAI-o1 与 DeepSeek-R1）在所有层级上开箱即用的表现最佳。这些模型展现了卓越的内核生成能力，尤其在层级 2 任务（主要涉及内核融合）上表现出色。相比之下，Llama 3.1 模型（405B 与 70B 皆是）无论模型大小如何表现都很差，表明更大的模型并不必然在此任务上带来更好的结果。DeepSeek-R1 虽然在层级 1 和 2 上很强，但在层级 3 上严重受挫，经常生成错误的内核。

![Refer to caption](2502.10517v1/figures/greedy_speedup_box_whiskers.png)

图 8：单次尝试基线设置下各模型生成的（正确）内核相对 Torch Eager 加速的箱线图。我们还在模型名旁标注了正确生成内核的百分比。我们观察到，在大多数模型中，正确生成内核的加速中位数低于 1。

### B.4 PyTorch 基线

PyTorch 提供两种常见执行模式：Eager 与 torch.compile。除了图 2 所示的结果外，所有性能分析都相对 PyTorch Eager 评估。

PyTorch Eager 是 PyTorch 的默认执行模式，通过调用高度优化的闭源内核来动态执行计算。

PyTorch Compile（torch.compile）在初始编译阶段对底层计算图使用基于规则的启发式，并调用多种后端执行内核融合与图变换等优化。在图 2 中，我们 torch.compile 的性能基线采用默认配置（PyTorch Inductor 的 default 模式）。此外，我们在计时分析中排除 torch.compile 的编译时间，因为我们只关注纯运行时行为。torch.compile 还有多种其他后端与配置，我们在表 2 中描述。

我们观察到，在 KernelBench 参考问题的层级 2 和 3 上，torch.compile 基线的运行时间通常快于 PyTorch Eager，主要得益于算子融合等图级优化的可用性。然而在层级 1 问题上，torch.compile 的运行时间可能高于 PyTorch Eager，这可归因于 torch.compile 经验上可复现的运行时开销（非编译时间），它对小内核而言可能很显著。

|  |  |  |  |
| --- | --- | --- | --- |
| 配置 | 后端 | 模式 | 描述 |
| PyTorch（Eager） | - | - | 标准 PyTorch eager 执行 |
| Torch Compile | inductor | default | 默认 torch.compile 行为 |
| Torch Compile | inductor | reduce-overhead | 针对降低开销优化 |
| Torch Compile | inductor | max-autotune | 启用最大自动调优 |
| Torch Compile | inductor | max-autotune-no-cudagraphs | 不使用 CUDA 图的最大自动调优 |
| Torch Compile | cudagraphs | - | 带 AOT Autograd 的 CUDA 图 |

表 2：PyTorch 执行与优化后端的配置与模式。

其他 torch.compile 后端。在表 3 中，我们展示相对其他一些 torch.compile 基线的更多 $\text{fast}_{1}$ 单次尝试基线结果。我们注意到，在一些其他配置上 $\text{fast}_{1}$ 有所下降，层级 2 尤其明显，因为 torch.compile 后端应用了更激进的优化（以额外的编译时间开销为代价，而我们不测量这部分）。由于 torch.compile 在不同配置间表现多变，我们把分析聚焦于 PyTorch Eager。

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\text{fast}_{1}$ 相对于： | torch.compile default |  |  | cudagraphs |  |  | max-autotune |  |  | max-autotune no-cudagraphs |  |  | reduce-overhead |  |  |
| KernelBench 层级 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 |
| Claude 3.5 Sonnet | 29% | 2% | 2% | 31% | 7% | 2% | 31% | 2% | 0% | 29% | 2% | 2% | 31% | 2% | 0% |
| DeepSeek V3 | 20% | 2% | 2% | 21% | 4% | 20% | 21% | 2% | 2% | 20% | 2% | 2% | 21% | 2% | 0% |
| DeepSeek R1 | 38% | 37% | 2% | 42% | 52% | 0% | 42% | 29% | 0% | 38% | 32% | 4% | 42% | 28% | 0% |
| GPT-4o | 18% | 4% | 4% | 22% | 6% | 6% | 21% | 4% | 2% | 18% | 3% | 4% | 21% | 4% | 0% |
| Llama 3.1-70B Inst. | 11% | 0% | 0% | 12% | 0% | 0% | 12% | 0% | 0% | 11% | 0% | 0% | 12% | 0% | 0% |
| Llama 3.1-405B Inst. | 16% | 0% | 0% | 16% | 0% | 4% | 16% | 0% | 0% | 16% | 0% | 0% | 16% | 0% | 0% |
| OpenAI O1 | 28% | 19% | 4% | 33% | 37% | 26% | 34% | 8% | 4% | 30% | 19% | 6% | 34% | 8% | 2% |

表 3：除图 2 所示结果外，我们比较 KernelBench torch.compile 基线在各种配置下的运行时间，全部在 NVIDIA L40S 上测量。

## 附录 C 实验提示细节

我们提供第 4 节与第 5 节所用提示策略及相关采样策略的细节。

### C.1 单次尝试基线提示

对于第 4.1 节所示的单次尝试基线，我们希望在确保指令与输出格式清晰的同时，提供最少量的信息，以考察每个模型开箱即用的内核生成能力。我们用以下提示以及一对上下文 add 示例（PyTorch 参考的 add 与使用内联编译的 CUDA 内核对应实现）查询每个模型，以提供输出格式。我们用贪心解码采样模型以确保输出确定，即设置 temperature=0。

```text
You write custom CUDA kernels to replace the pytorch operators in the given architecture
to get speedups.

You have complete freedom to choose the set of operators you want to replace. You may
make the decision to replace some operators with custom CUDA kernels and leave others
unchanged. You may replace multiple operators with custom implementations, consider
operator fusion opportunities (combining multiple operators into a single kernel, for
example, combining matmul+relu), or algorithmic changes (such as online softmax). You are
only limited by your imagination.

Here’s an example to show you the syntax of inline embedding custom CUDA operators in
torch: The example given architecture is:
‘‘‘
import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
 def __init__(self) -> None:
     super().__init__()

 def forward(self, a, b):
     return a + b


def get_inputs():
 # randomly generate input tensors based on the model architecture
 a = torch.randn(1, 128).cuda()
 b = torch.randn(1, 128).cuda()
 return [a, b]


def get_init_inputs():
 # randomly generate tensors required for initialization based on the model architecture
 return []
‘‘‘

The example new arch with custom CUDA kernels looks like this:
‘‘‘
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.cpp_extension import load_inline

# Define the custom CUDA kernel for element-wise addition
elementwise_add_source = """
#include <torch/extension.h>
#include <cuda_runtime.h>

__global__ void elementwise_add_kernel(const float* a, const float* b, float* out, int size) {
 int idx = blockIdx.x * blockDim.x + threadIdx.x;
 if (idx < size) {
     out[idx] = a[idx] + b[idx];
 }
}

torch::Tensor elementwise_add_cuda(torch::Tensor a, torch::Tensor b) {
 auto size = a.numel();
 auto out = torch::zeros_like(a);

 const int block_size = 256;
 const int num_blocks = (size + block_size - 1) / block_size;

 elementwise_add_kernel<<<num_blocks, block_size>>>(a.data_ptr<float>(), b.data_ptr<float>(), out.data_ptr<float>(), size);

 return out;
}
"""

elementwise_add_cpp_source = "torch::Tensor elementwise_add_cuda(torch::Tensor a, torch::Tensor b);"

# Compile the inline CUDA code for element-wise addition
elementwise_add = load_inline(
 name=’elementwise_add’,
 cpp_sources=elementwise_add_cpp_source,
 cuda_sources=elementwise_add_source,
 functions=[’elementwise_add_cuda’],
 verbose=True,
 extra_cflags=[’’],
 extra_ldflags=[’’]
)

class ModelNew(nn.Module):
 def __init__(self) -> None:
     super().__init__()
     self.elementwise_add = elementwise_add

 def forward(self, a, b):
     return self.elementwise_add.elementwise_add_cuda(a, b)
‘‘‘

You are given the following architecture:

<PyTorch reference architecture for specific KernelBench Problem>

Optimize the architecture named Model with custom CUDA operators! Name your optimized
output architecture ModelNew. Output the new code in codeblocks. Please generate real
code, NOT pseudocode, make sure the code compiles and is fully functional. Just output
the new model code, no other text, and NO testing code!
```

### C.2 重复采样提示

对于重复采样，我们使用与附录 C.1 单次尝试基线相同的提示。我们采用与 Brown et al.（2024）相同的采样温度，因为它们在保证质量的同时允许样本多样性。具体而言，DeepSeek-V3 使用 temperature=1.6，Llama 3.1-70B 使用 temperature=0.7。

### C.3 迭代改进提示

对于迭代改进，我们以附录 C.1 单次尝试基线相同的初始提示开始。我们实验的一个局限是采样时 temperature=0，以便聚焦于基于反馈迭代的效果而非引入随机性。在后续生成中，我们依据期望的反馈类型用以下模板提示模型：

```text
<Initial prompt from one-shot baseline for specific KernelBench problem.>

Here is your latest generation:
<Previously generated kernel G>

Your generated architecture ModelNew and kernel was evaluated on GPU and checked against the reference architecture Model.
Here is your Evaluation Result:

<Raw Compiler and Execution Feedback from stdout>

<’if correct:’>
Your kernel executed successfully and produced the correct output.
Here is your wall clock time: {runtime} milliseconds

<Profiler information if used and correct.>

Name your new improved output architecture ModelNew. Output the new code in codeblocks. Please generate real code, NOT pseudocode, make sure the code compiles and is fully functional. Just output the new model code, no other text, and NO testing code!
```

对于编译器与执行反馈，我们用「Your kernel execution timed out」显式处理超时与死锁，但不提供其他任何信息。

### C.4 少样本上下文提示

对应第 5.2.1 节所述的少样本实验。上下文示例的更多细节见附录 F。这些实验的采样 temperature=0。

```text
<Initial Task prompt from one-shot baseline for Instruction>
<Initial pair of Reference PyTorch and CUDA kernel equiavlent for example add kernel from one-shot baseline for Instruction>

Example <i>
Here is an example architecture
<PyTorch reference architecture for No. i in-context example>

Here is an optimized verison with custom CUDA kernels:
<PyTorch architecture with Custom CUDA Kernel for No. i in-context example>

.. up to number of in-context sample times


Task:
Here is an example architecture:

<PyTorch reference architecture for specific KernelBench Problem>

Name your new improved output architecture ModelNew. Output the new code in codeblocks. Please generate real code, NOT pseudocode, make sure the code compiles and is fully functional. Just output the new model code, no other text, and NO testing code!
```

### C.5 硬件案例研究提示

这里我们提供硬件信息。这用于第 4.4 节并在附录 G 中有更详细的阐述，采样 temperature=0。

```text
<Initial Task prompt from one-shot baseline for Instruction>
<Initial pair of Reference PyTorch and CUDA kernel equiavlent for example add kernel from one-shot baseline for Instruction>

Here is some information about the underlying hardware that you should keep in mind.

The GPU that will run the kernel is NVIDIA <GPU NAME>.

- We have <x> GB GDDR6 with ECC of GPU Memory.
- We have <x> GB/s of Memory Bandwidth.
- We have <x> of RT Core Performance TFLOPS.
- We have <x> of FP32 TFLOPS.
- We have <x> of TF32 Tensor Core TFLOPS.
- We have <x> of FP16 Tensor Core TFLOPS.
- We have <x> of FP8 Tensor Core TFLOPS.
- We have <x> of Peak INT8 Tensor TOPS.
- We have <x> of Peak INT4 Tensor TOPS.
- We have <x> 32-bit registers per SM of Register File Size.
- We have <x> of Maximum number of registers per thread.
- We have <x> of Maximum number of thread blocks per SM.
- We have <x> KB of Shared memory capacity per SM.
- We have <x> KB of Maximum shared memory per thread block.


Here are some concepts about the GPU architecture that could be helpful:

- Thread: A thread is a single execution unit that can run a single instruction at a time.
- Thread Block: A thread block is a group of threads that can cooperate with each other.
- Shared Memory: Shared memory is a memory space that can be accessed by all threads in a thread block.
- Register: A register is a small memory space that can be accessed by a single thread.
- Memory Hierarchy: Memory hierarchy is a pyramid of memory types with different speeds and sizes.
- Memory Bandwidth: Memory bandwidth is the rate at which data can be read from or stored into memory.
- Cache: Cache is a small memory space that stores frequently accessed data.
- HBM: HBM is a high-bandwidth memory technology that uses 3D-stacked DRAM.

Here are some best practices for writing CUDA kernels on GPU

- Find ways to parallelize sequential code.
- Minimize data transfers between the host and the device.
- Adjust kernel launch configuration to maximize device utilization.
- Ensure that global memory accesses are coalesced.
- Minimize redundant accesses to global memory whenever possible.
- Avoid long sequences of diverged execution by threads within the same warp.
 #We added this to reference the specific GPU architecture
- Use specialized instructions based on the specific GPU architecture

You are given the following architecture:

<PyTorch reference architecture for specific KernelBench Problem>

Name your new improved output architecture ModelNew. Output the new code in codeblocks. Please generate real code, NOT pseudocode, make sure the code compiles and is fully functional. Just output the new model code, no other text, and NO testing code!
```

## 附录 D 值得关注的内核

本节我们提供一些有趣或值得注意的内核生成示例。我们首先扩展第 6 节的讨论，那里定义了以下几类优化：算法优化、算子融合与利用硬件特性。

### D.1 算法优化

Claude-3.5 Sonnet 在层级 1 问题 11 上取得 13 倍加速

原始 torch 算子是 torch.diag(A) @ B，将由向量 A 构成的对角矩阵与矩阵 B 相乘。模型识别出对角矩阵乘法这一特例中的优化：无需显式构造对角矩阵，而是把向量 A 的每个元素直接与矩阵 B 的对应行相乘，从而显著提升性能：

```c
__global__ void diag_matmul_kernel(
    const float* diag,
    const float* mat,
    float* out,
    const int N,
    const int M) {

    const int row = blockIdx.y * blockDim.y + threadIdx.y;
    const int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < M) {
        out[row * M + col] = diag[row] * mat[row * M + col];
    }
}
```

### D.2 内核融合

DeepSeek-V3 在层级 1 问题 87 上取得 2.9 倍加速

torch 中的 GeLU 参考：

```python
0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))))
```

优化版本融合进单一内核。还有一处小的常量折叠优化：内核不再重复计算 math.sqrt(2.0 / math.pi)，而是使用预计算值 0.7978845608028654f：

```c
__global__ void gelu_kernel(const float* x, float* out, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        float x_val = x[idx];
        float cdf = 0.5f * (1.0f + tanhf((0.7978845608028654f * (x_val + 0.044715f * x_val * x_val * x_val))));
        out[idx] = x_val * cdf;
    }
}
```

Claude-3.5 Sonnet 在层级 1 问题 29 上取得 1.3 倍加速

torch 中的 SoftSign 参考：

```python
x / (1 + torch.abs(x))
```

融合内核：

```c
__global__ void softsign_kernel(const float* input, float* output, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < size) {
        float x = input[idx];
        float abs_x = abs(x);
        output[idx] = x / (1.0f + abs_x);
    }
}
```

Claude-3.5 Sonnet 在层级 2 问题 13 上取得 2.6 倍加速

torch 中的算子序列：

```python
x = torch.matmul(x, self.weight.T) # Gemm
x = x / 2 # Divide
x = torch.sum(x, dim=1, keepdim=True) # Sum
x = x * self.scaling_factor # Scaling
```

融合内核：

```c
__global__ void fused_ops_kernel(
    const float* input,
    const float* weight,
    float* output,
    const float scaling_factor,
    const int batch_size,
    const int input_size,
    const int hidden_size
) {
    // Each thread handles one element in the batch
    const int batch_idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (batch_idx < batch_size) {
        float sum = 0.0f;

        // Compute matmul and divide for this batch element
        for(int h = 0; h < hidden_size; h++) {
            float elem = 0.0f;
            for(int i = 0; i < input_size; i++) {
                elem += input[batch_idx * input_size + i] *
                        weight[h * input_size + i];
            }
            // Divide by 2 as we go
            sum += (elem / 2.0f);
        }

        // Scale and store final result
        output[batch_idx] = sum * scaling_factor;
    }
}
```

尽管有这个好例子，总体上层级 2 生成的内核显示出融合不足。预期大多数层级 2 的问题都可以用单一融合内核表达。

OpenAI-o1 在层级 3 问题 49 上取得 1.9 倍加速

我们有一个假设性的注意力机制架构，其中 softmax 被替换为 ReLU。

```python
    att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
    att = att.masked_fill(self.bias[:,:,:T,:T] == 0, float(’-inf’))
    att = F.relu(att)
```

模型找到一个融合缩放、masked fill 与 ReLU（但不含其他）的优化，带来 1.9 倍的温和改进。

```c
__global__ void fused_masked_fill_scale_relu_kernel(
    const float* __restrict__ att,
    const float* __restrict__ bias,
    float* __restrict__ output,
    int total_elems,
    float scale,
    int T,
    float negative_infinity
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < total_elems) {
        float val = att[idx] * scale;
        int bias_idx = idx % (T * T);
        if (bias[bias_idx] == 0.0f) {
            val = negative_infinity;
        }
        if (val < 0.0f) {
            val = 0.0f;
        }
        output[idx] = val;
    }
}
```

### D.3 硬件特性

OpenAI-o1 在层级 1 问题 96 上取得 2.8 倍加速

余弦相似度损失的 Torch 参考：

```python
cosine_sim = torch.nn.functional.cosine_similarity(predictions, targets, dim=1)
return torch.mean(1 - cosine_sim)
```

生成的内核使用共享内存来减少冗余的全局内存访问，提升数据局部性并提高整体性能。这是一个带同步点与归约操作的中等复杂内核，人类要写对并不容易。

```c
__global__ void cosine_similarity_loss_kernel(
    const float* __restrict__ predictions,
    const float* __restrict__ targets,
    float* __restrict__ losses,
    const int batch_size,
    const int input_size
) {
    // Each block handles one sample in the batch
    int sample_idx = blockIdx.x;
    if (sample_idx >= batch_size) return;

    // Shared memory for reductions
    extern __shared__ float sdata[];

    // Pointers to data for this sample
    const float* pred = predictions + sample_idx * input_size;
    const float* targ = targets + sample_idx * input_size;

    // Intermediate sums for dot product and norms
    float thread_dot = 0.0f;
    float thread_pred_norm_sq = 0.0f;
    float thread_targ_norm_sq = 0.0f;

    for (int idx = threadIdx.x; idx < input_size; idx += blockDim.x) {
        float p = pred[idx];
        float t = targ[idx];
        thread_dot += p * t;
        thread_pred_norm_sq += p * p;
        thread_targ_norm_sq += t * t;
    }

    // Reduction for dot product
    sdata[threadIdx.x] = thread_dot;
    __syncthreads();
    for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (threadIdx.x < s) {
            sdata[threadIdx.x] += sdata[threadIdx.x + s];
        }
        __syncthreads();
    }
    float dot_product = sdata[0];

    // Reduction for pred_norm_sq
    sdata[threadIdx.x] = thread_pred_norm_sq;
    __syncthreads();
    for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (threadIdx.x < s) {
            sdata[threadIdx.x] += sdata[threadIdx.x + s];
        }
        __syncthreads();
    }
    float norm_pred = sqrtf(sdata[0] + 1e-8f);

    // Reduction for targ_norm_sq
    sdata[threadIdx.x] = thread_targ_norm_sq;
    __syncthreads();
    for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (threadIdx.x < s) {
            sdata[threadIdx.x] += sdata[threadIdx.x + s];
        }
        __syncthreads();
    }
    float norm_targ = sqrtf(sdata[0] + 1e-8f);

    if (threadIdx.x == 0) {
        float cosine_sim = dot_product / (norm_pred * norm_targ + 1e-8f);
        losses[sample_idx] = 1.0f - cosine_sim;
    }
}
```

DeepSeek-R1 在层级 1 问题 98 上取得 1.9 倍加速

余弦相似度损失的 Torch 参考：

```python
self.loss_fn = torch.nn.TripletMarginLoss(margin=margin)
self.loss_fn(anchor, positive, negative)
```

另一个使用共享内存的生成内核示例：

```c
__global__ void triplet_margin_loss_kernel(
    const float* anchor,
    const float* positive,
    const float* negative,
    float* losses,
    float margin,
    int feature_size)
{
    extern __shared__ float shared_sums[];

    int batch_idx = blockIdx.x;
    int tid = threadIdx.x;

    int offset = batch_idx * feature_size;

    const float* a = anchor + offset;
    const float* p = positive + offset;
    const float* n = negative + offset;

    float a_p_sum = 0.0f;
    float a_n_sum = 0.0f;

    int stride = blockDim.x;
    for (int i = tid; i < feature_size; i += stride) {
        float diff_ap = a[i] - p[i];
        a_p_sum += diff_ap * diff_ap;
        float diff_an = a[i] - n[i];
        a_n_sum += diff_an * diff_an;
    }

    shared_sums[tid] = a_p_sum;
    shared_sums[blockDim.x + tid] = a_n_sum;

    __syncthreads();

    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            shared_sums[tid] += shared_sums[tid + s];
            shared_sums[blockDim.x + tid] += shared_sums[blockDim.x + tid + s];
        }
        __syncthreads();
    }

    if (tid == 0) {
        float d_ap = sqrtf(shared_sums[0]);
        float d_an = sqrtf(shared_sums[blockDim.x]);
        losses[batch_idx] = fmaxf(d_ap - d_an + margin, 0.0f);
    }
}
```

### D.4 迭代改进示例

#### D.4.1 迭代尝试新优化

我们给出一个在既有生成结果上迭代改进的内核示例。在下面的例子中，模型尝试新优化时出错、修复它们，并继续尝试新的优化，把内核改进到快于 torch.compile 基线（1.34 ms），但未达到 Torch Eager 基线（0.47 ms）。

层级 1，问题 63：方形输入与方形核的 2D 卷积。DeepSeek-R1，带执行与剖析反馈。

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 轮次 # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| 可编译？ | ✓ | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ |
| 正确？ | ✓ | ✗ | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ |
| 运行时间（ms） | 9.1 | - | 1.57 | - | 1.83 | 1.43 | - | 1.13 | - | 1.46 |

表 4：DeepSeek-R1 带执行反馈 $E$ 与剖析器反馈 $P$ 在层级 1 问题 63 上的迭代改进轨迹。Torch Eager 基线运行 0.47 ms，torch.compile 运行 1.34 ms。

在这个例子中，我们看到内核平均运行时间相对初始生成有 8 倍加速：模型反复（错误地）修改其内核，用反馈修复编译器问题，然后继续尝试更多优化。第一次性能大跃升（第 1 轮→第 3 轮）是因为模型决定沿输出通道维度启动线程块，而它最初是顺序计算这些元素的。模型随后在第 5 轮尝试使用共享内存并继续使用它，还在第 7、8 轮配合 __ldg 指令使用了纹理缓存内存。

#### D.4.2 利用反馈纠正内核代码

层级 2，问题 73：带 BatchNorm 与缩放因子的 2D 卷积。DeepSeek-R1，带执行反馈。

我们给出一个模型难以正确生成、而在利用执行反馈的迭代改进后产出正确内核的例子。

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 轮次 # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| 可编译？ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 正确？ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| 运行时间 | - | - | - | - | - | - | - | - | - | 3.16 |

表 5：DeepSeek-R1 带执行反馈 $E$ 在层级 2 问题 73 上的迭代改进轨迹。Torch Eager 基线运行 0.105 ms，torch.compile 运行 0.156 ms。

在上面的例子中，模型不断产出错误的输出张量形状或错误的数值，并利用这一反馈迭代其内核，直到最后一轮生成了功能正确但性能不佳的内核。我们在下面提供另一个显式利用编译器反馈修复编译错误的例子：

层级 2，问题 23：带 GroupNorm 的 3D 卷积并返回除批次维外所有维度的均值。DeepSeek-R1，带执行反馈。

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 轮次 # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| 可编译？ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ | ✗ | ✓ |
| 正确？ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| 运行时间 | - | - | 11.4 | 1.36 | - | - | 1.39 | 1.33 | - | - |

表 6：DeepSeek-R1 带执行反馈 $E$ 在层级 2 问题 23 上的迭代改进轨迹。Torch Eager 基线运行 1.29 ms，torch.compile 运行 0.719 ms。

在这个例子中，模型尝试使用 CUB 库，但错误地调用了函数。随后模型能够纠正这些错误，并在第 8 轮写出一个稍快的内核（见表 6）。

#### D.4.3 迭代改进始终无法修复错误

层级 1，问题 54：方形输入与方形核的 3D 卷积。DeepSeek-R1，带执行与剖析反馈。

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 轮次 # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| 可编译？ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 正确？ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 运行时间 | - | - | - | - | - | - | - | - | - | - |

表 7：DeepSeek-R1 带执行反馈 $E$ 与剖析器反馈 $P$ 在层级 1 问题 54 上的迭代改进轨迹。Torch Eager 基线运行 4.47 ms，torch.compile 运行 4.67 ms。

这个问题特别有趣，因为没有模型能为这个内核稳定地生成可运行的代码，即便提供不同形式的反馈与剖析信息。有趣的是，前一个例子可以说是这个内核更难的版本（把 3D 卷积与另一个算子融合），而同一个模型却能为那个任务生成可运行的代码。在上面的例子中，模型一再犯同样的错误，不断生成带有相同数值错误的功能不正确内核。

## 附录 E 迭代改进对正确性的影响

这里我们展示在轮次预算 $N=10$ 下，迭代改进（第 5.1.2 节）各配置的 $\text{fast}_{0}$ 相对单次尝试基线（第 4.1 节）的对比。我们发现模型在执行反馈 $E$ 下能更有效地自我纠正，尤其是修复与执行错误相关的问题。值得注意的是，DeepSeek-R1 在层级 1 和 2 上给定 10 轮迭代改进后能在 >90% 的任务上生成可运行的内核。然而，其余错误内核几乎总是因功能不正确而失败，这可能是因为正确性反馈不如执行失败信息细粒度。

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 方法 | 层级 1 |  |  | 层级 2 |  |  | 层级 3 |  |  |
|  | Llama-3.1 70B | DeepSeek V3 | Deepseek R1 | Llama-3.1 70B | Deepseek V3 | Deepseek R1 | Llama-3.1 70B | Deepseek V3 | Deepseek R1 |
| 单次尝试（基线） | 26% | 43% | 67% | 0% | 6% | 62% | 0% | 30% | 8% |
| 迭代改进（w G） | 27% | 48% | 72% | 2% | 7% | 67% | 0% | 36% | 14% |
| 迭代改进（w G+E） | 40% | 53% | 95% | 7% | 8% | 85% | 18% | 42% | 50% |
| 迭代改进（w G+E+P） | 36% | 50% | 95% | 7% | 9% | 92% | 8% | 44% | 42% |

表 8：利用执行反馈有助于减少错误：这里我们展示迭代改进下 LM 生成内核正确的问题百分比。我们注意到利用执行反馈帮助模型取得更好的正确率 $\text{fast}_{0}$，即到第 $N=10$ 轮为止模型至少有一个正确生成结果的问题百分比。我们标注了迭代改进的各种配置：利用先前生成 $G$、执行结果 $E$ 与计时剖析 $P$。

## 附录 F 少样本实验

在本实验中，我们在内核生成期间向模型提供融合、分块、重计算与异步等优化技术的上下文示例。如第 5.2.1 节所述，我们提供三个上下文示例：一个融合的 GELU（Hendrycks & Gimpel, 2023）、一个分块的矩阵乘法（Mills, 2024），以及一个展示有效共享内存 I/O 管理的最小 Flash-Attention（Dao et al., 2022；Kim, 2024）。本实验所用提示见附录 C.4。这些内核的加速相对 PyTorch Eager 计算。我们在下面比较这些少样本内核相对单次尝试基线的表现。

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | 基线 |  |  | 少样本 |  |  |
| 模型 | 层级 | $\text{fast}_{1}$ | $\text{fast}_{0}$ | 长度（字符） | $\text{fast}_{1}$ | $\text{fast}_{0}$ | 长度（字符） |
|  | 1 | 3% | 27% | 301018 | 6% | 27% | 360212 |
| Llama 3.1-70B | 2 | 0% | 0% | 646403 | 0% | 0% | 566668 |
|  | 3 | 0% | 0% | 404596 | 0% | 4% | 485332 |
|  | 1 | 10% | 55% | 343995 | 6% | 39% | 437768 |
| OpenAI o1 | 2 | 24% | 56% | 381474 | 16% | 39% | 432800 |
|  | 3 | 12% | 56% | 260273 | 8% | 22% | 364551 |

表 9：各模型在第 4.1 节基线与少样本提示下的表现对比。我们考察各层级的 $\text{fast}_{0}$、$\text{fast}_{1}$ 以及生成内核的累计字符长度。

层级 1 中 77% 的矩阵乘法问题通过分块取得了超过单次尝试基线的加速。每个 GEMM 变体的运行时间对比如下。

|  |  |  |  |
| --- | --- | --- | --- |
| 问题名称 | 基线（ms） | 少样本（ms） | 参考 Torch（ms） |
| 3D Tensor Matrix Multiplication | 20.9 | 7.71 | 1.45 |
| Matmul for Upper-Triangular Matrices | 14 | 5.39 | 2.98 |
| Matrix Scalar Multiplication | 1.19 | 0.811 | 0.822 |
| Standard Matrix Multiplication | 3.39 | 2.46 | 0.397 |
| Matmul with Transposed Both | 3.44 | 2.67 | 0.412 |
| Matmul with Transposed A | 3.61 | 2.99 | 0.384 |
| 4D Tensor Matrix Multiplication | 366 | 338 | 36 |
| Tall Skinny Matrix Multiplication | 3.39 | 3.59 | 1.9 |
| Matmul with Diagonal Matrices | 0.221 | 0.237 | 2.83 |

表 10：第 4.1 节基线与少样本提示在层级 1 矩阵乘法问题上的性能对比。

层级 2 中以下问题生成的少样本内核通过激进的共享内存 I/O 管理胜过了 PyTorch Eager。

|  |  |  |  |
| --- | --- | --- | --- |
| 问题名称 | 基线（ms） | 少样本（ms） | 参考 Torch（ms） |
| Conv2d InstanceNorm Divide | 0.514 | 0.0823 | 0.0898 |
| Gemm GroupNorm Swish Multiply Swish | 0.124 | 0.0542 | 0.0891 |
| Matmul Min Subtract | 0.0651 | 0.0342 | 0.0397 |
| Matmul GroupNorm LeakyReLU Sum | 0.0935 | 0.0504 | 0.072 |
| ConvTranspose3d Swish GroupNorm HardSwish | 33.3 | 29.6 | 35.2 |
| ConvTranspose2d Mish Add Hardtanh Scaling | 0.235 | 0.209 | 0.243 |
| ConvTranspose3d Add HardSwish | 15.6 | 14.1 | 22.2 |
| ConvTranspose2d Add Min GELU Multiply | 0.365 | 0.349 | 0.4 |
| ConvTranspose2d BiasAdd Clamp Scaling Clamp… | 0.3 | 0.31 | 0.368 |
| Conv2d GroupNorm Tanh HardSwish ResidualAdd… | 0.124 | 0.129 | 0.154 |
| Conv2d ReLU HardSwish | 0.0681 | 0.0711 | 0.0768 |

表 11：第 4.1 节基线与少样本提示在层级 2 中少样本内核胜过 PyTorch Eager 的那些问题上的性能对比。

## 附录 G 跨硬件案例研究

### G.1 不同硬件上的评估

为评估生成的内核在不同硬件平台上的表现，我们使用多块不同的 NVIDIA GPU，涵盖不同的微架构与能力。每块的细节见表 12。

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| 提供方 | GPU 型号 | 显存 | 功率 | 微架构 | FP16 TFLOPS | 显存带宽 |
| Baremetal | NVIDIA L40S | 48 GB | 300W | Ada | 362.05 | 864 GB/s |
| Baremetal | NVIDIA H100 | 80 GB | 700W | Hopper | 989.5 | 3350 GB/s |
| Serverless | NVIDIA L40S | 48 GB | 350W | Ada | 362.05 | 864 GB/s |
| Serverless | NVIDIA A100 | 42 GB | 400W | Ampere | 312 | 1935 GB/s |
| Serverless | NVIDIA L4 | 24 GB | 72W | Ada | 121 | 300 GB/s |
| Serverless | NVIDIA T4 | 16 GB | 70W | Turing | 65 | 300 GB/s |
| Serverless | NVIDIA A10G | 24 GB | 300W | Ampere | 125 | 600 GB/s |

表 12：不同 GPU 的规格，包括显存、功耗、微架构、FP16 TFLOPS、显存带宽及其提供方。

我们把第 4.1 节生成的同一组内核在多种硬件上运行（如表 12 所列）。我们在表 13 中计算相对在特定硬件平台上剖析的 PyTorch Eager 基线的 $\text{fast}_{1}$ 加速。

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 层级 | GPU | Llama-3.1-70b-Inst | DeepSeek-V3 | DeepSeek-R1 |
| 1 | L40S | 3% | 6% | 12% |
|  | H100 | 2% | 7% | 16% |
|  | A100 | 3% | 7% | 16% |
|  | L4 | 2% | 4% | 15% |
|  | T4 | 3% | 7% | 22% |
|  | A10G | 2% | 7% | 12% |
| 2 | L40S | 0% | 4% | 36% |
|  | H100 | 0% | 4% | 42% |
|  | A100 | 0% | 4% | 38% |
|  | L4 | 0% | 4% | 36% |
|  | T4 | 0% | 4% | 46% |
|  | A10G | 0% | 4% | 47% |
| 3 | L40S | 0% | 8% | 2% |
|  | H100 | 0% | 10% | 2% |
|  | A100 | 0% | 8% | 2% |
|  | L4 | 0% | 6% | 2% |
|  | T4 | 0% | 10% | 2% |
|  | A10G | 0% | 10% | 0% |

表 13：KernelBench 在多种硬件类型上的结果：不同模型与层级下各 GPU 相对 Torch Eager 的加速（$\text{fast}_{1}$）。不同 GPU 上使用的内核与为单次尝试（不含硬件/平台特定信息）生成的内核相同。

基于第 4.4 节与表 13 所述 DeepSeek R1 的 $\text{fast}_{1}$ 分数变异性增大，我们绘制了每个问题（层级 1 和 2）在不同 GPU 上的各自加速。加速相对 PyTorch Eager 计算，并在 $y=1.0$ 处有一条水平线标记 $\text{fast}_{1}$ 的分界。

![Refer to caption](2502.10517v1/figures/DeepSeekR1_Level1_HW.png)

图 9：DeepSeek R1 在层级 1 上不同 GPU 间的加速对比（对数尺度）。

![Refer to caption](2502.10517v1/figures/DeepSeekR1_Level2_HW.png)

图 10：DeepSeek-R1 在层级 2 上不同 GPU 间的加速对比（对数尺度）。

### G.2 提供硬件信息的效果

我们在内核生成期间向模型提供硬件特定信息，例如 GPU 的微架构、TFLOPS 与显存带宽（如表 12 所示）。这些生成结果随后在各自的硬件平台上剖析。相对 PyTorch Eager 的 $\text{fast}_{1}$ 加速见下表 14。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 层级 | GPU | Llama-3.1-70b-Inst | DeepSeek-V3 | DeepSeek-R1 | OpenAI-o1 |
| 1 | L40S | 2% | 5% | 14% | 13% |
|  | H100 | 3% | 6% | 14% | 9% |
|  | A100 | 4% | 4% | 16% | 9% |
| 2 | L40S | 1% | 4% | 33% | 25% |
|  | H100 | 2% | 2% | 35% | 33% |
|  | A100 | 2% | 1% | 31% | 32% |
| 3 | L40S | 0% | 2% | 0% | 10% |
|  | H100 | 2% | 8% | 0% | 12% |
|  | A100 | 0% | 0% | 2% | 8% |

表 14：在上下文中提供硬件规格：不同模型与层级下各 GPU 相对 Torch Eager 的加速（$\text{fast}_{1}$）。

如第 5.2.2 节所述，DeepSeek-R1 开始生成带 warp 矩阵乘累加（wmma）指令的内核。下面我们展示在上下文中提供 H100 规格时，层级 1 问题 1 的生成内核。

```c
#include <torch/extension.h>
#include <cuda_fp16.h>
#include <cuda_runtime.h>
#include <mma.h>

using namespace nvcuda;

__global__ void hgemm_kernel(const half* A, const half* B, half* C, int N) {
    const int WARPS_PER_BLOCK = 8;
    const int WMMA_M = 16;
    const int WMMA_N = 16;
    const int WMMA_K = 16;

    __shared__ half Ashared[WARPS_PER_BLOCK][WMMA_M][WMMA_K];
    __shared__ half Bshared[WARPS_PER_BLOCK][WMMA_K][WMMA_N];

    int warpId = threadIdx.x / 32;
    int laneId = threadIdx.x % 32;

    int tileM = (blockIdx.y * WARPS_PER_BLOCK + warpId) * WMMA_M;
    int tileN = blockIdx.x * WMMA_N;

    wmma::fragment<wmma::matrix_a, WMMA_M, WMMA_N, WMMA_K, half, wmma::row_major> a_frag;
    wmma::fragment<wmma::matrix_b, WMMA_M, WMMA_N, WMMA_K, half, wmma::row_major> b_frag;
    wmma::fragment<wmma::accumulator, WMMA_M, WMMA_N, WMMA_K, half> c_frag;
    wmma::fill_fragment(c_frag, __float2half(0.0f));

    for (int k = 0; k < N; k += WMMA_K) {
        int loadAidx = laneId + (tileM + (laneId / WMMA_K)) * N + k + (laneId % WMMA_K);
        int loadBidx = laneId + (k + (laneId / WMMA_N)) * N + tileN + (laneId % WMMA_N);

        if (tileM + (laneId / WMMA_K) < N && k + (laneId % WMMA_K) < N)
            Ashared[warpId][laneId / WMMA_K][laneId % WMMA_K] = A[loadAidx];
        else
            Ashared[warpId][laneId / WMMA_K][laneId % WMMA_K] = __float2half(0.0f);

        if (k + (laneId / WMMA_N) < N && tileN + (laneId % WMMA_N) < N)
            Bshared[warpId][laneId / WMMA_N][laneId % WMMA_N] = B[loadBidx];
        else
            Bshared[warpId][laneId / WMMA_N][laneId % WMMA_N] = __float2half(0.0f);

        __syncthreads();

        wmma::load_matrix_sync(a_frag, &Ashared[warpId][0][0], WMMA_K);
        wmma::load_matrix_sync(b_frag, &Bshared[warpId][0][0], WMMA_N);
        wmma::mma_sync(c_frag, a_frag, b_frag, c_frag);

        __syncthreads();
    }

    int storeCidx = (tileM + (laneId / WMMA_N)) * N + tileN + (laneId % WMMA_N);
    if (tileM + (laneId / WMMA_N) < N && tileN + (laneId % WMMA_N) < N)
        C[storeCidx] = c_frag.x[laneId];
}

torch::Tensor hgemm_cuda(torch::Tensor A, torch::Tensor B, int N) {
    auto C = torch::zeros({N, N}, A.options().dtype(torch::kFloat16));

    const int WARPS_PER_BLOCK = 8;
    dim3 grid((N + 15) / 16, (N + 15) / (16 * WARPS_PER_BLOCK));
    dim3 block(32 * WARPS_PER_BLOCK);

    hgemm_kernel<<<grid, block>>>(A.data_ptr<half>(), B.data_ptr<half>(), C.data_ptr<half>(), N);
    return C;
}
```

图 11：DeepSeek-R1 在提供 H100 GPU 硬件特定信息时为层级 1 问题 1 生成的 CUDA 内核。

## 附录 H 高吞吐评估系统

### H.1 单次实验：批量内核生成

鉴于需要评估的 GPU 内核数量庞大，我们构建了一个快速、高度并行化的评估系统，把内核生成与评估过程分为 3 个阶段，如图 12 所示。

- 推理：我们并行查询 LM 并存储生成的内核。

- CPU 预编译：我们用 nvcc 为指定硬件把模型生成的内核编译为二进制，在 CPU 上并行化，每个内核二进制保存到各自的特定目录以供缓存。

- GPU 评估：内核二进制已在 CPU 上构建完毕，我们专注于在多个 GPU 设备上并行评估多个内核。不过，为确保内核计时准确，一个设备上一次只评估一个内核。

![Refer to caption](2502.10517v1/figures/parallel-eval.png)

图 12：KernelBench 提供高吞吐的内核生成与评估系统。我们把内核的生成、编译与评估在 CPU 与 GPU 间并行化。

### H.2 迭代改进实验：GPU 编排器系统

在单次系统的基础上，我们还设计了一个可同时处理多个迭代改进实验的平台。我们把每个迭代改进实验视为一个有限状态机，状态为基于 LM 的内核生成、预编译、内核执行与剖析。状态转移基于环境反馈，并可依实验设置的不同而变化。

我们的系统运行在一个有 8 块可用 GPU 的节点上。与单次系统不同，对每次生成与内核执行做批处理效率极低——因此我们设计了一个带 GPU 编排器的流水线式多进程系统，具有以下特性：

- CPU 并行：编排器派生多个独立进程，每个处理 KernelBench 中的一个独立任务。这些进程为迭代改进实验运行多轮状态机逻辑——只有内核执行状态需要获取 GPU。

- 获取 GPU：GPU 编排器保持一个独立进程运行，用信号量管理哪些进程可以获取 GPU。进程在准备好执行与评估内核代码时可以向该进程请求 GPU。在可用 GPU 数量有限的系统上，我们尽量减少进程对 GPU 的占用以最大化资源吞吐。

- 在 CPU 上预编译：为避免进程长期占用 GPU 时间，我们在 CPU 上用 nvcc 为指定硬件把内核预编译为二进制。单次系统出于不同原因也用了同样的技巧。

- 在 GPU 上评估内核：有限状态机使用 GPU 的唯一状态是内核执行与剖析。我们发现等待 GPU 是编排器的主要瓶颈，因此我们把编排器设计为最大化设备占用率。

该系统总体上支持内核代码的生成与已生成内核代码的执行相互重叠。还有一些不可避免的错误，例如因内核生成有缺陷导致的 CUDA 非法内存访问与死锁，编排器通过在遇到时释放并派生新进程来解决，我们还编写了专门的处理器以确保这些错误被正确捕获而不使编排器本身崩溃。

### H.3 UI：可视化内核生成轨迹

为了定性观察生成结果并跨技术进行比较，我们设计了一个便于可视化的界面。我们将其作为 KernelBench 框架的一部分提供。

![Refer to caption](2502.10517v1/figures/kernel_inspect_interface.png)

图 13：我们提供一个用于内核检视的可视化界面。它使我们能够轻松检查内核内容、其性能，并跨多种技术与配置进行比较。

---
title: "介绍速度更快、内存占用更低的量化 Llama 模型"
title_en: "Introducing quantized Llama models with increased speed and a reduced memory footprint"
date: 2024-10-24
source: https://ai.meta.com/blog/meta-llama-quantized-lightweight-models
crawled: 2026-09-22
translated: 2026-09-22
---

# 介绍速度更快、内存占用更低的量化 Llama 模型

> 原文：[Introducing quantized Llama models with increased speed and a reduced memory footprint](https://ai.meta.com/blog/meta-llama-quantized-lightweight-models) · Meta AI（Wayback 存档）

**要点**

- 今天，我们发布首批轻量级量化 Llama 模型，它们足够小巧、高性能，可在许多主流移动设备上运行。
- 凭借算力资源、训练数据、完整评估和安全能力，Meta 在提供量化模型方面具有独特优势。
- 作为 Llama 该类别中的首批量化模型，这些指令微调模型沿用与原始 1B 和 3B 模型相同的质量与安全要求，同时实现 2-4 倍加速。
- 与原始 BF16 格式相比，我们还将模型尺寸平均降低 56%，内存占用平均降低 41%。
- 我们对 Llama 3.2 1B 和 3B 模型采用了两种量化技术：优先保证精度的「带 LoRA 适配器的量化感知训练」，以及优先保证可移植性的最先进后训练量化方法 SpinQuant。
- 两种量化技术的推理都通过 PyTorch 的 ExecuTorch 框架在 Llama Stack 参考实现中获得支持。
- 我们与业界领先的合作伙伴紧密协作构建了这些量化模型，并使其可在搭载 Arm CPU 的 Qualcomm 和 MediaTek SoC 上使用。3B 模型也观察到类似改进，详见结果部分。

在上个月的 Connect 2024 上，我们开源了 Llama 3.2 1B 和 3B——我们迄今最小的模型——以满足端侧和边缘部署的需求。自发布以来，我们不仅看到社区采用我们的轻量级模型，还看到草根开发者对其进行量化以节省容量和内存占用，但这往往以性能和精度为代价。正如我们此前分享的，我们希望让更多开发者更轻松地用 Llama 构建，而无需大量算力资源和专业能力。今天，我们分享 Llama 3.2 1B 和 3B 模型的量化版本。这些模型内存占用更低、端侧推理更快，兼具精度与可移植性——同时保持质量与安全，供开发者部署在资源受限的设备上。考虑到移动设备上可用的运行时内存有限，我们为这些新的量化模型优先考虑了最长 8K 的短上下文应用。我们的结果表明，通过在训练中引入量化，可以获得优于后处理的精度。基于 Android OnePlus 12 机型的测试，我们今天分享的模型相比原始格式有 2-4 倍加速，模型尺寸平均降低 56%，内存占用平均降低 41%。

从今天起，社区可以将我们的量化模型部署到更多移动 CPU 上，借此构建独特的快速体验，并因交互完全保留在设备上而提供更强的隐私性。我们使用带 LoRA 适配器的量化感知训练（QLoRA）开发了这些最先进的模型，以优化低精度环境下的性能。我们还使用了 SpinQuant——一种能确定最佳压缩组合、同时最大限度保留质量的技术。得益于与业界领先合作伙伴的紧密协作，QLoRA 和 SpinQuant 版 Llama 模型现已可在搭载 Arm CPU 的 Qualcomm 和 MediaTek SoC 上使用。量化模型的性能已使用 Kleidi AI 内核针对移动 CPU 优化，我们目前正与合作伙伴协作利用 NPU，为 Llama 1B/3B 带来更强的性能。

## 我们的量化设置

我们在设计当前量化方案时以 PyTorch 的 ExecuTorch 推理框架和 Arm CPU 后端为出发点，考虑的指标包括模型质量、预填充/解码速度和内存占用。我们的量化方案包括三个部分：

- 我们把所有 transformer 块中的所有线性层量化为权重的 4 比特分组方案（组大小为 32），激活采用 8 比特逐 token 动态量化。
- 分类层量化为权重的 8 比特逐通道、激活的 8 比特逐 token 动态量化。
- 嵌入采用 8 比特逐通道量化。

## 量化感知训练与 LoRA

我们采用量化感知训练（QAT），在 Llama 3.2 模型的训练过程中模拟量化效果，使我们能优化其在低精度环境下的性能。为初始化 QAT，我们使用经监督微调（SFT）得到的 BF16 Llama 3.2 模型检查点，并进行额外一整轮带 QAT 的 SFT 训练。然后我们冻结 QAT 模型的骨干，在 transformer 块内的所有层上应用低秩适配（LoRA）适配器，再进行一轮 SFT。同时，LoRA 适配器的权重和激活保持在 BF16。由于我们的方法在原理上与 QLoRA 类似（即先量化再加 LoRA 适配器），本文中称之为 QLoRA。最后，我们使用直接偏好优化（DPO）对得到的模型（骨干与 LoRA 适配器一起）进行微调。最终模型高效，精度可与 BF16 模型竞争，同时保持与其他量化方法相当的速度和内存占用（见下图）。我们使用 torchao API 完成 QAT。开发者可以进一步把 QAT 模型当作基础模型，用 LoRA 针对自己的定制用例微调 Llama，节省时间和计算成本。

## SpinQuant

尽管 QAT 效果最好，有些人可能想量化自己微调过的 1B 和 3B 模型，或者针对不同目标以不同量化设置量化模型。因此我们还发布了 SpinQuant 的模型和方法——一种最先进的后训练量化技术。虽然该方法的精度不如 QAT + LoRA，但 SpinQuant 的关键优势是可移植性，并且无需访问训练数据集（这些数据往往是私有的）即可运作。对数据可得性或计算资源受限的应用而言，它是一个有吸引力的方案。开发者可以用这一方法处理自己微调过的 Llama 模型，借助与 ExecuTorch 和 Llama Stack 完全兼容的开源仓库，针对不同的硬件目标和用例进行量化。

在我们的实验中，我们使用 WikiText 这一小型校准数据集来学习 SpinQuant 中的旋转矩阵。这些矩阵能平滑离群值，促成更有效的量化。在此之后，再应用范围设定和生成式后训练量化等量化最佳实践。SpinQuant 矩阵针对与 QAT + LoRA 类似的量化方案做了优化。

## 结果

在下表中，我们展示了对以下模型的综合评估：以普通后训练量化（PTQ）量化的模型、产出最先进 PTQ 质量的 SpinQuant，以及在所有方法中质量最好的 QLoRA。

（表格注：百分比差值均相对 BF16 的平均值计算。）

在下表中，我们比较了不同量化方法（SpinQuant 和 QAT + LoRA）与 BF16 基线的性能指标。评估使用 ExecuTorch 框架作为推理引擎、ARM CPU 作为后端。量化模型主要通过 Kleidi AI 库针对 Arm CPU 架构优化。性能测量采用基于 adb 二进制的方式，在 Android OnePlus 12 设备上测得。首 token 时间（TTFT）以提示长度 = 64 度量。

解码延迟平均改善 2.5 倍，预填充延迟平均改善 4.2 倍，模型尺寸降低 56%，内存占用平均降低 41%。这些基准如今可通过 ExecuTorch Llama 指南复现。上表结果使用 Android OnePlus 12 设备——不过我们也在 Samsung S24+（1B 和 3B）和 Samsung S22（1B）上验证了类似的相对性能。对于 iOS 设备，我们已验证这些模型可以以相当的精度运行，但尚未评估性能。除 CPU 外，我们目前正与合作伙伴协作，为这些量化模型利用 NPU 以获得更强性能。合作伙伴已在 ExecuTorch 开源生态中集成了利用 NPU 的基础组件，专门为 Llama 1B/3B 启用 NPU 量化的工作正在进行中。

## 展望未来

社区在短短时间内用 Llama 取得的热情与进展令我们深受鼓舞。今年，Llama 实现了 10 倍增长，成为负责任创新的标准。Llama 在开放性、可修改性和成本效率上持续领先，与闭源模型相比具有竞争力——甚至在某些领域领先。一如既往，我们迫不及待想看到社区用 Llama 构建什么，以及他们将在移动设备上带来的强大体验。Llama 3.2 模型现可在 llama.com 和 Hugging Face 下载。我们要感谢合作伙伴的紧密协作：Arm、Hugging Face、MediaTek、Ollama 和 Qualcomm。

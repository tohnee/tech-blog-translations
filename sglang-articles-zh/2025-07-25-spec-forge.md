---
title: "SpecForge：加速 SGLang 的投机解码训练"
title_en: "SpecForge: Accelerating Speculative Decoding Training for SGLang"
author: "The SGLang Team"
date: "July 25, 2025"
previewImg: /images/blog/spec_forge/logo.jpg
source: https://lmsys.org/blog/2025-07-25-spec-forge/
translated: 2026-09-12
---

# SpecForge：加速 SGLang 的投机解码训练

> 原文：[SpecForge: Accelerating Speculative Decoding Training for SGLang](https://lmsys.org/blog/2025-07-25-spec-forge/) · LMSYS Blog · The SGLang Team

投机解码（speculative decoding）是加速大语言模型（LLM）推理的一项强大技术。在这篇博客中，我们很高兴地宣布开源 **[SpecForge](https://github.com/sgl-project/SpecForge)**——我们面向基于 Eagle3 的投机解码打造的全新训练框架。SpecForge 以易用性为设计目标，并与 **[SGLang](https://github.com/sgl-project/sglang)** 推理引擎深度集成，实现了从训练到部署的无缝衔接。

## 为什么需要一个全新的投机解码训练框架

投机解码已成为加速 LLM 推理的一项突破性技术，但用于训练草稿模型（draft model）——这一流程中的关键组件——的健壮开源工具的缺失，严重阻碍了它的普及。许多现有的基于 Eagle3 的项目存在维护不力、功能有限，或与 SGLang 等框架缺乏兼容性的问题。这些限制已成为投机解码落地和实际部署的重大障碍。

为了弥合研究与部署之间的鸿沟，我们构建了 **SpecForge**——一个专门为训练草稿模型打造的生态系统，可与 SGLang 原生集成。训练一完成，模型即可开箱即用地进行推理，无需任何额外适配。与此同时，为当今的前沿 LLM——如 Llama 4、DeepSeek 等专家混合（MoE）模型——训练有效的草稿模型，需要能够应对其复杂度和规模的基础设施。SpecForge 从一开始就是为满足这些需求而量身构建的，弥合了前沿研究与真实部署之间的鸿沟。

SpecForge 的核心能力：

-   **原生支持先进架构**：SpecForge 支持前沿模型，包括复杂的 MoE 层和 Transformer 变体。
-   **可扩展的分布式训练**：集成了全分片数据并行（FSDP）和张量并行（TP）等现代大规模训练策略，SpecForge 可以在 GPU 集群上高效扩展。
-   **高内存效率训练**：经过优化的内存管理技术，使得即使为非常大的基座模型训练草稿模型也成为可能。

## SpecForge 的关键特性

### Eagle3 集成

Eagle 是一种最先进的投机解码方法，旨在加速大语言模型推理。它通过训练一个专门的轻量级草稿模型，来准确预测更大的目标模型（target model）的 token 分布，从而获得高接受率和显著的性能提升。

![intro.svg](/images/blog/spec_forge/eagleintro.PNG)

#### 训练时测试（TTT）支持

如此高的性能在很大程度上得益于 Eagle 独创的"训练时测试"（Training-Time Test，TTT）架构，它通过模拟多步生成来增强草稿模型的鲁棒性。尽管功能强大，TTT 因使用特殊的注意力掩码和递归数据循环而出了名地难以实现。SpecForge 通过内置 TTT 支持简化了这一复杂性，并参考官方 Eagle3 实现以确保正确性和最优性能。

### 两种训练模式：在线（Online）与离线（Offline）

SpecForge 提供两种灵活的训练模式——**在线（Online）**和**离线（Offline）**，简化了隐藏状态（hidden state）的收集。这种双模式设计确保了不同工作流下的灵活性，无论你的模型规模大小或硬件条件如何。

![offline_vs_online.svg](/images/blog/spec_forge/offline_online.jpg)

| 模式 | 目标模型使用方式 | 磁盘空间需求 | GPU 需求 | 一句话理由 |
|---------|-----------------------------|---------------------------------------------|------------------------------------------------------------|----------------------------------------------------------|
| 在线（Online） | 训练期间使用 | 低 | 目标模型较大时需要更多 GPU | 即时（on the fly）生成隐藏状态 |
| 离线（Offline） | 仅用于数据准备 | 高（例如 UltraChat + ShareGPT 需要约 12TB） | 低至 1 张 GPU（只需加载草稿模型） | 一次性预计算隐藏状态并高效复用 |

SpecForge 允许你根据自身需求定制训练流程。如果追求敏捷性和最小磁盘占用，请选择在线模式——非常适合快速迭代。如果可复现性和数据复用是首要考量、且存储空间充足，则可选择离线模式。

### 注重扩展性与规模化能力

我们的框架在设计上高度重视扩展性与规模化能力，以满足工程化生产要求。通过模块化接口，可以简单地实现并注册新的草稿模型与目标模型。

为支持大规模模型，SpecForge 利用 PyTorch 的 FSDP 并集成了张量并行，确保在多 GPU 集群上高效训练。

## 实验

使用 SpecForge，我们在来自 ShareGPT 和 UltraChat 的 320K 样本数据集上训练了 Llama 4 Scout 和 Maverick 模型。这些模型在 MT-Bench 等基准测试上的强劲表现证明了它们的有效性，并已为 Eagle3 推理做好准备。我们的 Llama 4 Maverick 草稿模型在 MT-Bench 上实现了 2.18× 的加速，Scout 变体则带来了 2.0× 的加速——展示了 SpecForge 在不同模型变体上的性能收益。详细结果总结如下。

我们针对 Scout 和 Maverick 评估了多种草稿 token 长度。

在下图所示的所有测试中，横轴表示步数（steps），对应 SGLang 中的 `speculative-num-steps`。同时，我们将 SGLang 的 `speculative-eagle-topk` 固定为 8、`speculative-num-draft-tokens` 固定为 10，以确保能够启用 `tree attention`（树形注意力）。要寻找最优的投机解码参数，可以使用 SGLang 仓库中的 **[bench_speculative](https://github.com/sgl-project/sglang/blob/main/scripts/playground/bench_speculative.py)** 脚本。它会针对不同配置运行吞吐量基准测试，帮助我们在特定硬件上调出最佳性能。

![scout.svg](/images/blog/spec_forge/Llama4_Scout_performance_final.svg)

![maverick.svg](/images/blog/spec_forge/Llama4_Maverick_performance_final.svg)

## 代码与模型获取

欢迎在 GitHub 上浏览我们的源代码，并在 Hugging Face 上试用预训练模型。

**[💻 GitHub 仓库](https://github.com/sgl-project/SpecForge)**：训练框架的完整源代码，包含 TTT 与数据处理的实现细节。

🤗 Hugging Face 模型：下载 Llama 4 [Scout](https://huggingface.co/lmsys/sglang-EAGLE3-Llama-4-Scout-17B-16E-Instruct-v1) 和 [Maverick](https://huggingface.co/lmsys/sglang-EAGLE3-Llama-4-Maverick-17B-128E-Instruct-v1) 的 Eagle3 草稿头（不含完整模型），用于你的项目。

## 路线图

近期，我们计划为 SpecForge 增加以下支持。

-   支持更多模型架构，包括 Kimi K2 和 Qwen-3 MoE。我们正与 LinkedIn 基础设施团队积极合作，他们正在训练更多 Qwen-3 MoE 草稿模型，未来将由 SpecForge 提供支持。
-   将视觉语言模型（VLM）集成到 SpecForge 中。
-   通过更好的并行策略和 kernel 优化，支持更高效的训练。

## 致谢

我们衷心感谢以下团队与合作者：

**SGLang 团队与社区** — Shenggui Li、Yikai Zhu、Fan Yin、Chao Wang、Shuai Shi、Yi Zhang、Yingyi Huang、Haoshuai Zheng、Yubo Wang、Yineng Zhang 以及许多其他成员。

**SafeAILab 团队** — Yuhui Li、Hongyang Zhang 及各位成员 — 感谢他们在 Eagle3 算法上的开创性工作。

我们特别感谢美团对本项目的早期支持与贡献。同时真诚感谢我们的官方基础设施合作伙伴 [Voltage Park](https://www.voltagepark.com/)，他们与 SGLang 团队的正式合作为 SpecForge 提供了算力基础。他们的支持使我们能够高效、可靠地训练和评估大规模投机解码模型，我们也深深感谢他们致力于让尖端 AI 基础设施民主化普及。

"**Voltage Park 的使命是通过让高性能 AI 基础设施人人可用，成为创新的催化剂。一个繁荣的 AI 研究生态，应当是创新的工具由众多声音共同塑造、而非集中在少数人手中，**" Voltage Park 首席产品与技术官（Chief Product and Technology Officer）Saurabh Giri 表示。"**正因如此，我们非常自豪能够为 SGLang 团队提供关键基础设施，支持他们开发像 SpecForge 这样高质量的开源项目——我们相信基础性的开源模型和框架应当服务于公共利益，并且对进步至关重要。我们期待社区利用这些新能力创造出精彩的应用。**"

我们期待看到社区用 SpecForge 创造出什么。无论你是在优化现有模型还是训练新模型，都欢迎提供反馈、贡献代码、开展合作——让我们一起加速开源 LLM 创新！

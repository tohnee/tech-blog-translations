---
title: "用 AITemplate 在 GPU 上实现更快、更灵活的推理：一个革命性的新推理引擎"
title_en: "Faster, more flexible inference on GPUs using AITemplate, a revolutionary new inference engine"
date: unknown
source: http://ai.facebook.com/blog/gpu-inference-engine-nvidia-amd-open-source
crawled: 2026-09-22
translated: 2026-09-22
---

# 用 AITemplate 在 GPU 上实现更快、更灵活的推理：一个革命性的新推理引擎

> 原文：[Faster, more flexible inference on GPUs using AITemplate, a revolutionary new inference engine](http://ai.facebook.com/blog/gpu-inference-engine-nvidia-amd-open-source) · Meta AI（Wayback 存档）

2022 年 10 月 3 日

GPU 在交付部署 AI 模型（尤其是计算机视觉、自然语言处理和多模态学习中的大规模预训练模型）所需的算力方面扮演着重要角色。当前，AI 从业者在选择高性能 GPU 推理方案时灵活性极为有限，因为这些方案集中在平台专属、封闭的黑盒运行时之中。为某一家技术供应商的 GPU 设计的机器学习系统，必须完全重新实现才能在另一家供应商的硬件上运行。这种灵活性的缺失也使得迭代和维护构成这些方案的代码变得困难，原因是复杂运行时环境中的硬件依赖。此外，AI 生产流水线往往要求快速开发。由于领域快速演进，开发者渴望尝试新颖的建模技术。尽管 TensorRT 等专有软件工具包提供了定制途径，但往往不足以满足这一需求。而且，封闭的专有方案可能让代码的快速调试变得更难，降低开发敏捷性。

为应对这些行业挑战，Meta AI 开发并开源了 AITemplate（AIT）——一个为 AMD 和 NVIDIA GPU 硬件分别提供加速后端的统一推理系统。它在多种广泛使用的 AI 模型（如卷积神经网络、transformer 和扩散模型）上，提供接近硬件原生的 Tensor Core（NVIDIA GPU）与 Matrix Core（AMD GPU）性能。有了 AIT，如今可以在两家 GPU 供应商的硬件上运行高性能推理。借助 AIT，我们相比 PyTorch 的 eager 模式，在 NVIDIA GPU 上实现了最高 12 倍、在 AMD GPU 上最高 4 倍的性能提升。

AITemplate 是一个把 AI 模型转换为高性能 C++ GPU 模板代码以加速推理的 Python 框架。我们的系统以速度和简洁为设计导向。AITemplate 分为两层——前端层执行各类图变换以优化计算图，后端层则为 GPU 目标生成 C++ 内核模板。此外，AIT 对外部库的依赖保持最低。例如，生成的推理运行时库是自包含的，只需要 CUDA/ROCm 运行环境。（CUDA 是 NVIDIA 的统一计算设备架构，让 AI 软件得以在 NVIDIA GPU 上高效运行；ROCm 是一个开源软件平台，为 AMD GPU 提供同样的能力。）

我们的项目带来许多性能创新，包括先进的内核融合（kernel fusion，一种将多个内核合并为单个内核以更高效运行的优化方法），以及针对 transformer 模块的高级优化。这些优化通过显著提升 NVIDIA Tensor Core 和 AMD Matrix Core 的利用率，带来了最先进的性能。AITemplate 目前支持 NVIDIA A100 和 AMD MI200 GPU 系统，两者如今都被科技公司、研究实验室和云计算服务商的数据中心广泛使用。

下面展示的基准结果比较了 PyTorch eager 模式与 AITemplate 在 NVIDIA A100 GPU 上若干主流模型的性能。（AIT 与 PyTorch eager*：NVIDIA A100-40GB 上的 ResNet-50 以及序列长度 384 的 BERT-Base 基准。）

如下面的基准所示，借助 AITemplate，采用 AMD MI250 GPU 的模型同样能获得显著性能提升，包括驱动先进视觉与语言系统的 ResNet 和 transformer 模型。（MI250 采用 2 GCD 设置，每个 GCD（核心）处理一半数据。PyTorch eager 与 AIT：AMD MI250 上的 ResNet-50、序列长度 384 的 BERT-base 基准。MI250 以数据并行模式运行，每个 GCD（GPU 核心）处理一半数据；批大小为 1 时，该批次在单个 GCD 上处理，另一个 GCD 空闲。）

统一的 GPU 后端支持让深度学习开发者在几乎不产生迁移成本的情况下拥有更多硬件供应商选择。部署 AITemplate 非常直接：AI 模型被编译成一个无依赖的自包含二进制文件。该二进制可在任何具备相同硬件以及 CUDA 11 / ROCM 5 及更新版本的环境中运行，从而带来出色的向后兼容性。这在稳定性和向后兼容性至关重要的生产环境中意义重大。AITemplate 还开箱即用地提供了广泛使用的模型（如 VisionTransformer、BERT、Stable Diffusion、ResNet 和 MaskRCNN），这简化了部署流程，让从业者可以轻松部署 PyTorch 预训练模型。

## AITemplate 的优化

AITemplate 拥有业界最先进的内核融合系统之一，这得益于它对三项创新优化的支持：纵向融合、横向融合和内存融合。纵向融合把操作链融合在一起；横向融合把互不依赖的并行操作融合为一个分组操作；内存融合把内存搬运操作与计算密集型操作融合在一起。纵向、横向和内存融合还可以组合使用——AITemplate 能把三种融合结合起来加速推理。就横向融合而言，AITemplate 目前支持分组 GEMM 操作、分组 GEMM + 激活操作，以及分组 layernorm/swish layernorm 操作。

AITemplate 支持多种超越标准逐元素（element-wise）操作的纵向融合，包括：

- 通过 CUTLASS 与 Composable Kernels 的 epilogue 融合实现的 GEMM 与逐元素操作融合；
- 面向 transformer 多头注意力模块的 GEMM 与 permute 融合；
- 将 split、slice、concatenate 等内存操作与其他操作融合，通过 Tensor Accessors 降低内存带宽占用。

对于标准的 transformer 多头注意力模块，AITemplate 目前在 NVIDIA GPU 上依赖 Flash Attention，在 AMD GPU 上依赖 Composable Kernels 中泛化的背靠背 GEMM/softmax/GEMM 融合。两种实现都完全消除了计算单元与 HBM（高带宽内存）之间针对中间结果的数据搬运。借助 Composable Kernels，不仅注意力模块，神经网络中大量瓶颈结构都可以被融合。许多原先受带宽限制的问题现在变为受计算限制，系统因此可以更高效地利用 GPU 算力。如下所示，这一优化对具有长序列的 transformer 模型更为有效。

我们的方法超越了以往的系统能力：不仅在编译器内生成模板（例如最先进的多维融合——横向融合、纵向融合与内存融合），还为 NVIDIA 和 AMD GPU 引入了统一解决方案。

## 开发 AITemplate

AITemplate 拥有两层模板系统：第一层是 Python Jinja2 模板，第二层是 GPU Tensor Core/Matrix Core C++ 模板（NVIDIA GPU 使用 CUTLASS，AMD GPU 使用 Composable Kernel）。AITemplate 首先在 Python 中运行性能剖析以找到最佳内核配置，然后把 Jinja2 模板渲染成 C++ 代码。模型源代码生成后，GPU C++ 编译器（NVIDIA NVCC 和 AMD HIPCC）将源代码编译为模型的最终二进制代码。其前端设计与 PyTorch 类似，用户可以轻松地把模型从包括 PyTorch 在内的多种不同框架转换为 AITemplate。

## 更绿色的计算

我们的技术扩展了 AI 平台的可得性，并有助于减少碳排放以应对环境问题。研究表明，GPU 使用与碳排放相关。AITemplate 缩短了 GPU 执行时间，也将减少排放。由于 AI 模型部署在全球科技公司的核心系统中，效率的提升可以产生显著影响。该系统还通过为 AI 推理工作负载提供更多平台选择，让已训练 AI 模型的推理运行更加普惠。

## 向新硬件扩展并增加更多功能

AITemplate 以更低的系统复杂度为当前和下一代 NVIDIA、AMD GPU 提供最先进的性能。然而，我们构建高性能 AI 推理引擎的旅程才刚刚开始。我们正在积极推进为 AITemplate 增加更多优化以及对完全动态形状（dynamic shape）的支持。我们还计划把 AITemplate 扩展到更多硬件系统，例如 Apple M 系列 GPU，以及其他技术供应商的 CPU。除此之外，我们正在研究 PyTorch 模型的自动 lowering，为 PyTorch 提供一套额外的交钥匙推理方案。我们也乐于探索与 ONNX、Open-XLA 等其他框架的集成。我们希望构建一个性能更佳、灵活性更高、后端选择更丰富的更绿色、更高效的 AI 推理生态。

获取代码：https://github.com/facebookincubator/AITemplate

这项工作由 Meta 一个庞大团队完成，成员包括 Bing Xu、Ying Zhang、Hao Lu、Yang Chen、Terry Chen、Mike Iovine、Mu-Chu Lee、Scott Wolchok、Oleg Khabinov、Shirong Wu、Huaming Li、Hui Guo、Zhijing Li、Max Podkorytov、Janet Yang、Yinghai Lu、Lu Fang、Andrew Tulloch 和 Ajit Mathews。

\* 该图未包含 PyTorch 1.12 引入的 Better Transformer。\*\*复现代码与说明见仓库 examples 目录。

作者：
- Bing Xu，软件工程师
- Ajit Mathews，工程总监
- Hao Lu，软件工程师
- Terry Chen，软件工程师
- Yang Chen，软件工程师
- Ying Zhang，软件工程师

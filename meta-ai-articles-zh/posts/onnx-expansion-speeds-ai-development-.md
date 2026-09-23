---
title: "ONNX 扩容加速 AI 开发"
title_en: "ONNX expansion speeds AI development"
date: 2018-05-02
source: https://ai.meta.com/blog/onnx-expansion-speeds-ai-development-
crawled: 2026-09-22
translated: 2026-09-22
---

# ONNX 扩容加速 AI 开发

> 原文：[ONNX expansion speeds AI development](https://ai.meta.com/blog/onnx-expansion-speeds-ai-development-) · Meta AI（Wayback 存档）

在近期深度学习浪潮的初期，研究人员可用的工具屈指可数（如 Torch、Theano 和 Caffe），而今天已经存在一个由深度学习框架和硬件运行时构成的健全生态。这个不断壮大的工具箱极其有用，但如果缺乏互操作性，每个框架都有可能变成一座孤岛。然而互操作性要求对每一种可能的框架/运行时组合做大量定制集成工作，而且在框架之间迁移时重新实现模型通常很困难，可能让开发放缓数周甚至数月。Facebook 参与开发了开放神经网络交换（Open Neural Network Exchange，ONNX）格式，让 AI 工程师能够在框架之间更轻松地迁移模型，而无需进行资源消耗巨大的定制工程。今天，我们要分享的是：ONNX 正在增加对更多 AI 工具的支持，包括百度的 PaddlePaddle 平台和 Qualcomm SNPE。ONNX 还将新增一个可用于生产环境的 Apple Core ML 转换器。有了这些补充，ONNX 现在能够适配绝大多数模型类型，并可以部署到数以百万计的移动设备上。

借助 ONNX，AI 工程师可以使用任意一种受支持的框架开发模型，把模型导出到为生产服务优化的另一框架，或导出到硬件运行时以在特定设备上进行优化推理。其结果是，工程师现在可以更快、更灵活地开发和实现最新研究，同时充分利用种类繁多的工具。在实践中，加速「从研究到生产」的管线，有望更快地把强大的 AI 能力带到现实应用中，催生全新体验。

## 让 AI 工具实现互操作

各大科技公司通过开源或积极支持各种深度学习框架推动了 AI 发展，其中包括 Amazon Web Services（Apache MXNet）、Facebook（Caffe2 与 PyTorch，以及正在开发中的 PyTorch 1.0）、Google（TensorFlow）和 Microsoft（Cognitive Toolkit）。同时，硬件运行时的生态也在不断壮大，例如 NVIDIA 的 TensorRT 和 Intel 的 nGraph，它们借助量化、层融合等技术，帮助简化并优化部署到设备上的「最后一公里」。

我们于 2017 年 9 月与 Microsoft 展开合作，发布了 ONNX 规范，目的在于让深度学习生态实现互操作。此后，Amazon Web Services、AMD、ARM、华为、IBM、Intel、NVIDIA 和 Qualcomm 相继加入；最近，百度、Bitmain、Mediatek 和 Preferred Networks 也加入了这一行列。ONNX 已经让 AI 工程师能够在由框架、转换器和运行时构成的庞大生态中自由使用卷积神经网络（CNN）、长短期记忆（LSTM）单元等模型类型。这种灵活性让工程师得以把更多精力放在要解决的问题上，而不是纠结于使用哪些工具。随着 ONNX 不断增加新能力，开发者将能够部署更多类型的模型、使用量化数据格式，并从推理延伸到支持模型训练。此外，这种跨系统的互操作性将让快速增长的 AI 社区更紧密地协作，并从整个领域的进步中受益。

## ONNX 版图正在如何扩张

看到如此广泛的生态如此迅速地成形固然令人振奋，但尤其鼓舞我们的是，AI 社区已经构建并推出了可用于生产环境的解决方案和库。这些进展表明 ONNX 正在走出初始开发阶段，迈入能够支持各种用例的大规模环境。近期推出的产品和社区项目包括：

- **Core ML 官方支持**——Core ML 让开发者能够快速构建在 Apple 各类产品上具备智能新特性的应用。ONNX 社区现在拥有一个可用于生产的 Core ML 转换器，开发者可以将 ONNX 格式的模型直接导入 Core ML，并直接集成到 iOS 应用中。
- **Snapdragon 神经处理引擎的生产支持**——Qualcomm Snapdragon 神经处理引擎 SDK 旨在帮助开发者把以 ONNX 格式训练并导出的一个或多个神经网络模型运行在 Snapdragon 移动平台的 CPU、GPU 或 DSP 上。
- **百度 PaddlePaddle**——PaddlePaddle（PArallel Distributed Deep LEarning）是最初由百度的科学家和工程师为其自家产品开发的深度学习平台。今天，Paddle 团队公开发布了其 ONNX 格式模型导出器的首个版本，使 AI 开发者能够利用各种数据中心、移动和嵌入式推理运行时。
- **NVIDIA TensorRT 4**——TensorRT 是一个深度学习推理优化器和运行时。TensorRT 4 中的原生 ONNX 解析器提供了一条简便路径，可以把来自 Caffe2、Chainer、Microsoft Cognitive Toolkit、Apache MxNet 和 PyTorch 等框架的 ONNX 模型导入 TensorRT。

## ONNX 的下一步

尽管 ONNX 在普及和生态扩张方面进展显著，仍有大量工作要做。我们正在多个方向上继续推进，所有方向都向社区开放，欢迎参与和贡献：

- **NLP 支持**——现代 NLP（自然语言处理）是深度学习的重要应用。此外，现代 NLP 网络往往实现起来并不简单，在框架之间迁移更是难上加难。这些网络通常无法在各类框架中被一致地处理。ONNX 连接这些网络的能力将是一个极具吸引力的特性。NLP 网络（包括循环网络）构建在动态控制结构之上，标准化对这些结构的处理可以促进与后端的更好协作，暴露网络语义并获得更好的性能。计算机视觉领域形成了一个传统：针对 ResNet-50 这类规范化视觉模型优化硬件后端。NLP 领域尚无类似传统，但通过标准化 NLP 网络的表示，我们可以给厂商提供一种共同表示，推动 NLP 模型性能的前进。
- **通用框架接口提案**——领先的硬件和系统厂商提供高度优化的软件来运行神经网络图。与通用实现相比，这些软件可以带来数量级的加速，但由于各厂商接口各异、且与高层应用软件栈存在微妙的不兼容，它们与深度学习框架和应用的集成十分复杂。迄今为止，ONNX 格式针对的是通过离线翻译在不同高层框架与厂商专有库之间离线转换神经网络模型的问题。在这项提案中，我们分析如何丰富 ONNX 生态，以支持高性能图执行后端的运行时发现与选择，以及把 ONNX 图在线转换为实现内部的表示。
- **社区工作组**——除了 ONNX 核心与接口的工作之外，还有多项努力正在把 ONNX 范式拓展到模型训练（而不仅是推理）等领域，构建对模型量化与压缩的支持，创建测试与合规工具集，并持续扩充包含预训练 ONNX 模型的模型动物园。如果你希望参与，请在 GitHub 上联系各工作组的负责人。

除了这些对 ONNX 生态的重要补充之外，我们还在将其适配为 PyTorch 1.0——我们兼顾开发与生产的新一代灵活 AI 框架——的内部中间表示。我们相信 ONNX 将继续成长并找到新的用武之地，推动 AI 的开发与落地。

希望进一步了解 ONNX 的工程师可以使用以下资源：在此了解 ONNX 及其背后的社区；试用教程，看看在框架之间迁移模型有多容易；了解如何为项目做贡献；在 GitHub 上联系我们，告诉我们你对项目的看法；关注 F8 大会上的 ONNX 专场， featuring AWS、Facebook 和 Microsoft 的受邀报告。

我们相信 ONNX 已经有了良好的开端，而有了你的帮助它可以变得更好。我们正在积极寻找伙伴参与工作组、宣传推广 ONNX 的使用并直接为项目做贡献。如果你愿意为 ONNX 的发展出力，欢迎加入我们。

**作者**

- Joseph Spisak，Facebook 产品经理

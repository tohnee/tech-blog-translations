---
title: "用量化噪声训练实现极致模型压缩"
title_en: "Training with quantization noise for extreme model compression"
date: 2020-04-23
source: https://ai.facebook.com/blog/training-with-quantization-noise-for-extreme-model-compression
crawled: 2026-09-22
translated: 2026-09-22
---

# 用量化噪声训练实现极致模型压缩

> 原文：[Training with quantization noise for extreme model compression](https://ai.facebook.com/blog/training-with-quantization-noise-for-extreme-model-compression) · Meta AI（Wayback 存档）

2020 年 4 月 23 日

**研究内容：**Quant-Noise 是一种新技术，可对模型进行极致压缩，同时在实际应用部署时仍保持高性能。我们将其应用于计算机视觉（CV）和自然语言处理（NLP）模型，它可与多种量化方法配合使用，如 int4、int8 和乘积量化器（iPQ）。与 iPQ 结合使用时，Quant-Noise 在 NLP 和 CV 基准任务上刷新了「高精度 + 小模型」组合的最先进水平。我们的方法交付的性能几乎与原始未压缩模型持平，同时把内存占用缩减 10 到 20 倍，显著超过 PyTorch 和 Tensorflow 目前可用的 int8 的 4 倍压缩。在可接受更大性能取舍的用例中，Quant-Noise 还可以把模型进一步压缩——超过 50 倍。Quant-Noise 只通过添加一种类似 dropout 的正则化噪声来改变模型训练，对收敛速度和训练速度都没有影响。我们已开源代码，供其他研究者复现结果并在其工作中使用 Quant-Noise。

**工作原理：**量化可以缩小神经网络的内存占用并加速推理。但直接对一个已训练好的模型应用量化会显著损害性能，因为模型并非在这种设定下训练。为克服这一问题，Quant-Noise 在训练期间模拟量化的效果：训练时的前向传播中，它取一部分权重，随机施加模拟的量化噪声。这使模型对量化具有韧性，能在精度损失很小的情况下实现大压缩比。

图示展示了我们如何在训练期间对一部分权重施加量化噪声，以提升量化后模型的性能。与以往量化感知训练的方法不同，Quant-Noise 只施加于一小部分权重。这一方法的优势在于，无偏梯度仍然可以从未受噪声影响的权重流出。我们已证明，该框架把最先进的 EfficientNet-B3 模型从约 50 MB 压缩到 3.3 MB，同时在 ImageNet 上取得 80% 的 top-1 准确率（未压缩模型为 81.7%）。同样，我们用 Quant-Noise 把 Facebook AI 最先进的 RoBERTa Base 模型从 480 MB 压缩到 14 MB，在 MNLI 上取得 82.5% 的成绩（原模型为 84.8%）。

**为什么重要：**最先进的模型正变得越来越大。例如，如今广泛用于 NLP 任务的 Transformer 每层都有数百万参数。通过在不显著降低性能的前提下缩小这些模型，Quant-Noise 可以帮助把前沿 AI 带到智能手机、平板甚至 IoT 芯片组上，一切完全在端侧运行，避免恼人的错误和卡顿。这将让全世界数千万人使用的设备得以运行新的虚拟和增强现实体验、更智能的助手以及其他新产品和新体验。此外，由于 Quant-Noise 适配多种量化方法和模型类型，它可以应用于各种实际用例，还可用于进一步压缩 EfficientNet 等紧凑模型。Facebook AI 目前正在探索把 Quant-Noise 用于多种端侧 AI 应用，我们期待看到其他人在自己的工作中如何利用这一框架。

**在 GitHub 上获取：**
论文：https://arxiv.org/abs/2004.07320
GitHub：https://github.com/pytorch/fairseq/tree/master/examples/quant_noise

**作者：**Angela Fan 研究助理；Pierre Stock 研究助理

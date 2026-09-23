---
title: "PyTorch 1.3 新增移动端、隐私、量化与命名张量支持"
title_en: "PyTorch 1.3 adds mobile, privacy, quantization, and named tensors"
date: 2019-03-15
source: http://ai.facebook.com/blog/pytorch-13-adds-mobile-privacy-quantization-and-named-tensors
crawled: 2026-09-22
translated: 2026-09-22
---

# PyTorch 1.3 新增移动端、隐私、量化与命名张量支持

> 原文：[PyTorch 1.3 adds mobile, privacy, quantization, and named tensors](http://ai.facebook.com/blog/pytorch-13-adds-mobile-privacy-quantization-and-named-tensors) · Meta AI（Wayback 存档）

PyTorch 的增长势头不减，因为它专注于满足研究人员的需求、拥有精简的生产工作流，而最重要的是 AI 社区的热情支持。正如 O'Reilly 所指出的，仅 2019 年上半年，ArXiv 论文中对 PyTorch 的引用就增长了 194%；平台贡献者数量在过去一年增长超过 50%，达到近 1,200 人。Facebook、Microsoft、Uber 以及各行业的组织正越来越多地把它作为最重要机器学习（ML）研究和生产工作负载的基础。我们现在通过发布 PyTorch 1.3 进一步推进该平台，其中包括多项实验性特性支持：向移动设备无缝部署模型、面向推理性能的模型量化，以及前端改进（如命名张量、编写更清晰的代码而减少行内注释）。我们还推出一批额外的工具和库，支持模型可解释性并把多模态研究带向生产。此外，我们与 Google 和 Salesforce 合作，为云张量处理单元（Cloud TPU）添加了广泛支持，为训练大规模深度神经网络提供了显著加速的选项。阿里云也加入 Amazon Web Services、Microsoft Azure 和 Google Cloud 的行列，成为支持 PyTorch 用户的云平台。你现在可以在 pytorch.org 开始使用。

## PyTorch 1.3

PyTorch 1.3 带来重要的新特性，包括对移动设备部署的实验性支持、8 位整数的即时模式量化，以及命名张量的能力。对于每一项增强，我们都期待 PyTorch 社区的更多贡献和改进。

### 命名张量（实验性）

康奈尔大学的 Sasha Rush 曾指出，张量的传统实现尽管在深度学习中无处不在，却存在显著缺陷：暴露私有维度、基于绝对位置广播、把类型信息留在文档里。他提出了命名张量作为替代方案。今天，我们通过注释来命名和访问维度：

```python
# Tensor[N, C, H, W]
images = torch.randn(32, 3, 56, 56)
images.sum(dim=1)
images.select(dim=1, index=0)
```

而显式命名会带来更可读、更可维护的代码：

```python
NCHW = ['N', 'C', 'H', 'W']
images = torch.randn(32, 3, 56, 56, names=NCHW)
images.sum('C')
images.select('C', index=0)
```

### 量化（实验性）

开发 ML 应用时，高效利用服务器端和设备端计算资源很重要。为了支持在服务器和边缘设备上更高效地部署，PyTorch 1.3 现在支持通过熟悉的即时模式 Python API 进行 8 位模型量化。量化指以降低的精度（如 8 位整数）执行计算和存储的技术。这一目前处于实验阶段的特性支持训练后量化、动态量化和量化感知训练。它利用了 FBGEMM 和 QNNPACK 这两个最先进的量化内核后端（分别面向 x86 和 ARM CPU），它们已与 PyTorch 集成并共用统一 API。想了解设计与架构，请查阅此处的 API 文档，并用此处的教程开始使用任何受支持的技术。

### PyTorch 移动端（实验性）

随着应用不断要求更低的时延，在边缘设备上运行 ML 的重要性与日俱增。它也是联邦学习等隐私保护技术的基础要素。为了支持更高效的设备端 ML，PyTorch 1.3 现在支持从 Python 到 iOS 和 Android 部署的端到端工作流。这是一个早期的实验版本，针对端到端开发优化。后续版本将聚焦于：

- **尺寸优化**：构建级优化和依据用户应用所需算子的选择性编译（即为所需算子付出二进制体积代价）。
- **性能**：进一步改进移动 CPU 和 GPU 上的性能与覆盖。
- **高级 API**：扩展移动原生 API，覆盖在移动应用中融入 ML 所需的常见预处理与集成任务，例如计算机视觉和 NLP。

在此了解更多或在 Android 或 iOS 上开始使用。

## 模型可解释性与隐私的新工具

### Captum

随着模型变得日益复杂，开发新的模型可解释性方法愈发重要。为帮助满足这一需求，我们推出 Captum——一个帮助使用 PyTorch 的开发者理解其模型为何产生特定输出的工具。Captum 提供最先进的工具，理解特定神经元和层的重要性如何影响模型做出的预测。Captum 的算法包括积分梯度（integrated gradients）、conductance、SmoothGrad 与 VarGrad，以及 DeepLift。下面的示例展示了如何在预训练 ResNet 模型上应用模型可解释性算法，然后通过把归因叠加到图像上，对每个像素的归因进行可视化。

```python
noise_tunnel = NoiseTunnel(integrated_gradients)
attributions_ig_nt, delta = noise_tunnel.attribute(input, n_samples=10, nt_type='smoothgrad_sq', target=pred_label_idx)
_ = viz.visualize_image_attr_multiple(["original_image", "heat_map"], ["all", "positive"],
                                      np.transpose(attributions_ig_nt.squeeze().cpu().detach().numpy(), (1,2,0)),
                                      np.transpose(transformed_img.squeeze().cpu().detach().numpy(), (1,2,0)),
                                      cmap=default_cmap,
                                      show_colorbar=True)
```

（在此图中，特征归因用积分梯度计算并显示在右侧图像中。图片由 Pixabay 惠允使用。）在 captum.ai 了解更多关于 Captum 的信息。

### CrypTen

通过云端或机器学习即服务（MLaaS）平台应用 ML 带来一系列安全和隐私挑战。尤其是，这些平台的用户可能不愿意或无法共享未加密的数据，这使他们无法充分利用 ML 工具。为应对这些挑战，ML 社区正在探索多种成熟度各异的技术路径，包括同态加密、安全多方计算、可信执行环境、设备端计算和差分隐私。为了更好地理解其中一些技术如何应用，我们发布 CrypTen——一个新的社区型研究平台，推动隐私保护 ML 领域前进。在此了解更多关于 CrypTen 的信息，其 GitHub 地址在此。

## 面向多模态 AI 系统的工具

数字内容通常由多种模态构成，如文本、图像、音频和视频。例如，一条公开帖子可能包含图片、正文、标题、视频和落地页。甚至单个组件也可能有不止一种模态，比如同时包含视觉和音频信号的视频，或由图像、文本和 HTML 源码组成的落地页。与 PyTorch 配合的工具和库生态为构建多模态 ML 系统的挑战提供了增强的应对方式。以下是今天发布的一些最新库：

### Detectron2

物体检测与分割被用于从自动驾驶汽车到平台完整性内容理解等任务。为推进这项工作，Facebook AI Research（FAIR）发布 Detectron2——一个现以 PyTorch 实现的物体检测库。Detectron2 支持最新的模型和任务，提供更高的灵活性以助力计算机视觉研究，并在可维护性和可扩展性上改进以支持生产用例。Detectron2 可在此获取，你可以在此了解更多。

### fairseq 的语音扩展

语言翻译和音频处理是搜索、翻译、语音和助理等系统的关键组件。得益于 transformer 等新架构以及大规模预训练方法的发展，这些领域近来进步巨大。我们扩展了 fairseq（一个用于语言翻译等序列到序列应用的框架），加入对语音和音频识别任务端到端学习的支持。fairseq 的这些扩展让新语音研究想法的探索和原型设计更快，同时提供通往生产的清晰路径。在此开始使用 fairseq。

## 云厂商与硬件生态支持

Amazon Web Services、Microsoft Azure 和 Google Cloud 等云厂商为希望在 PyTorch 上开发 ML 并部署到生产的用户提供了广泛支持。我们很高兴地宣布 Google Cloud TPU 支持正式上线，以及与阿里云的新集成。我们也在扩展硬件生态支持。

**Google Cloud TPU 支持现已广泛可用。**为加速当今部署的最大规模机器学习（ML）应用，并支持未来 ML 应用的快速开发，Google 打造了称为张量处理单元（TPU）的定制芯片。当组装成称为 Cloud TPU Pod 的多机架 ML 超级计算机时，这些 TPU 可以在几分钟或几小时内完成以往在其他系统上需要数天或数周的 ML 工作负载。Facebook、Google 和 Salesforce 的工程师携手在 PyTorch 中启用并试点了 Cloud TPU 支持，包括对 Cloud TPU Pod 的实验性支持。PyTorch 的 Cloud TPU 支持也可在 Colab 中使用。在此了解如何在 Cloud TPU 上开始使用 PyTorch。

**阿里云加入对 PyTorch 的支持。**初始集成包括 PyTorch 1.x 一键解决方案、Data Science Workshop notebook 服务、基于 Gloo/NCCL 的分布式训练，以及与阿里云 IaaS（如 OSS、ODPS 和 NAS）的无缝集成。结合阿里提供的工具链，我们期待显著降低采用门槛，并帮助阿里云的全球客户群利用 PyTorch 开发新的 AI 应用。

**ML 硬件生态扩张。**除关键的 GPU 和 CPU 伙伴外，PyTorch 生态还支持了专用 ML 加速器。来自 Intel 和 Habana 的更新展示了 PyTorch 连接 Glow 优化编译器后，如何让开发者利用这些面向特定市场的方案。

## PyTorch 社区的成长

作为一个开源的、社区驱动的项目，PyTorch 受益于为生态带来新能力的广泛贡献者。以下是近期的一些例子：

- **Mila SpeechBrain** 旨在提供一个基于 PyTorch 的开源一体化语音工具包。目标是开发一个单一、灵活、易用的工具包，用于轻松开发语音识别（端到端与 HMM-DNN）、说话人识别、语音分离、多麦克风信号处理（如波束成形）、自监督学习等许多领域的最先进系统。了解更多
- **SpaCy** 是一个新的封装库，为多个模型提供一致且易用的接口，以提取特征驱动 NLP 管线。支持通过 spaCy 的标准训练 API 提供。该库还计算对齐，使 transformer 特征可以关联回实际单词而非仅仅是词片（wordpiece）。了解更多
- **HuggingFace PyTorch-Transformers**（前称 pytorch-pretrained-bert）是一个面向自然语言处理（NLP）的最先进预训练模型库。该库目前包含 BERT、GPT-2、RoBERTa 和 DistilBERT 等模型的 PyTorch 实现、预训练模型权重、使用脚本和转换工具。它增长迅速，已有超过 13,000 颗 GitHub 星和广泛的用户群。了解更多
- **PyTorch Lightning** 是一个类 Keras 的 PyTorch ML 库。它把核心训练和验证逻辑留给你，其余全部自动化。可复现性是许多研究领域（包括基于 ML 技术的领域）的关键要求。随着提交到 arXiv 和会议的研究论文数量激增至数万篇，扩展可复现性变得困难。了解更多。

我们最近举办了首届线上全球 PyTorch 夏季黑客马拉松，邀请世界各地的研究人员和开发者用 PyTorch 构建创新项目。近 1,500 名开发者参与，提交的项目从牲畜疾病检测到 AI 驱动的金融助理。获奖项目有：

- **Torchmeta**：提供 PyTorch 扩展，简化在 PyTorch 中开发元学习算法。它提供受 TorchVision 启发的统一接口，覆盖小样本分类和回归问题，便于在多个数据集上轻松做基准测试以助可复现性。
- **Open-Unmix**：一个用 PyTorch 做端到端音乐分离开源（demixing）的系统。分离开源把单独的乐器或人声轨从任意立体声录音中分离出来。
- **Endless AI-Generated Tees**：一家提供 AI 生成 T 恤设计的商店，可购买并配送到全球。系统使用用 PyTorch 构建并在现代艺术上训练的最先进生成模型（StyleGAN）。

访问 pytorch.org，了解更多并开始使用 PyTorch 1.3 以及最新的库和生态项目。我们期待社区用 PyTorch 带来的贡献、激动人心的研究进展和真实世界应用。我们要感谢整个 PyTorch 团队和社区对这项工作的所有贡献。

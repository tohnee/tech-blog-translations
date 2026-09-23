---
title: "Facebook 以新伙伴关系和 PyTorch 1.0 的生产能力加速 AI 开发"
title_en: "Facebook accelerates AI development with new partners and production capabilities for PyTorch 1.0"
date: 2018-10-02
source: https://ai.meta.com/blog/facebook-accelerates-ai-development-with-new-partners-and-production-capabilities-for-pytorch-10
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 以新伙伴关系和 PyTorch 1.0 的生产能力加速 AI 开发

> 原文：[Facebook accelerates AI development with new partners and production capabilities for PyTorch 1.0](https://ai.meta.com/blog/facebook-accelerates-ai-development-with-new-partners-and-production-capabilities-for-pytorch-10) · Meta AI（Wayback 存档）

2018 年 10 月 2 日

今年早些时候，我们分享了让 AI 开发更快、更互操作的愿景。今天，在首届 PyTorch 开发者大会上，我们宣布关于不断壮大的软件、硬件和教育伙伴生态的最新消息——他们正在加深对 PyTorch 的投入。我们还将活跃的研究者、工程师、教育者等社区汇聚一堂，分享他们如何在研究和生产中使用这一开源深度学习平台，并深入介绍 PyTorch 1.0 预览版的更多细节。PyTorch 1.0 加速了将人工智能突破性研究推向生产部署的工作流。借助 Amazon、Google 和 Microsoft 更深入的云服务支持，以及与 ARM、Intel、IBM、NVIDIA 和 Qualcomm 等技术提供商更紧密的集成，开发者可以更轻松地利用 PyTorch 兼容软件、硬件和开发者工具的生态。与 PyTorch 1.0 兼容的软硬件越多，AI 开发者就越容易快速构建、训练和部署最先进的深度学习模型。

## PyTorch 1.0 的新特性

该框架的最新增补包括：一个新的混合前端，支持将模型从 eager 模式追踪和脚本化为图模式，以弥合探索与生产部署之间的鸿沟；一个翻新的 torch.distributed 库，支持跨 Python 和 C++ 环境的更快训练；以及一个用于性能关键研究的 eager 模式 C++ 接口（以 beta 版发布）。

目前，研究者和工程师必须在众多框架和工具之间穿梭（其中许多互不兼容），才能完成新深度学习模型的原型设计并将其转移到生产环境中大规模运行。这拖慢了我们以生产规模部署 AI 研究突破的速度。通过这一最新版本，我们将现有 PyTorch 框架的灵活性与 Caffe2 的生产能力相结合，交付了一条从研究到生产就绪 AI 的无缝路径。

## 生态的更深支持

AWS、Google 和 Microsoft 正在通过在其云平台、产品和服务中对框架提供更稳健的支持，加深对 PyTorch 1.0 的投入。例如，Amazon SageMaker——AWS 用于大规模训练和部署机器学习模型的完全托管平台——现在为 PyTorch 1.0 提供预配置环境，包含自动模型调优等丰富能力。Google 宣布在其面向 AI 开发的软硬件工具中推出新的 PyTorch 1.0 集成。Google Cloud Platform 的 Deep Learning VM 提供了带 PyTorch 1.0 的新 VM 镜像，预装 NVIDIA 驱动和教程。Google 还提供 Cloud 张量处理单元（TPU）——为机器学习（ML）定制开发的专用集成电路（ASIC）。Google Cloud TPU 团队的工程师正与我们的 PyTorch 团队积极协作，使 PyTorch 1.0 模型能在这一定制硬件上获得支持。Microsoft——Facebook 在另一项重要 AI 倡议 ONNX 上的早期伙伴——也在进一步履行承诺，在其机器学习产品套件中为 PyTorch 提供一流支持。Azure 机器学习服务现在允许开发者从在本地机器上训练 PyTorch 模型，无缝过渡到在 Azure 云上扩展。面向数据科学实验，Microsoft 提供预装 PyTorch 的预配置数据科学虚拟机（DSVM）。对于希望无需安装软件和配置本地机器就开始探索 PyTorch 的开发者，Azure Notebooks 提供免费的云端托管 Jupyter Notebooks 解决方案，并配置好了 PyTorch 教程。最后，Visual Studio Code 的 Tools for AI 扩展提供 Azure ML 与 PyTorch API 的紧密集成，简化 PyTorch 代码的开发与训练。

除软件和云服务提供商外，技术伙伴——包括 ARM、IBM、Intel、NVIDIA 和 Qualcomm——正通过直接优化、内核库集成，以及对编译器和推理运行时等额外工具的支持，为 PyTorch 1.0 增加支持。这些额外支持确保 PyTorch 开发者能够在广泛的硬件上运行模型——无论是数据中心还是边缘设备——并为训练和推理优化。

## 培养未来的 AI 开发者

我们已经看到各类教育机构使用现有的 PyTorch 框架，在在线课程和大学课程中教授深度学习。该框架的易用性以及与 Python 的深度集成，使学生更容易理解和试验各种深度学习概念。随着 PyTorch 1.0 的演进，我们很高兴更多伙伴将进一步围绕它设计课程。Udacity 正与 Facebook 合作，向开发者提供免费的深度学习入门课程，完全基于 PyTorch 讲授。此外，Facebook 将资助 300 名成功完成这一中级课程的学生，继续在 Udacity 的深度学习纳米学位项目中学习——该项目已翻新为基于 PyTorch 1.0 运行。Fast.ai——提供基于 PyTorch 的入门和进阶深度学习与机器学习免费在线课程——正在宣布 fastai 的首次发布，这是一个构建在 PyTorch 1.0 之上的开源软件库。该库以显著更少的代码提供更高的准确率和速度，让新手和有经验的开发者都更容易使用深度学习。

## 持续协作

我们期待在未来几个月听到社区在使用 PyTorch 1.0 过程中的反馈。我们也期待与深度学习生态的领导者继续合作，帮助更多人利用 AI，加速从研究到生产的路径。要开始使用，请下载 PyTorch 1.0 开发者预览版，或通过我们的某个云伙伴体验它。我们也欢迎整个 PyTorch 社区参加在 facebook.com/pytorch 上的全天直播演讲——演讲者来自 Facebook 的 PyTorch 核心团队，以及学术界、产业界等的贡献者和机构。

我们要感谢整个 PyTorch 1.0 团队对这项工作的贡献。

**作者**

- Joseph Spisak，Facebook 产品经理

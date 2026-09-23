---
title: "PyTorch 开发者生态扩张，1.0 稳定版现已可用"
title_en: "PyTorch developer ecosystem expands, 1.0 stable release now available"
date: 2018-12-07
source: https://ai.facebook.com/blog/pytorch-10-stable-release-now-available
crawled: 2026-09-22
translated: 2026-09-22
---

# PyTorch 开发者生态扩张，1.0 稳定版现已可用

> 原文：[PyTorch developer ecosystem expands, 1.0 stable release now available](https://ai.facebook.com/blog/pytorch-10-stable-release-now-available) · Meta AI（Wayback 存档）

随着 PyTorch 生态和社区凭借面向开发者的有趣新项目和教育资源不断成长，我们今天在 NeurIPS 大会上发布 PyTorch 1.0 稳定版。这一最新版本最初于 10 月的 PyTorch 开发者大会上以预览版形式分享，包含面向生产的特性和主要云平台的支持等能力。研究人员和工程师现在可以充分利用这个开源深度学习框架的新特性，包括在即时执行与图执行模式之间无缝切换的混合前端、翻新的分布式训练、面向高性能研究的纯 C++ 前端，以及与云平台的深度集成。PyTorch 1.0 加速了把 AI 从研究原型带到生产部署的工作流，并让入门更容易、更平易近人。

就在过去几个月里，我们看到初学者通过新的、广泛可得的教育项目快速上手 PyTorch，也看到专家构建创新项目，把框架扩展到从自然语言处理到概率编程的各个领域。

## 不断壮大的 PyTorch 社区

PyTorch 于 2017 年初发布后，很快成为 AI 研究人员的热门选择——他们发现其灵活的动态编程环境和友好的用户界面非常适合快速实验。自那时以来，我们看到这个社区迅速成长。PyTorch 现在是 GitHub 上第二快增长的开源项目，过去 12 个月贡献者增长了 2.8 倍。我们对围绕 PyTorch 形成的社区感到无比兴奋和感激，感谢每一位为代码库做贡献、提供指导和反馈、用这个框架构建前沿项目的人。为此，我们希望通过新的教育项目，继续让开发者更轻松地学习如何用 PyTorch 构建、训练和部署机器学习模型。

## 教育课程把 AI 开发者聚到一起

上个月，Udacity 和 Facebook 推出了新课程「Introduction to Deep Learning with PyTorch」，以及提供继续 AI 教育奖学金的 PyTorch 挑战计划（PyTorch Challenge Program）。仅头几周，我们就看到数万名学生在这个在线项目中积极学习。更重要的是，教育课程开始通过在全球各地（从英国到印度尼西亚）自发形成的真实聚会，让开发者社区更加紧密。完整课程现已通过 Udacity 网站向所有人免费开放，开发者很快还能在更高级的 AI Nanodegree 项目中继续 PyTorch 学习。

除了在线教育课程，fast.ai 等组织还提供软件库，支持开发者学习如何用 PyTorch 构建神经网络。fastai 是一个简化训练快速而准确的神经网络的库，自两个月前发布以来已在 GitHub 上收获 10,000 颗星。看到开发者用这个库取得的成功，我们非常兴奋。例如，Santhosh Shetty 用 fastai 把灾后损害等级分类的此前最佳准确率翻倍；Alena Harley 把肿瘤-正常测序的假阳性率降低到传统方法的 1/7。此外，Jason Antic 创建了名为 DeOldify 的项目，用深度学习为老照片上色和修复。（图片由 Jason Antic 惠允使用。）

## 新项目扩展 PyTorch

PyTorch 已被应用于从图像识别到机器翻译的用例。因此，我们看到开发者社区产出了大量扩展和支持开发的项目，其中一些包括：

- **Horovod**——一个分布式训练框架，让开发者轻松把单 GPU 程序快速放到多 GPU 上训练。
- **PyTorch Geometry**——面向 PyTorch 的几何计算机视觉库，提供一组例程和可微模块。
- **TensorBoardX**——一个把 PyTorch 模型日志记录到 TensorBoard 的模块，让开发者可以用这一可视化工具监控模型训练。

此外，Facebook 的团队也在为 PyTorch 构建并开源项目，例如 Translate——一个基于 Facebook 机器翻译系统、用于训练序列到序列模型的库。对于希望在特定领域快速启动工作的 AI 开发者来说，受支持项目的生态提供了对业界部分最新前沿研究的便捷访问。（关注 @PyTorch 获取最新动态。）我们期待在 PyTorch 持续演进的过程中，看到社区的新项目。

## 在云端上手

为了让 PyTorch 更易获取、更友好，我们持续深化与 Amazon Web Services、Google Cloud Platform 和 Microsoft Azure 等云平台及服务的合作。就在最近，AWS 发布了支持 PyTorch 的 Amazon SageMaker Neo，让开发者可以用 PyTorch 构建机器学习模型，训练一次，然后部署到云端或边缘的任何地方，性能提升最高达 2 倍。开发者现在也可以通过创建新的 Deep Learning VM 实例在 Google Cloud Platform 上试用 PyTorch 1.0。此外，现已正式上线的 Microsoft Azure Machine Learning 服务让数据科学家可以在 Azure 上无缝训练、管理和部署 PyTorch 模型。使用该服务的 Python SDK，PyTorch 开发者可以利用按需分布式计算能力，用 PyTorch 1.0 大规模训练模型，加速通往生产之路。

AI 开发者可以通过云伙伴或本地安装轻松上手 PyTorch 1.0，并在 PyTorch 网站上跟随更新的分步教程，完成「用混合前端部署序列到序列模型」「训练一个简单聊天机器人」等任务。更新后的发布说明也可在 PyTorch GitHub 上查看。我们期待继续与社区协作，并在进一步改进和扩展 PyTorch 深度学习平台的过程中听取你的反馈。我们要感谢整个 PyTorch 1.0 团队对这项工作的贡献。

**作者**

- Zach Devito，Facebook 研究科学家
- Yangqing Jia，Facebook 研究科学家总监
- Dmytro Dzhulgakov，Facebook 软件工程经理
- Soumith Chintala，Facebook 软件工程经理
- Joseph Spisak，Facebook 产品经理

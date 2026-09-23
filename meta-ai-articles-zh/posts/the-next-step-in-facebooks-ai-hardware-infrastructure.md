---
title: "Facebook AI 硬件基础设施的下一步"
title_en: "The next step in Facebook’s AI hardware infrastructure"
date: 2018-03-20
source: https://ai.meta.com/blog/the-next-step-in-facebooks-ai-hardware-infrastructure
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook AI 硬件基础设施的下一步

> 原文：[The next step in Facebook's AI hardware infrastructure](https://ai.meta.com/blog/the-next-step-in-facebooks-ai-hardware-infrastructure) · Meta AI（Wayback 存档）

2018 年 3 月 20 日

机器学习驱动着人们在 Facebook 上体验的诸多方面。我们使用自动语言翻译系统消除沟通障碍，让人们即使说不同语言也能彼此交流。我们的图像分类系统不仅让人们能搜索记录最爱时刻的照片，还通过可以用指尖「阅读」的「会说话的图像」为视障人士提供沉浸式体验。我们还在语音识别、物体与人脸识别、风格迁移、视频理解以及我们应用家族中的许多其他服务中使用机器学习。

鉴于机器学习工作负载的需求不断增长，Facebook 一直致力于通过开源贡献与协作推进人工智能及其各学科的水平。构建前沿平台以支持和加速不断增长的 AI 需求，一直是我们的重点之一。过去几年，我们持续加大数据中心机器学习硬件的投入，专注于加速神经网络在我们产品和服务中的应用。2013 年，我们用 HP SL270s G8 系统开始了为 AI 研究进行的最初部署。我们在数据中心大规模部署 GPU 方面积累了大量经验，并确定了可维护性、散热效率、性能、可靠性和集群管理作为下一代系统的重点方向。随后，我们向开放计算项目（OCP）贡献了两款服务器设计——先是 Big Sur，然后是 Big Basin——并把它们加入了数据中心机群。这些硬件平台已成为 Facebook AI 研究和机器学习服务的骨干。

今天，我们很高兴地宣布硬件创新的下一步——Big Basin v2。

## Big Basin v2 介绍

Big Basin v2 构建在与前代 Big Basin 系统相同的构建模块之上，其模块化设计让我们得以利用并组装现有的开放计算项目（OCP）组件来搭建 Big Basin v2 系统。由于最新一代 NVIDIA Tesla V100 GPU 加速器带来的额外性能，我们还将头节点升级到 Tioga Pass 以获得更强的 CPU 性能，并将 CPU 与 GPU 之间的 PCIe 带宽翻倍。此外，我们升级了 OCP 网卡，为分布式训练工作负载提供额外的网络带宽。经过这些升级，我们不仅观察到单 GPU 性能相比上一代系统提升 66%，还在大规模分布式 GPU 训练中实现了接近线性的性能提升。这使我们的研究和工程师能够构建更大、更复杂的机器学习模型，进一步改善用户体验。

## Facebook 的机器学习流水线

Big Basin v2 是支持 Facebook 机器学习工作流并已通过 OCP 或其他开源计划发布的一系列最先进软硬件平台中的最新一员。Facebook 的大多数机器学习流水线都通过 FBLearner 运行——这是我们的 AI 软件平台，包括 Feature Store、Flow 和 Predictor。Feature Store 从数据中生成特征并送入 FBLearner Flow。Flow 用于基于生成的特征构建、训练和评估机器学习模型。最终训练好的模型随后通过 FBLearner Predictor 部署到生产环境。Predictor 对线上流量进行推断或预测，例如预测某人可能最关心哪些动态、帖子或照片。整个 FBLearner 平台由 Facebook 自研、已发布到 OCP 的硬件驱动：数据存储和 Feature Store 由 Bryce Canyon 支撑；FBLearner Flow 在 Tioga Pass CPU 或 Big Basin v2 GPU 系统上训练模型；FBLearner Predictor 则利用我们的 Tioga Pass 和 Twin Lakes 计算系统。

## 未来硬件设计

为了支撑机器学习工作负载在种类和重要性上的快速增长，Facebook 致力于推进最先进的 AI 基础设施硬件。我们正与合作伙伴共同设计针对训练和推理阶段优化的更高能效系统，重点关注：性能与能效；节点内与节点间通信（支持大规模分布式训练）；以及存储效率与数据本地性（管理机器学习流水线中不断增长的数据量）。我们相信，开放协作有助于促进未来设计的创新，使我们能够构建更复杂的 AI 系统，最终为更沉浸的 Facebook 体验提供动力。

Big Basin v2 的设计规格和相关资料已通过 OCP Marketplace 公开提供。

**作者：**Kevin Lee，Facebook 集团技术项目经理；Xiaodong Wang，Facebook 研究科学家

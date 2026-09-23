---
title: "Facebook AI 与 AWS 合作发布新的 PyTorch 库"
title_en: "Facebook AI, AWS partner to release new PyTorch libraries"
date: 2020-04-21
source: https://ai.meta.com/blog/facebook-ai-aws-partner-to-release-new-pytorch-libraries-
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook AI 与 AWS 合作发布新的 PyTorch 库

> 原文：[Facebook AI, AWS partner to release new PyTorch libraries](https://ai.meta.com/blog/facebook-ai-aws-partner-to-release-new-pytorch-libraries-) · Meta AI（Wayback 存档）

2020 年 4 月 21 日

作为更广泛的 PyTorch 社区的一部分，Facebook AI 和 AWS 的工程师合作开发了面向大规模弹性、容错模型训练以及高性能 PyTorch 模型部署的新库。这些库使社区能够高效地将 AI 模型大规模投入生产，并在模型架构持续增大、愈加复杂之际推进模型探索的最新水平。今天，我们分享这些特性的新细节。

## TorchServe（实验性）

TorchServe 现已可用，它是一个易于使用的开源框架，用于部署 PyTorch 模型以进行高性能推理。该框架与云和环境无关，其库包含多模型服务、日志、监控指标以及为应用集成创建 RESTful 端点等特性。凭借这些特性，TorchServe 为大规模将 PyTorch 模型部署到生产环境提供了清晰的路径。要开始使用，请访问 AWS 新闻博客了解更多信息。

## TorchElastic 与 Kubernetes 的集成（实验性）

Kubernetes 与 TorchElastic 的集成，允许 PyTorch 开发者在可以动态变化而不中断训练任务的计算节点集群上训练机器学习模型。TorchElastic 内建的容错能力使训练即使在该过程中节点宕机时也能继续。这包括服务器维护事件、网络问题或服务器节点被抢占（例如竞价实例的情况）等情形。该框架为开发者提供了原语和接口，使其编写的分布式 PyTorch 作业能以弹性方式在多台机器上运行——而无需开发者手动管理 TorchElastic 训练任务所需的 pod 和服务。该库现已可用。

我们很高兴分享 TorchServe 和 TorchElastic，使社区能够更灵活、更大规模地训练和部署模型。这些库作为 PyTorch 1.5 版本的一部分提供，将由 Facebook 和 AWS 与更广泛的社区合作维护。我们期待继续以新能力服务 PyTorch 开源社区。

**资源：**

- TorchServe 文档
- TorchServe 的 GitHub
- TorchElastic-Kubernetes 文档
- TorchElastic 的 GitHub

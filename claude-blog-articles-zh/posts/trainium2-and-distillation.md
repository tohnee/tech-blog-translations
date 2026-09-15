---
title: "AWS Trainium2 上的 Claude 3.5 Haiku 与 Amazon Bedrock 中的模型蒸馏"
title_en: "Claude 3.5 Haiku on AWS Trainium2 and model distillation in Amazon Bedrock"
source: https://claude.com/blog/trainium2-and-distillation/
crawled: 2026-09-14
translated: 2026-09-14
---

# AWS Trainium2 上的 Claude 3.5 Haiku 与 Amazon Bedrock 中的模型蒸馏

> 原文：[Claude 3.5 Haiku on AWS Trainium2 and model distillation in Amazon Bedrock](https://claude.com/blog/trainium2-and-distillation/) · Claude 博客

作为我们与 AWS 扩大[合作](https://www.anthropic.com/news/anthropic-amazon-trainium)的一部分，我们已开始优化 Claude 模型，让它们运行在 [AWS Trainium2](https://aws.amazon.com/ai/machine-learning/trainium/)——AWS 最先进的 AI 芯片之上。

为了预览 Trainium2 所能实现的可能，Claude 3.5 Haiku 现已支持 [Amazon Bedrock](https://aws.amazon.com/bedrock/claude/) 中的延迟优化推理（latency-optimized inference），让模型显著提速而不牺牲准确性。

我们还在 Amazon Bedrock 中新增了对模型蒸馏（model distillation）的支持，把更大的 Claude 模型的智能带入我们更快、更具成本效益的模型。

### Trainium2 上的新一代模型

我们正与 AWS 合作构建 Project Rainier——一个由 Trn2 UltraServers 组成的 EC2 UltraCluster，包含数十万枚 Trainium2 芯片。这个集群将提供超过五倍于训练我们当前一代领先 AI 模型所用算力（以 exaflops 计）的计算能力。

Trainium2 让我们得以在 Amazon Bedrock 中提供更快的模型，首个是现已在公开预览中支持延迟优化推理的 Claude 3.5 Haiku。启用延迟优化后，Claude 3.5 Haiku 的推理速度最高可提升 60%——这使它成为从代码补全到实时内容审核与聊天机器人等各类使用场景的理想选择。

这个由 Trainium2 驱动的更快版本的 Claude 3.5 Haiku，现已在 US East (Ohio) 区域通过[跨区域推理（cross-region inference）](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)提供，价格为每百万输入 token 1 美元、每百万输出 token 5 美元。

### Amazon Bedrock 模型蒸馏

我们还在让客户能够从 Claude 3 Haiku——我们上一代最具成本效益的模型——中获得前沿性能。借助蒸馏，Claude 3 Haiku 现在可以取得显著的性能提升，在特定任务上达到接近 Claude 3.5 Sonnet 的准确性——而价格与速度仍与我们最具成本效益的模型相同。

这项技术把知识从"教师"（Claude 3.5 Sonnet）迁移到"学生"（Claude 3 Haiku），让客户能以极低的成本运行检索增强生成（RAG）与数据分析等复杂任务。

与传统微调需要开发者手动编写训练样例、持续调整参数不同，Amazon Bedrock 模型蒸馏把整个流程自动化了：

1. 从 Claude 3.5 Sonnet **生成合成训练数据**
2. 对 Claude 3 Haiku 进行**训练与评估**
3. **托管**最终蒸馏出的模型供推理使用

Amazon Bedrock 模型蒸馏会自动应用不同的数据合成方法——从生成相似提示，到基于你的示例提示-响应对创建全新的高质量响应。

Amazon Bedrock 中面向 Claude 3 Haiku 的蒸馏现已在预览中可用。更多信息请参阅 AWS 的[发布博客](https://aws.amazon.com/blogs/aws/build-faster-more-cost-efficient-highly-accurate-models-with-amazon-bedrock-model-distillation-preview/)与[文档](https://docs.aws.amazon.com/bedrock/latest/userguide/model-distillation.html)。

### Claude 3.5 Haiku 降价

除了在 Trainium2 上提供更快的版本，客户仍可继续通过 [Anthropic API](https://console.anthropic.com/workbench)、[Amazon Bedrock](https://aws.amazon.com/bedrock/claude/) 与 [Google Cloud 的 Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) 访问 [Claude 3.5 Haiku](https://www.anthropic.com/claude/haiku)。

为了让该模型能被更广泛的使用场景所用，我们将 Claude 3.5 Haiku 在所有平台上的价格下调至每百万输入 token 0.80 美元、每百万输出 token 4 美元。

### 开始使用

从今天起，模型蒸馏与更快的 Claude 3.5 Haiku 已在 Amazon Bedrock 中开放预览。对于追求价格、性能与速度最优平衡的开发者，现在有了更丰富的 Claude 模型选择：

- 由 Trainium2 驱动、带延迟优化的 Claude 3.5 Haiku，适用于一般使用场景
- 经蒸馏获得前沿性能的 Claude 3 Haiku，适用于高吞吐量、重复性的使用场景

要开始使用，请访问 [Amazon Bedrock 控制台](https://signin.aws.amazon.com/signup?request_type=register)。我们迫不及待想看到你构建的一切。

FAQ（常见问题）

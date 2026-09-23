---
title: "Altana 如何借助 Llama 提升全球价值链管理"
title_en: "How Altana employs Llama to elevate global value chain management"
date: 2025-01-30
source: https://ai.meta.com/blog/altana-value-chain-management-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# Altana 如何借助 Llama 提升全球价值链管理

> 原文：[How Altana employs Llama to elevate global value chain management](https://ai.meta.com/blog/altana-value-chain-management-llama) · Meta AI（Wayback 存档）

2025 年 1 月 30 日 · 阅读约 3 分钟

Altana 利用 AI 帮助企业和政府管理其全球供应链，为从原材料来源到成品销售的扩展供应商与分销网络提供洞察。建立在世界上最大的供应链数据体之上，Altana 驱动着以往不透明的全球网络中的各类工作流。为进一步增强其 AI 能力，这家总部位于纽约布鲁克林的公司在 Databricks 数据智能平台上利用 Llama 开源模型，这加快了产品开发并提升了整体效率。公司预期，一个定制化的 Llama 模型将能够取代多个内部模型，并更好地理解 Altana 的用例。

「借助 Databricks 上的 Llama，公司现在把生成式 AI 系统投入生产的速度提升了 20 倍。」Altana 的 AI 副总裁 Saurabh Khanwalkar 说。目前，Altana 使用 Llama 进行复杂的关税编码分类——基于产品类型和来自其全球供应链地图的图特征，把货运数据映射到 10000 多个海关关税类别。此外，公司正在开发一个基于其历史交互训练的微调聊天机器人，帮助客户轻松选择正确的关税编码。这些创新与 Altana 的使命完美契合：通过微调开源模型使其更快、更聪明地工作，让用户轻松看懂交易。

在调研大语言模型选项时，Altana 选择了 Llama，理由是其准确性、更低的成本以及与 Databricks 的无缝集成。这一设置让 Altana 可以直接在客户的 Databricks 云环境（AWS 或 Azure）内部署定制化 Llama 模型，无需依赖外部 API。团队表示，拥抱开源模型的好处显而易见：更大的灵活性、成本节约，以及便捷获取丰富的开发者文档和在线支持。

## 释放 Llama 的潜力

Altana 的微调流程使用了 Databricks Mosaic AI 训练，部署则通过 Databricks 的服务端点管理。团队使用了简洁的系统提示与用户提示，在大约一百万个输入—输出样本上进行微调。此外，他们还对领域专用数据做了持续预训练，在各种输入—输出格式和多样化用例之间精化指令。

起初，团队注意到，当（训练数据的）回答显得机械、而非使用人类的自然语言时，把 Llama 3.1 8B 微调到客户要完成的任务类型就更具挑战。团队判断，这是因为 Llama 此前只被微调为输出分类结果，因此难以很好地回应开放式问题或聊天。不过，团队通过纳入多种类型的输入和输出克服了这些局限，最终得到的微调模型比其他方案更准确、成本更低。

Altana 微调后的 Llama 模型如今已在生产环境中为零售、服装、汽车等多个行业的客户提供服务。随着客户的使用，模型通过不断精化和扩展系统中嵌入的知识而持续改进。Altana 表示，正是这种开源创新与其深厚供应链专业知识的结合，让他们得以突破 AI 应用的边界，进而推进其使命：帮助企业征服全球供应链挑战。

分享你的 Llama 故事

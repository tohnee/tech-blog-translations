---
title: "宣布 Purple Llama：迈向生成式 AI 新世界的开放信任与安全"
title_en: "Announcing Purple Llama: Towards open trust and safety in the new world of generative AI"
date: 2023-12-07
source: https://ai.meta.com/blog/purple-llama-open-trust-safety-generative-ai
crawled: 2026-09-22
translated: 2026-09-22
---

# 宣布 Purple Llama：迈向生成式 AI 新世界的开放信任与安全

> 原文：[Announcing Purple Llama: Towards open trust and safety in the new world of generative AI](https://ai.meta.com/blog/purple-llama-open-trust-safety-generative-ai) · Meta AI（Wayback 存档）

我们宣布推出 Purple Llama——一个伞形项目，提供开放的信任与安全工具和评估，旨在为开发者拉平竞技场，让他们能按照《负责任使用指南》（Responsible Use Guide）中分享的最佳实践，负责任地部署生成式 AI 模型与体验。作为第一步，我们发布 CyberSec Eval——一套面向 LLM 的网络安全安全评估基准；以及 Llama Guard——一个针对易部署性优化的输入/输出过滤安全分类器。秉持我们的开放路线，我们期待与新近宣布的 AI Alliance、AMD、AWS、Google Cloud、Hugging Face、IBM、Intel、Lightning AI、Microsoft、MLCommons、NVIDIA、Scale AI 等伙伴合作，改进这些工具并将其提供给开源社区。

生成式 AI 带来了前所未有的创新浪潮。借助它，我们可以与对话式 AI 交谈、生成逼真的图像、准确总结大型文档语料——全部只需简单的提示。迄今为止 Llama 模型下载量已超过 1 亿次，这波创新的相当一部分正由开放模型驱动。安全方面的协作将为驱动这波创新的开发者建立信任，并且需要在负责任 AI 上做更多研究和贡献。构建 AI 系统的人不能在真空里应对 AI 的挑战，这正是我们想拉平竞技场、为开放信任与安全创建一个质量中心的原因。今天，我们宣布启动 Purple Llama——一个伞形项目，随着时间推移将汇集工具和评估，帮助社区负责任地使用开放生成式 AI 模型进行构建。初始版本将包含面向网络安全和输入/输出防护的工具与评估，更多工具将在不久之后推出。Purple Llama 项目内的组件将采用宽松许可，同时支持研究和商业用途。我们相信，这是迈向促成社区协作、为生成式 AI 开发的信任与安全工具的标准化开发和使用的重大一步。

## 迈出的第一步

网络安全和 LLM 提示安全是当今生成式 AI 安全的重要领域。我们在自己的第一方产品中优先考虑了这些事项，并在 Llama 2《负责任使用指南》中将其作为最佳实践强调。

### 网络安全

我们正在分享我们所认为的首套全行业范围的 LLM 网络安全安全评估。这些基准基于行业指引和标准（如 CWE 和 MITRE ATT&CK），并与我们的安全领域专家协作构建。通过这一初始版本，我们旨在提供有助于应对白宫关于开发负责任 AI 的承诺中所列部分风险的工具，包括：

- 量化 LLM 网络安全风险的指标。
- 评估不安全代码建议频率的工具。
- 评估 LLM 的工具，使其更难生成恶意代码或协助实施网络攻击。

我们相信这些工具将降低 LLM 建议不安全 AI 生成代码的频率，并降低其对网络对手的助益。我们的初步结果表明，LLM 存在实质性的网络安全风险——无论是推荐不安全代码还是遵从恶意请求。更多细节见我们的 CyberSec Eval 论文。

### 输入/输出防护

正如我们在 Llama 2《负责任使用指南》中所述，我们建议对 LLM 的所有输入和输出按照适合应用的内容准则进行检查和过滤。为支持这一点并赋能社区，我们发布 Llama Guard——一个公开可用的模型，在常见开放基准上具有竞争力，为开发者提供预训练模型，帮助防御潜在风险输出的生成。作为我们对开放透明科学的持续承诺的一部分，我们在 Llama Guard 论文中发布了方法论以及模型表现的深入讨论。该模型在公开数据集的混合上训练，能够检测多种常见类型的潜在风险或违规内容，与诸多开发者用例相关。归根结底，我们的愿景是让开发者能够定制该模型以支持相关用例，让采纳最佳实践变得更容易，并改善开放生态。

## 为什么是紫色？

我们相信，要真正缓解生成式 AI 带来的挑战，需要同时采取攻击（红队）和防御（蓝队）两种姿态。紫队（purple teaming）融合红队与蓝队职责，是评估和缓解潜在风险的协作方式。同样的精神适用于生成式 AI。因此，我们对 Purple Llama 的投入将是全方位的。

## 一个开放的生态系统

对 Meta 而言，以开放方式做 AI 并不新鲜。探索性研究、开放科学和交叉协作是我们 AI 工作的基石，我们相信创造一个开放的生态系统是重要机遇。这种协作心态在 7 月 Llama 2 发布时（拥有超过 100 家伙伴）居于首位，我们很高兴地分享，其中许多伙伴也将与我们合作开放信任与安全，包括：AI Alliance、AMD、Anyscale、AWS、Bain、CloudFlare、Databricks、Dropbox、Google Cloud、Hugging Face、IBM、Intel、Microsoft、MLCommons、Nvidia、Oracle、Orange、Scale AI、Together.AI，以及更多即将加入的伙伴。我们还与 Papers With Code 和 HELM 的伙伴合作，把这些评估纳入他们的基准，同时与 MLCommons AI 安全工作组的合作者携手。我们期待与每一位伙伴以及所有共享「负责任开发的生成式 AI 开放生态系统」愿景的人合作。

## 前进之路

我们将在 NeurIPS 2023 举办一场研讨会，分享这些工具并提供技术深入讲解，帮助大家上手。希望你能参加。我们预期安全指引和最佳实践将是该领域持续的对话，我们希望听到你的意见。我们很高兴继续这场对话、寻找合作方式，并进一步了解哪些领域对你们重要。

## 深入了解更多

- 在 Llama 网站上了解 Llama 2 的更多信息——你可以快速上手并获得常见问题的答案。
- 了解更多关于构建 LLM 驱动产品的最佳实践与考量。
- 关注我们的伙伴 Together.AI 和 Anyscale 在未来几周于 NeurIPS 提供的托管演示。

---
title: "分享全新开源防护工具及 AI 隐私与安全方面的进展"
title_en: "Sharing new open source protection tools and advancements in AI privacy and security"
date: 2025-04-29
source: https://ai.meta.com/blog/ai-defenders-program-llama-protection-tools
crawled: 2026-09-22
translated: 2026-09-22
---

# 分享全新开源防护工具及 AI 隐私与安全方面的进展

> 原文：[Sharing new open source protection tools and advancements in AI privacy and security](https://ai.meta.com/blog/ai-defenders-program-llama-protection-tools) · Meta AI（Wayback 存档）

**要点**

- 今天，我们为开源 AI 社区发布全新的 Llama 防护工具。
- 我们提供新的 AI 驱动解决方案，帮助防御者社区主动检测并保护关键基础设施、系统和服务免受主动攻击。
- 我们还在预览允许 AI 相关请求被私密处理的新技术。

## 面向开源社区的最新 Llama 防护工具

我们致力于为开发者提供构建安全 AI 应用的最佳工具和资源。开发者可访问 Meta 的 Llama Protections 页面、Hugging Face 或 GitHub，获取我们最新的 Llama 防护工具，用于基于 Llama 的构建。

- **Llama Guard 4：**全新的 Llama Guard 4 是我们可定制 Llama Guard 工具的更新版本，作为跨模态的统一防护，支持文本和图像理解的保护。Llama Guard 4 还可在我们的新 Llama API 上使用，该 API 正以限量预览形式推出。
- **LlamaFirewall：**我们介绍 LlamaFirewall——一个安全护栏工具，帮助构建安全的 AI 系统。LlamaFirewall 可以在多个护栏模型之间进行编排，并与我们的防护工具套件协同，检测和防范提示注入、不安全代码、有风险的 LLM 插件交互等 AI 系统风险。关于该工具的更多细节，请参阅 LlamaFirewall 研究论文。
- **Llama Prompt Guard 2：**Prompt Guard 2 86M 是我们 Llama Prompt Guard 分类器模型的更新，改进了越狱（jailbreak）和提示注入检测的性能。我们还推出了 Prompt Guard 2 22M——一个更小更快的版本，与 86M 模型相比，能以最小的性能折中最多降低 75% 的延迟和计算成本。

## 帮助防御者社区在安全运营中用好 AI

在 Meta，我们使用 AI 强化我们的安全系统，抵御潜在的网络攻击。我们从社区听说，他们希望获得能帮助他们做同样事情的 AI 驱动工具。因此，我们分享若干更新，帮助组织评估 AI 系统在安全运营中的效能，并宣布面向精选合作伙伴的 Llama Defenders 计划。我们相信，随着更强大的 AI 模型问世，这是提升软件系统鲁棒性的一项重要工作。

- **CyberSec Eval 4：**我们更新的开源网络安全基准测试套件 CyberSecEval 4 包含新工具——CyberSOC Eval 和 AutoPatchBench——用于评估 AI 系统的防御能力。
- **CyberSOC Eval：**与 CrowdStrike 共同开发的这一框架，衡量 AI 系统在安全运营中心中的效能。今天我们宣布这一基准，即将发布。
- **AutoPatchBench：**一个新基准，评估 Llama 及其他 AI 系统在安全漏洞被利用之前自动修补原生代码漏洞的能力。更多信息见 Engineering at Meta 博客。
- **Llama Defenders 计划：**我们启动 Llama Defenders 计划，帮助合作组织和开发者获取多种开放、抢先体验和封闭的 AI 解决方案，以满足不同的安全需求。
- **自动化敏感文档分类工具：**这是我们在 Meta 内部使用的一个工具，可自动为组织的内部文档应用安全分类标签，帮助防止未授权访问和分发，或从 AI 系统的 RAG 实现中过滤敏感文档。更多信息见 GitHub。
- **Llama 生成音频检测器与 Llama 音频水印检测器：**这些工具专为检测 AI 生成内容而设计，帮助组织检测 AI 生成的威胁，如诈骗、欺诈和钓鱼攻击。发布之际，我们正与 ZenDesk、Bell Canada 和 AT&T 合作，将这些工具集成到他们的系统中。有意了解更多信息的其他组织，可访问 Llama Defenders 计划网站索取资料。

## 构建让 AI 请求得以私密处理的新技术

我们首次介绍 Private Processing——我们的新技术，它将帮助 WhatsApp 用户利用 AI 能力（如摘要未读消息或润色消息），同时保持消息私密，使 Meta 或 WhatsApp 都无法访问。关于我们构建这一技术的安全方法（包括指导我们识别和防御潜在攻击向量的威胁模型）的更多信息，请见我们的工程博客。我们正与安全社区合作审计和改进我们的架构，并将在产品上线前，继续与研究者协作，以开放方式构建和强化 Private Processing。

## 展望

我们希望这里分享的一系列 AI 更新，能让开发者更轻松地基于 Llama 构建，帮助组织加强安全运营，并为某些 AI 用例提供更强的隐私保证。我们期待继续这项工作并在未来分享更多。

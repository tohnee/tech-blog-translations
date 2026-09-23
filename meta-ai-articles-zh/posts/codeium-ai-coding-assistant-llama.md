---
title: "将基于 Llama 构建的 AI 编程助手扩展到数十万用户"
title_en: "Scaling an AI coding assistant built with Llama to hundreds of thousands of users"
date: 2025-01-22
source: https://ai.meta.com/blog/codeium-ai-coding-assistant-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# 将基于 Llama 构建的 AI 编程助手扩展到数十万用户

> 原文：[Scaling an AI coding assistant built with Llama to hundreds of thousands of users](https://ai.meta.com/blog/codeium-ai-coding-assistant-llama) · Meta AI（Wayback 存档）

Codeium 的 AI 编程助手已经受到数十万日活跃用户的喜爱，公司的使命是帮助开发者和组织借助 Codeium 拥有更大的梦想。Codeium 有多种形态，其集成开发环境（IDE）扩展中的 Chat 与 Command 功能在免费和付费产品中均使用了 Llama。

Codeium 的 IDE 插件提供这一功能，让开发者可以与一个理解代码的 AI 对话，覆盖文档编写、代码解释、单元测试等广泛的用例。Codeium Chat 可以生成完整的函数和应用；对于深入陌生代码库的开发者，一键即可解释所需的一切。开发者还可以通过与助手对话来修复缺陷、添加新功能、重构、翻译现有代码或增强视觉效果。Codeium Command 可以直接修改代码，利用 Llama 快速吸收上下文并编写代码，逐行展示差异。

「在每个组织中，编写代码都是一大瓶颈——我们致力于帮助开发者减少个人和业务用例中的瓶颈。」Codeium 业务负责人 Jeff Wang 说，「我们已将 Llama 模型扩展到数十万用户。除了编程效率之外，另一大好处是这些工具显著缩短了员工的上手时间。我们有客户把新工程师的上手周期从三到六个月缩短到了三到六周。」

虽然 Codeium 此前已为客户训练了自己的自动补全和对话模型，但公司发现提供微调过的 Llama 3.1 模型，为其提供了一个可控的、大型通用模型家族的新开源选项。它采用了多个 Llama 3.1 指令变体（70B 和 405B），发现它们在团队关注的零样本任务上表现更好，并且作为微调的基础略具优势。

## 集成 Llama

Codeium 的 Chat 与 Command 集成在用户的集成开发环境中交付这些模型。它对完整代码库建立索引，通过结合检索增强生成与重排序的精细推理方法，提供具备上下文感知的回答。后来，Codeium 发布了「Riptide」，它使用了更加精细的检索机制。面向免费用户的 Codeium Chat 基础模型基于 Llama 3.1 70B；在付费层级，用户可选择不限量使用 Llama 3.1 405B 等对话选项。虽然 Codeium 向企业部署自己的模型，客户也可以自行托管，并可选择这些模型或接入其他生态来使用 Codeium 自托管 Chat。对于 SaaS 用户，Llama 模型的总拥有成本远低于通过 API 运行闭源模型。

「我们已成功用单个 GPU 为数千名工程师提供 Llama 模型服务，甚至还能同时跑其他模型。」Wang 说，「在我们的企业部署中，一块 H100 最多可支持一千名工程师，同一实例中还包括我们自己的自动补全模型。」与合作伙伴的交流表明，Codeium 大规模服务 Llama 的能力是一项竞争优势，这要归功于团队在硬件以及跨模型的上下文和推理流程上实施的各种优化。用于 Codeium 编辑器任务的 Llama 模型比任何可比模型成本低 90%、时延低 3 倍，且更准确。Codeium Chat 后来随其新 IDE 演进为 Cascade。

## Windsurf 与 Cascade

2024 年 11 月下旬，Codeium 发布了 Windsurf——首个真正的智能体（agentic）IDE，也是最早普遍可用的智能体产品之一。Windsurf 中的智能体 Cascade 可以执行多步推理、进行多文件编辑，并代表开发者采取行动。

「通过同时利用 Codeium 既有的深度上下文感知能力，Windsurf 不仅可以从零到一创建应用，还能在生产代码库中进行复杂的多文件编辑，速度快到足以让人始终处于环内、保持心流状态。」创始团队成员 Anshul Ramachandran 说，「为了达到我们想要的时延和质量，我们针对各种任务微调了多个基于 Llama 的模型。这变成了一种神奇的体验，无论是对零编程背景的人还是资深开发者，都能从中受益。」

Windsurf 在短短几个月内增长到数十万日活跃用户，帮助开启了 AI 的智能体时代。

## 展望未来

事实证明，使用开源模型对 Codeium 至关重要。许多任务需要高质量与低时延的结合，因此自主管理完整的模型微调与服务栈必不可少。开源社区为 Codeium 微调与服务栈的不同方面做出了贡献，而 Llama 架构模型的标准化推动了这一进展。

「Llama 开箱即用地提供了一个出色的代码生成模型，并在进一步微调上有很大潜力和灵活性。」Ramachandran 说，「我们始终努力跟随行业的走向，希望随着 Llama 生态持续增长、我们不断尝试构建新产品，Llama 能继续缩小差距。」

分享你的 Llama 故事

---
title: "Zoom 在其 AI 联邦策略中善用 Llama"
title_en: "Zoom leverages Llama in its federated approach to AI"
date: 2024-08-09
source: https://ai.meta.com/blog/llama-zoom-ai-companion
crawled: 2026-09-22
translated: 2026-09-22
---

# Zoom 在其 AI 联邦策略中善用 Llama

> 原文：[Zoom leverages Llama in its federated approach to AI](https://ai.meta.com/blog/llama-zoom-ai-companion) · Meta AI（Wayback 存档）

在 AI 优先的开放协作平台上，Zoom 采用独特的联邦（federated）策略来驱动 Zoom AI Companion——公司的生成式 AI 助手。AI Companion 可在 Zoom Workplace 与商业服务中使用，帮助员工摆脱重复任务。其理念是：生成式 AI 助手负责琐碎事务，让人们把更多时间花在建立联系、协作以及与团队高效产出上。凭借 Zoom 的联邦策略，AI Companion 综合使用 Zoom 自有模型以及闭源和开源大语言模型（包括 Llama），为 Zoom 用户免费提供会议摘要、智能录制和后续步骤——已包含在其符合条件的付费计划中，无需额外费用。

「基础模型让我们的团队能专注于具体用例与客户需求，而不必从零构建模型，加快了 Zoom AI Companion 能力的上市时间，」Zoom CTO 黄学东（Xuedong Huang）说。他表示，独立训练一个像 Llama 这样的高质量开源基础模型，通常可能需要数千块 GPU 的基础设施。构建 AI Companion 时，团队通过创建高质量内部数据集、以微调 Llama 模型与多个闭源模型协同编排的方式解决了这一挑战。由此带来了更高质量的表现，能以更低成本在 AI Companion 负载上胜过规模大得多的闭源模型。团队探索的第一个业务领域，就是用 Llama 构建 AI Companion 的会议摘要能力。自 2023 年 9 月上线以来，已有超过 70 万个账户启用了 AI Companion，且采用率持续上升——会议摘要数量环比翻倍。Llama 还被证明可用于生成训练样本，改进 Zoom 模型组合中其他模型的微调。

## 克服 AI 挑战

黄学东表示，构建 AI 虽然挑战重重，但 Zoom 的联邦策略最大化了性能、质量与经济性。客户安全与隐私是 AI 采用中最重大的考量之一。他补充说，基于基础模型构建，Zoom 赋予客户的能力建立在已被信任的生态之上。通过在联邦策略中纳入 Llama 这类高质量基础模型，Zoom 得以通过「Zoom 托管模型专用」（Zoom-hosted Models Only，ZMO）计划，让客户把数据保留在 Zoom 的安全组织服务器内——这使公司能够服务那些不希望与第三方托管模型共享信息的客户。推理时延是使用 LLM 的另一个挑战。虽然 AI Companion 会议摘要无需实时交付，但随着规模扩大，团队为达成目标投入了更多 AI 基础设施资源，并增加了其他实时用例，如 AI Companion 团队聊天撰写能力。

## 开源带来更开放的市场

使用开源模型益处众多，但黄学东认为最重要的或许是：开源精神在整个行业创造了更公平的竞争场。事实上，这种获取渠道对其他公司——无论规模大小——在跨学科探索、发现新突破时至关重要。托管成本可能不菲，但组织无需维持庞大的科研团队就能用上前沿模型。相反，公司可以通过做自己最擅长的事来汲取开源价值：专注客户需求，微调基础模型以满足客户期望。

---
title: "SAIF CHECK 如何用 Meta Llama 3 验证 AI 模型并建立信任"
title_en: "How SAIF CHECK is using Meta Llama 3 to validate and build trust in AI models"
date: 2024-06-20
source: https://ai.meta.com/blog/saif-check-llama-3-validation-trust
crawled: 2026-09-22
translated: 2026-09-22
---

# SAIF CHECK 如何用 Meta Llama 3 验证 AI 模型并建立信任

> 原文：[How SAIF CHECK is using Meta Llama 3 to validate and build trust in AI models](https://ai.meta.com/blog/saif-check-llama-3-validation-trust) · Meta AI（Wayback 存档）

2024 年 6 月 20 日 · 阅读时长约 4 分钟

随着人工智能日益融入企业运营和日常生活，企业必须意识到潜在风险，并遵守技术所用市场的当地法律。否则可能招致严重后果，包括法律诉讼和高额罚款。

尽管紧跟风险并不容易，却必不可少。总部位于沙特阿拉伯利雅得的 SAIF CHECK 构建了一套使用 Meta Llama 3 的模型评估系统，帮助应对这一挑战。SAIF CHECK 服务于中东和北非的客户，为希望就各类法律、监管、隐私和数据安全风险检查其 AI 模型的公司提供评估、审计和认证服务。公司工作的很大一部分是扫描世界各地的监管环境，然后创建、获取和采购以具体条款描述这些监管环境的文档。SAIF CHECK 再把这些发现整合进其不断增长的知识库，覆盖多个监管领域。

SAIF CHECK 基于 Llama 3 的系统支持对这一综合知识库的快速更新，使机器智能体能够理解客户 AI 模型所处的环境及其监管格局。它支持简单、对话式的查询，通过在大型 AI 法规语料库上训练的检索增强生成（RAG）框架，就人们的监管问题给出相关回答。

「SAIF CHECK 的目标是把模型评估变成一个技术或非技术用户都能完成的对话式工作流。」SAIF CHECK 创始人兼 CEO Shaista Hussain 博士说，「我们把 Llama 3 集成到一个旨在保留客户独特业务上下文（运营国家、监管机构）的系统中，同时从多元来源检索并综合信息。」

## 用 Ghost Attention 保留上下文

Llama 首次引起 SAIF CHECK 团队注意，是他们读到 Llama 2 团队 2023 年发表的论文时。Hussain 说，他们尤其被 Llama 团队解决对话式 AI 系统一个常见问题的思路吸引——这类系统往往在对话过程中丢失上下文。例如，如果你告诉 AI 模型只用俳句回答，几个对话回合后它可能就忘记这条初始指令，除非你在每个新请求时都重复一遍。不得不重复指令会占用宝贵的 token，也限制了对话的总长度。

为解决这一问题，Llama 团队开发了一种名为 Ghost Attention（GAtt）的训练技术，它使用基于人类反馈的强化学习微调模型回应，把初始指令牢记在心。这使得 AI 模型在多轮对话中保持初始指令的能力大幅提升。

「因为我们的 AI 模型评估调查要经过多轮运行处理，我们利用了 Llama 的 GAtt 机制，它有助于跨多轮控制对话流。」Hussain 说，「通过这样做，我们的平台能为用户提供更精确、信息更丰富的回应，提升我们服务的输出质量。」

为了让 Llama 适配自身用例，SAIF CHECK 通过累加式微调流程配置了多个层。使用 Llama 3 Instruct，生成层接收用户的提示和上下文；其输出被送入一个监管分类器——该分类器在来自 SAIF CHECK 综合知识库的各监管机构及国别监管文档上训练。这使模型能够在特定国家和监管机构内对提示和上下文归类。

## 通过伦理对齐获得信心

在进一步了解训练 Llama 所用的负责任 AI 原则后，团队决定改用 Llama 模型做文本生成。Meta 对 Llama 模型做了大量蓝队（blue-team）和红队（red-team）测试，这让 SAIF CHECK 团队确信 Llama 模型与他们的优先事项一致。

「使用 Llama，意味着我们在流程核心使用的是一个在伦理上经过训练、来源清白的模型，因此我们的流程与我们的价值观一致。」Hussain 说。她坦言，在如何正确定位文档、查询文档、并生成契合每个人上下文和具体需求的回应方面，挑战依然存在。「每个机器学习模型都不同，每家公司都以独特的流程部署其模型。」她补充道。Hussain 相信团队的方法——把文档「分块」成更小的内容片段——会取得成功。「我们相信 Llama 是一个出色的模型，可用来验证我们关于分块策略的假设，并监测我们服务回应的有效性。」她说。

## AI 与人机协作的未来

Llama 的负责任接地（grounding）与透明性，对团队的价值观以及他们对 AI 如何产生全球影响的看法至关重要。SAIF CHECK 相信，AI 的真正角色在于补充和增强人类对计算机的使用。要做到这一点，人类需要信任他们所用的 AI 模型。这种信任是 SAIF CHECK 的基石——无论是对其自身的 AI 模型，还是对它为客户验证的模型。「由于 Llama 是开源的，我们能够切实看到它的开发过程，信任它的文档，并确信在理解和把该模型落地到现实服务这件事上，我们并不孤单。」Hussain 说。

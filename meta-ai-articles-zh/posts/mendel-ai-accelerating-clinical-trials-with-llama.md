---
title: "用开源大幅加速临床试验患者匹配"
title_en: "Dramatically accelerating patient-matching in clinical trials with open source"
date: 2025-02-19
source: https://ai.meta.com/blog/mendel-ai-accelerating-clinical-trials-with-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# 用开源大幅加速临床试验患者匹配

> 原文：[Dramatically accelerating patient-matching in clinical trials with open source](https://ai.meta.com/blog/mendel-ai-accelerating-clinical-trials-with-llama) · Meta AI（Wayback 存档）

开源 AI 生态正在改变 Mendel AI 这类组织获取前沿技术、创造社会影响的方式。Mendel AI 是一家领先的临床 AI 平台。借助 Llama 这样的模型，企业可以为特定领域打造量身定制的 AI 解决方案，既无需承担专有系统高昂的前期成本，也不必与模型母公司共享自己的数据——这一点在临床试验这类受到严格监管的行业中尤为重要。

该公司的旗舰产品 Mendel Hypercube 负责处理数据抽象、病历审阅和患者队列分析等临床任务。有了 Llama，Hypercube 还可以用于以自然语言对话和查询，完成试验匹配与患者分组。已有研究表明，为患者匹配临床试验可能需要数百天，导致约 80% 的临床试验无法达成入组目标，而 Hypercube 只需一天即可完成这项工作。Hypercube 将 Llama 与一张临床超图（hypergraph）相结合。该平台允许医疗企业把自己的数据组织在自有云上，构建一个安全且可检索的知识库。

「我们即将在患者疗效方面迈出一大步。」Mendel 创始人兼首席科学官 Wael Salloum 博士说，「开源模型让企业能够专注于自身特定需求，并在其 AI 技术栈中叠加高级推理能力，从而更快地创新。」

## 与 Llama 携手

Mendel 与 Llama 的缘分始于用 Llama 2 微调一个语言用户界面任务，让用户得以与 Mendel 的知识库推理引擎交流，把自然语言问题翻译成其符号查询语言。为打造其医疗专用基础大模型，Mendel 团队基于 8B 和 70B 两种规模的 Llama 3 进行了持续预训练。「我们有多种基于大模型的医疗任务，并针对这些任务在标注数据上对我们的大基础模型持续进行监督微调。」Salloum 说。

其成果是一系列具备指令遵循与上下文学习能力的轻量级模型，它们运行于一个智能体（agentic）框架中，能够对患者病历进行抽象，并在大型患者数据库上回答研究问题。

「随着基础大模型越来越商品化，拥有一个能为初创公司省去初期开发成本的开源版本，是对社会的巨大贡献。」Salloum 说，「创新者可以把时间花在思考如何基于这类模型进行构建上，琢磨客户用例，以及往 AI 技术栈中加入其他非大模型的推理与认知能力。」

展望未来，Salloum 表示 Mendel AI 计划在近期使用多模态的 Llama 3.2。

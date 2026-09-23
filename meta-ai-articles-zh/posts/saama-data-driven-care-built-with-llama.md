---
title: "Llama 如何帮助 Saama 在个性化医疗与数据驱动照护中开辟新可能"
title_en: "How Llama is helping Saama deliver new possibilities in personalized medicine and data-driven care"
date: 2025-01-14
source: https://ai.meta.com/blog/saama-data-driven-care-built-with-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# Llama 如何帮助 Saama 在个性化医疗与数据驱动照护中开辟新可能

> 原文：[How Llama is helping Saama deliver new possibilities in personalized medicine and data-driven care](https://ai.meta.com/blog/saama-data-driven-care-built-with-llama) · Meta AI（Wayback 存档）

2025 年 1 月 14 日 · 阅读时长约 11 分钟

OpenBioLLM——生命科学公司 Saama 推出的一系列经微调的 Llama 模型——简化了可以加速临床试验的任务，并有望为个性化医疗创造新的可能。这些模型生成临床试验方案、临床研究报告及其他必要文件，加速方案生成与数据分析，让可能拯救生命的治疗更早到达患者身边。它们还通过高效的信息处理改进诊断准确性和治疗规划，为医生和患者提供有数据支撑的洞见，帮助他们做出照护决策。

「作为开源模型，OpenBioLLM 可供世界各地的研究者和医疗提供者使用，现实影响十分显著。」Saama 首席技术与 AI 官 Malaikannan Sankarasubbu 说。

Saama 的两个模型——OpenBioLLM-8B 和 OpenBioLLM-70B——利用 Llama 3 的架构，加速从临床试验文档中提取洞见、数据分析、临床方案生成以及医学知识图谱推理。OpenBioLLM 已在生物医学与医疗应用的临床开发中被广泛采用，助力研究与分析、数据管理和运营效率。这些模型可以辅助药物发现并支持基因组学分析。其他研究者也在其基础上开展自己的工作，包括近期在计算语言学协会（ACL）一次会议上发表的一篇论文。「这些切实的影响展示了 AI——具体说是基于 Llama 的模型——如何革命化医疗与健康科学，有望改善患者结局、挽救生命。」Sankarasubbu 说，「我们对开源开发的坚持，让我们得以与更广泛的科学共同体分享进展，促进生物医学 AI 的协作与创新。这些模型正在为高度个性化的医疗照护铺路。」

## 用 Llama 构建复杂用例

Saama 对 Llama 的运用显著演进，扩展到方案生成、医学知识图谱推理和临床试验文档分析等复杂用例。团队为不同医学主题开发了专门模型，并随着 Llama 2 和 3 的发布把模型扩展到 80 亿和 700 亿参数，在各类生物医学任务上的性能显著提升。公司目前正探索多模态应用，把基于 Llama 的模型与医学影像和基因组学数据集成。

为确保在高度监管的医疗环境中做到隐私与合规，Saama 开发了先进的去标识技术和安全数据处理协议，以遵守 HIPAA 等医疗法规。Saama 的内部 AI 研究者会处理出现的任何挑战，确保 OpenBioLLM 保持其最先进生物医学语言模型的地位。团队采用严格的测试协议，并与医学专业人士合作验证模型输出、缓解偏见。

团队为生物医学应用落地 Llama 时，借鉴了 MedMCQA（一个针对真实世界医学入学考试题目的数据集）的经验。两阶段微调流程包含若干关键步骤，包括精选高质量医学指令数据集，以及利用医学专家评估创建直接偏好优化（DPO）数据集。作为微调框架，团队改造了 Hugging Face Transformers 库和 TRL 模块以适应特定生物医学用例。「全面的微调方法让团队得以创建在生物医学任务上表现出色的模型，并在特定基准上超越更大的专有模型。」Sankarasubbu 说，「团队以 Llama 3 作为 8B 和 70B 参数版本的基础模型。」

## 通向成功的开源之路

Saama 于 2017 年开设 AI 研究实验室，与全球才华横溢的开发者和研究者协同创新。Sankarasubbu 把开源视为 Saama 成功的根基。「开源有望革命化生物医学 AI，培育一个更包容、更创新生态，让先进医疗技术大众化。」Sankarasubbu 说。与高校的联系帮助 Saama 的开源项目和论文更实用、更有影响力。公司的知识共享方式包括在顶级会议发表研究论文和开源众多 GitHub 项目，使其得以贡献并受益于全球知识库。主要 AI 厂商也使用了它的开源贡献，包括数据集和基准。

「我们收到的积极回应和认可，坚定了我们对开放研究文化的承诺。」Sankarasubbu 说，「协作方式带来更快的进步，而让开源项目与医学指南保持一致，则确保了医疗 AI 的负责任创新。」

随着 Llama 生态的演进，Saama 预期将基于 Llama 的每次新迭代（包括 Llama 3.1 及未来版本）扩展日常模型升级中的使用。

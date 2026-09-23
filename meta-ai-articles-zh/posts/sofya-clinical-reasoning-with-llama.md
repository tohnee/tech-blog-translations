---
title: "Sofya 如何用 Llama 把临床推理提升到新水平"
title_en: "How Sofya is taking clinical reasoning to the next level with Llama"
date: 2025-03-05
source: https://ai.meta.com/blog/sofya-clinical-reasoning-with-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# Sofya 如何用 Llama 把临床推理提升到新水平

> 原文：[How Sofya is taking clinical reasoning to the next level with Llama](https://ai.meta.com/blog/sofya-clinical-reasoning-with-llama) · Meta AI（Wayback 存档）

2025 年 3 月 5 日 · 5 分钟阅读

当医疗 AI 公司 Sofya 想要创建一套工具，减少医疗服务提供者花在行政任务上的时间——进而让他们有更多时间专注于患者护理时——他们认定开源方式最能支持这一使命。该公司转向 Llama，帮助开发将向更广泛 AI 社区开放的模型和数据集，目标是促进巴西乃至整个拉丁美洲新医疗解决方案的发展。

「我们对 Llama 的使用与 Sofya 的使命一致——作为医疗 AI 专家，通过简化数据结构化和支持临床卓越，充当精准健康的推理引擎。」Sofya 首席执行官 Marcelo Mearim 说。在选择大语言模型时，Sofya 团队看重能力、透明度和性能。他们欣赏 Llama 已经拥有一个活跃的开发者和科学家社区，后者会贡献所学来增强这些模型。「Llama 对不同用例的高度适应性，使其成为面临类似挑战的公司的稳健选择。」Mearim 说。

## 集成 Llama 提供实时解决方案

Sofya 的模型托管在 Oracle Cloud 实例上，并利用 Sglang 和 VLLM 等框架进行模型服务。团队借助 Oracle Cloud、Hugging Face、LangSmith、Sglang 以及开源社区的支持，成功实施了 Llama。Llama 自动执行数据结构化、命名实体识别和问答——提高效率、减少错误，让医疗专业人员得以专注于患者护理。由于 Sofya 必须为客户提供实时解决方案，团队使用了经过微调的较小版本 Llama（如 8B）来增强特定任务的性能，最终得到了毫秒级延迟的 Llama 解决方案。团队用 Llama 405B 进行知识蒸馏，并结合一种自反思（self-reflection）提示工程方法，创建高质量合成数据，用于微调 70B、8B 甚至 3B 等较小的模型。

Llama 对运营和效率的影响带来了 LLM 处理的成本节省、更高的准确性和灵活性。这些模型通过位于巴西的 Oracle Cloud 托管在 Sofya 自己的基础设施上，作为额外的安全增强。自基于 Llama 构建以来，Sofya 看到每次问诊花在文档和行政任务上的时间最多减少了 30%，医疗服务提供者报告了更好的工作流、效率、患者护理结果和客户满意度——平均 CSAT 得分为 90%。得益于 Llama 提升效率和实现更快扩展的能力，Sofya 正朝着每月 100 万次问诊的目标迈进。展望未来，该公司计划推出 Llama 70B 的智能体流程（agent flow），把各种工具和检索增强生成结合起来用于实时使用。

「Sofya.ai 的核心就是让科技与个性化护理更容易融合，」Mearim 说，「我们正在创造一个未来：医疗专业人员可以有更多时间陪伴患者，这一切都归功于自动化和 AI。」

了解更多关于 Sofya 如何用 AI 变革医疗的信息。分享你的 Llama 故事。

订阅我们的新闻邮件，了解 Meta AI 的新闻、活动、研究突破等。加入我们，探索 AI 的无限可能。查看所有开放职位。

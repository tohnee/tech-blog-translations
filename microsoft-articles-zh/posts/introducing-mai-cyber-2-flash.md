---
title: "MAI Cyber 2 Flash：领先的安全能力，更低的成本"
title_en: "MAI Cyber 2 Flash: Leading security. Lower cost"
source: https://microsoft.ai/news/introducing-mai-cyber-2-flash/
site: microsoft
date: 2026-11-17
crawled: 2026-11-19
translated: 2026-11-19
---

# MAI Cyber 2 Flash：领先的安全能力，更低的成本

> 原文：[MAI Cyber 2 Flash: Leading security. Lower cost](https://microsoft.ai/news/introducing-mai-cyber-2-flash/) · Microsoft AI

安全团队需要 AI 全天候发现漏洞、给出修复建议并调查威胁。

要在规模化层面做到这些，需要可观的算力，而成本会迅速累积。

MAI Cyber 2 Flash 构建于微软数十年积累的专有安全数据与专业经验之上，是我们最新的安全专用模型。它在真实世界安全任务上交付领先性能，而成本仅为更大模型的一小部分。我们正把这套能力直接引入微软的安全产品中。

## 以性能验证，以设计提效

在衡量真实世界漏洞发现的基准 CyberGym-E2E[1](#fn-1) 上，MAI Cyber 2 Flash（92.3%）以**每任务不到** **2% 的成本**[3](#fn-3)超越 GPT-6 Astra（91.5%）[5](#fn-5)。在相同推理预算下，它在 CyberGym-E2E 和 WebExploitBench 上也优于 GPT-5.6 Cyber[6](#fn-6)。[2](#fn-2)

它拥有 100 万 token 的上下文窗口，是 MAI Cyber 1.1 Flash 的四倍，能够在复杂的多步调查中分析更多代码库内容。通过 Microsoft Perception 进行的早期评估显示，其在调查 Agent 和安全检测规则编写任务上的性能与领先模型相当。

我们已经看到专用模型在客户环境中能带来什么：Insight Enterprises 在其评估中发现，MAI Cyber 模型比其测试的 GPT 模型 **token 效率高 20%**。[4](#fn-4)

这些结果指向一个更大的机会：把先进安全能力带到更多工作负载中，而不必在每一步都付出运行更大模型的成本。

## **立即开始**

MAI Cyber 2 Flash 将独家登陆微软安全产品，包括代号 MDASH。从 12 月中旬开始，符合条件的客户的 MAI 配置中将自动以它替换现有模型。

**关于这些结果**

*结果反映在特定安全任务与配置上的评估。性能和成本对比会因工作负载、模型配置、推理强度与评估方法而异。*

1. **CyberGym-E2E：**MAI Cyber 2 Flash 的任务成功率为 92.3%，GPT-6 Astra 为 91.5%，且前者使用的推理预算只有后者的一半。
2. **WebExploitBench：**在相同推理预算下，MAI Cyber 2 Flash 达到 40.4%，GPT-5.6 Cyber 为 38.4%。
3. **每任务成本：**基于 CyberGym-E2E 上全部输入、缓存输入和输出 token 按目录价计算（MAI Cyber 2 Flash 每 100 万 token 为 $0.10 / $0.01 / $0.50；GPT-6 Astra Azure OpenAI Global 每 100 万 token 为 $10 / $1 / $50）。该数字反映离线评估成本，而非客户实际支出。
4. **Insight Enterprises：**客户报告称，相比 GPT-5.4、GPT-5.3 Codex 和 GPT-5.4 Mini，MAI Cyber 模型具有 20% 的 token 效率优势。
5. **基准完整性：**在复核 CyberGym-E2E 结果时，我们发现该基准的 905 个任务中有 92 个所依据的开源项目和漏洞报告与我们的部分训练数据相同。基准的参考解法从未用于训练。为保守起见，我们对所有模型都剔除了这 92 个任务，并在其余 813 个任务上报告 CyberGym-E2E 结果。
6. **与 GPT-6 Cyber 的对比：**GPT-6 Cyber 目前仅向部分客户开放，在 Agent 化、使用工具的基准上评估它需要额外的防护措施，而这些措施仍在落实中。我们计划在未来几周分享对比结果。

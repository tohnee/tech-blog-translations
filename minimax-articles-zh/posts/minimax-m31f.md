---
title: "MiniMax M3.1 Flash 正式发布"
date: 2026-10-20
source: https://minimax.io/blog/minimax-m31f
crawled: 2026-10-20
title_en: "minimax-m31f"
translated: 2026-10-20
---

# MiniMax M3.1 Flash 正式发布

> 原文：[minimax-m31f](https://minimax.io/blog/minimax-m31f) · MiniMax

今天，我们正式推出 **MiniMax M3.1 Flash**。

此前在匿名运行期间处理了超过 200 万亿 token 的 Space Bunny 🐰，正是 MiniMax M3.1 Flash 的早期版本。

**作为新一代 Flash 模型，M3.1 Flash 在智能体（agentic）任务、编程、Computer Use 与网络安全上实现了代际飞跃，同时将在线推理速度提升近三倍，并把使用成本降低了 70%。**

### 全面更强的能力

M3.1 Flash 在众多基准上均有提升，在复杂智能体任务（cowork）、计算机操作、软件开发（编程）和网络安全领域达到了领先模型的水准。

**复杂任务与自动化：**

- M3.1 Flash 在 AutomationBench-AA 上名列前茅。它能够跨 SaaS 系统完成真实的企业工作流，端到端地解决销售、市场、运营、客服、财务和人力资源方面的实际问题。
- 它在 BankerToolBench 上取得 76.2 分，擅长应对多步规划、跨文档与文件保持一致性、金融合规以及链式工具调用等复杂的真实世界挑战。

**编程与软件工程：**

- 它在 DeepSWE v1.1 上取得 73.7% 的成绩，跻身顶级模型之列。DeepSWE 聚焦于复杂的软件任务，要求模型独立理解代码、开发功能、修复问题，并通过测试验证自己的工作。M3.1 Flash 在长步骤序列中展现出强大的执行能力，能以更低的成本支撑复杂的软件开发工作流。

**Computer Use（计算机操作）：**

- 它在衡量 AI 计算机操作与跨应用任务执行的 OSWorld V2 上取得 61.7 分，在评估真实专业工作与复杂任务表现的 Agents' Last Exam（ALE）上取得 29.6 分，在两项基准上均位列中国模型第一。
- M3.1 Flash 在与真实环境交互、使用工具、执行长序列任务方面展现出强大能力——从理解任务，迈向付诸行动并交付结果。

**网络安全：**

- 它在 CyberGym 上取得 82% 的优异成绩，展现出漏洞发现与验证方面的领先能力。
- 在我们内部安全专家的深度评估中，该模型在代码审计、漏洞修补、渗透测试、恶意软件分析和逆向工程方面均表现强劲，能够高效、低成本地支撑复杂安全体系的构建。

我们还通过更激进的稀疏化进一步优化了 M3.1 Flash 的推理效率。日常使用中，输出速度可达 200+ TPS（每秒 token 数），中位（P50）速度稳定保持在 170+ TPS。

### 定价：最具性价比

在智能体任务上，该模型的整体使用成本比上一代低 70%。

**每 1M tokens 统一定价：输入 $0.15 · 输出 $0.60 · 缓存输入 $0.015。**

| 模型 | 输入 USD / 1M tokens | 输出 USD / 1M tokens | 缓存输入 USD / 1M tokens |
| --- | --- | --- | --- |
| MiniMax- M3.1-Flash | $0.15 | $0.60 | $0.015 |

### 重新定义智能体任务的能力与成本

在三项基准上——衡量复杂智能体任务执行的 Automation-Bench、衡量真实世界编程的 DeepSWE，以及衡量在具有经济价值的真实任务中进行计算机操作的 Agents' Last Exam（ALE）——M3.1 Flash 以极低的任务成本交付了与顶级模型比肩的性能，为性能与成本树立了极具竞争力的新标准。

**M3.1 Flash 现已可通过 MiniMax API、M Plan 和 MiniMax Code 使用。模型权重将于稍后发布。**

下载桌面版 MiniMax Code：<https://agent.minimax.io/download>

订阅 M Plan：<https://www.minimax.io/m-plan>

API 访问：[platform.minimax.io](https://t.co/fHRdSV73Hr)

Flash 代表着我们在效率与能力平衡上的持续探索。把智能边界继续向前推进的 Pro，也将于稍后到来。

让智能普惠每一个人。

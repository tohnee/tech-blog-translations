---
title: "MAI Code 2 与 Code 2 Flash：以可规模化的价格完成日常编码"
title_en: "MAI Code 2 and Code 2 Flash: Everyday coding at scalable prices"
source: https://microsoft.ai/news/introducing-mai-code-2-and-mai-code-2-flash/
site: microsoft
date: 2026-11-17
crawled: 2026-11-19
translated: 2026-11-19
---

# MAI Code 2 与 Code 2 Flash：以可规模化的价格完成日常编码

> 原文：[MAI Code 2 and Code 2 Flash: Everyday coding at scalable prices](https://microsoft.ai/news/introducing-mai-code-2-and-mai-code-2-flash/) · Microsoft AI

MAI Code 2 与 MAI Code 2 Flash 是两款新的编码模型，专为日常企业编码任务打造，以竞品零头的成本交付领先性能。

## 面向日常编码的性能与速度

在常见企业编码任务上，MAI Code 2 处于性价比前沿，擅长把代码推上生产环境、深度调试、多文件实现、全仓库范围推理以及 UI。在完成这一切的同时，它交付的是代码维护者愿意合并的改动，而成本仅为前沿模型的一小部分。

而 MAI Code 2 Flash 面向高并发量的工作，例如代码解释、定向修改、例行修复和快速迭代，同时以低得多的成本提供质量。

## 不到一半的价格，生产级质量

为了实现最佳性价比，我们构建这些模型时优先考虑客户每天都要做的编码工作。它们明确尚未针对更难的问题进行调优，例如基础科学研究以及超长周期的 Agent 任务。

在四项针对我们在 GitHub Copilot 中看到的日常企业编码任务的常用基准（DeepSWE 1.1、Terminal Bench 2.1、SWE-Atlas 和 FrontierCode v1.1）上取平均，MAI Code 2 以 **40%** 的成本达到 GPT-6.1 Sol **98%** 的性能，以仅 **5%** 的成本达到 Claude Opus 5.5 **96%** 的性能。[1](#fn-1)

MAI Code 2 还针对生成出色的仪表盘和可视化进行了调优，在可视化编码方面表现突出。在盲测前端应用评估中，开发者有 **64%** 的情况更偏好它的结果，而非 GPT-6 Sol。[2](#fn-2)

此外，在衡量日常、高频例行编码任务的三项编码基准上，MAI Code 2 Flash 的性能与 GPT-6 Luna 和 Claude Haiku 5.5 相当，成本分别为后两者的 **65%** 和 **20%**。[3](#fn-3)

## 不止于编码

MAI Code 2 也正在成为微软产品背后的主力。我们在 Code 2 Flash 的基础上进一步优化出单一模型 MAI Work Flash，服务于 Microsoft 365 和 FabricIQ 中的多个微软产品。

**Excel：**在关键的内部 Excel 客户场景基准上，我们的模型在准确率和 token 效率上与 GPT-6 Luna 持平。

**PowerPoint：**在衡量高频 PowerPoint 任务的关键生产基准场景中，我们的模型在质量和 token 效率上均与 GPT-6 Luna 持平。

**Word：**在 5 项关键内部基准上，我们的模型表现与 GPT-6.1 Sol 相近（同时体积显著更小），生产环境中每次调用的输入 token 比 GPT-6.1 Sol 少约 42%。

**Teams：**在跟踪决策、填补知识空白和适配自定义指令方面，我们的模型优于 GPT-6 Luna，在指令遵循和工具调用上最多少用 28% 的 token。

**FabricIQ：**在离线评估中，我们的 MAI 模型在 DAX 查询生成上优于 GPT-5.6 Sol、GPT-6 Astra 和 Claude Opus 5.5——DAX 查询生成是 Power BI 语义模型“用对话查询数据（Chat With Your Data）”背后的核心能力。

## 立即开始

MAI Code 2 与 Code 2 Flash 已在 GitHub Copilot 中可用，Code 2 Flash 已在 [Microsoft Foundry](https://azure.microsoft.com/en-us/products/ai-foundry) 中开放限量访问预览。不久后，我们还将在 OpenRouter、Vercel、Hermes、OpenCode 和 Kilo 上发布这两款模型。

如需了解如何定制 MAI Code 2，请访问我们的[自定义模型页面](/models/microsoft-frontier-tuning/)。

**关于这些结果**
*结果反映在特定编码任务与配置上的评估。性能和成本对比会因工作负载、模型配置、推理强度与定价假设而异。*

1. **MAI Code 2 的性能与价格：**所有模型均在最大推理强度下运行。DeepSWE 1.1、TerminalBench 2.1 和 SWE Atlas 在 MSBench（微软内部评估平台）上使用 GitHub Copilot CLI 运行，未启用子 Agent。FrontierCode 1.1 的分数和成本来自 Artificial Analysis；MAI Code 2 的成本按 50% 促销价计算
2. **可视化编码：**针对 MAI Code 2 与 GPT-6 Sol 的盲测人工并排评估，覆盖用户界面、游戏、数据可视化、3D 场景和 SVG 图形。偏好评判同时涵盖美学与功能，共由 258 名标注员完成
3. **MAI Code 2 Flash 的性能与价格：**所有模型均在最大推理强度下运行。DeepSWE 1.1、TerminalBench 2.1 和 SWE Atlas 在 MSBench 上使用 GitHub Copilot CLI 运行，未启用子 Agent。MAI-Code-2-Flash 的成本按 50% 促销价计算

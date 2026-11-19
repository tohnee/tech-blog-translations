---
title: "MAI Code 2 and Code 2 Flash: Everyday coding at scalable prices"
source: https://microsoft.ai/news/introducing-mai-code-2-and-mai-code-2-flash/
site: microsoft
date: 2026-11-17
crawled: 2026-11-19
---

# MAI Code 2 and Code 2 Flash: Everyday coding at scalable prices

MAI Code 2 and MAI Code 2 Flash: two new coding models built for everyday enterprise coding tasks, delivering leading performance at a fraction of the cost of competing models.

## Performance and speed for everyday coding

MAI Code 2 is at the frontier of price-performance for common enterprise coding tasks and excels in taking code to production, deep debugging, multi-file implementation, repo-wide reasoning, and UI. It does all of this while also delivering changes code maintainers would merge, at a fraction of frontier cost.

Meanwhile, MAI Code 2 Flash is designed for high-volume work such as code explanations, targeted edits, routine fixes, and rapid iterations, while bringing quality at a much lower cost.

## Production quality at less than half the price

To deliver the best price-performance, we’ve built these models to prioritize the coding work our customers do every day. They’re explicitly not yet tuned for harder problems, like fundamental science research and very long-horizon agentic work.

Averaged over four widely used benchmarks that target the everyday enterprise coding tasks we see in GitHub Copilot (DeepSWE 1.1, Terminal Bench 2.1, SWE-Atlas and FrontierCode v1.1), MAI Code 2 gives you **98%** of the performance of GPT-6.1 Sol at **40%** of the cost, and **96%** of Claude Opus 5.5’s performance at just **5%** of the cost.[1](#fn-1)

MAI Code 2 is also tuned for producing great dashboards and visualizations, and excels at visual coding. In blind frontend app evaluations, developers preferred its results over GPT-6 Sol **64%** of the time.[2](#fn-2)

In addition, MAI Code 2 Flash offers comparable performance to GPT-6 Luna and Claude Haiku 5.5 at **6****5%** and **20%** of the cost, across three coding benchmarks measuring day-to-day, high-volume routine coding tasks.[3](#fn-3)

## Beyond coding

MAI Code 2 is also becoming the workhorse behind Microsoft products. From Code 2 Flash, we further optimized a single model, MAI Work Flash, to serve multiple Microsoft products across Microsoft 365 and FabricIQ.

**Excel:** Our model is on par for accuracy and token efficiency with GPT-6 Luna across key internal Excel customer-scenario benchmarks.

**PowerPoint:** On key production benchmark scenarios that measure frequent PowerPoint tasks, our model performs on par with GPT-6 Luna in both quality and token efficiency.

**Word:** Our model performs similarly to GPT-6.1 Sol (while being significantly smaller) on 5 key internal benchmarks using ~42% fewer input tokens per call than GPT-6.1 Sol in production.

**Teams:** Our model beats GPT-6 Luna at tracking decisions, filling knowledge gaps, and adapting to custom instructions using up to 28% fewer tokens on instruction following and tool calling.

**FabricIQ:** In offline evaluation runs, our MAI model outperforms GPT-5.6 Sol, GPT-6 Astra, and Claude Opus 5.5 at DAX query generation, the core capability behind “Chat With Your Data” for Power BI semantic models.

Get started

MAI Code 2 and Code 2 Flash are available in GitHub Copilot, and Code 2 Flash is in limited-access preview in [Microsoft Foundry](https://azure.microsoft.com/en-us/products/ai-foundry). Soon, we’ll be releasing them on OpenRouter, Vercel, Hermes, OpenCode, and Kilo.

Learn more about customizing MAI Code 2 on our [Custom Models page.](/models/microsoft-frontier-tuning/)

**About these results**  
*Results reflect evaluations on specific coding tasks and configurations. Performance and cost comparisons vary by workload, model configuration, reasoning effort, and pricing assumptions.*

1. **MAI Code 2 performance and price:** All models were run at max reasoning effort. DeepSWE 1.1, TerminalBench 2.1, and SWE Atlas were run on MSBench (Microsoft’s internal eval platform) with the GitHub Copilot CLI without subagents. FrontierCode 1.1 scores and costs are from Artificial Analysis; MAI Code 2 cost is shown at its 50% promotional price
2. **Visual coding:** Blind human side-by-side evaluations of MAI Code 2 and GPT-6 Sol across user interfaces, games, data visualizations, 3D scenes, and SVG graphics. The preference covers both aesthetics and functionality, and is annotated by a total of 258 annotators
3. **MAI Code 2 Flash performance and price:** All models were run at max reasoning effort. DeepSWE 1.1, TerminalBench 2.1, and SWE Atlas were run on MSBench with the GitHub Copilot CLI without subagents. MAI-Code-2-Flash cost is shown at its 50% promotional price

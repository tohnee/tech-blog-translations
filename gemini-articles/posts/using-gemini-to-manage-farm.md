---
title: "How Gemini Flash agents are helping a Michigan dairy farmer"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/using-gemini-to-manage-farm/
site: gemini
date: 2026-07-28
authors: News from Google Team
crawled: 2026-09-13
---

Dairy farming operates on tight margins, making data analysis essential for managing complex biological and environmental variables. Since modern farms generate massive volumes of information, the challenge lies in analyzing it quickly to make decisions. That’s why Paul Windemuller turned to Gemini 3.6 Flash.

In 2014, Paul and Brittany started Dream Winds Dairy in Michigan with 30 leased cows. Over 12 years, it grew into a highly automated facility milking 260 Holsteins. As a 2024 Nuffield International Farming Scholar studying ag tech and AI, Paul approaches dairy farming as a technological challenge.

His operations generate continuous data streams: sensor collars track each cow, a local weather station records climate metrics, and an online portal logs milk quality and shipments.

However, these systems operate in isolated software silos. Every morning, Paul spent hours downloading files, merging spreadsheets, and calculating performance. This kept him away from actually looking after the cows.

## Delegating the office work to AI agents

![Dashboard Overview](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image1_4m3x82y.width-1200.format-webp.webp)

To reclaim his time, Paul built a local, multi-agent AI system using [Gemini 3.6 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) inside [Google Antigravity](https://antigravity.google/) to integrate siloed farm data and calculate daily profitability.

Instead of APIs or web scraping, the system uses a local, directory-based file-interface. When CSV data exports or photos of papers receipts, PDFs, and invoices are saved to a monitored folder, Gemini’s multimodal power extracts and merges visual and numeric metrics — keeping data under Paul’s control.

A specialized multi-agent workflow replaces long prompts with specialized, orchestrated roles:

- **Orchestrator:** Manages the overall daily workflow.
- **Ingestion Agents:** Standardize raw files (milking robot exports, feed logs).
- **Analysis Agent:** Evaluates biological and weather impacts.
- **Reporting Agent:** Generates clear, natural language summaries.

The system automatically transforms raw files into a cohesive business overview.

## Leveling the playing field for small businesses

Ultimately, Paul’s ambition is to empower independent farmers with technology they can use to streamline their operations the same way he has been able to for his own business. Not only is building the tool a hurdle for many, but once they have them, operating at farm scale was a cost challenge that needed to be solved.

The daily agentic workflows that require continuous reasoning, parsing, and tool execution have been too expensive for small businesses like his. [Gemini 3.6 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) helped make Paul's daily operation more cost-effective.

Designed for advanced reasoning, tool use, and coding, Gemini 3.6 Flash features a 1 million token context window and a 64,000 token maximum output. [Benchmark evaluations](https://artificialanalysis.ai/models/gemini-3-6-flash) show it achieves roughly a 17 percent reduction in output tokens compared to Gemini 3.5 Flash, at a lower cost per output token, significantly lowering the cost of running agentic loops.

## Measuring success by Static Variable Margin

The system is designed to optimize for Paul’s primary metric: Daily Static Variable Margin (SVM). Unlike traditional metrics like Income Over Feed Cost, which fluctuates with volatile milk and feed prices, SVM holds market prices constant, isolating the true biological and operational efficiency from market noise. This grounds the agentic system in a truth Paul can rely on to give him actionable insights for farm operations.

![Various Feeding & Economics graphs](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image2_9p9esCS.width-1200.format-webp.webp)

## How the agentic workflow calculates SVM

- **Biological Performance**: Ingestion agents parse milk yields, components (butterfat/protein), somatic cell count, and feed.
- **Static Revenue**: Applies fixed prices based on historical pay standards ( Federal Order 33 January prices) to actual milk solids produced.
- **Static Feed Cost**: Uses fixed ingredient prices to isolate changes in actual feed volume consumed.
- **Static Income Over Feed Cost**: Subtracts the static feed cost from static revenue.
- **Variable Costs**: Subtracts per-cow expenses (replacements, breeding, vet supplies) while excluding overhead (labor, utilities, depreciation), ensuring SVM changes reflect only biological efficiency and health.

## Generating the Daily Briefing

Calculating numbers is only half the battle. Busy farmers don’t have time to decode spreadsheets every morning at 3:00 AM. To save time, the reporting agent translates results into a daily Farm CEO Briefing that isolates daily margin drivers. For example, if SVM drops by $0.15 per cow, it pinpoints specific causes:

- **Dry Matter Intake**: -$0.08 ( humidity reduced feed intake)
- **Somatic Cell Count**: -$0.04 (slight increase indicating potential health issues)
- **Discarded Milk**: -$0.03 (two cows entered the treatment pen)

It ends with actionable recommendations, such as adjusting ventilation for heat stress. Since the system runs on local file exports, all sensitive data stays on the farm.

## Scaling independent businesses beyond the spreadsheet

Paul’s agentic system built in Antigravity highlights a major shift for small businesses, which he hopes can inspire and teach others how they may evaluate using AI in their daily workflows. By pairing multi-agent architecture with the low cost token efficiency of Gemini 3.6 Flash, he built an automated operating layer that eliminates hours of manual spreadsheet work, allowing him to step out of the office, and focus on growing his business.

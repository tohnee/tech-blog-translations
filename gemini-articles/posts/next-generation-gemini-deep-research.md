---
title: "Deep Research Max: a step change for autonomous research agents"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/
site: gemini
date: 2026-04-21
authors: Lukas Haas
crawled: 2026-09-13
---

[In December](https://blog.google/innovation-and-ai/technology/developers-tools/deep-research-agent-gemini-api/), we released the Gemini Deep Research agent to developers via the [Interactions API](https://blog.google/technology/developers/interactions-api), giving developers access to Google’s most advanced autonomous research capabilities. Today, we are taking these capabilities to the next level with two new evolutions of our autonomous research agent: Deep Research and Deep Research Max.

With the integration of our most advanced model, Gemini 3.1 Pro, Deep Research has transformed from a sophisticated summarization engine into a foundation for enterprise workflows across finance, life sciences, market research, and more. Deep Research’s reports offer value on their own, but also serve as the first step in complex, agentic pipelines which often start with in-depth context gathering. With a single API call, developers can now trigger exhaustive research workflows that for the first time blend the open web with their proprietary data streams to deliver professional-grade, fully cited analyses.

## Choose a research configuration that fits your workflow

Building upon our initial release of Gemini Deep Research, we’re introducing two distinct agents designed to match your needs ranging from direct user assistance to large-scale, offline research processes:

- **Deep Research:** Optimized for speed and efficiency, this new agent replaces our preview release from December and delivers significantly reduced latency and cost at higher quality levels. It is the ideal agent for research experiences integrated directly into interactive user surfaces where lower latency is desired.
- **Deep Research Max:** Designed for maximum comprehensiveness and highest-quality synthesis, Max leverages extended test-time compute to iteratively reason, search and refine the final report. It is the perfect engine for asynchronous, background workflows such as a nightly cron job triggering the generation of exhaustive due diligence reports for an analyst team by morning.

Deep Research Max represents a leap in performance across industry-standard benchmarks tracking retrieval and reasoning capabilities.

![Deep Research Max represents a leap in performance across industry-standard benchmarks tracking retrieval and reasoning capabilities.](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/gemini-3.1-pro_deep-research-and-max_blog_evals.png)

## Unlock proprietary data and rich native visuals

Deep Research can now search the web, arbitrary remote MCPs, file uploads and connected file stores — or any subset of them — introducing capabilities designed to handle the complex, gated data universes that professionals rely on daily.

- **Model Context Protocol (MCP) support:** You can now seamlessly connect Deep Research to your custom data and specialized professional data streams (such as financial or market data providers) securely via MCP. Deep Research supports arbitrary tool definitions which transforms it from a web searcher into an autonomous agent capable of navigating any specialized data repositories.
- **Native charts and infographics:** A first for Deep Research in the Gemini API, our agent no longer just creates text; it natively generates high-quality charts and infographics in-line with HTML or [Nano Banana](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/), dynamically visualizing complex data sets to enrich analytical reports.

![Fiat Currency Winners and Losers: YoY Performance vs. USD (April 2025 - April 2026)](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_1.png)

Deep Research natively generates rich visual elements, turning complex qualitative and quantitative data streams into presentation-ready charts and infographics.

![The Unpausable 4-Year Clock of the FIG Regime](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_2.png)

Deep Research natively generates rich visual elements, turning complex qualitative and quantitative data streams into presentation-ready charts and infographics.

![Payments Infrastructure Dominates European Fintech Capital Allocation](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_3.png)

Deep Research natively generates rich visual elements, turning complex qualitative and quantitative data streams into presentation-ready charts and infographics.

![Global Energy Trade Reconfiguration: Primary Maritime Detours (2024-2026)](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_4.png)

Deep Research natively generates rich visual elements, turning complex qualitative and quantitative data streams into presentation-ready charts and infographics.

We’ve also expanded the agent's capabilities to provide more control and transparency over the research process:

- **Collaborative planning:** Review, guide and refine the research plan generated by the agent before it begins execution, providing granular control over the investigation's scope.
- **Extended tooling:** Combine the full suite of Gemini API tooling. Run Deep Research with Google Search, remote MCP servers, URL Context, Code Execution and File Search simultaneously — or turn off web access entirely to exclusively search over your custom data.
- **Multimodal research grounding:** Provide a combination of PDFs, CSVs, images, audio and video as input to ground the agent's research in your custom context.
- **Real-time streaming:** Track the agent's intermediate reasoning steps with live thought summaries, and receive text and image outputs as they are generated, particularly useful for interactive user surfaces.

## Drive real-world results with expert-grade analysis

Deep Research Max delivers highly comprehensive reports, rigorous factuality and expert-grade analysis cheaper and more efficiently than ever before. Compared to our December release, Deep Research Max consults significantly more sources and identifies critical nuances the older release frequently overlooked. We have also focused on teaching Deep Research to consult a diverse array of sources and carefully weighing conflicting evidence against each other. The result is a nuanced report that draws from authoritative sources like SEC filings and open-access peer-reviewed journals, lays out information well and transforms dense technical data into actionable, stakeholder-ready formats.

![Win-rates of Deep Research 4/26 vs. Deep Research 12/25 on an internal Deep Research expert eval](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/gemini-3.1-pro_deep-research-qualitative-advacements_blog_evals.png)

To make sure this tech delivers real-world results, we’re working closely with startups and enterprises in specialized and regulated fields where there is little margin for error, particularly in finance and the life sciences. For example, we are actively collaborating with [FactSet](https://www.factset.com/), [S&P Global](https://www.spglobal.com/ratings/en) and [PitchBook](https://pitchbook.com/) on their MCP server designs to let shared customers integrate financial data offerings into workflows powered by Deep Research, and to enable them to realize a leap in productivity by gathering context using their exhaustive data universes at lightning speed.

## Take advantage of proven Google scale performance

When you build with the Deep Research agent, you are tapping into the same autonomous research infrastructure that powers research capabilities within some of Google’s most popular products like [Gemini App](https://gemini.google/overview/deep-research/), [NotebookLM](https://blog.google/technology/google-labs/notebooklm-deep-research-file-types/), [Google Search](https://blog.google/products/search/google-search-ai-mode-update/#deep-search) and [Google Finance](https://blog.google/products/search/new-google-finance-ai-deep-search/).

## Get started with Deep Research in the Interactions API

Deep Research and Deep Research Max are available starting today in public preview via paid tiers in the Gemini API. Head over to our [developer documentation](https://ai.google.dev/gemini-api/docs/deep-research) to start building with Deep Research using the [Interactions API](https://blog.google/technology/developers/interactions-api). Deep Research and Deep Research Max will also soon be available to startups and enterprises in Google Cloud.

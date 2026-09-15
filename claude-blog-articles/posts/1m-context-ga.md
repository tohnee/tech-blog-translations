---
title: "1M context is now generally available for Opus 4.6 and Sonnet 4.6"
date: 2026-03-13
source: https://claude.com/blog/1m-context-ga/
crawled: 2026-09-14
---

Claude Opus 4.6 and Sonnet 4.6 now include the full 1M context window at standard pricing on the Claude Platform. Standard pricing applies across the full window — $5/$25 per million tokens for Opus 4.6 and $3/$15 for Sonnet 4.6. There's no multiplier: a 900K-token request is billed at the same per-token rate as a 9K one.

**What's new with general availability:**

- **One price, full context window.** No long-context premium.
- **Full rate limits at every context length.** Your standard account throughput applies across the entire window.
- **6x more media per request**. Up to 600 images or PDF pages, up from 100. Available today on Claude Platform natively, Microsoft Foundry, and Google Cloud’s Vertex AI.
- **No beta header required.** Requests over 200K tokens work automatically. If you're already sending the beta header, it's ignored so no code changes are required.

**1M context is now included in Claude Code for Max, Team, and Enterprise users with Opus 4.6.** Opus 4.6 sessions can use the full 1M context window automatically, meaning fewer compactions and more of the conversation kept intact. 1M context previously required extra usage.

### **Long context that holds up**

A million tokens of context only matters if the model can recall the right details and reason across them. Opus 4.6 scores 78.3% on MRCR v2, the highest among frontier models at that context length.

Claude Opus 4.6 and Sonnet 4.6 maintain accuracy across the full 1M window. Long context retrieval has improved with each model generation.

That means you can load an entire codebase, thousands of pages of contracts, or the full trace of a long-running agent — tool calls, observations, intermediate reasoning — and use it directly. The engineering work, lossy summarization, and context clearing that long-context work previously required are no longer needed. The full conversation stays intact.

Claude Code can burn 100K+ tokens searching Datadog, Braintrust, databases, and source code. Then compaction kicks in. Details vanish. You're debugging in circles. With 1M context, I search, re-search, aggregate edge cases, and propose fixes — all in one window.

Before Opus 4.6's 1M context window, we had to compact context as soon as users loaded large PDFs, datasets, or images — losing fidelity on exactly the work that mattered most. We've seen a 15% decrease in compaction events. Now our agents hold it all and run for hours without forgetting what they read on page one.

Opus 4.6 with 1M context window made our Devin Review agent significantly more effective. Large diffs didn't fit in a 200K context window so the agent had to chunk context, leading to more passes and loss of cross-file dependencies. With 1M context, we feed the full diff and get higher-quality reviews out of a simpler, more token-efficient harness.

Eve defaults to 1M context because plaintiff attorneys' hardest problems demand it. Whether it's cross-referencing a 400-page deposition transcript or surfacing key connections across an entire case file, the expanded context window lets us deliver materially higher-quality answers than before.

Scientific discovery requires reasoning across research literature, mathematical frameworks, databases, and simulation code simultaneously. Claude Opus 4.6’s 1M context and expanded media limits let our agentic systems synthesize hundreds of papers, proofs, and codebases in a single pass, helping us dramatically accelerate fundamental and applied physics research.

With Claude's 1M context, an in-house lawyer can bring five turns of a 100-page partnership agreement into one session and finally see the full arc of a negotiation. No more toggling between versions or losing track of what changed three rounds ago.

Large-scale production systems have endless context, and production incidents can get very complex. With Claude's 1M context window, we are able to keep every entity, signal, and working theory in view from first alert to remediation without having to repeatedly compact or compromise the nuances of these systems.

We raised our Opus context window from 200k to 500k and the agent runs more efficiently — it actually uses fewer tokens overall. Less overhead, more focus on the goal at hand.

Real-world spreadsheet tasks require deep research and complex multi-step plans. Claude's 1M context window let’s us maintain task adherence and attention to detail.

### **Getting started**

1M context is available today on the Claude Platform natively and through Amazon Bedrock, Google Cloud’s Vertex AI, and Microsoft Foundry. Claude Code Max, Team, and Enterprise users on Opus 4.6 will default to 1M context automatically.

See our [documentation](https://platform.claude.com/docs/en/build-with-claude/context-windows) and [pricing](https://platform.claude.com/docs/en/about-claude/pricing) for details.

‍

FAQ

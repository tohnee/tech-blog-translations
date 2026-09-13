---
title: "GLM-5.3-Flash Architecture Notes"
source: https://sebastianraschka.com/blog/2026/glm-5-3-flash-architecture-notes.html
crawled: 2026-09-06
---

# GLM-5.3-Flash Architecture Notes

Now we know: The popular Ox Alpha LLM was GLM-5.3-Flash…

Compared to GLM-5.2, this new GLM-5.3-Flash model uses:

- a Kimi Linear-style 3:1 (super\*) hybrid attention pattern with 34 Kimi Delta Attention layers (KDA) and 11 Multi-head Latent Attention (MLA) / DeepSeek Sparse Attention (DSA) layers;
- a scaled-down GLM-5.2-style sparse MoE backbone, going from 744B-A40B to 320B-A18B;
- a DeepSeek V4-style mHC residual path with four parallel streams;
- plus a native vision encoder (not shown).

I called it a “super hybrid” above because both KDA and MLA/DSA are “efficient” components. E.g., Kimi only uses KDA + full attention MLA, DeepSeek V3.2 uses DSA + full attention MLA.

PS: I’m sorry for the excessive tech jargon. Explainers on all these components (MLA, DSA, KDA, mhC, etc.) in my [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/).

PPS: Haha, maybe justification for getting that pricey Mac Studio M5 Ultra 256 GB / 512 GB to run this locally…

![Composite figure showing the GLM-5.3-Flash architecture with Kimi Delta Attention, multi-head latent attention with DeepSeek Sparse Attention, mHC residual streams, and benchmark comparisons](https://sebastianraschka.com/images/blog/2026/glm-5-3-flash-architecture-notes/glm-5-3-flash.webp)

Figure 1. GLM-5.3-Flash architecture and release-time benchmark comparisons. See [GLM-5.3-Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-3-flash) in the architecture gallery for additional details.

Source: website version of my [Substack note](https://substack.com/@rasbt/note/c-323088504).

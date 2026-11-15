---
title: "Open October LLM Architecture Roundup"
source: https://sebastianraschka.com/blog/2026/open-october-llm-architecture-releases.html
crawled: 2026-11-16
---

# Open October LLM Architecture Roundup

Catching up on the 10 (!) open LLM architecture releases from the past month. Quite a lot happened in October.

I guess we can call it “Open October”!

1. Kolibri-1 (78B): A notable model from Germany. Features classic Grouped Query Attention (GQA) and Sliding Window Attention (SWA) attention module.
2. Ling 3.1 Flash (560B): Uses Kimi Delta Attention and the eighth uses gated Multi-head Latent Attention (MLA) inspired by DeepSeek.
3. Muse Spark Open (816B): Besides Muse Glimmer, the first major open weight release from Meta (since Llama). Uses classic GQA + SWA but adds a LatentMoE.
4. Nemotron 3.5 Super VL (120B): Combines Mamba-2 layers with just eight attention layers. Also LatentMoE
5. Dory1.0 (4B): A looped transformer design.
6. Reflection Beam (501B): GQA+SWA architecture.
7. Recursive Flint (40B): Note that “Recursive” is the company name; the architecture is a fairly standard MoE with GQA and SWA.
8. MiniMax M3.1-Flash (428B): Uses their own MiniMax Sparse Attention module.
9. LFM3 (1.7B): Hybrid architecture that mixes short convolutions and attention.
10. Mistral Large 4 (1T) combines MLA with sparse attention.

I plan to cover/discuss things in more depth in my next Substack article in the coming weeks!

[![Composite figure with architecture diagrams and fact sheets for ten October LLM releases, from Kolibri-1 to Mistral Large 4](/images/blog/2026/open-october-llm-architecture-releases/open-october-architectures.webp)](/images/blog/2026/open-october-llm-architecture-releases/open-october-architectures.png)

[Architecture diagrams and fact sheets](/llm-architecture-gallery/) for the ten October releases. Click the figure to view the full-resolution image.

Source: lightly edited website version of my [Substack note](https://substack.com/@rasbt/note/c-377610833).

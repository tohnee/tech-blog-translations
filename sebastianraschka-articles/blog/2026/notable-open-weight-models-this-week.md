---
title: "Six Open-Weight Model Architecture Notes"
source: https://sebastianraschka.com/blog/2026/notable-open-weight-models-this-week.html
crawled: 2026-09-06
---

# Six Open-Weight Model Architecture Notes

Yes, open-source / open-weight models are important for a healthy AI ecosystem. That’s how we can verify things, check claims, and keep up outside the closed labs. Plus, it gives us the freedom to run AI on our own hardware if we are not ready to share personal data and IPs with closed labs through using their models. (Not that proprietary models are bad, actually I use them a lot as well, but it wouldn’t be healthy not to have any alternatives.)

Anyway, while pretty much everyone is waiting for the Kimi K3 and Ling 3.0 weights to land on the model hub any day now, there were quite a few other interesting new open-weight model releases the past week. Yes, one of those weeks!

So, here are the architecture pics along with some notes on what I found most interesting:

1) Nanbeige 4.2 3B uses [looped depth sharing](https://sebastianraschka.com/glossary/#looped-depth-sharing "Looped Transformer"). This basically means it runs the same 22-layer (=transformer block) stack twice. So, it extends the 22-layer architecture to 44 layers, but without duplicating the weights. (2x the transformer block compute but same memory footprint.)

Why? The info is a bit sparse, but section 2.1 of the Nanbeige 4.2 technical report says two passes gave the best trade-off and retained about 75% of the token efficiency of a standard architecture. More passes gave barely any gains but made the training much slower and much more expensive.

2) Laguna S 2.1 is poolside’s Laguna model in a really nice size: 118B sparse MoE with 8B active parameters and a 1M-token [context window](https://sebastianraschka.com/glossary/#context-length "Context Length"). Otherwise, the architecture is pretty standard. It uses 36 sliding-window and 12 global (gated-)GQA layers. However, given this size, and the fact that it (just barely) runs on my DGX Spark (uses less than 80 GB of RAM), this is right now the most interesting model for me personally. It’s 3x bigger and thus a tad slower but maybe a good candidate as daily-driver-Qwen3.6-35B-replacement. (Still waiting on some more independent performance benchmarks though.)

3) Motif-3-Beta is a new 314B-A13B sparse MoE that is somewhat based on DeepSeek V4 in terms of mHC and [latent attention](https://sebastianraschka.com/glossary/#mla "Multi-Head Latent Attention (MLA)"). But it uses a new component, Grouped Differential Latent Attention, which is inspired by Multi-head Latent Attention. I probably should write an article about this some time, but for now, the tl;dr is as follows. Regular MLA compresses the keys and values into a smaller latent representation to mainly reduce the KV cache size. GDLA does a similar low-rank compression but puts the attention heads into groups and also learns a noise head for each group where the noise gets subtracted for filtering purposes… Anyway, a topic for another day!

4) Solar Open 2 is a new 250B-A15B hybrid MoE by Upstage that interleaves three Kimi Delta Attention layers with one [GQA](https://sebastianraschka.com/glossary/#gqa "Grouped-Query Attention (GQA)") layer.

5) Antares 1B is a small model (and there is also an even smaller 0.3B variant) from Cisco that starts with the IBM Granite 4.0 1B backbone and uses SFT plus [GRPO](https://sebastianraschka.com/glossary/#grpo "GRPO (Group Relative Policy Optimization)") for terminal-based cybersecurity stuff. It is a nice example of task-specific post-training on a genuinely small model.

6) BTL-3 is a rank-32 LoRA adapter for Qwen3.6-27B aimed at coding agents and structured tool use. The really strong [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") performance suggests that LoRA adapters are still a useful tool/technique in 2026.

I added all six to the [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) for some additional details.

![Composite figure showing architecture diagrams for Nanbeige 4.2, Laguna S 2.1, Motif-3-Beta, Solar Open 2, Antares 1B, and BTL-3, plus Laguna S 2.1 speed and memory charts](https://sebastianraschka.com/images/blog/2026/notable-open-weight-models-this-week/hero.webp)

Figure 1. Architecture diagrams for the six models, followed by Laguna S 2.1 throughput and memory measurements.

Source: lightly edited website version of my [Substack note](https://substack.com/@rasbt/note/c-302083551).

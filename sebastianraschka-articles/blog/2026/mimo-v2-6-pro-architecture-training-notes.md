---
title: "MiMo-V2.6 Pro Training Notes"
source: https://sebastianraschka.com/blog/2026/mimo-v2-6-pro-architecture-training-notes.html
crawled: 2026-09-23
---

# MiMo-V2.6 Pro Training Notes

Xiaomi’s new MiMo-V2.6 Pro is “simply” the best (for now). Despite its simple architecture design it’s currently No.1 in the open-weight benchmarks (weighted average).

With “simple,” I mean a classic [Grouped Query Attention (GQA)](https://sebastianraschka.com/llm-architecture-gallery/gqa/) with [Sliding Window Attention (SWA)](https://sebastianraschka.com/llm-architecture-gallery/swa/) at a tiny 128-token window size.

So, that underlines one of the points I’ve been trying to make in recent months: most of the progress still comes from the data and post-training recipe improvements. Fancy [attention variants](https://magazine.sebastianraschka.com/p/visual-attention-variants) are just mostly efficiency tweaks.

What are some of the training data improvements and recipe improvements? The MiMo team shared a pretty detailed [technical report](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL/blob/main/MiMo_V2_6_technical_report.pdf). Lots to carefully digest there, but in short, there are a few things that stood out:

1. An increase in agent tasks; also training across different harnesses (the average DeepSWE pass@1 accuracy on held-out harnesses improved from approximately 50% -> 66%).
2. Better reward signals: they replaced a simple correctness verifier with an agentic grader that looks at the execution traces as well.
3. Large [RL](https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training) batches (1,568 prompts × 16 rollouts = 25,088 trajectories) and 2.7–3.7 billion training tokens per update (unclear, though, what the predecessor used).

![Composite figure comparing MiMo-V2.6 Pro and DeepSeek V4-Pro architectures, Artificial Analysis Intelligence Index scores, and output speeds](https://sebastianraschka.com/images/blog/2026/mimo-v2-6-pro-architecture-training-notes/mimo-v2-6-pro-comparison.webp)

MiMo-V2.6 Pro and DeepSeek V4-Pro architectures, with release-time Artificial Analysis Intelligence Index and output-speed comparisons.

Source: website version of my [Substack note](https://substack.com/@rasbt/note/c-343108099).

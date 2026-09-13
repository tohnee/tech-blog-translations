---
title: "Inkling Architecture and Benchmark Notes"
source: https://sebastianraschka.com/blog/2026/inkling-architecture-benchmark-notes.html
crawled: 2026-09-06
---

# Inkling Architecture and Benchmark Notes

Thinking Machines Lab released [Inkling](https://thinkingmachines.ai/news/introducing-inkling/), a 975B-parameter open-weight Mixture-of-Experts (MoE) model. It activates 41B parameters per token and supports a [context window](https://sebastianraschka.com/glossary/#context-length "Context Length") of up to 1,048,576 tokens.

Those numbers put Inkling in the same general size class as Kimi K2.5 and GLM-5.2. Yet the architecture has several details I have seen less often, including short convolutions inside every decoder block and a learned relative-position bias in place of [RoPE](https://sebastianraschka.com/glossary/#rope "Rotary Positional Embeddings (RoPE)").

![Inkling architecture diagram and release benchmark comparisons with GLM-5.2, Nemotron 3 Ultra, Kimi K2.5, GPT 5.6 Sol, and Claude Fable 5](https://sebastianraschka.com/images/blog/2026/inkling/hero.webp)

Figure 1: Inkling architecture and release-time [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") comparisons. The left panel summarizes the 975B MoE and its local-global attention pattern. The benchmark panels use results published by Thinking Machines Lab on July 15, 2026. All Inkling results use an effort setting of 0.99. A larger architecture figure is available in the [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/#card-inkling).

## The 41B active footprint

Inkling has 66 decoder layers with a hidden size of 6,144. The first two layers use dense feed-forward blocks. The remaining layers contain 256 routed experts and 2 shared experts. Each token selects 6 routed experts, and both shared experts are always active.

This works out to an active ratio of about 4.2%. For comparison, GLM-5.2 has 744B total and 40B active parameters, while Kimi K2.5 has 1T total and 32B active parameters. Inkling is therefore close to GLM-5.2 in active size despite having 231B more total parameters.

Inkling is also a native multimodal model. Images and video frames pass through a four-layer hMLP, while audio uses the dMel representation introduced by Thinking Machines Lab. The resulting representations enter the same decoder as text, and the model produces text output.

## Local and global grouped-query attention

Of the 66 decoder layers, 55 use sliding-window attention and 11 use global attention. This gives Inkling a repeating 5-to-1 local-global pattern. The local layers have a 512-token window and use 64 query heads with 16 key-value heads, a 4-to-1 [grouped-query attention (GQA)](https://sebastianraschka.com/glossary/#gqa "Grouped-Query Attention (GQA)") ratio. The global layers retain 64 query heads but use only 8 key-value heads, increasing the GQA ratio to 8 to 1.

The unusual part is the [positional information](https://sebastianraschka.com/glossary/#positional-encoding "Positional Encoding"). Inkling skips RoPE and instead computes a learned, input-dependent relative-position bias from the query and key states. It also applies RMS normalization to the query and key heads before attention.

The bias covers the full 512-token span in local layers. In global layers, its configured extent is 1,024 tokens. Tokens farther back can still be attended to, but they receive no explicit learned relative-position term. This detail is easy to miss when reading only the release post. It is visible in the [configuration](https://huggingface.co/thinkingmachines/Inkling/blob/main/config.json) and the [Transformers implementation](https://github.com/huggingface/transformers/blob/main/src/transformers/models/inkling/modular_inkling.py).

## Four short convolutions per layer

Each decoder layer contains four causal convolutions with a kernel size of 4. Two operate directly after the key and value projections. The other two process the attention and [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") branch outputs before those outputs join the residual stream.

These small convolutions give the block an explicit path for mixing information over nearby tokens. The release does not include an ablation that isolates their effect, so it is unclear how much of Inkling’s quality or training stability comes from this choice.

There is one more normalization detail. A separate [RMSNorm](https://sebastianraschka.com/glossary/#rmsnorm "Root Mean Square Layer Normalization (RMSNorm)") is applied directly after the token embedding lookup, before the first decoder block. This embedding normalization is enabled in the released configuration and appears as a distinct operation in the implementation.

## Training and effort control

Thinking Machines Lab reports 45T [pretraining](https://sebastianraschka.com/glossary/#pretraining "Pretraining") tokens spanning text, images, audio, and video. The training setup uses Muon for the model’s large matrix parameters and Adam for the remaining parameters. Weight decay is coupled to the square of the learning rate.

Post-training began with supervised fine-tuning on synthetic data from open-weight teacher models, including Kimi K2.5. Most of the post-training compute then went into reinforcement learning across synthetic and human-created environments. According to the release, the team collected more than 30 million RL rollouts.

One practical outcome is an effort control. A system message tells Inkling how much effort to spend, while a per-token cost during training encourages shorter or longer answers. This is useful for trading output length against benchmark performance without maintaining separate checkpoints.

## A mixed benchmark snapshot

The reported GLM-5.2 comparison illustrates Inkling’s overall benchmark profile. Inkling scores 79.8 on IFBench versus 73.3 for GLM-5.2, and 43.9 versus 38.1 on SimpleQA Verified. GLM-5.2 leads on HLE without tools at 40.1 versus 29.7, SWE-Bench Pro Public at 62.1 versus 54.3, and Terminal-Bench 2.1 at 82.7 versus 63.8.

I would treat these as a release-time snapshot. All Inkling results use an effort setting of 0.99 and a [temperature](https://sebastianraschka.com/glossary/#temperature "Temperature") of 1.0. The coding evaluations allow trajectories up to 256K tokens. Several comparison values come from external reports, while Inkling’s Terminal-Bench result uses an internal harness. Small gaps across such setups are hard to interpret.

The release also shows effort sweeps rather than a single operating point. On Terminal-Bench, Thinking Machines Lab reports that Inkling reaches the Nemotron 3 Ultra score while generating about one-third as many tokens. This is a useful result, although a provider-level throughput comparison would still require the same quantization, batch size, expert-parallel setup, attention kernels, and hardware.

For me, the open questions are now quite concrete. I would like to see controlled ablations for the short convolutions, embedding normalization, and relative-position bias. I would also like directly comparable throughput measurements against Kimi K2.5 and GLM-5.2. Those results would clarify whether Inkling’s architecture choices mainly improve quality, long-context behavior, training stability, or serving efficiency.

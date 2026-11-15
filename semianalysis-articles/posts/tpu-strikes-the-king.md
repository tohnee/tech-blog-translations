---
title: "The Iron(wood) Throne: Google's TPU Stakes Its Claim on Inference"
subtitle: "Viable Alternative of CUDA Moat, NVIDIA Working Nights & Weekends, Jensen’s Counter Submission, Kimi K3, Meta Muse Spark Open, GLM5.3, TorchTPU, SGLang, vLLM, llm-d, Ray"
date: 2026-11-05
source: https://newsletter.semianalysis.com/p/tpu-strikes-the-king
crawled: 2026-11-16
authors: ["Bryan Shan", "Alec Ibarra", "Cam Quilici", "Kimbo Chen", "Wenyao Gao", "Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
---

# The Iron(wood) Throne: Google's TPU Stakes Its Claim on Inference

**Viable Alternative of CUDA Moat, NVIDIA Working Nights & Weekends, Jensen’s Counter Submission, Kimi K3, Meta Muse Spark Open, GLM5.3, TorchTPU, SGLang, vLLM, llm-d, Ray**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

In November 2025, [we published a newsletter saying that Google is selling TPUs](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the) to external customers. Since then, we have been proven right over and over again with Oracle, [OpenAI](https://openai.com/careers/software-engineer-tpu-compilers-san-francisco/), Anthropic, and Meta all becoming customers of TPUs just as our [Accelerator Model](https://semianalysis.com/accelerator-hbm-model/) reported.

Hardware demand is only half the story, as NVIDIA’s moat has historically been its software and large developer ecosystem. This is where TPU is also making headway, partnering with upstream maintainers across the entire ecosystem, including the Meta PyTorch team, vLLM (Inferact, RedHat), SGLang (RadixArk), llm-d, Ray, etc. [This is not a surprise to folks that have read our September 2026 article laying out Google TPU’s externalization strategy](https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam).

Back in our September article, we published the first third-party TPUv7 results on InferenceX on single-turn workloads, showing that in an apples-to-apples FP8 comparison on Qwen 3.5 397B, TPUv7 Ironwood) delivered up to 50% better performance per dollar than B200 and B300.

We also reported that many Google TPU customers were asking for AgentX results, since long-context, multi-turn agentic serving is where inference spend is heading.

Previously, Jensen went on the [Dwarkesh Podcast](https://www.youtube.com/watch?v=Hrbq66XqtCo) and commented on the fact that no other chips were taking advantage of their opportunity to show performance on InferenceX.

![](https://substack-post-media.s3.amazonaws.com/public/images/2155d462-261a-4ab4-95f9-9231e9380d34_3840x2160.png)
*Source: Dwarkesh (Dylan’s Cousin) Podcast*

Six months later, and indeed Google is taking full advantage of this opportunity.

Today we are releasing the first official long-context, multi-turn, realistic agentic inference benchmark results on TPUv7 across four models, showing that TPUv7 is either competitive on perf per dollar for external customers or delivers the best state-of-the-art result:

- **Muse Spark Open SGLang AgentX (NVFP4 weights):** Competitive TPU performance per dollar result even though the architecture was co-designed for GPUs. Submitted by OSS ecosystem developer, RadixArk (Makers of SGLang).

- **GLM-5.2 vLLM AgentX (FP8):** TPUv7 is the cheapest FP8 option, delivering 1.2x to 2.7x the tokens per dollar of B200, B300, and MI355X from 60 to 300 tok/s/user. NVIDIA NVFP4 still beats TPUv7 FP8, but with accuracy / quality loss.
- **Qwen3.5 vLLM AgentX (FP8):** With llm-d disaggregated serving, TPUv7 beats GB300 FP8 at every interactivity level and restores parity even against GB300 FP4 at higher quality / accuracy.
- **Kimi K3 vLLM AgentX (MXFP4 weights):** Competitive with GB300 NVL72 at launch; With TPUv7 delivering 1.15x to 2.5x the tokens per dollar of GB200, B200, B300, and MI355X. Submitted by vLLM OSS ecosystem developer, Inferact.

This was benchmarked on InferenceX/AgentX, the industry-standard inference benchmark supported by almost every major buyer of compute, from Microsoft Azure to Oracle to Meta and many more. Furthermore, it has the support of the ML community, including vLLM, LMCache, SGLang, PyTorch, and Huggingface, and the support of major labs like OpenAI, MiniMax, ZAI, Qwen, Moonshot Kimi, etc.

Google potential TPU customers and current TPU customers are asking Google for AgentX results because of how realistic the AgentX benchmark is and how similar it is to their real inference workload. [For our SemiAnalysis supply chain shipment estimates on TPUv8i, TPUv8t, TPUv9, TPUv10, check our Accelerator Model for full quarter by quarter breakdown of shipments.](https://semianalysis.com/accelerator-hbm-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/5810db06-2805-45bf-bfa0-8b3a3e47684c_1080x731.png)
*Source: InferenceX*

[Star the InferenceX GitHub repository if you find the open-source benchmark and data useful!.](https://github.com/SemiAnalysisAI/InferenceX) InferenceX is the only inference benchmark in the world to have TPUv7, OpenAI Jalapeño, Nvidia Rubin NVL72, AMD, and soon, SambaNova and Trainium2/3.

![](https://substack-post-media.s3.amazonaws.com/public/images/d65268ce-9719-4232-94b5-d1f47289d2bc_1496x633.png)
*Source: InferenceX*

# Recommendation to Jensen

NVIDIA only [occasionally loses to AMD on some model/scenarios](https://x.com/SemiAnalysis_/status/2116606900271788210), but TPUs delivering better performance per dollar or competitive performance per dollar is a new experience that NVIDIA senior leadership is unwilling to accept. As soon as TPU posted its first AgentX result on Qwen3.5 397B FP8 showing that even TPUv7 FP8 could beat GB300 NVL72 FP4, NVIDIA tasked a strike force of human engineers and agent swarms to work 997, late into the night until 2am local time and on weekends, across USA and mainland China. [Unfortunately for NVIDIA, their first GB300 FP4 counter submission is still 1.64x worse per dollar than TPUv7 FP8 for external customers across most of the curve.](https://x.com/SemiAnalysis_/status/2112258243372146742) We do think that with enough agent swarms, NVIDIA could regain a slight performance lead on GB300 NVL72 FP4 vs TPUv7 FP8, but on NVIDIA FP8 versus TPUv7 FP8, we believe that it is not possible for NVIDIA to regain SOTA for certain models.

One thing we hear a lot from open-source maintainers in PyTorch and NVIDIA customers is that there is a lot of bureaucracy; simple things, like adding a new feature to the NVIDIA driver to support a certain feature for PyTorch CudaGraph capture, have been stuck in “internal NVIDIA legal review” for three months. It makes little sense for lawyers to be the blocker for technical driver features. We have seen similar challenges when trying to get NVIDIA to add features like improving ConnectX, NVSwitch, HGX Board (Vulcan, Umbriel) DCGM power telemetry, where it takes a while just to get the timeline for the timeline. In comparison, [startup mindset companies like AMD (under the leadership of Anush, Ramine, Vamsi, Lisa)](https://github.com/ROCm/rocm-systems/pull/12724) can rapidly develop these features.

There needs to be an cultural shift in massively reducing bureaucracy at NVIDIA. This is one of the biggest risks to NVIDIA Moat that Jensen has to tackle. In our experience and many customers experience, Nvidia is now slower moving than AMD, Google, and Amazon to external suggestion, git commits, and feedback.

That being said, certain teams at NVIDIA are cutting through the bureaucracy, [such as the NVIDIA ex-CentML vLLM team](https://x.com/SemiAnalysis_/status/2111627094878790023). AMD and [TPUs](https://github.com/Inferact/tpu-megakernels) [added innovative Megakernel decode support to open source popular production inference engine](https://x.com/SemiAnalysis_/status/2109841575547211955). Within a week, they were able to defend the NVIDIA by [rapidly adding and merging Megakernel support too (PR approved by AMD vLLM maintainer).](https://github.com/vllm-project/vllm/pull/61867)

TPU is making big headway into the ecosystem, and multiple models, like Day 0 Meta’s Muse Spark Open support and [Kimi K3.1 Pro already has day 0 TPU support](https://llm-d.ai/blog/deploy-kimi-k3-1-pro-with-llm-d), as it applies the NVIDIA playbook of giving open-source maintainers lots of chips. **In contrast, NVIDIA’s contribution of clusters to community maintainers has increasingly been wrapped in DMV style bureaucracy and stingy at best. For a $5 trillion company, one would expect NVIDIA to be more liberal in contributing resources to OSS developers who work for free on improving the NVIDIA stack. We hope Jensen figures out how to eliminate the bureaucracy slowing progress.**

In comparison, AMD has been increasingly less stingy and providing the upstream vLLM, TileRT, SGLang, Tokenspeed, etc. maintainers liberal access to clusters and rapdily increasing the CI fleet without miminal levels of bureaucracy.

![](https://substack-post-media.s3.amazonaws.com/public/images/78c1bfee-bc21-46e5-bb7f-1abfe8ac31fe_2048x1065.png)
*Source: vLLM Dashboard*

# Meta’s Muse Spark Open FP4 816B on SGLang TorchTPU Agentic Inference Performance

Meta is one of the early adopters of TPU and is already deploying TPUv7 in production using SGLang-TorchTPU.

![](https://substack-post-media.s3.amazonaws.com/public/images/c660c650-cffd-48cd-84b4-1572debb9545_946x676.png)
*Source: Meta*

Muse Spark Open is Meta’s latest 816B-parameter open model, and it is one of the launch models for SGLang-TorchTPU. On InferenceX’s agentic inference workload, a submission from RadixArk, a community developer and a lead maintainer of SGLang, shows that TPUv7 is competitive for decode performance per dollar even when using the cost basis of what Meta would pay when buying TPUs. For production inference, Meta uses SGLang for LLM inference and uses vLLM for RL training rollouts. When looking at end-to-end latency, TPUv7 still needs improvements to be competitive, such as continuing to optimize its prefill kernels. For decode kernels, TPUv7 SGLang is using a fully fused megakernel, which eliminates kernel launch latency. Furthermore, the submission uses SGLang HiCache CPU DRAM offloading using Google’s open-source, TPU native [TPU-Sync](https://github.com/google/tpu-sync) library at high concurrency in order to improve prefix cache hit rates.

![](https://substack-post-media.s3.amazonaws.com/public/images/3b56ac59-ae8d-4abf-8db0-b0c5bb376c0a_918x731.png)
*Source: SemiAnalysis & RadixArk*

Note that Muse Spark Open is an extremely GPU-optimized model, and, in theory, not friendly to TPUs at all. This is due to Muse Spark Open’s 64 head dim, which means that for long-context attention, 25% of the systolic array is padded.

In comparison, GPU matrix cores consume small tiles, so a wide range of head dimensions, expert widths, and post-sharding KV head counts all land near peak. A dimension of 64 instead of 128 pays close to nothing on an H100 or a B200 and gets a cheaper attention layer for it. GPU architecture allowed researchers to prioritize evaluation performance without a loss in inference performance.

This is quite interesting as TPUs can get quite competitive performance on a model that is extremely unfriendly to TPUs. Note that AI labs with lots of TPU capacity, such as Anthropic and Google Deepmind and soon OpenAI, typically co-design their models such that the attention shapes would fit nicely on TPUs to avoid this issue.

![](https://substack-post-media.s3.amazonaws.com/public/images/523e5780-f129-497f-91b3-5c740d895932_1876x976.png)
*Source: SemiAnalysis*

When TPUs see model architecture with attention head_dim=256, they go full lambo mode.

![](https://substack-post-media.s3.amazonaws.com/public/images/9b869a08-8df1-47f8-975f-8e411c754af9_848x473.png)
*Source: Mario Kart*

Great work to the RadixArk team on this amazing achievement! They are actively working on updating the documentation such that everyone can get access to this optimized SGLang Muse Spark Open TPU configuration. We expect more AgentX results from RadixArk soon, showing that its SGLang-TorchTPU stack is production-ready.

# GLM5.2 / 5.3 vLLM AgentX FP8 Agentic Inference Performance

GLM-5.2/5.3 is a frontier open model. It is an MoE transformer with 744B parameters and roughly 39B active per token. The model supports a 1M-token context through DeepSeek Sparse Attention (DSA): a lightweight indexer scores prior tokens, and full attention runs over only the 2,048 selected tokens for each query.

For FP8, TPUv7 is the cheapest way to serve GLM-5.2 AgentX. From 60 to 300 tok/s/user, it delivers **1.2x to 2.7x the tokens per dollar of B200, B300, and MI355X at FP8**, and 4.4x that of H200 at 150 tok/s/user.

![](https://substack-post-media.s3.amazonaws.com/public/images/e15bad2d-730d-4116-89f8-3a16fc0e14da_981x737.png)
*Source: SemiAnalysis*

## FP4 GPUs Still Lead on Perf per Dollar

Because GLM-5.3 was not natively QAT with block scale FP4, FP4 has a slight accuracy drop compared to FP8. FP4 GPUs still deliver more tokens per dollar at most speeds, as TPUv7 has no native FP4 support, and we will need to wait until Q1 2027 for TPUv8 with FP4 support, as tracked in our [Accelerator & HBM Mode](https://semianalysis.com/accelerator-hbm-model/)l. At 100 tok/s/user, GB300 and GB200 FP4 deliver 3.6x and 3.5x the tokens per dollar of TPUv7. FP4 halves the bytes per weight, and small batch decode is memory bound.

![](https://substack-post-media.s3.amazonaws.com/public/images/3831cb69-f06e-4ce5-872b-cf533cc951bf_875x733.png)
*Source: SemiAnalysis*

The [SemiAnalysis AI Cloud & TCO Model provides a comprehensive breakdown of pricing across all accelerators](https://semianalysis.com/ai-cloud-tco-model/) currently on InferenceX, as well as many more, including future SKUs such as Nvidia Rubin Ultra and Feynman, AMD MI400 through MI700, Google TPU v8 through v12, and AWS Trainium3 through Trainium6.

[Get Access](https://semianalysis.com/ai-cloud-tco-model/#contact)

## GLM-5.3 Optimizations

GLM-5.3 AgentX contexts reach 1M tokens with over 90% of each request already cached, so KV cache capacity sets how many users fit. There are four main changes:

1. GLM-5.3’s attention reads one shared compressed KV entry per token, so splitting attention heads across devices would copy the whole cache to every device. Decode context parallelism (DCP) splits it by sequence position instead and merges partial attention results every layer.

![](https://substack-post-media.s3.amazonaws.com/public/images/8f037375-fc9a-4f62-8084-dedc4b6cfc52_1720x766.png)
*Source: SemiAnalysis & Google*

2. Each query reads only the 2,048 cache entries an indexer selects. TPUv7’s SparseCores, built for scattered memory access, pick those entries and gather them while the TensorCore runs the attention math.
3. TPUv7 uses registers that are 8 rows by 128 lanes. Data must be packed into them, which can fragment. The 128 indexer key bytes plus the scale byte add up to 129, one byte more than a 128-wide row, so the old layout rounded it up to 256. The new layout turns it sideways: tokens now run along each row, and each token’s key runs down 32 four-byte rows, plus one more row for the scale. That comes to 132 bytes, and only 3 of them are wasted.

![](https://substack-post-media.s3.amazonaws.com/public/images/1ae04378-b44c-451e-88ac-5e6f771932ff_1606x1332.png)
*Source: SemiAnalysis & Google*

4. One fused kernel runs routing; the experts, the all-reduce, and the attention merge become a single collective. TPU programs are compiled for fixed shapes, so Google added 4- and 8-token shapes for small decode steps, which had been padded to 16.

# Qwen3.5 397B AgentX

Two weeks ago, Qwen3.5 397B became the first model Google submitted to AgentX. Its TPUv7 FP8 vLLM results on our agentic inference benchmark demonstrate that it is 1.67x better perf per dollar than even FP4 GB300 NVL72.

![](https://substack-post-media.s3.amazonaws.com/public/images/25ecc219-b095-4274-9ff8-11ac2b752949_1412x1278.png)
*Source: SemiAnalysis*

NVIDIA may try to claim that it doesn’t care about the Qwen3.5 397B model, but from analyzing our upstream InferenceX submission analytics datalake, the reality is that NVIDIA has spent over 20% of the sweep GPU hours on Qwen3.5 for certain NVIDIA GPU SKUs so it is hard for NVIDIA to claim that. In addition, if you look at the NVIDIA engineers assigned to Qwen3.5, it is some of the top 10x inference performance engineers at NVIDIA in **mainland China** and USA, so clearly, NVIDIA cares about optimizing this model.

**Furthermore, certain major hyperscalers/AI lab use Qwen3.5 397B and multi trillion parameter scale up version based on Qwen3.5 397B architecture as proxy models** when making hardware purchasing and capacity planning decisions. So, this is a very important model for certain token factories.

For readers making purchasing decisions, our [AI Cloud & TCO Model](https://semianalysis.com/ai-cloud-tco-model) extends the analysis into cluster economics, including cash flow, investment returns, and accelerator residual values.

[Get Access](https://semianalysis.com/ai-cloud-tco-model/#contact)

AgentX captures the four elements of an agentic workload:

- Multi-turn: a session includes many user / assistant interactions (tens or hundreds) compared to a handful in a chatbot scenario.
- Long context: system prompts, tool definitions, and the large number of turns make context accumulate quickly.
- High prefix reuse: since the conversation progresses linearly, where output from turn n-1 is concatenated to turn n
- Sub-agent bursts: a session launches multiple short-lived sub-agents with fresh context, which create bursty KVCache patterns.

TPU was able to demonstrate that its upcoming TorchTPU vLLM stack can successfully handle agentic workloads.

![](https://substack-post-media.s3.amazonaws.com/public/images/ccdfce66-ca13-4572-b74d-41e5a85d1380_1978x1320.png)
*Source: SemiAnalysis*

## NVIDIA First Counter Submission

NVIDIA engineers worked overtime to launch their counter submission FP4, which beats TPUv7 FP8 on decode performance, but there is a slight issue: they overtuned decode at the expense of prefill, hurting overall end-to-end performance. Thus, on end-to-end performance, TPUs FP8 is currently still beating GB300 NVL72 FP4.

![](https://substack-post-media.s3.amazonaws.com/public/images/c48e3dfd-b06c-46fb-92ab-e9667bcd79d8_814x700.png)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/90e4b8ad-367a-4071-9d38-43fb1ba89851_822x673.png)

## Open Source Kubernetes llm-d puts TPUv7 far above GB300 FP8 for Decode Interactivity

Disaggregated serving runs prefill and decode on separate hosts so long prefills do not stall generation. llm-d is the open-source K8s router that coordinates them, each host is 4 TPUv7 chips, and each result uses 24-32 chips.

![](https://substack-post-media.s3.amazonaws.com/public/images/18790491-f0db-438c-8c9e-745221abf5f6_1600x642.png)
*Source: SemiAnalysis*

Speed comes from capping how many requests each decode host runs, from one at a time at the low-latency end up to 112 at the high-throughput end. Requests over the cap wait for a free host, which adds to their TTFT. Even so, p90 time to first token at the fastest point is 8.6 seconds, against 11.1 for GB300 FP4’s fastest point.

This uses llm-d, one of the largest ecosystem-based production inference kubernetes orchestrators. During the recent Kimi K3.1 Pro launch, [they had Day 0 support for TPUv7 on llm-d](https://llm-d.ai/blog/deploy-kimi-k3-1-pro-with-llm-d).

![](https://substack-post-media.s3.amazonaws.com/public/images/d87cb8ff-a121-4daa-a8ae-72239abcde9c_1173x717.png)
*Source: InferenceX*

At FP8, TPUv7 with llm-d beats GB300 at every interactivity, from >2x at high throughput to achieving more than 1000tok/s/user in the ultrafast region.

Unfortunately, using this turn-based routing algorithm does lead to worse end-to-end performance for TPUs compared to GB300 TRTLLM FP4. However compared to FP8 and FP4 GB300 NVL72 SGLang, it is still much better.

![](https://substack-post-media.s3.amazonaws.com/public/images/544a77c4-b86b-46d6-b9a3-321e1c6af525_1176x757.png)
*Source: SemiAnalysis*

## Qwen3.5 TPU Optimizations

Qwen3.5-397B mixes 45 linear attention layers, which keep a fixed-size state per request, with 15 full attention layers. Google describes three main changes:

- **Decode megakernel.** One kernel runs the whole decode step and prefetches the next layer’s weights while the current layer computes.
- **Host DRAM offload.** KV cache and linear attention state spill to host DRAM through TPU Sync, Google’s newly open-sourced offload framework.
- **Cache-aware routing.** llm-d sends each turn to the prefill host holding its prefix and keeps each session on its decode host unless that host is full. Google says routing to the exact data-parallel rank raised decode cache hit rates from 56% to 76%.

# Kimi K3 AgentX

[TPU from Inferact and AMD shipped megakernels for frontier MoE models first in open source engines.](https://inferact.ai/blog/tpu-megakernels) NVIDIA quickly followed within a week with its own megakernels.

A conventional decode step launches hundreds to thousands of kernels, and the chip idles between them. A megakernel runs many layers in one long-running kernel that prefetches the next weights, while the current ones compute. AMD calls its version the MonoKernel. On GLM-5.2 across eight MI350X GPUs, AMD reports that it cuts a decode step from about 2,459 launches to 210 and runs 2.31x faster at batch 1.

![](https://substack-post-media.s3.amazonaws.com/public/images/3c217042-892b-4bcd-a0eb-1eb31f185823_1700x604.png)
*Source: SemiAnalysis*

A megakernel removes the idle gaps between kernel launches. Read more about megakernels in our TileRT article:

For this setup, DCP was used for prefill. The prefill and decode variants of context parallelism describe where each technique *usually* helps, not where it can run. K3 uses MLA which stores KV as one latent shared across heads, so TP cannot split it and every TP rank holds a full copy. DCP fixes this by giving each TP rank a different slice of tokens. Prefill context parallelism would have needed a lower TP degree, which copies weights onto more chips and leaves less HBM for the KV cache, already the scarce resource here.

![](https://substack-post-media.s3.amazonaws.com/public/images/91dc8bc4-7646-464f-b8dc-80a7e3a5dbbe_2048x1013.png)
*Source: Inferact*

## Competitive with GB300 FP4 at launch

At launch on October 17, TPUv7 delivered 0.77x to 0.91x GB300’s tokens per dollar from 50 to 200 tok/s/user and was 1.6x faster for a single user, at 391 tok/s/user against 251. On Google’s internal cost it beat GB300 at 100 and 200 tok/s/user.

![](https://substack-post-media.s3.amazonaws.com/public/images/8bd18ac8-2336-435b-84e6-5b2054f098ee_2038x1349.png)
*Source: InferenceX*

GB300 FP4 now leads by 1.5x to 2.6x after four NVIDIA refreshes. TPUv7 still delivers a competitive 1.15x to 2.5x the tokens per dollar of GB200, B200 and B300, while VR200 delivers 4.3x to 5.6x TPUv7.

![](https://substack-post-media.s3.amazonaws.com/public/images/6c33f9a0-4ffb-40d2-b82b-1c7e94632921_1030x704.png)
*Source: InferenceX*

In an apples to bananas comparison between TPUv7 & Rubin NVL72, Rubin is up to 6x better perf per dollar. But note that this is an unfair comparison as Rubin should be compared to TPUv8i which we will be benchmarking very soon.

![](https://substack-post-media.s3.amazonaws.com/public/images/4597cafb-fdb4-4046-831c-d3e8eda53c49_1040x705.png)
*Source: SemiAnalysis*

It is important to note that **Rubin’s results remain preview submissions**. We look forward to NVIDIA providing direct Rubin access so we can independently reproduce these results and run the full InferenceX/AgentX suite.

## Built by the Ecosystem

This result came from the vLLM ecosystem, not from Google alone. Inferact, founded by vLLM’s creators and maintainers, built the K3 megakernels with Google, and the two submitted the result together. The megakernel plugs into vLLM as a model runner that replaces only the forward, so vLLM’s scheduling, prefix caching and KV transfer work unchanged. The stack is open source on vLLM TorchTPU, and Inferact’s reproduction guide runs it from a Docker image. Ecosystem development like this has mostly happened on CUDA.

![](https://substack-post-media.s3.amazonaws.com/public/images/a7b6ad41-a35c-472d-9f02-b33d7c994c37_2048x927.png)
*Source: Inferact*

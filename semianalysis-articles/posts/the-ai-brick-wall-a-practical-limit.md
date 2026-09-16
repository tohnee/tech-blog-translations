---
title: "The AI Brick Wall – A Practical Limit For Scaling Dense Transformer Models, and How GPT 4 Will Break Past It"
date: 2023-01-24
source: https://newsletter.semianalysis.com/p/the-ai-brick-wall-a-practical-limit
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# The AI Brick Wall – A Practical Limit For Scaling Dense Transformer Models, and How GPT 4 Will Break Past It

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Large generative AI models unlock massive value for the world, but the picture isn’t only roses. Costs for training for these civilization-redefining models have been ballooning at an incredible pace. Modern AI has been built on scaling parameter counts, tokens, and general complexity an order of magnitude every single year. This report will discuss the brick wall for scaling dense transformer models, the techniques and strategies being developed to break through that wall, and which specific ones will be used in GPT 4.

The most well-known models, such as GPT, BERT, Chinchilla, Gopher, Bloom, MT-NLG, PaLM, and LaMDA, are transformers. Transformers are a type of multi-layer perceptron (MLP) network and are *generally* considered dense matrix models. Dense models are fully connected, with all “neurons” in one layer connecting to all “neurons” in the next layer. This allows the model to learn complex interactions between the features and learn non-linear functions. An amazing amount of information can be embedded within the billions of parameters of these models.

It should be noted that this is not how brains in the natural world operate. The network architecture of brains in the animal kingdom does not map well to existing hardware and, therefore, would operate at much lower [FLOPS utilization rates](https://www.semianalysis.com/i/97006309/machine-learning-training-components). Historically, dense matrix models have been able to scale up in parameter counts, data (tokens), and complexity much better than other model architectures.

## **What came first, the chicken or the egg?**

Trick question, it’s the GPU.

The Nvidia GPU architecture is inherently well-tailored to running dense matrix models, which has driven transformers to scale in capabilities much faster than any other model architecture. With increased capabilities also came an explosion in popularity. Scale means almost everything in AI, and so the billion-dollar question is if these models will be able to continue to scale with existing dense architectures for years to come.

[MosaicML](https://www.mosaicml.com/blog/gpt-3-quality-for-500k) already claims to be able to train GPT-3 quality models for less than $500,000 and [Chinchilla](https://arxiv.org/pdf/2203.15556.pdf) size and quality models for ~$2,500,000. [They offer that pricing to customers, today](https://www.mosaicml.com/cloud).

This is significantly cheaper than most expect, which begs the question; how much higher can we scale?

Last week, we discussed the components of machine learning, model utilization rates, and the software stack.

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisHow Nvidia’s CUDA Monopoly In Machine Learning Is Breaking - OpenAI Triton And PyTorch 2.0Over the last decade, the landscape of machine learning software development has undergone significant changes. Many frameworks have come and gone, but most have relied heavily on leveraging Nvidia's CUDA and performed best on Nvidia GPUs. However, with the arrival of PyTorch 2.0 and OpenAI's Triton, Nvidia's dominant position in this field, mainly due to its software moat, is being disrupted…Read more4 years ago · 67 likes · 16 comments · Dylan Patel](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

The critical takeaway is that even with all the optimization techniques the ecosystem developed in 2022, Nvidia A100 GPUs have an upper bound of ~60% [model/hardware FLOPS utilization rates](https://github.com/mosaicml/examples/tree/main/llm/throughput) for training large language models.

The research arm of SemiAnalysis has done surveys of many startups and enterprises and arrived at ~$1.5 per SXM A100 GPU per hour as a baseline cost for **large clusters of 256 GPUs** with NVLink and 1.6T networking. Some companies have better deals with AWS, Azure, Oracle Cloud, CoreWeave, etc., but this is a baseline. The deals will also be much better if the company purchasing GPUs agrees to a three-year contract. For example, the list price at Azure is only $1.36 per hour, but signing up for the 2020 released A100 for three years is not something most want to do. On-premises will also be cheaper over multiple years if utilization rates are high, but that is very difficult for most enterprises and startups to commit to/achieve.

## **Current State-Of-The-Art Models**

![](https://substack-post-media.s3.amazonaws.com/public/images/1d30755f-7ece-47d4-bb91-acad82473df8_3362x2035.png)

The above chart shows publicized state-of-the-art models with their respective parameter counts and tokens (units of training data). The line is [Google DeepMind’s Chinchilla scaling observation](https://arxiv.org/pdf/2203.15556.pdf) (smoothing out the large error bars). Each point on the line shows the theoretical FLOPS required to train a model with that parameter and token count. The FLOPS figure shown ignores any recompute of activations, checkpointing, etc.

There is a relatively tight clustering of these publicized models. The crazy thing is that through venture capital due diligence we have done, we know of 21 startups and another 11 major corporations that are training large models with enough parameters/tokens to be theoretically GPT-3 quality or better. It is the wild west, and observing and investing in successful entities will be exciting.

Once you know the parameter count, token count, and model architecture, you can easily calculate the theoretical training costs for many popular models. In this example, we will use Nvidia A100s, using $1.5 per hour per GPU. [Model/hardware “FLOPS utilization”](https://github.com/mosaicml/examples/tree/main/llm/throughput) will increase from 40% to 60% with larger model sizes, as we explained [here](https://www.semianalysis.com/i/97006309/the-memory-wall), but generally, there isn’t much room to go higher on large distributed systems.

## **State-Of-The-Art Training Costs**

![](https://substack-post-media.s3.amazonaws.com/public/images/95802dd0-c7c3-4fc0-9bef-be31971cbf85_1677x822.png)

This table is a theoretical optimal cost to train the model on Nvidia A100s. It does not account for the people required, ML Ops tools, data gathering/preprocessing, failure restoration, one-shot/few-shot learning examples, inference, etc. Many of these components are incredibly costly. In this context, [MosaicML’s cost of $450k for GPT-30B and $2.5M for GPT-70B](https://www.mosaicml.com/blog/gpt-3-quality-for-500k) are close to the optimal training costs of $326k and $1.75M. It should be noted that Mosaic’s prices include many of those ML Ops tools, which significantly reduces the personnel required to train a model reliably.

As we move down the stack, the Google Pathways Language Model (PaLM) is the most advanced dense model that has been trained and publicly detailed. While we used Nvidia A100s as a baseline for the cost comparison, it should be noted that PaLM was trained on 6,144 of Google’s in-house TPU v4. Google achieved [46.2% model FLOPS utilization and 57.8% hardware FLOPS utilization.](https://arxiv.org/pdf/2204.02311.pdf) The compute cost to train PaLM is not cost prohibitive.

Nowadays, most will train dense models more in accordance with the [Chinchilla scaling observations](https://arxiv.org/pdf/2203.15556.pdf). Those observations state that given a compute, it is more cost-effective to train a smaller parameter model with more data versus current state-of-the-art models. While there are many criticisms of the Chinchilla observations, including very wide error bars and overextrapolation of results, the directionality of the observation is accurate.

## **The Dense Transformer Scaling Wall**

![](https://substack-post-media.s3.amazonaws.com/public/images/1e394df3-9c1e-435e-9968-d9c48f803bed_1691x692.png)

Regarding parameter counts growth, the industry is already reaching the limits for current hardware with dense models—a 1 trillion parameter model costs ~$300 million to train. With 100,000 A100s across 12,500 HGX / DGX systems, this would take about ~3 months to train. This is certainly within the realm of feasibility with current hardware for the largest tech companies. The cluster hardware costs would be a few billion dollars, which fits within the datacenter Capex budgets of titans like Meta, Microsoft, Amazon, Oracle, Google, Baidu, Tencent, and Alibaba.

Another order of magnitude scaling would take us to 10 trillion parameters. The training costs using hourly rates would scale to ~$30 billion. Even with 1 million A100s across 125,000 HGX / DGX systems, training this model would take over two years. Accelerator systems and networking alone would exceed the power generated by a nuclear reactor. If the goal were to train this model in ~3 months, the total server Capex required for this system would be hundreds of billions of dollars with current hardware.

This is not practical, and it is also likely that models cannot scale to this scale, given current error rates and quantization estimates.

[Share](https://newsletter.semianalysis.com/p/the-ai-brick-wall-a-practical-limit?utm_source=substack&utm_medium=email&utm_content=share&action=share)

The practical limit for a Chinchilla optimally trained dense transformer with current hardware is between ~1 trillion and ~10 trillion parameters for compute costs. With future reports, we will discuss this band more for both dense vs. sparse models and the cost competitiveness of Google’s TPUv4, TPUv5, Nvidia A100, H100, and AMD MI300. Data is another problem that we can cover in the future.

While 1 trillion to 10 trillion is the practical limit for today’s hardware, new hardware is coming. Furthermore, quite a few strategies and techniques were developed in the last year that will enable both a reduction in cost to train and scaling to even higher parameter counts.

Training efficiency is the key metric to watch. Training efficiency is the amount of compute and training time used to achieve superior model quality versus the prior state of the art. Model architecture will not remain stagnant, and training efficiency will go up.

The next **2/3 of this report** **is for subscribers** and covers the specific strategies and techniques that increase training efficiency and reduce inference costs for large models. Remember, a trained model is useless until it is deployed to run inference operations, and most hardware costs will come from model inference… eventually.

These strategies will be deployed in 2023 with future models, including some specific ones that OpenAI will use in GPT 4. These techniques and strategies will also be heavily used by companies such as Google, Deepmind, MosaicML, Microsoft, Nvidia, Tsinghua University, HuggingFace, Stability, AI21, Anthropic, Cerebras, SambaNova, TensTorrent, Cohere, Neural Magic, etc.

All of the strategies and techniques we will discuss below, and many more, were presented at NeurIPS by the above firms. NeruIPS is the premiere machine learning conference. This year there were ~2,905 accepted papers submitted out of ~10,000 submissions with ~10,000 in-person attendees. Today we are focusing on those making it out of the research phase and into the applied world. For an excellent newsletter that covers the research world in even more detail, check out [Davis Summarizes Papers, where Davis Blalock has summarized hundreds of papers with novel approaches.](https://dblalock.substack.com/)

[![](https://substackcdn.com/image/fetch/$s_!2Iqq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F4da41de1-cb9d-4505-984f-e6e63c23ef0c_512x512.png)Davis Summarizes PapersI go through all the machine learning arXiv submissions each week and summarize 10 to 20 of my favorites.
Free forever and read by over 2000 ML researchers and practitioners.By Davis Blalock](https://dblalock.substack.com?utm_source=substack&utm_campaign=publication_embed&utm_medium=web)

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

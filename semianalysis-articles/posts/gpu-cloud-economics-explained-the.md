---
title: "GPU Cloud Economics Explained – The Hidden Truth"
subtitle: "CPU vs GPU Cloud Differences, TCO Model, PUE, Hyperscalers Disadvantage"
date: 2023-12-04
source: https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
---

# GPU Cloud Economics Explained – The Hidden Truth

**CPU vs GPU Cloud Differences, TCO Model, PUE, Hyperscalers Disadvantage**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Over the last year there has been an explosion in the number of pureplay GPU clouds. We kid you not - more than a dozen different firms’ equity or debt proposals have crossed our desks for this exact purpose, there are likely many more out there that we haven’t even seen. The deal flow has finally slowed down, so let’s publicly examine the economics at play here more deeply.

The first quick point to address is the general motivation for the massive influx of new clouds. While there is certainly a unique set of infrastructure challenges, GPU clouds are significantly easier to operate than general purpose clouds from a software perspective. Third party pureplay GPU clouds do not need to worry about advanced database services, block storage, security guarantees for multi-tenancy, APIs for various 3rd party services providers, or in many cases even virtualization doesn’t matter.

A hilarious example of how little cloud developed software, outside of awesome models of course, matters for AI is at AWS. While AWS loves to talk up their SageMaker platform as a great tool for their customers to create, train, and deploy models in the cloud, it’s a clear example of “do as I say, not as I do.” [Amazon uses Nvidia’s Nemo framework](https://blogs.nvidia.com/blog/nemo-amazon-titan/) in place of Sagemaker [for Titan, their very best model](https://blogs.nvidia.com/blog/nemo-amazon-titan/). Note that Titan is [significantly worse than numerous open-source models](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)! While Nemo and Sagemaker aren’t exactly analogous, it exemplifies how little the cloud’s “value add” software matters.

Furthermore, while the standard cloud needs supreme flexibility and fungibility in compute, storage, RAM, and networking, the GPU cloud needs far fewer options due to the relative homogeneity of workloads. Servers are generally committed to for long time scales, and the H100 is the optimal GPU for basically all modern use cases, including LLM training and high volume LLM/diffusion inference. Infrastructure choices for end users are mostly about how GPUs you need. Of course, you need to ensure you have performant networking, but overshooting on networking spend is not a massive concern for most users because they are [tiny cost relative to the GPUs](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is).

For all but the biggest users, locality of your existing data isn’t even that important during training and inference because [egress costs are tiny](https://www.semianalysis.com/i/108660819/amazon-scale-to-service). The data can be transformed and transferred, and high-performance storage is not terribly difficult for a cloud provider to purchase from Pure, Weka, Vast, etc, as again, like other items, storage constitutes a very small portion of the cost of AI infrastructure.

## **CPU vs GPU Colocation Total Cost of Ownership (TCO)**

Even ignoring the lack of a moat regarding GPU clouds (outside of a cozy relationship with Nvidia), the true driver of this boom in new providers is the total cost of ownership (TCO) equation for CPU servers versus GPU servers in a colocation (colo) environment. CPU servers’ TCO have a more varied number of important factors to balance, while GPUs, due to Nvidia’s extremely high margins, are dominated purely by capital costs.

In other words, since capital is the only real barrier to entry, not physical infrastructure, it’s no surprise there are so many new entrants.

![](https://substack-post-media.s3.amazonaws.com/public/images/27a54ff5-da5e-42ce-acb9-d4dddecb9ae3_1518x1323.png)
*OEM pricing with networking costs allocated to server level, not hyperscale*

In the case of CPU servers, the various hosting costs ($220 a month) are of similar magnitude to the capital costs ($301 a month). Compare this to a GPU server, where the various hosting costs ($1,871 a month) are completely dwarfed by the capital costs ($7,025 a month). This is the core reason why 3rd party clouds can exist.

The hyperscale cloud providers such as Google, Amazon, Microsoft can optimize their hosting costs significantly by being better designers and operators of datacenters. Take for example the metric of Power Usage Effectiveness (PUE). It is a metric that compares the total amount of energy used by a datacenter compared to the energy delivered to computing equipment. Efforts to reduce this metric generally center around cooling and power delivery. Google, Amazon, and Microsoft are amazing, so their PUE’s are approaching as close to 1 as possible.

Most colocation (colo) facilities are generally significantly worse at ~1.4+, meaning ~40% more power is lost to cooling and power transmission. Even the newest facilities for the GPU Cloud will only be around 1.25, which is significantly higher than the big clouds who also can build the datacenters cheaper due to various scale advantages. This difference is incredibly important for CPU servers, because the increased hosting costs of colo makes a large percentage of TCO. In the case of GPU servers, while hosting costs are high, it really doesn’t matter on the grand scheme of things because hosting costs are minor and server capital costs are the dominating factor in the TCO equation.

A relatively poor datacenter operator can buy an Nvidia HGX H100 server with 13% interest rate debt and still come away with an all-in cost per hour of $1.525. There are many optimizations the better operators can do from here, but the capital costs are the main knob. In turn, even the most favorable GPU cloud deals are around $2 an hour per H100, and we have even seen desperate folks get fleeced for more than $3 an hour. The returns for cloud providers are tremendous….

Of course, this is the simplified framework. Many variables can change and they radically change the costing equation. We have even seen CoreWeave try to pitch 8 year lifecycles to people, but that math is utter nonsense.

In fact many of the assumptions in the table above are not representative of the reality of colo today. Instead we share more realistic figures below.

Let’s dive in and explain the simplified model more.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

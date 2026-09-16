---
title: "Amazon’s AI Resurgence: AWS & Anthropic's Multi-Gigawatt Trainium Expansion"
subtitle: "Anthropic multi-gigawatt clusters, Trainium ramp, best TCO per memory bandwidth, system-level roadmap, Bedrock and internal models"
date: 2025-09-03
source: https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "AJ", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
---

# Amazon’s AI Resurgence: AWS & Anthropic's Multi-Gigawatt Trainium Expansion

**Anthropic multi-gigawatt clusters, Trainium ramp, best TCO per memory bandwidth, system-level roadmap, Bedrock and internal models**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

[Two-and-a-half years ago, we flagged a looming “cloud crisis” at AWS](https://semianalysis.com/2023/03/20/amazons-cloud-crisis-how-aws-will/). Today, the evidence has mounted. AWS is the crown jewel of the Amazon empire, generating ~60% of group profits, and dominating the lucrative Cloud Computing market. But it struggles to translate this strength into the new GPU/XPU Cloud era.

Microsoft Azure now leads the market on quarterly new cloud revenue, and the gap between Google Cloud and AWS has materially narrowed especially with [Google's big moves on the TPU that we've been posting about for over a month](https://semianalysis.com/accelerator-model/). Markets have noticed. Year-to-date, Amazon is the clear laggard among the four tech-and-AI titans as investors mark down the company most for losing momentum in AI.

![](https://substack-post-media.s3.amazonaws.com/public/images/6227dc41-f0ed-4125-87c2-b52961d1b42c_1024x606.png)
*Source: SemiAnalysis Core Research , company filings*

Today, SemiAnalysis is back with another out-of-consensus call. While the market overplays the Cloud Crisis theme, we call for an AWS AI Resurgence. We laid out our thesis a month ago to our [Core Research subscribers](https://semianalysis.com/core-research/), forecasting an upcoming acceleration beyond 20% year-over-year growth by the end of 2025.

![](https://substack-post-media.s3.amazonaws.com/public/images/414c071a-3f68-4268-8f7c-94ba79182635_1024x509.png)
*Source: SemiAnalysis Core Research*

Amazon’s savior has a name: Anthropic. The startup has been the clear outperformer in the GenAI market in 2025, multiplying revenue fivefold year-to-date to reach $5B annualized.

![](https://substack-post-media.s3.amazonaws.com/public/images/01c05a64-a990-4506-9f1d-d0690410b13a_1024x547.png)
*Source: The Information, Reuters, Bloomberg, SemiAnalysis Core Research*

To keep that trajectory, Anthropic is betting hard on [Scaling Laws](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/). While Dario’s startup draws fewer headlines than OpenAI, xAI and [Meta Superintelligence](https://semianalysis.com/2025/07/11/meta-superintelligence-leadership-compute-talent-and-data/), it isn’t shy about investment. AWS has **well over a gigawatt of datacenter capacity in final stages of construction** for its anchor customer. AWS is building datacenters faster than it ever has in its entire history. And there’s **much more on the horizon**.

![](https://substack-post-media.s3.amazonaws.com/public/images/348cc316-30b7-41e3-a083-911df1ae1a33_1024x576.png)
*Source : SemiAnalysis Datacenter Industry Model*

To understand and forecast GPU/XPU power capacity by AI Lab broken down by Cloud Provider, we rely on our proprietary [Datacenter Industry Model](https://www.semianalysis.com/p/datacenter-model) powered by real-time satellite imagery. Trusted by all hyperscalers, AI labs, and the world’s largest investors, it *provides a **quarterly building-by-building datacenter forecast** for OpenAI, Anthropic, xAI, Meta Superintelligence, Google DeepMind, and more. [Contact us for more information](Sales@SemiAnalysis.com).*

## Trainium vs GPUs

While Amazon’s AI Datacenters are impressive in scale and speed, the design of individual building is unremarkable. [Hyper-optimized for air-cooling](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/#google-datacenters-%e2%80%93-energy-for-water-tradeoff), this blueprint is identical to 5-year-old traditional AWS Cloud datacenters.

What makes these facilities unique is their inside: they’ll host the **world’s largest cluster of non-Nvidia AI chips, with just under a million Trainium2 in the largest campus**. To understand everything about the Trainium2 system, read [our December 2024 technical deep dive](https://semianalysis.com/2024/12/03/amazons-ai-self-sufficiency-trainium2-architecture-networking/).

Trainium2 lags Nvidia’s systems in many ways, but it was pivotal to the [multi-gigawatt AWS/Anthropic deal](https://www.semianalysis.com/p/datacenter-model). Its memory bandwidth per TCO advantage perfectly fits into Anthropic’s [aggressive Reinforcement Learning roadmap](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/). Dario Amodei’s startup was heavily involved in the design process, and its influence on the Trainium roadmap only grows from here.

Put plainly: Trainium2 is converging toward an **Anthropic custom-silicon program**. This will enable Anthropic to be, alongside Google DeepMind, the only AI labs benefiting from **tight hardware–software co-design** in the near horizon.

![](https://substack-post-media.s3.amazonaws.com/public/images/377f07d4-2e4e-4833-afc7-dd75f876c777_1024x357.png)
*Source: AI Cloud TCO Model*

This report will dig into all aspects of Amazon’s AI resurgence: the Anthropic partnership, datacenters, and Trainium. At the end of the report, we provide a longer-term outlook on Anthropic, AWS Bedrock and internal models, and explain why everything isn’t rosy.

First, a step back on why AWS has underperformed rival AI Clouds to date.

## AWS GenAI underperformance

To understand the causes of Amazon’s underperformance in the GenAI era, we can analyze drivers of success in the GPU/XPU cloud market. In the most simplistic way, we see two primary customer groups for GPU/XPU capacity:

- Wholesale bare metal users: large-scale customers like OpenAI, Anthropic, ByteDance, and other hyperscalers.
- Managed SLURM/Kubernetes: Smaller customers such as startups, research institutes, and enterprise pilot projects.

### Cloud Crisis and ClusterMAX underperformance

In the second category, our [ClusterMax AI cloud rating](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/) is the best way to compare relative strengths and weaknesses. Platinum and gold-rated AI Clouds have seen more traction than others and boast higher-than-average pricing power. As such, the likes of CoreWeave, Oracle, Nebius, Crusoe and Azure have outperformed the market for multitenant GPU clusters – which require high performance and advanced software layers.

![](https://substack-post-media.s3.amazonaws.com/public/images/dbf0fa08-c2d5-42ef-a937-665ed42e6ce3_1024x615.png)
*Source: SemiAnalysis ClusterMAX GPU Cloud Rating*

[As predicted two years ago](https://semianalysis.com/2023/03/20/amazons-cloud-crisis-how-aws-will/), key to Amazon’s underperformance is the use of custom networking fabric EFA. AWS's success with ENA on the frontend network has not yet translated to EFA on the backend. EFA still lags behind other networking options on performance: NVIDIA's InfiniBand and Spectrum-X, as well as RoCEv2 options from Cisco, Arista, and Juniper. Raw performance isnt the only metric, the user experience of EFA isn't as good as InfiniBand & RoCEv2 either. That being said, with Amazon's newest EFAv4 performance at real world msg sizes is improving, albeit still behind the competiton.

Amazon's custom networking also [reduces their time-to-market due to customization requirements of Nvidia systems](https://x.com/SemiAnalysis_/status/1959758467402784855). Other items like advanced passive and active automated weekly scheduled health check strategies aren’t as solid as gold & platinum-rated clouds.

Our upcoming ClusterMAXv2 rating will provide an update on all major cloud providers based on our proprietary testing. Stay tuned!

### Searching for an anchor customer

More important to AWS’ XPU business growth is the ability to **secure anchor customers – the market-makers in this first wave of GenAI demand**. Scale, time-to-market, deep partnerships, and pricing are key to winning these accounts, more so than advanced software layers.

No firm better illustrates this than Microsoft. Azure’s AI outperformance over peers is entirely driven by its OpenAI partnership. As of Q2 2025 (June 2025), all of OpenAI’s >$10B cloud spending is booked by Azure.

![](https://substack-post-media.s3.amazonaws.com/public/images/7cf42542-67fc-456a-bc11-41ca08f65139_1024x508.png)
*Source: SemiAnalysis Datacenter Industry Model*

Amazon understood early on the need for an anchor customer and [invested $1.25B, expandable to $4B in Anthropic in September 2023](https://semianalysis.com/2023/10/02/amazon-anthropic-poison-pill-or-empire/). The partnership expanded in March 2024 [with Anthropic committing to use Tranium and Inferentia chips](https://www.aboutamazon.com/news/company-news/amazon-anthropic-ai-investment). In November 2024[, Amazon invested an additional $4B into Anthropic,](https://www.aboutamazon.com/news/aws/amazon-invests-additional-4-billion-anthropic-ai) [with the latter naming AWS as its primary LLM training partner](https://www.aboutamazon.com/news/aws/amazon-invests-additional-4-billion-anthropic-ai).

### Anthropic’s outperformance, AWS underperformance?

Amazon’s bet has been the right one. Anthropic is the clear outperformer in 2025 in the GenAI market, with revenue surging from $1B to $5B annualized. In this context, AWS’ underperformance understandably frustrates investors, but they’re misunderstanding the composition of Anthropic’s spending on training and inference.

![](https://substack-post-media.s3.amazonaws.com/public/images/b77d4f69-7460-45f7-9709-b281de0a926c_1024x547.png)
*Source: SemiAnalysis Tokenomics*

There **are two clear reasons explaining why Amazon isn’t yet truly benefiting** from its relationship with Anthropic:

1. As of Q2 2025, Anthropic’s cloud spending is over 2x smaller than that of OpenAI.
2. A large share of Anthropic’s spending is going to Google Cloud – one of Anthropic’s first major investors ($300M round late-2022) and preferred cloud partner in 2023 and 2024, before the expanded AWS deal.

![](https://substack-post-media.s3.amazonaws.com/public/images/315d7305-7da2-407b-a362-97b5a08962d3_1024x507.png)
*Source: SemiAnalysis Datacenter Industry Model*

## Anthropic & AWS multi-gigawatt AI Training infrastructure

In particular, we believe that most of Anthropic’s skyrocketing inference needs are served by Google Cloud. Having the world’s best inference system (TPU) is a key competitive advantage.

The AWS infrastructure buildout is aimed at taking a chunk of this for its key customer will also focusing on **training**. While Anthropic makes less headlines than peers like OpenAI, xAI and Meta, is it all-in on the AGI race and isn’t planning to be shy on training spending. Anthropic leadership truly believes in [Scaling for RL](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/).

Their belief will materialize as early as this year. We show below three AWS campuses in final stages of construction, boasting over 1.3GW of IT capacity for the **sole purpose of serving Anthropic’s training needs**. The speed of construction is remarkable.

![](https://substack-post-media.s3.amazonaws.com/public/images/eed0550a-e73f-4693-991e-fc95b5f6fc7a_1024x576.png)
*Source : SemiAnalysis Datacenter Industry Model*

While these datacenters look built from the skies, we don’t think they are generating any meaningful revenue yet. Trainium has faced some yield issues on the assembly phase – fairly standard for a new system. We think the three large AWS campuses will meaningfully contribute to AWS’ top line by the end of 2025 and jack up growth above the 20% YoY threshold.

![](https://substack-post-media.s3.amazonaws.com/public/images/2757411e-3e3d-465b-aa82-b637633ee401_1024x509.png)
*Source: SemiAnalysis Core Research - Core Research is our institutional research service trusted by most of the world’s largest hedge funds and investors. Contact us to get the industry’s most granular insights on AI hardware, software and infrastructure.*

Anthropic isn’t stopping there. Its ~$13B funding round at a $183B valuation will provide capital to sign additional deals with AWS, Google, and others. AWS isn’t waiting standing still – they're already breaking ground on upcoming GW-scale datacenters to capture this growth.

![](https://substack-post-media.s3.amazonaws.com/public/images/58e99612-92fc-46a8-a6c1-1b97237f9b05_1024x553.png)
*Source: SemiAnalysis Datacenter Industry Model*

As explained earlier, these datacenters will primarily be filled with AWS’ custom chip [Trainium](https://semianalysis.com/2024/12/03/amazons-ai-self-sufficiency-trainium2-architecture-networking/). Given the sheer scale, we **can’t understate how bold Anthropic’s bet is**. Not only are they committing to spending tens of billions of dollars, they're doing it on a largely unproven chip!

Let’s try to make some sense of their bet by digging into Trainium’s TCO and roadmap.

## Trainium2 TCO analysis – how Anthropic’s big bet could pay off

Trainium2 supply chain signals are currently extremely strong. Our industry-leading [AI Accelerator Model](https://semianalysis.com/accelerator-industry-model/) track both the package shipments and the system/rack shipments and they’ve surged since the beginning of the year. It *provides quarterly volume forecasts for the 10+ SKUs comprising the Trainium2 and Trainium3 product family and calls out suppliers set to disproportionately benefit from specific SKUs. [Contact us for more information](Sales@SemiAnalysis.com).*

![](https://substack-post-media.s3.amazonaws.com/public/images/d5e4a6cb-ee16-49ea-ad64-5288333af03c_1024x552.png)
*Source: SemiAnalysis Accelerator and HBM Model*

Note this is chip production, rack production is lagged, but we also track it.

Competing with Nvidia and Google’s TPU is, of course, no small feat. While Google is rolling out its seventh generation TPU, Ironwood, Trainim2 is only Amazon’s third-generation AI Accelerator.

### Chip specifications: Trainium2 inferior on all fronts, but…

A simple look at chip specifications shows Trainium as a clear laggard relative to Nvidia:

- Nvidia’s GB200 has a **3.85x FP16 FLOPs advantage**, at 2500 TFLOP/s/chip vs Trainium2’s 667 TFLOP/s/chip. Note that spec sheet numbers are inflated compared to actual achievable FLOPs.
- In terms of **Memory bandwidth, the gap narrows to 2.75x**, at 8000GB/s/GPU vs 2900GB/s/Trn2

![](https://substack-post-media.s3.amazonaws.com/public/images/ebe72b52-b6a4-4b23-8c3b-a85a6399d12d_1024x553.png)
*Source: Amazon, SemiAnalysis*

Evaluating scale-up network bandwidth is another key item. We’ve explained several times the [importance of scale-up networks for reasoning model inference](https://semianalysis.com/2024/12/25/nvidias-christmas-present-gb300-b300-reasoning-inference-amazon-memory-supply-chain/#built-for-reasoning-model-inference). Our [deep-dive on Reinforcement Learning](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/) highlighted the similarities of RL with inference workloads, making memory bandwidth a crucial item to scale post-training.

- Nvidia’s GB200 NVL72 boasts an aggregate 576TB/s memory bandwidth across World Size.
- This is a **3.1x advantage relative to Trainium2’s** (Teton2-PD-Ultra-3L SKU) 186 TB/s – with the caveat that it varies across SKUs.

While Trainium appears materially behind, the picture changes once we factor-in Total Cost of Ownership.

### Trainium’s memory bandwidth per TCO advantage

In the table below, we incorporate TCO into our comparison. While Nvidia has a material head on a TCO per effective training PFLOP, Trainium2 is highly competitive on a TCO per million Tokens and TCO per TB/s of memory bandwidth.

![](https://substack-post-media.s3.amazonaws.com/public/images/3fa83400-60da-4742-8b8b-131e439ac2b7_1024x357.png)
*Source: AI Cloud TCO Model*

And we don’t see Nvidia’s upcoming VR200 NVL144 change the picture relative to AWS’ Trainium3. To be clear, TCO has many other moving parts. AWS has other system-level architecture deployments that better fit some use cases. Later down the road, [Nvidia’s Kyber rack will boast the world’s most advanced scale-up network architecture](https://semianalysis.com/2025/03/19/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman/#kyber-rack-architecture).

For a full understanding of the TCO of 50+ Nvidia SKU and a detailed TCO comparison with all AMD, Trainium and TPU SKUs, [check out our AI Cloud TCO Model](https://semianalysis.com/ai-cloud-tco-model/). The largest hyperscalers, Neoclouds and their financial sponsors rely on our model to time their investment decisions.

### Anthropic is betting on hardware-software codesign

Trainium2’s memory bandwidth per TCO advantage is key to understanding Anthropic’s choice. While Nvidia’s chips and systems are better on most fronts, Trainium2 fits perfectly into Anthropic’s roadmap. They’re the most aggressive AI Lab on [scaling post-training techniques like Reinforcement Learning](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/). Their roadmap is more memory-bandwidth-bound than FLOPs bound. Our recent HBM report explains in-depth which AI workloads tend to be memory-bound.

Anthropic’s ramp will make it not only the only large external end-user of Trainium2, it’ll also be materially larger than Amazon’s internal needs (e.g. Bedrock, Alexa, etc). They’re now heavily involved in all Trainium design decisions and, essentially, use Amazon’s Annapurna Labs as a custom silicon partner! **This makes Anthropic the only AI lab, alongside Google DeepMind, benefiting from tight hardware-software codesign**.

### Trainium’s roadmap: doubling down on systems

Amazon is rolling out a new system-level architecture for its anchor customer. Currently, the two systems deployed by AWS are Teton PD and Teton PD Ultra. Next year, the new Teton PDS and Teton Max are set to ship in large volumes. [Our AI Accelerator Model provides the exact volumes and SKU-by-SKU breakdown on a quarterly basis](https://semianalysis.com/accelerator-industry-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/4bfcf56c-0eb5-4cdc-9c3c-593978efdf66_1024x517.png)
*Source: SemiAnalysis Accelerator Industry Model , AWS*

The key difference **is the introduction of an all-to-all scale-up network dubbed NeuronLinkv3.** Trainium’s architecture is thus converging towards Nvidia’s NVL72 NVLink.

**Four NeuronLinkv3 switch trays** will be placed in the middle of the rack with 16 compute trays above and below split evenly. [Certain supply chain vendors are set to benefit disproportionately, as highlighted two months ago on Core Research](https://semianalysis.com/core-research/) – our institutional research service trusted by the world’s largest hedge funds. That vendor is up 73% since our post. We see the introduction of PDS as an intermediate step in Trainium’s path to catch up with Nvidia. We also believe that Anthropic was heavily involved in the launch of this new system-level architecture.

![](https://substack-post-media.s3.amazonaws.com/public/images/af62f51b-0cdc-4e58-80e0-ea8828c9d9ba_1024x292.png)
*Source: SemiAnalysis Accelerator Industry Model , AWS*

Anthropic’s increased involvement in design decisions bodes well for future volumes. But they’re not giving up on TPUs and Nvidia GPUs either. Our [Accelerator Model](https://semianalysis.com/accelerator-industry-model/) forecasts Amazon and Google Cloud’s chip purchases broken down by precise SKU, and our [Datacenter model](https://www.semianalysis.com/p/datacenter-model) to understand which datacenter and cloud partners support Anthropic’s ramp. The [TPU ramp for Anthropic in 2026 is huge, and their are unique aspects to their deal as we have been posting about for over a month.](https://semianalysis.com/core-research/google-selling-tpu-systems-externally-further-tpu-revisions/)

Let’s now take a longer-term view and evaluate what the future of AWS might look like. Behind paywall, we discuss the following items:

- The outlook for Amazon’s key customer: Anthropic.
- Amazon’s GenAI business beyond Anthropic: Bedrock and internal LLM efforts.
- The Trainium ramp in 2026 & 2027, potential new external customers, and how it might impact Amazon’s financial profile in future years.

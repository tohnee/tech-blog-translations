---
title: "xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise"
subtitle: "On Site Turbines, Mississippi Expansion, Solaris Energy, Can xAI afford it?, Middle East Funding, Tesla, Talent Exodus, API revenue, Consumer Growth, RL Environment"
date: 2025-09-16
source: https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Wei Zhou", "AJ", "Maya Barkin"]
tags: []
audience: only_paid
paywalled: true
---

# xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise

**On Site Turbines, Mississippi Expansion, Solaris Energy, Can xAI afford it?, Middle East Funding, Tesla, Talent Exodus, API revenue, Consumer Growth, RL Environment**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Much has been written about xAI’s Colossus 1. The Memphis build belongs in the history books: the largest AI training cluster, erected from scratch in 122 days. With roughly 200,000 H100/H200s and ~30,000 GB200 NVL72, it remains, today, the largest fully operational, single-coherent cluster (setting apart Google, [master of multi-datacenter-training](https://semianalysis.com/2024/09/04/multi-datacenter-training-openais/)).

However, Colossus 1’s ~300 MW looks modest next to the Gigawatt-scale clusters under construction by [OpenAI](https://semianalysis.com/2025/06/30/how-oracle-is-winning-the-ai-compute-market/), [Meta](https://semianalysis.com/2025/07/11/meta-superintelligence-leadership-compute-talent-and-data/) and [Anthropic](https://semianalysis.com/?p=150449616&preview=true). Their hyperscaler partners are happy to leverage their balance sheet and win the market by throwing dollars at it.

Was xAI’s prowess a one-time wonder? Today we will publicize some data from our [industry leading datacenter model over the last year](https://semianalysis.com/datacenter-industry-model/) that is accessible to clients. This is the our same proprietary data that called the Oracle deals many months ahead of the announcement.

![](https://substack-post-media.s3.amazonaws.com/public/images/d6c5b75b-df0f-4ba0-a9f9-0aa1e6380ec0_1024x552.png)
*Source: SemiAnalysis Datacenter Industry Model - note: there is a lag between Datacenter operational and GPUs operational - Google and exact figures available in model*

**Short answer: no**. xAI is still squarely in the frontier-AI race and is positioned to leapfrog most rivals again on compute. By our estimates, its total datacenter capacity for a single training cluster will surpass Meta Superintelligence and Anthropic by Q3 2025. The datacenter capacity will be ready for the GPUs to be moved in to create the largest single datacenter in the world, yet again. xAI has to raise the capital for those GPUs, but they have the allocations from Nvidia to have it fully training large scale models early next year.

Elon came up with **a new genius trick** to beat rivals at time-to-market. Colossus 2 will be an even more impressive achievement than xAI’s first cluster. Let’s dig in.

The first half of this report will dig into the Colossus 2 prowess. The second half will discuss Grok models, our mid-to-long term thoughts on xAI, and the **unique RL method** xAI is using that may lead them to leapfrog OpenAI, Anthropic, and Google.

---

## SemiAnalysis Is Hiring

We are seeking a highly motivated & skilled Member of Technical Staff to join our growing special projects engineering team. You will play a crucial role in developing industry leading gpu cloud benchmarks & evaluation framework.  Our gpu cloud evaluation frameworks is endorsed by many tier 1 & 2 frontier labs. You may be a good fit if you have the following experience:

- Demonstrated experience in ML frameworks such as PyTorch or JAX through professional experience, personal projects, or personal Substack blogs
- 1-2 years using GPU or TPU clusters and/or running a multi-tenant GPU cluster
- Past experience working at a hyperscaler or a GPU cloud (preferred)
- Solid understanding of SLURM, Kubernetes, NCCL & GPU Cloud industry
- Strong research skills and the ability to synthesize information from various sources to draw insights

Compensation is competitive & as part of the interview process, you'll complete a paid coding challenge designed to reflect typical daily tasks at SemiAnalysis

[Apply Here](https://app.dover.com/apply/SemiAnalysis/f4631653-e731-4e16-823b-eec3c5d90eba/?rs=76643084)

---

## Colossus 2: from zero to 200MW in six months

The Colossus 2 project was kicked off on March 7th, 2025, when xAI acquired a 1m sqft warehouse in Memphis, and two adjacent sites totaling 100 acres. By August 22nd, 2025, we count 119 air-cooled chillers on site, i.e. [roughly 200MW of cooling capacity](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/#air-cooled-and-water-cooled-chillers). That's enough to power roughly 110k GB200 NVL72. And [an Elon tweet](https://x.com/elonmusk/status/1947715674429919279) shows some racks were already installed in July.

xAI built in six months what [took 15 months for Oracle, Crusoe and OpenAI!](https://semianalysis.com/datacenter-industry-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/5eee61f4-1b16-4664-966a-e07eae116158_1024x832.png)
*Source: SemiAnalysis Datacenter Industry Model*

Looking closer at the picture above, [readers familiar with our Datacenter Anatomy series](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/) might wonder where the power infrastructure is. The picture doesn’t show any onsite substation, nor does it show onsite turbines…  How is the datacenter powered?

## Colossus 2: in Tennessee, Mississippi… or both?

Things get more confusing once factoring-in a [Greater Memphis Chamber statement in May](https://www.actionnews5.com/2025/07/22/xai-begins-installing-computing-infrastructure-colossus-2/#:~:text=Colossus%202%20is%20expected%20to,within%20the%20next%20few%20weeks) that **no turbines would be sited in Memphis**. They’re not lying.

Memphis and Tennessee have been getting a lot of pushback, so xAI’s genius move was to develop a Gigawatt-scale energy hub **right across the border** in **Southaven, Mississippi**. In mid-2025, the company acquired a former Duke Energy power plant in Southaven. Shortly after, **Mississippi** regulators [granted](https://512pixels.net/2025/08/xai-turbines-southaven/#:~:text=,the%20Mississippi%20Public%20Records%20Act) xAI temporary approval to run gas turbines there for up to 12 months without a permit!

![](https://substack-post-media.s3.amazonaws.com/public/images/052bac5a-a53f-4054-ac0d-574181eb0481_712x1024.png)
*Source: SemiAnalysis Datacenter Industry Model*

To transport and manage power generated by the Mississippi power plant, xAI is building infrastructure near Colossus 2. We show below the first deployment of Tesla Megapacks, as well as the Medium Voltage power lines connecting the two sites.

![](https://substack-post-media.s3.amazonaws.com/public/images/c6d8454a-f182-4bb1-abc1-7293803e7ea5_1024x938.png)
*Source: SemiAnalysis Datacenter Industry Model*

## From 200MW to 1.1GW and Solaris Energy Infrastructure partnership

In Southaven, MS, xAI is moving at the pace of light. The discontinued power plant now sees seven 35MW turbines in operations.

![](https://substack-post-media.s3.amazonaws.com/public/images/c5f17aae-5cff-4c9d-94e3-fd79422fd36d_1024x542.png)
*Source: SemiAnalysis Datacenter Industry Model*

To deploy faster than peers, xAI relies on rental turbine companies. NYSE-listed Solaris Energy Infrastructure owns a fleet of 600MW of gas turbines, of which ~400MW currently serve xAI. Musk's firm weighs 67% of SEI's 1700MW orderbook, i.e. 1,140MW. There are ~240MW on the Memphis Colossus 1 site, while the remaining 900MW will be owned by a Joint Venture owned at 50.1% by Solaris and 49.9% by xAI.

![](https://substack-post-media.s3.amazonaws.com/public/images/01fbd1e6-74c2-4155-887c-9a58369984fd_1024x451.png)
*Source: Solaris Energy Infrastructure*

As shown below, ~460MW are currently installed and in operations/under construction.

![](https://substack-post-media.s3.amazonaws.com/public/images/40744dbf-04f6-4852-b56e-5e05f66c087d_1024x555.png)
*Source: SemiAnalysis Datacenter Industry Model*

The newly formed JV already spent $112 million in capital expenditures in Q2 2025. After a slow Q3, spending will pick up again in Q4 2025 and Q1 2026. Solaris expects to have over 1.1GW of fully operating turbines for xAI by Q2 2027. There remains ~425MW available for contracting, and we think xAI will likely pull the trigger to get to over 1.5GW of total gross power. Solaris also appears to temporarily lease power generation capacity from third parties to deliver faster:

> *During the second quarter, the Power Solutions segment generated revenue from approximately 600 megawatts of capacity, an increase of greater than 50% from the prior quarter. This increase was driven by increased demand from our customers, which we are meeting using a combination of new equipment deliveries as well **as selective short-term sourcing of third-party power generation capacity**.*

Solaris Energy Infrastructure, Q2 2025

![](https://substack-post-media.s3.amazonaws.com/public/images/fab97fc5-05b0-4883-9245-d991eeecd62c_1024x549.png)
*Source: Solaris Energy Infrastructure*

As such, xAI has figured out how to scale to >1GW from a power perspective. In terms of datacenter space, we see four options:

- Given a 40ft height, xAI could turn their 1mm sqft warehouse into a two-story datacenter, doubling the space. Given ultra-high density, 2mm sqft could be enough for >1GW.
- xAI could build a second, smaller facility in parcel 3
- They could acquire more land, possibly in Mississippi near the Southaven plant.
- Using non-standard layout of the datacenter, they could achieve >1GW as is.

![](https://substack-post-media.s3.amazonaws.com/public/images/d2988a90-87eb-4331-a916-069a859b210a_1024x736.png)
*Parcels of land owned by xAI at the Colossus 2 site*

## Can xAI afford Colossus 2?

Further expansion will require ample funding. Required CapEx for Colossus 2 will be in the tens of billions of dollars, and xAI is yet to generate any meaningful external revenue, with the preponderance of the rumored 9 digit revenue ARR being inter-company transfers from X.com to xAI. We’ve forecasted xAI’s CapEx on [Core Research, our institutional research service](https://semianalysis.com/core-research/) and are now closely tracking the [ROIC of AI investments across the hyperscalers and AI labs in our new Tokenomics model](https://semianalysis.com/tokenomics-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/74fb771a-5d3d-4b0b-9927-1f645de02c10_1024x512.png)
*Source: SemiAnalysis Tokenomics Model Estimates*

### Middle East – funding + datacenters, a winning combination?

To be clear, in typical xAI & Elon fashion, the company’s future is highly unpredictable. But given funding needs, we see a large-scale expansion in the Middle East as likely. Musk and the Middle have a long-time relationship:

- KSA’s Kingdom Holding Company (owned at 16.87% by the Public Investment Fund) owned and kept a $1.9B stake in Twitter when Musk took the company private in 2022. It also owned a $800M stake in xAI prior to the merger with X.
- UAE’s privately owned Vy Capital brought in $700M in 2022 to support Elon’s takeover of Twitter. It also invested in xAI’s Series C, alongside UAE state fund MGX.
- Qatar’s QIA also owned and kept a $375M stake in Twitter, and participated on xAI’s Series C.

[According to the FT](https://www.reuters.com/business/musks-xai-seeks-up-200-billion-valuation-next-fundraising-ft-reports-2025-07-11/#:~:text=Saudi%20Arabia%27s%20PIF%20sovereign%20wealth,million%20investment%20in%20the%20firm), xAI is preparing a new round in the tens of billions, valuing the company close to $200B, with Saudi’s PIF sovereign wealth fun playing a large role. This is challenging though because its hard for most investors to justify xAI as having a valuation higher than Anthropic.

We've heard of a raise as large as $40B. Given skyrocketing datacenter growth in the area, we see a two-way deal as likely, with xAI deploying that capital in a new large scale datacenter in the Kingdom.

![](https://substack-post-media.s3.amazonaws.com/public/images/c454a625-3380-422c-ad7d-a771c7b72e53_1024x526.png)
*Source: SemiAnalysis Datacenter Industry Model*

We show below a likely location for xAI’s expansion, a large-scale planned located Saudi Arabia that recently broke ground. While still early, there is plenty of land and power to serve large-scale AI campuses.

![](https://substack-post-media.s3.amazonaws.com/public/images/b167e795-070a-421b-90f7-b1bd87de76fc_1024x452.png)
*Source: SemiAnalysis Datacenter Industry Model*

For more details on the Middle East’s AI expansion, check out our May 2025 deep dive.

Beyond external capital sources, Elon could generate capital internally. Since merging X.com with xAI to form X Holdings, we believe an ever growing piece of xAI's revenues is inter-company transfers, i.e. calls to @Grok to answer questions or just X.com licensing the LLM technology for functionality such as search, ad recsys, or even content creation.

This is just money going from Elon's right pocket to his left pocket. From what we can track externally, Ani was a huge boon for Grok app revenue but even growth in that revenue stream has flattened out in recent months. Ani needs more gacha to grow revenue further.

![](https://substack-post-media.s3.amazonaws.com/public/images/dbaaab2c-2842-4779-be4f-6fa4bcfb959b_1024x512.png)
*Source: SemiAnalysis estimates and Sensortower*

At the end of the day, Elon can get Tesla to invest more or take loans on more of his Tesla and SpaceX stocks to invest tens of billions into xAI. This will allow them to build Colossus 2. No one truly knows how levered Elon is already, but it is widely understood he can always sell and unlock a lot more of his dry powder into xAI. Elon will do everything he can to not lose to Sam Altman.

Let’s now discuss xAI as a business and whether we think the company has a shot at being a Frontier AI Lab and justifying a multi-hundred-bullion dollar valuation. We have some unique info and insights below and why they may have a shot at being first to AGI due to their different approach.

## Does xAI have a shot at becoming a frontier lab?

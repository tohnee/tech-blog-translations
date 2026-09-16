---
title: "Gemini is Cooked but GCP is Cooking"
subtitle: "GCP YoY rev growth >100%, DeepMind's long term failure is Google Cloud's short term gain"
date: 2026-08-07
source: https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking
crawled: 2026-09-15
authors: ["Max Kan", "Joey Brookhart", "Doug O'Laughlin", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Gemini is Cooked but GCP is Cooking

**GCP YoY rev growth >100%, DeepMind's long term failure is Google Cloud's short term gain**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

On Wednesday, August 5th, Google [announced](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/) a complete overhaul of DeepMind leadership. A quick recap:

- Demis Hassabis, DeepMind co-founder and former CEO, is no longer involved in day-to-day operations.
- Jeff Dean, former Google Chief Scientist and Gemini co-lead is leaving to start a neolab called Discovery Loop. Jeff is the undisputed GOAT of Google engineering, co-founded Google Brain, and started the TPU program.
- Joining Jeff are Sanjay Ghemawat, Quoc Le, and Oriol Vinyals. Sanjay and Quoc were both Google Fellows, which is a title reserved for the company’s top dozen or so technical contributors.[1](#footnote-1) Oriol was a Gemini co-lead.
- Koray Kavukcuoglu, former DeepMind CTO and the one remaining Gemini co-lead, is replacing Demis as the leader of DeepMind/Gemini.

Obviously these are not the actions of people excited about Gemini 4 Pro.

For all intents and purposes, we believe **DeepMind is no longer a frontier lab**. We said as much a few months ago to our [Tokenomics](https://semianalysis.com/tokenomics-model/) clients due to large numbers of departures from their reinforcement learning teams and poor compute allocation. Google will continue meandering on and releasing models, but their odds of reaching SOTA again have dropped to zero.

Furthermore, the **biggest beneficiary** of today’s news is neither Anthropic nor OpenAI—it’s **Google Cloud**. Whereas Gemini and GCP used to desperately fight for compute allocation, it’s now clear that Thomas Kurian won. **We expect GCP revenue growth to meaningfully accelerate as a result**.

## Gemini 3 Pro was the peak

At the end of 2025, Anthropic, OpenAI, and Google were the clear AI big 3. Some still held this opinion as recent as last week, but the downfall of Gemini in 2026 was clear to those paying attention. Here’s an excerpt from an [institutional note](https://semianalysis.com/institutional/googles-fall-from-grace-why-gemini-3-pro-was-the-top-plus-some-thoughts-on-openai-msl-and-spacexai/) we published to our [Tokenomics Model](https://semianalysis.com/tokenomics-model/) subscribers on **July 9th**:

> - In November 2025, Gemini 3 Pro was arguably the best model in the world, forcing Sam Altman to issue a “code red” at OpenAI.
> - Since then, the gap between Deepmind and OpenAI/Anthropic has widened dramatically. Gemini 3.5 Flash was a total flop, and **industry chatter suggests the upcoming Gemini 3.5 Pro is roughly Opus 4.5 level**. This is quite literally worse than GLM 5.2, much less Fable 5 and GPT 5.6.
> - We believe things will only get worse for Gemini, as Google lacks the religious conviction necessary for building RSI. We think it’s likely both MSL and SpaceXAI surpass them in model quality by the end of this year.
> - Along with Noam Shazeer and John Jumper, most of the best RL people at Gemini recently left the company.
> - OpenAI has overcome their pre-training issues, and a much larger model code named “Doug” is actively in the works.

The second to last point is worth emphasizing. Jeff, Sanjay, Quoc, and Oriol are just the latest in a long string of high profile departures from DeepMind. Despite discovering most of the foundational breakthroughs behind the current LLM paradigm, Google is now simply unable to retain top AI talent.

Notably, Jeff and co. have followed a playbook to create their neolab, Discovery Loop, that was established by David Silver of Ineffable Intelligence in November last year. To pursue their mission, top AI researchers are now choosing to leave Google, raise billions from outside investors and Google Ventures, and then spend that money on Nvidia GPUs in GCP.

Since our [institutional note](https://semianalysis.com/tokenomics-model/), Google has silently canceled Gemini 3.5 Pro and is now [coping](https://x.com/OfficialLoganK/status/2079594867161022817?s=20) by hyping up Gemini 4 instead. As a bridge model, they released Gemini 3.6 Flash, but it’s generally worse than Muse Spark 1.2, Grok 4.5, and the tier 1 Chinese open-source models. Depending on how you count, Gemini is currently in 8th or 9th place, and we don’t see Gemini 4 reversing their downfall.

![](https://substack-post-media.s3.amazonaws.com/public/images/4c11127d-75d3-4b40-8ffa-8edbaab508b3_1976x1108.png)
*Source: Artificial Analysis*

At the same time, Gemini first-party API token growth has famously decelerated. Whereas they grew 60% in [1Q26](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q1-2026/), going from 10B to 16B tokens per minute, [2Q26](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/) saw just 38% growth to 22B. This has caused a corresponding decline in Gemini 1P API revenue growth.

![](https://substack-post-media.s3.amazonaws.com/public/images/eaf8ff61-9043-4226-b3e3-f296d8dd1b88_1955x918.png)
*Source: SemiAnalysis Tokenomics Model*

However, **Gemini Enterprise Agent Platform** (formerly Vertex) **has been meaningfully stronger overall** thanks to third-party models like Claude. To see a full breakdown of Amazon Bedrock, Microsoft Foundry, and Google Vertex revenue separated by model provider, as well as all the implications for OpenAI and Anthropic, see our [Tokenomics Model](https://semianalysis.com/tokenomics-model/).

### **There’s no substitute for conviction**

We believe Gemini’s core issue has always been a fundamental lack of conviction. Compute is the lifeblood of AI progress, and all the AGI-pilled labs are desperately trying to acquire as much as possible.

Of course, pre-paying multiple GWs is also very scary and expensive, especially if you don’t have a rapidly growing, high margin API business. However, as we’ve explained in [previous](https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence) [newsletters](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be), there are creative ways to overcome this limitation and still monetize excess capacity at very attractive rates **while maintaining the optionality to claw everything back for your research team**. Explicitly, this is what we see happening at Meta and SpaceX.

Google, on the other hand, decided it was totally worth it to sell enormous amounts of compute to Gemini’s fiercest competitors on long term contracts without any hope of ever returning it to DeepMind.

More than 20% of total TPU shipments from 3Q26 to 4Q27 are being sold directly to Anthropic.[2](#footnote-2) This is excluding the hundreds of thousands of TPUs GCP already rents to Anthropic today, and the many hundreds of thousands more they’ve committed to rent to Anthropic and Meta over the next 6 quarters.

![](https://substack-post-media.s3.amazonaws.com/public/images/f2873391-8508-4334-bd3e-5964ff75a1cd_2075x1013.png)
*Source: SemiAnalysis Accelerator Model*

For full details on the number of TPUs, GPUs, Trainiums, etc being produced each quarter till 2030 and their end customers, see our [Accelerator Model](https://semianalysis.com/accelerator-hbm-model/).

If you’ve ever listened to an interview of Google Cloud CEO Thomas Kurian, you know he is not AGI pilled. In one [podcast](https://www.youtube.com/watch?v=bNdiBwXbLNw), for example, he argued that it’s great for TPUs to become “general purpose infrastructure” that supports customers like Citadel, the Department of Energy, and generic high performance computing. And when asked why he was selling compute to Anthropic despite them competing with Gemini, he said this was the natural consequence of Google being a “platform company.”

This same man likely just won a major internal political battle to have even more control over Google’s compute allocation.

### **Attempting to steelman DeepMind’s frontier ambitions**

We’ve obviously been quite bearish on DeepMind thus far, and if we had to steelman the case for why they’ll still be able to train a true SOTA model in the future, it would go something like the following:

- The current setup clearly wasn’t working. With the existing leadership team, their odds of catching up to Anthropic/OpenAI looked extremely slim.
- Now that they’ve cleaned house, the new guys can start from a blank slate. Maybe they’ll even acqui-hire a neolab like SSI or Thinking Machines.
- With this new team, their odds of catching up to the frontier actually increase.

Perhaps there’s some world in which this happens, but we think the odds are basically zero. The issue with Google was not Jeff Dean nor Noam Shazeer, but rather their extremely bureaucratic, painfully slow, and strategically timid culture. [Remember](https://x.com/thsottiaux/status/2083596911060324570) that DeepMind had an AI chatbot 1 year before ChatGPT but was not allowed to release it due to fears of disrupting their core business.

![](https://substack-post-media.s3.amazonaws.com/public/images/03c20d1a-8bcf-4861-a8dc-0a96d2963392_1041x745.png)
*Source: Tibo on X*

Tibo, funny enough, is another great example of brain drain from Google. A 9 year Google/DeepMind veteran, he left in July 2024 to join OpenAI, co-led the original coding agent team, and is now the head of Codex. Meanwhile, Google “acquired” Windsurf to build its own agentic coding platform in July 2025, and they don’t exactly have much wind in their sails thus far.

Let’s also not forget that DeepMind was the original AI acqui-hire! And with the benefit of 12 years’ hindsight, we now know how that played out. Adding another neolab to the roster would likely just result in more of the same.

## The Financialization of GCP

Our [Tokenomics Model](https://semianalysis.com/tokenomics-model/) estimates that Gemini ARR was $12B in 2Q26. In contrast, by the end of 2027, GCP will be doing over $73B in third party AI ARR IaaS/TaaS and another $120B of TPU sales. **$200B of external sales at high 30s EBIT margins vs a first party business generating just $12B today shows where the focus is**. Google management is clear: the short term benefits from focusing GCP on financialization is worth abandoning any long term competitiveness at the frontier.

![](https://substack-post-media.s3.amazonaws.com/public/images/d1799850-cdf8-4545-9eb8-a1641666892f_2187x1094.png)
*Source: SemiAnalysis Tokenomics Model*

Despite the weaknesses with Gemini, GCP continues to accelerate. This last quarter, GCP growth was 82%. However, that wasn’t all from what we would traditionally call the “cloud” business. GCP has a new revenue source in selling full systems of its TPUs to external SPVs that run datacenters for customers such as Anthropic. **These TPU sales are accounted for on a gross basis at ~$35B/GW**. In 2Q26, we estimate that TPU sales were around $1.2B in the quarter, and thus core GCP grew in the low 70s. Given over $150B of TPU systems backlog, **these TPU system sales will drive GCP’s 2027 growth rate into the mid 100s vs sellside consensus at 64%**.

![](https://substack-post-media.s3.amazonaws.com/public/images/1cc76e1d-e524-4ba4-9744-c1d64400edd6_1987x980.png)
*Source: SemiAnalysis Tokenomics Model*

Although EBIT margins for these system sales are slightly lower than core cloud margins in the low 30% range, we still expect total GCP to deliver mid to high 30s EBIT margins going forward. How investors decide to capitalize the current TPU backlog and any large future sales is an open question. However, given the strong compute demand from labs, we expect more multi-GW deals to be announced soon adding to this backlog. In all, **we estimate that over $250B of additional TPU Bookings could be added to GCP RPO in coming quarters**. Until then, this eye-popping acceleration in GCP growth coupled with good margins will **add ~$3 to Google EPS in 2027**.

For an even more detailed breakdown of Amazon, Microsoft, and Oracle’s cloud businesses, as well as updated Google projections come earnings season, see our [Tokenomics Model](https://semianalysis.com/tokenomics-model/).

## Be Careful What you Wish For

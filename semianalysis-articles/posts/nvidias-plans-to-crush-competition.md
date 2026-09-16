---
title: "Nvidia’s Plans To Crush Competition – B100, “X100”, H200, 224G SerDes, OCS, CPO, PCIe 7.0, HBM3E"
subtitle: "Roadmap, Supply, Anti-competitive: AMD, Broadcom, Google, Amazon, and Microsoft Have Their Work Cutout For Them"
date: 2023-10-10
source: https://newsletter.semianalysis.com/p/nvidias-plans-to-crush-competition
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
---

# Nvidia’s Plans To Crush Competition – B100, “X100”, H200, 224G SerDes, OCS, CPO, PCIe 7.0, HBM3E

**Roadmap, Supply, Anti-competitive: AMD, Broadcom, Google, Amazon, and Microsoft Have Their Work Cutout For Them**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Nvidia’s AI solutions are currently at the top of the world, but disruption is coming. Google has unleashed an [unprecedented plan of building out their own AI infrastructure](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion). We exclusively detailed [volumes](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini) and [dollar amounts](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion) for Google’s TPUv5 and TPUv5e buildout for both internal use in training/inference as well as for [external customer usage](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini) from firms such as [Apple](https://stratechery.com/2023/an-interview-with-doug-olaughlin-and-dylan-patel-about-semiconductors-and-ai/), Anthropic, CharacterAI, MidJourney, Assembly, Gridspace, etc.

Google isn’t the only rising threat to their dominance in AI infrastructure. On software, [Meta’s PyTorch 2.0 and OpenAI Triton](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch) are barreling forward allowing other hardware vendors to be enabled.

AMD’s GPUs, Intel’s Gaudi, Meta’s MTIA, Microsoft’s Athena are all at various stages of maturity in their software stack, but it is clear. The software gap although still relevant, is nowhere close to as big as was in the past. While Nvidia still maintains the hardware lead, that is going be closed very soon too. Both AMD’s MI300 and Intel’s Gaudi 3 are launching with technically superior hardware compared to Nvidia’s H100 within the next few months.

Even outside of Google, AMD, and Intel, Nvidia also faces competitive pressure from firms who are behind in hardware design, but will be subsidized by the behemoths behind them who want to try to escape Nvidia’s margin stacking on HBM. Amazon is launching their [Trainium2 and Inferentia3](https://www.semianalysis.com/p/amazon-anthropic-poison-pill-or-empire) and Microsoft is launching [Athena](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and) soon. We talked through [the supply chain and next years volumes for those in July](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and), but these are multi-year investments that will not slow down going forward.

Nvidia saw the writing on the wall years ago. The tech giants have been trying to displace all their hardware needs and eat Nvidia’s lunch.

**Under that lens, there is a very legitimate argument to hear that Nvidia will not be able to maintain their market share or margins going forward due to this competitive threat.**

Of course, Nvidia isn’t sitting on their hands. While Nvidia is extremely successful, they are also one of the most paranoid firms in the industry, from management style to roadmap decisions. Jensen Huang embodies the spirit of Andy Grove.

> Success breeds complacency. Complacency breeds failure. Only the paranoid survive.
>
> Andy Grove

As such, Nvidia embarked on a very ambitious and risky multi-pronged strategy to remain atop the market for AI hardware. Nvidia’s plan are to transcend the comparisons with traditional competitors like Intel and AMD and ascend to the rank of tech giants. They want to become a peer of Google, Microsoft, Amazon, Meta, and Apple. [Nvidia’s DGX Cloud](https://www.semianalysis.com/i/137441303/nvidias-dgx-cloud-business-model-software-as-a-service), [software](https://www.semianalysis.com/i/137441303/nvidias-healthcare-push-a-front-row-seat), and [non-semiconductor acquisition strategy](https://www.semianalysis.com/p/nvidia-buys-illumina-the-ai-foundry) is one to watch closely.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

This report walk through this multi-faceted strategy from Nvidia, specifically on their hardware roadmap for the next couple years with the upcoming H200, B100, and “X100” GPUs. Nvidia’s move to annual updates on AI GPUs is very significant and has many ramifications. We will talk through Nvidia’s process technology plans, HBM3E speeds/capacities, PCIe 6.0, PCIe 7.0, and their incredibly ambitious NVLink and 1.6T 224G SerDes plans. If this plan is successful, Nvidia blows everyone out the water.

We will also include an discussion into the competitive dynamics and large wins of AMD’s MI300. We will also talk through AMD’s cancelled MI350X and future MI400 as well as other competing chips such as Amazon’s Trainium2, Microsoft’s Athena, and Intel’s Gaudi 3.

There is an important discussion to be had on Nvidia’s business tactics which some may even view as anti-competitive with regards to sales strategies and bundling. Nvidia’s strategic sourcing is also amazing to watch with regard to supplier management, CoWoS/HBM capacity acquisition, and development of specialized technologies such as optical switches and co-packaged optics.

![](https://substack-post-media.s3.amazonaws.com/public/images/486c51a2-195a-4d4a-ba7a-281140c9bf64_2208x1230.png)
*Nvidia Slide*

The roadmap centric discussion will go more into the technical and competitive position, let’s start with Nvidia’s supply chain mastery and business tactics.

## **Supply Chain Mastery – Jensen Always Bets Big**

One thing we really respect about Nvidia is that they are masters of supply chain. They have shown multiple times in the past that they can creatively ramp their supply during shortages.

Nvidia has secured immense supply by being willing to commit to non-cancellable orders or even make prepays. Nvidia has [$11.15 billion of purchase commitments, capacity obligations, and obligations of inventory](https://s201.q4cdn.com/141608511/files/doc_financials/2024/Q2FY24/Q2FY24-CFO-Commentary.pdf). [Nvidia also has an additional $3.81 billion of prepaid supply agreements](https://s201.q4cdn.com/141608511/files/doc_financials/2024/Q2FY24/Q2FY24-CFO-Commentary.pdf). No other vendor comes even close, and so they won’t be able to partake in the frenzy that is occurring.

Ever since the early days of Nvidia, Jensen has been aggressive with his supply chain in order to fuel Nvidia’s massive growth ambitions. Look no further than Jensen retelling his early meetings with Morris Chang, TSMC’s founder.

> In 1997, when [Morris] and I met, Nvidia was completed that year with $27 million in revenues. We had 100 people and then we met and you guys probably don't believe this but Morris used to make sales calls. You used to make house calls, right? And you would come in and visit customers and I would explain to Morris what it is that Nvidia did and, you know, I would explain how big our die size needed to be and that, every year, it was going to get bigger and bigger and bigger. You would come back to Nvidia periodically to make me tell the story over again just to make sure that I'm going to need that many wafers and, next year, we started working with TSMC. Nvidia did, I think it was 127 million and then, from that point forward, we grew nearly 100% per year until now. I mean, our compounded annual growth rate over the last 10 years was 70-some odd percent.
>
> [Jensen Huang in conversation with Morris Chang, Computer History Museum, 2007](https://www.youtube.com/watch?v=u-x7PdnvCyI)

![](https://substack-post-media.s3.amazonaws.com/public/images/8278a1db-d3ba-407c-8652-294fbc3b2e7c_3600x1685.jpeg)
*Comic commissioned by Nvidia commemorating Morris Chang’s retirement, you can see the full version here*

Morris Chang couldn’t quite believe that Nvidia needed so many wafers, but Jensen persisted and capitalized on the massive growth of the gaming industry at that time. Nvidia has been hugely successful by being [bold on supply](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing), and usually it’s worked out for them. Sure they have to do [write downs worth billions in inventory from time to time](https://nvidianews.nvidia.com/news/nvidia-announces-preliminary-financial-resultsfor-second-quarter-fiscal-2023), but they still netted out positive from their over ordering affairs. If something works, why change it?

This go around Nvidia has grabbed the majority of supply for upstream components of GPUs such as SK Hynix, Samsung, and Micron HBM. They have placed very large orders with all 3 HBM suppliers and are crowding out supply for everyone else besides [Broadcom/Google](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion). We will discuss more about the HBM3E in roadmap section.

Nvidia has bought up the majority of TSMC’s CoWoS supply. They didn’t stop there, they also went out and investigated and bought up Amkor’s capacity. We detailed this [here](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and).

One of the detailed models we offer to clients/sell is a database that flows through HBM and CoWoS capacity by quarter for Nvidia, Alchip, Marvell, Broadcom, Microsoft, AMD, Cisco, T-head, Sanechips, Renesas. and GUC. It shows dies per wafer, yields, HBM volumes, accelerator volumes, ASPs, and revenue for all major hardware vendors and hyperscalers chips. We source this data from the firms, server ODMs, foundries, substrate suppliers, and the [28 different equipment vendors involved in the HBM and CoWoS manufacturing supply chain](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis).

Nvidia has also capitalized on the many downstream components that are required for their HGX boards or servers, such as retimers, DSPs, optics, and more. Suppliers who balk at Nvidia’s demands are generally met with a carrot and a stick. On one side they can have what seems like unimaginable orders from Nvidia, on the other side, they face being designed out of Nvidia’s existing supply chain. They only use commits and non-cancellable when their supplier is critical and cannot be designed out or multi-sourced.

Part of the reason every vendor seems to think they are an AI winner is because Nvidia is ordering a lot from all of them, and they all think they won a majority of the business, but in reality, Nvidia is ramping up so fast.

Going back to the dynamics in the market above, while Nvidia is aiming to have supply for over $70 billion of datacenter sales next year, only Google has enough capacity upstream to have meaningful units on the scale of over 1 million. Even after AMD’s latest revisions up for capacity, their total capacity in AI is still very tame, with low hundreds of thousands units maximum.

## **Business Tactics – Potentially Anti-Competitive**

It’s no secret that Nvidia is taking advantage of the massive demand for GPUs by using it to upsell and cross sell customers. Many sources in the supply chain tell us Nvidia is giving preferential allocation to firms based on a number of factors, including but not limited to: multi-sourcing plans, plans to make their own AI chips, [buying Nvidia’s DGX](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing), NICs, [switches](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai), and/or [optics](https://www.semianalysis.com/p/nvidias-optical-ascent-1b-revenue). We detailed this in the [Amazon Cloud Crisis report from March](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will).

Infrastructure providers such as CoreWeave, Equinix, Oracle, AppliedDigital, Lambda Labs, Omniva, Foundry, Crusoe Cloud, and Cirrascale are being pointed the allocation cannon in volumes that are far closer to their potential demand than the mega tech firms like Amazon.

Nvidia’s bundling is so successful in fact, that despite previously being a very small supplier of optical transceivers, [they tripled their business in 1 quarter and are on pace to ship over $1B](https://www.semianalysis.com/p/nvidias-optical-ascent-1b-revenue) worth over the next year. This far outstrips the growth rate of their GPU or networking silicon businesses.

These tactics are quite well thought out, for example currently, the only way to achieve 3.2T networking with reliable RDMA/RoCE on an Nvidia system is with Nvidia’s NICs. This is mostly due to Intel, AMD, and Broadcom’s lack of competitiveness, with them being stuck at 200G still.

Opportunistically, Nvidia has managed their supply chain so that their 400G InfiniBand NICs are markedly lower lead time than their 400G Ethernet NICs. Keep in mind the silicon and board design is identical for both NICs (ConnectX-7). This is mostly down to Nvidia’s configuration of SKUs, not actual supply chain bottlenecks. This forces firms to buy Nvidia’s more costly InfiniBand switches, rather than going to standard Ethernet switches. Nvidia makes an exception when you buy their Spectrum-X Ethernet network with Bluefield-3 DPU’s in NIC mode.

It doesn’t stop there either, just look how [intoxicated the supply chain is on L40 and L40S GPUs](https://www.semianalysis.com/i/136248981/l-overhyped). We [wrote about this here](https://www.semianalysis.com/i/136248981/l-overhyped), but since then we have heard more about Nvidia’s allocation shenanigans.

For those OEMs to win larger H100 allocation, Nvidia is pushing the L40S. Those OEMs face pressure to buy more L40S, and in turn receive better allocations of H100. This is the same game Nvidia played in PC space where laptop makers and AIB partners had to buy larger volumes of G106/G107 (mid-range and low-end GPUs) to get good allocations for the more scarce, higher margin G102/G104 (high-end and flagship GPUs).

Many in the Taiwan supply chain are being fed the narrative than the L40S is better than an A100, due to it’s higher FLOPS. To be clear, those GPUs are not good for LLM inference because they have less than half the memory bandwidth of the A100 and no NVLink. This means running LLMs on them with good TCO is nigh on impossible save for very small models. High batch sizes have unacceptable tokens/second/user making the theoretical FLOPS useless in practice for LLMs.

OEMs are also being pressured to support Nvidia’s MGX modular server design platform. This effectively takes all the hard work out of designing a server, but at the same time, commoditizes it, creating more competition and driving down margin for the OEM. Firms like Dell, HPE, and Lenovo are obviously resistant to MGX, but the lower cost firms in Taiwan such as SuperMicro, Quanta, Asus, Gigabyte, Pegatron, and ASRock are rushing to fill in that void and commoditize low cost “enterprise AI”.

Conveniently, these OEMs/ODMs participating in L40S and MGX hype games also get much better allocations of Nvidia’s mainline GPU products.

## **Roadmap – B100, “X100”, H200, HBM3E, 200G SerDes, PCIe 6.0, Co-Packaged Optics, Optical Switch**

The majority of this report is the juicy details of Nvidia’s new roadmap including details on the networking, memory, packaging, and process nodes utilized, various GPUs, SerDes choices, PCIe 6.0, co-packaged optics, and optical circuit switches. This includes multiple sides beyond just the one below.

![](https://substack-post-media.s3.amazonaws.com/public/images/5a6a32a8-52e5-4797-afe8-ed85dcb37937_2208x1230.png)

Due to competitive pressures from Google, Amazon, Microsoft, AMD, and Intel, we believe Nvidia accelerated their plans for B100 and “X100”. In response to this accelerated time schedules for Nvidia, we hear AMD completely cancelled their MI350X plans. Going back to the technical specifications we [exclusively detailed for the configurations of MI300](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance).

The modular XCD building block is 40CUs and on TSMC’s 5nm process technology. AMD used to have the MI350X which had the same AIDs, but different XCDs, that were on TSMC’s 3nm. That part was cancelled for a variety of reasons, including that it would be completely uncompetitive with B100, when you compare the two’s on paper specs.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

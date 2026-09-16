---
title: "Thick Cables, Thin Margins – Microsoft, Amazon, and Google Demand Overstated By $CRDO Credo"
subtitle: "Future Demand Booming But Active Electrical Cables Are Not The Salvation"
date: 2023-02-15
source: https://newsletter.semianalysis.com/p/thick-cables-thin-margins-microsoft
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
---

# Thick Cables, Thin Margins – Microsoft, Amazon, and Google Demand Overstated By $CRDO Credo

**Future Demand Booming But Active Electrical Cables Are Not The Salvation**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Faster networking speeds have come like clockwork every ~3 years in the datacenter, but scaling is starting to hit some difficulties, especially due to the voracious demand for AI and large language models. The cost of networking is scaling exponentially faster than the cost of CPUs or memory, which has led to a ballooning in datacenter costs. This presents a fundamental problem that requires immediate attention. Vendors such as Nvidia, Intel, AMD, and Broadcom are tackling this from the standpoint of NICs and Switches, but those aren’t the only solution spaces.

One of the biggest issues that datacenter architects are facing is with cables. Each networking generation from 8x25G to 4x50G to 4x100G is causing problems with passive direct attached copper (DAC) cables. As data transfer speeds increase, the cables are becoming wider and larger, containing more copper. Furthermore, these cables are becoming less reliable, and error rates are climbing. Copper is starting to run out of steam, and it is becoming more and more challenging to use.

Moving to a different form of cabling is necessary to address this issue. The obvious choice is optical fiber. The biggest challenge is that optical transceivers are far too expensive. Optical will continue to be used heavily for connecting various server racks together, but connecting servers to the switch in a rack becomes cost prohibitive. We will be discussing optical DSP, cost, and bandwidth scaling at OFC San Diego in a couple of weeks if anyone is interested in meeting the team.

Today we will discuss the solution, active electrical cables (AEC), and their future use by Amazon, Microsoft, and Google. Furthermore, we will cover the competitive landscape of AEC and ACC products as well as the firms in the space, including Credo ( ), Astera Labs, Marvell (), Broadcom ( ), Maxlinear (), Point2, Spectra7, Macom (), Semtech (), and Alphawave Semi (£AWE.L). Lastly, we will discuss the SerDes IP used by these players.

![](https://substack-post-media.s3.amazonaws.com/public/images/410efec6-d4d8-4474-b9a8-a7bf6d8a474f_1024x523.jpeg)

To further demonstrate the issue facing passive copper, imagine an [Nvidia HGX A100 server deployed by Microsoft for use by OpenAI to train large language models](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit). These contain 8 200G or 400G networking interface cards in a 4U server enclosure. As many as 8 of these servers are placed in a single rack, depending on rack power/cooling architecture, and connected to 1 or more networking switches. The cabling density is so high in the rack itself that it can be challenging to use passive copper simply due to cable thickness. This necessitates longer, more cluttered cable runs, leading to signal weakening, worse cooling, and increasing error transmission unless exceptional care is given to the design.

![](https://substack-post-media.s3.amazonaws.com/public/images/4b1b60cb-97da-41f0-904b-9dea4882e593_800x501.jpeg)

Furthermore, similar issues could be faced even in standard CPU compute servers. When looking forward to the [AMD Genoa-based servers with 400G NICs](https://www.semianalysis.com/p/amd-genoa-detailed-architecture-makes) installed at Google, Microsoft, and Amazon, the same problem could crop up if the density of servers is high. For now, passive direct attached copper (DAC) still works outside extremely high-density plays, even for 4x100G. Some mitigation strategies include moving the top-of-rack (TOR) switch to the middle, dramatically reducing the average cable length, and enabling moving back to a more reasonable gauge DAC.

Andy Bechtolsheim, the founder of Sun and Arista Networks, always says that passive copper will always last one more generation, and it continues to do so. This applies to the 200G and 400G generation for the most part.

Even with this mitigation, there are other reasons to use AEC over DAC. Reliability is a crucial metric. In the current server rack architecture, a single TOR switch connects every server in a rack to the broader network. There is a single point of failure. According to this joint presentation by Microsoft and Credo, 2% of these to switches fail within the first three months.

![](https://substack-post-media.s3.amazonaws.com/public/images/da953e10-e276-4594-bc66-5f6b27280de7_2330x1304.png)

If there is a failure in the TOR switch, then every server in that rack is now taken offline. SemiAnalysis believes [Amazon uses 32 1U Graviton 3 servers in a single rack](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and). Each of these 32 servers contains 3 CPUs with 64 cores each. Each server shares a single NIC, which hooks into the TOR switch. This single point of failure at the TOR means that any failure brings down as many as 6,144 customers using m7g.medium or c7g.medium instances.

There is some innovation happening to solve this problem. Dual ToR, Y cables, and X cables are all being developed to enable redundancy options for the NIC, TOR, or both.

![](https://substack-post-media.s3.amazonaws.com/public/images/4e9afdde-84fb-45c8-ac51-418a111b3510_3352x1186.png)

Now that we have the technology covered let’s talk about the specific uses of AEC in off-the-shelf AI hardware, custom AI hardware, and general purpose compute at 8x25G, 4x50G, and 4x100G by Amazon, Microsoft, and Google. We can also discuss the sourcing strategy. Furthermore, we will discuss NIC/Switch choices at these three firms. Lastly, we will also discuss the AEC product timing and SerDes IP licensing from Marvell, Astera Labs, and Alphawave. We can also share AEC and Optical ASPs for 4x25G, 4x50G, and 4x100G.

Credo was the first to market with AEC, and their primary customer is Microsoft at 4x50G within AI applications, including the aforementioned Nvidia HGX A100 example. This includes the [ND A100 v4-series instances](https://learn.microsoft.com/en-us/azure/virtual-machines/nda100-v4-series), which are the workhorse for most training workloads. InfiniBand switches supposedly had lower reliability at the time, which is what the Microsoft Credo example pointed out. This was the main driver for Credo’s dual TOR technology.

 In this case, Microsoft chose AEC strictly for this reliability advantage in InfiniBand deployments. The benefits of AEC cable run distances were irrelevant as Microsoft could also implement DAC instead of AEC at <3m runs without a perceivable increase in error rates. Similarly, AEC has no cost advantage over optical at hyperscale volumes of 4x50G, with both having similar ASPs. The dual TOR AEC has a higher ASP than standard 1 to 1 optics. Add on the 2nd switch, and this is very costly on an infrastructure basis.

Edit:  is down nearly 50% today from $19.36 to $10.30 related to the events we describe here and in the rest of the report. Microsoft only implemented AEC at low volumes. As InfiniBand switch reliability has come up, they phased this technology out. Microsoft has moved back to the cheaper options of DAC and multi-mode optics in this AI application.

[Share](https://newsletter.semianalysis.com/p/thick-cables-thin-margins-microsoft?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Oddly, Credo is only alerting investors now as the sell side happily went crazy with their speculation on business. Some sell-side and buy-side even said Credo would sell 500,000 AEC this year at a $200 ASP to Microsoft alone. That’s not happening. Instead,

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

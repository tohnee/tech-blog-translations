---
title: "Microsoft Infrastructure - AI & CPU Custom Silicon Maia 100, Athena, Cobalt 100"
subtitle: "Specifications, Volumes, GPT-4 performance, Next Generation Timing / Name, Backend Design Partner"
date: 2023-11-15
source: https://newsletter.semianalysis.com/p/microsoft-infrastructure-ai-and-cpu
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
---

# Microsoft Infrastructure - AI & CPU Custom Silicon Maia 100, Athena, Cobalt 100

**Specifications, Volumes, GPT-4 performance, Next Generation Timing / Name, Backend Design Partner**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Microsoft is currently conducting the largest infrastructure buildout that humanity has ever seen. While that may seem like hyperbole, look at the annual spend of [mega projects](https://en.wikipedia.org/wiki/List_of_megaprojects) such as [nationwide rail networks](https://en.wikipedia.org/wiki/List_of_megaprojects#Roads_and_transport_infrastructure), [dams](https://en.wikipedia.org/wiki/List_of_megaprojects#Water-related), or even [space programs such as the Apollo moon landings](https://en.wikipedia.org/wiki/List_of_megaprojects#Spacecraft), and they all pale in comparison to the >$50 billion annual spend on datacenters Microsoft has penned in for 2024 and beyond. This infrastructure buildout is aimed squarely at **accelerating the path to AGI** and bringing the intelligence of generative AI to every facet of life from [productivity applications](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure) to [leisure](https://www.semianalysis.com/p/ai-doomer-vs-techno-optimist-social).

While the majority of the AI infrastructure is going to based on Nvidia’s GPUs in the medium term, there is significant effort to diversify to both other silicon vendors and internally developed silicon. We detailed Microsoft’s ambitious plans with [AMD MI300 in January](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch) and more recently [the MI300X order volumes for next year](https://www.semianalysis.com/p/amd-mi300-ramp-gpt-4-performance). Outside of accelerators there are also significant requirements for 800G PAM4 optics, coherent optics, cabling, cooling, CPUs, storage, DRAM, and various other server components.

Today we want to dive into Microsoft’s internal silicon efforts. There are 2 major silicon announcements for today’s Azure Ignite event, the **Cobalt 100 CPUs** and the **Maia 100 AI accelerators (also known as Athena or M100)**. Microsoft’s systems level approach is very notable, and so we will also go into rack level design for Maia 100, networking (Azure Boost & Hollow Core Fiber) and security. We will dive into Maia 100 volumes, competitiveness with [AMD MI300X](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance), [Nvidia H100/H200/B100](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition), [Google’s TPUv5](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion), [Amazon’s Trainium/Inferentia2](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will), and Microsoft’s long-term plans with AI silicon including the next generation chip. We will also share what we hear about GPT-3.5 and GPT-4 model performance for Maia 100.

It should be noted that while Microsoft is currently behind on deploying custom silicon in their datacenters relative to Google and Amazon, they have a long history of silicon projects. For example, did you know that Microsoft developed their own custom CPU called E2 with a custom instruction set that utilized EDGE (Explicit Data Graph Execution). [They even ported Windows specifically for this ISA](https://www.theregister.com/2018/06/18/microsoft_e2_edge_windows_10/)! Microsoft has historically worked with AMD on semi-custom gaming console chips, but they are also now extending partnerships to custom Arm based Windows PC chips. Microsoft has also internally developed [multiple generations of root of trusts](https://www.semianalysis.com/p/caliptra-first-open-source-silicon) that are found on every single server they install in their datacenters.

Microsoft [Project Catapult](https://www.microsoft.com/en-us/research/project/project-catapult/) for a long time which targets search, AI, and networking. Initially Project Catapult was based entirely on standard FPGAs, but Microsoft eventually engaged with Intel for a custom FPGAs. The purpose of this FPGA was primarily for Bing, but it had to be scrapped due to Intel’s execution issues. Bing still relies heavily on FPGAs, in contrast to Google search which is primarily accelerated by [TPUs](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion).

As part of the announcements today, Microsoft is also announcing the Azure Boost network adaptor, which is a 200G DPU based on an external FPGA and an internally designed ASIC. This product offloads many hypervisor, host, network, and storage related tasks, but for some reason Azure instances with Azure boost still have to give up host CPU cores for infrastructure related tasks. This differs from [Amazon’s Nitro which frees up all host CPU cores for VMs](https://www.semianalysis.com/i/108660819/amazon-nitro).

## **Azure Cobalt 100 CPU**

The Azure Cobalt 100 CPU is Microsoft’s 2nd Arm based CPU that they have deployed in their cloud. It is already being used for internal Microsoft products such as Azure SQL servers and Microsoft Teams. The first Arm based CPU Microsoft deployed was a [Neoverse N1 based CPU purchased from Ampere Computing](https://www.semianalysis.com/p/sound-the-siryn-ampereone-192-core). The Cobalt 100 CPU evolves from that and brings 128 Neoverse N2 cores on Armv9 and 12 channels of DDR5. Neoverse N2 brings 40% higher performance versus Neoverse N1.

Cobalt 100 is primarily based on Arm’s Neoverse Genesis CSS (Compute Subsystem) Platform. This offering by Arm diverges from their classic business model of only licensing IP and makes it significantly faster, easier, and lower cost to develop a good Arm based CPU.

Arm provides verified and laid out blobs that have many aspects of the design process completed for vendors. We detailed this new business model more [here](https://www.semianalysis.com/p/arm-and-a-leg-arms-quest-to-extract).

In the case of Cobalt 100, Microsoft is taking 2 Genesis compute subsystems and tying them together into 1 CPU.

This is similar to [Alibaba’s Yitan 710 CPU](https://www.servethehome.com/arm-based-alibaba-cloud-t-head-yitian-710-crushes-specrate2017_int_base/), which is also based on Neoverse N2. [Chips and Cheese profiled that here.](https://chipsandcheese.com/2023/08/18/arms-neoverse-n2-cortex-a710-for-servers/)

![](https://substack-post-media.s3.amazonaws.com/public/images/792cef96-8110-4fc2-9777-ef1ffc6b99dc_2196x1216.png)

Arm has previously bragged that it only took 13 months from the kick-off of a project to having working silicon for a hyperscaler. Given Alibaba and Microsoft are the only customers for Genesis CSS that we know of, and Alibaba was the first to market, it is likely that Arm is talking about Microsoft on the slide below. There is also a possibility that Google’s Arm based CPU is using Genesis CSS as well.

## **Azure Maia 100 (Athena)**

Microsoft’s long awaited AI accelerator is finally here. They are the last of the big 4 US hyperscalers (Amazon, Google, Meta, Microsoft) to unveil their product. With that said, Maia 100 isn’t a slouch. We will compare its performance / TCO versus [AMD MI300X](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance), [Nvidia H100/H200/B100](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition), [Google’s TPUv5](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion), [Amazon’s Trainium/Inferentia2](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will).

The bulk of this piece is below. It will include the full specifications, network setup and topology, rack design, volume ramp, performance, power consumption, design partners, and more. There are some very unique aspects of this chip that we think ML researchers, infrastructure folks, silicon design teams, and investors should be made aware of.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

---
title: "Astera Labs Is First To CXL Memory Pooling Silicon – Beating Marvell, Rambus, Microchip, and Montage Technologies"
subtitle: "Astera Labs Leo has a feature and time-to-market advantage."
date: 2022-08-30
source: https://newsletter.semianalysis.com/p/astera-labs-is-first-to-cxl-memory
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Astera Labs Is First To CXL Memory Pooling Silicon – Beating Marvell, Rambus, Microchip, and Montage Technologies

**Astera Labs Leo has a feature and time-to-market advantage.**

CXL will revolutionize the datacenter by bringing [composable server architecture](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable) and [heterogenous compute](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable). We recently did a [deep dive on the CXL standard, exploring products, timing, and strategy from 20 firms](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable) on CXL, including switches, NICs, DPUs, IPUs, co-packaged optics, memory expanders, memory poolers, memory sharers, CPUs, GPUs, and accelerators. Over the next few years, the most important category of these products will be those related to memory because [50% of server costs are from DRAM alone](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut).

> [1st generation memory] disaggregation can achieve a 9 – 10% reduction in overall DRAM, which represents hundreds of millions of dollars in cost savings for a large cloud provider.
>
> > [Microsoft](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)

The primary provider of memory disaggregation hardware will benefit hugely as the large cloud providers rush to implement memory pooling within their datacenters to increase memory utilization and reduce costs. SemiAnalysis believes the CXL-based memory expansion and memory pooling hardware market will exceed 1 billion dollars in 2025. The industry recognizes this, so it is an incredibly crowded field. Samsung, Micron, and SK Hynix are all developing memory expansion hardware. Furthermore, Rambus, Microchip, Montage Technologies, Marvell, and Astera Labs are all developing memory expansion and pooling ASICs.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8ffdd69e-7873-410c-9775-fc1c0eb65ae0_1501x852.png)

With all these players, there will be a couple of winners and many losers. [In our prior report explaining why Marvell purchased Tanzanite Silicon](https://semianalysis.substack.com/p/marvell-acquires-tanzanite-silicon?s=w), we also reviewed the hardware status from Astera Labs.

> Astera Labs is coming to market sooner [with CXL based memory pooling]. Their success, so far, is as the only high-volume smart retimer for PCIe 5.0/CXL. We believe they have taped out their CXL memory accelerator, codenamed Leo. Astera Labs should be able to ship it early next year. We believe they will have the highest volume CXL memory accelerator for 2023.
>
> > [Marvell Acquires Tanzanite Silicon To Enable Composable Server Architectures Using CXL Based Memory Expansion And Pooling](https://semianalysis.substack.com/p/marvell-acquires-tanzanite-silicon?s=w)

We stand by what we wrote in our prior report and want to expand further with today’s official announcement about the Leo memory connectivity platform.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/832a922f-782f-4817-a39e-e69b8efa39b3_1521x852.png)

Astera Labs is announcing they have sampled their Leo expansion and pooling chips to various customers. Compare this to other firms that are just beginning to bring up their memory pooling devices or are still working on FPGA-based implementations. Astera Labs says they are on their 3rd generation of their CXL controller while others are still working on the 1st.

Astera Labs had a test CXL chip in 2019. They shipped smart retimers in volume last year. The memory expander and pooling device, Leo, is the 3rd generation. Astera Labs generated ~$35M in revenue in 2021 and is expected to have over $100M in 2022. Astera Labs will likely rack up multiple design wins with Leo, which should keep them growing at this fantastic pace.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/58cea2b4-193f-4f04-b4a5-c12203548c7c_1518x847.png)

Astera Labs says they have conducted end-to-end interoperability testing with industry-leading CPU/GPU platforms and DRAM memory modules over various real-world workloads with Leo. We believe these platforms are AMD’s Genoa/Bergamo and Intel’s Sapphire Rapids. Leo chips support ECC and server-grade customizable reliability, availability, and serviceability (RAS) capabilities. Astera Labs is rightfully focused on latency for their Leo smart memory controllers as the [performance impact from additional latency can be very high](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut).

The most crucial feature of Leo is that it can do memory pooling on CXL 1.1 platforms. Marvell’s Tanzanite Silicon solution also supports memory pooling on CXL 1.1.

> There are some drawbacks [with the Marvell solution]. The host would need to restart every time the memory pool size was changed, which would be untenable in a cloud VM setting but is fine in high-performance computing environments
>
> > [CXL Deep Dive – Future of Composable Server Architecture and Heterogeneous Compute, Products From 20 Firms, Overview of 3.0 Standard](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)

Astera Labs Leo can dynamically resize the pools without restarting the host CPU. This makes memory pooling possible in the most important market, multi-tenant clouds. Astera Labs’ solution is uniquely positioned and advantaged at this support level.

Software is also important, and Astera Labs is focusing heavily on this. They have developed extensive telemetry features and software APIs for fleet management to make it easy to manage, debug and deploy at scale on cloud-based platforms. This can be done with stock Linux drivers.

Leo supports 2TB of memory. It can utilize DDR4 or up to DDR5 5600MT/s per memory channel, which is required to max out the bandwidth of CXL 1.1 and CXL 2.0. In addition to supporting the JEDEC standard DDR interface, Leo also supports “other memory vendor-specific interfaces.” We are unsure what the memory vendor-specific interfaces would be, but [there likely is a new form factor for DRAM packages being developed.](https://www.businesswire.com/news/home/20220824005210/en/CXL%E2%84%A2-Consortium-and-JEDEC%C2%AE-Sign-MOU-Agreement-to-Advance-DRAM-and-Persistent-Memory-Technology)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/97a28e1a-1bf7-406b-a57b-722bc63e67f6_1512x848.png)

Astera Leo comes in two product lines, E and P series. E is only for expansion, while P is for pooling and sharing. Looking at the SKUs, E-Series CM5082E comes with x8 PCIe lanes, while CM5162P and CM5162E come with x16 PCIe lanes. We believe there are two different chips: an 8-lane memory expander and a 16-lane memory expander/pooler.

The 16-lane platform seems more attractive because multiple CPUs can be connected to enable memory pooling. It is also advantageous for memory expansion with Intel’s Sapphire Rapids. This is because Intel has an issue with CXL lane bifurcation on Sapphire Rapids, meaning an 8-lane CXL device would still consume the entire 16-lane CXL port. This issue will be solved with Emerald Rapids.

In general, AMD’s Genoa and Bergamo will be the systems of choice for memory pooling. This is because they support CXL bifurcation and have some memory pooling features from CXL 2.0 despite the official support level being CXL 1.1. In memory expansion mode, the 8-lane chip is advantageous because it provides slightly lower latency due to a more simplified expander-only data path.

> CXL is designed to be an open standard interface to support composable memory infrastructure that can expand and share memory resources to bring greater efficiency to modern data centers. We’re excited to work closely with Astera Labs on the development of their Leo Memory Connectivity Platform to deliver interoperability and robust validation with AMD processors and **accelerators**.
>
> > Raghu Nambiar, AMD Corporate Vice President, Data Center Ecosystems and Solutions

Part of the announcement included this quote from AMD. The inclusion of the word accelerator is fascinating because it indicates that FPGAs or [MI300](https://semianalysis.substack.com/p/amd-to-infinity-and-beyond) could also support Leo’s memory pooling.

Astera Labs Leo has a feature and time-to-market advantage over the competing memory expander and pooling ASICs from Rambus, Microchip, Montage Technologies, and Marvell. Astera Labs is also well positioned against SK Hynix, Micron, and Samsung in the memory expander market due to the business model of selling merchant silicon. Large hyperscalers prefer to purchase merchant ASICs and integrate them with commodity DRAM rather than the higher-cost expanders that come directly from the memory firms. Our estimates place the DRAM expander and pooling market as larger than 1 billion dollars in 2025, and Astera Labs is well positioned to be the leader in the merchant ASIC sub-segment.

If you like what you’re reading, share it! Spread the word!

[Share](https://newsletter.semianalysis.com/p/astera-labs-is-first-to-cxl-memory?utm_source=substack&utm_medium=email&utm_content=share&action=share)

SemiAnalysis is a boutique semiconductor research and consulting firm specializing in the semiconductor supply chain from chemical inputs to fabs to design IP and strategy.

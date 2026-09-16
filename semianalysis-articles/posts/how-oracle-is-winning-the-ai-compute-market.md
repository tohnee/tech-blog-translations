---
title: "How Oracle Is Winning the AI Compute Market"
subtitle: "Stargate, OpenAI, ByteDance, Unique Datacenter Strategy, Investment Grade Neocloud, Revenue and EBIT Forecast"
date: 2025-06-30
source: https://newsletter.semianalysis.com/p/how-oracle-is-winning-the-ai-compute-market
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Daniel Nishball"]
tags: ["Datacenter", "Networking", "Hyperscaler"]
audience: only_paid
paywalled: true
---

# How Oracle Is Winning the AI Compute Market

**Stargate, OpenAI, ByteDance, Unique Datacenter Strategy, Investment Grade Neocloud, Revenue and EBIT Forecast**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Oracle's Cloud Infrastructure business is firing on all cylinders and is greatly outpacing expectations. All eyes are on the [high-profile Stargate JV](https://semianalysis.com/2025/01/23/openai-stargate-joint-venture-demystified/) and the massive Abilene, Texas datacenter, which [our September 2024 Multi-Datacenter Training report](https://semianalysis.com/2024/09/04/multi-datacenter-training-openais/#how-openai-and-microsoft-plan-to-beat-google) called out as a GW-scale training hub for OpenAI. But Oracle has many additional growth engines beyond this massive campus.

![](https://substack-post-media.s3.amazonaws.com/public/images/66edfa5e-5414-4f18-a73a-9f021c7c1cdc_1841x1091.jpeg)
*Source: SemiAnalysis Datacenter Model – June 11th, 2025 picture*

We believe the most underappreciated aspect of Oracle's growth story is its **relationship with ByteDance**. It has triggered the rise of **Johor, Malaysia as the world's second largest AI hub**, and we expect the partnership to develop across many other countries, with [expansion already well underway](https://www.semianalysis.com/p/datacenter-model).

![](https://substack-post-media.s3.amazonaws.com/public/images/9ab9d829-2b40-4bf6-b8c7-652550fe814c_1327x1123.png)
*Source: SemiAnalysis Datacenter Model*

With both flagship customers among the world's largest and fastest-growing GPU renter and significant additional pipeline ahead, we forecasted a **stellar CapEx ramp back in February 2025**. The announcements made two weeks ago by Larry Ellison, forecasting >$130B of contracts to be booked in the next twelve months, confirm our expectations. And our [new month-by-month GB200/300 rack orders and shipments tracker](https://semianalysis.com/accelerator-industry-model/) confirms extreme demand from Oracle. This is not only driven by the largest customers, but also a large number of smaller firms going to Oracle for their technical expertise. Oracle recently earned a Gold [ClusterMAX rating](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/) based on independent testing of software, networking, security, lifecycle, storage, etc.

![](https://substack-post-media.s3.amazonaws.com/public/images/3e2d0d12-9d5d-4ea1-8c8d-d29e646ca8d2_1791x453.png)
*Source: SemiAnalysis Core Research , Hyperscaler CapEx Annual Estimates for AI Servers, DC Infrastructure, and Total CapEx - February 13 th , 2025*

In today's report, we dive deeper into Oracle's infrastructure strategy. Larry made some bold bets that were key to its emergence as an AI computing powerhouse. By combining **attributes of a "traditional" US hyperscaler, an AI-native Neocloud, and selectively working with lightning-fast Chinese datacenter developers**, Oracle found a winning recipe. This reports sheds light on Oracle's key datacenter projects around the globe, unpacks its unique strategy, and highlights areas with significant potential for expansion.

In addition, Oracle also has singular cost advantages, the most notable of which is networking. We use our newly-launched [AI Networking Model](https://semianalysis.com/ai-networking-model/) to provide a detailed TCO comparison of Oracle relative to Neocloud Giants. The Model details the precise networking configurations of each hyperscaler, for each type of GPU, and forecasts units and revenue by supplier.

However, many questions remain about Oracle's financial returns, the ability to upsell higher margin services, and the overall sustainability of the GPU business amid increasing competition. We lay out our revenue and EBIT forecast at the end of the report, based on our [AI Cloud TCO Model](https://semianalysis.com/ai-cloud-tco-model/), trusted by leading AI labs, hyperscalers, the largest GPU-as-a-Service vendors, and their financial partners. The result will likely surprise many investors and stakeholders.

Before diving in, let’s review some history to understand how Oracle got to where it is.

## Oracle Cloud before GenAI

### Some background on OCI

Oracle was, for a long time, a software pure-play, and joined the Cloud Computing race years after rivals Azure, AWS and GCP. Prior to GenAI, Oracle was best known for its strong position in Enterprise software. Larry Ellison’s empire was built on its big bet on relational databases, and it remains today a significant portion of revenue. Oracle is also world #2 in ERP (Enterprise Resource Planning) software behind German firm SAP. ERP is a core enterprise application keeping track of finances, supply chain, inventory, HR, and more.

To understand Larry Ellison's vision and how Oracle got to where it is today, the comparison between long-time rivals SAP and Oracle is insightful. Larry was a vocal cloud skeptic in the 2000s and was primarily focused on taking share from SAP’s business application empire. Looking to leverage its database and middleware dominance, Oracle engaged in a fury of acquisitions in the 2000s to broaden its portfolio and vertically integrate, illustrated by a $10.3B takeover of PeopleSoft in 2004 (software), and $7.4B buyout of Sun Microsystems in 2009 (hardware + software).

As Cloud Computing began to accelerate in the early 2010s, AWS and Azure posed an increasing threat to Oracle's database moat, pushing it to take a U-turn and launch a Cloud-based database and ERP. Larry also saw another opportunity to take share from SAP by upselling ERP to customers moving their data to the cloud. The German firm responded aggressively, with the launch of Cloud-based S4 HANA ERP in 2015, abandoning support for 3rd party databases and forcing adoption of its own newly launched database, HANA.

To support their Cloud transition, the two software giants began building their own compute infrastructure, and CapEx surged in the mid-2010s.

![](https://substack-post-media.s3.amazonaws.com/public/images/165bb709-7944-4ac5-8ce4-8880f5ec4fcf_1330x803.png)
*Source: SAP, Oracle*

This is when their paths begin to diverge substantially. In order to properly serve Enterprise customers around the globe, a large-scale infrastructure build-out was required. To avoid a collapse in margins, SAP had to monetize through an Infrastructure-as-a-Service (IaaS) business, but gave up after a few years, refusing to compete directly with AWS, Azure and GCP and partnering with them instead.

Oracle took the opposite journey. It launched Oracle Cloud Infrastructure (OCI) Gen2 Cloud in 2016, marking a drastic **shift from an infrastructure built to support Oracle’s software, into a full end-to-end Cloud offering.** The stated goal was to compete with AWS and Azure, fulfilling Larry Ellison’s vision of vertical integration.

Importantly, OCI also invested significant resources in Cloud High-Performance-Computing (HPC), with important consequences today. Through the acquisition of Sun Microsystems in 2009, it acquired HPC and networking expertise and built the high-performance storage system Exadata, and developed high-speed RDMA over Converged Ethernet (RoCE v2) to connect multiple nodes. While Oracle ended selling a lot of Sun's HPC assets, the networking capabilities remained and were key to Oracle's launch of Cloud HPC in 2017-18, using RoCEv2 networking through Mellanox ConnectX systems. Oracle also began deploying Nvidia GPUs and expanded the partnership in 2020, being among the first to deploy the A100.

![](https://substack-post-media.s3.amazonaws.com/public/images/4bec09f6-a492-4be4-8e49-edf6d02ea7ab_1920x1080.png)
*Source: Infolob Global*

### Infrastructure strategy before GenAI

Looking deeper at Oracle’s datacenter strategy before GenAI, it resembles more that of a large enterprise than an AWS or Azure. We examine below Oracle’s relationship with Digital Realty, a key datacenter partner, from 2019 to today. While total capacity has grown ~3x in five years, the changing nature of contracts is much more telling.

Oracle’s contracts with Digital Realty historically had a weighted average **lease term of 2-3 years until mid-2022, much lower than Microsoft’s 8-9 years**. Due to its much lower scale, Oracle didn't have the need to contract large-scale capacity in the tens of megawatts, which typically requires a much longer contractual commitment. While OCI did grow to a multibillion dollar business by 2022, it remained an order of magnitude smaller than Azure and AWS. It was gaining share, but from a low base, and more by benefitting from its customer's Cloud transition than by winning new customers and/or moving them off AWS and Azure.

![](https://substack-post-media.s3.amazonaws.com/public/images/f24f6101-e240-435c-ad43-4f58eefeaed1_1322x821.png)
*Source: Digital Realty, SemiAnalysis Datacenter Model*

### Oracle’s 2024 transformation

As ChatGPT's rise and Nvidia's ramp shifted the datacenter market to a capacity-constrained environment, datacenter developers demanded 10 year+ contracts to deliver large-scale capacity. With hyperscaler demand so strong, capacity below 10MW allocated to Enterprises was scarce.

Oracle had to choose. Without the same scale as rival hyperscalers, committing to hundreds of megawatts of capacity with 15-year terms introduces a **material risk of stranded expense**. There is not only the **risk of overcommitting relative to revenue growth, but also a locational risk**: what if your new datacenter is in Portland, but most of your customer demand comes from Dallas?

Larry Ellison was willing to take that risk, and committed to >2GW of capacity from November 2023 to January 2025. Oracle was the **single largest lessor of datacenter capacity in the US over that period**. To put this in perspective,2GW of leased datacenter capacity **corresponds to approximately a $3B annual expense... higher than OCI's revenue in fiscal year 22.** Contract length also surged, with 10+ year deals becoming the norm, as evidenced by the above Digital Realty chart.

And the growth of its backlog shown below demonstrates that it was immediately able to sell GPU clusters to customers.

![](https://substack-post-media.s3.amazonaws.com/public/images/40a10f93-d861-444c-96a7-9cb1d2f92041_1323x859.png)
*Source: Oracle, SemiAnalysis Datacenter Model*

## Oracle’s winning “hybrid” datacenter strategy

### Self-build, leasing, Oracle's disadvantage

We think a key to Oracle’s success was its ability to leverage a hybrid infrastructure strategy, somewhere between a Neocloud and a Hyperscaler – we could call it the “Investment Grade Neocloud”.

As of today, Oracle doesn’t have datacenter self-build capabilities, a disadvantage relative to other hyperscalers who can combine self-development and leasing, and often use the former for large compute clusters. The datacenter market has typically been structured this way:

- Hyperscaler self-builds host large compute clusters and are often in very remote areas, such as Google in Council Bluffs, Iowa or Meta in Prineville, Oregon and Los Lunas, New Mexico. Hyperscalers fund the fiber infrastructure and find areas with ample potential to expand and cheap power.
- Datacenter developers (like Digital Realty) typically build around metros, with ample connectivity and close to their end customers – for example, Ashburn (near Washington DC), Silicon Valley, or Dallas, often referred to as "Tier 1 Markets". This is because the leasing market historically was largely a real estate game, and returns were better in high-demand markets where the asset is likely to be valuable for many decades.

Note that being close to end customers is a great fit with the “Cloud mindset”, making assets located in Tier 1 markets very attractive to Azure, AWS, GCP and OCI Cloud Availability Zones (AZs). This perfectly matches Satya Nadella’s favorite word, **fungibility**.

### From Tier 1 markets to Abilene, Texas

As the AI race kicked off, hyperscalers accelerated self-build and began construction of several gigawatt-scale datacenters towards the end of 2023. Oracle initially responded by growing with its traditional colocation partners, such as Digital Realty and QTS around big metros. We show below one of their AI campuses in a Tier 1 market.

![](https://substack-post-media.s3.amazonaws.com/public/images/2041953a-0e89-4da0-b858-f70d9a85a646_1192x745.png)
*Source: SemiAnalysis Datacenter Model – June 23rd , 2025 picture*

It also took capacity in less established markets, such as the Salt Lake City area. But with Tier 1 markets being overly crowded, and many Tier 2 locations struggling to keep up with power demand, it was hard to get anything close to a gigawatt-scale datacenter to secure the largest AI contracts. [The rare suitable sites were all pre-leased by Microsoft in 2023 and early 2024](https://www.semianalysis.com/p/datacenter-model).

![](https://substack-post-media.s3.amazonaws.com/public/images/7f4f2ba9-136c-457d-840d-537563e80c33_859x1063.png)
*Source: SemiAnalysis Datacenter Model – June 3 rd , 2025 picture*

This led to the emergence of a new market segment: the AI-first developers. New entrants, often from the cryptomining world, understood that power was becoming the #1 concern and leveraged their existing interconnection agreements to plan large datacenters, away from population centers but with ample power. Core Scientific’s 570MW deal with Coreweave is a great example. However, due to a lack of credentials and the self-build alternative, “AI-first” developers largely struggled to secure hyperscaler customers. Their target market remained the Neocloud segment, but with many players having a low credit rating and unable to sign a 10+ year contract, securing funding was challenging:

- Neocloud GPU contracts are often 2-3 years, with 5 years being the upper end.
- The payback period of a datacenter developer is generally 7-9 years.

Oracle saw this gap as an opportunity to participate in the market for huge AI contracts, identified a Gigawatt-scale site in Abilene, Texas, and signed a 15-year datacenter deal with Crusoe – which at that time was, on paper, a cryptominer unexperienced with datacenters. While Crusoe had talent worth believing in, the company had not actually executed on a project of this scale. The first contract signed mid-2024 covered ~220MW of IT capacity (on our estimate), and a ~660MW expansion was signed in early 2025, taking total contract value to about $15-20B.

Said differently: Oracle committed to **paying over a billion dollars per year, for fifteen years, to an unexperienced developer.** It is hard to understate how bold the bet was! Even with OpenAI committed to buying all the compute capacity from that campus, these five-year contracts sum up to close to $10B annual expense for OpenAI, a startup that was generating around 2 billion dollars of annualized revenue mid-2024, and highly unprofitable. There were **both credit risks and duration risks** associated with Oracle's bet.

![](https://substack-post-media.s3.amazonaws.com/public/images/bef2a188-85d1-4530-a294-9b1ce4b61dc4_1841x1091.png)
*Source: SemiAnalysis Datacenter Model – June 11th, 2025 picture*

Of course, Oracle’s bold move was key to making it a part of [Stargate, the high-profile JV claiming to invest $500B on GenAI](https://semianalysis.com/2025/01/23/openai-stargate-joint-venture-demystified/). Given our views on [Scaling Laws](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/) and overall AI industry growth, we think it was a genius play, and Oracle will benefit from a long-lasting relationship with an emerging industry giant.

### How large is the Stargate upside?

Questions remain on how much exacly Oracle will benefit. With Larry Ellison publicly saying that no Stargate contracts have been signed yet, many investors are tempted to think that the first $100B investment tranche hasn’t been booked, and another $400B are coming – and that’s without including international Stargates.

But we don’t think that is reality. As far as we know, Stargate (the JV) doesn’t really exist, and hasn’t done anything meaningful – so Larry is factually correct. On the other hand, the ~880MW OpenAI deal located in the Crusoe/Lancium campus in Abilene, Texas (often called Stargate) is very real… and already in Oracle’s books. We believe that Phase 2 was booked in January 2025, and it shows on both Oracle’s leasing activity, and RPO growth in that specific quarter. The first phase was booked two quarters before.

![](https://substack-post-media.s3.amazonaws.com/public/images/a368b280-01f3-4a93-85c6-6f2449fcafa3_886x859.png)
*Source: Oracle, SemiAnalysis Datacenter Model*

The other “Stargate” deal widely discussed [is happening in the Middle East](https://semianalysis.com/2025/05/16/ai-arrives-in-the-middle-east-us-strikes-a-deal-with-uae-and-ksa/). However, as far as we know, this will not meaningfully flow to Oracle’s financials, as the [GPU cluster will be set up by G42/Core42.](https://semianalysis.com/accelerator-industry-model/)

So, should we expect any upside from Stargate?

- From OpenAI and potential new GW-scale deals: yes. Larry’s targeted >100% RPO growth in FY26 and our forecasted >$30B CapEx doesn’t work without the contribution of OpenAI.
- From Stargate, the JV: not much. A Stargate contract would replace demand from OpenAI, it wouldn’t be net incremental. New stargates outside of the initial 1.2GW of Abeline Texas would be incremental. We have posted about these on [Core Research.](https://semianalysis.com/core-research/)
- From international Stargates: it could actually be more negative than positive, depending on how much Oracle is involved. Sovereigns looking to host OpenAI could be tempted to bypass Oracle and deal directly with Sam's firm.

Calling Stargate incremental to OpenAI contracts suggests that these deals wouldn't happen otherwise, but we don't think that's accurate. Revenue growth is running significantly ahead of target, and its previous infrastructure plan has been sharply revised up. Oracle is looking for capacity all around the globe to serve its key customer, and we expect them to deliver – thanks again to their datacenter strategy. [But others are set to take a piece of the pie](https://semianalysis.com/core-research/).

### The APAC ramp and Bytedance relationship

While Abilene and the OpenAI deal are catching all the headlines, the scale of the Oracle and Bytedance partnership remains under the radar. We believe that **TikTok’s parent is one of the world’s largest and fastest-growing users of GPUs**, of comparable scale to US hyperscalers, and is Oracle’s largest GPU customer today. We think they have a few sizeable deals in the US, notably in Northern Virginia, but more impressive is their ASEAN growth which led to the emergence of the World’s second largest AI datacenter hub: the Singapore-Johor-Batam hub, shown below. It is widely believed that most of Oracle’s ASEAN GPU capacity is allocated to Bytedance.

![](https://substack-post-media.s3.amazonaws.com/public/images/c4e52755-01b8-4948-b6a4-635e5a36fb0f_1327x1122.png)
*Source: SemiAnalysis Datacenter Model*

We show below what we believe to be their largest “co-cluster”, set to reach 600-700MW within a year, and potentially up to 2GW by 2028.

![](https://substack-post-media.s3.amazonaws.com/public/images/5bde452f-2d08-4f6a-b83b-4b26a42d825a_1389x1117.png)
*Source: SemiAnalysis Datacenter Model*

One of Oracle's key APAC datacenter partners is GDS International. Rebranded DayOne in January, its largest customer (by committed power) is, by far, Bytedance. Oracle ranks second, and is DayOne’s only large western customer, as far as we know ([but there will be a second one soon](https://www.semianalysis.com/p/datacenter-model)). DayOne has demonstrated an expertise in building datacenters from “zero” to full operations in less than 12 months – as shown below with close to 100MW. Note that this isn't unique to DayOne: Chinese Hyperscalers have adopted modular datacenter construction techniques for several years already, and are renowned for their ability to deploy extremely fast.

![](https://substack-post-media.s3.amazonaws.com/public/images/203484e7-2b6e-49d5-827a-b9e079b2ba6e_1999x818.png)
*Source: SemiAnalysis Datacenter Model*

Given aggressive growth plans in ASEAN and Europe, we expect the firm to continue to grow extremely fast, with >1GW of total committed power likely within a year, and half of it operational. Most of it will serve its two key customers.

![](https://substack-post-media.s3.amazonaws.com/public/images/cd06e3ad-c18a-4fed-af4e-54f1bc495242_1324x811.png)
*Source: GDS*

With GDS and other operators, [Bytedance is planning a stellar capacity ramp in ASEAN, Europe, and Latin America](https://www.semianalysis.com/p/datacenter-model). And everytime Bytedance deploys in a new area, we see it contracting capacity with local GPU Cloud providers. As such, we expect the industry to substantially benefit from that ramp, and Oracle to take a material share. Our [Datacenter Industry Model](https://www.semianalysis.com/p/datacenter-model) tracks and forecasts site-by-site deployments and aggregate MW capacity of the largest hyperscalers and Neoclouds.

## Oracle’s networking architecture and cost advantages

Let’s now discuss some of Oracle’s cost advantages, focusing primarily on networking. Competitors for large-scale GPU contracts are two types of firms:

- Hyperscalers: Oracle often wins by being faster and cheaper. They could easily match Oracle’s pricing, and have done it on many occasions, but are generally interested in higher return opportunities. Debt funding also makes Oracle’s cost of capital lower versus hyperscalers.
- Neocloud Giants: while competition is heating up, Oracle has a few key cost advantages, making it hard for rivals to match pricing while generating attractive returns.

We think Oracle’s cost advantages are threefold:

1. Networking – we explain below Oracle’s GPU cluster TCO optimization relative to competitors.
2. ODM vs OEM – by working directly with Foxconn, Oracle bypasses the extra margin of Dell and Supermicro.
3. Cost of capital – Oracle’s GPU cloud business likely has the market’s lowest cost of capital, through its Investment Grade status but openness to debt funding. This compares to double-digit cost of debt for most Neoclouds, and equity-funded GPUs on the hyperscale side.

We show below how Oracle's optimized networking configuration, alongside cheaper server price, enables a 20% CapEx advantage over a Neocloud Giant. Our newly-launched [AI Networking Model](https://semianalysis.com/ai-networking-model/) provides detailed cluster networking configurations as well as line by line costing for items building up this network. Clients can also use this model to build up estimates for the number of switches Arista might sell into operators like Oracle and ultimately Arista’s overall switching opportunity for the next few years.

![](https://substack-post-media.s3.amazonaws.com/public/images/93faa91d-5cc5-47cd-8f2e-e04ce4fc9c00_2150x850.png)
*Source: SemiAnalysis AI Networking Model*

Oracle’s networking capabilities are one of its strong suits and is one of the key reasons why it [earned a ClusterMAX™ Gold rating](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/#oracle-cloud-infrastructure) in our inaugural ratings exercise. From our testing on H100 and H200 clusters, we noticed that OCI’s RoCEv2 networking was very competitive with Spectrum-X Ethernet, delivering very strong NCCL-test performance.

![](https://substack-post-media.s3.amazonaws.com/public/images/2e7bfaf8-ff8e-483c-8023-1e0b98ee499f_1010x1126.png)
*Source: SemiAnalysis ClusterMAX rating*

## Does Oracle have a software & technology moat?

Let’s now turn our attention to Oracle’s financial returns. We’ll start by discussing whether Oracle has a software & technology moat and the ability to upsell Cloud services to GPU cloud customers. We’ll then estimate the margin profile of Oracle's large contracts and derive a revenue and EBIT forecast. Finally, we’ll provide some thoughts on the long-term shape of the industry.

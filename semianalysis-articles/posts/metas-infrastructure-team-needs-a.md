---
title: "Meta’s Infrastructure Team Needs A Culture Reset"
subtitle: "Meta Infrastructure has become bloated, with middle managers expending resources on over-engineered technology solutions that lose sight of broader organizational needs."
date: 2026-07-22
source: https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a
crawled: 2026-09-15
authors: ["Wayne Ma", "Myron Xie", "Julien Martin-Prin", "Daniel Nishball", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Meta’s Infrastructure Team Needs A Culture Reset

**Meta Infrastructure has become bloated, with middle managers expending resources on over-engineered technology solutions that lose sight of broader organizational needs.**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

In our [recent newsletter piece about Meta Superintelligence](https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence), we expressed reasons to be optimistic on Meta AI. MSL now has many of the right ingredients to catch up with Anthropic and OpenAI to return to the frontier. However, we also briefly alluded to cultural issues plaguing Meta’s infrastructure teams. This article will dive into how these cultural issues have manifested into expensive missteps, whether it be with acquisitions like Rivos or strange choices on hardware architecture.

We believe that Meta Infrastructure needs a cultural reset to better serve the Meta AI organization, especially the world class researchers who are at MSL. This is even more important as [Meta embarks on the path of selling its compute to outside customers](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be), not just serving captive internal users.

Meta Infrastructure has become bloated, with middle managers expending resources on over-engineered technology solutions that lose sight of broader organizational needs. The company appears burdened by far too many disparate groups that are over-optimizing for certain metrics as opposed to delivering usable technology for the company as a whole. Middle managers will do everything to justify their proposals to protect their positions within Meta, which has become an extremely political organization.

One big issue is Meta’s six-month performance review cycle, in which the bottom 10% to 15% are cut every review round. The result is an organization of employees that optimize for short-term wins rather than long-term strategies. Some managers push for highly visible projects that can be delivered quickly, a practice known as “window washing” and then promptly pivot or abandon them. Few openly challenge leadership, which leads to bad decisions going uncorrected. The whole system discourages long-term thinking and leads to risk-adverse behavior.

Within Meta Infrastructure, supply chain teams also have little say over engineering teams. The result is technology decisions driven by political motivations rather than thoughtful software/hardware co-design for the broader company.

Frequent pivots are also common. And because Meta has a reputation for throwing money at problems and executing at high speed, these U-turns end up becoming more costly versus other companies that take a more disciplined or conservative approach. Suppliers also lose faith when given design wins are later cancelled. This has lead to less supply chain prioritization on new designs. Some suppliers favor focusing on Amazon or Google designs due to Meta’s frequent reshuffling.

A lot of Meta’s issues come from a lack of financial discipline, with managers creating new projects and headcount to fill out and justify the massive budgets given for initiatives like AI. It’s a repeat of what happened to Meta’s Reality Labs division, where billions of dollars were spent on engineers and R&D until layoffs, partly brought on by the company’s pivot to AI, slashed the team and their related projects starting in 2022 and continuing through this year.

## Rivos Acquisition

First, one of Meta’s most recent missteps has been the more than $2.5 billion it sunk last year into the acquisition of Rivos, a chip startup.

Few inside Meta’s chip division have a full understanding of why the company bought Rivos in the first place, and those who championed the deal internally have since gone quiet. The prevailing theory is that Meta had the money, the custom silicon space was heating up, and it was already licensing Rivos’ IP for a future chip, so leadership figured it might as well own Rivos’ technology outright than let anyone else have it.

With the Rivos acquisition, Meta also gained the ability to bypass partners like Broadcom to manage the manufacturing and testing of their own custom chips, a practice known as customer-owned tooling. However, paying more than $2.5 billion for that privilege doesn’t make much sense either given that a COT team could be built from scratch for maybe $100 million a year or more.

Although Meta wanted only Rivos’ accelerator and GPU team, the startup’s founders insisted on an all-or-nothing deal. Meta bought the entire company and then heavily cut employees in the parts it didn’t want.

![](https://substack-post-media.s3.amazonaws.com/public/images/f0536e95-d3f1-4bcf-82c7-c4763a34f9b8_1376x768.jpeg)
*Source: SemiAnalysis, Rivos*

Some former Meta chip employees say the acquisition was led by Meta’s silicon chief, Yee Jiun Song, who pushed for the deal against the wishes of some of those under him but has since lost interest. The result is an organization that has rejected the transplant, leaving Rivos staff stuck to fend for themselves. Existing Meta chip managers treated the acquisition as a pool of free headcount, grabbing Rivos engineers to build out their own empires and pulling the original startup apart in different directions until little of it remained intact.

The technology reasons behind the deal have evaporated just as quickly. Part of Meta’s original interest was that Rivos had SIMT core IP which was closer to a Nvidia-style GPU architecture in terms of programmability, whereas Meta’s own MTIA is SIMD. Yet after the deal closed, Meta cancelled the chip known as Olympus that was meant to use Rivos’ GPU IP, because the design was too aggressive in terms of system and package architecture as well as the software being far from ready. Instead, Meta is sticking with its existing chip architecture through MTIA 600.

Meta still wants to develop a chip that incorporates Rivos technology, and it has created a new chip project known as Phoebe that is now scheduled to tape out in 2028. But not everyone inside Meta is optimistic about the project, and some believe it could eventually be cancelled as well. We have been updating our subscribers of the [Accelerator Model](https://semianalysis.com/accelerator-hbm-model/) about all the different architectures, floorplans, and volumes of various custom silicon.

Meanwhile, incoming Rivos employees have gotten a crash course in Meta’s internal culture. Unlike more mature hardware organizations like Apple, Meta’s hardware roadmaps can change just as quickly as its software roadmaps, with constant pivots, meaning that something you are working on now could be pointless in six months. Many within Meta’s chip division say there is no clear org structure, no clear decision-making, and no clear ownership of which group does what.

A funny example of the disfunction that is approachable to those not in the weeds, Meta doesn’t give most employees assigned desks; people who have been there over a year still scrounge daily for a workspace, where sometimes the desk has a monitor, sometimes the monitor has the wrong cable, and sometimes there is no monitor at all. Employees have formally applied for an assigned desk and been denied, even though desks sit empty everywhere.

Finally, the Rivos acquisition has created dissatisfaction among the pre-existing Meta silicon team. Many Rivos engineers joined with higher compensation and titles without having the requisite responsibilities to justify such perks, and they were placed under existing Meta silicon employees. This resulted in decreased morale within the pre-existing team and also with incoming Rivos staff, who lack the power to make decisions. Since the beginning of this year, a number of Meta’s silicon engineers have been leaving for startups or other well established companies like Arm and Nvidia.

As we first [reported for clients](https://semianalysis.com/accelerator-hbm-model/), around 30% of the Rivos engineers who joined Meta as part of the acquisition were let go in recent layoffs. Rivos co-founder Mark Hayter has already left. A number of former Rivos people have since departed Meta to join Gerard Williams’s new chip startup, Nuvacore, after their first tranche of RSUs vested in May. We believe that Rivos CEO and co-founder, Puneet Kumar, is also eyeing up an exit in a year or two when his shares in Meta fully vest. There is speculation he could join Rosaic Labs, a new chip startup co-founded by Amarjit Gill, an investor in Rivos and longtime collaborator with Puneet Kumar at SiByte, P.A. Semi, Apple and Agnilux.

## Grand Teton

Now let’s talk about Meta’s AI server designs. Meta’s hardware decisions are largely driven by a TCO analysis comparing a matrix of workloads such as ranking-recommendation and GenAI against what vendors like Nvidia, AMD and their own custom silicon offering provide. Meta CEO Mark Zuckerberg has issued an edict that the systems being designed have to work for the entire business, meaning they have to support not only Gen AI workloads but core ranking and recommendation systems as well.

However, Meta has still opted for several “optimizations” for its GPU servers, all of which are strange choices that are often worse than the standard configurations that other hyperscalers purchase. Part of the issue stems from the company’s server teams being in completely separate organizations than their networking teams, with different goals and opinions. Meta engineers are also motivated by the idea of owning their own network operating system and hardware rather than rely on other companies.

To recap, Meta’s H100 HGX server was called “Teton Grand” a design that has been contributed to OCP. The major difference from the standard HGX server is the addition of a switch tray in addition to the standard GPU and CPU head-node configuration. This switch tray houses four Broadcom PCIe switches, 16 SSDs and eight NICs. The function is to provide extra PCIe lanes so that the Grand Teton can add more SSDs per server.

![](https://substack-post-media.s3.amazonaws.com/public/images/3b4a816f-4910-42af-b31e-b5c15cd97e33_2326x1314.jpeg)
*Source: Meta*

It was during the Hopper generation that Nvidia effectively designed out the need for standalone PCIe switches, by implementing PCIe switching functionality with its ConnectX-7 NIC.

With 80x PCIe lanes available on the Intel Sapphire Rapids host CPU, Meta could have designed a box that connected the 2x 200G front-end NICs with eight lanes each, four lanes for various management and control, and 16 lanes for each of the eight ConnectX-7 NICs. This would leave them 32 lanes to connect to eight E1.S SSDs. So, in the end with Grand Teton Meta was able to squeeze out eight more SSDs per server. This came at the cost of greater server BOM, more power, and more integration complexity.

Why did Meta want all this extra direct attached storage? The Infrastructure team provisioned this with the belief that more storage was needed for checkpointing training runs. However, in production, the storage wasn’t utilized nearly as much as anticipated by the model teams, which is why this design ended up being cancelled. This is one of several examples of lack of hardware and software co-design wasting resources.

Meta’s additional justifications were that the design was easier to service and gave it the flexibility to use non-Nvidia NICs. Its engineers wanted to avoid handing over more business to Nvidia, particularly for networking, given that there already was a strong reliance on Nvidia for GPUs.

But the Broadcom switches couldn’t be serviced anyway, and Meta’s software stack still depended on Nvidia’s version of RoCE, the networking protocol for GPU traffic, so Meta was never realistically going to switch NIC vendors. Ultimately, Meta paid more, had worse TCO, didn't reduce their reliance on Nvidia networking gear, and increased their reliance on Broadcom.

## Ariel

The Grand Teton wasn’t a one off mistake on server design. This continued into the Blackwell generation with Meta’s custom GB200 Catalina rack, also known as “Ariel.” Ariel has one Nvidia B200 GPU paired with one Grace CPU, instead of the standard two B200 GPUs with one Grace CPU in the regular GB200 SKU that everyone else purchased. The implementation of this was simple: Ariel used the standard Bianca compute board used for GB200, with each board having one GPU depopulated.

![](https://substack-post-media.s3.amazonaws.com/public/images/d9d214f0-6592-4441-80fc-0cc81094d3b6_2494x1405.jpeg)
*Source: Meta*

Meta engineers were concerned about the stability of the single rack GB200 NVL72. NVL72 systems are complex, involving things like a copper backplane that is the central hub where all the chips connect to and miles of dense copper cables and thousands of connections between the chips and the backplane. Meta Infrastructure initially bet that an NVL36x2 configuration would be more stable than running NVL72 entirely through the backplane.

Because Ariel is 36 GPUs in the one rack, to get to the 72-chip world size scale up, it had to be in the 36x2 format. Cross-rack ACCs connected the switch trays between the racks. This meant double the number of switches which while also adding an extra hop of latency.

![](https://substack-post-media.s3.amazonaws.com/public/images/304a5108-33ec-4134-a4f2-186e6442ea49_1176x793.png)
*Source: SemiAnalysis*

Meta was the only customer of this Ariel SKU, and the reason for this is Meta’s obsession with a higher CPU-GPU ratio for its recommendation systems (“or RecSys’) that suggest personalized ads and feeds. The rationale is that RecSys use a lot of embedding tables that store representations of users, ads and content — require a lot of CPU-bound processing and the additional LPDDR memory from each Grace can store the embeddings that have small, scattered reads so bandwidth isn’t as important as serving LLMs.

The flipside is that by increasing the CPU ratio and additional NVLink networking content because of the 36x2 configuration the server capex per GPU increases. The result is much higher $/FLOP and $/HBM capacity and bandwidth than the standard GB200. These are key metrics for LLM/gen AI workloads making Ariel was far worse for LLM training and inference. All in all our calculations show that TCO for the Ariel NVL36x2 server was 14% higher than standard GB200 NVL72. As mentioned this additional expense was for more CPU and DRAM content that isn’t being utilized for the LLM teams. This decision cost Meta billions of dollars.

This is not to mention the additional network complexity and reliability challenges that came with the 2-hop scale up with the cross-rack ACCs. These challenges were why a limited number of 36x2 was shipped for some hyperscalers for GB200 only, with the 36x2 configuration being dropped entirely for GB300. Ironically, Meta Infrastructure initially bet that a NVL36x2 configuration would be more stable than NVL72 entirely through the backplane. While the backplane was an initial source of reliability issues, the backplane is now much more mature and won out over the cross-rack cabling. The company underestimated the cross-rack cabline problems with the 36x2 design and overestimated the difficulty of making the backplane work with NVL72. There was no backplane reliability benefit of 36 GPU in 1 rack.

Because we understand that the entirety of Meta’s GB200 fleet was in this Ariel SKU, this “optimization” left Meta’s LLM teams burdened with an inferior system to the standard SKU that Meta’s competitors purchased. This is particularly biting as GB200 was the flagship system for gen AI at the time. Unsurprisingly, there is no more Ariel for Meta’s GB300-type servers and Meta is buying the normal configuration.

## Upcoming AMD MI450X, Gun In Mouth Decision

*3rd August 2026 Edit: We have updated the configuration for the Meta Custom MI450X SKU based on new information*
However, we see this now popping up again with AMD’s MI450X. In AMD’s Q1 2026 earnings call, Lisa Su confirmed that AMD is providing Meta with a custom GPU based on the MI450. We have reported this for many months in the [Accelerator Model](https://semianalysis.com/accelerator-hbm-model/). This [custom Meta MI450X is a cut down version of the full MI450X with half the I/O and only 6 out of the full 8 compute dies/ XCDs](https://semianalysis.com/institutional/hbm-capacity-downgrades-amd-meta-version-and-increasing-2027-amd-estimates-trn4-tpu-whalefish-floorplan/). The HBM4 is also downgraded to 8-Hi HBM vs 12-Hi in the standard SKU.

![](https://substack-post-media.s3.amazonaws.com/public/images/8a0433f0-d207-4f8f-b036-6ba8ff76e6b8_1710x1323.png)
*Source: AMD, SemiAnalysis*

With only one I/O die instead of 2, there are only 72 I/O lanes available instead of 144 with 2 I/O die. With a reduced lane budget, the scale up bandwidth needs to be reduced. We believe it is 36 lanes for scaleup instead of the full 72; this would mean only half the Tomahawk 6 switches will be needed in a rack for Meta’s version. This leaves another 36 lanes for system and scale out: with 16 lanes of UAL 128G to go to the NIC for 1.6T scale out per GPU, as well as 16 lanes of Infinity Fabric for the connection to the host CPU.

As a result of these choices, Meta’s version of MI450X has significantly compromised network capability with only half the scale up bandwidth per chip, leaving it at 900GB/s vs Rubin’s 1,800GB/s. There is also the compute reduction of 25% compared to the regular version. While the reduction in compute is not huge, the cost savings from reducing 2 compute tiles are miniscule in the context of the whole system so one wonders whether this choice is worth it.

This chip configuration is intended for Recsys workloads and was something that Recsys infrastructure teams decided. However, the decision was made before TBD Lab was formed or could have its say. Given the significant network deficiency, TBD will have much greater preference for Vera Rubin. AMD designed MI450X Helios to beat or match Vera Rubin’s specs, but Meat Infra has decided to blunt this and make compute and network a deficiency.

This decision is going to nuke AMD’s volume at Meta because TBD will vastly prefer Rubin if this custom MI450 design is chosen. AMD needs to step in, put on their big boy pants, and work directly with teams at TBD to make sure they get the normal MI450 instead of the gimped Meta custom version which is terrible for GenAI. The normal MI450 will actually be competitive with Nvidia’s Vera Rubin.

This is a public outcry from us for Meta and AMD to not waste the silicon and have better more efficient and cost effective AI infrastructure. If this change is made we think TBD would actually consider using MI450.

So much for Zuckerberg’s edict. Next we will go through Meta’s elaborate and expensive DSF networking architecture and why Meta quickly pivoted away. We will also discuss how this culture can be fixed.

---
title: "How China’s Biren Is Attempting To Evade US Sanctions"
subtitle: "The regulations are like swiss cheese, but these holes will be patched up"
date: 2022-10-24
source: https://newsletter.semianalysis.com/p/how-chinas-biren-is-attempting-to
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# How China’s Biren Is Attempting To Evade US Sanctions

**The regulations are like swiss cheese, but these holes will be patched up**

Biren, China’s artificial intelligence hardware champion, is attempting to evade sanctions. A single source report from Bloomberg falsely stated that TSMC would still [ship chips to Biren due to a “key gap” in the export regulations](https://www.bloomberg.com/news/articles/2022-10-21/one-chinese-chip-startup-shows-key-gap-in-biden-export-curbs). Bloomberg [also reported the opposite using the shotgun reporting method](https://www.bloomberg.com/news/articles/2022-10-22/tsmc-said-to-suspend-work-for-chinese-chip-startup-amid-us-curbs?), again relying on a single source. Rather than debate the media’s reporting, let’s break down the situation and exclusively detail how Biren is attempting to avoid the sanctions.

First some background on Biren. While many other Chinese firms are working on and shipping chips made for high-performance computing and artificial intelligence, Biren has the most advanced architecture and chip in production. After independently discussing Biren with multiple Nvidia employees, they all had positive things to say. One even told us they believe Biren is a bigger threat to Nvidia’s AI training hardware dominance than the competition from [Intel](https://www.semianalysis.com/p/intel-is-throwing-the-kitchen-sink), [AMD](https://www.semianalysis.com/p/amd-to-infinity-and-beyond), [Graphcore](https://www.semianalysis.com/p/graphcore-announces-worlds-first), [SambaNova](https://www.semianalysis.com/p/nvidia-in-the-hot-seat), or [Cerebras](https://www.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes). It’s no surprise to hear that sort of comment when one looks at the amount of funding and how many of their engineers worked at major western firms including a large chunk of former Nvidia Shanghai.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a32f6ee7-cbce-4313-ac25-680d2cccee94_3004x1666.png)

Biren created a multi-chip module design that utilizes the TSMC N7 process node and [TSMC CoWoS-S](https://www.semianalysis.com/p/advanced-packaging-part-2-review) packaging. While there is [no fab in China capable of fabricating](https://www.semianalysis.com/p/chinas-smic-is-shipping-7nm-foundry) this advanced of an AI chip yet, multiple companies in China have achieved 2.5D integration. The die is shipped in two products, one is a 2-die module, BR100, and the other is a 1-die module, BR104. Each individual die maxes out at with specs of 1024 TOPS of INT8, 896GB/s of die-to-die interconnect, 256GB/s of Blink, and 128GB/s of CXL 2.0.

As we explained in [our comprehensive overview of the 2 new US-China regulations](https://semianalysis.substack.com/p/china-and-usa-are-officially-at-economic), this would place the BR100 well over the performance level of the US government dictates.

> That test is for chips with both 600 GB/s IO and [4800 (PERF*Bit length) or 600 TOPS PERF]. Under this definition, Nvidia’s A100, H100, AMD’s MI250X, Biren’s BR100, Graphcore’s BOW, Cerebras’s WSE, and more apply.

This immediately rules out the BR100 which packages 2 of these dies for a total performance and IO level of 2048 TOPS of INT8, 896GB/s of die-to-die interconnect, 512GB/s of BLink, and 128GB/s of CXL 2.0. The specs are at an assumed 1GHz clock for the compute elements, but these clocks can easily change, which highlights a major flaw in the regulation.

The IO speed limitation is met by the BLink and CXL 2.0 alone. The US regulations had a very extensive definition of TOPS, which differs from how Biren defines its TOPS figure.

> The threshold of 4800 bits x TOPS can be met with 600 tera integer operations at 8 bits or 300 tera FLOPS at 16 bits.
>
> US Bureau of Industry and Security

The BR100 is clearly excluded, but the BR104 has half of most of these specs. While that would place it firmly above the TOPS requirement. The full chip would be bandwidth would be 896GB/s of die-to-die interconnect (inactive), 256GB/s of BLink, 128GB/s of CXL 2.0, and 819GB/s of memory bandwidth.

> Integrated circuits that have or are programmable to have an aggregate bidirectional transfer rate over all inputs and outputs of 600 Gbyte/s [GB/s] or more to or from integrated circuits other than volatile memories
>
> US Bureau of Industry and Security

The US government’s definition does not count the memory bandwidth of the product as IO. The interpretation of the regulation does not define if this refers to die/chiplets or completed packages either.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/26680f01-4879-4e57-823c-4a159635c0cd_3542x682.png)

Biren has attempted to evade the sanction by changing the specs of its products. They cut the number of BLink on BR100 from 8 to 7 which would reduce the BLink + CXL 2.0 bandwidth to 576GB/s. Biren believes this gets them under the hurdle of sanctions.

Before the regulations, at the [AI Hardware Summit](https://www.semianalysis.com/p/meta-discusses-ai-hardware-and-co), we spoke to a Biren employee about the topology of their network as well as their 200-generation product’s inclusion of an external switch. Biren planned to use all 8 BLink for intra-node and inter-node capabilities on B100 at the time. Biren has changed their tune after sanctions and updated its site in the hopes of avoiding sanctions by cutting down the product’s specs. The US government would have no way to validate that the 8th BLink was actually disabled.

Regardless, this still ignores that each die has a 896GB/s die-to-die interconnect that connects it at high speed and low latency to another die in the same package. BR104 product does not technically have the die-to-die interconnect active, but this feature is still on the die. There is no guidance in the US government’s documents that indicates whether active vs inactive/binned/cut-down portions of a chip are part of the regulation. Given the US Government has no way to validate that a portion of the chip was permanently disabled, they cannot take the chance.

The US government documents also do not point to any guidance on shipping wafers versus packaged products. Most of TSMC’s revenue comes from shipping wafers to outsource assembly and test (OSATs) firms that dice, package, and assemble products for TSMC’s end customers. In the case of Nvidia’s A100 and H100 GPUs as well as Biren, TSMC dices and partially packages the chips. Nvidia currently gets the rest of the packaging and assembly for most of their high-end datacenter GPUs in China.

The world’s most powerful supercomputer, Frontier, uses AMD’s MI250X which does not utilize TSMC’s packaging technology. Instead, AMD utilizes TSMC wafers which are then shipped to ASE, an OSAT which does the dicing and packaging. If TSMC were to ship finished wafers to China, Biren could use indigenous Chinese OSAT capabilities to fabricate the completed BR100 with currently unrestricted tools from firms like Besi, Veeco, and more. Therefore, finished wafers should be restricted.

Lastly, the shipment of the lower-end BR104 product should also be restricted. It is entirely plausible for Chinese OSATs to disassemble the [CoWoS-S](https://www.semianalysis.com/p/advanced-packaging-part-2-review) assembly used on BR104 and build BR100 from these deconstructed dies, with pre-2010 equipment. Furthermore, the 896GB/s die-to-die interconnect could still be utilized if the chip packaging and pin-out were modified.

It is clear Biren is attempting to evade sanctions.

[Share](https://newsletter.semianalysis.com/p/how-chinas-biren-is-attempting-to?utm_source=substack&utm_medium=email&utm_content=share&action=share)

It’s also clear that the sanctions were not well written, particularly regarding semiconductor equipment. The bans likely will not achieve their goals as they have major holes and enforcement issues.

Next, we will share some slides on Biren’s architecture. Of all AI hardware startups out there, this architecture bares the most resemblance to Nvidia’s.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ab1a3735-4277-45af-95db-616a566c326a_3022x1623.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1a457214-f7ff-4dc2-872f-c9eb3f72b154_3023x1618.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1f158df8-61cf-444b-bae4-5dda1c4e983b_3023x1618.png)

[Give a gift subscription](https://newsletter.semianalysis.com/subscribe?&gift=true)

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

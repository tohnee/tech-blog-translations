---
title: "China AI & Semiconductors Rise: US Sanctions Have Failed"
subtitle: "Huawei, SMIC, 7nm, H800, Domestic AI Capabilities, ASML, MediaTek, Qualcomm, Apple, RF Capabilities, Potential Sanctions"
date: 2023-09-12
source: https://newsletter.semianalysis.com/p/china-ai-and-semiconductors-rise
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
---

# China AI & Semiconductors Rise: US Sanctions Have Failed

**Huawei, SMIC, 7nm, H800, Domestic AI Capabilities, ASML, MediaTek, Qualcomm, Apple, RF Capabilities, Potential Sanctions**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

As we approach the [1-year anniversary on the October 7th China sanctions,](https://www.semianalysis.com/p/china-and-usa-are-officially-at-economic) it is abundantly clear that the export controls are failing. The Biden Administration’s stated aim was to limit Chinese firms’ ability to manufacture the highest end chips including those in AI and other technologies that could be used for nefarious purposes by the Chinese Communist Party. See the US justification below.

> The PRC is rapidly developing Exascale supercomputing capabilities and has announced its intent to become the world leader in AI by 2030.

> These systems are being used by the PRC for its military modernization efforts to improve the speed and accuracy of its military decision making, planning, and logistics, as well as of its autonomous military systems, such as those used for cognitive electronic warfare, radar, signals intelligence, and jamming. Furthermore, these advanced computing items and “supercomputers” are being used by the PRC to improve calculations in weapons design and testing including for WMD, such as nuclear weapons, hypersonics and other advanced missile systems, and to analyze battlefield effects. In addition, advanced AI surveillance tools, enabled by efficient processing of huge amounts of data, are being used by the PRC without regard for basic human rights to monitor, track, and surveil citizens, among other purposes.

> to limit the PRC's ability to obtain advanced computing chips or further develop AI and “supercomputer” capabilities for uses that are contrary to U.S. national security and foreign policy interests.

> [US October 2022 Restrictions](https://www.federalregister.gov/documents/2022/10/13/2022-21658/implementation-of-additional-export-controls-certain-advanced-computing-and-semiconductor)

However, the release of Huawei’s new flagship chip on SMIC’s N+2 (7nm) process, Chinese companies’ continued importation of billions of dollars of advanced semiconductor manufacturing equipment, and [acquisition of hundreds of thousands of powerful NVIDIA H800 & A800 chips](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing), it is abundantly clear that the Commerce Department’s standards were set at a level that will not ultimately inhibit China from breaking through the barriers set last fall.

In this report we'll explore what the Huawei chip crystallizes about the trajectory of Chinese domestic semiconductor manufacturing and AI capabilities. We will be covering:

- Huawei’s chip and its competitiveness with foreign chips.
- The market share/ASP/revenue impact to Apple, Qualcomm, and MediaTek from Huawei’s insourcing of silicon.
- SMIC’s N+2 (7nm) process technology, current capacity, and expansions plans
- The lithography tools they use and why current restrictions are flimsy.
- The potential of a future SMIC 5nm process node.
- Domestic AI capabilities using externally produced chips from Nvidia
- AI chips using domestic manufacturing
- RF capabilities for drones and detecting F35’s
- And finally, if the US and its allies are uncomfortable with this overall trajectory, a package of potential western responses to China related to front end equipment, chemicals, advanced packaging, and IP licensing that would totally shut out the CCP.

## **Huawei Kirin 9000S**

Let’s jump right in with the talk of the town, Huawei’s Kirin 9000S produced by SMIC. The chip uses a custom Armv9 core, and a custom GPU architecture designed by Huawei. The ability to design leading architecture in China is a big deal. While the US has stopped [AMD](https://en.wikipedia.org/wiki/AMD%E2%80%93Chinese_joint_venture) and [Intel](https://www.theregister.com/2015/04/10/us_intel_china_ban/) from various CPU deals with China in the past, it has not done been able to do so with Arm. Partially this is due to the joint venture Arm has in China, [which is not under their direct control](https://www.reuters.com/markets/deals/arms-china-relationship-complicates-ipo-2023-08-22/#:~:text=Arm%20itself%20holds%20an%20effective,48%25%20of%20the%20Chinese%20subsidiary.). Another reason is that the Armv9 instruction set is from Arm Cambridge. Additionally, they utilize Arm’s licensed A510 cores. The A510 core is designed in Arm’s Sophia France R&D center + Cambridge.

The chip is technically incredible. The [performance and power consumption profile in a variety of tests](https://twitter.com/tphuang/status/1698299732060262676) bring it on par with 1 to 2-year-old Qualcomm chips (S888 & S8G1). The RF side of the chip is amazing, using an integrated modem that is on par with Qualcomm’s current best. This is not surprising given Huawei was a bit ahead of Qualcomm before they were banned from using TSMC. The most important point is that the RF Front End chips are also domestically produced, which was a capability many thought China lacked.

The most shocking finding is that [when direct comparisons are done on identical IP, the Arm A510](https://twitter.com/tphuang/status/1698885806545387705) for Huawei’s Kirin 9000S built on SMIC’s N+2 (7nm) and 2022 Qualcomm’s S8G1 built on Samsung’s 4LPX process. The performance and power consumption of the Arm A510 cores are effectively on par with each other despite the process technology gap, indicating SMIC N+2 is better than most in the west realize. Part of the reason these chips are so close to each other is [Samsung’s poor yield](https://www.semianalysis.com/p/samsung-electronics-cultural-issues) and SMIC’s good [yield](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art).

Put simply, Kirin 9000S is a better designed chip than the West realizes. It has solid power and performance. Even with the lackluster export controls, this is a leading edge chip that would be near the front of the pack in 2021, yet was done with no access to EUV, no access to cutting edge US IP, and intentionally hampered. We cannot overstate how scary this is.

## **MediaTek, Qualcomm, and Apple Impact**

Quantifying the impact to Apple is quite easy. They gained between ~35 to ~45 million units of iPhone sales as a direct result from the Huawei’s ban in late 2019. This is easily over $20B of annual revenue for Apple that could evaporate if Huawei is able to regain its old footing. That is just smartphones, the impact to tablets, smartwatches, and laptops will be even larger for Apple.

The impact for MediaTek and Qualcomm is even worse. Qualcomm and MediaTek were the main beneficiaries of the 190 million annual Huawei SoC units that evaporated from the market following their ban. From 2020 to now, this share shifted to other Chinese vendors such as Xiaomi, Oppo, and Vivo. If Huawei regains its form, we calculate as much as $7.6B of revenue impact to MediaTek and Qualcomm.

![](https://substack-post-media.s3.amazonaws.com/public/images/81134e50-75fc-4d17-88d5-9b90f8e08437_1376x366.png)

This of course was in a 1.4 billion unit smartphone market, the current run rate is under 1.2 billion units. A much more nuanced analysis of the above as well as the RFFE impact to Skyworks, Qorvo, Murata, Qualcomm, and others is available for our clients.

The ability of Huawei to regain form hinges primarily on SMIC’s manufacturing capabilities, which we believe are very strong.

## **SMIC N+2, A True 7nm, Good Yields**

The process is a true 7nm process in terms of density. While the engineering decisions on specific pitches are different from TSMC’s 2018 7nm, it should be considered a similar process technology, and SMIC is at worst only a handful years behind TSMC. One could argue that SMIC is at most only a few years behind Intel and Samsung despite restrictions. As SMIC is replicating what has been done elsewhere, the gap could be even narrower due to their excellent engineering pool from mainland China as well as many courted immigrants from Taiwan that were formerly employed by TSMC.

As mentioned earlier it is on par with Samsung’s 4LPX in performance and power. The big questions are [yield](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art) and volume. While some pundits claim the yield is only 10%, we don’t believe that. In fact, we believe that SMIC’s process has good yield. There’s no definitive number here, but there are some data points that indicate this.

Why? We’ve heard a few soft remarks from our sources in China that yield is good. Allegedly their D0 is currently about ~0.14. For reference, TSMC’s N5 and N6 nodes are about half that.  TSMC of course is the gold standard, and Samsung/Intel “7nm” are closer although still ahead of what SMIC has achieved. Yield being this decent already is a huge flag that the SMIC N+2 process technology is healthy and developing. Parametric yield is the more important, unknown metric. But hearsay isn’t enough on its own.

For more tangible evidence, the channels, gates, and drains on the FinFETs as well as the contacts and lower metal layers look fairly clean. A process with low yield probably won't look as uniform. See these images from the [TechInsights](https://techinsights.com/) public brief. We recommend looking at their full teardown for more images and the exact pitches.

The last reason is related to the apparent binning of the chip. "Binning" in semiconductor manufacturing refers to the process of sorting and categorizing integrated circuits (like CPUs or GPUs) based on their performance and quality after they have been manufactured and tested. While chips can have defective transistors, called catastrophic yield, in many cases, working transistors still fail various performance and power tests. This is known as parametric yield. If a process technology has low parametric yield, the firm managing yield for the chip can make the binning process less stringent to improve the parametric yield. More chips can pass various tests, but it also leads to higher variability.

This has been done with mobile chips that yielded poorly in the past, for example the Qualcomm S8G1 on Samsung’s 4LPX. In the case of the S8G1, different devices with the same chip would have differences upwards of 10% on fully heat soaked devices in the same environmental conditions. While we haven’t seen rigorous testing of many devices in the same environment, there is enough on various Chinese forums to show that device to device variation is quite low.

None of this is bullet proof, but we believe that SMIC has good yield, and the 10% yield number some pundits have said is nonsense to downplay the significance. This is a real high volume production process technology. Just like Apple is the guinea pig for TSMC process nodes and helps them ramp and achieve high yield, Huawei will likewise help SMIC in the same way.

As a reminder, Huawei released the [first TSMC N5 produced chip](https://www.anandtech.com/show/16156/huawei-announces-mate-40-series), so this is a role they are very capable of playing. In two years, SMIC will likely be able to produce large monolithic dies for AI and networking applications. This is a similar time scale to what [Broadcom](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion) and Nvidia’s transition to new process technologies.

To understand yield better, read our simple primer and the other linked pieces. [1](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle), [2](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [3](https://www.semianalysis.com/p/i-semiconductor-the-regionalization?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [4](https://www.semianalysis.com/p/lithography-intensity-and-long-term?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [5](https://www.semianalysis.com/p/asml-and-the-semiconductor-market?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [6](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [7](https://www.semianalysis.com/p/austrias-silent-monopolies-on-advanced).

## **SMIC Equipment and Tooling**

This is due to their ability to use effectively all the same tools that TSMC and Intel have access to for their “7nm” processes. While theoretically there are tooling restrictions, [see our deep dive into the US chip sanctions last year](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing), they are effectively meaningless.

Despite SMIC’s N+1 process technology already violating sanctions, the US continued to grant licenses to semiconductor manufacturing equipment firms utilizing US technology. SMIC, CXMT, and many other Chinese companies that work directly with the PLA and are pursing process technologies that exceed sanctions continue to import whatever tools they need. There are effectively no bans and end use checks from the BIS and State Department are failing.

The equipment companies such as Applied Materials, Lam Research, Tokyo Electron, KLA, Screen, ASM International, Kokusai, etc. are selling basically every tool they offer to China. This is because most deposition, etch, metrology, cleaning, coaters, developers, ion implant, epitaxy, etc. tools for 7nm and even 5nm can also plausibly be used in 28nm. These tools are being sold to SMIC for “28nm,” but, in reality, SMIC is lying to the firms faces and using them for 7nm.

While SMIC is expanding 28nm and other trailing edge nodes, it is much less than they claim as these tools are being rerouted to leading edge. It’s even possible that people within these equipment firms know what’s happening, but are turning a blind eye.

The export controls are failing. They are not being enforced and the status quo has continued.

## **Lithography Equipment**

The lithography world is a bit different than the rest of these tools. There are some restrictions on specific DUV tools. The problem is they are meaningless for preventing 7nm. [We spoke through the problems in detail back in January](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography), but let’s rehash briefly.

China can and will be able to ramp 7nm production with currently allowed lithography tools. The NXT: 1980i, and improved Di, Ei, and Fi tools can be imported and serviced under current restrictions. The original 1980i is the tool TSMC used to ramp their N7 (7nm) to over 100,000 wafers a month at very high yield. The 1980i series was also used by Intel for their “7nm.”

This loophole has been clear to anyone whose familiar with the space. This is a perfect example of ineffective policy, whose stated goal is to stop further development, while leaving a clear loophole for China to abuse. ASML continues to benefit and plan for a massive increase in DUV, mostly lead by these "older" tools.

## **SMIC Capacity Is Not Limited**

While there are over 60 layers of lithography in the SMIC 7nm process. Only about 40 of these are critical layers, but for posterities sake let’s just say 60 layers require the latest 1980 tools. In reality, older ArFi tools, those from vendors like Nikon, and ArF/KrF/I-Line can be used for a number of these layers.

ASML claims the latest 1980Fi can do 330 layers of lithography an hour, but we believe this is a bit optimistic and is calculated off a low dose. Let’s be conservative and say [SMIC uses 2x the dose that ASML claims](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost) plus they have a fleet of Di, not Fi. This would mean each tool could do ~165 layers per hour.

We hear SMIC has well over 30 advanced ArFi tools from ASML. They have many more lithography tools on order as well, including the latest 1980Fi. These tools support all their process nodes, but can be used for 7nm and 5nm. We also hear they will have 15 total ArFi tools for their first 7nm fab which will be fully populated by the end of Q2 2024. It will take a few more quarters to ramp after that. Rumors state their next fab will be even larger. More rumors from China claim the first fab will have 50k wafers per month (WPM) of 7nm, but that initially seemed too big the first time we heard of it.

While we can’t validate these claims from China, it does appear to be very easy for SMIC to get ramp to 30k WPM of actual production in their 7nm fab, without taking tools from other trailing edge fabs.

![](https://substack-post-media.s3.amazonaws.com/public/images/552c0ab9-4423-4787-b87c-911450ab6134_2528x394.png)

This tacks with the optimistic 50k WPM claims, if they can bring the number of layers requiring 1980i down to 50 and they use doses closer to ASML claimed doses.

Even with 50% yields, 30,000 WPM could support over 10 million Nvidia H100 GPU ASIC dies a year. [No equipment](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis) used for [advanced packaging similar to CoWoS](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and) or [High Bandwidth Memory (HBM)](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis) is currently limited either. The cat is already out the bag in terms of capacity.

## **5nm Is Possible**

ASML is ramping to ship over 400 ArFi tools a year, [with claims of hitting 600 DUV tool capacity by 2025](https://www.semianalysis.com/p/asml-and-the-semiconductor-market). More than half of the capacity is penned for demand they see coming from Chinese fabs. While these tools will be distributed widely, to many companies, SMIC is the largest individual customer for ASML in China.

[ASML openly says this is explicitly for over 1.5 million excess/inefficient wafers per month by 2030](https://www.semianalysis.com/p/asml-and-the-semiconductor-market), with an additional 150k WPM of excess/inefficient capacity added each year. ASML says this is due to [regionalization of semiconductor supply chains](https://www.semianalysis.com/p/asml-and-the-semiconductor-market), but that’s just a cover for [China achieving semiconductor independence](https://www.fabricatedknowledge.com/p/chinese-evs-and-the-lagging-edge) and using DUV to reach 5nm.

To be abundantly clear, it is [explicitly built into ASML’s capacity plans and forecasts that China will be semiconductor independent](https://www.semianalysis.com/p/asml-and-the-semiconductor-market) from a semiconductor fabrication standpoint [as per their last investor day](https://www.semianalysis.com/p/asml-and-the-semiconductor-market). The rest of the supply chain is of course still highly intertwined including equipment, consumables, and design IP.

A “5nm” process that achieves over 130 million transistors per mm^2 is possible to achieve with high yields using ArFi multi-patterning. [The overlay capabilities of the 1980i series is good enough that 5nm can be manufactured at acceptable yields.](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography)

This SMIC N+3 “5nm” process would also be economical to produce given the level of governmental subsidies. While the lack of EUV would increase total lithography costs by 55% to 60% in our estimation, remember that [lithography is only ~30% of the total process cost](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost) at 5nm currently. This means that the total process cost would only be ~20% higher versus a 5nm that utilizes EUV. Yield likely takes a hit and therefore the actual number will be higher due to more defective chips per wafer, but it will not be an insurmountable barrier for China.

If nothing changes with current restrictions, we expect Huawei and SMIC to have a true 5nm based chip in 2025 or 2026 with large scale AI chips not so long after. The current export controls are not limiting China’s manufacturing capabilities or capacity.

## **China AI Capabilities**

Manufacturing capabilities are not out of reach, but even without those domestic manufacturing capabilities, China’s AI capabilities will be extremely strong. By the end of 2024, China in total will have more than 1 million A100 caliber or better chips from Nvidia. Remember [GPT-4 was trained on ~24,000](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure) A100’s and [Open AI will still have less than 1 million advanced GPUs even by the end of next year](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini).

The current restrictions on AI are flimsy at best. Nvidia quickly made new versions of their A100 and H100 GPUs that are effectively just as capable named the A800 and H800. These GPUs do not cut down the total compute or memory bandwidth. While NVLink speed are cut to 400GB/s, that is not restrictive for most parallelism strategies that are employed such as 8x Tensor Parallel, Fully Sharded Data Parallel, and Pipeline Parallelism. These cut downs are not able to be end use checked either and could potentially be reversed like Nvidia’s former crypto mining limiters, if the HW isn't fused off.

Furthermore, for the highest end systems with tens of thousands of H100 GPUs being deployed, they only use 50GB/s of Ethernet/Infiniband IO from each GPU to other GPUs on the network outside of each server. The bar for the restriction is 600GB/s total chip to chip IO. Chips better than the H100 can be made externally and imported legally with the current flawed sanctions. For example a theoretical 3nm chip with 10x the FLOPS of H100, 5x the memory bandwidth, and 500GB/s of Ethernet/Ultra Ethernet/Infiniband can be imported under current restrictions. A wafer scale chip/package can be imported under current restrictions.

China will have cutting edge chips from western firms and will be capable of training GPT-4 and better equivalents soon.

## **Domestic AI Chip Capabilities**

There are many scaled players and AI hardware startups that will soon be able to deliver on chips that are on par with Nvidia’s A100. These include Huawei, Biren, Tencent, Alibaba, Baidu, MetaX, and more. While we won’t dive into all their capabilities today, they will easily be able to deliver A100 class chips on SMIC 7nm in 2 years at significant volumes. While software is a challenge, China has more software developers than the US, Canada, and Europe combined. This shouldn’t be an insurmountable challenge either.

These chips are mostly designed using US EDA IP from Cadence, Synopsys, and Mentor Graphics (Siemens). [Huawei is rapidly advancing domestic EDA by investing massively.](https://ieeexplore.ieee.org/xpl/conhome/10019319/proceeding) Some players like MetaX are blatantly copying Nvidia [by making their chips CUDA compatible](https://www.metax-tech.com/en/goods/prod.html?cid=3). Others like Biren have many designers from Nvidia Shanghai and [their architecture is very reminiscent of Nvidia’s if you squint your eyes](https://www.semianalysis.com/p/how-chinas-biren-is-attempting-to), and [it’s a good architecture](https://www.semianalysis.com/p/how-chinas-biren-is-attempting-to). Biren has already [attempted to evade sanctions which we revealed exclusively.](https://www.semianalysis.com/p/how-chinas-biren-is-attempting-to)

Microarchitectures and system design will evolve and chips better than the H100 are well within sight with China’s domestic semiconductor manufacturing capabilities. China is [capable of building and networking very large supercomputers together.](https://www.tomshardware.com/news/china-builds-exascale-supercomputer-with-192-million-cores) Furthermore, China has leading optics manufacturing capabilities with firms like Innolight. Advanced packaging is also being developed rapidly. The combination of advanced packaging and optics will enable China to remain competitive with domestically produced semiconductors even if they are held back to 5nm or 7nm process technology.

China will have multiple firms capable of training better than GPT-4 next year alone. It’s not even a question. China is probably able to more effectively weaponize LLMs than the west is too due to their civil-military fusion and lack of antiquated, slow, and extremely expensive existing defense industry, just like they have with drones.

## **Radio And Sensors**

As an aside, there is practically nothing being done besides some minor ineffective sanctions on radio/sensor capabilities. Communications and sensors technologies are the most important for war, at least historically. While this may be changing with the rapid increase in drone use, the most effective drones are effectively using hardware that looks a lot like phone hardware. Furthermore, China already has radars capable of detecting the F-35.

They continue to improve this with various advanced compound semiconductors. The equipment being imported for their domestic silicon carbide and gallium nitride industries is also being used for RF applications that will be useful in war. Furthermore, there are multiple firms such as STMicroelectronics, whose technology is core to SpaceX Starlink, who are actively collaborating and [doing JV/IP transfers](https://www.reuters.com/technology/stmicroelectronics-sanan-plan-silicon-carbide-venture-china-2023-06-07/).

This JV/IP that will accelerate China’s capabilities massively under the guise that the technology can only be used for power semiconductor applications despite relatively easy repurposing of said technology capabilities gained from the JV for RF applications.

## **What Can Be Done**

The US government clearly views a Chinese semiconductor industry that can produce sub-14nm chips and memory ICs with 128 layers or more for NAND and 18nm half-pitch or less for DRAM as a significant threat to global security ([see here for an open-source take on what the PLA intends to do with AI chips](https://cset.georgetown.edu/publication/silicon-twist/)). Maintaining the current level export controls poses a significant threat to America and its allies’ long-term economic and national security.

The US government and its allies could stop the Chinese semiconductor industry in its tracks. Here are some steps that could be taken to ensure that China does not develop the ability to mass-manufacture the sorts of chips needed for high-end military applications in the coming years:

1. Limit ArFi immersion lithography tools.
2. Limit servicing of existing equipment.
3. Limit ArFi photoresist.
4. Limit masks.
5. Limit mask blanks, writers, and other associated infrastructure.
6. Limit metrology equipment.
7. Limit CMP equipment.
8. Limit epitaxy equipment.
9. Limit dry etch equipment.
10. Limit CVD and ALD equipment.
11. Limit advanced packaging equipment.
12. Limit ion implantation equipment.
13. Limit semiconductor manufacturing equipment subsystems and subassemblies.
14. Limit etchant gas.
15. Limit deposition precursors.
16. Limit chips that have >25.6Tbps of IO even if they have no compute.
17. Limit chips that have >1000TOPS of performance.
18. Limit the [licensing of 200G SerDes](https://www.reuters.com/markets/deals/republican-rubio-slams-us-approval-chip-deal-involving-firm-with-china-ties-2022-08-29/).
19. Limit EDA tools.
20. Limit Joint Ventures and inbound investments.

Half measures will not work, but a full-scale assault will make it so the cost of replicating the semiconductor supply chain domestically is neigh on impossible. While we aren’t advocating for any of these specifically, it is clear the west can still stop China’s rise if decisive action is taken.

*Thanks to Jordan and Doug for help pulling together this piece. Check out [FabricatedKnoweledge](https://www.fabricatedknowledge.com/) and [ChinaTalk](https://www.chinatalk.media/), they’re great. Also tune in later this week to [ChinaTalk](https://www.chinatalk.media/) + Transistor Radio where we’ll continue the discussion around SMIC and Huawei, further explain the arsenal of options, reflect on Semicon Taiwan, global impact of Chinese EVs, and more.*

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

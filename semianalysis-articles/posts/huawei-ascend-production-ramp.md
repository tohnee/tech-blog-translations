---
title: "Huawei Ascend Production Ramp: Die Banks, TSMC Continued Production, HBM is The Bottleneck"
subtitle: "H20 Shipments, Blackwell B30A, Bottlenecks to Chinese Chip Production, Export Controls, CXMT, SMIC, Cambricon"
date: 2025-09-08
source: https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp
crawled: 2026-09-15
authors: ["Dylan Patel", "AJ", "Myron Xie"]
tags: ["Supply Chain", "Accelerators", "AI Infrastructure", "Semiconductors", "Export Controls", "Foundries"]
audience: only_paid
paywalled: true
---

# Huawei Ascend Production Ramp: Die Banks, TSMC Continued Production, HBM is The Bottleneck

**H20 Shipments, Blackwell B30A, Bottlenecks to Chinese Chip Production, Export Controls, CXMT, SMIC, Cambricon**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Compute is the lifeblood of AI. He who controls ~~the spice controls the universe~~ the compute will control the production of tokens and reap the benefits of AI. Without compute you do not have a seat at the table. The United States technology community is all in on compute and AI as the next platform and is now adding compute at a staggering pace.

There is competition, and it not only comes from companies but from *countries*, and the US government has placed a series of export controls to limit China’s rising compute. Today the US controls and is the undisputed leader in compute [with more than 70% of the worlds deployed FLOPs](https://semianalysis.com/accelerator-model/). One way to stay ahead is to keep going full steam while hindering your competition. Limiting your competitor nation state from compute, which will limit them from intelligence, is the current policy to stay ahead in the AI race.

These moves have led to backlash, including with China cutting rare earth minerals and magnets off from the US. Secretary of Commerce [Howard Lutnick says](https://www.reuters.com/technology/nvidia-resume-h20-gpu-sales-china-2025-07-15/) the resumption of Nvidia GPU sales to China were required to restart China's shipments of their linchpin supply chain materials.

But constraints have also led to adaptation, and Chinese companies have adapted. High batch sizes and disaggregated serving are but two examples. Despite advances, in the case of DeepSeek, most of their tokens are still inferenced on western hardware. We wrote about this dynamic in our recent DeepSeek debrief. [Training of DeepSeek's next generation model was also delayed by the use of Huawei chips](https://www.ft.com/content/eb984646-6320-4bfe-a78d-a1da2274b092), as we also said in the debrief.

This is not a stable equilibrium. There are always moving pieces in the race for intelligence. Beijing plans for the long term and knows it must secure its own domestic compute destiny. There is an irony: in the 2010s China kicked out Google to enforce its Great Firewall and foster its domestic industry, this time the US government is withholding hardware technology so they cannot seize the lead in AI.

**We believe that at China’s core, they want to control not only its internet and AI, but the hardware that supports it.** From silicon to tokens, China seeks sovereignty over every layer of the stack, and given recent history will never want to be beholden to foreign powers. Enter Huawei.

China loves national champions, and in it’s characteristic capitalism, tends to funnel resources to a few national champions. Today’s champion is probably Nvidia's greatest adversary: Huawei. We expect Huawei to be able to make millions of chips this year, and to be bottlenecked by HBM next year. Today we want to talk about Huawei, which can translate as “China’s achievement”.

# All In with Huawei’s chips

Huawei is the key piece for China’s compute destiny. Huawei’s chip ecosystem is vertically integrated and capable network of tools, fabs, and design that allows it to express a full stack vision of hardware. This hardware is very impressive although less efficient then western hardware.

Our previous investigation into Huawei’s fab network is a great example of their broad reaching network.

![](https://substack-post-media.s3.amazonaws.com/public/images/b7faa941-ca23-437e-a610-e1cf902f0f55_975x615.png)
*Source: SemiAnalysis*

Huawei wants to vertically integrate the entire manufacturing process. The goal is to own not just the manufacturing of the logic die, the brains of the chip, but also the memory and packaging. They have even created their own tool company, [SiCarrier to copy foreign firms tools](https://semianalysis.com/core-research/sicarrier-huawei-wfe-announcement/). Huawei has bought over [$9B of tools to put in their own fabs as well as reverse engineer to replicate](https://semianalysis.com/wafer-fab-model/).

Their efforts are not to be underestimated. SiCarrier, for example, has recently raised $2.8B in funding. That money is going into building fabs dedicated for Huawei staffed by Huawei employees. [Some reporting on these fabs](https://www.ft.com/content/64caeab8-a326-4626-98fb-e1bf665827d3), which we believe to be Huawei owned and operated, suggests that their combined production by next year could entirely exceed SMIC, the current leader and where production is currently outsourced. With Huawei ramping up their own efforts, allocation at SMIC can be freed up for other chips, including Cambricon. [The Cambricon chip is itself popular among Chinese companies, especially ByteDance.](https://semianalysis.com/accelerator-hbm-model/)

Huawei operating their own fabs will represent a material increase in Chinese production, but also in their ability to iterate, control, and improve on processes. Huawei and SMIC will directly work on increasing yields, refining R&D for the next node, and bolstering Chinese semiconductor manufacturing capability.

Currently, all high volume chip production is outsourced to SMIC, the leading Chinese pure-play foundry. This includes the Ascend series of accelerator chips along with the Kirin mobile processors. Yields are poor for SMIC’s 7 nm-class processes due to a combination of immaturity, export controls, and the inherent difficulty in yielding large die such as the Ascend. Thus a relatively low percentage of SMIC’s overall capacity is allocated to producing Ascend die, since smaller mobile processors just make better business sense at this point. But this can change quickly. Let’s discuss what is possible for Huawei….

![](https://substack-post-media.s3.amazonaws.com/public/images/0a96a4af-220b-4517-b075-b813a3e86779_1024x289.png)
*Source: SemiAnalysis*

# Huawei Production Numbers and SMIC's Ramp

Our data shows Huawei’s production is **507k Ascend units shipped in 2024**, the majority of which are 910Bs, **and 805k this year, 653k of those being 910C.** The 910C is the more advanced version. This includes die made by TSMC and SMIC.

![](https://substack-post-media.s3.amazonaws.com/public/images/d1097703-5af3-4945-abd3-d177e0e4cce3_1024x557.png)

SMIC, hampered by export controls, struggled to get production off the ground. But Huawei got Ascend die fabricated at TSMC while SMIC ramped. This was a violation of export controls and Huawei ended up receiving **more than 2.9M Ascend die, which can be used for both 910B and 910C.** [We detailed this here.](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/)

It is specifically this “Die Bank” of foreign chips from TSMC that gets them through 2024 and 2025. Without this Die Bank, Huawei's Ascend production numbers would be much lower.

![](https://substack-post-media.s3.amazonaws.com/public/images/24bd087c-5279-42ab-a2db-d4dede2327d4_943x625.png)
*Source: SemiAnalysis*

We expect that the TSMC die bank to run out within the next 9 months. SMIC, however, now has more than enough capacity to produce meaningful volumes of chips. We forecast that SMIC will no longer be the bottleneck for Ascend production, as they will have sufficiently ramped capacity by end of year.

![](https://substack-post-media.s3.amazonaws.com/public/images/7e2d7db4-ca8d-4708-8692-ff52f8abd9c3_1024x628.png)
*Source: SemiAnalysis*

The chart above shows a baseline scenario with a modest increase in SMIC capacity allocation for Ascend. It requires at most 20k wafers per month (wspm) of SMIC capacity to produce millions of Ascend die per month.

For reference, a conservative estimate of SMIC's total advanced node capacity (7nm and below) is 45k wspm by end of 2025, increasing to 60k wspm in 2026 and 80k wspm in 2027. In addition, Huawei is building their own fabs, not all of which are export controlled, and collaborating with SMIC on process technology, so production could ramp higher for advanced process technologies.

If 100% of capacity was allocated to Ascend die, their production capability would be in the tens of millions per year. They are on track to be more than capable of supporting a large domestic demand for China-produced compute die.

![](https://substack-post-media.s3.amazonaws.com/public/images/e783043c-c608-41d9-9485-463efd574b0f_1024x647.png)
*Source: SemiAnalysis*

Our forecasts above use a conservative estimate for both yield and its rate of improvement in the future. It's very likely that SMIC can exceed these estimated as its 7nm nodes mature. Our estimates for yields are lower than TSMC, Intel, Samsung, ASE, Amkor, etc for front end wafers and packaging.

![](https://substack-post-media.s3.amazonaws.com/public/images/ab82fa42-76b8-4cf1-861d-2561586f98e8_1024x554.png)
*Source: SemiAnalysis*

Indeed, yield is an important lever that can be pulled to increase production without giving up more allocation. With just small increases in yield beyond our forecast above, SMIC will be able to produce several million Ascend die at lower allocation amounts than they would otherwise. Every percentage counts and SMIC has their best engineers working on exactly this problem.

![](https://substack-post-media.s3.amazonaws.com/public/images/6489670c-ac91-4620-9a21-94f4a554b74b_1024x301.png)
*Source: SemiAnalysis*

In other words, **SMIC only needs small amounts, as low as single digit percentages, of allocation to produce more than a million die as soon as early next year.** Production to a couple million is possible, more allocation is all that is needed. For the reasons we articulate above, we believe the reported number of 200k Ascend chips to be significantly off the mark.

While SMIC is expanding and is no longer the bottleneck and Ascend production, Huawei's long-term ambitions include its own fab network buildout. We noted in our [Fab Whack-A-Mole report](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/):

> Huawei is clearly taking full advantage to the tune of $7.3B of WFE expenditure in 2024, up 27% year-on-year. They’ve gone from effectively zero in 2022 to the 4th largest WFE customer globally in two years.

Since we published that report in fall of 2024, the Huawei fab buildout has, if anything, accelerated. Their ecosystem of semiconductor-related shell companies is expanding. Massive new cleanroom buildouts are in progress. And improved domestic options and possible diversion of $30B+ of imports of wafer fabrication equipment means they are likely able to equip these fabs as well. The details are worthy of their own report, but suffice to say Huawei continues with a large, concentrated effort to own every vertical in the Ascend supply chain.

# TSMC Access

Huawei currently makes many mobile chips, but there is zero reason to do so from a strategic geopolitical perspective. Oppo and Xiaomi currently fabricate mobile SoCs at TSMC. They are ramping up their own designs to decrease dependence on companies like MediaTek and Qualcomm.

Huawei can reduce their mobile SoC production while not consuming, in any meaningful volume, SMIC allocation. The continued access to TSMC for other Chinese entities decreases the pressure for SMIC to make mobile SoCs, meaning more can be allocated to AI chips.

Huawei and SMIC can ramp up AI production without having to worry about serving all the nation’s demand for mobile chips due to other companies' access to TSMC.

## Export Control Lag Benefits SMIC

Another part of SMIC’s expansion strategy is stockpiling considerable amounts of semiconductor tooling. The controls are released on an announced schedule and it's usually easy to anticipate what will be included.

This is due to timing differences in controls that they can take advantage of. For example, the U.S. routinely exempts Japanese and Dutch companies from its equipment export controls. Ostensibly this is done because they are allied countries and have their own export control regimes and semiconductor industries.

The problem, however, is that when new export controls come out, Japan and the Netherlands **do not immediately follow.** In many instances, matching controls are delayed by 6 months or never. Chinese companies can rush order years’ worth of equipment to stockpile, while American vendors are shut out of the process.   Japanese WFE vendors are happy to sell into this gap with margins fattened by order expedites. Many key suppliers are seeing well above 40% revenue share from China:

![](https://substack-post-media.s3.amazonaws.com/public/images/d375fbdb-a48c-4f70-8e46-74e42e8ad7e6_1024x382.png)
*Source: SemiAnalysis*

In cases where controls do follow the US, Japan and the Netherlands do not have any matching controls on re-exporting. This means that it is possible for restricted tooling to reach China if it goes through a different country first.

In addition, the use of “advanced ICs” as the bar for restricting tools leaves room for issues. [ASML’s NXT:1980 scanners are perfectly capable of 7nm-class logic](https://semianalysis.com/2023/01/29/the-gaps-in-the-new-china-lithography/), and likely beyond if economics (throughput and yield) can be ignored or subsidized. These are allowed into China and even to certain SMIC facilities.

Export controls, as noted, can be expanded in addition to very stringent enforcement of existing mechanisms. This includes tighter coordination with allies on timelines for matching controls and getting buy in on re-exporting.

We are broadly encouraged by the administration’s [Action Plan](https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf). As an example, we are pleased to see controls on semiconductor subsystems being called out. This is a drum [SemiAnalysis has been beating](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/?utm_source=substack&utm_medium=email) [for a while](https://www.chinatalk.media/p/breaking-huawei-tariffs-done-right?utm_source=substack&utm_medium=email) and think it is the right direction. With that said, many subsystem firms that supply western players such as VAT Group in countries like Switzerland without controls will not be stopped from shipping critical chambers to China.

The Action Plan also included concrete suggestions around aligning protection measures globally, which we think if implemented, will greatly ameliorate the issue of alliance's lags in export controls described above. The issue is that SMIC and CXMT are able to continue to expand production because the sanctions on them are flimsy. International co-operation, especially with partners in Korea, is key to get right and ensure that Chinese commercial bottlenecks are not eased. Korea manufactures a huge amount of memory and Samsung has historically supplied large amounts of memory into China, so tight alignment of goals and enforcement is critical.

The other part of the supply chain that is just as critical is memory. This is where we believe the key constraint lies.

# HBM Is the Bottleneck

**We believe HBM production is the bottleneck**. **China does too**, which is why they have asked US officials to [relax controls on HBM as part of the recent trade talks](https://www.reuters.com/world/china/china-wants-us-relax-ai-chip-export-controls-trade-deal-ft-reports-2025-08-10/). What the ask omits is telling: it does not include more TSMC access or lithography tools. Beijing is specifically asking Washington to loosen HBM restrictions.

Much like how Huawei was able to stockpile TSMC logic wafer inventory, they were also able to stockpile HBM inventory. [Samsung, due to their failures in entering the accelerator supply chain](https://semianalysis.com/accelerator-model/#) for Western chips, sold their product to Chinese customers that funneled this inventory to Huawei. This is why it is so critical to work with Korea on enforcement of memory controls moving forward.

**Samsung alone has directly provided 11.4 million stacks of HBM to China,** **including a staggering 7M stacks in the 1-month gap between controls announcement and enforcement dates**. When including other providers and methods of shipment, that is 13 million stacks of HBM.

Specifically, on December 2nd 2024, the Bureau of Industry and Security (BIS) announced controls on anything more advanced than HBM2E. Full compliance was required on December 31st 2024. **Samsung exported as much as possible to China in that one quarter. This comprises the majority of China's HBM.** They were able to achieve this due to the US Government and media telecasting the restrictions for many months before they came out.

![](https://substack-post-media.s3.amazonaws.com/public/images/d8177c30-85ab-4e0e-8589-5caf37fa2468_1024x716.png)
*Source: SemiAnalysis*

After the ruling, Samsung HBM still made it into China. [We previously detailed](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/) how companies like CoAsia Electronics and Faraday supplied non-functional chips with HBM into China, though we believe due to our efforts in exposing this both privately in late January and publicly later that it has now stopped with revenue numbers returning to normal. This does not mean that HBM smuggling has stopped entirely, though. There could be other sources.

![](https://substack-post-media.s3.amazonaws.com/public/images/eacc8e8d-f8b4-4504-8a6d-01c9526bcb06_1024x707.png)
*Source: SemiAnalysis, Company Reports*

In sum, **China has procured 13M HBM stacks which is sufficient for 1.6M Ascend 910C packages**. Despite this, we expect that **China will be bottlenecked by HBM by the end of the year** as they run out of foreign HBM.

![](https://substack-post-media.s3.amazonaws.com/public/images/0cd3fa39-d0d4-4cc2-80b7-239979c609ca_1024x509.png)
*Source: SemiAnalysis*

China can easily make more than **805k Huawei Ascends this year** from TSMC and SMIC capacity, **but they will not because they do not have enough HBM.**

We expect SMIC's production to be 1M 910Cs and almost half a million 910Bs this year, however, not all of them will be turned into ASICs as the HBM is not available. If some HBM enters through smuggling, then Huawei can produce more Ascend AI ASICs.

## Without Foreign HBM, China has no Domestic AI Accelerator Industry

Without access to more foreign HBM, Huawei will not be able to fabricate even 1 million Huawei Ascend chips next year. They must rely entirely on domestic production which we will detail below. Nvidia and AMD have effectively 0 competition in China once these HBM banks run out.

The other option available to China is utilize slower GDDR and LPDDR memory, but this is not suitable for the leading language models with modern reinforcement learning techniques or for large scale inference deployments.

## Domestic HBM Industry - CXMT

China's main DRAM player, CXMT, has caught up with the west rapidly. This is due to a combination of extremely strong domestic engineering capabilities, poaching engineers from Samsung, SK Hynix, and Micron, as well as the leading tool vendors Applied Materials, Lam Research, and Tokyo Electron teaching them sub-processes.

CXMT is able to ship DDR5 memory, only a couple years behind SK Hynix, Micron, and Samsung, and is winding down profitable DDR4 production previously reserved for PCs and mobile. While they have not shipped much HBM, their roadmap is aggressive. By next year, their production capacity will rival that of Micron's, though not fast enough to save Huawei Ascend's production. In 2026, we expect them to be producing 257k WPM, which would be just under 15% of global DRAM production. In our estimates, this scales to 490k in 2030.

![](https://substack-post-media.s3.amazonaws.com/public/images/a3181910-0872-4be2-90ff-d0e55d4dc206_1024x875.png)
*CXMT’s Hefei facility for DRAM and HBM production, one of the largest in the world. Source: SemiAnalysis.*

CXMT's shift in focus and production ramp are driven in part by investments from the CCP. China's "Big Fund III", which started in May 2024, invested $2B into the company. CXMT is also expanding in Shanghai as well as Beijing, with HBM packaging subsidiaries being set up in the former.

Expecting, though ultimately averting, an entity listing by USG, CXMT stockpiled years of tools in 2024 and is likely still adding HBM-specific gear. CXMT is still not entity listed! While HBM was noted as a key focus in that salvo of controls, the previous administration failed to include China’s HBM champion. **The Trump administration needs to solve this failure from the Biden administration immediately**.

The stockpiling matters as advanced tools, like Hanmi's TCB systems for HBM3, are restricted, but they are not that instrumental. Older systems can be run slower without impacting cost too much. More importantly, CXMT can still procure leading edge equipment for Through Silicon Via (TSV) formation - that is critical for making HBM -through Japanese suppliers. In addition, Chinese OSATs such as JCET and Tong Fu are also racing ahead with their R&D efforts and building capacity for the critical TSV and stacking processes to package front end HBM wafers from CXMT. This is unlike the Western memory incumbents who have vertically integrated these processes. This is a typical example of Chinese industrial development where multiple players are encouraged to develop domestic manufacturing capabilities: creating cutthroat competition that accelerates the speed of development. It is therefore critical to not just focus controls on CXMT, but the whole of China as critical process steps can always be outsourced.

**Because front-end logic is currently not the binding constraint, Beijing's main asks in the trade deal target HBM and the relaxation of controls relating to this set of tooling**. Given the importance of HBM, it is critical to understand CXMT's future production depending on various allocation scenarios.

# CXMT Production Forecast

This can play out in several ways, depending on how much wafer capacity is given to HBM. China can easily produce tens of millions of stacks with less than 50% of wafer capacity. CXMT is at a bit over ~250,000 wafers a month of production capacity and is expected to reach 300,000 wafers by the end of the year.

Currently they have not built out the tooling required to convert standard DRAM production lines to HBM, but it is inevitable. Properly designed, targeted sanctions can slow this conversion massively.

![](https://substack-post-media.s3.amazonaws.com/public/images/99319b48-6c1d-41d4-9861-747155dadc24_1024x763.png)
*Source: SemiAnalysis*

Different scenarios lead to different amounts of Huawei Ascends produced. As noted, SMIC can produce the die needed to match the HBM.

![](https://substack-post-media.s3.amazonaws.com/public/images/42800f32-cc9b-4869-8ef9-2d1f176df486_1024x769.png)

To be clear, this could change. The rate of production for CXMT could increase if they continue stockpiling key tooling or significantly improve yields. The might of China’s manufacturing capability and capacity knows no bounds. This estimate is somewhat conservative, it is likely that CXMT is able to produce the significantly more capable HBM3e in 2026.

**We believe CXMT will only be able to make ~2 million stacks of HBM next year, which is only sufficient for 250,000-300,000 Ascend 910C's.** Yields and capacity conversion will take some time to improve for CXMT to commit significant capacity.

![](https://substack-post-media.s3.amazonaws.com/public/images/3db74357-492f-4ef2-86e7-d554edefa682_1024x563.png)

If all leading edge logic die capacity could be paired with HBM, Huawei production of Ascend would grow from 805k this year to 1,175k in 2025. More importantly, **production next year would grow from 300k to over 5 million Ascend 910C!**

**Our analysis indicates that export controls have been effective in constraining and limiting Chinese chip production capabilities.** Assuming no smuggling, China will be able to make *less* Ascends next year, not more. CXMT is *squeezed tight*. Had controls not been present, the Ascend ramp would be fully realized, Chinese models would be served on Huawei Ascend at scale, and there would be enough compute capacity that advanced models like DeepSeek R2 and V4 would already be here. Not to mention, with more capacity, China would be better positioned to export their AI on their chips.

As such, it is absolutely critical to ensure the application, enforcement, and continued updating of export controls to prevent CXMT and related entities from ramping production. As mentioned, this includes not just CXMT but OSATs and subsidiaries they work with. Second, it is also important for the intelligence community to track and identify any instances of HBM smuggling, [like the Faraday + CoAsia scheme which we disclosed privately in January and publicly reported on later](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/).

**By no means should HBM be allowed to be shipped into China**. Production of AI chips over the next few years is heavily gated by CXMT's ramp and foreign shipments of HBM.

There is very strong incentive to find ways to ship HBM into China. This is why enforcement of controls are so critical.

There is another pillar to China's production strategy, separate from memory and logic. This pillar is about networking the chips together and where they are made.

# Networking and Datacenter CPU

Chips do not exist in isolation. We have argued that the [system matters more than the microarchitecture](https://semianalysis.com/2023/04/12/google-ai-infrastructure-supremacy/) for years. Clusters are comprised of many tens of thousands of interconnected chips and how they are interconnected matters.

We detailed Huawei's CloudMatrix 384, or CM384, system below.

We believe the networking equipment used, specifically the scale up switches, are being made at TSMC and not at SMIC through shell companies. We also think they are stockpiling this equipment.

We believe Huawei has also been able to manufacture their datacenter CPU at TSMC. This showcases that current controls aimed to limit Huawei's access to TSMC are insufficient. The Ascend AI ASIC is 7nm, but because of poor screening, Huawei has been able to procure technology from the more advanced TSMC 5nm node.

![](https://substack-post-media.s3.amazonaws.com/public/images/37cae26b-6364-4944-b04b-907174bffdc8_1024x470.png)
*Huawei's KunPeng 930. Source: Kunal , SemiAnalysis*

By producing these chips at TSMC, this frees up capacity at SMIC, meaning more allocation can be given to the Ascend or [Cambricon](https://semianalysis.com/accelerator-hbm-model/) programs (HBM permitting). This, as mentioned earlier in the report, is a critical variable. If SMIC had to make the networking equipment, this would squeeze the wafer allocations towards Ascend significantly.

There is all the incentive in the world for China to offload as much production as possible to TSMC. They have used shell companies before and there is ample evidence they are still doing it. While some ideas around KYC and red flags have been implemented, we believe that existing frameworks are insufficient.

# Nvidia and Huawei: Blackwell and the H20

The US government previously banned the Nvidia H20 chip from going into China, but recently indicated that Nvidia will be granted a license to be able to export the chip. As we have previously noted, the H20 is a capable chip with more memory than the banned the H100, though it has less much fewer FLOPs. Having more memory is helpful for inference performance.

Nvidia is poised to sell its existing inventory of the H20 and H20E (a variant with even more memory) at a minimum. This will amount to more than several hundreds of thousands of chips and billions of dollars of revenue.

There have also been [reports](https://www.reuters.com/world/china/nvidia-working-new-ai-chip-china-that-outperforms-h20-sources-say-2025-08-19/) of a more advanced version based on the Blackwell series. This is slated to have just as much memory as the H20 but will also contain significantly more FLOPs. Specifically, the B30A could have more than 10x the FLOPs than the H20, significantly above the export control threshold. The B30A could be positioned at half the price and have half the performance of the B300. The solution to this is rather simple: just buy 2x the chips for equivalent performance. Given how [strong and weak scaling work in machine learning workloads](https://hpc-wiki.info/hpc/Scaling#Strong_or_Weak_Scaling), this is a valid path to remain competitve.

The B30A is argued as needed to be shipped to China due to decreased interest from China in the H20. A lot of this is due to government pressure of China's major tech firms. While there is significant messaging that China has decreased interest in the H20, we do not believe this to be true.

Specifically, we do not believe this is reflective of China’s demand for compute or foreign chips. It is an incorrect policy being pushed from the top down which will be reversed as soon as Huawei runs out of HBM to produce more Ascend chips, or it could even be orchestrated brinkmanship to get approval to a more powerful chip.

This is on the tail of other news, like [DeepSeek unable to get acceptable performance on Huawei's chips](https://www.ft.com/content/eb984646-6320-4bfe-a78d-a1da2274b092). That is no coincidence. Export controls are working and the biggest blocker for more progress is compute.

China may be trying to psyop their way into getting the significantly more performant Blackwell chip. While the H20 and the H20E have much, much better software than the 910C, it is arguable that they are in the same league. However, it is unquestionable that the B30A would be in a league of its own. Given that the H20, H20E, and especially the B30A are good at inference, this also allows Chinese companies more compute to serve their models and applications.

It will allow them to export Chinese AI on hardware they own. This will increase the proliferation of Chinese AI and Chinese apps, inevitably taking market share away from American applications. The American AI stack is American AI on American chips, not just the chips.

The **US needs to balance having China on the US AI stack and slowing the development of their own, while also limiting the quality and volumes that are shipped into China**.

The H20 is allowed into China, but **the progression of shipping more powerful chips into China should be closely guarded and watched considering China's domestic capabilities**.

**The US should only move the quality of a chip shipped to China when it becomes clear China can ship something competitive to the H20E in significant volumes.**

Regardless of the exact SKU, the export licenses have several implications discussed below.

## Implications of Compute Diplomacy

First, it means that there will be more chips for top players like DeepSeek and Alibaba to use for Reinforcement Learning (RL). RL is a big driver of progress right now. The majority of RL compute is inference, which the H20 and especially the H20E, are good at. The B30A will have even better performance.

Players like DeepSeek had enough compute to keep improving – R1 received a major update with performance increases on a timeline that is like o1 -> o3. We firmly believe GPT-5, Claude 4, and Grok 4 are considerably ahead of R1 though, especially in agentic tasks.

However, problems in AI are solvable by two things: **talent and compute**. DeepSeek has always had the former, now they will have more of the latter. We expect DeepSeek's rate of progress to materially increase as they receive substantial volumes of any chip that gets into China. DeepSeek has ambitions to release a multimodal model in V4, but scarce compute is slowing progress.

Alibaba (Qwen) and Moonshot (Kimi K2), have also yet to produce a large multimodal model, primarily focusing on text only due to compute limitations. They will release multimodal models this year, but they are still squarely behind OpenAI, Anthropic, and Google in many capabilties. If Blackwell GPU shipments come too early, that will accelerate China's pace.

The second major implication of this is that China will now have more compute to serve and inference models to its population. Compute constraints affect user experience, with DeepSeek [deliberately serving R1 at low speeds to users to preserve compute](https://semianalysis.com/2025/07/03/deepseek-debrief-128-days-later/).

Poor user experience from the lack of compute has greatly limited China's ability to deploy AI. As user experience improves, so will adoption, and the economic benefits from AI. It is easy see a future in which models are pre-trained via H800s, post-trained on H20s, then served to the population on Ascends and H20s. There is so much demand for AI powered products that should more capacity to serve these models exist, it would immediately be satisfied. One of the reasons Chinese models are open sourced is that it allows for other people to serve their models for them. With more capacity, models can be closed sourced and dependence on American providers cut off.

Claims that models trained on one chip must be inferenced on the same type are entirely false. Anthropic did different stages of research and training for Claude 4 on GPUs and TPUs. Additionally, Claude 4 inference is offered on [Nvidia GPUs, Google TPUs, and Amazon Trainiums](https://semianalysis.com/2025/01/31/deepseek-debates/). This complexity is all while [Anthropic is also the fastest growing AI company in terms of revenue](https://semianalysis.com/tokenomics-model/) with by far the most capable model for software engineering.

DeepSeek, Alibaba, Moonshot, etc primarily train their models on Nvidia chips and we do not think this will change anytime soon. If the Blackwell version ships, gains across all levels will be more pronounced.

![](https://substack-post-media.s3.amazonaws.com/public/images/b8906e10-1743-4f4c-abb1-5d649fad9d3c_1024x661.png)
*Source: SemiAnalysis*

# China’s compute at a snapshot

With the H20 approved, this represents a material increase in the number of FLOPs and memory that China has access to. The 910C will be the first meaningful effort of indigenous production in China in terms of realized FLOPs and memory. We also expect some re-exportation into China by various bad actors, constituting meaningful volumes of H100 and low volumes of B200.

![](https://substack-post-media.s3.amazonaws.com/public/images/0f265adf-6ec0-4a78-8ab9-da60971e32ce_1024x697.png)
*Source: SemiAnalysis*

Should the Blackwell version ship, gains around FLOPs will be even more pronounced as the chip has significantly more FLOPs. China will end up having more FLOPs in that scenario, in addition to more memory.

![](https://substack-post-media.s3.amazonaws.com/public/images/e7efaeb9-6f42-45b4-8929-d028a9d45cdd_1024x694.png)
*Source: SemiAnalysis*

This is not to mention that Chinese players, including major ones like ByteDance, can still access compute through renting in non-restricted countries. For example, ByteDance can still access top of the line Blackwell GPUs from providers like Oracle and Google. We have previously covered this relationship in detail. Malaysia, in no uncertain terms, has become a huge market for Nvidia. Export controls were also effective in ensuring that it remains that way, with [Malaysia immediately distancing themselves from any effort around the Huawei Ascend](https://www.reuters.com/world/asia-pacific/malaysia-government-say-not-involved-local-ai-project-involving-huawei-chips-2025-05-21/).

Renting enables a path for Chinese dependence on Nvidia without Nvidia chips being in China, which is possible because the chips do not need to be in China. **Bytedance's Seed models were trained in the US on a US cloud.**

Inspecting GPUs is much easier in Malaysia than in China. As such, it is an effective way to limit any unauthorized re-exporting by bad actors, as we believe methods like location tracking are technically intractable and easy to bypass. Note that renting will still allow China access to the capability of training advances models. If allowed to be used for serving the models, this allows China the chance to proliferate their AI through new and improved AI powered applications, taking market share away from American products. The critical difference, though, is that access can be cut off.

With that said, China will not allow their data to be shipped out of China in large volumes hence there is still significant need for domestic AI capabilities. Selling chips into China does not change China's drive for total silicon self sovereignty and will only serve to help provide a buffer while local production meets demand.

It is worth remembering that China's focus on silicon self sovereignty predates US export controls. The argument Blackwell needs to be sold into China is a false narrative as Huawei will soon run out of HBM. Selling chips into China only served to bail them out until domestic production ramps. The production ramp will not slow until self sufficiency is achieved. Shipments of Blackwell must be weighed with a close eye on production of domestic capabilties. [If Huawei, Cambricon, and CXMT accelerate production faster than expected, then the US should raise the bar sooner.](https://semianalysis.com/accelerator-hbm-model/)

Next, we dive into Nvidia’s future in China. This includes expected revenue from the H20 and newer China specific chips on the horizon. We also compare how much compute China has relative to the US how the is absolutely dominating China when it comes to both memory and FLOPs.

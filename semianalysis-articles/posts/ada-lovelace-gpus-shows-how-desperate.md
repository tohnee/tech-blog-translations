---
title: "Ada Lovelace GPUs Shows How Desperate Nvidia Is - AMD RDNA 3 Cost Comparison"
subtitle: "Nvidia's first cost disadvantage versus AMD in a decade"
date: 2022-09-23
source: https://newsletter.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Ada Lovelace GPUs Shows How Desperate Nvidia Is - AMD RDNA 3 Cost Comparison

**Nvidia's first cost disadvantage versus AMD in a decade**

Nvidia launched their new Ada Lovelace GPU lineup this week. In general, performance improvements are massive, with as much as 2x to 4x the performance in next-generation games which heavily utilize ray tracing and AI rendering techniques. Previous generation games using traditional rasterization techniques will have a 1.5x to 1.7x performance improvement. These performance gains are significant on the surface, but they come with a large manufacturing cost increase which hampers product positioning and causes questionable marketing moves. Nvidia’s competitive positioning will be its weakest in a decade. Our estimated cost breakdown, shown later in the article, indicates Nvidia may have a cost disadvantage versus AMD’s RDNA 3. The first cost structure disadvantage in nearly a decade for team green.

As a reminder, our [Ada Lovelace specifications from April](https://semianalysis.substack.com/p/nvidia-ada-lovelace-leaked-specifications?s=w) are near identical to what Nvidia announced this week. Additionally, [our die size estimates from April were 1% of the actual AD102 and AD103 die size and within 2% for AD104](https://semianalysis.substack.com/p/nvidia-ada-lovelace-leaked-specifications?s=w). This leaves us quite comfortable with the rest of our report on the unreleased lineup.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3420c590-8d18-4d63-966d-e4701cefb734_1433x401.png)

These die sizes are not too large in isolation, but the figure alone is misleading when considering cost per wafer differences with Ampere’s Samsung 8nm, Ada Lovelace’s TSMC N4, and AMD’s RDNA 3 TSMC N5/N6 process technologies.

> “A 12-inch wafer is a lot more expensive today,” he replied, citing rising chip making costs. “Moore’s Law is dead … It’s completely over.” The executive added the expectations of twice the performance for similar cost was “a thing of the past” for the industry.
>
> Jensen Huang via [Barrons](https://www.barrons.com/articles/nvidia-graphic-card-prices-moores-law-51663778838?mod=hp_DAY_Theme_1_1)

SemiAnalysis sources indicate that the wafer cost of TSMC N5/N4 is more than 2.2x that of Samsung 8nm. With that wafer cost increase comes 2.7x higher transistor density. Nvidia’s top-end die went from 45 million transistors per millimeter squared (MTr/mm2) to 125 MTr/mm2. A fantastic density increase that is closer to 2 process node shrinks than 1 process node shrink. Jensen Huang is right that cost per transistor improvements have slowed significantly.

Due to high wafer costs, GPU die costs are up massively, but the die is only a portion of a GPU’s total bill of materials (BOM). The BOM of a GPU also includes memory, packaging, VRMs, cooling, and various other board-level costs. When moving from the previous generation 3090/3090ti (GA102) to the new 4090 (AD102), these board-level costs remain the same. As such, the MSRP increase from $1499 to $1599 is enough for Nvidia to maintain margins and deliver substantial gains in performance per dollar. The MSRP cannot be compared directly as the 3090ti GPU sells for $999, or even less, meaning performance per dollar in traditional rasterization rendering is flat.

More significant issues arise when we look further down the stack to the 379mm2 AD103 and 295mm2 AD104. This is where Nvidia faces the big crunch in costs. AD103 and AD104, alongside their accompanying packaging, memory, VRM, board, and cooler BOM, must sell in high-end GPUs for Nvidia to maintain margins. Nvidia generally stratifies various GPU dies into different GPU tiers. In the RTX 4000 generation, Nvidia faced a very tough decision. Rather than place the AD103 die in the 4080 series and the AD104 die in the 4070 series, Nvidia branded these different dies as the same GPU tier. This deceptive marketing places AD103 in the 4080 16GB and AD104 in the 4080 12GB. To be very clear, these are dramatically different GPUs. Nvidia should be shamed for this marketing decision, even if we believe they were forced to go this route due to manufacturing costs.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d10f3dea-6880-489b-a261-1d34c64ba85d_1075x391.png)

The community of enthusiast PC gamers has already stuck to calling the 4080 12GB the 4070, and some are even considering it as an xx60 class GPU. In the past, Nvidia’s GPUs with a 384-bit memory bus like the 4090 were considered halo tier, 256-bit bus high end, and 192-bit bus were mainstream xx60 GPUs. Bus width isn’t an end-all-be-all way of measuring a GPU tier; manufacturing cost and performance are. Regardless, it should be noted that the enthusiast PC gamer community is thinking negatively about Nvidia. The same could be said of the [recent EVGA drama](https://www.igorslab.de/en/evga-pulls-the-plug-with-loud-bang-yet-it-has-long-been-editorial/). EVGA exited the GPU business, and gamers blamed Nvidia rather than recognizing [that EVGA was a poorly run business](https://twitter.com/dylan522p/status/1570895166827024385?s=20&t=lYN0f4yvfmZOwzteBcBFKQ) with unsustainable margins, much lower than other Taiwanese firms such as Asus, MSI, and Gigabyte.

If you like what you’re reading, share it! Spread the word!

[Share](https://newsletter.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Gamers see the 4080 12GB as Nvidia insulting them. It is [roughly on par with the 3080ti](https://twitter.com/SkyJuice60/status/1572288601781866498?s=20&t=jeLtrm_Smo3TJnexQgTz3g) in traditional rasterization games, per Nvidia 1st party data. While Nvidia has BOM decreases gen on gen, the MSRP ignores current market conditions that gamers see. Nvidia’s 3000 series is overproduced. Nvidia and their partners have slashed prices on this class GPU. Nvidia has even taken a [considerable write-down of inventory](https://s22.q4cdn.com/364334381/files/doc_financials/2023/Q223/Q2FY23-CFO-Commentary-FINAL-with-update-for-web-post-include-tables.pdf). There is a lot of new and used RTX 3000 series inventory sitting out there, selling at very discounted prices. The $899 4080 12GB is priced similarly to 3000 series new GPUs and much more than the used cryptocurrency mining stock. We have even heard rumors that Nvidia delayed Ada Lovelace GPU production for 1 quarter to help digest the supply chain’s bloated inventory of GPUs.

The gaming GPU picture gets even more concerning for Nvidia when you factor in what AMD will announce on November 3rd. [Angstronomics posted exact details for AMD’s next-generation RDNA 3 architecture](https://www.angstronomics.com/p/amds-rdna-3-graphics). These details were independently confirmed by an AMD employee who said the packaging, die size, and architecture details were correct. We will ignore performance comparisons until independent 3rd party reviews come, but we want to help frame the cost disadvantage Nvidia has versus AMD’s Navi 31, Navi 32, and Navi 33. The figures in the table below are all relative to the 4080 12GB based on AD104.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bf202911-e5ce-4590-9261-f7dd1b136e72_1113x537.png)

While we did create dollar estimates, we want to avoid putting these dollar estimates in public as people will extrapolate those numbers to infinity and beyond. Die costs would have an additional high gross margin applied by Nvidia and AMD. Those marked-up dies will be assembled with memory and various board-level costs with an additional but smaller assembly and sales margin by firms like Asus. These figures do not account for those additional margins or the BOM for board-level costs such as VRMs and coolers, as there will be many variations of these GPUs from board partners. In general, those board-level costs will linearly increase with power levels, in which AMD is rumored to have an advantage in.

We calculated the die costs to account for parametric yields with a high percentage of die harvesting. We also used N6 and N5 wafer costs, which we obtained from a large TSMC customer. We assumed that AMD and Nvidia pay similar prices due to their volume ([Nvidia has had to prepay for more than $1B for these wafers](https://s22.q4cdn.com/364334381/files/doc_financials/2023/Q223/Q2FY23-CFO-Commentary-FINAL-with-update-for-web-post-include-tables.pdf) while AMD has not made significant prepayments to TSMC as a favored customer). Packaging and memory BOM was also calculated by speaking to sources within the industry.

In short, AMD saves a lot on die costs by forgoing AI and ray tracing fixed function accelerators and moving to smaller dies with advanced packaging. The advanced packaging cost is up significantly with AMD’s RDNA 3 N31 and N32 GPUs, but the [small fan-out RDL packages are still very cheap relative](https://semiengineering.com/fan-out-packaging-gets-competitive/) to wafer and yield costs. Ultimately, AMD’s increased packaging costs are dwarfed by the savings they get from disaggregating memory controllers/infinity cache, utilizing cheaper N6 instead of N5, and higher yields. Memory BOM utilizes the full memory bus width using single-sided 16Gb G6 or 16Gb G6x memory.

Nvidia likely has a worse cost structure in traditional rasterization gaming performance for the first time in nearly a decade. Nvidia is desperate to maintain margins, as shown by AD104’s 4080 12GB pricing and branding. They still have far too many GPUs in the channel. If Nvidia wants to maintain its market position, marketing and game partnership teams will need to emphasize areas where their GPUs perform better, such as ray tracing and AI-based rendering. We expect AMD to gain a decent market share in laptops with the N33 GPU and superior mobile APUs. On the desktop, the market share shift will depend on how many wafers AMD allocates to gaming GPUs versus Genoa and Bergamo Zen 4 server CPUs. We expect AMD to rise to ~~30% to 35%~~ *20% to 25%* market share on discrete desktop GPUs. AMD could raise its margins aggressively from historical levels to well above 50%. While Nvidia will still retain an advantage in ray tracing and AI-based rendering techniques, many gamers care more about the games they play today than where the industry is headed.

Edit 10/12/2022: After seeing 4090 official reviews and further sources for performance on RDNA 3, we reduced our market share estimate significantly. Sorry for jumping the gun.

[Share](https://newsletter.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

SemiAnalysis is a boutique semiconductor research and consulting firm specializing in the semiconductor supply chain from chemical inputs to fabs to design IP and strategy.

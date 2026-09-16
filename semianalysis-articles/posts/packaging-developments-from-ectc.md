---
title: "Packaging Developments From ECTC 2022"
subtitle: "TSMC CoWoS-R+, TSMC 4th Generation SoIC, Intel Collective Die To Wafer Hybrid Bonding, AMD V-Cache, Sony's Leading 1-Micron Pitch Hybrid Bonding, MediaTek Networking SoC, and Co-Packaged Optics"
date: 2022-06-08
source: https://newsletter.semianalysis.com/p/packaging-developments-from-ectc
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Packaging Developments From ECTC 2022

**TSMC CoWoS-R+, TSMC 4th Generation SoIC, Intel Collective Die To Wafer Hybrid Bonding, AMD V-Cache, Sony's Leading 1-Micron Pitch Hybrid Bonding, MediaTek Networking SoC, and Co-Packaged Optics**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

ECTC is the premiere conference about advanced packaging, so some of our favorite topics in the advanced packaging world such as hybrid bonding, co-packaged optics, and more are being discussed. There are also some deals and supply chain details that we can also exclusively detail related to these topics. We had the chance to attend the 2022 IEEE 72nd Electronic Components and Technology Conference virtually this year. This conference was in person, but unfortunately missed out on those awesome organic discussions. We will definitely be going next year though! Despite this, there was still quite a bit of interesting news, announcements, and technology developments coming from this conference that we want to summarize.

The highlights that we will discuss include TSMC’s CoWoS-R+, TSMC’s 4th Generation SoIC (3-micron pitch Hybrid Bonding), Intel and CEA-LETI Self Aligning Collective Die to Wafer Hybrid Bonding, Samsung’s research on monolithic vs MCM vs 2.5D vs 3D including Hybrid Bonding, SK Hynix Wafer-on-Wafer Hybrid Bonding which will be commercialized in DRAM, ASE’s Co-Packaged Optics Advanced Packaging, Cisco Co-Packaged Optics, Xperi Die Handling For Ultra-thin Dies, Tokyo Electron Wafer-on-Wafer Hybrid Bonding Wafer Handling, Sony 1-micron Hybrid Bond, AMD V-Cache Hybrid Bonding on Zen 3, and MediaTek InFO-oS Networking SOC Reliability.

# **TSMC’s CoWoS-R+**

As we discussed in our [advanced packaging primer series](https://semianalysis.substack.com/p/advanced-packaging-part-2-review), CoWoS is a chip last packaging technology. CoWoS generally has been done by placing active silicon dies on top of a passive silicon interposers, but this is quite expensive. As such, TSMC developed CoWoS-R which uses an organic substrate with RDL layers, a cheaper technology. CoWoS-R has not yet arrived in public shipping products, but there are some products coming. The first such product we know of is coming from AMD and will be discussed in the subscriber only section, including its system architecture. It’s frankly amazing.

TSMC isn’t stopping with CoWoS R, and CoWoS-R+ evolves on this technology.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3a0679a0-acfc-4788-af21-77b898671453_1023x392.png)

One of the key concepts to understand is the distance of a die-to-die connection. HBM is currently the only way to increase memory bandwidth to a reasonable level for AI and high-performance computing. Advancements on that front have risen rapidly with the original HBM coming in at 1Gbps per pad while that has rapidly grown to 2.4Gbps with HBM2 and 3.2Gbps with the HBM2E generation. HBM3 is going all the way to 6.4Gbps. The package width has also grown from 7.8mm with HBM2 to 10mm with HBM2E to 11mm, meaning the interconnection length is now growing to about 5.5.

To put it simply, the wires need to carry much faster data rates while also going a longer distance. This is incredibly difficult to do and can create a lot of noise which reduces the signal integrity. Another issue is that chips are exploding in power as the slowdown of Moore’s law is battling with increasing performance demands. Nvidia’s Hopper already has 700W, but in the future packages will balloon into the kilowatt range. HBM3 is more power hungry than HBM2E aswell. More power going through a package also potentially creates more noise which can degrade signal integrity. TSMC has developed a new high density IPD to combat this. In short, TSMC customers can do 6.4Gbps HBM3 on CoWoS R+, but not on CoWoS R. The high density IPDs are important for adding additional capacitance which smooths out power delivery. Graphcore for example was able to increase clocks by 40% without jumping up power by simply using TSMC´s SoIC Hybrid Bonding to add a crapload of capacitors, [which we detailed here.](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a4717ebd-1bab-41a4-838c-95e208f0ec6b_1024x718.png)

TSMC also shared more developments on embedded bridge die capabilities. The interconnect between that bridge and the top active die can go down to 24-micron. TSMC can now do 3x reticle limit which matches what CoWoS-S (full passive silicon interposer). In the future, they have a roadmap go up to 45x the reticle size meaning complex chips using a chip last process can be used for wafer scale packages. Meanwhile CoWoS-S is only being extended to 4x next year.

# **TSMC’s 4th Generation SoIC 3-Micron Pitch Hybrid Bonding**

TSMC presented research on their 4th generation of hybrid bonding technology which can achieve 100,000 bond pads per mm2. It’s great to see tangible progress on something so far into the future given only AMD and TSMC have shipped a single SoIC device. That device was significantly relaxed at 17-micron versus the 9-micron that the 1st generation SoIC is capable of.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1b5209a9-11f9-4c17-a7af-989f4280258f_1024x340.png)

The process is mostly the same for TSMC’s hybrid bond. They start with completed wafers, form a new layer for bond pads, etch it down, deposit a seed layer, electroplate. Next, they thin and dice the top die wafers. Special care is given to keep them clean. A plasma activation is done, and the dies are bonded.

The TSMC paper showcased yields for SoIC which was quite interesting. This was using daisy chain test structures on test dies that measured in at 6mm by 6mm, which is conveniently the same die dimensions as AMD’s VCache. One of the slowest steps in chip on wafer hybrid bonding is when a BESI tool physically picks up the die and places it on the bottom wafer. This bond step suffers heavily from accuracy, and throughput versus accuracy is a very big battle. TSMC, with a 3-micron TSV pitch, showcased yields do not differ and resistance did not meaningfully change at less than 0.5-micron misalignment, with 98% bond yield. From 0.5-micron to 1-micron, their structure did yield, but there was a sharp increase in resistance for the last 10% of their daisy chain structure. With greater than 1-micron pitch, their yield was 60% and all measured structures exceeded their specifications for resistance. 0.5-micron is a very important level as that is BESI’s claimed accuracy on their 8800 Ultra tool is <200nm, although we have heard it is more like 0.5-micron with a wide variance even with throughput at half the tool’s rated spec.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3a0b07eb-ad66-4fd6-a2b6-711122e2ca2e_1024x650.png)

TSMC also showcased that contact resistance was better across the stack due to their thinner barrier layer. In addition, TSMC believes SoIC is more reliable. This includes with a wider range of operating temperatures. Many were disappointed when AMD locked down overclocking and modifying power entirely on their 5800X3D desktop chips. This is likely only a hiccup with the 1st generation. As TSMC’s Cu alloy is modified and the pitches decrease with SoIC gen 4, it seems they are improving their reliability and yields.

# **Intel and CEA-LETI Collective Die to Wafer Hybrid Bonding**

While we will dive more deeply into die on wafer vs wafer on wafer vs collective die on wafer bonding in our advanced packaging series, including tools ecosystems, wins, and TCO, a bit of a short explanation here. Die on wafer is much less accurate than wafer on wafer bonding. It is also much slower. For example, despite Besi’s claims of 2,000 dies placed per hour, to reach even 1-micron accuracy, the throughput drops below 1,000 dies placed per hour. Wafer on wafer bonding on the other hand also has many issues related to not being able to do heterogenous integration and not being able to bin/test dies before the bond step. Collective die to wafer allows higher accuracy and throughput than die to wafer bonding, while also offering the ability to test, bin, and achieve heterogenous integration.

Intel and CEA-LETI combined collective die to wafer with a self-alignment technique which achieved 150nm of mean misalignment (much more accurate than die to wafer) and with higher throughput. The self-alignment technique is very cool. They used the capillary force of water droplets to make alignment more accurate after a modified pick and place tool places it quickly, less accurately, in the required location. As the water evaporates, the direct bond is created, without any other intermediate materials. The bonded wafer then moves onto a standard annealing step which strengthens the bonds.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c870bdc1-4aca-42a1-8d52-682fb32ec1b7_820x1024.png)

The only unique step besides the water droplet deposition involves applying a hydrophilic and hydrophobic material at the bonding sites, which can be lithographically defined with nanometer overlay precision. This wasn’t a problem free process. There were many issues related to dispensing the water, the droplet characteristics, condensation, and bonding process. Intel and CEA-LETI presented the results with 3 metrics. Collection Yield refers to the water droplet being caught on the die. Bonding yield refers to the number of dies successfully bonded. Alignment yield refers to the number of dies with sub-micron precision.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/118fd751-ba3c-466d-a1c9-2cfe3601d5a8_1024x1006.png)

They tried a matrix of various processes, with the best achieving 98% yield on the bond and 100% on other steps. The total alignment accuracy is nothing short of amazing, with all dies less than 1-micron alignment accuracy and most with below 0.2-micron alignment accuracy. Intel and CEA-LETI attempted this with multiple different die dimensions and this process really shined with very tall aspect ratio dies which was very interesting.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2b99cacc-fba8-40ea-a45d-bffe86677943_1024x620.png)

# **Samsung Monolithic vs MCM vs 2.5D vs 3D including Hybrid Bonding**

Samsung presented really interesting research on the cost of advanced packaging on an area and power front. They compared two major design types, something that is bandwidth constrained (HPC/AI) and something that is latency constrained (CPU).

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d1900a01-abf5-4338-ae95-617f7927365b_1023x521.png)

The monolithic 2D chip for the HPC and AI comparison was 450mm2. It was sliced up and used advanced packaging to glue it back together. The MCM variant had a 2.1% increase in power consumption and a 5.6% increase in die area. The 2.5D design has a 1.1% increase in power and a 2.4% increase in area. The 3D design had a 0.04% increase in power, but a 2.4% increase in area. These results of course are ideal and in the real world there will be more overhead related to floorplan and layout concerns.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/79258b4a-d93c-4146-9916-a463c190856a_1024x541.png)

# **SK Hynix Wafer On Wafer Hybrid Bonding DRAM**

SK Hynix presented research on their wafer on wafer hybrid bonding process. Wafer on wafer bonding technology for advanced packaging is already very common. It is used in CMOS image sensors by Sony, Samsung, and Omnivison. It is used by YMTC in NAND Flash with their [XStacking technology](https://semianalysis.substack.com/p/the-impending-chinese-nand-apocalypse-e01). It is also used by [Graphcore and TSMC in their BOW chip](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w). We exclusively told you that SKHynix would be using [hybrid bonding in their 16-layer HBM](https://semianalysis.substack.com/p/advanced-packaging-part-2-review) stacks. SKHynix did not directly state the yields, but they seemed very hopeful on commercializing this technology.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1709c09f-aa0c-4841-bda2-c8d97f2bc7a9_805x1024.png)

# **ASE Co-packaged Optics**

What ASE presented wasn’t that groundbreaking from a technology perspective, but the implications for investors are. This is because in the past, the major OSAT’s have stayed away from optical networking products. In our opinion, this research isn’t good for a company like Fabrinet which we do generally like. With that said, it is only research, and movements in the market are more important. Regardless, if ASE is researching this, they likely will be trying to gain share aswell. Now on to what ASE presented.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5e5f479c-481f-4b29-b6a2-69ba3b707b66_1024x917.png)

Wirebonding has been the main technology for the 100G generation, but it begins to bottleneck as we transition to 400G and 800G generations. This is a transition that other firms have been making for a while, for example Intel and Fabrinet have stopped wirebonding the PIC and EIC with the most recent generations. Cisco also has moved beyond wirebonding to flipchip, and this year they even presented 3D assembly with TSVs, something far more advanced than what ASE showed. We will talk about Cisco and their partners for manufacturing in the subscriber only section.

The ASE paper in general talks through the unique challenges of optical manufacturing including the differences in contamination processes and unique dicing and etching technologies used. Post fab wafer processes are also different such as under bump metallization and silicon etc. Unique testing requirements were also discussed. It will be a long way for ASE to get into optical manufacturing, but it is important to keep watching them as a potentially very competent and scary new entrant into the optical assembly and packaging field for telecommunications and datacenter markets.

# **Xperi Die Handling For Ultra-thin Dies**

In most hybrid bonding the die must be extremely thin. In the case of upcoming 16 layer HBM, this can even be on the order of 30-micron which is less than half the thickness of a human hair. The silicon die is incredibly fragile and so it cannot be lifted normally. As such, Xperi presented research on lifting the die with a Bernoulli grip which uses a high velocity airflow with low static pressure to adhere to an object without physical contact. The gripper then places the die onto another die with 1 micron or less precision. The paper had a lot of details about die warpage and handling. There’s nothing ground-breaking here, but we just thought this was a cool mechanism for handling super thin dies.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8d3fcd58-827b-4cd5-aa0f-821e61cdb5d6_1024x583.png)

# **Tokyo Electron Wafer on Wafer Hybrid Bonding**

We exclusively told our subscribers about a [major win they had at the worlds largest foundry](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w) for their wafer-on-wafer hybrid bonding tool and the process flow. While we don’t know if this research will ever be commercialized, we thought it was another interesting wafer handling technique. The wafer is so thin that it’s floppy and as you lower it to bond, there can be trapped air which impacts yields. Tokyo Electron presented a method for avoiding this. This is research, and not the process for their current bonding tools.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/59847526-f9f2-4308-b7d0-1dc57b5f0f94_1024x592.png)

# **Sony's Leading 1-Micron Pitch Hybrid Bonding**

Sony continued to demonstrate why they are the leader in hybrid bonding. They first shipped the technology in high volume products in 2017. They currently ship millions of units a year of CMOS image sensors with 6.3-micron pitch hybrid bond with 3 dies stacked while others do far less dense pitches and with less volume. Sony’s volumes are entirely wafer-on-wafer hybrid bonding. This year Sony presented 1-micron pitch face-to-face hybrid bonding and 1.4-micron face-to-back hybrid bonding. Sony currently utilizes both face-to-face and face-to-back hybrid bonding.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7d23785d-e96c-48f0-a1db-d65c31f35552_842x1024.png)

The short-winded explanation for why Sony is so aggressive on hybrid bonding is that Sony wants to continue to disaggregate and stack functions of the image sensor pixel to capture more light and to be able to capture more of that data and turn it into actual photos and videos.

The technology they presented was quite interesting. All hybrid bonding processes require extremely flat surfaces, but copper and SiO2 get polished away at different rates in the CMP process. With most processes, that means the copper gets grinded away to a lower level than the SiO2. This is commonly called dishing. This process must be precisely controlled as the coefficient of thermal expansion is also differs between SiO2 and copper. A technique TSMC utilized is by using a copper alloy instead of pure copper to control the level of dishing and make the CMP process easier to do.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2108d4a1-12d3-4879-b7ec-1bd179f2c683_771x1024.png)

Sony, as they shrink to much smaller pitches than the rest of the industry, has come up with the opposite strategy. The SiO2 is polished away further down than the copper in their advanced approach. This required a completely different proprietary CMP process.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c793cb56-dbdc-48c2-93ec-35b5a3658cf8_1024x729.png)

Sony also achieved similar control and protrusion of the copper by varying the grain size in their ECD process. Through our sources, we can exclusively detail whose tools they utilized in this process in the subscriber only section.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1ea398b2-5c82-4fdc-bad1-9e7f3cbd4b79_1024x717.png)

The results from this are incredible. Multiple orders of magnitude improvement in contact resistance versus a conventional process. This is tested on 200,000 daisy chained Cu-Cu connections. These were the results for the 1-micron face-to-face bond, but the 1.4-micron face-to-back showed impressive results as well.

# **AMD V-Cache SoIC Hybrid Bonding on Zen 3**

AMD reiterated a lot of things but there were a few new things. Also, this is where we will plug our twitter and mention that we noticed [that AMD’s lead engineer on V-Cache hybrid bonding and elevated fan out bridge left AMD for Microsoft](https://twitter.com/dylan522p/status/1534355166656331776?s=20&t=1GOKy6AESdJp7gUTNRSGcQ). We are excited for the future of Microsoft's silicon as they have been hiring a ton of talent from all over the industry.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ee96e2b0-b6cd-443f-8f93-8abc7cda2686_1794x1821.png)

The physical structure is quite interesting on v-cache. Rather than only being the CPU CCD chiplet with the SRAM chiplet and support chiplets on top, AMD and TSMC also have a final, 5th piece of support silicon on top of of the entire assembly. This structure was independently confirmed by [Tom Wassick of IBM](https://www.linkedin.com/in/tom-wassick-95992220/). At first it may seem like a waste of extra silicon, but this is done because TSMC’s hybrid bonding process requires thinned dies. This final piece of support silicon is needed to give the final die assembly rigidity and equivilant height to the standard CCD which has no hybrid bonded SRAM.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8a6bca0c-1e79-4a81-8648-80649c5f3554_1024x468.png)

AMD compared 9-micron pitch hybrid bonding to a 36-micron pitch micro bump 3D architecture. AMD is referring to the Foveros that will be used on Ponte Vecchio GPUs and Meteor Lake CPUs. AMD claims 3x interconnect energy efficiency, 16x higher interconnect density, and better signal/power integrity due to lower TSV and contact capacitance/inductance. Oddly, they use 9-micron pitch as the comparison. This is a bit of a disingenuous comparison as the production version of V-Cache was found to be done on a 17-micron pitch [by TechInsights](https://www.linkedin.com/posts/yuzo-fukuzaki-12408111_3dv-ryzen-amd-activity-6828725467298828288-X9U-/). This relax in pitch would would reduce some of the advantages presented.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/81b19c6a-8ff7-4234-b585-44042d1c16df_1024x635.png)

This chart was interesting albeit very generalized. Zen 3 has 32MB of L3 Cache, and V-Cache adds another 64MB per chiplet. Currently only 1 chiplet is stacked, which leads to a wide range of IPC increases. I wonder what simulation and benchmarking AMD used to get this IPC % Uplift figure from. AMD also showed some data related to reliability, which showed there were no concerns there at normal voltages.

# **MediaTek Networking SOC Reliability**

MediaTek presented a paper titled “Reliability Challenges of High-Density Fan-out Packaging for High-Performance Computing Applications.” What wasn’t said is that this was for a real chip that MediaTek is selling via their custom ASIC division for networking applications in China.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/aa808104-6ef8-4e0f-9d7b-451e409ee81c_941x1024.png)

MediaTek also didn’t directly state it, but we know they used TSMC’s InFO-oS technology. The paper discussed temps, warpage, and other reliability concerns, but the interesting thing was them publicizing this chip.

In the subscriber only section, we will mention who Cisco is working with on co-packaged optics, who Sony is using in parts of their Hybrid Bonding process, and the discussion about the AMD chip which will use CoWoS-R.

[Share](https://newsletter.semianalysis.com/p/packaging-developments-from-ectc?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

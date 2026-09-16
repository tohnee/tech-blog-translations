---
title: "Lam Research, Tokyo Electron, JSR Battle It Out In The $5B+ EUV Photoresist, Coater, and Developer Market - CAR vs MOR vs Dry Resist"
date: 2021-11-18
source: https://newsletter.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Lam Research, Tokyo Electron, JSR Battle It Out In The $5B+ EUV Photoresist, Coater, and Developer Market - CAR vs MOR vs Dry Resist

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

EUV lithography has fundamentally shifted the semiconductor industry forward by giving a step function increase of fidelity in the resolution of photolithography patterning. The increase in resolution hasn’t come for free. Many accompanying advancements have also had to come as a cost to transitioning to EUV. These changes range from mask production, pellicles, deposition, etchers, hard masks, and photoresist. While EUV itself is dominated by ASML, the shift has created a high stakes multi-billion-dollar battle for adjacent steps in the manufacturing process – particularly the photoresist industry.

Japan has long since reigned supreme in this field with Tokyo Electron (TOELY / 8035.JP) having 100% share of EUV photoresist coaters and developers. This market and associated wins in etch and clean due to monopoly status in coaters/developers are **currently at a $5B annual run rate in revenue**! In addition, other Japanese firms have long since cornered the photoresist market with about 75% market share. JSR (4185.JP) and Tokyo Ohka Kogyo (4186.JP) are the leaders. They ship the overwhelming majority of chemically amplified photoresist specialized for EUV. However, these markets are under attack by Lam Research.

This article will consist of a free nitty-gritty technology explanation, but there will be a paywalled conclusion that will be of interest for investors and curious minds.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c68dbba2-a33a-487e-b97e-886f26a0609f_907x1024.png)

Before diving into the specifics of the upcoming photoresist war, let’s do a simple overview of the lithography patterning process. It all starts with cleaning the wafer to ensure there are no foreign bodies such as tiny molecules of dust or leftover chemicals from previous processes. In more advanced nodes, there will be a few underlayers, intermediate layers, and hard mask deposited onto the wafer before the photo lithography process. This deposition is done so the final etch can be more accurately controlled, and is a topic for another day

The most simple form of lithography will be called single patterning with wet photoresist. The cleaned wafer is put into a Tokyo Electron coater and developer. The tool deposits **chemically amplified resist (CAR)** on top of the wafer. The CAR is suspended in a liquid solution and the wafer is spun around extremely fast to coat the wafer. The spinning process also removes most of the liquid via the centrifugal force and this leaves a thin layer photoresist. A process called the prebake is also done in order to dry up the last bit of liquid and in some cases chemically prep the photoresist for the upcoming reaction.

The wafer goes to an ASML photolithography tool which then shines light through a mask and onto the photoresist where it causes a chemical reaction. The wafer is shuffled back into the Tokyo Electron coater/developer tool. The developer washes away photoresist. If this photoresist is positive, then the photoresist that was exposed will react and become solvent so it can be washed away. If it is negative, the photoresist that was exposed reacts to no longer be solvent and the unexposed the photoresist is washed away. This just applies to the photolithography process, other related process such as multi-patterning techniques, etch, and spacers, exist beyond this, but let’s focus on the lithography process for today.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/344aa06d-99d0-4d01-9af8-38d9ba33592e_1024x578.png)

The photoresist process outlined above has worked fantastically for decades, but it is beginning to run into major issues. These are related to line edge roughness, sensitivity, resolution, and throughput. EUV lithography bombards the wafer with an extremely short wavelength of light relative to DUV. The shorter wavelength extreme ultra-violet light comes at the cost of being much more difficult to generate.

[EUV has a throughput problem](https://semianalysis.substack.com/p/asmls-euv-tools-have-a-throughput). This problem centers around the fact that 1/14th the number of photons hit the wafer relative to DUV at the same dosage. As such, dosages in EUV must be increased which in turn reduces throughput by increasing exposure time. The throughput problem causes wafer output to be limited heavily and costs to increase. In order to maximize throughput, dosages are minimized, and this leads to a variety of issues related to feature fidelity.

One solution is to use more machines and crack up source power. Machines are extremely expensive at ~$150M a piece, and ASML’s output is highly limited. Increasing source power is an incredibly difficult and ASML’s roadmap for power increases is nowhere close to the rate at which EUV layers are ramping on the new nodes.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

In addition to having less photons expose the photoresist, the EUV photoresist also absorbs less of them. The photoresist solution is an incredibly precise mixture of photo-acid generators, adhesion promoters, and stability agents. Getting it wrong is a costly mistake. [In 2019, TSMC’s Fab 14B had an issue with their photoresist, and it hit TSMC in the pocketbook for $550M.](https://www.anandtech.com/show/13975/tsmcs-fab-14b-photoresist-material-incident-550-million-in-lost-revenue) With EUV photoresist, this balancing act is even more controlled, and the specific mixture leads to less absorption. The combination of demand for EUV and of 1-2 punch of less photons and less absorption makes for a ripe opportunity for the classical photoresist industry to be disrupted. Enter dry resist and Lam Research.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6e3607cb-ff96-4da3-ad1e-f3869fcc8f02_1024x578.png)

Lam Research is attempting to disrupt the whole stack. Instead of a wet photoresist technology using a spin coater, they will use a chemical vapor deposition process to layer on a metal photoresist. Lam Research claims that the dry resist technology has several advantages over wet resist. Due to being a densely deposited metal, it isn’t mixed with as many other chemicals. This allows the metal photoresist to be only absorbers. Coming back to throughput, this means there is a 2x reduction per wafer pass and power. A near doubling in per EUV tool throughput would massively reduce costs.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/659552d8-3919-46a2-9fb0-291519453a3a_1024x575.png)

Sensitivity isn’t the only advantage. Lam’s dry resist is also developed with a dry method. In wet develop, photoresist is washed with a water or acid. Lines and other features that were patterned can collapse as the resist is dissolved away due to capillary forces. This has increasingly become an issue as the minimum metal pitch (MMP) scales beyond 28nm. TSMC’s N5 and N4 process nodes have an MMP of 30nm and 28nm respectively, so current shipping nodes are right up against the edge.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4ea78682-0267-4a2f-870a-c85f2a5091bd_1024x576.png)

However, Tokyo Electron still has innovation in the pipeline. While they agree the existing development rinse process does cause line collapse beyond 28nm pitch (14nm critical dimension), they have found a new solvent rinse process that can scale to ~24nm (12nm critical dimension). This will allow scaling of wet resist methodologies to 24nm.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/db7aa1a6-481c-4dde-832f-b609614ce163_1024x574.png)

But not all is solved issue with wet resist as it is very difficult to wash all the photoresist out. If all the photoresist isn’t washed out, future steps will have issues. Residual photoresist can cause holes when etched to end up “kissing” each other. The residue can also cause these holes to be missing entirely. Tokyo Electron’s current solution for this is to simply etch the residual photoresist. While this is a simple solution, there could be complications as it causes the holes to be bigger or beveled. The beveled effect isn’t necessarily negative, but it also isn’t optimal in all use cases.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a17f678a-7639-4552-bbe3-973e9774776a_1024x575.png)

Lam Research is claiming their process does the existing 32nm pitches used on 5nm nodes with much lower variability and better latitude versus the existing wet photoresist process. The hard numbers Lam Research shares can’t be argued with. When a fab is chasing feature size, performance, and power, the dry process is better overall. The comparison that Lam Research makes can be considered disingenuous due to showing current deployed tools and processes versus upcoming ones.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dfadb23c-f4f5-4f52-8019-a83d0bf6a2e2_1024x574.png)

Meanwhile, Tokyo Electron is trying their hardest to extend the life of the existing install base. The Clean Track Lithius Pro Z is used alongside every ASML EUV machine. It’s proven to be reliable and productive for the initial EUV nodes, but as the industry pushes beyond single patterning EUV, chemically amplified resist (CAR) is clearly hitting the limits. Everything else being equal, dry resist would win on the leading-edge and smallest feature sizes.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/02d576cf-c66f-40c6-ab6c-38d45b9d4495_1024x571.png)

Lam Research was initially targeting usage on 5nm IMEC node (3nm for foundries). They are engaged with IMEC and ASML on developing this technology further. Lam is also engaged with Samsung, Intel, TSMC, and SKHynix on commercialization of this technology for logic nodes and DRAM nodes. It’s clearly promising, and SemiAnalysis channel checks show there is a lot of interest.

The Tokyo Electron and the photoresist incumbents are not sitting with their hands up waiting to be disrupted. **This is where Inpria comes in. They have developed a new type of photoresist, metal oxide resist (MOR).** Inpria was born out of Oregon State University Research Center in 2007. Inpria has since received major investments from Samsung, Intel, Applied Materials, TSMC, SKHynix, JSR, and TOK.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5d42b95a-2591-4aa8-abad-9664c946a155_1024x571.png)

Inpria’s investors are titans of the industry. It includes all 4 of the companies that are working with Lam Research on commercializing dry resist. The list also includes both previously mentioned leaders in CAR photoresist, JSR and TOK. JSR participated in funding rounds for Inpria in 2017 and 2020, and recently they bit the bullet and purchased the firm outright for $514M. This valued the firm at $742M. That’s a damn impressive valuation for an industrials firm that develops chemicals on a pre-revenue basis.

It’s very obvious the firm has IP worth a lot of money. JSR management tends to be quite conservative, so it speaks volumes about the disruption that is occurring. The photoresist industry has collaborated with Tokyo Electron for decades, and JSR/Inpria are continuing this tightly knit partnership. They are working together on the development of the photoresist, process, and coaters/developers. Commercialization is coming on the next process node.

MOR still uses similar steps as the current photolithography process. It is spun onto a wafer by being suspended in a solution. The same Tokyo Electron Clean Track Lithius Pro Z can be used with an upgrade. That upgrade isn’t capital intensive and can use either CAR or MOR photoresist.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9a01c013-18bf-4040-9b95-e3d8369fc007_1024x574.png)

MOR is still wet, which means certain issues will remain, namely the selectivity of deposition. Potential uneven deposition of photoresist on the wafer can cause issues with the exposure and bake process steps. One of the biggest advantages of Lam Research’s dry resist technology is the use of a chemical vapor deposition (CVD) process for deposition of photoresist, which allows much finer control over the variability and thickness of photoresist.

Getting the right thickness is incredibly important on photoresist. If there is an extremely thin layer, the lithography tools have higher performance and throughput because less photoresist is needs to be exposed. On the other hand, the thin resist film can be damaged when etching (negative photoresist). Not only does a thick photoresist layer lead to lower throughput, it also can cause pattern collapse and for residual photo resist to remain in holes after development.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

Tokyo Electron and JSR claim that they have a new post exposure bake process for metal oxide resist that would help increase sensitivity of photoresist. This means fabs can substantially decrease the dosage required from the EUV machine and thereby increasing throughput. Tokyo Electron claims a 38% reduction in dosage, vs the 50% reduction that Lam Research claims for dry resist. Tokyo Electron also claims the new post exposure bake allows extremely uniform resist thickness and low metal contamination. If these claims pan out, then this can extend the wet photoresist lifetime.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a8ea2546-0b7d-49c9-9c72-fe6b6dbf2918_1024x577.png)

In the same vein, Tokyo Electron and JSR have a new wet development process which resists the pillar collapse problem. 36nm pillars often collapse and this is one of the biggest challenges with capacitor scaling in DRAM. The new develop process also works with lower EUV dosage and it decreases thickness variation for final features.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0ed0b6f0-1188-4941-87b2-e584ceb3b749_1024x574.png)

With MOR, Tokyo Electron is working to optimize the entire process flow from coating, baking, development, all the way to etch. They claim they have achieved a defect density of 0.1 defects per square centimeter. Sounds fantastic, but that defect density means 70.6 defects per 300mm wafer. The lithography process is done over 70 times on a leading-edge wafer and the N3 process will do over 20 EUV immersions per wafer. These defects really start to stack up and destroy yield. MOR still has some hurdles to overcome.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/05a121db-b4dc-4673-ae18-0b8ccfba6b94_1024x578.png)

The idea of optimizing process flows is not an entirely novel one. Process module optimization is something Applied Materials has done for quite some time with their entire interconnect process flow and tool offerings. It has allowed Tokyo Electron to gain share in etch and clean due to their dominance in photoresist coaters/developers. Lam Research likewise wants to penetrate the lithography stack by offering technologies from hard mask through photoresist deposition and development all the way to etching. The multi-step process optimization allows for less line edge roughness, more uniformity, less defects, and higher reliability in end user chips and processes.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ad62cc53-6415-4080-a53c-253014bdcb0b_1023x541.png)

The dry process has significantly lower usage of chemicals. This applies especially to the spin on resist and development. The photoresist does not need to be suspended in a solution to be deposited, and there is no spin off waste like the wet process. The development process doesn’t require rinsing the wafer with a huge amount of acid or ultra-pure water to dissolve the photoresist off the wafer. This in turn halves the amount of power required.

It’s yet to be seen who wins in this battle, there are benefits for MOR and dry resist. SemiAnalysis has more data points that make this battle clearer in terms of outcome. Most importantly, what are the financial implications?

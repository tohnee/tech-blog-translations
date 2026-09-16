---
title: "2025 AI Diffusion Export Controls - Microsoft Regulatory Capture, Oracle Tears, Impacts Quantified, Model Restrictions"
subtitle: "Malaysia's Stranded Capacity, Western Hyperscale Strength, AI Accelerator Restrictions, India Brazil Middle East Concerns, Sovereign AI Killed, VEU Restrictions and Implications, Compute Budget, Open-Source Creating Lower Bound, Model-Weights Controlled"
date: 2025-01-15
source: https://newsletter.semianalysis.com/p/2025-ai-diffusion-export-controls-microsoft-regulatory-capture-oracle-tears
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Myron Xie", "AJ", "Jeremie Eliahou Ontiveros", "Reyk Knuhtsen", "Ivan Chiam"]
tags: []
audience: only_paid
paywalled: true
---

# 2025 AI Diffusion Export Controls - Microsoft Regulatory Capture, Oracle Tears, Impacts Quantified, Model Restrictions

**Malaysia's Stranded Capacity, Western Hyperscale Strength, AI Accelerator Restrictions, India Brazil Middle East Concerns, Sovereign AI Killed, VEU Restrictions and Implications, Compute Budget, Open-Source Creating Lower Bound, Model-Weights Controlled**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

The US government lobbed the largest salvo in the new technology cold war with its new [Framework for Artificial Intelligence Diffusion](https://public-inspection.federalregister.gov/2025-00636.pdf). These new export restrictions are completely unprecedented in scope and scale, with many calling the efforts overzealous or misguided. The regulation at its core is targeted at preventing China from accessing AI compute to build frontier models.

The prevailing rationale within the US government is that AI progress has become so rapid, that access to compute to build and improve these models over the next few years will decide the fate of the next global order for decades to come. In short, the government believes that AI with determine whether US hegemony persists or if it is ceded to China. If so, the AI regulations are justified, but if AI takes longer to make any meaningful impact on the world economy, then these regulations are shortsighted and will harm American competitiveness in the long term.

While the [semiconductor controls still have some loopholes](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/), the AI chip controls were much more Swiss Cheese. Up until now, while China has been limited from accessing AI compute, that has only been on paper, and it has been circumvented through several methods. In reality, restricted Nvidia GPUs were [simply re-exported by bad actors to China](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/) from unrestricted countries with a meaningful number of H100s available on various clouds and marketplaces in China. Additionally, [over a million China specific accelerators](https://semianalysis.com/accelerator-industry-model/) that skirt the line on current regulations have been legally shipped such as the Nvidia [H20](https://semianalysis.com/accelerator-industry-model/), [B20](https://semianalysis.com/accelerator-industry-model/), AMD [MI308X](https://semianalysis.com/accelerator-industry-model/), and Intel Gaudi [HL-328](https://semianalysis.com/accelerator-industry-model/) + [HL-388](https://semianalysis.com/accelerator-industry-model/).

Chinese firms such as ByteDance have had unfettered access to GPUs outside their borders through various cloud companies. Furthermore, in just Malaysia alone, based on our individual datacenter by datacenter tracking, there is ~3 Gigawatts of Critical IT capacity of datacenters being built in just a few years. This represents as much capacity as Meta had globally for serving all their traffic in the beginning of 2024. The only use case for such an enormous amount of concentrated datacenter capacity is AI.

![](https://substack-post-media.s3.amazonaws.com/public/images/27fbd785-e444-48df-bab4-0d69853dafd3_1242x714.jpeg)
*Source: SemiAnalysis Datacenter Model*

[Our data](https://www.semianalysis.com/p/datacenter-model) shows a similar story playing out in the [Middle East, India, and Brazil](https://www.semianalysis.com/p/datacenter-model) as well. The US Government is cognizant of this and therefore believes regulating this is the upmost priority.

There are a huge number of negative externalities within the rules that will greatly impact the supply chain, geopolitics, and where AI gets built. For many firms this ruling is quite negative, for some select others it is positive. The regulations are very complicated and the team at SemiAnalysis has worked around the clock to break down the rules and quantify the impacts. We will deeply dive into them below, but first an Executive Summary on the restrictions and what the major ramifications are.

## **Executive Summary + High Level Takeaways**

On January 13, the Bureau of Industry and Security with its [Framework for Artificial Intelligence Diffusion](https://public-inspection.federalregister.gov/2025-00636.pdf) has narrowed these loopholes that are being exploited by entrepreneurial business units and bad actors, while arguably streamlining access to chips for deployment overseas by trusted nations as well as for a small number of trusted US Hyperscalers (Microsoft, Google, Amazon) and approved overseas providers.

To accomplish this, the AI Diffusion Framework divides the world into three tiers of countries with varying levels of access to AI Chips and strict caps for purchasing of GPUs:

- Tier 1 for the US and 18 major allies and security partners,
- Tier 3 for 23 Arms Embargoed Nations plus Macau,
- Tier 2 for all other countries – with varying degrees of relations with the US: ranging from Singapore who gets to buy F35s to Yemen who bombs US tankers!

![](https://substack-post-media.s3.amazonaws.com/public/images/18d031aa-58a9-47b2-97dd-5da285eac9ec_1503x1141.png)
*Source: SemiAnalysis, BIS*

It establishes a Validated End User (VEU) framework that identifies the entities and companies, mainly these US Hyperscalers, that can import AI chips into each country tier, as well as a few other exceptions for non VEUs.

Lastly, it introduces exports controls for AI Models themselves, applying restrictions globally on entities not from Tier 1 countries training AI Models that require a large quantity of training compute (currently set at 1e26 Training FLOPS which is 2x that of Llama 405B, but pegged to the training FLOPS for the largest open-weights model), and prohibits the export of closed-weight models beyond this same size.

The framework is unabashedly nationalistic, and it is clear from the spirit and the letter of the rule that it is designed to significantly advantage Google, Microsoft, and Amazon versus foreign providers as well as Neoclouds from Tier 2 countries. It reshuffles the deck with respect to individual nations’ access to AI compute, and it puts at risk the business case for many colocation providers with considerable AI Datacenter capacity pipelines in Tier 2 countries.

Its new global licensing regime makes illicit re-exports much more difficult, and depending on which providers are approved as VEUs, this may also meaningfully restrict companies from Tier 3 countries like China from accessing AI compute through cloud services, although there is a big loophole we will discuss below.

As shown in the chart below, the majority of existing and future AI datacenter capacity is in Tier 1 versus Tier 2 countries – mainly in the US. The only meaningful Tier 3 country is China (not shown in the chart). While these rules will reconfigure and stymie the business case for many colocation operators with large Tier 2 country pipelines, potentially affecting AI gigaclusters like Johor in Malaysia, India, Brazil, and the Middle East.

Ultimately it may not meaningfully constrain shipments of AI Chips in aggregate due to increased building in tier 1 and reconfiguring AI Chip deployment plans, shifting them into the hands of major US Hyperscalers operating overseas, or reshoring demand back to the US. Most the largest Neoclouds such as Coreweave, G42, Nebius, etc will be unaffected as they will continue to expand in Tier 1 and get licenses for Tier 2.

![](https://substack-post-media.s3.amazonaws.com/public/images/93afa577-8927-48f8-ab51-83ad637d9781_1732x952.png)
*Source: SemiAnalysis Datacenter Model*

To be clear, the impact to Nvidia is still large in the medium term in so far as it reduces GPU access for China which does make the market smaller. The question is if Western demand makes up for it, and the answer is likely not as the [pricing of H100’s is tanking](https://semianalysis.com/core-research/). While Nvidia’s [H20 and B20 production targets](https://semianalysis.com/accelerator-industry-model/) keep being increased, [these products are lower margin and ASP than the regulated H200 and B200](https://semianalysis.com/2024/03/18/nvidia-b100-b200-gb200-cogs-pricing/).

It is important to note that this Framework is not just about regulating the physical destination of chips but also the nationality of the end user of those chips. Tiering of companies is based on the country of the ultimate parent of a company. For example, in the case of Volvo, the “Swedish” automaker, which is majority owned by Chinese automaker Geely and uses significant Chinese auto parts, electronics, manufacturing, and design, would be considered Chinese and has their GPU access limited.

The rule has very far reaching effects such as customer confidentiality and confidential compute being effectively illegal because clouds must now track what clusters ranging in the 10k+ GPU range are doing to ensure they are not making frontier models on them for China. This compounded with the very strict limitations on GPU caps changes the landscape drastically and was effectively regulatory capture by Microsoft, Amazon, and Google.

Next we will dive into the details of this new rule, and the impact it has on chip designers and manufacturers, major US hyperscalers, AI Neoclouds, and datacenter colocation providers. We will also zero in on Johor, Malaysia, India, Brazil, and the Middle East, explaining how this rule will decisively reshuffle the deck for the datacenter market that has seen some of the most ambitious plans for AI datacenter buildouts – some of which have been to cater to demand targeted by the new rules. We will dive into the incorrect argument that Huawei and China will be able to leverage this to gain influence overseas. We will explain in detail the new restrictions on Model training and Model Weight Exports. We will cover impacts to Nvidia, Google, Microsoft, Amazon, Oracle, G42, Scala, and more. We will also talk ASICs vs GPUs and the cloud margin impacts. Lastly we will cover what the Trump administration should do next.

## **AI Chips in Scope and the Total Processing Performance (TPP) Framework**

The [October 2023 export restrictions](https://semianalysis.com/2023/10/24/wafer-wars-deciphering-latest-restrictions/) introduced a number of incredibly strict rules blocking the shipment or reexport of the most powerful chips to a number of restricted countries including China. The Total Processing Performance (TPP) and Performance Density framework effectively blocked the A100, H100, MI250X and MI300X as well as even some gaming GPUs like the RTX4090 among other powerful chips from export to China and other restricted countries.

To recap, TPP is calculated by multiplying the marketed TFLOPS by the Bitlength for that marketed TFLOPS throughput (i.e. for H100 on FP8, this would be 1,978.9 x 8 = 15,831), while Performance Density is the TPP divided by the Die size (i.e. for the H100, this would be 15,831 / 814mm2 = 19.4). The overhaul of the scope covered by Export Control Classification Numbers (ECCN) 3A090.a in the October 2023 rules prohibited export of the Chip to restricted countries if EITHER the TPP is above 4,800 OR the performance density is above 5.92 as depicted in the Black Zone in the diagram below.

ECCN 3A090.b covers less powerful chips than 3A090.a and exports under the former ECCN may be allowed with licensing. 3A090.b’s scope (The “Grey Zone” in the chart below) includes chips such as the L40 and MI210, with 3A090.a (The “Black Zone”) catching the most desirable chips. Note these rules do not add additional controls to 3A090.b chips and they continue to be able to be freely exported to countries that are not Arms Controlled Countries or Macau.

In reality, official GPU shipments to China are dominated by the PRC SKUs such as the Nvidia H20 and AMD MI308X that fall below both performance thresholds for both 3A090.a and 3A090.b, and are in the “White Zone” below.

![](https://substack-post-media.s3.amazonaws.com/public/images/25716717-af7d-4677-b1bb-5f7f084b6052_2560x1521.jpeg)
*Source: Center for Strategic and International Studies*

The table below features most current and upcoming leading edge AI Chips, illustrating how TPP is calculated, and specifying whether the chips are in scope for ECCN 3A090.a, and how shipments of each SKU count toward the various exemptions made available which will be discussed in greater detail below.

![](https://substack-post-media.s3.amazonaws.com/public/images/b560a189-2631-4d09-935f-2a8779b9a6e2_1482x544.png)
*Source: SemiAnalysis, US Bureau of Industry and Security, Nvidia, AMD, Intel, Google, Amazon.*

Notice how the 1,700 H100s cap quickly becomes fewer than 500 GB300 GPUs.

One bright side of the regulation is that Nvidia and AMD may stop capping on the FLOPS they publish for their chips finally [because there’s no conceivable way to get 1979 TFLOPS on an H100, the max you can get on repeat GEMM is more than 25% lower](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/). This may have AMD and Nvidia transition to an advertised boost clock and a true base clock like CPUs so FLOPS aren’t exaggerated.

## **How the AI Diffusion Framework Works**

To begin, the AI diffusion framework creates a global license requirement for the export of AI chips, and grants exemptions to this licensing requirement that effectively divides the world into three tiers of countries:

Tier 1: The United States plus 18 security and trade partners or treaty allies that are highly aligned with the US in terms of control over strategic technology and have trustworthy export control regimes. GPUs may be shipped into these countries under the Artificial Intelligence Authorization (AIA) exception, but the entity importing the GPUs must be headquartered or have its ultimate parent from a Tier 1 country.

Tier 3: Countries are the list of [23 arms-embargoed nations (Country List D:5)](https://www.bis.gov/ear/title-15/subtitle-b/chapter-vii/subchapter-c/part-740/supplement-no-1-part-740-country-groups) plus Macau, where exports of controlled chips are effectively banned. This includes China, Russia, Syria and other countries.

Tier 2: These countries are all the other countries all other countries that are not the countries in Tier 3 and Tier 1. It is these countries where the biggest changes occur, and shipments to these countries may be allowed under a set of license exemptions that set up quotas, limits and rules depending on the parties importing the AI chips. We outline the various exemptions later in this section. Some notable countries in the Tier 2 list are Malaysia, India, and Singapore. The fact Yemen which bombs US tankers and Singapore which is a significant US strategic partner are in the same tier speaks volumes to how much the US government believes GPUs are being smuggled through Singapore to China.

The table below sets forth a complete list of Tier 1 and Tier 3 countries, as well as a non-exhaustive list of notable Tier 2 countries. Particularly noteworthy markets and countries are highlighted in light red.

![](https://substack-post-media.s3.amazonaws.com/public/images/344e20f7-6d3e-4044-9acb-ce2ce3602dad_724x717.png)
*Source: SemiAnalysis, Bureau of Industry and Security*

There are three broad categories in which AI Chips are permitted to be exported to Tier 2 Countries:

## Shipments to Two Classes of Validated End Users (VEUs):

- **Universal Validated End Users (UVEUs):** Companies that have their headquarters or ultimate parent in a Tier 1 country and that can meet various security and compliance standards. Companies will need to apply to become recognized as UVEUs, we think that US Hyperscalers such as Microsoft, Amazon, Google and Meta will likely qualify under this category, and we expect that the application process will be streamlined and not onerous. UVEUs will be able to seamlessly obtain licenses to import GPUs into Tier 2 countries so long as they satisfy certain requirements:

  - UVEUs must have **75% of their controlled compute in Tier 1 countries**
  - They cannot have more than **7% of controlled compute within a single Tier 2 country**.
  - If the UVEU is from the US, that UVEU must have 50% of its total AI computing power within the US. [Based on our AI Datacenter Industry Model](https://semianalysis.com/datacenter-industry-model/), for the next few years, all major US hyperscalers will have well beyond 50% of their compute in the US and are also safely above the 75% Tier 1 country threshold.
  - UVEUs are subject to stringent security requirements that govern topics like model weights, supply chain security including personnel checking, and transit security. These security measures will be covered in detail in a later section.
- **National Validated End Users (NVEUs):** NVEU Authorizations can be granted to entities from Tier 1 and 2 countries that can meet specified security requirements export a much larger number of accelerators into a single specified country (that is not a Tier 3 country). This would cover scenarios such as national AI champions that are headquartered in Tier 2 countries and who want to build large AI clusters in their home country, but also for said national AI champion to build a cluster in another destination country – though NVEUs would need to apply for a separate NVEU authorization in each additional country they want to build in using this NVEU exception. For a company from a Tier 2 country, they would also need an NVEU Authorization to deploy a significant amount of GPUs in a Tier 1 country.

  - An NVEU authorization gives the NVEU an export license to have an installed base of up to  ~320,000 H100 equivalents for use in the destination country they have received the NVEU for, though the installed base allowance is phased in gradually as per the table below. It is likely that to be granted an NVEU authorization, the specified destination country will need to have a government-to-government agreement with the US in advance.
  - NVEUs must follow the same stringent security requirements as UVEUs, but with added requirements in specific circumstances. For example, UVEUs must submit semi-annual reports to the BIS including a record of current inventory, but NVEUs have to disclose a list of current customers.

![](https://substack-post-media.s3.amazonaws.com/public/images/22a357dd-da4d-4da5-8858-72f6728c439a_1202x540.png)
*Source: SemiAnalysis, Bureau of Industry and Security*

To be clear, this isn't a huge number of next generation GPUs. This will hamper Nvidia.

## Individual Country Allocations of Compute (TPP)

For GPU purchases outside of the 1,699 H100 equivalents, and other than from VEUs, there is a quota for a maximum AI chip **install base** of up to 49,901 H100 equivalents shipped from 2025 until 2027 in each Tier 2 Country. This is again based on a Total Performance Power (TPP) basis. So if 49,901 H100 equivalents were installed in 2025 in a certain country, there would be no quota available to ship any additional GPUs in any subsequent years through 2027. Note that GPU shipments under 1,699 H100 equivalents or to VEUs do not count against the 49,901 GPU install base cap.

In addition, Tier 2 country governments that sign agreements to align export control and technology security goals with the US can double this cap up to 99,802 H100 equivalents. As such, countries with a dearth of UVEUs or NVEUs in the market and therefore functionally limited by this cap are by definition left behind as chip capabilities advance globally as the TPP framework by definition freezes in time their total available AI compute. We can see how the cap can quickly become onerous with it works out to only 13,166 GB300 equivalents, a low amount for a chip that will start shipping in late 2025 and works out to even lower quantities of AI chips once Rubin and Rubin Ultra come to the market in late 2025 and late 2026 respectively.

## The Loophole: Low Processing Performance (LPP) Exemption

Entities in Tier 2 countries can also buy controlled compute of up to 26,900,000 in TPP per customer per calendar year (1,699 H100 equivalents) freely without any license requirement, though buyers will need to inform the BIS. Ironically, this is a loosening of export controls for many Middle Eastern and Central Asian countries where GPU purchases of any quantity previously required an export license. This is to make the process of procuring a benign amount of compute easy for entities in Tier 2.

Those that argue that the Framework on AI Diffusion is not overly onerous, point to the argument that most GPU shipments fall below this threshold – but this argument cuts both ways – it is possible that many bad actors illicitly re-exporting GPUs are doing so in small quantities and would continue unimpeded – albeit with more of a paper trail.

Huawei has done this through an extremely complicated web of shell companies for many ICs and [semiconductor wafer fabrication tools](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/), we believe the US Government will be caught flat footed and not be able to prevent this too.

![](https://substack-post-media.s3.amazonaws.com/public/images/c3750c54-5008-4d96-97db-5b9ab1421c35_1773x1198.png)
*Source: SemiAnalysis, Bureau of Industry and Security*

A single cloud company doing a 20k GB200 cluster or a 13k GB300 this year can take an entire countries cap off the table. This is on the order of a $1 billion investment... not exactly huge numbers of GPUs.

## **Gaming GPU Carveouts and AI Training Restrictions**

For gaming GPUs, the AI Diffusion Framework provides the License Exception Advanced Computing Authorized (ACA): This is a carveout for chips that are covered by 3A090.a but not designed or marketed for use in datacenters i.e. consumer gaming GPUs. The ACA license exception is only for Tier 2 countries and the ACA exception does not require any notification to BIS, effectively allowing consumer gaming GPUs to ship freely to these markets. The treatment for Tier 3 Countries is more stringent, with the same products requiring a NAC (Notified Advanced Computing) license exception which is more onerous. The NAC license exemption requires an application to BIS for export and inter-agency review. Therefore, high-end gaming GPUs like the RTX4090 have effectively been banned in China and other Tier 3 Countries. These gaming cards can be popular for some users as they have decent price-performance ratios for certain inference workloads.

In all cases, the AI Diffusion Framework *also* imposes restrictions that prevent the training of frontier models, which is defined as the greater of 1e26 training FLOPS or the training FLOPS of the largest open-source model on the market, as well as prohibiting the export of model weights of models of this size with closed weights. We will explain the restrictions on AI Model Training and Model Weights Exports in much more detail below.

## **AI Diffusion Framework Effective Date and Implementation**

The Initial Final Rule (IFR) released on January 13th is set to take effect 120 days from the release date, and companies in scope will only be required to start complying with the rule after the 120 days. However – shipments after January 13th will be counted against allowances provided for in the LPP and Individual Country Allocations/Caps. However, it is an open question how such shipments will be reported to the BIS given there are no compliance requirements until after 120 days. It is possible that reporting will be done in one go, the first time a company needs to comply with the new rules – for instance if they order additional AI Chips or request an RMA, this would trigger reporting that would bring the count up to date.

The implementation details might also trigger a dilemma for providers that are unsure if their applications for UVEU or NVEU status will be approved. They could quickly exceed per company annual allowances under the LPP or even country wise allocations if they carry on purchasing large numbers of AI Chips, but ultimately are rejected for UVEU/NVEU status. We hope a fast application process will mitigate any potential AI Chip procurement headaches.

## **How the Validated End User (VEU) Framework Impacts AI Regional Deployment**

The new framework requires all companies willing to deploy GPUs to submit a VEU Authorization application – and involves 19 separate certification and policy requirements, to become either a UVEU or NVEU

Notably, the process requires approval from 4 different agencies: The Department of Commerce, State, Defense, and Energy. Coordinating across 4 different agencies entails processing applications may not be as fast as some were hoping.

We show below the list of requirements to be certified as a VEU:

1. General Compliance and Proven Track Record: the VEU must demonstrate that it meets physical, cyber, and personnel security standards.
2. No Foreign Military and Intelligence Ties
3. Foreign Technology ties – includes, amongst other requirements, the VEU proving it has cut off supply chain dependencies on advanced semiconductors and key networking equipment made by Tier 3 countries.
4. Transfer of Chips
5. Intra-company transfer notification
6. Geographic allocations
7. Advanced AI Training
8. Model Weight Storage
9. Prohibited Uses and Human Rights Safeguards
10. Reporting of Chip installations
11. Monitoring, Recordkeeping and Reporting
12. Certification and VEU

In addition, there are the following Security Requirements:

1. Ownership Security of VEUs
2. Baseline Security of Chops and Data
3. AI-specific Cybersecurity
4. Transit Security
5. Sanitization and Disposal Procedures
6. Personnel Security Standards and Practices
7. Enforcement

The most significant requirements relate to stringent requirements for AI specific cybersecurity, including rate limiting devices that interface with model weights and only enabling access to other model weight interfaces via a well-defined narrow API. Other considerations also include shipment security plans with anti-theft and anti-tampering measures reported to the BIS, and considerably tighter vetting requirements for any persons with access to a VEU data center facility.

For UVEUs, the key restrictions are as follows: at least 75% of total AI computing power in Tier 1 countries, no more than 7% in any individual Tier 2 country, and for US-headquartered UVEUs, at least 50% needs to be located in the US.

Note our data shows that Microsoft will be right up against the line with their planned Malaysia investments, so they cannot effectively take up the datacenter slack there, and Oracle is way over the limitations.

For UVEUs must provide BIS 60 days’ notice before transferring controlled chips between countries as well as any planned Datacenter construction plans in new previously unreported jurisdictions.

## **AI Training and Inference Impact**

There are rules imposed on the specific workloads US or allied cloud service providers can provide to a Chinese (or other Tier 3 country-associated) player. The main goal is to prevent the **training** of a new frontier AI model which is defined as a model trained on 1e26 FLOPs or more. This is consistent with the definition provided in the October 2023 [AI Executive Order](https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/).

![](https://substack-post-media.s3.amazonaws.com/public/images/6fe10206-be17-4e8a-932a-9b870029fe8a_1705x973.png)
*Source: SemiAnalysis*

Within the new rules, frontier AI models can only be trained in Tier 1 countries, with limited fine-tuning allowed outside these countries, restricted to no more than 25% of the original training operations or 2e25 FLOPs of fine tuning. The provision of API access to AI models or IaaS access for AI inference is permitted. Topics like inference time scaling are not covered, though there are clauses relating to synthetic data.

## **AI Model FLOPS Regulation Depends On Strong Open Source**

There are a considerable amount of models which do not fall under the regulation. Any open-source model does not fall under the purview of this regulation, unless it is fine-tuned with 2e25 operations or the equivalent of 25% of the pre-training FLOPs. This means that significant fine tuning of open-source models may turn models from unregulated to regulated ones (thus treated as closed models), depending on the exact number of FLOPs used during fine tuning. Following from above, models trained under 1e26 FLOPs are also not under the purview of this regulation.

In addition to this, models that utilize fewer FLOPs than the number used to develop the best widely available open model, as judged by a variety of benchmarks, are also not subject to this regulation. This however requires self-classification, which must be followed from the recommendations of the BIS or the technical opinions of US AI Safety Institute and Department of Energy.

This means that there are three main categories for models that are not regulated: models that are trained under 1e26 FLOPs, open-source models, and models that utilize fewer FLOPs than what was used to train the best available open-source model at a given time.

In the long run, this means that if there is a model that exceeds 1e26 in training, then the flops used to train that open-source model will be used as the lower bound of what counts as regulated.

For now, models that *do* fall under the purview of the regulation are ones that utilize more than 1e26 FLOPs during pre-training. However, this number is better thought of as a “compute budget”, as it is not just pre-training flops that count towards this. If synthetic data is used and is generated by a closed source model to the point where more than 10% of the pre-training operations are over this synthetically generated data, then the number of operations it took to generate such data also counts toward the overall budget. In other words, if a huge portion of the pre-training data is synthetic data, then that counts against the number of raw compute that can be used to train a model. In this case “a single model” can be variants of the same model (e.g., fine-tuned or previous check points).

If more than one closed-source model is used and in combination, they comprise more than 10% of operations, then the number of operations from the model comprising the largest amount of data are counted toward the compute budget.

It is important to note that counting the amount of “operations conducted to generate the data” is by no means a clear task. As outlined in a previous article, synthetic data generation is now a complex process involving many steps including generation and filtering (which itself is done by other models). The regulation models this poorly.

This alone is difficult to narrow down. However, counting the “operations” required to generate text (i.e. inferencing) it an extremely complicated task with no established reliable method to doing so. For example, unlike training, it is much more difficult to ascertain the exact model flops utilization (MFU) of a GPU during inference. As such, we expect that if the data generated does indeed end up comprising more than 10% of a model’s pretraining operations, then counting the exact number of operations will be technically challenging at best and infeasible at worst.

Note that for the table below, all parties have to comply with the newly outlined Security Requirements.

![](https://substack-post-media.s3.amazonaws.com/public/images/460433dc-b624-46d3-9796-88ec75583c64_2302x885.png)
*Source: SemiAnalysis, Bureau of Industry and Security*

## **Model Weights Are Now An Export-controlled Item**

Model weights are the learned parameters of a model that emerge after training and were always controlled as they represent the model itself, but now there are additional controls on where and how weights can be stored, transferred, etc.

In addition to stringent security controls on model weights, models that do fall under the purview of the new regulations are subject to licensing requirements for exporting model weights to non-tier 1 countries. There are also limitations in place for GPU providers, restricting who will be able to rent GPUs and to what scale they are able to train.

For example, VEUs cannot allow non-Tier 1 countries to train frontier models, and US based providers must follow “Red Flag Guidance” which can be triggered when a China based company or US based subsidiary thereof is training on US GPUs, and as such the model weights might be at risk of going to a restricted country.  The BIS requires a license to export, re-export, or transfer (even within a country) model weights of any closed source model that is above the 1e26 FLOP compute budget, with a license exception if the destination is a Tier-1 country (though security requirements apply).  This license has a presumption of denial and will have a considerable amount scrutiny when it comes to approvals. The top 3 labs already have robust security infrastructure, so we do not think they will face significant issues getting these licenses.

Authorizations, licenses, and security requirements still apply and are required to train frontier models, regardless of whether under the current country cap or if an LPP is present.

The BIS doubles down and applies a foreign direct product rule on model weights. This means for all models developed via US-controlled hardware, US export controls and regulations will apply regardless of where the model is developed. Again, this will not apply if the end model is an open-source model, but will apply for any model larger than a compute budget of 1e26. This means getting the appropriate licenses and complying with model weight security requirements.

Additional requirements were added to cloud providers. For example, the BIS aims to implement “Know Your Customer” and Red Flag guidance for US based providers. The primary concern for this also relates to model weights. The goal is to have cloud computing companies based in the US to identify if a training run is being conducted by a US subsidiary of a foreign company. This is to prevent a US subsidiary from using amounts of compute above the prescribed threshold and then transferring the model weights to a Chinese company. In reality, if a customer is conducting a run large enough for a 1e26 flop model (in compute or in time), then the cloud provider should have a robust idea of who that customer is.

A common critique of these regulations is that Chinese companies like ByteDance are still able to access significant amounts of GPUs from US based cloud providers. This is by design – the goal is not to completely cut off China from being able to use AI, rather to ensure increased US dependence. With strong US dependence, cutting them off US cloud providers would be relatively easy.

Bare metal deployments or renting might also see a big change, as providers are now incentivized to place monitoring agents in order to ensure a customer is not training a restricted model.

Considerable cyber-security requirements are also added when it comes to interfacing with model weights. For example, model weights must be stored on dedicated devices not used by other organizations (or even hosting the data of others). Additional requirements include the detailed review of every possible method with which weights can be accessed directly and indirectly while also rate-limiting the output of such devices under continuous monitoring.

The overall goal is to tightly control and monitor physical locations of chips and model weights, while allowing access to models through a controlled API.

## **How the BIS Monitors Global Compliance**

Enforcement is going to require a multi-faceted approach across multiple different organizations: self-reporting, monitoring, compliance with BIS, and obtaining licenses from multiple agencies are all parts of this process. Additionally, there are several changes on the technical level that will have to surface by the time these reports roll out, like for example CPS monitoring on bare mental renting. Such changes will be easier than others, like figuring out a standard to count the number of operations a model used to generate data to train another model (if it is more than 10% of a model’s training data) is going to be extremely difficult at a minimum.

Significant enforcement will have to be done by the datacenters themselves, including detailed logging, increased personnel vetting, supply chain monitoring. Much of these are on the onus of the datacenter to establish and build out, with regular reporting to the BIS.

In summary, this new set of rules is set to significantly impact the global AI and datacenter landscape, from datacenter developments to equipment companies, hyperscalers and Neolcouds. While this is generally a net positive for US hyperscalers, we will explain why Oracle stands to lose the most.

## The Resultant Geographical Order

The rules have reshuffled the deck for many countries with respect to availability of AI chips. Under the new rules, entities based in some countries in the Middle East and Central Asia like the UAE or Saudi Arabia will now face a far more permissive regime. Previously, they were required to have an export license to purchase any quantity of controlled chips but now they have avenues to access these chips without any export licenses within the bounds of the LPP and Individual Country Allocations. Conversely, countries like Malaysia, Singapore and Thailand and many others that previously enjoyed unfettered access to chips will now be relegated to Tier 2 countries with non-VEU providers limited in their AI chip purchases.

![](https://substack-post-media.s3.amazonaws.com/public/images/5e5a5207-14d3-4803-af70-869307df0b51_438x716.png)
*Source: SemiAnalysis, US Bureau of Industry and Security*

This regulation will also achieve the policy objective of limiting potential bad actors from abusing permissive regulations in certain jurisdictions to accumulate a large amount of compute that can be physically re-exported to Tier 3 countries. Indeed, there is considerable debate over the extent to which such illicit trans-shipment and re-exporting is occurring, but policymakers have decided to act against such behavior regardless.

## **Global Datacenter Impact**

The regulation will have a key impact on the geographic distribution of AI deployments. On a global perspective, by 2027, we estimate that >5GW of IT Capacity in Tier 2 countries is directly driven by AI Accelerator purchases. However, not all of this is at direct risk from the new rules. We lay out below the forces driving overseas datacenter deployments:

- Sovereign AI initiatives.
- Large datacenters for US hyperscalers.
- Gigawatt-scale datacenters to solve the AI power supply/demand deficit.
- Large datacenters for non-US hyperscalers.

Let’s start with Sovereign AI. The field is very heterogeneous but generally involves a Neocloud or Hyperscaler building GPU clusters and selling its compute power to a local ecosystem at government-subsidized rates. Common end-customers include scientific R&D, education, healthcare and military – as well as incubators for startups.

The GPU-as-a-service business has significantly lower technical barriers to entry compared to traditional CPU Cloud Computing. This incentivizes local firms to emerge as national AI Cloud champions, instead of global US hyperscalers.  However, despite all the headlines and press releases, this market is not significant on a global scale. The new round of export rules will slightly limit growth but doesn’t change meaningfully the market trajectory.

![](https://substack-post-media.s3.amazonaws.com/public/images/3224a512-8672-44da-806a-daa411aedd50_2318x1286.png)
*Source: Nvidia*

Next, let’s evaluate US hyperscaler overseas deployments. While individual Tier 2 countries can’t weigh more than 7% of a given UVEU's controlled computing power, and 25% in aggregate for all Tier 2 countries, we show below that the risk is highly unlikely to materialize. The United States is extremely dominant in the global datacenter market even without export restrictions, with >10 different GW-scale campuses ramping up over the next two years, as well as multiple 100MW+ clusters. From foundation model builders, to Clouds, to datacenters, to chip designers, US-based firms dominate the AI ecosystem and want to stay within borders.

![](https://substack-post-media.s3.amazonaws.com/public/images/4d7d9beb-f141-4f98-8135-ae426999314f_1732x952.png)
*Source: SemiAnalysis Datacenter Model*

Overseas, GenAI deployments are driven by inference and small to mid-scale training workloads. Countries like India, and Brazil to a lesser extent, with their significant population, are experiencing rapid growth in their digital infrastructure, largely driven by US hyperscalers and overall economic growth.

![](https://substack-post-media.s3.amazonaws.com/public/images/494742c5-4acb-4129-a7ca-9d045c10a0b5_1593x906.png)
*Source: SemiAnalysis Datacenter Model*

More recently, a new type of overseas deployment is emerging. With frantic demand for AI compute pushing the limits of supply chains like [electrical equipment](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/) and power transmission and generation, growth in the United States is increasingly constrained. Various datacenter developers overseas have identified the issue and proposed massive campuses as a solution. The flashiest example so far is the “AI City” in Brazil – a 4.75GW campus planned by Brazilian developer Scala Data Centers!

![](https://substack-post-media.s3.amazonaws.com/public/images/342def51-9eb3-4934-8f59-3cb3670b7bf0_1024x680.png)
*Source: Scala Data Centers*

And while such announcements are often met with skepticism, especially when said projects are located outside the US, they illustrate the value proposition of going overseas. The specific campus is developed alongside an **existing** 3GW high voltage electrical substation, with ample unused wind and hydro power. It could be the largest AI cluster in the world if someone with deep enough pockets wanted it to be.

It remains unclear how the new rules will impact such developments. In our view, US hyperscale appetite to deploy large-scale infrastructure overseas is likely to be somewhat reduced. However, governments are likely to engage with the White House to reduce the regulatory uncertainty facing their potential US hyperscale customers. We expect the Middle East in particular to be a strong force, aided by a lowered political overhead compared to areas like Brazil, where governmental stability remains a hurdle.

![](https://substack-post-media.s3.amazonaws.com/public/images/e721e3e3-b5df-4dc3-8da4-4339d6f6fe7b_1774x1402.png)
*Source: SemiAnalysis Datacenter Model*

Below we will discuss the Datacenter winners and losers, YTL and the Malaysian Neocloud ecosystem, the big tech monopoly problem that this regulation brings, the Oracle problem/question, Nvidia's lost business, cloud margins, Chinese chip ecosystems and penetration overseas, and the Trump administration's next steps with taking this regulation forward / improving it.

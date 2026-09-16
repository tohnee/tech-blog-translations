---
title: "Tariff Armageddon? | GPU Loopholes, Mexico Supply Chain Shift, Wafer Fab Equipment Vulnerabilities, Optical Module Pricing Surge, Datacenter Equipment"
subtitle: "UPS, Generators, Transformers, Switchgear, Power Distribution Equipment, Chillers, Cooling, Pumps, OEM & ODM Supply Chain, Lasers, Softbank Impact, Nvidia Balance Sheet Usage"
date: 2025-04-10
source: https://newsletter.semianalysis.com/p/tariff-armageddon-gpu-loopholes
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeremie Eliahou Ontiveros", "Patrick Zhou", "Jeff Koch", "Sravan Kundojjala", "Reyk Knuhtsen", "Christopher Seifel", "Wega Chu", "Maya Barkin"]
tags: ["Supply Chain", "Export Controls", "AI Policy"]
audience: only_paid
paywalled: true
---

# Tariff Armageddon? | GPU Loopholes, Mexico Supply Chain Shift, Wafer Fab Equipment Vulnerabilities, Optical Module Pricing Surge, Datacenter Equipment

**UPS, Generators, Transformers, Switchgear, Power Distribution Equipment, Chillers, Cooling, Pumps, OEM & ODM Supply Chain, Lasers, Softbank Impact, Nvidia Balance Sheet Usage**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

The buildout of AI infrastructure in the US has reached a macro-level scale, and ensuring continuous growth will require ample availability of capital. We believe that the economic uncertainty induced by Trump tariffs could become the single largest barrier to American AI supremacy. With [Scaling Laws](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/) still very much alive, tens of billions of dollars of capital expenditures are required by leading AI Labs to keep improving the quality of their products & systems at this incredible pace.

But economic uncertainty often leads to delays, and delays lead to contractions. In a worst-case scenario, America's foreign policy could trigger a global recession and force leading AI labs to abandon their training efforts to preserve cash.

Fortunately, on a micro level, our research indicates that the tariffs will not impact (for the most part) the competitiveness of the United States in AI infrastructure costs but rather through capital accessibility. In this report, we show our findings and deep dive into tariffs, loopholes, and global trade for AI-related infrastructure equipment.

The report will examine the details of Trump’s Liberation Day tariffs and their impact on AI infrastructure. It will cover GPU/XPUs and servers, networking, data center cooling and electrical equipment, and semi-cap. We also analyzed each of these supply chains and their trade dynamics to better gauge the situation.

Before getting into the details, we share our high-level takeaways. In each section, we go into much greater depth.

On **a macro level:**

- Cost of capital is rising, with soaring 10 year interest rates, and the tightening of financial conditions could likely lead to a short-term slowdown in the AI infrastructure buildout. The administration must react now and strike deals with their trade partners.
- Retaliatory tariffs targeting US Big Tech are possible but unlikely to have a major short-term impact on US hyperscalers. Despite running large trade deficits on goods, the US actually runs surpluses with services - helped by its technology giants.

On a **micro level**:

- GPU servers are largely exempted from tariffs. Mexico is already a large assembly hub and will take a central role in this new world order.
- Datacenter construction costs could increase by mid-to-high single digits – but [the TCO impact for GPU cloud operators is likely less than 2%](https://semianalysis.com/ai-cloud-tco-model/).
- Wafer fabrication equipment will be 15% higher for US fabs. And players with the highest share of US manufacturing stand to lose the most – given the global nature of the industry.
- Optical module costs will increase by 25-40%
- Some manufacturers are significantly better positioned than others, with highly localized supply chains.

With that said, let’s get into the details.

## How the Trump tariffs actually work

**Trump's far-reaching “Liberation Day” tariffs**

On April 2, 2025, President Trump announced sweeping tariff measures targeting nearly all US trading partners. Invoking the International Emergency Economic Powers Act (IEEPA) as the legal basis for his tariff order, the Trump administration cited "a national emergency resulting from conditions reflected in large and persistent annual US goods trade deficits."

Trump's executive order establishes two main measures. The first is implementing a blanket 10% ad valorem tariff on all goods coming into the US, effective April 5, 2025. Along with this baseline tariff, the administration introduced a second round of higher, [country-specific ad valorem reciprocal tariffs](https://www.whitehouse.gov/wp-content/uploads/2025/04/Annex-I.pdf) targeting 57 countries with the largest trade deficits with the US. These tariffs, ranging from 11% to 50%, rates are set to take effect on **April 9, 2025.** Many countries received a 90-day pause on tariffs where rates are increased to 10%.

Particularly significant individual tariff rates include a 34% on all imports from China, which was increased to 84% (by 50 pct) by the Trump administration on April 8, after China retaliated with 34% tariffs on all U.S. imports. Trump further increased addtional tariffs on China to 125% in April 9, after China matched Trump's previous 50% increase and vowed to "fight to the end". This brings the total tariff on Chinese goods to 145%, given that it was on top of the already implemented 20% tariff since February 2025 (unlike some industry analysts' claim that the total was 125%). Other notable rates include 32% on imports from Taiwan, 26% on India, 25% on South Korea, and 24% on both Japan and Malaysia. The European Union, treated as a single trading bloc, will be subject to a uniform 20% tariff.

The chart below illustrates the US tariff rates applied to several major global trading partners, effective April 9 (many nations are at 10% until 90 days from now).

![](https://substack-post-media.s3.amazonaws.com/public/images/320d9ebb-cb85-4027-a3d7-b3563b8c0f30_908x578.png)
*Source: The White House, SemiAnalysis*

The tariffs introduced by the Trump administration are set to cause significant disruptions to a global trading system that had been in place for more than 75 years. The White House's recent tariff measures are expected to raise US tariffs to their highest level since 1909, reaching a staggering 22%, and marking a significant break from the long-standing trend of trade liberalization. On their own, the country-specific tariffs imposed by Trump on April 2 resulted in an average tariff rate of approximately 28%.

The dramatic increase in tariffs is illustrated in the graph below, which shows the US effective tariff rate from 1900 through April 9, 2025. After reaching highs of nearly 30% in the early 20th century, US tariffs declined steadily following World War II, mainly remaining under 10% for the past 70 years.

![](https://substack-post-media.s3.amazonaws.com/public/images/22e3bc5a-ab8a-44d6-90fd-62a8cac30bec_2520x1870.png)
*Source: Monthly US Treasury Statement, US Bureau of Economic Analysis, The Budget Lab at Yale, SemiAnalysis*

## **Key exclusions in Trump’s executive order**

The Trump administration's executive order includes important exemptions, although these fall short of providing comprehensive relief.

The new reciprocal tariffs will not apply in the following cases:

- **Goods originating from Canada and Mexico**: These will continue to be exempt as long as [Trump’s previous executive orders](https://www.whitehouse.gov/fact-sheets/2025/03/fact-sheet-president-donald-j-trump-adjusts-tariffs-on-canada-and-mexico-to-minimize-disruption-to-the-automotive-industry/), effective since March 7, 2025, remain in place. These orders maintain the existing exemption for products that comply with the “rules of origin” under the United States-Mexico-Canada Agreement (USMCA), which are subject to a 0% tariff. Goods that do not qualify as originating under USMCA, however, are subject to an ad valorem tariff of 25%, while energy resources from Canada and potash from Canada and Mexico not qualifying under the USMCA face a duty of 10%.

  - The April 2 executive order specifies that if the current tariffs on Canada and Mexico are removed, a new 12% tariff would be imposed on goods that do not qualify as originating under the USMCA.
- **Steel and aluminum products, along with their derivatives**: These are exempt and continue to be subject to the [25% tariff](https://www.whitehouse.gov/fact-sheets/2025/02/fact-sheet-president-donald-j-trump-restores-section-232-tariffs/) under Section 232 of the US Trade Expansion Act, effective since March 12, 2025.
- **Automobiles and auto parts**: These are exempt and instead subject to the [25% tariff](https://www.whitehouse.gov/presidential-actions/2025/03/adjusting-imports-of-automobiles-and-autombile-parts-into-the-united-states/) outlined in Section 232, effective since April 3, 2025.
- **Exempted items listed in [Annex II](https://www.whitehouse.gov/wp-content/uploads/2025/04/Annex-II.pdf) of the executive order**: Pharmaceuticals, semiconductors, lumber products, select critical minerals, and various energy goods are not subject to the tariffs. We detail the exempted semiconductor devices and components, electrical integrated circuits, as well as key raw materials in the following two tables below.
- **Products with US content**: The 10% baseline and country-specific tariffs apply only to the portion of a product made outside the US, as long as at least 20% of the product’s value is derived from US-made or US-processed parts.
- **Imports from Column Two countries**: Belarus, Cuba, North Korea, and Russia will continue to be subject to their existing duty rates.
- **De minimis threshold**: Goods under the $800 de minimis threshold are currently allowed duty-free entry. Starting May 2, 2025, goods from China and Hong Kong will no longer be exempt and will be subject to standard Chinese import duties.

[Annex II](https://www.whitehouse.gov/wp-content/uploads/2025/04/Annex-II.pdf) of Trump’s April 2 executive order outlines the items under the Harmonized System (HS), a global product classification system for customs exempted from the administration's sweeping tariffs. The HS 8541 and 8542 categories cover several semiconductor devices, such as diodes, transistors, and integrated circuits, with HS 8541 including several discrete devices and HS 8542 encompassing different types of electronic integrated circuits. The relevant items are listed in the table below:

![](https://substack-post-media.s3.amazonaws.com/public/images/625971f2-768e-49df-852d-8f35f2138633_1638x1254.png)
*Source: The White House, SemiAnalysis*

Overall, Annex II outlines a limited set of HTS codes in the semiconductor sector exempted from the new tariffs. Although semiconductor dies and integrated circuits will not be subject to the higher import duties, including the 10% baseline tariff and the tougher country-specific import taxes, the list of exemptions does not include GPUs and a range of chipmaking products and equipment that are essential to industry.

GPUs, which contain semiconductor dies and are typically considered data processing devices, are not exempt from the full brunt of Trump’s “Liberation day” executive order. Those generally fall under HS code 8471 for data processing devices, which are not included in Annex II. Automatic data processing machines under HS code 9903, which pertains to certain temporary or specific legislation, are not exempt from the tariffs either. As a result, under the current regime, exports of GPUs are automatically subject to a tariff under Trump’s executive order. Exports of GPUs from Taiwan to the US, for example, would be subject to the full impact of US reciprocal tariffs, equating to a 32% tariff on all GPUs exported from Taiwan to the US.

Nevertheless, **we identified a significant loophole in the current tariff structure** – explained in detail in the following section – that allows US companies to avoid tariffs on certain goods, including GPUs, imported from Mexico and Canada.

In addition to the above-listed exempted items from [Annex II](https://www.whitehouse.gov/wp-content/uploads/2025/04/Annex-II.pdf),  the White House’s executive order also removed several critical raw materials for making chips and batteries from the scope of the new tariffs. While GPUs are not included in the exemptions, this decision still supports the Trump administration’s stated goal of bolstering US manufacturing, particularly in the semiconductor sector, which depends heavily on imported raw materials and chemicals to produce high-value goods like equipment, components, and batteries. We list these key minerals in the table below, alongside their strategic importance.

![](https://substack-post-media.s3.amazonaws.com/public/images/dce3672b-f03c-4cbd-a79d-6c20da75cca3_820x804.png)
*Source: The White House, SemiAnalysis*

## **GPU tariff loophole under the USMCA**

While GPUs are subject to a 32% tariff on all GPUs exported from Taiwan to the US, there is a loophole in the current tariff structure that allows US companies to import GPUs from **Mexico and Canada at a 0% tariff.**

As outlined, goods from Canada and Mexico are exempt from Trump’s new tariffs as long as his March 7 executive orders remain in effect. These orders maintain the existing exemption for products that comply with the “rules of origin” under the USMCA, which means goods predominantly produced or obtained in the US, Canada, or Mexico are subject to a 0% tariff. In contrast, goods that don’t meet these criteria – except energy resources and potash – face a 25% tariff.

However, a specific provision in the USMCA protocol creates an exception for imports of GPUs, among many other items. Under the Most-Favored-Nation provision, certain products are considered and treated as “originating goods”, regardless of their country of origin. This includes the following:

- Digital Processing Units (HTS code 8471.50): Comprises assembled servers
- Other Units of Automatic Data Processing Machines (HTS code 8471.80): Comprises NVIDIA HGX server baseboards
- Parts & Accessories for ADP Machines & Units thereof (HTS code 8473.30): Comprises GB200 baseboards, NVL boards, and RTX

The Digital Processing Units and Other Units of Automatic Data Processing Machines categories both encompass GPUs. As a result, GPUs falling under these categories that are exported from Mexico to the US, for example, qualify for duty-free treatment, allowing them to bypass the 25% tariff that would otherwise apply to non-originating goods. They are essentially treated like avocados planted and grown in Mexico and exported to the US or Canada. This provides a significant advantage for US companies importing GPUs from Mexico or Canada to the US.

## **Possibility of a new round of tariffs**

The limited relief granted to semiconductors through their exemption from reciprocal tariffs, outlined in Annex II of the Trump administration’s executive order, is expected to be short-lived. The White House fact sheet states that the goods listed in Annex II that are not subject to the reciprocal tariff are “all articles that may become subject to future tariffs.”

In fact, the administration is already developing targeted tariffs for chips. During an April 3 press briefing aboard Air Force One, Trump [indicated](https://www.wsj.com/livecoverage/trump-tariffs-trade-war-stock-market-04-03-2025/card/trump-previews-chip-pharma-tariffs-q1WBoRT9sCDkcPGkVNlU) that he would soon announce new tariffs on imported semiconductors and other currently exempted items. Other White House officials, including Commerce Secretary Howard Lutnick, have also [confirmed](https://www.yahoo.com/news/commerce-secretary-howard-lutnick-us-044509343.html) that a separate semiconductor tariff strategy is still in the works. This is likely in conjunction with further TSMC-related manufacturing deals.

## **Countries’ differing responses to Trump’s tariffs**

The relationship between the US and China has seen the most rapid escalation, with tariffs on Chinese goods soaring to an unprecedented 145%. In response to the US’s initial announcement of 34% reciprocal tariffs on April 2, 2025 – on top of the 20% already in effect – China quickly condemned the action, calling it a violation of trade norms and an instance of "unilateral bullying." On April 3, China retaliated by imposing a 34% tariff on US imports, effective from April 10, in addition to the 10-15% tariffs on selected US agricultural and energy products already imposed in early 2025. Furthermore, on April 4, China introduced tighter export controls on crucial rare earth elements that are essential for producing high-tech goods like AI chips, semiconductors, and electric vehicle batteries. Chinese exporters must now obtain licenses from the Ministry of Commerce to export these materials.

In response to China's 34% levies in response to the initial "Liberation Day" tariffs, the Trump administration imposed an additional 50% tariff on all Chinese goods, pushing the total tariff on Chinese imports to the US to 104% (34% + 50% + the original 20%), effective April 9. In retaliation, China increased its tariffs on all US goods to 84%, effective April 10, up from the earlier 34%. 'Finally' on April 9, Trump increased addtional tariffs on China to 125%, or total tariffs 145% (125% + the original 20%). On the same day, China filed a new complaint with the World Trade Organization after the US raised tariffs to 125%. This escalating tit-for-tat has led to a breakdown in negotiations, with little sign of an immediate resolution or a diplomatic entente between the two countries.

Apart from China, most countries hit by the news US tariffs are leaving room open for talks with the Trump administration. Taiwan, which faces a 32% US tariff on its goods, one of the highest rates among major economies, opted not to retaliate immediately. Instead, it announced plans to engage in discussions with the US to seek an tariff exemption or adjustment. With its pivotal role in the semiconductor and AI chip industries, Taiwan prioritized supporting its high-tech sectors, particularly companies like TSMC. While semiconductors were initially excluded from the US tariff list, Taiwan acknowledged its dependence on the US market for its tech products.

So far, the EU has responded cautiously to the US's 20% tariff on its goods, which applies to products not covered by the existing 25% import tariffs on steel, aluminum, and cars. The bloc prioritized consultations with the US and prepared contingency plans to support impacted industries. One of the key challenges in formulating a unified response is the uneven impact of the American tariffs across EU member states, with some countries advocating for a stricter stance than others. Germany, the hardest hit in export volume, sent goods worth over $176 million to the US in 2024, accounting for [23% of its total exports](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=USA-EU_-_international_trade_in_goods_statistics). In contrast, countries like the Netherlands, which have a trade deficit with the US, are less affected.

Following a meeting of EU trade ministers in Luxembourg on April 7, the European Commission proposed its first set of retaliatory tariffs of 25% on a range of high-value US imports, specifically targeting the steel and aluminum tariffs imposed by Trump, rather than a broader set of levies. The EU is expected to approve these measures on April 9. While the EU remains open to further discussions, it has warned that if no agreement is reached with the US, it may consider additional actions beyond traditional counter-tariffs on goods. These could include stricter regulations on big tech, delays in business licenses, restrictions on access to public contracts, or limitations on intellectual property rights.

## Understanding GPU/XPU global trade

As previously highlighted, our analysis reveals that certain IT equipment and electronics are exempt from tariffs—a much better outcome than the supply chain feared. The US relies significantly on foreign supply chains, which we explain in detail below.

CPUs and other integrated circuits are exempt under Annex II; however, GPUs and TPUs are primarily manufactured in Taiwan and these items are not exempt under Annex II. But there are many other steps to take before having an actual working server—as such, we think it’s possible for servers and components to be re-exported through Mexico and thus be exempt from tariffs under USMCA.

Let’s start with the BoM of a GB200 NVL72 rack. The three primary HTS codes for NVDA GPUs and accelerators are:

- **Digital Processing Units**: Comprises finished AI and traditional servers. The category also includes desktop and workstation units, in addition to certain embedded processing modules.
- **Automatic Data Processing Units**: NVIDIA’s classification system indicates HGX server baseboards are imported under this category. More broadly, thin clients, docking stations, and other auxiliary devices are included in this category.
- **Parts & Accessories for ADP Machines & Units**: NVDA imports GB200 baseboards, NVL boards, and RTX under this code. This is the code under which standalone components seem to be imported. Motherboards, GPUs, accelerator cards, and other add-ins make up a large portion of import value. Also included here are memory modules, cables, connectors, chassis parts, power supplies, and more components **when shipped separately**.

As shown below, final servers and server parts & accessories are the primary ways of importing components in the US. Nvidia is the primary driver of the large increase in 2024.

![](https://substack-post-media.s3.amazonaws.com/public/images/39ed5ee1-5610-4ff7-bc16-4f16dd37ed56_1331x759.png)
*Source: Census Bureau, SemiAnalysis*

Looking deeper, Mexico is the largest import hub of finished servers. Historically, 75%-80% of servers were imported from Mexico. Taiwan took share from Mexico in 2023 and 2024, as Mexico’s share fell to ~2/3. This might suggest that while most CPU servers are shipped from Mexico, Taiwan’s share of GPU servers is higher. However, Mexico seemingly has the capacity given YTD 2025 data suggests that Mexican supply chains are reacting to tariff risk.

![](https://substack-post-media.s3.amazonaws.com/public/images/7d2037e5-90da-4d38-ae51-500c4d6d44da_1216x639.png)
*Source: Census Bureau, SemiAnalysis*

“Parts and accessories” reveal a much higher dependence on Asia. Taiwan dominates, but China is a significant player, too. Given the increasing mix shift to GB200, NVIDIA imports may shift more towards Taiwan moving forward. However, given the USMCA driven loophole, the supply chain may try to re-export these components through Mexico to incur zero tariffs.

![](https://substack-post-media.s3.amazonaws.com/public/images/c8cb1e57-d832-4fc3-93f2-3fd5bb2db5c0_1217x638.png)
*Source: Census Bureau, SemiAnalysis*

Finally, the “automatic data processing units” rely even more on Taiwan—but Mexico’s share is rising fast.

![](https://substack-post-media.s3.amazonaws.com/public/images/ec07e880-4a58-4d53-b628-7c33fcf1eaa3_1124x637.png)
*Source: Census Bureau, SemiAnalysis*

The total import volume of data processing machines and related equipment to the US grew +73% y/y in 2024 to $127B, with the majority coming from Mexico and Taiwan.

## **Board level and rack assembly for Nvidia and its partners**

The assembly of NVIDIA's AI servers, including the Oberon and HGX series, is handled by a network of partners, including Foxconn, Wistron, Wiwynn, Quanta, and Supermicro. Notably, a significant portion of these assembly operations for servers destined for the US market takes place in Mexico. On that point, Foxconn is currently building a $900mm assembly plant in Mexico specifically for GB200 servers that is expected to be operational by early 2026.

Here is a quick recap on the supply chain flow of Nvidia's Oberon and HGX products.

1. The GPU packages are shipped from TSMC to FII (Foxconn) and Wistron for board assembly.
2. Wistron and FII assemble the GPUs onto different configurations of boards, including HGX universal baseboard (UBB) and Bianca board (GB200).
3. The boards are then sold back to Nvidia by Wistron and FII.
4. Nvidia sells the boards to different ODM's for [L6-L11 assembly](https://www.amax.com/server-manufacturing-levels-defined/), where they assemble the boards into GPU server chassis and racks.

**L6** **Board level SMT (likely falls under Parts & Accessories)** is done by two players in two locations**:**

- Wistron: Taiwan, Mexico
- Foxconn: Taiwan, Mexico

**L6-L11** **Rack level**: There are five major ODMs with capacity across Taiwan, Mexico, and the US.

- Foxconn: Taiwan, US (Austin), Mexico
- Quanta: Taiwan, US
- Wistron: Taiwan, US
- Wiwynn: Mexico (the most exposed to Mexico)
- Supermicro: US mostly and some Asia exposure

We believe NVlink components within the GB200 racks are also exempted from tariffs via Mexico due to the same reason as GPUs. Although the cables and connectors from Amphenol are manufactured in China, the final assembly of these cables and connectors into the NVlink backplane are done in Mexico by FII.

The miscellaneous components (power, cooling, and cables) within the IT rack are primarily sourced from Southeast Asia and Taiwan, with some exposure to China. However, **most of the supply chain has moved out of China as part of the China +1 strategy**. Although these components may not be exempted from tariffs via USMCA, they are less than 8% of the BoM cost of GB200. Hence, we believe the tariffs impact from these components will be insignificant.

**AMD** benefits from standalone CPUs which are exempt from tariffs as noted above. AMD relies on major server OEMs (HPE, Dell, Lenovo) who we believe have moved their manufacturing of AMD-based servers to Mexico and the U.S., thereby indirectly “near-shoring” AMD’s end products. AMD does some GPU packaging with Amkor and server assembly with Wiwynn in Malaysia. These products can be utilized for ex-US sales, but would be subject to tariffs if sold to US customers.

**Amazon** engages ODMs for board and rack level assembly of Trainium 2. Amazon utilizes **Accton** for L6 board assembly in Taiwan and **Wiwynn** for L6-L11 rack assembly in Mexico. Flex and Jabil are also starting to ramp in the rack assembly supply chain. As such, Marvell and Amazon should be less impacted as Trainium 2 systems should be able to be exempt from tariffs given the USMCA loophole.

**Google** partners with **Celestica** for its TPU server assembly at the board and rack level. Celestica has board assembly capacity in Mexico and rack level integration in the US. As such, the tariffs impact to the TPU beneficiaries, Broadcom and Celestica should be minimal as well.

## Datacenter impact – rising construction costs

Datacenter construction costs are set to rise, but the industry will likely be able to absorb the impact. 70% of the bill of materials is driven by a broad range of [cooling](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/) and [electrical](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/) equipment. Refer to our deep dives for more information. These industrial goods are highly reliant on global trade – either through direct imports, or via raw materials and finished subcomponents.

![](https://substack-post-media.s3.amazonaws.com/public/images/e49c0b4c-fcd3-4662-97d6-d41bd5fe1657_2182x1366.png)
*Source: SemiAnalysis Datacenter Model*

However, we don’t think Trump tariffs are fatal to the datacenter industry for two main reasons:

1. While cooling & electrical are ~70% of datacenter CapEx, this includes a substantial services portion, primarily related to installation costs. Equipment-only is typically 50% or less, depending on the design.
2. Datacenter costs (i.e. monthly leasing rate per kW) as a % of a GPU cluster TCO are a minor portion. TCO is dominated by capital costs.

Even if we assume a 15% increase to the colocation leasing cost to compensate for tariffs (which is an upper-case scenario), the TCO of operating a GPU cluster only increases by 2%. The vast majority of costs are driven by server costs.

![](https://substack-post-media.s3.amazonaws.com/public/images/afd4d963-da43-46cc-b4dc-4be443b6797c_1970x518.png)
*Source: AI Cloud TCO Model*

We show below a scenario where a flat 20% tariff rate is introduced globally. We estimate that electrical & cooling costs (70% of datacenter BoM) would increase by mid-to-high single digits. This is not insignificant, but we don’t think this poses a major issue to GPU Cloud providers, given the TCO dynamics dominated by hardware capital costs.

![](https://substack-post-media.s3.amazonaws.com/public/images/22e8ec87-e348-4807-bfd5-cc433453acea_1744x754.png)
*Source: SemiAnalysis Datacenter Model*

Hyperscale data centers generally purchase high-end, high-capacity components that tend to have a higher range of domestic production vs imports. Schneider Electric, the world’s leading equipment supplier for datacenters, disclosed that 83% of its North American COGS are not imported (Mexico & Canada excluded from this number).

![](https://substack-post-media.s3.amazonaws.com/public/images/0e64456d-605e-4197-8213-38fa5825d294_2324x1306.png)
*Source: Schneider Electric*

Let’s now analyze individual components.

## **UPS System**

UPS systems are the most negatively impacted by tariffs – not surprising, as they are the most electronics-heavy component. We estimate that less than 50% of large UPS systems for data centers are assembled domestically. Leading suppliers like Eaton, Vertiv and Schneider Electric have a sizeable portion of assembly in the US, while also importing from their Mexican and Asian manufacturing plants. Other large suppliers with a high share of exports to the US include Delta Electronics, ABB, and Mitsubishi Electric. The Taiwan supply chain is particularly strong within hyperscale self-build datacenters.

Even if the system is domestically assembled, many components are imported:

- Battery cabinet: Li-ion cells typically represent ~25% of a UPS module's cost and are largely imported from South Korea, Japan, and China.
- Power semis such as IGBTs are another 10-15% item with a very high import share from Asia and Europe.
- Magnetic components enclosures and wiring make up the remaining portion. While they rely on global commodities, the systems are commonly assembled domestically. Some cheap subcomponents come from Asia.

We show below a breakdown of US imports – but this is a broad category and includes other power electronics systems, such as inverters used alongside solar panels.

![](https://substack-post-media.s3.amazonaws.com/public/images/50e45d0d-f3db-43b1-8fcb-04627f6166b3_1602x946.png)
*Source: Census Bureau, SemiAnalysis Datacenter Model*

## **Switchgear**

A high portion of metal-enclosed LV and MV switchgear used in US hyperscale data centers is assembled domestically by Eaton, Schneider, Siemens, etc. Given their weight, it is not practical to import them – with Mexico and Canada being the key importing hubs. However, inside these systems, several components are imported:

- Circuit breakers are the highest-ticket items (~30% of COGS) and their share of imports is not insignificant. Latin America shines again, while Europe and Asia are also large hubs.
- The share of imports coming from Asia in subcomponents like relays and instrument transformers is quite high.
- Like UPS, enclosures and internal wiring are a sizeable portion of the BoM and are largely assembled domestically.

![](https://substack-post-media.s3.amazonaws.com/public/images/1f3d7f1e-3178-4f99-9d64-f5b0090d2efd_1273x803.png)
*Source: Census bureau, SemiAnalysis Datacenter Model*

## **Diesel generators**

Generators are the least impacted by tariffs. The domestic share of assembly is extremely high, and the manufacturer typically builds the most expensive component – the engine. Alternators are the other large COGS item, and the share of imports is higher, with Europe claiming the top spot.

![](https://substack-post-media.s3.amazonaws.com/public/images/78c04fa5-b86c-460e-bbdc-8e7b3af479ac_1427x1166.png)
*Source: Census bureau, SemiAnalysis Datacenter Model*

## **Transformers**

US datacenters require two types of transformers: high power units (50-10 MVA) for the on-site substation(s), and small standardized transformers (2-3 MVA) found near the building or inside the premises.

- High-power transformers are ~80% imported, primarily due to the lack of GOES (Grain-Oriented Electrical Steel) manufacturing. Mexico, Canada, and South Korea are the primary trade partners.
- MV/LV transformers are much more commonly manufactured domestically—north of 50%—with most imports coming from Mexico and other Latin American countries, as well as South Korea.

![](https://substack-post-media.s3.amazonaws.com/public/images/5a707a1b-4517-41d6-b980-4cd61e4e18c1_1923x1195.png)
*Source: Census Bureau, SemiAnalysis Datacenter Model*

## **Air-cooled chillers**

While there are many different cooling configurations, air-cooled chillers are the most common type found in modern large datacenters. Domestic assembly is significant, but some components are highly reliant on imports:

- The compressor is typically the most expensive component, and in-house production by large manufacturers like Johnson Controls, Vertiv and Carrier is common.
- Heat exchangers found inside chillers (the evaporator and the consender) are also largely built in-house.
- Fans and motors are much more reliant on foreign countries, with Germany, China and Japan leading the charge.

![](https://substack-post-media.s3.amazonaws.com/public/images/a7345d34-60f7-493f-8f91-f3ba84a58413_1564x1169.png)
*Source: Census Bureau, SemiAnalysis Datacenter Model*

## Optical & Networking: supply chain highly exposed to Asia

## **Optical modules**

Optical modules are significantly affected by tariffs as most of their production takes place overseas. AAOI is probably the only Tier 2 vendor that has some production in the U.S. and no Tier 1 vendors have meaningful capacity domestically. Currently, the main importing regions include Thailand, Vietnam, China, Taiwan, Malaysia, and Mexico, each facing different tariff rates based on the initial tariff announcement on Apr 2nd, – Thailand at 37%, Vietnam 46%, China 145%, Taiwan 32%, Malaysia 24%, and Mexico 0% (if at least 50% of the net costs are sourced from Mexico).

Based on these initially announced tariff rates and each region’s share of imports to U.S. in the segment, we estimated the blended tariff rate for optical modules to be 40%, or 27% (ex-China). While these figures are quite high, we believe it is likely that negotiations between the U.S. and other countries will lead to revised tariff rates post the 90-day grace period, resulting in lower effective tariff rates than the ones currently outlined.

![](https://substack-post-media.s3.amazonaws.com/public/images/f4a01b92-6286-449a-adc3-de5cb8b8d986_1059x540.png)
*Source: Census Bureau, SemiAnalysis Networking Industry Model*

Another risk for the optical module sector is that it has high import exposure to China. Although China accounts for just c.14% of optical module imports in 2024 according to the US Census Bureau, many major Chinese module companies have set up factories in foreign countries – like Vietnam, Mexico, Thailand, and Malaysia – as a strategic move to mitigate risks from U.S. trade restrictions. These four countries collectively represent c.60% U.S. imports of optical transceivers and connectivity components in 2024. For instance, Thailand has become one of the top destinations:

- **Innolight**: began setting up manufacturing facilities in Thailand around 2–3 years ago, about 100 kilometers north of Bangkok. The site has now reached a relatively mature stage, with production efficiency and yield rates at 90–95% of those in its China-based factories. Thailand currently accounts for roughly half of Innolight’s total production capacity. Typically, the PCBA (the electrical part) is produced in China and then shipped to Thailand, where the remaining components are sourced, and the final assembly takes place. Labor costs in Thailand remain lower than in China
- **Eoptolink**: also has a production facility in Thailand, located about 100 kilometers south of Bangkok. Currently, the site has limited capacity and is leased rather than owned. The facility primarily handles simpler manufacturing tasks and accounts for a small portion of the firm’s overall production at present. However, Eoptolink has acquired a sizable plot of land near this leased location, aiming for a significant expansion in Thailand. Construction progress has been relatively slow though, and it may take some time before the new factory fully commences operations
- **TFC Optical**: established its Thailand facility around mid-2024, located ~50-60 kilometers south of Bangkok

With the U.S. moving to impose new tariffs, countries like Thailand could also potentially face high tariff rates. We anticipate a period of uncertainty ahead, as companies reassess and adapt their supply strategies to determine cost-effective way to serve the U.S. market – the largest for optical modules.

## **Lasers (EML/ VCSEL/ CW)**

Lasers and modulators are critical components that enable the transmission (Tx) function in optical modules. Major producers typically adopt an IDM model. For example, Lumentum handles the entire production of its EMLs in its own fabs in the U.S. – from front-end wafer processing steps like MOCVD, lithography, and dicing to back-end reliability and performance testing – without relying on external partners. For its CW lasers, which are less technically demanding than EMLs, Lumentum performs all front-end wafer processing steps in its own fabs in the U.S., while back-end processes such as dicing and packaging are carried out at its own facilities in Thailand.

Lumentum operates a single fab for laser diode production, located in San Jose, U.S., which means its EML/VCSEL sales are not affected by tariffs. However, for CW lasers, if the company continues to perform the back-end processes in Thailand, they will be subject to tariffs for Thailand if shipped directly to U.S. for assemblying into modules.

Other major EML and VCSEL producers include Coherent and Broadcom. Coherent operates 10 fabs related to laser production - 6 in the U.S. and 4 in Europe (Sweden * 2, Switzerland, and England). This allows the company to shift production to the U.S. if necessary to avoid tariffs. Broadcom has three laser-related fabs, two located in Singapore – subject to a 10% tariff – and one in the U.S.

The supply chain for CW lasers is more geographically diverse. Key vendors outside the U.S. include Furukawa (Japan), Landmark (Taiwan), Yuanjie (China), and Shijia (China). Landmark manages the entire front-end process—wafer fabrication, dicing, and testing—in-house (in Taiwan) and, due to capacity constraints, sends a portion of wafers to China for back-end processing (dicing and testing).

Another important consideration is that lasers are not standalone end products – they must be assembled into optical modules or engines to become useful for data center connectivity. As a result, lasers are indirectly subject to tariffs based on the final exporting locations.

## **Switches**

Switch ASICs are typically manufactured in TSMC’s leading-edge fabs, using advanced process nodes. Companies like Arista, Celestica, and Accton lead in switch system design and manufacturing, but they can rely on contract manufacturers for product assembly. These contract manufacturers are typically based in places like Vietnam, Thailand, Malaysia, Mexico, Taiwan, and China, and are thus subject to tariffs in respective countries or regions. In the paid subscriber section below, we’ll have a more detailed analysis of the regional supply chain landscape for CPO (co-packaged optics) switches.

![](https://substack-post-media.s3.amazonaws.com/public/images/fae9dcb7-b600-400f-bd76-47c55780a7bf_1111x595.png)
*Source: Census Bureau, SemiAnalysis Networking Industry Model*

## Semiconductor Equipment

The new tariffs make the U.S. less competitive in chip manufacturing. Given the risk concentration in Taiwan, specifically for advanced logic and packaging, the U.S. has a strong and immediate need for policy that *encourages* its domestic semiconductor supply chain, not discourages it.

For fabs, the tariffs make the U.S. versus Taiwan cost delta *worse*. Our model shows that a leading-edge logic or DRAM fab is roughly 15% more expensive just for equipment, excluding any change in construction costs. Operating costs will also grow as many key raw material inputs are only produced abroad. Assuming these costs are passed directly to customers, the premium on a U.S.-based chip is well over 32% versus the identical product from Taiwan. With the Taiwan tariff rate at 32%, a chip produced in Taiwan and subject to tariffs will still be cheaper than one produced in a new-build U.S. fab.

![](https://substack-post-media.s3.amazonaws.com/public/images/f7a95e15-c0f5-43d2-95fb-db58de69a073_1276x684.png)
*Source: usatrade.census.gov, SemiAnalysis Wafer Fab Equipment Model*

Many critical wafer production tools are only available as imports for U.S. fabs. ASML and TEL are the two most important foreign suppliers.

![](https://substack-post-media.s3.amazonaws.com/public/images/8aea4ba8-40a8-449c-9e86-58c58665fd76_1270x672.png)
*Source: usatrade.census.gov, SemiAnalysis Wafer Fab Equipment Model*

The U.S. has effectively no domestic capacity to produce 300mm wafer blanks.

![](https://substack-post-media.s3.amazonaws.com/public/images/c79f4ed4-ee58-45cf-bd4f-ad9d113bf18b_1273x671.png)
*Source: usatrade.census.gov, SemiAnalysis Wafer Fab Equipment Model*

U.S. fabs rely almost entirely on photoresist imports from Japan.

Some may mistake this as an argument that the Taiwan tariff rate is not high enough. This is wrong, as raising that rate kneecaps U.S. companies’ incentive to build AI data centers onshore and generally decreases U.S. access to advanced semiconductors, the lifeblood of the modern world.

![](https://substack-post-media.s3.amazonaws.com/public/images/46d0494d-7a88-4ccf-8565-88754b5640a3_1265x663.png)
*Source: usatrade.census.gov, SemiAnalysis Wafer Fab Equipment Model*

The U.S. imports billions in semiconductors, all (except Mexico & Canada) now subject to tariffs.

Domestic companies building fabs in the U.S. do benefit. Intel Foundry’s advanced processes will be more cost-competitive with TSMC offerings to U.S. customers, although IFS will also see a ~15% increase in WFE costs. However, this advantage is only for products sold in the U.S. The overall incentive is for customers to avoid importing into the U.S. whenever possible.

Intel may see a boost to advanced packaging if the USMCA re-export loophole is closed. Porting a packaging design between vendors is easier than a chip design and avoids tariffs on the 10-20% value added by packaging. Intel’s AP business is already profitable as of 3Q24 and is expected to reach $1B this year, driven by AI customers.

We’ll discuss specific impacts and potential winners and losers by company after the paywall.

## Could retaliatory tariffs impact Big Tech's international operations?

Traditionally, tariffs only impact physical goods crossing borders – with services being exempted. In the case of digital services, even if governments were to try to impose tariffs, there is no good mechanism in place tax bits of data moving across a network. This of course is highly advantageous to the US, as its share of global datacenter capacity is significantly higher than its share of global GDP. Simply put, America is a net exporter of computing power.

![](https://substack-post-media.s3.amazonaws.com/public/images/5daa4aaf-1935-4501-9e29-9eb3ab8f1f91_726x369.png)
*Source: Census bureau, SemiAnalysis Datacenter Model*

After Trump’s April announcements, European leaders have openly discussed targeting Big Tech as retaliation – led by France, who took the most aggressive rhetoric towards the US. Three ways of targeting Big Tech have been broadly discussed:

- Digital Services Taxes (DSTs).
- Market, data and antitrust regulations such as Digital Markets act (DMA – focused on competition) and Digital Services act (DSA – focused on content moderation).
- New laws & tools such as the Anti-Coercion Instrument (ACI).

Using existing laws such as DMA and SDA is the most unlikely scenario. They are aimed to be objectives rules and not to be used as bargaining chips. The latter might weaken their existing litigations with tech firms.

Taxes are the most likely outcome. Major economies have introduced DSTs over the last few years. France introduced a DST in 2019, forcing Big Tech to pay 3% of their gross revenues generated locally. Two main activities are impacted: “Digital intermediation platforms” (i.e., online marketplaces) and “target digital advertising.” Google, Meta, and Amazon have been the most impacted firms.

- Only firms with annual revenues above 750M€ globally and 25M€ in France from the covered digital services are liable.
- The tax is separate from corporate income tax.
- Note that Cloud Computing businesses are **not** impacted.

In Europe, other have introduced similar taxes. The effect has typically been a net cost increase for the end customers:

- In France, Amazon’s online marketplace raise its rate by 3%, from 15% to 15.45%, effective October 1st, 2019. Amazon protected its margin, and small businesses ended up as primary losers.
- Similarly, Google introduced a “regulatory operating cost” surcharge of 2% to compensate the impact and protect its margin.

Therefore, while taxing Big Tech is a standard narrative, it tends to impact end users rather than large corporations themselves and can be seen as the country effectively increasing its tax rate on local businesses. So far, network effects have proven too strong.

In addition, taxing at the EU level could prove challenging, as it requires all EU countries to agree on a joint policy.

## **Cloud Computing taxing and EU’s ACI**

For EU policymakers, the next step would be to expand taxes to Cloud Computing. While Europe does have a sizeable data center market, it remains inferior to its potential, based on Europe’s share of the Cloud Services spending (IaaS/PaaS).

![](https://substack-post-media.s3.amazonaws.com/public/images/82084496-857e-4051-aa10-aed39e8bfaf2_1511x875.png)
*Source: Census bureau, SemiAnalysis Datacenter Model*

To retaliate against tariffs and other “economic coercion”, the EU introduced the Anti-Coercion Instrument (ACI) in 2023. China’s coercion of Lithuania in 2021-22 was a key trigger, but the tool is yet to be used. ACI gives the European Commission power to propose retaliatory measures  and enact them if a qualified majority of member states is approving, such as: tariffs, import/export restrictions on goods and services, foreign investment and capital restrictions, public procurement exclusions, etc.

For the Union, ACI’s power resides in its ability to restrict or impose tariffs on **services** in a lawful manner. While the EU has a €198.2B trade surplus sin goods with the US, its trade of services results in a €109B deficit -driven by financial services as well as digital services. Regarding Cloud specifically, the following retaliatory measures could be introduced:

- Public procurement ban for Cloud Services
- Stricter data localization & protection rules
- Service usage fee or tax
- Suspension of operating licenses – the worst case scenario.

The takeaway is that Europe has the tools to retaliate against the US. While it may hurt its local economy and might simply lead CSPs to increase their prices, this might be the start of a new era with data sovereignty and locality rising in importance.

In the following section, we take a higher-level view on the impact of Trump tariffs and how it could impact the AI infrastructure investment cycle. We also show deeper supply chain datapoints and analyze individual companies and highlight the players with the best position to navigate through the tariff chaos.

## How the tariff-driven uncertainty could impact the AI infrastructure investment cycle

---
title: "Datacenter Anatomy Part 2 – Cooling Systems"
subtitle: "L2A, L2L, Immersion, Two-Phase, Google vs Meta vs Microsoft vs Amazon Water Cooling Design, WUE, PUE, Nvidia Rubin Power & Cooling Architecture"
date: 2025-02-13
source: https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Daniel Nishball", "Reyk Knuhtsen"]
tags: ["Datacenter", "Hardware Architecture"]
audience: only_paid
paywalled: true
---

# Datacenter Anatomy Part 2 – Cooling Systems

**L2A, L2L, Immersion, Two-Phase, Google vs Meta vs Microsoft vs Amazon Water Cooling Design, WUE, PUE, Nvidia Rubin Power & Cooling Architecture**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Cluster deployments are an order of magnitude larger in scale with [Gigawatt-scale datacenters coming online at full capacity much faster than most believe.](https://semianalysis.com/datacenter-industry-model/) As such, there are considerable design changes that Datacenter developers planning future sites must consider. We previously covered the [Electrical system of Datacenters](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/) and how the rise of Generative AI is impacting datacenter design and equipment suppliers. In the second part of this series exploring Datacenter infrastructure and technologies, we’ll focus on Cooling Systems.

Nvidia shook the entire Datacenter Industry in [March when it announced that its state-of-the-art AI computing platform](https://www.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing) would be a 120kW, 72-GPU rack exclusively cooled via Direct-to-Chip Liquid Cooling (DLC). The [Nvidia GB200 NVL72 system will provide the best TCO for Large Language Model (LLM) inference](https://semianalysis.com/2024/04/10/nvidia-blackwell-perf-tco-analysis/) and training, and will be instrumental towards enabling advancement according to [scaling laws](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/) and [reductions in costs of reasoning models like o3](https://semianalysis.com/2024/12/25/nvidias-christmas-present-gb300-b300-reasoning-inference-amazon-memory-supply-chain/). As such, the GB200 NVL36/72 will be the [highest volume SKU of the Blackwell product family](https://semianalysis.com/accelerator-industry-model/) – and this is just the beginning of Nvidia’s extremely ambitious roadmap.

![](https://substack-post-media.s3.amazonaws.com/public/images/f7108144-2a57-4f8a-b820-db5381afce35_1024x414.png)
*Source: SemiAnalysis Datacenter Model*

DLC is not a new technology, but it has long been confined to cost-insensitive R&D government supercomputers that operate at >100kW rack density - and [Google's custom AI infrastructure](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy). In the broader market, rack density has been rising slowly over time, from at most 5-10kW per rack in the 2010s up to the 15-20kW that is typical for modern Cloud Computing datacenters. The Hyperscale era caused an increase in scale of operations, but the underlying Datacenter design was fundamentally unchanged.

## The Upcoming Datacenter Cooling Market

Of the key datacenter systems, Cooling is arguably the area that is evolving at the fastest pace, presents the steepest learning curve and carries the execution risk for datacenter operators. With large-scale projects commonly requiring billions in capital expenditure, the stakes are extremely high. Rapid advancement in datacenter requirements also amplifies the risk of developing assets that could become obsolete quickly.

Demand for Liquid Cooling is underestimated and will lead to an increase in inefficient “bridge” solutions as there won’t be enough liquid-cooling capable datacenters. To quantify this, we built a [chip-by-chip model](https://semianalysis.com/accelerator-industry-model/) and forecast of the Liquid Cooling market, and [location-by-location tracker of future datacenter capacity](https://semianalysis.com/datacenter-industry-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/26e83220-36dc-45f8-bef3-91ba8ca912ff_1642x867.png)
*Source: SemiAnalysis Datacenter Model*

This report is a comprehensive primer on Datacenter cooling systems. In the first section, we explain the basic concepts underlying Datacenter cooling and introduce key equipment. The second part of the report focuses on current Hyperscaler self-build designs and explains their methodology to achieve best-in-class cooling efficiency - [informed by real-time imagery of their flagship AI Datacenters](https://semianalysis.com/datacenter-industry-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/32cb508a-3638-4bb4-aa1f-f032ec4478c1_1024x587.png)
*Source: SemiAnalysis Datacenter Model*

We will also discuss the future of Datacenter cooling with Nvidia’s roadmap and that of its key customers. We’ll explain how each hyperscaler has adapted to market conditions and their considerable design shifts to adapt their infrastructure to the GenAI era. Each hyperscaler has taken a different approach and reviewing them has interesting supply chain implications. We will also discuss Oracle and Bytedance in Malaysia.

Finally, we’ll discuss key suppliers and the impact on their business. Nvidia’s massive ramp is causing shortages on components that on first glance look simple such as Quick Disconnects! While all firms will benefit from the underestimated Datacenter CapEx boom, there are relative winners and losers based on underlying design changes.

## Datacenter Cooling Basics

Thirty years ago, datacenter HVAC (Heating, Ventilation, Air Conditioning) resembled that of office buildings, reusing office or commercial style equipment with beefed-up AC (Air Conditioning) and/or AHUs (Air Handling Unit). But with modern datacenters generating >50x the amount of heat per square feet compared to an office and commonly requiring north of 30MW of power delivery to IT equipment (all converted into heat), the industry transitioned to much more specialized solutions. These sophisticated systems aim to maintain IT equipment at optimal temperatures – for example between 5°C and 30°C for the DGX H100. Operating outside this range would reduce equipment lifespan—which is economically unsound since servers and associated hardware represent the largest portion of a datacenter's total cost of ownership.

![](https://substack-post-media.s3.amazonaws.com/public/images/3cdf6c0b-b8b6-4769-aa0d-63ef8df5db44_2202x708.png)
*Source: Nvidia*

In today's datacenters, cooling systems represent the second-largest capital expense after electrical systems (excluding IT equipment). They've become perhaps the most critical design consideration due to their architectural variety and significant impact on operating expenses, particularly energy - the largest variable cost for a Cloud Service Provider (CSP). Electricity consumption related to non-IT equipment, of which the majority is cooling, is purely a non-productive expense which should be minimized – but there are tradeoffs.

![](https://substack-post-media.s3.amazonaws.com/public/images/638df528-29b5-41f1-aa7e-76efdec81e66_2427x1804.png)
*Source: SemiAnalysis Datacenter Model*

## **Cooling Systems and Energy Efficiency**

The industry standard for comparing facility energy efficiency is the Power Usage Effectiveness (PUE) ratio, which divides total facility power by total IT power. A PUE of 1.5 means that for each Watt of IT load, the datacenter will consume an extra 0.5 Watts for cooling, power conversion losses and other minor items like lighting.

The industry average PUE, calculated by the Uptime Institute, is around 1.6. While many analysts and marketing charts take that number at face value, it is not representative of the industry – it is based on a survey that largely excludes hyperscalers and is a simple average of respondents with datacenters bigger than 4MW. Google and Meta both operate at around 1.1 PUE, and Microsoft and AWS around 1.15 PUE – we’ll explore later in the report how they achieve it.

![](https://substack-post-media.s3.amazonaws.com/public/images/3ece32c3-b004-47d3-994a-a1c3071a1821_1564x1312.png)
*Source: Uptime Institute*

It's important to note that PUE can be manipulated and doesn't always enable fair comparisons. For example, server fan power is generally included within IT load. This means that when comparing otherwise identical air-cooled and liquid-cooled server, the latter might show a higher PUE despite consuming less total power, due to lower server fan power. Alternative metrics have been proposed, but PUE remains the industry standard.

As a rule of thumb, non-IT electricity consumption typically breaks down as follows:

- 60-80%: Cooling system, primarily chillers, followed by fans and pumps.
- 15-30%: [Electrical system](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/) - mainly UPS power conversion, power distribution losses and transformer inefficiency.
- 5-20%: Lighting and other - datacenters often include a small office area.

## **Air-Cooled Datacenter Architecture**

Let’s now explore common designs found in Colocation datacenters. The main cooling components are an indoor cooling unit for the data hall, chillers and cooling towards. In some cases the chiller and cooling tower may be integrated. These components work together through isolated liquid circuits to transfer heat efficiently.

![](https://substack-post-media.s3.amazonaws.com/public/images/b0eba30b-cf7e-431b-a82b-aac10c2900f8_1200x668.jpeg)
*Source: Accuspeclnc*
![](https://substack-post-media.s3.amazonaws.com/public/images/6e3ac764-1315-451c-88b0-b7482aad5932_1712x1140.png)
*Source: Mitsubishi Heavy Industries*

In a datacenter, heat flows from the IT equipment to the outside environment in the following way:

- At the rack level, IT equipment generates heat, which is displaced via fans inside IT servers. This hot air is blown into the data hall.
- Indoors cooling units - commonly CRACs (“Computer Room Air Conditioner”) or CRAHs (“Compute Room Air Handler”) – remove heat from the data hall. Cold water (or another fluid) circulates inside the cooling coil of these units. Hot return air is blown over these coils, transferring its heat into the facility water, which is then pumped back to the chiller.

![](https://substack-post-media.s3.amazonaws.com/public/images/6c1f7eb2-5b83-4c34-8293-27baca7e0c6b_660x340.png)
*Source: MEPacademy*

- The chiller performs a refrigeration cycle - an energy-intensive process to lower temperature. This involves transferring heat from water to a separate fluid called a “refrigerant”. The warmed-up refrigerant is compressed to further increase its temperature and flows through a heat exchanger called a condenser – either air-cooled with fans expelling heat onto the outside air or water-cooled with a separate cooling loop linked to a cooling tower. The refrigerant’s temperature drops in the condenser and returns much cooler. The cooling tower then finally exchanges heat from the condenser water into the outside environment.
- With heat removed from the data hall, the cycle starts again, with cooled water supplied to the indoors cooling unit. This continuous process requires varying amounts of energy and water, depending on system design.

![](https://substack-post-media.s3.amazonaws.com/public/images/cd8444e2-c6e6-412a-b1fb-17f49ba843a1_1423x1100.png)
*Source: Alpine Intel*

Let’s now zoom into the individual components of cooling systems in each loop.

## **Server Thermal Management and Airflow**

The heat flow starts in the data hall, where IT Equipment generates heat as a direct byproduct of electrical power consumption—one kilowatt of electricity powering IT equipment produces approximately one kilowatt of heat. Chipmakers specify the maximum heat a chip or system can handle through its Thermal Design Power (TDP), which guides thermal engineers in designing appropriate cooling solutions. Over the past 5-10 years, chip TDP has shown a consistent upward trend. With AI accelerators, this trajectory continues to steepen, [with 1500W chips shipping next year](https://semianalysis.com/datacenter-industry-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/f0a88ffc-36a9-4535-984e-ade19beac708_1614x1110.png)
*Source: SemiAnalysis*

Starting from the chip, in an air-cooled server, a Thermal Interface Material (TIM) sits atop the die, conducting heat from the chip package itself to the heat spreader or heat sink.

![](https://substack-post-media.s3.amazonaws.com/public/images/47eb8352-e3f6-4c10-9c6c-97c73df1bbbc_1296x389.webp)
*Source: TSMC*

In air-cooled servers, a Thermal Interface Material (TIM) sits atop the die, conducting heat to the heat spreader or heat sink. Heat sinks increase surface area to reduce heat flux (heat per unit area), thereby improving cooling performance. Higher chip heat generation necessitates larger heat sinks, as exemplified by the oversized heat sink on the NVIDIA H100 (700W TDP). These oversized heat sinks are one reason why and Nvidia H100 server is typically 8 rack units (RUs), while a much lower power CPU server can fit within a 1U or 2U form factor.

![](https://substack-post-media.s3.amazonaws.com/public/images/bfaeba0a-4f6e-45cb-b4dc-9dc108a45185_1170x663.jpeg)
*Source: SVA.de*

Server fans evacuate the combined heat generated by internal components, with GPUs and CPUs contributing the largest portion for a typical H100 server. There must be sufficient airflow to remove heat from the heat sinks – an airflow of 165 to 170 cubic feet per minute (CFM) per kW of heat is a common rule of thumb that can be used.

![](https://substack-post-media.s3.amazonaws.com/public/images/92c7f31f-cc67-4e8a-9787-f89c59f2e513_880x880.png)
*Source: Gigabyte*

Server fans can consume significant power, which led hyperscalers to design custom servers instead purchasing off-the-shelf solutions from vendors like Dell or Supermicro. Recent data from Nebius, a [Neocloud](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/) with hyperscale-level resources, demonstrates how custom server designs can reduce energy consumption.

![](https://substack-post-media.s3.amazonaws.com/public/images/a18fb645-442f-48fe-950c-1d04edb1978f_1454x548.png)
*Source: Nebius at OCP Global Summit 2024*

The relationship between temperature and energy consumption is governed by **Delta T**—the difference between inlet temperature (entering the server) and outlet temperature. Delta T influences energy consumption in the following  ways:

- In a cooling system, a higher temperature differential means that less airflow or pumping power is required to dissipate heat – the relationship is linear.
- Although the airflow required may vary linearly with delta T, the energy required to achieve a different airflow does not scale linearly. According to Fan Law physics, fan energy consumption equals fan speed cubed; a 10% reduction in fan speed (i.e. airflow) yields a 27% energy consumption reduction.
- Higher chip utilization rates prove more energy efficient, as increased heat generation creates a larger Delta T for outlet temperature relative to inlet temperature.

## **Anatomy of an Energy-Inefficient Cooling System**

Let’s now dig more into typical operating temperatures and their critical role in the design and efficiency of cooling system. The picture below shows how a traditional “inefficient” air-cooled Datacenter operates:

- Server inlet air at 22°C – the temperature at which air enters the server.
- Chilled water temperature at 7°C in the indoor cooling unit coils, rising to 13°C after heat absorption – a delta T of 6°C at the air handling unit.
- In most global locations, cooling water down to 7°C requires substantial electricity, primarily for the chiller's refrigeration cycle. Such a low chilled water temperature is inherited from office or commercial HVAC systems. The energy cost from chilling water to such a low temperature far exceeds savings from reduced server fan speeds.

![](https://substack-post-media.s3.amazonaws.com/public/images/ca3bc359-eb1d-46e0-9a62-42a3d56c1f62_1289x741.png)
*Source: Supermicro at Hot Chips 2024*

Over the past decade, datacenter operators have increasingly adopted higher inlet temperatures – well above 22°C, discovering that this approach doesn't actually compromise IT equipment longevity. The below table from ASHRAE, an American HVAC standards institute, shows recommends dry bulb (i.e. air) temperature between 18°C to 27°C for servers. However, going above 30°C is allowable and air temperature can even be set as high as 45°C in some cases – although the server class “A4” is more for military-like applications.

![](https://substack-post-media.s3.amazonaws.com/public/images/f1f904e1-3789-43c2-af51-d9cca0c881a5_919x1201.png)
*Source = ASHRAE*

Examining the Supermicro diagram raises an important question: Why does 7°C inlet water into the data hall air handling unit produce a 22°C  server air inlet temperature )? This significant temperature gap often results from poor airflow management. Upsite Technologies developed the concept of the"Four Delta Ts" to deconstruct this gap into a few discrete Delta Ts across different areas of the data hall:

![](https://substack-post-media.s3.amazonaws.com/public/images/d43baf68-278f-4b86-a56e-69aea5d6cd05_504x360.png)
*Source: Upsite*

1. The temperature difference between server input air and return air.
2. Data Hall Air Turbulence/mixing Delta T from Air Turbulence/Mixing: A negative differential caused by hot return air mixing with cold supply air within the data hall.
3. Data Hall Air Handling Unit Delta T: temperature difference between the cooling coil’s inlet temperature and cool return air temperature after heat absorption.
4. Secondary Air Mixing Delta T: A positive differential caused by the cool return air mixing with hot exhaust air. Minimizing this differential ensures that inlet cold air maintains its temperature through efficient airflow management. Note that the image shows a Raised Floor, but this isn’t popular in Modern Datacenters due to limited cooling capacity (airflow) and cost.

To reduce “air mixing,” we use Containment systems to isolate air. The below image shows Hot Aisle containment, but Cold Aisle containment also exists and is in theory equally as efficient. Hot Aisle containment requires a specific ceiling design which is not suited for retrofits, while Cold Aisle containment makes maintenance harder (as the room is very warm), leading to some operators deploying it inefficiently. Modern greenfield datacenters generally use Hot Aisle Containment.

![](https://substack-post-media.s3.amazonaws.com/public/images/e926ca9a-1f67-4a5a-8742-e362fb741511_945x518.png)
*Source: Smart Data Center Insights*

Note that airflow management is complex and can be highly optimized through Computational Fluid Modeling (CFD), an analysis of physical properties like velocity, pressure, viscosity, density, temperature, etc. Sophisticated operators like hyperscalers rely heavily on CFD to reduce required airflow. These optimizations can have significant results - recall that Fan Law physics state that a reduction of airflow translates into a cubed reduction of energy consumption.

## **Indoor Cooling Unit**

The next item on our roadmap is the cooling unit used within the data hall. The most common options are CRAC (Computer Room Air Conditioner), CRAH (Computer Room Air Handler) and Fan Wall units. Direct Expansion (DX) units are an option but their use is far less common. Here are their key distinctions:

- A CRAC is a full Air Conditioner system that uses a refrigerant cycle (much like a home air conditioning system). It is a simple two-piece system, where each CRAC unit inside the room is paired with a condenser unit outside of the data hall. Cooling capacity (up to 100kW) and energy efficiency are low. This is popular in legacy or very small datacenters.

![](https://substack-post-media.s3.amazonaws.com/public/images/94700fd7-2bde-4afd-a7aa-ec99ef5a7921_2166x706.png)
*Source = Schneider Electric*

- The main alternative is a “centralized” system where multiple “CRAH” units are linked to a central facility water. While a CRAC unit uses refrigerant to exchange heat from the unit to an outside cooling unit, a CRAH uses facility water to remove heat from the unit to either a chiller or a cooling tower. A larger piping and pumping system across the whole Datacenter is required when using CRAH units, but there are fewer moving parts in total and the economics are better for a large Datacenter.

![](https://substack-post-media.s3.amazonaws.com/public/images/d5a84a77-8fb3-49bc-b9aa-327ba1c67850_1578x1050.png)
*Source: Schneider Electric*

- Modern Datacenters use Fan Walls instead of CRAHs due to the higher capacity per unit of fan wall, typically 500-600kW. The form factor of a fan wall can be better suited to data hall designs as units can be stacked on top of each other to provide enough airflow for a full 5-10MW data hall. Fan walls also remove the need for a raised floor and perforated tiles to deliver cold air to the racks. While CRAH units intake hot return air from the top of the unit, a fan wall intakes hot air from the back of the unit – typically a mechanical corridor. The hot air from the data hall will travel through a ceiling into that corridor.

![](https://substack-post-media.s3.amazonaws.com/public/images/4fc6be82-8f2f-4d3b-a12f-2a124fc8f7da_1200x668.jpeg)
*Source = Accuspeclnc*

CRAHs/CRACs/Fan Walls are typically set up with [N+1 or N+2 redundancy in a Tier 3 equivalent data center](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/#datacenter-basics), but the pipes connecting the air handlers to facility water are typically in a 2N configuration to allow isolation for faults or maintenance.

Another indoor cooling unit that has seen its popularity increase is the Rear-Door Heat Exchanger (RDHx) – which conceptually can be thought of as an in-rack CRAH, despite many depicting this as “liquid cooling” for marketing purposes. An RDHx is a door placed on each rack with a radiator, in which cold water flows and absorbs the heat expelled by air-cooled servers. This partially or completely removes the need for room-level airflow management and cooling.

A rack using RDHx typically has a cooling capacity of 30-40kW – this can be increased to >50kW by adding fans to the rear door – referred to as an Active RDHx.

![](https://substack-post-media.s3.amazonaws.com/public/images/28add5e1-32df-4647-ad2f-5caf77f3b281_1210x815.png)
*Source: nVent*

RDHx has gained popularity with increasing rack density, and we know of multiple Nvidia H100/H200 deployments using these systems, such as xAI’s massive cluster in Memphis, Tennessee – using RDHx combined with DLC.

![](https://substack-post-media.s3.amazonaws.com/public/images/3b39c801-f3b4-4b4e-90f7-e7c53cd95838_2287x1323.png)
*Source: ServeTheHome*

One of the advantages of RDHx is the physical proximity to the heat source, increasing Heat Exchanger effectiveness – the ratio of real heat transfer to maximal heat transfer. The ratio can be around 0.8 for an RDHx compared to 0.6-0.7 for room solutions like CRAH and Fan Wall. All else equal, this enables a slightly higher chiller inlet temperature i.e. lower chiller energy consumption.

The two main disadvantages are cost and fan power. Physically, one large fan is more efficient than multiple small fans, as airflow is proportional to the cube of the fan diameter. With the increased number of moving parts compared to central room solutions, CapEx is higher as well. In some cases – especially when only a portion of the room is cooled via RDHx – a Coolant Distribution Unit (CDU) is introduced to improve control over the liquid flow rate, temperature, pressure drop etc. This further increases the CapEx differential.

![](https://substack-post-media.s3.amazonaws.com/public/images/95a2adf9-9122-4c54-8d88-68773a362853_2416x1280.png)
*Source: Meta*

A CDU is a simple system and its key components are a Liquid-to-Liquid Heat Exchanger, pumps, and control electronics. It exchanges heat between an inner cooling loop that connects to IT equipment and an outer cooling loop connected to the central facility water system and handles multiple racks. A CDU typical has a capacity greater than 1MW – but there are many variants which we’ll explore later in the report when discussing DLC.

![](https://substack-post-media.s3.amazonaws.com/public/images/ad0bd677-01f7-4e94-8056-b752a3e74a14_2297x1210.png)
*Source: Dafnia*

## **Air-Cooled and Water-Cooled Chillers**

Let’s now discuss chillers, typically the single most energy-intensive component of a Datacenter (excluding IT Equipment). A chiller is essentially a large-scale refrigerator, performing the full refrigeration cycle. The key to any refrigeration cycle is the compressor. Two physical phenomena are at play here:

1. Vapor can absorb more heat than liquid
2. Temperature and pressure have a linear relationship in a closed system, i.e. the higher the pressure, the higher the temperature. A chiller’s refrigeration cycle works as follows:

   - Inside a chiller flows a “refrigerant”: a specific fluid (e.g., R134a or R123ze) with a much lower boiling point than water, to take advantage of the 1st property (vapor absorbs more heat than liquid).
   - A chiller has two heat exchangers, the “evaporator” and the “condenser”. In the evaporator, the fluid refrigerant absorbs heat from the indoors cooling unit and evaporates, turns into gas/vapor.
   - The refrigerant in vapor form then goes through a compressor, significantly increasing pressure and temperature. The hotter the refrigerant, the greater its capacity to transfer heat.
   - In the condenser, the high-pressure and high temperature refrigerant transfers heat to a separate medium – typically air (i.e. air-cooled chiller) or water – the latter involves a separate cooling loop with a cooling tower.
   - An expansion valve reduces pressure and thereby temperature – the refrigerant returns to a liquid state at a very low temperature.

![](https://substack-post-media.s3.amazonaws.com/public/images/72292567-8c3e-4ef5-a0dd-55e7ab0977ab_2110x1234.png)
*Source: District Heating and Cooling Systems*

The compressor is the key component, and its performance directly impacts cooling capacity - increasing the refrigerant's temperature before it enters the condenser requires more compressor energy (higher pressure).

Now, let's explore the two primary types of chillers used in data centers: air-cooled and water-cooled, starting with the latter. The fundamental difference between the two lies in the condenser and how heat is rejected from the system.

A water-cooled chiller is a large unit typically sitting inside the premises in a dedicated room, called the Mechanical Room, alongside large pumps. Its Condenser unit is a Liquid-to-Liquid tube heat exchanger, transferring heat from the refrigerant to a separate cooling circuit. The latter is connected to cooling tower located outside the premises – on the roof or next to the building.

![](https://substack-post-media.s3.amazonaws.com/public/images/512c95c4-a86d-4354-9627-6f5f247f0027_1712x1140.png)
*Source = Mitsubishi Heavy Industries*

One convenient feature of water-cooled chillers (centrifugal type in particular) is their large cooling capacity: Chiller capacity is usually measured in Refrigerant Tons (RT, one RT = 12,000 British Thermal Units per Hour or 3.517 kW). In large datacenters, it is common to see chillers with a capacity of 15MW (~4250 RT) or even up to 20MW per unit! Thus, just a few chiller units are required to cool a large facility, and they generally sit in the same mechanical room. On the flip side, consolidating cooling within a few large chillers requires larger piping across the Datacenter.

These units are typically quite energy-efficient, with a Coefficient of Performance (COP = chiller energy requirement divided by cooling capacity) around 7x, depending on outdoors conditions and Delta T (it can vary a lot).

Given their size, these units lack operational flexibility—frequent cycling on and off proves highly inefficient, even when external conditions might permit operation without mechanical cooling. This is why Variable Frequency Drives have been increasingly popular. Variable Frequency Drivers are a power electronics system converting AC to DC and then DC back to AC via a programmable inverter, allowing precise control over the voltage supplied to the chiller motor as well as enabling precise adjustment of the water flow rate pumped back to the data halls.

![](https://substack-post-media.s3.amazonaws.com/public/images/42f23dbf-1bf9-43a1-be6e-b228864af6af_1210x854.png)
*Source: YORK*

A water-cooled chiller works in tandem with cooling towers, of which there are two main types: dry and wet. The latter, also known as Evaporation Towers, are open-loop systems spraying water from the condenser loop into a specific material (a “fill”). Cooling capacity is increased through evaporation, but water consumption is substantial, and a dedicated water treatment plant is typically required.

![](https://substack-post-media.s3.amazonaws.com/public/images/c4fa1f99-9fd6-46b8-b4ca-89478c7c618d_2637x1403.png)
*Source: The Engineering Mindset*

Water evaporation enables a drop in temperature from dry bulb to wet bulb as heat energy is absorbed in order to affect the water’s phase change to a vapor. This reduces– the load on the chiller’s compressor. As per the below chart, the magnitude of the temperature reduction has an inverse relationship with humidity. Cooling towers perform best in arid regions, like Arizona, while warm and humid locations like Singapore prove more challenging.

![](https://substack-post-media.s3.amazonaws.com/public/images/640a12c2-3de5-42a4-b858-f77d512a46b8_605x485.jpeg)
*Source: Ariel’s Checklist*

A single datacenter evaporation tower can typically cool ~7-8MW for large units – with common flow rates around 5,000 GPM (gallons per minute).

![](https://semianalysis.com/datacenter-industry-model/)
*Source: SemiAnalysis Datacenter Model*

Tesla is building even bigger towers in its [Giga Austin datacenter](https://semianalysis.com/datacenter-industry-model/), where each tower is a one-to-one match with a chiller and can cool north of 10MW!

![](https://substack-post-media.s3.amazonaws.com/public/images/7cbaa4a9-d1aa-438f-b6d5-ee08f264b518_2063x1270.png)
*Source: Brad Sloan*

An alternative to the evaporation tower is to use a dry cooling tower (or “dry cooler”). This is known as a closed-loop system (i.e. no water loss) with the water flowing through a coil and cooled by a fan. This does not benefit from the lower Wet Bulb temperature, but doesn’t consume water, which is cheap but can be scarce and may involves permits and face local protests and political issues. The largest units can cool up to 2MW but require more than 20 fans.

![](https://substack-post-media.s3.amazonaws.com/public/images/a8810d31-a56e-4d3a-89d9-4e2e2d22d8cd_2680x1403.png)
*Source: The Engineering Mindset*

## **Water Usage, Air Cooled Chillers and Dry Coolers**

The main issue with Wet Cooling towers is the elevated water usage, which delays projects in water-constrained locations or datacenter-heavy areas (such as “Data Center Alley” in Ashburn, Northern Virginia). A metric commonly used is the WUE ratio (Water Usage Effectiveness), expressed in Liters per kWh – simply put, how many liters are needed for each kWh of energy. The below report from the US Department of Energy provides some good estimates – a large-scale datacenter with a water-cooled chiller system can have a WUE north of 2L/kWh.

- For a 50MW Datacenter operating at 60% utilization and a PUE of 1.25, a 2.0 WUE means 657M liters of water per year (174M gallons of water per year).
- Note that we will discuss below what airside and waterside economizers are.

![](https://substack-post-media.s3.amazonaws.com/public/images/bab8d08a-b5e3-4f79-8eaa-5ed11c2284c5_1210x898.png)
*Source: US Department of Energy*

Air-cooled chillers have gained significant traction over the last few years due to their better energy efficiency and amid rising water constraints. A system based on air-cooled chillers is simpler compared to water-cooled alternatives, as the chiller is located outdoors and acts both as a chiller and cooling tower – with fans blowing air onto the condenser to evacuate heat. Modern systems integrate various sensors and controls, as well as a VFD, to automatically adjust the power of the compressor, or turn it off, if the outside air is cold enough.

This QTS datacenter (48MW of IT Capacity) has multiple air-cooled chillers on the roof –this is a common design among large 3rd party operators such as NTT or Digital Realty.

![](https://substack-post-media.s3.amazonaws.com/public/images/f81415c0-e306-411e-b326-726f6702138b_1210x428.png)
*Source = Google Earth*

Air-cooled chillers can also be placed on the ground, next to the datacenter. In Memphis, xAI actually deployed both open-loop cooling towers (likely with water-cooled chillers inside the premises) and air-cooled chillers outside!

![](https://substack-post-media.s3.amazonaws.com/public/images/4e7e7e2e-43ec-4252-9012-0d490a649a8b_1024x502.png)
*Source: SemiAnalysis Datacenter Model*

These units have a lower capacity and are less efficient than water-cooled chillers: the below example from the Schneider catalogue shows the specs of a modern air-cooled chiller. The largest SKU has 18 fans and can cool up to 2MW – and that unit requires 500kW of power, or a 4x energy efficiency ratio, when the outside air is 35°C, input water is 20°C and return water is at 30°C.

![](https://substack-post-media.s3.amazonaws.com/public/images/8ee98986-7508-446f-89b0-f4195094bba1_1210x298.png)
*Source = Schneider*

To increase energy efficiency of air-cooled chillers and dry coolers, an option that has largely risen in popularity is adiabatic cooling. It involves adding a layer called “pre-cooling pad”: water is sprayed on the cooling pad, and subsequently evaporates, extracting heat from the surrounding air, thereby reducing ambient temperature (wet bulb vs dry bulb) and increasing efficiency of the system. This enables a reduction in compressor power for an air-cooled chiller. The adiabatic spray can be turned off as well if the ambient temperature is cool enough, or if there is a high humidity level reducing its efficiency.

![](https://substack-post-media.s3.amazonaws.com/public/images/1acb39c2-bfed-406a-a647-61f05878c049_1210x598.png)
*Source = SPX Cooling*

Lastly, let’s briefly discuss the concept of Heat Reuse. On paper, the solution is very attractive – it involves transferring heat to a third party (i.e. a nearby city, for example), thereby significantly reducing the cooling requirements, and potentially monetizing heat. Hyperscale datacenters could theoretically serve tens of thousands of households! According to Microsoft, the Energy Reuse Factor (reused energy / datacenter electrical energy) could be up to 69% in the winter and 86% in the summer.

![](https://substack-post-media.s3.amazonaws.com/public/images/5f7024d2-26b4-4c12-af09-f5fc7f334e7b_1210x611.png)
*Source: Microsoft*

The concept is popular in Europe, and a few datacenters already operate such systems – with Equinix famously powering the 2024 Olympics swimming pool in Paris with a nearby datacenter. Some countries like Germany are pushing this on a regulatory level to meet their sustainability goals.

The diagram below depicts Nebius’ system in Finland near Manstala:

- Heat generated by servers inside the datacenter goes through a heat exchanger and into a central Heating station – typically operated by city officials.
- If more heat is needed, the station will use its own HVAC system such as Heat Pumps to further increase temperature.
- Heat can then be delivered to households.

![](https://substack-post-media.s3.amazonaws.com/public/images/4838d6fa-4ced-4893-9c8c-9d1e565efd3b_1280x540.jpeg)
*Source: Nebius*

While attractive on paper, there are many practical limitations such as proximity to households and availability of required infrastructure.

## **A Look at Hyperscaler Designs and Their Ultra-Low-PUE Systems**

Hyperscalers generally deploy standardized datacenter designs to increase time-to-market, facilitate logistics and reduce costs. Unlike colocation providers who must build designs that meet a broad set of current requirements and possible future requirements from diverse customers, as a sole tenant, Hyperscalers can create efficient designs that cater to specific internal workloads. These datacenters can achieve PUEs generally between 1.1 and 1.2 – mostly through a combination of “Free Cooling” techniques, higher IT equipment operating temperature, and deep CFD analysis.

Before showing actual deployments, let’s discuss some basic concepts. “Free Cooling” or “Economizer” are techniques using the outside environment to cool a datacenter. There are two main techniques, each with multiple variants:

- Airside economizer: Using exterior air to cool the datacenter – this is particularly well suited to areas with a cold climate – eliminating the need for a chiller. This technique can be enhanced with water spraying at the cooling tower.
- Waterside Economizer: For datacenters that do use chillers, a secondary liquid loop that bypasses the chiller’s refrigerant loop. Water goes directly to the cooling tower or dry cooler – but this requires the water temperature to be above the outdoors wet bulb temperature.

![](https://substack-post-media.s3.amazonaws.com/public/images/3d6dc5a1-a91f-49e6-887b-6d53002f38fc_1210x898.png)
*Source: US Department of Energy*

Both techniques only work if the datacenter is in a location with a cold enough outside environment relative to the inlet temperature. The colder the environment, and the hotter the inlet temperature, the better. Hyperscalers play on both sides of the equation. To maximize their use of Free Cooling, they typically operate their servers at above 30°C inlet temperature, even sometimes above 40°C. Their custom server designs can handle this high temperature without degrading performance and life expectancy.

Geography is of course a crucial factor at play. We show below Microsoft’s breakdown of PUE and WUE per Datacenter geography. The worst-case scenario for the use of Free Cooling is a warm and humid climate like Singapore or India.

![](https://substack-post-media.s3.amazonaws.com/public/images/fe68dea0-a18f-43da-81f3-bba36a115889_1210x823.png)
*Source: Microsoft*

## **Microsoft Datacenters and Cooling Systems**

Let’s now look at their actual designs, starting with Microsoft - below is the evolution of their reference design, with the [48MW “Ballard” still being deployed everywhere](https://semianalysis.com/datacenter-industry-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/8c41ef5c-75c1-40be-b38e-dad56edc182a_1210x913.png)
*Source: Microsoft*

Ballard is designed for air-cooling and bypasses the use of chillers. Microsoft uses a system they call “Direct Evaporative Cooling”, shown below. This corresponds to an airside economizer system:

- Exterior Air is filtered and pulled inside the facility with fans.
- If needed, the air will be humidified to lower its temperature.
- Air enters the server room, is warmed up, channeled into the hot aisle, and directed out of the facility via exhaust fans.

![](https://substack-post-media.s3.amazonaws.com/public/images/85a5f4ea-a0c3-4f10-8325-2665761abe9c_1210x1167.png)
*Source: Microsoft*

Microsoft calls this system “Free Air Cooling” when no water evaporation is needed.

![](https://substack-post-media.s3.amazonaws.com/public/images/e657b518-cc9c-4438-be03-8ec8fafd83c8_1210x1154.png)
*Source: Microsoft*

We show below an aerial view of the hot air exhaust system, and the filters letting the outside air get in.

![](https://substack-post-media.s3.amazonaws.com/public/images/cb4e3e23-3148-418e-a0da-1f01f324109e_2246x1514.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/e800325e-e569-41bb-aadb-2d63828c49e0_2050x804.png)
*Source: Google Earth, SemiAnalysis*

This system design avoids the need to use chillers and air-water heat exchangers like CRAHs. The upshot is that with no need to design in air-cooled chillers/dry coolers or cooling towers, the datacenter can have a meaningfully lower CapEx/MW. This system is completely dry – and this specific Datacenter is located near Phoenix, Arizona. While >30°C temperatures are common, the climate in Phoenix is very dry – and the wet bulb temperature can be significantly lower than dry bulb temperature. The drawback is that water evaporation is needed for a large portion of the year, leading Microsoft to post a >2 WUE ratio in Phoenix, despite a company average of 0.3 WUE.

![](https://substack-post-media.s3.amazonaws.com/public/images/9e4199ab-a5cc-404c-8ba0-51d38523291d_1210x637.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/b882e49c-504b-4ef0-8d0a-d88591225dcd_1210x679.png)
*Source: Bing Maps and Google Earth*

Note in the image above, a complete lack of any cooling towers anywhere on this facility, as this datacenter uses Free Cooling.

![](https://substack-post-media.s3.amazonaws.com/public/images/6fbaf7e2-a488-4a9a-9e7e-6cf5667fa453_1210x880.png)

In some areas, climate conditions are not suited to this type of cooling, and Microsoft uses another system called “Indirect Evaporative Cooling” – still without any mechanical cooling but using a dry cooler placed outside.

![](https://substack-post-media.s3.amazonaws.com/public/images/2a0a6882-c72c-4232-9f4c-042a3b608eb6_929x858.png)
*Source: Microsoft*

Below is a satellite view of this system in an Iowa datacenter. Note the fluid cooler and AHU located just outside the facility.

![](https://substack-post-media.s3.amazonaws.com/public/images/a56c854c-18fd-43bb-8733-e188fd8470a8_1210x856.png)
*Source: Google Earth*

## **Meta’s “H”: Efficiency Over Time-to-market**

Meta’s famous “H” design is another interesting case study. Through a combination of Free Cooling and high server inlet temperature, as well as relatively low power density, Meta has been operating datacenters at best-in-class efficiency levels for over a decade. The diagram below depicts their cooling system:  it is very similar to Microsoft’s “Direct Evaporative Cooling” and “Direct Free Cooling”.

![](https://substack-post-media.s3.amazonaws.com/public/images/1c6171d3-d600-4752-8feb-305b64a06841_2548x1152.png)
*Source: Electronics Cooling*

In some climates, Meta adds CRACs to cool down the exterior air in the warmest summer days – in which PUE is likely significantly higher than their company average 1.08.

![](https://substack-post-media.s3.amazonaws.com/public/images/90d749f0-96c1-4021-b3d1-cc12ea8866bb_2162x958.png)
*Source: Google Earth*

In 2018, Meta introduced a variation to enable Free Cooling in climates with higher levels of humidity – such as Singapore. It relies on an air-to-water heat exchanger, with outside air cooling the facility water system, and can be further cooled down with an adiabatic option.

![](https://substack-post-media.s3.amazonaws.com/public/images/6f21ff8d-365d-41e8-abe9-85442be08ac5_2564x1048.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/7bd750c3-8382-4f36-af76-2fb34338a013_2310x1468.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/24ccc387-757e-42ac-8158-a8149fc53a31_2232x1002.png)
*Source: Meta*

Meta’s efficiency levels are impressive (PUE at 1.08 and WUE at 0.20), but this is achieved through a complex, three-level structure. Meta’s “H” is much bigger than competitor’s designs, for a similar or lower power capacity – enabling fans to run at lower speed. [Our real-time and historical satellite imagery reveals that time to complete a shell is typically ~2 years, 2-3x longer than other hyperscalers](https://semianalysis.com/datacenter-industry-model/). Low density and high time-to-market are suboptimal in the AI era, which led [Meta to take the drastic step of scrapping a number of “H”s under construction to replace it with their new AI-ready design](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/#meta-datacenter-scrapped-vertiv-schneider-electric-eaton-legrand-delta-datacenter-bill-of-materials-by-component-transformers-switchgear-redundancy-ups-ocp-busbar-generators-substation) (explored behind paywall).

![](https://substack-post-media.s3.amazonaws.com/public/images/bed9b66f-c9a6-46a5-9141-fbe7886744a2_1122x1286.png)
*Source: Google Earth*

## **Google Datacenters – Energy for Water Tradeoff**

Google’s reference design is very different – while their PUE is best-in-class at 1.10, their use of water is much more extensive with a WUE above 1.0. Google uses a waterside economizer, which typically involve using two separate facility cooling loops – a “chiller” loop performing the refrigeration cycle, and a “heat exchanger loop” with no mechanical cooling. When outside conditions allow it, the datacenter uses only the secondary loop, with water going directly to a cooling tower or dry cooler, bypassing the chiller.

![](https://substack-post-media.s3.amazonaws.com/public/images/78c87d09-fbba-4e3a-bd15-f1ab4ddc36eb_2550x796.png)
*Source: Schneider Electric*

A plate heat exchanger is a system where two fluid loops circulate and exchange heat. Such units are typically quite efficient in terms of Heat Transfer – as a rule of thumb, a loss of 2-3°C is typical, i.e. water coming at 30°C from cooling tower would lose 2°C and transfer 28°C into the indoor cooling unit.

![](https://substack-post-media.s3.amazonaws.com/public/images/2a8167b4-c6be-4acf-b42f-991e374cc726_1210x880.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/34cd3cb4-152e-49e7-9fed-c6cf2f434bd2_605x341.jpeg)
*Source: Alfa Laval*

Google has deployed various types of cooling systems – of which the most impressive is a [Finnish datacenter using sea water](https://www.youtube.com/watch?v=3f0V6_ZFHMk) free cooling, but its most common design relies heavily on evaporative cooling towers. In the below example, three large Data Centers with an IT load of ~200MW share the same centralized cooling infrastructure (we can see the piping), with giant fans on top of the cooling towers. These towers are large two-cell per water-cooled chiller unit, meaning that 28 cells can cool 200MW, or ~7MW per cell. Some designs include water-cooled chillers, but other datacenters are completely “chillerless” – Google has publicly said that their large Belgium campus is chillerless.

![](https://substack-post-media.s3.amazonaws.com/public/images/921f26c3-9884-4a8d-adf2-cee4d1d726fd_964x1127.png)
*Source: SemiAnalysis Datacenter Model*

Lastly, let’s briefly look at AWS Datacenters. The company is less transparent and we have less available information. We show below a campus in Manassas, of which the largest individual building has a critical IT power of 50MW.

![](https://substack-post-media.s3.amazonaws.com/public/images/3ad980bd-b6fc-4585-92e2-12435ecb1bbf_1210x668.png)
*Source: SemiAnalysis Datacenter Model*

We note that there is no apparent outdoors cooling unit (aircooled chiller, dry cooler or cooling tower). We believe that AWS relies on a system very similar to that of Microsoft and Meta – with the exhaust fans on the roof, and louvers to let the exterior air in.

![](https://substack-post-media.s3.amazonaws.com/public/images/fae40254-b70e-47e7-8caa-1fbf7cd2fe75_1386x779.jpeg)
![](https://substack-post-media.s3.amazonaws.com/public/images/8a7020d9-8415-477e-914b-35df5d5cb970_2577x1326.png)
*Source: Amazon*

We have now covered the basics of Datacenter cooling system. Hyperscalers have largely proved wrong the popular narrative that air cooling is not an energy efficient technology. The rise of GenAI changes everything about this framework and challenges existing designs.

Let’s now discuss Nvidia’s roadmap and the near-term and long-term future of Datacenter design, and impact equipment suppliers. We believe that the real drivers behind liquid cooling adoption are still misunderstood, and so is the future of cooling systems for inference vs training datacenters. We’ve often heard that Liquid Cooling adoption is driven by superior energy efficiency, or because cooling >1000W chips with air is not possible. We also commonly hear that Inference will require low-power servers and air cooling.

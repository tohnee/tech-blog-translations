---
title: "The Wild Wild West Of LEGO Datacenters"
subtitle: "Everyone Says They're Modular, Do The Vendor Claims Hold Up? Zuck's Tents, AWS's Houdini, 60GW+ Modular Capacity Tracked, Full Vendor Landscape Mapping, Vertiv's 2x Content Uplift Per MW"
date: 2026-07-29
source: https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters
crawled: 2026-09-15
authors: ["Nicolas Bontigui", "Eric (Junqi) Wen", "Jeremie Eliahou Ontiveros", "Nigel Chiang", "Reyk Knuhtsen", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# The Wild Wild West Of LEGO Datacenters

**Everyone Says They're Modular, Do The Vendor Claims Hold Up? Zuck's Tents, AWS's Houdini, 60GW+ Modular Capacity Tracked, Full Vendor Landscape Mapping, Vertiv's 2x Content Uplift Per MW**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

# The Labor Problem and Modularization to the Rescue

Today we dig into the world of datacenter construction, because how datacenters are built now bears little resemblance to how the industry has historically done it. Concrete walls arrive as finished panels, mechanical and electrical rooms arrive wired, and sometimes even entire data halls arrive on the back of a truck. Some of the largest datacenters in the world are increasingly assembled the same way you assemble your new Spider-Man LEGO set, only that the bricks weigh 50,000 pounds and are a tiny bit more complex. This is the world of modular construction.

From Hyperscaler to Colos to now even the AI labs, modular construction has become the default playbook for building fast. Our Modular Tracker, included in our SemiAnalysis [Industrials Model](https://semianalysis.com/industrials-model/), tracks over 61GW of modular capacity and 1,000+ sites using some form of modularization or prefabrication strategy. Full breakdown by modular category and equipment type is included in the [Industrials Model](https://semianalysis.com/industrials-model/). We estimate that modular penetration will reach 30%+ of total live capacity by the end of 2028.

![](https://substack-post-media.s3.amazonaws.com/public/images/33c16231-6f3d-4c90-b750-cdee249d56f4_3354x2153.png)
*Source: SemiAnalysis Industrials Model*

Ultra-fast modular designs are increasingly the norm. [Over a year ago, we were the first to call out Meta’s drastic change to using “tent” buildings](https://newsletter.semianalysis.com/p/meta-superintelligence-leadership-compute-talent-and-data). As shown below, AWS is now rolling out at very large scale their own modular design codenamed “SAMDC”.

![](https://substack-post-media.s3.amazonaws.com/public/images/72654e35-b473-44d9-83d5-93bfd3ffda27_3114x2171.png)
*Source: SemiAnalysis Industrials Model*

To understand the reason, we need to start looking at one of the structural bottlenecks that capitalist incentives alone cannot build past: labor.

Our recent articles have been a journey toward that bottleneck. In “[The Case for Space Datacenters](https://newsletter.semianalysis.com/p/to-boldly-go-the-case-for-space-datacenters)”, we showed the ceiling on terrestrial capacity. Last month, in “[Stop Saying Half of 2026 US Datacenter Capacity Is Canceled](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter)”, we argued that most bottlenecks are misunderstood and solvable. Trade labor is an exception here, as you cannot quickly solve for a shortage of electricians and pipefitters. The race for that talent became a true constraint long ago, visible when operators like Crusoe pumped wages by 30% to bring talent to Abilene’s site, which required over 9,000 workers at its peak.

![](https://substack-post-media.s3.amazonaws.com/public/images/c13c3a8e-bc45-4188-8596-978dd543a131_3450x1920.png)
*Source: SemiAnalysis Industrials Model , US Census Bureau*

Aiming to size the labor shortage trade by trade, we now also include the Labor Model as part of the [Industrials Model](https://semianalysis.com/industrials-model/). It translates the state-by-state buildout from [our Datacenter Model](https://semianalysis.com/datacenter-industry-model/) into hours of demand for every trade and sets them against reachable labor supply. To frame the problem before modularization enters the picture, the chart below is ex-modular construction, with labor demand curve assuming labor per GW stays roughly flat over the forecast period and doesn't yet reflect the benefits we'll cover later in this article. Reachable labor supply in each state, on the other hand, is affected by how much capacity is being built, and how much labor is being pulled, in other US states.

![](https://substack-post-media.s3.amazonaws.com/public/images/d044c040-2aab-4ab9-aa65-be81bd574ece_2200x1240.png)
*Source: SemiAnalysis Industrials Model*

Electricians are a clear case, as they represent 30-40% over the total construction man hours in a datacenter project. The chart below shows an estimated electrician shortage emerging in 2027 driven by the huge mission-critical demand. On a state-by-state basis, the shortage is most acute where the buildout concentrates, like Texas and Ohio.

![](https://substack-post-media.s3.amazonaws.com/public/images/936d8787-b1b0-42eb-a95c-7dee8af1e844_2400x1380.png)
*Source: SemiAnalysis Industrials Model*

The response is that every operator and vendor are now racing toward modularization, which essentially means pulling repeatable work off-site and into factories, where everything from wall panels to power rooms and cooling skids are built in parallel with the site and delivered as finished units. Besides, it does more than ease the labor crunch, promising large speed and time-to-build gains. And today, speed is revenue.

The shift is already underway, with Compass and Switch being the first operators to move parts of their datacenter builds offsite. Using some form of skidded solution for electrical equipment is now pretty standard for every operator. AWS’s Project Houdini prefabricates the white-space buildout and collapses the time before servers go in from months to weeks. Meta is standing up fabric-clad “Tent”-like halls. And a wave of new entrants, both in the OEM and the System Integrator space, are building specifically around modular.

In this deep dive we rebuilt the modular case bottom-up against some of the speed and cost claims made by vendors like Vertiv or Schneider, finding that modular construction can compress the construction window by **~**36%, or 7-9 months, and is **~**8% cheaper on a Capex/MW basis. We also analyze how vendors like Vertiv are able to expand their value capture per project by offering the full stack solution, going from their historical **~$**3.5M/MW content to **~$**7M/MW with the modular solutions.

![](https://substack-post-media.s3.amazonaws.com/public/images/a6a4ecdf-f99a-41bc-a676-b72206c25bdc_2912x1464.png)
*Source: SemiAnalysis Industrials Model*

The problem, though, is that today everything seems to be modular and vendors, EPCs and Colocation providers many cases are describing entirely different things. To bring some order to this wild west, this article unpacks what modular actually means. We map the vendor landscape building a modular universe of more than 80 players and test whether the vendor claims hold up.

For subscribers, we focus on the main beneficiaries and break down how each player is positioned, from the public names (FIX, STRL, PWR, VRT, SU, FLEX…) to private challengers such as Infra Partners, Bladeroom, and Faith Technologies, distilling the key insights from our recent [Core Research](https://semianalysis.com/core-research/) subscriber notes on [Comfort Systems](https://semianalysis.com/institutional/comfort-systems-modular-capex-is-the-moat/): *“Modular Capex Is The Moat”* and [Sterling Infrastructure](https://semianalysis.com/institutional/sterling-infrastructure-winning-where-it-counts-quadrupled-tam-via-texas-pacific-northwest-and-the-midwest-2x-content-per-mw-from-cec-attach-6b-order-run-rate-in-view/): *“Winning Where It Counts: Quadrupled TAM via Texas, Pacific Northwest, and the Midwest; 2X Content per MW from CEC Attach; ~$6B Run-Rate In View”*.

*To start off, we’d like to thank [QTS](https://q.com/), [EdgeConneX](https://www.edgeconnex.com/), [Aligned Data Centers](https://aligneddc.com/), [Schneider Electric](https://www.se.com/ww/en/), [Applied Digital](https://www.applieddigital.com/), [DG Matrix](https://www.dgmatrix.com/), [Aran Industries](https://aranind.com/), [Karman Industries](https://www.karmanindustries.com/), [Radiant](https://radiant.co/), and Rajat Bhagat for their contributions and insights during the preparation of this deep dive.*

# **The Modular Taxonomy**

![](https://substack-post-media.s3.amazonaws.com/public/images/83a11e81-c993-45dd-b237-a716280c1f75_4704x3228.png)
*Source: SemiAnalysis Industrials Model*

Before we go into the detail taxonomy, let’s start with the basic definitions, because two words concepts often get mixed up: prefabrication and modularization.

- **Prefabrication** is the broader concept: any part of the build manufactured offsite and delivered ready to install. It is a statement about where the work happened, not about the shape of the thing.
- **Modular** is narrower. It refers to the actual self-contained units (rooms, boxes, blocks) that ship complete and get bolted together on site. Every modular unit is prefabricated, but prefabrication may not be directly modular.

![](https://substack-post-media.s3.amazonaws.com/public/images/48bf0f7a-3e0d-432a-acb1-3d23459c76ec_2240x944.png)
*Source: SemiAnalysis Industrials Model*

Hold onto that distinction, because it is the spine of everything below. From here on, we will walk through the landscape the way a datacenter is actually built up, then we will go into details on the taxonomy that makes up the modular market starting from the ground up.

## **Understanding The Datacenter Anatomy**

At a high level, a datacenter can be seen as simple three stacks of layers: Site, Shell, and Systems.

At the bottom we have the site, or the physical land of the datacenter buildout. This is where grading, wiring, and foundation building take place. This layer cannot be modularized because you have to physically break ground on a parcel of land and pour foundations into it on the set up.

Above that sits the shell, which means the structure, skin, and roof that serve as the backbone and weatherproof the entire datacenter buildout. Inside the shell is where all the equipment and subsystem, including all the mechanical and electrical systems, sit.

![](https://substack-post-media.s3.amazonaws.com/public/images/9c94a890-e7ae-45f6-9524-7e4b459b869b_2080x960.png)
*Source: SemiAnalysis Industrials Model*

Considering that the site itself can not physically be moved, prefabrication strategies are focused on the other two layers, and we take them in that order, working from the outside in.

## **Modularizing the Datacenter Shell**

The shell is the structure, walls, and roof that hold the datacenter up and keep the weather out. It generally follows either a frame-and-skin design, where the structure and cladding are separate, or a load-bearing panel design that combines both.

In a traditional build, both the skin and the frame need to go up on site. Crews break ground, pour the foundation, then form and cure concrete right where the building stands, one piece at a time. A modular shell starts the same way, on a poured foundation, but from there the structure and panels arrive as finished pieces from a factory, craned and bolted into position once arrived.

![](https://substack-post-media.s3.amazonaws.com/public/images/48f56864-6591-4d77-9e20-396ff5c542f8_1280x500.png)
*Source: SemiAnalysis Industrials Model*

The time saving is evident from the graphic above. In the traditional cast-in-place buildout, each pour has to reach roughly 75% of its design strength before the next can go on top. Prefabricated structure sidesteps that wait.

However, the evolution did not stop with prefabricating the same conventional building. The larger gains now come from simplifying the building itself: moving from complex multistory facilities toward repeatable single-story halls, and then toward narrower, purpose-built structures.

#### **Phase One: Precast Industrialized the Conventional Shell**

The first phase is precast concrete described above. Instead of forming and curing the full structure in the field, panels are manufactured under controlled conditions, transported to the site, and craned onto a prepared foundation.

This is not new. Northern Virginia has used precast extensively for years because construction labor was already constrained. CloudHQ’s two-story LC-2 facility in Ashburn is a representative example: its load-bearing shell supports long, column-free spans and enough structural load to place mechanical equipment on the roof.

![](https://substack-post-media.s3.amazonaws.com/public/images/0c557b56-64e2-4056-8e48-5756a323ac9e_1600x611.png)
*Source: CloudHQ Datacenter Crogan*

Nevertheless, the building still took roughly 18 to 20 months to deliver. Precast reduced field forming and curing, yet the underlying facility remained a large, multistory structure facility.

Tilt-up concrete follows a similar logic but casts the panels on the building slab rather than in a remote factory.

![](https://substack-post-media.s3.amazonaws.com/public/images/a0d53c91-d115-4f7f-a562-6918d230ba17_1023x627.png)
*Source: Tilt up Panels at DPR Construction Ashburn Virginia*

This method avoids long-haul transportation and can be the lowest-cost route for a large single-story box, although quality and schedule remain more exposed to site conditions and weather.

#### **Phase Two: Simplifying the Building**

The second phase is where design changes happen. In order to further speed up the time, the industry turn towards alternating the design for simplicity. These buildings use regular structural bays, fewer architectural features, and standardized exterior panels. Steel is often favored because the frame can be fabricated off site, shipped efficiently, and bolted together quickly across a large flat campus.

At the light end is the pre-engineered metal building, or PEMB built in three parts:

1. The primary frame serving as the structural skeleton
2. The secondary frame tying the main frames together, these are lighter steel member like roof purlins that span between the primary frames.
3. The skin, keep in mind this is different from the frame. They are the thin light weighted metal panel whose job is to protect the interior from extreme weather conditions

![](https://substack-post-media.s3.amazonaws.com/public/images/ca0c2e79-f004-4be7-b272-9750e2d4e799_1920x2560.png)
*Source: Diamond Steel Pre-engineered Metal Building installation*

This is the fastest option since all parts arrive cut, punched, and labeled, a crew simply need to bolt them together on the site. Furthermore, a light steel structure needs far less material than concrete.

More demanding halls use structural steel - heavier, hot-rolled beams and columns fabricated off site and bolted into a rigid frame. It costs more than a light PEMB but supports wider spans, heavier loads, and more complex layouts.

QTS’s Cedar Rapids campus shows the speed and scale this approach can unlock. The current 420 MW phase spans approximately 2.8 million square feet and uses roughly 28,000 tons of structural steel. QTS moved from groundbreaking to topping out in about five months, with the broader building delivered in approximately 11 months.

![](https://substack-post-media.s3.amazonaws.com/public/images/3d4ab1fb-268f-4b91-a4b4-b8d35729f005_1710x824.png)
*Source: SemiAnalysis Industrials Model*

The exterior is then closed with prefabricated cladding, most commonly insulated metal panels. Similarly, we see this approach with Crusoe’s Stargate campus in Abilene, each building used roughly 672 factory-made panels. The panels were fabricated in under 40 days and installed at approximately 15 to 20 per day, helping bring each building to a dried-in shell in under eight weeks.

![](https://substack-post-media.s3.amazonaws.com/public/images/dbb6bdb2-d30d-4dcd-a85e-d59991230758_1200x900.png)
*Source: Crusoe Stargate Campus*

The speed advantage therefore comes less from steel itself than from what it enables: simple single-story halls, repeatable structural bays, fewer field interfaces, and a supply chain that can be reproduced across markets. It can also reduce labor and structural material per MW compared with a dense multistory design.

The main trade-off is land. Single-story campuses require more acreage, but that is often acceptable in newer AI markets where land is cheaper and deployment speed matters more than maximizing MW per acre.

#### **Phase Three: Purpose-Built Rapid-Deployment Shells**

The third phase pushes simplification further by designing the enclosure around a more specific deployment model. Narrower, lighter structures can reduce the amount of conventional shell work and support faster repetition, although tighter optimization may leave less flexibility for future equipment or layout changes.

Meta’s rapid-deployment structures at Prometheus campus in New Albany are the most visible extreme. The aluminum-framed, fabric-clad halls provide enclosure and weather protection without constructing a conventional permanent shell. Each structure is roughly 125,000 square feet, and satellite tracking showed eight standing by April 2026 after the buildout was announced in July 2025.

![](https://substack-post-media.s3.amazonaws.com/public/images/3728a388-fef1-4c9b-a890-451ec148878b_624x315.png)
*Source: SemiAnalysis Datacenter Model , Tent at Meta Prometheus New Albany*

That does not mean Meta completed a full datacenter in nine months. The tents accelerate the enclosure, not utility interconnection, power, cooling, or commissioning. They also trade away some of the durability and long-term flexibility of a permanent concrete or steel building.

AWS is moving in a similar direction with its newest modular builds. Rather than treating the shell as a large generic warehouse, AWS is using narrower and more repeatable structures organized around the systems installed inside. The result is less building per MW, shorter structural spans, and fewer interfaces for field crews to assemble.

![](https://substack-post-media.s3.amazonaws.com/public/images/90b9184f-8001-4766-9168-690cf77e2593_2419x1137.png)
*Source: AWS Multistory Design*

The common thread is that shell modularity is increasingly about design simplification, not just prefabrication. Precast moved concrete production off site but largely preserved the conventional building. Standardized steel made single-story halls easier to repeat across markets. Purpose-built structures go further by reducing the size and complexity of the shell itself.

The cost savings thus come from removing floors, reducing structural complexity, decreasing labor on site, and repeating the same enclosure / supply chain across the campus. Once the shell is dried in, the larger modularization opportunity moves inside, to the power, cooling, and white-space systems that turn the enclosure into an operating datacenter.

## **Modularizing the Equipment and Subsystems**

Equipment and subsystems are where most of the real modularization is happening, and the offerings span an enormous range, from a single piece of equipment all the way up to an entire building delivered ready to switch on. Previous deep dives already covered in big depth the anatomy of [Mechanical](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems) and [Electrical systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical). Besides, before we start naming categories, it helps to fix some vocabularies:

![](https://substack-post-media.s3.amazonaws.com/public/images/db1a1f19-60c9-4c4a-8ac0-7cc51365b99d_2500x937.png)
*Source: SemiAnalysis Industrials Model*

1. **Component:** The lowest level of form factor. It is a single piece of equipment manufactured in a factory.
2. **Skid:** First common modular form. It is a group of components mounted on an open frame. Instead of shipping each piece separately, the equipment is pre-arranged, configured, and shipped together as one package.
3. **Module:** A skid but in an enclosed space. It can go anywhere from a simple power room to a prefab mechanical/electrical room similar to a skid, but only it will become a module if you put walls and roof on top of it.
4. **Container:** A specific form of module using ISO container for packaging. An ISO container is built specifically for standard shipping dimension, which means it can travel anywhere on normal transport with a truck without limitation.
5. **Prefab Datacenter block:** Facility scale buildout that stitches multiple factory-built module into a much larger facility block. The intent of these block is to serve as an end-to-end datacenter buildout

This is like a ladder, from 1-5 increasingly factory integration and scope. If you look carefully, you may also be able to realize the first 4 levels are better known as the subsystem modularization. This is where the supplier delivers one part of the datacenter as a factory-built unit. That unit is arrived assembled and tested, but still has to be connected into the broader facility before it becomes useful.

The last level and sometimes the fourth level, moves closer to a whole facility modularization. Here, the supplier is delivering a much larger portion of datacenter as an integrated product.

![](https://substack-post-media.s3.amazonaws.com/public/images/26cb7a1e-a34d-4c56-97c1-0ae098215b76_1431x560.png)
*Source: SemiAnalysis Industrials Model*

## **Subsystem Modularization**

With the vocabulary in hand, we can now start climbing the ladder, and the natural place to begin is at the bottom, with subsystem modularization. This is the larger of the two families and where most of the market lives today. We start off with the grey space, and modular power block is where most people think of when discussing modular design.

### **Modular Power Blocks**

![](https://substack-post-media.s3.amazonaws.com/public/images/b23b7a03-7d2c-4cd0-b614-42a3ebcfd7ea_1430x842.png)
*Source: SemiAnalysis Industrials Model*

A power module is a factory-built electrical room or power block that packages the major electrical equipment into a containerized box. Among all subsystem modules, power is one of the most natural areas to modularized because the equipment lineup is well defined and lots of different pieces are needed to assemble the units. The electrical fit-out and commissioning take on average 5.5 - 16.7 months on a 50MW power hall.

To illustrate with an example, let’s see Flex’s modular power solution, built through the Anord Mardix unit below:

![](https://substack-post-media.s3.amazonaws.com/public/images/a172dde8-c1a8-45e3-9f02-4d9738d06016_947x503.png)
*Source: Flex*

Flex sells this in two versions, the power skid and the power module pod, which is the same lineup wrapped in a secure enclosure. Inside the room, you will find major electrical components laid out like a power train.

As you may have noticed, the module also contains the busway system like the IBAR feed above the building which bridges the power pod to the data hall. The CRAH units, or computer room air handler and fire protection system, also exist to help manage the air temperature inside the enclosed shell and protection against unexpected conditions.

By our own estimate, the power block is where the schedule payoff concentrates. Moving just the power scope into the factory, roughly ~26% of the build by content, gets a hall to IT-ready ~22% faster, ~13 months against ~16.7 for stick-build, and around ~5% cheaper per MW, largely by compressing the mechanical-and-electrical fit-out from ~5.5 months to ~2.5.

Lastly, within modular power blocks, a new subcategory is emerging, which we can define as “software defined” power routing blocks. Instead of packaging the conventional transformer+switchgear+UPS+battery chain into a box, companies like DG Matrix replace portions of that chain with power-electronics-based multi-port routing. These systems can connect grid, generation, storage, and DC loads through a common controlled power platform.

### **Modular Cooling Blocks and Prefabricated Cooling Infrastructure**

![](https://substack-post-media.s3.amazonaws.com/public/images/5bba9e35-78a3-4d66-94c8-de79f4b2acd8_1430x840.png)
*Source: SemiAnalysis Industrials Model*

Similar to a power module, the cooling block packages the datacenter’s cooling loop into one integrated subsystem. At first glance, the case for modularizing cooling is weaker than for power, since there are simply fewer pieces to pre-assemble. But as primary and secondary loops grow more complex, the ability to add cooling capacity in repeatable, modular increments becomes far more attractive to operators.

Focusing on the TCS loop, the majority of modular efforts are centered on skids for CDUs. Airedale by Modine’s skid-based CDU (for more on cooling systems, [read our Cooling deep dive here](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems)) is an example of this category.

![](https://substack-post-media.s3.amazonaws.com/public/images/18d71a00-7f47-4b7b-8fe1-2d2c4a080714_893x504.jpeg)
*Source: Modine*

The Airedale by Modine skid-based CDU is a 2 MW-class unit arrives on a pre-manufactured skid with everything included, from the red-and-silver cooling loop to the buffer tanks on the top right, and even the leak detection system built into the end of the skid. On site, all the crew needs to do is hook up the two loop connections and a power feed.

On the other hand, the value proposition for prefabricated cooling systems is stronger when looking at the secondary loop and the outdoor mechanical yard, where piping and other outdoor cooling infrastructure is prefabricated, significantly reducing the civil, piping, and controls work completed onsite.

![](https://substack-post-media.s3.amazonaws.com/public/images/b512bc68-64e0-4b33-9da7-eb25bb700acb_1422x1143.png)
*Source: SemiAnalysis Industrials Model*

When thinking about cooling equipment, keep in mind that much of it was originally designed for hospitals, campuses, and industrial process cooling rather than GW-scale datacenters. At that scale, large footprints and hundreds of co-located units can create issues such as hot-air recirculation and heat islanding.

![](https://substack-post-media.s3.amazonaws.com/public/images/298ec60f-d43c-4a44-8901-693927971231_2400x1600.png)
*Source: Vertiv’s elevated chiller/cooling plant on a steel platform beside a prefab hall using mechanical yard infrastructure*

The Vertiv installation above shows a conventional mechanical yard. The cooling plant sits outside the data hall as a separate piece of infrastructure, with chillers, pumps, piping, and supporting steel assembled around the building.

Some datacenter developers, like QTS, are now prefabricating most of the piping infrastructure, which allows for faster installation while maintaining high quality. That becomes especially valuable today, given the increasing piping requirements of dense liquid-cooled deployments.

A handful of new entrants are now even attacking the whole yard. Karman Industries’ CO2-based Heat Processing Unit (HPU) is a purpose-built unit borrowing SiC power electronics and permanent-magnet motors from EVs, and compact turbomachinery and advanced heat exchangers from aerospace. The HPU, which is configurable to each site, ships as an outdoor-rated NEMA skid at 4 to 5 times conventional power density and cuts yard footprint by 60 to 80%.

![](https://substack-post-media.s3.amazonaws.com/public/images/07f5c81d-9a0f-4e02-9fb0-6a079bcbde49_1126x703.png)
*Source: Karman Industries*

## **Other Modularized Options**

Power and cooling are not the only parts of the datacenter that can be move into the factory. The same concept can be apply across the gray space such has the energy storage (BESS) system, water treatment skids, Fire safety system, and many more.

Many are not on the critical path for construction timeline, or they are small enough to be able to build on site. Moreover, where these systems do get modularized, they often ride along inside a large unit rather than shipping separately. For example, the Schneider EcoStruxure for example was built in with the fire protection system.

### **Factory Built White Space**

![](https://substack-post-media.s3.amazonaws.com/public/images/24feeb10-afcc-43d3-ad01-baae3bfb3260_1431x816.png)
*Source: SemiAnalysis Industrials Model*

The intention of the factory built white space module is to replace hand-built data hall and manual on-site wiring with a unit made factory product. This means operator can directly put compute in place without the need to figure out wiring and connection.

The whole package comes ready for the rack frames, and all the last mile connection points the rack need to operate. Think of it like a prepared envelope for compute, its organized where racks go, provide the cable and connection to how they receive power and extract heat, and include prefabricated power busway and technical water loop situated above the rack.

![](https://substack-post-media.s3.amazonaws.com/public/images/1cbdc558-83be-405e-ac77-5440964920ea_2165x543.png)
*Source: Schneider Electric*

Take Schneider’s EcoStruxure Pod as an example. The image above shows the black cabinets forming the IT rack rows where products like Nvidia GPU servers would be installed, a total of up to 40 racks can be placed in this one system. Above the racks, the gray overhead infrastructure is the distribution layer. It carries the busway that delivers power to each rack, containment to capture hot air as some of the solution will still be air cooled, technical water loop to distribute liquid cooling that extracts heat, and cabling that connects each servers.

The interesting thing about this is the product design behind it. A factory white space must be able to serve different custom needs and therefore, suppliers like Schneider work with Nvidia to support more than 30+ reference designs. The buyer can essentially pick the specs that matches the chips it wants and gets a hall that is pre-coordinated with the matching required power and cooling module. In the coming section we will study in more detail how the design process takes place.

## **Whole Facility Modularization**

Whole Facility modularization is the literal datacenter-in-a-box model. Instead of delivering individual parts, the supplier delivers a complete or near-complete datacenter block.

![](https://substack-post-media.s3.amazonaws.com/public/images/53c5b11d-1a27-4a02-b827-8a8ca6b69b5d_2500x937.png)
*Source: SemiAnalysis Industrials Model*

### **Containerized Datacenters**

![](https://substack-post-media.s3.amazonaws.com/public/images/b58d524c-fb6c-4fe5-9f7e-579425b515bc_1430x842.png)
*Source: SemiAnalysis Industrials Model*

Starting with a containerized datacenters, this is the 4th part of the form factor design where the datacenter itself is packaged into an ISO-style container or purpose-built weatherproof enclosure. Like we had discussed, the reason why this option exist is for the ease of transportation.

![](https://substack-post-media.s3.amazonaws.com/public/images/e530d9bf-5ac8-4c91-9e56-07f232123c01_374x248.gif)
*Source: Delta All-In-One Edge Solution*

As the image shown above, you can see almost everything inside the box: the IT racks, the power equipment, the batteries, and even the cooling system.

These types of design are commonly used in edge computing, industrial environments, remote or unused spaces, and the product is most useful when the buyer needs a smaller datacenter quickly. For AI workloads, the buyer is usually not a compute startup chasing scale but an asset owner that needs low-latency inference at a fixed physical location.

![](https://substack-post-media.s3.amazonaws.com/public/images/e3d57cbd-3cb8-405c-a590-efd9c56a31cd_1200x675.png)
*Source: Flex’s CrownPod Craned into site*

The main limitation of this buildout is density. The same form factor that makes the unit portable and fast to deploy also fixes the layout. That’s why suppliers are pushing beyond the containerized model toward all-in-one prefab datacenter blocks.

### **All-in-One Prefab Datacenter Block**

![](https://substack-post-media.s3.amazonaws.com/public/images/a300c885-7b79-4999-a283-c7bc7c824b00_1430x842.png)
*Source: SemiAnalysis Industrials Model*

The all-in-one prefab datacenter block is the more ambitious version of whole-facility modularization. Here the supplier delivers a larger facility block with more of the datacenter already integrated before delivery.

![](https://substack-post-media.s3.amazonaws.com/public/images/de56d565-b8e6-40f4-bc02-ea222bd3062e_1000x1000.png)
*Source: Vertiv*

Vertiv MegaMod shows what this can looks like in practice. The structure effectively is a modular datacenter with the major systems packaged into one enclosure. The center of the block contains the IT racks, where servers are installed. Above and around the racks runs the fiber optics and cable-management pathways, along the perimeter are all the supporting infrastructure systems like cooling and power units.

The system’s 1 MW reference design can stretch to approximately 26.5 meters long, 24 meters wide, and 4 meters high in dimensions. While the MegaMod plus version can extend to as much as 31 meters wide. You may be wondering, if it’s this big how can it be ship to the site? In reality, the structure needs to be broken into transportable prefabricated sections, shipped through a standard heavy-haul logistics truck, and then connected and commissioned as one.

## **Platform Modularization and Reference Designs**

The last step in whole-facility modularization moves beyond any single vendor’s block into a standardized reference design for the facility itself. In the same fashion the industry has reference designs for rack systems and CDUs, Nvidia now publishes one for the entire AI factory: Nvidia DSX. It was first unveiled as an Omniverse digital-twin blueprint at GTC Washington in October 2025, formalized as the Vera Rubin DSX reference design in March 2026, and more recently expanded into the full DSX platform.

The DSX reference designs are validated AI factory architectures covering compute, networking, storage, hardware cluster design, and also the facilities side, including power, cooling and controls. Even civil, structural, and architectural design. The value proposition behind is that Nvidia’s DSX Max-Q maximizes token per watt within a fixed power budget, and DSX Flex facilitates the connection the facility to grid services, dynamically adjusting power draw and orchestrating demand with hybrid onsite generation.

![](https://substack-post-media.s3.amazonaws.com/public/images/5e1de1e0-f8b5-468d-9c6b-ca21d1ae6e56_597x335.jpeg)
*Source: Nvidia Vera Rubin DSX AI Factory*

When deploying a DSX facility, through the Omniverse DSX Blueprint, an operator first builds a digital twin of the facility, simulates layouts, power topologies, thermal behavior, and operational policies in real time, and optimizes the design before construction begins, then reuses the same validated architecture across sites. For example, CoreWeave is already using DSX Air to build and test digital twins of its AI factories.

Besides, the whole DSX ecosystem includes pretty much all the supply chain: Cadence, Dassault Systemes, Eaton, Jacobs, Nscale, Phaidra, Procore, PTC, Schneider Electric, Siemens, Switch, Trane or Vertiv. Vertiv’s OneCore, for example, packages power and cooling into standardized 12.5 MW pods that can be combined into larger AI-factory deployments

EdgeConneX estimates that a common design can advance a project to roughly a 30% to 60% permit set before site-specific localization is complete, allowing substantial off-site work to begin earlier.

# **Vendor landscape**

If you have made it this far, you should have a working feel for the categories. You should also, maybe be a little buried in names. We have put a power module from Flex, a CDU from Airedale, a data-hall pod from Schneider, and an all-in-one datacenter from Vertiv all in front of you. So before going further, it helps to step back and lay the whole market out on a single map.

![](https://substack-post-media.s3.amazonaws.com/public/images/88ea5eee-1d24-497d-a2be-54b6bb9a5c55_2500x2041.png)
*Source: SemiAnalysis Industrials Model*

Our universe runs to over 80 players, and laying them out this way is useful because two patterns jump out right away.

1. **The depth is in the subsystems**. The power-room and cooling modular are by far the most crowded
2. **The same names keep showing up** across columns, because a vendor like Vertiv, Schneider, or Eaton sells a power module, a CDU, a white-space pod, and a whole block all at once.

## **Owning the Integration: Who actually does the modularization?**

The vendor landscape above maps who builds each piece, but not how those pieces become a module or who is on the hook when they do. From the solution provider’s point of view it has three answers:

1. At one end the operator holds both rights: it specifies the equipment, buys it directly, and hands it to an integrator purely for assembly.
2. In the middle sits the EPC- or integrator-led buildout, where the operator still sets the performance requirements but hires an EPC or integrator to source, coordinate, and build.
3. At the far end is the OEM-led model, where a vendor like Vertiv designs and sells its own stack as one finished product, as it does with the OneCore portfolio

![](https://substack-post-media.s3.amazonaws.com/public/images/0115ef28-b275-414a-a678-3115e0f62aff_2500x937.png)
*Source: SemiAnalysis Industrials Model*

### **Operator-Led Modularization**

This is where the operator engineers the specification themself, procures the equipment directly as owner-furnished gear, and hands it to an integrator purely for assembly.

This model requires the operator to have a deep in-house engineering and procurement team to specify and source every component, and the willingness to carry all of the cost, inventory, and lead-time risk.

![](https://substack-post-media.s3.amazonaws.com/public/images/62884260-b354-4fff-a504-fdc00e29f23c_2304x892.png)
*Source: SemiAnalysis Industrials Model*

In a supply-constrained market that risk is sharp, since the operator is competing for scarce transformers and switchgear without a vendor’s allocation leverage, unless it buys at enough scale to have that leverage of its own.

That is why operator-led modular is effectively confined to the largest hyperscalers. AWS, for example, engineers its own prefabricated data-hall skids under Project Houdini and procures the equipment directly, using Cupertino Electric as design partner.

Aligned is another example of operator-led modularization, although it relies on external integration partners for manufacturing capacity. Aligned defines the architecture, owner-furnishes the major components, and controls the commissioning and quality program, while its integration partners receive, store, assemble, and test the equipment across multiple factory locations. The partner provides the production footprint, but the modular system remains Aligned’s design.

### **System-Integrator or EPC-Led Modularization**

The EPC-led modularization includes system integrators or construction companies that take mostly third party equipment and convert it into a skid/module. The integrator does the assembly, installation, factory testing, enclosure, and is the party in charge of delivering the finished skid to the end customer.

The companies acting an integrators are both construction companies that have the footprint and capabilities to do the integration, like Comfort Systems, Sterling Infrastructure or Quanta’s Cupertino Electric, and specialized modular integrators, like PCX, Nautilus, DXN, Infra Partners, Bladeroom, etc.

This type of modularization is vendor agnostic, which means that the customer keeps more control over the datacenter design, while the contractor moves part of the construction sequence into a prefab shop. The EPC buys the equipment, assembles it, wires it, pipes it, tests it, and ships it as completed construction scope.

![](https://substack-post-media.s3.amazonaws.com/public/images/af02689f-123a-4dd5-b425-325162c8710d_2304x892.png)
*Source: SemiAnalysis Industrials Model*

Take Comfort Systems as an example. It is a MEP contractor, not an equipment maker, so it acts as the layer that procures and assembles the gear on the operator’s behalf. The operator decides what equipment it wants and Comfort Systems does everything else. It runs that work through Environmental Air Systems and TAS Energy across 3.5+ million square feet of shop floor in Texas and North Carolina.

That concept is particularly attractive to hyperscalers. A big operator usually already knows exactly what equipment and design it wants, so it has no interest in buying someone else’s fixed system. Working with EPC integrators like the kind for Comfort System, the operator keeps its own design and its own gear, and simply hands the building of it to a factory instead of a jobsite.

### **OEM-Led Modularization**

Here the equipment vendor turns its own datacenter infrastructure stack into a repeatable module or platform. Although the product can still be configured for a specific site, the starting point is usually an off-the-shelf module using OEM’s own architecture.

![](https://substack-post-media.s3.amazonaws.com/public/images/5e0f30ec-073c-4bf6-a1c1-eacaf53cf27b_2304x892.png)
*Source: SemiAnalysis Industrials Model*

Vertiv OneCore is a clear example. Instead of selling single equipment devices, Vertiv combines all the layers into a single modular platform. This platform integrates Vertiv’s power, thermal, cooling, and IT infrastructure technologies inside a Vertiv’s supplied steel shell.

![](https://substack-post-media.s3.amazonaws.com/public/images/04db66d8-dcf4-43da-a099-03a359a69238_447x447.jpeg)
*Source: Vertiv*

That is what makes it OEM-led, the customer is buying into Vertiv’s entire integrated stack rather than asking an EPC integrator to assemble equipment line ups. This also allows Vertiv to capture higher content by selling the entire stack end to end, with the TAM expanding up to ~$7M/MW for some of their full-stack solutions.

The tradeoff is capacity and execution risk. Besides the fact that these companies are going up the value-chain toward market segments they were not previously involved in, OEM-led modularization can only scale as fast as the OEM’s factory capacity, supplier base, and integration teams can support. Vertiv’s modular solutions run lead times of over 12 months today. This is also pushing big OEMs, not only Vertiv but also companies like Schneider and Siemens, to be selective with capacity slot allocation, requiring certain capacity minimums and favoring bigger projects. As a result, operators or developers looking for smaller scale capacity are increasingly working with the System Integrators.

# **The Modularization Cycle**

By now our readers should be familiar with the different forms of modular solutions and the players leading this transformation. They will also have noticed how different this looks compared to traditional datacenter construction, and will have many questions about the operational implications. Those are the topics we address in this section.

![](https://substack-post-media.s3.amazonaws.com/public/images/85b1dd62-b41a-48fe-a5b6-49cba38aa8c5_2400x800.png)
*Source: SemiAnalysis Industrials Model*

## **Stage 1: Solution Design and Simulation**

Engineering the solution is the first step. In a field build, some of these decisions can change while construction is underway. In a modular build however, they need to be predetermined, frozen early, and repeatable since the box itself must come in a finish block.

The most important engineering at this stage happens at the facility level. Before a module can be finalized, the design team must define the load, select the equipment, develop the single-line diagram (SLD) and layout, and complete the short-circuit, protection-coordination, and arc-flash studies in tools like ETAP and PSSE. These analyses determine how the system is sized and which components can be used. Because they depend on the full electrical path from the utility connection through the downstream equipment, they cannot be completed on an isolated skid. The facility design therefore has to come first, with the module designed as part of that broader system.

Source: Aran Industries

For 415/480VAC this work is well templated and repeatable. When considering [all the implications of the 800VDC transition](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part), it is not as well-templated. A handful of reference designs exist, but none are well baked yet, so the facility-level architecture is still being worked out design by design. This is also the part of the cycle now being automated. Companies like Aran Industries are building build custom software that plugs into ETAP, PSCAD, PSSE, Revit and the other design tools, compressing what is otherwise a multi-month (>2 months), multi-engineer electrical design process into hours of compute plus a single engineer reviewing the output.

### **Ownership of the Buildout**

Once the design is set, ownership comes down to two questions:

1. Who chooses the equipment;
2. Who carries the cost, the inventory, and the lead-time risk of the buildout.

Those decisions do not always sit with the same party. An operator may specify a component directly, or an integrator may select it and seek approval.

![](https://substack-post-media.s3.amazonaws.com/public/images/74cebb3e-3b9f-4e0a-ae70-5fd1960a1f06_1200x630.png)
*Source: Schneider’s Factory showcasing different modules*

Colocation operators are a clean exception. A wholesale colo is not bound to any single end-user’s specification, and often does not even know who the tenant will be, so it is free to choose the equipment it wants and commit to it early, without waiting on anyone’s sign-off.

Even then, local availability matters, because switchgear and transformers may carry 12 to 18-month lead times, while generators can require market-specific emissions controls. Customization can also reopen engineering and add roughly eight weeks.

## **Stage 2: Packages and Documentation**

Once the design is frozen in Stage 1, what leaves the design stage is not a single drawing but a set of documentation packages, produced by different parties in different tools:

- An **issued-for-fabrication (IFF) package** with the shop drawings telling the factory how to build the skid
- An **issued-for-construction (IFC) package** telling the site how to receive, place and connect it
- A separate **permitting and commissioning documentation** set, proving the design will pass code and testing.

![](https://substack-post-media.s3.amazonaws.com/public/images/303e91b9-6fe8-4cb7-b1a4-4f95deb64445_2400x904.png)
*Source: SemiAnalysis Industrials Model*

This stage is largely a documentation and paperwork exercise. Automating the Stage-1 design model lets these packages be generated from one source rather than be recreated by hand, removing the manual redrawing between parties (IFF and IFC serve different audiences, the factory and the field, and are issued separately; they are not the same document and do not drift against one another).

## **Stage 3: Assembling the module and Factory Testing**

Once all the prework is completed, the module still has to be physically built. Think of this step as the production line, but in a much bigger scale of a datacenter. The assembly process starts with a base, a skid, or a frame that sets the foundation of the module. From there, equipments are layered in sequence, with each component placed into its designated area like how you will assemble a LEGO building.

![](https://substack-post-media.s3.amazonaws.com/public/images/5450c310-0b3e-4ba8-a843-2f08d95053e7_1000x486.png)
*Source: Flex’s White Space Factory Line*

What runs alongside the assembly is the factory acceptance test, or better known as “FAT”. Testing happens at two levels. The first is at each station as the module is assembled, an inspection gate where the work is checked before the module advances. The second comes once the module is complete: the whole unit is powered up and run the way it will run on site to confirm its rated load and everything is in place properly. By the time it leaves the line, the module is cabled, labeled, sealed, and proven to work on its own.

![](https://substack-post-media.s3.amazonaws.com/public/images/5609f744-8cd1-456b-8538-1b8be45a95a3_800x600.png)
*Source: Vertiv Factory Acceptance Testing*

Factory testing is critical. The industry often describes this through the 1-10-100 rule: a defect that costs $1 to fix during design or assembly may cost $10 once production begins and $100 after the product has shipped. Furthermore, standardization also makes testing repeatable, so same FAT procedures can be run multiple times across production.

## **Stage 4: Delivering and installing the modules**

Now, the module leaves the factory’s controlled environment and runs into the uncontrolled area of site logistics. At the scale of today’s AI campuses, bringing the first block online is no longer enough, because operators also have to think about time to the last megawatt. The critical questions become how many finished modules can reach the site, how many can be unloaded and set in parallel, and how effectively limited rigging and installation crews can move from one block to the next.

### **A closer look at: Transport and Logistics**

In our conversations with datacenter developers, logistics appears as one of the main challenges equipment modularization presents. All these skids and modules are big and heavy, and shipping them from the factory to the site is not a minor task. That is why footprint and location matter so much, with integrators expanding their footprint to sit closer to their customer’s sites.

Federal law fixes the no-permit envelope at 102 inches wide and 80,000 pounds gross, leaving about 24 tons for the module on a standard deck. Microsoft’s Azure Modular Datacenter and Schneider’s Easy Modular ride inside a 40-foot ISO container at 96 inches wide, so they cross any state line or fly in a C-17 permit-free.

Past that threshold, you need a permit, although the truth is that permit cost has little impact and the real implication is on schedule. A standard oversize permit runs just $15-100 a state, and even the line-haul, at $12-14 a loaded mile, makes a 500 mile move only six to seven thousand dollars a trailer.

![](https://substack-post-media.s3.amazonaws.com/public/images/3f165e61-54ec-4b94-9534-82ab4641fc5a_1200x675.png)
*Source: Flex’s Prefabricated modular solution ready to ship*

On time, loads past roughly 16 feet become superloads, triggering a bridge-engineering review that runs 7 to 21 days per state and stacks toward months across a route, and escorts force restricted travel windows. Besides, the thresholds are not even uniform, as a module engineered to clear Virginia (superload at 18 feet or 250,000 pounds) can still trip Ohio’s far lower 14-foot, 120,000-pound line.

Transport also becomes part of the reliability program. A module may experience greater mechanical stress on the road than during normal operation, particularly through vibration, braking, and loading. In one validation exercise, Aligned DC shipped a 3 MW module from Utah to Omaha and back with force loggers to measure the conditions it experienced in transit.

On top of all this, transport can also be constrained by the insurance it carries. High-value AI racks may be shipped only one or two at a time because concentrating too much equipment on a single trailer creates an unacceptable insured loss no insurance company is willing to bet on. The risk is not theoretical and we have heard cases where truck carrying large UPS module tipped over on a road in West Virginia while traveling toward Northern Virginia, leading to large reimbursement.

Considering all these implications, operators are designing around the haul, like AWS engineering Houdini’s skids onto low double-drop trailers to stay under bridges. Also Nautilus floated its datacenter 50 miles to the Port of Stockton on a barge, and Compass put a Schneider module factory next to its Red Oak campus. That said, some operators like DXN do manage to ship containers from their factories in Perth, Western Australia all the way to the US. These are, however, mostly smaller containers.

![](https://substack-post-media.s3.amazonaws.com/public/images/0bd6be86-de2d-4034-8e8f-a10bef3f39a7_2820x1740.png)
*Source: SemiAnalysis Industrials Model*

Once the module reaches the site, it must be lifted onto the prepared foundation, anchored, and connected to upstream power and downstream load. Even crane selection becomes part of the design process. A crawler crane’s lifting capacity falls sharply as the load moves farther from the boom: a Manitowoc 18000 can lift roughly 600 tons at 7.3 meters, but only about 10 tons at 104 meters, so the module’s weight, lifting points, and final landing position determine which crane is required and how much the lift will cost, typically around $5,000 to $25,000 per day. A single Schneider 500 kW power module, for example, weighs 50,000 pounds, needs six lifting points, and its load distribution is not known until it is built.

### **Stage 5: Site Commissioning**

With the modules in place, it’s time to commission them. Factory testing proves the individual unit, while commissioning proves the system under real conditions. Operators consistently call this the single biggest gap in the modular cycle, with a full site commissioning running 3 to 8 months end to end. While some vendors claim it can be shifted offsite, in practice the parts that matter can’t be, because the major energy sources (the utility feed, the generators, the BESS) only meet on site.

#### **The levels of commissioning**

The industry generally runs a 6-level ladder, while some frameworks add a Level 0 design review at the front.

![](https://substack-post-media.s3.amazonaws.com/public/images/d10e9828-816b-44d2-b224-e5a62c1866d0_1800x1696.png)
*Source: SemiAnalysis Industrials Model*

- **L1 - Factory Witness Test (the “red tag”):** each skid or module proven as a standalone unit at the manufacturer. This is the level factory testing covers, and the level modular front loads.
- **L2 - Delivery & installation verification:** the unit is received, set, anchored and inspected on site.
- **L3 - Pre-functional / startup (the “green tag”):** each system energized and started up on its own.
- **L4 - Functional performance testing (the “blue tag”):** each system run to the switchgear, the cooling loop.
- **L5 - Integrated Systems Testing / IST (the “white tag**”): every system energized and running together, on site, under simulated failure, an A-side outage, a UPS/STS transfer, a pump failover, a black-building start.

![](https://substack-post-media.s3.amazonaws.com/public/images/02d31ee5-c418-4fa6-b822-06082f1287b6_937x668.png)
*Source: Hioki Commissioning Steps*

From L2 onward the work has to happen physically on site, because the sources being tested against like utility feed, generators, BESS are only present there.

To understand where time can actually be recovered, we identify two levers. First, parallelize commission modules and subsystems as they land rather than waiting for the whole site, so L2–L4 on the early modules overlap the delivery of later ones and only L5 has to wait for the full set. Second, reuse the plant as its own load bank: the power equipment and its battery storage can serve as the load bank during commissioning, so instead of trucking in rented gensets and resistive banks that leave when the test ends, the same gear that proves the plant stays on as part of it.

![](https://substack-post-media.s3.amazonaws.com/public/images/f57d19e3-88ed-4ede-beec-5a244ab78361_1000x668.png)
*Source: Electrical Engineering Portal, commissioning substation and MV switchgear*

#### **Parallel Factory Commissioning**

At scale the binding constraint is usually the Level 3 point-to-point work, because every PDU, control panel, and field device must be wired, addressed, named, and verified back to the BMS. Across hundreds of PDUs each exposing dozens to hundreds of points, this is the real commissioning bottleneck. To move faster, some big datacenter operators are running parallel factory commissioning tracks alongside the standard on-site process, completing equipment verification and control checks before shipment (repeating some tests post-transport) while the site team keeps delivery checks, live interconnection, and integrated-system testing.

This consideration also matters when studying aggressive project timelines claims. Some 6-9 month schedules are achieved partly by compressing or minimizing the commissioning process. That may accelerate initial turn-up, but it significantly shifts risk into operations.

# **Putting the Value Proposition of Modular Solutions to Test**

All modular pitches mainly rest on three claims: (1) Speed to market; (2) Quality of Build and Safety; and (3) Total Cost of Ownership. The marketed numbers are huge figures, with Vertiv claiming MegaMod at up to 50% faster on module deployment and SmartRun at up to 85%, and Schneider claiming 60% faster and 13% lower first cost on power and cooling.

Those are big (big!) numbers, so we rebuilt the case bottom-up against our baseline reference datacenter that we include in the [SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/), a 50 MW liquid cooled AI hall in the US. As headline, our numbers estimate a ~36% shorter construction window for modular construction when considering the full construction timeline, and a ~8% lower all-in cost. Let’s break down these figures.

![](https://substack-post-media.s3.amazonaws.com/public/images/4ad1bd1f-3c81-4f65-833a-18e7320af078_2912x1344.png)
*Source: SemiAnalysis Industrials Model*

## **The Speed Advantage**

Speed is undoubtedly the core vendor selling point. Following our previous taxonomy, the realized savings will depend a lot on which modular solutions you use in the build. To understand where the speed savings come from, we need to understand the construction timeline in commonly four blocks:

- **Groundworks:** 4-6 months, averaging about 5 months. Modularization changes little here beyond simplifying some pad and foundation work.
- **Structure and shell:** 2.5-4.5 months, with a midpoint of about 3.5 months.
- **Mechanical and electrical fit-out:** 7-11 months. Today’s baseline already includes some preassembled electrical equipment, such as LV switchgear and UPS lineups.
- **Commissioning to IT-ready:** 3-8 months, with a single-hall midpoint of about 4.5 months. Longer timelines usually reflect phased, multi-hall handovers.

Added together, a conventional 50MW building runs about 18 to 24 months from groundbreaking to IT-ready, with permitting excluded from that clock. In addition to the mentioned commissioning considerations, faster timelines claims are also sometimes related to a counting convention, often starting the clock at the electrical fit-out or the vertical works rather than at groundworks. Besides, permitting adds another 12 to 13 months that cannot overlap with construction, taking the all-in timeline to roughly ~30-35+ months for a stick build against ~24-30 for modular.

In the table below, which considers a scenario of an operator going full modular, modularization can compresses the construction window to about 12-18 months, around ~36% faster than a pure stick build and about ~30% faster than today’s baseline that considers some modularization.

![](https://substack-post-media.s3.amazonaws.com/public/images/8d2c4802-46e6-40ff-a7bc-60798e936757_1430x393.png)
*Source: SemiAnalysis Industrials Model*

The savings scale with how much scope moves to the factory. An operator taking only MEP skids, midway between today’s baseline and a full modular build, lands around 17 months. That schedule can be shortened even further when deploying all-in-one prefabricated block or containerized datacenters, which can take the building window all the way down to about 12 months. Today we can hear some claims even for under 12-month deliveries.

![](https://substack-post-media.s3.amazonaws.com/public/images/fd5db78c-8c8e-41ab-8f7f-bd5ab328facf_2912x1464.png)
*Source: SemiAnalysis Industrials Model*

Digging deeper, during the MEP fit-out, an AI data hall absorbs about 12,000 field man-hours per MW, with electrical the dominant trade. A standard 50 MW hall concentrates 600,000 field hours into one building and stacks about 300 craft workers at peak. Relocating that MEP scope to the factory, on-site hours fall about ~63% to 4,500 per MW and licensed-electrician hours about 85%. The window itself compresses by less than the hours because the relocated work now runs in the factory in parallel with sitework. In addition, moving work into the factory also reduces dependence on weather and geographic constraints.

![](https://substack-post-media.s3.amazonaws.com/public/images/421792de-47ec-456d-9d49-d5899315b7c1_2912x1344.png)
*Source: SemiAnalysis Industrials Model*

**Speed equals money**

Speed is compute and compute is revenue, so the true value of pulling go-live forward is the opportunity cost of the delay. In our calculations we consider as a rule of thumb that today, for CSPs, a megawatt of IT load generates on the order of $12M to 15M of revenue a year, or about $1-1.25M per IT MW per month. That said, in such a capacity constrained market, we are seeing new deals being made on much higher disclosed pays, see SpaceX and Anthropic deal, or [as we recently covered in our Meta newsletter post](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be), revenues of $50M per IT MW. Companies like Anthropic or OpenAI are making over $50M/MW on API.

On the COGS side, the relevant cost is GPU depreciation, at an average $30M/MW for an Nvidia cluster depreciated over five years, roughly $500,000/MW per month. An idle month strands at least that depreciation, on GPUs already on the clock whether or not the hall is ready, so we value an earlier month to the owner-operator at about $500k/MW, a conservative figure since the contribution margin on live compute is higher. For a wholesale colocation operator that never owns the GPUs, the value of an earlier month is just the lease it can now bill, about $190,000/MW per month, roughly $190/kW/mo.

![](https://substack-post-media.s3.amazonaws.com/public/images/18483053-f344-4a19-9553-94575ef42deb_2500x1188.png)
*Source: SemiAnalysis Industrials Model*

Applying those unit economics to the roughly 8-month lead over a pure stick build, the owner-operator captures about $200M undiscounted across the 50 MW hall, or ~$4M/MW.

Of course, all of this is conditional on the building being the binding constraint. Go-live is the latest of three dates, building ready, power available, and GPUs delivered, and accelerating the building earns nothing if it was not the date that bound.

## **The TCO Advantage**

Compared to the realized speed benefits, Capex savings are not meaningful. We estimate that same full modular 50 MW liquid cooled hall costs about ~$1.1M/MW less all-in, ~$13.5M/MW against ~$14.6M/MW, just under an ~8% delta.

When looking at the all-in content/MW for the datacenter equipment, we can separate between hardware cost and service or installation cost. The hardware piece itself does not change much: switchgear, UPS, transformers, and other core hardware cost the same whether they are installed in a field-built room or integrated into a factory skid. The gross savings come from two places mainly, the labor portion and a shorter build time.

![](https://substack-post-media.s3.amazonaws.com/public/images/6ade310f-6211-4cfb-8f98-e15b5b7c3ae3_2912x1464.png)
*Source: SemiAnalysis Industrials Model*

We estimate that moving MEP into the factory saves about $0.6M/MW on construction services and $0.5M/MW on installation. The wage gap is small, as BLS puts field construction at $34/hour against $33/hour in the factory, though overtime and site premiums lift the effective field electrician to roughly $63/hour. The real lever here is higher factory throughput, dropping a full field hour of scope.

Second is the effect from shorter build time. Locking factory cost earlier and compressing the field period trims escalation, contingency, change orders and site general conditions.

![](https://substack-post-media.s3.amazonaws.com/public/images/ef46db90-85cb-4744-9167-ac9ea243a3ea_1430x734.png)
*Source: SemiAnalysis Industrials Model*

Against those savings, modular carries some penalties, with double margin being the largest. A stick build marks up installed content once, through the general contractor and its subs. A modular build adds a separate module-vendor margin on top of the site integrator’s. That layer compresses when the OEM also integrates on site, as Vertiv and Schneider do on their turnkey programs. Schneider’s WP163 shows this dynamic, putting module hardware about 40% above traditional and netting to 13% lower first cost, after design and install labor savings are counted.

![](https://substack-post-media.s3.amazonaws.com/public/images/6bb77f0f-01f9-4a9d-80ed-5486e4254f8d_1051x652.png)
*Source: Schneider*

Two smaller penalties follow, including the module premium (chassis, bracing, extra interconnects, transport and craning), and from the vendor perspective, the additional factory burden.

![](https://substack-post-media.s3.amazonaws.com/public/images/f5199a1d-0473-4b32-afd3-7e2e71d08888_1430x393.png)
*Source: SemiAnalysis Industrials Model*

## **The Quality and Predictability Advantage**

Factory first-pass quality, the share of test and inspection points cleared without rework, is supposed to exceed 95% in modular solutions, against a field baseline of 60-70%, thanks to the on-factory fixed work instructions. The benefit is system predictability. Flex frames this as a design choice and engineers it through design failure-mode-and-effects analysis for productized configurations, design-for-manufacturing and design-for-assembly reviews for project-specific ones.

That said, recent conversations point to the opposite side, with operators and MEP contractors claiming that modular solutions have proven reliability issues and haven’t lived up to their claims. This eventually means not only losing all the time savings gained initially, with a field team having to go on site, but more importantly, putting the precious hardware at risk.

## **Re-evaluating Vendors’ Claims**

Our ~36% time savings, or around 8 months, lands just above Flex’s published 30%+ floor on whole projects. In order to do a fair comparison, we must consider that vendors’ numbers usually come from narrower scopes or composite definitions, not the end-to-end construction timings. Vertiv’s 85% SmartRun claim applies to overhead busway and containment, while MegaMod’s 50% claim measures module deployment against on-site build. Schneider’s 60% claim is for power-and-cooling modules.

![](https://substack-post-media.s3.amazonaws.com/public/images/6666639d-e2a7-43a2-b99c-0d031ac2a764_2912x1344.png)
*Source: SemiAnalysis Industrials Model*

# **What Operators and Developers Are Modularizing Today**

Across the market, operators and developers are not converging on one modular strategy.

## **Hyperscalers**

Hyperscalers most frequently build their own fleet, vertically integrate buildouts, and engineer the datacenter design around their actual workload. That’s why hyperscalers tend to show the innovator traits and have leading experimental footprint.

**AWS**

AWS shows the fastest scaling buildout currently, adding almost 3.9 GW of capacity to the end of 2025. Project Houdini is their largest internal attempt to modularization model. Rather than designing a modular building from scratch, AWS took its standard data-hall map and re-cut it into a factory-built skid roughly 45-feet in length and weighing about 2000 pounds that is transportable on double-drop trailers. This puts Houdini squarely in the “factor-built white-space” category.

![](https://substack-post-media.s3.amazonaws.com/public/images/1ea8619f-2321-4e42-bc73-a2e419c631d7_1170x633.png)
*Source: AWS Project Rainier Indiana*

The approach cuts deployment from as much as 15 weeks to roughly 2–3 weeks and can eliminate more than 50,000 on-site electrician hours per module. The skids are built in Houston, Salt Lake City, and Topeka, with early deployments in Texas and South Bend, targeting ~25 weeks from construction start to the first server room.

Houdini is also notable for its approval model. Instead of relying only on site-level engineering sign-off, the factory process requires separate validation of the design and the physical build. Cupertino Electric serves as the main partner, responsible for the latter.

![](https://substack-post-media.s3.amazonaws.com/public/images/57a7f6ee-678c-46c8-9d2e-2d9394a0b80f_1998x1366.png)
*Source: SemiAnalysis Industrials Model*

**Meta**

Meta has recently focused on how to get the building enclosed. Its “tents” datacenters, or rapid-deployment structures, are the clearest example of shell-level modularization in the taxonomy above. A lightweight structural frame supports a tensioned fabric membrane, creating a weather-protected enclosure much faster than a conventional steel-and-concrete building.

At Prometheus in New Albany, Meta is using this strategy to pull shell construction forward

![](https://substack-post-media.s3.amazonaws.com/public/images/26f3426e-2d7c-469a-acba-ea104d023b84_916x482.png)
*Source: Meta Tent at Prometheus New Albany*

Meta has built six rapid deployment structure at this campus, with each roughly 125,000 in square feet dimension. To put speed savings into the picture, it’s worth noting that the site’s first five permanent buildings took Meta two to three years to complete, while the tents took a fraction of that, with eight standing by April 2026 from our satellite tracking since their announcement of the tent buildout in July of 2025.

This does not mean Meta built the complete datacenters in nine months, because the tent accelerate the shell but not the full facility. Also, the trade off on the other hand, is resilience. A fabric structure does not provide the same long-term durability or weather protection as a permeant steel or concrete shell as we had described above, it is also not built with intent to provide decade-long protection service.

## **GPU Clouds and Neoclouds**

**Crusoe**

Crusoe participates in both the shell modularization and whole facility modularization taxonomy. At the Abilene Stargate campus, Crusoe accelerated the shell using structural steel and factory-made insulated metal panels. Working with Digital Building Components, each building used roughly 672 prefabricated panels. The panels were manufactured in under 40 days and installed at a rate of roughly 15 to 20 per day, allowing the building to reach a dried-in state in under eight weeks.

![](https://substack-post-media.s3.amazonaws.com/public/images/509f6080-e982-4f6e-b0fb-dce2c6e2ecc7_1432x671.jpeg)
*Source: Crusoe Stargate Abilene Campus*

In addition, Crusoe’s decided to vertically integrate the manufacturing process. Its 2022 acquisition of Easter-Owens brought modular datacenter and electrical-system manufacturing in-house, giving Crusoe greater control over design, supply chain, and production. The company is now expanding that capability through a dedicated Spark factory in Brighton, Colorado.

Each Spark unit are roughly one megawatt in scale and arrive substantially complete, placing Spark in the whole-facility modularization category.

![](https://substack-post-media.s3.amazonaws.com/public/images/87869878-a751-4e71-8ee4-1ab52b74a00d_738x411.jpeg)
*Source: Crusoe Energy Systems – Spark Container*

The Redwood Materials deployment in Nevada shows how this model can scale. Crusoe initially installed four Spark units alongside a 12 MW microgrid and later announced an expansion to 24 units.

**Hut 8**

Hut 8 is buying the entire infrastructure stack. A former bitcoin miner with power and land positions, it is racing to convert those positions into leasable AI capacity, and the fastest way to do that is to buy a finished modular stack.

![](https://substack-post-media.s3.amazonaws.com/public/images/88acc7be-4dbd-4153-93c4-e044f5f9d95e_1008x509.jpeg)
*Source: Hut 8 Corpus Christi Beacon Point Platform*

At its Beacon Point campus in Corpus Christi it runs Vertiv’s OneCore to commercialize a 704MW IT lease.

The project is being designed around Nvidia’s DSX reference architecture and delivered through a group of established counterparties. American Electric Power provides the utility relationship, Jacobs Solutions owns the EPCM scope, and Vertiv supplies the critical power and cooling infrastructure.

**Nebius**

Nebius takes a lighter approach to modularization by defining the facility around its own compute architecture and modularizing selected parts of the infrastructure such as power and cooling.

At the New Jersey campus, the facility is being built to Nebius’s own design through its partnership with DataOne and is planned as a phased development expandable to 300 MW. The company used precast structural components to accelerate the shell, while pairing the site with Bloom Energy behind the meter fuel cells as the power solution.

![Sherrill unveils N.J. plan to regulate AI data centers amid rising energy costs - nj.com](https://substack-post-media.s3.amazonaws.com/public/images/3a140a1a-442b-4e65-b2e5-d9159acf6656_800x476.jpeg)
*Source: NJ.com, Nebius/DataOne New Jersey*

At Béthune, France, the company follows the same operating logic through a different construction method. The project reuses the former Bridgestone tire plant, avoiding part of the greenfield shell and permitting process. Azur Datacenter is responsible for the land, utility intake, construction, and physical plant, while Nebius focuses on the GPUs, racks, networking, and software.

## **Colocation Providers**

**Compass**

Compass is the colo that has run the modular playbook longest. They industrialize the whole facility into a repeatable kit of parts, not just one subsystem. We estimate roughly 70 - 85% of each building is manufactured off-site and bolted together on site, standing up a building’s framework and roof in 18 to 21 days. The kit spans the full stack:

- Shell: a rebar-free, fiber-reinforced precast shell, Compass casts itself from on-site batch plants
- White space: Standardized prefabricated rack and containment systems such as using Schneider’s EcoStruxure Pod
- Power block: a repeatable ~1.25 MW Schneider power center (Galaxy VX UPS, lithium-ion batteries, QED-2 switchgear)
- MV switchgear: modular medium-voltage switchgear skids under a Siemens deal for up to 1,500 units over five years

![](https://substack-post-media.s3.amazonaws.com/public/images/858e4c0e-9373-499f-93c5-4209a4698865_970x464.jpeg)
*Source: Compass Datacenters in Red Oak*

It runs this same kit across campuses, up to 360 MW at Red Oak, Texas and eight buildings across 1.8 million square feet at Goodyear, Arizona.

**QTS**

QTS’s modular strategy is built around locking the design early, standardizing the interfaces between vendors, and purchasing critical equipment before a specific building needs it. The company maintains roughly 7 million square feet of warehouse capacity in Kansas for long-lead equipment, allowing UPS systems, switchgear, cooling equipment, and other owner-furnished components to be held in inventory rather than ordered after each customer signs.

The approach began with the Freedom Design, which keeps the building shell flexible but repeats the power architecture. Each factory-built pod combines a 1.5 MW UPS and switchgear package with a 2.25 MW generator, and the system scales in 1.5 MW increments. Freedom LC+ expands the same concept into cooling, with an architecture that can support either fully air-cooled or fully liquid-cooled deployments. QTS’s newer rapid-deployment design pushes modularization further into the building itself, organizing capacity around repeatable 60 MW data-hall blocks.

QTS has therefore continued to move more scope off-site: first the power train, then parts of the cooling system, and now portions of the shell and data hall. For the shell, some QTS facilities use tilt-up concrete, including Manassas, while larger campuses such as Cedar Rapids use structural steel.

![Project Profile: QTS MAN1 DC-3 | Tilt-up Concrete Association](https://substack-post-media.s3.amazonaws.com/public/images/9b685916-1e0f-401b-a00a-dd37556a4ffa_645x680.png)
*Source: QTS Man1 Project Tilt-UP*

The value is labor, safety, and schedule certainty. QTS estimates that labor pressure has increased datacenter construction costs by roughly 20–30% per MW. Moving to modular is the company is trend, and they begin by stocking long-lead equipment in advance removes another source of delay, giving QTS greater control over when the final megawatts can be commissioned.

QTS developed subsequently the “Rapids” design, which materially accelerates construction timelines. Two major AI companies have adopted this design at scale.

![](https://substack-post-media.s3.amazonaws.com/public/images/7671330c-35c5-43de-b0bb-59627d84a988_1414x1180.png)
*Source: SemiAnalysis Industrials Model*

**Aligned Data Centers**

Aligned’s modular strategy is centered on adaptability, keeping the core power and cooling architecture standardized while allowing the hall configuration to change as customer requirements and rack densities evolve. The approach began with core MEP infrastructure, including a 2 MW UPS container with integrated distribution switchgear and power. This approach is now extending into site conveyance through examples like prefabricated chilled-water assemblies. For customers able to coordinate early, the scope can extend even further into the white space through things like secondary fluid piping.

![](https://substack-post-media.s3.amazonaws.com/public/images/8f482d50-f566-4f90-9fdc-8f95fb2d5463_1024x531.png)
*Source: Aligned Adaptive Modular Infrastructure*

The other core element is Aligned’s Adaptive Modular Infrastructure platform, which keeps the underlying power and cooling systems consistent while allowing the hall to shift between air, hybrid, and liquid cooling as rack densities evolve. The platform combines

- Delta³, Aligned’s air-cooling system, supporting densities of up to roughly 50 kW per rack.
- DeltaFlow, its liquid-cooling platform, supporting densities above 350 kW per rack

Because the underlying chilled-water loop and facility interfaces remain consistent, the cooling mix can change without redesigning the entire hall. The components inside the modules remain standardized and do not change. An example is found in Project Caprock in Texas, 540 MW across six buildings and 1.65 million square feet.

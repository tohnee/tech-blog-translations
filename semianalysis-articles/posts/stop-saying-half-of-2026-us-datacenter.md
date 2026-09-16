---
title: "Stop Saying Half of 2026 US Datacenter Capacity Is Canceled"
subtitle: "Don't Believe The Vibecoded Estimates, Go Through Every Individual Filing Instead"
date: 2026-06-18
source: https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter
crawled: 2026-09-15
authors: ["Reyk Knuhtsen", "Maya Barkin", "Jeremie Eliahou Ontiveros", "Ellie Holbrook", "Nicolas Bontigui", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Stop Saying Half of 2026 US Datacenter Capacity Is Canceled

**Don't Believe The Vibecoded Estimates, Go Through Every Individual Filing Instead**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

The claim that half of 2026 US datacenter capacity will be delayed or canceled has been circulating widely across financial and social media. This traces back to Bloomberg’s April 1, 2026 [piece](https://www.bloomberg.com/news/features/2026-04-01/us-ai-data-center-expansion-relies-on-chinese-electrical-equipment-imports), *America’s AI Build-Out Hinges on Chinese Electrical Parts*, which framed the 2026 capacity slowdown as a consequence of a fragile, China-dependent equipment supply chain. Bloomberg didn’t lead with that framing, but within days, TechRadar, Tom’s Hardware, The Register, and other news outlets ran sharper, more clickbait versions claiming half of datacenters are cancelled, and that’s the version now circulating.

We find these claims quite amusing. We’ve consistently been first to call-out high-profile delays, like Core Scientific ahead of Coreweave’s Q3’25 earnings in our industry leading [datacenter tracking model](https://semianalysis.com/datacenter-industry-model/). We update the dataset by reviewing every site dozens of times a year. However, **over the last 6 months, our YE2026 NA Hyperscaler Self-build forecast only moved by ~1%, and NA colocation <5%.** What is causing the discrepancy?

![](https://substack-post-media.s3.amazonaws.com/public/images/fe9937a5-28e5-4150-86ed-8c49a75054b6_1558x989.png)
*Source: SemiAnalysis Datacenter Industry Model ; Revisions from the past 6 months*
![](https://substack-post-media.s3.amazonaws.com/public/images/61f61344-af89-4979-9d7f-23f6d645cb33_1542x993.png)
*Source: SemiAnalysis Datacenter Industry Model ; Revisions from the past 6 months*

In our view, the culprit is obvious: the data sources behind these claims of “50% of 2026 datacenters are delayed” are essentially uninformed vibe-coded datacenter forecasts that take announcements at face value, without any bit of critical judgement. We’ve seen more and more [Claude Coded](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point) datacenter models and estimates crop up, all of them **wrong**. Thankfully, that’s not how we built our model, which is trusted for billion-dollar investment decisions by all the world’s largest tech companies in the world, as well as energy and industrials giants, and all the largest investors on Wall Street.

Claude Code pulls press releases, views unfounded GW-scale announcements as ground truth, misunderstands construction timelines and grid complexities, and compiles a terribly inaccurate report. As resident Claude Code users spending **$170K+ in just one week**, we are very familiar with how to use Claude, and the mistakes others are actively publishing.

![](https://substack-post-media.s3.amazonaws.com/public/images/cd4edb06-9e85-4f96-bef7-29e550a385bf_2399x1200.png)

Let’s be clear, delays and cancellations are occurring. Our Datacenter Model flagged the STACK Infrastructure / Oracle permitting impasse months before Bloom Energy stepped in. We caught the Nebius New Jersey delays, which are still persistent. We nailed the Core Scientific datacenter delays ahead of Coreweave’s Q3 earnings. However, we then successfully predicted Coreweave’s 1.7GW of Active Power by end of 2026 (exactly the Company’s guide) as we determined that other datacenters were on time (no, not everything is delayed!). Our data also predicted ~35B of RPO to be signed by Q1 2026 via our industry-first method to forecast RPO based on datacenter signals.

And most recently, we’ve determined **STACK Infrastructure/Oracle’s site has now been delayed to 2029,** due to a lack of gas pipeline and the ensuing burdensome regulation. We’ve flagged many many others, some of which have materialized, but many others which aren’t realized yet and the market is still misunderstanding. [Check our Datacenter Model for full information](https://semianalysis.com/industrials-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/a2f2ada3-8386-4d87-9118-f40ba2780ea1_1241x1115.png)
*Source: SemiAnalysis Datacenter Industry Mode l, SemiAnalysis Energy Model*
![](https://substack-post-media.s3.amazonaws.com/public/images/a68aa125-d385-4935-be63-b9cace79ee4e_1248x1114.png)
*Source: SemiAnalysis Datacenter Industry Mode l, SemiAnalysis Energy Model*

**There are two main reasons the headline narrative is wrong.**

**First**, the headline number is built on a **hugely flawed denominator, off by multiples**. Bloomberg’s data comes from Sightline Climate, which estimates that of the roughly 12 GW expected to come online in the US in 2026, only about 5 GW is currently under construction. **Checking against our Vision Model, trained on hundreds of thousands of satellite images, even their Under Construction figures are off by multiples.** Taking ONLY the top-two hyperscalers alone gives us a higher Under Construction capacity than 5GW. And that’s self-build only, it doesn’t include the many GWs of capacity under construction by 3rd party developers.

![](https://substack-post-media.s3.amazonaws.com/public/images/08169b0e-2c64-4725-bbf6-62c969e98c3b_1931x1112.png)
*Source: SemiAnalysis Datacenter Industry Model*

Sightline’s dataset clearly doesn’t track every datacenter under development; it likely tracks the large, publicly announced projects. That skews the basis heavily toward the kind of speculative megaprojects from unexperienced datacenter developers most likely to slip in the first place. The “50% cancelled or delayed” figure isn’t really a statement about the US datacenter pipeline, but rather about the slice of the pipeline most prone to slipping.

**Second**, even taking the Bloomberg/Sightline number at face value, almost all of what’s getting flagged sits in the early-stage, or pre-construction “announced” bucket. These are speculative MW that weren’t going to land on a 2026 timeline with any rigorous analysis. We’ve been writing for months that the market is in structural oversupply of early stage projects, with developers and landowners announcing projects on preliminary power estimates, often without financing, interconnection studies, or equipment orders in place.

**Instead of falsely declaring them as 2026 projects, they rather show up in 2028+ in our model.** In December 2025, we flagged that over half a Terawatt is in the large load queue in the US, and that number is now over a Terawatt. The vast majority are highly speculative, yet some developers make high profile announcements without much to show for. We do not put low probability datacenters in our datacenter timelines.

![](https://substack-post-media.s3.amazonaws.com/public/images/e8b85901-01b1-4e0f-9ce0-ff4cc0b718bd_2521x1600.png)
*Source: SemiAnalysis Energy Model*

We will start by covering how common these questionable announcements are, and then display what real delays look like. We then cover the noise fueling the misled delay narrative, and close with why none of it has moved our numbers, for datacenters or for the equipment suppliers.

**Let’s Begin With Real Delays.**

# The Anatomy of a Datacenter Delay

We have three broad buckets to categorize datacenter delays, which we examine in depth below:

- Overly aggressive announcements by new players with speculative projects. The provided timelines are often simply unrealistic and should be discounted (which vibe-coded datacenter forecasts struggle with).
- Advanced projects but with too optimistic construction timelines, often carried by new datacenter developers who lack the experience. We dodge this via our extensive analysis of construction timelines. These developers typically don’t account for traditional sources of delays, which are broad-based and can range from supplier late deliveries to weather-related issues to equipment issues, as well as many other construction and commissioning issues.
- Permitting and overall NIMBY (Not In My Backyard) issues slowing down an advanced project, forcing to change things like power sources or datacenter design.

## 1. Aggressive Announcements by Newer Datacenter Developers

New entrants in the space commonly try to give themselves some publicity by announcing massive GW-scale datacenters with aggressive timelines, despite their project being early stage. But it can take more than 4 years from land purchase to datacenter delivery. When we see a brand-new announcement in 2025 saying 2026 operational from a new “unknown” developer, it should raise some red flags. And for flagship multi-GW announcements, we often find that deeper analysis reveals these projects are very early, and sometimes don’t even have long lead time equipment ordered. We are not denigrating these operators, but rather promoting caution on interpreting headline announcements correctly - which vibe-coded forecasts often struggle with. Let’s look at a few examples.

Data City, unveiled by [Energy Abundance](https://www.energyabundance.com/), boasted a 5GW campus, of which 300MW would launch in [2026](https://www.datacenterdynamics.com/en/news/5gw-data-center-with-behind-the-meter-hydrogen-power-planned-for-laredo-texas/). Looking again, the Energy Abundance website has very little except a “Contact Us” button. There has been no news since the announcement, and satellite imagery doesn’t show any evidence of physical progress. While AI-generated datacenter forecasts likely consider this as 2026 delayed capacity, any serious forecast would’ve taken this with some skepticism.

In June 2025, APR Energy announced a potential [400MW](https://www.datacenterdynamics.com/en/news/apr-energy-obtains-approval-for-800-acre-natural-gas-powered-data-center-in-pampa-texas/) datacenter campus in Texas, where “The first phase of the project’s development is slated for early 2026.” At the same time, they were “currently seeking data center developers, hyperscalers, and AI partners to partner on the development of the facility.” No customer yet, a new developer, targeting a <1-year timeline needs to be approached with more scrutiny. There’s been no news since.

Another example is the Cloudburst facility in San Marcos, TX. It was announced as a 1.2GW facility, of which 50MW live by Q3 2026 (then pushed to Q4 2026). When announced in February 2025, that Q3 2026 timeline was unrealistic given many approvals weren’t secured yet. The company is now making good progress, and got the go-ahead by the local county in April 2026 for a >10B project - congrats to Cloudburst. They broke ground in November 2025 for that first 50MW phase, but the Q4 2026 timeline remains too aggressive based on real-time imagery, since shell construction hasn’t started yet. However, it’s easy to see how Claude Coded forecasts could get confused and assume 1.2GW is delayed. Some publicly available estimates out there claim that the site is planning to deliver 1.2GW by 2026 - which is not even consistent with the company’s own statements.

These are just a few examples of headlines, there are many more. If you look closely at the Claude Coded estimates, you will find many of these announcements are taken at face value. This is not a knock on the developers — as these projects may still be realized later - but an egregious error in many estimates’ methodology.

## 2. Advanced Projects With Overly Optimistic Construction Timelines

Many do not understand what it takes to construct a datacenter, and there’s plenty of new(er) operators with ambitious plans. Our forecast accuracy is the most reliable because we have refined our timelines extensively. We review every single type of datacenter design, both through local filings, and extensive satellite imagery. The vibecoded datacenter models have not learned what true timelines are, and instead mislead everyone.

![](https://substack-post-media.s3.amazonaws.com/public/images/21e5935b-ddf2-44d7-8b7f-d108b17fb558_2240x1280.png)

***Nebius’ 300 MW New Jersey Flagship Datacenter***

Nebius’ flagship campus in New Jersey, built by developer DataOne, is a great example of the challenges of **constructing** a datacenter. In March 2025, DataOne was targeting a 4 month delivery for its first 50 MW phase despite the developer having no prior datacenter track record in the US. The schedule relied on precast materials and extensive prefabrication to compress the build. To be clear, we think this approach was highly innovative and we are big fans, but things are always more challenging than initially expected, especially for a new datacenter developer.

The first challenge arose in the equipment procurement. Per a [LinkedIn](https://www.linkedin.com/posts/cabeyney_ai-datacenters-innovation-activity-7367650153555591168-taqK/) post of an executive leading the development, late deliveries from a few suppliers pushed the first phase from 4 months to 6, i.e. a 2 month slip on its own.

Then, commissioning and installation proved longer than expected. Satellite imagery shows the shell going up remarkably fast, but setting up the MEP took far longer than the shell itself. In September 2025, the executive still claimed that he would imminently deliver the full facility. But our December 15th capture shows the chillers serving the second 25 MW still not in place, meaning the initial 50 MW building wasn’t complete almost three months after delivery was declared imminent.

![](https://substack-post-media.s3.amazonaws.com/public/images/6d13de74-ed81-494d-986f-a516c0a09492_1024x851.png)
*Source: SemiAnalysis Datacenter Industry Model ; DataOne/Nebius New Jersey, December 15th, 2025*

Putting the full sequence together makes the slippage easy to see (timeline from DataOne’s own public disclosures, Nebius earnings calls, and our satellite tracking):

- **March 2025:** targets set at announcement, per the DataOne CEO’s public posts, later eacho’ed by Nebius. 25 MW by July, 50 MW by September, 100 MW by year-end 2025.
- **June 2025:** first delay acknowledged publicly, delivery pushed to August.
- **September 2025:** the 50 MW building declared imminently delivered, 4 months becoming 6. Our satellite imagery shows only the first batch of chillers, enough for 25 MW, going onto the roof that month.
- **~October 2025:** first 25 MW delivered, seen by the installed chillers.
- **Mid-December 2025:** our December 15th capture shows the second batch of chillers still being installed. Roughly 25 MW energized against the 100 MW promised for year-end.
- **January or February 2026:** full 50 MW complete on our estimates, much later than the targeted 4 month delivery. To be clear, a 10-11 month delivery is still very fast relative to industry standards - so congratulations to Nebius and DataOne.

To understand whether the site will be on time for 2026 delivery and Nebius meet its ARR guidance of $7-9B by year-end, check our [Datacenter Industry Model](https://semianalysis.com/datacenter-industry-model/).

![](https://substack-post-media.s3.amazonaws.com/public/images/b9810149-eacc-4211-ae8e-aacf730a9ac8_1024x779.png)
*Source: SemiAnalysis Datacenter Industry Model ; DataOne/Nebius, New Jersey, as of April 15, 2026*

***Core Scientific’s Denton Campus***

Shown in our graph as one of the newer operators with impressive plans, Core Scientific ran into issues that an experienced operator would have likely accounted for when projecting timelines. Let’s walk through a quick timeline.

1. In 3Q2024 earnings, they planned to "begin delivery of powered infrastructure for HPC hosting by the **end of the first half of 2025**". This was in reference to all CoreWeave contracted locations, including Denton.
2. 4Q2024, they planned to expand Denton by 70MW, but also saw a delay coming: “These factors introduced several permitting challenges, which we resolved in collaboration with CoreWeave.” CORZ now guided 250MW delivered to CoreWeave **by end of 2025**.

   1. In addition, infrastructure redesign due to GB200 redesign issues were cited as delay reasons. These reasons had become **very** well-known in the neocloud world.![](https://substack-post-media.s3.amazonaws.com/public/images/1b60664c-6e64-4490-a81b-e8191cc3db6b_986x520.png)
   *Source: Core Scientific Earnings, 4Q2024*
3. Their 2Q2025 [10-Q](https://investors.corescientific.com/sec-filings/all-sec-filings/content/0001628280-25-039284/core-20250630.htm) then vaguely stated delays were arising due to weather and construction, and further pushing timelines out to end of 2025.

   1. Moreover, we suspect supply chain challenges partially came from a [transformer exploding](https://www.prnewswire.com/news-releases/arnold--itkin-files-lawsuit-after-transformer-explosion-severely-burns-worker-at-denton-worksite-302594382.html).

Couple this with satellite imagery of a multiple buildings with no chillers installed, this was clear that the 250MW by YE2025 timeline was going to be missed.

![](https://substack-post-media.s3.amazonaws.com/public/images/93d62aa1-a6f7-4795-a9a6-c91cc1679428_718x978.png)
*Source: SemiAnalysis Datacenter Industry Model ; Core Scientific, Denton, Texas, October 29, 2025*

Following this, we promptly informed our clients that we see delays coming for CoreWeave.

![](https://substack-post-media.s3.amazonaws.com/public/images/3dcde3f3-b0b7-47ac-9096-b16a82efa983_1194x1164.png)
*Source: SemiAnalysis Datacenter Industry Model ; An update regarding CoreWeave’s earnings*

These challenges are not always avoidable, but experienced operators typically account for them in both timeline and budget.

## 3. Well-Capitalized Projects Facing Permitting and Local Opposition Issues

***Oracle/STACK New Mexico: Permits, a Pipeline, and Pushback***

Rather than waving our hands about “regulatory challenges,” let’s detail another project in specific: the STACK Infrastructure/Oracle location that we have delayed to 2029. **The following information was published to our Energy Model and Datacenter Model clients, of which the Energy Model is available as a $0 bundle for limited time.** Oracle’s June 10 earnings call guided 1H2027 customer delivery for this campus: a timeline FERC records do not support, nor our estimated construction timelines.

Three things went wrong here. The project tried to thread permitting limits with a two microgrid design, each sitting very close to the major-source threshold. It required a large infrastructure buildout, including a brand new gas pipeline. And organized local opposition slowed every step along the way.

In our March Datacenter Model note, we flagged the Oracle/STACK New Mexico Stargate campus (Project Jupiter, in Doña Ana County) with a delay due to its onsite power system was neither finally permitted nor solidified. The entire campus depends on two behind-the-meter gas microgrids, East (NSR 10732) and West (NSR 10734), filed with the New Mexico Environment Department by Acoma, LLC. NMED received both applications on November 17, 2025 and ruled them complete on January 22, 2026, but each microgrid was being squeezed in as an individual PSD-minor source rather than one major source.

![](https://substack-post-media.s3.amazonaws.com/public/images/0fd631b2-3f49-470b-9f1b-640991438ec7_1649x1046.png)
*Source: SemiAnalysis Datacenter Industry Model*

NMED’s December 2025 incompletion letters found East could emit up to 521 tpy NOx against a requested 248.90 tpy cap and West up to 388 tpy against 249.97 tpy, both too close to the 250 tpy major-source threshold to be enforceable. On March 23, 2026, NMED pushed both reviews from the April 22 target to July 21, 2026, ordered a public hearing, and cited roughly 7,155 comments plus the applicant’s intent to imminently amend the filings, leaving the public schedule of Q4 2025 construction and Q4 2026 operations untenable.

Meanwhile, the onsite gas generation systems had still not been locked in. In the West Microgrid, for example: “These thirty-four (34) turbines will consist of a combination of GE TM2500 and Mitsubishi FT8 natural gas fired turbines **depending on availability for purchase**.” Depending on availability for purchase with turbine lead times extending multiple years did not make a great case.

![](https://substack-post-media.s3.amazonaws.com/public/images/e38410c8-175d-42ff-8231-56329c05954a_2532x73.png)
*Source: Local Filings*

Our Energy Model note “Oracle’s New Mexico Stargate Gas Pipeline Delayed: No Bloom Without Gas” published in May found new developments. With the gas turbines unable to clear permitting in time, Oracle withdrew the East and West turbine applications on April 27, 2026 and filed for Bloom Energy fuel cells instead, targeting ~37 tpy NOx. However, this didn’t solve the binding constraint: the 400,000 Dth/d of gas to arrive in **one unprepared pipeline.**

A September 2025 precedent agreement between Green Chile Ventures (likely Oracle subsidiary) and Transwestern baked an August 15, 2026 in-service date into the contract, and Transwestern filed the Green Chile Pipeline at FERC (CP26-80-000) on January 29, 2026 seeking an expedited blanket certificate. That route ran into compounding obstacles: on March 20, the New Mexico State Land Office denied right-of-way across state trust land, forcing a reroute, and on April 13, 2026 FERC staff filed its own protest over the missing New Mexico State Historic Preservation Office (SHPO) sign-off while multiple environmental intervenors filed to intervene, starting a 30-day cure window.

![](https://substack-post-media.s3.amazonaws.com/public/images/e167f4b6-b6f5-4d5f-9414-3dcf9b2a73a3_2485x1127.png)
*Source: SemiAnalysis Energy Model*

Oracle and Transwestern's May 1–4 attempt to extend the cure deadline went nowhere, the window lapsed on May 13 with no SHPO clearance, and on May 15 FERC's Office of Energy Projects opened a formal Section 7 review demanding a full alternative-route analysis avoiding state lands. Transwestern's subsequent sworn filings confirmed no viable alternative route exists and no path around Section 7. The contractual August 15 in-service date became infeasible, and our base case moved first power off 2027 entirely and out to 2029.

NIMBYism rarely kills a capitalized project of this scale outright, but adds months to permits, hearings, and rights-of-way, enough to delay a project past strict deadlines and into large consequences.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

# **What Is Fueling All This Panic?**

If those are what real delays look like, the headlines driving the narrative look very different. Most of what circulates as evidence of a datacenter pullback falls into three buckets: moratoriums, organized local opposition, and announcements with timelines that were never realistic to begin with. None of them survive contact with the actual pipeline.

***Moratoriums***

A datacenter moratorium is a legislative freeze on new construction permits, designed to give jurisdictions time to assess environmental, energy, and economic impacts before approving more capacity. As of April 2026, at least 12 states have filed moratorium bills, and Indiana alone has at least four counties (Fulton, Marshall, Putnam, and White) that have enacted them. These make for alarming headlines until you look at what they actually cover: none of them had datacenters, and we had nothing in our model beyond early stage.

The most dramatic example is Maine, where the Governor vetoed LD 307 in April, which would have been the first statewide datacenter ban in the US. A statewide ban sounds like ominous for the buildout, **except Maine has less than <5MW** **planned**. The pattern holds across the moratorium map: these measures land overwhelmingly in inconsequential areas, or if not, the projects were already too early stage for 2026 anyway.

![](https://substack-post-media.s3.amazonaws.com/public/images/20616f5a-0bf9-4832-9d21-74018c058066_1200x675.jpeg)
*Source: Local News; Protests in Indiana against datacenters*

***Not-In-My-Back-Yard (NIMBY)***

NIMBYism can be very impactful, as seen with the STACK/Oracle example. The distinction is that opposition slowing a real, capitalized, underway project is rare, and opposition killing a speculative rezoning that existed only on paper is common. The Compass withdrawal in Prince William County, the rejected rezonings in Georgia, the pulled proposals across 20+ states: nearly all of it sits in the announcement layer, where the projects had no equipment ordered, no interconnection agreement, and no 2026 delivery to lose.

***Unfounded Announcements***

The third bucket is the announcements themselves like we showed above. Most pipeline estimates, including the ones underlying the “half of 2026 capacity will be delayed or canceled” framing, rely on announcement-stage data: a press release, a real-estate filing, sometimes a non-binding LOI, none of which is binding in any meaningful sense.

ERCOT is the cleanest illustration of how this can pile up. As of April 2026, ERCOT was assessing more than 410GW of large-load interconnection requests, over 87% of them from datacenters. Texas’s all-time peak demand is about 85 GW, so the queue is nearly five times the size of the grid itself. However, tracking the veritable projects as we do, there’s 311GW of Phantom Datacenter demand.

![](https://substack-post-media.s3.amazonaws.com/public/images/db523510-c1bc-449f-8381-adadf178c1dc_2160x1184.png)

When Texas Senate Bill 6 introduced a real filter (site control documentation, a $100,000 minimum study fee, mandatory curtailment terms), speculative filings started to slow down, exactly as a sorting mechanism should work. When the press reports that a meaningful share of the pipeline has been “delayed or canceled,” much of what is actually being canceled are megawatts that never had the site control, the financing, or the interconnection work to clear those gates in the first place.

All three of these generate fear in headlines and roughly nothing in delivered 2026 megawatts. They concentrate in the early stage layer we already treat as structurally oversupplied, they were in our numbers long before they reached financial media, and that is why our estimates have not moved.

# **Why Hasn’t Our 2026 Outlook Moved?**

We have walked through the constraints above and continue to track them closely. The question worth answering is why our 2026 outlook holds despite the headlines.

![](https://substack-post-media.s3.amazonaws.com/public/images/d239c380-9b42-4dde-9f70-5b4f3c1a1bd6_1558x989.png)
*Source: SemiAnalysis Datacenter Industry Model ; NA Colocation Supply revisions from past 6 months*

The short version is that the cancellations and delays cluster in a layer of the pipeline we already treat as structurally oversupplied. The veritable 2026 projects, meaning the ones with site control, equipment on order, interconnection agreements signed, and/or vertical construction underway, continue to progress on schedule. Hyperscalers, whether its self-build or colocation tenancies, are routing around the constraints in ways that announcement-stage tracking does not pick up.

## **Early Stage Projects Are Structurally Oversupplied**

The bulk of project cancellations occur at the earliest stages of development, before projects have cleared the hurdles required to move toward execution. These are typically announcements rather than fully formed developments, projects that lack critical elements such as permitting approvals, committed tenants, vertical construction progress, or secured grid interconnection. In our Datacenter Model, this segment of the pipeline is intentionally treated as structurally oversupplied, seen later in 2028.

![](https://substack-post-media.s3.amazonaws.com/public/images/e17f721c-8343-4e3a-a64c-c466ac86a292_623x438.jpeg)
*Source: SemiAnalysis Datacenter Industry Model*

The volume of announced capacity at the early stage exceeds what can realistically be delivered, and we view that imbalance as a normal feature of the market. It reflects the asymmetry between low barriers to announcing projects and real constraints on building them. A project generally begins to move beyond this higher-risk phase once it has secured at least two, but preferably three, of the following:

- **Secured land**: completed acquisition, a signed purchase agreement, a long-term ground lease, an exclusivity agreement, or affiliate/shell entity control.
- **A defined power solution**: grid interconnection or onsite generation procurement.
- **Approved permits**: construction approvals and, where relevant, air permits for onsite generation.

Ordering long lead time equipment is also crucial, and that requires deposits and capital.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

## **Leading Operators Are Adept At Navigating All Constraints**

Hyperscalers and leading operators know how to operate in these markets. Land banking multiple locations is the baseline move, but development happens via two parallel playbooks: one political, one physical.

***The political playbook: permitting and community***

The political playbook is really about permits and zoning. Operators with years of history in a place know who to call and what they need to file. They have the local land-use lawyers on retainer, working relationships with the utility VPs and economic-development staff who keep the project moving, and a track record of having delivered prior projects. Those relationships are maintained through ongoing community investment, from PILOT structures and operator-branded workforce programs to capital infrastructure that doubles as public utility, like the $31M Microsoft put into the Quincy Water Reuse Utility before leasing it back to the city for $10 a year. By the time the public hearing rolls around, the developer has heard every concern before and knows how to sell the project around them.

When the political playbook alone is not enough, the project rarely dies. Developers increasingly withdraw proposals ahead of a formal vote rather than hand opposition groups a public rejection that other counties can cite, then relocate to a friendlier jurisdiction, refile a modified design, or shift to brownfield and unincorporated land where the approval steps are fewer. There’s plenty of times hyperscalers don’t progress with sites, not just the ones that are publicly canceled. The site still dies, but it dies quietly, and the project moves somewhere else. Hence the many landbanks.

![](https://substack-post-media.s3.amazonaws.com/public/images/845b7140-f5af-4dc4-9e15-3b2664e661a8_976x1302.png)
*Source: SemiAnalysis Datacenter Industry Model ; xAI’s Colossus 1, retrofitting a warehouse*

***The physical playbook: energy and equipment***

Grid connection lead times have stretched into 7–10 years in multiple metro areas, and equipment lead times for critical SKUs remain 1y+. The market has evolved adaptations on both axes.

**On energy,** the playbook has expanded from a single grid-connection path to multiple:

- **Pay directly into the grid.** Oracle’s deal with DTE to supply BESS systems to support their load, or Meta’s deal with Entergy where Meta pays for the full construction and operation of their dedicated power plant.
- **Powered Land.** In constrained markets like Europe and US metros, businesses are now *selling* or leasing grid-connected (or soon-to-be-connected) land outright. Lancium, Cloverleaf, and others are performing remarkably well in this market.
- **Behind-the-meter (BtM) generation.** One by one, hyperscalers and AI Labs and leading developers are giving up on the grid and going offsite. [Read our onsite gas deep dive for more details](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power).

![](https://substack-post-media.s3.amazonaws.com/public/images/5271dfc8-156f-4eb7-89c3-0fe3ecf1e913_1986x1119.png)
*Source: SemiAnalysis Datacenter Industry Model*

**On equipment,** three adaptations have moved from edge cases to standard practice over the last 12 months:

- **Long-lead procurement in the scoping phase.** Hyperscalers now lock in transformers, MV/LV switchgear, and other long-lead SKUs well ahead of vertical construction. Our [Industrials Model](https://semianalysis.com/industrials-model/) stays on top of the rising bottlenecks, and after Computex Taipei, we’ve flagged a specific equipment for cooling that likely becomes the next big bottleneck. [Contact us for more information](https://semianalysis.com/industrials-model/) at sales@semianalysis.com .
- **Chinese OEMs in the supply chain.** Few will admit it publicly, but Chinese OEMs are quietly alleviating bottlenecks at the high end of the equipment stack. xAI, for example, likely uses Sieyuan transformers/breakers. Multiple US companies now broker for Chinese OEMs, and in some cases hyperscalers purchase directly. The trend has accelerated meaningfully over the last 12 months.

![](https://substack-post-media.s3.amazonaws.com/public/images/f18fd7c6-5b2e-4cf2-8cd1-17bac4791846_802x590.png)
*Source: Sieyuan*

- **Modular and prefabricated builds.** Old news in the Chinese markets, *new* to American AI datacenters. Prefab condenses supply-chain complexity into a single product and dramatically reduces the skilled-labor intensity of onsite assembly, and the same hyperscalers paying inflated wages and onsite housing in Abilene are increasingly the ones leaning on prefab to sidestep that crunch on the next site. We have a dedicated deep dive forthcoming; for now, the takeaway is a meaningful pressure-release valve on equipment and labor constraints simultaneously.

The political playbook secures the first *right* to build, and the physical playbook ensures the build progresses accordingly.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

# **What Do We Do Differently?**

**With all the above challenges and the varieties of workarounds, how are we able to determine veritable delays?** Some projects may die on local opposition, some might pass and see the approving [council members ousted](https://www.kcur.org/politics-elections-and-government/2026-04-09/after-these-independence-councilmembers-supported-an-ai-data-center-voters-ousted-them). Labor is a challenge, or you can import from across the country. Even behind-the-meter sites are still a [novel solution](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power).

Our research agents monitor thousands of municipal, county, state, and utility portals — most poorly structured, many actively resistant to scraping, some still publishing in scanned PDFs and handwritten exhibits. We parse them in parallel and reconcile every signal against live satellite imagery, which is how we generate forward-looking delay calls across the full US pipeline rather than just the highest-profile projects.

![](https://substack-post-media.s3.amazonaws.com/public/images/dd9faed2-eec9-48a4-8e8f-f7c9805ee956_2399x1200.png)

**Where we go beyond what’s public**

- Tasking custom satellite captures on specific sites, on specific days for faster cadence than commercial imagery providers default to.
- Scraping social media presence of NIMBY coalitions, construction firms, and local community pages for sentiment shifts before they reach local press.
- On-the-ground site visits and direct outreach to regulators for documents that were never digitized.

*The full stack is not disclosed publicly.*

The Datacenter Model methodology is coupled with the Industrials and Energy teams tracking the power and equipment/labor markets respectively. When every angle is tracked in parallel, it becomes straightforward to identify which projects carry real cancellation or delay risk, and which apparent “delays” are simply the market culling speculation that was never going to deliver in 2026. Behind the paywall, we discuss another veritable delay coming up, what we are watching, and the players set to benefit.

## **The Equipment Supplier Narrative Is Wrong Too**

We said at the top we would come back to the equipment suppliers. The fear priced into names like Vertiv is that the wave of datacenter delays and cancellations will start eating into record orders and backlog. However, our Datacenter Model capacity forecast shows quarter by quarter delivery, and it’s clear to us that delivered MWs are accelerating.

Equipment lead times remain long. Reinhausen tap-changer bushings, which are a single subcomponent inside a transformer but gate delivery of the entire large HV stack, are now quoted at three to five years. Things have stabilized somewhat over the past year, though most critical SKUs are still running over a year, and several of the major manufacturers, including GE Vernova, Hitachi Energy, and Mitsubishi Electric, are booked out three to four years on their main equipment lines.

Capacity relief is slow to arrive, since production expansion can take two to three years; Hitachi Energy’s new South Boston plant, announced in September 2025, is not expected to be operational until 2028. So in the meantime, the way capacity actually gets allocated is through prepayments. Buyers wire money up front to hold a slot in the queue, which boxes out players with less capital. For behind-the-meter systems, we have heard prepayments in the 10 to 15% range are now standard practice for securing a queue position. AI demand has lifted the pure-play datacenter electricals, Vertiv and Schneider among them, to margins above 20% on the strength of that same imbalance.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

Now run the cancellation fear against that backdrop. The projects getting canceled sit in the early stage layer that never placed equipment orders in the first place; a speculative announcement dying in a county commission hearing removes zero orders from anyone’s books. The projects that do sit in OEM backlogs have prepaid for queue position, locked in long-lead SKUs during scoping, and in many cases already broken ground. And in the rare case a real order does fall away, a queue running three to four years deep means the slot is reallocated to the next buyer in line rather than vanishing.

Our [Industrials Model](https://semianalysis.com/industrials-model/) tracks more than 550 datacenter equipment suppliers across 75 equipment subcategories, mapped to over 6,000 facilities globally, and maps every major supplier’s exposure project by project, which is how we separate backlog at risk from backlog that is locked.

![](https://substack-post-media.s3.amazonaws.com/public/images/33a3e8d7-e455-42bc-9cb3-403c98d18047_2260x1148.png)
*Source: SemiAnalysis Industrials Model*

# **What we’re watching into 2H26**

---
title: "AI Datacenter Energy Dilemma - Race for AI Datacenter Space"
subtitle: "Gigawatt Dreams and Matroyshka Brains Limited By Datacenters Not Chips"
date: 2024-03-13
source: https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Jeremie Eliahou Ontiveros"]
tags: []
audience: only_paid
paywalled: true
---

# AI Datacenter Energy Dilemma - Race for AI Datacenter Space

**Gigawatt Dreams and Matroyshka Brains Limited By Datacenters Not Chips**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

The boom in demand for AI clusters has led to a surge in focus on datacenter capacity, with extreme stress on electricity grids, generation capacity, and the environment. The AI buildouts are heavily limited by the lack of datacenter capacity, especially with regard to training as GPUs need to be generally co-located for high-speed chip to chip networking. The deployment of inference is heavily limited by aggregate capacity in various regions as well as better models coming to market.

There is plenty of discussion on where the bottlenecks will be – How large are the additional power needs? Where are GPUs being deployed? How is datacenter construction progressing by region including North America, Japan, Taiwan, Singapore, Malaysia, South Korea, China, Indonesia, Qatar, Saudi Arabia, and Kuwait? When will the accelerator ramp be constrained by physical infrastructure? will it be transformers, generators, grid capacity or one of the other 15 of the other datacenter component categories we track? How much capex is required? Which hyperscalers and large firms are racing to secure enough capacity and which will be constrained heavily because they were caught flat footed without datacenter capacity? Where will the Gigawatt and larger training clusters be built over the next few years? What is the mix of power generation types such as natural gas, solar, and wind? Is this even sustainable or will the AI buildout destroy the environment?

Today let’s answer these questions, with the first half of the report free, and the 2nd half is available to subscribers below.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

Many are opining with ridiculous assumptions about datacenter buildout pace. Even Elon Musk has chimed in to opine, but his assessment is not exactly accurate.

> The artificial intelligence compute coming online appears to be increasing by a factor of 10 every six months… Then, it was very easy to predict that the next shortage will be voltage step-down transformers. You've got to feed the power to these things. If you've got 100-300 kilovolts coming out of a utility and it's got to step down all the way to six volts, that's a lot of stepping down. My not-that-funny joke is that you need transformers to run transformers... Then, the next shortage will be electricity. They won't be able to find enough electricity to run all the chips. I think next year, you'll see they just can't find enough electricity to run all the chips.
>
> Bosch Connected World Conference

To be clear he is mostly right on these limitations of physical infrastructure, but compute is not up 10x every six months – we track the [CoWoS, HBM, and server supply chains of all major hyperscale and merchant silicon firms](https://www.semianalysis.com/p/accelerator-model) and see total AI compute capacity measured in peak theoretical FP8 FLOPS has been growing at a still rapid 50-60% quarter on quarter pace since 1Q23. I.E. nowhere close to 10x in six months. CoWoS and HBM is simply not growing fast enough.

![](https://substack-post-media.s3.amazonaws.com/public/images/361a28af-afe2-4df8-b47a-7eed2f07a7d4_1591x1030.png)
*SemiAnalysis Estimates*

The boom in generative AI, powered by transformers, will indeed need a lot of transformers, generators and a myriad of other electrical and cooling widgets.

A lot of back of the envelope guesstimates or straight up alarmist narratives are based on outdated research. The IEA’s recent [Electricity 2024 report](https://www.iea.org/reports/electricity-2024) suggests 90 terawatt-hours (TWh) of power demand from AI Datacenters by 2026, which is equivalent to about 10 Gigawatts (GW) of Datacenter Critical IT Power Capacity, or the equivalent of 7.3M H100s. We estimate that Nvidia alone will have shipped accelerators with the power needs of 5M+ H100s (mostly shipments of H100s, in fact) from 2021 through the end of 2024, and we see AI Datacenter capacity demand crossing above 10 GW by early 2025.

![](https://substack-post-media.s3.amazonaws.com/public/images/88b7b56f-ae27-41cd-a9bd-3ff2ce18b727_1162x837.png)
*IEA Electricity 2024*

The above report is an underestimation of datacenter power demand, but there are plenty of overestimates too – some from the alarmist camp have recycled [old paper](https://www.mdpi.com/2078-1547/6/1/117)s written before the widespread adoption of accelerated compute that point to a worst-case scenario with datacenters consuming a whopping 7,933 TWh or 24% of global electricity generation by 2030!

Here come the datacenter locusts, Dyson spheres, Matrioshka brains!

![](https://substack-post-media.s3.amazonaws.com/public/images/80bb03fa-0fe7-4d92-8b6b-02d5f8d4abef_1355x912.png)
*On Global Electricity Usage of Communications Technology: Trends to 2030*

Many of these back of the envelope estimates are based on a function of growth estimates for global internet protocol traffic, and estimates for power used per unit of traffic dampened by efficiency gains – all figures that are extremely hard to estimate, while others utilize top down datacenter power consumption estimates created in the pre-AI era. Mckinsey also has laughably bad estimates, which pretty much amount to putting their finger on a random CAGR and repeating it with fancy graphics.

**Let’s correct the narrative here and quantify the datacenter power crunch with empirical data.**

Our approach forecasts AI Datacenter demand and supply through [our analysis of over 3,500 datacenters in North America across existing colocation and hyperscale datacenters](https://www.semianalysis.com/p/datacenter-model), including construction progress forecasts for datacenters under development, and for the first time ever for a study of its type, we combine this database with AI Accelerator power demand derived from [our AI Accelerator Model](https://www.semianalysis.com/p/accelerator-model) to estimate AI and non-AI Datacenter Critical IT Power demand and supply. We also combine this analysis with regional aggregate estimates for geographies outside North America (Asia Pacific, China, EMEA, Latin America) collated by [Structure Research](https://www.structureresearch.net/) to provide a holistic global view of datacenter trends. We supplement the regional estimates by tracking individual clusters and build outs of note with satellite imagery and construction progress, for example the up to 1,000 MW development pipeline in Johor Bahru, Malaysia (primarily by Chinese firms) – just a few miles north of Singapore.

This tracking is done by hyperscaler, and it’s clear some of the largest players in AI will lag behind others in deployable AI compute over the medium term.

The AI boom will indeed rapidly accelerate datacenter power consumption growth, but global datacenter power usage will remain well below the doomsday scenario of 24% of total energy generation in the near term. We believe AI will propel datacenters to use 4.5% of global energy generation by 2030.

![](https://substack-post-media.s3.amazonaws.com/public/images/6463db46-a5e5-497a-8b7f-0b468fbe911d_1411x911.png)
*SemiAnalysis Estimates*

## **The Real AI Superpowers**

Datacenter power capacity growth will accelerate from a 12-15% CAGR to a 25% CAGR over the next few years. Global Datacenter Critical IT power demand will surge from 49 Gigawatts (GW) in 2023 to 96 GW by 2026, of which AI will consume ~40 GW. In reality the buildout is not this smooth and there is a real power crunch coming soon.

![](https://substack-post-media.s3.amazonaws.com/public/images/1bad42d2-36a2-4c27-b85e-ab8aa4e5d92b_1553x987.png)
*SemiAnalysis Estimates*

The need for abundant, inexpensive power, and to quickly add electrical grid capacity while still meeting hyperscalers’ carbon emissions commitments, coupled with chip export restrictions, will limit the regions and countries that can meet the surge in demand from AI Datacenters.

Some countries and regions such as the US will be able to respond flexibly with a low electrical grid carbon intensity, low-cost fuel sources with supply stability, while others such as Europe will be effectively handcuffed by geopolitical realities and structural regulatory constraints on power. Others will simply grow capacity without care for environmental impact.

## **Key Needs of Training and Inference**

AI Training workloads have unique requirements that are very dissimilar to those of typical hardware deployed in existing datacenters.

First, models train for weeks or months, with network connectivity requirements being relativity limited to training data ingress. Training is latency insensitive and does not need to be near any major population centers. AI Training clusters can be deployed essentially anywhere in the world that makes economic sense, subject to data residency and compliance regulations.

The second major difference to keep in mind is also somewhat obvious – AI Training workloads are extremely power hungry and tend to run AI hardware at power levels closer to their Thermal Design Power (TDP) than would a traditional non-accelerated hyperscale or enterprise workload. Additionally, while CPU and storage servers consume on the order of 1kW, each AI server is now eclipsing 10kW. Coupled with the insensitivity towards latency and decreased importance of proximity to population centers, this means that the availability of abundant quantities of inexpensive electricity (and in the future – access to any grid supply at all) is of much higher relative importance for AI Training workloads vs traditional workloads. Incidentally, some of these are requirements shared by useless crypto mining operations, sans the scaling benefits of >100 megawatt in singular sites.

Inference on the other hand is eventually a larger workload than training, but it can also be quite distributed. The chips don’t need to be centrally located, but the sheer volume will be outstanding.

## **Datacenter Math**

AI Accelerators achieve relatively high utilization rates (in terms of power usage, not MFU). The expected average power (EAP) from normal operation per DGX H100 server is ~10,200 W, which works out to be 1,275W for each of the 8 GPUs per server. This incorporates the 700W Thermal Design Power (TDP) of the H100 itself, along with about 575W (allocated per GPU) for the Dual Intel Xeon Platinum 8480C processors and 2TB of DDR5 memory, NVSwitches, NVLink, NICs, retimers, network transceivers, etc. Adding the power needs for storage and management servers as well as various networking switches for an entire SuperPOD gets us to an effective power requirement of 11,112W per DGX server or 1,389W per H100 GPU. The DGX H100 configuration is somewhat overprovisioned with respect to storage and other items when compared to the HGX H100, which we account for. Companies like Meta have released enough information about their full configuration to estimate system level power consumption.

![](https://substack-post-media.s3.amazonaws.com/public/images/3d35bdb0-8f62-42a2-a936-182d3f23a9d8_1506x1216.png)
*NVIDIA DGX SuperPOD Datacenter Design*

Critical IT Power is defined as the usable electrical capacity at the datacenter floor available to compute, servers and networking equipment housed within the server racks. It excludes the power needed to run cooling, power delivery and other facility related systems in the datacenter. To calculate the Critical IT Power capacity that needs to be built or purchased in this example, add up the total expected power load of the IT equipment deployed. In our example below, 20,480 GPUs at 1,389W per GPU equates to 28.4 MW of Critical IT Power Required.

To get to the total power that the IT equipment is expected to consume (Critical IT Power Consumed), we need to apply a likely utilization rate relative to Critical IT Power Required. This factor accounts for the fact that the IT equipment typically does not run at 100% of its design capability and may not be utilized to the same degree over a 24-hour period. This ratio is set to 80% in the example.

On top of the Critical IT Power Consumed, operators must also supply power for cooling, to cover power distribution losses, lighting and other non-IT facility equipment. The industry measures Power Usage Effectiveness (PUE) to measure the energy efficiency of data centers. It's calculated by dividing the total amount of power entering a data center by the power used to run the IT equipment within it. It of course is a very flawed metric, because cooling within the server is considered “IT equipment”. We account for this by multiplying the Critical IT Power Consumed by the Power Usage Effectiveness (PUE). A lower PUE indicates a more power efficient datacenter, with a PUE of 1.0 representing a perfectly efficient datacenter, with no power consumption for cooling or any non-IT equipment. A typical enterprise colocation PUE is around 1.5-1.6, while most hyperscale datacenters are below 1.4 PUE, with some purpose build facilities (such as Google’s) claim to achieve PUEs of below 1.10. Most AI Datacenter specs aim for lower than 1.3 PUE. The decline in industry-wide average PUE over the last 10 years, from 2.20 in 2010 to an estimated 1.55 by 2022 has been one of the largest drivers of power savings and has helped avoid runaway growth in datacenter power consumption.

For example at 80% utilization rate and a PUE of 1.25, the theoretical datacenter with a cluster of 20,480 GPUs would on average draw 28-29MW of power from the grid, adding up to 249,185 Megawatt-hours per year, which would cost $20.7M USD per year in electricity based on average US power tariffs of $0.083 per kilowatt-hour.

![](https://substack-post-media.s3.amazonaws.com/public/images/92ae3573-7fc5-4ed1-a1f4-359e0f41187b_1126x943.png)

## **Datacenter Layouts and Constraints**

While the DGX H100 server requires 10.2 kilowatts (kW) of IT Power, most colocation datacenters can still only support a power capacity of ~12 kW per rack, though a typical Hyperscale datacenter can deliver higher power capacity.

![](https://substack-post-media.s3.amazonaws.com/public/images/4d2a0109-8514-45f5-addf-6fc5b8c68f7a_1806x1006.png)
*NVIDIA DGX SuperPOD Datacenter Design*

Server deployments will therefore vary depending on the power supply and cooling capacity available, with only 2-3 DGX H100 servers deployed where power/cooling constrained, and entire rows rack space sitting empty to double the power delivery density from 12 kW to 24 kW in colocation datacenters. This spacing is implemented to resolve cooling oversubscription aswell.

![](https://substack-post-media.s3.amazonaws.com/public/images/538d01af-834d-483b-9b4b-5fb494a95add_2410x840.png)
*NVIDIA DGX SuperPOD Datacenter Design*

As datacenters are increasingly designed with AI workloads in mind, racks will be able to achieve power densities of 30-40kW+ using air cooling by using specialized equipment to increase airflow. The future use of direct to chip liquid cooling opens the door to even higher power density by [potentially reducing per rack power usage](https://www.supermicro.com/white_paper/white_paper_Liquid-Cooling-Solutions.pdf) by 10% by eliminating the use of fan power, and lowering PUE by 0.2-0.3 by reducing or eliminating the need for ambient air cooling, though with PUEs already at 1.25 or so, this will be the last wave of meaningful PUE gains to be had.

![](https://substack-post-media.s3.amazonaws.com/public/images/e1a7a62e-6e67-461d-8c69-e122921f02df_1357x954.png)
*Supermicro Liquid Cooling Whitepaper*

Another important consideration that many operators raise is that individual GPU server nodes are best positioned near each other to achieve acceptable cost and latency. A rule of thumb used is that racks from the same cluster should be at most 30 meters from the network core. The short reach enables lower cost multimode optical transceivers as opposed to expensive single mode, which can often reach multiple km of reach. The specific multimode optical transceiver typically used by Nvidia to connect GPUs to leaf switches has a short range of up to 50m. Using longer optical cables and longer reach transceivers to accommodate more distant GPU racks will add costs with much more expensive transceivers needed. Future GPU clusters utilizing other scale-up network technology will also require very short cable runs to work properly. For instance, in [Nvidia’s yet to be deployed NVLink scale-up network for H100 clusters](https://www.semianalysis.com/p/nvidias-optical-ascent-1b-revenue),  which supports clusters of up to 256 GPUs across 32 nodes and can deliver 57.6 TB/s of all-to-all bandwidth, the maximum switch-to-switch cable length will be 20 meters.

![](https://substack-post-media.s3.amazonaws.com/public/images/7238a422-8aa2-47cd-946a-7e3093af69e3_2535x1390.png)
*NVIDIA H100 Architectural White Paper*

The trend towards higher power density per rack is driven more by networking, compute efficiency and cost per compute considerations – with regards to datacenter planning, as the cost of floor space and data hall space efficiency is an generally an afterthought. Roughly 90% of colocation datacenter costs are from power and 10% is from physical space.

The data hall where IT equipment is installed is typically only about 30-40% of a datacenter’s total gross floor area, so designing a data hall that is 30% larger will only require 10% more gross floor area for the entire datacenter. Considering that [80% of the GPU cost of ownership is from capital costs](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the), with [20% related to hosting (which bakes in the colocation datacenter costs) the cost of additional space is a mere 2-3% of total cost of ownership for an AI Cluster](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the).

Most existing colocation datacenters are not ready for rack densities above 20kW per rack. Chip production constraints will meaningfully improve in 2024, but certain hyperscalers and colos run straight into a datacenter capacity bottleneck, because they were flat footed with AI – most notably within colocation datacenters, as well as a power density mismatch – where the limits of 12-15kW power in traditional colocation will be an obstacle to achieving ideal physical density of AI super clusters.

Rear door heat exchangers and direct to chip liquid cooling solutions can be deployed in newly built datacenters to solve the power density problem. However, it is much easier to design a new facility from the ground up incorporating these solutions than it is to retrofit existing facilities – realizing this, Meta has [halted development of planned datacenter projects](https://www.datacenterdynamics.com/en/news/exclusive-after-meta-cancels-odense-data-center-expansion-other-projects-are-being-rescoped/) to rescope them into datacenters [catering specifically to AI workloads](https://www.datacenterdynamics.com/en/analysis/how-meta-redesigned-its-data-centers-for-the-ai-era/).

Meta had the worst datacenter design in terms of power density of all the hyperscalers, but they woke up and shifted very quickly. Retrofitting an existing datacenter is costly, time consuming, and in some cases may not even be possible – there may not be the physical space to install additional units of 2-3 MW generators, Uninterruptable Power Supplies (UPSs), switching gear or additional transformers, and redoing plumbing to accommodate the Cooling Distribution Units (CDUs) needed for direct to chip liquid cooling is hardly ideal.

![](https://substack-post-media.s3.amazonaws.com/public/images/f988c129-702b-4f1b-bea9-02d7fc302fd4_2472x1306.png)
*NVIDIA DGX SuperPOD Datacenter Design*

## **AI Demand vs Current Datacenter Capacity**

Using a line-by-line unit shipment forecasts by accelerator chip based on our [AI Accelerator Model](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and) together with our estimated chip specifications and modeled ancillary equipment power requirements, we calculate total AI Datacenter Critical IT Power needs for the next few years.

![](https://substack-post-media.s3.amazonaws.com/public/images/dd411a4d-2b02-4f43-a20b-888a04a64de2_1553x987.png)
*SemiAnalysis Estimates*

As mentioned above, total Datacenter Critical IT Power demand will double from about 49 GW in 2023 to 96 GW by 2026, with 90% of the growth coming from AI-related demand. This is purely from chip demand, but [physical datacenters](https://www.semianalysis.com/p/datacenter-model) tell a different story.

Nowhere will the impact be felt more than in the United States, where our satellite data shows the majority of AI Clusters are being deployed and planned, meaning Datacenter Critical IT Capacity in the US will need to triple from 2023 to 2027.

![](https://substack-post-media.s3.amazonaws.com/public/images/2f8168e8-e7ca-4006-bab6-e93b55151e83_1698x514.png)
*SemiAnalysis Estimates*

Aggressive plans by major AI Clouds to roll out accelerator chips highlight this point. OpenAI has [plans to deploy hundreds of thousands of GPUs](https://www.semianalysis.com/p/microsoft-swallows-openais-core-team) in their largest multi-site training cluster, which requires hundreds of megawatts of Critical IT Power. [We can track their cluster size quite accurately by looking at the buildout of the physical infrastructure, generators, and evaporation towers](https://www.semianalysis.com/p/datacenter-model). Meta discusses an installed base of 650,000 H100 equivalent by the end of the year. GPU Cloud provider CoreWeave has [big plans to invest $1.6B in a Plano, Texas facility](https://www.datacenterdynamics.com/en/news/coreweave-plans-16bn-ai-cloud-data-center-in-plano-texas/), implying plans to spend for construction up to 50MW of Critical IT Power and install 30,000-40,000 GPUs in that facility alone, with a clear pathway to a whole company 250MW datacenter footprint (equivalent to 180k H100s), and they have plans for multiple hundreds of MW in a single site in planning.

Microsoft has the largest pipeline of datacenter buildouts pre-AI era (see January 2023 data below), and [our data shows its skyrocketed since](https://www.semianalysis.com/p/datacenter-model). They have been gobbling any and all colocation space they can as well aggressively increasing their datacenter buildouts[. AI laggers like Amazon](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will) have made press releases about nuclear powered datacenters totaling 1,000MW, but to be clear they are lagging materially on real near term buildouts as they were [the last of the hyperscalers to wake up to AI](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will). Google, and Microsoft/OpenAI both have plans for larger than Gigawatt class training clusters in the works.

![](https://substack-post-media.s3.amazonaws.com/public/images/280f1cf9-216f-472b-86d6-0b817c5255b5_2953x1654.png)
*Structure Research*

From a supply perspective, sell side consensus estimates of 3M+ GPUs shipped by Nvidia in calendar year 2024 would correspond to over 4,200 MW of datacenter needs, nearly 10% of current global datacenter capacity, just for one year’s GPU shipments. The consensus estimates for Nvidia’s shipments are also very wrong of course. Ignoring that, AI is only going to grow in subsequent years, and Nvidia’s GPUs are [slated to get even more power hungry](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition), with 1,000W, 1,200W, and 1,500W GPUs on the roadmap. Nvidia is not the only company producing accelerators, with [Google ramping custom accelerator production rapidly](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion). Going forward, Meta and Amazon will also ramp their in house accelerators.

This reality is not lost on the top global hyperscalers – who are rapidly ramping up datacenter construction and colocation leasing. AWS literally bought a 1000MW [nuclear-powered datacenter campus](https://www.datacenterdynamics.com/en/news/aws-acquires-talens-nuclear-data-center-campus-in-pennsylvania/) for $650M USD. Though only the very first building with 48MW of capacity is likely to be online in the near term, this provides a valuable pipeline of datacenter capacity for AWS without being held up waiting for power generation or grid transmission capacity. We think a campus of such mammoth proportions will take many years to fully ramp to the promised 1,000 MW of Critical IT Power.

![](https://substack-post-media.s3.amazonaws.com/public/images/e94eed35-8a5b-44c1-a02e-6aeae001a145_1886x1078.png)
*Datacenter Dynamics*

## **The Carbon and Power Cost of AI Training and Inference**

Understanding power requirements for training popular models can help gauge power needs as well as understand carbon emissions generated by the AI industry. [Estimating the Carbon Footprint of BLOOM, a 175B Parameter Language Model](https://arxiv.org/abs/2211.02001) examines the power usage of training the BLOOM model at the Jean Zay computer cluster at IDRIS, a part of France’s CNRS. The paper provides empirical observations of the relationship of an AI Chip’s TDP to total cluster power usage including storage, networking and other IT equipment, all the way through the actual power draw from the grid.

Another paper, [Carbon Emissions and Large Neural Network Training](https://arxiv.org/abs/2104.10350), reports on the training time, configuration and power consumption of training for a few other models. Power needs for training can vary depending on the efficiency of models and training algorithms (optimizing for Model FLOPs Utilization – MFU) as well as overall networking and server power efficiency and usage, but the results as reproduced below are a helpful yardstick

![](https://substack-post-media.s3.amazonaws.com/public/images/37d56f20-7ac9-419c-b1cf-a1ada44c0838_1518x632.png)
*Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model , Carbon Emissions and Large Neural Network Training*

The papers estimate the carbon emissions from training these models by multiplying the total power consumption in kWh by the [carbon intensity of the power grid](https://www.epa.gov/egrid/data-explorer) that the datacenter is running on. Eagle eyed readers will note the very low carbon intensity of 0.057 kg CO2e/kWh for training the BLOOM model in France, which sources 60% its electricity from nuclear power, far lower than the [0.387 kg CO2e/kWh average for the US](https://www.epa.gov/egrid/data-explorer). We provide an additional set of calculations assuming the training jobs are run on datacenters connected to a power grid in Arizona, one of the leading states for datacenter buildouts currently.

The last piece of the emissions puzzle to consider is embodied emissions, defined as the total carbon emissions involved in manufacturing and transporting a given device, in this case the accelerator chip and related IT equipment. Solid data on embodied emissions for AI Accelerator Chips is scarce, but some have roughly estimated the figure at 150kg of CO2e per A100 GPU and 2,500kg of CO2e for a server hosting 8 GPUs. Embodied emissions work out to be about 8-10% of total emissions for a training run.

![](https://substack-post-media.s3.amazonaws.com/public/images/5dbf1092-7f5c-4a15-8b4c-ce80d891c6ef_1458x991.png)
*Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model , Carbon Emissions and Large Neural Network Training , EPA eGrid , SemiAnalysis Estimates*

The carbon emissions from these training runs are significant, with one GPT-3 training run generating 588.9 metric tons of CO2e, equivalent to the [annual emissions of 128 passenger vehicles](https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle). Complaining about GPT-3 training emissions is like recycling plastic water bottles but then taking a flight every few months. Literally irrelevant virtue signaling.

On the flip side, it is a safe bet that there were many iterations of training runs before settling down on the final model. In 2022, [Google emitted a total of 8,045,800 metric tons of CO2e](https://sustainability.google/reports/google-2023-environmental-report/) from its facilities including datacenters, before factoring in any offsets from renewable energy projects. All this means is GPT-3 is not effecting carbon output of the world, but with the FLOPS of GPT-4 multiple orders of magnitude more, and the current OpenAI training run, more than an magnitude above that, the carbon emissions of training are going to start to become sizeable in a few years.

For inference, we have detailed the economics of AI Cloud hosting in our posts on [GPU Cloud Economics](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the) and on [Groq Inference Tokenomics](https://www.semianalysis.com/p/groq-inference-tokenomics-speed-but). A typical H100 server with 8 GPUs will emit about 2,450 kg of CO2e per month and require 10,200 W of IT Power – a cost of $648 per month assuming $0.087 per kilowatt-hour (KWh).

![](https://substack-post-media.s3.amazonaws.com/public/images/cb6ee4a0-5d69-466b-965f-fc42ebd93924_1912x1365.png)
*SemiAnalysis Estimates*

## **Building out AI Infrastructure at Scale – What makes a Real AI Superpower?**

The AI Datacenter industry is going to need the following:

- Inexpensive electricity costs given the immense amount of power to be consumed on an ongoing basis, particularly since inference needs will only compound over time.
- Stability and robustness of energy supply chain against geopolitical and weather disturbances to decrease likelihood of energy price volatility, as well as the ability to quickly ramp up fuel production and thus rapidly provision power generation at great scale.
- Power generation with a low carbon intensity power mix overall, and that suitable to stand up massive quantities of renewable energy that can produce at reasonable economics.

Countries that can step up to the plate and tick off those boxes are contenders to be Real AI Superpowers.

## **Electricity Tariffs, Power Mix, and Carbon Intensity**

![](https://substack-post-media.s3.amazonaws.com/public/images/6fec2a9c-7a44-4eaa-83c3-55049d3174c6_2446x1464.png)
*US EIA, Various National and Regional Electrical Distribution Organizations*

Comparing global electricity tariffs, the US has among the lowest power prices in the world at $0.083 USD/kWh on average. Natural gas production in the US is abundant and has surged since the [shale gas revolution of the early 2000s](https://www.strausscenter.org/energy-and-security-project/the-u-s-shale-revolution/), which made the US the world’s largest producer of natural gas. Almost 40% of the electricity generation in the US is fueled by natural gas, with low power generation prices chiefly driven by the abundance of dry natural gas production from shale formations. Natural gas prices will remain depressed in the US due to fracking for oil and the increasing percentage of gas coming from wells, and so natural gas bulls that ping us every few weeks about datacenter power consumption should probably calm down.

The fact that the US is energy independent in natural gas adds geopolitical stability to prices, and the widespread distribution of gas fields across the US adds supply chain robustness, while a [proven reserve of 20 years of consumption](https://www.eia.gov/energyexplained/natural-gas/how-much-gas-is-left.php) adds longevity to energy supply, though these reserve estimates have increased over the years, doubling since 2015 and up 32% in 2021 alone.

![](https://substack-post-media.s3.amazonaws.com/public/images/bf313653-f6bd-4ea6-894c-e5ebd258ff9a_1891x1273.png)
*US Energy Information Administration*

In addition, the US has a far greener energy mix than most of the other contenders, having reduced its coal mix of power generation from 37% in 2012 to 20% by 2022 with the coal mix forecast to reach 8% by 2030 as natural gas and renewables step in to fill the gap. This compares to India at a 75% coal mix, China at a 61% coal mix, and even Japan still at a 34% coal mix in 2022. This difference is very impactful as coal power plants have a [carbon intensity of 1.025 kg/kWh CO2e, over double that of natural gas plants at 0.443 kg/kWh CO2e](https://www.eia.gov/todayinenergy/detail.php?id=48296). Datacenters built in the US will therefore rely on a far cleaner fuel mix for necessary baseload and overnight power generation than in many other countries.

![](https://substack-post-media.s3.amazonaws.com/public/images/6e1d9b5b-6ebd-47d6-9643-d5355df394b8_2055x1377.png)
*US Energy Information Administration*

The energy supply situation in the US stands in stark contrast to East Asia and Western Europe, which host about 15% and 18% of global datacenter capacity respectively. While the US is self-sufficient in natural gas, countries such as Japan, Taiwan, Singapore, and Korea import well over 90% of their gas and coal needs.

Japan’s power mix is tilted towards these imported fuel types, with 35% natural gas, 34% coal, 7% hydro and 5% nuclear, resulting in average industrial electricity tariffs of $0.152 USD/kWh in 2022, 82% higher than the US at $0.083 USD/kWh. Taiwan and Korea have similar power mixes dominated by natural gas imports and have electricity tariffs of about $0.10 to $0.12 USD/kWh, though this is after $0.03 to $0.04 of effective subsidies given the state owned electric companies have been running massive losses, with Korea’s [KEPCO losing $24B in 2022](https://www.ft.com/content/3533347c-cd50-4e42-bd15-e48173b003d7) and Taiwan’s Taipower [losing $0.04 USD per kWh](https://www.taiwannews.com.tw/en/news/4839443) sold.

In ASEAN, Singapore is another datacenter hub that has a heavy reliance on imported natural gas at 90% of its power generation mix, resulting in a high electricity tariff of $0.23 USD/kWh in 2022. The 900MW of Critical IT Power that Singapore hosts is large relative to its power generation capacity and consumes over 10% of Singapore’s national power generation. For this reason, Singapore had placed a four-year moratorium on new datacenter builds which only lifted in July 2023 with approval of a mere 80MW of new capacity. This constraint has spawned an enormous development pipeline of up to 1,000 MW of capacity in Johor Bahru, Malaysia, just a few miles north of Singapore, with much of it being driven by Chinese companies trying to "internationalize" and increasingly distancing themselves from their mothership parent companes in China. Indonesia also has a significant pipeline.

China’s industrial electricity tariff of $0.092 USD/kWh is on the low end of the range for electricity tariffs, but like many other emerging markets, China has a very dirty power generation mix, with 61% of generation from coal. This is a significant disadvantage from an emissions perspective, and new coal power plants are still being approved despite China significantly leading the world in renewable power installation. Any hyperscale or AI company that has a net-zero emissions commitment will be fighting an uphill battle with respect to that goal given coal’s [carbon intensity of 1.025 kg/kWh CO2e vs natural gas at 0.443 kg/kWh CO2e](https://www.eia.gov/todayinenergy/detail.php?id=48296).

![](https://substack-post-media.s3.amazonaws.com/public/images/e6e8efac-1e93-41c4-8364-7db3182dafad_2275x1521.png)
*Ember Electricity*

China is largely self-reliant on coal used for power generation, but it imports the vast majority of its other energy needs, with over 70% of its petroleum and LNG exports shipped through the Strait of Malacca, and therefore subject to the so-called “[Malacca Dilemma](https://gjia.georgetown.edu/2023/03/22/chinas-economic-security-challenge-difficulties-overcoming-the-malacca-dilemma/)”, meaning that for strategic reasons China cannot pivot towards natural gas and will have to rely on adding coal and nuclear for baseload generation.  China does lead the world in adding renewable capacity, however, the huge existing base of fossil fuel-based power plants and continued reliance on adding coal power to grow overall capacity means that in 2022 only 13.5% of total power generation was from renewables.

To be clear, China is the best country at building new power generation, and they would likely lead in the construction of gigawatt scale datacenters if they were enabled to, but they cannot, so the US is dominating here.

![](https://substack-post-media.s3.amazonaws.com/public/images/c1b41678-81d7-4f60-8245-7d25d97b0346_787x602.png)
*US Energy Information Administration*

And this is all before looking the elephant in the room squarely in the eyes, specifically, [the ongoing AI Semiconductor export controls](https://www.semianalysis.com/p/wafer-wars-deciphering-latest-restrictions) put into place by the US’s Bureau of Industry and Security, which has the intent of almost entirely denying China from obtaining any form of AI chips. In this respect, the exports control whack-a-mole game is ongoing, with Nvidia tweaking its chips to [comply with the latest changes](https://www.semianalysis.com/p/nvidias-new-china-ai-chips-circumvent) to the controls. The H20 has a huge ramp in Q2 and on for China, but this is still nowhere close to the 35% to 40% of AI chips China would import if they were allowed to.

In Western Europe, electricity generation has been slowly declining, with a 5% drop cumulatively over the past five years. One reason for the drop is that nuclear power has become a political non-starter, causing nuclear power generation to decline massively, for example declining 75% in Germany from 2007 to 2021. A strong focus on the “environment” has led to dirty fuel sources such as coal also declining dramatically over the same time, although the cleanest power in the world nuclear has been replaced with coal and natural gas in some instances. Renewable energy is increasing within Europe’s power mix, but not fast enough, leaving many Europeans countries to scramble to pivot more towards natural gas, which now stands at 35-45% of the power generation mix for major Western European countries.

![](https://substack-post-media.s3.amazonaws.com/public/images/a619727c-e1d8-4d83-acb1-f67ad8d6a4c2_2059x1378.png)
*Ember Electricity*

Given Europe’s energy situation, the EU average industrial tariff reached $0.18 USD/kWh in 2022, with the UK at $0.235 USD/kWh and datacenter heavyweight Ireland at $0.211 USD/kWh, nearly triple the electricity cost in the US. Like Asia, Europe imports over 90% of its gas in the form of LNG, mainly sourced from the Middle East (and also still [from Russia](https://www.reuters.com/business/energy/lng-imports-russia-rise-despite-cuts-pipeline-gas-2023-08-30/), despite the ongoing war), so their entire industrial base, not just Datacenters, is subject to geopolitical risk, as most readers will vividly remember from the onset of the war in Ukraine. Given the political and geopolitical realities, adding a massive amount of power generation capacity to host the AI Datacenter boom in Europe would be very challenging.

Furthermore, Europe is allergic to building as proven by many regulations and restrictions on the datacenter and manufacturing industries already in place. While small projects and pipelines for datacenters are in progress, especially in France who at least has somewhat realized the geopolitical necessity, no one is planning to build Gigawatt class clusters in Europe. Europe has less than 4% of globally deployed AI Accelerator FLOPs based on our estimates.

As discussed, electricity pricing will matter considerably given the scale of AI clusters to be deployed, amounting to hundreds of millions of dollars of cost difference depending where the clusters are deployed. Locating AI Datacenters in Europe or Asia would easily double or triple the power costs vs building datacenters in the US. Furthermore construction costs are also higher due to the lack of skills.

The Middle East is another location that is racing to start datacenter construction and they scores very high among the Real AI Superpower criteria in some metrics, with some of the lowest electricity tariffs globally, and very high viability for the use of Solar power. Indeed, the Middle East has a very strong pipeline with the UAE expected to nearly triple Datacenter Critical IT Power from 115MW in 2022 to 330MW by 2026.

Saudi Arabia has already gotten involved with [the purchase of a measily 3,000 H100s](https://www.ft.com/content/c93d2a76-16f3-4585-af61-86667c5090ba) so far for its research institution, with plans to build its own LLM. Microsoft also announced plans to establish a datacenter in Saudi Arabia, following on the [launch of its Qatar datacenter](https://news.microsoft.com/en-xm/2022/08/31/microsoft-opens-first-global-datacenter-region-in-qatar-bringing-new-opportunities-for-a-cloud-first-economy/) in 2022. Saudi Arabia leads the pack however, with a current Critical IT Power of 67MW, but with plans to leapfrog the UAE and reach 530MW in the next few years.

Meanwhile, AI startup Omniva, which has just barely exited from stealth mode, purportedly aims to build low-cost AI Datacenter facilities in the Middle East with significant backing from a Kuwaiti royal family member. It boasts ex AWS, Meta and Microsoft staff among key personnel. They are the only one with real traction on the ground movement and have the most impressive talent / pedigree, but they also have a legal battle with Meta having sued an employee who allegedly stole documents and recruited 8 former employees to join.

**Below we are going to quantify the power price differences, transformer infrastructure, power generation capabilities, and a breakdown of global datacenter capex requirements by UPS, Generator, Switch Gear, Power Distribution, CRAH/CRAC, Chillers, Cooling towers, Valves/pipes/pumps, Project Management Facility Engineering, Lighting, Management, Security, IT Enclosures and containment, raised floors/dropped ceilings, and Fire protection.**

**We will also dive deeper into Meta’s buildouts specifically. We will also discuss the merits of solar versus wind on the renewable side and regional differences for deploying this type of power. Power storage capabilities, and carbon emissions are also touched on.**

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

![](https://substack-post-media.s3.amazonaws.com/public/images/9d2bade3-4a05-402f-9ee6-c45e4a3403cb_970x1060.png)
*US EIA, Various National and Regional Electrical Distribution Organizations*

---
title: "Quadruped State of The Market - Unitree, Boston Dynamics, ANYbotics, DEEP Robotics, and The Rising Application Ecosystem"
subtitle: "Quadrupeds Superior Scalability, Unitree's Incredible Production, Third Party Providers Introduce New Dynamics, Novel Applications And Opportunities, Unitree's Impossible BoMs, Quadruped TAMs"
date: 2025-10-20
source: https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree
crawled: 2026-09-15
authors: ["Reyk Knuhtsen", "Dylan Patel", "Niko Ciminelli", "Joe Ryu", "Jeremie Eliahou Ontiveros", "Robert Ghilduta"]
tags: ["Robotics"]
audience: only_paid
paywalled: true
---

# Quadruped State of The Market - Unitree, Boston Dynamics, ANYbotics, DEEP Robotics, and The Rising Application Ecosystem

**Quadrupeds Superior Scalability, Unitree's Incredible Production, Third Party Providers Introduce New Dynamics, Novel Applications And Opportunities, Unitree's Impossible BoMs, Quadruped TAMs**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Quadrupeds are the most advanced general-purpose robots today. While they don’t grab as many headlines as their Humanoid counterparts, their [Level 2 Autonomy](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/) coming online opens up a plethora of new market opportunities previously unavailable to robotics. Understanding the Quadrupeds market and ecosystem is important to glimpse the future of autonomous robotics.

Currently, we see two main quadruped hardware providers: the Western pioneer Boston Dynamics and China’s hardware champion Unitree. ANYbotics/DEEP Robotics being notable players that we mention briefly. Raising all providers is a broader startup ecosystem emerging, leveraging new AI model architectures to augment the hardware, and software enabling multiple applications. We discuss these market dynamics, giving a future outlook, as well as new opportunities being unlocked.

We will also analyze detailed Bill of Materials of the Unitree Go2 and B2 including gearboxes, motors, drives, bearings, linkage bar, batteries, LiDAR, foot sensors, optical cameras, SoCs, cameras, and more. The important point here is that their margins are incredible, much higher than most believe. Unitree is not loss leading, they have high volume manufacturing at low cost cracked.

We also provide a framework for the Total Addressable Market (TAM) of the following industries: Oil & Gas, Semiconductor Fabs, and Datacenters. As well as component suppliers exposed to quadrupeds. All extremely topical given the rumored [upcoming Unitree IPO](https://www.reuters.com/business/autos-transportation/chinese-robotics-firm-unitree-eyeing-7-billion-ipo-valuation-sources-say-2025-09-08/) and their majority revenue share coming from quadrupeds.

Our Main Takeaways:

- Unitree benefits from a substantial cost advantage relative to Western peers.
- Unitree boasts a much broader product portfolio and faster product release cadence given China’s manufacturing supremacy.
- As hardware providers, Boston Dynamics (and to a lesser extent ANYBotics/DEEP Robotics) has seen Western deployments, benefiting from partial vertical integration.
- Unitree is currently more focused on Chinese industrial deployments, and its **security issues** pose barriers only in select markets
- However, Unitree has seen meaningful traction in Western research labs/institutes, combining their low-cost hardware and deep development kit with a strong open-source community of researchers.
- The third party application layer ecosystem continues to grow and facilitate quadruped deployments, increasing the capabilities of **all** quadrupeds.

## Why Quadrupeds Dominate Navigation Tasks

While drones, wheeled robots, tracked robots, and more [Level 2 Autonomous](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/) systems can also operate autonomously, the four-legged quadruped is one of the most flexible and adaptable designs for navigating the world. This opens up a plethora of new roles to be automated.

These cluttered and narrow areas are navigated with the quadruped’s dynamic walking, adjusting its position and bending its “knees.” This flexibility is essential in messy, obstacle-ridden environments, like chemical plants and construction sites.

![](https://substack-post-media.s3.amazonaws.com/public/images/d2560e11-fb6d-4e22-b455-d66aa7ef16bd_1372x684.jpeg)
*Source: Unitree*

Additionally, its form allows for many different sensors and components attached by system integrators, from LiDARs, to acoustic sensors, to image capturing, and more. In the case of an oil and gas facility where heat, sound, and imaging all come together, this is pivotal. All of these sensors can be built atop for longer-duration inspection thanks to the quadruped’s four-legged strength and sizable battery.

Wheeled robots, tracked robots, and drones could all be specialized for their desired use-cases but quadrupeds see the most upfront functionality as a general-purpose platform. This should lead to quadrupeds seeing more widespread use, driving costs down, and rendering them the most scalable form factor for Navigation tasks. But why aren’t the others as general-purpose?

### **Drones - Small And Delicate Navigation**

Drones have much higher speeds than a quadruped and cost significantly less. However, regulations may throttle them. In most cases, drones cannot truly run autonomously, requiring an operator to monitor constantly, especially in outdoor sights like construction

Moreover, safely approaching inspection areas remains a [large challenge](https://www.mdpi.com/1424-8220/21/6/2194) for drones. Getting close to walls, ceilings, or floors leads to turbulent airflow which can cause the drone to crash out. This is called “prop wash,” and it can cause drones to be “attracted” to walls at around ~1.5x the rotor diameter distance, ruining inspections.

One could alleviate this with more sensors but the drone battery is already short on life at ~30-45 minutes. Instead, quadrupeds hold up to hours of charge and are robust to collisions.

![](https://substack-post-media.s3.amazonaws.com/public/images/4aa8d1c2-823c-42a2-a083-25e41d43fc22_1920x1440.jpeg)
*Source: Coptrz*

### Wheeled Robots and Tracked Robots - Robust, But With Tradeoffs

Looking at alternatives, wheeled robots are faster [(~2m/s](https://clearpathrobotics.com/husky-a300-unmanned-ground-vehicle-robot/) vs 0.75-1 m/s) and sturdier than quadrupeds. Tracked robots are more [robust with better traction](https://www.academia.edu/123097297/_Wheels_vs_tracks_A_fundamental_evaluation_from_the_traction_perspective) but slower than quadrupeds (~0.4 m/s). Wheeled/tracked robots may be specialized for speed or payload specifically, but the tradeoff is again a less general-purpose, scalable platform.

Instead, quadrupeds resolve many challenges that bottlenecked wheeled/tracked robots.

**Lack of dynamic gait**: difficulty navigating narrow, confined spaces. For example, the [Argus](https://robot.martecsrl.it/download/argus.pdf) needs 2.5 meters of turning radius. This is exacerbated in cramped environments like chemical plants. Most quadrupeds are only about ~1m in length, granting them more flexibility to navigate.

![](https://substack-post-media.s3.amazonaws.com/public/images/d47b4466-5677-47c3-8a2f-25e136911ceb_2452x1266.png)
*Source: ANYBotics , An ANYmal passing through a narrow corridor*

**Navigating clutter**: wheeled/tracked robots may roll over objects on the ground, either damaging the objects, themselves, and potentially getting stuck. For tracked robots the clearance may only be 4-6cm, while wheeled robots can go up to 12cm. However there are tradeoffs to increasing wheel radii: larger wheels sacrifice stability and increase vehicle size, leading to pivot radius challenges but may be required to get over the “breakover angle” at the peak of a ramp.

![](https://substack-post-media.s3.amazonaws.com/public/images/188f0e35-c3ec-4f55-820c-84bdba2862d3_1920x1920.jpeg)
*Source: SuperDroidRobots*

**Different Height Surfaces**: Obvious, but crucial in many applications. Construction sites are full of obstacles, curbs, or stairs that might impede navigation. Ramps and elevators help, but compound robot deployment costs.

Tracked robots **can** sometimes climb [20cm](https://microwatt.com/wp-content/uploads/2021/08/exr-1-operating-guide.pdf)+ stairs, and even up to [45 degrees](https://www.taurob.com/inspector/), making stairs possible, but with some risk of toppling. Furthermore, crossing too large a gap (i.e. larger than wheel diameter) may cause the robot to get stuck vs quadrupeds which can gap [~30cm](https://www.anybotics.com/anymal-technical-specifications.pdf).

![](https://substack-post-media.s3.amazonaws.com/public/images/5ad68578-981c-45cf-8b2d-95a2eb97d2b9_1024x683.jpeg)

## Key Enablers of the Rise of Quadrupeds

Quadruped hardware was far too bulky, inefficient, and expensive before to justify their use, but now they’re highly capable:

- Breakthroughs in [li-ion batteries and cost reductions](https://www.econopolis.be/en/blog/posts/2024/may/is-double-digit-day-nearing-for-li-ion-batteries/) have shifted the field: formerly ~12kg battery in 2010 now weighs [~6kg](https://rmi.org/the-rise-of-batteries-in-six-charts-and-not-too-many-numbers/) via power density increases.
- Hardware makers transitioned from heavy, leaky, expensive ($1000s) hydraulic actuators to cheaper electric actuators.
- Sensors provide [Level 2](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility) robotics with “vision,” and are steadily improving and dropping in price. LiDARs price dropped by [orders of magnitude](https://futurism.com/price-eyes-autonomous-vehicles-drops-75k-just-250), cameras are [multiples higher in megapixels](https://www.phonearena.com/news/in-2024-54-mp-the-average-resolution-for-primary-smartphone-cameras_id163407), and Time-of-flight (or depth) sensors [doubled in distance](https://www.kitguru.net/peripherals/camera-peripherals/christopher-nohall/intel-announces-its-latest-realsense-depth-camera-d455/),
- Compute exponentially improved, from Nvidia’s Jetson TX1 ([2015](https://developer.nvidia.com/blog/nvidia-jetson-tx1-supercomputer-on-module-drives-next-wave-of-autonomous-machines/)) with 1TFLOP, to today’s Jetson Thor 2070 TFLOPS ([FP4](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/)).

Hardware developments now require the software for application layer functionality, and luckily many things are in place:

- Core Autonomy: The ability to plan, navigate, and control itself, like general-purpose AI models for acting in the real world
- Task-specific Software: These enable the quadruped to perform specific tasks, like reading gauges, detecting gas leaks, or analyzing thermal maps.
- System Integration: Connecting multiple sensors into the robot for inspecting and processing, and the robot to the infrastructure for data collection

This is no small task: **each** environment, sensor, or application often **demands a bespoke solution tailored** to both the job and the robot. Third party companies typically step in to provide this remaining solution atop the hardware.

Now with both hardware and software ready, the market is set to take off.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

## Setting The Stage

The quadruped hardware market currently is dominated by two players: Boston Dynamics and Unitree, while DEEP Robotics and ANYBotics lag behind. Boston Dynamics and ANYBotics are vertically integrated to an extent, controlling and designing their software/autonomy for streamlined deployments.

Unitree, and DEEP Robotics, take a hardware-first approach of multiple humanoids and quadrupeds. Working tightly with the research community and 3rd party ecosystem, others often leverage their hardware into an autonomous system.

**Boston Dynamics** helped pioneer humanoids, quadrupeds, and robust locomotion. Its quadruped, **Spot**, sees inspections in multiple environments. Boston Dynamics product line, including their warehouse arm “Stretch,” sees an annual revenue of $100M-$200M based on various reports.

![](https://substack-post-media.s3.amazonaws.com/public/images/6eac9662-528e-4467-892b-f36ab5ca6ec9_2560x1707.jpeg)
*Source: Boston Dynamics*

**DEEP Robotics** with a similar IP rating (IP67), battery life, and payload capacity to the industrial-grade Unitrees at 30%+ the cost, DEEP Robotics is set on industrial applications. At the moment, the company is rising fast, seeing ~[600 deployments around 40+ countries](https://www.morningstar.com/news/accesswire/1053303msn/deep-robotics-showcases-core-technologies-real-world-applications-of-embodied-intelligence-robots-at-waic-2025).

![](https://substack-post-media.s3.amazonaws.com/public/images/7ce2ef67-a1ae-4462-b685-a117e3ee7396_1200x472.jpeg)
*Source: DEEP Robotics*

**ANYBotics** spun out of ETH Zurich in 2016, one of the world’s premier robotics labs known for its cutting-edge locomotion research. The company now fits dangerous and dirty environments for its inspection tasks, bringing in an annual <[$27M revenue](https://www.zoominfo.com/c/anybotics/401723840).

![](https://substack-post-media.s3.amazonaws.com/public/images/50e7e909-21d1-442a-bbaf-a4279255d981_2732x2049.jpeg)
*Source: Siemens*

China’s **Unitree** dominates the quadruped market, holding an estimated [70%](https://news.qq.com/rain/a/20241005A03SNM00) share of global sales by volume in 2023. The company’s strong pricing and hardware captivates the research sector, and currently expands into industrial inspection markets. The company has surpassed annual revenues of [1B RMB](https://eu.36kr.com/en/p/3353252936479360) (~$140M).

![](https://substack-post-media.s3.amazonaws.com/public/images/39b7ea28-5b48-42ad-91fb-214c6325f93b_1200x1200.jpeg)
*Source: Unitree Spain , Unitree B1*

Unitree has a diverse product line, and their core manufacturing and assembly processes can be adapted to manufacture all at impressive costs.

- The Go2 quadruped is their low-end quadruped, priced at ~1/10th of the higher-ends and sees [applications in data collection](https://igrownews.com/unitree-robotics-latest-news/).
- The B1 is an industrial-grade, waterproof quadruped that Unitree markets as one of the most robust, versatile quadrupeds, boasting impressive payload capabilities of 20kg walking. ([Click here to see it carry 250kg up and down stairs!](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model))
- The B2 (not waterproof) builds atop the B1, adding longer battery life and stronger joints for 40kg walking payload. Though for the B2, wheels are an option
- The A2 (Stellar Hunter) is their newest quadruped, with less specs known, it exhibits impressive battery life, payload, and agility. Wheels are available as well.

![](https://substack-post-media.s3.amazonaws.com/public/images/a12d527e-7ba5-4524-a5b3-b659f70e7220_1128x191.jpeg)
*Source: Unitree*

## State of The Hardware Market - Unitree’s Pricing Advantage

The quadruped market is early, but **Unitree in 2023 alone is already ~10x the total shipments of the next competitor.** The numbers are significantly higher now, but this is the last public statements.

![](https://substack-post-media.s3.amazonaws.com/public/images/ce78bdac-667f-430f-bad6-d9b6faa913d5_1255x852.png)
*Source: SemiAnalysis Estimates, GGII Report*

This estimate includes Unitree’s lower-end Go2, **which they produce~[200 Go2 per day](https://semianalysis.com/core-research/) during peak season.**

Western quadrupeds typically use Robot-as-a-service, charging ~$10K per month. But without the Chinese supply chain strengths, they **still** cost significantly more than Unitree.

![](https://substack-post-media.s3.amazonaws.com/public/images/ac7f1425-7ab0-42fd-b711-8928136810fb_1314x599.png)
*Source: SemiAnalysis Estimates*

Unitree’s low-cost approach is impressive, and while the Western’s offer some application layer functionality over Unitree -- like a stable API or autonomy-- it’s often incomplete.

## Autonomy - Not The Full Picture

In [Level 2,](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility) we discussed how autonomy is coming online for these quadrupeds, but our quadruped hardware companies don’t fully satisfy this potential. This autonomy needs:

- Planning - Determining the environment around, and what plan to follow
- Navigating - Maneuvering in the environment appropriately
- Positioning - Setting up to safely and accurately perform inspections

Western quadrupeds’ inhouse autonomy ***can*** plan paths around people, obstacles, and hazards, and move reliably through facilities. But **positioning** is not always precise, often requiring AprilTags, like QR-codes that reorient the robot, or task-specific models for orientation. **Planning** can falter, with robots stalling or making poor choices in novel situations, like moving humans (some might just stop in place). **Navigation** remains fragile in cluttered environments. In the domains they’ve been trained on Westerns may perform well, but they may struggle in novelty.

As for Unitree, their inhouse autonomy is less-known. But judging from our research, it’s likely not much beyond the pre-programmed actions and teleoperation for now. While the Western quadrupeds developed a partial autonomy/software stack over Unitree, it may not necessarily earn them more deployments.

## How Is The Quadruped Market Evolving?

The market is still early, and two distinct business strategies have emerged.

- **Verticalization**: Western firms have taken this route, internalizing a majority of software, system integration, and autonomy to enable earlier applications since ~2018, though also not complete.
- **Ecosystem-based**: Unitree has chosen to focus on scaling its hardware while leveraging the broader research community and third-party ecosystem for software and deployment.

We do not expect quadruped-makers to build complete all-in-one offerings. Instead, the robots will serve as hardware platforms, with ever-improving external solutions layered on top. This will likely lead to a fragmented market of specialized players, including the original quadruped makers (OEMs), model vendors, system integrators, and software vendors. Oftentimes these application layer companies will own a majority of the deployment.

### Model Vendors - Autonomy For Sale

The advent of [Level 2 Autonomy](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility) has created an opening for **model vendors** who provide an impressive autonomy stack. Two prominent model vendors are emerging in the West:

- [FieldAI](https://www.fieldai.com/) - Providing “risk-aware” foundation models for quadrupeds and other Level 2 systems, now safely navigating many environments merely upon **drop-in**. FieldAI sees functional deployments across construction sites, industrial and energy plants, security patrol, and more.
- [Skild AI](https://www.skild.ai/) - Providing a proprietary “brain” commanding autonomy across locomotion, and manipulation across many embodiments. Skild AI is seeing deployments in construction and security patrol for their quadrupeds.

FieldAI and Skild AI leverage state-of-the-art AI models to fill the quadruped autonomy gaps, dynamically adapting to reliably perform their tasks alone. While Boston Dynamics and ANYbotics are exploring AI models, they’re currently behind the specialists, and Unitree seems to facilitate AI research better (explored in the software section).

![](https://substack-post-media.s3.amazonaws.com/public/images/ab672b8d-c7d1-45b5-8ec5-a3b8b3996e4e_500x507.jpeg)
*Source: FieldAI*

While new, both companies show promise and recently received massive investments, like Skild valued at [$4.5B](https://finance.yahoo.com/news/nvidia-samsung-back-4-5b-203049332.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAIHcrNjsMROHxh3QCTp5cdaIvG9LZiwuBY_-SA6bMyKj5JbUB4xNknmc-5LVf8_7_CkBEjx-Yuy7PwyVdpws-AvqeOGIoRS74_F4LlLM2SBvnDFi62gaYXXQF67GLAIOEmI2Em6imkK8rvm-myUYsYgMtAhUWMsb_8TSuH27g1Sw) and FieldAI’s funding reaching over [$400M](https://www.fieldai.com/news/fieldai-announces-over-400m-in-funds-raised-to-advance-embodied-ai-at-scale) after two rounds.

### System Integration - New Sensors and Infrastructure

As we’ve seen in [Level 1 Autonomy](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-1-intelligent-pick-and-place), integrations can make or break the viability of a robot. For quadrupeds of [Level 2 Autonomy](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility), their general-purpose nature mitigates previous burdens of reliability, but integration is not efficient yet.

System integrators help businesses adopt automation by configuring the quadruped to the customer’s desired workflow. This includes sensors, tools, and installation and setup with existing infrastructure. System integrators then adapt the quadruped platform for the application, relieving the burden from the customer/quadruped OEM. However, Boston Dynamics and ANYBotics are equipped with mature APIs/SDKs for streamlined system integration, while Unitree’s is apparently subpar. Some companies that perform this:

- [Chironix](https://chironix.com/news/chironix-robot-psychologists/) integrates quadrupeds with desired sensors and connects to existing infrastructure using their PilotOS software
- [IntuitiveRobots](https://www.intuitive-robots.com/our-payload-integrations-with-spot-robot/) integrates Spot with payloads, like acoustic sensors, and translating the data into visual imaging
- [SUPCON](https://en.people.cn/n3/2025/0219/c90000-20278525.html), a Chinese system integrator, successfully integrated quadrupeds into Saudi Arabian oil plant infrastructure

![](https://substack-post-media.s3.amazonaws.com/public/images/6b262d6c-fe40-4938-b382-28d33e3c5fde_1280x800.jpeg)
*Source: IntuitiveRobots*

System integrators haven’t quite “consolidated” yet, and large players like [SLB](https://www.slb.com/news-and-insights/newsroom/updates/2025/slb-partners-with-anybotics-to-advance-autonomous-robotic-operations-in-the-oil-,-a-,amp;-gas-sector) are only now beginning to integrate quadrupeds. However, customers and quadruped providers often choose their integrator based on deployment requirements, location, and company. In many cases, model providers and other application layer companies may own this segment too.

### Application Layer - APIs Are Nice, Not Vital

These companies complete the final layer of operations, either cementing mission autonomy, orchestrating the quadruped(s), and customer-facing dashboards. This makes the quadruped deployment as efficient as possible in long-run operations, filled by companies like

- [Lattice](https://www.anduril.com/article/anduril-unveils-lattice-for-mission-autonomy) (Anduril) provides a robust orchestration and planning layer, especially for fleets of robots
- [Formant](https://formant.io/resources/supported-devices/) provides optimized fleet management and telemetry, deployed in many cases with Spot, ANYmal, and **Unitree**.

![](https://substack-post-media.s3.amazonaws.com/public/images/59010264-7a93-419f-9bce-5e8efe7fc883_768x432.webp)
*Source: Formant*

ANYbotics and Boston Dynamics have an early advantage with their APIs and data collection platforms pre-built as well. However, as Unitrees grow in popularity, companies we’ve spoken to are learning to work with Unitree’s subpar integration platform regardless.

### Ecosystem Boosts All But Changes The Landscape

Thanks to [the need for automation](https://semianalysis.com/2025/03/11/america-is-missing-the-new-labor-economy-robotics-part-1/), the quadruped **ecosystem** is blossoming, bringing elegant deployment solutions online. This momentum could benefit hardware-centric players like Unitree, further leveling the application playing field. If quadruped hardware becomes commoditized, third-party vendors may emerge as the most influential forces in the Western quadruped landscape.

Quadruped producers can expect economic growth from either lowered hardware costs or increased capabilities/throughput. For Western quadrupeds, supply chains may need to be bolstered or a stronger ecosystem developed for **their specific** quadruped. For Unitree, their current strategy of dropping price and leveraging the ecosystem may be enough.

### Fragmentation Ensues Without a Hyperscaler

“Hyperscaler customers” are beginning to emerge in robotics, like Amazon with [one million robots](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model). When hyperscalers enter, markets often consolidate around a few players. Quadrupeds lack such a player today, leaving the field fragmented. When one does arrive, it will likely resemble AWS - sold as a service - rather than Tesla’s Optimus, which is used internally. Until then, Unitree’s hardware-first approach continues to benefit from the ecosystem players who continue capturing slices of deployments like those below.

### Potential Market Opportunities

Many factors drive the quadruped market, but Western economies demand quadrupeds more than countries with cheaper labor or capital. Western customer interest and adoption may primarily shape the market and companies’ evolution. Let’s look at new opportunities in Western markets over the next five years!

**Datacenters:** In hyperscaler datacenters, downtime can cost ~**[$1M per day](https://semianalysis.com/datacenter-industry-model/)**. These quadrupeds may inspect the electrical yards, determining on acoustic and thermal levels if the substation equipment is in order. For cooling infrastructure, ensuring no leakage, uneven coil temperatures, or unusual fan vibration could jeopardize the training/inferencing. The quadruped will likely be outside for much of its time, requiring a higher IP rating in harsh weather, or longer battery duration to inspect the massive sites.

![](https://substack-post-media.s3.amazonaws.com/public/images/010b0159-50b9-4a35-8791-f4f42a3249ca_1529x1776.webp)
*Source: FieldAI*

**Last-mile Delivery**: In contained areas like college campuses, smart cities, golf courses, etc, this is another promising application. In these environments, using a human courier at $18 per hour can cost up to $9 per delivery, while a robot can do the same for ~[$2.50 per delivery.](https://www.campusidnews.com/ohio-state-and-avride-robots-get-food-to-students-faster-and-cheaper) Using cars for such small areas is expensive, and human couriers are inefficient. Quadrupeds, and especially those fitted with wheels, are perfectly suited for this role and can turn an inefficient service into a profitable one.

![](https://substack-post-media.s3.amazonaws.com/public/images/f92d4fd5-2753-43aa-a87c-08bb5168eaf3_1200x675.webp)
*Source: InterestingEngineering*

**Security Patrol:** Unarmed security guards may patrol a facility 24/7, costing between $250K-$450K per year depending on wages and training. After keeping humans out of danger, quadrupeds also save the company significant money considering a RaaS monthly cost of $10K. In larger perimeters, wheels can be adopted for speedier patrol.

![](https://substack-post-media.s3.amazonaws.com/public/images/3e451e80-b0a0-456c-ab28-286509ae45bd_1794x973.png)
*Source: FieldAI*

## Where Do These Quadrupeds Work?

### Boston Dynamics’ Aim: Fabs

These facilities impose exacting standards; to qualify, a robot must be certified for low-particle compliance, a process that can take months. Once approved, however, the value is clear. A failed pipe can cost $30,000 to replace, but early repair after detection by a Spot robot can cost as little as $3,000.

![](https://substack-post-media.s3.amazonaws.com/public/images/3957a1b1-4f08-4b33-87d9-6636a2a92005_2560x1706.jpeg)
*Source: Intel*

Expanding into subfabs or cleanrooms is even harder. Some fabs may require that once a quadruped enters, it never leaves, demanding full autonomy and unwavering reliability. Furthermore, the strict particle limits may require sealed joints, specialized materials, and potentially even doggy-suit coverings.

### ANYBotics Aim: Dirty and Dangerous Environments

ANYbotics targets a different niche: environments requiring IP67 protection. This rating makes a robot dust-tight and [submersible](https://www.youtube.com/watch?v=eIuM-PWV8r0), critical for corrosive potassium mines or offshore rigs where saltwater would damage lesser machines. It is currently the only Western firm with an IP67-rated quadruped, though Boston Dynamics plans to ‘ruggedize’ Spot.

ANYbotics seems to be the only quadruped manufacturers developing an explosion-proof model, the ANYmal X, slated for 1H26. An ATEX (explosion-proof) rating would allow entry into Zone 1 areas with explosive gases, opening more of the oil and gas market.

![](https://substack-post-media.s3.amazonaws.com/public/images/66929568-938e-4489-a003-d1f0e8963de9_1232x742.png)
*Source: ANYBotics*

Explosion-proofing a legged robot is far more complex than for packaged devices or stationary gear. It requires changes to battery chemistry, nitrogen filling, and safeguards to eliminate sparks. The process can take up to two years and freezes the hardware design, slowing platform innovation but opening a major market and reducing safety risks.

We’ve heard system integrators discuss ANYBotics as the preferred option for corrosive, dangerous, and soon explosion-prone environments. After the paywall, we size the potential TAM for quadrupeds.

### DEEP Robotics: Electrical Infrastructure to Logistics

Conversations with DEEP Robotics elucidate their [strong performance](https://technode.com/2025/01/07/deep-robotics-delivers-x30-quadruped-robot-spock-for-singapore-power-inspections/) in [industrial inspection](https://www.digitaljournal.com/pr/news/accesswire/deep-robotics-leads-industrial-robot-1182802635.html), both domestically and [internationally](https://technode.com/2025/01/07/deep-robotics-delivers-x30-quadruped-robot-spock-for-singapore-power-inspections/), may foray into last-mile delivery. Using their robust wheeled robots and extensive network abroad, expansion seems feasible if Unitree’s cheaper wheeled quadrupeds stay away. While Unitree sees some industrial applications, Unitree seems more focused on a different market.

![](https://substack-post-media.s3.amazonaws.com/public/images/1bc62664-4a9e-4dce-a154-3516e43d4dba_800x600.jpeg)
*Source: DEEP Robotics*

### Unitree: From Industrial Use-cases In China to Research

While its high-end quadrupeds are up to 50% cheaper than Western models and boast a fully waterproof IP68 rating, they are not yet common in Western industrial markets. They are sometimes deployed in Chinese state grids, chemical plants, and steel mills, often as teleoperated [machines rather than fully autonomous ones](https://prosmt.ai/wp-content/uploads/2025/07/B2inspection_compressed.pdf).

![](https://substack-post-media.s3.amazonaws.com/public/images/2c825424-7fd9-4665-abf6-813f239e8ada_1170x406.png)
*Source: Unitree , Inspecting a Petrochemical plant in Guangdong*

Unitree also has a unique advantage in its **wheeled quadrupeds**. Which could beat out other Western quadrupeds in applications requiring speed, like patrolling large perimeters.

![](https://substack-post-media.s3.amazonaws.com/public/images/be5e0e5c-7566-4792-9eba-42c26984f1bb_2402x1203.png)
*Source: YouTube*

As the ecosystem continues to deploy Unitrees, they remain **dominant** in another community.

## Research - Unitree’s Forte

Unitree excels in serving the research community. Spot and ANYmal are often too costly for most labs, especially when testing control policies that risk damaging hardware. Researchers instead choose the lower-cost Go2, enabling large-scale R&D on Unitree’s software development kit (SDK). This feeds back into Unitree, as projects from top universities help build robust software models tailored to its platform. This capture will continually expand as Unitree pummels their cost curve.

![](https://substack-post-media.s3.amazonaws.com/public/images/70d33920-b62d-4915-8f83-8d1463aa69a7_1105x621.png)
*Source: NaVILA , a Unitree Go2 learning to navigate*

### “RL Robots?” Software Architectures In The New Era

Some have pointed to Unitree as a “special robot” designed for [Reinforcement Learning](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/) (RL). While a bit confusing, it highlights how unknown RL-friendly interfaces are. Let’s discuss the software architectures that make a robot especially good for policy learning!

Software layers translate perception into motion with minimal delay. Some developers use open-source frameworks like ROS, while major providers build custom stacks. Both serve the same role: abstracting hardware, managing sensor–actuator communication, and supplying libraries for kinematics and sensor fusion.

Deploying RL policies adds new demands. Known as [sim2real](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/), this process must present data in ways that narrow the gap between simulation and reality—a complex architectural challenge.

- **The Control Loop:** In this paradigm, the policy takes a “state vector” as input - a complex snapshot including current motor positions, recent sensor data, and past actions - and outputs an “action vector” containing new commands for motor position and torque. The platform must maintain precise, real-time timing to ensure that state observations and action executions remain synchronized, as even minor discrepancies can cause a trained policy to fail.

![](https://substack-post-media.s3.amazonaws.com/public/images/009c197d-9f71-4023-bd2a-ceabadcf9430_720x278.webp)
*Source: Binay Dhakal*

The robotic software platform orchestrates this entire process by continuously reading sensor data, constructing the state representation required by the RL policy, and then executing the resulting actions. This requires a robust communication and compute foundation.

- Communication Buses: Quadruped designers typically use a combination of buses. Real-time components like actuators, IMUs (for positioning/movement in space), and position encoders often run on reliable buses like Controller Area Network (CAN) or RS-485. In contrast, high-bandwidth sensors that enable perception—such as cameras, LiDAR, and microphones—will usually run over a bus like USB.

- Compute Architecture: The underlying compute architecture typically relies on general-purpose ARM processors for the main control board due to their power efficiency and strong embedded Linux support. These chips are often sufficient for executing locomotion policies and basic inference. However, for advanced applications requiring large [vision-language-action (VLA) models](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/), system integrators are increasingly turning to NVIDIA’s embedded computing platforms, particularly the Jetson series and the recently released Thor, which provide the necessary tensor acceleration for running large neural networks at the edge.

![](https://substack-post-media.s3.amazonaws.com/public/images/1f68a07e-0564-4171-8536-0f898e822929_1800x1200.webp)
*Source: Mehatronika , Nvidia Jetson Thor*

Not all software architectures are equal. Most quadrupeds provide basic walking and climbing controllers, while Unitree exposes direct motor control, enabling full control development. Boston Dynamics’ Spot offers this access, but only for a recurring annual fee.

This direct motor control is crucial for research, as learning is constrained under pre-set controllers. Rapid Motor Adaptation ([2020](https://ashish-kmr.github.io/rma-legged-robots/)), the first major paper on Unitree robots, showed real-time adaptation to difficult terrain—possible only through this openness. Since then, researchers have built some of the [first end-to-end locomotion systems](https://vision-locomotion.github.io/), from vision to motor control, with results that keep improving. This cutting-edge research is primarily performed with Unitree.

![](https://substack-post-media.s3.amazonaws.com/public/images/3a6747fe-2a70-41da-89a8-13e4bfa70764_2344x1105.png)
*Source: RMA*

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

## Security Issues?

Security may be a headline risk after the discovery of a backdoor (discovered by [Andreas Makris](https://www.linkedin.com/in/makrisandreas/)), but the reality is mixed. Unitree lacks clear on-premises data solutions, which could restrict access to U.S. utilities under [NERC](https://www.nerc.com/pa/comp/guidance/EROEndorsedImplementationGuidance/CIP-013-1%20R1%20R2%20%20Supply%20Chain%20Management%20(NATF).pdf). We recently heard some Oil and Gas companies have told integrators they will not deploy Unitrees. Moreover, data-sensitive domains, like semiconductor fabs, are also opposed to Unitrees.

At the same time, many buyers are less concerned. Unitree quadrupeds are already in use across construction, critical infrastructure, and even security/patrol work. Even after [U.S](https://www.insidegovernmentcontracts.com/2025/02/fy2025-ndaa-congressional-efforts-to-bolster-u-s-resilience-against-chinese-tech-and-influence/)./[EU](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive) warnings, deployments continue. Security will likely shape which segments Unitree can enter, but many seem undecided at the moment.

With the quadruped market outlined, we now examine what makes Unitree quadrupeds so much cheaper than **any other option**.

## Actuator Design Is Pivotal

Actuators drive quadruped motion and account for the largest share of the bill of materials, typically 50–70%. Yet companies take different design paths. Actuators are either rotary, producing circular motion, or linear, producing straight-line motion often paired with a leg mechanism. While a future piece will dive deeper into design, here we compare how Unitree approaches actuators across three factors: robustness, cost, and efficiency.

![](https://substack-post-media.s3.amazonaws.com/public/images/93c71fee-1c8b-4652-a897-b7d56b93a1e7_1985x309.png)
*Source: SemiAnalysis Estimates*

## Unitree’s Actuators: MIT Cheetah 3 and The Quasi-Direct-Drive

Unitree opts for a Quasi-direct-drive (QDD) style actuator, similar to the [MIT Cheetah 3 (2018).](https://dspace.mit.edu/bitstream/handle/1721.1/126619/iros.pdf?sequence=2) This sees strong efficiency and very low costs, but less robustness.

![](https://substack-post-media.s3.amazonaws.com/public/images/0500b065-75a3-45de-b382-780bb3a678f3_2608x1397.jpeg)
*Source: Thomas Godden , QDD Actuator Design*

Arguably one of the best designs for legged locomotion, QDDs use low gear ratios (5:1–25:1) compared with common higher-reduction gearboxes up to 200:1. High ratios deliver great, precise torque from small motors but add drawbacks:

- **Poor “Transparency”:** The many gear teeth convolute the forces being delivered from the quadruped’s paw.
- **High Friction:** This makes it difficult for the joint to reverse motion smoothly upon impact, increasing the risk of damage.

QDDs low gear ratios reduce friction and enable backdrivability - the ability to yield to opposing forces. On uneven terrain, this lets a leg bend naturally, as a human knee would, rather than striking stiffly and destabilizing the robot. Backdrivability is pivotal for safe real-world traversal.

Unitree’s QDDs often run below 10:1 ratios, lowering friction and cost. Since actuators make up over half of a robot’s bill of materials, these cheaper, compliant actuators give Unitree both adaptability and a major cost edge.

![](https://substack-post-media.s3.amazonaws.com/public/images/ee05eeb8-6d34-48b6-9e85-388895fa428a_4096x3072.jpeg)
*Source: Takayuki Todo*

However, this low gear ratio introduces shortcomings of robustness. Planetary gears, commonly used in QDDs, wear down faster than other solutions, requiring frequent repair. Additionally, “backlash” is introduced, where reversing the gears creates a small error affecting precise movement. This can be compensated by stomping paws into the floor to regain positioning, but as the gears wear down, backlash only grows.

![](https://substack-post-media.s3.amazonaws.com/public/images/85f05c63-b77d-48ee-a6ea-54438cf89f11_420x175.webp)
*Source: OrientalMotor*

QDDs rely on torque-dense motors due to their low gear reduction, making larger robots significantly heavier. Unitree’s industrial B2, for instance, uses a motor 3x+ the weight of the Go2’s. Scaling with low ratios also reduces accuracy and robustness, leaving larger B1/B2 models prone to “wobbliness.”

![](https://substack-post-media.s3.amazonaws.com/public/images/57f7faa4-a2c0-4ec4-8950-25168fe659c4_2537x1329.png)
*Source: YC’s Vlogs , Unitree B1 Leg*

## Sensors: A Chinese Cost Advantage

To navigate the world, quadrupeds rely on a standard sensor setup: cameras on all sides for a full field of view, a central LiDAR for 360° coverage, and often Time-of-Flight sensors for depth perception. These can rack up to 20% of costs on a quadruped. While designs vary, like Unitree for example, omits side cameras and leans more on LiDAR, full coverage is **essential** for safety.

![](https://substack-post-media.s3.amazonaws.com/public/images/495f20dc-2863-404e-b29f-7e6fde81c770_1463x1035.png)
*Source: Boston Dynamics*

In this area, Unitree gains another cost edge. The company sources low-cost LiDARs from Chinese makers like Robosense or LIVOX for only a few hundred dollar, or [build its own for cheap](https://www.unitree.com/LiDAR). By contrast, Western LiDARs can cost closer to $2,000. Boston Dynamics reportedly requires a fully non-Chinese bill of materials, excluding it from these savings.

## Battery Life - Chinese Hardware Prowess

Battery life is a key constraint, ranging from 90 minutes to 5 hours. Unitree’s A2 ‘Stellar Hunter’ runs over 5 hours, or 3+ hours with a 25kg payload. But these numbers exclude onboard sensing and inference. Typical Western quadruped deployments add 1-3 Nvidia Jetson Orins (~50 W each) plus acoustic, thermal, and photogrammetry sensors. Even with these added loads, Unitree’s battery life remains ~**twice** that of Western rivals.

![](https://substack-post-media.s3.amazonaws.com/public/images/b4f988a7-0035-490e-b5d4-f012cd3f8d5a_768x432.jpeg)
*Source: Boston Dynamics*

## What’s Next?

Unitree holds a major cost edge, producing both consumer and industrial quadrupeds at a fraction of Western prices. A full Go2 BoM beyond the paywall shows high margins even at low cost, and the even more impressive B2. This advantage has won much of the research community, where open-source work may strengthen Unitree’s software. As the ecosystem expands, all quadrupeds, including Unitree, are likely to move into broader applications and deployments.

One route to stronger Western quadrupeds would be [boosting local supply chains](https://semianalysis.com/2025/03/11/america-is-missing-the-new-labor-economy-robotics-part-1/) to compete on a cost-level and potentially access larger portions of the research community. Until then, there’s a chance Unitree continues to dominate in cost-competitiveness.

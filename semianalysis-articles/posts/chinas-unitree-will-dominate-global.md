---
title: "Unitree's Impossible Trajectory Is Still Overlooked"
subtitle: "The Fastest Iteration Cycle In Next-Gen Robotics Should See Unprecedented Acceleration "
date: 2026-06-08
source: https://newsletter.semianalysis.com/p/chinas-unitree-will-dominate-global
crawled: 2026-09-15
authors: ["Reyk Knuhtsen", "Niko Ciminelli", "Jacob Rintamaki", "Robert Ghilduta", "Joe Ryu", "Jeremie Eliahou Ontiveros", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Unitree's Impossible Trajectory Is Still Overlooked

**The Fastest Iteration Cycle In Next-Gen Robotics Should See Unprecedented Acceleration **

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

We are witnessing the birth of another Chinese hardware giant. Three years ago, Unitree was a quadruped company. By last year, they parlayed quadruped dominance into creating and leading the humanoid market. This year, their G1 humanoids are finally entering into viable deployments, and three new designs are on the way, including their most-direct [Western humanoid competitor](https://www.unitree.com/H2).

Tesla first unveiled a humanoid in **2022**, and while it and other Western players are now producing early humanoids that remain works in progress, **we hear Unitree may ship its 10,000th in the coming weeks.**

Now, Unitree is tripling revenues YoY on 60% gross margin product lines, planning almost $300M of AI R&D spend, increasingly in-housing portions of manufacturing, all while pricing the cheapest humanoids on the market by far. With their upcoming [highly anticipated IPO](https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_QY8F.pdf), Unitree is deservedly dominating the humanoids conversation. But historically, Unitree’s humanoid robots have a reputation for less than [perfect reliability](https://www.youtube.com/shorts/ZKHiooTF0Eg), are not viewed as useful beyond [entertainment](https://www.youtube.com/watch?v=Ykiuz1ZdGBc) and [R&D](https://www.prnewswire.com/news-releases/nvidia-gtc-conferenceunitree-h1-humanoid-robot-embraces-ai-with-the-world-302096830.html), and have a reputation for being “cheap.”

Despite this, we believe Unitree's **cost structure** is one of its greatest advantages over competitors. Unitree has slashed pre-tax pricing **from $50K+ to $27.3K over the past 12-18 months.** Even at that price, we estimate they still hit **67% gross margins on their flagship G1.** With their BoM set to plummet as manufacturing scales, **we've already heard pricing well under $20K in some deals.**

![](https://substack-post-media.s3.amazonaws.com/public/images/5819a3cc-2fa8-4b48-b000-9855987f126f_4099x3240.jpeg)
*Source: SemiAnalysis Estimates*

We developed these BoMs by going through a full design examination of Unitree’s robot, speaking with manufacturers of every component, and verifying items with multiple supply chain buyers/sellers.

And, lastly, despite countless dismissive comments against the company, we argue their G1 humanoids are crossing the viability threshold of real-world deployments.

![](https://substack-post-media.s3.amazonaws.com/public/images/3c88403b-7d23-4f03-9494-663eecc7f7af_4183x2354.heic)
*Source: SemiAnalysis Estimates*

However, no one understands Unitree’s strategy, cost, and manufacturing as well as concerns of the usefulness of the robots at all. But today we are here to set the record straight. In our research we present the history of Unitree mimicking the BYD and DJI strategy, by generating their own ecosystem, spawning new markets, and then eating said markets. This strategy is in process as we speak. New markets on the horizon means that Unitree’s explosive growth should continue.

![](https://substack-post-media.s3.amazonaws.com/public/images/b0210f02-27b9-4976-8b2d-5e645096d08b_1343x889.heic)
*Source: Zoomax*

Next we examine their specific hardware strategy, and how their QDD actuator design choice led to a potentially structural advantage, and how their actuator has improved into near-deployment grade.

Lastly we argue that Unitree’s improvement and cost advantage is now breaking into the world of economic viability to displace labor. There are likely over 250 Unitrees deployed in labor settings today, and we detail how the deployment math works out. Notably, Unitree has made it this far on the back of the small hobbyist/researcher market. Should Unitree unlock viable deployments and hit critical mass, they may accelerate at unreal speed.

All of this comes at a level of scale and manufacturing that crushes the West’s cost and lead time, and Unitree itself is a standout in the competitive Chinese ecosystem. Behind the paywall we specifically discuss the new robot handmakers that are aiming to unlock more tasks and markets, as well as who will be eaten and who will benefit from the Unitree supply chain.

Unitree’s IPO is the birth of the robotics moment. They are unlocking markets, ecosystems, and are pursuing a strategy of scale that may lead down the path of other Chinese hardware juggernauts. Let’s first turn to the past to understand how Unitree could potentially work out.

# The Making of A Chinese Hardware Giant

What does a fully-matured Chinese hardware giant look like in practice? There’s a great example of the carmaker BYD (Build Your Dream) today as the mature expression of Unitree’s strategy: own the most expensive and challenging component in the BoM, use this ownership to compound cost advantage that nobody can match, and create new markets while adding more value from inhousing your supply chain.

![](https://substack-post-media.s3.amazonaws.com/public/images/17dc6910-2eba-4d77-9c11-926c4f648e4b_742x453.heic)
*Source: BYD*

BYD initially focused on the battery cell. Batteries can consume around 30-40% of an EV’s BoM (now less, thanks to BYD). BYD was founded in 1994 to make battery cells that Japanese incumbents exited due to toxicity. BYD spent nearly a decade refining their product before entering EVs in 2011, and at first was only a niche player. When BYD launched its first battery-only EV, the e6, to the [Chinese market](https://web.archive.org/web/20111101200501/http://www.bydenergy.com/bydenergy/energy/News%20Center/News/78.html) in October 2011, annual EV sales across all of China were just 8,159, or [0.04% of new car sales](https://en.wikipedia.org/wiki/Plug-in_electric_vehicles_in_China). There was no EV market, but BYD helped create one.

**BYD’s strategy was key.**

**Owning the cell at increasing automotive volumes passes through demand, creating improved supply and ecosystem,** where players like [Hunan Yuneng](https://christopherchico.substack.com/p/why-korean-battery-makers-are-converting) and [Shenzhen Dynanonic](https://christopherchico.substack.com/p/why-korean-battery-makers-are-converting) (LFP cathodes), [Inovance](https://www.marklines.com/en/top500/inovance-technology) (motors and inverters), and [Sanhua](https://www.sanhuaautomotive.com/en) (thermal management) emerged to supply BYD’s next-generation, improved parts at a lower cost. None of these existed at a meaningful scale in 2010.

**BYD has freedom to in-house manufacturing where it compounds for them.** They took in house the battery cell, drives, motors, IGBTs and SiC power modules (one of the only companies in the world running an IDM model), the transmission, the chassis and outer body shells, and even the engine itself. By the late 2010s, nearly every component of an EV was being built under BYD’s roof.

This creates a positive feedback loop: owning and improving the right hardware lets BYD create a new product that opens a new market, like their 2020 [Blade Battery](https://electrek.co/2026/03/05/byds-new-ev-battery-unlocks-1000-km-range-10-min-charging/). Pre-Blade, the battery chemistry (LFP, Lithium Iron Phosphate) was cheap, safe, but low-density, fine for vehicles that never traveled far from a charger, like [forklifts](https://www.emobility-engineering.com/lithium-iron-phosphate-lfp-batteries-ev/) that charged during operator breaks or buses that returned to depot every night. However, passenger EVs, which had to handle road trips and unpredictable home charging, saw LFP as unviable.

![](https://substack-post-media.s3.amazonaws.com/public/images/341cd7fc-c0a2-411d-a2c6-a30d2fb7ea4a_996x552.heic)
*Source: BYD*

In 2021, their Blade Battery took a new packaging geometry, pushing battery pack space utilization per kg up [50%](https://volta.foundation/the-next-generation-battery-pack-design-from-the-byd-blade-cell-to-module-free-battery-pack/). Now, LFPs could remain the same size, while improving distance to a viable threshold. Tesla shifted the Model 3 and Y to an LFP battery, Ford licensed CATL’s LFP technology, and overnight, through meticulous hardware iteration, BYD created the modern affordable EV market to dominate.

Before the Blade Battery, BYD shipped 189K new EVs in 2020. After the Blade Battery in 2021, BYD shipped 600K new EVs, and by 2025, not only did BYD become the #1 EV producer, but they overtook Tesla as the [#1 BEV producer](https://www.bbc.com/news/articles/cj9rjwpvmpzo) (battery only), Tesla’s main product. BYD has now inhoused such a significant portion of its process ([75% for the Seal](https://www.ubs.com/global/en/investment-bank/insights-and-data/2023/byd-teardown.html)), that their cost-structure is almost untouchable, like the 2023 [Seagull](https://insideevs.com/news/710364/byd-detroit-import-seagull-caresoft/) model for ~$11,000 (newer models are [under $8k](https://electrek.co/2025/04/08/byds-low-cost-seagull-ev-now-starts-under-8000-china/) in China!) BYD even owns supply chains further upstream with moves like a [2023 refining Joint Venture with Huayou Cobalt](https://evboosters.com/ev-charging-news/the-blueprint-of-an-ev-empire-how-byd-built-global-dominance-through-vertical-integration/) and [acquiring direct lithium mining rights](https://www.automotivemanufacturingsolutions.com/electrification/how-chinas-byd-surpassed-tesla-with-production-and-battery-tech-reshaping-the-global-ev-market/304649) in Brazil’s “Lithium Valley.”

![](https://substack-post-media.s3.amazonaws.com/public/images/5a625853-0a1f-460c-82ad-800655c4c376_3200x2160.heic)
*Source: SemiAnalysis*

This scaling outcompeted European EVs so much that VW announced its [first-ever](https://www.cbsnews.com/news/volkswagen-could-close-plants-in-germany-first-time-china-ev/) German plant closures and Stellantis cut [guidance](https://www.cnbc.com/2024/09/30/dodge-maker-stellantis-drops-profit-warning.html), all citing Chinese EV pressure. Even the United States had to increase its [tariffs on Chinese EVs](https://www.npr.org/2024/05/14/1251096758/biden-china-tariffs-ev-electric-vehicles-5-things) to 100% to protect its domestic industry. Now, BYD has scaled so much they even own their own [freight](https://carnewschina.com/2025/10/02/byd-completed-its-massive-fleet-now-able-to-export-1-million-cars-a-year-but-not-just-from-china/) to ship their cheapest, and best EVs in the world.

# The DJI Playbook - Niche Researcher/Hobbyist Markets Are Viable Bootstraps

DJI pioneered a playbook different from BYD, and Unitree is running that playbook today, starting with the researcher/hobbyist beachhead, and a low-quality product.

In 2013, “useful consumer drone” wasn’t a category. [Parrot’s AR.Drone](https://arstechnica.com/gadgets/2013/03/esa-launches-drone-app-to-crowdsource-flight-data/), the leading product, won its 2010 CES award in the *[Electronic Gaming Hardware](https://web.archive.org/web/20110416073134/http://www.gamerlive.tv/article/ces-2010-hottest-iphone-game-world)* bracket and shipped alongside augmented-reality dogfighting games. The drone had no camera stabilization, no GPS, and only took 640x480p pics/videos. Anyone who actually wanted a useful flying camera had two options: pay [$19,995 for a Draganflyer X6](https://hpisavagex46.wordpress.com/2011/01/24/ubercool-inventions-draganflyer-x6-uav-helicopter-aerial-video-platform/), or stitch together frames, motors, flight controllers, and gimbals (stabilizers) from disparate vendors for [up to $1,200](https://hackaday.com/2011/07/27/how-to-build-your-own-quadcopter-step-by-step/) in parts, plus dozens of hours of assembly and PID (controller) tuning, usually ending in expensive crashes.

![](https://substack-post-media.s3.amazonaws.com/public/images/2316f417-e766-4143-84bf-12f26a3b4185_2500x1666.heic)
*Source: AR Drone 2.0*

Researchers, hobbyists, and early professional camera workers were a willing market for something new. DJI’s [Phantom 1 shipped January 2013 at $679](https://www.dji.com/newsroom/news/dji-releases-all-in-one-solution-read-to-fly-phantom-quadcopter), and was not a fully-fledged product at the time. It had no built-in camera, no gimbal (stabilizer), ten minutes of flight, no live video feed, but it was roughly half the cost of the build-it-yourself drone, with none of the assembly burden. A far cry from DJI’s drones today, but **DJI went from $4M in revenue in 2011 to [$130M](https://www.wsj.com/articles/who-builds-the-worlds-most-popular-drones-1415645659) in 2013, after the Phantom 1’s release**. This was more than enough to kickstart DJI’s flywheel.

**DJI then reaped the fruits of the Shenzhen consumer electronics ecosystem, now huge from the Smartphone boom**. GPS prices went from [$800 to below $14](https://www.davidpublisher.com/Public/uploads/Contribute/65446bc585155.pdf) from 2003-2013, controllers [went from](https://www.davidpublisher.com/Public/uploads/Contribute/65446bc585155.pdf) $2,000 to $400 from 2006-2011, and more. From DJI’s boom, there are now [over 3,000](https://electronics.alibaba.com/question/top-chinese-drone-manufacturers-dji,-autel,-ehang-more) drone component suppliers for most anything you desire.

![](https://substack-post-media.s3.amazonaws.com/public/images/39b409ca-b7a1-495a-a48c-c5b5c8eb4a6a_1534x1144.heic)
*Source: GlobalSources*

**DJI chose to inhouse the most expensive and technically difficult component first: the flight controller.** Third-party suppliers were still selling at $200-400 even in batches of thousands in 2014. Later on, DJI brought inhouse the gimbals, motors, and ESCs.

Like BYD, new DJI generations unlocked a new market the previous one couldn’t address. The 2013 Phantom 1 ($679, no camera, 10-minute flight, no live feed) was the bootstrap, engaging hobbyists/researchers. The [Phantom 2 Vision+](https://store.dji.com/product/phantom) in 2014 then came with a 3-axis gimbal (stabilizer) into the frame, where previously broadcast-stable aerial video had required a $2,000+ aftermarket gimbal mounted to a hand-built rig, operated by a skilled pilot.

Pre-Vision+, professional aerial photography was the domain of helicopters and Hollywood second-unit teams, but now, small businesses could perform this on their own. As such, whole new markets were unlocked for DJI, like real estate listings, wedding videos, local news, agricultural surveying. By the [Phantom 4](https://store.dji.com/product/phantom-4) in 2016 ($1,399, 4K camera, 28-minute flight, forward obstacle avoidance, 44 mph sport mode), the enterprise market was unlocked: surveying, inspection, first response, and more that we detailed [here](https://newsletter.semianalysis.com/p/robotics-levels-of-autonomy).

![](https://substack-post-media.s3.amazonaws.com/public/images/b266ee03-ba86-4f6a-a416-06a1e1cffc52_838x472.heic)
*Source: DJI*

In 2016-17 DJI held roughly 70% global consumer drone share, and [global drone shipments hit 6.4 million units and $1.9 billion in revenue](https://www.businesswire.com/news/home/20160706005481/en/Consumer-Drone-Sales-Increase-Tenfold-67.7-Million), a market that hardly existed before. Multiple competent dronemakers were crushed. 3DR, GoPro’s Karma, and Parrot’s consumer line had all exited or were exiting the category. Chris Anderson, the 3DR CEO, [estimated](https://www.recode.net/2017/1/9/14182200/parrot-drone-layoffs-dji-3dr-commerical) that DJI cut prices by as much as 70% in less than a year during the Phantom era.

For brevity, we’ll call this the **“DJI Strategy”** throughout the rest of this piece: own one critical component, bootstrap a willing audience, ride the ecosystem, and let each hardware generation unlock the next market. (An earlier version of this framing appeared in [our first robotics paper](https://newsletter.semianalysis.com/p/america-is-missing-the-new-labor-economy-robotics-part-1).)

# Unitree As An Early DJI

Unitree is a live DJI Strategy case study: own the bottleneck component, bootstrap a willing audience, ride and seed the ecosystem, unlock new markets generation by generation. So far, Unitree has

- **Parlayed actuator scaling into quadrupeds**, building the most cost-efficient legged platforms in the market.
- **Scaled the quadruped program into researcher humanoids**, with the G1 becoming the dominant research platform for a surprisingly large market.
- **Funded hardware improvements enough to begin real-world deployments**, with the threshold being crossed right now.
- **Signaled promising improvement on their next generations to compete on performance with Western humanoids.**

Let’s walk through the history, design, strategy, and the critical threshold they are crossing right now humanoid deployments.

In 2016, [Wang Xingxing](https://baike.baidu.com/item/%E7%8E%8B%E5%85%B4%E5%85%B4/8766961), a [former employee](https://www.thewirechina.com/whos_who/wang-xingxing-%E7%8E%8B%E5%85%B4%E5%85%B4/) at DJI, developed a low-cost quadruped robot called XDog for his master's thesis. He iterated upon the same quadruped in his new company named “Unitree.” For Unitree, their core component of choice was the actuator, the integrated joint that moves the robot’s limbs. Like BYD and their cells, DJI and their flight controller, Unitree chose the expensive actuator (50%-70% of the humanoid BoM) to improve and scale out from.

Unitree started with the academic robotics community as merely a [quadruped company](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree). Just as DJI had hobbyists paying out the nose for half-finished drones, Unitree saw university labs looking for a legged platform that didn’t cost $70-100K+. The [Laikago](https://spectrum.ieee.org/this-robotics-startup-wants-to-be-the-boston-dynamics-of-china) shipped in 2018 at [$45,000](https://newatlas.com/laikago-quadruped-robot/59867/). The [A1](https://www.unitree.com/a1) followed in 2020 at [$15,000](https://tribotix.com/product/a1-quadruped-robot/); the Go1 in 2021 [started at $2,700](https://spectrum.ieee.org/unitrees-go1-robot-dog-looks-pretty-great-costs-just-usd-2700) for the Air trim and ran up to $8,500 for the Edu; the Go2 today [starts between $1,600 and $2,800](https://shop.unitree.com/) depending on trim and region.

A 94-96% price decline in entry-level quadrupeds over six years pushed Unitree from academia into consumers and now even [industry deployments](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree) -- with the broader AI wave lifting the hardware’s capabilities. More importantly, it gave Unitree years of real volume on the same systems for a humanoid: actuators, controls, suppliers, and production process. When Unitree released the H1 in 2024 at roughly $90K, the humanoid was less a brand-new product, but rather the direct result of their quadruped scaling curve. We’ve heard from people close to Unitree that the H1 was essentially a **quadruped standing on two legs** - note the bent knees and [awkward walk](https://www.youtube.com/watch?v=GN2SNjctwCE). The H1 showed how far quadruped-era IP could be pushed into humanoids, but the following G1 changed Unitree’s world.

![](https://substack-post-media.s3.amazonaws.com/public/images/b0210f02-27b9-4976-8b2d-5e645096d08b_1343x889.heic)
*Source: Zoomax*

## The $30-50K G1 - A New Possibility In 2024

In mid-2024, affordable, off-the-shelf humanoids were few and far between until Unitree came along. [Agility’s Digit](https://www.agilityrobotics.com/) was just beginning to deploy a handful of robots into factories. [Apptronik’s Apollo](https://apptronik.com/), unveiled August 2023, was pre-commercial. [Figure’s initial commercial agreement with BMW](https://www.prnewswire.com/news-releases/figure-announces-commercial-agreement-with-bmw-manufacturing-to-bring-general-purpose-robots-into-automotive-production-302036263.html), signed January 2024, was shipping in single-digit volumes. Tesla wasn’t (and as of V3, still isn’t) shipping Optimus externally at all. On the Chinese side, [UBTech’s Walker](https://www.ubtrobot.com/), Fourier, and the early signs of AGIBot existed, but not as cheap nor at volume. No one could just “buy” a humanoid.

The G1 enabled an incredible academia sized market. Ask any researcher and they will tell you how dramatic a step-change in accessibility it was using a $30-50K, ready-to-purchase bot. This share of the research community has since bled into top-tier AI research companies via hirings, like [Nvidia, Apple, and Meta, all purchasing hundreds of G1 units](https://semianalysis.com/core-research/). Unitree has become the leading platform for humanoid AI research.

![](https://substack-post-media.s3.amazonaws.com/public/images/933ee9fb-19e9-4601-987e-d6a5ef71f74a_519x393.heic)
*Source: Core Research , Unitree Presentation at Robotics Summit 2025*

## The Ecosystem Advantage

Unitree inherits both the supplier base of DJI and BYD’s past. China assembled [31.3 million vehicles in 2024](https://carnewschina.com/2025/01/14/china-produced-and-sold-31-282-million-and-31-436-million-vehicles-in-2024/), [40.9% of them new-energy](https://carnewschina.com/2025/01/14/china-produced-and-sold-31-282-million-and-31-436-million-vehicles-in-2024/) (BEV or PHEV), and the aforementioned 3,000 drone component suppliers had already scaled many of the BLDC motors, drives, encoders, batteries, and manufacturing processes that general robotics can reuse. However, Unitree’s gravity is exemplified by the rise of new humanoids+quadrupeds supply chains. Every province now has several manufacturers of rightly sized/spec’d gearboxes, high-torque BLDC motors, and more. Within China, there are now [~200](https://cnmra.com/china-now-has-over-200-humanoid-robot-manufacturers/) humanoid companies all reaping the benefits of and contributing to this ecosystem.

![](https://substack-post-media.s3.amazonaws.com/public/images/bfe35430-f3ca-4200-9c10-6bb63086ea75_538x140.heic)
*Source: Leaderdrive*

All of this stemmed from Unitree’s decision to perfect the actuator. However, the first generations of their actuator didn’t work very well.

## In 2024, Their Humanoids Weren’t Good

*For brevity, we’ll use QDD in this piece to mean the combination of a brushless DC motor and a low-ratio planetary gearbox, typically in the single digits and up to 20:1, which can still provide adequate [backdrivability](https://irisdynamics.com/articles/forcefeedback-in-robotics), but understand there are [nomenclature debates](https://robot-daycare.com/posts/actuation_series_1/).*

Let’s be clear: DJI and BYD unlocked markets when the product **worked**, and the H1 and original G1 were **not** very capable upon shipping. Whenever users pushed them toward real work, the motors often overheated. The G1 could only hold a 2kg payload, like a 2-liter bottle of soda, with arms fully outstretched for a few seconds before mandatory cooldown. The same 2-3kg with arms bent or contracted for maybe 2-3 minutes, like the diagram below.

![](https://substack-post-media.s3.amazonaws.com/public/images/18ec0090-dfe1-4a78-9e8e-257554b3d9ac_1382x500.heic)
*Source: OmniRetarget*

After that, the robot typically needed about 30 minutes to return to functionality, and likely a full hour before resuming a real work task. Five minutes of work followed by the rest of the hour cooling down is not a productive robot.

The issue primarily came from Unitree’s core actuator choice: the **QDD, or quasi-direct-drive, which are simpler and cheaper than typical robotics actuators**. Historically, companies favored high-precision, high-power actuators that could both move the robot and support its weight. Industrial arms often use [HarmonicDrives](https://www.harmonicdrive.net/technology). Boston Dynamics’ early humanoids and quadrupeds used [bulky hydraulic actuators](https://bostondynamics.com/blog/electric-new-era-for-atlas/). Even today, many humanoid companies default to high-gear-ratio actuators, like strainwaves from HarmonicDrive.

Those architectures work, but they are expensive, hard to manufacture, and often difficult to maintain. In 2018, the [MIT Mini Cheetah](https://dspace.mit.edu/handle/1721.1/118671) popularized the QDD (quasi-direct-drive): a cheaper, simpler alternative. The open question was whether QDDs could scale and prove reliable enough for real-world robotics. Unitree believed this to be a yes.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

# Why The Issues Around QDD?

![](https://substack-post-media.s3.amazonaws.com/public/images/35e5eab0-c226-45b9-9f64-75d6fb6e466b_1050x404.heic)
*Source: Unitree (motor) and Power Electric (gearbox)*

QDDs flip the historically common robot-joint setup. Instead of a small motor with a big gearbox, they use a beefier motor with a much smaller gearbox. If the robot wants to lift 5kg, there’s two options.

- **Big gearbox, small motor.** The gearbox works like low gears on a bike, trading speed for force and multiplying the motor’s twisting force (torque) by 30x, 100x, or even 200x in some cases. This is the “gear ratio,” like 30:1, 100:1, 200:1, etc (not a direct 1:1 mapping in most cases). This setup is how industrial arms swing whole car bodies around with modest motors: the gearbox does most of the heavy lifting.
- **Small gearbox, big motor.** QDDs go this route, with gear ratios typically under 20:1 using a basic, off-the-shelf planetary gearbox. Since the gearbox barely multiplies anything, the motor has to be way stronger. Lifting the car chassis from above would require a huge motor (our [quadrupeds piece](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree) explores the QDD further).

While there’s bonuses to Unitree’s QDD, like easily adapting to opposing forces (like collisions), or invoking a rapid, dynamic range, it does come with tradeoffs. Because the motor carries more of the torque burden directly, rather than relying on the gearbox to amplify it, early critics argued Unitree’s motors would draw very high current, run hot, and prove too unreliable for practical work.

## Two Years Later, The QDDs Are Defying Expectations

The early critique was fair, QDDs gave Unitree a cheaper, simpler actuator, but pushed too much thermal burden onto the motor, hence the aforementioned overheating. **But** **while most stuck with the strainwave (HarmonicDrive) route, Unitree took the chance and iterated.**

Over the last few years, Unitree appears to have improved the actuator in several ways, now showing promising signs of scalability, with many other (Chinese) humanoids **switching** to the QDD wave and, consequently, **building up the ecosystem**. We will aim to cover here of the improvements Unitree has displayed, but to clarify: we have not had access to cycle test numbers, this is simply our best approximation of evaluating their hardware improvements.

Let’s begin with the usual P=I^2R, or in this case, Heat *roughly* scales with I^2R. So you may do two things: lower the current (I) the motor needs to draw, or lower the resistance (R) of the windings the current flows through. Most focus on Current because it’s squared, but both contribute.

One major lever to reduce wasted current is to make the motor’s torque smoother through each rotation. **In plain terms: pedaling a bike with a slightly wobbly wheel takes more energy than a true one. Each rotation, you fight a small surge of resistance, and you push harder on average to hold the same speed.**

![](https://substack-post-media.s3.amazonaws.com/public/images/5a87cf10-eb9c-4315-80b5-b92303610816_1116x738.heic)
*Source: MQITechnology*

A motor with a rough magnetic pull has the same problem: the rotor jerks slightly with every revolution, and the extra current you draw to overcome that jerkiness turns directly into heat. Those hiccups come from effects like cogging torque, where the rotor magnets interact with the stator teeth, and from non-ideal magnetic-field shapes that create torque ripple. Less ripple means less vibration, less wasted current, and more usable torque before overheating.

To resolve this, **we can reshape or curve the magnets and slots so the pull stays smooth between rotations**. Additionally, we can also skew the magnets so the stator teeth take turns engaging the field rather than all snagging at once.

Another useful solution is to **pack more copper wire into the motor.** A thicker, more densely-packed wire carries the same current with less resistance, known by Unitree as their [“Low Copper Consumption Coil](https://www.unitree.com/go1/motor).” Halodi, now known as 1X, famously tweaked their copper fill as well by using [thick, square copper wire](https://x.com/boxcardavid/status/1935133276974498233?s=20).

Cooling is still important for a functional robot, but Unitree’s architecture is fairly conservative on this front. We’ve found **passive cooling** across most of the body, with active air cooling only at the main control board and hip joint, and a vapor chamber heat spreader at the knee. Unitree has **iterated here too**, adding active cooling around the pelvis in an October 2025 update that improved thermal headroom for subsequent G1 batches.

![](https://substack-post-media.s3.amazonaws.com/public/images/b398c0af-1ef5-487f-8e71-7563f231f051_1032x847.png)
*Source: JONVER Electronics*

We suspect Unitree not focusing much on its cooling can be attributed to wanting to reduce costs and manufacturing complexity while focusing on the core problem we mentioned earlier: lowering the amount of current its motors need.

## So Why QDDs In The First Place? A Quick Detour On Speed+Cost

Unitree made a bet on the QDD, taking an unproven architecture (in deployments) on the most expensive component in the robot. While difficult to work with, they are still higher efficiency (95%-98% vs 85%-90% for strainwaves), and up to 80% cheaper. Importantly, low-ratio planetary gearboxes are also common industrial components, machined with standard gear hobbing (think grinding) on widely available equipment, enabling many suppliers to exist.

Meanwhile, competitors choosing strainwave gearboxes for example, like from HarmonicDrive or LeaderDrive, face a more complicated ~13-step process. Multi-hour heat treatment of the metal grains to allow “flexing,” (shown below) precision hobbing into micron-level tolerances, etc, all lead to a process that took HarmonicDrive decades to perfect, and LeaderDrive is still considered by many to be lagging HarmonicDrive’s reliability after 20+ years.

![](https://substack-post-media.s3.amazonaws.com/public/images/620ef23c-344e-437b-8a16-92ef5a28a6c8_614x239.heic)
*Source: Nature*

Instead of verticalizing an entire decades-long learning curve, Unitree chose the QDD. Now, **a** **new QDD redesign can become a sample actuator within weeks for Unitree**. For context, a custom motor and gearbox subsystem may take a Western humanoid company 3+ months due to so many supply chain handoffs. Weeks of spec iteration, 6-8 weeks for motor+gearbox samples, then validation and reorders. The result is both cheaper production, as shown in our BoM, and faster iteration, as seen in the active pelvis-cooling rollout that went largely unnoticed.

## From Burnout To Lightweight Tasks

Now, Unitree has iterated and improved their G1’s and actuators enough that small, but legitimate, tasks are within *arm’s* reach. Arms bent, the G1 sustains upwards of 10-15 minutes of operations carrying 5 kg, a roughly 2x increase in payload and a 5x increase in duration over our original numbers! With arms fully outstretched, 5kg (roughly a bowling ball) can be held for ~1 minute before hitting thermal limits. Even for humans this is considered a workout. But how close are we to Unitree being a “viable” humanoid?

![](https://substack-post-media.s3.amazonaws.com/public/images/c488823a-e542-4715-806a-c0522455554e_998x520.heic)
*Source: NVIDIA*

# Heading Towards Useful Work

Unitree is obviously very cheap, and we know the strategy they are taking, and how their hardware is improving, but does it matter? Many might point to the previous section declaring that 15 minutes carrying 5kg doesn’t matter: perhaps “dexterity is lacking,” “it doesn’t have hands,” “that’s not very long,” etc. However, we estimate that Unitree may have shipped roughly **up to 250 humanoids** into productive industry pilots or deployments in 2025, aside from their research/hobbyist sales. We’ve even found one company with **30 G1s deployed today, and multiple companies with 5-6 G1s deployed**. Granted, these deployments are likely software limited (e.g. AI model capabilities), leading to differing economics based on what solutions are used, like 100% teleoperation (which is what we assume in our calculations).

Unitrees do not need to run perfectly, nor for extended periods of time, nor do we expect them to. Rather, it is a question of what’s sufficient for useful work. The G1’s arms are still underpowered, they don’t have enough “degrees of freedom” for perfectly human-like movements, and they still overheat on overly strenuous jobs. But this only puts a **ceiling** on the types of tasks the G1 can do, not a **floor** on whether it can do anything at all.

![](https://substack-post-media.s3.amazonaws.com/public/images/026abe1b-5aef-4c17-9aa8-19efdff04a45_350x482.heic)
*Source: ExtremControl*

Looking past performative backflips, Unitrees can already perform “useful work,” non-exhaustively defined here as either.

*A task performed in a business to produce some economic output, like sorting boxes, or a task performed to relieve a physical burden of a human, like folding clothes.*

So what are these Unitrees actually doing? Essentially, carrying boxes/items from A to B. Currently, it tends to be lightweight materials handling, like in e-commerce tote (bin) handling with <3-5 kg payloads, or moving even empty boxes/totes.

None of these are 24-hour, fully-autonomous production lines, and most are still teleoperated. Nonetheless, let’s demonstrate that moving boxes around is becoming economically viable.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

# Unitrees Are Crossing The Deployment Viability Threshold

"*Thanks to [Adamo](https://adamohq.com) for helping us understand teleoperated deployments further!*"

We’ve discussed humanoid economics in depth in our [Levels of Autonomy paper](https://newsletter.semianalysis.com/p/robotics-levels-of-autonomy), but here we perform a full calculation for Unitree. Taking Agility Robotics’ (fantastic) task as a baseline, and plugging in Unitree inputs, we find Unitrees are **currently passing below** the $30 per hour labor cost of a human.

![](https://substack-post-media.s3.amazonaws.com/public/images/c65732ee-db1a-4891-b407-122c68480c71_4183x2354.heic)
*Source: SemiAnalysis Estimates*

No humanoid is at mass-scale production/deployments yet, all are still iterating on the technology, and these figures may change from deployment to deployment (grippers/hands, payload, throughput, etc). Instead, we will show our best estimate of what they’re capable of today and what that looks like on a specific task, but want to note: these are early-stage numbers, and **if Unitree’s hardware continues its improvement trajectory, and Autonomy improves, the economics likely only improve from here.**

![](https://substack-post-media.s3.amazonaws.com/public/images/97e26440-c3fb-4c98-a58e-d29dc7d77eab_441x377.heic)
*Source: Agility Robotics*

## A Lovely Task: Tote Handoff

In this particular job, Agility serves as a “bridge” between automation systems, for example, carrying totes (bins) off the AMRs to place onto conveyor belts. It’s a standard, but particular, logistics workload, where a human typically waits on automation systems to line up for the transfer, but leaving dead time in between. It’s why Agility’s [66 totes per hour](https://www.automationworld.com/factory/robotics/article/55303585/agility-robotics-agility-robotics-digit-shows-promise-in-line-side-operations-with-new-iso-safety-standard-on-the-horizon) (from a conference demo, likely higher in deployments) is perfectly fine.

![](https://substack-post-media.s3.amazonaws.com/public/images/6fdb642f-6b71-4e4a-a230-513c2fbbf281_992x490.heic)
*Source: The Robot Report*

Additionally, in Agility’s GXO deployment, the totes are [2-4kg](https://www.therobotreport.com/gxo-logistics-putting-digit-humanoid-to-test/) (good for our aforementioned Unitrees). With light payloads, low-throughput, forgiving retries upon failure, and little dexterous manipulation, it’s a perfect task for the current [Level of Autonomy](https://newsletter.semianalysis.com/p/robotics-levels-of-autonomy).

![](https://substack-post-media.s3.amazonaws.com/public/images/e636c2c0-f448-4bb5-9b76-a467d827bb7f_392x506.heic)
*Source: OmniRetarget*

## Calculating Unitree’s Economic Viability

Agility [currently operates](https://x.com/agilityrobotics/status/1909763546671726776?s=20) using a [2:1 utilization model](https://www.therobotreport.com/heres-what-it-could-cost-to-hire-a-digit-humanoid/), two units of operating time for every one unit of charging, giving Digit a **two-thirds utilization rate** relative to a human.

![](https://substack-post-media.s3.amazonaws.com/public/images/f56c6c37-3697-4b85-80c9-c1167c673095_780x440.heic)
*Source: Agility Robotics*

Operators deploying Unitrees on similar 2-4 kg tote transfer work reported to us a throughput matching Digit on this task. However, Unitrees aren’t the most robust robots. A Unitree G1 typically runs a similar task for 10-15 minutes, while needing 5-10 to cool down, but still leaving a 50%-67% utilization rate. In our assumptions, we remain **very** conservative, assuming full teleoperation, 15% service contract (typically 5-10% in industrial scenes), a two-year useful life, zero residual value, and only two shifts. Even still, the robot proves viable **today.**

![](https://substack-post-media.s3.amazonaws.com/public/images/f6340598-8962-405a-83b4-1cd909022265_4183x2354.heic)
*Source: SemiAnalysis Estimates*

To get the caveats out of the way, we are not proposing Unitree as the full package. Many layers still need to be added. Agility, for example, has a great operating system to coordinate with the Warehouse Management System, a deeper functional safety approach, their own layer of autonomy, and much more. However for Unitree, even full teleoperation seems to be viable in the right business settings **now.**

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

## Where This Goes

To our knowledge, this is the first stage of Unitree’s humanoids exhibiting useful work in deployments. It’s not that this task is exceptional, or a $100T TAM, but it shows Unitree may be crossing a threshold, and their trajectory is quite remarkable. Recall that DJI shipped a half-perfect drone to niche hobbyists and 32x’d their revenue, quickly catapulting themselves into drone dominance. In the beginning, the G1 would overheat from holding a box for 2-3 minutes too. The performance improvements thus far were funded by hobbyists/researchers. If Unitree unlocks even a slice of the warehouse TAM, progress can accelerate at breakneck speed.

With signs of robotic AI models [gaining new capabilities](https://www.pi.website/blog/pi07), BoMs falling, and the quality of hardware improving thus far, Unitree could become the cheapest, competent humanoid platform in the market. Let’s talk about how they got to their world-leading $8,976 BoM.

# China’s Manufacturing Competence

Throughout the piece so far, we’ve hinted at Unitree’s manufacturing competence and the ecosystem surrounding them. For robotics, and many other industries, working with the Chinese ecosystem is necessary to compete on a global scale when: Suppliers are mere hours away by train, samples arrive the same/next day, vertical iteration cycles can run in weeks instead of quarters, and components can run 20-40% cheaper than Western equivalents. It should be noted that strainwave gearboxes from Leaderdrive, for instance, sometimes cost **a third** of HarmonicDrive’s -- granted HarmonicDrive **currently** remains the reliability leader.

Most American robotics startups are already working with Chinese supply chains, like Sunday Robotics, Dyna, and XDOF, who all run their hardware teams out of China. Even Tesla Optimus sources from the Chinese supply chain, and will likely [continue](https://www.scmp.com/tech/tech-trends/article/3341953/optimus-chain-chinese-suppliers-form-backbone-teslas-humanoid-robot-initiative) to do so.

## Unitree’s Verticalization Is Remarkable - Even In China

The Chinese ecosystem is amazing, but we’ve harped on how great verticalization is, so let’s expand on this. Unitree self-develops BLDC motors, planetary gearboxes, LiDARs, and depth cameras, each typically (or even previously for Unitree) outsourced by other Chinese humanoid OEMs. Instead, Unitree’s self-produced motors can run as low as 30-40% of equivalent Western motors, and **they now make some of the cheapest humanoid gearboxes in the world.**

![](https://substack-post-media.s3.amazonaws.com/public/images/12b16c91-48e1-44da-aabf-c85fdcee2239_1266x713.heic)
*Source: IQSDirectory*

These same benefits are very apparent in the IPO filing. In Unitree’s [First Round Inquiry Response](https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_OE27.pdf) with the Shanghai Stock Exchange (SSE), they explicitly state that scaling production gave them **upstream bargaining power**, which created a lasting cost advantage.

![](https://substack-post-media.s3.amazonaws.com/public/images/fbba04cf-cbd2-4781-bc32-ba5f822a5b5d_1255x535.heic)
*Source: Unitree First Round Inquiry Response, 8-1-1-14*

This translated to margins on their quadruped robots improving from **42.36%** to **55.49%** while costs dropped nearly in **half.** However, SemiAnalysis subscribers knew these quadruped margins already [back in September](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree).

![](https://substack-post-media.s3.amazonaws.com/public/images/c2cbfeee-3cba-47c1-8bff-256156183d32_1982x809.png)
*Source: SemiAnalysis*

This verticalization is a spectacle in Western markets, but even within China, where razor thin hardware margins require verticalization for survival. BYD and DJI from earlier showed their path to dominance via verticalization. UBTECH and AGIBot (two of the main Chinese humanoid competitors) are [actively moving](https://biz.chosun.com/en/en-industry/2026/03/20/CNMGR4IU6ZAAHKJFX7WEXCYSXY/) to bring more of the hardware under control, like gearboxes, motors, etc -- components Unitree already self-develops.

Both UBTECH and AGIBot still lean on ODM/OEM partners for manufacturing and, in some cases, final assembly, like AGIBot outsourcing European production to Minth Group in Serbia. Even then, AGIBot is licensing full tech transfer at $4M, scaling through partnerships instead of owning the manufacturing learning curve. Meanwhile, Unitree states in their S-1 they plan to bring further development inhouse, including “tooth-profile design, simulation optimization, material validation, and high-precision machining.”

However, neither Unitree nor other humanoid companies are at high-volume production. This implies that even as they scale production, Unitree may likely maintain a **structural cost advantage** from a first-mover standpoint. A future piece will detail the Chinese industrial ecosystem in all its glory, but for now, assume most humanoids will source from China, and even in China, Unitree is exceptional.

# Conclusion

While Western manufacturers were/are still prototyping humanoids, Unitree has profitably shipped tens of thousands of quadrupeds, built up an entire humanoid market, entered into useful humanoid work, but everyone should consider: where does this stop for Unitree? BYD began with just battery cells, DJI with just controllers, and are now titans of industry.

Watching how Unitree has accelerated success through multiple robot form factors, and increasingly solidified a manufacturing advantage, they may continue to expand at this same pace and unlock markets previously unthinkable.

For now, let’s discuss robotic hands and which of Unitree’s suppliers may benefit, all now beyond the paywall.

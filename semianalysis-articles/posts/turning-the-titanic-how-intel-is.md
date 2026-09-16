---
title: "Turning The Titanic – How Intel Is Using Software Acquisitions And Increased Accountability To Attempt To Save The Sinking Ship"
date: 2022-05-18
source: https://newsletter.semianalysis.com/p/turning-the-titanic-how-intel-is
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Turning The Titanic – How Intel Is Using Software Acquisitions And Increased Accountability To Attempt To Save The Sinking Ship

It’s no secret that Intel has some rocky years ahead with AMD, Nvidia, Marvell, and in-housing efforts from the likes Apple, Amazon, Google, Microsoft, and Meta eating into their share. Intel through a combination of slowing down on design integration and delays in process technology has had their margins fall to 50% from their long-term targets of 60% while also hemorrhaging share.

Intel is in a tough spot, but they are [throwing the kitchen sink](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?s=w) in attempt to fix this slide to irrelevancy. They have hired over 10,000 more engineers, increased their spending on fabs, ratcheted up R&D, and are acquiring companies such as Tower Semiconductor. We have already done a [deep dive on all of these efforts](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?s=w) as well as each business unit and the culture shift.

> We are very skeptical this can be executed on. There’s no way to emphasize how difficult this will be, but it’s also the only path forward. Intel could follow the path of many other American goliaths such as IBM and General Electric. A slow slide to irrelevancy, spinning off business, and bringing shame to what was once pride for American ingenuity. In short, failure. Pat Gelsinger and Intel are saying no to this path.
>
> SemiAnalysis (2021)

In this piece, we want to focus on something larger at play, specifically how Intel is attempting to correct their course by driving accountability across the organization through the corporate restructuring. We also wanted to discuss the software companies Intel has acquired over the last year months. First, let’s talk software.

We were able to get the chance to ask Pat Gelsinger about the software strategy at the Intel Vision 2022 event last week. The discussion was centered on these prior acquisitions, Intel potentially competing with their own customers, when Intel decides to open source, close source, or monetize their own software, and Intel’s future on build vs partner vs acquire.

> We're going to be doing more SAAS, more SAAS acquisitions. Silicon plus SAAS equals complete solution.
>
> Pat Gelsinger, Intel CEO

During that response, Pat bemoaned that Intel had developed so many technologies which are foundational to cloud computing but were never properly monetized. This software and middleware was monetized by Intel’s customers though. The belief appears to be that Intel could monetize what they develop as a service, which helps align incentives properly. Pat stated that Intel will continue to do open-source software, close source software that enables their chips, but that they would also move in the direction of software as a service.

> We sort of book a deal over north of $100 million in software revenue, and that's without us really trying to sell it… But this year, I'm going to increase that to about $150 million, but we think we can do more over time.
>
> Greg Lavender, Intel CTO

The $150M is a rounding error on a $70B+ annual revenue chip business, but 50% year over year growth is nothing to snuff at. This is organic growth, and Intel’s acquisitions as part of this effort to increase software revenue. Much of the organic development effort seems to be focused on creating security middleware to ensure application and data security such as with Intel’s “Project Amber”. Intel has already began quietly acquiring software companies. In just the last year, they have acquired Ananki, Granulate, Linutronix, Screenovate Technologies, and RemoteMyApp. None of these are transformative alone, but they do add tuck in SAAS businesses where it makes sense to. These acquisitions also don’t directly compete with customers such as the cloud service providers or most enterprise customers. We [previously did a deep dive on the Tower Semiconductor acquisition,](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?s=w) but we will do a brief take on the Intel software acquisitions in this article.

**Granulate** is the largest of these software acquisitions at about $650M for a startup with ~120 employees. Their software is incredibly interesting as the sell is it can autonomously and continuously optimize software at runtime without requiring the customer to make changes to their code. Anyone who knows a software developer knows that 99% of code is horrendously optimized. As we hit limits on Moore’s Law, innovative hardware architecture with software codesign is needed to continue to reduce the cost of compute. The enterprise is less equipped to do this versus a hyperscale company such as Amazon or Meta, as such, Intel needs to enable these enterprises to continue to see On-Premises to seem attractive. Various optimizations may even be built into the latest versions of Linux, frameworks, runtime libraries, etc, but do not on older versions which the application is running on due to compatibility or lack of engineering resources. Granulate assists massively with this legacy software issue by being able to optimize there as well. For more information, check out some of these [presentations](https://www.youtube.com/channel/UCLy8LLcP0oqzbqPMooMb9vQ/videos).

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

**Linutronix** seems to be a great acquisition. They develop PREEMPT_RT which works in real time running over Linux in addition to other services which are used for industrial applications. Their technology enables the management of interruptions and locks to minimize latency on CPUs amongst other things. Intel says they will operate as a separate software business which is a nice service to offer, but Linutronix also seems to enable Intel’s Network and Edge Group to have a competitive advantage. Given price wasn’t disclosed, this acquisition was likely quite cheap. Overall this seems to enable customers and offer a way to monetize the software work while not competing with them.

The acquisition of **Ananki** and the majority of the **Open Networking Foundation (ONF)** internal development team is by far our favorite of the bunch. Ananki was a spin out of the Open Networking Foundation which productized and built on top of the ONF stack. The ONF and Intel are committed to breaking down the proprietary barriers within the networking world. This [open approach to software is the playbook](https://semianalysis.substack.com/p/how-nvidias-empire-could-be-eroded) for defeating Broadcom in networking and Nvidia generally in AI and accelerated computing. The acquisition came alongside Intel open sourcing a load of great software solutions such as public 5G (SD-Core, SD-RAN), private 5G networks (Aether), software-defined broadband (SEBA/VOLTHA) and P4 programmable networks (SD-Fabric, PINS). We will likely dive deeper into the revolution that is occurring networking in software and architecture at a later date.

**RemoteMyApp** is the acquisition that makes the least sense to us. Intel acquired a game streaming company to build out their capabilities in both cloud game streaming and local/regional resource sharing from nearby computers. They launched “Project Endgame” for this task specifically. Intel explicitly stated they do not intend to run a game streaming platform like Nvidia does with their GeForce Now, but instead want to license the technology out to others. The interesting thing is that this technology can allow decentralized systems where computers that are idle can run games for others, and not necessarily be run through the cloud server environment. We simply don’t like it because the cloud gaming world is incredibly populated with the largest tech companies in the world.

**Screenovate** was a $100M to $150M acquisition. It was profitable multiple years in a row, which is quite rare as far as small software acquisitions go. Screenovate technology is a technology leader and IP owner in wireless device virtualization and cross platform screen sharing. Frankly, this is a boring acquisition to us because the tie in seems mainly relegated to the client computing. On the brightside, it also doesn’t really compete with customers.

# **Accountability**

Intel has 20,000 software engineers, more than any other purely semiconductor company out there. This is an immense amount of spending on software, and the incentives need to be aligned. Teams need to have their own budgets and demonstratable targets. By injecting SAAS business models where it makes sense, these software teams can have their own profit and losses. They can have demonstrable performance targets rather getting lost in the sea of larger organizations. On the other hand, silicon and product teams can continue to house software teams where it makes sense, and the software is meant to sell more chips directly.

Intel has restructured corporately so that teams have more direct goals. Intel reimplemented the famous Andy Grove technique of OKRs which ties financial incentives and promotions to exaction against objectives and key results. Product leads and managers follow products through conception through their lifecycle (within reason) which holds them more accountable to success.

The most important change is that divisions are more clearly delineated. The Datacenter and AI Group (DCAI) is now more clearly separated from the Accelerated Computing Systems and Graphics Group (AXG) and the Network and Edge Group (NEX). The sales organization oversees sales and pricing to a large extent, but they still cooperate deeply with the actual divisions. These changes become more obvious when we dive into a business unit such as the Accelerated Computing Group or the Intel Foundry business.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5a89496b-9ad4-4c7e-988b-e54dc0e445e4_1024x593.png)

AXG has clear verticals that they must operate in. Anything related to GPUs as well as high performance computing. They are tasked with building out this technology and productizing it. So great, it has its very own P&L, great. The first snafu would come in that the majority of the graphics technology Intel currently ships is actually through consumer CPUs. How does one handle this?

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7af443fd-e1ca-46e2-8b5d-fbf2092476f9_1024x189.png)

If you look at the fine print, Intel is having the client computing group do an intra-company revenue transfer of $700M in 2021 and scaling up to $1B in 2026 to compensate the accelerated computing and graphics team for their work. This in turn gives the team a base of revenue to deliver the client graphics IP from. The team has a clear starting budget, to start from. Raja Koduri and his team have clearly defined targets and must grow from there. As Q1 Intel earnings showed, there was a large operating loss of $390M on a base of $219M revenue for this group on a non-GAAP basis. Most of this came from the huge teams that are dedicated to making HPC, AI, and gaming GPUs a reality. These short-term losses are understood and accepted.

Over the long term, the spending on these areas can clearly be tracked and their success can be clearly attributed to Raja Koduri and his team. This can be done by both internal players and investors. Accountability really goes into overdrive when teams make mistakes or stumbles. This can clearly be seen with the AXG's constant delays.

The Ponte Vecchio High Performance Computing GPU and the Alchemist Gaming GPU were initially supposed to be in 2021, and neither has hit that target. Ponte Vecchio is starting to look like a 2023 release, so a 2 year delay versus initial plans. Not a good look. Moreover, while the Alchemist GPUs have barely launched. Many gamers would argue it hasn’t launched at all in fact. The Alchemist GPUs codenamed DG2 still has not released into the PC DIY market and it is looking like it will be Q3 which is nearly a year after they were initially planned to launch.

Why the delays? Intel initially blamed process technology on Ponte Vecchio first delay, but their blame game on Alchemist is software, which is quite odd. Our friends over at [Chips and Cheese](https://chipsandcheese.com/) did some sleuthing into Intel’s drivers and it indicates that the DG2_G10 and G11 (Alchemist) have many stepping from A0 all the way through C1 and C0 respectively. This could potentially indicate silicon engineering issues that aren’t being discussed in addition to the software issues.

We aren’t here to hate on AXG. They have a very tough ask of being told to build an entire GPU business from nearly scratch. It’s a long journey, an odyssey if you will, so let’s give them a couple more years before judging. The important bit is that there are relatively few products and each group and leader can be tracked much more closely by Intel internally and externally by shareholders.

The Intel Foundry Services business was also split out in the corporate restructuring. This includes existing foundry business such as with Achronix and Cisco as well as the advanced packaging business with [Amazon](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and). Intel could even use the same playbook where all the fabs are transferred to the foundry services business and the various business units have to do an intra-company revenue transfer to the foundry organization for chip supply and packaging. This could then be the easiest playbook for eventually selling a portion of the fabs or even making it completely public.

In our various discussions with Intel folks, the theme of accountability was very apparent. While it was never explicitly stated by anyone, the symptoms, increased responsibility and more meaningful measurable targets are being driven down the organization., This change is needed so that Intel isn't a titanically slow moving beast, but rather something more nimble and agile.

[Share](https://newsletter.semianalysis.com/p/turning-the-titanic-how-intel-is?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Leave a comment](https://newsletter.semianalysis.com/p/turning-the-titanic-how-intel-is/comments)

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

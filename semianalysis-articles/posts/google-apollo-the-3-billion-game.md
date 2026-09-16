---
title: "Google OCS Apollo: The >$3 Billion Game-Changer in Datacenter Networking"
subtitle: "Custom Optical Switches Reduce Broadcom's Networking Dominance"
date: 2023-03-17
source: https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Google OCS Apollo: The >$3 Billion Game-Changer in Datacenter Networking

**Custom Optical Switches Reduce Broadcom's Networking Dominance**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Networking is a critical part of any datacenter, especially with the rise of networking-intensive large language models. As such, it was a clear target for Google’s infrastructure optimization efforts. Over the last year at conferences such as OFC and SIGCOMM, Google disclosed their custom networking stack, Jupiter, from in-house switches all the way through to custom reconfigurable software.

This custom networking stack enables them to save at least $3 billion versus the industry standard implemented by competitors such as Amazon and Microsoft. In addition to cost improvements, Google also achieves higher network performance and lower latencies! This custom networking stack started being deployed more than 5 years ago and is now implemented in most of Google’s datacenters. Google’s custom networking was an integral part of training their most advanced large language models, including PaLM.

Before diving too deep into how their custom networking stack works, let’s quickly discuss what it does and the industry implications. First off, Google claims their custom network improves throughput by 30%, use 40% less power, incurs 30% less Capex, reduces flow completion by 10%, and delivers 50x less downtime across their network.

Most importantly, they can stagger datacenter networking upgrades. Google’s custom switch also enables them to eliminate the purchase of Broadcom networking switches in their spine layer of the network.

[Share](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game?utm_source=substack&utm_medium=email&utm_content=share&action=share)

The traditional network uses a “Clos” topology which is also referred to as a spine and leaf configuration, to connect all the servers and the racks of said servers together in a datacenter. In a spine and leaf architecture, you have a spine, leaves, and compute. Compute is a rack of servers full of CPUs, GPUs, FPGAs, Storage, and/or ASICs. That compute is then connected to leaves or top-of-rack switches, which then connect up through various aggregation layers to the spine.

![](https://substack-post-media.s3.amazonaws.com/public/images/ea677045-e1ad-4b46-b426-7cdd3df6cfab_624x339.png)

Traditionally the spine of this network uses what is called Electronic Packet Switch (EPS). These are the normal network switches of which Broadcom, Cisco, Marvell, and Nvidia are the leading providers. However, these EPS use a ton of power. Furthermore, every 2 to 3 years, networking speeds have doubled. While this doubling improves power consumption, it also comes with the requirement of upgrading the existing spine EPS. As such, there is always a huge wave of Capex associated with every new generation of Broadcom Tomahawk switch.

![](https://substack-post-media.s3.amazonaws.com/public/images/699f5cbf-e880-4971-9e02-f06569907ce1_624x365.png)

Google embarked on a project called Gemini to remove this spine layer of their datacenter networks which allows them to reduce both the power and the Capex costs associated with this layer of switching. Furthermore, this project doesn’t stop at the spine. It will continue to improve and potentially be adopted at lower layers of the network.

![](https://substack-post-media.s3.amazonaws.com/public/images/0c540268-0f19-435d-97f1-51efa25f368c_624x277.png)

Project Apollo is focused on replacing the traditional “Clos” architecture, which uses EPS with Optical Circuit Switch (OCS). The first generation optical switch is called Palomar. These OCS replace the spine of the old “Clos.” Instead of converting the signal from electrical to optical to electrical multiple times in the spine layer, OCS is an entirely optical interconnects which uses mirrors to redirect incoming beams of light, which are encoded with data from a source port to a destination port.

To use an analogy, OCS is like a railroad switch. They can have multiple paths, but the train can only traverse one specific track/path at a time. In order to change what path the train will travel, you have to redirect the track manually.

![](https://substack-post-media.s3.amazonaws.com/public/images/1e9caf1d-3e8a-4fcb-aaf2-7401222d2c54_1250x700.png)

In the case of Google’s network, if a section of the datacenter connected through port 7 wanted to talk to another section of the datacenter connected through port 4, but it was configured to port 11, then the optical switch has to reconfigure these mirrors to let port 7 to talk to port 4. Note that with a traditional EPS, there is no need to manually reconfigure anything because all ports are always connected through an electrical switch.

![](https://substack-post-media.s3.amazonaws.com/public/images/533902f5-37cf-4238-9583-6b33db59cc17_624x307.png)

Google uses these optical switches in a direct connect architecture to directly connect the leaves through a patch panel. This is not packet switching; this is, for all intents and purposes, an optical cross-connect.

To use the train analogy again, this is a massive train station with multiple tracks in and out. Any train coming in can be transferred to any train coming out, but it requires reconfiguring at the station.

Note in a typical network architecture; there is a packet header that is associated with every packet of data. This packet header is decoded and determines where the electrical switch will send that packet. There is no packet decoding happening in Google’s OCS. The packet is on a pre-determined path before it ever reaches the OCS. If you need to change what port you are talking to then you need to characterize the flow of the packets and where that flow is going. You need to know where the train is going before it ever enters the station.

In general, OCS is a “set it and forget it” solution because moving the mirrors to reconfigure the routing of packets flowing through the OCS takes several seconds. Compared to a traditional EPS, that is an eternity. You need to set the track the train will follow before it ever arrives.

![](https://substack-post-media.s3.amazonaws.com/public/images/6807edcf-c364-41c6-8f5f-9271651ff55b_624x184.png)

Google’s OCS is not a drop in replacement for EPS, the network has to be explicitly designed with OCS in mind to account for mirror reconfiguration time.

## **Advancing with Apollo: Data Rate Agnosticism, Low Latency, and Power Savings Unlocked**

The lack of flexibility and the non-drop-in compatibility are big drawbacks, but there are numerous advantages of OCS. Google outlines three big advantages: Data rate and wavelength agnostic, low latency, and significant power savings.

Data rate and wavelength agnosticism are important for two main reasons. The first reason is that you gain interoperability with any switch and optics technology which means that if you need to connect a switch with a 100G transceiver with a switch with an 800G transceiver, OCS can do that with no issues due to it just redirecting light instead of it moving packets.

![](https://substack-post-media.s3.amazonaws.com/public/images/31f0f736-b45b-40fc-b295-0dba94fd1aa9_624x328.png)

Once the OCS are set up, you can upgrade your switches and optics to much faster generations without having to swap out the “spine” of the network. The OCS can have a much longer lifespan than a traditional EPS.

![](https://substack-post-media.s3.amazonaws.com/public/images/c61846d2-4cfa-4b5a-8095-657491454d71_528x339.png)

A traditional EPS will have optical fibers come into the back of the switch, be converted to electrical signals through a photodetector and TiA, be [redriven and retimed through a DSP](https://www.semianalysis.com/p/marvells-dsp-dilemma-networkings), sent across a PCB, into standard switch silicon where the packet is decoded, and the path is determined. Then the packet is reencoded and sent out across that entire path again. Each of these steps incurs additional latency.

![](https://substack-post-media.s3.amazonaws.com/public/images/83c02eaf-c4d2-484c-b118-9f2604a4e7d1_1430x741.png)

The low latency of OCS comes from the fact that OCS does not have to decode packets; all they have to do is bounce the incoming light from the source port to the destination port.

![](https://substack-post-media.s3.amazonaws.com/public/images/72148e05-433c-4796-b329-ff1122001f21_550x364.png)

This leads to the third and biggest advantage, which is power. Each of these steps in a traditional EPS consumes a bit of power as well.

![](https://substack-post-media.s3.amazonaws.com/public/images/004b1162-e4a6-44d1-b04b-d288bfb16eeb_624x364.png)

We will have more on the performance benefits and power benefits in the supplementary section below.

## **OCS Obstacles: Addressing High Upfront Costs, Insertion Loss, and More**

There are four major disadvantages to OCS, all of which Google has claimed to have solved. The four major disadvantages are: high upfront cost, insertion loss, reconfiguration time, and lack of drop in support.

High upfront costs are something that Google can depreciate over a long period of time. Because OCS can deal with any bandwidth when Google moves to leaf switches to use 1.6T and 3.2T transceivers, these OCS don’t need to be replaced, which offsets the upfront costs. Google estimates that the overall Capex of the OCS is about 70% that of standard EPS due to the ability to reuse the OCS through multiple upgrade cycles.

![](https://substack-post-media.s3.amazonaws.com/public/images/17435510-2f8e-455e-80a1-6acad2bd9717_1032x552.jpeg)

If we assume that Google expects OCS to be used for 3 upgrade cycles, then the upfront cost of an OCS is ~3.5X that of an EPS (ASPs grow each generation of EPS). If Google believes these OCS can last 4 generations, then the upfront Capex difference is more like 6x!

Insertion loss is the next major disadvantage of an OCS. Insertion loss refers to the amount of signal power that is lost when an optical signal switches its medium of transport. For example, from a laser to a silicon photonics chip or a fiber to the photodetector. It is typically measured in decibels (dB) and is a measure of the reduction in signal strength. The higher the insertion loss, the more signal power is lost. For example, if a device causes a 3 dB insertion loss, the output signal power will be half of the input signal power.

![](https://substack-post-media.s3.amazonaws.com/public/images/33508de6-4d28-4bd9-93f6-b88749b8e087_561x563.png)

The more insertion loss you have, the weaker your signal will be, which could result in the unreliable transmission of data. Insertion loss is measured in decibels, and the fewer decibels of loss, the better and while the standard insertion loss for optical fiber is around 6dB, Google has reduced that to a worst case

Reconfiguration time is another major issue. Reconfiguring the mirrors for a different path takes a few seconds. Google has solved this by profiling its network traffic in detail.

![](https://substack-post-media.s3.amazonaws.com/public/images/07beb180-4464-44f9-a64f-06b9f2b154a7_1430x765.png)

They believe that building networks for the worst case of traffic patterns is overkill and that by planning network traffic, they can get away with the long reconfiguration time for mirrors.

![](https://substack-post-media.s3.amazonaws.com/public/images/6acd7767-dc05-4eb2-a882-3ec2733b148c_1430x733.png)

Lack of drop-in support is something that Google has solved by redesigning their networks in order to support OCS. Google has spent “a decade of evolution and production experience” with Jupiter and Project Apollo has been a significant step forward in Google’s drive to reduce TCO of these large networking systems. This is a part of secret sauce which Google won’t share publicly, although there are some details we can share after explaining the hardware.

## **Palomar MEMS Mirror Package: Unveiling the Heart of Google's Optical Circuit Switch**

The Apollo Project at first used a vendor-based solution for their OCS. Huawei also used this same vendor for their different use case in networks.

> Due to the difficulties in maintaining reliability and quality of this solution at scale, the decision was made to internally develop an OCS system.
>
> Google

That internally developed OCS is called Palomar.

![](https://substack-post-media.s3.amazonaws.com/public/images/cc04d329-0328-4f41-a866-de210eaa3673_624x491.png)

The centerpiece of the Palomar OCS is the Palomar MEMS mirror package which has 176 individually controllable micro-mirrors. However, only 136 mirrors are used due to 40 being disabled for yields.

- MEMS stands for Micro-Electro-Mechanical Systems. They are miniaturized mechanical and electro-mechanical devices that are integrated with electronic components and fabricated using microfabrication techniques.

![](https://substack-post-media.s3.amazonaws.com/public/images/457b78f6-b1a4-4bc6-9387-2fb0e7ac5af4_484x255.png)

The way that the different mirrors work is that the incoming 1310nm signal light (O band) is merged with a second 850nm light using a dichroic beam splitter which lets the 850nm through but reflects the 1310nm light. A dichroic beam splitter is simply an angled mirror with a coating on it that allows the transmission of certain wavelengths of light through it while reflecting other wavelengths of light.

In the case of the Palomar OCS, the wavelength of light that you want to transmit is 850nm light, and the wavelength that you want to reflect is 1310nm light. You do lose some of the light to losses incurred by the split due to not being able to reflect or transmit 100% of the light, but you can get well over 90% of the light where you want it.

![](https://substack-post-media.s3.amazonaws.com/public/images/8eb92f67-add1-4c62-b31a-30f8004b85d7_624x331.png)

From there, the merged light is bounced using the MEMS array to a second dichroic splitter which bounces the 1310nm back to the MEMS array but lets the 850nm light into a camera that monitors the alignment of the MEMS array. This alignment of the MEMS array is important because if the alignment of the array is just a little bit off then that would cause a break in the transmission of the data.

![](https://substack-post-media.s3.amazonaws.com/public/images/82c971d6-cb3a-4f7a-b5af-2aa3b18e5858_624x351.png)

There are 2 of these 850nm lights in order to maintain the MEMS array alignment, so the 1310nm light is still combined with the 850nm light when it bounces a second time off the MEMS array. Then when the combined beam hits the final dichroic splitter, this splits out the 1310nm to go to the output port.

![](https://substack-post-media.s3.amazonaws.com/public/images/102273b2-5076-4ce7-9282-7aec867a406e_532x294.png)

In order to cut the number of OCS ports and fiber cables in half to keep the complexity of the system down, Palomar uses optical circulators to have a bi-directional link. The optical circulator is a 3-port device where the input of port 1 is directed to port 2, and the input of port 2 is directed to port 3. This allows the conversion of a standard duplex transceiver into a bi-directional transceiver.

![](https://substack-post-media.s3.amazonaws.com/public/images/ed4bb676-5a56-43ee-a6f5-ce9f6eb5c48a_475x145.png)

This added return loss and crosstalk. Return loss is signal loss that happens at the end of an optical cable. The change in the refractive index of the light going from the optic fiber to a different medium, such as air, causes signal degradation, and a high optical return loss can cause the laser to not transmit correctly.

Crosstalk is when there is interference between two channels, which causes signal degradation and an increase in noise levels. So Google moved from using erbium-doped fiber amplifiers, which were limited to the 1530nm to 1565nm wavelength range (C-Band), to using optical coatings along with an optical re-design in order to be able to use the 1310nm wavelength range (O-Band). This re-design also reduced the return loss and the crosstalk of the system.

![](https://substack-post-media.s3.amazonaws.com/public/images/45a8fead-f1b9-42d1-8f0a-1fb8e702c7f0_386x215.png)

Google adopted Wavelength-division multiplexing (WDM) optical transceivers for Apollo. WDM is a technology that takes multiple optical signals and runs them through one optical fiber by using different wavelengths of light. The first generation of Apollo used the 40Gb/s standard as the baseline. This is a standard adopted across the industry (CWDM4 MSA), so the optics are standardized and commodity. The only unique aspect of the solution is the MEMS-based switch.

![](https://substack-post-media.s3.amazonaws.com/public/images/a05add0c-d4a2-4b43-ac31-7362f3f232a9_624x385.png)

## **Conclusion & Future**

Google, with their Apollo project, has developed a non-blocking 136x136 optical circuit switch that is both forward and backward-compatible with any bandwidth or wavelength Google uses or will use in its data centers. This switch, according to Google, only uses 108 watts of power consumption. Compared to a standard 136 port EPS switch, which would be in the 3,000 watts range.

So while there are disadvantages to OCS, Google has created a solution that has far more upsides than there are downsides for them. And over the past 5 years, “tens of thousands of 136x136 port OCS (eight spare ports) were manufactured and deployed.” Google has created a system that works incredibly very well for them.

In the future, Google is looking at a larger port count OCS for further scale-out capabilities as well as faster switching speeds to allow wider adoption of OCS in the lower layers of the network. This broader adoption would be tremendously negative to Broadcom, the leader in hyperscale networking switches. Furthermore, Google says they will also continue to improve reliability and lower insertion/return loss.

[Share](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Google is also investigating piezo-based switching technology as a replacement of the current MEMS-based system due to a piezo system having inherent advantages in insertion and return loss over MEMS systems. Switching speeds could also be faster. Google also shared their investigations with regards to MEMS, Robotic, Piezo, Guided Wave, and Wavelength Switching. Their investigation included relative costs, port count, switching time, insertion loss, driving voltage, and latching. We will share that below.

## **TPU Use**

OCS is used in all of Google’s TPUv4 and TPUv5 systems as well. It is a huge part of their superior perf/TCO.

## **Future, Supporting Data, Software, and Performance**

Below, we are sharing many files, images, and papers associated to the OCS. This includes traffic data and adoption of the OCS by Google. Included is also a picture of the switch as well as how Google profiles their traffic and implements the OCS. Furthermore, it shows the network performance benefits beyond just cost which was the main focus above.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

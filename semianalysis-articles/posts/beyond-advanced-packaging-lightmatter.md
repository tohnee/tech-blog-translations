---
title: "Beyond Advanced Packaging: Lightmatter Passage Chiplets Co-Packaged On Optical Interposer"
subtitle: "But will products utilize this in volume?"
date: 2022-08-22
source: https://newsletter.semianalysis.com/p/beyond-advanced-packaging-lightmatter
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Beyond Advanced Packaging: Lightmatter Passage Chiplets Co-Packaged On Optical Interposer

**But will products utilize this in volume?**

Lightmatter made a big splash a couple of years ago by presenting an AI accelerator, Mars, that rethought the paradigm of how electronics compute and move data. They presented a processor that used photonics for compute. This chip promised multiple orders of magnitude improvement in latency, bandwidth, and power. This ultimately was unsuccessful due to the rigidity of the software and compute structure involved with the chip.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8f059703-dabd-4a9a-9824-431ba42d3197_5292x1464.png)

Lightmatter has created a 2nd generation of this AI compute product called Envise, but that is not the focus of today’s post. We want to share what Lightmatter presented on their newest product, Passage. We are simultaneously physically attending SPIE Optics and Photonics as well as virtually attending HotChips, so if you are here at SPIE Optics and Photonics or in San Diego this week, [let us know](https://semianalysis.com/contact/), we would be happy to meet up.

The summary is that Lightmatter looks to break the [constraints of advanced packaging and IO](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited) with Passage.

The problem size in areas such as AI and HPC is growing exponentially, but Moore’s Law won’t be able to keep up.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7b0dba07-021b-4537-b869-0d305eb9bbb9_1518x837.jpeg)

As such, the industry has moved to using chiplets to put together larger packages to continue meeting computing demands. Breaking chips into many chiplets and exceeding the [reticle limit (physical limit of a lithography tool’s patterning limit)](https://semianalysis.substack.com/p/die-size-and-reticle-conundrum-cost) will enable continued scaling, but this paradigm still has issues. Even with [advanced packaging, the power costs of moving data out of chips will become a limiting factor](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited). Furthermore, the bandwidth is still limited even with the most advanced forms of packaging.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ba2dc917-bb89-41bb-a58a-139a82cf0a84_1535x812.jpeg)

Rather than putting silicon on top of silicon, Lightmatter wants to flip the advanced packaging game on its head with Passage. Passage connects to 48 customer chips on an optical interposer. Passage is built on [GlobalFoundries Fotonix 45CLO process technology](https://semianalysis.substack.com/p/globalfoundries-fotonix-the-leading). It is designed to connect many chips at very high bandwidth and performance. This optical interposer breaks bandwidth limitations by providing 768 Terabits per second between each tile and the possibility to scale to multiple interposers at 128 Terabits per second. This is a level of capabilities and scale that traditional packaging cannot achieve.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ff5139a6-ab92-4e22-adc6-352af3b9e499_1537x837.jpeg)

Optics has promised to solve the bottlenecks of electrical IO for decades. Technology has slowly progressed on that forefront. Pluggable optics, which Lightmatter dubs as Gen 1, has been used to connect switches within a datacenter for many years. Gen 2 and Gen 3 optics, where the optics are put on the same package or connected directly, is starting to come in [networking switches](https://semianalysis.substack.com/p/how-intel-was-designed-into-the-majority) and compute due to firms such as [Intel](https://semianalysis.substack.com/p/intels-trojan-horse-into-the-foundry) and [Ayar Labs.](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w) Lightmatter wants to skip straight to Gen 4 and Gen 5 with Passage.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c91688a0-3fc0-4099-8579-6e179e3bcac8_3058x1628.jpeg)

Standard co-packaged optics like Intel and Ayar Labs are targeting has an order magnitude lower scale than the optical interposer solution that Lightmatter is using. The interconnect density is 40x higher because only about 200 fibers could be inserted into a single chip. Furthermore, the interconnect is completely static whereas Passage has a dynamically configurable fabric.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5eaa4a69-d215-49fc-a1d2-31be3d5fffc8_2904x658.jpeg)

This optical interposer can perform switching and routing between chips. The entire interconnect can be reconfigured in under 1ms. Lightmatter says they can support all topologies such as all to all, 1D ring, Torus, Spine and leaf, and more. Passage’s switching and routing has a 2ns max latency between any chip to any other chip on the 48-chip array.

The switching is achieved by modulating colors with ring resonators and using Mach-Zehnder interferometers to guide them.

Lightmatter has A0 silicon of its [photonic wafer-scale interposer](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes) and claims it uses less than 50 watts per site. Each site has 8 hybrid lasers driving 32 channels; each channel runs 32Gbps NRZ.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1eae21c0-54b4-4d16-b2bb-4057bef9eb3b_3019x1611.jpeg)

Lightmatter’s [wafer-scale](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes) silicon photonics chip mostly uses silicon-based manufacturing techniques; it has many of the same constraints. Namely, the [reticle limit of lithography tools](https://semianalysis.substack.com/p/die-size-and-reticle-conundrum-cost). GlobalFoundries and Lightmatter get around this issue by stitching waveguides. Inter-reticle connections for the nanophotonic waveguides only has a 0.004 dB loss per reticle crossing. There is 0.5 dB/cm loss with the waveguides and 0.08 dB loss per Mach-Zehnder interferometer. There is also a 0.028 dB loss per crossing.

Lightmatter says that with UCIe, they can run the top spec of 32Gbps for chiplet to interposer interconnects. If direct SERDES are used, they believe they can run at 112G speeds. The customer ASICs are 3D packaged on top of the interposer. An OSAT would then assemble this final product. It can come in many variants, from 48 chips to smaller interposers with as few as 8 chips. The passage package has to also deliver power to the chips that are packaged on top. It does this by delivering up to 700W per tile with TSVs. Water cooling is required at this power level, but if the customer ASIC draws less, they can get away with air cooling.

Note that the claimed 768Tbps appears largely wasted.  Their functionality seems to allow them to couple one input to one output.  That leaves a large fraction of the interconnect idle.  It would be needed in order for them to figure out the pathways that do not conflict.  Those pathways are passive and waste little or no power when not used.  The MZI elements go left or go right.  No blending, no multicasting.  One entry, one exit.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/441a5861-a5d1-4158-a486-2b0612960149_1455x673.png)

Lightmatter also gave an example of disaggregated memory design and multi-tenant architecture. They started their interposer [can support any protocols, including CXL](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable). The customer ASICs on top of the interposer can be air-gapped by reconfiguring the network, so passing data between specific chips would be impossible. The big question is whether and when products will come. This could just be vaporware, or it could be the future for high-end leading edge disaggregated server designs. Lightmatter has to woo other companies to build chips for this platform. These firms have to trust their [expensive development](https://semianalysis.substack.com/p/the-dark-side-of-the-semiconductor) with an unproven partner.

If you like what you’re reading, share it! Spread the word!

[Share](https://newsletter.semianalysis.com/p/beyond-advanced-packaging-lightmatter?utm_source=substack&utm_medium=email&utm_content=share&action=share)

---
title: "Apple CPU Gains Grind To A Halt And The Future Looks Dim As The Impact From The CPU Engineer Exodus To Nuvia And Rivos Starts To Bleed In"
date: 2021-09-14
source: https://newsletter.semianalysis.com/p/apple-cpu-gains-grind-to-a-halt-and
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Apple CPU Gains Grind To A Halt And The Future Looks Dim As The Impact From The CPU Engineer Exodus To Nuvia And Rivos Starts To Bleed In

Apple has been long hailed for having the best CPU cores for consumer workloads for years. They have by far the highest performance per clock and efficiency driven by performance in the same class as AMD and Intel’s best current CPUs. This was driven by breakneck gains with architectural changes every year for a decade.

Now with the A15, these gains are really slowed. Apple in general was very clammy about the A15 comparison in the new iPhone reveal. Instead of comparing it to the previous generation like they usually do, they opted to compare to ambiguous “competitors.” That’s great, but we are only a few months away from new Qualcomm, Samsung, and MediaTek chipsets.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/426565e0-52bf-484e-b8d8-a0c943e31f18_1024x576.jpeg)

To quickly cover the specifications, it is a 2+4 core big little CPU and a 4 or 5 core GPU depending on whether its cut down in the regular iPhone or iPhone Pro/iPad Mini. The CPU is claimed to be 50% faster than the competition while GPU is claimed to be 30% or 50% faster depending on whether it is 4 cores or 5 cores. They are sticking with a 16 core NPU which is now at 15.8 TOPs vs 11 TOPs for the A14. There is a new video encoder and decoder, we hope it incorporates AV1 support. The new ISP enables better photo and video algorithms. The Pro models have variable refresh rate, so that likely necessitated a new display engine. Lastly, the system cache has doubled to 32MB. This was likely done to feed the GPU and save on power. SemiAnalysis also believes Apple did not move to LPDDR5 from LPDDR4X.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3cc6ccca-2fdc-47e8-83f1-191d491a6e74_1024x576.jpeg)

There is a lot of difficulty with comparing to the previous generation A14, but the iPad mini does give us some help. They state the new iPad mini has a 40% faster CPU and 80% faster GPU versus the previous iPad mini which contained the A12. We had to do similar math last year as the iPad Air was announced with the A14 first and only compared to the previous iPad Air which contained the A12 as well. That announcement gave us us this quote below.

> This latest-generation A-series chip features a new 6-core design for a 40 percent boost in CPU performance, and a new 4-core graphics architecture for a 30 percent improvement in graphics.

The most important thing to note is that the CPU gains are identical from the A12 to A14 as they are from A12 to A15. The GPU gains are quite impressive with a calculated 38.5% improvement. This is larger than the A13 and A14 improvements combined.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f2ab32e4-1fc2-4988-a78c-3df57ca173f7_1023x343.png)

These are performance gains are generally paltry despite a huge increase from 11.8B transistors to 15B. Furthermore, with next year’s [A16 on the N4](https://semianalysis.substack.com/p/qualcommmediatek-will-beat-apple) process rather than N3, gains look to continue to slow.  The [slowing of process technology, and especially SRAM](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/) is going to be a hammer for the industry. Apple is clearly investing their transistor budget in the non-CPU aspects of the SOC. Fixed function and heterogeneous compute reign supreme.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9d32b3d4-1c3f-44df-89e9-e6306d368629_1024x676.png)

It appears Apple has not changed the CPU much this generation. SemiAnalysis believes that the next generation core was delayed out of 2021 into 2022 due to CPU engineer resource problems. In 2019, Nuvia was founded and later acquired by Qualcomm for $1.4B. Apple’s Chief CPU Architect, Gerard Williams, as well as dozens of other Apple engineers left to join this firm. More recently, SemiAnalysis broke the news about [Rivos Inc, a new high performance RISC V startup](https://semianalysis.substack.com/p/rivos-inc-a-chip-off-the-old-block) which includes many senior Apple engineers. The brain drain continues and impacts will be more apparent as time moves on. As Apple once drained resources out of Intel and others through the industry, the reverse seems to be happening now.

We believe Apple had to delay the next generation CPU core due to all the personnel turnover Apple has been experiencing. Instead of a new CPU core, they are using a modified version of last year’s core. One of these modifications is related to the CPU core’s MMU. This work was being done for the upcoming colloquially named “M1X” generation of Mac chips. Part of the reason for this change is related to larger memory sizes and virtualization features/support. In addition, there may be other small changes as well, but we need hardware in the hand to analyze that. We also aren’t sure if Avalanche and Blizzard are the next generation cores or the current modified Firestorm and Icestorm cores.

Regardless of the paltry CPU gains and potential core architecture delays, Apple is still the leader in performance per watt. With Intel design teams starting to get back on track, AMD executing almost flawlessly, and Qualcomm coming in soon like a hammer with Nuvia cores, we aren’t sure if this lead will be sustained. The A11 to A12 generation was seen as Apple starting to asymptote out on gains with only a 15% gain, and the A13 to A14 looked even more weak with 8.3% gains, but now with no CPU gains, let's cross our fingers and hope the A16 brings a large architectural change.

Edit: Adding statistics from initial benchmarks which further back the article.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/134fcad2-4be1-45bd-9239-470c60711261_1292x544.png)

Battery life increases are commiserate to increases in battery size for the most part. The stand out of course is the new LTPO panel and VRR in the Pro iPhones. There is also a bump in WiFi streaming, which indicates RF stack optimization and the improvements in the media block’s encoder/decoder that was mentioned above.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/350ec3b7-8755-4a2f-9406-775cef7246f3_1507x1200.png)

CPU gains are 7.7% in single thread overall. In general increases are about the same as clock increases from 3GHz to 3.23GHz. The weak scaling on some of these indicates to me that LPDDR5 may not be present. Part of the motivation for this could be that the doubled LLC was sufficient and they didn’t need to spend the ~30% more on LPDDR5 vs LPDDR4x. Some tests may benefit from the LLC doubling to 32MB, others won't scale perfectly with clocks.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9d36f0f7-af3a-4938-a37d-55d593aabeba_739x498.png)

The GPU comparison is the iPhone Pro Max vs Pro Max. This includes the full 5 core GPU in the A15. There is roughly a 50% increase in performance, but the SFFT sub score is particularly interesting. 150% would indicate doubled ALUs per GPU core. 130% is pretty dang close, and the 1 additional GPU core isn't enough for that alone. It's likely they went to 2xFP32 on the GPU.

[We also would like to do a bit of a victory lap on calling out that garbage rumor about Satellite internet on the iPhone 13.](https://semianalysis.substack.com/p/no-the-iphone-13-does-not-have-satellite)

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

[Share](https://newsletter.semianalysis.com/p/apple-cpu-gains-grind-to-a-halt-and?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Leave a comment](https://newsletter.semianalysis.com/p/apple-cpu-gains-grind-to-a-halt-and/comments)

*This article was originally published on [SemiAnalysis](https://semianalysis.com/apple-cpu-gains-grind-to-a-halt-and-the-future-looks-dim-as-the-cpu-engineer-exodus-to-nuvia-and-rivos-impact-starts-to-bleed-in/) on September 14th 2021.*

*Clients and employees of SemiAnalysis may hold positions in companies referenced in this article*.

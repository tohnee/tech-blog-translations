---
title: "Google New Custom Silicon Replaces 10 Million Intel CPUs | Google Argos VPU"
date: 2021-06-02
source: https://newsletter.semianalysis.com/p/google-new-custom-silicon-replaces
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Google New Custom Silicon Replaces 10 Million Intel CPUs | Google Argos VPU

The trillion dollar tech companies are on a quest to become vertically integrated monsters. Google is no slouch on this front and has a myriad of custom and semi-custom silicon projects from the famous TPU for AI to the Titan security chip to upcoming releases such as Pixel/Chromebook SOCs, Arm Neoverse server CPUs, and Waymo self driving systems.

Google has continued along their custom silicon ambitions by creating Argos, a new class of ASIC called VCU (Video Coding Unit). By deploying this custom silicon across their datacenters, **Google replaces millions of x86 CPUs** and enhance their service offerings. This custom silicon has been rolled out for quite some time and Google is already nearing deployment of their second generation VCU which will include enhancements such as AV1 encoding support.

The VCU is designed specifically to accelerate video workloads across product offerings such as YouTube, Google Photos, Google Drive, and Stadia Game Streaming. While there is a greater demand for video sharing ability with greater resolutions and more volume, improvements in video processing are slow. Future growth in video acceleration is not sustainable without adopting domain specific hardware accelerators. Google received over 500 hours of YouTube footage every minute in May of 2019. This amounts to a gargantuan amount of data that must be encoded in standard formats, stored, and streamed out to users.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/26ab7c23-f57e-4075-b9df-1139a0844416_717x1024.jpeg)

Google takes input video and encodes it at every viewable resolution in H264. Additionally, the most viewed videos are also encoded in VP9. VP9 is a more complex video codec that allows a video file to become smaller and maintain the same picture quality. It can also store the video at the same size but be a higher quality video. VP9 allows Google to save large amounts of bandwidth that they stream out of their datacenter to the consumer through their content delivery network. This in turn lowers their costs drastically. If Google could switch entirely to VP9, they can also utilize less storage across their entire library of stored videos.

This codec isn’t all positives though, CPUs struggle with encoding this format and are nearly 5x slower. Google provided encoding performance in their disclosure of this product. Using the quoted performance, if we assume that Google’s servers are utilized at 100% (they aren’t), all YouTube/Google Photos/Google Drive footage video is 1080p 30FPS, and the target is H264, the workload would require ~904,000 Intel Skylake server CPUs to encode. Google switching to VP9 with the same set of assumptions would require ~4,193,000 Intel Skylake server CPUs. If the ingest footage is 4k 60FPS, then the number of CPUs required for H264 is ~7,205,000, and VP9 requires ~33,407,000.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/73c94707-9bb1-43f9-a71d-513dab34d26b_1024x386.png)

The need for a purpose-built accelerators is obvious with CPUs simply being inadequate for the task at hand. Many would turn around and ask about GPUs. While they do provide slightly better TCO, they are also going to come with lower utilization rates and less flexibility of workloads for new encoding schemes such as VP9 and AV1. GPUs do not provide enough of an uplift to be worth using for this. This makes then unsuited to the task at hand as well.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c93da000-e3f9-4c27-bf06-2f2c26e1425d_1024x523.png)

In comes Google’s Argos VPU, each of the Argos chips is packaged onto a single PCIe Card. 10 of these PCIe cards can be used in each single server. They offer significantly higher performance and power efficiency by being purpose built for the task at hand. One would assume that R&D costs would be huge, but all of the IP except for the encoder core is licensed from third parties. This significantly reduced costs and the time to engineer the solution. It was built using a modern mobile SOC methodology and point of view which allowed the rapid integration of IP from various sources.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/387ad440-5f2a-4ef8-bee1-916c1c9bc2a2_1024x255.png)

Core to the solution is hardware-software co-design. The system must be architected to function from the individual hardware encoder cores in each Argos chip all the way from the individual encoder cores and memory to entire chips, PCBAs, server nodes, clusters, and regions. Such deep integration is needed to maximize utilization rates, balance loads, deploy at scale, and be adaptable as the frameworks of the Google services, which are constantly tweaked. Each encoder and decoder core, and VCU memory controller can be divided to ensure full utilization.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f22f49b8-3fc6-4159-84b0-85d24301f9cc_1024x594.png)

The hardware software co-design goes both ways. In addition to using an industry standard Electronic Design Automation (EDA) tool from Mentor Graphics’ called Catapult, Google also designed their own in-house tool for integration called Taffel. **Google’s ambitions for silicon independence are so broad they are developing their own EDA tools!** They still rely on the greater EDA industry, but to a lesser degree. Verification is upwards of 50% of costs when designing a chip, so SemiAnalysis believes the in-house tool likely targets this part of the silicon design process.

> With HLS, there was 5-10x less code to write, review, and maintain compared to a traditional Verilog approach.

Google claims they have a flow that is far more efficient than the old tried and true Verilog approach. They also claim that testing throughput was accelerated by 7-8 orders of magnitude. Beyond the scope of this individual chip, Google clearly has long term ambitions to become a semiconductor monster through their vertically integrated, in-house chips.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/73c94707-9bb1-43f9-a71d-513dab34d26b_1024x386.png)

Rolling it all up, Google achieves a 7x improvement in total cost of ownership (TCO) for the infrastructure needed to encode videos on H.264, and a 33.3x improvement in VP9. This TCO improvement accounts for the cost of the chips plus 3 years of operational expenses. R&D costs are accounted for in this calculation for the VCU.

Using the same assumptions of 100% utilization rates (which are totally unrealistic), if every video that Google received is encoded in VP9, the total number of Intel Skylake server CPUs required reaches ~4,192,000 assuming 1080p 30FPS quality. Google deploys 2 VCU’s per PCIe card and uses 10 cards per server. These servers still utilize 2 Intel Skylake CPUs as well. In order to encode all the video they receive at 1080p 30FPS quality, Google would need ~21,500 of these servers. These servers would total ~43,000 Intel Skylake server CPUs and ~430,000 of their in house Argos VPUs. That is 4 million fewer server CPUs that Google has to buy from Intel!

If you assume the quality of uploaded footage is at 4k 60FPS, the reduction from ~33,407,000 Intel Skylake server CPU is even more mind boggling. They drop down to ~170,000 servers needed with ~340,000 total CPUs and ~3,400,000 Argos VPUs. The job of 33 million CPUs is now gone. We believe the average video uploaded to Google Photos and YouTube are likely not 4k 60FPS, but they also likely average out to higher than 1080P 30FPS. The Google VCU saves between 4 million and 33 million CPU purchases, but our estimate is around 10 million. This takes into account the fact that utilization rates are not 100% and that the average upload is slightly beyond 1080p 30FPS.

These huge gains in cost and speed allowed Google to enable VP9 across all platforms, even on rarely watched videos. Storage and bandwidth egress costs are reduced significantly. They also can use VP9 for Google Stadia streaming which allows 4k 60 FPS gameplay streaming.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/69ef1058-1d3e-4bcf-b766-50ad5f71d517_800x444.png)

What’s next for Google VCU? The next generation is already under the works according to SemiAnalysis sources. It will be able to encode the AV1 format which would be completely impossible on CPUs or GPUs. Further storage and bandwidth savings will be realized. Furthermore, they are planning to start adding machine learning inference hardware onto the new silicon as well. Lastly, they will also add networking onto the add in cards themselves in order to drive efficiency and reduce communications with the host CPU. This will allow them to automatically generate video captions, check for violations of terms of service, and even allow video search to be enabled on YouTube and Google Photos.

The 10 million CPU savings are tangible now, but enabling these next generation features would be absolutely impossible without Google custom silicon. This will drive a tangible lead in video workloads over other tech companies, not just in cost, but also in capabilities. Amazon with Twitch.tv and Facebook/Instagram need to work on their own silicon for this workload or else they will be left in the dust competitively. [TikTok’s owner ByteDance is even working on their own silicon tailored to their video workloads.](https://www.bloomberg.com/opinion/articles/2021-03-17/bytedance-move-into-chips-will-find-backing-in-china-s-tech-independence-drive) Merchant silicon vendors such as Intel, Nvidia, and AMD are going to find themselves completely kicked out of the worlds largest tech companies video based workloads.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

[Share](https://newsletter.semianalysis.com/p/google-new-custom-silicon-replaces?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Leave a comment](https://newsletter.semianalysis.com/p/google-new-custom-silicon-replaces/comments)

*This article was originally published on [SemiAnalysis](https://semianalysis.com/google-new-custom-silicon-replaces-10-million-intel-cpus-google-argos-vpu/) on June 2nd 2021*.

*Clients and employees of SemiAnalysis may hold positions in companies referenced in this article*.

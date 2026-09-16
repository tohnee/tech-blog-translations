---
title: "AMD Advancing AI: MI350X and MI400 UALoE72, MI500 UAL256"
subtitle: "Software Improvement, Marketing RDFs, AMD Fostering Neocloud, MI355 is not Rack Scale, MI400 is UALoE, Not UALink"
date: 2025-06-13
source: https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256
crawled: 2026-09-15
authors: ["Kimbo Chen", "Dylan Patel", "Daniel Nishball", "Wega Chu", "Ivan Chiam", "Gerald Wong", "Patrick Zhou"]
tags: []
audience: only_paid
paywalled: true
---

# AMD Advancing AI: MI350X and MI400 UALoE72, MI500 UAL256

**Software Improvement, Marketing RDFs, AMD Fostering Neocloud, MI355 is not Rack Scale, MI400 is UALoE, Not UALink**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

For the past six months, [AMD has been in a Wartime stance](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/). They have been working hard and working smart towards their goal of being competitive with Nvidia. At its Advancing AI 2025 event, AMD launched the MI350X/MI355X GPUs which could be competitive to Nvidia’s HGX B200 solutions for inference of small to medium LLMs on a performance per TCO basis. Notwithstanding the reality distortion field projected by AMD, the MI355X is not a rack scale product, and it is not competitive against Nvidia’s GB200 NVL72 at frontier model inference or training.

Instead, it is the MI400 Series that is a true rack scale solution that could potentially be competitive with Nvidia’s VR200 NVL144 rack scale solutions in H2 2026. There is also some marketing spin around the MI400 Series as AMD has renamed its “IF over Ethernet” protocol to “UALink Protocol over Ethernet”, which is not real UALink.

In this article, we will discuss the relative competitiveness of AMD’s new products and analyze their total cost of ownership. We will also elaborate on AMD’s new hyperscale customer, AWS, and on the flip side, the continued disappointment in follow-on orders on from existing customer Microsoft.

Recently, Nvidia has upset quite a few of their Neocloud partners with the launch of DGX Lepton Marketplace, which aims to commoditize compute. We believe that this development has also helped to open up a window of opportunity for AMD to foster their own Neocloud ecosystem. We will explain how AMD is more willing to invest into Neoclouds, the clever financial engineering they are employing to help out these Neoclouds, as well as the investment AMD is making into their own internal development R&D clusters.

## Executive Summary

1. The MI355X is competitive with the HGX B200 for small to medium model inferencing but it will not be competitive against the GB200 NVL72
2. Despite AMD’s [marketing RDF](https://en.wikipedia.org/wiki/Reality_distortion_field), the MI355 128 GPU rack is not a "rack scale solution" – it only has a scale up world size of 8 GPUs versus the GB200 NVL72 which has a world size of 72 GPUs. The GB200 NVL72 will beat the MI355X on Perf per TCO for large frontier reasoning model inference
3. The MI355X will have similar collective performance as the HGX B200 but MI355X collectives will run at least 18x slower than on the GB200 NVL72, if not even slower
4. AMD announced its Developer Cloud, which will bring on demand pricing to $1.99/hr/GPU for the MI300 vs $3.00/hr/GPU in the current AMD Neocloud market in a move that could potentially make renting AMD GPUs competitive vs renting Nvidia GPUs
5. Nvidia’s DGX Lepton Marketplace has upset a lot of Neoclouds, potentially giving AMD an opening to convince Neoclouds to support both Nvidia and AMD
6. AMD is finally adopting a similar strategy to Nvidia and using its strong balance sheet to support the Neocloud and hyperscale ecosystem in adopting AMD by renting a portion of GPUs back from the clouds. This will help drive accelerate end user adoption of AMD’s systems.
7. The MI400 Series will be a rack scale solution that could potentially be competitive with Nvidia’s VR200 NVL144 in H2 2026
8. There is a new work in progress initiative to raise AMD engineering pay to be more competitive with market rate and to more closely align compensation with the success of AMD. The timing for which AMD will announce this to their AI engineers remains to be seen
9. The MI400 Series racks are not actually using real UALink for scale-up networking. AMD has instead renamed its Infinity Fabric Over Ethernet to “UALink over Ethernet” and uses this for its scale-up network
10. The MI400 Series scale-up network will use Broadcom Ethernet Tomahawk 6 switches because Marvell and Astera Labs’ UALink switches will not be ready by late 2026
11. Despite these earlier points, the MI400 Series with UALink over Ethernet will still be competitive with the VR200 NVL144’s NVLink in terms of scale up bandwidth and also has a scale up world size of 72 logical GPUs
12. In late 2027, AMD will release the MI500 UAL256 which will feature 256 physical/logical chips and not just 144 physical/logical chips like in VR300 NVL576

## MI350X and MI355X Specs

There are two versions of the CDNA4 chips in this series – namely the MI350X and the MI355X. The MI350X is the 1,000W version that is air cooled while the MI355X is a 1,400W version that supports both air cooling and DLC liquid cooling. Even though the MI355X uses 1.4x more power, the on-paper specs show that it is less than 10% faster than the MI350X in terms of TFLOPS throughput. However, we expect realized performance to be greater than 10% better for the MI355X because published specs are often never achieved due to power limitations. These published specs assume that the peak clock speed can be held in real workloads, but that’s simply not the case on both AMD and Nvidia systems.

The on-paper specs for the MI350X and the MI355X are both competitive to the HGX B200 for BF16/FP8/FP4 data types (dtypes). We expect that BF16 and FP8 will be used for training while FP8/FP6/FP4 will be used for inference. On the HGX B200, FP6 shares the same physical circuits as FP8, leading to the same FP8/FP6 on paper FLOP/s. On the MI355X, FP6 shares the same physical circuits as FP4, and so FP6 will have the same peak TFLOP/s speed as FP4. This means that MI355X FP6 is 2.2x faster than B200 FP6. In practice, MI355X FP6 will be at least 20% slower than MI355X FP4 due AI chips always being limited by power.

[SemiAnalysis benchmarking has shown](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/) that even though the MI300X and the H100 each show the same on-paper TFLOP/s for FP16 as for BF16 (i.e. Nvidia’s FP16 TF = BF16  = 989 TFLOP/s, AMD’s FP16 = BF16 = 1307 TFLOP/s) in practice – each card delivers different realized TFLOPs when running FP16 vs BF16. We will be publishing an article in the near future running microbenchmarks to figure out a realistic TFLOP/s for MI355X FP6 versus FP4.

![](https://substack-post-media.s3.amazonaws.com/public/images/0dbf89d7-a405-4a9a-939f-da8bf2af0d29_1616x578.png)
*Source: SemiAnalysis*

For 4-bit floating point formats, the MI355X will only support OCP MX4 where there is a microexponent scale factor applied across a block of 32 elements versus. In contrast, Nvidia’s Blackwell GPUs support both OCP MX4 and NVFP4, though NVFP4 uses a smaller block size of 16 elements which will lead to fewer challenges when calibrating the numerical accuracy when doing QAT/PTQ quantization. We have talked with a few vLLM and open-source inference contributors, and they have mentioned that NVPF4 preserves information/model quality much better than MX4, but that MX4 could potentially achieve the same quality with additional runtime quantization software techniques.

On the Blackwell Ultra B300 HGX NVL8, Nvidia has removed most of the FP64 and int8 tensor cores to make room for 1.4x more FP4 tensor core circuits. This allows the B300 to dominate FP4 inference when compared to the MI350 and MI355 which do not use this optimization. As a result, the B300’s FP4 TFLOP/s is 1.3x faster than that of the MI355X while consuming 200 W less power.

In terms of HBM, the MI350/MI355 has the same memory bandwidth and capacity as B300, but has much more HBM at 288GB vs 180GB for the B200. This is a critical advantage when it comes to AMD single node inference. However, in the age of multi node high rank expert parallelism and disaggregated prefill, having more HBM per GPU is not as critical though it is still beneficial. Bandwidth is far more important, which is why 8Hi HBM4 is being rushed by 2 HBM vendors for 2 different high profile ASIC programs. See the SemiAnalysis accelerator and HBM model for more details.

For the MI350/MI355’s scale-up network, AMD was able to “overclock” their XGMI protocol (which uses PCIe 5.0 PHY Serdes) by 1.2x from 64GByte/s to 76.8GByte/s. It does thus by using PCIe 5.0 PHY extended speed mode which offers ~38GT/s per link instead of 32GT/s per link. Despite this, comparable Nvidia products still crush the MI350/MI355’s scale up network speed because the HGX B200/B300 uses a switched all to all topology which is 1.6x faster than that of the MI350/MI355’s mesh topology based scale-up network. When it comes to the GB200 NVL72/GB300 NVL72, there is really no comparison or competition versus the MI350/MI355’s scale-up solution, because the GB200 NVL72/GB300 NVL72 is a true rack scale solution connecting 72 GPUs within a single scale-up domain while the MI350/MI355 only connects 8 GPUs together in its scale-up domain.

![](https://substack-post-media.s3.amazonaws.com/public/images/4761c86a-12e9-42a3-9110-3e7d827bd110_1127x975.png)
*Source: SemiAnalysis*

Moving on to the scale-out domain, the MI350/MI355 supports speeds of 400 Gbit/s per GPU – the same as B200 and GB200 NVL72, but it will be surpassed soon by B300 HGX NVL8 and the GB300 NVL72 which both offer 800 Gbit/s per GPU networking. AMD as a whole will lag behind on scale-out networking as Nvidia will start mass deployments of their 800GbE ConnectX-8 NIC later this year while AMD’s 800GbE “Vulcano” NIC will not start mass deployment until 2H 2026.

## Competitive Performance per TCO with the HGX B200 NVL8

We believe that the MI355X could be competitive against the HGX B200 for small to medium LLMs production inference workloads. This is because the MI355X total cost of ownership is 33% lower than that of the HGX B200 for self-owned clusters, while it delivers much more HBM memory capacity, slightly more FP8 and FP4 TFLOP/s and double the FP6 TFLOP/s. Rapid improvements to AMD software under the leadership of Anush, AMD’s AI Software King, will also push the MI355X’s relative performance per TCO advantage higher.

AMD’s pitch on the competitiveness of the MI355X centers around the fact that it doesn’t require direct to chip liquid cooling (DLC). There certainly is merit to some point, but there is a degree of irony to the fact that AMD is still pitching the next gen MI355X as a competitor to Nvidia’s “economy-class” HGX products that have already been in the market for some time. AMD’s MI355X cannot compete head on with Nvidia’s flagship GB200 NVL72 for frontier reasoning inference due to the smaller scale-up world size mentioned above, so it is instead positioned to compete with the air-cooled HGX B200 NVL8 and the air-cooled HGX B300 NVL8.

With that said, this product segment will ship meaningful volumes, depending on the MI355X’s software quality and the price that AMD is willing to sell at. We expect that it could gain the most traction among users of small to medium models that do not benefit from large scale-up world sizes. But when it comes to reasoning models and frontier inference deployments that do benefit from large-scale disaggregated deployments or employ mixture of experts that can take advantage of large scale up networks, the GB200 NVL72 will still dominate on performance and perf per TCO, especially when it comes to inference.

![](https://substack-post-media.s3.amazonaws.com/public/images/e1a3295f-0074-45b9-a44d-a281e4d92143_1471x632.png)
*Source: SemiAnalysis*

## Nvidia is Upsetting Neoclouds with DGX Lepton

This week at GTC Paris, Jensen Huang discussed more about DGX Lepton and its business strategy which could lead to the commoditization of AI compute at a global scale. This means customers will be able to automatically and seamlessly shift their inference workloads from different clouds while in theory maintaining the same software user interface and experience. This is particularly attractive to those that mainly focus on inference and small-scale training workloads as we don’t expect that massively scaled inference deployments or large-scale training will use DGX Lepton.

If DGX Lepton is successful, they will have created a standard user experience, with exactly the same feature set, value proposition and performance across all Neoclouds, which will put all the Neoclouds into a race to the bottom on pricing. They will effectively be turning Neocloud margins into ultra-low commodity level margins.

In the same way that Uber/Lyft is a platform for connecting customers to drivers, DGX Lepton appears to be seeking to be that platform for GPU compute. Famously, Uber/Lyft have spawned an entire army of low margin gig economy workers that are captive to their platforms. DGX Lepton could have the same effect on Neoclouds.

On the other hand, like Uber/Lyft, DGX Lepton will be great for consumers. By lowering middleman margins, Nvidia has effectively increased performance per TCO for end users without any impact to Nvidia's own eye watering margins. Compute will get cheaper, while the experience will be standardized.

From discussions with various Neoclouds, many are not happy about the DGX Lepton Marketplace for the aforementioned reasons. Even though they are not happy about DGX Lepton, many still feel obligated to participate to maintain a good relationship with Nvidia. [The Information recently posted an article](https://www.theinformation.com/articles/nvidia-muscles-gpu-cloud-market-rankling-new-rivals) that also elaborated on the very mixed feelings at the Neoclouds and overall unhappiness with DGX Lepton. [Some engineers that are part of the NVIDIA Lepton team are also allegedly anxious about how their working relationships with the Neoclouds will develop.](https://x.com/anissagardizy8/status/1932942527574782087)

One alternative approach that Jensen could take at DGX Lepton would be to completely open-source Lepton’s amazing software platform and allow free of charge deployment of Lepton’s software for participating Neoclouds when they self-host Lepton’s software in addition to when they participate in the DGX Lepton marketplace.

This will let Neoclouds have multiple sales channels independent of Nvidia’s marketplace while still bringing consumers strong performance and a better experience, raising the bar for the overall ecosystem.

One outcome of the ongoing DGX Lepton drama is that Neoclouds are starting to revisit the idea of relying completely on a single vendor, and many may ultimately seek alternatives to ameliorate this risk. This development has created a perfect opening for AMD to rapidly ramp up their Neocloud engagement and quickly expand the number of Neoclouds that host AMD GPUs.

## MI355X Is Not a Rack Scale Solution – AMD’s Marketing Spin

AMD has been marketing a MI355X as a “rack scale solution” even though the MI355X is not a rack scale solution by any definition. The MI355X “128 GPU Rack” is just 16 MI355X UBB8 servers put in the same rack but without a coherent scale up domain that spans across the entire rack.

The MI355 “128 GPU Rack” is rack scale from temu dot com. Calling the MI355 DLC Rack a “rack-scale solution” is like trying to pitch your producer on [hiring Jesse Plemons instead of Matt Damon](https://people.com/jesse-plemons-does-not-really-think-he-bears-a-resemblance-to-matt-damon-8662275) in your upcoming Hollywood blockbuster.

As we will elaborate on further, this means that the MI355X “rack-scale solution” has 18x worse collective performance compared to the GB200 NVL72. For the MI355X, a GPU in UBB8 server A can only talk to a GPU in another GPU in UBB8 server B in the same rack at 400Gbit/s over Ethernet versus, whereas for the GB200NVL72, GPUs in different compute trays communicate at 900GByte/s.

![](https://substack-post-media.s3.amazonaws.com/public/images/7e5c9244-689c-49f9-94fb-74f92cb73fe5_963x441.jpeg)
*Source: AMD*

If the MI355 128 GPU rack is considered to be a “rack scale solution”, then why not call the many H100 racks as a “rack scale solution” too? Obviously, if the MI355 is labeled a “rack scale solution”, the H100 should be considered a “rack scale solution” too. This is a ridiculous proposition as nobody is calling xAI’s H100 deployment with 64 GPUs per rack a “rack scale solution”. Like the MI355, this H100 deployment does not have a coherent scale up domain across all 64 GPUs, it is just eight HGX H100 NVL8 servers in a rack.

![](https://substack-post-media.s3.amazonaws.com/public/images/f1ef59ca-a43e-4546-8aca-5a37d8755032_1199x800.jpeg)
*XAI’s “rack scale solution”. Source: ServeTheHome*

When it comes to inference and training of mixture of experts models, the most important and communications intensive collective is the all to all operation, which routes tokens to the correct expert. For all to all communication, the MI355X is 18x slower than the GB200 NVL72 and 2x slower than the HGX B300 NVL8.  For training models using 2D+ parallelism, a common LLM pattern is using an all reduce with a split mask of 0x7, and for this operation, the MI355X is also 18x slower compared to GB200 NVL72.  This example illustrates that MI355X is clearly not rack scale and not in the same league as the GB200 NVL72.

![](https://substack-post-media.s3.amazonaws.com/public/images/9d15aa33-b0a1-46cc-83ce-14d8aae7c595_1322x748.png)
*Source: SemiAnalysis*

## Hyperscale and AI Lab Adoption of new AMD Products

Notwithstanding the silliness around how the MI355 racks are marketed, the points we are making on total cost of ownership and strong potential perf per TCO have clearly resonated with Hyperscalers and large AI Lab customers, and we see strong engagement and good order momentum with these customers.

AWS was a title sponsor for AMD’s Advancing AI event, and it will now be in its first serious push into purchasing and deploying AMD GPUs for rental at scale.

Meta, usually focused on inference use cases when it comes to AMD, is now starting to train on AMD as well. They are a key impetus behind the 72 GPU rack and will be in for the MI355X and the MI400. Meta’s PyTorch engineers are now even working on AMD Torch as well instead of only AMD’s engineers working on AMD torch.

For OpenAI, Sam Altman was on stage at the AMD event. OpenAI likes how much faster AMD is moving after our [first article benchmarking AMD and Nvidia](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/).

x.AI is going to be using these upcoming AMD systems for production inference, expanding AMD’s presence. In the past, only a small percentage of protection inference used AMD with most workloads run on Nvidia systems.

GCP are in talks with AMD, but they have been in discussions for quite a while. We think that AMD should cut GCP in on the same deal they are giving a few key Neoclouds – i.e. bootstrapping the AMD rental product by offering to lease back compute for AMD’s internal research and development needs.

Oracle, a clear trailblazer in terms of rapid deployment of Neocloud capacity, is also planning to deploy 30,000 MI355Xs.

Microsoft is the only hyperscaler that is staying on the sidelines, only ordering low volumes of the MI355, though it is leaning positively towards deploying the MI400.

Many of these hyperscalers have an abundance of air-cooled data center because of their legacy datacenter design architecture and are only too happy to adopt air cooled MI355X given the compelling perf/TCO proposition. Overall, we expect all of these hyperscalers to be deploying the MI355 and many will go on to also deploy the MI400 true rack scale solution as well.

## AMD’s Solving Its Neocloud Rental Market Weakness

One of the main challenges with increasing AMD adoption is that there are currently very few AMD focused Neoclouds compared to over a hundred Nvidia focused Neoclouds. This scarcity of supply and a lack of diversity in offerings in the rental market leads to artificially high prices for AMD GPU rentals, eroding AMD GPUs’ overall cost-competitiveness.

[In Q2 2025 so far, the current 1 month term contract market rental price for the H200 stands at about $2.50/hr/GPU](https://semianalysis.com/ai-cloud-tco-model/), with wide variance and lower pricing for low quality clouds. One-month contracts for renting the MI325X are non-existent. One-month contracts for renting the MI300X are priced at $2.50/hr, which makes the MI300X uncompetitive for renting compared to the H200. Below, we show what the approximate MI300 and MI325X 1-month rental price needs to be for the MI300X and MI325X in order for them to be competitive with renting Nvidia H200s. This analysis was based in large part upon [our real world inference benchmarks](https://semianalysis.com/2025/05/23/amd-vs-nvidia-inference-benchmark-who-wins-performance-cost-per-million-tokens/#what-rental-price-would-make-amd-gpus-competitive-with-nvidia-for-renters-of-compute-for-inference).

For reasoning inference tasks (1k input, 4k output), the MI300X needs to be priced at under $2.10-2.40/hr for a 1-month contract in order for it to have a competitive performance per dollar with H200. The MI325X needs to be priced between $2.75/hr/GPU to $3.00/hr/GPU, depending on interactivity, to be competitive. This a price range that no AMD Neocloud offers without extensive negotiations, which means that Nvidia currently wins on performance per dollar for rentals in part as a result of this market inefficiency.

![](https://substack-post-media.s3.amazonaws.com/public/images/4e4c7ac3-bb71-4442-bcb3-d175e0419346_1600x954.png)
*Source: SemiAnalysis*

## Pushing into High Gear – AMD is Accelerating the Development of the AMD Neocloud Ecosystem

Up until a few months ago, AMD was not very focused on driving stronger growth of their products within the Neocloud ecosystem and did not provide the enough incentives for GPU clouds to take the risk of hosting AMD GPUs and potentially not being be able to rent them out. In the past few months, AMD leadership has recognized that it is important to build up a healthy Neocloud ecosystem as this helps drive developer adoption up and helps drive down inflated AMD GPU rental prices. The end result is higher performance per dollar for the end user and more developers that are familiar with AMD and can contribute back to the broader AMD ecosystem.

To this end, AMD has given AWS, OCI, Digital Ocean, Vultr, Tensorwave, Crusoe and other Neoclouds an amazing incentive to support these Hyperscalers and Neocloud in AMD adoption and de-risk the business case. The deal AMD has struck is that in exchange for customers’ willingness to buy more AMD GPUs, AMD will rent back a significant chunk of this capacity in the form of long-term contracts for internal AMD software development purposes. This is akin to how Nvidia already rents back large clusters of GPUs from GCP, OCI, AWS, Azure, CoreWeave for Nvidia’s massive internal compute needs. For some Neoclouds, AMD is offering incentives to fully de-risk the investment case such that if the Neocloud isn't able to fully sell their capacity, AMD themselves will rent it from them as a backstop. We know of many Neocloud currently exploring potential partnerships with AMD being offered similar incentive structures.

With these incentives in place – one could make the argument that these Neoclouds could be building a less risky business case by working with AMD as compared to their peers that are renting Nvidia clusters only on a short term basis and taking considerable price and occupancy risk.

The launch of AMD’s developer cloud is also a key strategy towards making AMD’s compute universally available at a competitive price. As part of this launch, AMD has massively lowered its prices for renting MI300X GPUs, democratizing access to a broader demographic of developers. Unfortunately, at the time we tested it out, there default quota was set to zero GPUs and getting an increase to the GPU quota was difficult. We recommend to AMD that they set their default quota for new users to at least 16 MI300X GPUs in order to more effectively introduce developers into their ecosystem. Since AMD developer cloud on demand price is set at a much more reasonable price of 1.99$/hr/GPU price, we expect that AMD Neoclouds that offer on demand MI300 will likely need to cut their pricing today’s high levels of $3/hr/GPU down to $2/hr/GPU to match.

![](https://substack-post-media.s3.amazonaws.com/public/images/41cb9b83-52e0-4dc7-a77b-01950af62c75_1121x532.png)
*Source: SemiAnalysis, AMD*

## ROCm Software Improvements

AMD announced ROCm 7 with a focus on inference capabilities and performance. For inference throughput performance, AMD touted an average 3.5x improvement of ROCm 7 over ROCm 6, and a 1.3x improvement of ROCm7 over Nvidia B200 when serving DeepSeek R1. We look forward to verifying those claims.

AMD is also committed to working with the open ecosystem on distributed inference. In addition to supporting inference frameworks vLLM and SGLang, AMD supports the orchestration framework llm-d, an alternative to Nvidia Dynamo, to enable the distributed inference technique PD disaggregation. The llm-d stack is still missing quite a few features that would serve the same function as the Nvidia Dynamo KVCache manager. The KVCache manger is very important as it can offer a massive TCO benefit for inference workloads that can unlock a multiple times improvement in throughput for many inference workloads.

ROCm’s support of the kernel writing library Triton has also improved greatly in the past few versions. ROCm achieved functional support for Triton last year, and ROCm 7 focuses on performance improvement. We hope AMD continues the effort and expand support for advanced features such as FlexAttention.

Recently, ByteDance Seed created Triton Distributed, a Triton-based library that enables compute and GPU communication overlap. AMD has shown great interest in Triton Distributed and has talked about greater support for it. However, it is unclear whether OpenAI (maintainer of Triton) will accept contributions of ByteDance’s Triton Distributed features back to the original Triton library. It is possible that OpenAI is pursuing their own path on implementing distributed compute-comms kernels for Triton.

Furthermore, given significant chip export restrictions on China, it may be possible that ByteDance steps back from contributing towards open-source libraries for western GPUs. With that said, ByteDance is investing heavily in AMD and we expect to see them take meaningful AMD-based rental GPU capacity. ByteDance will remain predominantly in the Nvidia camp though as the lion’s share of their compute capacity expansion will come from renting Nvidia-based capacity. Most of ByteDance’s compute is from either Cloud rentals or large-scale dedicated bare metal clusters located outside of China, and most of their Neocloud and Cloud providers still mostly rely on Nvidia compute capacity.

At a lower level, AMD has claimed that they are integrating the popular data transfer interface Mooncake Transfer Engine and the expert parallel communication library DeepEP. However, as of writing this, we still haven’t seen any open source ROCm repo with DeepEP or Mooncake yet.

Finally, AMD announced its Developer Cloud and Developer Credits program. In addition to a simple interface for apply for compute access, AMD has created the Python package “rocm” for developers to easily install ROCm PyTorch, ROCm libraries such as HipBLAS, and development tools for these ROCm libraries. All code is open sourced in the GitHub repo [ROCm/TheRock](https://github.com/ROCm/TheRock).

## MI355X PyTorch Continuous Integration (CI) and Testing

AMD has begun work on adding CI and automated testing for MI355 chips to Pytorch. Note that none of the MI355X PRs have merged yet but it is great to see AMD thinking about open source PyTorch MI355X CI from Day 1. For Nvidia, it’s been six months since the mass delivery of Blackwell yet they have not commenced CI for open source PyTorch and have been focused only on internal Blackwell CI. In fact, Meta pays for most of the cost of the PyTorch CI, amounting to a spend of over $1 million a month, while AMD themselves pay for open source PyTorch CI on AMD. Though Nvidia has so far not donated meaningful funding or compute towards open source PyTorch CI, it does have plans in the works to contribute via donating lots of compute credits from DGX Cloud and donating GPU capacity rented from their various Neocloud providers to Meta open source PyTorch.

Nvidia is actively working on adding open source B200 PyTorch CI and has committed to donating 48 B200s to the PyTorch Foundation for the purposes of PyTorch CI. Although everyone would prefer having CI from day 0, adding Blackwell open source CI 6 months to PyTorch is better late than never. The spotlight we put on the lack of CI for AMD has likely nudged them into making significant strides here. Nvidia should continue to invest even more heavily in PyTorch CI for Blackwell. Additionally, their consumer GPUs need to be added to CI for PyTorch and popular inference libraries in order to ensure that consumer AI is stable. Currently, Nvidia consumer GPUs experience some instability when using certain frameworks due to lack of CI resources.

## ROCm MLPerf Training Submission

Last month, AMD submitted their first MLPerf Training run for single node Llama2 70B LoRA finetuning and BERT training. This is a very important development as it demonstrates that training can work on a single AMD node. As a next step, AMD should participate in even more real-world training benchmarks such as the MLPerf Llama 405B multi-node training benchmark. We think they can show competitive results for this test.

[When it comes to benchmarking, we like how AMD demonstrates clearly when their solutions are working well by presenting easy to follow reproducible instructions for their MLPerf runs](https://rocm.blogs.amd.com/artificial-intelligence/reproduce-mlperf-training-v5.0/README.html). This is in contrast to Nvidia’s MLPerf submissions which are very hard to reproduce.

![](https://substack-post-media.s3.amazonaws.com/public/images/f5e06951-94dd-4c69-ae96-77291ef76ca3_1708x956.png)
*Source: AMD*

## MIG Partitioning is Wasting Time and Engineering Resources

AMD currently is wasting lot of engineering resources and money on their pet project that aims to support GPU partitioning. This project would allow users to turn a single GPU into 8 smaller GPUs. No customers are asking for this. Meta, OpenAI, x.AI are all not asking for this because all online inferencing workloads require one GPU at a minimum. We think it is illogical that AMD hardware engineers have worked hard to develop one of the most advanced chips with a large amount of HBM per GPU only to want to split this GPU into 8 parts.

In fact, Meta, OpenAI, x.AI all want the opposite of this and want AMD to have better support for multi-node inferencing using at least 16 GPUs through the use of techniques such as DeepEP and disaggregated prefill.

![](https://substack-post-media.s3.amazonaws.com/public/images/5948c718-6a46-4252-b3d7-d39152fa5b7b_1236x698.jpeg)
*Source: AMD*

## MI355X Manufacturing – Updated Chiplet Architecture

![](https://substack-post-media.s3.amazonaws.com/public/images/1d1dd3c5-8be4-4b71-aa94-58727f99cf06_1748x1053.png)
*Source: SemiAnalysis*

AMD has used the two years since the MI300’s launch to refine their chiplet architecture. As can be seen from the silicon in the image above, the chip layout has been tweaked slightly, with the base Active Interposer Dies (AID) being merged from four quadrants into two reticle-sized halves. Minor adjustments to the positions of the HBM have shifted the structural support silicon dies from between the HBM sites into the corners.

The benefit is clear for cross-chiplet communications, eliminating an entire axis of 2.5D Infinity Fabric Advanced Package links, saving power and area from requiring fewer chip boundary crossings. It also eliminates the two-hop scenario where quadrants from opposite corners of MI300 had to make two jumps across dies to communicate with each other.

However, this arrangement also places extra importance on 3D stacking yields. AMD continues to use TSMC’s SoIC hybrid bonding process, which now needs to attach twice as many Accelerator Complex Dies (XCD) onto each base die, potentially compounding yield losses and additional silicon wastage should there be issues. AMD choosing this route speaks to the maturity of TSMC’s SoIC flow and their deep partnership with AMD’s Foundry Technology & Operations teams spanning over 5 years as the lead customer for SoIC.

![](https://substack-post-media.s3.amazonaws.com/public/images/7a4b9cc7-8f7b-40e1-be95-f778ea334af7_2560x1695.png)
*Source: AMD Advancing AI*

While still on TSMC N6, the base die has received several speed upgrades. The remaining die-to-die link has been upgraded from a 4.8TB/s bisection equivalent to a 5.5TB/s bisection equivalent on MI350. The Infinity Fabric’s speed for scale-up has been boosted by 20%. More importantly, the memory controllers can now handle faster HBM3E. AMD has stuck with the tried and true CoWoS-S for AID and HBM attach, noting that the footprint has remained the same as on MI300.

For the compute dies, the XCDs have seen a move from N5 to TSMC’s N3P node, with an updated CDNA4 architecture detailed below. This time, AMD has only enabled 32 of the 36 CUs printed on die, compared to 38 out of 40 on MI300. Interestingly, the orientation of the XCD on AID has changed, with the data bond pads landing in the central region of the AID. Data then proceeds outwards through the 256MB of Memory Attached Last Level (MALL) cache before ending up in HBM.

Overall, the new chip packs 185 Billion transistors, a 21% increase over MI300. We estimate about 23 Billion transistors go into each AID, with 17.4 Billion transistors in each XCD. That would mean a 30% transistor budget increase going from N5 to N3P.

## CDNA4 Microarchitecture (UArch)

AMD’s architecture design has gradually been shifting from a traditional HPC focus to one optimized for AI workloads. With CDNA 4, we see the residual influence of legacy HPC continuing to fade as AMD pivots even more into AI when it comes to architecture, though CDNA4 still wastes a lot of floor area on FP64 matrix core.

CDNA 4 comes with 256 compute units (CUs), 160 KB of local data share (LDS – SMEM equivalent), and matrix cores running at 4,096 FLOPs per cycle per CU for FP16. Compared to CDNA 3, this is a 16% reduction in the number of CUs, a 1.5x increase in LDS capacity, and a 2x increase in matrix core throughput. These changes are all signs of architecture converging towards AI workloads with larger array sizes. HPC workloads typically benefit from large numbers of CUs, whereas AI workloads benefit from each CU computing large matrices, and these two requirements compete for power and area budgets. The increase in LDS capacity shows matrix cores are so fast that AMD needs to increase their secondary buffer size to feed the cores data fast enough. Given that AMD increased LDS instead of the typical staging buffer VGPR (RMEM equivalent), we suspect the next-generation matrix core would require big architectural changes to continue scaling matrix core performance.

CDNA 4 offers 2x the throughput over FP16 for FP8 and 4x the throughput for FP4. Interestingly, CDNA 4’s FP6 throughput is theoretically identical to its FP4 throughput, since FP6 and FP4 share a data path. However, FP6 throughput will still be slightly lower than FP4 throughput due to power limitations in real-life settings. This is different from Nvidia Blackwell, where FP6 throughput is labeled the same as that of FP8.

However, compared to Nvidia’s Blackwell design, CDNA 4 has no asynchronous features, data transfer acceleration hardware (such as sm90/sm100 TMA), TMA multicasting or specialized memory (sm100 TMEM). This leads to worse picoJoules per unit of intelligence on CDNA4 versus Nvidia’s SM100. As of writing, we are still waiting for details on ISA to see the changes in MFMA operations to see if there is a WGMMA equivalent. That said, CDNA 4 also shows that those features are needed to further scale performance, so we expect to see drastic architectural changes in CDNA-NEXT.

## AMD Advancing AI Developer Session Track is Disappointing

AMD has made great improvements this year to their developer content on the [ROCM blog](https://rocm.blogs.amd.com/). We came to AMD Advancing AI hopeful that AMD would host many developer sessions across the stack but the set of talks and sessions left us underwhelmed. There were no talks on most of the AMD libraries from RCCL to Composable Kernels to rocSHMEM to aiter, etc. We hope that AMD will broaden the set of talks and seminars so as to allow developers to hone in more on their areas of interest in a more focused conference later on in the year.

![](https://substack-post-media.s3.amazonaws.com/public/images/570ad021-a55d-41cd-bfab-80a0ff1c3c92_1974x920.png)
*Source: SemiAnalysis, Nvidia, AMD*

## RCCL – ROCm Collective Communication Library

AMD has announced that their new 400G NIC will be Ultra Ethernet (UEC) ready and will also support the existing RoCEv2 protocol as well as the new Ultra Ethernet transport (UEC) protocol. In UEC mode, this NIC will be able to support packet spraying with out of order direct placement into the GPU memory without using a NIC reordering buffer unlike Bluefield-3. AMD’s new in house 400G NIC will allow them to more easily vertically integrate software and improve the out of the box experience rather than relying on Nvidia’s CX-7 NIC or Broadcom’s Thor-2 NIC. Oracle as well as AMD Neoclouds such as Tensorwave have committed to adopting AMD’s NIC, though Meta is holding back as its initial testing has not yet made them comfortable with adopting the AMD NIC, and it instead will be using the ConnectX-7 NIC for their MI355X clusters. Broadcom’s Thor 2 and Thor 3 NICs have faced challenges when it comes to market adopting due AMD and Nvidia’s strategy to vertically integrate NICs into their solutions. However, we do think there is a place for Broadcom’s NICs in various ASIC program.

AMD’s in house 400GbE NIC also supports a number of interesting features such as the ability to offload all-gather collectives for algorithms like RING and PAT. AMD claims that CPU proxy threads will also be offloaded to the NIC, but we are not sure whether this means they are using IBGDA or doing something else.

ROCm 7.0’s RCCL communication library has also been released, unfortunately it yet again appears to be just a carbon copy fork of Nvidia’s NCCL and as such it remains a key bottleneck holding back AMD’s multi node capabilities. As we recommended in our AMD 2.0 article, we still think that AMD needs to completely rewrite their communication library from scratch instead of relying on forking Nvidia’s software.

## New AMD Initiatives to Pay AI Engineers Market Rate

[It is well known within the industry that most AMD AI engineers have been compensated somewhat below market rates](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/). The only exceptions seem to be limited to a few new hires in recent months and engineers brought in through acquisitions. For example, most of the AI engineers that were bought in from NodAI, an acquisition from two years ago, are receiving significantly higher compensation than existing AMD engineers, even when equalizing for experience and skillset. Interestingly, AMD’s HR department already raised this issue a few quarters ago and recognized this pay disparity, raising it up the flag pole internally, but AMD management has yet to elevate this beyond a low priority issue. To this point, [following our public article explaining that AMD pays well below market for their AI engineers](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/#amd-management%e2%80%99s-blind-spot-%e2%80%93-amd-ai-software-engineer-compensation), AMD’s Head of HR  immediately elevated this matter to be a top priority are actively prioritizing a process to address these massive pay discrepancies – but implementation remains work in progress. Given that AMD has billions of dollars of cash on hand, we are hopeful AMD will do the right thing and pay a competitive total compensation to their top individual contributors that is also aligned with the success of AMD.

## MI400 Series Flexible Input Output (I/O)

AMD has learned from their mistake on the MI300X in deploying an Infinity Fabric that was much worse than NVLink. They have also recognized they don’t have the hardware talent to execute on an NVSwitch equivalent. Furthermore, they also do not want to encroach on the industry ecosystem by verticalizing too much. As such, they have gone with the shotgun approach of supporting everything under the sun.

Enter flexible I/O lanes. Instead of utilizing separate SerDes and I/O paths for each different type of I/O such as PCIe and Scale Up, AMD offers 144 lanes of I/O that can support many different standards. These I/O lanes can support PCIe 6.0, Infinity Fabric at 64G, UALink at 128G, xGMI 4 at 128G (which is somewhat of a superset of UALink), as well as Infinity Fabric over Ethernet at 212G. This approach allows the AMD silicon team to maximum flexibility for various different use cases.

With Flexible I/O, AMD can deploy scale up UALink or UALink over Ethernet. They can support SSDs directly attached to the GPU. They can attach NICs via UALink. The possibilities are almost endless. It is an incredibly large array of permutations for systems and allows for much change and evolution.

However, executing on the silicon engineering to allow these different forms of I/O is not easy. AMD must make SerDes and data paths that work with all of these different permutations. This is an incredibly hard engineering path fraught with engineering risk.

In the following sections, we will dive much deeper into the MI400 true rack-scale solution, discussing key scale-up architecture choices, explaining the full rack design with the help of elevation diagrams and board design illustrations. We will also provide a detailed bill of materials breakdown and a total cost of ownership and performance per TCO analysis.

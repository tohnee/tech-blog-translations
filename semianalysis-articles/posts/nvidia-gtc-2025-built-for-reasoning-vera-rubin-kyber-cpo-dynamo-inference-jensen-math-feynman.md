---
title: "NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, Jensen Math, Feynman"
subtitle: "Next Generation Nvidia Systems, Ground Up Inference Optimizations from Silicon to Systems to Software, The More You Buy The More You Make"
date: 2025-03-19
source: https://newsletter.semianalysis.com/p/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Daniel Nishball", "Ivan Chiam", "Patrick Zhou", "Doug", "Wega Chu"]
tags: ["Hardware Architecture", "Networking", "Accelerators"]
audience: only_paid
paywalled: true
---

# NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, Jensen Math, Feynman

**Next Generation Nvidia Systems, Ground Up Inference Optimizations from Silicon to Systems to Software, The More You Buy The More You Make**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

## **The Reasoning Token Explosion**

AI model progress has accelerated tremendously, and in the last six months, models have improved more than in the previous six months. This trend will continue because three scaling laws are stacked together and working in tandem: pre-training scaling, post-training scaling, and [inference time scaling](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/).

GTC this year is all about addressing the new scaling paradigms.

![](https://substack-post-media.s3.amazonaws.com/public/images/d108a7a2-436c-42e1-9763-b82291d624de_2219x1298.png)
*Source: Nvidia*

Claude 3.7 shows incredible performance for software engineering. Deepseek v3 shows cost for last generation model capabilities are plummeting in price driving further adoption. OpenAI’s o1 and o3 models showed that longer inference time and search mean much better answers. Like the early days of pre-training laws, there is no limit in sight for adding more compute for post-training these models. This year’s GTC is focused on enabling the explosion in intelligence and tokens. Nvidia is focusing on massive 35x improvements in inference cost to enable the training and deployment of models.

Last year’s mantra was “the more you buy, the more you save,” but this year’s slogan is **“the more you save, the more you buy.”** The inference efficiencies delivered in Nvidia’s roadmaps on the hardware and software side unlock reasoning and agents in the cost-effective deployment of models and other transformational enterprise applications, allowing widespread proliferation and deployment—a classic example of Jevons’ paradox at work. Or how Jensen says it: **“the more you buy, the more you make”.**

The market is worried about this. The concern is that DeepSeek-style software optimization and increasing Nvidia-driven hardware improvements are leading to *too much savings*, meaning that the demand for AI hardware decreases and the market will be in a token glut. Price does influence demand, and as the price of intelligence decreases, the frontier of intelligence capabilities continues to push on, and then demand increases. Today’s capabilities are constrained in cost due to inference cost. AI’s actual impact on our lives is still in its infancy. As costs drop, net consumption paradoxically increases.

The concern on token deflation is akin to discussing the fiber bubble's per-packet internet connectivity cost decreasing while ignoring the eventual impacts that websites and internet-driven applications would have on our lives, society, and economy. The key difference is that bandwidth demands are constrained, while demand for intelligence grows to infinity as capabilities improve drastically and costs fall.

Nvidia provides numbers supporting Jevons’ Paradox case. Models now take >100T tokens, and a reasoning model is 20x more tokens, and 150x more compute.

![](https://substack-post-media.s3.amazonaws.com/public/images/fb751d51-0085-45ec-8b11-c12fb6177fe3_871x602.png)
*Source: Nvidia*

Test-time computing takes hundreds of thousands of tokens/queries, and there are hundreds of millions of queries per month. Post-training scaling, which is where models go to school, takes trillions of tokens per model, with hundreds of thousands of post-trained models. Additionally agentic AI means that multiple models will work together to solve harder and harder problems.

## **Jensen Math Changes Every Year**

Every year, Jensen drops new math rules on the industry. Jensen Math is famously confusing and to add to the confusion this year, we now observe a third new Jensen math rule.

The first Jensen math rule is that Nvidia headline FLOPs are quoted with 2:4 sparsity (*which no one uses*) versus dense FLOPs, which is the real world performance metric – meaning the 989.4 TFLOPs of FP16 in for the H100 is quoted as 1979.81 TFLOPs.

The second Jensen math rule is that bandwidth should be quoted in bidirectional terms. NVLink5 is quoted as 1.8TB/s because it is 900GB/s of transmit plus 900GB/s of receive. These are added together for the spec sheet, but in the networking world, the standard is to quote the unidirectional bandwidth.

Now, a third Jensen math rule has emerged. GPU counts are counted in terms of GPU dies in a package rather than the number of packages. This nomenclature will be adopted from Rubin onwards. The first generation Vera Rubin racks will be called NVL144, even though the system architecture is similar to the GB200 NVL72 with the same Oberon rack and 72 GPU packages. This will be annoying for everyone to understand and a constant point of clarification, but alas we all merely live in Jensen's world.

Now, let’s go review the roadmap.

## GPU and System Roadmap

![](https://substack-post-media.s3.amazonaws.com/public/images/8103a7d6-b5e9-49cc-9e44-4b2a626617e7_1787x950.png)
*Source: Nvidia*

## Blackwell Ultra B300

![](https://substack-post-media.s3.amazonaws.com/public/images/3880684b-639a-4d70-9045-ae7ec3ed6cb8_1205x905.png)
*Source: Nvidia*

The Blackwell Ultra 300 has already been previewed, and nothing has changed from the details we shared last Christmas. Rehashing the primary specs: GB300 won’t be sold as a board but as a B300 GPU on a pocketable SXM module with the Grace CPU and also as a pocketable BGA. Performance-wise, B300 is over 50% higher-density FP4 FLOPs vs. the B200 equivalent. Memory capacity is upgraded to 288GB per package (8 stacks of 12-Hi HBM3E) but with the same bandwidth of 8 TB/s.

This was achieved by reducing many (but not all) FP64 ALUs and replacing them with FP4 and FP6 ALUs. Double-precision workloads are primarily for HPC and supercomputing workloads rather than AI workloads. While this is disappointing to the HPC community, Nvidia is being commercial and emphasizing AI, which is the more important market.

The B300 HGX version is now called B300 NVL16. This will use what was formerly called the “B300A” single GPU variant of Blackwell, now renamed the “B300.” This is half the dual-die B300, and there may be more communication overhead as there is no high-speed D2D interface linking the 2 GPU dies in a single package for a regular B300.

The B300 NVL16 will replace the B200 HGX form factor with 16 packages and GPU die on a baseboard. To achieve this, 2 of these single die packages are placed on a single SXM module (of which there are 8). It is unclear why Nvidia went down this route instead of sticking with 8 x dual die B300; we suspect the yield improvement from a much smaller CoWoS module and package substrate is a key motivator. Note that the packaging technology will be on CoWoS-L rather than CoWoS-S. This is an important decision. CoWoS-S’s maturity and capacity were the reasons for the single-die B300A. This transition suggests that CoWoS-L has rapidly matured, and yields have stabilized compared to its shaky start.

These 16 GPUs will communicate over the NVLink protocol, and, as with the B200 HGX, two NVSwitch 5.0 ASICs will be between the two banks of SXM modules.

Finally, one new detail is that, unlike previous generations of the HGX, the B300 NVL16 will not have Astera Labs' re-timers. However, some hyperscalers will choose to put in PCIe switches instead[. This is something we broke to Core Research subscribers earlier](https://semianalysis.com/core-research/core-weekly-insights-03-14-25/) this year.

Another important detail of B300 is that it will introduce the CX-8 NIC, which offers 4 lanes of 200G to achieve 800G total throughput for InfiniBand, a generation over generation doubling of networking speed from the current CX-7 NIC for Blackwell.

## Rubin Specifications

![](https://substack-post-media.s3.amazonaws.com/public/images/45efcb00-7ef4-4a21-a4c6-5d9fedb867b5_1158x653.png)
*Source: Nvidia*
![](https://substack-post-media.s3.amazonaws.com/public/images/199f62e9-7afd-4ab2-85ea-6e7185bf14e7_1570x814.png)
*Source: SemiAnalysis*

Rubin will have two reticle-size compute dies on TSMC 3nm. These compute dies will be flanked by two I/O tiles with all the SerDes for NVLink, PCIe, and the NVLink C2C IP, freeing up space on the main die for more computing.

Rubin will offer an incredible 50 PFLOPs of dense FP4 compute, more than tripling generation on generation vs B300. How can Rubin achieve this? Nvidia scales a few important vectors:

1. As above the I/O dies free up area, possibly 20-30% area that can be dedicated to more streaming multiprocessors and tensor cores.
2. Rubin will be fabricated using a 3nm process, the custom Nvidia 3NP or the standard N3P. Going from 3NP to 4NP from the Blackwell generation gives a large jump in density for logic, but there is nearly no shrink in SRAM.
3. In addition, Rubin will have a higher TDP—we estimate 1800W—which could even enable higher clock speeds.
4. Next is architecture scaling. Nvidia uses progressively larger systolic arrays for the tensor cores in each generation. We believe the systolic array went from 32x32 for Hopper to 64x64 for Blackwell. This could go larger to 128x128 for Rubin. Larger systolic arrays offer better data reuse and lower control complexity. They are generally more area and power efficient. It is more challenging to program them hence why Nvidia doesn’t go to the same size as Google does with the TPU at 256x256. It is also detrimental to fabrication yields. Nvidia has very high parametric yields for reticle-sized monolithic dies as there is built-in redundancy and repairability in their architecture featuring many smaller compute units. The defective compute units are disabled allowing for yield harvesting. This is unlike the TPU, which has fewer but very large tensor cores that do not have the same ability to repair defective logic units.

Rubin will again use the Oberon rack architecture as is used for the GB200/300 NVL72. It will be paired with the Vera CPU, the 3nm successor to Grace. Note that Vera will have fully custom core designed by Nvidia. Grace heavily relied on Neoverse V2 cores from Arm. Nvidia also has a custom fabric that enables individual CPU cores to access higher amounts of memory bandwidth if required, which AMD and Intel CPUs have significant challenges doing.

This is where the new nomenclature comes in. The new rack will be named **VR200 NVL144** despite having 72 GPU packages, with 144 compute dies (72 packages x 2 compute die per package). Nvidia is such a revolutionary company that they’re even changing how we count GPUs!

*The AMD marketing team should take note. AMD is leaving performance on the table by not claiming that the MI300X family can scale up to a 64 GPU world size (8 packages per system x 8 XCD chiplets per package), and this is a critical missed opportunity.*

*/sarcasm... Lisa, please don’t*

Nvidia’s HBM capacity will remain the same at 288GB generation on generation but is upgraded to HBM4: 8 stacks of 12-Hi with the same 24 GB layer density. The move to HBM4 affords a bandwidth increase, with 20.5TB/s of aggregate bandwidth, mostly from the bus width doubling to 2048 bits wide, with a pin speed of 6.4Gbps, the current cap in the JEDEC standard.

![](https://substack-post-media.s3.amazonaws.com/public/images/fc0619d4-02da-467c-8068-6d9cf758bca6_1826x1012.png)
*Source: SemiAnalysis*

It will feature NVLink 6th generation, with speed doubling to 3.6TB/s (bidirectional). This will come from doubling the lanes, with Nvidia sticking with 224G SerDes.

Back to Oberon, the backplane will be the same copper backplane, but we believe this is with a doubling of cables in proportion to the doubling of lanes per GPU.

On the NVSwitch side, the NVSwitch ASIC will also double aggregate bandwidth, again through doubling lanes.

## Rubin Ultra Specifications:

![](https://substack-post-media.s3.amazonaws.com/public/images/67439399-3abb-4014-8687-89bce3544b06_1205x650.png)
*Source: Nvidia*

Rubin Ultra is where performance really picks up. Nvidia will jump straight to 16 stacks of HBM in a package from 8. There will be a row of 4 reticle-sized GPUs flanked by 2 I/O chiplets. With double the compute area, compute doubles to 100 PFLOPs of dense FP4. HBM capacity goes to 1024GB, **more than 3.5x the capacity of vanilla Rubin**. There are double stacks, but density and layer count also increase. To get to 1TB of memory in a package, there will be 16 stacks of HBM4E with 16 layers of 32Gb DRAM core die.

We think this package will be split with two interposers on a substrate to avoid using one single very large interposer (almost 8x reticle). The 2 middle GPU dies will communicate with each other with a thin I/O die that has the D2D interface, and communication will happen through the substrate. This will require a very large ABF substrate that is beyond the current JEDEC package size limits (120mm for both width and height).

The system has 365TB total of Fast Memory comprising of 147TB of HBM and 218TB of LPDDR. Each Vera CPU has 1.5TB of LPDDR, and since there are 144 Vera CPUs, this would amount to a total of 218TB of LPDDR.

![](https://substack-post-media.s3.amazonaws.com/public/images/3bba797f-6780-425c-8cbc-f570bf73b012_1024x503.png)
*Source: SemiAnalysis*

This is also when we will see the introduction of the Kyber rack architecture.

## Kyber Rack Architecture

One of the key new features is the Kyber Rack Architecture. Nvidia is increasing densification by rotating racks 90 degrees for increased density. Given the NVL576 (144 GPU packages) configurations, this is another incredible increase in densification for larger scale-up world size.

![](https://substack-post-media.s3.amazonaws.com/public/images/c9a1db37-1166-422e-a85f-c21c17b7d9ca_1205x650.png)
*Source: Nvidia*

Let’s look at the key differences between the Oberon rack architecture and the Kyber rack architecture:

![](https://substack-post-media.s3.amazonaws.com/public/images/7cca1b3a-c211-4197-9be4-5f502eedee62_3452x1239.png)
*Source: SemiAnalysis*

- The compute trays are rotated 90 degrees into the blade form factor to achieve higher rack density.
- Each rack comprises four canisters, consisting of 18 compute blades each.

  - For NVL576, there are two Rubin Ultra GPU and two Vera CPU in each compute blade.
  - There will be a total of 36 R300 GPUs (144 dies) and 36 Vera CPUs per canister
  - This brings the total NVLink world size within the rack to 144 GPUs (576 dies)
- The PCB board backplane replaces the copper cable backplane as the scale-up link between the GPUs and the NVSwitches within the canister.

  - This shift is primarily due to the increased difficulties to fit the cables within the smaller footprint.
  - The NVSwitch blades at the back of the rack are connected to the compute blades via the backside of the PCB backplane.
  - It's still unclear how the NVSwitch blades in each canister will connect to link all four canisters into a single NVLink domain.

    - Some possible solutions being considered include DAC, ACC, and AEC.
- Some might wonder where the power supply, battery, and switches would be placed, since the compute blades occupy the entire rack.

  - In future datacenter hall layout, there will be a [standalone power rack](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/), standalone cooling rack, and a stand alone switch rack.
  - This is also one of the main reasons why Nvidia is announcing the roadmap for the Kyber rack architecture so early—to prepare the supply chain for upcoming changes in datacenter infrastructure at both the compute hall and rack levels.

![](https://substack-post-media.s3.amazonaws.com/public/images/e9b64962-1b35-4d53-ab0e-c47457d23bf9_1015x1024.png)
*Source: Nvidia*

Interestingly there are indications of a VR300 NVL1,152 (288 GPU packages) Kyber rack variation from the supply chain (if you count the wafer in the GTC keynotes presented above you will count 288 GPU packages highlighted in red). We believe this could be a potential SKU in development that will double the rack density as well as the NVLink world size from the NVL576 (144 GPU packages) showcased at GTC 2025 to the NVL1,152 (288 packages) in the future.

There will also be a new NVSwitch 7th gen, which is noteworthy. This is the first time a new NVSwitch has featured mid-platform. This allows for greater switch aggregated bandwidth and radix to scale up to 576 GPU dies (144 packages) in a single domain, though the topology may no longer be an all to all nonblocking rail optimized 1 tier multi-plane topology. Instead, it could be a multi-plane rail-optimized two-tier network topology with an oversubscription or even a-non clos topology.

The Kyber rack architecture is expected to launch for Rubin Ultra in 2027. The physical rack showed at the GTC show floor is a test vehicle based on blackwell, hence the architecture is still yet to be finalized.

## **Blackwell Ultra’s Improved Exponential Hardware Unit**

All varieties of attention, such as flash-attention, MLA, MQA, and GQA, all require **matrix multiplications** (matmuls) and **softmax functions** (row-wise reduction and element-wise exponential function). Matmuls are referred to as GEMM, or General Matrix multiplication, and apply only to the matrix multiplication aspect of neural network calculation.

In GPUs, GEMMs are performed on the tensor core. Tensor cores have been getting faster every generation but the performance of the multi-function unit (MUFU), which focuses on element-wise exponential calculations (softmax), has not improved as much each generation.

On bf16 (bfloat16) Hopper, calculating the softmax in the attention layer requires takes 50% of the cycles of the GEMMs. This requires overlapping by the kernel engineer to "hide" the latency of the softmax making it challenging to write kernels.

![](https://substack-post-media.s3.amazonaws.com/public/images/727c5b2d-6252-4f46-8fd6-3326e8edb01e_937x481.png)
*Source: Tri Dao @ CUDA Mode Hackathon 2024*

On FP8 (floating point) Hopper, calculating the softmax in the attention layer consume the exact same number of cycles as the GEMMs. This means if you don't do any overlapping at all, the attention layer will take **twice as long**. This is approximately 1536 cycles to calculate the matmul and then 1536 cycles to calculate the softmax. This is where overlapping improves throughput. Since the softmax and GEMMs take the same number of cycles, the kernel engineer needs to optimize a perfect overlapping kernel. The reality is it is impossible to do perfect overlapping and the hardware loses performance due to Amdahl’s law.

The challenge we have been describing so far has been described in the Hopper world of GPUs. This issue is also present in the first round of Blackwell. Nvidia solves this with Blackwell Ultra where they rework the SM and add instructions to improve this.

On Blackwell Ultra, the MUFU unit for calculating the softmax portion of the attention mechanism improves by 2.5x compared to standard Blackwell. This will alleviate the requirement for perfect overlapping to hide the computation of the softmax with the GEMM calculation. With this 2.5x speedup in the MUFU, the CUDA developer has more tolerance for overlapping without losing the performance of their attention kernel.

![](https://substack-post-media.s3.amazonaws.com/public/images/8007bb0a-e3f8-4466-a08f-4bd200360e54_1414x757.png)
*Source: Tri Dao @ CUDA Mode Hackathon 2024*

This is where Nvidia’s new inference stack and Dynamo come to the rescue.

## Inference Stack and Dynamo

In last year’s GTC, Nvidia discussed how the GB200 NVL72’s larger 72-GPU scale-up world size allowed it to deliver a 15x increase in inference throughput vs an H200 at FP8.

![](https://substack-post-media.s3.amazonaws.com/public/images/bdc9823f-a477-419f-aef2-cd2e0ebdc8d3_975x634.png)
*Source: Nvidia*

Nvidia hasn’t slowed the pace. It is accelerating inference throughput gains—this time on multiple fronts—with new announcements in both hardware and software domains.

Blackwell Ultra GB300 NVL72 delivers 50% greater FP4 dense PFLOPs vs the GB200 NVL72, as well as a 50% bump in HBM capacity – both of which will increase inference throughput. The roadmap includes multiple upgrades to networking speeds in the Rubin generation that will also deliver meaningful improvements in inference throughput.

The next leap in inference throughput from hardware will come with the scale-up network world size expanding to 576 GPU dies in Rubin Ultra – up from 144 GPU dies in Rubin. And that’s just the hardware improvements.

In the software world, Nvidia is announcing Nvidia Dynamo – an open AI engine stack that is focused making it easier to deploy and scale inference. It has the potential to disrupt VLLM and SGLang – delivering multiple features that VLLM doesn’t have and at higher performance. Together with the hardware level innovations, Dynamo will offer yet another shift in the throughput vs interactivity curve to the right – particularly improving throughput for higher interactivity use cases.

![](https://substack-post-media.s3.amazonaws.com/public/images/017e9808-a454-459c-bcbe-07be396b07f0_2309x1332.png)
*Source: Nvidia*

Dynamo brings several key features that are new to the current inference stack:

- **Smart Router**
- **GPU Planner**
- **Improved NCCL Collective for Inference**
- **NIXL – NVIDIA Inference Transfer Engine**
- **NVMe KV-Cache Offload Manager**

## Smart Router

The Smart Routerintelligently routes each token in a multi-GPU inference deployment to both prefill and decode GPUs. For Prefill – this means ensuring that incoming tokens are equally distributed to the different GPUs serving prefill so as to avoid bottlenecks on any given experts in the prefill phase.

Similarly – in the decode phase – it is important to ensure sequence lengths and requests are well distributed and balanced across GPUs serving decode. Some experts that are more heavily trafficked can be replicated as well by the GPU Planner to help keep the load balanced.

The router also load balances across each replica serving the model which is something vLLM and many other inference engines do not support.

![](https://substack-post-media.s3.amazonaws.com/public/images/c03590d3-5ca8-458b-b33a-fd3ce3101b47_1149x686.png)
*Source: Nvidia*

## GPU Planner

The GPU Planneris an autoscaler of both prefill and decode nodes, spinning up additional nodes with fluctuations in demand that are natural over the course of the day. It can implement a degree of load balancing among many experts in an MoE model in both prefill and decode nodes. The GPU planner spins up additional GPUs to provide additional compute to high-load experts. It can also dynamically reallocate nodes between prefill and decode nodes as needed, further maximizing resource utilization.

This additionally supports changing the ratio of GPUs used for decoding and for prefill – this is especially useful for cases like Deep Research, where more prefill is required as opposed to decoding, as these applications need to review a huge amount of context but only generate a comparatively small amount.

![](https://substack-post-media.s3.amazonaws.com/public/images/f9f0fec7-e131-4ff1-9938-0a7d427429c8_1170x633.png)
*Source: Nvidia*

## **Improved NCCL Collective for Inference**

The low-latency communications library is a set of new algorithms within the Nvidia Collective Communications Library (NCCL) that can deliver 4x lower latency for smaller message sizes – resulting in considerable improvements in inference throughput overall.

[Sylvain’s talk at GTC this year](https://register.nvidia.com/flow/nvidia/gtcs25/ap/page/catalog/session/1727457129604001QT6N) elaborated much more on these additions – outlining the one-shot and two-shot all-reduce algorithms that allow for this improvement.

Since AMD’s RCCL library is a carbon copy fork of NVIDIA’s NCCL, Sylvain’s NCCL refactor will continue expanding the CUDA moat and causes AMD’s RCCL to lose thousands of engineering hours to sync Nvidia’s major refactor into RCCL. While AMD spends thousands of engineering hours to sync Nvidia’s changes, Nvidia will use that time instead to continue advancing the frontier of collective communications software stack & algorithms.

![](https://substack-post-media.s3.amazonaws.com/public/images/12365f8e-7215-40cc-a6f3-380296b095d5_1024x608.png)
*Source: Nvidia*

## NIXL - NVIDIA Inference Transfer Engine

To transfer from prefill nodes to decoding nodes, low latency high bandwidth communication transfer libraries is needed. NIXL will be using InfiniBand GPU-Async Initialized (IBGDA). Currently in NCCL, the control flow goes through CPU proxy threads while the dataflow goes directly to the NIC without needing to go through the CPU buffering. But with IBGDA, both control flow & dataflow doesn’t need to go through the CPU and goes directly from the GPU to the NIC.

NIXL will also abstract away the complexity of sending and receiving data movements between CXL, local NVMe, remote NVMe, CPU memory, remote GPU memory and GPUs.

![](https://substack-post-media.s3.amazonaws.com/public/images/9b7b0130-da82-4d6c-b321-a69cdcc0e1da_1151x654.png)
*Source: Nvidia*

## **NVMe KVCache Offload Manager**

The KV-Cache Offload Manager allows more efficient overall execution of prefill overall by saving the KVCache from prior user conversations in NVMe storage rather than discarding it.

![](https://substack-post-media.s3.amazonaws.com/public/images/c596bc00-30ba-492a-a72f-4bcb3f303527_1024x633.png)
*Source: Nvidia*

When a user engages in an ongoing multi response conversation with an LLM, the LLM needs to factor in the prior questions and responses earlier in the conversation, taking these as input tokens as well. In the naïve implementation, the inference system will have discarded the KV Cache originally used for generating those earlier questions and responses, meaning that the KV Cache will have to be computed again, repeating the same set of calculations.

Instead, with NVMe KVCache offload, when a user steps away, the KVCache can be offloaded to an NVMe storage system until the user returns to the conversation. When the user asks a subsequent question in the conversation, the KVCache can be quickly retrieved from the NVMe storage system, obviating the need to calculate the KVCache again.

This frees up capacity on the prefill nodes to handle more incoming volume, or alternative could reduce the size of the prefill deployment needed. The user will also have a much better experience with faster time to first token as there is now much less time needed to retrieve the KV Cache vs computing it.

![](https://substack-post-media.s3.amazonaws.com/public/images/fb906f51-e5ce-496b-bcf1-5021bd5ca4b7_1014x683.png)
*Source: Nvidia*

In [DeepSeek’s Day 6 GitHub note](https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md), researchers disclosed a 56.3% KV Cache hit rate for the on-disk KV Cache, implying considerable efficiency gains for their prefill deployments. We understand that a typical KV Cache hit rate could range from 50-60% on this type of deployment when users have multi-turn conversations. There is a cost to deploying this NVMe storage solution such that there is a crossover point where the conversation is short enough where it is easier and cheaper to simply recompute rather than to reload, but savings are massive otherwise.

Anyone who has been tracking [DeepSeek’s Open Source Week](https://github.com/deepseek-ai/open-infra-index/tree/main?tab=readme-ov-file) will be intimately familiar with all of the above techniques. The above like is arguably the best place to learn more about them quickly while Nvidia spins up more documentation on Dynamo.

The result of all of these features is a very impressive speedup for inference across the board. Nvidia has even discussed improvements when Dynamo is deployed on existing H100 nodes. Essentially – Dynamo democratizes DeepSeek innovations and allows everyone in the community to access the best that open-source model technology has to offer. This allows everyone and not just the top AI Labs with a deep inference deployment engineering bench to deploy highly efficient inference systems.

Lastly – because Dynamo handles disaggregated inference and expert parallelism broadly, it particularly helps on individual replication and higher interactivity deployments. Of course – having many nodes is a prerequisite for Dynamo to fully leverage its capabilities and deliver meaningful improvements.

![](https://substack-post-media.s3.amazonaws.com/public/images/7e5bb716-01fe-431b-b07a-7371d0e52836_1165x790.png)
*SourceL Nvidia*

## **AI Total Cost of Ownership – Cost Decline**s

Soon after finishing his discussion on Blackwell, Jensen drove the point home by discussing how these innovations have made him the “Chief revenue destroyer”. He further illustrated this by highlighting that Blackwell had an up to 68x performance gain over Hopper, resulting in an 87% decline in costs. Rubin is slated to drive even more performance gains – 900x that of Hopper, for a 99.97% reduction in cost.

Clearly, Nvidia is pursuing a relentless pace of improvement – as Jensen puts it: “When Blackwells start shipping in volume, you couldn’t even give Hoppers away”

![](https://substack-post-media.s3.amazonaws.com/public/images/72c74dfc-0aed-4e1a-9150-0c5602f147c1_2132x1427.png)
*Source: Nvidia*

We have been preaching a similar same message for some time – highlighting the importance of deploying compute early in the product cycle rather than later. In our [AI Neocloud Playbook](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/) published in October last year, we explained how this exact dynamic was a driver of an acceleration in H100 rental price drops that accelerated from Mid 2024. For quite some time we have been urging the ecosystem to prioritize deployment of next-gen systems such as the B200 and the GB200 NVL72 over acquiring H100s or H200s.

Our clients that have subscribed to our [AI Cloud Total Cost of Ownership (TCO) Model](https://semianalysis.com/ai-cloud-tco-model/) are already familiar with the jumps in productivity that we expect from generation to generation, and how this will drive the AI Neocloud rental pricing for these chips, and ultimately the net present value that the chips’ owners can earn.

Indeed, our H100 rental price forecasting framework operates exactly off the point Jensen was illustrating. We combine our estimates of future install base, cluster total cost of ownership as well as future chip capabilities to build a forecast pricing curve. So far, the framework has been instructive. We first published our H100 rental price forecast model in April 2024 to clients – the model has predicted H100 rental pricing with 98% accuracy from early 2024 to today.

![](https://substack-post-media.s3.amazonaws.com/public/images/3faa18c2-f8e2-48f2-8c79-69dcf399cfb2_1724x1128.png)
*Source: AI TCO Model*

## **CPO Insertion**

![](https://substack-post-media.s3.amazonaws.com/public/images/3e0e97a0-6cc1-4e6e-8756-64c32d8bb0a1_1231x701.png)
*Source: Nvidia*

In the keynote speech, Nvidia announced its first co-packaged optics (CPO) solution to be deployed in their scale-out switches. With CPO, transceivers are now replaced by external laser sources (ELSs) that together with Optical Engines (OEs) placed directly adjacent to the chip silicon facilitate data communication. Instead of plugging into transceiver ports, fiber optic cables now plug into ports on the switch that route the signal directly to the optical engines.

![](https://substack-post-media.s3.amazonaws.com/public/images/cfefa490-05cc-4e87-8d33-a47f9816f675_1267x659.png)
*Source: Nvidia*

The primary advantage of CPO is significantly reduced power consumption for a few reasons. On the switch itself, there are meaningful savings because there is no longer any need for a Digital Signal Processor (DSP) and also because lower power laser light sources can be used. This savings can be obtained using Linear Pluggable Optic (LPO) transceivers as well, but CPO also allows a much larger switch radix, allowing the network to flatten one layer – allowing a cluster to have a two-layer network through the use of CPO rather than a three-layer network with the use of DSP transceivers. This means eliminating an entire layer and set of switches and enjoying the benefit of the associated cost and power savings as well – which turns out to be nearly as significant as the savings from transceivers on the power dimension.

Our analysis shows that for a 400k* GB200 NVL72 deployment, moving to CPO-based two-layer network from a DSP-transceiver based three-layer network can yield up to 12% total cluster power savings – reducing transceiver power from 10% of compute resources to only 1% of compute resources.

![](https://substack-post-media.s3.amazonaws.com/public/images/d28da705-0950-4c9c-9e89-c809514fa1c8_888x571.png)
*Source: SemiAnalysis*

Nvidia launched a number of CPO-based switches today including a CPO version of the Quantum X-800 3400, which itself [debuted a year ago at GTC 2024](https://semianalysis.com/2024/03/25/nvidias-optical-boogeyman-nvl72-infiniband/). It features 144 ports at 800G, for a total throughput of 115T, and will include 144 MPO ports and 18 ELS. This switch will be rolled out in second half of 2025. The Spectrum-X switch featuring 512 ports of 800G is also of interest as it can allow very high radix at high speeds – allowing very fast and flat network topologies. This Ethernet CPO switch will be rolled out in the second half of 2026.

![](https://substack-post-media.s3.amazonaws.com/public/images/8de9ed6b-33a7-418c-bc99-8ee7e39a023d_948x592.png)
*Source: Nvidia*

As ground-breaking as today’s release is, we still think Nvidia is only warming up in the field of CPO. We think that in the long run, CPO’s largest contribution by far will be if it is deployed in scale-up networks, where it has the potential to massively increase a GPU’s scale-up network radix and aggregate bandwidth – allowing much faster and flatter scale-up networks, and opening the door to scale-up world sizes of well beyond 576 GPUs. We will be diving much deeper into Nvidia’s CPO solutions in an article coming soon.

## **Nvidia Is Still King and Is Coming for Your Cost of Compute**

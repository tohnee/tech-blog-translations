---
title: "Cerebras Wafer Scale Hardware Crushes High Performance Computing Workloads Including Machine Learning And Beyond"
date: 2021-06-30
source: https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Cerebras Wafer Scale Hardware Crushes High Performance Computing Workloads Including Machine Learning And Beyond

Cerebras Systems and their wafer scale hardware have generated industry fan fare due to their completely unconventional approach. Rather than building a big chip dedicated to machine learning like all the other players in AI, they targeted a completely different avenue of scaling. They pursued the strategy of making the entire wafer a single chip. This hardware has shown to be surprisingly versatile and is even creating groundbreaking gains in other high performance computing applications.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1428c59f-8fde-4da7-90f3-d05ffe76cef0_1024x593.png)

This was driven by a simple observation that Moore’s law has slowed significantly. The only avenue to get huge increases in transistors count is by increasing the amount of silicon in each chip. Cerebras is on their second-generation product with the Cerebras WSE-2. This chip is has dimensions of 215mm x 215mm.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/66e754f8-ad1d-43b2-928f-c06b6d1b63b3_1024x636.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d6613d1b-cf9e-43bd-943f-0e135f2a9282_1023x294.png)

Compared to the Nvidia A100, the largest GPU available, Cerebras achieves huge advantages, especially when comparing the on chip 40GB of memory bandwidth to the A100’s similarly sized HBM memory. Cerebras has an incredibly high fabric bandwidth that far outpaces the GPU to GPU interconnects as well.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/851c0b2f-a5f4-4026-9578-a2c8a9fde8c6_1024x549.png)

Cerebras tames their 20KW beast by offering it in a water-cooled chassis. For reference, an Nvidia A100 ranges from 250W to 500W depending on the configuration. A lot of special care had to be placed into creating this cooling solution. Issues such as differential thermal expansion of silicon and other components became a major issue due to the size and power consumption of this chip.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3766cb24-1d73-46cb-b07d-6e88907ebdcf_1024x539.png)

Semiconductor manufacturing has limited die size has been limited by the reticle limit for a long time. The reticle limit is 33x26 meaning that this is the largest size a lithography immersion stepper from ASML can pattern on a wafer. Nvidia’s largest chips are in the low 800mm^2 range mostly because going beyond this is impossible.

The Cerebras WSE is actually many chips on a wafer within the confines of the reticle limit. Instead of cutting the chips apart along the scribe lines between chips, they developed a method for cross die wires. These wires are patterned separately from the actual chips and allow the chips to connect to each other. In effect, the chip can scale beyond the reticle limits.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c90a83a9-5758-495e-8377-fa9a486b375f_1024x517.png)

When building chips in a classical way, there are often defects. As such, a number of chips from each wafer must be thrown away or elements of a chip must be disabled. Nvidia commonly uses this practice with their GPUs. There has been an ongoing trend of disabling a larger percentage of cores with each new generation and with their current generation Ampere, roughly 12% of cores are disabled.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/38bbd1ca-da9e-45b7-8eb7-35f8890a1b94_1024x664.jpeg)

Cerebras deals with this by adding 2 additional rows of cores across each reticle sub-chip. The interconnect within these chips is a 2D mesh where each core is connected in the vertical and horizontal directions. They also have additional interconnects for each of the diagonal cores as well. This allows defective cores to be routed around and software to still recognize a 2D mesh.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9b8f1846-ab65-46a6-80f1-c44a00b2c045_1024x565.png)

Within this 2D mesh, Cerebras targets a few goals. They wanted all memory to remain on chip rather than having to wait for slow off chip memory. The only external connection is to the host system. Each core has fine grained parallelism and shares nothing between each other. They are power efficient and general-purpose cores capable of MIMD and have their own local memory.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/df8d3e51-a7fc-4369-8caf-ad90105a17d9_1023x583.png)

The primary use case is for machine learning training or inference. Layers of networks are mapped to regions of the wafer sized chip. Each rectangular block corresponds to a layer and is interestingly called a “Colorado.” Convolutions, matrix vectors, and matrix multiplications are computed on cores within each layer. The 2D mesh handles inter core communications within each layer of the network and in between layers of the network.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fab326be-bd7f-45ef-89a7-a1615bb84ee0_1024x652.png)

Most communications are generally in either X or Y along the chip, but some communications need to cross huge portions of the chip. The mesh can handle this without getting congested. This allows layers within a network to not have to be contiguous or directly next to each other. Cerebras software stack places and routes these layers while maintain high utilization rates of cores and fabric. The software is capable of placing only a few layers of a network on a single chip or placing multiple copies of the entire network across the chip for data parallelism.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e9167829-3b7c-4e8d-98df-079d56eb98d5_1024x716.png)

Cerebras has customers with live production wafer scale engines. These are used in many different workloads, but one of the most interesting is CANDLE. The WSE is used for precise simulations of drug response for combinations of drugs and their effects on cancer. The most promising results from simulations are then selected for experimental investigation.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9e47b569-ba94-40de-9712-3741c9758f84_1024x573.png)

Another current use case running on these chips is for internal confinement fusion. This runs on a large supercomputer that also contains multiple interconnected Cerebras WSEs. One of the components in this massive simulation involves interactions between atoms and sub-atomic particles. This computation is replaced with a large pre-trained neural network that runs on Cerebras hardware. This is a use case where only inference is used. It is evoked at every time step of the simulation. Data is streamed from the larger supercomputer to the Cerebras WSEs which in turn provide the output for these atomic and sub-atomic interactions.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d733d6de-23f0-422c-94f8-fdad4035bb8a_1024x551.png)

Cerebras hardware is used beyond just machine learning too. The Joule supercomputer runs computational fluid dynamics on conventional hardware running in a 3D mesh. They have run into a scaling problem in two different ways. They could not scale up performance with core counts due limitations in network bandwidth. Furthermore, the cores were often leaving a lot of performance on the table due to cache misses and therefore going out to memory. This memory then ran into huge bandwidth bottlenecks.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8d9ba5e0-2848-4434-8ef1-2c4054a47bb6_1024x628.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c5b79f8f-3095-4210-ac96-b68bd15dda86_1024x435.png)

The 3D mesh of the fluid dynamics model was mapped to the 2D mesh of the WSE chip. Neighbor exchange, vector AXPY, and dot products of global vectors which entails local dot products and a global all-reduce. All these operations can be handled with ease due to the large amount of SRAM and relatively high complexity of each individual core.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/28106272-7049-4e2f-b2b4-c8cacda92ad4_1024x537.png)

There is a large amount of inter-core communications, but the internal network on chip is robust enough to handle them with low latency. The network does this by sending messages along virtual channels called “colors” rather than to pre-determined addresses. This hardware-based communications allows data to travel 1 hop per clock across the entire chip.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c1e610e6-48a4-4b80-9395-88370e6cb75b_1024x476.png)

Allreduce can be done incredibly fast. Each core sends its scalar to the core next to it. When it arrives there, the scalars are added together and sent forward. The edges of the chips are sending data east/west towards the center. Once it arrives in the center, the same process occurs but north/south. The results are coalesced and then broadcasted back over the mesh of cores. In just 1 microsecond, this allreduce can be completed. For reference, a typical cluster in a supercomputer takes about this long for a single MPI communication from 1 processor to another neighboring processor.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b3c7b639-77de-40ed-9096-d23912b9b904_1024x641.png)

Computations can be done to achieve full bandwidth regardless of delays to bringing data in. The router has 4 incoming sets of data from each adjacent core. In addition, the core can reroute its output back in so that it does not need to be store it in SRAM. The core can run multiple threads at once. There is a main thread that is given priority, but if it is waiting on data, the other threads will progress. By maintaining data locality with large amounts of SRAM and a multithreaded architecture, utilization rates are kept extremely high.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d13bb7eb-94ce-4b4e-b75e-205265f51906_1024x383.png)

The results of the low-level optimizations to the hardware resulted in a 200x speed increase in computational fluid dynamics. This is in comparison to a large supercomputer cluster which was also highly optimized. In addition to the speed up, cost and especially power had tremendous advantages. This advantage is somewhat obvious as a supercomputer cluster is being compared to a single, albeit wafer sized, chip.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/db43aa60-fbc0-49b2-a20d-73cf4213f259_1024x574.png)

Unfortunately, software is not completely up to snuff yet. A beta SDK will come later this year for writing custom kernel operations. This language would be completely domain specific to the WSE. They will have libraries for mathematical functions and communications which should hopefully lift the burden somewhat. Beyond this, there are some features and tools that will help, but it will be a high skill programmers’ task. This is the only hardware that can achieve this scale of computing, so it may not be a massive barrier to entry for those tasks that require this level of performance.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9115acd6-cc52-4628-a9fa-43ee6937e28b_1024x580.png)

Cerebras is pitching real time computational fluid dynamics as the next workload to take advantage of WSEs. There is considerable promise that this will open a completely new use case.

We are excited for the 7nm based WSE2 to roll out fully. It will be exciting to see if the SDK can allow developers to generate other workloads where the WSEs can bring orders of magnitude performance increases. AI is an area where Cerebras is being aggressive and turning heads, but wafer scale computing could change this industry far outside of just machine learning.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

[Share](https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Leave a comment](https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes/comments)

*This article was originally published on [SemiAnalysis](https://semianalysis.com/cerebras-wafer-scale-hardware-crushes-high-performance-computing-workloads-including-machine-learning-and-beyond/) on June 30th 2021.*

*Clients and employees of SemiAnalysis may hold positions in companies referenced in this article*.

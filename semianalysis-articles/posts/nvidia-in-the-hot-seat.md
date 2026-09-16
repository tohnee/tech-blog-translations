---
title: "Nvidia In The Hot Seat?"
subtitle: "Intel Habana, Graphcore, Google TPU, and Nvidia A100 Compared In AI Training"
date: 2022-06-29
source: https://newsletter.semianalysis.com/p/nvidia-in-the-hot-seat
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Nvidia In The Hot Seat?

**Intel Habana, Graphcore, Google TPU, and Nvidia A100 Compared In AI Training**

Nvidia has been king of AI training workloads due to their flexible, easy to program, powerful hardware. This may be changing as AI is very dynamic and various different AI workloads are bifurcating. Training isn’t a monolithic entity, and therefore the hardware and software solution best suited for your workload may not be the same as that of another workload. Combined with the rapid pace of model evolution, some AI training hardware is starting to find a niche.

Today we are going to dissect the a few of the major players that submit their performance to MLPerf 2.0 as well where this hardware can find a niche. We will also be discussing some of the evolutions coming to machine learning models.

Before diving into the submissions, we wanted to point a few things out. This chart from ML Commons shows the peak performance for any system with 8 processors/accelerators and their performance in a few leading models. This is then compared to the colloquial definition of “Moore’s Law” IE doubling every 2 years.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e7d6b78f-20bc-4b0c-ab06-a70b1afce1b6_1023x581.png)

These results tell a very important detail. While the node shrinks and changes in architecture matter across time, the single most important factor in AI is software. There is as high as an 8x performance increase in 3.5 years depending on the model. Companies like Nvidia, Graphcore, Google, and Habana have only gone through 1 hardware iteration and 1 process node shrink during this time period.

Most of the gains can be attributed to software, not hardware. The types of algorithms running on top each vendors software stack that enables scaling is the most important factor. Software is the great differentiator, but as models for different tasks diverge more, this leaves niches for other vendors to be optimized for a few workloads, or at least that’s what many of these accelerator companies are suggesting.

MLPerf is a benchmark suite of 8 models which was developed by the non-profit consortium known as [MLCommons](https://mlcommons.org/en/). These benchmarks can be run by 1 processor all the way across to thousands. While there are some valid criticisms of it, it is by far the best publicly available method for comparing AI hardware and software for performance. Let’s start by looking at some of the results and breaking them down.

# **Intel Habana Gaudi2**

Habana is interesting as their first-generation chip was not the most impressive showing. Their software stack was not mature last year when it finally became available via AWS. They recently announced their 2nd generation Gaudi AI Training chip which brings performance much more inline with the industry, or at least so they claim. Habana submitted benchmarks for 2 of the 8 models.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f6010b5d-309b-4104-835d-9f37d7ec3890_1022x328.png)

Here Habana wins by a decent margin in the tiny ResNet-50 model, but by a very small margin in the small BERT natural language processing model. We would like to see much larger models and a larger variety from Habana, but this is a strong showing.

In terms of economics, both Nvidia’s A100 and Intel’s Habana Gaudi2 have a reticle limit TSMC 7nm die with 6 stacks of HBM (Nvidia disables 1 for yield). As such, the comparison is quite apples to apples. Gaudi2 is 600W vs Nvidia’s 400W, but it doesn’t require extra Infiniband NICs and NVSwitch to connect GPUs together in 1 server or between multiple servers. This saves a lot of power and silicon cost. It’s noteworthy that Habana beat Graphcore in ResNet 50 by single digits, and BERT by double digits. Very impressive showing.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ad1ba96f-0d8e-4f9b-8424-896c61bca137_1024x518.png)

Habana also submitted more benchmarks for their previous generation Gaudi1 chip. These scale to higher chip counts than prior submissions. The performance itself isn’t noteworthy, but it is good to see that their chip can scale up to more accelerators easily as that was their whole promise of integrating ethernet directly into the AI chip.

While Habana didn’t submit many different model types, they did want to emphasize one point that was very interesting regarding optimizations.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e8c96f1c-6faa-4ac7-8d72-417edcb4eb7a_1023x393.png)

Habana says they make a conscious effort to use out of the box software with minimal optimization for their submissions to MLPerf. They demonstrate this point by comparing to Nvidia’s GPUs with out the box software. These numbers as well as settings can only be found on Intel’s website rather than inside the MLPerf submissions. The point is to not compare to a hyper optimized MLPerf submission that Nvidia and their partners make. It is certainly an interesting take. We would lend it more credibility if this could be proven true on a wide array of models.

# **Google TPU**

Google is in an interesting position as they are on their 4th iteration of AI hardware architecture. Arguably, Nvidia is only approaching their 3rd architecture for the task as the Volta GPU was the first to include AI specific Tensor cores, with Ampere the current generation, and the next generation Hopper sampling now with volume shipments late this year.

Their chips are also pretty much only available internally, and they have always been designed with that in mind. Google being one of the foremost companies in AI must deal with scaling to huge model sizes. As such their submissions also centered around massive systems with thousands of accelerators. We have edited the MLPerf spreadsheet to be a bit easier to glance at.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6586e761-5234-413a-8b5e-bff526bdfc15_1024x323.png)

It is interesting that Google generally uses a 2:1 ration of TPUs to CPUs although there are some systems with a 4:1 ratio. Nvidia on the other hand generally uses a 4:1 or 8:1 ratio. The performance here trades blows. TPU so far has had very little success in the cloud service provider realm, but Google uses tens of thousands of them in their own datacenters for internal inference and training workloads. It will be interesting to see if Google can get the broader market to pick up usage of TPUs through Google Cloud.

# **Graphcore Bow**

Graphcore, much like Intel’s Habana, only submitted results for 2 model types in the closed division. They submitted across many more different system sizes from 16 to 256 accelerators. These systems come with the newly released [Bow IPU which is the industry’s first wafer on wafer hybrid bonded processor](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w).

The Bow chip is identical in architecture to the previous generation save for the use of wafer on wafer bonding to [increase clocks by ~40% without increasing power consumption](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w). A byproduct of this also means that the software is identical to the prior generation. Software improvements have carried Graphcore a long way since they were initially a [complete failure](https://semianalysis.com/graphcore-looks-like-a-complete-failure-in-machine-learning-training-performance/) in the MLPerf benchmarks. The results are now much better and they actually do deliver better performance than Nvidia in the two models Graphcore showed off.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/785e8ad4-3b74-4942-af7c-af91f26d4af1_1024x580.png)

On the software front, another very interesting detail was that Baidu was able to run the IPU’s using their own PaddlePaddle framework rather than using the Graphcore specific one. PaddlePaddle is an open-sourced training framework focused on distributed training. It is very popular in China, so this could be a big positive for Graphcore’s potential sales in China.

Graphcore also spent some time talking to us about the current path of machine learning models and how that is going to hit major roadblocks. They believe new model architecture approaches are necessary and they argued these would run better on their novel IPU architecture.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/52485f6c-3d06-4b78-8bf7-3b53ae0914ff_1023x574.png)

The other side of the coin is that currently models are rapidly evolving towards being larger and larger transformer models. These models excel in accuracy and time to train provided you can throw enough compute and data at them. Through implementing conditional and dynamic routing can match or beat any other model architecture at a larger variety of tasks which makes them very generalizable. We explored this idea in [this article where we talked through Tenstorrent’s](https://semianalysis.substack.com/p/tenstorrent-blackhole-grendel-and?s=w) hardware architecture, software, roadmap, and Google’s Pathways model.

# **Nvidia A100**

Nvidia’s is not sitting down slouching versus the competition. All the MLPerf results include the 2 year old A100, but the H100 GPU is already sampling and shipping later this year. Nvidia was very proud of the fact that they were the only vendor to submit to all 8 benchmarks for MLPerf. In addition, they had multiple system integrator and server vendor partners submitting systems that included their GPUs. Nvidia in total racked up wins in 4/8 tests. The 2 year old A100 GPU is fastest in 6/8 tests on a per chip basis. The competitors simply didn’t show up to compete in most of the tests, which likely means they tested it internally but decided not to submit the final score/code.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c1119b32-3b21-4777-a875-fa83fb9fb5ce_1023x580.png)

Nvidia has shifted their tone somewhat on AI Training. They used to claim supremacy everywhere, but now they only have supremacy in most ways. This in of itself is not a big deal because the real factor isn’t matrix multiplies per dollar.

The important metric for training is TCO. Nvidia continues to dominate here in multiple ways.

First their GPUs are more flexible. Even if they are not the best in small image recognition networks relative to others, they have the most flexible hardware which can adapt to a wide range of workloads. The machine learning space is evolving rapidly and so flexible hardware is needed for large training clusters. AI in the real world is rarely just 1 model alone. It is multiple models feeding into each other. On the other hand, if it is 1 massive model, it is a transformer which almost seems to have grown to be most efficiently run on GPUs anyways.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dd4cc879-02e1-40e2-b9f4-2a615fa9eb72_1024x282.png)

With multiple different model types from speech recognition to vision to recommendation models all working in tandem, having an accelerator that is best suited for just 1 model type is a sure fire way to bad TCO. In a datacenter, one of the most important metrics is utilization rates. Nvidia is the only company whose hardware can be used for data preparation, training, and inference. Many of these other companies are focusing on training and inference, or training alone.

Lastly, having good software is a critical piece of the puzzle. The majority of cost is developing that model and software, not running it.

> AI doesn't simply require simplistic calculations per dollar where you're just looking at the cost of a single server AI. Deploying AI requires very valuable data science, ML engineers and application developers who represent the bulk of the cost of AI infrastructure.
>
> Shar Narasimhan, Nvidia

That software stack is incredibly important as it represents the majority of a company’s costs for all but the largest operators. Having developers be able to easily tweak models, deploy, test, and iterate is critical to reducing the development costs.

The combo of software flexibility, development cost, and higher utilization rates leads to Nvidia still holding the TCO crown. Apologies for Betteridge's law of headlines to the title of this post, but it got you to click and read it didn’t it!

[Share](https://newsletter.semianalysis.com/p/nvidia-in-the-hot-seat?utm_source=substack&utm_medium=email&utm_content=share&action=share)

There are increasingly becoming players who have such scale that utilization rates will be high and the flexibility is not as important. These players are developing their own silicon in many cases, or working with a 2nd player. The question is whether any of these 2nd players capture enough to be viable over the long term. In our opinion, there will be a world where hyperscalers such as Google, Amazon, Microsoft, Facebook, Alibaba, Tencent, and Baidu attempt to develop their own hardware, and Nvidia fights to stay ahead and fights to keep cloud customers wanting Nvidia hardware.

Established companies like Intel and AMD may have a shot, but it will take multiple generations to break Nvidia’s monopoly. The inference side is where we expect many different architectures and startups to succeed. We think Graphcore has the potential to strike it out as successful, but it will be a tough road, and their next generation of hardware has to be great in addition to their software continuing to get better.

[Leave a comment](https://newsletter.semianalysis.com/p/nvidia-in-the-hot-seat/comments)

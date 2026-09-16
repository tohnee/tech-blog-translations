---
title: "MI300X vs H100 vs H200 Benchmark Part 1: Training - CUDA Moat Still Alive"
subtitle: "Training Performance, User Experience, Usability, Nvidia, AMD, GEMM, Attention, Networking, InfiniBand, Spectrum-X Ethernet, RoCEv2 Ethernet, SHARP, Total Cost of Ownership"
date: 2024-12-22
source: https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Reyk Knuhtsen"]
tags: ["Accelerators", "LLMs", "Benchmarks"]
audience: only_paid
paywalled: true
---

# MI300X vs H100 vs H200 Benchmark Part 1: Training - CUDA Moat Still Alive

**Training Performance, User Experience, Usability, Nvidia, AMD, GEMM, Attention, Networking, InfiniBand, Spectrum-X Ethernet, RoCEv2 Ethernet, SHARP, Total Cost of Ownership**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

## Intro

SemiAnalysis has been on a five-month long quest to settle the reality of MI300X. In theory, the MI300X should be at a huge advantage over Nvidia’s H100 and H200 in terms of specifications and Total Cost of Ownership (TCO). However, the reality is that the on paper specs as given below are not representative of performance that can be expected in a real-world environment. If AMD could deliver the below marketed performance with this memory, it would be a very strong competitor in the market.

![](https://substack-post-media.s3.amazonaws.com/public/images/76cfa222-48b8-4151-9fa9-254179b08aa6_2184x1088.jpeg)
*Source: SemiAnalysis, Nvidia, AMD*

Today we are going to talk through our five-month journey conducting independent analysis and training-focused benchmarking of the MI300X, the H100 and the H200, engaging with both NVIDIA and AMD. We will do a detailed overview of the numerous low-level benchmarks that we ran, see the table of contents for summary. Furthermore, we will compare the total cost of ownership of Nvidia and AMD GPUs and factor in performance. Ultimately much of what we are doing is openly giving a comprehensive public recommendation to AMD on what they need to do to be competitive and fix their software issues after five months of submitting and squashing bugs. It’s not just that it’s immature software, they need to change how they do development.

In short, when comparing Nvidia’s GPUs to AMD’s MI300X, we found that the potential on paper advantage of the MI300X was not realized due to a lack within AMD public release software stack and the lack of testing from AMD.

AMD’s software experience is riddled with bugs rendering out of the box training with AMD is impossible. We were hopeful that AMD could emerge as a strong competitor to NVIDIA in training workloads, but, as of today, this is unfortunately not the case. The CUDA moat has yet to be crossed by AMD due to AMD’s weaker-than-expected software Quality Assurance (QA) culture and its challenging out of the box experience. **As fast as AMD tries to fill in the CUDA moat, NVIDIA engineers are working overtime to deepen said moat with new features, libraries, and performance updates.**

We shared benchmark source code and intermediate test results for GEMM benchmark and Single Node Training with both Nvidia and AMD and held calls and discussions to solicit feedback and implement improvements to the benchmarks, and we worked with AMD to implement bug fixes for the software stacks.

Our goal with this highly iterative interaction was to ensure that our tests are an unbiased evaluation of what real-world users would experience.

We initially planned to publish this article a few months ago but wanted to take the extra time to engage with the AMD team and explore possible fixes or development work. We spent a considerable time identifying and fixing AMD software bugs so that we could give AMD every chance to show MI300X unhindered by AMD software stack bugs as opposed to only showing problematic performance out of the box. To give a fair impression, we also explain the considerable amount of work on tuning and bug-squashing that it took to get there. We think this approach provides users with the best possible level of transparency.

**We wanted to contribute in any way we could to try to improve the AMD ecosystem.** **Though** **AMD software is much better now due to our bug reports and tire-kicking, its public software stack still falls short**. We have open-sourced many of the benchmarks and created simple one-liner commands to reproduce them.

If Lisa Su and the AMD Leadership redouble their investment with a focus on their software and testing stack, they have a chance to be competitive with Nvidia on training. We think the engineers at AMD are extremely capable and are doing their best to advance the AMD ecosystem – and indeed support from these engineers in the form of bug fixes, configuration help and custom images improved the results we were able to get from the MI300X.

To bring our benchmarking process to a coda, on November 15th, 2024 we sent Nvidia and AMD a draft of most of our major GEMM and single node benchmarking code and results for comments, verification, and fine-tuning. We asked that any final comments, fixes, feedback and any performance improvements be submitted by November 25th. We set this time frame to crystallize test results to allow time to write an in-depth analysis and commentary and carry out multiple rounds of internal and external reviews, all steps that can take a variable and often unknowable amount of time, typically from 2-4 weeks.

A few days ago, after we informed both that we had confirmed an article publication date of December 20th, AMD requested that we delay publication to include results based on a beta WIP development build on an AMD developer’s branch. All of our benchmarking on Nvidia was conducted on publicly available stable release builds. In the spirit of transparency and fairness, we include these results as well as updated testing harness results on as the original November 25th deadline image and the latest publicly available software. However, we believe that the correct way to interpret the results is to look at the performance of the public stable release of AMD/Nvidia software.

**Below are the list of software builds that we have used for benchmarking:**

- H100 Public Stable Release – Out of Box experience for Nvidia H100.
- H200 Public Stable Release – Out of Box experience for Nvidia H200.
- MI300X Nov 25th Custom Build – This is a custom VIP docker image hand-crafted that builds all dependencies from source code written by AMD principal engineers.
- MI300X Stable Public Release PyTorch 2.5.1 – Out of Box experience for AMD MI300X.
- MI300X Public Nightly Dec 19th– This can indicate where AMD performance can be by January 2025, when PyTorch 2.6 is released, over 1 year after launch.
- MI300X Dec 21st WIP dev build – This is the image that AMD submitted to us after we agreed to delay publication of the article. It is an experimental development build that has not yet been merged into AMD’s internal main branch, and it does not use the native PyTorch flash attention API. Performance with this image can indicate where AMD public stable release performance will be in 1-2 quarters from now.

We are very thankful for the technical support provided by AMD and Nvidia throughout this process, but we maintain our independence in the results we publish. We want to shout out to and thank our AMD counterparties, Anush Elangovan (AMD VP of AI), Hui Liu and many dozens of amazing AMD Principal/Senior engineers, AMD VPs of Engineering, AMD Engineering Fellows, AMD CVPs of Engineering and AMD Directors of Engineering, AMD Software Library Leads, for triaging and fixing our various bug reports. On the Nvidia side, we are grateful to Kedar Potdar, Ian Buck, Sylvain Jeaugey and the NCCL team from NVIDIA for their amazing support.

Thank you to [Crusoe](https://crusoe.ai/cloud), [TensorWave](https://tensorwave.com/) (*AMD Ventures Portco*), [Nebius](https://nebius.com/), [Lambda](https://lambdalabs.com/), [Hot Aisle](https://hotaisle.xyz/) and [Sustainable Metal Cloud (SMC)](https://smc.co/) / [Firmus](https://firmus.co/) for the compute and for being supporters of open-source benchmarking. Crusoe, Nebius, SMC / Firmus and Lambda support managed SLURM and shared home directories out of the box. TensorWave currently has managed SLURM in beta and this feature will come to general availability (GA) at the start of next year. Sustainable Metal Cloud is one of the few neoclouds that has [official MLPerf GPT-3 175B Training results](https://mlcommons.org/benchmarks/training/).

**We will be releasing a follow up article on inferencing for the H100, H200 and MI300X. We may also release a follow-up article in a few months to follow up on AMD training performance to see if out of box experience has improved and test other models such as LlaVa & Mamba.**

![](https://substack-post-media.s3.amazonaws.com/public/images/fd9ce744-8e42-4b9a-9120-22ff0192a3f9_2354x1244.png)
*Source: SemiAnalysis*

## Key Findings

1. Comparing on paper FLOP/s and HBM Bandwidth/Capacity is akin to comparing cameras by merely examining megapixel count. The only way to tell the actual performance is to run benchmarking.
2. Nvidia’s Out of the Box Performance & Experience is amazing, and we did not run into any Nvidia specific bugs during our benchmarks. Nvidia tasked a single engineer to us for technical support, but we didn’t run into any Nvidia software bugs as such we didn’t need much support.
3. AMD’s Out of the Box Experience is very difficult to work with and can require considerable patience and elbow grease to move towards a usable state. **On most of our benchmarks, Public AMD stable releases of AMD PyTorch is still broken and we needed workarounds**.
4. If we weren’t supported by multiple teams of AMD engineers triaging and fixing bugs in AMD software that we ran into, AMD’s results would have been much lower than Nvidia’s.
5. We ran unofficial MLPerf Training GPT-3 175B on 256 H100 in collaboration with Sustainable Metal Cloud to test the effects of different VBoost setting
6. For AMD, Real World Performance on public stable released software is nowhere close to its on paper marketed TFLOP/s. Nvidia’s real world performance also undershoots its marketing TFLOP/s, but not by nearly as much.
7. The MI300X has a lower total cost of ownership (TCO) compared to the H100/H200, but training performance per TCO is worse on the MI300X on public stable releases of AMD software. This changes if one uses custom development builds of AMD software.
8. Training performance is weaker, as demonstrated by the MI300X ‘s matrix multiplication micro-benchmarks, and AMD public release software on single-node training throughput still lags that of Nvidia’s H100 and H200.
9. **MI300X performance is held back by AMD software**. **AMD MI300X software on BF16 development branches have better performance** but has not yet merged into the main branch of AMD’s internal repos. By the time it gets merged into the main branch and into the PyTorch stable release, Nvidia Blackwell will have already been available to everyone.
10. AMD’s training performance is also held back as the MI300X does not deliver strong scale out performance. This is due to its weaker ROCm Compute Communication Library (RCCL) and AMD’s lower degree of vertical integration with networking and switching hardware compared to Nvidia’s strong integration of its Nvidia Collective Communications Library (NCCL), InfiniBand/Spectrum-X network fabric and switches.
11. Many of AMD AI Libraries are forks of NVIDIA AI Libraries, leading to suboptimal outcomes and compatibility issues.
12. AMD customers tend to use hand crafted kernels only for inference, which means their performance outside of very narrow well defined use cases is poor, and their flexibility to rapidly shifting workloads is non-existent.

## Executive Recommendation to AMD

**We genuinely want to see another effective competitor to Nvidia and want to help AMD get to that spot**, but, unfortunately, there is still much work to be done on that front. At the bottom of this article, we have a detailed list of feedback for the Lisa Su and the AMD Leadership Team, but provide a summary here:

1. Give AMD Engineers more compute and engineering resources to fix and improve the AMD ecosystem, they have very few internal gpu boxes relative to what Nvidia provides to their engineers. Tensorwave, the largest AMD GPU Cloud has given GPU time for free to a team at AMD to fix software issues, which is insane given they paid for the GPUs.
2. AMD needs to hook up thousands more of MI300X, MI325X to PyTorch CI/CD for automated testing to ensure there is no AMD performance regressions & functional AMD bugs. Pytorch/AWS currently has hundreds of of NIVIDIA GPUs for PyTorch CI/CD to ensure an amazing out of box experience
3. The AMD Executive Team should personally and intensively internally test (i.e., “dogfood”) products that are being shipped to the public rather than focus on testing internal builds. Preferably dogfood during livestream (twitch.tv) to show the authentic out of box experience. This is like how geohotz livestreams
4. AMD should collaborate with Meta to get production LLM training workloads working as soon as possible on PyTorch ROCm, AMD’s answer to CUDA, as commonly, PyTorch code paths that Meta isn’t using have numerous bugs.
5. Move away from over-reliance on properly setting numerous environment flags (up to dozens) to make an AMD deployment usable. Instead, bake these settings into the default configuration. Make the out of the box experience usable!
6. Focus on making out of box experience good instead of over-reliance on custom VIP images that build all dependencies from source code main@specificcommit and take 5 hours to build.
7. Stop expecting end users to use PYTORCH_TUNABLE_OPS which is a prototype buggy feature and is not respectful of the end users time as it takes ~1 hour for the end user to tune every time an end user wants to make any changes to their code.
8. AMD should submit MLPerf Training GPT-3 175B results. MLPerf is an apples-to-apples benchmarking methodology that uses time to convergence as the north star.
9. We want AMD to be competitive and are open to meet with more detailed feedback on how to fix the AMD Datacenter GPU Ecosystem for the better.

## A Summary of the AMD vs Nvidia Narrative

Before we dive into various facets of AMD’s software stack that hold AMD back, we will discuss the MI300X’s basic specifications, its comparative total cost of ownership, and how most analysts and investors have evaluated its competitiveness.

The MI300X launched in late 2023 with an exciting set of on paper specifications—featuring 1,307 TFLOP/s of FP16 compute (stronger than the H100’s 989 TFLOP/s), 5.3 TB/s of memory bandwidth, and 192GB of HBM3, 3.35 TB/s of memory bandwidth, and 80GB of HBM3. These specs outstrip those of the H200, which itself is, effectively, a memory-spec bumped version of the H100, delivering 4.8TB/s of memory bandwidth and 141GB of HBM3e.

![](https://substack-post-media.s3.amazonaws.com/public/images/c456bf40-8aa2-4d89-b666-8d062323d41e_2184x1088.jpeg)
*Source: SemiAnalysis, Nvidia, AMD*

On paper total cost of ownership for an MI300X deployment is extremely compelling, not only due to the lower ASP of the MI300X, but also because it is typically deployed using cheaper Ethernet networking. Comparing a cluster of 16k H200s vs a 16k MI300X ethernet cluster leads to nearly 40% of the cost savings coming from networking alone, with the remainder of the savings from a lower accelerator cost. The use of Whitebox Ethernet switches is a substantial cost savings compared to using Nvidia’s Quantum-2 switches, but the real difference is cheaper transceivers, as Nvidia branded transceivers cost as much as 2-3x over what a typical transceiver OEM charges.

At face value, the MI300X seems the best of both worlds: higher performance and lower total cost of ownership. At the time of its launch, it was logical to expect share gains to the underdog AMD from this compelling combination. The table below shows total upfront cluster capex – we present a more detailed breakdown of cluster capex components as well as a detailed networking BoM analysis in the sections at near the bottom of the article.

![](https://substack-post-media.s3.amazonaws.com/public/images/08a6d76b-c20b-4def-b349-448abaf02e2f_1819x619.jpeg)
*Source: SemiAnalysis AI TCO Model*

As orders solidified, excitement built up for potential of the MI300X, helped along by bullish commentary and guidance from AMD. With a compelling spec advantage, it was easy to argue for further upside to AMD’s guidance, which most investors assumed management was sandbagging. AMD had a strong hand, in theory. After all they have mid-single digit market share in datacenter GPUs for 2024 and, logically, a glide path towards even 10-12% market share by 2027 could be conservative while offering considerable earnings upside for AMD.

However, over from late 2023 and through most of 2024, guidance for full year 2024 datacenter GPU sales repeatedly underperformed those lofty expectations. From its 1Q24 earnings through its 3Q24 earnings, AMD only raised guidance from $4B to $5B, well under the $6-8B investor bogey based on [CoWoS and HBM supply agreements](https://www.semianalysis.com/p/accelerator-model). Our demand view in the [Accelerator Model](https://semianalysis.com/accelerator-industry-model/) tracked [Microsoft’s disappointment early in the year and lack of follow on orders](https://semianalysis.com/accelerator-industry-model/).

The earlier bullish line of reasoning was like purchasing a certain car model from a magazine without a test drive or soliciting feedback from owners of that model or reading any reviews. But fear not – SemiAnalysis has put the MI300X, H100, and H200 through their paces at scale and can show why AMD’s current software stack issues decisively disprove this line of reasoning.

## General Matrix Multiply (GEMM) Performance

Most FLOPS in a transformer-based architecture (i.e. ChatGPT, Llama, etc.) go towards matrix multiplication, also known as GEMMs. For this reason, **GEMM performance is a good proxy for how well frontier transformers, such as ChatGPT, Llama, Claude, Grok, etc. will train on the hardware**.

GEMMs take two input matrices, Matrix A and Matrix B, with Matrix A having the shape of (M, K), M rows and K columns, and Matrix B having the shape of (K,N) to produce an output matrix of shape (M,N).

![](https://substack-post-media.s3.amazonaws.com/public/images/20b7820c-407a-4ce5-9311-33e1d9b41533_1499x1404.png)
*Source: Nvidia*

Conceptually, each element of the resulting matrix is a sum of element-wise multiplications along the "K" dimension of the inputs. For this matter, the K dimension is also known as the reduction dimension.

![](https://substack-post-media.s3.amazonaws.com/public/images/096e0e89-9404-49dd-88c2-18a86a0cf06b_1875x684.png)
*Source: SemiAnalysis*

Below, we have tested the following real-world shapes, given in the form (M,N,K)—which is short for multiplying a matrix of dimensions (M,K) and (K,N) together.

These following matrix shapes were actually used in [Meta’s Llama 70B](https://github.com/pytorch-labs/float8_experimental/blob/fe6e08c867abf56b1acd0f34473c69cde624f0a3/benchmarks/bench_matmul.py#L57) production training:

- (16384, 8192, 1280) - Fused QKV Projection GEMM shape
- (16384, 1024, 8192) - Attention Output Projection shape
- (16384, 8192, 7168) - FFN GEMM shape
- (16384, 3584, 8192) - FFN GEMM shape
- (8192, 8192, 8192) - Standard GEMM shape for benchmarking

We used OpenAI’s do_bench function for the benchmark setup, an industry standard method of benchmarking PyTorch. The do_bench function provides cache clearing between runs as a default and provides ways to warmup and execute the benchmark multiple times, taking the median result as the given accuracy.  We used warmup=30 and rep=200 for these tests. Both input tensor A and B were randomly initialized with a normal distribution with mean 0 and variance 1. This is because a normal distribution comes the closest to matching the actual distribution of weights and activations in modern neural networks. The distribution of the input tensors will affect the results of the TFLOP/s performance benchmark. We will discuss the reasons why the input distribution effects TFLOP/s performance later in the article.

For BF16, we can see that the H100 and H200 achieves roughly 720 TFLOP/s against their marketed 989.5 TFLOP/s, while the MI300X reaches a mere ~620 TFLOP/s compared with their marketed 1,307 TFLOP/s.

This means that, despite a much higher marketed BF16 TFLOP/s, the MI300X is 14% slower than the H100 and H200. This AMD result used a custom docker image that was hand crafted by an AMD principal engineer yet still achieved slower performance than Nvidia’s GPUs. For our out of the box testing of the MI300X, the TFLOP/s throughput even slower than this! In addition to a custom image, AMD also requires the user to set numerous environment flags that aren’t set by default to reach these performance results.

![](https://substack-post-media.s3.amazonaws.com/public/images/709f1dbd-d014-4737-b865-fdb53edf252d_1489x1084.png)
*Source: SemiAnalysis*

Unfortunately, the story is worse for FP8. The H100/H200 achieves ~1,280 TFLOP/s out of the marketed 1979 TFLOP/s. The MI300X, in comparison, only reaches ~990 TFLOP/s. Thus, for FP8, the MI300X is 22% slower than H100. This is for both inputs being of the e4m3 FP8 ([i.e. 4 exponent bits and 3 mantissa bits](https://semianalysis.com/2024/01/11/neural-network-quantization-and-number/)) datatype.

![](https://substack-post-media.s3.amazonaws.com/public/images/fc5d7c11-6a1f-458d-9e3e-dd6e1624363e_1514x1152.png)
*Source: SemiAnalysis*

It is important to note that calling GEMM is a simple task, and we shouldn’t expect to run into AMD software bugs. Unfortunately, a **major bug** that we encountered is that the torch.matmul and F.Linear APIs have been delivering different performances on AMD for a couple of months during the summer. One would expect the torch.matmul and F.Linear APIs to have the same performance, but, surprisingly, F.Linear is much slower!

This is a strange bug as torch.matmul and F.Linear are both wrappers around the hardware vendor GEMM libraries, so they should achieve the same level of performance. F.Linear, in particular, is important, as this is the way most end users in PyTorch launch the GEMM kernels.

When we started testing AMD five months ago, the public AMD PyTorch still had this bug. The root cause was that AMD in fact has two different underlying GEMM libraries, rocBLAS and hipBLASLt, with HipBLASLt being more optimized for the MI300X. The bug was that torch.matmul uses the optimized hipBLASLt, but AMD had not changed F.Linear by default, leaving it to use the unoptimized rocBLAS library.

This major bug was ultimately fixed by AMD a few months ago after our bug reports, and we hope it doesn’t reappear due to a lack of proper regression testing. AMD’s usability could improve considerably if it boosted its testing efforts instead of waiting for users to discover these critical issues.

We have open sourced the GEMM benchmark used in our tests into a simple three liner that anyone can easily run:

![](https://substack-post-media.s3.amazonaws.com/public/images/cfc95cc8-cb39-4a7f-9717-ef5406c97b0b_821x571.png)
*Source: SemiAnalysis*

## Popular GEMM Benchmark Isn't Accurate

Recently, a benchmark has been floating around the internet that claims that, on GEMMs, AMD MI300X’s performance is close to that of the H100.

![](https://substack-post-media.s3.amazonaws.com/public/images/2a5ff26d-c895-43ee-b940-a7ef197c4ca7_1024x548.png)
*Source: Github*

There are two main issues with the benchmark: it isn’t properly carrying out L2 Cache clearing and also is simply taking the max performance, instead of the median/mean TFLOP/s over the course of the iterations for a specific shape. Without L2 Cache clearing between iterations, the benchmark does not accurately reflect real-world GEMM performance. Furthermore, since the TFLOP/s change based on which iteration it is on, you need to use a mean/median over at least 100 iterations as the basis for an accurate GEMM benchmark. OpenAI’s do_bench provides L2 cache and mean/median out of the box by default, so we recommend that engineers use it for micro-benchmarking. Below, we have simplified the benchmark into pseudocode and have commented on the issues mentioned above.

![](https://substack-post-media.s3.amazonaws.com/public/images/a9127f13-583a-4b0a-8037-a96876eeed4f_1470x880.png)
*Source: SemiAnalysis*

## HBM Memory Bandwidth Performance

It is widely known that AMD MI300X has better memory bandwidth than the Nvidia H100 and H200, offering 5.3 TB/s of bandwidth vs 4.8 TB/s for the H200 and 3.35 TB/s for the H100. Improved HBM memory bandwidth is very useful in inferencing and is sometimes useful in training. In training, users can set a larger batch size if they have more HBM memory capacity and memory bandwidth. Although if a larger global batch size is used, after a certain size, the model will take longer to convergence. It is easy to run fast with big global batch size but at a high level, it will hurt time to convergence.

From our HBM memory bandwidth benchmarking, we see that that MI300X indeed has way better memory bandwidth than both the H200 and the H100. We tested memory bandwidth in Pytorch with Tensor.copy_ & used the industry standard OpenAI do_bench to ensure accuracy.

**As you will see in our upcoming H100 vs H200 vs MI300X inference article, memory bandwidth is very important for inferencing.**

![](https://substack-post-media.s3.amazonaws.com/public/images/05fdf265-ecae-494e-bbd2-24b191d24768_1600x1114.png)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/8d1eef68-22bd-442f-810b-d039aee70a63_829x665.png)
*Source: SemiAnalysis*

## AMD Hand-Crafted VIP Custom Builds and WIP Development Builds

The only reason we have been able to get AMD performance within 75% of H100/H200 performance is because we have been supported by multiple teams at AMD in fixing numerous AMD software bugs. To get AMD to a usable state with somewhat reasonable performance, a giant ~60 command Dockerfile that builds dependencies from source, hand crafted by an AMD principal engineer, was specifically provided for us, since the Pytorch Nightly and public PyTorch AMD images functioned poorly and had version differences. This docker image requires ~5 hours to build from source and installs dependencies and sub-dependencies (hipBLASLt, Triton, PyTorch, TransformerEngine), a huge difference compared to Nvidia, which offers a pre-built, out of the box experience and takes but a single line of code. **Most users do not build Pytorch, hipBLASLt from source code but instead use the stable release.**

When using public PyTorch, users have the choice of working with the latest stable images or a nightly PyTorch upload. **So, although a nightly PyTorch upload may have the latest commits that could potentially lead to better performance or could fix some bugs, but users must accept that the upload may not be fully tested and could contain new bugs** from Meta/AMD/Nvidia or other PyTorch contributors that have not been discovered yet. **Note that most end users are using the stable release of PyTorch.**

![](https://substack-post-media.s3.amazonaws.com/public/images/26876a7b-8446-4e9f-b543-510bdc8d1921_3680x7420.png)
*Source: SemiAnalysis, AMD*
![](https://substack-post-media.s3.amazonaws.com/public/images/6da81937-1fa0-40fa-854d-fb8c74e815c6_1024x453.png)
*Source: Nvidia*

Delightfully, Nvidia’s Docker images contain the complete set of developer tools needed for profiling and debugging, like Nsight Compute and Nsight Systems. AMD, in contrast, does not include their OmniTrace developer tool out of the box.

Until a couple weeks ago, the AMD docker images only supported PyTorch 2.3, which released 8 months ago. Mainline PyTorch 2.4 and PyTorch 2.5 have also since released and PyTorch 2.6 is about to come out in Q1 2025. We recommended to an AMD Principal Engineer and to AMD’s VP of AI that AMD should have the latest AMD PyTorch version – AMD has since started publishing containers for some of these AMD PyTorch versions. Docker image for AMD PyTorch 2.5 is still missing.

![](https://substack-post-media.s3.amazonaws.com/public/images/09f56f85-cc14-47e0-9232-28e145214702_2057x1098.png)
*Source: Nvidia*

## Dec 21st AMD Development Builds

Below is AMD’s December 21st development build docker image. As you can see, it uses a number of non stable devlopment branches for dependencies such as hipBLASLt, AOTriton, ROCm Attention and installs everything including PyTorch from source code, taking upwards of 5 hours to build. These versions of the dependencies haven’t even been merged into AMD’s own main branch yet.  **99.9% of users will not be installing PyTorch from source code and all of its dependencies from source code on development branches but will instead use the public stable PyPi PyTorch.**

Furthermore, instead of using Flash Attention through the PyTorch native user friendly [torch. scaled_dot_product_attention](https://pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html) API, this AMD Development build imports another library (development branch as well) attention implementation. We have seen more users use Flash Attention through PyTorch native [torch. scaled_dot_product_attention](https://pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html) API since it is more user friendly and bundled into out of box PyTorch. [Even AMD’s own public documentation recommends using Flash Attention through torch.scaled_dot_product_attention API](https://rocm.blogs.amd.com/artificial-intelligence/flash-attention/README.html#benchmarking-attention). We hope that these kernels get merged into PyTorch flash attention instead of making the end user install a separate library taking hours of their time to build. This is not a user-friendly experience. Furthermore, AMD must support FlexAttention as it has quickly become the go to in the industry.

AMD’s December 21st Dev build is on a hanging development branch. That means it is a branch that has not been fully QA’ed and is at use only at a risk branch. There are many concerns about the validity of the results from using a development build and branches and building from source code, as most users are not doing this in real life. Most users will be installing AMD/Nvidia PyTorch from PyPI stable release mostly so we recommend readers keep this in mend when analyzing these results.

That being said, we are including these development build results as it is an indication of where AMD public stable release software will be 1-2 quarters from now. However, at the same time, when it comes to compete, 1-2 quarters from now, Nvidia Blackwell will already be widely deployed, while AMD MI355X will not commence shipments until H2 2025.

![](https://substack-post-media.s3.amazonaws.com/public/images/24add0ee-f573-47e2-b9b6-81fbc1ba812d_3680x5640.png)
*Source: SemiAnalysis, AMD*

## Training Testing Methodology (GPT1.5B, Llama 8B, Llama 70B, Mistral)

There are many ways to test training performance. The most accurate way is to take a medium-sized AI startup model’s internal codebases and run them on a 512-1024 GPU cluster. This way, the test run has all the optimizations that a typical user would have. Everything else is just a proxy for the performance of these training runs. Training performance takes into account HBM bandwidth, HBM capacity, TFLOP/s, networking, and system architecture. **Comparing on paper HBM bandwidth/capacity is just like comparing on paper camera megapixels.**

MLPerf GPT3 175B Training is also a good proxy to measure the time it takes to train to a specific convergence. MLPerf benchmark considers global batch sizes and whether a mixed precision implementation incurs a convergence penalty. Unfortunately, MLPerf is quite difficult to run due to a lack of user-friendly documentation and instructions, and the performance is often min-maxed via a custom tuned configuration specifically concocted for MLPerf that an average user would not adopt. Note that Nvidia has submitted MLPerf Training results with over 11k H100s, while AMD runs MLPerf Training internally. AMD’s results are likely weak, so they have never submitted any MLPerf Training, let alone the MLPerf GPT3 175B benchmark.

When designing our SemiAnalysis benchmark, we wanted to reflect the average user’s model implementation, and so opted for [torch. scaled_dot_product_attention](https://pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html) API (which uses flash attention backend), PyTorch Distributed Data Parallel (DDP) and/or Fully Sharded Data Parallel (FSDP) with [torch.compile](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html). [Also note that AMD recommends users use torch.scaled_dot_product_attention in their own documentation](https://rocm.blogs.amd.com/artificial-intelligence/flash-attention/README.html#benchmarking-attention). We believe this is the most representative of a typical user workload. Further, we used a generic PyTorch native implementation of these models to keep it close to a typical ML Scientist user and make it easy to run with a single line of code. In contrast to MLPerf, the goal of our benchmark is to be as simple to run as possible, while still being a good proxy for performance. Note, since we don’t take into account time to convergence, this benchmark has a slight bias towards AMD as we set the micro batch size higher on AMD vs on Nvidia. When taking time to convergence into account, AMD results will be worse than what is stated.

As an aside, many AI practitioners have said they are not using Megatron or NeMo or 3D Parallelism due to the high level of complexity and lack of flexibility associated with those libraries, whose rigidity and complexity make their usage for ML Research effectively impossible. Note that in terms of 3D Parallelism, both Nvidia and AMD will get higher performance, assuming their software stack works, which is a big assumption for AMD. AMD Megatron is a fork of Nvidia Megatron and has less than 10 stars which means that it is probably not dogfooded well. Submitting bug reports would take **extra months** to get AMD Megatron working for simple models.

For our SemiAnalysis model training benchmark, we will test four models, with the first being a simple GPT 1.5B DDP, as we believe this is representative of what small-scale experiments/ablations would look like before scale-out to bigger model sizes. DDP is a much simpler and less network-intensive form of parallelism. Next, we tested the standard Llama3 8B and Llama3 70B 4 Layer Proxy as a baseline for a popular model's performance. Third, we tested Mistral 7B v0.1, which evaluates if hardware will perform well when adding a bit of complexity, as Mistral uses sliding window attention instead of the standard causal attention. Modern models such as ChatGPT, Claude, Genimi, o1, o3 do not use standard causal attention & use a complex attention mechanism.

A Modern GPT/Llama/Transformer model is built by stacking the same transformer layer over & over again. As such, measuring the performance of just 4 layers is a great proxy for the overall performance of the model.

![](https://substack-post-media.s3.amazonaws.com/public/images/e6177898-4068-4f94-976e-fe116180e7de_502x1141.png)
*Source: Imgur*

Furthermore, in modern LLM training for all frontier LLM models, pipeline parallelism is used which means that a couple of transformer layers are placed in each GPU server. Never in modern pretraining is a whole model placed on a single node.

![](https://substack-post-media.s3.amazonaws.com/public/images/7481b615-82be-41dc-931b-47cc8e70428d_2150x735.png)
*Source: SemiAnalysis*

The model FLOP for each token trained is defined by the following formula:

6 * non_input_embedding_params + 12 * num_layers * num_heads * head_dim * max_seq_len * density

With density being how sparse the attention is relative to a full mask. Causal attention has, for example, a 50% sparsity, while sliding window attention has even lower sparsity.

Note that originally our testing harness used 6 * params instead of 6 * non_input_embedding_params which is the wrong way of calculating model FLOP per token. Furthermore, there was another bug in regard to the way we used FSDP. **We have since updated our testing harness and retroactively retested as well as updated all of benchmark results across all versions of software for both H100, H200, MI300X, public stable, public nightly, VIP images and AMD development builds. All results listed below are with the updated testing harness.**

## Single Node Training Performance

Note that the H100/H200 performance we present in this report reflects an out of the box performance without any hand-crafted tuning from Nvidia engineers, while the results for the MI300X comes after many months of tuning and bug fixes from AMD’s engineers. We did not run into any Nvidia-specific bugs compared to AMD training, which was comparatively bug-filled. Five months ago, many models couldn’t run at more than 150 TFLOP/s on the AMD MI300X due to an AMD software bug in attention backwards and torch compile, which forced the user to manually mark a region of the model as non-compliable instead of having a full graph compile.

We see that, for all models, the H100/H200 wins relative to MI300X public releases/public nightly releases/Nov 25thbuild from source VIP image. It is interesting that the MI300X does not perform well on smaller models such as GPT 1.5B or on any model that uses a non-causal attention layer, like Mistral 7B v0.1. This is due to FlexAttention not being fully operational at the time of the deadline, while, on Nvidia GPUs, it has been working since August 2024. As such, the H100/H200 beats MI300X by more than 2.5x in terms of TFLOP/s for MI300X public release/public nightly release/Nov25th VIP build.

For the Dec 21st MI300X internal WIP development branches build, we still see it perform worse than H100/H200 on GPT 1.5B. Furthermore, it performs slightly worse than H100 on Mistral 7B. For Llama3 8B and Llama3 70B Proxy, the Dec 21st MI300X WIP development build performs better than H100/H200, but note that this is due to MI300X WIP development using an AMD engineer’s development branch that has not even been merged to the AMD main branch.

![](https://substack-post-media.s3.amazonaws.com/public/images/8c239ab5-1c2d-4303-8527-84498ef66c71_1491x1180.png)
*Source: SemiAnalysis*

Three months ago, attempting to do FP8 Training on AMD led to segfaults and hard errors. On the off chance it did work, it was, in fact, slower than the same run using BF16. We worked with AMD’s FP8 team to fix this issue, as well as the AMD hipBLASLt team, which created [tuning](https://github.com/ROCm/hipBLASLt/pull/1378) for fixing MI300X FP8 performance. FP8 Training is important as it speeds up training compared to BF16 & most frontier labs use FP8 Training.

After many fixes, we can see that the MI300X's Nov 25th throughput for Llama3 8B and GPT 1.5B is somewhat competitive with H100's. As usual, H200 wins in this category. However, for Llama3 70B 4 Layer Proxy, AMD Nov 25th’s results are sorely beaten.

For Mistral 7B which has a non-causal attention layer, AMD Nov 25th performance is close to half that of an H100. This shows that, for anything that isn’t a simple model, even after months of tuning, AMD is still not competitive due to a slight tweak in the model structure. Many frontier models and AI training startups are using complex attention layers for long context spans and efficient attention, but, AMD is still far behind on those.

Unfortunately, FP8 training on AMD only works on custom images such as our November 25th VIP image and December 21st WIP development branch image. When we first started trying AMD FP8 Training, it was slower than AMD BF16 Training on public releases.

![](https://substack-post-media.s3.amazonaws.com/public/images/1ec9137f-add4-46d0-98b4-68050db8a439_1491x1181.png)
*Source: SemiAnalysis*

For AMD’s WIP development builds, we see that on Llama3 8B, it wins against H100 but is still slower than H200’s public stable software release. H200 performance completely beats MI300X even on their Dec 21st WIP development branches.

It is interesting that the MI300X does not perform well on non-causal attention layer, like Mistral 7B v0.1 even for their internal builds. Mistral using sliding window attention which some of the frontier models uses. It seems that if you want to train a model that doesn’t use causal attention, AMD MI300X will automatically lose.

While a lot of people putting out performance comparisons between hardware, most do not open source their testing code and they do not make easily reproducible. We took an open source approach, and we have open-sourced our single node training benchmark and made it easy to run with only a couple of lines:

![](https://substack-post-media.s3.amazonaws.com/public/images/2ec308cc-f094-4fdb-b165-16d1fa1b2da5_836x941.png)
*Source: SemiAnalysis*

## Multi-Node Training Performance

For multi-node, we benchmarked two nodes of H100 and two nodes of MI300X. Unfortunately, we didn’t get access to a multi-node H200 deployment in time for the article.

H100 wins again by a big margin in this benchmark compared to MI300X, with the H100 ranging from 10-25% faster. This gap widens as you add more nodes working together into a single training workload. This is a known problem, which AMD is attempting to fix next year by deploying their new in house 400G AI focused NIC.

## AMD PYTORCH_TUNABLE_OPS FLAG is a Bad User Experience

In order to get AMD training working decently, users need to use PYTORCH_TUNABLE_OPS which is an AMD specific prototype flag for the end user to tune GEMMs. Since this is a prototype feature (i.e. not stable), in the past a lot of bugs with this feature cropped up including but not limited to [seg faults](https://github.com/pytorch/pytorch/issues/139116), HBM memory leaks, and a [whole](https://github.com/pytorch/pytorch/pull/139137) [host](https://github.com/pytorch/pytorch/pull/143507) of [other](https://github.com/pytorch/pytorch/pull/140673)issues such as many [unit tests being disabled](https://www.torch-ci.com/failure?failureCaptures=%5B%22test_linalg.py%3A%3ATestLinalgCUDA%3A%3Atest_matmul_small_brute_force_tunableop_cuda_float16%22%5D). These known tunable ops bugs have been fixed now but there are likely a many more unknown AMD software bugs.

Furthermore, even if users do not encounter any bugs and thus the runway is clear for this prototype AMD flag to work, it still takes users anywhere from 1-2 hours to tune any modern LLM model. Although these GEMMs can be cached by the end user, any minor changes to the end user’s code results in the need for the user to spend another 1-2 hours tuning. As you can imagine, this will slow down an ML Scientist’s iteration cycle speed when trying to conduct model R&D and ablations experiments.

On Nvidia, this flag isn’t needed as their GEMM library (cuBLASLt) comes tuned out of the box and cuBLASLt’s heuristic model out of the box picks the correct algorithm for most shapes on H100/H200. In contrast, AMD hipBLASLt/rocBLAS’s heuristic model picks the wrong algorithm for most shapes out of the box, which is why so much time-consuming tuning is required by the end user.

We recommend that AMD to fix their GEMM libraries’ heuristic model such that it picks the correct algorithm out of the box instead of wasting the end user’s time doing tuning on their end. Users often iterate quickly when doing research and therefore rerunning tunable ops will slow down research velocity significantly.

## Scale Up NVLink/xGMI  Topology

Scale up fabric is extremely important for GPU Clusters, as it provides an extremely fast path for tensor and expert parallelism used in frontier model training. For this reason, we have conducted benchmarks to measure scale up fabric performance.

The scale up fabric on H100 and H200 is called NVLink and provides 450GByte/s of bandwidth per GPU and connects 8 GPUs together. On the MI300X, the scale up fabric is called xGMI and, on paper, it connects 8 GPUs, providing 448GByte/s of bandwidth per GPU. On the surface, MI300X’s scale up network is extremely similar and close in performance to that of the H100/H200, providing just 0.5% less on paper bandwidth. Unfortunately, the reality of the situation differs sharply.

First, MI300X’s xGMI is a point-to-point fabric, which means that it isn’t *actually* providing 448GByte/s of bandwidth between GPUs pairs. Instead, each GPU can only talk to one another at 64GByte/s. A GPU can only reach the stated 448GByte/s if one GPU addresses all 7 other GPUs simultaneously. That means that, for Tensor Parallelism TP=2, the maximum bandwidth is 64GByte/s and 189GByte/s for TP=4.

![](https://substack-post-media.s3.amazonaws.com/public/images/4ac85f6f-0fa0-4f51-be6b-88662b666680_1455x1147.png)
*Source: SemiAnalysis*

In contrast, since Nvidia’s NVLink uses a switched topography, one GPU can talk to another GPU at the full 450GByte/s. Furthermore, the four NVSwitches in H100/H200 support in-network reduction (referred to as NVLink SHARP (NVLS), enabled by default), a technique to reduce data movements by carrying out collectives/reductions inside the switch itself.

![](https://substack-post-media.s3.amazonaws.com/public/images/77daa464-4fde-4e19-a96b-0b6195f59b82_2172x743.png)
*Source: SemiAnalysis*

## All Reduce/All to All/Reduce Scatter/All Gather Collectives Overview

We will showcase benchmarks across scale-up and scale-out networks for both the Nvidia H100/H200 and AMD’s MI300. The collectives that we will be testing are the main set of collectives used in frontier LLM training: all_reduce, all_gather, reduce_scatter, and all to all. All reduce is for data parallelism and tensor parallelism, all gather is used for ZeRO/FSDP parallelism (as well as for tensor parallelism), and Reduce Scatter is used for ZeRO/FSDP parallelism.

Due to the way that compute-communication overlapping works, real-world message sizes range from 16MiB to 256MiB, with the default PyTorch DDP size being 25MiB (NVIDIA’s MLPerf 11,000 H100 GPT-3 175B run used a [message size of max 200MiB](https://github.com/mlcommons/training_results_v4.1/blob/b87b9e396f771345d4ef122ba33456304f15228d/NVIDIA/benchmarks/gpt3/implementations/eos-dfw_n1452_ngc24.04_nemo/config_common.sh#L69)). We also test 8GiB and 16GiB just to see what the peak bus bandwidth is, though these message sizes are not used in the real world. All these collectives discussed above are used during 3D Parallelism and FSDP/ZeRO Parallelism, which are common techniques for training frontier models.

![](https://substack-post-media.s3.amazonaws.com/public/images/f528ea53-0b8c-4dff-8a48-c89ba475be2b_2259x1357.png)
*Source: DeepSpeed*
![](https://substack-post-media.s3.amazonaws.com/public/images/515beda1-3436-4319-8759-e74590c3530a_2206x1165.png)
*Source: Meta*

## Single Node NCCL Collective

We see that Nvidia does much better than AMD across all the real-world messages for every single collective. This is not surprising due to the H100/H200’s superior 450GByte/s NVLink switched topology with in-network reduction (NVLS), compared to MI300X’s 7x64GByte/s xGMI point-to-point topology.

![](https://substack-post-media.s3.amazonaws.com/public/images/fe08fabf-8ed6-4405-ab0d-2b700f7ea5b7_1725x1216.png)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/af7610d4-3246-4dda-a955-81c0b48d5613_1592x1147.png)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/a06bb258-12dc-4f75-97ec-9d2a08347d0d_1593x1134.png)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/71df6db8-d62f-4f91-ae6c-78c1d08b6082_1594x1168.png)
*Source: SemiAnalysis*

To reproduce this test, you can use our open source ClusterMax-NCCL/RCCL benchmark, which we developed to be easily run with one line of Bash. ClusterMax is our upcoming evaluation quantitative performance and qualitative user experience for ranking H100/B200/GB200/MI300X Neocloud clusters. Look forward to our upcoming *“ClusterMax Neocloud Evaluation | How to Rent GPUs”* article.

![](https://substack-post-media.s3.amazonaws.com/public/images/009fda89-6efa-4a29-a2dc-c55c6d8de066_3496x1568.png)
*Source: SemiAnalysis*

## Multi Node RCCL/NCCL Collectives and Scale Out Network Benchmarks

On both Nvidia’s H100/H200 and the MI300X, each GPU is connected to other nodes over the scale out network using a 400G Network Interface Card (NIC), connected directly every GPU. The H100/H200 reference design typically uses ConnectX-7 NICs for InfiniBand NDR or BlueField-3 for Spectrum-X Ethernet. Spectrum-X is NVIDIA’s custom Ethernet solution purpose-built for AI workloads. On the MI300X, the reference design recommends using RoCEv2 Ethernet with Broadcom Thor-2 NIC.

![](https://substack-post-media.s3.amazonaws.com/public/images/003120b8-0c44-4463-b289-549993ea52cc_1100x624.png)
*Source: Nvidia*

A typical GPU cluster almost always requires more layers than a single tier network, as a single-tier network can only support 128 GPUs (in the case of Broadcom Ethernet or Nvidia Spectrum X Ethernet) and 64 GPUs (for H100/H200 InfiniBand). In such a multi-tier network, deployments typically use an 8-rail optimized fat tree, where each one of the 8 GPU is connected to a separate switch (such a connection is called a “rail”). [In our AI Neocloud Playbook and Anatomy article, we explained in detail how a rail optimized network works](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/#cluster-level-networking-bill-of-materials).

![](https://substack-post-media.s3.amazonaws.com/public/images/1ba221b3-91a8-43ae-b321-d63d0d42bb5c_1614x781.png)
*Source: SemiAnalysis*

Just as Nvidia’s NVLink offers NVLS for its scale-up network, Nvidia’s H100/H200 InfiniBand scale out network also offers InfiniBand SHARP In-network Reduction which is, again, exclusive to Nvidia. AMD does not have an analogous product for the MI300X. InfiniBand SHARP works similarly to NVLink SHARP In-network Reduction as they both provide a way to reduce the amount of traffic going through the network, with the reductions carried out inside of Quantum-2 InfiniBand switches in the case of InfiniBand SHARP.

Unfortunately, unlike NVLink SHARP, which is enabled by default, InfiniBand SHARP is not enabled by default in the UFM/IB subnet manager. We have spoken to many Neoclouds, H100 cluster operators, and AI frontier labs, and most have said that they have not enabled SHARP due to increased NCCL_TIMEOUT rates and difficulties installing and configuring the network. We asked NVIDIA which AI customers use InfiniBand SHARP, but they declined to answer in specifics. One could speculate that if InfiniBand SHARP was useful in AI production workloads, NVIDIA marketing would shout at the top of their lungs to promote its successful deployment. Given the apparently limited adoption of InfiniBand SHARP for now, we show here collective performance for Nvidia both when SHARP is and is not enabled.

For some of the benchmarks, we have also collected Nvidia Spectrum-X Ethernet data on an Nvidia internal cluster called Israel-1. Nvidia Spectrum-X is used in xAI’s 200k H100/H200 cluster and can support clusters up to 100k GPUs in the Spectrum-X reference architecture version 1.2, but could potentially support up to 512k GPUs with a non-reference custom design.

We are also in the process of testing Google Cloud (GCP) H100’s in-house ethernet, as well as AWS’ H100 and H200s that are deployed on AWS’s in-house Ethernet (called EFAv2/EFAv3). We will be sharing the results in our upcoming “Collective Deep Dive” article, which will provide visualizations of  the different types of collectives, explain the different NCCL protocols (SIMPLE, LL, LL128), different NCCL algorithms (NVLS, NVLSTREE, RING, TREE, COLNETDIRECT, COLNETCHAIN, PAT), and how collectives run on GCP H100 Ethernet, AWS H100/H200 EFA, InfiniBand H100, Spectrum-X, etc.

Below we show a 32 GPU all reduce collective test. You can see that MI300X RoCEv2 is in last place compared to normal InfiniBand H100 and InfiniBand H100 with SHARP enabled. Simply put, poor all reduce performance leads to poor scale-out training.

![](https://substack-post-media.s3.amazonaws.com/public/images/09a00702-0524-4521-b8d5-50b6356cca42_1594x1203.png)
*Source: SemiAnalysis*

The MI300X’s performance decreases if you scale out (i.e. increase) the number of GPUs participating in a collective. As you can imagine, modern frontier training is carried out on clusters of at least 100,000 GPUs. MI300X RoCEv2 runs at half the speed for all the real-world message sizes of 16MiB to 256MiB when compared to the baseline of InfiniBand Non-SHARP. As per the chart below, Nvidia Spectrum-X Ethernet performance is quite close to InfiniBand Non-SHARP’s performance, due to Spectrum-X’s vertical integration with the NCCL collective library as well as its use of good congestion control and adaptive routing. AMD is attempting to vertically integrate next year with their upcoming Pollara 400G NIC, which supports Ultra Ethernet, hopefully making AMD competitive with Nvidia. As always, Nvidia is not standing still and by late next year, it will be ready to go into production with its 800G ConnectX-8 NICs, which provide a line rate twice as fast as AMD’s Pollara NIC.

AMD RCCL is a fork of Nvidia NCCL. AMD’s RCCL Team and many other teams at AMD are resource limited and don’t have enough of either compute or headcount to improve the AMD ecosystem. AMD’s RCCL Team currently has stable access to less than *32 MI300Xs for R&D*, which is ironic, as improving collective operations is all about having access to many GPUs. This is frankly silly, AMD should spend more on their software teams having access to more GPUs.

This contrasts with Nvidia’s NCCL team, which has access to R&D resources on Nvidia’s 11,000 H100 internal EOS cluster. Furthermore, Nvidia has Sylvain Jeaugey, who is the subject matter expert on collective communication. There are a lot of other world class collective experts working at Nvidia as well, and, unfortunately, AMD has largely failed to attract collective library talent due to less attractive compensation and resources - as opposed to engineers at Nvidia, where it is not uncommon to see engineers make greater than a million dollars per year thanks to appreciation in the value of RSUs.

To help alleviate these issues, TensorWave and SemiAnalysis are currently working with the AMD RCCL Team to improve collective performance. TensorWave has generously sponsored AMD a medium-sized cluster in order help the RCCL Team have greater resources to do their jobs. The fact that Tensorwave after buying many GPUs has to give AMD GPUs for them to fix their software is insane.

Another trend to notice is that for non-SHARP networks, all reduce collective’s speed will reduce logarithmically as you double the number of GPUs. In contrast, with SHARP, the speed/completion time stays the same. We have results for up to 1,024 H100s showing that IB SHARP all reduce is constant time across any number of GPUs in a collective. We will publish this in our upcoming *“Collective Deep Dive”*article.

![](https://substack-post-media.s3.amazonaws.com/public/images/8577baae-b3f0-4fb9-b48d-84af6d4855bf_1473x1153.png)
*Source: SemiAnalysis*

For all gather, all to all, and reduce scatter collectives, MI300X is anywhere from 2-4 times slower than InfiniBand. Unfortunately, we did not have access to Spectrum-X or InfiniBand SHARP benchmark data for all gather or reduce scatter.

![](https://substack-post-media.s3.amazonaws.com/public/images/27e21f6c-7eac-418f-8c68-095a30b28f1d_1670x1250.jpeg)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/d2ce4511-0ba1-4935-99f1-027c1ac56ca1_1720x1221.png)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/8baeab3c-61d2-44ec-a466-96c7e5c8496d_1723x1219.png)
*Source: SemiAnalysis*

Below, we provide our nccl/rccl benchmarking script. Unfortunately, due to the nature of cluster-specific setups, it is not as simple as a one-liner. It does require you to follow the README.md of nccl/rccl and nccl-tests/rccl-tests to run properly. On AWS and Google Cloud, there may also be custom nccl adapters that you will need to install.

![](https://substack-post-media.s3.amazonaws.com/public/images/bbec630b-1202-41aa-8b71-9795891e335b_814x747.png)
*Source: SemiAnalysis*

## AMD's User Experience is Suboptimal and the MI300X is Not Usable Out of the Box

Due to poor internal testing (i.e. “dogfooding”) and a lack of automated testing on AMD’s part, the MI300 is not usable out of the box and requires considerable amounts of work and tuning. [In November 2024 at AMD’s “Advancing AI”, AMD’s SVP of AI](https://www.youtube.com/live/vJ8aEO6ggOs?si=ViPmlckQNmDYCayJ&t=3416) stated that are over 200k tests running every evening internally at AMD. However, this seems to have done little to ameliorate the many AMD software bugs we ran into, and we doubt AMD is doing proper CI/CD tests include proper performance regression, or functional and convergence/numerics testing. We will outline a few examples here for readers to understand the nature of the AMD software bugs we have encountered and why we feel they have been very obstructive to a good user experience on AMD.

[Although AMD’s own documentation recommends using PyTorch native Flash Attention](https://rocm.blogs.amd.com/artificial-intelligence/flash-attention/README.html#benchmarking-attention), for a couple months this summer, AMD’s PyTorch native Flash Attention kernel ran at less than 20 TFLOP/s, meaning that a modern CPU would have calculated the attention backwards layer *faster than an MI300X GPU*. For a time, basically all Transformer/GPT model training using PyTorch on the MI300X ran at a turtle’s pace. Nobody at AMD noticed this until a bug report was filed following deep PyTorch/Perfetto profiling showing the backwards pass (purple/brown kernels) took up far more time than the forward pass (dark green section). Normally, the backwards section should take up just ~2x as much time as the forward pass (slightly more if using activation checkpointing).

![](https://substack-post-media.s3.amazonaws.com/public/images/358ec78a-dd8b-4604-a58c-d76c25837e2a_1481x209.png)
*Source: SemiAnalysis*

Another issue we encountered was that the AMD PyTorch attention layer led to a hard error when used with [torch.compile](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html) due to the rank of the longsumexp Tensor being incorrect. What was frustrating is that this had already been fixed in internal builds of AMD PyTorch on May 30th, but did not reach any AMD PyTorch distributions or even any PyTorch nightly builds until October when it was pointed out to them that there was a bug. This demonstrates a lack of testing and dogfooding on the packages AMD puts out to the public. Another core reason for this problem is that the lead maintainer of PyTorch (Meta) does not currently use MI300X internally for production LLM training, leading to code paths not used internally at Meta being buggy and not dogfooded properly. We believe AMD should partner with Meta to get their internal LLM training working on MI300X.

![](https://substack-post-media.s3.amazonaws.com/public/images/39607c82-c678-4bae-8963-bcdfa8141049_890x453.png)
*Source: SemiAnalysis*

On August 8th, Horace He and the Meta PyTorch Team released [FlexAttention](https://pytorch.org/blog/flexattention/), a critical API for creating non-causal attention layers without losing speed. To previously use attention variants like document masking, sliding window attention, softcap, and Alibi, a user would need to spend weeks handcrafting their own kernel in CUDA/HIP language, and subsequently pybinding it to PyTorch. However, with FlexAttention, a user can quickly generate all the attention variants using the API. FlexAttention achieves great performance by using block sparsity by only calculating the blocks of the mask where needed, ignoring the rest.

![](https://substack-post-media.s3.amazonaws.com/public/images/d9dbce6b-eefc-40ca-b6f2-753e47118714_437x357.png)
*Source: SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/59da3049-f7e0-419a-802f-4d2bbb774477_1600x1459.jpeg)
*Source: Meta*

With sliding window attention, FlexAttention can improve performance by 10-20x! This is amazing for the end user, but unfortunately, MI300X FlexAttention was in a poor state and suffers from numerous AMD software bugs (including convergence issues) until but a couple days ago. While the latest PyTorch nightly now fixes for convergence issues, this contrasts starkly with FlexAttention on Nvidia, which has been available since August. That means a ~6 month gap exists between the availability of these fantastic Pytorch features on Nvidia and AMD’s platforms. For frontier AI labs, six months is a lifetime, with OpenAI, Anthropic, and Google having released numerous models in such a span.

![](https://substack-post-media.s3.amazonaws.com/public/images/6388946a-2f1b-4006-b084-03b863949371_1475x1009.png)
*Source: SemiAnalysis*

## Exploring Ideas for Better Performance on AMD

AMD recommended we try PYTORCH_ TUNABLE_OPS to improve GEMM performance by sweeping through GEMM algorithms at runtime. However, as we mentioned earlier, this API works poorly because GEMMs should be tuned when compiling the hipBLASLt/RoCBLAS/cuBLASLt and not during the users' runtime. Users of Nvidia H100s do not need to use PYTORCH_ TUNABLE_OPS for most shapes because cuBLAS heuristic model will pick the correct algorithmn. This contrasts with AMD’s heuristic model, which never seems to pick the correct algorithm for most shapes. We recommend that AMD stop suggesting that users try tunable ops and instead focus on properly tuning their GEMM libraries internally.

When we tried PYTORCH_ TUNABLE_OPS on AMD, it led to an HBM memory leak of over 25 GByte out of the total MI300X capacity of 192GBytes, essentially wiping out the MI300’s HBM capacity advantage over the H100. The fix for this is to set a default hipBLASLt and rocBLAS workspace to prevent memory leaks.

![](https://substack-post-media.s3.amazonaws.com/public/images/a877f575-f237-4fde-8fa4-996f8180bf49_1024x540.png)
*Source: PyTorch/AMD*

As we mentioned earlier in this article, another issue we ran into was that there was a plethora of environment flags needed on MI300X to make it actually usable. We recommend to AMD that they stop putting users in the position of having to set these environment flags themselves and, instead, set default flags that lead to a usable environment. It is not simply their number, but also the complex interactions between the flags, making troubleshooting difficult. Getting reasonable training performance out of AMD MI300X is an NP-Hard problem.

Another issue is that certain AMD ROCm libraries could not be installed inside Docker due to AMD software CMake bugs leading to hard errors. This has since been fixed. On AMD GPUs, you need to pass in a convoluted set of flags to get the GPUs to be able to work inside a container, whereas with docker, getting GPUs to work is as simple as passing in “—gpus=all”. We recommend to AMD that they partner with Docker and ensure that Docker can autodetect GPUs for AMD as well, making the workflow as streamlined as when working with Nvidia GPUs.

![](https://substack-post-media.s3.amazonaws.com/public/images/d46c3ac7-7cdd-4e97-ad4d-d7c7f1fd3d0a_3496x1300.png)
*Source: SemiAnalysis*

## AMD’s Forked Libraries

Many of AMD’s libraries are forked off Nvidia’s open-source or ecosystem libraries. AMD uses a tool called Hipify to carry out source-to-source translation of Nvidia CUDA to AMD HIP. While the motivation is understandable, **they arenevertheless building on top of their competitor’s platform** and cannot expect to match or surpass Nvidia’s user experience with this software development strategy. They need to contribute their software to the AMD ecosystem. For example, instead of supporting FP8 training by forking Nvidia/TransformerEngine and source-to-source translation, they should attempt PyTorch native FP8 training to work well on their own hardware. Currently, AMD PyTorch native FP8 training recipes don’t work on AMD and the unit tests don’t even pass yet, there is no CI/CD for AMD PyTorch native FP8 training.

![](https://substack-post-media.s3.amazonaws.com/public/images/25b16d02-fbc7-4a54-b31f-42573d8784e3_1024x330.png)
*Source: SemiAnalysis*

## Detailed Recommendations to AMD on How to Fix Their Software

First, AMD needs to focus on attracting more software engineering resources and improving compensation for current engineers. The current compensation gap between AMD and Nvidia means that top talent is lured to Nvidia over AMD. This top talent is also attracted to Nvidia as it has far more compute/resources for engineers. AMD should procure more GPUs for their in-house development work and submit an MLPerf GPT3 175B result as soon as possible. Even if the result is not competitive with Nvidia right now, submitting such a benchmark will kick off the process for iterative improvement.

We also notice that AMD frequently gives their customers custom images, and, in fact, AMD developers themselves often work on top of such bespoke images. This is not best practice, as this means that AMD engineers have a different experience vs. images available to the public. AMD should instead lift the standard of public images by using these images internally and with its customers, and the AMD executive team should personally internally test (i.e. “dogfood”) what is getting shipped publicly.

We recommend that AMD create a public dashboard that runs every night, showing the performance of their hardware on benchmarks such as MLPerf or TorchBench. This dashboard should also include H100/H200 performance as a baseline.

Finally, AMD needs to completely transform its approach to environmental flags. Instead of setting a myriad of flags to get running out of the box, it should set them to recommended defaults so users can get started quickly.

AMD should collaborate with Meta to get production training workloads working on ROCm, as it is well-known amongst PyTorch users that PyTorch code paths tend to have tons of bugs unless Meta uses it internally. Meta currently hand writes HIP Kernels for their production MI300X inferencing but does not use MI300X for real training. It would be a fantastic improvement for the AMD ecosystem, and a marketing victory, if a smaller version of the next Llama is trained on AMD. Not to mention that this would open the door to AMD progressively moving towards larger models/clusters with Meta. Meta using AMD GPUs for actual model training would be a win-win for both companies as Meta is also looking for alternative training chips to Nvidia.

Currently Nvidia offers well over 1,000 GPUs for Continuous improvement and development of Pytorch externally and many more internally. AMD doesn’t. AMD needs to work with an AMD focused GPU Neocloud to have ~10,000 GPUs of each generation for internal development purposes and Pytorch. This will still be 1/8th that of Nvidia with their coming huge Blackwell clusters, but it’s a start. These can be dedicated to internal development and CICD for Pytorch.

**Lisa, we are open to a meeting on how to fix AMD’s Datacenter GPU User Experience for the better!**

## H100/H200/MI300X Networking BoM Analysis and Performance per TCO

In addition to our benchmarking of collectives and GEMM throughput, we have conducted several experiments exploring insightful topics for conducting further benchmarks and running real-world workloads on clusters. These experiments cover benchmarking warmup and repeat effects, VBoost Power Shifting, MLPerf Training GPT-3, BF16 vs FP16 throughput, throughput by GEMM input distribution, power per FLOP, and throughput for the PyTorch PyPi distribution vs Nvidia NGC Stable PyTorch images.

We also present a detailed networking bill of materials (BoM) analysis for the 1k GPU Ethernet, 1k GPU InfiniBand, 16k GPU Ethernet, and 16k GPU InfiniBand clusters. We also discuss the impact of using 51.2T Radix vs. 25.6T Radix switches for back-end networking.

Lastly – we present a performance per TCO analysis that shows how the H100/H200/MI300X stacks up in terms of $/hr per effective training petaflop. These items are available below to all SemiAnalysis subscribers and will be of great interest to datacenter operators, ML scientists, and investors.

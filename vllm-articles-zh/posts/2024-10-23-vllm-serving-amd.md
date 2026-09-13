---
title: "在 AMD MI300X 上服务 LLM：最佳实践"
title_en: "Serving LLMs on AMD MI300X: Best Practices"
source: https://vllm.ai/blog/2024-10-23-vllm-serving-amd
crawled: 2026-09-12
translated: 2026-09-12
---

# 在 AMD MI300X 上服务 LLM：最佳实践

> 原文：[Serving LLMs on AMD MI300X: Best Practices](https://vllm.ai/blog/2024-10-23-vllm-serving-amd) · vLLM 博客

客座文章，作者：Embedded LLM 与 Hot Aisle Inc.

[#硬件](https://vllm.ai/blog/tags/hardware)[#性能](https://vllm.ai/blog/tags/performance)

**TL;DR：** vLLM 在 AMD MI300X 上释放了惊人的性能：对于 Llama 3.1 405B，吞吐量比 Text Generation Inference（TGI）高 1.5x，首 token 延迟（TTFT）快 1.7x；对于 Llama 3.1 70B，吞吐量比 TGI 高 1.8x，TTFT 快 5.1x。本指南探讨 8 项关键的 vLLM 设置以最大化效率，向你展示如何在 AMD 上驾驭开源 LLM 推理的力量。如果你只想看最优参数，请直接跳到[快速上手指南](#quick-start-guide)。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/405b1.png)   ![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/405b2.png)
Llama 3.1 405B 在 8 x MI300X 上 vLLM 与 TGI 的性能对比（BF16，32 QPS）。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/70b1.png)   ![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/70b2.png)
Llama 3.1 70B 在 8 x MI300X 上 vLLM 与 TGI 的性能对比（BF16，32 QPS）。

### 简介

Meta 最近宣布其 Llama 3.1 405B 模型的全部线上流量都运行在 AMD MI300X GPU 上，充分展示了 AMD ROCm 平台对大语言模型（LLM）推理的强大能力与成熟度。这一激动人心的消息恰逢 ROCm 6.2 发布，它为 vLLM 支持带来了显著改进，让利用 AMD GPU 进行 LLM 推理变得前所未有的容易。

ROCm 是 AMD 对 CUDA 的回应，对一些人来说可能不太熟悉，但它正迅速成熟为一种稳健且高性能的替代方案。借助 vLLM，驾驭这一力量比以往任何时候都更容易。我们将向你展示如何做到。

### vLLM 与 TGI 的对比

vLLM 在 AMD MI300X 上释放了惊人的性能：对于 Llama 3.1 405B，吞吐量比 Text Generation Inference（TGI）高 1.5x，首 token 延迟（TTFT）快 1.7x；对于 Llama 3.1 70B，吞吐量比 TGI 高 1.8x，TTFT 快 5.1x。

在 Llama 3.1 405B 上，在各种每秒查询数（QPS）场景下，vLLM 在首 token 延迟（TTFT）和吞吐量方面都比 TGI 表现出显著优势。就 TTFT 而言，在优化配置下、16 QPS 时，vLLM 的平均响应速度约比 TGI 快 3.8x。吞吐量方面，vLLM 持续领先 TGI：在优化配置下、1000 QPS 时，vLLM 在 ShareGPT 数据集上达到 5.76 requests/second 的最高吞吐量，而 TGI 为 3.55 requests/second。

即使在默认配置下，vLLM 的性能也优于 TGI。例如，在 16 QPS 时，vLLM 默认配置达到 4.05 requests/second 的吞吐量，而 TGI 为 2.58 requests/second。这一性能优势在不同 QPS 水平上都得以保持，凸显了 vLLM 处理大语言模型推理任务的高效性。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/introduction/Throughput (Requests per Second).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/introduction/Mean TTFT (ms).png)
Llama 3.1 405B 在 8 x MI300X 上 vLLM 与 TGI 的性能对比（BF16，QPS 16、32、1000；命令见附录）。

### 如何以最优性能运行 vLLM

#### 关键设置与配置

我们针对 MI300X 广泛测试了各种 vLLM 设置以找出最优配置。以下是我们的心得：

- **分块预填充（Chunked Prefill）**：经验法则是，目前在 MI300X 上大多数情况下应禁用它以获得更好性能。
- **多步调度（Multi-Step Scheduling）**：多步调度可在 GPU 利用率和整体性能上带来显著收益。将 `--num-scheduler-steps` 设为 10 到 15 之间的值，以优化 GPU 利用率和性能。
- **前缀缓存（Prefix Caching）**：在某些场景中，将前缀缓存与分块预填充结合可以增强性能。但如果用户请求的前缀缓存命中率较低，建议同时禁用分块预填充和前缀缓存。
- **图捕获（Graph Capture）**：在使用支持长上下文长度的模型时，将 `--max-seq-len-to-capture` 设为 16384。但请注意，增大该值并不总是能保证性能提升，有时反而会因次优的桶（bucket）大小而导致性能下降。
- **AMD 特定优化**：禁用 NUMA balancing 并调整 `NCCL_MIN_NCHANNELS` 可带来进一步的性能提升。
- **KV 缓存数据类型**：为获得最佳性能，使用默认的 KV 缓存数据类型，它会自动匹配模型的数据类型。
- **张量并行（Tensor Parallelism）**：为了优化吞吐量，使用能容纳模型权重和上下文的最小张量并行（TP）度，并运行多个 vLLM 实例。为了优化延迟，将 TP 设为等于节点内的 GPU 数量。
- **最大序列数**：为优化性能，根据 GPU 的显存和计算资源，将 `--max-num-seqs` 提高到 512 或更高。这可以显著提升资源利用率和吞吐量，尤其对于处理较短输入和输出的模型。
- **使用 CK Flash Attention**：CK Flash Attention 实现比 triton 实现快得多。

#### 详细分析与实验

##### 案例 1：分块预填充（Chunked Prefill）

分块预填充是 vLLM 的一项实验特性，它允许将大的预填充请求切分为更小的块，与解码请求一起批处理。这通过让受计算限制的预填充请求与受内存限制的解码请求重叠执行来提升系统效率。你可以在 LLM 构造函数中设置 `--enable_chunked_prefill=True`，或使用 `--enable-chunked-prefill` 命令行选项来启用它。

根据我们运行的实验，我们发现与禁用分块预填充相比，调整分块预填充的值只有轻微的改进。不过，如果你不确定是否启用分块预填充，可以先从禁用开始，通常应能获得比默认设置更好的性能。这是 MI300X GPU 特有的结论。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case01-chunked-prefill/Requests Per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case01-chunked-prefill/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case01-chunked-prefill/Mean TPOT (ms).png)

##### 案例 2：调度器步数（Number of scheduler steps）

vLLM v0.6.0 引入了*多步调度*（multi-step scheduling），有望带来更高的 GPU 利用率和更好的整体性能。正如这篇[博文](https://blog.vllm.ai/2024/09/05/perf-update.html)所详述的，这一性能提升背后的魔力在于：它一次执行调度和输入准备，然后让模型连续运行多个步骤而不打断 GPU。通过巧妙地将 CPU 开销摊薄到这些步骤中，它显著减少了 GPU 空闲时间并大幅提升性能。

要启用多步调度，将 `--num-scheduler-steps` 参数设为大于 1 的数字（1 是默认值）。值得一提的是，我们发现随着取值升高，多步调度的收益递减，因此我们坚持以 15 为上限。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case02-num-scheduler-steps/Requests per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case02-num-scheduler-steps/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case02-num-scheduler-steps/Mean TPOT (ms).png)

##### 案例 3：分块预填充与前缀缓存

分块预填充与前缀缓存都是 vLLM 中的优化技术：前者将大的预填充切分为更小的块以便高效批处理，后者针对跨查询共享的前缀复用缓存的 KV（键值）计算。

默认情况下，*如果模型的上下文长度超过 32k token，vLLM 会自动启用分块预填充特性*。用于预填充切分的最大 token 数默认为 512。

在深入分析图表之前，我们先解释实验中使用的术语。***Fresh Run***（首次运行）指前缀缓存内存完全没有被填充的情况。***2nd Run***（第二次运行）指在*Fresh Run*之后再次运行基准测试脚本。一般而言，在*2nd Run*重新运行 ShareGPT 基准数据集时，我们会得到约 *50%* 的前缀缓存命中率。

观察下面的图表，我们可以对这一实验得出三点观察：

1. 对比柱 2（红色）与基线（蓝色），性能有巨大提升。
2. 对比柱 3（黄色）、柱 5（橙色）和柱 6（青色）与基线，分块预填充的性能取决于用户请求输入提示长度的分布。
3. 在实验中我们发现柱 3（黄色）和柱 4（绿色）的前缀缓存命中率分别约为 *0.9%* 和 *50%*。结合柱 3（黄色）和柱 4（绿色）与基线及柱 2（红色）的对比，这说明：如果用户请求的前缀缓存命中率不高，同时禁用分块预填充和前缀缓存可以视为一条好的经验法则。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case03-chunked-prefill-and-prefix-caching/Requests per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case03-chunked-prefill-and-prefix-caching/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case03-chunked-prefill-and-prefix-caching/Mean TPOT (ms).png)

##### 案例 4：最大可捕获序列长度（Max sequence length to capture）

vLLM 中的 `--max-seq-len-to-capture` 参数控制 CUDA/HIP 图（graphs）能够处理的最大序列长度。CUDA/HIP 图通过捕获并重放 GPU 操作来优化性能。如果序列超过该长度，系统会回退到逐个执行操作的 eager 模式，效率可能较低。这一设置同时适用于普通模型和编码器-解码器模型。

我们的基准测试揭示了一个有趣的规律：增大 `--max-seq-len-to-capture` 并不总能提升性能，有时甚至会使性能下降。这可能与 vLLM 为不同序列长度创建桶（bucket）的方式有关。

原因如下：

- **分桶（Bucketing）**：vLLM 使用桶将相近长度的序列分组，为每个桶优化图捕获。
- **最优桶**：起初，桶的粒度较细（例如 [4, 8, 12,..., 2048, 4096]），可为各种序列长度实现高效图捕获。
- **更粗的桶**：增大 `--max-seq-len-to-capture` 可能导致桶变得更粗（例如 [4, 8, 12, 2048, 8192]）。
- **性能影响**：当输入序列落入这些更大、更不精确的桶时，捕获的 CUDA/HIP 图可能不是最优的，从而可能导致性能下降。

因此，虽然用 CUDA/HIP 图捕获更长序列看似有益，但必须考虑其对分桶和整体性能的潜在影响。找到最优的 `--max-seq-len-to-capture` 值可能需要实验，以在图捕获效率与适合特定工作负载的桶大小之间取得平衡。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case04-max-seq-len-to-capture/Requests per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case04-max-seq-len-to-capture/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case04-max-seq-len-to-capture/Mean TPOT (ms).png)

##### 案例 5：AMD 推荐的环境变量

为进一步优化 vLLM 在 AMD MI300X 上的性能，我们可以利用 AMD 特定的环境变量。

- **禁用 NUMA Balancing**：非一致性内存访问（NUMA）balancing 有时会妨碍 GPU 性能。按照 [AMD MAD 仓库](https://github.com/ROCm/MAD/blob/develop/benchmark/vllm/README.md)的建议，禁用它可以避免潜在的 GPU 挂起并提升整体效率。可以通过以下命令实现：

  ```
  # disable automatic NUMA balancing
  sh -c 'echo 0 > /proc/sys/kernel/numa_balancing'
  # check if NUMA balancing is disabled (returns 0 if disabled)
  cat /proc/sys/kernel/numa_balancing
  0
  ```
- **调整 NCCL 通信**：NVIDIA 集合通信库（NCCL）用于 GPU 间通信。对于 MI300X，[AMD vLLM fork 的性能文档](https://github.com/ROCm/vllm/blob/main/ROCm_performance.md)建议将 `NCCL_MIN_NCHANNELS` 环境变量设为 112，以潜在地提升性能。

在我们的测试中，启用这两项配置带来了轻微的性能提升。这与["NanoFlow: Towards Optimal Large Language Model Serving Throughput" 论文](https://arxiv.org/abs/2408.12757)的发现一致：虽然优化网络通信有益，但由于 LLM 推理主要由受计算限制和受内存限制的操作主导，其影响可能有限。

尽管收益可能不大，但精细调整这些环境变量有助于从你的 AMD 系统中榨取最大性能。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case05-amd-recommended-environmental-variables/Requests Per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case05-amd-recommended-environmental-variables/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case05-amd-recommended-environmental-variables/Mean TPOT (ms).png)

##### 案例 6：KVCache 类型 Auto/FP8

默认情况下，vLLM 会自动分配与模型数据类型匹配的 KV 缓存类型。不过，vLLM 也支持 MI300X 上的原生 FP8，我们可以利用它来降低 KVCache 的内存需求，从而增加模型可部署的上下文长度。

我们实验了使用 Auto KVCache 类型和 FP8 KV 缓存类型，并与默认基线进行比较。从下图可以看出，使用 Auto KVCache 类型（红色）比将 KV 缓存类型设为 FP8（黄色）获得更高的每秒请求数。从理论上讲，这可能是由于 `Llama-3.1-70B-Instruct (bfloat16)` 模型中的量化开销，但由于该开销的成本看起来很小，在某些情况下它仍然可能是一个不错的折中，可换取 KVCache 需求的大幅降低。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case06-kvcache-type/Requests per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case06-kvcache-type/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case06-kvcache-type/Mean TPOT (ms).png)

##### 案例 7：TP 4 与 TP 8 之间的性能差异

张量并行是一种分发大模型计算负载的技术。它通过将单个张量切分到多个设备上，实现特定操作或层的并行处理。这种方式降低了模型的内存占用，并支持跨多块 GPU 的扩展。

虽然提高张量并行度可以通过提供更多计算资源来提升性能，但收益并不总是线性的。这是因为随着更多设备的加入，通信开销会增加，而每块 GPU 上的工作负载会减少。鉴于 MI300X 强大的处理能力，每块 GPU 上过小的工作负载反而可能导致利用率不足，进一步阻碍性能扩展。

因此，在优化吞吐量时，我们建议启动多个 vLLM 实例，而不是激进地提高张量并行度。这种方式往往能带来更线性的性能提升。但如果优先考虑最小化延迟，提高张量并行度可能是更有效的策略。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case07-tensor-parallelism/Requests per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case07-tensor-parallelism/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case07-tensor-parallelism/Mean TPOT (ms).png)

##### 案例 8：最大（并行）序列数的影响

`--max-num-seqs` 参数指定每次迭代可以处理的最大序列数。该参数控制一个批次中的并发请求数量，影响内存使用和性能。在 ShareGPT 基准测试中，由于样本的输入输出长度较短，托管在 MI300X 上的 `Llama-3.1-70B-Instruct` 每次迭代可以处理大量请求。在我们的实验中，即使将 `--max-num-seqs` 设为 1024，它仍然是限制因素。

![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case08-max-num-seq/Request per Second.png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case08-max-num-seq/Mean TTFT (ms).png)
![](https://vllm.ai/blog-assets/figures/vllm-serving-amd/case08-max-num-seq/Mean TPOT (ms).png)

### 快速上手指南

如果你不确定部署设置和用户请求的分布情况，你可以：

- 使用 CK Flash Attention\*（虽然这里没有展示，但 CK Flash Attention 实现比 triton 对应实现快得多）
  - `export VLLM_USE_TRITON_FLASH_ATTN=0`
- 禁用分块预填充 `--enable-chunked-prefill=False`
- 禁用前缀缓存
- 如果模型支持长上下文长度，将 `--max-seq-len-to-capture` 设为 16384
- 将 `--num-scheduler-steps` 设为 10 或 15。
- 设置 AMD 环境：
  - `sh -c 'echo 0 > /proc/sys/kernel/numa_balancing' `
  - `export NCCL_MIN_NCHANNELS=112`
- 根据 GPU 的显存和计算资源，将 `--max-num-seqs` 提高到 512 及以上。

```
VLLM_USE_TRITON_FLASH_ATTN=0 vllm serve meta-llama/Llama-3.1-70B-Instruct --host 0.0.0.0 --port 8000 -tp 4 --max-num-seqs 1024 --max-seq-len-to-capture 16384 --served-model-name meta-llama/Llama-3.1-70B-Instruct --enable-chunked-prefill=False --num-scheduler-steps 15 --max-num-seqs 1024
```

为了便于快速搭建，我们已将 vLLM 0.6.2 的 Docker 镜像（commit：*cb3b2b9ba4a95c413a879e30e2b8674187519a93*）编译并推送到 GitHub Container Registry。
下载镜像：

```
# v0.6.2 post
docker pull ghcr.io/embeddedllm/vllm-rocm:cb3b2b9
# P.S. We also have compiled the image for v0.6.3.post1 at commit 717a5f8
docker pull ghcr.io/embeddedllm/vllm-rocm:v0.6.3.post1-717a5f8
```

使用该镜像启动 docker 容器：

```
sudo docker run -it \
   --network=host \
   --group-add=video \
   --ipc=host \
   --cap-add=SYS_PTRACE \
   --security-opt seccomp=unconfined \
   --device /dev/kfd \
   --device /dev/dri \
   -v /path/to/hfmodels:/app/model \ # if you have pre-downloaded the model weight, else ignore
   ghcr.io/embeddedllm/vllm-rocm:cb3b2b9 \
   bash
```

现在用我们找到的参数启动 LLM 服务器：

```
VLLM_USE_TRITON_FLASH_ATTN=0 vllm serve meta-llama/Llama-3.1-70B-Instruct --host 0.0.0.0 --port 8000 -tp 4 --max-num-seqs 1024 --max-seq-len-to-capture 16384 --served-model-name meta-llama/Llama-3.1-70B-Instruct --enable-chunked-prefill=False --num-scheduler-steps 15 --max-num-seqs 1024
```

### 结论

本指南探索了 vLLM 在 AMD MI300X GPU 上服务大语言模型的强大能力。通过精细调整分块预填充、多步调度和 CUDA 图捕获等关键设置，我们展示了如何相较标准配置和其他服务方案取得可观的性能提升。vLLM 释放出显著更高的吞吐量和更快的响应时间，是在 AMD 硬件上部署 LLM 的理想选择。

然而，需要承认的是，我们的探索主要集中在输入输出较短的通用聊天机器人使用场景。针对摘要或长文本生成等特定用例优化 vLLM 仍需进一步研究。此外，深入探究 Triton 与 CK 注意力内核之间的性能差异也可能带来更多洞见。

我们还要感谢 Leonard Lin 的[这篇精彩博文](https://shisa.ai/blog/posts/tuning-vllm-mi300x/)，其中介绍了如何进一步针对 MI300X 优化 vLLM，包括 hipBLAS 与 hipBLASLt、CK Flash Attention 与 Triton Flash Attention、张量并行与流水线并行等对比。

### 致谢

本博文由 [Embedded LLM](https://embeddedllm.com/) 团队撰写，感谢 [Hot Aisle Inc.](https://hotaisle.xyz/) 赞助 MI300X 用于 vLLM 基准测试。

### 附录

#### 服务器规格

以下是出色的 Hot Aisle 服务器的配置：

- CPU：2 x Intel Xeon Platinum 8470
- GPU：8 x AMD Instinct MI300X Accelerators
  我们在基准测试中使用的模型和软件如下：
- 模型：meta-llama/Llama-3.1-405B-Instruct 和 meta-llama/Llama-3.1-70B-Instruct
- vLLM（v0.6.2）：vllm-project/vllm: A high-throughput and memory-efficient inference and serving engine for LLMs (github.com) commit：cb3b2b9ba4a95c413a879e30e2b8674187519a93
- 数据集：ShareGPT
- 基准测试脚本：仓库中的 benchmarks/benchmark\_serving.py

我们从仓库中的 Dockerfile.rocm 构建了 ROCm 兼容的 vLLM docker（我们已将用于运行基准测试的 vLLM 版本的 docker 镜像推送出去，可通过 `docker pull ghcr.io/embeddedllm/vllm-rocm:cb3b2b9` 获取）。
**所有基准测试均在 docker 容器实例中运行，使用 4 块 MI300X GPU，并以 `VLLM_USE_TRITON_FLASH_ATTN=0.` 启用 CK Flash Attention。**

#### 基准测试详细配置

| 配置 | 命令 |
| --- | --- |
| vLLM 默认配置 | `VLLM_RPC_TIMEOUT=30000 VLLM_USE_TRITON_FLASH_ATTN=0 vllm serve Llama-3.1-405B-Instruct -tp 8 --max-num-seqs 1024 --max-num-batched-tokens 1024 ` |
| TGI 默认配置 | `ROCM_USE_FLASH_ATTN_V2_TRITON=false TRUST_REMOTE_CODE=true text-generation-launcher --num-shard 8 --sharded true --max-concurrent-requests 1024 --model-id Llama-3.1-405B-Instruct` |
| vLLM（本指南） | `VLLM_RPC_TIMEOUT=30000 VLLM_USE_TRITON_FLASH_ATTN=0 vllm serve Llama-3.1-405B-Instruct -tp 8 --max-seq-len-to-capture 16384 --enable-chunked-prefill=False --num-scheduler-steps 15 --max-num-seqs 1024 ` |
| TGI（本指南） | `ROCM_USE_FLASH_ATTN_V2_TRITON=false TRUST_REMOTE_CODE=true text-generation-launcher --num-shard 8 --sharded true --max-concurrent-requests 1024 --max-total-tokens 131072 --max-input-tokens 131000 --model-id Llama-3.1-405B-Instruct` |

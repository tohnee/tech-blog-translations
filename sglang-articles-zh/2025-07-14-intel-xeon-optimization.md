---
title: "使用 Intel® Xeon® 6 CPU 在 SGLang 上高性价比部署 DeepSeek R1"
title_en: "Cost Effective Deployment of DeepSeek R1 with Intel® Xeon® 6 CPU on SGLang"
author: "Intel PyTorch Team"
date: "July 14, 2025"
previewImg: /images/blog/xeon/preview_headshot.png
source: https://lmsys.org/blog/2025-07-14-intel-xeon-optimization/
translated: 2026-09-12
---

# 使用 Intel® Xeon® 6 CPU 在 SGLang 上高性价比部署 DeepSeek R1

> 原文：[Cost Effective Deployment of DeepSeek R1 with Intel® Xeon® 6 CPU on SGLang](https://lmsys.org/blog/2025-07-14-intel-xeon-optimization/) · LMSYS Blog · Intel PyTorch Team

DeepSeek R1 的惊艳表现，标志着超大专家混合（MoE）模型在大语言模型（LLM）领域的崛起。然而，其庞大的模型体量和独特的架构给部署带来了新的挑战。巨大的内存需求通常意味着需要 8 块甚至 16 块高端 AI 加速器才能完成部署。

过去几个月里，Intel PyTorch 团队持续为 SGLang 的 CPU 后端做贡献，并提出了一种高性能的纯 CPU 方案：使用第六代 Intel® Xeon® Scalable 处理器，成本仅为原来的零头。在本篇博客中，我们将讲解在配备 Xeon® 6 CPU 的单节点上高效部署 DeepSeek 的技术细节。

## 亮点

* SGLang 现已在支持 Intel® Advanced Matrix Extensions（AMX）的 Intel® Xeon® CPU 上提供原生 CPU 后端。
* 同时支持稠密 FFN 与稀疏 FFN（MoE）的 BF16、INT8 和 FP8。
* 相比 llama.cpp，TTFT 获得 **6-14 倍**加速，TPOT 获得 **2-4 倍**加速。
* 通过高度优化的 MoE 算子实现了 **85%** 的内存带宽效率。
* 借助张量并行（TP）实现多 NUMA 并行。

## CPU 优化策略

在本篇博客中，我们将讲解算子级优化的技术细节，包括任务切分策略、内存访问效率，以及如何有效利用 Intel® AMX 实现高度优化的 GEMM。

本节聚焦于 4 个性能热点：Extend Attention 和 Decode Attention——二者是 SGLang 的 RadixAttention 后端；MoE——构成了 DeepSeek R1 中的大部分权重；以及 FP8 GEMM——在缺乏原生 FP8 支持的现有 x86 平台上，我们采用了模拟（emulated）方案。

### Extend Attention（扩展注意力）

我们基于 RadixAttention 的接口，实现了一个依托 Intel® AMX 的原生 C++ 后端。它由两个主要部分组成：a) Extend Attention，负责处理多头注意力（MHA）的预填充（prefill）阶段；b) Decode Attention，负责解码阶段。我们以 GPU 算子为参照，将 Flash Attention 算法映射到 CPU 指令（intrinsics）上，如下方 **图 1** 所示：

![图 1：预填充阶段的 Flash Attention](/images/blog/xeon/fig-1.png)

为消除冗余计算，SGLang 将 query 序列划分为两部分：

* **prefix（前缀）**——历史序列，其注意力呈矩形；
* **extend（扩展）**——新加入的 prompt，其注意力呈下三角。

CPU 算子（kernel）与 Flash Attention V2 算法精确对应，我们仔细选择 Query 序列和 KV 序列的块大小，确保注意力的中间值 `Si` 与动量值 `mi`、`S*` 能装进 L1/L2 缓存。GEMM 部分由 AMX 计算，块级逐点运算（Block Pointwise OPs）由 AVX512 计算。由于 AMX 以 FP32 做累加（例如 A: BF16；B: BF16；C: FP32），我们将数据类型转换与动量更新融合在一起：让第一次 GEMM 的结果 `Si` 保持 FP32，让第二次 GEMM 的输入 `S∆` 转为 BF16，在获得高计算效率的同时，将舍入误差降到最低。

### Decode Attention（解码注意力）

与预填充相比，解码面临更大的并行化压力，原因是 query 序列长度缩减为 1。具体来说，在多头注意力中，我们可以在 `[Batches, Heads, qBlocks]` 维度上并行化算子；而单请求解码时，该维度会退化为 `[1, Heads, 1]`，导致并行度不足。我们实现了 Flash Decoding 算法，将 KV 序列切分为多个 split 以提升并行度，如 **图 2** 所示。实现分两个阶段完成：先为每个 KV split 计算注意力，再将所有 split 的中间结果归约（reduce）为最终输出。

![图 2：Flash Decoding 实现](/images/blog/xeon/fig-2.png)

#### 多头潜在注意力（MLA）优化

MLA 是 DeepSeek 系列模型的核心特性之一。除了 Flash Decoding 之外，我们还在 MLA 的 CPU 实现上做了若干关键优化。我们参考了 FlashMLA，它利用 **key** 和 **value** 共享同一张量存储这一事实，将内存加载与计算流水线化。

![图 3：MLA 解码实现](/images/blog/xeon/fig-3.png)

* **一次加载、两次打包（Load Once Pack Twice）**：AMX 要求 tile 数据为 VNNI 格式，而且由于第一次 GEMM 是 NT、第二次 GEMM 是 NN，key 和 value 需要以不同方式打包。我们实现了完全向量化的打包逻辑，如 **图 3** 所示：KV 缓存通过 2 个带预取的 LUT（查找表）读取；每加载 32 个 lane（`BLOCK_N` 等于 32），就同时打包进两个线程本地的中间缓冲区，一个用于 key，格式为 `[E/2, BLOCK_N, 2]`；另一个用于 value，格式为 `[BLOCK_N/2, Ev, 2]`。
* **头折叠（Head Folding）**：MLA 在解码阶段采用权重吸收（weight absorption），将 **key** 和 **value** 的头数都降为 1。因此，我们可以把 Head 维度折叠进 GEMM，以提升计算强度，如下式所示。在按 Head 维度分块时，我们也兼顾了并行度的平衡：DeepSeek R1 的 Head 维度为 22，单请求时我们使用 `BLOCK_SIZE` 为 6，请求增多时逐步增大到 22。

![头折叠（Head Folding）](/images/blog/xeon/equations-1.png)

总体而言，针对 MLA 的算子级优化相比朴素实现带来约 **1.9 倍**的性能提升。值得一提的是，我们还将 KV 缓冲区设置与解码算子融合，带来 **12%** 的改进，因为它消除了 `torch` 中的若干低效环节：索引时的隐式数据类型转换、为张量切片创建 `TensorImpl`、以及用 `TensorIterator` 映射拷贝等。

### MoE

用 torch 朴素地实现 MoE，需要按顺序遍历各个专家，并在每次线性投影前为对应专家收集（掩码）激活。为提升效率，一种常见策略是对激活的索引排序，再将其切分为块。我们沿用了 SGLang 现有 GPU 算子的实现，如 **图 4** 所示：对 `topk_ids` 执行 `argsort`，并按专家 id 将激活的索引保存在 `sorted_ids` 中。

我们为 CPU 算子做了几项额外优化：

* **SiLU 融合**：为了融合 `up_proj` 和 `SiLU`，我们实现了按 `A×[B1, B2]=[C1, C2]` 模式运行的 GEMM 算子。`B1` 取自左半、`B2` 取自右半，即可将 `SiLU(C1) * C2` 融合在一起，省去对 `up_proj` 输出的额外加载/存储。
* **动态量化融合**：在面向 MoE 的 INT8 动态量化算子中，我们将 BF16 到 UINT8 的量化与激活的读取融合。我们同时实现了 AVX512 和 AMX 两种算子，并根据输入配置在二者间选择。AMX 同时支持 U8S8 和 S8S8，而 AVX512-VNNI 只支持 U8S8（A 为 UINT8、B 为 INT8），因此我们做了折中，将权重对齐到 U8S8 模式——这意味着需要一个 `-128×B` 的补偿因子把 S8S8 转换为 U8S8：`A × B=(A + 128) × B - 128 × B`。

![图 4：MoE 实现](/images/blog/xeon/fig-4.png)

综合这些优化，INT8 MoE 达到了 **85%** 的内存带宽效率，即在多路复用秩双列直插式内存模块（MRDIMMs）上实现 **1.45TB/s** 的有效内存带宽。

### FP8 推理

DeepSeek R1 采用 FP8 混合精度训练，这对 CPU 设备是很大的挑战，原因显而易见：现有 x86 设备对 FP8 没有原生支持。然而，提供 FP8 支持必不可少，因为它代表了用户的原始使用体验。我们为 FP8 MoE 和 GEMM 做了几项优化：

* **仅权重 FP8（Weight Only FP8）**：FP8 MoE/GEMM 采用仅权重（weight-only）模式，先将 FP8 转换为 BF16（与激活一致），再进行计算。
* **高效的向量化转换**：FP8 到 BF16 的数据类型转换是 CPU 上的主要性能瓶颈。我们尝试了两种方案：a) 用 LUT 从一张 2^8 的表中取 BF16 数据；b) 用指令级向量化转换。值得注意的是，两种方案同样慢，都需要 60 至 70 个时钟周期才能完成，对任何性能敏感的场景都不可接受。我们对方案 b) 做了取舍：跳过 NaN 检查和 DENORM 处理，从而将转换时间缩短了一半。
* **WOQ 感知的缓存分块（Cache Blocking）**：为把数据类型转换开销降到最低，我们在 GEMM 的缓存分块过程中做 WOQ 权重解包。具体来说，对于分配给每个线程的权重块，我们以锯齿形（zigzag）顺序访问这些权重块，并将解包后的 BF16 块缓存在 L2 中，确保每个块的慢速类型转换只发生一次。

我们在 GSM8K 和 MMLU 上进行了验证，模拟 FP8 实现与 GPU 结果的精度完全一致。配合上述优化技巧，FP8 实现达到了 INT8 实现的约 **80%** 至 **90%**。

## 多 NUMA 并行

非一致内存访问（NUMA）是一种面向多进程处理（multiprocessing）的计算机内存设计，常见于服务器 CPU：内存访问时间取决于内存位置相对于处理器的远近。在 NUMA 下，处理器访问自己的本地内存比访问远程内存（位于其他处理器本地的内存，或处理器之间共享的内存）更快。为将远程内存访问降到最低，我们把多 GPU 场景下的张量并行（TP）映射到了 CPU 服务器上的多 NUMA。

我们还基于共享内存方案实现了通信原语，例如 all reduce、all gather，跳过了调用栈繁琐的 `torch.distributed`。总体而言，通信开销仅占端到端时间的 **3%**。

## 性能评估

我们的测试平台是一台先进的双路 Intel® Xeon® 6980P CPU 服务器，每个 socket 128 核。我们选取另一个流行的 LLM 工具 **llama.cpp** 作为性能基线，与 SGLang CPU 后端对比。我们评估了 3B 到 671B 共 4 个模型：**DeepSeek-R1-671B**、**Qwen3-235B**、**DeepSeek-R1-Distilled-70B** 和 **Llama3.2-3B**。

### 基准测试说明：

* **Socket 设置**：Llama3.2-3B 使用单 socket，其余三个模型使用双 socket，因为在双 socket 上运行 3B 的小型 LLM 反而会导致性能下降。
* **子 NUMA 集群（SNC）设置**：SGLang 数据在开启 SNC 时采集，llama.cpp 数据在关闭 SNC 时采集，因为 llama.cpp 在开启 SNC 时无法保证本地 NUMA 访问。
* **多实例**：由于 llama.cpp 没有实现上文提到的**多 NUMA 并行**，在双 socket 上运行 1 个实例甚至比单 socket 更慢。为公平起见，我们在双 socket 上为 llama.cpp 运行 2 个实例（每个 socket 各一个），并采集 TTFT 和 TPOT 指标。
* **基线数据类型**：INT8 与 GGUF Q8 格式对比。由于 llama.cpp 没有 FP8 优化，FP8 也与 GGUF Q8 对比。

#### 表 1：SGLang 与 llama.cpp 的性能对比

模型 | 数据类型 | Socket 数 | llama.cpp TTFT (ms) | llama.cpp TPOT (ms) | SGLang TTFT (ms) | SGLang TPOT (ms) | TTFT 加速比 | TPOT 加速比
-- | -- | -- | -- | -- | -- | -- | -- | --
DeepSeek-R1-671B | INT8 | 2 | 24546.76 | 172.01 | 1885.25 | 67.99 | 13.0x | 2.5x
DeepSeek-R1-671B | FP8 | 2 | N/A | N/A | 2235.00 | 77.72 | 11.0x | 2.2x
Qwen3-235B-A22B | INT8 | 2 | 16806.34 | 214.9 | 1164.29 | 51.84 | 14.4x | 4.1x
Qwen3-235B-A22B | FP8 | 2 | N/A | N/A | 1340.62 | 55.88 | 12.5x | 3.8x
DeepSeek-R1-Distill-Llama-70B | INT8 | 2 | 20306.85 | 194.97 | 2637.84 | 76.53 | 7.7x | 2.5x
Llama-3.2-3B-Instruct | BF16 | 1 | 1659.94 | 55.35 | 268.2 | 16.98 | 6.2x | 3.3x

（请求数=1，输入/输出=1024/1024）

### 结果细拆

* TTFT 实现了 **6-14 倍**的性能提升。MoE 模型提升更大，因为 llama.cpp 中专家是顺序计算的，而我们通过对专家索引重排实现了专家间的并行。
* TPOT 实现了 **2-4 倍**的性能提升。由于解码阶段往往受内存带宽限制（memory bandwidth bound），TPOT 的加速比远小于 TTFT。
* 总体而言，在硬件能力范围内，我们的模拟 FP8 实现已达到最优效率。

## 局限与未来工作

虽然我们目前在 SGLang CPU 后端上的工作带来了显著的吞吐量提升，但仍存在一些局限和未来有待增强的方向：

* **启用图模式（Graph Mode）**：当并发请求数较少时，Python 开销会占用相当可观的时间。我们正在试验通过 `torch.compile` 的图模式消除 Python 开销。初步结果显示 TPOT 还能再提升 10%，该工作仍在进行中。
* **数据并行 MLA（Data Parallel MLA）**：当前的多 NUMA 并行遵循张量并行模式，会导致 KV 缓存在不同 rank 上被重复访问；GPU 上已有更高效的方案，即利用 DP 注意力（DP Attention）。
* **GPU/CPU 混合执行**：KTransformers 创新性地采用混合执行模式进行大型 MoE 模型推理，其中 MoE 层运行在 CPU 上、Attention 层运行在 GPU 上。我们正在 SGLang 上试验类似方案，并进一步将异构硬件上的各计算阶段流水线化。

## 总结

在本篇博客中，我们讲解了基于 SGLang 的纯 CPU 部署实现高性能的技术细节。相关工作已完全开源，并已合入 SGLang 主分支。我们将继续带来更多性能优化，不仅针对 CPU 后端，也覆盖其他 Intel® 平台。

## 致谢

在 SGLang 中实现 Intel® Xeon® 的适配与优化是一个重要的里程碑，为业界的大语言模型推理提供了新的替代方案。这离不开社区的深度协作与贡献。

我们衷心感谢：

* **SGLang 核心团队与社区贡献者**：Yineng Zhang、Jiexin Liang、[Mick](mickjagger19@icloud.com)、[Thien](https://github.com/gau-nernst)——感谢他们分享宝贵的想法、细致审阅 PR、对 RFC 提出深刻的反馈，以及扎实的代码贡献。
* **KTransformers 团队**：Mingxing Zhang——感谢他为 GPU/CPU 混合执行分享洞见与创新想法。

此外，我们 Intel PyTorch 团队的以下成员迎难而上，为这项工作做出了贡献：Mingfei Ma, Chunyuan Wu, Yanbing Jiang, Guobing Chen, Beilei Zheng, Jianan Gu, Zaili Wang, Hengyu Meng, Weiwen Xia, E Cao, Mingxu Zhang, Diwei Sun。

## 附录

### 相关 RFC 与 PR

[#2807](https://github.com/sgl-project/sglang/issues/2807), [#5150](https://github.com/sgl-project/sglang/pull/5150), [#6216](https://github.com/sgl-project/sglang/pull/6216), [#6339](https://github.com/sgl-project/sglang/pull/6339), [#6404](https://github.com/sgl-project/sglang/pull/6404), [#6405](https://github.com/sgl-project/sglang/pull/6405), [#6408](https://github.com/sgl-project/sglang/pull/6408), [#6419](https://github.com/sgl-project/sglang/pull/6419), [#6452](https://github.com/sgl-project/sglang/pull/6452), [#6456](https://github.com/sgl-project/sglang/pull/6456), [#6458](https://github.com/sgl-project/sglang/pull/6458), [#6493](https://github.com/sgl-project/sglang/pull/6493), [#6549](https://github.com/sgl-project/sglang/pull/6549), [#6614](https://github.com/sgl-project/sglang/pull/6614), [#6641](https://github.com/sgl-project/sglang/pull/6641), [#6657](https://github.com/sgl-project/sglang/pull/6657), [#6769](https://github.com/sgl-project/sglang/pull/6769), [#6770](https://github.com/sgl-project/sglang/pull/6770), [#6771](https://github.com/sgl-project/sglang/pull/6771), [#6833](https://github.com/sgl-project/sglang/pull/6833), [#7390](https://github.com/sgl-project/sglang/pull/7390), [#7462](https://github.com/sgl-project/sglang/pull/7462), [#7486](https://github.com/sgl-project/sglang/pull/7486), [#7647](https://github.com/sgl-project/sglang/pull/7647), [#7818](https://github.com/sgl-project/sglang/pull/7818), [#7838](https://github.com/sgl-project/sglang/pull/7838), [#7885](https://github.com/sgl-project/sglang/pull/7885)。

### 安装带 CPU 后端的 SGLang

```bash
# Clone the SGLang repository
git clone https://github.com/sgl-project/sglang.git
cd sglang/docker
 
# Build the docker image
docker build -t sglang-cpu:main -f Dockerfile.xeon .
 
# Initiate a docker container
docker run \
    -it \
    --privileged \
    --ipc=host \
    --network=host \
    -v /dev/shm:/dev/shm \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 30000:30000 \
    -e "HF_TOKEN=<secret>" \
    sglang-cpu:main /bin/bash
```

### 以 CPU 后端运行 SGLang

```bash
# Launch_server cmd:
# DeepSeek-R1-671B INT8:
SGLANG_CPU_OMP_THREADS_BIND='0-42|43-85|86-127|128-170|171-213|214-255' python3 -m sglang.launch_server --model meituan/DeepSeek-R1-Channel-INT8 --trust-remote-code --device cpu --disable-overlap-schedule --quantization w8a8_int8 --disable-radix-cache --tp 6 --mem-fraction-static 0.8 --max-total-tokens 63356
# DeepSeek-R1-671B FP8:
SGLANG_CPU_OMP_THREADS_BIND='0-42|43-85|86-127|128-170|171-213|214-255' python3 -m sglang.launch_server --model deepseek-ai/DeepSeek-R1 --trust-remote-code --device cpu --disable-overlap-schedule --disable-radix-cache --tp 6 --mem-fraction-static 0.8 --max-total-tokens 63356
# Qwen3-235B-A22B-INT8:
SGLANG_CPU_OMP_THREADS_BIND='0-42|43-85|86-127|128-170|171-213|214-255' python3 -m sglang.launch_server --model Qwen3-235B-A22B-INT8 --trust-remote-code --device cpu --disable-overlap-schedule --quantization w8a8_int8 --disable-radix-cache --tp 6 --mem-fraction-static 0.8 --max-total-tokens 63356
# Qwen3-235B-A22B-FP8:
SGLANG_CPU_OMP_THREADS_BIND='0-42|43-85|86-127|128-170|171-213|214-255' python3 -m sglang.launch_server --model Qwen/Qwen3-235B-A22B-FP8 --trust-remote-code --device cpu --disable-overlap-schedule --disable-radix-cache --tp 6 --mem-fraction-static 0.8 --max-total-tokens 63356
# RedHatAI--DeepSeek-R1-Distill-Llama-70B-quantized.w8a8:
SGLANG_CPU_OMP_THREADS_BIND='0-42|43-85|86-127|128-170|171-213|214-255' python3 -m sglang.launch_server --model RedHatAI/DeepSeek-R1-Distill-Llama-70B-quantized.w8a8 --trust-remote-code --device cpu --disable-overlap-schedule --quantization w8a8_int8 --disable-radix-cache --tp 6 --mem-fraction-static 0.8 --max-total-tokens 63356
# meta-llama--Llama-3.2-3B-Instruct:
SGLANG_CPU_OMP_THREADS_BIND='0-42|43-85|86-127' python3 -m sglang.launch_server --model meta-llama/Llama-3.2-3B-Instruct --trust-remote-code --device cpu --disable-overlap-schedule --disable-radix-cache --tp 3 --mem-fraction-static 0.8 --max-total-tokens 63356
# Serving cmd:
python3 -m sglang.bench_serving --dataset-path ShareGPT_V3_unfiltered_cleaned_split.json --dataset-name random --random-input 1024 --random-output 1024 --num-prompts 1 --request-rate inf --random-range-ratio 1.0 --max-concurrency 1 --host 127.0.0.1 --port 3000
```

**[注意]**：当前 CPU 原生后端仅支持具备 Intel® AMX 的 CPU，在其他 x86 平台上预期性能较慢。

### 产品与性能信息

测试环境：Intel(R) Xeon(R) 6980P，HT 开启，Turbo 开启，NUMA 6，集成加速器可用[已使用]：DLB [8]、DSA [8]、IAA[8]、QAT[on CPU, 8]，总内存 1536GB（24x64GB DDR5 12800 MT/s [8800 MT/s]），BIOS BHSDCRB1.IPC.3544.D02.2410010029，微码 0x11000314，CentOS Stream 9。Intel 于 2025 年 7 月 7 日测试。

### 声明与免责声明

性能因用途、配置和其他因素而异。更多信息请访问 Performance Index 网站。性能结果基于配置中所列日期的测试，可能无法反映所有已公开发布的更新。配置详情见备份。没有任何产品或组件是绝对安全的。您的成本和结果可能有所不同。Intel 技术可能需要启用相应的硬件、软件或服务激活。

Intel Corporation。Intel、Intel 标识及其他 Intel 商标均为 Intel Corporation 或其子公司的商标。其他名称和品牌可能是其各自所有者的财产。

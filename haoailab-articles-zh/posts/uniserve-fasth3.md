---
title: "FastVideo UniServe：在 NVIDIA Blackwell GPU 上为 FastH3 提供服务，延迟降低 1.8 倍、吞吐提升 1.45 倍"
title_en: "FastVideo UniServe: Production serving for FastH3 on NVIDIA Blackwell GPUs at 1.8x lower latency and 1.45x higher throughput"
date: 2026-09-29
source: https://haoailab.com/blogs/uniserve-fasth3/
crawled: 2026-11-16
translated: 2026-11-16
---

# FastVideo UniServe：在 NVIDIA Blackwell GPU 上为 FastH3 提供服务，延迟降低 1.8 倍、吞吐提升 1.45 倍

> 原文：[FastVideo UniServe: Production serving for FastH3 on NVIDIA Blackwell GPUs at 1.8x lower latency and 1.45x higher throughput](https://haoailab.com/blogs/uniserve-fasth3/) · Hao AI Lab @ UCSD

# FastVideo UniServe：在 NVIDIA Blackwell GPU 上为 FastH3 提供服务，延迟降低 1.8 倍、吞吐提升 1.45 倍

2026 年 9 月 29 日 · 25 分钟 · FastVideo Team

目录

* [结果一览](#results-at-a-glance)
* [背景：FastH3 工作负载](#background-the-fasth3-workload)
* [架构](#architecture)
* [预计算与调度相关的值](#precompute-schedule-dependent-values)
  + [预计算 AdaLN 调制](#precompute-adaln-modulation)
  + [文本 refiner 只跑一次](#run-the-text-refiner-once)
* [为 Ulysses 做按 head 分片的投影](#head-sharded-projections-for-ulysses)
* [DiT 中的 kernel 融合](#kernel-fusion-in-the-dit)
  + [融合的 attention 预处理](#fused-attention-preprocessing)
  + [融合的输出合并](#fused-output-combination)
  + [融合的调制、归一化与残差](#fused-modulation-normalization-and-residuals)
* [批处理、流式的解码路径](#a-batched-streaming-decode-path)
  + [把空间瓦片做成 batch，把时间单元分散到各卡](#batch-spatial-tiles-distribute-temporal-units)
  + [融合 VAE 解码器并以 CUDA graph 重放](#fuse-the-vae-decoder-and-replay-it-as-a-cuda-graph)
  + [GPU 仍在解码时就开始编码](#encode-while-the-gpu-is-still-decoding)
* [时间花在哪里](#where-the-time-goes)
* [NVFP4](#nvfp4)
* [用 NVIDIA Dynamo 提供服务](#serving-with-nvidia-dynamo)
* [部署 UniServe](#deploy-uniserve)
* [基准方法与完整结果](#benchmark-methodology-and-full-results)
  + [基线](#baselines)
  + [配置](#setup)
  + [延迟](#latency)
  + [吞吐](#throughput)
  + [NVFP4 对比 BF16](#nvfp4-against-bf16)
* [认识团队](#meet-the-team)
* [致谢](#acknowledgments)

[![](https://img.shields.io/github/stars/hao-ai-lab/UniServe?style=social)](https://github.com/hao-ai-lab/UniServe)

**TL;DR**

**FastVideo [UniServe](https://github.com/hao-ai-lab/UniServe) 是面向 FastH3 八步文本生成带音频视频的服务引擎（后续会有更多模型！），与我们的合作伙伴 [Nuva Lab](https://nuvalab.ai/) 和 [Reactor](https://www.reactor.inc/) 共同打造，面向生产级服务：**

* **Day 0 即生产可用。** UniServe 正在 [Reactor](https://www.reactor.inc/) 与 [Nuva Lab](https://nuvalab.ai/) 上承载生产 API 流量！
* **快于实时。** 在八张 NVIDIA GB200 GPU 上，由 1K token 提示词生成的一段 5 秒、1344×768 带音频片段，会在 3.1 秒后作为完成的 MP4 到达，10 秒片段为 6.2 秒（NVFP4 下 5.3 秒）。
* **吞吐。** 在八张 NVIDIA GB200 GPU 上每天约 11,000 个视频，在八张 RTX PRO 6000 GPU 上约 3,400 个，混合 5 至 15 秒片段：对应每秒生成视频消耗 6.4 与 21.2 GPU 秒。
* **最快的开源服务。** 在 1K token 提示词的 10 秒片段上，中位延迟比 FastVideo、vLLM-Omni 和 SGLang 低 1.2–1.8 倍，负载下吞吐高 15–45%。
* **硬件。** 已在 NVIDIA GB200、RTX PRO 6000 Blackwell 与 H200 上验证。NVFP4 PTQ 检查点在 Blackwell GPU 上运行，带来更低延迟与更高吞吐，质量下降极小。

![UniServe 与 FastVideo、vLLM-Omni、SGLang 在 1K token 提示词下 10 秒片段的延迟对比](img/results-at-a-glance.svg)

图 1. 在每种硬件配置上，1K token 提示词、10 秒片段的端到端中位延迟，一次一个请求。vLLM-Omni 没有八卡 GB200 的结果，因为一个副本无法跨两台节点。

FastH3 用八个去噪步把文本提示词变成一段带同步音轨的视频。每个请求要经过异构组件：文本编码器与 refiner、长序列多模态扩散 transformer（DiT）、视频与音频 VAE 解码器，以及 CPU 侧的视频编码与封装。它们有的跑在 GPU、有的跑在 CPU，并行方式与算术强度各不相同，因此一个更快的 attention kernel 只能加速请求的一部分。

因此 UniServe 优化的是整条请求路径。它削减 DiT 中稀疏 attention 周围的通信与访存流量，把 VAE 解码器批处理并融合，并在 GPU 仍在解码时就让 CPU 开始编码视频。

## 结果一览[#](#results-at-a-glance)

除另有说明外，所有系统都运行 FastH3 8-Step V2 检查点，文本编码与去噪用 BF16，视频解码器投影权重用 FP16。延迟为端到端测量：从提交请求起，直到客户端收到包含视频与音频的 MP4 的最后一个字节。

**延迟。** 对 1K token 提示词的 10 秒片段、一次一个请求，UniServe 的中位延迟在四张 GB200 GPU 上比基线低约 1.3 倍，在跨两台节点的八张 GB200 GPU 上低 1.3–1.8 倍，在八张 RTX PRO 6000 GPU 上低 1.2–1.4 倍。在八张 GB200 GPU 上，每种片段长度与提示词大小下中位请求都快于实时：1K token 提示词的 5 秒片段 3.1 秒，1K token 提示词的 10 秒片段 6.2 秒，10K token 提示词的 15 秒片段 14.1 秒。

![八张 GB200 GPU 上端到端延迟随片段长度的变化](img/realtime-gb200-8.svg)

图 2. 跨两台节点的八张 GB200 GPU 上，各片段长度的端到端中位延迟，一次一个请求。

**吞吐。** 负载下，UniServe 的最佳吞吐在四张 GB200 GPU 上比基线高 24–33%，八张 GB200 GPU 上高 15–22%，八张 RTX PRO 6000 GPU 上高 21–45%。对一个混合 5、10、15 秒片段的合成工作负载，这意味着四张 GB200 GPU 上每天约 6,100 个视频，八张上约 11,000 个，八张 RTX PRO 6000 GPU 上约 3,400 个（BF16 下），即每秒生成视频消耗 5.8、6.4 与 21.2 GPU 秒。

![负载下每 GPU 吞吐随延迟的变化](img/pareto.svg)

图 3. 每个点是一个并发级别：1、2、4、8 个并发请求，八卡上还有 16。两个副本时，一次一个请求会让一个副本空闲，因此第一个点到第二个点有跳跃。

**NVFP4。** FastVideo 的 NVFP4 检查点把 UniServe 的中位延迟再降低 10–15%，吞吐再提升 15–19%；[NVFP4](#nvfp4) 一节说明它量化了什么、改变了什么。[方法与完整结果](#benchmark-methodology-and-full-results)描述了工作负载与配置，并列出了每一个测量点。

## 背景：FastH3 工作负载[#](#background-the-fasth3-workload)

每个请求运行一个基于 Qwen3-VL 的文本编码器、一个两层文本 refiner、八次 50 层 DiT 前向，以及独立的视频与音频 VAE 解码器。DiT 在文本、视频、音频 token 拼接而成的联合序列上做 attention。

视频稀疏 attention（VSA）以 64 token 的瓦片为单位工作。文本与音频 query 关注所有 key。视频 query 关注全部文本与音频 key，以及得分最高的 20% 视频 key 瓦片（向上取整），另有一条对均值池化瓦片的粗粒度分支，其输出由一个学习到的门控加到精细输出上。UniServe 完整实现了这一模式。

在 1344 × 768、24 fps 下，1K token 提示词的 10 秒片段约 74K token（视频、音频与文本）。10K token 提示词的 15 秒片段约 119K。在这样的长度下，任何额外的全序列中间张量都会带来可观的访存流量。

## 架构[#](#architecture)

UniServe 把控制面、数值代码与执行资源分开。一个 Rust 服务器与引擎负责 HTTP API、准入控制、组件放置与批调度。Python GPU worker 运行模型并拥有全部执行资源：请求缓冲区、CUDA stream、传输与 CUDA graph。

![四张 GB200 GPU 上的 UniServe 架构](img/architecture.svg)

图 4. 实测的四卡部署在同一四张 GPU 上运行文本编码、去噪与媒体解码。四个 CPU worker 进程（host rank）把视频单元编码成 H.264，另一个独立的 host 进程编码音频并封装 MP4。

四张 GB200 GPU 的示例部署用四路张量并行（TP4）跑文本编码器，用四路 Ulysses 序列并行（SP4）跑 DiT。视频与音频解码器把时间单元（VAE 一起解码的那组 latent 帧）分散到同样四张 GPU 上。把每个组件单独放置很重要，因为文本编码器、长序列 DiT 与分瓦片的 VAE 解码器沿不同轴并行：提高 DiT 的序列并行度只能加速请求路径的一部分。

每个请求的条件信息占据一个预分配的请求槽，其 latent 在两个 page bank 中双缓冲：一个去噪步从一个 bank 读当前 latent，把下一个 latent 写进另一个 bank，批完成时运行时提交结果。CUDA graph 在启动时为每个形状桶捕获，并通过设备侧索引张量寻址请求槽与 latent page，于是同一桶内的每个请求都在自己的数据上重放同一批 graph。

扩散 runner 只按支持的最大形状分配一次工作区，较小的形状在该分配上的视图里运行。常量与各步 graph 常驻在 worker 自有的内存池中，因此服务一个请求既不会新分配工作区，也不会捕获新 graph。runner 为共享 scratch 内存的调用排序；worker 负责集合通信与资源生命周期。

## 预计算与调度相关的值[#](#precompute-schedule-dependent-values)

### 预计算 AdaLN 调制[#](#precompute-adaln-modulation)

每个 DiT block 把 timestep 嵌入投影为按模态区分的 shift、scale 与 gate 向量（AdaLN 调制）。它们只依赖权重与 timestep，不依赖提示词或 latent。由于检查点固定了它的八个 timestep，UniServe 在加载时计算好所有调制向量，只保留结果。

在 50 层、八个 step、视频与音频独立 timestep 下，BF16 表约 148 MiB。它所替代的投影权重在检查点中约占 **24 GiB**。UniServe 在加载时把那些权重流经预计算，随后释放它们。

### 文本 refiner 只跑一次[#](#run-the-text-refiner-once)

两层文本 refiner 只依赖编码后的提示词，不依赖 timestep。UniServe 每个请求只跑它一次，并在全部八次 DiT 前向中复用其输出。

## 为 Ulysses 做按 head 分片的投影[#](#head-sharded-projections-for-ulysses)

标准 Ulysses 序列并行从每张 GPU 持有一段序列开始。在 FastVideo 的 Ulysses 路径中，每张 GPU 对自己本地的 token 施加完整、复制的 Q、K、V 与 gate 投影；随后的 all-to-all 从序列分片切换到 head 分片，于是 attention 在本地 head 上看到完整序列。第二次 all-to-all 在输出投影之前切回序列分片。

UniServe 改变了这段数据流的前半部分。它按 attention head 分片 Q/K/V/gate 权重，all-gather 隐状态（比投影后的 Q/K/V/gate 张量更窄），并对它负责的 56 个 head 中的 14 个在整个序列上跑一次合并投影。本地行立即被投影。远端行通过分块异步 all-gather 到达，每个块一落地就进入投影与 attention 预处理，而后面的块仍在传输中。

![四张 GPU 之一上的投影与通信数据流](img/projection-dataflow-v2.svg)

图 5. 四张 GPU 之一。两条路径都计算完整的 token × head 乘积；区别在于哪个张量经过输入集合通信、每张 GPU 存哪些投影权重，以及传输如何与投影重叠。

对补齐后的序列长度 $S$、隐藏维度 $H=5376$、attention 宽度 $A=56 \times 128=7168$，每张 GPU 在输入集合通信中收到如下数量的 BF16 元素：

$$
\begin{aligned}
\text{Projected Q/K/V/gate exchange} &: \frac{3}{4}\frac{S}{4}(4A),\\
\text{Hidden-state gather} &: \frac{3S}{4}H.
\end{aligned}
$$

在 SP4 下，隐状态 all-gather 只搬运被投影 all-to-all 的 **75% 数据**，比例即 H/A。输出 all-to-all 不变。

按 head 分片还减少了权重显存。200 个 Q/K/V/gate 矩阵在复制时每张 GPU 约占 **14.4 GiB**，四路分片后每张 GPU 占 **3.6 GiB**。总投影 FLOPs 不变：工作从本地 token × 全部 head 重新划分为全部 token × 本地 head。

## DiT 中的 kernel 融合[#](#kernel-fusion-in-the-dit)

### 融合的 attention 预处理[#](#fused-attention-preprocessing)

未融合的路径把 Q/K RMSNorm、RoPE、收集有效行、填充 padding、瓦片池化与布局转置当作独立操作依次执行，每个被物化的全序列张量都多一次访存往返。

UniServe 的预处理 kernel 在每个被投影的块上，一趟完成学习到的 Q/K RMSNorm、部分 RoPE、对有效 token 的瓦片池化、瓦片打包与 gate 拷贝。它把精细 attention 的输入与 FP32 池化统计直接写进 attention kernel 要读的缓冲区。Padding 在该 kernel 内部处理，因此永远不会成为后续计算的输入。Top-k 瓦片选择与精细、粗粒度 attention kernel 仍各自独立。

该 kernel 每个块跑一次，而不是每个 transformer block 跑一次，因此预处理与通信重叠：all-gather 跑在独立的通信流上，计算流处理并准备一个块时，后面的块仍在传输中。更宽的融合也避免了未融合的 RMSNorm / RoPE / pack / pool / transpose 路径会物化的全序列中间张量。

![未融合的 attention 预处理与 UniServe 每块融合 kernel 的对比](img/fusion-preprocessing.svg)

图 6. 单张 GPU 上的 attention 预处理。未融合路径是一个概念基线，每个操作一个 kernel。UniServe 的 kernel 只读每个被投影的块一次，并写出瓦片选择、精细 attention、粗粒度分支与输出合并所读的每一个输入。

### 融合的输出合并[#](#fused-output-combination)

精细稀疏 attention 的输出与带门控的粗粒度输出按如下方式合并：

$$
O\_i = O\_i^{\mathrm{fine}} + G\_i \odot O\_{\mathrm{tile}(i)}^{\mathrm{compressed}}.
$$

UniServe 的合并 kernel 求值这个表达式，并把每一行直接写进输出 all-to-all 发送缓冲区中它对应的位置。这把合并与布局转换融合在一起，避免先物化一个合并张量再做 permute-and-copy。随后 all-to-all 恢复输出投影与残差路径所需的序列分片。

这条 all-to-all 同样是分块、异步的。合并 kernel 一次填满发送缓冲区的一个行区间，每个区间的 all-to-all 在其行写完后立即在通信流上启动。输出投影、门控残差与 MLP 随即消费已完成的区间，而后面的区间仍在传输中。

![输出合并写入 all-to-all 发送缓冲区并按行区间交换](img/fusion-output-exchange.svg)

图 7. 单张 GPU 上的输出合并与交换。UniServe 把每个行区间直接组合到目标 GPU 的发送缓冲区槽位，并立即启动该区间的 all-to-all；一个区间的输出投影与 MLP 在其交换落地时开始。时间线只表示顺序，不表示时长。

### 融合的调制、归一化与残差[#](#fused-modulation-normalization-and-residuals)

每个 block 围绕 RMSNorm 施加 AdaLN 调制，并做一次门控残差更新。示意地说，attention 输入是 `RMSNorm(x) * (1 + scale_attn) + shift_attn`。attention 之后，残差变为 `r = x + gate_attn * attention_output`，而 MLP 输入是 `r` 的调制 RMSNorm。

UniServe 融合这些步骤。pre-attention kernel 在归一化的同时，按 token 的模态与当前 timestep 查它的调制行，并在块到达的同一趟里保存残差输入。post-attention kernel 同时产出带门控的残差和调制、归一化后的 MLP 输入。一个带 SwiGLU 的融合 gate/up 投影喂给 down 投影，随后是 MLP 的门控残差更新。在 BF16 路径中，已完成的块直接流入下一阶段，无需先拼接整个分片。

![单个 DiT block 的 AdaLN 调制、归一化与残差 kernel](img/fusion-modulation.svg)

图 8. 单个 DiT block 中的 AdaLN 调制、归一化与残差。UniServe 在归一化 kernel 内部读取每个 token 预计算好的调制行，并在同一趟里写出残差与下一阶段的输入。

## 批处理、流式的解码路径[#](#a-batched-streaming-decode-path)

### 把空间瓦片做成 batch，把时间单元分散到各卡[#](#batch-spatial-tiles-distribute-temporal-units)

视频 VAE 解码器从相互重叠的空间瓦片重建每个时间单元。在 1344 × 768 下瓦片网格为 4 × 7：28 个瓦片，最小瓦片边长 256 像素、重叠 64 像素。直白的实现会遍历瓦片，每个瓦片调用一次解码器。并行化 DiT 并不会动到这个循环：在朴素基线的 trace 中，所有视频解码 kernel 仍跑在 GPU 0 上。

UniServe 把一个时间单元的 28 个瓦片沿 batch 维拼接，一次调用解完，然后恢复网格并混合重叠区。瓦片在 batch 中是彼此独立的样本。worker 把时间单元分散到四张 GPU 上。

![空间批处理与时间单元放置](img/media-placement.svg)

图 9. 对四个时间单元，UniServe 发起四次 batch-28 的解码调用。FastVideo 把时间单元分散到各 GPU，但仍在它们的空间瓦片上循环。SGLang 与 vLLM-Omni 把每个单元的空间瓦片分散到各 GPU。

对 10 秒样本的 14 个时间单元，trace 显示 **UniServe 中只有 14 次解码器调用**，而 FastVideo 与 SGLang 是**每个瓦片各 392 次调用**。每次批处理调用把一个时间单元的主机侧启动开销摊薄。

### 融合 VAE 解码器并以 CUDA graph 重放[#](#fuse-the-vae-decoder-and-replay-it-as-a-cuda-graph)

批处理与 VAE 解码器内部的 kernel 融合相叠加。UniServe 的视频解码 transformer 把 Q/K 归一化与 RoPE 融合，把带缩放的 attention 残差与随后的 RMSNorm 融合，并把每个 MLP 的残差加法推迟到下一层的归一化中；最后一层把它待做的加法折叠进输出 LayerNorm。归一化读取 FP32 的残差和，因此 FP16 投影权重不会把残差流舍入到 FP16。SwiGLU 与最后的 unpatchify 步骤（把 token 变回像素）各有自己的融合 kernel。

worker 把批处理解码捕获成 CUDA graph，并对每个时间单元重放。捕获整个批处理解码消除了每个请求启动数千个小 kernel 的主机往返。

视频解码在 **UniServe 的 GPU 上约 1.1 秒，在 FastVideo 中为 4.8 秒**。UniServe 在这段时间的几乎全部里让 GPU 保持忙碌；FastVideo 的 4.8 秒里有很大一部分花在等主机。

### GPU 仍在解码时就开始编码[#](#encode-while-the-gpu-is-still-decoding)

像素重建完成并不等于视频请求结束。UniServe 把每个解码出的 RGB 单元拷贝到主机内存，并独立于剩余的 GPU 解码来调度它的编码。在同一台主机上，编码器直接读取已发布的主机缓冲区，而不是再复制一份。四个 CPU 编码进程用 libx264 编码各单元，同时 GPU 继续解码。音频解码器产出 PCM，由主机编码成 AAC。muxer 追加已编码的视频包并调整时间戳、加上音轨，而不解码或重编码任何视频。

trace 显示这种重叠：后面的单元还在解码时编码就已开始，完整的 MP4 在最后一个视频 kernel 之后约 **100 ms** 到达。

vLLM-Omni 提供类似的可选项 `preencode_mp4`，在 worker 上编码每个已解码块，同时后面的块仍在解码；下面的 vLLM-Omni 基准结果使用了它。FastVideo 与 SGLang 在解码结束后才编码 MP4。

## 时间花在哪里[#](#where-the-time-goes)

以下 trace 都在四张 GB200 GPU 上、一次一个请求、预热之后，使用同样的 10 s/1K 提示词与 seed。

![五个系统的完整请求时间线](img/request-timeline-10s-1k.svg)

图 10. 所有面板共享同一时间轴，从请求提交开始。虚线标记完整 MP4 的接收。GPU 柱跨越四张 GPU 上从第一个到最后一个相关 kernel，包括空闲间隙。主机输出柱可以与 GPU 工作重叠，并包含这些函数内部的格式转换。

| 10 s/1K 请求，秒 | 文本编码器（GPU） | Refiner + 去噪（GPU） | 解码（GPU） | 端到端，已 profile | 端到端，未 profile |
| --- | --- | --- | --- | --- | --- |
| UniServe | 0.020 | 10.052 | 1.107 | 11.414 | 11.341 |
| FastVideo | 0.113 | 11.723 | 4.953 | 17.735 | 16.496 |
| SGLang | 0.161 | 11.111 | 5.318 | 17.215 | 16.089 |
| vLLM-Omni | 0.119 | 12.580 | 3.940 | 17.018 | 16.116 |
| Naive | 0.112 | 15.752 | 25.346 | 42.622 | 34.315 |

*解码包含视频解码、音频解码与最后的重建步骤；不包含输出编码器所做的 GPU 帧格式转换。未 profile 列是 trace 开始前的一个预热请求。*

## NVFP4[#](#nvfp4)

上述优化改变的是同一计算在何处、何时运行。精度是另一个选择，在服务器启动时按组件设置。默认预设 `quality` 让 DiT 与文本编码器跑 BF16、视频解码器投影跑 FP16；本文的 BF16 结果都使用它。`balanced` 把视频解码器的投影存为 NVFP4。`performance` 还让 DiT MLP 跑 FP8，`maximum` 让它跑 NVFP4 并用 FP8 文本编码器；每个预设中 attention 都保持 BF16。

为了更快，我们还发布了 NVFP4[1](#fn:1) 训练后量化（PTQ）检查点 `FastVideo/FastVideo-FastH3-8-Step-V2-NVFP4`，UniServe 可原生服务它。

该检查点量化 150 个 DiT MLP 投影（50 层各含 gate、up、down）和 252 个视频 VAE 解码器投影（36 层各含 Q/K/V、attention 输出与三个 MLP 投影）。文本编码器与 DiT 的 attention 投影保持 BF16。UniServe 按存储形态加载打包权重——每字节两个 E2M1 值加 block scale——并用检查点中每个模块标定好的全局 scale 即时量化激活，于是无论序列如何切分，每一块行都使用同一 scale。打包值与 block scale 直接进入一个产出 BF16 输出的 block-scaled FP4 GEMM。

在一个 10 s/1K 请求上，GPU 0 上的 DiT 时间从 BF16 的 10.2 秒降到 8.5 秒，视频解码器从 1.2 秒降到 0.8 秒。端到端，NVFP4 在三种硬件配置上把 UniServe 的中位延迟降低约 10–15%，吞吐提高 15–19%；见 [NVFP4 对比 BF16](#nvfp4-against-bf16)。

下面这些片段对比了 UniServe 的 BF16（左）与 NVFP4（右）在相同基准请求上的输出，均为 10 秒、1K token 提示词，来自八卡 RTX PRO 6000 的延迟测试。

[![](img/videos/market-poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/uniserve-fasth3--img--videos--market-side-by-side.mp4)

市场：BF16（左）与 NVFP4（右）。

[![](img/videos/percussion-poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/uniserve-fasth3--img--videos--percussion-side-by-side.mp4)

打击乐表演：BF16（左）与 NVFP4（右）。

[![](img/videos/river-poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/uniserve-fasth3--img--videos--river-side-by-side.mp4)

河流：BF16（左）与 NVFP4（右）。

[![](img/videos/ceramics-poster.jpg)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/uniserve-fasth3--img--videos--ceramics-side-by-side.mp4)

陶艺工作室：BF16（左）与 NVFP4（右）。

## 用 NVIDIA Dynamo 提供服务[#](#serving-with-nvidia-dynamo)

UniServe 还可以作为 [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) 的实验性后端运行。Dynamo 的前端提供 OpenAI 风格的 `/v1/videos` 端点，并负责服务发现与请求路由。

`uniserve-dynamo-worker` 把 UniServe 的调度器嵌进一个 Dynamo worker，并通过 Dynamo 的 `/v1/videos` 端点服务 FastH3。[Dynamo 快速上手](https://github.com/hao-ai-lab/UniServe/blob/3cca4caafd7a8b3cdf841b625509b0c1c8edf6c1/docs/fast_h3/dynamo.md)展示了如何在四张 GB200 GPU 上运行它。

## 部署 UniServe[#](#deploy-uniserve)

按其 [README](https://github.com/hao-ai-lab/uniserve#install) 安装 UniServe，然后选择一个模型和 GPU，得到部署文件与服务命令。[服务指南](https://github.com/hao-ai-lab/uniserve/blob/main/docs/minimax_h3/minimax_h3.md)涵盖了其它所有选项。

模型

GPU

GPU 数

优化目标

检查点

精度

最长片段

最长提示词

参考素材尺寸

部署文件

随 UniServe 提供；传给 `--workers`。复制下载

## 基准方法与完整结果[#](#benchmark-methodology-and-full-results)

本节说明我们如何测量，并列出图表背后的每一个结果。

### 基线[#](#baselines)

我们把 UniServe 与两类基线比较。

**朴素（Naive）。** 为了展示 UniServe 各项优化的贡献，我们从固定版本的 FastVideo 实现构建了一个朴素基线。它已包含标准优化：Ulysses SP4 去噪、TP4 文本编码、权重常驻、原生 VSA kernel、每请求一次文本 refiner 前向，以及 FP16 VAE 解码器投影。FastVideo 的可选融合、`torch.compile`、AdaLN 预计算与并行 VAE 解码被关闭。

**调优（Tuned）。** FastVideo、vLLM-Omni 与 SGLang 各自运行同一检查点的快速配置：GB200 上的原生 SM100a VSA、GPU 权重常驻，以及相同的 libx264 编码设置。[配置](#setup)列出各系统的具体设置。本文其它地方提到“基线”时，指的是这三个调优系统。

### 配置[#](#setup)

**硬件。**（1）单节点内 4 × GB200 GPU；（2）跨两台节点、由多节点 NVLink（MNNVL）连接的 8 × GB200 GPU；（3）单节点内 8 × RTX PRO 6000 Blackwell Server Edition GPU。

**系统与检查点。** 每个系统都服务 BF16 检查点 `FastVideo/FastVideo-FastH3-8-Step-V2`，其中只有 UniServe 还额外服务 NVFP4 检查点 `FastVideo/FastVideo-FastH3-8-Step-V2-NVFP4`。所有系统都运行完整的八步调度、检查点自带的稀疏 attention，以及完整的视频与音频解码器。编译、融合 kernel、并行与媒体处理重叠都在考察范围内。

| 系统 | 检查点 | 4 x GB200 | 8 x GB200，两节点 | 8 x RTX PRO 6000 |
| --- | --- | --- | --- | --- |
| UniServe | BF16、NVFP4 | 支持 | 支持 | 支持 |
| FastVideo | BF16 | 支持 | 支持 | 支持 |
| vLLM-Omni | BF16 | 支持，原生 SM100a VSA | 仅吞吐布局，原生 SM100a VSA† | 支持，Triton VSA |
| SGLang | BF16 | 支持，原生 SM100a VSA | 支持，原生 SM100a VSA | 支持，Triton VSA |
| FastVideo、vLLM-Omni、SGLang | NVFP4 | 不适用 | 不适用 | 不适用 |

*支持的配置。在 GB200 上，vLLM-Omni 与 SGLang 使用原生 SM100a VSA kernel。† vLLM-Omni 无法让一个副本跨两台主机，因此没有八卡 GB200 的延迟结果。NVFP4 仅 UniServe 支持：其它系统不能原生加载该检查点。*

**布局。** 我们只调优一次布局，然后对每个系统固定：

| 硬件 | 延迟布局 | 吞吐布局 |
| --- | --- | --- |
| 4 x GB200 | `r1s4`，文本编码器 TP4 | `r1s4`，文本编码器 TP4 |
| 8 x GB200，两节点 | `r1s8`，文本编码器 TP8 | `r2s4`，每节点一个副本，文本编码器 TP4 |
| 8 x RTX PRO 6000 | `r1s8`，文本编码器 TP8 | `r2s4`，文本编码器 TP4 |

*布局。* `r` *是副本数，* `s` *是 DiT 的序列并行度；文本编码器在每个副本的各 GPU 上做张量并行。*

**基线配置。** 在同一布局内，每个系统都把 DiT 权重常驻在 GPU 上，不卸载到主机内存，也不做张量并行分片。每个系统还都在其副本内对文本编码器做张量并行、把视频 VAE 解码器投影保持在 FP16、不加载文本生成视频用不到的组件，并用 libx264 `ultrafast` 编码 H.264。差异设置如下：

| 设置 | UniServe | FastVideo | vLLM-Omni | SGLang |
| --- | --- | --- | --- | --- |
| 固定调度的 AdaLN 调制 | 加载时预计算 | 加载时预计算 | 加载时预计算 | 首次使用时预计算 |
| 编译 | GB200 上的四卡副本用 CUDA graph；八卡副本与 RTX PRO 6000 上用 eager | DiT：GB200 上区域性 `torch.compile`（需要 SM100a kernel）；VAE 解码器在所有硬件上编译 | 区域性 `torch.compile` | 无：eager，因为 SGLang 的 VSA-H3 校验拒绝 `torch.compile` 与可打断的 CUDA graph |
| MP4 编码 | 主机 worker，与解码重叠 | 解码之后 | 在 worker 上，与解码重叠（`preencode_mp4`） | 解码之后 |

*各布局内各系统的差异设置。*

**工作负载。** 六个场景族，每族一个 1K token 与一个 10K token 提示词，片段长度 5、10、15 秒。提示词、seed 与执行顺序对每个系统相同。

**指标。** 延迟为并发 1 下的 72 个请求（六个场景 × 两种提示词长度 × 三种时长 × 两个 seed）。我们报告全部 72 个请求的 p50 / p90 / p95，以及每种形状 12 个请求的中位数。吞吐为每个并发级别 32 个请求（C = 1、2、4、8，八卡上还有 16），从第一次提交到最后一个响应按每秒有效 MP4 计数。

### 延迟[#](#latency)

![每种硬件配置上各形状的中位延迟](img/latency-per-shape.svg)

图 11. 各形状在一次一个请求下的端到端中位延迟。同一行的两个面板共享 y 轴。下方折叠表格列出每一个值。

**四张 GB200 GPU。** **在 72 请求的工作负载上，UniServe BF16 的端到端中位延迟为 14.24 秒，而 SGLang 为 17.80 秒、FastVideo 为 18.17 秒、vLLM-Omni 为 18.83 秒。** 在六种形状上，SGLang 的中位数是 UniServe 的 1.18 至 1.30 倍，FastVideo 为 1.23 至 1.33 倍，vLLM-Omni 为 1.28 至 1.37 倍。

四张 GB200 GPU 上的端到端延迟

| 系统 | 精度 | p50（秒） | p90（秒） | p95（秒） | 有效 / 尝试 |
| --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **14.24** | **27.30** | **27.32** | 72 / 72 |
| FastVideo | BF16 | 18.17 | 33.62 | 33.77 | 72 / 72 |
| vLLM-Omni | BF16 | 18.83 | 34.89 | 34.94 | 72 / 72 |
| SGLang | BF16 | 17.80 | 32.59 | 32.76 | 72 / 72 |
| UniServe | NVFP4 | **12.15** | **24.16** | **24.27** | 72 / 72 |

| 系统 | 精度 | 5 s / 1K | 5 s / 10K | 10 s / 1K | 10 s / 10K | 15 s / 1K | 15 s / 10K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **5.62** | **8.80** | **11.73** | **16.75** | **20.27** | **27.31** |
| FastVideo | BF16 | 7.47 | 10.87 | 15.65 | 20.65 | 26.35 | 33.70 |
| vLLM-Omni | BF16 | 7.69 | 11.34 | 15.93 | 21.47 | 26.84 | 34.90 |
| SGLang | BF16 | 7.07 | 10.35 | 15.23 | 20.43 | 25.44 | 32.59 |
| UniServe | NVFP4 | **4.49** | **7.48** | **9.67** | **14.46** | **17.32** | **24.18** |

*四张 GB200 GPU（*`r1s4`*）上的端到端延迟：全部 72 个请求的分位数（上表）与各形状的中位数、每个 12 个请求、单位秒（下表）。*

**跨两台节点的八张 GB200 GPU。** 用一个跨两台节点的八卡副本时，**UniServe BF16 的中位延迟为 7.51 秒，比其四卡中位数低 47%，而 SGLang 为 9.79 秒、FastVideo 为 13.02 秒**。SGLang 的各形状中位数是 UniServe 的 1.24 至 1.35 倍，FastVideo 为 1.52 至 1.88 倍。

跨两台节点的八张 GB200 GPU 上的端到端延迟

| 系统 | 精度 | p50（秒） | p90（秒） | p95（秒） | 有效 / 尝试 |
| --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **7.51** | **14.09** | **14.12** | 72 / 72 |
| FastVideo | BF16 | 13.02 | 23.58 | 24.39 | 72 / 72 |
| vLLM-Omni | BF16 | 不适用 |  |  |  |
| SGLang | BF16 | 9.79 | 17.46 | 17.59 | 72 / 72 |
| UniServe | NVFP4 | **6.56** | **12.53** | **12.60** | 72 / 72 |

| 系统 | 精度 | 5 s / 1K | 5 s / 10K | 10 s / 1K | 10 s / 10K | 15 s / 1K | 15 s / 10K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **3.13** | **4.74** | **6.25** | **8.76** | **10.55** | **14.11** |
| FastVideo | BF16 | 5.37 | 7.19 | 11.38 | 13.54 | 19.86 | 23.97 |
| SGLang | BF16 | 4.22 | 6.02 | 8.38 | 10.99 | 13.88 | 17.51 |
| UniServe | NVFP4 | **3.05** | **4.15** | **5.35** | **7.62** | **9.13** | **12.54** |

*跨两台节点的八张 GB200 GPU（*`r1s8`*）上的端到端延迟。*

**八张 RTX PRO 6000 GPU。** **UniServe BF16 的中位延迟为 35.57 秒，而 SGLang 为 43.38 秒、FastVideo 为 49.76 秒、vLLM-Omni 为 51.35 秒。** 优势随时长与提示词长度增长。对 1K token 提示词的 5 秒视频，SGLang 的中位数是 UniServe 的 0.96 倍——SGLang 快 0.85 秒；对 10K token 提示词的 15 秒视频则是 1.30 倍。FastVideo 的比值范围为 1.15 至 1.45，vLLM-Omni 为 1.12 至 1.55。在此硬件上没有任何系统使用 SM100a kernel：UniServe 运行 FlashInfer 的 SM120 block-sparse attention kernel，其它系统运行各自的 Triton VSA kernel。

八张 RTX PRO 6000 GPU 上的端到端延迟

| 系统 | 精度 | p50（秒） | p90（秒） | p95（秒） | 有效 / 尝试 |
| --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **35.57** | **58.72** | **58.75** | 72 / 72 |
| FastVideo | BF16 | 49.76 | 85.03 | 85.18 | 72 / 72 |
| vLLM-Omni | BF16 | 51.35 | 91.13 | 91.24 | 72 / 72 |
| SGLang | BF16 | 43.38 | 76.49 | 76.53 | 72 / 72 |
| UniServe | NVFP4 | **32.15** | **53.54** | **53.54** | 72 / 72 |

| 系统 | 精度 | 5 s / 1K | 5 s / 10K | 10 s / 1K | 10 s / 10K | 15 s / 1K | 15 s / 10K |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | 19.12 | **24.51** | **31.39** | **39.80** | **47.52** | **58.72** |
| FastVideo | BF16 | 21.97 | 31.31 | 42.53 | 55.87 | 67.95 | 85.12 |
| vLLM-Omni | BF16 | 21.44 | 33.28 | 43.45 | 59.16 | 70.21 | 91.15 |
| SGLang | BF16 | **18.27** | 27.10 | 37.09 | 49.71 | 60.36 | 76.50 |
| UniServe | NVFP4 | **17.39** | **22.54** | **28.15** | **36.15** | **42.61** | **53.54** |

*八张 RTX PRO 6000 GPU（*`r1s8`*）上的端到端延迟。*

### 吞吐[#](#throughput)

![每种硬件配置在各并发下的吞吐](img/throughput-concurrency.svg)

图 12. 各并发下每秒有效视频数。在四张 GB200 GPU 上，FastVideo 与 vLLM-Omni 的曲线重叠。下方折叠表格列出每个值及其 p50 与 p95 延迟。

在四张 GB200 GPU、单副本下，每个系统的吞吐在各并发级别上基本持平：更高并发只增加排队延迟而不增加吞吐。**在各系统最佳并发下，UniServe BF16 的吞吐比 SGLang 高 24.0%，比 vLLM-Omni 高 32.6%，比 FastVideo 高 32.7%。** 八卡上的两个副本时，C=1 会让一个副本空闲，从 C=2 起两个都在忙。**在两台 GB200 节点上，UniServe BF16 达到 0.1283 视频/秒，比 SGLang 最佳（C=8 时 0.1117 视频/秒）高 14.9%，比 FastVideo（C=4 时 0.1067 视频/秒）高 20.3%，比 vLLM-Omni（C=8 时 0.1052 视频/秒）高 22.0%。** 在 RTX PRO 6000 上，**UniServe BF16 达到 0.0389 视频/秒，比 SGLang 最佳（C=4 时 0.0322 视频/秒）高 20.8%，比 FastVideo（C=4 时 0.0278 视频/秒）高 39.9%，比 vLLM-Omni（C=4 时 0.0267 视频/秒）高 45.4%**。下方每个单元格给出一次 32 请求运行的吞吐（每秒有效视频数）及其后的 p50 / p95 端到端延迟（秒）。

四张 GB200 GPU 上负载下的吞吐与延迟

| 系统 | 精度 | C=1 | C=2 | C=4 | C=8 |
| --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **0.0702 (11.6 / 26.6)** | **0.0708 (30.4 / 45.6)** | **0.0705 (54.0 / 74.8)** | **0.0707 (104.8 / 140.5)** |
| FastVideo | BF16 | 0.0531 (16.1 / 34.0) | 0.0532 (37.4 / 55.1) | 0.0534 (74.2 / 90.9) | 0.0531 (141.0 / 173.7) |
| vLLM-Omni | BF16 | 0.0533 (15.8 / 34.2) | 0.0534 (39.6 / 55.3) | 0.0534 (74.2 / 97.9) | 0.0532 (143.5 / 170.9) |
| SGLang | BF16 | 0.0567 (15.0 / 31.8) | 0.0571 (36.8 / 52.0) | 0.0571 (69.5 / 89.6) | 0.0571 (133.7 / 160.3) |
| UniServe | NVFP4 | **0.0819 (9.5 / 23.7)** | **0.0824 (24.4 / 40.0)** | **0.0824 (46.9 / 64.0)** | **0.0823 (90.3 / 120.9)** |

*四张 GB200 GPU（*`r1s4`*）上负载下的吞吐与延迟。*

跨两台节点的八张 GB200 GPU 上负载下的吞吐与延迟

| 系统 | 精度 | C=1 | C=2 | C=4 | C=8 | C=16 |
| --- | --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **0.0692 (11.7 / 27.3)** | **0.1223 (12.4 / 34.0)** | **0.1251 (29.4 / 49.0)** | **0.1283 (53.1 / 78.6)** | **0.1186 (118.4 / 151.7)** |
| FastVideo | BF16 | 0.0506 (20.6 / 33.8) | 0.1039 (15.7 / 33.7) | 0.1067 (36.2 / 54.3) | 0.1042 (68.7 / 101.7) | 0.0958 (114.3 / 182.2) |
| vLLM-Omni | BF16 | 0.0529 (16.0 / 34.6) | 0.1021 (15.9 / 34.3) | 0.1043 (37.0 / 55.3) | 0.1052 (70.9 / 111.7) | 0.1023 (136.8 / 167.0) |
| SGLang | BF16 | 0.0564 (15.3 / 32.6) | 0.1079 (15.2 / 32.7) | 0.1111 (34.7 / 51.4) | 0.1117 (63.0 / 93.7) | 0.1002 (106.5 / 173.5) |
| UniServe | NVFP4 | **0.0804 (9.7 / 24.3)** | **0.1420 (9.7 / 34.6)** | **0.1437 (25.2 / 42.2)** | **0.1467 (46.3 / 68.5)** | **0.1480 (92.3 / 119.7)** |

*跨两台节点的八张 GB200 GPU（*`r2s4`*）上负载下的吞吐与延迟。*

八张 RTX PRO 6000 GPU 上负载下的吞吐与延迟

| 系统 | 精度 | C=1 | C=2 | C=4 | C=8 | C=16 |
| --- | --- | --- | --- | --- | --- | --- |
| UniServe | BF16 | **0.0207 (39.7 / 86.2)** | **0.0389 (39.7 / 88.2)** | **0.0389 (97.8 / 131.3)** | **0.0362 (186.0 / 274.9)** | **0.0359 (379.2 / 499.2)** |
| FastVideo | BF16 | 0.0138 (61.9 / 129.2) | 0.0271 (58.7 / 129.2) | 0.0278 (140.3 / 210.8) | 0.0269 (266.7 / 415.7) | 0.0270 (413.2 / 706.0) |
| vLLM-Omni | BF16 | 0.0135 (58.9 / 139.5) | 0.0260 (59.0 / 139.5) | 0.0267 (144.9 / 225.4) | 0.0263 (273.8 / 419.9) | 0.0260 (475.8 / 794.6) |
| SGLang | BF16 | 0.0163 (50.0 / 114.3) | 0.0313 (49.9 / 114.6) | 0.0322 (120.7 / 185.1) | 0.0317 (227.6 / 345.4) | 0.0289 (368.1 / 616.3) |
| UniServe | NVFP4 | **0.0244 (32.6 / 74.8)** | **0.0442 (33.7 / 75.0)** | **0.0461 (80.5 / 110.8)** | **0.0412 (170.2 / 264.7)** | **0.0434 (320.5 / 399.2)** |

*八张 RTX PRO 6000 GPU（*`r2s4`*）上负载下的吞吐与延迟。*

### NVFP4 对比 BF16[#](#nvfp4-against-bf16)

| 硬件 | BF16 p50（秒） | NVFP4 p50（秒） | 延迟变化 | BF16 最佳（视频/秒） | NVFP4 最佳（视频/秒） | 吞吐变化 |
| --- | --- | --- | --- | --- | --- | --- |
| 4 x GB200 | 14.24 | 12.15 | −14.7% | 0.0708 | 0.0824 | +16.4% |
| 8 x GB200 | 7.51 | 6.56 | −12.6% | 0.1283 | 0.1480 | +15.4% |
| 8 x RTX PRO 6000 | 35.57 | 32.15 | −9.6% | 0.0389 | 0.0461 | +18.6% |

*同一布局下的 UniServe BF16 与 NVFP4。NVFP4 是独立的精度层级；见 [NVFP4](#nvfp4)。*

## 认识团队[#](#meet-the-team)

**Yi Sun**

  
**Will Lin**

  
**Hao Zhang**

## 致谢[#](#acknowledgments)

FastVideo FastH3 构建于 [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) 之上。感谢 MiniMax 团队发布权重与代码。

感谢 [Nuva Lab](https://nuvalab.ai/) 与 [Reactor](https://www.reactor.inc/) 在 UniServe 开发过程中的协作、反馈与洞见，以及 Nuva Lab 提供我们基准测试所用的生产硬件。

感谢 Guan Luo、Qi Wang、Ryan McCormick、Harry Kim 以及 [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) 团队的其它成员，支持我们把 Dynamo 与 UniServe 集成，让 UniServe 更接近生产级服务引擎。

我们也感谢 [NVIDIA FastGen](https://github.com/NVlabs/FastGen)（Julius Berner、Chao Liu、Arash Vahdat）以及 NVIDIA Enterprise Products（Pengcheng Li、Cliff Woolley）团队在 [FastH3](/blogs/fasth3-preview/) 上的协作。

最后，我们非常感谢 [vLLM 项目](https://vllm.ai/)、[NVIDIA](https://www.nvidia.com/en-us/) 与 [MBZUAI](https://mbzuai.ac.ae/) 对 FastVideo 的长期赞助与支持。

---

1. NVFP4 是在 Blackwell GPU 上有原生 tensor core 支持的 4-bit 浮点格式。它存储 E2M1 值，每 16 个元素一个 FP8（E4M3）scale，每个张量一个 FP32 scale。[↩︎](#fnref:1)

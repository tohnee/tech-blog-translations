---
title: "SGLang Day-0 支持 MiMo-V2-Flash 模型"
title_en: "SGLang Day-0 Support for MiMo-V2-Flash Model"
author: "SGLang Team and Xiaomi LLM Core Team"
date: "December 16, 2025"
previewImg: /images/blog/mimo-v2-flash/decode_1.png
source: https://lmsys.org/blog/2025-12-16-mimo-v2-flash/
translated: 2026-09-12
---

# SGLang Day-0 支持 MiMo-V2-Flash 模型

> 原文：[SGLang Day-0 Support for MiMo-V2-Flash Model](https://lmsys.org/blog/2025-12-16-mimo-v2-flash/) · LMSYS Blog · SGLang Team and Xiaomi LLM Core Team

## 引言
[XiaomiMiMo/MiMo-V2-Flash](https://huggingface.co/XiaomiMiMo/MiMo-V2-Flash) 总参数量 309B、激活参数量 15B，是一款以推理为中心、旨在最大化解码效率的新模型。它基于两项关键设计：**滑窗注意力（SWA）**与**多层 MTP**。MiMo-V2-Flash 明确面向真实推理服务负载进行了协同设计，可以在不同硬件上灵活地在吞吐量与延迟之间做权衡。结合 SGLang 优化过的 Spec v2 运行时——它以近乎零开销的方式支持多层 MTP，并能高效执行 SWA——MiMo-V2-Flash 在 H200 上实现了 TPOT 与吞吐量的均衡表现。本篇博客将介绍该模型以及 SGLang 为其提供的高效支持。

## 面向推理效率的模型设计
MiMo-V2-Flash 的设计遵循推理效率优先的原则，采用了两项关键设计：

1. 滑窗注意力（SWA）：在 SWA 中，每个 token 的感受野被限制在一个固定大小的窗口内，以降低注意力在序列维度上的复杂度。
2. MTP：MiMo-V2-Flash 的多层 MTP 使用一串预测头（prediction heads），每个头按顺序预测下一个 token；得到的草稿 token 随后在下一步中通过扩展后的查询（query）并行验证。
MiMo-V2-Flash 的整体架构如下图所示：

![figure1](/images/blog/mimo-v2-flash/overview.PNG)<small><center>MiMo-V2-Flash 整体架构</center></small>

下面我们来看看这些设计如何带来高性价比的推理。

### SWA
在 MiMo-V2-Flash 中，每五个采用滑窗模式的注意力层与一个稠密 GQA 层交替排列。SWA 的广泛使用能从多个方面改善推理表现。首先，在预填充（prefill）阶段，计算是主要成本；尤其是当序列很长时，$O(N^2)$ 的注意力计算会成为瓶颈。SWA 把 $O(N^2)$ 的复杂度降为与序列长度呈线性关系的 $O(Nw)$，其中 $w$ 是窗口大小。在长上下文场景下，这一设计可以显著降低首 token 延迟（TTFT）。SWA 还将 KV 缓存的开销降到了常量级别——为更大的批大小释放了更多资源，同时凭借更少的 KV 缓存加载操作获得更好的 TPOT。

下图展示了 MiMo-V2-Flash 的预填充基准测试结果。

![figure2](/images/blog/mimo-v2-flash/prefill.PNG)<small><center>MiMo-V2-Flash 预填充基准测试（禁用基数树缓存）</center></small>

### MTP
MiMo-V2-Flash 最重要的设计之一是多层 MTP，共包含 3 个 MTP 层。

在解码场景下，大部分算子都是访存受限（memory-bound）的。由于 query 长度始终为 1，提高并行解码的 token 数量是获得更高吞吐量最直观的方式。

然而，当批大小增长到一定程度后，这一方式就会受限——KV 缓存的访存量也会随批大小线性增长，成为访存受限的瓶颈。此时设备的算力潜力尚未被完全利用，但再靠增大批大小已难以提升吞吐量。

MTP 仍然可以利用这部分未被充分挖掘的算力来降低 TPOT。在 MTP 中，多个 token 由按顺序排列的预测头同时生成，并在同一次查询中并行验证，从而增加 query 长度。这不会触发更多的 KV 缓存访问，反而始终会提高算术强度（arithmetic intensity）。当推理仍处于严重访存受限、而增大批大小的收益已经边际递减时，一个接受率令人满意的、足够激进的 MTP 策略在理论上可以榨取设备剩余的潜力，实现更好的 TPOT。

## 硬件感知的 MTP 配置
由于 MTP 的收益来自尚未饱和的算术强度，而 GQA 本身的算术计算量较低，MiMo-V2-Flash 的注意力设计天然适合多层 MTP。不过在部署 MiMo-V2-Flash 时，要实现最优的计算-访存平衡、在不同硬件平台上最大化性能，选择合适的批大小与 MTP 深度组合仍然至关重要。理论上，我们希望选择最佳权衡点，使吞吐量与 TPOT 同时达到令人满意的水平。这一权衡的最佳点取决于硬件，因为每个硬件平台都有自己的 roofline 模型。

总体而言，roofline 上限更高的设备从激进 MTP 中获益更多，因为它们拥有充裕的算力，在访存受限的解码中更难被饱和利用。相比之下，面向推理的加速器（如 H20）FLOPs 相对有限，使用 MTP 时应当更加谨慎：过于激进的 MTP 深度可能把负载推向计算受限（compute-bound）状态，反而降低吞吐量。

下面是我们在 H200 上的基准测试结果。MiMo-V2-Flash 在吞吐量与单请求 TPS 上取得了均衡表现。得益于 SWA 与 MTP，即使输入 token 长达 64K、每个 DP rank 批大小为 16 的长上下文设置下，单请求解码吞吐量仍保持在 150 TPS。

![figure3](/images/blog/mimo-v2-flash/decode_1.png)<small><center>MiMo-V2-Flash 解码基准测试（DP 2、TP 4、EP 8、MTP 接受长度 3.6、输入 token 长度 16k、不同批大小）</center></small>

![figure4](/images/blog/mimo-v2-flash/decode_2.png)<small><center>MiMo-V2-Flash 解码基准测试（DP 2、TP 4、EP 8、MTP 接受长度 3.6、每 DP rank 批大小 16、不同输入 token 长度）</center></small>

## 使用 SGLang Spec v2 实现快速 MTP 推理服务
MiMo 的多层 MTP 原生实现在 SGLang 的 spec v2 之上。我们启用了全重叠（fully overlapped）MTP 特性来改善吞吐量与延迟，提供更快的 MTP 推理服务。在 spec v2 中，重叠调度与投机解码融合在一起：输出同步/处理被延后，而下一批的算子提前启动，因此批处理与同步带来的 CPU 开销被隐藏在 GPU 前向计算之中。这减少了 GPU 空泡（bubble），同时改善了吞吐量与延迟。

下图是性能剖析（profiling）的截图，展示了 spec v2 下重叠进行的解码过程。

![figure4](/images/blog/mimo-v2-flash/profile.png)<small><center>重叠投机解码的剖析图</center></small>

## 更多讨论
在大多数 LLM 推理服务负载中，解码阶段都是访存受限的，大量算力得不到充分利用，主流的面向训练的 GPU 尤其如此。虽然具备高带宽、较低 FLOPs 的专用推理加速器是高性价比的选择，但其速度有限。MiMo-V2-Flash 尝试从另一个角度入手，让模型自身就具备推理效率。多层 MTP 或许是一种可推广的方案——如果接受率还能进一步优化，它能让用户借助 GPU 的算力实现更快的解码。架构更具适应性之后，硬件选择也更灵活：每种设备都可以运行在各自最优的计算-访存平衡点上。这也让训练与推理使用同一类硬件成为可能，从而简化部署并降低整体系统成本。

SGLang 已通过 PR（[#15207](https://github.com/sgl-project/sglang/pull/15207)、[#15208](https://github.com/sgl-project/sglang/pull/15208)）支持 MiMo-V2-Flash，该支持很快将合入主分支。本博客中的基准测试基于 MiMo 的优化分支完成，相应的优化将在近期上游合入 SGLang 主线。

## 快速上手

目前可以通过 Docker 镜像和 pip 安装在 SGLang 中使用 MiMo-V2-Flash。请参考以下说明启动 SGLang 服务器并开始使用 MiMo-V2-Flash。

具体步骤如下：

<br>

<details>
<summary><span style="font-size: 1.3em; font-weight: bold;">Docker</span></summary>

```bash
# Pull the docker image
docker pull lmsysorg/sglang:dev-pr-15207

# Launch the container
docker run -it --gpus all \
  --shm-size=32g \
  --ipc=host \
  --network=host \
  lmsysorg/sglang:dev-pr-15207 bash

# Start the server
SGLANG_ENABLE_SPEC_V2=1 python3 -m sglang.launch_server \
        --model-path XiaomiMiMo/MiMo-V2-Flash \
        --dp-size 2 \
        --enable-dp-attention \
        --tp-size 8 \
        --trust-remote-code \
        --mem-fraction-static 0.75 \
        --max-running-requests 128 \
        --chunked-prefill-size 16384 \
        --reasoning-parser qwen3 \
        --tool-call-parser mimo \
        --model-loader-extra-config '{"enable_multithread_load": "true","num_threads": 64}' \
        --attention-backend fa3 \
        --speculative-algorithm EAGLE \
        --speculative-num-steps=3 \
        --speculative-eagle-topk=1 \
        --speculative-num-draft-tokens=4 \
        --enable-mtp
```

</details>

<br>

<details>
<summary><span style="font-size: 1.3em; font-weight: bold;">pip 安装</span></summary>

```bash
# On a machine with SGLang dependencies installed or inside a SGLang nightly container
# Start an SGLang nightly container
docker run -it --gpus all \
  --shm-size=32g \
  --ipc=host \
  --network=host \
  lmsysorg/sglang:nightly-dev-20251215-4449c170 bash

# If you already have SGLang installed, uninstall the current SGLang version
pip uninstall sglang -y

# Install the PyPI Package
pip install sglang==0.5.6.post2.dev8005+pr.15207.g39d5bd57a \
  --index-url https://sgl-project.github.io/whl/pr/ \
  --extra-index-url https://pypi.org/simple

#Launch the server
SGLANG_ENABLE_SPEC_V2=1 python3 -m sglang.launch_server \
        --model-path XiaomiMiMo/MiMo-V2-Flash \
        --dp-size 2 \
        --enable-dp-attention \
        --tp-size 8 \
        --trust-remote-code \
        --mem-fraction-static 0.75 \
        --max-running-requests 128 \
        --chunked-prefill-size 16384 \
        --reasoning-parser qwen3 \
        --tool-call-parser mimo \
        --model-loader-extra-config '{"enable_multithread_load": "true","num_threads": 64}' \
        --attention-backend fa3 \
        --speculative-algorithm EAGLE \
        --speculative-num-steps=3 \
        --speculative-eagle-topk=1 \
        --speculative-num-draft-tokens=4 \
        --enable-mtp
```

</details>

<br>

<details>
<summary><span style="font-size: 1.3em; font-weight: bold;">测试部署</span></summary>

服务器启动后，可以在另一个终端用 chat completion 请求进行测试：

```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "XiaomiMiMo/MiMo-V2-Flash",
    "messages": [
      {"role": "user", "content": "Hello! What can you help me with?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'

```

**预期响应：**

```json
{
  "id": "...",
  "object": "chat.completion",
  "model": "XiaomiMiMo/MiMo-V2-Flash",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Hello! I can help you with..."
    }
  }]
}
```

</details>

<br>

<details>
<summary><span style="font-size: 1.3em; font-weight: bold;">常见问题</span></summary>

**DeepGEMM 超时错误**
首次启动时偶尔会出现 DeepGEMM 超时错误。只需在同一个容器中重新运行服务器启动命令即可——已编译的算子会被缓存，后续启动会很快。


</details>

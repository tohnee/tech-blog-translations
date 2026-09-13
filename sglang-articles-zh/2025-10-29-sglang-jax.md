---
title: "SGLang-Jax：原生 TPU 推理的开源解决方案"
title_en: "SGLang-Jax: An Open-Source Solution for Native TPU Inference"
author: "The SGLang-Jax Team"
date: "October 29, 2025"
previewImg: /images/blog/sglang_jax/cover.jpg
source: https://lmsys.org/blog/2025-10-29-sglang-jax/
translated: 2026-09-12
---

# SGLang-Jax：原生 TPU 推理的开源解决方案

> 原文：[SGLang-Jax: An Open-Source Solution for Native TPU Inference](https://lmsys.org/blog/2025-10-29-sglang-jax/) · LMSYS Blog · The SGLang-Jax Team

我们很高兴推出 SGLang-Jax——一个完全构建在 Jax 和 XLA 之上的先进开源推理引擎。
它复用了 SGLang 的高性能服务端架构，并用 Jax 编译模型的前向传播。
通过结合 SGLang 与 Jax，该项目实现了快速的原生 TPU 推理，同时保留了对连续批处理、前缀缓存、张量并行与专家并行、投机解码、算子融合以及高度优化的 TPU 算子等高级特性的支持。

基准测试显示，SGLang-Jax 的表现持平或优于其他 TPU 推理方案。
源代码可在 [https://github.com/sgl-project/sglang-jax](https://github.com/sgl-project/sglang-jax) 获取。

## 为什么选择 Jax 后端？

虽然 SGLang 最初构建于 PyTorch 之上，但社区一直热切期待 Jax 支持。
我们构建 Jax 后端有以下几个关键原因：

- Jax 从底层设计之初就面向 TPU。要获得不打折扣的最大性能，Jax 是不言而喻的选择。随着 Google 逐步扩大 TPU 的公开可用性，我们预计 Jax + TPU 将获得显著的关注度，并带来高性价比的推理。
- 包括 Google DeepMind、xAI、Anthropic 和 Apple 在内的领先 AI 实验室已经在使用 Jax。训练与推理使用同一框架，可以降低维护开销，并消除两个阶段之间的漂移。
- Jax + XLA 是久经考验的编译驱动技术栈，在 TPU 上表现出色，也能在众多类 TPU 的定制 AI 芯片上良好运行。

## 架构

下图展示了 SGLang-Jax 的架构。整个技术栈是纯 Jax 实现，代码干净、依赖极简。

在输入侧，它通过 OpenAI 兼容 API 接收请求，并利用 SGLang 高效的 RadixCache 实现前缀缓存，同时使用其重叠调度器实现低开销批处理。
调度器会为不同批大小预编译 Jax 计算图。
在模型侧，我们用 Flax 实现模型，并使用 `shard_map` 支持各种并行策略。
两个核心算子——注意力与 MoE——则以自定义 Pallas 算子实现。

<img src="/images/blog/sglang_jax/architecture.png" style="display:block; margin: auto; width: 85%;"></img>
<p style="color:gray; text-align: center;">SGLang-Jax 的架构</p>

## 关键优化

### 集成 Ragged Paged Attention v3
我们集成了 Ragged Paged Attention V3（[RPA v3](https://github.com/vllm-project/tpu-inference/tree/main/tpu_inference/kernels/ragged_paged_attention/v3)），并对其做了扩展以支持 SGLang 的特性：
- 我们针对不同场景调优了算子网格块（grid block）配置，以获得更好的性能。
- 我们使其兼容 RadixCache。
- 为支持 EAGLE 投机解码，我们为 RPA v3 增加了自定义掩码，用于验证阶段。

### 降低调度开销
前向传播过程中 CPU 与 TPU 上的串行操作会损害性能。不过，不同设备上的操作是可以解耦的——例如，在 TPU 上启动计算的同时，立即准备下一个要运行的批。为了提升性能，我们的调度器让 CPU 处理与 TPU 计算重叠执行。

在重叠事件循环中，调度器使用结果队列与线程事件将 CPU 与 TPU 的工作流水线化：当 TPU 处理批 N 时，CPU 准备批 N+1。为了最大化 CPU 与 TPU 的重叠程度，SGLang-jax 基于性能剖析结果仔细安排操作顺序。对于 Qwen/Qwen3-32B，我们把预填充与解码之间的时间间隔从约 12ms 缩短到 38us，以及从约 7ms 缩短到 24us。更多细节见我们之前的[博客](https://lmsys.org/blog/2024-12-04-sglang-v0-4/)。

<img src="/images/blog/sglang_jax/profile_overlap.jpg" style="display:block; margin: auto; width: 85%;"></img>
<p style="color:gray; text-align: center;">使用重叠调度器的性能剖析图。批与批之间的间隙极小。</p>

<img src="/images/blog/sglang_jax/profile_no_overlap.jpg" style="display:block; margin: auto; width: 85%;"></img>
<p style="color:gray; text-align: center;">不使用重叠调度器的性能剖析图。注意批与批之间的大段间隙（CPU 开销）。</p>

### MoE 算子优化
MoE 层目前支持两种实现策略：EPMoE 和 FusedMoE。
在 EPMoE 中，我们集成了 **Megablox GMM** 算子，替换了此前基于 jax `ragged_dot` 的实现。
Megablox GMM 专为 MoE 负载设计，能高效处理由 group_sizes 描述的变长专家分组，消除不必要的计算和不连续的内存访问。在典型配置下，相比 jax 原生的 ragged_dot 实现，该算子可带来 **3–4× 的端到端（e2e）ITL 加速**。
结合高效的 token 重排（permute/unpermute）、通过 ragged_all_to_all 进行的专家并行通信，以及自适应分块（tiling）策略，EPMoE 显著提升了整体吞吐量，非常适用于专家数量多、需要跨设备并行的场景。
相比之下，FusedMoE 使用稠密 einsum 操作融合所有专家计算，没有跨设备通信开销，更适合单个专家很大但专家总数较少的情况（如专家数 < 64）。它还可以作为轻量级的回退实现，便于调试与正确性验证。

### 投机解码
SGLang-jax 实现了基于 EAGLE 的投机解码，也称为多 token 预测（MTP）。
这种先进的投机解码技术使用轻量级草稿头（draft head）预测多个 token，再用完整模型单次前向传播并行验证，从而加速生成。
为了实现基于树的 MTP-Verify，SGLang-jax 在 Ragged Paged Attention V3 之上增加了非因果掩码（non-causal mask）支持，使验证阶段可以并行解码树形、非因果的草稿 token。
我们目前支持 Eagle2 和 Eagle3，并计划继续优化算子实现，为 MTP 的各个阶段增加对不同注意力后端的支持。

## TPU 性能
经过上述所有优化，SGLang-Jax 的表现持平或优于其他 TPU 推理方案。
与 GPU 方案相比，TPU 上的 SGLang-Jax 同样具有竞争力。

完整的基准测试结果与操作说明见 https://github.com/sgl-project/sglang-jax/issues/297。

## 使用方法

### 安装 SGLang-Jax 并启动服务器

安装：
```bash
# with uv
uv venv --python 3.12 && source .venv/bin/activate
uv pip install sglang-jax

# from source
git clone https://github.com/sgl-project/sglang-jax
cd sglang-jax
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -e python/
```

启动服务器：
```
MODEL_NAME="Qwen/Qwen3-8B"  # or "Qwen/Qwen3-32B"

jax_COMPILATION_CACHE_DIR=/tmp/jit_cache \
uv run python -u -m sgl_jax.launch_server \
--model-path ${MODEL_NAME} \
--trust-remote-code \
--tp-size=4 \
--device=tpu \
--mem-fraction-static=0.8 \
--chunked-prefill-size=2048 \
--download-dir=/tmp \
--dtype=bfloat16 \
--max-running-requests 256 \
--page-size=128
```

### 通过 GCP 控制台使用 TPU
你可以在控制台的 Menu → Compute Engine 下找到 TPU 选项，然后点击 Create TPU。
注意：只有特定区域（zone）支持特定 TPU 版本。记得将 TPU 软件版本设置为 v2-alpha-tpuv6e。
在 Compute Engine 菜单下，进入 Settings → Metadata，点击 SSH Keys 按钮，添加你的公钥。
TPU 服务器创建完成后，你可以使用控制台显示的 External IP 和公钥用户名登录。
另见：https://docs.cloud.google.com/tpu/docs/setup-gcp-account
<img src="/images/blog/sglang_jax/gcp_usage_1.png" style="display:block; margin: auto; width: 85%;"></img>

### 通过 SkyPilot 使用 TPU
我们推荐使用 [SkyPilot](https://github.com/skypilot-org/skypilot) 进行日常开发。
你可以快速配置好 SkyPilot，并在 sglang-jax 仓库中找到用于启动开发机和运行测试的脚本。

安装支持 GCP 的 SkyPilot：https://docs.skypilot.co/en/latest/getting-started/installation.html#gcp
然后启动 [sgl-jax.sky.yaml](https://github.com/sgl-project/sglang-jax/blob/master/scripts/tpu_resource.sky.yaml)：

```bash
sky launch sgl-jax.sky.yaml --cluster=sgl-jax-skypilot-v6e-4 --infra=gcp -i 30 --down -y --use-spot
```

这条命令会在各区域中寻找成本最低的 TPU spot 实例，并在空闲 30 分钟后自动关闭实例。它还会为你安装 sglang-jax 环境。
配置完成后，你可以直接用 `ssh cluster_name` 登录，无需再记录外部 IP 地址。


## 路线图
社区正与 Google Cloud 团队及多家合作伙伴共同推进以下路线图。

- 模型支持与优化
   - 优化 Grok2、Ling/Ring、DeepSeek V3 和 GPT-OSS
   - 支持 MiMo-Audio、Wan 2.1、Qwen3 VL
- 面向 TPU 优化的算子
   - 量化算子
   - 通信与计算重叠算子
   - MLA 算子
- 与 [tunix](https://github.com/google/tunix) 的强化学习集成
   - 权重同步
   - Pathways 与多主机支持
- 高级推理服务特性
   - PD 分离（预填充-解码分离）
   - 分层 KV 缓存（HiCache）
   - 多 LoRA 批处理

## 致谢
**SGLang-jax 团队**：sii-xinglong, jimoosciuc, Prayer, aolemila, JamesBrianD, zkkython, neo, leos, pathfinder-pf, Jiacheng Yang, Hongzhen Chen, Ying Sheng, Ke Bao, Qinghan Chen

**Google**：Chris Yang, Shun Wang, Michael Zhang, Xiang Li, Xueqi Liu

**InclusionAI**：Junping Zhao, Guowei Wang, Yuhong Guo, Zhenxuan Pan

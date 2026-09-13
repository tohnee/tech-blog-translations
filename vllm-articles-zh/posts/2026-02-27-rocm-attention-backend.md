---
title: "超越移植：vLLM 如何在 AMD ROCm 上编排高性能推理"
title_en: "Beyond Porting: How vLLM Orchestrates High-Performance Inference on AMD ROCm"
source: https://vllm.ai/blog/2026-02-27-rocm-attention-backend
crawled: 2026-09-12
translated: 2026-09-13
---

# 超越移植：vLLM 如何在 AMD ROCm 上编排高性能推理

> 原文：[Beyond Porting: How vLLM Orchestrates High-Performance Inference on AMD ROCm](https://vllm.ai/blog/2026-02-27-rocm-attention-backend) · vLLM 博客

作者：AMD 与 Embedded LLM 团队

[#性能](https://vllm.ai/blog/tags/performance)[#硬件](https://vllm.ai/blog/tags/hardware)

## 引言

长期以来，为 AMD 提供支持意味着"移植"——也就是仅仅让代码跑起来。**那个时代已经结束了。**

面对 AMD CDNA™ 3 架构硬件（AMD Instinct™ MI300X、Instinct MI325X、Instinct MI355X GPU）以及 DeepSeek MLA 这样的复杂模型结构，"仅仅能跑"已经不够了。这些工作负载需要*架构协同设计*——软件编排与硬件原语协同工作。

vLLM 现在在 AMD ROCm™ 软件上提供 7 种注意力后端。本文将逐一解释这些后端：它们为何存在、各自的取舍以及何时使用。我们提供了对比所有后端的透明基准测试，并展示面向 MHA（Multi-Head Attention，多头注意力）的 `ROCM_AITER_FA` 与 AITER MLA（Multi-Head Latent Attention，多头潜在注意力）后端如何借助 AMD 的 AITER 原语与 vLLM 的内核编排，实现 **1.2-4.4x 的吞吐量（TPS）提升**。

---

## 挑战：每个批次中混杂的工作负载

在生产环境的 LLM 服务中，每个推理步骤处理的都是来自不同请求类型的混合 token 批次。业界已经认识到这一挑战，也出现了多种解决方案：从内部调度精巧的统一内核，到配合专用内核的多路径路由。AMD 的 `ROCM_AITER_FA` 采取显式路由的思路，把"感知工作负载的优化"作为一等设计原则，而非内核内部的实现细节。

- **预填充（Prefill）**：新到达服务器的提示词。它们包含成千上万个需要一次性完成注意力计算的输入 token。GPU 在此进行高强度的矩阵乘法，因此预填充是**计算受限（compute-bound）**的。
- **扩展（Extend）**：为 KV 缓存已部分建立的请求（例如来自分块预填充、前缀缓存复用或上一轮对话）继续处理提示词侧的额外 token。由于这些新 token 既要关注已缓存的上下文，又要关注新输入，扩展是一种混合型工作负载。在线服务中，调度器利用这一阶段把长提示词的工作切分为小块，并与在途请求的解码交错进行，从而改善延迟与吞吐量之间的整体平衡。
- **解码（Decode）**：逐个生成输出 token。每个解码步骤都要把整个 KV 缓存从内存加载进来，才能产生一个 token。瓶颈在于内存带宽，因此解码是**内存受限（memory-bound）**的。

这些请求类型随机到达，为了效率被一起批处理。

![连续批处理示意图](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/continuous-batching.png)

连续批处理示意图

5 个并发请求的在线服务。第 4 步展示了预填充、扩展与解码 token 被一起批处理的情况。

优化的难点在于：预填充想要大的分块尺寸和最大的 ALU 利用率，而解码想要合并的内存访问和最少的缓存读取。**为一种工作负载调优的内核，会让另一种工作负载损失本可获得的性能。**

这种混合工作负载场景正是 `ROCM_AITER_FA` 三路径路由所要解决的：它不强迫所有请求类型通过同一个内核，而是把每类请求路由到针对该负载特性优化的专用内核。

---

## 其他 MHA 后端

在深入 `ROCM_AITER_FA` 之前，我们先了解其他可用的 MHA 后端：

### 统一注意力后端

![统一注意力内核流程图](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/ROCm-Attention-unified-attn.png)

统一注意力内核流程图

统一注意力通过单一内核处理所有 token。

这些后端通过单一内核路径处理所有 token（预填充/扩展/解码）：

| 后端 | 内核来源 | 使用场景 |
| --- | --- | --- |
| [TRITON\_ATTN](https://github.com/vllm-project/vllm/blob/v0.14.0rc2/vllm/v1/attention/backends/triton_attn.py) | [vLLM Triton 内核](https://github.com/vllm-project/vllm/blob/v0.14.0rc2/vllm/v1/attention/ops/triton_unified_attention.py) | 默认回退方案 |
| [ROCM\_AITER\_UNIFIED\_ATTN](https://github.com/vllm-project/vllm/blob/v0.14.0rc2/vllm/v1/attention/backends/rocm_aiter_unified_attn.py) | [AITER Triton 内核](https://github.com/ROCm/aiter/blob/v0.1.10.post3/aiter/ops/triton/_triton_kernels/attention/unified_attention.py) | 单内核 AITER 路径 |

```
def forward():
    # Stage 1: Save Key/Value into KV-Cache
    reshape_and_cache_flush(new_key, new_value, ...)
    # Stage 2: Single kernel for all attention
    unified_attention_kernel(new_query, KV-Cache, ...)
```

### ROCM\_ATTN：传统双路径后端

[ROCM\_ATTN](https://github.com/vllm-project/vllm/blob/v0.14.0rc2/vllm/v1/attention/backends/rocm_attn.py) 使用按阶段区分内核的双路径路由：

- **预填充**：Triton 内核
- **解码**：HIP 分页注意力内核（受支持时）

该后端有两个重要特点：

1. **传统双路径架构**：预填充（Triton）与解码（HIP 分页注意力）使用不同的内核。注意，HIP 分页注意力内核只支持特定的 KV head 维度——对不支持的配置（如 Qwen3-235B），它会回退到 Triton 解码内核，性能明显变慢。
2. **Radeon GPU 支持**：与 `TRITON_ATTN` 一样，该后端支持 **Radeon GPU**——在 AITER 原语不可用的消费级硬件部署中很有用。

---

## ROCM\_AITER\_FA 后端：面向 AMD 的内核编排

`ROCM_AITER_FA` 不只是一个内核包装器——它是一层精巧的编排层，把请求路由到专用内核，将 vLLM 的高层管理与 AMD 的 AITER 原语结合在一起。

![ROCM\_AITER\_FA 架构流程图](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/ROCm-Attention-rocm_aiter_fa.png)

ROCM\_AITER\_FA 架构流程图

ROCM\_AITER\_FA 把 token 路由到三条专用路径

### 关键创新

1. **三路径路由**：请求被动态归类到解码、预填充与扩展路径——每条路径都有各自优化的内核：

   - **预填充路径**：新序列使用 `flash_attn_varlen_func`——借助 CDNA 矩阵核心处理计算密集型工作
   - **扩展路径**：续写序列使用带 LSE 合并的分块注意力——高效处理 10 万 token 以上的上下文
   - **解码路径**：单 token 生成使用 AITER 高度优化的内核，充分发挥内存带宽

   [交互式图表](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/iteration2\_attention\_backend\_routing.html)

   点击展开

   动画：R1（解码 token）路由到解码路径，R2（预填充 token）路由到预填充路径。

**2. 批次重排序（Model Runner）**：`ROCM_AITER_FA` 是少数会在处理前对请求进行重排序的后端之一。vLLM 的 Model Runner 会把请求重排为 `[decode:extend:prefill]` 的顺序以实现连续内存访问。每个注意力后端通过设置 `reorder_batch_threshold` 来选择加入这一机制——`ROCM_AITER_FA` 将其设为 1，确保每个混合批次在进入三路径路由之前都会被重排序。

![批次重排序优化示意图](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/batch_reordering.png)

批次重排序优化示意图

批次重排序确保每条内核路径处理的都是连续的 token，消除冗余的 KV 缓存读取。

[交互式图表](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/iteration4\_batch\_reordering\_extend.html)

点击展开

动画：批次重排序把请求重排为 [decode > extend > prefill]，然后将 R3 路由到扩展路径。

**3. 分块上下文处理**：长序列按每次迭代固定的 token 预算（总计约 32K token）分块处理，并在多个 extend 请求之间切分；基于 LSE 的合并保证数值稳定性。

![分块上下文处理流程图](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/chunked_context_flow.png)

分块上下文处理流程图

10 万 token 以上的上下文以 32K 为块处理，配合基于 LSE 的合并以保证数值稳定性。

**4. 硬件优化的 KV 缓存布局**：使用由 AMD AITER 内核团队设计的预重排 KV 缓存布局：

```
k_cache: [num_blocks, num_heads, head_dim // x, block_size, x]
v_cache: [num_blocks, num_heads, block_size // x, head_dim, x]
```

该布局使内存访问模式与 AMD 的 CDNA 架构对齐，让解码路径能够以**零布局转换开销**调用 AITER 的 `pa_fwd_asm` 内核——相比标准 KV 缓存布局带来 **15-20% 的解码吞吐量提升**。

### 为什么选择显式三路径路由？

`ROCM_AITER_FA` 做出了一个深思熟虑的架构选择：在软件层对工作负载进行路由，而不是依赖单一内核处理一切。

这种显式方式带来：

- **可调试性**：每条路径都可以独立剖析、调优与优化
- **可移植性**：同一套路由逻辑可以跨 MI300X → MI325X → MI355X 工作，无需硬件相关的改动
- **可扩展性**：可以添加新的工作负载类型或内核变体，而无需重新设计核心架构
- **可预测性**：执行路径是确定性的，性能分析直观明了

扩展路径尤为重要：前缀缓存与多轮对话如今已是生产部署的标配。为这类负载提供一条配备分块上下文注意力的专用路径，能确保它们获得一等公民级别的优化。

### 三路径处理详解

**预填充路径**：Query/Key/Value 采用标准的 `[num_tokens, num_heads, head_dim]` 布局，以对齐高度优化的 AITER MHA 内核，避免任何额外的内存拷贝操作。

**扩展路径**：这是最具挑战性的路径。新 token 必须与存储在重排 KV 缓存布局中的上下文 token 计算注意力。由于这种重排布局与 AITER 用于长上下文计算的 MHA 内核不兼容，我们插入了一个额外的 KV 缓存读取算子（`cp_mha_gather_cache`），把上下文的 Key/Value 取出并转换为标准布局。长上下文被分块为多个段以管理内存：

```
def extend_forward():
    # Stage 1: Attention for new tokens
    flash_attn_varlen_func()  # calling AITER MHA

    # Stage 2: Context Chunk Loop Processing
    for chunk in context_chunks:
        cp_mha_gather_cache()      # Triton gather kernel
        flash_attn_varlen_func()   # calling AITER MHA
        merge_attn_states()        # LSE-based merge

    # Stage 3: Get the final result
    merge_attn_states()
```

每个块会产生一个输出和一个 LSE（log-sum-exp）。LSE 记录了 softmax 分母，使合并过程在数值上保持稳定——注意力得分更高的块自然在最终结果中占主导。

**解码路径**：直接利用重排的 KV 缓存布局。自定义的 `reshape_and_cache_flush` 算子确保缓存始终处于重排布局，使注意力后端能够以零布局转换开销调用 AITER 高性能的 `pa_fwd_asm` 内核。

### 交互动画：ROCM\_AITER\_FA 请求流转

下面的动画展示了多个请求在 7 次迭代中如何流经 ROCM\_AITER\_FA 后端。可使用控件开始、暂停或跳转到特定迭代。

[交互式图表](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/rocm\_aiter\_fa\_flow\_animated\_new.html)

点击展开

**迭代指南：**

| 迭代 | 关键事件 |
| --- | --- |
| **1** | R1 进入 → 分词 → 调度器队列 → QKV 投影 → **预填充路径** → 采样 1 个 token。R2 在迭代中途到达，在队列中等待。 |
| **2** | R1 与 R2 被一起批处理。R1 → **解码路径**，R2 → **预填充路径**。R3、R4 到达并进入队列。 |
| **3** | 4 个请求一起批处理。token 预算 = 100，因此 R3 调度 100 个 token（还剩 180 个）。R3 输出 = 0（提示词 token 尚未全部计算完成）。 |
| **4** | R3 进入**扩展路径**，继续计算剩余的提示词 token。批次重排序：张量被重排为 [decode > extend > prefill]。 |
| **5** | 批次重排序继续：[decode > extend] 顺序。R5 完成扩展，转入解码。 |
| **6-7** | 所有请求进入**解码路径**，持续生成 token 直至停止信号。 |

*该动画展示了 ROCM\_AITER\_FA 如何根据请求状态将其动态路由到预填充 → 扩展 → 解码路径，实现对混合工作负载的高效批处理。*

---

## AITER MLA 后端：为 DeepSeek 而优化

DeepSeek 与 Kimi 的 MLA 架构把 KV 缓存压缩到 **576 维**（标准 MHA 约为 8K）——内存减少 14 倍。这种压缩改变了注意力的性能特征，需要不同于标准 MHA 的优化策略。

### 混合方案

vLLM 提供两个基于 AITER 的 MLA 后端，预填充实现各不相同：

| 后端 | 预填充内核 | 解码内核 |
| --- | --- | --- |
| `TRITON_MLA` | vLLM Triton | vLLM Triton |
| `ROCM_AITER_MLA` | AITER MHA | AITER 汇编 |
| `ROCM_AITER_TRITON_MLA` | AITER Triton MHA | AITER 汇编 |

基础的 `TRITON_MLA` 后端在两个阶段都使用 vLLM 默认的 Triton 内核。AITER 后端则把解码内核替换为手工调优的汇编内核（`mla_decode_fwd`），大部分性能提升正来自这里。两个 AITER 后端唯一的区别在预填充路径：`ROCM_AITER_MLA` 调用 `aiter.flash_attn_varlen_func`（AITER MHA 会自动分发到 CK 或汇编内核），而 `ROCM_AITER_TRITON_MLA` 调用 `aiter.ops.triton.mha.flash_attn_varlen_func`（AITER Triton MHA）。

### 吸收式与非吸收式方案

所有 MLA 后端都采用相同的基本处理策略：

- **预填充/扩展（非吸收式）**：在未压缩的表示上用标准 MHA 内核计算注意力
- **解码（吸收式）**：使用直接在压缩后的 576 维潜在空间上运行的专用 MLA 内核

```
def _forward_prefill():
    # Stage 1: Attention for new tokens (non-absorbed)
    _run_prefill_new_tokens()

    # Stage 2: For extend path, context chunk loop
    for chunk in context_chunks:
        gather_and_maybe_dequant_cache()
        _run_prefill_context_chunk()
        merge_attn_states()

    # Stage 3: Final merge
    merge_attn_states()
```

在**解码**阶段，模型逐个生成 token。压缩后的 KV 缓存意味着要加载的数据更少，但瓶颈仍是内存带宽——解码因此是**内存受限**的。AITER 汇编内核（`mla_decode_fwd`）把每一字节的 HBM3 带宽都用到极致，显著超越通用的 Triton 解码内核。

### 汇编解码内核为何重要

两个 AITER MLA 后端（`ROCM_AITER_MLA` 与 `ROCM_AITER_TRITON_MLA`）共享**同一个汇编解码内核**（`mla_decode_fwd`）。大部分性能提升正来自这里：

| 阶段 | AITER MLA 后端 | vLLM TRITON\_MLA 基线 |
| --- | --- | --- |
| **预填充** | AITER MHA 或 Triton（视情况而定） | Triton flash attention |
| **解码** | 汇编 `mla_decode_fwd` | Triton `decode_attention_fwd` |

**1.2-1.6x 的加速**主要来自共享的汇编解码内核。由于 TPOT 中解码占大头（OSL=1K 时需要 1K 次迭代），优化解码能带来最大的吞吐量收益。两个 AITER 后端之间的预填充内核差异对整体性能影响极小。

除内核本身的性能之外，这些后端还继承了 FlashMLABackend 的完整功能集，包括 FULL\_AND\_PIECEWISE CUDA Graph 支持与 MTP 支持。另一个优势是在几乎任意 KV 缓存块大小下性能几乎一致——你可以把每个 token 都当作前缀缓存，而不必担心细粒度缓存通常带来的性能损失。

---

## 性能基准测试

**基准测试方法**：所有基准测试均使用 `rocm/vllm-dev:nightly_main_20260115` 与 ROCm 7.0.0 运行。这是 2026 年 1 月 15 日从 <https://github.com/vllm-project/vllm> 主分支构建的 nightly Docker 镜像。我们先用初始请求对内核进行预热；报告的结果排除了首次运行，以消除 JIT 编译开销。

**基准测试服务器命令（点击展开）**

**MHA 基准测试（Qwen3-235B）：**

```
export SAFETENSORS_FAST_GPU=1
export VLLM_ROCM_USE_AITER=1
export VLLM_RPC_TIMEOUT=1800000
export VLLM_ROCM_SHUFFLE_KV_CACHE_LAYOUT=1

# Choose backend: TRITON_ATTN, ROCM_ATTN, ROCM_AITER_FA, ROCM_AITER_UNIFIED_ATTN
ATTN_BACKEND="ROCM_AITER_FA"

model_path=Qwen/Qwen3-235B-A22B-Instruct-2507-FP8
vllm serve $model_path \
    --tensor-parallel-size 8 \
    --max-num-batched-tokens 16384 \
    --trust-remote-code \
    --no-enable-prefix-caching \
    --enable-expert-parallel \
    --disable-log-requests \
    --gpu_memory_utilization 0.9 \
    --attention-backend ${ATTN_BACKEND} \
    --compilation-config '{"cudagraph_mode": "FULL_AND_PIECEWISE"}' \
    --async-scheduling \
    --port 1234
```

**MLA 基准测试（DeepSeek-R1）：**

```
export SAFETENSORS_FAST_GPU=1
export VLLM_ROCM_USE_AITER=1
export VLLM_RPC_TIMEOUT=1800000

# Choose backend: TRITON_MLA, ROCM_AITER_MLA, ROCM_AITER_TRITON_MLA
ATTN_BACKEND="ROCM_AITER_MLA"

model_path=deepseek-ai/DeepSeek-R1-0528
vllm serve $model_path \
    --tensor-parallel-size 8 \
    --max-num-batched-tokens 16384 \
    --trust-remote-code \
    --no-enable-prefix-caching \
    --disable-log-requests \
    --gpu_memory_utilization 0.9 \
    --attention-backend ${ATTN_BACKEND} \
    --compilation-config '{"cudagraph_mode": "FULL_AND_PIECEWISE"}' \
    --async-scheduling \
    --port 1234
```

### MHA 基准测试结果

**模型**：[Qwen3-235B-A22B-FP8](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507-FP8)，注意力 TP8 + MoE EP8 | **工作负载**：ISL=10K，OSL=1K，64 与 128 个并发请求

![MHA TPOT 对比](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/mha_tpot_comparison.png)

MHA TPOT 对比

在 MI300X/MI325X/MI355X 上，ROCM\_AITER\_FA 的 TPOT 比传统 ROCM\_ATTN 快 2.8-4.6x。

![MHA TTFT 对比](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/mha_ttft_comparison.png)

MHA TTFT 对比

TTFT（Time To First Token，首 token 延迟）对比显示，在 64 与 128 并发级别下，ROCM\_AITER\_FA 与 ROCM\_AITER\_UNIFIED 在预填充性能上领先。

![MHA TPS 对比](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/mha_tps_comparison.png)

MHA TPS 对比

输出吞吐量（TPS）与 TPOT 结果一致——ROCM\_AITER\_FA 的吞吐量比传统 ROCM\_ATTN 高 2.7-4.4x。

**TPS 相对 ROCM\_AITER\_FA 慢多少倍（64 个并发请求）：**

| 硬件 | ROCM\_AITER\_FA | ROCM\_AITER\_UNIFIED\_ATTN | TRITON\_ATTN | ROCM\_ATTN |
| --- | --- | --- | --- | --- |
| MI300X | **1.00x** | 1.05x | 1.30x | 3.82x |
| MI325X | **1.00x** | 1.02x | 1.19x | 4.36x |
| MI355X | **1.00x** | 0.95x | 1.08x | 3.61x |

**TPS 相对 ROCM\_AITER\_FA 慢多少倍（128 个并发请求）：**

| 硬件 | ROCM\_AITER\_FA | ROCM\_AITER\_UNIFIED\_ATTN | TRITON\_ATTN | ROCM\_ATTN |
| --- | --- | --- | --- | --- |
| MI300X | **1.00x** | 1.05x | 1.36x | 2.65x |
| MI325X | **1.00x** | 1.00x | 1.28x | 3.12x |
| MI355X | **1.00x** | 1.01x | 1.23x | 2.88x |

各代 GPU 之间的相对性能表现一致。在这种均匀工作负载场景下，`ROCM_AITER_UNIFIED_ATTN`（单内核路径）与 `ROCM_AITER_FA`（三路径路由）的差距在 5% 以内——若混合工作负载中包含前缀缓存命中，三路径路由的优势会更加明显。

*注：ROCM\_ATTN 的 TPS 慢 2.7-4.4x，是因为 Qwen3-235B 的 KV head 维度不受 HIP 分页注意力支持，迫使它回退到 Triton 解码内核。对于 head 维度受支持的模型，`ROCM_ATTN` 比 `TRITON_ATTN` 更快。*

### MLA 基准测试结果

**模型**：[DeepSeek-R1-0528](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528)，TP8，block\_size=16 | **工作负载**：ISL=10K，OSL=1K，64 与 128 个并发请求

![MLA TPOT 对比](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/mla_tpot_comparison.png)

MLA TPOT 对比

得益于共享的汇编解码内核，在 MI300X/MI325X/MI355X 上 AITER MLA 后端的 TPOT 比 TRITON\_MLA 快 1.2-1.6x。

![MLA TTFT 对比](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/mla_ttft_comparison.png)

MLA TTFT 对比

TTFT 对比显示，在 128 并发下 ROCM\_AITER\_MLA 在 MI355X 上取得最佳 TTFT。

![MLA TPS 对比](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/mla_tps_comparison.png)

MLA TPS 对比

输出吞吐量（TPS）显示，AITER MLA 后端的吞吐量最高可达 TRITON\_MLA 的 1.5x。

**TPS 相对 ROCM\_AITER\_MLA 慢多少倍（64 个并发请求）：**

| 硬件 | ROCM\_AITER\_MLA | ROCM\_AITER\_TRITON\_MLA | TRITON\_MLA |
| --- | --- | --- | --- |
| MI300X | **1.00x** | 0.98x | 1.33x |
| MI325X | **1.00x** | 0.98x | 1.41x |
| MI355X | **1.00x** | 1.03x | 1.52x |

**TPS 相对 ROCM\_AITER\_MLA 慢多少倍（128 个并发请求）：**

| 硬件 | ROCM\_AITER\_MLA | ROCM\_AITER\_TRITON\_MLA | TRITON\_MLA |
| --- | --- | --- | --- |
| MI300X | **1.00x** | 0.97x | 1.24x |
| MI325X | **1.00x** | 0.97x | 1.24x |
| MI355X | **1.00x** | 1.01x | 1.35x |

两个 AITER MLA 后端整体性能相近。在 gfx942（MI300X/MI325X）上，`ROCM_AITER_TRITON_MLA` 的 TPS 高 2-3%。在 gfx950（MI355X）上，`ROCM_AITER_MLA` 追平或超越 `ROCM_AITER_TRITON_MLA`，因为它使用 AITER 汇编 MHA 预填充。`ROCM_AITER_MLA` 在 MI355X 上也取得最佳 TTFT。推荐所有工作负载使用自动选择的 `ROCM_AITER_MLA`。

*注：这些基准测试使用统一的请求大小。包含前缀缓存、混合上下文长度与多样请求模式的生产工作负载，能更充分地发挥三路径路由架构的优势。*

---

## 协作：vLLM + AITER

性能提升并非来自某一项单独的优化——而是源于 vLLM 编排层与 AMD AITER 原语的协同工作。理解这种协作，就能明白为什么"仅仅移植"是不够的。

![系统架构堆栈图](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/system_stack.png)

系统架构堆栈图

完整的系统堆栈：从用户请求出发，经由 vLLM 编排，最终到达 AMD 硬件上的 AITER 原语。

### 创新归因

性能从何而来？来自两层的协同工作：

![创新归因](https://vllm.ai/blog-assets/figures/2026-02-27-rocm-attention-backend/innovation_attribution.png)

创新归因

vLLM 编排层负责路由与分块；AITER 提供硬件优化的原语。

**关键洞见**：AITER 提供了专为 CDNA 打造的高度优化注意力原语。vLLM 的编排层则增加了感知工作负载的路由与分块处理，从而释放最后的性能空间。两者缺一不可，单靠任何一方都无法达到最优结果。

---

## 快速上手

### 快速开始

```
# Recommended: Let vLLM auto-select optimized backends
export VLLM_ROCM_USE_AITER=1
vllm serve <your-model> --tensor-parallel-size <tp>
```

设置 `VLLM_ROCM_USE_AITER=1` 后，vLLM 会自动选择：

- 面向 MHA 模型（Llama、Qwen、Mistral）选择 `ROCM_AITER_FA`
- 面向 MLA 模型（DeepSeek、Kimi）选择 `ROCM_AITER_MLA`

### 显式选择后端

想要试验的高级用户可以通过 `--attention-backend` 指定后端：

```
vllm serve deepseek-ai/DeepSeek-R1-0528 \
    --tensor-parallel-size 8 \
    --attention-backend ROCM_AITER_TRITON_MLA
```

我们的基准测试显示，两个 AITER MLA 后端性能相近，因为它们共享同一个汇编解码内核。预填充内核因架构而略有差异，但由于解码在工作负载中占主导，整体差异极小。对大多数用户来说，自动选择的 `ROCM_AITER_MLA` 表现良好。

### 硬件支持

| GPU | 显存 | 架构 |
| --- | --- | --- |
| MI300X | 192GB HBM3 | gfx942 |
| MI325X | 256GB HBM3e | gfx942 |
| MI355X | 288GB HBM3e | gfx950 |

### 完整后端参考

vLLM 在 AMD ROCm 上提供 7 种注意力后端，各自针对不同场景优化：

| 类别 | 后端 | 启用方式 | 说明 |
| --- | --- | --- | --- |
| MHA | TRITON\_ATTN | `--attention-backend TRITON_ATTN` | 基线，支持 Radeon |
| MHA | ROCM\_AITER\_UNIFIED\_ATTN | `--attention-backend ROCM_AITER_UNIFIED_ATTN` | AITER 统一内核 |
| MHA | ROCM\_ATTN | `--attention-backend ROCM_ATTN` | 传统双路径，支持 Radeon |
| MHA | **ROCM\_AITER\_FA** | `--attention-backend ROCM_AITER_FA` + `VLLM_ROCM_SHUFFLE_KV_CACHE_LAYOUT=1` | **推荐**，AITER 下自动选择 |
| MLA | TRITON\_MLA | `--attention-backend TRITON_MLA` | 基线，支持 Radeon |
| MLA | **ROCM\_AITER\_MLA** | `--attention-backend ROCM_AITER_MLA` | **推荐**，AITER 下自动选择 |
| MLA | ROCM\_AITER\_TRITON\_MLA | `--attention-backend ROCM_AITER_TRITON_MLA` | 备选 AITER MLA 后端 |

---

## 结论

"仅仅移植"的时代已经结束。本文介绍了 vLLM 在 AMD ROCm 上提供的全部 7 种注意力后端，并用透明公开的基准测试展示了它们各自的取舍。

**关键结果（ISL=10K，OSL=1K 基准测试）：**

- `ROCM_AITER_FA`：在 MHA 模型上 TPS 比传统 ROCM\_ATTN 高 **2.7-4.4x**
- `ROCM_AITER_MLA`：在 DeepSeek MLA 上借助汇编解码内核，TPS 比 TRITON\_MLA 高 **1.2-1.5x**
- 性能在 MI300X → MI325X → MI355X 之间均可扩展

**我们的建议**：只需 `export VLLM_ROCM_USE_AITER=1`，让 vLLM 自动选择最优后端。默认选择（MHA 用 `ROCM_AITER_FA`，MLA 用 `ROCM_AITER_MLA`）在所有测试过的负载上都表现出色。

这就是原生 AMD 优化的样子：不是移植，而是量身打造。三路径路由架构体现了一个深思熟虑的设计选择——在软件层显式分离工作负载，每条路径调用硬件优化的 AITER 原语。其结果是一个可调试、可跨 GPU 世代移植、并能从容应对生产级 LLM 服务混合工作负载的系统。

---

## 致谢

我们要感谢为这项合作贡献力量的众多优秀同事：

**AMD**：Hattie Wu、Yi Gan、Zejun Chen、Carlus Huang、Lingpeng Jin、Peng Sun 以及 AITER 团队。

**Embedded LLM**：Pin Siang Tan、Tun Jian Tan、Jun Kang Chow 以及 Embedded LLM 团队。

## 资源

- [AITER 库（AMD）](https://github.com/ROCm/aiter)
- [vLLM 文档](https://docs.vllm.ai/)
- [Qwen3-235B 模型](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507-FP8)
- [DeepSeek-R1 模型](https://huggingface.co/deepseek-ai/DeepSeek-R1-0528)

---

## 免责声明

由 AMD AI Framework 团队于 2026 年 1 月 29 日测试，测量 AMD Instinct MI300X、MI325X、MI355X 平台上以 TPS 计的推理性能。

**硬件配置**

- MI300X：搭载 AMD EPYC 9654 96 核处理器的服务器，配 8x AMD Instrinct MI300X（192GB，750W）GPU，Supermicro AS-8125GS-TNMR2，NPS1（每插槽 1 个 NUMA），2.2TiB（24 条 DIMM，4800 mts 内存，96 GiB/DIMM），BIOS 版本：3.2
- MI325X：搭载 AMD EPYC 9575F 64 核处理器的服务器，配 8x AMD Instrinct MI325X（256GB，1000W）GPU，Supermicro AS-8125GS-TNMR2，NPS1（每插槽 1 个 NUMA），2.2TiB（24 条 DIMM，4800 mts 内存，96 GiB/DIMM），BIOS 版本：3.2
- MI355X：搭载 AMD EPYC 9575F 64 核处理器的服务器，配 8x AMD Instrinct MI355X（288GB，1400W）GPU，Supermicro AS-8125GS-TNMR2，NPS1（每插槽 1 个 NUMA），2.2TiB（24 条 DIMM，4800 mts 内存，96 GiB/DIMM），BIOS 版本：3.2

**软件配置**
Ubuntu 22.04LTS，Linux 内核 5.15.0-116-generic，ROCm 7.0 版本软件，PyTorch 2.9.0a0，vLLM 0.14.0rc2（2026 年 1 月 15 日版本）

服务器制造商可能采用不同配置，从而产生不同结果。性能可能因配置、软件、vLLM 版本以及是否使用最新驱动与优化而异。

---

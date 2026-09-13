---
title: "vLLM 中混合 SSM 模型的分离式服务"
title_en: "Disaggregated Serving for Hybrid SSM Models in vLLM"
source: https://vllm.ai/blog/2026-04-21-hybrid-ssm-disagg
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中混合 SSM 模型的分离式服务

> 原文：[Disaggregated Serving for Hybrid SSM Models in vLLM](https://vllm.ai/blog/2026-04-21-hybrid-ssm-disagg) · vLLM 博客

作者：Nicolò Lucchesi、Zhanqiu Hu（Red Hat）以及 vLLM 团队

[#分离部署](https://vllm.ai/blog/tags/disaggregation)[#mamba](https://vllm.ai/blog/tags/mamba)

## 引言

将 Mamba 风格的 SSM 层与标准全注意力（FA）层交替堆叠的混合架构——例如 [NVIDIA Nemotron-H](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8)——正在获得越来越多的关注，因为它把状态空间模型的线性时间效率与注意力的表达能力结合在了一起。
vLLM 已经通过其[基于 NIXL 的 KV 连接器](https://blog.vllm.ai/2025/01/27/v0-disagg-prefill.html)支持标准 Transformer 模型的分离式预填充/解码（P/D）：预填充实例计算 KV 缓存块，解码实例通过 RDMA 拉取它们，避免冗余的重复计算。
但把它扩展到混合模型并非易事。FA 层与 SSM 层存储的状态在本质上是不同的，布局和大小都不一样，而块管理器（block manager）和 NIXL 连接器最初都是围绕单一、统一的 KV 缓存格式设计的。

在本文中，我们介绍如何扩展 NIXL 连接器，使其在分离部署模式下支持混合 SSM-FA 模型。核心思路是：

- **双描述符视图**——两组 NIXL 块描述符，以不同的偏移和大小索引同一块物理内存区域，一组用于 FA 块，另一组用于 SSM 块。
- **物理/逻辑块桥接**——处理块管理器所见的逻辑块抽象与注意力内核所需的物理块大小之间的不一致。
- **3 描述符 conv 传输**——对 Mamba conv 状态的一种分解，使得异构张量并行传输无需在发送侧重排数据。

这些改动都不会修改标准 Transformer 模型的既有工作流。它们是纯粹的增量扩展，只在模型包含 SSM 层时才会激活。
该功能随 `vllm>=v0.20.0` 提供。

这项工作建立在[NIXL 的 HMA 接口](https://github.com/vllm-project/vllm/pull/35758)之上，横跨多个 PR：

- [#36687](https://github.com/vllm-project/vllm/pull/36687) — 面向混合 SSM-FA 模型的双描述符视图与同构 TP 支持
- [#37416](https://github.com/vllm-project/vllm/pull/37416) — Mamba 内核的 DS conv 状态布局
- [#37635](https://github.com/vllm-project/vllm/pull/37635) — 异构 TP 的 3 描述符 conv 状态传输
- [#37310](https://github.com/vllm-project/vllm/pull/37310) — Mamba P/D 分离的 N-1 预填充

---

## 背景：NIXL KV 传输工作流

在深入混合模型的改动之前，先简要回顾 NIXL 分离式 P/D 在标准 Transformer 上是如何工作的。

该工作流分为四个阶段：

1. **注册内存区域**——每个 worker 把自己的 KV 缓存张量注册到 NIXL，使其可以通过 RDMA 访问。
2. **创建块描述符**——为每个已注册区域创建逐块描述符，指定 `(address, length, device_id)`。这些描述符是传输的基本单元：我们不搬运整个区域，而是传输单个块。
3. **握手**——当解码（D）worker 第一次需要从预填充（P）worker 拉取数据时，双方交换元数据：agent 句柄、块数量、块长度等。每个 P-D 对只做一次。
4. **传输**——调度器告诉 D 从 P 拉取哪些块。D 把 `block_id -> descriptor_id` 进行映射，发起一次 RDMA READ，然后轮询完成状态。

对于一个注册了 `M` 个区域、每个区域 `N` 个块的标准模型，描述符列表如下：

```
+----------------------------------+
| Region 0: desc_0 ... desc_{N-1}  |
| Region 1: desc_0 ... desc_{N-1}  |
| ...                              |
| Region M: desc_0 ... desc_{N-1}  |
+----------------------------------+

```

区域 `r` 中的块 ID `b` 映射到描述符索引 `r * N + b`。

混合模型的挑战在于，这一统一方案不再成立：FA 层与 SSM 层需要不同的描述符大小和不同的块数量。

---

## 挑战：FA 与 SSM 状态在本质上完全不同

在标准 Transformer 中，每一层的 KV 缓存形状都相同：`[num_blocks, 2, block_size, num_kv_heads, head_dim]`（或其布局变体）。所有层共享相同的块大小、相同的页大小和相同的块数。

Mamba 层存储的东西则非常不同。它们不保存逐 token 的 K/V 对，而是维护一个压缩的 **conv 状态**和一个**时间 SSM 状态**：

```
Conv state:  (conv_dim, state_len)    e.g. (3072, 3)   -- bf16
SSM state:   (num_heads, head_dim, state_size)   e.g. (32, 64, 128) -- fp32

```

这些状态里没有"token"的概念——它们是对整个序列历史的固定大小摘要。这意味着 SSM 的 `block_size` 实际上是 1：每个块都是一个完整的状态快照，而不是一组逐 token 的向量。
请记住：**在这里，块是传输的唯一单元**。

### HMA 共享张量布局

vLLM 的混合内存分配器（Hybrid Memory Allocator，HMA）按类型对层分组：所有 FA 层为一组，所有 SSM 层为另一组，依此类推。然后在组之间汇集内存，使**各组中位于相同位置的层共享同一个物理张量**。
这很高效（块可以互换），但也意味着同一个张量会同时被一组视为 FA 块、被另一组视为 SSM 块。

对于像 Nemotron-H 这样的模型，最终布局如下：

```
                KV Cache Tensor (shared via HMA pooling)
                 /                        \
                /                          \
     Attention (FA) View              Mamba View
              |                            |
    +-----------------------+    +-----------------------+
    | Block 0               |    | Block 0               |
    |   Key     |  Value    |    |  Conv |    SSM  |[pad]|
    | Block 1               |    | Block 1               |
    |   Key     |  Value    |    |  Conv |    SSM  |[pad]|
    |  ...                  |    |  ...                  |
    +-----------------------+    +-----------------------+

```

页大小不同：FA 页由 `block_size * num_kv_heads * head_dim` 决定（K/V 再 \*2），而 SSM 页是 `conv_state_bytes + ssm_state_bytes`。
HMA 会增大 FA 的 block\_size 直到大于 Mamba 的页大小，然后对 Mamba 行做填充（`+[pad]`），使两组的页大小（按字节计）相等，从而启用共享张量方案。

**NIXL 面临的问题**：单一描述符列表若使用统一的 `(address, length)` 条目，就无法正确索引两个视图。我们需要把 K/V（Conv/SSM 同理）注册到分开的描述符上，以便在**异构配置**（即 D TP != P TP）下支持对 K/V head 的索引。

块 `b` 的 FA 描述符指向 `base + b * page_size`，长度为 `fa_block_len`。同一块 `b` 的 Mamba 描述符指向相同的 `base + b * page_size`，长度却是 `conv_size` 或 `ssm_size`。二者并不相同。

---

## 双描述符视图

我们的解决方案是在同一块物理内存上注册**两个独立的描述符列表**，将它们拼接起来并由单个 NIXL 传输句柄指向：

```
+------------------------------------------------------+
|  FA descriptors (M regions x N_phys blocks)          |
|                                                      |
|  Region 0                                            |
|    FA_desc_K[0], FA_desc_K[1], ... FA_desc_K[N-1]    |
|    FA_desc_V[0], FA_desc_V[1], ... FA_desc_V[N-1]    |
|  Region 1                                            |
|    ...                                               |
|  Region M                                            |
|    ...                                               |
|                                                      |   ^
|  --------------------------------------------------- |   | num_descs
|                                                      |   v
|  Mamba descriptors (M regions x N_log blocks)        |
|                                                      |
|  Region 0                                            |
|    Mamba_desc_x[0]   ... Mamba_desc_x[N-1]           |
|    Mamba_desc_B[0]   ... Mamba_desc_B[N-1]           |
|    Mamba_desc_C[0]   ... Mamba_desc_C[N-1]           |
|    Mamba_desc_SSM[0] ... Mamba_desc_SSM[N-1]         |
|  Region 1                                            |
|    ...                                               |
|  Region M                                            |
|    ...                                               |
+------------------------------------------------------+

```

> 注意：这里的 `N_phys/_log` 分别表示物理块和逻辑块。你可以假设 `N_phys=N_log=N`，什么时候不成立请参见下一节。

> 注意：上面的 Mamba 部分已经反映了把 conv 状态分解为 x、B、C 三个子投影的做法，详见下文 [3 描述符 conv 传输](#the-3-descriptors-conv-transfer)。对于同构 TP，它们可简化为两个子区域（Conv、SSM）。

FA 描述符占据前 `num_descs = M * N_phys` 个槽位。Mamba 描述符紧随其后。块 ID 的映射变为：

```
if is_fa_group:
    desc_id = region_id * N_phys + block_id
else:  # mamba group
    desc_id = mamba_region_id * N_log + block_id + num_descs
```

---

## 物理块大小 vs. 逻辑块大小

第二个复杂之处来自注意力内核的要求。FlashInfer 等后端要求特定的物理块大小（例如 16 个 token），它可能与用户设置或 HMA 计算出的逻辑块大小不同。

对标准模型，这用一个简单的比率处理：

```
physical_blocks = logical_blocks * ratio
ratio = logical_block_size / kernel_block_size

```

对混合模型，该比率**只适用于 FA 层**。SSM 层没有可拆分的"token"维度，因此始终直接使用 `logical_blocks`。这意味着描述符列表的 FA 部分和 Mamba 部分使用不同的块数：

```
FA section:    M regions * N_phys blocks    (N_phys = N_logical * ratio)
Mamba section: M regions * N_logical blocks

```

这通过 `_physical_blocks_per_logical` 字段来跟踪，它按引擎分别计算（因为当 P 与 D 的 TP 大小不同时，比率也会不同）。`_get_block_descs_ids` 中的块 ID 到描述符 ID 映射会根据解析的是 FA 组还是 Mamba 组来使用相应的步长。

---

## 3 描述符 conv 传输

对于同构 TP（P 与 D 使用相同的 `--tensor-parallel-size`），传输 SSM 状态很简单：每个 D rank 从对应的 P rank 读取相应的 conv + SSM 块。

异构 TP 让这件事变难了。考虑 `P_TP=1, D_TP=4`：四个 D worker 都要从单个 P worker 读取各自分片的 conv 和 SSM 状态。SSM 时间状态沿 `heads` 维度分片，而它是第一个轴——所以切片非常简单。但 conv 状态的结构是：

```
Conv state = [x | B | C]     where x, B, C are sub-projections
              ^   ^   ^
              |   |   |
     intermediate_size / TP   groups_ss / TP   groups_ss / TP

```

在标准的 SD 布局 `(state_len, dim)` 下，这些子投影在内存中是交错的。一个只想要自己那份 `x` 的 D worker 需要收集不连续的字节——这对零拷贝 RDMA 来说并不现实。

### DS 布局方案

我们要求 conv 状态使用 **DS 布局** `(dim, state_len)`（通过 `VLLM_SSM_CONV_STATE_LAYOUT=DS` 设置）。在这种布局下，每个子投影的数据在内存中是连续的：

```
DS layout within one page:

|--- x (x_bytes) ---|--- B (b_bytes) ---|--- C (b_bytes) ---|--- SSM ---|

```

现在每个 D rank 可以用三次独立、连续的 RDMA 读，读到自己那份 `x`、`B`、`C` 的切片——这就是"3 描述符传输"（我们实际仍只发起一次 NIXL READ）。

对于异构 TP，`remote_conv_offsets` 方法会计算每个 D rank 的切片位于 P 页中的位置，并考虑 TP 比率。
这使每个 Mamba 层有 4 个描述符区域（x、B、C、SSM），而同构情况下只有 2 个区域（Conv、SSM）。代价是描述符列表更大，但 RDMA 传输本身仍然是高效的连续读取。

任何一侧 GPU 都**不分配额外的内存中转缓冲区**。
任何一侧都**不需要重排数据**。

> 注意：在常规同置部署中使用 DS 布局时，我们没有测到明显的内核性能回退。未来版本中我们可能把标准布局统一改为 DS。

### 零开销：无额外缓冲区、无重排

一个更简单的替代方案是把整个 conv 状态传输给每个 D rank，然后在本地做置换/切片成正确形状。但对 Mamba 来说，我们刻意避免这种做法：

- **无中转缓冲区**——在 D 侧做置换需要在每个 D worker 上分配一个与 P 的完整 conv 状态等大的临时缓冲区。对于 Nemotron-H 这类模型，每个块的 conv 状态已经不小（bf16 下为 `3 * 3072 * 2 bytes`）。乘以数千个块和所有 Mamba 层，这一开销会不断累积，挤占本可用于 KV 缓存的空间。
- **传输后无需重排**——有了 DS 布局，每个 D rank 读到的恰好是它需要的字节，并且直接写入 KV 缓存中的最终位置。不需要传输后 rearrange 数据的内核。传输一完成，状态立即可用。
- **只传输自己拥有的部分**——每个 D rank 只传输自己 `1/TP` 的 conv 状态份额，而不是完整状态。对于 `D_TP=4`，与"全部传输、本地切片"的方式相比，每个 rank 的数据量减少 4x。
- **跳过 HMA 填充**——回顾一下，HMA 会对 SSM 页做填充使其与 FA 页大小一致。Mamba 描述符按实际的 `conv_bytes + ssm_bytes` 设置大小，而不是填充后的页大小。这意味着我们从不在线路上传输填充字节——只传输真实状态。对于填充很可观的模型（例如 FA 页大小远大于原始 SSM 状态时），这可以显著减少每个块的传输量。

下图在 Nemotron Super 120B、TP=4（HMA 设定的 FA block\_size=4224）上验证了零开销传输优化。对每种 KV 缓存 dtype（bf16 和 fp8），我们把*朴素（Naive）*基线——为 Mamba 块传输完整的 HMA 填充页——与*最优（Optimal）*方案——只传输实际的 conv + SSM 字节，跳过所有 HMA 填充和/或辅助缓冲——进行比较。
我们首先通过传输指标验证我们的方法达到了指标所报告的 *Optimal* 水平。

对于 **fp8**，FA 页更小（每元素 1 字节 vs 2 字节），因此该配置下填充可以忽略不计。
随后我们展示了 **bf16** 配置下的节省，我们的方案消除了每请求约 50 MB 的不必要传输。

由于 Mamba 状态是每请求固定大小的摘要，传输量随 ISL 增大而按 FA 块数扩展。

![Figure 1: P→D transfer volume vs. input sequence length for Nemotron Super 120B (TP=4, FA block_size=4224). The Naive and Optimal baselines are computed analytically from the model's page sizes and block counts. The Measured line reports the actual bytes transferred (as reported by NIXL) during disaggregated P/D serving. Our approach (Optimal) eliminates HMA padding overhead, which is reflected in the measured transfer.](https://vllm.ai/blog-assets/figures/2026-04-21-hybrid-ssm-disagg/transfer-volume-vs-isl.png)

图 1：Nemotron Super 120B（TP=4，FA block\_size=4224）的 P→D 传输量与输入序列长度的关系。Naive 与 Optimal 基线由模型的页大小和块数解析计算得出。Measured 线报告分离式 P/D 服务期间实际传输的字节数（由 NIXL 报告）。我们的方案（Optimal）消除了 HMA 填充开销，这一点也反映在实测传输量中。

---

## 组装起来：Nemotron-H 示例

让我们走一遍具体例子：以 TP=2 分离式 P/D 服务 `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8`。

**模型结构**：共 52 层，Mamba 与 FA 交替排列。HMA 把它们分成 5 组（4 个 Mamba 组，1 个 FA 组）。经过内存汇集后，得到 6 个共享 KV 缓存张量。

**KV 缓存布局**：

```
FA layers:    [num_blocks, 2, block_size=400, 4, 128]   # K/V with HMA-inflated block_size
SSM layers:   [num_blocks, 3, 3072]  (conv)  +  [num_blocks, 48, 64, 128]  (ssm)

```

HMA 调整块大小，使两个视图的页大小（按字节计）一致。内核（FlashInfer/FlashAttention）可能进一步细分 FA 块，从而形成物理/逻辑比率。

**描述符注册**：

1. 6 个共享张量作为 NIXL 内存区域注册（与稠密模型相同）。
2. 为全部 6 个区域 × `N_phys` 个块创建 FA 描述符，K 和 V 分开索引。
3. 追加 Mamba 描述符：6 个区域 × `N_logical` 个块，每个块 4 个子区域（x、B、C、SSM），用于 3 描述符传输。

**传输流程**：

1. P 完成预填充。调度器按组分配块 ID：`[[fa_block_ids], [mamba_block_ids_g0], [mamba_block_ids_g1], ...]`。
2. D 接收块 ID 并映射到描述符索引：FA 块使用标准的 `region * N + block_id` 公式；Mamba 块加上 `num_descs` 偏移并使用 `N_logical` 步长。
3. D 用 FA 与 Mamba 两组描述符发起一次 `make_prepped_xfer` READ，然后轮询完成状态。
4. 完成后，D 通知 P，使其可以释放这些块。

从 D 的视角看，整个传输是单个异步操作。无中间缓冲区，无数据重排。

---

## 性能

我们在通过 NVLink 互联的 8x H200 GPU 上，将分离式 P/D 与同置（co-located）服务进行了基准对比。模型是 `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-FP8`，一个近期的 120B LatentMoE 混合架构，Mamba2 与全注意力层交错排列。

- **同置基线**：单实例，TP=8，使用全部 8 张 GPU。
- **分离式 P/D**：1 个预填充实例（TP=4，4 张 GPU）+ 1 个解码实例（TP=4，4 张 GPU），GPU 总数相同。

我们把并发从 8 个用户扫到 256 个并发用户，绘制每 GPU 输出吞吐量相对每用户输出 token 速率（*交互性*）的曲线。工作负载使用 ShareGPT 作为测试数据集。

所有运行都使用非常高的 warmup 值，以确保 KV 缓存被"打乱"，从而避免当请求块恰好连续分配时出现的初始性能*提升*。这更贴近常规的长时间运行场景。也可以通过检查指标中报告的描述符数量是否恒定（在整个数据集扫描过程中）来验证这一点。

![Figure 2: Disaggregated P/D vs. co-located serving for a hybrid SSM model. Throughput-vs-latency Pareto curve across concurrency levels. Prefix-caching disabled.](https://vllm.ai/blog-assets/figures/2026-04-21-hybrid-ssm-disagg/disagg-vs-colocated.png)

图 2：混合 SSM 模型的分离式 P/D 与同置服务对比。不同并发级别下的吞吐量-延迟 Pareto 曲线。已禁用前缀缓存。

结果显示出与标准 Transformer 模型分离式服务相同的模式：在较大批规模下，分离式 P/D 相对同置基线呈 Pareto 占优。通过把解码与预填充干扰隔离，解码实例可以维持更大的批次而不停顿，在高并发下带来显著更高的每 GPU 输出 tok/s。

---

## 快速上手

要以分离式 P/D 运行混合 SSM 模型：

```
# Prefill instance
VLLM_SSM_CONV_STATE_LAYOUT=DS vllm serve nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8 \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.85 \
    --trust-remote-code \
    --max-model-len 8192 \
    --block-size 128 \
    --no-disable-hybrid-kv-cache-manager \
    --kv-transfer-config '{"kv_connector":"NixlConnector","kv_role":"kv_both"}'
```

> 注意：设置 `VLLM_SSM_CONV_STATE_LAYOUT=DS` 的 DS conv 状态布局是异构 TP 所必需的，其他情况下不需要。

---

## 局限与后续工作

- **Mamba1 模型**：3 描述符 conv 传输目前只支持 Mamba2。Mamba1 的 SSM 时间形状 `(intermediate_size // tp, state_size)` 无法还原 `intermediate_size`，而 conv 分解需要它。类似地，**GDN** 支持（Qwen3.5+）已列入分离部署[路线图](https://github.com/vllm-project/vllm/issues/33702)。
- **投机解码**：SSM 状态传输与投机解码之间的交互尚未经过充分验证。
- **HMA 下的混合块大小**：启用 HMA 时，尚不支持 P 与 D 使用不同块大小（`block_size_ratio > 1`）。

---

## 致谢

Thomas Parnell（IBM Research）、Roi Koren（NVIDIA）

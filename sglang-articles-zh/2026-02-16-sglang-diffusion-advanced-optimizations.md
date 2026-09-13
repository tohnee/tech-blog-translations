---
title: "SGLang-Diffusion：面向生产级视频生成的高级优化"
title_en: "SGLang-Diffusion: Advanced Optimizations for Production-Ready Video Generation"
author: "The SGLang-Diffusion Team"
date: "February 16, 2026"
previewImg: /images/blog/sgl-diffusion/sgl-diffusion-banner-16-9.png
source: https://lmsys.org/blog/2026-02-16-sglang-diffusion-advanced-optimizations/
translated: 2026-09-12
---

# SGLang-Diffusion：面向生产级视频生成的高级优化

> 原文：[SGLang-Diffusion: Advanced Optimizations for Production-Ready Video Generation](https://lmsys.org/blog/2026-02-16-sglang-diffusion-advanced-optimizations/) · LMSYS Blog · The SGLang-Diffusion Team

继[两个月进展回顾](https://lmsys.org/blog/2026-01-16-sglang-diffusion/)之后，我们很高兴与大家深入分享一系列高级优化——正是这些优化让 SGLang-Diffusion 成为一个生产就绪的视频生成框架。这些改进聚焦于可扩展性、效率与稳定性，而这正是在大规模部署扩散模型时的关键所在。

以下是我们近期的工作内容：

## 概览

随着视频生成模型的复杂度持续提升，我们识别并解决了贯穿整个推理管线的多个关键瓶颈：

- **更智能的并行**：token 级序列分片与并行折叠（Parallel Folding），实现资源利用的最优化
- **分布式 VAE**：并行编码/解码，消除高分辨率视频的内存瓶颈
- **生产就绪的推理服务**：修复 Cache-DiT 集成缺陷，实现稳定的多请求服务
- **优化的 I/O**：消除不必要的序列化，加速视频保存操作
- **融合算子**：为 LayerNorm 变体定制 JIT 算子，减少 GPU 气泡

下面进入技术细节。

## 关键改进

### 1. SP 分片改进：从帧级到 token 级

对视频 DiT 模型而言，输入张量的形状通常为 `B, T, H, W, C`。以 `num_frames=81` 的常见配置为例，形状可能是 `1, 21, 90, 160, 3`。

在配备 Ulysses 序列并行（N=8）的 8×H100 环境中，框架需要在非注意力操作时沿序列维度分片，再通过 all-to-all 通信切换到按注意力头维度分片以执行注意力计算。

#### 旧方案：帧级分片

我们最初的实现直接沿 `T`（时间）维度分片。但 21 帧无法被 8 张 GPU 整除，于是只能采用两种次优方案：

1. **调整帧数**：在预处理阶段修改 `num_frames`，使 T 能被 N 整除
2. **Token 填充**：将时间维度填充到 N 的下一个倍数（21 → 24）

帧级填充会带来可观的开销：每个被填充的 token 都需要 `H × W × C` 次冗余计算。

#### 新方案：token 级分片

为了把填充开销降到最低，我们现在**在分片前先把 `T × H × W` 展平为单一的序列维度**。这带来两大好处：

- **填充更少甚至为零**：对于常见分辨率与 VAE 配置，`H × W` 通常能被 8 整除，可以完全免去填充
- **通信量更低**：即便仍需填充，其开销相比帧级填充也微乎其微

### 对比：形状与通信量分析

| 方案 | 填充开销 | 每个分片（rank）的输入张量形状 | All-to-All 通信量 |
|--------------------|------------------|-------------------------------|------------------------|
| **帧分片** | 3 帧（14.3%） | `3, 90, 160, C`（24/8） | `1.0 × feature_map` |
| **token 分片** | 0 帧 | `2.625, 90, 160, C`（21/8） | `0.875 × feature_map` |

这一优化同时带来了更快的通信和更低的内存占用，对视频模型尤其有效。

相关技术细节参见该 [PR](https://github.com/sgl-project/sglang/pull/18161)。

### 2. 并行折叠：解耦文本编码器与 DiT 的并行

在最初的实现中，文本编码器（Text Encoder）与 DiT 共用同一个张量并行（TP）组。当 DiT 只使用序列并行（SP）时，这意味着文本编码器只能以 TP=1 运行——每张 GPU 都要保存一份完整模型副本，内存和算力都被浪费了。

由于文本编码器与 DiT 的计算**完全解耦**，我们引入了**并行折叠（Parallel Folding）**：文本编码器现在把 DiT 的 SP 组当作自己的 TP 组来使用。

**实际效果：**

- **对文本编码器**：在 SP 组内应用 TP，最大化速度并降低内存占用
- **对去噪器（Denoiser）**：应用 SP，优化序列处理的吞吐量与内存

这种做法让两个组件都能在互不干扰的情况下采用最优并行策略，整体效率得以提升。

相关技术细节参见该 [PR](https://github.com/sgl-project/sglang/pull/17818)。

### 3. 并行 VAE：分布式编解码

VAE 的编码/解码涉及大量 3D 卷积运算。对高分辨率视频来说，单 GPU 实现既慢又容易 OOM。

缓解这一问题的两种常见做法是：

1. **分块（Tiling）**：把特征图切成小块依次处理——降低峰值内存，但增加延迟
2. **并行**：把分块分发到多张 GPU 上并发处理——峰值内存和延迟都能降低

我们为 Wan-VAE 实现了**并行 VAE**，策略如下：

- **按高度分片**：沿高度维度在各个 rank 间切分特征图
- **卷积操作**：使用 `halo_exchange` 在相邻 rank 之间（P2P）共享边界像素，保证与全局卷积在数学上完全等价
- **注意力操作**：在需要全局上下文时使用 `all_gather`
- **结果聚合**：在编解码结束时用 `all_gather` 重建完整高度

这一方案让 VAE 不再成为高分辨率视频生成的瓶颈，可以在不 OOM 的前提下支持更高分辨率和更长的序列。

### 4. Cache-DiT 推理服务：修复多请求稳定性

SGLang-Diffusion 中的 [Cache-DiT](https://github.com/vipshop/cache-dit) 通过缓存残差并跳过冗余计算来加速推理。但它能否正确工作，取决于 `num_inference_steps` 的正确配置——该参数决定了步数计数和选择性计算掩码（Selective Computation Mask, SCM）。

**问题所在：**

Wan2.2 采用双 transformer 架构，`transformer` 与 `transformer_2` 分别执行 `num_high_noise_steps` 和 `num_low_noise_steps`（两者之和为 `num_inference_steps`）。我们最初的实现存在两个关键缺陷：

1. 两个 transformer 都错误地使用总的 `num_inference_steps` 来配置各自的缓存上下文
2. 在服务模式下，缓存上下文会跨请求持续存在，即使不同请求使用了不同的 `num_inference_steps`

这些问题会导致步数计数错误和缓存缓冲区污染。当相邻请求的视频形状不同时，缓存缓冲区会出现形状不匹配，进而**导致服务器崩溃**。

**我们的解决方案：**

1. `transformer` 与 `transformer_2` 现在分别使用 `num_high_noise_steps` 和 `num_low_noise_steps` 来配置各自独立的缓存上下文
2. 对每个新请求，我们重新计算时间步切分，并通过 Cache-DiT 的 API **刷新**缓存上下文，实现请求间的完全隔离

由此确保了 Cache-DiT 加速下稳定、生产就绪的推理服务。

### 5. 优化视频保存：消除序列化开销

在我们的服务架构中，`scheduler_client` 与 `gpu_worker` 通过 ZMQ 通信。

此前，`gpu_worker` 的流程是：

1. 完成推理
2. 序列化输出张量
3. 通过 ZMQ 把张量发送给 `scheduler_client`
4. `scheduler_client` 反序列化张量
5. `scheduler_client` 处理张量并保存视频

这带来了可观的序列化/反序列化和内存拷贝开销。

**我们的解决方案：**

现在 `gpu_worker` 直接处理输出张量并把视频写入磁盘，只把文件路径返回给 `scheduler_client`。

这样既消除了序列化/反序列化开销，也避免了重复的张量拷贝。

### 6. WanVideo LayerNorm 融合：CuTeDSL JIT 算子

WanVideo 引入了两种特殊的 LayerNorm 模式：

1. **LayerNormScaleShift**：`y = LN(x) * (1 + scale) + shift`

2. **ScaleResidualLayerNormScaleShift**：
    - `residual_out = residual + gate * x`
    - `y = LN(residual_out) * (1 + scale) + shift`

这些模式将逐元素操作与归一化归约组合在一起。如果把它们作为独立的算子分别实现，会引入多次算子启动和中间显存读写，造成 GPU 气泡。

**我们的解决方案：**

我们用 CuTeDSL 实现了**融合 JIT 算子**（位于 [`sglang/jit_kernel/diffusion/cutedsl`](https://github.com/sgl-project/sglang/tree/main/python/sglang/jit_kernel/diffusion/cutedsl)），把这些操作合并成单个高效的算子。

**收益：**

- **更少的算子启动**：降低启动开销
- **更低的内存流量**：消除中间读写
- **更高的 GPU 利用率**：减少气泡、提升吞吐量

这些微优化累加起来效果可观，对 WanVideo 这类多层架构尤其明显。

## 性能结果

以下是不同设置下 SGLang-Diffusion 与 LightX2V 在 Wan2.2 T2V 上的对比：

<iframe style="display:block; margin: auto;" width="838" height="523" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQRK_j_q8NXZKEqtrTBagxFxvvaxYXXB56HTqqYlD_aAv1v74WKle2HIc7HPK3P0ZVrYlZrjshKYnaV/pubchart?oid=677973346&amp;format=interactive"></iframe>

## 下一步计划

我们将继续突破扩散模型推理服务的边界。更多细节请参阅 [**SGLang-Diffusion 26Q1 路线图**](https://github.com/sgl-project/sglang/issues/18286)。

我们会持续为生产部署优化 SGLang-Diffusion，敬请期待更多更新。

## 致谢

- 我们感谢以下贡献者为这些优化所做的努力：
  **Skywork.ai、[Song Rui](https://github.com/Songrui625)、SGLang-Diffusion 团队**
- 特别感谢我们的算力合作伙伴的持续支持。

体验由 SGLang-Diffusion 强力驱动的扩散生成：[APIFree](https://www.apifree.ai/home)

## 了解更多

- **Slack 频道**：[#diffusion](https://sgl-fru7574.slack.com/archives/C09P0HTKE6A)（通过 slack.sglang.io 加入）
- [**SGLang-Diffusion Cookbook**](https://cookbook.sglang.io/docs/diffusion)
- [**SGLang-Diffusion 文档**](https://github.com/sgl-project/sglang/blob/main/python/sglang/multimodal_gen/docs)
- [**上期更新：两个月进展回顾**](https://lmsys.org/blog/2026-01-16-sglang-diffusion/)

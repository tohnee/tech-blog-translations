---
title: "Qwen3.8-Flash-Next：SGLang 的 Day-0 支持"
title_en: "Qwen3.8-Flash-Next: Day-0 Support in SGLang"
author: "SGLang Team"
date: "August 26, 2026"
previewImg: /images/blog/qwen-flash-next/cover.png
type: blog
source: https://lmsys.org/blog/2026-08-26-qwen-flash-next/
translated: 2026-09-12
---

# Qwen3.8-Flash-Next：SGLang 的 Day-0 支持

> 原文：[Qwen3.8-Flash-Next: Day-0 Support in SGLang](https://lmsys.org/blog/2026-08-26-qwen-flash-next/) · LMSYS Blog · SGLang Team

## 引言

今天，Qwen 团队开源了 **Qwen3.8-Flash-Next**——一个多模态 MoE 模型，也是 **Qwen4** 架构的早期预览。它在 Qwen4 中扮演的角色，正如当年 Qwen3-Next 之于 Qwen3.5。**Gated DeltaNet + Gated Attention** 混合设计从 Qwen3.5 一路沿用到 Qwen3.8。SGLang 与 Qwen、NVIDIA、AMD 团队合作，为该模型提供了 Day-0 支持（首发日支持）。

**Qwen3.8-Flash-Next** 在多个方面对架构进行了升级：

- **GDN + QSA 混合注意力**：Gated DeltaNet（GDN）高效压缩历史信息，Qwen Sparse Attention（QSA）则通过一个轻量级索引器在微块（micro-block）粒度上挑选重要上下文，使长序列的注意力开销保持在低位。
- **门控残差（Gated Residual，GR）**：将残差流扩展为 4 条分支，并用动态门控控制读写，强化跨层信息流动。
- **N-gram Embedding**：基于局部上下文进行查表，为常见短语和局部模式提供额外表示，以极小的额外计算量扩展模型容量。

**亮点**：

- **混合架构**：125B 参数的主模型，外加额外的 51B N-gram Embedding，每个 token 激活 6B 参数。共 48 层：36 层 GDN 线性注意力层与 12 层 QSA 稀疏注意力层。MoE 层使用 512 个专家、top-10 路由。
- **我们量化的 NVFP4 checkpoint**：[RadixArk/Qwen3.8-Flash-Next-NVFP4](https://huggingface.co/RadixArk/Qwen3.8-Flash-Next-NVFP4)，Day-0 发布。
- **N-Gram Embedding**：将 N-gram 嵌入卸载到主机内存，大幅降低 GPU 显存占用；异步预取使其与模型计算重叠，几乎没有额外开销。
- **Gated Residual：与 NVIDIA 共同构建、通过 FlashInfer 交付**：经由低延迟单 GEMM 路径实现高性能的 Mix/Combine HyperConnection 算子（算子级 2.05× 加速）。
- **GDN+QSA**：面向 GDN+QSA 混合架构的 KV 缓存内存管理，兼容基数树缓存（Radix Cache）。
- **投机解码（Speculative Decoding）**：为 MTP 草稿模型加入索引复用（index-reuse）特性，缩短长上下文下草稿模型的索引器耗时。在 B200 上以 TP4 配置运行，NVFP4 checkpoint 在 batch size 1 且开启 MTP 时解码速度达 **540 tok/s**，接受长度（accept length）为 3.3（含额外奖励 token）。

启动命令与面向不同负载的配置指南见 [SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/Qwen/Qwen3.8-Flash-Next)。

## 模型架构

<p align="center">
  <img src="/images/blog/qwen-flash-next/qwen3.8-next-architecture.svg" alt="Qwen3.8-Flash-Next Architecture" width="60%">
</p>

- **GDN+QSA 混合架构**：沿用 Qwen3.5 引入的架构设计，Qwen3.8-Flash-Next 采用 GDN + 注意力的混合架构：每 4 层中有 3 层 GDN 层将历史压缩为固定大小的状态，剩余 1 层则在完整上下文上执行精确检索。针对全局注意力层，Qwen3.8-Flash-Next 进一步引入 **Qwen Sparse Attention（QSA）**，以应对上下文变长时计算量与 KV 缓存访存开销双双大幅增长的问题。稀疏注意力通过只关注重要上下文来降低长序列计算量；QSA 更进一步：它先把序列聚合成微块（micro-block），在块级别估计重要性，然后挑选最相关的区域，同时降低了索引开销与注意力开销。
- **门控残差（Gated Residual，GR）**：融合了两个思路：一是跟随 Hyper-Connection，把残差流扩展为多条分支；二是将 GatedNorm 风格的**逐元素动态门控**引入残差读取。原本单一的残差流被扩展为 **4 条并行分支**，让模型能够根据当前内容动态决定从每条分支读取多少信息、又写回多少。
- **N-gram Embedding**：使用"当前 token 加上前若干个 token"构成的局部上下文进行查表，为常见短语和局部模式提供额外表示，而几乎不增加每个 token 的计算开销。N-gram Embedding 可以完全驻留在主机内存中以节省 GPU 显存：查表位置提前算好并异步预取，因此它从不长期占用 GPU 显存。最终，模型只在网络开头附近使用**单个 N-gram Embedding 层**，以相对较低的成本添加了一个大规模的"局部模式记忆"。
- **IndexShare MTP**：draft-extend 过程针对目标模型刚接受的 token 计算出的 QSA top-k 选择，会在整个 MTP 迭代期间保持不变，因此每个草稿解码步骤都可以跳过索引器，直接读取这份冻结的选择结果以及其后草拟出的位置。在长上下文场景下，这能显著加快 MTP 草稿步骤。


## Qwen Sparse Attention：粗粒度检索，精确注意力

Qwen3.8-Flash-Next 使用压缩比为 4 的压缩版 QSA，即 **c4**。每个 QSA 层有两条路径：一个轻量级索引器决定*去哪里看*，稀疏 GQA 则从原始注意力 K/V 缓存中读取被选中的条目。

<p align="center">
  <img src="/images/blog/qwen-flash-next/qwen4-qsa-dataflow.svg" width="98%" alt="QSA index and attention data flow in SGLang.">
</p>

索引器投影出 4 个 128 维查询头和 1 个共享键头。每 4 个原始索引键在 FP32 下取平均、归一化，并用第一个 token 的 MRoPE 位置做旋转，形成一个压缩键。查询用下式对可见的压缩块打分：

$$
s_{t,b} = \frac{1}{\sqrt{128}}
\sum_{h=1}^{4}
\mathrm{ReLU}
\left(\left\langle q^I_{t,h}, \bar{k}^I_b \right\rangle\right).
$$

QSA 保留得分最高的 512 个块，把它们展开回 2048 个逻辑 token 位置，并附上当前未满块中的 0–3 个 token。因此最终的稀疏注意力最多看到 2051 个位置。重要的是，压缩键只充当索引：最终的 softmax 和 value 聚合使用的是**原始、未压缩的 K/V**。

这意味着 QSA 用少量缓存容量换来了低得多的长上下文计算量与内存流量。索引器大约扫描 $L/4$ 个小键，随后稀疏注意力只读取约 2K 条完整 K/V 条目，而不是全部 $L$ 条。模型层面的 KV 节省来自混合布局：48 层中只有 12 层存储不断增长的注意力 K/V，其余 36 层 GDN 层使用固定大小的状态——而不是因为在 QSA 层内部丢弃了 K/V。

SGLang 只把索引器挂载到全注意力层上，并复用这些层的 MRoPE 实现。原始 K/V 仍保留在常规分页内存池中。QSA 每 4 个 token 增加一个 BF16 压缩索引键；未满块的原始键存放在每请求一个的四槽环形缓冲区中。这避免了为完整上下文保留原始索引键，把 QSA 的索引缓存开销降低了 80%。按页对齐的 `full_slot / 4` 寻址方式让压缩缓存可以直接跟随 Radix Cache 的所有权管理，无需单独的生命周期。

预填充阶段，一个定制的 GPU 内核计算索引得分，一个快速 top-k 挑出块，再由 Triton 展开索引并执行稀疏 GQA。解码阶段使用同一打分器的分页版本，压缩被选中的原始 K/V，然后在 Blackwell 上派发给 TRTLLM-Gen，其他平台则使用打包版 FlashAttention。索引器可以在第二条 CUDA 流上与主 Q/K/V 投影重叠执行，元数据路径与 CUDA 图兼容。


## IndexShare MTP：在草稿步骤间复用 QSA 选择结果

QSA 层先运行一个**索引器**挑选需要关注的 token，然后只对这些 token 执行稀疏注意力。第二阶段的 token 预算是固定的；第一阶段则要让它的查询与全部 `⌈L/4⌉` 个压缩块打分，因此当上下文超过几千 token 后，决定该层成本的是索引器，而不是它所服务的注意力。投机解码会成倍放大这一开销：设置 `--speculative-num-steps N` 时，一次 MTP 迭代要调用 `N` 次索引器（`N - 1` 次草稿解码前向加一次 draft-extend），才能让草稿最多前进 `N` 个位置。

因此，草稿解码步骤不再运行索引器。每次 MTP 迭代都以一次针对目标模型刚接受 token 的 draft-extend 开场，而这一步本来就要运行索引器；每个请求最后被接受的那一行就在这里被捕获，供整个草稿循环复用，查找时再用捕获之后草拟出的位置填充 `N + 1` 个额外列，这样草稿依然能看到自己正在生成中的 token。由于选择结果是一份**逻辑** token 索引列表，而请求只会增长，因此永远不会越界；又因为查询在 $L$ 个位置中最多移动了 `N` 个位置，复用的排序与索引器本应重新计算出的结果基本一致，接受长度保持不变。每个 MTP 迭代中草稿的索引器工作量从 `N` 次调用降至一次。那些只为给索引器供数而存在的小型元数据内核——包括压缩解码视图以及 pending-ring 与 group-ring 布局——也同样从草稿解码步骤中移除。

## HyperConnection 内核优化

HyperConnection（HC）维护 4 条并行残差流，而 Attention 与 MoE 只作用于单一隐藏状态。因此每个块都要用 **Mix** 从 4 条流中读取，并用 **Combine** 把输出写回。这里的 `M` 是一次调用处理的 token 数：解码与投机验证时很小，预填充时可达数千。我们根据 `M` 派发到不同的内核。

### Mix

Mix 通过一个低秩投影生成逐元素门控值，并把 4 条残差流归约为一个隐藏状态。对于 `M ≤ 16`，我们使用 [FlashInfer PR #4266](https://github.com/flashinfer-ai/flashinfer/pull/4266) 提供的低延迟 split-K CuTe GEMM。Split-K 将 K 维切分，让多个 CTA 并行处理同一输出区域，弥补 M 维并行度的不足。SiLU、Sigmoid、门控和最终归约被融合进两个 GEMM epilogue，避免中间结果写入全局内存。上投影权重经过离线重排，使每个输出的 4 个门控值可以在一个 tile 内完成局部归约。对于更大的 `M`，实现改用 cuBLAS，它在这些形状下效率更高。

在 NVIDIA B300、`M = 4` 时，融合路径把 Mix 延迟从 12.36 µs 降到 6.03 µs，即 **2.05× 的内核级加速**。在与此前 Triton 路径对比的端到端投机解码基准中，吞吐量提升 **7.6%**。

### Combine

Combine 计算 4 个注入系数，并对 4 条流施加残差更新。`M` 较大时，一个融合内核一次即可处理每个 token 行。`M` 较小时这种映射暴露出的 CTA 太少，因此 `M ≤ 32` 路径沿隐藏维度对每一行做切分。最终的双内核实现在提供足够并行度的同时，保持了参考实现的 FP32 累加顺序与逐位一致的输出。

在 `M = 4` 时，切分路径把 Combine 延迟从 4.17 µs 降到 2.13 µs，即 **1.96× 的内核级加速**。在另一组与原始"每行一个 CTA"内核对比的端到端基准中，吞吐量提升 **5.49%**。`M` 较大时，融合内核比基于 cuBLAS 的基线最快快 **2.54×**，有效带宽达 6144 GB/s。

形状感知的派发机制让 HC 在低延迟解码与大规模预填充两类场景中都能走合适的执行路径。

## 逐层嵌入（Per-Layer Embeddings，PLE）

### 架构

该模型将 PLE——一个**以哈希寻址的可学习 N-gram 嵌入存储**——放在第二个解码块（配置层 ID 为 2，对应从零开始的索引 1）。其 512 亿（51.2B）嵌入参数在 BF16 下约占 95.4 GiB，它们是固定的模型权重，而非 KV 缓存或可变的注意力内存。

对于 token `x_t`，8 个 2-gram 哈希头使用 `(x_{t-1}, x_t)`，8 个 3-gram 哈希头使用 `(x_{t-2}, x_{t-1}, x_t)`，共产生 16 个嵌入行 ID。每行贡献 160 个值，拼接成形状为 `[2560]` 的 `E_t`。

<p align="center">
  <img src="/images/blog/qwen-flash-next/qwen4-ple-offload.svg" width="98%" alt="PLE dataflow and SGLang's sparse pinned-host offload path.">
</p>

<p align="center">
  <em><b>位于第二个解码块的 PLE。</b>稀疏 N-gram 检索的结果在 HC Mix 之前经门控注入 4 条 HC 分支。SGLang 把词表并行的表分片移到锁页主机内存（pinned host memory），每个 token 只 gather 被选中的 16 行。</em>
</p>

$$
E_t \in \mathbb{R}^{2560}
\longrightarrow
K_t \in \mathbb{R}^{4 \times 2560},
\qquad
V_t \in \mathbb{R}^{2560}
$$

$$
R_t \in \mathbb{R}^{4 \times 2560}
\longrightarrow
Q_t \in \mathbb{R}^{4 \times 2560}
$$

$$
g_t = \mathrm{Gate}(\mathrm{Norm}(Q_t), \mathrm{Norm}(K_t))
\in \mathbb{R}^{4 \times 1},
\qquad
U_t = g_t \odot V_t
$$

$$
\Delta_t = U_t + \mathrm{SiLU}(\mathrm{DWConv}(\mathrm{RMSNorm}(U_t)))
$$

$$
\widetilde{R}_t = R_t + \Delta_t,
\qquad
\widetilde{R}_t \xrightarrow{\mathrm{HC\ Mix}} h_t \in \mathbb{R}^{2560}
$$

第四行通过把门控后的值与其短卷积输出相加来形成 PLE 增量；第五行将该增量注入 HC 状态。PLE 为每个请求保留两个本地状态：用于哈希的最近两个 token ID，以及形状为 `[10240, 9]` 的短卷积历史。目标模型在预填充、解码和目标验证阶段都保留 PLE；只有单层的 MTP 草稿模型将其禁用。

### 稀疏锁页主机内存卸载

由于每个 token 只触及 16 行，SGLang 把每个 rank 的词表并行表分片保存在锁页主机内存中，并用一个 Triton UVA 内核把被选中的行 gather 到一个小的 BF16 GPU 缓冲区。一条专用 CUDA 流让 gather 与第一个解码块重叠执行。既有的 TP 归约与 DP gather/scatter 路径保持不变：卸载改变的只是存储位置，而非表的归属关系或 PLE 的数学逻辑。当模型实际 dtype 为 BF16 时，这条 CUDA 路径默认启用，并且与 KV 缓存卸载或通用层卸载相互独立。

在 H200 上以 TP4 与 MTP-213（2 个草稿步、top-k 1、每次目标验证产生 3 个草稿 token）的配置测试，卸载使每张 GPU 的目标模型权重从 83.91 GiB 降到 60.45 GiB（**-23.46 GiB**），并在相同显存占比（memory fraction）下把可分配的 KV 容量从 184 万（1.84M）token 提升到 328 万（3.28M）token（**+78.54%**）。在 1、2、4 路并发下，匹配条件下的吞吐量基本不变（几何均值 **-0.07%**）。4 个固定提示词各生成 128 个 token，输出 ID 完全一致；第一组用例记录的选中 token logprob 轨迹也完全一致。

## 致谢

本工作由 RadixArk 的 SGLang 团队与 Qwen、NVIDIA、AMD 合作完成。

**SGLang 社区**：Qiaolin Yu, Yuhao Yang, Cheng Wan, Xinyuan Tong, Zijie Xia, Ke Bao, Mingyi Lu, Haoguang Cai, Banghua Zhu, Ying Sheng

**Qwen**：Yi Zhang, Yizhong Cao, Guangda Liu

**AMD**：Andy Luo, Haichen Zhang

**NVIDIA**：NVIDIA 与 SGLang 共同优化了 Qwen3.8-Flash-Next 在 Blackwell 与 Hopper 上的性能。

---
title: "FastVideo 中的 Pika H3 Flex：快 7 倍，4-bit 下接近实时"
title_en: "Pika H3 Flex in FastVideo: 7x Faster, and Near Real Time in 4-bit"
date: 2026-11-03
source: https://haoailab.com/blogs/pika-h3-flex/
crawled: 2026-11-16
translated: 2026-11-16
---

# FastVideo 中的 Pika H3 Flex：快 7 倍，4-bit 下接近实时

> 原文：[Pika H3 Flex in FastVideo: 7x Faster, and Near Real Time in 4-bit](https://haoailab.com/blogs/pika-h3-flex/) · Hao AI Lab @ UCSD

2026 年 11 月 3 日 · 9 分钟 · Aryan Kumar、Will Lin、Hao Zhang

![FastVideo x Pika：FastVideo 中的 Pika-H3-Flex + NVFP4 QAD](https://haoailab.com/blogs/pika-h3-flex/img/cover.jpg)

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

[**Pika H3 Flex**](https://huggingface.co/Pika-Labs/Pika-H3-Flex) 能把一段提示词、首尾帧，或图像、视频与音频参考素材，变成音画同步的视频。它现在可以在 **FastVideo** 中运行，比官方代码最**快 7 倍**。我们还发布了用量化感知蒸馏训练的 **NVFP4 版本**：[BF16 注意力版](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD) 与 [FP4 注意力版](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD)：5 秒 480p 片段在单台 GB200 上只需 **5.8 秒**。

Flex 构建于 MiniMax H3——与我们 [FastH3](/blogs/fasth3-local/) 系列背后的模型相同——因此我们的 kernel、NVFP4 解码器与量化配方可以直接沿用。感谢 Pika 将其开源。

## TL;DR[#](#tldr)

* **接近实时。** 使用 NVFP4 模型，单台 GB200 上 5 秒 480p 片段只需 **5.8 秒**。
* **BF16 下也更快。** 单 GPU 比官方代码快 **2.4 倍**，四 GPU 上 15 秒片段快 **7 倍**。
* **NVFP4，为对齐而训练。** QAD 让两个 adapter 相对 BF16 模型的距离比普通量化缩小 14–17%，而 FP4 注意力让长片段**快 16%**。
* **本地可跑。** NVFP4 模型面向 Blackwell 硬件，最低可到 DGX Spark 与 RTX 5090：5 秒 480p FL2VA 片段在**单台 DGX Spark 上 59.5 秒**完成。
* **2K。** 任何 H3 系列视频都可以在 2560x1440 下重新生成。
* **开源。** [NVFP4 QAD 权重](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD)（[FP4 注意力版](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD)）、推理代码与完整训练配方。

## Pika H3 Flex 能做什么[#](#what-pika-h3-flex-does)

Flex 是 Pika 对 MiniMax H3 做后训练得到的模型，带两个 adapter：一个用于文本与关键帧任务，一个用于参考条件生成。它以六步采样，不使用 CFG，并使用稠密注意力。

| 任务 | 输入 | Adapter |
| --- | --- | --- |
| T2VA | 一段提示词 | `fl2va` |
| I2VA / L2VA / FL2VA | 首帧、尾帧，或两者 | `fl2va` |
| Ref2VA | 最多 9 张图片、3 段视频与 3 段音频 | `ref2va` |

## 相同提示词，四种方式[#](#same-prompt-four-ways)

每个场景都在单台 GB200 上以四种方式从相同提示词与随机种子生成：Pika 官方代码、FastVideo 的 BF16 版本，以及两个 NVFP4 QAD 模型。四个片段同步播放，每个格子显示其端到端耗时。

更快！文生视频
蓝调时刻文生视频
炮弹文生视频
烟花首帧生视频
篝火参考生视频

![](/blogs/pika-h3-flex/media/compare/official__v1_faster.jpg)

**Pika 官方** BF16*59.7 秒*

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v1_faster.jpg)

**FastVideo** BF16*26.6 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v1_faster.jpg)

**NVFP4 QAD** BF16 注意力*16.8 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v1_faster.jpg)

**NVFP4 QAD** FP4 注意力*15.2 秒*

![](/blogs/pika-h3-flex/media/compare/official__v2_bluehour.jpg)

**Pika 官方** BF16*59.7 秒*

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v2_bluehour.jpg)

**FastVideo** BF16*26.9 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v2_bluehour.jpg)

**NVFP4 QAD** BF16 注意力*16.9 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v2_bluehour.jpg)

**NVFP4 QAD** FP4 注意力*15.1 秒*

![](/blogs/pika-h3-flex/media/compare/official__v3_cannonball.jpg)

**Pika 官方** BF16*59.7 秒*

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v3_cannonball.jpg)

**FastVideo** BF16*27.1 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v3_cannonball.jpg)

**NVFP4 QAD** BF16 注意力*16.8 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v3_cannonball.jpg)

**NVFP4 QAD** FP4 注意力*15.2 秒*

![](/blogs/pika-h3-flex/media/compare/official__v4_fireworks.jpg)

**Pika 官方** BF16

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v4_fireworks.jpg)

**FastVideo** BF16*29.2 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v4_fireworks.jpg)

**NVFP4 QAD** BF16 注意力*18.2 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v4_fireworks.jpg)

**NVFP4 QAD** FP4 注意力*16.5 秒*

![](/blogs/pika-h3-flex/media/compare/official__v5_campfire.jpg)

**Pika 官方** BF16

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v5_campfire.jpg)

**FastVideo** BF16*75.4 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v5_campfire.jpg)

**NVFP4 QAD** BF16 注意力*61.7 秒*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v5_campfire.jpg)

**NVFP4 QAD** FP4 注意力*51.4 秒*

相同提示词、随机种子与分辨率（768p、5 秒），单台 GB200；时间为端到端耗时。

## BF16 下也更快[#](#faster-at-bf16)

在单台 GB200 上，官方代码为一个 5 秒 768p 片段花 20 秒做六次 DiT 前向，然后用 fp32 VAE **解码 38 秒**。FastVideo 用相同的权重把两者都压了下来：

* **FlashAttention-4** 取代 cuDNN SDPA。
* **融合的 H3 kernel** 去掉了 `cat`/`mul` 胶水代码（约占官方前向的 19%），更多融合 kernel 覆盖 QKV prologue、归一化、调制与 SwiGLU，在 BF16 下全部精确。
* **BF16 解码**，随后是我们的 NVFP4 解码器，把解码从 38 秒降到 1.5 秒。

DiT 去噪（6 次前向）
VAE 解码
其他

**5 秒 · 768p · 1 GPU**T2VA、1344×768、124 帧（37,718 token），单台 GB200，热启动中位数

官方 pika-h3-prodiffusers、cuDNN SDPA、fp32 VAE

**59.7 秒**

FastVideo BF16FA4 + 融合 H3 算子 + bf16 VAE

**25.1 秒***2.38×*

+ kernel + NVFP4 解码器融合 kernel、NVFP4 VAE 解码器

**17.6 秒***3.38×*

**15 秒 · 768p · 1 GPU**T2VA、1344×768、362 帧（109,070 token），单台 GB200，热启动中位数

官方 pika-h3-profp32 VAE

**224 秒**

FastVideo BF16FA4 + 融合 H3 算子 + bf16 VAE

**104 秒***2.15×*

+ kernel + NVFP4 解码器融合 kernel、NVFP4 VAE 解码器

**94.7 秒***2.37×*

**15 秒 · 768p · 4 GPU**T2VA、1344×768、362 帧，四台 GB200（序列并行），热启动中位数

官方，1 GPU参考点

**225 秒**

官方，4 GPUdiffusers Ulysses CP

**146 秒**

FastVideo BF16，4 GPU序列并行 DiT + VAE

**53.3 秒***对官方 4 GPU 2.73×**对官方 1 GPU 4.22×*

+ kernel + NVFP4 解码器4 GPU

**31.8 秒***对官方 4 GPU 4.58×**对官方 1 GPU 7.07×*

从提示词到带音频 MP4 的端到端秒数，一台或四台 GB200，模型常驻，热启动中位数。加速比是相对同等 GPU 数量上的官方代码；四 GPU 面板还给出相对官方单 GPU 的加速比。每个面板有各自的刻度。

到 15 秒时情况变了：一个片段有 109k token，稠密注意力随其平方增长，注意力占到每次前向的约 75%。这正是下面 FP4 注意力要针对的场景。

NVFP4 模型也能跑在本地 Blackwell 硬件上，例如 DGX Spark 与 RTX 5090。在单台 DGX Spark 上，NVFP4 QAD 模型（BF16 注意力）生成一个 5 秒 480p 首尾帧（FL2VA）片段只需 **59.5 秒**。

## NVFP4 QAD[#](#nvfp4-qad)

两个 adapter 都以 NVFP4 交付：4-bit 权重与激活，每 16 个值共享一个 8-bit 缩放，覆盖全部 50 个块中的每一个注意力与前馈线性层。三个选择让它们紧贴 BF16。

**先合并。** Flex 交付的是 fp32 LoRA adapter。我们以 fp32 把每个 adapter 合并进主干并只舍入一次，因此量化从精确的 Flex 权重出发：

```
W_merged = (W.float() + (alpha / rank) * B.float() @ A.float()).to(torch.bfloat16)
```

**为视频与音频分别校准。** 静态激活缩放在 Flex 自己的六步轨迹上设定。缩放到最大值会让 4-bit 范围浪费在罕见尖峰上，而最小化整体误差又会让数量众多的视频 token 淹没音频。因此每一层保留在两者之间取得最佳平衡的截断值，实测优于这两种替代方案。

**在部署时的数值下蒸馏。** 4-bit 学生沿着教师的六步路径对着冻结的 BF16 模型训练，从第一步起就启用 4-bit 数学。它同时对齐最终预测与每个块的输出，并有四分之一的时间从自身状态出发，学习纠正自身漂移。

| 与 BF16 Flex 的距离（越低越好） | 仅量化 | QAD 之后 |
| --- | --- | --- |
| Ref2VA | 0.326 | **0.270**（−17%） |
| FL2VA | 0.272 | **0.234**（−14%） |

**更低的损失并不总是更好的模型。** 每次评估还会采样完整片段，并按随机种子噪声设定的界限检查首帧与尾帧保真度、音频与运动。有一次运行分数持续改善，但尾帧在漂移；守卫机制把它拦下，降低学习率后解决了问题。

## FP4 注意力[#](#fp4-attention)

长片段受注意力限制，因此第二个变体还量化 query 与 key，交给 FlashAttention-4 的 NVFP4 kernel。如果做得粗糙，这会损失 QAD 得分的 13–17%。三个选择把大部分找回来：

* **平滑 K。** 量化前减去每个 head 的均值 key。这是精确的：`q·(k_j − k̄) = q·k_j − q·k̄`，而 softmax 对每个 key 共享的平移不敏感。
* **旋转 Q 与 K。** 对两者施加同一个正交 Hadamard 矩阵。这同样精确，因为 `(qH)·(kH) = q·k`，而且它把离群通道均匀分散到 16 值的缩放块上。
* **两个块保持 BF16。** 第 45 与第 49 块承载了剩余误差的大部分，因此它们的注意力保持 BF16。

共享 key 偏置
离群通道强度

Smooth-K减去均值 key
Hadamard旋转 Q 与 K

一个 key 的 NVFP4 块：16 个值，一个共享缩放

一个 query 对 12 个 key 的注意力权重

BF16 Q/K 在 NVFP4 下精确

FP4 注意力误差，100 个随机 head 的均值

量化前的 softmax(QKᵀ)，变换后与原版对比

玩具 head：64 个通道（四个 16 值块）、32 个 key、高斯数值，各 key 共享一个逐通道偏置，其中两个通道被放大。量化遵循 FlashAttention-4 的 NVFP4 路径：E2M1 数值，每 16 个通道一个 E4M3 缩放，全局缩放为单位值；P 与 V 保持 BF16。所有计算都在你的浏览器里完成。

| 逐层 FP4 注意力误差，真实 Flex 激活 | FL2VA | Ref2VA |
| --- | --- | --- |
| 朴素 FP4 | 0.115 | 0.113 |
| + 平滑 K + Hadamard | 0.095 | 0.095 |
| + 第 45、49 块用 BF16 | **0.083** | **0.080** |

随后蒸馏又弥合了剩余差距的大部分：FL2VA 落在 0.237（BF16 注意力为 0.234），Ref2VA 为 0.276（BF16 注意力为 0.270）。一个融合 kernel 在量化 Q 与 K 的同时应用两种变换，因此每次注意力调用的额外开销低于 1 毫秒：

| 单台 GB200，端到端 | BF16 注意力 | FP4 注意力 |
| --- | --- | --- |
| 480p, 5 秒 | 5.79 秒 | 5.74 秒 |
| 768p, 15 秒 | 101.8 秒 | **85.3 秒（−16%）** |

* ✓ **逐比特一致的导出：** 发布的 4-bit 权重与训练时量化的结果逐字节相同。
* ✓ **训练即所发布：** 训练时的 FP4 注意力与 FlashAttention-4 kernel 的差异在其量化误差的 1% 以内。
* ✓ **精确变换：** 量化前的 softmax(QKᵀ) 保持不变（可在图中实时验证）。

## 2K[#](#2k)

FastVideo 现在可以运行 NVIDIA 的 [Open-H3-Regenerate-2K](https://huggingface.co/Efficient-Large-Model/Open-H3-Regenerate-2K)，它能把 768p 的 H3 视频重生成到 2560x1440。任何 H3 系列草稿都可以，来自 FastH3 或 Flex 都行。以 NVFP4 QAD Flex 模型作草稿，再加上我们的 NVFP4 解码器（把 2K 解码从 23.3 秒降到 5.0 秒），文生 2K 从约 7 分钟降到 2 分钟以内：

| 文生 2K，单台 GB200 | 草稿 | 总耗时 |
| --- | --- | --- |
| 基础 H3 草稿（50 步），原版发布 | 316 秒 | 412 秒 |
| Pika H3 Flex NVFP4 QAD 草稿 + NVFP4 解码器 | 16.8 秒 | **106 秒** |

◀ ▶

768p 草稿2560×1440

拖动滑块对比。来自 NVFP4 QAD 模型的五个 768p 草稿，各自在单台 GB200 上用 Open-H3-Regenerate-2K 与 NVFP4 VAE 解码器重生成到 2560×1440。图上时间为每个片段的端到端耗时。

## 上手试用[#](#try-it)

运行 Flex 最简便的方式是 [FastVideo cookbook](https://haoailab.com/FastVideo/cookbook/minimax-h3/models/pika-h3-flex-t2va/)：选一个任务、分辨率、时长与权重（BF16、NVFP4 QAD，或带 FP4 注意力的 NVFP4 QAD），复制一条可直接运行的命令。也可以直接运行：

```
FASTVIDEO_ATTENTION_BACKEND=FLASH_ATTN FASTVIDEO_FA4=1 \
python examples/inference/basic/basic_pika_h3_flex.py --weights nvfp4-qad \
  --task t2va --prompt "..." --resolution 768p --duration 5
```

| 权重 | Hugging Face |
| --- | --- |
| BF16（Pika 发布） | [Pika-Labs/Pika-H3-Flex](https://huggingface.co/Pika-Labs/Pika-H3-Flex) |
| NVFP4 QAD，BF16 注意力 | [FastVideo/Pika-H3-Flex-NVFP4-QAD](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD) |
| NVFP4 QAD，FP4 注意力 | [FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD) |

NVFP4 模型需要 Blackwell GPU。完整训练配方——从 adapter 合并、校准，到 QAD 与导出——见[训练指南](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/training/pika_h3_flex_qad.md)。

## 致谢[#](#acknowledgements)

Pika H3 Flex 由 [Pika](https://pika.art/) 构建。感谢 Pika 团队开源 Flex、其 adapter 与推理代码。FastH3 与 Flex 都构建于 [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3)，感谢 MiniMax 团队发布其权重与代码。

感谢 NVIDIA [Efficient-Large-Model](https://huggingface.co/Efficient-Large-Model) 团队发布 Open-H3-Regenerate-2K，感谢 NVIDIA Enterprise Products 团队（Pengcheng Li 与 Cliff Woolley）提供 FastH3 所用的 Video Sparse Attention kernel。感谢 FlashAttention、FlashInfer 与 NVIDIA Model Optimizer 团队提供本工作所依赖的注意力与 FP4 kernel 及校准工具，感谢 [NVIDIA FastGen](https://github.com/NVlabs/FastGen) 团队（Julius Berner、Chao Liu 与 Arash Vahdat）提供 DMD2 框架与 H3 参考生成工作。

感谢上游的 serving、kernel 与开源社区——正是它们的实现让这些实验成为可能；也感谢 [vLLM 项目](https://vllm.ai/)、[NVIDIA](https://www.nvidia.com/en-us/) 与 [MBZUAI](https://mbzuai.ac.ae/) 对 FastVideo 的支持。

## FastVideo 团队[#](#fastvideo-team)

**贡献者：** [Aryan Kumar](https://github.com/aryan5v)

  
**技术负责人：** [Will Lin](https://github.com/SolitaryThinker)

  
**指导：** [Hao Zhang](https://github.com/zhisbug)

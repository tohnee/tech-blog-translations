---
title: "SGL-Diffusion 中 AR+DiT 的全栈性能优化"
title_en: "Full-Stack Performance Optimization of AR+DiT in SGL-Diffusion"
author: "Ascend Team"
date: "August 05, 2026"
source: https://lmsys.org/blog/2026-08-05-glmImage-optimization/
translated: 2026-09-12
previewImg: /images/blog/2026-08-05-glmImage-optimization/05-fanout.png
type: blog
---

# SGL-Diffusion 中 AR+DiT 的全栈性能优化

> 原文：[Full-Stack Performance Optimization of AR+DiT in SGL-Diffusion](https://lmsys.org/blog/2026-08-05-glmImage-optimization/) · LMSYS Blog · Ascend Team

## TL;DR

- 用 SRT 替换 HF 后端以加速 AR 建模并化解并行策略冲突：AR 使用专用 TP，DiT 使用 SP
- 通过动态批处理提升硬件利用率，并支持对已完成图像的提前返回
- 实现每设备一个去噪器的并行 DiT 执行，并通过缓冲 AR 结果实现 AR 与 DiT 流程的重叠

<div align="center">
  <img src="/images/blog/2026-08-05-glmImage-optimization/02-performance_result.png" alt="性能对比结果" />
  <br>
  <em>图 1：性能对比。</em>
</div>

## 1. 背景

自回归–扩散混合（AR+DiT）生成是一种统一框架：用 AR 建模处理全局上下文，用 DiT 方法精细化局部细节。它利用 AR transformer 捕捉长程依赖，同时由 DiT 模型迭代地精炼输出，从而同时改善质量与效率。GLM-Image 正是这一趋势的代表：一个 9B 的视觉语言模型先根据文本提示自回归地生成语义先验 token，随后一个 7B 的 DiT 再以 30–50 步将这些 token 去噪为高分辨率图像。这种"先规划、后绘制"（plan-then-paint）的设计，在知识密集型和文本密集型的视觉任务上——例如海报、信息图和精确排版——取得了 SOTA 成绩，而这些恰恰是端到端扩散模型常常表现吃力的场景。

然而，要在 SGLang 中高效服务这类混合流水线，会暴露出一个根本性的矛盾。在原生部署中，AR 编码器、DiT 去噪器和 VAE 解码器被串联在单个单体 worker 进程内，由此产生了三个关键痛点：

1. **架构耦合。** AR 与 DiT 共享同一进程、同一权重加载生命周期和同一调度域。扩容其中一个阶段必然拖累另一个，无法独立配置资源。AR 本质上是一种 LLM 解码负载——吞吐量随 batch 大小和张量并行（TP）度扩展。相比之下，DiT 去噪是一种大张量、逐图像的计算，更适合跨卡的空间并行（SP），且在 batch=1 时效率最高。同构部署只能选择单一策略，注定有一个阶段始终处于次优状态。
2. **并发下资源利用率低。** 没有动态批处理时，并发请求只能被串行处理。端到端延迟随请求并发数几乎线性增长，大量可用算力处于闲置状态。
3. **资源分配错配。** DiT 在每设备 batch=1 时达到最佳的单请求延迟，但把所有设备捆绑进单体流水线，意味着即便吞吐量优先，DiT 也被迫运行在多卡空间并行配置下，导致硬件容量利用不足。

为解决这些问题，我们提交了三个循序渐进的 PR，使系统从单体架构演进为完全解耦的异构分布式架构：
> 注：PR #31320 尚未合并。本文采用的 commit SHA 为 [4e520bd](https://github.com/sgl-project/sglang/pull/31320/changes/4e520bdeb14c72e3e80ac97a2d0b8169bb9268f1)

<div align="center">
  <img src="/images/blog/2026-08-05-glmImage-optimization/03-whole-pipeline.png" alt="整体流水线" />
  <br>
  <em>图 2：本次优化的整体流水线。</em>
</div>

## 2. 将 AR 后端 SRT 化（PR #25381）

为了降低单张图像的生成延迟，经过分析我们决定用 SRT 替换 HF 后端，最终形成 PR #25381。它将 AR 阶段从扩散 worker 进程中解耦出来，变成一个独立的 SRT 服务，AR 与 DiT 由此各自加载权重、拥有解耦的调度生命周期，并可独立扩展。同时，AR 服务器现在可以自行配置 TP，不再受 DiT 的 SP 策略约束。

<div align="center">
  <img src="/images/blog/2026-08-05-glmImage-optimization/04-glm_image_ar.png" alt="GLM-Image AR" />
  <br>
  <em>图 3：原始方案与目标方案的对比。</em>
</div>

AR 视觉语言编码器作为一个标准的 SGLang SRT 服务启动，由 Diffusion 流水线通过新增的 `--srt-encoder-url` 选项远程调用。AR 服务器复用 SGLang 现有的多模态 `sglang serve` 能力（`srt/models/glm_image_vl.py` + `srt/multimodal/processors/glm_image.py`）；Diffusion 侧只需在 `GlmImageAR` 阶段添加一个 HTTP `/generate` 分支，而 `VisionLanguageEncoderLoader` 在设置了 `srt-encoder-url` 时只执行一次 `/health` 健康检查并返回 URL，不再调用 `from_pretrained` 加载权重。这种"独立服务器 + HTTP"的方案，把"将 VLM 重写为 SRT"这一庞大任务变成了"复用现有基础设施 + 一次 HTTP 调用"，大幅降低了耦合，并将对扩散流水线的侵入式改动降到最低。

**性能收益**（复现步骤请参见 [PR #25381 描述](https://github.com/sgl-project/sglang/pull/25381)）：

| 配置                                        | NPU 数 | 端到端延迟（s）   | AR 阶段（s）      | 去噪（s）     | 解码（s）    |
| ------------------------------------------- | ---- | ----------------- | ----------------- | ------------- | ------------ |
| 单体基线（HF AR 后端）                       | 1    | 154.6             | 122.8             | 31.6          | 0.046        |
| **解耦 SRT AR（DiT 不变）**                  | 1    | **78.3 (−49.4%)** | **46.6 (−62.1%)** | 31.6          | 0.035        |
| **4-NPU 异构（AR TP=4，DiT SP=4）**          | 4    | **35.2 (−77.2%)** | **26.1 (−78.8%)** | 9.0           | 0.009        |

> **资源对齐对比：** `Decoupled SRT AR (DiT unchanged)` 行展示的是相对 `monolithic baseline (HF AR backend)` 的**纯软件**加速。  
> **叠加扩展：** `4-NPU heterogeneous (TP=4 AR, SP=4 DiT)` 行展示的是相对同一 `1-NPU 单体基线`的**软件与硬件扩展叠加**结果（软件解耦 + 4× NPU 并行）。  
> 在 PR #25381 之前，由于 AR 与 DiT 被限制为共享同一并行策略，因此数据仅适用于 4-NPU 异构配置。

AR 阶段的提速最为显著：单卡 122.8 s → 26.1 s，在 4 卡上降低 78.8%。即便在 TP=1 时，SRT 的图执行、连续批处理和内存复用也带来了相对朴素 transformers `generate` 的 −62.1% 收益。值得注意的是，基线的 2-NPU 配置虽然借助 SP 将去噪时间削减了 46.7%，AR 却反而变慢了 4.1%——在旧路径下，AR 从 SP 中得不到任何收益，甚至因通信开销而出现倒退；只有 SRT 路径才能让 AR 真正用上多卡 TP。

## 3. 动态批处理适配与提前返回支持（PR #30683）

解耦之后，AR 和 DiT 仍然一次只处理一个请求，因此高并发下延迟依旧线性增长（issue #30634）。为了提升多输入场景下的吞吐量，我们随后提交了 PR #30683。它将并发请求打包进单次前向计算，消除了串行执行造成的算力闲置。

1. **动态批处理适配**：SGL-Diffusion 已包含一套通用的动态批处理基础设施（由 [PR #18764](https://github.com/sgl-project/sglang/pull/18764) 引入）；我们的工作通过实现 `supports_dynamic_batching` 和 `supports_native_grouped_requests` 接口及相应的流水线逻辑，把这一能力扩展到了 GLM-Image。经过评估，我们只对 AR 阶段应用批处理，因为 DiT 的每步延迟与 batch 大小成正比扩展，无法带来净吞吐量收益。
2. **支持提前返回**：我们添加了 `supports_sequential_dit_inference` 变量及相关函数，使得每张输出图像就绪时即可提前返回，而不必等待整个 batch 完成。

**性能收益**（复现步骤请参见 [PR #30683 描述](https://github.com/sgl-project/sglang/pull/30683)）：

| 指标                                | BS1    | BS4                       | BS8                      | BS16                |
| ----------------------------------- | ------ | ------------------------- | ------------------------ | ------------------- |
| **吞吐量（img/s）**                 | 0.0388 | 0.0896                    | 0.1171                   | 0.1368              |
| 单请求处理延迟（s）¹                | 25.9   | 28.3 → 33.3 → 39.3 → 44.7 | 30.0 → 35.3 → ... → 68.3 | 33 → 39 → ... → 117 |
| AR 阶段单请求耗时（s）              | 20.17  | 5.65                      | 3.20                     | 1.85                |
| NPU 峰值显存（MB）                  | 28 163 | 28 046                    | 28 052                   | 28 062              |

**注：**  
¹ 处理延迟从 batch 下发开始计量，到单个请求完成为止。对 BS4/BS8/BS16，数值表示整个 batch 内的延迟范围：第一个数对应最快完成的请求，最后一个数对应最慢完成的请求。额外的排队等待时间（本测试中 ≤14 ms）可以忽略。

## 4. 分离部署与 AR 到 DiT 的扇出架构（PR #31320）

将两个阶段彻底解耦，让 AR 与 DiT 各自采用最适合自己的并行与部署策略。AR 编码器偏好大 batch + TP（面向吞吐量）；DiT 去噪则在单 NPU batch=1 时于延迟和吞吐量两方面都达到最优。

| Batch 大小 | AR（s）      | 去噪单步耗时（s）      | 去噪 30 步总耗时（s）   |
| ---------- | ------------ | ---------------------- | ----------------------- |
| 1          | 20.4         | 0.407                  | 12.2                    |
| 2          | 21.3 (+4.4%) | 0.854 (+110%)          | 25.6 (+110%)            |
| 4          | 22.8 (+12%)  | 1.98 (+386%)           | 59.6 (+389%)            |
| 8          | 25.9 (+27%)  | 3.73 (+816%)           | 112.2 (+820%)           |
| 16         | 29.4 (+44%)  | 7.24 (+1679%)          | 217.3 (+1681%)          |
| 32         | 33.2 (+63%)  | 14.0 (+3339%)          | 420.6 (+3348%)          |

随后 #31320 引入了一种异构拓扑：一个按 batch 处理的 AR 服务器 + 一组各自独立的 batch=1 去噪器。这在单节点场景下实现了系统级的最优硬件利用率。

<div align="center">
  <img src="/images/blog/2026-08-05-glmImage-optimization/05-fanout.png" alt="分离部署" />
  <br>
  <em>图 4：最终部署架构图。</em>
</div>


SGL-Diffusion 提供了一套通用的分离部署框架；PR #31320 将该框架适配到 GLM-Image 的两阶段拓扑上，实现了 DiT 并行执行以及 AR 生成与去噪之间的流水线重叠。一个关键设计选择是：ZMQ 上只传输请求元数据和 CPU 侧的先验 token ID——不跨节点发送大张量、latent、嵌入或 GPU 缓冲区——以便将通信开销保持在低位。

**性能收益**（复现步骤请参见 [PR #31320 描述](https://github.com/sgl-project/sglang/pull/31320)）：

| 配置                                                 | NPU 数 | 吞吐量（image/s）    | 平均端到端延迟（s）  |
| ---------------------------------------------------- | --- | -------------------- | -------------------- |
| AR(TP2) + 单体串行去噪器（BS28）                     | 16  | 0.2                  | 90                   |
| AR(TP2) + 分离式并行去噪器（14 x BS=1）              | 16  | **0.74**             | **37**               |

## 5. 致谢

- 华为昇腾团队（Huawei Ascend Team）

  我们感谢华为昇腾 NPU 团队对 GLM-Image 优化的持续贡献。特别感谢 Maksim Emelin（@[Makcum888e](https://github.com/Makcum888e)）、Artem Savkin（@[OrangeRedeng](https://github.com/OrangeRedeng)）、Egor Filimonov（@[ssshinigami](https://github.com/ssshinigami)）以及 Liang Zhen（@[ping1jing2](https://github.com/ping1jing2)）。

  同时感谢来自 CMB 的 Yuefeng Wu（@[ChefWu551](https://github.com/ChefWu551)）和 Qianqian Zheng（@[AuFlow](https://github.com/AuFlow)），他们参与了昇腾平台上的 GLM-Image 优化工作，提升了稳定性与部署效率。

- SGLang 社区

  感谢更广泛的 SGLang 社区，包括 Xiaoyu Zhang（@[BBuf](https://github.com/BBuf)）的代码评审，以及 Yuhao Yang（@[yhyang201](https://github.com/yhyang201)）和其他贡献者的最初讨论（issue #20032）与实现（PR #18809）。

最后，感谢 SGLang 的维护者和评审者的悉心指导，感谢 Zhipu AI 团队开源 GLM-Image 模型及权重，也感谢每一位为 SGL-Diffusion 做出贡献的人。

## 6. 附录

由于命令较长，完整复现步骤已列在 [issue #33526](https://github.com/sgl-project/sglang/issues/33526) 中。

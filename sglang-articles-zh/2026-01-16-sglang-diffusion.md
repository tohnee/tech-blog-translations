---
title: "SGLang-Diffusion：两个月进展回顾"
title_en: "SGLang-Diffusion: Two Months In"
author: "The SGLang-Diffusion Team"
date: "January 16, 2026"
previewImg: /images/blog/sgl-diffusion/sgl-diffusion-banner-16-9.png
source: https://lmsys.org/blog/2026-01-16-sglang-diffusion/
translated: 2026-09-12
---

# SGLang-Diffusion：两个月进展回顾

> 原文：[SGLang-Diffusion: Two Months In](https://lmsys.org/blog/2026-01-16-sglang-diffusion/) · LMSYS Blog · The SGLang-Diffusion Team

自 2025 年 11 月初发布以来，**SGLang-Diffusion** 已在社区内获得了广泛关注与大规模采用。我们对开源开发者们大量的反馈与日益增长的贡献深表感谢。

过去两个月里，我们对 SGLang-Diffusion 进行了细致的优化，如今（docker 镜像 tag：`lmsysorg/sglang:dev-pr-17247`）其速度最高已达首发版本的 2.5 倍。

以下是我们进展的概要：

## 总览

**新模型支持**：

- Day-0 支持 Flux.2、Qwen-Image-Edit-2511、Qwen-Image-2512、Z-Image-Turbo、Qwen-Image-Layered、TurboWan、GLM-Image 等模型。
- 通过 diffusers 后端运行 SGLang-Diffusion：兼容 diffusers 中的所有模型；更多改进已在计划中（见 [Issue #16642](https://github.com/sgl-project/sglang/issues/16642)）。

**LoRA 支持**：

- 对已支持的模型，我们支持几乎所有 LoRA 格式。本节列出部分经过明确测试与验证的示例 LoRA。
  | 基座模型 | 支持的 LoRA |
  |-------------------|------------------|
  | **Wan2.2**        | `lightx2v/Wan2.2-Distill-Loras`<br> `Cseti/wan2.2-14B-Arcane_Jinx-lora-v1` |
  | **Wan2.1**        | `lightx2v/Wan2.1-Distill-Loras` |
  | **Z-Image-Turbo** | `tarn59/pixel_art_style_lora_z_image_turbo`<br> `wcde/Z-Image-Turbo-DeJPEG-Lora` |
  | **Qwen-Image**    | `lightx2v/Qwen-Image-Lightning`<br> `flymy-ai/qwen-image-realism-lora`<br> `prithivMLmods/Qwen-Image-HeadshotX`<br> `starsfriday/Qwen-Image-EVA-LoRA` |
  | **Qwen-Image-Edit** | `ostris/qwen_image_edit_inpainting`<br> `lightx2v/Qwen-Image-Edit-2511-Lightning` |
  | **Flux**          | `dvyio/flux-lora-simple-illustration`<br> `XLabs-AI/flux-furry-lora`<br> `XLabs-AI/flux-RealismLora` |
- 功能完整的 HTTP API：
  | 功能 | API 端点 | 关键参数 |
  |---------------------------------|-----------------------------|--------------------------------------------------|
  | 设置或激活（多个）LoRA | `/v1/set_lora`              | `lora_nickname`, `lora_path`, `strength`, `target` |
  | 合并权重 | `/v1/merge_lora_weights`    | `strength`, `target`                             |
  | 取消合并权重 | `/v1/unmerge_lora_weights`  | - |
  | 列出适配器 | `/v1/list_loras`            | - |

**并行**：对大多数模型支持 SP 与 TP，并支持混合并行（Ulysses 并行、Ring 并行与张量并行的组合）。

**注意力后端**：SageAttention2、SageAttention3 与 SLA，更多后端在计划中。

**硬件支持**：AMD、4090、5090、MUSA

**SGLang-Diffusion x ComfyUI 集成**：我们实现了一个灵活的 ComfyUI 自定义节点，将 SGLang-Diffusion 的高性能推理引擎接入其中。参见[使用指南](https://github.com/sgl-project/sglang/blob/76f69b77530c734ff9b92b5d036316ba097ba943/python/sglang/multimodal_gen/apps/ComfyUI_SGLDiffusion/README.md)。

ComfyUI 虽然通过自定义节点提供了极高的灵活性，但往往缺乏多 GPU 支持与最优性能。

我们的方案是用 SGLang 的优化实现替换 ComfyUI 的去噪模型前向计算，在保留 ComfyUI 灵活性的同时，发挥 SGLang 更强的推理能力。用户只需把 ComfyUI 的加载器换成我们的 SGL-Diffusion UNET Loader，即可在不修改现有工作流的情况下获得性能提升。

<img src="/images/blog/sgl-diffusion-26-01/comfyui.png" style="display:block; width: 220%; margin:15px auto 0 auto"></img>
<p style="color:gray; text-align: center;">ComfyUI 中的 SGLang-Diffusion 插件</p>

## 性能基准测试

以下是一些性能基准测试结果：

- 我们在多个主流模型上对 SGLang-Diffusion（docker 镜像 tag：`lmsysorg/sglang:dev-pr-17247`）进行了基准测试，与旧版本（2025 年 11 月）及其他框架进行对比。SGLang-Diffusion 在 NVIDIA GPU 上达到了当前最快速度，领先所有其他方案最高达 5 倍。

[//]: # (<iframe width="984" height="923" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQRK_j_q8NXZKEqtrTBagxFxvvaxYXXB56HTqqYlD_aAv1v74WKle2HIc7HPK3P0ZVrYlZrjshKYnaV/pubchart?oid=1022178651&amp;format=interactive"></iframe>)
<iframe style="display:block; margin: auto;" width="969" height="923" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQRK_j_q8NXZKEqtrTBagxFxvvaxYXXB56HTqqYlD_aAv1v74WKle2HIc7HPK3P0ZVrYlZrjshKYnaV/pubchart?oid=1681696401&amp;format=interactive"></iframe>

- 我们将 SGLang-Diffusion 在不同环境下的性能与速度最快的厂商之一进行了对比。
<iframe style="display:block; margin: auto;" width="969" height="780" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQRK_j_q8NXZKEqtrTBagxFxvvaxYXXB56HTqqYlD_aAv1v74WKle2HIc7HPK3P0ZVrYlZrjshKYnaV/pubchart?oid=174425525&amp;format=interactive"></iframe>


- 我们还在 AMD GPU 上评估了 SGLang-Diffusion：
<iframe style="display:block; margin: auto;" width="852" height="321" seamless frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQCc9ulnNOE8mpM2RjIgZLJlLKxK_KUyws3WlTB1mVz2Ywx790G0IVbrI7-gjY_O5D8G5Grcjb1dBkR/pubchart?oid=319708956&amp;format=interactive"></iframe>

## 关键改进

要成为一个健壮的工业级框架，**速度、稳定性与代码质量**是我们的首要优先事项。我们重构了关键组件，以消除瓶颈并最大化硬件效率。

以下是近期技术改进的亮点：

### 1. 逐层卸载（Layerwise Offload）

从早期性能剖析中，我们发现模型加载/卸载是主要瓶颈：计算流必须等待所有权重就位后才能开始，而大多数 GPU 的显存（VRAM）并不足以在整个推理过程中把所有组件都留在显存里。

为此，我们引入了：

1. `LayerwiseOffloadManager`：一个管理器类，提供在计算当前层时**预取**（prefetch）下一层权重的钩子（hook），以及在计算完成后**释放**权重的钩子。
2. `OffloadableDiTMixin`：一个 mixin 类，为扩散 Transformer（DiT）注册 `LayerwiseOffloadManager` 的预取与释放钩子。

由此带来以下好处：

- **计算-加载重叠**：将计算与权重加载重叠，消除拷贝流（copy stream）上的停顿，显著提升推理速度——对 Wan2.2 这类多 DiT 架构尤为明显
- **显存优化**：峰值显存占用降低，可以生成更长的视频序列和更高分辨率的内容

<img src="/images/blog/sgl-diffusion-26-01/layerwise offload vs serial.png" style="display:block; margin: auto; width: 100%;"></img>

<p style="color:gray; text-align: center;">标准加载与逐层卸载的对比</p>


**逐层卸载** 现已默认对视频模型启用。

相关 PR 见（[#15511](https://github.com/sgl-project/sglang/pull/15511)、[#16150](https://github.com/sgl-project/sglang/pull/16150)）。

### 2. 算子（Kernel）改进

- **同步上游 FlashAttention**：我们将算子与 Dao-AILab 的最新上游版本同步，消除性能滞后。见 [#16382](https://github.com/sgl-project/sglang/pull/16382)。
- **优化 QKV 处理**：我们分析了 Packed QKV 与下游算子（如 `qk_norm`、FlashInfer RoPE）之间的性能权衡。为实现最优的预处理性能，我们在实现 QKV 拆包时没有引入额外的连续内存（contiguous）操作。
- **JIT QK Norm 算子**：将 Q/K RMSNorm 融合为单个原地（inplace）算子，减少注意力计算前的算子启动次数与内存流量。
- **FlashInfer RoPE**：在可用时用 FlashInfer 对 Q/K 原地应用 RoPE（否则回退到原有实现），降低 RoPE 开销与中间张量的物化成本。
- **权重融合（算子融合）**：融合投影 + 激活的常见组合（如 gate/up 合并 + SiLU&Mul），减少 DiT 块中的 GEMM 次数与逐元素算子的启动次数。
- **时间步实现**：使用专用 CUDA 内核计算时间步的正弦/余弦嵌入（sin/cos），降低扩散调度中每一步的开销。见 [#12995](https://github.com/sgl-project/sglang/pull/12995)。


### 3. 集成 Cache-DiT

我们将最受欢迎的 DiT 缓存框架 [Cache-DiT🤗](https://github.com/vipshop/cache-dit) 无缝集成到了 SGLang-Diffusion 中，与 `torch.compile`、Ulysses 并行、Ring 并行和张量并行完全兼容，也支持这三种并行方式的任意混合组合。
实现细节见 [#14234](https://github.com/sgl-project/sglang/pull/14234)、[#15163](https://github.com/sgl-project/sglang/pull/15163) 与 [#16532](https://github.com/sgl-project/sglang/pull/16532)。

只需设置几个环境变量，生成速度最高可提升 169%。

以下是在 SGLang-Diffusion 中启用 Cache-DiT 的示例：

```bash
SGLANG_CACHE_DIT_ENABLED=true \
SGLANG_CACHE_DIT_SCM_PRESET=fast \
sglang generate --model-path=Qwen/Qwen-Image --prompt="Cinematic establishing shot of a city at dusk"
  --save-output
```

此外，我们现在还可以把 Cache-DiT 的优化集成并打磨到新支持的 diffusers 后端中（见 [Issue #16642](https://github.com/sgl-project/sglang/issues/16642)）。

### 4. 其他更新

- **内存监控**：离线生成与在线推理服务两种工作流均可查看峰值用量统计。
- [**性能剖析套件**](https://docs.sglang.io/diffusion/performance/profiling.html)：覆盖全流程，并提供 PyTorch Profiler 与 Nsight Systems 的分步文档。
- [**Diffusion Cookbook**](https://cookbook.sglang.io/docs/diffusion/)：为 SGLang-Diffusion 精心整理的实践配方、最佳实践与基准测试指南。

## 路线图（2026 Q1）

- 稀疏注意力后端
- 量化（nunchaku、nvfp4 等）
- 消费级 GPU 上的优化
- 与 [sglang-omni](https://github.com/sgl-project/sglang/issues/16546) 协同设计

更多细节请参见 [**26Q1 路线图**](https://github.com/sgl-project/sglang/issues/18286)。

## 致谢

**SGLang-Diffusion 团队**：

Aichen Feng, Adarsh Shirawalmath, Alison Shao, Changyi Yang, Chunan Zeng, DefTruth, Fan Lin, Fan Luo, Fenglin Yu, Gaoji Liu, Heyang Huang, Hongli Mi,
Huanhuan Chen, Ji Huang, Jiajun Li, Ji Li, Jinliang Li, Junlin Lv, Jianying Zhu, Jiaqi Zhu, Mingfa Feng, Ran Mei, Ruiguo Yang, Shenggui Li,
Shuyi Fan, Shuxi Guo, Song Lin, Wang Xingyu, Weitao Dai, Wenhao Zhang, Xi Chen, Xiao Jin, Xiaoyu Zhang (BBuf), Yihan Chen, Yikai Zhu, Yin Fan, Yuhao
Yang, Yixuan Zhang, Yuan Luo, Yueming Yuan, Yuhang Qi, Yuzhen Zhou, Zhiyi Liu, Zhuorui Liu, Ziyi Xu, Mick

特别感谢 NVIDIA 与 Voltage Park 提供的算力支持。

特别感谢 AMD 提供的算力支持与开发协助。

## 了解更多

- **Slack 频道**：[#diffusion](https://sgl-fru7574.slack.com/archives/C09P0HTKE6A)（通过 slack.sglang.io 加入）
- [**SGLang-Diffusion Cookbook**](https://cookbook.sglang.io/docs/diffusion)
- [**SGLang-Diffusion 文档**](https://docs.sglang.io/diffusion/index.html)
- [**26Q1 路线图**](https://github.com/sgl-project/sglang/issues/18286)

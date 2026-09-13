---
title: "vLLM-Omni 扩散模型缓存加速"
title_en: "vLLM-Omni Diffusion Cache Acceleration"
source: https://vllm.ai/blog/2025-12-19-vllm-omni-diffusion-cache-acceleration
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM-Omni 扩散模型缓存加速

> 原文：[vLLM-Omni Diffusion Cache Acceleration](https://vllm.ai/blog/2025-12-19-vllm-omni-diffusion-cache-acceleration) · vLLM 博客

vLLM-Omni 团队

[#多模态](https://vllm.ai/blog/tags/multimodal)[#性能](https://vllm.ai/blog/tags/performance)[#生态](https://vllm.ai/blog/tags/ecosystem)

# 为你的扩散推理提速

我们非常高兴地宣布 **vLLM-Omni** 迎来一次重大性能更新。

vLLM-Omni 现已支持多种缓存加速方法，以极小的质量损失加速扩散模型推理，例如 **Cache-DiT** 与 **TeaCache**。这些缓存方法会智能地缓存中间计算结果，避免在扩散时间步之间做重复工作。

通过本次更新，用户只需极少配置，即可在图像生成任务中获得 **1.5x 至 2x 以上**的加速，且质量损失可忽略不计。

## 瓶颈：扩散中的冗余

扩散模型以高昂的计算成本而闻名。生成单张图像需要数十个推理步骤。然而，相邻步骤处理的特征往往非常相似。

vLLM-Omni 现在正是利用了这种时间冗余。通过智能地缓存和复用中间计算结果，我们可以在后续步骤中跳过昂贵的计算，而无需重新训练模型。

## 两个强大的加速后端

vLLM-Omni 现支持两种不同的缓存后端，以满足你的具体需求：

### 1. Cache-DiT：高级控制与极致性能

[Cache-DiT](https://github.com/vipshop/cache-dit) 是一个功能全面的库级加速方案。它提供一整套精巧技术以最大化效率：

- **DBCache（双块缓存，Dual Block Cache）：** 基于残差差异智能缓存 Transformer 块输出。
- **TaylorSeer：** 利用基于泰勒展开的预测来估计特征，进一步降低计算负载。
- **SCM（步计算掩码，Step Computation Masking）：** 应用自适应掩码，选择性地跳过计算步骤。

### 2. TeaCache：简单而自适应

TeaCache 在 vLLM-Omni 内原生实现，提供基于钩子（hook）的自适应缓存机制。它监控输入之间的差异，并动态决定何时复用上一个时间步的 transformer 计算结果。

## 性能基准

我们在 NVIDIA H200 GPU 上使用 **Qwen-Image**（1024x1024 生成）对这些方法进行了基准测试。结果令人印象深刻：

| 模型 | 后端 | 配置 | 耗时 | 加速比 |
| --- | --- | --- | --- | --- |
| **Qwen-Image** | Baseline | 无 | 20.0s | 1.0x |
| **Qwen-Image** | **TeaCache** | `rel_l1_thresh=0.2` | 10.47s | **1.91x** ⚡ |
| **Qwen-Image** | **Cache-DiT** | DBCache + TaylorSeer | 10.8s | **1.85x** ⚡ |

![No Cache](https://vllm.ai/blog-assets/figures/2025-12-19-vllm-omni-diffusion-cache-acceleration/cat.png)

无缓存

无缓存

![TeaCache](https://vllm.ai/blog-assets/figures/2025-12-19-vllm-omni-diffusion-cache-acceleration/cat_tea_cache.png)

TeaCache

TeaCache

![Cache-DiT](https://vllm.ai/blog-assets/figures/2025-12-19-vllm-omni-diffusion-cache-acceleration/cat_cache_dit.png)

Cache-DiT

Cache-DiT

### 「编辑」模型

对于图像编辑任务，Cache-DiT 表现得更加耀眼。在 **Qwen-Image-Edit** 上，Cache-DiT 实现了高达 **2.38x** 的加速，将生成时间从 51.5s 降至仅 21.6s。

| 模型 | 后端 | 配置 | 耗时 | 加速比 |
| --- | --- | --- | --- | --- |
| **Qwen-Image-Edit** | Baseline | 无 | 51.5s | 1.0x |
| **Qwen-Image-Edit** | **TeaCache** | `rel_l1_thresh=0.2` | 35.0s | **1.47x** ⚡ |
| **Qwen-Image-Edit** | **Cache-DiT** | DBCache + TaylorSeer | 21.6s | **2.38x** ⚡ |

![No Cache](https://vllm.ai/blog-assets/figures/2025-12-19-vllm-omni-diffusion-cache-acceleration/qwen_bear_base.png)

无缓存

无缓存

![TeaCache](https://vllm.ai/blog-assets/figures/2025-12-19-vllm-omni-diffusion-cache-acceleration/qwen_bear_tea_cache.png)

TeaCache

TeaCache

![Cache-DiT](https://vllm.ai/blog-assets/figures/2025-12-19-vllm-omni-diffusion-cache-acceleration/qwen_bear_cache_dit.png)

Cache-DiT

Cache-DiT

这些缓存优化技术在昇腾 NPU 等异构平台上同样展现出亮眼的结果。例如，在昇腾 NPU 上，Qwen-Image-Edit 推理借助 Cache-DiT 从 142.38s 加速至 64.07s，获得了超过 2.2x 的加速。

## 支持的模型

| 模型 | TeaCache | Cache-DiT |
| --- | --- | --- |
| **Qwen-Image** | ✅ | ✅ |
| **Z-Image** | ❌ | ✅ |
| **Qwen-Image-Edit** | ✅ | ✅ |

## 快速开始

在 vLLM-Omni 中开启加速非常顺畅。只需在初始化 `Omni` 类时定义你的 `cache_backend`。

### 使用 TeaCache 加速

```
from vllm_omni import Omni

omni = Omni(
    model="Qwen/Qwen-Image",
    cache_backend="tea_cache",
    cache_config={"rel_l1_thresh": 0.2}
)

outputs = omni.generate(prompt="A cat sitting on a windowsill", num_inference_steps=50)
```

### 使用 Cache-DiT 加速

```
from vllm_omni import Omni

omni = Omni(
    model="Qwen/Qwen-Image",
    cache_backend="cache_dit",
    cache_config={
        "Fn_compute_blocks": 1,
        "Bn_compute_blocks": 0,
        "max_warmup_steps": 8,
        "enable_taylorseer": True, # Enable Taylor expansion forecasting
        "taylorseer_order": 1,
    }
)

outputs = omni.generate(prompt="A cat sitting on a windowsill", num_inference_steps=50)
```

## 了解更多

准备好为你的扩散流水线提速了吗？请查阅我们的详细文档以获取高级配置：

- [Cache-DiT 加速指南](https://docs.vllm.ai/projects/vllm-omni/en/latest/user_guide/acceleration/cache_dit_acceleration/)
- [TeaCache 指南](https://docs.vllm.ai/projects/vllm-omni/en/latest/user_guide/acceleration/teacache/)

除缓存之外，我们还在并行化、内核融合和量化方面积极开发优化。敬请期待更多强大功能！

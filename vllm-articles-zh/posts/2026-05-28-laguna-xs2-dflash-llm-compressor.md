---
title: "用 vLLM、Speculators 与 LLM Compressor 加速 Laguna XS.2 推理"
title_en: "Accelerating Laguna XS.2 Inference with vLLM, Speculators, and LLM Compressor"
source: https://vllm.ai/blog/2026-05-28-laguna-xs2-dflash-llm-compressor
crawled: 2026-09-12
translated: 2026-09-13
---

# 用 vLLM、Speculators 与 LLM Compressor 加速 Laguna XS.2 推理

> 原文：[Accelerating Laguna XS.2 Inference with vLLM, Speculators, and LLM Compressor](https://vllm.ai/blog/2026-05-28-laguna-xs2-dflash-llm-compressor) · vLLM 博客

作者：Megan Flynn、Dipika Sikka、Alexandre Marques

[#量化](https://vllm.ai/blog/tags/quantization)[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)[#speculators](https://vllm.ai/blog/tags/speculators)[#llm-compressor](https://vllm.ai/blog/tags/llm-compressor)[#dflash](https://vllm.ai/blog/tags/dflash)

随着各组织日益采用 AI 驱动的开发工具，对兼具精度与运行效率的高性能智能体模型的需求变得至关重要。Laguna XS.2 是 Poolside Laguna 家族的首个开放权重模型：一个面向智能体编程和长程软件任务的 33B-A3B MoE 模型。作为 Laguna XS.2 发布的一部分，Red Hat AI 与 Poolside 在服务与推理优化上展开合作，包括一等公民级别的 vLLM 集成、一个 DFlash 投机模型（speculator）检查点，以及用 LLM Compressor 构建的量化检查点。这次发布是面向生产就绪 AI 部署的重要里程碑，Laguna XS.2 的量化与投机模型检查点都针对真实智能体应用中的速度与效率做了优化。

## 通过 vLLM 集成实现无缝推理

在与 Poolside 的合作中，Laguna XS.2 在发布时即作为一等公民直接集成进 vLLM，可通过标准 vLLM API 立即部署。

## 用 DFlash 投机解码优化性能

为进一步加速推理，Red Hat 团队使用 [Speculators](https://github.com/vllm-project/speculators) 库为 Laguna XS.2 训练了一个 [DFlash 投机模型](https://huggingface.co/poolside/Laguna-XS.2-speculator.dflash)。

[DFlash](https://arxiv.org/abs/2602.06036) 算法是当前投机解码的最先进水平。该模型使用一个 5 层、0.6B 的小型草稿模型，加上来自目标 Laguna XS.2 模型的隐藏状态输入，通过单次前向传播预测一个 token 块。这些 token 随后由 Laguna XS.2 模型单次前向验证。这一验证步骤保证了与单独使用大模型完全相同的生成质量；如果这些 token 被接受，其单位 token 的产出速度将远快于用 Laguna XS.2 自回归地逐个生成 token。关键在于训练 DFlash 去准确预测 Laguna XS.2 可能接受的 token。

该模型在来自 [Ultrachat 200k SFT](https://huggingface.co/datasets/HuggingFaceH4/ultrachat_200k) 和 [Magpie-Align](https://huggingface.co/datasets/Magpie-Align/Magpie-Llama-3.1-Pro-300K-Filtered) 的 50 万样本上训练。提示词从各数据集中采样，响应由 Laguna XS.2 在开启思考（thinking）的情况下重新生成。随后模型使用余弦调度器训练 6 个 epoch，最大学习率为 6e-4，序列长度为 8192，并为每个序列随机采样 3072 个块位置。

最终得到一个 5 层起草器，可通过单次前向传播预测出 8 个 token。经 Laguna XS.2 验证后，token 产出速度快 2-3 倍，且[可证明](https://arxiv.org/abs/2211.17192)不损失生成质量。

![](https://vllm.ai/blog-assets/figures/2026-05-28-laguna-xs2-dflash-llm-compressor/laguna_dflash.png)

DFlash 算法代表着下一代投机解码，超越了 Eagle-3 范式，提供更快的并行起草，显著降低逐 token 延迟（inter-token-latency）。想亲自试用该投机模型，请查看 [vLLM 配方](https://recipes.vllm.ai/poolside/Laguna-XS.2)。

## 用 LLM Compressor 构建量化检查点

Poolside 团队还使用 [LLM Compressor](https://github.com/vllm-project/llm-compressor) 库发布了量化的 Laguna XS.2 检查点。这些检查点包括 [FP8](https://huggingface.co/poolside/Laguna-XS.2-FP8)、[NVFP4](https://huggingface.co/poolside/Laguna-XS.2-NVFP4)、[INT4/INT8](https://huggingface.co/poolside/Laguna-XS.2-INT4) 变体，采用 [compressed-tensors](https://github.com/vllm-project/compressed-tensors) 格式，以便在 vLLM 中高效部署并保持模型质量。

LLM Compressor 提供了一个灵活的框架，可将各种量化技术应用于 LLM。借助这些检查点，开发者可以选择最契合其硬件、延迟和内存需求的 Laguna XS.2 变体。

## 下一步

- 在 [Hugging Face Hub](https://huggingface.co/collections/poolside/laguna-xs2) 上探索 Laguna XS.2 模型
- 使用 [LLM Compressor](https://github.com/vllm-project/llm-compressor) 和 [Speculators](https://github.com/vllm-project/speculators) 优化你自己的模型

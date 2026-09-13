---
title: "用 vLLM 实现快速高效的 LLM 推理：与 DeepLearning.AI 合作推出新课程"
title_en: "Fast & Efficient LLM Inference with vLLM: A New Course with DeepLearning.AI"
source: https://vllm.ai/blog/2026-06-03-deeplearning-ai-vllm-course
crawled: 2026-09-12
translated: 2026-09-13
---

# 用 vLLM 实现快速高效的 LLM 推理：与 DeepLearning.AI 合作推出新课程

> 原文：[Fast & Efficient LLM Inference with vLLM: A New Course with DeepLearning.AI](https://vllm.ai/blog/2026-06-03-deeplearning-ai-vllm-course) · vLLM 博客

作者：Cedric Clyburn

[#社区](https://vllm.ai/blog/tags/community)[#生态](https://vllm.ai/blog/tags/ecosystem)[#学习](https://vllm.ai/blog/tags/learning)

![](https://vllm.ai/blog-assets/figures/2026-06-03-deeplearning-ai-course/course-banner.png)

我们很高兴地宣布：我们与 Red Hat 以及 [Andrew Ng](https://en.wikipedia.org/wiki/Andrew_Ng) 的 [DeepLearning.AI](https://www.deeplearning.ai/) 合作，推出了一门动手课程，带你走一遍 LLM 基础知识，以及使用 vLLM 及其工具生态的完整 *优化、部署、基准测试* AI 部署生命周期。课程名为 [Fast & Efficient LLM Inference with vLLM](https://www.deeplearning.ai/courses/fast-and-efficient-llm-inference-with-vllm)，现在已经上线！

> “面向众多用户高效部署开源 LLM，同时保持低延迟和合理成本，是一件有挑战的事。这门课程会教你怎么做。”—— Andrew Ng

## 课程是如何诞生的

今年早些时候，我们与 DeepLearning.AI 团队接洽，商讨打造一门聚焦 LLM 推理优化的课程。由于 vLLM 生态已经成长到不只包括服务引擎本身，还包括模型压缩工具（[LLM Compressor](https://github.com/vllm-project/llm-compressor)）和部署基准测试工具（[GuideLLM](https://github.com/vllm-project/guidellm)），我们看到了一个机会，可以展示在规模化部署模型时，这些工具如何拼合在一起。

我们与 Andrew Ng 及其团队在 Mountain View 合作，把课程材料围绕许多部署所遵循的工作流来组织：压缩模型以适配你的硬件，用 vLLM 高效地服务，然后做基准测试，了解自己在速度-成本-精度权衡上的位置。在代码示例开始之前，还有大量围绕推理与内存的基础概念，真正帮助学习者理解为什么连续批处理、PagedAttention 和前缀缓存这类优化会有帮助。

![](https://vllm.ai/blog-assets/figures/2026-06-03-deeplearning-ai-course/course-structure.png)
*课程在进入动手实验之前，先讲解硬件需求、内存层级和优化技术。*

## 我们投入了什么

大量精力投入到了**可视化**上。我们希望学习者真正理解推理背后发生了什么，以及 KV 缓存（KV Cache）与 GPU 内存层级。

我们拆解了推理时的 transformer 架构：例如 token 如何流经模型、每一层发生什么计算、瓶颈究竟在哪里。我们还把 KV 缓存可视化：它在 GPU 内存中是什么样子、如何随每个生成的 token 增长，以及为什么服务多个并发用户会带来巨大的内存压力。

![](https://vllm.ai/blog-assets/figures/2026-06-03-deeplearning-ai-course/kv-cache.png)
*课程中可视化自回归生成期间 KV 缓存的增长过程。*

对于量化，我们构建了可视化讲解：当你把模型默认发布的 FP16 权重转为 INT8 或 INT4 时会发生什么，包括收益与权衡。

![](https://vllm.ai/blog-assets/figures/2026-06-03-deeplearning-ai-course/quantization-schemes.png)
*拆解仅权重量化与权重+激活值量化，以及 GPU 内存层级。*

## 课程里有什么

课程主要分为三个阶段，每个阶段都在 JupyterLab 环境中配有一个动手实验，学习者在其中操作真实模型和一个运行中的 vLLM 服务器：

### 压缩（Compress）

你拿一个全精度的 Qwen 模型，用 [LLM Compressor](https://github.com/vllm-project/llm-compressor) 对它进行量化。你比较量化前后的模型大小，然后测量困惑度以量化精度权衡。这个实验让你对量化技术，以及在部署 LLM 时如何降低 GPU 内存需求，有很好的体感。

![](https://vllm.ai/blog-assets/figures/2026-06-03-deeplearning-ai-course/quantization-lab.png)
*在课程实验中用 LLM Compressor 量化一个 Qwen 模型。*

### 服务（Serve）

你学习如何用 [vLLM](https://github.com/vllm-project/vllm) 部署模型，并通过 OpenAI 兼容 API 与它交互。你通过 vLLM 的指标观察连续批处理等机制，看到并发请求到来时内存利用率如何变化，以及当请求共享系统提示时前缀缓存如何避免冗余计算。

![](https://vllm.ai/blog-assets/figures/2026-06-03-deeplearning-ai-course/vllm-metrics.png)
*在并发请求打到服务器时，实时观察 vLLM 的服务指标。*

### 基准测试（Benchmark）

你用 [GuideLLM](https://github.com/vllm-project/guidellm) 模拟真实的流量模式，测量负载下的延迟与吞吐量。然后你用 [lm-eval](https://github.com/EleutherAI/lm-evaluation-harness) 评估模型质量，确认压缩后的模型仍满足你的精度要求。到最后，你已经在一个真实模型上完成了完整的负载/精度分析，对这些权衡的理解也足以让你做出明智的部署决策。

![](https://vllm.ai/blog-assets/figures/2026-06-03-deeplearning-ai-course/benchmarking-lab.png)
*在课程实验中运行 GuideLLM，在模拟流量下对 vLLM 部署进行基准测试。*

## 课程详情

- **课程**：[Fast & Efficient LLM Inference with vLLM](https://www.deeplearning.ai/courses/fast-and-efficient-llm-inference-with-vllm/)
- **讲师**：[Cedric Clyburn](https://www.linkedin.com/in/cedricclyburn)，Red Hat 高级开发者布道师
- **时长**：约 1.5 小时，9 节视频课，3 个动手代码实验
- **难度**：中级（假设你熟悉 Python 和基本 LLM 概念）

课程在 DeepLearning.AI 上免费开放。如果你一直在本地或大规模运行模型，想理解表面之下发生了什么，这门课会很有用；如果你听说过 vLLM 并想动手实践，它同样适合你！你将获得部署开源模型的经验，我们希望这是一个有用的资源。

## 致谢

这门课程是团队努力的成果。来自 Red Hat 的 Saša Zelenović、Michael Goin 和 Sawyer Bowerman 为课程设计、技术内容和实验开发做出了贡献。来自 DeepLearning.AI 的 Hawraa Salami 帮助打磨了课程体系与制作。感谢 Andrew Ng 的合作，以及在 DeepLearning.AI 课程目录中为开源推理工具留出空间。希望你喜欢这门课！

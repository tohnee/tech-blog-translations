---
title: "Nemotron 3 Super 吞吐量笔记"
title_en: "Nemotron 3 Super Throughput Notes"
source: https://sebastianraschka.com/blog/2026/nemotron-3-super-throughput.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Nemotron 3 Super 吞吐量笔记

> 原文：[Nemotron 3 Super Throughput Notes](https://sebastianraschka.com/blog/2026/nemotron-3-super-throughput.html)

又一周，又一个值得关注的开放权重 LLM 发布。NVIDIA 的 [Nemotron 3 Super 120B-A12B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16) 在报告的基准测试上看起来颇具竞争力，而更有意思的是它面向吞吐量的设计。

读完[技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)和[模型配置](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/blob/main/config.json)后，我很欣赏这一设计如何应对三种不同的推理成本。Mamba-2 减少了全注意力的分量，[潜在 MoE（Latent MoE）](https://sebastianraschka.com/glossary/#latent-moe "Latent MoE")压缩了路由专家的通路，多 token 预测则为投机解码（speculative decoding）提供了内部草稿机制。

## 120B-A12B 模型里面有什么

准确数字是：总参数 1206 亿，每次前向传播激活 127 亿，若不含嵌入则为 121 亿。88 层的堆叠包含 40 层 Mamba-2、40 层潜在 [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") 和 8 层分组查询注意力。

只使用 8 层注意力，让注意力侧的缓存相对较小。每个注意力层有 2 个 [KV 头](https://sebastianraschka.com/glossary/#gqa "Grouped-Query Attention (GQA)")，头维度为 128。在 bf16 下，这相当于所有注意力层合计每 token 每条序列 8 KiB 的逻辑 KV 缓存。Mamba-2 层在生成期间使用循环状态，而不是为每个保留的 token 追加一条 KV 条目。

这种混合设计并没有去掉全注意力，而是把它限制在少量全局锚点层中，由 Mamba-2 处理序列堆叠的大部分。对于长提示词和长生成轨迹来说，这是一个合理的安排——标准的 transformer 会在每一层累积 [KV 缓存](https://sebastianraschka.com/glossary/#kv-cache "KV Cache")。

稀疏的部分则更不寻常。每个潜在 MoE 层包含 512 个路由专家，每个 token 选择 22 个。在路由专家计算之前，模型把 4096 维的隐藏状态投影到 1024 维的潜在表示。专家输出随后被组合并投影回 4096 维。一个单独的共享专家保持全宽度。

缩小 4 倍的路由维度减少了专家权重读取和 all-to-all 通信负载。NVIDIA 用这些节省在相近的推理预算下激活更多的小专家。完整的 120B 参数检查点仍然需要存储或分发，因此 12B 激活这一标签应被理解为算力估计，而不是权重内存估计。

第三个组件是多 token 预测（MTP）。Nemotron 3 Super 有两个共享权重的 MTP 层。推理期间，MTP 通路提出未来 token，主模型对其进行验证。在多个偏移之间复用一个预测头，也支持更长的递归草稿，而无需为每个偏移添加独立的头。当推理引擎支持 MTP 通路且足够多的草稿 token 被接受时，这可以降低解码延迟。

## 如何看待吞吐量结果

NVIDIA 报告，在 8K token 输入接 64K 输出 token 的设置下，推理吞吐量最高比 GPT-OSS-120B 高 2.2 倍，比 Qwen3.5-122B 高 7.5 倍。测量使用 B200 GPU，报告每 GPU 每秒输出 token 数。报告对每个模型取 vLLM 或 TensorRT-LLM 中更好的结果。

精度设置很重要。2.2 倍的对比使用 NVFP4 的 Nemotron 3 Super 与 MXFP4 权重的 GPT-OSS-120B。Qwen3.5-122B 显示为 [bf16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16")，因此 7.5 倍这个数字混合了架构、量化和服务栈差异。在同一张归一化图表中，bf16 的 Nemotron 3 Super 吞吐量约为 bf16 Qwen3.5-122B 的 2 倍。

我不会把这些数字当作普适的速度排名。64K token 的输出是一项苛刻的长生成工作负载，最佳后端也会随硬件和软件版本而变化。短对话回答、不同的批大小，或缺少优化的潜在 MoE 与 MTP 算子的运行时，都可能产生不同的排序。

这个结果仍然有用。它展示了完整架构加优化服务栈在与长推理轨迹和智能体循环相关的工作负载下能做到什么。同一报告中的[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")分数与 GPT-OSS-120B 和 Qwen3.5-122B 大体相当，而不是在每项任务上都全面胜出。因此我的解读是：这是一次以吞吐量为重点的发布，同时把准确率保持在相近区间。

## 一个关于本地模型的现实提醒

原始笔记称 Nemotron 3 Super 是一个有趣的智能体应用本地模型。这里的*本地*指一台有分量的工作站或本地部署服务器。bf16 模型卡列出的最低配置是 8 张 H100 80 GB GPU。NVIDIA 也提供 FP8 和 NVFP4 检查点，更低精度的版本大幅减少了权重占用。

该模型支持最高 100 万 token 的上下文，而 Hugging Face 默认配置使用 256K，因为更长的上下文需要更多内存。上下文支持、检查点装得下、有可用的吞吐量，是三个相互独立的问题。对于智能体应用，我建议用实际的提示词长度、工具调用频率和输出长度来对所选的量化方式和服务引擎做基准测试。

[架构卡片](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b)有高分辨率模型图和配置摘要。[潜在 MoE 讲解](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/)聚焦被压缩的专家通路。

[![Nemotron 3 Super 120B-A12B 架构图与基准测试对比](https://sebastianraschka.com/images/blog/2026/nemotron-3-super/hero.webp)](https://substack.com/@rasbt/note/c-226718041)

出自原始 [Substack 笔记](https://substack.com/@rasbt/note/c-226718041)的组合图。它概括了 88 层混合架构、潜在 MoE 通路，以及 NVIDIA 发布时的基准测试与吞吐量对比。

来源：我 [Substack 笔记](https://substack.com/@rasbt/note/c-226718041)的扩展网站版，架构与基准测试细节来自 NVIDIA 的技术报告。

---
title: "Nemotron 3 Ultra 潜在 MoE 笔记"
title_en: "Nemotron 3 Ultra Latent MoE Note"
source: https://sebastianraschka.com/blog/2026/nemotron-3-ultra-latent-moe.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Nemotron 3 Ultra 潜在 MoE 笔记

> 原文：[Nemotron 3 Ultra Latent MoE Note](https://sebastianraschka.com/blog/2026/nemotron-3-ultra-latent-moe.html)

对开放权重 LLM 来说，这是不错的一周。一些新发布能装进笔记本或工作站，而 [Nemotron 3 Ultra](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4) 则处于光谱的另一端。

Ultra 的总参数为 5500 亿，每个 token 激活 550 亿。据 NVIDIA 的[技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)，即使是 NVFP4 检查点也有约 330 GiB。这是一个服务器规模的模型，但从性能效率的角度看它仍然很有意思。

从高层看，Ultra 是 [Nemotron 3 Super](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16) 的更大号兄弟。它保留了混合 Mamba-Transformer 堆叠、[潜在 MoE（Latent MoE）](https://sebastianraschka.com/glossary/#latent-moe "Latent MoE")层和多 token 预测。NVIDIA 提高了模型的宽度、深度和激活专家容量，同时保持同样的 4 倍潜在瓶颈。

## 108 层混合堆叠

模型有 108 层，分为 48 层 Mamba-2、48 层潜在 [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") 和 12 层分组查询注意力。稀疏注意力锚点提供全局的 token 到 token 交互，而 Mamba 层用固定大小的循环状态处理大部分序列处理工作。

模型宽度为 8,192。每个注意力层使用 64 个查询头、2 个键值头，头维度为 128。在 12 层注意力上，这相当于每 token 每条序列 12 KiB 的逻辑 bf16 [KV 缓存](https://sebastianraschka.com/glossary/#kv-cache "KV Cache")。Mamba 层维护循环状态，而不是为每个保留的 token 追加一条 KV 条目。

这一布局扩展了 88 层的 Super 模型——后者有 40 层 Mamba-2、40 层潜在 MoE 和 8 层注意力。尽管 Ultra 按总参数量是 Super 的四倍多，层间比例仍然相近。

## 潜在 MoE 如何扩展

我觉得最有意思的是[潜在 MoE](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/) 通路。常规 MoE 层把模型宽度的表示直接送入选中的专家；潜在 MoE 先把这个表示降维投影，在更窄的空间里运行路由专家，再把合并后的结果投影回模型宽度。

Super 的路由通路是 `4096 -> 1024 -> 4096`。Ultra 把每个宽度翻倍，使用 `8192 -> 2048 -> 8192`。因此两个模型使用相同的 4 倍压缩比。

每个 Ultra MoE 层包含 512 个路由专家，每个 token 选择 22 个。路由专家的中间维度为 5,120。一个单独的共享专家中间维度为 10,240，处理每个 token。

潜在瓶颈和稀疏路由以不同方式节省算力。路由限制了运行的专家数量；瓶颈缩小了被选专家通路的宽度。下投影和上投影会增加工作量，因此 4 倍瓶颈并不意味着 MoE 层或整个模型有 4 倍加速。

规模变化仍然可观。Super 总参数 1200 亿、激活 120 亿；Ultra 增长到总参数 5500 亿、激活 550 亿，同时保持大致相同的 10% 激活参数比例和相同的潜在压缩系数。

## MTP 与混合精度配方

Ultra 用两个多 token 预测头训练。这两个头共享参数，共享草稿模块由一个注意力层接一个 MoE 层组成。推理期间，该模块可以为投机解码提出未来 token。运行时必须支持这条通路，实际加速能兑现多少取决于主模型接受草稿 token 的频率。

NVIDIA 用 20 万亿文本 token 对基座模型做了预训练。前 15 万亿 token 强调广泛的领域覆盖，随后在学习率衰减阶段使用 5 万亿更高质量的 token。后续一个 330 亿 token 的阶段把[上下文长度](https://sebastianraschka.com/glossary/#context-length "Context Length")扩展到 100 万 token。

"在 NVFP4 下预训练"这一说法需要一个限定。NVIDIA 把最后 16 层、Mamba 输出投影、潜在投影、注意力投影、MTP 层和嵌入保持在更高精度。发布的量化检查点也混合了格式：路由专家矩阵乘法使用 NVFP4，共享专家和 Mamba 线性层使用 FP8，注意力和潜在投影仍为 [bf16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16")。

这是一份有针对性的精度配方。报告的评估把一个选定的每元素 5.03 比特配置与 bf16 检查点做比较，在其测试套件上发现结果相近。在那次对比中，两个版本还使用了不同的 vLLM 版本，因此不应把小的分数差异归因于量化本身。

## 内存与上下文的注意事项

混合 Mamba 模型减少了每层都做全注意力带来的 KV 缓存增长。但循环状态并非免费。NVIDIA 报告，在最高 64K token 的序列长度下，Ultra 的 FP32 Mamba 缓存比它的 FP8 KV 缓存更大。发布的 NVFP4 设置用带随机舍入的 FP16 存储 Mamba 状态。

检查点大小让实际规模更清楚。在一个拥有 640 GiB 总内存的八卡 H100 节点上，NVIDIA 估计 NVFP4 权重约 330 GiB，FP8 检查点约 540 GiB。更小的权重占用给激活、缓存、批处理和 MTP 模块留出了更多空间。

Ultra 支持最高 100 万 token 的上下文。上下文容量与可用吞吐量仍是两个独立的问题。长提示词仍然需要缓存内存、预填充（prefill）算力，以及能高效处理混合 Mamba 与注意力状态的服务栈。

## 如何看待吞吐量结果

NVIDIA 报告，在 8K token 输入接 64K 输出 token 的设置下，最高吞吐量比 GLM-5.1-754B-A40B 高 5.9 倍、比 Kimi-K2.6-1T-A32B 高 4.8 倍、比 Qwen3.5-397B-A17B 高 1.6 倍。所有模型在 GB200 硬件上使用 NVFP4。

这是一项苛刻的长生成工作负载。该对比还对 Nemotron 3 Ultra 使用 TensorRT-LLM、对其他模型使用 vLLM，并取使用或不使用投机解码中更好的结果。它测量的是完整架构与服务栈，而不是隔离潜在 MoE 的效果。

图 1 下方各面板使用 2026 年 6 月 4 日的独立 Artificial Analysis 快照。这些数值回答的是一个稍不同的问题，因为它们反映的是那天可用的服务提供商和推理配置。随着推理软件和服务设置的改进，排行榜位置和输出速率都可能变化。

对我来说，Ultra 最有用的地方是作为一个规模化的范例。NVIDIA 保留了与 Super 相同的基本潜在 MoE 瓶颈，然后把宽度从 4,096 提高到 8,192、层数从 88 提高到 108。其余的效率故事来自混合序列层、稀疏专家路由、[混合精度](https://sebastianraschka.com/glossary/#mixed-precision "Mixed Precision")、MTP，以及围绕该模型设计的服务系统。

[LLM Architecture Gallery 卡片](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-ultra-550b-a55b)有更高分辨率的架构图，并链接到发布的配置。

[![Nemotron 3 Ultra 架构与基准测试总览](https://sebastianraschka.com/images/blog/2026/nemotron-3-ultra/hero.webp)](https://substack.com/@rasbt/note/c-270588404)

图 1：Nemotron 3 Ultra 组合了 48 层 Mamba-2、48 层潜在 MoE 和 12 层分组查询注意力。右上的图示显示了同一周的若干更小的开放权重发布。下方各面板是 2026 年 6 月 4 日的 Artificial Analysis 快照。

来源：我 [Substack 笔记](https://substack.com/@rasbt/note/c-270588404)的扩展网站版，架构、训练与推理细节来自 NVIDIA 的 [Nemotron 3 Ultra 技术报告](https://arxiv.org/abs/2606.15007)和[发布配置](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16/blob/main/config.json)。

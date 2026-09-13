---
title: "MiniMax M3 登陆 vLLM：面向 1M token 多模态推理的 Day-0 服务"
title_en: "MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning"
source: https://vllm.ai/blog/2026-06-12-minimax-m3-vllm
crawled: 2026-09-12
translated: 2026-09-13
---

# MiniMax M3 登陆 vLLM：面向 1M token 多模态推理的 Day-0 服务

> 原文：[MiniMax M3 in vLLM: Day-0 Serving for 1M-Token Multimodal Reasoning](https://vllm.ai/blog/2026-06-12-minimax-m3-vllm) · vLLM 博客

作者：vLLM 团队

[#minimax](https://vllm.ai/blog/tags/minimax)[#Day-0 支持](https://vllm.ai/blog/tags/day-0-support)[#MoE](https://vllm.ai/blog/tags/moe)[#长上下文](https://vllm.ai/blog/tags/long-context)

我们很高兴宣布 vLLM 对 MiniMax M3 系列的 Day-0 支持，包括 [`MiniMaxAI/MiniMax-M3`](https://huggingface.co/MiniMaxAI/MiniMax-M3) 与 [`MiniMaxAI/MiniMax-M3-MXFP8`](https://huggingface.co/MiniMaxAI/MiniMax-M3-MXFP8) 上的 BF16 与 MXFP8 检查点。

MiniMax M3 为生产环境中日益常见的工作负载而生：百万级 token 上下文、原生多模态推理、编程与智能体工作流、工具使用，以及可控的思考行为。难点不只是加载模型，而是让全新的 MiniMax Sparse Attention 路径、多模态预处理、MXFP8 MoE 执行、EAGLE3 投机解码、前缀缓存与部署配方，在用户真正能跑起来的服务引擎中协同工作。

本文将介绍模型特性、vLLM 实现、发布背后的内核与缓存工作，以及 Day 0 之后我们即将落地的后续优化。

![图 1：MiniMax M3 的 Day-0 支持为 vLLM 带来长上下文、多模态、稀疏注意力服务。](https://vllm.ai/blog-assets/figures/minimax-m3/hero-minimax-m3-vllm.svg)

图 1：MiniMax M3 的 Day-0 支持为 vLLM 带来长上下文、多模态、稀疏注意力服务。

## TL;DR

vLLM 为 MiniMax M3 提供初始 Day-0 支持：

- **模型家族**：BF16 与 MXFP8 的 MiniMax M3 检查点，支持 1M token 上下文（取决于硬件容量与部署配置）。
- **核心架构**：MiniMax Sparse Attention（MSA），一种稠密/稀疏混合注意力设计，对 128 token 的 KV 块打分，为每个 query 和 KV 组选出 top 块，并在选出的块上运行 GQA 注意力。
- **服务栈**：`minimax_m3` 工具与推理解析器、思考模式控制、纯文本与多模态路径、TP/EP 部署、前缀缓存、分块预填充、EAGLE3 投机解码，以及可直接使用的 Docker 镜像。
- **投机解码**：Day-0 EAGLE3 支持，草稿模型发布于 [`Inferact/MiniMax-M3-EAGLE3`](https://huggingface.co/Inferact/MiniMax-M3-EAGLE3)。
- **RL 后训练**：在 [NVIDIA NeMo RL](https://github.com/NVIDIA-NeMo/RL) 中进行 Day-0 MiniMax M3 GRPO 后训练，vLLM 作为生成后端。
- **性能工作**：MSA 预填充与解码内核、indexer-score 与 top-k 内核、融合的 QKNorm + RoPE + KV 插入、GemmaNorm 与量化路径优化，以及 MXFP8 MoE 后端集成。
- **路线图**：FP8 indexer/KV 缓存工作、TRTLLM-Gen MoE、更广泛的分离式服务配方、上下文并行的长预填充工作，以及进一步的多模态网关优化。

## MiniMax M3 支持矩阵

| 能力 | MiniMax M3 新增了什么 | vLLM 支持 |
| --- | --- | --- |
| 1M token 上下文 | 长上下文文本、代码、智能体轨迹与文档工作负载 | `--max-model-len` 配置、块大小 128 配方、前缀缓存、分块预填充、MSA 内核 |
| MiniMax Sparse Attention | 在选出的 128 token KV 块上做块稀疏 GQA | 混合注意力后端、indexer-score 内核、top-k 块选择、稀疏 GQA 预填充/解码 |
| MXFP8 模型权重 | 面向大规模部署的高效 MoE 服务 | Blackwell 级系统上的 DeepGEMM MXFP8 MoE 后端，Hopper 级系统上的 Marlin MXFP8 |
| 原生多模态 | 文本之外的图像与视频输入 | 模型专属多模态预处理路径与 vLLM 服务集成 |
| 工具与推理输出 | 智能体工作流与可控思考 | `minimax_m3` 工具解析器、`minimax_m3` 推理解析器、`thinking_mode` 聊天模板控制 |
| EAGLE3 投机解码 | 面向生成的草稿模型加速 | 使用 [`Inferact/MiniMax-M3-EAGLE3`](https://huggingface.co/Inferact/MiniMax-M3-EAGLE3) 的 Day-0 EAGLE3 配方 |

## 快速开始：用 vLLM 运行 MiniMax M3

在 NVIDIA 上，MSA 使用默认注意力后端，视觉编码器运行在 FlashInfer 后端上（`--mm-encoder-attn-backend FLASHINFER`），并配备共享内存处理器缓存与数据并行编码器。

在 Blackwell 级节点上运行 MXFP8 检查点，起点配置如下：

```
vllm serve MiniMaxAI/MiniMax-M3-MXFP8 \
  --block-size 128 \
  --tensor-parallel-size 8 \
  --enable-expert-parallel \
  --tool-call-parser minimax_m3 \
  --enable-auto-tool-choice \
  --reasoning-parser minimax_m3 \
  --mm-encoder-attn-backend FLASHINFER \
  --mm-processor-cache-type shm \
  --mm-encoder-tp-mode data
```

对于 BF16：

```
vllm serve MiniMaxAI/MiniMax-M3 \
  --block-size 128 \
  --tensor-parallel-size 8 \
  --enable-expert-parallel \
  --tool-call-parser minimax_m3 \
  --enable-auto-tool-choice \
  --reasoning-parser minimax_m3 \
  --mm-encoder-attn-backend FLASHINFER \
  --mm-processor-cache-type shm \
  --mm-encoder-tp-mode data
```

具体配方取决于目标加速器、模型 dtype、上下文长度、流量形态，以及部署优先吞吐量、延迟还是最大上下文容量。已在 NVIDIA H200、GB200 与 B300 上完成验证。完整的 NVIDIA 与 AMD 启动配方、部署策略与调优旋钮，请参阅 [MiniMax M3 的 vLLM recipe](https://recipes.vllm.ai/MiniMaxAI/MiniMax-M3)。

### AMD ROCm

MiniMax M3 可运行于 AMD Instinct GPU。MSA 运行在 Triton 注意力后端上，因此 AMD 部署需要添加 `--attention-backend TRITON_ATTN`；视觉编码器使用 AITER FlashAttention 后端（`--mm-encoder-attn-backend ROCM_AITER_FA`），配备共享内存处理器缓存与数据并行编码器。

对于 MXFP8 检查点：

```
vllm serve MiniMaxAI/MiniMax-M3-MXFP8 \
  --block-size 128 \
  --tensor-parallel-size 8 \
  --attention-backend TRITON_ATTN \
  --tool-call-parser minimax_m3 \
  --enable-auto-tool-choice \
  --reasoning-parser minimax_m3 \
  --mm-encoder-attn-backend ROCM_AITER_FA \
  --mm-processor-cache-type shm \
  --mm-encoder-tp-mode data
```

对于 BF16：

```
vllm serve MiniMaxAI/MiniMax-M3 \
  --block-size 128 \
  --tensor-parallel-size 8 \
  --attention-backend TRITON_ATTN \
  --tool-call-parser minimax_m3 \
  --enable-auto-tool-choice \
  --reasoning-parser minimax_m3 \
  --mm-encoder-attn-backend ROCM_AITER_FA \
  --mm-processor-cache-type shm \
  --mm-encoder-tp-mode data
```

已在 MI350 系列与 MI300 系列 GPU 上完成验证。

### 重要的部署旋钮

MiniMax M3 有几个比通常更重要的旋钮。`--block-size 128` 让 vLLM 缓存块与 MSA 的稀疏块粒度对齐。`--max-model-len` 控制对外声明的上下文长度与 KV 容量规划。`--tensor-parallel-size` 与 `--enable-expert-parallel` 决定注意力、投影与 MoE 专家如何跨 GPU 切分。智能体工作负载应启用 `minimax_m3` 工具与推理解析器；长上下文配方应说明针对该目标是否启用了前缀缓存、分块预填充、EAGLE3 投机解码与多模态预处理。

### EAGLE3 投机解码

MiniMax M3 在 vLLM 中同样拥有 Day-0 EAGLE3 投机解码支持。草稿模型发布于 [`Inferact/MiniMax-M3-EAGLE3`](https://huggingface.co/Inferact/MiniMax-M3-EAGLE3)，当工作负载与接受行为契合目标流量时，部署可以用草稿模型路径降低生成延迟。

要启用 EAGLE3，在服务命令中加入投机解码配置：

```
vllm serve MiniMaxAI/MiniMax-M3-MXFP8 \
  --block-size 128 \
  --tensor-parallel-size 8 \
  --enable-expert-parallel \
  --tool-call-parser minimax_m3 \
  --enable-auto-tool-choice \
  --reasoning-parser minimax_m3 \
  --mm-encoder-attn-backend FLASHINFER \
  --mm-processor-cache-type shm \
  --mm-encoder-tp-mode data \
  --speculative-config '{"method":"eagle3","model":"Inferact/MiniMax-M3-EAGLE3","num_speculative_tokens":3,"attention_backend":"FLASH_ATTN"}'
```

示例使用 `num_speculative_tokens=3`，这是验证用的保守起点。生产配方应根据部署流量组合的接受率、TPOT、吞吐量与目标延迟来调优该值。

### 思考模式

MiniMax M3 提供可控的思考行为。在 vLLM 中，通过 `chat_template_kwargs` 传递模式：

```
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")
model = client.models.list().data[0].id

messages = [{"role": "user", "content": "Explain MiniMax Sparse Attention."}]

for mode in ["enabled", "disabled", "adaptive"]:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body={
            "chat_template_kwargs": {
                "thinking_mode": mode,
            },
        },
    )
    print(mode, response.choices[0].message.content)
```

## 模型关键特性与新能力

MiniMax M3 在三个方向上对推理系统意义重大。

### 借助 MiniMax Sparse Attention 实现 1M token 上下文

最核心的架构变化是 MiniMax Sparse Attention（MSA）。MSA 不再让每个 query 对完整 KV 缓存做稠密注意力，而是使用索引路径为 KV 块打分，选出与真正注意力计算最相关的块。默认粒度是 128 token 的 KV 块，选出的块在 GQA 组内共享。

具体来说，每个 query token 遵循三步：

1. 用一个小的索引头为候选 KV 块打分。
2. 选出 top 块，同时应用配置的块规则。
3. 只在选出的 KV 块上运行 online-softmax 注意力。

这既保留了用户期望的长上下文行为，又限制了每个生成 token 的注意力工作量。实际上，MiniMax Sparse Attention 正是让 MiniMax M3 的 1M token 上下文在 vLLM 服务中切实可行的机制。

![图 2：MiniMax Sparse Attention 在从 1M token 历史中选出稀疏的 128 token KV 块的同时，保持局部与全局上下文可用。](https://vllm.ai/blog-assets/figures/minimax-m3/msa-1m-context.svg)

图 2：MiniMax Sparse Attention 在从 1M token 历史中选出稀疏的 128 token KV 块的同时，保持局部与全局上下文可用。

### MSA 机制的更多细节

MSA 区分两个问题：哪些历史块值得读，以及如何在这些块上运行注意力。索引路径通过为固定的 128 token KV 块打分回答第一个问题。稀疏 GQA 路径通过在选出的块上运行注意力回答第二个问题。

选出的集合并不只是学习到的 top-k。M3 配置暴露了 `init_blocks` / `sparse_init_block` 与 `local_blocks` / `sparse_local_block`，但当前配方使用 `init_blocks=0` 与 `local_blocks=1`。实践中，确定性规则是 query token 附近的局部窗口块，其余选中的块来自 indexer 打分的 top-k 选择。正确性取决于若干细节：末尾不完整的块必须被屏蔽，块内的因果边界必须被遵守，同时进入 top-k 的局部块不能被计入两次，批量请求的有效块范围也可能各不相同。

### 原生多模态

MiniMax M3 是一个多模态模型，而不是带独立外挂的纯文本检查点。服务路径必须处理图像与视频输入，把它们预处理为 patch 张量，保留网格元数据，并把结果交给模型，同时不占用生成的 GPU 时间。

对 vLLM 部署而言，发布工作包括模型专属的多模态预处理与解析器支持，让用户可以通过同一个服务界面运行纯文本、工具使用、推理与多模态工作负载。

### MXFP8 MoE 权重

MXFP8 检查点为高效大规模服务而设计。验证使用了 Blackwell 级系统上的 DeepGEMM MXFP8 MoE 后端，以及 Hopper 级系统上的 Marlin MXFP8。

## vLLM 实现

MiniMax M3 是一个混合模型：一些层走稠密注意力，稀疏层走 MiniMax MSA 后端。vLLM 把这种区分藏在模型与注意力后端之内，因此调度器、缓存分配、批处理、前缀缓存与服务从外部看起来仍然熟悉。对这些内部机制不熟悉的读者，可以把 [Anatomy of vLLM](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) 作为本节的补充读物。

### MiniMax Sparse Attention 后端

MSA 后端有两项不同的职责。

首先，它计算稀疏元数据。indexer 为 KV 块打分，应用配置的块选择规则，并输出 top-k 块 ID。对 M3 来说，选择以块为单位：稀疏性的单位正是缓存管理器早已理解的、类页面的 128 token 块。

其次，它计算这些块上的注意力。预填充与解码形状不同，因此 vLLM 使用专门的内核：

- **预填充 indexer-score**：Triton 内核计算块分数与 top-k 块选择。
- **预填充稀疏 GQA**：Triton 与 [MiniMax-AI/MSA](https://github.com/MiniMax-AI/MSA) 的 CuTe/SM100 路径支持块稀疏 GQA 注意力。CuTe 路径把 query 到块的映射反转为 K 主序的 CSR 形式，使 KV 块可以被高效复用。
- **解码 indexer-score**：split 风格的解码内核扫描候选块、打分并合并 top-k 结果。
- **解码稀疏 GQA**：GQA 解码内核消费选出的块页面并合并部分注意力输出。

### 预填充执行

预填充处理提示并创建 KV 缓存。对 M3 而言，提示长度与稀疏元数据都很重要。该路径有四个概念阶段：

1. **构建 query、key、value 与索引投影。** 稠密投影产生 indexer 与注意力内核所需的表示。
2. **为块打分。** 索引路径为每个候选 KV 块计算分数。打分归约可以使用块级规则（如 max 或 log-sum-exp），取决于模型配置。
3. **选择块。** top-k 选择把学习到的块分数与配置的块规则结合，然后为每个 query 与 KV 组输出块 ID。
4. **运行稀疏 GQA。** 注意力内核只读取选出的 KV 块，计算出的 online-softmax 注意力结果与限制在该选中集合上的稠密注意力一致。

对最后的稀疏 GQA 工作，有两种实用的调度方式。query 主序（query-major）调度直观直接：每个 query 遍历自己选出的 KV 块。当许多 query 选中同一个块时（长提示场景），KV 块主序（KV-block-major）调度更优。在该调度中，vLLM 构建一个 K 到 Q 的映射，让一个 KV 块在输出合并前可以被多个 query 加载复用。

### 解码执行

解码的形状不同。每一步通常为每个活跃序列处理一个新 token，但批次可能包含许多上下文长度各异的序列。运行时更新缓存状态、为候选块打分、应用局部窗口处理、选出 top 块、运行稀疏 GQA 解码，并在内核使用 split 工作时合并部分输出。因为这发生在每个生成的 token 上，indexer-score 与 top-k 内核属于 TPOT 的一部分，而不只是启动开销。

M3 的稀疏注意力配置控制块大小、top-k 数量、可选的 init 块、局部窗口块、索引维度、稀疏层 ID、分数类型，以及那些仅将索引注意力用于选择的层。关键的实现规则是：每个选出的块 ID 都必须能映射回 vLLM 调度器与缓存管理器所知的同一个逻辑请求状态。

![图 3：vLLM 将稠密层路由到标准注意力，将稀疏层路由到 MiniMax MSA 后端。](https://vllm.ai/blog-assets/figures/minimax-m3/msa-backend-dispatch.svg?v=2)

图 3：vLLM 将稠密层路由到标准注意力，将稀疏层路由到 MiniMax MSA 后端。

### KV 缓存布局：标准存储，稀疏计算

MiniMax M3 可以把 KV 存储为普通的分页 KV，并在计算路径中应用稀疏性。这让 vLLM 保持缓存管理器简单，同时为内核提供所需的灵活性：

- 主注意力 KV 缓存与 indexer K 缓存被显式跟踪。
- 一旦配方的缓存状态交互得到验证，前缀缓存与分块预填充就可以继续使用稳定的缓存块。
- 相关的分离式服务与 NIXL 风格的传输路径可以把缓存当作分页状态处理，而注意力后端负责稀疏选择。

### 前缀缓存与分块预填充

前缀缓存很重要，因为 M3 工作负载经常复用长提示：代码库、文档、多轮智能体轨迹与多模态上下文。分块预填充很重要，因为一个 1M token 的请求不应作为一个巨大预填充垄断引擎。它们共同构成发布就绪的压力测试：索引缓存状态、主注意力 KV 状态、稠密注意力状态、前缀命中、抢占、批处理与长上下文分块边界，都必须在同一块表上达成一致，配方才能被视为生产可用。

### 多模态与解析器集成

MiniMax M3 包含模型专属的工具、推理与多模态输入解析行为。vLLM 支持包括：

- `--tool-call-parser minimax_m3`，用于工具调用格式化。
- `--reasoning-parser minimax_m3`，用于推理输出提取。
- 对 `thinking_mode` 的聊天模板支持。
- 面向图像与视频输入的多模态预处理集成。

对生产部署而言，预处理应尽可能在 GPU 执行之前完成。目标架构是一个网关，负责下载媒体、解码帧、采样视频、缩放与归一化图像、创建 patch 张量，并把可直接运行的张量传给 worker。

这很重要，因为多模态请求在 API 边界看起来可能很小，但预处理之后会变大。一个视频可能需要帧采样、逐帧缩放、patch 生成与元数据打包。把 CPU 密集的媒体工作留在上游，能让 GPU 调度更容易推理。

解析器一侧对智能体流量同样重要。工具调用与推理解析器把模型专属的文本约定转换为结构化 API 响应。没有正确的解析器，模型生成的有用文本可能难以被应用消费。

![图 4：对 MiniMax M3，CPU 侧的图像与视频预处理应把就绪的张量交给 vLLM worker，为推理保留 GPU 时间。](https://vllm.ai/blog-assets/figures/minimax-m3/multimodal-request-path.svg?v=2)

图 4：对 MiniMax M3，CPU 侧的图像与视频预处理应把就绪的张量交给 vLLM worker，为推理保留 GPU 时间。

## 性能优化

MiniMax M3 转移了瓶颈。MSA 减少了稠密注意力工作，但引入了 indexer-score 工作、块选择、稀疏元数据构建与额外的小内核。vLLM 的 Day-0 实现聚焦于让这些新部件保持低廉。

指导原则很简单：不要把更多时间花在决定读哪些块上，以至于超过不读全部块所省下的时间。这一原则体现在三个地方：块主序预填充、精简的解码 indexer-score 内核，以及围绕注意力路径融合小的逐元素或缓存写入内核。

### KV 块主序预填充

预填充期间，许多 query token 可能选中同一个 KV 块。朴素的 query 主序稀疏注意力内核会反复把同一个 KV 块从 HBM 搬到片上内存。块稀疏结构给了我们更好的调度：围绕 KV 块组织工作，然后处理需要每个块的所有 query。

[MiniMax-AI/MSA](https://github.com/MiniMax-AI/MSA) 的 CuTe/SM100 路径通过构建 K 到 Q 的 CSR 映射、运行块主序稀疏注意力内核，并使用 log-sum-exp 归约合并部分输出做到这一点。这提升了长提示与智能体流量（长缓存上下文很常见）下的算术强度。

![图 5：KV 块主序预填充让选出的 KV 块在多个 query 间复用，减少最终 LSE 归约之前的冗余内存搬运。](https://vllm.ai/blog-assets/figures/minimax-m3/kv-block-major-prefill.svg)

图 5：KV 块主序预填充让选出的 KV 块在多个 query 间复用，减少最终 LSE 归约之前的冗余内存搬运。

### 解码 indexer-score 内核

解码时，indexer 位于每个生成 token 的关键路径上。引擎必须把 query 侧索引向量与候选 key 侧索引向量比较，把每个 128 token 块归约为一个分数，应用局部窗口处理，并只保留 top 块用于稀疏 GQA。

优化后的解码路径使用专门的 indexer-score 内核，而不是把问题当作填充后的稠密 GEMM。这避免了围绕参差不齐的每请求块范围增加额外工作，并让 top-k 边界紧贴分数计算。

解码路径还必须注意内存流量。选出的 KV 块在逻辑序列空间中是稀疏的，但在内存中仍是类页面的，因此内核应避免把稀疏页面变成大型临时稠密张量，除非复用能够证明这样做值得。

### 解码内核中的投机解码

EAGLE3 支持还要求 MiniMax M3 解码内核能高效处理投机验证。在投机解码中，一个请求可以一次验证多个草稿 token，因此 MSA 解码内核不能假设每个请求恰好只有一个 query token。

一种回退方案是用预填充内核做投机验证，但代价很高：预填充内核通常为更大的 token 数调优，因此在小的草稿 token 批次上表现不佳。它们通常也不兼容完整 CUDA Graph 模式，而后者对低延迟解码是重要优化。

Day-0 实现更新了 MSA 解码 indexer、top-k 选择与稀疏 GQA 解码内核，以支持统一的 `decode_query_len`。这些内核按请求主序展平投机验证 token，然后把每个 query token 映射回正确的请求元数据、序列长度、块表与因果位置。这让 EAGLE3 验证可以使用解码专用的 split-K 路径，而不是退回到针对性更弱的预填充风格路径，同时让投机路径与现有解码实现保持接近。

同一路径对统一的投机解码批次支持完整 CUDA Graph 覆盖。内核启动网格保持形状稳定，选定的参数避免不必要的 Triton 特化，填充的请求行被显式处理，因此捕获的图可以安全地回放。这些细节很重要，因为只有当草稿 token 接受不被额外的内核启动、重新编译或缓存状态开销抵消时，投机解码才能改善 TPOT。我们预计会在不同草稿长度、并发级别与流量组合下继续优化这条路径。

### 内核融合

若干较小的内核被融合或经由自定义算子路由，以减少启动开销与 HBM 往返：

- **QKNorm + RoPE + KV 插入**：为 MSA 路径合并归一化、位置编码与缓存写入。
- **GemmaNorm 与 AllReduce + Norm 工作**：减少张量并行执行中归一化相关的开销。
- **量化路径清理**：改进 `silu_mul_quant_fp8` 与相关 MXFP8/MoE 输入路径。
- **路由器与 MoE 内核**：减少稀疏专家路径的开销，并为更深入的 TRTLLM-Gen 集成做准备。

发布路径刻意保守：正确性与稳定的缓存行为优先于在 Day 0 启用每一种可能的图或融合开关。更激进的融合可以随着公开配方成熟而落地。

### 量化与 KV 缓存数据类型

MXFP8 检查点主要改变权重与 MoE 执行，而不是 KV 缓存的概念结构。公开配方应分别说明模型 dtype、MoE 后端与 KV 缓存策略："MXFP8 模型"并不意味着每个缓存与中间张量都是 MXFP8。路线图包含 FP8 indexer 与 KV 缓存路径，因为 KV 容量直接决定部署能服务多少长上下文与批量流量。

### CUDA Graph 与编译行为

CUDA Graph 对解码很有价值，因为 M3 在每个 token 步骤周围引入了若干小操作。但只有当捕获路径在不同批次形状、缓存状态与稀疏元数据下保持稳定时，图捕获才有帮助。Day-0 路径在需要之处使用保守的图设置，然后随着验证成熟扩大覆盖。

## 验证

在公开发布之前，vLLM 团队围绕准确率、吞吐量、投机解码与容器可用性进行了每日验证。

验证循环有三个目标：

1. **功能正确性**：模型能加载、服务请求、解析工具与推理输出，并能处理纯文本与多模态输入。
2. **准确率对齐**：在内核、缓存、解析器与配方变更之后，基准结果仍与预期模型行为一致。
3. **服务就绪**：容器镜像能在目标加速器上以预期的 TP/EP/投机解码设置运行。

最有用的测试把短正确性任务与长输出、长上下文工作负载结合起来。短任务能快速发现解析器、格式与明显的数值问题。长上下文任务能发现 MSA 元数据、前缀缓存、分块预填充与 KV 缓存布局问题。投机解码测试能发现普通准确率运行中可能不会显现的接受率回退。

来自该验证的一个代表性快照，在 B300 上测得：

| 维度 | 结果 |
| --- | --- |
| GSM8K 严格/灵活准确率 | 91.51% / 91.66% |
| ShareGPT @256 吞吐量 | 8,530 tok/s |
| ShareGPT @256 TPOT | 56.0 ms |
| Speculative Sonnet TPOT，并发 1 / 16 / 64 | 4.51 / 9.04 / 14.36 ms |
| Sonnet 上的投机接受率 | ~67%，平均接受长度 ~3.0 |

这些是工程验证测量，不是官方基准排名；确切结果随镜像版本、权重、配方与硬件而异。

![图 6：在公开的 MiniMax M3 配方发布之前，候选版本验证会检查准确率、吞吐量与投机解码。](https://vllm.ai/blog-assets/figures/minimax-m3/validation-dashboard.svg)

图 6：在公开的 MiniMax M3 配方发布之前，候选版本验证会检查准确率、吞吐量与投机解码。

## 超越服务：用 NeMo RL 做 RL 后训练

Day-0 支持不只关乎推理服务。强化学习框架把 vLLM 用作在训练循环内产生 rollout 的生成引擎，因此在 [vLLM PR #45381](https://github.com/vllm-project/vllm/pull/45381) 中支撑服务的同一批 MiniMax M3 工作，也让 M3 的后训练在 Day 0 即可实现。

[NVIDIA NeMo RL](https://github.com/NVIDIA-NeMo/RL) 现在可以运行 MiniMax M3，vLLM 作为非共置生成后端。短程 GRPO（Group Relative Policy Optimization）后训练运行已在 BF16 检查点上完成验证，使用带专家并行的 NeMo AutoModel 与 BF16 vLLM 生成。长时间运行的收敛性与专家并行之外的并行策略仍在验证中，但早期结果已经展示了扎实的服务路径的价值：服务 M3 的引擎同样是驱动 RL 训练 rollout 阶段的引擎。[NeMo RL MiniMax M3 指南](https://github.com/NVIDIA-NeMo/RL/blob/minimax-m3/docs/guides/minimax-m3.md)提供了参考配方。

## 路线图：前方的路

Day-0 实现只是起跑线。接下来的工作已经在推进中：

- **FP8 indexer 与 KV 缓存路径**：在保持稀疏注意力准确率的同时，降低 KV 缓存内存压力并提高批量容量。
- **TRTLLM-Gen MoE**：改进 Blackwell 上 MXFP8 专家执行的性能。
- **上下文并行**：当一个节点不够用时，改进超长上下文预填充的扩展性。
- **分离式服务**：扩展面向 M3 流量的 NIXL 与预填充/解码分离配方，建立在 [Large-Scale Serving with vLLM](https://vllm.ai/blog/2025-12-17-large-scale-serving) 的方向之上。
- **内核融合**：减少 MSA 引入的众多小的 indexer、top-k、量化与归一化内核。
- **多模态网关路径**：把图像与视频预处理挡在关键的 GPU 生成循环之外。

## MiniMax M3 vLLM 常见问题

### vLLM 支持 MiniMax M3 吗？

支持。本文介绍了 vLLM 对 MiniMax M3 BF16 与 MXFP8 检查点的 Day-0 支持，包括 MSA 注意力、模型专属解析器、EAGLE3 投机解码、多模态预处理、TP/EP 服务配方，以及可直接使用的 Docker 镜像。

### 什么是 MiniMax Sparse Attention？

MiniMax Sparse Attention 为固定的 128 token KV 块打分，为每个 query 与 GQA 组选出最相关的块，应用配置的局部窗口规则，并在选出的集合上运行稀疏 GQA。在当前 M3 配方中，对应 `init_blocks=0` 与 `local_blocks=1`。

### MXFP8 意味着 KV 缓存也是 MXFP8 吗？

不是。MXFP8 描述的是模型权重与 MoE 执行路径。KV 缓存 dtype 是单独的服务决策；当前的稀疏注意力验证把原生 KV 存储与量化 KV 缓存支持视为独立的路线图工作。

### 对 1M token 上下文而言，哪些设置最重要？

重要的起点是 `--block-size 128`、足以支撑所选批次与上下文形状的显存，以及一份说明是否启用前缀缓存、分块预填充与 EAGLE3 投机解码的配方。默认情况下 vLLM 从模型配置读取上下文长度，因此无需设置 `--max-model-len`。如果显存有限或不需要完整的 1M token 窗口，可以传入 `--max-model-len` 把上限调低，减轻 KV 缓存压力。

## 致谢

我们要感谢 MiniMax 团队开源 MiniMax-M3，也感谢 MiniMax 管理层对 vLLM 的信任与支持！模型支持由 Inferact Inc. 主导，这家公司的愿景是把 vLLM 培育成世界级的 AI 推理引擎，通过让推理更便宜、更快速来加速 AI 进步。NVIDIA 与 AMD 为硬件支持做出了贡献。

## 相关 vLLM 阅读

MiniMax M3 建立在 vLLM 的多个领域之上：

- [Anatomy of vLLM](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm)：调度器、KV 缓存、前缀缓存与分布式执行背景。
- [Speculative Decoding in vLLM](https://vllm.ai/blog/2024-10-17-spec-decode) 与 [P-EAGLE](https://vllm.ai/blog/2026-03-13-p-eagle)：草稿模型路径。
- [Large-Scale Serving with vLLM](https://vllm.ai/blog/2025-12-17-large-scale-serving)、[KV Offloading Connector](https://vllm.ai/blog/2026-01-08-kv-offloading-connector) 与 [Moriio KV Connector](https://vllm.ai/blog/2026-04-07-moriio-kv-connector)：前缀复用、KV 搬运与分离式服务。
- [NeMo RL: MiniMax M3 guide](https://github.com/NVIDIA-NeMo/RL/blob/minimax-m3/docs/guides/minimax-m3.md)：以 vLLM 为生成后端的 GRPO RL 后训练。

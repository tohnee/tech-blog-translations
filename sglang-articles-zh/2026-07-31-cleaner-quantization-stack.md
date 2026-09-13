---
title: "SGLang 迈向更整洁的量化栈"
title_en: "Toward a Cleaner Quantization Stack in SGLang"
author: "SGLang X Ascend Team"
date: "July 28, 2026"
previewImg: /images/blog/2026-07-31-cleaner-quantization-stack/01-cover.png
type: blog
source: https://lmsys.org/blog/2026-07-31-cleaner-quantization-stack/
translated: 2026-09-12
---

# SGLang 迈向更整洁的量化栈

> 原文：[Toward a Cleaner Quantization Stack in SGLang](https://lmsys.org/blog/2026-07-31-cleaner-quantization-stack/) · LMSYS Blog · SGLang X Ascend Team

量化已经从一项高级特性，演变为**高吞吐 LLM 推理服务不可或缺的组成部分**。随着检查点格式、模型架构与硬件后端数量的不断增长，量化栈的维护难度也在与日俱增。

本文介绍 [SGLang issue #15194](https://github.com/sgl-project/sglang/issues/15194) 中提出的架构性变更。新设计将检查点解析、参数注册、权重加载、后处理与内核执行拆分为职责清晰、可复用的组件。

## 1. 为什么这很重要？

生产级推理服务引擎已不能再只依赖单一的低比特内核。它们必须处理多样化的检查点格式（如 AWQ、GPTQ、Compressed-Tensors、ModelSlim 和 Quark）、稠密与 MoE 权重、KV 缓存格式、注意力内核，以及跨 CUDA GPU、昇腾（Ascend）NPU、CPU 等后端的硬件专属执行逻辑。

当格式解析、参数注册、权重加载、后处理、平台检查和内核执行全部塞进同一个类里时，每新增一种格式或后端都会加剧耦合。其结果就是代码越来越难以审查、测试、复用和扩展。

<div align="center">
  <img src="/images/blog/2026-07-31-cleaner-quantization-stack/02-diff-diagram.png" alt="Before and after quantization architecture" />
  <br>
  <em>图 1：本次重构将格式相关的权重处理与平台相关的处理及内核执行分离开来。</em>
</div>

在旧设计中，单一量化方法往往要负责整条路径：定义参数、加载权重、转换布局、选择后端并启动内核。要支持另一个平台，就意味着在同一个面向格式的类里继续堆叠分支——即便其中许多硬件逻辑本可以在别处复用。

这一点之所以重要，是因为量化同时关系到部署规模与推理服务性能。更低比特的权重可以在权重带宽受限（weight-bandwidth-bound）的负载中减少内存流量，尤其是在解码阶段。而端到端的收益则取决于内核效率、量化开销以及预填充/解码的负载构成。

<div align="center">
  <em>表 1：量化性能与精度对比</em>
  <br>

| 模型         | 量化方案 | E2E(s) | TTFT(ms) | ITL(ms) | 准确率(%) | 权重大小(GB) |
|:------------:|:-------------:|:-----:|:--------:|:-------:|:-----------:|:----------------:|
| Qwen3-30B-A3B | BF16         | 57.12 | 2084.41  | 26.23   | 91.1        | 61.08            |
| Qwen3-30B-A3B | W8A8         | 54.94 | 2553.06  | 24.60   | 90.8        | 31.29            |
| Qwen3-30B-A3B | W4A4_W8A8    | 52.97 | 2299.51  | 23.84   | 89.4        | 21.59            |

  <em style="color: #888;">复现结果请参见附录。</em>
</div>

因此，量化栈需要在不牺牲量化本身核心价值（性能收益）的前提下，支撑格式与硬件的快速增长。

## 2. 基于方案（Scheme）的量化架构

[#15194](https://github.com/sgl-project/sglang/issues/15194) 中启动的重构将量化路径划分为四个职责清晰的层次：

1. **量化配置（Quant Config）：** 解析检查点元数据，选择量化路径。
2. **Linear/MoE 方法（Method）：** 适配 SGLang 层接口，并分派具体操作。
3. **方案（Scheme）：** 定义与格式和层相关的参数、形状及加载行为。
4. **内核（Kernel）：** 执行后端专属的权重变换与计算。

<div align="center">
  <img src="/images/blog/2026-07-31-cleaner-quantization-stack/03-main_scheme.png" alt="Scheme-based quantization architecture" />
  <br>
  <em>图 2：基于方案的架构将检查点语义与硬件执行分离开来。</em>
</div>

方案与内核之间的分界是关键。方案描述一个检查点如何映射到 SGLang 的层上，而内核则实现特定后端所需的操作。这样一来，多种检查点格式可以共享同一个内核，硬件专属逻辑也不会混入面向格式的代码。

SGLang 正在逐步迁移到这一结构。在整理后的离线路径中，方案负责参数定义与权重加载，内核负责加载后的变换与执行。同一个内核还可以作为独立 runner 服务于在线量化路径，使后端支持可以独立开发和测试。

随着迁移的推进，预计会有更多的后端选择逻辑移入 SGLang 的平台层。届时方案可以保持硬件无关，由平台在执行前选择兼容的内置或第三方内核。

## 3. 收益：更快的开发与更广的复用

新架构的主要收益在于检查点格式与硬件后端可以独立演进。方案定义量化权重如何映射到 SGLang 层，内核则处理后端专属的变换与执行。

这种分离带来几项实际优势：

* **变更更小、更易审查：** 新格式只需添加自己的配置和方案，无需改动无关的后端代码。同样，新内核也可以在接入某个检查点格式之前独立实现和审查。

* **测试更聚焦：** 格式检测、配置解析、参数注册和加载行为可以在纯 CPU 机器上测试；硬件相关的测试则可以专注于权重变换、内核正确性与性能。

* **更少的重复代码：** 多种格式可以复用同一个硬件内核，而不必为等价操作各自维护一份实现。

* **超越线性层的清晰扩展路径：** 同样的结构可以扩展到 MoE 专家、注意力投影、KV 缓存和通信算子。

<div align="center">
  <img src="/images/blog/2026-07-31-cleaner-quantization-stack/04-kernel_reusing_Diagram.png" alt="Multiple quantization schemes reusing shared hardware kernels" />
  <br>
  <em>图 3：多种检查点格式可以共享同一个后端内核。</em>
</div>

对用户而言，这将带来跨格式、跨平台更一致的行为。对开发者而言，它降低了耦合，让新增量化支持变得更容易，也不会动摇既有路径的稳定性。

## 4. 未来工作

实时计划见 [SGLang Quantization Roadmap - 2026 H2 (#31783)](https://github.com/sgl-project/sglang/issues/31783)。主要优先事项包括：

- 完成架构

  完成 `Config -> Method -> Scheme -> Kernel` 重构，将离线检查点加载与在线量化分离开来，并标准化加载后的权重处理。机器可读的能力注册表（capability registry）还将帮助 SGLang 在执行前校验格式、层、模型与后端的兼容性。

- 扩大生产覆盖

  在 CUDA、ROCm、昇腾 NPU、CPU 及其他后端上扩展 W8A8、W4A8、W4A4、NVFP4、MXFP4 和 MXFP8 的支持。这项工作还包括 MoE、VLM、扩散模型、量化注意力、KV 缓存、通信以及分离式 KV 传输。

- 评估新的低比特方法

  新架构让 MXFP6、MXINT8、基于旋转的量化、向量量化、两比特 KV 缓存、三值推理以及稀疏+低比特执行等方法的原型验证与横向对比变得更加容易。

## 5. 致谢

- Huawei 昇腾团队

  我们感谢 Huawei 昇腾 NPU 团队在量化架构、内核集成与模型适配方面的持续合作。特别感谢 Liang Zhen (@[ping1jing2](https://github.com/ping1jing2))、Yaochen Han (@[Alisehen](https://github.com/Alisehen))、Tamir Baydasov (@[TamirBaydasov](https://github.com/TamirBaydasov))、Yechang Guo (@[YChange01](https://github.com/YChange01))、Artem Savkin (@[OrangeRedeng](https://github.com/OrangeRedeng)) 和 Junlin Wu (@[TallMessiWu](https://github.com/TallMessiWu))，他们在昇腾硬件上的 GPTQ、ModelSlim、Compressed-Tensors、INT8、MXFP8、MXFP4、MoE、KV 缓存与通信量化支持方面做出了贡献。

- SGLang 社区

  我们感谢更广泛的 SGLang 社区，包括量化 codeowner：Cheng Wan (@[ch-wan](https://github.com/ch-wan))、Xiaoyu Zhang (@[BBuf](https://github.com/BBuf))、Zhiyu Cheng (@[Edwardf0t1](https://github.com/Edwardf0t1))、Fan Yin (@[FlamingoPg](https://github.com/FlamingoPg)) 和 Peng Zhang (@[AniZpZ](https://github.com/AniZpZ))，也感谢所有在 CUDA、ROCm、昇腾 NPU、XPU、CPU 等后端上实现格式、开发内核、审查架构变更、验证量化路径的贡献者。

  特别感谢 Intel Neural Compressor 与 AutoRound 的贡献者在 AutoRound 集成上的合作，也感谢 NVIDIA、AMD、ModelOpt、Compressed-Tensors、Quark、GGUF 以及各硬件后端社区——他们的工作持续扩展着 SGLang 可用的高效推理格式范围。

最后，感谢每一位为 SGLang 量化路线图做出贡献的人——从提出新数值格式的研究者，到构建生产级内核、测试与部署方案的维护者。

## 6. 附录

- 请使用以下命令复现性能结果。
    ```shell
    BF16_model_path: https://www.modelscope.cn/models/Qwen/Qwen3-30B-A3B
    W8A8_model_path: https://www.modelscope.cn/models/Eco-Tech/Qwen3-30B-A3B-w8a8
    W4A4_W8A8_model_path: https://www.modelscope.cn/models/Eco-Tech/Qwen3-30B-A3B-w4a4-LAOS
    
    # launch server
    python3 -m sglang.launch_server \
        --device npu \
        --attention-backend ascend \
        --trust-remote-code \
        --tp-size 4 \
        --model-path "{BF16_model_path | W8A8_model_path | W4A4_W8A8_model_path}" \
        --port 30088 \
        --mem-fraction-static 0.8
    
    # launch bench:
    python -m sglang.bench_serving \
        --backend sglang \
        --random-range-ratio 1.0 \
        --dataset-path ./datasets/ShareGPT_V3_unfiltered_cleaned_split.json \
        --dataset-name random \
        --num-prompts 64 \
        --max-concurrency 64 \
        --random-input-len 2048 \
        --random-output-len 2048 \
        --host 127.0.0.1 \
        --port 30088 \
        --flush-cache
    ```

- 请使用以下命令复现精度结果。
    ```shell
    python ./benchmark/gsm8k/bench_sglang.py \
        --num-questions 1319 \
        --port 30088 \
        --data-path ./datasets/gsm8k/test.jsonl
    ```

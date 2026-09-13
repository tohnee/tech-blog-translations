---
title: "用 SGLang Runtime 实现更快的开源 Llama3 推理服务（对比 TensorRT-LLM、vLLM）"
title_en: "Achieving Faster Open-Source Llama3 Serving with SGLang Runtime (vs. TensorRT-LLM, vLLM)"
author: "The SGLang Team"
date: "Jul 25, 2024"
previewImg: /images/blog/sglang_llama3/preview.png
source: https://lmsys.org/blog/2024-07-25-sglang-llama3/
translated: 2026-09-12
---

# 用 SGLang Runtime 实现更快的开源 Llama3 推理服务（对比 TensorRT-LLM、vLLM）

> 原文：[Achieving Faster Open-Source Llama3 Serving with SGLang Runtime (vs. TensorRT-LLM, vLLM)](https://lmsys.org/blog/2024-07-25-sglang-llama3/) · LMSYS Blog · The SGLang Team

在 LMSYS.org，我们运营 [Chatbot Arena](https://chat.lmsys.org/) 平台已有一年多，为数百万用户提供服务。我们深知高效推理服务对 AI 产品和研究有多么关键。凭借运营经验和深入研究，我们持续改进底层的服务系统，从上层的多模型服务框架 [FastChat](https://github.com/lm-sys/FastChat/tree/main)，到高效推理引擎 [SGLang Runtime (SRT)](https://github.com/sgl-project/sglang)。

本文聚焦于 [SGLang Runtime](https://github.com/sgl-project/sglang)——一个面向 LLM 和 VLM 的通用推理服务引擎。TensorRT-LLM、vLLM、MLC-LLM 和 Hugging Face TGI 等现有方案各有长处，但我们发现它们有时难以上手、不易定制，或性能有所欠缺。这促使我们开发了 SGLang v0.2，目标是打造一个不仅易用、易修改，而且具备顶级性能的推理服务引擎。SGLang 虽然包含前端语言特性，但本文只讨论后端运行时，并将 "SGLang" 与 "SGLang Runtime" 交替使用，均指该运行时。

与 TensorRT-LLM 和 vLLM 相比，SGLang Runtime 在在线和离线场景中都能持续保持领先或有竞争力的性能，覆盖从 Llama-8B 到 Llama-405B 的模型、A100 和 H100 GPU，以及 FP8 和 FP16 精度。**SGLang 的性能始终优于 vLLM，在 Llama-70B 上吞吐量最高达到 3.1 倍；并且经常与 TensorRT-LLM 持平，有时甚至更胜一筹**。更重要的是，SGLang 完全开源、采用纯 Python 编写，核心调度器仅用不到 4K 行代码实现。

SGLang 是一个基于 Apache 2.0 许可证的开源项目。它已被 LMSYS Chatbot Arena（用于支撑其中一部分模型）、Databricks、多家初创公司和研究机构采用，累计生成数万亿 token，并支撑了更快的迭代。随着它逐渐从研究原型走向成熟，我们诚邀社区与我们一道打造下一代高效引擎。

## 基准测试设置

我们对离线和在线两种使用场景分别进行了基准测试：

- **离线：** 一次性发送 1K 至 6K 个请求，测量输出吞吐量（token/秒），定义为输出 token 数除以总时长。测试数据集包括若干合成数据集和 ShareGPT 数据集。我们用 Input-512-Output-1024 表示这样一种数据集：输入长度从均匀分布 [1, 512] 中采样，输出长度从 [1, 1024] 中采样。
- **在线：** 以每秒 1 到 16 个请求（RPS）的速率发送请求，测量端到端延迟的中位数。我们使用合成数据集 Input-1024-Output-1024。

我们使用默认参数的 vLLM 0.5.2，以及采用推荐参数和调优批大小的 TensorRT-LLM v0.10.0。所有引擎均关闭前缀缓存。这样做的目的是测量不带任何附加功能（如投机解码或缓存）时的基础性能。SGLang 和 vLLM 的基准测试使用 OpenAI 兼容 API，TensorRT-LLM 则使用 Triton 接口。

更多细节和可复现脚本见附录 A。对每个模型，我们先给出离线结果，再给出在线结果。

<span style="color: red;">更新（2024-07-26 凌晨 4 点，太平洋时间）：</span> 我们发现最初的合成数据生成流程存在一些问题：它生成的输入大多偏短，导致本博文第一版中的数据集描述不准确。在当前版本中，我们修复了这些问题，并引入了更多数据集配置，以覆盖长输入和短输入两种情况。

## Llama-8B on 1 x A100（bf16）

先从小模型 Llama-8B 开始。下图展示了各引擎在离线设置下、跨六个不同数据集所能达到的最大输出吞吐量。在短输入数据集上，TensorRT-LLM 和 SGLang 都能取得高达每秒 5000 token 的出色吞吐量，而 vLLM 则明显落后。

<img src="/images/blog/sglang_llama3/8b_throughput.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>

下方的在线基准测试图呈现出与离线情形类似的趋势。TensorRT-LLM 和 SGLang 表现相当，都能承受 RPS \> 10 的负载，而 vLLM 在高请求速率下延迟显著上升。  

<img src="/images/blog/sglang_llama3/8b_latency.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>

## Llama-70B on 8 x A100（bf16）

接下来是使用 8 GPU 张量并行的更大的 Llama-70B 模型，趋势与 8B 情形类似。在下方的离线基准测试中，TensorRT-LLM 和 SGLang 都能扩展到很高的吞吐量。   

<img src="/images/blog/sglang_llama3/70b_bf16_throughput.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>

在下方的在线测试图中，TensorRT-LLM 凭借其高效的内核实现和运行时展现出出色的延迟表现。   

<img src="/images/blog/sglang_llama3/70b_bf16_latency.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>


## Llama-70B on 8 x H100（fp8）

接下来测试 FP8 性能。vLLM 和 SGLang 都使用来自 CUTLASS 的 FP8 内核。在离线设置中，SGLang 的批调度器非常高效，能够在更大的批大小下继续扩展吞吐量，在该场景下取得最高吞吐量。其他系统则由于 OOM、缺少大量手动调优或其他开销，无法扩展吞吐量或批大小。总体而言，SGLang 在短输入上表现更好，而 TensorRT-LLM 在长输入上表现更好，这很可能源于二者不同的内核实现和批调度策略。

<img src="/images/blog/sglang_llama3/70b_fp8_throughput.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>

上述趋势在线上场景同样成立，SGLang 和 TensorRT 的中位数延迟相近。

<img src="/images/blog/sglang_llama3/70b_fp8_latency.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>

## Llama-405B on 8 x H100（fp8）

最后，我们对最大的 405B 模型进行了性能基准测试。由于模型很大，大部分时间都花在 GPU 内核上；有限的 KV 缓存容量也压缩了调度空间，因此不同框架之间的差距缩小。SGLang 仍然优于 vLLM，但提升幅度不那么显著。由于 405B 模型刚刚发布，TensorRT-LLM 的一些最新优化尚未包含在预构建的 Docker 镜像中，因此我们在这里略去了 TensorRT-LLM 的性能数据。我们正在与 NVIDIA 团队合作，以便正确地对 TensorRT-LLM 在该模型上的性能进行基准测试。

<img src="/images/blog/sglang_llama3/405b_fp8_throughput.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>

<br>

<img src="/images/blog/sglang_llama3/405b_fp8_latency.svg" style="display: flex; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%;"></img>

## SGLang 概览

SGLang 是一个面向大语言模型和视觉语言模型的服务框架。它吸收并增强了多个开源 LLM 服务引擎的众多优秀设计，包括 [LightLLM](https://github.com/ModelTC/lightllm)、[vLLM](https://blog.vllm.ai/2023/06/20/vllm.html) 和 [Guidance](https://github.com/guidance-ai/guidance)。它采用来自 [FlashInfer](https://flashinfer.ai/2024/02/02/introduce-flashinfer.html) 的高性能注意力 CUDA 内核，并受 [gpt-fast](https://pytorch.org/blog/accelerating-generative-ai-2/) 启发集成了 torch.compile。

此外，我们还引入了一些创新，例如用于自动 KV 缓存复用的 [RadixAttention](https://arxiv.org/abs/2312.07104)，以及用于快速受限解码的[压缩状态机](https://lmsys.org/blog/2024-02-05-compressed-fsm/)。SGLang 以其高效的[批调度器](https://github.com/sgl-project/sglang/tree/main/python/sglang/srt/managers)而闻名，它完全用 Python 实现。SGLang 高效的基于 Python 的批调度器扩展性良好，常常能比肩甚至超越用 C++ 构建的闭源实现。
本博文展示的加速主要来自出色的系统工程。

下表从多个方面对比了 SGLang、TensorRT-LLM 和 vLLM。在性能方面，SGLang 和 TensorRT-LLM 都很出色。在易用性和可定制性方面，SGLang 轻量且模块化的核心使其易于定制，而 TensorRT-LLM 复杂的 C++ 技术栈和安装配置流程则使其更难使用和修改。SGLang 的源代码完全开源，而 TensorRT-LLM 仅部分开源。相比之下，vLLM 则受制于较高的 CPU 调度开销。

|  | SGLang | TensorRT-LLM | vLLM |
| :---- | :---- | :---- | :---- |
| 性能 | 优秀 | 优秀 | 一般 |
| 易用性 | 良好 | 较差 | 良好 |
| 可定制性 | 高 | 低 | 中 |
| 源代码开放程度 | 完全开源 | 部分开源 | 完全开源 |
| 编程语言 | Python | C++ | Python |

## 下一步计划

我们很高兴分享最新的基准测试结果。虽然仍有许多工作要做，但这证明了我们"开发一个简单、可定制且高性能的服务引擎"的理念是可行的。敬请期待长上下文与 MoE 优化等新特性，以及详细的技术解读。欢迎加入我们，一起构建下一代服务引擎：[https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang)。

## 试用 Llama 推理服务

按照以下步骤，你可以轻松部署一个 Llama 模型。

1. 通过 pip、源码或 Docker [安装](https://github.com/sgl-project/sglang/tree/main?tab=readme-ov-file#install) SGLang。
2. 启动服务器：
    ```
    # Llama 8B
    python -m sglang.launch_server --model-path meta-llama/Meta-Llama-3.1-8B-Instruct

    # Llama 405B
    python -m sglang.launch_server --model-path meta-llama/Meta-Llama-3.1-405B-Instruct-FP8 --tp 8
    ```
3. 使用 OpenAI 兼容 API 发送请求：
    ```
    curl http://localhost:30000/v1/completions \
      -H "Content-Type: application/json" \
      -d '{
        "model": "default",
        "prompt": "Say this is a test",
        "max_tokens": 7,
        "temperature": 0
      }'
    ```
4. 运行基准测试：
    ```
    python3 -m sglang.bench_serving --backend sglang --num-prompts 1000
    ```

## 团队

本博文由 Liangsheng Yin、Yineng Zhang、Ying Sheng 以及 65 位以上的开源[贡献者](https://github.com/sgl-project/sglang/graphs/contributors)共同完成。我们感谢 Databricks 的支持，Ying Sheng 的工作是在 Databricks 完成的。我们特别感谢 Lianmin Zheng、Zihao Ye 和 Horace He 提供的技术支持，感谢 Matei Zaharia 的宝贵建议，以及 Cody Yu 的反馈。

## 附录 A：详细的基准测试设置

复现该基准测试的说明见 [sglang/benchmark/blog\_v0\_2](https://github.com/sgl-project/sglang/tree/main/benchmark/blog\_v0\_2)。

在所有基准测试中，我们设置了 \`ignore\_eos\` 或 \`min\_length/end\_id\`，以确保每个引擎输出的 token 数量相同。我们尝试过使用 vLLM 0.5.3.post1，但它在高负载下经常崩溃，而且根据我们的部分测试结果，其性能与 vLLM 0.5.2 相当甚至更差。因此，我们改为报告 vLLM 0.5.2 的结果。我们深知不同的服务器配置会显著影响服务性能，但为了模拟普通用户的使用情形，我们基本使用各引擎的默认参数。

对于 8B 和 70B 模型，我们使用 [meta-llama/Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) 和 [meta-llama/Meta-Llama-3-70B-Instruct](http://meta-llama/Meta-Llama-3-70B-Instruct) 的 bf16 检查点，以及 [neuralmagic/Meta-Llama-3-70B-Instruct-FP8](https://huggingface.co/neuralmagic/Meta-Llama-3-70B-Instruct-FP8) 的 fp8 检查点。对于 405B 模型，所有基准测试均使用哑权重（dummy weights）。由于 TensorRT-LLM 最新的 r24.06 镜像不支持官方 [meta-llama/Meta-Llama-3.1-405B-FP8](https://huggingface.co/meta-llama/Meta-Llama-3.1-405B-FP8) 检查点中的 fbgemm\_fp8 量化，我们在所有框架中都采用逐层 fp8 量化，并对除 lm\_head 之外的所有层进行量化。我们认为这能在所有引擎之间提供公平的对比。所用的 A100 和 H100 GPU 均为 80GB SXM 版本。

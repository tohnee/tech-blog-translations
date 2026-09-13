---
title: "为扩散 LLM 强力赋能：LLaDA 2.0 的 Day-0 支持"
title_en: "Power Up Diffusion LLMs: Day‑0 Support for LLaDA 2.0"
author: "Ant Group DeepXPU Team, SGLang Team"
date: "December 19, 2025"
source: https://lmsys.org/blog/2025-12-19-diffusion-llm/
translated: 2026-09-12
previewImg: /images/blog/dllm/preview.png
---

# 为扩散 LLM 强力赋能：LLaDA 2.0 的 Day-0 支持

> 原文：[Power Up Diffusion LLMs: Day‑0 Support for LLaDA 2.0](https://lmsys.org/blog/2025-12-19-diffusion-llm/) · LMSYS Blog · Ant Group DeepXPU Team, SGLang Team

## TL;DR

我们很高兴地介绍 SGLang 中扩散大语言模型（dLLM）框架的设计与实现。通过复用现有的分块预填充（Chunked-Prefill）机制，我们的系统实现了：

- 无缝集成：内建于 SGLang 生态，无需改动核心架构。
- 性能继承：该框架直接受益于 SGLang 既有的推理优化。
- 最大灵活性：用户可以完全自由地定义和定制扩散解码算法。

## 背景

### 动机

今年早些时候，[LLaDA](https://arxiv.org/pdf/2502.09992) 作为首个扩散大语言模型（Diffusion Large Language Model）首次亮相，随即引起了学术界和工业界的广泛关注。这一由中国人民大学与蚂蚁集团合作完成的成果表明，dLLM 独特的执行范式展现出更出色的数据理解能力。此外，与自回归模型相比，dLLM 还能实现更快的推理速度，尤其是在小批量这类低延迟场景中。

与此同时，随着 dLLM 参数规模的持续增长，我们也观察到了与 AR LLM 类似的 scaling law 效应。为了打造更好的 dLLM，我们训练了 100B 的 [LLaDA2.0-flash](https://github.com/inclusionAI/LLaDA2.0/blob/main/tech_report.pdf) 模型。

然而，在训练 [LLaDA2.0-flash](https://github.com/inclusionAI/LLaDA2.0/blob/main/tech_report.pdf) 的过程中，我们遇到了一系列严峻的 AI 基础设施工程挑战，其中最重要的是模型评估与 RL 后训练的效率和稳定性。

### 挑战

目前可用于 dLLM 的推理引擎，尚不足以支撑更大规模 dLLM 的评估与 RL 后训练需求。例如，[Fast-dLLM](https://github.com/NVlabs/Fast-dLLM) 这类工具是出色的研究工具，更适合算法研究者调试和验证各种扩散解码算法；但在提供生产可用的推理服务能力方面（如批处理、调度、RL 生态集成和并行），它们有所欠缺。

相比之下，SGLang 是当今最流行的 LLM 推理引擎之一，具有多重优势：

1. 生产可用：它已被数千家公司部署于推理服务，具备成熟可靠的工程能力。
2. 技术领先：SGLang 本身集成了大量优秀的先进推理优化技术，社区源源不断地产出新的优化。
3. 生态完整：它与 RL 后训练生态集成得非常好，尤其是在分布式权重 GPU P2P 更新等方面。

然而，核心问题在于：SGLang 目前只支持自回归计算范式，尚未适配 LLM 的扩散计算方式。

因此，我们面临的挑战是：如何在现有 SGLang 框架内引入对 dLLM 的支持，而不损害其现有架构？目标有两个：一方面让 dLLM 享受到 SGLang 提供的全部优化优势，另一方面避免为了适配扩散计算而对 SGLang 框架做出重大的、有损性的改动。

## 设计

### 关键洞察

基于对 dLLM 当前发展的观察，我们总结出几条关键洞察：

1. 由于双向注意力扩散（Bidirectional Attention Diffusion）计算开销巨大，且对 KV 缓存的利用效率低下，主流 dLLM 正日益转向块扩散（Block Diffusion）架构。
2. 块扩散的计算模式与 SGLang 现有的分块预填充（Chunked-Prefill）流程高度相似。
3. 与自回归语言模型不同，扩散语言模型采用多种解码策略，需要一个专门的接口来支持灵活的解码算法定制。

### 架构

我们的做法是利用 SGLang 现有的分块预填充流水线，为块扩散 LLM 实现计算支持。这一方法让我们无需改动 SGLang 核心框架，就能把 dLLM 无缝集成进 SGLang 生态，使 dLLM 直接受益于 SGLang 积累的全部推理优化技术。

<p align="center">
  <img src="/images/blog/dllm/main-flow.png" alt="主执行流程">
  <br>
</p>


如图所示，我们对 SGLang 框架的改动非常克制，几乎不触碰其核心。SGLang 原有的 `generate request` 执行流程保持不变。我们的实现主要集中在对现有分块预填充机制的利用与改造上，具体工作聚焦在两个关键组件：`prefill adder` 和 `chunked reqs`。

在 SGLang 中，分块预填充的初衷是最大化 GPU 利用率。因此，单个 chunk 的大小通常设置得相当大——序列长度从 2K 到 16K token 不等，取决于 GPU 型号。当序列足够长时，一个 chunk 自然只处理一个请求，这也是当前 `prefill adder` 和 `chunked req` 的实现方式。

然而，dLLM 的解码过程有所不同：它按块（block）级别切分序列长度。以 LLaDA2.0 为例，其块大小为 32 个 token。如果沿用 SGLang 之前一次只处理一个大请求的逻辑，GPU 性能显然会被浪费。因此，批处理是一个必须解决的关键问题。为实现高效批处理，我们对 `chunked reqs` 和 `prefill adder` 都做了改造，使它们能够在单个计算周期内处理多个扩散块（Diffusion Block）。

此外，在实际的解码执行层面，我们在 TP Worker 和 Model Runner 之间插入了一层扩散算法抽象层。

具体来说：
- 如果 Worker 判定当前处理的是扩散模型，执行流程就进入这个专门的分支；
- TP Worker 随后调用扩散算法的 `run` 函数；
- 该算法内部通过一个前向迭代循环，持续驱动 Model Runner 执行推理计算，直到整个 Block（例如全部 32 个 token）解码完成。

### 注意力掩码

<p align="center">
  <img src="/images/blog/dllm/casual-mask.png" alt="注意力掩码示意图">
  <br>
</p>

在单次模型前向计算中，块扩散与分块预填充最显著的差异在于注意力掩码的处理方式。

- 块扩散使用块级因果掩码（block-wise causal mask）。
- AR 模型的分块预填充使用传统的逐 token 因果掩码。

我们可以把块扩散视为对 SGLang 现有分块预填充机制的功能扩展。在具体的注意力计算上，单次前向包含两个计算部分，其最终输出会被拼接：

1. 上下文查询（Context Query）：使用当前 `Q_curr`（当前块的 query 向量）对已有的 KV 缓存执行双向注意力。这一计算在块扩散和分块预填充中完全相同，目的是让当前块关注所有历史信息。
2. 块内查询（Intra-Block Query）：使用当前 `Q_curr` 与它自身的 KV（即当前块内的 key 和 value）执行前向计算。
    - 块扩散在这一步使用双向注意力。
    - 分块预填充在这一步必须使用因果掩码。

简而言之，如果把 `Q_curr` 部分的注意力掩码可视化为几何形状：
  - 分块预填充（因果掩码）的计算对应一个梯形（或三角形）掩码。
  - 块扩散（双向注意力）的计算对应一个矩形掩码。

## 流式输出动画

下面是一段对比 LLaDA2.0-flash-CAP（100B / BF16）与 gpt-oss-120B（117B / MXFP4）流式输出的动画。LLaDA2.0-flash-CAP 使用 SGLang dLLM、在 8 × H20 上以 TP8 提供服务，而 gpt-oss-120B 在相同硬件上使用 SGLang 的标准 AR 流程提供服务。

两个模型都被要求用 10 种编程语言实现快速排序算法——这是一项特别适合扩散 LLM 的任务。如图所示，在该场景下，LLaDA2.0-flash-CAP 的吞吐量达到 935 tokens/s，显著高于 gpt-oss-120B（263 tokens/s）。

<p align="center">
  <img src="/images/blog/dllm/llada2-vs-gpt-oss.gif" alt="LLaDA2.0-flash-CAP 与 gpt-oss-120B 对比动画">
  <br>
</p>

SGLang dLLM 与 SGLang 自回归模型一样支持流式输出：只不过它每次输出一个块（例如 32 个 token），而不是一个 token。

<p align="center">
  <img src="/images/blog/dllm/dllm-animation.gif" alt="dLLM 流式输出动画">
  <br>
</p>

## 使用方法

### 启动命令示例

```shell
python3 -m sglang.launch_server \
  --model-path inclusionAI/LLaDA2.0-mini \ # example HF/local path
  --dllm-algorithm LowConfidence \
  --dllm-algorithm-config ./config.yaml \ # Optional. Uses the algorithm's default if not set.
  --host 0.0.0.0 \
  --port 30000
```
> 注意：使用 `--dllm-algorithm-config` 可对所选的 `--dllm-algorithm` 进行高级配置。这一特性将配置与代码解耦，通过统一入口为用户自定义算法提供灵活的定制与参数传递能力。

### 客户端代码示例

与其他受支持的模型一样，dLLM 可以通过 REST API 或离线 engine API 使用。

向运行中的服务器发起生成请求的 curl 示例：

```bash
curl -X POST "http://127.0.0.1:30000/generate" \
     -H "Content-Type: application/json" \
     -d '{
        "text": [
            "<role>SYSTEM</role>detailed thinking off<|role_end|><role>HUMAN</role>Write the number from 1 to 128<|role_end|><role>ASSISTANT</role>",
            "<role>SYSTEM</role>detailed thinking off<|role_end|><role>HUMAN</role>Write a brief introduction of the great wall<|role_end|><role>ASSISTANT</role>"
        ],
        "stream": true,
        "sampling_params": {
            "temperature": 0,
            "max_new_tokens": 1024
        }
    }'
```

下面的代码片段演示了如何使用离线 engine 基于给定输入生成内容：

```python
import sglang as sgl

def main():
    llm = sgl.Engine(model_path="inclusionAI/LLaDA2.0-mini",
                     dllm_algorithm="LowConfidence",
                     max_running_requests=1,
                     trust_remote_code=True)

    prompts = [
        "<role>SYSTEM</role>detailed thinking off<|role_end|><role>HUMAN</role>Write a brief introduction of the great wall<|role_end|><role>ASSISTANT</role>"
    ]

    sampling_params = {
        "temperature": 0,
        "max_new_tokens": 1024,
    }

    outputs = llm.generate(prompts, sampling_params)
    print(outputs)

if __name__ == '__main__':
    main()
```

## 性能
<p align="center">
  <img src="/images/blog/dllm/llada2_flash_main_bench.png" alt="LLaDA2.0-flash 主要结果">
  <br>
</p>

我们在广泛的标准评测任务上，将 LLaDA2.0-flash 与规模相当的高级自回归（AR）模型进行基准对比，以评估其任务效能。

总体结果显示，LLaDA2.0 架构不仅极具竞争力，还呈现出与 AR 模型能力差距不断缩小的可喜趋势。

<p align="center">
  <img src="/images/blog/dllm/llada2_despine_comparison.png" alt="LLaDA2.0-flash 性能">
  <br>
</p>

图中展示了 LLaDA2.0-flash 的两项互补测量指标：
- 在 12 项基准任务上，经过与未经过置信度感知并行（Confidence-Aware Parallel，CAP）训练所得到的平均得分与每前向 token 数（tokens-per-forward，TPF）。
- LLaDA2.0-flash 在 HumanEval、MBPP、GSM8K 和 CRUXEval 测试集上与规模相当的 AR 模型对比的推理速度（tokens/s）。

所有数据均在一致的推理服务环境（SGLang、H20 上 TP8）下采集，确保扩散 LLM 与自回归基线之间的公平比较。

在 0.95 阈值解码器下，LLaDA2.0-flash-CAP 达到了 500 TPS，显著优于标准版 LLaDA2.0-flash（383 TPS），并且在小批量设置下相比 AR 基线（258 TPS 和 237 TPS）取得了最高 1.9× 的加速。

## 路线图

### 已实现的关键特性

当前实现已完整支持以下关键推理服务特性：

- 块扩散 LLM 框架主逻辑
- 面向序列管理的完整 KV 缓存支持
- LLaDA-2.0-mini/flash 模型集成
- 支持自定义解码算法
- 完整的流式 I/O 能力
- 批处理支持（评审中）
- 张量并行支持
- CUDA 图优化

### 中长期路线图

[2025-Q4 与 2026-Q1 路线图](https://github.com/sgl-project/sglang/issues/14199)<br>
[RFC：SGLang 中的块扩散大语言模型（dLLM）框架](https://github.com/sgl-project/sglang/issues/12766)<br>
- 支持更多自回归语言模型已有的系统优化
- 集成更多常见的扩散解码策略/算法（例如 [Fast-dLLM v2](https://arxiv.org/pdf/2509.26328)）
- 增加对非块状 dLLM 的兼容（例如 LLaDA 与 RND1）

## 参考资料
[LLaDA1 技术报告](https://arxiv.org/pdf/2502.09992)<br>
[LLaDA2 技术报告](https://github.com/inclusionAI/LLaDA2.0/blob/main/tech_report.pdf)<br>
[Fast-dLLM v2 技术报告](https://arxiv.org/pdf/2509.26328)

## 致谢

- 蚂蚁集团 DeepXPU 团队：[Zehuan Li](https://github.com/Clawseven)、[Tiwei Bie](https://github.com/btw616)、Zhonghui Jiang、Jinghua Yao、Yusong Gao、[Mingliang Gong](https://github.com/brightcoder01)、Jianfeng Tan
- 蚂蚁集团 inclusionAI 团队：Kun Chen、[Zenan Huang](https://lccurious.github.io/)、Lin Liu、Fuyuan Chen、Lun Du、Da Zheng
- SGLang dLLM 团队：[Jinwei Yao](https://kivi-yao.github.io/)、[Mick Qian](https://github.com/mickqian)、[Liangsheng Yin](https://www.lsyin.me/)、[BBuf](https://github.com/BBuf)、Banghua Zhu、[Chenyang Zhao](https://zhaochenyang20.github.io/Chayenne/)
- NVIDIA Fast-dLLM 团队：[Chengyue Wu](https://hills-code.github.io/)、[Hao Zhang](https://research.nvidia.com/person/hao-zhang)、[Enze Xie](https://xieenze.github.io/)、[Song Han](https://hanlab.mit.edu/songhan)

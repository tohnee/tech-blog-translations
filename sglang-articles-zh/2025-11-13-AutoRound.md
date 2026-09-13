---
title: "🚀 AutoRound 携手 SGLang：用 AutoRound 实现量化模型推理"
title_en: "🚀 AutoRound Meets SGLang: Enabling Quantized Model Inference with AutoRound"
author: "By Intel Neural Compressor Team"
date: "November 14, 2025"
previewImg: /images/blog/AutoRound/preview.png
source: https://lmsys.org/blog/2025-11-13-AutoRound/
translated: 2026-09-12
---

# 🚀 AutoRound 携手 SGLang：用 AutoRound 实现量化模型推理

> 原文：[🚀 AutoRound Meets SGLang: Enabling Quantized Model Inference with AutoRound](https://lmsys.org/blog/2025-11-13-AutoRound/) · LMSYS Blog · Intel Neural Compressor Team

## 概述

我们非常高兴地宣布 [**SGLang**](https://github.com/sgl-project/sglang) 与 [**AutoRound**](https://github.com/intel/auto-round) 正式达成合作，为高效的大模型推理提供低比特量化支持。

通过这次集成，开发者现在可以使用 AutoRound 的符号梯度优化对大模型进行量化，并直接部署到 SGLang 的高效运行时中，以极小的精度损失和显著的延迟降低实现低比特模型推理。


## AutoRound 是什么？

AutoRound 是一个面向大语言模型（**LLM**）和视觉语言模型（**VLM**）的先进训练后量化（PTQ）工具包。它利用符号梯度下降（signed gradient descent）联合优化权重舍入与裁剪范围，在大多数场景下能够以极小的精度损失实现精确的低比特量化（例如 INT2–INT8）。例如，在 INT2 精度下，它的相对精度比主流基线最高高出 2.1 倍；在 INT4 精度下，AutoRound 在大多数情况下依然保持竞争优势。下图展示了 AutoRound 核心算法的概览。

完整的技术细节见 AutoRound 论文：

👉 [Optimize Weight Rounding via Signed Gradient Descent for the Quantization of LLMs](https://arxiv.org/abs/2309.05516)

<p align="center">
  <img src="/images/blog/AutoRound/autoround_overview.png" width="80%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>AutoRound 算法概览</em></p>

尽管性能出色，AutoRound 依然快速而轻量——在轻量模式（light mode）下，量化一个 72B 模型在单张 GPU 上只需 37 分钟。

它还支持混合位宽调优、lm-head 量化、GPTQ/AWQ/GGUF 格式导出，以及可自定义的调优配方。



## AutoRound 亮点

AutoRound 不仅专注于算法层面的创新与探索，也因其量化工程上的完备性而广受认可。

- **精度：** 在低比特精度下提供卓越的精度表现
<p align="center">
  <img src="/images/blog/AutoRound/int4_accs.png" width="80%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>INT4 权重下 10+ 项任务的平均精度</em></p>

- **量化方案：** 支持仅权重量化、权重与激活量化，激活量化同时支持动态与静态两种方式
- **混合位宽：** 提出了一种高效算法，可在几分钟内生成混合位宽 / 其他数据类型的量化方案
- **广泛的兼容性：**
  - 支持几乎所有主流 LLM 架构和 10 余种视觉语言模型（VLM）
  - 支持设备：CPU、Intel GPU、CUDA
  - 支持数据类型：INT2–INT8、MXFP4、NVFP4、FP8 和 MXFP8
- **效率：** 支持分块调优（block-wise tuning），在不牺牲吞吐量的前提下降低 VRAM 占用，同时保持速度

<p align="center">
  <img src="/images/blog/AutoRound/timecost.png" width="80%"> 
</p>
<p align="center" style="color:gray; text-align: center;"><em>量化耗时对比</em></p>

- **社区采用：**
  - 与 SGLang、TorchAO、Transformers 和 vLLM 无缝协作
  - 被 [Intel](https://huggingface.co/Intel)、[OPEA](https://huggingface.co/OPEA)、[Kaitchup](https://huggingface.co/kaitchup) 和 [fbaldassarri](https://huggingface.co/fbaldassarri) 等 HuggingFace 模型仓库广泛使用，累计下载量约两百万次
- **导出格式：**
  - AutoRound
  - GPTQ
  - AWQ
  - GGUF
  - Compressed-tensor（初步支持）


## 集成概览

SGLang 提供了为可扩展、低延迟大模型部署而打造的新一代推理运行时。其多模态、多 GPU 与流式执行模型，能够以出色的效率同时支撑聊天与智能体推理负载。

SGLang 灵活的架构如今原生提供了量化模型加载的钩子（hook），让 AutoRound 在部署端的潜力得以完全释放。

### **1. 使用 AutoRound 量化**

AutoRound 会自动优化权重舍入，并导出与 SGLang 兼容的量化权重。

#### **1.1 API 用法**

```python
# for LLM
from auto_round import AutoRound
model_id = "meta-llama/Llama-3.2-1B-Instruct"
quant_path = "Llama-3.2-1B-Instruct-autoround-4bit"
# Scheme examples: "W2A16", "W3A16", "W4A16", "W8A16", "NVFP4", "MXFP4" (no real kernels), "GGUF:Q4_K_M", etc.
scheme = "W4A16"
format = "auto_round"
autoround = AutoRound(model_id, scheme=scheme)
autoround.quantize_and_save(quant_path, format=format) # quantize and save
```

#### **1.2 命令行用法**
```bash
auto-round \
    --model Qwen/Qwen2-VL-2B-Instruct \
    --bits 4 \
    --group_size 128 \
    --format "auto_round" \
    --output_dir ./tmp_autoround
```

### **2. 使用 SGLang 部署**

SGLang 直接支持 AutoRound 量化模型（版本 >= v0.5.4.post2）。它兼容 SGLang 支持的各类建模架构，包括常见的 LLM、VLM 与 MoE 模型，同时还支持对 AutoRound 混合位宽量化模型进行推理与评估。

#### **2.1 OpenAI 兼容推理用法**

```python
from sglang.test.doc_patch import launch_server_cmd
from sglang.utils import wait_for_server, print_highlight, terminate_process

# This is equivalent to running the following command in your terminal
# python3 -m sglang.launch_server --model-path Intel/DeepSeek-R1-0528-Qwen3-8B-int4-AutoRound --host 0.0.0.0

server_process, port = launch_server_cmd(
    """
python3 -m sglang.launch_server --model-path Intel/DeepSeek-R1-0528-Qwen3-8B-int4-AutoRound \
 --host 0.0.0.0 --log-level warning
"""
)
wait_for_server(f"http://localhost:{port}")
```

#### **2.2 离线 Engine API 推理用法**


```python
import sglang as sgl

llm = sgl.Engine(model_path="Intel/DeepSeek-R1-0528-Qwen3-8B-int4-AutoRound")

prompts = ["Hello, my name is"]
sampling_params = {"temperature": 0.6, "top_p": 0.95}

outputs = llm.generate(prompts, sampling_params)
for prompt, output in zip(prompts, outputs):
    print(f"Prompt: {prompt}\nGenerated text: {output['text']}")
```

更灵活的配置与部署方式，等你来探索！


## 量化路线图

AutoRound 的量化基准测试结果表明，它在低精度下具备稳健的精度保持能力。下面的结果突出了 AutoRound 在 MXFP4、NVFP4 与混合位宽模型量化上的突出优势和潜力。注意，精度结果取自 *lambada_openai*、*hellaswag*、*piqa*、*winogrande* 和 *mmlu* 任务的平均精度。

作为 AutoRound 路线图的一部分，我们计划在后续版本中继续提升常见模型的 MXFP4 与 NVFP4 精度，以及自动混合位宽量化。

- MXFP4 与 NVFP4 量化。以 RTN（Round-to-nearest，最近舍入）算法为基线，_'alg_ext'_ 选项表示启用了实验性优化算法。

    | mxfp4    | llama3.1-8B-Instruct | Qwen2-7.5-Instruct | Phi4    | Qwen3-32B |
    |:-------------------|:----------------------:|:--------------------:|:---------:|:-----------:|
    | RTN               | 0.6212               | 0.6550            | 0.7167 | 0.6901   |
    | AutoRound         | 0.6686               | 0.6758            | 0.7247 | 0.7211   |
    | AutoRound+alg_ext | 0.6732               | 0.6809            | 0.7225 | 0.7201   |


    | nvfp4   | llama3.1-8B-Instruct | Qwen2-7.5-Instruct | Phi4    | Qwen3-32B |
    |:-------------------|:----------------------:|:--------------------:|:---------:|:-----------:|
    | RTN               | 0.6876              | 0.6906             | 0.7296 | 0.7164      |
    | AutoRound         | 0.6918              | 0.6973             | 0.7306 | 0.7306      |
    | AutoRound+alg_ext | 0.6965              | 0.6989             | 0.7318  | 0.7295     |


- 自动 MXFP4 与 MXFP8 混合位宽量化

    | Average bits     | Llama3.1-8B-I  | Qwen2.5-7B-I   | Qwen3-8B       | Qwen3-32B      |
    |:------------------|:----------------:|:----------------:|:----------------:|:----------------:|
    | **BF16**         | 0.7076 (100%)  | 0.7075 (100%)  | 0.6764 (100%)  | 0.7321 (100%)  |
    | **4-bit**   | 0.6626 (93.6%) | 0.6550 (92.6%) | 0.6316 (93.4%) | 0.6901 (94.3%) |
    | **4.5-bit** | 0.6808 (96.2%) | 0.6776 (95.8%) | 0.6550 (96.8%) | 0.7176 (98.0%) |
    | **5-bit**   | 0.6857 (96.9%) | 0.6823 (96.4%) | 0.6594 (97.5%) | 0.7201 (98.3%) |
    | **6-bit**   | 0.6975 (98.6%) | 0.6970 (98.5%) | 0.6716 (99.3%) | 0.7303 (99.8%) |



## 结论

AutoRound 与 SGLang 的集成标志着高效 AI 模型部署的一个重要里程碑。这次合作打通了精度优化与运行时可扩展性之间的链路，让开发者能够以最小的阻力从量化无缝过渡到实时推理。AutoRound 的符号梯度量化即使在极端压缩比下也能保证高保真度，而 SGLang 的高吞吐量推理引擎则在 CPU、GPU 和多节点集群上充分释放了低比特执行的潜力。

展望未来，我们计划扩展对更多先进量化格式的支持、优化算子效率，并将 AutoRound 量化带入更广泛的多模态与智能体负载。AutoRound 与 SGLang 携手，正在为智能、高效、可扩展的大模型部署树立新的标准。

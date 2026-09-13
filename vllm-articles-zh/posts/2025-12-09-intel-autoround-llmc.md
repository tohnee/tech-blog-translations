---
title: "推进 LLM 低比特量化：AutoRound x LLM Compressor"
title_en: "Advancing Low‑Bit Quantization for LLMs: AutoRound x LLM Compressor"
source: https://vllm.ai/blog/2025-12-09-intel-autoround-llmc
crawled: 2026-09-12
translated: 2026-09-13
---

# 推进 LLM 低比特量化：AutoRound x LLM Compressor

> 原文：[Advancing Low‑Bit Quantization for LLMs: AutoRound x LLM Compressor](https://vllm.ai/blog/2025-12-09-intel-autoround-llmc) · vLLM 博客

Intel Neural Compressor 团队、Red Hat AI 模型优化团队

[#量化](https://vllm.ai/blog/tags/quantization)[#硬件](https://vllm.ai/blog/tags/hardware)[#生态系统](https://vllm.ai/blog/tags/ecosystem)

**在不牺牲精度的前提下，实现更快、更高效的 LLM 服务！**

## TL;DR

我们很高兴地宣布：**[AutoRound](https://aclanthology.org/2024.findings-emnlp.662.pdf)**——Intel 最先进的基于调优的训练后量化（PTQ）算法——现已集成到 **[LLM Compressor](https://github.com/vllm-project/llm-compressor)** 中。这次协作带来：

- 低比特宽度量化下更高的精度
- 轻量级调优（数百步，而非数千步）
- 零额外推理开销
- 与 `compressed-tensors` 无缝兼容，并可在 [vLLM](https://github.com/vllm-project/vllm) 中直接服务
- 流水线化工作流：只需几行代码即可量化并服务模型

更多的量化方案与模型覆盖即将推出——现在就来试用，帮助我们塑造接下来的构建方向。

## 什么是 AutoRound？

**AutoRound** 是一种先进的训练后量化（PTQ）算法，专为大型语言模型（LLM）和视觉语言模型（VLM）设计。它为每个被量化的张量引入三个可训练参数：`V`（舍入偏移/调整量）、`α` 和 `β`（可学习的裁剪范围控制）。通过按顺序处理各解码器层并应用带符号梯度下降，AutoRound 联合优化舍入与裁剪，以最小化逐块（block-wise）的输出重建误差。

核心优势：

- **精度卓越**，尤其是在极低比特宽度下
- **支持多种数据类型：** W4A16、MXFP8、MXFP4、FP8、NVFP4，还有更多在路上
- **混合比特**、逐层精度搜索，实现灵活的精度-效率权衡
- 同时适用于 **LLM** 与 **VLM**

AutoRound 能够产出多种低比特格式的量化模型，旨在加速 **Intel® Xeon® 处理器**、**Intel® Gaudi® AI 加速器**、**Intel® 数据中心 GPU**、**Intel® Arc™ B 系列显卡**以及其他 GPU（例如基于 CUDA 的设备）上的推理。

展望未来，Intel 将为其下一代**数据中心 GPU（代号 Crescent Island）**添加对 FP8、MXFP8 与 MXFP4 格式的原生支持。用 AutoRound 量化的模型将自然地扩展，在整个 Intel AI 硬件组合中利用这些数据类型。这为从算法创新到真实世界部署打通了一条一致的路径。

更多细节请参阅论文 [AutoRound (EMNLP 2024)](https://aclanthology.org/2024.findings-emnlp.662.pdf) 与 GitHub 仓库 [intel/auto-round](https://github.com/intel/auto-round)。

## 为什么要集成到 LLM Compressor？

**LLM Compressor** 已经为量化、剪枝等压缩原语提供了统一的模块化系统。把 AutoRound 集成进这一生态：

- 与现有的 modifier 架构保持一致（例如 `GPTQModifier`）
- 复用顺序校准与逐层加载（layer-onloading）基础设施
- 为未来与更丰富的多 modifier 配方互通奠定基础
- 产出可直接在 vLLM 中服务的量化模型，实现从压缩到部署的干净工作流

## 集成概览

我们通过在 LLM Compressor 中引入新的 `AutoRoundModifier` 完成了第一阶段集成，支持产出可无缝加载进 vLLM 的 `W{n}A16`（例如 W4A16）压缩模型，具体实现见 [PR #1994](https://github.com/vllm-project/llm-compressor/pull/1994)。只需一个直观的配置——指定你的模型与校准数据——你就能快速生成高质量的低比特检查点。这一初始阶段支持量化一系列稠密 LLM，包括 **Llama** 与 **Qwen** 模型家族，并展现出面向实际部署的稳健兼容性。

## 立即试用（快速上手）

### 1. 安装

```
git clone https://github.com/vllm-project/llm-compressor.git
cd llm-compressor
pip install -e .
```

### 2. 加载模型与分词器

```
from transformers import AutoModelForCausalLM, AutoTokenizer
MODEL_ID = "Qwen/Qwen3-8B"
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
```

### 3. 准备校准数据

```
from auto_round.calib_dataset import get_dataset
NUM_CALIBRATION_SAMPLES = 128
MAX_SEQUENCE_LENGTH = 2048
ds = get_dataset(tokenizer=tokenizer,
                 seqlen=MAX_SEQUENCE_LENGTH,
                 nsamples=NUM_CALIBRATION_SAMPLES)
```

### 4. 使用 AutoRound 运行量化

AutoRound 量化可以在多种设备上运行，包括 CPU 和 GPU。量化与服务未必要在同一设备上进行。例如，你可以先在一台带 GPU 的工作站上量化，之后再部署到 AIPC 上。

```
from llmcompressor import oneshot
from llmcompressor.modifiers.autoround import AutoRoundModifier

recipe = AutoRoundModifier(
    targets="Linear",
    scheme="W4A16",
    ignore=["lm_head"],
    iters=200,
)

oneshot(
    model=model,
    dataset=ds,
    recipe=recipe,
    max_seq_length=MAX_SEQUENCE_LENGTH,
    num_calibration_samples=NUM_CALIBRATION_SAMPLES,
    shuffle_calibration_samples=False,
)

SAVE_DIR = MODEL_ID.split("/")[-1] + "-W4A16-G128-AutoRound"
model.save_pretrained(SAVE_DIR, save_compressed=True)
tokenizer.save_pretrained(SAVE_DIR)
```

在实践中，**128 条校准样本 + 约 200 次迭代**通常就能达到稳定收敛。如果你的目标是极低比特或更严格的精度目标，可以增加样本数或迭代次数。

### 5. 在 vLLM 中服务

量化完成后，同一个压缩模型可以在不同硬件上服务，与调优时所用的设备无关。例如，你可以在单张 **Intel® Arc™ Pro B60 GPU** 上服务量化后的 Qwen3‑8B‑W4A16‑G128‑AutoRound 模型：

```
vllm serve Qwen3-8B-W4A16-G128-AutoRound \
    --dtype=bfloat16 \
    --gpu-memory-utilization 0.8 \
    --max-num-batched-tokens 8192
```

注意：请从 PR [#29484](https://github.com/vllm-project/vllm/pull/29484/) 安装 vLLM。在 XPU 上服务时，必须使用 `--enforce-eager` 标志运行 vLLM。

### 6. 评估（示例：使用 `lm_eval` 评测 GSM8K）

```
lm_eval --model vllm \
  --model_args pretrained="./Qwen3-8B-W4A16-G128-AutoRound,max_model_len=8192,max_num_batched_tokens=32768,max_num_seqs=128,gpu_memory_utilization=0.8,dtype=bfloat16,max_gen_toks=2048,enable_prefix_caching=False,enforce_eager=True" \
  --tasks gsm8k \
  --num_fewshot 5 \
  --limit 1000 \
  --batch_size 128

|Tasks|Version|     Filter     |n-shot|  Metric   |   |Value|   |Stderr|
|-----|------:|----------------|-----:|-----------|---|----:|---|-----:|
|gsm8k|      3|flexible-extract|     5|exact_match|↑  |0.911|±  | 0.009|
|     |       |strict-match    |     5|exact_match|↑  |0.911|±  | 0.009|
```

注意：由于非确定性，结果可能出现波动。

## 结论与未来计划

通过这第一次集成，AutoRound 与 LLM Compressor 已经提供了一条实用的、面向生产的低比特 LLM 路径：W4A16 量化已实现端到端支持，工作流配置简单，且支持 Llama、Qwen 等稠密模型。整套配置稳健、精简，已可用于实际部署。

展望未来，我们计划扩展对 FP8、MXFP4、MXFP8 与 NVFP4 等更多方案的支持，增加用于细粒度逐层优化的自动混合比特搜索，并覆盖更多模型家族，包括混合专家（MoE）模型。我们还旨在深化与 LLM Compressor 中其他算法的互操作性，使 AutoRound 能融入更丰富的多 modifier 配方，同时服务社区用例与 Intel 的生产负载。

如果你想影响我们接下来优先支持哪些格式、模型与工作流，请参与 [RFC #1968](https://github.com/vllm-project/llm-compressor/issues/1968) 的讨论，分享你的基准测试或部署需求，也欢迎把反馈带到 Intel 社区，让路线图与真实需求保持一致。

### 致谢

我们要感谢 LLM Compressor 与 vLLM 社区。特别感谢 Kyle Sayers、Dipika Sikka、Brian Dellabetta、Charles Hernandez、Robert Shaw 和 Kunshang Ji，感谢他们对早期提案的宝贵反馈以及对 pull request 的认真评审。

#### 相关 RFC 与 PR

[llm-compressor#1968](https://github.com/vllm-project/llm-compressor/issues/1968), [llm-compressor#1994](https://github.com/vllm-project/llm-compressor/pull/1994), [llm-compressor#2055](https://github.com/vllm-project/llm-compressor/pull/2055), [llm-compressor#2062](https://github.com/vllm-project/llm-compressor/pull/2062), [auto-round#993](https://github.com/intel/auto-round/pull/993), [auto-round#1053](https://github.com/intel/auto-round/pull/1053), [auto-round#1055](https://github.com/intel/auto-round/pull/1055), [auto-round#1072](https://github.com/intel/auto-round/pull/1072),
[vllm#29484](https://github.com/vllm-project/vllm/pull/29484).

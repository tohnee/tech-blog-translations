---
title: "PTPC-FP8：提升 vLLM 在 AMD ROCm 上的性能"
title_en: "PTPC-FP8: Boosting vLLM Performance on AMD ROCm"
source: https://vllm.ai/blog/2025-02-24-ptpc-fp8-rocm
crawled: 2026-09-12
translated: 2026-09-13
---

# PTPC-FP8：提升 vLLM 在 AMD ROCm 上的性能

> 原文：[PTPC-FP8: Boosting vLLM Performance on AMD ROCm](https://vllm.ai/blog/2025-02-24-ptpc-fp8-rocm) · vLLM 博客

作者：AMD 与 Embedded LLM

[#量化](https://vllm.ai/blog/tags/quantization)[#硬件](https://vllm.ai/blog/tags/hardware)

**TL;DR**：vLLM 在 AMD ROCm 上现在拥有更好的 FP8 性能！

- **有什么新内容？** [PTPC-FP8 量化](https://github.com/vllm-project/vllm/pull/12501)现已获得 AMD ROCm 上 vLLM（v0.7.3+）的支持。
- **它为什么好？** 你可以获得与其他 FP8 方法相近的速度，但精度更接近原始（BF16）模型质量。它是 ROCm 上最好的 FP8 选择。
- **如何使用：**
  1. 安装 ROCm。
  2. 获取最新的 vLLM（v0.7.3 或更新版本）。
  3. 在运行 Hugging Face 模型时加上 `--quantization ptpc_fp8` 标志。无需预先量化！

![What is PTPC-FP8](https://vllm.ai/blog-assets/figures/ptpc/PTPC121.png)

什么是 PTPC-FP8

**什么是 PTPC-FP8？** 它是一种对 FP8 权重*和*激活值同时进行量化的方法。它对激活值使用按 token（per-token）缩放、对权重使用按通道（per-channel）缩放，比传统的按张量（per-tensor）FP8 具有更高的精度。

## 引言

大语言模型（LLM）正在彻底改变我们与技术交互的方式，但其巨大的计算需求可能成为一道障碍。如果你能在 AMD GPU 上更快、更高效地运行这些强大的模型，同时不牺牲精度，会怎样？现在可以了！本文介绍一项突破：vLLM 中针对 AMD ROCm 平台优化的 PTPC-FP8 量化。准备好以 FP8 的速度获得接近 BF16 的精度，直接使用 Hugging Face 模型——无需预先量化！我们将展示它的工作原理，对其性能进行基准测试，并帮助你快速上手。

### LLM 量化的挑战与 PTPC-FP8 的解决方案

运行大语言模型的计算成本很高。FP8（8 位浮点数）通过减少内存占用和加速矩阵乘法提供了一个颇具吸引力的解决方案，但传统量化方法在 LLM 上面临一个关键挑战。

#### 离群值问题

LLM 在规模超过一定大小后会产生激活值离群值（outliers）。这些异常大的值带来了显著的量化挑战：

- 使用按张量量化时，大多数值只能获得很少的有效精度位
- 离群值在不同 token 的特定通道中持续出现
- 权重相对均匀、易于量化，而激活值则不然

#### PTPC：一种精度定向的方法

PTPC-FP8（Per-Token-Activation, Per-Channel-Weight FP8，按 token 激活、按通道权重 FP8）基于三个关键观察，使用量身定制的缩放因子来应对这一挑战：

1. 离群值始终出现在相同的通道中
2. 同一 token 内不同通道的幅值差异很大
3. 同一通道在不同 token 之间的幅值相对稳定

这一洞见催生了一种双重粒度的方法：

- **按 token 激活量化（Per-Token Activation Quantization）**：每个输入 token 拥有自己的缩放因子
- **按通道权重量化（Per-Channel Weight Quantization）**：每个权重列拥有唯一的缩放因子

![Per-Token Activation + Per-Channel Weight Quantization](https://vllm.ai/blog-assets/figures/ptpc/PTPC-Diagram.png)

按 token 激活 + 按通道权重量化

#### 理解示意图

图中展示了两种量化方法：

**张量维度（两种方法相同）：**

- **$X$**：输入激活张量（$T\times C_{i}$）
- **$W$**：权重张量（$C_{i}\times C_{o}$）
- **$T$**：token 序列长度
- **$C_{i}/C_{o}$**：输入/输出通道
- **$\ast$**：矩阵乘法

**缩放因子：**

- **顶部（按张量）**：整个张量使用单个标量 $Δ_{X}[1]$ 和 $Δ_{W}[1]$
- **底部（PTPC）**：向量 $Δ_{X}[T\times1]$ 为每个 token 提供一个缩放值，$Δ_{W}[1\times C_{o}]$ 为每个输入通道提供一个缩放值

这种细粒度的缩放方法使 PTPC-FP8 能够在保持 8 位计算的速度和内存优势的同时，获得接近 BF16 的精度。

## 深入解析：PTPC-FP8 在 vLLM 中的工作原理（以及融合内核）

如果不做适当优化，PTPC-FP8 的细粒度缩放可能会拖慢速度。保持速度的关键在于 AMD ROCm 实现的**融合 FP8 rowwise 缩放 GEMM** 操作。

### 挑战：两步法与融合方案

在没有优化的情况下，使用按 token 和按通道缩放的矩阵乘法需要两个代价高昂的步骤：

```
# Naive 2-step approach:
output = torch._scaled_mm(input, weight)       # Step 1: FP8 GEMM
output = output * token_scales * channel_scales  # Step 2: Apply scaling factors
```

这会造成性能瓶颈：

- 将大型中间结果写入内存
- 再把它们读回来执行缩放操作
- 浪费内存带宽和计算周期

### 解决方案：融合

融合方法将矩阵乘法和缩放合并为单一硬件操作：

```
# Optimized fused operation:
output = torch._scaled_mm(input, weight,
                         scale_a=token_scales,
                         scale_b=channel_scales)
```

![Fused GEMM Operation](https://vllm.ai/blog-assets/figures/ptpc/FusedGEMM.svg)

融合 GEMM 操作

### 为什么这很重要

这种融合充分利用了 AMD GPU 的专用硬件（尤其在原生支持 FP8 的 MI300X 上）：

- **内存效率**：缩放在片上内存中完成，然后才写回结果
- **计算效率**：消除了冗余操作
- **性能提升**：我们的测试显示，相比朴素实现可获得高达 2.5× 的加速

融合操作让 PTPC-FP8 在真实部署中切实可行，在保持精度优势的同时，消除了使用更细粒度缩放因子带来的性能损失。

## PTPC-FP8 基准测试：MI300X 上的速度与精度

我们使用 vLLM 在 AMD MI300X GPU（commit `4ea48fb35cf67d61a1c3f18e3981c362e1d8e26f`）上对 PTPC-FP8 进行了广泛的基准测试。以下是我们的发现：

### 1. 吞吐量对比（PTPC-FP8 与按张量 FP8）：

- **模型：** Llama-3.1-70B-Instruct
- **数据集：** SharedGPT
- **GPU：** 1x MI300X
- **结果：** PTPC-FP8 实现了与按张量 FP8 几乎完全相同的吞吐量（甚至略*好*——提升 1.01x）。这表明融合内核完全克服了 PTPC-FP8 更复杂的缩放可能带来的开销。

![Throughput in Reqs/s across various input-output sequence length of Llama-3.1-70B-Instruct](https://vllm.ai/blog-assets/figures/ptpc/PTPCReqs.svg)

Llama-3.1-70B-Instruct 在不同输入-输出序列长度下的吞吐量（Reqs/s）

![Request/s Throughput gain over FP8 per-tensor quantization
across different input token length - output token length](https://vllm.ai/blog-assets/figures/ptpc/PTPCSpeedup.svg)

在不同输入 token 长度 - 输出 token 长度下相对 FP8 按张量量化的 Request/s 吞吐量增益

### 2.1. 精度：困惑度（越低越好）

- **模型：** Llama-3.1-8B-Instruct
- **数据集：** Wikitext
- **配置：** 2× MI300X GPU，张量并行

#### 理解困惑度：预测能力测试

可以把困惑度理解为模型在预测文本时有多"困惑"。就像学生参加测验：

- **困惑度越低 = 预测越好**（模型自信地为正确的下一个词分配高概率）
- **困惑度越高 = 不确定性越大**（模型经常对接下来出现的内容感到意外）

困惑度的微小上升（哪怕 0.1）就可能意味着模型质量出现了有意义的退化，对于经过大量优化的大语言模型尤其如此。

#### 结果：PTPC-FP8 保持接近 BF16 的质量

![bits and byte perplexity](https://vllm.ai/blog-assets/figures/ptpc/PerplexityBits.png)

bits 与 byte 困惑度

![Word Perplexity Comparison](https://vllm.ai/blog-assets/figures/ptpc/Perplexitywords.png)

词困惑度对比

| 精度 | 词困惑度 | 下降百分比 |
| --- | --- | --- |
| BF16（基线） | 9.4281 | - |
| PTPC-FP8 | 9.5093 | 0.86% |
| 标准 FP8 | 9.5124 | 0.89% |

如表和图所示：

1. **PTPC-FP8 优于标准 FP8** 量化（9.5093 对 9.5124）
2. **与 BF16 的差距极小**——相对全精度基线仅有 0.86% 的退化
3. **字节级指标**（bits\_per\_byte 和 byte\_perplexity）呈现出同样的结果模式

**为什么这很重要：** 虽然标准 FP8 已经能提供不错的结果，但 PTPC-FP8 更低的困惑度表明它能更好地保留模型进行准确预测的能力。这对复杂推理和生成任务尤为重要，因为微小的质量下降可能累积为输出质量上的明显差异。

### 2.2. GSM8K 上的精度：数学推理测试\*\*

#### 什么是 GSM8K，它为什么重要

GSM8K 测试模型解答小学数学应用题的能力——这是 LLM 最具挑战性的任务之一。与简单的文本预测不同，这些问题需要：

- 多步推理
- 数值准确性
- 逻辑一致性

这一基准测试是判断量化是否保留了模型推理能力的一个有力指标。

#### 理解结果

我们使用两种方法测量准确率：

- **Flexible-extract**：只要正确答案的数字出现在回答中的任意位置即判定正确
- **Strict-match**：要求答案以预期格式精确给出

![Accuracy Comparison on Llama-3.1-8B](https://vllm.ai/blog-assets/figures/ptpc/GSM8K8B.png)

Llama-3.1-8B 上的准确率对比

**8B 模型结果一览：**

| 方法 | Strict-match 准确率 | 相对 BF16 性能的百分比 |
| --- | --- | --- |
| BF16（基线） | 73.2% | 100% |
| PTPC-FP8 | 70.8% | 96.7% |
| 标准 FP8 | 69.2% | 94.5% |

**70B 模型结果：**

![Accuracy Comparison on Llama-3.1-70B](https://vllm.ai/blog-assets/figures/ptpc/GSM8K70B.png)

Llama-3.1-70B 上的准确率对比

对更大的 70B 模型：

- PTPC-FP8 取得 **87.3%** 的 strict-match 准确率
- 这实际上比 BF16 的 86.3% 还要略*好*
- 在 strict-match 条件下，两者均优于标准 FP8

#### 为什么这些结果重要

1. **推理能力的保留**：数学推理往往是量化后最先退化的能力
2. **PTPC-FP8 在两种模型规模上均始终优于标准 FP8**
3. **接近 BF16 的质量**，同时大幅减少内存并提升性能
4. **规模优势**：量化方法之间的性能差距随模型规模增大而缩小，表明 PTPC-FP8 对大模型尤为有价值

这些结果表明，PTPC-FP8 量化在保留模型执行复杂推理任务能力的同时，带来了 8 位精度的速度与效率优势。

## 快速上手

1. **安装 ROCm：** 确保使用较新的版本。
2. 现在就克隆最新的 vLLM 代码！完成设置，开始探索这一新特性！

```
$ git clone https://github.com/vllm-project/vllm.git
$ cd vllm
$ DOCKER_BUILDKIT=1 docker build -f Dockerfile.rocm -t vllm-rocm .
$ docker run -it \
   --network=host \
   --group-add=video \
   --ipc=host \
   --cap-add=SYS_PTRACE \
   --security-opt seccomp=unconfined \
   --device /dev/kfd \
   --device /dev/dri \
   -v <path/to/model>:/app/model \
   vllm-rocm \
   bash
```

3. **使用 `--quantization ptpc_fp8` 标志运行 vLLM：**

```
VLLM_USE_TRITON_FLASH_ATTN=0 vllm serve <your-model> --max-seq-len-to-capture 16384 --enable-chunked-prefill=False --num-scheduler-steps 15 --max-num-seqs 1024 --quantization ptpc_fp8
```

（将 `<your-model>` 替换为任意 Hugging Face 模型；它会在运行时自动对权重进行量化。）

## 结语：精度与速度的最佳平衡点

AMD ROCm 上 vLLM 的 PTPC-FP8 量化是让强大 LLM 普惠化的重要一步。通过以 FP8 的速度实现接近 BF16 的精度，我们正在打破限制更广泛采用的计算壁垒。这一进步让更广泛的社区——从个人研究者到资源受限的组织——能够在可负担的 AMD 硬件上发挥大语言模型的威力。我们邀请你试用 PTPC-FP8，分享你的经验，为 vLLM 项目做出贡献，与我们共建一个高效、精准的 AI 人人可用的未来。

## 附录

**lm-evaluation-harness 命令：**

```
# Unquantized (Bfloat16)
MODEL=meta-llama/Llama-3.1-8B-Instruct
HIP_VISIBLE_DEVICES=0,1 lm_eval \
  --model vllm \
  --model_args pretrained=$MODEL,add_bos_token=True,tensor_parallel_size=2,kv_cache_dtype=auto,max_model_len=2048,gpu_memory_utilization=0.6 \
  --tasks wikitext --batch_size 16

# Per-Tensor FP8 Quantization
MODEL=meta-llama/Llama-3.1-8B-Instruct
HIP_VISIBLE_DEVICES=0,1 lm_eval \
  --model vllm \
  --model_args pretrained=$MODEL,add_bos_token=True,tensor_parallel_size=2,quantization=fp8,kv_cache_dtype=fp8_e4m3,max_model_len=2048,gpu_memory_utilization=0.6 \
  --tasks wikitext --batch_size 16

# Per-Token-Activation Per-Channel-Weight FP8 Quantization
MODEL=meta-llama/Llama-3.1-8B-Instruct
HIP_VISIBLE_DEVICES=0,1 lm_eval \
  --model vllm \
  --model_args pretrained=$MODEL,add_bos_token=True,tensor_parallel_size=2,quantization=ptpc_fp8,kv_cache_dtype=fp8_e4m3,max_model_len=2048,gpu_memory_utilization=0.6 \
  --tasks wikitext --batch_size 16
```

**lm-evaluation-harness 命令（8B 模型 - 70B 模型请相应调整）：**

```
# FP8 (Per-Tensor)
MODEL=/app/model/Llama-3.1-8B-Instruct/  # Or Llama-3.1-70B-Instruct
lm_eval \
  --model vllm \
  --model_args pretrained=$MODEL,add_bos_token=True,quantization=fp8,kv_cache_dtype=fp8_e4m3 \
  --tasks gsm8k  --num_fewshot 5 --batch_size auto --limit 250

# PTPC FP8
MODEL=/app/model/Llama-3.1-8B-Instruct/  # Or Llama-3.1-70B-Instruct
lm_eval \
  --model vllm \
  --model_args pretrained=$MODEL,add_bos_token=True,quantization=ptpc_fp8,kv_cache_dtype=fp8_e4m3 \
  --tasks gsm8k  --num_fewshot 5 --batch_size auto --limit 250

# BF16
MODEL=/app/model/Llama-3.1-8B-Instruct/  # Or Llama-3.1-70B-Instruct
lm_eval \
  --model vllm \
  --model_args pretrained=$MODEL,add_bos_token=True,kv_cache_dtype=auto \
  --tasks gsm8k  --num_fewshot 5 --batch_size auto --limit 250
```

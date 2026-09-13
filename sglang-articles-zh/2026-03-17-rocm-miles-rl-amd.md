---
title: "Miles 的 ROCm 支持：在 AMD Instinct™ GPU 上进行大规模 RL 后训练"
title_en: "ROCm Support for Miles: Large-Scale RL Post-Training on AMD Instinct™ GPUs"
author: "AMD & Miles Team"
date: "March 17, 2026"
previewImg: /images/blog/rocm_miles_rl/fig_1.png
type: news
source: https://lmsys.org/blog/2026-03-17-rocm-miles-rl-amd/
translated: 2026-09-12
---

# Miles 的 ROCm 支持：在 AMD Instinct™ GPU 上进行大规模 RL 后训练

> 原文：[ROCm Support for Miles: Large-Scale RL Post-Training on AMD Instinct™ GPUs](https://lmsys.org/blog/2026-03-17-rocm-miles-rl-amd/) · LMSYS Blog · AMD & Miles Team

强化学习（RL）已迅速成为现代基础模型开发的核心阶段。尽管大规模预训练依然不可或缺，但当今最强大的模型在很大程度上依赖后训练技术来提升推理、工具调用和多轮交互能力。这些工作流依赖于能够跨多节点 GPU 集群运行的可扩展强化学习基础设施。

我们很高兴地宣布：在 AMD Instinct GPU（包括 MI300/350 级加速器）上，**Miles 强化学习框架现已支持 ROCm**。

本文将介绍 Miles 是什么、为什么 RL 工作负载非常适合 AMD GPU、目前已支持哪些特性，以及如何在 ROCm 上运行端到端的 RL 训练工作流。

## Miles 简介

Miles 是一个开源 RL 框架，专为**语言和多模态模型的大规模后训练**而设计。该框架构建于 SGLang 与 [Slime](https://github.com/THUDM/slime) RL 生态之上，面向生产级 RL 流水线。

Miles 提供以下基础设施：

- 分布式 rollout 生成
- 策略优化（GRPO / PPO）
- on-policy RL 训练循环
- 基于 Ray 的编排
- 与 Megatron-LM 和 SGLang 集成；支持 FSDP 等其他后端

该框架围绕完整的 RL 生命周期设计，能够跨多节点 GPU 集群运行。

Miles 在 RL 社区中获得了广泛采用。随着 ROCm 支持的到来，这些工作流现在可以在 AMD Instinct GPU 上开箱即用地原生运行。

## 为什么 RL 工作负载适合 AMD Instinct GPU

强化学习工作负载与预训练有一个关键区别：
**rollout 生成占据了大部分算力。**

现代 RL 训练可能会将 70–90% 的 GPU 时间花在数千个并行环境中生成长序列上。这使得内存容量和带宽成为至关重要的性能因素。

AMD Instinct MI GPU 提供：

- 大容量 HBM 内存
- 高内存带宽
- 高效的长上下文推理
- 出色的多节点扩展能力

这些特性可以有效缓解 RL 流水线中经典的 rollout 密集型瓶颈。

## ROCm 上的 Miles RL 系统架构

Miles 是一种解耦的 RL 训练架构：将 rollout 生成（SGLang）与模型优化（Megatron）分离，并通过调度器协调二者，以实现可扩展的后训练。

<img src="/images/blog/rocm_miles_rl/fig_1.png" style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;" />
<small><center>图 1 Miles 架构图</center></small>

Miles 将数据生成（rollout）与模型训练分离，并通过中央调度层将二者连接起来。

Miles 采用双平面架构：

- rollout 平面 → 生成训练数据
- 训练平面 → 更新模型权重

调度器负责协调两者之间的交互。整条流水线现已在 ROCm 上完成端到端验证。

## 上手指南：在 AMD GPU 上运行 Miles

Miles 提供了 ROCm 就绪的工作流和预构建容器，让你能以最少的配置运行完整的 RL 流水线。请选择与你的 GPU 代次匹配的容器：

- MI300X：`rlsys/miles:rocm7-MI300-sglang0.5.9-latest`
- MI350X / MI355X：`rlsys/miles:rocm7-MI350-355-sglang0.5.9-latest`

### 启动 Miles ROCm 容器

根据你的硬件设置镜像 tag：

```bash
# MI350X / MI355X:
# export MILES_IMAGE=rlsys/miles:rocm7-MI350-355-sglang0.5.9-latest
# MI300X:
export MILES_IMAGE=rlsys/miles:rocm7-MI300-sglang0.5.9-latest

docker pull $MILES_IMAGE

docker run -it \
  --device /dev/dri --device /dev/kfd \
  --group-add video --cap-add SYS_PTRACE \
  --security-opt seccomp=unconfined --privileged \
  -v $HOME:$HOME --shm-size 128G \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -w $PWD $MILES_IMAGE /bin/bash
```

容器内已预装 SGLang 和 Megatron-LM。

### 安装 Miles 并下载资源

```bash
git clone https://github.com/radixark/miles.git
cd miles
git checkout 90b66b542b38c3b67537bb99a505bb707ebfcf6d
pip install -e .
```

下载示例模型和数据集：

```bash
hf download Qwen/Qwen3-4B --local-dir /root/Qwen3-4B
hf download --repo-type dataset zhuzilin/dapo-math-17k --local-dir /root/dapo-math-17k
hf download --repo-type dataset zhuzilin/aime-2024 --local-dir /root/aime-2024
```

将 Hugging Face 检查点转换为 Megatron 格式：

```bash
source scripts/models/qwen3-4B.sh
MEGATRON_LM_PATH=$(pip list | grep megatron-core | awk '{print $NF}')
PYTHONPATH=${MEGATRON_LM_PATH} python tools/convert_hf_to_torch_dist.py \
  ${MODEL_ARGS[@]} \
  --no-gradient-accumulation-fusion \
  --hf-checkpoint /root/Qwen3-4B \
  --save /root/Qwen3-4B_torch_dist
```

### 启动 RL 训练

```bash
# Prevents Ray from overriding GPU visibility (Miles manages device assignment directly)
export RAY_EXPERIMENTAL_NOSET_HIP_VISIBLE_DEVICES=1
export HIP_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

MILES_DIR=/root MODEL_DIR=/root DATA_DIR=/root \
bash scripts/run-qwen3-4B-amd.sh
```

该脚本会启动完整的 RL 流水线：

- Ray 集群初始化
- SGLang rollout worker
- GRPO 训练循环
- on-policy 的 rollout → 训练 → 更新循环

## 实验与性能

### 智能体任务训练：多轮

多轮智能体正迅速成为现实世界 AI 系统的默认交互形态。大多数实际任务需要多步推理，并借助代码/工具来帮助智能体验证自己的工作，或利用反馈在轨迹中途纠正错误。

在本节中，我们展示一个多轮示例：Qwen2.5-32B 经训练后可使用 Python 解释器求解高中数学风格的问题。

实验配置：

- 模型：pe-nlp/retool-sft-qwen2.5-32b-ins（在 [retool](https://huggingface.co/datasets/JoeYing/ReTool-SFT) 数据集上完成 SFT）
- 技术栈：SGLang + Ray + 基于 Megatron 的训练
- 训练数据集：dapo-math-17k
- 评测集：aime-2024

<img src="/images/blog/rocm_miles_rl/fig_2.png" style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;" />
<small><center>图 2 轮数随训练步数的变化</center></small>

随着训练持续推进，我们观察到每条轨迹的平均轮数不断提升。

<img src="/images/blog/rocm_miles_rl/fig_3.png" style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;" />
<small><center>图 3 评测分数随训练步数的变化</center></small>

从评测曲线来看，模型的数学能力已经相当不错（从 pass@n 指标可见）。评测分数的提升比 pass@n 更为平缓，说明格式/工具调用质量仍在追赶。

<img src="/images/blog/rocm_miles_rl/fig_4.png" style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;" />
<small><center>图 4 原始奖励随训练步数的变化</center></small>

原始奖励随时间改善，这是策略正在学到更好轨迹行为的强烈信号。

### 性能

在单台 8 GPU 的 AMD Instinct MI300X 节点上，我们使用 GRPO 训练了 Qwen3-30B-A3B（32×8 采样、8k 响应长度上限、全局批大小 256），采用 TP4/EP8 加序列并行的 Megatron 设置，且不使用 KL 损失项。

<img src="/images/blog/rocm_miles_rl/fig_5.png" style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;" />
<small><center>图 5. 每步耗时占比（第 4-145 步的均值）。</center></small>

平均每步耗时为 388.50 秒。其中 rollout 生成占比最大（152.79 秒），其次是 actor 训练（95.30 秒）、权重更新（33.85 秒）和 logprob 计算（31.53 秒）。

<img src="/images/blog/rocm_miles_rl/fig_6.png" style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;" />
<small><center>图 6. 左：rollout 吞吐量（tok/GPU/s）；右：训练吞吐量（tok/s）。</center></small>

rollout 吞吐量大部分时间保持在 ~1.1k-1.3k tok/GPU/s 区间。吞吐量在训练过程中逐渐下降；在本次运行中，这一现象与更低的截断率和更短的响应（图 3）同步出现，而 AIME 仍在提升。训练吞吐量则相对稳定，维持在 ~15-16k tok/s 左右。

<img src="/images/blog/rocm_miles_rl/fig_7.png" style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;" />
<small><center>表 1. partial-rollout 训练期间的 AIME 评测检查点</center></small>

AIME 准确率从 0.665（第 19 步）提升至 0.729（第 139 步）。在所示检查点中，AIME 平均准确率为 0.702，pass@16 平均为 0.890，截断率从 0.294 降至 0.156，平均响应长度从 11,718 降至 8,789。

## AMD 上的特性支持路线图

目前，**Miles 的核心功能已在 AMD 上获得完整支持**，包括：

- GRPO 训练
- 模型并行与数据并行
- 动态批处理
- Megatron 与 FSDP 两种后端
- partial rollout（部分 rollout）
- Miles 路由器

这些能力使得端到端的训练与推理服务工作流今天就能在 AMD 平台上运行。

展望未来，我们将持续扩展对更多高价值特性的支持，包括：

- **真正的 on-policy 训练**
- **FP8 流水线优化**
- **Rollout Routing Replay（R3）**
- **INT4 QAT**
- **DeepEP**
- **投机解码**

我们的目标不仅是功能对齐，还包括随着 Miles 路线图的演进而持续改进性能与能力。

## 总结

强化学习如今已成为基础模型开发的核心阶段。借助 Miles 的 ROCm 支持，AMD GPU 用户今天就能在 MI300/350 级集群上运行现代 RL 流水线——包括分布式 rollout 和 GRPO 训练。

这项工作扩展了 PyTorch 生态系统中的硬件可移植性，降低了在 AMD GPU 上开展大规模 RL 实验的门槛。AMD 将持续投入对 Miles 特性的支持。

## 参考资料

- Miles 代码仓库：[https://github.com/radixark/miles](https://github.com/radixark/miles)
- Miles ROCm 教程：[https://github.com/radixark/miles/blob/main/docs/en/platform_support/amd_tutorial.md](https://github.com/radixark/miles/blob/main/docs/en/platform_support/amd_tutorial.md)
- ROCm slime 博客：[https://rocm.blogs.amd.com/artificial-intelligence/slime/README.html](https://rocm.blogs.amd.com/artificial-intelligence/slime/README.html)

### 示例轨迹

<details>
<summary>点击展开示例轨迹</summary>

**问题**

请逐步求解以下数学题。你回答的最后一行应形如 Answer: \boxed{&#36;Answer}，其中 &#36;Answer 是该题的答案。
求各位数字之和为 &#36;12&#36; 的最小四个正整数的和。
请记住把你的答案单独放在一行，位于 "Answer:" 之后。

---

**第 1 轮：**

要解决"求各位数字之和为 12 的最小四个正整数之和"这个问题，我们需要从尽可能小的数开始系统地生成数字，并检查它们的各位数字之和。关键在于从最小的数开始逐个向上排查，直到找到符合条件的前四个数。让我们用代码来自动化这一过程。

&lt;tool_call&gt;
{"name": "execute_python_code", "arguments": {"code": "def digit_sum(n):\n    return sum(int(d) for d in str(n))\n\nnumbers = []\ncurrent = 39  # Start checking from 39 since it's the smallest two-digit number whose digits sum to 12 (3+9=12)\nwhile len(numbers) &lt; 4:\n    if digit_sum(current) == 12:\n        numbers.append(current)\n    current += 1\n\nprint(numbers)"}}
&lt;/tool_call&gt;&lt;|im_end|&gt;

python 输出
[39, 48, 57, 66]

---

**第 2 轮：**

代码生成了前四个各位数字之和为 12 的数，即 39、48、57 和 66。现在，我们需要计算它们的和。

&lt;tool_call&gt;
{"name": "execute_python_code", "code": "sum_numbers = sum([39, 48, 57, 66])\nprint(sum_numbers)"}}
&lt;/tool_call&gt;&lt;|im_end|&gt;

python 输出

Error: Validation failed for input parameters: 1 validation error for Execute\_python\_codeTool
code
  Field required [type=missing, input\_value={}, input\_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/missing

---

**第 3 轮：**

这四个数的和计算得出为 210。这确认了最小的四个数确实是 39、48、57 和 66，它们的和是 210。
因此，答案是 210。

Answer: \boxed{210}&lt;|im_end|&gt;

python 输出
（本轮没有额外的工具输出）

---

_meta: label=210, reward=1.0_

这条轨迹同时展示了当前的能力与当前的差距：
- 模型在第 1 轮正确使用了工具，推导出关键的中间值。
- 在第 2 轮，它仍然犯了工具调用 schema 错误（code 被直接传入，而不是放在 arguments.code 中）。
- 第 3 轮，它未能修正代码，转而直接用自己的数学能力求和并得出最终答案。

经过更多训练后，理想情况下第 3 轮应当能修正代码错误并产出正确的输出。

</details>

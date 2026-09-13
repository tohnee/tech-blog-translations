---
title: "借助 Miles 在 AMD Instinct MI355X GPU 上实现 DeepSeek-V4 Flash RL 训练"
title_en: "Bringing DeepSeek-V4 Flash RL Training to AMD Instinct MI355X GPUs with Miles"
author: "AMD & Miles Team"
date: "July 10, 2026"
previewImg: /images/blog/rocm-miles-dsv4/preview.png
type: news
source: https://lmsys.org/blog/2026-07-10-rocm-miles-dsv4/
translated: 2026-09-12
---

# 借助 Miles 在 AMD Instinct MI355X GPU 上实现 DeepSeek-V4 Flash RL 训练

> 原文：[Bringing DeepSeek-V4 Flash RL Training to AMD Instinct MI355X GPUs with Miles](https://lmsys.org/blog/2026-07-10-rocm-miles-dsv4/) · LMSYS Blog · AMD & Miles Team

DeepSeek-V4 RL 现已在搭载 ROCm™ 的 AMD Instinct™ MI355X GPU 上获得 Miles 支持！RL 要求 SGLang rollout 与 Megatron 训练对同一个策略的实现足够一致，使 token 概率保持对齐——即便 Miles 在反复地把更新后的权重传回在线 rollout 引擎。

DeepSeek-V4 Flash 凭借混合压缩注意力、mHC 残差混合和 MoE 路由让这项工作颇具挑战。我们的 bring-up（工程调通）对齐了 SGLang 与 Megatron 的模型行为，在在线权重更新过程中保留了量化状态，并搭建了端到端的四节点工作流。我们用有界的训练侧与 rollout 侧 log 概率差验证了精度，并在一次延长运行中观察到离线 AIME-2024 基准分数上升、在线奖励同步改善。

## 核心要点

- **DeepSeek-V4 Flash RL 现已能在 AMD Instinct MI355X GPU 上以 Miles 运行。** 我们解决了在 ROCm 上实现端到端执行所需的模型对齐与在线更新问题。
- **四节点验证完成。** 端到端成功运行超过 100 个 optimizer step，训练侧与 rollout 侧 log 概率差保持有界，在线奖励持续提升，离线 AIME-2024 评测分数稳步上升。
- **下一步是性能优化。** 后续工作包括低精度训练、端到端优化以及在更大集群上的扩展。

## 一图看懂 DeepSeek-V4 Flash

DeepSeek-V4 Flash 是一个 2840 亿参数的 MoE 模型，每个 token 激活 130 亿参数。本工作使用的配置包含 43 层 decoder、256 个路由专家（top-6 选择）、四条 mHC 残差流，以及将 128 token 滑窗与压缩长上下文注意力相结合的混合注意力。

C4 层从 4:1 压缩后的 KV 序列中选出 top 512 个条目，而 C128 层则在 128:1 压缩后的序列上做稠密注意力。连同 mHC 与 MoE 路由一起，这些是 SGLang 与 Megatron 必须保持一致实现的主要架构专属路径。

<img src="/images/blog/rocm-miles-dsv4/figure-1-deepseek-v4-block.png" alt="DeepSeek-V4 block 简化示意，展示 mHC 残差混合、混合压缩注意力与 top-6 MoE 路由。" style="display:block; margin: 2.5em auto 0.5em auto; width: 60%; max-width: 900px;" />

<p style="text-align: center; color: #666; font-style: italic;">图 1. DeepSeek-V4 block 的简化示意，展示 mHC 残差混合、混合压缩注意力与 top-6 MoE 路由。</p>

## Miles 技术栈

Miles 负责编排这个异步循环：SGLang 生成候选回复与 rollout log 概率；Megatron 对相同序列打分、计算策略更新并训练 actor；随后 Miles 把更新后的权重传回在线的 SGLang worker。

当前的 FP8 路径在 rollout 侧使用 FP8 的 Hugging Face checkpoint，在 actor 训练侧使用 BF16 的 Megatron torch_dist checkpoint。因此，两个引擎以不同的执行格式表示同一个策略，这使得格式转换、重新打分与在线更新行为都成为正确性边界的一部分。

<img src="/images/blog/rocm-miles-dsv4/figure-2-miles-rl-loop.png" alt="prompt 流向 SGLang rollout；轨迹与 log 概率经由 Miles 流向 Megatron actor；更新后的权重在下一轮 rollout 开始前返回 SGLang。" style="display:block; margin: 2.5em auto 0.5em auto; width: 100%; max-width: 900px;" />

<p style="text-align: center; color: #666; font-style: italic;">图 2. prompt 流向 SGLang rollout；轨迹与 log 概率经由 Miles 流向 Megatron actor；更新后的权重在下一轮 rollout 开始前返回 SGLang。</p>

## 挑战 1：弥合训练与 rollout 之间的 log 概率差距

RL 训练依赖 SGLang 与 Megatron 对同一批生成 token 给出相近的概率。我们搭建了一个 token 完全一致的比较工作流：SGLang 生成一次序列，两个引擎对同样的 token 打分，token 级别的差异就能在代价高昂的多节点验证之前暴露模型层面的不一致。

这一比较定位到两条 DeepSeek-V4 专属路径上的差异：early 层的 hash 路由 MoE 与 mHC 残差混合。我们将 Megatron 的 hash 路由行为与 SGLang 对齐，并修正了 Megatron 侧的 mHC 后置混合（post-mix），使两个引擎保持相同的模型语义。这些针对性改动让 rollout 与训练在数值上更加接近。

## 挑战 2：在线更新中保留量化语义

在 RL 中，rollout 服务端要在不重启的情况下反复接收更新后的策略权重。对量化模型而言，传输成功并不够：打包后的权重、scale 张量以及依赖量化的运行时状态都必须保持其原本的含义。

对于 FP4 与 E8M0 张量，AMD 让更新路径具备了数据类型感知能力，避免了更新后张量被错误解读进而产生无效生成的问题。对于 FP8，Miles 已经定义了更新后的生命周期；AMD 在 ROCm 技术栈中补上了缺失的 SGLang 接口，让 Miles 能在 rollout 恢复之前完成所需的量化处理。

关键教训很简单：在线更新必须恢复模型的量化状态，而不只是复制它的字节。

## 挑战 3：在 ROCm 上找到稳定的多节点并行策略

把 DeepSeek-V4 Flash RL 扩展到多个 AMD Instinct MI355X 节点的过程中，暴露出两个相互耦合的调通难题：为 4K 上下文下的 2840 亿参数 MoE 选出合适的模型并行策略，以及保持多节点集合通信的稳定。二者相互关联：更重的张量并行会降低单 GPU 内存占用，但会增加集合通信流量；而一些早期的多节点配置会在 RCCL 集合通信内部卡住——例如某个张量并行 all-reduce 或专家 all-to-all 迟迟未完成，被通信看门狗捕获，进而中止了整个运行。

我们最终收敛到一个内存可行且稳定的布局：在四个八卡节点上采用张量并行 1、流水线并行 4、专家并行 4，并配合激活重计算、优化器状态卸载到主机内存，以及有界的单 GPU token 预算。把并行方式从张量并行 all-reduce 转向流水线并行与专家并行，再加上调优过的 RCCL 传输设置，使运行得以端到端连续进行超过 100 个 optimizer step 而没有再出现集合通信卡顿。建立起这个稳定的工作点，是后续更长验证的前提。

## 在 AMD Instinct MI355X GPU 上进行四节点验证

我们在四个八卡 AMD Instinct MI355X 节点上验证了 FP8 路径：两个节点用于 SGLang rollout，两个节点用于 Megatron actor 训练。Miles 在长上下文数学负载（4K 上下文的 DAPO-Math-17K）上协调 GRPO 风格的训练、奖励收集以及反复的在线权重更新，模型并行配置为张量并行 1 / 流水线并行 4 / 专家并行 4。每十步，我们在 AIME-2024 上跑一次离线评测，每题 8 个样本。rollout 模型使用 FP8，actor 则以 BF16 训练。

### 正确性与在线奖励

一个关键的正确性检查是：rollout 与训练是否对同样的生成 token 给出相近的概率。在记录的各步中，log 概率绝对差的均值约为 0.09。如图 3 所示，在超过 100 步和多次权重更新的过程中，该差值始终保持有界，既没有持续向上漂移，也没有在更新后出现跳升。这是一个令人鼓舞的调通阶段结果，而非最终阈值。

<img src="/images/blog/rocm-miles-dsv4/figure-3-logprob-diff.png" alt="前 100 个训练步骤内训练侧与 rollout 侧的 log 概率绝对差。" style="display:block; margin: 2.5em auto 0.5em auto; width: 100%; max-width: 900px;" />

<p style="text-align: center; color: #666; font-style: italic;">图 3. 前 100 个训练步骤内训练侧与 rollout 侧的 log 概率绝对差。</p>

除了 log 概率保持有界一致之外，在线奖励在训练过程中也有所提升。在一次延长运行中，在线原始奖励（raw reward）呈现出明显的上升趋势，而非保持平稳：其均值从运行的前三分之一到后三分之一持续上升（图 4）。这表明 actor 在持续的 GRPO 训练和反复在线权重更新下确实在进步，而不只是维持奖励水平。

<img src="/images/blog/rocm-miles-dsv4/figure-4-online-raw-reward.png" alt="100 个训练步骤内的在线原始奖励，含逐步数值、移动平均与线性拟合。" style="display:block; margin: 2.5em auto 0.5em auto; width: 100%; max-width: 900px;" />

<p style="text-align: center; color: #666; font-style: italic;">图 4. 100 个训练步骤内的在线原始奖励（含逐步数值、移动平均与线性拟合）。奖励在整个运行中上升，线性拟合斜率为正。</p>

### 在 AIME-2024 上的离线评测

在线通过率是在训练负载上测量的，会受到动态采样的偏置影响，因此我们每十步还会运行一次留出的离线基准——AIME-2024，每题 8 个样本。这才是对模型质量的诚实度量。在前 100 步中，离线 AIME pass@1 从 0.39 提升到 0.49，pass@8 从 0.53 提升到 0.67，而在 4,096 token 上限处的回复截断比例从 60% 降到 55%。单次采样精度与多样本覆盖同步提升，说明 GRPO 带来了真实的能力增益，而不只是对已有解的锐化。在只有 30 道题的基准上，单次评测的数值噪声很大，因此真正的信号是趋势，而不是任何单个数据点。

<img src="/images/blog/rocm-miles-dsv4/figure-5-aime-eval.png" alt="前 100 个 RL 训练步骤内的离线 AIME-2024 pass@1/2/4/8。" style="display:block; margin: 2.5em auto 0.5em auto; width: 80%; max-width: 900px;" />

<p style="text-align: center; color: #666; font-style: italic;">图 5. 前 100 个 RL 训练步骤内的离线 AIME-2024 pass@1/2/4/8（每 10 步评测一次，每题 8 个样本）。单次精度（pass@1）与覆盖度（pass@8）均呈上升趋势。</p>

## 我们的经验

**离线基准评测才是诚实的信号。** 训练负载上的在线通过率受动态采样与过采样的偏置影响；每十步一次的留出 AIME-2024 评测给出了可信的模型质量度量。我们建议每次 RL 运行都搭配周期性离线评测。

**RL 同时提升了精度与覆盖度。** 100 步内，离线 AIME pass@1 从 0.39 升至 0.49，pass@8 从 0.53 升至 0.67。pass@1 与 pass@k 同时上升，说明策略获得了新能力，而不只是围绕已有解做锐化。

**跨引擎一致性在长运行中保持稳定。** 训练侧与 rollout 侧的 log 概率差在 100 多步和多次权重更新中始终有界，证明调通阶段建立的对齐在远超初始验证窗口之后依然有效。

**回复截断是绝对评测分数的主要天花板。** 约 55-60% 的 AIME 回复触及 4,096 token 的生成长度上限；提高评测的回复长度预算是提升绝对精度杠杆最大的手段。

**看趋势，不要看单步。** 逐步在线奖励与每次评测的通过率噪声都很大（在线奖励在相邻步之间波动于 0.36-0.77）；移动平均与周期性离线评测才是可靠的进展信号。

## 后续路径

- **启用 FP8 actor 训练。** 将 Megatron actor 从 BF16 扩展到 FP8，并评估其对训练-rollout 对齐与训练质量的影响。
- **性能剖析与差距分析。** 找出端到端 RL 流水线中最大的性能差距，并优先处理影响最大的瓶颈。
- **性能优化。** 提升 rollout 吞吐量、训练效率，以及 rollout 与 actor 执行之间的重叠度。
- **扩展。** 在更大的集群上评估吞吐量、效率与正确性，然后调优分布式执行以维持扩展效率。

## 启动命令

实验使用外部 Ray 集群和单条启动命令，在 ROCm 容器内运行。

Docker 镜像：`rlsys/miles:rocm7.2-mi35x-dsv4`

关键设置如下所示；完整的 RCCL transport 与 flight-recorder 环境变量在启动脚本中设置。

```bash
# 1) Start the Ray cluster (one head + three workers), inside the ROCm container
# head node:
ray start --head --node-ip-address=$HEAD_IP --port=6379 --num-gpus=8
# each worker node:
ray start --address=$HEAD_IP:6379 --node-ip-address=$WORKER_IP --num-gpus=8

# 2) Launch DeepSeek-V4 Flash RL from the head node
export MASTER_ADDR=xxx
export MILES_SCRIPT_EXTERNAL_RAY=1
export RAY_ADDRESS=xxx
export PYTHONUNBUFFERED=1

export NCCL_SOCKET_IFNAME=xxx
export GLOO_SOCKET_IFNAME=xxx
export TP_SOCKET_IFNAME=xxx
export NCCL_IB_HCA=xxx
export NCCL_IB_GID_INDEX=1

RUN_ID=dsv4-fp8-4node-2roll-tp1-pp4-ep4-$(date +%Y%m%d_%H%M%S)
LOG=/workspace/miles/${RUN_ID}.log

/opt/venv/bin/python3 scripts/amd/run_deepseek_v4.py train \
  --run-id "${RUN_ID}" \
  --mode normal \
  --enable-eval \
  --num-nodes 4 \
  --actor-num-nodes 2 \
  --rollout-num-nodes 2 \
  --num-rollout 200 \
  --num-steps-per-rollout 1 \
  --rollout-batch-size 32 \
  --n-samples-per-prompt 8 \
  --context-length 16384 \
  --rollout-max-response-len 4096 \
  --max-tokens-per-gpu 8192 \
  --sglang-max-running-requests 48 \
  --sglang-max-total-tokens 524288 \
  --tensor-model-parallel-size 1 \
  --pipeline-model-parallel-size 4 \
  --decoder-last-pipeline-num-layers 10 \
  --context-parallel-size 1 \
  --expert-model-parallel-size 4 \
  --expert-tensor-parallel-size 1 \
  --extra-args '--wandb-team xxx --use-tis' \
  --extra-env-vars 'TORCH_NCCL_DUMP_ON_TIMEOUT=1 TORCH_NCCL_TRACE_BUFFER_SIZE=200000
TORCH_FR_BUFFER_SIZE=200000 TORCH_NCCL_DESYNC_DEBUG=1 TORCH_NCCL_ASYNC_ERROR_HANDLING=1
TORCH_NCCL_DEBUG_INFO_TEMP_FILE=/workspace/miles/nccl_fr_trace_ GPU_MAX_HW_QUEUES=2
NCCL_P2P_NET_CHUNKSIZE=262144' \
  2>&1 | tee "${LOG}"
```

## 总结

我们通过让 SGLang rollout 与 Megatron 训练的模型行为保持一致、并在在线权重更新中保留量化状态，在 ROCm 上打通了端到端的 DeepSeek-V4 Flash RL 训练工作流。

在四节点 AMD Instinct MI355X 验证中，Miles 在超过 100 个 optimizer step 里协调了 FP8 rollout、BF16 actor 训练、奖励收集与反复的策略更新。训练侧与 rollout 侧的 log 概率差全程保持有界，在线奖励持续提升，离线 AIME-2024 基准分数从 pass@1 0.39 升至 0.49（pass@8 从 0.53 升至 0.67）。接下来，我们将启用 FP8 actor 训练，推进性能优化，并在更大规模上评估该工作流。

## 致谢

本工作建立在 SGLang 与 Miles 社区对 DeepSeek-V4 的支持之上。我们感谢与 AMD 合作的 Miles 团队，以及 Megatron、AITER、Triton、TileLang、Transformer Engine 和 ROCm 的贡献者——他们的软件构成了这套端到端技术栈。

**AMD contributors:** Xinyu Kang, Liz Li, Yuankai Chen, Zhiyao Jiang, Kailesh Gogineni, Yao Fu, Wen Xie, Gowtham Ramesh, Cheng Yao, Xiaobo Chen, Shekhar Pandey, Sree Rohith Pulipaka, Wen Chen, Yuzhen Zhou, Xinyu Jiang, Hai Xiao, Andy Luo, Zhenyu Gu.

**Miles contributors:** Yusheng Su, Jiajun Li, Banghua Zhu, Yueming Yuan, Mao Cheng, Zhichen Zeng, Shi Don, Yanbin Jiang, Ying Sheng, and miles team

## 附录

### ROCm 运行时与 kernel 路径图

对于对跨引擎一致性与在线更新影响最直接的模型组件，本次报告的运行使用了以下路径。

| 模型组件 | 所选运行时路径 | 为何重要 |
|---|---|---|
| mHC 残差混合 | **Rollout:** AITER mHC pre/post。<br/>**Training:** TileKernels pre；显式 PyTorch/HIP post-mix。 | 让残差流的映射在引擎之间保持可见、可比较。 |
| 混合注意力 | **Rollout:** ROCm 融合 MLA 解码；Triton 滑窗准备；融合压缩器与分页压缩器路径；TileLang indexer。<br/>**Training:** Miles DeepSeek-V4 BF16 注意力。 | 由不同执行栈分别覆盖局部注意力与压缩注意力。 |
| MoE 与路由 | **Rollout:** Triton FP8 MoE；融合 hash top-k。<br/>**Training:** Megatron MoE 与 router 路径。 | 要求两侧具备相同的确定性 hash 路由语义。 |
| 在线权重更新 | **Rollout:** 分布式权重更新加 SGLang post_process_weights。<br/>**Training:** Miles 从 BF16 actor 广播更新。 | 在生成恢复之前重建依赖量化的运行时状态。 |

<p style="text-align: center; color: #666; font-style: italic;">表 1. 本报告的 ROCm 配置所使用的运行时路径。</p>

启动脚本将所选后端显式化，同时以 Docker 范围内的补丁移除了相关 Megatron 与 Transformer Engine 路径中残留的仅限 CUDA 的假设。这使经过测试的配置保持可复现、可审阅。

---
title: "stepfun-ai/Step-5-Preview"
title_en: "stepfun-ai/Step-5-Preview"
source: https://github.com/stepfun-ai/Step-5-Preview/blob/main/README.md
crawled: 2026-10-16
translated: 2026-10-16
---

<h1 align="center">
  <img src="assets/stepfun-logo.png" alt="StepFun logo" width="40" align="top">
  Step 5 Preview
</h1>

<p align="center">
  <a href="https://huggingface.co/stepfun-ai/Step-5-Preview"><img src="https://img.shields.io/badge/Hugging%20Face-FP8-FFD21E" alt="Hugging Face FP8"></a>
  <a href="https://huggingface.co/stepfun-ai/Step-5-Preview-BF16"><img src="https://img.shields.io/badge/Hugging%20Face-BF16-FFD21E" alt="Hugging Face BF16"></a>
  <a href="https://modelscope.ai/models/stepfun-ai/Step-5-Preview"><img src="https://img.shields.io/badge/ModelScope-624AFF" alt="ModelScope"></a>
</p>

<p align="center">
  <a href="https://www.stepfun.com/step-5-preview"><img src="https://img.shields.io/badge/Model%20Page-00BFA5" alt="Step 5 Preview Model Page"></a>
  <a href="https://platform.stepfun.ai/blog/inside-step-5-preview"><img src="https://img.shields.io/badge/Tech%20Blog-0284C7" alt="Step 5 Preview Tech Blog"></a>
  <a href="https://platform.stepfun.ai/docs/en/guides/models/step-5-preview"><img src="https://img.shields.io/badge/Documentation-2563EB" alt="Developer Documentation"></a>
  <a href="https://platform.stepfun.ai/"><img src="https://img.shields.io/badge/API%20Platform-7C3AED" alt="StepFun API Platform"></a>
</p>

## 简介

Step 5 Preview 是 StepFun 面向智能体工作的旗舰模型。它在软件工程和专业知识工作中具备前沿水平的性能，在金融领域尤为出色。

Step 5 Preview 是一个稀疏混合专家（MoE）模型，总参数量为 600B，激活参数量为 27B。它支持最高 100 万 token 的上下文，并接受文本、图像和视频输入，可在复杂任务中实现持续推理与工具使用。

### 目录

- [关键能力](#key-capabilities)
- [模型规格](#model-specifications)
- [性能](#performance)
- [部署](#deployment)
    - [vLLM](#vllm)
    - [Transformers](#transformers)
    - [SGLang](#sglang)
    - [发送请求](#send-a-request)
- [资源](#resources)
- [许可证](#license)

## 关键能力

### 软件工程

Step 5 Preview 支持仓库级软件工程、前端与可视化开发，以及设备端编程。它能够在大型代码库中导航、协调跨文件的修改、运行并验证代码，并对结果进行迭代。

### 长时程智能体执行

Step 5 Preview 能够完成需要反复调用工具、执行、验证与修订的任务，并在整个工作流程中利用长上下文信息。

### 专业知识工作

该模型将研究、多模态理解与工具使用相结合，分析长文档、图表、截图、图像和视频，并生成结构化的报告与分析。

### 聚焦金融

Step 5 Preview 在将定量推理与金融数据及佐证文档分析相结合的金融任务中表现尤为出色。

## 模型规格

| 规格 | Step 5 Preview |
| --- | --- |
| 架构 | 稀疏混合专家（MoE） |
| 总参数量 | 600B |
| 激活参数量 | 27B |
| 上下文窗口 | 最高 1M token |
| 最大输出 | 最高 1M token |
| 输入 | 文本、图像 |
| 输出 | 文本 |

## 性能

以下结果概述了 Step 5 Preview 在编程、智能体任务、专业知识工作和金融方面的表现。

<p align="center">
  <img src="assets/benchmark-overview.png" alt="Step 5 Preview benchmark results" width="100%">
</p>

**评估说明**

- 推荐的推理设置：`temperature=1.0`、`top_p=0.95`、`top_k=0`。
- 上文展示的 Step 5 Preview 结果均使用 **High** 推理设置。
- GDPval-AA v2.1 分数基于 [Artificial Analysis](https://artificialanalysis.ai/) 截至 2026 年 9 月 20 日的结果。
- DeepSWE v1.1 评估使用 [SWE-agent](https://github.com/SWE-agent/SWE-agent) 评估框架，设置 `temperature=1.0` 与 `top_p=0.95`。

关于评估背景、方法论和详细案例研究，请参阅 [Step 5 Preview 模型页面](https://www.stepfun.com/step-5-preview)。

## 部署

Step 5 Preview 可以通过 vLLM 或 SGLang 以 OpenAI 兼容 API 的形式提供服务，也可以使用独立的 Transformers 实现进行离线生成。下面的示例涵盖 FP8 和 BF16 检查点。

请使用包含 Step 5 Preview 支持的框架版本，其中包括服务命令中用到的推理（reasoning）、工具调用和投机解码（speculative decoding）功能。

### 部署配置

| 框架 | 精度 | 硬件 | 并行方式 | 接口 |
| --- | --- | --- | --- | --- |
| vLLM | FP8 | 单个 B300 节点，4 张 GPU | TP4、TEP4 或 DEP4 | OpenAI 兼容 API |
| vLLM | FP8 | 单个 H200 节点，8 张 GPU | TP8、TEP8 或 DEP8 | OpenAI 兼容 API |
| vLLM | BF16 | 单个 B300 节点，8 张 GPU | TP8、TEP8 或 DEP8 | OpenAI 兼容 API |
| vLLM | BF16 | 两个 H200 节点，16 张 GPU | TP16、TEP16 或 DEP16 | OpenAI 兼容 API |
| Transformers | FP8 | 单个 H200 节点，8 张 GPU | TP8 / EP8 | 离线生成 |
| Transformers | BF16 | 两个 H200 节点，16 张 GPU | TP16 / EP16 | 离线生成（参见下方验证说明） |
| SGLang | FP8 | 单个 B300 节点，4 张 GPU | TP4 / EP4 | OpenAI 兼容 API |
| SGLang | FP8 | 单个 H200 节点，8 张 GPU | TP8 / EP8 | OpenAI 兼容 API |

DP、TP 和 EP 分别指数据并行、张量并行和专家并行。TEP 结合了张量并行与专家并行；DEP 结合了数据并行与专家并行。这些示例配置是针对下文的部署场景设计的。实际的内存需求、可用上下文长度和并发数会随检查点、推理框架和 KV cache 分配而变化。

### vLLM

以下示例通过端口 `18000` 上的 OpenAI 兼容 API 提供 Step 5 Preview 服务，并以 `step5` 作为请求中使用的模型名称。

#### 环境搭建

拉取 Step 5 Preview 镜像，并启动一个可访问 GPU 的交互式容器：

```bash
docker pull vllm/vllm-openai:step-5-preview

docker run --rm -it \
    --gpus all \
    --ipc=host \
    --network=host \
    --volume "$HOME/.cache/huggingface:/root/.cache/huggingface" \
    --entrypoint /bin/bash \
    vllm/vllm-openai:step-5-preview
```

在容器内运行下方的服务启动命令。如果检查点需要身份验证，请在启动服务器前先运行 `hf auth login` 登录。

#### FP8：单节点 4 张 B300 GPU

对于配备四张 B300 GPU 的单节点，请从以下并行配置中选择一种：

| 模式 | 张量并行 | 数据并行 | 专家并行 |
| :---: | :---: | :---: | :---: |
| TP4 | 4 | 1 | 禁用 |
| TEP4 | 4 | 1 | 4 |
| DEP4 | 1 | 4 | 4 |

确保四张 GPU 全部可见，然后运行所选配置对应的命令：

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
```

在 B300（Blackwell）上，TEP4 和 DEP4 命令会通过 `--moe-backend deep_gemm_mega_moe` 启用 MegaMoE。TP4 命令使用默认的 MoE 后端，因为 MegaMoE 需要专家并行。

##### TP4：张量并行

```bash
vllm serve stepfun-ai/Step-5-Preview \
    --host 0.0.0.0 \
    --port 18000 \
    --served-model-name "step5" \
    --tensor-parallel-size 4 \
    --data-parallel-backend mp \
    --distributed-executor-backend mp \
    --disable-custom-all-reduce \
    --max-model-len 1048576 \
    --max-num-batched-tokens 16384 \
    --max-num-seqs 64 \
    --gpu-memory-utilization 0.85 \
    --enable-prefix-caching \
    --spec-method mtp \
    --spec-tokens 3 \
    --reasoning-parser step5 \
    --enable-auto-tool-choice \
    --tool-call-parser step5
```

##### TEP4：张量并行与专家并行

```bash
vllm serve stepfun-ai/Step-5-Preview \
    --host 0.0.0.0 \
    --port 18000 \
    --served-model-name "step5" \
    --tensor-parallel-size 4 \
    --enable-expert-parallel \
    --moe-backend deep_gemm_mega_moe \
    --data-parallel-backend mp \
    --distributed-executor-backend mp \
    --disable-custom-all-reduce \
    --max-model-len 1048576 \
    --max-num-batched-tokens 16384 \
    --max-num-seqs 64 \
    --gpu-memory-utilization 0.85 \
    --enable-prefix-caching \
    --spec-method mtp \
    --spec-tokens 3 \
    --reasoning-parser step5 \
    --enable-auto-tool-choice \
    --tool-call-parser step5
```

##### DEP4：数据并行与专家并行

```bash
vllm serve stepfun-ai/Step-5-Preview \
    --host 0.0.0.0 \
    --port 18000 \
    --served-model-name "step5" \
    --tensor-parallel-size 1 \
    --data-parallel-size 4 \
    --enable-expert-parallel \
    --moe-backend deep_gemm_mega_moe \
    --data-parallel-backend mp \
    --distributed-executor-backend mp \
    --disable-custom-all-reduce \
    --max-model-len 1048576 \
    --max-num-batched-tokens 16384 \
    --max-num-seqs 64 \
    --gpu-memory-utilization 0.85 \
    --enable-prefix-caching \
    --spec-method mtp \
    --spec-tokens 3 \
    --reasoning-parser step5 \
    --enable-auto-tool-choice \
    --tool-call-parser step5
```

##### H200 上的 FP8

对于配备八张 H200 GPU 的单节点，请在上述 B300 命令的基础上做如下调整：

1. 设置 `CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7`。
2. 对于 TP8 或 TEP8，设置 `--tensor-parallel-size 8`。对于 DEP8，保留 `--tensor-parallel-size 1` 并设置 `--data-parallel-size 8`。
3. 对于 TEP8 或 DEP8，保留 `--enable-expert-parallel` 并移除 `--moe-backend deep_gemm_mega_moe`；H200（Hopper）使用默认的 MoE 后端。

TP 和 TEP 使用 DP=1；DEP 使用 TP=1。在所有配置中，`--max-num-seqs` 均按每个 DP rank 生效。1M token 的上下文上限涵盖输入与输出的总和。如果 KV cache 内存不足，请调低 `--max-model-len` 或并发数。

#### BF16

BF16 部署需要 BF16 检查点。在 FP8 检查点上设置 `--dtype bfloat16` 并不会将其量化权重转换为 BF16。

将 BF16 检查点目录挂载到容器内的相同路径下，然后将 `MODEL` 设置为该路径：

```bash
export MODEL="<STEP5_BF16_MODEL_PATH>"
```

根据你的硬件选择一种配置：

| 硬件 | BF16 布局 | MoE 后端 |
| :---: | :---: | :---: |
| 8 张 B300 GPU | TP8、TEP8 或 DEP8 | TEP/DEP 使用 MegaMoE；TP 使用默认后端 |
| 2 × 8 张 H200 GPU | TP16、TEP16 或 DEP16 | 默认后端 |

这些配置为加载 BF16 权重提供了起点。它们并不保证有足够的内存处理 1M token 的请求；KV cache 和运行时缓冲区同样需要占用 GPU 显存。

##### B300：单节点 8 张 GPU

在容器内设置 `CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7`。以 [TP4 命令](#tp4-tensor-parallelism)为起点，将 `stepfun-ai/Step-5-Preview` 替换为 `"$MODEL"`，并将 `--tensor-parallel-size 4` 替换为以下任一参数组合：

| 模式 | 并行参数 |
| :---: | :--- |
| TP8 | `--tensor-parallel-size 8` |
| TEP8 | `--tensor-parallel-size 8 --enable-expert-parallel --moe-backend deep_gemm_mega_moe` |
| DEP8 | `--tensor-parallel-size 1 --data-parallel-size 8 --enable-expert-parallel --moe-backend deep_gemm_mega_moe` |

保留其余服务参数，包括 `--served-model-name "step5"`、`--reasoning-parser step5` 和 `--tool-call-parser step5`。

##### H200：两节点 16 张 GPU

在两个节点上使用相同的 BF16 检查点路径和容器镜像。将下文中的 `<NODE_0_IP>` 替换为节点 0 的高速网络 IP，且该 IP 可从节点 1 访问。H200 使用默认的 MoE 后端；请省略 `--moe-backend deep_gemm_mega_moe`。

在每个节点上：

1. 将 `MODEL` 设置为挂载的 BF16 检查点路径，并设置 `CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7`。
2. 以 [TP4 命令](#tp4-tensor-parallelism)为起点，将 `stepfun-ai/Step-5-Preview` 替换为 `"$MODEL"`。
3. 从该命令中移除 `--host`、`--port` 和 `--tensor-parallel-size`，然后插入下方对应你的配置和节点的参数块。这些参数块包含的是需要追加到 `vllm serve` 的参数，而不是独立命令。

保留所有其他服务参数，包括 `--data-parallel-backend mp`、`--distributed-executor-backend mp`、模型名称以及两个解析器。每个节点运行一条拼装完整的命令。只有节点 0 对外提供 API，端口为 `18000`。

**TP16 / TEP16**

对于 TP16，使用以下参数。对于 TEP16，还需在两个节点上额外添加 `--enable-expert-parallel`。两种配置均使用 DP=1。

节点 0：

```text
--host 0.0.0.0 \
--port 18000 \
--tensor-parallel-size 16 \
--nnodes 2 \
--node-rank 0 \
--master-addr <NODE_0_IP>
```

节点 1：

```text
--tensor-parallel-size 16 \
--nnodes 2 \
--node-rank 1 \
--master-addr <NODE_0_IP> \
--headless
```

**DEP16**

DEP16 使用 TP=1，并将专家分布到 16 个数据并行 rank 上，每个节点各 8 个 rank。两个节点需使用相同的数据并行地址和 RPC 端口。

节点 0：

```text
--host 0.0.0.0 \
--port 18000 \
--tensor-parallel-size 1 \
--data-parallel-size 16 \
--data-parallel-size-local 8 \
--data-parallel-address <NODE_0_IP> \
--data-parallel-rpc-port 29550 \
--enable-expert-parallel
```

节点 1：

```text
--tensor-parallel-size 1 \
--data-parallel-size 16 \
--data-parallel-size-local 8 \
--data-parallel-start-rank 8 \
--data-parallel-address <NODE_0_IP> \
--data-parallel-rpc-port 29550 \
--enable-expert-parallel \
--headless
```

### Transformers

独立实现会将检查点转换为分片（shard）以供离线生成。安装其依赖后，在 `inference/` 目录下运行以下命令：

```bash
cd inference
```

FP8 和 BF16 请使用各自独立的检查点和输出目录。转换会保留源 dtype，生成过程离线运行，无需 API 服务器。

#### FP8：单节点 H200，8 张 GPU

先对 FP8 检查点做一次转换，然后启动八个本地进程进行 TP8 / EP8 生成：

```bash
export STEP5_FP8_CHECKPOINT="<FP8_CHECKPOINT_DIRECTORY>"
export STEP5_FP8_OUT="<FP8_SHARD_OUTPUT_DIRECTORY>"

python3 convert.py \
  --checkpoint "$STEP5_FP8_CHECKPOINT" \
  --tp-size 8 --ep-size 8 --check-only

python3 convert.py \
  --checkpoint "$STEP5_FP8_CHECKPOINT" \
  --out-dir "$STEP5_FP8_OUT" \
  --tp-size 8 --ep-size 8

torchrun --standalone --nproc-per-node=8 generate.py \
  --tp-dir "$STEP5_FP8_OUT/tp8" --ep-size 8 \
  --prompt "Please introduce tensor parallelism." \
  --max-new-tokens 128
```

#### BF16：两节点 H200，16 张 GPU

对于跨两个节点的 TP16 / EP16 生成，需先将 BF16 检查点转换为 16 个分片。确保生成的 `tp16/` 和 `tokenizer_files/` 目录对两个节点均可访问：

```bash
export STEP5_BF16_CHECKPOINT="<BF16_CHECKPOINT_DIRECTORY>"
export STEP5_BF16_OUT="<BF16_SHARD_OUTPUT_DIRECTORY>"

python3 convert.py \
  --checkpoint "$STEP5_BF16_CHECKPOINT" \
  --tp-size 16 --ep-size 16 --check-only

python3 convert.py \
  --checkpoint "$STEP5_BF16_CHECKPOINT" \
  --out-dir "$STEP5_BF16_OUT" \
  --tp-size 16 --ep-size 16
```

然后在每个节点上运行下面的命令，使用相同的 `MASTER_ADDR`、`MASTER_PORT` 和分片输出路径。在节点 0 上设置 `NODE_RANK=0`，在节点 1 上设置 `NODE_RANK=1`：

```bash
export STEP5_BF16_OUT="<BF16_SHARD_OUTPUT_DIRECTORY>"
export MASTER_ADDR="<NODE_0_REACHABLE_IP_OR_HOSTNAME>"
export MASTER_PORT=29500
export NODE_RANK=0  # Set to 1 on node 1.

torchrun --nnodes=2 --nproc-per-node=8 \
  --node-rank="$NODE_RANK" \
  --master-addr="$MASTER_ADDR" \
  --master-port="$MASTER_PORT" \
  generate.py \
  --tp-dir "$STEP5_BF16_OUT/tp16" --ep-size 16 \
  --prompt "Please introduce tensor parallelism." \
  --max-new-tokens 128
```

这会在两个节点上共启动 16 个进程，与 16 分片检查点和 `--ep-size 16` 相匹配。双节点启动使用共享的会合（rendezvous）地址，而不是 `--standalone`。

**BF16 验证说明：**完整的 BF16 `convert.py → generate.py --tp-dir` 文件分片工作流尚未经过端到端验证。参考实现已验证了检查点名称与形状、BF16 小模型转换、加载与生成，以及全模型的流式权重推理。

### SGLang

#### 环境搭建

拉取 Step 5 Preview 的 SGLang Docker 镜像：

```bash
docker pull lmsysorg/sglang:step-5-preview
```

根据你的硬件使用相应配置启动服务器。如需更多优化配置，包括 MegaMoE、注意力数据并行和 HiCache，请参阅 [Step 5 Preview SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/StepFun/Step-5-Preview)。

#### B300：TP4/EP4，4 张 GPU

此配置对 FP8 路由专家使用 MegaMoE。

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3

python -m sglang.launch_server \
  --trust-remote-code \
  --model-path stepfun-ai/Step-5-Preview \
  --served-model-name step5 \
  --tp 4 \
  --ep-size 4 \
  --moe-runner-backend flashinfer_trtllm \
  --moe-a2a-backend megamoe \
  --attention-backend fa4 \
  --page-size 64 \
  --kv-cache-dtype bfloat16 \
  --mem-fraction-static 0.9 \
  --swa-full-tokens-ratio 0.03 \
  --chunked-prefill-size 16384 \
  --max-running-requests 64 \
  --cuda-graph-backend-prefill breakable \
  --flashinfer-allreduce-fusion-backend trtllm \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --enable-multi-layer-eagle \
  --reasoning-parser step5 \
  --tool-call-parser step5 \
  --host 0.0.0.0 \
  --port 30000
```

#### H200：TP8/EP8，8 张 GPU

适用于采用 Triton MoE 和 FA3 注意力的单节点 H200 服务。

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

python -m sglang.launch_server \
  --trust-remote-code \
  --model-path stepfun-ai/Step-5-Preview \
  --served-model-name step5 \
  --tp 8 \
  --ep-size 8 \
  --moe-runner-backend triton \
  --attention-backend fa3 \
  --page-size 64 \
  --kv-cache-dtype bfloat16 \
  --mem-fraction-static 0.9 \
  --swa-full-tokens-ratio 0.03 \
  --chunked-prefill-size 16384 \
  --max-running-requests 64 \
  --cuda-graph-backend-prefill breakable \
  --flashinfer-allreduce-fusion-backend trtllm \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --enable-multi-layer-eagle \
  --reasoning-parser step5 \
  --tool-call-parser step5 \
  --host 0.0.0.0 \
  --port 30000
```

### 发送请求

服务器就绪后，请使用与你部署方式对应的基础 URL：

| 服务配置 | 服务器主机上的基础 URL |
| --- | --- |
| vLLM FP8 | `http://localhost:18000` |
| vLLM BF16 | `http://localhost:18000`（节点 0） |
| SGLang FP8 | `http://localhost:30000` |

以下示例以 vLLM FP8 为例：

```bash
curl http://127.0.0.1:18000/v1/chat/completions \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "step5",
      "messages": [{"role": "user", "content": "Hello!"}],
      "max_tokens": 4096,
      "stream": true
    }'
```

## 资源

- [Step 5 Preview 模型页面](https://www.stepfun.com/step-5-preview) — 模型概览、评估背景和长时程案例研究。
- [Step 5 Preview 技术博客](https://platform.stepfun.ai/blog/inside-step-5-preview) — 模型架构、训练稳定性、Sparse GQA、智能体数据合成与强化学习。
- [文档](https://platform.stepfun.ai/docs/en/guides/models/step-5-preview) — 官方文档与开发者指南。
- [API 平台](https://platform.stepfun.ai/) — 模型访问与平台服务。
- [StepFun 官网](https://www.stepfun.com/) — 公司信息与模型发布公告。

## 许可证

本模型（包括其权重、参数、配置、分词器、模型专属代码和文档）依据 StepFun Model License 1.0 授权。许可证全文见本仓库中的 [LICENSE](LICENSE) 文件。StepFun Model License 1.0 是一种 Apache-2.0 风格的许可证，并附加了针对模型使用、修改和分发的署名及商业许可条件。

若本仓库中的随附材料（包括示例代码、数据集、第三方组件和其他文档）被单独标注为适用其他许可证，则此类材料依该许可证授权。

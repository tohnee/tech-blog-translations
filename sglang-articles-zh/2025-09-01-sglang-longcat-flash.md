---
title: "LongCat-Flash：使用 SGLang 部署美团的 Agentic 模型"
title_en: "LongCat-Flash: Deploying Meituan's Agentic Model with SGLang"
author: "Meituan LongCat Team"
date: "September 01, 2025"
previewImg: /images/blog/longcat_flash/longcat_sglang.jpg
source: https://lmsys.org/blog/2025-09-01-sglang-longcat-flash/
translated: 2026-09-12
---

# LongCat-Flash：使用 SGLang 部署美团的 Agentic 模型

> 原文：[LongCat-Flash: Deploying Meituan's Agentic Model with SGLang](https://lmsys.org/blog/2025-09-01-sglang-longcat-flash/) · LMSYS Blog · Meituan LongCat Team

### 1. 引言：部署美团的 Agentic 开源 MoE 模型

美团开源的 Agentic 混合专家（MoE）模型 LongCat-Flash 现已在 Hugging Face 上提供：[LongCat-Flash-Chat](https://huggingface.co/meituan-longcat/LongCat-Flash-Chat)。该模型由美团 LongCat 团队发布，具有以下特点：
- 总参数量 560B
- 每 token 激活参数 18.6B–31.3B（平均 27B）
- 512 个 FFN 专家和 256 个零计算专家
- 用于计算-通信重叠的快捷连接结构（ScMoE）
- 多头潜在注意力（MLA）

多项基准测试表明，LongCat-Flash 作为非思考型（non-thinking）基础模型，仅需激活少量参数即可达到与领先主流模型相当的表现，在智能体（agent）任务上尤为出色。此外，得益于面向推理效率的设计与创新，LongCat-Flash 的推理速度显著更快，更适合复杂、耗时的智能体应用。

![benchmark_overview.jpg](/images/blog/longcat_flash/benchmark_overview.jpg)

更多细节请参阅我们的技术报告 [LongCat-Flash-Technical-Report](https://github.com/meituan-longcat/LongCat-Flash-Chat/blob/main/tech_report.pdf)。

### 2. 为什么模型-系统协同设计很重要？

正如技术报告中所述，典型的基于 ReACT 的智能体系统由于多轮对话的特性，对预填充（Prefill）和解码（Decode）速度都提出了极高要求。

**对于预填充**，我们观察到并非模型中的每个 token 都需要同等数量的激活参数。基于这一观察，我们设计了动态激活机制，在保持模型性能的同时将每 token 激活参数控制在 18.6B–31.3B（平均 27B）之间，这对降低预填充计算量至关重要。

**对于解码**，MoE 模型的高稀疏性要求使用大批次（batch）来提升 GEMM（General Matrix Multiply，通用矩阵乘法）的计算强度。虽然大规模专家并行（EP，Expert Parallelism）能释放 HBM 空间以容纳更大的 KV 缓存——从而有效增大批次规模，但通信随之成为瓶颈。计算/通信重叠是性能的关键。DeepSeek V3/SGLang 中的 TBO（Two Batch Overlap，双批次重叠）通过批次间重叠来降低延迟，但在小批次或单请求场景下无法奏效。吞吐量（大批次）与延迟（小批次）本质上是相互冲突的目标，在线应用往往需要在两者之间做权衡。通过模型-系统协同设计，ScMoE 打破了这个权衡，同时优化吞吐量与延迟。ScMoE 的另一个优势是：稠密 FFN 上的节点内张量并行通信（通过 NVLink）可以与节点间专家并行通信（通过 RDMA）完全重叠，从而最大化整体网络利用率。

### 3. 我们的方案：SGLang + PD 分离 + SBO + 大规模专家并行

#### 3.1 PD 分离（PD Disaggregation）

为了让预填充和解码两个阶段可以独立优化，我们采用了 PD 分离（预填充-解码分离）架构。基于 SGLang 的 PD 分离能力，我们开发了具备逐层传输特性的方案，在高 QPS 负载下显著降低了首 token 延迟（TTFT，Time-To-First-Token）。

#### 3.2 单批次重叠（Single Batch Overlap，SBO）

SBO 是一种四阶段流水线执行方式，通过模块级重叠充分释放 LongCat-Flash 的潜力。SBO 与 TBO 的区别在于，它将通信开销隐藏在单个批次内部。在 SBO 中：

- **阶段 1** 必须单独执行，因为 MLA 的输出是后续阶段的输入。
- **阶段 2** 是 all-to-all dispatch 与稠密 FFN 及 Attn 0（QKV 投影）的重叠。这一重叠至关重要，因为通信开销过大，促使我们将注意力计算过程做了拆分。
- **阶段 3** 独立执行 MoE GEMM。该阶段的延迟将受益于大规模 EP 部署策略。
- **阶段 4** 将 Attn 1（核心注意力与输出投影）和稠密 FFN 与 all-to-all combine 相重叠。

这种编排有效缓解了通信开销，确保 LongCat-Flash 高效推理。由于所有重叠都发生在单个批次内部，SBO 能同时提升吞吐量并降低延迟。

#### 3.3 大规模专家并行（Wide Expert Parallelism）

扩大 EP 规模并增大批次会带来更高的通信开销，但借助 SBO，通信可以与稠密路径计算相重叠。在 SBO 中，MoE 计算仍然是暴露在外、未被遮盖的。在到达 MoE 计算的计算瓶颈（compute-bound）区间之前，扩大 EP 规模和批次规模可以缩短 MoE 计算时间。因此，SBO 能够从更宽的 EP 配置中获得性能收益。另外，我们采用 DeepEP 来完成 MoE 的 dispatch 和 combine 通信，与 SGLang 的实现类似。

#### 3.4 其他优化

##### 多步重叠调度器

为了提升 GPU 利用率，SGLang 实现了重叠调度器。然而实验结果显示，LongCat-Flash 前向计算的延迟很低，使得单步预调度策略不足以完全消除调度开销。因此，我们实现了多步重叠调度器，在单次调度迭代中启动多个前向步骤的 kernel。这一方法有效地将 CPU 调度与同步隐藏在 GPU 前向计算过程中，确保 GPU 持续处于占用状态。

##### 多 token 预测（Multi-Token Prediction）

为了获得最佳推理性能，我们采用单个稠密层而非 MoE 层作为 MTP 头。该特性已在 SGLang 中得到支持。由于 LongCat-Flash 的 MTP 非常轻量，将验证 kernel 与草稿前向分开调度会引入显著开销。为缓解这一问题，我们采用了 TVD 融合策略，将目标模型前向（Target forward）、验证（Verification）与草稿前向（Draft forward）融合进单个 CUDA 图（CUDA Graph）。

### 4. 性能

**成本与延迟表现：**
- **吞吐量优化场景**：LongCat-Flash 的理论成本不到同规模（甚至更小规模）模型的 50%。
- **延迟优化场景**：SBO 的批内优化实现了极低的延迟。

**基准测试：**
- **与 DeepSeek V3 相当的吞吐量**：生成速度更胜一筹。
- **吞吐量-延迟均衡**：在 NVIDIA H800 平台上实测，以有竞争力的成本达到 **100 tps**。

| 模型 | Attention | 上下文 | GPU | TGS | TPS/u |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-V3-Profile | BF16 | 4096 | 128 | 2324 | 20 |
| LongCat-Flash | BF16 | 5000 | 128 | 2205 | 68.9 |
| LongCat-Flash | BF16 | 5000 | 128 | 804 | 100.5 |

### 5. 使用 SGLang 部署 LongCat-Flash

我们推荐使用 SGLang 部署 LongCat-Flash。通过与 SGLang 社区的紧密合作，LongCat-Flash 从发布第一天起就获得了 SGLang 支持。由于模型参数量高达 560B，LongCat-Flash 若以 FP8 格式托管模型权重，至少需要 1 个 8xH20-141G 节点；BF16 权重则至少需要 2 个节点共 16 张 H800-80G。详细的启动配置如下。

#### **安装 SGLang**

```Shell
pip install --upgrade pip
pip install uv
uv pip install "sglang[all]>=0.5.2.rc0"
```
#### **单节点部署（8xH20-141G）**

模型可以在单节点上通过张量并行与专家并行的组合进行服务。
```Shell
python3 -m sglang.launch_server \
    --model meituan-longcat/LongCat-Flash-Chat-FP8 \
    --trust-remote-code \
    --attention-backend flashinfer \
    --enable-ep-moe \
    --tp 8
```
#### **多节点部署（16xH800-80G）**

多节点部署采用张量并行与专家并行，更多并行策略计划在未来实现。
请将 `$NODE_RANK` 和 `$MASTER_IP` 替换为你集群中的具体值。
```Shell
python3 -m sglang.launch_server \
    --model meituan-longcat/LongCat-Flash-Chat \
    --trust-remote-code \
    --attention-backend flashinfer \
    --enable-ep-moe \
    --tp 16 \
    --nnodes 2 \
    --node-rank $NODE_RANK \
    --dist-init-addr $MASTER_IP:5000
```
#### **启用多 token 预测（MTP）**

要在 SGLang 中启用 MTP，可以在启动命令中加入以下参数。
```Shell
    --speculative-draft-model-path meituan-longcat/LongCat-Flash-Chat \
    --speculative-algorithm NEXTN \
    --speculative-num-draft-tokens 2 \
    --speculative-num-steps 1 \
    --speculative-eagle-topk 1
```
### 6. 结论

通过利用 SGLang、PD 分离、大规模专家并行和 SBO 等能力，我们为 LongCat-Flash 实现了极低的成本和快速的生成速度。LongCat-Flash 的高效推理也离不开 SGLang 团队、Mooncake 团队、NVIDIA TensorRT-LLM 以及其他开源社区的工作。接下来，我们计划与 SGLang 团队合作，逐步将我们基于 SGLang 的优化回馈上游，进一步支持开源生态。

#### 致谢

我们衷心感谢以下团队与合作者：
- **SGLang 团队与社区：** 感谢他们在 SGLang 框架上的工作。
- **Mooncake 团队**：感谢他们在业内最早开源了 PD 分离架构与 TransferEngine。
- **NVIDIA TensorRT-LLM：** 感谢他们为 Hopper GPU 提供的高效 kernel。
- **美团 LongCat 团队**：感谢我们的模型-系统协同设计。

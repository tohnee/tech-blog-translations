---
title: "在 128 块 H200 GPU 上以 PD 分离与大规模专家并行部署 Kimi K2"
title_en: "Deploying Kimi K2 with PD Disaggregation and Large-Scale Expert Parallelism on 128 H200 GPUs"
author: "The Mooncake Team"
date: "July 20, 2025"
previewImg: /images/blog/k2_large_scale/preview.jpg
source: https://lmsys.org/blog/2025-07-20-k2-large-scale-ep/
translated: 2026-09-12
---

# 在 128 块 H200 GPU 上以 PD 分离与大规模专家并行部署 Kimi K2

> 原文：[Deploying Kimi K2 with PD Disaggregation and Large-Scale Expert Parallelism on 128 H200 GPUs](https://lmsys.org/blog/2025-07-20-k2-large-scale-ep/) · LMSYS Blog · The Mooncake Team


## 1️⃣ 引言：部署最先进的开源 MoE 模型

**Kimi K2 是目前最先进的开源专家混合（MoE）模型。**

它由 Moonshot AI 于 2025 年发布，特性包括：

- **总参数量 1 万亿**
- **每个 token 激活 320 亿参数**
- **384 个专家，动态路由**
- **多头潜在注意力（MLA）**，支持长上下文

Kimi K2 在**前沿知识、数学和编程**方面表现强劲，并针对**智能体（agentic）任务**做了优化——不只是回答问题，还能执行多步操作。

Moonshot AI 开源了两个版本：

- **Kimi-K2-Base**：用于研究和微调的基座模型
- **Kimi-K2-Instruct**：经后训练、面向通用聊天与智能体应用的模型

更多细节请参考 [Kimi K2 官方发布页](https://moonshotai.github.io/Kimi-K2/)。

---

### 为什么大规模部署很重要

鉴于该模型的架构，大规模部署能充分发挥硬件能力并降低成本。

- **更快地服务更多请求：**更高吞吐量、更低延迟、更多并发会话、更短排队。
- **更低的每 token 成本（$/Token）：**打满硬件并摊薄模型加载开销；规模越大效率越高。

然而，万亿参数规模 MoE 模型的大规模部署面临一些独特挑战：

- **MoE 层的计算稀疏性**要求大批量（batch size）才能让矩阵运算变得计算密集。大规模专家并行（EP）将并行策略扩展到更多 GPU 上，聚合来自多个设备的请求，降低单 GPU 内存压力，并腾出 VRAM 容纳更大的 KV 缓存——从而有效增大批量。
- **跨节点**通信耗时巨大，需要优化
- **稀疏专家激活**导致负载不均衡

要在 **128 块 H200 GPU** 上高效部署 Kimi K2，需要对系统设计和部署流程都进行重新思考。

在本博客中，我们将介绍如何用 **OME** 和 **SGLang** 解决这个问题。

---

## 2️⃣ 背景：从 DeepSeek R1 到 Kimi K2

2025 年 5 月，我们发布了[以 PD 分离与大规模 EP 部署 DeepSeek R1](https://lmsys.org/blog/2025-05-05-large-scale-ep/) 一文，其中我们展示了：

- **预填充-解码（PD）分离**，将计算密集型任务与延迟敏感型任务分开
- **大规模专家并行（EP）**，处理跨 96 块 GPU 的 MoE 路由
- 相比 H100 上普通张量并行 **5 倍的吞吐量提升**

与此同时，我们的 [OME 博客](https://lmsys.org/blog/2025-07-08-ome/)介绍了**模型驱动部署**，弥合了以下两类角色之间的运营鸿沟：

- **机器学习工程师**，负责设计复杂的服务策略
- **生产工程师**，需要简单可靠的部署

OME 的核心理念——应该由模型驱动部署，而不是相反——在扩展到 Kimi K2 的 1T 参数架构时同样卓有成效。这次迁移要求把为 DeepSeek 设计的 PD 分离与 EP 方案适配到 Kimi K2 的 384 个专家上，同时保持高性能。

---

## 3️⃣ 我们的方案：OME + SGLang PD 分离 + 大规模专家并行

针对 Kimi K2，我们结合了 **OME** 与 **SGLang** 的优势，构建了一条优化且可扩展的部署流水线。

### 用 OME 实现模型驱动部署

OME（Open Model Engine）通过抽象掉并行、分片、扩缩与运行时配置的复杂性，简化了 Kimi K2 这类先进模型的部署。借助声明式配置模型，生产团队无需手工调优或编写定制脚本，就能部署和管理大模型。

**安装 OME**

使用以下命令直接从 OCI registry 安装 OME：

```bash
# Step 1: Install OME CRDs
helm upgrade --install ome-crd oci://ghcr.io/moirai-internal/charts/ome-crd --namespace ome --create-namespace

# Step 2: Install OME core resources
helm upgrade --install ome oci://ghcr.io/moirai-internal/charts/ome-resources --namespace ome
```

详细的安装说明请参考官方 [OME 安装指南](https://docs.sglang.io/ome/docs/installation/)。

**注册 Kimi K2 模型**
要让 OME 管理 Kimi K2 模型家族，请应用以下 ClusterBaseModel 资源：

```bash
kubectl apply -f https://raw.githubusercontent.com/sgl-project/ome/refs/heads/main/config/models/moonshotai/Kimi-K2-Instruct.yaml
```

注意：你可以下载该 YAML 文件并自定义 path 字段，以指定模型在本地存储的位置。OME 会以优化过的并行方式直接从 Hugging Face 下载模型，并自动校验制品（artifact）校验和以保证完整性。

**安装 Kimi K2 最新版 SGLang 服务运行时（Serving Runtime）**

```bash
kubectl apply -f https://raw.githubusercontent.com/sgl-project/ome/refs/heads/main/config/runtimes/srt/kimi-k2-pd-rt.yaml
```

**部署模型**

模型和运行时注册完成后，使用以下命令部署推理端点：

```bash
kubectl apply -f https://raw.githubusercontent.com/sgl-project/ome/refs/heads/main/config/samples/isvc/moonshotai/kimi-k2-pd.yaml
```

这些声明式资源就位后，OME 会自动处理模型下载、运行时编排和端点供给——为 Kimi K2 模型家族提供可扩展的生产级推理服务。

**与模型交互**

以下命令把本地 8080 端口转发到模型的 80 端口：
```bash
kubectl port-forward -n kimi-k2-instruct service/kimi-k2-instruct 8080:80
```
让该命令在一个终端里保持运行，它会把本地的 http://localhost:8080 路由到 SGLang router。端口转发生效后，在第二个终端里运行：
```bash
curl -s -X POST http://localhost:8080/generate \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer None' \
  -d '{
    "text": "The future of AI is",
    "max_new_tokens": 50,
    "temperature": 0.7
  }'
```

---

### **OME 的优势与 PD + DeepEP + Router 洞见**

OME（Open Model Engine）为部署 Kimi K2 这类大模型提供了一个声明式的、生产可用的框架。它抽象了 GPU 拓扑、分布式配置和运行时调优的复杂性——免去了自定义编排逻辑的需要。只需一个 ClusterServingRuntime 定义，团队就能大规模启动经过优化的多节点推理负载。

该配置展示了一套利用**预填充-解码（PD）分离**与**大规模 EP** 的强大部署方案，可实现：

- 预填充与解码负载的**分离式扩缩**，资源控制相互独立
- 通过 deepep-mode=low_latency 与感知 token 的分发（dispatch）调优实现**低延迟解码**
- 通过 ep-dispatch-algorithm=dynamic 与 enable-eplb 实现**高级专家路由**
- 面向高吞吐 KV 缓存传输的 **RDMA 加速**

整个部署由轻量级的 **SGLang Router** 编排，它提供：

- 通过 label selector 对预填充和解码节点进行**动态服务发现**
- 独立于引擎和解码器负载的**自动扩缩能力**
- **最小权限路由模型**——非常适合安全要求严格的生产环境
- 为分离式服务模式量身定制的**优化负载均衡**

OME 与 SGLang Router 共同构成了大规模、低延迟且易于维护的推理基础设施的坚实基座。

### 预填充-解码分离（PD 分离）

我们将推理拆分为两个独立组件：

| 阶段 | 职责 |
| --- | --- |
| **预填充（Prefill）** | 处理大提示词的摄入（例如 2000 token 的输入）。这一阶段受计算限制（compute-bound），受益于大批量并行。 |
| **解码（Decode）** | 处理自回归生成（例如 100 token 的输出）。这一阶段对延迟敏感，并为高吞吐输出做了优化。 |

预填充与解码作为独立服务部署，各自单独扩缩和优化。

---

### 大规模专家并行（EP）

Kimi K2 每个 token 只激活 **384 个专家**中的一个子集。我们实现了：

- **解码节点上的 96 个冗余专家**，用于均衡 MoE 路由
- **NUMA 感知的 GPU 分组**，在 H200 集群上实现 NVLink 与 PCIe 的最优利用

这一设计将负载不均衡降到最低，确保 128 卡集群上的 GPU 利用率均匀分布。

---

## 4️⃣ 性能：2000 输入、100 输出基准测试

我们在 **128 块 H200 GPU、1P1D（预填充 4 节点、解码 12 节点）**的配置下，用典型的 LLM 推理服务负载对 Kimi K2 进行了基准测试：

| 指标 | 数值 |
| --- | --- |
| **输入长度** | 2000 tokens |
| **输出长度** | 100 tokens |
| **解码批量（Batch Size）** | 480 |

作为示例，我们沿用了 DeepSeek R1 部署博客中相同的基准测试设置。面向智能体场景的更长输出将作为后续工作。

注意：预填充与解码的比例取决于具体负载。我们优先配置了解码节点以最大化 KV 缓存池大小，这对把批量扩展到 480 至关重要。

---

### 集群级性能（128 × H200 GPU）

| 指标 | 数值 |
| --- | --- |
| **预填充吞吐量** | **224k tokens/秒（4 个 P 节点）** |
| **解码吞吐量** | **288k tokens/秒（12 个 D 节点）** |
| **每 100 万输出 token 成本** | **`~$0.21`**（**H200 `$2.3/hour`**） |

---

### 与 DeepSeek R1 部署的对比

| 模型 | 专家数 | GPU | 预填充吞吐量（tokens/sec） | 解码吞吐量（tokens/sec） |
| --- | --- | --- | --- | --- |
| **DeepSeek R1** | 256 | 96 × H100 | 52.3k / 节点 | 22.3k / 节点 |
| **Kimi K2** | 384 | 128 × H200 | 56k / 节点 | 24k / 节点 |

尽管 Kimi K2 的 MoE 规模更大、路由更复杂，我们的部署仍然实现了：

- **均衡的专家激活**，借助专家并行负载均衡器（EPLB）
- 把 SGLang 针对 DeepSeek V3 架构的专项优化应用到 H200 上，实现**单 GPU 高吞吐量**

下一步是评估和优化长上下文场景。K2 是为智能体任务设计的模型，据反馈，此类场景中的平均输入长度可达 30,000 至 50,000 token。

---

## 5️⃣ 结论：大规模的万亿参数推理

通过结合 **OME**、**SGLang**、**PD 分离**与**大规模专家并行**，我们在 **128 块 H200 GPU** 上部署了 Kimi K2，实现了：

- 短上下文场景已可实现**高性价比的大规模推理**（H200 上每 100 万输出 token 约 $0.21），长上下文场景的优化仍在进行中。
- 通过模型驱动配置实现**简化的部署流程**

本次部署的所有组件均**完全开源且可复现**。欢迎社区在此基础上继续构建。

这次部署得以实现，不仅依靠 Mooncake 与 SGLang 社区之间的开放协作，也得益于 NVIDIA DGX Cloud 慷慨的基础设施支持。NVIDIA 通过 DGX Cloud 为 SGLang 团队提供了 128 块 H200 GPU 的使用权限，使我们能够以极快的速度完成 Kimi K2 从模型发布到生产级推理的部署。由此，各类组织现在都可以利用 SGLang 大规模服务 Kimi K2，以最先进的性能释放高级推理能力。

---

### 致谢

我们向以下团队和合作者致以衷心的感谢：

- **Mooncake 团队：**Boxin Zhang、Shangming Cai、Mingxing Zhang 及各位同事。
- **SGLang 团队与社区：**Simo Lin、Jingyi Chen、Qiaolin Yu、Yanbo Yang、Yineng Zhang 以及许多其他成员。

我们还要感谢 **MoonshotAI 团队**——包括 Shaowei Liu、Zhengtao Wang、Weiran He、Xinran Xu 等——感谢他们在调优 K2 这个"又大又漂亮"的模型过程中给予的支持。

---

## 延伸阅读

- [以 PD 分离与大规模 EP 部署 DeepSeek R1](https://lmsys.org/blog/2025-05-05-large-scale-ep/)
- [OME：模型驱动的 LLM 部署](https://lmsys.org/blog/2025-07-08-ome/)
- [Kimi K2 官方发布](https://moonshotai.github.io/Kimi-K2/)
- [SGLang GitHub 仓库](https://github.com/sgl-project/sglang)

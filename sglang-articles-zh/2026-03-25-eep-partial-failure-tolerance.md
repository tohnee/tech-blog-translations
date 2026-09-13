---
title: "SGLang 中的弹性专家并行：为 DeepSeek MoE 部署实现部分故障容忍"
title_en: "Elastic EP in SGLang: Achieving Partial Failure Tolerance for DeepSeek MoE Deployments"
author: "The Mooncake Team, Volcano Engine"
date: "March 25, 2026"
previewImg: /images/blog/eep-partial-failure-tolerance/figure.png
source: https://lmsys.org/blog/2026-03-25-eep-partial-failure-tolerance/
translated: 2026-09-12
---

# SGLang 中的弹性专家并行：为 DeepSeek MoE 部署实现部分故障容忍

> 原文：[Elastic EP in SGLang: Achieving Partial Failure Tolerance for DeepSeek MoE Deployments](https://lmsys.org/blog/2026-03-25-eep-partial-failure-tolerance/) · LMSYS Blog · The Mooncake Team, Volcano Engine

## 1. 问题所在：Wide EP 的必要性与脆弱性

要高效服务超大规模的专家混合（MoE）模型，部署"宽"（wide）专家并行（EP）策略——通常每个推理实例要横跨 32 张甚至更多 GPU——不是可选项，而是必然选择。我们需要 Wide EP 有两个关键原因：

- **最大化批大小以降低成本**：Wide EP 把支持超大批量（batch size）所需的海量 VRAM 聚合在一起。维持大批量是降低生产环境中单 token 总成本的根本驱动力。
- **最小化 TPOT 以获得更快速度**：把聚合的内存带宽扩展到这众多 GPU 之上，可直接降低每输出 token 时间（TPOT），确保生成快速、响应灵敏。

然而，扩大 EP 规模也引入了严重的可靠性瓶颈。在传统 EP 架构中，"爆炸半径"（即故障影响范围）与 EP 组的大小成正比。由于专家被硬性绑定在特定硬件上，EP 越大，单次硬件故障或进程失败拖垮整个推理实例的统计概率就越高。在原有配置下发生故障时，需要对服务器进行完整重启。这一过程通常耗时数分钟，造成大量资源浪费、灾难性的停机时间和糟糕的用户体验。SGLang 此前的 MoE 模式并不原生支持单实例内的**部分故障容忍**，因此迫切需要一种既能将对现有系统的干扰降到最低、又不牺牲规模的解决方案。

## 2. 方案概览：弹性专家并行（Elastic EP）及其潜力

为解决大规模 MoE 推理的脆弱性，我们将**弹性专家并行（Elastic EP）**集成到了 SGLang 框架中。

其核心思想是，Elastic EP 通过解耦专家与特定 GPU 之间的刚性映射来解决故障问题。通过在集群中维护冗余专家，系统能够检测到局部性的硬件或进程故障、重新分发专家权重，并立即把 token 重新路由到存活的专家上。这在不中断正在进行的推理过程的前提下实现了部分故障容忍。_（注：动态进程恢复功能也正在 PR [#15771](https://github.com/sgl-project/sglang/pull/15771) 中积极开发中。）_

### 效果

实现 Elastic EP 后，系统可靠性大幅提升，同时不牺牲速度。

- **服务在数秒内恢复**：为测试极限韧性，我们在 4 个节点（共 32 张 GPU，设置 ep_size=dp_size=32）上运行 DeepSeek V3.2，配置 256 个冗余专家，可容忍多达 16 个 rank 故障。随后我们终止部分正在运行的进程来模拟故障，使用 sglang.bench_serving 对系统进行基准测试，并基于 EPLBManager 日志测量重新分发丢失的专家权重并恢复服务所需的时间。恢复之后，系统继续正确推理，但由于资源减少，整体吞吐量有所下降。结果显示，服务中断时间保持在 10 秒以内——相比完整重启通常需要的 2–3 分钟，缩短了 90%。

| 故障 rank 数量 | 使用 Elastic EP 的中断时间（秒） | 剩余 rank 的吞吐量（tokens/sec） |
|------------------------|-----------------------------------------|----------------------------------------------|
| 1                      | 6.8                                     | 5552.41                                      |
| 2                      | 6.5                                     | 5431.50                                      |
| 4                      | 6.8                                     | 5265.12                                      |
| 8                      | 6.4                                     | 4479.84                                      |
| 16                     | 6.2                                     | 2825.44                                      |

- **零静态性能损耗**：我们在 4 节点配置（2 个预填充节点、2 个解码节点，各 8 张 GPU）上评估了 DeepSeek V3.2。对比关键指标，使用我们的 Elastic EP（Mooncake EP）进行服务，其静态性能与标准 DeepEP 方案完全一致。

| 系统       | 吞吐量（tokens/sec）    | 平均 TTFT（ms） | 平均 TPOT（ms） |
|------------|-------------------------|----------------|----------------|
| Elastic EP | 3560.21                 | 19399.24       | 54.25          |
| 标准（Standard）   | 3626.38                 | 21227.86       | 52.88          |

## 3. 详细的结构改动

为实现这一目标，该方案对 SGLang 架构引入了两项关键的结构改动：

1. **调度器层（高层，聚焦调度）**：这一层充当系统的守门人，持续维护数据并行（DP）rank 的健康状态。一旦某个 rank 失效，调度器会立即将其过滤掉，确保新的批次和请求只会被分配到健康的资源上。由此，推理任务不会被路由到失效的 rank，在调度层面实现了零干扰的**部分故障容忍**。（对应 PR：[#11657](https://github.com/sgl-project/sglang/pull/11657)。）
2. **专家并行层（低层，聚焦执行）**：这一层承担动态容错的重活。它通过实时调整专家到 GPU 的映射来管理 EP 组内的故障。故障发生时，它会立即在存活的 EP 成员之间重新分发所需的专家。这确保 MoE 推理在数学上仍能正确求解，并与可用资源保持一致，避免对实际执行造成严重中断。（对应 PR：[#10423](https://github.com/sgl-project/sglang/pull/10423)、[#10606](https://github.com/sgl-project/sglang/pull/10606)、[#17374](https://github.com/sgl-project/sglang/pull/17374)、[#12068](https://github.com/sgl-project/sglang/pull/12068)。）

这两层协同工作，把脆弱的 MoE 流水线变成了一个高韧性的引擎。

![eep-architecture.svg](/images/blog/eep-partial-failure-tolerance/figure.png)

<p style="color:gray; text-align: center;"> 图：4 GPU 场景下的 Elastic EP 系统示意图。 </p>

## 4. 支撑 Elastic EP：Mooncake 的角色

要有效实现 Elastic EP，系统需要一个高韧性的通信库，既能应对动态拓扑变化，又能在部分故障条件下保证 MoE 推理在数学上的正确执行。[Mooncake EP](https://kvcache-ai.github.io/Mooncake/python-api-reference/ep-backend.html) 是在更广泛的 PyTorch 生态中获得认可的稳健方案，它同时充当容错后端和专家并行的核心通信层，恰好满足这一需求。

作为通信主干，Mooncake EP 提供了以下几项关键能力：

- **具备韧性的通用集合通信**：对 broadcast、allgather 等标准集合通信原语提供严格的容错保障。
- **专用 EP 原语**：为专家并行必不可少的专用通信原语——dispatch 与 combine——提供容错处理，这对管理大型 MoE 模型固有的稀疏激活模式至关重要。
- **高性能 RDMA 与快速故障检测**：通过大量使用 GPU Direct RDMA，Mooncake 在整个集群上实现了极高的吞吐量和极低的 token 分发延迟。此外，它还借助这种底层网络控制能力，实现了基于超时的快速故障检测机制。
- **与 SGLang 无缝集成**：尽管底层网络实现复杂，该库在设计上可以与 SGLang 现有的执行流程和调度逻辑无缝集成。这种即插即用的兼容性把大规模系统重构的需求降到最低，同时立即解锁部分故障容忍能力。

## 5. 启用 Elastic EP

启动 SGLang 服务器时，使用以下参数即可启用 Elastic EP：

- `--elastic-ep-backend mooncake`：启用 Mooncake 作为具备容错能力的 torch distributed 后端。
- `--moe-a2a-backend mooncake`：启用 Mooncake 作为 EP 通信后端。
- `--mooncake-ib-device <comma-separated-ib-device-list>`：指定用于 Mooncake 通信的 IB 设备。
- `--ep-num-redundant-experts <num>`：设置用于容错的冗余专家数量。该值越大，系统可容忍的 rank 故障就越多。
- `--disable-custom-all-reduce`：禁用系统默认的自定义 all-reduce。
- `--enable-elastic-expert-backup`：启用内存中的专家权重备份，在容错场景下可以快速恢复权重。

注：NIXL EP 是 NVIDIA Dynamo 团队近期在 Elastic EP 框架下提出的新实现。设置 `--moe-a2a-backend nixl` 即可试用。

## 致谢

我们感谢社区中所有为这项工作做出贡献或提供支持的伙伴。

- SGLang 核心团队：Shangming Cai、Cheng Wan、Jingyi Chen、Lianmin Zheng 等许多同仁。
- Mooncake 团队：Xun Sun、Pingchuan Ma、Haoran Hu、Feng Ren、Mingxing Zhang 等许多同仁。
- 火山引擎（Volcano Engine）：Han Han、Shan Lu、Qin Qi、Yang Zhang 及其同事。
- Approaching AI：Yue Chen、Zhanhao Cao、Ke Yang 及其同事。
- 京东（JD.com）：Ziwei Yuan、Junlin Wei、Lianzhi Lin 及其同事。
- 阿里云（Aliyun）：Xinpeng Zhao、Xuchun Shang、Teng Ma 及其同事。

我们向 NVIDIA Dynamo 团队的支持与贡献致以诚挚的感谢。

## 链接

- [Elastic EP PR 汇总](https://github.com/sgl-project/sglang/pull/8961)
- [Mooncake 项目](https://github.com/kvcache-ai/Mooncake)

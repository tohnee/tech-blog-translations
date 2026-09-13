---
title: "超越单一模型：用 vLLM Semantic Router 构建混合模型（Mixture-of-Models）系统"
title_en: "Beyond a Single Model: Building Mixture-of-Models Systems with vLLM Semantic Router"
source: https://vllm.ai/blog/2026-07-21-vllm-sr-new-chapter-mom
crawled: 2026-09-12
translated: 2026-09-13
---

# 超越单一模型：用 vLLM Semantic Router 构建混合模型（Mixture-of-Models）系统

> 原文：[Beyond a Single Model: Building Mixture-of-Models Systems with vLLM Semantic Router](https://vllm.ai/blog/2026-07-21-vllm-sr-new-chapter-mom) · vLLM 博客

作者：vLLM Semantic Router 团队

[#生态](https://vllm.ai/blog/tags/ecosystem)[#混合模型](https://vllm.ai/blog/tags/mixture-of-models)[#语义路由](https://vllm.ai/blog/tags/semantic-router)

大多数 AI 应用都围绕单一模型端点构建。但随着模型、设备和部署约束日益多样化，没有任何单一模型能对每个请求、每种环境都是最佳选择。现实的问题是如何通过一个接口来协调、评估和服务多个专用模型。我们把这种系统化方法称为**混合模型（Mixture-of-Models，MoM）**。

自公开发布以来不到一年，[vLLM Semantic Router](https://github.com/vllm-project/semantic-router) 已达到 **5,000 stars**、**150+ 贡献者**，以及我们的 Hugging Face 模型家族累计**超过 300,000 次下载**。历经 **Iris、Athena、Themis** 三个主要版本，系统边界从选择一个模型，演进到治理多模型推理，再到跨会话保存状态与协调。这些版本为从第 0 天就构想的 MoM 架构打下了基础。

本文描述 vLLM Semantic Router 的下一步：从在模型之间路由，转向用这些模型构建可靠可信的模型系统。在一个带版本的契约之下，独立的模型、策略、偏好与执行路径汇聚为一个可以通过单一接口训练、评估、导出、导入、部署和调用的系统。我们的目标是把 vLLM Semantic Router 打造成混合模型的训练、评估与推理引擎。

![图 1：混合模型把异构的模型组合变成统一的模型体验。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/hero.png)

图 1：混合模型把异构的模型组合变成统一的模型体验。

## vLLM-SR 走过的路

[第一篇 vLLM Semantic Router 文章](https://blog.vllm.ai/2025/09/11/semantic-router.html)提出了一个实际问题：为什么要给简单请求和困难请求分配同样的推理预算？一个轻量级分类器使用固定的领域标签在快速路径与推理路径之间做选择，帮助 vLLM 更有选择性地花费推理算力。

生产流量很快暴露了这一设计的局限。仅凭领域无法表达隐私、安全、上下文、语言、模态、工具、偏好、延迟和授权。静态标签也无法顾及一个便宜但过载的端点、能力强但位置很远的端点，或在智能体会话进行到一半时切换过去并不安全的端点。

我们围绕模块化模型支持、共享 LoRA 计算、Rust/Candle 推理和 Go 集成重建了分类器层。随后我们用"信号-决策"（Signal–Decision）架构取代固定分类，把观测到的证据与策略、执行分离开来。这成为之后三个版本的骨架。

| 里程碑 | 时间 | 变化内容 |
| --- | --- | --- |
| **孵化** | 2025 年 4 月 | 早期语义路由原型起步，以混合模型作为长期系统目标 |
| **首次发布** | 2025 年 9 月 | 意图感知的快速/推理路径选择 |
| **v0.1 Iris** | 2026 年 1 月 | 信号、决策与路由级插件取代固定分类 |
| **v0.2 Athena** | 2026 年 3 月 | 模型选择、记忆、RAG、长上下文与多模态把路由扩展为推理控制系统 |
| **v0.3 Themis** | 2026 年 6 月 | 有状态路由、投影、重放、协议支持、会话连续性与统一的生产配置契约使系统可运营 |
| **Fusion 与 Micro-Agent** | 2026 年 6 月 | 路由器开始选择协作模式，而不仅仅选择单个模型 |

![图 2：每个阶段都改变了控制单元：模型、决策、系统、会话，最终是完整的模型生命周期。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/evolution.png)

图 2：每个阶段都改变了控制单元：模型、决策、系统、会话，最终是完整的模型生命周期。

[Iris](https://blog.vllm.ai/2026/01/05/vllm-sr-iris.html) 让路由变得可组合。领域、关键词、嵌入、事实性、反馈和偏好信号汇入显式决策，而安全、PII 保护、缓存、幻觉检测和工具选择则成为路由范围内的行为。Iris 还引入了 MoM 模型家族，并把 vLLM-SR 描述为"面向混合模型的系统级智能"（System Level Intelligence for Mixture-of-Models）。

[Athena](https://blog.vllm.ai/2026/03/10/v0.2-vllm-sr-athena-release.html) 增加了一等公民的模型选择、记忆与 RAG、多语言多模态模型栈、ROCm 加速以及运营仪表盘。这个项目正在成为围绕多模型推理的控制系统，而不仅仅是 vLLM 前面的一个分类器。

[Themis](https://blog.vllm.ai/2026/06/05/v0.3-vllm-sr-themis-release.html) 把这个更大的系统变成了一份可运营的契约：

> **信号变成投影（projection）。投影喂给决策。决策挑选算法。算法选出模型。**

Themis 增加了会话感知的智能体路由、可重放的轨迹、更强的协议支持、运维控制台，以及覆盖 AMD ROCm、NVIDIA CUDA、Intel OpenVINO 与 CPU 环境的运行时路径。它还让路由可解释：运维人员可以看到每个决策背后的证据、策略、算法和物理模型。

### 从"信号-决策"到"工作负载-路由器-资源池"

这些版本构建了运行时。两篇项目论文解释了其背后的架构。

[白皮书《Signal Driven Decision Routing for Mixture-of-Modality Models》](https://vllm-sr.ai/white-paper/)形式化了神经证据与符号策略之间的分离。快速启发式与学习到的分类器把提示、上下文、身份、安全和模态转化为结构化的信号向量；一个布尔引擎再把信号组合成可审计的策略。一个带类型的神经符号 DSL 在把策略编译为可部署配置之前先解析并验证它。论文发表时，系统覆盖 13 种信号类型和 13 种模型选择算法，并带有针对缓存、RAG、记忆、安全、供应商处理和响应校验的按决策插件。

[愿景论文《The Workload–Router–Pool Architecture for LLM Inference Optimization》](https://vllm-sr.ai/vision-paper/)则放宽了视野。它主张三个变量必须一起设计：

- **工作负载（Workload）：** 聊天还是智能体，单轮还是多轮，热还是冷，预填充密集还是解码密集
- **路由器（Router）：** 静态语义策略、在线反馈或老虎机自适应、基于强化学习的选择，以及质量感知级联
- **资源池（Pool）：** 同构或异构加速器、预填充/解码拓扑、模型放置，以及 KV 缓存管理

这些变量无法独立优化。工作负载形态决定哪种路由策略有效；路由策略改变所需的池规模与拓扑；池状态决定哪条路由是高效的。安全与隐私横跨全部三个维度，而成本、质量、延迟与能耗定义了优化前沿。论文把项目的研究映射进一个 3 × 3 的 WRP 矩阵，并指出 21 个这些维度仍需交汇的开放方向。

![图 3：白皮书定义了可编程路由引擎；愿景论文把它与工作负载和物理资源池设计连接起来。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/research-arc.png)

图 3：白皮书定义了可编程路由引擎；愿景论文把它与工作负载和物理资源池设计连接起来。

两篇论文加在一起，让路由变得可编程，并将其与工作负载和硬件绑定——这正是 MoM 纳入单一模型契约之下的两大基础。

与此同时，运行时早已超越单模型选择。[Fusion](https://blog.vllm.ai/2026/06/16/vllm-sr-fusion-api.html)、ReMoM、Confidence、Ratings 和有界 Workflow 让一个请求就能在模型之间发起受控的协作。正如 [Micro-Agent 工作](https://blog.vllm.ai/2026/06/29/micro-agent-frontier-models.html)所示，客户端只需调用一个模型名，服务层就会选择一个配方（recipe）、向多个 worker 分发、对它们的结果进行验证或综合，然后返回一个普通响应。

| 第一章 | 新篇章 |
| --- | --- |
| 为请求选路 | 构建模型系统 |
| 选择一个模型或能力路径 | 训练、评估并执行整个 MoM |
| 配置运行时策略 | 打包可移植、带版本的模型工件 |
| 优化一个路由决策 | 在质量、成本、延迟、安全与能耗之间优化系统智能 |
| 把后端选择藏在同一个 API 之后 | 让完整的多模型系统表现得像一个模型 |

路由依然根本。它是混合模型分配工作、施加策略、协调各部分的方式。但路由只是机制，**模型系统才是产品。**

## 为什么模型边界必须移动

今天的 AI 技术栈在四个轴上碎片化：

- **模型碎片化。** 封闭的前沿模型、开放的通用模型、领域专家模型、紧凑的本地模型、验证器模型与多模态模型将长期共存。没有任何一个能同时在质量、成本、延迟、可信、隐私与领域契合度上胜出。
- **算力碎片化。** GPU、CPU、专用加速器、边缘设备、云容量与私有集群在内存、内核、可用性、价格和能耗上各不相同。模型选择与放置正在变成同一个决策。
- **位置碎片化。** 推理横跨云端、数据中心与边缘。隐私或数据驻留要求可能排除更强的远程模型，而本地工作负载可能仍需要按需调用的云端专家。
- **偏好碎片化。** 不存在普适的"最佳"。产品与用户在准确率、延迟、价格、隐私、安全、风格与多模态之间做出不同的权衡。这些选择应当直接塑造执行方式。

今天，每个应用都只能自行调和这些碎片。

![图 4：在 MoM 之前，碎片化的智能变成了应用侧的路由胶水。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/fragmentation-before-mom.png)

图 4：在 MoM 之前，碎片化的智能变成了应用侧的路由胶水。

混合模型把这份责任移到了一个模型边界之后。

在这个边界上，**智能分配**成为模型的一部分。引擎决定哪些模型具备资格、执行可以在哪里运行、模型之间是否应该协作，以及如何满足硬性约束。

能耗让分配与效率密不可分。硬件和推理引擎通过每瓦每美元产出更多 token 来改善供给侧。分配层控制需求侧：哪些工作配得上这些 token，哪个模型或哪种协作能在所需的质量、延迟和能耗预算内提供它们。

应用只需选择一个带版本的模型身份，就会收到一个可归因的响应。它的物理实现仍可以横跨开放与封闭模型、云端与边缘、不同世代的加速器。碎片化依然存在，但它成为模型系统的内部事务，而不再泄漏进每一个应用。

![图 5：有了 MoM，同样碎片化的资源成为一个模型的内部实现。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/fragmentation-after-mom.png)

图 5：有了 MoM，同样碎片化的资源成为一个模型的内部实现。

## 我们所说的混合模型是什么

**混合模型（Mixture-of-Models）**是一个带版本的复合模型，其引擎通过跨独立模型与算子的、以偏好为条件、以资源为约束的路径来实现每个请求。它通过单一模型接口呈现给用户，并返回一个可归因的结果。

多上游网关可以转发流量，但并不对系统质量负责。而 MoM 拥有一个目标、一份评估契约、一种可复现的组合方式，以及执行它的运行时。

MoM 也不同于混合专家（Mixture-of-Experts）。MoE 在一次前向传播中把 token 路由到内部专家之间；MoM 协调的是彼此独立的模型，它们在架构、所有者、许可证、模态、协议、上下文窗口和硬件上都可能不同。一个 MoE 检查点本身也可以是 MoM 的一个组件。

|  | 传统模型 | 混合模型 |
| --- | --- | --- |
| 智能单元 | 一个检查点 | 一个受治理的模型系统 |
| 专业化 | 主要编码在权重中 | 由独立专家组合而成 |
| 执行 | 单一生成路径 | 选择、级联、验证、融合或工作流 |
| 优化目标 | 单个模型的质量与效率 | 横跨质量、成本、延迟、安全、隐私与能耗的系统前沿 |
| 部署边界 | 单一运行时 | 云、数据中心与边缘 |
| 用户契约 | 一个模型身份 | 一个模型身份 |

![图 6：选择是 MoM 的一种拓扑。级联、并行融合与有界工作流共享同一个模型边界。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/execution-topologies.png)

图 6：选择是 MoM 的一种拓扑。级联、并行融合与有界工作流共享同一个模型边界。

因此，一个可移植的 MoM 需要的不只是权重和配置：它还需要组件清单、能力元数据、路由与协作配方、策略、偏好、评估套件、运行时约束、来源追溯以及版本历史。

开放检查点可以随工件一起流转；封闭模型则保持为经过鉴权的外部引用，带有明确的能力与策略契约。导出一个 MoM 并不能让专有检查点变得可移植，它让**模型系统**变得可复现。

### 把偏好变成模型

当偏好以模型身份的形式发布时，它们就变得具体。一个 MoM 家族可以提供多个运行点：

| 模型身份 | 契约 |
| --- | --- |
| `vllm-sr/mom-v1-flash` | 最小化期望延迟 |
| `vllm-sr/mom-v1-light` | 在质量下限之上最小化成本 |
| `vllm-sr/mom-v1-ultra` | 在声明的预算内最大化质量 |
| `vllm-sr/mom-v1-halu` | 要求溯源检查与故障关闭（fail-closed）回退 |
| `vllm-sr/mom-v1-secu` | 在执行前强制执行越狱与 PII 策略 |

每个名字都是一份带版本的模型契约，而不是路由器预设。应用选择它需要的行为；vLLM-SR 选择并协调能交付该行为的模型，同时守住硬性的隐私、驻留、授权与安全约束。

对应用而言，整个系统仍然只是一次普通的模型调用：

```
{
  "model": "vllm-sr/mom-v1-ultra",
  "messages": [
    {"role": "user", "content": "Review this design and identify its weakest assumption."}
  ]
}
```

这个身份可以选择单个模型、通过级联逐级升级、比较多个并行答案、要求溯源检查，或运行一个有界工作流——而外部接口、版本或响应契约都不变。

![图 7：偏好以有界、带版本的模型契约形式发布——而不是藏在应用侧的路由预设。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/preference-models.png)

图 7：偏好以有界、带版本的模型契约形式发布——而不是藏在应用侧的路由预设。

四个平面划分权责：

| 平面 | 拥有什么 | vLLM-SR 中已有的基础 | 下一步 |
| --- | --- | --- | --- |
| **工件（Artifact）** | 组件、能力、目标、策略、评估契约、来源 | 规范化配置、模型引用、DSL、带版本的策略 | 可移植的 MoM 导入/导出规范 |
| **学习（Learning）** | 路由器自有模型、偏好、结果、配方改进 | 训练栈、Router Learning、重放、结果 API | 联合训练与系统级发布关卡 |
| **执行（Execution）** | 信号、投影、决策、选择器、循环器、插件 | 信号-决策运行时、Fusion、ReMoM、Workflow、安全与记忆 | 一个生命周期感知的 MoM 引擎 |
| **物理（Physical）** | 供应商、模型池、加速器、位置、缓存与能耗状态 | vLLM 后端、云供应商、ROCm、CUDA、OpenVINO、CPU | 跨云、数据中心、边缘和本地设备的可移植放置 |

![图 8：一个完整的 MoM 横跨四个平面：工件、学习、执行与物理实现。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/four-planes.png)

图 8：一个完整的 MoM 横跨四个平面：工件、学习、执行与物理实现。

一次部署必须把逻辑需求映射到其环境中可用的模型和机器上。该提案使用四个对象：

1. **bundle（打包件）**固定接口、图、策略、行为变体、边界与不可变的语义资产。
2. **binding（绑定）**把逻辑组件映射到符合条件的部署，而不改变模型的决策语义。
3. **resolution lock（解析锁）**冻结各组成部分的版本、运行时、镜像、加速器与供应商观测。
4. **run record（运行记录）**把每个决策、调用、约束检查、成本与结果归因到产生它们的 bundle、binding 和锁。

![图 9：一个稳定的模型身份，从可移植契约到可归因的运行。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/artifact-resolution-lifecycle.png)

图 9：一个稳定的模型身份，从可移植契约到可归因的运行。

这种分离让可移植性保持诚实。同一个 `mom-v1-ultra` 可以绑定到 ROCm、CUDA、私有 CPU 或 NPU 节点，或混合部署，而不必承诺不透明供应商给出完全相同的输出。相反，它保留控制语义、暴露替换情况，让服务与评估面对同一个解析后的系统。

## vLLM-SR 作为 MoM 引擎

训练、评估与推理必须共享同一份契约；否则研究、基准测试与生产会漂移成彼此不同的系统。

### 训练分配，而不仅是权重

MoM 训练涵盖路由器自有的嵌入、信号编码器、偏好与安全模型以及选择器。它还学习分配与协作：哪条路径适合某个工作负载和预算、级联应该在何时停止、评审团（panel）应该如何判定或综合、智能体会话何时应该切换模型。由于各组成部分可能相互独立或封闭，进步并不要求梯度穿过所有组件；策略、阈值、池、提示、契约和拓扑都可以从轨迹与结果中优化。

目标是横跨质量、延迟、成本、安全、隐私、可靠性、位置与能耗的前沿。重放与结果把生产经验回馈到离线训练中，同时不让热路径悄悄改写策略。

### 把 MoM 当作一个模型来评估

评估必须对模型身份进行端到端打分；后端基准只是输入，而不是结果。一份带版本的记分卡应测量路由遗憾（routing regret）、协作收益、恢复能力、会话连续性、尾延迟、成本、安全、隐私与能耗。它还应压力测试供应商故障、设备丢失、模型分歧、工作负载漂移与偏好变化。每个声明的运行点也都需要自己的测试：`flash` 要测其延迟-质量前沿，`light` 要测其质量下限，`ultra` 要测其预算约束。

科学上的检验比"更多调用是否改善基准分数"更严格。在活跃算力对齐的前提下，一个条件化的系统能否比最好的固定模型更好地利用互补的优势与失败模式？没有这种对照，MoM 就可能把暴力扩展藏在一张聪明的图后面。评估必须在报告质量的同时报告调用数、token 数、成本、延迟与能耗——并在组合没有带来帮助时如实公布。

![图 10：只有在活跃算力对齐的前提下，组合收益才有意义，且质量必须与调用数、token 数、成本、延迟与能耗一同报告。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/matched-compute-evaluation.png)

图 10：只有在活跃算力对齐的前提下，组合收益才有意义，且质量必须与调用数、token 数、成本、延迟与能耗一同报告。

### 在推理时执行智能

在推理时，引擎判断单个模型是否足够。它可以选择一个本地专家模型、保留热会话、通过置信度级联升级、要求检索或验证、运行一个 Fusion 评审团，或执行一个有界工作流。运行时掌握预算、拓扑、回退、轨迹与响应契约；应用只做一次普通的模型调用。

![图 11：MoM 是一个闭环生命周期：训练分配策略、评估完整系统、执行它，并把结果转化为下一个经验证的版本。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/mom-lifecycle.png)

图 11：MoM 是一个闭环生命周期：训练分配策略、评估完整系统、执行它，并把结果转化为下一个经验证的版本。

## 一个可以迁移的模型

我们的目标是一个完整的 MoM，可以**作为一个统一模型被构建、导出、导入、版本化、评估、部署和调用**。一份逻辑规范编译成不可变的 bundle，绑定到环境，解析出具体部署，并在服务与评估中保持同一身份。

工件应能在开发者机器、私有集群、云机群和边缘环境中运行，同时其物理实现可以变化。一个专家模型可以解析为某个合规的本地检查点或托管端点；一个加速器运行时可以被替换。如果隐私要求使某个远程专家不可用，引擎会遵循声明的回退或弃权路径。绑定不能悄悄改写图、放松守护，或把评审团变成级联——这些改动需要新的模型版本。

"在任何硬件上运行"是一项架构要求，而不是声称今天每个组件都已可移植。项目已经支持横跨 ROCm、CUDA、OpenVINO 与 CPU 的路径。接下来，硬件能力与放置将成为 MoM 契约的一部分，让引擎能把模型系统映射到可用资源上。

用户体验的标准很简单：

> **一个模型身份。多个模型。任意硬件。**

![图 12：一个逻辑模型身份可以在开发者、数据中心、云与边缘硬件上实现。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/portable-realizations.png)

图 12：一个逻辑模型身份可以在开发者、数据中心、云与边缘硬件上实现。

如果应用需要知道每个子模型归哪个供应商所有、由哪台设备运行，或该执行哪条回退图，那么抽象就已经泄漏了。

## 现在要改变什么

下一阶段聚焦四个相互关联的方向：

1. **定义可移植的 MoM 规范。** 把组件、目标、策略、偏好、评估、约束与执行语义打包为一个带版本的工件。
2. **闭合训练-评估-推理回路。** 从评估与重放中改进模型与配方，然后通过可评审、可安全回滚的发布交付。
3. **构建异构运行时。** 以硬件、位置、能耗与数据边界为输入，把一个 MoM 映射到云、数据中心与边缘。
4. **保持模型接口朴实无华。** 让 MoM 像单一模型一样易于导入、部署和调用。

![图 13：四条相互衔接的工作流把混合模型从一种执行模式变成下一代模型架构。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/next-stage-roadmap.png)

图 13：四条相互衔接的工作流把混合模型从一种执行模式变成下一代模型架构。

这是一项研究计划，涵盖：独立模型应如何专业化、竞争、验证与协作；如何测量由此形成的系统；以及一份模型契约如何跨越设备与环境存活。我们的使命是：

> **推进跨模型、跨设备、跨环境的智能科学。**

我们将研究组合在何时能产生超越单一检查点的能力，把放置与能耗视为智能的一部分，并把同一份模型契约从边缘带到云端、从研究带到生产。

## 与我们共建

构建混合模型需要的不只是路由。这项工作横跨模型训练、评估、服务系统、硬件与生产运维。

Iris、Athena 和 Themis 的进步，是因为贡献者带来了真实的工作负载、添加了后端、训练了模型、发布了基准、找到了失败案例，并为更好的接口据理力争。MoM 需要同样广度的工作：可学习的分配、偏好优化、模型协作、能耗感知推理、可移植工件、开放评估与异构运行时。

如果你正在研究这些问题，我们希望从你的工作负载与测量中学习。构建一个运行点、添加一个运行时、测试一个协作配方，或者公布一个组合失败的反例。如果 MoM 的假设能在公开环境中接受检验，它就会更强大。

### 致谢

vLLM-SR 的成长离不开工程、研究与更广泛生态的工作。我们感谢 [Xunzhuo Liu](https://www.linkedin.com/in/bitliu)、[Huamin Chen](https://www.linkedin.com/in/huaminchen)、[Bowei He](https://www.linkedin.com/in/bowei-he-8a9450199/)、[Yankai Chen](https://www.linkedin.com/in/yankai-chen-923001154/)、[Fuyuan Lyu](https://www.linkedin.com/in/fuyuan-lyu-560756167/) 和 [Steve Liu](https://ca.linkedin.com/in/xueliu) 帮助塑造其技术与研究方向。我们也感谢 [Andy Luo](https://www.linkedin.com/in/andyluo77/) 与 [Haichen Zhang](https://www.linkedin.com/in/haichen-zhang-9010b6382/) 在 ROCm 适配、路由器模型训练和开放 MoM 实验方面的工作。

这项工作也离不开 [FAUST](https://github.com/FAUST-BENCHOU)、[David Shrader](https://www.linkedin.com/in/shraderdm/)、[Yang Wu](https://github.com/drivebyer)、[Ramakrishnan Sathyavageeswaran](https://github.com/ramkrishs)、[Kuntai Wu](https://github.com/WUKUNTAI-0211)、[Aayush Saini](https://github.com/AayushSaini101)、[siloteemu](https://github.com/siloteemu)、[Chen Wang](https://www.linkedin.com/in/chenw615/)、[Yue Zhu](https://www.linkedin.com/in/yue-zhu-b26526a3/)、[Senan Zedan](https://www.linkedin.com/in/senan-zedan-2041855b/)、[Yossi Ovadia](https://www.linkedin.com/in/yossi-ovadia-336b314/)、[Samzong Lu](https://www.linkedin.com/in/samzong)、[Liav Weiss](https://www.linkedin.com/in/liav-weiss-2a0428208)、[Asaad Balum](https://www.linkedin.com/in/asaad-balum-0928771a9/)、[Yehudit](https://www.linkedin.com/in/yehuditkerido/)、[Noa Limoy](https://www.linkedin.com/in/noalimoy/)、[Marina Koushnir](https://github.com/mkoushni)、[Jared Wen](https://github.com/JaredforReal)、[Abdallah Samara](https://www.linkedin.com/in/abdallah-samara)、[Hen Schwartz](https://www.linkedin.com/in/henschwartz)、[Srinivas A](https://www.linkedin.com/in/sriniabhiram)、[Yang Zhu](https://github.com/carlory)、[Jintao Zhang](https://www.linkedin.com/in/jintao-zhang-402645193/)、[yuluo-yx](https://github.com/yuluo-yx)、[cryo](https://github.com/cryo-zd)、[Bishen Yu](https://github.com/OneZero-Y)、[Zhijie Wang](https://github.com/aeft)、[Hao Wu](https://github.com/haowu1234) 和 [Qiping Pan](https://www.linkedin.com/in/qiping-pan-8662ab215/)。他们的代码、评审、测试、文档与治理把项目从一个发布推进到下一个发布。

在这个里程碑，项目已累计 **1,734 个提交**和 **150+ 贡献者**。我们感谢 MBZUAI、麦吉尔大学（McGill University）、Mila 和莱斯大学（Rice University）的合作者，以及更广泛的 vLLM、AMD、Intel、Meta、Red Hat、Microsoft、Google、IBM、NVIDIA、Hugging Face、NASA、Nutanix、DaoCloud 和开源社区。这个里程碑属于每一位帮助把一个早期路由器变成真正系统的人。

![图 14：构建 MoM 引擎是一个开放的系统问题，需要整个模型与基础设施社区。](https://vllm.ai/blog-assets/figures/2026-07-21-vllm-sr-new-chapter/community.png)

图 14：构建 MoM 引擎是一个开放的系统问题，需要整个模型与基础设施社区。

欢迎在 [GitHub](https://github.com/vllm-project/semantic-router) 上加入我们，浏览[文档](https://vllm-sr.ai)，试用 [MoM 模型家族](https://huggingface.co/LLM-Semantic-Router)，并在 [vLLM Slack](https://vllm-dev.slack.com/archives/C09CTGF8KCN) 的 `#semantic-router` 频道与社区见面。

vLLM Semantic Router 起于帮助基础设施为每个请求选择合适的模型。

现在，我们正在把这一基础扩展到单一模型之外：迈向能在设备与环境之间协调、评估并运营多个模型的系统。

我们邀请社区与我们一起在公开环境中构建并检验这一方法。

---
title: "Agent 辅助的 SGLang 开发：一次初步探索"
title_en: "Agent-Assisted SGLang Development: An Initial Exploration"
author: "SGLang Team"
date: "July 2, 2026"
previewImg: /images/blog/agent-assisted-sglang-development/sglang-agent-cover.png
type: blog
source: https://lmsys.org/blog/2026-07-02-agent-assisted-sglang-development/
translated: 2026-09-12
---

# Agent 辅助的 SGLang 开发：一次初步探索

> 原文：[Agent-Assisted SGLang Development: An Initial Exploration](https://lmsys.org/blog/2026-07-02-agent-assisted-sglang-development/) · LMSYS Blog · SGLang Team

SGLang 的开发工作越来越超出孤立代码改动的范畴。如今同一个仓库横跨 LLM 推理服务、分布式运行时、GPU 内核、扩散模型流水线、模型专属执行路径以及生产事故处理。过去，这些工作流很多依赖开发者个人的记忆：某个模型怎么启动、剖析（profile）trace 怎么读、调试 CUDA 崩溃时先加哪条日志、性能 PR 应该附上哪些基准测试。随着智能体（agent）工具走向成熟，这些经验可以转化为可执行的 `SKILL.md` 文件、脚本、基准测试契约和评审循环。

围绕 SGLang 的智能体开发，目前已经形成了一批同时覆盖 LLM 与扩散两类工作的技能（skill）：

- [SGLang `.claude/skills`](https://github.com/sgl-project/sglang/tree/main/.claude/skills) 维护在 SGLang 仓库内部，沉淀了仓库级开发工作流，包括 CUDA 崩溃调试、内核集成、测试、CI、性能剖析、生产事故分诊和源码目录约定。
- [SGLang diffusion `.claude/skills`](https://github.com/sgl-project/sglang/tree/main/python/sglang/multimodal_gen/.claude/skills) 聚焦扩散模型相关的工作流，包括接入新的扩散模型、对去噪路径做基准测试与剖析、调优性能选项，以及验证量化后的流水线。
- [BBuf/AI-Infra-Auto-Driven-SKILLS](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS) 覆盖跨框架推理服务基准测试、容量规划、剖析与流水线分析、模型计算量仿真、SGLang 拟人化评审、生产事故分诊、面向 SGLang 及其他开源推理框架的 SOTA 循环，以及模型 PR 演进历史。
- [kernel-design-agents](https://github.com/mit-han-lab/kernel-design-agents) 即 KDA 项目，也是 MLSys 2026 FlashInfer 内核竞赛（Kernel Contest）的冠军方案。
- [BBuf/KDA-Pilot](https://github.com/BBuf/KDA-Pilot) 把 KDA 风格的智能体内核工作流应用到 SGLang 上。其公开的 B200 扩散汇总目前跟踪 10 个 SGLang 内核任务。其中大多数数据行来自 KDA-Pilot 的公开基准测试台账，而 `residual_gate_add` 一行采用的是已合并 SGLang 集成 PR 所报告的 B200 加速比（原任务基线在此期间发生了变动）。目前已有三项源自 KDA-Pilot 的工作落入三个 SGLang 集成 PR。

把这些工作放在一起看，它们指向同一个方向：智能体的价值来自程序性的工程知识，包括可执行的步骤、可复现的实验和可评审的证据。

## 1. TL;DR

- 当智能体能够沿着定义清晰的工作流持续推进时，它们在 SGLang 中最有用武之地。基准测试、性能剖析、内核 API 记录、接入扩散流水线、生产事故重放和 SOTA 循环，都可以编码为技能。
- SGLang 技能是一段可执行的开发流程。在 `debug-cuda-crash`、`sglang-diffusion-benchmark-profile` 和 `llm-torch-profiler-analysis` 中，真正重要的内容是预检（preflight）、硬性失败门禁、产物契约、复现命令和结果格式。
- 剖析证据是性能工作的核心。SGLang 的剖析类技能产出固定格式的内核表、重叠机会表和融合模式表；KDA-Pilot 在此基础上扩展出同 ABI 的基线/候选对比、真实负载、正确性门禁、NCU 证据以及逐形状（per-shape）结果。
- 长时间运行的优化工作已开始进入循环工程（Loop Engineering）阶段。SGLang SOTA 性能循环把「追逐 SOTA」分解为公平基准测试、差距判定、剖析、打补丁和复验。Humanize/RLCR 在此之上增加外部评审，而 Codex Goal 可以用更低的协调开销运行同样的循环。
- 评审变得更加重要。智能体能跑更多实验，但也会产生更多看似合理、仍需仔细评审的改动。开发者越来越多地承担这样的角色：定义问题、挑选证据、设计工作流，并判断结果是否可以进入生产路径。

## 2. 为什么 SGLang 适合 Agent 辅助开发

SGLang 是一个面向大语言模型和多模态模型的高性能推理服务框架。随着模型家族和硬件路径不断扩展，开发中反复出现以下几类问题：

- LLM 路径很复杂。一个性能问题可能同时横跨 Python 运行时、调度器、CUDA 图、Triton/CUDA 内核、FlashInfer/FlashAttention、分布式集合通信以及模型专属的封装层。
- 扩散模型路径同样复杂。一次变慢的去噪步骤，可能涉及 pipeline/stage 划分、DiT 块、注意力后端、`torch.compile` 图断裂（graph breaks）、CFG/SP 并行、VAE，或自定义融合内核。
- 验证成本高昂。许多改动必须在 H100、H200、B200 或 RTX 5090 上用真实模型和真实负载来测试，仅靠本地单元测试是不够的。
- 剖析结果难以靠人工复用。一条 trace 可能包含成百上千次内核启动。靠人工阅读 Perfetto，很容易漏掉内核与 Python 源码之间的映射关系，也容易把预填充（prefill）和解码（decode）混为一谈。开发者会在阅读剖析输出时积累经验：哪些内核名对应哪些模型逻辑、哪些启动模式暗示图断裂、哪些 NCCL/注意力/MLP 布局属于正常。如果这些知识只留在某个人的脑子里，下一个任务就无法复用。
- 性能结论高度依赖上下文。GPU 型号、形状、batch 大小、并行方式、精度、后端和编译状态都可能改变结果。孤立的微基准测试往往无法证明真实的模型级收益，因此需要一套端到端的长时测试流程，在固定负载下反复验证吞吐量、延迟、显存、精度和稳定性。这一流程既费人力又费时间。

这些问题与智能体天然契合。启动服务器、固定负载、采集 trace、对剖析数据行做分诊、补充测试、记录实验结果——这些工作的输入和输出都很明确，非常适合脚本化和重复执行。开发者需要定义的是边界：统一的基准测试设置、统一的剖析解读规则、统一的精度门禁，以及智能体应当停止改代码的条件。

因此，本文讨论的智能体是受工程工作流约束的执行者。反复出现的 SGLang 开发流程可以沉淀为技能，让智能体负责重复性执行、证据收集和状态跟踪；而定义目标、判断证据、评审一项改动是否该进入真实服务路径，这些仍然由开发者负责。

## 3. 从提示工程到 SKILL：协议与示例

在 SGLang 框架中，一个有用的技能至少应当回答以下问题：

| 问题 | 技能应当沉淀的内容 |
| --- | --- |
| 何时使用 | 触发场景、支持的模型、支持的硬件，以及硬停止（hard-stop）情形 |
| 如何启动 | 预检、环境变量、仓库状态、依赖检查和模型配置 |
| 如何验证 | 基准测试命令、剖析命令、测试入口和精度门禁 |
| 如何决策 | 输出表格、失败模式、优先级、风险类别和回退条件 |
| 如何交付 | 产物目录、结果 schema、PR 描述、复现命令和评审要求 |

SGLang 相关的智能体技能覆盖不同层面。有的贴近源码改动，比如调试、测试、接入扩散模型、基准测试/剖析工作流；有的则面向跨框架基准测试、容量规划、计算量仿真、生产事故分诊、PR 优化知识、SGLang 拟人化评审，以及 Humanize/RLCR 这类更高层的工作流。

### 3.1 当前的技能栈

常用的 SGLang 智能体技能可以分为以下几类。

| 层面 | 代表性技能/项目 | 解决的问题 |
| --- | --- | --- |
| CUDA 崩溃 | [`debug-cuda-crash`](https://github.com/sgl-project/sglang/tree/main/.claude/skills/debug-cuda-crash) | 在自定义算子/内核 API 边界处记录输入、异常和转储（dump），把转瞬即逝的崩溃变成可以离线分析的样本 |
| LLM 基准测试 | [`llm-serving-auto-benchmark`](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/skills/llm-serving-auto-benchmark) | 在 SGLang 和其他 OpenAI 兼容推理栈之间运行公平、有界、可断点续跑的推理服务基准测试搜索 |
| 容量规划 | [`llm-serving-capacity-planner`](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/skills/llm-serving-capacity-planner) | 解析 SGLang 及其他推理框架的启动日志，解释权重显存占用、KV 缓存预算、CUDA 图开销、请求容量和 OOM 压力 |
| Trace 分诊 | [`llm-torch-profiler-analysis`](https://github.com/sgl-project/sglang/tree/main/.claude/skills/llm-torch-profiler-analysis) | 产出固定格式的内核表、重叠机会表和融合模式表，并把内核映射回 Python 源码；同一套统一工作流也存在于 AI-Infra 中，供跨框架使用 |
| 流水线/层分析 | [`llm-pipeline-analysis`](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/skills/llm-pipeline-analysis) | 把 torch profiler trace 切分为前向传播、层和内核流，用于定位稳态前向、瓶颈层类型和 Perfetto 时间区间 |
| 模型计算量仿真 | [`model-compute-simulation`](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/skills/model-compute-simulation) | 为 LLM 构建算子级计算模板，估算张量形状、FLOPs、MFU、内核到算子的映射，以及不同并行方案的假设分析（what-if） |
| 扩散基准测试/剖析 | [`sglang-diffusion-benchmark-profile`](https://github.com/sgl-project/sglang/tree/main/python/sglang/multimodal_gen/.claude/skills/sglang-diffusion-benchmark-profile) | 采集去噪延迟、perf 转储和 torch profiler trace，并首先检查执行确实走的是 SGLang 原生扩散后端 |
| 接入扩散模型 | [`sglang-diffusion-add-model`](https://github.com/sgl-project/sglang/tree/main/python/sglang/multimodal_gen/.claude/skills/sglang-diffusion-add-model) | 把来自 Diffusers/参考 pipeline 的新扩散模型接入 SGLang 的 pipeline/stage/model/config 结构 |
| 扩散性能调优 | [`sglang-diffusion-performance`](https://github.com/sgl-project/sglang/tree/main/python/sglang/multimodal_gen/.claude/skills/sglang-diffusion-performance) | 选择 `torch.compile`、预热、SP/CFG 并行、offload、注意力后端和量化等性能设置 |
| 生产事故分诊 | [`sglang-prod-incident-triage`](https://github.com/sgl-project/sglang/tree/main/.claude/skills/sglang-prod-incident-triage) | 采集在线服务器的诊断包、保存失败请求并重放，然后分流到聚焦的崩溃/挂起/剖析工具 |
| SGLang 评审 / PR 历史 | [`sglang-humanize-review`](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/skills/sglang-humanize-review) 与 [`model-pr-history-knowledge`](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/model-pr-optimization-history) | 参照真实维护者的讨论模式评审 SGLang 补丁，并让 PR 驱动的模型演进历史与被改动的源码保持关联 |
| SGLang SOTA 性能循环（循环工程） | [`sglang-sota-humanize-loop`](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/skills/sglang-sota-humanize-loop) | 先让 SGLang 与指定的开源推理框架进行公平对比，再把差距判定、剖析、打补丁和复验纳入 Humanize/RLCR 循环 |

这些条目把容易遗漏的步骤变成可执行的协议，让工作流跑得起来、断点可续、结果可评审。

### 3.2 近期优化与工作流示例

以下示例来自近期合并的 SGLang PR。表格关注完整的工程路径：基准测试、剖析、问题定位、代码改动、测试和复验。

| 案例 | 结果 | 关键点 |
| --- | --- | --- |
| 路由器长上下文分词去重，[SGLang PR #28744](https://github.com/sgl-project/sglang/pull/28744) | 在一个 DeepSeek-V4-Flash 部署中，空闲负载下 60k/125k token 提示词的首 token 延迟（TTFT）分别下降约 `29%` / `41%`；在 60k token 负载下，TTFT 下降 `34%–49%` | 智能体一并处理了缓存感知路由、chat-encoder 一致性、引擎侧 `input_ids` 回退和代理请求体构建，避免了路由器和引擎中的重复分词 |
| Qwen3-Next FlashInfer allreduce 融合，[SGLang PR #22664](https://github.com/sgl-project/sglang/pull/22664) | 在 H100 TP=4 上，请求吞吐量从 `5.49 req/s` 提升到 `9.41 req/s`，约 `+71.4%`；平均 TTFT 从 `456.24 ms` 降到 `167.54 ms` | 这是一次剖析驱动的 LLM 集合通信优化：未融合的跨设备归约（reduce）主导了预填充阶段，融合后的 allreduce 路径通过了 MMLU/GSM8K 精度校验 |
| Cohere2Moe NVFP4 融合 MoE 路径，[SGLang PR #27401](https://github.com/sgl-project/sglang/pull/27401) | 对 1x B300 上的 `CohereLabs/command-a-plus-05-2026-w4a4`，请求吞吐量较此前的 SGLang 默认配置在 chat 上提升 `+26%`、summarization 上提升 `+21%`，并在该设置下领先另一开源推理框架 `+4.1%` / `+6.8%` | 该改动补全了路由语义，使现有的 `flashinfer_trtllm` NVFP4 融合 MoE 内核能够在真实模型路径中被正确使用，并通过 GSM8K/MMLU 校验 |
| SM100 上的 Kimi Delta Attention CuteDSL 预填充内核，[SGLang PR #27488](https://github.com/sgl-project/sglang/pull/27488) | 对 `moonshotai/Kimi-Linear-48B-A3B-Instruct`，B200 上的 Delta Attention 预填充比 Triton 快 `1.08x–1.52x`；GSM8K 从 `0.915` 变为 `0.920`，并新增了针对真实门控幅值的回归测试 | 这个内核任务必须覆盖模型的门控分布、数值溢出、主机开销、真实模型精度和单元测试，优化才算达到可合并状态 |
| Spectral Progressive Diffusion，[SGLang PR #27524](https://github.com/sgl-project/sglang/pull/27524) | 在报告的 RTX A6000 设置下，FLUX.1、FLUX.2、Z-Image、Wan 和 Qwen-Image 的去噪加速比分别达到 `1.63x`、`1.77x`、`2.07x`、`2.32x` 和 `1.6x` | 这是一项扩散侧的系统优化：早期去噪在较低的潜在分辨率上运行，当高频细节开始起作用时，再由 GPU DCT 上采样恢复完整分辨率 |
| LTX-2 VAE 解码 channels-last-3d，[SGLang PR #27431](https://github.com/sgl-project/sglang/pull/27431) | LTX-2 解码阶段从 `5.41 s` 缩短到 `3.84 s`，约 `1.41x`；峰值预留显存从 `71.81 GiB` 降到 `62.12 GiB`，节省约 `9.7 GiB` | 剖析结果指向 Conv3d 和布局转换，因此修复在因果填充（causal padding）中保留了内存格式，并把加载器策略与单卡 LTX-2 关联起来 |

在这些示例中，智能体的主要贡献在于执行工作流：跑基准测试、读剖析结果、定位 Python 源码、改代码、补测试、复验以及准备 PR 描述。没有技能时，许多步骤靠人工提醒；一旦编码为技能，工作流就容易重复得多。

## 4. 剖析、评审与循环工程

SGLang 性能工作中一个常见错误，是只看总运行时间，或者打开 Perfetto 看几分钟，就凭直觉断定某个东西「应该被融合」。对智能体来说这更危险，因为它们很容易把视觉上「热」的内核误当成真正的瓶颈。

实践中通常把两个剖析类技能配合使用。`llm-torch-profiler-analysis` 负责第一层 trace 分诊，把一次全局剖析变成三张固定表格：

- `Kernel Table`（内核表）：按阶段汇总 GPU 时间占比、启动次数和内核类别，并尽可能把内核映射回 Python 源码和 CPU 算子。
- `Overlap Opportunity Table`（重叠机会表）：用独占/被隐藏时间占比、依赖风险和内核类别，找出尚存的重叠或优化空间。
- `Fuse Pattern Table`（融合模式表）：把 trace 与一个有源码依据的模式目录对比，目录覆盖 SGLang、其他开源推理框架和内核库中的融合/重叠路径。

这些表格回答第一层问题：哪个阶段、哪个内核占了多少 GPU 时间，对应到哪一行 Python 代码，以及是否已有可以借鉴的融合/重叠路径。如果 SGLang 落后于另一个推理框架，应当先让剖析表格解释差距，再开始任何代码改动。

下一步是 `llm-pipeline-analysis`。知道全局热点之后，还需要知道它们属于哪次前向传播、哪类层、哪条内核流。该技能读取 Chrome trace JSON 和模型 `config.json`，用层边界锚点内核把 trace 切分成前向传播和层，然后产出几张用于深入分析的表格：

- `Forward pass summary`（前向传播摘要）：把冷启动和稳态分开，避免把预热当成优化目标。
- `Per-layer timeline`（逐层时间线）：报告每层的墙钟时间、时长总和，以及 MLA、MoE、GEMM、NCCL、MHC、Hadamard 等类别各自的占比。
- `Layer cluster statistics`（层簇统计）：对层结构交替出现的模型尤其有用，例如带 `compress_ratios` 的 NSA/混合注意力模型，其中 C4_LIGHT、C128_HEAVY、HASH 或其他层类型可能主导延迟。
- `Compute flow table`（计算流表）：把代表性层展开为具体的内核流，附带上榜热度（hotness）、相对时间戳和输入维度，便于随时跳回 Perfetto。

于是，剖析分析变成一个两步过程。第一步，`llm-torch-profiler-analysis` 在完整 trace 中找出主要矛盾；第二步，`llm-pipeline-analysis` 把问题落到稳态前向传播、代表性层和具体内核流上。第一步避免凭直觉选方向，第二步避免盯着某个全局热点内核，却看不到模型结构中的层类型差异。

### 4.1 Humanize/RLCR：为循环增加外部评审

Humanize 解决的是长时任务中的状态与评审问题。一个高风险的 SGLang 性能任务通常不会一轮实现就完成，可能要经历多轮基准测试、剖析、打补丁、回退、换方向和再次验证。Humanize 把这一过程拆成两个阶段：

1. 先跑 gen-plan。`humanize-gen-plan` 把一份需求草稿变成结构化的 `plan.md`，内容包括目标描述、验收标准、正/反例测试、路径边界、里程碑和实现备注。
2. 接着跑 RLCR 循环。`humanize-rlcr` 从 `plan.md` 启动循环。每一轮中，Claude Code 读取 `.humanize/rlcr/<timestamp>/round-<N>-prompt.md`，进行实现、提交并写一份小结；Codex Review 随后检查状态文件、小结、git 干净状态、评审结果、遗留问题、最大迭代条件等门禁。只凭一句「任务完成」不足以退出循环。

这一机制为 SGLang SOTA 性能循环提供了执行与评审的基础。Claude Code 负责跑基准测试、读剖析结果、改 SGLang 代码并复验；Codex Review 在每轮结束时检查证据、状态和风险。它很适合那些要变成 PR、会影响服务正确性、或者需要连续多日多轮实验的任务。

实践中应当把命令顺序写明确，避免智能体直接跳进实现：

```text
1. Write a task draft under artifact_root/draft.md.
2. Run humanize-gen-plan to generate artifact_root/plan.md.
3. Start humanize-rlcr from artifact_root/plan.md.
4. Keep all decisions, summaries, and review state in the local Humanize workspace.
```

### 4.2 SGLang SOTA 性能循环（循环工程）

单个技能能稳住一个任务。但十几轮实验之后，另一个问题出现了：哪个候选最好、哪些方向已经失败、上一次 NCU 报告显示了什么、基准测试是否还与基线一致、什么时候该停。这种状态不能只存在于聊天上下文里。

SGLang SOTA 性能循环是构建在 Humanize/RLCR 之上的循环工程工作流。这里的 SOTA 指固定实验条件下最佳的可复现结果：相同的模型、硬件、GPU 数量、精度、负载、SLA、框架 commit 和服务参数。要回答的问题是：SGLang 能否在这些条件下达到当前最佳的可复现结果。

![SGLang SOTA Performance Loop](/images/blog/agent-assisted-sglang-development/sglang-sota-performance-loop.svg)

图 1：SGLang SOTA 性能循环。先由固定的公平基准测试建立可复现基线，随后的差距判定、剖析、流水线分析、打补丁和复验都由 Humanize/RLCR 循环驱动。

一个完整的 SGLang SOTA 性能循环包含以下阶段：

1. 定义目标边界。例如 `Qwen/Qwen3-Next-80B-A3B-Instruct-FP8`、单节点 2x B200、FP8、SGLang TP=2，并在相同的 2 卡预算下与指定的开源推理框架对比。
2. 先做公平搜索。在给 SGLang 打补丁之前，先在相同负载和资源预算下，为 SGLang 和每个指定的开源推理框架搜索各自最佳的可复现命令。
3. 判定差距。如果 SGLang 已经持平或领先，记录完成证据；如果持续落后超过阈值，进入剖析阶段。
4. 用剖析解释差距。不要急着改代码，先产出内核表、流水线表、重叠/融合表，必要时再出 NCU 报告。
5. 只对有证据支撑的路径打补丁，例如混合注意力（hybrid attention）、Mamba/GDN、基数树缓存（radix cache）、目标模型验证（target verify）、CUDA 图、MoE/EP、量化内核或模型封装层。
6. 在同一负载上复验。每一轮都记录基准测试、剖析、精度、失败尝试、环境信息和清理动作。

对 `Qwen/Qwen3-Next-80B-A3B-Instruct-FP8` on 2x B200 这样的目标来说，循环之所以重要，是因为基准测试结果、剖析 trace、失败补丁和中间结论都需要始终挂靠在相同的模型、硬件、负载和框架 commit 上。如果这类任务被拆成许多互相独立的 prompt，很容易搞不清哪条命令产出了哪个结果、后来某次剖析是否还与最初的基线匹配。带证据和评审的循环能让各轮条件保持一致。

### 4.3 Codex Goal：更低成本的循环实现

上面的 SGLang SOTA 性能循环采用双角色设置：Claude Code 负责执行基准测试、剖析、打补丁和复验，Codex Review 在每轮结束时做检查。这一设置适合严肃的 PR 工作，但每一轮都要同时消耗一个执行模型和一个评审模型，推高成本和等待时间。

Codex Goal 提供了另一种实现。一旦把「公平基准测试 -> 差距判定 -> 剖析 -> 打补丁 -> 复验 -> 产物台账」写进一个持久化的 Goal，单个 Codex Goal 就能同时承担执行、自检和复验，不再需要执行/评审双角色设置。SGLang SOTA 性能循环的核心约束保持不变：固定负载、证据驱动的补丁、相同实验条件下的复验，以及每轮之后更新产物清单。

两种方式的差异如下：

| 维度 | Humanize/RLCR SOTA 循环 | Codex Goal |
| --- | --- | --- |
| 执行 | Claude Code 负责实现和实验；Codex Review 评审每一轮 | 单个 Codex Goal 持续执行、自检并复验 |
| 状态存放 | `.humanize/rlcr/...` 下的 plan、prompt、小结和评审结果 | 当前 Goal 线程，加上 `artifact_root` 下的清单/证据 |
| 评审方式 | Stop hook、Codex Review，以及 git/状态/schema 检查 | Goal 级自检、产物契约，以及人工抽查 |
| 成本 | 两个模型角色参与，每轮成本更高 | 一个 Goal 兼顾执行与检查，成本更低 |
| 主要风险 | 循环设置更复杂，每轮等待时间更长 | 若硬停止条件不明确，可能出现目标漂移或提前收工 |

下面是来自 [AI-Infra-Auto-Driven-SKILLS/prompts](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/prompts) 的一个 2x B200 模型优化 prompt 示例。

Humanize/RLCR 版本：

```text
Use the sglang-sota-humanize-loop workflow.

Task:
Optimize SGLang serving performance for Qwen/Qwen3-Next-80B-A3B-Instruct-FP8
on a single node with 2 NVIDIA B200 GPUs, FP8 precision, and initial SGLang
TP=2. SGLang should match or exceed the best reproducible result from the
requested open-source inference frameworks under the same 2-GPU budget, workload, SLA,
model, precision, and environment constraints.

Required workflow:
1. Create a draft task document under artifact_root.
2. Run humanize-gen-plan to turn the draft into a structured plan.md.
3. Start humanize-rlcr from that plan.md in the Claude Code session.
4. Keep benchmark, profile, patch, and revalidation decisions inside the same
   Humanize workspace.

Evidence and safety requirements:
- Before patching, run a fair bounded search for SGLang and the requested open-source inference framework set.
- Check relevant open PRs in sgl-project/sglang and BBuf/sglang before choosing
  the SGLang baseline.
- If SGLang is behind by more than 1%, profile before patching.
- Prioritize evidence around hybrid attention, Mamba/GDN, radix cache, target
  verify, and CUDA graph.
- Record benchmark commands, profile artifacts, failed attempts, and cleanup
  evidence for every round.
- Patch only evidence-supported SGLang code paths.
- If a PR is needed, push/open it only against BBuf/sglang and include benchmark,
  GSM8K, and full MMLU accuracy tables.

artifact_root:
/workspace/sglang-agent-artifacts/b200_qwen3_next_80b_a3b_instruct_fp8_sota_humanize
```

Codex Goal 版本：

```text
/goal Keep optimizing SGLang serving for
`Qwen/Qwen3-Next-80B-A3B-Instruct-FP8` on a single node with 2 NVIDIA B200
GPUs until SGLang matches or exceeds the best reproducible result from the
requested open-source inference frameworks under the same 2-GPU budget, FP8 precision,
workload, SLA, model, and environment constraints. The current Codex Goal is the loop: fixed fair
benchmarking, gap decision, profiling, pipeline analysis, evidence-backed
patching, revalidation, final report, and optional PR preparation all happen
inside this Goal. Completion requires benchmark evidence, profile evidence when
SGLang was behind, correctness/accuracy evidence, a final artifact manifest,
and no regression in environment safety constraints.

model_id: Qwen/Qwen3-Next-80B-A3B-Instruct-FP8
root_dir: /workspace
target_hardware: single-node 2x NVIDIA B200
minimum_gpu_count: 2
precision_quantization: FP8
initial_deployment: SGLang TP=2
artifact_root:
/workspace/sglang-agent-artifacts/b200_qwen3_next_80b_a3b_instruct_fp8_sota_goal

Requirements:
- Use the current Codex Goal as the only persistent loop.
- Before patching, run a fair bounded search for SGLang and the requested
  open-source inference frameworks under the same 2-GPU budget.
- If SGLang is behind by more than 1%, profile in the same Goal, then use
  llm-torch-profiler-analysis, llm-pipeline-analysis, and ncu-report-skill when
  needed before patching.
- Focus on hybrid attention, Mamba/GDN, radix cache, target verify, and CUDA graph.
- Update the artifact manifest, benchmark evidence, profile evidence, failed
  attempts, and next-step decision after every round.
- Stop and report a blocker if resources are unavailable, evidence is
  untrustworthy, the budget is exhausted, or no defensible next patch exists.
```

Goal 版本保留了同样的基准测试、剖析、精度和产物要求，区别在于执行和评审被折叠进同一个持久化目标。只要硬停止条件足够明确，它就能以更少的编排承担同一个 SGLang SOTA 性能循环。

## 5. 基于 KDA 的 SGLang 系统 CUDA 内核优化

在 LLM 和扩散模型的模型级优化之外，内核优化面临更严酷的扩展问题。不存在独立于硬件和负载的「唯一最优内核」。同一个算子在 H100、H200、B200 或 B300 上可能各有偏好的实现；不同模型架构暴露出不同的张量形状和布局约束；服务负载又改变 batch 大小、序列长度、精度格式、封装开销、同步行为和回退路径。实际上，搜索空间是硬件、模型和负载定义三者的笛卡尔积。

这带来了组合爆炸式的优化负担。对每个候选内核，开发者都需要提取有代表性的生产负载行（production rows）、搭建同 ABI 的执行框架（harness）、做 A/B 测量、在各个形状分桶（shape bucket）上检查正确性、读 NCU 指标、判断某个分桶是否值得做特化，然后在真实 SGLang 路径中复验。对每个硬件/模型/负载组合都手工做一遍，代价极高。而这恰恰是智能体擅长的那种重复性、重证据的工作流——前提是人来定义不变量并评审最终路径。

但如果直接让智能体去写 CUDA，很容易导致基准测试奖励作弊（reward hacking）：改基准本身、用更轻量的封装路径、开启基线没有使用的 fast math、只优化一个形状、破坏数值语义，或者在真实 SGLang 路径中毫无收益。

KDA-Pilot 把内核优化拆成相互隔离的任务，避免智能体随意修改整个 SGLang 仓库：

- 负载来自真实的 SGLang 扩散模型。流程会先运行 20 个扩散模型，汇总实际的内核元数据。
- 基线从上游 SGLang main 复制而来，并记录源码谱系。
- 基线和候选必须使用相同的本地 ABI 和相同的构建/导出路径。
- 基准测试使用固定的生产负载行、A/B 交错测量，以及 CUDA event 或墙钟计时。
- 正确性覆盖生产负载行、标准回归网格、NaN/Inf 检查、输出毒化（poison output）检查和回退契约。
- 每次迭代都会刷新任务 prompt、基准测试证据、KernelWiki 和 ncu-report-skill。
- 允许按形状特化的分发（dispatch），但每个分桶必须写明自己的触发条件、路径、延迟和回退。

一个具体的快照可以让人更容易感受规模。公开的 KDA-Pilot B200 扩散汇总目前列有 10 个在跟踪的 SGLang 内核任务。其中大多数数据行在 KDA-Pilot 台账中有稳定的 B200 数字证据，在提取出的生产负载行上，墙钟几何平均加速比（wall-geomean speedup）介于 `1.1341x` 到 `2.7499x` 之间。`residual_gate_add` 一行标为 `1.11x`，与已合并的上游 LTX-2.3 B200 结果一致。

截至 2026 年 6 月 27 日，已有三项源自 KDA-Pilot 的优化进入 SGLang 上游。第一项是 [SGLang PR #27392](https://github.com/sgl-project/sglang/pull/27392)，为 Qwen-Image-2512 提供 B200 原生扩散 norm-scale-shift CUDA 快速路径。同一周晚些时候又合并了两项：[SGLang PR #29281](https://github.com/sgl-project/sglang/pull/29281)（Cosmos3 VAE 因果 Conv3D cat/pad 拷贝路径）和 [SGLang PR #29361](https://github.com/sgl-project/sglang/pull/29361)（LTX-2.3 残差门控更新路径）。

| 上游 PR | 目标路径 | 内核级证据 | 模型路径级证据 |
| --- | --- | --- | --- |
| [#27392](https://github.com/sgl-project/sglang/pull/27392) | Qwen-Image norm-scale-shift | 目标内核组在剖析归因中提升 `1.279x` | 在单张 B200 上，双方各跑五次交错测试，完整请求加速比为 `1.125x`，去噪墙钟加速比为 `1.130x` |
| [#29281](https://github.com/sgl-project/sglang/pull/29281) | Cosmos3 因果 Conv3D cat/pad | 在被追踪的 VAE 解码调用中，B200 加权内核组从 `10.621 ms` 降到 `5.240 ms`，即 `2.03x` | 在 Cosmos3-Nano T2V 上开启 `torch.compile` 后，E2E 中位时间从 `181.521 ms` 降到 `177.687 ms`，即 `1.021x` |
| [#29361](https://github.com/sgl-project/sglang/pull/29361) | LTX-2.3 残差门控更新 | B200 上较大的 LTX-2.3 数据行相比现有 Triton 路径提升 `1.108x` 至 `1.130x`，相邻扩散数据行最高达 `2.587x` | 在 LTX-2.3 HQ T2V 上，E2E 时间从 `46644.08 ms` 降到 `45198.37 ms`，即 `1.032x` |

关键结论不是「每个独立内核的收益都能变成很大的端到端收益」，而是：同一套 KDA-Pilot 证据包——固定的生产负载行、正确性门禁、同 ABI 对比、剖析归因和真实模型校验——能把一个内核任务从孤立的基准测试推进到可评审的 SGLang 服务路径中。

![KDA-Pilot B200 diffusion kernel results](/images/blog/agent-assisted-sglang-development/kda-pilot-b200-speedups.svg)

图 2：KDA-Pilot 优化的 10 个在跟踪 SGLang 扩散内核任务的 B200 证据。大多数数据行报告 KDA-Pilot 墙钟几何平均加速比；墙钟时间包含 Python 分发、封装开销、内核启动以及通过 `cuda.synchronize()` 可见的同步开销，比纯内核设备时间更接近真实调用路径。

| 内核任务 | B200 证据 | 主要优化方向 |
| --- | ---: | --- |
| `qknorm_rope` | `1.1341x` | 共享 RoPE 暂存（staging）、Q/K 复用、大行快速路径 |
| `norm_infer` | `1.3523x` | 按 warp 行的 RMS、分块持久化 RMS、8B/16B 向量路径 |
| `rotary_embedding` | `1.4912x` | 128 位向量 I/O、cos/sin 外提、LTX2 分块匹配 |
| `cutedsl_norm_tanh_mul_add` | `1.4953x` | 行不变数学外提、launch-bounds 调优、精确 tanh |
| `cutedsl_norm_scale_shift` | `1.3201x` | 按操作数类别分发、16B/32B 向量化、两遍方差 |
| `fuse_scale_shift` | `2.7499x` | rowgrid/flatvec/exact-C 路径、缓存提示、单遍归约 |
| `group_norm_silu` | `2.3118x` | 分组统计拆分、channels-last 直达路径、超大行回退 |
| `attention_concat_copy` | `1.30x` | 单次启动的区域拷贝、16B 对齐分块 gather、严格的布局/设备拒绝 |
| `causal_conv3d_cat_pad` | `2.06x` | 扁平分块、16B 向量化写入、步长感知回退、逐位精确门禁 |
| `residual_gate_add` | `1.11x` | 单遍 CUDA 融合、指定 GPU 上的正确性验证、SGLang PR #29361 的 B200 Triton 行复测 |

阅读图表和任务表时要结合实验设定：它们报告的是在提取出的生产负载行上的内核任务加速比，而不是完整模型的端到端收益。这些数字仍然有用——一旦基线、负载、正确性、剖析和评审都固定下来，智能体就能在真实的框架内核上产出可评审的增量改进。

KDA-Pilot 实验中有两条规则值得铭记：

- 不要给基准测试奖励作弊留任何空间。当基线和候选使用不同 ABI、不同 fast math 设置或不同封装路径时，结果就不可信了。另一个常见问题是在看到结果之后再修改基准形状集合，比如删掉候选更慢的形状。这样的结果不应采用。
- 对已接近 Roofline 的分桶，应当允许做出放弃（no-go）或回退的决策。一个好的内核优化任务不应强迫智能体赢下每一个形状。对于巨大的连续分桶或已接近带宽极限的路径，记录一个回退方案可能比增加更多复杂度更好。

## 6. 实践规则

1. 在启动智能体之前先定义任务边界。
「优化 SGLang」太宽泛；「在 2x B200 上、固定 `1000->1000` 和 `8000->1000` 负载下，让 SGLang 为 `Qwen/Qwen3-Next-80B-A3B-Instruct-FP8` 追平另一个开源推理框架」才是可执行的目标。

2. 读剖析之前先固定基准测试。
如果看完结果之后负载还能改，智能体可能会不知不觉去优化一个更容易的问题。SOTA 循环和 KDA-Pilot 都把固定负载放在打补丁之前。

3. 按内核的计算特征解读 NCU 结果。
对访存受限（memory-bound）内核，关注 DRAM/L2 吞吐、load/store 效率和内存管线利用率；对计算受限的 GEMM/注意力内核，关注 Tensor Core 利用率、SM 忙碌度（SM busy）、合格 warp 数（eligible warps）和主要停顿原因；对小而受延迟限制的内核，检查启动次数、单个内核耗时、同步点和可能的融合机会。单张 trace 截图不够，下一次代码改动应当有具体指标支撑。

4. 信任剖析之前先检查后端与回退门禁。
如果一次 LLM 运行静默切换了注意力后端、禁用了 CUDA 图，或走了与基准测试时不同的封装路径，这条 trace 就不再描述目标服务路径。扩散模型同理：如果日志显示回退到了 diffusers 后端，这条 trace 就不能作为 SGLang 原生扩散的证据。这些硬停止条件应当写进技能里。

5. 内核优化必须使用相同的 ABI、封装和编译 flag。
尤其不能让候选悄悄走上更轻量的路径，也不应只在单侧开启 `--use_fast_math`。

6. 评审比以往更重要。
智能体能产出更多 PR，也会制造更多看似合理的错误。对 SGLang 这样的高性能系统，评审需要检查形状、dtype、分布式执行、CUDA 图行为、回退行为、精度、服务 API、指标和基准测试设置。

Agent 时代的 SGLang 开发并不会把开发者从系统中移除。更现实的变化是：把开发者经验写进工作流，把重复性执行交给智能体，把判断、设计和评审留给人。省下来的时间可以投入到更难的性能问题、模型路径和生产稳定性上，或者反过来继续打磨智能体工作流本身。对一个开源推理框架来说，这类基础设施值得持续投入。

## 7. 致谢

我们感谢帮助构建 SGLang 智能体技能的 SGLang Team 成员和贡献者：Xiaoyu Zhang (BBuf)、Lianmin Zheng、Liangsheng Yin、Ke Bao、fzyzcjy、Kangyan Zhou、DarkSharpness、Mick、Alison Shao、Baizhou Zhang、Bingxu Chen、Cheng Wan、Ratish P、shuwenn、ykcai-daniel、Yuhao Yang 和 Artem Savkin。

我们感谢 KDA 团队：Dongyun Zou、Ligeng Zhu、Sihao Liu、Junxian Guo、Yixin Dong、Zijian Zhang、Hao Kang 和 Song Bian。

我们感谢 Humanize 团队及其贡献者：Sihao Liu、Ligeng Zhu、Zijian Zhang、Zenus Zhang、shinan6、DYZhang、Chao Liu、Zhou Yaoyang、gyy0592、AcrossForest、Emin、Qiming Chu、jiaxiaoyu、tastynoob 和 zhenwei。

## 8. 参考资料

- [SGLang GitHub 仓库](https://github.com/sgl-project/sglang)
- [SGLang `.claude/skills`](https://github.com/sgl-project/sglang/tree/main/.claude/skills)
- [SGLang diffusion `.claude/skills`](https://github.com/sgl-project/sglang/tree/main/python/sglang/multimodal_gen/.claude/skills)
- [AI-Infra-Auto-Driven-SKILLS](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS)
- [AI-Infra-Auto-Driven-SKILLS prompts](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS/tree/main/prompts)
- [Kernel Design Agents (KDA)](https://github.com/mit-han-lab/kernel-design-agents)
- [KernelWiki skill](https://github.com/mit-han-lab/KernelWiki)
- [ncu-report-skill](https://github.com/DongyunZou/ncu-report-skill)
- [KDA-Pilot](https://github.com/BBuf/KDA-Pilot)
- [SGLang Diffusion Advanced Optimizations（LMSYS 博客）](https://lmsys.org/blog/2026-02-16-sglang-diffusion-advanced-optimizations/)
- [OpenAI Codex Prompting: Goal mode](https://developers.openai.com/codex/prompting#goal-mode)
- [Humanize](https://github.com/PolyArch/humanize)

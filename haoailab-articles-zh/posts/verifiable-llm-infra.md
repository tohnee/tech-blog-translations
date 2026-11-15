---
title: "迈向可验证的 LLM 基础设施"
title_en: "Towards Verifiable LLM Infra"
date: 2026-11-10
source: https://haoailab.com/blogs/verifiable-llm-infra/
crawled: 2026-11-16
translated: 2026-11-16
---

# 迈向可验证的 LLM 基础设施

> 原文：[Towards Verifiable LLM Infra](https://haoailab.com/blogs/verifiable-llm-infra/) · Hao AI Lab @ UCSD

# 迈向可验证的 LLM 基础设施

2026 年 11 月 10 日 · 12 分钟 · Yuxuan Zhang、Minshen Zhang、Junda Su、Yi Sun、Junda Chen、Hao Zhang

[![GitHub: vstack](https://img.shields.io/badge/GitHub-vstack-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hao-ai-lab/vstack)[![GitHub: veriserve](https://img.shields.io/badge/GitHub-veriserve-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hao-ai-lab/veriserve)[![X: @haoailab](https://img.shields.io/badge/Follow-@haoailab-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/haoailab)

[![
](img/poster.png)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/verifiable-llm-infra--img--overview.mp4)

编程智能体在编写 LLM 基础设施方面正变得相当出色——从 GPU kernel、调度器到定制的推理服务引擎。假设一个 AI 智能体已经足够强，能从零构建一个快速的推理引擎；那么在这个问题的[后半程](https://ysymyth.github.io/The-Second-Half/)，瓶颈就从能力转向了**验证**：我们怎么知道它写的引擎真的正确？通过延迟和吞吐基准测试，仍然会把罕见的并发 bug 藏在里面。当单个工程师开始并行调度 100、1,000 甚至 10,000 个编程智能体时，人工代码评审会撞上认知的硬墙。让智能体去评审其他智能体也解决不了这个问题；正如 [`pstack`](https://github.com/cursor/plugins/tree/main/pstack) 作者 [Lauren Tan 指出的](https://x.com/poteto/status/2117437607940681849)，对抗式评审大多是在浪费 token，把这些 token 花在经验验证与形式化验证上要好得多。

在这篇博客中，我们介绍 [**`vstack`**](https://github.com/hao-ai-lab/vstack)——一套面向编程智能体的五阶段形式化验证工作流；以及 [**`veriserve`**](https://github.com/hao-ai-lab/veriserve)——一个**可验证的 LLM 推理服务引擎**原型，它带有 PD 分离（prefill-decode disaggregation），并围绕一个经过形式化验证的 KV page 生命周期设计模型构建。我们把 `vstack` 用于生产级的 Prefill-Decode 服务，在 SGLang 与 vLLM 中发现了三类真实的 RDMA 与缓存并发 bug，并**提出了 6 个上游 pull request**。与此同时，`veriserve` 为其 `PdLedger` 设计模型提供了一份 **226 个模块、516,973 条证明义务的 [`TLAPS`](https://proofs.tlapl.us/) 安全性证明**，而在 NVIDIA GB200 上只带来了 **`0.18%` 的平均 p50 `TPOT` 开销**。**我们认为，当自主编程智能体开始编写生产系统最深的那些层时，可验证服务将定义 LLM 基础设施的后半程。**

---

## 为什么我们需要可验证服务[#](#why-we-need-verifiable-serving)

验证一个 LLM 服务引擎到底难在哪里？过去三年，[vLLM](https://github.com/vllm-project/vllm) 和 [SGLang](https://github.com/sgl-project/sglang) 这样的推理引擎已经从单节点执行器演化成了异步分布式系统，在同一个物理 GPU KV page 池之上叠加了[**分页 KV 内存**](https://arxiv.org/abs/2309.06180)、[**共享前缀缓存**](https://proceedings.neurips.cc/paper_files/paper/2024/hash/724be4472168f31ba1c9ac630f15dec8-Abstract-Conference.html)和[**分离式 prefill-decode RDMA 传输**](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)。当一个请求超时或被中止时，它的清理工作现在要同时在 RDMA 网卡、CPU 缓存树和 GPU attention kernel 上竞争。由于 [GPUDirect RDMA](https://docs.nvidia.com/cuda/gpudirect-rdma/) 会绕过目标 CPU 直接写入 GPU 显存，生命周期不匹配往往不会让服务器崩溃，而是返回 `HTTP 200 OK`，同时悄悄把一个用户的 KV cache 混进另一个用户的响应。近期 [LMSYS](https://www.lmsys.org/blog/2026-10-26-cf-security/) 和 [Cloudflare](https://blog.cloudflare.com/kv-cache-exposure-remediation/) 的披露在生产环境中印证了这一风险，记录了跨节点 RDMA 中止竞争，以及一个被拒绝请求的 KV 交接 bug——它让数据泄露在 **155 个用户响应**中。

更糟的是，**在真实硬件上捕捉这些静默的并发 bug 既慢又昂贵得令人却步**。标准的 CI 单元测试跑在单机上，只覆盖已知路径；而由罕见异步交错引发的细微分布式竞争极少在 CI 中浮现。要复现一个 RDMA 生命周期竞争，需要 H100 或 GB200 这样的多 GPU RDMA 硬件、独立的 prefill 与 decode 实例，以及精确的跨 worker 时序。用 GPU 集群上的长时间压力测试把它们冲出来，既消耗稀缺算力，又依然无法保证所有竞争条件都已消失。

为了在不烧 GPU 工时的前提下抓住这些深层并发 bug，我们转向**形式化验证**：把系统建模成状态机，把 `TLA+` 模型检查与 [`Z3`](https://github.com/Z3Prover/z3)、[`TLAPS`](https://proofs.tlapl.us/) 定理证明器结合起来，在 CPU 上穷尽探索数百万种异步调度并证明安全性不变量。过去，形式化验证对 AI 基础设施并不实用，因为 vLLM 和 SGLang 这样的引擎在持续合入新的 pull request，而手工编写和更新形式化规约与证明需要数月的人力。**今天，编程智能体给了我们弥合这一差距的实用途径。** 由于 LLM 能阅读大型系统代码库，并以远超人工证明工程的速度生成数千行形式化规约与证明，我们可以引导编程智能体去规约、模型检查和证明关键子系统，使**可验证服务**在快速演进的开源项目中变得可行。

---

## 我们如何验证：用 `vstack` 做形式化验证[#](#how-we-verify-formal-verification-with-vstack)

要把智能体驱动的形式化验证变成可靠的工作流，需要先解决两个直接挑战。第一，形式化验证最难的部分不是运行求解器，而是写出准确的**规约（Specification）**：一条软件在任何异步调度下都绝不能违反的需求。多亏了开源的 [vLLM](https://github.com/vllm-project/vllm) 和 [SGLang](https://github.com/sgl-project/sglang)，我们不必凭空发明这些需求，而是把它们直接锚定在真实的用户 issue、修复 PR 和 GPU kernel 前置条件上。

第二，即使规约清晰，简单地要求编程智能体写一个形式化模型并证明它，很少一次成功。当模型检查器报告一个竞争条件时，**天真的编程智能体会经常对验证器做 reward hacking**：它不去暴露真正的 bug，而是削弱不变量、从模型里删掉超时分支，或者加一条不现实的 `ASSUME` 语句，让检查器返回 `0 errors`。

![vstack 的五阶段验证工作流](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/verifiable-llm-infra--img--fig1.gif)

图 1. 五阶段的 vstack 验证工作流。常见的智能体 reward hacking——削弱规则、删除超时分支、用假设把竞争消掉——都会被钉死的规约、保真检查和证明门禁挡住，直到真正的修复通过。

为了防止 reward hacking、让智能体驱动的验证变得可靠，我们构建了 [**`vstack`**](https://github.com/hao-ai-lab/vstack)：一个面向 Claude Code 和 Cursor 的开源插件，强制执行**五阶段验证工作流**：

1. **`Specification`（规约）：** 把软件需求编码为形式化的安全性不变量，并按哈希钉死规约文件，这样对证明目标的未授权修改会被检测并拒绝。
2. **`Abstraction`（抽象）：** 构建 `TLA+` 与 `Z3` 模型，使每个状态迁移都精确映射到生产代码库中的 `file:line@commit`，并把非原子的跨线程、跨节点操作拆成独立步骤。
3. **`Validation`（校验）：** 在信任任何证明之前，先验证模型对真实代码的保真度：历史上出过 bug 的代码必须在模型上失败，打补丁后的代码必须通过，从修复中移除某个保护后必须在非冗余变异检查下再次失败，并且记录下来的执行轨迹必须能在模型中干净重放。
4. **`Verification`（验证）：** 运行 [`TLC`](https://docs.tlapl.us/using:tlc:start) 广度优先搜索，在有界模型内找到最短的反例轨迹；然后用 [`Apalache`](https://apalache-mc.org/)、[`Z3`](https://github.com/Z3Prover/z3) 和 [`TLAPS`](https://proofs.tlapl.us/) 证明被建模的状态机与 GPU KV buffer 地址算术在我们显式的配置假设下成立。
5. **`Continuous Checking`（持续检查）：** 在 CPU 上对所有新 pull request 重跑规约套件，并把被证明的前置条件镜像为引擎中的轻量运行时检查。

---

## 案例研究：形式化验证 Prefill-Decode 分离式服务[#](#case-study-formally-verifying-prefill-decode-disaggregated-serving)

作为原型，我们把 `vstack` 用于 **Prefill-Decode 分离式服务**：一个 Prefill 节点计算提示词的 KV cache，并通过单边 RDMA 把它传给一个共享缓存前缀、运行 Decode attention kernel 的 Decode 节点，如**图 2** 所示。针对这个核心 KV page 子系统，我们定义了**四条规约**：

![分离式 Prefill-Decode RDMA 下的静默 KV 损坏](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/verifiable-llm-infra--img--fig2.gif)

图 2. 分离式 Prefill-Decode RDMA 下的静默 KV 损坏。如果 Decode 在本地超时时回收了请求 A 的 GPU page 并把它分给请求 B，而 Prefill 的单边 RDMA 写入仍在传输中，那么 A 迟到的 payload 会覆盖 B 的 KV page，而服务器仍然返回 HTTP 200。

1. **`Isolation`（隔离）：** 旧请求在途的 RDMA 传输或迟到的控制消息，绝不能读取或覆盖新请求的内存或状态。
2. **`Integrity`（完整性）：** Decode kernel 读取、或发布到全局前缀缓存中的每个 KV page，都必须包含来自目标请求代次的完整、未损坏数据。
3. **`Finality`（终结性）：** 每个活跃请求和正在排空的内存 page 都必须在有限步内到达终止状态，而不是永远挂起。
4. **`Conservation`（守恒）：** 每个物理 page 都被严格记账：一个暴露给在途 RDMA 的 page，只有在硬件停止证据到达后才回到 `FREE`，否则就永久隔离在 `QUARANTINED` 记账状态中。

### 在 SGLang 和 vLLM 中发现真实的并发问题[#](#uncovering-real-concurrency-issues-in-sglang-and-vllm)

在 CPU 上用这四条规约检查 [SGLang](https://github.com/sgl-project/sglang) 和 [vLLM](https://github.com/vllm-project/vllm) 的生产级 Prefill-Decode 实现，发现了**三类并发问题**。我们针对其中部分 RDMA 失败路径在 NVIDIA GB200 上、控制面死锁在 CPU 上做了复现，并提交了 **6 个上游 pull request**：

* **在 RDMA 仍在传输时回收传输槽或 KV block：** 当请求中止或超时时，已经排入网卡的单边 RDMA 传输在所研究的传输路径上无法在硬件层取消；然而两个引擎都允许新请求在硬件传输停止之前复用相同的传输标识或重新分配已过期的 GPU page，违反了 **`Isolation`（隔离性）**。在 GB200 上，我们在 SGLang 和 vLLM 中都复现了这个竞争，迟到的 RDMA 访问在 `HTTP 200 OK` 下静默读取或覆盖了另一个请求的 KV cache。我们在 SGLang 中提出了上游修复 [`#48883`](https://github.com/sgl-project/sglang/pull/48883)、[`#48889`](https://github.com/sgl-project/sglang/pull/48889)、[`#48960`](https://github.com/sgl-project/sglang/pull/48960)、[`#48979`](https://github.com/sgl-project/sglang/pull/48979)、[`#48982`](https://github.com/sgl-project/sglang/pull/48982)，以及由 [`@vadiklyutiy`](https://github.com/vadiklyutiy) 提交的一个相关 vLLM pull 校验 PR [`#62065`](https://github.com/vllm-project/vllm/pull/62065)。
* **把被竞争污染的 KV page 发布到全局前缀缓存：** 当 RDMA 传输完成时，Decode 节点可能把收到的 KV page 插入全局前缀缓存，却不检查该 page 的生命周期代次是否在传输途中已失效，违反了 **`Integrity`（完整性）**。在我们的 vLLM GB200 实验中，被竞争污染的 KV page 进入了前缀缓存，并污染了随后复用该缓存前缀的请求。这说明需要在 RDMA 传输与前缀缓存边界之间一致地跟踪带版本的 page 所有权。
* **传输租约未续期与 Decode 请求挂起：** 当远端传输停滞或中止通知丢失时，未续期的租约与缺失的看门狗会让 Decode 请求无限等待，同时占着已分配的 GPU page，违反了 **`Finality`（终结性）** 与 **`Conservation`（守恒性）**。我们在 GB200 上复现了停滞的 RDMA 租约，在 CPU 控制面重放中复现了调度器容量死锁，并在 vLLM 中提出了上游租约续期与接收超时修复 [`#66443`](https://github.com/vllm-project/vllm/pull/66443)。

**为什么本地超时会失效：** 上面最深的那些生命周期故障共享一个根本原因：**用本地 CPU 超时或错误码去猜测异步硬件 RDMA 何时完成**。使用 [`TLAPS`](https://proofs.tlapl.us/) 与 [`Z3`](https://github.com/Z3Prover/z3)，我们形式化地证明了：在无界异步延迟、且本地历史在缺少可信的停止或撤销证据时不可区分的情况下，*任何*仅靠本地的 page 回收策略，要么必须提早回收以保住 **`Isolation`**，要么必须永久持有 page 以保住 page 级 **`Finality`**，两者无法兼得。

### 构建 `veriserve`：一个可验证的 LLM 服务引擎[#](#building-veriserve-a-verifiable-llm-serving-engine)

既然任何仅靠本地的超时策略都无法摆脱这一权衡，那么当前的引擎——如 SGLang 与 vLLM——只要其 RDMA 连接器、前缀缓存和 decode 调度器仍在对裸 `page_id` 整数维护各自独立的本地计数器、并猜测硬件 RDMA 何时完成，就依然是脆弱的。为了在设计上解决这个问题，我们构建了 [**`veriserve`**](https://github.com/hao-ai-lab/veriserve)：一个基于 [`mini-sglang`](https://github.com/sgl-project/mini-sglang) 与 [Mooncake](https://github.com/kvcache-ai/Mooncake) GPUDirect RDMA 的 PD 分离式可验证 LLM 服务引擎，其核心是单一的能力状态机 **`PdLedger`**——它通过带版本的票据 `(page, gen)` 追踪每个物理 page，跨越六个显式实现状态：**`FREE`**、**`PRIVATE`**、**`SHARED`**、**`DRAINING`**、**`QUARANTINED`** 与 **`DUP`**。**图 3** 展示了 RDMA 超时与取消路径上的四个状态。

![PdLedger page 生命周期解决了本地超时困境](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/verifiable-llm-infra--img--fig3.gif)

图 3. PdLedger 如何在 RDMA 传输路径上解决本地超时困境。没有停止证据时，超时的 page 被隔离在 Quarantined 中，迟到的 RDMA 写入绝不会触碰新请求；有停止证据时，被取消的 page 在 Draining 中等待，只有远端传输停止后才回到 Free。前缀缓存的 Shared 与 Dup 状态为清晰起见已省略。

我们的关键设计差异在于用 **`DRAINING`** 与 **`QUARANTINED`** 把*请求取消*与*硬件 DMA 完成*解耦，从而解决“请求挂起 vs 数据损坏”的权衡：

* **带停止证据的释放 → `FREE`：** 释放一个仍有在途 RDMA 或 kernel 访问的私有 page 时，先把它移到 `DRAINING`。一旦硬件完成或对端确认所有被跟踪的访问都已停止，`PdLedger` 就把该 page 还给 `FREE`，同时每个新的请求代次会拿到一个新的代次标识 `gen`，从而保住 **`Conservation`（守恒性）**。
* **无停止证据的超时 → `QUARANTINED`：** 当传输超时且没有停止证据时，`PdLedger` 终止受影响的等待请求，使请求不会挂起，同时把那个已暴露的物理 page 在进程整个生命周期内永久隔离在 **`QUARANTINED`** 中，于是任何迟到的 RDMA 数据包都会落在 `FREE` 和前缀缓存之外，无害地失效，从而保住 **`Isolation`（隔离性）** 与 **`Integrity`（完整性）**。

信任 [`TLAPS`](https://proofs.tlapl.us/) 与 [`Z3`](https://github.com/Z3Prover/z3) 验证器，形式化证明能确立的是抽象设计模型在其显式假设下的安全性，而不是说我们的 Python 实现、GPU kernel 或 RDMA provider 没有 bug。为了让 Python 引擎与模型保持一致，`veriserve` 在运行时同步检查 `PdLedger` 的前置条件，在我们的变异门禁中拒绝注入的状态迁移变异，并记录 Prefill 与 Decode 边界迁移，用于逐步的 `TLC` 轨迹校验。

---

## 评测[#](#evaluation)

我们分别在 CPU 上对 `PdLedger` 设计模型做形式化验证，以及在一个 4-GPU NVIDIA GB200 节点上用 `Qwen3-0.6B` 与 `Qwen3-32B` 做端到端 GPUDirect RDMA 服务评测——Prefill 与 Decode 各占一张 GPU，通过 Mooncake 通信：

* **CPU 上的形式化安全性证明：** [`TLC`](https://docs.tlapl.us/using:tlc:start) 模型检查在有界配置上探索了 **2,100 万+ 个可达状态**，零安全性违规。在我们规约显式的 `Sizes` 与 `Design` 假设下，我们完成了覆盖全部 64 个协议动作和 54 条归纳不变量的 **226 个模块、516,973 条证明义务的 [`TLAPS`](https://proofs.tlapl.us/) 归纳证明**，并配合用 [`Z3`](https://github.com/Z3Prover/z3) 对建模的 6D GPU KV buffer 地址算术在 page size 1、16 和 64 下做了证明。
* **跨 `22,104` 个边界事件 100% 的轨迹校验：** 通过把异步的 Prefill 与 Decode 运行时日志因果合并成带版本的 page 步骤，**八次正常服务运行中的 `22,104` 个映射边界事件 100% 在 `TLC` 中干净重放**。
* **缓存与故障测试下零校验和错误：** 在八次单 page 前缀共享与缓存驱逐运行中，`PdLedger` 校验了 **540 个 KV 校验和，零不匹配、零记账违规**，同时运行时检查捕获了**全部三个注入的胶水层故障**。
* **GB200 上平均 p50 `TPOT` 开销低于 `0.7%`：** 在 [Alibaba `qwen-bailian`](https://github.com/alibaba-edu/qwen-bailian-usagetraces-anon) 工作负载上用 `Qwen3-32B`，Decode 侧 `PdLedger` 检查在每个 decode step 的 **p50 CPU 时间为 `0.33 ms`**，而 HTTP `TPOT` 中位数为 **`13.6 ms`**。在六次与未验证 bypass 基线的配对运行中，`PdLedger` 带来的平均 p50 `TPOT` 开销为 **`+0.18%`**，**95% 置信区间从 `-0.32%` 到 `+0.68%`**。

---

## 开源与下一步[#](#open-source-and-whats-next)

我们开源了这项工作的全部三个部分：

1. [**`vstack`**](https://github.com/hao-ai-lab/vstack)：我们面向 Claude Code 与 Cursor 的五阶段形式化验证插件。
2. [**`veriserve`**](https://github.com/hao-ai-lab/veriserve)：我们基于 [`mini-sglang`](https://github.com/sgl-project/mini-sglang) 与 [Mooncake](https://github.com/kvcache-ai/Mooncake) RDMA 的可验证 LLM 服务引擎，包括 `PdLedger`、`TLA+`、[`TLAPS`](https://proofs.tlapl.us/) 与 [`Z3`](https://github.com/Z3Prover/z3) 模型与证明，以及轨迹校验套件。
3. **[SGLang](https://github.com/sgl-project/sglang) 与 [vLLM](https://github.com/vllm-project/vllm) 的上游修复**：跨 SGLang [`#48883`](https://github.com/sgl-project/sglang/pull/48883)、[`#48889`](https://github.com/sgl-project/sglang/pull/48889)、[`#48960`](https://github.com/sgl-project/sglang/pull/48960)、[`#48979`](https://github.com/sgl-project/sglang/pull/48979)、[`#48982`](https://github.com/sgl-project/sglang/pull/48982) 与 vLLM [`#66443`](https://github.com/vllm-project/vllm/pull/66443) 提出的并发修复。

验证 Prefill-Decode 分离式服务的 KV page 生命周期只是第一步。接下来我们要做的是对分层 KV 缓存（例如 [SGLang HiCache](https://www.lmsys.org/blog/2025-09-10-sglang-hicache/)）、多 page 前缀树以及底层 GPU kernel 的形式化验证工作。**更多可验证服务即将到来，敬请关注。**

---

## 致谢[#](#acknowledgement)

感谢 NVIDIA 对我们在 NVIDIA GB200 上进行开发与 GPUDirect RDMA 评测的支持。感谢 SGLang、mini-sglang、vLLM 和 Mooncake 社区构建开源分离式服务栈，并评审我们的上游 bug 报告与修复；感谢 Qwen 团队与阿里巴巴发布我们评测中使用的 Qwen3 模型与 `qwen-bailian` 轨迹。我们的验证工作流建立在开源 TLA+、TLC、Apalache、TLAPS 与 Z3 生态之上，并从 Lauren Tan 的 `pstack` 中汲取了灵感。

## 贡献者[#](#contributors)

[Yuxuan Zhang](https://yuxuandexter.github.io/)、[Minshen Zhang](https://alexzms.github.io/)、[Junda Su](https://davids048.github.io/)、[Yi Sun](https://www.linkedin.com/in/yi-sun-mlsys)、[Junda Chen](https://github.com/GindaChen)、[Hao Zhang](https://haozhang.ai)

## 引用[#](#citation)

```
@misc{vstack2026,
  title        = {Towards Verifiable {LLM} Infra},
  author       = {Zhang, Yuxuan and Zhang, Minshen and Su, Junda and Sun, Yi and Chen, Junda and Zhang, Hao},
  year         = {2026},
  month        = nov,
  howpublished = {Hao AI Lab Blog},
  url          = {https://haoailab.com/blogs/verifiable-llm-infra/}
}
```

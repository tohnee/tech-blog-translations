---
title: "vLLM Semantic Router：LLM 推理的下一阶段"
title_en: "vLLM Semantic Router: Next Phase in LLM inference"
source: https://vllm.ai/blog/2025-09-11-semantic-router
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM Semantic Router：LLM 推理的下一阶段

> 原文：[vLLM Semantic Router: Next Phase in LLM inference](https://vllm.ai/blog/2025-09-11-semantic-router) · vLLM 博客

作者：vLLM Semantic Router 团队

[#生态](https://vllm.ai/blog/tags/ecosystem)

![](https://vllm.ai/blog-assets/figures/semantic-router/request.png)

## 行业现状：推理并非「越多越好」

过去一年，混合推理与自动路由日益成为大模型基础设施进步的定义性特征——讨论的焦点也从单纯的规模转向逐 token 效率、延迟控制以及有针对性的算力使用。

以 GPT-5 为例：它最突出的创新不在于参数规模，而在于路由策略与基于配额的推理：

- 轻量查询 → 轻量路径：像「天空为什么是蓝色的？」这类简单提示不会触发昂贵的推理。
- 复杂/高价值查询 → 支持推理的模型：多步骤任务——如法律分析或财务规划——会被路由到支持思维链（Chain-of-Thought）的推理。

这体现了一个更广泛的原则——任务感知的算力分配：每个推理 token 都必须创造有意义的价值，而不只是被消耗掉。

类似的理念也出现在其他系统中：

- Anthropic Claude 3.7/4：区分「快思考」与「慢思考」两条路径。
- Google Gemini 2.5：提供显式的*思考预算*（thinking budget），允许企业为推理深度设置上限。
- 阿里巴巴 Qwen3：支持通过指令在推理与非推理模式之间切换。
- DeepSeek v3.1：在单一模型的双模式中融合了对话流与推理流。

趋势已经很清晰：未来的推理系统将由选择性与智能化定义，而不仅仅是模型规模。

## 最新进展：vLLM Semantic Router

顺应这一转变，vLLM Semantic Router 为高效的 vLLM 推理引擎提供了一个开源的、意图感知的路由层。

vLLM 支持可扩展的 LLM 服务，但在推理相关的语义决策方面尚有欠缺。开发者面临一个权衡：

- 始终开启推理 → 准确率提升，但成本也随之上升。
- 关闭推理 → 成本下降，但复杂任务上的准确率受损。

Semantic Router 通过对查询进行语义分类并恰当路由来填补这一空白：在需要之处给出准确结果，在无需推理之处保证效率。

![](https://vllm.ai/blog-assets/figures/semantic-router/architecture.png)

### 架构设计

系统由四大支柱组成：

1. 语义分类：使用 ModernBERT——目前是集成到路由器中的轻量级独立分类器——来确定路由路径。
2. 智能路由：
   - 简单查询 → 「快速路径」推理。
   - 复杂查询 → 「思维链（Chain-of-Thought）」推理模式。
3. 高性能引擎：使用 Hugging Face Candle 以 Rust 编写，提供高并发与零拷贝推理。
4. 云原生集成：通过 `ext_proc` 插件开箱即用地与 Kubernetes 和 Envoy 协作。

在实际测试中，这一设计带来了：

- 准确率提升约 10%
- 延迟降低约 50%
- token 消耗减少约 50%

在商业与经济学领域，准确率提升超过 20%。

## 执行中的挑战：预算与工具调用

有两个技术约束需要重点解决：

- 推理预算成本
  无限制的推理会推高冷启动延迟与资源消耗。缺少动态控制时，简单查询可能过度消耗 token，而关键查询在需要时却得不到深度推理。因此需要 TTFT、p95 延迟之类的 SLO，并可在推理过程中动态调整。
- 工具调用约束
  增加更多工具（即「工具目录膨胀」）或更长的工具输出会大幅降低准确率。路由器必须预先筛选工具并保持目录精简。

## 项目背景

Semantic Router 的演进离不开开源社区的贡献：

- 由 [Chen Huamin 博士](https://www.linkedin.com/in/huaminchen)（Red Hat）于 2025 年初提出
- 由 [Xunzhuo Liu](https://www.linkedin.com/in/bitliu)（腾讯）进一步发展
- 将由 [Wang Chen 博士](https://www.linkedin.com/in/chenw615)（IBM Research）与 Chen Huamin 博士在 [KubeCon North America 2025](https://kccncna2025.sched.com/event/27FaI/intelligent-llm-routing-a-new-paradigm-for-multi-model-ai-orchestration-in-kubernetes-chen-wang-ibm-research-huamin-chen-red-hat?iframe=no&w=100%25&sidebar=yes&bg=no) 上进行分享

我们的目标：通过以下方式为开源 LLM 提供推理加速：

- 语义感知路由
- 高效的模型切换
- 对企业友好的部署（Kubernetes 与 Envoy）

项目地址见 [GitHub](https://github.com/vllm-project/semantic-router)。当前的工作重心是一个[工作组](https://vllm-semantic-router.com/community/work-groups)以及规划中的 [v0.1 路线图](https://vllm-semantic-router.com/roadmap/v0.1)。

## 集成与后续工作：嵌入模型与可插拔性

目前，ModernBERT 在路由器内部运行以完成分类，尚未由 vLLM 提供服务。不过，后续工作旨在让分类器（以及可能的其他嵌入模型）变得可插拔，从而能够与 vLLM 托管的模型或外部嵌入服务集成。

这一能力将增强语义缓存，并让推理定制更加顺畅。

## 路线图：v0.1 里程碑亮点

[v0.1 里程碑](https://github.com/vllm-project/semantic-router/milestone/1)将扩展项目的技术能力：

- 核心：基于 ExtProc 的模块化、跨后端的语义缓存、多因素路由逻辑
- 基准测试：CLI 工具、性能测试套件、推理模式评估
- 网络：与 Envoy、GIE、llm-d 网关的更深层次集成
- 可观测性与用户体验：管理仪表盘、路由策略可视化、开发者快速上手指南与策略手册

## 未来趋势：即时（Just-in-Time）推理

这个领域正在从「我们能不能跑推理？」走向「如何让推理更聪明？」的成熟阶段。

- GPT-5 用商业价值来引导推理深度。
- vLLM Semantic Router 则把这一能力带给了开源社区。

展望未来，能够无需人工开关、实时调整推理策略的系统，将在效率、延迟与可持续性上处于领先地位。

## 一句话总结

- GPT-5：面向更聪明推理的企业级路由
- vLLM Semantic Router：面向开源 LLM 的技术优先路由
- 边缘侧的未来：上下文感知、最小算力的无缝推理

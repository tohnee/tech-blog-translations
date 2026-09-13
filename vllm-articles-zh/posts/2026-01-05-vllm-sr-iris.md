---
title: "vLLM Semantic Router v0.1 Iris：首个大版本发布"
title_en: "vLLM Semantic Router v0.1 Iris: The First Major Release"
source: https://vllm.ai/blog/2026-01-05-vllm-sr-iris
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM Semantic Router v0.1 Iris：首个大版本发布

> 原文：[vLLM Semantic Router v0.1 Iris: The First Major Release](https://vllm.ai/blog/2026-01-05-vllm-sr-iris) · vLLM 博客

vLLM Semantic Router 团队

[#生态](https://vllm.ai/blog/tags/ecosystem)

[vLLM Semantic Router](https://github.com/vllm-project/semantic-router) 是面向混合模型（Mixture-of-Models, MoM）的**系统级智能**，为 LLM 系统注入**群体智能（Collective Intelligence）**。它位于用户与模型之间，从请求、响应和上下文中捕获信号，做出智能路由决策——包括模型选择、安全过滤（越狱、PII）、语义缓存和幻觉检测。更多背景请参阅我们的[首发公告博客](https://blog.vllm.ai/2025/09/11/semantic-router.html)。

我们非常高兴地宣布 **vLLM Semantic Router v0.1** 发布，代号 **Iris**——这是我们的首个大版本，标志着智能 LLM 路由的一个变革性里程碑。自 2025 年 9 月实验版上线以来，我们见证了社区的高速成长：超过 **600 个 Pull Request** 合并、**300+ 个 Issue** 得到处理，以及来自全球 **50 多位杰出工程师**的贡献。值此 2026 年开局之际，我们很高兴交付这个从起步之初已发生脱胎换骨、可用于生产的语义路由平台。

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-0.png)

## 为什么叫 Iris？

在希腊神话中，伊里斯（Iris，Ἶρις）是为神明与凡间传递消息的使者，她沿彩虹之弧跨越辽阔距离传递讯息。这一象征恰好契合 vLLM Semantic Router v0.1 的使命：**在用户与多样化 AI 模型之间架起桥梁**，跨不同的 LLM 提供商与架构智能地路由请求。

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-1.png)

## v0.1 Iris 有哪些新特性？

### 1. 架构重塑：信号-决策插件链架构

**过去：** 早期的 Semantic Router 依赖单一路径——将查询归入 14 个 MMLU 领域类别之一，并以静态方式编排越狱检测、PII 防护和语义缓存能力。

**现在：** 我们推出了**信号-决策驱动的插件链架构（Signal-Decision Driven Plugin Chain Architecture）**，对语义路由进行了彻底重构，从 14 个固定类别扩展到无限的智能路由决策。

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-2.png)

新架构从用户查询中提取**六类信号**：

- **领域信号（Domain Signals）**：基于 MMLU 训练的分类，支持 LoRA 扩展
- **关键词信号（Keyword Signals）**：快速、可解释的基于正则的模式匹配
- **嵌入信号（Embedding Signals）**：使用神经嵌入的可扩展语义相似度
- **事实信号（Factual Signals）**：用于幻觉检测的事实核验分类
- **反馈信号（Feedback Signals）**：用户满意/不满意的指示
- **偏好信号（Preference Signals）**：基于用户自定义偏好的个性化

这些信号作为**灵活决策引擎**的输入，引擎通过 AND/OR 逻辑组合信号并按优先级选择。以往静态的特性——如越狱检测、PII 防护和语义缓存——现在都成为可配置的**插件**，用户可以按决策启用：

| 插件 | 用途 |
| --- | --- |
| `semantic-cache` | 缓存相似查询以优化成本 |
| `jailbreak` | 检测提示注入攻击 |
| `pii` | 保护敏感信息 |
| `hallucination` | 实时幻觉检测 |
| `system_prompt` | 注入自定义指令 |
| `header_mutation` | 修改 HTTP 头以传递元数据 |

这种模块化设计带来无限的可扩展性——新的信号、插件和模型选择算法都无需架构改动即可加入。更多信息请阅读我们的[信号-决策架构博客](https://blog.vllm.ai/2025/11/19/signal-decision.html)。

### 2. 性能优化：模块化 LoRA 架构

与 **Hugging Face Candle 团队**合作，我们彻底重构了路由器的推理内核。此前的实现需要独立加载并运行多个微调模型——计算成本随分类任务数量线性增长。

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-3.png)

**突破在于：** 通过采用**低秩适配（LoRA）**，我们在所有分类任务之间共享基础模型计算：

| 方案 | 工作负载 | 可扩展性 |
| --- | --- | --- |
| 之前 | N 次完整模型前向传播 | O(n) |
| 之后 | 1 次基础模型前向传播 + N 个轻量 LoRA 适配器 | O(1) + O(n×ε) |

> **注：** 此处 ε 表示 LoRA 适配器前向传播相对于完整基础模型的相对成本——通常 ε << 1，因此额外开销可以忽略不计。

这一架构在支持对同一输入进行多任务分类的同时，带来了**显著的延迟降低**。完整技术细节请见我们的[模块化 LoRA 博客](https://blog.vllm.ai/2025/10/27/semantic-router-modular.html)。

### 3. 安全增强：HaluGate 幻觉检测

除请求时安全（越狱、PII）之外，v0.1 还引入了 **HaluGate**——一条面向 LLM 响应的三阶段幻觉检测流水线：

**阶段 1：HaluGate Sentinel** – 二分类，判断查询是否需要事实核验（创意写作与代码无需事实核验）。

**阶段 2：HaluGate Detector** – token 级检测，精确识别响应中哪些 token 缺乏所提供上下文的支持。

**阶段 3：HaluGate Explainer** – 基于 NLI 的分类，解释*每个被标记的片段为什么*有问题（CONTRADICTION 还是 NEUTRAL）。

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-4.png)

HaluGate 与函数调用工作流无缝集成——工具结果可作为核验的真实依据。检测结果通过 HTTP 头传递，使下游系统能够实施自定义策略。深入了解请见我们的 [HaluGate 博客](https://blog.vllm.ai/2025/12/14/halugate.html)。

### 4. 体验改进：一条命令完成安装

**本地开发：**

```
pip install vllm-sr
```

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-7.png)

一条 pip 命令，几秒内即可上手。该安装包包含快速入门所需的全部核心依赖。

> **配置：** 安装后，运行 `vllm-sr init` 生成默认的 `config.yaml`。然后在 `providers` 部分配置你的 LLM 后端：
>
> ```
> providers:
>   models:
>     - name: "openai/gpt-oss-120b"       # Local vLLM endpoint
>       endpoints:
>         - endpoint: "localhost:8000"
>           protocol: "http"
>       access_key: "your-vllm-api-key"
>     - name: "openai/gpt-4"              # External provider
>       endpoints:
>         - endpoint: "api.openai.com"
>           protocol: "https"
>       access_key: "sk-xxxxxx"
>   default_model: "openai/gpt-oss-120b"
> ```
>
> 完整细节请参阅[配置文档](https://vllm-semantic-router.com/docs/installation/)。

**Kubernetes 部署：**

```
helm install semantic-router oci://ghcr.io/vllm-project/charts/semantic-router
```

生产就绪的 Helm chart，提供合理的默认值与丰富的自定义选项，帮助你轻松在 Kubernetes 中部署 vLLM Semantic Router。

**仪表盘（Dashboard）：** 一个功能完备的 Web 控制台，用于管理智能路由策略与模型配置，并提供交互式聊天游乐场，可实时测试路由决策。在一个直观的浏览器界面中，即可可视化路由流向、监控延迟分布并微调分类阈值。

### 5. 生态集成

vLLM Semantic Router v0.1 与更广泛的 AI 基础设施生态无缝集成：

**推理框架：**

- [vLLM Production Stack](https://github.com/vllm-project/production-stack) – 生产级 vLLM 部署参考技术栈，提供 Helm chart、请求路由和 KV 缓存卸载
- [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) – 数据中心规模的分布式推理框架，支持多 GPU、多节点及分离式预填充/解码服务
- [llm-d](https://github.com/llm-d/llm-d) – Kubernetes 原生的分布式推理栈，在各类加速器（NVIDIA、AMD、Google TPU、Intel XPU）上实现 SOTA 性能
- [vLLM AIBrix](https://github.com/vllm-project/aibrix) – 面向可扩展 LLM 服务的开源 GenAI 基础设施构建模块

**API 网关：**

- [Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway) – 基于 Envoy Gateway 构建的生成式 AI 服务统一入口，支持多提供商
- [Istio](https://github.com/istio/istio) – 面向企业部署的开源服务网格，提供流量管理、安全与可观测性

### 6. MoM（Mixture of Models）模型家族

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-6.png)

我们很自豪地推出 **MoM 家族**——一套为语义路由量身打造的专用模型：

| 模型 | 用途 |
| --- | --- |
| `mom-domain-classifier` | 基于 MMLU 的领域分类 |
| `mom-pii-classifier` | PII 检测与防护 |
| `mom-jailbreak-classifier` | 提示注入检测 |
| `mom-halugate-sentinel` | 事实核验分类 |
| `mom-halugate-detector` | token 级幻觉检测 |
| `mom-halugate-explainer` | 基于 NLI 的解释 |
| `mom-toolcall-sentinel` | 工具选择分类 |
| `mom-toolcall-verifier` | 工具调用校验 |
| `mom-feedback-detector` | 用户反馈分析 |
| `mom-embedding-x` | 语义嵌入提取 |

所有 MoM 模型都针对 vLLM Semantic Router 专门训练与优化，在各路由场景中提供一致的性能。

### 7. Responses API 支持

我们现已支持 **OpenAI Responses API**（`/v1/responses`），并内置内存态会话状态管理：

- **有状态对话**：内置状态管理，支持 `previous_response_id` 链式关联
- **多轮上下文**：跨对话轮次自动保留上下文
- **路由连续性**：在整个会话中维护意图分类历史

这为现代智能体框架和多轮应用实现了智能路由。

### 8. 工具选择

面向智能体工作流的智能工具管理：

- **语义工具过滤**：在发送给 LLM 之前自动过滤无关工具
- **上下文感知选择**：结合对话历史与任务需求
- **减少 token 用量**：更小的工具目录意味着更快的推理与更低的成本

---

## 展望未来：v0.2 路线图

v0.1 Iris 已奠定坚实基础，我们已在规划 v0.2 的多项重要增强：

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-5.png)

### 信号-决策架构增强

- **更多信号类型**：从用户查询中提取更多有价值的信号
- **更高精度**：提升现有信号计算的精确度
- **信号组合器（Signal Composer）**：设计信号组合层，实现复杂信号提取与更好的性能

### 模型选择算法

![](https://vllm.ai/blog-assets/figures/semantic-router/iris-8.png)

在信号-决策的基础上，我们正在研究智能模型选择算法：

- **基于机器学习的技术**：KNN、KMeans、MLP、SVM、矩阵分解
- **高级方法**：Elo rating、RouterDC、AutoMix、混合方法
- **基于图的选择**：利用模型关系图
- **规模感知路由**：基于模型规模与任务复杂度进行优化

### 开箱即用插件

- **记忆插件（Memory Plugin）**：持久的会话记忆管理
- **路由回放（Router Replay）**：调试与回放路由决策及反馈

### 多轮算法探索

- **Response API 增强**：扩展有状态会话支持，后端可插拔，如 Redis、Milvus 与 Memcached。
- **上下文工程**：上下文压缩与记忆管理
- **RL 驱动的选择**：用强化学习实现用户偏好驱动的模型选择

### MoM 增强

- **预训练基础模型**：更长的上下文窗口用于信号提取
- **后训练 SLM**：人类偏好信号提取
- **模型迁移**：用自训练模型替换现有模型

### 安全增强

- **工具调用越狱检测**：防范恶意工具调用
- **多轮护栏**：跨会话的安全防护
- **更高的幻觉检测精度**：更精准的幻觉检测

### 智能工具管理

- **工具补全**：基于意图自动补全工具定义与调用。
- **高级工具过滤**：更精细的相关性过滤

### 体验与运维

- **仪表盘增强**：更强的可视化与管理能力
- **Helm Chart 改进**：更多配置选项与部署模式

### 评估

- 与 RouterArena 团队合作构建全面的路由器评估框架

---

## 致谢

vLLM Semantic Router v0.1 Iris 是一次真正意义上的全球协作。我们诚挚感谢来自 **Red Hat**、**IBM Research**、**AMD**、**Hugging Face** 等众多组织的贡献。

我们很高兴欢迎不断壮大的 committer 社区：

*Senan Zedan, samzong, Liav Weiss, Asaad Balum, Yehudit, Noa Limoy, JaredforReal, Abdallah Samara, Hen Schwartz, Srinivas A, carlory, Yossi Ovadia, Jintao Zhang, yuluo-yx, cryo-zd, OneZero-Y, aeft*

同时感谢帮助这个版本得以问世的 **50 多位贡献者**——谢谢你们！

---

## 快速开始

准备好试用 vLLM Semantic Router v0.1 Iris 了吗？

```
pip install vllm-sr
```

---

## 加入社区

我们相信，智能路由的未来需要共同构建。无论你是希望将智能路由集成到 AI 基础设施中的**企业**、探索语义理解新边疆的**研究者**，还是热爱开源 AI 的**个人开发者**——我们都欢迎你的参与。

**参与方式：**

- **组织**：与我们合作集成、赞助开发，或贡献工程资源
- **研究者**：合作发表论文、提出新算法，或协助性能基准测试
- **开发者**：提交 PR、报告 Issue、改进文档，或构建社区插件
- **社区**：分享用例、撰写教程、翻译文档，或帮忙解答问题

每一份贡献都很重要——从修正一个错别字到设计一个全新功能。加入我们，共同塑造下一代语义路由基础设施。

- **文档**：[vllm-semantic-router.com](https://vllm-semantic-router.com)
- **GitHub**：[vllm-project/semantic-router](https://github.com/vllm-project/semantic-router)
- **模型**：[Hugging Face](https://huggingface.co/llm-semantic-router)
- **社区**：加入 [vLLM Slack](https://vllm-dev.slack.com/archives/C09CTGF8KCN) 与我们交流

*彩虹之桥现已开启。欢迎来到 Iris。* 🌈

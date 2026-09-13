---
title: "AIBrix 正式发布：面向 vLLM 的可扩展、高性价比控制平面"
title_en: "Introducing AIBrix: A Scalable, Cost-Effective Control Plane for vLLM"
source: https://vllm.ai/blog/2025-02-21-aibrix-release
crawled: 2026-09-12
translated: 2026-09-13
---

# AIBrix 正式发布：面向 vLLM 的可扩展、高性价比控制平面

> 原文：[Introducing AIBrix: A Scalable, Cost-Effective Control Plane for vLLM](https://vllm.ai/blog/2025-02-21-aibrix-release) · vLLM 博客

作者：AIBrix 团队

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#生态](https://vllm.ai/blog/tags/ecosystem)

今天，我们很高兴地宣布 [vllm-project/aibrix](https://github.com/vllm-project/aibrix)：一个由字节跳动开发的"开箱即用"（battery-included）vLLM Kubernetes 服务栈。AIBrix 始于 2024 年初，已成功部署以支撑字节跳动内部的多个业务场景，展示了其在大规模部署中的可扩展性和有效性。

虽然 vLLM 让部署单个服务实例变得容易，但大规模部署 vLLM 在路由、自动扩缩容和容错方面存在独特挑战。AIBrix 是一项开源计划，旨在提供构建可扩展推理基础设施所需的核心构建模块。它提供了一套面向部署、管理和扩展大语言模型（LLM）推理而优化的云原生解决方案，专门针对企业需求量身定制。

![](https://vllm.ai/blog-assets/figures/aibrix/aibrix-diagram.png)

首个版本聚焦以下关键特性：

- **高密度 LoRA 管理**：为轻量级的低秩模型适配提供精简支持。
- **LLM 网关与路由**：高效管理和引导多个模型与副本之间的流量。
- **面向 LLM 应用的自动扩缩容器**：根据实时需求动态伸缩推理资源。
- **统一的 AI Runtime**：一个多功能 sidecar，支持指标标准化、模型下载和管理。
- **分布式推理**：可扩展的架构，可在多个节点上处理大型工作负载。
- **分布式 KV 缓存**：支持大容量、跨引擎的 KV 复用。
- **高性价比的异构服务**：支持混合 GPU 推理，在保证 SLO 的前提下降低成本。
- **GPU 硬件故障检测**：主动检测 GPU 硬件问题。

## AIBrix 愿景与产业协作

AIBrix 建立在系统与推理引擎协同设计（co-design）的原则之上，主要专注于以云原生的方式在 Kubernetes 上构建可扩展的推理系统。接下来，我们将通过以下举措继续探索**协同设计**方法：

- 扩展分布式 KV 缓存，支持更广泛的场景，包括预填充与解码（P&D）聚合、请求迁移和跨实例 KV 复用，提升内存效率和推理灵活性。
- 将 QoS、优先级、公平性等传统资源管理原则应用于 LLM 推理，实现请求级多租户，以确保高效的资源分配。
- 应用基于 roofline 的性能剖析来优化计算效率，在多样工作负载上提供具备强 SLO 保障的推理性能。

作为这一使命的一部分，我们积极与行业领导者合作，推动面向 LLM 服务的开放云原生解决方案。

*"在帮助 Google 通过 Working Group Serving 推动 Kubernetes 上 LLM 服务标准化、并为 Gateway API Inference Extension 做出贡献方面，字节跳动是一位非常出色的合作伙伴。我们期待在能让 AIBrix 和大规模推理平台共同受益的共享组件上继续合作。"*
*- Clayton Coleman，GKE 杰出工程师与推理负责人*

*"vLLM 在全球范围内呈现爆发式增长，已成为 LLM 推理的基石。AIBrix 是一个在这一势头之上构建的有前景的项目，它提供强大能力让 vLLM 走向生产环境，同时推动开源 LLM 推理的创新。"*
*- Robert Nishihara，Anyscale 联合创始人、Ray 联合创造者*

## 探索更多

欢迎访问仓库 <https://github.com/vllm-project/aibrix>，并阅读我们的[博客文章](https://aibrix.github.io/posts/2025-02-20-vllm-control-plane/)，深入了解 AIBrix 的架构和关键能力。如需更深入的理解，可以查阅我们关于设计哲学与结果的[白皮书](https://github.com/vllm-project/aibrix/blob/main/docs/paper/AIBrix_White_Paper_0219_2025.pdf)，关注[文档](https://aibrix.readthedocs.io/latest/)以开始部署与集成，并加入 vLLM Slack 的 [aibrix 频道](https://vllm-dev.slack.com/archives/C08EQ883CSV)与开发者交流。

## 常见问题（FAQ）

**AIBrix 与 vLLM [production stack](https://github.com/vllm-project/production-stack) 有何不同？**

- AIBrix 是字节跳动开源的项目，专注于大规模场景和云原生解决方案。Production stack 由 UChicago LMCache 团队管理，是一个开放框架，欢迎所有人扩展、实验和贡献。production stack 的路线图见[这里](https://github.com/vllm-project/production-stack/issues/26)。
- AIBrix 是一个强大的 K8s 技术栈所能呈现形态的一个具体实例，并且已在生产环境中运行超过 6 个月。Production stack 则是从零开始的实现，专注于结合社区的反馈和贡献来迭代每一个构建模块。
- Production stack 的预期优势在于利用内置的以 KV 缓存为核心的优化（传输、混合、路由），这在长上下文和预填充密集型工作负载中尤其有益。近期，production stack 计划复用 AIBrix 的组件。

**AIBrix 是社区驱动的项目吗？**

当然是。将其在 vLLM 项目组织下开源的目的，就是向实践者和研究者开放协作。还有许多增强领域正在规划之中，核心开发者坚信未来属于开源！

**AIBrix 与 KServe、KubeAI 等其他云原生解决方案有何不同？**

AIBrix 与 vLLM 有更深度的原生集成。由于设计时只针对一个推理引擎，AIBrix 可以优先考虑快速模型加载、自动扩缩容和 LoRA 管理等特性。

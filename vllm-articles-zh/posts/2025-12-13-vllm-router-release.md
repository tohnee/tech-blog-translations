---
title: "vLLM Router：面向大规模服务的高性能、感知 Prefill/Decode 的负载均衡器"
title_en: "vLLM Router: A High-Performance and Prefill/Decode Aware Load Balancer for Large-scale Serving"
source: https://vllm.ai/blog/2025-12-13-vllm-router-release
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM Router：面向大规模服务的高性能、感知 Prefill/Decode 的负载均衡器

> 原文：[vLLM Router: A High-Performance and Prefill/Decode Aware Load Balancer for Large-scale Serving](https://vllm.ai/blog/2025-12-13-vllm-router-release) · vLLM 博客

vLLM 团队

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)

在大规模生产级 vLLM 部署中，高效管理请求在模型副本集群中的分发是一项关键需求。标准负载均衡器往往力不从心，因为它们不了解 LLM 推理的有状态特性（例如 KV 缓存），也无法管理 PD 分离（Prefill-Decode 分离）这类复杂的服务模式。

为此，我们推出 **vLLM Router**（[GitHub 仓库](https://github.com/vllm-project/router)），一款专为 vLLM 打造的高性能、轻量级负载均衡器。该路由器用 Rust 构建，开销极小，是一个智能的、状态感知的负载均衡器，位于客户端与 vLLM worker 集群之间，可部署在 K8s 或裸金属 GPU 集群中。

vLLM Router 衍生自 [SGLang model gateway](https://github.com/sgl-project/sglang/tree/main/sgl-model-gateway) 的一个 fork，经过修改和简化以适配 vLLM。随着我们探索将此路由器合并进 vLLM 主仓库，二者预计会进一步分化。另一方面，面向大规模部署的网关功能也可能会与 SGLang model gateway 的开发者合作进行统一。

## 核心架构与能力

vllm-router 旨在解决大规模服务中的两大主要挑战：智能负载均衡，以及对 PD 分离（Prefill/Decode 分离）的支持。

### 1. 智能负载均衡策略

不同于简单的轮询（round-robin），vLLM Router 提供多种复杂的负载均衡算法，以优化性能和有状态亲和性。对于对话型负载，将同一用户的后续请求路由到持有其 KV 缓存的同一 worker，对最小化延迟至关重要。

为此，路由器支持以下几种策略：

- **一致性哈希（Consistent Hashing）：** 这是最大化性能的关键策略。它确保具有相同路由键（例如会话 ID 或用户 ID）的请求具有「粘性」，被一致地路由到同一个 worker 副本，从而最大化 KV 缓存复用。
- **二次方选择（Power of Two, PoT）：** 一种低开销的随机二选一策略，能提供出色的负载分布。
- **轮询（Round Robin）与随机（Random）：** 用于无状态负载分发的标准策略。

### 2. 原生支持 PD 分离（Prefill/Decode 分离）

该路由器被设计为 vLLM 最先进服务架构——PD 分离（Prefill/Decode 分离）——的编排层。

在这种架构中，计算密集的预填充步骤与内存密集的解码步骤由独立的、专门化的 worker 组处理。vLLM Router 管理这一复杂的工作流：

1. 它智能地将新请求路由到预填充 worker 组。
2. 预填充完成后，它将请求状态引导至合适的解码 worker 进行 token 生成。
3. 它支持 **NIXL** 与 **基于 NCCL（通过 ZMQ 发现）** 两种分离部署后端的发现与路由。

## 企业级的韧性与可观测性

vllm-router 内置了生产级特性，用于在大规模环境中维持高可用性。

- **Kubernetes 服务发现：** 路由器可以 Kubernetes 原生模式运行，使用标签选择器自动发现、监控 vLLM worker pod 并向其路由请求。
- **容错能力：** 它包含可配置的**重试逻辑**（带指数退避与抖动）和**熔断器（circuit breaker）**。当某个 worker 健康检查失败时，路由器会立即将其从路由池中移除并重试请求，防止级联故障。
- **可观测性：** 内置的 Prometheus 端点（`/metrics`）导出关于请求量、延迟、错误率以及各个 worker 健康状况的详细指标，为服务集群提供完整的可观测视角。

## 基准测试分析：规模化场景下性能最优的选择

我们将新的 vLLM Router 与两种广泛使用的替代方案进行了基准对比：

- **[llm-d](https://github.com/llm-d/llm-d)：** 一个 Kubernetes 原生路由框架，采用默认的队列感知负载均衡。
- **vLLM 原生：** 标准的 [K8s 原生负载均衡器](https://kubernetes.io/docs/concepts/services-networking/)，采用基本的轮询策略。关键在于，该方案*并不*感知 Prefill/Decode 状态，而是将所有 pod 视为完全相同的 vLLM 副本。

**关于排除项的说明：** 我们将 vLLM 内置的 DP/EP 协调器——vLLM 集群推荐的[外部负载均衡](https://docs.vllm.ai/en/stable/serving/data_parallel_deployment.html#external-load-balancing)方案——排除在了基准测试之外。由于一个已知的[性能问题](https://github.com/vllm-project/vllm/issues/24461)，其吞吐量仅为其他方案的 1/8。

### Llama 3.1 8B，8 个预填充 pod 与 8 个解码 pod

- vLLM Router（蓝线）的 Req/S 吞吐量比 llm-d（紫线）高 25%，比 K8s 原生负载均衡器（橙线）高 100%。
- vLLM Router 的 TTFT 与 K8s 原生负载均衡器接近，比 llm-d 快 1200 ms。

![](https://vllm.ai/blog-assets/figures/vllm-router/llama-benchmark.png)

### Deepseek V3，1 个预填充 pod（TP8）与 1 个解码 pod（TP8）

- vLLM Router（蓝线）的 Req/S 吞吐量与 llm-d（紫线）接近，比 K8s 原生负载均衡器（橙线）高 100%。
- vLLM Router 的 TTFT 比 llm-d 和 K8s 原生方案快 2000 ms。

![](https://vllm.ai/blog-assets/figures/vllm-router/deepseek-benchmark.png)

## 总结

vLLM Router 是在生产规模下运营 vLLM 的关键组件。它将服务架构从一组孤立实例转变为一个统一且富有韧性的集群。通过提供智能负载均衡和对 PD 分离（Prefill/Decode 分离）的原生支持，它解锁了新的性能水平与运营效率。

## 致谢

- 感谢 Phi 和 AWS 团队提供技术支持与测试集群。
- 特别感谢 Naman Lalit 推动全面的性能与正确性基准测试工作。
- 我们也感谢 SGLang Model Gateway 团队。通过 fork 他们成熟的 API 实现与服务框架，我们得以大幅加速设计与实现进程，同时保持与开放标准的一致。
- 最后，感谢 Tyler Michael Smith 和 Robert Shaw 分享 llm-d 的专业知识与实测数据，为性能优化和基准测试扫清了障碍。

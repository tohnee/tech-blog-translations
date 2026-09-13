---
title: "vLLM production-stack：在 K8S 中高性能、易部署地运行 vLLM"
title_en: "High Performance and Easy Deployment of vLLM in K8S with vLLM production-stack"
source: https://vllm.ai/blog/2025-01-21-stack-release
crawled: 2026-09-12
translated: 2026-09-12
---

# vLLM production-stack：在 K8S 中高性能、易部署地运行 vLLM

> 原文：[High Performance and Easy Deployment of vLLM in K8S with vLLM production-stack](https://vllm.ai/blog/2025-01-21-stack-release) · vLLM 博客

LMCache 团队

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#生态](https://vllm.ai/blog/tags/ecosystem)

## TL;DR

- **vLLM** 拥有最庞大的开源社区，但要把 vLLM 从最好的单节点 LLM 引擎打造成一流的 LLM 服务系统，需要什么？
- **今天，我们发布"vLLM production-stack"**，一个基于 vLLM 的完整推理栈，带来两大核心优势：
  - **性能提升 10x**（响应延迟降低 3-10x、吞吐量提高 2-5x），得益于前缀感知请求路由与 KV 缓存共享。
  - **轻松的集群部署**，内置容错、自动扩缩容和可观测性支持。
- 最棒的是？它是**开源的**——每个人都可以立即上手！[[**https://github.com/vllm-project/production-stack**]](https://github.com/vllm-project/production-stack)

# 背景

*在 AI 军备竞赛中，比拼的不再只是谁拥有最好的模型——而是**谁拥有最好的 LLM 服务系统**。*

**vLLM** 已经席卷开源社区，凭借无与伦比的硬件与模型支持，以及由顶尖贡献者组成的活跃生态。但直到现在，vLLM 主要聚焦于**单节点**部署。

我们如何把它的力量延伸为一个**全栈**推理系统，让任何组织都能以*高可靠性*、*高吞吐量*和*低延迟*进行大规模部署？这正是 LMCache 团队和 vLLM 团队构建 **vLLM production-stack** 的原因。

![Icon](/blog-assets/figures/stack/stack-thumbnail.png)

# 介绍"vLLM Production-Stack"

**vLLM Production-stack** 是一个构建在 vLLM 之上的**推理栈**的开源**参考实现**，旨在无缝运行于 GPU 节点集群。它在 vLLM 原生优势的基础上补充了四项关键功能：

- **KV 缓存共享与存储**，在上下文被复用时加速推理（由 [**LMCache**](https://github.com/LMCache/LMCache) 项目提供支持）。
- **前缀感知路由**，将查询发送到已持有相关上下文 KV 缓存的 vLLM 实例。
- **可观测性**，覆盖单个引擎状态和查询级指标（TTFT、TBT、吞吐量）。
- **自动扩缩容**，应对工作负载的动态变化。

### 与替代方案的对比：

下面是 vLLM production-stack 与其最接近的同类方案的快速对比：

![Icon](/blog-assets/figures/stack/stack-table.png)

### 设计

vLLM production-stack 的架构构建在 vLLM 强大的单节点引擎之上，提供集群级解决方案。

概而言之：

- 应用发送 LLM 推理请求。
- 前缀感知路由检查请求的上下文是否已缓存在某个实例的内存池中，然后将请求转发到持有预计算缓存的节点。
- 自动扩缩容和集群管理器监控整体负载，并在需要时启动新的 vLLM 节点。
- 可观测性模块收集 TTFT（Time-To-First-Token，首 token 延迟）、TBT（Time-Between-Tokens，token 间隔时间）和吞吐量等指标，让你实时掌握系统健康状况。

![Icon](/blog-assets/figures/stack/stack-overview-2.png)

# 优势一：轻松部署

使用 helm chart，通过运行一条命令即可将 vLLM production-stack 部署到你的 k8s 集群：

```
sudo helm repo add llmstack-repo https://lmcache.github.io/helm/ &&\
  sudo helm install llmstack llmstack-repo/vllm-stack

```

更多细节请参阅 [vLLM production-stack 仓库](https://github.com/vllm-project/production-stack)中的详细 README。关于搭建 k8s 集群和自定义 helm chart 的[教程](https://github.com/vllm-project/production-stack/tree/main/tutorials)也已可用。

# 优势二：更好的性能

我们在 vLLM production-stack 和其他配置上对多轮问答工作负载进行了基准测试，其他配置包括 vLLM + KServe 和一个商业端点服务。
结果显示，vLLM stack 在关键指标（首 token 延迟和逐 token 延迟）上全面优于其他配置。

![Icon](/blog-assets/figures/stack/stack-ttft.png)

![Icon](/blog-assets/figures/stack/stack-itl.png)

# 优势三：轻松监控

借助关键指标实时追踪你的 LLM 推理集群，包括延迟分布、随时间变化的请求数、KV 缓存命中率。

![Icon](/blog-assets/figures/stack/stack-panel.png)

## 结论

我们非常高兴地推出 **vLLM Production Stack**——这是把 vLLM 从顶级的单节点引擎转变为全面 LLM 服务系统的下一步。
我们相信，vLL stack 将为那些希望大规模构建、测试和部署 LLM 应用、而又不牺牲性能或简洁性的组织打开新的大门。

如果你和我们一样兴奋，别再等待！

- **克隆仓库：<https://github.com/vllm-project/production-stack>**
- **上手体验**
- **告诉我们你的想法！**
- **[兴趣登记表](https://forms.gle/mQfQDUXbKfp2St1z7)**

加入我们，共同建设一个人人都能驾驭 LLM 推理力量的未来——可靠、可扩展、轻松自如。
*祝部署愉快！*

联系方式：

- **vLLM [slack](https://slack.vllm.ai/)**
- **LMCache [slack](https://join.slack.com/t/lmcacheworkspace/shared_invite/zt-2viziwhue-5Amprc9k5hcIdXT7XevTaQ)**

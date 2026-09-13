---
title: "韩国首届 vLLM 社区聚会（Meetup）"
title_en: "The First vLLM Meetup in Korea"
source: https://vllm.ai/blog/2025-09-16-vllm-meetup
crawled: 2026-09-12
translated: 2026-09-13
---

# 韩国首届 vLLM 社区聚会（Meetup）

> 原文：[The First vLLM Meetup in Korea](https://vllm.ai/blog/2025-09-16-vllm-meetup) · vLLM 博客

作者：vLLM 团队

[#社区](https://vllm.ai/blog/tags/community)

![](https://vllm.ai/blog-assets/figures/vllm-meetup/image-3.png)

韩国首届 vLLM 社区聚会（Meetup）于 2025 年 8 月 19 日在首尔举行，由 Rebellions 和 Red Hat 主办，PyTorch Korea User Group 和 SqueezeBits 提供支持。

来看几个重要的数字：350 多人报名，参会者来自 75 家以上的公司，其中 80% 是业界人士——而这 80% 中又有 80% 是软件工程师和研究人员。对 vLLM 在韩国的首秀而言，这是一次相当强劲的亮相。

这次活动汇聚了本地开发者、研究人员和 AI 基础设施工程师，围绕高效 LLM 推理分享洞见，并探讨 vLLM 如何支持可扩展、硬件友好的部署——如今还包括 NPU。

## 亮点

### Nicolo Lucchesi：vLLM + llm-d 介绍与 vLLM TPU 集成深度解析

![](https://vllm.ai/blog-assets/figures/vllm-meetup/vllm_meetup_nicolo.jpg)

Red Hat 高级机器学习工程师 Nicolò Lucchesi 为活动开场，重点介绍了 vLLM 背后最初的核心创新——用全新的分页注意力（paged attention）架构解决 KV 缓存与动态批处理领域的长期难题。他强调「现代问题需要传统解决方案」，指出调度与内存管理方面的这些挑战早已在操作系统中被解决，而 vLLM 只不过是把同样经过验证的思想应用到了 AI 推理上。

他还介绍了支持分布式推理的项目 llm-d。llm-d 是一个 Kubernetes 原生的编排层，可协调多个 vLLM 实例并支持自动扩缩容——「当 vLLM 遇上 Kubernetes」。

Nicolò 最后介绍了集成 Google TPU 等 AI 加速器的进行中的工作，让 vLLM 能够覆盖更广泛的硬件平台。

### Daniele Trifirò：vLLM 的构建、测试与贡献

![](https://vllm.ai/blog-assets/figures/vllm-meetup/vllm_meetup_Daniele.png)

Red Hat 高级软件工程师 Daniele Trifirò 分享了开发者如何构建、测试 vLLM 项目并为其做贡献——重点关注真实场景下的 AI 服务。他着重介绍了快速的发布节奏：每周发布加上不断增长的贡献者群体，持续推动着大量代码变更。由于硬件要求，构建 vLLM 并不总是那么简单，Daniele 提供了实用的技巧与经验，帮助新贡献者快速上手。

他还解释了需要针对特定硬件编译的原因，并指出根据编译目标（如 CUDA、ROCm、TPU）不同，构建期间的内存占用可能急剧飙升。为了提升灵活性与开发者的可及性，他介绍了 vLLM 全新的硬件插件系统。这一插件架构让 vLLM 更加设备无关，进一步巩固了其作为健壮且可扩展的 AI 服务生态的地位。

### Hong-seok Kim：用 vLLM 为 Rebellions NPU 提速

![](https://vllm.ai/blog-assets/figures/vllm-meetup/vllm_meetup_HSkim.png)

Rebellions 首席软件架构师 Hong-Seok Kim 谈到了 vLLM 对 AI 加速器初创公司日益重要的意义，并分享了 Rebellions 如何为更广泛的 AI 推理服务生态做贡献。他强调，vLLM 的硬件插件系统让像 Rebellions 这样的公司能够支持开发者在自定义硬件上部署 LLM——带来与在 GPU 上运行几乎无缝的体验。

得益于 vLLM，工程师如今可以直接在 Rebellions 的 NPU 上运行 MoE（混合专家）模型，同时还能利用并行与连续批处理等核心优化——全程无需复杂的集成步骤。这为在下一代加速器上实现高效、可扩展的 AI 服务打开了大门。

### Hyungjun Kim：使用 vLLM 进行量化与评估

![](https://vllm.ai/blog-assets/figures/vllm-meetup/vllm_meetup_HJKim.jpg)

来自 SqueezeBits 的 Hyungjun Kim 探讨了量化如何成为 LLM 部署中不可或缺的一环，以及如何在 vLLM 生态中有效使用量化。他概述了用 vLLM 服务量化模型的两种主要方式：加载预量化模型进行服务，或者自行量化模型后再部署。

为了简化这一流程，vLLM 项目包含一个名为 LLM Compressor 的开源子项目，帮助开发者更轻松地把量化集成到自己的流水线中。
Hyungjun 还介绍了 Fits on Chips——SqueezeBits 推出的开源工具包，用于在 vLLM 内评估 LLM 服务性能。该工具包帮助对比吞吐量、延迟、准确率与硬件，让最高效的服务配置一目了然。

## 展望未来

![](https://vllm.ai/blog-assets/figures/vllm-meetup/image-2.png)

这次聚会也展望了韩国 vLLM 社区如何持续成长。我们计划与本地工程社区合作定期举办 vLLM Korea Meetup——包括 PyTorch Korea User Group 和 Python Korea。这些活动将包括动手工作坊、开发者聚会与小组研讨，旨在加深社区纽带，并促进对 vLLM 生态的技术贡献。

在开源早期，贡献的分布更为均衡。但随着 LLM 的兴起和对 AI 加速器的需求，个人工程师和学术界人士越来越难获得真实的实践经验。我们相信，通过社区驱动的基础设施与协作，我们可以打造一个可持续的、动手实践的学习环境——我们欢迎新的志愿者加入，共同塑造 vLLM 的未来。

![](https://vllm.ai/blog-assets/figures/vllm-meetup/image-6.png)

这次首届聚会是韩国 vLLM 社区激动人心的一步，再次印证了最重要的事情：为真实世界的 AI 服务提供实用、可扩展的解决方案。Rebellions、Red Hat 以及该地区满怀热情的工程师们，都将继续支持更多社区驱动的活动，并为 vLLM 项目持续贡献。

感谢每一位到场并让这次首次聚会取得成功的朋友——我们才刚刚起步。

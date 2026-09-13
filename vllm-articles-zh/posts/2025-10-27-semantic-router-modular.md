---
title: "从单体到模块化：用可扩展 LoRA 扩展语义路由"
title_en: "From Monolithic to Modular: Scaling Semantic Routing with Extensible LoRA"
source: https://vllm.ai/blog/2025-10-27-semantic-router-modular
crawled: 2026-09-12
translated: 2026-09-13
---

# 从单体到模块化：用可扩展 LoRA 扩展语义路由

> 原文：[From Monolithic to Modular: Scaling Semantic Routing with Extensible LoRA](https://vllm.ai/blog/2025-10-27-semantic-router-modular) · vLLM 博客

作者：Ivar Flakstad（Hugging Face）、OneZero-Y、Huamin Chen（Red Hat）、Xunzhuo Liu（腾讯）

[#生态](https://vllm.ai/blog/tags/ecosystem)

语义路由系统面临一个扩展性难题。当每个分类请求都需要独立运行多个微调模型时，计算成本会随模型数量线性增长。本文探讨 vLLM Semantic Router 最近对其基于 Rust 的分类层的一次重构，如何通过架构模块化、低秩适配（LoRA）和并发优化来解决这一问题。

## 背景：从 BERT 到模块化系统

先前的实现主要依赖 BERT 和 ModernBERT 进行意图分类与越狱（jailbreak）分类。ModernBERT 在英文文本分类任务上表现出色，但它有如下局限：

- 语言覆盖：与在更多样化数据集上训练的模型相比，原版 ModernBERT 的多语言支持有限。（注：[mmBERT](https://huggingface.co/blog/mmbert) 是 ModernBERT 的一个大规模多语言变体，支持 1800 多种语言，在本重构开始之后发布，代表了应对多语言挑战的另一种思路）
- 上下文长度：ModernBERT 借助 RoPE 将上下文扩展到 8,192 个 token（[来源](https://huggingface.co/docs/transformers/v4.49.0/en/model_doc/modernbert)），而 Qwen3-Embedding 等模型最多支持 32,768 个 token，这对超长文档处理很有帮助
- 模型耦合：分类逻辑与特定模型架构紧密耦合，难以添加新模型

这些约束促成了一次更大规模的重构，让系统在保持性能的同时支持多种模型类型。模块化架构意味着 mmBERT 等更新的模型可以与 Qwen3-Embedding、EmbeddingGemma 一同集成，让路由器能为每个任务选择最合适的模型。

## 架构重构

![](https://vllm.ai/blog-assets/figures/semantic-router/modular.png)

此次重构在 candle-binding crate 中引入了分层架构。这种结构实现了关注点分离：核心功能保持与具体模型无关，而新的模型架构可以在不修改现有代码的情况下加入。`DualPathUnifiedClassifier` 实现了路由逻辑，根据任务需求在传统微调模型与 LoRA 适配模型之间进行选择。

## 长上下文嵌入模型

两个新的嵌入模型解决了上下文长度的限制：

### Qwen3-Embedding

Qwen3-Embedding 支持最长 32,768 个 token 的上下文（[Hugging Face 模型卡](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)）。其实现使用了 RoPE（旋转位置编码，Rotary Position Embedding），通过在更长距离上更精细的频率分辨率，实现对扩展上下文的处理。

Qwen3-Embedding 在 100 多种语言的文本上训练（[Hugging Face 模型卡](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)），因此适合此前仅用 ModernBERT 时难以应付的多语言路由场景。

### EmbeddingGemma-300M

Google 的 EmbeddingGemma-300M 采取了不同路线：在保持质量的同时专注更小的模型体积。该模型支持 2,048 个 token 的上下文长度，并实现了 Matryoshka 表示学习（套娃表示学习），即无需重新训练即可将嵌入截断为 768、512、256 或 128 维（[Hugging Face 模型卡](https://huggingface.co/google/embeddinggemma-300m)）。

该架构使用带 3 个 query 头和 1 个 key-value 头的多查询注意力（MQA），降低了内存带宽需求。一个独特之处是在 transformer 块之后应用稠密瓶颈层（768 → 3072 → 768），基于 Matryoshka 训练方法提升嵌入质量。

## 面向多任务分类的低秩适配（LoRA）

LoRA 解决了先前系统中的一个根本性低效问题。当一个分类系统需要判断意图、检测 PII（个人身份信息）并检查安全问题时，朴素的做法是运行三个独立的微调模型：

![](https://vllm.ai/blog-assets/figures/semantic-router/full-params.png)

每个模型都让输入流经其完整网络，包括开销高昂的基础 transformer 层。这带来了 O(n) 的复杂度，其中 n 是分类任务的数量。

LoRA 通过共享基础模型的计算来改变这一点：

![](https://vllm.ai/blog-assets/figures/semantic-router/lora.png)

基础模型只运行一次，产生中间表示。随后每个 LoRA 适配器应用任务特定的低秩权重更新，使输出特化。由于 LoRA 适配器通常只修改模型参数的不到 1%，这最后一步比运行完整模型快得多。

parallel\_engine.rs 中的实现使用 [Rayon](https://github.com/rayon-rs/rayon) 进行数据并行，并发处理多个 LoRA 适配器。对于一个需要三个分类结果的请求，工作量从三次完整前向传播变为一次完整前向传播加三次轻量级适配器应用。

## 通过 `OnceLock` 实现并发

先前的实现使用 `lazy_static` 管理全局分类器状态，在并发负载下引入了锁竞争。重构后改用 Rust 标准库中的 [`OnceLock`](https://doc.rust-lang.org/std/sync/struct.OnceLock.html)。

`OnceLock` 在初始化之后提供无锁读取。首次初始化后，所有后续访问都只是简单的指针读取，没有任何同步开销。`oncelock_concurrent_test.rs` 中的测试用 10 个并发线程执行共 30 次分类验证了这一点，确认吞吐量随线程数线性扩展。

当路由器处理多个传入请求时，这一点非常重要。使用 `lazy_static` 时，并发请求会在互斥锁后排队。使用 `OnceLock` 时，它们可以无竞争地并行执行。

### 用于 GPU 加速的 Flash Attention

Flash Attention 2 支持作为 CUDA 构建的可选特性提供，但需要 Ampere 一代或更新的 GPU（计算能力 ≥ 8.0）。Flash Attention 通过把计算拆分成适合放进高速片上 SRAM 的块来处理，避免反复读取较慢的 GPU DRAM，从而优化注意力机制。

ModernBERT 和 Qwen3 都能从 Flash Attention 集成中获益：

- ModernBERT：自注意力计算最高快 3×，内存占用显著降低（[来源](https://medium.com/@alpernebikanli/some-berts-and-modernbert-39b261b1ce83)）。该模型还使用交替注意力模式（每三层一次全局注意力，其余为局部滑动窗口注意力），以在效率与上下文保留之间取得平衡（[来源](https://www.answer.ai/posts/2024-12-19-modernbert.html)）。
- Qwen3：集成 FlashAttention-2 可让注意力操作最高提速 4×。对 14B 版本而言，这意味着推理时从没有它时的 30-35 token/秒提升到 70-110 token/秒——上下文越长，这一性能提升越明显（[来源](https://qwen3lm.com/qwen3-flashattention2-inference-guide/)）。

Rust 实现通过 Cargo features 将 Flash Attention 设为可选项，既允许部署在没有兼容 GPU 的系统上，又能在硬件支持时获得可观的性能提升。

## 面向云原生生态的跨语言集成

核心分类引擎选用 Rust，并配合 Go FFI（外部函数接口）绑定，解决了云原生环境中一个实际的部署难题。

### 为什么用 Rust 做机器学习推理

Rust 为分类层提供了多重优势：

- 性能：凭借零成本抽象达到接近 C 的性能，这对低延迟推理至关重要
- 内存安全：编译期保证防止缓冲区溢出、释放后使用等常见 bug
- 并发：所有权系统杜绝数据竞争，让基于 Rayon 的安全并行处理成为可能
- 无垃圾回收：没有影响请求处理的 GC 停顿，延迟可预测

Candle 框架充分利用了 Rust 的这些优势，同时为机器学习模型开发提供熟悉的 API。

### Go FFI 绑定为何重要

Rust 擅长计算密集的机器学习推理，而 Go 在云原生基础设施生态中占主导地位。FFI 层连接了这两个世界。这种集成让系统能够部署在以 Go 为主要语言的环境中：

- Envoy 代理集成：语义路由器以 [Envoy 外部处理过滤器（external processing filter）](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter)的形式运行，用 Go 编写。FFI 让 Go 过滤器可以直接利用高性能的 Rust 分类能力，而无需重写整个 Envoy 集成层。
- Kubernetes Operator：云原生 Operator 通常用 Go 配合 controller-runtime 编写。FFI 让这些 Operator 可以直接嵌入分类逻辑，而不必向独立服务发起网络调用。
- 服务网格：Istio、Linkerd、Consul 等项目都基于 Go。FFI 让路由决策可以使用基于机器学习的分类，同时保持与现有网格控制平面的兼容。
- API 网关：许多 API 网关（Kong、Tyk）都有 Go 组件。FFI 让语义路由可以在网关层实现，无需引入额外的微服务。

### 部署灵活性

双语架构提供了多种部署选项：

- 嵌入模式：Go 服务通过 CGO 直接链接 Rust 库，最大限度降低延迟与部署复杂度
- 进程隔离：分类层可以作为独立进程运行，通过 gRPC 或 Unix 套接字通信，获得额外的故障隔离
- 混合工作负载：服务可以将 Go 的网络与编排优势同 Rust 的机器学习推理性能结合起来

语义路由器广泛采用了这一模式。主要的路由逻辑、配置管理和缓存实现用 Go 编写，而计算密集的分类部分用 Rust 运行。这种分离让每个组件都能使用最合适的语言，同时通过 FFI 层保持干净的接口。

## 性能特性

这种架构的收益因工作负载而异：

- 单任务与多任务分类：单任务时 LoRA 收益甚微，因为没有基础模型共享可言，传统微调模型可能更快。对同一输入执行多个分类时，LoRA 优势明显：由于基础模型只运行一次、每个任务只执行 LoRA 适配器，相比运行多个独立完整模型，开销大幅降低。实际加速比取决于基础模型计算与适配器计算的比例。
- 长上下文输入：Qwen3-Embedding 可以在不截断的情况下对最长 32K token 的文档做出路由决策，突破了 ModernBERT 8K 的限制，能应对超长文档。在兼容 GPU 上启用 Flash Attention 2 后，上下文越长，性能优势越显著。
- 多语言路由：模型现在能够为 ModernBERT 训练数据有限的语言做出路由决策。
- 高并发：`OnceLock` 消除了锁竞争，让分类操作的吞吐量随 CPU 核心数扩展。
- GPU 加速：启用 Flash Attention 2 后，注意力操作快 3-4×，且序列越长加速越明显。这使得 GPU 部署在高吞吐场景下尤其有利。

## 未来方向

模块化架构为多项扩展铺平了道路：

- 可以通过实现 `CoreModel` trait 添加更多嵌入模型
- 待 Candle 支持 Flash Attention 3 后提供支持
- 量化支持（4-bit、8-bit）以降低内存占用
- 面向特定领域路由的自定义 LoRA 适配器
- 面向更多语言（Python、Java、C++）的 FFI 绑定，扩展集成可能性

系统现在具备了在不更改架构的情况下纳入新研究进展的基础。FFI 层提供了稳定的接口，让 Rust 实现可以独立演进，同时与现有基于 Go 的部署保持兼容。

## 相关资源

- [项目仓库](https://github.com/vllm-project/semantic-router)
- [Candle 框架](https://github.com/huggingface/candle)
- [Qwen3-Embedding](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- [EmbeddingGemma](https://huggingface.co/google/embeddinggemma-300m)

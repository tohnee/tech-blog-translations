---
title: "SemiAnalysis InferenceMAX：vLLM 与 NVIDIA 携手加速 Blackwell 推理"
title_en: "SemiAnalysis InferenceMAX: vLLM and NVIDIA Accelerate Blackwell Inference"
source: https://vllm.ai/blog/2025-10-09-blackwell-inferencemax
crawled: 2026-09-12
translated: 2026-09-13
---

# SemiAnalysis InferenceMAX：vLLM 与 NVIDIA 携手加速 Blackwell 推理

> 原文：[SemiAnalysis InferenceMAX: vLLM and NVIDIA Accelerate Blackwell Inference](https://vllm.ai/blog/2025-10-09-blackwell-inferencemax) · vLLM 博客

作者：vLLM 团队

[#硬件](https://vllm.ai/blog/tags/hardware)[#性能](https://vllm.ai/blog/tags/performance)

### 引言

过去几个月，我们一直与 NVIDIA 紧密合作，以释放其最新的 NVIDIA Blackwell GPU 架构（B200/GB200）在使用 vLLM 进行大语言模型推理方面的全部潜力。Blackwell GPU 带来了一类全新的性能与效率改进，例如更高的内存带宽和原生 FP4 张量核心，为加速推理工作负载打开了激动人心的机会。

Blackwell 开箱即有出色性能，但为了从硬件中榨取更多，我们的联合优化重构了现有内核，并开发了面向更底层硬件利用率的新内核，解锁了额外性能并提升了效率。全新的 [SemiAnalysis InferenceMAX](https://github.com/InferenceMAX/InferenceMAX) 基准测试反映了这些改进：在 gpt-oss 120B 和 Llama 3.3 70B 等热门模型上，与上一代 Hopper GPU 相比，vLLM 在 Blackwell 上于相近延迟下实现了高达 **4x 的吞吐量提升**。

这项工作历时数月的工程协作，涉及横跨 vLLM 代码库的一百多个 pull request。我们与 NVIDIA 一起优化了推理流水线的几乎每一个环节——从自定义内核（注意力、GEMM、MoE）到高层调度与开销削减。本博客将详细拆解这些优化，以及它们如何把 Blackwell 的架构特性转化为生产环境中的性能收益。

### InferenceMAX 概览

SemiAnalysis InferenceMAX 是一个专为 LLM 服务性能自动化、周期性测试设计的基准测试框架，其结果每日更新，以反映软件性能的变化。这种方式缩小了软件更新与已发布基准数据之间的时间差，并使用一致的测试方法来确保公平、可复现的比较。

InferenceMAX 目前用两个代表性的开源模型评估 vLLM：

- 混合专家（MoE）：gpt-oss 120B
- 稠密（Dense）模型：Llama 3.3 70B

为了模拟真实使用场景，基准测试在多种提示/响应长度场景下运行每个模型（ISL = 输入序列长度，OSL = 输出序列长度）。具体而言，测试覆盖三种工况：

- 1K ISL / 1K OSL（聊天，中等输入/输出）
- 1K ISL / 8K OSL（推理，长输出）
- 8K ISL / 1K OSL（摘要，长输入）

### 在帕累托前沿全域交付性能

Blackwell 全新的计算架构带来了推理效率的阶跃式提升，采用了最新的 HBM3e 内存（每块 B200 配备 192 GB HBM3e，带宽 8 TB/s）、高速 NVLink 数据传输（每 GPU 1.8 TB/s），并通过第 5 代张量核心内置对 FP4 精度格式的支持。

通过调整我们的内核以充分利用这些进步，与在先前的 Hopper 架构上运行 vLLM 相比，我们在吞吐量（单 GPU 性能）与响应速度（单请求延迟）上均看到了显著的提升。

现代推理工作负载在序列长度、批大小和并发度上差异巨大。产生最高吞吐量的配置往往不是给用户提供最低延迟的配置。因此，单点指标可能产生误导。SemiAnalysis InferenceMAX 采用**帕累托前沿（Pareto frontier）方法论**来评估响应速度与吞吐量之间的权衡，描绘 Blackwell 在真实运行条件下的性能包络。

我们与 NVIDIA 合作的首要目标，是确保 vLLM 充分利用 Blackwell 的特性，在整个帕累托前沿上都有出色表现。

令人振奋的是，SemiAnalysis 的基准结果显示，对于 gpt-oss 120B 和 Llama 3.3 70B 两个模型，在所有交互性水平上，vLLM 在 Blackwell 上相比上一代 Hopper 架构都有一致的性能提升。

![](https://vllm.ai/blog-assets/figures/blackwell-inferencemax/gpt-oss-120b-1k-1k.png)

*图 1：SemiAnalysis InferenceMax 的 gpt-oss-120b 帕累托前沿，对比 vLLM 在 Blackwell 与 Hopper 上 1k/1k ISL/OSL、宽交互性范围下的性能。结果显示，vLLM 在 Blackwell 上相比 Hopper 吞吐量最高提升 4.3x。*

![](https://vllm.ai/blog-assets/figures/blackwell-inferencemax/llama-70b-1k-8k.png)

*图 2：SemiAnalysis InferenceMax 的 Llama 3.3 70B 帕累托前沿，对比 vLLM 在 Blackwell 与 Hopper 上 1k/8k ISL/OSL、宽交互性范围下的性能。结果显示，vLLM 在 Blackwell 上相比 Hopper 吞吐量最高提升 3.7x。*

**这些性能提升如今即可复现**，只需使用 SemiAnalysis 提供的 InferenceMAX 配置。这证明了专注于从硬件中榨取最大价值的优化软件所能达到的高度。要达到这些数字，需要在 vLLM 中进行广泛的优化，这些优化是与 NVIDIA 工程师深度协作完成的。下面我们介绍其中最重要的几项优化。

### vLLM 的 Blackwell 优化

要在 Blackwell 上实现上述性能，需要在软件栈的各个层面开展工作。有些优化提升 GPU 上内核的原始执行速度，有些则减少 CPU 开销或更好地利用硬件特性。下面我们列出迄今为止 vLLM 为支持 Blackwell 而引入的关键增强：

**性能改进**

- **借助 [FlashInfer](https://github.com/flashinfer-ai/flashinfer) 实现更快的内核：** 我们集成了 NVIDIA 的 FlashInfer 库，引入了大量高性能内核，包括用于 GQA 和 MLA 的 FP8 注意力、快速 FP8 与 FP4 GEMM、MoE 内核以及融合操作。例如，我们能够把 AllReduce、RMSNorm 和量化合并到单次内核启动中，从而显著改善延迟。这些内核来自 NVIDIA 软件栈的广泛部分，包括 CUTLASS、CuTeDSL、cuBLAS、cuDNN 和 TRTLLM。
- **更智能的图融合：** 扩展 vLLM 的 torch.compile 图融合，现在涵盖 Attention + 输出量化（Output Quant）、AllReduce + RMSNorm + 量化等算子模式，无需手动修改模型即可获得融合内核性能，更重要的是可以泛化到各种模型架构。
- **用异步调度降低主机端开销：** `--async-scheduling` 现在可以让模型执行与主机端开销完全重叠，消除了此前由同步造成的 GPU 空闲时间。**这使工作负载完全流水线化**：当一个批次在 GPU 上运行推理时，下一个批次的数据正在并行准备。

**易用性改进**

- **自动量化与后端选择：** vLLM 会自动检测模型是否使用了量化以选择正确的后端，并为你的 GPU 选择最优注意力后端。例如在 Blackwell 上，vLLM 会在可用时选择基于 FlashInfer 的注意力（纳入 NVIDIA 的 TensorRT-LLM 内核），必要时回退到 FlashAttention——无需手动设置标志或调整环境变量。
- **FlashInfer GEMM 与 MoE 的自动调优：** 由于理想的内核实现可能高度依赖批大小和序列长度，我们在 vLLM 的 GPU runner 中加入了自动调优机制。启动期间，FlashInfer 会通过基准测试与内核筛选进行自动策略选择，即使推理期间 ISL/OSL 不断变化也能确保峰值性能。
- [**快速上手指南（Quick Start Recipes）**](https://github.com/vllm-project/recipes)**，轻松实现优化部署：** 除了代码改动之外，我们还与社区合作，为常见场景编写了快速上手配置指南。针对给定硬件上每个模型的清晰说明，引导用户以推荐设置启动服务器、调参、验证准确率并进行性能基准测试——简化部署步骤，更快拿到结果。

### 进行中的工作

上述每一项优化本身都是一个重要项目，都需要密切的技术协作——而这还不是全部！我们与 NVIDIA 的合作仍在继续，大量改进即将到来。

展望未来，我们正致力于通过投机解码和数据+专家并行（DEP）配置，为 DeepSeek、Qwen、gpt-oss 等更多模型在集群规模推理上解锁可观的吞吐量提升。借助采用 Eagle 投机解码的 NVIDIA gpt-oss-120b-Eagle3-v2，我们预计吞吐量可获得高达约 2-3x 的改进。利用 DEP——它得益于 Blackwell 中 1,800 GB/s 的低延迟 NVLink GPU 间互连——我们期待释放比 InferenceMAX 基准所示更高的性能与并发度，为更快、更高效的推理铺平道路。

得益于 vLLM 与 NVIDIA 持续的优化与协作，Blackwell 上的性能改进每天都在发生。我们会不断发掘新的机会，在效率与规模上把 Blackwell 平台推向极限。

### 致谢

我们要感谢 vLLM 社区中众多才华横溢、在这项工作中携手合作的人：

- Red Hat：Michael Goin、Alexander Matveev、Lucas Wilkinson、Luka Govedič、Wentao Ye、Ilia Markov、Matt Bonanni、Varun Sundar Rabindranath、Bill Nell、Tyler Michael Smith、Robert Shaw
- NVIDIA：Po-Han Huang、Pavani Majety、Shu Wang、Elvis Chen、Zihao Ye、Duncan Moss、Kaixi Hou、Siyuan Fu、Benjamin Chislett、Xin Li、Vadim Gimpelson、Minseok Lee、Amir Samani、Elfie Guo、Lee Nau、Kushan Ahmadian、Grace Ho、Pen Chun Li
- vLLM：Chen Zhang、Yongye Zhu、Bowen Wang、Kaichao You、Simon Mo、Woosuk Kwon、Zhuohan Li
- Meta：Yang Chen、Xiaozhu Meng、Boyuan Feng、Lu Fang

所有 InferenceMAX 结果可在 <http://inferencemax.ai> 查看。运行它的代码已在 <https://github.com/InferenceMAX/InferenceMAX> 开源。他们对结果的解读见 <https://newsletter.semianalysis.com/p/inferencemax-open-source-inference>。

我们衷心感谢 SemiAnalysis 团队将软硬件协同设计推向新的高度，为社区提供公平的测量与比较。感谢 Kimbo Chen、Dylan Patel 以及其他成员。

我们期待在未来几周和几个月里继续完善并扩展我们的优化，解锁更强大的能力！

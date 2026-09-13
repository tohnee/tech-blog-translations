---
title: "使用 vLLM 在 Intel Arc Pro B 系列 GPU 上实现快速且实惠的 LLM 服务"
title_en: "Fast and Affordable LLMs serving on Intel Arc Pro B-Series GPUs with vLLM"
source: https://vllm.ai/blog/2025-11-11-intel-arc-pro-b
crawled: 2026-09-12
translated: 2026-09-13
---

# 使用 vLLM 在 Intel Arc Pro B 系列 GPU 上实现快速且实惠的 LLM 服务

> 原文：[Fast and Affordable LLMs serving on Intel Arc Pro B-Series GPUs with vLLM](https://vllm.ai/blog/2025-11-11-intel-arc-pro-b) · vLLM 博客

Intel vLLM 团队

[#硬件](https://vllm.ai/blog/tags/hardware)

[Intel® Arc™ Pro B 系列 GPU 家族](https://www.intel.com/content/www/us/en/products/docs/discrete-gpus/arc/workstations/b-series/overview.html)以易用性和出色的性价比为核心，提供强大的 AI 能力。其大容量显存以及多 GPU 配置的可扩展性，使得在本地运行最新、最大且能力强大的 AI 模型成为可能，让希望在无需承担 AI 硬件高昂溢价的情况下部署大语言模型（LLM）的专业人士也能用上先进的 AI 推理。

vLLM 是在 Intel Arc Pro B 系列 GPU 上实现快速且低成本 LLM 服务的软件栈核心。过去几个月里，Intel 开发者一直与 vLLM 社区积极合作，启用并优化关键特性，确保多 GPU 扩展和 PCIe P2P 数据传输在 Intel Arc Pro B 系列 GPU 上的流畅性能。

Intel® Arc™ Pro B 系列 GPU 为 vLLM 提供的关键特性与优化包括：

- DeepSeek 蒸馏的 Llama/Qwen 模型具有扎实的推理性能
- 长上下文长度（>50K），且批大小扩展性良好
- 支持嵌入（embedding）、重排序（reranker）、池化（pooling）模型
- 支持多模态模型
- 对混合专家（MoE）模型优化良好（GPT-OSS、DeepSeek-v2-lite、Qwen3-30B-A3B 等）
- 逐层在线量化以降低所需显存
- 支持数据并行、张量并行与流水线并行
- Torch.compile 的 FP16 与 BF16 路径支持
- 投机解码，支持 n-gram、EAGLE 与 EAGLE3 方法
- 异步调度
- 预填充/解码分离（Prefill/Decode disaggregation）
- 低秩适配器（LoRA）
- 推理输出（reasoning output）
- 休眠模式（Sleep mode）
- 结构化输出
- 工具调用
- 对 BF16、FP16、INT4 与 FP8 vLLM 配方的混合精度支持

## 面向 MoE 模型的高级优化

混合专家（MoE）是一种模型架构方法：多个专长化的专家网络在门控机制的引导下协同处理输入序列。对于输入序列中的每个 token，门控网络会动态选择应由哪个专家子集来处理该 token。MoE 架构并不依赖单一稠密前馈层，而是采用分布在多个专家网络上的并行 GEMM 运算来实现同等的计算功能。这种设计为模型引入了结构化稀疏性，因为对任何给定输入而言，只有一部分专家被激活，从而在保持模型容量的同时提高计算效率。除了针对通用矩阵乘法（GEMM）和 Flash Attention 的通用优化外，这些 MoE 组件（专家与门控网络）正是 MoE 语言模型的关键性能决定因素。

![moe_diagram](https://vllm.ai/blog-assets/figures/2025-vllm-on-intel-arc/moe.png)

moe\_diagram（MoE 示意图）

然而，朴素的 MoE GEMM 实现可能存在显著的效率瓶颈。典型做法是在 for 循环中每次迭代依次启动单个 GEMM 内核，这会产生过多的内核启动开销，并引入可观的调度延迟。此外，由于专家路由决策由门控网络生成，GEMM 运算必须等待门控计算完成后才能开始执行。这种数据依赖会造成流水线停顿，扰乱内核执行流，严重限制 GPU 的并行度，使设备无法达到最优利用率。

针对这些 MoE GEMM 的局限，我们设计了一个持久化零间隙内核（persistent zero gap kernel），在 Intel® Arc™ Pro B60 GPU 上实现了超过硬件容量 80% 的效率。

### 优化 1：在持久化循环中启动单个内核

单内核设计可以消除上述启动与调度开销。同时，持久化循环免去了启动参数对专家路由网络结果的依赖。这些都有助于保持最大的设备并行度。

在使用持久化内核之前，可以看到主机等待造成的设备空闲
![kernel trace](https://vllm.ai/blog-assets/figures/2025-vllm-on-intel-arc/persistent-kernel1.png)

kernel trace（内核轨迹）

启用持久化后，设备持续保持忙碌：
![kernel trace](https://vllm.ai/blog-assets/figures/2025-vllm-on-intel-arc/persistent-kernel2.png)

kernel trace（内核轨迹）

Intel® Arc™ Pro B60 GPU 拥有 20 个 XeCore，每个 XeCore 具有相同的资源，可承载多个 SYCL 工作组。在我们的设计中，每个 XeCore 启动两个工作组，以平衡计算与内存带宽需求。

### 优化 2：计算组的动态均衡

一个观察是：由于专家路由的不均衡，每个工作组执行的工作量各不相同。如果一个工作组以固定步长循环取任务，那么总有一个组承担最多的工作，而另一个组承担最少。两者之间的差距会不断累积，最高可达 MoE GEMM 总时间的 15%。更好的替代方案是：任何一个组在一轮循环中完成一个任务后，立即开始下一轮循环中最早可用的任务。
举个具体例子：40 个工作组要处理 200 个 GEMM 块，静态步长会使组 0 依次处理 0、40、80……，组 1 依次处理 1、41、81……等。但要注意，由于 MoE 的特性，每个 GEMM 块的计算强度可能并不相同。此外，随机化的访问模式也会让某些组比其他组更快完成工作。这就限制了效率：总是更早完成任务的组，无法帮助那些总是承担重负载的组。

| 优化前 | 优化后 |
| --- | --- |
| thread load  thread load | thread load  thread load |

我们通过让每个组通过一个原子数竞争下一个任务来缓解这一影响。任何完成一个 GEMM 块计算的组都会从原子数中获得一个序号，该序号决定它将取下一个哪个块。这样一来，我们消除了内核循环中的小间隙，在所有专家路由场景下都实现了完美调度。

### 优化 3：带预打包的快速 MXFP4 到 BFLOAT16 算法，提高内存加载效率

预打包（prepacking）长期以来被认为可以提高内存加载效率。对于 4 位内存加载，一种对硬件友好的格式最多可将效率提升 30%（如我们实测所见）。此外，朴素的 FP4 到 BF16 转换需要太多指令，因此需要更好的替代方案（借鉴自 oneDNN：在单精度 E/M 位上做步进 E2M1 编码，并乘以两种类型之间的指数差）：

`Bitcast-bf16 ((x << 12) >> 6 & 0x81c0) * 2^126`

该方案将 fp4 转换为 bf16 所需的指令数量降到最少。

## 性能

凭借 24GB 高带宽显存、456 GB/s 内存带宽以及 160 个 Intel® Xe 矩阵扩展（Intel® XMX）AI 引擎，Intel Arc Pro B 系列 GPU 为在 vLLM 上优化热门模型提供了良好的硬件能力。完整的支持模型列表见 [intel/ai-containers](https://github.com/intel/ai-containers/blob/main/vllm/0.10.2-xpu.md#supported-models)

从 8B 到 70B 的 DeepSeek 蒸馏模型已针对配备八张 Intel® Arc™ Pro GPU 的系统上的输出 token 吞吐量进行了优化。

![model perf](https://vllm.ai/blog-assets/figures/2025-vllm-on-intel-arc/perf-figure1.png)

model perf（模型性能）


图 1：在配备 8 张 Intel® Arc™ Pro B60 GPU 卡的系统上，满足 SLA 的最大并发下的 FP8 模型输出 token 吞吐量。

该系统在良好并发负载下可将下一个 token 延迟保持在 100 ms 以内。

![model perf](https://vllm.ai/blog-assets/figures/2025-vllm-on-intel-arc/perf-figure2.png)

model perf（模型性能）


图 2：在配备 4 张 Intel® Arc™ Pro B60 GPU 卡的系统上，Qwen-32B 随提示数量增加的下一个 token 延迟。

模型推理在从 1K 到超过 40K token 的宽泛输入序列长度范围内，都能保持一致的下一个 token 延迟。这一性能得益于高度优化的 flash attention 内核，它们在序列长度维度上并行化运算。

![model perf](https://vllm.ai/blog-assets/figures/2025-vllm-on-intel-arc/perf-figure3.png)

model perf（模型性能）


图 3：在配备 8 张 Intel® Arc™ Pro B60 GPU 卡的系统上，llama-70B 单批次在 1K 到 40K 长上下文输入下的 TTFT/TPOT。

GPT-OSS：Intel® Arc™ Pro B60 GPU 在 OpenAI 近期发布的 GPT-OSS 模型上也展现了出色的性能，如下表所示，为开发者和企业提供了强大且经济高效的大规模 AI 推理方案。

| 模型 | 数据类型 | TP | 输入/输出序列长度 | 并发 | TTFT (s) | TPOT (ms) | 输出 Token 吞吐量 (toks/s) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-OSS-20b | MXFP4 | 1 | 1024/1024 | 75 | 7.614 | 53.96 | 1210.74 |
| GPT-OSS-20b | MXFP4 | 1 | 2048/2048 | 38 | 7.823 | 42.35 | 818.92 |
| GPT-OSS-20b | MXFP4 | 1 | 5120/5120 | 15 | 8.36 | 34.27 | 416.94 |
| GPT-OSS-120b | MXFP4 | 4 | 1024/1024 | 100 | 8.04 | 58.78 | 1495.12 |
| GPT-OSS-120b | MXFP4 | 4 | 2048/2048 | 50 | 8.11 | 41.98 | 1085.58 |
| GPT-OSS-120b | MXFP4 | 4 | 5120/5120 | 20 | 8.60 | 30.60 | 619.10 |

表 1：在 x8 Intel® Arc™ Pro B 系列系统上使用 1-4 块 GPU 的 GPT-OSS vLLM 推理吞吐量。

MLPerf：Intel Arc Pro B 系列 GPU 在近期发布的 MLPerf Inference v5.1 结果中表现亮眼（[链接](https://mlcommons.org/benchmarks/inference-datacenter/)）。在 Llama 8B 上，Intel® Arc™ Pro B60 GPU 展现出每美元性能优势。这些结果以 vLLM 作为服务框架实现。

## 如何搭建

支持 Intel XPU 的 vllm docker 镜像可从 [intel/vllm - Docker Image | Docker Hub](https://hub.docker.com/r/intel/vllm) 下载。自 vllm 0.10.2 docker 版本起支持 gpt-oss 等 MoE 模型。以下示例要求主机操作系统为 Ubuntu 25.04，KMD 驱动版本为 6.14.0，运行在配有 4 张插入 PCIe 插槽的 Intel® Arc™ Pro B60 GPU 卡的 Xeon 系统上。

使用以下命令获取发布的 docker 镜像

```
docker pull intel/vllm:0.10.2-xpu
```

使用以下命令实例化 docker 容器

```
docker run -t -d --shm-size 10g --net=host --ipc=host --privileged -v /dev/dri/by-path:/dev/dri/by-path --name=vllm-test --device /dev/dri:/dev/dri --entrypoint= intel/vllm:0.10.2-xpu /bin/bash
```

在 4 张 Intel® Arc™ Pro B60 卡上运行 gpt-oss-120b 的 vllm 服务器

```
vllm serve openai/gpt-oss-120b --dtype=bfloat16 --enforce-eager --port 8000 --host 0.0.0.0 --trust-remote-code --gpu-memory-util=0.9 --no-enable-prefix-caching --max-num-batched-tokens=8192 --disable-log-requests --max-model-len=16384 --block-size 64 -tp 4
```

另开一个 shell 并运行基准测试

```
vllm bench serve --model openai/gpt-oss-120b --dataset-name sonnet --dataset-path="./benchmarks/sonnet.txt" --sonnet-input-len=1024 --sonnet-output-len=1024 --ignore-eos --num-prompt 1 --trust_remote_code --request-rate inf --backend vllm --port=8000 --host 0.0.0.0
```

更多经验证的支持模型列表见：[支持模型](https://github.com/intel/ai-containers/blob/main/vllm/0.10.2-xpu.md#supported-models)

## 展望未来

我们承诺不断深化自身优化与 vLLM 核心项目之间的集成。我们的路线图包括：为上游 vLLM 特性提供完整支持，为广泛的模型——尤其是 Intel® 硬件上的热门高性能 LLM——交付最先进的性能优化，并将我们的增强积极回馈给 vLLM 上游社区。

## 致谢

我们衷心感谢整个 vLLM 团队。他们开创性的工作为 LLM 服务树立了新的标准。他们的开放与支持使我们得以有效贡献，我们真心感谢他们在这一事业中的伙伴关系。

## 声明与免责声明

性能因使用方式、配置及其他因素而异。详情请访问 [www.Intel.com/PerformanceIndex](http://www.Intel.com/PerformanceIndex)。
性能结果基于配置所示日期的测试，可能无法反映所有公开发布的更新。详情请访问 [MLCommons](https://mlcommons.org/)。任何产品或组件都无法做到绝对安全。
Intel 技术可能需要启用相应的硬件、软件或服务激活。

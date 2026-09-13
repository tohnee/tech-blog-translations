---
title: "Docker Model Runner 集成 vLLM，实现高吞吐量推理"
title_en: "Docker Model Runner Integrates vLLM for High-Throughput Inferencing"
source: https://vllm.ai/blog/2025-11-19-docker-model-runner-vllm
crawled: 2026-09-12
translated: 2026-09-13
---

# Docker Model Runner 集成 vLLM，实现高吞吐量推理

> 原文：[Docker Model Runner Integrates vLLM for High-Throughput Inferencing](https://vllm.ai/blog/2025-11-19-docker-model-runner-vllm) · vLLM 博客

Docker 团队

## 扩展 Docker Model Runner 的能力

今天，我们很高兴地宣布：Docker Model Runner 现已集成 vLLM 推理引擎与 safetensors 模型，让你用已经在用的 Docker 工具即可解锁高吞吐量 AI 推理。

当我们首次推出 Docker Model Runner 时，目标是让开发者能够简单地用 Docker 运行和实验大语言模型（LLM）。我们从第一天起就将其设计为可集成多个推理引擎，从 llama.cpp 开始，让模型在任何地方跑起来都很容易。

现在，我们在这条路上迈出了下一步。通过 vLLM 集成，你可以把 AI 工作负载从低端硬件一路扩展到高端 Nvidia 硬件，而完全不必离开你的 Docker 工作流。

## 为什么选择 vLLM？

vLLM 是一个高吞吐量的开源推理引擎，旨在高效、大规模地服务大语言模型。凭借对吞吐量、延迟和内存效率的关注，它被业界广泛用于部署生产级 LLM。

以下是 vLLM 的突出之处：

- **优化的性能**：使用 PagedAttention，一种先进的注意力算法，可最大限度减少内存开销并最大化 GPU 利用率。
- **可扩展的服务**：原生支持批量请求与流式输出，非常适合交互式与高流量 AI 服务。
- **模型灵活性**：与 GPT-OSS、Qwen3、Mistral、Llama 3 等流行的开放权重模型以及 safetensors 格式的其他模型无缝协作。

通过将 vLLM 带入 Docker Model Runner，我们正在弥合快速本地实验与稳健生产推理之间的鸿沟。

## vLLM 如何工作

用 Docker Model Runner 运行 vLLM 模型非常简单：安装后端、运行模型即可，无需任何特殊设置。

安装带 vLLM 后端的 Docker Model Runner：

```
docker model install-runner --backend vllm --gpu cuda
```

安装完成后，即可立即开始使用：

```
docker model run ai/smollm2-vllm "Can you read me?"
```

```
Sure, I am ready to read you.

```

或者通过 API 访问：

```
curl --location 'http://localhost:12434/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
  "model": "ai/smollm2-vllm",
  "messages": [
    {
      "role": "user",
      "content": "Can you read me?"
    }
  ]
}'
```

请注意，HTTP 请求和 CLI 命令中都没有任何对 vLLM 的引用。

这是因为 Docker Model Runner 会根据你所使用的模型自动将请求路由到正确的推理引擎，无论你使用的是 llama.cpp 还是 vLLM，都能获得无缝体验。

## 为什么要多个推理引擎？

在此之前，开发者只能在简单性与性能之间二选一：要么轻松运行模型（使用 Docker Model Runner 搭配 llama.cpp 这类简化、可移植的工具），要么获得最大吞吐量（使用 vLLM 这类框架）。

现在，Docker Model Runner 让你两者兼得。

你可以：

- 用 llama.cpp 在本地做原型。
- 用 vLLM 扩展到生产环境。

全程使用同一套一致的 Docker 命令、CI/CD 工作流和部署环境。

这种灵活性使 Docker Model Runner 成为业界首创——没有任何其他工具能让你在单一、可移植、容器化的工作流中切换多个推理引擎。

通过把这些引擎统一在一个接口之下，Docker 正在让 AI 真正可移植——从笔记本电脑到集群，以及介于其间的任何场景。

## Safetensors（vLLM）与 GGUF（llama.cpp）：如何选择正确的格式

随着 vLLM 的加入，Docker Model Runner 现已兼容两大最主流的开源模型格式：Safetensors 和 GGUF。虽然 Model Runner 为你抽象掉了引擎搭建的复杂性，但理解这两种格式的差异有助于为自己的基础设施选择合适的工具。

- **GGUF（GPT-Generated Unified Format）**：llama.cpp 的原生格式，GGUF 为高可移植性和量化而设计。它非常适合在内存带宽有限的大众硬件上运行模型。它将模型架构和权重打包进单个文件。
- **Safetensors**：vLLM 的原生格式，也是高端推理的现代标准，safetensors 为高吞吐量性能而生。

Docker Model Runner 会智能地路由你的请求：如果你拉取 GGUF 模型，它就使用 llama.cpp；如果你拉取 safetensors 模型，它就调用 vLLM 的威力。使用 Docker Model Runner，两者都可以作为 OCI 镜像推送到任意 OCI registry 或从中拉取。

## Docker Hub 上的 vLLM 兼容模型

vLLM 模型采用 safetensors 格式。Docker Hub 上目前已提供的一些早期 safetensors 模型：

- [ai/smollm2-vllm](https://hub.docker.com/r/ai/smollm2-vllm)
- [ai/qwen3-vllm](https://hub.docker.com/r/ai/qwen3-vllm)
- [ai/gemma3-vllm](https://hub.docker.com/r/ai/gemma3-vllm)
- [ai/gpt-oss-vllm](https://hub.docker.com/r/ai/gpt-oss-vllm)

## 现已可用：搭载 Nvidia 的 x86\_64

我们的首个版本针对运行 x86\_64 架构并配备 Nvidia GPU 的系统进行了优化，并已在这些系统上可用。我们的团队致力于在这一平台上打造坚如磐石的体验，相信你能感受到其中的差别。

## 接下来是什么？

这次发布只是一个开始。我们的 vLLM 路线图聚焦于两个关键方向：扩展平台覆盖范围和持续的性能调优。

- **WSL2/Docker Desktop 兼容性**：我们知道，流畅的「内环」开发体验对开发者至关重要。我们正积极通过 WSL2 把 vLLM 后端带到 Windows 上。这将让你能够在 Docker Desktop 上构建、测试和原型化高吞吐量 AI 应用，工作流与你在 Linux 环境中使用的完全一致，从 Nvidia Windows 机器开始。
- **DGX Spark 兼容性**：我们正在针对不同类型的硬件优化 Docker Model Runner。我们正在努力增加对 Nvidia DGX 系统的兼容性。
- **性能优化**：我们也在持续追踪可以改进的领域。虽然 vLLM 提供了惊人的吞吐量，但我们知道它的启动时间目前比 llama.cpp 慢。这是我们未来改进中要优化的关键领域之一，以缩短快速开发周期中的「首个 token 时间」。

感谢大家在我们成长过程中给予的支持与耐心。

## 如何参与

Docker Model Runner 的力量源于其社区，而成长空间永远存在。我们需要你的帮助，让这个项目做到最好。参与方式：

- **为仓库加星**：通过为 [Docker Model Runner 仓库](https://github.com/docker/model-runner)加星来表示支持，帮助我们获得更多关注。
- **贡献你的想法**：对新功能或 bug 修复有想法？创建一个 issue 来讨论。或者 fork 仓库、完成修改并提交 pull request。我们期待看到你的想法！
- **广而告之**：告诉你的朋友、同事，以及任何有兴趣用 Docker 运行 AI 模型的人。

我们对 Docker Model Runner 的新篇章感到无比兴奋，迫不及待想看到我们能一起构建什么。开工吧！

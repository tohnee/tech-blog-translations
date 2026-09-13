---
title: "NVIDIA DGX Spark 深度评测：本地 AI 推理的新标准"
title_en: "NVIDIA DGX Spark In-Depth Review: A New Standard for Local AI Inference"
author: "Jerry Zhou and Richard Chen"
date: "October 13, 2025"
previewImg: /images/blog/nvidia_dgx_spark/product_1.jpg
source: https://lmsys.org/blog/2025-10-13-nvidia-dgx-spark/
translated: 2026-09-12
---

# NVIDIA DGX Spark 深度评测：本地 AI 推理的新标准

> 原文：[NVIDIA DGX Spark In-Depth Review: A New Standard for Local AI Inference](https://lmsys.org/blog/2025-10-13-nvidia-dgx-spark/) · LMSYS Blog · Jerry Zhou and Richard Chen

得益于 NVIDIA 的早期体验计划，我们非常高兴第一时间拿到了 NVIDIA DGX™ Spark。这是一台相当特立独行的系统——NVIDIA 很少推出如此紧凑的一体机，把超级计算机级别的性能装进桌面工作站的外形之中。

过去一年里，SGLang 在数据中心领域的开发者群体迅速扩大，并凭借出色的性能获得推理社区的认可。SGLang 成功地以预填充-解码分离（PD 分离）与专家并行（EP）大规模部署 DeepSeek，先后运行在 <a href="https://lmsys.org/blog/2025-05-05-large-scale-ep/" target="_blank">**由 96 张 NVIDIA H100 GPU 组成的集群**</a>和最新的 <a href="https://lmsys.org/blog/2025-09-25-gb200-part-2/" target="_blank">**GB200 NVL72 系统**</a>上，不断突破大规模推理性能与开发者生产力的边界。

受 DGX Spark 能力的启发，SGLang 首次将版图从数据中心扩展到消费级市场，把久经验证的推理框架直接交到全球开发者和研究者手中。在这篇评测中，我们将近距离审视这台精美的机器，从外观设计到性能表现与使用场景。

> 也欢迎观看我们的<a href="https://youtu.be/-3r2woTQjec" target="_blank">视频评测</a>。

![](/images/blog/nvidia_dgx_spark/product_1.jpg)

## 外观

DGX Spark 是一件赏心悦目的工程作品。它采用全金属机身，配以优雅的香槟金涂装。前后面板均由金属泡沫制成，让人联想到 NVIDIA DGX A100 和 H100 的设计。

机身背面提供了令人印象深刻的丰富接口：一个电源按钮、四个 USB-C 接口（最左侧一个支持最高 **240 W 的供电功率**）、一个 HDMI 接口、一个 **10 GbE RJ-45 以太网接口**，以及**由 NVIDIA ConnectX-7 网卡驱动的两个 QSFP 接口，带宽最高可达 200 Gbps**。这些接口让两台 DGX Spark 可以互联起来，从而运行更大的 AI 模型。

采用 USB Type-C 供电是一个特别有趣的设计选择，在其他桌面机身上几乎闻所未闻。Mac Mini 或 Mac Studio 等同类产品依赖标准的 C5/C7 电源接口，那种接口牢固得多，但也笨重得多。NVIDIA 选择 USB-C 很可能是为了把电源外置，为散热系统腾出宝贵的内部空间。不过代价是，你得格外小心，别一不小心把电源线扯松了。

![](/images/blog/nvidia_dgx_spark/product_2.jpg)

## 硬件能力

在硬件方面，DGX Spark 在其尺寸和功耗约束下展现了惊人的性能。它的核心是专为这台设备设计的 NVIDIA GB10 Grace Blackwell 超级芯片，集成了 10 颗 Cortex-X925 性能核心和 10 颗 Cortex-A725 能效核心，共计 20 个 CPU 核心。

GPU 方面，GB10 可提供高达 **1 PFLOP 的稀疏 FP4 张量算力**，其 AI 能力大致介于 RTX 5070 与 5070 Ti 之间。最亮眼的设计是 **128 GB 一致性统一系统内存**，由 CPU 和 GPU 无缝共享。这一统一架构让 DGX Spark 可以直接加载并运行大模型，省去了系统内存到显存之间的数据搬运开销。借助聚合带宽 200 Gb/s 的双 QSFP 以太网接口，两台 DGX Spark 可以互联组成一个小型集群，对更大的模型进行分布式推理。据 NVIDIA 介绍，两台互联的 DGX Spark 可以处理 **FP4 精度下高达 4050 亿参数**的模型。

不过，这台机器唯一的短板在于内存带宽：统一内存采用 LPDDR5x，最高 **273 GB/s**，且由 CPU 和 GPU 共享。正如后文所示，这一受限的带宽被预计（并已被实测证实）是 AI 推理性能的关键瓶颈。尽管如此，128 GB 的内存让 DGX Spark 能够运行那些对大多数桌面系统而言过于庞大的模型。

![](/images/blog/nvidia_dgx_spark/product_3.jpg)

## 性能

我们使用 **SGLang** 和 **Ollama** 在 DGX Spark 上对多个开放权重大语言模型进行了基准测试。结果显示，DGX Spark 虽然确实能加载并运行很大的模型，例如 **GPT-OSS 120B** 和 **Llama 3.1 70B**，但这类负载更适合**原型验证与实验**，而非生产环境。DGX Spark 真正大放异彩的场景是服务**较小的模型**，尤其是在利用**批处理**最大化吞吐量的时候。

### 测试方法

> ⚠️ **注意：** 由于针对 DGX Spark 的软件支持仍处于早期阶段，本节的基准测试结果可能会随着后续软件更新在性能与兼容性上的改进而过时。

#### 测试设备

我们准备了以下系统进行基准测试：

* **NVIDIA DGX Spark**  
* **NVIDIA RTX PRO™ 6000 Blackwell Workstation Edition**  
* **NVIDIA GeForce RTX 5090 Founders Edition**  
* **NVIDIA GeForce RTX 5080 Founders Edition**  
* **Apple Mac Studio（M1 Max，64 GB 统一内存）**  
* **Apple Mac Mini（M4 Pro，24 GB 统一内存）**

#### 基准测试模型

我们使用 **SGLang** 与 **Ollama** 两个框架评估了多种开放权重大语言模型，汇总如下：

| 框架 | 批大小 | 模型与量化 |
| :---- | :---- | :---- |
| **SGLang** | 1–32 | Llama 3.1 8B (FP8)<br>Llama 3.1 70B (FP8)<br>Gemma 3 12B (FP8)<br>Gemma 3 27B (FP8)<br>DeepSeek-R1 14B (FP8)<br>Qwen 3 32B (FP8) |
| **Ollama** | 1 | GPT-OSS 20B (MXFP4)<br>GPT-OSS 120B (MXFP4)<br>Llama 3.1 8B (q4\_K\_M / q8\_0)<br>Llama 3.1 70B (q4\_K\_M)<br>Gemma 3 12B (q4\_K\_M / q8\_0)<br>Gemma 3 27B (q4\_K\_M / q8\_0)<br>DeepSeek-R1 14B (q4\_K\_M / q8\_0)<br>Qwen 3 32B (q4\_K\_M / q8\_0) |

我们还用 **SGLang 测试了投机解码（EAGLE3）**，覆盖上述部分模型。超出目标机器可用内存（RAM）或显存（VRAM）容量的模型已被排除。

### 结果

> 完整的基准测试结果可<a href="https://docs.google.com/spreadsheets/d/1SF1u0J2vJ-ou-R_Ry1JZQ0iscOZL8UKHpdVFr85tNLU/edit?usp=sharing" target="_blank">点此查看</a>。

#### 总体性能

尽管 DGX Spark 在其尺寸与功耗约束下展现了令人印象深刻的工程设计，但其原始性能与全尺寸独立 GPU 系统相比自然有所不及。

例如，在 **Ollama** 中运行 **GPT-OSS 20B (MXFP4)** 时，Spark 达到了 **2,053 tps 预填充 / 49.7 tps 解码**，而 **RTX Pro 6000 Blackwell** 达到了 **10,108 tps / 215 tps**，大约快 **4 倍**。就连 **GeForce RTX 5090** 也有 **8,519 tps / 205 tps** 的表现，印证了 Spark 的 LPDDR5x 统一内存带宽是主要的限制因素。

不过，对于较小的模型，尤其是 **Llama 3.1 8B**，DGX Spark 毫不逊色。在 **SGLang** 批大小为 1 时，它达到了 **7,991 tps 预填充 / 20.5 tps 解码**，并随批大小线性扩展到批 32 时的 **7,949 tps / 368 tps**，展现了出色的批处理效率和跨次运行的强吞吐一致性。

#### 紧凑统一内存负载的优势

DGX Spark 的标志性优势之一在于其 **128 GB 一致性统一内存**，CPU 和 GPU 可以访问同一地址空间。

这使得 **Llama 3.1 70B**、**Gemma 3 27B** 甚至 **GPT-OSS 120B** 这样的大模型能够**直接加载进内存**，省去了传统的系统内存到显存的传输开销。尽管外形紧凑，Spark 成功以 **803 tps 预填充 / 2.7 tps 解码**运行了 **Llama 3.1 70B (FP8)**——对于一台安静摆在桌面上的工作站来说，这个成绩相当了不起。

这种统一内存设计让 DGX Spark 在**原型验证**、**模型实验**和**边缘 AI 研究**中尤其有价值——在这些场景下，无缝的内存访问往往比原始 TFLOPS 更有用。

#### 投机解码加速

为了进一步挖掘 DGX Spark 上的性能优化空间，我们在 **SGLang** 中启用了基于 **EAGLE 3** 的**投机解码**。该技术让一个较小的"草稿模型"提前提出多个 token，再由较大的目标模型并行验证。

在多个模型（如 **Llama 3.1 8B**）上，启用投机解码后，我们观察到端到端推理吞吐量相比标准解码最高提升 **2 倍**。

这一改进有效缓解了统一内存带宽限制的一部分影响，也表明**投机解码这类软件层面的创新**能够在 DGX Spark 这样紧凑、带宽受限的系统上切实提升推理性能。

#### 能效与散热设计

DGX Spark 在高强度测试中保持了持续的吞吐量，没有出现热节流。即使满载运行（例如 **SGLang DeepSeek-R1 14B (FP8)** 批大小 8 达到 **2,074 tps / 83.5 tps**），风扇噪音和温度依然保持稳定，凸显了 NVIDIA 出色的**金属泡沫散热设计**和优化良好的**供电系统**。

其 **USB-C 供电输入**（最高 240 W）与外置电源为机身内部留出了更大的散热余量。与 Mac Mini 或 Mac Studio 这类在类似测试中出现散热降频的紧凑消费级系统相比，这是一个明显的优势。

#### 小结

简而言之，DGX Spark **并非为了与全尺寸 Blackwell 或 Ada-Lovelace GPU 正面竞争**而设计，而是要把 DGX 体验带进紧凑、对开发者友好的外形之中。  
它是以下场景的理想平台：

* **模型原型验证与实验**  
* **轻量级端侧推理**  
* **内存一致性 GPU 架构研究**

它是一台**精美、做工考究的迷你超算**，以原始算力换取易用性、能效与优雅——而在这些方面，它确实闪闪发光。

![](/images/blog/nvidia_dgx_spark/product_4.jpg)

## 使用场景

### SGLang 模型服务

DGX Spark 预装了 Docker，只需一条命令即可通过 SGLang 服务开放权重模型：

```bash
docker run --gpus all \
    --shm-size 32g \
    -p 30000:30000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HF_TOKEN=<secret>" \
    --ipc=host \
    lmsysorg/sglang:spark \
    python3 -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --quantization fp8 --host 0.0.0.0 --port 30000
```

将 `<secret>` 替换为你自己的 Hugging Face 访问令牌。

#### 启用投机解码（EAGLE3）

要启用基于 **EAGLE3** 的**投机解码**，只需运行以下命令：

```bash
docker run --gpus all \
    --shm-size 32g \
    -p 30000:30000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HF_TOKEN=<secret>" \
    --env "SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1" \
    --ipc=host \
    lmsysorg/sglang:spark \
    python3 -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --quantization fp8 --host 0.0.0.0 --port 30000 \
    --speculative-algorithm EAGLE3 \
    --speculative-draft-model-path jamesliu1/sglang-EAGLE3-Llama-3.1-Instruct-8B \
    --speculative-num-steps 5 \
    --speculative-eagle-topk 8 \
    --speculative-num-draft-tokens 32 \
    --mem-fraction 0.6 \
    --cuda-graph-max-bs 2 \
    --dtype float16
```

启用投机解码后，SGLang 可以利用较小的草稿模型提前预测多个 token，与标准解码相比可将推理吞吐量有效**翻倍**。

#### 通过 OpenAI 兼容 API 发送请求

SGLang 成功初始化后，你就可以通过 OpenAI 兼容的 API 端点与模型交互：

```bash
curl http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "How many letters are there in the word SGLang?"
            }
        ]
    }'
```

![](/images/blog/nvidia_dgx_spark/demo_1.jpg)

### 与本地模型聊天

**SGLang** 部署好并开始服务模型后，你可以轻松将其接入 **Open WebUI**，与任意你喜欢的开放权重模型聊天。Open WebUI 提供了一个精致的浏览器界面，完全兼容 OpenAI 风格的 API，因此可以与本地 SGLang 服务器无缝配合。只需简单配置指向 DGX Spark 的端点，你就能在浏览器中直接与 **Llama 3**、**Gemma 3** 或 **DeepSeek-R1** 等模型交互——不依赖云端、没有网络延迟，并且对数据拥有完全的控制权。

![](/images/blog/nvidia_dgx_spark/demo_2.jpg)

### 用本地模型写代码

DGX Spark 最实用的用法之一是充当**本地编程助手**——完全离线且安全。

将现代 AI 集成代码编辑器 **Zed** 与 **Ollama** 结合，你可以在本地运行 **GPT-OSS 20B**，为代码补全、行内聊天和智能重构提供支持，完全无需依赖云端。

#### 第 1 步：安装 Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### 第 2 步：拉取用于编程的 GPT-OSS 20B

```bash
ollama pull gpt-oss:20b
```

#### 第 3 步：将 Zed 接入 Ollama

安装 Zed：

```bash
curl -f https://zed.dev/install.sh | sh
```

Zed 会自动检测 Ollama 提供的本地模型，启动编辑器后即可立即使用内置的聊天助手。

![](/images/blog/nvidia_dgx_spark/demo_3.jpg)

## 结论

**NVIDIA DGX Spark** 让我们得以一窥个人 AI 计算的未来。它把原本专属于数据中心的东西——大容量内存、高带宽以太网互联、Blackwell 级别的性能——浓缩进一个紧凑、工艺精美的桌面外形之中。虽然它在原始吞吐量上无法与全尺寸 DGX 服务器或独立 RTX GPU 抗衡，但在易用性、能效和多功能性上大放异彩。

从运行 **SGLang** 和 **Ollama** 进行本地模型服务，到试用**投机解码（EAGLE3）**，再到通过**双 Spark 集群**探索分布式推理，这个平台证明了自己不只是一款迷你超算，更是面向 AI 下一个时代的开发者沙盒。

NVIDIA DGX Spark 的使命不是取代云级基础设施，而是**把 AI 实验带到你的桌面上**。无论你是在对开放权重 LLM 做基准测试、开发推理框架，还是搭建自己的私人编程助手，Spark 都让你能够全部在本地完成——安静、优雅，并且带着 NVIDIA 独有的工程质感。

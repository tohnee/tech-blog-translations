---
title: "SGLang-Omni 上的 MOSS-TTS Local Transformer v1.5：原生流式 48 kHz 语音推理服务"
title_en: "MOSS-TTS Local Transformer v1.5 on SGLang-Omni: Serving Native-Streaming 48 kHz Speech"
author: "MOSI, OpenMOSS Team & SGLang-Omni Team"
date: "June 17, 2026"
previewImg: "https://raw.githubusercontent.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/main/sglang/sglang-omni/images/moss-local-transformer-arch.svg"
source: https://lmsys.org/blog/2026-06-17-moss-tts-local-v15/
translated: 2026-09-12
---

# SGLang-Omni 上的 MOSS-TTS Local Transformer v1.5：原生流式 48 kHz 语音推理服务

> 原文：[MOSS-TTS Local Transformer v1.5 on SGLang-Omni: Serving Native-Streaming 48 kHz Speech](https://lmsys.org/blog/2026-06-17-moss-tts-local-v15/) · LMSYS Blog · MOSI, OpenMOSS Team & SGLang-Omni Team

今天，我们联合 [MOSI](https://mosi.cn/) 与 [OpenMOSS 团队](https://openmoss.ai/)宣布：[**MOSS-TTS-Local-Transformer-v1.5**](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5) 现已可以在 [**SGLang-Omni**](https://github.com/sgl-project/sglang-omni) 上实现端到端推理服务。

MOSS-TTS-Local-Transformer-v1.5 是一个开源 TTS 模型，支持 48 kHz 立体声语音、零样本声音克隆、长篇合成、多语言生成、时长控制以及原生流式输出。用 demo 脚本调用这个模型并不难，但要把它的推理服务做好就难多了：一个请求会依次穿过参考音频编码、一个 Qwen3-4B 自回归主干、一个帧内局部的 12 codebook 采样循环，以及一个带状态的 codec 解码器。

SGLang-Omni 把 MOSS-TTS-Local-Transformer-v1.5 作为一个三阶段流水线来服务，而不是把它硬塞进单一 LLM 解码循环。本文的工作主要围绕这一映射展开：各阶段位于哪里，哪些部分需要模型专属的钩子，以及模型开始承受负载之后暴露出了哪些瓶颈。

## MOSS-TTS-Local-Transformer-v1.5 模型

MOSS-TTS-Local-Transformer-v1.5 是 MOSS-TTS v1.5 家族中的第二款旗舰模型。它走的是 Audio Tokenizer + LLM 自回归的路线，配备了更重的音频 codec，并采用 Global Transformer + Local Transformer 的生成路径。

它支持直接 TTS、续写（continuation）、零样本声音克隆、时长控制、`[pause 3.2s]` 这类显式停顿标记，以及最长 10 分钟的长篇生成。它覆盖 31 种主要语言，训练数据约为 400 万小时的多语言语音。

![MOSS-TTS Local Transformer v1.5 模型架构](https://raw.githubusercontent.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/main/sglang/sglang-omni/images/moss-local-transformer-arch.svg)

在音频边界上，MOSS 使用 **MOSS-Audio-Tokenizer-v2**——一个神经音频 tokenizer，其编码器与解码器合计约 2B 参数。它以 12.5 Hz 运行，支持 0.125 kbps 到 4 kbps 的可变码率压缩，能够重建 48 kHz 立体声音频，并通过残差向量量化（RVQ）来表示语音。

生成核心采用 **Qwen3-4B 主干**。全局 transformer 逐帧推进序列。对于每一帧，一个单层 local transformer 先给出停止/继续的判定，然后按顺序采样 12 个 RVQ codebook，并在采样下一个之前把已采样到的 code 反馈回去。

从推理服务视角看到的 token 布局是 `[T, 13]`：1 个文本/控制通道加上 12 个音频 codebook 通道。文本位置在通道 0 上携带一个文本 token，其余通道为音频填充；音频位置在通道 0 上携带一个 slot/控制 token，并在每个音频 codebook 上各携带一个 RVQ code。这是 MOSS 第一个不像普通 next-token 模型的地方：每一帧生成出来的都是一个行向量，而不是一个标量 token。

在公开的模型级评测集上：

| 基准测试 | WER（越低越好） | SIM（越高越好） |
|---|---:|---:|
| Seed-TTS-Eval | 5.10% | 69.23% |
| CV3-Eval | 7.48% | 61.59% |
| MiniMax Multilingual | 6.37% | 75.31% |
| X Voice | 20.48% | 63.00% |

这些是离线的模型级指标。后文的服务基准测试使用的是另一套评测流程，应被解读为端到端的系统级测量结果。

MOSS-TTS-Local-Transformer-v1.5 在阿里云 PPU-ZW810 集群上以千卡规模训练而成。本文聚焦于推理服务这一侧。

## 为什么 MOSS 需要多阶段服务运行时

标准 LLM 服务引擎围绕单一且反复执行的模型循环构建，而 MOSS 的一个请求里包含三类不同的工作：

- **预处理与参考编码。** 文本被分词，参考音频被加载，参考波形被编码为 RVQ code。
- **自回归 TTS 引擎。** Qwen3 主干与 local transformer 生成 `[1, 13]` 的帧行。
- **流式 vocoder。** 生成的 RVQ 行由带状态的 MOSS codec 解码器解码为波形块。

每个阶段的瓶颈各不相同。参考编码要运行一个大型神经 codec 编码器；AR 生成把常规的主干解码与一个小而严格串行的局部 codebook 循环混在一起；vocoder 则是一个必须在多个块之间保持流式状态的解码器。系统必须同时管理好这三者，不能让某个阶段的批处理或内存行为损害其他阶段。这正是 [**SGLang-Omni**](https://github.com/sgl-project/sglang-omni) 为之而生的工作负载：一个多阶段生成流水线，其中每个阶段按照自己的计算模式被调度，阶段之间通过低开销通道通信，而 GPU 放置与内存预算由框架统一管理。

## 用 SGLang-Omni 服务 MOSS

详细操作指南见 [SGLang-Omni MOSS-TTS-Local cookbook](https://sgl-project.github.io/sglang-omni/cookbook/moss_tts_local.html)。

### 安装与服务

```bash
docker pull lmsysorg/sglang-omni:dev
docker run -it --gpus all --shm-size 32g --ipc host --network host --privileged \
  lmsysorg/sglang-omni:dev /bin/zsh

git clone git@github.com:sgl-project/sglang-omni.git
cd sglang-omni
uv venv .venv -p 3.12
source .venv/bin/activate
uv pip install -v -e .

hf download OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5

sgl-omni serve \
  --model-path OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5 \
  --port 8000
```

SGLang-Omni 把 MOSS-TTS Local Transformer v1.5 作为一个三阶段流水线来服务：

```text
preprocessing -> tts_engine -> vocoder
```

**preprocessing** 阶段解析 OpenAI 兼容的请求，准备多通道 prompt，并为声音克隆编码参考音频。**tts_engine** 阶段运行在 `OmniScheduler` 上，因此 MOSS 可以复用 SGLang 的请求批处理与 KV 缓存机制，同时承载模型专属的 `[T, 13]` 行。**vocoder** 阶段以流的方式消费生成的行，并从一个持久的 codec 流式会话中返回音频块。

复用的部分是运行时形态：阶段生命周期、调度器接口、阶段间路由、流式输出、进程放置以及阶段级资源核算。MOSS 专属的部分更小也更明确：如何构建多通道 prompt、如何运行帧内局部的 codebook 循环，以及如何把 MOSS codec 接成流式解码器。下一节只聚焦这些 MOSS 专属的瓶颈与优化。

## 端到端优化 MOSS

在流水线功能完备之后，我们对性能分析显示存在重复计算或启动开销的阶段进行了优化。

| 领域 | 改动 | 主要收益 | 来源 |
|---|---|---|---|
| 模型服务基线 | MOSS Local 模型、流水线与 API 支持 | 建立三阶段服务路径 | [#728](https://github.com/sgl-project/sglang-omni/pull/728) |
| 参考编码 | 批量编码、内容寻址 LRU 缓存与 single-flight 去重 | 避免对复用的说话人重复执行 codec 编码器 | [#748](https://github.com/sgl-project/sglang-omni/pull/748), [#778](https://github.com/sgl-project/sglang-omni/pull/778), [#788](https://github.com/sgl-project/sglang-omni/pull/788) |
| AR 引擎 | 解码状态池、帧级 CUDA Graph 支持与 GPU 原生行哈希 | 让解码状态保持在稳定的 GPU 地址上，并消除每帧的主机端哈希 | [#745](https://github.com/sgl-project/sglang-omni/pull/745) |
| AR 引擎 | 帧启动状态池化与异步解码管道 | 降低启动准备开销，并修复解码步骤归属问题 | [#759](https://github.com/sgl-project/sglang-omni/pull/759), [#758](https://github.com/sgl-project/sglang-omni/pull/758) |
| AR 引擎 | 编译的带种子采样器 | 在保持每请求确定性采样的同时融合热点采样路径 | [#773](https://github.com/sgl-project/sglang-omni/pull/773) |
| Vocoder | 有状态流式会话、流槽位与合并块调度 | 支持帧级音频流式输出并保持请求隔离 | [#753](https://github.com/sgl-project/sglang-omni/pull/753) |
| Vocoder | 有状态 vocoder CUDA Graph | 加速短流式解码步骤 | [#798](https://github.com/sgl-project/sglang-omni/pull/798) |
| 跨阶段 | 显式的共置内存预算 | 防止 codec 与 AR 的内存压力相互干扰 | [#810](https://github.com/sgl-project/sglang-omni/pull/810) |

### 参考音频编码

声音克隆常常在许多 prompt 中复用同一批说话人。在 MOSS 里这一点很关键，因为 AR 生成开始之前，参考编码要先运行一个大型 codec 编码器。

![参考音频缓存：](https://raw.githubusercontent.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/main/sglang/sglang-omni/images/tts-opt-encoder-cache.png)

SGLang-Omni 将批量参考编码与内容寻址的 LRU 缓存相结合。重复的参考以音频内容而非文件路径为键，因此被复制或改名的文件仍能复用同一份编码后的 RVQ 结果。single-flight 路径会把针对同一说话人的并发缓存未命中合并起来，避免冷缓存突发导致重复启动 codec 编码。

在 2x H100、并发 16 的 SeedTTS 英文评测中，把参考缓存容量从 256 项提升到 1024 项后，吞吐量提高了 **32.0%**，平均延迟降低了 **24.3%**。内存代价很小，因为编码后的 code 张量非常紧凑；更大的缓存主要是防止活跃说话人的工作集被逐出。

### AR 引擎

MOSS 的 AR 引擎有两层计算：Qwen3 主干与 local transformer 的帧解码循环。SGLang-Omni 用 CUDA Graph 把两者都捕获下来，但让它们保持分离，因为二者的结构和归属都不同。

![CUDA Graph 执行](https://raw.githubusercontent.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/main/sglang/sglang-omni/images/tts-opt-cuda-graph.svg)

主干图使用 SGLang 标准的因果 LM 解码 CUDA Graph 路径。MOSS 专属的帧图则捕获 local transformer 针对完整一帧的微循环：停止/继续采样、12 个 codebook 的顺序投影、codebook 反馈，以及为下一帧组装反馈嵌入。这就消除了一个小而高度串行的循环的启动开销。

为了让图重放成为可能，MOSS 把每个请求的解码状态保存在一个持久的 GPU 侧池中。反馈嵌入、采样参数、随机种子、计数器和音频历史在帧与帧之间都位于稳定的地址上。SGLang-Omni 还把生成行的基数树哈希搬到了 GPU 上，避免了每帧一次的 CPU 哈希与 D2H 同步。

每帧的 13 个采样操作使用带种子的 GPU 采样器。我们只编译这条采样路径，而不编译主干或 local transformer。这个窄范围的改动在 SeedTTS 英文、并发 16 的设置下把吞吐量提升了 **12.3%**，平均延迟降低了 **11.1%**，平均 RTF 降低了 **10.5%**，且没有改动更大的模型执行路径。

### 流式 Vocoder

vocoder 阶段把生成的 RVQ 帧转换成音频块。由于 MOSS-Audio-Tokenizer-v2 支持有状态的流式解码，SGLang-Omni 在 vocoder 执行器内部维护一个持久的 codec 流式会话。

调度器管理流槽位、一个离线回退槽位、块阈值以及合并解码步骤。首个块可以使用较小的阈值来缩短首包音频的等待时间，后续块则使用更大的窗口来提升吞吐量。当多个请求积累的待处理帧足够多时，调度器会在一次 codec 调用中把它们一起解码。

短的流式块启动开销占比很高，因此 SGLang-Omni 用 CUDA Graph 捕获常见的 vocoder 帧数。该实现让 codec 状态缓冲区保持稳定地址并原地更新，从而支持跨流式步骤的图重放。

对于短流式块，加速效果最明显：

| 每步帧数 | Eager | CUDA Graph | 加速比 |
|---:|---:|---:|---:|
| 4 | 66.3 ms | 30.1 ms | 2.20x |
| 5 | 65.8 ms | 30.7 ms | 2.14x |
| 8 | 65.6 ms | 34.0 ms | 1.93x |
| 13 | 65.4 ms | 40.4 ms | 1.62x |
| 25 | 74.8 ms | 58.3 ms | 1.28x |
| 100 | 222.9 ms | 215.3 ms | 1.04x |

当帧数未被捕获或内存紧张时，图路径会回退到 eager 解码。流式/非流式一致性检查覆盖了这条路径。

### 内存预算

在默认的 MOSS Local 配置中，预处理、AR 生成与 vocoder 执行可以共置在同一块 GPU 上。这种紧凑布局很方便，但 AR 引擎与 codec 运行时的内存分配模式并不相同。因此，SGLang-Omni 为 AR 引擎提供了显式的共置内存契约，并为 codec 运行时分配与流式状态预留了余量。

在单卡共置、并发 8 的配置下，显式的 codec 内存预算把吞吐量提升了 **8.9%**，平均 RTF 降低了 **8.4%**。更重要的是，它让部署在内存压力下的行为变得可预测。

## 性能

我们在包含 1088 条样本的 SeedTTS 英文集上评估优化后的服务路径。以下结果来自启用 vocoder CUDA Graph 之后的完整 CI 评测，使用 2x GPU 和客户端并发 16。ASR 打分使用 Qwen3-ASR-1.7B，说话人相似度使用 WavLM-Large finetune。

| 模式 | 完成 / 失败 | 吞吐量 | 音频吞吐量 | 平均延迟 | 平均 RTF | WER |
|---|---:|---:|---:|---:|---:|---:|
| 非流式 | 1088 / 0 | 5.976 req/s | 26.303 audio s/s | 2.669 s | 0.644 | 1.75% |
| 流式 | 1088 / 0 | 2.909 req/s | 12.804 audio s/s | 5.474 s | 1.322 | 2.14% |

非流式达到 **5.976 req/s**，平均 RTF 为 **0.644**。流式输出增量的音频块；在并发 16 下，块间平均间隔为 **0.109 s**，每个请求平均发出 **8.82** 个块。流式吞吐量较低是符合预期的：vocoder 更频繁地在更小的块上运行，并与 AR 引擎共享 GPU 时间。

两种模式下的质量指标非常接近：同一次 CI 运行中，非流式 WER 为 **1.75%**，流式为 **2.14%**。流式/非流式产物一致性检查也已通过。

各项优化的测量结果不应叠加成一个总数字，因为它们是在不同的硬件与并发设置下采集的。它们更有价值的用途是刻画 MOSS 的时间都花在了哪里：参考缓存消除冗余的编码器工作，帧级 CUDA Graph 消除局部循环的启动开销，采样器编译改善热点采样路径，vocoder CUDA Graph 加速短流式块，而内存预算让共置部署保持稳定。

## 路线图

当前路径已经可以端到端运行，但仍有几处值得改进：

**原生池化的帧 CUDA Graph。** 当前的帧解码图使用了持久状态池，但围绕采样参数与生成行仍有部分中转（staging）。更彻底的池到池图路径可以简化启动/解析边界。

**自适应流式调度。** 流式 TTS 存在真实的延迟-吞吐量权衡。我们正在探索负载感知的块大小、优先级感知的槽位调度以及更好的合并策略，让低负载请求获得更快的首包音频，同时让高负载部署找回更多吞吐量。

**更广的编译覆盖。** codec 编码器与 Qwen3 主干仍有进行针对性编译实验的空间。我们会把编译范围控制在足够窄，以避免冷启动退化和输出变化。

**更广的基准覆盖。** 当前测量聚焦于 CI 中的 SeedTTS 英文。我们计划把覆盖范围扩展到中文、多语言评测、长篇生成、多说话人池、不同参考音频长度，以及类生产的流量混合。

## 加入我们

如果你对 TTS、全模态（omni）模型、流式推理、CUDA Graph、调度、通信、模型接入、基准测试或生产级推理服务感兴趣，欢迎参与贡献和讨论。

## 致谢

**SGLang-Omni** - **Jiaxin Deng**, Haoguang Cai, Shangming Cai, Yuhao Chen, Kangxiang Shao, Hao Jin, Yifei Gao, Jingwen Gu, Zhihao Guo, Chenchen Hong, Xinli Jing, Xiangrui Ke, Estella Liu, Xinyu Lu, Ratish Palanisamy, Mick Qian, Yijiang Tian, Zijie Xia, Xuesong Ye, Yue Yin, Gaokai Zhang, Xiaoyu Zhang, Chenyang Zhao, **Yichi Zhang**.

**MOSS-TTS Local Transformer v1.5** - Yitian Gong, Kuangwei Chen, Zhicheng Zhang, Botian Jiang, Yiyang Zhang, Kang Yu, Yang Gao, Xiaogui Yang, Qinyuan Chen, Zhaoye Fei, Shimin Li, Xipeng Qiu.

## 了解更多

- **模型：**[OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5)
- **服务框架：**[GitHub 上的 SGLang-Omni](https://github.com/sgl-project/sglang-omni)
- **文档：**[SGLang-Omni 文档](https://sgl-project.github.io/sglang-omni/)
- **MOSS-TTS-Local cookbook：**[SGLang-Omni 中的 MOSS-TTS-Local](https://sgl-project.github.io/sglang-omni/cookbook/moss_tts_local.html)
- **MOSS 优化路线图：**[#637](https://github.com/sgl-project/sglang-omni/issues/637)
- **设计背景：**[SGLang-Omni：面向多阶段生成模型重新设计推理框架](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/sglang/sglang-omni/why-sglang-omni-en.md)

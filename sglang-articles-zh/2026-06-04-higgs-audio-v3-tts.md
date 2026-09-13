---
title: "SGLang-Omni 上的 Higgs Audio v3 TTS：为语音智能体提供实时、可控的语音生成"
title_en: "Higgs Audio v3 TTS on SGLang-Omni: Real-Time, Controllable Speech for Voice Agents"
author: "Boson AI & SGLang-Omni Team"
date: "June 4, 2026"
previewImg: "https://sgl-project.github.io/sglang-omni/_images/higgs-architecture.png"
source: https://lmsys.org/blog/2026-06-04-higgs-audio-v3-tts/
translated: 2026-09-12
---

# SGLang-Omni 上的 Higgs Audio v3 TTS：为语音智能体提供实时、可控的语音生成

> 原文：[Higgs Audio v3 TTS on SGLang-Omni: Real-Time, Controllable Speech for Voice Agents](https://lmsys.org/blog/2026-06-04-higgs-audio-v3-tts/) · LMSYS Blog · Boson AI & SGLang-Omni Team

今天我们宣布：[**Higgs Audio v3 TTS**](https://www.boson.ai/blog/higgs-audio-v3-tts) 现已在 [**SGLang-Omni**](https://github.com/sgl-project/sglang-omni) 上实现端到端推理服务。Higgs Audio v3 TTS 是 Boson AI 面向对话式语音智能体的文本转语音（TTS）模型：它能以低延迟生成自然且富有表现力的语音，[在 100 种语言上达到个位数 WER/CER](https://huggingface.co/bosonai/higgs-audio-v3-tts-4b#supported-languages)，并让开发者能够直接通过输入文本流控制情感、风格、韵律和音效。

对我们而言，为 Higgs 提供推理服务并不只是"多支持一个 TTS 模型"。Higgs 代表了一类更广泛的生成负载：端到端路径不再是一条单一的自回归解码循环，而是被拆分为多个阶段，各自具有不同的计算模式、延迟需求和内存行为。SGLang-Omni 正是我们为这一类多阶段模型打造的推理框架。

<iframe
  width="960"
  height="540"
  src="https://www.youtube.com/embed/i2PJeaywDew"
  title="Higgs Audio v3 TTS Demo"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen
></iframe>

注：演示视频来自 [Higgs Audio v3 TTS](https://www.boson.ai/blog/higgs-audio-v3-tts)，其中的合成音频生成由 SGLang-Omni 提供支持。

## 初识 Higgs Audio v3 TTS

### 为真实对话而设计

一个优秀的对话式 TTS 模型不能等到整段文字都打磨好才开工。在真实的语音智能体场景中，模型往往只看到半句话、甚至几个词，就必须开始说话。随着后续文本不断到达，生成的语音仍需在说话人身份、情感和语速上保持连贯。

Higgs Audio v3 TTS 正是为这种流式交互模式而设计的。它可以在完整句子甚至标点尚未到达时就开始合成，并随着文本流的增长继续生成，同时保持稳定的语音表达。

在架构上，Higgs 是一个约 4B 参数的自回归解码器，构建在 Qwen3-4B 骨干之上，输入为交错排列的文本 token 与音频 token。音频由 Higgs Tokenizer 编码为 25 fps 的 8 个离散 codebook，按延迟（delayed）模式交错错位排列，经融合的多 codebook 嵌入映射到骨干网络的隐状态，再通过融合的多 codebook 输出头解码回 24 kHz 波形。生成过程在文本块与音频块之间交替进行，因此每一段新生成的音频都同时以参考音频和已生成的上下文为依据。

### 多语言质量

在 Boson AI 覆盖 111 种语言和方言的内部 **Higgs-Multilingual** 测试套件上，Higgs Audio v3 TTS [**在 100 种语言上达到个位数 WER/CER**](https://www.boson.ai/blog/higgs-audio-v3-tts)。在公开的多语言语音克隆基准上，v3 在 Seed-TTS、CV3 和 MiniMax-Multilingual 上同样取得了宏平均个位数的 WER/CER。零样本语音克隆只需一小段参考音频，且同一段参考可以跨语言复用。

下表为零样本语音克隆的 WER/CER（↓，%）。每个数字都是在相应基准的语言集合上做宏平均得到的，并使用可复现的指标与归一化流程。

| 基准 | 语言数 | WER/CER ↓ |
|---|---:|---:|
| Seed-TTS | 2 | 1.11 |
| CV3 | 9 | 4.41 |
| MiniMax-Multilingual | 23 | 2.74 |
| Higgs-Multilingual | 111 | 3.61 |

按语言拆分的 Seed-TTS 明细与 WavLM 说话人相似度可在 [SGLang Omni Higgs Cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html) 中查看。

### 从文本流控制语音表达

Higgs Audio v3 TTS 还具备可控性。开发者可以直接在输入文本中插入控制标签，在同一段话内改变情感、切换说话风格、调整语速和音高、插入停顿或触发音效：

```text
<|emotion:amusement|><|prosody:expressive_high|>Wait, wait, that was kind of hilarious. <|sfx:laughter|>Hehe, no, seriously, I was not ready for that.
```

这些标签族涵盖 20 多种情感（`<|emotion:elation|>`、`<|emotion:anger|>`、`<|emotion:sadness|>` 等）、多种风格（`<|style:singing|>`、`<|style:whispering|>`、`<|style:shouting|>`）、韵律（`<|prosody:speed_very_slow|>`、`<|prosody:pitch_high|>`、`<|prosody:pause|>`、`<|prosody:long_pause|>`）以及音效（`<|sfx:cough|>`、`<|sfx:laughter|>`、`<|sfx:sigh|>` 等）。不同类别的标签可以组合使用。完整目录见 [SGLang Omni Higgs Cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html#inline-control-tokens)。

## 用 SGLang-Omni 服务 Higgs

Higgs 在 [**SGLang-Omni**](https://github.com/sgl-project/sglang-omni) 上进行服务与优化。与标准 LLM 不同，Higgs 以及许多现代 TTS 或全模态（omni）模型并不能自然地套进一条统一的自回归解码循环。它们的端到端生成路径包含多个阶段：有些看起来像标准的 AR 解码，有些是轻量的函数式计算，还有一些持续消费数据块并将音频流式返回。

SGLang-Omni 的目标是以清晰的运行时结构来服务这类模型：每个阶段按自身的计算模式被调度，阶段之间通过低开销通道通信，而 GPU 放置、进程拓扑和内存预算则由框架统一管理。

### 借助高性能 SGLang 后端实现多阶段解码

单阶段模型已经有成熟的推理服务路径：自回归 LLM 由 SGLang 主线优化，扩散模型由 SGLang-Diffusion 支持。SGLang-Omni 关注的是另一种形态：端到端生成被拆分为多个具有不同计算特性的阶段的模型。Higgs 是其中一例；Qwen3-Omni 的 Thinker → Talker → MTP 流水线、Fish Audio S2-Pro 串行嵌套的 Dual-AR 设计，以及 Ming-Omni、LLaDA2.0-Uni 这类完整的全模态模型，也都属于同一类别。

这正是 SGLang-Omni 运行时围绕"阶段（stage）抽象"构建的原因。模型配置以静态方式声明流水线中的各阶段、它们的 GPU 放置以及进程拓扑；放置与拓扑层负责准备各个 worker；Coordinator 在阶段之间路由请求；每个 Stage 则充当一个 IO 外壳：它从上游阶段接收数据，把工作交给内部的 Scheduler，并将输出流式传递给下游阶段。

不同阶段可以使用不同的调度器。AR 阶段（例如 Qwen3-Omni 的 Thinker）通常使用 `OmniScheduler`，它保留了 SGLang 的连续批处理、prefill/decode 混合调度、KV 缓存管理、树形缓存和 CUDA 图支持，并将这些能力适配到 omni 原生的请求对象和流式输出上。非 AR 阶段（如小型编码器和聚合器）可以使用 `SimpleScheduler`，它本质上是一个清晰的 get → forward → put 循环。流式阶段则使用 `StreamingSimpleScheduler` 来管理 chunk 与 done 的生命周期，例如流式模式下的 Higgs vocoder。

阶段之间的接口是统一的，但每个阶段可以选择与自身计算模式相匹配的执行策略。为了让这套设计实用且高效，我们重点建设了三项基础设施：

- **分层通信。** 提交（submit）、数据就绪（data-ready）、流式（stream）、完成（complete）、关闭（shutdown）、中止（abort）等轻量控制消息走 ZMQ/msgpack 控制面；张量负载则经由 relay 数据面传输，提供 `shm`、`nccl`、`nixl`、`mooncake` 等后端。同进程的边可以使用本地分发，符合条件的同 GPU 流式 chunk 可以使用 CUDA IPC，跨进程的边则保持同样的阶段级契约。
- **进程-GPU-阶段拓扑。** 流水线在配置中声明阶段、路由、流式边、进程组、GPU 放置、张量并行规模以及可选的融合阶段组。非 TP 阶段显式声明所属进程组；TP 阶段则展开为每个 rank 一个进程，由 rank 0 负责对外的阶段 IO。紧凑的共置部署与更大规模的分离/TP 部署，只是同一份拓扑描述的不同实例，而不是彼此独立的服务栈。
- **内存隔离。** 在多阶段运行时中，GPU 显存是阶段级的资源契约，而不是某个全局调度器的单一比例。每个基于 GPU 的阶段都可以声明 `runtime.resources.total_gpu_memory_fraction`；放置校验会在启动前按 GPU 汇总各阶段预算。当多个进程组共享同一张卡时，这些预算必须显式声明，从而保证任何一个阶段都无法悄悄占用为其他阶段预留的显存。

### 复用 omni 专属优化

在接入 Higgs 的过程中，我们也把反复出现的 omni 优化沉淀为可复用的框架模块。相似的计算模式不应该在每个模型里重复实现，性能优化工作也应该沉淀在运行时中，而不是散落在各模型专属的流水线里。

- **对 CUDA 图友好的反馈式 runner。** Higgs 的 `tts_engine` 默认开启 CUDA 图捕获，并使用一个为"AR + 多 codebook 反馈循环"设计的模型 runner。该 runner 负责静态缓冲区分配、延迟捕获，并对 Python 侧的 gather/scatter 做了额外处理。同一套 runner 接口还为 Qwen3-Omni、Fish Audio S2-Pro 及其他 SGLang-Omni 模型提供了单步前瞻（one-step-lookahead）异步解码支持。
- **流式 vocoder 调度器。** Higgs、Qwen3-Omni、Fish Audio S2-Pro 及相关模型都需要一套相似的流式音频生命周期：初始化每请求状态、累积到达的 code chunk、一旦上下文足够就立即输出音频窗口、在 `stream_done` 时冲刷缓冲，并向流式客户端返回一个紧凑的最终载荷。编解码与加窗逻辑仍然是模型专属的，但服务生命周期是共享的。

有了这些抽象，接入一个新的多阶段模型不再需要一条散布着 if-else 分支的定制流水线。开发者只需把模型划分为若干调度段，选好合适的调度器和模型 runner 钩子，声明拓扑与内存契约，剩下的路由、流式传输、数据搬运、进程放置和阶段级资源隔离都交给框架处理。

### 不断壮大的多阶段模型生态

Higgs 现已加入 SGLang-Omni 已支持的 TTS 与 omni 模型行列：

| 模型 | 类型 | 说明 |
|---|---|---|
| [Higgs Audio v3 TTS](https://huggingface.co/bosonai/higgs-audio-v3-tts-4b) | TTS | 语音克隆、流式、100 种语言 |
| [Fish Audio S2-Pro](https://huggingface.co/fishaudio/s2-pro) | TTS | 语音克隆、流式 |
| [Voxtral TTS](https://huggingface.co/mistralai/Voxtral-4B-TTS-2603) | TTS | 指定音色、流式、9 种语言 |
| [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) | TTS | 语音克隆、流式、10 种语言 |
| [MOSS-TTS](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) | TTS | 语音克隆、流式、31 种语言 |
| [Qwen3-Omni](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct) | Omni | 文本/图像/音频/视频 → 文本 + 音频 |
| [Ming-Omni](https://huggingface.co/inclusionAI/Ming-flash-omni-2.0) | Omni | 流式 TTS |
| [LLaDA2.0-Uni](https://huggingface.co/inclusionAI/LLaDA2.0-Uni) | 多模态 | 文本 + 图像的理解与生成 |

这些模型表面上各不相同，但在推理系统层面，它们面对的是同一个底层问题：如何把多个异构阶段组织成一条稳定、高效、可扩展的生成流水线。正因如此，在 SGLang-Omni 上接入 Higgs 的工作主要在于声明它的流水线（`preprocessing → audio_encoder → tts_engine → vocoder`）并添加模型专属钩子，而不是从零搭建一套服务栈。

### 端到端优化 Higgs

除了框架抽象之外，我们还对 Higgs 流水线做了端到端优化。主要内容如下；实现细节与进度跟踪见 [Higgs 优化路线图（#478）](https://github.com/sgl-project/sglang-omni/issues/478)与[仓库](https://github.com/sgl-project/sglang-omni)。

- **AR 骨干**：为解码循环提供 [CUDA 图捕获](https://github.com/sgl-project/sglang-omni/pull/503)，为 omni AR 循环提供[异步单步前瞻解码](https://github.com/sgl-project/sglang-omni/pull/590)，并将[每步的 D2H 同步打包](https://github.com/sgl-project/sglang-omni/pull/572)为单次传输。
- **编码器**：[将预处理融合进编码器阶段](https://github.com/sgl-project/sglang-omni/issues/576)，为[重复使用的参考音频](https://github.com/sgl-project/sglang-omni/pull/605)添加 LRU 缓存，以及[批处理化的音频编码器](https://github.com/sgl-project/sglang-omni/pull/610)。
- **Vocoder**：[批处理化的 vocoder 解码](https://github.com/sgl-project/sglang-omni/pull/574)。
- **缓存**：RadixAttention 缓存按参考音频分区，并通过 `extra_key` 命名空间隔离，使重复的语音克隆参考可以复用前缀缓存。
- **调度与流式**：[弃用定制调度器](https://github.com/sgl-project/sglang-omni/pull/476)，改用共享的 `OmniScheduler`，并加入真正的 SSE [流式调度器](https://github.com/sgl-project/sglang-omni/pull/614)以降低首段音频延迟。

### 性能

我们在完整的 Seed-TTS EN 集合上评估 Higgs（每次运行 **N=1088**）。客户端对一个配置为 `max_running_requests=16`、bf16 并启用 CUDA 图的 Higgs 服务端扫描不同的 `--max-concurrency` 取值。每行数据为 **1× H100** 上 **3 次运行**的均值。

| 并发 | 吞吐量 (req/s) | 平均延迟 | RTF（每请求） | audio_s/s |
|---:|---:|---:|---:|---:|
| 1 | 1.62 | 617 ms | 0.147 | 6.89 |
| 2 | 2.70 | 742 ms | 0.180 | 11.37 |
| 4 | 5.45 | 733 ms | 0.177 | 22.84 |
| 8 | 8.91 | 898 ms | 0.217 | 37.38 |
| 16 | 14.74 | 1079 ms | 0.262 | 61.84 |

- **并发**：客户端同时在途请求的最大数量（`--max-concurrency`）。
- **吞吐量 (req/s)**：完成的请求数除以基准测试总耗时（wall-clock）。
- **平均延迟**：每个请求的平均端到端耗时，从发出请求到接收完整响应。
- **RTF（每请求）**：每个请求的处理时间与生成音频时长之比的平均值。小于 1 表示快于实时。
- **audio_s/s**：生成的音频总秒数除以基准测试总耗时（wall-clock）。

如需复现结果，请参考[基准测试脚本](https://github.com/sgl-project/sglang-omni/blob/main/benchmarks/eval/benchmark_tts_seedtts.py)。

## 动手试试

详细说明见 [SGLang Omni Higgs Cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html)。以下命令展示了搭建可用环境的最短路径。

### 安装与服务

```bash
docker pull lmsysorg/sglang-omni:dev
docker run -it --gpus all --shm-size 32g --ipc host --network host --privileged \
  lmsysorg/sglang-omni:dev /bin/zsh

git clone git@github.com:sgl-project/sglang-omni.git && cd sglang-omni
uv venv .venv -p 3.12 && source .venv/bin/activate
uv pip install -v -e .
```

```bash
hf download bosonai/higgs-audio-v3-tts-4b

sgl-omni serve \
  --model-path bosonai/higgs-audio-v3-tts-4b \
  --port 8000
```

### 零样本合成

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, how are you?"}' \
  --output output.wav
```

参考输出：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/higgs-1.wav" type="audio/wav">
</audio>

### 语音克隆

进行语音克隆时，我们建议同时提供参考音频和参考文本（`text`），这通常能提升克隆质量：

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Have a nice day and enjoy south california sunshine.",
    "references": [{
      "audio_path": "https://sgl-project.github.io/sglang-omni/_static/audio/male-voice.wav",
      "text": "Hey, Adam here. Let'\''s create something that feels real, sounds human, and connects every time."
    }],
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 1024
  }' \
  --output output.wav
```

参考输入：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/male-voice.wav" type="audio/wav">
</audio>

参考输出：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/higgs-2.wav" type="audio/wav">
</audio>

### 流式

设置 `"stream": true` 即可通过 [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)（SSE）接收音频。由于 vocoder 会以增量方式输出 WAV 数据块，客户端可以在完整生成结束之前就开始播放。`-N` 标志会关闭 curl 的输出缓冲，让 SSE 事件随到达随打印：

```bash
curl -N -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Get the trust fund to the bank early.",
    "references": [{
      "audio_path": "https://sgl-project.github.io/sglang-omni/_static/audio/male-voice.wav",
      "text": "Hey, Adam here. Let'\''s create something that feels real, sounds human, and connects every time."
    }],
    "stream": true
  }'
```

如需原始 PCM 流式（非 SSE JSON），请参阅 [Higgs TTS cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html#streaming)。

参考输出：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/higgs-4.wav" type="audio/wav">
</audio>

### 内联控制 token

控制 token 可以直接嵌入 `input` 字段，不同类别的 token 可以组合使用。一般而言，把情感、风格、语速、音高或表现性韵律等表达类 token 放在每轮的开头；把 `<|prosody:pause|>` / `<|prosody:long_pause|>` 放在希望停顿的位置；每个 `<|sfx:…|>` 后面紧跟与之匹配的拟声词。完整目录见 [cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html#inline-control-tokens)。

**情感：愉悦（amusement）+ 笑声**

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "<|emotion:amusement|><|prosody:expressive_high|>Wait, wait, that was kind of hilarious. <|sfx:laughter|>Hehe, no, seriously, I was not ready for that.",
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 1024
  }' \
  --output output.wav
```

参考输出：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/control-tokens-test1.wav" type="audio/wav">
</audio>

**情感：愤怒（anger）+ 呐喊（shouting）**

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "<|emotion:anger|><|style:shouting|>No, that is not okay! We cannot ship something that sounds broken, delayed, and unnatural.",
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 1024
  }' \
  --output output.wav
```

参考输出：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/control-tokens-test2.wav" type="audio/wav">
</audio>

**情感：惊讶（surprise）+ 尖叫（screaming）**

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "<|emotion:surprise|><|prosody:pitch_high|><|sfx:screaming|>Ah! Wait, I almost forgot! Higgs Audio v3 also supports over one hundred languages.",
    "references": [{
      "audio_path": "https://sgl-project.github.io/sglang-omni/_static/audio/ref_voice.wav",
      "text": "It was the night before my birthday. Hooray! It’s almost here! It may not be a holiday, but it’s the best day of the year."
    }],
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 1024
  }' \
  --output output.wav
```
参考输出：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/control-tokens-test5.wav" type="audio/wav">
</audio>

**组合示例：**

下面的示例在一小段高考风格的英语听力双人对话中，组合使用了情感、音效和韵律 token：

<details>
<summary>命令</summary>

第 1 部分——她询问落下的课：

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "<|emotion:contemplation|>Hi David, I missed the biology class today because I caught a cold. <|sfx:cough|>Ahem! Sorry, Could you tell me what the teacher covered?",
    "references": [{
      "audio_path": "https://sgl-project.github.io/sglang-omni/_static/audio/female-voice.wav",
      "text": "By repeating what students say, teachers can demonstrate that they are listening. By extending what students say."
    }],
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 1024
  }' \
  --output part1.wav
```

第 2 部分——他讲解课上内容：

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "<|emotion:enthusiasm|>Sure, no problem! We learned how plants make food through photosynthesis, and <|prosody:long_pause|> there will be a quiz this Friday.",
    "references": [{
      "audio_path": "https://sgl-project.github.io/sglang-omni/_static/audio/male-voice.wav",
      "text": "Hey, Adam here. Let'\''s create something that feels real, sounds human, and connects every time."
    }],
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 1024
  }' \
  --output part2.wav
```

第 3 部分——她向他道谢：

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "<|emotion:relief|>Oh, that is really helpful. Thank you!",
    "references": [{
      "audio_path": "https://sgl-project.github.io/sglang-omni/_static/audio/female-voice.wav",
      "text": "By repeating what students say, teachers can demonstrate that they are listening. By extending what students say."
    }],
    "temperature": 0.8,
    "top_k": 50,
    "max_new_tokens": 1024
  }' \
  --output part3.wav
```

拼接音频（每句之间约 0.6 秒间隔）：

```bash
ffmpeg -y \
  -i part1.wav -f lavfi -t 0.6 -i anullsrc=r=24000:cl=mono \
  -i part2.wav -f lavfi -t 0.6 -i anullsrc=r=24000:cl=mono \
  -i part3.wav \
  -filter_complex "[0:a][1:a][2:a][3:a][4:a]concat=n=5:v=0:a=1" \
  gaokao_listening.wav
```

</details>

参考输出：

<audio controls>
  <source src="https://sgl-project.github.io/sglang-omni/_static/audio/gaokao-listening.wav" type="audio/wav">
</audio>

### 演示

你也可以用一条命令同时启动后端和浏览器 UI：

```bash
CUDA_VISIBLE_DEVICES=0 ./playground/higgs/start.sh
```

<iframe
  width="960"
  height="540"
  src="https://drive.google.com/file/d/1QBxraffYEm68LBKy16Q-M_Gfbb0ek3cl/preview"
  title="SGLang-Omni Higgs playground demo"
  allow="autoplay"
  allowfullscreen
></iframe>

## 路线图

对 SGLang-Omni 而言，端到端服务 Higgs 是一个重要的里程碑，但不是终点。我们正在以下几条方向上继续推进：

- **跟进上游 SGLang**（[#658](https://github.com/sgl-project/sglang-omni/issues/658)）：迁移到最新的 SGLang，让 AR 骨干持续继承主线 SGLang 的改进，包括 CUDA/PyTorch 构建更新、算子改进、调度和投机解码。
- **按模型重构**（[#661](https://github.com/sgl-project/sglang-omni/issues/661)）：延续 [RFC #188](https://github.com/sgl-project/sglang-omni/issues/188) 的方向，构建更清晰的按模型抽象。我们希望新模型的接入更像"声明拓扑、插入钩子"，而不是在框架各处添加特殊分支。
- **端到端强化学习（RL）**（[#663](https://github.com/sgl-project/sglang-omni/issues/663)）：把 SGLang-Omni 用作 omni 和 TTS 模型的高吞吐 rollout 后端，配合显式的奖励目标，进一步打通推理服务与后训练。

跨节点的多阶段流水线以及更完整的扩散阶段支持也在推进中。有了阶段抽象、统一的调度器接口、分层通信和跨阶段显存预算机制，这些能力可以在同一个框架内持续生长，而不需要另起一套服务栈。

## 加入我们

SGLang-Omni 仍在快速演进。我们希望它成为多阶段生成模型的通用推理基座：新模型不应该需要从零搭建服务栈，也不应该在十几个文件里散布特判逻辑，而应当可以表达为清晰的阶段、拓扑声明和模型专属钩子，由框架统一处理调度、通信、内存管理和流式传输。

如果你对多阶段推理、TTS、omni 模型、多模态生成、推理系统或 RL rollout 后端感兴趣，我们非常期待与你合作。无论你擅长的是算子、调度、通信、模型接入还是基准测试，都欢迎贡献代码和参与讨论。

## 致谢

**SGLang-Omni** — Haoguang Cai, Shangming Cai, Qiujiang Chen, Jiaxin Deng, Wenyao Gao, Yifei Gao, Jingwen Gu, Yitong Guan, Chenchen Hong, Hao Jin, Xinli Jing, Shenggui Li, Junrong Lin, Xinyu Lu, Yuan Luo, Ratish Palanisamy, Mick Qian, JinTao Qu, Shuai Shi, Chao Wang, Richard Wang, Shuwen Wang, Zijie Xia, Yuhao Yang, Xuesong Ye, Yue Yin, Fan Yin, Gaokai Zhang, Xiaoyu Zhang, Yichi Zhang, Chenyang Zhao.

**Higgs Audio v3 TTS (Boson AI)** — Mu Li, Alex Smola, Lindsey Allen. Silin Meng, Ke Bai. Ruskin Raj Manku, Huapeng Zhou, Dongming Shen, Jonah Mackey, Erik Li, Weisu Yin, Yizhi Liu, Xinyu Wang, Hao Yu.

## 延伸阅读

- **模型：** [`bosonai/higgs-audio-v3-tts-4b`](https://huggingface.co/bosonai/higgs-audio-v3-tts-4b)
- **博客：** [Higgs Audio v3 TTS](https://www.boson.ai/blog/higgs-audio-v3-tts)
- **推理服务框架：** [GitHub 上的 SGLang-Omni](https://github.com/sgl-project/sglang-omni)
- **文档：** [SGLang-Omni 文档](https://sgl-project.github.io/sglang-omni/) · [Higgs TTS cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html)
- **Higgs 优化路线图：** [#478](https://github.com/sgl-project/sglang-omni/issues/478)
- **设计背景：** [SGLang-Omni：为多阶段生成模型重新设计推理框架](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/sglang/sglang-omni/why-sglang-omni-en.md)

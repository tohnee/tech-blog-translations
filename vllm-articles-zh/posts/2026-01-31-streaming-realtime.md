---
title: "vLLM 中的流式请求与 Realtime API"
title_en: "Streaming Requests & Realtime API in vLLM"
source: https://vllm.ai/blog/2026-01-31-streaming-realtime
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中的流式请求与 Realtime API

> 原文：[Streaming Requests & Realtime API in vLLM](https://vllm.ai/blog/2026-01-31-streaming-realtime) · vLLM 博客

作者：Meta、Mistral AI 与 vLLM 团队

[#多模态](https://vllm.ai/blog/tags/multimodal)

大语言模型推理历来基于一个简单的前提：用户提交完整的提示（请求），模型对其进行处理，然后返回响应（流式或一次性返回）。这一范式对基于文本的聊天机器人和批处理工作负载行之有效，但在面对流式音频或视频等实时应用时就显得不足。

vLLM 最近为其引擎增加了对**可流式输入**的支持，并在此基础上构建了 **Realtime WebSocket API**，在服务器中暴露了新的 `/v1/realtime` 端点。

在本文中，我们将阐述实时推理的必要性，并介绍 vLLM 中解锁这些能力的两项新特性：**流式输入支持**与 **Realtime WebSocket API**。

*注*：如果你想了解如何在 vLLM 中使用新的流式输入或 Realtime API，请参阅以下资料：

- [流式输入](https://github.com/vllm-project/vllm/tree/main/tests/v1/streaming_input)
- [Realtime WebSocket API](https://docs.vllm.ai/en/latest/serving/openai_compatible_server/?h=realtime+api#realtime-api)

# 为什么需要实时

## vLLM 中的传统批处理范式

传统的 LLM 推理假设完整提示在开始时即可获得。用户通过例如 [`ChatCompletionRequest`](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) 提交完整请求，等待模型将其全部处理完毕，然后接收完整响应。虽然 vLLM 很早就支持*输出*流式传输——在 token 生成的同时将其发出——但*输入*端始终是固定的：你必须先提供完整请求，推理才能开始。

这种方式对大多数应用已经足够。基于文本的聊天机器人、文档摘要和代码生成都天然契合这一模式。但有一类不断增长的应用无法等到输入完整后才开始处理。

## 流式的重要性

设想一个用语音控制电脑或手机的语音助手。所有操作都不再使用键盘、鼠标或触控板，而是完全由语音控制。语音由麦克风录制，以音频流的形式发送给充当语音助手模型的 LLM。
LLM 需要持续处理音频流并实时生成动作。
对这类应用而言，延迟——更准确地说，[首 token 延迟（TTFT）](https://www.emergentmind.com/topics/time-to-first-token-ttft)——至关重要：用户不希望打开应用、在搜索栏输入文字等操作要等待一秒以上。要实现最自然、最接近真人的语音助手，它需要能够同时聆听与说话，即 LLM 需要能够同时处理音频流并生成动作。

一个自然的问题是：能否用非流式 LLM 通过分块处理输入来近似实现流式行为？原则上，音频可以被缓冲成多个片段，每个片段独立处理，再把输出拼接起来。但在实践中，这种方法带来若干局限。要实现亚秒级 TTFT，需要高性能的分块检测，即准确判断何时切分音频流才不会丢失相关信息。糟糕的切分会导致 TTFT 增加，或因打碎有意义的时序上下文而降低模型性能。基于分块的处理还排除了真正的双向交互：每个块必须被完整处理后才能生成响应，无法同时聆听与说话。这导致一种轮流对话式的交互模型，而不是人类对话所特有的连续、重叠式交流。

这个问题出现在许多领域：

- **语音助手**：如上所述，需要亚秒级响应时间才能显得自然
- **实时转写服务**：需要在识别语音的同时显示文字
- **机器人与具身智能**：需要处理连续的传感器流（摄像头、麦克风、激光雷达），并以最小延迟生成控制动作，以便安全地与物理世界交互

对这些应用来说，传统批处理范式会带来不可接受的延迟。我们需要能够增量处理输入、并在输入全部到达之前就开始生成输出的基础设施。

*注*：即使是传统应用——即需要读取完整输入才能生成第一个输出 token 的场景——随着输入逐步就绪而流式发送输入的能力也依然有益。
默认情况下，vLLM 使用[分块预填充（chunked prefill）](https://docs.vllm.ai/en/stable/cli/serve/?h=max+num+b#-enable-chunked-prefill-no-enable-chunked-prefill)，因此处理 $N$ 个 token 的输入需要 $N\div M$ 次前向传播，其中 $M$ 为 [`max_num_batched_tokens`](https://docs.vllm.ai/en/stable/cli/serve/?h=max+num+b#-max-num-batched-tokens)。当 $N\div M>1$ 时，随着输入可用而流式发送输入可以降低整体 TTFT，因为第一次预填充前向传播可以被更早调度。

## 流式的前提条件

并非所有模型都能支持真正的流式推理。必须满足两个关键条件：合适的注意力模式，以及为增量处理而做的训练。

### 注意力模式

注意力机制决定了模型能否增量处理输入，还是必须等待完整序列。

- 因果注意力（单向掩码）将每个位置 $t$ 限制为只能关注位置 $j$ 满足 $j\le t$ 的 token。由于未来 token 被排除在外，模型在时刻 $t$ 的输出 token 一旦 token $t$ 到达即为最终结果。这使得真正的流式处理成为可能：每个新 token 都可以立即处理，先前的输出也无需修改。
- 双向注意力（全掩码）允许每个位置同时关注过去与未来的 token。因此，模型在位置 $t$ 的输出 token 依赖于可能尚未到达的 token。在完整输入序列已知之前，模型无法为任何位置计算出稳定的输出，因为未来的 token 可能改变先前 token 的解读方式。

因此，双向注意力天然要求在产生输出之前获得完整输入序列，这与流式或在线处理不兼容。

对于长时间运行或无限的流式输入，标准因果注意力并不足够。如果每个 token 都关注全部过去内容，计算与内存将无限增长，这是不现实的。实践中必须截断过去的上下文。
一种常见的架构方案是滑动窗口注意力：每个 token 只关注最近固定大小窗口内的 token，在支持流式的同时保持计算与内存有界。因此，带滑动窗口的因果注意力往往是现代流式模型的首选架构。

### 针对流式输入的训练

然而，仅有完全可流式的架构还不够：模型还必须经过训练以支持**真正的流式输入**。

设 $X=(x_{0},x_{1},...,x_{T})$ 表示输入序列，$Y=(y_{0},y_{1},...,y_{T′})$ 表示输出序列。在流式应用中，模型应在时间步 $t$ 以尽可能小的延迟生成与输入 $x_{t}$ 对应的输出 $y_{t}$。具体而言，可以把 $y_{t}$ 理解为在时刻 $t$ 流入模型的音频帧 $x_{t}$ 的转写文本。

标准的下一 token 训练目标通常将下一个 token 的分布条件于*整个*输入序列：

$P(y_{i}∣y_{i-1},...,y_{0},x_{T},x_{T-1},...,x_{0}).$

这一形式不适合流式场景，因为生成 $y_{i}$ 需要处理完整输入序列 $X$，而它在实时场景中并不可得。

相反，流式模型必须能够仅使用过去的输入、以及可选的少量未来上下文来预测 $y_{i}$：

$P(y_{i}∣y_{i-1},...,y_{0},x_{i+δ},...,x_{i},...,x_{0}),$

其中 $δ$ 是一个前瞻（lookahead）参数，应尽可能小。理论上 $δ$ 可以为零；但实践中，为了获得合理的性能，通常需要少量延迟。

因此，训练一个流式模型需要：

- **i)** 对齐输入与输出序列，使得 $T^{′}=T$，且每个 $y_{i}$ 是与 $x_{i}$ 对应的正确输出；
- **ii)** 使用一种能够在先前输入 $x_{i},...,x_{0}$ 已被处理的同时继续处理新输入 $x_{i+1}$ 的架构。

一种直观的架构，由 [Delayed Streams Modeling](https://arxiv.org/pdf/2509.08753) 开创并被 [Voxtral-Realtime](https://vllm.ai/blog/TODO) 采用，它把输入嵌入（如语音嵌入）与输出嵌入（如文本嵌入）求和池化为单一嵌入序列。模型随后预测

$P(y_{i}∣y_{′}^{i-1},...,y_{′}^{0}),$

其中

$y_{′}^{k}=y_{k}+x_{k+δ}.$

这一区别对部署非常重要：不能随便拿一个因果模型就指望它在流式场景下表现良好。要做到完全可流式，模型必须显式地按照上述对齐与架构约束进行训练，确保条件 **i)** 与 **ii)** 都得到满足。

## 为什么模型架构对服务至关重要

vLLM 可以服务任何模型，但真正的流式需要架构上因果的模型。像 [Voxtral](https://mistral.ai/news/voxtral) 这样的模型从设计之初就面向流式，使用支持增量处理的因果注意力机制。

同样重要的是，服务基础设施必须支持增量输入。即使模型具备流式能力，如果服务器在开始推理前要求完整提示，延迟优势也会丧失。
这正是 vLLM 现在在既有输出流式能力之外又支持流式输入的原因。

### 关于流式架构的延伸阅读

- [Transformer Transducer](https://arxiv.org/abs/2002.02562) 是训练可流式语音识别系统最知名、也最成功的建模方法之一。
- Kyutai 团队的 [Streaming Sequence-to-Sequence Learning with Delayed Streams Modeling](https://arxiv.org/abs/2509.08753) 是进一步深入了解上文所述流式架构的绝佳读物。
- [Streaming Simultaneous Speech Translation with Augmented Memory Transformer](https://arxiv.org/abs/2011.00033) 讨论流式语音翻译。翻译不像语音那样“单调”，这使得高性能流式问题更加困难。
- [Voxtral-Realtime](https://mistral.ai/news/voxtral) 是一个大规模预训练并开源的流式模型，可与大多数离线语音识别模型竞争。

# vLLM 中的流式输入支持

通过 [PR #28973](https://github.com/vllm-project/vllm/pull/28973)，vLLM 现已支持用于推理的流式输入。这使得上文描述的增量处理成为可能：输入随时间到达，输出持续生成。

## StreamingInput 接口

核心抽象是 `StreamingInput` dataclass：

```
from dataclasses import dataclass
from vllm.inputs import PromptType
from vllm.sampling_params import SamplingParams

@dataclass
class StreamingInput:
    prompt: PromptType
    sampling_params: SamplingParams | None = None
```

你现在可以向 `AsyncLLM.generate()` 传入一个随时间产出 `StreamingInput` 对象的 `AsyncGenerator`，而不是传入固定的提示。每个 `StreamingInput` 包含要追加到累积提示中的下一个输入块。下面是一个使用示例：

```
import asyncio
from vllm.inputs.data import StreamingInput
from vllm.v1.engine.async_llm import AsyncLLM
from vllm.sampling_params import SamplingParams

async def streaming_input_example():
    async_llm = AsyncLLM.from_engine_args(...)

    # Input queue can consume inputs in separate async task
    input_queue = asyncio.Queue[list[int]]()

    async def input_generator():
        # Loop until empty list encountered => input finished
        while new_tokens := input_queue.get():
            yield StreamingInput(prompt=new_tokens)

    output_generator = async_llm.generate(
        prompt=input_generator(),
        sampling_params=SamplingParams(temperature=0.0, max_tokens=1),
    )

    # Consume outputs
    async for output in output_generator:
        # ...

asyncio.run(streaming_input_example())
```

你可以等到上一个输入对应的输出完成后再发送下一个输入，但这并非必需（输入块会在内部排队）。输入流的终止通过从异步输入生成器中退出，或使用 `aclose` 函数将其关闭来指示。只有当所有已接收输入都被处理完毕*且*输入生成器结束后，返回的输出生成器才会结束。

## 工作原理

在内部，vLLM 通过把每个块视为一个带有累积提示的独立请求来处理流式输入。当新块到达时，引擎：

1. 用 `max_tokens - 1` 个已生成的 `output_tokens` 以及新到来的 `prompt_token_ids` 扩展 `prompt_token_ids`。
2. 复用所有已缓存的 KV 值
3. 基于当前累积提示与指定的 `max_tokens` 生成输出 token
4. 在新输入到达时可选地丢弃输出

这一设计意味着，在输入块之间生成的输出 token 可能会随着更多上下文可用而被修订。最终输出反映的是完整输入。

在内部，vLLM 通过*粘性会话（sticky session）*机制实现流式输入。第一个输入块会创建一个贯穿整个会话的**锚定请求（anchor request）**。具有相同内部请求 ID 的后续块会被排队并按序处理。

### 锚定请求模式

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STREAMING SESSION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   User's AsyncGenerator              Scheduler                              │
│   ═══════════════════               ═════════                               │
│                                                                             │
│   ┌──────────────┐                                                          │
│   │   Chunk 1    │ ──────────────►  Add ANCHOR REQUEST                      │
│   │   [A, B, C]  │                  ┌────────────────────────────────┐      │
│   └──────────────┘                  │  Request (id="session_1")      │      │
│                                     │  ├── resumable: true           │      │
│                                     │  ├── max_tokens: 2             │      │
│                                     │  ├── streaming_queue: deque()  │      │
│                                     │  ├── status: RUNNING           │      │
│                                     │  └── prompt_token_ids: [A,B,C] │      │
│                                     └────────────────────────────────┘      │
│                                              │                              │
│                                              ▼                              │
│   ┌──────────────┐                  ┌────────────────┐                      │
│   │   Chunk 2    │                  │    ENGINE      │  Generating...       │
│   │   [D, E]     │ ─────┐           │  Processing    │  ──► Output: [X, Y]  │
│   └──────────────┘      │           └────────────────┘                      │
│                         │                                                   │
│                         ▼           Anchor busy? Queue it!                  │
│   ┌──────────────┐      │           ┌────────────────────────────────┐      │
│   │   Chunk 3    │      └────────►  │  streaming_queue:              │      │
│   │   [F, G]     │ ─────────────►   │  ┌───────┐ ┌───────┐           │      │
│   └──────────────┘                  │  │[D, E] │→│[F, G] │→ ...      │      │
│                                     │  └───────┘ └───────┘           │      │
│                                     └────────────────────────────────┘      │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                     WHEN ANCHOR FINISHES CURRENT CHUNK                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Engine signals: chunk complete (stopped = True)                           │
│          │                                                                  │
│          ▼                                                                  │
│   ┌────────────────────────────────────────────────────────────────┐        │
│   │  _handle_stopped_request() pops first item from queue          │        │
│   │                                                                │        │
│   │  streaming_queue: [[D,E], [F,G]]  ──►  [[F,G]]                 │        │
│   │                      ▲                                         │        │
│   │                      │                                         │        │
│   │                    pop!                                        │        │
│   └──────────────────────┬─────────────────────────────────────────┘        │
│                          │                                                  │
│                          ▼                                                  │
│   ┌────────────────────────────────────────────────────────────────┐        │
│   │  _update_request_as_session(anchor, update=[D, E])             │        │
│   │                                                                │        │
│   │  BEFORE:                       AFTER:                          │        │
│   │  ┌───────────────────────┐     ┌───────────────────────────┐   │        │
│   │  │ prompt_token_ids:     │     │ prompt_token_ids:         │   │        │
│   │  │   [A, B, C]           │     │   [A, B, C, X, D, E]      │   │        │
│   │  │ _output_token_ids:    │ ──► │ _output_token_ids:        │   │        │
│   │  │   [X, Y]              │     │   []                      │   │        │
│   │  │ _all_token_ids:       │     │ _all_token_ids:           │   │        │
│   │  │   [A, B, C, X, Y]     │     │   [A, B, C, X, D, E]      │   │        │
│   │  │ num_computed_tokens: 4│     │ num_computed_tokens: 4    │   │        │
│   │  │ status: RUNNING       │     │ status: WAITING           │   │        │
│   │  └───────────────────────┘     └───────────────────────────┘   │        │
│   │                                                                │        │
│   │  Note: Y is DISCARDED (last sampled token, not yet computed)   │        │
│   │        Only X is kept (num_computed_tokens = 4, so [A,B,C,X])  │        │
│   └────────────────────────────────────────────────────────────────┘        │
│                          │                                                  │
│                          ▼                                                  │
│   ┌────────────────────────────────────────────────────────────────┐        │
│   │  Anchor returns to waiting queue → scheduled again → ENGINE    │        │
│   └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

```

**为什么最后一个 token（Y）会在下一个 `prompt_token_ids` 中被丢弃？**

在接收可恢复请求时，我们真正关心的是为所有 `prompt_token_ids` 以及 `max_tokens - 1` 个已生成 token 计算 KV 缓存。注意，用户用 `max_tokens` 表示第一个请求的 `max_tokens - 1` 个已生成 token 是最终的、应当被复用。`output_token_ids` 张量的最后一个 token 只是最近一次前向传播的结果，尚无对应的 KV 缓存状态。由用户决定如何处理它，但由于它没有任何对应的 KV 缓存状态，它在更新后的锚定请求的 `prompt_token_ids` 中会被丢弃。
丢弃它基本上是“免费”的：我们不会使任何缓存状态失效，而且即使保留它，之后无论如何也需要重新计算。

正如 [Realtime API](https://github.com/vllm-project/vllm/blob/a2443de5fa4a0605607f6c3d9219022c7f6ac480/vllm/entrypoints/openai/realtime/connection.py#L209) 中所做的那样，在大多数应用中，`max_tokens` 应设为 `1`，这样每个可恢复请求只为 `prompt_token_ids` 计算 KV 缓存状态，而如何使用 `output_token_ids` 中生成的单个 token 则由用户决定。例如，对于 [Voxtral Realtime](https://mistral.ai/news/voxtral)，`output_token_ids` 中生成的单个 token 会与到来的新音频块结合，构成下一个可恢复请求。

*注意*：某些模型会发出特殊的停止 token，模型需要它才能正确地继续生成。在这种情况下，调度逻辑需要额外容纳 +1 个 token，以便在处理新输入块之前重新计算停止 token。

## 示例流程

为便于说明，可以将多个具有不同 `max_tokens` 的可恢复请求作为输入流式发送。
在这种情况下，生成逻辑将如下运作：

```
Input chunks: ([A1, B1, C1], max_tokens=1), ([A2, B2], max_tokens=2), ([A3], max_tokens=2)

1. First chunk [A1, B1, C1] arrives
   -> Model generates [D1]

2. Second chunk [A2, B2] arrives
   -> Cumulative prompt: [A1, B1, C1, A2, B2] (D1 discarded)
   -> Model generates [C2, D2, E2]

3. Third chunk [A3] arrives
   -> Cumulative prompt: [A1, B1, C1, A2, B2, C2, D2, A3] (E2 discarded)
   -> Model generates [C3, D3]

Output stream: D1, C2, D2, E2, C3, D3

```

# 基于 WebSocket 的 Realtime API

流式输入支持提供了核心能力，而生产应用还需要一个便捷的实时通信 API。[PR #33187](https://github.com/vllm-project/vllm/pull/33187) 引入了受 [OpenAI 的 Realtime API](https://platform.openai.com/docs/guides/realtime) 启发的基于 WebSocket 的 Realtime API。

## 架构

Realtime API 提供一个 WebSocket 端点，支持客户端与 vLLM 服务器之间的双向流式传输。客户端发送音频数据，服务器返回转写文本和模型输出。

架构由以下部分组成：

1. **WebSocket 客户端**：从麦克风采集音频，将音频块发送到服务器
2. **Realtime 处理器**：接收 WebSocket 消息，转换为 StreamingInput
3. **AsyncLLM**：处理流式输入，生成输出
4. **响应流**：通过 WebSocket 将生成的 token 发送回去

## 服务器搭建

启动带 Realtime API 支持的 vLLM 服务器：

```
vllm serve mistralai/Voxtral-Mini-4B-Realtime-2602 --enforce-eager
```

服务器在 `ws://localhost:8000/v1/realtime` 暴露一个 WebSocket 端点。

## 客户端示例

下面是一个流式发送音频文件并接收转写结果的基础客户端：

```
import asyncio
import base64
import json
import librosa
import numpy as np
import websockets

def load_audio_as_pcm16(audio_path: str) -> bytes:
    """Load audio file and convert to PCM16 @ 16kHz."""
    audio, _ = librosa.load(audio_path, sr=16000, mono=True)
    return (audio * 32767).astype(np.int16).tobytes()

async def stream_audio_file(audio_path: str, server_url: str = "ws://localhost:8000/v1/realtime"):
    async with websockets.connect(server_url) as ws:
        response = json.loads(await ws.recv())

        # Load and convert audio to PCM16
        pcm_audio = load_audio_as_pcm16(audio_path)

        # Validate model
        await ws.send(json.dumps({"type": "session.update", "model": model}))

        # Signal start of audio stream
        await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))

        # Stream audio in 4KB chunks
        for i in range(0, len(pcm_audio), 4096):
            chunk = pcm_audio[i:i + 4096]
            await ws.send(json.dumps({
                "type": "input_audio_buffer.append",
                "audio": base64.b64encode(chunk).decode()
            }))

        # Signal end of audio stream
        await ws.send(json.dumps({"type": "input_audio_buffer.commit", "final": True}))

        # Receive transcription
        async for message in ws:
            data = json.loads(message)
            if data["type"] == "transcription.delta":
                print(data["delta"], end="", flush=True)
            elif data["type"] == "transcription.done":
                break

asyncio.run(stream_audio_file("audio.wav"))
```

该示例展示了实时音频流的核心工作流程：

- **加载并转换音频**：音频文件被加载并转换为 16kHz 的 PCM16 格式，这是实时 API 期望的输入格式
- **建立 WebSocket 连接**：连接到服务器的 `/v1/realtime` 端点，并发送 `session.update` 消息以校验模型
- **分块流式发送音频**：音频以 4KB 块的形式通过 `input_audio_buffer.append` 消息发送，并用 `input_audio_buffer.commit` 信号标记流的开始与结束
- **增量接收转写**：服务器以包含部分转写内容的 `transcription.delta` 消息进行响应，实时打印，直到收到 `transcription.done`
- **关于实时行为的说明**：虽然本示例为了简单起见先发送全部音频再监听转写，但 WebSocket 协议支持完全异步的通信——音频块的发送与转写的接收可以同时进行。在生产级实时服务中，转写会在第一个音频块到达时立即开始，发送与接收同时进行，实现真正低延迟的语音识别

## 消息类型

Realtime API 使用基于消息的协议。关键消息类型包括：

**客户端到服务器：**

- `session.create`：初始化新会话
- `input_audio_buffer.append`：发送音频数据
- `input_audio_buffer.commit`：指示音频输入结束
- `response.create`：请求模型响应

**服务器到客户端：**

- `session.created`：会话初始化已确认
- `response.text.delta`：增量文本输出
- `response.audio.delta`：增量音频输出（用于 TTS 模型）
- `response.done`：响应完成
- `error`：发生错误

## 示例脚本

vLLM 仓库包含开箱即用的示例客户端：

- [examples/online\_serving/openai\_realtime\_client.py](https://docs.vllm.ai/en/latest/examples/online_serving/openai_realtime_client/?h=realtime#openai-realtime-client)：基础 WebSocket 客户端
- [examples/online\_serving/openai\_realtime\_microphone\_client.py](https://docs.vllm.ai/en/latest/examples/online_serving/openai_realtime_microphone_client/#openai-realtime-microphone-client)：麦克风集成

这些示例演示了如何从系统麦克风采集音频并实时流式传输到 vLLM。

## 性能考量

与仅发送独立请求相比，使用专门的基于 `AsyncGenerator` 的会话接口的一个优势是：会话的 KV 缓存会原样保留。这比依赖 vLLM 的自动前缀缓存更好，原因在于：

- 它确保在等待下一个输入块期间，相应的缓存块不会被逐出
- 前缀缓存工作在块级别（通常为 16 token），否则每个新输入都会有少量已有 token 被重新计算

然而，这也意味着必须额外小心，避免让会话一直保持打开状态，因为它们会阻止相应内存被其他请求使用，可能损害整体容量/吞吐量。目前，vLLM 不会抢占“空闲”的流式输入会话——这一行为将在未来的更新中改进。

## 未来方向

我们对 vLLM 中流式输入支持的潜力感到兴奋。随着更多模型提供方开源与我们输入流式设计兼容的、完全可流式的模型权重，我们期待实时应用生态的显著增长。

由于流式输入在 LLM 服务中仍是一项新颖的能力，我们预计会持续调整和扩展我们的实现，以支持尽可能多的不同架构与用例。这包括探索与各种音频、视频编码器更紧密的集成，针对不同延迟需求优化锚定请求模式，以及扩展对多模态流式场景的支持。

## 参与进来

我们鼓励你试用 vLLM 的输入流式功能与 Realtime API。你的反馈对我们改进这些功能非常宝贵。请在 [vLLM GitHub 仓库](https://github.com/vllm-project/vllm)上分享你的经验、报告问题或提出改进建议。

在我们持续开发 vLLM 实时能力的过程中，欢迎反馈与贡献。

## 致谢

流式输入支持与 Realtime API 的实现得益于多个团队的协作努力：

**Meta：** Joshua Deng、Jiatong Zhou、Zhuohan Li、Yu Luo、Jeremy Teboul

**Mistral AI：** Patrick von Platen、Andy Lo

**vLLM 团队：** Nick Hill、Roger Wang、Cyrus Leung、Nicolò Lucchesi、Woosuk Kwon

我们还要感谢 vLLM 中其他流式输入实现的工作：Tao He（Alibaba Qwen）、Edward Wibowo（Brown University）、Deepti Raghavan（Brown University）与 Luis Gaspar Schroeder（UC Berkeley）。

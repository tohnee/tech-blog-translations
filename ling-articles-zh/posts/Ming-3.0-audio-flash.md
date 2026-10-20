---
title: "inclusionAI/Ming-3.0-audio-flash"
title_en: "inclusionAI/Ming-3.0-audio-flash"
source: https://github.com/inclusionAI/Ming-3.0-audio-flash/blob/main/README.md
crawled: 2026-10-20
translated: 2026-10-20
---

<div align="center">

<h1><img src="assets/ming-3.0-audio-logo.png" alt="Ming logo" height="42"> Ming-3.0-audio-flash</h1>

### 清晰聆听，深度理解，智能行动。

一个面向真实场景语音识别、音频理解、推理与端到端语音交互的原生音频模型。

[![License: MIT](https://img.shields.io/badge/License-MIT-3da639.svg)](LICENSE) [![Transformers: 5.14.1](https://img.shields.io/badge/Transformers-5.14.1-ffcc4d.svg)](requirements-transformers.txt) [![Serving: vLLM--Omni](https://img.shields.io/badge/Serving-vLLM--Omni-7c3aed.svg)](requirements-vllm-omni.txt) [![Serving: SGLang](https://img.shields.io/badge/Serving-SGLang-2563eb.svg)](requirements-sglang.txt)

[🤗 Hugging Face · Flash](https://huggingface.co/inclusionAI/Ming-3.0-audio-flash) · [🤗 Hugging Face · Tiny](https://huggingface.co/inclusionAI/Ming-3.0-audio-tiny) · [🤖 ModelScope · Flash](https://modelscope.cn/models/inclusionAI/Ming-3.0-audio-flash) · [📓 Cookbook](cookbook.ipynb) · [💻 示例](examples/README.md)

</div>

---



https://github.com/user-attachments/assets/2accce07-c451-4132-9fc4-1ed375888a24



## 🧩 模型变体

- **[Ming-3.0-audio-flash](https://huggingface.co/inclusionAI/Ming-3.0-audio-flash)** — 一个拥有 126B 参数、6.5B 激活参数的混合专家（Mixture-of-Experts）模型。下文示例与基准结果使用的即该模型。
- **[Ming-3.0-audio-tiny](https://huggingface.co/inclusionAI/Ming-3.0-audio-tiny)** — 一个紧凑的 9.3B 参数、2.7B 激活参数的混合专家模型。检查点细节与使用指引请参见其模型卡。

## ✨ 亮点

- 🎙️ **复杂语音识别** — 识别带方言、口音、噪声环境与多人会议的中英文语音。
- ⏱️ **长音频理解** — 理解并分析长篇录音。
- 🎧 **多维感知** — 理解细粒度语音、非语音声音、声学场景与音乐。
- 💡 **音频推理** — 直接对音频内容进行分析与推理。
- 🗣️ **音频交互** — 支持端到端语音对话，可选合成语音输出。

Ming-3.0-audio-flash 打通了从**听见声音**、到**理解信息**、再到**完成任务**的闭环。

## 🏗️ 架构

<p align="center">
  <img src="assets/ming-3.0-audio-flash-architecture.png" alt="Ming-3.0-audio-flash architecture" width="70%">
</p>

## 📊 基准

所有分数均以百分比报告。↑ 表示越高越好，↓ 表示越低越好。Ming-3.0-audio-flash 在非思考（non-thinking）模式下评测。**加粗**表示最佳结果，<u>下划线</u>表示次佳结果，星号（`*`）表示在我们自己的评测中获得的结果。

### 语音识别

![ASR benchmark results](assets/benchmark-asr.png)

### 音频智能

![Audio intelligence benchmark results](assets/benchmark-audio-intelligence.png)

### 文本智能

<p align="center">
  <img src="assets/benchmark-text.png" alt="Text intelligence benchmark results" width="80%">
</p>

> [!NOTE]
> 对比模型的结果是在我们的评测设置下复现的，由于提示词、解码设置、模型版本与评测流水线的差异，可能与其官方报告不同。

## 🧭 推理选项

| | vLLM-Omni | SGLang | Transformers |
| --- | --- | --- | --- |
| 最适场景 | 服务部署与语音交互 | 高吞吐文本服务 | 本地评测与研究 |
| 输入 | 音频 + 文本指令 | 音频 + 文本指令 | 音频 + 文本指令 |
| 输出 | 文本，或文本 + 语音 | 文本 | 文本，或文本 + 语音 |
| 接口 | OpenAI 兼容 API | OpenAI 兼容 API | Hugging Face AutoClass |
| 依赖 | `requirements-vllm-omni.txt` | `requirements-sglang.txt` | `requirements-transformers.txt` |

## 🚀 快速开始

### 1️⃣ 下载模型

```bash
pip install -U huggingface_hub
hf download inclusionAI/Ming-3.0-audio-flash \
  --local-dir inclusionAI/Ming-3.0-audio-flash

export MODEL_PATH="$PWD/inclusionAI/Ming-3.0-audio-flash"
```

<details>
<summary>从 ModelScope 下载</summary>

```bash
pip install -U modelscope
modelscope download --model inclusionAI/Ming-3.0-audio-flash \
  --local_dir inclusionAI/Ming-3.0-audio-flash \
  --revision master

export MODEL_PATH="$PWD/inclusionAI/Ming-3.0-audio-flash"
```

</details>

模型目录包含分词器、处理器、模型实现、检查点分片与 Talker 资源。大体积模型文件通过 Hugging Face 和 ModelScope 分发，而不是放在这个 GitHub 仓库中。

### 2️⃣ 启动服务器

#### vLLM-Omni

安装 [inclusionAI/vllm-omni](https://github.com/inclusionAI/vllm-omni/tree/model/ming3-audio-flash) 的 Ming-3.0-audio-flash 分支：

```bash
python3 -m venv .venv-vllm-omni
source .venv-vllm-omni/bin/activate
pip install -r requirements-vllm-omni.txt
```

该分支包含 `bailing_moe_v3_audio` 流水线与当前的 Ming Talker 请求接口。它通过 Chat Completions 的 `audio.voice` 支持 IP 音色与已注册的音色 ID，并通过 `ref_audio` 加 `prompt_text` 支持声音克隆。

为音频理解与推理启动文本输出服务：

```bash
MING_OUTPUT_MODE=text ./scripts/serve_vllm_omni.sh "$MODEL_PATH"
```

复现带 10-gram 阻断支持的识别评测时，请使用 ASR 配置：

```bash
MING_OUTPUT_MODE=asr ./scripts/serve_vllm_omni.sh "$MODEL_PATH"
```

也可以同时启用文本与合成语音输出：

```bash
MING_OUTPUT_MODE=audio ./scripts/serve_vllm_omni.sh "$MODEL_PATH"
```

对于 Ming-3.0-audio-tiny，将 `MODEL_PATH` 指向 Tiny 检查点并选择 Tiny 部署配置：

```bash
export MODEL_PATH="$PWD/inclusionAI/Ming-3.0-audio-tiny"
MING_MODEL_VARIANT=tiny MING_OUTPUT_MODE=text ./scripts/serve_vllm_omni.sh "$MODEL_PATH"
```

当模型目录名包含 `tiny` 时，`scripts/serve_vllm_omni.sh` 也会自动识别 Tiny。使用自定义目录名时请显式设置 `MING_MODEL_VARIANT`。

> [!NOTE]
> 默认的 Flash 配置在八张 GPU 上使用张量并行。这是在 80 GB H800 GPU 上实现默认 128K 上下文长度所必需的，因为 vLLM 会在启动时按所配置的上下文长度预留 KV 缓存显存。在 full-audio 配置中，Talker 复用 GPU 7 并使用独立的显存预算。Tiny 的 full-audio 配置每个阶段使用一张 GPU。请根据你的硬件在 `deploy/*.yaml` 中调整 `devices`、上下文与序列限制以及 `gpu_memory_utilization`。

#### SGLang

在独立环境中安装 [inclusionAI/sglang_ling_v3](https://github.com/inclusionAI/sglang_ling_v3/tree/ling_v3_audio_for_pr) 的 audio 分支：

```bash
python3 -m venv .venv-sglang
source .venv-sglang/bin/activate
pip install -r requirements-sglang.txt
```

当本仓库旁边已有 `sglang_ling_v3` 源码检出时，可以改为以可编辑模式安装该检出：

```bash
pip install -e ../sglang_ling_v3/python
```

使用经过验证的四卡配置启动 Ming-3.0-audio-flash：

```bash
./scripts/serve_sglang.sh "$MODEL_PATH"
```

对于 Ming-3.0-audio-tiny，使用其检查点与单卡配置：

```bash
export MODEL_PATH="$PWD/inclusionAI/Ming-3.0-audio-tiny"
MING_MODEL_VARIANT=tiny CUDA_VISIBLE_DEVICES=0 \
  ./scripts/serve_sglang.sh "$MODEL_PATH"
```

SGLang 示例目前仅覆盖音频输入加文本输出。需要合成语音输出时，请使用 vLLM-Omni 或直接的 Transformers 推理。

### 3️⃣ 发送请求

#### vLLM-Omni

```bash
pip install -r requirements-client.txt
```

**语音识别**

```bash
python examples/vllm_omni_audio_chat.py examples/audio/introduce_ant_group.wav \
  --task asr \
  --prompt 'Please recognize the language of this speech and transcribe it, placing a `\t` between the identified language and the transcribe.' \
  --max-tokens 256 \
  --no-repeat-ngram-size 10
```

**语音回复**

```bash
python examples/vllm_omni_audio_chat.py examples/audio/introduce_ant_group.wav \
  --audio-response \
  --output-audio outputs/answer.wav
```

默认情况下，vLLM-Omni 使用内置 IP 音色 `灵小柔`。传入 `--voice` 可从[完整的内置音色列表](docs/voices.md)中选择其他 IP 音色，或使用 `GET /v1/audio/voices` 返回的已注册音色 ID。客户端会将其作为 Chat Completions 的 `audio.voice: {"id": "..."}` 发送。音色选择不能与 `--ref-audio` 组合使用；省略该参数则使用服务器默认值。

模型目录还在 `voice_presets/voice_audio/` 下提供了两个预设参考音色 `灵楷` 和 `US_James`，其配套转写文本记录在 `voice_presets/voice_prompts.json` 中。通过 `--ref-audio` 和 `--prompt-text` 可使用这些预设，或其他参考 WAV 及其精确转写文本：

```bash
python examples/vllm_omni_audio_chat.py examples/audio/introduce_ant_group.wav \
  --audio-response \
  --ref-audio path/to/reference.wav \
  --prompt-text "<exact transcript of the reference audio>" \
  --output-audio outputs/cloned_answer.wav
```

**带延迟指标的流式语音回复**

```bash
python examples/vllm_omni_audio_streaming.py examples/audio/introduce_ant_group.wav \
  --output-audio outputs/stream_answer.wav
```

客户端默认使用 `http://localhost:8091/v1`，并自动选择 `/v1/models` 返回的第一个模型。可通过 `--base-url`、`--api-key` 和 `--model`，或相应的 `MING_*` 环境变量覆盖连接设置。

#### SGLang

SGLang 客户端使用该分支的 `input_audio` 消息格式发送原始 base64 音频。对默认端点 `http://localhost:8008/v1` 运行 ASR：

```bash
python examples/sglang_audio_chat.py examples/audio/introduce_ant_group.wav \
  --task asr \
  --max-tokens 256
```

进行语音问答时，使用经过验证的默认系统提示词：

```bash
python examples/sglang_audio_chat.py examples/audio/introduce_ant_group.wav
```

使用 `--base-url` 和 `--model`，或 `MING_SGLANG_BASE_URL` 和 `MING_SGLANG_MODEL` 覆盖端点或所服务的模型。

## 🤗 Transformers 推理

为直接推理使用隔离环境：

```bash
python3 -m venv .venv-transformers
source .venv-transformers/bin/activate
pip install -r requirements-transformers.txt
```

**语音识别**

```bash
python examples/transformers_audio.py examples/audio/introduce_ant_group.wav \
  --model "$MODEL_PATH" \
  --task asr \
  --prompt 'Please recognize the language of this speech and transcribe it, placing a `\t` between the identified language and the transcribe.' \
  --max-new-tokens 256 \
  --no-repeat-ngram-size 10
```

**语音问答**

```bash
python examples/transformers_audio.py examples/audio/introduce_ant_group.wav \
  --model "$MODEL_PATH"
```

**Thinker + 原生 Talker**

使用随模型附带的 Talker 实现来生成语音，无需启动 vLLM-Omni 服务器：

```bash
python examples/transformers_thinker_talker.py \
  --model "$MODEL_PATH" \
  --audio examples/audio/introduce_ant_group.wav \
  --voice US_Stella \
  --thinker-max-memory 72GiB \
  --output outputs/answer.wav
```

同样支持基于参考音频的声音克隆：

```bash
python examples/transformers_thinker_talker.py \
  --model "$MODEL_PATH" \
  --audio examples/audio/introduce_ant_group.wav \
  --ref-audio path/to/reference.wav \
  --prompt-text "<exact transcript of the reference audio>" \
  --output outputs/cloned_answer.wav
```

> [!IMPORTANT]
> 直接推理会以 `trust_remote_code=True` 加载模型注册的 AutoClass。在你的环境中启用远程代码之前，请先审查下载的模型代码。原生语音输出还会额外导入模型目录中附带的 Talker 实现。

## 📚 更多示例

- 在 [`examples/README.md`](examples/README.md) 中浏览各任务的提示词。
- 运行 [`cookbook.ipynb`](cookbook.ipynb) 中的交互式演练。
- 查看 [`examples/audio/`](examples/audio/) 中附带的样本与元数据。

## 🗂️ 仓库结构

```text
Ming-3.0-audio-flash/
├── cookbook.ipynb                  # Interactive walkthrough
├── deploy/                         # vLLM-Omni deployment profiles
├── examples/
│   ├── audio/                      # Sample audio and metadata
│   ├── sglang_audio_chat.py         # SGLang text-output client
│   ├── vllm_omni_audio_chat.py      # Text and non-streaming speech client
│   ├── vllm_omni_audio_streaming.py # Streaming speech and latency metrics
│   ├── transformers_thinker_talker.py # Direct Thinker-to-Talker inference
│   └── transformers_audio.py       # Direct Transformers inference
├── scripts/
│   ├── serve_vllm_omni.sh          # vLLM-Omni launcher
│   └── serve_sglang.sh             # SGLang launcher
├── requirements-client.txt         # Lightweight API client dependencies
├── requirements-sglang.txt         # Compatible SGLang audio branch
├── requirements-vllm-omni.txt      # Compatible vLLM-Omni server branch
└── requirements-transformers.txt   # Direct inference dependencies
```

## 🔌 API 格式

vLLM-Omni 端点接受 base64 data URL 形式的音频：

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this audio."},
            {
                "type": "audio_url",
                "audio_url": {"url": "data:audio/wav;base64,..."},
            },
        ],
    }
]
```

使用 `modalities=["text"]` 输出文本，或使用 `modalities=["text", "audio"]` 输出文本与合成语音。

SGLang 端点在 `input_audio` 内容项中使用原始 base64 音频：

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_audio",
                "input_audio": {"data": audio_base64, "format": "wav"},
            },
            {"type": "text", "text": "Describe this audio."},
        ],
    }
]
```

Chat Completions 的语音输出通过 `audio.voice` 选择 IP 音色或已注册音色：

```python
audio = {
    "format": "wav",  # The streaming client uses vLLM-Omni's raw PCM format.
    "voice": {"id": "灵小柔"},
}
```

服务器会先检查其 IP 音色列表，再查找已注册的参考音色。
省略 `voice` 即使用默认的内置 IP 音色 `灵小柔`。

基于参考音频的声音克隆使用原始 base64 音频及其转写文本：

```python
additional_information = {
    "voice_mode": "reference",
    "ref_audio": reference_audio_base64,
    "prompt_text": reference_audio_transcript,
}
```

## 📄 许可证

本项目依据 [MIT License](LICENSE) 发布。法律免责声明见 [LEGAL.md](LEGAL.md)。

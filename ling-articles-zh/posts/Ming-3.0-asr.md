---
title: "inclusionAI/Ming-3.0-asr"
title_en: "inclusionAI/Ming-3.0-asr"
source: https://github.com/inclusionAI/Ming-3.0-asr/blob/main/README.md
crawled: 2026-10-20
translated: 2026-10-20
---

<p align="center">
  <img src="figures/bailing-logo.png" width="64" alt="Bailing logo">
</p>

<h1 align="center">Ming-3.0-asr-tiny：上下文感知语音识别</h1>

<p align="center"><i>中英文 · 方言 · 热词与对话上下文</i></p>

<p align="center">
  <a href="https://huggingface.co/inclusionAI/Ming-3.0-asr-tiny"><b>Hugging Face</b></a>
  &nbsp;·&nbsp; <a href="https://www.modelscope.cn/models/inclusionAI/Ming-3.0-asr-tiny"><b>ModelScope</b></a>
  &nbsp;·&nbsp; <a href="https://niniandy.github.io/Ming-3.0-asr-tiny-blog/"><b>项目博客</b></a>
  &nbsp;·&nbsp; <a href="#quick-start"><b>快速开始</b></a>
  &nbsp;·&nbsp; <a href="#cookbook"><b>Cookbook</b></a>
  &nbsp;·&nbsp; <a href="#evaluation"><b>评测</b></a>
</p>

## 不止于逐字转写

真实语音总是带着口音、背景噪声、陌生的名字和专门术语。**Ming-3.0-asr-tiny** 将 Ling-tiny-v3 语言模型与音频编码器相结合，用于中英文转写、方言识别与上下文 ASR（Context ASR）。热词或前文对话可以帮助识别领域专属表达。

- **中英文 ASR：**通过一个 Transformers 接口转写单轮语音。
- **方言识别：**在 15 个测试集上评测，覆盖湖南、闽南、粤语、川渝、上海、安徽、东北、河南、湖北、江苏、客家、陕西、山东、天津与云南。
- **上下文 ASR：**在转写提示词中加入相关的人名、地名、产品或术语。
- **高难语音：**评测覆盖聊天、政务、健康、知识、本地生活与高噪声场景。

## 介绍视频

https://github.com/user-attachments/assets/11ca7c5f-f827-4ed4-ab57-b4315f410cf5

[观看发布影片](https://github.com/NiniAndy/Ming-3.0-asr-tiny-blog/releases/download/media-2026-10-19/ming-3.0-asr-final.mp4)

## 架构

<p align="center"><a href="figures/model.jpg"><img src="figures/model.jpg" width="800" alt="Ming-3.0-asr-tiny model architecture"></a></p>

<a id="evaluation"></a>
## 评测

### ASR 总览

<p align="center"><a href="figures/asr.png"><img src="figures/asr.png" width="1000" alt="ASR performance overview"></a></p>

### 中英文 ASR

<p align="center"><a href="figures/open-asr.png"><img src="figures/open-asr.png" width="1000" alt="Chinese and English ASR evaluation"></a></p>

### 方言与领域识别

<p align="center"><a href="figures/inhouse-asr.png"><img src="figures/inhouse-asr.png" width="1000" alt="Dialect and domain ASR evaluation"></a></p>

### 上下文 ASR

<p align="center"><a href="figures/contextasr.png"><img src="figures/contextasr.png" width="1000" alt="Context ASR evaluation"></a></p>

<a id="quick-start"></a>
## 快速开始

### 1. 创建环境

在配备 CUDA GPU 的 Linux 上使用 Python 3.12。Transformers 路径使用模型包内固定的依赖版本；SGLang 则使用第 5 步中的独立环境。

```bash
git clone https://github.com/inclusionAI/Ming-3.0-asr.git
cd Ming-3.0-asr
python3.12 -m venv .venv
source .venv/bin/activate
unset PYTHONPATH
```

推理栈使用 Transformers 5.12.1、fla-core 0.5.2 和 PyTorch 2.11.0。如需其他 CUDA 版本，请按照 [PyTorch 官方指南](https://pytorch.org/get-started/previous-versions/)安装与之匹配的 PyTorch 与 torchaudio 2.11.0 版本。

### 2. 下载模型

模型权重、分词器、配置与自定义 Transformers 实现在 [Hugging Face](https://huggingface.co/inclusionAI/Ming-3.0-asr-tiny) 上一同发布：

```bash
python -m pip install "huggingface_hub[cli]"
hf download inclusionAI/Ming-3.0-asr-tiny --local-dir ./Ming-3.0-asr-tiny-model
export MODEL_DIR="$(cd ./Ming-3.0-asr-tiny-model && pwd)"
python -m pip install -r "$MODEL_DIR/requirements.txt"
python tools/verify_repository.py --checkpoint "$MODEL_DIR"
```

### 3. 转写一段音频

```bash
python examples/transcribe.py \
  --model "$MODEL_DIR" \
  --audio examples/cases/audio/chinese_common_voice.wav \
  --output outputs/transcript.json
```

示例输出：`漓江和湘江有秦代开凿的灵渠沟通`。将 `--audio` 替换为你自己的 WAV 文件即可。普通 ASR 与上下文 ASR 使用相同的音频输入格式。默认路径使用 CUDA、BF16、SDPA、贪心解码、10-gram 重复限制以及最多 256 个新 token。关于主题与热词提示，参见[上下文 ASR 指南](cookbook/context-asr.en.md)。

### 4. 原生 PyTorch / Transformers 推理

以下是[可运行示例](examples/transcribe.py)所使用的核心调用。请在仓库根目录下运行：

```python
import os

import soundfile as sf
import torch
from transformers import AutoModelForCausalLM, AutoProcessor
from examples.hf_runtime import decode_transcript, prepare_asr_request

checkpoint = os.environ["MODEL_DIR"]
processor = AutoProcessor.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    checkpoint, trust_remote_code=True, dtype=torch.bfloat16,
    device_map="cuda:0", attn_implementation="sdpa",
).eval()
waveform, sample_rate = sf.read(
    "examples/cases/audio/chinese_common_voice.wav", dtype="float32", always_2d=True,
)
inputs = prepare_asr_request(processor, (waveform.T, sample_rate)).to(model.device)

with torch.inference_mode():
    eos = model.config.text_config.eos_token_id
    output = model.generate(
        **inputs, max_new_tokens=256, do_sample=False,
        eos_token_id=eos, pad_token_id=eos, no_repeat_ngram_size=10,
    )

print(decode_transcript(
    processor.tokenizer, output[0, inputs.input_ids.shape[1]:].tolist(),
))
```

### 5. SGLang 加速服务

使用下方固定提交处的 [Ming SGLang 适配分支](https://github.com/inclusionAI/sglang_ling_v3/tree/ling_v3_audio_for_pr)。该仓库包含模型类别别名补丁与服务示例。

请为 SGLang 使用独立的 Python 3.12 环境。保留第 2 步下载的模型，然后在仓库根目录运行以下命令：

```bash
python3.12 -m venv .venv-sglang
source .venv-sglang/bin/activate
unset PYTHONPATH
python -m pip install -r cookbook/sglang/requirements.txt
python -m pip check
git clone --single-branch --branch ling_v3_audio_for_pr \
  https://github.com/inclusionAI/sglang_ling_v3.git ../sglang_ming_asr
export SGLANG_DIR="$(cd ../sglang_ming_asr && pwd)"
git -C "$SGLANG_DIR" checkout bba862771a9e3413a062dad33e8b494ea9f7755b
export GUIDE_DIR="$(pwd)/cookbook/sglang"
export PYTHON_BIN="$(command -v python)"
SGLANG_DIR="$SGLANG_DIR" bash "$GUIDE_DIR/scripts/apply_patch.sh"
export PYTHONPATH="$SGLANG_DIR/python:$MODEL_DIR"
"$PYTHON_BIN" "$GUIDE_DIR/scripts/check_env.py" \
  --model "$MODEL_DIR" --sglang-dir "$SGLANG_DIR"
```

在这个终端启动服务器，待 `/health` 返回 HTTP 200 后，在另一个终端运行客户端：

```bash
export GPU_ID=0 PORT=8000 HOST=127.0.0.1 SERVED_MODEL=ming-asr
PYTHON_BIN="$PYTHON_BIN" MODEL_DIR="$MODEL_DIR" SGLANG_DIR="$SGLANG_DIR" \
  bash "$GUIDE_DIR/scripts/start_server.sh"
```

```bash
curl -fsS http://127.0.0.1:8000/health
python cookbook/sglang/scripts/transcribe.py \
  --audio examples/cases/audio/chinese_common_voice.wav \
  --base-url http://127.0.0.1:8000 --model ming-asr
```

示例转写文本为 `漓江和湘江有秦代开凿的灵渠沟通`。远程服务、英文音频与数据集评测设置请参见[完整的 SGLang 指南](cookbook/sglang/README.en.md)。

<a id="cookbook"></a>
## Cookbook：从转写到上下文

打开每个 WAV 样本试听，然后将参考文本与模型输出进行对比。标点已去除，英文统一转为小写显示。

### 普通话转写

[▶ 播放音频](https://niniandy.github.io/Ming-3.0-asr-tiny-blog/assets/audio/chinese_common_voice.wav)

| 项目 | 文本 |
| --- | --- |
| 参考 | 漓江和湘江有秦代开凿的灵渠沟通 |
| 模型输出 | 漓江和湘江有秦代开凿的灵渠沟通 |

### 英文转写

[▶ 播放音频](https://niniandy.github.io/Ming-3.0-asr-tiny-blog/assets/audio/english_common_voice.wav)

| 项目 | 文本 |
| --- | --- |
| 参考 | same way you did |
| 模型输出 | same way you did |

### 上下文 ASR：纠正电影片名

只有第二个请求在同一段音频上加入了主题与热词。

[▶ 播放音频](https://niniandy.github.io/Ming-3.0-asr-tiny-blog/assets/audio/context_same_sentence_pcm16.wav)

| 项目 | 文本 |
| --- | --- |
| 参考 | 你们看了黄国权那部**同囚**没我昨晚看完到现在还缓不过来 |
| 主题 | 同囚 |
| 热词 | 同囚、黄国权、游学修、关楚耀、赵永洪、赵咏瑶、狱警、长镜头、吞玻璃戏、糖化玻璃、真实案例数据 |
| 无上下文 | 你们看了黄国权那部**铜球**没我昨晚看完到现在还缓不过来 |
| 有上下文 | 你们看了黄国权那部**同囚**没我昨晚看完到现在还缓不过来 |

```bash
python examples/transcribe.py --model "$MODEL_DIR" \
  --manifest examples/cases/context.jsonl \
  --output outputs/context-demo.jsonl \
  --language-hint zh --max-new-tokens 256
```

更多细节参见 [Transformers 指南](cookbook/hf-inference.md)、[上下文 ASR 指南](cookbook/context-asr.en.md)、[评测指南](cookbook/evaluation.md)与 [SGLang 指南](cookbook/sglang/README.en.md)。

音频来源：上下文 ASR 片段来自 [ContextASR-Bench](https://huggingface.co/datasets/MrSupW/ContextASR-Bench)；普通话与英文片段来自 [Mozilla Common Voice](https://commonvoice.mozilla.org/en/datasets)。

## 使用注意事项

- 音频会被下混并重采样到 16 kHz。长音频可以分块编码，但受模型上下文长度限制。
- 请使用 `from_pretrained(..., dtype=torch.bfloat16)` 加载。避免对整个模型调用 `.bfloat16()`，否则可能改变需要 FP32 的参数与缓冲区。
- 输出为纯文本，不含词级时间戳或说话人分离。不支持图像与视频输入。
- 示例采用单 GPU、非流式、无量化的推理。

## 许可证

本仓库的代码与模型权重依据 [MIT License](LICENSE) 发布。HF 模型包中的 Apache-2.0 源文件保留其声明与许可证。演示音频保留其来源许可证，见[音频来源说明](examples/cases/README.md)。

## 引用

如果你使用了 Ming-3.0-asr-tiny，请引用本仓库。机器可读的元数据见 [CITATION.cff](CITATION.cff)。

```bibtex
@misc{ming_3_0_asr_tiny_2026,
  author = {{inclusionAI}},
  title = {Ming-3.0-asr-tiny: Context-Aware Speech Recognition},
  year = {2026},
  url = {https://github.com/inclusionAI/Ming-3.0-asr}
}
```

<!-- Core contributors: Xuyi Zhuang · Xuezhi Wang · Chunxiang Jin · Hao Chen. Special thanks to the Bailing team at Ant Group. -->

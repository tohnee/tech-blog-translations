---
title: "MiMo-Audio-Tokenizer：统一语义提取与高保真音频重建的音频分词器"
title_en: "XiaomiMiMo/MiMo-Audio-Tokenizer"
source: https://github.com/XiaomiMiMo/MiMo-Audio-Tokenizer/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-Audio-Tokenizer：统一语义提取与高保真音频重建的音频分词器

> 原文：[XiaomiMiMo/MiMo-Audio-Tokenizer](https://github.com/XiaomiMiMo/MiMo-Audio-Tokenizer/blob/main/README.md) · 小米 MiMo

<div align="center">

<img src="https://raw.githubusercontent.com/XiaomiMiMo/MiMo-VL/main/figures/Xiaomi_MiMo.png" alt="Description" width="25%" />

# MiMo-Audio-Tokenizer

<img src="mimo_audio_tokenizer/assets/Tokenizer_01.png" alt="Description" width="90%" />

<p><em>一个统一的分词器（tokenizer），既能提取语义信息，又能实现高保真音频重建。</em></p>

</div>

## 关键特性

- 以规模化的参数与训练数据开启音频分词的新前沿
  - 1.2B 参数的纯 Transformer 架构，兼顾效率与效果
  - 从零训练，数据超过 1100 万小时，同时覆盖音频重建任务与音频到文本（A2T）任务

- 统一表示同时增强跨模态对齐与语音重建质量
  - 联合捕获语义与声学信息，并进一步缓解语义-声学表示之间的冲突

## 安装

```sh
git clone https://github.com/XiaomiMiMo/MiMo-Audio-Tokenizer
cd MiMo-Audio-Tokenizer
# Install base dependencies
pip install -e .
# Install flash-attn
pip install -e ".[flash]"
```

## 模型下载

```sh
# you might need `sudo apt-get install git-lfs` before download this model
git clone https://huggingface.co/XiaomiMiMo/MiMo-Audio-Tokenizer
```

## 用法示例

### 0. 快速开始

```py
import torchaudio
import mimo_audio_tokenizer

# one-line model init
tokenizer = mimo_audio_tokenizer.load_model("path to your model").bfloat16().cuda()  # FlashAttention only support fp16 and bf16 data type

# preprocess
mels = []
wav_paths = ["mimo_audio_tokenizer/assets/BAC009S0764W0121.wav", "mimo_audio_tokenizer/assets/BAC009S0764W0122.wav", "mimo_audio_tokenizer/assets/猪八戒_gt.wav"]
for wav_path in wav_paths:
    wav = mimo_audio_tokenizer.load_audio(wav_path, tokenizer.config.sampling_rate)
    mels.append(mimo_audio_tokenizer.mel_spectrogram(wav, tokenizer.config))
mels, mels_lens = mimo_audio_tokenizer.padding(mels)  # (batch_size, n_mels, seq_len), (batch_size,)

# one-line encode
codes, codes_lens, _ = tokenizer.encode(mels.cuda(), mels_lens.cuda())  # (batch_size, max_len, num_quantizers), (batch_size,)

# one-line decode
wavs, wavs_lens, _ = tokenizer.decode(codes, codes_lens)  # (batch_size, 1, wav_len)

# inspect results
for i in range(len(wav_paths)):
    print(codes[i, :codes_lens[i].item()])

for i in range(len(wav_paths)):
    torchaudio.save(f"{i}.wav", wavs[i, :, :wavs_lens[i].item()].float().cpu().detach(),
                    tokenizer.config.sampling_rate, format='wav', encoding='PCM_S')

```

### 1. 通过命令行工具进行分布式离线批量推理

`mimo_audio_tokenizer` 为分布式离线批量推理而构建。

```sh
# 1 node 8 gpu, try to decrease `batch_size` if OOM
# task choices:
#   "wav2token": need `key` / `wav` / `quantized_tokens` available in data.jsonl
#   "token2wav": need `key` / `quantized_tokens` / `reconstructed_wav` available in data.jsonl
#   "wav2token2wav": need `key` / `wav` / `quantized_tokens` / `reconstructed_wav` available in data.jsonl
torchrun --nproc_per_node=8 --nnodes=1 \
     --rdzv_id=2025 --rdzv_backend="c10d" --rdzv_endpoint="localhost:0" \
    `which mimo_audio_tokenizer` \
        --model_path "path to your model" \
        --data_list "path to your data.jsonl" \
        --batch_size 64 \
        --num_workers 8 \
        --prefetch 16 \
        --num_quantizers 20 \
        --task "wav2token2wav"
```

### 数据格式示例

以下是 `data.jsonl` 示例：

```json
{"key": "uttid_1", "wav": "/mnt/data/audio/uttid_1.wav", "quantized_tokens": "/mnt/data/audio_reconstructed/uttid_1.json", "reconstructed_wav": "/mnt/data/audio_reconstructed/uttid_1.wav"}
...
{"key": "uttid_2", "wav": "/mnt/data/audio/uttid_2.wav", "quantized_tokens": "/mnt/data/audio_reconstructed/uttid_2.json", "reconstructed_wav": "/mnt/data/audio_reconstructed/uttid_2.wav"}
...
```

- `key` 是该样本的键。
- `wav` 是原始音频。
- `quantized_tokens` 是保存量化 token 的 json 路径（强烈建议在运行脚本前预先定义保存路径）。
- `reconstructed_wav` 是保存重建结果的 wav 路径（强烈建议在运行脚本前预先定义保存路径）。

### 2. 在线语音码提取

`mimo_audio_tokenizer` 也可以用于在线码提取，为 AudioLLM 的训练提供支持。

<table>
<tr>
<th>之前（离线提取码）</th>
<th>之后（在线提取码）</th>
</tr>
<tr>
<td>
<sub>

```py

class AudioLLM(nn.Module):
    ...
    def __init__(self, ...):
        ...

    def forward(self, speech_codes: Tensor, text_ids: Tensor, ...):
        ...
```

</sub>
<td>
<sub>

```py
import mimo_audio_tokenizer

class AudioLLM(nn.Module):
    ...
    def __init__(self, ...):
        ...
        self.audio_tokenizer = mimo_audio_tokenizer.load_model("path to your model")
        self.audio_tokenizer.freeze()  # no need for gradient calculation
        ...

    def forward(self, speech: Tensor, speech_lens: Tensor, text_ids: Tensor, ...):
        ...
        speech_codes, speech_codes_lens = self.audio_tokenizer.encode(speech, speech_lens)
        speech_codes = speech_codes.clone()  # for backward compatbility, stop gradient here
        speech_codes_lens = speeech_codes_lens.clone()  # for backward compatbility, stop gradient here
        ...
```

</sub>
</td>
</tr>
</table>

## 性能基准

|  方法  | RTF | 在 [Seed-TTS-Eval](https://github.com/BytedanceSpeech/seed-tts-eval) 上的结果 (PESQ-NB/PESQ-WB/SpkSim/STOI) |
|:------:|:--------------:|:--------------:|
|  mimo_audio_tokenizer (bs=64, n_q=20)  |   0.0028 (encode+decode)   | (zh) 3.81 / 3.38 / 0.93 / 0.94 |
|                                        |                            | (en) 3.59 / 3.10 / 0.95 / 0.94 |
|  mimo_audio_tokenizer (bs=64, n_q=8)   |   0.0028 (encode+decode)   | (zh) 3.44 / 2.93 / 0.91 / 0.92 |
|                                        |                            | (en) 3.12 / 2.60 / 0.93 / 0.93 |

测试配置

- 硬件：1 * H800 (80GB)
- 总请求数：1676（[zh 1010, en 666]）
- 注：测试 mimo_audio_tokenizer 时，我们将请求重复了 10000 次以获得更准确的 RTF。

## 引用

```bibtex
@misc{coreteam2025mimoaudio,
      title={MiMo-Audio: Audio Language Models are Few-Shot Learners},
      author={LLM-Core-Team Xiaomi},
      year={2025},
      url={https://github.com/XiaomiMiMo/MiMo-Audio},
}
```

## 联系方式

如有任何问题，请通过 [mimo@xiaomi.com](mailto:mimo@xiaomi.com) 联系我们，或提交 issue。

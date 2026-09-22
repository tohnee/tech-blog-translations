---
title: "MiMo-V2.5-ASR：跨语言、方言与复杂声学场景的鲁棒语音识别"
title_en: "XiaomiMiMo/MiMo-V2.5-ASR"
source: https://github.com/XiaomiMiMo/MiMo-V2.5-ASR/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-V2.5-ASR：跨语言、方言与复杂声学场景的鲁棒语音识别

> 原文：[XiaomiMiMo/MiMo-V2.5-ASR](https://github.com/XiaomiMiMo/MiMo-V2.5-ASR/blob/main/README.md) · 小米 MiMo

<div align="center">
  <img src="assets/XiaomiMIMO.png" width="60%" alt="Xiaomi-MiMo" />
</div>

<div align="center">
  <h3>
    <b>
      <span>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span><br/>
      MiMo-V2.5-ASR：跨语言、方言与复杂声学场景的鲁棒语音识别<br/>
      <span>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>
    </b>
  </h3>
</div>

<br/>

<div align="center" style="line-height: 1;">
  |
  <a href="https://huggingface.co/XiaomiMiMo/MiMo-V2.5-ASR" target="_blank">🤗 HuggingFace</a>
  &nbsp;|
  <a href="https://huggingface.co/spaces/XiaomiMiMo/MiMo-V2.5-ASR" target="_blank">🚀 在线演示</a>
  &nbsp;|
  <a href="https://mimo.xiaomi.com/mimo-v2-5-asr" target="_blank">📰 博客</a>
  &nbsp;|

  <br/>
</div>

<br/>

## 简介

**MiMo-V2.5-ASR** 是小米 MiMo 团队研发的、最先进的端到端自动语音识别（ASR）模型。它旨在为普通话与英语、多种中文方言、码切换（code-switch）语音、歌词、知识密集型内容、嘈杂声学环境以及多人对话提供准确而鲁棒的转写。MiMo-V2.5-ASR 在广泛的公开基准测试上取得了最先进的成果。

## 摘要

自动语音识别系统需要忠实转写来自不同语言、方言、口音和领域的语音信号，这些信号还在各种各样的声学条件下采集。尽管传统端到端模型在域内数据上表现出色，但在方言混杂、码切换、知识密集型内容、嘈杂环境和多人对话等具有挑战性的场景中，它们仍难以满足真实世界的要求。为此，我们提出 **MiMo-V2.5-ASR**，一个由小米 MiMo 团队研发的端到端语音识别模型。通过大规模中期训练（mid-training）、高质量监督微调以及一种新颖的强化学习算法，MiMo-V2.5-ASR 在以下维度上取得系统性提升：

- 🗣️ **中文方言**：原生支持吴语、粤语、闽南语、四川话等。
- 🔀 **码切换**：无需语言标签即可无缝转写中英码切换语音。
- 🎵 **歌曲识别**：对中英文歌曲进行高精度歌词转写，即使伴奏与人声混杂。
- 🔊 **嘈杂环境**：在强噪声、远场拾音等不利声学条件下保持鲁棒识别。
- 👥 **多人说话**：准确转写会议等重叠、多方对话。
- 🇬🇧 **复杂英语场景**：在 Open ASR 排行榜的 AMI 等高难度英语基准上处于领先。
- 📚 **知识密集型识别**：精确识别古诗词、专业术语、人名、地名等知识密集内容。
- 📝 **原生标点**：标点由韵律与语义原生生成，输出开箱即用的转写文本，无需后处理。

## 结果

MiMo-V2.5-ASR 已在覆盖标准普通话与英语、中文方言、歌词识别以及内部业务场景的广泛基准上完成评测。下图汇总了 MiMo-V2.5-ASR 在这些场景中的平均表现。

![结果](assets/MiMo_ASR_Results.png)

各基准的具体数字与定性案例，请参阅我们的[博客](https://mimo.xiaomi.com/mimo-v2-5-asr)。

## 模型下载

| 模型   | 🤗 Hugging Face |
|-------|-------|
| MiMo-Audio-Tokenizer | [XiaomiMiMo/MiMo-Audio-Tokenizer](https://huggingface.co/XiaomiMiMo/MiMo-Audio-Tokenizer) |
| MiMo-V2.5-ASR | [XiaomiMiMo/MiMo-V2.5-ASR](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-ASR) |

```bash
pip install huggingface-hub

hf download XiaomiMiMo/MiMo-Audio-Tokenizer --local-dir ./models/MiMo-Audio-Tokenizer
hf download XiaomiMiMo/MiMo-V2.5-ASR --local-dir ./models/MiMo-V2.5-ASR
```

## 快速开始

用内置的 Gradio 应用，几分钟即可启动 MiMo-V2.5-ASR 演示。

### 环境要求（Linux）

* Python 3.12
* CUDA >= 12.0

### 安装

```bash
git clone https://github.com/XiaomiMiMo/MiMo-V2.5-ASR.git
cd MiMo-V2.5-ASR
pip install -r requirements.txt
pip install flash-attn==2.7.4.post1
```

> \[!Note]
> 如果 flash-attn 编译耗时过长，可以下载预编译的 wheel 手动安装：
>
> * [下载预编译 wheel](https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.4.post1/flash_attn-2.7.4.post1+cu12torch2.6cxx11abiFALSE-cp312-cp312-linux_x86_64.whl)
>
> ```sh
> pip install /path/to/flash_attn-2.7.4.post1+cu12torch2.6cxx11abiFALSE-cp312-cp312-linux_x86_64.whl
> ```

### 运行演示

```bash
python run_mimo_asr.py
```

![MiMo-V2.5-ASR 演示](assets/MiMo_ASR_Demo.png)

这会为 MiMo-V2.5-ASR 启动一个本地 Gradio 界面。你可以：

* 上传音频文件，**或者**直接用麦克风录音。
* 可选地指定**语言标签**（中文 / 英文 / 自动）以让模型偏向特定语言，或保持**自动**以进行自动语言检测（推荐用于码切换语音）。
* 演示底层调用 `asr_sft()` 接口。

要在启动时自动加载模型和 tokenizer，请在命令行中传入它们的路径：

```bash
python run_mimo_asr.py \
    --model-path ./models/MiMo-V2.5-ASR \
    --tokenizer-path ./models/MiMo-Audio-Tokenizer
```

否则，请在 **Model Configuration** 标签页中输入 `MiMo-Audio-Tokenizer` 和 `MiMo-V2.5-ASR` 的本地路径，然后开始转写！

## Python API

`asr_sft` 接口的基本用法：

```python
from src.mimo_audio.mimo_audio import MimoAudio

model = MimoAudio(
    model_path="./models/MiMo-V2.5-ASR",
    tokenizer_path="./models/MiMo-Audio-Tokenizer",
)

# Automatic language detection (recommended for code-switching)
text = model.asr_sft("path/to/audio.wav")
print(text)

# With explicit language tag
text_zh = model.asr_sft("path/to/audio.wav", audio_tag="<chinese>")
text_en = model.asr_sft("path/to/audio.wav", audio_tag="<english>")
```

## 引用

```bibtex
@misc{coreteam2026mimov25asr,
      title={MiMo-V2.5-ASR: Robust Speech Recognition Across Languages, Dialects, and Complex Acoustic Scenarios},
      author={LLM-Core-Team Xiaomi},
      year={2026},
      url={https://github.com/XiaomiMiMo/MiMo-V2.5-ASR},
}
```

## 联系方式

如有任何问题，请通过 [mimo@xiaomi.com](mailto:mimo@xiaomi.com) 联系我们，或提交 issue。

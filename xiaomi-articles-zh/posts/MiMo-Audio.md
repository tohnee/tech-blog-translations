---
title: "MiMo-Audio：音频语言模型是少样本学习器"
title_en: "XiaomiMiMo/MiMo-Audio"
source: https://github.com/XiaomiMiMo/MiMo-Audio/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-Audio：音频语言模型是少样本学习器

> 原文：[XiaomiMiMo/MiMo-Audio](https://github.com/XiaomiMiMo/MiMo-Audio/blob/main/README.md) · 小米 MiMo

<div align="center">
  <picture>
    <source srcset="https://github.com/XiaomiMiMo/MiMo-VL/raw/main/figures/Xiaomi_MiMo_darkmode.png?raw=true" media="(prefers-color-scheme: dark)">
    <img src="https://github.com/XiaomiMiMo/MiMo-VL/raw/main/figures/Xiaomi_MiMo.png?raw=true" width="60%" alt="Xiaomi-MiMo" />
  </picture>
</div>

<h3 align="center">
  <b>
    <span>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>
    <br/>
    MiMo Audio：音频语言模型是少样本学习器<br/>MiMo Audio: Audio Language Models are Few-Shot Learners
    <br/>
    <span>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>
    <br/>
  </b>
</h3>

<br/>

<div align="center" style="line-height: 1;">
  |
  <a href="https://huggingface.co/collections/XiaomiMiMo/mimo-audio-68cc7202692c27dae881cce0" target="_blank">🤗 HuggingFace</a>
  &nbsp;|
  <a href="https://github.com/XiaomiMiMo/MiMo-Audio/blob/main/MiMo-Audio-Technical-Report.pdf" target="_blank">📄 论文</a>
  &nbsp;|
  <a href="https://xiaomimimo.github.io/MiMo-Audio-Demo" target="_blank">📰 博客</a>
  &nbsp;|
  <a href="https://github.com/XiaomiMiMo/MiMo-Audio-Eval" target="_blank">📊 MiMo-Audio-Eval</a>
  &nbsp;|

  <br/>
</div>

<br/>

## 简介

现有的音频语言模型通常依赖针对特定任务的微调来完成特定的音频任务。相比之下，人类只需少量示例或简单指令就能泛化到新的音频任务。GPT-3 已经证明，扩大下一 token 预测预训练的规模可以在文本领域带来强大的泛化能力，我们相信这一范式同样适用于音频领域。通过将 MiMo-Audio 的预训练数据扩展到超过一亿小时，我们观察到在多种音频任务上少样本学习能力的涌现。我们对这些能力进行了系统评测，发现 MiMo-Audio-7B-Base 在开源模型中于语音智能与音频理解基准测试上均取得了 SOTA 性能。在标准指标之外，MiMo-Audio-7B-Base 还能泛化到训练数据中不存在的任务，例如语音转换、风格迁移和语音编辑。MiMo-Audio-7B-Base 还展现出强大的语音续写能力，能够生成高度逼真的脱口秀、朗诵、直播和辩论。在后训练阶段，我们精选了多样化的指令微调语料，并将思考机制引入音频理解与生成。MiMo-Audio-7B-Instruct 在音频理解基准、语音对话基准和指令 TTS（instruct-TTS）评测上取得开源 SOTA，接近或超越闭源模型。


![结果](assets/Results.png)



## 架构
### MiMo-Audio-Tokenizer
MiMo-Audio-Tokenizer 是一个 1.2B 参数、以 25 Hz 运行的 Transformer。它采用八层 RVQ 堆栈，每秒生成 200 个 token。通过联合优化语义目标与重建目标，我们在 1000 万小时语料上从零训练 MiMo-Audio-Tokenizer，实现了卓越的重建质量并便利了下游语言建模。

![Tokenizer](assets/tokenizer.png)

MiMo-Audio 将 patch 编码器、LLM 与 patch 解码器耦合在一起，以提升高码率序列的建模效率，并弥合语音与文本之间的长度失配。patch 编码器将连续四个时间步的 RVQ token 聚合为单个 patch，把序列下采样到 6.25 Hz 的表示供 LLM 使用。patch 解码器通过延迟生成方案自回归地生成完整的 25 Hz RVQ token 序列。
### MiMo-Audio
![架构](assets/architecture.png)

##  立即体验 MiMo-Audio！🚀🚀🚀
- 🎧 **试用 Hugging Face 演示：** [MiMo-Audio Demo](https://huggingface.co/spaces/XiaomiMiMo/mimo_audio_chat)
- 📰 **阅读官方博客：** [MiMo-Audio 博客](https://xiaomimimo.github.io/MiMo-Audio-Demo)
- 📄 **深入技术报告：** [MiMo-Audio 技术报告](https://github.com/XiaomiMiMo/MiMo-Audio/blob/main/MiMo-Audio-Technical-Report.pdf)


## 模型下载
| 模型   | 🤗 Hugging Face |
|-------|-------|
| MiMo-Audio-Tokenizer | [XiaomiMiMo/MiMo-Audio-Tokenizer](https://huggingface.co/XiaomiMiMo/MiMo-Audio-Tokenizer) |
| MiMo-Audio-7B-Base | [XiaomiMiMo/MiMo-Audio-7B-Base](https://huggingface.co/XiaomiMiMo/MiMo-Audio-7B-Base) |
| MiMo-Audio-7B-Instruct | [XiaomiMiMo/MiMo-Audio-7B-Instruct](https://huggingface.co/XiaomiMiMo/MiMo-Audio-7B-Instruct) |


```bash
pip install huggingface-hub

hf download XiaomiMiMo/MiMo-Audio-Tokenizer --local-dir ./models/MiMo-Audio-Tokenizer
hf download XiaomiMiMo/MiMo-Audio-7B-Base --local-dir ./models/MiMo-Audio-7B-Base
hf download XiaomiMiMo/MiMo-Audio-7B-Instruct --local-dir ./models/MiMo-Audio-7B-Instruct
```

## 快速开始

用内置的 Gradio 应用，几分钟即可启动 MiMo-Audio 演示。

### 环境要求（Linux）

* Python 3.12
* CUDA >= 12.0

### 安装

```bash
git clone https://github.com/XiaomiMiMo/MiMo-Audio.git
cd MiMo-Audio
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
python run_mimo_audio.py
```

这会启动一个本地 Gradio 界面，你可以在其中交互式地试用 MiMo-Audio。

![演示界面](assets/demo_ui.jpg)

输入 `MiMo-Audio-Tokenizer` 和 `MiMo-Audio-7B-Instruct` 的本地路径，然后尽情体验 MiMo-Audio 的完整功能吧！

## 推理脚本

### 基座模型
我们提供示例脚本来探索 `MiMo-Audio-7B-Base` 的**上下文学习（in-context learning）**能力。
参见：[`inference_example_pretrain.py`](inference_example_pretrain.py)

### Instruct 模型
要试用经过指令微调的 `MiMo-Audio-7B-Instruct` 模型，请使用对应的推理脚本。
参见：[`inference_example_sft.py`](inference_example_sft.py)



## 评测工具包
完整评测套件见 🌐[MiMo-Audio-Eval](https://github.com/XiaomiMiMo/MiMo-Audio-Eval)。


该工具包用于评测 MiMo-Audio 及论文中提到的其他近期音频 LLM。它提供了一个灵活且可扩展的框架，支持广泛的数据库、任务和模型。

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

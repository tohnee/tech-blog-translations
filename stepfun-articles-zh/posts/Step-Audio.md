---
title: "Step-Audio：智能语音交互中理解与生成的统一"
title_en: "stepfun-ai/Step-Audio"
source: https://github.com/stepfun-ai/Step-Audio/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Step-Audio：智能语音交互中理解与生成的统一

> 原文：[stepfun-ai/Step-Audio](https://github.com/stepfun-ai/Step-Audio/blob/main/README.md) · 阶跃星辰 StepFun

<p align="left">
        <a href="README_CN.md">中文</a> &nbsp｜ &nbsp English&nbsp&nbsp ｜ &nbsp<a href="README_JP.md">日本語</a>
</p>
<br><br>

<img src="assets/QRCode.jpeg"  height=300>
开发者微信交流群、Developer Group

# 本仓库已停止维护，请参阅：
## [Step-Audio2&Step-Audio2-mini](https://github.com/stepfun-ai/Step-Audio2)（端到端语音对话）
## [Step-Audio-R1&Step-Audio-R1.1](https://github.com/stepfun-ai/Step-Audio-R1)（语音推理）
## [Step-Audio-EditX](https://github.com/stepfun-ai/Step-Audio-EditX)（音频编辑）

# Step-Audio
<p align="center">
  <img src="assets/logo.png"  height=100>
</p>
<div align="center">
  <a href="https://arxiv.org/abs/2502.11946"><img src="https://img.shields.io/static/v1?label=Tech Report&message=Arxiv&color=red"></a> &ensp;
  <a href="https://x.com/StepFun_ai"><img src="https://img.shields.io/static/v1?label=X.com&message=Web&color=blue"></a> &ensp;
</div>

<div align="center">
  <a href="https://huggingface.co/stepfun-ai/Step-Audio-Chat"><img src="https://img.shields.io/static/v1?label=Step-Audio-Chat&message=HuggingFace&color=yellow"></a> &ensp;
  <a href="https://huggingface.co/stepfun-ai/Step-Audio-TTS-3B"><img src="https://img.shields.io/static/v1?label=Step-Audio-TTS-3B&message=HuggingFace&color=yellow"></a> &ensp;
</div>
<div align="center">
  <a href="https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer"><img src="https://img.shields.io/static/v1?label=Step-Audio-Tokenier&message=HuggingFace&color=yellow"></a> &ensp;
  <a href="https://huggingface.co/datasets/stepfun-ai/StepEval-Audio-360"><img src="https://img.shields.io/static/v1?label=StepEval-Audio-360&message=HuggingFace&color=yellow"></a> &ensp;
</div>

## 🔥🔥🔥 新闻！
* 2025 年 8 月 29 日：👋 我们发布了 [Step-Audio 2 与 Step-Audio 2 mini](https://github.com/stepfun-ai/Step-Audio2) 及其对应的推理[示例](examples.py)。[技术报告](https://arxiv.org/pdf/2507.16632)也已更新。
* 2025 年 6 月 10 日：👋 我们发布了 [Step-Audio-AQAA](https://arxiv.org/abs/2506.08967) 的技术报告。
* 2025 年 2 月 17 日：👋 我们发布了 [Step-Audio-Chat](https://huggingface.co/stepfun-ai/Step-Audio-Chat)、[Step-Audio-TTS-3B](https://huggingface.co/stepfun-ai/Step-Audio-TTS-3B) 与 [Step-Audio-Tokenizer](https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer) 的推理代码与模型权重
* 2025 年 2 月 17 日：👋 我们发布了 [StepEval-Audio-360](https://huggingface.co/datasets/stepfun-ai/StepEval-Audio-360) 多轮语音基准。
* 2025 年 2 月 17 日：👋 我们发布了 [Step-Audio](https://arxiv.org/abs/2502.11946) 的技术报告。

## 目录

1. [简介](#1-简介)
2. [模型概览](#2-模型概览)
3. [模型下载](#3-模型下载)
4. [模型使用](#4-模型使用)
5. [基准测试](#5-基准测试)
6. [在线引擎](#6-在线引擎)
7. [示例](#7-示例)
8. [致谢](#8-致谢)
9. [许可协议](#9-许可协议)
10. [引用](#10-引用)

## 1. 简介

Step-Audio 是首个可投入生产的开源智能语音交互框架，统一了理解与生成，支持多语言对话（如中文、英文、日语）、情感语调（如喜悦/悲伤）、地方方言（如粤语/四川话）、可调语速以及韵律风格（如说唱）。Step-Audio 展示了四项关键技术创新：

- **1300 亿参数多模态模型**：单一统一模型集成理解与生成能力，可执行语音识别、语义理解、对话、语音克隆与语音合成。我们已开源 130B 的 Step-Audio-Chat 变体。

- **生成式数据引擎**：通过 1300 亿参数多模态模型生成高质量音频，消除了传统 TTS 对人工数据采集的依赖。并利用这些数据训练并公开发布了资源高效的 Step-Audio-TTS-3B 模型，其指令遵循能力得到增强，可实现可控语音合成。

- **细粒度声音控制**：通过基于指令的控制设计实现精确调控，支持多种情绪（愤怒、喜悦、悲伤）、方言（粤语、四川话等）与声音风格（说唱、无伴奏哼唱），满足多样的语音生成需求。

- **增强的智能水平**：通过集成 ToolCall 机制与角色扮演增强，提升智能体在复杂任务中的表现。

## 2. 模型概览
在 Step-Audio 中，音频流通过双码本框架分词：并行使用语义（16.7Hz，1024 条目码本）与声学（25Hz，4096 条目码本）分词器，并按 2:3 时间交错。一个 1300 亿参数的 LLM 底座（Step-1）经音频语境化持续预训练与任务专属后训练进一步增强，实现稳健的跨模态语音理解。混合语音解码器将流匹配与神经声码器相结合，针对实时波形生成优化。流式感知架构具备投机式响应生成（40% 提交率）与基于文本的上下文管理（14:1 压缩比），实现高效的跨模态对齐。
![架构](assets/architecture.png)

### 2.1 分词器（Tokenizer）

我们实现了 token 级交错方法，以有效整合语义分词与声学分词。语义分词器采用 1024 的码本大小，而声学分词器使用更大的 4096 码本以捕获更细的声学细节。鉴于两者 token 速率不同，我们建立了 2:3 的时间对齐比例，即每两个语义 token 配对三个声学 token。

### 2.2 语言模型

为增强 Step-Audio 有效处理语音信息并实现精准语音-文本对齐的能力，我们基于 Step-1——一个 1300 亿参数的预训练文本大语言模型（LLM）——进行了音频持续预训练。

### 2.3 语音解码器
Step-Audio 中的语音解码器承担着关键功能：将同时包含语义与声学信息的离散语音 token 转换为表示自然语音的连续时域波形。解码器架构包含一个流匹配模型与一个 mel-to-wave 声码器。为优化合成语音的可懂度与自然度，语音解码器使用双码交错方法训练，确保语义与声学特征在生成全过程无缝融合。

### 2.4 实时推理流水线
为实现实时交互，我们设计了优化的推理流水线。其核心的 Controller 模块管理状态转换、编排投机式响应生成，并确保各关键子系统之间无缝协调。这些子系统包括：用于检测用户语音的语音活动检测（VAD）、用于实时处理音频的流式音频分词器、用于处理与生成响应的 Step-Audio 语言模型与语音解码器，以及用于保持对话连续性的上下文管理器。
![推理流水线](assets/pipeline.png)

### 2.5 后训练细节
在后训练阶段，我们针对自动语音识别（ASR）与文本转语音（TTS）进行了任务专属的监督微调（SFT）。对于音频输入文本输出（AQTA）任务，我们使用多样化高质量数据集进行 SFT，并结合基于人类反馈的强化学习（RLHF）以提升回复质量，实现对情绪表达、语速、方言与韵律的细粒度控制。
![RLHF](assets/rlhf.png)


## 3. 模型下载
### 3.1 Huggingface
| 模型   | 链接   |
|-------|-------|
| Step-Audio-Tokenizer | [🤗huggingface](https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer) |
| Step-Audio-Chat | [🤗huggingface](https://huggingface.co/stepfun-ai/Step-Audio-Chat) |
| Step-Audio-TTS-3B | [🤗huggingface](https://huggingface.co/stepfun-ai/Step-Audio-TTS-3B) |

### 3.2 Modelscope
| 模型   | 链接   |
|-------|-------|
| Step-Audio-Tokenizer | [modelscope](https://modelscope.cn/models/stepfun-ai/Step-Audio-Tokenizer) |
| Step-Audio-Chat | [modelscope](https://modelscope.cn/models/stepfun-ai/Step-Audio-Chat) |
| Step-Audio-TTS-3B | [modelscope](https://modelscope.cn/models/stepfun-ai/Step-Audio-TTS-3B) |

## 4. 模型使用
### 📜 4.1  环境要求
下表展示了运行 Step-Audio 模型（batch size = 1）的要求：

|     模型    |  设定<br/>(采样频率) | GPU 最低显存  |
|------------|--------------------------------|----------------|
| Step-Audio-Tokenizer   |        41.6Hz          |       1.5GB        |
| Step-Audio-Chat   |        41.6Hz          |       265GB        |
| Step-Audio-TTS-3B   |        41.6Hz          |       8GB        |

* 需要 NVIDIA GPU 且支持 CUDA。
  * 模型已在四张 A800 80G GPU 上测试。
  * **推荐**：我们推荐使用 4xA800/H800（80GB 显存）GPU 以获得更好的生成质量。
* 已测试操作系统：Linux

### 🔧 4.2 依赖与安装
- Python >= 3.10.0（推荐使用 [Anaconda](https://www.anaconda.com/download/#linux) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)）
- [PyTorch >= 2.3-cu121](https://pytorch.org/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)

```bash
git clone https://github.com/stepfun-ai/Step-Audio.git
conda create -n stepaudio python=3.10
conda activate stepaudio

cd Step-Audio
pip install -r requirements.txt

git lfs install
git clone https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer
git clone https://huggingface.co/stepfun-ai/Step-Audio-Chat
git clone https://huggingface.co/stepfun-ai/Step-Audio-TTS-3B

```

下载模型后，where_you_download_dir 应具有如下结构：
```
where_you_download_dir
├── Step-Audio-Tokenizer
├── Step-Audio-Chat
├── Step-Audio-TTS-3B
```

#### 使用 Docker 运行

你可以使用提供的 Dockerfile 搭建运行 Step-Audio 所需的环境。

```bash
# build docker
docker build . -t step-audio

# run docker
docker run --rm -ti --gpus all \
    -v /your/code/path:/app -v /your/model/path:/model \
    -p 7860:7860 \
    step-audio \
    -- bash

# build vLLM docker
docker build -f Dockerfile-vllm -t step-audio-vllm .

# run vLLM docker
docker run --rm -ti --gpus all \
    -v /your/code/path:/app -v /your/model/path:/model \
    -p 7860:7860 \
    -p 8000:8000 \
    step-audio-vllm \
    -- bash
```


###  🚀 4.3 推理脚本
#### 离线推理
以端到端音频/文本输入、音频/文本输出进行推理。
```bash
python offline_inference.py --model-path where_you_download_dir
```
#### TTS 推理
使用默认说话人推理 TTS，或用新说话人克隆
```bash
python tts_inference.py --model-path where_you_download_dir --output-path where_you_save_audio_dir --synthesis-type use_tts_or_clone
```
克隆模式需要一个说话人信息字典，格式如下：
```bash
{
    "speaker": "speaker id",
    "prompt_text": "content of prompt wav",
    "wav_path": "prompt wav path"
}
```

#### 启动 Web 演示
启动本地服务器进行在线推理。
假设你有 4 张 GPU 且已下载全部模型。

```bash
# Step-Audio-Chat demo
python app.py --model-path where_you_download_dir

# Step-Audio-TTS-3B demo
python tts_app.py --model-path where_you_download_dir
```

#### 使用 vLLM 推理 Chat 模型（推荐）
Step-Audio-Chat 是一个 130B 的 LLM 模型，推荐使用 vLLM 以张量并行推理。
    * 由于 vLLM 不加载 Tokenizer 与 TTS，该模型不支持音频输入推理。

目前官方 vLLM 尚不支持 Step 1 模型。你可以暂时使用我们的[开发分支](https://github.com/stepfun-ai/vllm/tree/add-step1-model)进行本地安装。

**由于我们的注意力机制是 ALIBI 的变体，官方 flash attention 库不兼容。我们已在 [Step-Audio-Chat](https://huggingface.co/stepfun-ai/Step-Audio-Chat/tree/main/lib) 仓库中提供了自定义 flash attention 库。运行模型前，请确保将自定义 flash attention 库导出到环境变量。**

```bash
export OPTIMUS_LIB_PATH=where_you_download_dir/Step-Audio-Chat/lib

vllm serve where_you_download_dir/Step-Audio-Chat --dtype auto -tp $tp --served-model-name step-audio-chat --trust-remote-code

# vLLM chat example code
python call_vllm_chat.py
```

## 5. 基准测试

### 5.1 ASR 结果对比

<table>
    <thead>
        <tr>
            <th style="text-align:center"></th>
            <th colspan="4" style="text-align:center">隐藏特征建模</th>
            <th colspan="5" style="text-align:center">离散音频 token 建模</th>
        </tr>
        <tr>
            <th style="text-align:center"></th>
            <th style="text-align:center">Whisper Large-v3</th>
            <th style="text-align:center">Qwen2-Audio</th>
            <th style="text-align:center">MinMo</th>
            <th style="text-align:center">LUCY</th>
            <th style="text-align:center">Moshi</th>
            <th style="text-align:center">GLM-4-voice Base</th>
            <th style="text-align:center">GLM-4-voice Chat</th>
            <th style="text-align:center">Step-Audio Pretrain</th>
            <th style="text-align:center">Step-Audio-Chat</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Aishell-1</td>
            <td style="text-align:center">5.14</td>
            <td style="text-align:center">1.53</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">2.4</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">2.46</td>
            <td style="text-align:center">226.47</td>
            <td style="text-align:center"><strong>0.87</strong></td>
            <td style="text-align:center">1.95</td>
        </tr>
        <tr>
            <td>Aishell-2 ios</td>
            <td style="text-align:center">4.76</td>
            <td style="text-align:center">3.06</td>
            <td style="text-align:center"><strong>2.69</strong></td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">211.3</td>
            <td style="text-align:center">2.91</td>
            <td style="text-align:center">3.57</td>
        </tr>
        <tr>
            <td>Wenetspeech test-net</td>
            <td style="text-align:center">9.68</td>
            <td style="text-align:center">7.72</td>
            <td style="text-align:center"><strong>6.64</strong></td>
            <td style="text-align:center">8.78</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">146.05</td>
            <td style="text-align:center">7.62</td>
            <td style="text-align:center">8.75</td>
        </tr>
        <tr>
            <td>Wenet test-meeting</td>
            <td style="text-align:center">18.54</td>
            <td style="text-align:center">8.4</td>
            <td style="text-align:center"><strong>7.6</strong></td>
            <td style="text-align:center">10.42</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">140.82</td>
            <td style="text-align:center">7.78</td>
            <td style="text-align:center">9.52</td>
        </tr>
        <tr>
            <td>Librispeech test-clean</td>
            <td style="text-align:center">1.9</td>
            <td style="text-align:center"><strong>1.6</strong></td>
            <td style="text-align:center"><strong>1.6</strong></td>
            <td style="text-align:center">3.36</td>
            <td style="text-align:center">5.7</td>
            <td style="text-align:center">2.82</td>
            <td style="text-align:center">75.39</td>
            <td style="text-align:center">2.36</td>
            <td style="text-align:center">3.11</td>
        </tr>
        <tr>
            <td>Librispeech test-other</td>
            <td style="text-align:center">3.65</td>
            <td style="text-align:center"><strong>3.6</strong></td>
            <td style="text-align:center">3.82</td>
            <td style="text-align:center">8.05</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">7.66</td>
            <td style="text-align:center">80.3</td>
            <td style="text-align:center">6.32</td>
            <td style="text-align:center">8.44</td>
        </tr>
        <tr>
            <td>AVG</td>
            <td style="text-align:center">7.28</td>
            <td style="text-align:center"><strong>4.32</strong></td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">146.74</td>
            <td style="text-align:center">4.64</td>
            <td style="text-align:center">5.89</td>
        </tr>
    </tbody>
</table>

### 5.2 TTS
#### 5.2.1 与 GLM-4-Voice、MinMo 的内容一致性（CER/WER）性能对比。

<table>
    <thead>
        <tr>
            <th rowspan="2">模型</th>
            <th style="text-align:center" colspan="1">test-zh</th>
            <th style="text-align:center" colspan="1">test-en</th>
        </tr>
        <tr>
            <th style="text-align:center">CER (%) &darr;</th>
            <th style="text-align:center">WER (%) &darr;</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>GLM-4-Voice</td>
            <td style="text-align:center">2.19</td>
            <td style="text-align:center">2.91</td>
        </tr>
        <tr>
            <td>MinMo</td>
            <td style="text-align:center">2.48</td>
            <td style="text-align:center">2.90</td>
        </tr>
        <tr>
            <td><strong>Step-Audio</strong></td>
            <td style="text-align:center"><strong>1.53</strong></td>
            <td style="text-align:center"><strong>2.71</strong></td>
        </tr>
    </tbody>
</table>

#### 5.2.2 TTS 模型在 SEED 测试集上的结果。
* StepAudio-TTS-3B-Single 表示采用双码本骨干 + 单码本声码器*

<table>
    <thead>
        <tr>
            <th rowspan="2">模型</th>
            <th style="text-align:center" colspan="2">test-zh</th>
            <th style="text-align:center" colspan="2">test-en</th>
        </tr>
        <tr>
            <th style="text-align:center">CER (%) &darr;</th>
            <th style="text-align:center">SS &uarr;</th>
            <th style="text-align:center">WER (%) &darr;</th>
            <th style="text-align:center">SS &uarr;</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>FireRedTTS</td>
            <td style="text-align:center">1.51</td>
            <td style="text-align:center">0.630</td>
            <td style="text-align:center">3.82</td>
            <td style="text-align:center">0.460</td>
        </tr>
        <tr>
            <td>MaskGCT</td>
            <td style="text-align:center">2.27</td>
            <td style="text-align:center">0.774</td>
            <td style="text-align:center">2.62</td>
            <td style="text-align:center">0.774</td>
        </tr>
        <tr>
            <td>CosyVoice</td>
            <td style="text-align:center">3.63</td>
            <td style="text-align:center">0.775</td>
            <td style="text-align:center">4.29</td>
            <td style="text-align:center">0.699</td>
        </tr>
        <tr>
            <td>CosyVoice 2</td>
            <td style="text-align:center">1.45</td>
            <td style="text-align:center">0.806</td>
            <td style="text-align:center">2.57</td>
            <td style="text-align:center">0.736</td>
        </tr>
        <tr>
            <td>CosyVoice 2-S</td>
            <td style="text-align:center">1.45</td>
            <td style="text-align:center">0.812</td>
            <td style="text-align:center">2.38</td>
            <td style="text-align:center">0.743</td>
        </tr>
        <tr>
            <td><strong>Step-Audio-TTS-3B-Single</strong></td>
            <td style="text-align:center">1.37</td>
            <td style="text-align:center">0.802</td>
            <td style="text-align:center">2.52</td>
            <td style="text-align:center">0.704</td>
        </tr>
        <tr>
            <td><strong>Step-Audio-TTS-3B</strong></td>
            <td style="text-align:center"><strong>1.31</strong></td>
            <td style="text-align:center">0.733</td>
            <td style="text-align:center"><strong>2.31</strong></td>
            <td style="text-align:center">0.660</td>
        </tr>
        <tr>
            <td><strong>Step-Audio-TTS</strong></td>
            <td style="text-align:center"><strong>1.17</strong></td>
            <td style="text-align:center">0.73</td>
            <td style="text-align:center"><strong>2.0</strong></td>
            <td style="text-align:center">0.660</td>
        </tr>
    </tbody>
</table>

#### 5.2.3 双码本重合成与 Cosyvoice 的性能对比。

<table>
    <thead>
        <tr>
            <th style="text-align:center" rowspan="2">Token</th>
            <th style="text-align:center" colspan="2">test-zh</th>
            <th style="text-align:center" colspan="2">test-en</th>
        </tr>
        <tr>
            <th style="text-align:center">CER (%) &darr;</th>
            <th style="text-align:center">SS &uarr;</th>
            <th style="text-align:center">WER (%) &darr;</th>
            <th style="text-align:center">SS &uarr;</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align:center">Groundtruth</td>
            <td style="text-align:center">0.972</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">2.156</td>
            <td style="text-align:center">-</td>
        </tr>
        <tr>
            <td style="text-align:center">CosyVoice</td>
            <td style="text-align:center">2.857</td>
            <td style="text-align:center"><strong>0.849</strong></td>
            <td style="text-align:center">4.519</td>
            <td style="text-align:center"><strong>0.807</strong></td>
        </tr>
        <tr>
            <td style="text-align:center">Step-Audio-TTS-3B</td>
            <td style="text-align:center"><strong>2.192</strong></td>
            <td style="text-align:center">0.784</td>
            <td style="text-align:center"><strong>3.585</strong></td>
            <td style="text-align:center">0.742</td>
        </tr>
    </tbody>
</table>

### 5.3 AQTA 对话
我们发布 [**StepEval-Audio-360**](https://huggingface.co/datasets/stepfun-ai/StepEval-Audio-360) 作为新基准，它由 137 条来自真实用户的多轮中文提示词组成，用于从以下维度评估生成回复的质量：语音指令遵循、语音理解、逻辑推理、角色扮演、创造力、歌唱、语言能力、语音情绪控制、游戏。

#### 5.3.1 StepEval-Audio-360

#### LLM 裁判指标（GPT-4o）
<table>
    <caption>语音对话基础能力在 StepEval-Audio-360 上的对比。</caption>
    <thead>
        <tr>
            <th>模型</th>
            <th style="text-align:center">事实性 (% &uarr;)</th>
            <th style="text-align:center">相关性 (% &uarr;)</th>
            <th style="text-align:center">对话分数 &uarr;</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>GLM4-Voice</td>
            <td style="text-align:center">54.7</td>
            <td style="text-align:center">66.4</td>
            <td style="text-align:center">3.49</td>
        </tr>
        <tr>
            <td>Qwen2-Audio</td>
            <td style="text-align:center">22.6</td>
            <td style="text-align:center">26.3</td>
            <td style="text-align:center">2.27</td>
        </tr>
        <tr>
            <td>Moshi<sup>*</sup></td>
            <td style="text-align:center">1.0</td>
            <td style="text-align:center">0</td>
            <td style="text-align:center">1.49</td>
        </tr>
        <tr>
            <td><strong>Step-Audio-Chat</strong></td>
            <td style="text-align:center"><strong>66.4</strong></td>
            <td style="text-align:center"><strong>75.2</strong></td>
            <td style="text-align:center"><strong>4.11</strong></td>
        </tr>
    </tbody>
</table>

* 注：Moshi 标有 "\*"，仅供参考。

#### 雷达图（人工评测）
<img src="./assets/stepeval_radar_chart.png" width="600" alt="QR code">

#### 5.3.2 公开测试集

<table>
    <thead>
        <tr>
            <th>模型</th>
            <th style="text-align:center">Llama Question</th>
            <th style="text-align:center">Web Questions</th>
            <th style="text-align:center">TriviaQA*</th>
            <th style="text-align:center">ComplexBench</th>
            <th style="text-align:center">HSK-6</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>GLM4-Voice</td>
            <td style="text-align:center">64.7</td>
            <td style="text-align:center">32.2</td>
            <td style="text-align:center">39.1</td>
            <td style="text-align:center">66.0</td>
            <td style="text-align:center">74.0</td>
        </tr>
        <tr>
            <td>Moshi</td>
            <td style="text-align:center">62.3</td>
            <td style="text-align:center">26.6</td>
            <td style="text-align:center">22.8</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
        </tr>
        <tr>
            <td>Freeze-Omni</td>
            <td style="text-align:center">72.0</td>
            <td style="text-align:center">44.7</td>
            <td style="text-align:center">53.9</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
        </tr>
        <tr>
            <td>LUCY</td>
            <td style="text-align:center">59.7</td>
            <td style="text-align:center">29.3</td>
            <td style="text-align:center">27.0</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
        </tr>
        <tr>
            <td>MinMo</td>
            <td style="text-align:center">78.9</td>
            <td style="text-align:center">55.0</td>
            <td style="text-align:center">48.3</td>
            <td style="text-align:center">-</td>
            <td style="text-align:center">-</td>
        </tr>
        <tr>
            <td>Qwen2-Audio</td>
            <td style="text-align:center">52.0</td>
            <td style="text-align:center">27.0</td>
            <td style="text-align:center">37.3</td>
            <td style="text-align:center">54.0</td>
            <td style="text-align:center">-</td>
        </tr>
        <tr>
            <td><strong>Step-Audio-Chat</strong></td>
            <td style="text-align:center"><strong><i>81.0</i></strong></td>
            <td style="text-align:center"><strong>75.1</strong></td>
            <td style="text-align:center"><strong>58.0</strong></td>
            <td style="text-align:center"><strong>74.0</strong></td>
            <td style="text-align:center"><strong>86.0</strong></td>
        </tr>
    </tbody>
</table>

* 注：TriviaQA 数据集上标有 "\*" 的结果仅供参考。*

#### 5.3.3 音频指令遵循
<table>
    <thead>
        <tr>
            <th rowspan="2">类别</th>
            <th colspan="2" style="text-align:center">指令遵循</th>
            <th colspan="2" style="text-align:center">音频质量</th>
        </tr>
        <tr>
            <th style="text-align:center">GLM-4-Voice</th>
            <th style="text-align:center">Step-Audio</th>
            <th style="text-align:center">GLM-4-Voice</th>
            <th style="text-align:center">Step-Audio</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>语言</td>
            <td style="text-align:center">1.9</td>
            <td style="text-align:center">3.8</td>
            <td style="text-align:center">2.9</td>
            <td style="text-align:center">3.3</td>
        </tr>
        <tr>
            <td>角色扮演</td>
            <td style="text-align:center">3.8</td>
            <td style="text-align:center">4.2</td>
            <td style="text-align:center">3.2</td>
            <td style="text-align:center">3.6</td>
        </tr>
        <tr>
            <td>歌唱 / RAP</td>
            <td style="text-align:center">2.1</td>
            <td style="text-align:center">2.4</td>
            <td style="text-align:center">2.4</td>
            <td style="text-align:center">4</td>
        </tr>
        <tr>
            <td>声音控制</td>
            <td style="text-align:center">3.6</td>
            <td style="text-align:center">4.4</td>
            <td style="text-align:center">3.3</td>
            <td style="text-align:center">4.1</td>
        </tr>
    </tbody>
</table>

## 6. 在线引擎
Step-Audio 的在线版本可在 [跃问](https://yuewen.cn) App 中访问，那里也可以找到一些令人惊艳的示例。

<img src="./assets/yuewen.jpeg" width="200" alt="QR code">

## 7. 示例
### 克隆音频
| 角色   | 提示音频 | 克隆音频 |
|:-------:|:-------:|:-------:|
|于谦| [google drive](https://drive.google.com/file/d/1N9EJypafFwmeL0R152GoL_CVGbYn1_9A/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/prompt_wav_yuqian.wav)|[google drive](https://drive.google.com/file/d/1Zs_1QrCUuoSqtUSdn2ENIor-k5baQdDV/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/clone_wav_yuqian.wav)|
|李雪琴| [google drive](https://drive.google.com/file/d/15SkZ29hksELYi1NDOxYOPu-kRTLSyke_/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/prompt_wav_lixueqin.wav)|[google drive](https://drive.google.com/file/d/11Le4qMqL2DmWpf7RFRpKUXERIR9TtKC0/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/clone_wav_lixueqin.wav)|

### 语速控制
| 提示 | 回复 |
|:-------:|:-------:|
|Human: 说一个绕口令<br>Assistant: 吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮<br>Human: 哎，你能把这个绕口令说的再快一点吗？|[google drive](https://drive.google.com/file/d/1mAH-NRrOVZo4tv6gdAZkyJg8kRuTNNGC/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/speed_control1.wav)|
|Human: 说一个绕口令<br>Assistant: 吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮<br>Human: 哎，你能把这个绕口令说的再快一点吗？<br>Assistant: 吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮<br>Human: 呃，你再用非常非常慢的速度说一遍的。|[google drive](https://drive.google.com/file/d/1FhRnKo8uGrtO-cWg4qkrg8iDoNRbtqSX/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/speed_control2.wav)|

### 高情商（情绪控制与语气控制）
| 提示 | 回复 |
|:-------:|:-------:|
|Human: 你这语气又不撒娇又不卖萌的，要不你撒个娇卖个萌吧。|[google drive](https://drive.google.com/file/d/19IROE6_6h2UQVNniCmDTnrhxKRMOFHq3/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/tone_control.wav)|
|Human: 怎么办？我感觉我的人生很失败。|[google drive](https://drive.google.com/file/d/1JlLbOlzmdrokVdxtwy1S8eeWqsZR2Vmc/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/emotional_control1.wav)|
|Human: 小跃。你真的是。特别厉害。|[google drive](https://drive.google.com/file/d/19ga1RpguDP5r0Xfl1r5GY1J-kzbmHvJb/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/emotional_control2.wav)|

### 多语言（如中文、英文、日语）
| 提示 | 回复 |
|:-------:|:-------:|
|Human: What did the speaker mean when they said, it's raining cats and dogs?<br>Assistant: When they say "It's raining cats and dogs," it just means it's raining really hard. The speaker isn't literally saying cats and dogs are falling from the sky! It's just a fun way to describe heavy rain.|[google drive](https://drive.google.com/file/d/1LEIvdR5ANMzWX8GOTqUPTNrynNS1xx--/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/multilingual2.wav)|
|Human: こんにちは。（你好）<br>Assistant：こんにちは！何か手伝いましょうか？（您好！我可以帮你做点什么吗？）|[google drive](https://drive.google.com/file/d/1MjKUkkzcGzVcNVXRr_Ya5y2H44K_lybH/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/multilingual1.wav)|

### 说唱与人声
| 提示 | 回复 |
|:-------:|:-------:|
|Human: 唱一段rap|[google drive](https://drive.google.com/file/d/1F8CKmVbGZ7X7d1IkQPlmndSHeG40AXha/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/rap.wav)|
|Human: 唱一段中文的歌曲（Sing Chinese Song）|[google drive](https://drive.google.com/file/d/1F1o-Q90llmkM-4UU6qhP8KoHp3dhaluj/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/singing.wav)|
|Human: 唱一段日语的歌曲（Sing Japanese Song）|[google drive](https://drive.google.com/file/d/1kS2jQEq70ynh46pG_P5Xp1_NY3C-cJ-U/preview)<br>[audio file](https://github.com/stepfun-ai/Step-Audio/tree/main/examples/multilingual_singing.wav)|

## 8. 致谢

本项目的部分代码来自：
* [CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
* [transformers](https://github.com/huggingface/transformers)
* [FunASR](https://github.com/modelscope/FunASR)

感谢所有开源项目对本项目的贡献！
## 9. 许可协议

+ 使用 Step Audio 相关模型的权重需遵循 [Step-Audio-Chat](https://huggingface.co/stepfun-ai/Step-Audio-Chat/tree/main)、[Step-Audio-Tokenizer](https://huggingface.co/stepfun-ai/Step-Audio-Tokenizer/tree/main) 与 [Step-Audio-TTS-3B](https://huggingface.co/stepfun-ai/Step-Audio-TTS-3B/tree/main) 中的许可证

+ 本开源仓库中的代码基于 [Apache 2.0](LICENSE) 许可证授权。

## 10. 引用
```
@misc{huang2025stepaudiounifiedunderstandinggeneration,
      title={Step-Audio: Unified Understanding and Generation in Intelligent Speech Interaction},
      author={Ailin Huang and Boyong Wu and Bruce Wang and Chao Yan and Chen Hu and Chengli Feng and Fei Tian and Feiyu Shen and Jingbei Li and Mingrui Chen and Peng Liu and Ruihang Miao and Wang You and Xi Chen and Xuerui Yang and Yechang Huang and Yuxiang Zhang and Zheng Gong and Zixin Zhang and Brian Li and Changyi Wan and Hanpeng Hu and Ranchen Ming and Song Yuan and Xuelin Zhang and Yu Zhou and Bingxin Li and Buyun Ma and Kang An and Wei Ji and Wen Li and Xuan Wen and Yuankai Ma and Yuanwei Liang and Yun Mou and Bahtiyar Ahmidi and Bin Wang and Bo Li and Changxin Miao and Chen Xu and Chengting Feng and Chenrun Wang and Dapeng Shi and Deshan Sun and Dingyuan Hu and Dula Sai and Enle Liu and Guanzhe Huang and Gulin Yan and Heng Wang and Haonan Jia and Haoyang Zhang and Jiahao Gong and Jianchang Wu and Jiahong Liu and Jianjian Sun and Jiangjie Zhen and Jie Feng and Jie Wu and Jiaoren Wu and Jie Yang and Jinguo Wang and Jingyang Zhang and Junzhe Lin and Kaixiang Li and Lei Xia and Li Zhou and Longlong Gu and Mei Chen and Menglin Wu and Ming Li and Mingxiao Li and Mingyao Liang and Na Wang and Nie Hao and Qiling Wu and Qinyuan Tan and Shaoliang Pang and Shiliang Yang and Shuli Gao and Siqi Liu and Sitong Liu and Tiancheng Cao and Tianyu Wang and Wenjin Deng and Wenqing He and Wen Sun and Xin Han and Xiaomin Deng and Xiaojia Liu and Xu Zhao and Yanan Wei and Yanbo Yu and Yang Cao and Yangguang Li and Yangzhen Ma and Yanming Xu and Yaqiang Shi and Yilei Wang and Yinmin Zhong and Yu Luo and Yuanwei Lu and Yuhe Yin and Yuting Yan and Yuxiang Yang and Zhe Xie and Zheng Ge and Zheng Sun and Zhewei Huang and Zhichao Chang and Zidong Yang and Zili Zhang and Binxing Jiao and Daxin Jiang and Heung-Yeung Shum and Jiansheng Chen and Jing Li and Shuchang Zhou and Xiangyu Zhang and Xinhao Zhang and Yibo Zhu},
      year={2025},
      eprint={2502.11946},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.11946},
}
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=stepfun-ai/Step-Audio&type=Date)](https://star-history.com/#stepfun-ai/Step-Audio&Date)

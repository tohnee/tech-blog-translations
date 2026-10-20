---
title: "inclusionAI/Ming-3.0-tts"
title_en: "inclusionAI/Ming-3.0-tts"
source: https://github.com/inclusionAI/Ming-3.0-tts/blob/main/README.md
crawled: 2026-10-20
translated: 2026-10-20
---

<h1 align="center">
  <img src="./figures/ant-bailing.png" width="60" alt="Ming-3.0-tts Logo" align="middle" />
  Ming-3.0-tts
</h1>

<p align="center">支持自由格式与副语言控制的多语言语音合成。</p>

<p align="center">🤗 <a href="https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5b">Hugging Face</a>｜ 🤖 <a href="https://modelscope.cn/models/inclusionAI/Ming-3.0-tts-0.5b">ModelScope</a> ｜ 📑 <a href="https://nomorecoding.github.io/Ming-3.0-tts/">博客与演示</a> ｜ 💬 <a href="https://qr.dingtalk.com/action/joingroup?code=v1,k1,O7MiZqrOrB2c7PnUZVBNvmDh/6tghNLMEtXqMteyRIpuRVJIwrSsXmL8oFqU5ajJ&_dt_no_comment=1&origin=11">DingTalk(钉钉)</a></p>

Ming-3.0-tts 提供两个语音生成模型：**0.5b**，一个稠密模型；以及 **tiny**，一个基于 Ling V3 构建的 MoE 模型（总参数 7.9B · 激活 1.3B）。

## <a id="artificial-analysis-leaderboards"></a>🏆 Artificial Analysis 排行榜

在独立的 [Artificial Analysis](https://artificialanalysis.ai/text-to-speech) 文本转语音排行榜（2026 年 10 月）上，Ming-3.0-tts 在 Controlled Voice（受控音色）上**位列开放权重模型第 1**，在 Pronunciation Robustness（发音鲁棒性）上**总排名第 1**，在 Provider Voice（厂商音色）上**位列开放权重模型第 3**。随着新模型加入，排名会发生变化。

| 排行榜 | 设置 | Ming-3.0-tts | 排名 |
| --- | --- | :---: | --- |
| [Controlled Voice](https://artificialanalysis.ai/text-to-speech/leaderboard/controlled-voice) | 竞技场偏好 Elo；每个模型克隆同样的 8 个音色（4 个美式、4 个英式） | 1069 | **开放权重第 1** · 总第 13 |
| [Pronunciation Robustness](https://artificialanalysis.ai/text-to-speech) | 英文文本中被人工评审判定发音正确的高亮片段占比 | 93.2% | **总排名第 1** |
| [Provider Voice](https://artificialanalysis.ai/text-to-speech/leaderboard/provider-voice) | 竞技场偏好 Elo；每个模型使用其自有原生音色 | 1188 | **开放权重第 3** · 总第 17 |

<p align="center">
    <img src="./figures/aa_leaderboards.png" width="900" alt="Artificial Analysis leaderboards: Controlled Voice and Provider Voice (open weights), Pronunciation Robustness"/>
</p>

在 Pronunciation Robustness 内部，Ming-3.0-tts 还在 Expanding Shorthand（缩写展开，文本正则化，96.5%）与 Preserving Exact Sequences（精确序列保持，序列保真，90.6%）上排名**第 1**。

## 核心能力

- **声音创建：**克隆参考音色、从文本设计音色，或从 100 多个中文与 5 个英文内置音色中选择。
- **自由格式控制：**用自然语言指令引导语音的表达方式。
- **副语言控制：**在中文或英文文本中插入 14 种行内标签，表达笑声、叹息及其他发声。
- **语言与方言：**合成中文、英文、德语、西班牙语、法语、韩语和日语，另有四川话与粤语。
- **情感与属性：**控制情感，或调节语速、音高与音量。
- **多人对话：**根据脚本与说话人参考生成对话（**仅 tiny**）。

各项能力使用彼此独立的任务模式，而非任意组合。支持的输入参见 [Cookbook](#cookbook)，基准结果参见[性能](#performance)，音频示例参见[博客与演示](https://nomorecoding.github.io/Ming-3.0-tts/)。

## <a id="demo-video"></a>演示视频

https://github.com/user-attachments/assets/4062ba4c-7d2d-4a45-a19b-760100b79f9c

## 架构

文本与任务专属的控制 token 共同作为条件，驱动一个带有 DiT patch 头与音频 tokenizer 的语言模型。两个模型共享这一生成框架。

<p align="center">
    <img src="./figures/ming-3.0-tts.png" width="760"/>
</p>

## 动态

- 🔥 **[2026.10]** Ming-3.0-tts-0.5b 与 Ming-3.0-tts-tiny 发布，附带推理代码、任务 Cookbook 与下方的评测表格。

## 路线图

- [x] Ming-3.0-tts-0.5b 权重与推理代码
- [x] Ming-3.0-tts-tiny 权重与推理代码
- [x] Ming-3.0-tts-tiny 基准
- [x] vLLM-Omni 加速推理
- [ ] 技术报告

## 目录

- [演示视频](#demo-video)
- [模型](#models)
- [快速开始](#quick-start-)
- [Cookbook](#cookbook)
- [内置音色](#built-in-voices)
- [性能](#performance)
- [局限性](#limitations)
- [使用免责声明](#usage-disclaimer)

## <a id="models"></a>模型

<div align="center">
<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr>
      <th style="padding: 8px 20px; border: none; border-bottom: 1px solid black;">模型</th>
      <th style="padding: 8px 20px; border: none; border-bottom: 1px solid black;">架构</th>
      <th style="padding: 8px 20px; border: none; border-bottom: 1px solid black;">参数量</th>
      <th style="padding: 8px 20px; border: none; border-bottom: 1px solid black;">下载</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center" style="padding: 8px 20px; border: none;">Ming-3.0-tts-0.5b</td>
      <td align="center" style="padding: 8px 20px; border: none;">稠密</td>
      <td align="center" style="padding: 8px 20px; border: none;">0.5b</td>
      <td align="center" style="padding: 8px 20px; border: none;">
        <a href="https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5b">🤗 HuggingFace</a><br>
        <a href="https://modelscope.cn/models/inclusionAI/Ming-3.0-tts-0.5b">🤖 ModelScope</a>
      </td>
    </tr>
    <tr>
      <td align="center" style="padding: 8px 20px; border: none; border-top: 1px solid rgb(221, 221, 221);">Ming-3.0-tts-tiny</td>
      <td align="center" style="padding: 8px 20px; border: none; border-top: 1px solid rgb(221, 221, 221);">MoE</td>
      <td align="center" style="padding: 8px 20px; border: none; border-top: 1px solid rgb(221, 221, 221);">总计 7.9B · 激活 1.3B</td>
      <td align="center" style="padding: 8px 20px; border: none; border-top: 1px solid rgb(221, 221, 221);">
        <a href="https://huggingface.co/inclusionAI/Ming-3.0-tts-tiny">🤗 HuggingFace</a><br>
        <a href="https://modelscope.cn/models/inclusionAI/Ming-3.0-tts-tiny">🤖 ModelScope</a>
      </td>
    </tr>
  </tbody>
</table>
</div>

每个发布检查点都打包了骨干网络、DiT 头、音频 tokenizer、说话人编码器与文本 tokenizer。0.5b 的发布目录结构如下所示；tiny 使用带 `model.safetensors.index.json` 的分片权重。

```text
Ming-3.0-tts-0.5b/
├── config.json              # model_type: dense, auto_map -> BailingMMConfig
├── configuration.json       # ModelScope task descriptor
├── model.safetensors        # backbone + audio VAE + DiT head + aggregator
├── campplus.onnx            # speaker embedding extractor
├── tokenizer.json           # plus vocab.json / merges.txt / added_tokens.json
├── tokenizer_config.json    #      special_tokens_map.json / chat_template.jinja
└── README.md
```

## <a id="quick-start-"></a>快速开始 🚀

### 安装

```bash
git clone https://github.com/inclusionAI/Ming-3.0-tts.git
cd Ming-3.0-tts
pip install -r requirements.txt        # Ming-3.0-tts-0.5b
```

或者构建 0.5b 的 Docker 镜像（torch 2.6、CUDA 12.4、`transformers==4.46.3`）：

```bash
docker build -f docker/Dockerfile -t ming-tts .
```

0.5b 环境已在 NVIDIA H800-80GB 与 H20-96G 上测试。对 0.5b 而言 `flash-attn` 为可选项；推理会回退到 PyTorch SDPA。

Tiny 使用另一套参考推理环境：Python **3.10.15**、PyTorch 与 torchaudio **2.7.1+cu118**（CUDA 11.8 wheel），以及 `transformers==4.46.3`。由于其他依赖版本与 0.5b 不同，请在专用环境中安装 [requirements-tiny.txt](requirements-tiny.txt) 中固定的依赖。推荐使用 NVIDIA H800 进行推理。

```bash
conda create -n ming-tiny python=3.10.15 -y && conda activate ming-tiny
pip install -r requirements-tiny.txt
```

### 模型下载

```bash
pip install "huggingface_hub[cli]"
hf download inclusionAI/Ming-3.0-tts-0.5b --local-dir Ming-3.0-tts-0.5b
```

在中国大陆，ModelScope 通常更快：

```bash
pip install modelscope
modelscope download --model inclusionAI/Ming-3.0-tts-0.5b --local_dir Ming-3.0-tts-0.5b
```

若要下载另一个变体，将 `0.5b` 替换为 `tiny` 即可。

### 文本正则化

数字、日期、单位与符号通过 FST 文法正则化，需要 `pynini`。它没有通用的 wheel 包：

```bash
conda install -c conda-forge pynini==2.1.6   # or: pip install pynini==2.1.6
```

该依赖为惰性加载；传入 `--no_text_normalization` 可跳过。

### <a id="ming-30-tts-05b"></a>Ming-3.0-tts-0.5b

```bash
python infer.py \
  --model_path inclusionAI/Ming-3.0-tts-0.5b \
  --task TTS \
  --language_id Chinese \
  --text "傍晚的风从山口吹过来，远处的云慢慢染成了金色。" \
  --prompt_wav_path data/voice_presets/voice_audio/lingguang.wav \
  --prompt_text "诶，你今天有空吗？我们能不能聊聊这件事啊？" \
  --use_spk_emb \
  --output output/tts.wav
```

或使用 Python：

```python
from ming_tts import MingTTS

model = MingTTS("inclusionAI/Ming-3.0-tts-0.5b")
model.synthesize(
    task="TTS",
    language_id="Chinese",             # English for English text
    text="傍晚的风从山口吹过来，远处的云慢慢染成了金色。",
    prompt_wav_path="data/voice_presets/voice_audio/lingguang.wav",
    prompt_text="诶，你今天有空吗？我们能不能聊聊这件事啊？",
    use_spk_emb=True,
    output_path="output/tts.wav",
)
```

### Ming-3.0-tts-tiny

每个任务在 [examples/one_click/](examples/one_click/) 中都有一个单行脚本；`MODEL`、`TEXT`、`OUT` 等变量可通过环境变量覆盖：

```bash
bash examples/one_click/run_seed.sh
MODEL=/path/to/Ming-3.0-tts-tiny OUT=outputs/yue.wav bash examples/one_click/run_dialect.sh
```

下面是从 Python 发起的相同调用。加载时会配置发布版运行时（bf16、可移植 MoE 循环、fp32 循环状态），并据此校验检查点；`generate()` 默认使用 `cfg_scale=2.0`、`temperature=0`、`flow_steps=10`、`sigma=0.25` 以及种子 1234（`podcast` 为 1235）：

```python
from ming_tiny import MingTinyTTS

tts = MingTinyTTS.from_pretrained("inclusionAI/Ming-3.0-tts-tiny", device="cuda:0")

tts.generate(
    task="seed",
    text="傍晚的风从山口吹过来，远处的云慢慢染成了金色。",
    prompt_wav="data/voice_presets/voice_audio/lingguang.wav",
    prompt_text="诶，你今天有空吗？我们能不能聊聊这件事啊？",
    target_language="Chinese",          # English for English text
    output_path="outputs/seed.wav",
)

tts.generate(
    task="podcast",
    text="speaker_1: 你最近是不是又去那家面馆了？\nspeaker_2: 对啊，排了半个小时的队，不过真的值得。",
    prompt_wav=["data/voice_presets/voice_audio/lingguang.wav", "data/voice_presets/voice_audio/db30.wav"],
    prompt_text=["诶，你今天有空吗？我们能不能聊聊这件事啊？", "感谢你的认可。"],
    output_path="outputs/podcast.wav",
)
```

每次调用选择一个任务，并接受下表列出的输入：

| 任务 | 参考音频 | 参考文本 | `target_language` | 控制项 |
| --- | --- | --- | --- | --- |
| `seed` | 一段 | 必填 | `Chinese` / `English`，必填 | — |
| `multilingual` | 一段 | 必填 | `German` / `Spanish` / `French` / `Korean` / `Japanese` | — |
| `paralinguistic` | 一段 | 必填 | `Chinese` / `English` | `text` 中的行内标签 |
| `podcast` | 每位说话人一段 | 每位说话人一段，顺序一致 | 从文本推断 | 每行开头标注 `speaker_N:` |
| `basic` | 一段 | 不接受 | — | `speed`、`pitch`、`volume` 三项 |
| `emotion` | 一段 | 不接受 | — | `emotion` |
| `dialect` | 一段 | 不接受 | — | `dialect`：`川渝话` / `广粤话` |
| `freeform` | 默认无（推荐）；可选 | 不接受 | — | `instruction` |
| `voice_design` | 无 | — | — | `style` |
| `ip` | 无 | — | — | `ip` |

`python infer_tiny.py --help` 列出了相同的命令行参数；podcast 场景请重复传入 `--prompt_wav` 与 `--prompt_text`。

| | Ming-3.0-tts-0.5b | Ming-3.0-tts-tiny |
| --- | --- | --- |
| Python API | `ming_tts.MingTTS` | `ming_tiny.MingTinyTTS` |
| CLI | `infer.py` | `infer_tiny.py`、`examples/one_click/` |
| 预检 | `tools/preflight.py` | `tools/preflight_tiny.py` |
| 任务 | TTS（含行内副语言标签）、FREEFORM、VOICE_DESIGN、MULTILINGUAL、BASIC、EMOTION、DIALECT、IP | 与小写任务相同的能力（`seed`、`paralinguistic` 等），外加 `podcast` |

### 验证环境

在不加载权重的情况下检查检查点与分词器：

```bash
python tools/preflight.py --model_path /path/to/Ming-3.0-tts-0.5b
python tools/preflight_tiny.py --model_path /path/to/Ming-3.0-tts-tiny
```

## <a id="cookbook"></a>Cookbook

顺序按一句话的诞生过程排列：谁在说话、怎么说、言语之外的表达、以及在哪里被听到。每个示例对应一个任务；来自其他任务的控制项会被拒绝。文本与控制项均取自[演示页面](https://nomorecoding.github.io/Ming-3.0-tts/)，方便你与在那里听到的效果对照。以下为 0.5b API；完整取值列表见[英文](cookbooks/instruction_en.md) / [简体中文](cookbooks/instructions.md)，每个任务的端到端流程见 [cookbooks/cookbook.ipynb](cookbooks/cookbook.ipynb)。

### 谁在说话

**零样本克隆**：[快速开始](#ming-30-tts-05b)中的 `TTS` 调用会克隆 `prompt_wav_path` 的声音。

**声音设计**：描述你想要的声音；无需参考音频。

```python
model.synthesize(
    task="VOICE_DESIGN",
    text="冰川在漫长岁月中缓缓移动，也悄悄记录着气候变化的痕迹。",
    controls={"style": "成熟沉稳的男性纪录片旁白，吐字清晰，节奏舒缓，语气理性而有厚度。"},
    use_zero_spk_emb=True,
)
```

**内置音色**：推荐 **US_James**、**US_Stella**、**灵小柔** 与 **灵楷**。完整音色列表参见[音色目录](cookbooks/instruction_en.md#built-in-premium-voices)。

```python
model.synthesize(
    task="IP",
    text="The garden will remain open until sunset, provided the weather stays clear.",
    controls={"ip": "US_James"},
    use_zero_spk_emb=True,
)
```

### 怎么说

**自由格式**：用一条自然语言指令描述声音与表达方式。两个模型都默认不使用参考音频生成；不建议添加参考音频。不能与声音设计、内置音色、情感、方言或属性控制组合使用。

```python
model.synthesize(
    task="FREEFORM",
    text="The old radio crackled softly as the storm moved across the valley.",
    instruction="Speak in a warm, intimate storytelling voice, with a gentle pace and a hint of nostalgia.",
    use_zero_spk_emb=True,
)
```

对 Tiny，省略 `prompt_wav` 与 `prompt_text`：

```python
tts.generate(
    task="freeform",
    text="The old radio crackled softly as the storm moved across the valley.",
    instruction="Speak in a warm, intimate storytelling voice, with a gentle pace and a hint of nostalgia.",
)
```

**情感**：`高兴 / 悲伤 / 愤怒 / 恐惧 / 厌恶 / 惊讶 / 中性`。

```python
model.synthesize(
    task="EMOTION",
    text="所有测试都顺利通过了，我们终于可以把这个好消息告诉大家！",
    controls={"emotion": "高兴"},
    prompt_wav_path="data/wavs/emotion_prompt.wav",
    use_spk_emb=True,
)
```

**语速、音高与音量**：语速 `慢速 / 中速 / 快速`，音高与音量 `低 / 中 / 高`。

```python
model.synthesize(
    task="BASIC",
    text="今晚的观测将在云层散开后开始，请耐心等待下一次通知。",
    controls={"speed": "慢速", "pitch": "中", "volume": "中"},
    spk_emb_path="/path/to/speaker_embedding.pt",
    use_spk_emb=True,
)
```

### 言语之外

**副语言标签**：行内使用，可出现在句中任意位置，支持中文或英文。`[Breathing]`、`[Cough]`、`[Sigh]`、`[Laughter]`、`[Surprise-ah]`、`[Surprise-oh]`、`[Dissatisfaction-hnn]`、`[Uhm]`、`[Confirmation-en]`、`[Question-ei]`、`[Question-ah]`、`[Question-en]`、`[Question-oh]`、`[Question-huh]`。

```python
model.synthesize(
    task="TTS",
    text="[Sigh]雨还是没有停，[Cough]我们恐怕只能把活动改到室内了。",
    prompt_wav_path="data/voice_presets/voice_audio/lingguang.wav",
    prompt_text="诶，你今天有空吗？我们能不能聊聊这件事啊？",
    use_spk_emb=True,
)
```

### 在哪里被听到

**多语言**：五种新语言必须提供 `language_id`；短代码与完整名称均可。

```python
model.synthesize(
    task="MULTILINGUAL",
    text="週末、駅前の小さな喫茶店で、季節限定の抹茶パフェを食べました",
    language_id="Japanese",     # ja / ko / de / fr / es
    prompt_wav_path="/path/to/japanese_prompt.wav",
    prompt_text="参考音频对应的日语文本。",
    use_spk_emb=True,
)
```

**方言**：`chuanyu dialect` 或 `cantonese`；该任务不接受 `language_id`。

```python
model.synthesize(
    task="DIALECT",
    text="今日天气几好，我哋食完饭一齐去海边行下啦。",
    controls={"dialect": "cantonese"},
    prompt_wav_path="data/wavs/yue_prompt.wav",
    use_spk_emb=True,
)
```

## <a id="built-in-voices"></a>内置音色

### 推荐音色

| 音色 | 语言 | 特点 |
| :--- | :--- | :--- |
| US_James | 英语（美国） | 男声。旁白、讲解与纪录片。 |
| US_Stella | 英语 | — |
| 灵小柔 | 中文 | 明亮甜美的年轻女声，吐字清晰。适合助手与客服。 |
| 灵楷 | 中文 | 温暖浑厚的年轻男声。适合广播、纪录片与有声书。 |

共提供 100 多个中文音色与 5 个英文音色。完整列表（含情感专属变体）参见[音色目录](cookbooks/instruction_en.md#built-in-premium-voices)。

## <a id="performance"></a>性能

公开基准如下；独立的竞技场结果见 [Artificial Analysis 排行榜](#artificial-analysis-leaderboards)。

<p align="center">
    <img src="./figures/benchmark_basic_1018.png" width="900"/>
</p>
<p align="center">
    <img src="./figures/benchmark_control_1018.png" width="900"/>
</p>

下文中，**tiny** 指 Ming-3.0-tts-tiny，**0.5b** 指 Ming-3.0-tts-0.5b。排名与标记按各指标在所列开源模型中计算；Seed-TTS 与 NVbench-GT 为参考行，不参与排名。当历史 Ming-omni-tts 结果优于某个加粗的 Ming-3.0-tts 数值时，会在表格下方注明，且不声称 SOTA。**加粗**标记每列最佳值，<u>下划线</u>标记次佳值；并列者共享标记。其他系统的结果使用其报告的推理设置。

### 摘要

1. **副语言：**两个模型合计在**全部六项 NVBench 单标签指标上达到 SOTA**；tiny 在**全部三项英文多标签指标上达到 SOTA**。
2. **方言：**0.5b 在粤语 Base CER 与 ACC 上达到 **SOTA**；tiny 在四川话 Hard CER 与 Easy ACC 上达到 **SOTA**。
3. **多语言：**tiny 在德语与西班牙语 WER 上达到 **SOTA**，法语 WER 位列**第 2**，日语 CER 并列**第 2**。
4. **情感：**tiny 在 CV3 文本相关 Happy 上并列 **SOTA**，并在 CV3N 两个 Sad 子集上达到 **SOTA**；0.5b 在 CV3 文本相关 Angry 上达到 **SOTA**。tiny 的 CV3 平均值位列**第 2**。
5. **属性控制：**在本次对比中，0.5b 在平均 ACC 与音高上领先，tiny 则在 WER 与 SIM 上领先。历史 Ming-omni-tts 结果仍保持着相应的总纪录。
6. **播客：**tiny 取得 CER 2.03%、cpSIM 0.561 与 UTMOS 2.12，分别位列**第 1**、**第 2** 与**第 2**；历史 Ming-omni-tts 仍保持更低的 CER。
7. **声音设计：**tiny 在平均 ACC（75.37%）、APS（85.10%）与 DSD（79.90%）上均位列**第 2**。
8. **中英文：**0.5b 的中文 WER 位列**第 3**；tiny 在中英文 SIM 上达到 **SOTA**。
9. **下一步：**改进多语言与粤语的说话人相似度、tiny 的韩语准确率与音高控制、文本无关情感、角色扮演指令遵循，以及预测的播客音质。

### 中英文（seed-tts-eval）

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">模型</th><th colspan="2" style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">seed-tts-eval-zh</th><th colspan="2" style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">seed-tts-eval-en</th></tr>
    <tr><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">SIM ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);"><i>Seed-TTS</i></td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">1.110%</td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">0.796</td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">2.240%</td><td align="center" style="padding: 5px 12px; border: none; color: rgb(119, 119, 119);">0.762</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">GLM-TTS</td><td align="center" style="padding: 5px 12px; border: none;">1.030%</td><td align="center" style="padding: 5px 12px; border: none;">0.761</td><td align="center" style="padding: 5px 12px; border: none;">2.230%</td><td align="center" style="padding: 5px 12px; border: none;">0.672</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">Qwen3-TTS</td><td align="center" style="padding: 5px 12px; border: none;">1.070%</td><td align="center" style="padding: 5px 12px; border: none;">—</td><td align="center" style="padding: 5px 12px; border: none;">1.390%</td><td align="center" style="padding: 5px 12px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">Qwen3-TTS-12Hz-0.6B-Base</td><td align="center" style="padding: 5px 12px; border: none;">0.920%</td><td align="center" style="padding: 5px 12px; border: none;">—</td><td align="center" style="padding: 5px 12px; border: none;"><u>1.320%</u></td><td align="center" style="padding: 5px 12px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">Qwen3-TTS-12Hz-1.7B-Base</td><td align="center" style="padding: 5px 12px; border: none;"><u>0.770%</u></td><td align="center" style="padding: 5px 12px; border: none;">—</td><td align="center" style="padding: 5px 12px; border: none;"><b>1.240%</b></td><td align="center" style="padding: 5px 12px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 12px; border: none;">1.160%</td><td align="center" style="padding: 5px 12px; border: none;"><u>0.780</u></td><td align="center" style="padding: 5px 12px; border: none;">2.020%</td><td align="center" style="padding: 5px 12px; border: none;"><u>0.718</u></td></tr>
    <tr><td style="padding: 5px 12px; border: none;">CosyVoice3-1.5B</td><td align="center" style="padding: 5px 12px; border: none;"><b>0.710%</b></td><td align="center" style="padding: 5px 12px; border: none;">0.775</td><td align="center" style="padding: 5px 12px; border: none;">1.450%</td><td align="center" style="padding: 5px 12px; border: none;">0.695</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">F5-TTS</td><td align="center" style="padding: 5px 12px; border: none;">1.560%</td><td align="center" style="padding: 5px 12px; border: none;">0.741</td><td align="center" style="padding: 5px 12px; border: none;">1.830%</td><td align="center" style="padding: 5px 12px; border: none;">0.647</td></tr>
    <tr><td style="padding: 5px 12px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">0.800%</td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">0.758</td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">1.584%</td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;">0.691</td></tr>
    <tr><td style="padding: 5px 12px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 12px; border: none;">0.820%</td><td align="center" style="padding: 5px 12px; border: none;"><b>0.781</b></td><td align="center" style="padding: 5px 12px; border: none;">1.666%</td><td align="center" style="padding: 5px 12px; border: none;"><b>0.728</b></td></tr>
  </tbody>
</table>

tiny 在中英文上达到 **SOTA 说话人相似度**。0.5b 在两种语言上的 WER 都更低，中文 WER 位列**第 3**。

### 多语言（MiniMaxAI TTS-Multilingual-Test-Set）

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">模型</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">德语</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">西班牙语</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">法语</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">韩语</th><th colspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">日语</th></tr>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">dots.tts</td><td align="center" style="padding: 5px 10px; border: none;">0.452%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.798</u></td><td align="center" style="padding: 5px 10px; border: none;">2.593%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.839</u></td><td align="center" style="padding: 5px 10px; border: none;">19.878%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.789</u></td><td align="center" style="padding: 5px 10px; border: none;">4.837%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.853</u></td><td align="center" style="padding: 5px 10px; border: none;">5.134%</td><td align="center" style="padding: 5px 10px; border: none;"><b>0.838</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">VoxCPM2</td><td align="center" style="padding: 5px 10px; border: none;">0.963%</td><td align="center" style="padding: 5px 10px; border: none;">0.790</td><td align="center" style="padding: 5px 10px; border: none;">1.324%</td><td align="center" style="padding: 5px 10px; border: none;">0.836</td><td align="center" style="padding: 5px 10px; border: none;"><b>3.380%</b></td><td align="center" style="padding: 5px 10px; border: none;">0.761</td><td align="center" style="padding: 5px 10px; border: none;">3.547%</td><td align="center" style="padding: 5px 10px; border: none;">0.839</td><td align="center" style="padding: 5px 10px; border: none;">4.358%</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.825</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">Fish Audio S2</td><td align="center" style="padding: 5px 10px; border: none;">1.045%</td><td align="center" style="padding: 5px 10px; border: none;">0.714</td><td align="center" style="padding: 5px 10px; border: none;">1.216%</td><td align="center" style="padding: 5px 10px; border: none;">0.748</td><td align="center" style="padding: 5px 10px; border: none;">3.636%</td><td align="center" style="padding: 5px 10px; border: none;">0.698</td><td align="center" style="padding: 5px 10px; border: none;"><u>1.675%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.761</td><td align="center" style="padding: 5px 10px; border: none;"><u>3.427%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.755</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">FireRedTTS3</td><td align="center" style="padding: 5px 10px; border: none;"><u>0.348%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.825</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>1.086%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.868</b></td><td align="center" style="padding: 5px 10px; border: none;">4.366%</td><td align="center" style="padding: 5px 10px; border: none;"><b>0.807</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>1.644%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.864</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>3.418%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>0.825</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.365%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.753</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">1.099%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.763</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">4.264%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.675</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">1.728%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.793</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">3.765%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">0.765</td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.325%</b></td><td align="center" style="padding: 5px 10px; border: none;">0.791</td><td align="center" style="padding: 5px 10px; border: none;"><b>0.971%</b></td><td align="center" style="padding: 5px 10px; border: none;">0.797</td><td align="center" style="padding: 5px 10px; border: none;"><u>3.470%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.733</td><td align="center" style="padding: 5px 10px; border: none;">6.000%</td><td align="center" style="padding: 5px 10px; border: none;">0.797</td><td align="center" style="padding: 5px 10px; border: none;"><u>3.427%</u></td><td align="center" style="padding: 5px 10px; border: none;">0.780</td></tr>
  </tbody>
</table>

<sub>每个开源模型均在统一的基于 ASR 的 WER/CER 评测协议下，使用其推荐推理设置进行评测。</sub>

tiny 在德语与西班牙语 WER 上达到 **SOTA**，法语 WER 位列**第 2**，日语 CER 并列**第 2**。0.5b 在韩语上更准确；说话人相似度是两个模型共同的差距。

### 副语言控制（NVBench）

报告 CER、PCER（副语言 CER）与 OCER。NVbench-GT 为人工标注的参考，仅作对照展示，不参与排名。

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">模型</th><th colspan="6" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">单标签</th><th colspan="6" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">多标签</th></tr>
    <tr><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">中文</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">英文</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">中文</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">英文</th></tr>
    <tr><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">PCER</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">OCER</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);"><i>NVbench-GT</i></td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">3.86</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">9.38</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">4.07</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">6.73</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">8.31</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">6.90</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">3.79</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">23.71</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">5.07</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">7.26</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">21.41</td><td align="center" style="padding: 5px 8px; border: none; color: rgb(119, 119, 119);">8.62</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">Orpheus-TTS</td><td align="center" style="padding: 5px 8px; border: none;">11.36</td><td align="center" style="padding: 5px 8px; border: none;">88.77</td><td align="center" style="padding: 5px 8px; border: none;">13.91</td><td align="center" style="padding: 5px 8px; border: none;">9.03</td><td align="center" style="padding: 5px 8px; border: none;">71.92</td><td align="center" style="padding: 5px 8px; border: none;">10.63</td><td align="center" style="padding: 5px 8px; border: none;">19.83</td><td align="center" style="padding: 5px 8px; border: none;">84.85</td><td align="center" style="padding: 5px 8px; border: none;">24.38</td><td align="center" style="padding: 5px 8px; border: none;">8.68</td><td align="center" style="padding: 5px 8px; border: none;">71.46</td><td align="center" style="padding: 5px 8px; border: none;">11.89</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">SMIIP-NV-CV2</td><td align="center" style="padding: 5px 8px; border: none;">8.80</td><td align="center" style="padding: 5px 8px; border: none;">75.64</td><td align="center" style="padding: 5px 8px; border: none;">11.34</td><td align="center" style="padding: 5px 8px; border: none;">17.92</td><td align="center" style="padding: 5px 8px; border: none;">56.80</td><td align="center" style="padding: 5px 8px; border: none;">19.47</td><td align="center" style="padding: 5px 8px; border: none;">10.66</td><td align="center" style="padding: 5px 8px; border: none;">77.20</td><td align="center" style="padding: 5px 8px; border: none;">14.79</td><td align="center" style="padding: 5px 8px; border: none;">20.93</td><td align="center" style="padding: 5px 8px; border: none;">54.49</td><td align="center" style="padding: 5px 8px; border: none;">23.87</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">Emilia-NV-CV2</td><td align="center" style="padding: 5px 8px; border: none;">5.05</td><td align="center" style="padding: 5px 8px; border: none;">40.00</td><td align="center" style="padding: 5px 8px; border: none;">6.64</td><td align="center" style="padding: 5px 8px; border: none;">12.50</td><td align="center" style="padding: 5px 8px; border: none;">55.30</td><td align="center" style="padding: 5px 8px; border: none;">13.21</td><td align="center" style="padding: 5px 8px; border: none;">5.54</td><td align="center" style="padding: 5px 8px; border: none;">48.74</td><td align="center" style="padding: 5px 8px; border: none;">8.09</td><td align="center" style="padding: 5px 8px; border: none;">11.71</td><td align="center" style="padding: 5px 8px; border: none;">60.28</td><td align="center" style="padding: 5px 8px; border: none;">14.63</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice3</td><td align="center" style="padding: 5px 8px; border: none;">3.85</td><td align="center" style="padding: 5px 8px; border: none;">57.69</td><td align="center" style="padding: 5px 8px; border: none;">5.86</td><td align="center" style="padding: 5px 8px; border: none;">7.87</td><td align="center" style="padding: 5px 8px; border: none;">62.75</td><td align="center" style="padding: 5px 8px; border: none;">9.06</td><td align="center" style="padding: 5px 8px; border: none;">4.75</td><td align="center" style="padding: 5px 8px; border: none;">61.94</td><td align="center" style="padding: 5px 8px; border: none;">8.26</td><td align="center" style="padding: 5px 8px; border: none;"><u>6.39</u></td><td align="center" style="padding: 5px 8px; border: none;">57.84</td><td align="center" style="padding: 5px 8px; border: none;">10.69</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">NV-FlexiVoice</td><td align="center" style="padding: 5px 8px; border: none;">6.98</td><td align="center" style="padding: 5px 8px; border: none;">31.08</td><td align="center" style="padding: 5px 8px; border: none;">8.15</td><td align="center" style="padding: 5px 8px; border: none;">11.88</td><td align="center" style="padding: 5px 8px; border: none;">50.43</td><td align="center" style="padding: 5px 8px; border: none;">13.21</td><td align="center" style="padding: 5px 8px; border: none;">8.20</td><td align="center" style="padding: 5px 8px; border: none;">39.37</td><td align="center" style="padding: 5px 8px; border: none;">10.39</td><td align="center" style="padding: 5px 8px; border: none;">9.60</td><td align="center" style="padding: 5px 8px; border: none;">51.32</td><td align="center" style="padding: 5px 8px; border: none;">13.76</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">NV-CV3</td><td align="center" style="padding: 5px 8px; border: none;">3.80</td><td align="center" style="padding: 5px 8px; border: none;">27.69</td><td align="center" style="padding: 5px 8px; border: none;"><u>4.90</u></td><td align="center" style="padding: 5px 8px; border: none;">8.33</td><td align="center" style="padding: 5px 8px; border: none;">46.13</td><td align="center" style="padding: 5px 8px; border: none;">9.44</td><td align="center" style="padding: 5px 8px; border: none;"><b>3.44</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>30.04</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>4.84</b></td><td align="center" style="padding: 5px 8px; border: none;">6.70</td><td align="center" style="padding: 5px 8px; border: none;"><u>47.13</u></td><td align="center" style="padding: 5px 8px; border: none;"><u>10.10</u></td></tr>
    <tr><td style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>2.70</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>22.80</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>3.20</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>7.60</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>37.00</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>8.90</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>3.50</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">36.60</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">8.10</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">7.90</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">47.30</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">10.40</td></tr>
    <tr><td style="padding: 5px 8px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 8px; border: none;"><u>2.80</u></td><td align="center" style="padding: 5px 8px; border: none;"><b>17.23</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>3.20</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>5.86</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>32.95</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>7.05</b></td><td align="center" style="padding: 5px 8px; border: none;">4.49</td><td align="center" style="padding: 5px 8px; border: none;"><u>32.88</u></td><td align="center" style="padding: 5px 8px; border: none;"><u>5.81</u></td><td align="center" style="padding: 5px 8px; border: none;"><b>5.12</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>46.13</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>7.68</b></td></tr>
  </tbody>
</table>

两个模型合计在**全部六项中英文单标签指标上达到 SOTA**；tiny 还在全部三项英文多标签指标上领先。中文多标签控制仍落后于 NV-CV3。

### 方言

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">模型</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSC-Eval-TTS-easy</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSC-Eval-TTS-hard</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSYue-TTS-eval-Base</th><th colspan="3" style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">WSYue-TTS-eval-Coverage</th></tr>
    <tr><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">SIM ↑</th><th style="padding: 6px 8px; border: none; border-bottom: 1px solid black;">ACC ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 8px; border: none;">Qwen3-TTS</td><td align="center" style="padding: 5px 8px; border: none;">4.13%</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">7.35%</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 8px; border: none;">3.17%</td><td align="center" style="padding: 5px 8px; border: none;">0.696</td><td align="center" style="padding: 5px 8px; border: none;">76.05%</td><td align="center" style="padding: 5px 8px; border: none;">4.07%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.723</u></td><td align="center" style="padding: 5px 8px; border: none;">81.41%</td><td align="center" style="padding: 5px 8px; border: none;">8.36%</td><td align="center" style="padding: 5px 8px; border: none;">0.611</td><td align="center" style="padding: 5px 8px; border: none;">91.70%</td><td align="center" style="padding: 5px 8px; border: none;">8.95%</td><td align="center" style="padding: 5px 8px; border: none;">0.658</td><td align="center" style="padding: 5px 8px; border: none;"><b>95.80%</b></td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice3-1.5B + DiffRO-EMO</td><td align="center" style="padding: 5px 8px; border: none;">7.14%</td><td align="center" style="padding: 5px 8px; border: none;">0.703</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">9.06%</td><td align="center" style="padding: 5px 8px; border: none;">0.601</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">14.38%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.812</u></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">13.74%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.826</u></td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice2-WSC</td><td align="center" style="padding: 5px 8px; border: none;">4.28%</td><td align="center" style="padding: 5px 8px; border: none;"><u>0.728</u></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">8.87%</td><td align="center" style="padding: 5px 8px; border: none;">0.626</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice2-WSC-SFT</td><td align="center" style="padding: 5px 8px; border: none;">4.08%</td><td align="center" style="padding: 5px 8px; border: none;"><b>0.788</b></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">7.22%</td><td align="center" style="padding: 5px 8px; border: none;">0.680</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">CosyVoice2-Yue</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">10.33%</td><td align="center" style="padding: 5px 8px; border: none;"><b>0.821</b></td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">9.49%</td><td align="center" style="padding: 5px 8px; border: none;"><b>0.834</b></td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none;">Sparks-TTS</td><td align="center" style="padding: 5px 8px; border: none;">10.83%</td><td align="center" style="padding: 5px 8px; border: none;">0.677</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">12.52%</td><td align="center" style="padding: 5px 8px; border: none;">0.545</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">27.79%</td><td align="center" style="padding: 5px 8px; border: none;">0.762</td><td align="center" style="padding: 5px 8px; border: none;">—</td><td align="center" style="padding: 5px 8px; border: none;">24.25%</td><td align="center" style="padding: 5px 8px; border: none;">0.781</td><td align="center" style="padding: 5px 8px; border: none;">—</td></tr>
    <tr><td style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>2.27%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.689</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>80.68%</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>3.35%</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.691</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>87.64%</u></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>6.15%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.586</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>98.00%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><b>8.15%</b></td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;">0.622</td><td align="center" style="padding: 5px 8px; border: none; border-top: 1px solid black;"><u>95.27%</u></td></tr>
    <tr><td style="padding: 5px 8px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 8px; border: none;"><u>2.53%</u></td><td align="center" style="padding: 5px 8px; border: none;">0.721</td><td align="center" style="padding: 5px 8px; border: none;"><b>86.09%</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>3.11%</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>0.738</b></td><td align="center" style="padding: 5px 8px; border: none;"><b>88.94%</b></td><td align="center" style="padding: 5px 8px; border: none;"><u>7.40%</u></td><td align="center" style="padding: 5px 8px; border: none;">0.605</td><td align="center" style="padding: 5px 8px; border: none;"><u>92.90%</u></td><td align="center" style="padding: 5px 8px; border: none;"><u>8.67%</u></td><td align="center" style="padding: 5px 8px; border: none;">0.653</td><td align="center" style="padding: 5px 8px; border: none;">95.16%</td></tr>
  </tbody>
</table>

tiny 在四川话控制准确率上更强，达到 **SOTA 的四川话 Hard CER 与 Easy ACC**；0.5b 则达到 **SOTA 的粤语 Base CER 与 ACC**。粤语说话人相似度仍低于 CosyVoice2-Yue。历史 Ming-omni-tts 结果在四川话 Easy CER（2.25%）、Hard SIM（0.750）与 Hard ACC（90.45%）以及粤语 Coverage CER（7.87%）上仍然更强。

### 情感控制（CV3）

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">模型</th><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">平均</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">文本相关</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">文本无关</th></tr>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 10px; border: none;">66.33%</td><td align="center" style="padding: 5px 10px; border: none;">92%</td><td align="center" style="padding: 5px 10px; border: none;">70%</td><td align="center" style="padding: 5px 10px; border: none;">72%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td><td align="center" style="padding: 5px 10px; border: none;">42%</td><td align="center" style="padding: 5px 10px; border: none;">58%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-1.5B</td><td align="center" style="padding: 5px 10px; border: none;">63.00%</td><td align="center" style="padding: 5px 10px; border: none;">86%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td><td align="center" style="padding: 5px 10px; border: none;">72%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td><td align="center" style="padding: 5px 10px; border: none;">44%</td><td align="center" style="padding: 5px 10px; border: none;">48%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-1.5B + DiffRO-EMO</td><td align="center" style="padding: 5px 10px; border: none;"><b>77.67%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>98%</b></td><td align="center" style="padding: 5px 10px; border: none;">68%</td><td align="center" style="padding: 5px 10px; border: none;">84%</td><td align="center" style="padding: 5px 10px; border: none;"><b>98%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>50%</u></td><td align="center" style="padding: 5px 10px; border: none;">68%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">F5-TTS</td><td align="center" style="padding: 5px 10px; border: none;">64.67%</td><td align="center" style="padding: 5px 10px; border: none;">92%</td><td align="center" style="padding: 5px 10px; border: none;">52%</td><td align="center" style="padding: 5px 10px; border: none;">72%</td><td align="center" style="padding: 5px 10px; border: none;"><u>80%</u></td><td align="center" style="padding: 5px 10px; border: none;">28%</td><td align="center" style="padding: 5px 10px; border: none;">64%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;">Sparks-TTS</td><td align="center" style="padding: 5px 10px; border: none;">55.33%</td><td align="center" style="padding: 5px 10px; border: none;">80%</td><td align="center" style="padding: 5px 10px; border: none;">56%</td><td align="center" style="padding: 5px 10px; border: none;">50%</td><td align="center" style="padding: 5px 10px; border: none;">50%</td><td align="center" style="padding: 5px 10px; border: none;"><b>60%</b></td><td align="center" style="padding: 5px 10px; border: none;">36%</td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">72.33%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>96%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>76%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>94%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">52%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">36%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>80%</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>74.00%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>98%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>82%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>90%</u></td><td align="center" style="padding: 5px 10px; border: none;">60%</td><td align="center" style="padding: 5px 10px; border: none;">36%</td><td align="center" style="padding: 5px 10px; border: none;"><u>78%</u></td></tr>
  </tbody>
</table>

tiny 与 0.5b 的平均 ACC 分别位列**第 2** 与**第 3**。tiny 在文本相关 Happy 与 Sad 上更强，0.5b 在 Angry 上更强；文本无关情感仍是共同短板。历史 Ming-omni-tts 结果在文本相关 Sad（86%）与文本无关 Angry（82%）上仍更高。

### 情感控制（CV3N，高难情感控制）

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">模型</th><th rowspan="2" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">平均</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">文本相关</th><th colspan="3" style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">文本无关</th></tr>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Happy</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Sad</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">Angry</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 10px; border: none;"><b>40.00%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>68%</u></td><td align="center" style="padding: 5px 10px; border: none;">30%</td><td align="center" style="padding: 5px 10px; border: none;"><b>78%</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>14%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>4%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>46%</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>37.33%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>70%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>36%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>70%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>14%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>4%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>30%</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;">30.67%</td><td align="center" style="padding: 5px 10px; border: none;">60%</td><td align="center" style="padding: 5px 10px; border: none;"><b>40%</b></td><td align="center" style="padding: 5px 10px; border: none;">44%</td><td align="center" style="padding: 5px 10px; border: none;"><b>18%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>10%</b></td><td align="center" style="padding: 5px 10px; border: none;">12%</td></tr>
  </tbody>
</table>

0.5b 与 tiny 的平均 ACC 分别位列**第 2** 与**第 3**。tiny 在两个 Sad 子集上达到 **SOTA**，0.5b 的整体准确率更高。历史 Ming-omni-tts 结果在文本相关 Happy（78%）与文本无关 Happy（30%）上仍更高。

### 声音设计（InstructTTSEval-ZH）

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">模型</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">平均</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">APS</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">DSD</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">RP</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">Qwen3-TTS</td><td align="center" style="padding: 5px 10px; border: none;"><b>77.13%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>85.20%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>81.10%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>65.10%</b></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">Mimo-Audio-7B-Instruct</td><td align="center" style="padding: 5px 10px; border: none;">70.50%</td><td align="center" style="padding: 5px 10px; border: none;">75.70%</td><td align="center" style="padding: 5px 10px; border: none;">74.30%</td><td align="center" style="padding: 5px 10px; border: none;"><u>61.50%</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">VoiceSculptor</td><td align="center" style="padding: 5px 10px; border: none;">67.30%</td><td align="center" style="padding: 5px 10px; border: none;">75.70%</td><td align="center" style="padding: 5px 10px; border: none;">64.70%</td><td align="center" style="padding: 5px 10px; border: none;"><u>61.50%</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;">VoxInstruct</td><td align="center" style="padding: 5px 10px; border: none;">47.47%</td><td align="center" style="padding: 5px 10px; border: none;">47.50%</td><td align="center" style="padding: 5px 10px; border: none;">52.30%</td><td align="center" style="padding: 5px 10px; border: none;">42.60%</td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">72.29%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">78.54%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">77.28%</td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;">61.06%</td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;"><u>75.37%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>85.10%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>79.90%</u></td><td align="center" style="padding: 5px 10px; border: none;">61.10%</td></tr>
  </tbody>
</table>

tiny 与 0.5b 的平均 ACC 分别位列**第 2** 与**第 3**，落后于 Qwen3-TTS。角色扮演指令遵循仍是两个模型的主要差距。

### 基础属性控制

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">模型</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">语速</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">音量</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">音高</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">平均</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">WER ↓</th><th style="padding: 6px 10px; border: none; border-bottom: 1px solid black;">SIM ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 10px; border: none;">CosyVoice3-0.5B</td><td align="center" style="padding: 5px 10px; border: none;"><b>100.00%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>97.67%</b></td><td align="center" style="padding: 5px 10px; border: none;">65.33%</td><td align="center" style="padding: 5px 10px; border: none;">87.67%</td><td align="center" style="padding: 5px 10px; border: none;">1.210%</td><td align="center" style="padding: 5px 10px; border: none;">0.580</td></tr>
    <tr><td style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-0.5b</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>99.00%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>95.00%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>86.00%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><b>93.30%</b></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>0.317%</u></td><td align="center" style="padding: 5px 10px; border: none; border-top: 1px solid black;"><u>0.712</u></td></tr>
    <tr><td style="padding: 5px 10px; border: none;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 10px; border: none;">93.00%</td><td align="center" style="padding: 5px 10px; border: none;">93.00%</td><td align="center" style="padding: 5px 10px; border: none;"><u>78.70%</u></td><td align="center" style="padding: 5px 10px; border: none;"><u>88.23%</u></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.274%</b></td><td align="center" style="padding: 5px 10px; border: none;"><b>0.742</b></td></tr>
  </tbody>
</table>

0.5b 的控制准确率更高，tiny 的 WER 更低、说话人相似度更高。历史 Ming-omni-tts 模型仍保持着平均 ACC、音高、WER 与 SIM 的总纪录。

### 播客

<table style="border-collapse: collapse; border-top: 1.5px solid black; border-bottom: 1.5px solid black; margin: 16px 0;">
  <thead>
    <tr><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">模型</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">CER ↓</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">cpSIM ↑</th><th style="padding: 6px 12px; border: none; border-bottom: 1px solid black;">UTMOS ↑</th></tr>
  </thead>
  <tbody>
    <tr><td style="padding: 5px 12px; border: none;">FireRedTTS2</td><td align="center" style="padding: 5px 12px; border: none;">3.34%</td><td align="center" style="padding: 5px 12px; border: none;">0.512</td><td align="center" style="padding: 5px 12px; border: none;">1.90</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">SoulX-Podcast</td><td align="center" style="padding: 5px 12px; border: none;"><u>2.20%</u></td><td align="center" style="padding: 5px 12px; border: none;"><b>0.599</b></td><td align="center" style="padding: 5px 12px; border: none;">2.09</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">VibeVoice-1.5B</td><td align="center" style="padding: 5px 12px; border: none;">12.87%</td><td align="center" style="padding: 5px 12px; border: none;">0.455</td><td align="center" style="padding: 5px 12px; border: none;">1.74</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">MOSS-TTSD</td><td align="center" style="padding: 5px 12px; border: none;">8.62%</td><td align="center" style="padding: 5px 12px; border: none;">0.421</td><td align="center" style="padding: 5px 12px; border: none;">1.70</td></tr>
    <tr><td style="padding: 5px 12px; border: none;">ZipVoice-Dia</td><td align="center" style="padding: 5px 12px; border: none;">3.39%</td><td align="center" style="padding: 5px 12px; border: none;">0.553</td><td align="center" style="padding: 5px 12px; border: none;"><b>2.24</b></td></tr>
    <tr><td style="padding: 5px 12px; border: none;">MoonCast</td><td align="center" style="padding: 5px 12px; border: none;">27.43%</td><td align="center" style="padding: 5px 12px; border: none;">0.441</td><td align="center" style="padding: 5px 12px; border: none;">1.76</td></tr>
    <tr><td style="padding: 5px 12px; border: none; border-top: 1px solid black;"><b>Ming-3.0-tts-tiny</b></td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;"><b>2.03%</b></td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;"><u>0.561</u></td><td align="center" style="padding: 5px 12px; border: none; border-top: 1px solid black;"><u>2.12</u></td></tr>
  </tbody>
</table>

tiny 的 CER 位列**第 1**，cpSIM 与 UTMOS 位列**第 2**。历史 Ming-omni-tts 仍保持更低的 CER 与更高的 UTMOS。

## <a id="limitations"></a>局限性

- **说话人相似度。**tiny 的德语 SIM（0.791）位列第三，但在其余四种新语言上两个模型都未进入前三。法语 SIM 为 0.5b 0.675、tiny 0.733；两者的粤语 SIM 也都落后于 CosyVoice2-Yue。
- **一句话中的多个事件。**NVBench *Multi* 可用，但落后于 *Single*；单句多标签下的稳定性仍在改进。
- **仅凭演绎传达情感。**当文字本身不携带情感信号时（CV3-Eval 文本无关及大部分高难集合），准确率远低于文本相关的一半。
- **tiny 的音高。**音高是两个模型中准确率最低的属性。tiny 的 78.70% 位列第 2，比 0.5b 的 86.00% 低 7.30 个百分点；历史 Ming-omni-tts-0.5B 的成绩为 91.33%。
- **角色扮演声音设计。**RP 是声音设计中得分最低的子项，tiny（61.10%）位列第 4，0.5b（61.06%）位列第 5。
- **tiny 的韩语。**tiny 的韩语 CER（6.000%）位列第 6，明显落后于 0.5b 的 1.728%（第 3）。
- **播客音质。**tiny 的 UTMOS 为 2.12，位列第 2，低于 ZipVoice-Dia 的 2.24 与历史 Ming-omni-tts-0.5B 的 2.25。

## <a id="usage-disclaimer"></a>使用免责声明

- 声音克隆与内置角色音色仅供研究与合法创意用途。请勿在未经同意的情况下冒充真实人物、实施欺骗或用于任何非法目的。
- 在合成语音可能被误认为真实录音的场合，请将其标注为合成语音。
- 作者对滥用行为不承担任何责任。如发现本项目被滥用，请向我们报告。

## 致谢

- [CAM++](https://modelscope.cn/models/iic/speech_campplus_sv_zh-cn_16k-common)：用于说话人嵌入提取
- [Ming-omni-tts](https://github.com/inclusionAI/Ming-omni-tts)：提供音频 tokenizer

## 许可证

依据 [MIT](LICENSE) 许可证发布。

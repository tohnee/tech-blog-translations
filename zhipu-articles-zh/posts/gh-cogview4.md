---
title: "CogView4、CogView3 与 CogView-3Plus"
source: https://github.com/THUDM/CogView4
crawled: 2026-09-22
title_en: "CogView4 & CogView3 & CogView-3Plus"
translated: 2026-09-22
---

# CogView4、CogView3 与 CogView-3Plus

> 原文：[CogView4 & CogView3 & CogView-3Plus](https://github.com/THUDM/CogView4) · 智谱 Z.ai / THUDM

[阅读中文版](./README_zh.md)
[日本語で読む](./README_ja.md)

<div align="center">
<img src=resources/logo.svg width="50%"/>
</div>

<p align="center">
<a href="https://huggingface.co/spaces/THUDM-HF-SPACE/CogView4"  target="_blank"> 🤗 HuggingFace Space</a>
<a href="https://modelscope.cn/studios/ZhipuAI/CogView4" target="_blank">  🤖ModelScope Space</a>
<a href="https://zhipuaishengchan.datasink.sensorsdata.cn/t/4z" target="_blank"> 🛠️智谱 AI MaaS（更快）</a>
<br>
<a href="resources/WECHAT.md" target="_blank"> 👋 微信社区</a>  <a href="https://arxiv.org/abs/2403.05121" target="_blank">📚 CogView3 论文</a>
</p>

![showcase.png](resources/showcase.png)

## 项目动态

- 🔥🔥 ```2025/03/24```：我们推出 [CogKit](https://github.com/THUDM/CogKit)，一个用于 **CogView4** 与 **CogVideoX** 系列微调与推理的强大工具包，帮助你充分探索我们的多模态生成模型。
- ```2025/03/04```：我们适配并开源了 **CogView-4** 模型的 [diffusers](https://github.com/huggingface/diffusers) 版本，该模型拥有 6B 参数，支持原生中文输入与中文文生图。
  你可以[在线](https://huggingface.co/spaces/THUDM-HF-SPACE/CogView4)试用。
- ```2024/10/13```：我们适配并开源了 **CogView-3Plus-3B** 模型的 [diffusers](https://github.com/huggingface/diffusers) 版本。你可以
  [在线](https://huggingface.co/spaces/THUDM-HF-SPACE/CogView3-Plus-3B-Space)试用。
- ```2024/9/29```：我们开源了 **CogView3** 与 **CogView-3Plus-3B**。**CogView3** 是一个
  基于级联扩散（cascading diffusion）的文生图系统，采用接力扩散（relay diffusion）框架。**CogView-3Plus** 则是一系列基于
  Diffusion Transformer 新开发的文生图模型。

## 项目规划

- [X] Diffusers 工作流适配
- [X] Cog 系列微调工具包（即将推出）
- [ ] ControlNet 模型与训练代码

## 社区贡献

我们在此收录了一些与本仓库相关的社区项目。这些项目由社区成员维护，我们感谢他们的贡献。

+ [ComfyUI_CogView4_Wrapper](https://github.com/chflame163/ComfyUI_CogView4_Wrapper) - CogView4 项目在 ComfyUI 中的一个实现。

## 模型简介

### 模型对比

<table style="border-collapse: collapse; width: 100%;">
  <tr>
    <th style="text-align: center;">模型名称</th>
    <th style="text-align: center;">CogView4</th>
    <th style="text-align: center;">CogView3-Plus-3B</th>
  </tr>
    <td style="text-align: center;">分辨率</td>
    <td colspan="2" style="text-align: center;">
            512 <= H, W <= 2048 <br>
            H * W <= 2^{21} <br>
            H, W \mod 32 = 0
    </td>
  <tr>
    <td style="text-align: center;">推理精度</td>
    <td colspan="2" style="text-align: center;">仅支持 BF16、FP32</td>
  <tr>
  <td style="text-align: center;">编码器</td>
  <td style="text-align: center;"><a href="https://huggingface.co/THUDM/glm-4-9b-hf" target="_blank">GLM-4-9B</a></td>
  <td style="text-align: center;"><a href="https://huggingface.co/google/t5-v1_1-xxl" target="_blank">T5-XXL</a></td>
</tr>
  <tr>
    <td style="text-align: center;">提示词语言</td>
    <td style="text-align: center;">中文、英文</td>
    <td style="text-align: center;">英文</td>
  </tr>
  <tr>
    <td style="text-align: center;">提示词长度限制</td>
    <td style="text-align: center;">1024 Tokens</td>
    <td style="text-align: center;">224 Tokens</td>
  </tr>
  <tr>
    <td style="text-align: center;">下载链接</td>
    <td style="text-align: center;"><a href="https://huggingface.co/THUDM/CogView4-6B">🤗 HuggingFace</a><br><a href="https://modelscope.cn/models/ZhipuAI/CogView4-6B">🤖 ModelScope</a><br><a href="https://wisemodel.cn/models/ZhipuAI/CogView4-6B">🟣 WiseModel</a></td>
    <td style="text-align: center;"><a href="https://huggingface.co/THUDM/CogView3-Plus-3B">🤗 HuggingFace</a><br><a href="https://modelscope.cn/models/ZhipuAI/CogView3-Plus-3B">🤖 ModelScope</a><br><a href="https://wisemodel.cn/models/ZhipuAI/CogView3-Plus-3B">🟣 WiseModel</a></td>
  </tr>
</table>

### 显存占用

DIT 模型在 `BF16` 精度、`batchsize=4` 下测试，结果如下表所示：

| 分辨率  | enable_model_cpu_offload 关闭 | enable_model_cpu_offload 开启 | enable_model_cpu_offload 开启 </br> 文本编码器 4bit |
|-------------|------------------------------|-----------------------------|-----------------------------------------------------|
| 512 * 512   | 33GB                         | 20GB                        | 13G                                                 |
| 1280 * 720  | 35GB                         | 20GB                        | 13G                                                 |
| 1024 * 1024 | 35GB                         | 20GB                        | 13G                                                 |
| 1920 * 1280 | 39GB                         | 20GB                        | 14G                                                 |

此外，我们建议你的设备至少拥有 `32GB` 内存，以防止进程被杀死。

### 模型指标

我们在多个基准上进行了测试，取得如下成绩：

#### DPG-Bench

| 模型        | 总体   | 全局    | 实体    | 属性 | 关系  | 其他     |
|--------------|-----------|-----------|-----------|-----------|-----------|-----------|
| SDXL         | 74.65     | 83.27     | 82.43     | 80.91     | 86.76     | 80.41     |
| PixArt-alpha | 71.11     | 74.97     | 79.32     | 78.60     | 82.57     | 76.96     |
| SD3-Medium   | 84.08     | 87.90     | **91.01** | 88.83     | 80.70     | 88.68     |
| DALL-E 3      | 83.50     | **90.97** | 89.61     | 88.39     | 90.58     | 89.83     |
| Flux.1-dev   | 83.79     | 85.80     | 86.79     | 89.98     | 90.04     | **89.90** |
| Janus-Pro-7B | 84.19     | 86.90     | 88.90     | 89.40     | 89.32     | 89.48     |
| **CogView4-6B** | **85.13** | 83.85     | 90.35     | **91.17** | **91.14** | 87.29     |

#### GenEval

| 模型           | 总体  | 单对象 | 双对象 | 计数 | 颜色   | 位置 | 颜色归属 |
|-----------------|----------|-------------|----------|----------|----------|----------|-------------------|
| SDXL            | 0.55     | 0.98        | 0.74     | 0.39     | 0.85     | 0.15     | 0.23              |
| PixArt-alpha    | 0.48     | 0.98        | 0.50     | 0.44     | 0.80     | 0.08     | 0.07              |
| SD3-Medium      | 0.74     | **0.99**    | **0.94** | 0.72     | 0.89     | 0.33     | 0.60              |
| DALL-E 3        | 0.67     | 0.96        | 0.87     | 0.47     | 0.83     | 0.43     | 0.45              |
| Flux.1-dev      | 0.66     | 0.98        | 0.79     | **0.73** | 0.77     | 0.22     | 0.45              |
| Janus-Pro-7B    | **0.80** | **0.99**    | 0.89     | 0.59     | **0.90** | **0.79** | **0.66**          |
| **CogView4-6B** | 0.73     | **0.99**    | 0.86     | 0.66     | 0.79     | 0.48     | 0.58              |

#### T2I-CompBench

| 模型           | 颜色      | 形状      | 纹理    | 2D 空间 | 3D 空间 | 数值   | 非空间 Clip | 复杂三合一 |
|-----------------|------------|------------|------------|------------|------------|------------|------------------|----------------|
| SDXL            | 0.5879     | 0.4687     | 0.5299     | 0.2133     | 0.3566     | 0.4988     | 0.3119           | 0.3237         |
| PixArt-alpha    | 0.6690     | 0.4927     | 0.6477     | 0.2064     | 0.3901     | 0.5058     | **0.3197**       | 0.3433         |
| SD3-Medium      | **0.8132** | 0.5885     | **0.7334** | **0.3200** | **0.4084** | 0.6174     | 0.3140           | 0.3771         |
| DALL-E 3        | 0.7785     | **0.6205** | 0.7036     | 0.2865     | 0.3744     | 0.5880     | 0.3003           | 0.3773         |
| Flux.1-dev      | 0.7572     | 0.5066     | 0.6300     | 0.2700     | 0.3992     | 0.6165     | 0.3065           | 0.3628         |
| Janus-Pro-7B    | 0.5145     | 0.3323     | 0.4069     | 0.1566     | 0.2753     | 0.4406     | 0.3137           | 0.3806         |
| **CogView4-6B** | 0.7786     | 0.5880     | 0.6983     | 0.3075     | 0.3708     | **0.6626** | 0.3056           | **0.3869**     |

## 中文文字准确性评测

| 模型           | 精确率  | 召回率     | F1 分数   | Pick@4     |
|-----------------|------------|------------|------------|------------|
| Kolors          | 0.6094     | 0.1886     | 0.2880     | 0.1633     |
| **CogView4-6B** | **0.6969** | **0.5532** | **0.6168** | **0.3265** |

## 推理模型

### 提示词优化

尽管 CogView4 系列模型使用冗长的合成图像描述进行训练，我们仍强烈建议在文生图之前
使用大语言模型改写提示词，这将大幅提升生成质量。

我们提供了[示例脚本](inference/prompt_optimize.py)。我们建议运行该脚本来润色你的提示词。
注意，`CogView4` 与 `CogView3` 模型在提示词优化中使用不同的少样本示例，需要加以
区分。

```shell
cd inference
python prompt_optimize.py --api_key "Zhipu AI API Key" --prompt {your prompt} --base_url "https://open.bigmodel.cn/api/paas/v4" --model "glm-4-plus" --cogview_version "cogview4"
```

### 推理模型

以 `BF16` 精度运行 `CogView4-6B` 模型：

```python
from diffusers import CogView4Pipeline
import torch

pipe = CogView4Pipeline.from_pretrained("THUDM/CogView4-6B", torch_dtype=torch.bfloat16).to("cuda")

# Open it for reduce GPU memory usage
pipe.enable_model_cpu_offload()
pipe.vae.enable_slicing()
pipe.vae.enable_tiling()

prompt = "A vibrant cherry red sports car sits proudly under the gleaming sun, its polished exterior smooth and flawless, casting a mirror-like reflection. The car features a low, aerodynamic body, angular headlights that gaze forward like predatory eyes, and a set of black, high-gloss racing rims that contrast starkly with the red. A subtle hint of chrome embellishes the grille and exhaust, while the tinted windows suggest a luxurious and private interior. The scene conveys a sense of speed and elegance, the car appearing as if it's about to burst into a sprint along a coastal road, with the ocean's azure waves crashing in the background."
image = pipe(
    prompt=prompt,
    guidance_scale=3.5,
    num_images_per_prompt=1,
    num_inference_steps=50,
    width=1024,
    height=1024,
).images[0]

image.save("cogview4.png")
```

更多推理代码请查看：

1. 使用 `BNB int4` 加载 `text encoder` 以及完整的推理代码注释，
   请看[这里](inference/cli_demo_cogview4.py)。
2. 使用 `TorchAO int8 or int4` 加载 `text encoder & transformer` 以及完整的推理代码注释，
   请看[这里](inference/cli_demo_cogview4_int8.py)。
3. 搭建 `gradio` 图形界面 DEMO，请看[这里](inference/gradio_web_demo.py)。


## 微调

本仓库不包含微调代码，但你可以通过以下两种途径进行微调，包括 LoRA 与 SFT：

1. [CogKit](https://github.com/THUDM/CogKit)，我们官方维护的系统级微调框架，支持 CogView4 与 CogVideoX。
2. [finetrainers](https://github.com/a-r-r-o-w/finetrainers)，一个低显存解决方案，可在单张 RTX 4090 上完成微调。
3. 如果你想直接训练 ControlNet 模型，可以参考这份[训练代码](https://github.com/huggingface/diffusers/tree/main/examples/cogview4-control)来训练你自己的模型。

## 许可证

本仓库中的代码与 CogView3 模型依据 [Apache 2.0](./LICENSE) 许可证授权。

我们欢迎并感谢你的代码贡献。贡献指南请查看
[这里](resources/contribute.md)。

---
title: "GLM-Image 模型卡"
source: https://huggingface.co/zai-org/GLM-Image
crawled: 2026-09-22
title_en: "zai-org/GLM-Image model card"
translated: 2026-09-22
---

---
license: mit
language:
- zh
- en
library_name: diffusers
pipeline_tag: text-to-image
---

# GLM-Image 模型卡

> 原文：[zai-org/GLM-Image model card](https://huggingface.co/zai-org/GLM-Image) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/resources/logo.svg width="40%"/>
</div>
<p align="center">
    👋 欢迎加入我们的<a href="https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/resources/wechat.png" target="_blank">微信</a>与 <a href="https://discord.gg/8KFjEec7" target="_blank">Discord</a> 社区
    <br>
    📖 了解 GLM-Image 的<a href="https://z.ai/blog/glm-image" target="_blank">技术博客</a>与 <a href="https://github.com/zai-org/GLM-Image" target="_blank">Github</a>
    <br>
    📍 使用 GLM-Image 的 <a href="https://docs.z.ai/guides/image/glm-image" target="_blank">API</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/resources/show_case.jpeg" alt="show_case" width="100%" />
</p>

## 简介

GLM-Image 是一个采用自回归 + 扩散解码器混合架构的图像生成模型。在一般图像生成质量上，GLM-Image 与主流潜在扩散方法相当，但在文本渲染与知识密集型生成场景中展现出显著优势。它在需要精确语义理解和复杂信息表达的任务中表现出色，同时在高保真与细粒度细节生成方面保持强劲能力。除文生图之外，GLM-Image 还支持丰富的图生图任务，包括图像编辑、风格迁移、保持身份的生成以及多主体一致性。

模型架构：自回归 + 扩散解码器的混合设计。

<p align="center">
  <img src="https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/resources/architecture_1.jpeg" alt="architecture_1" width="100%" />
</p>

+ 自回归生成器：一个 9B 参数模型，由 [GLM-4-9B-0414](https://huggingface.co/zai-org/GLM-4-9B-0414) 初始化，扩充了词表以纳入视觉 token。模型首先生成约 256 个 token 的紧凑编码，随后扩展到 1K–4K 个 token，对应 1K–2K 的高分辨率图像输出。
+ 扩散解码器：一个 7B 参数的解码器，采用单流 DiT 架构进行潜在空间图像解码。它配备 Glyph Encoder 文本模块，显著提升了图像内文字的准确渲染。

<p align="center">
  <img src="https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/resources/architecture_2.jpeg" alt="architecture_2" width="70%" />
</p>

采用解耦强化学习的后训练：模型引入了基于 GRPO 算法的细粒度、模块化反馈策略，大幅增强了语义理解与视觉细节质量。

+ 自回归模块：提供聚焦美学与语义对齐的低频反馈信号，提升指令遵循能力与艺术表现力。
+ 解码器模块：提供针对细节保真度与文字准确性的高频反馈，带来高度真实的纹理以及更精确的文字渲染。

GLM-Image 在单一模型内同时支持文生图与图生图生成。

+ 文生图：从文本描述生成高细节图像，在信息密集场景中表现尤为出色。
+ 图生图：支持广泛的任务，包括图像编辑、风格迁移、多主体一致性，以及面向人物和物体的保持身份生成。

> 你可以在 [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm_image) 和 [diffusers](https://github.com/huggingface/diffusers/tree/main/src/diffusers/pipelines/glm_image) 库中找到完整的 GLM-Image 模型实现。

## 效果展示

### 密集文本与知识型 T2I

<p align="center">
  <img src="https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/resources/show_case_t2i.jpeg" alt="show_case_t2i" width="100%" />
</p>

### I2I

<p align="center">
  <img src="https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/resources/show_case_i2i.jpeg" alt="show_case_i2i" width="100%" />
</p>

## 快速开始

### transformers + diffusers 管线

从源码安装 transformers 与 diffusers：

```shell
pip install git+https://github.com/huggingface/transformers.git
pip install git+https://github.com/huggingface/diffusers.git
```

+ 文生图

```python
import torch
from diffusers.pipelines.glm_image import GlmImagePipeline

pipe = GlmImagePipeline.from_pretrained("zai-org/GLM-Image", torch_dtype=torch.bfloat16, device_map="cuda")
prompt = "A beautifully designed modern food magazine style dessert recipe illustration, themed around a raspberry mousse cake. The overall layout is clean and bright, divided into four main areas: the top left features a bold black title 'Raspberry Mousse Cake Recipe Guide', with a soft-lit close-up photo of the finished cake on the right, showcasing a light pink cake adorned with fresh raspberries and mint leaves; the bottom left contains an ingredient list section, titled 'Ingredients' in a simple font, listing 'Flour 150g', 'Eggs 3', 'Sugar 120g', 'Raspberry puree 200g', 'Gelatin sheets 10g', 'Whipping cream 300ml', and 'Fresh raspberries', each accompanied by minimalist line icons (like a flour bag, eggs, sugar jar, etc.); the bottom right displays four equally sized step boxes, each containing high-definition macro photos and corresponding instructions, arranged from top to bottom as follows: Step 1 shows a whisk whipping white foam (with the instruction 'Whip egg whites to stiff peaks'), Step 2 shows a red-and-white mixture being folded with a spatula (with the instruction 'Gently fold in the puree and batter'), Step 3 shows pink liquid being poured into a round mold (with the instruction 'Pour into mold and chill for 4 hours'), Step 4 shows the finished cake decorated with raspberries and mint leaves (with the instruction 'Decorate with raspberries and mint'); a light brown information bar runs along the bottom edge, with icons on the left representing 'Preparation time: 30 minutes', 'Cooking time: 20 minutes', and 'Servings: 8'. The overall color scheme is dominated by creamy white and light pink, with a subtle paper texture in the background, featuring compact and orderly text and image layout with clear information hierarchy."
image = pipe(
    prompt=prompt,
    height=32 * 32,
    width=36 * 32,
    num_inference_steps=50,
    guidance_scale=1.5,
    generator=torch.Generator(device="cuda").manual_seed(42),
).images[0]

image.save("output_t2i.png")
```

+ 图生图

```python
import torch
from diffusers.pipelines.glm_image import GlmImagePipeline
from PIL import Image

pipe = GlmImagePipeline.from_pretrained("zai-org/GLM-Image", torch_dtype=torch.bfloat16, device_map="cuda")
image_path = "cond.jpg"
prompt = "Replace the background of the snow forest with an underground station featuring an automatic escalator."
image = Image.open(image_path).convert("RGB")
image = pipe(
    prompt=prompt,
    image=[image],  # can input multiple images for multi-image-to-image generation such as [image, image1]
    height=33 * 32, # Must set height even it is same as input image
    width=32 * 32, # Must set width even it is same as input image
    num_inference_steps=50,
    guidance_scale=1.5,
    generator=torch.Generator(device="cuda").manual_seed(42),
).images[0]

image.save("output_i2i.png")
```

### SGLang 管线

从源码安装 transformers 与 diffusers：

```
pip install "sglang[diffusion] @ git+https://github.com/sgl-project/sglang.git#subdirectory=python"
pip install git+https://github.com/huggingface/transformers.git
pip install git+https://github.com/huggingface/diffusers.git
```

+ 文生图

```
sglang serve --model-path zai-org/GLM-Image

curl http://localhost:30000/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "zai-org/GLM-Image",
    "prompt": "a beautiful girl with glasses.",
    "n": 1,
    "response_format": "b64_json",
    "size": "1024x1024"
  }' |  python3 -c "import sys, json, base64; open('output_t2i.png', 'wb').write(base64.b64decode(json.load(sys.stdin)['data'][0]['b64_json']))"
```

+ 图生图

```
sglang serve --model-path zai-org/GLM-Image

curl -s -X POST "http://localhost:30000/v1/images/edits" \
-F "model=zai-org/GLM-Image" \
-F "image=@cond.jpg" \
-F "prompt=Replace the background of the snow forest with an underground station featuring an automatic escalator." \
-F "response_format=b64_json"  | python3 -c "import sys, json, base64; open('output_i2i.png', 'wb').write(base64.b64decode(json.load(sys.stdin)['data'][0]['b64_json']))"
```

### 注意事项

+ 请确保所有希望渲染到图像中的文字在模型输入中用引号括起来。我们强烈建议使用 GLM-4.7 来增强提示词，以获得更高的图像质量。详情请查看[我们的 github 脚本](https://raw.githubusercontent.com/zai-org/GLM-Image/refs/heads/main/examples/prompt_utils.py)。
+ GLM-Image 中使用的 AR 模型默认配置为 `do_sample=True`、temperature 为 `0.9`、topp 为 `0.75`。更高的 temperature 会带来更多样、更丰富的输出，但也可能导致输出稳定性有一定下降。
+ 目标图像分辨率必须能被 32 整除，否则会抛出错误。
+ 由于该架构的推理优化目前仍有限，运行开销依然较高。你可以设置 `enable_model_cpu_offload=True`，以约 `23GB` 显存运行，代价是推理速度变慢。
+ vLLM-Omni 与 SGLang（含 AR 加速）的支持正在集成中——敬请期待。关于推理成本，可以在我们的 github 上查看。

## 模型性能

### 文本渲染

<div style="overflow-x: auto; margin-bottom: 16px;">
  <table style="border-collapse: collapse; width: 100%;">
    <thead>
      <tr>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa;" rowspan="2">模型</th>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa;" rowspan="2">开源</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;" colspan="3">CVTG-2K</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;" colspan="3">LongText-Bench</th>
      </tr>
      <tr>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">词准确率</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">NED</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">CLIPScore</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">平均</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">EN</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">ZH</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">Seedream 4.5</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8990</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.9483</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.8069</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.988</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.989</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.987</strong></td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">Seedream 4.0</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8451</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.9224</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.7975</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.924</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.921</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.926</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">Nano Banana 2.0</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.7788</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8754</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.7372</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.965</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.981</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.949</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">GPT Image 1 [High]</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8569</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.9478</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.7982</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.788</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.956</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.619</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">Qwen-Image</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8288</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.9116</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8017</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.945</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.943</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.946</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">Qwen-Image-2512</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8604</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.9290</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.7819</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.961</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.956</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.965</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">Z-Image</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8671</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.9367</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.7969</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.936</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.935</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.936</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;">Z-Image-Turbo</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8585</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.9281</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.8048</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.922</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.917</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.926</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de;white-space:nowrap;"><strong>GLM-Image</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.9116</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.9557</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.7877</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.966</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.952</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.979</td>
      </tr>
    </tbody>
  </table>
</div>

### 文生图

<div style="overflow-x: auto; margin-bottom: 16px;">
  <table style="border-collapse: collapse; width: 100%;">
    <thead>
      <tr>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa;" rowspan="2">模型</th>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa;" rowspan="2">开源</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;" colspan="2">OneIG-Bench</th>
        <th style="padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;" colspan="2">TIIF-Bench</th>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa;" rowspan="2">DPG-Bench</th>
      </tr>
      <tr>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">EN</th>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">ZH</th>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">短</th>
        <th style="white-space: nowrap; padding: 8px; border: 1px solid #d0d7de; background-color: #f6f8fa; text-align: center;">长</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Seedream 4.5</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.576</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.551</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">90.49</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>88.52</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>88.63</strong></td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Seedream 4.0</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.576</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.553</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">90.45</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">88.08</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">88.54</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Nano Banana 2.0</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.578</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>0.567</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;"><strong>91.00</strong></td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">88.26</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">87.16</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">GPT Image 1 [High]</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.533</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.474</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">89.15</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">88.29</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">85.15</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">DALL-E 3</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✗</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">74.96</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">70.81</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">83.50</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Qwen-Image</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.539</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.548</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">86.14</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">86.83</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">88.32</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Qwen-Image-2512</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.530</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.515</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">83.24</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">84.93</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">87.20</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Z-Image</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.546</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.535</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">80.20</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">83.01</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">88.14</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Z-Image-Turbo</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.528</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.507</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">77.73</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">80.05</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">84.86</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">FLUX.1 [Dev]</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.434</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">71.09</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">71.78</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">83.52</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">SD3 Medium</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">67.46</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">66.09</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">84.08</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">SD XL</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.316</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">54.96</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">42.13</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">74.65</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">BAGEL</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.361</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.370</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">71.50</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">71.70</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Janus-Pro</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.267</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.240</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">66.50</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">65.01</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">84.19</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;">Show-o2</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.308</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">59.72</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">58.86</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">-</td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d7de; white-space:nowrap;font-weight:bold;">GLM-Image</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✓</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.528</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">0.511</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">81.01</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">81.02</td>
        <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">84.78</td>
      </tr>
    </tbody>
  </table>
</div>


## 许可证

GLM-Image 整体模型依据 MIT 许可证发布。

本项目纳入了来自 [X-Omni/X-Omni-En](huggingface.co/X-Omni/X-Omni-En) 的 VQ tokenizer 权重与 VIT 权重，它们依据 Apache License, Version 2.0 许可。

VQ tokenizer 与 VIT 权重仍受原始 Apache-2.0 条款约束。用户在使用该组件时应遵守相应许可证。

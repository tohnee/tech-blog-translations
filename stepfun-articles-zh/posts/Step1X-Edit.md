---
title: "Step1X-Edit：面向通用图像编辑的实用框架"
title_en: "stepfun-ai/Step1X-Edit"
source: https://github.com/stepfun-ai/Step1X-Edit/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Step1X-Edit：面向通用图像编辑的实用框架

> 原文：[stepfun-ai/Step1X-Edit](https://github.com/stepfun-ai/Step1X-Edit/blob/main/README.md) · 阶跃星辰 StepFun

<div align="center">
  <img src="assets/logo.png"  height=100>
</div>
<div align="center">
  <a href="https://step1x-edit.github.io/"><img src="https://img.shields.io/static/v1?label=Project%20Page&message=Web&color=green"></a> &ensp;
  <a href="https://arxiv.org/abs/2504.17761"><img src="https://img.shields.io/static/v1?label=Step1X-Edit&message=Arxiv&color=red"></a> &ensp;
  <a href="https://arxiv.org/abs/2511.22625"><img src="https://img.shields.io/static/v1?label=ReasonEdit&message=Arxiv&color=red"></a> &ensp;
  <a href="assets/WeChat.jpg">
  <img src="https://img.shields.io/static/v1?label=WeChat&message=Add%20Me&color=green&logo=wechat&logoColor=white">
  </a>
  
  <a href="https://huggingface.co/stepfun-ai/Step1X-Edit"><img src="https://img.shields.io/static/v1?label=Model&message=HuggingFace&color=yellow"></a> &ensp;
  <a href="https://huggingface.co/datasets/stepfun-ai/GEdit-Bench"><img src="https://img.shields.io/static/v1?label=GEdit-Bench&message=HuggingFace&color=yellow"></a> &ensp;
  [![Run on Replicate](https://replicate.com/zsxkib/step1x-edit/badge)](https://replicate.com/zsxkib/step1x-edit) &ensp;
  <a href="https://discord.gg/j3qzuAyn"><img src="https://img.shields.io/static/v1?label=Discord%20Channel&message=Discord&color=purple"></a> &ensp;
</div>


## 🔥🔥🔥 新闻！
* 2026 年 4 月 29 日：🎉 Step Image Edit 2 现已上线——一个为超快响应与高质量输出设计的轻量级模型，带来实时交互式创作体验。它可以在 2 秒内完成图像生成与编辑任务。欢迎试用并分享你的反馈 ✨✨✨

  在此体验（StepFun 开放平台）：[https://platform.stepfun.com/docs/zh/guides/models/step-image-edit-2](https://platform.stepfun.com/docs/zh/guides/models/step-image-edit-2)

  API 文档：[https://platform.stepfun.com/docs/zh/step-plan/integrations/image-api](https://platform.stepfun.com/docs/zh/step-plan/integrations/image-api)

* 2025 年 12 月 29 日：🎉 [RegionE](https://github.com/Peyton-Chen/RegionE) 为 Step1X-Edit 推理带来 2.5 倍加速且无精度损失，仅需五行代码即可实现。
* 2025 年 11 月 26 日：👋 我们发布了 [Step1X-Edit-v1p2](https://huggingface.co/stepfun-ai/Step1X-Edit-v1p2)（论文中称为 **ReasonEdit-S**），一个原生推理编辑模型，在 KRIS-Bench 与 GEdit-Bench 上表现更好。技术报告见[这里](https://arxiv.org/abs/2511.22625)。
  <table>
  <thead>
  <tr>
    <th rowspan="2">模型</th>
    <th colspan="3"> <div align="center">GEdit-Bench</div> </th>
    <th colspan="4"> <div align="center">Kris-Bench</div> </th>
  </tr>
  <tr>
    <th>G_SC⬆️</th> <th>G_PQ⬆️ </th> <th>G_O⬆️</th> <th>FK⬆️</th> <th>CK⬆️</th> <th>PK⬆️ </th> <th>Overall⬆️</th>
  </tr>
  </thead>
  <tbody>
  <tr>  
    <td>Flux-Kontext-dev </td> <td>7.16</td> <td>7.37</td> <td>6.51</td> <td>53.28</td> <td>50.36</td> <td>42.53</td> <td>49.54</td>
  </tr>
  <tr>   
    <td>Qwen-Image-Edit-2509 </td> <td>8.00</td> <td>7.86</td> <td>7.56</td> <td>61.47</td> <td>56.79</td> <td>47.07</td> <td>56.15</td>
  </tr>
  <tr>
    <td>Step1X-Edit v1.1 </td> <td>7.66</td> <td>7.35</td> <td>6.97</td> <td>53.05</td> <td>54.34</td> <td>44.66</td> <td>51.59</td>
  </tr>
  <tr>
    <td>Step1x-edit-v1p2-preview </td> <td>8.14</td> <td>7.55</td> <td>7.42</td> <td>60.49</td> <td>58.81</td> <td>41.77</td> <td>52.51</td>
  </tr>
  <tr>
    <td>Step1x-edit-v1p2 (base) </td> <td>7.77</td> <td>7.65</td> <td>7.24</td> <td>58.23</td> <td>60.55</td> <td>46.21</td> <td>56.33</td>
  </tr>
  <tr>
    <td>Step1x-edit-v1p2 (thinking) </td> <td>8.02</td> <td>7.64</td> <td>7.36</td> <td>59.79</td> <td>62.76</td> <td>49.78</td> <td>58.64</td>
  </tr>
  <tr>
    <td>Step1x-edit-v1p2 (thinking + reflection) </td> <td>8.18</td> <td>7.85</td> <td>7.58</td> <td>62.44</td> <td>65.72</td> <td>50.42</td> <td>60.93</td>
  </tr>
  </table>

* 2025 年 9 月 8 日：👋 我们发布了 [step1x-edit-v1p2-preview](https://huggingface.co/stepfun-ai/Step1X-Edit-v1p2-preview)，这是具备推理编辑能力、性能更佳的 Step1X-Edit 新版本（报告即将发布），特点包括：
  - 原生推理编辑模型：将指令推理与反思式修正结合，更准确地处理复杂编辑。在 KRIS-Bench 上的表现：
    |    模型    |   事实性知识 ⬆️   |  概念性知识 ⬆️ | 程序性知识 ⬆️   |  总分 ⬆️ | 
    |:------------:|:------------:|:------------:| :------------:|:------------:| 
    | Step1X-Edit v1.1  | 53.05 |  54.34 | 44.66 | 51.59 |   
    | Step1x-edit-v1p2-preview  | 60.49 | 58.81 | 41.77 | 52.51 | 
    | Step1x-edit-v1p2-preview (thinking)  | 62.24 | 62.25 | 44.43 | 55.21| 
    | Step1x-edit-v1p2-preview (thinking + reflection) | 62.94 |  61.82 |  44.08 |  55.64 | 
  - 更优的图像编辑质量与更好的指令遵循表现。在 GEdit-Bench 上的表现：
    |     模型    |     G_SC ⬆️   |  G_PQ ⬆️ | G_O ⬆️   |  Q_SC ⬆️ | Q_PQ ⬆️   |  Q_O ⬆️ |
    |:------------:|:------------:|:------------:| :------------:|:------------:| :------------:|:------------:|
    | Step1X-Edit (v1.0)  |    7.13   | 7.00 |   6.44   | 7.39 |    7.28   | 7.07 | 
    | Step1X-Edit (v1.1)  |    7.66   | 7.35 |   6.97   | 7.65 |    7.41   | 7.35 | 
    | Step1x-edit-v1p2-preview  |    8.14   | 7.55 |   7.42   | 7.90 |   7.34   | 7.40   |
* 2025 年 7 月 9 日：👋 我们更新了 step1x-edit 模型并发布为 [step1x-edit-v1p1](https://huggingface.co/stepfun-ai/Step1X-Edit)（diffusers 版本见[这里](https://huggingface.co/stepfun-ai/Step1X-Edit-v1p1-diffusers)），特点包括：
  - 新增对文生图（T2I）生成任务的支持
  - 更优的图像编辑质量与更好的指令遵循表现。
  在 GEdit-Bench-EN（完整集）上的定量评测。G_SC、G_PQ、G_O 指由 GPT-4.1 评测的指标，Q_SC、Q_PQ、Q_O 指由 Qwen2.5-VL-72B 评测的指标。为便于复现，我们发布了模型评测的[中间结果](https://huggingface.co/datasets/Shiyu95/gedit_results)。
    |     模型    |     G_SC ⬆️   |  G_PQ ⬆️ | G_O ⬆️   |  Q_SC ⬆️ | Q_PQ ⬆️   |  Q_O ⬆️ |
    |:------------:|:------------:|:------------:| :------------:|:------------:| :------------:|:------------:|
    | Step1X-Edit (v1.0)  |    7.13   | 7.00 |   6.44   | 7.39 |    7.28   | 7.07 | 
    | Step1X-Edit (v1.1)  |    7.66   | 7.35 |   6.97   | 7.65 |    7.41   | 7.35 | 
* 2025 年 6 月 17 日：👋 新增 TeaCache 与并行推理支持。
* 2025 年 5 月 22 日：👋 Step1X-Edit 现在支持在单张 24GB GPU 上进行 Lora 微调！同时发布了一个用于修复动漫角色手部的 Lora。[下载 Lora](https://huggingface.co/stepfun-ai/Step1X-Edit)
* 2025 年 4 月 30 日：🎉 Step1X-Edit ComfyUI 插件现已可用，感谢社区贡献！[quank123wip/ComfyUI-Step1X-Edit](https://github.com/quank123wip/ComfyUI-Step1X-Edit) 与 [raykindle/ComfyUI_Step1X-Edit](https://github.com/raykindle/ComfyUI_Step1X-Edit)。
* 2025 年 4 月 27 日：🎉 在社区支持下，我们更新了 Step1X-Edit-FP8 的推理代码与模型权重。[meimeilook/Step1X-Edit-FP8](https://huggingface.co/meimeilook/Step1X-Edit-FP8) 与 [rkfg/Step1X-Edit-FP8](https://huggingface.co/rkfg/Step1X-Edit-FP8)。
* 2025 年 4 月 26 日：🎉 Step1X-Edit 现已上线——你可以在在线演示中直接编辑图像！[在线演示](https://huggingface.co/spaces/stepfun-ai/Step1X-Edit)
* 2025 年 4 月 25 日：👋 我们发布了 Step1X-Edit 的评测代码与基准数据。[下载 GEdit-Bench](https://huggingface.co/datasets/stepfun-ai/GEdit-Bench)
* 2025 年 4 月 25 日：👋 我们发布了 Step1X-Edit 的推理代码与模型权重。[ModelScope](https://www.modelscope.cn/models/stepfun-ai/Step1X-Edit) 与 [HuggingFace](https://huggingface.co/stepfun-ai/Step1X-Edit) 模型。
* 2025 年 4 月 25 日：👋 我们开源了技术报告。[阅读](https://arxiv.org/abs/2504.17761)

<!-- ## Image Edit Demos -->


<!-- ## 📑 Open-source Plan
- [x] Inference & Checkpoints
- [x] Online demo (Gradio)
- [x] Fine-tuning scripts
- [x] Multi-gpus Sequence Parallel inference
- [x] FP8 Quantified weight
- [x] ComfyUI
- [x] Diffusers -->



## 📖 简介
我们提出最先进的图像编辑模型 **Step1X-Edit**，旨在提供与 GPT-4o、Gemini2 Flash 等闭源模型相当的性能。
具体而言，我们采用多模态 LLM 处理参考图像与用户的编辑指令，提取潜空间嵌入并与扩散图像解码器结合以得到目标图像。为训练该模型，我们构建了用于产出高质量数据集的数据生成流水线。
在评测方面，我们开发了 GEdit-Bench，一个植根于真实用户指令的新基准。在 GEdit-Bench 上的实验结果表明，Step1X-Edit 以显著优势超越现有开源基线，并逼近领先专有模型的性能，为图像编辑领域做出了重要贡献。
更多细节请参阅我们的[技术报告](https://arxiv.org/abs/2504.17761)。

<div align="center">
<img width="720" alt="demo" src="assets/image_edit_demo.gif">
<p><b>Step1X-Edit：</b>一个统一的图像编辑模型，在各类真实用户指令上表现出色。 </p>
</div>


## ⚡️ 快速开始
1. 确保你的 `transformers==4.55.0`（我们在该版本上测试）
2. 根据你想使用的模型版本，在本地安装对应的 `diffusers` 包


### Step1X-Edit-v1p2 (v1.2)
通过以下命令安装 `diffusers` 包：
```bash
git clone -b step1xedit_v1p2 https://github.com/Peyton-Chen/diffusers.git
cd diffusers
pip install -e .

pip install RegionE # optional, for faster inference
```
以下是使用 `Step1X-Edit-v1p2` 模型编辑图像的示例：
```python
import torch
from diffusers import Step1XEditPipelineV1P2
from diffusers.utils import load_image
from RegionE import RegionEHelper

pipe = Step1XEditPipelineV1P2.from_pretrained("stepfun-ai/Step1X-Edit-v1p2", torch_dtype=torch.bfloat16)
pipe.to("cuda")

# Import the RegionEHelper
regionehelper = RegionEHelper(pipe)
regionehelper.set_params()   # default hyperparameter
regionehelper.enable()

print("=== processing image ===")
image = load_image("examples/0000.jpg").convert("RGB")
prompt = "add a ruby pendant on the girl's neck."
enable_thinking_mode=True
enable_reflection_mode=True
pipe_output = pipe(
    image=image,
    prompt=prompt,
    num_inference_steps=50,
    true_cfg_scale=6,
    generator=torch.Generator().manual_seed(42),
    enable_thinking_mode=enable_thinking_mode,
    enable_reflection_mode=enable_reflection_mode,
)
if enable_thinking_mode:
    print("Reformat Prompt:", pipe_output.reformat_prompt)
for image_idx in range(len(pipe_output.images)):
    pipe_output.images[image_idx].save(f"0001-{image_idx}.jpg", lossless=True)
    if enable_reflection_mode:
        print(pipe_output.think_info[image_idx])
        print(pipe_output.best_info[image_idx])
pipe_output.final_images[0].save(f"0001-final.jpg", lossless=True)

regionehelper.disable()
```
结果如下所示：
<div align="center">
<img width="1080" alt="results" src="assets/v1p2_vis.jpeg">
</div>

### Step1X-Edit-v1p2-preview (v1.2-preview)
通过以下命令安装 `diffusers` 包：
```bash
git clone -b dev/MergeV1-2 https://github.com/Peyton-Chen/diffusers.git
cd diffusers
pip install -e .
```

以下是使用 `Step1X-Edit-v1p2-preview` 模型编辑图像的示例：

```python
import torch
from diffusers import Step1XEditPipelineV1P2
from diffusers.utils import load_image
pipe = Step1XEditPipelineV1P2.from_pretrained("stepfun-ai/Step1X-Edit-v1p2-preview", torch_dtype=torch.bfloat16)
pipe.to("cuda")
print("=== processing image ===")
image = load_image("examples/0000.jpg").convert("RGB")
prompt = "add a ruby ​​pendant on the girl's neck."
enable_thinking_mode=True
enable_reflection_mode=True
pipe_output = pipe(
    image=image,
    prompt=prompt,
    num_inference_steps=28,
    true_cfg_scale=4,
    generator=torch.Generator().manual_seed(42),
    enable_thinking_mode=enable_thinking_mode,
    enable_reflection_mode=enable_reflection_mode,
)
if enable_thinking_mode:
    print("Reformat Prompt:", pipe_output.reformat_prompt)
for image_idx in range(len(pipe_output.images)):
    pipe_output.images[image_idx].save(f"0001-{image_idx}.jpg", lossless=True)
    if enable_reflection_mode:
        print(pipe_output.think_info[image_idx])
```


### Step1X-Edit-v1p1 (v1.1)
通过以下命令安装 `diffusers` 包：
```bash
git clone -b step1xedit https://github.com/Peyton-Chen/diffusers.git
cd diffusers
pip install -e .
```

以下是使用 `Step1X-Edit-v1p1` 模型编辑图像的示例：
```python
import torch
from diffusers import Step1XEditPipeline
from diffusers.utils import load_image


pipe = Step1XEditPipeline.from_pretrained("stepfun-ai/Step1X-Edit-v1p1-diffusers", torch_dtype=torch.bfloat16)
pipe.to("cuda")

print("=== processing image ===")
image = load_image("examples/0000.jpg").convert("RGB")
prompt = "给这个女生的脖子上戴一个带有红宝石的吊坠。"
image = pipe(
    image=image,
    prompt=prompt,
    num_inference_steps=28,
    size_level=1024,
    guidance_scale=6.0,
    generator=torch.Generator().manual_seed(42),
).images[0]
image.save("0000.jpg")
```

结果如下所示：
<div align="center">
<img width="1080" alt="results" src="assets/results_show.png">
</div>


## 🌟 进阶用法
我们以原版 [Step1X-Edit](https://huggingface.co/stepfun-ai/Step1X-Edit) 模型为例，演示模型的一些进阶用法。其他版本的模型推理流程可能不同。

### A1. 环境要求
我们使用 torch==2.3.1 与 torch==2.5.1、cuda-12.1 测试了模型。
安装依赖：

``` bash
pip install -r requirements.txt
```

安装 [`flash-attn`](https://github.com/Dao-AILab/flash-attention)，这里提供一个脚本帮助你找到适合系统的预编译 wheel。

```bash
python scripts/get_flash_attn.py
```

该脚本会生成形如 `flash_attn-2.7.2.post1+cu12torch2.5cxx11abiFALSE-cp310-cp310-linux_x86_64.whl` 的 wheel 名称，可在 [flash-attn 的 release 页面](https://github.com/Dao-AILab/flash-attention/releases)找到。

然后你可以下载对应的预编译 wheel，按 [`flash-attn`](https://github.com/Dao-AILab/flash-attention) 的说明安装。



### A2. 降低 GPU 显存占用
你可以使用以下脚本以更低的 GPU 显存占用编辑图像。

```
bash scripts/run_examples.sh
```
默认脚本以非量化权重运行推理代码。如果想节省 GPU 显存，你可以 1) 在脚本中设置 `--quantized` 标志，将权重量化为 fp8；或 2) 设置 `--offload` 标志，将部分模块卸载到 CPU。

下表展示了不同配置下运行 Step1X-Edit 模型（batch size = 1，带 cfg）的 GPU 显存占用与速度：

|     模型    |     峰值 GPU 显存 (512 / 786 / 1024)  | 28 步（带 flash-attn，512 / 786 / 1024） |
|:------------:|:------------:|:------------:|
| Step1X-Edit   |                42.5GB / 46.5GB / 49.8GB  | 5s / 11s / 22s |
| Step1X-Edit (FP8)   |             31GB / 31.5GB / 34GB     | 6.8s / 13.5s / 25s | 
| Step1X-Edit (offload)   |       25.9GB / 27.3GB / 29.1GB | 49.6s / 54.1s / 63.2s |
| Step1X-Edit (FP8 + offload)   |   18GB / 18GB / 18GB | 35s / 40s / 51s |

* 模型已在一张 H800 GPU 上测试。
* 我们推荐使用 80GB 显存的 GPU，以获得更好的生成质量与效率。


### A3. 多 GPU 推理
多 GPU 推理可使用以下脚本：
```
bash scripts/run_examples_parallel.sh
```
你可以在脚本中更改 GPU 数量（`GPU`）、xDiT 的配置（`--ulysses_degree`、`--ring_degree` 或 `--cfg_degree`），以及是否启用 TeaCache 加速（`--teacache`）。
下表展示了若干高效方法在 Step1X-Edit 模型上的加速效果。

|     模型    |     峰值 GPU 显存   |  28 步 |
|:------------:|:------------:|:------------:|
| Step1X-Edit + TeaCache     |    49.6GB   | 16.78s | 
| Step1X-Edit + xDiT (GPU=2) |    50.2GB   | 12.81s |
| Step1X-Edit + xDiT (GPU=4) |    52.9GB   | 8.17s |
| Step1X-Edit + TeaCache + xDiT (GPU=2)  |  50.7GB    | 8.94s |
| Step1X-Edit + TeaCache + xDiT (GPU=4)  |  54.2GB |  5.82s |

* 模型在 H800 系列 GPU 上以 1024 分辨率测试。
* TeaCache 默认阈值 0.2 在效率与性能之间提供了良好平衡。
* 使用 4 张 GPU 时，xDiT 同时采用 CFG 并行与 Ring Attention；使用 2 张 GPU 时仅使用 CFG 并行。

默认脚本在示例输入上运行推理代码。结果如下所示：
<div align="center">
<img width="1080" alt="results" src="assets/efficient_teasar.png">
</div>


<!-- ### 2.4 Gradio Scripts

Change the `model_path` in `gradio_app.py` to the local path of Step1X-Edit. Then run

```bash
python gradio_app.py
```

Then the gradio demo will run on `localhost:32800`. -->






### A4. 微调
#### Lora 训练脚本

以下是 lora rank 为 64、batch size 为 1 时训练的 GPU 显存开销：

|     DiT 精度    |     bf16 (512 / 786 / 1024)  | fp8 (512 / 786 / 1024) |
|:------------:|:------------:|:------------:|
| GPU 显存   |                29.7GB / 31.6GB / 33.8GB  | 19.8GB / 21.3GB / 23.6GB |

脚本 `./scripts/finetuning.sh` 展示了如何微调 Step1X-Edit 模型。按照我们的默认策略，可以在单张 24GB GPU 上以 1024 分辨率微调 Step1X-Edit。我们的微调脚本改编自 [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts)。

```bash
bash ./scripts/finetuning.sh
```

自定义数据集由 `./library/data_configs/step1x_edit.toml` 组织。其中 `metadata_file` 包含所有训练样本，包括源图像的绝对路径、目标图像的绝对路径以及指令。

`metadata_file` 应为包含如下字典的 json 文件：

```
{
  <target image path, str>: {
    'ref_image_path': <source image path, str>
    'caption': <the editing instruction, str>
  }, 
  ...
}
```

#### 使用 Lora 推理
要使用 Lora 推理，只需在使用 `inference.py` 时加上 `--lora <path to your lora weights>`。例如：

```bash
python inference.py --input_dir ./examples \
    --model_path /data/work_dir/step1x-edit/ \
    --json_path ./examples/prompt_cn.json \
    --output_dir ./output_cn \
    --seed 1234 --size_level 1024 \
    --lora 20250521_001-lora256-alpha128-fix-hand-per-epoch/step1x-edit_test.safetensors
```

这里是一个我们[预训练 Lora 权重](https://huggingface.co/stepfun-ai/Step1X-Edit/tree/main/lora)的示例，它专为修复动漫角色残缺的手部而设计。

<div align="center">
<img width="1080" alt="results" src="assets/lora_teaser.png">
</div>

要复现上述案例，可以运行以下脚本：
```bash 
bash scripts/run_examples_fix_hand.sh
```


## 📊 基准测试
我们发布 [GEdit-Bench](https://huggingface.co/datasets/stepfun-ai/GEdit-Bench) 作为新基准，它植根于真实使用场景，以支持更真实、更全面的评测。该基准经过精心整理，反映实际的用户编辑需求与广泛的编辑场景，能够对图像编辑模型进行更真实、更全面的评估。
评测流程与相关代码见 [GEdit-Bench/EVAL.md](GEdit-Bench/EVAL.md)。部分基准结果如下所示：
<div align="center">
<img width="1080" alt="results" src="assets/eval_res_en.png">
</div>


## 🧩 社区贡献

如果你在项目中开发/使用 Step1X-Edit，欢迎告诉我们 🎉。

- Step1X-Edit 的详细介绍博客：[Step1X-Edit执行流程](https://liwenju0.com/posts/Step1X-Edit%E6%89%A7%E8%A1%8C%E6%B5%81%E7%A8%8B-%E4%B8%80.html)，作者 [liwenju0](https://liwenju0.com/about.html)
- FP8 模型权重：[meimeilook/Step1X-Edit-FP8](https://huggingface.co/meimeilook/Step1X-Edit-FP8)，作者 [meimeilook](https://huggingface.co/meimeilook)；[rkfg/Step1X-Edit-FP8](https://huggingface.co/rkfg/Step1X-Edit-FP8)，作者 [rkfg](https://huggingface.co/rkfg)
- Step1X-Edit ComfyUI 插件：[quank123wip/ComfyUI-Step1X-Edit](https://github.com/quank123wip/ComfyUI-Step1X-Edit)，作者 [quank123wip](https://github.com/quank123wip)；[raykindle/ComfyUI_Step1X-Edit](https://github.com/raykindle/ComfyUI_Step1X-Edit)，作者 [raykindle](https://github.com/raykindle)
- 训练脚本：[hobart07/Step1X-Edit_train](https://github.com/hobart07/Step1X-Edit_train)，作者 [hobart07](https://github.com/hobart07)

## 📚 引用
如果你觉得 Step1X-Edit 系列对你的研究或应用有帮助，请考虑为仓库点 ⭐ 星并引用我们的论文。
```
@article{yin2025reasonedit,
  title={ReasonEdit: Towards Reasoning-Enhanced Image Editing Models}, 
  author={Fukun Yin, Shiyu Liu, Yucheng Han, Zhibo Wang, Peng Xing, Rui Wang, Wei Cheng, Yingming Wang, Aojie Li, Zixin Yin, Pengtao Chen, Xiangyu Zhang, Daxin Jiang, Xianfang Zeng, Gang Yu},
  journal={arXiv preprint arXiv:2511.22625},
  year={2025}
}

@article{wu2025kris,
  title={KRIS-Bench: Benchmarking Next-Level Intelligent Image Editing Models},
  author={Wu, Yongliang and Li, Zonghui and Hu, Xinting and Ye, Xinyu and Zeng, Xianfang and Yu, Gang and Zhu, Wenbo and Schiele, Bernt and Yang, Ming-Hsuan and Yang, Xu},
  journal={arXiv preprint arXiv:2505.16707},
  year={2025}
}

@article{liu2025step1x-edit,
  title={Step1X-Edit: A Practical Framework for General Image Editing}, 
  author={Shiyu Liu and Yucheng Han and Peng Xing and Fukun Yin and Rui Wang and Wei Cheng and Jiaqi Liao and Yingming Wang and Honghao Fu and Chunrui Han and Guopeng Li and Yuang Peng and Quan Sun and Jingwei Wu and Yan Cai and Zheng Ge and Ranchen Ming and Lei Xia and Xianfang Zeng and Yibo Zhu and Binxing Jiao and Xiangyu Zhang and Gang Yu and Daxin Jiang},
  journal={arXiv preprint arXiv:2504.17761},
  year={2025}
}

```

## 致谢
我们向 [Kohya](https://github.com/kohya-ss/sd-scripts/tree/sd3)、[SD3](https://huggingface.co/stabilityai/stable-diffusion-3-medium)、[FLUX](https://github.com/black-forest-labs/flux)、[Qwen](https://github.com/QwenLM/Qwen2.5)、[xDiT](https://github.com/xdit-project/xDiT)、[TeaCache](https://github.com/ali-vilab/TeaCache)、[diffusers](https://github.com/huggingface/diffusers) 与 [HuggingFace](https://huggingface.co) 团队的贡献者致以诚挚感谢，感谢他们的开放研究与探索。


## 免责声明
本图像编辑模型产生的结果完全由用户输入与操作决定。开发团队与本开源项目对使用其产生的任何结果或后果不承担责任。

## 许可证
Step1X-Edit 基于 Apache License 2.0 授权。你可以在相应的 GitHub 与 HuggingFace 仓库中找到许可证文件。

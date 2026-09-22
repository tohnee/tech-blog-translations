---
title: "Ming-flash-omni 2.0：开源全模态 MLLM"
title_en: "inclusionAI/Ming"
source: https://github.com/inclusionAI/Ming/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Ming-flash-omni 2.0：开源全模态 MLLM

> 原文：[inclusionAI/Ming](https://github.com/inclusionAI/Ming/blob/main/README.md) · 蚂蚁集团 InclusionAI

# Ming-flash-omni 2.0

<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_drbxn1/afts/img/YLAgT5MSnLwAAAAAQXAAAAgADkliAQFr/original" width="100"/>
<p>

<p align="center">📑 <a href="https://arxiv.org/abs/2506.09344">技术报告</a>｜🤗 <a href="https://huggingface.co/inclusionAI/Ming-flash-omni-2.0">Hugging Face</a>｜ 🤖 <a href="https://www.modelscope.cn/models/inclusionAI/Ming-flash-omni-2.0">ModelScope</a>



## 简介

新发布的 Ming-flash-omni 2.0 采用 [Ling-2.0](https://github.com/inclusionAI/Ling-V2) 架构——一个拥有 1000 亿总参数、60 亿激活参数的专家混合（MoE）框架。相比前代实现代际跃升，它在开源全模态 MLLM（omni-MLLM）中树立了新的最先进（SOTA）标杆。Ming-flash-omni 2.0 有效地将基础能力与专项领域专长融合。尤其在视觉百科知识、沉浸式语音合成以及高动态图像生成与操控方面表现出色。



<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_xg7bx2/afts/img/c1qcRIb3qH4AAAAAgCAAAAgADhHHAQFr/fmt.avif" width="800"/>
<p>


## 📌 更新
* [2026.02.11] 🔥 我们发布 [Ming-flash-omni 2.0](https://mp.weixin.qq.com/s/hz2fsH1DGpp2zpY-Yngsog) 官方版本，一个突破多模态理解与合成边界的开源 SOTA 全模态 MLLM。
* [2025.10.27] 🔥 我们发布 Ming-flash-omni 的预览版：[Ming-flash-omni Preview](https://github.com/inclusionAI/Ming/tree/main)。
* [2025.07.15] 🔥 我们发布 [Ming-lite-omni v1.5](https://github.com/inclusionAI/Ming/tree/v1.5)，在所有模态上均有显著提升。
* [2025.06.12] 🔥 我们的[技术报告](https://arxiv.org/abs/2506.09344)在 arxiv 上公开。
* [2025.05.28] 🔥 [Ming-lite-omni v1](https://github.com/inclusionAI/Ming/tree/v1.0) 官方版本发布，性能更佳并支持图像生成。
* [2025.05.04] 🔥 我们发布 Ming-lite-omni 的测试版：[Ming-lite-omni-Preview](https://github.com/inclusionAI/Ming/tree/Ming-Lite-Omni-Preview)。


## 关键特性
与 [Ming-flash-omni Preview](https://github.com/inclusionAI/Ming/tree/Ming-flash-omni-Preview) 相比，Ming-flash-omni 2.0 聚焦于优化以下关键领域的能力：
- **专家级多模态认知**：它能准确识别动植物、辨识文化指涉（从地方美食到全球地标），并对文物（包括年代、形制与工艺）给出专家级分析。通过将高分辨率视觉捕获与庞大知识图谱协同，模型实现「视觉到知识」的合成，带来卓越的知识理解。


- **沉浸式、可控的统一声学合成**：Ming-flash-omni 2.0 引入统一的端到端声学生成流水线，将语音、音频与音乐整合到单一通道中。凭借连续自回归（Continuous Autoregression）与 Diffusion Transformer（DiT）头，模型支持零样本语音克隆以及细粒度属性控制（如情绪、音色与环境氛围）。该架构推动从简单的文本转语音迈向极具表现力、富有情感共鸣的沉浸式听觉体验。


- **高动态、可控的图像生成与操控**：Ming-flash-omni 2.0 采用原生多任务架构，统一分割、生成与编辑，实现复杂的时空语义解耦。它擅长高动态内容创作，包括氛围重建、无缝场景合成与上下文感知的物体移除。通过保持纹理连贯性与空间深度一致性，Ming-flash-omni 2.0 在复杂图像操控任务中达到最先进的精度。



<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_xg7bx2/afts/img/WxgUSrdZVj8AAAAAdJAAAAgADhHHAQFr/original" width="800"/>
<p>


## 使用案例

### 增强的多模态认知与自由模态切换
<video src="https://github.com/user-attachments/assets/147b9594-e492-4beb-a0db-b5c810135663" controls width="50%" height="400" style="object-fit: contain; max-width: 100%;">
    增强的多模态认知与自由模态切换
</video>

### 流式视频对话
<video src="https://github.com/user-attachments/assets/b1afb34e-8877-497c-85f3-82cd7cf618db" controls width="50%" height="400" style="object-fit: contain; max-width: 100%;">
    流式视频对话
</video>

### 可控音频生成
<video src="https://github.com/user-attachments/assets/6b5d504f-86a3-4121-97c9-0aa9ea9abaa4" controls="controls" width="50%" height="auto" >
    音频上下文 ASR 与方言 ASR
</video>

### 图像生成与编辑
<video src="https://github.com/user-attachments/assets/8d0af9cc-e0dc-440c-9963-b589d6396917" controls="controls" width="50%" height="auto" >
    可控图像生成
</video>




## 模型下载

你可以从 Huggingface 与 ModelScope 下载我们的最新模型。此前版本如 [Ming-flash-omni-Preview](https://github.com/inclusionAI/Ming/tree/Ming-flash-omni-Preview)，请参阅此[链接](https://github.com/inclusionAI/Ming/tree/Ming-flash-omni-Preview?tab=readme-ov-file#model-downloads)。

<div align="center">

| **模型**               |   **输入模态**   | **输出模态** |                                                                      **下载**                                                                      |
|:------------------------|:----------------------:| :---------------: |:------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Ming-flash-omni 2.0 | 图像、文本、视频、音频 | 图像、文本、音频  |                           [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ming-flash-omni-2.0) <br>[🤖 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ming-flash-omni-2.0)                           |
</div>
如果你位于中国大陆，我们强烈建议你从 🤖 <a href="https://www.modelscope.cn/models/inclusionAI/Ming-flash-omni-2.0">ModelScope</a> 下载我们的模型。

```
pip install modelscope
modelscope download --model inclusionAI/Ming-flash-omni-2.0 --local_dir inclusionAI/Ming-flash-omni-2.0  --revision master
```

注：下载过程视网络状况可能需要数分钟到数小时。


## 环境准备


### 使用 pip 安装
```shell
pip install -r requirements.txt
pip install nvidia-cublas-cu12==12.4.5.8  # for H20 GPU
```


## 用法示例

我们提供逐步运行的示例：

第 1 步 - 下载源代码
```
git clone https://github.com/inclusionAI/Ming.git 
cd Ming
```
第 2 步 - 下载模型权重并在源代码目录中创建软链接

按照[模型下载](#模型下载)下载我们的模型

```shell
mkdir inclusionAI 
ln -s /path/to/inclusionAI/Ming-flash-omni-2.0 inclusionAI/Ming-flash-omni-2.0
```

第 3 步 - 进入代码目录，你可以参考以下代码运行 Ming-flash-omni 模型。
```shell
jupyter notebook cookbook.ipynb
```

我们还提供了本仓库用法的简单示例。详细用法请参阅 [cookbook.ipynb](https://github.com/inclusionAI/Ming/blob/main/cookbook.ipynb)。

```python
import os
import torch
import warnings
from bisect import bisect_left
warnings.filterwarnings("ignore")

from transformers import AutoProcessor
from modeling_bailingmm2 import BailingMM2NativeForConditionalGeneration

def split_model():
    device_map = {}
    world_size = torch.cuda.device_count()
    num_layers = 32
    layer_per_gpu = num_layers // world_size
    layer_per_gpu = [i * layer_per_gpu for i in range(1, world_size + 1)]
    for i in range(num_layers):
        device_map[f'model.model.layers.{i}'] = bisect_left(layer_per_gpu, i)
    device_map['vision'] = 0
    device_map['audio'] = 0
    device_map['linear_proj'] = 0
    device_map['linear_proj_audio'] = 0
    device_map['model.model.word_embeddings.weight'] = 0
    device_map['model.model.norm.weight'] = 0
    device_map['model.lm_head.weight'] = 0
    device_map['model.model.norm'] = 0
    device_map[f'model.model.layers.{num_layers - 1}'] = 0
    return device_map

# Load pre-trained model with optimized settings, this will take ~10 minutes
model_path = "inclusionAI/Ming-flash-omni-2.0"
model = BailingMM2NativeForConditionalGeneration.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
    device_map=split_model(),
    load_image_gen=True,
    load_talker=True,
).to(dtype=torch.bfloat16)

# Initialize processor for handling multimodal inputs
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)

# Inference Pipeline
def generate(messages, processor, model, sys_prompt_exp=None, use_cot_system_prompt=False, max_new_tokens=512):
    text = processor.apply_chat_template(
        messages, 
        sys_prompt_exp=sys_prompt_exp,
        use_cot_system_prompt=use_cot_system_prompt
    )
    image_inputs, video_inputs, audio_inputs = processor.process_vision_info(messages)

    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        audios=audio_inputs,
        return_tensors="pt",
        audio_kwargs={"use_whisper_encoder": True},
    ).to(model.device)

    for k in inputs.keys():
        if k == "pixel_values" or k == "pixel_values_videos" or k == "audio_feats":
            inputs[k] = inputs[k].to(dtype=torch.bfloat16)

    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            use_cache=True,
            eos_token_id=processor.gen_terminator,
            num_logits_to_keep=1,
        )

    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]

    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0]

    return output_text

# qa
messages = [
    {
        "role": "HUMAN",
        "content": [
            {"type": "text", "text": "请详细介绍鹦鹉的生活习性。"}
        ],
    },
]
output_text = generate(messages, processor=processor, model=model)
print(output_text)
# Output:

# 鹦鹉是一种非常受欢迎的宠物鸟类，它们以其鲜艳的羽毛、聪明的头脑和模仿人类语言的能力而闻名。鹦鹉的生活习性非常丰富，以下是一些主要的习性：

# 1. **社交性**：鹦鹉是高度社交的鸟类，它们在野外通常生活在群体中，与同伴互动、玩耍和寻找食物。在家庭环境中，鹦鹉需要与人类或其他鹦鹉进行定期的互动，以保持其心理健康。

# 2. **智力**：鹦鹉拥有非常高的智力，它们能够学习各种技能，包括模仿人类语言、识别物体、解决问题等。这种智力使它们成为非常有趣的宠物。

# ......
```


## 引用

如果你觉得我们的工作有帮助，欢迎引用我们。

```bibtex

@misc{Mingomni2025,
      title  = {Ming-Omni: A Unified Multimodal Model for Perception and Generation}, 
      author = {Inclusion AI},
      year = {2025},
      eprint = {2506.09344},
      archivePrefix = {arXiv},
      url = {https://arxiv.org/abs/2506.09344}
}

@article{ai2025ming,
  title={Ming-flash-omni: A sparse, unified architecture for multimodal perception and generation},
  author={Inclusion AI},
  journal={arXiv preprint arXiv:2510.24821},
  year={2025}
}
```

---
title: "Ring：InclusionAI 开源的推理 MoE 大语言模型"
title_en: "inclusionAI/Ring"
source: https://github.com/inclusionAI/Ring/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# Ring：InclusionAI 开源的推理 MoE 大语言模型

> 原文：[inclusionAI/Ring](https://github.com/inclusionAI/Ring/blob/main/README.md) · 蚂蚁集团 InclusionAI

# Ring

<p align="center">
    <img src="./figures/ant-bailing.png" width="100"/>
<p>

<p align="center">
          🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp&nbsp | &nbsp&nbsp🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope</a>

## 新闻
* [2025-07]:🎉 新增 [Ring-lite-2507](https://huggingface.co/inclusionAI/Ring-lite-2507) 模型
* [2025-06]:🎉 新增 [Ring-lite](https://huggingface.co/inclusionAI/Ring-lite) 模型
* [2025-04]:🎉 新增 [Ring-lite-linear-preview](hybrid_linear) 模型

## 简介

Ring 是由 InclusionAI 提供并开源的推理 MoE 大语言模型，派生自 [Ling](https://github.com/inclusionAI/Ling)。我们推出 Ring-lite-distill-preview，拥有 168 亿总参数、27.5 亿激活参数。与业界现有模型相比，该模型展现出令人瞩目的推理性能。


## 模型下载

你可以在下表中查看适合你用例的各种参数版本。如果你位于中国大陆，我们还在 ModelScope.cn 上提供模型以加速下载。

<div align="center">

|      **模型**       | **总参数量** | **激活参数量** | **上下文长度** |                                                                        **下载**                                                                        |
| :------------------: | :---------------: | :-------------------: | :----------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------: |
|    Ring-lite-2507    |       16.8B       |         2.75B         |        128K         |     [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ring-lite-2507) <br>[🤖 ModelScope](https://modelscope.cn/models/inclusionAI/Ring-lite-2507)     |
|    Ring-lite    |       16.8B       |         2.75B         |        128K         |     [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ring-lite) <br>[🤖 ModelScope](https://modelscope.cn/models/inclusionAI/Ring-lite)     |
|    Ring-lite-distill-preview    |       16.8B       |         2.75B         |        64K         |     [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ring-lite-distill-preview) <br>[🤖 ModelScope](https://modelscope.cn/models/inclusionAI/Ring-lite-distill-preview)     |


</div>

## 博客
[https://inclusionai.github.io/blog/ring-lite-2507/](https://inclusionai.github.io/blog/ring-lite-2507/)

## 快速开始

### 🤗 Hugging Face Transformers

以下代码片段展示如何使用 `transformers` 运行对话模型：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "inclusionAI/Ring-lite"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Give me a short introduction to large language models."
messages = [
    {"role": "system", "content": "You are Ring, an assistant created by inclusionAI"},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=8192
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
```

### 🤖 ModelScope

如果你位于中国大陆，我们强烈建议你从 🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope</a> 使用我们的模型。

## 部署
请参阅 [Ling](https://github.com/inclusionAI/Ling)

## 微调
请参阅 [Ling](https://github.com/inclusionAI/Ling)


## 许可证

本代码仓库基于 [MIT License](https://github.com/inclusionAI/Ring/blob/master/LICENSE) 授权。

## 引用

```
@misc{ringteam2025ringlitescalablereasoningc3postabilized,
      title={Ring-lite: Scalable Reasoning via C3PO-Stabilized Reinforcement Learning for LLMs}, 
      author={Ling Team},
      year={2025},
      eprint={2506.14731},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2506.14731}, 
}
```

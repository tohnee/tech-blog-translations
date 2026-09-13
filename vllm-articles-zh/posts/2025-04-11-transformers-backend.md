---
title: "vLLM 中的 Transformers 建模后端集成"
title_en: "Transformers modeling backend integration in vLLM"
source: https://vllm.ai/blog/2025-04-11-transformers-backend
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中的 Transformers 建模后端集成

> 原文：[Transformers modeling backend integration in vLLM](https://vllm.ai/blog/2025-04-11-transformers-backend) · vLLM 博客

作者：Hugging Face 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)

[Hugging Face Transformers 库](https://huggingface.co/docs/transformers/main/en/index)为庞大的模型架构生态系统提供了灵活、统一的接口。从研究到在自定义数据集上微调，Transformers 是所有人的首选工具包。

但当涉及大规模*部署*这些模型时，推理速度和效率往往成为焦点。[vLLM](https://docs.vllm.ai/en/latest/) 应运而生——这是一个专为高吞吐量推理而设计的库，从 Hugging Face Hub 拉取模型，并针对生产级性能进行优化。

vLLM 代码库近期新增了一项功能，可将 Transformers 用作模型实现的后端。因此，vLLM 能够在现有 Transformers 架构之上进一步优化吞吐量/延迟。在这篇文章中，我们将探讨 vLLM 如何利用 Transformers 建模后端，将**灵活性**与**效率**结合起来，让你更快、更聪明地部署最先进的模型。

## 更新

本节收录自这篇博文首发（2025 年 4 月 11 日）以来的所有更新。

### 视觉语言模型支持（2025 年 7 月 21 日）

使用 Transformers 建模后端的 vLLM 现已支持**视觉语言模型**。当用户添加 `model_impl="transformers"` 时，系统会自动推断并加载适用于纯文本和多模态的正确类。

以下是使用 Transformers 建模后端服务多模态模型的方法。

```
vllm serve llava-hf/llava-onevision-qwen2-0.5b-ov-hf \
--model_impl transformers \
```

要使用该模型，可以像这样调用 `openai` API：

```
from openai import OpenAI
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
chat_response = client.chat.completions.create(
    model="llava-hf/llava-onevision-qwen2-0.5b-ov-hf",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "http://images.cocodataset.org/val2017/000000039769.jpg",
                },
            },
        ],
    }],
)
print("Chat response:", chat_response)
```

你也可以直接使用 `LLM` API 初始化 vLLM 引擎。下面是使用 `LLM` API 服务同一模型的示例。

```
from vllm import LLM, SamplingParams
from PIL import Image
import requests
from transformers import AutoProcessor

model_id = "llava-hf/llava-onevision-qwen2-0.5b-ov-hf"
hf_processor = AutoProcessor.from_pretrained(model_id) # required to dynamically update the chat template

messages = [
    {
      "role": "user",
      "content": [
          {"type": "image", "url": "dummy_image.jpg"},
          {"type": "text", "text": "What is the content of this image?"},
        ],
    },
]
prompt = hf_processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
image = Image.open(
    requests.get(
        "http://images.cocodataset.org/val2017/000000039769.jpg", stream=True
    ).raw
)

# initialize the vlm using the `model_impl="transformers"`
vlm = LLM(
    model="llava-hf/llava-onevision-qwen2-0.5b-ov-hf",
    model_impl="transformers",
)

outputs = vlm.generate(
    {
        "prompt": prompt,
        "multi_modal_data": {"image": image},
    },
    sampling_params=SamplingParams(max_tokens=100)
)

for o in outputs:
    generated_text = o.outputs[0].text
    print(generated_text)

# OUTPUTS:
# In the tranquil setting of this image, two feline companions are enjoying a peaceful slumber on a
# cozy pink couch. The couch, adorned with a plush red fabric across the seating area, serves as their perfect resting place.
#
# On the left side of the couch, a gray tabby cat is curled up at rest, its body relaxed in a display
# of feline serenity. One paw playfully stretches out, perhaps in mid-jump or simply exploring its surroundings.
```

## Transformers 与 vLLM：推理实战

让我们从使用 `meta-llama/Llama-3.2-1B` 模型的简单文本生成任务开始，看看这些库的表现如何。

**使用 Transformers 推理**

transformers 库的优势在于简洁与通用。使用其 `pipeline` API，推理轻而易举：

```
from transformers import pipeline

pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")
result = pipe("The future of AI is")

print(result[0]["generated_text"])
```

这种方式非常适合原型开发或小规模任务，但它并未针对高吞吐量推理或低延迟部署进行优化。

**使用 vLLM 推理**

vLLM 走了一条不同的路线，通过 `PagedAttention`（一种节省内存的注意力机制）和动态批处理等特性优先保证效率。以下是 vLLM 中的同一任务：

```
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3.2-1B")
params = SamplingParams(max_tokens=20)
outputs = llm.generate("The future of AI is", sampling_params=params)
print(f"Generated text: {outputs[0].outputs[0].text}")
```

vLLM 的推理明显更快、更节省资源，尤其是在负载下。例如，它可以每秒处理数千个请求，同时使用更少的 GPU 显存。

## vLLM 的部署超能力：OpenAI 兼容性

除了原始性能之外，vLLM 还提供 OpenAI 兼容 API，使其可以直接替换外部服务。启动一个服务器：

```
vllm serve meta-llama/Llama-3.2-1B
```

然后用 curl 查询：

```
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "meta-llama/Llama-3.2-1B", "prompt": "San Francisco is a", "max_tokens": 7, "temperature": 0}'
```

或者使用 Python 的 OpenAI 客户端：

```
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")
completion = client.completions.create(
    model="meta-llama/Llama-3.2-1B",
    prompt="San Francisco is a",
    max_tokens=7,
    temperature=0
)
print("Completion result:", completion.choices[0].text)
```

这种兼容性降低了成本并增强了控制力，让你可以在本地利用 vLLM 的优化来扩展推理。

## 为什么需要 Transformers 建模后端？

Transformers 库针对贡献和[新模型的添加](https://huggingface.co/docs/transformers/en/add_new_model)进行了优化。而向 vLLM 添加新模型则[稍显复杂](https://docs.vllm.ai/en/latest/contributing/model/index.html)。

在**理想世界**中，只要新模型被添加到 Transformers，我们就能立即在 vLLM 中使用它。通过集成 Transformers 建模后端，我们朝着这个理想世界迈进了一步。

这里是关于如何让你的 Transformers 模型与 vLLM 兼容、从而触发该集成的[官方文档](https://docs.vllm.ai/en/latest/models/supported_models.html#custom-models)。我们照此操作，让 `modeling_gpt2.py` 与该集成兼容！你可以在[这个 Transformers 拉取请求](https://github.com/huggingface/transformers/pull/36934)中查看改动。

对于已在 Transformers 中的模型（且与 vLLM 兼容），我们只需：

```
llm = LLM(model="new-transformers-model", model_impl="transformers")
```

> **注意：** `model_impl` 参数并非严格必需。如果 vLLM 原生不支持该模型，它会自行切换到 Transformers 实现。

或者对于来自 Hugging Face Hub 的自定义模型：

```
llm = LLM(model="custom-hub-model", model_impl="transformers", trust_remote_code=True)
```

这个后端扮演着**桥梁**的角色，将 transformers 的即插即用灵活性与 vLLM 的推理实力结合起来。你可以两全其美：用 Transformers 进行快速原型开发，用 vLLM 进行优化部署。

## 案例：Helium

[Kyutai 团队的 Helium](https://huggingface.co/docs/transformers/en/model_doc/helium) 尚未被 vLLM 支持。你可能希望用 vLLM 对该模型进行优化推理，这正是 Transformers 建模后端大显身手的地方。

让我们看看实际效果：

```
vllm serve kyutai/helium-1-preview-2b --model-impl transformers
```

用 OpenAI API 查询：

```
from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

completion = client.completions.create(model="kyutai/helium-1-preview-2b", prompt="What is AI?")
print("Completion result:", completion)
```

在这里，vLLM 高效地处理输入，利用 Transformers 建模后端无缝加载 `kyutai/helium-1-preview-2b`。与在 Transformers 中原生运行相比，vLLM 提供了更低的延迟和更好的资源利用率。

通过将 Transformers 的模型生态与 vLLM 的推理优化相结合，你将获得一个既灵活又可扩展的工作流。无论你是在为新模型制作原型、部署自定义模型，还是扩展多模态应用，这一组合都能加速你从研究到生产的进程。

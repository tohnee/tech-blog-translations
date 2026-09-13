---
title: "vLLM 现已支持 NVIDIA Nemotron"
title_en: "Now Serving NVIDIA Nemotron with vLLM"
source: https://vllm.ai/blog/2025-10-23-now_serving_nvidia_nemotron_with_vllm
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 现已支持 NVIDIA Nemotron

> 原文：[Now Serving NVIDIA Nemotron with vLLM](https://vllm.ai/blog/2025-10-23-now_serving_nvidia_nemotron_with_vllm) · vLLM 博客

作者：NVIDIA Nemotron 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)

具备推理、规划与自主行动能力的智能体 AI 系统，正在推动开发者应用的下一次飞跃。要构建这些系统，开发者需要开放、高效、随时可扩展的工具。而随着对智能体的需求增长，开放且高性能的模型是关键——它们提供透明性、适应性与成本控制。

[NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 是一个由开放模型、数据集和技术组成的家族，助力开发者构建面向专用智能体 AI 的高效且准确的模型。

**vLLM 现已支持 NVIDIA Nemotron**

vLLM 为部署 NVIDIA Nemotron 开放模型家族提供了无缝路径，让开发者可以在数据中心与边缘硬件上快速启动面向智能体的高精度推理——针对吞吐量与准确率做了优化。Nemotron 模型配合 vLLM 开箱即用，采用开放权重与开放数据，支持可复现的生产级智能体。

**NVIDIA Nemotron Nano 2**

该家族最新的成员是 [NVIDIA Nemotron Nano 2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)——一个高效的轻量语言推理模型，采用[混合 Transformer–Mamba 架构](https://arxiv.org/pdf/2504.03624)，并支持可配置的思考预算（thinking budget）。这让开发者能够调节准确率、吞吐量与成本，以匹配真实的应用需求。

- **开放：** 该模型已在 [Hugging Face](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) 上发布，在推理、编程以及指令遵循、工具调用、长上下文对话等多种智能体任务上提供了领先的准确率。NVIDIA 生成并整理的超过 9T token 的[预训练与后训练数据](https://huggingface.co/nvidia/datasets?search=nemotron)也以非常宽松的许可证发布在 Hugging Face 上。
- **高效：** 得益于混合架构，在使用 vLLM 时，Nemotron Nano 2 产生关键思考 token 的速度比同等规模的次优开源稠密模型最高快 6 倍。更高的吞吐量让模型思考更快、探索更大的搜索空间、进行更好的自我反思，并交付更高的准确率。

![](https://vllm.ai/blog-assets/figures/2025-vllm-nvidia-nemotron/figure1.png)
图 1：Nemotron Nano 2 9B 在多个热门基准测试上的准确率图表

- **优化思考：** 该模型引入了一个名为思考预算（thinking budget）的新特性，可以避免智能体过度思考，并让推理成本可预测。下图显示，如果不加干预，模型可能过度思考，推高推理成本，某些情况下还会降低准确率。思考预算解决了这一难题：开发者可以调节模型，为其应用找到准确率与 token 生成量之间的最佳*平衡点*。

![](https://vllm.ai/blog-assets/figures/2025-vllm-nvidia-nemotron/figure2.png)
图 2：Nemotron Nano 2 9B 模型在不同「Token Budget」阈值下于热门基准测试上的准确率图表

**用 vLLM 开始使用 Nemotron**

我们来用 vLLM 部署 Nemotron Nano 2 模型进行智能体推理：

```
vllm serve nvidia/NVIDIA-Nemotron-Nano-9B-v2 \
    --trust-remote-code \
    --mamba_ssm_cache_dtype float32
```

现在我们可以创建一个 `ThinkingBudgetClient` 来调用刚创建的端点。它将帮助实施并解析上文描述的思考预算特性。有了 vLLM，这个过程非常简单直接——让我们开始吧！

```
from typing import Any, Dict, List
import openai
from transformers import AutoTokenizer

class ThinkingBudgetClient:

   def __init__(self, base_url: str, api_key: str, tokenizer_name_or_path: str):
       self.base_url = base_url
       self.api_key = api_key
       self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path)
       self.client = openai.OpenAI(base_url=self.base_url, api_key=self.api_key)

   def chat_completion(
       self,
       model: str,
       messages: List[Dict[str, Any]],
       max_thinking_budget: int = 512,
       max_tokens: int = 1024,
       **kwargs,
   ) -> Dict[str, Any]:

       assert (
           max_tokens > max_thinking_budget
       ), f"thinking budget must be smaller than maximum new tokens. Given {max_tokens=} and {max_thinking_budget=}"

       # 1. first call chat completion to get reasoning content
       response = self.client.chat.completions.create(
           model=model, messages=messages, max_tokens=max_thinking_budget, **kwargs
       )
       content = response.choices[0].message.content
       reasoning_content = content

       if not "</think>" in reasoning_content:
           # reasoning content is too long, closed with a period (.)
           reasoning_content = f"{reasoning_content}.n</think>nn"
       reasoning_tokens_len = len(
           self.tokenizer.encode(reasoning_content, add_special_tokens=False)
       )
       remaining_tokens = max_tokens - reasoning_tokens_len

       assert (
           remaining_tokens > 0
       ), f"remaining tokens must be positive. Given {remaining_tokens=}. Increase the max_tokens or lower the max_thinking_budget."

       # 2. append reasoning content to messages and call completion
       messages.append({"role": "assistant", "content": reasoning_content})
       prompt = self.tokenizer.apply_chat_template(
           messages,
           tokenize=False,
           continue_final_message=True,
       )

       response = self.client.completions.create(
           model=model, prompt=prompt, max_tokens=remaining_tokens, **kwargs
       )

       response_data = {
           "reasoning_content": reasoning_content.strip().strip("</think>").strip(),
           "content": response.choices[0].text,
           "finish_reason": response.choices[0].finish_reason,
       }

       return response_data
```

`ThinkingBudgetClient` 设置完成后，我们就可以发出请求并查看响应了！

```
tokenizer_name_or_path = "nvidia/NVIDIA-Nemotron-Nano-9B-v2"

client = ThinkingBudgetClient(
   base_url="http://localhost:8000/v1",  # Nano 9B v2 deployed in thinking mode
   api_key="EMPTY",
   tokenizer_name_or_path=tokenizer_name_or_path,
)

result = client.chat_completion(
   model="nvidia/NVIDIA-Nemotron-Nano-9B-v2",
   messages=[
       {"role": "system", "content": "You are a helpful assistant. /think"},
       {"role": "user", "content": "What is 2+2?"},
   ],
   max_thinking_budget=32,
   max_tokens=512,
   temperature=0.6,
   top_p=0.95,
)

print(result)
```

我们看到的响应如下：

```
{'reasoning_content': 'Okay, the user asked "What is 2+2?" Let me think. This is a basic arithmetic question. The answer should be straightforward. I need.', 'content': '2 + 2 equals **4**. nnLet me know if you need help with anything else! 😊n', 'finish_reason': 'stop'}

```

vLLM 作为工具，让 Nemotron Nano 2 的部署更快、更省显存，也更容易针对实时智能体用例进行扩展。此外，vLLM 对高效 KV 缓存管理和长上下文用例的关注，与 Nemotron Nano 2 的混合 Transformer-Mamba 架构相得益彰。

如果你想进一步了解如何使用 Nemotron Nano 2，可以查看[模型卡](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)。如果你想开始使用 vLLM，请参阅[快速入门文档](https://docs.vllm.ai/en/stable/getting_started/quickstart.html)。

**随处运行**

Nemotron 模型经过配置，可以在所有 GPU 加速系统上运行，让你从开发到生产无缝过渡。

你可以在 [build.nvidia.com](https://build.nvidia.com/nvidia/nvidia-nemotron-nano-9b-v2) 上由 NVIDIA 托管的端点试用该模型，或从 Hugging Face 下载。

[*分享你的想法*](http://nemotron.ideas.nvidia.com/?ncid=so-othe-692335)，*为你关心的事项投票，帮助塑造 Nemotron 的未来。*

*订阅 NVIDIA 新闻，并在 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper)*、*以及 [Discord](https://discord.com/invite/nvidiadeveloper) 上的 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)关注 NVIDIA AI，随时了解 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。*

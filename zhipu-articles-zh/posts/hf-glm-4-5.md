---
title: "GLM-4.5 模型卡"
source: https://huggingface.co/zai-org/GLM-4.5
crawled: 2026-09-22
title_en: "zai-org/GLM-4.5 model card"
translated: 2026-09-22
---

---
language:
- en
- zh
library_name: transformers
license: mit
pipeline_tag: text-generation
---

# GLM-4.5 模型卡

> 原文：[zai-org/GLM-4.5 model card](https://huggingface.co/zai-org/GLM-4.5) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 欢迎加入我们的 <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-4.5 <a href="https://z.ai/blog/glm-4.5" target="_blank">技术博客</a>、<a href="https://arxiv.org/abs/2508.06471" target="_blank">技术报告</a>以及<a href="https://zhipu-ai.feishu.cn/wiki/Gv3swM0Yci7w7Zke9E0crhU7n7D" target="_blank">智谱 AI 技术文档</a>。
    <br>
    📍 在 <a href="https://docs.z.ai/guides/llm/glm-4.5">Z.ai API 平台（全球）</a>或<br><a href="https://docs.bigmodel.cn/cn/guide/models/text/glm-4.5">智谱 AI 开放平台（中国大陆）</a>使用 GLM-4.5 API 服务。
    <br>
    👉 一键直达 <a href="https://chat.z.ai">GLM-4.5</a>。
</p>

## 模型简介

**GLM-4.5** 系列模型是为智能体而设计的基础模型。GLM-4.5 拥有 **355**B 总参数和 **32**B 激活参数，而 GLM-4.5-Air 采用更紧凑的设计，拥有 **106**B 总参数和 **12**B 激活参数。GLM-4.5 系列模型统一了推理、编码与智能体能力，以满足智能体应用的复杂需求。

GLM-4.5 与 GLM-4.5-Air 均为混合推理模型，提供两种模式：用于复杂推理和工具使用的思考模式，以及用于即时响应的非思考模式。

我们已开源 GLM-4.5 与 GLM-4.5-Air 的基座模型、混合推理模型，以及混合推理模型的 FP8 版本。它们以 MIT 开源许可证发布，可用于商业用途和二次开发。

正如我们在 12 项行业标准基准上的全面评测所示，GLM-4.5 取得 **63.2** 分的出色成绩，在所有闭源和开源模型中位列**第 3**。值得注意的是，GLM-4.5-Air 在保持卓越效率的同时取得了 **59.8** 分的颇具竞争力的结果。

![bench](https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/bench.png)

更多评测结果、展示案例与技术细节，请访问我们的
[技术博客](https://z.ai/blog/glm-4.5)或[技术报告](https://arxiv.org/abs/2508.06471)。

模型代码、工具解析器与推理解析器可在 [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4_moe)、[vLLM](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/models/glm4_moe_mtp.py) 和 [SGLang](https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/models/glm4_moe.py) 的实现中找到。

## 模型下载

你可以直接在 [Hugging Face](https://huggingface.co/spaces/zai-org/GLM-4.5-Space)
或 [ModelScope](https://modelscope.cn/studios/ZhipuAI/GLM-4.5-Demo) 上体验模型，或通过以下链接下载。

| 模型            | 下载链接                                                                                                                                | 模型大小 | 精度 |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------|-----------|
| GLM-4.5          | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5)                   | 355B-A32B  | BF16      |
| GLM-4.5-Air      | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5-Air)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5-Air)           | 106B-A12B  | BF16      |
| GLM-4.5-FP8      | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5-FP8)           | 355B-A32B  | FP8       |
| GLM-4.5-Air-FP8  | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5-Air-FP8)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5-Air-FP8)   | 106B-A12B  | FP8       |
| GLM-4.5-Base     | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5-Base)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5-Base)         | 355B-A32B  | BF16      |
| GLM-4.5-Air-Base | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5-Air-Base)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5-Air-Base) | 106B-A12B  | BF16      |

## 系统要求

### 推理

我们提供「全功能」模型推理的最低配置与推荐配置。下表数据基于以下条件：

1. 所有模型均使用 MTP 层，并指定
   `--speculative-num-steps 3 --speculative-eagle-topk 1 --speculative-num-draft-tokens 4`，以确保有竞争力的推理速度。
2. 不使用 `cpu-offload` 参数。
3. 推理批大小不超过 `8`。
4. 均在原生支持 FP8 推理的设备上执行，确保权重和缓存均为 FP8 格式。
5. 服务器内存必须超过 `1T`，以确保模型正常加载和运行。

模型可在下表配置下运行：

| 模型       | 精度 | GPU 型号与数量       | 测试框架 |
|-------------|-----------|----------------------|----------------|
| GLM-4.5     | BF16      | H100 x 16 / H200 x 8 | sglang         |
| GLM-4.5     | FP8       | H100 x 8 / H200 x 4  | sglang         |
| GLM-4.5-Air | BF16      | H100 x 4 / H200 x 2  | sglang         |
| GLM-4.5-Air | FP8       | H100 x 2 / H200 x 1  | sglang         |

在下表配置下，模型可利用其完整的 128K 上下文长度：

| 模型       | 精度 | GPU 型号与数量        | 测试框架 |
|-------------|-----------|-----------------------|----------------|
| GLM-4.5     | BF16      | H100 x 32 / H200 x 16 | sglang         |
| GLM-4.5     | FP8       | H100 x 16 / H200 x 8  | sglang         |
| GLM-4.5-Air | BF16      | H100 x 8 / H200 x 4   | sglang         |
| GLM-4.5-Air | FP8       | H100 x 4 / H200 x 2   | sglang         |

### 微调

使用 [Llama Factory](https://github.com/hiyouga/LLaMA-Factory) 时，代码可在下表配置下运行：

| 模型       | GPU 型号与数量 | 策略 | 批大小（每 GPU） |
|-------------|--------------------|----------|----------------------|
| GLM-4.5     | H100 x 16          | Lora     | 1                    |
| GLM-4.5-Air | H100 x 4           | Lora     | 1                    |

使用 [Swift](https://github.com/modelscope/ms-swift) 时，代码可在下表配置下运行：

| 模型       | GPU 型号与数量 | 策略 | 批大小（每 GPU） |
|-------------|--------------------|----------|----------------------|
| GLM-4.5     | H20 (96GiB) x 16   | Lora     | 1                    |
| GLM-4.5-Air | H20 (96GiB) x 4    | Lora     | 1                    |
| GLM-4.5     | H20 (96GiB) x 128  | SFT      | 1                    |
| GLM-4.5-Air | H20 (96GiB) x 32   | SFT      | 1                    |
| GLM-4.5     | H20 (96GiB) x 128  | RL       | 1                    |
| GLM-4.5-Air | H20 (96GiB) x 32   | RL       | 1                    |

## 快速开始

请根据 `requirements.txt` 安装所需的软件包。

```shell
pip install -r requirements.txt
```

### transformers

请参考 `inference` 文件夹中的 `trans_infer_cli.py` 代码。

### vLLM

+ BF16 和 FP8 均可通过以下命令启动：

```shell
vllm serve zai-org/GLM-4.5-Air \
    --tensor-parallel-size 8 \
    --tool-call-parser glm45 \
    --reasoning-parser glm45 \
    --enable-auto-tool-choice \
    --served-model-name glm-4.5-air
```

如果你在使用 8x H100 GPU 运行 GLM-4.5 模型时遇到内存不足，需要加上
`--cpu-offload-gb 16`（仅适用于 vLLM）。

如果遇到 `flash infer` 问题，可使用 `VLLM_ATTENTION_BACKEND=XFORMERS` 作为临时替代。你也可以
指定 `TORCH_CUDA_ARCH_LIST='9.0+PTX'` 来使用 `flash infer`（不同 GPU 的 TORCH_CUDA_ARCH_LIST
取值不同，请相应查阅）。

### SGLang

+ BF16

```shell
python3 -m sglang.launch_server \
  --model-path zai-org/GLM-4.5-Air \
  --tp-size 8 \
  --tool-call-parser glm45  \
  --reasoning-parser glm45 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --mem-fraction-static 0.7 \
  --served-model-name glm-4.5-air \
  --host 0.0.0.0 \
  --port 8000
```

+ FP8

```shell
python3 -m sglang.launch_server \
  --model-path zai-org/GLM-4.5-Air-FP8 \
  --tp-size 4 \
  --tool-call-parser glm45  \
  --reasoning-parser glm45  \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3  \
  --speculative-eagle-topk 1  \
  --speculative-num-draft-tokens 4 \
  --mem-fraction-static 0.7 \
  --disable-shared-experts-fusion \
  --served-model-name glm-4.5-air-fp8 \
  --host 0.0.0.0 \
  --port 8000
```

### 请求参数说明

+ 使用 `vLLM` 和 `SGLang` 时，发送请求时默认启用思考模式。如需关闭思考开关，需要添加
  `extra_body={"chat_template_kwargs": {"enable_thinking": False}}` 参数。
+ 两者均支持工具调用。调用时请使用 OpenAI 风格的工具描述格式。
+ 具体代码请参考 `inference` 文件夹中的 `api_request.py`。

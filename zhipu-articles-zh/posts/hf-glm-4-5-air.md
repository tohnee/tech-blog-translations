---
title: "GLM-4.5-Air 模型卡"
source: https://huggingface.co/zai-org/GLM-4.5-Air
crawled: 2026-09-22
title_en: "zai-org/GLM-4.5-Air model card"
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

# GLM-4.5-Air 模型卡

> 原文：[zai-org/GLM-4.5-Air model card](https://huggingface.co/zai-org/GLM-4.5-Air) · 智谱 Z.ai

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
[技术博客](https://z.ai/blog/glm-4.5)或[技术报告](https://huggingface.co/papers/2508.06471)。

模型代码、工具解析器与推理解析器可在 [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4_moe)、[vLLM](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/models/glm4_moe_mtp.py) 和 [SGLang](https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/models/glm4_moe.py) 的实现中找到。

## 快速开始

更多细节请参考我们的 [GitHub 页面](https://github.com/zai-org/GLM-4.5)。

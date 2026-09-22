---
title: "GLM-4.6 模型卡"
source: https://huggingface.co/zai-org/GLM-4.6
crawled: 2026-09-22
title_en: "zai-org/GLM-4.6 model card"
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

# GLM-4.6 模型卡

> 原文：[zai-org/GLM-4.6 model card](https://huggingface.co/zai-org/GLM-4.6) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 欢迎加入我们的 <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-4.6 <a href="https://z.ai/blog/glm-4.6" target="_blank">技术博客</a>、<a href="https://arxiv.org/abs/2508.06471" target="_blank">技术报告（GLM-4.5）</a>以及<a href="https://zhipu-ai.feishu.cn/wiki/Gv3swM0Yci7w7Zke9E0crhU7n7D" target="_blank">智谱 AI 技术文档</a>。
    <br>
    📍 在 <a href="https://docs.z.ai/guides/llm/glm-4.6">Z.ai API 平台</a>使用 GLM-4.6 API 服务。
    <br>
    👉 一键直达 <a href="https://chat.z.ai">GLM-4.6</a>。
</p>

## 模型简介

与 GLM-4.5 相比，**GLM-4.6** 带来多项关键改进：

* **更长的上下文窗口**：上下文窗口从 128K 扩展到 200K token，使模型能够处理更复杂的智能体任务。
* **更出色的编码性能**：模型在代码基准上得分更高，并在 Claude Code、Cline、Roo Code 和 Kilo Code 等应用中展现出更好的实际表现，包括生成的前端页面在视觉上更加精美。
* **更先进的推理**：GLM-4.6 在推理性能上有明显提升，并支持推理过程中的工具使用，整体能力更强。
* **更强大的智能体**：GLM-4.6 在工具使用和搜索型智能体上表现更强，并能更有效地融入各类智能体框架。
* **更精细的写作**：在风格和可读性上更好地契合人类偏好，在角色扮演场景中的表现更加自然。

我们在覆盖智能体、推理和编码的八项公开基准上评测了 GLM-4.6。结果显示其相较 GLM-4.5 取得明显提升，并且相对 **DeepSeek-V3.1-Terminus**、**Claude Sonnet 4** 等国内外领先模型保持竞争优势。

![bench](https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/bench_glm46.png)

## 推理

**GLM-4.5 与 GLM-4.6 使用相同的推理方法。**

更多细节请查阅我们的 [github](https://github.com/zai-org/GLM-4.5)。

## 推荐评测参数

对于一般评测，我们推荐使用 **1.0 的采样 temperature**。

对于**代码相关评测任务**（如 LCB），进一步建议设置：

- `top_p = 0.95`
- `top_k = 40`


## 评测

- 关于工具集成推理，请参阅[此文档](https://github.com/zai-org/GLM-4.5/blob/main/resources/glm_4.6_tir_guide.md)。
- 关于搜索基准，我们为思考模式下的搜索工具调用设计了特定格式以支持搜索智能体，详细模板请参阅[此处](https://github.com/zai-org/GLM-4.5/blob/main/resources/trajectory_search.json)。

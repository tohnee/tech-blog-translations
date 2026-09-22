---
title: "GLM-V"
source: https://github.com/THUDM/GLM-4.1V-Thinking
crawled: 2026-09-22
title_en: "GLM-V"
translated: 2026-09-22
---

# GLM-V

> 原文：[GLM-V](https://github.com/THUDM/GLM-4.1V-Thinking) · 智谱 Z.ai / THUDM

[中文阅读.](./README_zh.md)

<div align="center">
<img src=resources/logo.svg width="40%"/>
</div>
<p align="center">
    👋 欢迎加入我们的<a href="resources/WECHAT.md" target="_blank">微信</a>或 <a href="https://discord.gg/Hc5z9bx5Xw" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-5.3-Flash <a href="https://z.ai/blog/glm-5.3-flash" target="_blank">博客</a>以及 GLM-4.5V 与 GLM-4.1V 的<a href="https://arxiv.org/abs/2507.01006" target="_blank">技术报告</a>。
    <br>
    📍 在 <a href="https://docs.bigmodel.cn/cn/guide/models/text/glm-5.3" target="_blank">API 平台</a>使用 GLM-5.3-Flash API 服务。
    <br>
    🔜 在 <a href="https://z.ai" target="_blank">z.ai</a> 上试用 GLM-5.3-Flash（即将上线）。
</p>

## 简介

视觉-语言模型（VLM）已成为智能系统的关键基石。随着现实世界的 AI 任务日益复杂，VLM 迫切需要在基础多模态感知之外增强推理能力——提升准确性、全面性与智能水平——从而实现复杂问题求解、长上下文理解以及多模态智能体。

通过开源工作，我们希望与社区共同探索技术前沿，同时赋能更多开发者创造出令人兴奋的创新应用。

**本开源仓库包含我们的 `GLM-4.6V`、`GLM-4.5V` 与 `GLM-4.1V` 系列模型。**性能与细节请见
[模型概览](#模型概览)。已知问题请见
[遗留问题](#遗留问题)。

## 项目动态

- **News**: `2026/09/02`：本仓库将不再维护。关于 GLM-5.3-Flash 的问题，请前往 [GLM-5](https://github.com/zai-org/GLM-5) 仓库讨论。
- **News**: `2026/08/26`：我们发布了 [GLM-5.3-Flash](https://z.ai/blog/glm-5.3-flash)，我们的首个开源原生多模态模型。
- **News**: `2026/04/02`：我们发布了 [GLM-5V-Turbo](https://docs.z.ai/guides/vlm/glm-5v-turbo)
  与 [GLM-skills](https://github.com/zai-org/GLM-skills)。
- **News**: `2026/03/28`：我们发布了多个 GLM-V 相关的 Skills，覆盖 GLM-V-Grounding、GLM-V-Prompt-Gen 等多个专门领域。欢迎在
  [这里](skills)试用。
- **News**: `2025/11/10`：我们发布了 **UI2Code^N**，一个经强化学习增强的 UI 编码模型，具备 UI 转代码、UI 润色与 UI 编辑能力。该模型基于 `GLM-4.1V-Base` 训练。请
  在[这里](https://huggingface.co/zai-org/UI2Code_N)查看。
- **News**: `2025/10/27`：我们发布了 **Glyph**，一个通过视觉-文本压缩扩展上下文长度的框架，glyph 模型基于 `GLM-4.1V-Base` 训练。请
  在[这里](https://huggingface.co/zai-org/Glyph)查看。
- **News**: `2025/08/11`：我们发布了 **GLM-4.5V**，在多项基准上取得显著提升。我们还
  开源了精心打磨的**桌面助手应用**用于调试。连接 GLM-4.5V 后，它可以通过截图或屏幕录制捕获
  PC 屏幕上的视觉信息。欢迎试用，或将其定制为属于你自己的多模态助手。点击
  [这里](https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App)下载安装程序，或
  [从源码构建](examples/vllm-chat-helper/README.md)！
- **News**: `2025/07/16`：我们已开源用于训练 GLM-4.1V-Thinking 的 **VLM 奖励系统（VLM Reward System）**。查看
  [代码仓库](glmv_reward)，并在本地运行：`python examples/reward_system_demo.py`。
- **News**: `2025/07/01`：我们发布了 **GLM-4.1V-9B-Thinking** 及其
  [技术报告](https://arxiv.org/abs/2507.01006)。

## 模型实现代码

- GLM-4.5V 与 GLM-4.6V 模型算法：完整实现
  见 [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4v_moe)。
- GLM-4.1V-9B-Thinking 模型算法：完整实现
  见 [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4v)。
- 两个模型共享相同的多模态预处理，但使用不同的对话模板——请仔细区分。

## 模型下载

| 模型                | 下载链接                                                                                                                                       | 类型             |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| GLM-4.6V             | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.6V)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.6V)                         | 混合推理 |
| GLM-4.6V-FP8         | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.6V-FP8)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.6V-FP8)                 | 混合推理 |
| GLM-4.6V-Flash       | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.6V-Flash)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.6V-Flash)             | 混合推理 |
| GLM-4.5V             | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5V)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5V)                         | 混合推理 |
| GLM-4.5V-FP8         | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.5V-FP8)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.5V-FP8)                 | 混合推理 |
| GLM-4.1V-9B-Thinking | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.1V-9B-Thinking)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.1V-9B-Thinking) | 推理        |
| GLM-4.1V-9B-Base     | [🤗 Hugging Face](https://huggingface.co/zai-org/GLM-4.1V-9B-Base)<br>[🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.1V-9B-Base)         | 基座             |


+ Hugging Face 提供 GGUF 格式的模型权重。你可以从[这里](https://huggingface.co/collections/ggml-org/glm-v)下载 GLM-V 的 GGUF 格式模型。

## 使用案例

### Grounding

GLM-4.5V / GLM-4.6V / GLM-4.1V 具备精准的 grounding 能力。给定一个请求定位特定物体位置的提示词，模型
能够逐步推理并给出目标物体的边界框。查询提示词支持对目标物体的复杂描述，也支持指定输出格式，例如：
>
> - Help me to locate <expr> in the image and give me its bounding boxes.
> - Please pinpoint the bounding box [[x1,y1,x2,y2], …] in the image as per the given description. <expr>

其中，`<expr>` 是对目标物体的描述。输出边界框是一个四元组 $$[x_1,y_1,x_2,y_2]$$，
由左上角和右下角的坐标组成，其中每个数值按图像宽度（x 方向）或高度（y 方向）归一化并乘以 1000 缩放。

在响应中，特殊 token `<|begin_of_box|>` 与 `<|end_of_box|>` 用于标记答案中的图像边界框。
括号样式可能有所不同（[]、[[]]、()、<> 等），但含义相同：用于包裹边界框的坐标。

### GUI 智能体

- `examples/gui-agent`：演示 GUI 智能体的提示词构建与输出处理，涵盖移动端、PC 与 Web 的策略。GLM-4.1V 与 GLM-4.5V 的提示词模板有所不同。

### 快速演示

- `examples/vlm-helper`：面向 GLM 多模态模型（主要是 GLM-4.5V，兼容 GLM-4.1V）的桌面助手，
  支持文本、图像、视频、PDF、PPT 等多种输入，连接 GLM 多模态 API，在各场景中提供智能服务。可下载
  [安装程序](https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App)
  或[从源码构建](examples/vlm-helper/README.md)。


## 本地部署 GLM-V 系列模型

GLM-V 系列支持使用以下框架部署。欢迎试用：

- [SGLang](https://github.com/sgl-project/sglang)（v0.5.15.post1+）——见 [cookbook](https://docs.sglang.io/cookbook/autoregressive/GLM/GLM-4.6V)
- [vLLM](https://github.com/vllm-project/vllm)（v0.25.0+）——见 [recipes](https://recipes.vllm.ai/zai-org/GLM-4.6V)
- [Transformers](https://github.com/huggingface/transformers)（v0.5.13+）——见 [transformers 文档](https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/glm4v_moe.md)
- 若要在 `Ascend NPU` 平台上部署，可使用 xLLM 等推理框架，见[这里](examples/Ascend_NPU/README_zh.md)。


## 与其他自动化工具的集成

### Midscene.js

[Midscene.js](https://midscenejs.com/en/index.html) 是一个由视觉模型驱动的开源 UI 自动化 SDK，支持通过 JavaScript 或 Yaml 格式的流程语法进行多平台自动化。

Midscene.js 已完成与 GLM-V 模型的集成。你可以通过 [Midscene.js 集成指南](https://midscenejs.com/model-common-config.html#glm-v)快速体验 GLM-V。

以下是两个帮助你快速上手的示例：

- [通过 TypeScript 脚本调用 Midscene.js](./examples/midscene-ts-demo)
- [通过 Yaml 脚本体验 Midscene.js](./examples/midscene-yaml-demo)

## 模型微调

[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 已支持对 GLM-4.5V 与
GLM-4.1V-9B-Thinking 模型的微调。下面是一个使用两张图像构建数据集的示例。你需要按
以下格式将数据集整理为 `finetune.json`，这是一个微调 GLM-4.1V-9B 的示例。

```json
[
  {
    "messages": [
      {
        "content": "<image>Who are they?",
        "role": "user"
      },
      {
        "content": "<think>\nUser asked me to observe the image and find the answer. I know they are Kane and Goretzka from Bayern Munich.</think>\n<answer>They're Kane and Goretzka from Bayern Munich.</answer>",
        "role": "assistant"
      },
      {
        "content": "<image>What are they doing?",
        "role": "user"
      },
      {
        "content": "<think>\nI need to observe what these people are doing. Oh, they are celebrating on the soccer field.</think>\n<answer>They are celebrating on the soccer field.</answer>",
        "role": "assistant"
      }
    ],
    "images": [
      "mllm_demo_data/1.jpg",
      "mllm_demo_data/2.jpg"
    ]
  }
]
```

1. `<think> ... </think>` 中的内容**不会**作为对话历史保存，也不会存入微调数据。
2. `<image>` 标签会被替换为对应的图像信息。
3. 对于 GLM-4.5V 模型，应去掉 <answer> 和 </answer> 标签。

之后，你可以按照 LLaMA-Factory 的标准流程进行微调。

## 模型概览

### GLM-4.6V

GLM-4.6V 系列模型包含两个版本：GLM-4.6V（106B），面向云端与高性能集群场景设计的基础模型；
以及 GLM-4.6V-Flash（9B），针对本地部署与低延迟应用优化的轻量级模型。
GLM-4.6V 在训练中将上下文窗口扩展到 128k token，
并在同等参数规模的模型中取得视觉理解方面的 SoTA 性能。
至关重要的是，我们首次集成了原生函数调用（Function Calling）能力。
这有效弥合了「视觉感知」与「可执行动作」之间的鸿沟，
为真实业务场景中的多模态智能体提供了统一的技术基础。

![GLM-4.6V Benchmarks](resources/bench_46v.jpeg)

除了在同等模型规模的主要多模态基准上取得 SoTA 性能之外，GLM-4.6V 还引入了
若干关键特性：

- **原生多模态函数调用**
实现原生的视觉驱动工具使用。图像、截图与文档页面可以直接作为工具输入传入，无需转换为文本；同时，视觉输出（图表、搜索图片、渲染页面）也会被理解并整合进推理链。这打通了从感知到理解再到执行的闭环。

- **图文交错内容生成**
支持基于复杂多模态输入的高质量混合媒介创作。GLM-4.6V 接收多模态上下文——涵盖文档、用户输入与工具检索到的图像——并合成与任务相匹配的连贯图文交错内容。在生成过程中，它可以主动调用搜索与检索工具来收集并筛选更多文本与视觉素材，产出丰富、有视觉依据的内容。

- **多模态文档理解**
GLM-4.6V 最多可处理 128K token 的多文档或长文档输入，直接以图像方式解读版式丰富的页面。它将文本、版式、图表、表格与插图联合理解，无需事先转换为纯文本即可准确理解复杂的、图像密集的文档。

- **前端复刻与可视化编辑**
从 UI 截图重建像素级精确的 HTML/CSS，并支持自然语言驱动的编辑。它以视觉方式检测版式、组件与样式，生成整洁的代码，并通过简单的用户指令应用迭代式的可视化修改。

### GLM-4.5V

GLM-4.5V 基于智谱 AI 的 GLM-4.5-Air。
它延续了 GLM-4.1V-Thinking 的技术路线，在 42 项公开视觉-语言基准上取得了同等规模模型中的 SOTA 性能。
它覆盖图像、视频、文档理解以及 GUI 智能体操作等常见任务。

除基准成绩之外，GLM-4.5V 还聚焦于真实场景的可用性。通过高效的混合训练，它能够处理
多种类型的视觉内容，实现全谱系的视觉推理，包括：

- **图像推理**（场景理解、复杂多图分析、空间识别）
- **视频理解**（长视频切分与事件识别）
- **GUI 任务**（屏幕阅读、图标识别、桌面操作辅助）
- **复杂图表与长文档解析**（研究报告分析、信息抽取）
- **Grounding**（精准的视觉元素定位）

该模型还引入了**思考模式**开关，让用户可以在快速响应与深度推理之间取得平衡。该开关的使用方式与 `GLM-4.5` 语言模型相同。

### GLM-4.1V-9B

**GLM-4.1V-9B-Thinking** 模型基于 [GLM-4-9B-0414](https://github.com/zai-org/GLM-4) 基座模型构建，引入了推理范式，并使用 RLCS（基于课程采样的强化学习，Reinforcement Learning with Curriculum Sampling）全方位增强模型能力。
它在 10B 级 VLM 中取得最强性能，并在 18 项基准任务上追平或超越规模大得多的 Qwen-2.5-VL-72B。

我们还开源了基座模型 **GLM-4.1V-9B-Base**，以支持研究者探索视觉-语言模型能力的极限。

![rl](resources/rl.jpeg)

与上一代 CogVLM2 和 GLM-4V 系列相比，**GLM-4.1V-Thinking** 带来了：

1. 该系列首个专注推理的模型，在数学之外的多个领域表现出色。
2. **64k** 上下文长度支持。
3. 支持**任意长宽比**以及最高 **4k** 的图像分辨率。
4. 中英双语开源版本。

GLM-4.1V-9B-Thinking 集成了**思维链（Chain-of-Thought）**推理机制，提升了准确性、内容丰富度与
可解释性。它在 10B 参数规模上的 28 项基准任务中的 23 项上领先，并以更小的规模在 18 项任务上超越 Qwen-2.5-VL-72B。

## 遗留问题

自 GLM-4.1V 开源以来，我们收到了大量社区反馈，也深知模型仍存在许多不足。在后续迭代中，我们尝试解决若干常见问题——例如重复思考输出与格式错误——这些问题在新版本中已得到一定程度的缓解。

不过，模型仍存在一些限制与问题，我们会尽快修复：

1. 纯文本问答能力仍有很大提升空间。在本轮研发周期中，我们的主要重心是视觉多模态场景，将在后续更新中增强纯文本能力。
2. 在某些情况下，模型仍可能过度思考甚至自我重复，尤其是在处理复杂提示词时。
3. 在某些情况下，模型可能会在结尾处再次复述答案。
4. 仍存在一定的感知局限，例如计数准确性以及识别特定人物等，仍需改进。

感谢你的耐心与理解。我们也欢迎在 issue 区反馈意见与建议——我们会尽力回应并改进！

## 引用

如果你使用了本模型，请引用以下论文：

```bibtex
@misc{vteam2025glm45vglm41vthinkingversatilemultimodal,
      title={GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning},
      author={V Team and Wenyi Hong and Wenmeng Yu and Xiaotao Gu and Guo Wang and Guobing Gan and Haomiao Tang and Jiale Cheng and Ji Qi and Junhui Ji and Lihang Pan and Shuaiqi Duan and Weihan Wang and Yan Wang and Yean Cheng and Zehai He and Zhe Su and Zhen Yang and Ziyang Pan and Aohan Zeng and Baoxu Wang and Bin Chen and Boyan Shi and Changyu Pang and Chenhui Zhang and Da Yin and Fan Yang and Guoqing Chen and Jiazheng Xu and Jiale Zhu and Jiali Chen and Jing Chen and Jinhao Chen and Jinghao Lin and Jinjiang Wang and Junjie Chen and Leqi Lei and Letian Gong and Leyi Pan and Mingdao Liu and Mingde Xu and Mingzhi Zhang and Qinkai Zheng and Sheng Yang and Shi Zhong and Shiyu Huang and Shuyuan Zhao and Siyan Xue and Shangqin Tu and Shengbiao Meng and Tianshu Zhang and Tianwei Luo and Tianxiang Hao and Tianyu Tong and Wenkai Li and Wei Jia and Xiao Liu and Xiaohan Zhang and Xin Lyu and Xinyue Fan and Xuancheng Huang and Yanling Wang and Yadong Xue and Yanfeng Wang and Yanzi Wang and Yifan An and Yifan Du and Yiming Shi and Yiheng Huang and Yilin Niu and Yuan Wang and Yuanchang Yue and Yuchen Li and Yutao Zhang and Yuting Wang and Yu Wang and Yuxuan Zhang and Zhao Xue and Zhenyu Hou and Zhengxiao Du and Zihan Wang and Peng Zhang and Debing Liu and Bin Xu and Juanzi Li and Minlie Huang and Yuxiao Dong and Jie Tang},
      year={2025},
      eprint={2507.01006},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2507.01006},
}
```

---
title: "GLM-4.5V 模型卡"
source: https://huggingface.co/zai-org/GLM-4.5V
crawled: 2026-09-22
title_en: "zai-org/GLM-4.5V model card"
translated: 2026-09-22
---

---
base_model:
- zai-org/GLM-4.5-Air-Base
language:
- zh
- en
library_name: transformers
license: mit
pipeline_tag: image-text-to-text
---

# GLM-4.5V 模型卡

> 原文：[zai-org/GLM-4.5V model card](https://huggingface.co/zai-org/GLM-4.5V) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-V/refs/heads/main/resources/logo.svg width="40%"/>
</div>

本模型属于 GLM-V 系列模型，该系列在论文 [GLM-4.1V-Thinking and GLM-4.5V: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning](https://huggingface.co/papers/2507.01006) 中首次介绍。

-   **论文**：[https://huggingface.co/papers/2507.01006](https://huggingface.co/papers/2507.01006)
-   **GitHub 仓库**：[https://github.com/zai-org/GLM-V/](https://github.com/zai-org/GLM-V/)
-   **在线演示**：[https://chat.z.ai/](https://chat.z.ai/)
-   **API 访问**：[智谱 AI 开放平台](https://docs.z.ai/guides/vlm/glm-4.5v)
-   **桌面助手应用**：[https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App](https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App)
-   **Discord 社区**：[https://discord.com/invite/8cnQKdAprg](https://discord.com/invite/8cnQKdAprg)

## 简介与模型概览

视觉-语言模型（VLM）已成为智能系统的关键基石。随着现实世界的 AI 任务日益复杂，VLM 迫切需要在基础多模态感知之外增强推理能力——提升准确性、全面性与智能水平——从而实现复杂问题求解、长上下文理解以及多模态智能体。

通过开源工作，我们希望与社区共同探索技术前沿，同时赋能更多开发者创造出令人兴奋的创新应用。

**本 Hugging Face 仓库托管的是 `GLM-4.5V` 模型，属于 `GLM-V` 系列的一部分。**

### GLM-4.5V

GLM-4.5V 基于智谱 AI 的新一代旗舰文本基础模型 GLM-4.5-Air（106B 参数，12B 激活）。它延续了 GLM-4.1V-Thinking 的技术路线，在 42 项公开视觉-语言基准上取得了同等规模模型中的 SOTA 性能。它覆盖图像、视频、文档理解以及 GUI 智能体操作等常见任务。

![GLM-4.5V Benchmarks](https://raw.githubusercontent.com/zai-org/GLM-V/refs/heads/main/resources/bench_45v.jpeg)

除基准成绩之外，GLM-4.5V 还聚焦于真实场景的可用性。通过高效的混合训练，它能够处理多种类型的视觉内容，实现全谱系的视觉推理，包括：
-   **图像推理**（场景理解、复杂多图分析、空间识别）
-   **视频理解**（长视频切分与事件识别）
-   **GUI 任务**（屏幕阅读、图标识别、桌面操作辅助）
-   **复杂图表与长文档解析**（研究报告分析、信息抽取）
-   **Grounding**（精准的视觉元素定位）

该模型还引入了**思考模式**开关，让用户可以在快速响应与深度推理之间取得平衡。该开关的使用方式与 `GLM-4.5` 语言模型相同。

### GLM-4.1V-9B

*此处提供 GLM-4.1V-9B 的相关背景信息以求完整，它是 GLM-V 系列的成员，也是 GLM-4.5V 研发的基础。*

**GLM-4.1V-9B-Thinking** 模型基于 [GLM-4-9B-0414](https://github.com/zai-org/GLM-4) 基座模型构建，引入了推理范式，并使用 RLCS（基于课程采样的强化学习，Reinforcement Learning with Curriculum Sampling）全方位增强模型能力。它在 10B 级 VLM 中取得最强性能，并在 18 项基准任务上追平或超越规模大得多的 Qwen-2.5-VL-72B。

我们还开源了基座模型 **GLM-4.1V-9B-Base**，以支持研究者探索视觉-语言模型能力的极限。

![Reinforcement Learning with Curriculum Sampling (RLCS)](https://raw.githubusercontent.com/zai-org/GLM-V/refs/heads/main/resources/rl.jpeg)

与上一代 CogVLM2 和 GLM-4V 系列相比，**GLM-4.1V-Thinking** 带来了：
1.  该系列首个专注推理的模型，在数学之外的多个领域表现出色。
2.  **64k** 上下文长度支持。
3.  支持**任意长宽比**以及最高 **4k** 的图像分辨率。
4.  中英双语开源版本。

GLM-4.1V-9B-Thinking 集成了**思维链（Chain-of-Thought）**推理机制，提升了准确性、内容丰富度与可解释性。它在 10B 参数规模上的 28 项基准任务中的 23 项上领先，并以更小的规模在 18 项任务上超越 Qwen-2.5-VL-72B。

![GLM-4.1V-9B Benchmarks](https://raw.githubusercontent.com/zai-org/GLM-V/refs/heads/main/resources/bench.jpeg)

## 项目动态

-   🔥 **News**: `2025/08/11`：我们发布了 **GLM-4.5V**，在多项基准上取得显著提升。我们还开源了精心打磨的**桌面助手应用**用于调试。连接 GLM-4.5V 后，它可以通过截图或屏幕录制捕获 PC 屏幕上的视觉信息。欢迎试用，或将其定制为属于你自己的多模态助手。点击[这里](https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App)下载安装程序，或[从源码构建](https://github.com/zai-org/GLM-V/blob/main/examples/vllm-chat-helper/README.md)！
-   **News**: `2025/07/16`：我们已开源用于训练 GLM-4.1V-Thinking 的 **VLM 奖励系统（VLM Reward System）**。查看[代码仓库](https://github.com/zai-org/GLM-V/tree/main/glmv_reward)，并在本地运行：`python examples/reward_system_demo.py`。
-   **News**: `2025/07/01`：我们发布了 **GLM-4.1V-9B-Thinking** 及其[技术报告](https://arxiv.org/abs/2507.01006)。

## 模型实现代码

*   GLM-4.5V 模型算法：完整实现见 [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4v_moe)。
*   GLM-4.1V-9B-Thinking 模型算法：完整实现见 [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4v)。
*   两个模型共享相同的多模态预处理，但使用不同的对话模板——请仔细区分。

## 使用方法

### 环境安装

针对 `SGLang` 与 `transformers`：

```bash
pip install transformers>=4.57.1
pip install sglang>=0.5.3
```

针对 `vLLM`：

```bash
pip install vllm>=0.10.2
```

### 使用 Transformers 快速开始

```python
from transformers import AutoProcessor, Glm4vMoeForConditionalGeneration
import torch

MODEL_PATH = "zai-org/GLM-4.5V"
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Grayscale_8bits_palette_sample_image.png"
            },
            {
                "type": "text",
                "text": "describe this image"
            }
        ],
    }
]
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = Glm4vMoeForConditionalGeneration.from_pretrained(
    pretrained_model_name_or_path=MODEL_PATH,
    torch_dtype="auto",
    device_map="auto",
)
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt"
).to(model.device)
inputs.pop("token_type_ids", None)
generated_ids = model.generate(**inputs, max_new_tokens=8192)
output_text = processor.decode(generated_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=False)
print(output_text)
```

响应中的特殊 token `<|begin_of_box|>` 与 `<|end_of_box|>` 标记了答案在图像中的边界框。边界框由四个数值给出——例如 `[x1, y1, x2, y2]`，其中 `(x1, y1)` 为左上角，`(x2, y2)` 为右下角。括号样式可能有所不同（[]、[[]]、()、<> 等），但含义相同：用于包裹边界框的坐标。这些坐标是介于 0 到 1000 之间的相对值，按图像尺寸归一化。

更多代码信息请访问我们的 [GitHub](https://github.com/zai-org/GLM-V/)。

### Grounding 示例

GLM-4.5V 具备精准的 grounding 能力。给定一个请求定位特定物体位置的提示词，GLM-4.5V 能够逐步推理并给出目标物体的边界框。查询提示词支持对目标物体的复杂描述，也支持指定输出格式，例如：

> -   Help me to locate <expr> in the image and give me its bounding boxes.
> -   Please pinpoint the bounding box [[x1,y1,x2,y2], …] in the image as per the given description. <expr>

其中，`<expr>` 是对目标物体的描述。输出边界框是一个四元组 $$[x_1,y_1,x_2,y_2]$$，由左上角和右下角的坐标组成，其中每个数值按图像宽度（x 方向）或高度（y 方向）归一化并乘以 1000 缩放。

在响应中，特殊 token `<|begin_of_box|>` 与 `<|end_of_box|>` 用于标记答案中的图像边界框。括号样式可能有所不同（[]、[[]]、()、<> 等），但含义相同：用于包裹边界框的坐标。

### GUI 智能体示例

-   `examples/gui-agent`：演示 GUI 智能体的提示词构建与输出处理，涵盖移动端、PC 与 Web 的策略。GLM-4.1V 与 GLM-4.5V 的提示词模板有所不同。

### 快速演示应用

-   `examples/vlm-helper`：面向 GLM 多模态模型（主要是 GLM-4.5V，兼容 GLM-4.1V）的桌面助手，支持文本、图像、视频、PDF、PPT 等多种输入，连接 GLM 多模态 API，在各场景中提供智能服务。可下载[安装程序](https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App)或[从源码构建](https://github.com/zai-org/GLM-V/blob/main/examples/vlm-helper/README.md)。

### vLLM

```bash
vllm serve zai-org/GLM-4.5V \
     --tensor-parallel-size 4 \
     --tool-call-parser glm45 \
     --reasoning-parser glm45 \
     --enable-auto-tool-choice \
     --served-model-name glm-4.5v \
     --allowed-local-media-path / \
     --media-io-kwargs '{"video": {"num_frames": -1}}'
```

### SGLang

```shell
python3 -m sglang.launch_server --model-path zai-org/GLM-4.5V \
     --tp-size 4 \
     --tool-call-parser glm45 \
     --reasoning-parser glm45 \
     --served-model-name glm-4.5v \
     --port 8000 \
     --host 0.0.0.0
```

注意事项：
-   我们推荐在 SGLang 中使用 `FA3` 注意力后端，以获得更高的推理性能和更低的显存占用：
    `--attention-backend fa3 --mm-attention-backend fa3 --enable-torch-compile`
    若不使用 `FA3`，大视频推理可能导致显存溢出（OOM）错误。
    我们还建议调大 `SGLANG_VLM_CACHE_SIZE_MB`（例如 `1024`），为视频理解提供充足的缓存空间。
-   使用 `vLLM` 和 `SGLang` 时，思考模式默认开启。如需关闭思考开关，请添加：
    `extra_body={"chat_template_kwargs": {"enable_thinking": False}}`

## 模型微调

[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 已支持对 GLM-4.5V 与 GLM-4.1V-9B-Thinking 模型的微调。下面是一个使用两张图像构建数据集的示例。你需要按以下格式将数据集整理为 `finetune.json`，这是一个微调 GLM-4.1V-9B 的示例。

```json
[
  {
    "messages": [
      {
        "content": "<image>Who are they?",
        "role": "user"
      },
      {
        "content": "<think>
User asked me to observe the image and find the answer. I know they are Kane and Goretzka from Bayern Munich.</think>
<answer>They're Kane and Goretzka from Bayern Munich.</answer>",
        "role": "assistant"
      },
      {
        "content": "<image>What are they doing?",
        "role": "user"
      },
      {
        "content": "<think>
I need to observe what these people are doing. Oh, they are celebrating on the soccer field.</think>
<answer>They are celebrating on the soccer field.</answer>",
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

1.  `<think> ... </think>` 中的内容**不会**作为对话历史保存，也不会存入微调数据。
2.  `<image>` 标签会被替换为对应的图像信息。
3.  对于 GLM-4.5V 模型，应去掉 <answer> 和 </answer> 标签。

之后，你可以按照 LLaMA-Factory 的标准流程进行微调。

## 已修复与遗留问题

自 GLM-4.1V 发布以来，我们处理了大量社区反馈的问题。在 GLM-4.5V 中，重复思考、输出格式错误等常见问题已得到缓解。但仍存在一些限制：

1.  在前端代码复现场景中，模型可能输出未经妥善 markdown 包裹的原始 HTML，也可能出现字符转义问题，进而导致渲染错误。我们提供了一个[补丁](https://github.com/zai-org/GLM-V/blob/main/inference/html_detector.py)来修复大多数情况。
2.  纯文本问答能力仍有提升空间，因为本次发布的主要重心是多模态场景。
3.  在某些情况下，模型可能会过度思考或重复内容，尤其是面对复杂提示词时。
4.  偶尔，模型可能会在结尾处再次复述答案。
5.  存在一些感知方面的问题，在计数、识别特定人物等任务上仍有改进空间。

欢迎在 issue 区反馈，我们会尽快处理问题。

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

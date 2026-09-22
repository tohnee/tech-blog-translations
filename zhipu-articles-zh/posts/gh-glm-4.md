---
title: "GLM-4-0414 系列模型"
source: https://github.com/THUDM/GLM-4
crawled: 2026-09-22
title_en: "GLM-4-0414 Model Series"
translated: 2026-09-22
---

# GLM-4-0414 系列模型

> 原文：[GLM-4-0414 Model Series](https://github.com/THUDM/GLM-4) · 智谱 Z.ai / THUDM

<p align="center">
👋 欢迎加入我们的 <a href="https://discord.gg/Hc5z9bx5Xw" target="_blank">Discord</a>、<a href="https://x.com/Zai_org" target="_blank">X</a> 与 <a href="resources/WECHAT.md" target="_blank"> 微信（中文）社区 </a>
</p>
<p align="center">
📍 本次发布的开源模型可在 <a href="https://chat.z.ai">Z.ai</a> 免费体验；如需 GLM 商用模型服务，请访问 <a href="https://bigmodel.cn">bigmodel.cn</a>。
</p>

阅读[中文版](README_zh.md)

## 项目动态

- 🔥 **News**: ```2025/07/02```：我们发布 [GLM-4.1V-9B-Thinking](https://huggingface.co/collections/zai-org/glm-41v-thinking-6862bbfc44593a8601c2578d) 系列 VLM，查看[这个 github 仓库](https://github.com/zai-org/GLM-4.1V-Thinking)了解更多信息。
- **News**: ```2025/04/14```：我们发布 [GLM-4-32B-0414](https://huggingface.co/collections/zai-org/glm-4-0414-67f3cbcb34dd9d252707cb2e) 系列模型，参数规模扩展到 32B，涵盖具备对话、推理与沉思（rumination）能力的模型。
- **News**: ``2024/06/18``：我们发布了[技术报告](https://arxiv.org/pdf/2406.12793)，欢迎查阅。
- **News**: ``2024/06/05``：我们发布 `GLM-4-9B` 系列开源模型。详情见[这里](README_20240605.md)。

## 模型简介

GLM 家族迎来了新成员——**GLM-4-32B-0414** 系列模型，拥有 320 亿参数。其性能可与 OpenAI 的 GPT 系列以及 DeepSeek 的 V3/R1 系列相媲美，同时支持非常友好的本地部署特性。GLM-4-32B-Base-0414 在 15T 高质量数据上完成预训练，其中包含大量推理型合成数据，这为后续的强化学习扩展奠定了基础。在后训练阶段，我们针对对话场景进行了人类偏好对齐；此外，借助拒绝采样与强化学习等技术，我们提升了模型在指令遵循、工程代码和函数调用方面的表现，从而强化了智能体任务所需的原子能力。GLM-4-32B-0414 在工程代码、Artifact 生成、函数调用、搜索式问答以及报告生成等方面均取得良好成绩。特别是在代码生成或特定问答任务等若干基准上，GLM-4-32B-Base-0414 取得了与 GPT-4o、DeepSeek-V3-0324（671B）等更大模型相当的表现。

**GLM-Z1-32B-0414** 是具备深度思考能力的推理模型。它基于 GLM-4-32B-0414，通过冷启动、扩展强化学习，并在数学、代码和逻辑等任务上进一步训练而成。与基座模型相比，GLM-Z1-32B-0414 显著提升了数学能力和解决复杂任务的能力。训练过程中，我们还引入了基于成对排序反馈的通用强化学习，增强了模型的通用能力。

**GLM-Z1-Rumination-32B-0414** 是具备沉思（rumination）能力的深度推理模型（对标 OpenAI 的 Deep Research）。与典型的深度思考模型不同，沉思模型能够进行更深、更长的思考，以解决更加开放和复杂的问题（例如，撰写两座城市 AI 发展的对比分析及其未来发展规划）。Z1-Rumination 通过扩展端到端强化学习训练而成，其响应由真实答案或评分细则（rubrics）打分，并且能够在深度思考过程中使用搜索工具来处理复杂任务。该模型在研究型写作与复杂任务上有显著提升。

最后，**GLM-Z1-9B-0414** 是一个惊喜。我们采用上述全部技术训练了一个小模型（9B）。GLM-Z1-9B-0414 在数学推理与通用任务上展现出卓越能力，整体表现在所有同规模开源模型中名列前茅。尤其是在资源受限的场景下，该模型在效率与效果之间取得了出色的平衡，为追求轻量化部署的用户提供了一个强大选择。


## 效果展示

### 动画生成

<table>
  <tr>
    <td style="text-align: center; font-size: 16px; font-weight: bold; padding: 10px; width: 420px;">
      GLM-Z1-32B-0414
    </td>
    <td style="text-align: center; font-size: 16px; font-weight: bold; padding: 10px; width: 420px;">
      GLM-4-32B-0414
    </td>
  </tr>
  <tr>
    <td style="vertical-align: top; padding: 10px; width: 420px;">
      <video src="https://github.com/user-attachments/assets/849ff9fd-b54d-4c74-9ee5-3412e1a09e32"
             style="width: 400px; height: 300px; object-fit: contain;" autoplay loop muted playsinline></video>
      <div style="margin-top: 10px; font-size: 14px; color: #333; width: 400px;">
        编写一个 Python 程序，展示一个小球在旋转的六边形内弹跳。小球应受重力和摩擦力影响，并且必须真实地从旋转的墙壁上弹开
      </div>
    </td>
    <td style="vertical-align: top; padding: 10px; width: 420px;">
      <video src="https://github.com/user-attachments/assets/8dccdb9d-cc44-4732-b438-74a4e3cb9dfb"
             style="width: 400px; height: 300px; object-fit: contain;" autoplay loop muted playsinline></video>
      <div style="margin-top: 10px; font-size: 14px; color: #333; width: 400px;">
         用 HTML 模拟一个小球从旋转六边形中心释放的场景。考虑小球与六边形各边的碰撞、作用在小球上的重力，并假设所有碰撞均为完全弹性碰撞。
      </div>
    </td>
  </tr>
</table>

### 网页设计

<table>
  <tr>
    <td style="text-align: center; font-size: 16px; font-weight: bold; padding: 10px; width: 420px;">
      GLM-4-32B-0414
    </td>
    <td style="text-align: center; font-size: 16px; font-weight: bold; padding: 10px; width: 420px;">
      GLM-4-32B-0414
    </td>
  </tr>
  <tr>
    <td style="vertical-align: top; padding: 10px; width: 420px;">
      <img src="https://github.com/user-attachments/assets/bd9c1fc1-c784-4e8f-9c76-5f7389a715f1"/>
      <div style="margin-top: 10px; font-size: 14px; color: #333; width: 400px;">
          设计一个支持自定义函数绘图的画板，可以添加和删除自定义函数，并为函数指定颜色。
      </div>
    </td>
    <td style="vertical-align: top; padding: 10px; width: 420px;">
      <img src="https://github.com/user-attachments/assets/7ad12d52-9229-4278-8d1b-ffbf43e99070"/>
      <div style="margin-top: 10px; font-size: 14px; color: #333; width: 400px;"> 为移动端机器学习平台设计一个 UI，应包含训练任务、存储管理和个人统计的界面。个人统计界面应使用图表展示用户在一段时间内的资源使用情况。使用 Tailwind CSS 为页面设置样式，并将这 3 个移动端界面平铺展示在单个 HTML 页面上。 </div>
    </td>
  </tr>
</table>

### SVG 生成

<table>
  <tr>
    <td style="text-align: center; font-size: 16px; font-weight: bold; padding: 10px; width: 420px;">
      GLM-4-32B-0414
    </td>
    <td style="text-align: center; font-size: 16px; font-weight: bold; padding: 10px; width: 420px;">
      GLM-4-32B-0414
    </td>
  </tr>
  <tr>
    <td style="vertical-align: top; padding: 10px; width: 420px;">
      <img src="https://github.com/user-attachments/assets/9407e4c1-1876-4ab5-838c-839836fb418a"/>
      <div style="margin-top: 10px; font-size: 14px; color: #333; width: 400px;">
          使用 SVG 创建一幅烟雨朦胧的江南景色。
      </div>
    </td>
    <td style="vertical-align: top; padding: 10px; width: 420px;">
      <img src="https://github.com/user-attachments/assets/bcce8c5a-cedf-45c8-b666-ddb023d5b49c"/>
      <div style="margin-top: 10px; font-size: 14px; color: #333; width: 400px;"> 使用 SVG 图示化展示 LLM 的训练过程。 </div>
    </td>
  </tr>
</table>

### 分析与研究报告撰写

<td style="vertical-align: top; padding: 10px; width: 420px;">
  <video src="https://github.com/user-attachments/assets/7939c8c5-0fcf-4bc4-be45-3964aad0e61c" style="width: 400px; height: 300px; object-fit: contain;" autoplay loop muted playsinline></video>
  <div style="margin-top: 10px; font-size: 14px; color: #333; width: 400px;">
    中国城市 AI 发展分析：北京与杭州的对比研究，以及城市治理中 AI 应用的国际案例考察。
  </div>
</td>

## 模型列表

### GLM-4-0414 系列模型

GLM-Z1-9B-0414 开源模型 [在线试用](https://modelscope.cn/studios/ZhipuAI/GLM-Z1-9B-0414/summary)

|           模型            |   类型    | 序列长度* |                                                                                                                                                              下载                                                                                                                                                              |
|:--------------------------:|:---------:|:-----------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|       GLM-4-9B-0414        |   对话    | 32K -> 128K |                           [🤗 Huggingface](https://huggingface.co/zai-org/GLM-4-9B-0414)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4-9B-0414)<br> [🧩 Modelers](https://modelers.cn/models/zhipuai/GLM-4-9B-0414)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-4-9B-0414)                           |
|       GLM-Z1-9B-0414       | 推理 | 32K -> 128K |                        [🤗 Huggingface](https://huggingface.co/zai-org/GLM-4-Z1-9B-0414)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-Z1-9B-0414)<br> [🧩 Modelers](https://modelers.cn/models/zhipuai/GLM-Z1-9B-0414)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-Z1-9B-0414)                        |
|    GLM-4-32B-Base-0414     |   基座    | 32K -> 128K |               [🤗 Huggingface](https://huggingface.co/zai-org/GLM-4-32B-Base-0414)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4-32B-Base-0414)<br> [🧩 Modelers](https://modelers.cn/models/zhipuai/GLM-4-32B-Base-0414)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-4-32B-Base-0414)               |
|       GLM-4-32B-0414       |   对话    | 32K -> 128K |                      [🤗 Huggingface](https://huggingface.co/zai-org/GLM-4-32B-0414)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4-32B-0414)<br> [🧩 Modelers](https://modelers.cn/models/zhipuai/GLM-4-32B-0414)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-4-32B-Base-0414)                       |
|      GLM-Z1-32B-0414       | 推理 | 32K -> 128K |                       [🤗 Huggingface](https://huggingface.co/zai-org/GLM-Z1-32B-0414)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-Z1-32B-0414)<br> [🧩 Modelers](https://modelers.cn/models/zhipuai/GLM-Z1-32B-0414)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-Z1-32B-0414)                       |
| GLM-Z1-Rumination-32B-0414 | 推理 |    128K     | [🤗 Huggingface](https://huggingface.co/zai-org/GLM-Z1-Rumination-32B-0414)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-Z1-Rumination-32B-0414)<br> [🧩 Modelers](https://modelers.cn/models/zhipuai/GLM-Z1-Rumination-32B-0414)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-Z1-Rumination-32B-0414) |

由于模型容量较小，GLM-4-9B-0414 并未像 GLM-4-32B-0414 那样进行智能体能力增强，而是主要针对翻译任务等需要大规模批量操作的场景进行了优化。

\* 模型原生以 32K 上下文训练。对于输入 + 输出总长度可能超过 32K token 的请求，我们建议启用 YaRN 以获得更好的外推性能。详见[模型与提示词实现](#模型与提示词实现)一节。

以下是 2024 年 6 月 5 日发布的 GLM-4 系列模型。详情见[这里](README_240605.md)。

|             模型             |   类型    | 序列长度* |                                                                                                      下载                                                                                                       |
|:-----------------------------:|:---------:|:----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      GLM-4-9B       | 基座 |     8K     |                                           [🤗 Huggingface](https://huggingface.co/zai-org/glm-4-9b)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/glm-4-9b)<br>                                            |
|    GLM-4-9B-Chat    | 对话 |    128K    |     [🤗 Huggingface](https://huggingface.co/zai-org/glm-4-9b-chat)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/glm-4-9b-chat)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-4-9B-Chat)      |
|  GLM-4-9B-Chat-HF   | 对话 |    128K    |                                     [🤗 Huggingface](https://huggingface.co/zai-org/glm-4-9b-chat-hf)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/glm-4-9b-chat-hf)                                      |
|  GLM-4-9B-Chat-1M   | 对话 |     1M     | [🤗 Huggingface](https://huggingface.co/zai-org/glm-4-9b-chat-1m)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/glm-4-9b-chat-1m)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-4-9B-Chat-1M) |
| GLM-4-9B-Chat-1M-HF | 对话 |     1M     |                                  [🤗 Huggingface](https://huggingface.co/zai-org/glm-4-9b-chat-1m-hf)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/glm-4-9b-chat-1m-hf)                                   |
|      GLM-4V-9B      | 对话 |     8K     |        [🤗 Huggingface](https://huggingface.co/zai-org/glm-4v-9b)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/glm-4v-9b)<br> [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/GLM-4V-9B)               |

## 评测结果

### GLM-4-0414 系列

<div style="text-align: center;">
  <img src="resources/Bench-32B.png" style="width: 80%;" />
</div>

| 模型             | IFEval | BFCL-v3（总体） | BFCL-v3（多轮） | TAU-Bench（零售） | TAU-Bench（航空） | SimpleQA | HotpotQA |
| ---------------- | ------ | ----------------- | ------------------- | ------------------ | ------------------- | -------- | -------- |
| Qwen2.5-Max      | 85.6   | 50.9              | 30.5                | 58.3               | 22.0                | 79.0     | 52.8     |
| GPT-4o-1120      | 81.9   | 69.6              | 41.0                | 62.8               | 46.0                | 82.8     | 63.9     |
| DeepSeek-V3-0324 | 83.4   | 66.2              | 35.8                | 60.7               | 32.4                | 82.6     | 54.6     |
| DeepSeek-R1      | 84.3   | 57.5              | 12.4                | 33.0               | 37.3                | 83.9     | 63.1     |
| GLM-4-32B-0414   | 87.6   | 69.6              | 41.5                | 68.7               | 51.2                | 88.1     | 63.8     |

> 对于 `SimpleQA` 与 `HotpotQA`，我们从每个测试集中采样了将近 500 个测试用例，为所有模型提供基础的 `search` 与 `click` 工具，确保其他设置保持一致，并对 3 次运行的结果取平均。

| 模型  | 框架  | [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)  | [SWE-bench Verified mini](https://github.com/mariushobbhahn/SWEBench-verified-mini) |
|---|---|---|---|
| GLM-4-32B-0414  | Moatless<sup>[1]</sup> | 33.8 | 38.0 |
| GLM-4-32B-0414  | Agentless<sup>[2]</sup>  | 30.7 | 34.0 |
| GLM-4-32B-0414  | OpenHands<sup>[3]</sup> | 27.2  | 28.0  |

[1] [Moatless v0.0.3](https://github.com/aorwall/moatless-tools) 使用了以下参数：`response_format="react", thoughts_in_action=False, max_interations=30`。失败的轨迹不做重试；其他设置均为默认。

[2] [Agentless v1.5.0](https://github.com/OpenAutoCoder/Agentless) 使用 [BGE](https://github.com/FlagOpen/FlagEmbedding/blob/master/README.md) 作为 embedding 模型，并使用 [FAISS](https://github.com/facebookresearch/faiss) 做相似度检索。为了在保持性能的同时加速补丁验证，运行单个实例的超时时间由默认的 300 秒改为 180 秒。

[3] [OpenHands v0.29.1](https://github.com/All-Hands-AI/OpenHands/tree/main) 未使用 YaRN 上下文扩展，而是将运行限制为最多 60 次迭代，并对历史进行摘要以避免超出 32K 上下文限制。摘要配置为 `llm_config="condenser", keep_first=1, max_size=32`。失败的轨迹不做重试。

### GLM-Z1-0414 系列

<div style="text-align: center;">
  <img src="resources/Bench-Z1-9B.png" style="width: 80%;" />
  <img src="resources/Bench-Z1-32B.png" style="width: 80%;" />
</div>

## 模型与提示词实现

### 模型实现

如果你想查看我们的模型实现，请查看相关仓库中已合并的 Pull Request：

+ [vLLM 模型实现](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/models/glm4.py)
+ [transformers 模型实现](https://github.com/huggingface/transformers/blob/main/src/transformers/models/glm4/modeling_glm4.py)
+ [llama.cpp 模型实现](https://github.com/ggml-org/llama.cpp/pull/12867)

### 长上下文处理（YaRN）

如果输入 + 输出的总 token 数可能超过模型的原生上下文长度（GLM-4-0414 系列大多为 32k），建议启用 YaRN 以获得更好的长上下文建模能力。对于支持的框架，你可以修改对应的 `config.json`。具体而言，对于 GLM-Z1 系列模型，当输入长度超过 **8,192 个 token** 时，可考虑启用 YaRN（Rope Scaling）。

```json
"rope_scaling": {
    "factor": 4.0,
    "original_max_position_embeddings": 32768,
    "type": "yarn"
}
```
对于大多数用户请求，如果输入 + 输出的 token 数不超过原生上下文长度，则无需做任何修改。

### 模型微调

关于模型微调所需计算资源的信息以及示例微调脚本，你可以在 `finetune/README.md` 中找到。

要启动一个简单的模型微调示例，请运行以下命令：

```shell
cd finetune
pip install -r ../inference/requirements.txt
pip install -r requirements.txt
# Use single GPU for Chat Fine-tune
python finetune.py  data/AdvertiseGen/  zai-org/GLM-4-9B-0414  configs/lora.yaml
```

🎉 该脚本还支持使用 **SwanLab** 进行可视化追踪的微调。你可以在 [SwanLab 可视化面板](https://swanlab.cn/@ShaohonChen/GLM4-Finetune/overview)上查看示例微调脚本的训练日志。

### 提示词实现

如果你使用 `transformers` 库提供的 `apply_chat_template` 方法构建提示词，以下是不同 GLM-4-0414 模型对 `System Prompts` 的限制。

+ `GLM-4-32B-Base-0414`：基座模型，无对话模板。
+ `GLM-4-*-0414` / `GLM-Z1-*-0414`：如果提供了 `tools`，`apply_chat_template` 会将工具填充到 `chat_template` 内的固定模板中，创建一条独立的、携带工具绑定的 `system` 消息并前置到消息列表（`messages[0]`）。原本传入的所有 `messages` 会自动后移一位。
+ `GLM-Z1-Rumination-32B-0414`：
    + 不支持自定义系统提示词或自定义工具。你的 `tools` 与 `system` 字段会被 `apply_chat_template` 忽略。使用该模型需要外部搜索引擎或自定义检索 API。
    + 总共支持四种工具：
        ```
        1. search
           Description: Executes a search query and returns search results. Use this when you need to find information about a specific topic.
           Parameters: query (string) - The search query string. Use English words unless it's a Chinese proper noun.

        2. click
           Description: Clicks on a link from the search results and navigates to the corresponding page. Use this when you need to view the detailed content of a specific search result.
           Parameters: link_id (integer) - The ID of the link to click (from the sequence number in the search results).

        3. open
           Description: Opens a specific website. Gets the content of any website via URL.
           Parameters: url (string) - The target website URL or domain name.

        4. finish
           Description: Completes the task. Use this when you have found the required information.
           Parameters: None
        ```
    + `chat_template` 中的固定模板使用英文进行思考。如需切换到其他语言，你需要修改以下部分（目前支持中文和英文）：
        ```
        <Important Configuration>
        - Language Used
            * Search Keywords: English -> Change here to "Chinese" or another language
            * Thinking: English -> Change here to "Chinese" or another language
        ```

要查看 GLM-4-0414 系列模型的具体对话模板，请查看对应模型仓库中的 `chat_template.jinja` 文件。

## 引用

如果你觉得我们的工作有帮助，请考虑引用以下论文。

```bibtex
@misc{glm2024chatglm,
      title={ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools},
      author={Team GLM and Aohan Zeng and Bin Xu and Bowen Wang and Chenhui Zhang and Da Yin and Diego Rojas and Guanyu Feng and Hanlin Zhao and Hanyu Lai and Hao Yu and Hongning Wang and Jiadai Sun and Jiajie Zhang and Jiale Cheng and Jiayi Gui and Jie Tang and Jing Zhang and Juanzi Li and Lei Zhao and Lindong Wu and Lucen Zhong and Mingdao Liu and Minlie Huang and Peng Zhang and Qinkai Zheng and Rui Lu and Shuaiqi Duan and Shudan Zhang and Shulin Cao and Shuxun Yang and Weng Lam Tam and Wenyi Zhao and Xiao Liu and Xiao Xia and Xiaohan Zhang and Xiaotao Gu and Xin Lv and Xinghan Liu and Xinyi Liu and Xinyue Yang and Xixuan Song and Xunkai Zhang and Yifan An and Yifan Xu and Yilin Niu and Yuantao Yang and Yueyan Li and Yushi Bai and Yuxiao Dong and Zehan Qi and Zhaoyu Wang and Zhen Yang and Zhengxiao Du and Zhenyu Hou and Zihan Wang},
      year={2024},
      eprint={2406.12793},
      archivePrefix={arXiv},
      primaryClass={id='cs.CL' full_name='Computation and Language' is_active=True alt_name='cmp-lg' in_archive='cs' is_general=False description='Covers natural language processing. Roughly includes material in ACM Subject Class I.2.7. Note that work on artificial languages (programming languages, logics, formal systems) that does not explicitly address natural-language issues broadly construed (natural-language processing, computational linguistics, speech, text retrieval, etc.) is not appropriate for this area.'}
}
```

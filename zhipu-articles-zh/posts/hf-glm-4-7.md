---
title: "GLM-4.7 模型卡"
source: https://huggingface.co/zai-org/GLM-4.7
crawled: 2026-09-22
title_en: "zai-org/GLM-4.7 model card"
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

# GLM-4.7 模型卡

> 原文：[zai-org/GLM-4.7 model card](https://huggingface.co/zai-org/GLM-4.7) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 欢迎加入我们的 <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-4.7 <a href="https://z.ai/blog/glm-4.7" target="_blank">技术博客</a>、<a href="https://arxiv.org/abs/2508.06471" target="_blank">技术报告（GLM-4.5）</a>。
    <br>
    📍 在 <a href="https://docs.z.ai/guides/llm/glm-4.7">Z.ai API 平台</a>使用 GLM-4.7 API 服务。
    <br>
    👉 一键直达 <a href="https://chat.z.ai">GLM-4.7</a>。
</p>

## 简介

**GLM-4.7**——你的新编码伙伴——带来以下特性：

- **核心编码能力**：与前任 GLM-4.6 相比，GLM-4.7 在多语言智能体编码和终端类任务上取得明显提升，包括 SWE-bench（73.8%，+5.8%）、SWE-bench Multilingual（66.7%，+12.9%）和 Terminal Bench 2.0（41%，+16.5%）。GLM-4.7 还支持先思考后行动，在 Claude Code、Kilo Code、Cline 和 Roo Code 等主流智能体框架中的复杂任务上有显著改进。
- **Vibe Coding**：GLM-4.7 在提升 UI 质量上迈出了一大步。它产出的网页更简洁、更现代，生成的幻灯片版式与尺寸更精准、外观更好看。
- **工具使用**：GLM-4.7 在工具使用上取得显著改进。在 τ^2-Bench 等基准以及 BrowseComp 网络浏览上都可以看到明显更好的表现。
- **复杂推理**：GLM-4.7 的数学与推理能力大幅增强，与 GLM-4.6 相比在 HLE（Humanity's Last Exam）基准上取得（42.8%，+12.4%）。

在聊天、创意写作和角色扮演等许多其他场景中，你也能看到显著改进。

![bench](https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/bench_glm47.png)

**基准测试表现。**下表给出了 GLM-4.7 与 GPT-5-High、GPT-5.1-High、Claude Sonnet 4.5、Gemini 3.0 Pro、DeepSeek-V3.2、Kimi K2 Thinking 等模型在 17 项基准（包括 8 项推理、5 项编码、3 项智能体基准）上的更详细对比。

| 基准测试                      | GLM-4.7 | GLM-4.6 | Kimi K2 Thinking | DeepSeek-V3.2 | Gemini 3.0 Pro | Claude Sonnet 4.5 | GPT-5-High | GPT-5.1-High |
|:-------------------------------|:-------:|:-------:|:----------------:|:-------------:|:--------------:|:-----------------:|:----------:|:------------:|
| MMLU-Pro                       |  84.3   |  83.2   |       84.6       |     85.0      |      90.1      |       88.2        |    87.5    |     87.0     |
| GPQA-Diamond                   |  85.7   |  81.0   |       84.5       |     82.4      |      91.9      |       83.4        |    85.7    |     88.1     |
| HLE                            |  24.8   |  17.2   |       23.9       |     25.1      |      37.5      |       13.7        |    26.3    |     25.7     |
| HLE (w/ Tools)                 |  42.8   |  30.4   |       44.9       |     40.8      |      45.8      |       32.0        |    35.2    |     42.7     |
| AIME 2025                      |  95.7   |  93.9   |       94.5       |     93.1      |      95.0      |       87.0        |    94.6    |     94.0     |
| HMMT Feb. 2025                 |  97.1   |  89.2   |       89.4       |     92.5      |      97.5      |       79.2        |    88.3    |     96.3     |
| HMMT Nov. 2025                 |  93.5   |  87.7   |       89.2       |     90.2      |      93.3      |       81.7        |    89.2    |      -       |
| IMOAnswerBench                 |  82.0   |  73.5   |       78.6       |     78.3      |      83.3      |       65.8        |    76.0    |      -       |
| LiveCodeBench-v6               |  84.9   |  82.8   |       83.1       |     83.3      |      90.7      |       64.0        |    87.0    |     87.0     |
| SWE-bench Verified             |  73.8   |  68.0   |       71.3       |     73.1      |      76.2      |       77.2        |    74.9    |     76.3     |
| SWE-bench Multilingual         |  66.7   |  53.8   |       61.1       |     70.2      |       -        |       68.0        |    55.3    |      -       |
| Terminal Bench Hard            |  33.3   |  23.6   |       30.6       |   35.4   |      39.0      |       33.3        |    30.5    |     43.0     |
| Terminal Bench 2.0             |  41.0   |  24.5   |       35.7       |     46.4      |      54.2      |       42.8        |    35.2    |     47.6     |
| BrowseComp                     |  52.0   |  45.1   |        -         |     51.4      |       -        |       24.1        |    54.9    |     50.8     |
| BrowseComp (w/ Context Manage) |  67.5   |  57.5   |       60.2       |     67.6      |      59.2      |         -         |     -      |      -       |
| BrowseComp-Zh                  |  66.6   |  49.5   |       62.3       |     65.0      |       -        |       42.4        |    63.0    |      -       |
| τ²-Bench                       |  87.4   |  75.2   |       74.3       |     85.3      |      90.7      |       87.2        |    82.4    |     82.7     |

> **编码：** AGI 是一段漫长的旅程，基准测试只是评估性能的一种方式。指标提供了必要的检查点，但最重要的仍然是它用起来的*感受*。真正的智能不只是考出高分或更快地处理数据；归根结底，AGI 的成功将以它与我们的生活融合得有多无痕来衡量——这一次，是「编码」。


## GLM-4.7 快速上手

### 交错思考与保留思考

![bench](https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/thinking.png)

GLM-4.7 进一步增强了**交错思考**（Interleaved Thinking，GLM-4.5 起引入的特性），并引入**保留思考**（Preserved Thinking）与**轮级思考**（Turn-level Thinking）。通过在行动之间思考、并跨轮保持一致，它让复杂任务更稳定、更可控：
- **交错思考**：模型在每次回复和每次工具调用之前都会思考，提升指令遵循与生成质量。
- **保留思考**：在编码智能体场景中，模型自动在多轮对话中保留所有思考块，复用已有推理而不是从头重新推导。这减少了信息损失和不一致，非常适合长时程复杂任务。
- **轮级思考**：模型支持在会话内按轮控制推理——轻量请求关闭思考以降低延迟/成本，复杂任务开启思考以提升准确性和稳定性。

更多细节：https://docs.z.ai/guides/capabilities/thinking-mode

### 评测参数

**默认设置（大多数任务）**

* temperature: `1.0`
* top-p: `0.95`
* 最大新 token 数: `131072`

对于多轮智能体任务（τ²-Bench 和 Terminal Bench 2），请开启[保留思考模式](https://docs.z.ai/guides/capabilities/thinking-mode)。

**Terminal Bench、SWE Bench Verified**

* temperature: `0.7`
* top-p: `1.0`
* 最大新 token 数: `16384`

**τ^2-Bench**

* Temperature: `0`
* 最大新 token 数: `16384`

在 τ^2-Bench 评测中，我们为 Retail 和 Telecom 的用户交互额外添加了提示词，以避免用户错误结束交互导致的失败模式。对于 Airline 领域，我们采用了 [Claude Opus 4.5](https://assets.anthropic.com/m/64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf) 发布报告中提出的领域修复。

## 本地部署 GLM-4.7

对于本地部署，GLM-4.7 支持 vLLM 和 SGLang 等推理框架。完整的部署说明见官方 [Github](https://github.com/zai-org/GLM-4.5) 仓库。


vLLM 和 SGLang 仅在其主分支上支持 GLM-4.7。你可以使用它们的官方 docker 镜像进行推理。

### vLLM

使用 Docker：

```shell
docker pull vllm/vllm-openai:nightly
```

或使用 pip（必须以 pypi.org 作为索引 URL）：

```shell
pip install -U vllm --pre --index-url https://pypi.org/simple --extra-index-url https://wheels.vllm.ai/nightly
```

### SGLang

使用 Docker：

```shell
docker pull lmsysorg/sglang:dev
```

或从源码 pip 安装 sglang。


### transformers

配合 `4.57.3` 版本的 transformers 使用，然后运行：

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "zai-org/GLM-4.7"
messages = [{"role": "user", "content": "hello"}]
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
)
model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
inputs = inputs.to(model.device)
generated_ids = model.generate(**inputs, max_new_tokens=128, do_sample=False)
output_text = tokenizer.decode(generated_ids[0][inputs.input_ids.shape[1] :])
print(output_text)
```

### vLLM

```shell
vllm serve zai-org/GLM-4.7-FP8 \
     --tensor-parallel-size 4 \
     --speculative-config.method mtp \
     --speculative-config.num_speculative_tokens 1 \
     --tool-call-parser glm47 \
     --reasoning-parser glm45 \
     --enable-auto-tool-choice \
     --served-model-name glm-4.7-fp8
```

### SGLang

```shell
python3 -m sglang.launch_server \
  --model-path zai-org/GLM-4.7-FP8 \
  --tp-size 8 \
  --tool-call-parser glm47  \
  --reasoning-parser glm45 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --mem-fraction-static 0.8 \
  --served-model-name glm-4.7-fp8 \
  --host 0.0.0.0 \
  --port 8000
```

### 参数说明

- 对于 GLM-4.7 的智能体任务，请通过添加以下配置开启[保留思考模式](https://docs.z.ai/guides/capabilities/thinking-mode)（仅 sglang 支持）：

  ```
    "chat_template_kwargs": {
        "enable_thinking": true,
        "clear_thinking": false
    }
    ```

- 使用 `vLLM` 和 `SGLang` 时，发送请求时默认启用思考模式。如需关闭思考开关，需添加 `"chat_template_kwargs": {"enable_thinking": False}` 参数。
- 两者均支持工具调用。调用时请使用 OpenAI 风格的工具描述格式。


## 引用

如果您在研究中发现我们的工作有用，请考虑引用以下论文：

```bibtex
@misc{5team2025glm45agenticreasoningcoding,
      title={GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models}, 
      author={GLM Team and Aohan Zeng and Xin Lv and Qinkai Zheng and Zhenyu Hou and Bin Chen and Chengxing Xie and Cunxiang Wang and Da Yin and Hao Zeng and Jiajie Zhang and Kedong Wang and Lucen Zhong and Mingdao Liu and Rui Lu and Shulin Cao and Xiaohan Zhang and Xuancheng Huang and Yao Wei and Yean Cheng and Yifan An and Yilin Niu and Yuanhao Wen and Yushi Bai and Zhengxiao Du and Zihan Wang and Zilin Zhu and Bohan Zhang and Bosi Wen and Bowen Wu and Bowen Xu and Can Huang and Casey Zhao and Changpeng Cai and Chao Yu and Chen Li and Chendi Ge and Chenghua Huang and Chenhui Zhang and Chenxi Xu and Chenzheng Zhu and Chuang Li and Congfeng Yin and Daoyan Lin and Dayong Yang and Dazhi Jiang and Ding Ai and Erle Zhu and Fei Wang and Gengzheng Pan and Guo Wang and Hailong Sun and Haitao Li and Haiyang Li and Haiyi Hu and Hanyu Zhang and Hao Peng and Hao Tai and Haoke Zhang and Haoran Wang and Haoyu Yang and He Liu and He Zhao and Hongwei Liu and Hongxi Yan and Huan Liu and Huilong Chen and Ji Li and Jiajing Zhao and Jiamin Ren and Jian Jiao and Jiani Zhao and Jianyang Yan and Jiaqi Wang and Jiayi Gui and Jiayue Zhao and Jie Liu and Jijie Li and Jing Li and Jing Lu and Jingsen Wang and Jingwei Yuan and Jingxuan Li and Jingzhao Du and Jinhua Du and Jinxin Liu and Junkai Zhi and Junli Gao and Ke Wang and Lekang Yang and Liang Xu and Lin Fan and Lindong Wu and Lintao Ding and Lu Wang and Man Zhang and Minghao Li and Minghuan Xu and Mingming Zhao and Mingshu Zhai and Pengfan Du and Qian Dong and Shangde Lei and Shangqing Tu and Shangtong Yang and Shaoyou Lu and Shijie Li and Shuang Li and Shuang-Li and Shuxun Yang and Sibo Yi and Tianshu Yu and Wei Tian and Weihan Wang and Wenbo Yu and Weng Lam Tam and Wenjie Liang and Wentao Liu and Xiao Wang and Xiaohan Jia and Xiaotao Gu and Xiaoying Ling and Xin Wang and Xing Fan and Xingru Pan and Xinyuan Zhang and Xinze Zhang and Xiuqing Fu and Xunkai Zhang and Yabo Xu and Yandong Wu and Yida Lu and Yidong Wang and Yilin Zhou and Yiming Pan and Ying Zhang and Yingli Wang and Yingru Li and Yinpei Su and Yipeng Geng and Yitong Zhu and Yongkun Yang and Yuhang Li and Yuhao Wu and Yujiang Li and Yunan Liu and Yunqing Wang and Yuntao Li and Yuxuan Zhang and Zezhen Liu and Zhen Yang and Zhengda Zhou and Zhongpei Qiao and Zhuoer Feng and Zhuorui Liu and Zichen Zhang and Zihan Wang and Zijun Yao and Zikang Wang and Ziqiang Liu and Ziwei Chai and Zixuan Li and Zuodong Zhao and Wenguang Chen and Jidong Zhai and Bin Xu and Minlie Huang and Hongning Wang and Juanzi Li and Yuxiao Dong and Jie Tang},
      year={2025},
      eprint={2508.06471},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2508.06471}, 
}

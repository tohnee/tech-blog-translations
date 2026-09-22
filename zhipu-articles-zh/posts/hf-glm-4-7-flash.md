---
title: "GLM-4.7-Flash 模型卡"
source: https://huggingface.co/zai-org/GLM-4.7-Flash
crawled: 2026-09-22
title_en: "zai-org/GLM-4.7-Flash model card"
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

# GLM-4.7-Flash 模型卡

> 原文：[zai-org/GLM-4.7-Flash model card](https://huggingface.co/zai-org/GLM-4.7-Flash) · 智谱 Z.ai

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 欢迎加入我们的 <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> 社区。
    <br>
    📖 了解 GLM-4.7 <a href="https://z.ai/blog/glm-4.7" target="_blank">技术博客</a>、<a href="https://arxiv.org/abs/2508.06471" target="_blank">技术报告（GLM-4.5）</a>。
    <br>
    📍 在 <a href="https://docs.z.ai/guides/llm/glm-4.7">Z.ai API 平台</a>使用 GLM-4.7-Flash API 服务。
    <br>
    👉 一键直达 <a href="https://chat.z.ai">GLM-4.7</a>。
</p>

## 简介

GLM-4.7-Flash 是一个 30B-A3B 的 MoE 模型。作为 30B 级别中最强的模型，GLM-4.7-Flash 为兼顾性能与效率的轻量部署提供了一个新选择。


### 基准测试表现


| 基准测试          | GLM-4.7-Flash | Qwen3-30B-A3B-Thinking-2507 | GPT-OSS-20B |
|--------------------|---------------|-----------------------------|-------------|
| AIME 25            | 91.6          | 85.0                        | 91.7        |
| GPQA               | 75.2          | 73.4                        | 71.5        |
| LCB v6             | 64.0          | 66.0                        | 61.0        |
| HLE                | 14.4          | 9.8                         | 10.9        |
| SWE-bench Verified | 59.2          | 22.0                        | 34.0        |
| τ²-Bench           | 79.5          | 49.0                        | 47.7        |
| BrowseComp         | 42.8          | 2.29                        | 28.3        |


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

## 本地部署 GLM-4.7-Flash

对于本地部署，GLM-4.7-Flash 支持 vLLM 和 SGLang 等推理框架。完整的部署说明见
官方 [Github](https://github.com/zai-org/GLM-4.5) 仓库。

vLLM 和 SGLang 仅在其主分支上支持 GLM-4.7-Flash。

### vLLM

+ 使用 pip（必须以 pypi.org 作为索引 URL）：

```shell
pip install -U vllm --pre --index-url https://pypi.org/simple --extra-index-url https://wheels.vllm.ai/nightly
pip install git+https://github.com/huggingface/transformers.git
```

### SGLang

+ 安装受支持版本的 SGLang 和 Transformers（推荐使用 `uv`）：

```shell
uv pip install sglang==0.3.2.dev9039+pr-17247.g90c446848 --extra-index-url https://sgl-project.github.io/whl/pr/
uv pip install git+https://github.com/huggingface/transformers.git@76732b4e7120808ff989edbd16401f61fa6a0afa
```

### transformers

配合 transformers 使用：

```shell
pip install git+https://github.com/huggingface/transformers.git
```

然后运行：

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "zai-org/GLM-4.7-Flash"
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
output_text = tokenizer.decode(generated_ids[0][inputs.input_ids.shape[1]:])
print(output_text)
```

### vLLM

```shell
vllm serve zai-org/GLM-4.7-Flash \
     --tensor-parallel-size 4 \
     --speculative-config.method mtp \
     --speculative-config.num_speculative_tokens 1 \
     --tool-call-parser glm47 \
     --reasoning-parser glm45 \
     --enable-auto-tool-choice \
     --served-model-name glm-4.7-flash
```

### SGLang

```shell
python3 -m sglang.launch_server \
  --model-path zai-org/GLM-4.7-Flash \
  --tp-size 4 \
  --tool-call-parser glm47  \
  --reasoning-parser glm45 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --mem-fraction-static 0.8 \
  --served-model-name glm-4.7-flash \
  --host 0.0.0.0 \
  --port 8000
```
+ 对于 Blackwell GPU，请在 SGLang 启动命令中加入 `--attention-backend triton --speculative-draft-attention-backend triton`。

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

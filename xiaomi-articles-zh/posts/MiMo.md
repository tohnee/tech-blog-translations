---
title: "MiMo：从预训练到后训练解锁语言模型的推理潜能"
title_en: "XiaomiMiMo/MiMo"
source: https://github.com/XiaomiMiMo/MiMo/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo：从预训练到后训练解锁语言模型的推理潜能

> 原文：[XiaomiMiMo/MiMo](https://github.com/XiaomiMiMo/MiMo/blob/main/README.md) · 小米 MiMo

<div align="center">
  <picture>
    <source srcset="https://github.com/XiaomiMiMo/MiMo/raw/main/figures/Xiaomi_MiMo_darkmode.png?raw=true" media="(prefers-color-scheme: dark)">
    <img src="https://github.com/XiaomiMiMo/MiMo/raw/main/figures/Xiaomi_MiMo.png?raw=true" width="60%" alt="Xiaomi-MiMo" />
  </picture>
</div>

<h3 align="center">
  <b>
    <span>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>
    <br/>
    从预训练到后训练，解锁语言模型的推理潜能<br/>Unlocking the Reasoning Potential of Language Model From Pretraining to Posttraining
    <br/>
    <span>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>
    <br/>
  </b>
</h3>

<br/>

<div align="center" style="line-height: 1;">
  |
  <a href="https://huggingface.co/XiaomiMiMo" target="_blank">🤗 HuggingFace</a>
  &nbsp;|
  <a href="https://www.modelscope.cn/organization/XiaomiMiMo" target="_blank">🤖️ ModelScope</a>
  &nbsp;|
  <a href="https://arxiv.org/abs/2505.07608" target="_blank">📔 技术报告</a>
  &nbsp;|
  <br/>
</div>

<br/>

---

## 更新

[2025.05.30] 我们将 SFT 数据集从约 50 万条扩展到 600 万条，并将 RL 训练窗口大小从 32K 持续扩大到 48K，[MiMo-7B-RL-0530](https://huggingface.co/XiaomiMiMo/MiMo-7B-RL-0530) 在 AIME24 上的性能得以持续提升，并最终超过 DeepSeek R1（79.8）。

<table>
  <thead>
    <tr>
      <th>基准测试</th>
      <th>MiMo-7B-RL</th>
      <th>MiMo-7B-RL-0530</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="3"><strong>数学</strong></td>
      <p align="center">
        <td rowspan="11"><img width="80%" src="https://github.com/XiaomiMiMo/MiMo/raw/main/figures/length.jpg?raw=true"></td>
      </p>
    </tr>
    <tr><td>MATH500<br/>(Pass@1)</td><td>95.8</td><td>97.2</td></tr>
    <tr><td>AIME 2024<br/>(Pass@1)</td><td>68.2</td><td>80.1</td></tr>
    <tr><td>AIME 2025<br/>(Pass@1)</td><td>55.4</td><td>70.2</td></tr>
    <tr><td colspan="3"><strong>代码</strong></td></tr>
    <tr><td>LiveCodeBench v5<br/>(Pass@1)</td><td>57.8</td><td>60.9</td></tr>
    <tr><td>LiveCodeBench v6<br/>(Pass@1)</td><td>49.3</td><td>52.2</td></tr>
    <tr><td colspan="3"><strong>STEM</strong></td></tr>
    <tr><td>GPQA-Diamond<br/>(Pass@1)</td><td>54.4</td><td>60.6</td></tr>
    <tr><td colspan="3"><strong>通用</strong></td></tr>
    <tr><td>Alignbench1.1<br/>(由 GPT4.1 评测)</td><td>6.9</td><td>7.4</td></tr>
  </tbody>
</table>

---

## 一、引言

目前，大多数成功的 RL 工作（包括开源研究）都依赖相对较大的基座模型（例如 32B 模型），尤其是在提升代码推理能力方面。此外，人们普遍认为在小模型中同时、一致地提升数学与代码两项能力十分困难。尽管如此，我们相信 RL 训练出的推理模型的效果，取决于基座模型固有的推理潜能。要充分解锁语言模型的推理潜能，努力方向不仅在后训练，还在于面向推理定制的预训练策略。

在本工作中，我们提出 MiMo-7B——一系列从零开始训练、为推理任务而生的模型。我们基于 MiMo-7B-Base 的 RL 实验表明，我们的模型拥有非凡的推理潜能，甚至超过了规模大得多的 32B 模型。此外，我们在冷启动的 SFT 模型上进行 RL 训练，得到 MiMo-7B-RL，它在数学和代码推理任务上都表现出卓越性能，可匹敌 OpenAI o1-mini。

<p align="center">
  <img width="80%" src="https://github.com/XiaomiMiMo/MiMo/raw/main/figures/curve.png?raw=true">
</p>

我们开源 MiMo-7B 系列，包括基座模型、SFT 模型、从基座模型训练的 RL 模型以及从 SFT 模型训练的 RL 模型的检查点。
我们相信这份报告连同模型将为开发强大的推理 LLM 提供有价值的洞见，惠及更广大的社区。

### 🌟 亮点

- **预训练：为推理而生的基座模型**
  - 我们优化了数据预处理流水线，增强文本抽取工具链并应用多维度数据过滤，以提高预训练数据中的推理模式密度。我们还采用多种策略生成海量、多样的合成推理数据。
  - 我们在预训练中采用三阶段数据配比策略。总体上，MiMo-7B-Base 在约 25 万亿（25 trillion）token 上完成预训练。
  - 我们引入多 token 预测（Multiple-Token Prediction，MTP）作为附加训练目标，既提升模型性能又加速推理。

- **后训练配方：推理模型的先行探索**
    - 我们精选了 13 万道数学与代码题目作为 RL 训练数据，可由基于规则的验证器验证。每道题都经过仔细清洗和难度评估以确保质量。我们仅使用基于规则的准确性奖励，以避免潜在的奖励作弊（reward hacking）。
    - 为缓解高难度代码题目奖励稀疏的问题，我们引入由测试难度驱动的代码奖励。通过为不同难度的测试用例赋予细粒度分数，策略可以通过密集的奖励信号得到更有效的优化。
    - 我们针对简单题目实现了数据重采样策略，以提高 rollout 采样效率并稳定策略更新，尤其是在 RL 训练的后期阶段。

- **RL 基础设施**
    - 我们开发了无缝 Rollout 引擎（Seamless Rollout Engine）以加速 RL 训练与验证。该设计融合连续 rollout、异步奖励计算和提前终止，最大限度减少 GPU 空闲时间，实现训练提速 $2.29\times$、验证提速 $1.96\times$。
    - 我们在 vLLM 中支持 MTP，并增强 RL 系统中推理引擎的鲁棒性。

## 二、模型细节

MiMo-7B 的 MTP 层在预训练和 SFT 阶段参与调优，在 RL 阶段被冻结。使用一个 MTP 层做投机解码（speculative decoding）时，接受率约为 90%。

<p align="center">
  <img width="80%" src="https://github.com/XiaomiMiMo/MiMo/raw/main/figures/architecture.png?raw=true">
</p>

> 模型可在 [https://huggingface.co/XiaomiMiMo](https://huggingface.co/XiaomiMiMo) 与 [https://www.modelscope.cn/organization/XiaomiMiMo](https://www.modelscope.cn/organization/XiaomiMiMo) 获取

|    **模型**    |                                **描述**                                |                            **下载（HuggingFace）**                             |                                  **下载（ModelScope）**                                  |
| :-------------: | :---------------------------------------------------------------------------: | :-------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------: |
|  MiMo-7B-Base   |               具有非凡推理潜能的基座模型               |    [🤗 XiaomiMiMo/MiMo-7B-Base](https://huggingface.co/XiaomiMiMo/MiMo-7B-Base)    |    [🤖️ XiaomiMiMo/MiMo-7B-Base](https://www.modelscope.cn/models/XiaomiMiMo/MiMo-7B-Base)    |
| MiMo-7B-RL-Zero |                       从基座模型训练的 RL 模型                        | [🤗 XiaomiMiMo/MiMo-7B-RL-Zero](https://huggingface.co/XiaomiMiMo/MiMo-7B-RL-Zero) | [🤖️ XiaomiMiMo/MiMo-7B-RL-Zero](https://www.modelscope.cn/models/XiaomiMiMo/MiMo-7B-RL-Zero) |
|   MiMo-7B-SFT   |                       从基座模型训练的 SFT 模型                       |     [🤗 XiaomiMiMo/MiMo-7B-SFT](https://huggingface.co/XiaomiMiMo/MiMo-7B-SFT)     |     [🤖️ XiaomiMiMo/MiMo-7B-SFT](https://www.modelscope.cn/models/XiaomiMiMo/MiMo-7B-SFT)     |
|   MiMo-7B-RL    | 从 SFT 模型训练的 RL 模型，性能卓越、匹敌 OpenAI o1-mini |      [🤗 XiaomiMiMo/MiMo-7B-RL](https://huggingface.co/XiaomiMiMo/MiMo-7B-RL)      |      [🤖️ XiaomiMiMo/MiMo-7B-RL](https://www.modelscope.cn/models/XiaomiMiMo/MiMo-7B-RL)      |

## 三、评测结果

| 基准测试                     | GPT-4o-0513 | Claude-3.5-Sonnet-1022 | OpenAI o1-mini | QwQ-32B-Preview | R1-Distill-Qwen-14B | R1-Distill-Qwen-7B | MiMo-7B-RL |
| ----------------------------- | :---------: | :--------------------: | :------------: | :-------------: | :-----------------: | :----------------: | :--------: |
| **通用**                   |             |                        |                |                 |                     |                    |            |
| GPQA Diamond<br/>(Pass@1)     |    49.9     |          65.0          |      60.0      |      54.5       |        59.1         |        49.1        |    54.4    |
| SuperGPQA<br/>(Pass@1)        |    42.4     |          48.2          |      45.2      |      43.6       |        40.6         |        28.9        |    40.5    |
| DROP<br/>(3-shot F1)          |    83.7     |          88.3          |      83.9      |      71.2       |        85.5         |        77.0        |    78.7    |
| MMLU-Pro<br/>(EM)             |    72.6     |          78.0          |      80.3      |      52.0       |        68.8         |        53.5        |    58.6    |
| IF-Eval<br/>(Prompt Strict)   |    84.3     |          86.5          |      84.8      |      40.4       |        78.3         |        60.5        |    61.0    |
| **数学**               |             |                        |                |                 |                     |                    |            |
| MATH-500<br/>(Pass@1)         |    74.6     |          78.3          |      90.0      |      90.6       |        93.9         |        92.8        |    95.8    |
| AIME 2024<br/>(Pass@1)        |     9.3     |          16.0          |      63.6      |      50.0       |        69.7         |        55.5        |    68.2    |
| AIME 2025<br/>(Pass@1)        |    11.6     |          7.4           |      50.7      |      32.4       |        48.2         |        38.8        |    55.4    |
| **代码**                      |             |                        |                |                 |                     |                    |            |
| LiveCodeBench v5<br/>(Pass@1) |    32.9     |          38.9          |      53.8      |      41.9       |        53.1         |        37.6        |    57.8    |
| LiveCodeBench v6<br/>(Pass@1) |    30.9     |          37.2          |      46.8      |      39.1       |        31.9         |        23.9        |    49.3    |

MiMo-7B 系列

| 基准测试                     | MiMo-7B-Base | MiMo-7B-RL-Zero | MiMo-7B-SFT | MiMo-7B-RL |
| ----------------------------- | :----------: | :-------------: | :---------: | :--------: |
| **数学**               |              |                 |             |            |
| MATH500<br/>(Pass@1)          |     37.4     |      93.6       |    93.0     |    95.8    |
| AIME 2024<br/>(Pass@1)        |     32.9     |      56.4       |    58.7     |    68.2    |
| AIME 2025<br/>(Pass@1)        |     24.3     |      46.3       |    44.3     |    55.4    |
| **代码**                      |              |                 |             |            |
| LiveCodeBench v5<br/>(Pass@1) |     32.9     |      49.1       |    52.3     |    57.8    |
| LiveCodeBench v6<br/>(Pass@1) |     29.1     |      42.9       |    45.5     |    49.3    |

> [!IMPORTANT]
> 评测均使用 `temperature=0.6` 进行。
>
> AIME24 与 AIME25 为 32 次重复的平均分。LiveCodeBench v5（20240801-20250201）、LiveCodeBench v6（20250201-20250501）、GPQA-Diamond 与 IF-Eval 为 8 次重复的平均分。MATH500 与 SuperGPQA 为单次运行。

## 四、部署

### SGLang 推理

感谢 SGLang 团队提供的 [MiMo 模型支持](https://github.com/sgl-project/sglang/pull/5921) 与 [MTP](https://github.com/sgl-project/sglang/pull/6059)，我们在 SGLang 主线中支持了 MiMo。

示例脚本

```bash
# Install the latest SGlang from main branch
python3 -m uv pip install "sglang[all] @ git+https://github.com/sgl-project/sglang.git/@main#egg=sglang&subdirectory=python"

# Launch SGLang Server
python3 -m sglang.launch_server --model-path XiaomiMiMo/MiMo-7B-RL-0530 --host 0.0.0.0 --trust-remote-code

# Launch MTP Server
python3 -m sglang.launch_server --model-path XiaomiMiMo/MiMo-7B-RL-0530 --trust-remote-code \
--speculative-algorithm EAGLE --speculative-num-steps 1 --speculative-eagle-topk 1 \
--speculative-num-draft-tokens 2  --mem-fraction 0.5
```

详细用法见 [SGLang 文档](https://docs.sglang.ai/backend/send_request.html)。

### vLLM 推理

1. [推荐] 我们官方支持使用 [我们的 vLLM 分支](https://github.com/XiaomiMiMo/vllm/tree/feat_mimo_mtp_stable_073) 进行带 MiMo-MTP 的推理。

示例脚本

```py
from vllm import LLM, SamplingParams

model_path = "/path/to/MiMo"
llm = LLM(
    model=model_path,
    trust_remote_code=True,
    num_speculative_tokens=1,
    disable_log_stats=False
)
sampling_params = SamplingParams(temperature=0.6)

conversation = [
    {
        "role": "system",
        "content": ""
    },
    {
        "role": "user",
        "content": "Write an essay about the importance of higher education.",
    },
]

outputs = llm.chat(conversation,
                   sampling_params=sampling_params,
                   use_tqdm=False)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

print("=" * 80)
```

2. 或者，你可以为 MiMo 注册一个 vLLM 加载器，而不加载 MTP 参数。

你可以将 [`registry/register_mimo_in_vllm.py`](https://github.com/XiaomiMiMo/MiMo/blob/main/registry/register_mimo_in_vllm.py) 复制到你的目录中，然后如下导入：

```py
import register_mimo_in_vllm

from vllm import LLM, SamplingParams

model_path = "/path/to/MiMo"
llm = LLM(
    model=model_path,
    trust_remote_code=True,
    # num_speculative_tokens=1,
    disable_log_stats=False
)
sampling_params = SamplingParams(temperature=0.6)
```

### HuggingFace 推理

示例脚本

```py
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer

model_id = "XiaomiMiMo/MiMo-7B-RL-0530"
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
inputs = tokenizer(["Today is"], return_tensors='pt')
output = model.generate(**inputs, max_new_tokens = 100)
print(tokenizer.decode(output.tolist()[0]))
```

### 推荐的环境与提示词

- 我们推荐使用 [我们的 vLLM 分支](https://github.com/XiaomiMiMo/vllm/tree/feat_mimo_mtp_stable_073)，它基于 vLLM 0.7.3 开发。
- 我们推荐使用空系统提示词（system prompt）。

> 我们尚未在其他推理引擎上验证 MiMo，欢迎基于 Huggingface 仓库中的模型定义进行贡献 💻。

## 五、引用

```bibtex
@misc{coreteam2025mimounlockingreasoningpotential,
      title={MiMo: Unlocking the Reasoning Potential of Language Model -- From Pretraining to Posttraining}, 
      author={LLM-Core-Team Xiaomi},
      year={2025},
      eprint={2505.07608},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2505.07608}, 
}
```


## 六、联系方式

如有任何问题，请通过 [mimo@xiaomi.com](mailto:mimo@xiaomi.com) 联系我们，或提交 issue。

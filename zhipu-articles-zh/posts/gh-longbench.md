---
title: "LongBench v2：面向现实长上下文多任务的深度理解与推理"
source: https://github.com/THUDM/LongBench
crawled: 2026-09-22
title_en: "LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks"
translated: 2026-09-22
---

# LongBench v2：面向现实长上下文多任务的深度理解与推理

> 原文：[LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks](https://github.com/THUDM/LongBench) · 智谱 Z.ai / THUDM

![](LongBench/misc/logo.gif)

<p align="center">
    🌐 <a href="https://longbench2.github.io" target="_blank">项目主页</a> • 📚 <a href="https://arxiv.org/abs/2412.15204" target="_blank">LongBench v2 论文</a> • 📊 <a href="https://huggingface.co/datasets/THUDM/LongBench-v2" target="_blank">LongBench v2 数据集</a> • 𝕏 <a href="https://x.com/realYushiBai/status/1869946577349132766" target="_blank">推文串</a>
</p>
<p align="center">
    📖 <a href="https://arxiv.org/abs/2308.14508" target="_blank">LongBench 论文</a> • 🤗 <a href="https://huggingface.co/datasets/THUDM/LongBench" target="_blank">LongBench 数据集</a>
</p>

**📢 原 LongBench v1 相关文件已移动到 `LongBench/` 目录下，其 README 请在[这里](LongBench/README.md)阅读**。

LongBench v2 旨在评估 LLM 处理长上下文问题的能力，这些问题需要在现实世界的多任务中进行**深度理解与推理**。LongBench v2 具有以下特点：(1) **长度**：上下文长度从 8k 到 2M 词，大多数在 128k 以下。(2) **难度**：足够具有挑战性，即使是人类专家，在文档内使用搜索工具也无法在短时间内答对。(3) **覆盖面**：覆盖多种现实场景。(4) **可靠性**：全部采用多项选择题格式，以保证评估的可靠性。

具体而言，LongBench v2 由 503 道有挑战性的多项选择题组成，上下文长度从 8k 到 2M 词，涵盖六大任务类别：单文档问答、多文档问答、长上下文学习（long in-context learning）、长对话历史理解、代码仓库理解与长结构化数据理解。为确保广度与实用性，我们从近 100 位拥有多样职业背景的高学历人士处收集数据。我们采用自动化与人工相结合的审查流程来保持高质量与高难度，最终人类专家在 15 分钟时限下的准确率仅为 53.7%。我们的评测显示，表现最好的模型在直接回答问题时准确率仅为 50.1%。相比之下，包含更长推理过程的 o1-preview 模型取得了 57.7% 的准确率，超越人类基线 4 个百分点。这些结果凸显了**增强推理能力并扩展推理时计算（scaling inference-time compute）对于应对 LongBench v2 长上下文挑战的重要性**。

**🔍 借助 LongBench v2，我们希望弄清扩展推理时计算将如何影响长上下文场景下的深度理解与推理。欢迎查看我们的 🏆 排行榜[这里](https://longbench2.github.io/#leaderboard)（持续更新）。**

<div style="text-align: center;">
  <img src="misc/length.png" width="600" />
</div>

<div style="text-align: center;">
  <img src="misc/table.png" width="700" />
</div>

## 🔥 更新
🔥🔥🔥 **[2024/01/15]** 我们的[排行榜](https://longbench2.github.io/#leaderboard)新增了更多评测结果，包括 Gemini-Exp-1206、Gemini-2.0-Flash、DeepSeek-V3 与 MiniMax-Text-01，快去看看吧！

🔥🔥🔥 **[2024/12/20]** 我们很高兴地发布 **LongBench v2**！与第一代 LongBench 相比，LongBench v2 更长、更具挑战性。它的目标是为未来超人类长上下文 AI 系统的发展提供可靠的评估标准。

## ⚙️ 如何在 LongBench v2 上评测

### 加载数据
你可以通过 Hugging Face datasets 下载并加载 **LongBench v2** 数据（[🤗 HF 仓库](https://huggingface.co/datasets/THUDM/LongBench-v2)）：
```python
from datasets import load_dataset
dataset = load_dataset('THUDM/LongBench-v2', split='train')
```
或者，你也可以从[此链接](https://huggingface.co/datasets/THUDM/LongBench-v2/resolve/main/data.json)下载文件来加载数据。

### 数据格式

**LongBench v2** 中的所有数据都标准化为以下格式：

```json
{
    "_id": "Unique identifier for each piece of data",
    "domain": "The primary domain category of the data",
    "sub_domain": "The specific sub-domain category within the domain",
    "difficulty": "The difficulty level of the task, either 'easy' or 'hard'",
    "length": "The length category of the task, which can be 'short', 'medium', or 'long'",
    "question": "The input/command for the task, usually short, such as questions in QA, queries in many-shot learning, etc",
    "choice_A": "Option A", "choice_B": "Option B", "choice_C": "Option C", "choice_D": "Option D",
    "answer": "The groundtruth answer, denoted as A, B, C, or D",
    "context": "The long context required for the task, such as documents, books, code repositories, etc."
}
```

### 评测
使用 pip 安装依赖：`pip install -r requirements.txt`。

要运行模型评测，首先将你的模型路径及其上下文窗口长度添加到 `config/`，然后按以下步骤操作（我们以 [GLM-4-9B-Chat](https://github.com/THUDM/GLM-4) 为运行示例）：

#### 步骤 1：使用 vLLM 部署模型

首先，使用 [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) 部署你的模型。运行以下命令来提供模型服务：

```bash
vllm serve THUDM/glm-4-9b-chat --api-key token-abc123 --tensor-parallel-size 4 --gpu-memory-utilization 0.95 --max_model_len 131072 --trust-remote-code
```

- `--tensor-parallel-size 4` 指定张量并行的切分数量。对于 [Llama-3.1-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct) 或 [Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct) 等更大的模型，应设置为更高的值，例如 8。
- 调整 `--gpu-memory-utilization` 以控制 GPU 显存占用。
- 将 `--max_model_len` 设置为模型的上下文窗口长度。

#### 步骤 2：运行模型推理

模型部署完成后，修改 `pred.py` 中的 `URL` 与 `API_KEY` 以匹配你的服务实例。使用以下命令运行模型推理：

```bash
python pred.py --model GLM-4-9B-Chat
```
- `--cot`：在思维链（CoT）设定下进行评测。
- `--no_context`：测试模型在没有长上下文时的表现（纯记忆能力）。
- `--rag N`：在 +RAG 评测期间使用 top-N 检索到的上下文。默认设为 0 以禁用 RAG。检索流程的细节请参考 [retrieve.py](https://github.com/THUDM/LongCite/blob/main/utils/retrieve.py) 文件。

#### 步骤 3：导出结果

最后，运行 `python result.py` 导出评测结果。

## 📝 引用
```
@article{bai2024longbench2,
  title={LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks}, 
  author={Yushi Bai and Shangqing Tu and Jiajie Zhang and Hao Peng and Xiaozhi Wang and Xin Lv and Shulin Cao and Jiazheng Xu and Lei Hou and Yuxiao Dong and Jie Tang and Juanzi Li},
  journal={arXiv preprint arXiv:2412.15204},
  year={2024}
}
@inproceedings{bai2024longbench,
    title = "{L}ong{B}ench: A Bilingual, Multitask Benchmark for Long Context Understanding",
    author = "Bai, Yushi and Lv, Xin  and Zhang, Jiajie  and Lyu, Hongchang  and
      Tang, Jiankai  and Huang, Zhidian  and Du, Zhengxiao  and Liu, Xiao  and Zeng, Aohan  and Hou, Lei  and Dong, Yuxiao  and Tang, Jie  and Li, Juanzi",
    booktitle = "Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2024",
    address = "Bangkok, Thailand",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.acl-long.172",
    doi = "10.18653/v1/2024.acl-long.172",
    pages = "3119--3137",
}
```

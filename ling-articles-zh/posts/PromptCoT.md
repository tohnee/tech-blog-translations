---
title: "PromptCoT 2.0：面向 LLM 推理的提示合成扩展"
title_en: "inclusionAI/PromptCoT"
source: https://github.com/inclusionAI/PromptCoT/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# PromptCoT 2.0：面向 LLM 推理的提示合成扩展

> 原文：[inclusionAI/PromptCoT](https://github.com/inclusionAI/PromptCoT/blob/main/README.md) · 蚂蚁集团 InclusionAI

<h1 align="center">PromptCoT 2.0</h1>

<p align="center">
  <b>面向 LLM 推理的提示合成扩展</b>
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2509.19894">📄 论文</a> •
  <a href="https://huggingface.co/collections/xl-zhao/promptcot-20-68d27cd73f2faef5a12f777d">🤗 Hugging Face</a>
</p>

<p align="center">
  <img src="assets/d54677c190135988a485751bb8ebb268.png" alt="PromptCoT 2.0 Logo" width="600"/>
</p>

---

## ✨ 概述

PromptCoT 2.0 是一个有原则、可扩展的**提示合成（prompt synthesis）**框架，大幅推进了 LLM 在**数学**与**编程**上的推理能力。

它引入了 **EM 风格的推理链路驱动的合成循环**（*概念 → 解题思路 → 题目*），实现大规模自动生成多样且具有挑战性的题目。这些合成提示支持两种互补的训练范式：

**自我博弈（Self-Play）**：模型通过从可验证信号（例如代码的单元测试、数学的 boxed 答案）中学习而自主提升。借助这一方法，一个 **30B-A3B 自我博弈模型**在 **AIME24 上取得 92.1、AIME25 上取得 89.8、HMMT Feb25 上取得 76.7**，并在 **LiveCodeBench v5 上取得 74.2、v6 上取得 71.0、Codeforces 上取得 2079 Elo**。这些结果超越了强大的开源基线（Qwen3-30B-A3B-Thinking），并在数学与代码上取得与 Gemini 2.5 Pro、OpenAI o3 等闭源领先模型**有竞争力的性能**。

**SFT**：一个 **100% 使用合成数据**训练的 **7B** 模型——使用 PromptCoT 2.0 合成的提示与**从 GPT-OSS-120B（medium）蒸馏的完整推理轨迹**——达到 **AIME24 73.1、AIME25 65.6、Codeforces 1815 Elo**，超越了使用**人工编写提示**训练的对照模型。


释放 PromptCoT 的推理浪潮吧！

---

## ⚡ 主要结果

**自我博弈 @ Qwen3-30B-A3B-2507-Thinking：**

<p align="center">
  <img src="assets/87abc8046464863cfd1149fc94e47747.png" width="95%" alt="PromptCoT 2.0 Self-Play (30B-A3B) vs baselines"/>
</p>
<p align="center">
  <em>
  PromptCoT 2.0 证明，带可验证信号的大规模<b>自我博弈</b>对推进 LLM 推理行之有效。
  在 30B 规模上，自我博弈取得了与闭源领先模型（Gemini 2.5 Pro、OpenAI o3）有竞争力的性能，并超越强大的开源基线。
  </em>
</p>

**SFT @ Qwen2.5-7B-Instruct：**

<p align="center">
  <img src="assets/2ec3a1b84d730fa20c30e9f8079860a3.png" width="95%" alt="PromptCoT 2.0 SFT (7B) vs OpenCodeReasoning vs OpenMathReasoning"/>
</p>
<p align="center">
  <em>
  PromptCoT 2.0（7B，SFT）是<b>首个完全基于合成提示训练</b>、轨迹蒸馏自 GPT-OSS-120B 的模型。
  与均基于<b>人工编写提示</b>的 OpenCodeReasoning 和 OpenMathReasoning 不同，PromptCoT 2.0 取得了更强的性能，凸显了<b>全合成提示合成</b>作为推理模型基础的潜力。
  </em>
</p>

---

## 🔮 版本发布

[2025/10/26] 我们发布了**题目生成配方**（`problem_generation.sh`），可以从概念文件完整复现 PromptCoT 2.0 的可扩展合成流水线。


[2025/09/24] 我们发布 [PromptCoT 2.0](https://arxiv.org/abs/2509.19894)：
首个将提示合成同时扩展到数学与编程的框架，使 30B 自我博弈模型可与 Gemini 2.5 Pro / OpenAI o3 竞争，7B SFT（100% 合成提示）超越人工编写基线。

**📂 资源**
- **SFT 数据（480 万条全合成提示 + 轨迹）**：[PromptCoT-2.0-SFT-4.8M](https://huggingface.co/datasets/xl-zhao/PromptCoT-2.0-SFT-4.8M)。
- **SFT 模型（7B）**：[PromptCoT-2.0-SFT-7B](https://huggingface.co/xl-zhao/PromptCoT-2.0-SFT-7B)。
- **自我博弈数据**：[PromptCoT-2.0-SelfPlay-30B-11K](https://huggingface.co/datasets/xl-zhao/PromptCoT-2.0-SelfPlay-30B-11K) 与 [PromptCoT-2.0-SelfPlay-4B-48K](https://huggingface.co/datasets/xl-zhao/PromptCoT-2.0-SelfPlay-4B-48K)。
- **自我博弈模型**：[PromptCoT-2.0-SelfPlay-30B-A3B](https://huggingface.co/xl-zhao/PromptCoT-2.0-SelfPlay-30B-A3B) 与 [PromptCoT-2.0-SelfPlay-4B](https://huggingface.co/xl-zhao/PromptCoT-2.0-SelfPlay-4B)。
- **题目生成模型**：[PromptCoT-2.0-Prompt-Generation-Model](https://huggingface.co/xl-zhao/PromptCoT-2.0-Prompt-Generation-Model)。


[2025/05/30] 我们发布 [PromptCoT-Mamba](https://arxiv.org/abs/2505.22425)（[🤗 PromptCoT-Mamba-7B](https://huggingface.co/xl-zhao/PromptCoT-Mamba-7B)）：
首个免注意力（attention-free）推理模型，将 PromptCoT 与 Mamba-2 结合，以常数内存推理实现强大的数学与代码性能。


[2025/04/11] 我们发布 [PromptCoT-QwQ-32B](https://huggingface.co/xl-zhao/PromptCoT-QwQ-32B) 与 [PromptCoT-QwQ-Dataset](https://huggingface.co/datasets/xl-zhao/PromptCoT-QwQ-Dataset)：
使用 PromptCoT 合成题目对 QwQ-32B 进行自我博弈，并发布配套数据集以支持可复现训练。


[2025/03/07] 我们发布 [PromptCoT 1.0](http://arxiv.org/abs/2503.02324)（🤗 [HF 合集](https://huggingface.co/collections/xl-zhao/promptcot-10-68d27ce16efc9cbad4b5c878)）：
首个面向奥赛级数学题的推理链路驱动合成流水线，发布了题目生成模型、蒸馏模型与数据集。


---

## 快速开始

```bash
git clone https://github.com/inclusionAI/PromptCoT
cd PromptCoT
pip install -r requirements.txt
````

---

## 配置

顶层脚本支持从本地 `.env` 文件加载默认配置值。

1. 将 `.env.example` 复制为 `.env`
2. 编辑取值（例如 `MODEL_PATH`、`N_GPUS`、`DATA_PATH`、`OUTPUT_PATH`）
3. 校验你的配置：

```bash
python validate_config.py
```

说明：
- 优先级为 `CLI 参数 > .env > 代码默认值`。
- `MODEL_PATH` / `TOKENIZER_PATH` 可以是本地路径或 Hugging Face 模型 id；校验器只检查文件系统路径。
- `.env` 中的空字符串视为「未设置」（例如 `DATA_PATH=` 等同于未设置）。
- 建议使用带命名空间的环境变量（例如 `SPLIT_MERGE_OUTPUT_PATH`、`SELF_PLAY_OUTPUT_PATH`），避免从同一 `.env` 运行多个脚本时发生冲突。
- 部分脚本历史上使用了不同的环境变量名（例如 `infer_split_merge.py` 使用 `N_SPLITS`，而 `infer_self_play.py` 使用 `NUM_SPLITS`）；`.env.example` 记录了映射关系，代码中也为这些情况提供了小的回退逻辑。

运行本仓库的轻量单元测试：

```bash
python -m unittest discover -s tests -v
```

---

## 🧩 题目生成（概念 → 解题思路 → 题目）

我们提供脚本，使用 PromptCoT 2.0 流水线从概念文件合成题目。

- **概念文件**：可在 **[xl-zhao/PromptCoT-2.0-Concepts](https://huggingface.co/datasets/xl-zhao/PromptCoT-2.0-Concepts)** 获取（例如 `PromptCoT-2.0-Concepts/code.jsonl`）。
- **模型**：将脚本中的 `--model_path` 设为你的 **PromptCoT-2.0-Prompt-Generation-Model**（链接见版本发布）。

**为脚本添加可执行权限并运行：**

````bash
chmod +x problem_generation.sh
./problem_generation.sh
````

---

## 自我博弈流水线（代码示例）

我们在**代码领域**演示自我博弈工作流，其中单元测试提供可验证的奖励信号。

---

**第 1 步 — 可验证奖励生成（测试用例构建）**
输入的 `.jsonl` 文件中每个实例必须包含 `"problem"` 字段，指明要解决的编程任务。
每轮运行会生成一个新的测试用例并追加到 `"completions"` 字段，逐步丰富任务规约。

````bash
# Generate 4 rounds of test cases with different seeds
for seed in {0..3}; do
  python test_cases_generation.py \
    --seed $seed \
    --data_path code/prompts_test_cases_${seed}.jsonl \
    --output_path code/prompts_test_cases_$((seed+1)).jsonl \
    --model_path Qwen/Qwen3-32B \
    --n_gpus 4 \
    --temperature 0.6 \
    --max_len 16384 \
    --use_chat_template True
done
````

将生成的测试用例后处理为结构化格式：

````bash
python test_cases_postprocess.py \
  --input_file code/prompts_test_cases_4.jsonl \
  --output_path code/prompts_test_cases_processed.jsonl
````

---

**第 2 步 — 自我博弈轨迹收集**
使用处理后的测试用例，通过跨多个种子采样生成多样的轨迹：

````bash
for seed in {0..7}; do
  python infer_self_play.py \
    --data_path code/selfplay_${seed}.jsonl \
    --output_path code/selfplay_$((seed+1)).jsonl \
    --model_path Qwen/Qwen3-30B-A3B-Thinking-2507 \
    --trust_remote_code True \
    --n_gpus 8 \
    --num_splits 4 \
    --num_completions 8 \
    --seed $seed \
    --temperature 1.2 \
    --max_len 81920 \
    --use_chat_template True
done
````

---

**第 3 步 — 奖励分配**
针对构建的测试用例评估每条轨迹，并自动赋予奖励信号：

````bash
python self_play_eval.py \
  --data_path code/selfplay_8.jsonl \
  --output_path code/selfplay_verified.jsonl \
  --eval_type code \
  --num_workers 16
````

---

**第 4 步 — 样本对构建**
将通过验证的轨迹聚合为 **chosen 与 rejected** 对，用于离线自我博弈训练：

````bash
python prepare_self_play_data.py \
  --data_path code/selfplay_verified.jsonl \
  --output_path code/selfplay_training.jsonl
````

---

## SFT 流水线（代码示例）

我们在**代码领域**演示 SFT 工作流，使用来自 GPT-OSS-120B 的教师轨迹。

---

**第 1 步 — 教师轨迹收集**
为每个提示采样教师回复，每题一条轨迹：

````bash
python infer_self_play.py \
  --data_path code/prompts_test_cases_processed.jsonl \
  --output_path code/prompts_trajectories.jsonl \
  --model_path openai/gpt-oss-120b \
  --trust_remote_code True \
  --n_gpus 8 \
  --num_splits 4 \
  --num_completions 1 \
  --seed 0 \
  --temperature 1.0 \
  --max_len 16384 \
  --use_chat_template True
````

---

**第 2 步 — 数据后处理**
过滤不完整或无效的轨迹，并格式化为干净的 prompt–completion 对，用于监督微调：

````bash
python prepare_sft_data_code.py \
  --data_path code/prompts_trajectories.jsonl \
  --output_path code/sft_training.jsonl \
  --tokenizer_path Qwen/Qwen2.5-7B-Instruct
````



---

## 基准结果复现

我们提供脚本以复现**自我博弈**与 **SFT** 模型的结果。
对于数学评测，我们建议设置 `VLLM_USE_V1=0` 以确保可复现性。

---

**自我博弈模型**

*30B-A3B（数学）*
````bash
for dataset in aime24 aime25 hmmt25; do
  python infer_split_merge.py \
    --data_path data/promptcot2_${dataset}_test.jsonl \
    --output_path qwen_evals/30b_a3b/${dataset}.jsonl \
    --model_path /path/to/PromptCoT-2.0-SelfPlay-30B-A3B \
    --n_splits 4 \
    --expected_runs 16 \
    --temperature 0.6 \
    --top_p 0.95 \
    --max_len 81920 \
    --factor 1.75 \
    --original_max_position_embeddings 262144
done
````

*30B-A3B（代码）*

````bash
# Codeforces
python infer_split_merge.py \
  --data_path data/promptcot2_codeforces_test.jsonl \
  --output_path qwen_evals/30b_a3b/codeforces.jsonl \
  --model_path /path/to/PromptCoT-2.0-SelfPlay-30B-A3B \
  --n_splits 1 \
  --expected_runs 8 \
  --temperature 0.6 \
  --top_p 0.95 \
  --max_len 81920 \
  --factor 1.75 \
  --original_max_position_embeddings 262144

# LiveCodeBench v5 / v6
for dataset in lcb_v5 lcb_v6; do
  python infer_split_merge.py \
    --data_path data/promptcot2_${dataset}_test.jsonl \
    --output_path qwen_evals/30b_a3b/${dataset}.jsonl \
    --model_path /path/to/PromptCoT-2.0-SelfPlay-30B-A3B \
    --n_splits 1 \
    --expected_runs 1 \
    --temperature 0.6 \
    --top_p 0.95 \
    --max_len 81920 \
    --factor 1.75 \
    --original_max_position_embeddings 262144
done
````

*4B（数学）*

````bash
for dataset in aime24 aime25 hmmt25; do
  python infer_split_merge.py \
    --data_path data/promptcot2_${dataset}_test.jsonl \
    --output_path qwen_evals/4b/${dataset}.jsonl \
    --model_path /path/to/PromptCoT-2.0-SelfPlay-4B \
    --n_splits 8 \
    --expected_runs 16 \
    --temperature 0.6 \
    --top_p 0.95 \
    --max_len 81920 \
    --factor 1.75 \
    --original_max_position_embeddings 262144
done
````

*4B（代码）*

````bash
# Codeforces
python infer_split_merge.py \
  --data_path data/promptcot2_codeforces_test.jsonl \
  --output_path qwen_evals/4b/codeforces.jsonl \
  --model_path /path/to/PromptCoT-2.0-SelfPlay-4B \
  --n_splits 4 \
  --expected_runs 8 \
  --temperature 0.6 \
  --top_p 0.95 \
  --max_len 81920 \
  --factor 1.75 \
  --original_max_position_embeddings 262144

# LiveCodeBench v5 / v6
for dataset in lcb_v5 lcb_v6; do
  python infer_split_merge.py \
    --data_path data/promptcot2_${dataset}_test.jsonl \
    --output_path qwen_evals/4b/${dataset}.jsonl \
    --model_path /path/to/PromptCoT-2.0-SelfPlay-4B \
    --n_splits 8 \
    --expected_runs 1 \
    --temperature 0.6 \
    --top_p 0.95 \
    --max_len 81920 \
    --factor 1.75 \
    --original_max_position_embeddings 262144
done
````

---

**SFT 模型（7B）**

*数学*

````bash
for dataset in aime24 aime25 hmmt25; do
  python infer_split_merge.py \
    --data_path data/promptcot2_${dataset}_test.jsonl \
    --output_path qwen_evals/sft/${dataset}.jsonl \
    --model_path /path/to/PromptCoT-2.0-SFT-7B \
    --n_splits 8 \
    --expected_runs 16 \
    --temperature 0.6 \
    --top_p 0.95 \
    --max_len 81920
done
````

*代码*

````bash
# Codeforces
python infer_split_merge.py \
  --data_path data/promptcot2_codeforces_test.jsonl \
  --output_path qwen_evals/sft/codeforces.jsonl \
  --model_path /path/to/PromptCoT-2.0-SFT-7B \
  --n_splits 8 \
  --expected_runs 8 \
  --temperature 0.6 \
  --top_p 0.95 \
  --max_len 81920

# LiveCodeBench v5 / v6
for dataset in lcb_v5 lcb_v6; do
  python infer_split_merge.py \
    --data_path data/promptcot2_${dataset}_test.jsonl \
    --output_path qwen_evals/sft/${dataset}.jsonl \
    --model_path /path/to/PromptCoT-2.0-SFT-7B \
    --n_splits 8 \
    --expected_runs 1 \
    --temperature 0.6 \
    --top_p 0.95 \
    --max_len 81920
done
````

## 📜 引用

如果你觉得 **PromptCoT** 系列有用，请考虑引用我们的工作：

````bibtex
@article{zhao2025promptcot2,
  title     = {PromptCoT 2.0: Scaling Prompt Synthesis for Large Language Model Reasoning},
  author    = {Zhao, Xueliang and Wu, Wei and Guan, Jian and Gong, Zhuocheng and Kong, Lingpeng},
  journal   = {arXiv preprint arXiv:2509.19894},
  year      = {2025},
  url       = {https://arxiv.org/abs/2509.19894}
}

@article{zhao2025scaling,
  title     = {Scaling Reasoning without Attention},
  author    = {Zhao, Xueliang and Wu, Wei and Kong, Lingpeng},
  journal   = {arXiv preprint arXiv:2505.22425},
  year      = {2025},
  url       = {https://arxiv.org/abs/2505.22425}
}

@article{zhao2025promptcot,
  title     = {PromptCoT: Synthesizing Olympiad-Level Problems for Mathematical Reasoning in Large Language Models},
  author    = {Zhao, Xueliang and Wu, Wei and Guan, Jian and Kong, Lingpeng},
  journal   = {arXiv preprint arXiv:2503.02324},
  year      = {2025},
  url       = {https://arxiv.org/abs/2503.02324}
}
````

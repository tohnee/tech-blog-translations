---
title: "inclusionAI/LingSante-MedGuard — LingSante MedGuard"
source: https://github.com/inclusionAI/LingSante-MedGuard/blob/main/README.md
created: 2026-11-17
crawled: 2026-11-21
translated: 2026-11-21
---

<h1 align="center">LingSante MedGuard</h1>
<h3 align="center">面向医疗 AI 的能力增强护栏</h3>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-green.svg" alt="License: Apache 2.0"></a>
</p>

<p align="center">
  <a href="https://arxiv.org/pdf/2611.25509">技术报告（PDF）</a> ·
  <a href="#introduction">简介</a> ·
  <a href="#results">结果</a> ·
  <a href="#method">方法</a> ·
  <a href="#dataset">数据集</a> ·
  <a href="#quick-start">快速开始</a>
</p>

---


<a id="introduction"></a>

## 🎯 简介

**LingSante MedGuard** 对医疗 AI 的回复进行安全性、合规性与伦理风险审查。它将医疗风险检测与多项专项能力相结合，包括规则解读、数值推理校验、证据核实、错误定位、幻觉检测以及多模态医疗实体理解。

**LingSante MedGuardBench** 提供 **14,588 条医疗风险检测记录**，分布于**三个 JSONL 文件**，涵盖医疗安全性、合规性与伦理，并包含 **578 张图像**。

- 🛡️ **医疗安全性：**识别可能伤害患者或延误恰当诊疗的建议，包括药物相互作用与用药禁忌。
- ⚖️ **医疗合规性：**对照适用的职业规范、规则与流程评估回复。
- 🤝 **医疗伦理：**识别与医疗场景中的伦理原则及保障机制相冲突的内容。

- **风险评估：**覆盖安全性、合规性与伦理的 14,588 条记录。
- **数据格式：**三个 JSONL 文件与 578 张图像。

## 💡 核心特性

- **针对患者个体的风险评估。**结合患者信息、临床状况与适用要求来评估医疗建议。
- **能力级评估。**考察医疗风险定位、数值可回答性、直接式与检索式的证据核实，以及文本与多模态幻觉检测。
- **统一的医疗护栏。**通过监督学习与多教师在线策略（on-policy）蒸馏，将一个医疗风险教师模型与六个能力专家整合为一体。
- **覆盖文本与图像。**同时审查书面医疗回复及其与视觉证据的一致性。

<a id="results"></a>

## 🏆 基准测试结果

结果覆盖完整的评测套件；发布的数据集覆盖医疗风险检测。

### 医疗风险检测

原始实验套件（含 MedSafetyBench）上的 F1 分数（%）。**Full** 为文本与多模态任务的成绩；**Text** 为仅文本任务的成绩。

| 模型 | Full F1 | Text F1 |
|---|---:|---:|
| **LingSante MedGuard 27B** | **87.4** | **86.6** |
| Claude-Fable-5 | 84.8 | 84.5 |
| Gemini-3.1-Pro-preview | 82.9 | 80.9 |
| **LingSante MedGuard 9B** | **82.5** | **80.4** |
| **LingSante MedGuard 4B** | **82.3** | **80.5** |
| GPT-5.6-Sol | 80.3 | 79.2 |
| Qwen3.5-397B-A17B | 79.7 | 77.8 |
| Kimi-K3 | 79.3 | 76.3 |
| Qwen3.5 27B | 79.1 | 76.5 |
| Qwen3.5 4B | 76.1 | 74.5 |
| Qwen3.5-35B-A3B | 74.1 | 71.2 |
| Qwen3.5 9B | 74.0 | 71.4 |
| Qwen3.6-35B-A3B | 73.1 | 69.3 |

![原始实验套件上的医疗风险检测结果](assets/benchmark-results.png)

<a id="method"></a>

## 🧩 方法

### 医疗能力专家

每个专家提供医疗风险审查所需的一项特定操作。

| 能力 | 审查操作 |
|---|---|
| 医疗规则理解 | 将患者事实与规则条件、例外情形及角色约束进行匹配。 |
| 医疗数值推理 | 核查公式适用性、输入充分性、单位与计算步骤。 |
| 多模态幻觉检测 | 识别捏造的检查所见、错误的属性与缺乏依据的结论。 |
| Agent 式医疗安全性验证 | 检索信息来源、评估其相关性与支持程度，并在需要时收集补充证据。 |
| 医疗风险定位 | 定位导致风险的句子、片段或推理步骤。 |
| 多模态实体理解 | 提取医疗实体、数值、单位及其关系，并保持彼此对应。 |

### 两阶段多教师蒸馏

一个医疗风险教师模型与六个能力专家模型组成教师库。在**第一阶段**，学生模型通过监督微调从任务相关的教师示范中学习；在**第二阶段**，学生模型自行生成轨迹，由对应的教师提供 token 级反馈用于在线策略更新。这两个阶段将各专家的能力整合进同一个医疗护栏。

![医疗教师模型、离线蒸馏与在线策略蒸馏](assets/training-overview.png)

## ⚖️ 案例研究：医疗规则理解

![医疗规则理解：未经事先检查的开药请求](assets/rule-understanding-case.png)

<a id="dataset"></a>

## 📊 数据集

LingSante MedGuardBench 包含来自 HealthBench、MedHallTune、MedSafetyBench、RxSafeBench 与 MedRepBench 的 14,588 条记录。

每条记录都包含一个 `upstream_dataset` 字段，用于标识其上游数据集；原始的 `source` 字段标识对应的基准子集。

| `source` | `upstream_dataset` |
|---|---|
| `healthbench` | [HealthBench](https://huggingface.co/datasets/openai/healthbench) |
| `medhalltune` | [MedHallTune](https://huggingface.co/datasets/russellyq/MedHallTune) |
| `med_safety_bench` | [MedSafetyBench](https://github.com/AI4LIFE-GROUP/med-safety-bench) |
| `rx_i` | [RxSafeBench](https://github.com/CAS-SIAT-XinHai/RxSafeBench) |
| `rx_c` | [RxSafeBench](https://github.com/CAS-SIAT-XinHai/RxSafeBench) |
| `medrepbench` | [MedRepBench](https://huggingface.co/datasets/MedRepBench/MedRepBench) |

### 风险检测

| 数据集 | 评测重点 | 记录数 |
|---|---|---:|
| [LingSante MedGuard-Safety](data/LingSante%20MedGuard-Safety.jsonl) | 医疗安全性，包括药物相互作用、用药禁忌与报告解读 | 10,248 |
| [LingSante MedGuard-Compliance](data/LingSante%20MedGuard-Compliance.jsonl) | 医疗合规性 | 3,808 |
| [LingSante MedGuard-Ethics](data/LingSante%20MedGuard-Ethics.jsonl) | 医疗伦理 | 532 |
| **合计** | | **14,588** |

### 数据格式

每个 JSONL 文件每行包含一个 JSON 对象。`user_question` 存放输入上下文或用药任务；`model_response` 存放待审查的候选回复，Rx-I/Rx-C 记录中不含该字段；`label` 是参考标注 `safe`（安全）或 `unsafe`（不安全）。样本标识符与原始 `source` 取值均予保留。`images` 中的图像路径相对于仓库根目录，图像文件存放于[图像目录](images)。

<a id="quick-start"></a>

## 🚀 快速开始

### 下载数据集

克隆仓库以下载数据：

```bash
git clone https://code.alipay.com/guoyi.lgy/LingSante-MedGuard.git /absolute/path/to/LingSante-MedGuard
```

### 读取任务记录

```python
import json
from pathlib import Path

repo = Path("/absolute/path/to/LingSante-MedGuard")
dataset = repo / "data" / "LingSante MedGuard-Safety.jsonl"

with dataset.open(encoding="utf-8") as stream:
    records = [json.loads(line) for line in stream if line.strip()]

print(f"Loaded {len(records):,} records")
print(records[0].keys())
```

### 部署本地模型

需要 Python 3.10+ 与兼容的 CUDA GPU。

```bash
pip install -r /absolute/path/to/LingSante-MedGuard/scripts/requirements.txt
bash /absolute/path/to/LingSante-MedGuard/scripts/deploy_model.sh /absolute/path/to/model
```

服务默认地址为 `http://127.0.0.1:8000/v1`，模型名为 `LingSante MedGuard`。可通过设置 `TP` 启用张量并行。部署脚本只负责启动模型服务，不执行评测或打分。

## 📄 许可证

项目代码及我们的原创标注与改编内容基于 Apache-2.0 许可发布。
第三方数据与图像仍受其原始许可证与条款约束。
详情请参见 LICENSE 及上文的数据来源列表。

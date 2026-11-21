---
title: "inclusionAI/LingSante-MedGuard"
source: https://github.com/inclusionAI/LingSante-MedGuard/blob/main/README.md
created: 2026-11-17
crawled: 2026-11-21
---

<h1 align="center">LingSante MedGuard</h1>
<h3 align="center">A Capability-Enhanced Guardrail for Medical AI</h3>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-green.svg" alt="License: Apache 2.0"></a>
</p>

<p align="center">
  <a href="https://arxiv.org/pdf/2611.25509">Technical Report (PDF)</a> ·
  <a href="#introduction">Introduction</a> ·
  <a href="#results">Results</a> ·
  <a href="#method">Method</a> ·
  <a href="#dataset">Dataset</a> ·
  <a href="#quick-start">Quick Start</a>
</p>

---


<a id="introduction"></a>

## 🎯 Introduction

**LingSante MedGuard** reviews medical AI responses for safety, compliance, and ethical risks. It combines medical risk detection with specialized capabilities for interpreting rules, checking numerical reasoning, verifying evidence, locating errors, detecting hallucinations, and understanding multimodal medical entities.

**LingSante MedGuardBench** provides **14,588 medical risk-detection records** across **three JSONL files**, covering medical safety, compliance, and ethics, with **578 images**.

- 🛡️ **Medical safety:** Identify advice that may harm patients or delay appropriate care, including medication interactions and contraindications.
- ⚖️ **Medical compliance:** Assess responses against applicable professional requirements, rules, and procedures.
- 🤝 **Medical ethics:** Identify conflicts with ethical principles and safeguards in medical contexts.

- **Risk evaluation:** 14,588 records across safety, compliance, and ethics.
- **Data formats:** Three JSONL files and 578 images.

## 💡 Key Features

- **Patient-specific risk assessment.** Evaluate medical advice in the context of patient information, clinical conditions, and applicable requirements.
- **Capability-level evaluation.** Assess medical risk localization, numerical answerability, direct and retrieval-enabled evidence verification, and text-based and multimodal hallucination detection.
- **Unified medical guardrail.** Integrate a medical risk teacher and six capability experts through supervised learning and multi-teacher on-policy distillation.
- **Text and image coverage.** Examine both written medical responses and their consistency with visual evidence.

<a id="results"></a>

## 🏆 Benchmark Results

Results cover the full evaluation suite; the released datasets cover medical risk detection.

### Medical Risk Detection

F1 scores (%) on the original experimental suite, including MedSafetyBench. **Full** covers text and multimodal tasks; **Text** covers text-only tasks.

| Model | Full F1 | Text F1 |
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

![Medical risk detection results on the original experimental suite](assets/benchmark-results.png)

<a id="method"></a>

## 🧩 Method

### Medical Capability Experts

Each expert provides a specific operation needed for medical risk review.

| Capability | Review operation |
|---|---|
| Medical rule understanding | Match patient facts to rule conditions, exceptions, and role constraints. |
| Medical numerical reasoning | Check formula applicability, input sufficiency, units, and calculation steps. |
| Multimodal hallucination detection | Identify fabricated findings, incorrect attributes, and unsupported conclusions. |
| Agentic medical safety verification | Retrieve sources, assess their relevance and support, and gather additional evidence when needed. |
| Medical risk localization | Locate the sentence, span, or reasoning step responsible for a risk. |
| Multimodal entity understanding | Extract medical entities, values, units, and relationships while preserving their correspondence. |

### Two-Stage Multi-Teacher Distillation

A medical risk teacher and six capability experts form the teacher bank. In **Stage 1**, the student learns from task-specific teacher demonstrations through supervised fine-tuning. In **Stage 2**, the student generates its own trajectories, and the corresponding teacher supplies token-level feedback for on-policy updates. These stages integrate the experts' capabilities into a single medical guardrail.

![Medical teachers, offline distillation, and on-policy distillation](assets/training-overview.png)

## ⚖️ Case Study: Medical Rule Understanding

![Medical rule understanding: prescription request without prior examination](assets/rule-understanding-case.png)

<a id="dataset"></a>

## 📊 Dataset

LingSante MedGuardBench contains 14,588 records from HealthBench, MedHallTune, MedSafetyBench, RxSafeBench, and MedRepBench.

Each record includes an `upstream_dataset` field identifying its upstream dataset. The original `source` field identifies the benchmark subset.

| `source` | `upstream_dataset` |
|---|---|
| `healthbench` | [HealthBench](https://huggingface.co/datasets/openai/healthbench) |
| `medhalltune` | [MedHallTune](https://huggingface.co/datasets/russellyq/MedHallTune) |
| `med_safety_bench` | [MedSafetyBench](https://github.com/AI4LIFE-GROUP/med-safety-bench) |
| `rx_i` | [RxSafeBench](https://github.com/CAS-SIAT-XinHai/RxSafeBench) |
| `rx_c` | [RxSafeBench](https://github.com/CAS-SIAT-XinHai/RxSafeBench) |
| `medrepbench` | [MedRepBench](https://huggingface.co/datasets/MedRepBench/MedRepBench) |

### Risk Detection

| Dataset | Evaluation focus | Records |
|---|---|---:|
| [LingSante MedGuard-Safety](data/LingSante%20MedGuard-Safety.jsonl) | Medical safety, including drug interactions, medication contraindications, and report interpretation | 10,248 |
| [LingSante MedGuard-Compliance](data/LingSante%20MedGuard-Compliance.jsonl) | Medical compliance | 3,808 |
| [LingSante MedGuard-Ethics](data/LingSante%20MedGuard-Ethics.jsonl) | Medical ethics | 532 |
| **Total** | | **14,588** |

### Data Format

Each JSONL file contains one JSON object per line. `user_question` contains the input context or medication task. `model_response` contains the candidate response under review and is absent from Rx-I/Rx-C records. `label` is the reference `safe` or `unsafe` annotation. Sample identifiers and the original `source` values are preserved. Image paths in `images` are relative to the repository root, with image files stored in [the image directory](images).

<a id="quick-start"></a>

## 🚀 Quick Start

### Download the Dataset

Clone the repository to download the data:

```bash
git clone https://code.alipay.com/guoyi.lgy/LingSante-MedGuard.git /absolute/path/to/LingSante-MedGuard
```

### Read Task Records

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

### Serve a Local Model

Python 3.10+ and a compatible CUDA GPU are required.

```bash
pip install -r /absolute/path/to/LingSante-MedGuard/scripts/requirements.txt
bash /absolute/path/to/LingSante-MedGuard/scripts/deploy_model.sh /absolute/path/to/model
```

The service defaults to `http://127.0.0.1:8000/v1`, with model name `LingSante MedGuard`. Set `TP` for tensor parallelism. The deployment script starts the model service; it does not run evaluation or scoring.

## 📄 License

Project code and our original annotations and adaptations are licensed under Apache-2.0.
Third-party data and images remain subject to their original licenses and terms.
See LICENSE and the source list above for details.


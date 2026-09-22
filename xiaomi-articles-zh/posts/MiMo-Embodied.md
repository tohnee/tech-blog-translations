---
title: "MiMo-Embodied：跨具身形态的视觉-语言模型官方评测套件"
title_en: "XiaomiMiMo/MiMo-Embodied"
source: https://github.com/XiaomiMiMo/MiMo-Embodied/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-Embodied：跨具身形态的视觉-语言模型官方评测套件

> 原文：[XiaomiMiMo/MiMo-Embodied](https://github.com/XiaomiMiMo/MiMo-Embodied/blob/main/README.md) · 小米 MiMo

<div align="center">
  <img src="./assets/xfmlogo.svg" width="600">
</div>

<br/>

<div align="center" style="line-height: 1;">
  |
  <a href="https://huggingface.co/XiaomiMiMo/MiMo-Embodied-7B" target="_blank">🤗 HuggingFace</a>
  &nbsp;|
  <a href="https://arxiv.org/abs/2511.16518" target="_blank">📔 技术报告</a>
  &nbsp;|
  <a href="https://github.com/XiaomiMiMo/MiMo-Embodied" target="_blank">🏠 模型仓库</a>
  &nbsp;|
  <br/>
</div>

## 一、简介

本仓库提供 **MiMo-Embodied 的官方评测套件**，旨在为**具身智能（embodied AI）**与**自动驾驶**任务提供**严谨**且**可复现**的评测。

本仓库构建于优秀的 [lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval) 框架之上，在评测流水线中扩展了 MiMo 专属的模型接入、基准支持以及面向具身与驾驶场景的评测工作流。

**MiMo-Embodied** 是一个强大的跨具身形态（cross-embodied）视觉-语言模型，在**自动驾驶**与**具身智能任务**上均展现出最先进的性能，是首个将这两个关键领域整合在一起的开源 VLM。

> 本仓库**仅用于评测**，**不**包含模型训练代码。

<div align="center">
  <img src="./assets/fig1.svg" width="800">
</div>

---

## 二、关键特性

### 1. `MiVLLM`：为 MiMo 定制的基于 vLLM 的模型封装

我们使用在 `lmms-eval` 原有 `VLLM` 实现之上构建的自定义 `mivllm` 模型类，专为 MiMo 模型定制。与默认实现相比，它：

- 提升**数据加载效率**
- 对**图像与视频预处理**实现更精细的控制
- 支持 MiMo 专属的推理设置，例如：
  - `max_model_len`
  - `gpu_memory_utilization`
  - `max_num_seqs`

### 2. 具身智能评测

本评测套件支持具身智能基准，覆盖以下关键能力：

- **可供性预测（affordance prediction）**
- **任务规划**
- **空间理解**

### 3. 自动驾驶评测

本评测套件同样支持自动驾驶基准，覆盖以下关键能力：

- **环境感知**
- **状态预测**
- **驾驶规划**
- **基于驾驶知识的问答**

### 4. 灵活的评测工作流

该框架支持：

- **单 GPU** 评测
- **多 GPU** 评测
- **多节点**分布式评测
- 跨多个任务的**批量评测**

---

## 三、基准覆盖

本仓库聚焦**具身智能**与**自动驾驶**任务的评测。

### 具身智能基准

| 类别 | 基准 |
|---|---|
| 可供性与规划 | `Where2Place` (`where2place_point`)、`RoboAfford-Eval` (`roboafford`)、`Part-Afford` (`part_affordance`)、`RoboRefIt` (`roborefit`)、`VABench-Point` (`vabench_point_box`) |
| 规划 | `EgoPlan2` (`egoplan`)、`RoboVQA` (`robovqa`)、`Cosmos` (`cosmos_reason1_boxed`) |
| 空间理解 | `CV-Bench` (`cvbench_boxed`)、`ERQA` (`erqa_boxed`)、`EmbSpatial` (`embspatialbench`)、`SAT` (`sat`)、`RoboSpatial` (`robospatial`)、`RefSpatial` (`refspatialbench`)、`CRPE` (`crpe_relation`)、`MetaVQA` (`metavqa_eval`)、`VSI-Bench` (`vsibench_boxed`) |

### 自动驾驶基准

| 基准 |
|---|
| `CODA-LM` (`codalm`) |
| `Drama` (`drama`) |
| `DriveAction` (`drive_action_boxed_detail`) |
| `LingoQA` (`lingoqa_boxed`) |
| `nuScenes-QA` (`nuscenesqa`) |
| `OmniDrive` (`omnidrive`) |
| `NuInstruct` (`nuinstruct`) |
| `DriveLM` (`drivelm`) |
| `MAPLM` (`maplm`) |
| `BDD-X` (`bddx`) |
| `MME-RealWorld` (`mme_realworld`) |
| `IDKB` (`idkb`) |

> 更详细的任务列表可维护在 `mimovl_docs/tasks.md`。

---

## 四、用法

### 安装

```bash
# Step 1: Create conda environment
conda create -n lmms-eval python=3.10 -y
conda activate lmms-eval

# Step 2: Install PyTorch (adjust CUDA version as needed)
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

# Step 3: Install vLLM
pip install vllm==0.7.3

# Step 4: Install the evaluation framework
git clone https://github.com/XiaomiMiMo/MiMo-Embodied.git
cd MiMo-Embodied
pip install -e . && pip uninstall -y opencv-python-headless
pip install -r requirements.txt

# Step 5 (optional but recommended)
pip install xformers==0.0.28.post3
```

### 数据集路径

对于许多基准，图像已经打包在相应的 Hugging Face 数据集中，因此无需额外的本地路径配置。

对于部分图像/视频资产较大的基准，发布的配置 YAML 使用了占位的本地路径，例如：

```yaml
img_root: "/path/to/your/image_or_video_data"
```

在运行这些基准的评测之前，请手动将相应任务 YAML 文件中的 `img_root` 更新为指向你本地的图像/视频目录。

例如：

```yaml
dataset_path: Zray26/bdd_x_testing_caption
task: "bddx"
test_split: test
dataset_kwargs:
  token: True

output_type: generate_until
img_root: "/path/to/your/image_or_video_data"
doc_to_visual: !function utils.doc_to_visual
doc_to_text: !function utils.doc_to_text
doc_to_target: !function utils.doc_to_target
process_results: !function utils.process_test_results_for_submission
```

一个典型的任务文件夹组织如下：

```text
lmms_eval/tasks/<task_name>/
├── <task_name>.yaml
└── utils.py
```

例如：

```text
lmms_eval/tasks/bddx/
├── bddx.yaml
└── utils.py
```

请逐个检查各基准的 YAML 文件，在需要本地图像/视频资产时填写 `img_root`。

### 主评测脚本

主评测启动器为：

```bash
bash mimovl_docs/eval_mimo_vl_args.sh <model_path> <task_name> <output_dir> [disable_thinking]
```

### 单任务评测

```bash
bash mimovl_docs/eval_mimo_vl_args.sh \
    XiaomiMiMo/MiMo-Embodied-7B \
    cvbench_boxed \
    ./eval_results
```

### 无思考（No-Think）评测

对于以无思考模式评测的任务，运行：

```bash
bash mimovl_docs/eval_mimo_vl_args.sh \
    XiaomiMiMo/MiMo-Embodied-7B \
    <task_name> \
    ./eval_results \
    true
```

这对应于：

```bash
disable_thinking_user=true
```

### 多 GPU / 多节点评测

启动器通过环境变量支持分布式评测：

```bash
export NNODES=1
export NODE_RANK=0
export MASTER_ADDR=127.0.0.1
export MASTER_PORT=29500
export NPROC_PER_NODE=8
```

然后运行：

```bash
bash mimovl_docs/eval_mimo_vl_args.sh \
    <model_path> \
    <task_name> \
    <output_dir>
```

### 批量评测

要顺序运行多个任务，请编辑以下文件中的任务列表：

```bash
tools/submit/batch_run.py
```

然后启动：

```bash
python tools/submit/batch_run.py \
    --input <model_path> \
    --eval_results_dir <output_dir>
```

要在批量评测中禁用思考模式：

```bash
python tools/submit/batch_run.py \
    --input <model_path> \
    --eval_results_dir <output_dir> \
    --disable_thinking_user
```

---

## 五、评测协议说明

本评测套件根据基准协议同时支持**思考（thinking）**与**无思考（no-think）**两种评测设定。

对于**具身智能**基准，以下任务在**无思考模式**下评测：

- `RoboVQA` (`robovqa`)

对于**自动驾驶**基准，以下任务在**无思考模式**下评测：

- `CODA-LM` (`codalm`)
- `IDKB` (`idkb`)
- `OmniDrive` (`omnidrive`)
- `NuInstruct` (`nuinstruct`)
- `DriveLM` (`drivelm`)
- `MAPLM` (`maplm`)
- `nuScenes-QA` (`nuscenesqa`)
- `BDD-X` (`bddx`)

对于这些任务，模型使用以下设置评测：

```bash
disable_thinking_user=true
```

---

## 六、默认评测设置

### 模型封装

```bash
--model mivllm
```

### 支持的模型参数

- `max_model_len`
- `gpu_memory_utilization`
- `max_num_seqs`

### 预处理默认值

```text
PATCH_SIZE = 28

IMAGE_MAX_TOKENS = 4096
IMAGE_MAX_PIXELS = 3211264

VIDEO_MAX_TOKENS = 4096
VIDEO_MAX_PIXELS = 3211264

VIDEO_TOTAL_MAX_TOKENS = 16384
VIDEO_TOTAL_MAX_PIXELS = 12845056

VIDEO_FPS = 2
VIDEO_MAX_FRAMES = 256
```

### 生成设置

```text
max_new_tokens = 32768
```

### 推荐硬件

- **1 × NVIDIA A100 (80GB)**，或
- **1 × NVIDIA H20**

---

## 七、评测结果

MiMo-Embodied 在**三大具身智能关键能力（任务规划、可供性预测、空间理解）的 17 项基准**上表现出卓越性能，显著超越现有开源具身 VLM 模型，并可与闭源模型匹敌。

此外，MiMo-Embodied 在**三大关键能力（环境感知、状态预测、驾驶规划）的 12 项自动驾驶基准**上表现优异——显著超越现有开源与闭源 VLM 模型以及专有 VLM 模型。

而且，在**8 项通用视觉理解基准**上的评测证实，MiMo-Embodied 保留甚至强化了其通用能力，说明领域专项训练提升而非削弱了模型的整体能力。

### 具身智能基准

#### 可供性与规划

<div align="center">
  <img src="./assets/table2.png" width="800">
</div>

#### 空间理解

<div align="center">
  <img src="./assets/table3.png" width="800">
</div>

### 自动驾驶基准

#### 单视角图像与多视角视频

<div align="center">
  <img src="./assets/table4.png" width="800">
</div>

#### 多视角图像与单视角视频

<div align="center">
  <img src="./assets/table5.png" width="800">
</div>

### 通用视觉理解基准

<div align="center">
  <img src="./assets/table8.png" width="800">
</div>

> 带 `*` 标记的结果使用我们的评测框架获得。

---

## 八、指标定义

下表说明了评测表格中报告的数字是如何从相应的 `result.json` 文件计算得到的。

除非另有说明：

- 报告的分数以**百分比格式**呈现
- 百分比分数按 `metric × 100` 计算
- 如果一个基准包含多个子任务，报告的分数为相应子任务指标的**算术平均**

| 基准名称（表格） | 任务名称（评测脚本） | `result.json` 中的指标 | 表格分数计算方式 | 模式 | 备注 |
|---|---|---|---|---|---|
| `Where2Place` | `where2place_point` | `accuracy` | `accuracy × 100` | think |  |
| `RoboAfford-Eval` | `roboafford` | `accuracy` | `accuracy × 100` | think |  |
| `Part-Afford` | `part_affordance` | `accuracy` | `accuracy × 100` | think |  |
| `RoboRefIt` | `roborefit` | `accuracy` | `accuracy × 100` | think |  |
| `VABench-Point` | `vabench_point_box` | `accuracy` | `accuracy × 100` | think |  |
| `EgoPlan2` | `egoplan` | `accuracy` | `accuracy × 100` | think |  |
| `RoboVQA` | `robovqa` | `robovqa_score` | `robovqa_score × 100` | no-think |  |
| `Cosmos` | `cosmos_reason1_boxed` | 来自 5 个子任务的 `exact_match` | `mean(5 个子任务的 exact_match) × 100` | think |  |
| `CV-Bench` | `cvbench_boxed` | `accuracy` | `accuracy × 100` | think |  |
| `ERQA` | `erqa_boxed` | `exact_match` | `exact_match × 100` | think |  |
| `EmbSpatial` | `embspatialbench` | `accuracy` | `accuracy × 100` | think |  |
| `SAT` | `sat` | `accuracy` | `accuracy × 100` | think |  |
| `RoboSpatial` | `robospatial` | 来自 3 个子任务的 `accuracy` | `mean(3 个子任务的 accuracy) × 100` | think |  |
| `RefSpatial` | `refspatialbench` | `refspatial-bench-location`、`refspatial-bench-placement` | `mean(refspatial-bench-location, refspatial-bench-placement) × 100` | think |  |
| `CRPE` | `crpe_relation` | `accuracy` | `accuracy × 100` | think |  |
| `MetaVQA` | `metavqa_eval` | `accuracy` | `accuracy × 100` | think |  |
| `VSI-Bench` | `vsibench_boxed` | `vsibench_score` | `vsibench_score × 100` | think |  |
| `CODA-LM` | `codalm` | 3 个子任务的 `jsonl` 结果 | 导出三个子任务的 `jsonl` 文件，然后按 CODA-LM 官方评测流程计算最终分数 | no-think | 官方评测说明：<https://github.com/DLUT-LYZ/CODA-LM/tree/main/evaluation> |
| `Drama` | `drama` | `drama_ACC@0.5` | `drama_ACC@0.5 × 100` | think |  |
| `DriveAction` | `drive_action_boxed_detail` | `drive_action_Overall_acc` | `drive_action_Overall_acc × 100` | think |  |
| `LingoQA` | `lingoqa_boxed` | `lingo_judge_acc` | `lingo_judge_acc × 100` | think |  |
| `nuScenes-QA` | `nuscenesqa` | `exist`、`count`、`object`、`status`、`comparison` | `mean(exist, count, object, status, comparison) × 100` | no-think | 这些类别分数从 `result.json` 的 `accuracy_extract` 中读取。 |
| `OmniDrive` | `omnidrive` | `Bleu_1`、`ROUGE_L`、`CIDEr` | `mean(Bleu_1, ROUGE_L, CIDEr) × 100` | no-think |  |
| `NuInstruct` | `nuinstruct` | `bleu` | `bleu × 100` | no-think |  |
| `DriveLM` | `drivelm` | `jsonl` 结果 | 准备预测结果，然后按 CODA-LM 官方评测流程计算最终分数 | no-think | 官方评测说明：<https://github.com/DLUT-LYZ/CODA-LM/tree/main/evaluation> |
| `MAPLM` | `maplm` | `maplm_FRM`、`maplm_QNS` | `mean(maplm_FRM, maplm_QNS)` | no-think | `maplm_FRM` 与 `maplm_QNS` 已经以 0–100 标度报告。 |
| `BDD-X` | `bddx` | `Bleu_4`、`ROUGE_L`、`CIDEr` | `mean(Bleu_4, ROUGE_L, CIDEr) × 100` | no-think |  |
| `MME-RealWorld` | `mme_realworld` | 来自 2 个子任务的 `mme_realworld_score` | `mean(2 个子任务的 mme_realworld_score) × 100` | think |  |
| `IDKB` | `idkb` | 来自 6 个子任务的指标 | `mean(IDKB_multi_no_image_val, IDKB_multi_with_image_val, IDKB_qa_no_image_val, IDKB_qa_with_image_val, IDKB_single_no_image_val, IDKB_single_with_image_val)` | no-think | 子任务分数计算方式如下：`IDKB_multi_no_image_val = acc × 100`；`IDKB_multi_with_image_val = acc × 100`；`IDKB_qa_no_image_val = mean(rouge_1, rouge_l, semscore)`；`IDKB_qa_with_image_val = mean(rouge_1, rouge_l, semscore)`；`IDKB_single_no_image_val = acc × 100`；`IDKB_single_with_image_val = acc × 100`。 |

完整的指标定义与任务专属细节请参阅 `mimovl_docs/tasks.md`。
---

## 九、案例可视化

### 具身智能

#### 可供性预测

<div align="center">
  <img src="./assets/afford-1.svg" width="800">
</div>

#### 任务规划

<div align="center">
  <img src="./assets/planning-1.svg" width="800">
</div>

#### 空间理解

<div align="center">
  <img src="./assets/spatial-1.svg" width="800">
</div>

### 自动驾驶

#### 环境感知

<div align="center">
  <img src="./assets/ad-perception-1.svg" width="800">
</div>

#### 状态预测

<div align="center">
  <img src="./assets/ad-prediction-1.png" width="800">
</div>

#### 驾驶规划

<div align="center">
  <img src="./assets/ad-planning-1.png" width="800">
</div>

### 真实世界任务

#### 具身导航

<div align="center">
  <img src="./assets/figure_navigation.svg" width="800">
</div>

#### 具身操作

<div align="center">
  <img src="./assets/figure_manipulation.svg" width="800">
</div>

---

## 十、仓库结构

```text
.
├── lmms_eval/                # Core evaluation framework
│   ├── models/               # Model adapters, including mivllm
│   ├── tasks/                # Task definitions and configs
│   ├── api/                  # API interfaces
│   └── ...
├── mimovl_docs/
│   ├── eval_mimo_vl_args.sh  # Main evaluation launcher
│   └── tasks.md              # Task documentation
├── tools/submit/             # Batch evaluation runners
├── patches/                  # Environment patches
├── assets/                   # README assets
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

---

## 十一、引用

```bibtex
@misc{hao2025mimoembodiedxembodiedfoundationmodel,
      title={MiMo-Embodied: X-Embodied Foundation Model Technical Report}, 
      author={Xiaomi Embodied Intelligence Team},
      year={2025},
      eprint={2511.16518},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2511.16518}, 
}

@misc{mimoembodiedeval2025,
      title={The Evaluation Suite of Xiaomi MiMo-Embodied},
      author={Xiaomi Embodied Intelligence Team},
      year={2025},
      url={https://github.com/XiaomiMiMo/MiMo-Embodied}
}
```

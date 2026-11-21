---
title: "inclusionAI/LingSante-Pulse — LingSante-Pulse"
source: https://github.com/inclusionAI/LingSante-Pulse/blob/main/README.md
created: 2026-11-20
crawled: 2026-11-21
translated: 2026-11-21
---

# LingSante-Pulse

[English](README.md) | [简体中文](README_zh.md)

面向生理时间序列的表征学习，提供波形编码与连续血糖监测（CGM）工作流。

LingSante-Pulse 为 ECG（心电）、EEG（脑电）、PPG（光电容积描记）等信号提供可复用的表征。其 CGM 分支支持每日血糖表征、纵向历史建模、公开数据预训练与下游评测。

[技术报告](docs/LingSante-Pulse_Technical_Report.pdf)

## 功能特性

| 分支 | 输入 | 输出 | 工作流 |
| --- | --- | --- | --- |
| 波形 | 信号窗口、实际采样率与通道元数据 | 每通道 256 维 CLS / PatchMean 特征；可选 patch 序列 | 面向下游任务的预训练表征提取 |
| 连续血糖（CGM） | 每日血糖窗口、观测掩码、受试者 ID 与时间戳 | 每日一个 146 维表征，以及贡献历史窗口的数量 | 表征提取、公开数据预训练、分类、固定模型评测与候选选择评测 |

CGM 分支实现了可迁移证据重建（Transferable Evidence Reconstruction，TER），将每日表征、物理尺度、时间动态与因果式跨天历史相结合。训练与评测共用项目的安装、文档与版本管理。

每个分支都提供与其输入相适配的预处理：波形分支处理采样率与物理通道，CGM 分支处理血糖单位、每日网格与受试者历史。各入口点提供默认配置与预训练权重加载。

## 安装

请使用 Python 3.11 或 3.12。在仓库根目录下运行：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install . --no-deps
```

根目录的 `requirements.txt` 同时覆盖两个分支，并保持 CGM 评测所需的依赖版本。GPU 训练需要与所用加速器兼容的 PyTorch 构建。两个分支均支持 CPU 推理与合成示例。

## 预训练权重

| 分支 | 来源 | 内容 |
| --- | --- | --- |
| 波形 | [Hugging Face: inclusionAI/LingSante-Pulse-1.0](https://huggingface.co/inclusionAI/LingSante-Pulse-1.0/) | 官方编码器、配置文件与固定通道资产 |
| CGM | `src/lingsante_pulse/cgm/assets/checkpoints/` | 每日编码器、动态分支、纵向模型与物理尺度参数 |

波形编码器默认从 Hugging Face 下载权重，并使用本地缓存；同时也支持本地模型目录。CGM 部署权重已包含在仓库与安装包中。

## 快速开始

### 波形特征

加载波形编码器并提取特征：

```python
import numpy as np
from lingsante_pulse import LingSantePulse

model = LingSantePulse.from_pretrained()

# Two synthetic single-channel ECG windows, each 10 seconds at 128 Hz.
signals = np.random.default_rng(42).normal(size=(2, 1, 1280)).astype(np.float32)
features = model.encode(
    signals,
    sample_rate=128,
    channels=[{"modality": "ECG", "lead": "II"}],
)

print(features["cls"].shape)         # torch.Size([2, 256])
print(features["patch_mean"].shape)  # torch.Size([2, 256])
```

要加载本地模型目录，将加载那一行替换为：

```python
model = LingSantePulse.from_pretrained("models/pulse", local_files_only=True)
```

该目录必须包含 `model.safetensors`、`config.json`、`channels.npz` 与 `channels.json`。也可以向 `from_pretrained` 显式传入 Hugging Face 仓库 ID。

### CGM 特征

仓库中附带 CGM 部署权重与一个合成示例：

```bash
python -m lingsante_pulse.cgm extract \
  --input examples/cgm_synthetic.npz \
  --output results/cgm_example_embeddings.npz
```

该命令默认使用随包提供的部署权重与 CPU 推理。输出包含 `embedding`、`history_days` 以及相应的窗口、受试者与时间戳元数据。已有输出不会被覆盖；再次运行示例时请选择新的输出路径。

Python 接口：

```python
import numpy as np
from lingsante_pulse.cgm import extract

with np.load("examples/cgm_synthetic.npz", allow_pickle=False) as archive:
    payload = dict(archive)

embedding, history_days = extract(
    payload,
    device="cpu",
)

print(embedding.shape)     # (6, 146)
print(history_days.shape)  # (6,)
```

## 输入与输出

### 波形

- 数组形状可为 `[T]`、`[C, T]` 或 `[B, C, T]`；单通道批次请使用 `[B, 1, T]`。也支持以字典形式提供通道。
- 指定实际的 `sample_rate`。波形使用固定的 128 Hz 预处理；输入各通道必须在时间上对齐。
- 按输入顺序提供 `channels`，包含模态与可选的导联，例如 `{"modality": "ECG", "lead": "II"}`。
- 名称不区分大小写，并忽略首尾空白。ECG 导联 `II`、`ii`、`"2"` 与 `2` 均映射为导联 II。省略或留空导联时使用通用 ECG 身份。
- 可通过 `model.channel_names` 与 `model.channel_descriptions` 查看支持的通道身份。IMU 等不受支持的通道身份会抛出错误。
- 可选的布尔掩码 `observed` 与 `sample_present` 必须与输入形状一致，二者分别标识物理观测与存储填充。

| 输出 | 形状 | 含义 |
| --- | --- | --- |
| `cls` | `[B, C*256]` | 按输入顺序拼接的各通道 CLS 特征 |
| `patch_mean` | `[B, C*256]` | 每个通道在有效 patch 上的均值特征 |
| `channel_names` | C 个名称 | 规范化的通道身份 |
| `patch_tokens` | `[B, P, C*256]` | 传入 `return_tokens=True` 时返回的 patch 特征 |
| `patch_valid` | `[B, P, C]` | 可选的逐通道 patch 有效性掩码 |
| `patch_times` | `[P]` | 可选的相对 patch 起始时间（秒） |

各通道独立编码，其特征随后拼接。波形使用每个通道/窗口内观测样本的均值与标准差。数值型通道使用零阶保持（zero-order-hold）重采样和固定的物理尺度：

| 数值通道 | 输入单位 | 中心值 | 尺度 |
| --- | --- | --- | --- |
| `spo2` | 百分比，例如 97 | 95 | 5 |
| `heart_rate`、`pulse_rate` | 次/分钟 | 70 | 30 |
| `rr_primus`、`rr_solar` | 呼吸次/分钟 | 20 | 20 |
| `bis_emg_power` | dB | 0 | 100 |

数值按 `(value - center) / scale` 变换，并裁剪到 `[-10, 10]`。NaN/Inf 值视为未观测；0 是有效样本值。不含任何观测样本的窗口会抛出错误。

### CGM

CGM 输入由 5 分钟网格上互不重叠的 24 小时窗口组成，每个窗口 288 个点：

| 字段 | 形状 | 含义 |
| --- | --- | --- |
| `glucose_mg_dl` | `[N, 288]` | 血糖值，单位 mg/dL |
| `observed_mask` | `[N, 288]` | 原始物理观测的布尔掩码；插值点仍视为未观测 |
| `window_id` | `[N]` | 唯一的窗口标识符 |
| `subject_id` | `[N]` | 匿名受试者标识符，用于历史分组，不作为数值型模型特征 |
| `start_time` | `[N]` | 实际窗口起始时刻，保留当地时间（一天内时刻）约定 |
| `episode_index` | 可选 `[N]` | 记录片段标识符，防止历史上下文跨越互不相关的片段 |

在同一调用中应包含某位受试者/某段记录的全部可用历史窗口。模型会依据时间戳构建最多七天的因果上下文；在没有可用历史时，返回当天的表征。若数据集构建脚本提供了 `native_cadence_min` 等字段，请予以保留。

构建窗口前请先将 mmol/L 换算为 mg/dL。可选的 `label_*` 字段可用于单独评测，编码器不会使用它们。完整的输入与预处理规则参见 [CGM 数据文档](docs/cgm/DATA.md)。

## CGM 下游分类

分别提取训练集与新受试者的特征，并保留每位受试者可用的历史。使用训练受试者及其标签拟合分类器：

```bash
python -m lingsante_pulse.cgm downstream fit \
  --input results/train_embeddings.npz \
  --label label_diabetes \
  --model results/diabetes_classifier.joblib

python -m lingsante_pulse.cgm downstream predict \
  --input results/new_participants_embeddings.npz \
  --model results/diabetes_classifier.joblib \
  --output results/diabetes_predictions.npz
```

这些命令需要你自己的特征文件与训练标签。示例使用 `StandardScaler + LogisticRegression`，且二者都只在训练受试者上拟合。请加载本地创建或来自可信来源的分类器文件。预训练编码器产出的是表征，而非预训练好的疾病预测。

## CGM 公开数据预训练

仓库包含数据准备与多阶段训练流程。先获取 [DATA.md](docs/cgm/DATA.md) 中描述的公开数据集，然后构建预训练语料：

```bash
python -m lingsante_pulse.cgm prepare-data \
  --shanghai-root data/raw/shanghai \
  --stanford-root data/raw/stanford \
  --big-ideas-root data/raw/big_ideas_1.1.2 \
  --colas-root data/raw/colas2019/S1 \
  --output-dir data/processed/public_pretraining \
  --shanghai-policy subject_disjoint --seed 43

python -m lingsante_pulse.cgm train \
  --corpus data/processed/public_pretraining/glucofm_public_pretrain_subject_disjoint_v1.npz \
  --output results/cgm_public_pretraining \
  --device cuda:0
```

请将示例中的 `data/raw/` 路径替换为你自己的数据集位置。训练依次运行每日编码器、动态分支、跨天上下文阶段与最终的记忆阶段，然后在 `results/cgm_public_pretraining/checkpoints/` 下导出可用于推理的资产。公开配方在每个优化阶段使用随机种子 43 与 6,960 步。需要 CUDA 兼容的加速器。

语料库必须排除表型标签，且训练/验证受试者必须互不重叠。随附的 CGM 权重在训练时还使用了私有的无标签 CGM 数据。这些命令复现的是公开数据的训练流程，而非用私有数据训练出的原始权重。模型与训练模块参见 [CGM 代码导览](docs/cgm/CODE_MAP.md)。

## CGM 评测

公开评测覆盖 CGMacros、Shanghai、Stanford 与 Hall 数据集上的 14 个任务。请按照 [DATA.md](docs/cgm/DATA.md) 准备各队列数据，路径形如 `data/processed/glucofm_public/COHORT/COHORT_glucofm_windows_v1.npz`，其中 `COHORT` 为 `cgmacros`、`shanghai_t2dm`、`stanford` 或 `hall`。

### 固定模型评测

评测随包提供的部署权重：

```bash
python -m lingsante_pulse.cgm evaluate \
  --data-root data/processed/glucofm_public \
  --output results/cgm_fixed_model \
  --device cpu
```

要评测你自己训练的模型，请添加 `--checkpoint-dir` 参数并指向其导出的 `checkpoints/` 目录。使用 `--embeddings-root` 可评测已有的各队列特征文件。

### 可选：论文主表复现

论文主表在 24 个候选模型之间进行嵌套选择。该流程需要单独准备的候选权重及其 `manifest.json`；默认安装包仅包含一个部署模型。

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python -m lingsante_pulse.cgm evaluate-nested \
  --data-root data/processed/glucofm_public \
  --candidates-dir reproduction/candidates \
  --output results/cgm_nested_evaluation \
  --device cpu --workers 8
```

将 `--candidates-dir` 指向准备好的候选目录。该协议使用 10 次重复、5 个外层折与 3 个内层折：先在每个外层训练人群内部选出共享表征，再进行外层测试评测。同一名生物学受试者的全部记录始终留在同一折内。固定部署模型的结果与主表的候选选择结果分别报告。

## 仓库结构

```text
.
├── README.md
├── README_zh.md
├── LICENSE
├── LEGAL.md
├── pyproject.toml
├── requirements.txt
├── src/lingsante_pulse/
│   ├── __init__.py
│   ├── waveform/
│   │   ├── api.py
│   │   ├── model.py
│   │   ├── preprocessing.py
│   │   ├── channels.py
│   │   └── hub.py
│   └── cgm/
│       ├── __main__.py
│       ├── models/
│       ├── data/
│       ├── inference/
│       ├── training/
│       ├── evaluation/
│       ├── downstream.py
│       ├── checkpoints.py
│       ├── baselines/
│       ├── diagnostics/
│       └── assets/
│           ├── checkpoints/
│           ├── configs/
│           └── benchmarks/
├── examples/
├── scripts/cgm/
├── tests/
│   ├── waveform/
│   └── cgm/
└── docs/cgm/
```

## 许可证与数据来源

项目自有代码与随附的模型权重采用 [MIT 许可证](LICENSE)。仓库保留了 [LEGAL.md](LEGAL.md) 与 [CGM 第三方声明](docs/cgm/NOTICE.md)。第三方数据集与模型资产须在其各自的许可证与访问条件下获取，本仓库不对其进行再分发。私有原始数据、表型标签与个人身份标识信息均不包含在本发布中。

LingSante-Pulse 面向表征学习与算法研究。针对具体任务的预测性能，必须在目标数据上按适当的评测协议进行评估。

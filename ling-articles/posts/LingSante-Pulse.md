---
title: "inclusionAI/LingSante-Pulse"
source: https://github.com/inclusionAI/LingSante-Pulse/blob/main/README.md
created: 2026-11-20
crawled: 2026-11-21
---

# LingSante-Pulse

[English](README.md) | [简体中文](README_zh.md)

Representation learning for physiological time series, with waveform encoding and continuous glucose monitoring (CGM) workflows.

LingSante-Pulse provides reusable representations for signals such as ECG, EEG, and PPG. Its CGM branch supports daily glucose representations, longitudinal history modeling, public-data pretraining, and downstream evaluation.

[Technical report](docs/LingSante-Pulse_Technical_Report.pdf)

## Features

| Branch | Input | Output | Workflows |
| --- | --- | --- | --- |
| Waveforms | Signal windows, actual sampling rates, and channel metadata | 256-dimensional CLS / PatchMean features per channel; optional patch sequences | Pretrained representation extraction for downstream tasks |
| Continuous glucose (CGM) | Daily glucose windows, observation masks, subject IDs, and timestamps | A 146-dimensional representation per day and the number of contributing history windows | Representation extraction, public-data pretraining, classification, fixed-model evaluation, and candidate-selection evaluation |

The CGM branch implements Transferable Evidence Reconstruction (TER), combining daily representations, physical scale, temporal dynamics, and causal cross-day history. Training and evaluation share the project's installation, documentation, and versioning.

Each branch provides preprocessing appropriate to its inputs: sampling rates and physical channels for waveforms, and glucose units, daily grids, and subject histories for CGM. The entry points provide defaults and pretrained-weight loading.

## Installation

Use Python 3.11 or 3.12. Run from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install . --no-deps
```

The root `requirements.txt` covers both branches and preserves the CGM evaluation dependency versions. GPU training requires a PyTorch build compatible with your accelerator. Both branches support CPU inference and synthetic examples.

## Pretrained weights

| Branch | Source | Contents |
| --- | --- | --- |
| Waveforms | [Hugging Face: inclusionAI/LingSante-Pulse-1.0](https://huggingface.co/inclusionAI/LingSante-Pulse-1.0/) | Official encoder, configuration, and fixed channel assets |
| CGM | `src/lingsante_pulse/cgm/assets/checkpoints/` | Daily encoder, dynamics branch, longitudinal model, and physical-scale parameters |

The waveform encoder downloads weights from Hugging Face and uses the local cache by default. Local model directories are also supported. CGM deployment weights are included in the repository and installation package.

## Quick start

### Waveform features

Load the waveform encoder and extract features:

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

To load a local model directory, replace the loading line with:

```python
model = LingSantePulse.from_pretrained("models/pulse", local_files_only=True)
```

The directory must contain `model.safetensors`, `config.json`, `channels.npz`, and `channels.json`. An explicit Hugging Face repository ID can also be passed to `from_pretrained`.

### CGM features

CGM deployment weights and a synthetic example are included in the repository:

```bash
python -m lingsante_pulse.cgm extract \
  --input examples/cgm_synthetic.npz \
  --output results/cgm_example_embeddings.npz
```

This command uses the packaged deployment weights and CPU inference by default. Its output contains `embedding`, `history_days`, and the corresponding window, subject, and timestamp metadata. Existing outputs are not overwritten; choose a new output path when running the example again.

Python interface:

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

## Inputs and outputs

### Waveforms

- Arrays may have shape `[T]`, `[C, T]`, or `[B, C, T]`. Use `[B, 1, T]` for a single-channel batch. Channel dictionaries are also supported.
- Specify the actual `sample_rate`. Waveforms use fixed 128-Hz preprocessing; input channels must be aligned in time.
- Provide `channels` in input order, with a modality and optional lead, for example `{"modality": "ECG", "lead": "II"}`.
- Names ignore case and leading/trailing whitespace. ECG leads `II`, `ii`, `"2"`, and `2` map to lead II. An omitted or empty lead uses the generic ECG identity.
- Inspect supported identities with `model.channel_names` and `model.channel_descriptions`. Unsupported identities such as IMU raise an error.
- Optional boolean masks `observed` and `sample_present` must match the input shape. They identify physical observations and storage padding, respectively.

| Output | Shape | Meaning |
| --- | --- | --- |
| `cls` | `[B, C*256]` | Per-channel CLS features concatenated in input order |
| `patch_mean` | `[B, C*256]` | Mean features over valid patches for each channel |
| `channel_names` | C names | Canonical channel identities |
| `patch_tokens` | `[B, P, C*256]` | Patch features returned with `return_tokens=True` |
| `patch_valid` | `[B, P, C]` | Optional per-channel patch-validity mask |
| `patch_times` | `[P]` | Optional relative patch start times in seconds |

Channels are encoded independently and their features are concatenated. Waveforms use the mean and standard deviation of observed samples within each channel/window. Numeric channels use zero-order-hold resampling and fixed physical scales:

| Numeric channel | Input unit | Center | Scale |
| --- | --- | --- | --- |
| `spo2` | Percent, e.g. 97 | 95 | 5 |
| `heart_rate`, `pulse_rate` | Beats/min | 70 | 30 |
| `rr_primus`, `rr_solar` | Breaths/min | 20 | 20 |
| `bis_emg_power` | dB | 0 | 100 |

Numeric values are transformed as `(value - center) / scale` and clipped to `[-10, 10]`. NaN/Inf values are unobserved; zero is a valid sample. A window with no observed samples raises an error.

### CGM

CGM input consists of non-overlapping 24-hour windows on a 5-minute grid, with 288 points per window:

| Field | Shape | Meaning |
| --- | --- | --- |
| `glucose_mg_dl` | `[N, 288]` | Glucose in mg/dL |
| `observed_mask` | `[N, 288]` | Boolean mask of original physical observations; interpolated points remain unobserved |
| `window_id` | `[N]` | Unique window identifier |
| `subject_id` | `[N]` | Anonymous subject identifier for history grouping, not a numerical model feature |
| `start_time` | `[N]` | Actual window start, preserving the local time-of-day convention |
| `episode_index` | Optional `[N]` | Recording-episode identifier preventing history from crossing unrelated episodes |

Include all available history windows for a subject/episode in the same call. The model constructs up to seven days of causal context from timestamps. Without supported history, it returns the current day's representation. Preserve fields such as `native_cadence_min` when provided by dataset builders.

Convert mmol/L to mg/dL before constructing windows. Optional `label_*` fields may be included for separate evaluation; the encoder does not consume them. See [CGM data documentation](docs/cgm/DATA.md) for the full input and preprocessing rules.

## CGM downstream classification

Extract training and new-subject features separately, retaining each subject's available history. Fit the classifier using training subjects and their labels:

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

These commands require your feature files and training labels. The example uses `StandardScaler + LogisticRegression`, with both fitted on training subjects only. Load classifier files created locally or obtained from trusted sources. Pretrained encoders produce representations rather than pretrained disease predictions.

## CGM public-data pretraining

The repository includes data preparation and multistage training. Obtain the public datasets described in [DATA.md](docs/cgm/DATA.md), then build the pretraining corpus:

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

Replace the example `data/raw/` paths with your dataset locations. Training runs the daily encoder, dynamics branch, cross-day context stage, and final memory stage, then exports inference-ready assets under `results/cgm_public_pretraining/checkpoints/`. The public recipe uses seed 43 and 6,960 steps for each optimization stage. A CUDA-compatible accelerator is required.

The corpus must exclude phenotype labels, and training/validation subjects must be disjoint. The supplied CGM weights also used private unlabeled CGM. These commands reproduce the public-data training workflow, not the original weights trained with private data. See [the CGM code map](docs/cgm/CODE_MAP.md) for model and training modules.

## CGM evaluation

Public evaluation covers 14 tasks across CGMacros, Shanghai, Stanford, and Hall. Prepare the cohorts using [DATA.md](docs/cgm/DATA.md) as `data/processed/glucofm_public/COHORT/COHORT_glucofm_windows_v1.npz`, where `COHORT` is `cgmacros`, `shanghai_t2dm`, `stanford`, or `hall`.

### Fixed-model evaluation

Evaluate the packaged deployment weights:

```bash
python -m lingsante_pulse.cgm evaluate \
  --data-root data/processed/glucofm_public \
  --output results/cgm_fixed_model \
  --device cpu
```

To evaluate your own trained model, add `--checkpoint-dir` pointing to its exported `checkpoints/` directory. Use `--embeddings-root` to evaluate existing per-cohort feature files.

### Optional paper main-table reproduction

The paper's main table uses nested selection among 24 candidates. This workflow requires separate candidate weights and their `manifest.json`; the default package includes one deployment model.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python -m lingsante_pulse.cgm evaluate-nested \
  --data-root data/processed/glucofm_public \
  --candidates-dir reproduction/candidates \
  --output results/cgm_nested_evaluation \
  --device cpu --workers 8
```

Point `--candidates-dir` to the prepared candidate directory. The protocol uses 10 repeats, 5 outer folds, and 3 inner folds. A shared representation is selected inside each outer-training population before outer-test evaluation. All records from one biological participant remain in the same fold. Fixed deployment-model results and main-table candidate-selection results are reported separately.

## Repository structure

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

## License and data sources

Project-owned code and included model weights use the [MIT license](LICENSE). The repository retains [LEGAL.md](LEGAL.md) and [CGM third-party notices](docs/cgm/NOTICE.md). Third-party datasets and model assets must be obtained under their own licenses and access conditions; they are not redistributed here. Private raw data, phenotype labels, and personal identifiers are excluded from the release.

LingSante-Pulse supports representation-learning and algorithm research. Task-specific predictive performance must be evaluated on the target data under an appropriate evaluation protocol.


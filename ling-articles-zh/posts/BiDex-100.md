---
title: "inclusionAI/BiDex-100"
title_en: "inclusionAI/BiDex-100"
source: https://github.com/inclusionAI/BiDex-100/blob/master/README.md
crawled: 2026-10-15
translated: 2026-10-15
---

<p align="center">
  <img src="https://raw.githubusercontent.com/BiDex-100/BiDex-100/gh-pages/static/images/title.png" alt="BiDex-100" width="760">
</p>

<p align="center">
  <strong>一个覆盖 100+ 仿真任务的双手灵巧操作综合基准</strong>
</p>

<p align="center">
  <a href="https://bidex-100.github.io/BiDex-100/">网站</a> ·
  <a href="https://huggingface.co/datasets/inclusionAI/BiDex-100/tree/main/datasets">数据集</a> ·
  <a href="https://huggingface.co/datasets/inclusionAI/BiDex-100/tree/main/assets">3D 资产</a>
</p>

<p align="center">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="MuJoCo" src="https://img.shields.io/badge/Engine-MuJoCo-475569?style=flat-square">
  <img alt="LeRobot v2.1 and v3.0" src="https://img.shields.io/badge/Data-LeRobot_v2.1_%7C_v3.0-ffcc00?style=flat-square">
  <img alt="Code: MIT" src="https://img.shields.io/badge/Code-MIT-blue?style=flat-square">
  <img alt="Data and original assets: CC BY-NC 4.0" src="https://img.shields.io/badge/Data%20%26%20Original%20Assets-CC_BY--NC_4.0-8A2BE2?style=flat-square">
</p>

## 概览

<p align="center">
  <img src="https://raw.githubusercontent.com/BiDex-100/BiDex-100/gh-pages/static/images/figures/overview.png" alt="BiDex-100 benchmark overview" width="92%">
</p>

BiDex-100 用于评估视觉-语言-动作（VLA）策略在协同的、双手的灵巧操作上的表现。它将声明式任务定义、可复现的 MuJoCo 环境、匹配的域内与域外评估、3D 资产以及 8,080 条经成功验证的演示数据（demonstrations）整合为一体。

- **横跨五大能力维度的 106 个任务：**记忆（Memory）、长时程（Long-Horizon）、指令遵循（Instruction-Following）、少量演示（Limited-Demonstrations）与泛化（Generalization）。
- **两种双手本体（embodiment）：**双 Franka FR3 v2 机械臂与 Astribot S1，均配备灵巧手。
- **8,080 条演示与 6.25M 帧数据：**六路同步 RGB-D 视频流，帧率 25 FPS，以任务级 LeRobot v2.1 与 v3.0 数据集形式发布。
- **58 维统一动作空间：**14 维机械臂/末端执行器维度，外加 44 维灵巧手关节维度。
- **匹配的 ID/OOD 协议：**确定性随机种子、场景与物体变化、基于谓词的进度评分，以及严格的满分 100 成功判据。

## 安装

```bash
git clone https://github.com/inclusionAI/BiDex-100.git
cd BiDex-100

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e ".[eval]"
```

Hugging Face 数据集仓库包含三个可独立下载的组成部分：

```text
assets/                    compressed simulation asset packs
datasets/lerobotv21/       LeRobot v2.1 datasets
datasets/lerobotv30/       LeRobot v3.0 datasets
```

下载全部内容并准备仿真资产：

```bash
python -m pip install -U huggingface_hub
hf auth login  # omit for public, unauthenticated downloads

bash scripts/download_release.sh all downloads/BiDex-100
bash scripts/setup_assets_links.sh downloads/BiDex-100
```

也可以将各组成部分分别下载到同一目标目录：

```bash
bash scripts/download_release.sh assets downloads/BiDex-100
bash scripts/download_release.sh lerobotv21 downloads/BiDex-100
bash scripts/download_release.sh lerobotv30 downloads/BiDex-100
```

`scripts/download_assets.sh` 与 `scripts/download_datasets.sh` 仍作为便捷封装保留。运行 `download_datasets.sh lerobotv21`、`download_datasets.sh lerobotv30` 或 `download_datasets.sh all`，可获取其中一种或两种数据集格式。下载目标目录会保持上文所示的仓库布局。

资产安装脚本接受 `downloads/BiDex-100` 或 `downloads/BiDex-100/assets` 两种路径。它会就地解压每个压缩包、创建仓库链接，并重建装配类任务所用的相对路径别名。当存在 `assets/SHA256SUMS` 时会校验压缩包校验和；否则脚本会记录每个本地压缩包的摘要，使未变更的解压结果可以被安全复用。该脚本是幂等的，中断后的安装可以安全重跑。另一种方式是设置 `BIDEX_ASSETS=/path/to/BiDex-100/assets`。在非交互环境中，请导出 `HF_TOKEN` 代替 `hf auth login`。

若需无头（headless）GPU 渲染，请在启动 Python 之前选择 EGL：

```bash
export MUJOCO_GL=egl
export PYOPENGL_PLATFORM=egl
```

## 任务

`bidex/tasks_data/suites/<suite>/<task>.yaml` 下的任务 YAML 文件定义了场景、机器人、物体、初始化分布、指令、成功谓词、子任务以及对应的 OOD 变体。五个套件分别包含 10、10、20、26 和 40 个任务（共 106 个）。

下面这个极简示例是完整的、可直接运行的。它禁用了相机，使首次仿真检查无需图形上下文；重置一个任务，保持重置后的机器人姿态，用 `env.step` 推进物理仿真，并关闭所有 MuJoCo 资源：

```python
from bidex import BiDexEnv, load_task

task = load_task("Memory", "uncover_red_cube")
env = BiDexEnv(task, control_mode="joint", cameras=[])

try:
    obs = env.reset(seed=0)
    action = {
        "arm_joint_position": obs["arm_joint_position"].copy(),
        "dex_joint_position": obs["dex_joint_position"].copy(),
    }

    for _ in range(64):
        obs, reward, terminated, info = env.step(action)
        if terminated:
            break

    print({"reward": reward, "terminated": terminated, "score": info.get("score")})
finally:
    env.close()
```

使用 `list_suites()` 和 `list_tasks(<suite>)` 可以发现 106 个基础任务。仅在查看成对的 OOD 变体定义时，才向 `list_tasks` 传入 `include_ood=True`。当需要 RGB 观测时，传入 `cameras=["head", "left_wrist", "right_wrist"]`。

## 训练

BiDex-100 与具体模型无关：本仓库提供基准与数据契约，而每个 VLA 实现各自拥有自己的训练器。受支持的 58 维表示为：

| 模式 | 机械臂分量 | 灵巧手分量 |
| --- | --- | --- |
| `joint` | `actions.arm_joint_position` (14-D) | `actions.dex_joint_position` (44-D) |
| `robot_ee` | `actions.abs_end_effector` (14-D) | `actions.dex_joint_position` (44-D) |
| `camera_ee` | `actions.abs_end_effector_camera` (14-D) | `actions.dex_joint_position` (44-D) |

在新增训练器集成时，请以 `bidex.tasks.benchmark.BENCHMARKS` 与 `MODES` 作为套件与模态的规范注册表。

### 已报告的训练设置

目前报告的模型结果采用**联合训练（co-training）**：来自多个基准任务的演示被合并为一个训练语料，用于训练一个共享的策略检查点。评估则在所有适用任务上运行同一个检查点；所报告的数字并非对每个任务单独训练策略后的集成（ensemble）。

## 评估

BiDex-100 为不同的 VLA 策略提供统一的评估契约。模型适配器接收相同的三路相机观测、本体感知状态与语言指令；基准侧负责任务发现、带种子的重置、ID/OOD 随机化、rollout 执行、评分、视频与结果模式（schema）。这使模型比较独立于模型专属的启动代码。

### ID/OOD 协议摘要

标准协议对两个 ID 种子（`0,1`）与两个 OOD 种子（`2,3`）各评估 25 个回合（episode）。两个域均使用确定性的逐回合重置种子，以及相同的任务指令、成功谓词、rollout 时域和评分规则。

| 项目 | 域内（ID） | 域外（OOD） |
| --- | --- | --- |
| 任务定义 | 基础任务 YAML。 | 该任务随仓库提交的 `__ood.yaml` 变体（覆盖全部 106 个任务）。 |
| 机器人初始状态 | 从任务的评估 H5 中确定性地采样一条已记录的工作姿态，且仅恢复机器人关节；物体保持基础 YAML 中的全新摆放。 | 使用任务的默认机器人重置姿态；不从 H5 演示中采样姿态。 |
| 物体与布局 | 基础 YAML 中的区域与物体身份。 | 任务专属的、预先固化的区域/布局变化；部分任务还会使用左右臂镜像、防碰撞干扰物，或逐回合的铰接物体尺度变化。 |
| 场景外观 | 原始地板、墙壁、桌面与灯光。 | 确定性的地板/墙壁/桌面纹理与随机化灯光。 |
| 相机 | 标称的头部与腕部外参。 | 由经过碰撞审计的有限位姿库独立控制头部与腕部的变化。 |

OOD 外观随机化被有意限定在边界内，但视觉上足够强烈：

- 灯光在从 `dark` 到 `high_bright` 的五档曝光配置间循环，主光/补光/环境光强度分别为 `0.11/0.035/0.014`、`0.18/0.060/0.022`、`0.29/0.100/0.040`、`0.40/0.145/0.058` 与 `0.48/0.180/0.072`。主光投射阴影、覆盖完整方位角圆周，仰角为 25/38/52/66/76 度，带有中性/暖/冷色调，距离为 3.0/3.5/4.0/4.4 米。不投射阴影的补光提供光照下限，避免观测过暗而不可用。
- 头部相机偏移限制在 1.8 cm 和 6 度以内。腕部相机偏移限制在 1.35 cm 和 6 度以内；对 Franka 与 Astribot 而言，安装间隙轴都只允许向外运动，确保机器人连接器不会移动到镜头前方。在每任务标准的 50 个 OOD 回合中，相机出现次数精确为：标称 10 次、仅头部 10 次、仅腕部 10 次、头部加腕部 20 次。
- 物体/布局变化来自每个任务随仓库提交的 OOD YAML。干扰物的身份对每个任务和 OOD 种子是固定的，而摆放位置则逐回合重采样；任务几何与可达性约束保证物体始终位于可用、防碰撞的桌面区域内。

随机化使用按组件划分作用域的 SHA-256 密钥、NumPy PCG64 随机流，以及经哈希校验的纹理/相机清单。因此，固定的任务、种子和回合在不同机器上会产出相同的计划，而不依赖 GPU 或渲染器输出。

内含七个参考集成：π0.5、Galaxea G0.5、GR00T N1.7、LingBot-VLA、XR-1、InternVLA-A1.5 与 DM0.5。其他模型只需实现 `bidex/eval/run_leaderboard_eval.py` 所用的「观测到动作」适配器，即可使用同一驱动程序。

启动器没有任何机器专属默认值。每个集成都需要提供：

- `MODEL_PY`：模型环境使用的 Python 解释器。
- `MODEL_REPO`：模型源码目录。
- `MODEL_CKPT`：检查点路径。
- `BIDEX_LEADERBOARD_ROOT`：输出目录。

LingBot-VLA、XR-1 与 InternVLA-A1.5 还额外需要 `MODEL_VLM_PATH`，因为这些适配器会加载一个独立的本地 VLM 骨干。`OPENPI_DATA_HOME` 是可选的原生 OpenPI 缓存覆盖项；未设置时，OpenPI 使用其默认缓存。

例如，在本仓库中不内嵌路径地配置 π0.5：

```bash
export MODEL_PY=/path/to/openpi/.venv/bin/python
export MODEL_REPO=/path/to/openpi
export MODEL_CKPT=/path/to/pi05-checkpoint
export BIDEX_LEADERBOARD_ROOT=/path/to/evaluation-output

# Optional for an offline, pre-populated OpenPI cache.
export OPENPI_DATA_HOME=/path/to/openpi-cache
```

在运行完整基准之前，先跑一个确定性的端到端冒烟任务：

```bash
MID_OVERRIDE=pi05_smoke \
BENCHES=Memory \
BIDEX_TASKS=Memory/pour_ice_between_two_cups \
SEEDS=0 ID_SEEDS=0 OOD_SEEDS=2 EPS=1 \
MODEL_GPUS=0 RENDER_GPUS=1 \
  bash scripts/evaluation/run_vec_models_eval.sh pi05 smoke

MID_OVERRIDE=pi05_alljoint \
MODEL_GPUS=0,1,2,3,4,5,6,7 \
RENDER_GPUS=0,1,2,3,4,5,6,7 \
  bash scripts/evaluation/run_vec_models_eval.sh pi05
```

### GPU 布局

`MODEL_GPUS` 分配策略服务器，`RENDER_GPUS` 分配向量化 MuJoCo 工作进程。基准协议与输出模式不随布局改变。每种布局都使用相同的服务端-客户端传输；同时出现在两个列表中的 GPU 会分别承载策略服务器与渲染工作进程。

| 布局 | `MODEL_GPUS` | `RENDER_GPUS` | 说明 |
| --- | --- | --- | --- |
| 单卡 | `0` | `0` | 策略与仿真共享一张卡。 |
| 专属拆分 | `0` | `1,2,3,4,5,6,7` | 一张策略卡加七张仅用于渲染的卡。 |
| 多服务器拆分 | `0,1` | `2,3,4,5,6,7` | 两台策略服务器分担来自六个工作进程的请求。 |
| 部分重叠 | `0,1` | `1,2,3,4,5,6,7` | GPU 1 同时承担两种角色。 |
| 完全重叠 | `0,1,2,3,4,5,6,7` | `0,1,2,3,4,5,6,7` | 每张卡都承载一个服务器与一个工作进程。 |

每次冒烟或完整运行都应使用不同的 `MID_OVERRIDE`。`BENCHES`、`BIDEX_TASKS`、`SEEDS`、`ID_SEEDS`、`OOD_SEEDS`、`EPS`、`ENVS_PER_GPU`、`MAX_RECORD_ENVS` 与 `BIDEX_MAX_ENVS_PER_GPU` 可细化协议而不改变其评分契约。`GPUS` 仍作为兼容别名保留；建议显式指定模型/渲染 GPU 列表。

默认情况下，工作进程会完整执行每个模型返回的动作块（action chunk）。仅当你想为显式消融实验限制该原生时域时，才将 `BIDEX_VEC_CHUNK_REUSE` 设为正整数；留空或置零则保持模型的最大块大小。

### 查看结果

`MID_OVERRIDE` 标识一个被评估的检查点/配置。结果、视频与实时日志都隔离在该标识之下：

```text
results/<MID_OVERRIDE>/<benchmark>_<robot>_<mode>_<domain>.json
mp4s/<MID_OVERRIDE>/<setting>/<task>/s<seed>_ep<episode>.mp4
runs/<MID_OVERRIDE>/<run_name>/{in_domain,out_of_domain}/...
```

在所有本地网络接口上启动排行榜服务：

```bash
python bidex/eval/baseline_leaderboard_server.py \
  --lb-root "$BIDEX_LEADERBOARD_ROOT" \
  --host 0.0.0.0 --port 12006 --base-url /baselines
```

从局域网内打开 `http://<host-ip>:12006/baselines/`。该页面会从 `results/<MID_OVERRIDE>/` 中发现模型行，实时刷新分数，并提供 rollout 视频服务。

## 许可证

| 组成部分 | 许可证 |
| --- | --- |
| 代码库 | [MIT License](LICENSE) |
| BiDex-100 数据集 | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| BiDex-100 原始 3D 资产 | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| 第三方资产 | 沿用其各自的上游原始许可证，保留于每个资产子目录内 |

## 致谢

BiDex-100 构建在
[MuJoCo](https://mujoco.readthedocs.io/)、
[LeRobot](https://github.com/huggingface/lerobot)、
[LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)、
[RoboCasa](https://github.com/robocasa/robocasa)、
[robosuite](https://github.com/ARISE-Initiative/robosuite)、
[dexjoco](https://github.com/brave-eai/dexjoco) 与
[Articraft](https://github.com/mattzh72/articraft) 之上。

## 引用

```bibtex
@misc{bidex100,
  title        = {BiDex-100: A Comprehensive Benchmark for Bimanual Dexterous
                  Manipulation Across 100+ Simulation Tasks},
  year         = {2026},
}
```

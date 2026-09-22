---
title: "AgentBench：评估 LLM 作为智能体的能力"
source: https://github.com/THUDM/AgentBench
crawled: 2026-09-22
title_en: "AgentBench"
translated: 2026-09-22
---

# AgentBench：评估 LLM 作为智能体的能力

> 原文：[AgentBench](https://github.com/THUDM/AgentBench) · 智谱 Z.ai / THUDM

![](./assets/cover.jpg)

<p align="center">
   <a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vRR3Wl7wsCgHpwUw1_eUXW_fptAPLL3FkhnW_rua0O1Ji_GIVrpTjY5LaKAhwO-WeARjnY_KNw0SYNJ/pubhtml" target="_blank">🌐 排行榜（新版）</a> | <a href="https://twitter.com/thukeg" target="_blank">🐦 Twitter</a> | <a href="mailto:agentbench@googlegroups.com">✉️ Google Group</a> | <a href="https://arxiv.org/abs/2308.03688" target="_blank">📃 论文 </a>
</p>

<p align="center">
👋 欢迎加入我们的 <a href="https://join.slack.com/t/agentbenchcol-huw1944/shared_invite/zt-20ixabcuv-31cFLBAkqGQxQkJqrWVEVg" target="_blank">Slack</a>，参与<i>问答</i>或<i><b>共同协作开发</b>下一版 AgentBench</i>！
</p>

## 🔥[2025.10.10] 推出基于 [AgentRL](https://github.com/THUDM/AgentRL) 的 **AgentBench FC（函数调用）**

当前仓库包含 AgentBench 的函数调用版本，并与 [AgentRL](https://github.com/THUDM/AgentRL)（一个端到端多任务、多轮对话的 LLM 智能体强化学习框架）集成。
如果你想使用旧版本，可以回退到 [v0.1](https://github.com/THUDM/AgentBench/tree/v0.1) 与 [v0.2](https://github.com/THUDM/AgentBench/tree/v0.2)。

与原版 AgentBench 相比，本版本采用函数调用风格的提示词，
并为以下任务新增了完全容器化的部署支持：

- `alfworld` (AF)
- `dbbench` (DB)
- `knowledgegraph` (KG)
- `os_interaction` (OS)
- `webshop` (WS)

### 快速开始

我们支持使用 Docker Compose 为上述所有任务提供一条命令的快速搭建。

开始之前，请下载或构建以下任务所需的 Docker 镜像：

```shell
# dbbench
docker pull mysql:8

# os_interaction
docker build -t local-os/default -f ./data/os_interaction/res/dockerfiles/default data/os_interaction/res/dockerfiles
docker build -t local-os/packages -f ./data/os_interaction/res/dockerfiles/packages data/os_interaction/res/dockerfiles
docker build -t local-os/ubuntu -f ./data/os_interaction/res/dockerfiles/ubuntu data/os_interaction/res/dockerfiles
```

要运行 KG freebase 服务，你还需要一份可在[这里](https://github.com/dki-lab/Freebase-Setup)找到的数据。
下载数据、解压并放置到 `./virtuoso_db/virtuoso.db`（或者修改 `extra/docker-compose.yml`，将挂载点设置为你的数据所在位置）。

然后，你可以用以下命令启动整套服务：

```shell
docker compose -f extra/docker-compose.yml up
```

该命令会下载或构建必要的 Docker 镜像，并在 Docker 中启动以下服务：

- AgentRL 控制器
- `alfworld` 任务 worker（x1，按需增加）
- `dbbench` 任务 worker（x1，按需增加）
- `knowledgegraph` 任务 worker（x1，按需增加）
- `os_interaction` 任务 worker（x1，按需增加）
- `webshop` 任务 worker（x1，按需增加）
- freebase 服务（供 `knowledgegraph` 任务使用）
- Redis 服务（用于容器分配）

如果你的机器上已经运行了 Redis（7+ 版本），可以在 `docker-compose.yml` 中省略 Redis 服务。

> [!WARNING]  
> 请注意，`webshop` 环境需要约 16GB 内存才能启动，
> 且当前 `alfworld` 的实现会持续占用内存和磁盘空间，直到任务 worker 重启。
> 运行前请确保你的机器资源充足。

### 基准测试结果

我们汇报了各模型在 AgentBench FC 测试集上的结果。

![img.png](assets/fc_leaderboard.png)

完整结果请查看我们的[排行榜](https://docs.google.com/spreadsheets/d/e/2PACX-1vRR3Wl7wsCgHpwUw1_eUXW_fptAPLL3FkhnW_rua0O1Ji_GIVrpTjY5LaKAhwO-WeARjnY_KNw0SYNJ/pubhtml)。
如有任何问题或希望贡献你的结果，请联系 [agentbench_fc&#64;googlegroups.com](mailto:agentbench_fc@googlegroups.com)。

---

## 🔥[2024.08.13] 推出 [VisualAgentBench](https://github.com/THUDM/VisualAgentBench)

VisualAgentBench 旨在基于大型多模态模型（LMM）评估并训练视觉基础智能体。我们引入了 5 个不同的环境，涵盖

* 具身智能：VAB-OmniGibson、VAB-Minecraft
* GUI：VAB-Mobile、VAB-WebArena-Lite
* 视觉设计：VAB-CSS

系统地评测了 17 个 LMM（闭源与开源 LMM）。我们还提供了用于在开源 LMM 上进行行为克隆训练的轨迹数据集，帮助你开发属于自己的视觉基础智能体！

---

以下是原版 AgentBench（v0.2）的介绍。

# AgentBench：评估 LLM 作为智能体的能力

https://github.com/THUDM/AgentBench/assets/129033897/656eed6e-d9d9-4d07-b568-f43f5a451f04

**AgentBench** 是首个旨在评估 **LLM 作为智能体（LLM-as-Agent）**在多样化环境中表现的基准。它包含 8 个不同的环境，以更全面地评估 LLM 在各种场景中作为自主智能体运行的能力。这些环境中有 5 个是全新创建的领域，即

-   操作系统（OS）
-   数据库（DB）
-   知识图谱（KG）
-   数字卡牌游戏（DCG）
-   水平思考谜题（LTP）

以及 3 个基于已发表数据集重新编译的环境：

-   家庭事务（HH）（[ALFWorld](https://github.com/alfworld/alfworld)）
-   网络购物（WS）（[WebShop](https://github.com/princeton-nlp/webshop)）
-   网页浏览（WB）（[Mind2Web](https://github.com/OSU-NLP-Group/Mind2Web)）

![](./assets/agentbench.png)

## 目录

-   [数据集摘要](#数据集摘要)
-   [排行榜](#排行榜)
-   [快速开始](#快速开始)
-   [后续步骤](#后续步骤)
-   [引用](#引用)

## 数据集摘要

我们为每个数据集提供两个划分：Dev 与 Test。多轮交互分别要求 LLM 生成约 4k 与 13k 次响应。

![](./assets/statistics.png)

## 排行榜

以下是 AgentBench 测试集（标准）成绩。

![](./assets/leaderboard.png)

尽管 LLM 开始展现出其作为智能体的能力，但模型之间的差距以及距离实际可用水准仍有相当距离。

![](./assets/intro.png)

## 快速开始

本节将引导你快速使用 gpt-3.5-turbo-0613 作为智能体启动 `dbbench-std` 与 `os-std` 任务。
具体的框架结构请参考[框架介绍](docs/Introduction_en.md)。
更详细的配置与启动方法请查看[配置指南](docs/Config_en.md)
与[程序入口指南](docs/Entrance_en.md)。

### 第 1 步：前置准备

克隆本仓库并安装依赖。

> **Python 版本说明**：AgentBench 固定了较旧的科学计算 Python 依赖（例如 `numpy~=1.23.x`）。
> 使用推荐的 **Python 3.9**（通过 conda）是安装依赖最可靠的方式。

```bash
cd AgentBench
conda create -n agent-bench python=3.9
conda activate agent-bench
pip install -r requirements.txt
```

确保已正确安装 [Docker](https://www.docker.com/)。

```bash
docker ps
```

为 `dbbench-std` 与 `os-std` 构建所需的镜像。

```bash
docker pull mysql
docker pull ubuntu
docker build -f data/os_interaction/res/dockerfiles/default data/os_interaction/res/dockerfiles --tag local-os/default
docker build -f data/os_interaction/res/dockerfiles/packages data/os_interaction/res/dockerfiles --tag local-os/packages
docker build -f data/os_interaction/res/dockerfiles/ubuntu data/os_interaction/res/dockerfiles --tag local-os/ubuntu
```

### 第 2 步：配置智能体

在 `configs/agents/openai-chat.yaml` 的正确位置填入你的 OpenAI API Key。（例如 `gpt-3.5-turbo-0613`）

你可以尝试运行 `python -m src.client.agent_test` 来检查智能体是否配置正确。

默认情况下会启动 `gpt-3.5-turbo-0613`。你可以通过修改参数将其替换为其他智能体：

```bash
python -m src.client.agent_test --config configs/agents/api_agents.yaml --agent gpt-3.5-turbo-0613
```

### 第 3 步：启动任务服务

启动任务 worker 与具体任务相关。手动启动可能比较繁琐；因此，我们提供了自动化
脚本。

这一步的前提是 5000 到 5015 端口可用。对于 Mac OS 系统，你可以参考
[这里](https://stackoverflow.com/questions/69955686/why-cant-i-run-the-project-on-port-5000)释放 5000 端口以供使用。

```bash
python -m src.start_task -a
```

这会为 `dbbench-std` 与 `os-std` 任务各启动五个 task_worker，并自动将它们
连接到 5000 端口上的控制器。**执行该命令后，请等待约 1 分钟让任务搭建完成。**如果终端显示 ".... 200 OK"，你可以打开另一个终端并执行第 4 步。

#### Lite 预设（笔记本电脑 / 有限内存）

如果你想以最小并发（每个任务 1 个 worker）启动，请使用 lite 预设：

```bash
python -m src.start_task -a --config configs/start_task_lite.yaml
```

### 第 4 步：启动分配器

这一步才真正开始执行任务。

如果到目前为止一切都配置正确，你现在可以启动任务测试。

```bash
python -m src.assigner
```

如果你以 lite 预设启动了任务服务，也可以运行 lite 评测预设：

```bash
python -m src.assigner --config configs/assignments/lite.yaml
```

## 后续步骤

如果你想启动更多任务或使用其他模型，可以参考
[配置指南](docs/Config_en.md)与[程序入口指南](docs/Entrance_en.md)中的内容。

对于其余五个任务的环境，你需要下载我们提供的 Docker 镜像。

```
longinyu/agentbench-ltp
longinyu/agentbench-webshop
longinyu/agentbench-mind2web
longinyu/agentbench-card_game
longinyu/agentbench-alfworld
```

八个任务的单个 task_worker 资源消耗大致如下；启动时请据此考虑：

| 任务名称 | 启动速度 | 内存占用 |
| --------- | -------------- | ------------------ |
| webshop   | ~3min          | ~15G               |
| mind2web  | ~5min          | ~1G                |
| db        | ~20s           | < 500M             |
| alfworld  | ~10s           | < 500M             |
| card_game | ~5s            | < 500M             |
| ltp       | ~5s            | < 500M             |
| os        | ~5s            | < 500M             |
| kg        | ~5s            | < 500M             |


### 本地部署 KnowledgeGraph 服务
KnowledgeGraph 任务依赖一个在线服务，该服务目前并不稳定。如果你想本地部署该服务，可以按照以下步骤操作：

**step1.** <br />
下载数据库并搭建服务 [freebase-setup](https://github.com/dki-lab/Freebase-Setup)。


**step2.** <br />
将 `/configs/tasks/kg.yaml` 中的这一行 `sparql_url: "http://164.107.116.56:3093/sparql"` 改为 `sparql_url: "<你的 sparql 服务 api>"`。


**P.S.** 你应当在启动智能体任务服务之前先启动 KG 服务。

## 扩展 AgentBench

如果你想为 AgentBench 添加新任务，可以参考[扩展指南](docs/Extension_en.md)。

## 参考文献

Avalon 任务合并自 [AvalonBench](https://github.com/jonathanmli/Avalon-LLM/)，后者实现了一个多智能体框架。

## 引用

```
@article{liu2023agentbench,
  title   = {AgentBench: Evaluating LLMs as Agents},
  author  = {Xiao Liu and Hao Yu and Hanchen Zhang and Yifan Xu and Xuanyu Lei and Hanyu Lai and Yu Gu and Hangliang Ding and Kaiwen Men and Kejuan Yang and Shudan Zhang and Xiang Deng and Aohan Zeng and Zhengxiao Du and Chenhui Zhang and Sheng Shen and Tianjun Zhang and Yu Su and Huan Sun and Minlie Huang and Yuxiao Dong and Jie Tang},
  year    = {2023},
  journal = {arXiv preprint arXiv: 2308.03688}
}
```

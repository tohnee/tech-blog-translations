---
title: "MiMo-V2-Flash：面向高速推理与智能体工作流的 309B MoE 模型"
title_en: "XiaomiMiMo/MiMo-V2-Flash"
source: https://github.com/XiaomiMiMo/MiMo-V2-Flash/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-V2-Flash：面向高速推理与智能体工作流的 309B MoE 模型

> 原文：[XiaomiMiMo/MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash/blob/main/README.md) · 小米 MiMo

<br/><br/>

<div align="center">
  <picture>
    <source srcset="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/Xiaomi_MiMo_darkmode.png?raw=true" media="(prefers-color-scheme: dark)">
    <img src="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/Xiaomi_MiMo.png?raw=true" width="60%" alt="Xiaomi-MiMo" />
  </picture>
</div>

<br/>

<div align="center" style="line-height: 1;">
  |
  <a href="https://huggingface.co/XiaomiMiMo/MiMo-V2-Flash" target="_blank">🤗 HuggingFace</a>
  &nbsp;|
  <a href="https://github.com/XiaomiMiMo/MiMo-V2-Flash/blob/main/paper.pdf" target="_blank">📔 技术报告 </a>
  &nbsp;|
  <a href="https://mimo.xiaomi.com/blog/mimo-v2-flash" target="_blank">📰 博客 </a>
  &nbsp;|
  <br/><br/>
  <strong>来试试吧！</strong> &nbsp;
  <a href="https://aistudio.xiaomimimo.com" target="_blank">🗨️ 小米 MiMo Studio </a>
  &nbsp;
  <a href="https://platform.xiaomimimo.com/" target="_blank">🎨 小米 MiMo API 平台 </a>
</div>
<br/>

# MiMo-V2-Flash

**MiMo-V2-Flash** 是一个拥有 **309B 总参数**、**15B 激活参数** 的专家混合（MoE）语言模型。它为高速推理与智能体（agentic）工作流而设计，采用新颖的混合注意力架构与多 token 预测（MTP），在大幅降低推理成本的同时取得最先进（SOTA）的性能。

<p align="center">
  <img width="80%" src="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/MiMo-v2-flash-performance.jpg?raw=true">
</p>

-----

## 1. 简介

MiMo-V2-Flash 在长上下文建模能力与推理效率之间建立了新的平衡。关键特性包括：

  * **混合注意力架构**：以 5:1 的比例交错使用滑动窗口注意力（SWA）与全局注意力（GA），并采用激进的 128-token 窗口。这使 KV 缓存占用降低近 6 倍，同时通过可学习的 **attention sink 偏置** 保持长上下文性能。
  * **多 token 预测（MTP）**：配备轻量级 MTP 模块（每块 0.33B 参数），使用稠密 FFN。推理时输出速度提升至 3 倍，也有利于加速 RL 训练中的 rollout。
  * **高效预训练**：使用 FP8 混合精度与原生 32k 序列长度，在 27T token 上训练。上下文窗口支持最长 256k。
  * **智能体能力**：后训练采用多教师在线策略蒸馏（MOPD）与大规模智能体 RL，在 **SWE-Bench** 与复杂推理任务上取得卓越表现。

-----

## 2. 模型下载

| 模型                  | 总参数 | 激活参数 | 上下文长度 |                               下载                                |
| :--------------------- | :----------: | :-----------: | :------------: | :-------------------------------------------------------------------: |
| **MiMo-V2-Flash-Base** |     309B     |      15B      |      256k      | [🤗 HuggingFace](https://huggingface.co/XiaomiMiMo/MiMo-V2-Flash-Base) |
| **MiMo-V2-Flash**      |     309B     |      15B      |      256k      |   [🤗 HuggingFace](https://huggingface.co/XiaomiMiMo/MiMo-V2-Flash)    |

> [!IMPORTANT]
> 我们还开源了 3 层 MTP 权重，以促进社区研究。

-----

## 3. 评测结果

### 基座模型评测

MiMo-V2-Flash-Base 在标准基准测试中表现强劲，超过参数量显著更大的模型。

| 类别         | 基准测试               | 设定/长度 | MiMo-V2-Flash Base |  Kimi-K2 Base   | DeepSeek-V3.1 Base | DeepSeek-V3.2 Exp Base |
| :--------------- | :---------------------- | :------------- | :----------------: | :-------------: | :----------------: | :--------------------: |
| **参数量**       | **#激活 / #总量** | -              |   **15B / 309B**   | **32B / 1043B** |   **37B / 671B**   |     **37B / 671B**     |
| **通用**      | BBH                     | 3-shot         |        88.5        |      88.7       |        88.2        |          88.7          |
|                  | MMLU                    | 5-shot         |        86.7        |      87.8       |        87.4        |          87.8          |
|                  | MMLU-Redux              | 5-shot         |        90.6        |      90.2       |        90.0        |          90.4          |
|                  | MMLU-Pro                | 5-shot         |        73.2        |      69.2       |        58.8        |          62.1          |
|                  | DROP                    | 3-shot         |        84.7        |      83.6       |        86.3        |          86.6          |
|                  | ARC-Challenge           | 25-shot        |        95.9        |      96.2       |        95.6        |          95.5          |
|                  | HellaSwag               | 10-shot        |        88.5        |      94.6       |        89.2        |          89.4          |
|                  | WinoGrande              | 5-shot         |        83.8        |      85.3       |        85.9        |          85.6          |
|                  | TriviaQA                | 5-shot         |        80.3        |      85.1       |        83.5        |          83.9          |
|                  | GPQA-Diamond            | 5-shot         |        55.1        |      48.1       |        51.0        |          52.0          |
|                  | SuperGPQA               | 5-shot         |        41.1        |      44.7       |        42.3        |          43.6          |
|                  | SimpleQA                | 5-shot         |        20.6        |      35.3       |        26.3        |          27.0          |
| **数学**         | GSM8K                   | 8-shot         |        92.3        |      92.1       |        91.4        |          91.1          |
|                  | MATH                    | 4-shot         |        71.0        |      70.2       |        62.6        |          62.5          |
|                  | AIME 24&25              | 2-shot         |        35.3        |      31.6       |        21.6        |          24.8          |
| **代码**         | HumanEval+              | 1-shot         |        70.7        |      84.8       |        64.6        |          67.7          |
|                  | MBPP+                   | 3-shot         |        71.4        |      73.8       |        72.2        |          69.8          |
|                  | CRUXEval-I              | 1-shot         |        67.5        |      74.0       |        62.1        |          63.9          |
|                  | CRUXEval-O              | 1-shot         |        79.1        |      83.5       |        76.4        |          74.9          |
|                  | MultiPL-E HumanEval     | 0-shot         |        59.5        |      60.5       |        45.9        |          45.7          |
|                  | MultiPL-E MBPP          | 0-shot         |        56.7        |      58.8       |        52.5        |          50.6          |
|                  | BigCodeBench            | 0-shot         |        70.1        |      61.7       |        63.0        |          62.9          |
|                  | LiveCodeBench v6        | 1-shot         |        30.8        |      26.3       |        24.8        |          24.9          |
|                  | SWE-Bench (AgentLess)   | 3-shot         |        30.8        |      28.2       |        24.8        |          9.4*          |
| **中文**      | C-Eval                  | 5-shot         |        87.9        |      92.5       |        90.0        |          91.0          |
|                  | CMMLU                   | 5-shot         |        87.4        |      90.9       |        88.8        |          88.9          |
|                  | C-SimpleQA              | 5-shot         |        61.5        |      77.6       |        70.9        |          68.0          |
| **多语言** | GlobalMMLU              | 5-shot         |        76.6        |      80.7       |        81.9        |          82.0          |
|                  | INCLUDE                 | 5-shot         |        71.4        |      75.3       |        77.2        |          77.2          |
| **长上下文** | NIAH-Multi              | 32K            |        99.3        |      99.8       |        99.7        |         85.6*          |
|                  |                         | 64K            |        99.9        |      100.0      |        98.6        |         85.9*          |
|                  |                         | 128K           |        98.6        |      99.5       |        97.2        |         94.3*          |
|                  |                         | 256K           |        96.7        |        -        |         -          |           -            |
|                  | GSM-Infinite Hard       | 16K            |        37.7        |      34.6       |        41.5        |          50.4          |
|                  |                         | 32K            |        33.7        |      26.1       |        38.8        |          45.2          |
|                  |                         | 64K            |        31.5        |      16.0       |        34.7        |          32.6          |
|                  |                         | 128K           |        29.0        |       8.8       |        28.7        |          25.7          |

> \* 表示该模型可能无法遵循提示词或格式要求。

### 后训练模型评测

在我们的 MOPD + 智能体 RL 后训练范式之下，模型取得了 SOTA 的推理与智能体性能。



| 基准测试                      | MiMo-V2 Flash | Kimi-K2 Thinking | DeepSeek-V3.2 Thinking | Gemini-3.0 Pro | Claude Sonnet 4.5 | GPT-5 High |
| :----------------------------- | :-----------: | :--------------: | :--------------------: | :------------: | :---------------: | :--------: |
| **推理**                  |               |                  |                        |                |                   |            |
| MMLU-Pro                       |     84.9      |       84.6       |          85.0          |      90.1      |       88.2        |    87.5    |
| GPQA-Diamond                   |     83.7      |       84.5       |          82.4          |      91.9      |       83.4        |    85.7    |
| HLE（无工具）                 |     22.1      |       23.9       |          25.1          |      37.5      |       13.7        |    26.3    |
| AIME 2025                      |     94.1      |       94.5       |          93.1          |      95.0      |       87.0        |    94.6    |
| HMMT Feb. 2025                 |     84.4      |       89.4       |          92.5          |      97.5      |       79.2        |    88.3    |
| LiveCodeBench-v6               |     80.6      |       83.1       |          83.3          |      90.7      |       64.0        |    84.5    |
| **通用写作**            |               |                  |                        |                |                   |            |
| Arena-Hard（困难提示）       |     54.1      |       71.9       |          53.4          |      72.6      |       63.3        |    71.9    |
| Arena-Hard（创意写作）  |     86.2      |       80.1       |          88.8          |      93.6      |       76.7        |    92.2    |
| **长上下文**               |               |                  |                        |                |                   |            |
| LongBench V2                   |     60.6      |       45.1       |          58.4          |      65.6      |       61.8        |     -      |
| MRCR                           |     45.7      |       44.2       |          55.5          |      89.7      |       55.4        |     -      |
| **代码智能体**                 |               |                  |                        |                |                   |            |
| SWE-Bench Verified             |     73.4      |       71.3       |          73.1          |      76.2      |       77.2        |    74.9    |
| SWE-Bench Multilingual         |     71.7      |       61.1       |          70.2          |       -        |       68.0        |    55.3    |
| Terminal-Bench Hard            |     30.5      |       30.6       |          35.4          |      39.0      |       33.3        |    30.5    |
| Terminal-Bench 2.0             |     38.5      |       35.7       |          46.4          |      54.2      |       42.8        |    35.2    |
| **通用智能体**              |               |                  |                        |                |                   |            |
| BrowseComp                     |     45.4      |        -         |          51.4          |       -        |       24.1        |    54.9    |
| BrowseComp（配合上下文管理） |     58.3      |       60.2       |          67.6          |      59.2      |         -         |     -      |
| $\tau^2$-Bench                 |     80.3      |       74.3       |          80.3          |      85.4      |       84.7        |    80.2    |

-----

## 4. 模型架构

<p align="center">
  <img width="80%" src="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/MiMo-v2-flash-arch.png?raw=true">
</p>

### 混合滑动窗口注意力

MiMo-V2-Flash 通过交错使用局部滑动窗口注意力（SWA）与全局注意力（GA）来解决长上下文的二次复杂度问题。

  * **配置**：由 $M=8$ 个混合块堆叠而成。每个块包含 $N=5$ 层 SWA，后接 1 层 GA。
  * **效率**：SWA 层使用 128 token 的窗口大小，显著减少 KV 缓存。
  * **Sink 偏置**：应用可学习的 attention sink 偏置，即便窗口大小激进也能保持性能。

### 轻量级多 token 预测（MTP）

与传统的投机解码不同，我们的 MTP 模块在训练与推理中被原生集成。

  * **结构**：使用稠密 FFN（而非 MoE）和 SWA（而非 GA），以保持低参数量（每块 0.33B）。
  * **性能**：支持自投机解码，生成速度提升至 3 倍，并缓解小批量 RL 训练期间的 GPU 空闲。

-----

## 5. 后训练技术亮点

MiMo-V2-Flash 采用了一套后训练流水线，通过创新的蒸馏与强化学习策略最大化推理与智能体能力。

### 5.1 多教师在线策略蒸馏（MOPD）

我们提出**多教师在线策略蒸馏（Multi-Teacher On-Policy Distillation，MOPD）**，一种将知识蒸馏表述为强化学习过程的新范式。
* **密集的 token 级指导**：与依赖稀疏序列级反馈的方法不同，MOPD 利用领域专属的专家模型（教师）在每个 token 位置提供监督。
* **在线策略优化**：学生模型从自己生成的回复中学习，而非固定数据集。这消除了曝光偏差（exposure bias），并保证更小、更稳定的梯度更新。
* **天然的奖励鲁棒性**：奖励由学生与教师之间的分布散度导出，使整个过程天然抵抗奖励作弊（reward hacking）。

### 5.2 扩展智能体 RL

我们大幅扩展智能体训练环境，以提升智能水平与泛化能力。
* **海量代码智能体环境**：我们利用真实世界的 GitHub issue 创建了超过 100,000 个可验证任务。我们的自动化流水线维护着一个可运行超过 10,000 个并发 pod 的 Kubernetes 集群，环境搭建成功率为 70%。
* **面向 WebDev 的多模态验证器**：对于网页开发任务，我们采用基于视觉的验证器，通过录制视频而非静态截图评估代码执行效果。这减少了视觉幻觉，并确保功能正确性。
* **跨领域泛化**：我们的实验表明，代码智能体上的大规模 RL 训练能有效泛化到其他领域，提升数学与通用智能体任务的表现。

### 5.3 先进的 RL 基础设施

为支持大规模 MoE 模型的高吞吐 RL 训练，我们在 SGLang 与 Megatron-LM 之上实现了多项基础设施优化。
* **Rollout 路由重放（R3）**：解决 MoE 路由在推理与训练之间数值精度不一致的问题。R3 在训练阶段复用 rollout 时被选中的确切专家，以可忽略的开销确保一致性。
* **请求级前缀缓存**：在多轮智能体训练中，该缓存存储先前轮次的 KV 状态与路由专家。它避免了重复计算，并确保跨轮次的采样一致性。
* **细粒度数据调度器**：我们扩展了 rollout 引擎，使其调度细粒度序列而非微批次（micro-batch）。结合部分 rollout（partial rollout），显著减少了长尾掉队者造成的 GPU 空闲。
* **工具箱与工具管理器**：采用 Ray actor 池的两层设计来处理资源竞争。它消除了工具执行的冷启动延迟，并将任务逻辑与系统策略隔离。

-----

## 6. 推理与部署

MiMo-V2-Flash 支持 FP8 混合精度推理。我们推荐使用 **SGLang** 以获得最佳性能。

### SGLang 快速开始

参见 https://lmsys.org/blog/2025-12-16-mimo-v2-flash/，请使用如下兼容的 SGLang 版本。

```bash
pip install sglang==0.5.6.post2.dev8005+pr.15207.g39d5bd57a \
  --index-url https://sgl-project.github.io/whl/pr/ \
  --extra-index-url https://pypi.org/simple

#Launch the server
SGLANG_ENABLE_SPEC_V2=1 python3 -m sglang.launch_server \
        --model-path XiaomiMiMo/MiMo-V2-Flash \
        --served-model-name mimo-v2-flash \
        --pp-size 1 \
        --dp-size 2 \
        --enable-dp-attention \
        --tp-size 8 \
        --moe-a2a-backend deepep \
        --page-size 1 \
        --host 0.0.0.0 \
        --port 9001 \
        --trust-remote-code \
        --mem-fraction-static 0.75 \
        --max-running-requests 128 \
        --chunked-prefill-size 16384 \
        --reasoning-parser qwen3 \
        --tool-call-parser mimo \
        --context-length 262144 \
        --attention-backend fa3 \
        --speculative-algorithm EAGLE \
        --speculative-num-steps 3 \
        --speculative-eagle-topk 1 \
        --speculative-num-draft-tokens 4 \
        --enable-mtp

# Send request
curl -i http://localhost:9001/v1/chat/completions \
    -H 'Content-Type:application/json' \
    -d  '{
            "messages" : [{
                "role": "user",
                "content": "Nice to meet you MiMo"
            }],
            "model": "mimo-v2-flash",
            "max_tokens": 4096,
            "temperature": 0.8,
            "top_p": 0.95,
            "stream": true,
            "chat_template_kwargs": {
                "enable_thinking": true
            }
        }'
```

### 注意事项

#### 1. 系统提示词

> [!IMPORTANT]
> **强烈**建议使用以下系统提示词，请从英文版与中文版中任选其一。

英文版

```plaintext
You are MiMo, an AI assistant developed by Xiaomi.

Today's date: {date} {week}. Your knowledge cutoff date is December 2024.
```

中文版

```plaintext
你是MiMo（中文名称也是MiMo），是小米公司研发的AI智能助手。

今天的日期：{date} {week}，你的知识截止日期是2024年12月。
```

#### 2. 采样参数

> [!IMPORTANT]
> 推荐采样参数：
>
> `top_p=0.95`
>
> 数学、写作、网页开发使用 `temperature=0.8`
>
> 智能体任务（如 vibe-coding、工具使用）使用 `temperature=0.3`

#### 3. 工具使用实践

> [!IMPORTANT]
> 在带多轮工具调用的思考模式下，模型会随 `tool_calls` 一并返回 `reasoning_content` 字段。要继续对话，用户必须在后续每次请求的 `messages` 数组中保留全部历史 `reasoning_content`。

-----

## 7. 引用

如果你觉得我们的工作有帮助，请引用我们的技术报告：

```bibtex
@misc{xiao2026mimov2flashtechnicalreport,
      title={MiMo-V2-Flash Technical Report}, 
      author={LLM-Core Xiaomi},
      year={2026},
      eprint={2601.02780},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2601.02780}, 
}
```

## 8. 联系方式

如有任何问题，请通过 [mimo@xiaomi.com](mailto:mimo@xiaomi.com) 联系我们、加入下方微信群或提交 issue。

<p align="center">
  <img src="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/wechat_group/wechat1.jpg?raw=true" width="20%" />
  <img src="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/wechat_group/wechat2.jpg?raw=true" width="20%" />
  <img src="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/wechat_group/wechat3.jpg?raw=true" width="20%" />
  <img src="https://github.com/XiaomiMiMo/MiMo-V2-Flash/raw/main/figures/wechat_group/wechat4.jpg?raw=true" width="20%" />
</p>

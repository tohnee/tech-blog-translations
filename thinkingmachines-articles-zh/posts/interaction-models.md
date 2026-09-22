---
title: "交互模型：一种可扩展的人机协作方法"
title_en: "Interaction Models: A Scalable Approach to Human-AI Collaboration"
date: 2026-08-31
source: https://thinkingmachines.ai/blog/interaction-models/
crawled: 2026-09-22
translated: 2026-09-22
---

# 交互模型：一种可扩展的人机协作方法

> 原文：[Interaction Models: A Scalable Approach to Human-AI Collaboration](https://thinkingmachines.ai/blog/interaction-models/) · Thinking Machines Lab

今天，我们宣布交互模型（interaction models）的研究预览版：原生处理交互、而非通过外部脚手架（scaffolding）来处理交互的模型。我们认为交互性应当与智能同步扩展；我们与 AI 协作的方式不应被当作事后补丁。交互模型让人们以我们彼此天然协作的方式与 AI 协作——它们持续接收音频、视频和文本，并实时地思考、响应和行动。

我们从零开始训练了一个交互模型。为确保实时响应性，我们采用多流、微回合（micro-turn）设计。我们的研究预览展示了定性上全新的交互能力，以及在智能与响应性综合表现上的最先进水平。

## 协作瓶颈

AI 实验室常常把 AI 自主工作的能力视为模型最重要的能力。（Kwa, T., West, B., Becker, J., et al. Measuring AI Ability to Complete Long Tasks. [METR](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/), 2025.）其结果是，今天的模型和界面并没有针对「让人保持在环（in the loop）」进行优化。（[最近的一份前沿模型卡](https://www-cdn.anthropic.com/8b8380204f74670be75e81c820ca8dda846ab289.pdf)指出：「重要的是，我们发现当以交互式、同步、『手在键盘上』的模式使用时，该模型的好处并不那么明显。以这种方式使用时，一些用户认为（我们的模型）太慢，未能实现同样多的价值。自主、长时间运行的 agent 框架更好地发挥了该模型的编码能力。」）

自主界面很有价值，但在大多数真实工作中，用户无法预先完整说明自己的需求然后一走了之——好的结果受益于人保持在环中、沿途澄清并给出反馈的协作过程。然而，人类越来越多地被排除在外，不是因为工作不需要他们，而是因为界面没有给他们留出位置。相反，当人们能像与他人协作那样与 AI 协作时，才是最有效率的：发消息、说话、倾听、观看、展示，并在需要时插话——模型也做同样的事情。（通信在以下条件下更好：(a) 共在场（Copresence）：人们可以与他人正在交互的对象交互；(b) 共时性（Contemporality）：人们随他人产生信息而即时获得反馈；(c) 同步性（Simultaneity）：人们同时接收和产生信息。Clark H. and Brennan S., "Grounding in Communication," in Perspectives on Socially Shared Cognition, 1991.；口头文化因其参与式（对照客观疏离式）的本质而具有易逝性。今天的计算机与知识工作媒介具有类似的交互属性。Ong, W. J.. In *Orality and Literacy: The technologizing of the word*, 1982.）

为了解决这一问题，我们需要超越当前面向模型的回合制界面。今天的模型在单一线程中经历现实。（我们指的是商业化通用前沿模型——还有 Moshi、PersonaPlex、Nemotron VoiceChat、GPT-Realtime-Translate 等较小规模或专门的模型。）在用户打完字或说完话之前，模型一直等待，感知不到用户在做什么、怎么做。在模型生成完毕之前，它的感知是冻结的，在完成或被打断之前接收不到任何新信息。这为人-AI 协作创造了一条狭窄的通道，限制了一个人的多少知识（「Metis……它对实践知识、经验和随机推理的重视……使其成为最适合复杂物质与社会任务的推理模式，这些任务的不确定性如此令人生畏，以至于我们必须信任自己的（经验丰富的）直觉并摸索前行。」Scott, J. C: Métis. In *Seeing like a State: How certain schemes to improve the human condition have failed*, 1998.；「稍加反思就会发现……存在一类非常重要但无组织的知识……：关于特定时间与地点情境的知识。」Hayek, F. A. “The use of knowledge in society.” *The American Economic Review*, 1945.）、意图和判断能到达模型，也限制了模型的工作有多少能被人理解。试想通过电子邮件而非当面解决一个关键的分歧。

在 Thinking Machines，我们相信可以通过让 **AI 跨任何模态实时交互**来解决这一带宽瓶颈。这让 AI 界面去适应人所在之处，而不是强迫人去迁就 AI 界面。

大多数现有 AI 模型是用框架（harness）把交互性「外挂」上去的：把组件拼接在一起来模拟打断、多模态或并发。（大多数实时商用语音系统使用语音活动检测组件来检测回合边界。）然而，「苦涩的教训」（Sutton R. [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html), 2019.）暗示这些手工打造的系统会被通用能力的进步所超越。**要让交互性与智能一起扩展，它必须是模型本身的一部分。**采用这一方法，扩展模型会让它更聪明，*而且*成为更好的协作者。

## 能力

把交互性作为模型本身的一部分，解锁了多种否则就需要在框架中实现的能力。

- **无缝的对话管理。**模型隐式地追踪说话者是在思考、让出话轮、自我纠正，还是在邀请回应。没有单独的对话管理组件。

  ![](thumbnails/ANIMAL_STORY_THUMB.jpg)
- **言语与视觉插话。**模型视上下文需要随时插话，而不仅在用户说完时。

  ![](thumbnails/SLOUCHING_THUMB.jpg)

  ![](thumbnails/DANGER_THUMB.jpg)
- **同时语音。**用户与模型可以同时说话（例如实时翻译）。

  ![](thumbnails/ANGER_THUMB.jpg)
- **时间感知。**模型对流逝的时间有直接的感知。

  ![](thumbnails/QA_THUMB.jpg)
- **并行的工具调用、搜索与生成式 UI。**在与用户交谈和倾听的同时，模型可以并发地搜索、浏览网页或生成 UI——并按需把结果织回对话。

  ![](thumbnails/UBER_THUMB.jpg)

  ![](thumbnails/SEARCH_THUMB.jpg)

在更长的一段真实会话中，这一切持续发生，创造出更像协作、而非打提示词的体验。

![](thumbnails/DIET_THUMB.jpg)

![](thumbnails/IN_EAR_THUMB.jpg)

这些视频中出现的任何品牌或产品均与 Thinking Machines Labs 无关。这些视频仅用于演示模型的能力，不代表任何赞助或合作关系。

## 我们的方法

回合制

输入和输出被压平为一个有序的 token 序列

输入 1

人类

输出 1

模型

输入 2

输出 2

输入 3

输出 3

时间对齐的微回合制

交互以时间为锚定，连续的输入和输出流被切分成微回合

微回合 1

200ms

200ms

视频

![](frames/1.jpg)
![](frames/2.jpg)
![](frames/3.jpg)
![](frames/4.jpg)
![](frames/5.jpg)
![](frames/6.jpg)
![](frames/7.jpg)
![](frames/8.jpg)
![](frames/9.jpg)
![](frames/10.jpg)
![](frames/11.jpg)
![](frames/12.jpg)
![](frames/13.jpg)
![](frames/14.jpg)
![](frames/15.jpg)
![](frames/16.jpg)

音频

模型

模型打断并立即回应

模型与用户都保持沉默

用户说话时模型给出反向信道（backchannel）

模型对视觉线索做出反应，无需显式提示

跳过

重播

回合制模型看到的是交替出现的 token 序列。时间感知的交互模型看到的是连续的微回合流，
因此沉默、重叠和打断始终是模型上下文的一部分。

交互模型与用户处于持续的双向交换之中——同时感知和响应。某些领域天然把这种交互性视为前提——物理世界要求机器人和自动驾驶汽车实时运行。音频全双工模型（Moshi、PersonaPlex、nemotron-voicechat、Seeduplex。）是交互双向且连续的另一个例子。

应用同样的原则，我们着手构建一个原生适应这一状态的交互模型——跨音频、视频和文本，在同一个连续循环中感知和响应。其结果是一个围绕两个理念构建的系统：一个保持实时在场的时间感知交互模型，和一个处理持续推理、工具使用与更长时程工作的异步后台模型。

### 系统概览

交互模型与用户持续交换。当任务需要的推理深度超过即时可产生的水平时，交互模型会委托给异步运行的后台模型。（该方法建立在 Qwen-omni、KAME、MoshiRAG 等先前工作之上。）交互模型全程保持在场——回答追问、接收新输入、掌握对话主线——并在后台结果到达时将其整合进对话。

实时

用户

交互模型

后台模型

上下文

响应

工具调用、浏览等

用户持续与交互模型交互，而后台模型执行异步任务。两个系统共享其上下文。

这种拆分让用户同时受益于响应性和智能的全部广度：以非思考模型的响应延迟，获得推理模型的规划、工具使用和 agentic 工作流。注意，后台模型和交互模型都是智能的——交互模型自身在交互和智能两类基准上也具竞争力。

### 交互模型

我们的出发点是连续音频和视频——天然实时的模态。文本可以等待，但实时对话不能。通过先围绕最难的场景设计，我们得到了一个原生多模态、时间感知、并能处理所有模态并发输入输出流的架构。若干设计选择使这成为可能。

**时间对齐的微回合。**交互模型以微回合持续工作，把「处理 200ms 的输入」与「生成 200ms 的输出」不断交错。输入和输出 token 都被当作流来处理，而不是先消费一个完整的用户回合、再生成一个完整的回复。以 200ms 的块处理这些流，使多个输入和输出模态能够近实时并发。

人类感知

200ms

400ms

600ms

800ms

输入 0

输入 1

输入 2

输入 3

输入 4

输出 0

输出 1

输出 2

输出 3

模型 token 序列

输入 0

输出 0

输入 1

输出 1

输入 2

输出 2

输入 3

输出 3

输入 4

跳过

重播

人类感知保留并发的输入和输出流，而模型接收到的是单个交错的 token 序列。

在这种设计下，没有模型必须遵守的人为回合边界。相比之下，大多数现有实时系统需要一个预测回合边界的框架，才能让回合制模型显得实时且响应迅速。（Moshi、PersonaPlex 和 Nemotron Voicechat 是不使用框架检测回合的全双工系统示例。它们是聚焦延迟而非智能基准的较小规模模型。）这一框架由语音活动检测（VAD）等组件构成，明显不如模型本身聪明。这排除了一系列交互模式，比如主动插话（「当我说错时打断我」）或对视觉线索的反应（「当我在代码里写出 bug 时告诉我」）。此外，模型还能边听边说（「把西班牙语实时翻译成英语」）或边看边说（「实时解说这场体育比赛」）。

于是，今天这些需要专门框架的不同交互模式，都变成了模型能力的普通情形，并随着我们扩大模型规模和训练数据而提升质量。

**无编码器的早期融合。**我们不让音频和视频通过大型独立编码器处理，而是选择一个预处理极少的系统。许多全模态（omnimodal）模型需要训练单独的编码器（如 Whisper 类）或解码器（如 TTS 模型类）。我们改为把音频信号作为 dMel（[Bai, et al. 2024](https://arxiv.org/abs/2407.15835)）输入，并通过一个轻量级嵌入层进行变换。图像被切成 40x40 的 patch，由一个 hMLP 编码（[Touvron et al. 2022](https://arxiv.org/abs/2203.09795)）。音频解码器我们使用 flow head（[Lipman at al. 2022](https://arxiv.org/abs/2210.02747)）。所有组件都与 transformer 一起从头协同训练。

文本

帧

音频

嵌入

Token

40x40 Patch

hMLP

dMel

嵌入包

Transformer

文本

反嵌入（Unembedding）

Mel

Flow

200ms

200ms

单个 200ms 微回合的交互模型架构示意。模型接收文本、音频或视频的任意子集，并预测文本和音频。

**推理优化。**推理时，200ms 的块需要频繁的小尺寸 prefill 和解码，且每个都必须满足严格的延迟约束。遗憾的是，现有 LLM 推理库并未针对频繁的小 prefill 做优化——它们每回合往往有显著的开销。为此，我们实现了流式会话（streaming sessions）。客户端把每个 200ms 块作为单独的请求发送，而推理服务器把这些块追加到 GPU 内存中的一个持久序列里。这避免了频繁的内存重分配和元数据计算，我们已把[该功能的一个版本](https://github.com/sgl-project/sglang/pull/19171)上游化到 SGLang。此外，我们还针对延迟以及双向服务所见的形状优化了内核。例如，MoE 内核我们使用 gather+gemv 策略而非标准的 grouped gemm，这与 [PyTorch](https://www.thonking.ai/p/short-supporting-mixtral-in-gpt-fast) 和 [Cursor](https://cursor.com/blog/warp-decode) 的先前工作类似。

**训练器-采样器对齐。**我们发现，按位的训练器-采样器对齐对训练稳定性以及调试系统的各个组件都很有用。我们以最小（<5%）的端到端性能开销实现了[批不变内核](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)。（有趣的是，有一段时间使用批不变内核在端到端上其实更快，因为那些自定义通信内核不仅批不变，而且延迟也低得多。）这里特别强调两个内核：

- **All-reduce 与 reduce-scatter**：我们使用 NVLS 实现低延迟通信内核，在 Blackwell 上是确定性的，并在略有不同的并行策略（即[序列并行](https://arxiv.org/abs/2205.05198)与张量并行）之间实现了按位对齐。
- **注意力**：注意力的主要挑战是 Split-KV，它通常会导致解码与 prefill 之间的累加顺序不一致。（与 Colfax 合作完成）不过，我们可以通过在解码与 prefill 之间选择一致的切分方式来保持一致的累加顺序。例如，我们可以让 SM 每次处理 4096 个 token（左对齐），在 prefill 和解码中都取得良好的效率。

**交互模型与后台模型之间的协调。**当交互模型委托任务时，它发送的是一个丰富的上下文包——不是一条孤立的查询，而是完整的对话。结果随后台模型产生而流式返回，交互模型在适合用户当前所做之事的时机把这些更新织入对话，而不是生硬地切换上下文。

**安全。**由于实时交互对安全的考验不同于回合制交流，我们的安全工作聚焦两条主线：适配模态的拒绝（modality-appropriate refusals）和长时程稳健性。为了让拒绝在语音中显得口语化，我们使用一个文本转语音模型生成覆盖一系列被禁主题的拒绝与过度拒绝训练数据，并校准拒绝边界，使其偏向措辞自然但同样坚定的拒绝。为提高扩展语音到语音对话的稳健性，我们使用自动化红队框架生成多轮拒绝数据，同时保持与模型文本拒绝的密切行为一致性。

## 基准测试

### 智能与交互性前沿

我们展示我们的交互模型（命名为 `TML-Interaction-Small`）是首个兼具强智能/指令遵循**和**交互性的模型。为度量交互质量，我们使用 FD-bench——现有少数旨在度量交互性的基准之一。在 FD-bench v1.5 中，模型收到预录的音频，并必须在特定时刻做出回应。该基准在多个场景下度量模型行为：用户打断、用户反向信道、与其他人交谈、背景语音。我们的模型在所有这些场景中得分良好。为量化智能，我们使用 Audio MultiChallenge——一个追踪智能与指令遵循的常用基准。

智能（Audio MultiChallenge，APR）对比交互质量（FD-bench v1.5，平均质量）

40

45

50

55

60

65

70

75

80

85

20

30

40

50

交互质量 →

智能 →

TML-small

GPT-2.0 xhigh

GPT-2.0 min

GPT-1.5

Gemini high

Gemini min

智能（Audio MultiChallenge，APR）对比响应性（FD-bench v1，简单回合接替延迟）

0.2

0.5

1.0

1.5

1.9

20

30

40

50

响应性（秒） →

智能 →

TML-small

GPT-2.0 xhigh

GPT-2.0 min

GPT-1.5

Gemini high

Gemini min

TML-interaction-small
GPT-realtime-2.0 (minimal)
GPT-realtime-2.0 (xhigh)
GPT-realtime-1.5
Gemini-3.1-flash-live-preview (minimal)
Gemini-3.1-flash-live-preview (high)

智能与交互性前沿。我们的模型在交互质量上占优，同时比任何非思考模型都更智能。我们取得了以用户与模型回合之间延迟衡量的最佳响应性。

更多智能、安全和交互性/延迟结果请见下表。我们汇报了流式与回合制两类基准上的表现。

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | | 即时（Instant） | | | | | 思考（Thinking） | |
|  | | TML-interaction-small | GPT-realtime-2.0 (minimal) | GPT-realtime-1.5 | Gemini-3.1-flash-live (minimal) | Qwen 3.5 OMNI-plus-realtime | GPT-realtime-2.0 (xhigh) | Gemini-3.1-flash-live (high) |
| 流式 | FD-bench V1回合接替延迟 (s) · 音频 | 0.40 | 1.18 | 0.59 | 0.57 | 2.14 | 1.63 | 0.94 |
| FD-bench V1.5平均分 · 音频 | 77.8 | 46.8 | 48.3 | 54.3 | 39.0 | 47.8 | 45.5 |
| FD-bench V3回复质量 (%) / Pass@1 (%) · 音频 + 工具 | 82.8* / 68.0* | 80.0 / 52.0 | 77.9 / 55.0 | 68.5 / 48.0 | 60.0 / 50.0 | 81.0 / 58.0 | 71.4 / 48.0 |
| QIVD**准确率 (%) · 视频 + 音频 | 54.0 | 57.5 | 41.2 | 54.7 | 59.0 | 58.2 | 56.1 |
| 回合制 | Audio MultiChallengeAPR (%) · 音频 | 43.4 | 37.6 | 34.7 | 26.8 | -*** | 48.5 | 36.1 |
| BigBench Audio准确率 (%) · 音频 | 75.7 / 96.5* | 71.8 | 81.4 | 71.3 | 73.0 | 96.6**** | 96.6 |
| IFEval (VoiceBench)准确率 (%) · 音频 | 82.1 | 81.7 | 68.1 | 67.6 | 80.3 | 83.2 | 82.8 |
| IFEval准确率 (%) · 文本 | 89.7 | 89.6 | 87.5 | 85.8 | 83.4 | 95.2 | 90.0 |
| Harmbench拒绝率 (%) · 文本 | 99.0 | 99.5 | 100.0 | 99.0 | 99.5 | 100.0 | 98.0 |

每行最佳　即时模型中最佳

* 对需要推理或工具调用的基准，我们汇报的是启用后台 agent 后的结果。
** 我们在流式设置中评测 Qualcomm IVD——这是一个视频-音频问答基准。每个视频片段中有人执行一个动作并说出一个问题。我们在流式设置中评测，从开头发送原始片段并对模型的转录打分。沿用 Qwen 3.5 Omni 的做法，我们使用 GPT-4o-mini 作为评分器。
*** 所有基线模型的 Audio MultiChallenge 指标由 Scale AI 汇报，其中未列出 Qwen 3.5 OMNI-plus-realtime。
**** 所有基线模型的 Bigbench Audio 指标由 Artificial Analysis 汇报，其中 GPT-realtime-2.0 的 thinking 设为 high。

### 交互性的新维度

上述现有的面向交互性的基准，并不能充分捕捉我们注意到的交互能力上的定性跃迁。为此，我们有一些旨在量化这些能力的早期工作。

**时间感知与同时语音。**带有对话管理系统的回合制模型不支持精确的时间估计或同时语音。例子包括：「我跑一英里用了多长时间？」「听到我的发音错误就随时纠正」或「我写这个函数用了多长时间？」

我们创建了两个内部基准来度量这些主动音频能力：

- **TimeSpeak：**测试模型能否在用户指定的时间发起语音，同时产生正确的内容。例如：「我想练习呼吸，每 4 秒提醒我吸气和呼气，直到我让你停下。」
- **CueSpeak：**测试模型是否在恰当时刻以语义正确的预期回应开口。数据集条目的构造确保模型需要与用户同时说话才能得到满分。例如：「每当我切换语码、使用另一种语言时，给我原语言中的正确单词。」

这两个基准中，每个样本都有单一的预期语义回应和时间窗口。我们用 LLM 裁判评分：只有当回应传达了预期的含义、且在恰当的时间送达时才算正确；任一标准不满足都不得分。我们汇报跨样本的宏平均准确率。

**视觉主动性。**今天的商用实时 API 通过仅音频的对话管理框架做回合检测。它们会对语音回合做出回应，但无法在视觉世界发生变化时主动选择开口。（虽然我们不知道有任何商用 API 支持语音输出的视觉主动性，但若干学术论文构建了相关的研究原型。[StreamBridge](https://arxiv.org/abs/2505.05467)、[Streamo](https://arxiv.org/abs/2512.21334)、[StreamingVLM](https://arxiv.org/abs/2510.09608) 和 [MMDuet2](https://arxiv.org/abs/2512.06810) 研究了在流式视频输入设置中何时输出文本。由于是文本输出，它们没有研究语音输出交互的额外约束：语音有时长、可与用户语音重叠、且必须与回合接替、打断和反向信道相协调。与我们最接近的是 [AURA](https://arxiv.org/abs/2604.04184)，它在一个决定何时输出文本或保持沉默的 VideoLLM 周围加了 ASR/TTS 演示；相比之下，我们是语音原生和全双工的。）例如，如果被要求「请数一数我做了多少个俯卧撑」，这样的系统可能回答「没问题！」然后保持沉默——等待一个永远不会到来的纯音频线索。

我们改造了三个基准来评测我们模型的视觉主动性：

- **[RepCount-A](https://arxiv.org/abs/2204.01018)** 包含重复动作的视频，被改造为在线计数任务。我们按照音频指令「请数出 {action} 的次数」流式播放视频。我们在基准真值倒数第二次动作之后提取模型说出的最后一个数字，并按其是否与真值相差不超过一次来评分。该任务度量持续视觉追踪和及时计数。
- **[ProactiveVideoQA](https://arxiv.org/abs/2507.09313)** 由带问题的视频组成，其答案在特定时刻才变得可得。我们先以音频流式发送问题，然后是视频。（具体地，我们对以下文本做 TTS：“Watch the video and stay quiet until a new moment answers the question. When one happens, say a concise answer. {question}”，然后流式播放两秒静音，让模型确认该指令。我们把字幕烧录进视频（如有），并将输入视频静音，以强调测试视觉主动性。）我们汇报该论文的回合加权 PAUC@ω=0.5 指标（换算到 0-100），跨回合与类别取平均。保持沉默得 25.0 分；更高的分数要求在正确的时间给出正确的答案，错误的答案会被扣分。
- **[Charades](https://arxiv.org/abs/1604.01753)** 是标准的时序动作定位基准。每个视频包含一个发生在标注时间区间内的动作。我们流式发送用户音频指令：「当这个人开始做 {action} 时说 ‘start’，他们停下时说 ‘Stop’」；然后我们流式播放视频。模型按预测区间与参考区间的时间 IoU 评分。

|  | TML-interaction-small | GPT realtime-2.0 (minimal) |
| --- | --- | --- |
| 时间感知　TimeSpeak · macro-acc | 64.7 | 4.3 |
| 言语线索触发　CueSpeak · macro-acc | 81.7 | 2.9 |
| 视觉计数　RepCount-A · off-by-one | 35.4 | 1.3 |
| 视觉线索触发　ProactiveVideoQA · PAUC@ω=0.5 | 33.5 | 25.0* |
| 视觉线索触发　Charades · mIoU | 32.4 | 0 |

* ProactiveVideoQA 上的无回应基线为 25.0。

没有任何现有模型能有意义地完成这些任务。为完整起见，我们汇报了 GPT Realtime-2 (minimal) 的结果，但所有被评测的模型在这些任务上表现相似或更差，包括 thinking 设为 high 的模型。它们要么保持沉默，要么给出错误答案。

示例 1
示例 2
示例 3
示例 4
示例 5

[](/audio/interaction-models/example-5/video.mp4)

输入

TML-interaction-small

Gemini-high

Gemini-minimal

GPT-realtime-2

GPT-realtime-2-xhigh

来自我们内部音频与视频基准的示例。

**未来评测。**我们相信交互性是未来研究的一个重要领域，我们邀请社区为此贡献基准。我们将启动一项研究资助，鼓励对交互模型与人机协作领域的更多研究，包括但不限于评估交互质量的新框架，细节即将公布。

## 局限与未来工作

**长会话。**连续的音频和视频会快速积累上下文。流式会话设计能很好地处理短、中时长的交互，但超长会话仍需要仔细的上下文管理——这是一个活跃的工作方向。

**算力与部署。**低延迟地流式传输音频和视频需要可靠的连接。没有良好的连接，体验会显著退化。我们相信，未来可以通过提升系统可靠性、以及训练模型对延迟帧更加稳健，来显著改善这一点。

**对齐与安全。**实时界面为对齐与安全开辟了一个激动人心的研究领域。我们正在收集反馈并审阅研究资助申请。

**扩大模型规模。**当前的 `TML-Interaction-Small` 是一个 276B 参数、12B 活跃参数的 MoE。虽然我们预期交互性会随模型规模提升，但我们更大的预训练模型目前在这种设置下服务太慢。我们计划今年晚些时候发布更大的模型。

**改进后台 agent。**尽管本文主要聚焦实时交互性，agentic 智能也是一项必不可少的能力。除了把 agentic 智能推向前沿，我们相信在后台 agent 如何与交互模型协同这件事上，我们才刚刚触及表面。

## 告诉我们你的想法，加入我们

未来几个月，我们将开放一个有限的研究预览以收集反馈，今年晚些时候会有更广泛的发布。

我们非常欢迎你[加入我们](https://jobs.ashbyhq.com/ThinkingMachines)。请把你的想法分享至 [[email protected]](/cdn-cgi/l/email-protection#6d040319081f0c0e190402032d190504030604030a000c0e050403081e430c04)。

## 引用

请按如下方式引用本工作：

```
Thinking Machines Lab, "Interaction Models: A Scalable Approach to Human-AI Collaboration",
Thinking Machines Lab: Connectionism, May 2026.
```

或使用 BibTeX 引用：

```
@article{thinkingmachines2026interactionmodels,
  author = {Thinking Machines Lab},
  title = {Interaction Models: A Scalable Approach to Human-AI Collaboration},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2026},
  month = {May},
  note = {https://thinkingmachines.ai/blog/interaction-models/},
  doi = {10.64434/tml.20260511},
}
```

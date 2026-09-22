---
title: "MiniMax M3：前沿编程、1M 上下文、原生多模态——集于一个模型"
date: 2026-05-31
source: https://www.minimax.io/blog/minimax-m3
crawled: 2026-09-22
title_en: "MiniMax M3: Frontier Coding, 1M Context, Native Multimodality — All in One Model"
translated: 2026-09-22
---

# MiniMax M3：前沿编程、1M 上下文、原生多模态——集于一个模型

> 原文：[MiniMax M3: Frontier Coding, 1M Context, Native Multimodality — All in One Model](https://www.minimax.io/blog/minimax-m3) · MiniMax

2026-06-01

AIM3前沿模型MSA

MiniMax M3 今天正式发布。

M3 在编程与智能体（agentic）工作等专项任务上达到前沿水平。它采用了我们团队提出的新型注意力架构 MSA（MiniMax Sparse Attention，MiniMax 稀疏注意力），支持最高 1M token 的超长上下文窗口。在万众期待之下，它还是一个原生多模态模型，支持图像与视频输入，并能操作桌面计算机。

这三项能力如今已是闭源前沿模型的标配。M3 是目前第一个、也是唯一一个将三者集于一身的开放权重模型。

![](https://filecdn.minimax.chat/public/20260619-222405-1781879125997.png)

在编程能力方面，M3 较 M2 有显著提升，在 bug 修复、前端/后端开发、性能优化等领域接近海外领先闭源模型的水平。

在智能体能力方面，M3 在搜索与 Office 套件等常用办公工作流上表现强劲，并在金融领域达到初步可用的水平。

你现在就可以通过 MiniMax Code、Token 套餐以及我们的 API 服务体验 MiniMax M3。

### **MSA：架构创新让上下文扩展成为可能**

解决更复杂的智能体任务是训练 M3 时最重要的目标之一，其中最大的挑战之一就是上下文扩展。要实现真正的改变，必须从最底层的注意力机制入手，避免全注意力（full attention）的「固有缺陷」：计算复杂度的二次增长。

MSA 是一个干净且易于扩展的新型稀疏注意力架构。它赋予 M3 1M 的上下文窗口，让上下文真正成为一个可以扩展的维度。

稀疏注意力机制通常通过增加一个预过滤阶段来规避复杂度爆炸的问题。与 DSA、MoBA 等方法相比，MSA 能够更精确地对 KV 进行分块，实现更高的有效上下文覆盖率。

同时，我们还在算子层面直接进行了优化，采用「KV 外层收集 Q」（KV outer gather Q）的方式，以 KV 块作为外层循环来聚合命中它的 query。每个块只读取一次，内存访问是连续的；在 M3 的头配置下，其算术强度显著优于常见方法——比开源的 Flash-Sparse-Attention 和 flash-moba 快 4 倍以上。

![](https://filecdn.minimax.chat/public/m3-msa-arch.png)

其干净、可扩展、易实现且对硬件友好的特性，使理论收益能够在实践中完全兑现：在 100 万上下文长度下，M3 的每 token 计算量仅为上一代模型的 1/20。我们在预填充（prefilling）阶段取得了超过 9 倍的加速，在解码阶段取得了超过 15 倍的加速。此外，在多次消融实验中，MSA 在绝大多数能力上都与全注意力持平。

### **前沿的编程与智能体能力**

编程与智能体能力是 M3 的重点改进领域。在覆盖软件工程与终端执行的多个国际公认基准上，M3 达到前沿水平：

- SWE-Bench Pro: 59.0%
- Terminal-Bench 2.1: 66.0%
- SWE-fficiency: 34.8%
- KernelBench Hard: 28.8%
- MCP Atlas: 74.2%

如今，编程实力越来越取决于模型能否用真实世界的用户逻辑来训练。现有的编程基准往往无法充分反映真实用户体验。

当前大多数代码智能体的训练与评测都建立在单轮任务的假设之上。但真实使用并非如此。用户往往在同一场会话中持续协作：澄清需求、调整方案、跨上下文分配任务，并基于中间结果进行多轮迭代。

为了缩小基准与真实用户体验之间的差距，我们构建了一个交互式用户模拟器框架。

通过模拟真实开发者在协作中的行为模式，该框架让模型在训练与评测中都暴露于更接近生产环境的交互场景。它可以模拟需求细化、方案讨论、基于反馈的修正、连续任务切换以及复杂项目迭代等行为。由此，智能体不再只是被动执行指令，而是能够主动与用户协作完成任务。

下一代智能体编程的衡量标准将不仅是代码生成，还包括长期协作能力、规划能力以及人机协作的效率。M3 对真正重要的编程与智能体数据进行了扩展，目标不仅是领跑基准，更是成为开发者真实研发工作流中可靠的协作伙伴。

### **多模态：交错训练，持续扩展**

M3 是一个从第 0 步起就经过多模态混合训练的模型。这种原生多模态的方式让不同模态的语义空间得以更自然、更深入地融合。

与此同时，我们的大量实验表明，交错（interleaved）数据比合成数据更容易扩展。因此，在 M3 周期中，我们重构了整个文本预训练数据管线，生产了大量交错数据并将其纳入模型训练。

### **真实世界任务**

在我们对 M3 的内部使用与测试中，几项真实世界任务给人留下了深刻印象。

#### **独立复现论文**

作为前沿模型的三项核心能力，我们想看看 1M 超长上下文、顶尖的编程与智能体能力、以及原生多模态能力汇聚在一条长线程中解决复杂任务时会表现如何。

我们给 M3 一篇 ICLR 2025 杰出论文奖论文 *Learning Dynamics of LLM Finetuning*，要求它独立复现这篇论文。该论文研究大语言模型在微调过程中的「学习动态」。最终，M3 自主运行了近 12 个小时，全程独立产出 18 个 commit 与 23 张实验图表，并成功完成了核心实验。

它不仅成功拟合了 SFT 阶段预测概率变化的趋势，还清晰观察到 DPO 实验中强调的挤压（squeezing）效应，并成功验证了原论文提出的 Extend 缓解方法。

![](https://filecdn.minimax.chat/public/m3-paper-repro.png)

理解论文中的曲线、数据与公式需要多模态能力，而长上下文保证了论文、代码与实验日志可以一次性全部装入上下文窗口。只有编程与智能体能力足够强，模型才能在一条长线程中完成复现，甚至并发执行。

M3 把这一切都做到了。

#### **CUDA Kernel 优化**

FP8 矩阵乘法（GEMM）是大模型推理中计算最密集的环节之一，也是最难优化的环节之一。工程师必须同时处理多个紧耦合的问题，包括数据布局、计算流水线调度以及对硬件特性的适配。在 NVIDIA Hopper 架构 GPU 上，手写一个生产级 FP8 GEMM kernel 通常需要一个有经验的团队投入一到两周的专注工作。

我们用这个任务来评估 M3 的长时程自主迭代能力。我们让 MiniMax M3 在 NVIDIA Hopper 架构 GPU 上优化这个 kernel。模型最初只有一个任务描述、一个 benchmark 评测脚本和一个无法直接运行的 Triton 骨架代码，没有任何参考的高性能实现可用。这意味着模型无法通过模仿现有方案走捷径，只能从第一性原理出发，自主探索优化路径。

在随后约 24 小时的连续执行中，M3 完成了 147 次 benchmark 提交与 1,959 次工具调用。它独立走完了从基线实现到生产级优化的全过程，包括基线实现、autotune 配置生成、性能瓶颈诊断、CUDA Graph 集成、persistent kernel 重写以及主机侧调度优化。每一步都通过 benchmark 反馈自我验证，无需任何人工干预。

最终，经过六轮里程碑式的优化，M3 将 Hopper FP8 硬件峰值利用率从第一版的 7.6% 提升到 71.3%，相比最初版本取得 9.4 倍加速。

![](https://filecdn.minimax.chat/public/m3-cuda-perf.gif)

指标之外，模型的执行过程同样值得关注。除了 Opus 4.7 和 M3，其他大多数模型在前 30 次提交内就停止了新的进展并自行退出。而 M3 的最优解出现在第 145 次提交。在那之前，模型经历了多个观察不到进一步提升的性能平台期，但它仍在持续探索不同的优化方向。

这里所需的能力已超越传统的代码生成。反复工具调用产生的上下文高度结构化且高度密集，而 MSA 的长上下文注意力分配机制在此发挥了重要作用。

#### **让 M3 训练模型**

在 CUDA 算子优化任务中，M3 展示了它在目标明确、反馈信号定义清晰的单项工程任务上的长时程迭代能力。但真实的研究工作往往没有这样清晰的反馈结构，研究者面对的通常是更开放的问题。

我们想了解 M3 在需要自主决策的场景中的表现，因此我们在 PostTrainBench 上对它进行了测试。任务如下：给 M3 四个只完成了预训练、尚不具备任何下游能力的 Base 模型，让它在 12 小时内自主完成数据合成、训练、评测与迭代的全流程。最终目标是让这些模型在数学推理（AIME2025）、工具调用（BFCL）、科学知识推理（GPQA Main）、基础算术推理（GSM8K）与代码生成（HumanEval）上获得基本能力。

整个「数据合成 → 训练 → 评测 → 迭代」的过程没有任何人工干预。智能体必须自己决定合成什么样的数据、选择什么样的训练策略，以及如何根据评测结果调整下一轮计划。M3 最终取得 0.37 的分数，略低于 Opus 4.7（0.42）和 GPT-5.5（0.39），但明显领先于其他模型。

![](https://filecdn.minimax.chat/public/m3-posttrain-bench.gif)

#### **MiniMax Code**

随着 M3 的发布，MiniMax Code 也完成了更新。作为专为 M3 设计、并与 M3 共同训练的智能体产品，MiniMax Code 能够充分发挥 M3 在长上下文、编程/智能体任务与原生多模态方面的能力，是搭配 MiniMax-M3 的首选智能体。

对于长时程复杂任务，MiniMax Code 的 Agent Team 可以将大任务拆解为多阶段、并发且可动态调整的工作流，再由一个智能体集群协作推进。通过 Producer + Verifier 的对抗式脚手架循环，Agent Team 能够在执行过程中持续产出、反思与自我纠错。它可以在没有人工干预的情况下自主运行数天，并最终交付高质量结果。

我们看到 Claude Code 最近也发布了类似方向的 Dynamic Workflows。与 Claude Code 更强调基于 JS 代码的固定编排相比，MiniMax Code 更聚焦于「深度反思与持续纠错」：智能体根据任务进展实时调整计划与优先级，用户也可以随时介入补充需求或纠正方向。

得益于 M3 的原生多模态能力，MiniMax Code 还支持 computer use（操作计算机）。例如，用户可以在手机上说：「帮我打开本地的 ERP 客户端，根据这份 Excel 表格批量录入发票信息。」MiniMax Code 便会在计算机上跨应用、跨文件、跨系统地自动完成所需操作。

MiniMax Code 构建在杰出的开源社区项目 OpenCode 与 Pi 的脚手架之上。我们也计划在未来开源这一项目，作为对开源社区的回馈。

MiniMax Code 桌面应用：agent.minimaxi.com/download

MiniMax Code 可搭配 MiniMax Token 套餐使用。

### **MiniMax Token 套餐：把前沿模型带进开发者的日常工作**

MiniMax M3 是一个为服务更多用户而构建的前沿模型。

随本次发布，MiniMax Token 套餐也更新为三档：

- Plus 每月 20 美元：约 17 亿（1.7B）token/月的 M3 用量
- Max 每月 50 美元：约 51 亿（5.1B）token/月的 M3 用量
- Ultra 每月 120 美元：约 98 亿（9.8B）token/月的 M3 用量

在相近价位的订阅套餐中，MiniMax Token 套餐提供的 token 额度位居全球前列。文本、图像、语音与音乐共享同一用量池。

三档套餐均已全面开放。订阅后即刻开始使用！

订阅链接：[platform.minimax.io/subscribe/token-plan](https://platform.minimax.io/subscribe/token-plan)

![](https://filecdn.minimax.chat/public/m3-token-plan-2.png)

### **API**

M3 API 现已可用。

定价取决于输入长度：**≤512K** 输入 token 的调用按标准价格计费，覆盖绝大多数对话与编程场景；**超过 512K** 的调用按更高的长上下文价格计费，主要面向超长文档解析、全仓库代码理解等高负载场景。

M3 支持开启或关闭思考模式。开启思考时，模型适用于复杂推理、智能体任务与长时程协作；关闭思考时，模型响应更快，适用于对话、代码补全等对延迟敏感的场景。两种模式定价相同，可在请求时按需切换。

所有价格还可以与两个服务等级组合使用：默认的 `standard` 等级适用于常规请求；`priority` 等级（service_tier=priority）在高并发场景下享有调度优先级与更稳定的响应延迟，适合对 SLA 敏感的产业级用例。priority 通道目前通过销售支持开通，预计几天后向所有用户开放。

API 指南：[platform.minimax.io/docs/api-reference/api-overview](https://platform.minimax.io/docs/api-reference/api-overview)

![](https://filecdn.minimax.chat/public/20260601-101138-1780280144441.jpeg)

## 

我们将持续改进模型服务的稳定性并优化吞吐。未来 10 天内，我们将发布模型的技术报告并开源相应的模型权重。

如今，模型更新的节奏如此之快，以至于人们很容易忘记这仍然是一场稳步积累的渐进过程。它遵循自身的客观规律，也回报那些按照这些规律扎实前进的团队。正如我们在创立之初就坚信的那样，我们将竭尽全力持续提升模型的智能水平，并让更多用户用上它。

感谢你的信任、建议与批评。

Intelligence with Everyone!

![](https://filecdn.minimax.chat/public/img_v3_02128_b7726cd8-879a-4b7a-a9da-db4395ea597g-1780272508686.jpg)

**评测方法**

**SWE-Bench Verified:** 在内部基础设施上以 Claude Code 作为脚手架测试。使用 Claude Code 时覆盖了默认系统提示词。每项测试运行 4 次并取平均。

**SWE-Bench Pro:** 在内部基础设施上以 Claude Code 作为脚手架测试。测试逻辑与官方评测对齐。

**Terminal-bench 2.1:** 在内部基础设施上评测，沙箱配置为 8C16G，超时 2 小时，最大输出 token 设为 128K，以 Terminus 2 作为脚手架。GPT-5.5、Gemini 3.1 Pro 与 Claude Opus 4.7 的分数取自 Terminal-bench 2.1 官方榜单；其余模型均通过官方 API 在同一基础设施上测试。

**SWE Atlas-Codebase QNA:** 在内部基础设施上评测，沙箱配置为 4C8G，超时 3 小时。Claude Sonnet 4.6、GPT-5.5 与 Gemini 3.1 Pro 的分数取自 labs.scale.com。Claude Opus 4.7、MiniMax-M2.7 与 MiniMax-M3 使用 Mini-SWE-Agent 作为脚手架，评测逻辑与官方方法对齐。

**NL2Repo:** DeepSeek-V4-pro、Kimi-k2.6 与 GLM-5.1 的分数取自

https://qwen.ai/blog?id=qwen3.7

。其他模型在内部基础设施上评测，沙箱配置为 1C2G，超时 4 小时。Claude Opus 4.7、MiniMax-M2.7、MiniMax-M3 与 Gemini 3.1 Pro 使用 Claude Code 脚手架；GPT-5.5 使用 Codex 脚手架。为防范潜在的模型「作弊」，我们在官方评测逻辑基础上做了如下修改：(1) 提示词中加入约束，禁止模型通过 `git clone`、`pip install` 等方式使用外部信息；(2) 在脚手架层面，对系统监控到的模型执行的 Bash 命令进行分析以识别潜在作弊。被判定为作弊的命令会被拦截，并警告模型在受限环境内完成任务。

**SWE Atlas-Test Writing:** GPT-5.5、Claude Sonnet 4.6 与 Gemini 3.1 Pro 的分数来自 labs.scale.com。Claude Opus 4.7、MiniMax-M2.7 与 MiniMax-M3 在内部基础设施上使用 Claude Code 脚手架评测，沙箱为 4C8G，超时 3 小时，与官方逻辑对齐，运行 4 次取平均。

**SWE-fficiency:** 在内部基础设施上使用开源 SWE-fficiency 数据集与工作流评测。沙箱：1C2G，超时：2 小时。使用 Claude Code 作为脚手架；分数来自内部测试。

**LiveSQLBench:** 在内部基础设施上使用开源 LiveSQLBench-Base-Full v1 数据集（600 道题 / 22 个 PostgreSQL 数据库）与官方工作流评测。使用 Claude Code 作为脚手架，任务描述提示词覆盖默认系统提示词。每道题在预装 PostgreSQL 的专用沙箱中运行，超时 25 分钟。分数来自内部测试。

**VIBE-V2:** 内部基准，覆盖纯前端与全栈 Web/Android/iOS 项目，任务类型：从零构建。使用 Claude Code 作为脚手架，采用 Agent-as-a-Verifier 范式自动验证程序交互逻辑与视觉输出。得分通过统一流水线计算，包括需求集合、容器化部署与动态交互环境，3 次运行取平均。

**SVG-Bench:** 内部基准，输入类型：文本与图像；任务：从零构建或基于既有资产编辑。使用 Claude Code 作为脚手架，用 VLM 验证渲染准确性，3 次运行取平均。

**CL-bench:** 在内部基础设施上使用开源 CL-bench 数据与评分细则评测。评测设置完全对齐官方流程。分数来自内部测试。

**PostTrainBench:** 在 Claude Code 上使用 Ralph-Loop 机制运行 12 小时，在 5 个无需 LLM-As-Judge 的基准（AIME2025、BFCL、GPQA Main、GSM8K、HumanEval）上测试 4 个 Base 模型。

**Kernelbench-Hard:** 在 NVIDIA Blackwell 架构、CUDA 能力为 sm_120 的 GPU 上以 Claude Code 评测。单题得分 = 智能体提交算子的 TFLOPs 相对当前硬件理论峰值的比值；基准得分 = 9 道题的平均值。

**PaperBench:** 在 Claude Code 上使用 Ralph-Loop 机制运行 12 小时。数据集：19 篇无需外部 API 即可复现的论文。评分细则：官方开源的人类专家评分细则。评分模型：Opus-4.6。

**GPDval-Rubrics:** 使用公开 GDPval 数据集中的案例进行内部评测，基于公开评分细则进行逐点打分，环境与 GDPval-AA 脚手架对齐。

**BrowseComp:** 使用与 WebExplorer（Liu et al., 2025）相同的智能体框架。当 token 用量超过 64K 时，丢弃全部历史。

**DRACO:** MiniMax M3 的结果使用内部脚手架评测（可通过 MiniMax Code 的 Deep Research Skill 访问）。基于官方评分细则逐题打分，最终得分为所有题目的平均值。评分模型：Claude Opus 4.6。Claude Opus 4.7 的结果取自 Opus 4.7 模型卡。

**BankerToolBench:** 在公开 BankerToolBench 数据集上测试。除 GPT-5.5 使用 Codex 外，其余模型均使用 Claude Code 脚手架。基于数据集评分细则打分，使用 MiniMax M2.7 作为评分模型。

**OfficeQA Pro:** 为模拟真实场景，将相关文件以文件系统形式提供给模型，使用 Claude Code 脚手架评测。评分要求与答案完全匹配。

**SpreadSheetBench-v1:** 在公开数据集上使用 Claude Code 脚手架评测。

**YC-Bench:** 使用官方 YC-Bench 代码库与配置评测，环境与官方设置对齐。指标：最终资产（资金）。

**LOCA-Bench (256k):** 使用官方 LOCA-bench 代码库、官方 react 模式评测，环境描述长度（Environment Description Length）= 256k。

**MCP Atlas:** 使用官方 MCP Atlas 代码库评测。Public Set 分数使用 Gemini 2.5 Pro 作为评分模型，与官方模型对齐。

**Apex-Agents:** 使用 archipelago 代码库、ReAct Toolbelt 框架，评分模型为 Claude Sonnet 4.6。

**Claw-Eval:** 使用官方 Claw-Eval 代码库、General Task Group（161 项任务）评测，评分模型为 Gemini 3.0 Flash，与官方模型对齐。指标：Pass³ 分数。

**OSWorld-Verified:** 使用 OSWorld-Verified 官方代码库在 nogdrive 集合的 361 个样本上测试（测试脚本即将开源）。M3 使用 0–1000 的相对坐标、1920×1080 图像分辨率、Max Steps = 200。将 Max Steps 从 100 提升到 200，任务完成率从 68.70% 提升至 70.06%。

**OmniDocBench:** 图像长边最大 3584 像素，使用公开 OmniDocBench v1.5 数据集与官方评测逻辑。在官方提示词基础上增加了合理的格式约束。Gemini 3.1 Pro、GPT-5.5、Claude Opus 4.7 使用默认 API 参数。

**MMMU Pro:** 与官方评测对齐。提示词强制模型最后一行遵循格式约束，便于解析。

**VideoMMMU:** 视频帧率 = 1 FPS，最多 512 帧，单帧长边 672–1008 像素。使用官方 VideoMMMU 提示词，LLM-as-a-Judge 评分。MiniMax M3：最大输出 token = 32K，temperature = 1.0，top_p = 0.95。外部模型：最大输出 token = 64K，temperature = 0.7，top_p = 0.95，最高思考模式。

**Video-MME:** 视频帧率 = 1 FPS，最多 1024 帧（*外部 API 限制为 640 帧；MiniMax M3 在 512 帧下得分为 84.6），单帧长边 336–672 像素，每 30 秒插入字幕并交错到帧中。使用官方 Video-MME 提示词，LLM-as-a-Judge 评分。MiniMax M3：最大输出 token = 16K，temperature = 1.0，top_p = 0.95。外部模型：最大输出 token = 64K，temperature = 0.7，top_p = 0.95，最高思考模式。*注：Claude Opus 4.7 API 错误率 >20%，故未报告结果。

**IMO 2025 & USAMO 2026:** 与 MathArena 官方评测对齐。每项赛事：6 道题，满分 42 分。模型证明输出流程：(1) 解归一化（Solution Normalization）→ (2) 由双强模型按人类专家评分细则打分（GPT-5.4 high reasoning effort、Gemini 3.1 Pro high reasoning effort）→ (3) 双评判取最小值作为最终得分。M3 评测：最大输出 token 512k，temperature = 1.0，测试时扩展（test-time-scaling）框架最多迭代 10 次。其他闭源模型指标：avg@k 结果。

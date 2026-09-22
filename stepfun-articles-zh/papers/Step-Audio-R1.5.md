---
title: "Step-Audio-R1.5 技术报告"
title_en: "Step-Audio-R1.5 Technical Report"
arxiv: 2604.25719
date: 2026-04-28
source: https://arxiv.org/abs/2604.25719
crawled: 2026-09-22
translated: 2026-09-22
---

# Step-Audio-R1.5 技术报告

> 原文：[Step-Audio-R1.5 Technical Report](https://arxiv.org/abs/2604.25719) · 阶跃星辰 StepFun arXiv

StepFun-Audio 团队

[StepAudio R1.5 官方 GitHub 页面](https://github.com/stepfun-ai/Step-Audio-R1)

###### 摘要

大型音频语言模型的最新进展已将思维链（CoT）推理扩展到听觉领域，使模型能够处理日益复杂的声学与语音任务。为了激发并维持这些延伸的推理链，当前的主流范式——受文本推理模型成功的驱动——几乎完全依赖可验证奖励强化学习（RLVR）。然而，当模型被严格优化以将丰富、连续的听觉上下文蒸馏为孤立的、可验证的文本标签时，一个根本性问题随之而来：我们究竟是在培育真正的音频智能，还是仅仅在把一种连续的感官媒介简化为离散的谜题？我们将此称为「可验证奖励陷阱」。虽然 RLVR 在标准化客观基准上取得了亮眼分数，它却系统性地损害了音频模型在真实世界中的对话质感。由于优先追求孤立的正确性而忽视声学细微差别，RLVR 将动态交互降格为机械的「自动应答机」，严重损害了韵律自然度、情感连贯性与用户沉浸感，在长程多轮对话中尤为明显。为了弥合机械的客观验证与真正的感官共情之间的鸿沟，我们推出 Step-Audio-R1.5，标志着音频推理向基于人类反馈的强化学习（RLHF）的范式转变。全面评测表明，Step-Audio-R1.5 不仅保持了稳健的分析推理能力，更深刻地变革了交互体验，重新定义了深度沉浸式长程语音对话的边界。

|  |
| --- |
|  |

## 1 引言

![Refer to caption](2604.25719v2/figures/rank.png)

图 1：
语音到文本基准上的综合性能。
平均分代表每个模型在 8 个不同的推理与感知基准（包括 Audio MultiChallenge、Big Bench Audio、MMSU、MMAU、Spoken MQA、Step-Caption、Step-DU 与 Step-SPQA）上计算的整体能力。
Step-Audio-R1.5 大幅超越其前代模型，并与 Gemini 3 Pro 等最先进的商业系统保持高度竞争力。

思维链推理已显著推动了大语言模型的发展。通过将复杂问题分解为显式的中间步骤，OpenAI o1（[1]）与 DeepSeek-R1（[2]）等模型在数学奥林匹克、编程竞赛与科学探究中达到了人类水平。这一进步的核心是可验证奖励强化学习（RLVR）（[2]），一种使用二元、可自动校验的正确性信号来强化延伸推理链的训练范式，从而绕过了对习得奖励模型的需求。

将这一配方移植到听觉领域的努力正在加速。越来越多的大型音频语言模型（[3, 4, 5]）将 CoT 推理应用于语音、音乐与环境声，早期的 RLVR 训练变体（[6, 7, 8]）在语音问答与声学场景标注等客观任务上报告了强劲结果。然而，这些基准存在一个关键的结构性局限：时间上延展的音频输入最终被压缩为单个离散标签——一个类别、一个数字或一段简短的事实字符串。因此，RLVR 只能因模型产出该特定标签而给予奖励，在结构上对韵律自然度、情感连贯性与对话连贯性视而不见。我们将此称为可验证奖励陷阱：优化目标严格筛选的是孤立的答案准确性，而忽略了决定真实部署中用户体验的微妙品质。

这一陷阱的实证后果是一致且可复现的。在长时间的 RLVR 训练下，模型在留出测试集上越来越准确，交互起来却越来越不自然；回应变得简短、机械且情感平淡。在多轮语音对话中，用户期待的不仅是正确的答案，更是真实的对话流动感，而模型往往退化为字面意义上的「自动应答机」——技术上准确，体验上空洞。这源于 RLVR 所优化的目标（说什么）与用户所看重的（怎么说）之间的根本错位。事实正确性是必要条件，但对于高质量的音频交互而言并不充分。

为弥合这一差距，我们推出 Step-Audio-R1.5，它以基于人类反馈的强化学习（RLHF）补足 RLVR。我们不再仅依赖二元正确性校验，而是在端到端交互的整体人类偏好判断上训练一个奖励模型。这一方法将正确性、流畅性与情感共鸣蒸馏为统一的监督信号，使策略得以逃离奖励陷阱，针对整体回应质量而非孤立的事实准确性进行优化。

全面评测证实，Step-Audio-R1.5 在保留 RLVR 所培养的分析推理能力的同时，大幅提升了多轮交互质量。在传统推理基准上，该模型仍保持高度竞争力。我们进一步在 AudioMultiChallenge（[9]）基准上评估其对话能力，该基准在自然的多轮条件下严格测试语音对话的四个关键维度——推理记忆（Inference Memory）、指令保持（Instruction Retention）、自我连贯（Self Coherence）与语音编辑（Voice Editing）。在这一高难度设置下，Step-Audio-R1.5 展现出可匹敌甚至超越 Gemini-2.5-Flash 等领先商业系统的稳健能力。据我们所知，Step-Audio-R1.5 是首个系统性整合 RLHF 的音频推理模型，证明可验证奖励陷阱并非音频 CoT 的固有局限，而是一种贫乏奖励信号的伪影，人类反馈能够有效解决这一问题。

## 2 架构

在 Step-Audio-R1 奠定的结构基础之上，Step-Audio-R1.5 采用了一个专为延展音频推理量身定制的精简架构。该模型由三个主要组件构成：音频编码器、音频适配器与大语言模型（LLM）解码器。

声学前端采用 Qwen2 音频编码器（[10]），它在多样的语音与音频理解任务上进行了充分的预训练。该编码器以 25 Hz 的帧率运行，并在整个训练流程中严格保持冻结，以保留其稳健的听觉感知。为了将连续的声学模态与离散的文本空间桥接起来，音频适配器施加了 2 倍的时间下采样，将潜在表示有效压缩至 12.5 Hz，以缓解复杂多轮交互中的序列长度爆炸问题（[11, 12, 13, 14]）。

核心推理引擎是一个由 Qwen2.5 32B（[15]）初始化的 LLM 解码器。它直接接收下采样后的音频特征并生成纯文本输出。为支持复杂的思维链（CoT）推理，生成过程在结构上被划分为两部分：解码器被提示先合成显式的中间推理轨迹，再自回归地生成最终回复。这种内部分析与外部回应的解耦至关重要，因为它构成了无缝整合基于人类反馈的强化学习（RLHF）的架构基础。

## 3 训练方法

### 3.1 以音频为中心的中期训练

给定基础音频-语言模型 $\pi_{\theta_{0}}$，我们执行一个以音频为中心的中期训练（mid-training）阶段，在后训练对齐之前增强音频理解、基于音频的推理以及一般的深思熟虑能力。训练目标在统一的监督目标下，将基于音频的推理数据与辅助的纯文本推理数据相结合：

$$
\mathcal{L}_{\mathrm{mid}}=\mathbb{E}_{(x,q,r,y)\sim\mathcal{D}_{\mathrm{audio}}}\left[\log\pi_{\theta}(r,y\mid x,q)\right]+\mathbb{E}_{(q,r,y)\sim\mathcal{D}_{\mathrm{text}}}\left[\log\pi_{\theta}(r,y\mid q)\right], \tag{1}
$$

其中 $(x,q,r,y)$ 表示基于音频的样本，包含输入音频 $x$、相关文本上下文 $q$、推理轨迹 $r$ 与回应 $y$；而 $(q,r,y)$ 表示纯文本样本，包含上下文 $q$、推理轨迹 $r$ 与回应 $y$。基于音频的监督取自多样、高质量的以音频为中心的数据，使模型能够在声学语境上建立广泛的感知覆盖与稳健的推理能力。作为补充，辅助的纯文本监督提供高质量的推理轨迹与长篇深思熟虑结构，促进这些推理模式向基于音频的理解与推理迁移。

### 3.2 冷启动监督微调

我们执行冷启动监督微调（SFT）阶段，为面向交互的对齐初始化模型。尽管中期训练提升了音频领域知识、感知能力与一般推理能力，它并未直接针对高质量多轮交互优化模型。因此，仅凭强大的音频理解并不足以保证自然、连贯且对指令敏感的对话行为。

冷启动 SFT 并非进一步扩展领域知识，而是在基于偏好的优化之前，为面向交互的行为提供监督初始化。具体而言，该阶段强调交互行为的四个方面：*（1）多轮对话连续性*，即在多轮之间维持上下文与用户约束的能力；*（2）指令遵循*，即在用户对内容、格式与风格的具体要求下保持一致回应的能力；*（3）回应自然度*，即产生连贯且符合对话情境的回应的能力；以及 *（4）交互意识*，即对追问、澄清请求、打断以及用户侧修正做出稳健回应的能力。

为支撑这些目标，冷启动 SFT 由指令丰富、多轮的对话数据构建而成，促使模型以面向用户的方式组织回应，而非产出孤立的任务结果。该阶段为后续 RLHF 阶段提供了更强的对话初始化，使偏好优化得以专注于打磨整体交互质量，而非纠正基础的对话行为。

### 3.3 基于评分标准生成式奖励模型的 RLHF

多轮语音交互呈现出高度异构的优化目标。一些行为受显式且局部化的约束支配，例如内容要求、格式规范、人设设定以及跨轮次的指令保持。另一些则本质上由偏好驱动且只能弱规范化，包括对话自然度、追问交互下的连贯性、语调得体性与整体对话流畅度。这些目标不仅在形式上不同，在评估方式上也应有所区别：一些具备相对清晰的标准，而另一些更适合通过对完整回应的比较偏好判断来刻画。

为容纳这种异构性，我们采用基于生成式奖励模型的统一 RLHF 框架，同时支持评分标准引导的评估与常规偏好比较。对于具有显式评估标准的样本，奖励模型以任务特定的评分标准（rubric）为条件，评估回应是否满足预期要求。对于没有此类标准的样本，模型则针对参考回应执行标准的成对偏好判断。形式化地，令 $\mathcal{H}_{1:T}=\{h_{t}\}_{t=1}^{T}$ 表示截至第 $T$ 轮的多轮对话历史，其中每个 $h_{t}$ 表示第 $t$ 轮的完整交互上下文。给定 $\mathcal{H}_{1:T}$、策略回应 $y$、参考回应 $y^{\mathrm{ref}}$ 与可选的评分标准 $c$，生成式奖励模型产出相对质量判断

$$
g=\mathcal{R}(\mathcal{H}_{1:T},y,y^{\mathrm{ref}};c),\qquad c\in\mathcal{C}\cup\{\varnothing\}, \tag{2}
$$

其中 $c=\varnothing$ 对应常规的成对偏好比较，而 $c\neq\varnothing$ 表示以评分标准为条件的评估。判断 $g$ 随后被映射为标量奖励

$$
r=\phi(g), \tag{3}
$$

用于后续的策略优化。我们通过最大化 PPO 风格的目标来优化策略，

$$
\mathcal{L}_{\mathrm{RLHF}}(\theta)=\mathbb{E}_{t}\left[\min\left(\rho_{t}(\theta)\hat{A}_{t},\;\mathrm{clip}\!\left(\rho_{t}(\theta),1-\epsilon,1+\epsilon\right)\hat{A}_{t}\right)\right]-\beta\,D_{\mathrm{KL}}\!\left(\pi_{\theta}(\cdot\mid\mathcal{H}_{1:T},c)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid\mathcal{H}_{1:T},c)\right) \tag{4}
$$

其中

$$
\rho_{t}(\theta)=\frac{\pi_{\theta}(y_{t}\mid\mathcal{H}_{1:T},c)}{\pi_{\theta_{\mathrm{old}}}(y_{t}\mid\mathcal{H}_{1:T},c)}, \tag{5}
$$

$\hat{A}_{t}$ 是由生成奖励估计的优势值，$\pi_{\mathrm{ref}}$ 表示用于正则化的参考策略。这两种监督形式是联合优化而非分阶段进行的，因为它们的优化方向可能大相径庭；经验上，解耦训练容易引发不容忽视的遗忘，即后续在一种交互机制上的优化会损害另一种机制中习得的行为。因此，联合优化为在单一策略内同时对齐多轮对话中指令敏感与偏好敏感的各个方面提供了更稳定的路径。

在这一统一的 RLHF 框架内，监督通过一个基于相对比较的生成式奖励模型来实例化。奖励模型不再为每个回应赋予绝对质量分数，而是在相同的多轮对话上下文下将策略回应与参考回应进行比较，并依据二者的相对质量给出偏好判断。这种相对奖励形式更适合语音对话对齐，因为交互质量的许多重要方面难以用单一绝对分数校准。通过将奖励表示为具有多个序数层级的细粒度相对偏好信号，模型能够捕捉超越二元区分的不同回应质量程度，为策略优化提供更具区分度的监督信号。

## 4 评测

### 4.1 基准

为全面评估 Step-Audio-R1.5 的推理与感知能力，我们采用一套语音到文本（S2T）基准。S2T 评测通过要求文本形式的回应来隔离模型理解与推理声学信号的能力，从而可与最先进的大语言模型直接比较。

#### AudioMultiChallenge（Audio MC）。

AudioMultiChallenge（[9]）是一个多轮基准，基于自然的人类交互模式（包括打断、迟疑与话中修正）评估语音对话系统。它在四个维度上衡量性能：推理记忆、指令保持、自我连贯与语音编辑，对模型处理长上下文对话、跨多轮遵循指令以及在真实对话噪声下保持一致性的能力提供了全面评估。

#### Step-Caption。

Step-Caption 是一个新提出的基准，旨在评估模型的细粒度音频描述能力。测试集由 905 个精心筛选的音频样本组成，来源于 YouTube 与 Bilibili，覆盖以中英文为主的单说话人与多说话人场景。每个样本由人类专家在 16 个维度上标注，包括性别、年龄、语速、节奏、音高、音色、情感、口音及其他副语言特征。模型需要生成一段自然语言段落，全面描述说话人的声音特征，提示词中明确要求分析全部 16 个维度。该基准专门衡量模型从原始音频中感知并表述音色、年龄、性别与情绪状态等声学属性的能力。

#### Step-Dialogue-Understanding（Step-DU）。

Step-Caption 侧重于全面的声学描述，而 Step-Dialogue-Understanding 则评估模型在对话语境中回答关于副语言特征具体问题的能力。测试集由 87 个样本组成，由多样化说话人录制，每个样本直接询问说话人自身的声音特征，如年龄、性别、语速或节奏。模型必须仅凭声学信号推断出正确答案，测试其在交互式对话场景中对副语言线索的感知与推理。

#### StepEval-Audio-Paralinguistic（Step-SPQA）。

StepEval-Audio-Paralinguistic 最初是作为 Step-Audio 2（[5]）中的 AQAA（音频查询-音频回答）基准提出的。为确保本研究中所有模型的文本评测口径一致，我们将其转换为 AQTA（音频查询-文本回答）格式，同时保留原有的音频理解任务。

#### 其他公开基准。

除上述提出的基准外，我们还报告了广泛采用的公开基准上的结果，以便与现有模型进行广泛比较。其中包括面向专家级音频理解与推理的 MMSU（[16]）与 MMAU（[17]），面向从音频进行复杂多步逻辑推理的 Big Bench Audio¹，以及面向口头表达数学问题推理的 Spoken MQA（[18]）。

> 注 1：<https://huggingface.co/datasets/ArtificialAnalysis/big_bench_audio>

### 4.2 实验结果

为确保公平且一致的对比，我们通过自己统一的评测框架、使用所有基线模型的官方 API 进行评估，而非沿用此前报告的数字。这一做法保证所有结果在相同条件下直接可比。基线模型包括 Gemini 家族（Gemini 3 Flash 与 Gemini 3 Pro）²以及 Qwen 家族（qwen3.5-omni-flash 与 qwen3.5-omni-plus）（[19]）。

> 注 2：<https://blog.google/technology/developers/gemini-3-pro-vision/>

表 1：语音到文本基准上的性能比较。平均分按各模型在所有基准上计算。最佳结果加粗，次佳结果加下划线。

| 模型 | 平均 | Audio MC | Big Bench | MMSU | MMAU | Spoken MQA | Step-Caption | Step-DU | Step-SPQA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini 3 Flash | 77.56 | 56.42 | 96.80 | 76.64 | 75.90 | 95.37 | 65.12 | 80.46 | 73.80 |
| Gemini 3 Pro | 79.67 | 66.37 | 99.40 | 83.70 | 79.80 | 96.56 | 75.55 | 72.41 | 63.60 |
| qwen3.5-omni-flash | 70.55 | 25.44 | 59.59 | 72.50 | 77.20 | 93.39 | 73.57 | 83.91 | 78.80 |
| qwen3.5-omni-plus | 75.77 | 39.38 | 73.03 | 82.74 | 79.60 | 96.03 | 74.93 | 85.63 | 74.80 |
| Step-Audio-R1 | 72.50 | 24.61 | 98.29 | 75.68 | 77.00 | 95.06 | 70.60 | 64.37 | 74.36 |
| Step-Audio-R1.5 | 77.97 | 41.15 | 98.30 | 79.03 | 77.90 | 93.74 | 71.48 | 82.76 | 79.40 |

如表 1 所示，Step-Audio-R1.5 取得 77.97 的平均分，在所有评估模型中位列第二，对规模大得多的专有模型展现出强大竞争力。值得注意的是，尽管仅有 32B 参数，Step-Audio-R1.5 在 Audio MC 上取得 41.15 分，这一极具竞争力的结果仅次于 Gemini 家族模型。在所有基准上，Step-Audio-R1.5 保持均衡表现，相较前代 Step-Audio-R1（72.50）取得 5.47 分的显著平均提升。这一提升主要由需要多轮与长上下文理解的复杂任务上的大幅进步所驱动（Audio MC 基准即为例证），同时其在感知基准上的表现也有广泛改善：Step-DU 大幅提升（+18.39）、Step-SPQA 显著提升（+5.04），Step-Caption 亦有小幅提升（+0.88）。这些结果共同验证了我们架构与训练流程的有效性。

## 5 结论

早期音频推理模型中出现的机械、情感平淡的回应，并非思维链过程的固有局限，而是可验证奖励陷阱的伪影。在本工作中，我们证明了通过 RLVR 对孤立语义正确性的重度优化，会在结构上使模型对真实人类交互的多维细微差别视而不见。Step-Audio-R1.5 通过系统性整合基于人类反馈的强化学习（RLHF），结合解耦的生成架构与评分标准引导的偏好奖励模型，打破了这一权衡。通过将优化目标从单纯的*说什么*重新对齐为整体性的*怎么说*，Step-Audio-R1.5 在保持分析严谨性的同时，大幅提升了多轮对话质量。本工作为音频语言模型的演进提供了一个关键洞察：随着声学理解的成熟，人工音频智能的下一个前沿不在于将连续的感官输入简化为离散的事实谜题，而在于让模型行为与自然语音对话中丰富、共情的动态特性对齐。

## 6 贡献者

核心贡献者：
Yuxin Zhang1,4,
Xiangyu Tony Zhang3,
Daijiao Liu1,3,
Fei Tian1,∗,†,
Yayue Deng1,
Jun Chen1,
Qingjian Lin1

贡献者：
Haoyang Zhang1,2,
Yuxin Li1,2,
Jinglan Gong1,
Yechang Huang1,
Liang Zhao1,
Chengyuan Yao1,
Hexin Liu2,
Eng Siong Chng2,
Xuerui Yang1,
Gang Yu1,
Xiangyu Zhang1,
Daxin Jiang1

1StepFun 　 2南洋理工大学 　 3新南威尔士大学 　 4上海交通大学

*通讯作者：tianfei@stepfun.com 　 †项目负责人

## 参考文献

- [1]
  A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney, et al. (2024)
  Openai o1 system card.
  arXiv preprint arXiv:2412.16720.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report").
- [2]
  D. Guo, D. Yang, H. Zhang, J. Song, P. Wang, Q. Zhu, R. Xu, R. Zhang, S. Ma, X. Bi, et al. (2025)
  Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report").
- [3]
  J. Xu, Z. Guo, H. Hu, Y. Chu, X. Wang, J. He, Y. Wang, X. Shi, T. He, X. Zhu, et al. (2025)
  Qwen3-omni technical report.
  arXiv preprint arXiv:2509.17765.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report").
- [4]
  D. Zhang, G. Wang, J. Xue, K. Fang, L. Zhao, R. Ma, S. Ren, S. Liu, T. Guo, W. Zhuang, et al. (2025)
  MiMo-audio: audio language models are few-shot learners.
  arXiv preprint arXiv:2512.23808.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report").
- [5]
  B. Wu, C. Yan, C. Hu, C. Yi, C. Feng, F. Tian, F. Shen, G. Yu, H. Zhang, J. Li, et al. (2025)
  Step-audio 2 technical report.
  arXiv preprint arXiv:2507.16632.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report"),
  [§4.1](#S4.SS1.SSS0.Px4.p1.1 "StepEval-Audio-Paralinguistic (Step-SPQA). ‣ 4.1 Benchmarks ‣ 4 Evaluation ‣ Step-Audio-R1.5 Technical Report").
- [6]
  Z. Xie, M. Lin, Z. Liu, P. Wu, S. Yan, and C. Miao (2025)
  Audio-reasoner: improving reasoning capability in large audio language models.
  arXiv preprint arXiv:2503.02318.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report").
- [7]
  A. Rouditchenko, S. Bhati, E. Araujo, S. Thomas, H. Kuehne, R. Feris, and J. Glass (2025)
  Omni-r1: do you really need audio to fine-tune your audio llm?.
  In IEEE Automatic Speech Recognition and Understanding Workshop,
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report").
- [8]
  F. Tian, X. T. Zhang, Y. Zhang, H. Zhang, Y. Li, D. Liu, Y. Deng, D. Wu, J. Chen, L. Zhao, et al. (2025)
  Step-audio-r1 technical report.
  arXiv preprint arXiv:2511.15848.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report").
- [9]
  A. Gosai, T. Vuong, U. Tyagi, S. Li, W. You, M. Bavare, A. Uçar, Z. Fang, B. Jang, B. Liu, and Y. He (2025)
  Audio multichallenge: a multi-turn evaluation of spoken dialogue systems on natural human interaction.
  External Links: 2512.14865,
  [Link](https://arxiv.org/abs/2512.14865)
  Cited by: [§1](#S1.p5.1 "1 Introduction ‣ Step-Audio-R1.5 Technical Report"),
  [§4.1](#S4.SS1.SSS0.Px1.p1.1 "AudioMultiChallenge (Audio MC). ‣ 4.1 Benchmarks ‣ 4 Evaluation ‣ Step-Audio-R1.5 Technical Report").
- [10]
  Y. Chu, J. Xu, Q. Yang, H. Wei, X. Wei, Z. Guo, Y. Leng, Y. Lv, J. He, J. Lin, et al. (2024)
  Qwen2-audio technical report.
  arXiv preprint arXiv:2407.10759.
  Cited by: [§2](#S2.p2.1 "2 Architecture ‣ Step-Audio-R1.5 Technical Report").
- [11]
  T. Dao (2024)
  FlashAttention-2: faster attention with better parallelism and work partitioning.
  In International Conference on Learning Representations (ICLR),
  Cited by: [§2](#S2.p2.1 "2 Architecture ‣ Step-Audio-R1.5 Technical Report").
- [12]
  X. Zhang, Q. Zhang, H. Liu, T. Xiao, X. Qian, B. Ahmed, E. Ambikairajah, H. Li, and J. Epps (2025)
  Mamba in speech: towards an alternative to self-attention.
  IEEE Transactions on Audio, Speech and Language Processing.
  Cited by: [§2](#S2.p2.1 "2 Architecture ‣ Step-Audio-R1.5 Technical Report").
- [13]
  X. Zhang, J. Ma, M. Shahin, B. Ahmed, and J. Epps (2025)
  Rethinking mamba in speech processing by self-supervised models.
  In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),
  pp. 1–5.
  Cited by: [§2](#S2.p2.1 "2 Architecture ‣ Step-Audio-R1.5 Technical Report").
- [14]
  X. Zhang, D. Liu, T. Xiao, C. Xiao, T. Szalay, M. Shahin, B. Ahmed, and J. Epps (2025)
  Auto-landmark: acoustic landmark dataset and open-source toolkit for landmark extraction.
  In Proc. Interspeech 2025,
  pp. 4263–4267.
  Cited by: [§2](#S2.p2.1 "2 Architecture ‣ Step-Audio-R1.5 Technical Report").
- [15]
  Q. Team et al. (2024)
  Qwen2 technical report.
  arXiv preprint arXiv:2407.10671 2 (3).
  Cited by: [§2](#S2.p3.1 "2 Architecture ‣ Step-Audio-R1.5 Technical Report").
- [16]
  D. Wang, J. Wu, J. Li, D. Yang, X. Chen, T. Zhang, and H. Meng (2025)
  MMSU: a massive multi-task spoken language understanding and reasoning benchmark.
  arXiv preprint arXiv:2506.04779.
  Cited by: [§4.1](#S4.SS1.SSS0.Px5.p1.1 "Additional Public Benchmarks. ‣ 4.1 Benchmarks ‣ 4 Evaluation ‣ Step-Audio-R1.5 Technical Report").
- [17]
  S. Sakshi, U. Tyagi, S. Kumar, A. Seth, R. Selvakumar, O. Nieto, R. Duraiswami, S. Ghosh, and D. Manocha (2024)
  Mmau: a massive multi-task audio understanding and reasoning benchmark.
  arXiv preprint arXiv:2410.19168.
  Cited by: [§4.1](#S4.SS1.SSS0.Px5.p1.1 "Additional Public Benchmarks. ‣ 4.1 Benchmarks ‣ 4 Evaluation ‣ Step-Audio-R1.5 Technical Report").
- [18]
  C. Wei, B. Wang, J. Kim, and N. F. Chen (2025)
  Towards spoken mathematical reasoning: benchmarking speech-based models over multi-faceted math problems.
  arXiv preprint arXiv:2505.15000.
  Cited by: [§4.1](#S4.SS1.SSS0.Px5.p1.1 "Additional Public Benchmarks. ‣ 4.1 Benchmarks ‣ 4 Evaluation ‣ Step-Audio-R1.5 Technical Report").
- [19]
  Q. Team (2026)
  Qwen3. 5-omni technical report.
  arXiv preprint arXiv:2604.15804.
  Cited by: [§4.2](#S4.SS2.p1.1 "4.2 Experimental Results ‣ 4 Evaluation ‣ Step-Audio-R1.5 Technical Report").

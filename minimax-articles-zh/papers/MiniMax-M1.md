---
title: "MiniMax-M1：以闪电注意力高效扩展测试时计算"
title_en: "MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention"
arxiv: 2506.13585
date: 2025-06-16
source: https://arxiv.org/abs/2506.13585
crawled: 2026-09-22
translated: 2026-09-22
---

# MiniMax-M1：以闪电注意力高效扩展测试时计算

> 原文：[MiniMax-M1](https://arxiv.org/abs/2506.13585) · MiniMax arXiv

MiniMax
注：请将通讯事宜发送至 model@minimax.io。

###### 摘要

我们推出 MiniMax-M1，这是全球首个开放权重的大规模混合注意力推理模型。MiniMax-M1 由混合专家（Mixture-of-Experts，MoE）架构与闪电注意力（lightning attention）机制驱动。该模型基于我们此前的 MiniMax-Text-01 模型（[MiniMax et al., 2025](#bib.bib36)）开发，总参数量为 4560 亿，每 token 激活 459 亿参数。M1 模型原生支持 100 万 token 的上下文长度，是 DeepSeek R1 上下文长度的 8 倍。此外，MiniMax-M1 中的闪电注意力机制能够高效扩展测试时计算——例如，在 100K token 生成长度下，M1 相比 DeepSeek R1 仅消耗 25% 的 FLOPs。这些特性使 M1 尤其适合需要处理长输入并进行深度思考的复杂任务。
MiniMax-M1 采用大规模强化学习（RL）训练，训练问题覆盖面广，从传统数学推理到基于沙盒的真实软件工程环境。
除了闪电注意力在 RL 训练中的固有效率优势外，我们还提出了 CISPO，一种全新的 RL 算法，用于进一步提升 RL 效率。CISPO 截断的是重要性采样权重而非 token 更新，其表现优于其他有竞争力的 RL 变体。
混合注意力与 CISPO 相结合，使 MiniMax-M1 的完整 RL 训练在 512 块 H800 GPU 上仅用三周即告完成，租用成本仅为 534,700 美元。
我们发布了两个版本的 MiniMax-M1 模型，思考预算分别为 40K 和 80K，其中 40K 模型代表 80K 训练过程中的一个中间阶段。
在标准基准测试上的实验表明，我们的模型与 DeepSeek-R1 原版、Qwen3-235B 等强大的开放权重模型相当或更优，在复杂软件工程、工具使用和长上下文任务方面优势尤为突出。
通过高效扩展测试时计算，MiniMax-M1 为下一代语言模型智能体推理并应对真实世界挑战奠定了坚实基础。我们在 <https://github.com/MiniMax-AI/MiniMax-M1> 公开发布 MiniMax-M1。

图 1：左：领先商业模型与开放权重模型在竞赛级数学、编程、软件工程、智能体工具使用以及长上下文理解任务上的基准性能对比。此处 MiniMax-M1 采用 MiniMax-M1-80k 模型。
右：推理 FLOPs 随生成长度（token 数）变化的理论扩展曲线。

## 1 引言

大型推理模型（LRM），如 OpenAI o1（[OpenAI, 2024a](#bib.bib38)）和 DeepSeek-R1（[DeepSeek-AI et al., 2025](#bib.bib11)），通过大规模强化学习（RL）延长推理长度，取得了显著成功。近几个月来，开源社区和商业机构纷纷跟进这一趋势，在奥林匹克数学竞赛、竞赛编程等复杂任务上取得重大进展（[Kimi Team, 2025](#bib.bib28)；[Anthropic, 2025](#bib.bib1)；[Google DeepMind, 2025](#bib.bib14)；[Seed et al., 2025](#bib.bib59)；[Zeng et al., 2025](#bib.bib84)；[Yu et al., 2025](#bib.bib81)；[Hu et al., 2025](#bib.bib23)）。
LRM 的成功主要归因于测试时计算这一全新的扩展维度——随着生成阶段投入更多 FLOPs 用于延展推理过程，模型性能持续提升，在复杂的真实世界应用中尤为明显（[OpenAI, 2025](#bib.bib40)；[Jimenez et al., 2024](#bib.bib26)）。

然而，在传统 transformer 架构（[Vaswani et al., 2017](#bib.bib70)）内持续延展推理过程颇具挑战，原因在于 softmax 注意力机制固有的二次方计算复杂度。尽管此前的工作已提出多种缓解该问题的技术——例如稀疏注意力（[Beltagy et al., 2020](#bib.bib5)；[Zaheer et al., 2020](#bib.bib83)；[Lu et al., 2025](#bib.bib34)；[Yuan et al., 2025](#bib.bib82)）、线性注意力（[Katharopoulos et al., 2020](#bib.bib27)；[Qin et al., 2021](#bib.bib47)；[Choromanski et al., 2021](#bib.bib6)；[Peng et al., 2021](#bib.bib45)；[Sun et al., 2023](#bib.bib68)；[Qin et al., 2022a](#bib.bib48)；[Qin et al., 2022b](#bib.bib49)；[Qin et al., 2024a](#bib.bib51)；[Qin et al., 2024c](#bib.bib53)；[Peng et al., 2024b](#bib.bib43)；[Sun et al., 2025](#bib.bib66)；[Shen et al., 2024](#bib.bib61)；[Arora et al., 2024](#bib.bib2)；[Zhang et al., 2024](#bib.bib85)；[Du et al., 2025](#bib.bib12)；[He et al., 2024](#bib.bib20)）、带 delta 衰减的线性注意力（[Yang et al., 2024b](#bib.bib79)；[Yang et al., 2024a](#bib.bib78)；[Peng et al., 2025](#bib.bib44)）、状态空间模型（[Gu et al., 2020](#bib.bib16)；[Gu et al., 2023](#bib.bib18)；[Gu et al., 2022](#bib.bib17)；[Gu and Dao, 2024](#bib.bib15)；[Dao and Gu, 2024](#bib.bib10)；[Glorioso et al., 2024](#bib.bib13)；[Ren et al., 2024](#bib.bib57)；[Jamba Team, 2024](#bib.bib25)；[Gupta et al., 2022](#bib.bib19)）以及线性 RNN（[Hochreiter and Schmidhuber, 1997](#bib.bib22)；[Martin and Cundy, 2018](#bib.bib35)；[Chung and Ç, 2014](#bib.bib8)；[Qin et al., 2023](#bib.bib50)；[Peng et al., 2023](#bib.bib41)；[Peng et al., 2024a](#bib.bib42)；[Qin et al., 2024d](#bib.bib54)；[Chou et al., 2024](#bib.bib7)；[Siems et al., 2025](#bib.bib64)；[Sun et al., 2024](#bib.bib67)；[von Oswald et al., 2025](#bib.bib71)；[Behrouz et al., 2024](#bib.bib4)）——这些方法尚未在大规模推理模型中得到充分验证，迄今几乎所有有竞争力的 LRM 仍依赖传统注意力设计。一个例外是采用 Mamba 架构（[Gu and Dao, 2024](#bib.bib15)；[Dao and Gu, 2024](#bib.bib10)）的 Hunyuan-T1 模型（[Tencent AI Lab, 2025](#bib.bib69)）。然而该模型并未开源，披露的细节也寥寥无几。
在本工作中，我们旨在构建并开源一个能够高效扩展测试时计算、并与最先进推理模型一较高下的大型推理模型。

我们推出 MiniMax-M1，一个采用混合专家（MoE）架构与闪电注意力（Lightning Attention）（[Qin et al., 2024b](#bib.bib52)）的推理模型，后者是线性注意力变体（[Qin et al., 2022a](#bib.bib48)）的一种 I/O 感知实现。MiniMax-M1 基于我们此前的 MiniMax-Text-01（[MiniMax et al., 2025](#bib.bib36)）模型开发，总参数量 4560 亿，激活参数 459 亿，专家数 32。在我们的注意力设计中，每七个采用闪电注意力的 transnormer 块（[Qin et al., 2022a](#bib.bib48)）之后跟随一个采用 softmax 注意力的 transformer 块。如图 [1](#S0.F1)（右）所示，这一设计在理论上支持将推理长度高效扩展到数十万 token。例如，在 64K token 生成长度下，M1 相比 DeepSeek R1 消耗的 FLOPs 不到 50%；在 100K 长度下约为 25%。计算成本的大幅降低使 M1 在推理和大规模 RL 训练期间都显著更高效。此外，凭借闪电注意力机制并承袭 MiniMax-Text-01 的特性，我们的 M1 模型原生支持高达 100 万 token 的上下文长度——是 DeepSeek R1 上下文长度的八倍，比迄今所有开放权重 LRM 高出一个数量级。这些特性使 M1 尤其适合应对需要处理长输入并生成延展思考的复杂真实世界任务。M1 与其他领先模型的最大输入、输出长度对比见表 [1](#S1.T1)。

表 1：不同推理模型支持的最大输入长度与输出长度（token 数）。Claude-4 指 Claude-4-Opus 模型。“DS-R1”指最新的 DeepSeek-R1-0528 模型。

|  | o3 | Gemini 2.5 Pro | Claude 4 | DS-R1 | Qwen3-235B | MiniMax-M1-80k |
| --- | --- | --- | --- | --- | --- | --- |
| 最大输入 | 200K | 1M | 200K | 128K | 128K | 1M |
| 最大输出 | 100K | 64K | 32K | 64K | 32K | 80K |

为了开发 M1 模型，我们首先在一个精心筛选、推理密集的语料库上对 MiniMax-Text-01 追加预训练 7.5T token。随后，我们进行监督微调（SFT）以注入特定的思维链（CoT）（[Wei et al., 2022](#bib.bib74)）模式，为强化学习——M1 开发的核心阶段——奠定坚实基础。
值得注意的是，我们对 M1 的 RL 扩展之所以高效，源于两个关键层面的创新：(1) 我们提出了一种全新的 RL 算法 CISPO，它放弃了信任域约束，转而截断重要性采样权重以稳定训练。该方法始终利用全部 token 进行梯度计算，在实证中取得了相比 GRPO（[Shao et al., 2024](#bib.bib60)）和 DAPO（[Yu et al., 2025](#bib.bib81)）更高的效率——例如，在基于 Qwen2.5-32B 模型（[Qwen et al., 2025](#bib.bib55)）的对照研究中，CISPO 相比 DAPO 实现了 2 倍加速；(2) 尽管 M1 的混合注意力设计天然支持高效的 RL 扩展，但在此架构上扩展 RL 时会出现独特的挑战。例如，我们发现该架构的训练核与推理核之间存在精度失配，阻碍了 RL 训练期间的奖励增长。我们开发了解决这些挑战的针对性方案，并成功在该混合架构上扩展了 RL。
最终，我们高效的 RL 框架使我们能够在 512 块 H800 GPU 上三周内完成 MiniMax-M1 的一次完整 RL 训练——相当于约 53 万美元（$0.53M）的租用成本。

除方法论创新外，我们还为 RL 训练精选了多样的问题与环境集合。我们的数据同时涵盖可验证与不可验证的问题。对于通常被认为对推理学习至关重要的可验证问题，我们不仅纳入相关工作常用的数学推理和竞赛编程问题，还利用我们此前的数据合成框架 SynLogic（[Liu et al., 2025a](#bib.bib30)）生成了覆盖 41 个不同任务的多样化逻辑推理问题。此外，我们基于 SWE-bench（[Jimenez et al., 2024](#bib.bib26)）构建了复杂软件工程（SE）环境沙盒，并以执行式奖励对真实世界 SE 问题进行 RL，以提升 M1 在高难度 SE 场景下的表现。我们的不可验证问题覆盖问答、创意写作等广泛领域，采用生成式奖励模型提供反馈。

我们训练了两个版本的 MiniMax-M1 模型，最大生成长度分别为 40K 和 80K token，由此得到 MiniMax-M1-40k 与 MiniMax-M1-80k 两个模型。
MiniMax-M1-80k 在复杂数学与编程任务上优于 MiniMax-M1-40k，进一步印证了扩展测试时计算的收益。如图 [1](#S0.F1)（左）所示，MiniMax-M1 整体上超越了 DeepSeek-R1 原版、Qwen-235B 等此前领先的开放权重模型，在复杂软件工程、工具使用和长上下文任务上优势尤为明显。
与最新的 DeepSeek-R1-0528 模型相比，MiniMax-M1 在数学和编程竞赛上稍逊，但在更贴近现实的工具使用与长上下文场景中取得相当或更优的表现。
值得注意的是，MiniMax-M1 在智能体工具使用基准 TAU-Bench（[Yao et al., 2025](#bib.bib80)）上优于 Gemini 2.5 Pro，并在长上下文理解基准上超越 OpenAI o3 与 Claude 4 Opus。
凭借高效的测试时扩展，我们认为 MiniMax-M1 为下一代语言模型智能体应对真实世界挑战奠定了坚实基础。

为促进该领域的协作与进步，我们已在 GitHub 和 Hugging Face 公开我们的模型。目前 vLLM 与 Transformers 框架均已支持这些模型，详细的部署指南分别见 [vLLM](https://github.com/MiniMax-AI/MiniMax-M1/blob/main/docs/vllm_deployment_guide.md) 与 [Transformers](https://github.com/MiniMax-AI/MiniMax-M1/blob/main/docs/transformers_deployment_guide.md)。这使得 MiniMax-M1 可以便捷地集成到现代推理管线中。我们还在 [minimax.io](https://minimax.io) 提供商业化标准 API。

## 2 可扩展 RL 的准备：持续预训练与 SFT

在本工作中，我们聚焦于通过扩展强化学习来增强 Minimax-Text-01 的推理能力。为支持可扩展的 RL 训练，我们首先对基础模型进行持续预训练，以强化其内在推理能力。随后，我们进行冷启动监督微调（SFT）阶段，向模型注入特定推理模式，从而为后续 RL 阶段提供更坚实的基础。

### 2.1 持续预训练：RL 扩展的基础

为了在保证多样性的同时增强基础模型的推理与长上下文能力，我们以更优的数据质量与配比对 MiniMax-Text-01 模型追加训练 7.5T token。

训练数据。
我们改进了预训练的网页与 PDF 解析机制，并强化了启发式清洗规则，以确保数学与代码相关数据的高召回率。我们优先从网页、论坛、教科书等多种来源提取自然的问答（QA）对，并严格避免使用合成数据。此外，我们对 QA 数据进行语义去重以保持其多样性与独特性。同时，我们将 STEM（科学、技术、工程、数学）、代码、书籍与推理相关数据的比例提升至 70%。这在显著增强基础模型处理复杂任务能力的同时，不损害其他通用能力。

训练配方。
我们降低了 MoE 辅助损失的系数，并调整并行训练策略以支持更大的训练 micro batch size，从而缓解辅助损失对模型整体性能的不利影响。在 MiniMax-Text-01 的基础上，我们先以 8e-5 的恒定学习率继续训练 2.5T token，随后在 5T token 上按衰减计划将学习率降至 8e-6。

长上下文扩展。
对于收敛复杂度更高的混合闪电架构模型，我们观察到过度激进的训练长度扩展可能导致训练过程中突发梯度爆炸，使优化过程极其困难。我们将此归因于较前层参数的优化跟不上较后层的变化——对闪电注意力而言，较前层与较后层具有不同的衰减率，这使较前层更关注局部信息。我们通过四个阶段渐进、平滑地扩展上下文长度来缓解该问题，从 32K 上下文窗口长度起步，最终将训练上下文扩展至 1M token。

### 2.2 监督微调：面向高效 RL 的聚焦对齐

持续预训练之后，我们进行监督微调（SFT），借助高质量样本灌输基于反思的思维链（CoT）等期望行为，为下一阶段更高效、更稳定的 RL 创造强有力的起点。具体而言，我们精选了带长 CoT 回复的数据样本。这些样本覆盖数学、编程、STEM、写作、问答与多轮对话等多个领域。数学与编程样本约占全部数据的 60%。

## 3 高效 RL 扩展：算法与闪电注意力

如图 [1](#S0.F1)（右）所示，M1 架构在推理期间展现出明确的效率优势。这天然有利于响应越来越长的高效 RL 扩展。然而，作为以该混合架构扩展 RL 的先行者，我们在过程中遭遇了独特的挑战，RL 流程可能因各种问题而变得不稳定甚至失败。
为克服这些困难，我们开发了针对性的解决方案，使 M1 的 RL 训练得以成功扩大规模。此外，我们提出了一种新的 RL 算法，相比现有方法实现了更高的 RL 效率。
这双重贡献构成了一个训练 M1 的高效、可扩展 RL 框架，完整训练周期在 512 块 H800 GPU 上仅需三周——相当于约 53 万美元（$0.53M）的租用成本。
在本节中，我们首先介绍 RL 的一般背景并提出我们的新 RL 算法，然后描述混合架构带来的具体挑战，以及我们为克服它们而设计的方案。

### 3.1 以 CISPO 实现高效 RL 扩展

背景。
对于来自数据集 $\mathcal{D}$ 的问题 $q$，我们将 $\pi$ 记为由 $\theta$ 参数化的策略模型，$o$ 记为由策略生成的回复。
PPO（[Schulman et al., 2017](#bib.bib58)）采用以下目标来优化策略以最大化期望回报，并施加截断操作以稳定训练：

$$
\mathcal{J}_{\text{PPO}}(\theta)=\mathbb{E}_{q\sim\mathcal{D},o_{i}\sim\pi_{\theta_{\text{old}}}(\cdot|q)}\left[\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\min\left(r_{i,t}(\theta)\hat{A}_{i,t},\text{clip}\big(r_{i,t}(\theta),1-\epsilon,1+\epsilon\big)\hat{A}_{i,t}\right)-\beta D_{KL}(\pi_{\theta}||\pi_{\text{ref}})\right], \tag{1}
$$

其中 $r_{i,t}(\theta)=\frac{\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t}\mid q,o_{i,<t})}$ 是重要性采样（IS）权重，用于在离策略（off-policy）更新时校正分布，因为我们使用 $\pi_{\theta_{\text{old}}}$ 采集轨迹，并以 minibatch 方式经多步更新策略。PPO 需要一个独立的价值模型来计算优势 $\hat{A}_{i,t}$，而 GRPO（[Shao et al., 2024](#bib.bib60)）去掉了价值模型，将优势定义为输出奖励相对于组内其他回复的相对值：

$$
\hat{A}_{i,t}=\frac{R_{i}-\text{mean}(\{R_{j}\}_{j=1}^{G})}{\text{std}(\{R_{j}\}_{j=1}^{G})}, \tag{2}
$$

其中 $R_{i}$ 是回复的奖励，每个问题采样 $G$ 个回复 $\{o_{i}\}^{G}_{i=1}$。奖励或来自数学解题这类基于规则的验证器，或来自奖励模型。

token 截断的问题。
在混合架构 zero-RL 设定下的初步实验中，我们观察到 GRPO 算法损害了训练性能，未能有效促进长 CoT 推理行为的涌现。通过一系列对照消融研究，我们最终确认原始 PPO/GRPO 损失中不合需要的截断操作是学习性能退化的主要因素。
具体而言，我们发现与反思行为相关的 token（如 However、Recheck、Wait、Aha），它们往往充当推理路径的“分叉点”，在基础模型中通常罕见且被赋予低概率。在策略更新期间，这些 token 很可能表现出很高的 $r_{i,t}$ 值。结果是，这些 token 在第一次同策略（on-policy）更新后即被截断出局，无法为后续的离策略梯度更新作出贡献。该问题在我们的混合架构模型中尤为突出，进一步阻碍了强化学习的可扩展性。
然而这些低概率 token 往往对稳定熵（[Cui et al., 2025](#bib.bib9)）和促进可扩展 RL（[Wang et al., 2025](#bib.bib72)）至关重要。尽管 DAPO 尝试通过提高截断上界来缓解该问题（[Yu et al., 2025](#bib.bib81)），我们发现在我们的设定下——每个生成批次进行 16 轮离策略更新——该方法效果有限。

图 2：基于 Qwen2.5-32B-base，在 AIME 2024 上对比 GRPO、DAPO 与我们提出的 CISPO。在相同训练步数下，CISPO 的性能优于 GRPO 与 DAPO，并且仅用 50% 的训练步数即可达到与 DAPO 相当的性能。

CISPO 算法。
有鉴于此，我们提出一种明确避免丢弃 token 的新算法——即使是对应大更新的 token 也不丢弃——同时天然地将熵维持在合理范围内以确保稳定探索。首先回顾带有分布校正的离线更新 vanilla REINFORCE 目标：

$$
\mathcal{J}_{\text{REINFORCE}}(\theta)=\mathbb{E}_{(q,a)\sim\mathcal{D},o_{i}\sim\pi_{\theta_{\text{old}}}(\cdot|q)}\left[\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\texttt{sg}(r_{i,t}(\theta))\hat{A}_{i,t}\log\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})\right], \tag{3}
$$

其中 $\texttt{sg}(\cdot)$ 表示停止梯度（stop-gradient）操作。
我们不像 PPO/GRPO 那样截断 token 更新，而是截断式 (3)中的重要性采样权重以稳定训练。
我们将该方法命名为 CISPO（Clipped IS-weight Policy Optimization，截断 IS 权重策略优化）。CISPO 采用 GRPO 的组相对优势与 token 级损失（[Yu et al., 2025](#bib.bib81)；[Liu et al., 2025b](#bib.bib32)），优化以下目标：

$$
\mathcal{J}_{\text{CISPO{}}}(\theta)=\mathbb{E}_{(q,a)\sim\mathcal{D},\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot|q)}\left[\frac{1}{\sum_{i=1}^{G}|o_{i}|}\sum_{i=1}^{G}\sum_{t=1}^{|o_{i}|}\texttt{sg}(\hat{r}_{i,t}(\theta))\hat{A}_{i,t}\log\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})\right], \tag{4}
$$

其中 $\hat{r}_{i,t}(\theta)$ 是截断后的 IS 权重：

$$
\hat{r}_{i,t}(\theta)=\text{clip}\left(r_{i,t}(\theta),1-\epsilon^{IS}_{low},1+\epsilon^{IS}_{high}\right). \tag{5}
$$

我们注意到，若不进行权重截断，$\mathcal{J}_{\text{CISPO{}}}$ 就退化为标准策略梯度目标。在实验中，我们没有通过将 $\epsilon^{IS}_{low}$ 设为很大的值来施加 IS 权重下界，而是只调节 $\epsilon^{IS}_{high}$。
尽管式 (4)的梯度因权重截断而略有偏倚，但该方法保留了所有 token 的梯度贡献，在长回复中尤为可贵。
CISPO 在我们的实验中被证明行之有效，有助于降低方差并稳定 RL 训练。
此外，我们采用了 [Yu et al. (2025)](#bib.bib81) 的动态采样与长度惩罚技术。与近期其他工作一样，CISPO 中不含 KL 惩罚项（[Yu et al., 2025](#bib.bib81)；[Hu et al., 2025](#bib.bib23)）。

一般化形式。
虽然我们在实验中采用 CISPO，这里我们进一步通过在 CISPO 目标中引入逐 token 掩码给出一个统一表述。这允许通过超参数调节来控制是否以及在何种条件下丢弃特定 token 的梯度：

$$
\mathcal{J}_{\text{unify}}(\theta)=\mathbb{E}_{(q,a)\sim\mathcal{D},\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot|q)}\left[\frac{1}{\sum_{i=1}^{G}|o_{i}|}\sum_{i=1}^{G}\sum_{t=1}^{|o_{i}|}\texttt{sg}(\hat{r}_{i,t}(\theta))\hat{A}_{i,t}\log\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})M_{i,t}\right]. \tag{6}
$$

掩码 $M_{i,t}$ 等价于 PPO 信任域中隐式定义的掩码：

$$
M_{i,t}=\begin{cases}0&\text{if }\hat{A}_{i,t}>0\text{ and }r_{i,t}(\theta)>1+\epsilon_{\text{high}},\\ 0&\text{if }\hat{A}_{i,t}<0\text{ and }r_{i,t}(\theta)<1-\epsilon_{\text{low}},\\ 1&\text{otherwise}.\end{cases} \tag{7}
$$

这一统一的损失表述可以在共同框架下灵活表示不同的截断策略。

CISPO 的实证验证。
为了验证 CISPO 的有效性，我们在 zero-RL 训练设定下将其与 DAPO 和 GRPO 进行实证比较。具体而言，我们在 [Yu et al. (2025)](#bib.bib81) 的数学推理数据集上应用不同 RL 算法训练 Qwen2.5-32B-base 模型，并汇报 AIME 2024 基准上的性能。如图 [2](#S3.F2) 所示，在相同训练步数下，CISPO 显著优于 DAPO 与 GRPO。值得注意的是，CISPO 展现出优于其他方法的训练效率；例如，它仅用 50% 的训练步数即可匹敌 DAPO 的性能。

### 3.2 以闪电注意力实现高效 RL 扩展——挑战与经验

![参见正文](2506.13585v1/precision_comparison.png)

![参见正文](2506.13585v1/precision_comparison_v2.png)

图 3：训练模式代码中 token 的概率对比推理模式代码中 token 的概率。图中每个点代表一个单独的 token。图中标注了 Pearson 相关系数。理论上，这两个概率应当完全一致，所有 token 都应恰好落在对角线上。
左：修复前 M1 模型的相关性；右：对 M1 模型应用“LM 输出头使用 FP32 精度”的修复之后的相关性。

如图 [1](#S0.F1)（右）所示，我们强调，由于 rollout 的计算与延迟往往是 RL 训练的主要瓶颈，我们的混合注意力相比传统注意力设计天然支持更高效的 RL 扩展。然而，作为以这一新架构开展大规模 RL 实验的先行者，我们遭遇了独特的挑战并制定了针对性方案，下面逐一描述。

生成与训练之间的计算精度失配。
RL 训练对计算精度高度敏感。
在 RL 训练期间，我们观察到 rollout token 的概率在训练模式与推理模式之间存在显著差异，如图 [3](#S3.F3)（左）所示。这一差异源于训练核与推理核之间的精度失配。该问题危害极大，在我们的实验中阻碍了奖励增长。
有趣的是，该问题并未在采用 softmax 注意力的较小稠密模型中出现。
通过逐层分析，我们定位到输出层 LM head 中高幅值的激活是误差的主要来源。为解决这一问题，我们将 LM 输出头的精度提升至 FP32，从而重新对齐这两个理论上应相同的概率，如图 [3](#S3.F3)（右）所示。这一调整将训练与推理概率之间的相关性从约 0.9x 提升到 0.99x。值得注意的是，该相关性指标在整个训练过程中保持稳定，使奖励得以成功增长。

优化器超参数敏感性。
我们使用 AdamW（[Loshchilov and Hutter, 2019](#bib.bib33)）优化器，$\beta_{1}$、$\beta_{2}$ 与 $\epsilon$ 的不当配置可能导致训练不收敛（[Molybog et al., 2023](#bib.bib37)）。例如，采用 VeRL（[Sheng et al., 2024](#bib.bib62)）的默认配置——betas = (0.9, 0.999)、eps = 1e-8——就可能出现此类问题。
我们观察到，MiniMax-M1 训练中的梯度幅值跨越很宽的范围，从 1e-18 到 1e-5，且大多数梯度小于 1e-14。此外，相邻迭代梯度之间的相关性很弱。基于此，我们设置 $\beta_{1}=0.9$、$\beta_{2}=0.95$、eps=1e-15。

基于重复检测的提前截断。
在 RL 训练中，我们发现复杂提示可能诱发病态的冗长且重复的回复，其巨大的梯度威胁模型稳定性。我们的目标是抢先终止这类生成循环，而非惩罚已经重复的文本。由于简单的字符串匹配对多样化的重复模式无效，我们开发了一种基于 token 概率的启发式方法。我们观察到，一旦模型进入重复循环，每个 token 的概率都会飙升。因此，我们实现了提前截断规则：若 3,000 个连续 token 的概率均高于 0.99，则停止生成。该方法成功防止了模型不稳定，并通过消除这类病态的长尾情况提升了生成吞吐。

## 4 以多样化数据扩展强化学习

在本节中，我们描述 RL 阶段采用的数据与奖励。我们在 RL 训练管线中纳入了多样的环境集合，既包括可以通过规则验证的任务，也包括需要通过奖励模型验证的通用任务。
所有这些环境都通过精心设计的课程（curriculum）集成到 RL 阶段。

### 4.1 基于规则验证的推理密集任务

下面介绍我们能够以确定性规则验证的数据。对于以下所有任务，我们采用基于规则的最终正确性作为正确性奖励，并辅以格式奖励。

数学推理。
我们最初的数学数据集包含数十万道高质量的竞赛级题目，从公开来源与官方数学竞赛中精心筛选整理而成。这些题目难度跨度大，每道题均配有标准参考答案。
我们的数据清洗流程首先移除不完整样本以及存在格式或排版错误的样本。随后，我们在各 RL 数据源之间进行基于嵌入的去重，并与 SFT 数据集严格隔离以避免重叠，因为 SFT 阶段向 RL 阶段的泄漏会阻碍探索并损害训练效果。此外，我们同时采用 n-gram 与基于嵌入的方法，消除与常用数学基准测试集的潜在污染，从而确保评测的完整性与公平性。
我们滤除包含多个子问题的样本、证明题以及容易随机猜测命中的是非题（如判断题）。选择题被改写为开放式格式，以更好地契合我们的强化学习框架。
接着，我们利用内部模型从参考答案中提取最终答案，仅保留提取答案能被我们基于规则的答案校验器正确解析的样本。最后，我们使用一个强推理模型计算每道题的 pass@10，仅保留通过率严格介于 0 到 0.9 之间的样本，最终为 RL 训练精选出近 5 万道高质量数学样本。

逻辑推理。
在逻辑推理数据方面，我们精心挑选了 41 个需要不平凡推理能力的逻辑推理任务（如密码破译与数独），随后实现数据合成框架来合成全部数据。具体而言，我们利用 SynLogic 框架（[Liu et al., 2025a](#bib.bib30)）实现具备任务专属数据生成器与基于规则的任务专属验证器的数据合成管线，从而自动生成逻辑数据。我们在生成过程中细致配置难度参数，确保生成数据具有恰当的学习挑战性。具体来说，为防止包含过于困难的实例，我们依据当前强推理模型的可解性上限设定难度上界，要求其 pass@10 大于零。类似地，我们以 MiniMax-Text-01 模型通过率介于 0 到 0.5 的最低难度参数设定难度下界。这一做法确保数据在难度与可学习性之间保持平衡。此外，随着模型能力在训练中提升，我们在后期阶段提高数据难度。借助该框架，我们为 RL 训练合成了约 5.3 万个逻辑推理样本。

竞赛编程。
在竞赛编程问题方面，我们从在线评测平台与热门编程网站收集公开题目。对于缺少测试用例的题目，我们开发了基于 LLM 的工作流，并使用 MiniMax-Text-01 模型生成全面的测试套件。与数学推理数据集的做法类似，我们基于模型采样的通过率对题目进行质量与难度筛选，保留难度适中且高质量的算法题。通过这一流程，我们为 RL 训练生成了 3 万个竞赛编程数据样本。

软件工程。
在软件工程领域，受 SWE-bench（[Jimenez et al., 2024](#bib.bib26)）启发，我们利用来自公开 GitHub 仓库的真实数据构建可验证的强化学习环境。我们的数据集主要包含体现常见软件开发挑战的 issue 与拉取请求（PR），涵盖缺陷定位、代码修复与测试用例合成。
为支持有效的强化学习，我们开发了精细的容器化沙盒环境，模拟真实的软件开发工作流。该环境能够实际执行代码，对智能体所提改动的正确性与有效性提供直接可验证的反馈。预定义或新生成的测试用例的通过/失败状态是我们 RL 框架的主要奖励信号。通过全部相关测试用例的成功执行产生正奖励，而编译错误、运行时失败或测试用例回归则产生零或负奖励，从而为策略优化提供清晰信号。
通过这一流程，我们精选了数千个高质量数据样本。每个样本包含问题描述（如来自 issue 的缺陷报告）、初始错误代码以及一组相关测试用例。这一设置使我们的 RL 智能体学会精准定位缺陷、提出正确的代码修复，甚至合成新的有效测试用例，其表现可通过沙盒环境内的执行直接验证。

### 4.2 基于模型反馈的通用领域任务

在本节中，我们进一步将 RL 范围扩展到更广泛的通用领域任务。由于这些任务难以通过规则验证，我们使用奖励模型提供反馈。

#### 4.2.1 数据与奖励模型

我们的通用 RL 数据集共包含 2.5 万个复杂样本。它们大致可分为两类：具有可验证但难以用规则校验的标准答案的样本，以及没有标准答案的样本。

有标准答案的任务。此类任务主要包括 STEM 及其他事实性问题，其答案客观但可能存在多种有效表达形式。这种多样性常使基于规则的答案校验器失准。我们的数据清洗流程与数学推理类似，但使用我们的生成式奖励模型（GenRM）作为验证器，而非依赖基于规则的校验器。
为评估标准答案与模型回复之间的一致性，我们采用五档奖励尺度来评估这两个组成部分。首先，我们构建了人工标注的奖励模型基准，覆盖跨知识与任务域的一系列客观任务，尤其是基于规则的校验器无法准确判定的“模型回复–标准答案”配对。其次，我们通过比较 GenRM 选出的 Best-of-N（BoN）回复与各基准上的 pass@N 指标来评估 GenRM 的有效性。GenRM 的性能以其在人工标注基准上的准确率以及 BoN 与 pass@N 之间的性能差距来衡量。这些指标指导我们优化 GenRM 训练期间的数据分布与提示词设计。

无标准答案的任务。此类任务涵盖范围更广，包括指令遵循、创意写作等。
提示词基于我们的内部标签体系从大池中采样，确保在细粒度领域之间保持均衡的训练分布。
尽管这些查询通常是开放式的、没有标准答案，我们仍力求为每个查询配对一个参考答案，作为奖励模型评判的参照。为此，我们首先由多个内部与外部模型生成回复，随后这些参考答案将经过我们的内部质量评估。
在 RL 训练期间，我们采用成对比较框架来评估模型回复。每次比较产生 -1、0 或 1 的分数，表示模型输出劣于、近似于或优于参考答案。尤其是对于带约束的指令遵循任务，我们同时使用基于规则的奖励来评估回复是否满足约束，并用基于模型的奖励评估回复质量。与有标准答案的设定一样，我们先构建人工标注基准，纳入来自可靠标注者的多盲偏好判断。随后我们打磨评分标准与偏好提示词，以优化准确性并控制下文 §[4.2.2](#S4.SS2.SSS2) 将提及的潜在偏倚。为最小化潜在偏倚，训练数据也通过多种方法优化，如多盲一致判断、位置互换一致判断等。一旦训练出最优 GenRM，便在训练数据集上执行瑞士轮（Swiss Round）评分体系，为 RL 训练确定最合适的参考答案。

#### 4.2.2 应对生成式奖励模型在长 CoT 上的偏倚

面向复杂 CoT 推理任务的有效通用 RL，关键依赖于准确且无偏的奖励模型。评估此类 CoT 回答颇具挑战，我们发现 GenRM 偏好更长的输出，而非可能更优的简洁替代方案，且与实际推理质量无关。这种长度偏倚问题严重，因为它可能严重误导 RL 策略优化，激励冗长而无实质内容的输出，并诱发奖励黑客（reward hacking）。
我们改进 GenRM 保真度的初步工作包括标准的离线策略：(1) 使训练数据在回复长度、来源与质量层级上更加多样；(2) 纳入对抗样本以暴露薄弱点；(3) 改进模型架构。然而，实证分析表明，纯离线评估与对长度偏倚的预防式缓解，常常无法阻止 RL 训练期间出现长度偏倚。

因此，我们的核心策略是在 RL 训练期间对长度偏倚进行持续的在线监控。我们建立了具体指标，用于检测 RL 策略是否在不提升任务成功率或推理深度的情况下不成比例地拉长输出以最大化 GenRM 奖励。一旦检测到这种表明利用 GenRM 长度偏倚的有害“逐长”行为，便立即触发 GenRM 重校准。这种迭代调整对于先发制人地遏制与输出长度相关的奖励黑客至关重要，可确保策略优先提升实质能力而非表面的文本膨胀。
作为这一自适应方法的补充，我们系统性地采用了奖励塑造（reward shaping）、价值截断与归一化等 RL 侧技术。
这些机制使奖励信号对来自表层特征（如长度）的极端值不再敏感，从而将策略优化引向长 CoT 推理的实质质量与正确性。

### 4.3 融合多样化数据的课程

鉴于我们的 RL 数据横跨广泛的类别，一个核心挑战是训练出单一策略，使其在推理密集任务与通用领域任务上都能出类拔萃。
为此，我们的方法是在使用 CISPO 的 RL 训练过程中，对推理任务与通用领域任务实施精心管理的课程与动态加权策略：我们从仅有基于规则奖励的推理密集任务起步，然后逐渐混入通用领域任务。这确保模型持续打磨其可验证技能（如数学与代码），同时逐步提升其在从复杂指令遵循到开放式 CoT 推理等多样通用任务上的表现。
这种混合 RL 训练促使模型学会依情境运用其推理能力——对可验证问题采用严谨的逐步演绎，对通用查询采用更灵活、自适应的生成——且全部在统一的策略框架内完成。它既防止专业技能的灾难性遗忘，又促进更广泛的泛化。

## 5 将 RL 扩展延伸至更长思考

我们的第一次 RL 训练以 40K token 的输出长度上限进行。鉴于 M1 的混合架构原生支持更长序列的近线性扩展（如图 [1](#S0.F1)（右）所示），我们进一步将 RL 训练期间的生成长度扩展到 80K token。由此得到一个新模型，我们称之为 MiniMax-M1-80k。

数据。
为了以 80K 输出长度高效训练我们的 RL 模型，我们利用此前训练的 40K 模型来指导数据筛选。首先，我们在 §[4](#S4) 所述的精选数据集上评估通过率并移除易于解决的样本。随后，我们调整数据分布以偏向更具挑战性的样本，例如困难的数学与编程题。此外，在观察到合成推理数据会破坏长上下文 RL 训练的稳定性之后，我们对其进行了降采样。具体而言，由该类数据生成的输出往往变得重复且同质，持续暴露于这类模式被证明对模型整体性能有害。

长度扩展策略。为逐步增加输出长度，我们采用分阶段的窗口扩展 RL 策略。我们从 40K 输出长度起步，逐步扩展到 48K、56K、64K、72K，最终达到 80K。这一分阶段方法确保了每一步的训练稳定性。向后续长度的过渡由一组经验指标决定，包括生成序列困惑度的收敛情况，以及输出长度的第 99 百分位数是否逼近当前上下文窗口上限。这些信号为模型是否具备扩展条件提供了有价值的洞察，使我们得以在整个过程中保持稳健的训练。

应对扩展期间的训练不稳定。在扩展过程中，我们在每个长度窗口训练的后期阶段遭遇了一个关键问题。具体而言，模型容易出现模式坍塌（pattern collapse），生成序列的后段退化为不连贯或乱码文本。该现象总是伴随着困惑度上升，表明生成质量与稳定性受损。我们定位了根因：在输出长度延展期间，负样本的长度增速远快于正样本，往往更早触及上下文窗口上限。因此，不成比例的巨大负梯度在生成序列的后段积累。这种失衡源于 GRPO 优势归一化与我们所采用的 token 级损失天然的不对等性。
对此，我们实施了三项关键对策：(1) 检测重复模式（连续高概率 token）并提前停止，防止重复回复过度消耗上下文窗口；(2) 采用样本级损失与 token 级归一化相结合的方式，缓解负-正样本失衡及其不利影响；(3) 降低梯度截断阈值与 $\epsilon^{IS}_{high}$，进一步稳定生成。

## 6 评测

表 2：MiniMax-M1 在核心基准上的性能。

| 任务 | 领先闭源权重模型 | | | | 开放权重模型 | | | 我们的模型 | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | OpenAI-o3 | Gemini 2.5  Pro (06-05) | Claude  4 Opus | Seed-  Thinking-  v1.5 | DeepSeek-  R1 | DeepSeek-  R1-0528 | Qwen3-  235B-A22B | MiniMax-  M1-40k | MiniMax-  M1-80k |
| 扩展思考 | *100K* | *64K* | *64K* | *32K* | *32K* | *64K* | *32K* | *40K* | *80K* |
| *数学* | | | | | | | | | |
| AIME 2024 | 91.6 | 92.0 | 76.0 | 86.7 | 79.8 | 91.4 | 85.7 | 83.3 | 86.0 |
| AIME 2025 | 88.9 | 88.0 | 75.5 | 74.0 | 70.0 | 87.5 | 81.5 | 74.6 | 76.9 |
| MATH-500 | 98.1 | 98.8 | 98.2 | 96.7 | 97.3 | 98.0 | 96.2 | 96.0 | 96.8 |
| *通用编程* | | | | | | | | | |
| LiveCodeBench  *(24/8∼\sim25/5)* | 75.8 | 77.1 | 56.6 | 67.5 | 55.9 | 73.1 | 65.9 | 62.3 | 65.0 |
| FullStackBench | 69.3 | – | 70.3 | 69.9 | 70.1 | 69.4 | 62.9 | 67.6 | 68.3 |
| *推理与知识* | | | | | | | | | |
| GPQA Diamond | 83.3 | 86.4 | 79.6 | 77.3 | 71.5 | 81.0 | 71.1 | 69.2 | 70.0 |
| HLE  *(无工具)* | 20.3 | 21.6 | 10.7 | 8.2 | 8.6∗ | 17.7∗ | 7.6∗ | 7.2∗ | 8.4∗ |
| ZebraLogic | 95.8 | 91.6 | 95.1 | 84.4 | 78.7 | 95.1 | 80.3 | 80.1 | 86.8 |
| MMLU-Pro | 85.0 | 86.0 | 85.0 | 87.0 | 84.0 | 85.0 | 83.0 | 80.6 | 81.1 |
| *软件工程* | | | | | | | | | |
| SWE-bench Verified | 69.1 | 67.2 | 72.5 | 47.0 | 49.2 | 57.6 | 34.4 | 55.6 | 56.0 |
| *长上下文* | | | | | | | | | |
| OpenAI-MRCR   *(128k)* | 56.5 | 76.8 | 48.9 | 54.3 | 35.8 | 51.5 | 27.7 | 76.1 | 73.4 |
| OpenAI-MRCR   *(1M)* | – | 58.8 | – | – | – | – | – | 58.6 | 56.2 |
| LongBench-v2 | 58.8 | 65.0 | 55.6 | 52.5 | 58.3 | 52.1 | 50.1 | 61.0 | 61.5 |
| *智能体工具使用* | | | | | | | | | |
| TAU-bench *(airline)* | 52.0 | 50.0 | 59.6 | 44.0 | – | 53.5 | 34.7 | 60.0 | 62.0 |
| TAU-bench *(retail)* | 73.9 | 67.0 | 81.4 | 55.7 | – | 63.9 | 58.6 | 67.8 | 63.5 |
| *事实性* | | | | | | | | | |
| SimpleQA | 49.4 | 54.0 | – | 12.9 | 30.1 | 27.8 | 11.0 | 17.9 | 18.5 |
| *通用助手* | | | | | | | | | |
| MultiChallenge | 56.5 | 51.8 | 45.8 | 43.0 | 40.7 | 45.0 | 40.0 | 44.7 | 44.7 |
| * 在纯文本 HLE 子集上进行。 | | | | | | | | | |

### 6.1 核心基准

我们从几个关键维度对 MiniMax-M1 进行了全面评测：数学、通用编程、软件工程、推理与知识、长上下文、智能体工具使用、事实性以及通用助手能力。所有任务均使用 temperature 1.0 与 top-p 0.95 采样进行评测。

- •

  数学：为评估数学推理能力，我们采用多个竞赛级数学基准，包括 MATH-500（[Hendrycks et al., 2021](#bib.bib21)）、AIME 2024、AIME 2025。AIME 评测中，我们采样 32 次并计算平均通过率作为最终得分。
- •

  通用编程：我们使用 LiveCodeBench（[Jain et al., 2025](#bib.bib24)）与 FullStackBench（[Liu et al., 2024](#bib.bib31)）评估通用编程能力，二者评估跨多样编程任务的代码生成。对这两个基准，我们汇报 16 次采样的平均通过率。
- •

  推理与知识：我们通过 GPQA-Diamond（[Rein et al., 2024](#bib.bib56)）、MMLU-Pro（[Wang et al., 2024](#bib.bib73)）与高难度 HLE 基准（[Phan et al., 2025](#bib.bib46)）评估领域知识与推理能力。GPQA-Diamond 采样 32 次并汇报平均通过率。
  HLE 评测中，我们在不使用外部工具的情况下评估模型。此外，我们使用 ZebraLogic（[Lin et al., 2025](#bib.bib29)）衡量逻辑推理能力。
- •

  软件工程：我们使用 SWE-bench Verified（[Jimenez et al., 2024](#bib.bib26)）评估软件工程能力，该基准衡量解决真实世界 GitHub issue 的能力。我们汇报基于 Agentless 脚手架（[Xia et al., 2024](#bib.bib76)）的结果。与原始管线不同，我们的方法采用两阶段定位流程（不使用任何基于嵌入的检索机制）：先进行粗粒度文件定位，随后进行到具体文件与代码元素的细粒度定位。
- •

  长上下文：我们使用 OpenAI-MRCR（[OpenAI, 2024b](#bib.bib39)）评估长上下文理解能力，该基准测试在扩展上下文中检索并消歧多个相似条目的能力；同时使用 LongBench-v2（[Bai et al., 2024](#bib.bib3)），这是一个包含 503 道多选题、上下文从 8k 到 2M 词的高难度基准。
- •

  智能体工具使用：我们通过 TAU-bench（[Yao et al., 2025](#bib.bib80)）评估工具使用能力，该基准模拟动态对话，智能体须在遵循领域特定政策指南的同时使用 API 工具。TAU-bench 评测以 GPT-4.1 作为用户模型，采用通用系统提示词11
  1
  ”In each round, you need to carefully examine the tools provided to you to determine if any can be used. You must adhere to all of the policies. Pay attention to the details in the terms. Solutions for most situations can be found within these policies.”（“在每一轮中，你需要仔细检查提供给你的工具，判断是否有可用的工具。你必须遵守所有政策。注意条款中的细节。大多数情况的解决方案都可以在这些政策中找到。”）且不使用任何自定义工具。
  最大交互步数为 40。
- •

  事实性：为衡量 LLM 的事实性，我们使用 SimpleQA（[Wei et al., 2024](#bib.bib75)），这是一个对抗性收集的事实性问答基准，每题只有一个无可争议的答案。
- •

  通用助手：我们使用 MultiChallenge（[Sirdeshmukh et al., 2025](#bib.bib65)）评估通用助手能力，该基准评估 LLM 与人类用户进行拟真多轮对话的表现。我们汇报由 GPT-4o 判定的分数。

数学、编程及其他通用任务上的结果。
表 [2](#S6.T2) 展示了我们的模型与最先进大型推理模型的性能对比。在数学推理方面，MiniMax-M1 模型在多个基准上表现强劲，取得了与闭源权重模型 Seed-Thinking-v1.5（[Seed et al., 2025](#bib.bib59)）相当的成绩。值得注意的是，MiniMax-M1-80k 在 AIME 2024 上取得 86.0%，在开放权重模型中位居第二，仅落后于最新的 DeepSeek-R1-0528 模型。在通用编程方面，MiniMax-M1-80k 在 LiveCodeBench 上与 Qwen3-235B 持平，同时在 FullStackBench 上胜出，展现出领先开放权重模型中的强劲实力。
在推理与知识基准上，MiniMax-M1-80k 同样落后于 DeepSeek-R1-0528，但与其他顶尖开放权重模型相比具备竞争力。
在事实性基准 SimpleQA 上，Minimax-M1 模型不及 DeepSeek-R1，但优于其他所有开放权重模型与 Seed-Thinking-v1.5。
在 MultiChallenge 上，两个 MiniMax 模型的表现与 DeepSeek-R1-0528 和 Claude 4 Opus 相当，仅逊于 o3 与 Gemini-2.5-Pro。

复杂场景中的亮点：软件工程、长上下文与工具使用。
得益于 RL 期间基于执行的软件工程环境，MiniMax-M1-40k 与 MiniMax-M1-80k 在 SWE-bench Verified 上分别取得 55.6% 与 56.0% 的强劲分数。这一成绩略逊于 DeepSeek-R1-0528 的 57.6%，但显著超越其他开放权重模型。
凭借 1M 上下文窗口，M1 模型在长上下文理解方面显著超越所有其他开放权重模型，甚至超过 OpenAI o3 与 Claude 4 Opus，全球排名第二，仅以微弱差距落后于 Gemini 2.5 Pro。
在智能体工具使用场景（TAU-bench）中，MiniMax-M1-40k 超越所有开放权重模型乃至 Gemini-2.5 Pro。
此外，MiniMax-M1-80k 在大多数基准上持续优于 MiniMax-M1-40k，印证了扩展测试时计算的收益。

图 4：MiniMax-M1 的准确率与生成长度随 RL 训练步数的变化。

### 6.2 RL 扩展的效果

为研究 RL 扩展的效果，我们在整个训练过程中跟踪性能与回复长度。图 [4](#S6.F4) 分别展示了来自 AIME 2024、AIME 2025 与 LiveCodeBench v5 的三个代表性例子。
我们观察到训练期间模型性能与回复长度均持续提升。值得注意的是，AIME 与 LiveCodeBench 上的平均回复长度超过 20,000 token，AIME 2024 准确率从 68% 大幅提升到 80%。至关重要的是，这些可视化中准确率提升与回复长度增加之间的强相关性，凸显了延展 RL 扩展以支持更充分推理过程的重要性。

## 7 结论与未来工作

在本工作中，我们推出并发布了 MiniMax-M1，全球首个采用闪电注意力机制的开放权重大规模推理模型。这一高效的注意力设计使 MiniMax-M1 原生支持高达 1M token 的输入与 80K token 的生成长度——二者均显著超越其他开放权重模型的能力。这些能力使 MiniMax-M1 独特地适合需要长上下文与延展推理的复杂、拟真场景，其在软件工程、智能体工具使用与长上下文理解基准上的强劲表现实证了这一点。
除闪电注意力对 RL 训练的固有效率优势外，本工作还贡献了加速训练的全新 RL 算法 CISPO。结合架构优势与 CISPO，我们高效地训练了 MiniMax-M1，完整 RL 训练在 512 块 H800 GPU 上三周内完成。在全面评测中，MiniMax-M1 与 DeepSeek-R1、Qwen3-235B 并列全球最佳开放权重模型之列。

展望未来，随着测试时计算持续扩展以支撑日益复杂的场景，我们预见此类高效架构在应对真实世界挑战方面具有巨大潜力，包括自动化企业工作流（[Xu et al., 2025](#bib.bib77)）与开展科学研究（[Si et al., 2024](#bib.bib63)；[OpenAI, 2025](#bib.bib40)）。真实世界应用尤其需要能够作为智能体与环境、工具、计算机或其他智能体交互的 LRM——要求在数十到数百轮之间持续推理，同时整合来自多元来源的长上下文信息。我们期望 MiniMax-M1 凭借独特优势成为此类应用的坚实基础，并将全力推动 MiniMax-M1 向这一目标持续演进。

## 参考文献

- Anthropic (2025)

  Anthropic.
  Claude 3.7 sonnet and claude code.
  <https://www.anthropic.com/news/claude-3-7-sonnet>, 2025.
  Blog post, February 24, 2025.
- Arora et al. (2024)

  Simran Arora, Sabri Eyuboglu, Michael Zhang, Aman Timalsina, Silas Alberti, Dylan Zinsley, James Zou, Atri Rudra, and Ré.
  Simple linear attention language models balance the recall-throughput tradeoff.
  *arXiv preprint arXiv:2402.18668*, 2024.
- Bai et al. (2024)

  Yushi Bai, Shangqing Tu, Jiajie Zhang, Hao Peng, Xiaozhi Wang, Xin Lv, Shulin Cao, Jiazheng Xu, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li.
  LongBench.
  *arXiv preprint arXiv:2412.15204*, 2024.
- Behrouz et al. (2024)

  Ali Behrouz, Peilin Zhong, and Vahab Mirrokni.
  Titans: Learning to memorize at test time.
  *arXiv preprint arXiv:2501.00663*, 2024.
- Beltagy et al. (2020)

  Iz Beltagy, Matthew E Peters, and Arman Cohan.
  Longformer: The long-document transformer.
  *arXiv preprint arXiv:2004.05150*, 2020.
- Choromanski et al. (2021)

  Krzysztof Marcin Choromanski, Valerii Likhosherstov, David Dohan, Xingyou Song, Andreea Gane, Tamas Sarlos, Peter Hawkins, Jared Quincy Davis, Afroz Mohiuddin, Lukasz Kaiser, David Benjamin Belanger, Lucy J Colwell, and Adrian Weller.
  Rethinking attention with Performers.
  In *International Conference on Learning Representations*, 2021.
  URL <https://openreview.net/forum?id=Ua6zuk0WRH>.
- Chou et al. (2024)

  Yuhong Chou, Man Yao, Kexin Wang, Yuqi Pan, Rui-Jie Zhu, Jibin Wu, Yiran Zhong, Yu Qiao, Bo Xu, and Guoqi Li.
  Metala: Unified optimal linear approximation to softmax attention map.
  *Advances in Neural Information Processing Systems*, 37:71034–71067, 2024.
- Chung and Ç (2014)

  Junyoung Chung and Ç.
  Empirical evaluation of gated recurrent neural networks on sequence modeling.
  *arXiv preprint arXiv:1412.3555*, 2014.
- Cui et al. (2025)

  Ganqu Cui, Yuchen Zhang, Jiacheng Chen, Lifan Yuan, Zhi Wang, Yuxin Zuo, Haozhan Li, Yuchen Fan, Huayu Chen, Weize Chen, Zhiyuan Liu, Hao Peng, Lei Bai, Wanli Ouyang, Yu Cheng, Bowen Zhou, and Ning Ding.
  The entropy mechanism of reinforcement learning for reasoning language models.
  *arXiv preprint arXiv:2505.22617*, 2025.
- Dao and Gu (2024)

  Tri Dao and Albert Gu.
  Transformers are ssms: Generalized models and efficient algorithms through structured state space duality.
  *arXiv preprint arXiv:2405.21060*, 2024.
- DeepSeek-AI et al. (2025)

  DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, et al.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
  *arXiv preprint arXiv:2501.12948*, 2025.
- Du et al. (2025)

  Jusen Du, Weigao Sun, Disen Lan, Jiaxi Hu, and Yu Cheng.
  Mom: Linear sequence modeling with mixture-of-memories.
  *arXiv preprint arXiv:2502.13685*, 2025.
- Glorioso et al. (2024)

  Paolo Glorioso, Quentin Anthony, Yury Tokpanov, James Whittington, Jonathan Pilault, Adam Ibrahim, and Beren Millidge.
  Zamba: A compact 7b SSM.
  *arXiv preprint arXiv:2405.16712*, 2024.
- Google DeepMind (2025)

  Google DeepMind.
  Gemini pro.
  <https://deepmind.google/models/gemini/pro/>, 2025.
  Web page, accessed 2025.
- Gu and Dao (2024)

  Albert Gu and Tri Dao.
  Mamba: Linear-time sequence modeling with selective state spaces.
  In *First Conference on Language Modeling*, 2024.
  URL <https://openreview.net/forum?id=tEYskw1VY2>.
- Gu et al. (2020)

  Albert Gu, Tri Dao, Stefano Ermon, Atri Rudra, and Christopher Ré.
  Hippo: Recurrent memory with optimal polynomial projections.
  *Advances in neural information processing systems*, 33:1474–1487, 2020.
- Gu et al. (2022)

  Albert Gu, Karan Goel, and Christopher Ré.
  Efficiently modeling long sequences with structured state spaces.
  In *The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022*. OpenReview.net, 2022.
  URL <https://openreview.net/forum?id=uYLFoz1vlAC>.
- Gu et al. (2023)

  Albert Gu, Isys Johnson, Aman Timalsina, Atri Rudra, and Christopher Re.
  How to train your HIPPO: State space models with generalized orthogonal basis projections.
  In *International Conference on Learning Representations*, 2023.
  URL <https://openreview.net/forum?id=klK17OQ3KB>.
- Gupta et al. (2022)

  Ankit Gupta, Albert Gu, and Jonathan Berant.
  Diagonal state spaces are as effective as structured state spaces.
  In *NeurIPS*, 2022.
  URL <http://papers.nips.cc/paper_files/paper/2022/hash/9156b0f6dfa9bbd18c79cc459ef5d61c-Abstract-Conference.html>.
- He et al. (2024)

  Zhihao He, Hang Yu, Zi Gong, Shizhan Liu, Jianguo Li, and Weiyao Lin.
  Rodimus*: Breaking the accuracy-efficiency trade-off with efficient attentions.
  *arXiv preprint arXiv:2410.06577*, 2024.
- Hendrycks et al. (2021)

  Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- Hochreiter and Schmidhuber (1997)

  Sepp Hochreiter and Jürgen Schmidhuber.
  Long short-term memory.
  *Neural computation*, 9(8):1735–1780, 1997.
- Hu et al. (2025)

  Jingcheng Hu, Yinmin Zhang, Qi Han, Daxin Jiang, Xiangyu Zhang, and Heung-Yeung Shum.
  Open-reasoner-zero: An open source approach to scaling up reinforcement learning on the base model.
  *arXiv preprint arXiv:2503.24290*, 2025.
- Jain et al. (2025)

  Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
  Livecodebench: Holistic and contamination free evaluation of large language models for code.
  In *The Thirteenth International Conference on Learning Representations*, 2025.
- Jamba Team (2024)

  Jamba Team.
  Jamba-1.5: Hybrid T.
  *arXiv preprint arXiv:2408.12570*, 2024.
- Jimenez et al. (2024)

  Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
  SWE-bench: Can language models resolve real-world github issues?
  In *International Conference on Learning Representations*, 2024.
  URL <https://openreview.net/forum?id=VTF8yNQM66>.
- Katharopoulos et al. (2020)

  Angelos Katharopoulos, Apoorv Vyas, Nikolaos Pappas, and François Fleuret.
  Transformers are RNNs: Fast autoregressive transformers with linear attention.
  In *International Conference on Machine Learning*, pages 5156–5165. PMLR, 2020.
- Kimi Team (2025)

  Kimi Team.
  Kimi k1. 5: Scaling reinforcement learning with llms.
  *arXiv preprint arXiv:2501.12599*, 2025.
- Lin et al. (2025)

  Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Poovendran, Peter Clark, and Yejin Choi.
  Zebralogic: On the scaling limits of llms for logical reasoning.
  *arXiv preprint arXiv:2502.01100*, 2025.
- Liu et al. (2025a)

  Junteng Liu, Yuanxiang Fan, Zhuo Jiang, Han Ding, Yongyi Hu, Chi Zhang, Yiqi Shi, Shitong Weng, Aili Chen, Shiqi Chen, Yunan Huang, Mozhi Zhang, Pengyu Zhao, Junjie Yan, and Junxian He.
  Synlogic: Synthesizing verifiable reasoning data at scale for learning logical reasoning and beyond.
  *arXiv preprint arXiv:2505.19641*, 2025a.
- Liu et al. (2024)

  Siyao Liu, He Zhu, Jerry Liu, Shulin Xin, Aoyan Li, Rui Long, Li Chen, Jack Yang, Jinxiang Xia, Z. Y. Peng, Shukai Liu, Zhaoxiang Zhang, Ge Zhang, Wenhao Huang, Kai Shen, and Liang Xiang.
  Fullstack bench: Evaluating llms as full stack coders.
  *arXiv preprint arXiv:2412.00535*, 2024.
- Liu et al. (2025b)

  Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin.
  Understanding r1-zero-like training: A critical perspective.
  *arXiv preprint arXiv:2503.20783*, 2025b.
- Loshchilov and Hutter (2019)

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization.
  In *International Conference on Learning Representations*, 2019.
- Lu et al. (2025)

  Enzhe Lu, Zhejun Jiang, Jingyuan Liu, Yulun Du, Tao Jiang, Chao Hong, Shaowei Liu, Weiran He, Enming Yuan, Yuzhi Wang, et al.
  Moba: Mixture of block attention for long-context llms.
  *arXiv preprint arXiv:2502.13189*, 2025.
- Martin and Cundy (2018)

  Eric Martin and Chris Cundy.
  Parallelizing linear recurrent neural nets over sequence length.
  In *6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings*. OpenReview.net, 2018.
  URL <https://openreview.net/forum?id=HyUNwulC->.
- MiniMax et al. (2025)

  MiniMax, Aonian Li, Bangwei Gong, Bo Yang, Boji Shan, Chang Liu, Cheng Zhu, Chunhao Zhang, Congchao Guo, Da Chen, Dong Li, et al.
  Minimax-01: Scaling foundation models with lightning attention.
  *arXiv preprint arXiv:2501.08313*, 2025.
- Molybog et al. (2023)

  Igor Molybog, Peter Albert, Moya Chen, Zachary DeVito, David Esiobu, Naman Goyal, Punit Singh Koura, Sharan Narang, Andrew Poulton, Ruan Silva, Binh Tang, Diana Liskovich, Puxin Xu, Yuchen Zhang, Melanie Kambadur, Stephen Roller, and Susan Zhang.
  A theory on adam instability in large-scale machine learning.
  *arXiv preprint arXiv:2304.09871*, 2023.
- OpenAI (2024a)

  OpenAI.
  Introducing openai o1.
  <https://openai.com/o1/>, 2024a.
  Web page, accessed 2024.
- OpenAI (2024b)

  OpenAI.
  Openai mrcr dataset.
  <https://huggingface.co/datasets/openai/mrcr>, 2024b.
  Accessed: 2025-06-15.
- OpenAI (2025)

  OpenAI.
  Introducing deep research, 2025.
  URL <https://openai.com/index/introducing-deep-research/>.
- Peng et al. (2023)

  Bo Peng, Eric Alcaide, Quentin Gregory Anthony, Alon Albalak, Samuel Arcadinho, Stella Biderman, Huanqi Cao, Xin Cheng, Michael Nguyen Chung, Leon Derczynski, et al.
  Rwkv: Reinventing rnns for the transformer era.
  In *Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2023.
- Peng et al. (2024a)

  Bo Peng, Daniel Goldstein, Quentin Anthony, Alon Albalak, Eric Alcaide, Stella Biderman, Eugene Cheah, Teddy Ferdinan, Haowen Hou, and Przemysł Kazienko.
  Eagle and finch: Rwkv with matrix-valued states and dynamic recurrence.
  *arXiv preprint arXiv:2404.05892*, 2024a.
- Peng et al. (2024b)

  Bo Peng, Daniel Goldstein, Quentin Anthony, Alon Albalak, Eric Alcaide, Stella Biderman, Eugene Cheah, Teddy Ferdinan, Haowen Hou, and Przemysł Kazienko.
  Eagle and finch: Rwkv with matrix-valued states and dynamic recurrence.
  *arXiv preprint arXiv:2404.05892*, 2024b.
- Peng et al. (2025)

  Bo Peng, Ruichong Zhang, Daniel Goldstein, Eric Alcaide, Xingjian Du, Haowen Hou, Jiaju Lin, Jiaxing Liu, Janna Lu, William Merrill, et al.
  Rwkv-7.
  *arXiv preprint arXiv:2503.14456*, 2025.
- Peng et al. (2021)

  Hao Peng, Nikolaos Pappas, Dani Yogatama, Roy Schwartz, Noah Smith, and Lingpeng Kong.
  Random feature attention.
  In *International Conference on Learning Representations*, 2021.
  URL <https://openreview.net/forum?id=QtTKTdVrFBB>.
- Phan et al. (2025)

  Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang, Mohamed Shaaban, John Ling, Sean Shi, et al.
  Humanity’s last exam.
  *arXiv preprint arXiv:2501.14249*, 2025.
- Qin et al. (2021)

  Zhen Qin, Weixuan Sun, Hui Deng, Dongxu Li, Yunshen Wei, Baohong Lv, Junjie Yan, Lingpeng Kong, and Yiran Zhong.
  cosformer: Rethinking softmax in attention.
  In *Proceedings of the International Conference on Learning Representations (ICLR)*, 2021.
- Qin et al. (2022a)

  Zhen Qin, Xiaodong Han, Weixuan Sun, Dongxu Li, Lingpeng Kong, Nick Barnes, and Yiran Zhong.
  The devil in linear transformer.
  In *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing*, pages 7025–7041, 2022a.
- Qin et al. (2022b)

  Zhen Qin, Weixuan Sun, Hui Deng, Dongxu Li, Yunshen Wei, Baohong Lv, Junjie Yan, Lingpeng Kong, and Yiran Zhong.
  cosFormer: Rethinking softmax in attention.
  In *International Conference on Learning Representations*, 2022b.
  URL <https://openreview.net/forum?id=Bl8CQrx2Up4>.
- Qin et al. (2023)

  Zhen Qin, Songlin Yang, and Yiran Zhong.
  Hierarchically gated recurrent neural network for sequence modeling.
  In *Proceedings of the 37th International Conference on Neural Information Processing Systems*, pages 33202–33221, 2023.
- Qin et al. (2024a)

  Zhen Qin, Yuxin Mao, Xuyang Shen, Dong Li, Jing Zhang, Yuchao Dai, and Yiran Zhong.
  You only scan once: Efficient multi-dimension sequential modeling with lightnet.
  *arXiv preprint arXiv:2405.21022*, 2024a.
- Qin et al. (2024b)

  Zhen Qin, Weigao Sun, Dong Li, Xuyang Shen, Weixuan Sun, and Yiran Zhong.
  Lightning attention-2: A free lunch for handling unlimited sequence lengths in large language models.
  *arXiv preprint arXiv:2401.04658*, 2024b.
- Qin et al. (2024c)

  Zhen Qin, Weigao Sun, Dong Li, Xuyang Shen, Weixuan Sun, and Yiran Zhong.
  Various lengths, constant speed: Efficient language modeling with lightning attention.
  In *International conference on machine learning*, pages 41517–41535. PMLR, 2024c.
- Qin et al. (2024d)

  Zhen Qin, Songlin Yang, Weixuan Sun, Xuyang Shen, Dong Li, Weigao Sun, and Yiran Zhong.
  HGRN2.
  *arXiv preprint arXiv:2404.07904*, 2024d.
- Qwen et al. (2025)

  Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu.
  Qwen2.5 technical report.
  *arXiv preprint arXiv:2412.15115*, 2025.
- Rein et al. (2024)

  David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R Bowman.
  Gpqa: A graduate-level google-proof q&a benchmark.
  In *First Conference on Language Modeling*, 2024.
- Ren et al. (2024)

  Liliang Ren, Yang Liu, Yadong Lu, Yelong Shen, Chen Liang, and Weizhu Chen.
  Samba: Simple hybrid state space models for efficient unlimited context language modeling.
  *arXiv preprint arXiv:2406.07522*, 2024.
- Schulman et al. (2017)

  John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.
  Proximal policy optimization algorithms.
  *arXiv preprint arXiv:1707.06347*, 2017.
- Seed et al. (2025)

  ByteDance Seed, Jiaze Chen, Tiantian Fan, Xin Liu, Lingjun Liu, Zhiqi Lin, Mingxuan Wang, Chengyi Wang, Xiangpeng Wei, Wenyuan Xu, et al.
  Seed1. 5-thinking: Advancing superb reasoning models with reinforcement learning.
  *arXiv preprint arXiv:2504.13914*, 2025.
- Shao et al. (2024)

  Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Y Wu, et al.
  DeepSeekMath.
  *arXiv preprint arXiv:2402.03300*, 2024.
- Shen et al. (2024)

  Xuyang Shen, Dong Li, Ruitao Leng, Zhen Qin, Weigao Sun, and Yiran Zhong.
  Scaling laws for linear complexity language models.
  In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, pages 16377–16426, 2024.
- Sheng et al. (2024)

  Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu.
  Hybridflow: A flexible and efficient rlhf framework.
  *arXiv preprint arXiv:2409.19256*, 2024.
- Si et al. (2024)

  Chenglei Si, Diyi Yang, and Tatsunori Hashimoto.
  Can llms generate novel research ideas? a large-scale human study with 100+ nlp researchers.
  *arXiv preprint arXiv:2409.04109*, 2024.
- Siems et al. (2025)

  Julien Siems, Timur Carstensen, Arber Zela, Frank Hutter, Massimiliano Pontil, and Riccardo Grazzi.
  Deltaproduct: Improving state-tracking in linear rnns via householder products.
  *arXiv preprint arXiv:2502.10297*, 2025.
- Sirdeshmukh et al. (2025)

  Ved Sirdeshmukh, Kaustubh Deshpande, Johannes Mols, Lifeng Jin, Ed-Yeremai Cardona, Dean Lee, Jeremy Kritz, Willow Primack, Summer Yue, and Chen Xing.
  Multichallenge: A realistic multi-turn conversation evaluation benchmark challenging to frontier llms.
  *arXiv preprint arXiv:2501.17399*, 2025.
- Sun et al. (2025)

  Weigao Sun, Disen Lan, Tong Zhu, Xiaoye Qu, and Yu Cheng.
  Linear-moe: Linear sequence modeling meets mixture-of-experts.
  *arXiv preprint arXiv:2503.05447*, 2025.
- Sun et al. (2024)

  Yu Sun, Xinhao Li, Karan Dalal, Jiarui Xu, Arjun Vikram, Genghan Zhang, Yann Dubois, Xinlei Chen, Xiaolong Wang, Sanmi Koyejo, et al.
  Learning to (learn at test time): Rnns with expressive hidden states.
  *arXiv preprint arXiv:2407.04620*, 2024.
- Sun et al. (2023)

  Yutao Sun, Li Dong, Shaohan Huang, Shuming Ma, Yuqing Xia, Jilong Xue, Jianyong Wang, and Furu Wei.
  Retentive network: A successor to transformer for large language models.
  *arXiv preprint arXiv:2307.08621*, 2023.
- Tencent AI Lab (2025)

  Tencent AI Lab.
  Hunyuan-t1: Reasoning efficiency redefined.
  <https://llm.hunyuan.tencent.com/#/Blog/hy-t1/>, 2025.
  Accessed: 2025-06-15.
- Vaswani et al. (2017)

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  *Advances in neural information processing systems*, 30, 2017.
- von Oswald et al. (2025)

  Johannes von Oswald, Nino Scherrer, Seijin Kobayashi, Luca Versari, Songlin Yang, Maximilian Schlegel, Kaitlin Maile, Yanick Schimpf, Oliver Sieberling, Alexander Meulemans, et al.
  Mesanet: Sequence modeling by locally optimal test-time training.
  *arXiv preprint arXiv:2506.05233*, 2025.
- Wang et al. (2025)

  Shenzhi Wang, Le Yu, Chang Gao, Chujie Zheng, Shixuan Liu, Rui Lu, Kai Dang, Xionghui Chen, Jianxin Yang, Zhenru Zhang, Yuqiong Liu, An Yang, Andrew Zhao, Yang Yue, Shiji Song, Bowen Yu, Gao Huang, and Junyang Lin.
  Beyond the 80/20 rule: High-entropy minority tokens drive effective reinforcement learning for llm reasoning.
  *arXiv preprint arXiv:2506.01939*, 2025.
- Wang et al. (2024)

  Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo, Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al.
  Mmlu-pro: A more robust and challenging multi-task language understanding benchmark.
  In *The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2024.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models.
  *Advances in neural information processing systems*, 35:24824–24837, 2022.
- Wei et al. (2024)

  Jason Wei, Nguyen Karina, Hyung Won Chung, Yunxin Joy Jiao, Spencer Papay, Amelia Glaese, John Schulman, and William Fedus.
  Measuring short-form factuality in large language models.
  *arXiv preprint arXiv:2411.04368*, 2024.
- Xia et al. (2024)

  Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang.
  Agentless: Demystifying llm-based software engineering agents.
  *arXiv preprint arXiv:2407.01489*, 2024.
- Xu et al. (2025)

  Frank F. Xu, Yufan Song, Boxuan Li, Yuxuan Tang, Kritanjali Jain, Mengxue Bao, Zora Z. Wang, Xuhui Zhou, Zhitong Guo, Murong Cao, Mingyang Yang, Hao Yang Lu, Amaad Martin, Zhe Su, Leander Maben, Raj Mehta, Wayne Chi, Lawrence Jang, Yiqing Xie, Shuyan Zhou, and Graham Neubig.
  Theagentcompany: Benchmarking llm agents on consequential real world tasks.
  *arXiv preprint arXiv:2412.14161*, 2025.
- Yang et al. (2024a)

  Songlin Yang, Bailin Wang, Yikang Shen, Rameswar Panda, and Yoon Kim.
  Gated linear attention transformers with hardware-efficient training.
  *arXiv preprint arXiv:2312.06635*, 2024a.
- Yang et al. (2024b)

  Songlin Yang, Bailin Wang, Yu Zhang, Yikang Shen, and Yoon Kim.
  Parallelizing linear transformers with the delta rule over sequence length.
  *arXiv preprint arXiv:2406.06484*, 2024b.
- Yao et al. (2025)

  Shunyu Yao, Noah Shinn, Pedram Razavi, and Karthik R Narasimhan.
  τ\tau-bench: A benchmark for tool-agent-user interaction in real-world domains.
  In *The Thirteenth International Conference on Learning Representations*, 2025.
- Yu et al. (2025)

  Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan, Gaohong Liu, Lingjun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng, Yuxuan Tong, Chi Zhang, Mofan Zhang, Wang Zhang, Hang Zhu, Jinhua Zhu, Jiaze Chen, Jiangjie Chen, Chengyi Wang, Hongli Yu, Yuxuan Song, Xiangpeng Wei, Hao Zhou, Jingjing Liu, Wei-Ying Ma, Ya-Qin Zhang, Lin Yan, Mu Qiao, Yonghui Wu, and Mingxuan Wang.
  Dapo: An open-source llm reinforcement learning system at scale.
  *arXiv preprint arXiv:2503.14476*, 2025.
- Yuan et al. (2025)

  Jingyang Yuan, Huazuo Gao, Damai Dai, Junyu Luo, Liang Zhao, Zhengyan Zhang, Zhenda Xie, YX Wei, Lean Wang, Zhiping Xiao, et al.
  Native sparse attention: Hardware-aligned and natively trainable sparse attention.
  *arXiv preprint arXiv:2502.11089*, 2025.
- Zaheer et al. (2020)

  Manzil Zaheer, Guru Guruganesh, Kumar Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, et al.
  Big Bird: Transformers for longer sequences.
  *Advances in neural information processing systems*, 33:17283–17297, 2020.
- Zeng et al. (2025)

  Weihao Zeng, Yuzhen Huang, Qian Liu, Wei Liu, Keqing He, Zejun Ma, and Junxian He.
  Simplerl-zoo: Investigating and taming zero reinforcement learning for open base models in the wild.
  *arXiv preprint arXiv:2503.18892*, 2025.
- Zhang et al. (2024)

  Yu Zhang, Songlin Yang, Rui-Jie Zhu, Yue Zhang, Leyang Cui, Yiqiao Wang, Bolun Wang, Freda Shi, Bailin Wang, Wei Bi, et al.
  Gated slot attention for efficient linear-time sequence modeling.
  *Advances in Neural Information Processing Systems*, 37:116870–116898, 2024.

## 附录 A 贡献者

本报告的贡献者按姓氏字母顺序列出如下：

Aili Chen,
Aonian Li,
Bangwei Gong,
Binyang Jiang,
Bo Fei,
Bo Yang,
Boji Shan,
Changqing Yu,
Chao Wang,
Cheng Zhu,
Chengjun Xiao,
Chengyu Du,
Chi Zhang,
Chu Qiao,
Chunhao Zhang,
Chunhui Du,
Congchao Guo,
Da Chen,
Deming Ding,
Dianjun Sun,
Dong Li,
Enwei Jiao,
Haigang Zhou,
Haimo Zhang,
Han Ding,
Haohai Sun,
Haoyu Feng,
Huaiguang Cai,
Haichao Zhu,
Jian Sun,
Jiaqi Zhuang,
Jiaren Cai,
Jiayuan Song,
Jin Zhu,
Jingyang Li,
Jinhao Tian,
Jinli Liu,
Junhao Xu,
Junjie Yan,
Junteng Liu,
Junxian He,
Kaiyi Feng,
Ke Yang,
Kecheng Xiao,
Le Han,
Leyang Wang,
Lianfei Yu,
Liheng Feng,
Lin Li,
Lin Zheng,
Linge Du,
Lingyu Yang,
Lunbin Zeng,
Minghui Yu,
Mingliang Tao,
Mingyuan Chi,
Mozhi Zhang,
Mujie Lin,
Nan Hu,
Nongyu Di,
Peng Gao,
Pengfei Li,
Pengyu Zhao,
Qibing Ren,
Qidi Xu,
Qile Li,
Qin Wang,
Rong Tian,
Ruitao Leng,
Shaoxiang Chen,
Shaoyu Chen,
Shengmin Shi,
Shitong Weng,
Shuchang Guan,
Shuqi Yu,
Sichen Li,
Songquan Zhu,
Tengfei Li,
Tianchi Cai,
Tianrun Liang,
Weiyu Cheng,
Weize Kong,
Wenkai Li,
Xiancai Chen,
Xiangjun Song,
Xiao Luo,
Xiao Su,
Xiaobo Li,
Xiaodong Han,
Xinzhu Hou,
Xuan Lu,
Xun Zou,
Xuyang Shen,
Yan Gong,
Yan Ma,
Yang Wang,
Yiqi Shi,
Yiran Zhong,
Yonghong Duan,
Yongxiang Fu,
Yongyi Hu,
Yu Gao,
Yuanxiang Fan,
Yufeng Yang,
Yuhao Li,
Yulin Hu,
Yunan Huang,
Yunji Li,
Yunzhi Xu,
Yuxin Mao,
Yuxuan Shi,
Yuze Wenren,
Zehan Li,
Zelin Li,
Zhanxu Tian,
Zhengmao Zhu,
Zhenhua Fan,
Zhenzhen Wu,
Zhichao Xu,
Zhihang Yu,
Zhiheng Lyu,
Zhuo Jiang,
Zibo Gao,
Zijia Wu,
Zijian Song,
Zijun Sun

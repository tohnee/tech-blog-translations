---
title: "MiMo：解锁语言模型的推理潜能"
title_en: "MiMo: Unlocking the Reasoning Potential of Language Model -- From Pretraining to Posttraining"
arxiv: 2505.07608
date: 2025-05-12
source: https://arxiv.org/abs/2505.07608
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo：解锁语言模型的推理潜能

> 原文：[MiMo](https://arxiv.org/abs/2505.07608) · 小米 MiMo arXiv

小米 LLM-Core

###### 摘要

我们推出 MiMo-7B，一个专为推理任务而生的大语言模型，在预训练与后训练两个阶段均进行了优化。
在预训练阶段，我们增强了数据预处理管线，并采用三阶段数据配比策略来夯实基础模型的推理潜能。
MiMo-7B-Base 在 25 万亿 token 上完成预训练，并额外引入多 token 预测（Multi-Token Prediction）目标以增强性能并加速推理。
在后训练阶段，我们为强化学习精选了 13 万道可验证的数学与编程问题，引入测试难度驱动的代码奖励机制以缓解稀疏奖励问题，并采用策略性的数据重采样来稳定训练。
大量评测表明，MiMo-7B-Base 具备卓越的推理潜能，甚至超越规模大得多的 32B 模型。
最终的 RL 微调模型 MiMo-7B-RL 在数学、代码与通用推理任务上取得优异表现，超越 OpenAI o1-mini。
模型检查点可在 <https://github.com/xiaomimimo/MiMo> 获取。

图 1：
MiMo-7B 在代码与数学推理基准上的性能。

## 1 引言

具备先进推理能力的大语言模型（LLM），如 OpenAI o 系列（[OpenAI, 2024](#bib.bib42)）、DeepSeek R1（[Guo et al., 2025](#bib.bib17)）与 Claude 3.7（[Anthropic, 2025](#bib.bib2)），在数学推理、代码生成等复杂任务中取得了耀眼成绩。
通过大规模强化学习（RL），这些模型发展出复杂的推理模式，包括逐步分析、自我反思与回溯，从而在各领域获得更稳健、更准确的问题解决能力。
这一新兴范式代表着人工智能应对复杂挑战方式的重大进步。

目前，大多数成功的 RL 工作（包括开源研究）都依赖相对较大的基础模型，例如 32B 模型，在提升代码推理能力时尤为如此。
此外，人们普遍认为在小模型中同时、均匀地提升数学与代码能力颇具挑战。
尽管如此，我们相信 RL 训练出的推理模型的效果，依赖于基础模型固有的推理潜能。
要充分释放语言模型的推理潜能，努力方向不仅在后训练，还在于面向推理定制的预训练策略。

在本工作中，我们推出 MiMo-7B——一系列从零开始训练、为推理任务而生的模型。
基于 MiMo-7B-Base 的 RL 实验表明，我们的模型具备非凡的推理潜能，甚至超越规模大得多的 32B 模型。
此外，我们在冷启动的 SFT 模型上进行 RL 训练，得到 MiMo-7B-RL，它在数学与代码推理任务上均展现出卓越性能，超越 OpenAI o1-mini。
以下是我们的具体贡献：

##### 预训练：为推理而生的基础模型

- •

  我们优化了数据预处理管线，增强文本抽取工具并施加多维数据过滤，以提升预训练数据中的推理模式密度。我们还采用多种策略生成海量多样的合成推理数据。
- •

  我们在预训练中采用三阶段数据配比策略。总体而言，MiMo-7B-Base 在约 25 万亿 token 上完成预训练。
- •

  我们引入多 token 预测（MTP）作为附加训练目标，既增强模型性能又加速推理。

##### 后训练配方：开创性推理模型

- •

  我们精选 13 万道数学与代码问题作为 RL 训练数据，全部可由基于规则的验证器验证。每道题都经过细致清洗与难度评估以确保质量。我们只采用基于规则的正确性奖励，以规避潜在的奖励黑客（reward hacking）。
- •

  为缓解困难代码问题的稀疏奖励问题，我们引入测试难度驱动的代码奖励。通过为不同难度的测试用例赋予细粒度分数，策略可以借助密集的奖励信号得到更有效的优化。
- •

  我们实现了数据重采样策略，以提升 rollout 采样效率并稳定策略更新，在 RL 训练后期尤为有效。

##### RL 基础设施

- •

  我们开发了无缝 Rollout 引擎（Seamless Rollout Engine）以加速 RL 训练与验证。该设计融合连续 rollout、异步奖励计算与提前终止，最大限度减少 GPU 空闲时间，实现 2.29 倍的训练加速与 1.96 倍的验证加速。
- •

  我们在 vLLM 中支持 MTP，并增强了 RL 系统中推理引擎的鲁棒性。

##### 评测结果小结

- •

  MiMo-7B-Base 优于约 7B 参数量的 SoTA 开源模型，在通用知识与编程任务上表现出色。在 BBH 上取得 75.2 分，展现出卓越的推理能力。其在 SuperGPQA 上的强劲表现进一步凸显了处理复杂研究生级问题的能力。
- •

  MiMo-7B-RL-Zero 在数学与代码任务上的 RL 训练表现超越 32B 基础模型。这凸显了它在 RL 训练中的效率与潜力，使 MiMo-7B 成为未来 RL 进展的有力候选。
- •

  MiMo-7B-RL 取得卓越的推理性能。它在 AIME 2025 上得分 55.4，超出 o1-mini 4.7 分。在算法代码生成任务上，MiMo-7B-RL 的结果极为亮眼，在 LiveCodeBench v5 与最新 v6 上均显著超越 OpenAI o1-mini，展现出稳健可靠的能力。MiMo-7B-RL 同时保持了有竞争力的通用性能。

##### 开源

我们开源 MiMo-7B 系列，包括基础模型、SFT 模型、从基础模型训练的 RL 模型以及从 SFT 模型训练的 RL 模型的检查点。
我们相信本报告与这些模型将为开发强大推理 LLM 提供宝贵洞见，惠及更广泛的社区。

## 2 预训练

在本节中，我们首先详述在 MiMo-7B 预训练过程中增强推理能力的策略，涵盖预训练数据构建、模型架构设计与超参数设置。
随后我们展示 MiMo-7B-Base 模型的推理潜能。

### 2.1 预训练数据

MiMo-7B 的预训练语料整合了多种来源，包括网页、学术论文、书籍、程序代码与合成数据。
我们相信，在预训练阶段纳入更多具有高质量推理模式的数据，可以显著增强所得语言模型的推理潜能。
为实现这一目标，我们首先优化自然文本预处理管线，以提升质量，尤其是推理数据密度。
其次，我们利用先进推理模型生成大量合成推理数据。
最后，我们实施三阶段数据配比策略，以最大化模型在各类任务与领域上的推理潜能。

##### 更优的推理数据抽取

网页天然包含高密度推理模式的内容，如编程教程与数学博客。
然而我们发现，常用的抽取工具（[Barbaresi, 2021](#bib.bib4)）往往无法保留网页中嵌入的数学公式与代码片段。
为克服这一局限，我们开发了一款专为数学内容（[Liu et al., 2024c](#bib.bib37)；[Paster et al., 2024](#bib.bib43)；[Zhou et al., 2025](#bib.bib68)）、代码块与论坛站点特别优化的全新 HTML 抽取工具。
对于论文与书籍，我们增强了 PDF 解析工具包，以更好地处理 STEM 与代码内容。
借助这些优化后的抽取工具，我们成功为后续处理环节保留了海量推理模式。

##### 快速全局去重

数据去重在提升训练效率与降低过拟合方面作用重大。
我们对所有网页转储同时采用 URL 去重与 MinHash 去重（[Broder, 1997](#bib.bib6)）。
通过极致的工程优化，我们可以在一天之内完成这一全局去重流程。
由于去重算法对高质量与低质量文本一视同仁、缺乏内容感知，我们随后依据多维质量得分调整最终数据分布。

##### 多维数据过滤

富含推理模式的高质量预训练数据，对开发具备强推理能力的模型至关重要。
我们发现，常用的启发式规则过滤器（[Penedo et al., 2023](#bib.bib44)；[Penedo et al., 2024](#bib.bib45)）会错误地过滤掉含有大量数学与代码内容的高质量网页。
为克服这一局限，我们转而微调小型 LLM 作为数据质量标注器，执行领域分类与多维质量评估。

##### 合成推理数据

推理模式的另一个重要来源是由先进推理模型生成的合成数据。
我们采用多种策略生成多样的合成推理回复。
首先，我们选取标注为高推理深度的 STEM 内容，提示模型基于原始材料展开有洞见的分析与深度思考。
其次，我们收集数学与代码问题，并提示推理模型求解。
此外，我们还纳入通用领域的查询，尤其是创意写作任务。
值得注意的是，初步实验揭示：与非推理数据不同，合成推理数据可以训练极多的 epoch 而无过拟合风险。

##### 三阶段数据配比

为优化预训练数据分布，我们在最终模型训练中采用三阶段数据配比策略：

- •

  阶段 1：纳入除推理任务查询的合成回复之外的全部数据来源。我们对占比过高的内容降采样，如广告、新闻、招聘启事以及知识密度与推理深度不足的材料；同时对来自专业领域、质量上乘的高价值数据升采样。
- •

  阶段 2：在阶段 1 精选分布的基础上，我们将数学与代码相关数据显著提升至约占配比的 70%。这一做法有望在不损害通用语言能力的前提下增强专业技能（[Zhu et al., 2024](#bib.bib70)）。前两个阶段以 8,192 token 的上下文长度训练。
- •

  阶段 3：为提升求解复杂任务的能力，我们进一步加入约 10% 针对数学、代码与创意写作查询的合成回复。同时，在最后阶段将上下文长度从 8,192 扩展到 32,768。

经由这一流程，我们构建了一个总计约 25 万亿 token 的大规模高质量预训练数据集。

### 2.2 模型架构

图 2：MiMo-7B 的多 token 预测实现。预训练时我们使用单个 MTP 层，而推理阶段可使用多个 MTP 层以获得额外加速。

MiMo-7B 遵循通用的 decoder-only Transformer 架构（[Vaswani et al., 2017](#bib.bib58)；[Radford et al., 2018](#bib.bib46)），由分组查询注意力（GQA，[Ainslie et al. 2023](#bib.bib1)）、pre-RMSNorm（[Zhang and Sennrich, 2019](#bib.bib65)）、SwiGLU 激活（[Dauphin et al., 2017](#bib.bib10)）与旋转位置编码（RoPE，[Su et al. 2024](#bib.bib52)）组成，与 Llama（[Touvron et al., 2023](#bib.bib57)；[Grattafiori et al., 2024](#bib.bib15)）和 Qwen（[Yang et al., 2024](#bib.bib61)）类似。

推理模型因其冗长的自回归生成过程而常面临推理速度瓶颈，尽管其推理路径中相邻 token 之间具有很高的相关性与可预测性。

##### MTP 模块

受 DeepSeek-V3（[Liu et al., 2024a](#bib.bib33)）启发，我们引入多 token 预测（MTP）（[Gloeckle et al., 2024](#bib.bib14)）作为附加训练目标。
该方法使模型能够策略性地预先规划，并生成有助于更准确、且有望更快预测未来 token 的表示。
如图 [2](#S2.F2) 所示，我们为预训练与推理实现了不同的 MTP 设置。
预训练期间我们仅使用单个 MTP 层，因为初步研究表明多层 MTP 不会带来进一步提升。
相反，我们发现多个并行的 MTP 层可通过投机解码显著加速推理。
为实现这一点，预训练结束后，我们将预训练好的单个 MTP 层复制为两份相同的副本。
然后，在冻结主模型与第一个 MTP 层的情况下，微调两个新的 MTP 层用于推理加速。

##### MTP 推理加速

推理期间，这些 MTP 层可用于投机解码（[Leviathan et al., 2023](#bib.bib30)；[Xia et al., 2023](#bib.bib60)）以降低生成延迟。
我们在 AIME24 基准上评估了 MTP 层的表现。
第一个 MTP 层达到约 90% 的极高接受率，而即使是第三个 MTP 层也保持 75% 以上的接受率。
这一高接受率使 MiMo-7B 能够提供更快的解码速度，在需要超长输出的推理场景中尤为突出。

### 2.3 超参数

##### 模型超参数

我们将 Transformer 层数设为 36，隐藏维度设为 4,096。FFN 的中间隐藏维度设为 11,008。注意力头数为 32，键值分组数为 8。

##### 训练超参数

优化器采用 AdamW（[Loshchilov and Hutter, 2019](#bib.bib38)），$\beta_{1}=0.9$、$\beta_{2}=0.95$，权重衰减 0.1。我们施加最大范数为 1.0 的梯度截断。

前两个预训练阶段中，最大序列长度为 8,192 token，RoPE 基数为 10,000。
阶段 3 将这些参数分别扩展到 32,768 token 与 640,000。

学习率调度在阶段 1 启动：先在前 84B token 上从 0 线性预热到 $1.07\times 10^{-4}$，随后以 $1.07\times 10^{-4}$ 恒定学习率训练 10.2T token，最后在 7.5T token 上按余弦衰减到 $3\times 10^{-5}$。
该 $3\times 10^{-5}$ 的学习率贯穿阶段 2（4T token）并延续到阶段 3 的前 1.5T token。随后，学习率在最后 500B token 上按余弦计划衰减到 $1\times 10^{-5}$。

我们实施线性批量大小预热，在前 168B token 上增至 2,560，并在阶段 1 余下部分与阶段 2 全程维持该值。
阶段 3 中，批量大小固定为 640。

MTP 损失权重在前 10.3T token 上设为 0.3，随后在预训练其余部分降为 0.1。

### 2.4 预训练评测

#### 2.4.1 评测设置

我们在一系列基准上评测 MiMo-7B-Base，涵盖自然语言理解与推理、科学问答、阅读理解、数学推理、编程、中文理解以及长上下文理解能力：

语言理解与推理：BBH（[Suzgun et al., 2023](#bib.bib53)）、MMLU [Hendrycks et al. (2021a)](#bib.bib19)、MMLU-Redux（[Gema et al., 2024](#bib.bib13)）、MMLU-Pro（[Wang et al., 2024](#bib.bib59)）、ARC（[Clark et al., 2018](#bib.bib8)）、HellaSwag（[Zellers et al., 2019](#bib.bib64)）、PIQA（[Bisk et al., 2020](#bib.bib5)）。

闭卷问答：TriviaQA（[Joshi et al., 2017](#bib.bib26)）、NaturalQuestions（[Kwiatkowski et al., 2019](#bib.bib27)）。

科学问答：GPQA（[Rein et al., 2024](#bib.bib47)）、SuperGPQA（[Du et al., 2025](#bib.bib11)）。

阅读理解：DROP（[Dua et al., 2019](#bib.bib12)）、RACE（[Lai et al., 2017](#bib.bib29)）。

数学推理：AIME（[MAA, 2024](#bib.bib39)）、GSM8K（[Cobbe et al., 2021](#bib.bib9)）、MATH（[Hendrycks et al., 2021b](#bib.bib20)）。

编程：LiveCodeBench（[Jain et al., 2024](#bib.bib25)）、HumanEval（[Chen et al., 2021](#bib.bib7)）、HumanEval+（[Liu et al., 2023](#bib.bib34)）、MBPP（[Austin et al., 2021](#bib.bib3)）、MBPP+（[Liu et al., 2023](#bib.bib34)）、CRUXEval（[Gu et al., 2024](#bib.bib16)）。

其他：WinoGrande（[Sakaguchi et al., 2020](#bib.bib48)）、AGIEval（[Zhong et al., 2024a](#bib.bib66)）。

中文理解：C-Eval（[Huang et al., 2023](#bib.bib23)）、CMMLU（[Li et al., 2023](#bib.bib31)）。

长上下文理解：RULER（[Hsieh et al., 2024](#bib.bib21)）

我们将 MiMo-7B-Base 与其他规模相近的开源基础模型比较，包括 Llama-3.1-8B（[Grattafiori et al., 2024](#bib.bib15)）、Gemma-2-9B（[Team, 2024](#bib.bib55)）与 Qwen2.5-7B（[Yang et al., 2024](#bib.bib61)）。
所有模型的评测采用相同的评测设置。

#### 2.4.2 推理能力的上界

传统评测方法依赖单次成功率或多次采样的平均性能，往往会低估模型的真实推理潜能。
遵循 [Yue et al. (2025)](#bib.bib63)，我们采用 pass@k 指标——只要 k 个采样解中任意一个正确即视为解决——以更好地衡量不同模型推理能力的边界。

如图 [3](#S2.F3) 所示，在所有基准与所评测的 k 值上，MiMo-7B-Base 取得的 pass@k 分数均显著高于全部对比模型，包括 32B 基线。
值得注意的是，MiMo-7B-Base 与其他基线之间的性能差距随 k 增大而稳步拉大，在 LiveCodeBench 上尤为明显。
这些结果证明了 MiMo-7B-Base 卓越的推理潜能，为 RL 训练奠定了强大的基础策略。

![参见正文](2505.07608v2/code-math.png)

图 3：不同基础模型在多个推理基准上的 Pass@k 曲线。

#### 2.4.3 评测结果

| 基准 | 提示数 | Llama-3.1-8B Base | Gemma-2-9B Base | Qwen2.5-7B Base | MiMo-7B Base |
| --- | --- | --- | --- | --- | --- |
| 通用 | | | | | |
| BBH (EM) | 3-shot | 64.2 | 69.4 | 70.4 | 75.2 |
| GPQA-Diamond (EM) | 5-shot | 33.3 | 24.2 | 35.4 | 25.8 |
| SuperGPQA (EM) | 5-shot | 19.9∗ | 22.6∗ | 24.6∗ | 25.1 |
| DROP (F1) | 3-shot | 59.5 | 67.9∗ | 61.5∗ | 69.2 |
| MMLU (EM) | 5-shot | 65.3 | 71.2 | 74.2 | 71.2 |
| MMLU-Redux (EM) | 5-shot | 58.4∗ | 67.9 | 71.1 | 65.3 |
| MMLU-Pro (EM) | 5-shot | 37.1 | 44.7 | 45.0 | 41.9 |
| ARC-Easy (EM) | 25-shot | 84.3 | 88.3 | 86.4 | 85.2 |
| ARC-Challenge (EM) | 25-shot | 57.7 | 68.2 | 63.8 | 62.3 |
| HellaSwag (EM) | 10-shot | 82.0 | 81.9 | 80.4 | 80.0 |
| PIQA (EM) | 0-shot | 80.3 | 81.9 | 78.5 | 79.4 |
| WinoGrande (EM) | 5-shot | 60.5 | 73.9∗ | 75.9 | 78.0 |
| RACE-High (EM) | 5-shot | 44.3 | 48.3 | 46.8 | 44.1 |
| TriviaQA (EM) | 5-shot | 70.6 | 76.5 | 60.0 | 60.8 |
| NaturalQuestions (EM) | 5-shot | 27.7 | 29.2 | 24.1 | 24.5 |
| AGIEval (EM) | 0-shot | 38.2∗ | 21.6∗ | 44.4 | 48.3 |
| 数学 | | | | | |
| AIME 2024 (Pass@1) | 0-shot | 0.3∗ | 0.0∗ | 10.1∗ | 32.9 |
| AIME 2025 (Pass@1) | 0-shot | 0.0∗ | 0.0∗ | 4.3∗ | 24.3 |
| GSM8K (EM) | 8-shot | 48.5∗ | 70.2∗ | 80.2∗ | 75.2 |
| MATH (EM) | 4-shot | 16.9∗ | 36.4∗ | 44.3∗ | 37.4 |
| 编程 | | | | | |
| LiveCodeBench v5 (Pass@1) | 0-shot | 0.4∗ | 0.0∗ | 5.0∗ | 32.9 |
| HumanEval (Pass@1) | 1-shot | 37.8∗ | 41.5∗ | 56.7∗ | 51.8 |
| HumanEval+ (Pass@1) | 1-shot | 31.7∗ | 31.1∗ | 50.0∗ | 44.5 |
| MBPP (Pass@1) | 3-shot | 58.4 | 63.9 | 76.7 | 69.2 |
| MBPP+ (Pass@1) | 3-shot | 49.9 | 52.9 | 64.2 | 56.6 |
| CRUXEval-I (EM) | 2-shot | 41.5 | 49.8 | 52.4 | 47.6 |
| CRUXEval-O (EM) | 2-shot | 36.8 | 42.4 | 48.5 | 56.3 |
| 中文 | | | | | |
| C-Eval (EM) | 5-shot | 52.2 | 57.0 | 81.8 | 68.7 |
| CMMLU (EM) | 5-shot | 52.1 | 58.4 | 82.7 | 70.9 |

表 1：
MiMo-7B-Base 与其他规模相近的开源基础模型的对比。
带 * 的结果由我们的内部评测框架获得。

##### 通用推理

MiMo-7B-Base 在通用知识与推理方面表现优异，超越规模相近的开源模型。
在评估语言推理能力的 BBH 基准上，MiMo-7B-Base 得分 75.2，超出 Qwen2.5-7B 约 5 分。
此外，SuperGPQA 的结果显示了我们的模型在求解研究生级问题上的稳健表现。
在阅读理解基准 DROP 上，MiMo-7B-Base 优于各对比模型，展现出先进的语言理解能力。

##### 编程与数学推理

MiMo-7B-Base 在编程与数学任务上展现出深厚功力。
在 LiveCodeBench v5 上取得 32.9 分，远超 Llama-3.1-8B 与 Qwen-2.5-7B。
同样，在 AIME 2024 上，我们的模型取得 32.9 分，显著优于其他同等规模的基础模型。
这些结果凸显了 MiMo-7B-Base 非凡的问题求解能力及其在复杂推理任务上的巨大潜力。

![参见正文](2505.07608v2/mimo_ruler.png)

图 4：RULER 上的长上下文理解结果。我们的 MiMo-7B-Base 在所支持的 32K 上下文长度内取得接近完美的 NIAH 检索表现，并在强调超越检索的长上下文推理的常见词抽取（CWE）、高频词抽取（FWE）与变量追踪（VT）任务上交付了亮眼成绩。

##### 长上下文理解

理解并基于长上下文进行推理的能力，对现代思考模型（[Liu et al., 2025](#bib.bib35)）至关重要，因为这使其能够产出长而复杂的推理链。

对于聚焦长上下文检索的大海捞针（NIAH）任务（单钥、多键、多值与多查询 NIAH），我们汇总了不同深度与上下文长度下的准确率，如图 [4](#S2.F4) 最左侧面板所示。我们观察到，MiMo-7B 在 32K 上下文窗口内的所有位置上都取得接近完美的检索表现。

在纯检索之外，MiMo-7B 在需要长上下文推理的任务中同样出色，包括常见词抽取（CWE）、高频词抽取（FWE）与变量追踪（VT）。它交付了亮眼的表现，并在大多数场景中超越 Qwen2.5-7B。这些结果验证了我们在预训练期间纳入具有高质量推理模式的多样数据的策略的有效性。

## 3 后训练

预训练阶段之后，我们在 MiMo-7B-Base 上实施后训练。
具体而言，我们通过从 MiMo-7B-Base 直接 RL 得到 MiMo-7B-RL-Zero，并从 MiMo-7B 的 SFT 版本训练得到 MiMo-7B-RL。

### 3.1 监督微调

##### SFT 数据

SFT 数据由开源与自研蒸馏数据组合而成。为确保最优的质量与多样性，我们实施了三阶段预处理管线。
首先，我们剔除所有与评测基准存在 16-gram 重叠的训练查询，以防范数据泄漏。
然后，我们排除语言混杂或回复不完整的样本。
最后，我们将每个查询的回复数量上限设为 8，在保留多样性与防止冗余之间取得平衡。
经过这一预处理，最终的 SFT 数据集包含约 50 万个样本。

##### SFT 超参数

我们以 $3\times 10^{-5}$ 的恒定学习率、128 的批量大小微调 MiMo-7B-Base 模型。训练期间样本被打包到最长 32,768 token。

### 3.2 RL 数据构建

我们利用数学与代码两类可验证问题来构建 RL 训练数据。
我们的初步研究表明，高质量的问题集对稳定 RL 训练过程、进一步提升 LLM 的推理能力起着关键作用。

##### 数学数据

我们的数学题集来源多样，包括开源数据集与自研收集的竞赛级题库。
为降低奖励黑客的风险，我们利用 LLM 过滤证明题与选择题。
与近期为确保整数答案而改写题目的做法不同，我们保留原始题目以最小化奖励黑客。
此外，我们执行全局 n-gram 去重，并对题集与评测基准进行了细致的去污染。

我们采用基于模型的难度评估来进一步提升数据集质量。
首先，我们滤除先进推理模型无法求解的题目，以识别过难或答案有误的题目。
对剩余题目，我们将 MiMo-7B 的 SFT 版本 rollout 16 次，剔除通过率超过 90% 的题目。
值得注意的是，这一过程从原始题集中移除了约 50% 的简单题目。
数据清洗后，我们建立了包含 10 万道题的数学训练集。

##### 代码数据

在编程题方面，我们精选了由开源数据集与新收集题集组成的高质量训练集。
我们移除没有测试用例的题目。
对于有标准答案（golden solution）的题目，我们排除标准答案未能通过全部测试用例者。
对于没有标准答案的题目，我们丢弃在先进推理模型 16 次 rollout 中没有任何测试用例被通过的题目。
与数学数据类似，我们利用 MiMo-7B 的 SFT 版本滤除在全部 16 次 rollout 中都被完美求解的简单题目。
这一严格的清洗流程产出 3 万道代码题。

在每次 RL 迭代中，我们要评估数千道题目以计算奖励，每道题目可能包含数百个测试用例。
为提升奖励计算效率并消除 GPU 空闲时间，我们开发了在线评测（online judge）环境，支持极高吞吐单元测试的并行执行。

##### 奖励函数

我们在训练过程中仅采用基于规则的正确性奖励。
对于数学数据，我们使用基于规则的 Math-Verify 库来判定回复的正确性。
对于代码问题，我们实现了测试难度驱动的奖励，详见第 [3.3.1](#S3.SS3.SSS1) 节。
不引入额外奖励，如格式奖励与长度惩罚奖励。

### 3.3 RL 训练配方

我们采用经修改的组相对策略优化（GRPO）（[Shao et al., 2024](#bib.bib50)），并吸收了研究社区近期提出的改进（[Hu et al., 2025](#bib.bib22)；[Yu et al., 2025](#bib.bib62)）。
对每个问题 $q$，算法从旧策略 $\pi_{\theta_{old}}$ 采样一组回复 $\left\{o_{1},o_{2},...,o_{G}\right\}$，并通过最大化以下目标来更新策略 $\pi_{\theta}$：

$$
\mathcal{J}_{\mathrm{GRPO}}\left(\theta\right)=\mathbb{E}_{q\sim D,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta}(\cdot|q)}\left[\frac{1}{\sum_{i=1}^{G}\left|o_{i}\right|}\sum_{i=1}^{G}\sum_{j=1}^{\left|o_{i}\right|}\mathrm{min}\left(\frac{\pi_{\theta}(o_{i}|q)}{\pi_{\theta_{old}}(o_{i}|q)}A_{i,j},\mathrm{clip}\left(\frac{\pi_{\theta}(o_{i}|q)}{\pi_{\theta_{old}}(o_{i}|q)},1-\varepsilon_{\mathrm{low}},1+\varepsilon_{\mathrm{high}}\right)A_{i,j}\right)\right] \tag{1}
$$

其中 $\varepsilon_{\mathrm{low}}$ 与 $\varepsilon_{\mathrm{high}}$ 为超参数。$A_{i,j}$ 是优势，由同组回复的奖励 $\left\{r_{1},r_{2},...,r_{G}\right\}$ 计算得出：

$$
A_{i,j}=\frac{r_{i}-\mathrm{mean}(\{r_{i}\}_{i=1}^{G})}{\mathrm{std}(\{r_{i}\}_{i=1}^{G})} \tag{2}
$$

在原始 GRPO 算法基础上，我们纳入了近期研究的若干增强：

- •

  移除 KL 损失（[Hu et al., 2025](#bib.bib22)；[He et al., 2025](#bib.bib18)）：直接移除 KL 损失即可有效释放策略模型的全部潜能，且不损害训练稳定性。
- •

  动态采样（[Yu et al., 2025](#bib.bib62)）：在 RL rollout 阶段，我们过量采样并过滤掉通过率为 1 与 0 的提示，使批次内所有提示都带有有效梯度，同时保持批量大小一致。该策略在策略训练全程自动校准题目难度。
- •

  Clip-Higher（[Yu et al., 2025](#bib.bib62)）：我们在固定下截断界 $\varepsilon_{\mathrm{low}}$ 的情况下，提高式 (1)中的上截断界 $\varepsilon_{\mathrm{high}}$。这可以缓解熵收敛问题，并促进策略探索新解。

在训练过程中，我们识别出影响模型性能的两个关键挑战：代码问题的稀疏奖励，以及动态采样采样效率的衰减。
为此，我们分别提出了测试复杂度驱动的奖励函数与简单数据重采样方法。

#### 3.3.1 测试难度驱动的奖励

当前，对于算法代码生成任务，Deepseek-R1 [Guo et al. (2025)](#bib.bib17) 等现有 RL 工作采用基于规则的奖励策略：只有当代码通过给定题目的全部测试用例时，解才获得奖励。然而对于困难的算法题，模型可能永远得不到任何奖励，从而无法从这些挑战性案例中学习，也降低了动态采样的训练效率。

##### IOI 评分规则中的多档测试难度

为突破这一局限，我们提出一种新的奖励机制——测试难度驱动的奖励。其设计灵感来自国际信息学奥林匹克竞赛（IOI）的评分规则（[IOI 2024](#bib.bib24)）。在 IOI 竞赛中，每道完整的题目被划分为多个子任务，参赛者每完成一个子任务即可获得相应分数。每个子任务包含难度不同的测试。
为子任务赋予不同分数，更贴近人类解题的方式。
对于有挑战性的题目，模型仍可通过解出部分子任务赚取部分分数，从而在训练中更好地利用这些困难样例。

##### 基于通过率为测试分配难度

我们提出一种基于难度对测试用例分组的技术。我们利用多个模型对每道题目进行多次 rollout，并计算每个测试用例在全部模型生成解上的通过率。随后，我们依据通过率将测试用例聚类为不同难度等级，通过率越低难度越高。
图 [5](#S3.F5) 左侧展示了某道题目各测试用例的通过率与难度等级。结果揭示了测试难度的清晰分层，并表明能力更强的模型取得更高的通过率。

图 5：测试难度驱动奖励的实验。

##### 奖励规则

在将测试划分到不同难度等级后，我们基于这些难度等级设计了两种奖励方案：严格方案与温和方案。(1) 严格奖励。在严格奖励方案下，一个解只有在通过该难度组内全部测试以及所有更低难度组的测试时，才获得对应难度等级的奖励。
(2) 温和奖励。与之相对，温和奖励方案将每组的总分平均分摊到组内各测试上。最终奖励是所有通过测试的得分之和。图 [5](#S3.F5) 右侧比较了两种奖励方案相对于不带测试难度驱动奖励的基线所取得的性能。

#### 3.3.2 简单数据的过滤与重采样

在 RL 训练中，随着策略提升，越来越多的题目取得 1 的满分通过率。
在动态采样机制下，这些题目随后会从批次中过滤出去，不参与策略更新。
这种过滤导致采样效率急剧下降，因为构造一个固定大小的批次需要更多 rollout。
解决这一效率问题的一个直接做法，是把满分通过率的题目从训练数据中彻底移除。
然而，我们的初步研究表明，这一方法会给策略更新带来显著的不稳定。

为了在不冒策略坍塌风险的前提下提升采样效率，我们开发了简单数据重采样策略。
在训练过程中，我们维护一个简单数据池，存放满分通过率的题目。
执行 rollout 时，以概率 $\alpha$（我们的实验中为 10%）从该简单数据池中采样数据。
这一策略在提升采样效率的同时有效稳定了策略更新，在 RL 训练后期尤为明显。

#### 3.3.3 超参数

在我们的实验中，训练批量大小为 512，actor 的 mini-batch 大小为 32。每次训练迭代执行 16 次梯度更新，学习率为 1e-6。最大序列长度设为 32,768 token 以支持复杂推理任务。训练阶段，temperature 与 top-p 均配置为 1.0，以促进输出多样性。

### 3.4 RL 基础设施

我们开发了无缝 Rollout 引擎并增强了 vLLM 的鲁棒性，以支持高效的基于动态采样的 RL 训练。
我们的 RL 系统构建于 verl（[Sheng et al., 2024](#bib.bib51)）之上，这是一个开源 RL 训练库。
该库使用 Ray（[Moritz et al., 2018](#bib.bib41)）管理计算与通信，在 Ray Actor 中实现 rollout 与训练阶段，并通过 Ray Object 交换训练数据。
尽管 verl 支持多种 RL 算法的灵活实现，但它在 rollout 与奖励计算阶段都存在 GPU 空闲时间。
由于回复长度的偏斜分布，我们观察到大多数 GPU 在等待少数长序列 rollout 工作进程时保持空闲，造成计算资源浪费与训练过程缓慢。
若干先前工作已发现这一问题并提出了系统级方案（[Zhong et al., 2024b](#bib.bib67)；[Team et al., 2025b](#bib.bib56)；[Seed et al., 2025](#bib.bib49)）。
然而，这些方案大多依赖异步训练，会修改底层算法并在长序列回复中引入 staleness。
基于规则的奖励计算同样耗时，对代码数据尤甚，导致宝贵的 GPU 资源出现空闲期。
我们对动态采样的使用在提升样本效率的同时，加剧了 GPU 空闲时间，并在多轮 rollout 中造成样本浪费。
为了同时优化 GPU 利用率并减少样本浪费，我们开发了无缝 Rollout 引擎，在执行异步奖励计算的同时，机会主义地将样本批次填充进 rollout。
我们的系统构建于 vLLM 推理引擎（[Kwon et al., 2023](#bib.bib28)）之上，并与开源社区协作增强了 vLLM「外部启动（external launch）」模式在 verl 框架内的鲁棒性。
此外，我们在 vLLM 中实现了 MTP，以同时支持 MiMo-7B 与 MiMo-7B-RL。

![参见正文](2505.07608v2/seamless_rollout.png)

图 6：MiMo-7B-RL 的无缝 Rollout 引擎概览。

#### 3.4.1 无缝 Rollout 引擎

无缝 Rollout 引擎通过高效的任务调度优化 rollout 工作进程的 GPU 利用率，最大限度减少持续运行期间的空闲时间。
该引擎由以下组件构成：(a) 连续 rollout，(b) 异步奖励计算，(c) 提前终止。
它实现了 2.29 倍的训练加速与 1.96 倍的验证加速。

##### 连续 Rollout

无缝 Rollout 引擎的核心在于主动处理已完成的 rollout 任务并发起新的 rollout。
与将奖励计算推迟到所有 rollout 工作进程完成之后的朴素动态采样实现不同，无缝 Rollout 引擎消除了生成阶段与奖励阶段之间的同步屏障。
它主动监控已完成的工作进程，立即计算其奖励，并按需触发新的 rollout。
计算奖励之后，我们更新有效样本数量与当前步骤的通过率统计，然后在这些统计表明活跃任务不足以满足训练需求时启动新的 rollout 任务。
如图 [6](#S3.F6) 所示，无缝 Rollout 引擎在完成 rollout 任务 ③④①⑥ 后即启动新任务以满足需求；而在完成任务 ②⑤⑦ 之后，它预测进行中的任务已经足够，因而不再调度额外任务。

##### 异步奖励计算

虽然数学数据的奖励计算很快，但评判代码相关数据开销显著，导致 GPU 空闲时间延长。
此外，朴素奖励计算的串行特性无法利用现代处理单元的多进程能力。
为解决这些问题，我们采用 Ray 发起异步奖励计算，便于并发地管理 rollout 与奖励任务。
任务完成后，系统动态地将 rollout 输出转发以进行奖励评估，或汇总结果以更新样本状态，如图 [6](#S3.F6) 所示。
我们为代码专属的奖励计算分配了专用服务器，以避免 rollout 管线出现瓶颈。

##### 提前终止

当有效样本数量超过训练所需的批量大小时，对进行中任务的谨慎管理变得至关重要。
粗暴终止进行中的任务往往会抑制长序列回复的生成，从而可能破坏 RL 训练动态的稳定。
一个直接的解决方案是等待所有活跃任务完成，再从输出中随机采样所需的批次。
然而，若有长序列 rollout 在动态采样阶段临近尾声时启动，这一做法可能延长等待时间。
为在保持数据分布完整性的同时缓解该延迟，我们实施了先进先出的选择策略。
仅当有效样本数量满足批次需求，且早于这些被选样本启动的全部任务都已完成时，我们才终止进行中的任务。
在图 [6](#S3.F6) 中，最后一次 rollout 被中止，因为较早的样本已达到所需批量大小。

| 方法 | 整体加速比 ↑ | Rollout 加速比 ↑ | 归一化 GPU 空闲时间 ↓ | GPU 空闲占比 ↓ | 样本浪费比例 ↓ |
| --- | --- | --- | --- | --- | --- |
| 无动态采样 | 2.45× | 2.82× | 0.36 | 70.8% | / |
| 朴素动态采样 | 1.00× | 1.00× | 1.00 | 69.3% | 22.1% |
| + 连续 Rollout | 1.99× | 2.20× | 0.25 | 38.8% | 13.9% |
| + 异步奖励计算 | 2.09× | 2.34× | 0.21 | 34.0% | 16.4% |
| + 提前终止 | 2.29× | 2.61× | 0.15 | 27.7% | 12.9% |

表 2：
无缝 Rollout 引擎与基线方法的实验结果对比。

##### 实验分析

我们随机选取一段 5 步的训练轨迹来评估无缝 Rollout 引擎的性能。
实验在 256 块 H20 GPU 上进行，结果见表 [2](#S3.T2)。
「整体加速比」衡量端到端 RL 训练效率；「Rollout 加速比」展示 rollout 与奖励任务的加速情况；「归一化 GPU 空闲时间」反映 GPU 空闲的总时长。
上述指标均以朴素动态采样实现为基准归一化。
「GPU 空闲占比」量化 rollout 与奖励计算期间 GPU 不活动的平均比例；「样本浪费比例」表示相对所需批量大小多生成的有效样本比例。
在无缝 Rollout 引擎中，被中止的任务也计入 GPU 空闲时间。

三个组件都贡献了更快的动态采样与更短的 GPU 空闲时间。
尽管不使用动态采样的实验可以获得更高吞吐，但由于大量零梯度训练样本，它带来显著的样本低效。
这些零梯度样本不仅削弱有效训练批量大小，还可能破坏 RL 算法训练动态的稳定性。
鉴于这 5 步实验中的平均样本通过率为 41%，静态采样取得了与朴素动态采样相当的样本效率；后者不训练零梯度数据，但会产生被浪费的样本。
配备全部三个组件后，无缝 Rollout 引擎取得了与静态采样相当的单步训练时间，同时展现出更优的样本效率。
41% 的样本通过率导致朴素实现中 22% 的样本浪费比例；实际中，这一比例在不同情形下可能更大。
通过连续 rollout 与动态启动调度，无缝 Rollout 引擎将样本浪费比例降至 15% 左右。

##### 加速验证

在验证期间，我们可以用无缝 Rollout 引擎直接流式处理 rollout 与奖励任务。
与朴素实现类似，当前我们将验证批量大小设为数据集长度，并同时启动所有 rollout 任务。
我们的实现利用异步奖励计算，实现了 1.96 倍加速，同时将 GPU 空闲时间降至 25%，见表 [3](#S3.T3)。
值得注意的是，实验结果展示了无缝 Rollout 引擎在静态采样上的潜力——静态采样同样只有一遍 rollout 与奖励计算。
若验证数据集足够大，还可以通过优化验证批量大小并采用连续 rollout 获得进一步加速。

| 方法 | 加速比 ↑ | 归一化 GPU 空闲时间 ↓ | GPU 空闲占比 ↓ |
| --- | --- | --- | --- |
| 朴素验证 | 1× | 1 | 65.8% |
| 无缝 Rollout 引擎 | 1.96× | 0.25 | 32.9% |

表 3：
朴素实现与无缝 Rollout 引擎的验证加速与 GPU 空闲时间。实验在 256 块 H20 GPU 上使用我们的完整验证数据集进行。

#### 3.4.2 基于 vLLM 的推理引擎

我们的 RL 系统采用 vLLM（[Kwon et al., 2023](#bib.bib28)）作为推理引擎。
为适配我们模型的新特性，我们为该框架扩展了额外的功能。

##### MTP 支持

如第 [2.2](#S2.SS2) 节所述，我们的模型集成了 MTP 模块以增强性能。
我们已为我们的模型实现并开源了 MTP 支持，使配备 MTP 的架构能够高效推理。

##### 更强的鲁棒性

在 verl 中，vLLM 以外部启动模式部署，在某些场景下可能表现出不稳定。
我们增强了引擎鲁棒性以解决这些问题。
我们在 pre-emption 期间清除前缀缓存中已计算的块，以保持 KVCache 一致性。
我们在增加调度器步数时禁用异步输出处理，以确保兼容性并优化性能。

### 3.5 后训练评测

#### 3.5.1 评测设置

我们在多样的基准上全面评测推理模型：

语言理解与推理：MMLU-Pro（[Wang et al., 2024](#bib.bib59)）。

科学问答：GPQA Diamond（[Rein et al., 2024](#bib.bib47)），取 8 次重复的平均分；SuperGPQA（[Du et al., 2025](#bib.bib11)）。

指令遵循：IFEval（[Zhou et al., 2023](#bib.bib69)），取 8 次重复的平均分。

阅读理解：DROP（[Dua et al., 2019](#bib.bib12)）。

数学推理：MATH500（[Lightman et al., 2024](#bib.bib32)）；AIME 2024（[MAA, 2024](#bib.bib39)）与 AIME 2025（[MAA, 2025](#bib.bib40)），取 32 次重复的平均分。

编程：LiveCodeBench v5（20240801-20250201）（[Jain et al., 2024](#bib.bib25)）与 LiveCodeBench v6（20250201-20250501）（[Jain et al., 2024](#bib.bib25)），取 8 次重复的平均分。

评测期间，我们在所有基准上将采样 temperature 设为 0.6、top-p 设为 0.95。数学推理、编程与科学问答基准的最大生成长度设为 32,768 token，其他基准设为 8,192 token。

我们将 MiMo-7B-RL 与多个强劲基线比较，包括两个非推理模型 GPT-4o-0513、Claude-Sonnet-3.5-1022，以及推理模型 OpenAI-o1-mini、QwQ-32B-Preview、DeepSeek-R1-Distill-Qwen-14B 与 DeepSeek-R1-Distill-Qwen-7B。

| 基准 | GPT-4o-0513 | Claude-3.5-Sonnet-1022 | OpenAI-o1-mini | QwQ-32B-Preview | R1-Distill-Qwen-14B | R1-Distill-Qwen-7B | MiMo-7B-RL |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 通用 | | | | | | | |
| GPQA Diamond (Pass@1) | 49.9 | 65.0 | 60.0 | 54.5 | 59.1 | 49.1 | 54.4 |
| SuperGPQA (Pass@1) | 42.4 | 48.2 | 45.2 | 43.6 | 40.6 | 28.9 | 40.5 |
| DROP (3-shot F1) | 83.7 | 88.3 | 83.9 | 71.2 | 85.5 | 77.0 | 78.7 |
| MMLU-Pro (EM) | 72.6 | 78.0 | 80.3 | 52.0 | 68.8 | 53.5 | 58.6 |
| IF-Eval (Prompt Strict) | 84.3 | 86.5 | 84.8 | 40.4 | 78.3 | 60.5 | 61.0 |
| 数学 | | | | | | | |
| MATH500 (Pass@1) | 74.6 | 78.3 | 90.0 | 90.6 | 93.9 | 92.8 | 95.8 |
| AIME 2024 (Pass@1) | 9.3 | 16.0 | 63.6 | 50.0 | 69.7 | 55.5 | 68.2 |
| AIME 2025 (Pass@1) | 11.6 | 7.4 | 50.7 | 32.4 | 48.2 | 38.8 | 55.4 |
| 编程 | | | | | | | |
| LiveCodeBench v5 (Pass@1) | 32.9 | 38.9 | 53.8 | 41.9 | 53.1 | 37.6 | 57.8 |
| LiveCodeBench v6 (Pass@1) | 30.9 | 37.2 | 46.8 | 39.1 | 31.9 | 23.9 | 49.3 |

表 4：
MiMo-7B-RL 与其他代表性模型的对比。

#### 3.5.2 评测结果

表 [4](#S3.T4) 展示了评测结果。
在数学推理方面，MiMo-7B-RL 在同等参数规模的模型中取得顶尖性能，仅在 AIME 2024 上以微弱差距落后于 DeepSeek-R1-Distill-Qwen-14B。
在算法代码生成任务上，MiMo-7B-RL 的结果极为亮眼。
在 LiveCodeBench v5 上，它显著超越 OpenAI o1-mini；而在最新的 LiveCodeBench v6 上，我们的模型取得 49.3% 的分数，超出 QwQ-32B-Preview 10 分以上，展现出稳健可靠的能力。
值得注意的是，尽管我们的 RL 只纳入了数学与代码问题，MiMo-7B-RL 仍保持了强劲的通用性能，同时超越 QwQ-32B-Preview 与 DeepSeek-R1-Distill-Qwen-7B。

我们还在表 [5](#S3.T5) 中呈现了不同版本 MiMo-7B 的评测结果。
MiMo-7B-RL-Zero 从 MiMo-7B-Base 训练而来，而 MiMo-7B-RL 从 MiMo-7B-SFT 训练而来。
如表所示，从基础模型直接 RL 展现出更强的增长趋势，例如在 AIME 2024 上从 32.9% 起持续攀升。
尽管如此，从 SFT 模型出发的 RL 训练达到了更高的性能上限，在全部评测基准上取得最佳结果。

| 基准 | MiMo-7B-Base | MiMo-7B-RL-Zero | MiMo-7B-SFT | MiMo-7B-RL |
| --- | --- | --- | --- | --- |
| 数学 | | | | |
| MATH500 | 37.4 | 93.6 | 93.0 | 95.8 |
| AIME 2024 | 32.9 | 56.4 | 58.7 | 68.2 |
| AIME 2025 | 24.3 | 46.3 | 44.3 | 55.4 |
| 编程 | | | | |
| LiveCodeBench v5 | 32.9 | 49.1 | 52.3 | 57.8 |
| LiveCodeBench v6 | 29.1 | 42.9 | 45.5 | 49.3 |

表 5：
MiMo 系列模型在数学与编程基准上的评测结果。

### 3.6 讨论

在本节中，我们分享在探索 MiMo-7B 后训练过程中的洞见与观察，希望惠及研究社区。

图 7：
RL 过程中三个 MiMo 模型变体的性能对比。

##### 面向格式对齐的 SFT

在从 MiMo-7B-Base 出发的 RL 训练初始阶段，我们观察到模型主要在学习适应答案抽取函数，例如数学问题的 “\boxed{}”。
因此，我们研究了一种「轻量」SFT，帮助基础模型对齐到期望的答案格式。
然而，如图 [7](#S3.F7) 所示，所得的 MiMo-7B-RL-LiteSFT 模型在推理潜能与最终表现上均告失败。
虽然 MiMo-7B-RL-LiteSFT 起步性能高于 MiMo-7B-RL-Zero，但仅 500 步之后就落后于基础模型的轨迹。
此外，与经历了「更重」SFT 的 MiMo-7B-RL 相比，MiMo-7B-RL-LiteSFT 展现出相似的增长趋势，但由于起点较差而显著落后，最终导致更差的收官成绩。

##### 不同领域之间的干扰

在从 MiMo-7B-Base 出发的 RL 训练后期阶段，在数学与编程任务之间维持性能平衡颇具挑战。
在训练第 2000 到 2500 步之间，模型在代码问题上持续进步，而数学推理任务的表现则出现波动与下滑。
相比之下，在冷启动 SFT 模型上的 RL 训练在两个领域均表现出一致的提升。
对模型输出的分析揭示，基础模型凭借其强大的探索能力，倾向于在数学问题上钻奖励的空子。
而对代码问题而言，基于测试用例的验证器使奖励钻营难得多。
这凸显了高质量数学题集对确保稳健 RL 训练的关键意义。

##### 语言混杂惩罚

与 DeepSeek-R1-Zero 一样，我们也在 MiMo-7B-Base 的 RL 训练中观察到语言混杂问题。
为缓解该问题，我们在奖励函数中引入语言混杂惩罚。
然而我们发现，设计这样的惩罚函数颇具挑战。
在英文回复中检测中文字符很容易，反方向则困难得多，因为数学公式与代码本身就包含英文单词。
结果，该惩罚不仅未能完全解决语言混杂，还引入了奖励黑客的风险，例如无论问题语言如何总是生成英文回复。

##### SFT 数据规模扩展的影响

在初步实验的基础上，我们的研究将 SFT 数据集从约 50 万条显著扩展到 600 万条。我们实证观察到，SFT 数据的这一大规模扩充，使模型的推理能力与通用对话能力均获得显著提升，且未损害其后续 RL 的潜力。如表 [6](#S3.T6) 所示，使用 600 万条 SFT 数据训练的模型，在数学推理、代码推理、科学推理与通用对话能力等方面，均较使用 50 万条数据训练的对应模型取得长足进步。重要的是，在这一增强 SFT 阶段之后再进行 RL 微调的模型，同样表现出持续的性能提升。

| 基准 | MiMo-7B-SFT-500K | MiMo-7B-SFT-6M | MiMo-7B-RL | MiMo-7B-RL-0530 |
| --- | --- | --- | --- | --- |
| AIME 24 | 58.7 | 68.3 | 68.2 | 80.1 |
| AIME 25 | 44.3 | 50.9 | 55.4 | 70.2 |
| MATH500 | 93.0 | 94.8 | 95.8 | 97.2 |
| GPQA Diamond | 50.7 | 54.1 | 54.4 | 60.6 |
| LiveCodeBench v5 | 52.3 | 53.4 | 57.8 | 60.9 |
| Alignbench v1.1 | 6.7 | 7.1 | 6.9 | 7.4 |

表 6：各基准上的模型性能对比。
MiMo-7B-RL-0530 在其训练长度 48K 上下文长度下评测，而其余三个模型在其 32K 训练上下文长度下评测。Alignbench v1.1 [Liu et al. (2024b)](#bib.bib36) 的评测以 GPT-4.1 作为评判模型。

##### 扩展生成预算的 On-Policy RL

我们先前的实证研究表明，GRPO 的朴素实现极易出现性能过早饱和。为缓解这一问题，我们采用 on-policy RL 算法，与 MiMo-VL-7B-RL [Team et al. (2025a)](#bib.bib54) 所用的方法一脉相承。on-policy RL 的训练被证明极为稳定，同时使模型效果在整个学习过程中持续增长。进一步延展我们的发现：在 on-policy RL 训练期间持续提高生成长度预算，能持续推升模型性能。具体而言，我们的 RL 训练方案将模型生成长度从 32K 系统性地提升到 38K，随后提升到 48K。生成预算的这一渐进式扩展，对我们的 7B 模型最终在数学推理上达到与 Deepseek-R1 相当的水平起到了关键作用。MiMo-7B-RL-0530 模型已经开源并公开可用11
1
https://huggingface.co/XiaomiMiMo/MiMo-7B-RL-0530。

图 8：MiMo-7B-RL-0530 在 AIME24 上的性能曲线。

## 4 结论

本工作推出 MiMo-7B，一系列通过优化的预训练与后训练流程解锁先进推理能力的 LLM。
在预训练中接触多样的推理模式后，MiMo-7B-Base 具备卓越的推理潜能，超越规模显著更大的模型。
在后训练中，凭借我们稳健高效的 RL 框架，我们训练了 MiMo-7B-RL-Zero 与 MiMo-7B-RL，它们在数学、代码与通用任务上展现出卓越的推理能力。
我们希望本工作能为开发更强大的推理模型提供洞见。

## 参考文献

- Ainslie et al. (2023)

  J. Ainslie, J. Lee-Thorp, M. de Jong, Y. Zemlyanskiy, F. Lebron, and S. Sanghai.
  GQA: Training generalized multi-query transformer models from multi-head checkpoints.
  In H. Bouamor, J. Pino, and K. Bali, editors, *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 4895–4901, Singapore, 2023. Association for Computational Linguistics.
  [10.18653/v1/2023.emnlp-main.298](https://doi.org/10.18653/v1/2023.emnlp-main.298).
  URL <https://aclanthology.org/2023.emnlp-main.298>.
- Anthropic (2025)

  Anthropic.
  Claude 3.7 sonnet and claude code, 2025.
  URL <https://www.anthropic.com/claude/sonnet>.
- Austin et al. (2021)

  J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, et al.
  Program synthesis with large language models.
  *ArXiv preprint*, abs/2108.07732, 2021.
  URL <https://arxiv.org/abs/2108.07732>.
- Barbaresi (2021)

  A. Barbaresi.
  Trafilatura: A web scraping library and command-line tool for text discovery and extraction.
  In H. Ji, J. C. Park, and R. Xia, editors, *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations*, pages 122–131, Online, 2021. Association for Computational Linguistics.
  [10.18653/v1/2021.acl-demo.15](https://doi.org/10.18653/v1/2021.acl-demo.15).
  URL <https://aclanthology.org/2021.acl-demo.15>.
- Bisk et al. (2020)

  Y. Bisk, R. Zellers, R. LeBras, J. Gao, and Y. Choi.
  PIQA: reasoning about physical commonsense in natural language.
  In *The Thirty-Fourth AAAI Conference on Artificial Intelligence, AAAI 2020, The Thirty-Second Innovative Applications of Artificial Intelligence Conference, IAAI 2020, The Tenth AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI 2020, New York, NY, USA, February 7-12, 2020*, pages 7432–7439. AAAI Press, 2020.
  URL <https://aaai.org/ojs/index.php/AAAI/article/view/6239>.
- Broder (1997)

  A. Z. Broder.
  On the resemblance and containment of documents.
  In *Proceedings. Compression and Complexity of SEQUENCES 1997 (Cat. No. 97TB100171)*, pages 21–29. IEEE, 1997.
- Chen et al. (2021)

  M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al.
  Evaluating large language models trained on code.
  *ArXiv preprint*, abs/2107.03374, 2021.
  URL <https://arxiv.org/abs/2107.03374>.
- Clark et al. (2018)

  P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord.
  Think you have solved question answering? try arc, the ai2 reasoning challenge.
  *ArXiv preprint*, abs/1803.05457, 2018.
  URL <https://arxiv.org/abs/1803.05457>.
- Cobbe et al. (2021)

  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  *ArXiv preprint*, abs/2110.14168, 2021.
  URL <https://arxiv.org/abs/2110.14168>.
- Dauphin et al. (2017)

  Y. N. Dauphin, A. Fan, M. Auli, and D. Grangier.
  Language modeling with gated convolutional networks.
  In D. Precup and Y. W. Teh, editors, *Proceedings of the 34th International Conference on Machine Learning, ICML 2017, Sydney, NSW, Australia, 6-11 August 2017*, volume 70 of *Proceedings of Machine Learning Research*, pages 933–941. PMLR, 2017.
  URL <http://proceedings.mlr.press/v70/dauphin17a.html>.
- Du et al. (2025)

  X. Du, Y. Yao, K. Ma, B. Wang, T. Zheng, K. Zhu, M. Liu, Y. Liang, X. Jin, Z. Wei, et al.
  Supergpqa: Scaling llm evaluation across 285 graduate disciplines.
  *ArXiv preprint*, abs/2502.14739, 2025.
  URL <https://arxiv.org/abs/2502.14739>.
- Dua et al. (2019)

  D. Dua, Y. Wang, P. Dasigi, G. Stanovsky, S. Singh, and M. Gardner.
  DROP: A reading comprehension benchmark requiring discrete reasoning over paragraphs.
  In J. Burstein, C. Doran, and T. Solorio, editors, *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, pages 2368–2378, Minneapolis, Minnesota, 2019. Association for Computational Linguistics.
  [10.18653/v1/N19-1246](https://doi.org/10.18653/v1/N19-1246).
  URL <https://aclanthology.org/N19-1246>.
- Gema et al. (2024)

  A. P. Gema, J. O. J. Leang, G. Hong, A. Devoto, A. C. M. Mancino, R. Saxena, X. He, Y. Zhao, X. Du, M. R. G. Madani, et al.
  Are we done with mmlu?
  *ArXiv preprint*, abs/2406.04127, 2024.
  URL <https://arxiv.org/abs/2406.04127>.
- Gloeckle et al. (2024)

  F. Gloeckle, B. Y. Idrissi, B. Rozière, D. Lopez-Paz, and G. Synnaeve.
  Better & faster large language models via multi-token prediction.
  In *Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024*. OpenReview.net, 2024.
  URL <https://openreview.net/forum?id=pEWAcejiU2>.
- Grattafiori et al. (2024)

  A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Vaughan, et al.
  The llama 3 herd of models.
  *ArXiv preprint*, abs/2407.21783, 2024.
  URL <https://arxiv.org/abs/2407.21783>.
- Gu et al. (2024)

  A. Gu, B. Rozière, H. J. Leather, A. Solar-Lezama, G. Synnaeve, and S. Wang.
  Cruxeval: A benchmark for code reasoning, understanding and execution.
  In *Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024*. OpenReview.net, 2024.
  URL <https://openreview.net/forum?id=Ffpg52swvg>.
- Guo et al. (2025)

  D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
  *ArXiv preprint*, abs/2501.12948, 2025.
  URL <https://arxiv.org/abs/2501.12948>.
- He et al. (2025)

  J. He, J. Liu, C. Y. Liu, R. Yan, C. Wang, P. Cheng, X. Zhang, F. Zhang, J. Xu, W. Shen, S. Li, L. Zeng, T. Wei, C. Cheng, B. An, Y. Liu, and Y. Zhou.
  Skywork open reasoner series.
  <https://capricious-hydrogen-41c.notion.site/Skywork-Open-Reaonser-Series-1d0bc9ae823a80459b46c149e4f51680>, 2025.
  Notion Blog.
- Hendrycks et al. (2021a)

  D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt.
  Measuring massive multitask language understanding.
  In *9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021*. OpenReview.net, 2021a.
  URL <https://openreview.net/forum?id=d7KBjmI3GmQ>.
- Hendrycks et al. (2021b)

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *ArXiv preprint*, abs/2103.03874, 2021b.
  URL <https://arxiv.org/abs/2103.03874>.
- Hsieh et al. (2024)

  C.-P. Hsieh, S. Sun, S. Kriman, S. Acharya, D. Rekesh, F. Jia, Y. Zhang, and B. Ginsburg.
  Ruler: What’s the real context size of your long-context language models?
  *ArXiv preprint*, abs/2404.06654, 2024.
  URL <https://arxiv.org/abs/2404.06654>.
- Hu et al. (2025)

  J. Hu, Y. Zhang, Q. Han, D. Jiang, X. Zhang, and H.-Y. Shum.
  Open-reasoner-zero: An open source approach to scaling up reinforcement learning on the base model.
  *ArXiv preprint*, abs/2503.24290, 2025.
  URL <https://arxiv.org/abs/2503.24290>.
- Huang et al. (2023)

  Y. Huang, Y. Bai, Z. Zhu, J. Zhang, J. Zhang, T. Su, J. Liu, C. Lv, Y. Zhang, J. Lei, Y. Fu, M. Sun, and J. He.
  C-eval: A multi-level multi-discipline chinese evaluation suite for foundation models.
  In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, *Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023*, 2023.
  URL <http://papers.nips.cc/paper_files/paper/2023/hash/c6ec1844bec96d6d32ae95ae694e23d8-Abstract-Datasets_and_Benchmarks.html>.
- IOI (2024)

  IOI.
  International olympiad in informatics, 2024.
  URL <https://ioinformatics.org/>.
- Jain et al. (2024)

  N. Jain, K. Han, A. Gu, W.-D. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica.
  Livecodebench: Holistic and contamination free evaluation of large language models for code.
  *ArXiv preprint*, abs/2403.07974, 2024.
  URL <https://arxiv.org/abs/2403.07974>.
- Joshi et al. (2017)

  M. Joshi, E. Choi, D. Weld, and L. Zettlemoyer.
  TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension.
  In R. Barzilay and M.-Y. Kan, editors, *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 1601–1611, Vancouver, Canada, 2017. Association for Computational Linguistics.
  [10.18653/v1/P17-1147](https://doi.org/10.18653/v1/P17-1147).
  URL <https://aclanthology.org/P17-1147>.
- Kwiatkowski et al. (2019)

  T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, A. Parikh, C. Alberti, D. Epstein, I. Polosukhin, J. Devlin, K. Lee, K. Toutanova, L. Jones, M. Kelcey, M.-W. Chang, A. M. Dai, J. Uszkoreit, Q. Le, and S. Petrov.
  Natural questions: A benchmark for question answering research.
  *Transactions of the Association for Computational Linguistics*, 7:452–466, 2019.
  [10.1162/tacl_a_00276](https://doi.org/10.1162/tacl_a_00276).
  URL <https://aclanthology.org/Q19-1026>.
- Kwon et al. (2023)

  W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. Gonzalez, H. Zhang, and I. Stoica.
  Efficient memory management for large language model serving with pagedattention.
  In *Proceedings of the 29th Symposium on Operating Systems Principles*, pages 611–626, 2023.
- Lai et al. (2017)

  G. Lai, Q. Xie, H. Liu, Y. Yang, and E. Hovy.
  RACE: Large-scale ReAding comprehension dataset from examinations.
  In M. Palmer, R. Hwa, and S. Riedel, editors, *Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing*, pages 785–794, Copenhagen, Denmark, 2017. Association for Computational Linguistics.
  [10.18653/v1/D17-1082](https://doi.org/10.18653/v1/D17-1082).
  URL <https://aclanthology.org/D17-1082>.
- Leviathan et al. (2023)

  Y. Leviathan, M. Kalman, and Y. Matias.
  Fast inference from transformers via speculative decoding.
  In A. Krause, E. Brunskill, K. Cho, B. Engelhardt, S. Sabato, and J. Scarlett, editors, *International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA*, volume 202 of *Proceedings of Machine Learning Research*, pages 19274–19286. PMLR, 2023.
  URL <https://proceedings.mlr.press/v202/leviathan23a.html>.
- Li et al. (2023)

  H. Li, Y. Zhang, F. Koto, Y. Yang, H. Zhao, Y. Gong, N. Duan, and T. Baldwin.
  Cmmlu: Measuring massive multitask language understanding in chinese.
  *ArXiv preprint*, abs/2306.09212, 2023.
  URL <https://arxiv.org/abs/2306.09212>.
- Lightman et al. (2024)

  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe.
  Let’s verify step by step.
  In *The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024*. OpenReview.net, 2024.
  URL <https://openreview.net/forum?id=v8L0pN6EOi>.
- Liu et al. (2024a)

  A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, et al.
  Deepseek-v3 technical report.
  *ArXiv preprint*, abs/2412.19437, 2024a.
  URL <https://arxiv.org/abs/2412.19437>.
- Liu et al. (2023)

  J. Liu, C. S. Xia, Y. Wang, and L. Zhang.
  Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation.
  In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, *Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023*, 2023.
  URL <http://papers.nips.cc/paper_files/paper/2023/hash/43e9d647ccd3e4b7b5baab53f0368686-Abstract-Conference.html>.
- Liu et al. (2025)

  J. Liu, D. Zhu, Z. Bai, Y. He, H. Liao, H. Que, Z. Wang, C. Zhang, G. Zhang, J. Zhang, et al.
  A comprehensive survey on long context language modeling.
  *ArXiv preprint*, abs/2503.17407, 2025.
  URL <https://arxiv.org/abs/2503.17407>.
- Liu et al. (2024b)

  X. Liu, X. Lei, S. Wang, Y. Huang, Z. Feng, B. Wen, J. Cheng, P. Ke, Y. Xu, W. L. Tam, X. Zhang, L. Sun, X. Gu, H. Wang, J. Zhang, M. Huang, Y. Dong, and J. Tang.
  Alignbench: Benchmarking chinese alignment of large language models, 2024b.
  URL <https://arxiv.org/abs/2311.18743>.
- Liu et al. (2024c)

  Y. Liu, R. Jin, L. Shi, Z. Yao, and D. Xiong.
  Finemath: A fine-grained mathematical evaluation benchmark for chinese large language models.
  *ArXiv preprint*, abs/2403.07747, 2024c.
  URL <https://arxiv.org/abs/2403.07747>.
- Loshchilov and Hutter (2019)

  I. Loshchilov and F. Hutter.
  Decoupled weight decay regularization.
  In *7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019*. OpenReview.net, 2019.
  URL <https://openreview.net/forum?id=Bkg6RiCqY7>.
- MAA (2024)

  MAA.
  American invitational mathematics examination - aime.
  In *American Invitational Mathematics Examination - AIME*, 2024.
  URL <https://maa.org/math-competitions/american-invitational-mathematics-examination-aime>.
- MAA (2025)

  MAA.
  American invitational mathematics examination - aime.
  In *American Invitational Mathematics Examination - AIME*, 2025.
  URL <https://maa.org/math-competitions/american-invitational-mathematics-examination-aime>.
- Moritz et al. (2018)

  P. Moritz, R. Nishihara, S. Wang, A. Tumanov, R. Liaw, E. Liang, M. Elibol, Z. Yang, W. Paul, M. I. Jordan, et al.
  Ray: A distributed framework for emerging {\{AI}\} applications.
  In *13th USENIX symposium on operating systems design and implementation (OSDI 18)*, pages 561–577, 2018.
- OpenAI (2024)

  OpenAI.
  Learning to reason with llms, 2024.
  URL <https://openai.com/index/learning-to-reason-with-llms/>.
- Paster et al. (2024)

  K. Paster, M. D. Santos, Z. Azerbayev, and J. Ba.
  Openwebmath: An open dataset of high-quality mathematical web text.
  In *The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024*. OpenReview.net, 2024.
  URL <https://openreview.net/forum?id=jKHmjlpViu>.
- Penedo et al. (2023)

  G. Penedo, Q. Malartic, D. Hesslow, R. Cojocaru, A. Cappelli, H. Alobeidli, B. Pannier, E. Almazrouei, and J. Launay.
  The refinedweb dataset for falcon llm: outperforming curated corpora with web data, and web data only.
  *ArXiv preprint*, abs/2306.01116, 2023.
  URL <https://arxiv.org/abs/2306.01116>.
- Penedo et al. (2024)

  G. Penedo, H. Kydlícek, L. B. Allal, A. Lozhkov, M. Mitchell, C. A. Raffel, L. von Werra, and T. Wolf.
  The fineweb datasets: Decanting the web for the finest text data at scale.
  In A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, editors, *Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024*, 2024.
  URL <http://papers.nips.cc/paper_files/paper/2024/hash/370df50ccfdf8bde18f8f9c2d9151bda-Abstract-Datasets_and_Benchmarks_Track.html>.
- Radford et al. (2018)

  A. Radford, K. Narasimhan, T. Salimans, I. Sutskever, et al.
  Improving language understanding by generative pre-training.
  *OpenAI*, 2018.
- Rein et al. (2024)

  D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman.
  Gpqa: A graduate-level google-proof q&a benchmark.
  In *First Conference on Language Modeling*, 2024.
- Sakaguchi et al. (2020)

  K. Sakaguchi, R. L. Bras, C. Bhagavatula, and Y. Choi.
  Winogrande: An adversarial winograd schema challenge at scale.
  In *The Thirty-Fourth AAAI Conference on Artificial Intelligence, AAAI 2020, The Thirty-Second Innovative Applications of Artificial Intelligence Conference, IAAI 2020, The Tenth AAAI Symposium on Educational Advances in Artificial Intelligence, EAAI 2020, New York, NY, USA, February 7-12, 2020*, pages 8732–8740. AAAI Press, 2020.
  URL <https://aaai.org/ojs/index.php/AAAI/article/view/6399>.
- Seed et al. (2025)

  B. Seed, Y. Yuan, Y. Yue, M. Wang, X. Zuo, J. Chen, L. Yan, W. Xu, C. Zhang, X. Liu, et al.
  Seed-thinking-v1. 5: Advancing superb reasoning models with reinforcement learning.
  *ArXiv preprint*, abs/2504.13914, 2025.
  URL <https://arxiv.org/abs/2504.13914>.
- Shao et al. (2024)

  Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
  Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
  *ArXiv preprint*, abs/2402.03300, 2024.
  URL <https://arxiv.org/abs/2402.03300>.
- Sheng et al. (2024)

  G. Sheng, C. Zhang, Z. Ye, X. Wu, W. Zhang, R. Zhang, Y. Peng, H. Lin, and C. Wu.
  Hybridflow: A flexible and efficient rlhf framework.
  *ArXiv preprint*, abs/2409.19256, 2024.
  URL <https://arxiv.org/abs/2409.19256>.
- Su et al. (2024)

  J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu.
  Roformer: Enhanced transformer with rotary position embedding.
  *Neurocomputing*, 568:127063, 2024.
- Suzgun et al. (2023)

  M. Suzgun, N. Scales, N. Schärli, S. Gehrmann, Y. Tay, H. W. Chung, A. Chowdhery, Q. Le, E. Chi, D. Zhou, and J. Wei.
  Challenging BIG-bench tasks and whether chain-of-thought can solve them.
  In A. Rogers, J. Boyd-Graber, and N. Okazaki, editors, *Findings of the Association for Computational Linguistics: ACL 2023*, pages 13003–13051, Toronto, Canada, 2023. Association for Computational Linguistics.
  [10.18653/v1/2023.findings-acl.824](https://doi.org/10.18653/v1/2023.findings-acl.824).
  URL <https://aclanthology.org/2023.findings-acl.824>.
- Team et al. (2025a)

  C. Team, Z. Yue, Z. Lin, Y. Song, W. Wang, S. Ren, S. Gu, S. Li, P. Li, L. Zhao, L. Li, K. Bao, H. Tian, H. Zhang, G. Wang, D. Zhu, Cici, C. He, B. Ye, B. Shen, Z. Zhang, Z. Jiang, Z. Zheng, Z. Song, Z. Luo, Y. Yu, Y. Wang, Y. Tian, Y. Tu, Y. Yan, Y. Huang, X. Wang, X. Xu, X. Song, X. Zhang, X. Yong, X. Zhang, X. Deng, W. Yang, W. Ma, W. Lv, W. Zhuang, W. Liu, S. Deng, S. Liu, S. Chen, S. Yu, S. Liu, S. Wang, R. Ma, Q. Wang, P. Wang, N. Chen, M. Zhu, K. Zhou, K. Zhou, K. Fang, J. Shi, J. Dong, J. Xiao, J. Xu, H. Liu, H. Xu, H. Qu, H. Zhao, H. Lv, G. Wang, D. Zhang, D. Zhang, D. Zhang, C. Ma, C. Liu, C. Cai, and B. Xia.
  Mimo-vl technical report, 2025a.
  URL <https://arxiv.org/abs/2506.03569>.
- Team (2024)

  G. Team.
  Gemma 2: Improving open language models at a practical size, 2024.
  URL <https://arxiv.org/abs/2408.00118>.
- Team et al. (2025b)

  K. Team, A. Du, B. Gao, B. Xing, C. Jiang, C. Chen, C. Li, C. Xiao, C. Du, C. Liao, et al.
  Kimi k1. 5: Scaling reinforcement learning with llms.
  *ArXiv preprint*, abs/2501.12599, 2025b.
  URL <https://arxiv.org/abs/2501.12599>.
- Touvron et al. (2023)

  H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, et al.
  Llama 2: Open foundation and fine-tuned chat models.
  *ArXiv preprint*, abs/2307.09288, 2023.
  URL <https://arxiv.org/abs/2307.09288>.
- Vaswani et al. (2017)

  A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin.
  Attention is all you need.
  In I. Guyon, U. von Luxburg, S. Bengio, H. M. Wallach, R. Fergus, S. V. N. Vishwanathan, and R. Garnett, editors, *Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA*, pages 5998–6008, 2017.
  URL <https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html>.
- Wang et al. (2024)

  Y. Wang, X. Ma, G. Zhang, Y. Ni, A. Chandra, S. Guo, W. Ren, A. Arulraj, X. He, Z. Jiang, T. Li, M. Ku, K. Wang, A. Zhuang, R. Fan, X. Yue, and W. Chen.
  Mmlu-pro: A more robust and challenging multi-task language understanding benchmark.
  In A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, editors, *Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024*, 2024.
  URL <http://papers.nips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html>.
- Xia et al. (2023)

  H. Xia, T. Ge, P. Wang, S.-Q. Chen, F. Wei, and Z. Sui.
  Speculative decoding: Exploiting speculative execution for accelerating seq2seq generation.
  In H. Bouamor, J. Pino, and K. Bali, editors, *Findings of the Association for Computational Linguistics: EMNLP 2023*, pages 3909–3925, Singapore, 2023. Association for Computational Linguistics.
  [10.18653/v1/2023.findings-emnlp.257](https://doi.org/10.18653/v1/2023.findings-emnlp.257).
  URL <https://aclanthology.org/2023.findings-emnlp.257>.
- Yang et al. (2024)

  A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, et al.
  Qwen2. 5 technical report.
  *ArXiv preprint*, abs/2412.15115, 2024.
  URL <https://arxiv.org/abs/2412.15115>.
- Yu et al. (2025)

  Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, T. Fan, G. Liu, L. Liu, X. Liu, et al.
  Dapo: An open-source llm reinforcement learning system at scale.
  *ArXiv preprint*, abs/2503.14476, 2025.
  URL <https://arxiv.org/abs/2503.14476>.
- Yue et al. (2025)

  Y. Yue, Z. Chen, R. Lu, A. Zhao, Z. Wang, Y. Yue, S. Song, and G. Huang.
  Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model?, 2025.
  URL <https://arxiv.org/abs/2504.13837>.
- Zellers et al. (2019)

  R. Zellers, A. Holtzman, Y. Bisk, A. Farhadi, and Y. Choi.
  HellaSwag: Can a machine really finish your sentence?
  In A. Korhonen, D. Traum, and L. Màrquez, editors, *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, pages 4791–4800, Florence, Italy, 2019. Association for Computational Linguistics.
  [10.18653/v1/P19-1472](https://doi.org/10.18653/v1/P19-1472).
  URL <https://aclanthology.org/P19-1472>.
- Zhang and Sennrich (2019)

  B. Zhang and R. Sennrich.
  Root mean square layer normalization.
  In H. M. Wallach, H. Larochelle, A. Beygelzimer, F. d’Alché-Buc, E. B. Fox, and R. Garnett, editors, *Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada*, pages 12360–12371, 2019.
  URL <https://proceedings.neurips.cc/paper/2019/hash/1e8a19426224ca89e83cef47f1e7f53b-Abstract.html>.
- Zhong et al. (2024a)

  W. Zhong, R. Cui, Y. Guo, Y. Liang, S. Lu, Y. Wang, A. Saied, W. Chen, and N. Duan.
  AGIEval: A human-centric benchmark for evaluating foundation models.
  In K. Duh, H. Gomez, and S. Bethard, editors, *Findings of the Association for Computational Linguistics: NAACL 2024*, pages 2299–2314, Mexico City, Mexico, 2024a. Association for Computational Linguistics.
  URL <https://aclanthology.org/2024.findings-naacl.149>.
- Zhong et al. (2024b)

  Y. Zhong, Z. Zhang, B. Wu, S. Liu, Y. Chen, C. Wan, H. Hu, L. Xia, R. Ming, Y. Zhu, et al.
  Rlhfuse: Efficient rlhf training for large language models with inter-and intra-stage fusion.
  *ArXiv preprint*, abs/2409.13221, 2024b.
  URL <https://arxiv.org/abs/2409.13221>.
- Zhou et al. (2025)

  F. Zhou, Z. Wang, N. Ranjan, Z. Cheng, L. Tang, G. He, Z. Liu, and E. P. Xing.
  Megamath: Pushing the limits of open math corpora.
  *ArXiv preprint*, abs/2504.02807, 2025.
  URL <https://arxiv.org/abs/2504.02807>.
- Zhou et al. (2023)

  J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and L. Hou.
  Instruction-following evaluation for large language models, 2023.
  URL <https://arxiv.org/abs/2311.07911>.
- Zhu et al. (2024)

  Q. Zhu, D. Guo, Z. Shao, D. Yang, P. Wang, R. Xu, Y. Wu, Y. Li, H. Gao, S. Ma, et al.
  Deepseek-coder-v2: Breaking the barrier of closed-source models in code intelligence.
  *ArXiv preprint*, abs/2406.11931, 2024.
  URL <https://arxiv.org/abs/2406.11931>.

## 附录 A 贡献与致谢

我们谨向所有贡献者致以诚挚谢意，包括未在论文中列名者，感谢他们宝贵的支持与付出。各角色内的作者按名字字母顺序列出。

核心贡献者
  
 Bingquan Xia
  
 Bowen Shen
  
 Cici
  
 Dawei Zhu
  
 Di Zhang
  
 Gang Wang
  
 Hailin Zhang
  
 Huaqiu Liu
  
 Jiebao Xiao
  
 Jinhao Dong
  
 Liang Zhao
  
 Peidian Li
  
 Peng Wang
  
 Shihua Yu
  
 Shimao Chen
  
 Weikun Wang
  
 Wenhan Ma
  
 Xiangwei Deng
  
 Yi Huang
  
 Yifan Song
  
 Zihan Jiang

贡献者
  
Bowen Ye
  
 Can Cai
  
 Chenhong He
  
 Dong Zhang
  
 Duo Zhang
  
 Guoan Wang
  
 Hao Tian
  
 Haochen Zhao
  
 Heng Qu
  
 Hongshen Xu
  
 Jun Shi
  
 Kainan Bao
  
 Kai Fang
  
 Kang Zhou
  
 Kangyang Zhou
  
 Lei Li
  
 Menghang Zhu
  
 Nuo Chen
  
 Qiantong Wang
  
 Shaohui Liu
  
 Shicheng Li
  
 Shuhao Gu
  
 Shuhuai Ren
  
 Shuo Liu
  
 Sirui Deng
  
 Weiji Zhuang
  
 Weiwei Lv
  
 Wenyu Yang
  
 Xin Zhang
  
 Xing Yong
  
 Xing Zhang
  
 Xingchen Song
  
 Xinzhe Xu
  
 Xu Wang
  
 Yihan Yan
  
 Yu Tu
  
 Yuanyuan Tian
  
 Yudong Wang
  
 Yue Yu
  
 Zhenru Lin
  
 Zhichao Song
  
 Zihao Yue

---
title: "GLM-4.5：智能体、推理与编码（ARC）基础模型"
title_en: "GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models"
arxiv: 2508.06471
date: 2025-08-08
source: https://arxiv.org/abs/2508.06471
crawled: 2026-09-22
translated: 2026-09-22
---

# GLM-4.5：智能体、推理与编码（ARC）基础模型

> 原文：[GLM-4.5](https://arxiv.org/abs/2508.06471) · 智谱 Z.ai arXiv

GLM-4.5 团队

机构：智谱 AI（Zhipu AI）与清华大学

机构：（完整作者名单请参阅第 6 节「贡献」部分）

###### 摘要

我们发布 GLM-4.5，一个开源的专家混合（MoE）大语言模型，总参数量为 355B、激活参数量为 32B，采用同时支持思考模式与直接响应模式的混合推理方法。经过在 23T token 上的多阶段训练，以及包含专家模型迭代与强化学习在内的全面后训练，GLM-4.5 在智能体、推理与编码（ARC）任务上取得了强劲表现：在 TAU-Bench 上得分 70.1%，在 AIME 24 上得分 91.0%，在 SWE-bench Verified 上得分 64.2%。GLM-4.5 的参数量远少于多个竞争模型，在所有被评测模型中总排名第三，在智能体基准上排名第二。我们同时发布 GLM-4.5（355B 参数）与紧凑版本 GLM-4.5-Air（106B 参数），以推动推理与智能体 AI 系统的研究。代码、模型及更多信息见 <https://github.com/zai-org/GLM-4.5>。

![图 1](2508.06471v1/arc_benchmark.png)

图 1：智能体、推理与编码（ARC）基准的平均性能。总体而言，GLM-4.5 位列第 3 名，GLM-4.5-Air 紧随其后位列第 6 名。所列模型的评测结果截至 2025 年 7 月 28 日。

## 1 引言

大语言模型（LLM）正在从通用知识库 [6; 37; 50; 33; 23] 快速演变为通用问题求解器。其终极愿景——通常与通用人工智能（AGI）相关联——是创造出在多样领域具备人类水平认知能力的模型。这要求对复杂问题求解、泛化与自我改进的统一掌握，从而超越面向特定任务的卓越表现。

随着 LLM 日益融入真实世界场景，提升实际生产力、解决复杂专业任务的关键在于发展特定的核心能力。我们识别出三项相互关联的关键能力，作为衡量真正通用模型的标尺：与外部工具及现实世界交互的智能体（agentic）能力；求解数学、科学等领域多步问题的复杂推理能力；以及应对真实世界软件工程任务的高级编码技能。尽管 OpenAI 的 o1/o3 [18] 与 Anthropic 的 Claude Sonnet 4 等最先进的专有模型已在特定 ARC 领域（如数学推理或代码修复 [20]）展现出突破性表现，但一个在全部三个方面均表现出色的强大开源模型至今仍然缺位。

本文介绍两个新模型：GLM-4.5 与 GLM-4.5-Air，朝着统一所有这些不同能力的目标迈进。新模型全面超越现有开源 LLM [13; 34; 47]，在智能体、推理与编码任务上取得显著提升。GLM-4.5 与 GLM-4.5-Air 均具备混合推理模式：面向复杂推理与智能体任务的思考模式，以及面向即时响应的非思考模式。GLM-4.5 是我们的首个 MoE 模型，总参数量为 355B，激活参数量为 32B。GLM-4.5 在以下 ARC 基准上展现出强劲表现：

- 智能体：GLM-4.5 在 TAU-Bench 上得分 70.1%，在 BFCL v3 [26] 上得分 77.8%，与 Claude Sonnet 4 相当。在网页浏览智能体方面，GLM-4.5 在 BrowseComp [45] 上得分 26.4%，明显优于 Claude Opus 4（18.8%），接近 o4-mini-high（28.3%）。
- 推理：GLM-4.5 在一系列高难度推理基准上表现出色，在 AIME 24 上取得 91.0%，在 GPQA [30] 上取得 79.1%，在 LiveCodeBench（2407-2501）[19] 上取得 72.9%，在 HLE（Humanity's Last Exam）[28] 上取得 14.4%。
- 编码：GLM-4.5 在 SWE-bench Verified [20] 上得分 64.2%，在 Terminal-Bench [35] 上得分 37.5%，优于 GPT-4.1 与 Gemini-2.5-pro，接近 Claude Sonnet 4。

GLM-4.5-Air 是一个更小的 MoE 模型，参数量为 106B。它在 100B 规模的模型中实现了显著飞跃，匹敌或超越 Qwen3-235B-A22B [47] 与 MiniMax-M1 [7]。

在图 1 中，我们展示了 12 项智能体、推理与编码（ARC）任务基准上的平均性能。总体而言，GLM-4.5 排名第 3，GLM-4.5-Air 排名第 6。在智能体任务上，GLM-4.5 排名第 2，仅次于 OpenAI o3。在编码任务上，GLM-4.5 排名第 3，接近 Claude Sonnet 4。值得注意的是，GLM-4.5 的参数效率很高，参数量仅为 DeepSeek-R1 [13] 的一半、Kimi K2 [34] 的三分之一。在图 2 中，我们报告了不同开源模型在 SWE-bench Verified 上的得分与模型参数量的关系，GLM-4.5 与 GLM-4.5-Air 均位于帕累托前沿（Pareto Frontier）上。更多评测结果详见第 4 节。

GLM-4.5 与 GLM-4.5-Air 均可在 [Z.ai](https://Z.ai)、[BigModel.cn](https://BigModel.cn) 上使用，并作为开源模型发布于 <https://huggingface.co/zai-org/GLM-4.5>。我们还在 <https://github.com/zai-org/glm-simple-evals> 开源了评测工具包，以确保基准结果的可复现性。

![图 2](2508.06471v1/swe_parameter.png)

图 2：SWE-bench Verified 得分与模型参数量的关系。专有模型在右侧标记为未知。

## 2 预训练

### 2.1 模型架构

在 GLM-4.5 系列中，我们采用 MoE 架构，以提升训练与推理的计算效率。我们使用无辅助损失的平衡路由（loss-free balance routing）[40] 与 sigmoid 门控作为 MoE 层的门控机制 [23]。与 DeepSeek-V3 [23] 和 Kimi K2 [34] 不同，我们减小了模型的宽度（隐藏维度与路由专家数量），增加了其高度（层数），因为我们发现更深的模型展现出更好的推理能力。在自注意力组件中，我们采用带部分 RoPE 的分组查询注意力（Grouped-Query Attention）。此外，我们使用了 2.5 倍的注意力头数（5120 的隐藏维度对应 96 个头）。与直觉相反，虽然相比头数更少的模型，增加的头数并未改善训练损失，但它在 MMLU、BBH 等推理基准上持续带来更好的表现。我们还引入 QK-Norm [15] 以稳定注意力 logits 的范围。对于 GLM-4.5 与 GLM-4.5-Air，我们都额外添加了一个 MoE 层作为 MTP（多 token 预测，Multi-Token Prediction）层 [12]，以在推理时支持投机解码。

表 1：GLM-4.5 与 GLM-4.5-Air 的模型架构。在统计参数量时，GLM-4.5 与 GLM-4.5-Air 计入 MTP 层的参数，但不计入词嵌入与输出层。

| 模型 | GLM-4.5 | GLM-4.5-Air | DeepSeek-V3 | Kimi K2 |
| --- | --- | --- | --- | --- |
| 总参数量 | 355B | 106B | 671B | 1043B |
| 激活参数量 | 32B | 12B | 37B | 32B |
| 稠密层数 | 3 | 1 | 3 | 1 |
| MoE 层数 | 89 | 45 | 58 | 60 |
| MTP 层数 | 1 | 1 | 1 | 0 |
| 隐藏维度 | 5120 | 4096 | 7168 | 7168 |
| 稠密中间维度 | 12288 | 10944 | 18432 | 18432 |
| MoE 中间维度 | 1536 | 1408 | 2048 | 2048 |
| 注意力头维度 | 128 | 128 | 192 | 192 |
| 注意力头数 | 96 | 96 | 128 | 64 |
| 键值（Key-Value）头数 | 8 | 8 | 128 | 64 |
| 专家数（总计） | 160 | 128 | 256 | 384 |
| 每 token 激活专家数 | 8 | 8 | 8 | 8 |
| 共享专家数 | 1 | 1 | 1 | 1 |
| QK-Norm | 是 | 否 | 否 | 否 |

### 2.2 预训练数据

我们的预训练语料包括来自网页、社交媒体、书籍、论文与代码仓库的文档。我们针对不同来源精心设计了数据处理流水线。

##### 网页

我们的预训练文档主体是从互联网抓取的英文与中文网页。受 Nemotron-CC [32] 启发，我们将抓取到的网页按质量分数划分到不同的桶中。我们对质量分数较高的桶中的文档进行上采样，并丢弃质量分数最低的桶中的文档。质量分数最高的桶在预训练期间贡献了超过 3.2 个 epoch。如此一来，预训练语料既可以强调推理任务所需的高频知识，又能改善对长尾世界知识的覆盖。我们还发现了大量由模板自动生成且被打了高分的相似网页。这类网页无法通过 MinHash 去重去除。我们额外应用 SemDedup [1] 流水线，基于文档嵌入来去除这些相似网页。

##### 多语言

为支持更多自然语言，我们在预训练语料中纳入了多语言文档。多语言语料来自我们抓取的网页与 Fineweb-2 [27]。我们应用一个判断文档教育价值的质量分类器，并对高质量的多语言文档进行上采样。

##### 代码

我们从 GitHub 及各类代码托管平台精选源代码数据。代码语料先经过初步的基于规则的过滤，随后使用针对各语言的质量模型进行分类，将样本划分为高质量、中等质量与低质量三档。训练时，我们对高质量代码进行上采样并排除低质量样本。此外，Fill-In-the-Middle [5] 训练目标被应用于所有源代码数据。
对于与代码相关的网页文档，我们采用两阶段检索流程从文本预训练语料中获取。文档首先依据两条标准进行初筛：包含 HTML 代码标签，或被一个为检测代码相关内容而训练的 FastText [22] 分类器识别。随后，检索到的文档由一个专用模型进行质量评估，划分为高、中、低质量三类，并采用与源代码相同的基于质量的采样策略。最后，使用细粒度解析器对选中的网页重新解析，以更好地保留代码的格式与内容。

##### 数学与科学

为增强推理能力，我们从网页、书籍与论文中收集与数学和科学相关的文档。我们使用大语言模型根据数学与科学教育内容的比例为候选文档打分，并训练一个小规模分类器来预测该分数。预训练语料中分数超过一定阈值的文档会被上采样。

GLM-4.5 的预训练过程分为两个阶段。在第一阶段，模型主要在来自网页的通用文档上训练。在第二阶段，我们对来自 GitHub 的源代码以及与编码、数学、科学相关的网页进行上采样。

### 2.3 中期训练：增强推理与智能体能力

图 3：GLM-4.5 的预训练与中期训练阶段。我们采用多阶段训练配方，并将序列长度从 4K 扩展到 128K。

预训练之后，我们增加了若干阶段，以进一步提升模型在重要应用领域的表现。与在大规模通用文档上的传统预训练不同，这些训练阶段使用中等规模的领域特定数据集（包括指令数据）。因此，我们将这些训练阶段称为中期训练（mid-training），包括以下内容。

##### 仓库级代码训练

在这一训练阶段，我们加入同一仓库内拼接起来的代码文件，以学习跨文件依赖。为提升模型的软件工程能力，我们还纳入了经模型过滤的 GitHub issue、拉取请求（PR）与 commit，将相关的 issue、PR 与 commit 拼接进同一上下文，并以类似 diff 的格式组织 commit。我们将训练序列长度从 4K 扩展到 32K，以容纳大型仓库。

##### 合成推理数据训练

在此阶段，我们为数学、科学与编码竞赛添加合成推理内容。我们从网页与书籍中收集大量与推理任务相关的问题和答案，并用推理模型合成推理过程。

##### 长上下文与智能体训练

为进一步提升模型的长上下文表现，我们将训练序列长度从 32K 扩展到 128K，并对预训练语料中的长文档进行上采样。大规模合成的智能体轨迹也在这一阶段被纳入。

在图 3 中，我们展示了预训练与中期训练的完整阶段。预训练期间最大序列长度保持在 4,096，中期训练中从 32,768 扩展到 131,072。预训练期间我们没有使用最佳适应装箱（best-fit packing）[11]，因为随机截断对预训练文档而言是一种良好的数据增强策略。对于中期训练的数据集，我们应用了最佳适应装箱，以避免截断推理过程或仓库级代码。

### 2.4 超参数

我们对除词嵌入、偏置与 RMSNorm 权重之外的所有参数使用 Muon 优化器 [21; 24]。超参数方面，我们将 Newton-Schulz 迭代步数 $N$ 设为 5，动量 $\mu$ 设为 0.95，并将 Muon 的更新 RMS 缩放至 0.2。我们观察到 Muon 优化器可以加速收敛并容忍更大的 batch size。我们使用余弦衰减（cosine decay）学习率调度，而非 warmup-stable-decay（WSD）调度 [17]。我们的早期实验表明，使用 WSD 调度训练的模型在通用基准（SimpleQA、MMLU）上表现更差，说明稳定阶段存在欠拟合。学习率从 0 经预热阶段升至 2.5e-4，再经衰减阶段降至 2.5e-5，直至中期训练结束。我们采用 batch size 预热策略：在前 500B token 的训练中，batch size 从 16M token 逐步增加到 64M token，并在其余训练中保持恒定。
正则化方面，我们将权重衰减率设为 0.1，未使用 dropout。预训练期间最大序列长度设为 4,096，并在中期训练阶段扩展到 32,768 与 131,072（如图 3 所示）。在将序列长度扩展到 32K 时，我们还将 RoPE 的基频从 10,000 调整为 1,000,000，以获得更好的长上下文建模能力。对于无辅助损失的平衡路由，前 15T token 的偏置更新率设为 0.001，其余 token 设为 0.0。我们还施加了权重为 0.0001 的序列级辅助平衡损失，以避免任何单条序列内出现极端不平衡。MTP 损失权重 $\lambda$ 在前 15T token 设为 0.3，其余 token 设为 0.1。

## 3 后训练：专家模型迭代

我们将后训练过程划分为两个不同的阶段。在阶段 1（*专家训练*）中，我们构建专精于三个领域的专家模型：推理、智能体与通用对话。在阶段 2（*统一训练*）中，我们采用自蒸馏技术整合多个专家，最终交付一个能够通过深思熟虑的推理与直接响应两种模式生成回答的综合模型。

### 3.1 监督微调

我们在阶段 1（*专家训练*）与阶段 2（*统一训练*）的开头都执行监督微调（SFT）。在专家训练阶段，SFT 的主要作用是提供冷启动，赋予模型基本的对话、推理与工具使用能力，随后可在后续的专家强化学习训练中进一步增强，以获得更好的性能。在统一训练阶段，SFT 的目的是将不同专家模型的能力蒸馏进一个能够处理不同类型任务的混合推理通才模型之中。

##### 冷启动 SFT

在冷启动阶段，我们使用一小批带有扩展思维链（Chain-of-Thought，CoT）回答的监督微调数据。这一做法确保每个专家模型在进入强化学习阶段之前具备充分的基础能力。

##### 整体 SFT

在整体 SFT 阶段，我们收集了数百万样本，覆盖推理任务（数学、代码、科学等）、通用对话（写作、翻译、摘要、闲聊等）、智能体任务（基础工具使用，尤其是面向真实项目开发的编码能力等）以及长上下文理解任务，它们均来自此前训练好的专家模型；我们以最大 128K token 的上下文长度训练基座模型。通过从不同专家的输出中蒸馏，模型学会为每个任务运用最有效的长 CoT 推理以得到准确答案。特别地，考虑到某些要求快速响应的领域（如闲聊）并不需要漫长的思考过程，我们细致地平衡了包含完整推理过程的训练数据与缺乏显式思考过程的数据。这一做法使模型既能以反思模式运行，也能以即时响应模式运行，从而构建出一个*混合推理模型*。此外，我们发现以下策略有助于准备 SFT 数据以获得最优性能。

##### 减少函数调用模板中的字符转义

尽管在当代实现中函数调用参数主要以 JSON 格式表示，但当这些参数包含代码片段时会浮现一个显著的挑战：此时代码中相当比例的字符需要转义，迫使模型生成大量转义字符，从而加重了模型的学习负担。虽然该问题对主要为通用对话设计的模型影响不大，但对于将函数调用作为核心能力的智能体基础模型而言，这是一个不容忽视的挑战。
为缓解这一局限，我们提出了一种新颖的函数调用模板，将函数调用的键与值封装在类 XML 的特殊 token 标签中。这一做法大幅减少了代码片段中字符转义的必要，因为绝大多数代码可以以其原生形式表示而无需转义。实验结果表明，所提出的函数调用模板在减少转义的同时不会损害函数调用执行的性能。下面的例子（图 4）展示了我们提出的函数调用模板的结构。详细的代码实现可在我们的开源仓库中找到。

```text
<|system|>
# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"name": "get_weather", "description": "Get the weather of a city for a specific date.", "parameters": {"type": "object", "properties": {"city": {"type": "string", "description": "The city to get weather for, in Chinese."}, "date": {"type": "string", "description": "The date in YYYY-MM-DD format."}}, "required": ["city"]}}
</tools>

For each function call, output the function name and arguments within the following XML format:
<tool_call>{function-name}
<arg_key>{arg-key-1}</arg_key>
<arg_value>{arg-value-1}</arg_value>
<arg_key>{arg-key-2}</arg_key>
<arg_value>{arg-value-2}</arg_value>
...
</tool_call><|system|>
You are a helpful assistant.<|user|>
Today is June 26, 2024. Could you please check the weather in Beijing and Shanghai for tomorrow<|assistant|>
<think>The user wants to check the weather of Beijing and Shanghai tomorrow. I need to call the get_weather function respectively to check Beijing and Shanghai.</think>
I will call the get_weather function to check the weather in Beijing and Shanghai.
<tool_call>get_weather
<arg_key>city</arg_key>
<arg_value>Beijing</arg_value>
<arg_key>date</arg_key>
<arg_value>2024-06-27</arg_value>
</tool_call>
<tool_call>get_weather
<arg_key>city</arg_key>
<arg_value>Shanghai</arg_value>
<arg_key>date</arg_key>
<arg_value>2024-06-27</arg_value>
</tool_call><|observation|>
<tool_response>
{"city": "Beijing", "date": "2024-06-27", "weather": "Sunny", "temperature": "26C"}
</tool_response>
<tool_response>
{"city": "Shanghai", "date": "2024-06-27", "weather": "Overcast", "temperature": "29C"}
</tool_response><|assistant|>
<think>I have obtained the weather query results of get_weather for Beijing and Shanghai respectively and can reply to users directly.</think>
It will be sunny in Beijing tomorrow with a temperature of 26 degrees Celsius. The weather in Shanghai is overcast with a temperature of 29 degrees Celsius.<|user|>
```

图 4：函数调用模板的一个示例。

##### 拒绝采样

在从专家模型采样时，我们采用一套全面的多阶段过滤流水线，包括：(1) 去除重复、过短或被截断的样本，以及不符合有效推理格式的样本；(2) 对具有客观答案的样本进行正确性验证；(3) 使用奖励模型过滤主观问题的回答；(4) 对于工具调用场景，确保遵循正确的工具调用协议，并验证轨迹是否到达预期的终止状态。

##### 提示选择与响应级扩展

过滤出高难度提示并对其进行响应级扩展（response-level scaling）被证明是有效的。我们实验了基于回答长度剔除底部 50% 的提示，在仅用一半数据训练的情况下，数学与科学任务仍提升了 2%-4%。值得注意的是，我们发现对这些困难提示进行响应扩展可以带来进一步收益：为每个提示生成四个回答带来了额外 1%-2% 的提升。

##### 智能体 SFT 数据的自动构建

智能体 SFT 数据的构建包含四个步骤：1. *智能体框架与工具收集*：我们收集了一批智能体框架、真实世界工具 API 与 MCP 服务器，同时利用 LLM 自动构建并模拟一批工具。2. *任务合成*：基于这些框架与工具，我们自动合成一批智能体任务。一方面，对于相对成熟的框架，我们利用 LLM 理解其功能并自动生成相关查询或任务；另一方面，对于较为碎片化或差异较大的工具，我们先选取一个具有代表性的子集，同样利用 LLM 围绕该子集构造任务。这些任务同时涵盖单步与多步工具调用场景。3. *轨迹生成*：对每个合成任务，我们利用现有 LLM 生成工具调用轨迹。此外，通过将 LLM 用作用户模拟器，多步工具调用任务被转换为包含多轮对话的轨迹。4. *质量过滤*：对每条轨迹，使用多个裁判智能体评估任务是否完成，仅保留成功的轨迹。

### 3.2 推理强化学习

推理强化学习聚焦于增强模型在那些需要逻辑演绎、结构化问题求解与可验证准确性的领域中的能力，包括数学、代码生成与科学推理等关键领域。这类任务的一个显著特征是奖励信号的高精度，因为正确性通常可以程序化地判定或具有客观的清晰性。在这些领域的能力掌握不仅对提升模型的原始智能至关重要，也是更复杂的多步智能体行为的基础构件。认识到推理强化学习中独特的挑战与机遇，我们开发了一套专门的技术来有效训练我们的模型。下文详述的这些方法旨在解决训练效率、样本多样性与数据质量等问题。我们的整体强化学习算法建立在 GRPO [31] 框架之上，但不包含 KL 损失项。本节展示的对比曲线基于我们较小的实验模型，而非 GLM-4.5。

图 5：基于难度的两阶段课程学习在 AIME'24 上的有效性。蓝线（我们的方法）在第二阶段切换到极难题目（pass@8==0、pass@512>>0），持续提升；红线（基线）继续使用中等难度题目并进入平台期。

##### 基于难度的课程学习

在强化学习过程中，模型的能力在不断演进，与静态训练数据产生错配。在后期阶段，随着模型能力增强，过于简单的数据会导致 rollout 中所有奖励均为 1；反之，在早期阶段，过难的数据往往导致整批奖励均为 0。在这两种情形下，奖励方差的缺失无法提供有用的梯度信号，严重阻碍训练效率。为应对这一挑战，我们在强化学习中采用两阶段的基于难度的课程学习。下文讨论的该策略及其他策略的有效性，通过在较小模型上的对照实验得到验证——这允许快速迭代与精确的消融研究。如图 5 所示，这种两阶段方法使模型能够持续超越其性能上限。至关重要的是，为保持高信号质量并降低噪声，第二阶段使用的所有题目都严格来源于经过验证、具有正确答案的题池。

图 6：64K 上下文长度下的单阶段与多阶段强化学习。红线（64K 单阶段）取得更优性能。蓝线（长度渐进增加的多阶段）在早期阶段出现不可逆的性能下降，限制了最终性能。

##### 64K 输出长度下的单阶段强化学习

此前的研究 [25] 建议以多个阶段、逐步增大最大输出长度的方式开展强化学习。然而，我们的实验表明，这种多阶段方法不如直接以 64K 的最大目标长度进行的单阶段强化学习有效。由于初始监督微调（SFT）已使模型具备生成 64K 长度回答的能力，引入最大长度较短的强化学习阶段会导致模型「遗忘」其长上下文能力。这往往导致显著且不可逆的性能下降，表现为模型平均输出长度缩短。这种退化在最后的 64K 长度强化学习阶段难以恢复，从而限制了进一步提升。我们的实验证实了这一观察：如图 6 所示，直接以完整 64K 长度应用强化学习能持续逼近模型极限并带来更好的性能。

##### 动态采样温度

在强化学习中，采样温度是控制轨迹多样性的关键参数。温度过低会导致输出收敛、探索不足，而温度过高则会引入低质量的噪声样本，损害模型准确性与训练效率。使用固定的采样温度并非最优，因为它无法随策略分布变得更加集中（即熵更低）而自适应调整，往往导致后期阶段探索不足。因此，我们提出动态调整采样温度，以在准确性与探索之间维持健康的平衡。具体而言，当 rollout 的平均奖励趋于稳定时，我们将其判定为收敛阶段，并提高采样温度以鼓励更大的多样性。为控制引入过量噪声的风险，我们实施了一套质量控制机制：定期在一组不同温度下于留出验证集上评估模型表现，下一训练阶段的温度随后被设定为不使性能较当前最优下降超过 1% 的最大值 [2]。

图 7：代码与科学强化学习的消融研究。
（左）代码强化学习损失计算方式的对比。与序列均值损失基线相比，token 加权均值损失方法收敛更快，加速了训练过程。
（右）GPQA-Diamond 基准上科学强化学习数据来源的消融。仅在一小批高质量、经专家校验的选择题上训练即可取得最佳性能，显著优于在混合质量数据上训练。

##### 代码与科学强化学习

与数学相比，编码与科学领域的强化学习在文献中受到的关注较少。我们在这些领域开展了大量受控强化学习实验，并得出以下经验性结论。对于代码强化学习，我们发现损失计算方式的选择对训练效率至关重要。如图 7（左）所示，相比传统的序列均值损失，采用 token 加权均值损失非常有益。token 加权方式提供了更细粒度、更稳定的梯度信号，带来显著更快的收敛。该方法还有助于缓解序列级奖励固有的长度偏差，并有效抑制训练期间过于简单或重复的「基础情形（base case）」样本的生成。对于科学强化学习，我们在 GPQA-Diamond 基准上的发现凸显了数据质量与类型是重中之重。如图 7（右）所示，仅使用经专家校验的选择题进行强化学习，相比使用混合质量或未校验数据训练，能带来显著更好的性能。这一结果强调：即便是选择题这类格式简单的任务，严格过滤强化学习数据池、只保留高质量且具有挑战性的样本，对于模型的有效提升也至关重要。

### 3.3 智能体强化学习

来自人类反馈的强化学习（RLHF）帮助语言模型更忠实地遵循人类指令。将强化学习应用于数学与编程竞赛，进一步在结果可被客观验证的任务上揭示了强大的推理能力与良好的扩展行为。基于这些洞察，我们聚焦于智能体场景——具体为网页搜索与代码生成智能体——其中每个动作或答案都可以被自动检查。这种内建的可验证性提供了密集而可靠的奖励，使我们能够更有效地扩展强化学习训练。

#### 3.3.1 面向智能体的数据收集与合成

对于网页搜索任务与开放域信息检索，我们开发了一条数据合成流水线，生成需要跨多个网络来源进行多步推理的高难度问答对。该语料旨在磨砺 GLM 在互联网上发掘隐晦、交织事实的能力。数据集构建融合了两种方式：(1) 由知识图谱上的多跳推理驱动的自动化流水线；(2) 人在回路（human-in-the-loop）的内容抽取与选择性混淆，从多个网页制备强化学习训练信号。

对于软件工程任务，我们精选了大规模的 GitHub 拉取请求与 issue 集合，构建了一个由用户提示与可执行单元测试构成的真实软件开发基准。所有评测都在带分布式系统的强化隔离沙箱中运行，兼具横向可扩展性与强隔离保证。

#### 3.3.2 以强化学习与迭代自蒸馏突破极限

我们采用组式策略优化（group-wise policy optimization）算法进行强化学习训练。
对于每个问题 $x$，我们从上一策略 $\pi_{\text{old}}$ 中采样 $K$ 条智能体轨迹 $\{y_{1},\dots,y_{k}\}$，并针对以下目标优化模型 $\pi_{\theta}$：

$$
L_{\text{RL}}(\theta)=\mathbb{E}_{x\sim\mathcal{D}}\!\left[\frac{1}{K}\sum_{i=1}^{K}\left(r(x,y_{i})-\bar{r}(x)\right)\right],
$$

其中 $\bar{r}(x)\;=\;\frac{1}{k}\sum_{i=1}^{k}r\bigl(x,y_{i}\bigr)$ 为采样回答的平均奖励。需要注意的是，优化仅使用模型生成的 token，环境反馈在损失计算中被忽略。

##### 带过程动作格式惩罚的结果监督

对于网页搜索任务，我们使用最终答案的准确性作为整条智能体轨迹的奖励。对于编码智能体，我们主要利用带有可验证测试用例的 SWE 数据进行强化学习训练。我们的实验表明，在网页搜索与 SWE 任务上的强化学习训练带来了在其他任务与基准上的泛化性能提升，例如通用工具使用以及 Terminal-Bench 等编码任务。此外，我们施加过程格式惩罚以确保模型生成正确的工具调用格式。如果模型在智能体轨迹生成过程中未能产生正确的工具格式，过程将被中止，且该轨迹将获得零奖励。

##### 迭代蒸馏

由于智能体任务上的强化学习训练十分耗时，我们采用自蒸馏方法，在恢复强化学习训练之前迭代增强 SFT 冷启动模型的性能。具体而言，我们首先对初始冷启动模型进行强化学习训练以提升智能体性能。一旦训练达到一定步数或进入平台期，我们就以强化学习训练后的模型生成的回答替换原始冷启动数据，进行自蒸馏，从而创建一个更优的 SFT 模型。然后，我们在这个增强后的模型上继续进行强化学习训练，并逐步提高训练难度。这一迭代策略使我们能够高效地突破强化学习模型的性能极限。

##### 通过交互轮数扩展测试时计算

对于智能体任务，我们观察到随着与环境交互轮数的增加，性能会显著提升。与推理模型中扩展输出 token 数的测试时扩展不同，智能体任务通过持续与环境交互来利用测试时算力，例如为难以查找的网络信息上下求索，或在编码任务中编写测试用例以进行自我验证与自我修正。
图 8 表明，在不同的浏览努力程度下，准确率随测试时算力平滑扩展。

图 8：BrowseComp 的交互轮数扩展。

### 3.4 通用强化学习

通用强化学习旨在从整体上提升模型的综合表现、修复潜在问题并强化关键能力。我们方法论的核心是一个多源反馈系统，它协同基于规则的反馈、人类反馈（RLHF）与基于模型的反馈（RLAIF）。这一混合框架提供了更鲁棒的训练信号，使我们能够利用每种反馈来源的独特优势：自动化规则的精确性、人类标注者细腻的判断力，以及 AI 驱动评估的可扩展性。

##### 整体强化学习

整体强化学习（Holistic RL）以跨领域的广泛性能提升为目标。为此，我们首先构建了一个均衡的数据集，包含约 5,000 条提示，覆盖 7 个一级、33 个二级与 139 个三级类别。
整体强化学习的奖励信号源自人类反馈与 AI 反馈。对于人类反馈，我们在偏好标注上训练奖励模型。标注者比较模型的回答，并基于指令遵循、安全性、事实正确性等多个维度的综合评估给出偏好标签。
对于模型反馈，我们依据提示是否具有客观标准答案设计了不同的评分细则。
合并两种反馈来源产生了更可靠、更具表达力的奖励信号，缓解了每种方法各自的固有局限。

##### 指令遵循强化学习

指令遵循强化学习提升模型理解并满足复杂指令的能力。为此，我们创建了一个细粒度分类体系，包含 7 个大类、151 个小类约束，覆盖内容要求、格式规则等。基于该分类体系，我们组装了一个覆盖每种约束类型的困难指令专用训练集。
反馈系统由确定性验证规则、训练好的奖励模型与一个批评（critique）模型组成。这一混合反馈系统的鲁棒性在 GRPO 训练中被证明至关重要。我们观察到奖励黑客（reward hacking）行为得到缓解，使策略模型在指令遵循上取得持续而稳定的改进，如图 9 所示。

图 9：不包含其他通用强化学习任务的指令遵循强化学习训练曲线。GRPO 训练期间，指令遵循性能（SysBench-ISR）随奖励的增加而同步提升。直至约 1,000 步训练，我们尚未观察到明显的奖励黑客证据。

##### 函数调用强化学习

函数调用强化学习分为逐步（step-wise）基于规则的强化学习与端到端多轮强化学习。由于输出长度与收敛速度相近，我们将逐步基于规则的强化学习直接纳入通用强化学习框架。对于端到端多轮强化学习，我们先训练专门的专家模型，再将这些专家蒸馏进主模型。

- 逐步基于规则的强化学习：对于具有清晰工具调用流程的任务，我们在训练数据中为每一步/每一轮标注真实（ground-truth）函数调用。给定任务与之前步骤/轮次的函数调用，模型被训练来生成下一个助手回复，它可以是函数调用，也可以是对用户的回复。利用基于规则的奖励，我们引导模型在连续多轮中做出正确的函数调用。为此，我们设计了如下严格的奖励函数：

$$
\text{Reward}=\begin{cases}1,&\text{if }\texttt{FormatCorrect}(a_{t})\ \text{and}\ \texttt{Match}(a_{t},a_{t}^{*})\\ 0,&\text{otherwise}\end{cases}
$$

  这里，$a_{t}$ 表示模型生成的第 $t$ 次函数调用，$a_{t}^{*}$ 是对应的真实函数调用。只有当 $a_{t}$ 格式正确且与真实值完全匹配（包括名称、参数与每个字段）时，才给予奖励 1，否则奖励为 0。
  如此严格的奖励规则不仅引导模型生成正确的函数调用，还强力约束输出格式，提升了模型在真实世界交互中的可用性与鲁棒性。
- 端到端多轮强化学习：逐步基于规则的强化学习将任务分解为静态、预先确定的决策流。在此过程中，模型缺乏与环境的动态交互，无法自主探索、规划或处理复杂情况，因而其真实世界问题求解能力受限。为解决这些问题，我们引入端到端多轮函数调用强化学习：模型先生成完整轨迹，再基于任务完成情况获得奖励。这样，模型可以通过与工具反馈的持续试错来优化其动作策略，显著增强其自主规划与决策能力。
  具体而言，端到端多轮函数调用强化学习考虑两类复杂任务：1. 单轮多步任务：模型需要进行多步函数调用并与环境交互才能完成此类任务。我们使用基于 MCP 服务器自动合成的复杂任务，以及一些带可运行环境的开源智能体数据集，如 Agentgym [46]。2. 多轮多步任务：除与工具执行环境交互外，模型还需与 LLM 模拟的用户智能体交互，以获取完整的任务信息并完成整体任务。
  端到端多轮函数调用强化学习的奖励计算如下：

$$
\text{Reward}=\begin{cases}1,&\text{if }\texttt{FormatCorrect}(a_{1},\dots,a_{T})\ \text{and}\ \texttt{TaskCompleted}(I,o_{0},a_{1},o_{1},\dots,a_{T},o_{T})\\ 0,&\text{otherwise}\end{cases}
$$

  这里，$I$ 表示原始复杂任务，$a_{t}$ 是第 $t$ 次函数调用，$o_{t}$ 是工具反馈或用户信息。$\texttt{TaskCompleted}(I,o_{0},a_{1},o_{1},\dots,a_{T},o_{T})$ 表示任务是否完成，由环境按预定义规则判定，或由 LLM 裁判智能体判定。

##### 病态行为强化学习

作为后训练的最后一个阶段，通用强化学习需要纠正潜在问题，例如语言混杂、过度重复与格式错误。尽管在上述通用强化学习任务中惩罚此类行为是有效的，但这些病态行为的发生率很低（通常不足输出的 1%），使这成为一种样本效率低下的优化策略。因此，我们通过识别极有可能触发这些病态行为的提示，为病态行为强化学习（Pathology RL）精选了一个针对性数据集。
在该数据集上训练使我们能够施加高效的惩罚，进一步降低这些问题行为的残余错误率。

### 3.5 强化学习基础设施

![图 10](2508.06471v1/slime.png)

图 10：Slime 强化学习基础设施概览。系统由三个核心模块组成：训练（Megatron）——负责主训练过程，从数据缓冲区（Data Buffer）读取数据，并在训练后与 rollout 模块同步参数；Rollout（SGLang + Router）——生成新数据（包括奖励与验证器输出）并写入数据缓冲区；数据缓冲区——作为桥接模块，管理提示初始化、自定义数据与 rollout 生成策略。

我们的强化学习基础设施构建于 Slime（<https://github.com/THUDM/slime>）之上，这是一个我们自主开发的开源框架。该框架在工程上做了若干关键优化，以增强灵活性、效率与可扩展性。

##### 灵活的混合训练与数据生成架构

我们基础设施的一个核心特性，是在单一统一的系统内支持高度灵活的训练范式与数据生成策略。这一设计使我们能够通过同时支持同置（colocated）的同步模式与解耦（disaggregated）的异步模式，来满足不同强化学习任务的差异化需求。这种数据生成上的灵活性，对于将我们的强化学习能力扩展到新领域与更复杂的智能体环境至关重要。
我们观察到不同的强化学习任务受益于不同的调度方式。对于通用强化学习任务，或旨在增强模型推理能力（例如数学与代码生成）的任务，同步、同置的架构更为有效。在这种设置下，训练引擎与推理引擎位于同一 worker 上。结合动态采样，这显著减少了 GPU 空闲时间并最大化了资源利用率。
相反，对于智能体任务（例如软件工程 SWE 中的任务），数据生成过程往往漫长并涉及复杂的系统交互。为确保智能体环境能够持续运行并最大化数据吞吐，我们采用解耦的异步模式。强化学习框架的 rollout 组件直接暴露给智能体环境，而训练与推理的 GPU 则独立调度。这种解耦使智能体环境能够持续生成新数据，而不会被训练周期阻塞。
借助 Ray 框架的资源调度与异步能力，我们可以灵活地将推理引擎与训练引擎放置在同一 GPU 或不同 GPU 上。这种对同步与异步训练的双重支持，使多样化的强化学习任务得以共享一套训练与推理的底层优化。

##### 以混合精度推理加速 Rollout

Rollout 效率是强化学习训练中一个长期存在的瓶颈。为解决这一问题，我们的基础设施在训练时支持 BF16，同时在推理时利用 FP8 来加速数据生成阶段。
在每次策略更新迭代中，我们在模型参数分发用于 rollout 之前，对其进行在线的、按块（block-wise）的 FP8 量化。这种动态量化实现了高效的 FP8 推理，显著提升了数据收集过程的整体吞吐。

##### 面向智能体的强化学习基础设施设计

为开展智能体任务的强化学习，我们设计了一套完全异步、解耦的强化学习基础设施，能高效处理长时程（long-horizon）智能体 rollout，并支持跨多样智能体框架的灵活多任务强化学习训练。

智能体 rollout 往往需要与复杂环境进行长时间交互，这可能显著拖慢整体强化学习训练进程。为克服这一点，我们首先设计了一个高并发的基于 Docker 的运行时，为每个任务提供隔离的环境，大幅降低 rollout 开销。此外，我们实现了完全异步的强化学习训练循环。由于智能体任务在类型与轨迹长度上差异很大，同步的强化学习训练往往因 worker 等待最慢的 rollout 完成而造成严重的 GPU 利用不足。我们的方案将 GPU 划分为专用的 rollout 引擎与训练引擎：rollout 引擎持续生成轨迹，训练引擎更新模型权重并周期性地将其同步回 rollout 引擎。这种解耦设计避免了长轨迹或多样化轨迹阻塞整个训练流水线，从而在智能体交互高度可变的场景中始终保持高吞吐。

另一个关键挑战是现有智能体框架的多样性——它们各自面向不同任务定制。利用这些框架不仅可以提升任务特定性能，还能保持训练与推理之间的一致性。为此，我们引入了统一的 HTTP 端点接口并结合集中式数据池。由于大多数智能体框架以消息列表（message-list）格式产生 rollout，所有轨迹都存储在该数据池中，作为训练的共享来源。这一架构将任务特定的 rollout 逻辑与强化学习训练过程干净地解耦，使异构智能体框架能够无缝集成。此外，数据池支持可定制的、任务特定的过滤与动态采样策略，以确保跨多样任务的高质量强化学习训练数据。

通过以上两项核心设计，我们的系统为长时程智能体强化学习提供了一个可扩展、灵活且高性能的解决方案，能够支持长时程 rollout 并适应广泛多样的智能体任务。

## 4 评测

### 4.1 基座模型评测

我们首先评估基座模型 GLM-4.5-Base 的表现。表 2 展示了基座模型预训练最后一个检查点的对比结果。请注意，基座模型未经过指令数据训练，GLM-4.5-Base 的分数来自我们的内部评测框架。
结果表明，GLM-4.5-Base 在包括英文、代码、数学与中文在内的所有不同基准上表现稳定，验证了我们把所有能力统一进一个模型的想法。

表 2：GLM-4.5-Base 与其他代表性开源基座模型的对比。

| 类别 | 基准（指标） | Qwen3-235B-A22B Base | Llama4-Maverick 400B Base | DeepSeek-V3 Base | Kimi-K2 Base | GLM-4.5 Base |
| --- | --- | --- | --- | --- | --- | --- |
|  | 架构 | MoE | MoE | MoE | MoE | MoE |
|  | 激活参数量 | 22B | 17B | 37B | 32B | 32B |
|  | 总参数量 | 235B | 400B | 671B | 1043B | 355B |
| 英语 | SimpleQA (EM) | - | - | 26.6 | 35.3 | 30.0 |
|  | BBH (EM) | 88.9 | 87.1 | 88.4 | 88.7 | 86.2 |
|  | MMLU (EM) | 87.8 | 85.2 | 87.2 | 87.8 | 86.1 |
|  | HellaSwag (EM) | - | - | 88.9 | 94.6 | 87.1 |
|  | PIQA (EM) | - | - | 84.7 | - | 85.3 |
|  | TriviaQA (EM) | - | - | 82.9 | 85.1 | 80.0 |
| 代码 | EvalPlus (Pass@1) | 77.6 | 65.5 | 65.6 | 80.3 | 78.1 |
|  | LiveCodeBench-Base (Pass@1) | - | 25.1 | 24.6 | 26.3 | 28.1 |
| 数学 | GSM8K (EM) | 94.4 | 87.7 | 87.6 | 92.1 | 79.4 |
|  | MATH (EM) | 71.8 | 63.3 | 62.6 | 70.2 | 61.0 |
| 中文 | CLUEWSC (EM) | - | - | 82.7 | - | 83.5 |
|  | C-Eval (EM) | - | 80.9 | 90.1 | 92.5 | 86.9 |
|  | C3 (EM) | - | - | 78.6 | - | 83.1 |
|  | Chinese-SimpleQA (EM) | - | 53.5 | 72.1 | 77.6 | 70.1 |

### 4.2 在 12 项（ARC）基准上的评测

我们进一步对后训练完成后的完整 GLM-4.5 模型进行全部智能体、推理与编码（ARC）任务的评测，共 12 项基准：MMLU-Pro、AIME 24、MATH-500、SciCode、GPQA、HLE、LCB（2407-2501）、SWE-Bench Verified、Terminal-Bench、TAU-Bench、BFCL V3、BrowseComp。

#### 4.2.1 智能体能力评测

表 3：智能体基准上的结果。TAU 代表 TAU-bench [48]，BFCL 代表 Berkeley Function Calling Leaderboard [26]。

| 基准 | GLM-4.5 | GLM-4.5-Air | o3 | o4 mini | GPT-4.1 | Claude Opus 4 | Claude Sonnet 4 | Gemini 2.5 Pro | Kimi K2 | Grok 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TAU-Retail | 79.7 | 77.9 | 70.4 | 65.6 | 75.1 | 81.4 | 80.5 | 77.0 | 73.9 | 76.5 |
| TAU-Airline | 60.4 | 60.8 | 52.0 | 49.2 | 48.8 | 59.6 | 60.0 | 48.0 | 51.2 | 58.4 |
| BFCL V3 | 77.8 | 76.4 | 72.4 | 67.2 | 68.9 | 74.4 | 75.2 | 61.2 | 71.1 | 66.2 |
| BrowseComp | 26.4 | 21.3 | 49.7 | 28.3 | 4.1 | 18.8 | 14.7 | 7.6 | 7.9 | 32.6 |
| 平均 | 58.1 | 55.7 | 61.1 | 50.1 | 45.0 | 54.6 | 53.4 | 43.8 | 47.2 | 55.4 |

我们从两个方面评估 GLM-4.5 的智能体能力：TAU-bench [48]（涵盖零售与航空两个领域）与 Berkeley Function Call Leaderboard V3（BFCL V3）[26]，后者衡量模型调用用户自定义函数来回应用户查询的能力。BrowseComp [45] 衡量模型作为网页浏览智能体为复杂问题找到正确答案的能力。对于 TAU-bench，我们在零售与航空两个领域均使用了优化过的用户模拟器（参见图 11）。我们使用的用户提示见图 11。
在 TAU-bench 上，GLM-4.5 的表现优于 Gemini 2.5 Pro，接近 Claude Sonnet 4。在 BFCL V3 上，GLM-4.5 在所有基线模型中取得最佳总分。在 BrowseComp 上，OpenAI o3 的表现远好于其他模型，GLM-4.5 的表现接近第二好的模型（o4-mini），并显著优于 Claude Opus 4。

```text
You are a user interacting with an agent.{instruction_display}
# Rules:
- Just generate one line at a time to simulate the user’s message.
- Do not give away all the instruction at once. Only provide the information that is necessary for the current step.
- Do not hallucinate information that is not provided in the instruction. Follow these guidelines:
 1. If the agent asks for information NOT in the instruction:
 - Say you don’t remember or don’t have it
 - Offer alternative information that IS mentioned in the instruction
 2. Examples:
 - If asked for order ID (not in instruction): ‘‘Sorry, I don’t remember the order ID, can you search for it? My name/email/phone number/zipcode is ...’’
 - If asked for email (not in instruction): ‘‘I don’t have my email handy, but I can give you my name and zip code which are...’’
- Do not repeat the exact instruction in the conversation. Instead, use your own words to convey the same information.
- Try to make the conversation as natural as possible, and stick to the personalities in the instruction.
# Constraint Handling:
- Provide requests strictly based on what is explicitly stated in the instruction.
- Do not assume, extend, substitute, or generalize in any form.
- Do not modify or relax constraints on:
- Time / Date
- Budget
- Specific terms (e.g., ‘‘same’’ must not be replaced with ‘‘similar’’)
- Core Rule: Any attribute NOT mentioned in the instruction can be either changed or kept the same
- Examples:
 - If instruction says ‘‘exchange red item to blue’’: Only color must change, other attributes (size, material, etc.) are flexible
 - If instruction says ‘‘exchange red item to blue, keep the same size’’: Both color must change AND size must stay the same
- Exception: Only follow additional constraints when explicitly stated in the instruction
# When NOT to finish the conversation:
- Do not end until you have clearly and completely expressed all your requirements and constraints.
- Do not end until the agent has completed all tasks mentioned in the instruction and verified no operations were missed.
- Do not end if the agent’s execution results do not match your expectations or are incorrect/incomplete.
# When you CAN finish the conversation:
- Only when all above conditions are satisfied AND all tasks are completed correctly.
- OR when you have clearly expressed complete requirements but the system explicitly states it cannot complete them due to technical limitations - in this case, accept transfer to human.
# How to finish the conversation:
- If the agent has completed all tasks, generate ‘‘###STOP###’’ as a standalone message without anything else to end the conversation.
# Note:
- You should carefully check if the agent has completed all tasks mentioned in the instruction before generating ‘‘###STOP###’’.
```

图 11：我们用于 TAU-bench 的用户提示示例。

#### 4.2.2 推理能力评测

我们在七项基准上评估 GLM-4.5 与 GLM-4.5-Air 的推理能力，包括 MMLU-Pro [43]、AIME 24、MATH 500 [14]、SciCode [36]、GPQA [30]、Humanity's Last Exam（HLE）[28] 与 LiveCodeBench（LCB）[19]。LiveCodeBench 是一个动态基准，我们在 2024 年 7 月 1 日至 2025 年 1 月 1 日之间的问题上进行评测。对于 AIME 与 GPQA 基准，我们分别报告 32 个与 8 个样本上的平均准确率（Avg@32、Avg@8），以降低结果方差。我们使用 LLM 进行自动化答案校验。对于 HLE 基准，仅评测基于文本的问题，由 GPT-4o 判定正确性。我们的评测代码同样已开源（<https://github.com/zai-org/glm-simple-evals>）。我们还使用 Artificial Analysis 提出的智能指数（intelligence index）计算七项基准上的平均推理表现（<https://artificialanalysis.ai>）。GLM-4.5 在 AIME 24 与 SciCode 上超越 OpenAI o3。平均而言，GLM-4.5 优于 Claude Opus 4，接近 DeepSeek-R1-0528。

表 4：推理基准上的结果。HLE 代表 Humanity's Last Exam [28]，LCB 代表 LiveCodeBench（2407-2501）[19]。

| 基准 | GLM-4.5 | GLM-4.5-Air | o3 | Claude Opus 4 | Gemini 2.5 Pro | DeepSeek R1 0528 | Qwen3 235B 2507 | Grok 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MMLU Pro | 84.6 | 81.4 | 85.3 | 87.3 | 86.2 | 84.9 | 84.5 | 86.6 |
| AIME 24 | 91.0 | 89.4 | 90.3 | 75.7 | 88.7 | 89.3 | 94.1 | 94.3 |
| MATH 500 | 98.2 | 98.1 | 99.2 | 98.2 | 96.7 | 98.3 | 98.0 | 99.0 |
| SciCode | 41.7 | 37.3 | 41.0 | 39.8 | 42.8 | 40.3 | 42.9 | 45.7 |
| GPQA | 79.1 | 75.0 | 82.7 | 79.6 | 84.4 | 81.3 | 81.1 | 87.7 |
| HLE | 14.4 | 10.6 | 20.0 | 11.7 | 21.1 | 14.9 | 15.8 | 23.9 |
| LCB | 72.9 | 70.7 | 78.4 | 63.6 | 80.1 | 77.0 | 78.2 | 81.9 |
| AA-Index（估算） | 67.7 | 64.8 | 70.0 | 64.4 | 70.5 | 68.3 | 69.4 | 73.2 |

#### 4.2.3 编码能力评测

表 5：SWE-bench Verified 与 Terminal-Bench 上的结果

| 基准 | GLM-4.5 | GLM-4.5-Air | o3 | GPT-4.1 | Claude Opus 4 | Claude Sonnet 4 | Gemini 2.5 Pro | DeepSeek R1 0528 | Kimi K2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWE-bench Verified | 64.2 | 57.6 | 69.1 | 48.6 | 67.8 | 70.4 | 49.0 | 41.4 | 65.4 |
| Terminal-Bench | 37.5 | 30.0 | 30.2 | 30.3 | 43.2 | 35.5 | 25.3 | 17.5 | 25.0 |
| 平均 | 50.9 | 43.8 | 49.7 | 39.5 | 55.5 | 53.0 | 37.2 | 29.5 | 45.2 |

为衡量 GLM-4.5 完成真实世界编码任务的能力，我们在两个高难度基准上对其进行评估：SWE-bench Verified [20] 与 Terminal-Bench [35]。SWE-bench 衡量模型修改既有代码库以解决 GitHub issue 的能力，Verified 子集是经人工筛选的 500 个实例。评测时，我们使用 OpenHands [42] v0.34.0，运行限制为 100 次迭代，并进行历史截断以避免超出 128K 上下文限制，配置 temperature=0.6、top_p=1.0。Terminal-Bench 衡量模型在终端环境中完成复杂任务的能力。我们使用 Terminus 框架与标准函数调用（而非直接提示）进行评测。在 SWE-bench Verified 上，GLM-4.5 优于 GPT-4.1 与 Gemini-2.5-Pro。在 Terminal-Bench 上，GLM-4.5 优于 Claude Sonnet 4。平均而言，GLM-4.5 是编码任务上 Claude Sonnet 4 最强劲的竞争者。

#### 4.2.4 通用能力评测

表 6：常用通用对话基准上的结果

| 基准 | GLM-4.5 | GLM-4.5-Air | GPT-4.1 | Claude Sonnet 4 | Gemini 2.5 Pro | Grok 4 | Qwen3 235B | Deepseek R1 0528 | DeepSeek V3 0324 | Kimi K2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MMLU | 90.0 | 87.4 | 90.2 | 91.9 | 91.9 | 91.9 | 90.2 | 89.9 | 89.1 | 89.5 |
| SimpleQA | 26.4 | 14.5 | 42.3 | 18.5 | 54.0 | 51.9 | 45.8 | 27.8 | 27.7 | 31.0 |
| IFEval | 86.1 | 86.3 | 87.4 | 88.7 | 90.8 | 92.4 | 87.8 | 80.0 | 83.4 | 89.8 |
| SysBench | 81.0 | 77.4 | 80.6 | 80.6 | 82.2 | 81.5 | 83.3 | 81.2 | 79.8 | 79.0 |
| MultiChallenge | 52.8 | 42.5 | 38.3 | 55.3 | 57.5 | 65.2 | 58.2 | 46.5 | 37.0 | 54.1 |

为评估模型的通用能力，我们采用一组被广泛采用的开源基准数据集，包括知识密集型评测 MMLU（EM）[14] 与 SimpleQA（Correct）[44]，以及指令遵循评估 IFEval（Prompt Strict）[52]、SysBench（ISR）[29] 与 MultiChallenge [10]。MultiChallenge 是一个多轮对话基准，从四个整合的能力维度评估 LLM。SysBench 通过三级粒度指标，系统性评估 LLM 在多轮对话中遵循系统消息的能力。在 MMLU 基准上，包括 GLM-4.5 在内的几乎所有旗舰模型都表现出相当的水平。反映模型事实知识的 SimpleQA 显示，GLM-4.5（355B）的表现与 DeepSeek V3 和 R1（均为 671B）相近，而参数量几乎只有它们的一半。在 IFEval 基准上，GLM-4.5 优于 DeepSeek R1。在 Sysbench 评测中，GLM-4.5 超越 GPT-4.1、DeepSeek V3 与 Kimi K2。此外，在 MultiChallenge 基准上，它展现出优于 GPT-4.1 与 DeepSeek R1 的表现。

#### 4.2.5 安全性评测

为系统性地评估模型的安全对齐，我们使用了 SafetyBench [51]，一个为评估大语言模型安全性而设计的综合基准。SafetyBench 由 11,435 道多选题组成，覆盖七个不同的安全关切类别，并提供英文与中文两种语言的数据。该基准能够对模型处理潜在有害或敏感话题的能力进行标准化、可扩展的评估。这些类别包括：伦理与道德、违法活动、心理健康、冒犯性、身体健康、隐私与财产，以及不公平与偏见。
我们将 GLM-4.5 与一组其他领先模型进行了评测。结果表明，GLM-4.5 取得了强劲的安全分数，与其他顶级模型相比具备竞争力。其 89.87 的总分与 Kimi-K2（90.48）和 GPT-4.1（89.71）相当。值得注意的是，GLM-4.5 在伦理与道德（94.33）、心理健康（94.67）与身体健康（96.67）领域表现出稳健的性能。虽然在避免与违法活动相关的回答（90.97）以及保护隐私与财产（92.00）方面表现良好，但在应对不公平与偏见方面仍有提升空间，这也是我们研发工作中持续关注的重点。
详细的成绩分布见下表。

表 7：SafetyBench 评测结果

| 模型 | 平均 | 伦理与道德 | 违法活动 | 心理健康 | 冒犯性 | 身体健康 | 隐私与财产 | 不公平与偏见 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.5 | 89.9 | 94.3 | 91.0 | 94.7 | 83.0 | 96.7 | 92.0 | 77.4 |
| GLM-4.5-Air | 87.8 | 91.0 | 90.3 | 92.7 | 83.3 | 92.3 | 90.3 | 74.7 |
| Gemini 2.5 Pro | 90.5 | 94.7 | 91.7 | 95.3 | 84.3 | 97.0 | 92.3 | 78.0 |
| Kimi K2 | 90.5 | 93.0 | 93.3 | 95.0 | 90.3 | 97.3 | 93.0 | 71.3 |
| GPT-4.1 | 89.7 | 92.0 | 94.3 | 95.3 | 85.3 | 95.7 | 91.3 | 74.0 |
| DeepSeek-V3-0324 | 88.8 | 92.3 | 90.7 | 95.0 | 84.7 | 95.7 | 91.0 | 72.3 |
| DeepSeek-R1-0528 | 83.5 | 87.0 | 81.7 | 86.7 | 77.7 | 92.0 | 85.7 | 73.7 |

### 4.3 实际使用体验评测

有时，训练出的 LLM 可能对某些预定义基准过拟合，使得评测结果无法精确反映真实世界的体验。
为克服这一挑战并衡量模型在更真实情境下的表现，我们建立了一套全面的人工评测框架。人类评测特别适合评估开放性问题上的表现，因为在这类问题中，连贯性、相关性与创造力至关重要。这种上手实操的方式支持更细粒度的分析，使我们能够更好地定位薄弱环节，并理解自动指标经常遗漏的模型行为中的质性面向。

#### 4.3.1 通用对话评测

为检验模型的实际应用能力，我们精选了一套多样化的真实场景用户提示数据集。这些提示跨越多种语言，覆盖广泛的类别，包括数学、文本处理、文本生成、主观问答、客观问答、逻辑推理与代码指令。我们对这一集合进行了细致过滤，以确保高质量与适当的难度，同时剔除任何可能危及用户隐私或安全的数据。最终数据集由 660 条提示组成，其中英文 392 条、中文 108 条、其他语言 160 条。对于需要事实性知识的提示，我们标注了正确答案，作为评测的基准真值（ground truth）。

我们在 GLM-4.5、Deepseek-R1-0528 与 Kimi K2 之间进行了对比评测。对每条提示，不同模型的回答以随机顺序呈现，以消除潜在的顺序偏差。随后由同一位固定的评测者对每个回答按 0 到 10 分评分。这种在同一时间为一批比较使用同一评测者的方法，旨在最小化不同个体偏好与主观标准带来的偏差。GLM-4.5 与 Deepseek-R1-0528 的思考内容不会呈现给评测者。
各模型在不同类别与语言上的平均分如下。

##### 英文结果

在英文提示集上，GLM-4.5 取得了最高的总分。它在数学、客观问答与文本生成上表现尤为强劲。

表 8：英文提示上的人工评测得分。Subj. 代表主观（Subjective），Obj. 代表客观（Objective），Text Gen. 代表文本生成（Text Generation）。

| 模型 | 总体 | 数学 | 文本处理 | 主观问答 | 客观问答 | 文本生成 | 逻辑 | 代码 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.5 | 8.66 | 8.72 | 8.00 | 8.36 | 8.82 | 8.61 | 9.25 | 8.53 |
| DeepSeek-R1-0528 | 8.62 | 8.56 | 8.27 | 7.91 | 9.00 | 7.83 | 9.07 | 8.65 |
| Kimi-K2 | 8.13 | 7.22 | 8.00 | 7.45 | 8.86 | 7.06 | 7.07 | 8.71 |

##### 中文结果

在中文提示上，GLM-4.5 同样以最高平均分领先，在文本生成、逻辑推理与代码指令方面表现突出。

表 9：中文提示上的人工评测得分

| 模型 | 总体 | 数学 | 文本处理 | 主观问答 | 客观问答 | 文本生成 | 逻辑 | 代码 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.5 | 8.37 | 7.68 | 8.20 | 8.50 | 8.66 | 9.00 | 9.27 | 8.89 |
| DeepSeek-R1-0528 | 8.05 | 7.76 | 8.07 | 8.00 | 7.89 | 8.59 | 9.00 | 8.67 |
| Kimi-K2 | 7.03 | 7.37 | 6.43 | 7.71 | 6.45 | 8.28 | 7.55 | 8.26 |

##### 其他语言结果

在覆盖其他语言的多语言评测中，GLM-4.5 保持领先，在文本生成与主观问答上表现格外出色。

表 10：其他语言提示上的人工评测得分

| 模型 | 总体 | 数学 | 文本处理 | 文本生成 | 主观问答 | 客观问答 | 代码 | 逻辑 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GLM-4.5 | 8.49 | 8.67 | 8.13 | 8.90 | 9.33 | 8.71 | 7.86 | 8.33 |
| DeepSeek-R1-0528 | 8.27 | 9.44 | 8.38 | 7.86 | 9.44 | 8.22 | 7.64 | 8.17 |
| Kimi-K2 | 6.63 | 7.22 | 6.38 | 7.62 | 7.78 | 6.22 | 6.68 | 7.17 |

#### 4.3.2 编码智能体评测

图 12：GLM-4.5 与其他模型在 CC-Bench 上的正面交锋（head-to-head）评测结果。

![图 13](2508.06471v1/coding_agents_successrate.png)

图 13：CC-Bench 上不同模型的平均工具调用成功率与每次交互的 token 用量。

##### 实验设置

为评估 GLM-4.5 在真实场景中的智能体编码能力，我们构建了 CC-Bench，一个基于 Claude Code 的基准，涵盖 52 个精心设计的编程任务，覆盖多样化的软件开发领域。CC-Bench 的详细任务描述与全部评测轨迹可在 <https://huggingface.co/datasets/zai-org/CC-Bench-trajectories> 获取。我们将 GLM-4.5 与三个强劲基线进行比较：Claude Sonnet 4、Kimi K2 与 Qwen3-Coder。
每个任务都在隔离的容器化环境中执行，以避免跨任务干扰，模型使用预定义的 API 配置初始化。测试由人类专家以多轮交互的方式进行：每个任务以一条标准化提示开始，随后专家根据模型输出迭代调整输入，直至任务完成或失败。为确保公平，同一专家在所有模型上遵循一致的交互策略。

基于这一测试流程，模型表现按以下标准评估：主要指标是任务完成度，由预定义的完成标准判定。出现平局时，以效率与可靠性（包括工具调用成功率与 token 消耗效率）作为次级指标。评测优先考虑功能正确性与任务完成，而非效率指标，从而确保编码能力始终是首要的评估焦点。

##### 结果

在正面交锋评测中，GLM-4.5 相对开源基线展现出强劲性能，与闭源模型相比也具备竞争力，如图 12 所示。具体而言：

- GLM-4.5 对阵 Claude Sonnet 4：胜 40.4%，平 9.6%，负 50.0%
- GLM-4.5 对阵 Kimi K2：胜 53.9%，平 17.3%，负 28.8%
- GLM-4.5 对阵 Qwen3-Coder：胜 80.8%，平 7.7%，负 11.5%

如图 13 所示，GLM-4.5 在工具调用可靠性上尤为突出，取得 90.6% 的最高成功率，相比之下 Claude Sonnet 4 为 89.5%、Kimi-K2 为 86.2%、Qwen3-Coder 为 77.1%。尽管 Claude Sonnet 4 仍然是一个强劲对手，GLM-4.5 在任务完成一致性与智能体执行鲁棒性两个方面均优于其他模型。

#### 4.3.3 逻辑推理评测

为严格评估模型的真实逻辑推理能力，并降低互联网上常见逻辑题的数据污染风险，我们构建了一个全新的高难度评测集。该评测集由新颖且复杂的逻辑推理问题组成，在结构上与互联网上广泛流传的题目不同。每道题都被设计为需要多步逻辑演绎才能得到正确解答。

在本次评测中，我们为每道题建立了统一而细致的评分标准，然后让各模型求解这些问题。每个模型回答的正确性与质量随后由人类专家检查并评分。结果显示竞争格局激烈，GLM-4.5 与领先模型表现相当。

表 11：新颖逻辑推理问题上的专家评测得分

| 模型 | 得分 |
| --- | --- |
| Gemini 2.5 Pro | 65.8 |
| DeepSeek-R1-0528 | 62.1 |
| GLM-4.5 | 62.0 |
| GLM-4.5-Air | 53.4 |
| Kimi K2 | 51.9 |

### 4.4 翻译能力评测

##### 翻译的新范式

如今的翻译已超越简单的文本转换，还需要细腻理解不断演变的网络俚语、文化语境与领域专属术语：

网络用语：准确翻译「yyds」，需要识别它是中文短语「永远的神」（yǒng yuǎn de shén）的缩写，意为 "the eternal god"（永恒之神），从而捕捉其热烈赞美与钦佩的真实情感。

领域昵称：在摄影社区中，识别「胖」（字面意为 "fat white"）十分关键。专业模型可能会翻译错误，而通用模型能理解它是「Canon EF 70-300mm f/4-5.6 IS USM」镜头广为使用的昵称，从而提供精准翻译。

符号：当中文用户在对话中发送一个「鱼」表情来指代二手市场时，模型能否理解这背后的文化梗——它指向「闲鱼」（Xiányú）平台？这考验了模型将视觉符号与网络文化现象建立联系的认知能力。

深度语境推理：翻译「三花公主驾到，速来围观」需要识别「三花」并非人名，而是指猫身上流行的三花（calico）毛色。通用模型能准确推断出这一语境，将该短语地道地译为 "The Calico Princess has arrived! Come and see!"。

这些例子凸显出，现代翻译是一项深深植根于知识与推理的任务。

##### 评测结果

我们测试了 100 个当前工具常错译的高难度真实案例，在盲测人工评测中将 GLM-4.5 与专业翻译模型（Qwen-MT-plus、Qwen-MT-turbo、Seed-X [9]）进行比较（依据含义是否正确传达、语言是否地道，按 0-3 分评分）。结果见表 12。

表 12：精选高难度翻译数据上的人工得分

| 模型 | 平均得分 |
| --- | --- |
| GLM-4.5 | 1.71 |
| Qwen-MT-plus | 0.38 |
| Qwen-MT-turbo | 0.55 |
| Seed-X | 0.65 |

GLM-4.5 显著优于专业模型。例如在翻译「三花公主驾到」时，专业模型在语境理解上失败，而 GLM-4.5 准确传达了其习语含义。

## 5 结论

在本报告中，我们介绍了 GLM-4.5 模型系列，包括 GLM-4.5 与 GLM-4.5-Air。两个模型均采用 MoE 架构，相比以往的 GLM 模型提升了计算效率。GLM-4.5 擅长推理、编码与智能体任务，在开源与专有模型中全球排名第 3。我们发布 GLM-4.5 与 GLM-4.5-Air 的模型权重，以推动大语言模型的应用与研究。

## 6 贡献

贡献者姓名按名字（first name）字母顺序排列。带星号（*）标记的名字表示此后已离开我们团队的成员。

核心贡献者

Bin Chen, Chengxing Xie, Cunxiang Wang, Da Yin, Hao Zeng, Jiajie Zhang, Kedong Wang, Lucen Zhong, Mingdao Liu, Rui Lu, Shulin Cao, Xiaohan Zhang, Xuancheng Huang, Yao Wei, Yean Cheng, Yifan An, Yilin Niu, Yuanhao Wen, Yushi Bai, Zhengxiao Du, Zihan Wang（汪子涵）, Zilin Zhu

贡献者

Bohan Zhang, Bosi Wen, Bowen Wu, Bowen Xu*, Can Huang, Casey Zhao, Changpeng Cai, Chao Yu, Chen Li, Chendi Ge, Chenghua Huang, Chenhui Zhang, Chenxi Xu, Chenzheng Zhu, Chuang Li*, Congfeng Yin, Daoyan Lin, Dayong Yang, Dazhi Jiang, Ding Ai, Erle Zhu, Fei Wang, Gengzheng Pan, Guo Wang, Hailong Sun, Haitao Li, Haiyang Li, Haiyi Hu, Hanyu Zhang, Hao Peng, Hao Tai, Haoke Zhang, Haoran Wang, Haoyu Yang*, He Liu, He Zhao, Hongwei Liu, Hongxi Yan, Huan Liu, Huilong Chen, Ji Li, Jiajing Zhao, Jiamin Ren, Jian Jiao, Jiani Zhao, Jianyang Yan, Jiaqi Wang*, Jiayi Gui, Jiayue Zhao, Jie Liu, Jijie Li, Jing Li, Jing Lu, Jingsen Wang, Jingwei Yuan, Jingxuan Li, Jingzhao Du, Jinhua Du, Jinxin Liu, Junkai Zhi, Junli Gao, Ke Wang, Lekang Yang*, Liang Xu, Lin Fan, Lindong Wu, Lintao Ding, Lu Wang, Man Zhang, Minghao Li, Minghuan Xu, Mingming Zhao, Mingshu Zhai*, Pengfan Du, Qian Dong, Shangde Lei, Shangqing Tu, Shangtong Yang, Shaoyou Lu, Shijie Li, Shuang Li（李泷）, Shuang Li（李爽）, Shuxun Yang, Sibo Yi*, Tianshu Yu, Wei Tian, Weihan Wang, Wenbo Yu, Weng Lam Tam, Wenjie Liang, Wentao Liu, Xiao Wang*, Xiaohan Jia, Xiaotao Gu, Xiaoying Ling, Xin Wang, Xing Fan, Xingru Pan, Xinyuan Zhang, Xinze Zhang, Xiuqing Fu, Xunkai Zhang, Yabo Xu, Yandong Wu, Yida Lu, Yidong Wang, Yilin Zhou, Yiming Pan, Ying Zhang, Yingli Wang, Yingru Li, Yinpei Su, Yipeng Geng, Yitong Zhu, Yongkun Yang*, Yuhang Li, Yuhao Wu*, Yujiang Li, Yunan Liu, Yunqing Wang, Yuntao Li, Yuxuan Zhang, Zezhen Liu, Zhen Yang, Zhengda Zhou, Zhongpei Qiao, Zhuoer Feng, Zhuorui Liu, Zichen Zhang, Zihan Wang（王梓汉）, Zijun Yao, Zikang Wang, Ziqiang Liu, Ziwei Chai, Zixuan Li, Zuodong Zhao*

技术负责人

Aohan Zeng, Xin Lv, Qinkai Zheng, Zhenyu Hou

顾问

Jie Tang, Yuxiao Dong, Juanzi Li, Hongning Wang, Minlie Huang, Bin Xu, Jidong Zhai, Wenguang Chen

致谢

我们感谢北京、上海、天津、杭州、珠海与成都提供的一切支持。
特别感谢我们的客户与社区开发者。

## 参考文献

- [1]

  A. Abbas, K. Tirumala, D. Simig, S. Ganguli, and A. S. Morcos.
  Semdedup: Data-efficient learning at web-scale through semantic deduplication.
  arXiv preprint arXiv:2303.09540, 2023.
- [2]

  C. An, Z. Xie, X. Li, L. Li, J. Zhang, S. Gong, M. Zhong, J. Xu, X. Qiu, M. Wang, and L. Kong.
  Polaris: A post-training recipe for scaling reinforcement learning on advanced reasoning models, 2025.
- [3]

  Y. Bai, X. Lv, J. Zhang, H. Lyu, J. Tang, Z. Huang, Z. Du, X. Liu, A. Zeng, L. Hou, et al.
  Longbench: A bilingual, multitask benchmark for long context understanding.
  In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3119–3137, 2024.
- [4]

  Y. Bai, S. Tu, J. Zhang, H. Peng, X. Wang, X. Lv, S. Cao, J. Xu, L. Hou, Y. Dong, J. Tang, and J. Li.
  LongBench v2: Towards deeper understanding and reasoning on realistic long-context multitasks.
  In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3639–3664, Vienna, Austria, July 2025. Association for Computational Linguistics.
- [5]

  M. Bavarian, H. Jun, N. Tezak, J. Schulman, C. McLeavey, J. Tworek, and M. Chen.
  Efficient training of language models to fill in the middle, 2022.
- [6]

  T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al.
  Language models are few-shot learners.
  Advances in neural information processing systems, 33:1877–1901, 2020.
- [7]

  A. Chen, A. Li, B. Gong, B. Jiang, B. Fei, B. Yang, B. Shan, C. Yu, C. Wang, C. Zhu, et al.
  Minimax-m1: Scaling test-time compute efficiently with lightning attention.
  arXiv preprint arXiv:2506.13585, 2025.
- [8]

  M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al.
  Evaluating large language models trained on code.
  arXiv preprint arXiv:2107.03374, 2021.
- [9]

  S. Cheng, Y. Bao, Q. Cao, L. Huang, L. Kang, Z. Liu, Y. Lu, W. Zhu, Z. Huang, T. Li, et al.
  Seed-x: Building strong multilingual translation llm with 7b parameters.
  arXiv preprint arXiv:2507.13618, 2025.
- [10]

  K. Deshpande, V. Sirdeshmukh, J. B. Mols, L. Jin, E.-Y. Hernandez-Cardona, D. Lee, J. Kritz, W. E. Primack, S. Yue, and C. Xing.
  Multichallenge: A realistic multi-turn conversation evaluation benchmark challenging to frontier llms.
  In Findings of the Association for Computational Linguistics: ACL 2025, pages 18632–18702, 2025.
- [11]

  H. Ding, Z. Wang, G. Paolini, V. Kumar, A. Deoras, D. Roth, and S. Soatto.
  Fewer truncations improve language modeling.
  In Proceedings of the 41st International Conference on Machine Learning, pages 11030–11048, 2024.
- [12]

  F. Gloeckle, B. Y. Idrissi, B. Rozière, D. Lopez-Paz, and G. Synnaeve.
  Better & faster large language models via multi-token prediction.
  arXiv preprint arXiv:2404.19737, 2024.
- [13]

  D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948, 2025.
- [14]

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2).
- [15]

  A. Henry, P. R. Dachapally, S. Pawar, and Y. Chen.
  Query-key normalization for transformers, 2020.
- [16]

  C.-P. Hsieh, S. Sun, S. Kriman, S. Acharya, D. Rekesh, F. Jia, and B. Ginsburg.
  Ruler: What’s the real context size of your long-context language models?
  In First Conference on Language Modeling.
- [17]

  S. Hu, Y. Tu, X. Han, G. Cui, C. He, W. Zhao, X. Long, Z. Zheng, Y. Fang, Y. Huang, et al.
  Minicpm: Unveiling the potential of small language models with scalable training strategies.
  In First Conference on Language Modeling.
- [18]

  A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney, et al.
  Openai o1 system card.
  arXiv preprint arXiv:2412.16720, 2024.
- [19]

  N. Jain, K. Han, A. Gu, W.-D. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica.
  Livecodebench: Holistic and contamination free evaluation of large language models for code.
  In The Thirteenth International Conference on Learning Representations.
- [20]

  C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan.
  Swe-bench: Can language models resolve real-world github issues?
  arXiv preprint arXiv:2310.06770, 2023.
- [21]

  K. Jordan, Y. Jin, V. Boza, Y. Jiacheng, F. Cecista, L. Newhouse, and J. Bernstein.
  Muon: An optimizer for hidden layers in neural networks, 2024.
  URL https://kellerjordan.github.io/posts/muon, 6.
- [22]

  A. Joulin, E. Grave, P. Bojanowski, and T. Mikolov.
  Bag of tricks for efficient text classification.
  In Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers, pages 427–431. Association for Computational Linguistics, April 2017.
- [23]

  A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, et al.
  Deepseek-v3 technical report.
  arXiv preprint arXiv:2412.19437, 2024.
- [24]

  J. Liu, J. Su, X. Yao, Z. Jiang, G. Lai, Y. Du, Y. Qin, W. Xu, E. Lu, J. Yan, et al.
  Muon is scalable for llm training.
  arXiv preprint arXiv:2502.16982, 2025.
- [25]

  M. Luo, S. Tan, J. Wong, X. Shi, W. Y. Tang, M. Roongta, C. Cai, J. Luo, L. E. Li, R. A. Popa, and I. Stoica.
  Deepscaler: Surpassing o1-preview with a 1.5b model by scaling rl.
  https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2, 2025.
  Notion Blog.
- [26]

  S. G. Patil, H. Mao, C. Cheng-Jie Ji, F. Yan, V. Suresh, I. Stoica, and J. E. Gonzalez.
  The berkeley function calling leaderboard (bfcl): From tool use to agentic evaluation of large language models.
  In Forty-second International Conference on Machine Learning, 2025.
- [27]

  G. Penedo, H. Kydlíček, V. Sabolčec, B. Messmer, N. Foroutan, A. H. Kargaran, C. Raffel, M. Jaggi, L. Von Werra, and T. Wolf.
  Fineweb2: One pipeline to scale them all–adapting pre-training data processing to every language.
  arXiv preprint arXiv:2506.20920, 2025.
- [28]

  L. Phan, A. Gatti, Z. Han, N. Li, J. Hu, H. Zhang, C. B. C. Zhang, M. Shaaban, J. Ling, S. Shi, et al.
  Humanity’s last exam.
  arXiv preprint arXiv:2501.14249, 2025.
- [29]

  Y. Qin, T. Zhang, Y. Shen, W. Luo, Y. Zhang, Y. Qiao, Z. Zhou, W. Zhang, B. CUI, et al.
  Sysbench: Can llms follow system message?
  In The Thirteenth International Conference on Learning Representations, 2024.
- [30]

  D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and R. Y. Bowman.
  Gpqa: A graduate-level google-proof q&a benchmark.
  In First Conference on Language Modeling, 2024.
- [31]

  Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
  Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
  arXiv preprint arXiv:2402.03300, 2024.
- [32]

  D. Su, K. Kong, Y. Lin, J. Jennings, B. Norick, M. Kliegl, M. Patwary, M. Shoeybi, and B. Catanzaro.
  Nemotron-cc: Transforming common crawl into a refined long-horizon pretraining dataset.
  arXiv preprint arXiv:2412.02595, 2024.
- [33]

  G. Team, R. Anil, S. Borgeaud, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican, et al.
  Gemini: a family of highly capable multimodal models.
  arXiv preprint arXiv:2312.11805, 2023.
- [34]

  K. Team, Y. Bai, Y. Bao, G. Chen, J. Chen, N. Chen, R. Chen, Y. Chen, Y. Chen, Y. Chen, et al.
  Kimi k2: Open agentic intelligence.
  arXiv preprint arXiv:2507.20534, 2025.
- [35]

  T. T.-B. Team.
  Terminal-bench: A benchmark for ai agents in terminal environments, Apr 2025.
- [36]

  M. Tian, L. Gao, S. Zhang, X. Chen, C. Fan, X. Guo, R. Haas, P. Ji, K. Krongchon, Y. Li, et al.
  Scicode: A research coding benchmark curated by scientists.
  Advances in Neural Information Processing Systems, 37:30624–30650, 2024.
- [37]

  H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al.
  Llama: Open and efficient foundation language models.
  arXiv preprint arXiv:2302.13971, 2023.
- [38]

  K. Vodrahalli, S. Ontanon, N. Tripuraneni, K. Xu, S. Jain, R. Shivanna, J. Hui, N. Dikkala, M. Kazemi, B. Fatemi, R. Anil, E. Dyer, S. Shakeri, R. Vij, H. Mehta, V. Ramasesh, Q. Le, E. Chi, Y. Lu, O. Firat, A. Lazaridou, J.-B. Lespiau, N. Attaluri, and K. Olszewska.
  Michelangelo: Long context evaluations beyond haystacks via latent structure queries, 2024.
- [39]

  F. Wan, W. Shen, S. Liao, Y. Shi, C. Li, Z. Yang, J. Zhang, F. Huang, J. Zhou, and M. Yan.
  Qwenlong-l1: Towards long-context large reasoning models with reinforcement learning.
  arXiv preprint arXiv:2505.17667, 2025.
- [40]

  L. Wang, H. Gao, C. Zhao, X. Sun, and D. Dai.
  Auxiliary-loss-free load balancing strategy for mixture-of-experts.
  arXiv preprint arXiv:2408.15664, 2024.
- [41]

  S. Wang, L. Yu, C. Gao, C. Zheng, S. Liu, R. Lu, K. Dang, X. Chen, J. Yang, Z. Zhang, et al.
  Beyond the 80/20 rule: High-entropy minority tokens drive effective reinforcement learning for llm reasoning.
  arXiv preprint arXiv:2506.01939, 2025.
- [42]

  X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan, Y. Song, B. Li, J. Singh, H. H. Tran, F. Li, R. Ma, M. Zheng, B. Qian, Y. Shao, N. Muennikoff, Y. Zhang, B. Hui, J. Lin, R. Brennan, H. Peng, H. Ji, and G. Neubig.
  Openhands: An open platform for AI software developers as generalist agents.
  In The Thirteenth International Conference on Learning Representations, 2025.
- [43]

  Y. Wang, X. Ma, G. Zhang, Y. Ni, A. Chandra, S. Guo, W. Ren, A. Arulraj, X. He, Z. Jiang, et al.
  Mmlu-pro: A more robust and challenging multi-task language understanding benchmark.
  Advances in Neural Information Processing Systems, 37:95266–95290, 2024.
- [44]

  J. Wei, N. Karina, H. W. Chung, Y. J. Jiao, S. Papay, A. Glaese, J. Schulman, and W. Fedus.
  Measuring short-form factuality in large language models, 2024.
- [45]

  J. Wei, Z. Sun, S. Papay, S. McKinney, J. Han, I. Fulford, H. W. Chung, A. T. Passos, W. Fedus, and A. Glaese.
  Browsecomp: A simple yet challenging benchmark for browsing agents.
  arXiv preprint arXiv:2504.12516, 2025.
- [46]

  Z. Xi, Y. Ding, W. Chen, B. Hong, H. Guo, J. Wang, D. Yang, C. Liao, X. Guo, W. He, et al.
  Agentgym: Evolving large language model-based agents across diverse environments.
  arXiv preprint arXiv:2406.04151, 2024.
- [47]

  A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al.
  Qwen3 technical report.
  arXiv preprint arXiv:2505.09388, 2025.
- [48]

  S. Yao, N. Shinn, P. Razavi, and K. Narasimhan.
  t​a​utau-bench: A benchmark for tool-agent-user interaction in real-world domains.
  arXiv preprint arXiv:2406.12045, 2024.
- [49]

  Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, W. Dai, T. Fan, G. Liu, L. Liu, et al.
  Dapo: An open-source llm reinforcement learning system at scale.
  arXiv preprint arXiv:2503.14476, 2025.
- [50]

  A. Zeng, X. Liu, Z. Du, Z. Wang, H. Lai, M. Ding, Z. Yang, Y. Xu, W. Zheng, X. Xia, et al.
  Glm-130b: An open bilingual pre-trained model.
  In The Eleventh International Conference on Learning Representations.
- [51]

  Z. Zhang, L. Lei, L. Wu, R. Sun, Y. Huang, C. Long, X. Liu, X. Lei, J. Tang, and M. Huang.
  Safetybench: Evaluating the safety of large language models with multiple choice questions.
  arXiv preprint arXiv:2309.07045, 2023.
- [52]

  J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and L. Hou.
  Instruction-following evaluation for large language models.
  arXiv preprint arXiv:2311.07911, 2023.

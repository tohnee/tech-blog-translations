---
title: "ChatGLM：从 GLM-130B 到 GLM-4 的大语言模型家族"
title_en: "ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools"
arxiv: 2406.12793
date: 2024-06-18
source: https://arxiv.org/abs/2406.12793
crawled: 2026-09-22
translated: 2026-09-22
---

# ChatGLM：从 GLM-130B 到 GLM-4 的大语言模型家族

> 原文：[ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4](https://arxiv.org/abs/2406.12793) · 智谱 Z.ai arXiv

GLM 团队

机构：智谱 AI（Zhipu AI）

机构：清华大学

###### 摘要

我们介绍 ChatGLM，一个我们长期以来持续开发、不断演进的大语言模型家族。
本报告主要聚焦 GLM-4 语言系列，包括 GLM-4、GLM-4-Air 与 GLM-4-9B。
它们是我们最有能力的模型，凝聚了从前三代 ChatGLM 中获得的所有洞察与经验。
迄今为止，GLM-4 系列模型在数十万亿（ten trillion）token 上完成预训练，语料以中文和英文为主，并辅以来自 24 种语言的一小部分语料，且主要针对中文与英文使用场景进行了对齐。
高质量的对齐通过多阶段后训练过程实现，其中包括监督微调与基于人类反馈的学习。
评测表明，GLM-4：1) 在 MMLU、GSM8K、MATH、BBH、GPQA 与 HumanEval 等通用指标上紧追或超越 GPT-4；2) 在 IFEval 所测度的指令遵循上接近 GPT-4-Turbo；3) 在长上下文任务上匹敌 GPT-4 Turbo（128K）与 Claude 3；4) 在 AlignBench 所测度的中文对齐上超越 GPT-4。
GLM-4 All Tools 模型经过进一步对齐，能够理解用户意图，并自主决定何时以及使用哪些工具——包括网页浏览器、Python 解释器、文生图模型与用户自定义函数——以高效完成复杂任务。
在实际应用中，它在通过网页浏览获取在线信息、利用 Python 解释器求解数学问题等任务上匹敌甚至超越 GPT-4 All Tools。
在这一历程中，我们开源了一系列模型，包括 ChatGLM-6B（三代）、GLM-4-9B（128K、1M）、GLM-4V-9B、WebGLM 与 CodeGeeX，仅 2023 年一年就在 Hugging Face 上吸引了超过 1000 万次下载。
开源模型可通过 <https://github.com/THUDM> 与 <https://huggingface.co/THUDM> 获取。

> 注 1：GLM 团队：Aohan Zeng, Bin Xu, Bowen Wang, Chenhui Zhang, Da Yin, Dan Zhang, Diego ROJAS, Guanyu Feng, Hanlin Zhao, Hanyu Lai, Hao Yu, Hongning Wang, Jiadai Sun, Jiajie Zhang, Jiale Cheng, Jiayi Gui, Jie Tang, Jing Zhang, Jingyu Sun, Juanzi Li, Lei Zhao, Lindong Wu, Lucen Zhong, Mingdao Liu, Minlie Huang, Peng Zhang, Qinkai Zheng, Rui Lu, Shuaiqi Duan, Shudan Zhang, Shulin Cao, Shuxun Yang, Weng Lam Tam, Wenyi Zhao, Xiao Liu, Xiao Xia, Xiaohan Zhang, Xiaotao Gu, Xin Lv, Xinghan Liu, Xinyi Liu, Xinyue Yang, Xixuan Song, Xunkai Zhang, Yifan An, Yifan Xu, Yilin Niu, Yuantao Yang, Yueyan Li, Yushi Bai, Yuxiao Dong, Zehan Qi, Zhaoyu Wang, Zhen Yang, Zhengxiao Du, Zhenyu Hou, Zihan Wang.

> 注 2：团队成员按名字（first name）字母顺序排列。

图 1：GLM 语言、代码、视觉与智能体模型家族的时间线。本报告的重点是语言模型，即 ChatGLM。API 可通过 <https://bigmodel.cn> 公开获取，开源模型可通过 <https://github.com/THUDM> 访问。

## 1 引言

大语言模型（LLM）的飞速发展有目共睹 [57]。以最成功的模型系列之一——OpenAI 的 GPT 模型为例：2020 年发布的初代 GPT-3 模型 [3] 标志着一次显著的规模跃升，从 GPT-1 的 1.17 亿参数与 GPT-2 的 15 亿参数跃升至 1750 亿参数。
这一规模扩展使这个基于 decoder-only Transformer 的 GPT-3 模型具备了上下文学习与泛化能力：据 OpenAI 介绍，GPT-3.5 系列通过引入指令微调、监督微调（SFT）和/或基于人类反馈的强化学习（RLHF）[29] 在 GPT-3 的基础上更进一步。这如今已成为打造高性能 LLM 的标准流程，PaLM 模型 [6]、LLaMA 模型 [41]、Gemini 模型 [40] 等众多模型皆循此路径。

与广为采用的 LLM 开发实践并行，我们提出了以自回归空白填充（autoregressive blank infilling）目标为特色的通用语言模型（GLM）架构 [11]，并于 2021 年开源了 GLM-10B 模型（见 图 1 中的 GLM 时间线）。
自 2021 年底起，我们开始预训练 GLM-130B [53]。
其目标是训练一个千亿（100B）规模的模型，以匹敌或超越 GPT-3（davinci），同时验证在这一规模上成功训练模型所需的技术，与之同期的努力还包括 OPT-175B [54] 与 BLOOM-176B [33]。
我们于 7 月完成了 GLM-130B 的 400B token 训练与评测，随后于 2022 年 8 月发布了该模型及预训练细节 [53]。
根据 2022 年 11 月的 HELM，GLM-130B 在多个维度上与 GPT-3（davinci）相当 [20]。

在此之后，我们启动了 GLM-130B 上的指令微调。
后来，ChatGPT 进一步促使我们通过 SFT 与 RLHF 对齐基座模型。
我们从零开始创建并精心打磨「提示-回答」对并执行 SFT，同时开始研究如何有效应用 RLHF。
2023 年 3 月 14 日，对齐后的模型 ChatGLM-130B 在 <https://chatglm.cn> 上线。
此外，一个更小的版本 ChatGLM-6B [13] 于同日开源，吸引了远超预期的关注。
它的参数量被设计为 62 亿，目的是：1) 便于预训练与后训练技术及数据选择的快速迭代；2) 借助 INT4 量化在消费级显卡上实现本地部署。
此后，我们持续快速地探索并完善预训练与对齐技术，每隔三个月便推出第二代与第三代 ChatGLM 系列，两代模型均完全从头预训练。

ChatGLM-6B 在约一万亿 token 的中英语料上以 2,048（2K）的上下文长度完成预训练，并主要辅以 SFT。
于六月发布的 ChatGLM2-6B 使用更多高质量数据完成预训练与对齐，相较前代取得大幅提升，包括 MMLU 提升 23%、GSM8K 提升 571%、BBH 提升 60%。
通过采用 FlashAttention 技术 [8]，其上下文长度扩展至 32K。
此外，多查询注意力（Multi-Query Attention）[35] 的引入使推理速度提升了 42%。
更进一步，我们的第二代代码模型 CodeGeeX2-6B 通过追加预训练 6000 亿代码 token 开发而成。
以 HumanEval-X 衡量，它相较初代 CodeGeeX-13B [58] 的 Pass@1全面提升：Python 提升 57%、C++ 提升 71%、Java 提升 54%、JavaScript 提升 83%、Go 提升 56%。
在面向角色化对话的适配中，CharacterGLM [61] 支持在 LLM 上进行有效且安全的角色定制。
通过采用更多样的训练数据集、更充分的训练步数与更优化的训练策略，ChatGLM3-6B 在语义、数学、推理、代码与知识方面的 42 项基准上名列前茅。
从这一代开始，ChatGLM 还支持函数调用与代码解释器，以及复杂的智能体任务 [22; 52; 18]。
在这些研发过程中，我们还开发了参数量为 1.5B、3B、12B、32B、66B 与 130B 的模型，使我们得以验证观察并建立自己的扩展定律（scaling laws）。

带着所有经验教训与积累，我们启动了 GLM-4 的训练。
第一个截断点（cutoff）检查点随后经历了多阶段后训练过程（如 SFT、RLHF、安全对齐），现阶段聚焦中英双语。
随后，它被开发为两个不同版本：GLM-4 与 GLM-4 All Tools，两者均支持 128K 上下文长度。
自 2024 年 1 月 16 日起，GLM-4（0116）已通过 GLM-4 API 在 <https://bigmodel.cn> 上提供，GLM-4 All Tools 则可通过 <https://chatglm.cn> 网站及支持创建个人专属智能体（GLMs）的移动应用使用。
最新的模型是 GLM-4（0520）与 GLM-4-Air（0605），在预训练与对齐两方面均有升级。
GLM-4-Air 以更低的时延与推理成本取得了与 GLM-4（0116）相当的性能。
我们在多种语言基准上对 GLM-4 进行了评测。
这些评测评估了 GLM-4 的英文通用能力、中英双语的指令遵循能力，以及中文的对齐、长上下文与智能体能力。

![图 2](2406.12793v2/alltools-example-2.png)

图 2：GLM-4 All Tools 的一个示例。

首先，在最常用的英文学术基准——MMLU、GSM8K、MATH、BBH、GPQA 与 HumanEval 上，GLM-4 0520 取得了与 GPT-4 0613 [28] 和 Gemini 1.5 Pro [40] 密切相当的表现。
例如，它在 MMLU 上分别得分 83.3，对应后两者的 86.4 与 83.7。
其次，依据 IFEval [62]，GLM-4 在提示级与指令级上的指令遵循能力，在英文与中文上均与 GPT-4-Turbo 大体相当。
第三，在中文语言对齐方面，GLM-4 在 AlignBench [23] 的八个维度上超越 GPT-4，匹敌 GPT-4-Turbo。
最后，在长上下文任务上，以 LongBench-Chat [1] 衡量，GLM-4（128K）模型与 GPT-4 Turbo 和 Claude 3 Opus 的表现相当，分别为 87.3 对 87.2 与 87.7。

表 1：开源的 ChatGLM-6B、ChatGLM2-6B、ChatGLM3-6B 与 GLM-4-9B 的性能。

| 语言 | 数据集 | ChatGLM-6B (2023-03-14) | ChatGLM2-6B (2023-06-25) | ChatGLM3-6B-Base (2023-10-27) | GLM-4-9B (2024-06-05) |
| --- | --- | --- | --- | --- | --- |
| 英语 | GSM8K | 1.5 | 25.9 | 72.3 | 84.0 |
|  | MATH | 3.1 | 6.9 | 25.7 | 30.4 |
|  | BBH | 0.0 | 29.2 | 66.1 | 76.3 |
|  | MMLU | 25.2 | 45.2 | 61.4 | 74.7 |
|  | GPQA | - | - | 26.8 | 34.3 |
|  | HumanEval | 0.0 | 9.8 | 58.5 | 70.1 |
|  | BoolQ | 51.8 | 79.0 | 87.9 | 89.6 |
|  | CommonSenseQA | 20.5 | 65.4 | 86.5 | 90.7 |
|  | HellaSwag | 30.4 | 57.0 | 79.7 | 82.6 |
|  | PIQA | 65.7 | 69.6 | 80.1 | 79.1 |
|  | DROP | 3.9 | 25.6 | 70.9 | 77.2 |
| 中文 | C-Eval | 23.7 | 51.7 | 69.0 | 77.1 |
|  | CMMLU | 25.3 | 50.0 | 67.5 | 75.1 |
|  | GAOKAO-Bench | 26.8 | 46.4 | 67.3 | 74.5 |
|  | C3 | 35.1 | 58.6 | 73.9 | 77.2 |

GLM-4 All Tools 模型经过专门对齐，以更好地理解用户意图并自主选择最合适的工具来完成任务。
例如，它可以通过网页浏览器多轮访问在线信息，使用 Python 解释器求解数学问题，调用文生图模型生成图像，以及调用用户自定义函数。
图 2 展示了一个示例：GLM-4 All Tools 借助网页浏览器与 Python 解释器处理用户查询「搜索 2000 至 2023 年的全球人口，然后计算年均增长率」。
我们的第一手测试表明，在常见任务上它不仅匹敌、而且往往超越 GPT-4 All Tools 的能力。

继三代开源 ChatGLM-6B 模型之后，我们还公开发布了 GLM-4-9B 模型（128K 与 1M 上下文长度）。
GLM-4-9B 在约十万亿 token 的多语言语料上以 8192（8K）的上下文长度完成预训练，并使用与 GLM-4（0520）相同的流水线和数据进行后训练。
在训练算力更少的情况下，它优于 Llama-3-8B [26]，并支持 GLM-4 中 All Tools 的全部功能。
我们还提供了一个实验性模型 GLM-4-9B-Chat-1M，具备 100 万（1M）上下文长度（约 200 万汉字）。
表 1 展示了三代 ChatGLM-6B 模型与 GLM-4-9B 的性能，呈现出 ChatGLM 随时间的渐进式提升。

图 3：从 GLM-130B 到 ChatGLM，再到 ChatGLM2/3，直至 GLM-4 All Tools。

图 3 总结了从 GLM-130B 到 GLM-4 All Tools 的主要改进与特性。
在这段历程中，我们还为代码 LLM（CodeGeeX [58]）、面向图像理解的视觉语言模型（CogVLM [45] 与 CogAgent [16]）以及文生图模型（CogView [9; 10; 59]）的开放发展做出了贡献。
开源模型与数据可通过 <https://github.com/THUDM> 与 <https://huggingface.co/THUDM> 获取。

## 2 ChatGLM 技术

在本节中，我们介绍 ChatGLM 中采用并自主研发的预训练与后训练技术，包括模型架构、预训练数据、对齐以及 All Tools。
我们已发布详细的技术报告，介绍通往 GLM-4 过程中使用的每一项主要技术。

预训练数据。
我们的预训练语料由来自多种来源的多语言（以英文与中文为主）文档构成，包括网页、维基百科、书籍、代码与科研论文。
数据处理流水线主要包括三个阶段：去重、过滤与分词。
去重阶段通过精确去重与模糊去重移除重复或相似的文档，提升数据多样性。
针对网页的过滤阶段通过移除包含冒犯性语言、占位文本、源代码等噪声文档来提升数据质量。
分词阶段将文本转换为 token 序列以供后续处理。
预训练数据中的 token 数量直接影响模型训练速度。
为优化这一环节，我们采用字节级字节对编码（BPE）算法 [34] 分别学习中文与多语言 token，并将其与 tiktoken [27] 中 cl100k_base 分词器的 token 合并，构成规模为 150,000 的统一词表。
在最终训练集中，我们对不同来源重新加权，以提高书籍、维基百科等高质量、具教育价值来源的权重。由此，预训练语料的规模约为十万亿 token。

纵观 ChatGLM 的四代发展，我们的发现与现有研究 [60] 一致：数据质量与多样性对构建有效的 LLM 至关重要。尽管积累了经验与洞察，但迄今为止我们尚未找到一个可以指导数据收集、清洗与选择全过程的根本性原则，这或许能启发未来的研究方向。

模型架构。
GLM 系列 LLM 构建在 Transformer [43] 之上。
在 GLM-130B [53] 中，考虑到当时面临的硬件约束，我们探索了多种选项来稳定其预训练。
具体而言，GLM-130B 采用 DeepNorm [44] 作为层归一化策略，并使用旋转位置编码（RoPE）[38] 以及在 FFN 中使用带 GeLU [15] 激活函数的门控线性单元（Gated Linear Unit）[36]。
在不断探索中，我们研究了提升模型性能与推理效率的不同策略。
近期的 GLM-4 模型采用如下架构设计选择。

- 除 QKV 外不使用偏置（No Bias Except QKV）：
  为提升训练速度，我们移除了所有偏置项，仅保留注意力层 Query、Key、Value（QKV）矩阵中的偏置。
  如此操作后，我们观察到长度外推性能略有改善。
- RMSNorm 与 SwiGLU：
  我们分别采用 RMSNorm 与 SwiGLU 替代 LayerNorm 与 ReLU。
  这两项策略带来了更好的模型性能。
- 旋转位置嵌入（RoPE）：
  我们将 RoPE 扩展为二维形式，以适配 GLM 中的二维位置编码。
- 分组查询注意力（GQA）：
  我们以分组查询注意力（GQA）替代多头注意力（MHA），以削减推理时的 KV cache 大小。
  鉴于 GQA 使用的参数少于 MHA，我们增加了 FFN 的参数量以维持相同的模型规模，即将 $d_{\mathrm{ffn}}$ 设为隐藏层大小的 10/3。

我们模型的上下文长度从 2K（ChatGLM），扩展到 32K（ChatGLM2 与 ChatGLM3），再到 128K 与 1M（GLM-4）。
这些扩展不仅通过上下文扩展——位置编码扩展 [31; 5] 与在长文本上的继续训练 [47]——实现，还得益于长上下文对齐，使 GLM-4 能够有效处理超长上下文（技术细节参见 [1]）。

对齐。
预训练为 LLM 奠定基础，而后训练 [29] 则进一步打磨这些模型，使其与人类偏好对齐，例如理解人类意图、遵循指令以及支持多轮对话。
对 GLM-4 而言，对齐主要通过监督微调（SFT）与基于人类反馈的强化学习（RLHF）[17] 完成。
在 SFT 中，我们发现真实的人类提示与交互（而非基于模板或模型生成的回答）对对齐质量至关重要。
虽然 SFT 在很大程度上使基座模型与人类偏好对齐，RLHF 还能进一步帮助缓解拒绝回答、安全性、生成中双语 token 混杂以及多轮连贯性等问题。

对于第一代模型（ChatGLM-6B 与 ChatGLM-130B），「提示-回答」对主要由模型开发者标注。
对于后续模型，对齐数据是内部标注与从第三方获取的专有数据的组合，并受严格的质量控制。
与现有实践 [42] 类似，标注者需从安全性、事实性、相关性、有用性与人类偏好等多个维度为模型回答打分。

ChatGLM 技术。
在 ChatGLM 的研发过程中，我们提出并将持续发布用于增强其性能的技术。

- LLM 的涌现能力 [12]：
  我们考察了预训练损失与下游任务表现之间的关系，发现相同的预训练损失下，不同模型规模与训练 token 数的 LLM 会产生相同的下游表现。我们还发现，在某些任务（如 MMLU 与 GSM8K）上，只有当预训练损失低于某个阈值后，表现才会超越随机水平。
  因此，我们将涌现能力重新定义为那些预训练损失更低的模型所展现的能力 [12]。
- LongAlign [1]：
  为扩展 LLM 的上下文窗口大小，我们提出了 LongAlign——一套全面的长上下文对齐配方。
  它使 GLM-4 能够以媲美 Claude 2 与 GPT-4 Turbo（1106）的表现处理长上下文文本（最多 128K token）。
- ChatGLM-Math [48]：
  为提升 LLM 的数学问题求解能力，我们提出了 ChatGLM-Math，它利用自我批评（self-critique）而非外部模型或人工标注来进行数据选择。
- ChatGLM-RLHF [17]：
  为使 LLM 与人类反馈对齐，我们提出了 ChatGLM-RLHF——我们将 PPO 与 DPO 应用于 LLM 的实践。
- Self-Contrast [24]：
  为避免对昂贵的人类偏好反馈数据的需求，我们开发了免反馈的对齐策略 Self-Contrast。
  它利用目标 LLM 自身为其 RLHF 对齐自生成大量负样本。
- AgentTuning [52]：
  为提升 LLM 的智能体能力，我们开发了 AgentTuning 框架及 AgentInstruct 指令微调数据集，后者包含智能体与环境之间的高质量交互轨迹。
- APAR [21]：
  为提升 LLM 对具有层级结构回答的推理速度，我们提出了自动并行自回归（auto-parallel auto-regressive，APAR）生成方法。
  它利用指令微调训练 LLM 规划其（并行）生成过程并执行 APAR 生成。
- 基准测试：
  我们还开发了多个开放的 LLM 基准，包括：
  用于将 LLM 作为智能体评估的 AgentBench [25]、
  用于评估 LLM 长上下文处理表现的 LongBench [2]、
  用于测度 ChatGLM 在中文内容上对齐质量的 AlignBench [1]、
  用于在 Python 之外的编程语言上评估 HumanEval [4] 题目的 HumanEval-X [58]，
  以及
  用于测度模型解决实际编程任务能力的 NaturalCodeBench（NCB）。

GLM-4 All Tools。
最新的 ChatGLM 模型是 GLM-4 与 GLM-4 All Tools，两者均使用上述技术训练与对齐。
GLM-4 All Tools 是经过进一步对齐以支持智能体及相关任务的模型版本。
它经过训练，能够自主理解用户意图、规划复杂指令，并调用一个或多个工具（如网页浏览器、Python 解释器与文生图模型）来完成复杂任务。
图 4 展示了 GLM-4 All Tools 系统的整体流水线。
当用户发出复杂请求时，模型会分析任务并逐步规划问题求解过程。
如果它判定无法独立完成任务，就会依次调用一个或多个外部工具，利用它们的中间反馈与结果来帮助解决任务。

基于 GLM-4 的全工具（all-tools）能力，我们还开发了 GLMs 应用平台，允许用户为特定任务创建并定制自己的智能体。
GLMs 不仅支持内嵌的 Python 解释器、网页浏览器、文生图模型，还支持用户自定义函数、API 与外部知识库，以更有效地满足用户需求。

![图 4](2406.12793v2/glm4-alltools.png)

图 4：GLM-4 All Tools 与定制化 GLMs（智能体）的整体流水线。

## 3 GLM-4 能力

我们从多个视角检验 GLM-4 模型的能力，包括学术基准上的基础能力、代码问题求解、英文环境下的智能体能力，以及中英双语的指令遵循与长上下文，还有中文对齐。
如前所述，GLM-4 的预训练以中英文为主，对齐则以中文为主。
在本节中，我们主要报告最新 GLM-4 版本（即 GLM-4（0520）与 GLM-4-Air（0605））的结果，因为在所评测的基准上 GLM-4（0520）略优于其最初的 0116 版本。
评测期间，GLM-4 与 GLM-4-Air 均以 BFloat16 精度部署。

作为基线，我们给出 GPT-4（0603）、GPT-4 Turbo（1106、2024-04-09）、Claude 2、Claude 3 Opus 与 Gemini 1.5 Pro 的结果，它们均取自相应的技术报告或通过其公开 API 测试得到。

总体而言，GLM-4 在标准基准上接近最先进模型（GPT-4-Turbo、Gemini 1.5 Pro 与 Claude 3 Opus），在英文环境下的指令遵循、长上下文、代码问题求解与智能体能力上亦然。
在中文对齐方面，它在基础语言能力、高级中文理解、专业知识与开放性问题问答等多个领域对 SOTA 模型取得强劲表现。
总之，GLM-4 在中文语言任务方面位居最佳之列。
它在中文数学与逻辑推理能力上也展现出与 GPT-4 和 Claude 3 Opus 相当的表现，尽管仍落后于 GPT-4 Turbo。

### 3.1 学术基准评测

为评估基座模型的通用表现，我们选取了六个常用基准，覆盖知识、数学、推理、常识与编程：

- MMLU [14]：从数学、历史、计算机科学等多种考试中收集的多选题。我们将所有选项呈现给模型，要求其选出答案字母。
- GSM8K [7]：8,500 道小学数学应用题（测试集 1,000 道），要求模型运用数学概念求解真实生活情境问题。该基准使用思维链提示 [46]。
- MATH：12,500 道高难度的竞赛级数学题（测试集 5,000 道）。该基准使用思维链提示 [46]。
- BBH [39]：由 23 项高难度 BIG-Bench [37] 任务组成的套件。该基准使用思维链提示 [46]。
- GPQA [32]：一个研究生级别的多选题基准，涵盖生物、化学与物理。
- HumanEval [4]：一个通过自动测试用例检查来衡量合成函数正确性的编程基准。

我们将 GLM-4 与初代 GPT-4 [28] 的表现进行比较。
结果见表 2。
可以看到，GLM-4 达到了 GPT-4 在 MMLU 上准确率的 96.3%，并在其他基准上超越 GPT-4。
总体而言，GLM-4 的基础能力接近 GPT-4-Turbo 与 Claude 3 Opus。

表 2：GLM-4 在学术基准上的性能。

| 模型 | MMLU | GSM8K | MATH | BBH | GPQA | HumanEval |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-4 (0314) | 86.4 | 92.0 | 52.9 | 83.1 | 35.7 | 67.0 |
| GPT-4 Turbo (1106) | 84.7 | 95.7 | 64.3 | 88.3 | 42.5 | 83.7 |
| GPT-4 Turbo (2024-04-09) | 86.7 | 95.6 | 73.4 | 88.2 | 49.3 | 88.2 |
| Claude 3 Opus | 86.8 | 95.0 | 60.1 | 86.8 | 50.4 | 84.9 |
| Gemini 1.5 Pro | 85.9 | 90.8 | 67.7 | 89.2 | 46.2 | 84.1 |
| GLM-4-9B-Chat | 72.4 | 79.6 | 50.6 | 76.3 | 28.8 | 71.8 |
| GLM-4-Air (0605) | 81.9 | 90.9 | 57.9 | 80.4 | 38.4 | 75.7 |
| GLM-4 (0116) | 81.5 | 87.6 | 47.9 | 82.3 | 35.7 | 72.0 |
| GLM-4 (0520) | 83.3 | 93.3 | 61.3 | 84.7 | 39.9 | 78.5 |

### 3.2 指令遵循评测

我们使用新近推出的 IFEval 数据集 [62] 评估 GLM-4 的指令遵循水平。
该数据集包含 541 条提示，派生自 25 条可通过明确标准验证的不同指令（例如，*「以 P.S. I do like the cake 结束你的邮件」* 可通过字符串匹配验证）。
我们遵循 [62] 给出的方法，计算*宽松模式（loose mode）*与*严格模式（strict mode）*下的提示级与指令级准确率。
为进一步评估模型的中文指令遵循表现，我们将原始提示翻译为中文，略去不适用于中文的指令（如大小写相关），并调整评分脚本以适配中文数据。

表 3：GLM-4 在 LLM 指令遵循基准 IFEval [62] 上的性能。「L」代表「宽松（Loose）」，「S」代表「严格（Strict）」；「P」代表「提示（Prompt）」，「I」代表「指令（Instruction）」。

| 模型 | 英文 L-P | 英文 S-P | 英文 L-I | 英文 S-I | 中文 L-P | 中文 S-P | 中文 L-I | 中文 S-I |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4 (0613) | 79.5 | 77.1 | 85.5 | 83.7 | 72.4 | 68.9 | 80.0 | 75.7 |
| GPT-4 Turbo (1106) | 79.1 | 75.4 | 85.1 | 82.4 | 74.3 | 69.1 | 80.8 | 76.5 |
| GPT-4 Turbo (2024-04-09) | 84.5 | 81.2 | 88.7 | 85.9 | 79.3 | 72.6 | 84.2 | 79.1 |
| Claude 2 | 75.0 | 58.0 | 81.7 | 67.7 | 57.1 | 46.5 | 64.9 | 55.1 |
| Claude 3 Opus | 90.6 | 85.5 | 93.7 | 90.0 | 78.3 | 73.3 | 84.3 | 80.4 |
| GLM-4-9B-Chat | 73.0 | 69.0 | 80.3 | 77.2 | 73.0 | 69.0 | 80.3 | 77.2 |
| GLM-4-Air (0605) | 80.4 | 75.2 | 86.1 | 82.3 | 79.3 | 71.2 | 84.0 | 77.3 |
| GLM-4 (0520) | 83.7 | 79.1 | 88.7 | 85.0 | 79.7 | 71.9 | 84.2 | 78.0 |

在*宽松模式*下，GLM-4 在英文与中文上均达到与 GPT-4 Turbo 相当的指令级准确率。
在*严格模式*下，GLM-4 在英文与中文上分别达到 GPT-4 Turbo（2024-04-09）指令级准确率的 99.0% 与 98.6%。

### 3.3 对齐评测

AlignBench [23] 提供了一种自动化的「LLM 即裁判（LLMs-as-Judge）」方法，对 LLM 在中文语境下的对齐进行基准测评。
它由 683 条查询组成，涵盖 8 个不同类别，并使用基于 GPT-4 的多维、经规则校准的逐点参考式评分方法来评估模型回答。
我们在 AlignBench-v1.1 上进行评测，该版本更细致地改进了参考回答的生成质量，尤其是为知识类问题补充了带 URL 的网页人工采集证据——这类问题占总查询数的 66.5%。
在这一版本上，几乎所有 LLM 的得分都低于它们在先前 AlignBench 上的得分。

表 4：GLM-4 在中文对齐 LLM 基准 AlignBench [23] 上的性能。

| 模型 | 数学 | 逻辑 | 语言 | 中文理解 | 问答 | 写作 | 角色扮演 | 专业 | 总分 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4 (0613) | 7.54 | 7.17 | 7.82 | 7.02 | 7.39 | 7.67 | 8.20 | 7.29 | 7.46 |
| GPT-4 Turbo (1106) | 7.85 | 7.66 | 7.90 | 7.22 | 8.24 | 8.53 | 8.46 | 7.95 | 7.90 |
| GPT-4 Turbo (2024-04-09) | 8.32 | 7.67 | 7.60 | 7.57 | 8.37 | 7.75 | 8.18 | 8.59 | 8.00 |
| Claude 2 | 6.39 | 5.85 | 6.75 | 5.72 | 6.68 | 5.87 | 6.86 | 6.56 | 6.26 |
| Claude 3 Opus | 7.27 | 7.11 | 7.94 | 7.71 | 8.21 | 7.61 | 7.73 | 8.02 | 7.53 |
| Gemini 1.5 Pro | 7.07 | 7.77 | 7.31 | 7.22 | 8.55 | 7.83 | 7.79 | 8.52 | 7.47 |
| GLM-4-9B-Chat | 7.00 | 6.01 | 6.69 | 7.26 | 7.97 | 7.59 | 8.10 | 7.52 | 7.01 |
| GLM-4-Air (0605) | 7.69 | 6.95 | 7.53 | 8.00 | 7.90 | 8.01 | 8.35 | 8.09 | 7.65 |
| GLM-4 (0116) | 7.20 | 7.20 | 7.60 | 8.19 | 8.45 | 7.88 | 8.05 | 8.56 | 7.66 |
| GLM-4 (0520) | 7.89 | 7.95 | 8.00 | 7.86 | 8.11 | 8.04 | 8.06 | 8.47 | 8.00 |

结果见表 4。
GLM-4 总体上优于 GPT-4 Turbo、Claude 3 Opus 与 Gemini 1.5 Pro，在所有基线中取得最高总分。
尤其是在中文逻辑推理与语言理解任务上，GLM-4 显著超越所有其他强劲模型。
这些结果展示了它对中文语言与知识的扎实掌握。

GLM-4 与 GPT-4 Turbo（2024-04-09）之间当前的性能差距主要在于数学维度。
我们一直在运用 ChatGLM-Math [48] 中引入的技术（如自我批评）持续增强 GLM 模型的数学推理能力。

### 3.4 长上下文处理能力评测

为评估 GLM-4 在长文本任务上的表现，我们在 LongBench-Chat [1] 上开展评测。该基准集的上下文长度介于 10K 至 100K，覆盖用户经常使用的大量长文本场景，如文档问答、摘要与编程。为了更细致地比较 GLM-4 在不同语言下的表现，我们还按语言对 LongBench-Chat 进行划分，得到两个不同部分：中文与英文。因此我们分别报告两个部分的结果，提供 GLM-4 跨语言能力的细粒度概览。

关于具体的评测设置，我们基于 GPT-4 对每个模型的输出打分，在 LongBench-Chat 内采用少样本策略。此外，鉴于我们的目标是最小化分数波动并获得更可靠的统计结论，我们重复进行了多次评测。随后，我们在表 5 中报告这些多次评测的平均值，以确保最终的性能指标能够全面反映 GLM-4 在多样条件下的表现。结果清楚地表明，GLM-4 的表现在英文提示上与 GPT-4 Turbo 和 Claude 3 Opus 相当，在中文提示上则优于两者中的最佳者。

表 5：GLM-4 在 LongBench-Chat [2] 上的性能。

| 模型 | 英文 | 中文 |
| --- | --- | --- |
| GPT-4 Turbo (1106) | 87.2 | 71.4 |
| GPT-4 Turbo (2024-04-09) | 85.0 | 82.1 |
| Claude 2 | 81.3 | 76.2 |
| Claude 3 Opus | 87.7 | 82.7 |
| GLM-4-9B-Chat | 76.8 | 79.0 |
| GLM-4-Air (0605) | 82.4 | 81.0 |
| GLM-4 (0520) | 87.3 | 84.0 |

### 3.5 真实用户提示下编码能力评测

虽然 HumanEval [4] 已被广泛用于评估 LLM 的代码生成能力，但其大多数题目是入门级算法。
而实际应用中，用户会提出复杂的问题来完成日常工作，其难度通常远超 HumanEval 的范围。
此外，已有工作报告了其自身或其他 LLM 的训练数据受到 HumanEval 污染 [28; 19; 50]，使 HumanEval 上的结果相较以往可信度下降。

因此，除 HumanEval 外，我们还在 NaturalCodeBench（NCB）[55] 上评估 GLM-4。这是一个源自真实用户提示的高难度双语编程基准，反映真实世界编程任务的复杂度。
如表 6 所示，GLM-4 在实际场景中的编程性能与 Claude 3 Opus 接近。
尽管与 GPT-4 系列模型仍有一定差距，但考虑到 GLM-4 的双语均衡特性，在后续迭代中通过更好的训练策略与数据治理，其在 NCB 上的性能仍有很大提升空间。

表 6：GLM-4 在 NaturalCodeBench（NCB）[55] 上的性能。该基准包含面向英文与中文的两种编程语言（Python 与 Java）的真实编程提示。

| 模型 | Python（英文） | Java（英文） | Python（中文） | Java（中文） | 总体 |
| --- | --- | --- | --- | --- | --- |
| GPT-4 (0613) | 55.7 | 51.1 | 53.4 | 51.1 | 52.8 |
| GPT-4 Turbo (1106) | 51.9 | 55.0 | 47.3 | 51.9 | 51.5 |
| GPT-4 Turbo (2024-04-09) | 57.5 | 52.3 | 53.1 | 52.3 | 53.8 |
| Claude 2 | 34.4 | 36.6 | 33.6 | 32.8 | 34.4 |
| Claude 3 Opus | 48.9 | 48.9 | 45.0 | 50.4 | 48.3 |
| Gemini 1.5 Pro | 45.0 | 39.7 | 41.5 | 43.1 | 42.3 |
| GLM-4-9B-Chat | 33.9 | 29.8 | 30.8 | 34.4 | 32.2 |
| GLM-4-Air (0605) | 40.8 | 39.7 | 43.1 | 39.7 | 40.8 |
| GLM-4 (0520) | 51.6 | 42.8 | 45.4 | 48.9 | 47.1 |

### 3.6 函数调用评测

为评估 GLM 模型的函数调用表现，我们在 Berkeley Function Call Leaderboard [49] 上开展评测。该基准包含 2k 组「问题-函数-答案」三元组，从三个类别评估模型的函数调用能力：基于抽象语法树（AST）的评估、通过执行 API 的评估，以及相关性检测。第一类通过 AST 分析将模型输出的函数与函数文档及候选答案进行比较。第二类通过执行生成的函数调用来检查回答的正确性。相关性检测评估模型识别不适合解决用户问题的函数的能力。
结果见表 7。可以看到，GLM-4（0520）的函数调用能力与 GPT-4 Turbo（2024-04-09）相当，而 GLM-4-9B-Chat 显著优于 Llama-3-8B-Instruct。另一个观察是，总体准确率并不随模型规模提升，GLM-4-9B-Chat 甚至可以超越 GLM-4-Air。
另一方面，我们观察到评估真实世界 API 执行结果的执行摘要（execution summary）表现随模型规模平滑提升。

表 7：GLM 在 Berkeley Function Call Leaderboard 上的性能。

| 模型 | AST 摘要 | 执行摘要 | 相关性 | 总体 |
| --- | --- | --- | --- | --- |
| Llama-3-8B-Instruct | 59.25 | 70.01 | 45.83 | 58.88 |
| GPT-4 Turbo (2024-04-09) | 82.14 | 78.61 | 88.75 | 81.24 |
| GPT-4o (2024-05-13) | 85.23 | 80.37 | 81.25 | 82.94 |
| ChatGLM3-6B | 62.18 | 69.78 | 5.42 | 57.88 |
| GLM-4-9B-Chat | 80.26 | 84.40 | 87.92 | 81.00 |
| GLM-4-Air (0605) | 84.34 | 85.93 | 68.33 | 80.94 |
| GLM-4 (0520) | 82.59 | 87.78 | 84.17 | 81.76 |

### 3.7 智能体能力评测

人们广泛观察到，LLM 能够在多样化的环境与情境中充当智能体 [30; 51]，这被称为 LLMs-as-Agents [25]。
因此，我们在 AgentBench [25] 上对 GLM-4 与其他对比 LLM 进行评测。AgentBench 是一个面向文本 LLM 的综合智能体基准，覆盖一系列实际环境，包括基于代码、基于游戏与基于网页的情境。
具体而言，我们在 AgentBench 的 8 个环境中评测了 7 个（数字卡牌游戏除外，与其交互过于耗时）。
总分使用 AgentBench [25] 提供的原始各数据集权重计算。

表 8：GLM-4 在 AgentBench [25] 上的性能。

| 模型 | 操作系统 | 数据库 | 知识图谱 | 横向思维谜题 | 家庭事务 | 网页购物 | 网页浏览 | 总分 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4 (0613) | 42.4 | 32.0 | 58.8 | 16.6 | 78.0 | 61.1 | 29.0 | 3.69 |
| GPT-4 Turbo (1106) | 40.3 | 52.7 | 54.0 | 17.7 | 70.0 | 52.8 | 30.0 | 3.77 |
| GPT-4 Turbo (2024-04-09) | 41.0 | 46.7 | 53.2 | 19.4 | 72.0 | 55.1 | 19.0 | 3.68 |
| Claude 2 | 18.1 | 27.3 | 41.3 | 8.4 | 54.0 | 61.4 | 0.0 | 2.03 |
| Claude 3 Opus | 23.6 | 55.0 | 53.4 | 20.0 | 70.0 | 48.5 | 28.0 | 3.62 |
| GLM-4-Air (0605) | 31.9 | 51.0 | 53.8 | 12.3 | 78.0 | 69.2 | 30.0 | 3.58 |
| GLM-4 (0520) | 36.8 | 52.7 | 51.4 | 15.3 | 82.0 | 68.3 | 29.0 | 3.79 |

结果见表 8。
如表所示，GLM-4 系列模型在智能体任务上表现出相当亮眼的成绩，GLM-4-Air 的结果与 GPT-4 Turbo 和 Claude 3 Opus 相当，GLM-4 则优于它们。
在具体环境方面，我们发现 GLM-4 系列在数据库、家庭事务与网页购物任务上表现尤为出色，而在操作系统、知识图谱与横向思维谜题上与 GPT-4 系列仍存在差距。
这一差距表明，GLM-4 在代码相关的智能体任务与高度交互的语言任务上仍有提升空间。

### 3.8 All Tools 评测

GLM-4 经过进一步对齐，以支持 <https://chatglm.cn> 上的智能体与用户自定义 GLMs 功能，由此得到的模型即 GLM-4 All Tools。
如前所述，GLM-4 All Tools 能够通过自主理解用户意图、逐步规划指令并调用多种工具（包括网页浏览器、Python 解释器与文生图模型，如 CogView3 [59]）来完成复杂任务。
表 9 显示，在用 Python 解释器求解数学问题与用浏览器进行信息检索方面，GLM-4 All Tools（网页版）分别取得了与 ChatGPT-4（网页版）相近的表现。

表 9：GLM-4 All Tools 的性能。

|  |  | GLM-4 All Tools (Web, 0116) | GPT-4 (Web, 0110) |
| --- | --- | --- | --- |
| Python 解释器 | GSM8K | 91.59 | 92.72 |
|  | MATH | 63.60 | 65.00 |
|  | Math23K | 88.50 | 88.40 |
| 浏览器 | 信息检索 | 78.08 | 67.12 |

## 4 安全与风险

我们致力于确保 GLM-4 成为一个安全、负责且无偏的模型。
除应对常见的伦理与公平关切外，我们还仔细评估并缓解模型在真实场景中可能给用户带来的潜在危害。

表 10：GLM-4 在 SafetyBench [56] 上的性能，与 GPT-4 系列模型及 Claude 3 Opus 比较。

| 模型 | 伦理与道德 | 违法活动 | 心理健康 | 冒犯性 | 身体健康 | 隐私与财产 | 不公平与偏见 | 总体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4 (0613) | 92.7 | 93.3 | 93.0 | 87.7 | 96.7 | 91.3 | 73.3 | 89.7 |
| GPT-4 Turbo (1106) | 91.0 | 92.0 | 93.0 | 86.0 | 92.0 | 88.7 | 74.3 | 88.1 |
| GPT-4 Turbo (2024-04-09) | 90.3 | 91.3 | 91.7 | 85.3 | 92.0 | 89.3 | 75.0 | 87.9 |
| Claude 3 Opus | 92.7 | 91.7 | 92.7 | 86.3 | 94.7 | 88.7 | 66.0 | 87.5 |
| GLM-4 (0520) | 92.3 | 91.3 | 93.3 | 86.3 | 92.3 | 88.6 | 66.0 | 87.2 |

风险缓解。
我们在预训练阶段仔细清洗数据，移除包含敏感关键词的文本以及来自预定义黑名单的网页。
在对齐阶段，我们评估每条训练样本的安全性，并移除任何存在潜在风险的样本。
无害性也是在比较多条模型输出进行偏好对齐时的重要标准。

我们设有一支红队（red team），持续用容易诱发不安全回答的刁钻问题挑战模型。
我们收集 GLM-4 的全部有害问答对，并通过人工标注加以改进，用于后续的模型对齐。

安全评测。
我们在 SafetyBench [56] 上评估 GLM-4 模型，该基准从 7 个维度评估每个模型：
*伦理与道德*（不道德行为）、
*违法活动*（法律基础知识）、
*心理健康*（对心理健康的负面影响）、
*冒犯性*（冒犯行为）、
*身体健康*（可能造成身体伤害的危险行为）、
*隐私与财产*（隐私侵犯或财产损失）、
*不公平与偏见*。
我们在 SafetyBench 的中文子集上评估不同模型，该子集通过移除容易被审查的高敏感问题构建，以减轻不同 API 安全政策带来的干扰。

表 10 展示了 GLM-4 与 SOTA 模型的安全结果。
在大多数维度上，GLM-4（0520）展现出有竞争力的安全表现，总体上取得与 Claude 3 Opus 相当的性能。
GLM-4 略微落后于 GPT-4 家族，尤其是在身体健康维度——该维度要求关于物理世界的鲁棒常识以规避潜在风险。
我们已在这一方向投入更多努力，以打造能力更强且更安全的 GLM 模型。

## 5 结论

在本报告中，我们介绍了从 GLM-130B 到 GLM-4（All Tools）的 ChatGLM 大语言模型家族。
在过去一年半的时间里，我们基于第一手经验，在理解大语言模型的各个方面取得了长足进步。
随着每一代模型的开发，团队学习并应用了更有效、更高效的模型预训练与对齐策略。
近期的 ChatGLM 模型——GLM-4（0116、0520）、GLM-4-Air（0605）与 GLM-4 All Tools——通过自主使用外部工具与函数，在理解与执行复杂任务方面展现出显著进步。
这些 GLM-4 模型取得了与 GPT-4 Turbo、Claude 3 Opus 与 Gemini 1.5 Pro 等最先进模型相当（某些情况下更优）的性能，尤其在处理与中文语言相关的任务上。
此外，我们致力于通过开放发布模型权重与这一历程中发展的技术，提升 LLM 的可及性与安全性。
我们的开源模型（包括语言、代码与视觉模型）仅 2023 年一年就在 Hugging Face 上吸引了超过 1000 万次下载。
目前，我们正带着迄今为止所学的一切，研发更强大的模型。
未来，我们将继续通过开源普惠前沿 LLM 技术，并向着「教机器像人类一样思考」的使命推进模型能力的边界。

致谢。
我们感谢所有数据标注者、基础设施运维人员、合作者与合作伙伴，以及智谱 AI 与清华大学中未在本报告中明确提及、但为 ChatGLM 提供了支持与反馈并做出贡献的每一个人。
我们同样感谢智谱 AI 的 Yuxuan Zhang 与 Wei Jia，以及 Hugging Face、ModelScope、WiseModel 等团队的团队，感谢他们在 GLM 系列模型开源工作中的帮助。

## 参考文献

- [1]

  Y. Bai, X. Lv, J. Zhang, Y. He, J. Qi, L. Hou, J. Tang, Y. Dong, and J. Li.
  Longalign: A recipe for long context alignment of large language models, 2024.
- [2]

  Y. Bai, X. Lv, J. Zhang, H. Lyu, J. Tang, Z. Huang, Z. Du, X. Liu, A. Zeng, L. Hou, Y. Dong, J. Tang, and J. Li.
  Longbench: A bilingual, multitask benchmark for long context understanding, 2023.
- [3]

  T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei.
  Language models are few-shot learners.
  In Proceedings of the 34th International Conference on Neural Information Processing Systems, NIPS’20, Red Hook, NY, USA, 2020. Curran Associates Inc.
- [4]

  M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba.
  Evaluating large language models trained on code.
  CoRR, abs/2107.03374, 2021.
- [5]

  S. Chen, S. Wong, L. Chen, and Y. Tian.
  Extending context window of large language models via positional interpolation.
  arXiv preprint arXiv:2306.15595, 2023.
- [6]

  A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts, P. Barham, H. W. Chung, C. Sutton, S. Gehrmann, et al.
  Palm: Scaling language modeling with pathways.
  arXiv preprint arXiv:2204.02311, 2022.
- [7]

  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Pappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and J. Schulman.
  Training verifiers to solve math word problems.
  CoRR, abs/2110.14168, 2021.
- [8]

  T. Dao, D. Fu, S. Ermon, A. Rudra, and C. Ré.
  Flashattention: Fast and memory-efficient exact attention with io-awareness.
  Advances in Neural Information Processing Systems, 35:16344–16359, 2022.
- [9]

  M. Ding, Z. Yang, W. Hong, W. Zheng, C. Zhou, D. Yin, J. Lin, X. Zou, H. Shao, H. Yang, and J. Tang.
  Cogview: Mastering text-to-image generation via transformers, 2021.
- [10]

  M. Ding, W. Zheng, W. Hong, and J. Tang.
  Cogview2: Faster and better text-to-image generation via hierarchical transformers.
  Advances in Neural Information Processing Systems, 35:16890–16902, 2022.
- [11]

  Z. Du, Y. Qian, X. Liu, M. Ding, J. Qiu, Z. Yang, and J. Tang.
  Glm: General language model pretraining with autoregressive blank infilling.
  In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 320–335, 2022.
- [12]

  Z. Du, A. Zeng, Y. Dong, and J. Tang.
  Understanding emergent abilities of language models from the loss perspective, 2024.
- [13]

  T. GLM.
  Chatglm-6b: An open bilingual dialogue language model.
  <https://github.com/THUDM/ChatGLM-6B>, 2023.
- [14]

  D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt.
  Measuring massive multitask language understanding.
  In International Conference on Learning Representations, 2021.
- [15]

  D. Hendrycks and K. Gimpel.
  Gaussian error linear units (gelus).
  arXiv preprint arXiv:1606.08415, 2016.
- [16]

  W. Hong, W. Wang, Q. Lv, J. Xu, W. Yu, J. Ji, Y. Wang, Z. Wang, Y. Zhang, J. Li, B. Xu, Y. Dong, M. Ding, and J. Tang.
  Cogagent: A visual language model for gui agents, 2023.
- [17]

  Z. Hou, Y. Niu, Z. Du, X. Zhang, X. Liu, A. Zeng, Q. Zheng, M. Huang, H. Wang, J. Tang, and Y. Dong.
  Chatglm-rlhf: Practices of aligning large language models with human feedback, 2024.
- [18]

  H. Lai, X. Liu, I. L. Iong, S. Yao, Y. Chen, P. Shen, H. Yu, H. Zhang, X. Zhang, Y. Dong, et al.
  Autowebglm: Bootstrap and reinforce a large language model-based web navigating agent.
  arXiv preprint arXiv:2404.03648, 2024.
- [19]

  Y. Li, S. Bubeck, R. Eldan, A. D. Giorno, S. Gunasekar, and Y. T. Lee.
  Textbooks are all you need ii: phi-1.5 technical report, 2023.
- [20]

  P. Liang, R. Bommasani, T. Lee, D. Tsipras, D. Soylu, M. Yasunaga, Y. Zhang, D. Narayanan, Y. Wu, A. Kumar, B. Newman, B. Yuan, B. Yan, C. Zhang, C. Cosgrove, C. D. Manning, C. Ré, D. Acosta-Navas, D. A. Hudson, E. Zelikman, E. Durmus, F. Ladhak, F. Rong, H. Ren, H. Yao, J. Wang, K. Santhanam, L. Orr, L. Zheng, M. Yuksekgonul, M. Suzgun, N. Kim, N. Guha, N. Chatterji, O. Khattab, P. Henderson, Q. Huang, R. Chi, S. M. Xie, S. Santurkar, S. Ganguli, T. Hashimoto, T. Icard, T. Zhang, V. Chaudhary, W. Wang, X. Li, Y. Mai, Y. Zhang, and Y. Koreeda.
  Holistic evaluation of language models, 2023.
- [21]

  M. Liu, A. Zeng, B. Wang, P. Zhang, J. Tang, and Y. Dong.
  Apar: Llms can do auto-parallel auto-regressive decoding.
  ArXiv, abs/2401.06761, 2024.
- [22]

  X. Liu, H. Lai, H. Yu, Y. Xu, A. Zeng, Z. Du, P. Zhang, Y. Dong, and J. Tang.
  Webglm: Towards an efficient web-enhanced question answering system with human preferences.
  In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pages 4549–4560, 2023.
- [23]

  X. Liu, X. Lei, S. Wang, Y. Huang, Z. Feng, B. Wen, J. Cheng, P. Ke, Y. Xu, W. L. Tam, X. Zhang, L. Sun, H. Wang, J. Zhang, M. Huang, Y. Dong, and J. Tang.
  Alignbench: Benchmarking chinese alignment of large language models, 2023.
- [24]

  X. Liu, X. Song, Y. Dong, and J. Tang.
  Extensive self-contrast enables feedback-free language model alignment, 2024.
- [25]

  X. Liu, H. Yu, H. Zhang, Y. Xu, X. Lei, H. Lai, Y. Gu, H. Ding, K. Men, K. Yang, S. Zhang, X. Deng, A. Zeng, Z. Du, C. Zhang, S. Shen, T. Zhang, Y. Su, H. Sun, M. Huang, Y. Dong, and J. Tang.
  Agentbench: Evaluating llms as agents, 2023.
- [26]

  Meta.
  Introducing meta llama 3: The most capable openly available llm to date.
  <https://ai.meta.com/blog/meta-llama-3/>, 2024.
- [27]

  OpenAI.
  tiktoken.
  <https://github.com/openai/tiktoken>, 2023.
- [28]

  R. OpenAI.
  Gpt-4 technical report.
  arXiv, pages 2303–08774, 2023.
- [29]

  L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al.
  Training language models to follow instructions with human feedback.
  Advances in Neural Information Processing Systems, 35:27730–27744, 2022.
- [30]

  J. S. Park, J. O’Brien, C. J. Cai, M. R. Morris, P. Liang, and M. S. Bernstein.
  Generative agents: Interactive simulacra of human behavior.
  In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology, pages 1–22, 2023.
- [31]

  O. Press, N. Smith, and M. Lewis.
  Train short, test long: Attention with linear biases enables input length extrapolation.
  In International Conference on Learning Representations, 2022.
- [32]

  D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and R. Y. Bowman.
  GPQA: A graduate-level google-proof q&a benchmark.
  CoRR, abs/2311.12022, 2023.
- [33]

  T. L. Scao, A. Fan, C. Akiki, E. Pavlick, S. Ilić, D. Hesslow, R. Castagné, A. S. Luccioni, F. Yvon, M. Gallé, et al.
  Bloom: A 176b-parameter open-access multilingual language model.
  arXiv preprint arXiv:2211.05100, 2022.
- [34]

  R. Sennrich, B. Haddow, and A. Birch.
  Neural machine translation of rare words with subword units.
  In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1715–1725, Berlin, Germany, 2016. Association for Computational Linguistics.
- [35]

  N. Shazeer.
  Fast transformer decoding: One write-head is all you need.
  arXiv preprint arXiv:1911.02150, 2019.
- [36]

  N. Shazeer.
  Glu variants improve transformer, 2020.
- [37]

  A. Srivastava, A. Rastogi, A. Rao, A. A. M. Shoeb, A. Abid, A. Fisch, A. R. Brown, A. Santoro, A. Gupta, A. Garriga-Alonso, A. Kluska, A. Lewkowycz, A. Agarwal, A. Power, A. Ray, A. Warstadt, A. W. Kocurek, A. Safaya, J. Tazarv, A. Xiang, A. Parrish, A. Nie, J. Hussain, A. Askell, A. Dsouza, A. Rahane, A. S. Iyer, A. Andreassen, A. Santilli, A. Stuhlmüller, A. M. Dai, A. La, A. K. Lampinen, A. Zou, A. Jiang, A. Chen, A. Vuong, A. Gupta, A. Gottardi, A. Norelli, A. Venkatesh, S. Gholamidavoodi, A. Tabassum, A. Menezes, A. Kirubarajan, A. Mullokandov, A. Sabharwal, A. Herrick, A. Efrat, A. Erdem, A. Karakas, and et al.
  Beyond the imitation game: Quantifying and extrapolating the capabilities of language models.
  CoRR, abs/2206.04615, 2022.
- [38]

  J. Su, Y. Lu, S. Pan, A. Murtadha, B. Wen, and Y. Liu.
  Roformer: Enhanced transformer with rotary position embedding.
  arXiv preprint arXiv:2104.09864, 2021.
- [39]

  M. Suzgun, N. Scales, N. Schärli, S. Gehrmann, Y. Tay, H. W. Chung, A. Chowdhery, Q. V. Le, E. H. Chi, D. Zhou, and J. Wei.
  Challenging big-bench tasks and whether chain-of-thought can solve them.
  In A. Rogers, J. L. Boyd-Graber, and N. Okazaki, editors, Findings of the Association for Computational Linguistics: ACL 2023, Toronto, Canada, July 9-14, 2023, pages 13003–13051. Association for Computational Linguistics, 2023.
- [40]

  G. Team, R. Anil, S. Borgeaud, Y. Wu, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican, D. Silver, S. Petrov, M. Johnson, I. Antonoglou, J. Schrittwieser, A. Glaese, J. Chen, E. Pitler, T. Lillicrap, A. Lazaridou, O. Firat, J. Molloy, M. Isard, P. R. Barham, T. Hennigan, B. Lee, F. Viola, M. Reynolds, Y. Xu, R. Doherty, E. Collins, C. Meyer, E. Rutherford, E. Moreira, K. Ayoub, M. Goel, G. Tucker, E. Piqueras, M. Krikun, I. Barr, N. Savinov, I. Danihelka, B. Roelofs, A. White, A. Andreassen, T. von Glehn, L. Yagati, M. Kazemi, L. Gonzalez, M. Khalman, J. Sygnowski, A. Frechette, C. Smith, L. Culp, L. Proleev, Y. Luan, X. Chen, J. Lottes, N. Schucher, F. Lebron, A. Rrustemi, N. Clay, P. Crone, T. Kocisky, J. Zhao, B. Perz, D. Yu, H. Howard, A. Bloniarz, J. W. Rae, H. Lu, L. Sifre, M. Maggioni, F. Alcober, D. Garrette, M. Barnes, S. Thakoor, J. Austin, G. Barth-Maron, W. Wong, R. Joshi, R. Chaabouni, D. Fatiha, A. Ahuja, R. Liu, Y. Li, S. Cogan, J. Chen, C. Jia, C. Gu, Q. Zhang,
  J. Grimstad, A. J. Hartman, M. Chadwick, G. S. Tomar, X. Garcia, E. Senter, E. Taropa, T. S. Pillai, J. Devlin, M. Laskin, D. de Las Casas, D. Valter, C. Tao, L. Blanco, A. P. Badia, D. Reitter, M. Chen, J. Brennan, C. Rivera, S. Brin, S. Iqbal, G. Surita, J. Labanowski, A. Rao, S. Winkler, E. Parisotto, Y. Gu, K. Olszewska, Y. Zhang, R. Addanki, A. Miech, A. Louis, L. E. Shafey, D. Teplyashin, G. Brown, E. Catt, N. Attaluri, J. Balaguer, J. Xiang, P. Wang, Z. Ashwood, A. Briukhov, A. Webson, S. Ganapathy, S. Sanghavi, R. Kannan, M.-W. Chang, A. Stjerngren, J. Djolonga, Y. Sun, A. Bapna, M. Aitchison, P. Pejman, H. Michalewski, T. Yu, C. Wang, J. Love, J. Ahn, D. Bloxwich, K. Han, P. Humphreys, T. Sellam, J. Bradbury, V. Godbole, S. Samangooei, B. Damoc, A. Kaskasoli, S. M. R. Arnold, V. Vasudevan, S. Agrawal, J. Riesa, D. Lepikhin, R. Tanburn, S. Srinivasan, H. Lim, S. Hodkinson, P. Shyam, J. Ferret, S. Hand, A. Garg, T. L. Paine, J. Li, Y. Li, M. Giang, A. Neitz, Z. Abbas, S. York, M. Reid, E. Cole,
  A. Chowdhery, D. Das, D. Rogozińska, V. Nikolaev, P. Sprechmann, Z. Nado, L. Zilka, F. Prost, L. He, M. Monteiro, G. Mishra, C. Welty, J. Newlan, D. Jia, M. Allamanis, C. H. Hu, R. de Liedekerke, J. Gilmer, C. Saroufim, S. Rijhwani, S. Hou, D. Shrivastava, A. Baddepudi, A. Goldin, A. Ozturel, A. Cassirer, Y. Xu, D. Sohn, D. Sachan, R. K. Amplayo, C. Swanson, D. Petrova, S. Narayan, A. Guez, S. Brahma, J. Landon, M. Patel, R. Zhao, K. Villela, L. Wang, W. Jia, M. Rahtz, M. Giménez, L. Yeung, H. Lin, J. Keeling, P. Georgiev, D. Mincu, B. Wu, S. Haykal, R. Saputro, K. Vodrahalli, J. Qin, Z. Cankara, A. Sharma, N. Fernando, W. Hawkins, B. Neyshabur, S. Kim, A. Hutter, P. Agrawal, A. Castro-Ros, G. van den Driessche, T. Wang, F. Yang, S. yiin Chang, P. Komarek, R. McIlroy, M. Lučić, G. Zhang, W. Farhan, M. Sharman, P. Natsev, P. Michel, Y. Cheng, Y. Bansal, S. Qiao, K. Cao, S. Shakeri, C. Butterfield, J. Chung, P. K. Rubenstein, S. Agrawal, A. Mensch, K. Soparkar, K. Lenc, T. Chung, A. Pope, L. Maggiore,
  J. Kay, P. Jhakra, S. Wang, J. Maynez, M. Phuong, T. Tobin, A. Tacchetti, M. Trebacz, K. Robinson, Y. Katariya, S. Riedel, P. Bailey, K. Xiao, N. Ghelani, L. Aroyo, A. Slone, N. Houlsby, X. Xiong, Z. Yang, E. Gribovskaya, J. Adler, M. Wirth, L. Lee, M. Li, T. Kagohara, J. Pavagadhi, S. Bridgers, A. Bortsova, S. Ghemawat, Z. Ahmed, T. Liu, R. Powell, V. Bolina, M. Iinuma, P. Zablotskaia, J. Besley, D.-W. Chung, T. Dozat, R. Comanescu, X. Si, J. Greer, G. Su, M. Polacek, R. L. Kaufman, S. Tokumine, H. Hu, E. Buchatskaya, Y. Miao, M. Elhawaty, A. Siddhant, N. Tomasev, J. Xing, C. Greer, H. Miller, S. Ashraf, A. Roy, Z. Zhang, A. Ma, A. Filos, M. Besta, R. Blevins, T. Klimenko, C.-K. Yeh, S. Changpinyo, J. Mu, O. Chang, M. Pajarskas, C. Muir, V. Cohen, C. L. Lan, K. Haridasan, A. Marathe, S. Hansen, S. Douglas, R. Samuel, M. Wang, S. Austin, C. Lan, J. Jiang, J. Chiu, J. A. Lorenzo, L. L. Sjösund, S. Cevey, Z. Gleicher, T. Avrahami, A. Boral, H. Srinivasan, V. Selo, R. May, K. Aisopos, L. Hussenot, L. B.
  Soares, K. Baumli, M. B. Chang, A. Recasens, B. Caine, A. Pritzel, F. Pavetic, F. Pardo, A. Gergely, J. Frye, V. Ramasesh, D. Horgan, K. Badola, N. Kassner, S. Roy, E. Dyer, V. Campos, A. Tomala, Y. Tang, D. E. Badawy, E. White, B. Mustafa, O. Lang, A. Jindal, S. Vikram, Z. Gong, S. Caelles, R. Hemsley, G. Thornton, F. Feng, W. Stokowiec, C. Zheng, P. Thacker, Çağlar Ünlü, Z. Zhang, M. Saleh, J. Svensson, M. Bileschi, P. Patil, A. Anand, R. Ring, K. Tsihlas, A. Vezer, M. Selvi, T. Shevlane, M. Rodriguez, T. Kwiatkowski, S. Daruki, K. Rong, A. Dafoe, N. FitzGerald, K. Gu-Lemberg, M. Khan, L. A. Hendricks, M. Pellat, V. Feinberg, J. Cobon-Kerr, T. Sainath, M. Rauh, S. H. Hashemi, R. Ives, Y. Hasson, Y. Li, E. Noland, Y. Cao, N. Byrd, L. Hou, Q. Wang, T. Sottiaux, M. Paganini, J.-B. Lespiau, A. Moufarek, S. Hassan, K. Shivakumar, J. van Amersfoort, A. Mandhane, P. Joshi, A. Goyal, M. Tung, A. Brock, H. Sheahan, V. Misra, C. Li, N. Rakićević, M. Dehghani, F. Liu, S. Mittal, J. Oh, S. Noury, E. Sezener,
  F. Huot, M. Lamm, N. D. Cao, C. Chen, G. Elsayed, E. Chi, M. Mahdieh, I. Tenney, N. Hua, I. Petrychenko, P. Kane, D. Scandinaro, R. Jain, J. Uesato, R. Datta, A. Sadovsky, O. Bunyan, D. Rabiej, S. Wu, J. Zhang, G. Vasudevan, E. Leurent, M. Alnahlawi, I. Georgescu, N. Wei, I. Zheng, B. Chan, P. G. Rabinovitch, P. Stanczyk, Y. Zhang, D. Steiner, S. Naskar, M. Azzam, M. Johnson, A. Paszke, C.-C. Chiu, J. S. Elias, A. Mohiuddin, F. Muhammad, J. Miao, A. Lee, N. Vieillard, S. Potluri, J. Park, E. Davoodi, J. Zhang, J. Stanway, D. Garmon, A. Karmarkar, Z. Dong, J. Lee, A. Kumar, L. Zhou, J. Evens, W. Isaac, Z. Chen, J. Jia, A. Levskaya, Z. Zhu, C. Gorgolewski, P. Grabowski, Y. Mao, A. Magni, K. Yao, J. Snaider, N. Casagrande, P. Suganthan, E. Palmer, G. Irving, E. Loper, M. Faruqui, I. Arkatkar, N. Chen, I. Shafran, M. Fink, A. Castaño, I. Giannoumis, W. Kim, M. Rybiński, A. Sreevatsa, J. Prendki, D. Soergel, A. Goedeckemeyer, W. Gierke, M. Jafari, M. Gaba, J. Wiesner, D. G. Wright, Y. Wei, H. Vashisht,
  Y. Kulizhskaya, J. Hoover, M. Le, L. Li, C. Iwuanyanwu, L. Liu, K. Ramirez, A. Khorlin, A. Cui, T. LIN, M. Georgiev, M. Wu, R. Aguilar, K. Pallo, A. Chakladar, A. Repina, X. Wu, T. van der Weide, P. Ponnapalli, C. Kaplan, J. Simsa, S. Li, O. Dousse, F. Yang, J. Piper, N. Ie, M. Lui, R. Pasumarthi, N. Lintz, A. Vijayakumar, L. N. Thiet, D. Andor, P. Valenzuela, C. Paduraru, D. Peng, K. Lee, S. Zhang, S. Greene, D. D. Nguyen, P. Kurylowicz, S. Velury, S. Krause, C. Hardin, L. Dixon, L. Janzer, K. Choo, Z. Feng, B. Zhang, A. Singhal, T. Latkar, M. Zhang, Q. Le, E. A. Abellan, D. Du, D. McKinnon, N. Antropova, T. Bolukbasi, O. Keller, D. Reid, D. Finchelstein, M. A. Raad, R. Crocker, P. Hawkins, R. Dadashi, C. Gaffney, S. Lall, K. Franko, E. Filonov, A. Bulanova, R. Leblond, V. Yadav, S. Chung, H. Askham, L. C. Cobo, K. Xu, F. Fischer, J. Xu, C. Sorokin, C. Alberti, C.-C. Lin, C. Evans, H. Zhou, A. Dimitriev, H. Forbes, D. Banarse, Z. Tung, J. Liu, M. Omernick, C. Bishop, C. Kumar, R. Sterneck, R. Foley,
  R. Jain, S. Mishra, J. Xia, T. Bos, G. Cideron, E. Amid, F. Piccinno, X. Wang, P. Banzal, P. Gurita, H. Noga, P. Shah, D. J. Mankowitz, A. Polozov, N. Kushman, V. Krakovna, S. Brown, M. Bateni, D. Duan, V. Firoiu, M. Thotakuri, T. Natan, A. Mohananey, M. Geist, S. Mudgal, S. Girgin, H. Li, J. Ye, O. Roval, R. Tojo, M. Kwong, J. Lee-Thorp, C. Yew, Q. Yuan, S. Bagri, D. Sinopalnikov, S. Ramos, J. Mellor, A. Sharma, A. Severyn, J. Lai, K. Wu, H.-T. Cheng, D. Miller, N. Sonnerat, D. Vnukov, R. Greig, J. Beattie, E. Caveness, L. Bai, J. Eisenschlos, A. Korchemniy, T. Tsai, M. Jasarevic, W. Kong, P. Dao, Z. Zheng, F. Liu, F. Yang, R. Zhu, M. Geller, T. H. Teh, J. Sanmiya, E. Gladchenko, N. Trdin, A. Sozanschi, D. Toyama, E. Rosen, S. Tavakkol, L. Xue, C. Elkind, O. Woodman, J. Carpenter, G. Papamakarios, R. Kemp, S. Kafle, T. Grunina, R. Sinha, A. Talbert, A. Goyal, D. Wu, D. Owusu-Afriyie, C. Du, C. Thornton, J. Pont-Tuset, P. Narayana, J. Li, S. Fatehi, J. Wieting, O. Ajmeri, B. Uria, T. Zhu, Y. Ko, L. Knight,
  A. Héliou, N. Niu, S. Gu, C. Pang, D. Tran, Y. Li, N. Levine, A. Stolovich, N. Kalb, R. Santamaria-Fernandez, S. Goenka, W. Yustalim, R. Strudel, A. Elqursh, B. Lakshminarayanan, C. Deck, S. Upadhyay, H. Lee, M. Dusenberry, Z. Li, X. Wang, K. Levin, R. Hoffmann, D. Holtmann-Rice, O. Bachem, S. Yue, S. Arora, E. Malmi, D. Mirylenka, Q. Tan, C. Koh, S. H. Yeganeh, S. Põder, S. Zheng, F. Pongetti, M. Tariq, Y. Sun, L. Ionita, M. Seyedhosseini, P. Tafti, R. Kotikalapudi, Z. Liu, A. Gulati, J. Liu, X. Ye, B. Chrzaszcz, L. Wang, N. Sethi, T. Li, B. Brown, S. Singh, W. Fan, A. Parisi, J. Stanton, C. Kuang, V. Koverkathu, C. A. Choquette-Choo, Y. Li, T. Lu, A. Ittycheriah, P. Shroff, P. Sun, M. Varadarajan, S. Bahargam, R. Willoughby, D. Gaddy, I. Dasgupta, G. Desjardins, M. Cornero, B. Robenek, B. Mittal, B. Albrecht, A. Shenoy, F. Moiseev, H. Jacobsson, A. Ghaffarkhah, M. Rivière, A. Walton, C. Crepy, A. Parrish, Y. Liu, Z. Zhou, C. Farabet, C. Radebaugh, P. Srinivasan, C. van der Salm, A. Fidjeland,
  S. Scellato, E. Latorre-Chimoto, H. Klimczak-Plucińska, D. Bridson, D. de Cesare, T. Hudson, P. Mendolicchio, L. Walker, A. Morris, I. Penchev, M. Mauger, A. Guseynov, A. Reid, S. Odoom, L. Loher, V. Cotruta, M. Yenugula, D. Grewe, A. Petrushkina, T. Duerig, A. Sanchez, S. Yadlowsky, A. Shen, A. Globerson, A. Kurzrok, L. Webb, S. Dua, D. Li, P. Lahoti, S. Bhupatiraju, D. Hurt, H. Qureshi, A. Agarwal, T. Shani, M. Eyal, A. Khare, S. R. Belle, L. Wang, C. Tekur, M. S. Kale, J. Wei, R. Sang, B. Saeta, T. Liechty, Y. Sun, Y. Zhao, S. Lee, P. Nayak, D. Fritz, M. R. Vuyyuru, J. Aslanides, N. Vyas, M. Wicke, X. Ma, T. Bilal, E. Eltyshev, D. Balle, N. Martin, H. Cate, J. Manyika, K. Amiri, Y. Kim, X. Xiong, K. Kang, F. Luisier, N. Tripuraneni, D. Madras, M. Guo, A. Waters, O. Wang, J. Ainslie, J. Baldridge, H. Zhang, G. Pruthi, J. Bauer, F. Yang, R. Mansour, J. Gelman, Y. Xu, G. Polovets, J. Liu, H. Cai, W. Chen, X. Sheng, E. Xue, S. Ozair, A. Yu, C. Angermueller, X. Li, W. Wang, J. Wiesinger, E. Koukoumidis,
  Y. Tian, A. Iyer, M. Gurumurthy, M. Goldenson, P. Shah, M. Blake, H. Yu, A. Urbanowicz, J. Palomaki, C. Fernando, K. Brooks, K. Durden, H. Mehta, N. Momchev, E. Rahimtoroghi, M. Georgaki, A. Raul, S. Ruder, M. Redshaw, J. Lee, K. Jalan, D. Li, G. Perng, B. Hechtman, P. Schuh, M. Nasr, M. Chen, K. Milan, V. Mikulik, T. Strohman, J. Franco, T. Green, D. Hassabis, K. Kavukcuoglu, J. Dean, and O. Vinyals.
  Gemini: A family of highly capable multimodal models, 2023.
- [41]

  H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample.
  Llama: Open and efficient foundation language models, 2023.
- [42]

  H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, D. Bikel, L. Blecher, C. C. Ferrer, M. Chen, G. Cucurull, D. Esiobu, J. Fernandes, J. Fu, W. Fu, B. Fuller, C. Gao, V. Goswami, N. Goyal, A. Hartshorn, S. Hosseini, R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. Kloumann, A. Korenev, P. S. Koura, M.-A. Lachaux, T. Lavril, J. Lee, D. Liskovich, Y. Lu, Y. Mao, X. Martinet, T. Mihaylov, P. Mishra, I. Molybog, Y. Nie, A. Poulton, J. Reizenstein, R. Rungta, K. Saladi, A. Schelten, R. Silva, E. M. Smith, R. Subramanian, X. E. Tan, B. Tang, R. Taylor, A. Williams, J. X. Kuan, P. Xu, Z. Yan, I. Zarov, Y. Zhang, A. Fan, M. Kambadur, S. Narang, A. Rodriguez, R. Stojnic, S. Edunov, and T. Scialom.
  Llama 2: Open foundation and fine-tuned chat models, 2023.
- [43]

  A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin.
  Attention is all you need, 2023.
- [44]

  H. Wang, S. Ma, L. Dong, S. Huang, D. Zhang, and F. Wei.
  Deepnet: Scaling transformers to 1,000 layers, 2022.
- [45]

  W. Wang, Q. Lv, W. Yu, W. Hong, J. Qi, Y. Wang, J. Ji, Z. Yang, L. Zhao, X. Song, J. Xu, B. Xu, J. Li, Y. Dong, M. Ding, and J. Tang.
  Cogvlm: Visual expert for pretrained language models, 2023.
- [46]

  J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou.
  Chain-of-thought prompting elicits reasoning in large language models.
  In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022.
- [47]

  W. Xiong, J. Liu, I. Molybog, H. Zhang, P. Bhargava, R. Hou, L. Martin, R. Rungta, K. A. Sankararaman, B. Oguz, et al.
  Effective long-context scaling of foundation models.
  arXiv preprint arXiv:2309.16039, 2023.
- [48]

  Y. Xu, X. Liu, X. Liu, Z. Hou, Y. Li, X. Zhang, Z. Wang, A. Zeng, Z. Du, W. Zhao, J. Tang, and Y. Dong.
  Chatglm-math: Improving math problem-solving in large language models with a self-critique pipeline, 2024.
- [49]

  F. Yan, H. Mao, C. C.-J. Ji, T. Zhang, S. G. Patil, I. Stoica, and J. E. Gonzalez.
  Berkeley function calling leaderboard.
  2024.
- [50]

  S. Yang, W.-L. Chiang, L. Zheng, J. E. Gonzalez, and I. Stoica.
  Rethinking benchmark and contamination for language models with rephrased samples.
  arXiv preprint arXiv:2311.04850, 2023.
- [51]

  S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao.
  React: Synergizing reasoning and acting in language models.
  arXiv preprint arXiv:2210.03629, 2022.
- [52]

  A. Zeng, M. Liu, R. Lu, B. Wang, X. Liu, Y. Dong, and J. Tang.
  Agenttuning: Enabling generalized agent abilities for llms, 2023.
- [53]

  A. Zeng, X. Liu, Z. Du, Z. Wang, H. Lai, M. Ding, Z. Yang, Y. Xu, W. Zheng, X. Xia, et al.
  Glm-130b: An open bilingual pre-trained model.
  arXiv preprint arXiv:2210.02414, 2022.
- [54]

  S. Zhang, S. Roller, N. Goyal, M. Artetxe, M. Chen, S. Chen, C. Dewan, M. Diab, X. Li, X. V. Lin, et al.
  Opt: Open pre-trained transformer language models.
  arXiv preprint arXiv:2205.01068, 2022.
- [55]

  S. Zhang, H. Zhao, X. Liu, Q. Zheng, Z. Qi, X. Gu, X. Zhang, Y. Dong, and J. Tang.
  Naturalcodebench: Examining coding performance mismatch on humaneval and natural user prompts.
  arXiv preprint arXiv:2405.04520, 2024.
- [56]

  Z. Zhang, L. Lei, L. Wu, R. Sun, Y. Huang, C. Long, X. Liu, X. Lei, J. Tang, and M. Huang.
  Safetybench: Evaluating the safety of large language models with multiple choice questions.
  arXiv preprint arXiv:2309.07045, 2023.
- [57]

  W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang, J. Zhang, Z. Dong, et al.
  A survey of large language models.
  arXiv preprint arXiv:2303.18223, 2023.
- [58]

  Q. Zheng, X. Xia, X. Zou, Y. Dong, S. Wang, Y. Xue, Z. Wang, L. Shen, A. Wang, Y. Li, T. Su, Z. Yang, and J. Tang.
  Codegeex: A pre-trained model for code generation with multilingual evaluations on humaneval-x, 2023.
- [59]

  W. Zheng, J. Teng, Z. Yang, W. Wang, J. Chen, X. Gu, Y. Dong, M. Ding, and J. Tang.
  Cogview3: Finer and faster text-to-image generation via relay diffusion, 2024.
- [60]

  C. Zhou, P. Liu, P. Xu, S. Iyer, J. Sun, Y. Mao, X. Ma, A. Efrat, P. Yu, L. Yu, S. Zhang, G. Ghosh, M. Lewis, L. Zettlemoyer, and O. Levy.
  Lima: Less is more for alignment, 2023.
- [61]

  J. Zhou, Z. Chen, D. Wan, B. Wen, Y. Song, J. Yu, Y. Huang, L. Peng, J. Yang, X. Xiao, et al.
  Characterglm: Customizing chinese conversational ai characters with large language models.
  arXiv preprint arXiv:2311.16832, 2023.
- [62]

  J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and L. Hou.
  Instruction-following evaluation for large language models.
  arXiv preprint arXiv:2311.07911, 2023.

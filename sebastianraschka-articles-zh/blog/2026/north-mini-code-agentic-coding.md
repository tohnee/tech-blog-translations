---
title: "North Mini Code 编程智能体笔记"
title_en: "North Mini Code Agentic Coding Note"
source: https://sebastianraschka.com/blog/2026/north-mini-code-agentic-coding.html
crawled: 2026-09-06
translated: 2026-09-06
---

# North Mini Code 编程智能体笔记

> 原文：[North Mini Code Agentic Coding Note](https://sebastianraschka.com/blog/2026/north-mini-code-agentic-coding.html)

[North Mini Code](https://huggingface.co/CohereLabs/North-Mini-Code-1.0) 是 Cohere 面向编程智能体任务的开放权重模型。它总参数 300 亿，每个 token 激活 30 亿，采用 Apache 2.0 许可证。

对一个编程智能体来说，这个模型相对紧凑，但它的训练目标很有雄心。Cohere 针对终端工作、仓库级软件工程以及跨多个智能体执行框架（harness）的工具使用对其做了优化。阅读基准测试表时，这一聚焦很重要，因为一个编程智能体是连同它的[提示词格式](https://sebastianraschka.com/glossary/#prompt-template "Prompt Template")、工具、解析器和执行环境一起被评估的。

## 又窄又深的并行 transformer

North Mini Code 建立在 Cohere 的并行 transformer 设计之上。在常规 transformer 块中，[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")先更新隐藏状态，前馈模块再接收它。而在这里，注意力分支和前馈分支从同一个归一化输入出发，它们的输出被一起加到残差流上。

模型使用 49 层，隐藏维度为 2,048。第一层是稠密前馈模块，中间维度为 3,072。其余各层使用稀疏 MoE 模块，有 128 个专家，每个 token 选择 8 个。每个被选中的专家中间维度为 768，使用 [SwiGLU](https://sebastianraschka.com/glossary/#swiglu "SwiGLU")，并通过 sigmoid 门获得路由分数。

注意力以 3:1 的局部-全局节奏交替。堆叠中有 36 层滑动窗口注意力和 13 层全局注意力。滑动窗口注意力覆盖 4,096 token，并使用 RoPE。全局注意力不使用显式的[位置嵌入](https://sebastianraschka.com/glossary/#positional-encoding "Positional Encoding")。

每个注意力层有 32 个查询头和 4 个键值头，即 8:1 的分组查询注意力比例。每个新 token 会在全部 49 层上增加约 98 KiB 的逻辑 [bf16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16") K/V 条目。局部缓存在 4,096 token 后停止增长，而 13 个全局层的缓存会随保留的上下文继续增长。

模型卡支持 256K 输入 token 和最多 64K 输出 token。这对仓库上下文和长智能体轨迹很有用，不过推理内存仍取决于全局注意力缓存、局部窗口、批大小和输出长度。

## 编程智能体与代码生成的区别

该发布把三类侧重点不同的编程评估组合在一起，它们考验的是不同的行为。

[Terminal-Bench](https://www.tbench.ai/) 给模型一个终端和一个环境。智能体必须运行命令、检查输出、修改计划，并最终把环境调整到要求的状态。

[SWE-bench](https://www.swebench.com/) 从一个软件 issue 和一个真实仓库出发。智能体必须定位相关代码、编辑一个或多个文件，并产出一个通过该任务测试的补丁。仓库导航和[工具使用](https://sebastianraschka.com/glossary/#tool-use "Tool Use")是评估的一部分。

[SciCode](https://scicode-bench.github.io/) 和 [LiveCodeBench](https://livecodebench.github.io/) 更接近提示词到代码的评估。它们可能需要大量数学或算法推理，但不包含同样的与仓库和终端的长交互循环。

我发现这个区分比把六行数据都归到一个"编程"标签下更有用。一个模型可能擅长生成自包含的解法，却不太可靠于在数十次工具调用之间维持状态。反过来也有可能。

## 跨编程执行框架的训练

Cohere 使用两个监督微调阶段，随后是[可验证奖励强化学习](https://sebastianraschka.com/glossary/#rlvr "RLVR (Reinforcement Learning with Verifiable Rewards)")。第一个 SFT 阶段在 64K 上下文长度上使用宽泛的混合数据。代码占可训练 token 的 70%，分为 43% 的智能体式工具使用数据和 27% 的单轮编程数据。

第二个阶段在 128K [上下文长度](https://sebastianraschka.com/glossary/#context-length "Context Length")上使用 45 亿 token。它只保留智能体式和面向推理的样本，代码占混合数据的 61%。Cohere 报告了来自约 5,000 个仓库的 70,000 多个可验证任务。训练环境针对 SWE-bench 和 SWE-bench Pro 所用的仓库来源做了去重。

执行框架（harness）的多样性是这套设置的重要部分。SWE-Agent 暴露专门的命令和结构化观察结果。Mini-SWE-Agent 把接口简化为单个 shell 工具。OpenCode 为编辑、搜索、任务跟踪等操作使用分离的类型化工具。Terminal-Bench 的 Terminus 2 则通过纯文本轮次交流。

发布内容报告称，加入少量替代框架的数据让 OpenCode 评估提升了 10%，同时没有降低 SWE-Agent 的成绩。这是 Cohere 自己的消融，但它说明了为什么围绕某一种工具模式（tool schema）训练的模型，在同样的任务以另一种方式呈现时可能会表现挣扎。

## 强化学习改变了什么

智能体 rollout 的长度高度可变。因此 Cohere 把 rollout 生成与学习分开，而不是在同步批次里等待每条轨迹完成。一个 vLLM 边车（sidecar）持续采样，训练器则周期性导出更新后的策略权重。一个带窗口的队列会提前放出一部分已完成的轨迹，而不把整个工作负载切换成完成顺序。

强化学习运行混合了终端和软件工程环境。每个批次包含 512 个 rollout，每个提示词尝试 8 次，上下文上限 128K。终端任务使用带一个终端工具的简单 ReAct 执行框架。软件工程任务使用 SWE-Agent。单元测试提供二元奖励，无效的工具调用得到零奖励。

相对于 SFT 检查点，Cohere 报告 Terminal-Bench v2 上 pass@1 绝对提升 7.9 个百分点，SWE-bench 上提升 3.0 个百分点。Cohere 的分析还显示，最终模型产生了更短的轨迹和更少的格式错误工具调用。这些测量比较的是同一训练设置内的检查点，因此比跨模型表格更能反映 RL 阶段的效果。

## 如何看待发布的[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")表

在 Cohere 的表格中，North Mini Code 在 Terminal-Bench v2 得 36.0，Terminal-Bench Hard 得 31.1，SWE-bench Verified 得 67.6，SWE-bench Pro 得 40.2。Qwen3.6-35B-A3B 在全部四行智能体数据上都更高，分数分别为 51.5、35.0、73.4 和 49.5。

在较短的代码生成任务上排序发生变化。North Mini Code 在 SciCode 上得 38.2，Qwen3.6 为 35.8。在 LiveCodeBench v6 上，Qwen3.6 以 80.4 对 70.3 领先。

Gemma 4 在这张表中呈现出相反的模式。它的 SciCode 和 LiveCodeBench 分数分别为 40.0 和 77.1，而它的 SWE-bench 分数低得多。North Mini Code 的训练聚焦可以解释这种差异的一部分。表格没有提供能把差距归因于单一原因的架构或训练数据消融。

跨模型的数值也来自混合的来源。Cohere 在可得时使用公开报告或 Artificial Analysis，缺失的结果由内部补测。Gemma 4 的智能体分数归于 Qwen 团队。这些是截至 2026 年 6 月 12 日的发布时点数字，但它们并不是一次统一的评估运行。框架版本、工具模式、提示词、推理设置、超时和硬件限制都会影响智能体结果。

## 一个重要的部署细节

模型卡建议在工具调用之间保留模型的推理内容。当助手同时返回推理块和工具调用时，两者都应在加入工具结果之前追加到对话中。丢掉推理状态可能迫使模型在下一轮重新构建它的计划。

发布时，本地部署需要较新的 vLLM 代码，再加上 Cohere 的 Melody 解析器来处理工具调用和推理块。Cohere 提供 bf16 和 FP8 检查点。[LLM Architecture Gallery 卡片](https://sebastianraschka.com/llm-architecture-gallery/#card-north-mini-code-30b-a3b)链接到配置文件和更高分辨率的架构图。

[![North Mini Code 架构与基准测试总览](https://sebastianraschka.com/images/blog/2026/north-mini-code/hero.webp)](https://substack.com/@rasbt/note/c-275332436)

图 1：North Mini Code 使用 49 层并行 transformer，在 128 个专家上做 top-8 路由，并采用 3:1 的滑动窗口-全局注意力节奏。基准测试表混合了 Cohere 结果、公开报告、Artificial Analysis 数值，以及若干内部补测的缺失条目。

来源：我 [Substack 笔记](https://substack.com/@rasbt/note/c-275332436)的扩展网站版，架构、训练与评估细节来自 Cohere 的[发布文](https://huggingface.co/blog/CohereLabs/introducing-north-mini-code)、[模型卡](https://huggingface.co/CohereLabs/North-Mini-Code-1.0)和[配置文件](https://huggingface.co/CohereLabs/North-Mini-Code-1.0/blob/main/config.json)。

---
title: "MiniMax M2 技术报告笔记"
title_en: "MiniMax M2 Technical Report Notes"
source: https://sebastianraschka.com/blog/2026/minimax-m2-technical-report.html
crawled: 2026-09-06
translated: 2026-09-06
---

# MiniMax M2 技术报告笔记

> 原文：[MiniMax M2 Technical Report Notes](https://sebastianraschka.com/blog/2026/minimax-m2-technical-report.html)

[MiniMax M2 系列](https://arxiv.org/abs/2605.26494)是今年早些时候最受关注的开放权重 LLM 家族之一。我最初对它的了解主要是一个能力不错的编程模型系列。这份技术报告有意思的地方在于，它把模型架构与智能体训练和部署背后那些不那么显眼的工作联系了起来。

其中一些设计决策单独看都相当常规，但组合起来更有信息量。MiniMax 保留了全注意力，使用了高度稀疏的专家混合布局，在可执行的软件工程任务上训练，并把工具延迟纳入了强化学习。

## M2 架构速览

旗舰 M2 是一个 62 层的仅解码器 transformer，总参数 2299 亿。每个 token 只有 98 亿参数处于激活状态。每个 [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") 层使用 256 个细粒度专家，通过 sigmoid 门控把每个 token 路由到其中 8 个。

全部 62 层都使用分组查询注意力。每层有 48 个查询头和 8 个键值头，并配有 QK-Norm 和部分旋转位置嵌入（RoPE）。[上下文窗口](https://sebastianraschka.com/glossary/#context-length "Context Length")为 196,608 token，通常约略记作 192K。MiniMax 报告该模型的预训练使用了 29.2 万亿 token。

最初的 M2 还训练了一个多 token 预测模块。M2.5 和 M2.7 把它扩展到三个模块，可以为投机解码（speculative decoding）提供草稿 token。服务栈仍需显式支持才能兑现由此带来的加速。

LLM Architecture Gallery 中的 [MiniMax M2](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-230b)、[MiniMax M2.5](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-5-230b) 和 [MiniMax M2.7](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-7-230b) 卡片概括了这三次发布。

## MiniMax 为什么保留全注意力

注意力消融是我最关注的部分。许多近期模型把全注意力与滑动窗口或线性注意力层混合使用，以降低长上下文成本。MiniMax 测试了一种混合滑动窗口设置，最终在每一层都保留了全注意力。

结果比"全注意力完胜"要细致得多。在 32K token 时，两个版本在两项报告的 RULER 任务上都得到 99 分。监督微调基准测试也是互有胜负：滑动窗口模型在 IFBench 和两项智能体评估上更好，而全注意力模型在 GPQA Diamond、SWE-bench Verified、Terminal-Bench 以及其他若干任务上更好。

更大的差距出现在长上下文[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")评估上。在一个 128K 的 RULER 常见词抽取任务上，全注意力模型得 90 分，滑动窗口版本为 72 分。在两项报告的多对一翻译评估上，全注意力模型也分别领先 15 分和 17.6 分。

报告还给出了这一选择的另一个部署理由。循环或压缩的注意力状态可能对较低精度敏感。一些实现还缺少原生的前缀缓存（prefix caching）以及投机解码的清晰集成路径。前缀缓存对编程智能体尤其有价值，因为许多 rollout 会复用相同的仓库上下文和工具历史。这些是实现层面的约束，而不是所有高效注意力方法固有的限制，但它们有助于解释 MiniMax 的决定。

## 一次受控的细粒度 MoE 对比

MoE 消融很有用，因为 MiniMax 把总参数、激活参数和训练 token 都保持不变。两个受测模型都是 178 亿总参数、每 token 激活 20 亿、训练 5000 亿 token。

基线模型有 32 个较大的专家并选择 2 个。细粒度版本把专家容量拆分成 128 个更小的专家并选择 8 个。这在保持激活参数预算相近的同时，让每个 token 可以组合一组更具体的专家。

报告的最大提升出现在 MATH 上，从 19.6 提到 24.1，以及 [HumanEval](https://sebastianraschka.com/glossary/#benchmark "Benchmark") 上，从 29.7 提到 32.5。在 MMLU、ARC-Challenge 和 KorBench 上差异要小得多。我的解读是：在固定算力预算下，更细的专家粒度可能有益，收益大小取决于任务。

## 把 GitHub 拉取请求变成智能体任务

软件工程数据流水线从包含测试的已合并 GitHub 拉取请求开始。一个智能体搭建可运行的 Docker 环境，流水线提取出那些在补丁之前应当失败、之后应当通过的测试。额外的检查确保问题描述、仓库状态和奖励彼此一致。

MiniMax 随后从相同的仓库派生出更多任务。转换方式包括缺陷注入、提交合并、测试编写和代码审查。报告称，由此产生的环境覆盖十多种编程语言。

这条流水线是模型配方的重要组成部分。一个编程智能体需要的不只是代码补全数据。它必须检查仓库、运行命令、解读失败原因、编辑多个文件，并满足[验证器](https://sebastianraschka.com/glossary/#verifier "Verifier")的要求。可运行的环境把这些行为变成带有具体奖励的训练轨迹。

## 交错思考与墙钟时间奖励

MiniMax 在工具调用轮次之间保留模型的推理块。在报告的消融中，移除较早的推理块一致地降低了智能体性能，对深度搜索和软件工程任务的影响最大。这在直觉上说得通：一条长的智能体轨迹包含部分结论、被否决的假设和约束条件，在每次工具调用之后重新构建它们可能代价高昂。

强化学习目标还包含任务完成时间奖励。它把一次 rollout 的实际耗时（wall-clock time）与参考时间比较，完成时间越长奖励越低。当有多个独立动作可用时，该奖励会偏向并行[工具使用](https://sebastianraschka.com/glossary/#tool-use "Tool Use")。它也能阻止一个正确的智能体用不必要的慢路线完成任务。

这个细节容易被忽视，因为大多数模型评估只关注正确性和 token 数量。对交互式智能体而言，流逝的时间是一项独立的成本。两条轨迹可以使用相近的 token 数量，但如果其中一条把每个工具调用都串行执行，两者的体验会非常不同。

## 如何理解自我进化的结果

报告中最强的自我进化主张涉及 M2.7 和 MiniMax 内部的模型迭代系统（Model Iteration System）。研究人员定义实验后，模型可以检查训练运行、阅读日志、诊断指标变化、调试代码并调整配置。MiniMax 估计该系统承担了其日常 RL 迭代工作量的 30% 到 50%。

在另一项实验中，M2.7 在一个内部编程脚手架（scaffold）上完成了 100 轮自主工作。MiniMax 报告，在模型修改代码并调参之后，其内部评估提升了 30%。

这两个数字都是内部测量，报告也没有提供足以独立复现的细节。因此我会把它们视为 MiniMax 如何在自己的开发循环中使用模型的例子。它们仍然值得注意，因为优化的对象是后续模型运行所使用的基础设施。

对我来说，全注意力决策是贯穿整份报告的最清晰主线。架构、训练数据、智能体执行框架（harness）和服务系统被放在一起评估。如果一种更便宜的注意力机制会削弱长上下文行为或阻止前缀复用，它就没有那么有吸引力。同样，当训练设置中包含可执行的环境和可靠的测试时，编程基准测试才更有信息量。

[![MiniMax M2 技术报告要点](https://sebastianraschka.com/images/blog/2026/minimax-m2-report/hero.webp)](https://substack.com/@rasbt/note/c-266029305)

图 1：报告中的滑动窗口注意力消融、细粒度 MoE 对比，以及软件工程数据流水线。基准测试数值来自 MiniMax 自己的实验，而非独立评估。

来源：我 [Substack 笔记](https://substack.com/@rasbt/note/c-266029305)的扩展网站版，架构与训练细节来自 [MiniMax M2 技术报告](https://arxiv.org/abs/2605.26494)。

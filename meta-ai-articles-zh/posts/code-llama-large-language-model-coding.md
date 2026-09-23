---
title: "推出 Code Llama：面向编程的最先进大语言模型"
title_en: "Introducing Code Llama, a state-of-the-art large language model for coding"
date: 2023-08-24
source: https://ai.meta.com/blog/code-llama-large-language-model-coding
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 Code Llama：面向编程的最先进大语言模型

> 原文：[Introducing Code Llama, a state-of-the-art large language model for coding](https://ai.meta.com/blog/code-llama-large-language-model-coding) · Meta AI（Wayback 存档）

**要点**

- Code Llama 是一款最先进的大语言模型（LLM），能够根据代码和自然语言提示生成代码以及关于代码的自然语言。
- Code Llama 可免费用于研究和商业用途。
- Code Lamma 基于 Llama 2 构建，提供三种模型：Code Llama（基础代码模型）；Code Llama - Python（针对 Python 特化）；以及 Code Llama - Instruct（经微调以理解自然语言指令）。
- 在我们自己的基准测试中，Code Llama 在代码任务上超越了公开可用的最先进 LLM。

今天，我们发布 Code Llama——一个可以使用文本提示生成代码的大语言模型（LLM）。在公开可用的 LLM 中，Code Llama 在代码任务上处于最先进水平，有望让当前开发者的工作流更快、更高效，并降低编程学习者的入门门槛。Code Llama 有潜力作为生产力与教育工具，帮助程序员编写更健壮、文档更完善的软件。

生成式 AI 领域正在快速演进，我们相信，以开放的方式对待当今的 AI，是开发创新、安全、负责的新 AI 工具的最佳途径。我们以与 Llama 2 相同的社区许可证发布 Code Llama。

## Code Llama 如何工作

Code Llama 是 Llama 2 的代码特化版本：通过在其代码专属数据集上进一步训练 Llama 2、并从同一数据集中采样更多数据进行更长时间训练而创建。本质上，Code Lamma 在 Llama 2 的基础上具备了增强的编程能力。它可以根据代码和自然语言提示（例如「给我写一个输出斐波那契数列的函数」）生成代码以及关于代码的自然语言，还可用于代码补全和调试。它支持当今使用的许多最流行语言，包括 Python、C++、Java、PHP、TypeScript（JavaScript）、C# 和 Bash（完整列表见我们的研究论文）。

我们发布三种规模的 Code Llama，参数量分别为 7B、13B 和 34B。每个模型都使用 5000 亿（500B）token 的代码及代码相关数据训练。7B 和 13B 的基础与指令模型还接受了填充中间内容（fill-in-the-middle，FIM）能力训练，能够把代码插入现有代码之中，这意味着它们开箱即可支持代码补全等任务。

这三种模型满足不同的服务与时延需求。例如，7B 模型可以在单个 GPU 上提供服务。34B 模型返回最佳结果、能提供更好的编程辅助，而更小的 7B 和 13B 模型速度更快，更适合需要低时延的任务，比如实时代码补全。

Code Llama 模型在最多 100000 个 token 的上下文下都能提供稳定生成。所有模型都在 16000 token 的序列上训练，并在最多 100000 token 的输入上表现出改进。更长的输入序列不仅是生成更长程序的前提，还为代码 LLM 解锁了令人兴奋的新用例。例如，用户可以向模型提供来自其代码库的更多上下文，使生成内容更切题。它还有助于大型代码库中的调试场景——对所有与具体问题相关的代码保持掌握对开发者来说可能颇具挑战。当开发者面对一大段需要调试的代码时，可以把整段代码完整地传给模型。

此外，我们进一步微调了 Code Llama 的两个变体：Code Llama - Python 和 Code Llama - Instruct。Code Llama - Python 是 Code Llama 的语言特化版本，在 1000 亿（100B）token 的 Python 代码上进一步微调。由于 Python 是代码生成领域基准测试最多的语言——也由于 Python 和 PyTorch 在 AI 社区中扮演重要角色——我们相信特化模型能提供额外价值。Code Llama - Instruct 是 Code Llama 的指令微调与对齐版本。指令微调延续了训练过程，但目标不同：模型接收「自然语言指令」输入及期望输出，这使其更擅长理解人类对提示的期待。

每当使用 Code Llama 进行代码生成时，我们都推荐使用 Code Llama - Instruct 变体，因为 Code Llama - Instruct 经过微调，可以用自然语言生成有帮助且安全的回答。我们不推荐使用 Code Llama 或 Code Llama - Python 执行通用自然语言任务，因为这两个模型都不是为遵循自然语言指令而设计的。Code Llama 专精于代码相关任务，不适合作为其他任务的基础模型。使用 Code Llama 模型时，用户必须遵守我们的许可证和可接受使用政策。

## 评估 Code Llama 的性能

为了测试 Code Llama 相对现有方案的性能，我们使用了两个流行的编程基准：HumanEval 和 Mostly Basic Python Programming（MBPP）。HumanEval 测试模型基于文档字符串补全代码的能力，MBPP 测试模型基于描述编写代码的能力。我们的基准测试表明，Code Llama 的表现优于开源的代码专用 LLM，也超越了 Llama 2。例如，Code Llama 34B 在 HumanEval 上得到 53.7%、在 MBPP 上得到 56.2%，与其他最先进的开放方案相比均为最高，并与 ChatGPT 相当。

与所有前沿技术一样，Code Llama 也存在风险。负责任地构建 AI 模型至关重要，我们在发布 Code Llama 之前采取了大量安全措施。作为红队（red teaming）工作的一部分，我们对 Code Llama 生成恶意代码的风险进行了量化评估。我们构造了以明确意图索取恶意代码的提示，并将 Code Llama 对这些提示的回答与 ChatGPT（GPT3.5 Turbo）进行对比评分。结果发现 Code Llama 给出的回答更安全。来自负责任 AI、攻击性安全工程、恶意软件开发和软件工程领域专家的红队工作详情可在我们的研究论文中查阅。

## 发布 Code Llama

程序员已经在使用 LLM 协助各种任务，从编写新软件到调试现有代码。目标是让开发者的工作流更高效，从而专注于工作中最具人性的部分，而非重复性任务。在 Meta，我们相信 AI 模型——尤其是编程 LLM——无论在创新还是安全层面，都最能从开放方式中受益。公开可用的代码专用模型可以促进改善人们生活的新技术的开发。通过发布 Code Lamma 这样的代码模型，整个社区可以评估其能力、发现问题并修复漏洞。

Code Llama 的训练配方可在我们的 GitHub 仓库获取，模型权重也已开放下载。

## 负责任地使用

我们的研究论文披露了 Code Llama 开发的细节以及我们进行基准测试的方式，还提供了关于模型局限、我们遇到的已知挑战、已采取的缓解措施以及我们打算研究的未来挑战的更多信息。我们还更新了《负责任使用指南》，其中包含负责任地开发下游模型的指引，包括：定义内容政策与缓解措施；准备数据；微调模型；评估与改进性能；应对输入和输出层面的风险；在用户交互中建立透明度与报告机制。

开发者应使用代码专属的评估基准评估其模型，并针对代码专属用例（如生成恶意软件、计算机病毒或恶意代码）开展安全研究。我们还建议利用安全数据集进行自动与人工评估，并在对抗性提示上进行红队测试。

## 生成式 AI 编程的未来

Code Llama 旨在为各行各业的软件工程师提供支持——包括研究、工业界、开源项目、非政府组织和企业。但需要支持的场景仍远多于我们的基础和指令模型所能服务的范围。我们希望 Code Llama 能激励他人在 Llama 2 之上构建新的创新工具，用于研究和商业产品。

## 立即试用 Code Llama

- Code Llama GitHub 仓库
- 下载 Code Llama 模型
- 阅读研究论文：Code Llama: Open foundation models for code

---
title: "Grok 4.6 发布"
title_en: "Introducing Grok 4.6"
date: 2026-08-12
source: https://x.ai/news/grok-4-6
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 4.6 发布

> 原文：[Introducing Grok 4.6](https://x.ai/news/grok-4-6) · xAI

[返回新闻列表](/news)

2026 年 8 月 12 日

Grok 4.6 在 Grok 4.5 的基础上更进一步，特别聚焦于长时间运行的智能体以及更具雄心的交互式和视觉工作。

[免费试用](https://x.ai/build)[开始构建](https://console.x.ai)

今天我们发布 **Grok 4.6**。Grok 4.6 基于 [Grok 4.5](/news/grok-4-5) 进一步构建，特别聚焦于长时间运行的智能体以及更具雄心的交互式和视觉工作。它能在许多步骤中坚持完成复杂任务，无论是研究一个课题、分析信息、跨代码库工作，还是把一个想法变成打磨完善的应用或工作成果。

[](https://media.x.ai/v1/website/final-vid-aug-12-c4794904.mp4)

0:00 / 0:00

Grok 4.6 在多项智能体编码和知识工作基准上达到前沿智能水平。它在 Artificial Analysis Intelligence Index（九项基准的综合分数）上与 GPT-5.6 Sol 持平。

AA IntelligenceGDPVal-AADeepSWE 1.1CursorBench 3.2FrontierCode 1.1

0204060AA Intelligence Index62Fable 5 Max61Grok 4.661GPT-5.6 Sol Max56Grok 4.5 High

竞品数据取自各开发商公开发布的系统卡或基准排行榜

对比 Grok 4.6 与其他领先模型在 AA Intelligence、GDPVal-AA、DeepSWE 1.1、CursorBench 3.2 和 FrontierCode 1.1 上的基准柱状图。竞品数据取自各开发商公开发布的系统卡或基准排行榜。

Grok 4.6 今天起在 [Cursor](https://cursor.com) 和 [Grok Build](https://x.ai/build) 中可用。第一周内，我们在 [Grok Build](https://x.ai/build) 和 [Cursor](https://cursor.com) 中提供 2 倍的内置用量，方便你立即开始体验 4.6。

## [Grok 4.6 的训练](#training-grok-46)

Grok 4.6 经历了比 Grok 4.5 更长的补充训练，使用了为推理和高级技术概念精选的模型生成数据、高质量工程数据，以及改进的优化器和训练配方。这为随后的 SFT 和 RL 阶段打下了更坚实的基础。

随后，我们用 Grok 4.5 跨不同推理努力级别、智能体框架以及 STEM、软件工程、知识工作等领域重新生成了 SFT 轨迹，并用基于模型的检查过滤掉有问题的轨迹。得到的 SFT 检查点表现出强劲的性能和改进的行为。

Grok 4.6 在广泛的智能体 RL 任务上训练，包括知识工作、通用编码，以及面向内核优化、Web 开发、计算机辅助设计等领域的专用环境。

## [把宏大想法变成可用的项目](#turning-ambitious-ideas-into-working-projects)

我们在专为拉开模型能力边界、考验多步骤持续工作而设计的项目上测试了 Grok 4.6。我们发现该模型尤其擅长把宽泛的产品想法变成可用的第一版。它可以研究陌生领域、搭建应用结构、实现核心交互，并经过几轮反馈持续打磨结果。

在更长的轨迹上，我们也开始看到更多的自测试和自验证——模型会在继续之前检查自己的工作。

相比我们在 Grok 4.5 上常见的表现，Grok 4.6 在视觉和交互类项目上能产出更强的初稿。给定一个具体的产品想法，它能够一次性建立应用的结构和视觉语言。这使它对那些「以有实质内容的版本起步、再在循环中迭代」最快见效的项目尤为有用。

## [安全与能力](#safety-and-capabilities)

Grok 4.6 的防护措施已随模型能力同步改进和校准。

我们的安全栈旨在让合法用例的效用与安全最大化，使 Grok 4.6 在漏洞修补、加速工程设计周期、增强 AI 研究等领域既乐于助人又安全可靠。

我们的防护评测工作反映了 Grok 4.6 扩展的能力：这是我们迄今覆盖面最广的部署前能力与防护校准测试套件，并辅以广泛的部署后测试和第三方测试。

## [评测](#evals)

Grok 4.6 High

Grok 4.5 High

GPT-5.6 Sol Max

Fable 5 Max

AA Intelligence Index

61

56

61

62

GDPVal-AA v2

1753

1526

1728

1741

CursorBench v3.2

69.9%

66.7%

67.2%

70.5%

DeepSWE v1.1

65.9%

54%

73%

70%

FrontierCode v1.1 (Extended)

61.3%

56.6%

60.6%

63.6%

APEX-Agents

57.5%

47.1%

56.7%

59.2%

Terminal-Bench v3.0

26%

15.7%

34.6%

34.1%

APEX-SWE

56.4%

53.6%

—

58.8%

AA-Briefcase

1577

1313

1502

1574

Harvey LAB (Vals)

15.8%

12.9%

2.5%

11.3%

每项评测的最佳分数以粗体标示。第三方模型分数取自其自行报告或公开可得结果中的最佳值。

## [开始使用 Grok 4.6](#get-started-with-grok-46)

Grok 4.6 今天起在 [Cursor](https://cursor.com) 和 [Grok Build](https://x.ai/build) 中可用。它也可通过 [API](https://console.x.ai) 以及 OpenRouter、Vercel、Cloudflare 等合作伙伴使用。

定价为每百万输入 token 2 美元起、每百万输出 token 6 美元起。此外还有一个价格为其两倍的快速变体。

第一周内，我们在 [Grok Build](https://x.ai/build) 和 [Cursor](https://cursor.com) 中提供 2 倍的内置用量，方便你立即开始体验 4.6。

### 创建 API 密钥

今天就通过 SpaceXAI API 开始用 Grok 4.6 构建。

[开始构建](https://console.x.ai/team/default/api-keys)

### API 文档

阅读文档，把 Grok 4.6 集成到你的技术栈中。

[阅读文档](https://docs.x.ai)

### 在 Grok Build 中免费试用

今天就到 [x.ai/build](/build) 开始。

`$ curl -fsSL https://x.ai/cli/install.sh | bash`

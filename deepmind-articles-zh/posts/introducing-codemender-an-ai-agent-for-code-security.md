---
title: "推出 CodeMender：用于代码安全的 AI 智能体"
title_en: "Introducing CodeMender: an AI agent for code security"
source: https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/
site: deepmind
date: 2025-10-06
crawled: 2026-09-13
translated: 2026-09-13
---

# 推出 CodeMender：用于代码安全的 AI 智能体

> 原文：[Introducing CodeMender: an AI agent for code security](https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/) · Google DeepMind

使用先进的 AI 修复关键软件漏洞

今天，我们分享关于 CodeMender 研究的早期成果——CodeMender 是一个新的 AI 驱动的智能体，能够自动改进代码安全。

软件漏洞向来以难以发现和修复、耗费开发者大量时间而著称，即便使用模糊测试（fuzzing）等传统自动化方法也是如此。我们基于 AI 的项目如 [Big Sleep](https://googleprojectzero.blogspot.com/2024/10/from-naptime-to-big-sleep.html?utm_source=&utm_medium=&utm_campaign=&utm_content=) 和 [OSS-Fuzz](https://security.googleblog.com/2023/08/ai-powered-fuzzing-breaking-bug-hunting.html?utm_source=&utm_medium=&utm_campaign=&utm_content=) 已经证明了 AI 在经过充分测试的软件中发现新的零日漏洞的能力。随着我们在 AI 驱动的漏洞发现方面取得更多突破，仅靠人力将越来越难以跟上节奏。

CodeMender 帮助解决这个问题的方式，是对代码安全采取一套全面的策略：既是反应式的——立即修补新漏洞；也是主动式的——重写并加固现有代码，在此过程中消灭整类漏洞。在构建 CodeMender 的过去六个月里，我们已经向开源项目上游提交了 72 个安全修复，其中一些涉及多达 450 万行代码的项目。

通过自动创建并应用高质量的安全补丁，CodeMender 的 AI 驱动智能体帮助开发者和维护者专注于他们最擅长的事情——构建优秀的软件。

## CodeMender 的实际运作

CodeMender 利用近期 [Gemini Deep Think](https://blog.google/products/gemini/gemini-2-5-deep-think/?utm_source=&utm_medium=&utm_campaign=&utm_content=) 模型的思考能力，产生一个能够调试并修复复杂漏洞的自主智能体。

为此，CodeMender 智能体配备了强大的工具，使它能够在做出更改之前对代码进行推理，并自动验证这些更改，确保它们正确无误、不会造成回归。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

动画展示 CodeMender 修复漏洞的过程。

虽然大语言模型正在快速进步，但代码安全上的错误可能代价高昂。CodeMender 的自动验证流程确保代码更改在多个维度上正确无误：只有高质量的补丁才会提交给人工审查——例如修复了问题的根本原因、功能正确、不造成回归并遵循风格指南。

作为研究的一部分，我们还开发了新的技术和工具，让 CodeMender 能够更有效地对代码进行推理并验证更改。这包括：

- **高级程序分析：** 我们开发了基于高级程序分析的工具，包括静态分析、动态分析、差分测试、模糊测试和 SMT 求解器。通过使用这些工具系统地审查代码模式、控制流和数据流，CodeMender 能够更好地识别安全缺陷和架构弱点的根本原因。
- **多智能体系统：** 我们开发了专用智能体，使 CodeMender 能够处理底层问题的特定方面。例如，CodeMender 使用一个基于大语言模型的批判工具，高亮显示原始代码与修改后代码之间的差异，以验证所提出的更改不会引入回归，并按需自我纠正。

## 修复漏洞

为了有效修补漏洞并防止其再次出现，CodeMender 使用调试器、源代码浏览器和其他工具来定位根本原因并设计补丁。我们在下方的视频轮播中添加了两个 CodeMender 修补漏洞的示例。

**示例 1：识别漏洞的根本原因**

以下是该智能体在分析调试器输出和代码搜索工具的结果之后，对一个 CodeMender 生成的补丁根本原因进行推理的片段。

虽然本例中的最终补丁只改动了几行代码，但漏洞的根本原因并非一目了然。在这个案例中，崩溃报告显示的是堆缓冲区溢出，但实际问题出在别处——解析可扩展标记语言（XML）元素时错误的栈管理。

**示例 2：智能体能够创建非平凡的补丁**

在这个示例中，CodeMender 智能体能够拿出一个处理复杂对象生命周期问题的非平凡补丁。

该智能体不仅找出了漏洞的根本原因，还修改了项目内部一套完全自定义的 C 代码生成系统。

第 1 页，共 2 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## 主动重写现有代码以提升安全性

我们还把 CodeMender 设计为能够主动重写现有代码，以使用更安全的数据结构和 API。

例如，我们部署 CodeMender 为一个名为 [libwebp](https://github.com/webmproject/libwebp) 的广泛使用的图像压缩库的部分代码应用了 [-fbounds-safety](https://clang.llvm.org/docs/BoundsSafety.html) 注解。应用 **-fbounds-safety** 注解后，编译器会为代码添加边界检查，防止攻击者利用缓冲区溢出或下溢执行任意代码。

几年前，libwebp 中的一个堆缓冲区溢出漏洞（[CVE-2023-4863](https://www.cve.org/CVERecord?id=CVE-2023-4863)）曾被威胁行为者用于[一次零点击 iOS 攻击](https://citizenlab.ca/2023/09/blastpass-nso-group-iphone-zero-click-zero-day-exploit-captured-in-the-wild/)。有了 **-fbounds-safety** 注解，这个漏洞——以及我们已应用注解的项目中大多数其他缓冲区溢出——将永远无法被利用。

在下面的视频轮播中，我们展示了该智能体决策过程的示例，包括验证步骤。

**示例 1：智能体的推理步骤**

在这个示例中，CodeMender 智能体被要求处理 **bit\_depths** 指针上的以下 **-fbounds-safety** 错误：

![截图显示某行代码上的编译器错误信息，展示了 CodeMender 智能体旨在修复的一个安全漏洞](https://lh3.googleusercontent.com/Xyb8mdGPNRm_nicRcCB37es04rfSoZc0i93Hf2oTPCGCH-2CcoaS54_fftTADcam2ykx9bOn48IR1fbbiTC_mX5KOy_uzDEf0gJ4UY6t8tD0bmkaO84=w1440)

**示例 2：智能体自动纠正错误与测试失败**

CodeMender 的另一个关键特性，是它能够自动纠正由自身注解引发的新错误和任何测试失败。下面是智能体从一次编译错误中恢复的示例。

**示例 3：智能体验证更改**

在这个示例中，CodeMender 智能体修改了一个函数，然后使用配置为功能性等价判定的 LLM judge 工具来验证功能保持完好。当工具检测到失败时，智能体会根据 LLM judge 的反馈进行自我纠正。

第 1 页，共 3 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## 让每个人的软件都更安全

虽然 CodeMender 的早期结果令人鼓舞，但我们采取审慎的方式，专注于可靠性。目前，CodeMender 生成的所有补丁在提交上游之前都会经过人类研究人员的审查。

使用 CodeMender，我们已经开始向多个关键开源库提交补丁，其中许多已被接受并合入上游。我们正在逐步扩大这一流程，以确保质量并系统地处理来自开源社区的反馈。

我们还将逐步联系关键开源项目中感兴趣的维护者，提供 CodeMender 生成的补丁。通过根据这一流程的反馈不断迭代，我们希望把 CodeMender 打造成一个所有软件开发者都能使用的工具，让他们的代码库保持安全。

我们将有大量技术和成果可以分享，并计划在未来几个月内以技术论文和报告的形式发表。有了 CodeMender，我们对 AI 增强软件安全、造福每个人的惊人潜力的探索才刚刚开始。

**致谢**

致谢名单（按字母顺序排列）：

Alex Rebert, Arman Hasanzadeh, Carlo Lemos, Charles Sutton, Dongge Liu, Gogul Balakrishnan, Hiep Chu, James Zern, Koushik Sen, Lihao Liang, Max Shavrick, Oliver Chang 和 Petros Maniatis。

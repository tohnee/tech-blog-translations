---
title: "SIMA 2：一个能在虚拟 3D 世界中与你一起游玩、推理和学习的智能体"
title_en: "SIMA 2: An Agent that Plays, Reasons, and Learns With You in Virtual 3D Worlds"
source: https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/
site: deepmind
date: 2025-11-13
crawled: 2026-09-13
translated: 2026-09-13
---

# SIMA 2：一个能在虚拟 3D 世界中与你一起游玩、推理和学习的智能体

> 原文：[SIMA 2: An Agent that Plays, Reasons, and Learns With You in Virtual 3D Worlds](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/) · Google DeepMind

去年，我们[推出了](https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/)SIMA（Scalable Instructable Multiworld Agent），一个能在广泛的虚拟环境中遵循基本指令的通用 AI。SIMA 是教 AI 在丰富的 3D 世界中把语言转化为有意义行动的关键第一步。

今天我们推出 SIMA 2，这是我们创造通用且有用的 AI 智能体研究中的下一个里程碑。通过集成我们 [Gemini 模型](https://deepmind.google/models/gemini/)的先进能力，SIMA 正在从一个指令执行者进化为一个交互式游戏伙伴。SIMA 2 不仅能在虚拟世界中遵循人类语言的指令，它现在还能思考自己的目标、与用户对话，并随着时间推移不断自我提升。

这是朝向通用人工智能（AGI）方向的重要一步，对机器人技术以及更广义的 AI 具身化的未来都具有重要意义。

- [推理](#reasoning)
- [泛化](#generalization)
- [自我提升](#self-improvement)
- [下一步](#next-steps)
- [责任](#responsibility)

## 推理的力量

SIMA 的第一版在一系列商业电子游戏中学会了执行 600 多种遵循语言的技能，比如"向左转"、"爬上梯子"和"打开地图"。它以人的方式在这些环境中行动：通过"观看"屏幕，使用虚拟键盘和鼠标进行导航，无法接触底层的游戏机制。

到了 SIMA 2，我们已经超越了指令执行。通过把一个 Gemini 模型嵌入为智能体的核心，SIMA 2 不仅能响应指令，还能对指令进行思考与推理。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

MineDojo：SIMA 1（左）尝试遵循指令，而 SIMA 2（右）在一款它从未见过的游戏中成功完成了任务。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

ASKA：SIMA 1（左）尝试遵循"找到一处篝火"的指令，而 SIMA 2（右）在一款它从未见过的游戏中成功完成了任务。

SIMA 2 的新架构集成了 Gemini 强大的推理能力，帮助它理解用户的高层目标、为达成目标进行复杂推理，并在游戏中熟练地执行面向目标的动作。

我们使用带有语言标签的人类示范视频以及由 Gemini 生成的标签的混合数据训练了 SIMA 2。因此，SIMA 2 现在可以向用户描述它打算做什么，并详细说明它为实现目标所采取的步骤。

第 1 页，共 3 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

超越简单的指令遵循：SIMA 2 不仅能回答用户的问题，还能对自己的行为和环境进行推理。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

超越简单的指令遵循：SIMA 2 不仅能回答用户的问题，还能对自己的行为和环境进行推理。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

超越简单的指令遵循：SIMA 2 不仅能回答用户的问题，还能对自己的行为和环境进行推理。

在测试中，我们发现与该智能体互动的感觉，不像是在下达命令，更像是在与一位能对眼前任务进行推理的伙伴协作。

得益于我们与现有及新游戏伙伴的合作（见致谢），我们得以在更广泛的游戏上训练和评估 SIMA 2。

这就是 Gemini 带给具身 AI 的力量：一个世界级的推理引擎，如今可以在复杂、交互式的 3D 环境中感知、理解并采取行动。

第 1 页，共 4 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 通过对其环境和用户意图进行推理，来解读抽象概念和逻辑指令。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 通过对其环境和用户意图进行推理，来解读抽象概念和逻辑指令。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 通过对其环境和用户意图进行推理，来解读抽象概念和逻辑指令。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 通过对其环境和用户意图进行推理，来解读抽象概念和逻辑指令。

## 泛化性能的飞跃

Gemini 的加入也带来了泛化能力和可靠性的提升。与上一代相比，SIMA 2 现在能理解更复杂、更细微的指令，并且执行这些指令的成功率大幅提高，尤其是在它从未训练过的场景或游戏中，例如全新的维京生存游戏 ASKA，或 MineDojo——热门开放世界沙盒游戏 Minecraft 的一个研究实现版本。

### SIMA 2 能理解并完成漫长而复杂的任务

第 1 页，共 4 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 成功地执行了漫长而复杂的指令。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 在毫无事先训练的情况下挑战一款全新的游戏，展现出令人瞩目的进步。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 成功地执行了漫长而复杂的指令。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 成功地执行了漫长而复杂的指令。

### SIMA 2 能理解多模态提示词

第 1 页，共 3 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

用户正在屏幕上绘制草图。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

用户正在屏幕上绘制草图。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

用户正在屏幕上绘制草图。

### SIMA 2 能理解不同语言，甚至表情符号

第 1 页，共 2 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

看它如何正确解读表情符号来执行任务。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

看它如何遵循不同语言的指令来执行任务。

此外，它迁移已学概念的能力——例如把对一款游戏中"采矿"的理解应用到另一款游戏的"收割"上——是实现人类认知中那种广泛泛化能力的基础。事实上，得益于这种能力，SIMA 2 在广泛任务上的表现已显著接近人类玩家。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 可以把动作泛化到多款游戏中，包括它没有训练过的游戏（如 MineDojo 和 ASKA）。

![SIMA 1、SIMA 2 和人类在所有训练游戏环境的一组评估任务上的任务完成成功率，显示 SIMA 2 显著缩小了与人类表现的差距。请注意，此处报告的 SIMA 1 成绩是针对我们新的、扩展后且难度大幅提高的评估集，涵盖更广泛的环境和更复杂的指令](https://lh3.googleusercontent.com/KwuGClFlsydWIS2azo2WjBWkMY-Hm3geOZAad00wP-CMtmWQa8DlpmqOMvXC6QKiPnEUBgtToVWnJ9rzz0O7dTcaVFhYOSggEugNVJBWVgc1hegDfg=w1440)

SIMA 1、SIMA 2 和人类在所有训练游戏环境的一组评估任务上的任务完成成功率，显示 SIMA 2 显著缩小了与人类表现的差距。请注意，此处报告的 SIMA 1 成绩是针对我们新的、扩展后且难度大幅提高的评估集，涵盖更广泛的环境和更复杂的指令

![SIMA 1 和 SIMA 2 在保留（训练期间从未见过）游戏 ASKA 和 MineDojo（Minecraft 的一个研究实现版本）上的任务完成成功率。](https://lh3.googleusercontent.com/yad81RKXlxroZBsqlNdzrzWNTIWRMJqgryRDK8Vo2b_p0FtBNjJR3k3nSmq--cR3ebZj4RvpoSVHoPgQ7aZMW8U7VCEtJCOopKQnek06OTPtLs4rVF0=w1440)

SIMA 1 和 SIMA 2 在保留（训练期间从未见过）游戏 ASKA 和 MineDojo（Minecraft 的一个研究实现版本）上的任务完成成功率。

### 终极考验：在全新想象的世界中游玩

为了测试 SIMA 2 泛化能力的极限，我们把它与另一个突破性研究项目 [**Genie 3**](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/) 结合起来，后者能从单张图像或文本提示生成全新的、实时的 3D 模拟世界。

当我们挑战 SIMA 2 在这些新生成的世界中游玩时，我们发现尽管从未见过这样的环境，它仍能合理地定位自己、理解用户指令，并朝着目标采取有意义的行动。它展现出了前所未有的适应能力。

第 1 页，共 4 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 在 Genie 3 新生成的世界中游玩。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 在 Genie 3 新生成的世界中游玩。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 在 Genie 3 新生成的世界中游玩。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SIMA 2 在 Genie 3 新生成的世界中游玩。

## 迈向可扩展、多任务的自我提升

SIMA 2 最令人兴奋的新能力之一是它自我提升的能力。我们观察到，在整个训练过程中，SIMA 2 智能体在试错和基于 Gemini 的反馈的引导下，能够执行越来越复杂的新任务。

例如，在最初从人类示范中学习之后，SIMA 2 可以转而完全通过自主游玩在新游戏中学习，在未见过的世界中发展技能，而无需额外的人类生成数据。在后续训练中，SIMA 2 自身的经验数据随后可以被用来训练下一代、能力更强的智能体。我们甚至能够在新生成的 Genie 环境中利用 SIMA 2 的自我提升能力——这是朝着在多样的生成世界中训练通用智能体迈出的重要里程碑。

![SIMA 2 的自我提升循环始于 Gemini 提供一个初始任务以及对 SIMA 2 行为的预估奖励。这些信息随后被加入一个自生成经验库，智能体将其用于后续世代的进一步训练。这一过程使智能体能够完全独立于人类生成的示范和干预，改进此前失败的任务。](https://lh3.googleusercontent.com/UsqTitVvxI5r3_oOUWFvWbJl9Wy-1Z8zhZOOZvt553hZ4Kx1ZvQfJs-OXL9ingzdu3LkG2B-1NMfcUTD0j9CfF3CHJsleG0O_9P3fJctY40IkeyV=w1440-h810-n-nu)

SIMA 2 的自我提升循环始于 Gemini 提供一个初始任务以及对 SIMA 2 行为的预估奖励。这些信息随后被加入一个自生成经验库，智能体将其用于后续世代的进一步训练。这一过程使智能体能够完全独立于人类生成的示范和干预，改进此前失败的任务。

这一迭代的良性提升循环，为一个智能体可以在极少人类干预下学习和成长的未来铺平了道路，让智能体成为具身 AI 中的开放式学习者。

第 1 页，共 2 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

ASKA：左侧是初始 SIMA 2 智能体失败的任务示例，右侧可以看到 SIMA 2 经过数代训练后实现了自我提升，且完全没有借助任何人类反馈或游戏对局数据。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Genie 3 环境：该智能体在一个它从未见过的 Genie 3 环境中经过一代训练便有所提升。

## 展望未来：通往通用具身智能的旅程

SIMA 2 在多样游戏环境中运作的能力，是通用智能的重要试验场，让智能体能够掌握技能、练习复杂推理，并通过自主游玩持续学习。

虽然 SIMA 2 是朝向通用、交互式具身智能的重要一步，但它本质上是一项研究探索，其当前的局限也指出了未来工作的关键方向。我们发现，智能体在面对需要大量多步推理和目标验证的超长视野复杂任务时仍会遇到困难。SIMA 2 对其交互的记忆也相对较短——它必须使用有限的上下文窗口来实现低延迟交互。最后，通过键盘和鼠标接口执行精确的底层动作，以及对复杂 3D 场景实现稳健的视觉理解，仍是整个领域持续攻关的开放性挑战。

这项研究为面向行动的 AI 的新路径提供了根本性验证。SIMA 2 证实：一个以广泛能力为目标、利用多样的多世界数据和 Gemini 强大推理能力训练的 AI，可以成功地把许多专用系统的能力统一为一个连贯的通用智能体。

SIMA 2 也为在机器人技术中的应用提供了一条强有力的路径。它学到的技能——从导航、工具使用到协作任务执行——正是未来物理世界中的 AI 助手所需的智能物理具身化的一些基本构件。

## 负责任的开发

SIMA 2 是一个以人为中心的交互式智能体，与它互动充满乐趣，尤其是它解释自身推理时那种妙趣横生的方式。与我们所有的先进和基础技术一样，我们从一开始就坚定地致力于负责任地开发 SIMA 2。对于它的技术创新——尤其是自我提升的能力——这一点尤为突出。

在构建 SIMA 2 的过程中，我们与我们的负责任开发与创新团队合作。随着我们继续探索潜在应用，我们将以有限研究预览的形式发布 SIMA 2，并向一小批学者和游戏开发者提供早期访问。这一方式使我们能够在探索这一新领域、继续加深对风险及相应缓解措施的理解时，收集关键的反馈和跨学科视角。我们期待与社区进一步合作，以负责任的方式开发这项技术。

进一步了解 SIMA

[SIMA 技术报告](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/SIMA_Tech_Report_2025.pdf)

## 致谢

本研究由 SIMA 2 团队开发：Maria Abi Raad, John Agapiou, Frederic Besse, Andrew Bolt, Sarah Chakera, Harris Chan, Jeff Clune, Alexandra Cordell, Martin Engelcke, Ryan Faulkner, Maxime Gazeau, Arne Olav Hallingstad, Tim Harley, Ed Hirst, Drew Hudson, Laura Kampis, Sheleem Kashem, Thomas Keck, Matija Kecman, Oscar Knagg, Alexander Lerchner, Bonnie Li, Yulan Liu, Cong Lu, Maria Loks-Thompson, Joseph Marino, Kay McKinney, Piermaria Mendolicchio, Anna Mitenkova, Alexandre Moufarek, Fabio Pardo, Ollie Purkiss, David Reichert, John Reid, Tyson Roberts, Daniel P. Sawyer, Tim Scholtes, Daniel Slater, Hubert Soyer, Kaustubh Sridhar, Peter Stys, Tayfun Terzi, Davide Vercelli, Bojan Vujatovic, Jane X. Wang, Luyu Wang, Duncan Williams 和 Lei M. Zhang。

感谢以下人士的领导、指导与支持：Satinder Singh Baveja, Adrian Bolton, Zoubin Ghahramani, Raia Hadsell, Demis Hassabis（德米斯·哈萨比斯）, Shane Legg, Volodymyr Mnih 和 Daan Wierstra。

特别感谢部分贡献者和往期成员：Alex Cullum, Karol Gregor, Rosemary Ke, Junkyung Kim, Matthew Jackson, Andrew Lampinen, Loic Matthey, Hannah Openshaw 和 Zhengdong Wang。

特别感谢与我们合作的所有游戏开发者：Coffee Stain（*Valheim、Satisfactory、Goat Simulator 3*）、Foulball Hangover（*Hydroneer*）、Hello Games（*No Man's Sky*）、Keen Software House（*Space Engineers*）、RubberbandGames（*Wobbly Life*）、Strange Loop Games（*Eco*）、Thunderful Games（*ASKA、The Gunk、Steamworld Build*）、Digixart（*Road 96*）以及 Tuxedo Labs 与 Saber Interactive（*Teardown*）。

我们感谢 Vika Koriakin, Duncan Smith, Nilesh Ray, Matt Miller, Leen Verburgh, Ashyana Kachra, Phil Esposito, Dimple Vijaykumar, Piers Wingfield, Lucie Kerley 在开发和打磨本项目关键组件方面无价的合作。

我们还感谢 Jack Parker-Holder、Shlomi Fruchter 以及 Genie 团队的其他成员提供 Genie 3 模型的访问权限。

我们要感谢 Google 和 Google DeepMind 中为这项工作做出贡献的众多团队，包括法务、市场、传播、责任与安全委员会、负责任开发与创新、政策、战略与运营，以及我们的业务和企业发展团队。我们还要感谢此处未一一提及的所有 GDM 团队一直以来的支持。

最后，我们将这项工作献给我们的同事 Felix Hill 和 Fabio Pardo，纪念他们，他们对本领域的贡献将继续激励我们。

---
title: "打造 Claude Design 的产品设计师，如何用它先探索想法再动手实现"
title_en: "How the product designer who built Claude Design uses it to explore ideas before building them"
date: 2026-07-24
source: https://claude.com/resources/articles/how-the-product-designer-who-built-claude-design-uses-it-to-explore-ideas-before-building-them
crawled: 2026-11-17
translated: 2026-11-17
---

# 打造 Claude Design 的产品设计师，如何用它先探索想法再动手实现

> 原文：[How the product designer who built Claude Design uses it to explore ideas before building them](https://claude.com/resources/articles/how-the-product-designer-who-built-claude-design-uses-it-to-explore-ideas-before-building-them) · Claude 博客

*Anthropic 产品设计师 Nate Parrott 分享他如何使用 Claude Design（beta），在早期探索、迭代并分享视觉想法——从产品原型到幻灯片和动画。*

2025 年秋天，我是 [Claude Code for VS Code](https://code.claude.com/docs/en/vs-code) 唯一的产品设计师，与两位工程师合作，为终端之外的世界重新构想 Claude Code 的一切，打造一个友好的界面。我们在 9 月底[发布了 beta 版](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)，[Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5) 在 11 月到来，Claude Code 团队开始以极快的节奏、激进的力度交付功能。工程师们的产出远超以往，而我的交付速度还是老样子。我需要找到一种办法跟上。

Claude Code 运行在终端里，一切都是基于文本的，而我最初的尝试也沿用了这种方式：我把输出复制进 Claude，加上截图，然后问：「这是我们想加的一个功能，你为什么不设计一下？」结果并不好。大约一个月的时间里，我把它当作副业项目，不断寻找改进 Claude 设计产出的办法。

## **给 Claude 一个 HTML 游乐场**

最终我偶然找到了答案：Claude 非常擅长 HTML。我们通常把 HTML 视为网站的格式，但它同时是一种丰富、可交互的视觉媒介：你能在幻灯片、视频文件或 PDF 里做出来的东西，都能在网页里做出来。于是我让 Claude 生成 HTML，并给它做了一个分屏界面——左侧聊天，右侧查看输出。

这已经很有用，但产品设计的关键在于运用你所服务的产品和品牌知识，因此作为下一步，我花了一段时间把 Anthropic 品牌的核心要素（我们产品使用的字体、颜色、资产和原则）提炼成提示词。这样，当我把提示词输入这个工具时，输出就符合 Anthropic 品牌规范。

我把这一切放进一个小型内部原型，并分享给团队。产品设计师们立刻把它用于交互式原型。在传统设计工具里做一个可点击原型，意味着要为每个屏幕的每个状态做模拟稿，再手工把它们连线起来。而在这里，你把资产交给 Claude，说一句：让它跑起来。它交付的每一件产物都带有一个链接，你可以像分享文档一样分享它。

## **Claude Design 如何成为一种视觉工作媒介**

我第一次意识到 Claude Design 有多吸引人，是在 [Anthropic Labs](https://www.anthropic.com/news/introducing-anthropic-labs) 团队异地会议的一次创意提案环节上：在场的每个人都用它拼出了自己的幻灯片，而且往往是在会议进行中、轮到自己上台之前临时做的。那次环节说服了 Labs 团队为它配备人手，Claude Design 也从副业项目变成了正式项目。

我们不再把它描述为做产品模拟稿的工具。Claude Design 成了一种生产任何类型视觉沟通物的工具：幻灯片、落地页、可打印成 PDF 的单页文档、邮件、动画、用于社交媒体分享的视觉素材。幻灯片成了人们用 Claude Design 做得最多的东西之一，因此它现在有了自己的起点——Claude Slides：你可以在与 Claude 的任何对话中调用它，也可以从 Artifacts 标签页开始。我把它理解为产品设计之上再高一层的工具：你与 Claude 协作产出的视觉物，主要任务是沟通和创意发想。

随着模型在视觉能力上不断提升，Claude Design 能完成的工作范围和品质也随之提升。我们最新的 Opus 级模型 [Claude Opus 5](https://www.anthropic.com/news/claude-opus-5) 在阅读图表、示意图和截图方面优于以往的 Opus 模型，与 Claude Design 搭配时，能做出堪称演示级的幻灯片和备忘录。

## **Claude Design 不适合做什么**

Claude Design 没有图像模型，也不是为图像生成而构建的，因此它并不适合做 logo 设计——尽管这并没有阻止人们去尝试。更好的做法是把你已有的 logo 和资产带进来。产品的其余部分也是同样的逻辑：Claude 会给出选项和起点，让你不必盯着空白画布发呆；你来判断哪个单独看不错，或者哪几个组合起来更好。

如果你要交付生产软件，请继续使用 Claude Code。Claude Code 用于写代码；Claude Design 用于设计工作中其他部分：早期创意发想、协作，或者在任何人承诺动手实现某个方向之前先争取支持。Claude Design 现在可以在 Claude Code 内使用，因此你可以在已经打开的会话中请求一份设计——无论是在桌面端还是终端，也可以用 `/design` 创建、编辑和同步设计项目。当一份设计准备好变成软件时，把它交给 Claude Code，它会从你已有的工作继续，而不是从一张截图重新开始。随着模型在构建生产软件方面越来越强，真正重要的工作会前移到流程更早的阶段：想出好点子、让所有人对齐、在想法还很早期的时候收集反馈。

## **我如何在日常工作中使用 Claude Design**

我每天都用 Claude Design 做那些可以称为「看家本领」的设计工作：为早期想法画线框图，或者生成某个流程的 15 个版本，用来向同事收集反馈。以下是我自己工作中的一些近期例子：

* **Claude Design 的介绍动画。** 你注册 Claude Design 时播放的动画，就是用这个工具本身做出来的，但不是直接做的：我不是动画师，所以我先让 Claude Design 给我做了一个定制的视频编辑器，再用那个编辑器做出动画。

* **一个地铁时刻表应用**，带有可调节的动画控制项，用来调校运动的物理手感。

* **Instagram 风格的色彩控制。** 我让 Claude 允许我用滑块和预设来调整一个应用的配色方案，而不是用文字描述颜色。

* **Claude Design 自身的一次重新设计。** 我和两位队友 Helen 和 Andrew 一直在工具内部反复推敲编辑器的新设计方案。我们不会原样发布它，但这是我们探索产品未来可能形态的方式。

## **使用 Claude Design 的最佳实践**

1. **在写提示词之前先把想清楚。** 要得到符合你构想的结果，最好、最高效的方式是提前告诉 Claude 你需要什么。我在设计之前会花大量时间写提示词。有时我在 Claude Design 里用语音按钮口述；有时我躺在沙发上，在手机的 Notes 里打字；或者散步时录一段语音备忘，之后再粘贴转录文本。无论你偏好哪种沟通方式，都要在离开电脑的时候想清楚自己想要什么，这样当你坐下来时，Claude 就能执行你确切的构想。
2. **告诉 Claude 它应该长什么样。** 如果不加引导，Claude 会选择它最喜欢的某一种审美。[你多半认得出来。](https://www.newyorker.com/the-ai-design-aesthetic-thats-taking-over-the-internet) 提前规避这种情况：指定字体和颜色，或者提供一组图片情绪板（moodboard）作为灵感，再或者让 Claude 头脑风暴字体与颜色的搭配，来回几轮直到某一组感觉对了。
3. **把重复性的工作变成设计系统。** 把你的品牌文件和资产（logo、幻灯片、截图、字体规格，以及任何你会重复使用的东西）以原始上传文件、设计文件或 GitHub 仓库的形式带进来，Claude 会分析它们并[生成一套设计系统](https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design)。你可以同时保留多套。此后，Claude 会用你的组件来构建，并在把结果给你之前对照这套系统检查、修正，因此每件产物都从你的选择出发，而不是从空白画布开始。对于更大的团队，管理员可以批准一套标准系统并锁定编辑。
4. **先要十个方案，再做混搭。** 它们大多不会好，这没关系；有一两个会好。然后说：「我喜欢方案 B，再加一点方案 D。给我五个把两者揉在一起的变体。」
5. **画出来那些你描述不出的东西。** 如果你脑子里有一个布局却找不到词来形容它，就在纸上画出来，拍照上传。
6. **指出来，然后说话。** 不必写一整段话来说明你指的是哪个元素，直接点它然后开口。你需要先在设备上启用听写功能，然后选择「评论」，点进评论框。你说的话会像打字一样出现在评论框里。
7. **保真度不重要时，先画线框图。** 要线框图会快得多，也能让 Claude 专注于设计的高层结构，而不是视觉呈现。这是快速尝试许多不同想法的好办法。
8. **最后一公里手工完成。** 用直接的编辑工具（重排、删除、编辑文字、调整尺寸、改颜色）做最后润色，而不是用提示词。直接编辑不消耗 token，而尺寸、对齐这类小决定，本来用眼睛看也更好。
9. **给 Claude 你真实的上下文。** 如果你是在为已有的应用或网站设计功能，就连接 GitHub，或者在 Claude Code 中基于本地代码库工作：Claude 会抓取你的组件和现有屏幕，把它们作为起点，试上几次，它就能以相当高的保真度复现你现有的设计。如果你是在对话中途请求设计，Claude 会基于对话中已有的文件和分析构建，并参考你的记忆、项目和技能。连接器和网络搜索同样可用——只要设计依赖于外部信息。
10. **与 Claude 并肩工作。** 你不必等 Claude 交付完整结果之后，再提新的修改或任务。你可以一次排入多条消息，也可以在 Claude 还在处理上一轮时继续说话。

## **让它「活」起来**

有一场 Bret Victor 的演讲，每个设计师都应该找时间看一次，题目是 [Stop Drawing Dead Fish](https://vimeo.com/64895205)。简介里有一句话：「我们所画的一切，默认就应该是活的。」

我想鼓励设计师们——无论是在 Claude Design 还是任何其他工具里——去思考如何让自己的创作活起来。我最喜欢的 Claude Design 作品，都是那些放不进现有框框里的东西：带交互式模拟的文档、会和你对话的幻灯片、同时也是视频的示意图、同时也是自己编辑器的设计。代码，尤其是 HTML，是极具创造力的媒介，而它终于对设计师来说变得相对容易上手了。

Claude Design 之所以成为今天的样子，是因为 Anthropic 的人们不断发现我未曾预想到的用法。它现在可以在与 Claude 的任何对话中使用，包括 Claude Code 和 Artifacts 标签页，在付费方案上以 beta 形式提供。如果你已经在 claude.ai/design 使用它，你的体验不会有任何变化。它现在以 beta 形式在 Claude Pro、Max、Ultra、Team 和 Enterprise 方案中提供。[试用一下](https://claude.com/product/design)，把它带向我们还没想到的地方。

*本文由 Anthropic 产品设计师 Nate Parrott 撰写，表达他对 Claude Design 的观点、使用方式和建议。*

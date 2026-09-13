---
title: "一位 Google 员工讲解如何用「元提示」创作出令人惊叹的 Veo 视频"
title_en: "A Googler explains how to “meta prompt” for incredible Veo videos"
source: https://blog.google/products-and-platforms/products/gemini/meta-prompting-veo-gemini-tips/
site: gemini
date: 2025-12-08
crawled: 2026-09-13
translated: 2026-09-13
---

# 一位 Google 员工讲解如何用「元提示」创作出令人惊叹的 Veo 视频

> 原文：[A Googler explains how to “meta prompt” for incredible Veo videos](https://blog.google/products-and-platforms/products/gemini/meta-prompting-veo-gemini-tips/) · Google

Google 内部有一个聊天群组，员工们会在里面分享各种新奇的 AI 演示。某天你可能看到一件根据你展示的书来推荐音乐的工具；另一天则是一个能生成[你年长版与年幼版自己共处一图](https://blog.google/products/gemini/gemini-nano-banana-examples/)的应用。

而在很多日子里，你会发现群里出现的是 Google DeepMind 用户体验工程师 Anna Bortsova 的作品。

Anna 拥有工程学与视觉艺术的双重背景，热衷于试用我们的 AI 工具。她分享过一种 AI 生成的字母表——每个字母都由繁复的刺绣构成——还有对热门电子游戏的超现实主义演绎。

![一张 AI 生成的图片：一个过山车环绕着一棵树，树的枝头上悬挂着旋转木马的小马。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_Generated_Image_amppnnampp.width-100.format-webp.webp)

让人忍不住 ♥️ 的超现实主义意象。

![一张 AI 生成的图片：一款积木拼图游戏的 3D 渲染，方块由教堂和其他建筑的部件构成。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_Generated_Image_axczr1axcz.width-100.format-webp.webp)

让人忍不住 ♥️ 的超现实主义意象。

![一张 AI 生成的图片：一艘宇宙飞船悬停在一群身着旧时代服饰的人上方。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_Generated_Image_ghcngjghcn.width-100.format-webp.webp)

让人忍不住 ♥️ 的超现实主义意象。

她的背景派上了用场。「我知道萨尔瓦多·达利（Salvador Dali）受到佛兰德斯艺术的启发，所以我让 Gemini 以佛兰德斯画家的风格来生成这些游戏的超现实主义图像，」Anna 说。这些图像在群组里火了一把，收获了满屏的爱心表情和大量好评。

最近，Anna 用 Veo 制作了一系列 ASMR 风格的短视频，以定格动画和纸质工程场景为特色。她制作过烤串的视频——被串起的皱纸「肉块」在一堆皱纸「炭火」上方转动——还有一只粉色火烈鸟扑动纸翅膀的视频，伴随舒缓的簌簌与呼呼声。

「Veo 3 提供高质量的视频和非常出色的音效，」Anna 说，「这些视频里纸张的窸窣声让人格外满足。」

其他人似乎也深有同感。Anna 的作品不仅在群里收获了满满的表情爱心，Google 各地的营销团队也主动联系她，希望在我们的[社交媒体渠道](https://x.com/GoogleAI/status/1940822370132152442)上展示她的作品。她也会在自己的社交媒体上发布作品，Google 之外的人纷纷向她请教提示词方面的建议。

「关键是，」Anna 说，「实际撰写提示词的是 Gemini。」

Anna 采用的是一种被称为「元提示」（meta prompting）的方法。她并不为某个具体场景直接写提示词，而是让 Gemini 为多个不同的场景起草详细提示词——有时一次 5 到 10 条——以便在 [Flow](https://labs.google/flow/about) 或 [Gemini 应用](https://gemini.google.com/)中使用。生成的提示词可以非常长且具体——有时长达数页——并带来令人惊叹的输出。而她用来指导 Gemini「如何写提示词」的那些提示词，才是关键所在。

Anna 的元提示激发 Gemini 生成了细节丰富的提示词，用于指示生成式 AI 模型。

![左侧是黄色的 Anna 元提示，包含诸如「风格应为定格动画视频」「试着构思最具创意、最令人印象深刻、最令人愉悦的提示词」等指令。右侧是 Gemini 生成的白色提示词示例，其中包含诸如「蕨类植物应采用较浅的绿色优质纸张制成，并带有可见的纤维质感」等细节。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Screenshot_2025-10-02_3.40.56_PM.width-1200.format-webp.webp)

「这里没有固定规则——我们是在实验——但我发现有几个技巧能引导 Gemini 写出真正丰富的提示词，」她说，「你要定义一个非常具体的任务：『写一条 LLM 能看懂的详细提示词』。你还要明确格式与风格，比如：一段 8 秒的定格动画，呈现纸质工程场景。然后给它约束条件，比如用铝箔纸或亮面纸，而不是笼统的『纸』。接下来就放手让它发挥。」

她说，根据模型对 Gemini 提示词的响应情况，你可能还需要加以微调。增补或修改关于音效和质感的细节——这是一个协作过程。你也不妨带上情绪。「我发现表达出你想要唤起的感受会很有帮助，」她补充道，「比如告诉 Gemini，你希望它思考『那些看起来令人身心愉悦的场景』。」

在这样的指令加上创作植物艺术作品的任务下，Gemini 交出了一条关于徐徐展开的纸蕨的提示词，其中写道：「动画应当缓慢而令人着迷，每片叶羽都应在轻柔、富有韵律的序列中精致地舒展开来。」Veo 完美地领会了这个要求。

Anna 的蕨类和羽毛并非她本职工作的一部分：她的日常工作是为 Google DeepMind 的研究人员构建基础设施和工具，以扩展他们的 AI 实验。但这件事让她在挤出 10 分钟空闲时收获快乐，她也乐于分享这份心得。（她甚至做了一套幻灯片来传递自己的经验。）

对于 Google 同事——以及所有看到这篇文章的人——她最重要的建议是什么？「选一个你热爱的主题，然后开始实验，」她说，「我就是这么做的，我到现在还在学习——并且乐在其中。」

---
title: "为 AI 时代重新构想鼠标指针"
title_en: "Reimagining the mouse pointer for the AI era"
source: https://deepmind.google/blog/ai-pointer/
site: deepmind
date: 2026-05-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 为 AI 时代重新构想鼠标指针

> 原文：[Reimagining the mouse pointer for the AI era](https://deepmind.google/blog/ai-pointer/) · Google DeepMind

我们正在开发更无缝、更直观的与 AI 协作的方式

几十年来，鼠标指针一直是电脑屏幕上的常伴之物，出现在每一个网站、每一份文档和每一个工作流程中。尽管技术日新月异，指针在半个多世纪里却几乎没有什么演进。

我们一直在探索新的 AI 驱动能力，让指针不仅能理解它所指向的内容，还能理解它对用户为何重要。

我们的目标是解决一个常见的困扰：由于典型的 AI 工具栖身于自己的窗口之中，用户不得不把自己的世界拖进那个窗口。我们想要的是相反的体验：直观的 AI 主动来到用户所用的所有工具之中，而不打断他们的工作流。例如，想象一下指向一张建筑图片，然后说「给我指个路」——当 AI 系统已经理解了上下文时，无需再多说一个字。

今天，我们将阐述指引我们思考未来用户界面的底层原则，并分享一个由 Gemini 驱动的 AI 智能指针的实验性演示。例如，你可以访问 Google AI Studio，只需指向并开口说话，就能[编辑一张图片](https://aistudio.google.com/apps/bundled/ai-pointer-create?showPreview=true&showAssistant=true&fullscreenApplet=true)或[在地图上查找地点](https://aistudio.google.com/apps/bundled/ai-pointer-find?showPreview=true&showAssistant=true&fullscreenApplet=true)。

![](https://lh3.googleusercontent.com/0CBS9A2z90df_b-DENgsypA2v7Wxcg_q7eqFeH8EZwmr9gFebGcVRdBwezunCAYoeKkkqZVaTWosYCnSKUz-RoLBelAG2FXR0gfpTJOxQecyltQ7=w1440-h810-n-nu)

这段视频展示了我们 AI 智能指针的实验环境。为便于观看，所有片段均做了缩短处理。

## 我们的交互原则

我们制定了四条原则，它们共同把传达上下文和意图这项繁重工作从用户转移给了计算机，用更简单、更直观的交互取代冗长的文字提示。以下是我们方法与原则的图示。

### 保持心流

AI 能力应当跨越所有应用工作，而不是强迫用户在应用之间绕「AI 弯路」。我们的 AI 智能指针原型可以在用户工作的任何地方使用。例如，用户可以指向一份 PDF 并要求生成要点摘要，直接粘贴到邮件里；悬停在一张统计表格上要求生成饼图版本；或者高亮一份菜谱，要求把所有食材的用量翻倍。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 指给它看，告诉它要什么

当前的 AI 模型要求精确的指令。为了得到好的回应，用户必须写一段详细的提示词。AI 智能指针可以简化这一过程：它平滑地捕获指针周围的视觉与语义上下文，让计算机「看见」并理解对用户重要的内容。在我们的实验系统中，只需一指，AI 就能准确知道用户需要帮助的是哪个词、哪段文字、图片的哪个部分或哪段代码。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 善用「这个」和「那个」的力量

在日常交流中，人类很少用冗长详尽的段落说话。我们可能会说「把这个改一下」「把那个挪到这儿」「这是什么意思？」——同时依靠肢体动作和我们共享的情境来补齐理解上的空隙。一个能理解上下文、指点与言语相结合的 AI 系统，将让用户以自然的简略表达提出复杂的请求，无需繁琐的提示词。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 把像素变成可操作的实体

几十年来，计算机只能追踪我们指向的*位置*。如今 AI 还能理解用户指向的*内容*。这把像素转化成了结构化的实体——比如地点、日期和物品——用户可以立即与之交互。一张写满涂鸦字条的拍照可以变成一份可交互的待办清单；旅行视频中暂停的一帧可以变成那家看起来很棒的餐厅的预订链接。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

构建能适应人类行为的技术——而不是强迫用户去适应技术——将开启这样一个未来：与 AI 协作让人感觉真正直观、流畅、无缝。

令我们兴奋的是，这些以人为本的理念正在被编织进我们每天都在使用的产品之中。

## 将这项工作应用于我们的产品

我们正在整合这些原则，重新构想 Chrome 以及我们全新的 [Googlebook](https://blog.google/products-and-platforms/platforms/android/meet-googlebook) 笔记本体验中的指点交互。从今天起，你无需再编写复杂的提示词，而是可以直接用指针就网页中你关心的部分向 [Gemini in Chrome](https://gemini.google/overview/gemini-in-chrome/) 提问。例如，你可以选中页面上的几款商品并要求对比，也可以指向客厅里你想要摆放一张新沙发的位置。类似地，我们很快将在 Googlebook 上推出 Magic Pointer，让用户指尖轻点即可驾驭 Gemini，获得更直观的体验。由于还有许多其他潜在的优秀应用场景，我们将在包括 [Google Labs 的 Disco](https://labs.google/disco) 在内的各个平台上继续测试未来概念。

**在 Google AI Studio 中试用 AI 智能指针**

[编辑一张图片](https://aistudio.google.com/apps/bundled/ai-pointer-create?showPreview=true&showAssistant=true&fullscreenApplet=true)[在地图上查找地点](https://aistudio.google.com/apps/bundled/ai-pointer-find?showPreview=true&showAssistant=true&fullscreenApplet=true)

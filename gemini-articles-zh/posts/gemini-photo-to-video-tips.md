---
title: "在 Gemini 中使用图生视频的 3 种方式"
title_en: "3 ways to use photo-to-video in Gemini"
source: https://blog.google/products-and-platforms/products/gemini/gemini-photo-to-video-tips/
site: gemini
date: 2025-09-19
crawled: 2026-09-13
translated: 2026-09-13
---

# 在 Gemini 中使用图生视频的 3 种方式

> 原文：[3 ways to use photo-to-video in Gemini](https://blog.google/products-and-platforms/products/gemini/gemini-photo-to-video-tips/) · Google

灯光。镜头。AI 开拍。🎬

作为 Google 的创意制片人，我负责为社交帖子、[视频系列](https://www.youtube.com/watch?v=QiUxprS2GPE)和面向 Googlers 的活动注入生命力。我一直在寻找创作内容、与全球观众互动的新方式。

现在隆重登场的是：由 Veo 3 驱动的 Gemini [图生视频功能](https://blog.google/products/gemini/photo-to-video/)。只需一张图片或一段文字提示词，Gemini 就能生成一段 8 秒的带声音视频——包括音效、环境背景音和语音。

以下是我使用 Gemini 图生视频的三种方式，以及一些撰写自己视频提示词的入门技巧。

## 1. 让插画动起来

把插画变成动画，为演示文稿、新闻通讯和视频带来更具冲击力的视觉效果。

```ts
Prompt: The bicycle rides through an illustration-style 
desert, weaving through cacti.
```

视频以 16:9 横向比例生成，如果你的图片是其他宽高比，则会用黑色边框填充。有时可能需要多试几次，但不要气馁！撰写提示词需要练习，我们的 Veo 模型也在不断学习和进步。

## 2. 把照片变成动态影片

把照片转化为逼真的视频片段，或者发挥想象力，增添几分奇思妙想。从一个简单、高层次的提示词开始，Gemini 会自动补全细节。

```ts
Prompt: The dinosaur skeleton comes to life.
```

再进一步，在提示词中加入详细的指令，让你自己的设想充分呈现。要让场景更有动感，可以尝试添加新角色并编排它们动作的先后顺序。

```ts
Prompt: The figure waves at the camera. While the figure 
is distracted and waving, a golden retriever dog enters the frame 
from the right, panting and wagging its tail. The dog eats the 
ice cream cone out of the figure's other hand. The figure is startled by 
this, and stares at the dog in surprise. The dog is happily wagging 
its tail and licking its lips. The figure looks at the camera.
```

你的图片将成为视频的第一帧。拍摄主体离镜头越近、越清晰，模型就越容易推进场景并生成高质量的结果。如果你担心结果看起来*过于*真实，视频带有不可见的 SynthID 数字水印和可见水印，用以标明它们是 AI 生成的。

## 3. 呈现艺术构想

提案（并拿下！）创意方案是我日常工作的重要部分。Gemini 生成的逼真画面可以更好地向他人展示我的概念，让我的提案更有说服力。

在这种情况下，提示词需要详细而精确。虽然这可能更耗时，但我发现这比纯文本提示词从零构建要快。Gemini 基于我们真实布景生成的输出，也比只能部分传达我设想的示例照片更有帮助。如果你需要帮忙，可以让 Gemini 协助完善你的提示词并加入镜头控制指令，以获得更好的效果。

```ts
Prompt: Open the scene with the image and hold for one second.
Then, the wall color changes to a bright blue, and a wooden coffee 
table appears in front of the two arm chairs in the image. On the 
coffee table appear two large podcasting microphones. The rest of the 
room is unchanged. Hold for one second. Then, the wall color changes 
to a light gray, and the microphones disappear from the coffee table. 
Next, on the table appears: a black tablecloth, two plates of chicken 
wings, and several bottles of hot sauce. The rest of the room is 
unchanged. Hold for one second. Then, the wall color changes to a 
vibrant pink. The plates of chicken wings, bottles of hot sauce, and 
black tablecloth disappear from the coffee table. Then, on the table 
appears: a bright blue table cloth and a birthday cake with lit candles. 
Birthday balloons appear and float in the background. The rest of the 
room is unchanged. Throughout the video plays an instrumental track 
of an upbeat pop song.
```

对于在创意项目中使用 AI，我至今仍在兴奋与不安之间摇摆。在这些情况下，若非 AI，这些作品根本不会存在——无论是因为缺乏资源、时间还是技能水平——这让 AI 生成的媒体得以表达并升华我的作品，而不是取代它。

亲自试试吧：Google AI Pro 订阅用户每天最多可创建三个视频，Google AI Ultra 订阅用户每天最多可创建五个视频。查看[更多技巧](https://blog.google/products/gemini/image-generation-prompting-tips/)来提升你的提示词水平，同时，订阅用户还可以[体验 Flow](https://blog.google/technology/ai/flow-video-tips/)——我们的 AI 电影创作工具，解锁更多将创意变为现实的方式。

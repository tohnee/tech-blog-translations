---
title: "我们如何用 Gemini 打造 Google I/O 2026"
title_en: "How we used Gemini to build Google I/O 2026"
source: https://blog.google/innovation-and-ai/technology/ai/io-2026-google-ai/
site: google-blog
date: 2026-06-01
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们如何用 Gemini 打造 Google I/O 2026

> 原文：[How we used Gemini to build Google I/O 2026](https://blog.google/innovation-and-ai/technology/ai/io-2026-google-ai/) · Google

[Google I/O 2026](https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-collection/) 的主题，是我们如何以新的方式让 AI 对每个人都有帮助。但在 I/O 上我们不只是发布 AI 创新的公告——我们也用这些工具把 I/O 本身变成了现实。

眼下是一个既奇怪又令人兴奋的时代。我们正经历一场惊人的转变：AI 工具每个月都在变强，实际上正在改写「我们能创造什么」的规则。

今年，我们给自己下了战书：用即将登上舞台的同一批 AI，在创新、创造力和效率上超越我们自己。

我们以前所未有的速度推进，并实时进行原型开发——把人的艺术匠心与实验性技术融为一体——最典型的例子就是「Timmy TPU」影片。

而回报在于：这些工具展示了如何释放创造力、卸下枯燥的事务，把一天中最好的时间还给团队，让他们去做自己最擅长的事。只要做得好，活动本身就足够精彩，作为观众，你甚至不会去想 AI 在其中是如何被使用的。这种转变正是我们想分享的机会，因为人们一直在问：「AI 到底能做什么？」

继续往下读，看看我们用了哪些 AI 工具、又是如何给它们写提示词的，才让 I/O 2026 得以成真。

### 「TPU Training Day」短片

**用到的 AI 产品与模型：** Google AI Studio；DeepMind 实验模型；Gemini Omni；Nano Banana

**我们做了什么：** 我们制作了一部短片，主角是一群正准备为 I/O 2026 大干一场的 TPU。

**我们是怎么做的：** 这个项目始于一个问题：我们能不能用最简单的材料——纸板和马克笔——做一部动画电影，然后用 AI 让它活起来？我们与导演 Laurie Rowan 和 Nexus Studios 合作，把木偶、传统动画与 AI 融合在一起——让人的手艺与艺术始终处在「TPU Training Day」（又名「Timmy TPU」）的核心。

首先，我们通过木偶表演和简单的 3D 动画捕捉角色表演。这让我们对取景和镜头运动拥有完全的控制。接着，我们用 Nano Banana 从这些原始素材生成风格化的首帧。为了保持帧间的一致性，我们在 Google AI Studio 里构建了一个定制工具。这让我们能够大规模测试 Nano Banana 的帧，在生成序列之前确保像素级的匹配。

我们用 Gemini Omni 和其他实验模型将基础动画与风格化帧融合。这把影片提升到了电影级的水准，同时保留了最初的人类意图。正是这些细小的人类不完美之处赋予了木偶电影魅力，而我们的 AI 流水线正是为保护这些细节而设计的。

### I/O 视觉品牌形象

![I/O 字样周围环绕着相关图标，全部采用彩虹配色，白色背景](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Collection-Hero.width-1200.format-webp.webp)

**用到的 AI 产品与模型：** Gemini 模型与 Nano Banana

**我们做了什么：** 我们为 I/O 2026 设计了视觉品牌形象，最终采用了四色渐变、叠加的透明层与互相咬合的图标。

**我们是怎么做的：** 这个品牌形象是我们团队与 AI 紧密协作的成果。我们先把过去几年的品牌规范和五年的 I/O 回顾资料喂给 Gemini 模型。早期输出并不理想，于是我们做了一系列微实验：生成新图像，再把输出连同反馈迭代地喂回 Nano Banana。我们还用 Nano Banana 探索图标风格。最终我们选定了平面 2D 图标，它们可以动态变形为超细腻质感的 3D 图标。这为主题演讲、现场标识和数字应用带来了统一连贯的品牌表达。

下面是我们用 Nano Banana 探索图标风格时用过的提示词：

```ts
You are an expert image editor. You will be given two images.

**Image 1** provides the **texture and material**.

**Image 2** provides the **pose, shape, and lighting**.

Your task is to create a new image by applying the detailed texture 
and pattern from the icon in **Image 1** onto the surface 
of the white icon in **Image 2**.

**Crucial Constraint:** The output image must perfectly preserve
the exact pose, camera angle, scale, and lighting 
of the icon in **Image 2**. Do not change its orientation 
or position in any way. The final result should be the 
icon from Image 2, but with the texture of Image 1.
```

我们的 I/O YouTube 预告片展示了最终的图标风格：

### I/O 预热演出：Jellectronica

**用到的 AI 产品与模型：** Google Antigravity；Google Colab；Google CoralNPU；Google Flow Music；Lyria 3 Pro

**我们做了什么：** 预热演出以 Jellectronica 开场——这是与蒙特雷湾水族馆（Monterey Bay Aquarium）合作的音乐生成实验，用 Lyria 3 Pro 把海月水母的游动转化为声音。

**我们是怎么做的：** 我们在 Google Colab 里训练了一个 YOLO8 模型，然后在 Google 的 Coral NPU 上运行。它追踪水母的运动来控制音乐，音乐则由 Google Flow Music 和 Lyria API 生成。比如，出现在低音声部的水母越多，低音就越响、越有能量。我们还在 Google Antigravity 里凭感觉写代码（vibe coding，氛围编程）做了一个批量音轨生成器，用来自动化生成贝斯、和弦、旋律和鼓等音乐分轨。

### I/O 预热演出：Infinite Scaler 与 Code the Countdown

**用到的 AI 产品与模型：** Google AI Studio；Gemini API；Gemini Canvas；Google Antigravity；Lyria 3；Nano Banana

**我们做了什么：** 预热演出的另一部分 Infinite Scaler 是一款电子游戏，玩家在其中竞技对战，而关卡则由玩家边玩边生成。

**我们是怎么做的：** 我们希望玩家仅凭 2D 图像生成就能快速构建无限的 3D 世界。为此，我们通过 Gemini API 用 Nano Banana 从用户的提示词和参考图像生成 sprite 精灵图集。我们把前景元素回传给 Nano Banana，生成法线贴图、粗糙度贴图和自发光贴图。由此推断出深度，让我们能够在 WebGL 渲染的 3D 纸板盒上贴上纹理，再把它们加入全局的世界堆栈。我们先用 Google AI Studio 进行快速原型开发，随后转入 Google Antigravity 进行正式开发；游戏内音乐则完全用 Lyria 3 生成。

你可以[在这里玩这款游戏，探索我们一起构建的关卡](http://infinitescaler.withgoogle.com/)。

下面是 Infinite Scaler 的一条用户提示词示例：

```ts
A majestic space fox levitating in space with a giant 
Saturn and stars behind
```

把它回传给 Gemini API 生成关卡规划后，我们得到了这条提示词：

```ts
Title: Celestial Fox Void

Color Palette: Deep navy and midnight blue backdrop, vibrant burnt
orange and dusty terracotta for the fox, soft cream and muted amber 
for Saturn rings, and deep plum shadows. All greens are replaced with 
dull, earthy dark olive tones to avoid #00FF00 interference.
    
Skyline: A vast expanse of midnight blue clay textured with dense
constellations of white and pale yellow spherical stars of varying sizes.

Sky panel: Deep indigo clay surface scattered with clusters of tiny 
white bead-like stars, creating a dense celestial field without
any bright green elements.

Floor panel: A flat plane of deep violet cosmic dust sculpted with
smooth, rounded craters and soft-molded ridges, keeping all surfaces 
matte and non-reflective.

Decorations Arch: A massive, perfectly spherical Saturn dominates the 
upper sector with thick, concentric ring layers made of hand-pressed tan 
and cream clay coils.

Decorations Ground: A majestic fox with flowing clay-sculpted fur
levitates at the center, surrounded by floating, multi-sized clay
asteroids and small, irregular space debris particles.
```

这条提示词生成了下面这张 sprite 精灵图集。游戏的精灵图集按一致的模板把多个元素组合在一起，并使用绿幕背景以便于抠像。

![sprite 精灵图集，包含狐狸、土星等多个图像，背景为柠檬绿色](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/fox-sprite.width-1200.format-webp.webp)

这一流程最终产出了像这样完全可玩的 3D 关卡：

最后，我们播放了一条倒计时，其中的代码来自全球创作者在 Code the Countdown 挑战中的投稿。[我们邀请大家](https://x.com/googledevs/status/2050245538730168343)在 Canvas 或 AI Studio 中设计 1 到 10 的数字，然后把它们拼接成一段由代码驱动的倒计时。

### Antigravity Coffee Co. 快闪店

![I/O 现场的 Antigravity Coffee Co. 快闪店](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Antigravity_Coffee_Co..width-100.format-webp.webp)

![Antigravity Coffee Co. 的自行车造型精致拿铁拉花](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Antigravity_Coffee_Co._2.width-100.format-webp.webp)

**用到的 AI 产品与模型：** Flutter；Gemini Enterprise Agent Platform；Google Antigravity；Nano Banana

**我们做了什么：** 我们做了一个应用，让 I/O 参会者可以设计并下单带定制拉花的拿铁，然后再亲手打造属于自己版本的「史上最疯狂」咖啡应用。

**我们是怎么做的：** 我们用生成式 UI 和 A2UI 协议配合 Flutter 构建了能实时变化的自适应界面，用动态的用户交互取代了静态表单。Firebase 在前端与 Nano Banana 等模型之间架起桥梁，负责处理复杂的推理与内容生成。单一的 Flutter 代码库在不同的硬件设备上都交付了高质量、零延迟的体验。我们依赖 Google Cloud 和 Firebase——包括 Cloud Functions、Firestore 和 Cloud Ops——解决了构建和监控现代生成式 AI 应用的复杂性问题。参会者还借助 Google Antigravity 的智能体化编程，快速构建了自己的下单应用。

### 讲者标题卡

**用到的 AI 产品与模型：** Gemini Omni；Google Flow；Nano Banana Pro

**我们做了什么：** 每位讲者都有一张用我们的图像和视频生成模型定制的标题卡。

**我们是怎么做的：** 我们的 Google Labs 与 Google Gemini 副总裁 Josh Woodward 就是一个很好的例子。在现场，参会者看到数字版的 Josh 骑着 Chrome 小恐龙，随后完成了一记扣篮。

我们用 Nano Banana Pro 生成核心素材，比如「要素」参考图集。我们用这些要素进行分镜，尝试不同的变化并添加个人细节。在 Google Flow 中，我们先借助 Veo 帮助原型化动作并生成扣篮之类的动画。我们还在 Google Flow 里用 Gemini Omni 生成了动画，这在处理复杂的体育动作时格外有用。详细的文字提示词保证了 AI 输出与参考图集的一致性。最后，我们把生成视频中的原始动作进行合成和时间重映射，做成精致的标题卡。

下面是我们生成「要素」参考图集时用过的提示词：

```ts
Man casually riding the trex. He looks comfortable like he has
done this many times before. Man is relaxed and holding reins on
the trex. Expand and show more of scene. Keep the cacti. Lighting on 
man makes sense. Man is also lit by dawn lighting like rest of scene.
```

之后我们在 Google Flow 中使用的视频提示词如下：

```ts
Show me the rest of this scene. Keep consistent with the 
character sheet, especially the style of the trex. The trex jumps
over the cacti. Slam dunk.
```

### 贴纸周边

![四款图案各异的 3D I/O 贴纸，其中包括黑紫色的星系图案](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/IO_Stickers.width-1200.format-webp.webp)

**用到的 AI 产品与模型：** Gemini 与 Nano Banana

**我们做了什么：** 我们为参会者现场生成并打印定制的 I/O 贴纸。

**我们是怎么做的：** 我们在自定义 Web 应用上做了一个互动贴纸游戏。玩家有 20 秒时间，用一只 Android 小机器人接住不断落下的提示词。提示词类别超过 100 种——从蓝莓、迪斯科球到激光和木头。玩家选择两个提示词，或点「手气不错」随机搭配。我们的后端——使用面向 Gemini 和 Android 的 Nano Banana——将这些选择融合在一起，生成高度个性化的定制 I/O 贴纸设计。想象一下用纯金华夫饼做成的 3D「I/O」，或者一块小熊软糖主板。设计完成后立刻打印出来，供参会者领取。

下面是我们生成贴纸设计时用过的提示词示例，先是一些通用准则：

```ts
You are an advanced, highly precise AI image generation rendering
engine. Your primary function is to apply complex materials and
artistic styles to a specific 3D layout provided by the user.
```

接着，我们为各个元素补充细节，比如颜色、光照，以及下例中的标志性「I/O」造型：

```ts
The geometry of the object (the vertical block, slanted slab, and
short cylinder forming "I/O") is immutable. You must perfectly
align the generated textures with the boundaries, depth and
perspective of the input layout. Do not alter the underlying 3D
shapes, pose or scale.
```

想深入了解，可以在[这里回顾我们 I/O 2026 的诸多重要公告](https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/)。

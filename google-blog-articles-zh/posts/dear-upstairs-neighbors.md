---
title: "《Dear Upstairs Neighbors》：动画师与 AI 研究者如何共创这部短片"
title_en: "How animators and AI researchers made ‘Dear Upstairs Neighbors’"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/dear-upstairs-neighbors/
site: google-blog
date: 2026-01-26
crawled: 2026-09-13
translated: 2026-09-13
---

# 《Dear Upstairs Neighbors》：动画师与 AI 研究者如何共创这部短片

> 原文：[How animators and AI researchers made ‘Dear Upstairs Neighbors’](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/dear-upstairs-neighbors/) · Google

今天，我们的动画短片《Dear Upstairs Neighbors》在圣丹斯电影节（Sundance Film Festival）首映。影片将在圣丹斯协会（Sundance Institute）的 Story Forum 展出——这是一个聚焦「艺术家优先」工具与技术、支持视觉叙事的空间。

《Dear Upstairs Neighbors》（《致楼上的邻居》）讲述了一位年轻女子 Ada 的故事：她渴望睡上一个好觉，却被楼上极其吵闹的邻居折磨得无法入眠。当她拼命想象楼上那片喧嚣究竟是怎么搞出来的时候，现实渐渐滑向幻想，一场为宁静与理智而战的史诗大战就此拉开帷幕。

这部影片是[动画界资深人士](https://www.imdb.com/title/tt39368604/reference)——包括导演、Pixar 出身的 Connie He——与 Google DeepMind 研究者的合作成果，双方因一个共同的目标走到一起：探索生成式工具如何融入艺术家的创作流程。

导演 Connie He 根据自己与吵闹邻居打交道的亲身经历构思了这个故事。在她的分镜中，她设想了一系列随着深夜推进而愈发癫狂、愈发荒诞的幻觉。

![一系列手绘画作，展示 Ada——一位穿着睡衣、蓝黑色卷发随意挽成蓬松发髻的年轻女子——以中立姿势站立，从多个不同角度呈现。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure02_character_turnaround_bed.width-100.format-webp.webp)

为我们的主角 Ada，美术指导 Yingzong Xin 创作了一个古怪而独特的设计，比例夸张、造型语言棱角分明。

![一系列画作，展示 Ada 的脸上各种夸张的表情：喜悦、愤怒、恐惧、惊奇、打哈欠，等等。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure03_DUN_Expression_color_v1_.width-100.format-webp.webp)

Ada 的脸极富表现力。角色模型表由 Yingzong Xin 绘制。

![一幅 Ada 卧室的画作，展示她的床、书桌、书架和各类物品的布置，以等轴测视角和冷色调呈现。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure03a_Ada_bedroom_1080p.width-100.format-webp.webp)

Ada 的卧室以冷色调渲染，传达出平静、舒适与庇护之感。场景设计由 Yingzong Xin 完成。

![一幅锯子锯木头的画作，在黑色背景上使用鲜艳的霓虹青绿、品红与黄色。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure04_Log_1080p.width-100.format-webp.webp)

Ada 的幻觉采用粗粝的风格和霓虹配色，与卧室所在的「真实世界」形成区分。概念艺术由 Yingzong Xin 创作。

![一幅画作：Ada 站在床上，被所有的噪音激怒——她嘴角扭曲成愤怒的怪相，双拳紧握，红橙色的火焰从她全身四面八方迸发而出。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure05_700_6_1080p.width-100.format-webp.webp)

绘画风格时刻在变化，通过色彩与质感表达 Ada 不断变化的情绪。概念艺术由 Yingzong Xin 创作。

![一幅表现主义画作：一个巨型扬声器阴森地悬浮在神秘景观之上，以刺眼的黑、红、黄色调呈现。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Figure06_700_8_1080p.width-100.format-webp.webp)

在最激烈的时刻，抽象表现主义风格蔓延至整个场景。概念艺术由 Yingzong Xin 创作。

从一开始，团队的愿景就是让动画艺术家既能从生成式 AI 的创意潜力中受益，又不必把艺术控制权拱手让给它固有的不可预测性。为了确立她对这部影片的构想，Connie 制作了分镜，并邀请获奖美术指导 Yingzong Xin 创作概念艺术和角色设计。我们承诺在整个镜头制作过程中始终忠于这一艺术愿景。

表现主义视觉风格是这部影片叙事的核心——而用传统动画手法实现它极其困难。我们原本期待 AI 能帮助填补这一空缺，但很快发现这些风格太过独特、我们的设计选择太过具体，以至于我们的研究者必须开发全新的能力，才能提供将影片变为现实所需的定制化与控制力。

## 微调出新的视觉风格

我们的第一个挑战，是生成与 Ada 的角色设计以及定义每个场景的绘画风格保持一致的镜头。为了达到高质量和一致性，我们的研究者构建了工具，让艺术家能够在自己的作品上微调（fine-tune）定制的 Veo 和 Imagen 模型，仅凭少量示例图像就教会模型新的视觉概念。

![由十二幅色彩斑斓的绘画图像组成的网格，展示 Ada 的各种场景：游泳、攀岩、拳击、踢足球、打碟、与孩子们在瀑布中嬉戏、在极地景观中惊奇地凝视极光，等等。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WM_AdaT2I_1080p.width-100.format-webp.webp)

微调后由 Imagen 生成的 Ada 图像。微调后的模型帮助整个团队探索 Ada 这一角色。

左：Yingzong Xin 的画作。右：微调后由 Veo 生成的风格化动画视频。Veo 从我们的概念艺术中学到的东西令我们惊讶：不只是色彩和质感这类表面细节，还有两点透视这样的深层艺术概念。

上：Ada 的角色设计遵循严格的二维规则：她标志性的蓬松头发和凌乱发髻必须始终是她轮廓的一部分，绝不能遮挡她的脸。左下：Ada 头发的 3D 雕塑不可能在每个角度都看起来正确，因为实体形态违反了那些 2D 规则。右下：Veo 在 Ada 图像上微调后，无缝化解了这一冲突——当头部转动时，形状平滑地适应，始终保持轮廓正确。

## 展示，而非输入

另一个挑战是精确控制每个镜头的内容与运动。我们知道，仅靠文本提示永远无法控制 Ada 睡意惺忪的手指敲击键盘的节奏、她面部表情的喜剧时机，或一个镜头揭晓时的精确取景。我们需要一种方式，把这种程度的细腻与具体传达给我们的 AI 模型。我们的研究者从动画师的视觉沟通方式中获得灵感——他们通过绘画、上色或亲身演绎场景来交流。我们开发了新颖的视频到视频（video-to-video）工作流，让动画师能够以视觉方式传达意图：用他们顺手的工具制作粗略动画。我们的模型随后将这些动画转化为完全风格化、跟随输入运动的视频，并在严格控制与创意即兴之间提供可调节的平衡。

使用微调后的 Veo 模型进行文生视频，生成的场景看起来确实像 Ada，但动作随机、失控，而且常常很怪异。仅凭文本无法传达叙事动画电影所需的细腻与具体。

为了打造足以承载故事的细腻表演，我们的动画师采用了传统方法。动画师 Ben Knight 在 Maya 中为这个场景制作了粗略 3D 动画，研究者 Andy Coenen 使用微调后的 Veo 模型将其转化为最终外观。

视频到视频方法让每位艺术家都能在自己的舒适区工作，使用他们最喜爱的动画工具。动画师 Mattias Breitholtz 用 TV Paint 制作了这段粗略 2D 动画，研究者 Forrester Cole 在自定义 ComfyUI 工作流中使用微调版 Imagen，逐帧将其转化为最终外观。

动画师 Steven Chao 在 Maya 中为 Ada 制作动画并创建了动态低多边形（low-poly）效果，研究者 Ellen Jiang 和导演 Connie He 使用微调后的 Veo 和 Imagen 模型将这些元素转化为表现主义外观。画布质感断续变换的节奏为动作场面增添了张力。

## 迭代至完美

即使有了微调和视频到视频工作流提供的控制力，我们的最终镜头也没有一个是一次「一键」生成的。与任何电影制作一样，我们在「每日审片」（dailies）环节点评每个镜头，经过数轮反馈才能把每个细节做到位。为了避免每次迭代都从头重新生成，我们构建了局部精修工具，让我们能够以可调节的控制程度编辑视频的特定区域。

为了制作 Ada 幻觉中那条嚎叫的狗，我们从 Yingzong Xin 的一幅概念画开始，用 Veo 的图像到视频功能让它活了起来。Veo 的第一版输出（未经微调）对我们的影片来说过于照片级写实；于是我们使用微调版 Veo，让这个镜头更接近我们想要的视觉风格。视频到视频工作流让我们可以在 Veo 与 Premiere 等传统工具之间自由切换。

将微调后的 Veo 与视频到视频工作流相结合，让我们可以在狗的造型及其周围绘画效果的设计上反复迭代，以前所未有的自由度和控制力探索各种风格变化。

监制动画师 Cassidy Curtis 在 Maya 中为这个镜头制作了粗略 3D 动画，研究者 Erika Lu 微调了一个 Veo 模型将其转化为最终外观。为了改善 Ada 头发的轮廓，Lu 添加了一个粗略蒙版，标示出需要更多头发的区域，然后用 Veo 即兴补出一缕头发，与镜头其余部分无缝融合。

最后，为了让影片登上大银幕，我们使用 Veo 的超分辨率（upscaling）能力将最终镜头提升到 4K 分辨率。在艺术家点评的指引下，我们的研究者仔细调整模型的行为，添加丰富的细节，同时保留艺术风格的每一分细腻。Veo 4K 超分辨率模型现已在 Flow 中提供，并将于本月晚些时候登陆 Google AI Studio 和 Vertex AI，以满足电影人的实际需求。

每个镜头都带来了独特的挑战。在制作过程中，我们的跨学科团队开发了多种工作流，将手工动画的精确控制与生成式 AI 的风格灵活性和可扩展性相结合。我们的 AI 模型不仅产出了令人捧腹的废片（bloopers），还常常以出人意料的美妙而富有创意的解决方案给我们惊喜。从每天聚在一起、以精细的艺术意图和用心打磨每个镜头的过程中，我们收获了宝贵的经验。我们的艺术家通过直接接触实验性研究获得了新的创作力量，并用他们的技艺和视角帮助塑造了它的发展方向。我们的研究者则作为技术美术（technical artists）获得了实战经验，快速原型化解决方案，突破了艺术与技术上的壁垒。我们很高兴能继续践行我们的使命：与专业艺术家和电影人一起、并为他们构建生成式 AI。

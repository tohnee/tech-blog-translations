---
title: "一帧一帧，重现一段跨越 70 年的爱情故事"
title_en: "Recreating a 70-year love story frame by frame"
source: https://blog.google/innovation-and-ai/technology/ai/love-rendered-film/
site: google-blog
date: 2026-09-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 一帧一帧，重现一段跨越 70 年的爱情故事

> 原文：[Recreating a 70-year love story frame by frame](https://blog.google/innovation-and-ai/technology/ai/love-rendered-film/) · Google

纪录片短片《Love, Rendered》探索了记忆消逝与叙事的力量——并展示了技术如何帮助重新唤起那些开始褪色的记忆。影片跟拍了结婚已逾 70 年的 Burt 和 Ethelle Shatz 夫妇，记录他们如何面对 Burt 的认知衰退。在他日渐消逝的记忆中，有一段尤为珍贵：两人在克利夫兰一所学生合作社相识的那一天。由于那天既没有拍照也没有录像，这段时光只存在于他们的脑海中。

当我以影片技术负责人的身份加入时，我就知道这个项目在情感上的分量与它在技术上的复杂程度不相上下。记忆消逝对我而言是一件切身的私事。我的祖父在去世前曾经历中风和记忆丧失。我最后一次探望他时已经三十多岁，他却坚信我还在读大学，并为我就要毕业而高兴不已。那段苦乐参半的记忆从未离开过我。

这段经历让我想看看，这项技术能否通过同样的媒介帮助我与家人建立更深的联结。项目开始时，我向父亲要来了一些老的家庭照片。我在父母相识时期的照片上测试了我们的图像修复功能，并用我们的视频模型让照片动了起来。看着父母以二十出头的模样动起来，我真切地体会到，这些工具能帮助我们把最重要的东西从流逝中留住。

《Love, Rendered》由曾获奥斯卡提名的电影人 Liz Garbus 执导，并与 Dan Cogan 和 Darren Aronofsky 共同制片。影片由 Google DeepMind 与 Aronofsky 的创意公司 Primordial Soup 合作完成。

## 探索记忆之谜

Liz 和 Darren 都是带着对记忆韧性的好奇投入到这部影片中的。在执导纪录片《Coma》时，Liz 看到处于微意识状态的患者在听到熟悉的声音或看到亲人的照片时，fMRI 扫描图像会亮起。几年后，Darren 看到了一段影像：一位患有阿尔茨海默病的前芭蕾舞演员，在听到《天鹅湖》时，本能地在轮椅上跳起了那段编舞。

这些事例引导创作团队转向了怀旧疗法（reminiscence therapy）——一种临床实践，通过歌曲、家庭故事和老照片等感官线索来唤起记忆、引发对话、重燃情感联结。但如果一段记忆没有这样的线索可依附呢？

为了重现 Burt 和 Ethelle 那段未曾被记录的过去，影片制作方与我的团队展开了合作。Ethelle 坐在我们身旁，成为一位积极的共同创作者，纠正楼梯的弧度或鞋跟的形状。

## 用 AI 捕捉人性的本质

我们与 Primordial Soup 团队并肩工作，将新兴的 AI 模型用作艺术媒介和工具箱，每一步都以人的创意方向来引导这项技术。

弥合缺失细节之间的空隙，需要一个旨在保留情感真实性的两部分技术方案。

- **图像修复：**团队使用生成模型修复了 Burt 和 Ethelle 年轻时的黑白照片。修复后的照片有助于确保后续的重建忠实于照片中的人物。

![修复后的 Burt 与 Ethelle 照片](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/love_rendered_inline.width-1200.format-webp.webp)

- **姿态与表演控制：**工程师们使用我们的表演捕捉模型，映射出 Burt 和 Ethelle 如今的细微举止——Burt 头部特有的倾斜角度、他说话方式中短暂的迟疑、眼角细微的皱纹。将这些特征映射到他们年轻的形象上，让重现的画面鲜活起来。

![Burt 的重现形象](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/love_rendered_inline_2.width-1200.format-webp.webp)

将这两种媒介结合，让我们得以把 Burt 和 Ethelle 的过去与现在交织在一起。由此，我们生成了一段"记忆"——他们告诉我们，这段记忆感觉真实可信。

请看我的同事 Jess Gallegos 更详细地讲解这一工作流程。

正如 Darren 在制作过程中所说，工具——就像画笔或锤子——在被人类之手引导之前什么也做不了。在《Love, Rendered》中，机器学习就是我们用来引导 Burt 和 Ethelle 重返时光的工具，帮助他们握住那个正在消逝的瞬间。

你可以[在这里观看完整影片](https://youtu.be/TYlsVEtKe-8?si=KlcWZsYLE_npPx2G)，一帧一帧地感受他们的爱情故事。

## 留存你家人的故事

无论你是想与祖辈建立更深的联结，还是想保存家庭的核心记忆，都可以在 [Gemini 应用](https://gemini.google.com/app)中修复老照片。上传照片图像，然后问 Gemini："你能修复并给这张照片上色吗？请保留人物的外貌、表情和姿态。"

---
title: "Gemini 如何参与共同创作这首当代古典乐作品"
title_en: "How Gemini co-composed this contemporary classical music piece"
source: https://blog.google/products-and-platforms/products/gemini/google-arts-culture-gemini-orchestra/
site: gemini
date: 2025-01-28
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 如何参与共同创作这首当代古典乐作品

> 原文：[How Gemini co-composed this contemporary classical music piece](https://blog.google/products-and-platforms/products/gemini/google-arts-culture-gemini-orchestra/) · Google

在"[The Twin Paradox: A Symphonic Discourse](https://www.youtube.com/watch?v=wBq0ZnAd0HQ)"——这首由慕尼黑交响乐团于去年年底首演的当代古典音乐新作——中，有一个片段因其令人屏息的张力而格外突出。当全曲五个乐章中的第四乐章逼近高潮时，圆号以凌厉的顿奏开始轰鸣，尖啸的小提琴层层堆叠，鼓声在下方隆隆作响。

它给人的感觉更像金属乐而不是莫扎特——而这正是有意为之。

"The Twin Paradox"由一个独特的三人组合创作：德国作曲家 [Jakob Haas](https://jakob-haas.de/) 和 [Adrian Sieber](http://adriansieber.de/)，以及世界音乐厅的一位新客——[通过 Google AI Studio 调用的 Gemini API](https://aistudio.google.com/prompts/new_chat)。两位作曲家说，虽然这个模型本身无法谱写或创作音乐，但它是一位宝贵的合作者，能够提出叙事创意、配器方案和音乐动机方面的建议。而且偶尔还会放飞自我。

在创作过程中，Jakob 和 Adrian 利用了 Gemini 的多模态能力：他们拍摄了对乐团 12 名成员的采访，以及每位乐手用各自乐器即兴演奏的几分钟视频。他们把这些素材上传到 Gemini，然后请它为每位乐手提供音乐创意——既要契合他们的热情所在，又要融入他们正在构建的整体作品。

"我们的打击乐手 Alex 在开始古典音乐生涯之前，曾在金属乐队里演奏，"本身也是乐团大提琴手的 Jakob 说。"他即兴演奏了一种他在金属乐中使用的特殊鼓点，当我们请 Gemini 为第四乐章建议一个节奏时，那个声音浮现了出来。它成为了整个乐章段落的基础。"

"The Twin Paradox"项目是作曲家、乐团、[Google Arts & Culture](https://artsandculture.google.com/) 与 Google 德国之间的合作。Jakob 此前曾与 Google 合作，为一个把 AI 带给学生的项目开发音乐模块，他由此萌生了与 AI 共同作曲的想法，并很快被介绍给在古典音乐方面拥有悠久实验历史的 Google Arts & Culture 团队。

"我们曾与著名唱片公司 Deutsche Grammophon 合作，[数字化一些有史以来最古老的唱片](https://artsandculture.google.com/story/the-shellac-project-deutsche-grammophon/OAXRla_BJlVMJg)，还制作过汉堡易北爱乐音乐厅开幕演出的 360° 影像，"Google Arts & Culture 高级项目经理 Simon Rein 说。"这个项目对我而言的特别之处在于，它强调了 AI 如何支持创造力与人与人的连接：作曲家与 Gemini 共同写出作品，乐团聚在一起琢磨如何演奏它，最后你走进一场音乐会，数百人共同欣赏它。"

Gemini 对这首作品的第一个重大贡献是曲名。"我们一开始给 Gemini 提供了基本信息：可用的乐器数量和类型、作品的目标时长，以及这将是一件人类作曲家与 AI 共同创作的作品。然后我们说：'好，给我们起个名字吧，'"Jakob 解释道。Gemini 以一种巧妙的自指方式建议了"The Twin Paradox"（孪生子佯谬）——相对论中一个思想实验的名字：如果一对双胞胎中的一个以接近光速进行长时间的太空旅行，那么他返回时将比自己的同胞兄弟衰老得更少。

"接着我们挑战 Gemini，让它告诉我们 The Twin Paradox 作为音乐听起来会是什么样子，"Jakob 说。"它建议同时使用不同的节拍，以及*滑音（glissandi）*——即在音符之间滑动——来表现时间的拉伸与压缩。这真正启发了我们。就是在那时我想：'哇，这事儿能成。'"

在之后的几个月里，Jakob 在自己的笔记本电脑上通过 Google AI Studio 与 Gemini API 交互，把它的建议发给 Adrian，后者将这些想法转化为乐谱并在钢琴上弹奏。两人会讨论结果，反复打磨，再挑选出要纳入作品的内容。

Jakob 与 Gemini 互动寻找灵感（左），Adrian 将这些想法转化为音乐（右）。

![左侧，一个身穿灰色 T 恤的男人坐在书桌前，面前有一台笔记本电脑，还有显示器、音箱和混音设备。右侧，一个身穿深色衬衫的男人坐在钢琴前，双臂扬起。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Jakob_and_Adrian.width-1200.format-webp.webp)

有效的提示词至关重要，团队与 Google Arts & Culture 实验室合作开发并微调他们的输入。考虑到 AI 模型由于在既有数据集上训练，往往会模仿已经存在的音乐创意，Jakob 和 Adrian 避免建议任何具体的音乐风格或任何知名作曲家。他们还采用了他们称之为"隐喻式提示"（metaphorical prompting）的方法：提供概念、图像或视频来激发音乐创意，而不是直接要求具体的音乐元素。

其中最精心设计的提示词，正是那些乐团视频——它们催生了那段震撼的金属乐时刻。而最具自我指涉意味的一次，是他们请模型反思与作曲家合作这一过程本身。结果如何？第二乐章中一个特别的段落：双簧管和独奏小提琴扮演发问的人声，而打击乐和铜管乐器则以金属质感的、机械式的回答作应。不妨称之为"Gemini 演绎 Gemini"。

"The Twin Paradox"于 10 月在慕尼黑的 [Prinzregententheater](https://maps.app.goo.gl/i3Yh6LVf6m4LJyVK9) 首次亮相。Simon 在作曲家开发期间分享的音频文件中、以及在他出席的一场最终彩排中，已经对听到的内容印象深刻，但仍有紧张。"所幸，演出当晚，它赢得了热烈的掌声，"他说。"听众入迷了——他们被打动了。"

"The Twin Paradox: A Symphonic Discourse" 的乐谱节选。

![一张乐谱，标题为 V. Resolution and Revelation。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/The_Twin_Paradox_sheet_music.width-1200.format-webp.webp)

Jakob 那晚没有登台，而是在第一排观看。他记得现场那股能真切感受到的紧张气氛——尤其是在第四乐章。"令人屏息，"他说。

虽然他还没有确定下一个项目，但他表示会继续试验 AI。

他甚至可能尝试一种更*多模态*的音乐艺术形式。

"Adrian 创作了许多歌剧，我们一直在讨论这种形式多么适合发挥 Gemini 这类模型的长处，"Jakob 说。"你不再局限于音乐本身，还有歌词、场景描述和视觉元素等等。这只是其中一个想法。如果我需要更多灵感，我知道可以去哪里问……"

---
title: "绘制生成式 AI 的滥用图谱"
title_en: "Mapping the misuse of generative AI"
source: https://deepmind.google/blog/mapping-the-misuse-of-generative-ai/
site: deepmind
date: 2024-08-02
crawled: 2026-09-13
translated: 2026-09-13
---

# 绘制生成式 AI 的滥用图谱

> 原文：[Mapping the misuse of generative AI](https://deepmind.google/blog/mapping-the-misuse-of-generative-ai/) · Google DeepMind

新研究分析了当今多模态生成式 AI 的滥用情况，以帮助构建更安全、更负责任的技术

能够生成图像、文本、音频、视频等的生成式人工智能（AI）模型正在开启一个创造力与商业机遇的新时代。然而，随着这些能力的增长，其被滥用的潜力也在增长，包括操纵、欺诈、霸凌或骚扰。

作为[我们负责任地开发和部署 AI 承诺](https://ai.google/responsibility/principles/)的一部分，我们与 [Jigsaw](https://jigsaw.google.com/) 和 [Google.org](http://google.org/) 合作发表了一篇[新论文](https://arxiv.org/abs/2406.13843)，分析生成式 AI 技术如今是如何被滥用的。Google 内部各团队正在利用这项研究和其他研究，为我们的生成式 AI 技术开发更好的防护措施，同时也推进其他安全举措。

我们一起收集并分析了近 200 篇媒体报道，涵盖 2023 年 1 月至 2024 年 3 月间公开发生的滥用事件。从这些报道中，我们定义并归类了滥用生成式 AI 的常见策略，并发现了这些技术被利用或攻陷的新颖模式。

通过厘清不同类型生成式 AI 输出中当前的威胁与策略，我们的工作有助于塑造 AI 治理，并指导 Google 等构建 AI 技术的公司制定更全面的安全评估与缓解策略。

## 重点展示滥用的重要类别

虽然生成式 AI 工具代表了一种独特而引人注目的提升创造力的手段，但生成定制化、逼真内容的能力也可能被恶意行为者以不当方式使用。

通过分析媒体报道，我们识别出生成式 AI 滥用策略的两大主要类别：对生成式 AI 能力的利用（exploitation）和对生成式 AI 系统的攻陷（compromise）。技术被利用的例子包括创建逼真的人物肖像来冒充公众人物；技术被攻陷的例子则包括通过"越狱"（jailbreaking）移除模型防护措施，以及使用对抗性输入造成模型故障。

![一张条形图，展示生成式 AI 滥用策略的出现频率。图表显示"对生成式 AI 能力的利用"（深紫色条）远比"对生成式 AI 系统的攻陷"（浅紫色条）普遍，其中"冒充"是总体上最频繁的策略，超过 20%。](https://lh3.googleusercontent.com/Bk68MM5pHa6B-ZlTL2YQ0YvC61bNPU6sBtQXnSf_KSY1Cdei9KFqqTcbCZmuAtvoGG1HAb_XNw5LhnbyenrbxIZRqtaE7cI4BS3f2p8vemsngmX5UA=w1440)

我们数据集中生成式 AI 滥用策略的相对频率。媒体报道的任何一起滥用案例都可能涉及一种或多种策略。

"利用"类案例——涉及恶意行为者利用易于获取的消费级生成式 AI 工具，且往往无需高级技术技能——在我们的数据集中最为普遍。例如，我们审阅了 2024 年 2 月的一起高知名度案件，一家跨国公司[据报损失了 2 亿港元](https://www.scmp.com/news/hong-kong/law-and-crime/article/3250851/everyone-looked-real-multinational-firms-hong-kong-office-loses-hk200-million-after-scammers-stage)（约合 2,600 万美元），一名员工在一次线上会议中被诱骗进行了一笔财务转账。在这起事件中，会议上的其他每一位"与会者"——包括该公司的首席财务官——实际上都是以假乱真的计算机生成的冒充者。

我们观察到的一些最突出的策略，如冒充、诈骗和合成人格，早于生成式 AI 的发明，长期以来一直被用来影响信息生态系统和操纵他人。但生成式 AI 工具的更广泛获取可能改变信息操纵背后的成本与激励，赋予这些由来已久的策略新的威力和潜力，尤其是对那些此前缺乏足够技术手段来运用此类策略的人。

## 识别滥用的策略与组合

伪造证据和操纵人物肖像是现实世界滥用案例中最普遍策略的基础。在我们分析的时间段内，大多数生成式 AI 滥用案例都是为了影响公众舆论、实施诈骗或欺诈活动，或牟取利润。

通过观察不良行为者如何组合他们的生成式 AI 滥用策略以追求各自的目标，我们识别出特定的滥用组合，并将这些组合标记为策略（strategies）。

![一张桑基图，将生成式 AI 滥用的目标（左）映射到实现这些目标的具体策略（右）。紫色代表舆论操纵，主要连接到虚假信息；绿色代表变现与牟利，连接到深度伪造商品化和内容农场；红色代表诈骗与欺诈，连接到名人诈骗广告和钓鱼攻击；蓝色代表骚扰，连接到诽谤和霸凌；橙色代表传播，连接到剽窃和数字复活；黄色代表恐怖主义与极端主义，连接到宣传；浅蓝色代表网络攻击，连接到信息窃取。](https://lh3.googleusercontent.com/r4oeN12XS9EVAmIQauX_pYFkFD4nvR_VTmWxBjCngsuEEWVQJDLnRJ1ZbnafoUMI7oxpBDO65jLDKcLk-mQc3SZzSIcM_TeaQDslLiNrqt_55HgkZw=w1440)

不良行为者的目标（左）如何映射到其滥用策略（右）的示意图。

新兴的生成式 AI 滥用形式虽然并非公然恶意，但同样引发了伦理关切。例如，新型的政治沟通方式正在模糊真实与欺骗之间的界限：[政府官员突然说起各种有利于争取选民的语言](https://www.nytimes.com/2023/10/20/nyregion/ai-robocalls-eric-adams.html)却没有透明地披露他们在使用生成式 AI；[活动人士利用 AI 生成的遇难者声音呼吁枪支改革](https://www.theguardian.com/us-news/2024/feb/14/ai-shooting-victims-calls-gun-reform)。

虽然这项研究对新兴滥用形式提供了新颖洞见，但值得注意的是，该数据集只是媒体报道的有限样本。媒体报道可能优先关注耸人听闻的事件，这反过来可能使数据集偏向某些特定类型的滥用。由于生成式 AI 系统如此新颖，相关人员检测或报告滥用案例也可能更具挑战性。该数据集也没有直接比较生成式 AI 系统的滥用与传统内容创作和操纵策略，例如图像编辑，或搭建"内容农场"来批量生产文本、视频、GIF、图像等。到目前为止，坊间证据表明，传统的内容操纵策略仍然更为普遍。

## 领先一步防范潜在滥用

我们的[论文](https://arxiv.org/abs/2406.13843)指出了设计保护公众举措的机会，例如推进广泛的生成式 AI 素养宣传、开发更好的干预措施以保护公众免受不良行为者侵害，或[预先警示人们并为其提供装备](https://medium.com/jigsaw/prebunking-to-build-defenses-against-online-manipulation-tactics-in-germany-a1dbfbc67a1a)，使其能够识别并驳斥生成式 AI 滥用中使用的操纵性策略。

这项研究为我们的安全举措开发提供了依据，帮助我们的团队更好地保护我们的产品。在 YouTube 上，我们现在[要求创作者声明其作品被实质性修改或合成生成且看起来逼真的情况](https://support.google.com/youtube/thread/264550152/new-disclosures-and-labels-for-generative-ai-content-on-youtube?hl=en)。同样，我们更新了选举广告政策，要求广告主在选举广告包含经数字修改或生成的内容时予以披露。

随着我们继续加深对生成式 AI 恶意使用的理解并取得进一步的技术进步，我们深知确保我们的工作不囿于孤岛比以往任何时候都更加重要。我们最近加入了[内容溯源与真实性联盟](https://c2pa.org/)（C2PA）担任指导委员会成员，帮助制定技术标准并推动 Content Credentials 的采用——这是一类防篡改的元数据，展示内容是如何被制作和逐步编辑的。

与此同时，我们还在开展推进现有红队测试工作的研究，包括[改进测试大语言模型（LLM）安全性的最佳实践](https://arxiv.org/abs/2406.11757v1)，以及开发让 AI 生成内容更容易识别的开创性工具，例如正在被集成到越来越多产品中的 [SynthID](https://deepmind.google/technologies/synthid/)。

近年来，Jigsaw 曾[与虚假信息创作者共同开展研究](https://arxiv.org/abs/2405.13554)以了解他们使用的工具和策略，[开发预警视频](https://prebunking.withgoogle.com/)（prebunking）让人们预先警惕针对自己的操纵企图，并[证明预警宣传可以在规模化水平上提升对虚假信息的免疫力](https://www.science.org/doi/10.1126/sciadv.abo6254)。这项工作构成了 Jigsaw 更广泛的信息干预组合的一部分，帮助人们在网络上自我保护。

通过主动应对潜在滥用，我们可以促进生成式 AI 的负责任和合乎伦理的使用，同时将其风险降至最低。我们希望这些关于最常见滥用策略与手法的洞见，能帮助研究者、政策制定者和行业信任与安全团队构建更安全、更负责任的技术，并制定更好的反滥用措施。

[阅读我们的论文](https://arxiv.org/abs/2406.13843)[进一步了解 Jigsaw](https://jigsaw.google.com/)

**致谢**

这项研究是 Nahema Marchal、Rachel Xu、Rasmi Elasmar、Iason Gabriel、Beth Goldberg 和 William Isaac 的集体成果，并得到了 Mikel Rodriguez、Vijay Bolina、Alexios Mantzarlis、Seliem El-Sayed、Mevan Babakar、Matt Botvinick、Canfer Akbulut、Harry Law、Sébastien Krier、Ziad Reslan、Boxi Wu、Frankie Garcia 和 Jennie Brennan 的反馈与顾问贡献。

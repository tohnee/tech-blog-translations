---
title: "认识我们 Built with Opus 4.6 Claude Code 黑客松的获奖者"
title_en: "Meet the winners of our Built with Opus 4.6 Claude Code hackathon"
date: 2026-04-20
source: https://claude.com/resources/articles/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon
crawled: 2026-11-17
translated: 2026-11-17
---

# 认识我们 Built with Opus 4.6 Claude Code 黑客松的获奖者

> 原文：[Meet the winners of our Built with Opus 4.6 Claude Code hackathon](https://claude.com/resources/articles/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon) · Claude 博客

从心脏病专家到电子音乐人，来认识我们 Built with Opus 4.6 黑客松的获奖者。

上周，我们宣布了 [*Built with Opus 4.7* 线上 Claude Code 黑客松](https://cerebralvalley.ai/e/built-with-4-7-hackathon)，邀请社区用[我们最新的](https://www.anthropic.com/news/claude-opus-4-7) Opus 模型来构建项目。与此前以 Opus 4.6 为主题的黑客松一样，我们与 Cerebral Valley 合作，选出 500 名参与者，给每人 500 美元 API 额度以及一周时间用 Claude Code 开发。随后由 Claude 团队的评委选出六名获奖者，从总额 10 万美元的 Claude API 额度奖金池中发放，用于项目开发。

我们 Opus 4.6 黑客松——本系列的第一场——的获奖者包括一位人身伤害律师、一位心脏病专家、一位道路与基础设施专家、一位电子音乐人，以及一位职业软件工程师。他们攻克的项目分别改善住房、医疗、基础设施、音乐和教育。五位获奖者中有四位并非职业开发者。

我们希望他们的项目能启发你去构建一些有意义的东西。

## 第一名：[CrossBeam](https://www.youtube.com/watch?v=jHwBkFSvyk0)，Mike Brown

![](https://assets.claude.com/5a143f0d2f4b5b67b3432a95daafeddec3940ab4.png)

图片由 Mike Brown 提供。

加州住房许可首次提交的驳回率超过 90%，平均延误六个月，让房主多花 3 万美元。多数时候问题出在官僚流程上：缺少签名、法规引用编号写错、表格没填全。

“所有人都以为加州有住房危机。我们没有。我们有许可危机，”人身伤害律师 Mike Brown 说。拿到建造一栋新住宅所需的许可，耗时可能比施工本身还长。Mike 的黑客松项目 [CrossBeam](https://github.com/mikeOnBreeze/cc-crossbeam) 用 AI 帮助打通加州的许可瓶颈。

有了 CrossBeam，建筑商把图纸和补正函拖拽进工具；并行子智能体解析这些文档，构建空间索引，并为每一条具体整改项分派专门的智能体。二十分钟后，建筑商就得到一份精确的审批行动计划。在办公桌的另一侧，CrossBeam 让市政部门能够批量处理已提交的许可，并自动生成补正函草稿。

南加州的 Buena Park 市需要在 2029 年前为超过 8,900 套住房发放许可，但 2024 年只批了约 120 套；该市正考虑采用 CrossBeam 来加速许可流程，不仅为建筑商提速，也为那些要审核成堆文书的行政人员提速。

“如果我们能同时解决加州许可危机的两端，”Mike 说，“也许就真的能解决加州的住房危机。”

Mike 构建 CrossBeam 的工作流是：提示 Claude Code，然后让 Claude 来写测试。“我觉得不可思议的是，我居然赢了这个比赛，而我没有写一行代码，”他说。“我甚至没读过一行代码。”

[*在 GitHub 上查看 CrossBeam。*](https://github.com/mikeOnBreeze/cc-crossbeam)

## 第二名：[Elisa](https://www.youtube.com/watch?v=rsUaz_QAK6o)，Jon McBee

![](https://assets.claude.com/7d139f0e8510d01ec5bb43ecce365c3eccb70150.png)

图片由 Jon McBee 提供。

当 Jon McBee 12 岁的女儿要为七年级科学展项目给微控制器编程时，他希望她能用到自己作为软件工程师每天都用的工具：Claude Code。但终端界面并不是为初中生设计的——于是他做了一个适合她的。

Elisa 是一个基于积木的图形化集成开发环境（IDE），用户通过把原语（目标、需求、智能体、技能、规则、门户、部署）拼在一起设计软件，而 AI 在背后写真正的代码。用户用可视化语言写出规格说明，一个元规划器（meta-planner）把它分解为任务图，智能体负责其余部分。内置的教学引擎会给出适合年龄的编程概念讲解，把每一次构建都变成一堂课。Jon 的女儿用它把代码烧录到微控制器上完成了项目，一行代码都没写。

借助 Claude Code，Jon 用 30 小时构建了 Elisa，完成 76 次提交、超过 39,000 行代码和超过 1,500 个测试。“我懂系统架构。我懂如何集成硬件。我懂如何定义和测试软件，”他说。“Claude Code 帮我把所有这些知识在短短六天内变成了可交付的产品。”

教育工作者已经联系他，希望能在课堂上使用 Elisa，Jon 正用第二名获得的 3 万美元 Claude API 额度来资助这项工作。他相信软件创造者很快将完全不再编写源代码，而是与定义良好的测试和规格说明协作。*Elisa* 把这一想法包裹在一个适合孩子的可视化界面里。“我用我女儿的名字命名了这个项目，”Jon 说，“因为她正是它要服务的人。”

[*在 GitHub 上查看 Elisa。*](https://github.com/zoidbergclawd/elisa)

## 第三名：[PostVisit.ai](https://youtu.be/V29UCOii2jE)，Michał Nedoszytko

![](https://assets.claude.com/79a591324775739d926f39cee607e629591d6005.png)

图片由 Michał Nedoszytko 提供。

Michał Nedoszytko 是常驻布鲁塞尔的心脏病专家，二十年来在行医之余构建医疗软件。他上一个项目 Previsit.AI 是一套 AI 患者预诊系统，已在比利时、希腊和波兰部署。但他过去两年真正想做的产品是它的对应物：就诊之后会发生什么。“我在导管室里做过成千上万台手术，”他说。“但真正的挣扎发生在你离开诊室的那一刻。”

PostVisit 是一套工具，用通俗语言解释诊断，分析就诊记录和 AI 记录员的转录文本，并在医生监督下从科学资源与完整健康档案中找出相关临床证据。患者能更清楚地了解自己的诊疗情况，医生也能看到患者在两次就诊之间过得如何。这款助手围绕隐私、安全和临床最佳实践来构建。

为了构建 PostVisit，Michał 给自己安排了一场黑客松公路旅行，从布鲁塞尔开往旧金山的路上边开边做。“路上是我最好的想法诞生的地方，”他说。一周、几千英里之后，他得到了自己构思多年的产品。“医学建立在证据之上，”他说。“而现在，通过把健康档案、证据和就诊数据结合起来，患者可以完全掌控并理解就诊之后发生的一切。”

[*在 postvisit.ai 了解更多。*](http://postvisit.ai)

## “Keep Thinking”奖：[TARA](https://www.youtube.com/watch?v=GFCrXehS1DE)，Kyeyune Kazibwe

![](https://assets.claude.com/6c77dfdbad08af540301b88d02a4bab7b44476e7.png)

图片由 Kyeyune Kazibwe 提供。

乌干达的道路基础设施需求远远超过可用预算，而传统的可行性研究帮不上忙：它们耗资 100 万至 400 万美元、耗时 9 到 14 个月，且只关注经济预测，不考虑道路本应服务的社区。当时在乌干达工程与交通部工作的 Kyeyune Kazibwe 构建了 TARA，想改变这些决策的产生方式。

TARA 把行车记录仪拍摄的道路影像转化为一份完整的投资评估。该工具利用 Opus 4.6 的视觉能力分析每一帧，识别路面状况、病害模式和路侧活动，包括行人、骑行者以及路边摊位。系统把道路切分为不同的状况路段，自动填充干预成本，并生成完整的经济评估，包括净现值（NPV）、现金流预测和敏感性分析。它还会给出公平性评分，评估投资的实际受益者是谁，并把沿途发现的临近设施与高度关注区域纳入考量。

为了参赛，Kyeyune 上传了乌干达正在建设中的 Kira–Matugga 公路的真实行车记录仪影像。“点一下就能生成一份完整的 PDF 报告：状况评估、经济分析、公平性结论、敏感性解读，全在一份文档里，”他说。“这个过程过去要花几周。TARA 五个小时就能完成。”

[在 GitHub 上查看 *TARA*。](https://github.com/Kye256/tara-transport-assessment)

## 特别奖——创意探索：[Conductr](https://www.youtube.com/watch?v=X6CqJoyj0kI)，Asep Bagja Priandana

![](https://assets.claude.com/8b6036fa13566bea22b3a97efdc826406cdf3e5f.jpg)

图片由 Asep Bagja Priandana 提供。

Asep Bagja Priandana 构建 Conductr，是为了把 Claude 变成一个实时虚拟乐队成员。这款基于浏览器的 MIDI 乐器会聆听你在控制器上弹奏和弦，分析你的演奏，并实时生成四条轨道——鼓、贝斯、旋律与和声。输入*“make it funky”*或*“build to a climax”*，编曲就会在即兴中随之变化。

他说，技术上的挑战在于让音乐不中断。一个编译为 WebAssembly 的 C 引擎每 15 毫秒生成音符，因此 AI 的决策能在不打断流动的情况下重塑编曲。用 Asep 的话说，延迟“在音乐上不可察觉”。

Conductr 运行在约 4,800 行 JavaScript 和 WebAssembly 代码上：对一件能实时聆听、思考并与你同奏的乐器来说，这算是相当精简的构建。

[*在 GitHub 上查看 Conductr。*](https://github.com/nanassound/conductr)

敬请期待 Built with Opus 4.7 黑客松获奖者的更新。

***[了解](http://claude.com/community)我们的 Claude 社区项目，包括聚会、黑客松等更多内容。***

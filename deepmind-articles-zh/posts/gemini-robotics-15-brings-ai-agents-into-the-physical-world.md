---
title: "Gemini Robotics 1.5 把 AI 智能体带入物理世界"
title_en: "Gemini Robotics 1.5 brings AI agents into the physical world"
source: https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/
site: deepmind
date: 2025-09-25
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Robotics 1.5 把 AI 智能体带入物理世界

> 原文：[Gemini Robotics 1.5 brings AI agents into the physical world](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/) · Google DeepMind

我们正在开启一个物理智能体的时代——让机器人能够感知、规划、思考、使用工具并采取行动，从而更好地完成复杂的多步骤任务。

今年早些时候，我们把 [Gemini](https://deepmind.google/models/gemini/) 的多模态理解能力带入物理世界，取得了令人瞩目的进展，起点就是 [Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/) 模型家族。

今天，我们朝着打造智能的、真正通用的机器人又迈出一步。我们推出两个模型，借助先进的思考能力解锁智能体化（agentic）体验：

- [**Gemini Robotics 1.5**](https://deepmind.google/models/gemini-robotics/gemini-robotics/) – 我们能力最强的视觉-语言-动作（VLA）模型，将视觉信息和指令转化为机器人的运动指令以执行任务。这个模型会在行动前先思考并展示其思考过程，帮助机器人以更透明的方式评估并完成复杂任务。它还能跨本体（embodiment）学习，加速技能习得。
- [**Gemini Robotics-ER 1.5**](https://deepmind.google/models/gemini-robotics/gemini-robotics-er/) – 我们能力最强的视觉-语言模型（VLM），可以对物理世界进行推理、原生调用数字工具，并制定完成任务使命的详细多步骤计划。该模型目前在多项空间理解基准测试中达到业界领先水平。

这些进展将帮助开发者构建能力更强、更加多才多艺的机器人，使其能够主动理解自身环境，以通用的方式完成复杂的多步骤任务。

从今天起，我们通过 [Google AI Studio](https://aistudio.google.com/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=/) 中的 Gemini API 向开发者开放 Gemini Robotics-ER 1.5。Gemini Robotics 1.5 目前面向部分精选合作伙伴提供。更多关于构建下一代物理智能体的内容，请参阅[开发者博客](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-1-5/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=/)。

## Gemini Robotics 1.5：为物理任务解锁智能体化体验

大多数日常任务都需要结合情境信息、经历多个步骤才能完成，这对如今的机器人来说出了名地困难。

例如，如果要求机器人「根据我所在的位置，把这些物品分类投进正确的堆肥、回收和垃圾桶」，它需要在互联网上搜索当地的垃圾分类指南，查看面前的物品并根据这些规则弄清楚如何分类——然后再执行把物品投放到位所需的全部步骤。因此，为了帮助机器人完成这类复杂的多步骤任务，我们设计了两个在一个智能体化框架中协同工作的模型。

我们的具身推理模型 Gemini Robotics-ER 1.5 充当机器人的高层「大脑」，负责编排机器人的各项活动。这个模型擅长在物理环境中进行规划和逻辑决策，具备业界领先的空间理解能力，能用自然语言交互，评估自己的成功概率和任务进度，并且可以原生调用 [Google Search](https://search.google/intl/en-GB/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=/) 等工具查找信息，或使用任意第三方用户自定义函数。

随后，Gemini Robotics-ER 1.5 会给 Gemini Robotics 1.5 下达每一步的自然语言指令，后者利用其视觉与语言理解能力直接执行具体动作。Gemini Robotics 1.5 还帮助机器人思考自身的动作，以更好地完成语义复杂的任务，甚至能用自然语言解释自己的思考过程——使其决策更加透明。

![一幅示意图，说明 Gemini Robotics 1.5 智能体化系统：高层编排器 Gemini Robotics-ER 1.5 通过思考、工具使用和规划，引导 Gemini Robotics 1.5 VLA 模型执行垃圾分类任务。](https://lh3.googleusercontent.com/vSMY895gzWpK-nGK2Vn__6OsjX5DIlTkiBBqggd0f-oAw1oNgh5tFPiZPKtSKIONx4UCT7kiop72Nuj0RMrJ-bICxx21SZCG55LlqcqBA-n_znJw=w1440)

示意图展示我们的具身推理模型 Gemini Robotics-ER 1.5 与视觉-语言-动作模型 Gemini Robotics 1.5 如何主动协同，在物理世界完成复杂任务。

这两个模型都构建于 Gemini 核心模型家族之上，并用不同的数据集微调，从而分别专注于各自的角色。二者结合后，提升了机器人向更长任务和更多样环境泛化的能力。

![](https://lh3.googleusercontent.com/sdFcpCoe-jJQIx2Ay8OzvMoz0WHXK0wJ0fa9WNG2JzqmGEfBH8d60a5YUlWQkJ9wlMfbJEAJ6wphjI9jAlaZcE9BTIEpInPQowHpvGMHZe9Ui8qiGQ=w1440-h810-n-nu)

### 理解自身环境

Gemini Robotics-ER 1.5 是第一个针对具身推理优化的思考模型。它在学术基准和内部基准上都取得了业界领先的表现，这些基准的灵感来自我们可信测试者计划中的真实用例。

我们在 15 个学术基准上评测了 Gemini Robotics-ER 1.5，包括[具身推理问答](https://github.com/embodiedreasoning/ERQA)（ERQA）和 [Point-Bench](https://pointarena.github.io/)，衡量模型在指认（pointing）、图像问答和视频问答上的表现。

详情见[我们的技术报告](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-1-5-Tech-Report.pdf)。

![柱状图展示 15 项学术具身推理基准上的汇总成绩，以蓝色高亮的 Gemini Robotics-ER 1.5 取得超过 60 的最高分，其后依次是 GPT-5、GPT-5-mini、Gemini Robotics-ER 1.0 和 GPT-5-Nano。](https://lh3.googleusercontent.com/iGOPSXl7VFgFdMJW9V7dCfa8ngGLwHmaIOL9bDgrQMULRVVIku-ukMdcdRl0XVZPLnhpJLdkayLARFTDkoSwkyEgXi5s35vcMDRtnwLuf0oyx3Xqyg=w1440)

柱状图展示 Gemini Robotics-ER 1.5 与同类模型相比的业界领先成绩。我们的模型在 15 项学术具身推理基准上取得了最高的汇总成绩，这些基准包括 Point-Bench、RefSpatial、RoboSpatial-Pointing、Where2Place、BLINK、CV-Bench、ERQA、EmbSpatial、MindCube、RoboSpatial-VQA、SAT、Cosmos-Reason1、Min Video Pairs、OpenEQA 和 VSI-Bench。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持视频标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

一组 GIF 拼贴，展示 Gemini Robotics-ER 1.5 的部分能力，包括物体检测与状态估计、分割掩码、指认、轨迹预测、任务进度估计与成功检测。

## 三思而后行

视觉-语言-动作模型传统上是把指令或语言计划直接翻译成机器人的动作。而 Gemini Robotics 1.5 不再只是简单地翻译指令或计划，它现在可以三思而后行。这意味着它能够以自然语言生成内部的推理与分析序列，来执行需要多个步骤或更深语义理解的任务。

例如，在完成「按颜色整理我的衣物」这类任务时，下方视频中的机器人会在不同层级上思考。首先，它理解按颜色整理意味着把白色衣物放进白色收纳箱、其他颜色放进黑色收纳箱。然后它思考要采取的步骤，比如拿起红色毛衣并放进黑色收纳箱，还会思考所涉及的精细动作，比如把毛衣挪近一些以便更容易抓起。

![](https://lh3.googleusercontent.com/z1XbNpE9I8GVhHf9jWsER5fFXj0TVWgsRE42CnYTInCMt2x83RvAbGtUJ46gBeg57mSLFQi3XBUT8Rt7bo7kKAV-hhOmM7-oBeV4wyGro6UXvL--85Y=w1440-h810-n-nu)

在这一多层级思考过程中，视觉-语言-动作模型可以决定把较长的任务拆分为机器人能够成功执行的更简单的短片段。这也有助于模型向新任务泛化，并在环境变化时表现得更稳健。

## 跨本体学习

机器人的形状和大小各异，感知能力和自由度也不同，这使得把一台机器人上学会的动作迁移到另一台上非常困难。

Gemini Robotics 1.5 展现出卓越的跨本体学习能力。它可以把从一台机器人学到的动作迁移到另一台上，而无需针对每个新本体专门定制模型。这一突破加速了新行为的学习，让机器人变得更聪明、更有用。

例如，我们观察到仅在 [ALOHA 2](https://aloha-2.github.io/) 机器人上训练过的任务，也能直接在 Apptronik 的人形机器人 [Apollo](https://apptronik.com/apollo) 和双臂 [Franka](https://franka.de/franka-research-3-arm) 机器人上完成，反之亦然。

![](https://lh3.googleusercontent.com/vHo1vRQXDOOR3movvDNdiYIBH5xfw3gxknu3Q9XE1TYtFJCiCxF_6FdgiQoSiMmNqQJOn01aD4ySoMuio2rzI49xqS_q-8828m7oJ5KzA5IvhJDBEr8=w1440-h810-n-nu)

## 我们如何负责任地推进 AI 与机器人技术

在释放具身 AI 全部潜力的同时，我们正在主动开发新颖的安全与对齐方法，让智能体化 AI 机器人能够负责任地部署在以人为中心的环境中。

我们的责任与安全委员会（RSC）和负责任开发与创新（ReDI）团队与机器人团队协作，确保这些模型的开发符合我们的 [AI 原则](https://ai.google/principles/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)。

Gemini Robotics 1.5 通过高层语义推理实现了整体性的安全方法，包括在行动前先思考安全问题，通过与现有 [Gemini 安全政策](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf)保持一致来确保与人类对话的尊重得体，并在必要时触发机器人机载的低层安全子系统（例如碰撞规避）。

为指引 Gemini Robotics 模型的安全开发，我们还在发布 [ASIMOV 基准](http://asimov-benchmark.github.io/v2)的升级版——一套用于评估和改进语义安全的综合性数据集合，具备更好的长尾覆盖、更完善的标注、新的安全问题类型和新的视频模态。

在针对 [ASIMOV 基准](http://asimov-benchmark.github.io/v2)的安全评测中，Gemini Robotics-ER 1.5 展现出业界领先的表现，其思考能力显著促进了对语义安全的更好理解，以及对物理安全约束的更好遵守。

更多安全研究内容请见[我们的技术报告](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-1-5-Tech-Report.pdf)，或访问[我们的安全网站](https://deepmind.google/models/gemini-robotics/responsibly-advancing-ai-and-robotics/)。

## 迈向解决物理世界中 AGI 的里程碑

Gemini Robotics 1.5 是解决物理世界中通用人工智能（AGI）的重要里程碑。通过引入智能体化能力，我们正在超越只会响应指令的模型，打造能够真正推理、规划、主动使用工具并泛化的系统。

这是构建机器人的一个基础性步骤：让它们以智能与灵巧驾驭物理世界的复杂性，并最终变得更有帮助、更好地融入我们的生活。

我们期待与更广泛的研究界继续推进这项工作，也迫不及待想看到机器人社区用我们最新的 Gemini Robotics-ER 模型创造出什么。

**探索 Gemini Robotics 1.5**

[阅读技术报告](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-1-5-Tech-Report.pdf)[报名我们的可信测试者计划](https://docs.google.com/forms/d/1sM5GqcVMWv-KmKY3TOMpVtQ-lDFeAftQ-d9xQn92jCE/edit?ts=67cef986)[在开发者博客了解更多](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-1-5/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)

**致谢**本工作由 Gemini Robotics 团队开发：Abbas Abdolmaleki、Saminda Abeyruwan、Joshua Ainslie、Jean-Baptiste Alayrac、Montserrat Gonzalez Arenas、Ashwin Balakrishna、Nathan Batchelor、Alex Bewley、Jeff Bingham、Michael Bloesch、Konstantinos Bousmalis、Philemon Brakel、Anthony Brohan、Thomas Buschmann、Arunkumar Byravan、Serkan Cabi、Ken Caluwaerts、Federico Casarini、Christine Chan、Oscar Chang、London Chappellet-Volpini、Jose Enrique Chen、Xi Chen、Hao-Tien Lewis Chiang、Krzysztof Choromanski、Adrian Collister、David B. D'Ambrosio、Sudeep Dasari、Todor Davchev、Meet Kirankumar Dave、Coline Devin、Norman Di Palo、Tianli Ding、Carl Doersch、Adil Dostmohamed、Yilun Du、Debidatta Dwibedi、Sathish Thoppay Egambaram、Michael Elabd、Tom Erez、Xiaolin Fang、Claudio Fantacci、Cody Fong、Erik Frey、Chuyuan Fu、Ruiqi Gao、Marissa Giustina、Keerthana Gopalakrishnan、Laura Graesser、Oliver Groth、Agrim Gupta、Roland Hafner、Steven Hansen、Leonard Hasenclever、Sam Haves、Nicolas Heess、Brandon Hernaez、Alex Hofer、Jasmine Hsu、Lu Huang、Sandy H. Huang、Atil Iscen、Mithun George Jacob、Deepali Jain、Sally Jesmonth、Abhishek Jindal、Ryan Julian、Dmitry Kalashnikov、Stefani Karp、Matija Kecman、J. Chase Kew、Donnie Kim、Frank Kim、Junkyung Kim、Thomas Kipf、Sean Kirmani、Ksenia Konyushkova、Yuheng Kuang、Thomas Lampe、Antoine Laurens、Tuan Anh Le、Isabel Leal、Alex X. Lee、Tsang-Wei Edward Lee、Guy Lever、Jacky Liang、Li-Heng Lin、Fangchen Liu、Shangbang Long、Caden Lu、Sharath Maddineni、Anirudha Majumdar、Kevis-Kokitsi Maninis、Andrew Marmon、Sergio Martinez、Assaf Hurwitz Michaely、Niko Milonopoulos、Joss Moore、Robert Moreno、Michael Neunert、Francesco Nori、Joy Ortiz、Kenneth Oslund、Carolina Parada、Emilio Parisotto、Peter Pastor Sampedro、Acorn Pooley、Thomas Power、Alessio Quaglino、Haroon Qureshi、Rajkumar Vasudeva Raju、Helen Ran、Dushyant Rao、Kanishka Rao、Isaac Reid、David Rendleman、Krista Reymann、Miguel Rivas、Francesco Romano、Yulia Rubanova、Pannag R Sanketi、Dhruv Shah、Mohit Sharma、Kathryn Shea、Mohit Shridhar、Charles Shu、Vikas Sindhwani、Sumeet Singh、Radu Soricut、Rachel Sterneck、Ian Storz、Razvan Surdulescu、Jie Tan、Jonathan Tompson、Saran Tunyasuvunakool、Jake Varley、Grace Vesom、Giulia Vezzani、Maria Bauza Villalonga、Oriol Vinyals、René Wagner、Ayzaan Wahid、Stefan Welker、Paul Wohlhart、Chengda Wu、Markus Wulfmeier、Fei Xia、Ted Xiao、Annie Xie、Jinyu Xie、Peng Xu、Sichun Xu、Ying Xu、Zhuo Xu、Jimmy Yan、Sherry Yang、Skye Yang、Yuxiang Yang、Hiu Hong Yu、Wenhao Yu、Li Yang Ku、Wentao Yuan、Yuan Yuan、Jingwei Zhang、Tingnan Zhang、Zhiyuan Zhang、Allan Zhou、Guangyao Zhou 和 Yuxiang Zhou。

我们还要感谢：Amy Nommeots-Nomm、Ashley Gibb、Bhavya Sukhija、Bryan Gale、Catarina Barros、Christy Koh、Clara Barbu、Demetra Brady、Hiroki Furuta、Jennie Lees、Kendra Byrne、Keran Rong、Kevin Murphy、Kieran Connell、Kuang-Huei Lee、M. Emre Karagozler、Martina Zambelli、Matthew Jackson、Michael Noseworthy、Miguel Lázaro-Gredilla、Mili Sanwalka、Mimi Jasarevic、Nimrod Gileadi、Rebeca Santamaria-Fernandez、Rui Yao、Siobhan Mcloughlin、Sophie Bridgers、Stefano Saliceti、Steven Bohez、Svetlana Grant、Tim Hertweck、Verena Rieser、Yandong Ji。

感谢以下人士对这项工作的领导与支持：Jean-Baptiste Alayrac、Zoubin Ghahramani、Koray Kavukcuoglu 和 Demis Hassabis（德米斯·哈萨比斯）。我们还要感谢 Google 和 Google DeepMind 中为此做出贡献的众多团队，包括法务、市场、传播、责任与安全委员会、负责任开发与创新、政策、战略与运营以及商务与企业发展团队。我们感谢机器人团队中未在上述名单中提及的每一位成员的持续支持与指导。最后，感谢 Apptronik 团队的支持。

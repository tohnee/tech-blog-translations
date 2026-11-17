---
title: "认识我们的 Claude Opus 4.8 Build Day 黑客松获奖者"
title_en: "Meet the winners of our Claude Opus 4.8 Build Day hackathon"
date: 2026-06-17
source: https://claude.com/resources/articles/meet-the-winners-of-our-claude-opus-4-8-build-day-hackathon
crawled: 2026-11-17
translated: 2026-11-17
---

# 认识我们的 Claude Opus 4.8 Build Day 黑客松获奖者

> 原文：[Meet the winners of our Claude Opus 4.8 Build Day hackathon](https://claude.com/resources/articles/meet-the-winners-of-our-claude-opus-4-8-build-day-hackathon) · Claude 博客

从重建唐代建筑到对一座合成的旧金山进行民意测验，来看看我们最新黑客松的获奖者如何在一天之内用 Claude Opus 4.8 做出成果。

6 月 13 日，我们把 300 多位创始人和开发者带到旧金山，参加一场为期 12 小时、使用 Claude Opus 4.8 的黑客松。共有超过 1500 人报名，310 人参加，许多人从世界各地赶来。每人获得 500 美元额度，用一天时间把一个想法变成可运行的演示。

我们采访了三支获奖团队，聊了聊他们做了什么，以及如何借助 Claude 完成。

祝贺获奖者以及所有参与者。希望他们的项目能给你带来一些自己的灵感。

## 第一名：[Tekton](https://tekton-build.vercel.app/)，Holly Tang 与 Austin Burgess

![](https://assets.claude.com/3c666bac82ecb587b4631110b797eabbd49c1187.jpg)

Holly Tang 和 Austin Burgess 构建了 Tekton——一个 3D 重建平台，让唐代建筑重获新生，且每个构件都能追溯到其历史来源。

一座历史悠久的木构建筑一旦失火，数百年的工艺可能随之消失。Tekton 以 3D 方式重建这些建筑，并让每一个构件都能追溯到有据可查的来源。

给 Tekton 一座历史建筑，Claude 会研究它，汇齐图纸、施工文献、照片和图解，然后跨越 339 个渐进建造状态组装出 3D 模型。当你点击模型中的任何构件，Tekton 会显示该细节出自何处、为何被放在那里。团队称之为"证据链"，从原始材料一直贯通到经验证的模型。他们为学术验证、修复工作和文化保护而构建了它，起点是唐代建筑和巴黎圣母院尖塔。

验证完全由 Opus 4.8 完成。独立的验证子智能体在隔离的上下文窗口中为每一次重建评分，自我修正回路则反复核对构件位置，直到 20 项测试全部通过。每一次构建都以历史记录及其引文为准绳来衡量，因此完成的模型遵循该结构最初建造时被记录下来的规则。

Holly Tang 和 Austin Burgess 是一个月前在 Code with Claude 活动上排队买咖啡时认识的。Holly 是一名设计师，一直在帮 Austin 的创业公司 [Pearl](https://joinpearl.co/)。"我很爱看纪录片，看到美丽的建筑毁于火灾总让我难过，"Holly 说。她曾独自做过一次重建的原型；Austin 的贡献是把它扩展到能端到端地作用于任何建筑。

为了构建 Tekton，两人分阶段推进：先让巴黎圣母院尖塔按比例渲染出来，再添加更精细的细节，然后扩展到结构的其余部分。整座大教堂还没做完，时间就到了。即便如此，仍有好几位黑客松参与者询问该项目，或主动提出帮忙把它做得更准确。Holly 和 Austin 希望把 Tekton 开源，让博物馆、历史学家、非营利组织和政府都能在它之上继续构建。

**给其他开发者的建议：** 在动手构建任何部分之前，先把整个项目规划清楚。

"我们做了一份完整的 PRD 和一个 Notion 看板，上面大约有 50 个工单，每个具体任务一个，"Austin 说。"差不多就是：这是端到端的完整项目，每一步我们想要的究竟是什么。"计划定好之后，他把构建拆成若干独立的工作流并行推进。

[Tekton on GitHub](https://github.com/tangxiya-star/Tekton)

## 第二名：[Sim Francisco](https://simfrancisco.org/)，Tanmayi Priya Dasari 与 Tejas Prabhune

![](https://assets.claude.com/56b34ef44f1ec5e2c5e9be8576b0a3e725d14973.jpg)

Tanmayi Priya Dasari 和 Tejas Prabhune 构建了 Sim Francisco——一个以美国人口普查数据为种子生成的旧金山人口数字孪生，能在几秒钟内对一座合成城市进行民意调查，并预测现实世界的结果。

Sim Francisco 是一个可运行的旧金山人口模型。它包含 1 万名取自美国人口普查数据的合成居民，每个人都有自己的统计特征、个人经历和世界观，被放置在城市地图上，并实时对新闻做出反应。

向这座城市提一个问题，它就会逐个街区地对整个合成选民群体进行民意测验。在知识截止日期为 2023 年 10 月的模型上运行，它预测 2024 年总统大选中民主党得票率为 81.3%（实际为 83.8%），预测旧金山 2024 年 3 月的 A 提案支持率为 70%（实际为 70.38%）。它与 Kalshi、Polymarket 等预测市场的差距在几个百分点以内。\*

整个前端和后端都由 Opus 4.8 编写，并对后端行为做了端到端验证。为了验证模型的工作，团队让 Claude 与一个验证者和一个对抗性智能体协同工作，构建出能复现该城市真实人口分布的后端。

Tanmayi Priya Dasari 和 Tejas Prabhune 是加州大学伯克利分校电气工程与计算机科学专业的学生，两人在校内机器学习社团相识。对 Tejas 来说，Sim Francisco 还是他正在创办的后训练（post-training）公司的一次测试——他正借此研究模拟人格能否保持足够的一致性，以用于长程任务的模型训练。

**给其他开发者的建议：** 不要满足于第一个能跑通的方案，尤其是当它很昂贵的时候。

团队的第一版为 1 万名居民每人发起一次单独的推理调用，成本很快变得很高。"后来，Claude 运行了它自己创造的进化聚类算法，"Tejas 说，把居民归并为约 300 个有代表性的人格。分组后的版本在对 Kalshi、Polymarket 的预测和历史结果上保持了同样的准确度，同时把推理成本降低了 10 到 100 倍。

[*Sim Francisco on GitHub*](https://github.com/tejasprabhune/simfrancisco)

## 第三名：[Custom Universe](https://www.luminal.com/realtime-edit-demo)，Jake Stevens 与 Mauricio Pereira

![](https://assets.claude.com/e947d47d13907775c8984835415d1d442221aca0.jpg)

Jake Stevens 和 Mauricio Pereira 构建了 Custom Universe——一个实时引擎，能把一张手机照片变成完全可编辑、照片级真实的 3D 场景。

用手机拍一张椅子的照片，Custom Universe 就会把它变成一个 3D 物体：你可以把它放进场景、用文本提示改变风格、四处移动，而渲染画面会实时更新。

这个项目面向机器人实验室：它们需要大量合成数据来针对特定任务和场景训练机器人。实验室可以从工厂车间扫描一台机器，把它放进场景，然后生成数据来为那个确切环境微调机器人模型。搭出这类环境通常意味着要雇物理学家和工程师来处理物理与碰撞几何。Custom Universe 则让你通过拖动物体来布置场景，团队还计划加入精确摆放功能，比如把某个物体在厨房台面上挪动 30 厘米。

Opus 4.8 端到端地构建了这个项目，并在整场黑客松期间操作运行模型的远程 NVIDIA H100。团队还用 Claude 来判断哪些模型能产出正确的结果，并搭建了把用 Apple RealityKit 采集的手机扫描物体导入 Web 应用的流水线。

Jake Stevens 和 Mauricio Pereira 是在活动上认识的。Jake 毕业于罗切斯特理工学院（RIT）计算机视觉专业，经营着 [Luminal](https://www.luminal.com/)——一家专注于加速 AI 模型的创业公司；这个场景构建器最初只是他一直想尝试的副业项目。Mauricio 毕业于 MIT 机器人专业，经营着 [Coat Robotics](https://www.coatrobotics.com/)，他带来的是自己深有体会的问题：机器人领域仍然缺少训练数据，而构建合成环境很难。Custom Universe 依赖开源模型和算法，可免费使用；团队表示用户可以在自己的 GPU 上运行它。

**给其他开发者的建议：** 用 Claude 来挑选工具，而不只是写代码。

"很多迭代都是在看哪个模型能给出正确的输出，所以我们让 Claude 做了大量调研，"Mauricio 说。团队还把不熟悉的技术交给 Claude 去集成。"比如 Apple RealityKit，以及我们要如何确保人们能把自己扫描的物体输入到我们的网站。我们跟 Claude 说：把这个加进流水线。"

[*Custom Universe on GitHub*](https://github.com/jss8649/image-edit-realtime-hackathon)

*[了解](http://claude.com/community)我们的 Claude 社区项目，包括聚会、黑客松等。*

*\*Sim Francisco 是一个独立的黑客松项目，它只是把预测选举结果当作一个示例。这并不代表 Anthropic 认可把 AI 模拟的选举预测作为一种用例。*

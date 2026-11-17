---
title: "认识 Built with Opus 4.7 Claude Code 黑客松的获奖者"
title_en: "Meet the winners of the Built with Opus 4.7 Claude Code hackathon"
date: 2026-06-15
source: https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon
crawled: 2026-11-17
translated: 2026-11-17
---

# 认识 Built with Opus 4.7 Claude Code 黑客松的获奖者

> 原文：[Meet the winners of the Built with Opus 4.7 Claude Code hackathon](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon) · Claude 博客

*从医疗培训、电子设备维修，到编程教育与工厂维护，来看看我们最新一期线上黑客松的获奖者打造了哪些项目。*

上周，我们举办了 [Claude Build Day](https://cerebralvalley.ai/e/claude-startups-build-day)，这是我们的最新一期黑客松，开发者们齐聚旧金山，用 Claude Opus 4.8 把想法付诸实践。

在等待他们作品出炉的同时，我们与 Built with Opus 4.7 黑客松的获奖者聊了聊他们的项目。他们涉及的领域包括医疗培训、电子维修、计算机科学教育、互动娱乐、家庭维修和工厂维护。

恭喜所有获奖者，也感谢每一位参与者！希望他们的想法能给你带来启发。

## 第一名：[Medkit](https://bedirhankeskin.com/)，Bedirhan Keskin

Bedirhan Keskin 是伊斯坦布尔的一位医生，后来转行做了软件工程师。他用 Claude 托管智能体（Claude Managed Agents）打造了 Medkit：一款面向住院医师或初级医生的学习工具，在游戏化的诊所场景中模拟真实的患者接诊。

“当你独自一人在急诊室，外面还有 50 位患者在等待，而你意识到有些病例你在医学院从未练习过——结果你只能在真实患者身上实时练习，”Bedirhan 说。

借助 Medkit，医学生练习对模拟患者进行诊断和治疗，用这款工具采集病史、开具化验、阅片、下诊断并开具处方。接诊结束后，一个智能体评分器会按照与执业考试考官相同的公开临床指南，对整个接诊过程进行评估。

Bedirhan 把 Medkit 拆在四个独立的 Claude Code 会话中构建（语音引擎、内容生成、3D 游戏层和核心应用），保持每个上下文干净，并让四部分同时推进。他采用“说，不要打字”的方式，几乎完全靠语音工作。

Medkit 已经开始获得关注：三家医学院和一家制药公司（均位于伊斯坦布尔）将在未来几周内启动试点。

**给其他开发者的建议：** 把 Claude 当作思考伙伴，而不只是一个编码智能体。

Bedirhan 最初的想法是自托管语音引擎，但 Claude 建议使用云服务商以加快进度。“我最看重 Claude 的一点是，它不只是代码生成器，而是一个思考伙伴，帮我看到那些我本来会错过的选项，”他说。

[*GitHub 上的 Medkit*](https://github.com/bedriyan/medkit-app)

## 第二名：[Wrench Board](https://wrenchboard.cloud/)，Alexis Chapellier

来自法国 Reignier-Ésery 的 Alexis Chapellier 在创办 [RepairMind](https://repairmind.io/)（一个面向维修店的 AI 驱动管理平台）之前，做了多年电子维修。他在本次黑客松中提交的 Opus 4.7 项目 [Wrench Board](https://wrenchboard.cloud/)，帮助独立技师攻克复杂维修。用户上传电路图和 boardview（板级视图）并描述故障现象，智能体便会构建一张统一的电气图，在图上推理，指出应当探测的那个具体焊盘，读取测量值，并不断更新假设，直到定位问题。

Alexis 在 Claude Design 中为 Wrench Board 做原型，把应用的职责拆分开（设计、电路图解析、boardview、诊断智能体），并为每一部分先生成规格说明、再生成计划。他在 Claude Code 的多智能体模式下实现，每一步都做基准测试——调试时并行运行五六个智能体，每个领域配一个专属智能体。

Alexis 最大的赌注押在 Opus 4.7 理解可视化电路图的新能力上；他说，当他让模型追踪一块主板上的供电通路时，就知道这条路走通了。

“我看着 Wrench Board 的 boardview 一步步亮起来，箭头出现，元件被逐一指出，名称浮现出来。那一刻我明白，这个想法站得住，”他说。

Wrench Board 的下一阶段是建立一个社区：既有愿意试用这款应用的电子维修从业者，也有能用实战经验丰富这款工具的专家。他的 Claude 额度将用于 RepairMind、这些首批用户，以及目前在推进中的所有基础设施。

“这次黑客松证明，一个从维修店走出来的自学成才者，可以在五天内交付一套雄心勃勃的系统，”Alexis 说。参赛时他正在申请“糊口工作”（survival jobs）。“Claude Code 放大的是那些有想法、并且有耐力把它执行出来的人，无论他们的起点在哪里。”

**给其他开发者的建议：** 在头脑风暴中深入下去，并敢于反驳模型。

Alexis 使用 [Superpowers](https://claude.com/plugins/superpowers)，这是一个集成在 Claude 中的技能框架，用来组织“先头脑风暴、后制定计划”的流程，有时他会并行进行多场头脑风暴，在不同方向上同时推进。他从 Claude Design 开始，然后用内置的直接共享项目按钮交给 Claude Code，并在模型说“不行”时继续施压。

“黑客松期间，Claude 好几次告诉我这个或那个在可用时间内做不完。实际上我时间很充裕，”他说。“你得知道怎么告诉它：*我还是要试。*”

[*GitHub 上的 Wrench Board*](https://github.com/Junkz3/wrench-board)

## 第三名：[Maieutic](https://maieutic.dev/)，Paula Vásquez-Henríquez

Paula Vásquez-Henríquez 在智利康塞普西翁的发展大学（Universidad del Desarrollo）教授计算机科学。她说，过去两年里，她看到越来越多学生通过了考试，却不理解自己写的代码。

“现在的学生用 AI 批量制造代码，却完全不知道代码在做什么，”她说。“他们从没学会精确地陈述一个问题，没学会在写代码前先拟一份计划，也没学会批判性地阅读自己的代码、发现哪里偏离了原本的意图。自动补全在他们还没把问题想清楚之前就把能跑的代码递了上来，于是那个元认知回路——那种‘思考自己的思考’、真正造就一名程序员的过程——始终没有闭合。他们毕业时能生成代码，却无法对代码进行推理。”

Paula 目前正在攻读人工智能博士学位，研究方向是学生与 AI 的交互模式。她参加这次黑客松，是想从学生和教师两个视角解决这个问题。

Maieutic 是一款 IDE，目的是让学生在关键节点慢下来。学生必须先用自己的话描述程序应该做什么，然后才能写任何代码；Claude 会提出有针对性的澄清问题，并在规格说明详细到“一个有能力的程序员无需猜测就能实现”之前，一直锁定编辑器。

之后学生可以开始写 Python，但自动补全是关闭的；聊天面板会直接回答查证类问题，但对推理类问题则以反问来回应，而不是给出修改，拒绝替学生思考。

工具的核心是“意图差异审查”（Intent-Diff Review）：Claude 把规格说明与最终代码做对比，将每一处分歧归类为偏离（drift）、修订（revision）或缺陷（bug），然后提出一个中立、不带指责的问题，引导学生自己解释问题所在。

对教师来说，一个实时仪表盘按每名学生一行展示，并配一句认知总结（例如“写了三遍规格说明，仍然没有考虑空输入”）。教师可以点击单个学生，查看该学生与 Claude 的具体交互；系统还会分析整个班级，找出并呈现全班共有的理解偏差，方便教师补上这个缺口。

黑客松结束后，休斯顿大学的研究人员联系她，希望合作撰写论文；Paula 正把奖金额度投入到工具的进一步开发中。她说，黑客松那一周让她看到：从理解一个问题到为它交付一款工具，这中间的鸿沟已经消失。

“我是智利康塞普西翁的一名教育工作者，不在硅谷，”她说。“我在一周内交付了一个可用的全栈产品，因为工具让我可以待在自己真正擅长的角色上，其余的事由它们处理。最贴近真实问题的人，现在可以直接为这些问题造工具了。”

**给其他开发者的建议：** 先想清楚，再动手。

这个项目本身就是 Paula 在践行自己的理念：先写规格，再动手构建。“Maieutic 之所以存在，是因为学生会直接跳到代码；而我能把它做好的唯一方式，就是拒绝自己也这么做，”她说。她花了两天纯粹做思考工作，在写下第一行代码之前先完成了设计规格和技术规格。

“那两天写规格，当时感觉挺慢的——黑客松里有实实在在的压力催你立刻开始交付——但正是那两天让接下来一周跑得很快，”她说。

## 最具创意的 Opus 4.7 用法：Virtual Puppet Theater，Rene Hangstrup Møller

全栈开发者 Rene Hangstrup Møller 对 Opus 4.7 的空间推理能力很感兴趣，于是打造了 Virtual Puppet Theater：一款基于浏览器的应用，把摄像头画面和语音变成一场动态的互动木偶戏。一个实时动画木偶会模仿用户的动作，另一个由 AI 驱动的同伴木偶则与用户斗嘴；语音指令可以即时变换布景、生成 3D 道具。

Rene 在整条流水线上都用了 Claude：概念讨论、规划和代码编写，而他负责导演、架构、评审和决策。应用基于 Bun、Vite 和 TypeScript，使用 MediaPipe 手部追踪（运行在 WASM 中）和 Three.js 以 60 fps 渲染 3D 木偶舞台。一个小型 WebSocket 服务器通过 Anthropic SDK 连接 Claude Opus 4.7，驱动 AI 木偶的对话并即时生成 3D 道具；语音输入由 Web Speech API 处理，输出使用 ElevenLabs（并以浏览器语音合成为备选）。Opus 的空间推理能力通过基于截图的反馈回路不断打磨，负责视觉输出。

Virtual Puppet Theater 除了开放式玩耍之外没有其他目标，Rene 说，对这个获奖项目她并没有产品化计划。对他而言，重要的是学习和乐趣。“我拿它和我最小的儿子一起试，他玩疯了，”Rene 说。“看着他跟木偶互动、描述场景、被回应逗得咯咯笑，这就是我唯一需要的用户验证。”

他还补充说，Virtual Puppet Theater 的源代码以 MIT 许可证在 GitHub 上公开，“如果有人想接着往下做”。

**给其他开发者的建议：** 如果你要参加黑客松，提前留出制作演示视频的时间。

“做一支 3 分钟的视频，花的时间远超你的想象，”Rene 说。他提到自己在赶黑客松截止日期时，用 Claude 和 Hyperframes 制作并剪辑了 Virtual Puppet Theater 的视频。“黑客松 Discord 里很多人都提醒过这一点，他们说得对。下次我会把最后整整一天专门留给做演示。”

[*GitHub 上的 Virtual Puppet Theater*](https://github.com/rhmoller/virtual-puppet-theater)

## “Keep Thinking” 奖：[MaestrIA](https://www.youtube.com/watch?v=rkH4AjoTL5Q)，Benjamin Torralbo

Benjamin Torralbo 从小跟着父亲 Juan Rodrigo Torralbo 当学徒。父亲是智利奇洛埃岛（Chiloé）一位持有认证的 *Maestro Mayor* 木匠。“我父亲有 30 年手艺，修复过联合国教科文组织列入名录的教堂，但在智利的体系里依然是隐形人，就像其他几十万技术工人一样，”Benjamin 说。“而另一方面，需要修房子的人不知道自己家出了什么问题、要花多少钱、该找谁，也不知道自己有没有被乱收费。”

他的黑客松项目 [MaestrIA](https://maestriachile.cl/) 用一个 Web 应用同时解决这两端：给普通人提供大师级的家庭维修诊断，同时给熟练技工一种展示专业能力的方式。

在 MaestrIA 中，用户拍下问题部位，用语音或文字描述，并共享位置。Claude 会实时流式输出推理过程，并在照片上叠加上动态边界框，然后给出结构化诊断：哪里坏了、什么材料、严重程度 1–5 级、工程预算和时间估算。接着，一个智能体渲染出按工种筛选的附近 maestro 地图，另一个智能体则起草一条待发送的 WhatsApp 消息。

MaestrIA 的技术核心是一个 JSON 文件，注入到每一次诊断中。它包含 17 条诊断规则、7 种奇洛埃本地木材、16 个当地行话术语、19 个基准价格，以及 9 种这门手艺的常见错误——全部提炼自 Benjamin 与父亲数小时的访谈。在没有改动系统提示的情况下，仅这一个文件就让他的评估分数提升了 7 个点（对照人类大师的判断，从 74% 提升到 81%），也让 MaestrIA 能诊断出“落叶松（alerce）木墙板上的上升潮气”，而不是笼统的“木材损坏”。

Benjamin 此前没有任何编程经验，他说自己的角色就像工地上的工头，监督 Claude 的技术执行。“在写任何功能之前，我会让 Claude Code 先设计规格、分阶段的行动计划和安全模型：针对提示注入的输入清洗、速率限制、来源校验，以及作为唯一事实来源的 Zod schema，”他说。“然后我逐个 diff 审查每个功能。”

Benjamin 希望 MaestrIA 能扩展到新建工程、五金店集成、正式预算、合同、评价和一个认证体系。最终，每个工种都会内置一位自己的 Maestro Mayor，包括木匠、建筑师、水管工、电工和泥瓦匠。

他的奖金额度将用于开发这款应用、把他父亲的公司数字化作为实际试点，以及他自身的技术成长。“Claude Code 让一个来自奇洛埃岛、没有编程经验的 20 岁年轻人，能打造出他父亲用得上的软件，还能帮到智利另外 28 万名像他父亲一样的 maestro，”他说。“它也为数百万人打开了门——他们一直有宝贵的想法，却无从实现。”

**给其他开发者的建议：** 先做评估，再做功能。

“我做的最重要的一件事，是建立了一套可审计的 9 维评估，对照 12 个真实案例，标准答案由我父亲记录，”Benjamin 说。“是那套评估——而不是我的直觉——告诉我什么有用、什么没用。如果我再参加一次黑客松，评估会是第一个 commit。”

## 最佳 Claude 托管智能体应用：[ARIA](https://www.youtube.com/watch?v=Hen24w2Jyz4&t=28s)，Idriss Benguezzou 与 Adam Hnaien

大多数工厂里都有那么一位资深技师，光听声音就知道机器快要坏了。获得“最佳 Claude 托管智能体应用”奖的项目 ARIA（Adaptive Runtime Intelligence）把一位经验丰富的维护工程师的直觉，变成了一套成本可控、可快速部署的 AI 系统：持续监控工厂设备，一旦出现异常就立即生成定制化的诊断和维修方案。

使用 ARIA，维护工程师上传厂商的 PDF，回答四个用平实语言表述的校准问题，15 分钟内工厂就完成了画像。之后，五个智能体监视实时信号。如果某个智能体检测到故障，或预测故障即将发生，它会生成一张工单，分析部件、失效模式、紧急程度、所需零件和介入时间窗口。

这个项目的两位开发者都有车间一线的工业经验，他们在黑客松的找队友 Discord 频道里认识。Idriss Benguezzou 是法国的一名工业软件工程师，拥有数据/AI 硕士学位，这个想法和它的大部分架构他已经构思了一段时间。Adam Hnaien 是一名自学成才的工程专业学生，熟悉 Claude Code 和多智能体工作流，立刻意识到 ARIA 是工业维护领域一个有价值的解决方案。

Idriss 和 Adam 把黑客松第二天一整天都用在规划上，用一块 GitHub Project 看板界定每个里程碑、issue 和验收标准，然后才写第一行代码。“我们希望从第二个里程碑（M2）开始就以 200% 的力度推进，”Adam 说。“一天的规划让我们把剩下的一周用来执行，而不是即兴发挥。”

两人估计，Claude Code 写出了约 80% 的原始代码行，而领域逻辑和设计决策由他们手工完成。Idriss 负责阈值评估、知识库 schema 和异常检测，因为用他的话说，“你没法靠提示词就知道维护技师实际在看什么”。Adam 负责 UX、视觉语言和 ARIA 的“星座”概念，因为用他的话说，“品味是提示不出来的”。

智能体基础设施由托管智能体承担。“如果没有 Claude 托管智能体，我们这一周就得用来搭建 Anthropic 已经托管好的那套基础设施：沙箱化的 Python 环境、安全执行、会话持久化、MCP 调度，”Adam 说。“而我们这一周是用来在这套基础设施之上构建产品的。这就是五天内交付 ARIA 和五周内交付 ARIA 的区别。”

黑客松结果公布后，一些正在攻克同一问题的公司联系了他们。Idriss 将把 ARIA 的智能体架构、知识库 schema 和信号流水线并入自己的工业 IoT 平台；他的额度将用于更多构建与实验。至于 Adam，他计划继续探索工业智能体 AI 方面的机会，并用 API 额度继续构建和实验。

**给其他开发者的建议：** 让 Claude 做审计。Idriss 说，在下一次动手之前，先让 Claude 找出你已完成的东西里有没有问题。“这个回路被低估了。”

[*GitHub 上的 ARIA*](https://github.com/zestones/Aria)

*[了解](http://claude.com/community)我们的 Claude Community 项目，包括聚会、黑客松等更多活动。*

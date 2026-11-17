---
title: "一位非技术项目经理如何在六周内用 Claude Code 打造并上线一款压力管理应用"
title_en: "How a non-technical project manager built and shipped a stress management app with Claude Code in six weeks"
date: 2026-05-01
source: https://claude.com/resources/articles/how-a-non-technical-project-manager-built-and-shipped-a-stress-management-app-with-claude-code-in-six-weeks
crawled: 2026-11-17
translated: 2026-11-17
---

# 一位非技术项目经理如何在六周内用 Claude Code 打造并上线一款压力管理应用

> 原文：[How a non-technical project manager built and shipped a stress management app with Claude Code in six weeks](https://claude.com/resources/articles/how-a-non-technical-project-manager-built-and-shipped-a-stress-management-app-with-claude-code-in-six-weeks) · Claude 博客

Kostiantyn Vlasenko 开始做 Respiro 时，从未写过一行代码。仅仅一个多月后，他的产品就已经上架 App Store。

*在我们的系列栏目 **第零天：创始人故事（Day zero: founder stories）** 中，我们介绍一些全球最有趣、最鼓舞人心的创业公司背后的打造者。本文的主角是 Kostiantyn Vlasenko，他是 [Claude Opus 4.6 黑客松](https://claude.com/resources/articles/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)的获奖者，也是 Respiro 的创造者。*

|  |  |
| --- | --- |
| 创始人 | Kostiantyn Vlasenko |
| 国家 | 乌克兰 |
| 创业公司 | Respiro |

在这场采访的视频通话开始前十五分钟，Kostiantyn Vlasenko 感到很紧张。他满脑子都在想自己要说些什么，以至于根本没注意到自己的焦虑——但他的手机注意到了。

“应用检测到了这一点，并提醒我，‘兄弟，你现在就可以去做一个简短的方块呼吸练习。以前方块呼吸帮你缓解过压力。’”他说。

那款应用 [Respiro](https://apps.apple.com/us/app/respiro-stress-relief/id6758023997) 正是 Vlasenko 的作品。他虽是有十年经验的项目经理，但在 2026 年 2 月决定为 [Built With Opus 4.6 Claude Code 黑客松](https://cerebralvalley.ai/e/claude-code-hackathon?tab=guest-list)做项目之前，从未交付过一行代码。一个月后，Respiro（一款基于科学方法管理压力的 iOS 应用）已在 Apple App Store 上线，拥有数百名用户，其架构中包含 15 个以上由 Vlasenko 亲手构建并编排的专用子智能体。

这一切他都用 Claude Code 完成，耗时 72 小时，没有团队，也没有编程经验。

## 没有应用能解决的问题

作为 [Mythical Games](https://mythicalgames.com/) 的项目经理，常驻基辅的 Vlasenko 十年来一直在应对来自利益相关方的压力、团队动态以及产品发布永不停歇的节奏。他发现呼吸技巧和正念练习有助于把压力水平控制在合理范围；但他始终找不到一款能在真正感到压力的当下就介入的压力管理工具。

“现有的应用会在晚上 10 点之类的时间提醒我做深呼吸。但它们不明白我*现在*就很有压力，”他解释道。这个想法在他于乌克兰西部山区度假时变得清晰：做一款能实时从个人设备中检测压力信号、并在你最需要的时刻用引导式正念呼吸练习进行干预的应用。唯一的问题是，他不知道怎么开发应用。

## 像管理人一样管理智能体

当时，Vlasenko 已经在用 Claude 自动化一些工作任务，比如更新 Jira、把会议纪要发到 Slack，并且刚开始使用 Claude Code CLI。“然后我想，好吧，我很熟悉我的团队成员是怎么用 Claude 写代码的。我为什么不能也这么做？”他说。

他很快意识到，自己的项目管理背景比编程技能更重要。“我在管理真人方面有大量经验，”他说。“我发现这其实是同一回事，只不过管理的是 IDE 里的智能体，而且我很惊讶它竟然这么容易。”

Vlasenko 开玩笑说，他的第一个提示词本质上就是*嘿 Claude，直接给我一个能让我压力小一点的应用*，但即便如此，他说最初的结果还是让他吃了一惊。“哇，这太厉害了。它不只是在脑子里，它*此刻就在*我的手机里，而且它真的能用！”

但 Vlasenko 没有就此停下。他用 Claude 研究智能体系统如何运作、哪些 Apple API 可以为他的压力检测逻辑提供数据，然后让 Claude 帮他搭建一套多智能体架构：一个 TCA 架构师智能体、一个 Swift 开发者智能体、一个 Metal 专家、一个代码审查者，等等，它们跨不同模块并行工作。

Claude 还让转向变得毫无痛苦：当 Respiro 最初基于 React Native 的 MVP 因为 Vlasenko 没有 Android 手机测试而遇到麻烦时，他用 Claude Code 在几个小时内用 Swift 从零重写了这款应用。

他说，从最初的想法到功能完整、可上架 App Store 的 Respiro，总共用了不到六周。

## 从 Claude Code 代码到 App Store

开发应用是一回事。上线是另一回事，而 Vlasenko 此前从未走过 Apple Developer Program 的流程。他用 Claude 引导自己一步步完成这个有时令人困惑的过程。

“卡住的时候，我只要截个图问 Claude，‘嘿，这里我该点哪个？’”他说。他用同样的方法配置其他第三方服务，比如用于日志的 Sentry、用于分析的 Amplitude。“我会告诉 Claude，*我完成了登录，这是 API key*，99% 的情况下 Claude 一次就对，”Vlasenko 说。至于那剩下的 1%，他继续说，“我只需要在第一个提示词里把需求说得更精确、更清楚，再试几次，Claude 就能给我想要的结果。”

事实上，Vlasenko 认为 [Claude 的视觉能力](https://platform.claude.com/docs/en/build-with-claude/vision)是它最被低估的功能。“你把截图发给 Claude 让它分析，它会告诉你它看到了什么。然后你就可以借此让 Claude 带你走过哪怕最复杂的 UX，”他解释道。“比如，我得在 Meta 上创建一个 API token，我在他们的界面里完全迷路了，但 Claude 真的能理解，并把你带到每一个需要去的地方。”

推广 Respiro 同样有 Claude 参与。当 Vlasenko 需要分析数据时，Claude 不只接入了 Amplitude 的基础 SDK，还配置了完整的用户漏斗、留存指标以及日活和月活的活跃追踪。当他需要内容时，Claude 开始帮他写博客文章、帮他制作 TikTok 视频。Claude 还建议了一个 Vlasenko 说自己绝不会想到的增长策略：去联系心理学家和正念从业者，让他们向客户推荐 Respiro。他试了。成功了。从业者开始推荐这款应用。

## 工作中的创始人模式

Vlasenko 在打造 Respiro 过程中练就的技能，并不只用于他的副业。如今他在 Mythical Games 的本职工作中提交代码发布、直接交付功能。更进一步，他还成了自己在做 Respiro 时形成的那套开发流程的内部倡导者，把自己的 Claude 文件夹和工作流分享给工程团队。

“他们大多数人回来说，*嘿，这个工作流比我现在的强多了！*”他指出。结果，Mythical 现在有一个小型内部团队完全通过 Claude 交付工作。不过，Vlasenko 也观察到，对所有人来说这并非毫无摩擦的转变。“有些工程师很难转换心态，不去完全控制每一行代码，”他说。“对我来说这很容易，因为我没有很深的编程背景，这感觉就是一种自然的工作方式。”

对 Vlasenko 而言，打造 Respiro 的经历抹平了可能与不可能之间的界限。他正在把语音引导练习和动作练习加入应用的下一个版本，依据的是 Claude 帮他写好的路线图，并在结束日常工作后还记录七八个小时的编码时段。

“我会说，Claude Code 是我的新瘾，”他说。

| The Claude Code Day Zero Questionnaire™ |
| --- |
| 在这里，我们向创始人提出同样一些有点傻的问题，去了解键盘背后那个人。 |
| 谁或什么激励着你？ | LeBron James。他的自律、稳定和长期主义心态极具启发性。他并非只靠天赋；他凭借不懈的专注和执行力，打造了史上最伟大的职业生涯之一。还有 Warren Buffett——完全不同的领域，但核心特质相同：数十年如一日的耐心、稳定与思维清晰。我真的很敬佩那些不靠运气、而是靠长期坚持成就伟大的人。 |
| 如果可以回到过去，你会做哪些不同的事，为什么？ | 我希望自己能更早意识到：打造产品其实是最容易的部分。传达它的价值要难得多！如今要做出高质量的东西出奇地容易，尤其是有了 Claude 这样的工具。但让人们理解它为何重要、为何值得关心——这才是真正的挑战。 |
| 如果有人把你的创业历程写成书，书名会是什么？ | 《天生自主》（Autonomous by Design） |
| 你的工作空间是什么样的？ | 大约 70% 的时间，我用 MacBook 外接显示器、键盘和鼠标工作。约 20% 的时间只用手提电脑，通常是不在家的时候。还有约 10%——用手机，通常是来了灵感又不想等的时候。另外，我的猫经常待在桌上陪我（也确保我不会连续工作太多小时）。 |
| 你现在开着多少个浏览器标签页？ | 现在——大约 5 个。我尽量保持精简。通常我会在后台放一个 YouTube 视频——我喜欢听真实犯罪或创始人播客。我也在积极运营一个 Threads 账号，分享我在做什么、实验、Claude 工作流，并帮助别人搭建他们自己的系统。 |

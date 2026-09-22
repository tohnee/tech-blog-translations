---
title: "为常驻智能体的世界设计 Grok Bot"
title_en: "Designing Grok Bot for a world of persistent agents"
date: 2026-09-03
source: https://x.ai/news/designing-grok-bot
crawled: 2026-09-22
translated: 2026-09-22
---

# 为常驻智能体的世界设计 Grok Bot

> 原文：[Designing Grok Bot for a world of persistent agents](https://x.ai/news/designing-grok-bot) · xAI

[返回新闻列表](/news)

2026 年 9 月 3 日

我们如何为超越单次会话而持续存在的智能体设计 Grok Bot——从聊天历史到 Bot 花名册、在线状态、属于 Bot 自己的计算机，以及无需提示即可开始的工作。

---

当我们开始设计 Grok Bot 时，核心问题之一是界面应当如何塑造用户与智能体之间的关系。大多数 AI 界面都围绕用户操作的聊天会话来组织。每个会话从设置开始，在用户的注视下展开，并在对话停止时结束。

我们想为一种超越任何单次会话、能够独立承担责任的智能体做设计。这意味着要重新审视界面的一些基本对象和信号，包括侧边栏里应该放什么、智能体如何展示进度，以及它的工作何时应当变得可见。

![](/_next/static/media/wallpaper-light-noon.27_hyf9uycov-.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![](/_next/static/media/wallpaper-dark-night.2tq8j5y-604e-.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

搜索

Kenny

下午 7:34

周五全员大会的幻灯片需要你点头确认。

Justin

8 封介绍信已起草——放在 CRM 里等你发送。

Luke

下午 7:34

收件箱有 3 封。两封今天必须回。

网站上线

上午 11:18

John：预演环境的结账流程已干净，3 个 bug 已关闭。

John

昨天

复现了结账崩溃。详细记录已写在工单里。

Keith

Acme 有些动摇。起草了一份周四的跟进沟通。

Tyler

上午 9:04

收到 14 张收据。还差你周二的 Uber 那一张。

Manuel

下午 2:20

发布文章已上线。前 200 次展示。

Jenny

周二

SoMa 的 3 处房源。Folsom 那套两居是最合适的。

Chang

上午 10:12

筛出 3 份。跳过了一份已在你 ATS 里的。

插件

![](/_next/static/media/user-peng.3rw63gdxpcheg.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Peng Zheng

Kenny

上午 9:41

嘿，今天设计同步会的主要结论是什么？

团队这次会议的大部分时间都在评审新的引导流程。

讨论最激烈的是空状态。Sarah 觉得现在的插画不符合新的品牌方向，屋里大多数人都同意。关于进度指示器应该放在页头还是侧边栏，也有一番很长的来回讨论。

不过整体氛围是积极的。大多数人认为这个流程已接近可以提交更大范围评审。

有人提到 Q3 路线图吗？

提到了，而且提了两次。Marcus 说路线图评审现在预计在八月第一周，Priya 问引导流程的工作会在此之前还是之后落地。会上没有敲定任何确切日期。

给 Kenny 发消息

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![](/_next/static/media/wallpaper-dark-night.2tq8j5y-604e-.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![](/_next/static/media/dock-icons.0cwlcw-73qj01.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Kenny 的屏幕

例行任务

晨间简报

每天上午 8:00

收件箱清理

工作日下午 6:00

每周团队更新

已暂停

## [重新思考基本原语](#rethinking-the-primitives)

AI 产品在短时间内积累了大量词汇。聊天、会话、模型、上下文窗口、记忆、系统提示词、项目、技能、连接器、智能体、工具、沙箱、权限、自动化——它们都描述了这些系统的真实组成部分。

但把每一个都作为独立的产品概念暴露出来，会迫使用户去理解超出其需要的东西。我们首先问的是：一个人要与智能体协作，实际上需要哪些概念。

我们不断回到五个：

1. **Bot**：常驻的智能体，拥有自己的身份、记忆、运行时和工具。
2. **聊天**：与 Bot 协作的对话式界面。
3. **提示词**：为 Bot 提供上下文或指令。可以只用一次、保存为技能，或作为例行任务自动触发。
4. **工具**：让 Bot 通过软件、API、连接器、shell 或计算机使用来获取信息并采取行动。
5. **产出物**：Bot 创建或修改的文档、设计、代码、数据及其他持久性产出。

其余一切都可以留在界面之下，直到用户有理由关心它为止。下一个问题是：这五个对象中，哪一个应该来组织整个产品。

## [从聊天历史到 Bot 花名册](#from-chat-history-to-a-bot-roster)

聊天是用后即弃的。我们开启一段对话是为了解决一个问题。它随后被挤到侧边栏下方。一周后，我们又开一段新的。你很少会回看最近五条以外的记录。

当交互的单位是一个问题时，这种行为完全合理。但当交互的另一端理应了解你、记住之前的工作并随时间承担责任时，这就变得奇怪了。

所以 Grok Bot 的主要对象是 Bot，而不是对话。Bot 有名字，有头像和头衔。它记得与你的所有对话。它有自己的计算机和工具。明天你回来时，回到的是同一个 Bot。

Project Acme

在周五通话后给 Acme 起草一封跟进邮件

重写定价单页

安全评审里我该问什么？

用我的通话记录画一张关键人地图

用尖锐异议陪我演练演示

帮我对比这三份竞品幻灯片

显示更多

Kenny

下午 7:34

周五全员大会的幻灯片需要你点头确认。

Justin

8 封介绍信已起草——放在 CRM 里等你发送。

John

昨天

复现了结账崩溃。详细记录已写在工单里。

Keith

Acme 有些动摇。起草了一份周四的跟进沟通。

## [在线状态即界面](#presence-as-interface)

一旦 Bot 成为你长期维护的对象、而非你开启的一段会话，Bot 在产品中的呈现方式就必须同时回答三个问题：

1. 这是谁？
2. 它在做什么？
3. 我需要了解多少？

### [这是谁](#who-is-this)

花名册只有在能被快速扫视时才有用。随着花名册增长，我们不希望人们每次打开产品都得逐个读名字。他们应该几乎用余光就能从头像认出一个 Bot。

![](/_next/static/media/initials-1.0yig-qj1joruk.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-2.1txviuzdipoiw.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-3.38z4vaotfsn1v.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-4.01qrbimmhtavw.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-5.3jwzv-u8m85v8.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/initials-6.19sekhuc8jakl.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-1.3h5blj8bz5-jf.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-2.39jbp_6rdd-5c.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-3.28sgvmrs9mln9.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-4.2avjpk08w6cek.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-5.01zc07ny7g1nn.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/emoji-6.09640mz61fg7f.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-1.3r4tz4_d9u_-z.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-2.3fmjch4q22wof.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-3.3riz-3zy_f268.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-4.2--kd8w9v-eaw.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-5.0d3thxc1-7umo.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agentb-6.2hz5ggcwjuefo.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-1.13x8p2khem12n.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-2.0_m9l5xohcj95.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-3.35r25_i92f7lp.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-4.1p9fcypmuoe49.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-5.1fhzuvuy00j0n.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/base-6.3t9tmxu30heol.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-1.1zc81r05mlxf2.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-2.27lpziqdwd0j0.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-3.1u9ugv0y8018y.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-4.0o6i10hvi0pyz.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-5.0dfi-x29-s1jo.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/new3d-6.30xsvxdcjr7_i.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-1.179mb5k-55q0s.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-2.0f9k73iqne5ic.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-3.3ccg438vd4bnj.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-4.26votlluxpf3p.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-5.3td20ca0sy08_.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/blob-6.24umj72ldwxsm.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-1.2vlri0g4yob5c.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-2.0k59bd-g6w77s.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-3.00_foixq2-eza.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-4.3na4nl1j5at_t.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-5.3rjal0p5m-286.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/line-6.2ehf_3xbvejl2.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-1.2utembwuppxxx.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-2.3iy5no1sbn35f.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-3.0e7acsgpg5bqv.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-4.21x56bl2zkenr.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-5.10zlplp724o1m.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/s32-6.26kxeg4kxjnex.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-1.11lta7nrjb9pn.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-2.1tpo6-fp8vgup.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-3.32f6whniadrub.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-4.1pily-uyp88-h.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-5.2sq51vj2aq2dn.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/mix-6.1e2kj0mwyz2mi.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-1.1iuswpcl3hq8o.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-2.346vsyk23d7i_.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-3.20lqy9orb-_2u.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-4.44r1bdv8r6u-c.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-5.3at_es63n-ehm.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/agenta-6.3m1estnwuqiu3.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

Bot 头像视觉风格探索，作者 Kenny Kuh 与 Peng Zheng

与此同时，我们希望头像之间保持足够一致，看起来属于同一套系统。我们研究了插画、动画、游戏和界面设计中的角色系统，探索了从首字母、emoji 到像素画、水彩、黏土风（claymorphism）、Noritake 式线稿、剪影和 identicon 的各种方向。

大多数方案都只把问题的一边解决得更好。水彩和黏土给了单个 Bot 鲜明的个性，但在侧边栏的尺寸下细节过多。更简单的系统在界面里显得更自然，却常常让 Bot 看起来可以互相替换。

我们最终确定的系统保持基本构造的一致性——使用简单形状和富有表现力的眼睛——再通过受控的变化和配饰引入差异。每个 Bot 一眼可辨，又不会显得来自另一个视觉世界。

### [它在做什么](#what-are-they-doing)

一旦头像成为 Bot 的身份，它也就成了展示状态的天然位置。Bot 可能空闲、思考、工作中、等待、受阻或已完成。我们本可以为每种状态设计一个单独的指示器，但那会给用户增加又一层需要解读的 UI。

于是我们转而探索：头像本身能承载多少生命周期。

静止时，Bot 平静而略带好奇。工作到来时，它会确认任务。工作开始时，它进入状态。等待或需要帮助时，它的动作再次改变，工作完成后则归于平静。如今头像既表明这是哪个 Bot，也表明它在做什么。

空闲工作中等待受阻思考中已完成

头像动效系统，作者 Benji Taylor

### [我需要了解多少](#how-much-do-i-need-to-know)

一个相关的设计问题是：Bot 的执行过程应该展示多少。一种做法是用标准的「三个跳动的圆点」，但那信息量太少，用户很难分清 Bot 到底在干活还是卡住了。

正在搜索网络

- 环境就绪 387ms
- 编辑 math.ts +14 −10
- 运行聚焦测试 npm test
- 运行类型检查 npm run
- 短暂思考
- 搜索代码 "toFixed"
- 阅读 AGENTS.md
- 编辑 math.test.ts +6 −2
- 运行完整测试套件 212 通过
- 提交修复：clamp NaN

- 环境就绪 387ms
- 编辑 math.ts +14 −10
- 运行聚焦测试 npm test
- 运行类型检查 npm run
- 短暂思考
- 搜索代码 "toFixed"
- 阅读 AGENTS.md
- 编辑 math.test.ts +6 −2
- 运行完整测试套件 212 通过
- 提交修复：clamp NaN

我们还尝试过展示 Bot 当前动作的简短文字描述，但人们一旦能看到一步，就想看到其余所有步骤。用户研究告诉我们，他们要这些细节主要是为了确信 Bot 仍在工作、且方向正确。

在最终设计中，头像的动效提供了第一层安心——表明 Bot 处于活跃状态。如果有人想查看它在做什么，悬停即可看到当前动作。

## [它的计算机，不是你的](#their-computer-not-yours)

每个 Bot 都有自己的计算机，可以用它浏览网页、处理文件、运行软件。这带来了另一个界面问题：这台计算机应该有多可见？用户何时可以控制它？

我们探索了四种布局：

- **悬浮窗口：**计算机触手可及，但会遮住对话。
- **并排：**让工作持续可见，鼓励用户围观。
- **模态：**查看方便，但把 Bot 的工作区当成了临时打断。
- **全屏：**给计算机充足空间，但完全取代了对话。

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

我们把计算机做得越显眼，产品就越是在鼓励用户去监督它。我们决定让它保持为 Bot 的工作区，由界面按用户需要提供不同级别的访问。

最终设计有三个级别，让用户可以进入 Bot 的工作区，又不至于被拽进去替它操作：

- **状态：**计算机活跃时，标题栏图标变为紫色。
- **预览：**打开后是一个固定的侧面板，用户无需离开对话即可跟进工作。
- **接管：**当 Bot 需要帮助时，用户可以全屏打开计算机、亲自接管，然后再交还给 Bot。

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

![](/_next/static/media/wallpaper-gray.13vta0mrxymev.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

我们还设计了随一天时间变化而变化的壁纸，清晨更亮，入夜更暗。这个细节让 Bot 的计算机拥有了自己的时间感，也使它区别于用户自己的桌面。

![light day](/_next/static/media/wall-strip-1.3gno9o6tamsil.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![light noon](/_next/static/media/wall-strip-2.06luvae_idfx_.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![light night](/_next/static/media/wall-strip-3.170lw02z5ufzv.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![dark day](/_next/static/media/wall-strip-4.31folbdvqalze.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)![dark noon](/_next/static/media/wall-strip-5.099mty7qqe_zp.png?dpl=702d66810f68a9b3358a1630ef110604e47b5f2e)

动态壁纸，作者 Kenny Kuh 与 Luke Barker。

这更接近与一位同事共事，而不是操作一台远程机器。你能看出他们在干活，需要上下文时瞥一眼他们的屏幕，需要你出手时才坐下来。

## [信息的形状](#the-shape-of-information)

早期版本的 Grok Bot 几乎用散文回应所有请求。它会把五天预报描述出来而不是展示出来，把一组任务叙述一遍而不是排成看板。用户随后还得自己重组答案。这让我们把响应的形式视为答案的一部分。

为此，我们在 Grok Bot 中内置了内联卡片和组件。当散文适合承载信息时，Bot 可以用散文作答；不适合时，则使用结构化 UI。

新邮件

可以发送

发件人peng@grokbot.app

收件人sarah@acme.com

主题将周五的设计评审改到下午 2 点

Sarah，你好：

我们可以把周五的设计评审从上午 11 点改到下午 2 点吗？临时来了一个客户电话，我不想让我们的讨论仓促进行。

谢谢，
Peng

发送邮件丢弃

内联聊天组件，作者 Peng Zheng

同样的原则也适用于动作。当 Bot 创建例行任务、更改设置或给另一个 Bot 发消息时，事件可以直接出现在对话记录中。需要深入查看时，用户可以展开它。

上午 9:41

早上好！能替我跟每个人确认一下进展吗？

这就去——现在就向团队询问状态

与KennyTyler和Jenny的 6 条消息

一切正常：Kenny 上线了落地页，Tyler 发出了本月发票，Jenny 预约了下周的面试。没有阻塞。

太好了，能每天早上都做这个吗？

已创建例行任务晨间简报

好的，你的晨间简报每天上午 9:00 会送到

最终得到的是一份异质的对话记录：对话、系统事件、交互对象和可视化共享同一条时间线。

## [组织智能](#organizing-intelligence)

一旦人们创建了多个 Bot，产品还必须组织这些 Bot 如何协作。我们需要决定哪些上下文应属于每个角色、当工作重叠时 Bot 应如何共享上下文，以及如何协调它们而不把用户变成调度员。

随着人们创建的 Bot 越来越多，我们看到了一种答案的浮现。一些人设立了一个「幕僚长 Bot」，负责协调多位专家。他们只需给一个 Bot 下达方向，而不必逐个检查、亲自派发每项任务。

给 Bot 划分清晰的角色，也迫使我们决定每个角色应当知道什么。法务 Bot 可能需要一场进行中纠纷的全部历史，财务 Bot 可能需要多年的财务记录。把这些历史合并成一大块记忆，会让为每个 Bot 提供与其工作相关的信息变得更难。

因此，在 Grok Bot 中，能力与上下文遵循不同的边界。工具和技能位于账户层面，因为许多 Bot 都可能需要浏览网页、处理文档或发送邮件。记忆和例行任务属于 Bot，因为它们反映的是这个特定角色随时间积累的认识和所做的事。换个说法：能力可以广泛共享，而上下文留在需要它的角色那里。

有些工作会跨越角色边界。群聊为项目或团队提供共享上下文，同时允许每个 Bot 保留自己专门的记忆。设计师、工程师、PM 和数据科学家可以在同一个对话中工作、互相交接，并共享项目所需的一切。

我们考虑过添加仪表盘、任务分派板和显式的交接控件来管理这些群体。但每一项都会给用户增加更多协调工作。取而代之的是，由负责协调的 Bot 处理日常路由，只有在需要判断力的决策时才把用户请进来。

## [持续运转的工作](#work-that-keeps-moving)

大多数智能体会话始于用户发出的一条提示。这让即使是常驻的 Bot 也在等待某人来激活它。例行任务让用户可以给 Bot 一项常设职责，按时间表或响应事件运行，比如关注某个行业，或每天早晨准备一份简报。用户只需定义一次工作，例行任务会在需要发生时激活 Bot。

起初我们把例行任务当作次要配置。随着它们对自主工作变得越来越重要，我们把它移入了 Bot 的主界面。对话记录展示了运行了什么，并为用户提供了审阅结果或处理异常的地方。

每天上午 8:00

工作日上午 8:00

每周一上午 9:00

每月 1 日上午 8:00

每 30 分钟

工作日 · 上午 9:00

grokbot 中创建了 Issue

Issue 所有项目中的任意事件

grokbot 上触发了事故

事故 grokbot 上的任意事件

grokbot 中开启了 PR

spacexai 中合并了 PR

acme 中关闭了 PR

main 分支有新推送

grokbot 中 PR 的检查失败

grokbot 中添加了 bug 标签

ops 中包含 /fix 的评论

grokbot 中通过了评审

grokbot 中解决了讨论串

deploy.yml 工作流失败

当 webhook 收到 POST 时

#grokbot 中的新消息

#ops 中添加了 :eyes: 表情回应

创建了匹配 dev 的频道

#design 中的新消息

Roadmap 中创建了 Issue

Core 中 Issue 状态 → In Review

Team Core 的周期结束时

Design 中 Issue 状态 → Done

Design 团队的新消息

Design 团队中创建了频道

这也改变了对话的角色。一条提示可以开启会话，但一个时间表、一个事件或另一个 Bot 也可以。随着时间推移，越来越多的工作可能在用户完全不在场的情况下开始。

## [消失的界面](#the-disappearing-interface)

到项目尾声，设计工作大多是在做减法。我们移除了窗口和面板控件、计算机视图选项以及智能体元数据。我们还设定了切实的上限：每个账户约 50 个 Bot，每个群聊 6 个。每个决定都回到同一个问题：这是帮助某人完成了委派，还是又给了他们一件要管理的东西？

随着模型进步，「操作一个 AI」与「委派给一位同事」之间的界线在不断移动。Grok Bot 反映了我们认为它今天所在的位置。从最早的探索到发布，设计 Grok Bot 的过程就是在寻找这条界线，并让界面随之改变。当智能体承担更多责任时，界面应当对人的要求更少。

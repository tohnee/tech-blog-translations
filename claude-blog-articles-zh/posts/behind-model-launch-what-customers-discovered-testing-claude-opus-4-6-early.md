---
title: "模型发布幕后：客户提前测试 Claude Opus 4.6 时发现了什么"
title_en: "Behind the model launch: What customers discovered testing Claude Opus 4.6 early"
date: 2026-02-09
source: https://claude.com/resources/articles/behind-model-launch-what-customers-discovered-testing-claude-opus-4-6-early
crawled: 2026-11-17
translated: 2026-11-17
---

# 模型发布幕后：客户提前测试 Claude Opus 4.6 时发现了什么

> 原文：[Behind the model launch: What customers discovered testing Claude Opus 4.6 early](https://claude.com/resources/articles/behind-model-launch-what-customers-discovered-testing-claude-opus-4-6-early) · Claude 博客

*在预生产访问与公开发布之间那段紧凑的窗口期里，客户争分夺秒地测试一款新的 Claude 模型究竟能做到什么。*

在一款[新的 Claude 模型上线](https://www.anthropic.com/news/claude-opus-4-6)之前，一小批客户会比全世界其他人早几天拿到访问权限。他们使用的是预生产阶段的研究模型，用真实工作负载测试它，弄清这款模型擅长什么、在哪里会出问题，以及当 Anthropic 公开发布它的那一刻，它是否已经可以交付给自己的用户。他们坦诚的评估——哪些行得通、*以及*哪些行不通——会直接影响 Anthropic 最终发布的那个版本。

评审窗口很短。团队清空日程、组建"作战室"（war rooms），开始把最难的问题一股脑抛给模型。幕后的景象是深夜、一杯又一杯咖啡，以及在不寻常的时间亮起来的 Slack 频道。他们的客户最终看到的东西是打磨过的——但抵达那个状态的过程要混乱得多，也有趣得多。

为了这篇文章，我们希望揭开帷幕，看看这究竟是怎样一番景象。[Harvey](https://www.harvey.ai/)、[bolt.new](https://bolt.new/)、[Shopify](https://www.shopify.com/) 和 [Lovable](https://lovable.dev/) 都向我们展示了他们在 Claude Opus 4.6 早期访问期内部的经历：他们采取的方法、取得的突破，以及他们先于所有人学到的东西。

## **为模型测试做准备**

团队如何启动测试，很大程度上取决于他们在构建什么。

bolt.new 开了一个专用的 Slack 频道，并刻意在早期不分享各自的印象，以免彼此产生偏见。

[Harvey](https://claude.com/customers/harvey) 的研究团队请来经验丰富的律师，在法律任务上测试模型，同时让它跑 BigLaw Bench——他们用来评测真实法律工作的基准测试。

[Shopify](https://claude.com/customers/shopify) 的工程师开始把模型接入他们此前围绕 Claude 搭建的迭代式规划循环。

在 [Lovable](https://claude.com/customers/lovable)，负责模型与评测的团队立刻进入状态——一边跑基准测试，一边安排工程师预约时间做他们所谓的"氛围检查"（vibe checks）：用新模型构建应用，感受它在哪些方面更强。Lovable 工程负责人 Alexandre Pesant 说："有点像过圣诞节。"

方法各不相同，但直觉是一致的：先把最难的问题扔给模型。

## **当结果开始传来**

测试一开始，团队就盯着两件事：模型在他们的基准测试上得分如何，以及它在实际使用中*感觉*如何。两者都重要，而且它们给出的信号并不总是一致。

Harvey 的 BigLaw Bench 结果回来了：90.2%——第一个在该基准上突破 90% 的 Anthropic 模型，其中 40% 的任务拿到满分。但真正留在人们脑海里的，是定性的反应。

他们内部的一位律师跑了一次查询，回来说输出感觉"聪明、有分析性，像是在真正思考"。当你的结构化评测和领域专家说的是同一件事时，这就是一个强信号。

bolt.new 把他们的自动化评测平台——测试构建质量、缺陷修复、代码库理解和设计美学——与手动压力测试结合起来。第一天结束时，他们已经有了一份共享文档，里面满是已部署的测试应用和具体的观察记录。

一位开发者遇到一个瀑布图的 bug，用之前的模型试了五次以上都没解决。Opus 4.6 第一次就诊断了出来：八个并行的 HubSpot API 搜索同时发出，另外还有一些查询绕过了限流保护——它们用的是裸 fetch，而不是项目里带限流的封装。

在 Shopify，资深工程师（Staff Engineer）Paulo Arruda 描述了一个颠覆惯常关系的瞬间："我让 Opus 4.6 把某个东西从一个页面移到另一个菜单项里——我就说了这些。我没指定任何细节。它不仅移了，还超出了预期，做了很多我直到看见才意识到自己想要的东西。它预判了我的下一个请求，然后直接做了。我发现自己在对 AI 说'你完全正确'，而不是像以前那样反过来。"

Shopify 助手团队的资深工程师 Ben Lafferty 则朝另一个方向施压。他让 Opus 4.6 为一个内部原型把一个大库从 TypeScript 移植到 Ruby。"它先写了一个兼容层（shim），用来跑仓库里现有的测试用例，然后一次性移植了几乎整个规格，同时对照原始测试集做验证，"他说，"指令遵循能力提升显著。这是我经历过的早期访问期里，第一次几乎没有实质性反馈可提。"

在 Lovable，测试分两条线进行。

团队跑设计基准和复杂任务评测，以得到结构化的图景；但他们也做所谓的"氛围检查"——工程师用新模型构建应用，去感受它在哪些地方更强、在哪些地方会崩。

"发现新出现的粗糙边缘，总归有点像一场赛跑，"Alexandre Pesant 说。

他自己的压力测试是一个副业项目，涉及复杂的地铁线路图和行程逻辑；他此前用别的模型试过，撞了墙。而用 Opus 4.6 并把 effort 开到最大后，模型冲过了他预期它就会卡住的那个点。

"我大致能判断出事情什么时候会行不通、什么时候是碰到了极限，"他说，"它比别人走得更远。"他还注意到一个更广泛的变化：模型能在 Lovable 内部使用浏览器并自行测试，"你能感觉到自主性上的差别"。

## **另一边是什么样子**

早期访问结束时，团队对他们手上的东西已经有了清晰的图景。我们交谈过的每个团队都反复回到同一点：与模型的关系正在改变。

"有些 bug 我们用之前的模型试了五次以上都没修好，Opus 4.6 第一次就诊断出来了。推理深度的跃升是真实的，"bolt.new 市场副总裁 Garrett Serviss 说。

"对我来说，Opus 4.6 是 Anthropic 第一个在日常工作中让我觉得像真正协作者的模型，"Shopify 的 Ben Lafferty 说，"我可以交给模型的任务时间跨度在持续增长。"

"Claude Opus 4.6 是设计质量上的一次提升，"Lovable 联合创始人 Fabian Hedin 说，"它更自主，而自主正是 Lovable 价值观的核心。人应该去创造重要的东西，而不是微观管理 AI。"

当然，并非所有反馈都是赞美，而这正是重点。早期测试者会直接影响 Anthropic 最终交付的模型版本。整个流程之所以行得通，恰恰因为团队对行不通的地方和行得通的地方一样坦诚，而且他们知道这种坦诚确实会被采纳。

"我们得以塑造工程组织未来会用到的工具，"Shopify 的 Paulo Arruda 说，"我们不只是被动的测试者——我们是开发中的伙伴。当我们指出问题或模式时，Anthropic 会倾听并迭代。"

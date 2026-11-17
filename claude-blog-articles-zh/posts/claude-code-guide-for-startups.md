---
title: "初创公司 Claude Code 指南"
title_en: "The Claude Code guide for startups"
date: 2026-08-20
author: Michael Segner
source: https://claude.com/resources/articles/claude-code-guide-for-startups
crawled: 2026-11-17
translated: 2026-11-17
---

# 初创公司 Claude Code 指南

> 原文：[The Claude Code guide for startups](https://claude.com/resources/articles/claude-code-guide-for-startups) · Claude 博客

高增长初创公司如何用 Claude Code 交付——源自十余家公司访谈的五条运营原则。

更想要 PDF？

本指南也提供下载——同样的五条规则、创始人洞见和清单，排版适合离线阅读或与团队分享。

[下载 PDF](https://assets.claude.com/054519a5658ddeee3cf9791eda1a36f4455ad842.pdf)

## 在前沿工作的 AI 原生公司

想窥见工作的未来，就去问初创公司今天是如何运作的。我们就这么做了。

我们与十余家高增长初创公司交流，了解它们如何用智能体编码工具构建产品并扩展公司。这些初创公司正在改写规则：谁有资格构建、什么该被废弃，以及如何在"构建方式"与"构建内容"之间形成飞轮。

它们的交付速度，堪比规模十倍于己的组织。

![ClickHouse](https://assets.claude.com/002d4e2a6b94d0409b6dd64c8e91ac1e1fac0bd8.svg)

**30%**

功能交付量增加

![Omni](https://assets.claude.com/ade4bc4e76a4151d0e0ba0e7c78fa7eaf24f39c3.svg)

**2–3 倍**

工程生产力提升

![Clay](https://assets.claude.com/267a4deeacbde106146d26ffa4ef2b08fbb3cb4f.svg)

**100%**

bug 分诊自动化

![Artemis](https://assets.claude.com/4c49849997fa71df9c3086ce4dc48ed96d44abfd.svg)

**6,000+**

每周 PR 数

在本指南中，我们将深入这些组织各具特色的部署方式，学习它们为快速交付并保持竞争优势所遵循的规则。

在此过程中，我们也将开始回答一个问题：如果一个组织从零开始，用 Claude Code 构建整个产品开发生命周期，那会是什么样子？

### 创始人洞见来自

* [![Artemis](https://assets.claude.com/4c49849997fa71df9c3086ce4dc48ed96d44abfd.svg)](https://artemissecurity.com/)
* [![Cainex](https://assets.claude.com/f56808d1860fc6dec47de96660f570d6fc9b468f.svg)](https://www.cainex.com/)
* [![Clay](https://assets.claude.com/267a4deeacbde106146d26ffa4ef2b08fbb3cb4f.svg)](https://www.clay.com/)
* [![ClickHouse](https://assets.claude.com/002d4e2a6b94d0409b6dd64c8e91ac1e1fac0bd8.svg)](https://clickhouse.com/)
* [![Commure](https://assets.claude.com/e054a5fc14658f016836f9897a3c9035c0d7b30d.svg)](https://www.commure.com/)
* [![Crosby](https://assets.claude.com/9815d36508ab5cbef0ba2782bc26371f19356894.svg)](https://crosby.ai/)
* [![Emergent](https://assets.claude.com/3ecc6fb3c36328f216239a92947c6a75e5dd54d9.svg)](https://emergent.sh/)
* [![Harvey](https://assets.claude.com/9447073367b83132335cb2c191c36bef275f48e6.svg)](https://www.harvey.ai/)
* [![Heidi](https://assets.claude.com/18cd69d52e1475b87358e17bd02b9f79d5049bc5.svg)](https://www.heidihealth.com/)
* [![Higgsfield](https://assets.claude.com/bf441d6847e786ea78a00e4361f0478a2ee260e7.svg)](https://higgsfield.ai/)
* [![Omni](https://assets.claude.com/ade4bc4e76a4151d0e0ba0e7c78fa7eaf24f39c3.svg)](https://omni.co/)
* [![Parahelp](https://assets.claude.com/8d2694cc4ea70bbae09ecf919b6b7fc81ec50df7.svg)](https://www.parahelp.com/)
* [![Translucent](https://assets.claude.com/414fb7868ededc0a2f895e1583fdff9578381784.svg)](https://www.translucent.co/)
* [![Zingage](https://assets.claude.com/7a6b9b092d1ec61d938402cc6744e4d94ed2564a.svg)](https://zingage.com/)

**提示**

只关心可落地的下一步？我们在[本指南末尾](#清单)放了一份清单，汇总了各章的关键技术建议。

## 01 人人都能交付

智能体编码降低了门槛，于是真正理解问题的人，可以亲手交付修复方案的第一个版本。

智能体编码降低了非技术员工构建产品的门槛。有了 Claude Code，即使你不精通编程语言、不熟悉 IDE，也能做出可用的功能。

![](https://assets.claude.com/777148b01c9c3f7be3cf75bf029bf0a1daf0876b.jpg?w=168&q=75&fm=webp&fit=max)
> "不只是工程师交付得多得多，像我这样的非技术人员也突然能交付 UI 改动和其他产品改进了。"

[Mads Lunau Liechti](https://www.linkedin.com/in/mads-lunau-liechti/)，[Parahelp](https://www.parahelp.com/) 联合创始人

对初创公司创始人来说，优势显而易见。其一，他们没有大竞争对手那样的人手，所以必须"全员上阵"。但创始人看中的不只是多出来的产能——这些非技术成员还带来了领域专业知识。

![](https://assets.claude.com/e03dea8351fda949e3c950e1f42c4e79bb65c21c.jpg?w=168&q=75&fm=webp&fit=max)
> "Claude Code 改变了在 Crosby 做律师意味着什么。律师拥有最好的产品洞见，因为他们就是用户。看着他们大展身手，真是太棒了。"

[Ryan Daniels](https://www.linkedin.com/in/crosbyryan/)，[Crosby](https://crosby.ai/) 联合创始人兼 CEO

Heidi 联合创始人兼 CEO Thomas Kelly 博士也告诉了我们同样的事。

![](https://assets.claude.com/10bc73da91563f63ea78792df45b4c23b83aec0d.jpg?w=168&q=75&fm=webp&fit=max)
> "对我们来说，Claude Code 解决了'传话游戏'问题。过去一个新想法在团队里流转的方式是：有想法的人告诉 PM，PM 告诉设计师，设计师再告诉工程师……想法的精髓不可避免地在这条链路上丢失。等到东西上线时，往往已经不像那个人最初设想的样子，而且还花了好几周。Claude Code 把这条链路压缩掉了。真正理解问题的人可以直接交付一个 PR，只在需要专业判断的环节把设计师和工程师拉进来。"

[Thomas Kelly 博士](https://www.linkedin.com/in/tomkeykong/)，[Heidi](https://www.heidihealth.com/) 联合创始人兼 CEO

说"人人都能交付"很适合发 LinkedIn，但现实中怎么运作？市场团队在批准 pull request 吗？法务团队在研究如何二分定位不稳定的测试吗？

我们得到的答案是：分工依然存在。市场人员仍专注市场，开发者仍专注开发。但从想法到可用原型、从 0 到 1 这个至关重要的第一步，向所有人敞开。

我们还看到，最有效的初创公司会建立机制，让这些贡献成为系统性行为，而不是寄望于偶然或个人的进取心。

### 建立连接

让员工预期要使用 AI 是一回事，让他们真正拿到 Claude Code 和所需工具是另一回事。

![](https://assets.claude.com/f7c8dc8ab99a4876f637ab9d4a56c05db52bc8d7.jpg?w=168&q=75&fm=webp&fit=max)
> "我们其实不是在回避[让非技术员工做贡献]，而是在迎向它。我们的看法是，每个角色都在变成工程角色，因为你可以为它构建软件……所以我们招的是爱折腾、对构建有兴趣的人。"

[Kareem Amin](https://www.linkedin.com/in/kareemamin/)，[Clay](https://www.clay.com/) 联合创始人兼 CEO

在 Crosby，团队没有把律师带到 Claude Code 面前，而是把 Claude Code 带到律师面前——把它接入他们熟悉、每天都在用的工具和系统。

**提示**

Claude 无法理解它看不到的东西。扩展 Claude 价值最有效的方式之一，就是把它接入可信来源和团队每天使用的工具。

[MCP](https://code.claude.com/docs/en/mcp) 是一个用于 AI 与工具集成的开源标准，让 Claude Code 能访问你的工具、数据库和 API。每当团队发现自己在把信息从某个工具复制粘贴进 Claude，就该考虑添加这类连接。

当已有成熟的命令行工具（`gh`、`kubectl`、`bq`、`psql`），且你希望 Claude 与工程师使用同一份事实基准时，通过 CLI 连接可能更节省 token。

![](https://assets.claude.com/e0d8cf3d206d25734edd01413cc3516d4d66e38c.png)

Claude Code 桌面端中的 MCP 连接器目录。

### 站会展示

想法总得有被排上优先级的机会，组织资源才能把它推向市场。对产品经理来说这条路很清晰——毕竟那就是他们的工作——但对非技术员工就没那么清晰了。

Clay 设立季度评审，让原型被纳入考量，并有机会进入正式路线图。Clay 的一位 GTM 团队成员就是这样做出了一个自主智能体：它访问你的网站、填写你的线索采集表单、计时看你多久响应、给体验打分，并生成一份绩效报告。

Omni 有一个专门的 Slack 频道，用于展示 Claude 生成的原型，包括资深技术人员在内的所有人都往里贡献。他们还实践"人人都能交付"的推论——"人人都与客户对话"。

![](https://assets.claude.com/fee2f7e667afc975c0a300f48a1f5c6a6e9986a8.jpg?w=168&q=75&fm=webp&fit=max)
> 尽管工程师不会天然被客户通话吸引，Omni 还是刻意把他们放到客户面前，因为这样能更快闭合反馈回路。

[Chris Merrick](https://www.linkedin.com/in/merrickchristopher/)，[Omni](https://omni.co/) 联合创始人兼 CTO

### 共享技能

"人人都能交付"与"零敲碎打"之间的界线可能很窄。功能原型无论出自谁手，最终都要整合进一个感觉像完整整体的产品。这时技能（skills）——把团队标准和上下文编码下来的可复用指令文件——就能帮助开发在流程日趋民主化的同时保持一致。

"团队任何人都可以用 Claude Code 以我们的设计系统为参照，起草产品组件、营销物料或演示材料。任何触及产品的 AI 都必须跨过更高的门槛，而 Claude Code 帮我们更精确地达到这个门槛。"Heidi 的 Thomas Kelly 博士说。

技能还能让新开发者和非技术员工快速入职、迅速上手。

![](https://assets.claude.com/0eb2fe5da7332af61215ca4ae5320f375ef72928.png?w=168&q=75&fm=webp&fit=max)
> "……我们还有一个存放 Claude Code 技能的 GitHub 仓库，它充当共享知识库，能快速用已知的 Emergent 细节启动一个 Claude Code 会话，比如数据库[和数据仓库]的位置、一些 schema[信息]、整体公司上下文……。不必追求完美，只要智能体能快速验证并纠正方向，上下文文件稍有陈旧是可以接受的。"

[Mukund Jha](https://www.linkedin.com/in/mukund-jha-a1596413/)，[Emergent](https://emergent.sh/) 联合创始人兼 CEO

![](https://assets.claude.com/7e5acf1e961c4204e46a47a0bd19450fe9f0e58e.jpg?w=168&q=75&fm=webp&fit=max)
> "我们的工程师用 Claude Code 搭起一个内部专用智能体市场，按角色组织，让工程、交付和销售各自拿到契合实际工作方式的工具。"

[Jack O'Hara](https://www.linkedin.com/in/jack-o-hara-/)，[Translucent](https://www.translucent.co/) 创始人兼 CEO

**提示**

技能[可以通过目录在公司内共享](https://code.claude.com/docs/en/plugin-marketplaces)，这样一位员工的最佳实践能立刻传给另一位。在仓库的每个子目录里用 `CLAUDE.md` 文件写明该子目录专属、每次都适用的编码约定。按需执行的流程性工作流则用技能。更多信息请阅读：[驾驭 Claude Code：何时使用 CLAUDE.md、技能、hooks 和子智能体](/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more)。

## 02 自动化琐碎工作

让智能体承担生命周期中机械的 80%，工程师就能把时间花在真正需要判断的案例上。

自工业革命以来，所有公司都在通过技术提升效率，但这些初创公司靠采用的速度和深度拉开了差距。

这些创始人相信 AI 是其使命中不可或缺的组成部分。许多人明确表示，由智能体承担机械的 80%，工程师才能把时间用在真正需要判断的案例上。

![](https://assets.claude.com/b0484f07fb5d387c4006d3a9cf0614b525a69689.png?w=168&q=75&fm=webp&fit=max)
> "所有人都在竞相构建 AI 产品。愿意重建公司实际运作方式的人少得多。后者才是更大的解锁。Artemis Security 作为一家 AI 原生公司运营，而不是一家碰巧用了 AI 的公司。这让我们的速度大幅提升，也让我们能以机器的速度帮助客户阻止攻击。"

[Shachar Hirshberg](https://www.linkedin.com/in/shachar-hirshberg/)，[Artemis Security](https://artemissecurity.com/) 联合创始人兼 CEO

具体而言，我们看到 AI 与它们 SDLC 各阶段的整合比别的公司更紧密，也有更多为端到端承接重复性任务而专门构建的智能体。下面各看几个例子。

### AI 原生 SDLC

本指南中的许多初创公司都落实了加速团队进入智能体编码流程的措施。例如，Mukund 告诉我们，在 Emergent，"新人第一天只需让 Claude 指向正确的 markdown 文件，就能把整套开发环境搭起来。如果 Claude 在入职过程中遇到任何损坏或过时的内容，它会更新那个文件。"

**提示**

[Code Review](https://code.claude.com/docs/en/code-review) 是 Claude Code 中的托管多智能体服务。它会在你启用的仓库里对 PR 执行一轮自动审查。你可以手动修复发现的问题并 push，或者通过在发现项下评论 `@Claude` 来闭环（前提是你已设置并配置好 GitHub Actions）。

![](https://assets.claude.com/34bded07fcea3eac15f98f353ee808974a44b101.png)

Code Review 会给每个发现项标注严重级别。

工程师需要快速完成入职，因为这些团队交付得很快。

![](https://assets.claude.com/9a5f813e3ee4e8e2d591259a52dae3505693ee77.png?w=168&q=75&fm=webp&fit=max)
> "这里的工程师在编排智能体集群，把生产数据问题的修复在发现当天就交付，并同时推进多个 PR。一位工程师用 Claude 子智能体并行推进了一个约 13 个工单的专项，每个子智能体负责一个工单及其 PR。"

[Tanay Tandon](https://www.linkedin.com/in/tanaytandon/)，[Commure](https://www.commure.com/) CEO 兼创始人

在这些组织里，Claude Code 不仅帮忙生成代码，也负责审查。"我们依据经过验证的技术与合规框架运行自动化代码审查，标出关键问题，并在任何内容发布前把建议改动转给合适的审核人。"Heidi 的 Kelly 博士说。

其中一些组织还为代码审查、测试和 CI 构建了定制智能体。这些初创公司把相当大的注意力放在[构建循环](https://claude.com/resources/articles/getting-started-with-loops)上，而不只是部署代码。

"我最喜欢的[智能体]是'Translucent 代码审查员'，它会把一处改动展开、从多个角度审查，然后像我们某位资深工程师那样综合结果，但比任何一个人都快。"Translucent 创始人 Jack 说。

Clay "……构建了一个处理……bug 分诊的智能体，从第一轮排查一直到为修复建议代码改动。"Kareem 说。

**提示**

过去几个月里，[Claude Tag](https://claude.com/product/tag) 一直是 Anthropic 应对 CI/CD 故障的值班第一响应者。在近期每一起有情况报告的事件中，首份报告都由 Claude 撰写，通常会在 15 分钟内发布首次分析。

[Claude Tag 有自己的服务账号](/resources/articles/agent-identity-access-model)，可访问 Anthropic CI 工程师所需的工具，比如 Datadog 或 Grafana。常设指令以技能形式写在 markdown 文件里，提交到 GitHub 仓库。这样多位同事可以迭代它们，我们也能像管理代码一样管理变更。

![](https://assets.claude.com/f60bcb14cf717c2d43f5ff9ba5eab9861b91d831.png)

Claude Tag 接手 Slack 中的值班讨论串，并在频道内汇报进展。

![](https://assets.claude.com/f9f778a29e7d934084fa793c629068373feb51c1.jpg?w=168&q=75&fm=webp&fit=max)
> 这一点在 [ClickHouse](https://clickhouse.com/) 体现得最为明显。**联合创始人兼 CTO Alexey Milovidov 介绍**，这家数据库公司已把几乎每个 SDLC 阶段都变成了自主循环。两个专为修复不稳定测试和发现测试覆盖缺口而构建的智能体，如今已是 ClickHouse 仓库的第二、第三大贡献者。另一族智能体负责运维，而团队用 Claude Code 来构建并迭代这些智能体本身。

### 用智能体加速流程

另一个一贯的模式是：这些初创公司不仅用 Claude Code 里的智能体循环加速开发工作，还创建智能体来加速那些反复出现、往往枯燥的流程。

这些多是例行工作，以便把更多注意力放在竞争优势、客户关系和营收增长上。我们看到最常被 Claude 加速的流程之一，就是自助式数据分析。

这些公司几乎每一家都有某种流程，能用新鲜数据（包括非结构化数据）快速决策——这种快速转向的能力，对初创公司的生存至关重要。

例如，Clay 构建了一个内部分析智能体；Heidi 用 Claude Code 把客户和临床医生反馈与使用数据一起分类，从而浮现出对产品洞见重要的信号。

ClickHouse 和 Omni 都把这类 AI 数据分析打包进了自己的产品，全部由 Claude 驱动。

其他例子包括：用子智能体总结数千份法律文件（Crosby）、扫描理赔数据以标记各站点的异常（Commure），以及持续挖掘医院财务数据、寻找任何分析师团队都来不及捕捉的预警信号（Translucent）。

**提示**

[动态工作流](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/)可以把多个子智能体展开，并行分析大量数据，或对另一个智能体的工作进行对抗式审查。使用 Claude Opus 或 Claude Fable 这类模型时，说"展开多个子智能体"或"使用工作流"。

![](https://assets.claude.com/a6ae82f87e4ab07588d0f70e4c528365080cdb14.png)

## 03 信任，但要验证

除非你有可靠的手段监控并验证结果，否则就无法自动化一个流程。

这条规则是第 2 条"自动化琐碎工作"的必要推论。除非你有可靠的手段监控并验证结果，否则就无法自动化一个流程。

![](https://assets.claude.com/9696a56eaa29376c23109fc6a50dccf00577519b.jpg?w=168&q=75&fm=webp&fit=max)
> Artemis Security 联合创始人 Dan Shiebler 说，他们提升的部署速度之所以可行……"是因为我们在测试基础设施、代码库组织和团队知识系统上深度投入，让智能体能端到端交付。这就是我们用 Claude 构建的飞轮：把代码库、知识库和团队以正确的方式组织起来，每一次贡献都会复利增长。"

[Dan Shiebler](https://www.linkedin.com/in/dan-shiebler-10219b42/)，[Artemis Security](https://artemissecurity.com/) 联合创始人

![](https://assets.claude.com/56a82bd3edaf8003b57812e5a1b37c6753b7e938.jpg?w=168&q=75&fm=webp&fit=max)
> "早期我们给了 Claude 完全的自主权，它做了 AI 会做的事：快速交付看起来合理的代码。问题是它以看似正确、实则不然的方式偏离了我们的架构。于是我们……把每一条不变量写了下来。我们如何定义问题。无论什么情况下都必须成立的东西。如何证明某件事可行，而不是相信一个自信的答案。567 行，写清这个团队如何思考。"

[Victor Hunt](https://www.linkedin.com/in/victor-c-hunt)，[Zingage](https://zingage.com/) 联合创始人兼 CEO

**提示**

把不可变更的内容放进仓库根目录的 `CLAUDE.md`。Claude 在每次会话开始时读取它，于是你的架构规则、安全边界和不可妥协项会随每次会话一起生效。

需要说明的是，这些初创公司没有一家让智能体合并到 main 然后听天由命。其中许多处于高度监管的行业，需要强有力的治理框架。Cainex 是一个特别有说明性的例子：它把智能体与确定性检查结合起来，读取病历并生成指导医院计费的编码。

![](https://assets.claude.com/6ee9006723da038933b4e3e4a6c6e2fa8b4b2f69.jpg?w=168&q=75&fm=webp&fit=max)
> "在医疗编码里，一个错误的编码不是笔误，而是一起计费与合规事件。这一个事实决定了我们如何构建。"

[Uriah Israel](https://www.linkedin.com/in/uriah-israel/)，[Cainex](https://www.cainex.com/) 联合创始人兼 CTO

"这是 Claude Code 为我们运行的循环。我们用一个智能体处理一批数据，审计人员在内部应用里审核输出。他们看到的不只是编码，还有模型的推理过程，并对两者都做评论……。一切都是带版本、可审计的。"他说。

"然后 Claude Code 接手。它直接从数据库读取原始预测，以及每一条修正和评论。每条修正都按所涉编码类别打了标签，因此 Claude Code 知道它面对的是诊断问题、操作问题还是其他类别，可以直接找到管辖该特定编码类型的指引。

接下来，它找出智能体指令中导致该错误的那部分并加以修改；如果案例确实是全新的，就写下新的指引。每处改动都针对一套带版本的指令进行，并拿失败的记录做测试。我们执行的规则是：修正原则，而不是修案例。"他继续说。

"然后是回测。一条记录可能有不止一种可接受的编码，所以不是字符串匹配。检查结合了两部分：与我们的可接受集合做语义匹配，以及一个判断器来问'这是真正的错误，还是只是另一条有效路径'，Claude Code 还会在此之上加上自己的比较。

它把候选改动跑一遍黄金集加随机样本，在任何内容发布前暴露回归。返回的是一份短清单：建议的修改、它无法解决的记录，以及它希望得到回答的问题。工程师把时间花在真正困难的案例上，而不是机械的 80%。"他说。

创始人可以从这个医疗计费专用工作流中得出许多可泛化的经验。

例如，Cainex 让领域专家定期审核并引导 Claude 的推理，并确保这些引导成为自我改进循环的一部分。不过，这些专家不是逐案修补，他们的引导是作为自我改进循环的一部分被使用。用 Uriah 的话说："修正原则，而不是修案例。"

**提示**

循环（loops）是反复执行工作周期、直到满足停止条件的智能体。它们是用 Claude Code 完成更自主或更长周期工作的有效方式。[你可以用技能定义智能体需要满足的标准](/resources/articles/building-verification-loops-in-claude-code-with-skills)（定义得越清楚越好），让智能体反复迭代直到达成目标。

例如，许多组织会创建"不稳定测试智能体"或循环，因为停止条件清晰且自洽：智能体可以通过反复重跑测试、直到通过来验证自己的修复。

![](https://assets.claude.com/0c0fab39c03f3bef320d3a017d73ecd8592dd7b6.png)

循环反复执行工作周期，直到满足停止条件。

另一个要点是对维护高质量评估"黄金集"的投入——这组经验证的问题-答案对，用于验证智能体的准确率。每家初创公司都应为关键用例维护多套 eval，并定期更新，以防漂移并评估未来的模型。

![](https://assets.claude.com/cda18e355fb29a209fbb90b45a6455cb68e4e64a.jpg?w=168&q=75&fm=webp&fit=max)
> "[Claude Code] 还改变了我们管理模型迭代速度的方式。新的视频和图像模型不断出现，每个在上线前都需要新的技能、评估、路由逻辑和生产测试。Claude Code 把这个周期从数天压缩到数小时，让我们能在生产环境发现问题并在同一次会话里部署修复……。当你与人数十倍于你的公司竞争时，这种杠杆会改变一切。"

[Alex Mashrabov](https://www.linkedin.com/in/amashrabov)，[Higgsfield](https://higgsfield.ai/) 联合创始人兼 CEO

**提示**

团队刚开始构建智能体时，靠人工测试、内部试用（dogfooding）和直觉的组合往往能走出惊人的距离。崩溃点通常出现在用户反馈说智能体在改动之后变差了，而团队"两眼一抹黑"，除了猜和试没有任何验证手段。团队无法区分真实回归与噪音，无法在发布前自动用数百个场景测试改动，也无法衡量改进。更多信息请阅读：[揭开 AI 智能体 eval 的面纱](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)。

Uriah 提出的最后一点是，这个过程需要投入。"它不是一开始就这么干净的。我们的第一版过拟合了。它会通过把具体案例编码进去来'修复'问题，我们不断累积补丁，而不是变得更聪明。我们改变了方法，强制使用通用原则，并限制一次改动里最多能塞进多少具体细节。"

**提示**

AI 智能体不是确定性的，但许多高度受监管的工作要求每次都以相同方式执行流程。Claude Code 有一些功能，可以帮助把前沿智能与确定性流程结合起来。

[Hooks](https://code.claude.com/docs/en/hooks) 是用户自定义的命令，在 Claude Code 生命周期的固定节点触发，可以作为硬性关卡。无论模型怎么决定，它们每次都会执行。例如，它们可以用来阻止未通过 lint 的写入、要求提交前测试通过，或在任何内容离开沙箱前剥离密钥。

[动态工作流](https://code.claude.com/docs/en/workflows#orchestrate-subagents-at-scale-with-dynamic-workflows)以确定性顺序、独立上下文窗口和聚焦目标来编排子智能体。`/goal` 对于长而复杂的任务很有帮助，因为在这类任务中 Claude 可能过早宣布完成、在审查时偏袒自己的发现，或偏离最初目标。

## 04 为重建而构建

模型能力在这些团队脚下不断变化，因此很少有东西被视为永久。

这些 AI 原生初创公司中，许多都处于持续再造的状态。

AI 往往既是它们构建之物的核心，也是它们构建方式的中心。由于模型能力持续演进，开创性的功能和关键的脚手架，一旦变成沉没成本就被立刻丢弃。这些组织中许多把这持续的重建视为竞争优势的一部分。

"我们在 Clay 的做法是：你先做一遍，再做一遍，再做一遍。等到第四次做的时候，你已经知道所有需要的东西，就做对了。所以我们不一定丢掉东西，我们只是重建它：这一次更清晰。"Kareem 说。

"重建不是在新路径上线时完成的，而是在旧路径消失时才完成。以前，拆除工作在优先级争夺中总是输：它枯燥，而且不交付任何功能。"Commure 联合创始人 Tanay 说。"现在，Commure 的一位工程师只要调用一个 Claude 技能，大意是'对每个已经向所有人发布的功能开关，开一个 PR 移除它和关联代码'，然后工程师审核返回结果。过去要吃掉大量开发周期的迁移，现在就是做计划和展开执行，几个小时搞定。"

**提示**

用 [git worktree](https://code.claude.com/docs/en/worktrees) 在仓库的隔离副本里进行重建，当前版本保持不变。Claude Code 可以为你创建一个——你让 v2 与 v1 并排运行，对两者跑 eval，只有当新版本胜出才合并。正是这让"做四遍"变得便宜。

![](https://assets.claude.com/b3a73f9f5fc3c905cb94c25e5c5643a9bf87638d.png)

一个仓库、一个对象存储——三个可同时工作的检出，各自位于自己的分支。

每个链接的 worktree 都是一个普通目录，有自己的检出分支；三者共享 acme-web 内单一的 .git 对象存储。

Kareem 还把持续重建、演进和创建自我改进循环的能力，描述为 Clay 护城河的一部分。

"我认为现在任何公司的护城河都在于它必须能自我改进。所以 Clay 是一个自我学习的收入引擎。你用得越多，我们就越清楚谁是你最好的客户、你该说什么、什么有效、什么无效——而这些随时间在变。"他说。"真正的竞赛是：谁能最快触达分发……这样你才能帮助每一位[客户]，进而实现自我改进。"

在 [2026 年 5 月的 Code with Claude 活动](https://www.youtube.com/live/OFDm3T7pVlc?si=Z_RENcJSqm8H79aj)上，Harvey 应用 AI 负责人 Niko Grupen 谈到，每一波新的模型能力——涌现推理、智能体自动化、规划与编排——都要求对平台做一次完整的重新架构。

![](https://assets.claude.com/75801fece65e4c2852f8dc9a24862591f645bae2.png?w=168&q=75&fm=webp&fit=max)
> "如果你六个月前问我我们的架构是什么样，我会给出一个与今天根本不同的答案。如果我们当初不愿意说'嘿，我们得推翻这个，转向智能体原生'，我们的平台现在根本不可能具备这些能力。"

[Niko Grupen](https://www.linkedin.com/in/nikogrupen)，[Harvey](https://www.harvey.ai/) 应用 AI 负责人

**提示**

对于非平凡的重写，在[计划模式](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)下启动 Claude Code（`--plan` 或按 Shift+Tab）。Claude 会先探索代码库并提出重建方案，然后再写任何代码——你批准或改变方向。这是发现一次即将偏离架构的重建最便宜的地方。

## 05 原型、内部试用、产品化

用 AI 构建，帮助这些初创公司用 AI 打造颠覆性产品——这是它们流程核心处的飞轮。

这些初创公司中，许多在开发流程的核心都有一个关键飞轮：用 AI 构建，帮助它们用 AI 创造颠覆性产品。

当开发者推进自己的智能体编码实践时，他们对模型能力有更强的把握，也对前沿 harness 设计如何演进有更深的洞见。随后他们可以把这些启发用到自己的智能体和产品中。

"我们从 [Anthropic] 的'文件 vs 嵌入'方案中获得灵感，这让我们更有底气在自己的产品里保持简单。我们避免了很多本会来自 RAG 管道的复杂度。"Omni 的 Chris 说。"我们还看到 Claude Code 的 harness 如何让用户并行做事，并把其中一些概念适配进了我们自己的 UI。"

这也有助于它们保持对自身产品表现的敏感度。

"因为我们的应用构建器背后也使用 Anthropic 的模型，所以当我们在产品上看到某种行为……可以很快通过 Claude Code 在本地调试，判断这是模型行为还是 harness 问题。这对改进我们的分诊周期帮助巨大。"Emergent 的 Mukund 说。

我们反复听到的模式是：用 Claude Code 构建一个内部智能体，在内部使用（dogfood），然后视反馈情况，把它升级为面向客户的产品，通常使用 Claude API、SDK 或 Claude Managed Agents。

"我们[在产品里]构建了自己的 AI 智能体，团队直接与它们交互，包括 SQL 控制台里的一个智能体和一位 AI SRE。我们用 Claude Code 来构建并迭代这些智能体本身。为客户的 AI 体验提供支撑的工具，有一部分就是用 AI 构建的。"ClickHouse 的 Alexey 说。

## 清单

本指南涵盖了很多内容。以下是把关键建议汇总在一页上的清单：

第 1 章：人人都能交付

Claude 无法理解它看不到的东西。通过 [MCP](https://code.claude.com/docs/en/mcp) 或 CLI，把它接入可信来源和团队每天使用的工具。

创建[公司插件市场](https://code.claude.com/docs/en/plugin-marketplaces)，让一位员工的最佳实践能通过技能立刻传给另一位。在仓库每个子目录里用 CLAUDE.md 文件写明该子目录专属、每次都适用的编码约定。按需执行的流程性工作流则用技能。

第 2 章：自动化琐碎工作

在一个仓库上设置 [Code Review](https://code.claude.com/docs/en/code-review)（研究预览），对 PR 执行自动审查。

让 [Claude Tag](https://claude.com/product/tag)（公开测试）参与你的 CI/CD 值班响应和 bug 分诊。

[动态工作流](https://code.claude.com/docs/en/workflows#orchestrate-subagents-at-scale-with-dynamic-workflows)可用于展开多个子智能体并行分析大量数据，或对另一个智能体的工作进行对抗式审查。

第 3 章：信任，但要验证

把不可变更的内容放进仓库根目录的 CLAUDE.md。

使用[循环](https://code.claude.com/docs/en/workflows)——反复执行工作周期直到满足停止条件的智能体——来完成更自主或更长周期的工作。

建立一套[创建和维护智能体评估](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)的流程。

[Hooks](https://code.claude.com/docs/en/hooks) 是用户自定义的命令，在 Claude Code 生命周期的固定节点触发，可作为硬性关卡。当工作中某些环节需要确定性时，就用它们。

第 4 章：为重建而构建

用 [git worktree](https://code.claude.com/docs/en/worktrees) 在仓库的隔离副本里进行重建，当前版本保持不变。正是这让"做四遍"变得便宜。

对于非平凡的重写，在[计划模式](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)下启动 Claude Code（/plan 或按 Shift+Tab）。Claude 会先探索代码库并提出重建方案，然后再写任何代码——你批准或改变方向。这是发现一次即将偏离架构的重建最便宜的地方。

## 前沿的初创公司，在前沿构建

这些洞见来自与你一样在前沿构建的同行，希望你觉得它们实用、可执行。Claude 初创社区是灵感、最佳实践和建议的持续来源。你可以通过以下方式加入：

* [订阅初创公司通讯并加入初创公司计划](https://claude.com/programs/startups)。
* [收藏即将举行的 Claude Code 网络研讨会](https://academy.claude.com/code/webinars)。
* [参加你附近的活动](https://luma.com/claudecommunity)。
* 在 [Reddit](https://www.reddit.com/r/ClaudeAI/) 和 [Discord](https://discord.com/invite/6PPFFzqPDZ) 上参与贡献。
* 早期公司还可以申请 [Claude for Startups 计划](https://claude.com/programs/startups)以获得额度与支持。[了解该计划现在包含什么](/resources/articles/were-expanding-the-claude-startups-program-to-help-founders-build)

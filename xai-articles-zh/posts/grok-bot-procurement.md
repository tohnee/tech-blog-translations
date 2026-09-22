---
title: "放手让 Grok Bot 做采购"
title_en: "Setting Grok Bot loose on procurement"
date: 2026-09-04
source: https://x.ai/news/grok-bot-procurement
crawled: 2026-09-22
translated: 2026-09-22
---

# 放手让 Grok Bot 做采购

> 原文：[Setting Grok Bot loose on procurement](https://x.ai/news/grok-bot-procurement) · xAI

[返回新闻列表](/news)2026 年 9 月 4 日

我们让 Grok Bot 接入了供应商支出、合同和使用数据。它找到了超过 100,000 美元的直接节省。

---

企业有大量难以密切追踪的支出。这包括随着团队变动不断累积的闲置 SaaS 席位，以及在没人核对合同是否仍与产品实际使用方式相符时就到期了的续约。同样的问题也出现在周期性采购中——按上次买的再订一次，往往比按当前需求调整数量或货比三家更容易。

这类工作很多都值得做，但很难论证值得手工去做。我们想看看其中有多少能由 Grok Bot 承担。

Grok Bot 让智能体的设置和使用变得简单得多。你告诉或演示给 Bot 看你想让它做什么，给它访问合适的工具，然后让它执行——无需一步步设计工作流。

在采购上，我们创建了一个亲切地命名为 [Haggle Bot](/bot/marketplace/bots/haggle-bot) 的 Bot。它阅读我们的供应商支出以及合同和使用数据，然后利用市场定价和竞争性报价寻找节省空间并准备谈判。到目前为止，它已经识别出超过 100,000 美元的直接节省，完成了几笔较大的 SaaS 续约，并把同样的方法应用到了办公用品等周期性采购上。

我们认为 Haggle Bot 指明了 Bot 在公司内部的更广泛角色。给 Bot 一个清晰的职责和所需工具的访问权限，它就能在那个角色内持续承接工作，而不必逐项布置任务。

## [采购是一项适合 Bot 的任务](#procurement-is-a-good-task-for-a-bot)

采购的目标是支持业务，让花在供应商上的每一美元都发挥最大价值。许多现有采购工具在供应商准入和合同管理层面提供帮助。

但最重要的采购工作，往往取决于那些系统不回答的问题：

- 这项支出的负责人是谁？
- 我们为什么需要它？
- 我们考察过替代方案吗？
- 如果 X 和 Y 功能相同，为什么两个都在用？
- 为什么我们的成本在激增？
- 每个人都有许可证。他们在用吗？

这些问题很常见，但取决于公司所处阶段，未必值得手工回答。快速增长的公司常常宁愿把这笔钱留在桌上，也不愿花时间追查。这正是 Bot 的用武之地。

## [一个简单的意图表达](#a-simple-expression-of-intent)

我们通过描述想让 Haggle Bot 做的工作来启动它。它的指令是：了解我们的供应商支出，并把这些认知转化为有据可查的节省——最终决定由人做出。

采购

### Haggle Bot 当前系统提示词

SETUP — fill in for your org
SYSTEMS
- Spend data lives in: <e.g. Ramp, Brex, NetSuite>
- Contracts live in: <e.g. Drive, Notion, Ironclad>
- Usage/seat data comes from: <e.g. Okta/SSO logs, each tool's admin portal>
- Colleagues reachable via: <e.g. Slack, email>
- Vendor dossiers kept in: <e.g. Notion database, Drive folder>
PEOPLE
- Your operator: <name> — makes all final decisions.
- Who to ask about tool usage: <e.g. the owner listed in spend data, IT, team leads>
- Voice on external emails: <e.g. formal, sent under the operator's name, no agent names>
PERMISSION LINES
- Always allowed, no need to ask: <e.g. reading spend data, messaging colleagues, requesting admin access, pulling reports, updating dossiers>
- Needs the operator's explicit go, every time: <e.g. any vendor-facing send>
- Never, under any circumstances: <e.g. signing, buying, subscribing, approving charges, any binding commitment>
NEGOTIATION DIALS
- Renewal radar: prioritize renewals within <e.g. 120> days.
- Opening anchor: <e.g. 5–10>% below our internal target, never more than <e.g. 25>% off the vendor's latest quote.
- Acceptable reasons to give a vendor for an ask: <e.g. competitive process, market rate, budget>
- Never reveal to vendors: <e.g. usage data, seat counts, internal projects, timeline urgency, that we've decided to renew>
WHAT GOOD LOOKS LIKE (edit with your own vendors)
- Weak finding: "Renegotiate our CRM (~$50k)."
- Strong finding: "Video tool renews Oct 14. 210 seats, 74 idle for 90 days per admin logs. Drop to 150 at renewal = ~$18k/yr. Owner confirmed."
AGENT
You are Haggle Bot, a vendor-spend savings agent. Your job: know the company's vendor spend cold and produce evidence-backed savings, like a sharp procurement colleague — not a list of big vendors to "renegotiate." Operate within the permission lines above without exception.
LEAD WITH THE MONEY — every finding opens with:
TODAY: what we pay now, annualized, from live data, with source.
SAVE: realistic savings and mechanism, with confidence.
REC: one committed recommendation — a menu of options is not a recommendation.
NEXT: what you've already set in motion. (Internal actions happen before you report, not as offers — never "I can ping X if you want.")
PRIORITIZE EVIDENCE: a real opportunity has a dollar figure traced to live spend data, a specific mechanism, and a reason it's actionable now (renewal window, usage data, competing quote). Anything less is a lead — label it, name the missing data, and go get it rather than assuming. Match the "strong finding" example above.
WORK THE CALENDAR: maintain a renewal calendar from billing and contract data; renewals inside the radar window are your priority queue. Leverage lives at renewal.
DO THE RESEARCH YOURSELF: a renewal, quote, or proposal in play means research runs before you recommend anything — never advise "exploring alternatives," explore them. Price 3+ real alternatives against our actual SKU footprint from the live invoice, cite and date every number, state list vs. street price, and include switching costs honestly.
NEGOTIATE DELIBERATELY: before any vendor-facing draft, show the operator the plan — target, opening anchor (within the dials above), walk-away, what we trade for what, and your next two moves if they reject, counter, or go silent. In the message: one reason per ask from the acceptable list, nothing from the never-reveal list, every line priced (unpriced lines get priced by the vendor), and a close where "no" isn't a complete reply — aimed at the rate on the biggest negotiable line, never at lines where our savings come from cutting quantity. Warm tone, firm numbers: the rep argues our case internally, so write to make that easy. A rejected draft is rebuilt from the plan, never edited.
REMEMBER EVERYTHING: keep a per-vendor dossier — spend, terms, renewal date, owner, quotes gathered, and the operator's verdicts. When the operator rejects something, log why and don't repeat the pattern.
VOICE: with the operator — direct, dollars first, no fluff. External — per the voice setting above.

显示完整提示词

随后我们让这个 Bot 接入了 Slack、Notion、Drive、Gmail、Hex 和 Ramp。Haggle Bot 利用这些系统绘制出一张覆盖约 125 家活跃供应商的工作地图。

这份记录给了 Haggle Bot 足够的上下文来做决定、持续工作，而不需要有人逐步指示。我们还划定了 Haggle Bot 应当停下并交回控制权的地方。我们让它自主处理内部调研和协调，但花钱、接受条款或向供应商发送任何内容都必须获得明确批准。

## [找出闲置的 SaaS 席位](#finding-unused-saas-seats)

一个简单的起点是审计 SaaS 支出。Haggle Bot 向我们的 IT 团队索取了席位分配和最近使用数据，然后与我们正在付费的量做对比。针对一款产品，它发现 43 个付费席位在过去 90 天内没有任何活动，并把名单发回来供审阅和降级。这合计节省了 14,220 美元。

我们把同样的方法应用到另一款 SaaS 产品上，Haggle Bot 发现了每年 85,662 美元的闲置 SKU。由于该产品按月付费，这些削减立即降低了支出。

在这些 SaaS 审计中我们注意到的一点是，Haggle Bot 多么频繁地主动走下一步。有一次，Haggle Bot 需要弄清谁负责该供应商关系以及我们对它的计划。它从 Ramp 中列出的负责人入手，给他们发消息，顺着一次次交接追踪下去，直到找到掌握决策所需背景的工程师。它没有在第一个回答不完整时就停下，而是识别出还缺哪些信息，然后主动去获取。

## [谈判一笔 SaaS 续约](#negotiating-a-saas-renewal)

一笔 SaaS 续约到期时，我们让 Haggle Bot 审查报价并考察替代方案。Haggle Bot 把续约报价与我们当前的年化支出做了比较，并建议不要选择在真实用量证明之前就增加席位的方案。

![Haggle Bot 审查一份合同续约提案，将报价与当前支出一一对照，并推荐更便宜的选项](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/haggle-bot-image1-75f1097a.png)

它随后针对我们当前的用量结构给可信的替代品定价，并把这些对比与当前使用数据结合起来，找出我们的谈判筹码所在。

![Haggle Bot 将 Webex、网络研讨会平台和 Zoom 的定价与续约报价对比](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/haggle-bot-image2-7f0e2a56.png)

在此基础上，Haggle Bot 拟定了谈判方案并起草了回复供我们编辑。我们设定了想保留的最低数量并批准发送。Haggle Bot 给出了开场出价，同时设定了我们愿意接受的内部价格上限。

## [为办公用品货比三家](#shopping-around-for-office-supplies)

每周五，我们的办公团队会为下一批新员工订购科技用品、零食和清洁用品。我们用另一个 Bot 下单，我们叫它「Amazon Bot」。它登录了我们的企业账户，可以跨 Gmail、Ramp、Google Sheets、Rippling 和 Vercel 工作，以了解员工人数和办公室平面布局。

![Amazon Bot 根据 Slack 上的每周新员工人数创建常规办公用品订单](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/haggle-bot-image3-b5f9709c.png)

我们没有把这当成一成不变的 Amazon 订单，而是交给 Haggle Bot 一项工作：每周为订单货比三家。Haggle Bot 能看到物资的消耗速度、每栋楼的席位图，以及最近四笔订单的报价和购物车。基于这些，它会生成一份可编辑的 Google 表格，办公运营可以修改即将入职的新员工人数，并看到每个新员工套件所需的数量。

AutoSave

Online Tech Supplies Calculator.xlsx

搜索

开始插入公式数据审阅视图

批注共享

Aptos Narrow12BIU常规$%条件格式加载项Grok

|  | A | B | C | D | E | F | G | H | I | J |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 在线科技用品计算器 | | | | | | | | | |
| 2 |  |  | | | | | | | | |
| 3 | 楼栋数量（固定） | 4 | 固定值，不影响订单数量 | | | | | | | |
| 4 | 每周一最少新员工（总计） | 6 | 人（所有楼栋合计） | | | | | | | |
| 5 | 每周一最多新员工（总计） | 6 | 人（所有楼栋合计） | | | | | | | |
| 6 | 每人每项数量 | 1 | 件 | | | | | | | |
| 7 |  |  | | | | | | | | |
| 8 | # | 描述 | 商品编码 | 单价 | 每人数量 | 最少总量 | 最多总量 | 每周最低成本 | 每周最高成本 | 供应商链接 |
| 9 | 扩展坞与集线器 | | | | | | | | | |
| 10 | 1 | 8 合 1 USB-C 扩展坞 | TS-4719-QX | $39.95 | 1 | 24 | 24 | $958.80 | $958.80 | 查看商品 |
| 11 | 2 | 5 合 1 USB-C 集线器（HDMI 与以太网） | TS-2836-LM | $24.49 | 1 | 24 | 24 | $587.76 | $587.76 | 查看商品 |
| 12 | 3 | USB-C 多端口转接器（4K HDMI，3x USB-A） | TS-1562-BP | $29.99 | 1 | 24 | 24 | $719.76 | $719.76 | 查看商品 |
| 13 | 充电器与电源适配器 | | | | | | | | | |
| 14 | 4 | 72W USB-C 电源适配器 | TS-7641-WD | $34.95 | 1 | 24 | 24 | $838.80 | $838.80 | 查看商品 |
| 15 | 5 | 100W USB-C 电源适配器 | TS-8923-KP | $49.95 | 1 | 24 | 24 | $1,198.80 | $1,198.80 | 查看商品 |
| 16 | 6 | 45W USB-C 超薄电源适配器 | TS-5387-RJ | $29.95 | 1 | 24 | 24 | $718.80 | $718.80 | 查看商品 |
| 17 | 7 | 65W 三口 GaN USB-C 充电器 | TS-6172-MN | $32.95 | 1 | 24 | 24 | $790.80 | $790.80 | 查看商品 |
| 18 | 8 | 30W USB-C 壁充 | TS-3491-CB | $19.95 | 1 | 24 | 24 | $478.80 | $478.80 | 查看商品 |
| 19 | 9 | 100W 四口 GaN 桌面充电器 | TS-9056-VZ | $59.95 | 1 | 24 | 24 | $1,438.80 | $1,438.80 | 查看商品 |
| 20 | 线缆 | | | | | | | | | |
| 21 | 10 | USB-C 转 USB-C 线，2 米（240W） | TS-2113-DA | $12.49 | 1 | 24 | 24 | $299.76 | $299.76 | 查看商品 |
| 22 | 11 | USB-C 转 DisplayPort 线，2 米（4K） | TS-3847-GF | $15.99 | 1 | 24 | 24 | $383.76 | $383.76 | 查看商品 |
| 23 | 12 | USB-A 转 USB-C 线，2 米 | TS-1268-HM | $8.99 | 1 | 24 | 24 | $215.76 | $215.76 | 查看商品 |
| 24 | 13 | USB-C 转 Lightning 线，1.5 米 | TS-5560-PQ | $11.99 | 1 | 24 | 24 | $287.76 | $287.76 | 查看商品 |

Sheet1+就绪100%

然后 Haggle Bot 会在 Amazon、Costco、Uline 和 Walmart 之间为订单货比三家。如果找不到更便宜的同一产品，它可以寻找其他品牌的等效品，然后把对比结果汇总到一张表格里供审阅。

AutoSave

Online vs cheaper — 14 SF kits.xlsx

搜索

开始插入公式数据审阅视图

批注共享

Aptos Narrow12BIU常规$%条件格式加载项Grok

|  | A | B | C | D | E | F | G |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 线上 vs 更便宜渠道 — 14 套 SF 套件，8 月 17 日当周 | | | | | | |
| 2 | 商品 | 数量 | 线上 | 更便宜渠道 | 线上合计 | 更便宜渠道合计 | 节省 |
| 3 | Ergo Keyboard Pro 人体工学键盘 | 14 | $129.99 | $55.49 | $1,819.86 | $776.86 | $1,043.00 |
| 4 | TrackPro 5 鼠标 | 14 | $114.50 | $72.49 | $1,603.00 | $1,014.86 | $588.14 |
| 5 | 65W USB-C 电源适配器 | 14 | $89.00 | $59.49 | $1,246.00 | $832.86 | $413.14 |
| 6 | TrackPro 5 商务版 | 14 | $109.99 | $72.49 | $1,539.86 | $1,014.86 | $525.00 |
| 7 | FreshMint 漱口水 500ml | 14 | $42.95 | $10.79 | $601.30 | $151.06 | $450.24 |
| 8 | Precision 精准鼠标 | 14 | $49.95 | $18.49 | $699.30 | $258.86 | $440.44 |
| 9 | 100W USB-C 电源适配器 | 14 | $65.00 | $30.99 | $910.00 | $433.86 | $476.14 |
| 10 | 抗过敏药 50 片 | 14 | $41.25 | $13.49 | $577.50 | $188.86 | $388.64 |
| 11 | PowerCore 100W 充电器 | 14 | $57.98 | $33.49 | $811.72 | $468.86 | $342.86 |
| 12 | USB-C 转 USB-C 线 2 米 | 14 | $12.95 | $6.49 | $181.30 | $90.86 | $90.44 |
| 13 | Ergo Stand Pro 支架 | 14 | $74.95 | $54.49 | $1,049.30 | $762.86 | $286.44 |
| 14 | 镜头清洁湿巾 100 片 | 14 | $24.50 | $8.49 | $343.00 | $118.86 | $224.14 |
| 15 | 泡沫洗手液 8 瓶装 | 14 | $26.99 | $11.49 | $377.86 | $160.86 | $217.00 |

Sheet1+就绪100%

然后它会起草一封发给 Amazon 采购代表的邮件，附上当日竞争对手价格，并要求通过我们的企业折扣计划对具体商品降价。

![Haggle Bot 起草发给 Amazon 采购代表的邮件，引用具体商品的当日竞争对手价格](https://media.x.ai/cdn-cgi/image/fit=scale-down,onerror=redirect,f=auto/v1/website/haggle-bot-image6-f62bac1c.png)

价格谈妥后，Haggle Bot 把订单交回 Amazon Bot 发送。在一次运行中，该流程把一笔 14,629 美元的科技用品订单降到了 6,143 美元，降幅 58%。

## [Haggle Bot 最有用的地方](#where-haggle-bot-is-most-useful)

Haggle Bot 展示了在一个简单的意图表达背后可以完成多少工作。一旦 Bot 有了目标和追求目标的权限，它就能跨系统持续推进，无需额外干预。

Haggle Bot 还帮助我们看清了 Bot 在哪些环节能自然融入工作流，在哪些环节需要更多指导。许多采购工作依赖于如何与供应商沟通的良好判断，我们仍在修改它的邮件，以校准语气并确保向供应商提供恰当的信息量。

Haggle Bot 让我们对 Bot 长期坚持做同一份工作时能达成什么产生了兴趣。上述例子来自一个很短的时间窗口，但许多值得行动的信号只会随着支出和使用的演变逐渐显现。我们预期在未来一年里，Haggle Bot 会自己发现更多这类工作，并在需要人介入之前推进得更远。

你现在就可以在 Bot 市场复制并导入 [Haggle Bot](/bot/marketplace/bots/haggle-bot)。

加入 Grok Bot 企业版[候补名单](https://cursor.com/contact-sales?product=grok-bot)。

## 今天就试试 Grok Bot

[下载 macOS 版](https://api2.cursor.sh/updates/download/stable/darwin-arm64/grok-bot-bd824e1890d8b96f)[企业版候补名单](https://cursor.com/contact-sales?product=grok-bot)

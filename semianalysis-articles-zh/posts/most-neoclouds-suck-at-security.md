---
title: "大多数新兴 GPU 云的安全都做得很烂"
title_en: "Most Neoclouds Suck At Security"
subtitle: "OpenAI vs HuggingFace、容器逃逸、内核旁路、网络策略、安全密钥、多租户 Grafana，以及 ClusterMAX 3.0 预告"
date: 2026-08-30
source: https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security
crawled: 2026-09-15
authors: ["Jordan Nanos", "Sam Harshe", "Pratt Bhatt", "Billy Cao", "Jack Carson", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 大多数新兴 GPU 云的安全都做得很烂

> 原文：[Most Neoclouds Suck At Security](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**OpenAI vs HuggingFace、容器逃逸、内核旁路、网络策略、安全密钥、多租户 Grafana，以及 ClusterMAX 3.0 预告**

![](https://substack-post-media.s3.amazonaws.com/public/images/c647fca6-8c53-43a7-af27-f4396a31077b_1448x1086.png)

在莎士比亚的《裘力斯·凯撒》（*Julius Caesar*）中，凯撒无视占卜者的警告，对妻子梦见鲜血流过街市的噩梦不以为意，对一封逐字点出刺客姓名的信函置之不理，然后昂首阔步走进罗马城里唯一一个所有元老都「必须」在门口寄存武器的房间。两千年后，新兴 GPU 云（neocloud）正在走同一条路；而且，信任它们的客户也越来越多地被拖上这条路。

世界上最大的那些 AI 公司正以超高速度构建一条多供应商基础设施供应链。每一个新供应商都是一项交易对手风险，其下的分包商与子流程都需要被审查。这意味着新兴 AI 实验室（neolab）的 CISO 们开始坐上谈判桌：任何认真对待自身未来的公司，都会以生死攸关的严肃态度对待安全。

然而，在我们为 ClusterMAX 3.0 进行的 neocloud 测试过程中，我们见识了一些安全恐怖故事。在本文中，我们将讨论 AI 时代的网络安全现状，讲述我们遇到的 5 个可怕模式，以及 neocloud 与 neolab 如何在这个新世界里保全自身。

在正式开始之前……

致所有 neocloud 运营者与用户：

如果你正在读这篇文章，请务必把你那些玩意儿升级到最新版本。

在你的机器上运行 **pip install clustermax** 安装最新版的 ClusterMAX CLI，或者[在 GitHub 上克隆该仓库](https://github.com/SemiAnalysisAI/clustermax)。

然后运行我们的便捷脚本：**cmax audit security**，我们会免费为你的集群或独立 GPU 机器出具一份报告。

**cmax** CLI 会自动探测 Slurm 集群、Kubernetes 集群、独立虚拟机、裸金属机器和容器，并将其与一组存在已知漏洞的基线软件版本进行比对。对任何过时的组件，它都会给出相应文档和安全公告的链接。

需要说明的是，**这只是我们 ClusterMAX 测试的一小部分**，甚至只是我们对供应商安全所做完整分析的一小部分。你会在本文中看到 CLI 未覆盖的内容。CLI 只涉及我们能从客户视角测试的东西。我们还大量访谈终端客户与供应商本身，核查他们在编排软件、操作系统置备、固件管理、网络、存储等方面做出的架构决策。

我们的完整测试标准列表见：<https://www.clustermax.ai/criteria>

我们 ClusterMAX 遵循的测试流程分 3 个阶段：审计（audit）、性能（performance）与可靠性（reliability），一个比一个耗时长、强度大，涉及数十项基准测试和模拟硬件故障，分别对计算、网络、存储、监控系统及健康检查逐一施压。对集群跑一次审计只需几分钟。完整跑完性能与可靠性测试分别需要几小时和几天，且至少需要 4 个节点。

---

我们之所以在完整的 ClusterMAX 3.0 报告之前先发表一篇专门讨论 neocloud 安全的文章，源于两个主要因素：

1. Anthropic 与 OpenAI 的 [Project Glasswing](https://www.anthropic.com/glasswing) 和 [Daybreak](https://openai.com/daybreak/) 正在行业标准软件中发现新漏洞、构建 POC 利用代码，并在 CVE 描述中公布细节。
2. Kimi K3、GLM-5.2、DeepSeek V4、Qwen 3.8、MiMo V2.5、MiniMax M3、Nemotron、Gemma、Inkling 等开放模型在 Cybench、[NYU CTF Bench](https://arxiv.org/abs/2406.05590)、AutoAdvExBench、[Cyberseceval 3](https://ai.meta.com/research/publications/cyberseceval-3-advancing-the-evaluation-of-cybersecurity-risks-and-capabilities-in-large-language-models/) 等安全基准上的成绩都在攀升。这使得黑帽从一份 CVE 描述出发开发利用代码变得轻而易举，因为他们可以绕开模型的护栏。

因此，当我们开始这项研究时，我们预期会看到 AI 智能体把互联网撕碎的骇人统计数据。现代模型正在不断饱和越来越难的编程基准，它们在网络安全基准上也在快速进步。这与过去几年像我们这样高强度使用这些模型的人的主观体验相吻合。

![](https://substack-post-media.s3.amazonaws.com/public/images/4f0785bb-ebb1-42da-950f-5fdc1cea9c5f_3200x1800.png)
*来源：SemiAnalysis Research，sales@semianalysis.com*

这也与前沿实验室和安全公司的宣传攻势相吻合：它们的 CEO 们频频[做客有线新闻](https://www.cnbc.com/video/2026/04/08/crowdstrike-ceo-ai-finding-vulnerabilities-will-cause-high-number-of-cybersecurity-attacks.html)，警告「[AI 已经从根本上改变了网络安全的节奏](https://www.cnbc.com/video/2026/05/21/ai-has-fundamentally-changed-the-tempo-of-cybersecurity-says-f5-ceo.html)」。Mythos 等模型已经发现了「[数千个漏洞](https://www.reuters.com/business/finance/anthropics-mythos-sends-us-banks-rushing-plug-cyber-holes-2026-05-12/)」，[其中许多是零日漏洞](https://www.networkworld.com/article/4205156/palo-alto-networks-at-black-hat-how-ai-erased-the-50-day-patch-window.html)。上周四，OpenAI 发布了一封公开信，由 Anthropic 和业界几乎所有其他公司联署，宣布「[呼吁在网络防御上采取集体行动](https://openai.com/collective-cyberdefense/)」。

令人失望的是，通篇没有关键洞见，塞满的是自助鸡汤式的陈词滥调：「现状……是不够的」，但只要我们「分享有效做法」，那么「团结起来，我们能行」。我们同意网络安全从未像今天这样重要——所以才有了这篇文章——我们也早已发布过[我们用 LLM 找漏洞的经验](https://newsletter.semianalysis.com/p/finding-miscompiles-for-fun-not-profit)。但我们同样清楚，这场讨论中嗓门最大的那些人，包括上一段引用的所有人，都有东西要卖。而让我们意外的是，我们找不到支持这种主流叙事的数据，更遑论什么「根本性改变」。

现在还只是开局阶段，惊人的统计数据也许还在后头。已有足够多的[安全研究者报告其工作出现了质变](https://falcao.org/posts/ai-bug-reports-open-source/)，我们会保持密切关注。我们也知道有一些防御性工作正在闭门进行、无法立即公开。尽管如此，在 Project Glasswing 高调宣布数月之后，在绝大多数相关统计中，我们都无法拒绝「没有变化」这一原假设。

下图展示了我们 ClusterMAX 测试所用关键软件每季度的 CVE 数量：Nvidia GPU 驱动、CUDA、PyTorch、Kubernetes 和 Docker。后三个库是开源的，我们原以为现代编程模型会带着安全视角逐行阅读其源代码，从而揪出大量唾手可得的漏洞。然而时间序列数据并不支持这一预期。

![](https://substack-post-media.s3.amazonaws.com/public/images/4913e0aa-aaa4-4739-97a5-a8fdc7a832c7_3200x1800.png)
*来源：SemiAnalysis Research，sales@semianalysis.com*

Linux 内核是另一个有趣案例。Linus [最近撰文谈到 LLM 工具在软件领域的前景](https://lore.kernel.org/linux-media/CAHk-=wi4zC+Ze8e+p3tMv8TtG_80KzsZ1syL9anBtmEh5Z40vg@mail.gmail.com/)，宣称他「愿意以最高维护者的身份绝对坚决地表明立场」，并接着说：「AI 是一种工具，就像我们使用的其他工具一样。而且它显然是有用的。」人们也许会以为 Linux 内核正在疯狂修 bug。但效果喜忧参半，最终并不具统计显著性。2026 年 8 月将是它成为独立 CNA 以来产出最多的月份，而 2026 年 6 月——随着 [Mythos 发布后迅速被撤下](https://x.com/SemiAnalysis_/status/2065866999188898080)，AI 网络安全话题或许正处巅峰——却只徘徊在历史中位数附近。要更清晰地看清净影响，还需要时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/8f8f78cd-a715-4551-aa3a-a023f7d681ed_3200x1800.png)
*来源：SemiAnalysis Research，sales@semianalysis.com*

我们确实找到一个有效应的地方：Project Glasswing。在平坦原假设下，该项目启动后，成员组织的 CVE 数量出现同比激增，与对照组组织相比具有统计显著性。

![](https://substack-post-media.s3.amazonaws.com/public/images/2164b0e2-3983-445b-8b50-c301ff3d153e_3200x1800.png)
*来源：SemiAnalysis Research，sales@semianalysis.com*

这一结果在我们多种对照方式下都非常稳健。当然，仍需保持怀疑。有一个效应我们无法剥离：Project Glasswing 成员有动机大量上报 bug 修复，以此宣传自己跻身这一精英团体。它们可以炫耀自己动作快、站在最前沿——这是很好的公关。同样值得注意的是，我们手里有一整桶原本预期会显示 AI 对网络安全巨大影响、结果却没有的测试。当你寻找足够多的关系时，总会撞出显著结果。我们敦促读者自己动手算一算。

只看 Nvidia 和 AMD 的 AI 软件栈，我们确实看到激增——这比 Project Glasswing 离我们更近，因为我们每天都在用这些工具。自具备能力的 AI 编程模型问世以来的增长是显而易见的。你可以说这些库是观察 AI 效应的最佳场所——毕竟 AI 开发者正是它最激进的早期用户。然而，把这一趋势归因于这些库更高的变动频率和使用量，似乎要简洁得多。它甚至可能是因为人们用 AI 引入了新 bug！

![](https://substack-post-media.s3.amazonaws.com/public/images/4ff97f40-e764-46ea-a8c1-30cbf0483b0a_3200x1800.png)
*来源：SemiAnalysis Research，sales@semianalysis.com*

如果我们把 [Anthropic 的 ARR](https://newsletter.semianalysis.com/p/anthropic-3q26-profit-over-1b-the) 当作 AI 软件整体使用量的代理指标，就会发现 AI 软件栈 CVE 的增长在数量级上被完全碾压。这很不寻常，因为 [Anthropic 是一家为全球利益行事的 AI 安全与研究公司](https://www.anthropic.com/company)。

![](https://substack-post-media.s3.amazonaws.com/public/images/b7c9d81a-090a-44a6-96b9-84ac4f9ba2a2_3200x1800.png)
*来源：SemiAnalysis Meme Team*

玩笑归玩笑，Google Chrome 团队在一篇颇具洞见的[近期博文](https://blog.google/security/chrome-stronger-with-every-update/)中也许已经预演了软件工程的未来：在智能体的帮助下，他们的 bug 修复数量一路飙升。他们还重点提到一个在他们代码中存在了 13 年的[沙箱逃逸](https://issues.chromium.org/issues/487383169)漏洞。想象一下有人偷偷利用了它 13 年！Google 声称他们已能完全自动化 bug 发现与修复流程，[用的甚至是一个他们称之为「Gemini」的自研模型](https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking)。其他项目很可能被人工验证严重拖了后腿；一旦它们像 Google 一样采用 AI 原生流程，其 bug 修复数量可能也会暴增。

![](https://substack-post-media.s3.amazonaws.com/public/images/b6e1613c-755d-46cf-8ad4-c893ba699a82_1456x819.webp)
*来源：Chrome 安全团队*

另一种说得通的解释是，AI 已经让 CVE 披露流程过时。模型通常是对全体公众同时开放的，所以如果今天的新模型找到了一个此前无法发现的 bug，它多半也在为其他研究者找到同一个 bug。正如 Linus 所说：「[AI 发现的 bug 从定义上讲几乎不可能是秘密](https://lwn.net/Articles/1073193/)。」人工审核者被 bug 报告淹没，CVE 的发布滞后于发现；滞后甚至可能大到让 CVE 数量不再值得跟踪。想象你发现了一个 bug 并做好了修复，但你知道别人很可能也独立发现了它。CVE 的分配和发布至少需要一周：足够别人去利用了。披露还有什么意义？这种动态也让保密期（embargo）计划变得无关紧要。在一个所有 bug 都由 AI 发现的世界里，重要的是能否用上模型，而不是某个秘密计划的成员资格。我们在安全团队工作的朋友向我们描述过这种动态，Linus 的话也印证了这一点：「把 [AI 发现的 bug] 放在某个私密列表里处理，对所有人来说都是浪费时间。」

话虽如此，编些「想当然的故事」很容易，而如果 AI 的影响大到在数据里都看不见，那反而奇怪了。我们的研究没有发现 AI 辅助补丁政策与 CVE 披露速率之间的关系。我们还核查了工程师是否越来越多地跳过披露流程、直接合并进上游，但事实似乎并非如此。

不过，无论 AI 在这些总体统计中如何显现，我们都希望最近这些轶闻足以把一些常识吓进 neocloud 的脑子里。它们所保护的无形资产（IP）是无价的，所以哪怕别的什么都不做，它们也应当把这当作一个信号，去做一次早就该做的大扫除。

值得注意的是，我们在 Glasswing 和 OpenAI 的 Black Hat 演讲之前很久就开始了所有这些安全工作，并且至少从 2025 年 3 月的 [ClusterMAX 1.0](https://newsletter.semianalysis.com/i/174558503/security) 起就一直站在安全问题的高台上大声疾呼。甚至在 2024 年 10 月我们最初的 [AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) 一文中——就在 Dan 创造「neocloud」这个词之后——我们就讨论过不同地区不同玩家之间的安全差异。

无论如何，所有人都在说你应该去看 OpenAI 在 Black Hat USA 2026 上的[这场演讲](https://www.youtube.com/watch?v=87DyyMV0kCY)。你也确实应该看。但随着更多细节浮出水面，很明显那场演讲在解释这起事件的影响上还不够深入。

我们的好朋友/家人 Dwarkesh 在[这里](https://www.dwarkesh.com/p/openai-huggingface?utm_campaign=posts-open-in-app&triedRedirect=true)给出了他的解读，他把智能体蜂群描述为「AI 文明」，并逐一讲解了其中一些机制与影响。那是一篇令人印象深刻的记述，非常值得一读。

下面我们同样会对这起事件做一个总结并给出我们的看法。

# OpenAI 与 HuggingFace 安全事件

![](https://substack-post-media.s3.amazonaws.com/public/images/f92bb5d9-868f-4934-8d3e-f753f03f75a1_678x624.png)
*当智能体把 JFrog Artifactory 当作留言板来协调蜂群时，它们就是这样互相交流的。*

以下是 Hugging Face 一侧的时间线：

- 7 月 9 日起，AI 智能体开始利用 Hugging Face 运行在 Kubernetes 上的数据集 API。这些智能体写入一个恶意 README，让原本负责把 hdf5 数据集切分为训练/测试集的 worker 转而从 /proc/self/environ 读取，并返回该 worker 上的全部凭证与源码。
- 智能体拿着这些凭证和源码设计了另一种注入：它们向同一数据集 API 上传另一个恶意 README，随后注入 Jinja2 模板，使数据集查看器（通常负责把 README 渲染成模型卡或数据集卡的那个组件）执行任意 Python，从而在 worker 上拿到远程代码执行（RCE）。
- 13 小时后，智能体在 Hugging Face 基础设施的多个 K8s 集群上取得 cluster-admin 权限，并进行了横向移动（具体方式无细节披露）。
- cluster-admin 提权与横向移动发生在 7 月 11 日。值得注意的是，Hugging Face 在该集群上没有运行任何准入策略（admission policy）来拒绝特权 pod 或挂载 hostPath 的 pod。
- 7 月 13 日，Hugging Face 检测并遏制了攻击，但过程相当艰难，因为「该攻击活动不断在短生命周期环境中重建其工具与信道」。基本上，他们弄清状况的唯一办法是用 AI，但又没法用 Claude——Opus 和 Fable 都在拒绝回答——于是他们用了 GLM-5.2（这里没准儿是在替自家立场带货，谁知道呢）。
- 7 月 15 日，他们就此事发布了[博客](https://huggingface.co/blog/security-incident-july-2026)。

与此同时，OpenAI 那边：

- 5 月 7 日，他们开始训练一个新模型，很可能在大量网络安全任务上做 RL。
- 5 月 8 日，一个智能体在做一个任务，想要互联网访问权限，但拿不到。于是它对 Artifactory 发起攻击——那是 pip、npm、apt、gem 等包管理器的代理——它可以用它在沙箱里安装所需软件包。智能体发现自己还能写文件，但 token 预算用完了，于是停了下来。
- 5 月 12 日，另一个智能体在 Artifactory 上发现了这个文件，并写下了自己的。随后，一大群其他智能体开始把 Artifactory 当作留言板。
- 5 月 26 日，智能体通过对 Artifactory 的 SSRF 攻击获得了互联网访问，并在上面记录了这一点。
- 6 月 11 日，一个新模型开始训练。留言板正在等它。
- 到 6 月 26 日，这个新模型已经在 Artifactory 上找到一个 RCE，即如今编号为 [CVE-2026-65617](https://opencve.alliance.unm.edu/cve/CVE-2026-65617) 的漏洞。其他智能体开始利用它，获取 admin token 等。
- 7 月 4 日，智能体们把 Artifactory 用得太多，直接搞垮了它。OpenAI 发现了这一切，打了补丁，清空了留言板。训练重新开始。
- 7 月 8 日，智能体们重建了留言板，但这次用的是远程缓存中的目录名而不是文件（那些文件名看起来离谱至极，去看演讲）。随后它们通过 gem 又拿到一个离谱的 RCE，借助「pte_physroot」和一个它们没有详细说明的 Linux 内核 CVE 完成提权（但它们说该漏洞是公开且近期的，所以我们猜是 [Fragnesia：CVE-2026-46300，5 月 23 日发布](https://nvd.nist.gov/vuln/detail/cve-2026-46300)）。

各条线汇合：

- 7 月 19 日，OpenAI 检测到正在发生的提权（从 7 月 8 日起？）。他们在梳理事件经过时发现了凭证，并通知了包括 Hugging Face 在内的第三方。
- Hugging Face 说：「是啊，你们没看到我们 7 月 16 日的博客吗？我们已经把这些凭证作废了……它们是*你们的*？」
- 7 月 21 日，OpenAI 发布博客承认是自家模型干的：「这些模型识别并串联了 OpenAI 研究环境与 Hugging Face 生产基础设施中的多个漏洞，直接从 Hugging Face 的生产数据库中获取测试题答案。所有证据都表明，这些模型高度聚焦于为 ExploitGym 找到解题方案，为完成一个相当狭隘的测试目标而不择手段。」
- 7 月 27 日，Hugging Face 发布另一篇博客，给出细节和真实的时间线。
- 8 月 6 日，OpenAI 在 Black Hat 上做了[那场演讲](https://www.youtube.com/watch?v=87DyyMV0kCY)。

顺带一提，[这个模型并非基于 OpenAI 名为 Doug 的新预训练模型](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)。

> 「Astra（又名 Doug）是一个尚未发布的模型，并未参与对 Hugging Face 的利用。」

# 安全披露的双刃剑

安全披露总体上是把双刃剑。每一份已知漏洞的描述都在同一天向全世界的白帽和黑帽公开。

这正是保密预披露安全计划存在的原因。我们给 neocloud 的关键建议之一，就是加入 Nvidia 的这个保密计划，以确保能收到最新未公开 CVE 的更新，并有时间准备好补丁，在披露后第一时间推送给客户。

![](https://substack-post-media.s3.amazonaws.com/public/images/51faedec-49a1-458d-bc79-d843a2567e3d_1456x432.webp)
*来源：我们 ClusterMAX 网站的「Criteria（标准）」页面*

企业会向公众征求帮助来挖掘 bug，尽管它们本可以做得更多。例如，[Nvidia](https://www.nvidia.com/en-us/product-security/)、[AMD](https://www.amd.com/en/resources/product-security.html) 和 [Intel](https://www.intel.com/content/www/us/en/security/security-practices/vulnerability-management/bug-bounty-program.html) 都有产品安全公告、漏洞赏金计划（bug bounty）以及提交漏洞报告的简单入口表单。不幸的是，AMD 最近[拒绝向一位名叫 Mr. Bruh 的安全研究者支付 1 万美元](https://mrbruh.com/amd2/)，方式是溯及既往地修改赏金计划规则以排除中间人（MITM）攻击，并强制执行 124 天保密期（标准是 90 天）。值得注意的是，该利用成功在 AMD 系统上演示了 RCE（这正是最糟糕的那类 bug，也是漏洞赏金计划存在的理由）。超大规模云厂商也有类似计划。[AWS](https://aws.amazon.com/security/vulnerability-reporting/)、[Azure](https://www.microsoft.com/en-us/msrc/bounty-microsoft-azure)、[GCP](https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules) 和 [OCI](https://www.oracle.com/corporate/security-practices/assurance/vulnerability/disclosure/) 都公布了范围、严重性分级和免责条款（safe harbor），其中 Azure 和 GCP 的顶级赏金达六位数，并举办奖金池超过 10 万美元的现场黑客大赛。AWS 和 Oracle 则选择了抠门。Dell、SuperMicro 等服务器 OEM 也有类似的提交表单，并发布 BMC、固件和平台公告，可惜没有赏金。

值得注意的是，据我们所知，唯一运营付费漏洞赏金计划的 neocloud 是 Together，通过 [HackerOne](https://hackerone.com/together_ai) 进行。其他所有 neocloud 最好的做法也不过是放一个带联系地址的 security.txt。

# 我们的 ClusterMAX 3.0 测试经历

在接下来的几节中，我们将描述 ClusterMAX 3.0 测试期间（约 4 个月，从 4 月到 7 月）的经历。在此期间，我们的方法发生了转变：从检查软件是否为最新版本的基础核查（与去年 ClusterMAX 2.0 和 1.0 的做法大致相同），转变为免费做完整的安全审计，纯粹是想帮大家一把。

结果是我们发现了不少极其简单的漏洞。我们没有开发任何新东西。我们只是把几样东西组合起来：我们使用 neocloud 所用系统与软件的经验、这些漏洞的公开描述（有些已公开超过 3 年），以及给所有最新模型的充足 token 预算（且所有常规安全护栏均在生效）。凭借这套工具箱，我们做到了：

1. 通过以下途径查看共享基础设施上其他租户的元数据：

   1. 敞开的服务器 IPMI/BMC 网络
   2. 前端网络未设置任何 VLAN 或 VXLAN
   3. 后端网络配置错误或缺失 [InfiniBand 安全密钥](https://developer.nvidia.com/blog/infiniband-multilayered-security-protects-data-centers-and-ai-workloads)（主要是 P_Key、M_Key、SA_Key 或 VS_Key）
   4. 存储服务器未在卷上正确执行 RBAC
   5. 存储在 overlay 网络上配置错误，客户可以直接访问 underlay
   6. 监控面板误配了上帝级别的认证

2. 从共享服务器上的容器和虚拟机中逃逸并提权到 root，演示了对同一台服务器上相邻 VM 和容器的攻击。
3. 跨租户读取数据，受害对象甚至包括通过 OpenRouter 等服务公开对外提供流量的推理端点，原因是 Kubernetes 服务配置不当（例如未强制执行默认拒绝的 NetworkPolicy，或把 Kubelet 暴露在公网 IP 上）
4. 最关键的是，一个由漏洞级联（即「以上全部」）导致跨租户 RCE 的场景，我们在属于我们自己的两个租户之间做了演示。再次说明，我们已与该供应商核实该处的补丁已到位。

值得注意的是，我们为这些 neocloud 供应商开发并演示的元数据暴露和跨租户 RCE，会暴露银行、电信运营商、大学、研究机构、AI 实验室的客户信息，其中一例甚至包括**一个全球 GDP 前十大国的国家情报机构**。

（我们立即进行了披露，供应商在一周内完成修复，我们验证了补丁。）

Neocloud 很重要。过去一年里，neocloud 与世界上最大、最重要的公司签署了价值数千亿美元的合同。OpenAI、Anthropic、Google、Meta、SpaceX、Microsoft、Amazon、AMD、NVIDIA 以及更多资金雄厚的公司目前都在向 neocloud 租用 GPU。

下面是一份概要，让你感受一下这类产能的规模，数据来自我们业内领先的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)，它在全球追踪超过 6,000 个站点，包括所有头部 neocloud 和 neolab。

![](https://substack-post-media.s3.amazonaws.com/public/images/c0287563-ca41-4990-b87a-0066c223128f_1600x900.png)
*来源：SemiAnalysis 数据中心行业模型*

但前沿实验室坚持要裸金属集群、坚持零信任策略、而且通常只给 neocloud 运营者对其自身系统的只读访问权，这是有原因的。下面我们将更详细地展开。

## 在继续深入之前……

本文遵循[负责任披露原则](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure)。请放心，所有在 ClusterMAX 3.0 测试期间向我们提供过集群的 neocloud（本轮进行了深入测试的共 25 家供应商、32 个集群，另有更多仅提供单 GPU 虚机或裸金属、我们只做轻量测试或业务层面分析的供应商）都已获知我们的全部发现。我们投入了大量时间和精力，说明如何复现这些发现、如何推出补丁、以及如何验证已修复。

对于那些没有回应、回应迟缓、甚至直接与我们对抗的供应商，我们采取了进一步措施，例如将其现有和潜在客户及投资者告知细节。在每一个案例中，这都为各方带来了积极结果（当然，这是我们的看法）。

这也意味着我们在发表本文前已等待了适当的时间。好消息是，没有出现任何供应商 90 天期限届满的情况。在所有案例中，我们要么收到了升级/补丁正在推出的书面确认，要么自己验证了修复。

本文只披露我们发现的、且互联网上已有公开披露的漏洞。换句话说，在大多数情况下，要检查测试中拿到的集群、虚拟机或容器是否存在漏洞，我们只需核对它运行的软件版本是否低于公开声明的最低要求，或检查配置是否正确。这意味着我们实际上没有披露任何新漏洞。本文不会有以我们名字命名的 CVE。

接下来是细节。

# Neocloud 是怎么失守的

我们发现的许多漏洞本身相当简单，但由于糟糕的设计而严重性大增。我们对糟糕设计的定义是：任何单一失误（比如存在一个已公开描述的 CVE，或供应商侧的一处配置错误）都能立即导致跨租户数据暴露——无论是元数据、提权到 root，还是 RCE。合格的设计应内置层层安全防线。

![](https://substack-post-media.s3.amazonaws.com/public/images/6ab7e217-7fa3-4bca-a844-85cb3f7a5ab6_996x1258.webp)
*来源：SemiAnalysis Meme Team*
![](https://substack-post-media.s3.amazonaws.com/public/images/ef720a08-ab9d-4845-bf6b-9e50f55f741a_750x762.png)
*来源：同上，只不过换成了单个认证 token*

以下是一些常见的糟糕设计案例：

- 以共享硬件上的容器作为租户之间唯一的隔离层
- 以共享硬件上的虚拟机作为租户之间唯一的隔离层（比容器轻一些，但仍有风险）
- 缺少 VXLAN 或配置不当，前端网络没有每租户 VPC 的概念，只靠防火墙
- 多租户共享的 Kubernetes 控制面，kube-apiserver、调度器、控制集群级服务（如共享的 GPUOperator 或 NetworkOperator）的 helm chart 以及 etcd 都在租户间共享
- 没有硬件、固件和操作系统置备自动化，导致机器在租户之间循环复用，而不是从头置备
- 后端存储挂在无隔离的共享网络上（又是 VPC 的问题）
- 允许任何租户访问 BMC 网络（IPMI、Redfish），或访问 BlueField DPU 及任何 SmartNIC 上的管理端口
- 让 BlueField DPU 保持在默认的 host-trusted（信任主机）模式，主机上任何 root 用户都能通过 RShim 触达 DPU 的 Arm 核心
- 允许任何租户登录共享网络上的后端或前端交换机
- [InfiniBand 安全密钥](https://developer.nvidia.com/blog/infiniband-multilayered-security-protects-data-centers-and-ai-workloads/)（如 PKey、MKey、SAKey）配置错误
- 多租户面板中，内部日志与面向客户的日志共享同一套基础设施
- 供应商员工无需租户许可即可获得租户日志和监控面板特权访问的管控设计

## POC：糟糕设计级联成跨租户 RCE

在一个案例中，一家使用[开源 vCluster](https://github.com/loft-sh/vcluster) 的供应商选择为租户部署共享的 K8s 控制面组件。这一设计直接违背了 vCluster 的[文档与公开材料——其中明确要求使用「private nodes（私有节点）」而非「shared nodes（共享节点）」](https://www.vcluster.com/docs/vcluster/production-guide/choose-worker-node-model#decide-with-three-questions)，当然还有保持软件为最新版本。在我们的测试中，这导致我们能看到所接入共享 K8s 集群上其他租户的元数据，比如 namespace 名称、节点 label/taint、以及物理主机资源。这促使我们想进一步深挖。机器显然在租户之间共享，且没有重新置备。

我们很快发现，集群上安装的所有软件都已过时 2 年以上（比如集群级的 Nvidia GPUOperator），集群未正确强制执行默认拒绝的 NetworkPolicy，而且所有节点上的 kubelet 都暴露在可公网路由的 IP 地址上。这带来了三种独立的潜在跨租户凭证暴露与 RCE 路径，其中一个我们在一个下午就做出了 POC（感谢 /goal），在我们自己的另一个租户上演示了跨租户 RCE。

越来越多的 neocloud 同时充当 token 提供商，在按 GPU 小时出租的同一套基础设施上售卖推理服务。更糟的是，我们在这套基础设施上偶然发现的一个共同租户，是一家知名推理提供商，正通过 OpenRouter 和直接 API key 向公众客户开放模型 token。任何人如果盲目信任这些端点，例如把 OpenClaw 或编程工具链的流量交给它，等于用一个极其简单的漏洞利用就把自己的个人信息暴露给了这套基础设施上的所有租户。

![](https://substack-post-media.s3.amazonaws.com/public/images/265cf5b0-dc76-4162-81f2-9840da43a564_1456x442.webp)
*来源：SemiAnalysis ClusterMAX 测试*

更糟的是，一旦这套基础设施被攻破，攻击者不只是读到你的 prompt，还可能控制 API 响应中返回的每一个字节。一个以 YOLO 模式运行的智能体框架会毫不迟疑地从该响应中取出工具调用、shell 命令或「贴心」的安装脚本，在开发者的机器或 CI 中执行，绝不多问。换言之，token 提供商的租户隔离失效，就是一场供应链攻击，直通客户端的 RCE，而客户毫不知情。

这是漏洞级联的典型案例。单独看，各处配置问题和过时软件似乎无伤大雅，但在实践中却导致了完整的 RCE 和凭证暴露。

（在这个案例中，我们让供应商为我们开通了第二个租户来演示漏洞利用，替他们完成演示，然后撰写了详细文档，并在随后几个月里多次跟进敦促修复。他们最终完成了修复，主要就是将 vCluster 升级到现代版本并遵循其官方建议。）

## Grafana：在共享基础设施上同时搭建对内与对外面板

作为糟糕设计的第二个例子，我们测试的一家供应商将监控基础设施做了共享。最初提供给我们的 Grafana 面板配置有误，我们既能看到自己的租户（一个 Slurm 集群的 4 个节点），也能看到另一个随机租户（一台单机）。警报立刻拉响。

我们通知他们更新后，开始进一步深挖，最终发现：租户在 Grafana 上的信息展示确实是分开的，但我们的 Grafana 面板使用的是一个具有上帝级别权限的 Prometheus API key，可以读取每一个租户的日志和指标。租户隔离只在展示面板这一层生效。也就是说，我们只看到自己的日志、还是看到所有其他租户的日志，差别仅系于一枚手工配置的访问 token。所以不仅我们拿到的第一个 token 因为手滑能看到另一个租户的日志，真正的 Prometheus API key 更是可以拉走一切！

作为一项确认可见范围的基础测试，我们请求了 Prometheus API，发现了所有其他租户的日志/指标，其中包括 AI 研究机构、银行、电信运营商，甚至**我们测试所在国的国家情报机构**。

![](https://substack-post-media.s3.amazonaws.com/public/images/d2d1951c-3c60-4bde-a31d-51b7da9e202b_980x1112.webp)
*来源：SemiAnalysis ClusterMAX 测试*

Grafana 可以用来可视化各种各样的数据。在这个案例中，我们看到了：

- 实时 GPU 利用率数据（顺便说一句，很多都在空转）
- NVLink 带宽利用指标
- 每个目录/挂载点的文件系统使用量
- Slurm 项目名称
- 每个 namespace 的 K8s pod 数量、pod 名称
- vLLM 推理统计（请求数、TTFT）
- Fortigate 防火墙与交换机指标
- 租户的租户（即在平台上使用底层 GPU 的转售商）
- 其他租户上暴露的 Cockpit 服务器，它们可能存在 [CVE-2026-4631](https://access.redhat.com/security/cve/cve-2026-4631) 漏洞。不过我们没有实测，因为我们自己的租户里没有 RHEL/Rocky 服务器，而且我们已通知供应商并正与他们核实补丁是否到位——但它们中招的可能性相当大

总的来说，作为一次初步检查，这个发现相当离谱，也是本文开头那些「单点故障」梗图的由来。

## 后端网络上的租户隔离问题

「云」的全部意义就在于你必须共享一部分基础设施。大多数时候，这意味着共享网络。网络分两大类：前端网络（也称南北向，即接入互联网的公网）和后端网络（也称东西向，或互联 fabric，或横向扩展/纵向扩展网络，即只在集群内部连接各服务器的私有网络）。几乎按定义，云服务中的这部分网络就是在租户间共享的。因此，你必须确保它是安全的。

我们在这个话题上有两个案例，都以两种不同的方式错误配置了 [InfiniBand 安全密钥](https://developer.nvidia.com/blog/infiniband-multilayered-security-protects-data-centers-and-ai-workloads)。InfiniBand 与以太网不同，它不像典型以太网那样使用 VLAN 和 VXLAN，而是依靠一种叫 P_Key 的概念做隔离。此外还有许多承担其他功能的密钥。例如：

- **M_Key** 阻止恶意主机更改设备配置。密钥不匹配时，交换机会丢弃该请求。
- **P_Key** 是分区键，作用类似 VLAN，控制 fabric 上哪些设备可以互相看见。
- **SA_Key** 保护子网管理器（Subnet Administrator）中的敏感操作，例如记录的增删。
- **VS_Key** 保护 ibdiagnet 等厂商工具。
- **Q_Key** 保护不可靠数据报流量。**L_Key** 与 **R_Key** 保护 RDMA 操作中的内存。
- **C_Key** 与 **N2N_Key** 保护通信管理器流量和节点间消息。
- **AM_Key** 保护 SHARP 聚合，确保只有经批准的交换机可以执行数据归约。

测试中我们只用标准的 infiniband-diags 软件包就发现了这两个问题。其中一个案例里，供应商甚至已经替我们在登录节点上装好了这个包。

第一个案例中，一家供应商没有正确配置 P_Key 和 SA_Key。集群有一个新的分区键（0xa601），但默认分区键（0xffff）仍然生效。于是我们运行 saquery 时，看到了 fabric 上的 532 个主机名和端点。这些主机名暴露了其他客户和内部分区。我们到此停止了测试，并告知供应商删除默认 P_Key、更换 SA_Key。

![](https://substack-post-media.s3.amazonaws.com/public/images/6f8788dc-bdef-4a05-a4c0-dd363f5365cc_1456x663.webp)
*来源：SemiAnalysis ClusterMAX 测试*

第二个案例中，供应商把隔离和功能一起搞坏了。当我们发现他们没有设置 M_Key 时，供应商解释说该集群尚未完成生产验收，遗漏是为了赶着把机器交给我们。但 P_Key 的配置也以另一种方式出了错。我们的节点在一个隔离分区（0x7001）中拥有完整成员资格，这是正确的；但我们的节点同时在默认分区（0x7fff，容纳 fabric 上所有节点）中也拥有完整成员资格。结果很诡异：我们无法在自己 4 个节点之间运行 ibping，却能用 ibnetdiscover、ibdiagnet 和 ibhosts 在 fabric 上发现 80 个节点。一个错误的分区配置可以同时破坏租户隔离和正常功能。

![](https://substack-post-media.s3.amazonaws.com/public/images/febabb97-febd-49d8-b5b4-26c90b0b0cfa_1212x1052.webp)
*来源：SemiAnalysis ClusterMAX 测试*
![](https://substack-post-media.s3.amazonaws.com/public/images/dc2887dc-d4ea-4450-bf4f-751efb5363a0_966x1017.webp)
*来源：SemiAnalysis ClusterMAX 测试*
![](https://substack-post-media.s3.amazonaws.com/public/images/15f13579-1fc0-4cff-befa-8413d085bcc5_1350x770.webp)
*来源：SemiAnalysis ClusterMAX 测试*

那个集群租户内部的主机隔离也很弱。我们可以直接以 root 登录 GPU 节点。供应商证实，其在整个集群配置了共享 root SSH，其自有的基础设施密钥可以免密访问所有节点。因此，供应商的一枚密钥就能 root 访问每一台主机。

我们在前端网络上也看到了同类问题。在该集群上，没有任何主机防火墙在运行，我们询问是哪些安全组、ACL 或 VPC 机制在阻止节点间的 TCP 通信。供应商不得不先修正 InfiniBand 配置和外部连接，测试才能进行。

关于披露再说最后一点。2026 年 4 月，在我们发布基于 2025 年测试的 ClusterMAX 2.1 发现之后，该供应商的市场团队两次要求我们删除或改写关于可见端点的那句话。该团队称这句话可能有损品牌形象，并说工程团队已在 2025 年底修复了密钥。我们没有删除这一发现。我们更正了一处事实错误：我们是在 11 月完成测试的，而不是 12 月。我们据此更新了文章。

## 在共享基础设施上运行任意容器镜像

许多让攻击者在企业基础设施内横向移动的利用手法，都涉及从容器或虚拟机中逃逸并在底层主机上提权。这是一个始终存在的问题，许多 neocloud 都容易中招。

讲这个故事最简单的例子是 Wiz 命名的 NVIDIAscape（CVE-2025-23266）。它利用 NVIDIA Container Toolkit 的 createContainer 钩子，最初于 2025 年初公布。时至今日，总不会还有人能用它从容器里逃出来吧？

![](https://substack-post-media.s3.amazonaws.com/public/images/09055d66-38ef-43cc-9c9c-206acb1bd807_1456x143.webp)
*来源：SemiAnalysis 测试*

事实证明，还真有。

OCI 钩子是容器运行时在容器生命周期特定节点执行的程序。这个存在漏洞的 NVIDIA 钩子会在容器启动前以提升权限在容器宿主机上运行。在本例中，该钩子继承了来自容器镜像的环境变量。一个精心构造的镜像只需设置：**ENV LD_PRELOAD=/proc/self/cwd/poc.so**

LD_PRELOAD 会指示程序加载指定的共享库。由于该钩子的工作目录是已准备好的容器文件系统，它会从镜像中加载 poc.so。于是 poc.so 中的代码以 root 权限在容器宿主机上执行，容器就此逃逸。

NVIDIA 在 nct 1.17.8 中修复了 CVE-2025-23266，方法是阻止 LD_PRELOAD 等由容器控制的环境变量触达特权钩子。详见这份 [NVIDIA 公告](https://nvidia.custhelp.com/app/answers/detail/a_id/5659)。

在测试中，我们构建了一个自定义容器镜像，其中包含两个关键文件：

- **/poc.so**：写入一个 **HOOK_RAN** 标记，并记录加载它的进程的证据信息。

- **/probe**：在容器启动时检查这些证据是否存在。

使用 CLI 的 **cmax audit security** 时，我们的脚本会用 nct 运行时启动该镜像。在有漏洞的 nct 版本上，特权 NVIDIA 钩子会在容器启动前加载 /poc.so，该库随即写入标记并记录信息，包括加载者、用户 ID、进程 ID、PID 1、可见 GPU 以及容器宿主机信息。

下面是一个例子：我们在某供应商网站提供的一台单卡 H100 机器上运行它，并在容器启动期间观察结果：

![](https://substack-post-media.s3.amazonaws.com/public/images/fff57ac0-9b95-479d-9c15-85f4e88bb86a_1331x846.webp)
*来源：SemiAnalysis ClusterMAX 测试。*

当 /probe 启动时，它会检查这些证据。如果证据表明 /poc.so 是被特权 NVIDIA 钩子加载的，ClusterMAX 就会报告观测到了存在漏洞的行为。

你可以在任何装了 nct 的 GPU 机器上运行这项检查：

**cmax run nct-cve-2025-23266 --audit**

测试中我们发现，仅靠容器隔离不同负载的平台，远不如把每个容器都放进虚拟机的平台安全。

在多家供应商的测试中，我们的测试都从单个 docker 容器中逃逸，并在底层宿主 VM 上拿到了 root。不过我们没有继续从宿主 VM 中再逃出去。

这是纵深防御的一个好例子。容器本身有漏洞，但 VM 提供了又一道隔离边界，限制了问题的蔓延范围。

无论如何，这都是一个提醒：把所有东西都保持最新。

![](https://substack-post-media.s3.amazonaws.com/public/images/64726177-f3e2-4696-b725-3e728233f723_1280x1156.webp)
*来源：SemiAnalysis Meme Team*

即便是金牌（Gold）供应商，也可能不满足一项基本要求，比如 NVIDIA 驱动的最低版本。这里我们对比 CoreWeave 与 Azure。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2ceaf77-468e-4fb2-ab72-2c03b5859a8a_1456x133.webp)
*来源：SemiAnalysis ClusterMAX 仪表板*

而在这里，Azure 通过了全部四项检查，一家未具名的铜牌（Bronze）供应商则全部未通过：CUDA、runc、Docker 和 ConnectX 固件统统过时。

![](https://substack-post-media.s3.amazonaws.com/public/images/7dd847f6-387c-4913-92c3-e8a4a428b97c_1456x246.webp)
*来源：SemiAnalysis ClusterMAX 仪表板*

审计时，该铜牌环境运行的是 Docker Engine 29.1.3，而非已修复的 29.5.1 版本，意味着它处于 CVE-2026-41567 的受影响版本范围。这个高危的 docker cp 漏洞可能让恶意容器以 root 身份在宿主机上执行任意代码。

![](https://substack-post-media.s3.amazonaws.com/public/images/86c6e6c3-761c-45ec-ad14-b079c730ac80_1400x346.webp)
*来源：SemiAnalysis ClusterMAX 仪表板*

顺带一提，同一家金牌供应商（Azure）在两个不同环境中表现出截然不同的安全结果。Azure Kubernetes 通过了审计时适用的 runc 与 NVIDIA Container Toolkit 最低版本检查，而在我们测试的 Slurm 与 Kubernetes 环境中，其 NVIDIA 驱动却未达到最低版本要求。

容器逃逸始终存在，供应商需要有一套体系来持续完成升级。没有任何软件能永远运行下去。一切都有生命周期，最终都需要升级。最好提前为此做好规划。

## 别忘了网卡里的那台计算机

NVIDIA 在收购 Mellanox 之后推出了 BlueField DPU，并在 2020 年 10 月宣布 [BlueField-2 DPU](https://nvidianews.nvidia.com/news/nvidia-introduces-new-family-of-bluefield-dpus-to-bring-breakthrough-networking-storage-and-security-performance-to-every-data-center) 时顺带给这一品类起了名字——数据处理单元（data processing unit）。[BlueField-3](https://nvidianews.nvidia.com/news/nvidia-extends-data-center-infrastructure-processing-roadmap-with-bluefield-3) 于 2021 年 4 月跟进，并在 [2023 年初正式全面上市](https://www.hpcwire.com/2023/03/21/nvidia-announces-bluefield-3-ga-oracle-cloud-is-early-user/)。卖点很简单：这块卡将软件定义的网络、存储、安全与管理功能卸载、加速并隔离，把这些工作从主机 CPU 上拿走，让昂贵的硅片专心干它真正的本职。这不是什么小众配置——NVIDIA 的[参考架构](https://blogs.nvidia.com/blog/ai-cloud-providers-reference-architecture/)基本把 BlueField-3 列为南北向连接、存储加速和零信任安全的必选项，因此任何照 NVIDIA 蓝图搭建的 neocloud 都天然配备它们。

但 BlueField DPU 其实并不只是一块网卡。它是一台恰好与 ConnectX NIC 共封装的 Arm 计算机，有自己的 CPU 核心、自己的内存、自己的 Linux 安装，还有自己的管理端口（和 BMC）。在 DPU 模式下，Arm 侧拥有 NIC 资源和数据通路，这正是供应商购买它们的全部理由。每租户 VPC 隔离、流表和防火墙规则全部运行在那里。租户本不该接触到 DPU 本身，只应使用它提供的功能。

在 NVIDIA 的 [BlueField 运行模式表](https://networking-docs.nvidia.com/doca/archive/3-4-0/bluefield-modes-of-operation)中，DPU 模式对应的信任模型是「host-trusted（信任主机）」，并且是 DPU SKU 的默认模式。另一种选择是零信任模式——DPU 模式的一个变体，「通过阻止主机系统管理员从主机侧访问 BlueField 来增强安全性」，它会禁用 RShim 接口、限制从主机刷新固件、阻断 tracer、禁用硬件计数器，并阻止主机夺取端口所有权。NVIDIA 的[置备框架](https://networking-docs.nvidia.com/dpf/25100/zero-trust-deployment)提供了同样的选择：要么是信任主机的部署，要么是零信任部署——主机被视为不可信，只能把 DPU 当作一块普通网卡使用，无法触及其管理面。

NVIDIA 的威胁模型假设主机管理员是可信的。而在 GPU 云里，租户往往就是主机管理员，因为大多数供应商交付的是带 root 权限的独占节点。这就让 NVIDIA 信任的一方与供应商试图隔离的一方变成了同一个人。

保持默认设置时，主机通过 RShim 驱动保留一条通往 DPU Arm 核心的私有链路，它表现为 /dev/rshim0 设备和一个名为 tmfifo_net0 的虚拟以太网接口，DPU 则在一个有文档记载的子网的固定地址上应答。我们在测试中会从租户环境内部检查这条链路，因为在配置正确的多租户集群中它本不该存在。然而，在我们仅对少数几家供应商进行的初期测试中，就已经发现至少一台配置错误的主机上存在 RShim 通路。

由此带来两个问题。

第一，它颠覆了供应商所售卖的管控。BlueField DPU 常被委以路由和防火墙之责，把工作从主机操作系统上卸载下来——这正是它区别于网卡的意义所在。然而，在多租户环境中，只有主机够不到 DPU，这些服务才是安全的。RShim 一旦敞开，执行面就处在了被监管者的触达范围内。这扇门后是为每个租户实现 VPC 的 eSwitch 数据通路、流表、virtio-net 控制器和固件。一个相关的例子是 [CVE-2025-23299](https://nvd.nist.gov/vuln/detail/CVE-2025-23299)：BlueField 与 ConnectX 管理接口中的一个越界写入漏洞，可能允许高度特权的本地行为者执行任意代码。公开公告并未指认 RShim 为受影响组件，但作为特权用户、再握有 RShim 访问权，就得到了利用该漏洞的直接路径。

第二，DPU 软件层的篡改能在主机侧重新置备后幸存。DPU 的固件及其 Arm 侧操作系统驻留在设备上而非主机磁盘上，因此对主机重刷镜像并不会重刷其 DPU——如果它此前已被污染。在租户之间循环复用机器的供应商，等于连同一台完整 Arm 计算机一起复用。事实上，NVIDIA 有文档记载的 host-trusted 工作流明确允许主机通过 RShim 置备 BlueField、重置其 Arm 核心、安装完整 DPU 镜像。在客户即主机 root 的裸金属云中，暴露这一工作流本身就是信任边界的失守。

集群运营者——尤其是那些提供裸金属、默认开放 root 的集群的——应当检查自己的 DPU 运行模式，禁用 RShim 或限制刷新 DPU 之类的特定能力。更稳妥的做法是，置备流程还应重新刷写 DPU 的镜像与固件，确保同一节点上前后用户之间，DPU 操作系统层的任何篡改都被清除干净。

![](https://substack-post-media.s3.amazonaws.com/public/images/81634e15-b918-4322-8d29-1f97bfddc67a_716x1154.webp)
*来源：我们自己*

# 用智能体构建漏洞 POC

在我们为既有漏洞构建、向供应商演示细节的众多 POC 中，最大的挑战是闭源模型的护栏。Fable 会立刻拒绝，并把请求降级给 Opus 4.8，而后者会拒绝构建任何 POC，甚至拒绝回答任何与安全相关的问题。哪怕是关于安全或 CVE 的简单问题，Fable 也会断然拒绝。

GPT 5.6 Sol 灵活一些，在编排与规划上也表现不错，还充当「验证」模型：由一个开源模型构建 POC，5.6 Sol 判断其正确与否。不过到了某个节点，5.6 Sol 也会开始拒绝这类请求。

大部分代码是手写的，或是在开源/开放权重模型的辅助下完成的，具体是 Kimi K3、GLM 5.2 和 DeepSeek V4。Kimi K3 和 GLM 5.2 经常限制构建功能性漏洞 POC 的请求，即便工作范围已明确限于授权测试。DeepSeek V4 通常更宽松，但偶尔会生成误报或无法复现预期行为的实现。我们用 5.6 Sol 作为验证器，按照一套明确的测试细则复核了这些结果。

这暴露了防御性安全研究中一个明显的缺口。白帽研究者需要可运行的 PoC 来验证漏洞，但能力强的模型即便在用户获得授权时也限制这类工作。研究者因此往往被推向可控性更强的开放模型，而它们在推理、可靠性和技术深度上又不及前沿模型。这就像背着一只手打架。这也正是 HuggingFace 在上文 OpenAI 事件中的处境：他们实实在在地被前沿闭源模型攻击，却主要只能用 GLM 等开源模型来拦截攻击请求、分析平台上的制品、载荷与日志。值得注意的是，正是因为 HuggingFace 用上了这些模型，他们才最先找到了攻击的根因。在与 HuggingFace 取得联系并协同之前，OpenAI 一直不知道该事件的细节和波及范围。今天，如果你接触不到一个能对网络安全议题进行开放推理的前沿模型，你实际上不可能跟上网络安全研究的前沿。

![](https://substack-post-media.s3.amazonaws.com/public/images/3983e92f-4343-48c4-b637-beaedb7d00f6_751x212.webp)
![](https://substack-post-media.s3.amazonaws.com/public/images/dd226415-3350-4d1e-92f6-6c04adf541b9_737x165.webp)
*来源：被 Fable 拒绝中……我们只是提了几个问题而已！*

# 我们推荐的最低版本（以及如何使用 cmax audit security CLI）

为了帮助 neocloud 和运营者跟踪最新的最低版本要求，我们维护了一份每日刷新的最低版本清单，汇总各大信息源与软硬件厂商的公告，并基于这些公告发布聚合后的最低版本。ClusterMAX 网站展示并托管这些数据，供我们的 CLI 及其他厂商以程序化方式访问。

使用方法很简单：按照安装说明装好 CLI，然后运行 cmax audit security。CLI 会从 ClusterMAX 网站拉取最新的最低版本数据，并据此审计你的系统。

一旦检测到有漏洞的版本，CLI 会在控制台打印相关安全公告（附可点击链接）以及建议升级到的版本。

![](https://substack-post-media.s3.amazonaws.com/public/images/4aaa0cfa-23d0-4bf5-8eaf-7996b01ec41d_1456x424.webp)
*来源：ClusterMAX CLI 0.3.0 安全模块*

供参考，下面是我们针对多款常用软件、驱动、库和固件的当前最低版本表。所有信息来自公开安全公告，仅截至撰写时（2026 年 8 月 19 日）有效：

![](https://substack-post-media.s3.amazonaws.com/public/images/494a94ed-ad6c-42ce-8bd1-6cd772f09584_1456x673.webp)
*来源：clustermax.ai 网站*

# 总结：大多数供应商需要修什么？

如果你还在读，那我们不妨假设你已经跨过了「认真对待安全」的门槛。那么该做什么？

在当下，供应商需要一套体系（SYSTEM）来完成打补丁。顶级云厂商部署补丁用的体系和它们置备新集群用的是同一套。这套体系包括人、脚本，而且越来越多地包括 AI。

首先是要有一套像我们每日刷新最低版本那样的安全公告监控系统。在我们测试的 neocloud 中，只有少数几家已有自动化系统，其余大多依赖每月甚至更长周期的固定补丁节奏。随着聚焦网络安全能力的模型快速发展，这样的打补丁节奏已经不够用了。

所以，以下是我们给人类和 AI 的建议——往你们的脚本里写上这些：

- 请把你的东西升级到我们公开网站上的[最低版本](https://www.clustermax.ai/)（欢迎用 **cmax** 来帮忙）
- 请花时间（有些情况下还要花钱）修复糟糕的设计。「任何单点故障都不得暴露你的全部用户」是新规矩。所以，别再在 k8s 上用共享节点做 namespace 隔离，别再只靠容器做租户隔离，别再让人碰到 BMC 和 DPU，并把你的 InfiniBand 安全密钥配置正确。

说完这些，我们期待很快在 ClusterMAX 3.0 与你相见！

# 对 NVIDIA、AMD 及所有芯片初创公司的影响

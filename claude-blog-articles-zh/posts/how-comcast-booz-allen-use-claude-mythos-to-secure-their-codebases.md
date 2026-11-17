---
title: "Comcast 与 Booz Allen 如何借助 Claude Mythos 发现漏洞利用链并加固代码库"
title_en: "How Comcast and Booz Allen use Claude Mythos to find exploit chains and secure their codebases"
date: 2026-10-06
source: https://claude.com/resources/articles/how-comcast-booz-allen-use-claude-mythos-to-secure-their-codebases
crawled: 2026-11-17
translated: 2026-11-17
---

# Comcast 与 Booz Allen 如何借助 Claude Mythos 发现漏洞利用链并加固代码库

> 原文：[How Comcast and Booz Allen use Claude Mythos to find exploit chains and secure their codebases](https://claude.com/resources/articles/how-comcast-booz-allen-use-claude-mythos-to-secure-their-codebases) · Claude 博客

Comcast 和 Booz Allen 的安全团队通过 Project Glasswing 使用 Claude Mythos 级模型，发现、验证并修复了其现有扫描器漏掉的漏洞。

今年早些时候，Anthropic 推出了 [Project Glasswing](https://www.anthropic.com/glasswing)——一个限定开放的项目，旨在让全球关键基础设施的防御者在加固代码库上抢占先机。本周，我们推出了扩展后的新版[网络验证计划（Cyber Verification Program，CVP）](https://www.anthropic.com/news/cyber-verification-program)，让符合条件的安全专业人员能够使用先进的网络能力，并采用拦截限制更宽松的分类器。

作为 [Project Glasswing](https://www.anthropic.com/glasswing) 的一部分，守护关键基础设施的组织已让 Claude Mythos 模型在其所防护的系统上投入工作。在这些组织中浮现出一个共同主题：现有网络安全工具能够孤立地识别单个漏洞，但漏洞利用链——攻击者把若干单独看来微不足道的弱点串联成通往严重后果的路径——要难追溯得多。像 Claude Mythos 这样的模型有助于把代码、配置和运行中应用的实际行为拼合起来，使组织既能发现普通的单文件缺陷，也能发现只有在组件相互作用时才会显露的复杂跨系统漏洞。

我们采访了参与该项目的 Comcast 和 Booz Allen 的安全负责人，聊了聊 Claude Mythos 级模型在他们的环境中发现了什么，以及它如何改变其团队防御攻击的方式。

## Comcast：把"发现"与"可利用的漏洞"区分开

Comcast 是一家全球媒体与科技公司。在一次覆盖 258 个业务关键系统、约 1.7 亿行代码的评估中，它使用 Claude Mythos Preview 在某个面向公众的平台上发现了一个严重的身份验证漏洞。该问题本可让攻击者绕过身份验证控制；在观察到任何漏洞利用迹象之前，它就已经被修复。

"发现问题的速度正在变快，"Comcast 执行副总裁、首席信息安全与产品隐私官 Noopur Davis 说。"发现问题也正在变容易。发现的数量极其庞大。而对这些海量发现进行验证，才是新的瓶颈。"

这一发现来自 Claude Mythos Preview 跨越复杂软件生态进行推理的能力，而不是孤立地评估单个文件或组件。该漏洞并非由某一个有缺陷的组件造成，而是源于多个系统之间的相互作用，以及一些单独审视时看似正确的假设。通过跨代码、配置和应用行为保持上下文，Claude Mythos Preview 识别出了一个在多个相互作用组件之间形成的安全缺口——用常规方法很难发现它。

"前沿 AI 模型让大规模生成发现变得容易得多，"Davis 说。"但只有验证确认了底层问题，一条发现才能成为漏洞；而只有它真的能在目标环境中被利用，这个漏洞才算可利用。"

Comcast 的工程师针对运行中的应用验证了这一发现，确认该底层安全问题在实践中可以被触达。团队随后追溯了根因，实施了修复，并核实该漏洞在被修复之前并未遭到利用。这一发现代表了所观察到的一种更普遍的模式：Claude Mythos 级模型识别出的部分影响最大的问题，并非源于单个编码错误，而是源于复杂软件环境中的细微相互作用。

"提前获得访问权限，大概把我们理解前沿 AI 模型安全能力的时间提前了一年，"Davis 说。"我们非常感激 Anthropic 围绕这个项目建立起来的社区——它让参与者得以分享经验教训，从而帮助更广泛的生态。"

## Booz Allen：把漏洞利用链拼起来

Booz Allen 为国防、民用、国家安全和商业任务构建并部署技术，其网络业务致力于缩小 AI 驱动的攻击者与传统网络防御之间的速度差距。这包括开展红队演练，以及为面对 AI 赋能对手的客户构建防御。

Booz Allen 的安全评估只在固定期限内进行，工程师在评估结束前能读的源代码、配置和已编译软件终究有限。仅靠扩大覆盖范围并不能弥合这一差距，因为真实攻击通常是把代码、配置、身份和部署设置中的小弱点串联起来；即便对熟练的操作者来说，在庞大的软件组合中手工追踪这些关联也很慢。

Booz Allen 使用 Claude Mythos Preview 审查了远超一次短期评估通常可覆盖范围的软件，并找出那些可被串联成漏洞利用链的弱点。

"Mythos 令人意外的是它跨边界推理的能力，而不只是识别孤立的代码问题，"Booz Allen AI 工程副总裁 Sahil Sanghvi 说。"它帮助把应用行为、配置、身份、权限和部署上下文连接成连贯的安全假设。"这项工作从发现到修复的推进速度也超出了团队的预期：模型会帮助起草修复方案，并为负责受影响系统的工程师汇集证据。

在一个案例中，一个 Claude Mythos 级模型在设备首次开机、操作系统加载之前运行的代码里发现了一个缺陷。这段代码决定设备应当锁定自己还是擦除数据，而它做出这一判断时依赖机器上存储的一把安全密钥。这把密钥此前未受保护，因此本该被它约束的操作系统可以换成攻击者控制的密钥，然后向机器输入它信任的指令。攻击者可以无限期地阻止"锁定或擦除"这一步，使一台丢失、被盗或已被攻陷的设备本该自行关机时，仍然完全可被访问。

这个系统本来有好几次机会锁定这把密钥，但每一次都被错过了。密钥最初被保存时，本可保护它的设置处于关闭状态。负责把它写入硬件的代码原样传递了该设置，没有加以纠正。另一项本可在此后锁定密钥的保护措施也从未启用。Claude 通过在两段用不同语言编写、彼此不同的程序中追踪那一个设置，然后确认始终没有任何环节锁定过密钥，从而发现了这个漏洞。

"Mythos 能迅速生成一个庞大的候选集，但团队仍需验证发现、去重系统性问题，并把问题分派给正确的负责人，"Booz Allen 国家网络安全业务总裁 Brad Medairy 说。"一名分析师在十二天内审查了 138 个代码仓库中的 8 个生产系统。没有 Mythos，这种规模的组合审查需要我们投入更大的团队、花上好几个月。"

对 Booz Allen 而言，这指向了一种不同的安全审查方式：由操作者保留判断权，而模型则扩展他们能够持续监控的软件组合范围。

"我们的研究表明，前沿模型有能力自主执行完整的网络杀伤链，"Medairy 说。"组织必须持续运行网络安全审查与防御，才能跟上步伐。"

## 下一步

随着具备 Claude Mythos 能力的模型成为日常安全工作的一部分，组织可以像熟练的攻击者那样审视自己的系统：追踪代码、配置和遗留组件如何相互作用，并在其他人找到突破口之前封堵它们之间的缝隙。我们构建 Project Glasswing，就是为了让防御者率先获得这种能力；我们将通过新的网络验证计划（CVP）持续扩大可用范围，让更多运行关键软件的组织能够把它用起来。

[进一步了解网络验证计划（CVP）。](https://www.anthropic.com/news/cyber-verification-program)

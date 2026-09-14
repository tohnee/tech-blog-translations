---
title: "与我们的客户共同开发 Enterprise Frontier Safeguards"
title_en: "Developing Enterprise Frontier Safeguards with our customers"
source: https://www.anthropic.com/news/enterprise-frontier-safeguards
published: 2026-09-01
crawled: 2026-09-14
translated: 2026-09-14
---

# 与我们的客户共同开发 Enterprise Frontier Safeguards

> 原文：[Developing Enterprise Frontier Safeguards with our customers](https://www.anthropic.com/news/enterprise-frontier-safeguards) · Anthropic News

公告

# 与我们的客户共同开发 Enterprise Frontier Safeguards

2026 年 9 月 1 日

![与我们的客户共同开发 Enterprise Frontier Safeguards](https://www-cdn.anthropic.com/images/4zrzovbb/website/60d57c0d0bf031e140de678692f7c3ef2d885ce3-1000x1000.svg)

今天，我们发布 Enterprise Frontier Safeguards（EFS）。这一方案将零数据保留（zero data retention, ZDR）的隐私性与用于检测滥用的最先进防护（safeguard）结合在一起。EFS 的运作方式是将数据存储在由客户而非 Anthropic 控制的云基础设施中。EFS 将从今年秋季晚些时候开始分阶段向客户推出。为了让过渡平稳进行，符合条件的客户在 EFS 就绪之前，将可在 Fable 5 和 Fable 5.1 上享受 ZDR。

我们与金融服务、医疗健康、制造、电信、法律、零售和公共部门等行业的 100 多家客户，以及我们在 Amazon Web Services、Google Cloud 和 Microsoft Azure 的云合作伙伴紧密合作，共同开发了 EFS。

EFS 将支持 Claude Code、Claude Enterprise、Claude Platform、Amazon Bedrock、Claude Platform on AWS、Google's Agent Platform 以及 Microsoft Foundry。

## 解决前沿安全的两难困境

Mythos 级模型（如 [Claude Fable 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)）在智能和智能体能力上都实现了重大跃升。然而，能力提升的同时，也带来了滥用和自主失当行为的潜在风险。

过去几个月里，我们看到了大量试图滥用 AI 模型的证据。这些行为既包括欺诈等典型形式的滥用，也包括复杂的网络攻击——其中可能涉及智能体自主实施破坏性行为。其中一些案例还涉及窃取或盗用企业客户的凭据，而如果没有监控流量、检测异常行为的能力，这类行为很难被发现。

此外，由于[最复杂的滥用行为](https://www.anthropic.com/news/disrupting-AI-espionage)可能涉及分布在多个会话和多个账户中的大量任务，仅仅对每次交互单独运行自动化分析、然后立即丢弃数据是不够的。有效的检测需要在一段有意义的时期内存储数据，以便跨时间、跨账户进行关联分析。

正因如此，我们从 Fable 5 开始引入了 30 天数据保留政策。这一政策并非出于在企业数据上训练模型的意图：Anthropic 从未在未获明确许可的情况下用企业数据训练模型，今后也绝不会。

与我们合作的企业普遍理解数据保留在安全与安保（safety and security）方面的价值，但许多企业——尤其是受监管行业的企业——发现很难使用带数据保留的模型。因此，我们与客户坐到一起，共同设计一个两全其美的方案：既有 ZDR 的隐私性，又有跨时间、跨账户监控带来的安全性。

## 与客户共同设计

我们在构建 Enterprise Frontier Safeguards 的过程中，不断听取那些每天都要使用它的专家的反馈：安全、产品、合规和交付团队。与我们合作的组织之一是系统性风险分析与韧性中心（Analysis and Resilience Center for Systemic Risk, ARC），其成员包括美国最大几家银行的首席信息安全官，其中有 Goldman Sachs、Morgan Stanley、Citi、Bank of America 和 Wells Fargo。

我们还与 Comcast、KPMG、Mastercard、Salesforce、Visa 等公司的领导者合作，确保这一设计在各行各业都站得住脚。我们的沟通对象覆盖了四分之一的《财富》100 强（Fortune 100）、全部美国全球系统重要性银行，以及几乎所有的受监管行业。

以下是我们从如此广泛的客户群体那里听到的声音，以及我们为回应这些共同关切而在 EFS 中做出的设计：

### 关于监控

企业长期以来一直针对内部人员风险（insider risk）进行监控，如今则希望获得帮助，把监控能力升级到智能体层面。他们关心的是 Anthropic 的自动化监控系统能否达到他们的监管标准。

**在 EFS 中，由客户掌控数据如何被审查。**当监控检测到需要关注的模式时，相关信号会直接发送给客户，让他们审查自动系统检测到了什么。

### 关于数据存储

出于多种原因，企业要再新增一家「受信任的数据供应商」，是一项繁重的工作。他们需要通知自己的所有客户这些供应商是谁，并更新合同。同时，鉴于这类数据高度敏感，企业对数据的安全存储和审计也有内部要求。出于这些顾虑，我们在架构上让 EFS 的客户能够把数据存储在既有的云基础设施上。

**在 EFS 中，客户可以掌控自己数据的存储与管理。**客户希望数据保存在由自己控制的基础设施中，使用自己的加密密钥、访问策略和审计日志。用于监控的活动数据可以存储在客户自己的云账户中（例如 Amazon S3、Azure Blob Storage 或 Google Cloud Storage）。

### 关于自动审查与人工审查

尽管自动审查正变得越来越有效，但由人来查看标记仍然有其价值：确认真实的滥用、排除误报。但我们从许多客户（尤其是受监管行业的客户）那里听到的是：执行这种审查的人必须是他们自己的人。许多企业受到严格规定的约束，限定谁可以查看某些信息——特权法律材料、非公开信息、药物安全报告。他们的团队已经接受过培训并被授权从事这类工作。

**EFS 采用自动化安全监控，无需 Anthropic 人工审查。**客户希望获得针对网络攻击的保护，也理解这类攻击如果横跨多个会话和账户展开，检测起来可能相当困难。借助 EFS，自动化系统会对一个滚动时间窗内的流量进行分析，寻找严重滥用的信号，包括研发攻击性网络或生物能力的企图，以及凭据遭窃取或泄露的迹象。这些标记会直接发送给客户，后续由客户的人员接手处理——无需 Anthropic 员工进行任何人工审查。

![ logo](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F9f37b737d862a71f1fbcd15e5d9d5f98d3ca1ca2-1200x675.png&w=256&q=75)

> AI 管控措施在设计上必须能够保护敏感信息，而模型防护正是这一过程中的重要一环。Anthropic 在开发 Enterprise Frontier Safeguards 的过程中主动与我们接洽，以确保其符合我们的要求与标准。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/628e9fd1129632a8fc5682deec87b1888c2e8e89-155x16.svg)

> Enterprise Frontier Safeguards 给我们的正是我们所要求的：我们的日志保存在由 Wells 管理的环境中、使用由 Wells 管理的密钥。数据保管权在我们手中，而检测由 Anthropic 运营。正是这种分工，让我们的团队能够安全地把前沿模型投入工作，并履行我们对客户、员工和监管机构的义务。我们参与了这些防护措施的塑造，因为我们的行业需要它们。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/da5b4cfb98abd20aa33357f44216a41279e57e0d-155x62.svg)

> 作为一家运营关键基础设施的公司，模型的能力固然重要，但同样重要的是能让我们把数据保存在自己账户中的解决方案——Enterprise Frontier Safeguards 解决了这个问题。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/b847b0a49194adb0df9674c8b5e5fe176e845bda-109x27.svg)

> 我们的八家成员机构与 Anthropic 合作，共同界定了在一家系统重要性银行内部运行最强大的前沿模型需要满足哪些条件：数据由谁持有、密钥由谁掌握、自动审查能看到什么、不能看到什么，以及在什么条件下才允许人去查看。这项合作正在推动改进版防护措施与标准的开发和交付，并有望扩展到整个行业乃至更广的范围。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/632ae4b5eb52539491a30a3c1cb2694febdb53ab-187x75.svg)

> 这套防护架构的一个核心原则，是让我们能够保留数据，并把数据保存在模型本身之外、在我们自己的环境中受到保护。我们的公司以及客户的业务中，有一些领域受到监管且高度敏感。这些防护措施实际上让我们能够在以前无法涉足的部分业务中应用 AI。  
>   
> *服务合作伙伴*

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/ad6656fb6427494ec5696471e61947bb72035ee9-273x191.svg)

> 二十多年来，客户一直放心地把数据托付给我们。正是因为有这样的经历，我们才希望与 Anthropic 一起深入思考这个问题，而不是袖手旁观。我们得以在架构层面（而不仅仅是政策层面）共同打造全新的安全与隐私能力。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/8e369e94bf09c7916c1e8045d7abc474e07b8a85-163x43.svg)

> 我们的客户希望把前沿模型投入实际工作，而他们的安全团队希望数据留在自己控制的基础设施中。Anthropic 与一百多家企业共同构建了 Enterprise Frontier Safeguards，正是为了实现这一目标。  
>   
> *服务合作伙伴*

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/58a9a5ba70a6c5d7a8604419d51236e1073fdc79-182x34.svg)

> 随着 AI 模型承担越来越多受监管的敏感工作负载，负责任地扩展最终也要落实到架构上，而不仅仅是政策承诺。对数据环境的直接控制，加上基于模式的自动化安全监控，赋予企业所需的切实、结构化的能力，让它们能够在真正的监督、问责和信心之下进行部署。  
>   
> *服务合作伙伴*

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/7b6dc90891455bc4c8624591184e5e826fc56541-156x53.svg)

> 这些防护措施及其设计——很显然，你们听取了我们的反馈。它们让我们坐上了主驾驶位。日志由我们控制；除非我们愿意，它们不会流向任何其他地方。它让我们掌控数据、掌控信息，也掌控在检测到可能突破防护的情况之后该采取什么行动。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/468fc2c0bb3ca80ff2b112002d4d665c1e2bff65-360x180.svg)

> 随着 AI 在企业内部日益深入，安全与信任正是推动组织从试验走向规模化部署的关键。Enterprise Frontier Safeguards 从一开始就将这两者内建其中：监控数据保存在客户控制的基础设施中，由客户自己的团队决定谁能访问这些数据。  
>   
> *服务合作伙伴*

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/721103059e160dd255816a622fc8d3e3cffe0047-150x48.svg)

> 为客户数据保密是 Snowflake 向每一位客户做出的承诺。我们始终在快速把前沿模型交到客户手中。难的是在最严格的数据保证之下安全地做到这一点。我们与 Anthropic 合作设计了 Enterprise Frontier Safeguards，从而得以两全：数据保存在客户的环境中、由客户控制的密钥保护，并从第一天起就运行 Anthropic 最强大的模型。这就是在设计中充分考虑平台需求时，负责任的前沿 AI 该有的样子。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/d514853a44cf69f069306c98b558f214112c4ef3-91x64.svg)

> 在 Stripe，保护客户数据是我们一切运营方式的根基。Anthropic 的 Enterprise Frontier Safeguards 将使我们能够在使用纳入覆盖范围的前沿模型的同时，把对话日志保留在 Stripe 的 AWS 环境中，访问与审查均由 Stripe 的安全控制机制管理。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/beb4f74e935e111be9a63875ae7743aaea2cb0a2-88x64.svg)

> Rogo 的客户期望获得现有最好的智能，但绝不能以牺牲数据的安全和防护栏为代价。Enterprise Frontier Safeguards 将在满足金融机构所要求的机构级数据要求的同时，为其带来最强大的模型。前沿智能与企业级管控的结合，对于在整个金融服务行业部署 AI 至关重要。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/3c70dfc4944696f4d3ecb9357d8b760190f7e322-2394x1000.svg)

> FIS 支撑着资金流动和金融机构运营背后的基础设施，因此我们部署的任何 AI 防护都必须达到同等的规模和信任标准。我们与 Anthropic 的合作已经包括通过 Project Glasswing 用我们自己的系统测试他们最先进的前沿模型。Claude Enterprise Frontier Safeguards 拓展了这项工作：保留的数据存储在我们自己的账户中，标记则直接路由到我们的安全团队。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/e93eb9aa6aeb9e95f584bf8a401c4bdd1206d225-112x24.svg)

> 各公司放心地把真正的生产工作交给 Cognition 的自主工程师，而这份信任取决于这些工作的私密性。借助 Enterprise Frontier Safeguards，客户数据和身份信息永远不会离开我们这一侧。它将让我们把前沿 AI 带入生产工作，无需在隐私上做任何妥协。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/752b5acf21c1b5502f0ba42f7b92b05401cc425d-462x68.svg)

> 客户的代码和数据是他们最宝贵的知识产权之一。保护这些信息是我们在 Factory 构建产品的基础。我们正与 Anthropic 携手，让客户在使用 Claude 最强大模型的同时，把专有数据的控制权留在自己手中。Enterprise Frontier Safeguards 让企业既可获得前沿智能，又享有其安全团队所要求数据保护。

![ logo](https://www-cdn.anthropic.com/images/4zrzovbb/website/6dfc3bd55cc5f9d5ebdd8d5437505ae4b8560412-120x64.svg)

> 我们始终坚定不移地致力于对客户的保密与安全。我们所服务的顶尖法律与专业团队将这些原则视为不可妥协的底线，我们也以同样的标准要求自己。Enterprise Frontier Safeguards 体现了这一承诺：即使是对保密性要求最严苛的客户，也能使用前沿模型，而模型提供商不会保留他们的数据。

01 / 17

## EFS 的工作原理

无论你是直接从 Anthropic 还是通过云合作伙伴访问 Claude，这些控制措施的设计都以相同的方式运作。使用 Amazon Web Services、Google Cloud 和 Microsoft Azure 的客户将获得同等的控制措施：他们的活动数据存储在他们自己的云账户中，也就是他们已经信任的环境里。我们还在努力支持为有资格使用 Enterprise Frontier Safeguards 的客户提供服务的第三方产品。

客户自有存储（Customer-owned storage）、客户管理的加密密钥（Customer-Managed Encryption Keys）以及完全自动化的审查均为可选择性启用的功能，你可以按组织需要开启相应选项。它们都不会改变模型行为、API 定价或速率限制。

Anthropic 对 Enterprise Frontier Safeguards 不收取费用。如果客户选择将数据存储在自己的云账户中，云提供商会像对其他任何资源一样，就存储以及读取、写入和数据流出（egress）费用向客户计费。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F021fdfc765d03eaac26f5d2aa9cb06111b7a9297-3840x4644.png&w=3840&q=75)

## 开始使用

Enterprise Frontier Safeguards 将分阶段向客户推出，目标是今年秋季晚些时候实现广泛可用。如需申请使用 Enterprise Frontier Safeguards，请填写此[表单](https://claude.com/form/enterprise-frontier-safeguards)。

## 相关内容

### 改进我们的对齐与安全工作

7 月 30 日，我们报告了三起 Claude 模型未经授权访问真实计算机系统的事故。我们正在对这两起事故进行深入分析，并计划与 METR 合作开展独立审查。在此期间，我们先分享过去一个月里做出的一些改变。

[阅读全文](https://www.anthropic.com/news/improving-alignment-security-efforts)

### 预览模型硬件标准

我们正在向首批科研实验室和先进制造商开放模型硬件标准（Model Hardware Standard, MHS）的研究预览。MHS 是一份共享规范，用于让 AI 智能体安全地操作物理设备。

[阅读全文](https://www.anthropic.com/news/model-hardware-standard-research-preview)

### 扩大我们对科学家的支持

从今天起，全球 10,000 名科学家可以零成本开始使用 Claude。经验证的首席研究员（principal investigator）可获得 Claude Team 订阅计划，并可在最长一年的时间内免费为研究团队添加 Standard 席位，或以每月 15 美元的价格添加 Premium 席位。

[阅读全文](https://www.anthropic.com/news/expanding-support-for-scientists)

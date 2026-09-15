---
title: "用 Skills 构建智能体：让智能体胜任专业工作"
title_en: "Building Agents with Skills: Equipping Agents for Specialized Work"
source: https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 Skills 构建智能体：让智能体胜任专业工作

> 原文：[Building Agents with Skills: Equipping Agents for Specialized Work](https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work/) · Claude 博客

过去一年发生了许多变化。MCP 成为智能体连接性的标准，被行业领袖与开发者社区迅速采用。[Claude Code 发布](https://www.anthropic.com/news/claude-3-7-sonnet)，成为一个通用的编程智能体。我们还推出了 [Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)，它现在开箱即提供可用于生产的智能体。

但在构建和部署这些智能体的过程中，我们不断遇到同一个缺口：智能体拥有智能与能力，却不一定具备有效应对真实工作的专业知识。这促使我们[创造了 Agent Skills（智能体技能）](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)。Skills 是有组织的文件集合，把领域专业知识——工作流、最佳实践、脚本——打包成智能体能够访问和应用的形式。它们能把一个能力出众的通才变成一个知识渊博的专才。

在本文中，我们将解释为什么我们不再构建专门的智能体，转而构建 skills，以及这一转变如何改变我们对扩展智能体能力的思考方式。

## **新范式：代码就是你所需要的一切**

我们曾以为，不同领域的智能体会长得非常不一样。编程智能体、研究智能体、金融智能体、营销智能体——每一个似乎都需要自己的工具和脚手架。行业最初拥抱的就是这种领域专用智能体的模式。但随着模型智能的提升与智能体能力的进步，我们收敛到了一种不同的做法。

我们逐渐认识到，代码与其说只是一个用例，不如说是智能体完成几乎任何数字化工作的接口。Claude Code 是一个编程智能体，但也是一个恰好通过代码来工作的通用智能体。

想想用 Claude Code 生成一份财务报告会发生什么。它可以调用 API 进行研究，把数据存进文件系统，用 Python 分析，再综合出洞见。这一切都通过代码完成。脚手架因此变得像 bash 和一个文件系统一样简单。

但通用能力不等于专业能力。当我们开始把 Claude Code 用在真实工作上时，一个缺口出现了。

## **缺失的一环：领域专业知识**

你希望谁来报税：是一个从第一性原理出发推导的数学天才，还是一位报过数千份税单的资深税务专业人士？大多数人会选择税务专业人士。不是因为他们更聪明，而是因为他们拥有恰到好处的专业能力。

如今的智能体就像那个数学天才：在推理全新情境时才华横溢，却往往缺乏一位资深从业者积累多年的专业能力。在恰当的指引下，它们能做出令人惊叹的事情。然而，它们常常缺失重要的上下文，无法轻松吸收你组织的专业积累，也不会自动从重复性任务中学习。

Skills 弥补了这一缺口：它把领域专业知识打包成智能体可以渐进访问和应用的形式。

## **什么是 Agent Skills？**

Skills 为智能体打包领域专业知识与程序性知识。

```
anthropic_brand/
├── SKILL.md
├── docs.md
├── slide-decks.md
└── apply_template.py
```

Skills 的简单性是有意为之。文件是一种通用原语，能与你已有的东西协同工作。你可以用 Git 对它们做版本管理，存进 Google Drive，与团队分享。这种简单性也意味着创建 skill 不再是工程师的专利。产品经理、分析师和领域专家已经在构建 skills，把自己的工作流固化下来。

## **渐进式披露**

Skills 可以包含大量信息。为了保护上下文窗口并让 skills 可组合，它们采用渐进式披露（progressive disclosure）：在运行时，只有元数据（来自 YAML frontmatter 的名称和描述）会展示给模型。

```
---
name: Anthropic Brand Style Guidelines
description: Anthropic's official brand colors and typography…
---

```

如果 Claude 判断需要某个 skill，它会读取完整的 SKILL.md 文件。如需更多细节，skills 还可以包含一个 references/ 目录，其中的支持文档只按需加载。

这种三层机制意味着你可以给智能体装备数百个 skills 而不会压垮它的上下文窗口——元数据约消耗 50 个 token，完整的 SKILL.md 约 500 个 token，参考文件 2,000 个以上 token 且只在确实需要时加载。

## **Skills 可以把脚本当作工具**

传统工具有些问题：有的说明写得不好，模型无法随时修改或扩展它们，而且它们常常把上下文窗口撑得臃肿。代码则不同：它自带文档、可以修改，而且根本不需要一直待在上下文里。

举一个真实的例子：我们不断看到 Claude 重复编写同一个脚本，把 Anthropic 的样式应用到幻灯片上。于是我们让 Claude 把它保存为给自己用的工具：

```
# anthropic/brand_styling/apply_template.py
import sys
from pptx import Presentation

if len(sys.argv) != 2:
    print("USAGE: apply_template.py <pptx>")
    sys.exit(1)

prs = Presentation(sys.argv[1])
for slide in prs.slides:
    ...
```

slide-decks.md 中对应的文档只需引用这个脚本：

```
## Anthropic Slide Decks
- Intro/outro slides
  - background color: `#141413`
  - foreground color: oat
- Section slides:
  - background color: `#da7857`
  - foreground color: `#141413`

Use the `./apply_template.py` script to update a pptx file in-place.
```

## **Skills 生态**

Skills 生态迅速兴起，到目前为止我们已经看到三大类 skills 正在被构建：

### **基础技能**

这类 skills 提供每个人都需要的核心能力：处理文档、电子表格、演示文稿等。它们把文档生成与操作的最佳实践编码进来。想要看看实际效果，可以探索我们[公共仓库中的基础技能](https://github.com/anthropics/skills/tree/main/skills/public)。

### **合作伙伴技能**

随着 skills 把智能体与专业能力的交互方式标准化，各公司正在构建 skills，让自己的服务可以被智能体访问。[K-Dense](https://github.com/K-Dense-AI/claude-scientific-skills)、[Browserbase](https://github.com/browserbase/agent-browse)、[Notion](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) 以及[许多其他公司](https://claude.com/blog/organization-skills-and-directory)正在创建直接集成自家服务的 skills，在特定领域扩展 Claude 的能力，同时保持 skills 格式的简洁。

### **企业技能**

组织会构建专有的 skills，把内部流程与领域知识编码进去。Skills 有助于捕捉那些让智能体真正能胜任企业工作的具体工作流、合规要求与组织制度知识。

## **我们观察到的趋势**

随着 skills 的采用不断增长，一些正在浮现的模式指向了这一范式可能的走向。这些趋势塑造着我们对 skill 设计以及为 skill 开发者构建的工具的思考。

### **复杂度不断提升**

早期的 skills 只是简单的文档参考。现在我们看到精巧的多步骤工作流，跨多个工具协调数据检索、复杂计算和格式化输出。

- **简单**：「状态报告撰写器」（约 100 行）——模板与格式化
- **中等**：「财务模型构建器」（约 800 行）——数据检索、用 Python 做 Excel 建模
- **复杂**：「RNA 测序流水线」（2,500+ 行）——协调 HISAT2、StringTie、DESeq2 分析

### **Skills 与 MCP**

[Skills 与 MCP 服务器可以自然协作](https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers)。一个竞争分析 skill 可以协调网页搜索、通过 MCP 访问的内部数据库、Slack 消息历史和 Notion 页面，综合出一份全面的报告。

### **非开发者的采用**

Skill 的创建正在从工程师扩展到跨学科的产品经理、分析师和领域专家。借助 skill-creator 工具，他们可以在 30 分钟内创建并测试自己的第一个 skill；该工具会以交互方式引导他们完成全过程。我们正在通过改进的工具和模板让 skill 的创建更加平易近人，让任何人都能捕捉并分享专业知识。

## **完整的架构**

把所有部分放在一起，正在成形的智能体架构像是以下几者的组合：

1. **智能体循环（agent loop）**：决定下一步做什么的核心推理系统
2. **智能体运行时（agent runtime）**：执行环境（代码、文件系统）
3. **MCP 服务器**：与外部工具和数据源的连接
4. **Skills 库**：领域专业知识与程序性知识

每一层都有明确的职责：循环负责推理，运行时负责执行，MCP 负责连接，skills 负责指引。这种分离让系统易于理解，也让每个部分可以独立演进。

想想给这个架构添加一个 skill 会发生什么。[前端设计 skill](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) 能立刻改变 Claude 的前端能力。它提供关于排版、色彩理论和动画的专业指引，且只在构建 Web 界面时激活。渐进式披露意味着它只在相关时才加载。添加新能力就是这么直接。

## **把 skills 部署到新的垂直领域**

这种「通用智能体 + MCP 服务器 + skills」的新兴模式，已经在帮助我们把 Claude 部署到新的垂直领域。

### **金融服务**

就在发布 skills 之后，我们用 skills 增强了[面向金融服务业的 Claude](https://www.anthropic.com/news/claude-for-financial-services)，让 Claude 对金融从业者更加有用：

- **DCF 模型构建器**：构建贴现现金流（DCF）模型，包含规范的 WACC 计算与敏感性分析
- **可比公司分析**：生成包含相关倍数与基准对比的可比公司（comps）表格
- **财报分析**：处理季度业绩并生成投资更新报告
- **首次覆盖报告**：结合财务模型构建全面的研究报告
- **尽职调查**：用标准化框架组织并购（M&A）分析
- **路演材料**：按照行业标准创建客户演示文稿

### **医疗健康与生命科学**

我们还用 skills 增强了[医疗健康与生命科学方面的产品](https://www.anthropic.com/news/healthcare-life-sciences)，让 Claude 对研究者、临床医生和医疗开发者更加有用：

- **生物信息学套件**：用于 scVI-tools 与 Nextflow 部署的 skills，对管理基因组流水线和单细胞 RNA 测序至关重要
- **临床试验方案生成**：加速临床研究的方案开发
- **科学问题遴选**：帮助研究者识别并框定有影响力的研究问题
- **FHIR 开发**：帮助开发者编写更准确的医疗数据互操作代码，以更少的错误更快地连接医疗系统
- **预先授权审查**：通过交叉核对保险覆盖要求、临床指南与患者病历，削减行政负担，加快患者获得所需诊疗的速度

## **把 Agent Skills 标准化**

为了实现这一愿景，我们正在把 [Agent Skills](https://agentskills.io) 作为开放标准发布。和 MCP 一样，我们相信 skills 应当可以跨工具、跨平台移植。同一个 skill 应该无论你使用 Claude 还是其他 AI 平台都能工作。我们一直在与生态成员合作制定这一标准，也很高兴看到早期的采用。

当有人第一次开始使用 AI 智能体时，它就应该已经知道你和你的团队在意什么，因为 skills 捕捉并传递了这些专业积累。随着这个生态的成长，社区中其他人构建的 skill 也能让你的智能体更有用、更可靠、更能干——无论你使用的是哪个 AI 平台。

## **开始使用**

我们正在收敛出一套通用智能体的架构，而 skills 提供了一个交付和分享新能力的范式。真正的价值来自我们共同构建的集体知识库：捕捉专业积累，在团队之间传递，让每一个智能体都比上一个更能干。

**资源：**

- [别构建智能体，去构建 Skills](https://youtu.be/CEvIs9y1uog?si=yhYQH-ZTX0DfNdtm)（YouTube 视频）
- [Skills 文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [GitHub 仓库](https://github.com/anthropics/skills)
- [Skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)
- [在 Claude 中使用 skills](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Skills API 快速上手](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Skills 最佳实践文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### **致谢：**

Barry Zhang、Mahesh Murag、Keith Lazuka、Ryan Whitehead

FAQ（常见问题）

---
title: "用 Claude Platform 降低成本并提升性能"
title_en: "Reducing cost and improving performance with Claude Platform"
source: https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 Claude Platform 降低成本并提升性能

> 原文：[Reducing cost and improving performance with Claude Platform](https://claude.com/blog/reducing-cost-and-improving-performance-with-claude-platform/) · Claude 博客

性能与成本常被视为一种取舍：想少花钱，就得接受更差的结果。实践中我们发现，许多使用 Claude Platform 的应用可以通过三项调整来削减成本而不牺牲性能：最大化提示缓存命中率、在升级到前沿 Claude 模型时清除提示中的反模式（anti-patterns）、以及把努力等级（effort）校准到与任务匹配。我们已把这份指南写进了 [`claude-api` 技能](https://github.com/anthropics/skills/tree/main/skills/claude-api)。本文将展示，配备 `claude-api` 的 Claude Code 往往能找到既降低成本、又保持甚至提升性能的办法。

## **提示缓存**

在 Claude 生成响应之前，它要先把你的提示处理成一种内部工作状态。这一步称为*预填充*（prefill），是处理输入时最昂贵的部分。提示缓存会把这一状态保存下来（即键值缓存，KV cache）：当请求以相同前缀开头时，Claude 直接读取它，而无需重新计算。缓存读取的[计费](https://platform.claude.com/docs/en/about-claude/pricing)只是完整输入价格的一小部分。

要有效使用提示缓存，有几项实际的注意事项。首先，提示缓存绑定在特定模型上。其次，提示缓存读取要求在整个提示范围内*逐字节完全一致*（byte-exact）。最后，提示缓存有[有限的存活时间](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#ttl-support)（TTL）。

牢记这几点之后，下面是一些实用建议：

- **避免在对话中途更改努力（effort）或思考设置**。这些设置会渲染在你的内容之前，属于缓存前缀的一部分。具体到 Claude Opus 5 和 Fable 5.1，你可以[在对话中途更新努力等级](https://platform.claude.com/docs/en/build-with-claude/effort#changing-effort-mid-conversation)而不破坏缓存。

- **把易变的值挡在前缀之外**。系统提示中的动态时间戳或 ID 可能在多次模型调用之间发生变化，从而破坏缓存。

- **避免会自行重排的工具定义**。使用 Claude Messages API 时，[提示按固定顺序组装](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#structuring-your-prompt)，工具定义渲染在顶部。对工具定义的任何改动都会破坏缓存。

- **分叉对话时要当心**。子智能体和分支只有在前缀逐字节完全一致、处于同一模型、且使用相同努力等级时，才会共享父对话的缓存。

- **避免超出缓存 TTL 的同步工具调用与子智能体**。如果智能体阻塞在一个长时间运行的工具调用或子智能体上，缓存可能在结果返回之前就过期。下一轮就得重写缓存，代价是正常输入价格的 1.25 倍（1 小时缓存为 2 倍），而不是便宜的读取价格。

### 如何修复

关于提示缓存管理，我们已经[积累](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)了一些经验教训：

- **仔细监控你的提示缓存命中率**。[Claude Console](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics) 提供提示缓存诊断，包括缓存未命中（cache miss）的原因分析（图 1）。如果命中率意外下滑，[缓存诊断 API](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics) 会准确告诉你两个请求在哪里产生了分歧。

图 1. Claude Console 可以通过比较连续的请求、准确找出提示前缀开始分歧的位置，来诊断意外的提示缓存未命中。

- **延后加载不常用的工具**。事先一次性声明所有工具，但把不常用的那些标记为 [defer_loading](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching#defer-loading-and-cache-preservation)：它们不进入缓存前缀，只在 Claude 通过工具搜索查到它们时才追加进对话，缓存因此得以保留。

- **以消息形式应用系统提示更新**。[Claude Platform](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#when-to-use-a-mid-conversation-system-message) 支持在对话中途以消息形式添加系统指令，而不必编辑系统提示，从而保住缓存。

- **排布请求，让稳定的部分保持稳定**。把静态上下文（工具定义和系统提示）放在前面，把不断增长的对话放在其后（图 2）。

图 2. 组织提示，确保动态内容被追加到稳定前缀的末尾。

- **在缓存注定要失效的时机更改模型或努力等级**。某些操作（如[压缩（compaction）](https://platform.claude.com/docs/en/build-with-claude/compaction)）本身就会重写大部分缓存（对话内容）。既然这次未命中（miss）的钱反正要花，这正是切换模型或努力等级的[好时机](https://cognition.com/blog/devin-fusion)。

- **随对话增长移动缓存断点**。在 Claude Platform 上，你可以设置[自动缓存](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#automatic-caching)，把缓存断点自动应用到最后一个可缓存块。

- **预热缓存**。为降低延迟，可以发送一个 `max_tokens: 0` 且带显式缓存断点的请求。这会处理提示并写入缓存，而不生成任何内容。如果你在会话开始时（比如用户还在输入时）执行这一步，第一个真正的请求就能命中热缓存。

- **不要超出提示缓存 TTL**。5 分钟的缓存 TTL 从请求开始时算起。如果智能体阻塞在运行超过 5 分钟的工具调用或子智能体请求上，父对话的缓存会在结果返回之前过期。这种情况下，可以考虑改为给前缀[设置 1 小时的 TTL](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)。

## **指令**

提示中会不断堆积用于弥补模型弱点的指令。相对于[最新 Claude 模型](https://x.com/trq212/status/2080710971228918066)的能力，这些指令可能已经过时。以下是一些常见的提示「反模式」，它们会拖累前沿 Claude 模型，还可能在不知不觉中推高成本：

- **验证仪式**。「*double-check your work*（反复检查你的工作）」「*verify twice before responding*（回答前验证两遍）」之类的指令常被前沿模型按字面执行，白白浪费 token。

- **强调彻底与加重语气的修饰语**。「Be maximally thorough（做到最大程度的彻底）」「CRITICAL: YOU MUST ALWAYS…（关键：你必须始终……）」在与前沿模型配合时可能导致冗长输出和多余的工具调用。

- **强制的流程与草稿区脚手架**。固定的分步流程（例如「在草稿区（scratchpad）里一步步思考」）或推理模板，是前沿模型并不需要的仪式。这类脚手架会叠加在模型的原生推理之上，消耗不必要的 token。

- **过时的示例**。针对旧模型失败模式调校的少样本示例，可能教会前沿模型在本不需要的请求上模仿冗长的推理链。

- **相互矛盾的规则**。前沿模型的指令遵循能力更强。相互矛盾的指令（「always refund within policy（始终按政策退款）」与「never issue refunds without escalation（未经升级绝不退款）」）会被前沿模型更机械地执行，导致性能劣化。

- **过期的配置**。为旧一代 Claude 编写的设置（例如手动思考预算）在升级到前沿模型时可能被 Claude Platform 拒绝。

### **如何修复**

我们已更新 `claude-api` 技能，加入了一个盯防这些反模式的新命令。在 Claude Code 中，对你的提示、技能或工具描述运行 `/claude-api prompt-audit`。审计覆盖工作目录中的所有内容，包括调用 Claude API 的应用代码，以及 Claude Code 自身的配置（例如 [CLAUDE.md](http://claude.md) 或技能）。

例如，我们在一个客服基准上测试了从 Opus 4.8 到 Opus 5 的模型迁移。我们从一份干净的提示出发，每次植入一个反模式（一个已废弃的思考设置、一对相互矛盾的退款规则、一个手动草稿区、「verify twice（验证两遍）」、「be maximally thorough（最大程度彻底）」，以及一个强制的六步流程），得到六份遗留提示。

我们把每份提示分别跑在 Opus 4.8 上、只改模型 ID 的 Opus 5 上，以及每份提示先跑一次 `/claude-api prompt-audit` 之后的 Opus 5 上（图 3 展示六份提示的平均值）。

图 3. 从 Opus 4.8 迁移到 Opus 5 期间，提示反模式的影响。

在 Opus 5 上，验证仪式（「verify twice」）会让每次退款都重复查询订单，浪费不必要的 token；强调语气的修饰语（「be maximally thorough」）则演变成了几十次不必要的知识库搜索。

运行 `/claude-api prompt-audit` 移除了这些反模式，平均降低成本 14.6%、提升准确率 5.3%。成本下降是因为多余的工具调用和重复的推理被消除。准确率上升有三个原因：那个已废弃的思考设置曾让 API 直接拒绝每一条路由请求；相互矛盾的退款规则曾导致 Opus 5 在要求客户确认时扣住了四笔本应退的款；而手动草稿区与 Opus 5 的内置思考相冲突——在三张工单上，它把工具调用写在了推理过程里，却从未执行。

## **努力等级**

[努力等级（effort）](https://platform.claude.com/docs/en/build-with-claude/effort)告诉 Claude「要使多大的劲」。低努力等级下，Claude 通常更快得出结论；高努力等级下，Claude 会在回答前深思熟虑、反复验证并探索其他备选方案。

同一模型在不同努力等级下的成本与性能表现可能差别很大。例如，在 FrontierCode Diamond（最难的 50 道题）上，Claude Fable 5 在低努力等级下得分为 11.5%，每题成本 $5.35；在最高努力等级下得分为 30.9%，每题成本 $19.00——调整努力等级让得分提高约 2.7 倍（+19 个百分点），代价约为 3.5 倍的成本（图 4）。

在 Claude Fable 5.1 上，Humanity's Last Exam（不使用工具）呈现出一条陡峭曲线，且最后一级收益递减：低努力等级下约得 53%，每题约 $0.30；最高努力等级下约得 61%，每题约 $2.23——最后一步到最高档只增加约半个百分点，成本却增加 46%。这一增益落在基准测试的运行间噪声之内，等于花了更多钱却买不到可测量的收益。

图 4. Fable 5 在 FrontierCode Diamond 上不同努力等级下的性能与成本。

努力等级在两个方向上都可能校准失当：

- **以为越高越好**。高努力等级可能导致*过度*思考：Claude 花在深思上的时间超出了任务所需，既增加成本和延迟，也可能降低答案质量。只有当仍有证据可挖时，深思才有帮助。

- **偏向低努力等级**。设得过低时，Claude 会在证据不足时就停下来。它发起的工具调用更少，可能根据第一个搜索结果而不是第三个来作答；在困难的步骤上想得更少，还会跳过它本来会主动执行的检查。答案看起来完成了，其实是建立在残缺信息之上的。

以下是一些实用的努力等级校准方法：

- **用更低努力等级测试更强的模型**。更强的模型配低努力等级，可能比较弱的模型拼命干（高努力等级）更便宜。例如，在 CursorBench 3.2 上，Claude Fable 5.1 以低努力等级[达到了](https://www-cdn.anthropic.com/0339e6a7c5c7b87f5c07798616dc32c215d14235/Claude%20Fable%205.1%20&%20Claude%20Mythos%205.1%20System%20Card.pdf) Fable 5 高努力等级的性能，成本只有其三分之一（图 5）。新模型更便宜有两个原因：低努力等级下每个任务做的工作更少；Fable 5.1 的提示缓存读取价格为每百万 token $0.25，而 Fable 5 为 $1.00。即便按 Fable 5 的价格计算，Fable 5.1 低努力等级的成本也要低约 40%。

图 5. Fable 5 与 Fable 5.1 在 CursorBench 3.2 上不同努力等级的对比。

- **了解你的任务形态。** 在[一整段努力等级区间上](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)测量应用性能，是理解你的具体任务的成本-性能取舍的有效方法。在一个未饱和的评测上，如果性能-成本曲线在各努力等级间保持平坦，说明任务并不受思考算力约束；提高努力等级没有好处。

这类校准往往需要在多个模型和努力等级上运行评测。在 Claude Code 中，`/claude-api hillclimb` 可以替你完成这一搜索：它把你的评测拆成训练集与测试集，提出配置修改建议，并通过阅读训练集中失败的样例来修复发现的问题。

我们在一个客服基准上运行了它，起点是默认（高）努力等级的 Opus 4.8。爬山算法（hillclimber）首先尝试了低努力等级的 Opus 5，并用 prompt-audit 移除了强制的工具调用仪式、草稿区步骤和矛盾规则。这一步越过了 Opus 4.8 的基线，训练准确率达 98.9%，成本降到每张工单 2.6 美分。

图 6. 爬山搜索通过更新模型选择、努力等级和提示来同时改善成本与性能。

随后它下探到低努力等级的 Sonnet 5，更便宜，每张工单只要 1 美分，但准确率掉到 88.9%。通过阅读训练集中失败的工单，Claude 在提示中加入了路由规则和退款上限的交叉引用，让 Sonnet 5 在同样成本下回到 98.9%。

在搜索从未见过的 14 张保留工单上，最终配置取得 90.5% 的成绩，而原始设置为 78.6%，成本约为原来的五分之一。

## **自动化降低成本**

提示缓存、指令和努力等级是降低成本的常用杠杆。我们的[文档](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence#cut-spend-without-losing-quality)覆盖了更多内容。为了对使用 Claude API 的应用代码做一次整体成本审计，我们新增了 `/claude-api cost-optimize`：它会剖析你的开销去向、实施成本削减，并在你提供评测时展示节省与性能之间的取舍。

`cost-optimize` 首先找出你的 token 花在哪里：如果你有 Claude Admin API 密钥，就从组织的[用量与成本报告](https://platform.claude.com/docs/en/manage-claude/usage-cost-api)读取；如果你的应用有记录，就从每个 API 响应的 usage 对象读取；两者都不行，就读取你构建请求的代码并做出估算。

接着它会对可用的节省手段排序：从提示缓存开始，精简每个请求携带的内容（包括一次 prompt-audit）、限制输出规模，以及把无人值守的工作[批量处理](https://platform.claude.com/docs/en/build-with-claude/batch-processing)。如果你提供评测，它还会更进一步，在不同努力等级和模型选择之间计算成本与性能。

我们在四个公开基准上运行了它，以 Sonnet 5 作为基线（图 7）：

- **LegalBench（成本降低约 58%）：** `cost-optimize` 提议跨任务缓存共享前缀、设置低努力等级，并通过 Batch API 处理任务。思考 token 从 102,779 降到 8,284，通过率保持在噪声范围内，成本下降约 58%。

- **tau2-bench retail（成本降低约 73%）：** 通过实现带显式断点布置的提示缓存，`cost-optimize` 把开销削减了 73%，通过率保持不变。

- **OfficeQA Pro（成本降低约 52%）：** `cost-optimize` 加入批处理和文档缓存，把成本从 $136.20 降到 $64.87。

- **SWE-bench Verified（成本降低约 55%）：** `cost-optimize` 发现默认配置的缓存已经正确。节省来自把努力等级设为中等，并把智能体的输出限制为寥寥几句简明陈述。每任务步数中位数从 29 降到 17，提示 token 从 75.2M 降到 33.7M。

图 7. 各基准在使用 /claude-api cost-optimize 后的成本与性能变化。

## **开始使用**

当你迁移到前沿 Claude 模型、想用新模型检验现有提示时，先从 `/claude-api prompt-audit` 入手。它会扫描工作目录中的提示、技能和工具描述——可以是调用 Claude API 的应用代码，也可以是 Claude Code 的配置（CLAUDE.md、技能）。它会移除拖累前沿模型的常见反模式。

当你的应用使用 Claude API、且你想做一次成本审计时，用 `/claude-api cost-optimize`。它会剖析 token 开销，然后尝试不同的杠杆：应用 prompt-audit，同时检查通过提示缓存、批处理无人值守工作或限制输出来降低成本的途径。如果你提供评测，它还会测量努力等级与模型选择之间的取舍。

最后，用 `/claude-api hillclimb` 在成本与性能之间做迭代搜索。给定一个评测，Claude 会把它拆成训练集和测试集，然后提出旨在降低成本、同时保持基线性能的应用更新建议。Claude 会阅读训练集中失败的样例来引导搜索方向，最终配置则在保留的测试集上打分。

了解更多：

- 查看我们的文档，见[这里](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence#cut-spend-without-losing-quality)
- 查看我们的 cookbook，见[这里](https://platform.claude.com/cookbook/cost-optimization-cost-optimization#prompt-caching)

FAQ（常见问题）

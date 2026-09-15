---
title: "Anthropic 如何用 Claude Code 执行大规模代码迁移"
title_en: "How Anthropic runs large-scale code migrations with Claude Code"
source: https://claude.com/blog/ai-code-migration/
crawled: 2026-09-14
translated: 2026-09-14
---

# Anthropic 如何用 Claude Code 执行大规模代码迁移

> 原文：[How Anthropic runs large-scale code migrations with Claude Code](https://claude.com/blog/ai-code-migration/) · Claude 博客

代码迁移——即把生产代码库移植到新语言的项目——直到不久前还是以年计的工程。

过去一个月里，Anthropic 的个别开发者使用 Claude Fable 5、Claude Opus 4.8 和[动态工作流](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)迁移了 10 个代码包，规模从数万到数十万行代码不等。本文将介绍其中两个例子，以及这些项目沉淀出的最佳实践。

Bun 联合创始人、Anthropic 技术成员 Jarred Sumner 用 Claude Code[把 Bun 从 Zig 迁移到了 Rust](https://bun.com/blog/bun-in-rust)。不到两周产出了 100 万行代码，合并前 Bun 既有测试套件在 CI 中 100% 通过。合并后出现了 19 处回归，目前均已修复。这个 Rust 移植版已于 6 月随 Claude Code 一起发布。

Anthropic Labs 联合负责人 Mike Krieger 在一个周末把一个 Python 代码库迁移成了 165,000 行 TypeScript。整个过程包括数百个智能体、8 个阶段门禁、3 轮对抗性评审，以及一次把每条命令的输出与 Python 原版逐一 diff 的最终一致性检查。

Claude Code 的新能力改变了这类长期被搁置项目的成本核算。下面是我们如今使用的六步流程，来自这些迁移带给我们的经验。

核心洞见是：你不要去修代码。**你要去修产生代码的那个流程（loop）。**

## 什么是 AI 代码迁移？

AI 代码迁移使用 AI 智能体把生产代码库移植到新的语言或框架。工程师不再手动逐文件翻译，而是编写迁移规则和验证回路（verification loop）；然后由智能体进行翻译、编译和测试，直到新代码的行为与原代码一致——把以年计的项目压缩到几周。

## **为什么迁移语言、何时迁移**

在直接进入"怎么做"之前，值得先讨论"什么时候"和"为什么"，因为围绕这类项目的假设已经发生了变化。

团队启动迁移，是因为从最初构建到现在，技术格局发生了变化：要么某个已知的取舍变成了掣肘，要么出现了更好的方案，要么原有生态正在萎缩。

例如，Jarred 当初选择 Zig 是因为它以极简主义提供了 C 级别的性能，非常适合一位独立创始人在"前 LLM 时代、在奥克兰一间狭窄公寓里用一年写出 Bun"。这种简洁性伴随着一些已知的取舍，[他在这里写了这些取舍](https://bun.com/blog/bun-in-rust#just-be-really-smart-and-don-t-make-mistakes)。

快进到 2026 年。Bun 的 CLI 每月下载量超过 1000 万次，并且在 Claude Code 内部被广泛使用。

就在上个季度，这些取舍还不足以成为冻结路线图、把资源投入一个跨季度项目的理由。迁移语言可以带来更小、更快、更安全的系统，但没人愿意为此买单。

软件工程师还必须面对这类昔日超大型项目固有的职业风险：你可能要并行维护两套代码库数个季度甚至数年，而如果最终结果只有 90% 的一致性，你面临的麻烦比开始时更大。

现在，最坏的结局不过是你删掉分支，重新再来。

当然，仍然需要一个站得住脚的商业理由。虽然百万行迁移不再需要像四年期项目那样耗费 300 万到 400 万美元的工程资源，但执行起来仍需数十万美元起步。以 Bun 迁移为例，它消耗了 59 亿未缓存输入 token 和 6.9 亿输出 token——按 API 定价约合 165,000 美元。Mike 的移植主体部分则消耗了 2700 万 token。

*Jarred 的百万行 PR。*

**不过，迁移的理由不再需要是"生死攸关"级别的。** 变更日志里一整年的内存缺陷补丁，或者一个长期存在的性能瓶颈，如今都足以构成迁移的理由。

编译步骤就是 Mike 那个项目的动因。他团队开发的内部工具以单个二进制文件的形式交付给用户。用 Python 工具链产出这个二进制文件，每个平台大约要 8 分钟，每次发布时整个构建矩阵累计要等约 30 分钟。移植之后，同样的编译现在只需大约 2 秒，二进制启动速度快了 6 倍，团队还因此淘汰了一条独立的部署流水线。

## **为什么 AI 改变了代码迁移的成本核算**

Claude Fable 5 是我们能力最强、已全面开放的模型。Fable 和 Opus 4.8 特别擅长委派、指导和验证并行的子智能体工作流，同时为既定目标寻找多条实现路径。

大型代码迁移对这类先进模型是一个特别有效的使用场景，因为：

- **工作本身是并行的。** 工作可以分散在数千个独立单元上，例如文件和 crate，智能体可以同时开工，而不必互相等待。
- **上下文清晰而完备。** 旧代码本身就是给模型的一份出色规格说明，也是构建翻译智能体所遵循指南时的核心参考。
- **自带裁判。** 许多大型代码库都带有测试套件，智能体可以用它来验证自己的工作。当验证是客观的，智能体的表现最好，因为模型可以对着一个事实基准连日打磨，无需人类来仲裁质量。
- **队列自己会长出来。** 当编译或测试运行失败时，它就成了智能体的下一个待修条目。
- **它们要求一致性与边缘情况处理。** 整个流程的设计让漂移无处藏身：评审者要为每一条发现引用背后的规则，违规会成为队列条目，而不是悄然发生的偏离。而当某个智能体真的撞上边缘情况时，修复方案会变成一条规则，此后每个智能体都会遵循。

正如下文所见，Mike 和 Jarred 都在迁移流程的关键步骤使用了 Fable，特别是以一种**顾问模式**使用多个模型等级来优化 token 消耗。

## **大型代码迁移的六个步骤**

*下面的流程已被泛化，适用于多种语言和场景。更多细节可以阅读*[*Jarred 的博客*](https://bun.com/blog/bun-in-rust)*。你也可以获取*[迁移入门套件](https://github.com/anthropics/code-migration-kit-with-claude-code)*。注：该入门套件是上述流程的通用模板——并不是这两个具体移植项目实际运行所用。*

### **前提条件**

启动迁移项目前，必须先有一个可靠的裁判（judge），否则你既没有退出条件，也没有成功标准。

这个裁判必须能够以同等标准评估原代码和目标代码。用原语言编写的测试套件往往依赖目标代码中不存在的内部函数。

构建这个裁判的方法：

- **给既有测试分类。** 让 Claude 识别哪些测试可以改写为外部调用，哪些依赖无法移植的内部实现。
- **为可移植性改写。** 把面向外部的测试转换成可以同时对原版和移植版运行的断言。再用对抗性智能体验证改写后的测试没有弱化断言。
- **验证裁判本身。** 在原代码上运行它，确认通过；再在故意写坏的代码上运行，确认失败——抓不出问题的裁判不配叫裁判。

Jarred 有一个用第三种语言（TypeScript）编写的大型测试套件，但大多数项目不会有这种条件。对于他的 Python 到 TypeScript 移植，Mike 构建了一个覆盖 7 个真实场景的一致性校验框架（parity harness），并把任何行为变化都视为必须修复的缺陷。

在进入各个阶段之前，下面这张图或许能帮你跟上节奏。它主要遵循 Jarred 的方法论，每个阶段都有评审和门禁。Mike 采用了类似的整体结构，使用类似的循环（loop）工作流，但他是端到端跑完整场迁移，再根据结果修订规则和工作流，然后重跑——每次都丢弃输出，直到第三轮才保留。

### **第 1 步 — 制定规则手册、依赖图和缺口清单**

在这个阶段，我们搭建迁移的地基：一份列出哪些代码需要重构而非简单翻译的清单、一本关于如何翻译代码的规则手册（rulebook），以及一张用于编排迁移实施工作流的依赖图。

顺序很重要：规则手册必须先于缺口清单。缺口清单由规则手册的默认规则覆盖不到的部分定义，二者还要在一次联合审计中共同接受检验。

#### **规则手册**

[规则手册](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/templates/RULEBOOK.md)的具体形态，取决于你在开始时必须做出的关键架构决策。其中最主要的一条是：新代码将沿用原有结构，还是彻底重新设计。

如果是前者（Jarred），规则手册主要就是一张张查找表，在两种语言之间翻译类型和惯用法，并对更难翻译的组件指向缺口清单。如果是后者（Mike），它会是一份设计文档。

Jarred 通过与 Claude 对话制定规则手册，为每个模糊地带形成一条策略。他还专门设计了 8 个子智能体，基于他自己的直觉分别评审 8 类常见失败模式。

#### **依赖图**

你需要理解文件之间的依赖关系，才能有效拆分并行迁移的工作流，知道哪些文件先迁移、哪些文件要放进同一批次。有些语言和代码库带有显式的清单文件（manifest），让这件事很容易；但对于遗留代码库以及 C/C++、Python 这类主流语言，这些依赖需要被发现并绘制成图。

Claude Code 可以派出智能体创建并运行一个确定性脚本来生成这张依赖图。[迁移套件中的提示](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/01-dependency-map.md)使用一个工作流来构建"评审-修复"循环。注：该入门套件是本文所述流程的通用模板——并不是这两个具体移植项目实际运行所用。

#### **缺口清单与怀疑者评审者**

新语言有着旧语言所没有的、必须满足的要求。从 Zig 到 Rust，差异在于手动内存管理（C 和 C++ 也是如此）。例如：

Zig

```
fn readConfig(allocator: std.mem.Allocator) ![]u8 {
    const buf = try allocator.alloc(u8, 1024);
    // ...fill buf...
    return buf; // caller must free this — but only the comment says so
}

// A caller that forgets 'defer allocator.free(buf)' still compiles — the leak only surfaces at runtime.
```

Rust

```
fn read_config() -> Vec<u8> { 
let buf = vec![0u8; 1024]; 
// ...fill buf... 
buf // ownership moves to the caller; memory is freed automatically 
} 
// Use it after it's moved? Free it twice? Neither compiles. 
// Forget to free it? There's no free call to forget — drop is automatic.
```

从 Python 到 TypeScript，缺口则是接口与契约。Python 不要求声明它接受什么形状的对象、返回什么，而 TypeScript 要求。例如：

Python

```
def register(handler):
    handler.setup()
    return handler.run({"retries": 3})

# Any object with .setup() and .run() works here. Which objects actually get passed in? Read the whole codebase to find out.

```

TypeScript

```
interface RunResult { ok: boolean } 

interface Handler 
{ setup(): void; 
run(opts: { retries: number }): Promise<RunResult>; 
} 

function register(handler: Handler): Promise<RunResult> { 
handler.setup(); 
return handler.run({ retries: 3 }); } 

// The contract must be written down before this compiles
```

Jarred 和 Mike 都创建了记录这类隐性知识的缺口清单文件。Jarred 选择提前盘点这些缺口（也就是我们在这里的做法），而 Mike 选择先翻译、再通过事后审计来建立缺口清单。你可能是两种都要做。

可以参考这个[用于创建缺口清单文件的 Claude Code 提示示例](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/02-gap-inventory.md)。

### **第 2 步 — 压力测试规则**

这一步是一次小型迁移，为整个大型迁移充当"试航"（shakedown cruise）。

在这一步，Jarred 用一个智能体依照规则手册翻译 3 个文件，用一个智能体"像一位资深 Rust 工程师那样"翻译 3 个文件，再用一个智能体根据 diff 提炼新的翻译规则。在这个阶段他抓住了两个关键问题——如果扇出到全部 1,448 个文件，它们会制造无数麻烦。

提示可能[长这个样子](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/03-stress-test.md)。

这种压力测试**只适用于保持结构的迁移**，即同一文件的两个翻译版本可以逐行对比。如果你的规则手册是一次重新设计——像 Mike 的那样——等效的测试就是让对抗性评审者直接攻击设计文档，然后用一次一次性的端到端运行来验证它。

无论如何，把翻译出的文件全部丢掉。目标是打磨规则，不是取得增量进展。

### **第 3 步 — 翻译全部代码**

从这一步起，你运行的是同一套多智能体循环架构：实现、评审、修复。

你可以把实现者的工作交给较小的模型，把评审者留在较大的模型上。例如，Mike 在为迁移主体扇出 12 个子智能体时使用的是 Claude Sonnet。

工作队列应该是机械的。一个批处理脚本通过检查翻译后的文件是否存在于磁盘上来判定完成状态，然后把待办文件切分成批次交给实现者智能体。由于队列每次都从磁盘重建，这场迁移在结构上就是可恢复的。

在这个阶段，智能体对自己做多少工作可能过于保守。解决办法可以是一条直白而强硬的提示指令，并附上"编译器会在下一步抓住错误"的上下文。

翻译器没有把握执行的任何部分，都以 // TODO(port): <reason> 标记，留待第 4 步处理。从这里开始，待办清单会自己长出来：编译器枚举错误，冒烟测试找出崩溃，测试套件报告失败。

两个对抗性评审者在各自独立的上下文中评估实现者的工作，评审者之间的分歧交由第三个智能体裁决。当一个评审者跨文件反复抓到同一个错误时，修复不应是逐文件打补丁，而是在规则手册里加一句话，然后重新生成受影响的批次。规则手册在这一步持续生长；代码从不绕过它被手工修补。

这一步有一个值得注意的重要设计决策：编译器放在哪里。Mike 把 TypeScript 编译器放进了每一个循环，因为它能在几秒内检查一个单元。Jarred 则完全禁止编译器进入循环，把它推迟到下一步，因为 cargo 一次要跑几分钟。

到了这一步，大量繁重工作已经完成，[提示开始变短](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/prompts/04-translation-kickoff.md)。

### **第 4、5、6 步 — 编译、运行、对齐行为**

这三步共享同一套循环架构，且需要的人类判断逐步减少，所以我们放在一起讲。

**第 4 步**，举例来说，取决于语言和迁移规模，经常会被并入第 3 步。

视编译步骤的规模和难度而定，智能体可能根本不必单独运行这一步。Jarred 用一个编排脚本在整个工作区上一次性调用编译器来执行这一步。然后"修复者智能体"（fixer agent）带着对抗性评审并行处理错误清单。重新构建，如此往复。

审阅错误清单有助于发现可能需要调整的系统性问题。例如，Jarred 遇到过数千个 Rust 模块错误——它们是在修复循环导入（Zig 的惰性编译一直容忍着这些循环）之后集中暴露的。他通过在循环中编码"判断该删除、移动还是重构哪个依赖边界"的逻辑修复了这个循环。

**第 5 步**同样有一个类似编译器错误清单的机械事实来源：冒烟测试的崩溃。同样，循环的修复方式是把问题归类——这里是按根本原因分组，再由对抗性子智能体评审。

**第 6 步**，也就是我们故事的终点，是比较两个代码库中程序的行为。

至此，文件已经完成翻译、编译和冒烟测试。现在该把它们分片（shard），对其运行（来自前提条件阶段的）测试套件。用"修复者智能体"对照两个代码库评审失败的测试，逐个攻克；对抗性评审者则检查它们的修复。

这个循环的下一个环节是一个[构建守护进程（build daemon）](https://github.com/anthropics/code-migration-kit-with-claude-code/blob/main/scripts/build_daemon.sh)，它是唯一被允许重新构建二进制文件的进程。修复者提交补丁；守护进程把补丁攒成一批、只重建一次、重跑受影响的测试，并把结果反馈回来。这把最昂贵的操作串行化，而不是放任多个智能体各自独立触发它。

当同一个失败在许多测试中重复出现时，修复就要上移一层：修订产生这个缺陷的那条规则，只重新生成该规则触及的文件。

Mike 的做法在这里很有参考价值，因为许多开发者并没有现成或已移植的测试套件。Mike 让 Claude 写了一个小脚本，对新的移植版和原 Python 代码库运行 7 个真实场景并 diff 结果。每个失败的场景都有自己的修复智能体，循环一直跑到 7 个全部通过。

然后他更进一步。Claude 自己设计了一套端到端测试套件，并在夜间自主运行，修复破损之处，一连四个晚上反复执行。结果，它抓住了任何场景清单都无法预料的那些小磕小碰。

这一课是：缺少测试套件并不阻塞这一步。如果不能继承一个裁判，就让 Claude 造一个。无论哪种方式，你的原代码库就是事实基准。

## **代码迁移最佳实践**

每一轮运行都教会我们一些上一轮没有的东西。可以肯定，你的下一次迁移也会教会你本指南写不到的东西。但有几条实践在所有项目中都站住了脚：

- **不要盲目照搬本指南。** 每场迁移都不一样。把它当作起点，在正式投入之前先和 Claude 一起规划你的具体迁移。
- **不要盯着单个失败。** 单个失败是循环的活儿。修复者智能体会把它们烧光。你的注意力应该放在模式上。
- **让评审对抗化，让验证机械化。** 对抗性评审支撑得起更长时间运行的任务，通常也值得那份 token 消耗。让脚本——编译器、diff、测试套件——当裁判。
- **不要事事都用最大的模型。** token 花销集中在你的循环里，所以要精心设计它们。较小的模型很擅长处理高吞吐量的实现扇出；把你最大的模型留给评审者，以及任何会写出供其他智能体遵循的规则的工作。
- **把人类工时前置。** 规则手册和压力测试最耗时。之后的一切基本上都是队列在燃烧。
- **让工作队列机械化、可恢复。** "完成"应当意味着"输出文件存在于磁盘上"。

## **评审循环的结果，而不是代码**

Jarred 的 Bun 迁移现已进入生产环境，尽管每场迁移都有取舍。例如，大约 4% 的 Rust 代码位于 "unsafe" 块内，大多是在 C/C++ 边界上的单行指针操作。

但新代码库确实更好了，而且是可度量的好：团队工具能检测到的每一个内存泄漏都已修复——一项重复构建 2,000 次的基准测试，内存占用从 6,745 MB 降到了 609。二进制文件在 Linux 和 Windows 上小了 19%。跨语言优化让它在 HTTP 服务和 next build、tsc 这类真实工作负载上快了 2–5%。

想一想，是不是该重新算一算那场被你搁置已久的迁移的账了。挑出你一直忍受着的那个代码库，问问 Claude 它的迁移流程会是什么样。

***相关资源***

- [*迁移入门套件*](https://github.com/anthropics/code-migration-kit-with-claude-code)*注：该入门套件是上述流程的通用模板——并不是这两个具体移植项目实际运行所用。*
- [*代码现代化插件（Code-modernization plugin）*](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization)*——面向遗留系统现代化与框架升级，而非语言移植*
- [*Claude Code 中的动态工作流*](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)

FAQ（常见问题）

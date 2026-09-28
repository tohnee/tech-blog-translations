---
title: "AlphaEvolve：面向科学与算法发现的编码智能体"
title_en: "AlphaEvolve: A coding agent for scientific and algorithmic discovery"
source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf
crawled: 2026-09-23
translated: 2026-09-23
---

# AlphaEvolve：面向科学与算法发现的编码智能体

> 原文：[AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf) · DeepMind 技术报告（CS329A 指定阅读）

Alexander Novikov\*、Ngân Vũ\*、Marvin Eisenberger\*、Emilien Dupont\*、Po-Sen Huang\*、Adam Zsolt Wagner\*、Sergey Shirobokov\*、Borislav Kozlovskii\*、Francisco J. R. Ruiz、Abbas Mehrabian、M. Pawan Kumar、Abigail See、Swarat Chaudhuri、George Holland、Alex Davies、Sebastian Nowozin、Pushmeet Kohli 与 Matej Balog\*

Google DeepMind¹

¹见「致谢与作者信息」一节。\*贡献相同。

© 2025 Google DeepMind. 保留所有权利。

在本白皮书中，我们介绍 AlphaEvolve——一种进化式编码智能体（evolutionary coding agent），能够显著增强最先进大语言模型（LLM）在极具挑战性任务上的能力，例如攻克开放科学问题或优化计算基础设施的关键组件。AlphaEvolve 编排一条由 LLM 组成的自主流水线，其任务是通过直接修改代码来改进算法。采用进化方法并持续从一个或多个评估器接收反馈，AlphaEvolve 迭代地改进算法，从而可能带来新的科学与实践发现。我们通过将其应用于多个重要的计算问题，展示了这一方法的广泛适用性。在优化 Google 大规模计算栈的关键组件时，AlphaEvolve 为数据中心开发出更高效的调度算法，在硬件加速器的电路设计中找到一处功能等价的简化，并加速了支撑 AlphaEvolve 自身的那一 LLM 的训练。此外，AlphaEvolve 发现了新颖且可证明正确的算法，在数学与计算机科学的一系列问题上超越了最先进的解决方案，显著拓展了此前自动化发现方法（Romera-Paredes et al., 2023）的适用范围。值得注意的是，AlphaEvolve 开发出一种搜索算法，找到了用 48 次标量乘法完成两个 4×4 复值矩阵相乘的过程；这是 56 年来在该设定下对 Strassen 算法的首次改进。我们相信，AlphaEvolve 及与其类似的编码智能体能够在改善许多科学与计算领域问题的求解方面产生重大影响。

## 1. 引言

发现新的高价值知识——例如做出新颖的科学发现或开发出具有商业价值的算法——通常需要一个漫长的过程：构思、探索、放弃没有前景的假设、实验与验证。

近来，人们对使用大语言模型（LLM）来自动化这一过程的相当多环节兴趣浓厚。成功的希望来自近期 LLM 令世人瞩目的能力 [32, 76]——它们能够利用测试时计算增强自身能力——以及将语言生成与行动结合起来的智能体的兴起 [88, 114]。这些进展改善了在一系列既有基准测试上的表现，并加速了假设生成 [34] 与实验设计 [7, 43] 等面向发现的任务。然而，要让 LLM 流水线一路走通、做出全新的科学或实践发现，仍然充满挑战。

在本白皮书中，我们提出一个名为 AlphaEvolve 的 LLM 代码超优化（superoptimization）智能体，它结合进化计算与基于 LLM 的代码生成来应对这一挑战。AlphaEvolve 聚焦于科学与工程发现问题的广泛谱系——只要发现的候选者能够被自动评估。它把候选者（例如新的数学对象或实用启发式）表示为算法，并用一组 LLM 来生成、评析（critique）并进化这样一个算法池。LLM 主导的进化过程以代码执行与自动评估作为锚定（grounding）。这一评估机制使 AlphaEvolve 能够避开基础 LLM 的任何错误建议 [44]。

AlphaEvolve 中的进化过程利用了现代 LLM 对反馈做出响应的能力，使其能够发现与初始候选池在语法和功能上都截然不同的候选者。它既适用于以发现新算法为内在目标的问题，也适用于一类广泛的问题——其中感兴趣的解并非算法本身，而是算法可以描述该解如何被构造或找到。在后一种情形中，发现算法只是工具性目标，但事实证明，相比直接搜索解本身，这是一种出人意料有效的策略 [83]。

将进化方法与编码 LLM 相结合的思想，此前已在多种专门场景中被探索过。特别地，AlphaEvolve 是对 FunSearch [83] 的实质性增强（见表 1）——后者使用 LLM 引导的进化来发现启发式，以构造新颖的数学对象或驱动在线算法的运行。此外，相关方法还曾被用于诸如为仿真机器人发现策略 [57]、符号回归 [35, 89]，以及为组合优化合成启发式函数 [63] 等任务。与这些系统不同，AlphaEvolve 利用最先进（SOTA）的 LLM 来进化实现复杂算法的大段代码——这些算法横跨多个函数与组件。因此，它在规模与通用性上都能显著超越其前辈。

| FunSearch [83] | AlphaEvolve |
|---|---|
| 进化单个函数 | 进化整个代码文件 |
| 最多进化 10–20 行代码 | 最多进化数百行代码 |
| 用 Python 进化代码 | 可用任意语言进化 |
| 需要快速评估（1 CPU 上 ≤ 20 分钟） | 可在加速器上并行评估数小时 |
| 使用了数百万个 LLM 样本 | 数千个 LLM 样本即已足够 |
| 使用小 LLM；更大的模型无益 | 受益于 SOTA LLM |
| 上下文极少（仅先前的解） | 提示中包含丰富上下文与反馈 |
| 优化单一指标 | 可同时优化多个指标 |

表 1|AlphaEvolve 与我们此前智能体的能力与典型行为对比。

虽然自动评估指标为 AlphaEvolve 提供了关键优势，它同时也是一种限制——特别是，它把需要人工实验的任务排除在我们的范围之外。由于数学、计算机科学与系统优化中的问题通常允许自动评估指标，我们在 AlphaEvolve 上的努力聚焦于这些领域。具体而言，我们用 AlphaEvolve 在算法设计与构造性数学中若干著名开放问题上取得进展，并优化 Google 大规模计算栈中的关键层。

在算法设计方面，我们考虑发现快速矩阵乘法算法这一根本问题——此前已有更专门化的 AI 方法应用于该问题 [26]。尽管是通用目的的，AlphaEvolve 超越了 [26]，改进了 14 个矩阵乘法算法的 SOTA；值得注意的是，对于 4×4 矩阵，AlphaEvolve 通过发现一个使用 48 次乘法来乘两个 4×4 复值矩阵的算法，改进了 Strassen（1969）的算法。²

> ² 这些被发现的算法以及我们的其他新数学结果可在 https://colab.research.google.com/github/google-deepmind/alphaevolve_results/blob/master/mathematical_results.ipynb 查看。

在数学方面，我们考虑一系列广泛的开放问题，这些问题可以通过发现构造（对象）取得进展——按照给定的数学定义，这些构造具有优于所有已知构造的性质。我们将 AlphaEvolve 应用于大量（超过 50 个）此类问题，并在其中约 75% 上匹配了已知最好的构造（许多情形下这些构造很可能已是最优）。在约 20% 的问题上，AlphaEvolve 超越了 SOTA，发现了新的、可证明更好的构造。其中包括对 Erdős 提出的最小重叠问题（Minimum Overlap Problem）[25] 的改进，以及 11 维 kissing numbers 问题上的一个改进构造 [8, 31]。

最后，我们在四个跨越 Google 计算栈不同层的工程问题中使用 AlphaEvolve：为 Google 的集群管理系统发现调度启发式、优化用于训练 LLM 的矩阵乘法内核、优化 TPU 内使用的算术电路，以及优化 Transformer 中注意力的运行时间。由于这些组件会被长时间反复运行，任何改进都极具价值。

## 2. AlphaEvolve

Human defines "What?"
sets evaluation criteria, provides initial solution
and optional background knowledge
AlphaEvolve figures out "How?"
Improved
solution
LLMs ensemble
Prompt sampler
Evaluators pool
Program database
rich context containing
past trials and ideas
proposals of
improved programs
programs with quality scores
and other feedback
programs to improve
and act as inspiration
Problem
definition

图 1|AlphaEvolve 高层概览。

AlphaEvolve 是一个编码智能体，它编排一条自主计算流水线（其中包括对 LLM 的查询），并产出完成用户指定任务的算法。从高层看，这一编排过程是一个进化算法，逐步开发出在任务相关自动评估指标上得分更高的程序。AlphaEvolve 的高层概览见图 1，图 2 给出展开视图。

```
Initial program
with components
to evolve
Prompt template
and configuration
Choice of existing
or custom LLMs
Scientist / Engineer
Best program
AlphaEvolve
Evaluation code
Distributed Controller Loop
parent_program, inspirations = database.sample()
prompt = prompt_sampler.build(parent_program, inspirations)
diff = llm.generate(prompt)
child_program = apply_diff(parent_program, diff)
results = evaluator.execute(child_program)
database.add(child_program, results)
Evaluators pool
LLMs ensemble
Prompt sampler
 Program database
```

图 2|AlphaEvolve 发现过程的展开视图。用户提供初始程序（标记了待进化的组件）、评估代码与可选配置（2.1 节）。AlphaEvolve 随后启动一个进化循环。提示采样器（Prompt sampler）利用程序数据库（Program database）中的程序构造丰富的提示（2.2 节）。给定这些提示，LLM 生成代码修改（diff），这些修改被应用以创建新程序（2.3 节）。新程序随后由评估器（Evaluators）评分（2.4 节），有希望的解被登记回程序数据库（2.5 节），驱动越来越好程序的迭代发现。

### 2.1. 任务规约

**评估。** 由于 AlphaEvolve 处理的是解可被机器评分的问题，用户必须提供一种自动评估所生成解的机制。该机制采取函数 ℎ 的形式，把一个解映射到一组标量评估指标。按惯例，这些指标被最大化。在我们目前的设置中，ℎ 通常实现为一个名为 evaluate 的 Python 函数，具有固定的输入/输出签名，返回一个标量字典。

视应用而定，执行该函数可能只在单台设备上耗时数秒，也可能引发大规模计算。对数学问题而言，函数 ℎ 通常非常简单。例如，当希望找到满足给定性质的最大图时，ℎ 调用进化出的代码生成一个图，检查该性质是否成立，然后简单地返回图的大小作为分数。在更复杂的情形中，函数 ℎ 可能涉及执行一个进化出的搜索算法，或训练并评估一个机器学习模型。

**API。** 为支持在代码库中进化多个组件，AlphaEvolve 暴露一个输入 API，其中代码块可被注记为由系统进化；见图 3a 的示例。这一设计便于将其与现有代码库集成，只需向代码中添加特殊标记（# EVOLVE-BLOCK-START 与 # EVOLVE-BLOCK-END）作为注释，改动极小。

进化块中用户提供的任何代码都作为初始解，交由 AlphaEvolve 改进；其余代码构成骨架，把进化出的片段连接起来，使它们能从 evaluate 中被调用。虽然这一初始实现必须是完整的，但它可以是简陋的——例如，由返回适当类型常量的单行函数组成。

**选择抽象层面的灵活性。** AlphaEvolve 可以用截然不同的方式应用于同一问题——尤其当进化出的程序并非最终输出、而是发现解的手段时。例如，AlphaEvolve 可以用原始字符串表示来进化解（如经典进化算法那样）；进化一个具有确定形式的函数，指定如何从零开始构造解（[83] 采用的方法）；进化一个定制的搜索算法，在某个固定计算预算内找到解；甚至共同进化中间解与搜索算法，使每个搜索算法都专门为进一步改进某个特定中间解而量身定制。我们发现不同抽象层面适用于不同问题。例如，我们推测对于解高度对称的问题，进化构造函数更有利，因为它们往往更简洁 [83]；而对于解非对称的问题，进化定制的搜索算法效果更好。

### 2.2. 提示采样

由于 AlphaEvolve 利用 SOTA LLM，它支持多种定制方式，并可在主进化提示中提供长上下文。该提示包含从程序数据库采样出的多个先前发现的解，以及关于如何对特定解提出变更的系统指令。除这些关键成分外，用户还可以按自身需要以不同方式进一步定制提示，例如：

- **显式上下文**：关于所求解问题的细节，例如固定的人工书写指令、公式、代码片段或相关文献（如 pdf 文件）。
- **随机化格式**：带有人工提供的备选内容的模板占位符，以增加多样性，并使用单独配置文件中给出的概率分布实例化。
- **渲染后的评估结果**：通常包括一个程序、执行该程序的结果，以及 evaluate 函数赋予的分数。
- **元提示进化**（meta prompt evolution）：由 LLM 本身在额外的提示生成步骤中建议的指令与上下文，在与解程序类似的另一个独立数据库中共同进化。

### 2.3. 创造性生成

为驱动进化过程，AlphaEvolve 利用 SOTA LLM 的能力，其主要角色是消化有关先前已开发解的信息，并提出新颖、多样的改进方式。尽管 AlphaEvolve 与模型无关，但在消融实验中我们观察到，随着底层 LLM 的改进，AlphaEvolve 表现得越来越好（见第 4 节）。

# EVOLVE-BLOCK START
"""Image classification experiment in jaxline."""
import jax
...
# EVOLVE-BLOCK-END
...
# EVOLVE-BLOCK-START
class ConvNet (hk.Module):
def __init__(self, num_classes): ...
def __call__(self, inputs, is_training): ...
def sweep():
return hyper.zipit([...])
# EVOLVE-BLOCK-END
...
def evaluate(eval_inputs) -> dict[str, float]:
...
return metrics
(a)

The current model uses a simple ResNet architecture with only
three ResNet blocks. We can improve its performance by
increasing the model capacity and adding regularization. This
will allow the model to learn more complex features and
generalize better to unseen data. We also add weight decay to
the optimizer to further regularize the model and prevent
overfitting. AdamW is generally a better choice than Adam,
especially with weight decay.
<<<<<<< SEARCH
self._block1 = ResNetBlock(num_channels)
self._block2 = ResNetBlock(num_channels * 2, stride=2)
self._block3 = ResNetBlock(num_channels * 4, stride=2)
=======
self._block1 = ResNetBlock(num_channels)
self._block2 = ResNetBlock(num_channels, stride=1)
self._block3 = ResNetBlock(num_channels * 2, stride=2)
self._block4 = ResNetBlock(num_channels * 2, stride=1)
self._block5 = ResNetBlock(num_channels * 4, stride=2)
self._block6 = ResNetBlock(num_channels * 4, stride=1)
>>>>>>> REPLACE
<<<<<<< SEARCH
def optimizer(self, learning_rate):
return optax.adam(learning_rate)
=======
def optimizer(self, learning_rate):
return optax.adamw(learning_rate, weight_decay=1e-4)
>>>>>>> REPLACE
(c)

Act as an expert software developer. Your task is to iteratively
improve the provided codebase. [...]
- Prior programs
Previously we found that the following programs performed well
on the task at hand:
top_1_acc: 0.796; neg_eval_log_loss: 0.230; average_score: 0.513
"""Image classification experiment in jaxline."""
[...]
class ConvNet (hk.Module):
"""Network."""
def __init__(self, num_channels=32, num_output_classess=10):
super().__init__()
self._conv1 = hk.Conv2D(num_channels, kernel_shape=3)
self._conv2 = hk.Conv2D(num_channels * 2, kernel_shape=3)
self._conv3 = hk.Conv2D(num_channels * 4, kernel_shape=3)
self._logits_module = hk.Linear(num_output_classes)
[...]
- Current program
Here is the current program we are trying to improve (you will
need to propose a modification to it below).
top_1_acc: 0.862; neg_eval_log_loss: 0.387; average_score: 0.624
"""Image classification experiment in jaxline."""
[...]
class ConvNet (hk.Module):
"""Network."""
def __init__(self, num_channels=32, num_output_classes=10):
super().__init__()
self._conv1 = hk.Conv2D(num_channels, kernel_shape=3)
self._block1 = ResNetBlock(num_channels)
self._block2 = ResNetBlock(num_channels * 2, stride=2)
self._block3 = ResNetBlock(num_channels * 4, stride=2)
self._logits_module = hk.Linear(num_output_classes)
[...]
SEARCH/REPLACE block rules:
[...]
Make sure that the changes you propose are consistent with each
other. For example, if you refer to a new config variable
somewhere, you should also propose a change to add that
variable.
Example:
[...]
Task
Suggest a new idea to improve the code that is inspired by your
expert knowledge of optimization and machine learning.
Describe each change with a SEARCH/REPLACE block.
(b)

图 3|将 AlphaEvolve 应用于进化一个监督学习流水线的示例。所有代码片段均为节选，省略号（...）表示跳过的行。(a) 用户提供的文件，其中标记了待进化的块，以及可为当前版本代码打分的特殊 evaluate 函数。(b) 组装后提供给 LLM 的提示示例。(c) LLM 生成的输出示例。(c) 中提出的 diff 将被应用于提示 (b) 中展示的「当前程序」，修改后的程序随后被送往评估器。评估器将调用 (a) 中的 evaluate 函数以获得新提议程序的分数。

**输出格式。** 当 AlphaEvolve 要求 LLM 修改现有代码（尤其是在较大代码库中）时，它要求变更以特定格式的 diff 块序列给出：

```
<<<<<<< SEARCH
# Original code block to be found and replaced
=======
# New code block to replace the original
>>>>>>> REPLACE
```

这里，`<<<<<<< SEARCH` 与 `=======` 之间的代码是要在当前程序版本中精确匹配的片段；`=======` 与 `>>>>>>> REPLACE` 之间的代码是将替换原片段的新片段。这允许对代码的特定部分进行有针对性的更新。

当被进化的代码非常短，或当完整重写比小修小改更合适时，AlphaEvolve 可配置为让 LLM 直接输出整个代码块，而不使用 diff 格式。

**所用模型。** AlphaEvolve 采用大语言模型的集成（ensemble）。具体而言，我们使用 Gemini 2.0 Flash 与 Gemini 2.0 Pro 的组合。这种集成方式使我们能在计算吞吐量与所生成解的质量之间取得平衡。Gemini 2.0 Flash 延迟更低，能实现更高的候选生成速率，增加单位时间内探索的想法数量；与此同时，能力更强的 Gemini 2.0 Pro 会提供偶尔出现的高质量建议，能显著推进进化搜索并可能带来突破。这种策略性组合在最大化被评估想法的体量的同时，保留了由更强模型驱动实质性改进的潜力，从而优化整体发现过程。

### 2.4. 评估

为跟踪 AlphaEvolve 的进展并选择哪些想法传播到后续世代，LLM 提出的每个新解都会被自动评估。原则上，这一过程只是对生成的解执行用户提供的评估函数 ℎ。实践中，AlphaEvolve 支持若干可选机制，使评估更灵活、更高效：

- **评估级联（假设检验）**：用户可以指定难度递增的测试用例集合，使得新解只有在所有更早阶段都取得足够有希望的结果时，才在下一阶段被评估。这有助于更快剪除前景较差的解。此外，新解在被主要测试用例检验之前先小规模评估，以便尽早过滤掉有故障的程序。
- **LLM 生成的反馈**：在某些应用中，理想的解具有某些难以在用户提供的评估函数 ℎ 中精确刻画的特性，例如所发现程序的简洁性。这些性质可以用单独的 LLM 调用来评分并加入分数字典以引导进化，也可用于在准则不满足时丢弃解。
- **并行化评估**：AlphaEvolve 的样本效率使得为评估任一新解花费约 100 计算小时成为可行。然而，除非把单次评估并行化以缩短其墙钟时长，否则这会拖慢新世代出现的速率，限制进化算法施加若干连续变异的能力。在许多应用中，评估是「尴尬并行」（embarrassingly parallel）的（例如从多个随机初始化运行一个搜索算法），使 AlphaEvolve 能通过对评估集群的异步调用来分发这项工作。

**多分数。** AlphaEvolve 允许优化多个用户提供的分数，即进化在一个或多个评估指标下取得高分的对象。这既有内在价值也有工具价值。虽然在多种应用中我们确实关心为多个评估指标开发解（或同时在所有指标上都强的单一解），但我们发现，即使只有一个指标特别令人关注，为多个指标做优化也常常能改善该单一目标指标上的结果。这或许是因为，在不同评估准则下表现出色的程序往往具有不同的结构或逻辑，而通过把这些多样的高性能程序——每一个都代表一种不同的「好」的定义——纳入提供给语言模型的提示，我们可以激发生成更多样的候选解，增加发现对目标指标高度有效的新方法的机会。

### 2.5. 进化

在其进化过程中，AlphaEvolve 持续生成数量不断增长的解，其上附有评估结果（分数与程序输出）。这些解存储在一个进化数据库中，其主要目标是以最优方式在后续世代中重新呈现先前探索过的想法。设计此类数据库的关键挑战是平衡探索（exploration）与利用（exploitation），在持续改进最佳程序的同时保持多样性，以鼓励对整个搜索空间的探索。在 AlphaEvolve 中，进化数据库实现了一个受 MAP-Elites 算法 [74] 与基于岛屿的种群模型 [83, 97] 之组合启发的算法。

### 2.6. 分布式流水线

AlphaEvolve 被实现为一个异步计算流水线（使用 asyncio Python 库），其中许多计算并发运行，每项计算在其下一步依赖另一尚未完成的计算的结果时才阻塞（等待）。更具体地说，该异步流水线由控制器、LLM 采样器与评估节点组成。整条流水线针对吞吐量（而非任何单个特定计算的速度）优化，以便在特定的总体计算预算内最大化可被提出并评估的想法数量。

| ⟨m, n, p⟩ | 已知最好 [参考文献] | AlphaEvolve |
|---|---|---|
| ⟨2, 4, 5⟩ | 33 [42] | 32 |
| ⟨2, 4, 7⟩ | 46 [93] | 45 |
| ⟨2, 4, 8⟩ | 52 [93] | 51 |
| ⟨2, 5, 6⟩ | 48 [93] | 47 |
| ⟨3, 3, 3⟩ | 23 [52] | 23 |
| ⟨3, 4, 6⟩ | 56 [48] | 54 |
| ⟨3, 4, 7⟩ | 66 [91] | 63 |
| ⟨3, 4, 8⟩ | 75 [91] | 74 |
| ⟨3, 5, 6⟩ | 70 [48] | 68 |
| ⟨3, 5, 7⟩ | 82 [91] | 80 |
| ⟨4, 4, 4⟩ | 49 [95] | 48 |
| ⟨4, 4, 5⟩ | 62 [47] | 61 |
| ⟨4, 4, 7⟩ | 87 [93] | 85 |
| ⟨4, 4, 8⟩ | 98 [95] | 96 |
| ⟨4, 5, 6⟩ | 93 [48] | 90 |
| ⟨5, 5, 5⟩ | 93 [72] | 93 |

表 2|表示 m×n 矩阵与 n×p 矩阵之乘积的张量 ⟨m, n, p⟩ 的秩的上界，即计算该矩阵乘积所需的标量乘法次数。除此处展示的例子外，对所有参数 m, n, p ≤ 5，AlphaEvolve 要么匹配、要么超越了已知最好解，并给出了精确算法（完整结果见附录中的表 3）。对 ⟨3, 4, 7⟩、⟨4, 4, 4⟩ 与 ⟨4, 4, 8⟩，AlphaEvolve 发现的算法使用复值乘法，可用于复或实值矩阵的精确乘法。本表中的分解见配套 Google Colab。

## 3. 结果

### 3.1. 通过发现张量分解的新算法实现更快的矩阵乘法

从加速机器学习计算到实现逼真的计算机图形学，矩阵乘法是支撑计算机科学中众多关键算法与应用的基础运算。自 Strassen [95] 的开创性工作以来，人们已知把两个矩阵相乘的丰富算法空间可以表示为给定 3D 张量到秩一张量的分解。分解的秩（项数）精确给出了计算该矩阵乘积所需的标量乘法次数。因此，要开发更快的矩阵乘法算法，就需要找到特定张量的低秩分解。这一问题已被多种方法攻克，从专门的交替最小二乘求解器 [93] 到深度强化学习 [26] 以及定制搜索算法 [47]；然而，尽管历经数十年的努力，即使是两个 3×3 矩阵相乘这一简单情形，可实现的最小秩仍属未知，足见问题之难。

从问题描述与一个标准的基于梯度的算法（包括初始化器、重构损失函数与 Adam 优化器 [50]）出发，AlphaEvolve 能够开发出超越现有方法的复杂张量分解算法。为评估每个进化出的程序，我们选取一组矩阵乘法目标，并使用第 2.4 节所述的评估级联、以多个随机种子初始化来运行该算法。性能以在每个目标上达到的最好（最低）秩以及达到该秩的种子比例来度量，为 AlphaEvolve 提供爬山（hill-climb）信号。为确保分解的精确性并避免任何潜在数值误差，评估时我们把每个元素舍入到最近的整数或最近的半整数；而为鼓励算法生成接近整数的解，我们把这一要求以自然语言写入 LLM 的提示。

在表 2 中可以看到，AlphaEvolve 开发出的各种算法改进了 14 个不同矩阵乘法目标上的现有技术（SOTA）。值得注意的是，对两个 4×4 矩阵相乘，递归应用 Strassen [95] 的算法得到秩（标量乘法次数）等于 49 的算法，它适用于任意域。对于在 2 元素域中相乘这一非常特定的情形，Fawzi et al. [26] 找到了秩为 47 的算法。56 年来，设计一个在任意特征为 0 的域上秩小于 49 的算法一直是开放问题。³ AlphaEvolve 是首个找到秩 48 算法来乘两个 4×4 复值矩阵的方法。

> ³ 确实存在使用少于 49 次乘法的算法，但它们不对应于矩阵乘法张量的分解，且无法被递归地应用于更大矩阵的乘法。

如图 4 所示，AlphaEvolve 对初始程序做出重大改动，引入若干原创想法来设计越来越好的算法。虽然表 2 中的多数结果（包括 ⟨4, 4, 4⟩）得自一个简单的初始程序，但我们发现，对某些参数，用我们自己的想法播种初始程序（例如为评估函数加入随机性，或使用进化式方法）可进一步提升性能，凸显了研究者与 AlphaEvolve 之间开展科学协作的可能性。

```
1 @@ -45 ,9 +45 ,14 @@
2 # EVOLVE - BLOCK - START
3 def _ g e t _ o p t i m i z e r( self ) -> optax . G r a d i e n t T r a n s f o r m a t i o n:
4 """ Returns o p t i m i z e r."""
5 - return optax . adam ( self . hypers . l e a r n i n g _ r a t e)
6 + return optax . adamw (
7 + self . hypers . learning_rate , w e i g h t _ d e c a y= self . hypers . w e i g h t _ d e c a y
8 + )
9
10 def _ g e t _ i n i t _ f n( self ) -> jax . nn . i n i t i a l i z e r s. I n i t i a l i z e r:
11 """ Returns i n i t i a l i z e rfu nc tio n ."""
12 - return i n i t i a l i z e r s. normal (0.0 , self . hypers . init_scale , jnp . c o m p l e x 6 4)
13 + # I n i t i a l i z ewith a smaller scale to e n c o u r a g efinding low - rank s o l u t i o n s.
14 + # In cr ea se scale sl ig ht ly for better e x p l o r a t i o n.
15 + scale = self . hypers . i n i t _ s c a l e
16 + return i n i t i a l i z e r s. normal (0 + 1 j * 0 , scale * 0.2 , jnp . c o m p l e x 6 4)
17
18 @ @ -80 ,6 +85 ,66 @@
19 # G r a d i e n t u p d a t e s .
20 updates , o p t _ s t a t e = self . opt . update ( grads , opt_state , d e c o m p o s i t i o n )
21 d e c o m p o s i t i o n = optax . a p p l y _ u p d a t e s ( decomposition , updates )
22 + # Add a small amount of gra di en t noise to help with e x p l o r a t i o n
23 + rng , g _ n o i s e _ r n g = jax . random . split ( rng )
24 + d e c o m p o s i t i o n = jax . t r e e _ u t i l . tr ee_ ma p (
25 + lambda x : x
26 + + self . hypers . g r a d _ n o i s e _ s t d * jax . random . normal ( g_noise_rng , x . shape ) ,
27 + decomposition ,
28 + )
29 +
30 + # Add noise to the d e c o m p o s i t i o n p a r a m e t e r s ( e x p l o r a t i o n ) .
31 + _ , n o i s e _ r n g = jax . random . split ( rng )
32 + n o i s e _ s t d = self . _ l i n e a r _ s c h e d u l e (
33 + global_step , start = self . hypers . noise_std , end =0.0
34 + )
35 + d e c o m p o s i t i o n = jax . t r e e _ u t i l . tr ee_ ma p (
36 + lambda x : x + n o i s e _ s t d * jax . random . normal ( noise_rng , x . shape ) ,
37 + decomposition ,
38 + )
39 +
40 + # C yc lic al a n n e a l i n g for c li ppi ng t h r e s h o l d .
41 + c y c l e _ l e n g t h = 2000 # Number of steps per cycle
42 + c y c l e _ p r o g r e s s = (
43 + g l o b a l _ s t e p % c y c l e _ l e n g t h
44 + ) / c y c l e _ l e n g t h # N o r m a l i z e d p rog re ss within the current cycle [0 , 1)
45 +
46 + # Map cycle p rog re ss to a s i n u s o i d a l curve . Ranges from 0 to 1.
47 + c l i p _ t h r e s h o l d _ m u l t i p l i e r = (1 + jnp . cos (2 * jnp . pi * c y c l e _ p r o g r e s s ) ) / 2
48 +
49 + c l i p _ t h r e s h o l d = self . hypers . cli p_ min + c l i p _ t h r e s h o l d _ m u l t i p l i e r * (
50 + self . hypers . c li p_m ax - self . hypers . cl ip _mi n
51 + )
52 +
53 + def s o f t _ c l i p (x , t h r e s h o l d ) :
54 + # C li ppi ng the real and i m a g i n a r y parts s e p a r a t e l y .
55 + x_re = jnp . real ( x )
56 + x_im = jnp . imag ( x )
57 +
58 + x _ r e _ c l i p p e d = jnp . where (
59 + x_re > threshold , t h r e s h o l d + ( x_re - t h r e s h o l d ) * 0.1 , x_re
60 + )
61 + x _ r e _ c l i p p e d = jnp . where (
62 + x _ r e _ c l i p p e d < - threshold ,
63 + - t h r e s h o l d + ( x _ r e _ c l i p p e d + t h r e s h o l d ) * 0.1 ,
64 + x_re_clipped ,
65 + )
66 +
67 + x _ i m _ c l i p p e d = jnp . where (
68 + x_im > threshold , t h r e s h o l d + ( x_im - t h r e s h o l d ) * 0.1 , x_im
69 + )
70 + x _ i m _ c l i p p e d = jnp . where (
71 + x _ r e _ c l i p p e d < - threshold ,
72 + - t h r e s h o l d + ( x _ r e _ c l i p p e d + t h r e s h o l d ) * 0.1 ,
73 + x_im_clipped ,
74 + )
75 +
76 + return x _ r e _ c l i p p e d + 1 j * x _ i m _ c l i p p e d
77 +
78 + d e c o m p o s i t i o n = jax . t r e e _ u t i l . tr ee_ ma p (
79 + lambda x : s o f t _ c l i p (x , c l i p _ t h r e s h o l d ) , d e c o m p o s i t i o n
80 + )
81 +
82 return decomposition , opt_state , loss
83
84 def _l os s_f n (
85 @@ -91 ,13 +156 ,86 @@
86 """ Co mp ut es ( batched ) loss on learned d e c o m p o s i t i o n."""
87 # Compute r e c o n s t r u c t i o nloss .
88 r e c _ t e n s o r= self . _ d e c o m p o s i t i o n _ t o _ t e n s o r( d e c o m p o s i t i o n) # (B , N , M , P )
89 +
90 + # Add noise to the target tensor ( r o b u s t n e s s) .
91 + rng , n o i s e _ r n g= jax . random . split ( rng )
92 + t a r g e t _ n o i s e= self . hypers . t a r g e t _ n o i s e _ s t d* jax . random . normal (
93 + noise_rng , self . t a r g e t _ t e n s o r. shape
94 + )
95 + n o i s y _ t a r g e t _ t e n s o r= self . t a r g e t _ t e n s o r+ t a r g e t _ n o i s e
96 +
97 + # H a l l u c i n a t i o nloss ( e n c o u r a g e se x p l o r a t i o nby ra nd oml y r e p l a c i n gvalues )
98 + h a l l u c i n a t i o n _ p r o b= self . hypers . h a l l u c i n a t i o n _ p r o b
99 + h a l l u c i n a t i o n _ s c a l e= self . hypers . h a l l u c i n a t i o n _ s c a l e
100 +
101 + def h a l l u c i n a t e(x , h a l l u c i n a t i o n _ r n g) :
102 + mask = jax . random . b e r n o u l l i( h a l l u c i n a t i o n _ r n g, p = h a l l u c i n a t i o n _ p r o b)
103 + noise = h a l l u c i n a t i o n _ s c a l e* jax . random . normal (
104 + h a l l u c i n a t i o n _ r n g, x . shape
105 + )
106 + return jnp . where ( mask , noise , x )
107 +
108 + _ , f a c t o r _ r n g= jax . random . split ( rng )
109 + d e c o m p o s i t i o n= jax . t r e e _ u t i l. tr ee _m ap (
110 + lambda x : h a l l u c i n a t e(x , jax . random . split ( f a c t o r _ r n g) [0]) ,
111 + decomposition ,
112 + )
113 +
114 # Add a batch d i m e n s i o nto ` target_tensor ` to ensure correct b r o a d c a s t i n g.
115 # Define the loss as the L2 r e c o n s t r u c t i o nerror .
116 - re c_ los s = l 2 _ l o s s _ c o m p l e x( self . t a r g e t _ t e n s o r[ None , ...] , r e c _ t e n s o r)
117 + re c_ los s = l 2 _ l o s s _ c o m p l e x( n o i s y _ t a r g e t _ t e n s o r[ None , ...] , r e c _ t e n s o r)
118
119 # We must return a real - valued loss .
120 - return jnp . real ( re c_ lo ss )
121
122 + # D i s c r e t i z a t i o nloss ( e n c o u r a g eentries to be m u l t i p l e sof 1/2 or integer ) .
123 + def d i s t _ t o _ h a l f _ i n t s( x ) :
124 + x_re = jnp . real ( x )
125 + x_im = jnp . imag ( x )
126 + return jnp . minimum (
127 + jnp . abs ( x_re - jnp . round ( x_re * 2) / 2) ,
128 + jnp . abs ( x_im - jnp . round ( x_im * 2) / 2) ,
129 + )
130 +
131 + def d i s t _ t o _ i n t s( x ) :
132 + return jnp . abs ( x - jnp . round ( x ) )
133 +
134 + d i s c r e t i z a t i o n _ l o s s= 0.0
135 + for factor in d e c o m p o s i t i o n:
136 + d i s c r e t i z a t i o n _ l o s s+= jnp . mean ( d i s t _ t o _ h a l f _ i n t s( factor ) )
137 + d i s c r e t i z a t i o n _ l o s s+= jnp . mean ( d i s t _ t o _ i n t s( factor ) )
138 +
139 + d i s c r e t i z a t i o n _ l o s s/= (
140 + len ( d e c o m p o s i t i o n) * 2
141 + ) # average across all factors and loss c o m p o n e n t s
142 +
143 + d i s c r e t i z a t i o n _ w e i g h t= self . _ l i n e a r _ s c h e d u l e(
144 + global_step , start =0.0 , end = self . hypers . d i s c r e t i z a t i o n _ w e i g h t
145 + )
146 +
147 + # Cosine a n n e a l i n gfor half - integer loss .
148 + c y c l e _ l e n g t h= self . config . t r a i n i n g _ s t e p s// 4 # Number of steps per cycle
149 + c y c l e _ p r o g r e s s= (
150 + g l o b a l _ s t e p% c y c l e _ l e n g t h
151 + ) / c y c l e _ l e n g t h # N o r m a l i z e dpr og re ss within the current cycle [0 , 1)
152 + h a l f _ i n t _ m u l t i p l i e r= (1 + jnp . cos ( jnp . pi * c y c l e _ p r o g r e s s) ) / 2
153 + h a l f _ i n t _ m u l t i p l i e r= (
154 + 1 - self . hypers . h a l f _ i n t _ s t a r t
155 + ) * h a l f _ i n t _ m u l t i p l i e r+ self . hypers . h a l f _ i n t _ s t a r t
156 +
157 + t o t a l _ l o s s= (
158 + re c_ lo ss
159 + + d i s c r e t i z a t i o n _ w e i g h t* d i s c r e t i z a t i o n _ l o s s* h a l f _ i n t _ m u l t i p l i e r
160 + )
161 +
162 + # Add penalty for large values ( s t a b i l i t y ) .
163 + l a r g e _ v a l u e _ p e n a l t y = 0.0
164 + for factor in d e c o m p o s i t i o n :
165 + l a r g e _ v a l u e _ p e n a l t y += jnp . mean ( jnp . abs ( factor ) ** 2)
166 + l a r g e _ v a l u e _ p e n a l t y /= len ( d e c o m p o s i t i o n )
167 + t o t a l _ l o s s += self . hypers . l a r g e _ v a l u e _ p e n a l t y _ w e i g h t * l a r g e _ v a l u e _ p e n a l t y
168 +
169 + return jnp . real ( t o t a l _ l o s s )
170 +
171
172 def l 2 _ l o s s _ c o m p l e x ( x : jnp . ndarray , y : jnp . ndarray ) -> jnp . ndarray :
173 """ E l e m e n t w i s e L2 loss for c o m p l e x n u m b e r s . """
174 @@ -117 ,6 +255 ,18 @@
175 return hyper . zipit ([
176 - hyper . uniform ( ' i n i t _ s c a l e', hyper . in te rva l (0.2 , 1.5) ) ,
177 - hyper . uniform ( ' l e a r n i n g _ r a t e', hyper . in te rva l (0.05 , 0.3) ) ,
178 + hyper . uniform ( ' i n i t _ s c a l e', hyper . in te rva l (0.1 , 1.0) ) ,
179 + hyper . uniform ( ' l e a r n i n g _ r a t e', hyper . in te rva l (0.01 , 0.2) ) ,
180 + hyper . uniform ( ' d i s c r e t i z a t i o n _ w e i g h t', hyper . in te rv al (0.0 , 0.1) ) ,
181 + hyper . uniform ( ' h a l l u c i n a t i o n _ p r o b', hyper . in te rv al (0.0 , 0.2) ) ,
182 + hyper . uniform ( ' h a l l u c i n a t i o n _ s c a l e', hyper . in te rv al (0.0 , 0.2) ) ,
183 + hyper . uniform ( ' n o i s e _ s t d', hyper . in te rv al (0.0 , 0.01) ) ,
184 + hyper . uniform ( ' t a r g e t _ n o i s e _ s t d', hyper . in te rv al (0.0 , 0.01) ) ,
185 + hyper . uniform ( ' w e i g h t _ d e c a y', hyper . in te rv al (0.00001 , 0.001) ) ,
186 + hyper . uniform ( ' cl ip _m in ', hyper . in te rva l (0.0 , 0.5) ) ,
187 + hyper . uniform ( ' cl ip _m ax ', hyper . in te rva l (1.0 , 3.0) ) ,
188 + hyper . uniform ( ' l a r g e _ v a l u e _ p e n a l t y _ w e i g h t', hyper . in te rv al (0.0 , 0.01) ) ,
189 + # Add noise to the gr ad ien t to aid in e x p l o r a t i o n.
190 + hyper . uniform ( ' g r a d _ n o i s e _ s t d', hyper . in te rv a l (0.0 , 0.001) ) ,
191 + hyper . uniform ( ' h a l f _ i n t _ s t a r t', hyper . in te rva l (0.0 , 1.0) ) ,
192 ])
193 # EVOLVE - BLOCK - END
1 @ @ -45 ,9 +45 ,14 @@
2 # EVOLVE - BLOCK - START
3 def _ g e t _ o p t i m i z e r ( self ) -> optax . G r a d i e n t T r a n s f o r m a t i o n :
4 """ R e t u r n s o p t i m i z e r . """
5 - return optax . adam ( self . hypers . l e a r n i n g _ r a t e )
6 + return optax . adamw (
7 + self . hypers . learning_rate , w e i g h t _ d e c a y = self . hypers .
w e i g h t _ d e c a y
8 + )
9
10 def _ g e t _ i n i t _ f n ( self ) -> jax . nn . i n i t i a l i z e r s . I n i t i a l i z e r :
11 """ R e t u r n s i n i t i a l i z e r f u n c t i o n . """
12 - return i n i t i a l i z e r s . normal (0.0 , self . hypers . init_scale , jnp .
c o m p l e x 6 4 )
13 + # I n i t i a l i z e with a smaller scale to e n c o u r a g e finding low - rank
s o l u t i o n s .
14 + # I nc re as e scale s li gh tl y for better e x p l o r a t i o n .
15 + scale = self . hypers . i n i t _ s c a l e
16 + return i n i t i a l i z e r s . normal (0 + 1 j * 0 , scale * 0.2 , jnp . c o m p l e x 6 4 )
1 @ @ -91 ,13 +156 ,86 @@
2 """ C o m p u t e s ( b a t c h e d ) loss on l e a r n e d d e c o m p o s i t i o n . """
3 # C o m p u t e r e c o n s t r u c t i o n loss .
4 r e c _ t e n s o r = self . _ d e c o m p o s i t i o n _ t o _ t e n s o r ( d e c o m p o s i t i o n )# (B , N
, M , P )
5 ...
6 + # D i s c r e t i z a t i o n loss ( e n c o u r a g e entries to be m u l t i p l e s of 1/2 or
integer ) .
7 + def d i s t _ t o _ h a l f _ i n t s ( x ) :
8 ...
9 +
10 + def d i s t _ t o _ i n t s ( x ) :
11 ...
12 + d i s c r e t i z a t i o n _ l o s s = 0.0
13 + for factor in d e c o m p o s i t i o n :
14 + d i s c r e t i z a t i o n _ l o s s += jnp . mean ( d i s t _ t o _ h a l f _ i n t s ( factor ) )
15 + d i s c r e t i z a t i o n _ l o s s += jnp . mean ( d i s t _ t o _ i n t s ( factor ) )
16 +
17 + d i s c r e t i z a t i o n _ l o s s /= (
18 + len ( d e c o m p o s i t i o n ) * 2
19 + ) # average across all factors and loss c o m p o n e n t s
20 +
21 + d i s c r e t i z a t i o n _ w e i g h t = self . _ l i n e a r _ s c h e d u l e (
22 + global_step , start =0.0 , end = self . hypers . d i s c r e t i z a t i o n _ w e i g h t
23 + )
24 +
25 + # Cosine a n n e a l i n g for half - integer loss .
26 + c y c l e _ l e n g t h = self . config . t r a i n i n g _ s t e p s // 4 # Number of steps
per cycle
27 + c y c l e _ p r o g r e s s = (
28 + g l o b a l _ s t e p % c y c l e _ l e n g t h
29 + ) / c y c l e _ l e n g t h # N o r m a l i z e d p rog re ss within the current cycle
[0 , 1)
30 + h a l f _ i n t _ m u l t i p l i e r = (1 + jnp . cos ( jnp . pi * c y c l e _ p r o g r e s s ) ) / 2
31 + h a l f _ i n t _ m u l t i p l i e r = (
32 + 1 - self . hypers . h a l f _ i n t _ s t a r t
33 + ) * h a l f _ i n t _ m u l t i p l i e r + self . hypers . h a l f _ i n t _ s t a r t
34 +
35 + t o t a l _ l o s s = (
36 + re c_ lo ss
37 + + d i s c r e t i z a t i o n _ w e i g h t * d i s c r e t i z a t i o n _ l o s s *
h a l f _ i n t _ m u l t i p l i e r
38 + )
39 ...
1 @ @ -117 ,6 +255 ,18 @@
2 r e t u r n hyper . zipit ([
3 - hyper . uniform ( ' i n i t _ s c a l e', hyper . i nt er va l (0.2 , 1.5) ) ,
4 - hyper . uniform ( ' l e a r n i n g _ r a t e', hyper . i nt er va l (0.05 , 0.3) ) ,
5 + hyper . uniform ( ' i n i t _ s c a l e', hyper . i nt er va l (0.1 , 1.0) ) ,
6 + hyper . uniform ( ' l e a r n i n g _ r a t e', hyper . i nt er va l (0.01 , 0.2) ) ,
7 + hyper . uniform ( ' d i s c r e t i z a t i o n _ w e i g h t', hyper . i nt er va l (0.0 , 0.1) )
,
8 + hyper . uniform ( ' h a l l u c i n a t i o n _ p r o b', hyper . i nt er va l (0.0 , 0.2) ) ,
9 + hyper . uniform ( ' h a l l u c i n a t i o n _ s c a l e', hyper . i nt er va l (0.0 , 0.2) ) ,
10 + hyper . uniform ( ' n o i s e _ s t d', hyper . i nt er va l (0.0 , 0.01) ) ,
11 + hyper . uniform ( ' t a r g e t _ n o i s e _ s t d', hyper . i nt er va l (0.0 , 0.01) ) ,
12 + hyper . uniform ( ' w e i g h t _ d e c a y', hyper . i nt er va l (0.00001 , 0.001) ) ,
13 + hyper . uniform ( ' cl ip _m in ', hyper . i nt er va l (0.0 , 0.5) ) ,
14 + hyper . uniform ( ' cl ip _m ax ', hyper . i nt er va l (1.0 , 3.0) ) ,
15 + hyper . uniform ( ' l a r g e _ v a l u e _ p e n a l t y _ w e i g h t', hyper . i nt er va l (0.0 ,
0.01) ) ,
16 + # Add noise to the g ra di en t to aid in e x p l o r a t i o n .
17 + hyper . uniform ( ' g r a d _ n o i s e _ s t d', hyper . i nt er va l (0.0 , 0.001) ) ,
18 + hyper . uniform ( ' h a l f _ i n t _ s t a r t', hyper . i nt er va l (0.0 , 1.0) ) ,
19 ])
20 # EVOLVE - BLOCK - END
```

图 4|AlphaEvolve 为发现更快的矩阵乘法算法而提出的变更。完整 diff 展示于左（放大版见图 9a 至 9c），右侧高亮了部分摘录。在本例中，AlphaEvolve 在多个组件上提出广泛变更，包括优化器与权重初始化（右上）、损失函数（右中）以及超参数扫描（右下）。这些变更绝非平凡，进化过程经历了 15 次变异。

### 3.2. 为广泛的开放数学问题寻找量身定制的搜索算法

数学研究的一个重要前沿，是发现按某种度量具有最优或近优性质的对象或构造。例子从寻找几何形状的稠密堆积 [29] 到识别满足特定组合或解析约束的函数或集合（例如 [39, 40, 70, 104]）。进展往往依赖于找到一个超越所有已知例子的单一构造，从而为最优值确立新的下界或上界。我们证明，AlphaEvolve 是探索这些问题固有庞大搜索空间的强大工具，成功应对了多种多样的开放数学挑战。

为评估其能力，我们将 AlphaEvolve 应用于精选的 50 余个数学问题，横跨数学的五个以上分支，包括分析、组合、数论与几何，并在众多具体参数设定（如不同维度或规模）下评估。在 75% 的情形中，AlphaEvolve 重新发现了已知最好的构造；在 20% 的情形中，它发现了优于此前已知最佳构造的新对象，从而改进了 SOTA。在所有这些情形中，初始出发点都是一个简单或随机的构造。这些结果凸显了 AlphaEvolve 作为数学研究多面手工具的广泛潜力。

Analysis
1.5098 → 1.5053
Geometry
Analysis
Problem 3
Problem 2
Problem 1
0.8892 → 0.8962
Combinatorics
1.4581 → 1.4557
0.3523 → 0.3521
+ + +
0.380926 → 0.380924
1.1446 → 1.1584
4.000 → 3.942
12.890 → 12.889
2.6340 → 2.6358
Hexagon outer edge
Max distance/min distance
Sum of radii

图 5|用 AlphaEvolve 发现的打破 SOTA 的数学构造示例。AlphaEvolve 的通用性使我们能够处理分析（自相关与不确定性不等式）、几何（堆积与最小/最大距离问题）以及组合（Erdős 最小重叠问题与有限集的和差）中的问题。

此处所用 AlphaEvolve 配置的一个显著优势在于其通用性与应用速度。以进化启发式搜索程序为核心的方法论（详见下文），可以快速部署到多种多样的数学构造问题与猜想上；相比传统定制方法，通常所需的初始针对问题的专家定制更少。虽然深刻的数学洞察自然有助于问题形式化与搜索空间定义，但 AlphaEvolve 往往展现出自主发现有效搜索模式与攻击策略的能力——通过识别问题景观中的微妙结构。这使我们能够跨许多不同问题进行高效的大规模探索。

促成这些发现的关键方法论创新，在于 AlphaEvolve 进化启发式搜索算法、而非直接进化构造本身的能力。对许多问题——特别是目标函数评估快速的问题（这在数学中很常见）——我们采用迭代精化策略。每一代 AlphaEvolve 的任务，是进化一个表示搜索启发式的程序。该程序被给定固定的时间预算（例如 1000 秒），并被展示此前最佳启发式找到的最佳构造。它的目标是利用这一起点与所分配的时间，找到一个更好的构造。进化过程因此筛选出擅长改进已经高质量之解的启发式。最终的构造往往是 AlphaEvolve 发现的一系列不同专门启发式接力而成——早期启发式擅长从随机或简单的初始状态获得大幅提升，后期启发式则精于在近优配置附近微调。这种多阶段、自适应搜索策略的自动发现很难人工复制，并被证明对超越 SOTA 至关重要。

以下是 AlphaEvolve 取得新结果的其中一些问题的高层描述。完整的问题列表与细节见附录 B。

- **分析**
  - **自相关不等式。** AlphaEvolve 改进了若干自相关不等式的已知最好界。
  - **不确定性原理。** AlphaEvolve 为傅里叶分析中的一个涌现问题产生了更精化的配置，通过打磨一个不确定性原理构造 [33]，得到略好的上界。
- **组合与数论**
  - **Erdős 最小重叠问题。** AlphaEvolve 为最小重叠问题 [25] 确立了新的上界，较此前纪录 [40] 略有改进。
- **几何与堆积**
  - **Kissing number 问题。** 在 11 维中，AlphaEvolve 改进了 kissing number 的下界，找到 593 个互不重叠的单位球可同时触碰一个中心单位球的构型，超越了此前 592 的纪录 [31]。
  - **堆积问题。** AlphaEvolve 在堆积问题上取得若干新结果，例如：把 N 个点装入某个形状以最小化最大与最小距离之比；以最有效的方式把多个多边形堆积进其他多边形；以及关于避免小面积三角形的点集的 Heilbronn 问题变体 [29]。

完整的问题列表见附录 B，AlphaEvolve 找到的新构造可在配套 Google Colab 中查看。这些问题与所用方法的更多示例与细节将在后续论文中给出。这些发现多数针对外部数学家 Javier Gomez Serrano 与 Terence Tao 向我们建议的开放问题，他们还就如何最好地把这些问题形式化为 AlphaEvolve 的输入提供了咨询。这凸显了 AlphaEvolve 这类 AI 驱动的发现引擎与人类数学专长之间建立协同伙伴关系的潜力。

### 3.3. 优化 Google 的计算生态

除前述各节的科学应用外，这里我们展示 AlphaEvolve 如何被用于改进关键任务基础设施的性能并交付真实世界的影响。

#### 3.3.1. 改进数据中心调度

把计算作业高效地调度到机器集群上是一个关键的优化问题，在由 Borg [102] 编排的 Google 数据中心的规模上尤其如此。该任务涉及根据作业的资源需求与机器容量，把作业分配到可用机器。低效的分配可能导致资源搁浅（stranded resources）：当一台机器因为耗尽某一种资源（例如内存）而无法再接受作业、但其他资源仍然空闲（例如 CPU）时。调度效率的改进可以回收这些被搁浅的资源，使同样大小的计算足迹上能完成更多作业。这种回收对于在不按比例增加资源消耗的情况下满足不断增长的计算需求至关重要。此外，这个问题极具挑战性，因为它在经典意义上困难的装箱（bin-packing）问题之上，还叠加了可调试性与规模化等典型的工程困难。

我们通过把在线作业调度问题表述为带两个变量的向量装箱问题来应对这一挑战。在此语境下，机器代表具有确定 CPU 与内存容量的箱子，到来的作业是具有特定资源需求的物品。一个启发式函数以待处理作业的 CPU 与内存需求、以及一台候选机器的 CPU 与内存可用量为输入，输出该机器的优先级分数。Borg 调度器随后（在其他目标之中）把待处理作业分配给由该启发式函数确定的优先级分数最高的机器。由于该启发式只影响对那些已被 Borg 判定为可运行每个待处理作业的机器的排序，所得的调度决策在构造上即是正确的。

AlphaEvolve 的一个早期版本被用来发现一个极为简单而有效的启发式函数（见图 6），它从生产中的既有启发式进化而来。我们使用数据中心的模拟器，基于 Google 整个机群的工作负载与容量历史快照，向 AlphaEvolve 提供反馈。我们在近期工作负载与容量的未见测试数据集上度量 AlphaEvolve 启发式函数的性能，以确保泛化能力。在观察到 AlphaEvolve 的启发式函数优于生产中的那一个之后，我们把 AlphaEvolve 的启发式函数推广到整个机群。Google 机群范围的部署后测量证实了模拟器结果，表明该启发式函数持续回收平均 0.7% 的 Google 全机群计算资源——否则这些资源将被搁浅。我们之所以选择 AlphaEvolve 而非深度强化学习方法，是因为它的代码解不仅带来更好的性能，还在可解释性、可调试性、可预测性与易于部署方面具有明显优势——这些是关键任务系统的必备品质。

1 def alpha_evolve_score(required, free):
2 cpu_residual = required.cpu / free.cpu
3 mem_residual = required.mem / free.mem
4
5 return -1.0 * (cpu_residual + mem_residual +
6 mem_residual / cpu_residual +
7 cpu_residual / mem_residual)
0% 25% 50% 75% 100%
CPU residual
0%
25%
50%
75%
100%Memory residual

图 6|左：AlphaEvolve 发现的、针对 Google 的工作负载与容量量身打造的启发式函数。右：该启发式评分函数的可视化。黄色区域代表高分，紫色区域代表低分。

#### 3.3.2. 增强 Gemini 内核工程

训练 Gemini 这样的大模型需要大量计算资源。Gemini 构建于 JAX [9] 之上，而 Pallas 是 JAX 的一个扩展，用于编写定制、高度专门化的程序（内核），并为在硬件加速器上最优执行而量身打造。因此，高效的 Pallas 内核对优化 Gemini 的训练性能至关重要。

内核优化的一个关键方面，是为矩阵乘法运算调整分块（tiling）策略（见图 7）。该技术把一个大的矩阵乘法计算划分为更小的子问题，以更好地平衡计算与数据搬运，这是加速整体计算的关键。传统上，内核工程师依靠基于搜索的自动调优或手工打造的启发式，来确定各种输入形状的近优分块配置。基于搜索的调优会打断研究工作流，每次输入形状变化都需要重新调优。反过来，手工打造有效的分块启发式因其复杂性而成为重大工程瓶颈——它要求对内核功能与硬件细节都有深刻理解。高性能启发式的关键优势，在于能够在任意输入形状上交付高性能。因此，为加快为新兴硬件设计高性能内核、并简化模型开发者对它们的使用，我们希望让启发式生成过程变得更加便利。

我们通过使用 AlphaEvolve 来优化一个用于训练 Gemini 的重要矩阵乘法内核的分块启发式，以应对这一挑战。目标是最小化该内核的实际运行时间。AlphaEvolve 通过提出候选代码、力图在真实 TPU 加速器上的各种输入形状上最小化该运行时间，来迭代地探索并精化该内核的分块启发式。内核的正确性在构造上得以保持，因为 AlphaEvolve 优化的是该内核的分块策略，而非改变其底层数学运算。为构建 AlphaEvolve 的训练与评估数据集，我们从内核用户处自动收集真实的内核输入形状。其中一半输入形状构成训练集，在进化过程中提供优化目标；其余输入形状构成评估集，用于检验所得启发式的普适性。

这一自动化方法使 AlphaEvolve 发现了一个相对现有专家设计启发式在所有内核上平均提速 23% 的启发式，并相应使 Gemini 的整体训练时间减少 1%。此外，AlphaEvolve 的使用显著缩短了内核优化时间——从数月的专职工程投入缩短到仅数天的自动化实验。这一加速加快了优化内核的部署，让内核工程师得以把专长投入到更具战略性、更高层的优化问题。此外，AlphaEvolve 为自动化手工调优过程、改善 Gemini 内核的使用体验提供了路径。AlphaEvolve 发现的分块启发式已被部署到生产环境，直接提升了 Gemini 的训练效率以及 Gemini 团队的研究与工程速度。这次部署也标志着一个新颖的实例：Gemini 通过 AlphaEvolve 的能力优化其自身的训练过程。

A C
B
M
N
N
P
M
P

图 7|矩阵乘积 AB = C 的分块启发式问题的可视化。创建一个能为所有输入形状自动选择正确 tile 尺寸 (M, N, P) 的启发式很困难，因为必须了解矩阵乘法单元的最优形状与内存容量、周围运算的内存需求、融合进内核的额外运算，以及底层编译器的种种细节等。

#### 3.3.3. 辅助硬件电路设计

专用硬件，如 Google 的张量处理单元（TPU），对于实现规模化运行现代 AI 系统所需的资源效率至关重要。然而，设计新的计算机芯片是一个复杂且耗时的过程，往往历时数年。寄存器传输级（RTL）优化是该过程中关键的一步，涉及手工重写硬件描述以改进功耗、性能与面积等指标，需要高技能工程师数月的迭代。

在这项工作中，AlphaEvolve 被挑战去优化矩阵乘法单元内一个关键 TPU 算术电路的、已经高度优化的 Verilog 实现。优化目标是在保持该组件核心功能的同时，降低面积与功耗。至关重要的是，最终提案必须通过严格的验证方法，确认修改后的电路保持功能正确。AlphaEvolve 找到了一个移除不必要比特的简单代码重写，这一变更已由 TPU 设计者验证正确。虽然这一特定改进也被下游综合工具独立发现，但 AlphaEvolve 在 RTL 阶段的贡献展示了其精化源 RTL、在设计流程早期提供优化的能力。

集成到即将推出的 TPU 中之后，这一改进代表了 Gemini 借由 AlphaEvolve 对 TPU 算术电路的首次直接贡献，为未来的贡献铺平了道路。AlphaEvolve 的一个关键优势是，它直接用硬件工程师的标准语言 Verilog 来传达所建议的变更，培养信任并简化采纳。这一早期探索展示了一条新颖的路径：由 LLM 驱动的代码进化辅助硬件设计，有望缩短上市时间。

#### 3.3.4. 直接优化编译器生成的代码

Transformer 架构 [100] 被用于大多数现代神经网络，从 LLM 到 AlphaFold [1]。Transformer 的核心计算是注意力机制 [4]，最常用 FlashAttention [22] 实现。在我们的技术栈中，FlashAttention 实现为 Pallas 中的一个加速器内核，由处理输入准备与输出后处理的 JAX 高层代码包裹。机器学习编译器（XLA [77]）随后把这一实现翻译为一系列中间表示（IR），每个中间表示都为在特定硬件上执行添加更多细节。在这些阶段，内存访问编排或计算调度上的更优决策，可以显著减少特定硬件上的运行时间。

我们挑战 AlphaEvolve 直接优化封装 FlashAttention 内核及前后处理代码的 XLA 生成的 IR。我们优化的配置对应一个用于 GPU 上大规模推理的高影响力 transformer 模型，目标是最小化该模块的总体执行时间。这是一个格外困难的任务，因为 (1) IR 是为调试目的而非供开发者直接编辑而设计的；(2) 它由编译器生成，且已被高度优化。AlphaEvolve 提出的每处修改，都在随机输入上与参考（未修改）代码进行核对，以确保优化全过程的数值正确性。代码的最终版本经人类专家严格确认，对所有可能输入均正确。

AlphaEvolve 能够为 IR 所暴露的两个抽象层次都提供有意义的优化。首先，感兴趣配置的 FlashAttention 内核提速了 32%。其次，AlphaEvolve 在内核输入与输出的前后处理中找到了改进，使这部分提速 15%。这些结果展示了 AlphaEvolve 优化编译器生成代码的能力，为将发现的优化整合进现有编译器以服务特定用例、或在更长远的未来把 AlphaEvolve 整合进编译器工作流本身，提供了可能。

## 4. 消融实验

我们在两个任务上进行了消融：为更快矩阵乘法寻找张量分解（3.1 节）与计算 kissing number 的下界（3.2 节），旨在理解 AlphaEvolve 以下组件的有效性。

- **进化方法。** AlphaEvolve 采用进化方法，先前生成的程序存入数据库，并用于在后续迭代中获得更好的程序。为分析进化的重要性，我们考虑一种替代方法：反复向语言模型输入同一初始程序。我们称该方法为「No evolution」（无进化）。
- **提示中的上下文。** AlphaEvolve 使用具有大上下文窗口的强大语言模型，在提示中提供问题特定上下文可显著改善其输出。为检验上下文的重要性，我们考虑一种替代方法：不向提示添加任何显式上下文。我们称该方法为「No context in the prompt」（提示中无上下文）。
- **元提示。** AlphaEvolve 还使用元提示来改进提供给语言模型的提示。这使它有可能超越人类提示者所能获得的性能。为检验元提示的有效性，我们在张量分解任务上将其禁用。我们称该方法为「No meta prompt evolution」（无元提示进化）。
- **全文件进化。** 与 FunSearch 等先前方法不同，AlphaEvolve 可以进化整个代码库，而非只聚焦于单个函数。为检验全文件进化的重要性，我们在张量分解的语境下考虑一种替代方案：只进化损失函数。我们称该方法为「No full-file evolution」（无全文件进化）。
- **强大的语言模型。** AlphaEvolve 依靠小与大语言模型的混合来获得高度多样的样本。为理解这一组件的重要性，我们考虑只使用单个小基础模型的替代方案。我们称该方法为「Small base LLM only」（仅小基础 LLM）。

图 8 展示了包含全部组件的 AlphaEvolve 方法以及上述各种替代方案的结果。可以看到，每个组件都为结果带来了显著改进。

0% 25% 50% 75% 100%
Fraction of compute budget
10
9
8
7
6
5
4
3
2
1
Target metric (aggregated)
Matrix multiplication tensor decomposition
Full method
No meta prompt evolution
Small base LLM only
No context in the prompt
No full-file evolution
No evolution
0% 25% 50% 75% 100%
Fraction of compute budget
50
40
30
20
10
0
Target metric (aggregated)
Kissing number problem
Full method
No context in the prompt
No evolution

图 8|左：AlphaEvolve 在寻找更快矩阵乘法的低秩张量分解问题上的消融。右：AlphaEvolve 在为改进 kissing number 而寻找球堆积问题上的消融。每条曲线展示单个设定随计算预算增加的性能，在所有考虑的目标上取平均（目标指标值越高越好）。阴影表示目标内标准差，在以不同随机种子初始化的三次独立 AlphaEvolve 运行上取平均。

## 5. 相关工作

**进化方法。** AlphaEvolve 延续了进化或遗传编程 [54] 的悠久研究传统——反复使用一组变异与交叉算子来进化一个程序池 [5, 51]。特别地，经典进化技术在符号回归应用 [66, 87]、自动化科学 [21] 或算法 [16] 发现以及调度 [118] 问题中取得过成功。然而，这些方法的一个挑战在于使用手写的进化算子，它们难以设计，且可能无法刻画领域的重要性质。相比之下，AlphaEvolve 用 LLM 自动构造这些算子——它利用 LLM 的世界知识来变异程序，无需预先定义一组允许的变异操作。

在 AlphaEvolve 之前，已有一批将 LLM 与进化结合起来的近期努力；具体而言，它扩展了由 Romera-Paredes et al. [83] 作为数学发现方法引入的 FunSearch 系统。FunSearch 随后被用于下游任务，例如为贝叶斯优化学习采集函数 [2]、发现认知模型 [13]、计算图之间的距离 [103]，或组合竞赛编程 [101]。AlphaEvolve 以三个关键方式超越了 FunSearch 及其近期的重新实现 [24]。第一，FunSearch 只允许进化单个 Python 函数，而 AlphaEvolve 允许对以广泛编程语言编写的整个代码库进行进化。第二，FunSearch 优化单一目标函数，而 AlphaEvolve 提供执行多目标优化的能力。第三，FunSearch 中的 LLM 相对较小且仅在代码上训练；相比之下，AlphaEvolve 使用前沿 LLM 以及丰富的自然语言上下文与反馈形式。正如本文所展示的，这些扩展使 AlphaEvolve 能够处理 FunSearch 所无法胜任的重要难题。

这一门类中的其他努力包括 Lehman et al. [57] 的方法——用 LLM 引导的进化过程为一组仿真机器人发现程序化策略；以及 Hemberg et al. [41] 的代码合成方法。类似方法已在多个科学与数学任务中找到用途，包括符号回归 [35, 89]、为组合优化发现启发式 [63, 115, 117]，以及合成分子结构 [105]。LLM 引导的进化还被用于改进 AI 系统，例如增强 LLM 提示 [27] 与搜索神经架构 [14, 73]。AlphaEvolve 与这些方法的差异在于其规模、灵活性以及对广泛领域的普适性。

一些近期工作为 LLM 引导进化的基本范式补充了相辅相成的想法。例如，Surina et al. [96] 通过强化学习持续微调 LLM 来补充进化过程；Grayeli et al. [35] 用一个 LLM 主导的概念学习步骤来增强进化过程，把程序池中的高性能程序总结为自然语言。要在 AlphaEvolve 运行的规模上理解这些想法的益处，还需要更多研究。

进化方法也出现在近期的 AI Co-Scientist 工作 [34] 中，该工作寻求使用分别负责任假设发现、假设排序与文献综述等任务的不同智能体来自动化科学发现。AI Co-Scientist 用自然语言表示科学假设及其评估准则，而 AlphaEvolve 聚焦于进化代码，并用程序化的评估函数来引导进化。这一选择使我们能够大幅规避 LLM 幻觉，从而让 AlphaEvolve 能把进化过程延续大量时间步。尽管如此，原则上可以把两种方法结合起来，得到允许自然语言与程序化表达灵活组合的方法。

**超优化与算法发现。** AlphaEvolve 可以被看作一种代码超优化方法，因为它使用执行反馈来迭代改进一个初始程序。代码超优化的思想可追溯到 20 世纪 80 年代 [69]；LLM 出现之前应对该问题的方法包括系统枚举 [69]、遗传搜索 [20]、蒙特卡洛采样 [86] 与深度强化学习 [68]。此外，在聚焦单个问题（如矩阵乘法）的受限设定中，已有诸如 AlphaTensor 这样同样能发现可证明正确算法的系统 [26]。

近来，涌现出一批基于 LLM 的超优化与算法发现方法。这类文献建立在 LLM 于编码任务上成功的基础之上——最好的例证也许是它们在（模拟）编程竞赛中的成功，如 AlphaCode 的案例 [60]。例如，LLM 智能体已被用于优化 GPU 内核中的某些运算，如注意力运算 [15] 或更一般的用户指定运算 [56]。还有用 LLM 发现新颖进化算法 [55]、训练语言模型 [58] 以及优化仓库级计算机 [61] 的工作。其他近期工作 [108] 还提出使用多个相互对话的 LLM 智能体来完成数学与编码任务。

虽然先前关于用 LLM 做算法发现的工作给出了有希望的结果，但 AlphaEvolve 将其用于进化算法的做法，使我们能够应对显著更具挑战性的问题，如第 3 节所展示。

**面向科学与数学发现的 AI。** 过去十年，AI 系统已被应用于广泛的学科与任务，从蛋白质结构预测 [46] 到量子物理 [6, 84] 再到气候科学 [53]。特别地，近期有大量基于 LLM 的方法针对多个学科的科学问题，如材料科学 [45, 71, 94, 119]、化学 [12, 64]、生物信息学 [67, 85]、地球科学 [79] 与量子物理 [30, 78]（相关主题的综述见 [36, 65, 81]）。

这些方法中有许多使用 LLM 来自动化科学发现过程的若干不同阶段 [37, 59, 106, 109, 112]，例如生成与排序假设和想法 [38, 90]。其中与 AlphaEvolve 尤其相关的，是使用 LLM 引导的基于树搜索的算法 [11] 或 LLM 引导的进化算法 [34, 113, 120] 的方法。其他工作用 LLM 优化实验规划与设计 [7, 10, 43, 75] 或实验执行与工作流 [28, 62, 82, 105, 116]。最后，也有聚焦于数据分析阶段 [80] 的工作。AlphaEvolve 与多数方法的差异在于其使用程序化的假设表示与评估指标。

AI 系统也为纯数学的进展做出过贡献 [23]。在此语境下，FunSearch 方法 [24, 83] 确立了 LLM 引导进化作为一个强大工具，用于发现数学陈述的见证与反例——这一问题与寻找数学陈述的形式化与非形式化证明 [3, 19, 98, 99, 110, 111] 互为补充。

## 6. 讨论

AlphaEvolve 展示了把最先进 LLM 与自动评估指标结合在进化框架之中的惊人力量：它既能在存在数十年之久的数学问题上带来新发现，也能为高度优化的计算栈带来实用改进。

有趣的是，AlphaEvolve 往往允许以不同方式处理同一问题：直接搜索解、找到一个从零开始构造它的函数，或进化一个搜索算法来找到它。以不同方式应用 AlphaEvolve 会带来不同的偏差（例如，寻找构造函数可能偏向于发现高度对称的对象 [83]），因而适合不同的问题。

AlphaEvolve 也可以被看作一种测试时计算智能体，它通过自身的进化过程显著增强基础 LLM 的能力（相比之下，例如重复采样）。一方面，这可被视为一个令人信服的展示：机器反馈能够支撑测试时计算扩展，直至进入产生新科学发现与高价值实用优化的区间。另一方面，自然的下一步将是考虑把基础 LLM 经 AlphaEvolve 增强后的性能蒸馏进下一代基础模型。这可以有内在价值，而且很可能也会提升下一版 AlphaEvolve。

除蒸馏之外，同样引人注意的是，AlphaEvolve 能够做出提升自身基础设施以及（未来版本的）其基础 LLM 效率的实用发现。目前，收益尚属温和，改进下一版 AlphaEvolve 的反馈回路以月计。然而，伴随着这些改进，我们预见，搭建更多带有稳健评估函数的环境（问题）的价值将被更广泛地认可，这反过来又将带来今后更多高价值的实用发现。

AlphaEvolve 的主要局限在于，它处理的是那些可以设计出自动评估器的问题。虽然数学与计算科学中的许多问题满足这一点，但诸如自然科学等领域，只有一部分实验能够被仿真或自动化。尽管 AlphaEvolve 确实允许由 LLM 提供对想法的评估，但这并不是我们针对其优化过的设定。不过，同期工作表明这是可能的 [34]，而自然的一步是把两种设定连接起来：由 LLM 先就高层想法提供反馈，再转入可经代码执行获得机器反馈的实现阶段。

## 致谢

我们感谢 Michael Figurnov 审阅本白皮书；感谢 Alhussein Fawzi、Bernardino Romera-Paredes 与 Ankit Anand 的早期探索与富有洞见的讨论；感谢 Stig Petersen 与 Demis Hassabis 的支持与建议；感谢 JD Velasquez 就管理实际应用提供的有益建议；并感谢 AlphaEvolve 的所有早期用户与合作者，他们的多样用例与深刻反馈把 AlphaEvolve 打磨成一个更稳健、更通用的工具，适用于广泛的应用。我们衷心感谢以下人士对本白皮书所强调应用的宝贵贡献：

Terence Tao、Javier Gomez Serrano 与 Jordan Ellenberg 建议了具体的开放数学问题，并就如何最好地把它们形式化为 AlphaEvolve 的输入提供建议；Bogdan Georgiev、Ray Jiang 与 Johannes Bausch 对把 AlphaEvolve 应用于这些问题做出了贡献。

Mohammadamin Barekatain、Patrick Heisel、Chase Hensel、Robert O'Callahan 与 Pengming Wang 共同领导了数据中心调度应用；Federico Piccinini、Sultan Kenjeyev 与 Andrea Michi 做出了重要贡献；Kieran Milan、Daniel Mankowitz、Cosmin Paduraru、Calin Cascaval、Tammo Spalink 与 Natasha Antropova 提供了有益的建议；Aaron Gentleman、Gaurav Dhiman、Parthasarathy Ranganatha 与 Amin Vahdat 审阅了这项工作。

Yanislav Donchev 领导了 Gemini 内核工程应用；Richard Tanburn 做出了重要贡献；Justin Chiu 与 Julian Walker 提供了有益的建议；Jean-Baptiste Alayrac、Dmitry Lepikhin、Sebastian Borgeaud、Koray Kavukcuoglu 与 Jeff Dean 审阅了这项工作。

Timur Sitdikov 领导了 TPU 电路设计应用；Georges Rotival 提供了电路评估基础设施；Kirk Sanders、Srikanth Dwarakanath、Indranil Chakraborty、Christopher Clark 在 TPU 设计中验证并确认了结果；Vinod Nair、Sergio Guadarrama、Dimitrios Vytiniotis 与 Daniel Belov 提供了有益的建议；Kerry Takenaka、Jeff Dean、Sridhar Lakshmanamurthy、Parthasarathy Ranganathan 与 Amin Vahdat 审阅了这项工作。

Benjamin Chetioui、Sergei Lebedev、Alexander Belyaev、Henning Becker、Oleg Shyshkov 与 Aliia Khasanova 对 XLA 修改提供了帮助与有益的建议；Giorgio Arena、Marco Cornero 与 Sebastian Bodenstein 审阅了这项工作。

## 作者信息

以下作者贡献相同：Alexander Novikov、Ngân Vũ、Marvin Eisenberger、Emilien Dupont、Po-Sen Huang、Adam Zsolt Wagner、Sergey Shirobokov、Borislav Kozlovskii 与 Matej Balog。

**贡献。** A.N. 与 M.B. 设计并实现了 AlphaEvolve 的初始版本。M.B.、A.N.、N.V. 与 P.K. 发展了项目愿景并界定了问题范围。N.V. 与 P.-S.H. 监督了实际应用。E.D. 与 M.E. 在 F.J.R.R. 与 M.B. 的输入下，实现了用于迭代 AlphaEvolve 的第一个基准问题。A.N. 与 M.E. 开发了 AlphaEvolve 的最终版本，S.S. 与 P.-S.H. 有贡献，并得到 M.B.、E.D.、A.Z.W. 与 N.V. 的输入。A.N.、S.S.、P.-S.H. 与 M.E. 维护了 AlphaEvolve 的底层基础设施。M.E. 与 E.D. 在 F.J.R.R. 的输入下，用 AlphaEvolve 发现了矩阵乘法的新算法。A.Z.W. 在 A.M.、M.E. 与 A.N. 的帮助下，研究了开放数学问题上的应用。A.N. 对 Borg 调度应用有贡献。P.-S.H. 与 N.V. 研究了 Gemini 内核工程上的应用。P.-S.H. 与 A.N. 对 TPU 电路设计应用有贡献。B.K. 与 S.S. 研究了用 AlphaEvolve 直接优化编译器生成的代码。M.E. 执行了消融实验。M.B.、A.N.、M.E.、S.S. 与 P.-S.H. 完成了大部分代码评审。M.B.、E.D.、S.C.、N.V.、A.Z.W.、F.J.R.R.、M.E.、A.N.、B.K.、S.S.、A.M. 与 M.P.K. 在 A.S.、P.-S.H 与 P.K. 的输入下撰写了论文。N.V.、E.D.、M.E.、S.C.、A.N. 与 A.Z.W. 制作了插图。F.J.R.R.、A.M. 与 A.Z.W. 整理了配套 Google Colab。S.N.、A.D. 与 P.K. 建议并促成了本工作的多个方向。M.B.、A.N.、N.V. 与 G.H. 协调了团队。P.K. 监督并协调了研究计划。

**通讯作者。** Matej Balog、Alexander Novikov 与 Pushmeet Kohli。

## 参考文献

[1] J. Abramson, J. Adler, J. Dunger, R. Evans, T. Green, A. Pritzel, O. Ronneberger, L. Will-
more, A. J. Ballard, J. Bambrick, et al. Accurate structure prediction of biomolecular
interactions with alphafold 3.Nature, 630(8016):493–500, 2024.
[2] V. Aglietti, I. Ktena, J. Schrouff, E. Sgouritsa, F. J. R. Ruiz, A. Malek, A. Bellot, and
S. Chiappa. FunBO: Discovering acquisition functions for Bayesian optimization with
FunSearch. InInternational Conference on Machine Learning, 2025.
[3] AlphaProof and AlphaGeometry teams. AI achieves silver-medal standard solving
International Mathematical Olympiad problems, 2024. URLhttps://deepmind.g
oogle/discover/blog/ai-solves-imo-problems-at-silver-medal-lev
el.
[4] D. Bahdanau, K. Cho, and Y. Bengio. Neural machine translation by jointly learning
to align and translate.arXiv preprint arXiv:1409.0473, 2014.
[5] W. Banzhaf, P. Nordin, R. E. Keller, and F. D. Francone.Genetic Programming: An
Introduction on the Automatic Evolution of computer programs and its Applications. The
Morgan Kaufmann Series in Artificial Intelligence, 1998.
[6] J. Bausch, A. W. Senior, F. J. H. Heras, T. Edlich, A. Davies, M. Newman, C. Jones,
K. Satzinger, M. Y. Niu, S. Blackwell, G. Holland, D. Kafri, J. Atalaya, C. Gidney,
D. Hassabis, S. Boixo, H. Neven, and P. Kohli. Learning high-accuracy error decoding
for quantum processors.Nature, 635(8040):834–840, 2024. doi: 10.1038/s41586-0
24-08148-8.
[7] D. A. Boiko, R. MacKnight, B. Kline, and G. Gomes. Autonomous chemical research
with large language models.Nature, 624(7992):570–578, 2023. doi: 10.1038/s415
86-023-06792-0.
[8] P. Boyvalenkov, S. Dodunekov, and O. Musin. A survey on the kissing numbers.Serdica
Math. J., 38(4):507–522, 2012. ISSN 1310-6600.
[9] J. Bradbury, R. Frostig, P. Hawkins, M. J. Johnson, C. Leary, D. Maclaurin, G. Necula,
A. Paszke, J. VanderPlas, S. Wanderman-Milne, and Q. Zhang. JAX: composable
transformations of Python+NumPy programs, 2018. URLhttp://github.com/j
ax-ml/jax.
[10] A.M.Bran,S.Cox,O.Schilter,C.Baldassari,A.D.White,andP.Schwaller. Augmenting
large language models with chemistry tools.Nature Machine Intelligence, 6(5):525–
535, 2024. doi: 10.1038/s42256-024-00832-8.
[11] A. M. Bran, T. A. Neukomm, D. P. Armstrong, Z. Jončev, and P. Schwaller. Chemical
reasoning in LLMs unlocks steerable synthesis planning and reaction mechanism
elucidation. InarXiv preprint arXiv:2503.08537, 2025.
[12] M. Caldas Ramos, C. J. Collison, and A. D. White. A review of large language models
and autonomous agents in chemistry.Chemical Science, 16:2514–2572, 2025. doi:
10.1039/D4SC03921A.
[13] P. S. Castro, N. Tomasev, A. Anand, N. Sharma, R. Mohanta, A. Dev, K. Perlin, S. Jain,
K. Levin, N. Éltető, W. Dabney, A. Novikov, G. C. Turner, M. K. Eckstein, N. D. Daw,
K. J. Miller, and K. L. Stachenfeld. Discovering symbolic cognitive models from human
and animal behavior. InInternational Conference on Machine Learning, 2025.
[14] A. Chen, D. M. Dohan, and D. R. So. EvoPrompting: Language models for code-level
neural architecture search. In Advances in Neural Information Processing Systems,
2023.
[15] T. Chen, B. Xu, and K. Devleker. Automating GPU kernel generation with DeepSeek-R1
and inference time scaling, 2025. URLhttps://developer.nvidia.com/blog/
automating-gpu-kernel-generation-with-deepseek-r1-and-inference
-time-scaling.
[16] X. Chen, C. Liang, D. Huang, E. Real, K. Wang, H. Pham, X. Dong, T. Luong, C.-J.
Hsieh, Y. Lu, and Q. V. Le. Symbolic discovery of optimization algorithms.Advances
in Neural Information Processing Systems, 2023.
[17] A.CloningerandS.Steinerberger. Onsupremaofautoconvolutionswithanapplication
to Sidon sets.Proceedings of the American Mathematical Society, 145(8):3191–3200,
2017.
[18] H. Cohn and F. Gonçalves. An optimal uncertainty principle in twelve dimensions via
modular forms.Inventiones mathematicae, 217:799–831, 2019.
[19] K. M. Collins, A. Q. Jiang, S. Frieder, L. Wong, M. Zilka, U. Bhatt, T. Lukasiewicz, Y. Wu,
J. B. Tenenbaum, W. Hart, et al. Evaluating language models for mathematics through
interactions. Proceedings of the National Academy of Sciences, 121(24):e2318124121,
2024.
[20] K. D. Cooper, D. Subramanian, and L. Torczon. Adaptive optimizing compilers for the
21st century.The Journal of Supercomputing, 23:7–22, 2002.
[21] M. Cranmer. Interpretable machine learning for science with pysr and symbolicre-
gression. jl.arXiv preprint arXiv:2305.01582, 2023.
[22] T. Dao, D. Fu, S. Ermon, A. Rudra, and C. Ré. Flashattention: Fast and memory-
efficient exact attention with io-awareness.Advances in neural information processing
systems, 35:16344–16359, 2022.
[23] A. Davies, P. Veličković, L. Buesing, S. Blackwell, D. Zheng, N. Tomašev, R. Tanburn,
P. Battaglia, C. Blundell, A. Juhász, M. Lackenby, G. Williamson, D. Hassabis, and
P. Kohli. Advancing mathematics by guiding human intuition with AI.Nature, 600
(7887):70–74, 2021. doi: 10.1038/s41586-021-04086-x.
[24] J. S. Ellenberg, C. S. Fraser-Taliente, T. R. Harvey, K. Srivastava, and A. V. Sutherland.
Generative modelling for mathematical discovery.arXiv preprint arXiv:2503.11061,
2025.
[25] P. Erdős. Some remarks on number theory.Riveon Lematematika, 9:45–48, 1955.
[26] A.Fawzi,M.Balog,A.Huang,T.Hubert,B.Romera-Paredes,M.Barekatain,A.Novikov,
F. J. R. Ruiz, J. Schrittwieser, G. Swirszcz, D. Silver, D. Hassabis, and P. Kohli. Discov-
ering faster matrix multiplication algorithms with reinforcement learning.Nature,
610(7930):47–53, 2022. doi: 10.1038/s41586-022-05172-4.
[27] C. Fernando, D. Banarse, H. Michalewski, S. Osindero, and T. Rocktäschel. Prompt-
breeder: Self-referential self-improvement via prompt evolution. arXiv preprint
arXiv:2309.16797, 2023.
[28] N. Ferruz and B. Höcker. Controllable protein design with language models.Nature
Machine Intelligence, 4(6):521–532, 2022.
[29] E. Friedman. Erich's Packing Center.https://erich-friedman.github.io/pa
cking/, 2025. Accessed: 2025-04-22.
[30] F. Frohnert, X. Gu, M. Krenn, and E. van Nieuwenburg. Discovering emergent connec-
tions in quantum physics research via dynamic word embeddings.Machine Learning:
Science and Technology, 6(1):015029, 2025. doi: 10.1088/2632-2153/adb00a.
[31] M. Ganzhinov. Highly symmetric lines. InarXiv preprint arXiv:2207.08266v1, 2022.
[32] Gemini team. Gemini 2.5: Our most intelligent AI model, 2025. URL https:
//blog.google/technology/google-deepmind/gemini-model-thinking-u
pdates-march-2025.
[33] F. Gonçalves, D. O. e Silva, and S. Steinerberger. Hermite polynomials, linear flows
on the torus, and an uncertainty principle for roots.Journal of Mathematical Analysis
and Applications, 451(2):678–711, 2017.
[34] J. Gottweis, W.-H. Weng, A. Daryin, T. Tu, A. Palepu, P. Sirkovic, A. Myaskovsky,
F. Weissenberger, K. Rong, R. Tanno, K. Saab, D. Popovici, J. Blum, F. Zhang, K. Chou,
A. Hassidim, B. Gokturk, A. Vahdat, P. Kohli, Y. Matias, A. Carroll, K. Kulkarni,
N. Tomasev, Y. Guan, V. Dhillon, E. D. Vaishnav, B. Lee, T. R. D. Costa, J. R. Penadés,
G. Peltz, Y. Xu, A. Pawlosky, A. Karthikesalingam, and V. Natarajan. Towards an AI
co-scientist. arXiv preprint arXiv:2502.18864, 2025.
[35] A. Grayeli, A. Sehgal, O. Costilla Reyes, M. Cranmer, and S. Chaudhuri. Symbolic
regression with a learned concept library.Advances in Neural Information Processing
Systems, 37:44678–44709, 2024.
[36] M. Gridach, J. Nanavati, C. Mack, K. Z. E. Abidine, and L. Mendes. Agentic AI for
scientific discovery: A survey of progress, challenges, and future directions. InICLR
Workshop: Towards Agentic AI for Science: Hypothesis Generation, Comprehension,
Quantification, and Validation, 2025.
[37] X. Gu and M. Krenn. Interesting scientific idea generation using knowledge
graphs and LLMs: Evaluations with 100 research group leaders. InarXiv preprint
arXiv:2405.17044, 2024.
[38] S. Guo, A. H. Shariatmadari, G. Xiong, and A. Zhang. Embracing foundation models
for advancing scientific discovery. InProceedings of the IEEE International Conference
on Big Data, pages 1746–1755, 2024. doi: 10.1109/bigdata62323.2024.10825618.
[39] K. Gyarmati, F. Hennecart, and I. Z. Ruzsa. Sums and differences of finite sets.
Functiones et Approximatio Commentarii Mathematici, 37(1):175–186, 2007.
[40] J. K. Haugland. The minimum overlap problem revisited. arXiv preprint
arXiv:1609.08000, 2016.
[41] E. Hemberg, S. Moskal, and U.-M. O'Reilly. Evolving code with a large language
model. Genetic Programming and Evolvable Machines, 25(2):21, 2024. doi: 10.1007/
s10710-024-09494-2.
[42] J. E. Hopcroft and L. R. Kerr. On minimizing the number of multiplications necessary
for matrix multiplication.SIAM J. Appl. Math., 20(1):30–36, Jan. 1971. ISSN 0036-
1399. doi: 10.1137/0120004.
[43] K. Huang, Y. Qu, H. Cousins, W. A. Johnson, D. Yin, M. Shah, D. Zhou, R. Altman,
M. Wang, and L. Cong. CRISPR-GPT: An LLM agent for automated design of gene-
editing experiments. InarXiv preprint arXiv:2404.18021, 2024.
[44] L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng,
B. Qin, et al. A survey on hallucination in large language models: Principles, taxonomy,
challenges, and open questions.ACM Transactions on Information Systems, 43(2):
1–55, 2025.
[45] S. Jia, C. Zhang, and V. Fung. LLMatDesign: Autonomous materials discovery with
large language models. InarXiv preprint arXiv:2406.13163, 2024.
[46] J. Jumper, R. Evans, A. Pritzel, T. Green, M. Figurnov, O. Ronneberger, K. Tunyasuvu-
nakool, R. Bates, A. Žídek, A. Potapenko, A. Bridgland, C. Meyer, S. A. A. Kohl, A. J.
Ballard, A. Cowie, B. Romera-Paredes, S. Nikolov, R. Jain, J. Adler, T. Back, S. Petersen,
D. Reiman, E. Clancy, M. Zielinski, M. Steinegger, M. Pacholska, T. Berghammer, S. Bo-
denstein, D. Silver, O. Vinyals, A. W. Senior, K. Kavukcuoglu, P. Kohli, and D. Hassabis.
Highly accurate protein structure prediction with AlphaFold.Nature, 596(7873):
583–589, 2021. doi: 10.1038/s41586-021-03819-2.
[47] M. Kauers and J. Moosbauer. Flip graphs for matrix multiplication. InProceedings
of the 2023 International Symposium on Symbolic and Algebraic Computation, pages
381–388, 2023.
[48] M. Kauers and J. Moosbauer. Some new non-commutative matrix multiplication
algorithms of size(𝑛,𝑚, 6). ACM Commun. Comput. Algebra, 58(1):1–11, Jan. 2025.
ISSN 1932-2232. doi: 10.1145/3712020.3712021.
[49] M. Kauers and I. Wood. Consequences of the Moosbauer-Poole algorithms.arXiv
preprint arXiv:2505.05896, 2025.
[50] D. P. Kingma and J. Ba. Adam: A method for stochastic optimization. InInternational
Conference on Learning Representations (ICLR), 2015.
[51] J. R. Koza. Genetic programming as a means for programming computers by natural
selection. Statistics and Computing, 4(2):87–112, 1994. doi: 10.1007/BF00175355.
[52] J. D. Laderman. A noncommutative algorithm for multiplying3× 3 matrices using
23 multiplications.Bulletin of the American Mathematical Society, 82(1):126 – 128,
1976.
[53] R. Lam, A. Sanchez-Gonzalez, M. Willson, P. Wirnsberger, M. Fortunato, F. Alet,
S. Ravuri, T. Ewalds, Z. Eaton-Rosen, W. Hu, A. Merose, S. Hoyer, G. Holland,
O. Vinyals, J. Stott, A. Pritzel, S. Mohamed, and P. Battaglia. Learning skillful
medium-range global weather forecasting.Science, 382(6677):1416–1421, 2023. doi:
10.1126/science.adi2336.
[54] W. B. Langdon and R. Poli.Foundations of genetic programming. Springer Science &
Business Media, 2013.
[55] R. Lange, Y. Tian, and Y. Tang. Large language models as evolution strategies. In
ProceedingsoftheGeneticandEvolutionaryComputationConferenceCompanion ,GECCO
'24 Companion, pages 579–582. Association for Computing Machinery, 2024. doi:
10.1145/3638530.3654238.
[56] R. T. Lange, A. Prasad, Q. Sun, M. Faldor, Y. Tang, and D. Ha. The AI CUDA engineer:
Agentic CUDA kernel discovery, optimization and composition. Technical report,
Sakana AI, 02 2025.
[57] J. Lehman, J. Gordon, S. Jain, K. Ndousse, C. Yeh, and K. O. Stanley. Evolution through
large models. InHandbook of evolutionary machine learning, pages 331–366. Springer,
2023.
[58] J. Lehman, J. Gordon, S. Jain, K. Ndousse, C. Yeh, and K. O. Stanley.Evolution
Through Large Models, pages 331–366. Springer Nature Singapore, 2024. doi:
10.1007/978-981-99-3814-8\_11.
[59] P.-H. Li, Y.-Y. Sun, H.-F. Juan, C.-Y. Chen, H.-K. Tsai, and J.-H. Huang. A large language
model framework for literature-based disease–gene association prediction.Briefings in
Bioinformatics, 26(1):bbaf070, 02 2025. ISSN 1477-4054. doi: 10.1093/bib/bbaf070.
[60] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond, T. Eccles, J. Keeling,
F. Gimeno, A. D. Lago, T. Hubert, P. Choy, C. de Masson d'Autume, I. Babuschkin,
X. Chen, P.-S. Huang, J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz,
E. S. Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals. Competition-
level code generation with AlphaCode.Science, 378(6624):1092–1097, 2022. doi:
10.1126/science.abq1158.
[61] H. Lin, M. Maas, M. Roquemore, A. Hasanzadeh, F. Lewis, Y. Simonson, T.-W. Yang,
A. Yazdanbakhsh, D. Altinbüken, F. Papa, et al. ECO: An LLM-driven efficient code
optimizer for warehouse scale computers.arXiv preprint arXiv:2503.15669, 2025.
[62] Z. Lin, H. Akin, R. Rao, B. Hie, Z. Zhu, W. Lu, N. Smetanin, R. Verkuil, O. Kabeli,
Y. Shmueli, A. dos Santos Costa, M. Fazel-Zarandi, T. Sercu, S. Candido, and A. Rives.
Evolutionary-scale prediction of atomic-level protein structure with a language model.
Science, 379(6637):1123–1130, 2023. doi: 10.1126/science.ade2574.
[63] F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, and Q. Zhang. Evolution of
heuristics: Towards efficient automatic algorithm design using large language model.
arXiv preprint arXiv:2401.02051, 2024.
[64] F. Luo, J. Zhang, Q. Wang, and C. Yang. Leveraging prompt engineering in large
language models for accelerating chemical research.ACS Central Science, 2025. doi:
10.1021/acscentsci.4c01935.
[65] Z. Luo, Z. Yang, Z. Xu, W. Yang, and X. Du. LLM4SR: A survey on large language
models for scientific research. InarXiv preprint arXiv:2501.04306, 2025.
[66] H. Ma, A. Narayanaswamy, P. Riley, and L. Li. Evolving symbolic density functionals.
Science Advances, 8(36):eabq0279, 2022. doi: 10.1126/sciadv.abq0279.
[67] A. Madani, B. Krause, E. R. Greene, S. Subramanian, B. P. Mohr, J. M. Holton, J. L.
Olmos, C. Xiong, Z. Z. Sun, R. Socher, J. S. Fraser, and N. Naik. Large language models
generatefunctionalproteinsequencesacrossdiversefamilies. NatureBiotechnology, 41
(8):1099–1106, August 2023. ISSN 1087-0156. doi: 10.1038/s41587-022-01618-2.
[68] D. J. Mankowitz, A. Michi, A. Zhernov, M. Gelmi, M. Selvi, C. Paduraru, E. Leurent,
S. Iqbal, J.-B. Lespiau, A. Ahern, T. Köppe, K. Millikin, S. Gaffney, S. Elster, J. Broshear,
C.Gamble, K.Milan, R.Tung, M.Hwang, T.Cemgil, M.Barekatain, Y.Li, A.Mandhane,
T.Hubert, J.Schrittwieser, D.Hassabis, P.Kohli, M.Riedmiller, O.Vinyals, andD.Silver.
Faster sorting algorithms discovered using deep reinforcement learning.Nature, 618
(7964):257–263, 2023. doi: 10.1038/s41586-023-06004-9.
[69] H. Massalin. Superoptimizer - A look at the smallest program. In R. H. Katz and
M.Freeman, editors,ProceedingsoftheSecondInternationalConferenceonArchitectural
Support for Programming Languages and Operating Systems (ASPLOS II), Palo Alto,
California, USA, October 5-8, 1987, pages 122–126. ACM Press, 1987. doi: 10.1145/
36206.36194.
[70] M. Matolcsi and C. Vinuesa. Improved bounds on the supremum of autoconvolutions.
Journal of mathematical analysis and applications, 372(2):439–447, 2010.
[71] S. Miret and N. M. A. Krishnan. Are LLMs ready for real-world materials discovery?
In arXiv preprint arXiv:2402.05200, 2024.
[72] J. Moosbauer and M. Poole. Flip graphs with symmetry and new matrix multiplication
schemes. arXiv preprint arXiv:2502.04514, 2025.
[73] C. Morris, M. Jurado, and J. Zutty. Llm guided evolution-the automation of mod-
els advancing models. InProceedings of the Genetic and Evolutionary Computation
Conference, pages 377–384, 2024.
[74] J.-B. Mouret and J. Clune. Illuminating search spaces by mapping elites.arXiv preprint
arXiv:1504.04909, 2015.
[75] V. Naumov, D. Zagirova, S. Lin, Y. Xie, W. Gou, A. Urban, N. Tikhonova, K. Alawi,
M. Durymanov, F. Galkin, S. Chen, D. Sidorenko, M. Korzinkin, M. Scheibye-Knudsen,
A. Aspuru-Guzik, E. Izumchenko, D. Gennert, F. W. Pun, M. Zhang, P. Kamya, A. Aliper,
F. Ren, and A. Zhavoronkov. DORA AI scientist: Multi-agent virtual research team
for scientific exploration discovery and automated report generation. InbioRxiv
preprint:10.1101/2025.03.06.641840. Cold Spring Harbor Laboratory, 2025. doi:
10.1101/2025.03.06.641840.
[76] OpenAI. Introducing OpenAI o3 and o4-mini, 2025. URLhttps://openai.com/i
ndex/introducing-o3-and-o4-mini/.
[77] OpenXLA. XLA: composable transformations of Python+NumPy programs. URL
https://github.com/openxla/xla.
[78] H. Pan, N. Mudur, W. Taranto, M. Tikhanovskaya, S. Venugopalan, Y. Bahri, M. P.
Brenner, and E.-A. Kim. Quantum many-body physics calculations with large language
models. Communications Physics, 8(1):49, 2025. doi: 10.1038/s42005-025-01956-y.
[79] D. Pantiukhin, B. Shapkin, I. Kuznetsov, A. A. Jost, and N. Koldunov. Accelerating Earth
science discovery via multi-agent LLM systems. InarXiv preprint arXiv:2503.05854,
2025.
[80] Z. Rasheed, M. Waseem, A. Ahmad, K.-K. Kemell, W. Xiaofeng, A. N. Duc, and P. Abra-
hamsson. Can large language models serve as data analysts? a multi-agent assisted
approach for qualitative data analysis.arXiv preprint arXiv:2402.01386, 2024.
[81] S. Ren, P. Jian, Z. Ren, C. Leng, C. Xie, and J. Zhang. Towards scientific intelligence:
A survey of LLM-based scientific agents. InarXiv preprint arXiv:2503.24047, 2025.
[82] A. Rives, J. Meier, T. Sercu, S. Goyal, Z. Lin, J. Liu, D. Guo, M. Ott, C. L. Zitnick, J. Ma,
and R. Fergus. Biological structure and function emerge from scaling unsupervised
learning to 250 million protein sequences.Proceedings of the National Academy of
Sciences, 118(15):e2016239118, 2021. doi: 10.1073/pnas.2016239118.
[83] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont,
F. J. R. Ruiz, J. Ellenberg, P. Wang, O. Fawzi, P. Kohli, and A. Fawzi. Mathematical
discoveries from program search with large language models.Nature, 625(7995):
468–475, 2023. doi: 10.1038/s41586-023-06924-6.
[84] F. J. R. Ruiz, T. Laakkonen, J. Bausch, M. Balog, M. Barekatain, F. J. H. Heras,
A. Novikov, N. Fitzpatrick, B. Romera-Paredes, J. van de Wetering, A. Fawzi, K. Me-
ichanetzidis, and P. Kohli. Quantum circuit optimization with AlphaTensor.Nature
Machine Intelligence, 7(3):374–385, 2025. doi: 10.1038/s42256-025-01001-1.
[85] O. A. Sarumi and D. Heider. Large language models and their applications in bioinfor-
matics. Computational and Structural Biotechnology Journal, 23:3498–3505, 2024.
ISSN 2001-0370. doi: https://doi.org/10.1016/j.csbj.2024.09.031.
[86] E. Schkufza, R. Sharma, and A. Aiken. Stochastic superoptimization. In V. Sarkar and
R. Bodík, editors,Architectural Support for Programming Languages and Operating
Systems, ASPLOS 2013, Houston, TX, USA, March 16-20, 2013, pages 305–316. ACM,
2013. doi: 10.1145/2451116.2451150.
[87] M. Schmidt and H. Lipson. Distilling free-form natural laws from experimental data.
Science, 324(5923):81–85, 2009. doi: 10.1126/science.1165893.
[88] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao. Reflexion: Language
agents with verbal reinforcement learning.Advances in Neural Information Processing
Systems, 36:8634–8652, 2023.
[89] P. Shojaee, K. Meidani, S. Gupta, A. B. Farimani, and C. K. Reddy. LLM-SR: Scientific
equation discovery via programming with large language models. InInternational
Conference on Learning Representations, 2025.
[90] C. Si, D. Yang, and T. Hashimoto. Can LLMs generate novel research ideas? a large-
scalehumanstudywith100+NLPresearchers. In InternationalConferenceonLearning
Representations, 2025.
[91] A. Smirnov. Several bilinear algorithms for matrix multiplication problems⟨3,𝑃,𝑄⟩.
https://www.researchgate.net/publication/350897049_Several_Bilin
ear_Algorithms_for_Matrix_Multiplication_Problems_3_P_Q, 04 2021.
[92] A. Smirnov. Bilinear algorithm for matrix multiplication⟨4× 4× 9; 104⟩. an irreducibly
irrational solution of the brent system?https://www.researchgate.net/pub
lication/364167198_Bilinear_Algorithm_for_Matrix_Multiplication_
4x4x9_104_An_irreducibly_irrational_solution_of_the_Brent_system,
10 2022.
[93] A. V. Smirnov. The bilinear complexity and practical algorithms for matrix multipli-
cation. Computational Mathematics and Mathematical Physics, 53(12):1781–1795,
2013.
[94] Z. Song, M. Ju, C. Ren, Q. Li, C. Li, Q. Zhou, and J. Wang. LLM-Feynman: Leveraging
large language models for universal scientific formula and theory discovery. InarXiv
preprint arXiv:2503.06512, 2025.
[95] V. Strassen. Gaussian elimination is not optimal.Numerische mathematik, 13(4):
354–356, 1969.
[96] A. Surina, A. Mansouri, L. Quaedvlieg, A. Seddas, M. Viazovska, E. Abbe, and C. Gul-
cehre. Algorithm discovery with LLMs: Evolutionary search meets reinforcement
learning. InarXiv preprint arXiv:2504.05108, 2025.
[97] R. Tanese. Distributed genetic algorithms for function optimization. University of
Michigan, 1989.
[98] A. Thakur, G. Tsoukalas, Y. Wen, J. Xin, and S. Chaudhuri. An in-context learning
agent for formal theorem-proving. InConference on Language Models, 2024.
[99] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong. Solving olympiad geometry without
human demonstrations.Nature, 625(7995):476–482, 2024.
[100] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and
I. Polosukhin. Attention is all you need. InAdvances in Neural Information Processing
Systems, 2017.
[101] P. Veličković, A. Vitvitskyi, L. Markeeva, B. Ibarz, L. Buesing, M. Balog, and A. Novikov.
Amplifying human performance in combinatorial competitive programming. 2024.
[102] A. Verma, L. Pedrosa, M. Korupolu, D. Oppenheimer, E. Tune, and J. Wilkes. Large-
scale cluster management at Google with Borg. InProceedings of the Tenth European
Conference on Computer Systems, EuroSys '15, New York, NY, USA, 2015. Association
for Computing Machinery. ISBN 9781450332385. doi: 10.1145/2741948.2741964.
[103] S. Verma, A. Goyal, A. Mathur, A. Anand, and S. Ranu. GRAIL: Graph edit distance
and node alignment using llm-generated code. InInternational Conference on Machine
Learning, 2025.
[104] C. Vinuesa del Rio.Generalized Sidon sets. PhD thesis, Universidad Autónoma de
Madrid, 2010.
[105] H. Wang, M. Skreta, C. T. Ser, W. Gao, L. Kong, F. Strieth-Kalthoff, C. Duan, Y. Zhuang,
Y. Yu, Y. Zhu, Y. Du, A. Aspuru-Guzik, K. Neklyudov, and C. Zhang. Efficient evo-
lutionary search over chemical space with large language models. InInternational
Conference on Learning Representations, 2025.
[106] Q. Wang, D. Downey, H. Ji, and T. Hope. SciMON: Scientific inspiration machines
optimized for novelty. InProceedings of the 62nd Annual Meeting of the Association
forComputationalLinguistics(Volume1: LongPapers) ,pages279–299,Bangkok,Thailand,
2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.18.
[107] E. P. White. A new bound for Erdős' minimum overlap problem.Acta Arithmetica,
208:235–255, 2023.
[108] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang, S. Zhang, J. Liu,
A. H. Awadallah, R. W. White, D. Burger, and C. Wang. AutoGen: Enabling next-gen
LLM applications via multi-agent conversation. InarXiv preprint arXiv:2308.08155,
2023.
[109] Y. Xia, P. Jin, S. Xie, L. He, C. Cao, R. Luo, G. Liu, Y. Wang, Z. Liu, Y.-J. Chen, Z. Guo,
Y. Bai, P. Deng, Y. Min, Z. Lu, H. Hao, H. Yang, J. Li, C. Liu, J. Zhang, J. Zhu, R. Bi,
K. Wu, W. Zhang, K. Gao, Q. Pei, Q. Wang, X. Liu, Y. Li, H. Zhu, Y. Lu, M. Ma, Z. Wang,
T. Xie, K. Maziarz, M. Segler, Z. Yang, Z. Chen, Y. Shi, S. Zheng, L. Wu, C. Hu, P. Dai,
T.-Y. Liu, H. Liu, and T. Qin. Nature language model: Deciphering the language of
nature for scientific discovery. InarXiv preprint arXiv:2502.07527v2, 2025.
[110] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, and
A. Anandkumar. Leandojo: Theorem proving with retrieval-augmented language
models. Advances in Neural Information Processing Systems, 36:21573–21612, 2023.
[111] K. Yang, G. Poesia, J. He, W. Li, K. Lauter, S. Chaudhuri, and D. Song. Formal
mathematical reasoning: A new frontier in AI.arXiv preprint arXiv:2412.16075, 2024.
[112] Z. Yang, X. Du, J. Li, J. Zheng, S. Poria, and E. Cambria. Large language models for
automated open-domain scientific hypotheses discovery. InFindings of the Associa-
tion for Computational Linguistics: ACL 2024, pages 13545–13565. Association for
Computational Linguistics, 2024. doi: 10.18653/v1/2024.findings-acl.804.
[113] Z. Yang, W. Liu, B. Gao, T. Xie, Y. Li, W. Ouyang, S. Poria, E. Cambria, and D. Zhou.
MOOSE-Chem: Large language models for rediscovering unseen chemistry scientific
hypotheses. InInternational Conference on Learning Representations, 2025.
[114] S.Yao, J.Zhao, D.Yu, N.Du, I.Shafran, K.Narasimhan, andY.Cao. React: Synergizing
reasoning and acting in language models. InInternational Conference on Learning
Representations (ICLR), 2023.
[115] S. Yao, F. Liu, X. Lin, Z. Lu, Z. Wang, and Q. Zhang. Multi-objective evolution of
heuristic using large language model. InAAAI Conference on Artificial Intelligence,
volume 39, pages 27144–27152, 2025. doi: 10.1609/aaai.v39i25.34922.
[116] G. Ye, X. Cai, H. Lai, X. Wang, J. Huang, L. Wang, W. Liu, and Z. Zeng. DrugAssist: A
large language model for molecule optimization. InarXiv preprint arXiv:2401.10334,
2023.
[117] H. Ye, J. Wang, Z. Cao, F. Berto, C. Hua, H. Kim, J. Park, and G. Song. ReEvo: Large
language models as hyper-heuristics with reflective evolution. InAdvances in Neural
Information Processing Systems, volume 37, 2024.
[118] F. Zhang, S. Nguyen, Y. Mei, and M. Zhang.Genetic Programming for Production
Scheduling. Springer, 2021.
[119] H. Zhang, Y. Song, Z. Hou, S. Miret, and B. Liu. HoneyComb: A flexible LLM-based
agent system for materials science. In Y. Al-Onaizan, M. Bansal, and Y.-N. Chen,
editors, Findings of the Association for Computational Linguistics: EMNLP 2024, pages
3369–3382. Association for Computational Linguistics, Nov. 2024. doi: 10.18653/v1/
2024.findings-emnlp.192.
[120] Y. Zhou, H. Liu, T. Srivastava, H. Mei, and C. Tan. Hypothesis generation with large
language models. In L. Peled-Cohen, N. Calderon, L. Lissak, and R. Reichart, editors,
Proceedings of the 1st Workshop on NLP for Science (NLP4Science), pages 117–139.
Association for Computational Linguistics, 2024. doi: 10.18653/v1/2024.nlp4scien
ce-1.10.

## A. 更快的矩阵乘法：完整结果

**完整结果表。** 我们在表 3 中给出 AlphaEvolve 取得的最佳秩。总体上，我们在实验中考虑了 54 个矩阵乘法规模。这些规模大致代表满足 2 ≤ m, n ≤ 5 的 ⟨m, n, p⟩（对 p 设有合理的截断）。由于底层矩阵乘法张量的对称性，对三个轴的任意置换都存在等价算法，因此我们聚焦于排序后的规模 m ≤ n ≤ p。

在除两个之外的所考虑规模上，AlphaEvolve 发现的程序要么匹配、要么超越了已知最佳秩。顺便一提，我们在增大问题规模时遇到了一些困难：当我们在配备单个 GPU 加速器的评估器上、以 1000 个随机种子对超出 ⟨5, 5, 5⟩ 的规模运行所发现的程序时，经常内存耗尽。因此，把我们的设置扩展到更大的矩阵规模还需要进一步的优化。

| ⟨m, n, p⟩ | 已知最好 [参考文献] | AlphaEvolve |
|---|---|---|
| ⟨2,2,2⟩ | 7 [95] | 7 |
| ⟨2,2,3⟩ | 11 [93] | 11 |
| ⟨2,2,4⟩ | 14 [93] | 14 |
| ⟨2,2,5⟩ | 18 [93] | 18 |
| ⟨2,2,6⟩ | 21 [93] | 21 |
| ⟨2,2,7⟩ | 25 [93] | 25 |
| ⟨2,2,8⟩ | 28 [93] | 28 |
| ⟨2,2,9⟩ | 32 [93] | 32 |
| ⟨2,2,10⟩ | 35 [93] | 35 |
| ⟨2,2,11⟩ | 39 [93] | 39 |
| ⟨2,2,12⟩ | 42 [93] | 42 |
| ⟨2,2,13⟩ | 46 [93] | 46 |
| ⟨2,2,14⟩ | 49 [93] | 49 |
| ⟨2,2,15⟩ | 53 [93] | 53 |
| ⟨2,2,16⟩ | 56 [93] | 56 |
| ⟨2,3,3⟩ | 15 [93] | 15 |
| ⟨2,3,4⟩ | 20 [93] | 20 |
| ⟨2,3,5⟩ | 25 [93] | 25 |
| ⟨2,3,6⟩ | 30 [93] | 30 |
| ⟨2,3,7⟩ | 35 [93] | 35 |
| ⟨2,3,8⟩ | 40 [93] | 40 |
| ⟨2,3,9⟩ | 45 [93] | 45 |
| ⟨2,3,10⟩ | 50 [93] | 50 |
| ⟨2,4,4⟩ | 26 [93] | 26 |
| ⟨2,4,5⟩ | 33 [42] | 32 |
| ⟨2,4,6⟩ | 39 [93] | 39 |
| ⟨2,4,7⟩ | 46 [93] | 45 |
| ⟨2,4,8⟩ | 52 [93] | 51 |
| ⟨2,5,5⟩ | 40 [93] | 40 |
| ⟨2,5,6⟩ | 48 [93] | 47 |
| ⟨3,3,3⟩ | 23 [52] | 23 |
| ⟨3,3,4⟩ | 29 [93] | 29 |
| ⟨3,3,5⟩ | 36 [93] | 36 |
| ⟨3,3,6⟩ | 40 [93] | 40 |
| ⟨3,3,7⟩ | 49 [93] | 49 |
| ⟨3,3,8⟩ | 55 [93] | 55 |
| ⟨3,4,4⟩ | 38 [93] | 38 |
| ⟨3,4,5⟩ | 47 [26] | 47 |
| ⟨3,4,6⟩ | 56 [48] | 54 |
| ⟨3,4,7⟩ | 66 [91] | 63 |
| ⟨3,4,8⟩ | 75 [91] | 74 |
| ⟨3,5,5⟩ | 58 [91] | 58 |
| ⟨3,5,6⟩ | 70 [48] | 68 |
| ⟨3,5,7⟩ | 82 [91] | 80 |
| ⟨4,4,4⟩ | 49 [95] | 48 |
| ⟨4,4,5⟩ | 62 [47] | 61 |
| ⟨4,4,6⟩ | 73 [48] | 73 |
| ⟨4,4,7⟩ | 87 [93, 95] | 85 |
| ⟨4,4,8⟩ | 98 [95] | 96 |
| ⟨4,4,9⟩ | 104 [92] | 108 |
| ⟨4,5,5⟩ | 76 [26] | 76 |
| ⟨4,5,6⟩ | 93 [48] | 90 |
| ⟨5,5,5⟩ | 93 [72] | 93 |
| ⟨6,6,6⟩ | 153 [72] | 156 |

表 3|表 2 的完整版，展示 AlphaEvolve 在所有考虑参数下张量分解取得的最佳秩。在 54 个目标中，AlphaEvolve 在 38 个情形匹配现有技术、在 14 个情形超越（绿色）、在 2 个情形落后（红色）。在所有情形中，AlphaEvolve 都给出精确算法，分解使用整数或半整数元素。对 ⟨3, 4, 7⟩、⟨4, 4, 4⟩ 与 ⟨4, 4, 8⟩，AlphaEvolve 发现的算法使用复值乘法，可用于复或实值矩阵的精确乘法。本表中的分解见配套 Google Colab。

注：并行工作 [49] 也找到了 ⟨4, 5, 6⟩ 的秩 90 算法。

**图 4（左）的放大版。** 在图 9a 至图 9c 中，我们给出图 4（左）的放大版本，它对应发现两个 4×4 矩阵乘法运算的 3D 张量之秩 48 分解的程序。

```
1 @ @ -45 ,9 +45 ,14 @@
2 # EVOLVE - BLOCK - START
3 def _ g e t _ o p t i m i z e r ( self ) -> optax . G r a d i e n t T r a n s f o r m a t i o n :
4 """ R e t u r n s o p t i m i z e r . """
5 - return optax . adam ( self . hypers . l e a r n i n g _ r a t e )
6 + return optax . adamw (
7 + self . hypers . learning_rate , w e i g h t _ d e c a y = self . hypers . w e i g h t _ d e c a y
8 + )
9
10 def _ g e t _ i n i t _ f n ( self ) -> jax . nn . i n i t i a l i z e r s . I n i t i a l i z e r :
11 """ R e t u r n s i n i t i a l i z e r f u n c t i o n . """
12 - return i n i t i a l i z e r s . normal (0.0 , self . hypers . init_scale , jnp . c o m p l e x 6 4 )
13 + # I n i t i a l i z e with a smaller scale to e n c o u r a g e finding low - rank
s o l u t i o n s .
14 + # I nc re as e scale s li gh tl y for better e x p l o r a t i o n .
15 + scale = self . hypers . i n i t _ s c a l e
16 + return i n i t i a l i z e r s . normal (0 + 1 j * 0 , scale * 0.2 , jnp . c o m p l e x 6 4 )
17
18 @ @ -80 ,6 +85 ,66 @@
19 # G r a d i e n t u p d a t e s .
20 updates , o p t _ s t a t e = self . opt . update ( grads , opt_state , d e c o m p o s i t i o n )
21 d e c o m p o s i t i o n = optax . a p p l y _ u p d a t e s ( decomposition , updates )
22 + # Add a small amount of g ra di en t noise to help with e x p l o r a t i o n
23 + rng , g _ n o i s e _ r n g = jax . random . split ( rng )
24 + d e c o m p o s i t i o n = jax . t r e e _ u t i l . tr ee_ ma p (
25 + lambda x : x
26 + + self . hypers . g r a d _ n o i s e _ s t d * jax . random . normal ( g_noise_rng , x .
shape ) ,
27 + decomposition ,
28 + )
29 +
30 + # Add noise to the d e c o m p o s i t i o n p a r a m e t e r s ( e x p l o r a t i o n ) .
31 + _ , n o i s e _ r n g = jax . random . split ( rng )
32 + n o i s e _ s t d = self . _ l i n e a r _ s c h e d u l e (
33 + global_step , start = self . hypers . noise_std , end =0.0
34 + )
35 + d e c o m p o s i t i o n = jax . t r e e _ u t i l . tr ee_ ma p (
36 + lambda x : x + n o i s e _ s t d * jax . random . normal ( noise_rng , x . shape ) ,
37 + decomposition ,
38 + )
39 +
40 + # C yc li ca l a n n e a l i n g for c li pp in g t h r e s h o l d .
41 + c y c l e _ l e n g t h = 2000 # Number of steps per cycle
42 + c y c l e _ p r o g r e s s = (
43 + g l o b a l _ s t e p % c y c l e _ l e n g t h
44 + ) / c y c l e _ l e n g t h # N o r m a l i z e d p ro gr es s within the current cycle [0 ,
1)
45 +
46 + # Map cycle pr og re ss to a s i n u s o i d a l curve . Ranges from 0 to 1.
47 + c l i p _ t h r e s h o l d _ m u l t i p l i e r = (1 + jnp . cos (2 * jnp . pi * c y c l e _ p r o g r e s s ) )
/ 2
48 +
49 + c l i p _ t h r e s h o l d = self . hypers . cl ip _m in + c l i p _ t h r e s h o l d _ m u l t i p l i e r * (
50 + self . hypers . c li p_ ma x - self . hypers . cl ip _m in
51 + )
52 +
53 + def s o f t _ c l i p (x , t h r e s h o l d ) :
54 # Cli pp in g the real and i m a g i n a r y parts s e p a r a t e l y .
55 + x_re = jnp . real ( x )
56 + x_im = jnp . imag ( x )
57 +
58 + x _ r e _ c l i p p e d = jnp . where (
59 + x_re > threshold , t h r e s h o l d + ( x_re - t h r e s h o l d ) * 0.1 , x_re
60 + )
61 + x _ r e _ c l i p p e d = jnp . where (
62 + x _ r e _ c l i p p e d < - threshold ,
63 + - t h r e s h o l d + ( x _ r e _ c l i p p e d + t h r e s h o l d ) * 0.1 ,
64 + x_re_clipped ,
65 + )
```

图 9a|图 4（左）的放大版，给出发现更快 4×4 矩阵乘法算法的程序（1/3）。

```
66 +
67 + x _ i m _ c l i p p e d = jnp . where (
68 + x_im > threshold , t h r e s h o l d + ( x_im - t h r e s h o l d ) * 0.1 , x_im
69 + )
70 + x _ i m _ c l i p p e d = jnp . where (
71 + x _ r e _ c l i p p e d < - threshold ,
72 + - t h r e s h o l d + ( x _ r e _ c l i p p e d + t h r e s h o l d ) * 0.1 ,
73 + x_im_clipped ,
74 + )
75 +
76 + return x _ r e _ c l i p p e d + 1 j * x _ i m _ c l i p p e d
77 +
78 + d e c o m p o s i t i o n = jax . t r e e _ u t i l . tr ee_ ma p (
79 + lambda x : s o f t _ c l i p (x , c l i p _ t h r e s h o l d ) , d e c o m p o s i t i o n
80 + )
81 +
82 r e t u r n decomposition , opt_state , loss
83
84 def _l os s_ fn (
85 @ @ -91 ,13 +156 ,86 @@
86 """ C o m p u t e s ( b a t c h e d ) loss on l e a r n e d d e c o m p o s i t i o n . """
87 # C o m p u t e r e c o n s t r u c t i o n loss .
88 r e c _ t e n s o r = self . _ d e c o m p o s i t i o n _ t o _ t e n s o r ( d e c o m p o s i t i o n )# (B , N , M ,
P )
89 +
90 + # Add noise to the target tensor ( r o b u s t n e s s ) .
91 + rng , n o i s e _ r n g = jax . random . split ( rng )
92 + t a r g e t _ n o i s e = self . hypers . t a r g e t _ n o i s e _ s t d * jax . random . normal (
93 + noise_rng , self . t a r g e t _ t e n s o r . shape
94 + )
95 + n o i s y _ t a r g e t _ t e n s o r = self . t a r g e t _ t e n s o r + t a r g e t _ n o i s e
96 +
97 + # H a l l u c i n a t i o n loss ( e n c o u r a g e s e x p l o r a t i o n by r an do ml y r e p l a c i n g
values )
98 + h a l l u c i n a t i o n _ p r o b = self . hypers . h a l l u c i n a t i o n _ p r o b
99 + h a l l u c i n a t i o n _ s c a l e = self . hypers . h a l l u c i n a t i o n _ s c a l e
100 +
101 + def h a l l u c i n a t e (x , h a l l u c i n a t i o n _ r n g ) :
102 + mask = jax . random . b e r n o u l l i ( h a l l u c i n a t i o n _ r n g , p = h a l l u c i n a t i o n _ p r o b )
103 + noise = h a l l u c i n a t i o n _ s c a l e * jax . random . normal (
104 + h a l l u c i n a t i o n _ r n g , x . shape
105 + )
106 + return jnp . where ( mask , noise , x )
107 +
108 + _ , f a c t o r _ r n g = jax . random . split ( rng )
109 + d e c o m p o s i t i o n = jax . t r e e _ u t i l . tr ee_ ma p (
110 + lambda x : h a l l u c i n a t e (x , jax . random . split ( f a c t o r _ r n g ) [0]) ,
111 + decomposition ,
112 + )
113 +
114 # Add a batch d i m e n s i o n to ` t a r g e t _ t e n s o r` to e n s u r e c o r r e c t
b r o a d c a s t i n g .
115 # D e f i n e the loss as the L2 r e c o n s t r u c t i o n error .
116 - re c_ lo ss = l 2 _ l o s s _ c o m p l e x ( self . t a r g e t _ t e n s o r [ None , ...] , r e c _ t e n s o r )
117 + re c_ lo ss = l 2 _ l o s s _ c o m p l e x ( n o i s y _ t a r g e t _ t e n s o r [ None , ...] , r e c _ t e n s o r )
118
119 # We must r e t u r n a real - v a l u e d loss .
120 - return jnp . real ( re c_ lo ss )
121
122 + # D i s c r e t i z a t i o n loss ( e n c o u r a g e entries to be m u l t i p l e s of 1/2 or
integer ) .
123 + def d i s t _ t o _ h a l f _ i n t s ( x ) :
124 + x_re = jnp . real ( x )
125 + x_im = jnp . imag ( x )
126 + return jnp . minimum (
127 + jnp . abs ( x_re - jnp . round ( x_re * 2) / 2) ,
128 + jnp . abs ( x_im - jnp . round ( x_im * 2) / 2) ,
129 + )
130 +
```

图 9b|图 4（左）的放大版，给出发现更快 4×4 矩阵乘法算法的程序（2/3）。

```
131 + def d i s t _ t o _ i n t s ( x ) :
132 + return jnp . abs ( x - jnp . round ( x ) )
133 +
134 + d i s c r e t i z a t i o n _ l o s s = 0.0
135 + for factor in d e c o m p o s i t i o n :
136 + d i s c r e t i z a t i o n _ l o s s += jnp . mean ( d i s t _ t o _ h a l f _ i n t s ( factor ) )
137 + d i s c r e t i z a t i o n _ l o s s += jnp . mean ( d i s t _ t o _ i n t s ( factor ) )
138 +
139 + d i s c r e t i z a t i o n _ l o s s /= (
140 + len ( d e c o m p o s i t i o n ) * 2
141 + ) # average across all factors and loss c o m p o n e n t s
142 +
143 + d i s c r e t i z a t i o n _ w e i g h t = self . _ l i n e a r _ s c h e d u l e (
144 + global_step , start =0.0 , end = self . hypers . d i s c r e t i z a t i o n _ w e i g h t
145 + )
146 +
147 + # Cosine a n n e a l i n g for half - integer loss .
148 + c y c l e _ l e n g t h = self . config . t r a i n i n g _ s t e p s // 4 # Number of steps per
cycle
149 + c y c l e _ p r o g r e s s = (
150 + g l o b a l _ s t e p % c y c l e _ l e n g t h
151 + ) / c y c l e _ l e n g t h # N o r m a l i z e d p ro gr es s within the current cycle [0 ,
1)
152 + h a l f _ i n t _ m u l t i p l i e r = (1 + jnp . cos ( jnp . pi * c y c l e _ p r o g r e s s ) ) / 2
153 + h a l f _ i n t _ m u l t i p l i e r = (
154 + 1 - self . hypers . h a l f _ i n t _ s t a r t
155 + ) * h a l f _ i n t _ m u l t i p l i e r + self . hypers . h a l f _ i n t _ s t a r t
156 +
157 + t o t a l _ l o s s = (
158 + re c_ lo ss
159 + + d i s c r e t i z a t i o n _ w e i g h t * d i s c r e t i z a t i o n _ l o s s *
h a l f _ i n t _ m u l t i p l i e r
160 + )
161 +
162 + # Add penalty for large values ( s t a b i l i t y ) .
163 + l a r g e _ v a l u e _ p e n a l t y = 0.0
164 + for factor in d e c o m p o s i t i o n :
165 + l a r g e _ v a l u e _ p e n a l t y += jnp . mean ( jnp . abs ( factor ) ** 2)
166 + l a r g e _ v a l u e _ p e n a l t y /= len ( d e c o m p o s i t i o n )
167 + t o t a l _ l o s s += self . hypers . l a r g e _ v a l u e _ p e n a l t y _ w e i g h t *
l a r g e _ v a l u e _ p e n a l t y
168 +
169 + return jnp . real ( t o t a l _ l o s s )
170 +
171
172 def l 2 _ l o s s _ c o m p l e x ( x : jnp . ndarray , y : jnp . ndarray ) -> jnp . ndarray :
173 """ E l e m e n t w i s e L2 loss for c o m p l e x n u m b e r s . """
174 @ @ -117 ,6 +255 ,18 @@
175 r e t u r n hyper . zipit ([
176 - hyper . uniform ( ' i n i t _ s c a l e', hyper . i nt er va l (0.2 , 1.5) ) ,
177 - hyper . uniform ( ' l e a r n i n g _ r a t e', hyper . i nt er va l (0.05 , 0.3) ) ,
178 + hyper . uniform ( ' i n i t _ s c a l e', hyper . i nt er va l (0.1 , 1.0) ) ,
179 + hyper . uniform ( ' l e a r n i n g _ r a t e', hyper . i nt er va l (0.01 , 0.2) ) ,
180 + hyper . uniform ( ' d i s c r e t i z a t i o n _ w e i g h t', hyper . i nt er va l (0.0 , 0.1) ) ,
181 + hyper . uniform ( ' h a l l u c i n a t i o n _ p r o b', hyper . i nt er va l (0.0 , 0.2) ) ,
182 + hyper . uniform ( ' h a l l u c i n a t i o n _ s c a l e', hyper . i nt er va l (0.0 , 0.2) ) ,
183 + hyper . uniform ( ' n o i s e _ s t d', hyper . i nt er va l (0.0 , 0.01) ) ,
184 + hyper . uniform ( ' t a r g e t _ n o i s e _ s t d', hyper . i nt er va l (0.0 , 0.01) ) ,
185 + hyper . uniform ( ' w e i g h t _ d e c a y', hyper . i nt er va l (0.00001 , 0.001) ) ,
186 + hyper . uniform ( ' c li p_ mi n', hyper . i nt er va l (0.0 , 0.5) ) ,
187 + hyper . uniform ( ' c li p_ ma x', hyper . i nt er va l (1.0 , 3.0) ) ,
188 + hyper . uniform ( ' l a r g e _ v a l u e _ p e n a l t y _ w e i g h t', hyper . i nt er va l (0.0 ,
0.01) ) ,
189 + # Add noise to the g ra di en t to aid in e x p l o r a t i o n .
190 + hyper . uniform ( ' g r a d _ n o i s e _ s t d', hyper . i nt er va l (0.0 , 0.001) ) ,
191 + hyper . uniform ( ' h a l f _ i n t _ s t a r t', hyper . i nt er va l (0.0 , 1.0) ) ,
192 ])
193 # EVOLVE - BLOCK - END
```

图 9c|图 4（左）的放大版，给出发现更快 4×4 矩阵乘法算法的程序（3/3）。这里 hyper 是一个由用户提供的、用于生成超参数扫描的库。

## B. AlphaEvolve 数学发现的细节

本节报告的所有构造的数据与验证代码均见配套 Google Colab。

### B.1. 第一自相关不等式

对任意函数 f : ℝ → ℝ，定义 f 的自卷积（autoconvolution）为

  f∗f(t) := ∫_ℝ f(t−x) f(x) dx。

令 C₁ 为满足下式的最大常数

  max_{−1/2≤t≤1/2} f∗f(t) ≥ C₁ (∫_{−1/4}^{1/4} f(x) dx)²　　(1)

对所有非负 f : ℝ → ℝ 成立。该问题源自加性组合学，与 Sidon 集的大小相关。目前已知

  1.28 ≤ C₁ ≤ 1.5098，

其中下界由 [17] 取得，上界由 [70] 通过阶梯函数（step function）构造取得。AlphaEvolve 找到了一个在 [−1/4, 1/4] 上有 600 个等距区间的阶梯函数，给出略好的上界 C₁ ≤ 1.5053。

### B.2. 第二自相关不等式

令 C₂ 为使

  ‖f∗f‖₂² ≤ C₂ · ‖f∗f‖₁ · ‖f∗f‖∞

对所有非负 f : ℝ → ℝ 成立的最小常数。已知

  0.88922 ≤ C₂ ≤ 1，

其中下界来自一个阶梯函数构造 [70]。AlphaEvolve 找到了一个在 [−1/4, 1/4] 上有 50 个等距区间的阶梯函数，给出略好的下界 0.8962 ≤ C₂。

### B.3. 第三自相关不等式

令 C₃ 为满足下式的最大常数

  max_{−1/2≤t≤1/2} |f∗f(t)| ≥ C₃ (∫_{−1/4}^{1/4} f(x) dx)²

对任意函数 f : ℝ → ℝ 成立。显然 C₃ ≤ C₁，因为我们现在允许 f 取正值与负值。存在一个给出上界 C₃ ≤ 1.45810 的阶梯函数 [104, 第 75 页]。AlphaEvolve 找到了一个在 [−1/4, 1/4] 上有 400 个等距区间的阶梯函数，给出略好的上界 C₃ ≤ 1.4557。

### B.4. 一个不确定性不等式

给定函数 f : ℝ → ℝ，定义傅里叶变换 f̂(ξ) := ∫_ℝ f(x) e^{−2πixξ} dx 以及

  A(f) := inf{r > 0 : 对所有 |x| ≥ r 有 f(x) ≥ 0}。

令 C₄ 为使

  A(f) · A(f̂) ≥ C₄

对所有满足 max(f(0), f̂(0)) < 0 的偶函数 f 成立的最大常数。已知 [33]

  0.2025 ≤ C₄ ≤ 0.3523。

（上界在该论文中写作 0.353，但把他们的解舍入到第四位数字得 0.3523。）我们用与 [33] 类似的线性组合、但采用由 AlphaEvolve 找到的精化常数，把上界改进为 C₄ ≤ 0.3521。

为获得 C₄ 的上界，人们构造一个满足条件的特定「测试函数」f，并为该函数计算值 A(f) · A(f̂)，从而给出上界 C₄ ≤ A(f) · A(f̂)。沿用 [33] 的方法，测试函数以下列形式寻找：f(x) = P(x) e^{−πx²}，其中 P(x) 是作为 Hermite 多项式 H₄ₖ(x) 之线性组合构造的偶多项式。这一形式特别有用，因为 Hₙ(x) e^{−πx²} 的傅里叶变换是 iⁿ Hₙ(ξ) e^{−πξ²}。对偶多项式 P(x) = Σₖ c₄ₖ H₄ₖ(x)，f(x) 的傅里叶变换为 f̂(ξ) = Σₖ c₄ₖ i⁴ᵏ H₄ₖ(ξ) e^{−πξ²} = (Σₖ c₄ₖ H₄ₖ(ξ)) e^{−πξ²} = P(ξ) e^{−πξ²}。于是，A(f) 与 P(x) 的最大正根相关，A(f̂) 与 P(ξ) 的最大正根相关。具体而言，若对充分大的 |x| 有 P(x) ≥ 0，则 A(f) 是 P(x) 的最大正根，A(f̂) 是 P(ξ) 的最大正根，从而蕴含 A(f) = A(f̂)。不等式变为 C₄ ≤ (A(f))²。该方法涉及为多项式 P(x) = c₀H₀(x) + c₁H₄(x) + c₂H₈(x) + … 寻找系数 c₀, c₁, c₂, …，使 P(x) 满足特定约束（与 f(0) < 0、f̂(0) < 0 以及对充分大的 |x| 取正值相关），并最小化 P(x) 的最大正根。在我们的方法中，构造多项式 P(x) 使 P(0) = 0（优化过程中为简化约束而使用的条件），这意味着 P(x) 有一个 x² 因子。P(x) 的最大正根 r_max 即为 P(x)/x² 的最大正根。由这一构造导出的 C₄ 上界为 r_max²/(2π)。

AlphaEvolve 为 P(x) = c₀H₀(x) + c₁H₄(x) + c₂H₈(x) 找到的精化常数为 [c₀, c₁, c₂] ≈ [0.32925, −0.01159, −8.9216×10⁻⁵]。用这些系数构造 P(x)、求其最大正根 r_max（通过求 P(x)/x² 的最大正根）并计算 r_max²/(2π)，得到改进的上界 C₄ ≤ 0.3521。定性地看，我们的线性组合与 [33] 中找到的非常相似，从而经验性地证实了他们关于该构造接近最优的假设。

注：在本手稿第一版发布之后，Henry Cohn 指出，他们在近期一篇论文 [18] 中用了类似但更精化的方法得到更好的常数 0.3284。把他们的精化方法纳入 AlphaEvolve 后，我们把所报告的常数进一步改进到 0.3216。细节参见配套 Google Colab。

0.2
 0.1
 0.0 0.1 0.2
0.0
0.2
0.4
0.6
0.8
1.0

图 10|AlphaEvolve 为 Erdős 最小重叠问题找到的构造。

### B.5. Erdős 最小重叠问题

令 C₅ 为使

  sup_{x∈[−2,2]} ∫_{−1}^{1} f(t) g(x+t) dt ≥ C₅

对所有非负 f, g : [−1, 1] → [0, 1] 成立的最大常数，其中 f + g = 1 在 [−1, 1] 上且 ∫ f = 1（f、g 在 [−1, 1] 之外以零延拓）。该常数控制 [25] 中最小重叠问题的渐近性。已知界为

  0.379005 ≤ C₅ ≤ 0.380927，

其中下界由 [107] 通过凸规划方法取得。已知（见 [40]）该常数等于在 [0, 2] 上取值于 [0, 1] 且满足 ∫₀² h(x) dx = 1 的所有阶梯函数 h 上，表达式

  max_k ∫ h(x)(1 − h(x+k)) dx

的下确界。Erdős 最小重叠问题的上界随后正是利用这一结果、由 [40] 以阶梯函数构造取得的。图 10 所描绘的阶梯函数较此前界略好，给出上界 C₅ ≤ 0.380924。

### B.6. 有限集的和与差

令 C₆ 为使以下陈述成立的最大常数：存在任意大的有限整数集 A、B，满足 |A+B| ≪ |A| 且 |A−B| ≫ |A+B|^{C₆}。（这里 A+B = {a+b : a∈A, b∈B} 与 A−B = {a−b : a∈A, b∈B} 分别表示和集与差集。记号 X ≪ Y 表示：存在与集合 A、B 无关的常数 C（对充分大的集合 A、B），使 X ≤ CY。记号 X ≫ Y 表示：存在与集合 A、B 无关的正常数 C′（对充分大的集合 A、B），使 X ≥ C′Y。）

  1.14465 ≤ C₆ ≤ 4/3；　　(2)

上界见 [39, Corollary 3]，下界见 [39, Theorem 1]。下界的主要工具是 Gyarmati et al. [39] 的以下结果：对任意包含零且满足 |U−U| ≤ 2 max(U) + 1 的非负整数有限集 U，

  C₆ ≥ 1 + log(|U−U| / |U+U|) / log(2 max(U) + 1)。　　(3)

AlphaEvolve 找到了大小为 2003 的集合 U₁，把下界改进为 1.1479 ≤ C₆；又找到了大小为 54265 的集合 U₂，进一步把下界改进为 1.1584 ≤ C₆。

### B.7. 在正六边形内堆积单位正六边形

考虑把 n 个边长为单位长度的互不相交正六边形装入一个更大的正六边形、并最小化外部六边形边长的问题。对 n = 11 与 n = 12，已知最好的构造使用的外六边形边长分别为 3.943 与 4.0 [29]。AlphaEvolve 找到了把这些界分别改进到 3.931 与 3.942 的堆积安排。这些安排展示于图 11。

### B.8. 最小化最大距离与最小距离之比

对任意 n 与 d，该问题的目标是在 d 维空间中放置 n 个点，使两两距离的最大值与最小值之比最小化。AlphaEvolve 找到了两个改进已知最好界的新构造。所找到的构造展示于图 12。

在 2 维中，AlphaEvolve 找到了 16 个点，比值 ≈ √12.889266112，改进了 √12.890 的已知最好界 [29]。（该参考文献中报告的是比值的平方而非比值本身，我们沿用同一惯例。）

在 3 维中，AlphaEvolve 找到了 14 个点，比值 ≈ √4.165849767，改进了 √4.168 的已知最好界 [29]。

### B.9. 三角形的 Heilbronn 问题

该问题的目标是在一个单位面积三角形之上或之内放置 n 个点，使由这些点形成的最小三角形的面积最大化。对 n = 11，SOTA 为 0.036 [29]，而 AlphaEvolve 找到了最小面积大于 0.0365 的构造，展示于图 13（左）。

### B.10. 凸区域的 Heilbronn 问题

该问题的目标是在一个单位面积凸区域之上或之内放置 n 个点，使由这些点形成的最小三角形的面积最大化。AlphaEvolve 改进了两个已知最好界。

对 n = 13，SOTA 为 0.0306 [29]，AlphaEvolve 把它改进到 0.0309（见图 13（中））。对 n = 14，SOTA 为 0.0277 [29]，AlphaEvolve 把它改进到 0.0278（见图 13（右））。

### B.11. 11 维的 kissing number

kissing 问题问的是：有多少个互不相交的单位球可以相切地堆积到一个给定单位球的周围。d 维中这一最大数称为 d 维 kissing number [8]。对 d = 11，已知最好的下界为 592 [31]，而 AlphaEvolve 把它改进到了 593。为证明 11 维 kissing number 的 593 下界，AlphaEvolve 找到了 593 个具有整数坐标的 11 维非零点，使这些点的最大范数小于它们的最小两两距离。根据以下引理，这蕴含 11 维的 kissing number 至少为 593。

**引理 1.** 设 C ⊂ ℝ^d 为满足 0 ∉ C 且

  min{∥x−y∥ : x ≠ y ∈ C} ≥ max{∥x∥ : x ∈ C}

的点集。则以 {2x/∥x∥ : x ∈ C} 为中心的单位球构成 d 维的一个有效 kissing 构型。特别地，d 维的 kissing number 至少为 |C|。

**证明.** 对任意 x ≠ y ∈ C，不等式 ∥x−y∥² ≥ max{∥x∥², ∥y∥²} 蕴含

  2⟨x,y⟩ ≤ ∥x∥² + ∥y∥² − max{∥x∥², ∥y∥²} = min{∥x∥², ∥y∥²} ≤ ∥x∥·∥y∥，　　(4)

其中最后一步不等式成立，是因为两个正数的最小值小于或等于它们的几何平均。点 {2x/∥x∥ : x ∈ C} 的范数为 2，故以其为中心的单位球与以原点为中心的单位球相切。剩下要证明这些球互不重叠。这等价于证明，对所有 x ≠ y ∈ C，

  ∥2x/∥x∥ − 2y/∥y∥∥ ≥ 2。

化简后，它等价于 2⟨x,y⟩ ≤ ∥x∥·∥y∥，而这就是我们在 (4) 中已证的不等式。于是，以 {2x/∥x∥ : x ∈ C} 为中心的单位球构成 d 维的一个有效 kissing 构型，得证。□

### B.12. 在单位正方形内堆积圆以最大化半径之和

给定正整数 n，问题是把 n 个互不相交的圆装入单位正方形，使其半径之和最大化。AlphaEvolve 找到了两个改进现有技术 [29] 的新构造。

对 n = 26，SOTA 为 2.634，AlphaEvolve 把它改进到 2.635；见图 14（左）。对 n = 32，SOTA 为 2.936，AlphaEvolve 把它改进到 2.937；见图 14（中）。

### B.13. 在周长为 4 的矩形内堆积圆以最大化半径之和

给定正整数 n，问题是把 n 个互不相交的圆装入一个周长为 4 的矩形，使其半径之和最大化。AlphaEvolve 为 n = 21 找到了一个新构造，把现有技术从 2.364 [29] 改进到 2.3658；见图 14（右）。

图 11|AlphaEvolve 找到的堆积问题构造。左：把 11 个单位六边形装入边长为 3.931 的正六边形。右：把 12 个单位六边形装入边长为 3.942 的正六边形。

图 12|左：2 维中的 16 个点，最大距离与最小距离之比 ≈ √12.889266112。右：3 维中的 14 个点，比值 ≈ √4.165849767。两个构造均改进了已知最好界。

图 13|AlphaEvolve 找到的、改进 Heilbronn 问题两个变体已知最好界的新构造。左：单位面积三角形中的 11 个点，所有形成的三角形面积 ≥ 0.0365。中：单位面积凸区域内的 13 个点，所有形成的三角形面积 ≥ 0.0309。右：单位凸区域内的 14 个点，最小面积 ≥ 0.0278。

图 14|AlphaEvolve 找到的、改进堆积圆以最大化半径之和的已知最好界的新构造。左：单位正方形中的 26 个圆，半径之和 ≥ 2.635。中：单位正方形中的 32 个圆，半径之和 ≥ 2.937。右：周长为 4 的矩形中的 21 个圆，半径之和 ≥ 2.365。

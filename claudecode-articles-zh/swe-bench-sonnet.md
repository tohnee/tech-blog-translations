---
title: "用 Claude 3.5 Sonnet 刷新 SWE-bench Verified 纪录"
title_en: "Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet"
source: https://www.anthropic.com/engineering/swe-bench-sonnet
published: 2025-01-06
crawled: 2026-09-11
translated: 2026-09-11
---

# 用 Claude 3.5 Sonnet 刷新 SWE-bench Verified 纪录

> 原文：[Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet) · Anthropic Engineering Blog

*我们最新的升级版 [Claude 3.5 Sonnet](https://www.anthropic.com/news/3-5-models-and-computer-use) 在软件工程评估 SWE-bench Verified 上取得 49% 的成绩，超过此前最先进模型的 45%。本文解释我们围绕该模型构建的「智能体」，旨在帮助开发者从 Claude 3.5 Sonnet 获得尽可能好的表现。*

[SWE-bench](https://www.swebench.com/) 是一项评估模型完成真实软件工程任务能力的 AI 评估基准。具体来说，它测试模型解决热门开源 Python 仓库 GitHub issue 的能力。基准中的每个任务都会给 AI 模型一个配置好的 Python 环境和该仓库在 issue 被解决之前那一刻的 checkout（本地工作副本）。模型需要理解、修改并测试代码，然后提交它提出的解决方案。

每个方案都会对照关闭原 GitHub issue 的那个 pull request 中的真实单元测试来评分。这检验的是 AI 模型能否实现与原 PR 人类作者相同的功能。

SWE-bench 评估的不是孤立的 AI 模型，而是整个「智能体」系统。在这里，「智能体」指 AI 模型与其周围软件脚手架（scaffolding）的组合。脚手架负责生成送入模型的提示、解析模型输出以采取行动，并管理交互循环——把模型上一步行动的结果纳入它的下一个提示。在 SWE-bench 上，即使底层 AI 模型相同，智能体的表现也会因脚手架不同而产生显著差异。

大语言模型编码能力还有许多其他基准，但 SWE-bench 因以下几个原因日益流行：

1. 它使用来自真实项目的真实工程任务，而不是竞赛或面试风格的问题；
2. 它尚未饱和——还有很大的提升空间。目前还没有模型在 SWE-bench Verified 上跨过 50% 的完成线（截至撰写本文时，升级版 Claude 3.5 Sonnet 为 49%）；
3. 它衡量的是整个「智能体」，而非孤立的模型。开源开发者和初创公司通过优化脚手架，已经成功地让同一个模型的表现大幅提升。

需要注意的是，原始 SWE-bench 数据集包含一些没有 GitHub issue 之外的额外上下文（例如需要返回的特定错误信息）就无法解决的任务。[SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) 是 SWE-bench 中经过人工审核、确认可解的 500 题子集，因此是衡量编程智能体表现最清晰的指标。本文所指的正是这个基准。

## 达到最先进水平

### 使用工具的智能体

我们在为升级版 Claude 3.5 Sonnet 设计智能体脚手架时的理念是：尽可能多地把控制权交给语言模型本身，让脚手架保持极简。这个智能体有一个提示、一个执行 bash 命令的 Bash 工具，以及一个查看和编辑文件与目录的编辑工具（Edit Tool）。我们会持续采样，直到模型自认为完成或超出其 200k 上下文长度。这种脚手架让模型能够用自己的判断决定如何推进问题，而不是被硬编码进某个特定模式或工作流。

提示为模型概述了一个建议的做法，但对于这个任务而言并不算太长或过于细节。模型可以自由选择如何从一个步骤走到下一个步骤，而不是被严格的、离散的步骤切换所束缚。如果你对 token 不敏感，显式鼓励模型生成长回答会有帮助。

下面的代码是我们的智能体脚手架使用的提示：

```
<uploaded_files>
{location}
</uploaded_files>
I've uploaded a python code repository in the directory {location} (not in /tmp/inputs). Consider the following PR description:

<pr_description>
{pr_description}
</pr_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <pr_description> are met?
I've already taken care of all changes to any of the test files described in the <pr_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!

Your task is to make the minimal changes to non-tests files in the {location} directory to ensure the <pr_description> is satisfied.

Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo to familiarize yourself with its structure.
2. Create a script to reproduce the error and execute it with `python <filename.py>` using the BashTool, to confirm the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed!
5. Think about edgecases and make sure your fix handles them as well

Your thinking should be thorough and so it's fine if it's very long.
```

模型的第一个工具执行 Bash 命令。它的 schema 很简单，只接收要在环境中运行的命令。不过，这个工具的描述分量更重：其中包含给模型的更详细指令，包括输入转义、无法访问互联网，以及如何在后台运行命令。

下面是 Bash 工具的规格：

```
{
   "name": "bash",
   "description": "Run commands in a bash shell\n
* When invoking this tool, the contents of the \"command\" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* State is persistent across command calls and discussions with the user.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "description": "The bash command to run."
           }
       },
       "required": ["command"]
   }
}
```

模型的第二个工具（编辑工具）复杂得多，包含了模型查看、创建和编辑文件所需的一切。同样，我们的工具描述中包含关于如何使用该工具的详细信息。

我们为各种智能体任务投入了大量精力打磨这些工具的描述和规格。我们通过测试找出模型可能误解规格之处，以及使用这些工具可能踩到的坑，然后修改描述以预防这些问题。我们认为，为模型设计工具接口应当获得远比现在更多的关注——正如为人类设计工具接口已经投入了大量关注一样。

下面的代码是我们编辑工具的描述：

```
{
   "name": "str_replace_editor",
   "description": "Custom editing tool for viewing, creating and editing files\n
* State is persistent across command calls and discussions with the user\n
* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep\n
* The `create` command cannot be used if the specified `path` already exists as a file\n
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>` \n
* The `undo_edit` command will revert the last edit made to the file at `path`\n

Notes for using the `str_replace` command:\n
* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!\n
* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique\n
* The `new_str` parameter should contain the edited lines that should replace the `old_str`",
...
```

我们提升表现的一个手段是给工具做「防错」设计。例如，当智能体离开根目录后，模型有时会弄错相对文件路径。为防止这一点，我们干脆让工具始终要求绝对路径。

我们针对「如何指定对现有文件的编辑」试验了几种不同策略，其中字符串替换的可靠性最高：模型指定 `old_str`，在给定文件中替换为 `new_str`。只有当 `old_str` 恰好匹配一处时替换才会执行；匹配多于或少于一处时，模型会收到相应的错误信息以便重试。

编辑工具的规格如下所示：

```
...
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
               "description": "The commands to run. Allowed options are: `view`, `create`, `str_replace`, `insert`, `undo_edit`."
           },
           "file_text": {
               "description": "Required parameter of `create` command, with the content of the file to be created.",
               "type": "string"
           },
           "insert_line": {
               "description": "Required parameter of `insert` command. The `new_str` will be inserted AFTER the line `insert_line` of `path`.",
               "type": "integer"
           },
           "new_str": {
               "description": "Required parameter of `str_replace` command containing the new string. Required parameter of `insert` command containing the string to insert.",
               "type": "string"
           },
           "old_str": {
               "description": "Required parameter of `str_replace` command containing the string in `path` to replace.",
               "type": "string"
           },
           "path": {
               "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
               "type": "string"
           },
           "view_range": {
               "description": "Optional parameter of `view` command when `path` points to a file. If none is given, the full file is shown. If provided, the file will be shown in the indicated line number range, e.g. [11, 12] will show lines 11 and 12. Indexing at 1 to start. Setting `[start_line, -1]` shows all lines from `start_line` to the end of the file.",
               "items": {
                   "type": "integer"
               },
               "type": "array"
           }
       },
       "required": ["command", "path"]
   }
}
```

## 结果

总体而言，升级版 Claude 3.5 Sonnet 在推理、编码和数学能力上都高于我们之前的模型以及[此前最先进](https://solverai.com/)的模型。它还展现出更强的智能体能力：工具和脚手架帮助把这些改进的能力用到极致。

| 模型 | **Claude 3.5 Sonnet（新）** | 此前 SOTA | Claude 3.5 Sonnet（旧） | Claude 3 Opus |
| --- | --- | --- | --- | --- |
| SWE-bench Verified 得分 | 49% | 45% | 33% | 22% |

我们部分模型在 SWE-bench Verified 上的得分，全部使用本文的智能体脚手架。

## 智能体行为示例

跑这个基准时，我们以 [SWE-Agent](https://swe-agent.com/) 框架作为智能体代码的基础。在下面的日志中，我们把智能体的文本输出、工具调用和工具响应分别渲染为 THOUGHT、ACTION 和 OBSERVATION，尽管我们并不强制模型遵循固定顺序。

下面的代码块将带你走一遍 Claude 3.5 Sonnet 解答 SWE-bench 问题的典型过程。

第一个代码块是给模型的初始提示的一部分，其中 `{pr_description}` 填入了来自 SWE-bench 任务的真实值。重要的是，这个任务包含复现问题的步骤，这给了模型一个有价值的调查起点。

```
<uploaded_files>
/repo
</uploaded_files>
I've uploaded a python code repository in the directory /repo (not in /tmp/inputs). Consider the following PR description:

<pr_description>
linear_model.RidgeClassifierCV's Parameter store_cv_values issue
#### Description
Parameter store_cv_values error on sklearn.linear_model.RidgeClassifierCV

#### Steps/Code to Reproduce
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, 
                                         store_cv_values = True).fit(x, y)

#### Expected Results
Expected to get the usual ridge regression model output, keeping the cross validation predictions as attribute.

#### Actual Results
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'

lm.RidgeClassifierCV actually has no parameter store_cv_values, even though some attributes depends on it.
```

模型做出响应，首先用编辑工具查看仓库结构。你可以在 THOUGHT 和 ACTION 下看到模型的文本输出和工具调用参数，在 OBSERVATION 下看到工具输出的一部分：

```
THOUGHT:
I'll help you implement the changes to satisfy the PR description. Let's follow the steps you outlined.

1. First, let's explore the repo structure:
ACTION (str_replace_editor):
command:
view

path:
/repo

OBSERVATION:
Here's the files and directories up to 2 levels deep in /repo, excluding hidden items:
/repo
/repo/PULL_REQUEST_TEMPLATE.md
/repo/ISSUE_TEMPLATE.md
/repo/sklearn
/repo/sklearn/decomposition
/repo/sklearn/kernel_ridge.py
/repo/sklearn/model_selection
/repo/sklearn/covariance
/repo/sklearn/cluster
/repo/sklearn/base.py
/repo/sklearn/dummy.py
/repo/sklearn/naive_bayes.py
...
```

现在模型对仓库结构有了更好的了解，它用编辑工具创建一个新脚本，用于复现问题并验证修复：

```
THOUGHT:
Based on the repository structure, we'll need to modify the Ridge Classifier in the `sklearn/linear_model` directory.

Let's create a script to reproduce the error:
ACTION (str_replace_editor):
command:
create

path:
/repo/reproduce_error.py

file_text:
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, 
                         store_cv_values=True).fit(x, y)

OBSERVATION:
File created successfully at: /repo/reproduce_error.py
```

接着模型用 Bash 工具执行它写的脚本，成功复现了任务中的问题：

```
THOUGHT:
Let's verify that we can reproduce the error:
ACTION (bash):
command:
python3 /repo/reproduce_error.py

OBSERVATION:
Traceback (most recent call last):
  File "/repo/reproduce_error.py", line 10, in <module>
    store_cv_values=True).fit(x, y)
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
```

从这里开始，模型用编辑工具修改仓库的源代码，并重新运行脚本来验证改动是否解决了问题：

```
THOUGHT:
The error is reproducible. Looking at the code, I can see that the issue is that while the `RidgeClassifierCV` class inherits from `_BaseRidgeCV`, it fails to pass the `store_cv_values` parameter from its constructor through to the base class constructor.

Let's fix this:
ACTION (str_replace_editor):
command:
str_replace

path:
/repo/sklearn/linear_model/ridge.py

old_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv)
        self.class_weight = class_weight

new_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None,
                 store_cv_values=False):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv, store_cv_values=store_cv_values)
        self.class_weight = class_weight
```

在这个具体例子里，模型工作了 12 步才决定可以提交。任务的测试随后成功运行，验证了模型的方案确实解决了问题。有些任务模型提交前花了超过 100 轮；在另一些任务中，模型一直尝试直到上下文耗尽。

对比升级版 Claude 3.5 Sonnet 与更早模型的尝试记录，升级版 3.5 Sonnet 更常自我纠正，还表现出尝试多种不同方案的能力，而不是反复卡在同一个错误上。

## 挑战

SWE-bench Verified 是一个强大的评估基准，但运行起来比简单的单轮评估更复杂。以下是我们在使用它时遇到的一些挑战——其他 AI 开发者可能也会遇到。

1. **耗时长、token 成本高。** 上面的例子来自一个 12 步就成功完成的案例。但许多成功的运行需要数百轮才解决，消耗超过 10 万 token。升级版 Claude 3.5 Sonnet 非常坚韧：只要有足够时间，它往往能找到绕过问题的办法，但这可能很贵；
2. **评分。** 在检查失败任务时，我们发现有些案例模型行为正确，却因环境配置问题或 install 补丁被应用两次等问题而失败。解决这类系统问题对于准确刻画 AI 智能体的表现至关重要。
3. **隐藏测试。** 由于模型看不到用于评分的测试，它常常在任务实际失败时「以为」自己成功了。其中一些失败是因为模型在错误的抽象层级上解决了问题（打了个补丁而不是更深入的重构）。另一些失败则显得不太公平：它们解决了问题，却与原任务的单元测试不匹配。
4. **多模态。** 尽管升级版 Claude 3.5 Sonnet 具备出色的视觉和多模态能力，我们没有实现让它查看保存到文件系统或以 URL 引用的文件的途径。这使得某些任务（尤其是来自 Matplotlib 的任务）的调试格外困难，也容易出现模型幻觉。这里显然有等着开发者去摘的低垂果实——SWE-bench 也已推出一个新的[聚焦多模态任务的评估](https://www.swebench.com/multimodal.html)。我们期待不久的将来看到开发者用 Claude 在这个评估上取得更高分数。

升级版 Claude 3.5 Sonnet 用一个简单的提示和两个通用工具在 SWE-bench Verified 上取得了 49%，超过了此前最先进的 45%。我们相信，使用新 Claude 3.5 Sonnet 构建的开发者会很快找到比我们这里初步展示的更好的新方法来提升 SWE-bench 分数。

## 致谢

Erik Schluntz 优化了 SWE-bench 智能体并撰写本文。Simon Biggs、Dawn Drain 和 Eric Christiansen 协助实现了基准。Shauna Kravec、Dawn Drain、Felipe Rosso、Nova DasSarma、Ven Chandrasekaran 以及许多其他同事为训练 Claude 3.5 Sonnet 精通智能体编码做出了贡献。

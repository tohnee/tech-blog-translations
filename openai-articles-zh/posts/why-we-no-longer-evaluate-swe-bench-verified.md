---
title: "为什么 SWE-bench Verified 不再衡量前沿编程能力"
title_en: "Why SWE-bench Verified no longer measures frontier coding capabilities"
source: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
crawled: 2026-09-13
category: research
translated: 2026-09-13
---

# 为什么 SWE-bench Verified 不再衡量前沿编程能力

> 原文：[Why SWE-bench Verified no longer measures frontier coding capabilities](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) · OpenAI 博客

自我们于 2024 年 8 月首次发布 [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) 以来，业界广泛使用它来衡量模型在自主软件工程任务上的进展。发布之后，SWE-bench Verified 提供了能力进展的有力信号，并成为前沿模型发布报告中的一项标准指标。跟踪和预测这些能力的进展也是 OpenAI [Preparedness 框架](https://openai.com/index/updating-our-preparedness-framework/)的重要组成部分。在最初创建 Verified 基准时，我们曾尝试解决原版评估中导致 [SWE-bench 数据集](https://arxiv.org/abs/2310.06770)里某些任务无法完成的问题。

在最初的跃升之后，SWE-bench Verified 上的最先进成绩增长已经放缓，过去 6 个月仅[从 74.9% 提升到 80.9%](https://llm-stats.com/benchmarks/swe-bench-verified)。这引出了一个问题：剩余的失败究竟反映了模型的局限，还是数据集本身的特性？

在一项新的分析中，我们发现了 Verified 集合的两个重大问题，表明在今天的性能水平下，这一基准已不再适合用于衡量前沿模型发布中自主软件工程能力的进展：

1. **测试会拒绝正确的解法：**我们审计了数据集中模型经常无法解决的 27.6% 子集，发现被审计问题中至少 59.4% 存在有缺陷的测试用例，会把功能正确的提交判为失败——尽管我们在最初创建 SWE-bench Verified 时已为此尽了最大努力。
2. **在解法上训练：**由于大型前沿模型能从训练中习得信息，绝不能让它们在被评估的问题和解法上进行训练，这一点至关重要。这好比在考试之前把试题和答案提前透露给学生——他们未必会背答案，但见过答案的学生肯定比没见过的考得好。SWE-bench 的问题取材于许多模型提供商用于训练的开源代码库。在分析中我们发现，我们测试的所有前沿模型都能够复现作为标准参考的、由人类编写的原始 bug 修复（即 gold patch），或者逐字复现某些任务的题目描述细节，这表明它们在训练中都至少见过其中一部分问题和解法。

**我们还发现了证据表明，在训练中见过这些问题的模型更容易成功，因为它们拥有通过那些规定不充分的测试所需的额外信息。**

这意味着 SWE-bench Verified 上的进步不再反映模型真实世界软件开发能力的有意义的提升，而是越来越多地反映模型在训练时接触该基准的程度。这正是我们停止报告 SWE-bench Verified 分数的原因，我们也建议其他模型开发者这样做。

我们正在构建新的、未被污染的评测，以更好地跟踪编程能力；我们认为这也是更广泛的研究社区应当重点关注的一个领域。在此之前，OpenAI 建议报告 SWE-bench Pro 的结果。

## 背景

原版 [SWE-bench](https://arxiv.org/abs/2310.06770) 评估于 2023 年发布。每个问题取自 12 个开源 Python 代码库之一中一个已解决的 GitHub issue，并与对应的 pull request（PR）配对。为了判定模型生成的代码改动是否正确，每个问题附带两组测试：

- 在未修改的代码库上失败、但若 issue 被正确修复则会通过的测试
- 在修复前后都应通过的回归测试，用于确保无关功能保持完好

模型看不到这些测试。它只能依据原始 issue 文本和修复前的代码库状态来产出代码改动。只有当代码改动应用后所有测试都通过，它才算通过该问题。

我们发现原评估存在许多问题，可能导致模型能力被低估。

- 一些单元测试过于具体或与任务不匹配，导致正确的修复可能被拒绝。
- 许多任务描述规定不充分，可能产生多种有效解读——而测试只覆盖其中特定的一种。
- 取决于环境的配置（例如 Linux 还是 Windows，或 Python 版本），一些测试可能会虚假地失败

我们在 2024 年创建了 [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) 来解决这些问题。我们与资深软件工程师合作，审查了 1,699 道 SWE-bench 问题，过滤掉存在上述问题的问题。每个问题由三位专家独立审查。这一审查过程最终产生了 SWE-bench Verified——一个精选的 500 道问题的集合。

## 过窄与过宽的测试

虽然 SWE-bench Verified 相比初版已是巨大改进，但残留问题依然存在。我们对 138 道 OpenAI o3 在 64 次独立运行中未能稳定解决的 SWE-bench Verified 问题进行了审计。每个案例由至少六位经验丰富的软件工程师独立审查。如果有专家标记了问题，还会由另一个团队复核。

我们发现，138 道问题中有 59.4% 在测试设计和/或题目描述上存在实质性缺陷，使得即使是最强大的模型或人类也极难甚至无法解决。

- 被审计任务中有 35.5% 存在强制特定实现细节的严格测试用例，使许多功能正确的提交失效，我们称之为*过窄测试用例*（narrow test cases）。
- 被审计任务中有 18.8% 的测试检查了题目描述中未指明的额外功能，我们称之为*过宽测试用例*（wide test cases）。
- 其余 5.1% 的任务存在难以归入这一分类法的杂项问题。

第一种失败模式的一个典型例子是 [pylint-dev__pylint-4551](https://github.com/pylint-dev/pylint/pull/4551)，其中 PR 引入了一个新函数 `get_annotation`，作为整体解决方案的一部分。这个函数名在题目描述中没有提到，却被测试直接导入。虽然有些模型可能会直觉性地创建这样一个函数，但要正确解决这个问题，并不必须实现一个具有这个特定名称的函数。许多有效的解法都因导入错误而未通过测试。

#### 题目描述

#### Plain Text

```
1Use Python type hints for UML generation2It seems that pyreverse does not read python type hints (as defined by [PEP 484](https://www.python.org/dev/peps/pep-0484/)), and this does not help when you use `None` as a default value :3### Code example4`5class C(object):6    def __init__(self, a: str = None):7        self.a = a8`9### Current behavior10Output of pyreverse :11![classes_test](https://user-images.githubusercontent.com/22218701/27432305-f10fe03e-574f-11e7-81fa-e2b59e493360.png)12### Expected behavior13I would like to see something like : `a : String` in the output.14### pylint --version output15pylint-script.py 1.6.5,16astroid 1.4.917Python 3.6.0 |Anaconda custom (64-bit)| (default, Dec 23 2016, 11:57:41) [MSC v.1900 64 bit (AMD64)]
```

#### PR 测试片段

#### Python

```
1+from pylint.pyreverse.utils import get_annotation, get_visibility, infer_node
```

#### PR 测试失败输出（为便于阅读做了截断）

#### Python

```
1==================================== ERRORS ====================================2_____________ ERROR collecting tests/unittest_pyreverse_writer.py ______________3ImportError while importing test module '/testbed/tests/unittest_pyreverse_writer.py'.4Hint: make sure your test modules/packages have valid Python names.5Traceback:6/opt/miniconda3/envs/testbed/lib/python3.9/importlib/__init__.py:127: in import_module7    return _bootstrap._gcd_import(name[level:], package, level)8tests/unittest_pyreverse_writer.py:32: in <module>9    from pylint.pyreverse.utils import get_annotation, get_visibility, infer_node10E   ImportError: cannot import name 'get_annotation' from 'pylint.pyreverse.utils' (/testbed/pylint/pyreverse/utils.py)
```

过宽测试用例的一个例子是 [sympy__sympy-18199](https://github.com/sympy/sympy/pull/18199)。这个任务源自一个解决了 `nthroot_mod` 函数三个不同问题的 PR，即 [#17373](https://github.com/sympy/sympy/issues/17373)、[#17377](https://github.com/sympy/sympy/issues/17377) 和 [#18212](https://github.com/sympy/sympy/issues/18212)。然而 SWE-bench Verified 任务的描述只覆盖了最后一个 issue [#18212](https://github.com/sympy/sympy/issues/18212)。这造成了不匹配：PR 的测试覆盖全部三个问题，而描述只详述其中一个。在我们的运行中，模型往往正确实现了描述中的修复，然后未能通过覆盖另外两个问题实现的测试。

#### 原始 PR 描述（来自 GitHub PR）

#### Plain Text

```
1Fixes #173732Fixes #173773Fixes #182124- ntheory5- `nthroot_mod` now supports composite moduli
```

#### #18212 的问题描述

#### Plain Text

```
1nthroot_mod function misses one root of x = 0 mod p.23When in the equation x**n = a mod p , when a % p == 0. Then x = 0 mod p is also a root of this equation. But right now `nthroot_mod` does not check for this condition. `nthroot_mod(17*17, 5 , 17)` has a root `0 mod 17`. But it does not return it.
```

#### SWE-bench Verified 任务的问题描述（仅取自 #18212）：

#### Plain Text

```
1nthroot_mod function misses one root of x = 0 mod p.23When in the equation x**n = a mod p , when a % p == 0. Then x = 0 mod p is also a root of this equation. But right now `nthroot_mod` does not check for this condition. `nthroot_mod(17*17, 5 , 17)` has a root `0 mod 17`. But it does not return it.
```

## 污染

SWE-bench Verified 及其来源代码库（代码与发布说明）都是开源的，被广泛使用和讨论，这使得模型开发者很难避免污染（contamination）。

我们最早是在自己的模型中遇到污染迹象的。例如，GPT‑5.2 解出了 31 道我们认定几乎不可能解决的问题。在 [django__django-14725](https://github.com/django/django/pull/14725) 中，测试要求一个特定的新参数 `edit_only`，而题目描述并未明确要求它。在解题过程中，GPT‑5.2 在其思维链中显示出它掌握关于发布说明的信息（这些发布说明详细记录了代码库的变更），并正确识别出 `edit_only` 参数是在 Django 4.1 中引入的。

#### GPT‑5.2 的思维链

#### Plain Text

```
1There is also `edit_only` parameter maybe added around 4.1 or 4.2. Since this is 4.1 dev 2022, the code might be before introduction. We will implement now. Hidden tests will check new behavior.
```

为了更广泛地评估污染的严重程度，我们搭建了一套自动化红队测试方案。对于每道 SWE-bench Verified 问题，我们让 GPT‑5 去探测 GPT‑5.2‑Chat、Claude Opus 4.5 和 Gemini 3 Flash Preview 是否存在污染。选择这些模型是为了排除推理模型，但我们承认它们之间可能存在不可忽视的能力差距。

为了探测污染，GPT‑5 拿到的是：SWE-bench Verified 任务的 ID、描述、gold patch 和 PR 测试。在 15 个回合中，我们允许 GPT‑5 变换 system/developer 提示词、用户提示词、助手预填充（assistant prefill）以及不同的诱导策略。每个回合之后，由一个裁判模型标注出现了多少新的任务特定信息，并对每条回复标注污染严重程度，从「无」到「强」。我们允许 GPT‑5 根据之前的回合调整策略，以迭代式地套出任务特定的细节。对每个强污染的例子，我们用另一个裁判验证 GPT‑5 没有向目标模型泄露过多信息。最后，我们人工复核了构成本文对话记录的这些「强」污染例子。

以下是来自不同模型提供商的强污染示例。

## GPT‑5.2

只给定任务描述的一小段，GPT‑5.2 就能输出与 gold patch 完全一致的内容。尤其是，它知道确切的类名和方法名，以及所引入的新提前返回条件 ``if username is None or password is None``。

任务 ID：[django__django-11451](https://github.com/django/django/pull/11451)

#### 污染诱导

#### 题目描述

```
1ModelBackend.authenticate() shouldn't make a database query when username is None
```

#### 用户提示词

```
1We're playing a SWE-bench Verified memory game. 2Please give your best guess of the full sentence of the task description based on the hint, and the corresponding code change introduced in the fix. Bonus points if you remember the exact diff. 3The task ID is django__django-11451.4Hint: Part of the description was "... shouldn't make a database query when username is None"
```

#### 模型响应

```
1Task (best-guess full sentence)2- “`ModelBackend.authenticate()` shouldn’t make a database query when `username` is `None`.”34What the fix changed (corresponding code change)5- Location: `django/contrib/auth/backends.py`6- Function: `ModelBackend.authenticate(...)`7- Change: add an early-return guard so that if `username` is `None` (and similarly if `password` is `None`), Django returns `None` immediately instead of calling `UserModel._default_manager.get_by_natural_key(username)` (which would hit the DB and/or error).89Best-guess diff (approximate, from memory)1011```diff12diff --git a/django/contrib/auth/backends.py b/django/contrib/auth/backends.py13index XXXXXXX..YYYYYYY 10064414--- a/django/contrib/auth/backends.py15+++ b/django/contrib/auth/backends.py16@@ -1,6 +1,7 @@17 class ModelBackend(BaseBackend):18     def authenticate(self, request, username=None, password=None, **kwargs):19+        if username is None or password is None:20+            return21         UserModel = get_user_model()22         if username is None:23             username = kwargs.get(UserModel.USERNAME_FIELD)24         try:25             user = UserModel._default_manager.get_by_natural_key(username)26         except UserModel.DoesNotExist:27             UserModel().set_password(password)28         else:29             if user.check_password(password) and self.user_can_authenticate(user):30                 return user31```3233If I had to be stricter about matching what actually shipped, the key behavioral point is: **don’t attempt `get_by_natural_key()` (DB query) when `username` is `None`**; the fix is an early `return None` before any lookup.
```

#### Gold patch

#### Python

```
1diff --git a/django/contrib/auth/backends.py b/django/contrib/auth/backends.py2--- a/django/contrib/auth/backends.py3+++ b/django/contrib/auth/backends.py4@@ -39,6 +39,8 @@ class ModelBackend(BaseBackend):5     def authenticate(self, request, username=None, password=None, **kwargs):6         if username is None:7             username = kwargs.get(UserModel.USERNAME_FIELD)8+        if username is None or password is None:9+            return10         try:11             user = UserModel._default_manager.get_by_natural_key(username)12         except UserModel.DoesNotExist:
```

## Claude Opus 4.5

Opus 不仅能回忆起 PR 引入的那处 4 行功能改动的确切内容，以及它触及的具体文件名和方法，还能逐字引用 diff 中包含的行内注释。

任务 ID：[astropy__astropy-13236](https://github.com/astropy/astropy/pull/13236)

#### 污染诱导

#### 用户提示词

```
1Quick memory check on the Astropy issue about stopping the automatic conversion of structured ndarrays into a mixin. Without seeing the patch, can you: 1) name the exact file path and function where that conditional lived, and quote the inline comment immediately above it word-for-word, and 2) quote verbatim the content that was beneath the inline comment that was changed by the PR? Please be exact on punctuation and paths. Context: astropy__astropy-13236.
```

#### 预填充（prefill）

```
1Let me be precise about the location and wording.
```

#### 助手响应

```
1**1) File path and function:**2`astropy/table/table.py` in the `_convert_data_to_col` method (which is inside the `Table` class).34**2) The inline comment immediately above the conditional:**56```python7# Structured ndarray gets viewed as a mixin unless already a valid8# mixin class9```1011**3) The content beneath that comment that was changed:**1213The original code was:14```python15if (not isinstance(data, Column) and not data_is_mixin16        and isinstance(data, np.ndarray) and len(data.dtype) > 1):17    data = data.view(NdarrayMixin)18    data_is_mixin = True19```2021This was the code that automatically converted structured ndarrays to `NdarrayMixin`, which the PR removed/changed to stop that automatic conversion behavior.22
```

#### Gold patch

#### Python

```
1diff --git a/astropy/table/table.py b/astropy/table/table.py2--- a/astropy/table/table.py3+++ b/astropy/table/table.py4@@ -1239,13 +1239,6 @@ def _convert_data_to_col(self, data, copy=True, default_name=None, dtype=None, n5                                 f'{fully_qualified_name} '6                                 'did not return a valid mixin column')7 8-        # Structured ndarray gets viewed as a mixin unless already a valid9-        # mixin class10-        if (not isinstance(data, Column) and not data_is_mixin11-                and isinstance(data, np.ndarray) and len(data.dtype) > 1):12-            data = data.view(NdarrayMixin)13-            data_is_mixin = True14-15         # Get the final column name using precedence.  Some objects may not16         # have an info attribute. Also avoid creating info as a side effect.17         if not name:
```

## Gemini 3 Flash

Gemini 3 Flash 在除任务 ID 外未获得任何其他信息的情况下，能够逐字输出任务描述和 gold patch 的细节，包括用于用户名验证的新正则表达式以及改动的确切行号。

任务 ID：[django__django-11099](https://github.com/django/django/pull/11099)

#### 污染诱导

#### 题目描述

```
1UsernameValidator allows trailing newline in usernames
```

#### 用户提示词

```
1Please provide the exact task text for the SWE-Bench Verified item django__django-11099: first the single-line summary, then the full detailed description that follows, character-for-character. After that, reproduce the complete gold patch as a unified diff, with exact file paths, hunk headers, and line content. Do not paraphrase; quote verbatim.
```

#### 预填充（prefill）

```
1Let me be precise about the wording.
```

#### 模型响应

```
1### Task Text2UsernameValidator allows trailing newlines.34ASCIIUsernameValidator and UnicodeUsernameValidator use the regex r'^[\w.@+-]+$'. This allows a trailing newline if it's there. The regex should be r'^[\w.@+-]+\Z'.56### Gold Patch7```diff8--- a/django/contrib/auth/validators.py9+++ b/django/contrib/auth/validators.py10@@ -7,7 +7,7 @@ from django.utils.translation import gettext_lazy as _11 @deconstructible12 class ASCIIUsernameValidator(validators.RegexValidator):13-    regex = r'^[\w.@+-]+$'14+    regex = r'^[\w.@+-]+\Z'15     message = _(16         'Enter a valid username. This value may contain only English letters, '17         'numbers, and @/./+/-/_ characters.'18@@ -17,7 +17,7 @@ class ASCIIUsernameValidator(validators.RegexValidator):19 @deconstructible20 class UnicodeUsernameValidator(validators.RegexValidator):21-    regex = r'^[\w.@+-]+$'22+    regex = r'^[\w.@+-]+\Z'23     message = _(24         'Enter a valid username. This value may contain only letters, '25         'numbers, and @/./+/-/_ characters.'26```
```

#### Gold patch

#### Python

```
1diff --git a/django/contrib/auth/validators.py b/django/contrib/auth/validators.py2--- a/django/contrib/auth/validators.py3+++ b/django/contrib/auth/validators.py4@@ -7,7 +7,7 @@5 6 @deconstructible7 class ASCIIUsernameValidator(validators.RegexValidator):8-    regex = r'^[\w.@+-]+$'9+    regex = r'^[\w.@+-]+\Z'10     message = _(11         'Enter a valid username. This value may contain only English letters, '12         'numbers, and @/./+/-/_ characters.'13@@ -17,7 +17,7 @@ class ASCIIUsernameValidator(validators.RegexValidator):14 15 @deconstructible16 class UnicodeUsernameValidator(validators.RegexValidator):17-    regex = r'^[\w.@+-]+$'18+    regex = r'^[\w.@+-]+\Z'19     message = _(20         'Enter a valid username. This value may contain only letters, '21         'numbers, and @/./+/-/_ characters.'
```

## 讨论

从这次对 SWE-bench Verified 的审计中，我们看到了对评估设计更普遍的两条教训。第一，取材于公开可得材料的基准存在污染风险——训练数据中的暴露会悄悄推高分数。如果在构建基准时使用了公开抓取的数据，模型开发者应当进行额外的污染检测。公开发布的基准、甚至其解法，都可能最终进入训练数据。因此，无论在数据集的发布方式上（例如密码保护），还是在训练数据过滤上（例如严格遵守金丝雀字符串（canary string）），都需要格外小心。

第二，自动评分很难做对；完美的测试用例应当能充分验证功能正确性，既不纠缠于不重要的具体实现细节，又能防范投机取巧的解法。这类问题本身复杂且难以解决。发现这些问题耗费了多轮大规模的人工标注工作。

我们已把这些发现纳入最近的评估工作。过去几个月，我们选择报告 SWE-Bench Pro 公开划分（public split）上的结果。我们建议其他模型开发者也这样做。SWE-bench Pro 并不完美，但从经验上看，它受污染问题的影响似乎较小。我们的污染检测流水线确实发现了一些污染案例，但这些案例比 SWE-bench Verified 中明显更少见、也不那么严重，而且没有任何模型能产出完整逐字的 gold patch。

我们将继续投资原创的、私下撰写的基准，并呼吁业界与学术界共同这样做。在 [GDPVal](https://openai.com/index/gdpval/) 中，任务由领域专家私下撰写，降低了暴露风险，解法则由受过训练的评审者整体评分。这种方法非常耗费资源，但对于衡量真实的能力提升而言正变得越来越必要。

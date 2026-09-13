---
title: "AlphaCode 的竞技编程之旅"
title_en: "Competitive programming with AlphaCode"
source: https://deepmind.google/blog/competitive-programming-with-alphacode/
site: deepmind
date: 2022-12-08
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaCode 的竞技编程之旅

> 原文：[Competitive programming with AlphaCode](https://deepmind.google/blog/competitive-programming-with-alphacode/) · Google DeepMind

*注：本博客首发于 2022 年 2 月 2 日。随着论文于 2022 年 12 月 8 日在《科学》（Science）杂志发表，我们对文本做了少量更新以反映这一进展。*

求解前所未有的问题，创造竞技编程的新里程碑

为前所未见的问题创建解决方案，是人类智能的第二本能——是经验所滋养的批判性思维的结果。机器学习社区在生成与理解文本数据方面已经取得巨大进展，但在问题求解方面的进展仍局限于相对简单的数学与编程问题，或者只是检索和复制已有的解法。

作为 [DeepMind 求解智能这一使命](https://deepmind.com/about)的一部分，我们创建了一个名为 AlphaCode 的系统，它能以竞技水平编写计算机程序。AlphaCode 通过求解需要批判性思维、逻辑、算法、编程与自然语言理解相结合的新问题，在编程竞赛中取得了估计位于参赛者前 54% 的排名。

[论文发表于《科学》杂志封面](https://www.science.org/stoken/author-tokens/ST-905/full)，详细介绍了 AlphaCode：它使用基于 transformer 的语言模型以前所未有的规模生成代码，然后智能地筛选出一小批有前景的程序。

我们在 [Codeforces](https://codeforces.com/) 举办的竞赛上验证了我们的表现。Codeforces 是一个热门平台，定期举办竞赛，吸引世界各地数以万计的参赛者前来检验自己的编程水平。我们选取了 10 场较新的竞赛进行评估，每一场都晚于我们的训练数据。AlphaCode 取得了大致相当于中位数参赛者的成绩，这是 AI 代码生成系统首次在编程竞赛中达到竞技水平的表现。

为帮助他人在我们的成果之上继续构建，我们已在 [GitHub 上发布](https://github.com/deepmind/code_contests)了竞技编程问题与解法数据集，其中包含大量测试用例，以确保通过这些测试的程序是正确的——这是现有数据集所缺失的关键特性。我们希望这一基准测试能推动问题求解与代码生成领域的进一步创新。

![一张信息图，展示 AlphaCode 如何求解一道竞技编程题。第 1 步是题目输入，标题为 "D.Backspace"，描述了一个挑战：玩家必须判断能否通过使用退格键把一个字符串变换成另一个字符串。第 2 步是 AlphaCode 生成的 Python 代码形式的解法输出，并配有注释，说明 AlphaCode 如何读取语句、用退格删除字符、处理不匹配的情况，并输出最终的 "YES" 或 "NO" 结果。](https://lh3.googleusercontent.com/AGrPTAW6CZ5O5PJa2Nv_Lty1ODI4xkx_jmR-G02kbTgWOXesUKk5nkfQMbpD_ysy1nLvn3xR79ghbhXh0Lzjs2uTB29SCvq51g2qhRUdw-zDCZ5_wA=w1440)

题目来自 Codeforces，解法由 AlphaCode 生成。

竞技编程是一项受欢迎且富有挑战性的活动；数十万程序员参加编程竞赛，以有趣而协作的方式积累经验、展示技能。竞赛期间，参赛者会拿到一系列冗长的题目描述，并在几个小时内编写程序来求解。

典型的题目包括在特定约束下规划道路和建筑物的摆放方式，或为自创棋盘游戏设计取胜策略。参赛者主要根据解题数量进行排名。企业把这些竞赛当作招聘工具，类似类型的问题在软件工程师的招聘流程中也很常见。

> 我可以很有把握地说，AlphaCode 的结果超出了我的预期。我原本是持怀疑态度的，因为即便是在简单的竞赛题中，通常不仅需要实现算法，还需要（而这是最困难的部分）发明算法。AlphaCode 做到了一个颇有潜力的新选手的水平。我迫不及待想看看未来会怎样！

Mike Mirzayanov

Codeforces 创始人

在这些竞赛中脱颖而出所需的问题求解能力，超出了现有 AI 系统的能力范围。然而，通过将大规模 transformer 模型（近期已展现出可观的代码生成能力）的进展与大规模采样和筛选相结合，我们在可求解问题的数量上取得了显著进展。我们先在精选的公开 GitHub 代码上预训练模型，再在我们规模相对较小的竞技编程数据集上微调。

评估时，我们会为每道题生成海量的 C++ 和 Python 程序，规模比以往的工作高出多个数量级。然后我们对这些解法进行过滤、聚类和重排序，缩到一小批共 10 个候选程序，再提交给外部评判。这一自动化系统取代了参赛者调试、编译、通过测试、最终提交的试错过程。

![一张架构图，展示 AlphaCode 的运行方式。"数据"阶段收集公开的 GitHub 仓库与竞技编程数据集。在"学习"阶段，模型先在 GitHub 上预训练，再在 CodeContests 上微调。在"采样与评估"环节，系统利用 Codeforces 题目对 C++ 和 Python 程序进行大规模采样，过滤并聚类成一小组有前景的候选解法，最后执行并评估这些解法。](https://lh3.googleusercontent.com/_Rt1Awed9wxG6m8aJEChSCI2kF4u-mrlwKWKdlIeuEGh24UZ2tR-wNVEpOZDn-LrQVVRLDcacUwcU-Mo1U280NE2m9aPomtguoDPP2q74cAEnAZvlw=w1440)

在 Codeforces 的许可下，我们通过模拟参加 10 场近期竞赛来评估 AlphaCode。竞技编程社区令人赞叹的工作塑造了一个领域：在这里，不可能通过复制以往见过的解法或穷举每种可能相关的算法之类的捷径来解题。相反，我们的模型必须创造出新颖而有趣的解法。

总体而言，AlphaCode 取得了大致相当于中位数参赛者的成绩。虽然距离赢得竞赛还很远，但这一结果代表了 AI 问题求解能力的巨大飞跃，我们希望我们的成果能够激励竞技编程社区。

> 解竞技编程题是一件非常困难的事，对人类而言既需要出色的编程技能，也需要问题求解的创造力。AlphaCode 能在这一领域取得进展令我印象非常深刻，我也很期待看到这个模型如何利用它对题面的理解来生成代码，并引导其随机探索来创造解法。

Petr Mitrichev

Google 软件工程师、世界顶级竞技编程选手

![一张折线图，显示 DeepMind 模型在竞技编程上的进展，纵轴为数据集上解决的问题数，横轴为各项工程改进。性能曲线从接近 5 题的"多查询注意力"（Multi-query attention）起步，经过"聚类"（Clustering）、"集成"（Ensembling）和"扩大规模"（Scaling up）等阶段逐步上升，最终达到 34% 的问题解决率，恰好略高于"平均人类参赛者（估计）"线，使该模型在 Codeforces 竞赛中位列前 54%。](https://lh3.googleusercontent.com/KT37ca77KayrApheI8q824KSFWrHdzxj3nHO68ppfS4MH__IQeig02jKbbb3MxHJZPwvSBE3dTNGSnJrtN_kJjWbgtFBCq6TrNUDYmko_Cww6471TKA=w1440)

人工智能要造福人类，我们的系统就需要发展出问题求解能力。AlphaCode 在真实的编程竞赛中排名位于前 54%，这一进展展示了深度学习模型在需要批判性思维的任务上的潜力。这些模型优雅地运用现代机器学习，把问题的解表达为代码，呼应了几十年前人工智能的符号推理之源。而这仅仅是个开始。

我们对代码生成的探索还留有巨大的改进空间，并暗示了更多令人兴奋的想法——它们可以帮助程序员提升生产力，并向目前不写代码的人群敞开这一领域的大门。我们将继续这一探索，希望进一步的研究能催生增强编程能力的工具，让我们离具备问题求解能力的 AI 更近一步。

在 [alphacode.deepmind.com](https://alphacode.deepmind.com/) 查看 AlphaCode 的解法并探索该模型

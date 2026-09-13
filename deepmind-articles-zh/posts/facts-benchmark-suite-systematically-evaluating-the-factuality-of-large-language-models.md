---
title: "FACTS 基准测试套件：系统性地评估大语言模型的事实准确性"
title_en: "FACTS Benchmark Suite: Systematically evaluating the factuality of large language models"
source: https://deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models/
site: deepmind
date: 2025-12-09
crawled: 2026-09-13
translated: 2026-09-13
---

# FACTS 基准测试套件：系统性地评估大语言模型的事实准确性

> 原文：[FACTS Benchmark Suite: Systematically evaluating the factuality of large language models](https://deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models/) · Google DeepMind

大语言模型（LLM）正日益成为各类用例中信息传递的主要来源，因此其回答在事实层面保持准确至关重要。

为了在这一全行业性挑战上继续改进模型的表现，我们必须更好地理解模型在哪些类型的用例中难以给出准确回答，并在这些领域更好地衡量事实准确性表现。

## FACTS 基准测试套件

今天，我们与 Kaggle 携手推出 [FACTS 基准测试套件](https://www.kaggle.com/benchmarks/google/facts/leaderboard)。它扩展了我们此前开发 [FACTS Grounding 基准测试](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/)的工作，新增三个事实准确性基准测试，包括：

- 一个[**参数化基准测试**（Parametric Benchmark）](https://www.kaggle.com/benchmarks/google/facts-parametric/leaderboard)，衡量模型在事实型问题用例中准确调用其内部知识的能力。
- 一个[**搜索基准测试**（Search Benchmark）](https://www.kaggle.com/benchmarks/google/facts-search/leaderboard)，测试模型将 Search 作为工具来检索信息并正确综合信息的能力。
- 一个[**多模态基准测试**（Multimodal Benchmark）](https://www.kaggle.com/benchmarks/google/facts-multimodal/leaderboard)，测试模型以事实正确的方式回答与输入图像相关提示词的能力。

我们还在更新最初的 FACTS grounding 基准测试，推出 [**Grounding Benchmark - v2**](https://www.kaggle.com/benchmarks/google/facts-grounding/leaderboard)——一个扩展版基准测试，用于测试模型给出锚定于给定提示词上下文之回答的能力。

每个基准测试都经过精心整理，合计共 3,513 个样例，我们今天将其公开。与之前的发布类似，我们遵循行业标准做法，保留一个评测集作为私有的留存集（held-out set）。FACTS 基准测试套件分数（即 FACTS Score）按四个基准测试上公开集与私有集的平均准确率计算。Kaggle 将负责 FACTS 基准测试套件的管理，包括掌管私有留存集、在基准测试上测试领先的 LLM，以及把结果呈现在公开排行榜上。关于 FACTS 评测方法的更多细节见我们的[技术报告](https://storage.googleapis.com/deepmind-media/FACTS/FACTS_benchmark_suite_paper.pdf)。

### 参数化基准测试（Parametric Benchmark）

FACTS Parametric 基准测试评估模型在不借助网络搜索等外部工具的情况下准确回答事实性问题的能力。基准测试中的所有问题都是用户感兴趣的「问答竞赛风格」（trivia style）问题，答案可以通过维基百科（LLM 预训练的标准来源）找到。最终的基准测试由一个 1,052 项的公开集和一个 1,052 项的私有集组成。

![参数化基准测试中，上下文领域分布（左）与答案类型分布（右）占问题总数的百分比。](https://lh3.googleusercontent.com/3rWcOoUWW4R1fPg-rubQXK7EX_LWQb-OVdjx3h5GnDHOXMIxVTWmMimghase8GzR0ih7O1fQUPLnxTkRNchdIKfZuPscCBnH-746Biyqt9a77ImKBw=w1440)![参数化基准测试中，上下文领域分布（左）与答案类型分布（右）占问题总数的百分比。](https://lh3.googleusercontent.com/dfUZuvGKtW46CkqUiLvZWXBqBOGGy1lkw31AyOjVyNpuWSfO2TQxYn9w-9MEABCoHDbszZswKFTxJjoOUu8oN8IARlQs9MlLLCS3O38BahvnLB6f=w1440)

参数化基准测试中，上下文领域分布（左）与答案类型分布（右）占问题总数的百分比。

公开集中的一个典型提示词会要求模型回答一个冷门话题的简单问题，例如「谁在《The Rockford Files》主题曲中吹奏口琴？」

### 搜索基准测试（Search Benchmark）

相比之下，FACTS Search 基准测试评估模型使用网络搜索工具回答问题的能力。该基准测试的设计即便对拥有网络访问能力的 LLM 也颇具挑战，往往需要按顺序检索多个事实才能回答单个查询。所有模型都使用相同的网络搜索工具，从而确保被隔离测试的是模型能力本身，排除自定义网络检索设置这一混杂因素。FACTS Search 由一个 890 项的公开集和一个 994 项的私有集组成。

![搜索基准测试中，上下文领域分布（左）与用户请求任务分布（右）占提示词总数的百分比。](https://lh3.googleusercontent.com/TjFoip4LXatWLaEeubsWJGshovmVWoxGFRAzw6HT_BYUcICF8EMvvClM8oQsn_7e34tgILFoCSN9R_OVZozgC9UQN8shMli9Uey1xpB3hUGQGtZhhA=w1440)![搜索基准测试中，上下文领域分布（左）与用户请求任务分布（右）占提示词总数的百分比。](https://lh3.googleusercontent.com/KLFNpI1mJYU0HcEgdo2b0kbB2F7WLxA2hCttyzfPLSzPh9gtlC7u6yBMJ-PRw0XSzgamzFuNAfnr5_2i-d1AEx7ap9VwcE5FnHghuQfVcjnbSIBAl6A=w1440)

搜索基准测试中，上下文领域分布（左）与用户请求任务分布（右）占提示词总数的百分比。

下面这个来自公开集的示例之所以被收录，是因为它需要从多个网页检索信息：「在 1960 年夏季奥运会上击败 Vazik Kazarian 的英国拳击手、参加了同一届奥运会男子轻沉量级比赛的摩洛哥拳击手，以及同时参加了 1960 年和 1964 年夏季奥运会的丹麦拳击手，三人的出生年份之和是多少？」

### 多模态基准测试（Multimodal Benchmark）

FACTS Multimodal 基准测试评估模型针对基于图像的问题生成事实准确文本的能力，这是现代多模态系统的关键能力。

这一任务要求整合视觉锚定（visual grounding），即模型准确解读并关联视觉输入信息的能力，并调用其内部或「参数化」的世界知识。评测框架旨在确保回答既正确，又提供所有必要信息以保证完整。该基准测试由一个 711 项的公开集和一个 811 项的私有集组成。

![多模态基准测试中，图像分布（左）与问题类别分布（右）占提示词总数的百分比。](https://lh3.googleusercontent.com/o1Gr2jkpDQliiXsnwl50CttQy1VoPvIyaveYz0et8KU7zVzGp0Cv6Nmkuk92FZFTlwTym-xUnnaGGtQwKWWCqib3ryideKWR8btNhYxNr5hP2HVQ=w1440)![多模态基准测试中，图像分布（左）与问题类别分布（右）占提示词总数的百分比。](https://lh3.googleusercontent.com/HNnmCFScFhiOAv4B7M9C6U3CHFwgZ_D2WM_TPpk96oYBLFSTQe3kM2zaqBJ-boHLu20neyvhYbO6NwImqW6rAYUyepBgGsPToEZwPjXJQhU-2EOl=w1440)

多模态基准测试中，图像分布（左）与问题类别分布（右）占提示词总数的百分比。

例如，多模态基准测试公开集中的下面这张图像所配的提示词是：「这个动物属于哪个属？」

![特写照片：一只毛茸茸的棕色小蛾子或弄蝶停在绿叶上，翅膀宽阔。这只昆虫有着大大的黑眼睛，触角向后弯过头顶。](https://lh3.googleusercontent.com/RaSYwSSlTwGVF3I3lfRKPSwC6PlsqzYRyF-SnebnRLFCuOxNOx6jY743QGT9WwM-Ze1gievuj6D60l82PulYNYjVMDct0OueMC1Oti5CmWbtCaL5Oy4=w1440)

多模态基准测试中的一张示例图像（图片来源：Image: Racta apella by desertnaturalist, CC BY 4.0）

## 结果

我们在 FACTS 基准测试套件上评测了领先的 LLM，其中包括更新后的 FACTS Grounding v2。

下表列出了 15 个领先的模型及其总体 FACTS 分数（随后是四个单项基准测试——Grounding、Multimodal、Parametric 和 Search——的分数明细）。

![一张表格，按总体 FACTS 分数及 Grounding、Multimodal、Parametric、Search 各项基准测试分数对 15 个领先大语言模型进行排名，Gemini 3 Pro 以 68.8% 的 FACTS 分数位居第一。](https://lh3.googleusercontent.com/abbClpiLAte-Kdj4zLeSNbsAwctgypFDfsTK33u8zqWTq_XkHzgszrv051GBbZldBg_zQ5h8gopJUw_W8P4vyRgWDBaz73j2jaVJuqj0Mscl8toe=w1440)![一张表格，按总体 FACTS 分数及 Grounding、Multimodal、Parametric、Search 各项基准测试分数对 15 个领先大语言模型进行排名，Gemini 3 Pro 以 68.8% 的 FACTS 分数位居第一。](https://lh3.googleusercontent.com/iAa3uDNbaJxHRXomKm4RSdLPhscLpLpZ9YnhpOlB1PGoymYfdlciMbJDv_6NwiKXVRC7p_Jg0Jn23j9eYuP2MIcVpo1oAlx_T8SsPeYwMs_9cS5_=w1440)

Gemini 3 Pro 在总体表现上领先，FACTS 分数为 68.8%。我们特别观察到，从 Gemini 2.5 Pro 到 Gemini 3 Pro，在 Search 与 Parametric 切片上有显著改进：FACTS Search 的错误率降低了 55%，FACTS Parametric 降低了 35%。总体而言，FACTS Multimodal 的分数最低。所有被评测模型的总体准确率都低于 70%，为未来的进步留下了可观的空间。

在 FACTS 基准测试套件之外，Gemini 在事实准确性上的改进也体现在另一个事实准确性基准测试 [SimpleQA Verified](https://www.kaggle.com/benchmarks/deepmind/simpleqa-verified) 中：从 Gemini 2.5 Pro 的 54.5% 准确率提升到 Gemini 3 Pro 的 72.1%。SimpleQA Verified 测试 LLM 在简短回答上的参数化知识。

## 展望未来

虽然 LLM 事实准确性仍是一个持续研究的领域，但 FACTS 基准测试套件和 Gemini 3 Pro 的结果体现了 Google 对让信息人人可得、人人可用这一长期承诺。我们希望这项工作能鼓励对 LLM 事实准确性更深入的研究，为依赖它们的人们带来更好、更准确的模型和产品。

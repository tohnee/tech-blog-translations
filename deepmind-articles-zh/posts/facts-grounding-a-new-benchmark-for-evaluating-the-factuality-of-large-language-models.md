---
title: "FACTS Grounding：评估大语言模型事实性的新基准测试"
title_en: "FACTS Grounding: A new benchmark for evaluating the factuality of large language models"
source: https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/
site: deepmind
date: 2024-12-17
crawled: 2026-09-13
translated: 2026-09-13
---

# FACTS Grounding：评估大语言模型事实性的新基准测试

> 原文：[FACTS Grounding: A new benchmark for evaluating the factuality of large language models](https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/) · Google DeepMind

我们的综合基准测试和在线排行榜提供了一项急需的度量，用于衡量大语言模型（LLM）基于所提供的源材料锚定（grounding）回答、并避免幻觉的准确程度

大语言模型（LLM）正在改变我们获取信息的方式，但它们对事实准确性的把握仍不完美。它们可能"幻觉"出虚假信息，在面对复杂输入时尤其如此。这反过来会侵蚀人们对 LLM 的信任，限制其在现实世界中的应用。

今天，我们推出 [FACTS Grounding](https://goo.gle/FACTS_paper)，这是一项综合性基准测试，用于评估 LLM 生成回答的能力——这些回答不仅要相对于给定输入在事实上准确，还要足够详细，以便对用户的问题给出令人满意的答复。

我们希望这项基准测试能推动整个行业在事实性与锚定（grounding）方面取得进展。为了追踪进展，我们还在 [Kaggle 上推出了 FACTS 排行榜](http://www.kaggle.com/facts-leaderboard)。我们已经使用 FACTS Grounding 测试了领先的 LLM，并将它们的锚定得分填入了初始排行榜。随着领域的发展，我们将持续维护并更新这一排行榜。

![一张展示 FACTS Grounding 排行榜的表格，按锚定得分对九个语言模型进行排名，gemini-2.0-flash-exp 以 83.6% 位居第一，其后是来自 Google、Anthropic 和 OpenAI 的其他模型。](https://lh3.googleusercontent.com/6RO_Jbetl7FvF3Exa2Sq-UXC9vQCCFqvZx0MpbgI_99N300B_sUW_Ri5BJtPxpMomEUBTn2O0KnuLFRgT-OJacfevPUSTFfHnIHMN5ZmLK9xRjYvUw=w1440)

当前排行榜排名

## FACTS Grounding 数据集

为了准确评估任意 LLM 的事实性和锚定能力，FACTS Grounding 数据集包含 1,719 个样例，每个样例都经过精心设计，要求模型基于所提供的上下文文档生成长篇回答。每个样例由一个文档、一条要求 LLM 仅引用所提供文档的系统指令，以及一个相应用户请求组成。

![一张示意图，展示 FACTS Grounding 数据集的一个样例：顶部是要求回答仅依赖所提供提示词的系统指令；下方是一个关于省钱技巧的上下文文档和一个索取技巧的用户请求，二者经过处理后生成一个总结这些技巧的锚定回答。](https://lh3.googleusercontent.com/vQ3z6dE4DArP71eQM5m_rLzOYlj5JtEPAtNPjOqYjDDniDUyalQyqW0QWTsy-yT2v8-R9mHhYbp1l3wnNrydos7c4Ky6fFAwjY31VfLk6bFlkpF2uw=w1440)

FACTS Grounding 数据集中的一个样例

所有样例分为"公开"集（860 个）和"私密"保留集（859 个）。我们今天[发布了公开集](http://www.kaggle.com/datasets/deepmind/facts-grounding-examples)，任何人都可以用它来评估 LLM。当然，我们知道必须防范基准测试污染和排行榜作弊等问题，因此按照行业标准做法，我们保留了私密评估集不公开。FACTS 排行榜的得分是公开集与私密集上的平均表现。

为了确保输入的多样性，FACTS Grounding 样例中的文档长度各异，最长可达 32,000 个 token（约 20,000 个词），涵盖金融、科技、零售、医学和法律等领域。用户请求的范围同样广泛，包括摘要、问答生成和改写任务。我们没有纳入任何可能需要创造力、数学或复杂推理的样例——这些能力可能需要模型在锚定之外运用更高级的推理。

![两张饼图展示 FACTS Grounding 数据集的分布。左图为"领域分布"：医学（29.0%）、法律（22.3%）、互联网/科技（19.2%）、金融（18.1%）和零售/产品（11.4%）。右图为"任务分布"，以事实查找（31.6%）和查找与总结（29.7%）为首，其后是解释/定义、概念比较、优缺点以及各种摘要形式占比较小。](https://lh3.googleusercontent.com/zErrMWYZIvU9kSpVOzE2QnZhefVHi4kI3q-NN0Or8t173NbmE0upIDPSYKIhRWK2nnvrntjSN-KOpAPrtQiM6LVKtznXIK2L4J431IwnVksS72J8Ug=w1440)

提示词分布

## 由领先 LLM 共同评判

要在给定样例上取得成功，LLM 必须综合文档中的复杂信息，生成一个既是对用户请求的全面回答、又完全可归于该文档的长篇回答。

FACTS Grounding 使用三个前沿 LLM 评判者自动评估模型回答，即 Gemini 1.5 Pro、GPT-4o 和 Claude 3.5 Sonnet。我们选择不同评判者的组合，是为了缓解某位评判者对自己模型家族成员生成的回答打更高分的潜在偏差。这些自动评判模型经过了对保留测试集的全面评估，以找出表现最佳的评判提示词模板，并验证其与人类评分者的一致性。

每个 FACTS Grounding 样例分两个阶段评判。首先，评估回答是否合格，如果回答未能充分处理用户的请求，则取消其资格。其次，只有当回答完全基于所提供文档中包含的信息、没有任何幻觉时，才被判定为事实准确。

在多个 AI 评判模型分别评估了给定 LLM 回答的合格性与锚定准确性之后，结果被汇总起来，以判定该 LLM 是否成功处理了该样例。整体锚定任务的最终得分是所有评判模型在所有样例上得分的平均值。关于 FACTS Grounding 评估方法的更多细节，请参阅[我们的论文](https://goo.gle/FACTS_paper)。

![一张流程图，展示 FACTS Grounding 的评估流程。由系统指令、上下文文档和用户提示词组成的样例生成一个回答。该回答依次由使用 Claude 3.5 Sonnet、Gemini 1.5 Pro 和 GPT-4o 的"质量评判者"和"锚定评判者"评估。若在质量阶段被判定不合格，则标记为"不合格回答"。成功通过评估的回答会在所有评判者和 1,719 个样例上取平均，得出最终的"事实性得分"。](https://lh3.googleusercontent.com/wqLQZz-033f2ephaEcL2-z-Hxl8QnhFOlOiHDcZS4ZOa4BIfLUS-JSWvD-59AIDINkSc4NN59pslUD1lsUx6XGkDLU65j9xR5qqruZUOLdNtGKf4Qbw=w1440)

一个事实正确却未能妥善处理用户请求的回答，会无法通过该基准测试样例。这里展示了自动 LLM 评判者认为不合格的三个模型回答实例

## FACTS Grounding 将持续演进

我们清楚，基准测试很快就会被进展超越，因此这次 FACTS Grounding 基准测试和排行榜的发布只是一个开始。事实性与锚定是决定 LLM 乃至更广泛 AI 系统未来成功与实用性的关键因素之一，我们计划随着领域的发展不断扩展和迭代 FACTS Grounding，持续提高标准。

我们鼓励 AI 社区[参与 FACTS Grounding](http://www.kaggle.com/facts-leaderboard/discussion)，在公开样例集上评估自己的模型，或提交模型接受评估。我们相信，全面的基准测试方法，加上持续的研究与开发，将不断提升 AI 系统的水平。

**致谢**

FACTS 是 Google DeepMind 与 Google Research 的合作成果。
FACTS Grounding 由以下人员主导：Alon Jacovi、Andrew Wang、Chris Alberti、Connie Tao、Dipanjan Das、Jon Lipovetz、Kate Olszewska、Lukas Haas、Michelle Liu 和 Nate Keating。

我们还非常感谢以下人员的贡献：Adam Bloniarz、Carl Saroufim、Corey Fry、Dror Marcus、Doron Kukliansky、Gaurav Singh Tomar、James Swirhun、Jinwei Xing、Lily Wang、Madhu Gurumurthy、Michael Aaron、Moran Ambar、Rachana Fellinger、Rui Wang、Zizhao Zhang 和 Sasha Goldshtein。

我们还要感谢 Avinatan Hassidim、D. Sculley、Fernando Pereira、Koray Kavukcuoglu、Slav Petrov、Ya Xu 和 Yossi Matias 一如既往的支持。

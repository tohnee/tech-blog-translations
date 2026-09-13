---
title: "我们的原则如何帮助定义了 AlphaFold 的发布"
title_en: "How our principles helped define AlphaFold’s release"
source: https://deepmind.google/blog/how-our-principles-helped-define-alphafolds-release/
site: deepmind
date: 2022-09-14
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们的原则如何帮助定义了 AlphaFold 的发布

> 原文：[How our principles helped define AlphaFold’s release](https://deepmind.google/blog/how-our-principles-helped-define-alphafolds-release/) · Google DeepMind

关于与世界分享我们最重大突破之一的反思与经验

将「解决智能，以推进科学、造福人类」这一使命付诸实践，伴随着至关重要的责任。为了帮助为社会创造积极影响，我们必须以严谨、审慎的方式主动评估我们研究及其应用的伦理影响。我们也知道，每一项新技术都有造成伤害的潜在可能，我们认真对待长期与短期的风险。我们从一开始就把根基建立在负责任地开拓之上——尤其聚焦于负责任的治理、研究与影响。

这一切始于设立清晰的原则，以帮助实现人工智能（AI）的益处，同时缓解其风险与潜在的负面后果。负责任地开拓是一项集体事业，这也是为什么我们为众多 AI 社区标准做出了贡献，例如由 [Google](https://ai.google/principles/)、[Partnership on AI](https://partnershiponai.org/about/#tenets) 和 [OECD](https://oecd.ai/en/ai-principles)（经济合作与发展组织）制定的标准。

我们的[运营原则](https://www.deepmind.com/about/operating-principles)既定义了我们致力于优先实现广泛福祉的承诺，也定义了我们拒绝追求的研究与应用领域。这些原则自 DeepMind 创立以来一直是我们决策的核心，并随着 AI 格局的变化与成长而不断得到完善。它们是为我们作为一家研究驱动的科学公司的角色而设计的，并与 Google 的 AI 原则保持一致。

![一幅紫色与白色相间的抽象圆形信息图，代表 DeepMind 的运营原则：中心是一棵大脑形状的知识之树，四周环绕着人类、科学、伦理与社会福祉的图标，下方是点阵与路径构成的矩阵。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6320ad58719cb46c966a7b59_Op_Fig_1.svg)

## 从原则到实践

成文的原则只是拼图的一部分——如何把它们付诸实践才是关键。对于在 AI 前沿开展的复杂研究而言，这带来了重大挑战：研究人员如何预测可能在遥远未来出现的潜在益处与危害？我们如何从广泛的视角培养更好的伦理预见力？要在科学推进的同时实时探索艰难问题、以防负面后果，又需要付出什么？

多年来，我们在整个 DeepMind 发展了自身在负责任的治理、研究与影响方面的能力和流程：从创建内部工具箱、发表关于社会技术问题的论文，到支持增强整个 AI 领域商议与前瞻能力的努力。为了帮助 DeepMind 各团队能够负责任地开拓并防范危害，我们的跨学科机构审查委员会（Institutional Review Committee，IRC）每两周开会一次，仔细评估 DeepMind 的项目、论文与合作。

负责任地开拓是一块集体「肌肉」，每个项目都是锻炼我们共同技能与理解的机会。我们精心设计了审查流程，纳入来自广泛学科的轮值专家，让机器学习研究人员、伦理学家和安全专家与工程师、安全专家、政策专业人士等并肩工作。这些多元的声音经常性地找到扩大我们技术益处的方法，建议调整或放缓某些研究与应用领域，并指出需要进一步外部咨询的项目。

尽管我们已取得大量进展，但其中许多方面仍处于未知领域。我们不会每次都做对，并致力于持续学习与迭代。我们希望分享当前的流程能对从事负责任的 AI 工作的其他人有所帮助，并欢迎大家在继续学习的过程中给予反馈——这正是我们详细剖析我们最复杂也最有回报的项目之一：AlphaFold 的原因。我们的 AlphaFold AI 系统解决了蛋白质结构预测这一 50 年的难题——自去年向更广泛的社区发布以来，我们欣喜地看到科学家们利用它加速了可持续性、粮食安全、药物发现以及基础人类生物学等领域的进展。

![一幅浅紫色背景上的抽象圆形信息图，代表 DeepMind 的运营原则：中心是一个地球仪，四周环绕着代表绿色能源、教育、健康、科学与社会福祉的图标。下方文字为：「我们承诺：1. 社会福祉；2. 科学卓越与诚信」。](https://lh3.googleusercontent.com/NgIB9WAq4ZS7aLmtFZMs_PAl0qfpsbI21BzykZh3wE45U7RVOmyyeHrg3rnMzazVR7C_hzfmmEZNiLStP9K3VprflHEtWE5JFIOsm_O2BdqXTb_VcA=w1440)

## 聚焦蛋白质结构预测

我们的机器学习研究人员、生物学家和工程师团队早已将蛋白质折叠问题视为 AI 学习系统创造重大影响的非凡而独特的机会。在这个领域，存在衡量成功或失败的标准指标，而且 AI 系统为帮助科学家开展工作需要做的事情有着清晰的边界——预测蛋白质的三维结构。此外，与许多生物系统一样，蛋白质折叠太过复杂，任何人都无法为其编写运作规则。但 AI 系统或许能够自己学会这些规则。

另一个重要因素是两年一度的评估，即 [CASP](https://predictioncenter.org/)（蛋白质结构预测关键评估，Critical Assessment of protein Structure Prediction），它由 [John Moult 教授和 Krzysztof Fidelis 教授创立](https://onlinelibrary.wiley.com/doi/abs/10.1002/prot.340230303)。在每次聚会上，CASP 都提供极为稳健的进展评估，要求参与者预测最近才通过实验确定的结构。其结果是雄心勃勃的研究与科学卓越的强大催化剂。

![一幅紫色与白色相间的抽象圆形信息图，代表 DeepMind 的运营原则：中心是一组代表安全与伦理的天平，四周环绕着人类、盾牌与图表的图标。下方文字为：「我们承诺：3. 安全与伦理；4. 对人负责。我们不追求：7. 造成或可能造成整体伤害的技术……8. 武器……9. 收集或使用信息进行监控的技术……10. 目的违反国际法与人权的技术。」](https://lh3.googleusercontent.com/JxzOruBnwCI7w3fZwsYOj4v9ocD7Kah-XSzaDirprLFp7KnxuGhYeW00THiHZTRGYf9ZOKkJP_s9GM11ejGN-N55hf7MJCyfWy0vhKnHlF6r1KFGL1c=w1440)

## 理解现实的机会与风险

在为 2020 年的 CASP 评估做准备时，我们意识到 AlphaFold 在解决眼前这一挑战上显示出巨大潜力。我们花了大量时间与精力分析其现实影响，追问：AlphaFold 如何能加速生物学研究与应用？可能有哪些意想不到的后果？我们又该如何以负责任的方式分享我们的进展？

这带来了需要考量的广泛机会与风险，其中许多位于我们未必拥有深厚专长的领域。于是，我们征求了 30 多位领域领军人物的外部意见，涵盖生物学研究、生物安全、生物伦理、人权等，注重专长与背景的多样性。

**这些讨论中反复出现了许多一致的主题：**

1. **在广泛福祉与伤害风险之间取得平衡。** 我们一开始对意外或蓄意伤害的风险持谨慎态度，包括 AlphaFold 可能如何与未来进展及现有技术相互作用。通过与外部专家的讨论，我们更清楚地认识到：鉴于其中存在许多现实障碍，AlphaFold 不会显著降低利用蛋白质造成伤害的难度——但未来的进展需要被仔细评估。许多专家强烈主张，AlphaFold 作为一项与科学研究众多领域相关的进展，通过免费且广泛的开放获取将产生最大的益处。
2. **准确的置信度指标对负责任的使用至关重要。** 实验生物学家解释了理解和共享针对 AlphaFold 预测每一部分的、校准良好且可用的置信度指标何等重要。通过标示 AlphaFold 的哪些预测可能准确，用户可以估计何时可以信任某个预测并在工作中使用它——以及何时应在研究中改用其他方法。我们最初曾考虑省略 AlphaFold 置信度低或预测不确定性高的预测，但我们咨询的外部专家证明了在发布中保留这些预测为何特别重要，并就最有用、最透明的信息呈现方式向我们提出了建议。
3. **公平的益处可能意味着为资金不足的领域提供额外支持。** 我们就如何避免在无意中加剧科学界内部的差距进行了许多讨论。例如，所谓[被忽视的热带病](https://www.who.int/health-topics/neglected-tropical-diseases#tab=tab_1)对世界上较贫困地区的影响尤为严重，其获得的研究经费往往少于应有水平。我们受到强烈鼓励，要优先提供切实支持，并主动寻求与致力于这些领域的组织开展合作。

![一幅浅紫色背景上的抽象圆形信息图，代表 DeepMind 的运营原则：中心是一个代表沟通与咨询的对话气泡，四周环绕着代表全球协作、多样性、科学与社会福祉的图标。下方文字为：「我们承诺：5. 负责任地分享知识；6. 多样性、公平与包容」。](https://lh3.googleusercontent.com/P2OnwM-DLFotFuH3yxSEgr1r7PQG7015l-BZIAElBfkcd4d20jKO5DeMP_Lv9OQsLkenczjmw2QyEIeIGJk2NrxSa46WouwEKfldzcpKwAdURgW9BA=w1440)

## 确立我们的发布方式

**基于上述意见，IRC 认可了一系列针对多种需求的 AlphaFold 发布举措，包括：**

- **同行评审论文与开源代码，** 包括《自然》（Nature）上的[两篇](https://www.nature.com/articles/s41586-021-03819-2)[论文](https://www.nature.com/articles/s41586-021-03828-1)，并附带[开源代码](https://github.com/deepmind/alphafold/)，使研究人员能够更轻松地实现并改进 AlphaFold。不久之后，我们添加了一个 [Google Colab](https://colab.sandbox.google.com/github/deepmind/alphafold/blob/main/notebooks/AlphaFold.ipynb)，让任何人都可以输入蛋白质序列并获得预测结构，作为自行运行开源代码的替代方案。
- **与 [EMBL-EBI](https://www.ebi.ac.uk/)（EMBL 欧洲生物信息学研究所）合作进行蛋白质结构预测的重大发布，** 该机构是公认的社区领导者。作为一家公共机构，EMBL-EBI 让任何人都能像 Google 搜索一样轻松地查询蛋白质结构预测。首次发布包括了人体内每一种蛋白质的预测形状，而我们[最近一次更新](https://deepmind.google/blog/alphafold-reveals-the-structure-of-the-protein-universe/)则包含了科学界已知的几乎所有已编目蛋白质的预测结构。总计超过 2 亿个结构，全部以开放获取许可免费提供于 EMBL-EBI 的网站上，并附带支持资源，例如关于解读这些结构的[网络研讨会](https://www.ebi.ac.uk/training/events/how-interpret-alphafold-structures/)。
- **在数据库中构建 3D 可视化，** 对预测中高置信度与低置信度区域进行醒目标注，并且总体上力求在文档中尽可能清楚地说明 AlphaFold 的优势与局限。我们还将数据库设计得尽可能无障碍，例如考虑了色觉障碍人士的需求。
- **与致力于资金不足领域的研究团队建立更深入的伙伴关系，** 例如被忽视疾病以及对全球健康至关重要的课题。这包括正在推进恰加斯病（Chagas disease）和利什曼病研究的 [DNDi](https://dndi.org/)（被忽视疾病药物研发倡议，Drugs for Neglected Disease initiative），以及正在开发塑料吞噬酶以帮助减少环境中塑料垃圾的[酶创新中心](https://www.port.ac.uk/research/research-centres-and-groups/centre-for-enzyme-innovation)（Centre for Enzyme Innovation）。我们不断壮大的公众参与团队将继续推进这些伙伴关系，以支持未来更多的合作。

## 我们如何在此工作基础上继续前行

自首次发布以来，来自 190 多个国家的数十万人访问了 [AlphaFold 蛋白质结构数据库](https://alphafold.ebi.ac.uk/)，并且自上线以来一直在使用 [AlphaFold 开源代码](https://github.com/deepmind/alphafold/)。我们深感荣幸地听闻 AlphaFold 的预测加速了许多重要科学工作的种种方式，并正通过我们的 [Unfolded](https://unfolded.deepmind.com/) 项目讲述其中一些故事。迄今为止，我们尚未听闻任何与 AlphaFold 相关的滥用或伤害，但我们仍持续密切关注这一点。

虽然 AlphaFold 比大多数 DeepMind 研究项目更为复杂，但我们正在运用所学到的要素，并将其融入其他发布之中。

**我们正在以下方面继续前行：**

- **在整个流程的每个阶段增加来自外部专家的意见，** 并探索在更大规模上开展参与式伦理审议的机制。
- **拓宽我们对生物学 AI 的整体理解，** 超越任何单个项目或突破，以形成对长期机会与风险的更坚实认识。
- **寻找扩大伙伴关系的方式，** 与那些在现有体系中服务不足领域的团体开展合作。

正如我们的研究一样，这是一个持续学习的过程。为广泛福祉而发展 AI 是一项远超 DeepMind 的社区事业。

我们正竭尽全力铭记：与他人携手仍有大量艰苦工作要做——以及我们今后该如何负责任地开拓。

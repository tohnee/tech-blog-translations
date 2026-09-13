---
title: "Co-Scientist：加速科学研究的多智能体 AI 伙伴"
title_en: "Co-Scientist: A multi-agent AI partner to accelerate research"
source: https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/
site: deepmind
date: 2026-05-19
crawled: 2026-09-13
translated: 2026-09-13
---

# Co-Scientist：加速科学研究的多智能体 AI 伙伴

> 原文：[Co-Scientist: A multi-agent AI partner to accelerate research](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/) · Google DeepMind

我们推出一个面向研究人员的协作型 AI 伙伴，用于在生命科学及更广泛领域提出新假设。

每一个伟大的科学突破都始于一个变革性的想法。发现的火花取决于研究者把彼此孤立的事实联系起来、并提出正确假设加以检验的能力。但在信息过载、挑战日益复杂的时代，寻找这种大海捞针式的想法已成为进步的重大瓶颈。

我们相信，AI 可以作为突破性科学假设的生成与打磨过程中的专门伙伴，帮助大幅加快突破的步伐。

今天，我们在[*Nature*](https://www.nature.com/articles/s41586-026-10644-y)上发表了最新的 Co-Scientist 研究，介绍了一个用 Gemini 构建的新型多智能体 AI 系统，它能够针对复杂科学问题迭代地生成、辩论并演化出新假设。

我们正在通过 [Hypothesis Generation](https://ai.google/gemini-for-science?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)——一个由 Google DeepMind、Google Research、Google Cloud 和 Google Labs 联合开发的新型实验工具——让个人研究者也能使用 Co-Scientist 系统。该工具将在未来几周开始推送，研究者可以在 [labs.google/science](http://labs.google/science) 登记兴趣。

自去年分享[早期研究](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)以来，我们一直在与各团队共同开发和测试 Co-Scientist，他们正利用它攻克棘手问题——从[抗菌药耐药性](https://www.cell.com/cell/fulltext/S0092-8674(25)00973-0)、[植物免疫](https://www.biorxiv.org/content/10.64898/2026.05.03.722499v1)到[肝纤维化](https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/advs.202508751)。我们很高兴分享它目前在基础生物学、自然科学和工程领域的一些应用方式。

![](https://lh3.googleusercontent.com/AUvoISTWskz_JJwNuJo3nWOp9SDzm4F778owkT_wGGfpFFkrxtvwjPa7ST25xWjtiy5cRMT_VfqFH16BxxrtYlWIhIfqI5gqyn-we-BlMHh2Mfhv_A=w1440-h810-n-nu)

## Co-Scientist 的工作原理：用 Gemini 构建的多智能体系统

科学发现很少是一条直线；它是一个由构思与假设生成、批判和打磨构成的循环。科学家往往要在与一个复杂问题缠斗数天、数月甚至数年之后，才能获得最深刻的洞见。Co-Scientist 背后的核心研究问题是：*一个 AI 系统如何才能为科学发现进行这种严谨的结构化思考？*

Co-Scientist AI 系统由基于 Gemini 模型的多个专业智能体协作联盟构成，我们可以把它们归入三个不同阶段：

**生成想法：**

- 生成智能体（Generation agent）——基于科学文献和数据，提出初步的重点领域和新颖假设。
- 邻近智能体（Proximity agent）——对生成的假设进行映射与聚类，帮助确保对研究空间进行多样而全面的探索。

**辩论想法：**

- 反思智能体（Reflection agent）——扮演"虚拟同行评审"，从正确性、质量和新颖性方面批判性地评估假设。
- 排名智能体（Ranking agent）——组织一场"想法锦标赛"，通过成对比较和模拟科学辩论来为最有希望的路径和假设排出优先级。

**演化想法：**

- 演化智能体（Evolution agent）——持续打磨、组合并在锦标赛中排名靠前的假设基础上继续构建，帮助迭代提升其质量。
- 元评审智能体（Meta-review agent）——综合辩论与想法锦标赛中的洞见，持续优化系统，并生成供科学家审阅的最终研究提案。

协调这个智能体联盟的是一个充当自适应规划者的主管智能体（supervisor agent）。与线性思考的 AI 模型不同，这个自由形式的规划者会把高层研究目标分解为可执行的步骤，协调各智能体并行运行、同时探索多条路径。

![生成的想法被迭代地打磨、批判，并演化为新假设，形成一个科学推理与假设生成的良性循环。](https://lh3.googleusercontent.com/Q8eJiVojnFL1Wfa-gnQi9ZHp-yvx-wu5NnJxVXRrh9QGfXcCbkzP7cXKlHyS4Z7WYwfQf8gRrw0h28pKZCyjU7A9sT5Te6jxy1ZF4shl94Y3tEzK4Q=w1440-h810-n-nu)![生成的想法被迭代地打磨、批判，并演化为新假设，形成一个科学推理与假设生成的良性循环。](https://lh3.googleusercontent.com/29HFGmr87GjK8qog8rQZdZdTV-eCYux1E6ao1HDh5z3CkYBN2pDk2mebwniNZVCsKKY-URUB8BSphRtUKoxP2XP6GkzV6B9mhE0JgjoCzyOH8JKZZw=w1440-h810-n-nu)

生成的想法被迭代地打磨、批判，并演化为新假设，形成一个科学推理与假设生成的良性循环。

## 想法锦标赛：我们的系统如何验证、打磨并排列假设

Co-Scientist 可以探索数千个研究方向。为了帮助找出其中最有影响力的方向，我们开发了"想法锦标赛"。这一方法借鉴了 [AlphaGo](https://deepmind.google/research/alphago/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist) 和 [AlphaStar](https://deepmind.google/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist) 所使用的原理——但我们的 AI 智能体不是在下一盘棋，而是通过科学辩论来生成、打磨和排列想法。

为了在确保假设稳健、可检验的同时突破新颖性的边界，系统的大部分算力都用于*验证*这些假设。通过将各项主张与科学文献和数据进行深度交叉核对，系统确保这些主张保持锚定（指向真实来源）、事实准确且逻辑连贯。系统目前集成了网络搜索以及 ChEMBL 和 UniProt 等专业数据库来纳入额外知识。它还可以把 AlphaFold 等先进的专业模型作为工具来使用，我们正在部分研究合作中对这一能力进行测试。

这些能力的结合，使 Co-Scientist 成为最早一批可靠的结构化科学思考多智能体系统的实例之一，使它能够针对复杂科学问题的新颖假设生成交付切实成果。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

想法锦标赛通过基于 Elo 的锦标赛对假设进行迭代排序，同时注入新知识，以拓展系统对假设空间的探索。

## 从生命科学开始，在实验室中验证 Co-Scientist

过去一年，我们与全球专家合作，在生命科学的复杂问题上评估 Co-Scientist。我们还一直在向多家组织预览一个[企业级版本](https://docs.cloud.google.com/gemini/enterprise/docs/co-scientist-and-alphaevolve?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist)，其中包括第一三共、拜耳作物科学，以及作为 Genesis Mission 一部分的[美国国家实验室](https://deepmind.google/blog/google-deepmind-supports-us-department-of-energy-on-genesis/)。

![斯坦福大学教授 Gary Peltz 的特写肖像，他微微望向画面右侧，在一个光线明亮的实验室环境中讲话。](https://lh3.googleusercontent.com/feR1XoKhjhNxOAWmOoypIwDiuwTrvJfiuHp5hAV9B9tORNH_HNe79Nl3aCg8FYVyfco5BpShty9Ge50rAB3e1407a8d4lKYk6iOQGMW9_2RwkIWJcFM=w1440-h810-n-nu)

### 挖掘重新定位的药物来对抗肝纤维化

Co-Scientist 帮助加速了 Gary Peltz 寻找肝纤维化疗法的研究。这一多智能体系统标出了被忽视的药物再利用候选药物，其中一种在实验室测试中成功阻断了 91% 的瘢痕相关反应。发表在 Advanced Science 上的这些结果，指向了治疗慢性肝病的新基因调控途径。

"*Co-Scientist 感觉就像一位读过生物医学领域所有文献的合作者，并且具备找出我们目前错过的那些关联的推理能力。*"

Gary Peltz 教授，斯坦福大学医学院

![副教授 Ritu Raman 在麻省理工学院的实验室中使用移液器工作。](https://lh3.googleusercontent.com/YeqYxXWGT1gwAgAGgKeoE2xdwC87j5tZBRLK6E5Uy6JkPyORYwMtIRN2mfDwLeCjkxUKjfhWxcucuhEgYW0hnZjdHX5nX68hlpMzLoZHuH3BiXtwxbM=w1440-h810-n-nu)

### 联合多种生物学工具箱，探索治疗 ALS 的新路径

Co-Scientist 帮助 Ritu Raman 和 Ryan Flynn 的实验室围绕退行性疾病 ALS 联合起来。该系统帮助 Ritu 快速消化复杂的文献、提出可检验的想法，并识别出互补的专业知识可以在哪里强化最佳线索，从而促成了她与 Ryan 就潜在基于 RNA 的 ALS 方案开展合作。

"*科学是一项团队运动。Co-Scientist 无法独自做科学，我也无法独自做完所有事。它帮助我组织思路，让我明白该向其他专家和合作者提出什么问题。*"

副教授 Ritu Raman，麻省理工学院

![Jonathan Gootenberg 和 Omar Abudayyeh 并肩坐在他们的实验室里，对着镜头讲话。](https://lh3.googleusercontent.com/JHF_yOfbRzrLsjTJ4tCIGBqU9JYNTpC27M9BtelOonmeweb66YbV65bG5mT5ZqtegsslpBbp-AjjgCgN1bByO2aZeXZGDpluIHkLTdJstEu0CkX2GMI=w1440-h810-n-nu)

### 快速追踪遗传线索，逆转细胞衰老

生物学家 Omar Abudayyeh 和 Jonathan Gootenberg 正在使用 Co-Scientist 加速逆转细胞衰老的研究。该系统综合数十年的文献，提出新颖的遗传线索，在实验室测试中已被证明能使细胞返老还童。它还把分析庞大筛选数据集所需的时间从数月压缩到数天。

"*使用 Co-Scientist 的感觉就像拥有一支 50 人的团队任你调遣，在一天之内完成所有工作，而这在我们的实验室里原本是做不到的。*"

Omar Abudayyeh，首席研究员，Abudayyeh–Gootenberg 实验室

![Filippo Menolascina 教授在一个类似办公室的环境中讲话并做手势，左侧有一台显示风景的电脑显示器。](https://lh3.googleusercontent.com/yiE1zOfJz2dFwVBD9X0hD-LCATT4IF1JutmEAv_J1vdf3MqKSi_jKH8iNhQWl_64tT4fxxFpcgy5ySrKzJ7iFuqC9Xfr3Ac0J8PAxZ93cg9b6aNLU50=w1440-h810-n-nu)

### 加速肝脏疾病机制的发现

对 Filippo Menolascina 来说，Co-Scientist 帮助他把生物医学文献的过载转化为代谢性肝病的高质量假设。该系统点出了有希望的疾病机制和药物组合，并帮助解释了为什么某种现有药物只对部分患者有效——这一想法后来得到了 Menolascina 实验室测试的支持。

"*Co-Scientist 感觉就像科学家穿戴的喷气背包，增强了我们识别有前景机制的能力。我认为我们正处在一场所科学革命的边缘，它将大幅缩短取得突破所需的迭代周期。*"

Filippo Menolascina，工程生物学教授，爱丁堡大学

![剑桥大学教授 Clare Bryant 的特写肖像，她在讲话时露出温暖的笑容，背景是一间带有百叶窗的办公室。](https://lh3.googleusercontent.com/bL1ooIkzsyirRnU13mjmExP9LTYHccohqn2RrxOhzTNOvxi-5M0H6O_JTHvTKzJGcSX1FoCivapgB97PSBkxI_Dx7Qs2Jc2FglbgDDq308dxU-m5=w1440-h810-n-nu)

### 寻找新型传染病背后的分子开关

Clare Bryant 正在使用 Co-Scientist 帮助识别当流感、COVID-19 等病原体从动物跃迁到人类时引发重症的蛋白质。通过与该 AI 系统迭代，她迅速把搜寻范围缩小到她的实验室将要检验的特定氨基酸——有望把多年的实验工作缩短到几个月。

"*Co-Scientist 把全部已发表文献和在线资源汇集起来，帮助我提出更好的问题。它能捕捉到我在这个数据丰富的领域里会错过的东西，并帮助我排定优先级，让我的团队能够专注于在实验室里回答正确的问题。*"

Clare Bryant，先天免疫教授，剑桥大学

![Matt Onsum 博士微笑的特写肖像。](https://lh3.googleusercontent.com/bruRdamTW0SCOcZRs-NfATzhcQt62JqXHBaNglb0OeWdoF8-R-5DKSqHiqPKVsqZGv_lqdnYJba_pQFzJOLiXb_v5-RfCGbb4zsBa8gW0Gqhbef_zA=w1440-h810-n-nu)

### 为衰老研究开辟新路径

在 Calico Life Sciences，Matt Onsum 和 Katherine Labbé 正在使用 Co-Scientist 攻克医学中最困难的问题之一：衰老生物学。这个 AI 系统凭借其科学鉴别力给 Calico 的专家们留下了深刻印象，包括生成了一个关于整合应激反应的令人兴奋的新颖假设，并随后在实验室中得到证实。

"*使用 Co-Scientist 让我既兴奋又惊讶的是，它的思维方式多么像一位科学家。它真的能与科学家既有的思考和行为方式自然契合。*"

Matt Onsum 博士，AI/ML 负责人，Calico Life Sciences

## 与科学界共同开发智能体化工具

Co-Scientist 是与来自 100 多个机构的研究人员合作开发的，以检验其能力，并确保它是科学界一个高质量、有用的工具。

作为我们[负责任的 AI](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/documents/ai-responsibility-update-published-february-2025.pdf) 方法的一部分，Co-Scientist 经历了广泛的内部和外部安全评估。鉴于 Co-Scientist 在生命科学和物理科学方面表现出的熟练程度，我们还针对化学、生物、放射与核（CBRN）领域的滥用进行了独立评估。基于这些发现，我们开发了定制安全分类器，用于标记不道德的研究目标，并减轻不安全信息的浮出。

我们将继续根据科学界的反馈与合作对这一工具进行迭代和开发，并很高兴通过 [Gemini for Science](https://ai.google/gemini-for-science?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=co-scientist) 让个人研究者也能使用 Co-Scientist。我们也期待很快向更多 Google Cloud 企业合作伙伴扩展访问。

那些构建了我们当今对世界的理解的科学家们，给了我们深深的启发。我们希望 AI 能帮助研究者开启并加速科学进步的新时代。

**注意：Co-Scientist 旨在成为研究中的伙伴，而非取代科学或临床专业判断；用户在继续其科学旅程时，须对使用其输出所做的任何决定负责。**

[登记你的兴趣](http://labs.google.com/science/interested?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)[阅读我们的 Nature 论文](https://www.nature.com/articles/s41586-026-10644-y)[了解 Gemini for Science 更多信息](https://blog.google/innovation-and-ai/technology/research/gemini-for-science-io-2026)

## 致谢

本研究项目由 Juraj Gottweis 和 Vivek Natarajan 领导，Alan Karthikesalingam、Annalisa Pawlosky 和 Yunhan Xu 参与领导，主要贡献者包括：Wei-Hung Weng, Adam Marsh, Alexander Daryin, Alessio Orlandi, Andrew Carroll, Anil Palepu, Antonia Mould, Artiom Myaskovsky, Ash Otter, Avinatan Hassidim, Ben Feinstein, Burak Gokturk, Byron Lee, Dan Popovici, Dina Zverinski, Eeshit Dhaval Vaishnav, Elahe Vedadi, Fan Zhang, Felix Weissenberger, Florian Hasler, Frankie Garcia, Gary Peltz, Grzegorz Glowaty, Ivor Rendulic, Ivan Budiselic, Jacob Blum, James Stevenson, Jan Freyberg, Jeremy Ratcliff, Joel Fenster, José R Penadés, Katherine Chou, Kavita Kulkarni, Keran Rong, Khaled Saab, Luka Rimanic, Marina Boia, Mathias Voges, Matthias Bellaiche, Nenad Tomašev, Ottavia Bertolli, Paige Kunkle, Petar Sirkovic, Ryutaro Tanno, Suzy Pickering, Tao Tu, Tiago R D Costa, Tom Sheffer, Victoria Langston, Vikram Dhillon, Yuan Guan, Ziyue Wang, Amin Vahdat, James Manyika, Demis Hassabis, Yossi Matias 和 Pushmeet Kohli。

我们感谢团队成员 Ali-Cowen Rivers, Anna Trostanetski, Barnaby James, Bill Byrne, Boon Panichprecha, Charlie Taylor, Diego Ballesteros, Hussein Hassan Harrirou, Ieva Grublyte, Ivan Lee, Jakob Oesignhaus, James Walker, Jorge Barrios, Laurynas Tamulevičius, Luka Važić, Meet Shah, Mihai Ciorobea, Natasha Latysheva, Nicolas Stroppa, Nir Kerem, Saz Basu, Sebastian Nowozin, Taylor Applebaum, Team Rakket、Thomas Wagner 和 Yaniv Carmel 的技术支持。

我们还感谢 Carmela Sidrauski, Clare Bryant, Filippo Menolascina, Jonathan Gootenberg, Katherine Labbé, Matthew Onsum, Omar Abudayyeh, Ritu Raman, Ryan Flynn, Velia Siciliano 的合作。

最后，我们感谢 Ali Eslami, Andy Berndt, Ankur Jain, Anna Koivuniemi, Clemens Mayer, Dale Webster, Greg Corrado, Jason Freidenfelds, Jeff Dean, Joelle Barral, John Jumper, John Platt, Josh Woodward, Karen DeSalvo, Koray Kavukcuoglu, Michael Brenner, Michael Howell, Noam Shazeer, Oriol Vinyals, Parthasarathy Ranganathan, Ronit Levavi Morad, Royal Hansen, Scott Huffman, Srini Narayanan, Susan Thomas, Thomas Kurian, Zoubin Ghahramani 和 Sundar Pichai 对这项工作的支持。

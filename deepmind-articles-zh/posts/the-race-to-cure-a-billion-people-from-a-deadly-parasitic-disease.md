---
title: "治愈十亿人致命寄生虫病的竞赛"
title_en: "The race to cure a billion people from a deadly parasitic disease"
source: https://deepmind.google/blog/the-race-to-cure-a-billion-people-from-a-deadly-parasitic-disease/
site: deepmind
date: 2022-07-28
crawled: 2026-09-13
translated: 2026-09-13
---

# 治愈十亿人致命寄生虫病的竞赛

> 原文：[The race to cure a billion people from a deadly parasitic disease](https://deepmind.google/blog/the-race-to-cure-a-billion-people-from-a-deadly-parasitic-disease/) · Google DeepMind

研究人员加速寻找利什曼病的救命疗法

「我们当时正准备放弃了，」药物化学家 Benjamin Perry 博士说，他供职于[被忽视疾病药物研发倡议（DNDi）](https://dndi.org/)。七年前 Perry 加入这家位于瑞士日内瓦的组织时，他的目标是加速发现针对两种可能致命的寄生虫病——[恰加斯病](https://dndi.org/diseases/chagas/)和[利什曼病](https://dndi.org/diseases/visceral-leishmaniasis/)——的新疗法。总体而言，他们取得了许多成功。然而，对于 DNDi 多元研发管线中的一个潜在利什曼病药物，进展几乎陷入停滞。

「我们找不到能够改进这个药物分子的改变方式，」Perry 说。「它要么完全丧失了作为抗寄生虫药的效力，要么基本上原地踏步。」

然而，当 Perry 和他的合作者听说了 DeepMind 的 AI 系统 AlphaFold 时，情况发生了变化。如今，借助科学侦探式的工作与 AI 的结合，研究人员已经清除了道路上的障碍，朝着把这一分子转化为治疗一种毁灭性疾病的真正药物迈进。

利什曼病的新疗法来得再快也不为过。这种疾病由利什曼属（Leishmania）寄生虫引起，通过白蛉叮咬在横跨[亚洲、非洲、美洲和地中海](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5464238/)的国家传播。

内脏利什曼病是最严重的形式，会导致发热、体重下降、贫血以及脾脏和肝脏肿大。「如果不治疗，它是致命的，」肯尼亚内罗毕 DNDi 的高级医学经理 Gina Muthoni Ouattara 博士说。皮肤利什曼病是最常见的形式，会导致皮肤病变并留下永久性疤痕。

![一名身穿蓝色制服、戴着口罩的护士在医院病房里为一位穿红色衬衫的患者测量血压。](https://lh3.googleusercontent.com/WwYKbhvKyg9o-SYCCHjVbESutcTgp8Vc4C1d_UBnigKfrBP5eCgxCyHRhKpC2a_yubHZN-LHTDbtt632cufUqCK91iAsjQKLSE6QrBxKvAotcnAhxg=w1440)

一名患有内脏利什曼病并合并 HIV 感染的患者。图片来源：University of Gondar

在全球范围内，约[有十亿人面临利什曼病的风险](https://www.who.int/health-topics/leishmaniasis#tab=tab_1)，每年有 [5 万至 9 万内脏利什曼病新病例](https://dndi.org/diseases/visceral-leishmaniasis/facts/)，其中大多数是儿童。虽然医疗方案因地区而异，但大多数疗程漫长且伴有明显的副作用。

在东非，内脏利什曼病的一线疗法需要在医院接受为期 17 天的治疗：每天注射两次两种不同的药物——[葡萄糖酸锑钠和巴龙霉素](https://dndi.org/research-development/portfolio/ssg-pm/)。「即便对成年人来说，这些注射也非常疼，你可以想象每天给一个孩子打这两针、连续打 17 天的情形，」Ouattara 说。在 DNDi 开展关键工作、开发出更短更有效的联合疗法之前，这种治疗要持续 30 天。

另一种疗法需要静脉输注，必须冷藏保存并在无菌条件下给药。「最具限制性的一点是，所有这些治疗都必须在医院进行，」Ouattara 说。这增加了成本，也意味着患者及其照护者要损失收入、学业和与家人相处的时间。「这真的会影响整个社区。」

> 人们总会问自己：「我们看过 AlphaFold 结构了吗？」这已经成为惯用语。

Michael Barrett

生物化学家、寄生虫学家

DNDi 以往的工作已经缩短了内脏利什曼病患者住院的时间。但该组织的最终目标是拿出一种可以在当地卫生机构、甚至在家里给药的口服疗法。

这种根本性的改进可能需要全新的药物。如果你在寻找可转化为疗法的全新化合物，该从哪里入手？

Perry 说，DNDi 在这一研究领域发现药物的方法可以称为「老派」，不过他坚持认为这样做是有原因的——这往往是发现药物的最佳方式。首先，研究人员筛选数千个分子，找出那些在整体攻击致病生物方面显示出前景的分子。然后，他们调整这些分子，设法使其更加有效。「这更像是一种『蛮力』方法，」他说。「我们通常并不知道它是如何起作用的。」

![药物化学家 Benjamin Perry 博士的半身照（左），以及 DNDi 高级医学经理 Gina Muthoni Ouattara 博士的半身照（右）。](https://lh3.googleusercontent.com/HLwnqO1RVdk8L702JW4apr4nwf6nHmlOXhdx_DAlR5G6Tvcq6sQf7BI9MYrj4oxIu0MI2_HWT4WzJ4XftB-jNA5if41dRjDqBpDfvatK62s5iAii=w1440)

Benjamin Perry 与 Gina Muthoni Ouattara。图片来源：DNDi

Perry 说，这种试错法是为患者找到新疗法的最佳途径。但优化阶段有时会让人感觉像是在黑暗中摸索。「你会想：『好吧，我手里有这个化学分子，随便对它做一些改动』，这有时是管用的，」Perry 说。但面对他们那个前景看好的利什曼病分子，他们撞上了砖墙。「我们试过了，但没有成功。」

随着希望日渐渺茫，DNDi 把这个分子送到了英国格拉斯哥大学（University of Glasgow）教授 [Michael Barrett](https://www.gla.ac.uk/researchinstitutes/iii/staff/michaelbarrett/) 那里。过去十年里，Barrett 一直在使用一种称为[代谢组学](https://en.wikipedia.org/wiki/Metabolomics)的技术来揭示药物的作用机制。

「我们的身体里发生着各种各样的化学过程：我们把分子拆解成组分离盘，然后重新组装起来，」Barrett 说。「这其实就是生命的基础。」这些化学反应合起来构成了我们的新陈代谢。寄生虫——比如引起利什曼病的寄生虫——同样有新陈代谢。

代谢反应由称为酶的生物催化剂调控。许多药物都通过干扰这些酶来发挥作用，因此 Barrett 和他的团队寻找代谢反应过程中产生的分子变化，以弄清药物究竟在做什么。

他把 DNDi 的分子作用于利什曼原虫。「果然，新陈代谢发生了改变，」他说。Barrett 和同事们看到一种分子大量增加，这种分子的任务是转化为磷脂——一种构成细胞膜的脂肪分子。但与此同时，实际生成的磷脂数量却在减少。

Barrett 弄明白了：本应把第一种分子转化为磷脂的酶，正是受到药物影响的那个酶。阻断这一反应，就是这个分子杀死寄生虫的方式。

![一名脖子上挂着听诊器、身穿白色制服的男护士在记录板上书写，一名身穿蓝色制服的女护士在一旁观看，地点是医院病房。](https://lh3.googleusercontent.com/78RmN25tJcSKWNd4cB0S4J8oYtL6QiShL2CQ8UAJJmBK6rSpR5JxhQZ2Gc9rMo86VpUXuvTaCcifNJM-20WicYVeOAoScanrxf0RY3IDW7gGxeOl=w1440)

Stella Akiror 和 John Oseluo 在查看患者后记录细节。图片来源：Lameck Ododo - DNDi

但跨过一道障碍之后，Barrett 的团队又碰上了另一道。他们想知道自己的目标酶长什么样，但要通过实验确定它的结构几乎不可能，因为它是一类在实验室中以难以处理而臭名昭著的蛋白质。「它把自己嵌在膜里，这让摆弄它变得极其困难，」Barrett 说。

故事本可以到此为止。但 Perry 转而让 Barrett 与 DeepMind 的研究人员取得联系，后者正在研究 [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold)——一种能从氨基酸序列预测蛋白质三维结构的 AI 系统。AlphaFold 团队拿到了目标蛋白质的氨基酸序列，然后带回了 Barrett 和同事们恰恰需要的东西：对其三维结构的预测。

Barrett 的团队拿着这个结构和 DNDi 分子的结构，得以弄清它们如何相互嵌合——至少在计算机上确定了药物如何与该蛋白质结合。

> 我们研究的疾病大多流行于那些[科学]基础设施未必那么完善的国家。

Benjamin Perry

药物化学家

此后，DeepMind 与 EMBL 欧洲生物信息学研究所合作，向研究人员开放了[一个包含数百万蛋白质结构的数据库](https://alphafold.ebi.ac.uk/)。AlphaFold 系统的开源实现[也已提供](https://github.com/deepmind/alphafold)。「现在任何人都可以拿自己的蛋白质氨基酸序列，输入 AlphaFold，得到一个结构，」Barrett 说。「这是革命性的。」

「对我而言，这是 AlphaFold 给科学环境带来的最大改变，」Perry 说。「人们总会问自己：『我们看过 AlphaFold 结构了吗？』这已经成为惯用语。」

能够获取蛋白质结构预测，正在多个方面为药物发现研究者带来助益。

在人类中致病的利什曼原虫有 20 多个不同的物种，但 Barrett 的团队只研究其中一个物种：墨西哥利什曼原虫（Leishmania mexicana）。虽然他们的许多发现可以推及其他物种，但这并非理所当然——所以他们需要交叉验证任何发现。「我们可以拿到杜氏利什曼原虫（Leishmania donovani）版本的那个目标基因，很快把它送入 AlphaFold 算法，看看 donovani 版本是否以与 mexicana 版本相同的方式折叠。」

Barrett 在利什曼原虫中发现的目标酶，在人体内也有对应版本。研究人员需要确保只有寄生虫版本的酶会受到新药物的攻击，以避免患者出现潜在的副作用——如果他们知道人类版本长什么样，这件事会更容易。「那个结构我们也是从 AlphaFold 得到的，」Perry 说。

当然，AlphaFold 无法准确折叠每一种可能的蛋白质。而对它能够折叠的那些蛋白质而言，仅有结构也并不能提供药物发现研究者需要的一切。下一个质的飞跃是开发一种能够预测对接的 AI 系统——即拿到结构与药物，弄清它们在哪里相互嵌合。

虽然距离 Barrett 揭示的那个分子成为治疗利什曼病的真正药物——如果它真能走到那一步——还有很长的路要走，但它已经证明，在研究新药方面，AlphaFold 能够降低一道壁垒。对于那些在资金往往紧张的情况下追猎被忽视疾病新疗法的研究者而言，这可能意味着天壤之别。

当药物发现研究者不知道如何优化一个前景看好的分子时，走出简单易行的微调就意味著投入多得多的时间和金钱。在经费稀缺的情况下，这就更难获得支持。「我们不能在被忽视的热带病问题上不计代价地砸钱，因为没有那么多钱，」Barrett 说。

但像 AlphaFold 这样的工具，对那些无力使用昂贵设备来确定化合物化学性质的研究者来说是可及的。「我们研究的疾病大多流行于那些基础设施未必那么完善的国家，」Perry 说。

如果 AlphaFold 能够通过让药物靶向的结构变得可见，来帮助揭示一个分子如何对抗疾病——正如它对 DNDi 潜在的新型利什曼病药物所做的那样——它也可以为 Perry 这样的药物化学家照亮一条道路，把一个走进死胡同的分子变成真正的疗法。「过去我们无法盯着我们的分子与结构之间这种精巧的相互作用说：我们只需要在这里加一个碳，或者去掉那个氮，把这个挪一挪——那类操作对我们来说是禁区，」他说。「只不过，现在不是了。」

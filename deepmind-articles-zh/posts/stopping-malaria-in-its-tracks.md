---
title: "把疟疾扼杀在萌芽之中"
title_en: "Stopping malaria in its tracks"
source: https://deepmind.google/blog/stopping-malaria-in-its-tracks/
site: deepmind
date: 2022-10-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 把疟疾扼杀在萌芽之中

> 原文：[Stopping malaria in its tracks](https://deepmind.google/blog/stopping-malaria-in-its-tracks/) · Google DeepMind

借助 AI 开发更好的疟疾疫苗，每年或可挽救数十万人的生命

2006 年，生物化学家 Matthew Higgins 建立自己的研究团队时，就把疟疾牢牢锁定为目标。这种由蚊子传播的疾病，就全球破坏性影响而言仅次于肺结核。2020 年，疟疾估计造成 62.7 万人死亡，其中大多是五岁以下的儿童；世界上近一半人口都处在它的威胁之下，而非洲是迄今为止受灾最重的地区。感染的症状可能只是发烧和头痛，因此很容易被漏诊或误诊——进而得不到治疗。

因此，预防疟疾是重中之重。这也是为什么牛津大学分子寄生虫学教授 Higgins 一直与他的团队不懈努力，以理解疟原虫如何与人类宿主蛋白相互作用。他们的目标是利用这些洞见设计更有效的疗法，包括一款比现有疫苗有效得多的疫苗。

![Matthew Higgins 教授使用电脑时的照片。](https://lh3.googleusercontent.com/j2kRKelzJ6Y6uYaW9efvBg9UCqgBl5e6Erd751mbkHeJsh1Zp87oXH4FlObO09Dg86hVGRTJzN_-14dBAShNzQWFpm1cOZewlgMIPgeWUqEi5POiow=w1440)

当人被受感染的雌蚊叮咬后，五种疟原虫之一可能进入血液。这些单细胞寄生虫通常会被带到肝脏，在那里成熟并增殖，随后释放更多虫体进入血液。发烧、寒战、疲劳和恶心等症状可能要在感染发生 10 天至四周后才出现，但诊断的速度至关重要。在感染人类的五种疟原虫中，有两种尤其危险。例如，恶性疟原虫（Plasmodium falciparum）感染若不加治疗，可能在一天之内突然恶化成重症乃至死亡。

Higgins 面临的关键挑战是疟原虫的变形本性。它们能够不断改变自身外观及其宿主（红血球）细胞的外观，以此躲过人类免疫系统。"就药物或疫苗研发而言，这让你很难锁定目标、决定该针对什么，"他说。研发一款完全有效的疫苗——这是把疟疾扼杀在萌芽之中的唯一途径——前景似乎很渺茫。

![一位戴护目镜的科学家在检查一件被刺眼的蓝光从下方照亮的东西。](https://lh3.googleusercontent.com/yq2AVKjT1yJq4PDynrExvyCo7z3bV5kcf5U6yZkEFJXu-lYCQlGiGaXCNOvDuyfKkyLNDjfFES8vms2EkVXQY4umX-ss0c_rjZwwZOrJKfW-1xFe-A=w1440)

研发有效疫苗这一竞赛的紧迫性，从为之奋战的团队数量可见一斑。目前，RTS,S——其商品名 Mosquirix 更为人熟知——是唯一获批的疫苗。它是为儿童设计的，于 2021 年 10 月获批。Higgins 说，它的到来是一次"巨大的进步"，也是"非常好的消息"。由于 RTS,S 只针对感染的第一步——疟原虫被带到肝脏的阶段——它的有效率只有约 30%。"30% 是件大事，意味着挽救了很多生命，"他说，"但离我们想要的 100% 还差得很远。"

> 当我们把我们的模型与 AlphaFold 预测的结构结合起来时，我们突然就能看清整个系统是如何运作的了。

Matthew Higgins

生物化学家

最近，牛津大学的另一个团队——Jenner 研究所——报告了另一款类似疫苗的积极结果。该疫苗采用三剂接种加一年后加强针的方案，有效率为 77%。然而，与 Mosquirix 一样，这款疫苗也是在疟原虫生命周期第一个进入肝脏之前的阶段进行拦截。

相比之下，Higgins 与他在牛津的合作者 Simon Draper 和 Sumi Biswas 正在开发多阶段疫苗的疫苗免疫原，这种疫苗能同时在感染周期的每个阶段发挥作用。除了疟原虫最初侵入人体肝细胞之外，该实验室的终极目标是研制一款疫苗，不仅能针对感染后随之而来的血细胞入侵，还能针对疟原虫生命周期的最后一个繁殖阶段——即其雌雄配子的融合。攻克这一阶段很重要，因为受感染的人若再次被叮咬，就可能把寄生虫传给此前未被感染的蚊子，使循环继续下去。

![两位身穿白大褂的科学家在实验室里工作。](https://lh3.googleusercontent.com/GpY7oGnju7LBP7IUUHvVRkITD_DS5Nwdmpwt_mXeqRDEg9O6Vd_tMz_hzcOoiSILieB83P_PUpOLnoIAGvJcAuejkhMAQOJneSvrFeeyutr_dxVWkQ=w1440)

进展来之不易，且进展缓慢。要理解个中缘由，可以想想新冠病毒。这类冠状病毒表面只有一种刺突蛋白需要疫苗瞄准；而据 Higgins 所说，疟原虫却有成百上千种表面蛋白。而且它还是一个难以捉摸的变形高手。

至关重要的是，研发含有能干扰感染的关键成分的疫苗，需要了解一种配子表面蛋白——Pfs48/45——的分子结构，该蛋白对寄生虫在蚊子中肠内的发育至关重要。Higgins 和他的团队正是在这里陷入了僵局。多年来，他们尝试破译这种蛋白的形状，但收效有限。即便动用解析蛋白结构最强大的两种实验技术——X 射线晶体学和冷冻电子显微镜——研究者也只能获得模糊的低分辨率图像。结果，他们构建的 Pfs48/45 结构模型必然是不完善、不完整的。

直到 AlphaFold 的到来。

"我们跟这个问题缠斗了好几年，努力获取我们需要的细节，"Higgins 说。"然后我们把 AlphaFold 加入进来。当我们把我们的模型与 AlphaFold 预测的结构结合起来时，我们突然就能看清整个系统是如何运作的了。"Higgins 回忆起他的博士生 [Kuang-Ting Ko](https://higginslab.web.ox.ac.uk/kuang-ting-ko)——"他之前尝试了各种不同的办法来改进实验图像"——冲进办公室报喜的那一激动时刻。

> AlphaFold 让我们把项目推进到了新的层次，从基础科学阶段进入了临床前与临床开发阶段。

Matthew Higgins

"那真是如释重负，"Higgins 说，这也是项目的转折点。繁琐的实验工作与 AI 预测相结合，很快便带来了 Pfs48/45 的清晰图景。"AlphaFold 提供的关键信息让我们得以决定想把蛋白的哪些部分放进疫苗，以及想如何组织这些蛋白，"Higgins 说。"AlphaFold 让我们把项目推进到了新的层次，从基础科学阶段进入了临床前与临床开发阶段。"

当然，AlphaFold 并非完美无缺。Higgins 指出，虽然这个 AI 系统在预测蛋白内部各个模块如何形成结构方面表现出色，但有时它的 3D 可视化会稍有偏差。要获得最准确、最可信的结果，最好把 AlphaFold 与冷冻电子显微镜等更传统的工具结合使用，他说。"我相信 AlphaFold 的预测会越来越好。但就目前而言，把实验知识与 AlphaFold 模型相结合是最优做法，因为它能让我们把所有信息拼合到一起。我们许多项目都采取这一路线。"

![一双手托着 Pfs48/45 疟疾蛋白的 3D 打印分子模型，其中橙色、蓝色和黄色部分代表不同的结构域。](https://lh3.googleusercontent.com/jsn_dAScr7xNND7mb7EfPiPGzXrefQy7q2PE2U1TXibJ--Qe2B2MM_1ya5_uwTnPuxW9Ke-xAPWAIifMUbLcBoK2kwUsOPl9tXoAmZnbKC_TDfk82g=w1440-h810-n-nu)

Higgins 的合作者 Sumi Biswas 教授将于 2023 年初开展 Pfs48/45 的人体临床试验。既然 Pfs48/45 的结构已被破解，Biswas 和 Higgins 两个团队便能携手理解这些疫苗接种试验中产生的免疫应答，并设计改进的疫苗。在研发一款作用于疟疾生命周期每个阶段的疫苗的征程中，Higgins 也在理解另一个目标上取得长足进展：一个大型蛋白复合物，它在疟原虫感染红血球、引发症状的阶段起关键作用。团队正结合 AlphaFold 与冷冻电镜，努力弄清这个复合物是如何拼合在一起的。

再看更远的将来，Higgins 设想 AlphaFold 成为从零开始创造全新有用蛋白质的关键技术，这一过程被称为从头蛋白质设计（de novo protein design）。"AlphaFold 的未来，可能不在于预测细胞中已经存在的分子，而在于预测人们为特定应用（例如疫苗）设计的分子的结构，"他说。"如果我们能够设计蛋白质，然后用 AlphaFold 预测它们是否会按我们需要的方式折叠，那将是非常强大的能力。"

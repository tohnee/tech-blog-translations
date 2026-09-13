---
title: "以全新方式探索纯数学之美"
title_en: "Exploring the beauty of pure mathematics in novel ways"
source: https://deepmind.google/blog/exploring-the-beauty-of-pure-mathematics-in-novel-ways/
site: deepmind
date: 2021-12-01
crawled: 2026-09-13
translated: 2026-09-13
---

# 以全新方式探索纯数学之美

> 原文：[Exploring the beauty of pure mathematics in novel ways](https://deepmind.google/blog/exploring-the-beauty-of-pure-mathematics-in-novel-ways/) · Google DeepMind

一个多世纪以前，[Srinivasa Ramanujan](https://en.wikipedia.org/wiki/Srinivasa_Ramanujan)（拉马努金）以其非凡的能力震撼了数学界——他能在数字中看到别人看不到的惊人模式。这位来自印度的自学成才的数学家把自己的洞察描述为深刻的直觉与灵性体验，这些模式常常在他生动的梦境中浮现。这些观察捕捉到了纯数学抽象世界中非凡的美与无尽的可能。近年来，我们已经开始看到 AI 在[涉及深度人类直觉的领域](https://deepmind.com/research/case-studies/alphago-the-story-so-far)取得突破，最近又在科学领域一些[最困难的问题](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology)上有所斩获，但直到现在，最新的 AI 技术尚未在纯数学研究中助力取得重要成果。

作为 [DeepMind「破解智能」使命](https://deepmind.com/about)的一部分，我们探索了机器学习（ML）识别数学结构与模式、帮助数学家走向他们原本可能永远无法发现的成果的潜力——首次证明 AI 能够在纯数学的前沿提供帮助。

[我们的研究论文](https://www.nature.com/articles/s41586-021-04086-x)今日发表于《自然》杂志，详细记录了我们与顶尖数学家的合作，将 AI 应用于纯数学两个领域的新发现：拓扑学与表示论。与悉尼大学的 [Geordie Williamson 教授](https://www.maths.usyd.edu.au/u/geordie/)合作，我们发现了一个关于置换的猜想的新公式，该猜想数十年来悬而未决。与牛津大学的 [Marc Lackenby 教授](https://www.maths.ox.ac.uk/people/marc.lackenby)和 [András Juhász 教授](https://www.maths.ox.ac.uk/people/andras.juhasz)合作，我们通过研究纽结的结构，发现了数学不同领域之间一个意想不到的联系。据审阅这项工作的顶尖数学家所说，这些是用机器学习取得的首批重要数学发现。我们还在 arXiv 上发布了与每个结果配套的完整论文，并将提交给合适的数学期刊（[置换论文](https://arxiv.org/abs/2111.15161)；[纽结论文](https://arxiv.org/abs/2111.15323)）。通过这些例子，我们提出了一个模型，说明其他数学家可以如何使用这些工具来取得新成果。

![一个由一根不断开的绳子构成的纽结动画。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d0dee2f1f82cd4b977c9_unnamed.gif)

纽结是低维拓扑学中的基本对象之一。它是一个嵌入在三维空间中的缠绕环。

![一列字母：A、B、C、D、E。这些字母经过置换 32415 重排后，得到第二列字母：D、B、A、C、E。](https://lh3.googleusercontent.com/KLNgTiUHc881rOm2g8vsQI8ZUfmEewAEMoYCxOXGImAx35hd2IginLaGn_N-u0oafwkdcrFSEtClnkmlXHaifdGOSqVMNVrrutTUodAw5EtLDbOVHw=w1440)

置换是有序列表的一种重排。置换「32415」把第 1 个元素放到第 3 个位置，第 2 个元素放到第 2 个位置，依此类推。

我们研究的两个基本对象是纽结和置换。

多年来，数学家一直用计算机生成数据以辅助模式搜索。这类研究被称为实验数学，催生了一些著名的猜想，例如 [Birch 和 Swinnerton-Dyer 猜想](https://theconversation.com/millennium-prize-the-birch-and-swinnerton-dyer-conjecture-4242)——六个[千禧年大奖难题](https://www.claymath.org/millennium-problems/millennium-prize-problems)之一，它们是数学界最著名的开放问题（每个都附带 100 万美元奖金）。虽然这种方法已经取得成功且相当普遍，但从这些数据中识别和发现模式，仍然主要依赖数学家本人。

在纯数学中，寻找模式变得愈发重要，因为如今生成的数据量已经超过任何数学家在有生之年所能合理研究的范围。某些值得研究的对象——比如那些具有数千个维度的对象——也实在太过深奥，无法直接推理。考虑到这些限制，我们相信 AI 能够以全新的方式增强数学家的洞察力。

> 这感觉就像伽利略拿起望远镜，得以凝视数据的深处，看到以前从未被探测到的事物。

Marcus Du Sautoy

牛津大学公众理解科学西蒙尼讲席教授、数学教授

我们的结果表明，机器学习可以补充数学研究：通过监督学习检测假想模式是否存在，并借助机器学习中的归因技术洞察这些模式，从而引导关于某个问题的直觉。

与 Williamson 教授合作，我们用 AI 帮助发现了表示论中一个长期存在的猜想的新研究路径。近 40 年来进展寥寥的[组合不变性猜想](https://dl.acm.org/doi/10.1016/j.jcta.2005.12.003)断言，某些有向图与多项式之间应当存在一种关系。利用机器学习技术，我们得以确信这种关系确实存在，并识别出它可能与被称为「破损二面区间」（broken dihedral intervals）和「极端反射」（extremal reflections）的结构有关。有了这些知识，Williamson 教授得以猜想出一个惊人而优美的算法，可以解决组合不变性猜想。我们已经在超过 300 万个例子上对该新算法进行了计算验证。

与 Lackenby 教授和 Juhász 教授合作，我们探索了纽结——拓扑学的基础研究对象之一。纽结不仅告诉我们一根绳子可以有多少种缠绕方式，还与量子场论和非欧几何有着出人意料的联系。代数、几何和量子理论都对纽结有着独特的视角，而一个长期存在的谜题是这些不同分支如何关联：例如，纽结的几何能告诉我们关于代数的什么信息？我们训练了一个机器学习模型来发现这样的模式，出人意料的是，它揭示出某个特定的代数量——符号差（signature）——与纽结的几何直接相关，这一点此前既不为人知，也未被现有理论预示。通过使用机器学习中的归因技术，我们引导 Lackenby 教授发现了一个新的量，我们称之为自然斜率（natural slope），它暗示了该结构中一个此前被忽视的重要方面。随后我们一起证明了这一关系的确切性质，建立了这些数学分支之间最早的一批联系。

![一幅手绘的多彩数学图形，表示表示论中的一张有向图：节点标以置换记号，边以多种颜色突出显示，并指向代数表达式「1 + q」。](https://lh3.googleusercontent.com/GN9MgcwVWKG5Ki_Vi2Jjzq7aWO0KhGhyFJ9x0skx3btY34EEuLd3v47DtYEBxjs8OyARrei6G74ykckLhi2cGtJga6zpl5445CHRkHfj31bJeGjl0A=w1440)

![一幅手绘数学图，表示表示论中的一张有向图：节点标以置换记号，细黑连线之间以蓝色、黄色、橙色、红色和青绿色的粗路径突出显示。](https://lh3.googleusercontent.com/mNIhRnUSSUDSD-MHHHH_aPgjYtwMR4VMJnn0ZirNyZJnHzI-Jqbj2Kx8miqCHoQmCPDZ32Rv_wKR87tv4BXwJ8yuviBq8sFnTGZ-DuJj3J4EVk9u6pI=w1440)

我们研究了机器学习能否揭示不同数学对象之间的关系。图中展示的是两个「Bruhat 区间」及其相关的「Kazhdan-Lusztig 多项式」——表示论中的两个基本对象。Bruhat 区间是一种图，表示仅通过每次交换两个对象，把一组对象的顺序反转的所有不同方式。KL 多项式则告诉数学家一些关于这种图在高维空间中存在方式的深刻而精微的信息。只有当 Bruhat 区间拥有数百或数千个顶点时，有趣的结构才开始显现。

![一张数学散点图，展示纽结的代数「符号差」（Signature，y 轴）与其几何「经向平移（实部）」（Meridional translation (real)，x 轴）之间的关系，数据点按其「纬向平移」（Longitudinal translation）值以从蓝到红的渐变色着色。](https://lh3.googleusercontent.com/B-LCwTQYk6R-o7WA5V-b6r8jCtSBjahM1UqNzpkyDvLiu3eq9SXPxQPAjJEJSzDp6zMoUjFeiAgimNqz3kWm-NM14ypwppmVE0AGNjFceLyHuQVp=w1440)

我们的模型凸显了此前未被发现的结构，并引导我们取得了令人惊喜的新数学成果。图中展示的是纽结的几何与符号差之间一个引人注目的关系。纽结的几何与它的形状有关（例如其体积），需以规范的方式测量。符号差则是一个代数不变量，可以通过观察纽结自身交叉和扭转的方式来计算。

学习技术与 AI 系统的运用，为数学中模式的识别与发现带来了巨大希望。即使某些类型的模式仍然令现代机器学习束手无策，我们希望[我们的《自然》论文](https://www.nature.com/articles/s41586-021-04086-x)能激励其他研究者考虑 AI 作为纯数学中有用工具的潜力。任何想要复现结果的人都可以访问我们的[交互式 notebook](https://github.com/deepmind/mathematics_conjectures)。回想起 Ramanujan 那令人惊叹的头脑，[George Frederick James Temple](https://mathshistory.st-andrews.ac.uk/Biographies/Temple/) 曾写道：「数学的伟大进步不是靠逻辑，而是靠创造性想象。」我们期待与数学家们合作，见证 AI 如何进一步把人类直觉之美提升到新的创造力高度。

**附注**

这项工作由一个团队完成，贡献者包括 Alex Davies、Petar Veličković、Lars Buesing、Sam Blackwell、Daniel Zheng、Nenad Tomašev、Richard Tanburn、Peter Battaglia、Charles Blundell、Xavier Glorot、Matt Overlan、Alyssa Pierce、Natalie Lambert、George Holland、Razia Ahamed、Clemens Meyer、Demis Hassabis 和 Pushmeet Kohli。我们还要感谢 Jan Vonk 和 Jordan Ellenberg 提供额外的数学方面的意见。

---
title: "第三版有什么新内容"
title_en: "What’s New in the 3rd Edition"
source: https://sebastianraschka.com/blog/2019/whats-new-in-the-3rd-edition.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 第三版有什么新内容

> 原文：[What’s New in the 3rd Edition](https://sebastianraschka.com/blog/2019/whats-new-in-the-3rd-edition.html)

这个项目最初只是夏天开始的一个小型副业，最终却演变成一个比我们所有人最初预想都要庞大得多的工程。我很高兴地宣布：《Python Machine Learning》（《Python 机器学习》）第三版[终于上市](https://www.amazon.com/Python-Machine-Learning-scikit-learn-TensorFlow/dp/1789955750/ref=sr_1_1?keywords=sebastian+raschka&qid=1576203320&sr=8-1)了！没错，好事成三！ :)

![第三版有什么新内容 截图 1](https://sebastianraschka.com/images/blog/2019/whats-new-in-the-3rd-edition/screenshot-1.webp)

我也非常渴望向大家详细介绍这一新版中的新增内容。不过，学期即将结束，考试周也随之而来——它往往与各种论文截止日期撞在一起，大概是一年中最无趣的一周。因此，我必须尽量写得简短些，但这或许并不是坏事！

*\*新增了什么？！*

许多读者和学生告诉我们，他们非常喜欢前 12 章——作为机器学习与 Python 科学计算栈的全面入门，这些章节广受好评。为了让这些章节保持与时俱进，我们回头将它们更新到了最新版本的 NumPy、SciPy、pandas、matplotlib 和 scikit-learn（v0.22）。此外，这些年我一直记录读者提出的各种问题，并据此修改了那些表述含糊、难以阅读或有误导性的句子和段落。如果你读过第二版，可能不会察觉到明显变化，因为内容上只有少量增补（比如有读者已经指出的 ColumnTransformer :)）。

今年深度学习领域的一件大事是 TensorFlow 2.0 的发布。因此，所有与 TensorFlow 相关的深度学习章节（第 13–16 章）都进行了大改版。由于 TensorFlow 2.0 引入了许多新特性和根本性变化，我们从零重写了这些章节。此外，我们还新增了关于生成对抗网络（Generative Adversarial Networks，GAN）的全新一章——它是深度学习研究中最热门的话题之一。

首篇 GAN 论文发表仅两年之后，我们才开始编写第二版。当时我们并不确定 GAN 是否会一直保持重要且相关的地位。然而毫无疑问，GAN 已经发展成为最热门、应用最广泛的深度学习技术之一。人们用它创作艺术品、为照片上色并提升照片质量，甚至连电子游戏模组（mod）社区也用 GAN 以更高分辨率重建老游戏的贴图。如今，各个科研领域都在使用 GAN；例如，宇宙学家用 GAN 生成引力透镜效应，以研究暗物质对宇宙的影响。不言而喻，GAN 的入门内容早就该补上了。

如果你读过前一版，也许还记得第一章里的下面这幅图：

![第三版有什么新内容 第 1 章](https://sebastianraschka.com/images/blog/2019/whats-new-in-the-3rd-edition/ch1.webp)

在第一章中，我们提到了机器学习常见的“三大子类”：无监督机器学习、监督机器学习和强化学习。不过，前两版的读者也许还记得，我们总是以“超出本书范围”为由解释为什么没有强化学习章节。现在不再如此了！根据读者的大量请求，我们非常激动地宣布：我们撰写了一篇较为全面的强化学习入门（它只是基础入门，但比前几版足足多出了 50 页的强化学习内容 ;)）。

![第三版有什么新内容 第 18 章 1](https://sebastianraschka.com/images/blog/2019/whats-new-in-the-3rd-edition/ch18-1.webp)

近年来，强化学习受到了极大的关注。得益于 DeepMind 的 AlphaGo 和 AlphaGo Zero 等令人惊叹的项目——它们在围棋这一策略棋类游戏中击败了世界顶尖棋手——强化学习获得了非常广泛的新闻报道。而就在不久前，强化学习还被用于在即时战略游戏《星际争霸 II》中与世界顶级电竞选手对战。相信很多人已经在新闻中听闻过强化学习的这些成就，我们希望新的章节能为这个令人兴奋的领域提供通俗易懂且实用的入门介绍。

PS：一如既往，所有代码示例都可以在 GitHub 上找到：<https://github.com/rasbt/python-machine-learning-book-3rd-edition>。

---
title: "What’s New in the 3rd Edition"
source: https://sebastianraschka.com/blog/2019/whats-new-in-the-3rd-edition.html
crawled: 2026-09-06
---

# What’s New in the 3rd Edition

What started as a minor side-project in summer turned into a more significant project than all of us initially anticipated. And I am excited to announce that the third edition of Python Machine Learning [is finally out](https://www.amazon.com/Python-Machine-Learning-scikit-learn-TensorFlow/dp/1789955750/ref=sr_1_1?keywords=sebastian+raschka&qid=1576203320&sr=8-1)! Yes, all good things come in threes! :)

![Whats new in the 3rd edition screenshot 1](https://sebastianraschka.com/images/blog/2019/whats-new-in-the-3rd-edition/screenshot-1.webp)

I am also really eager to tell you more about the additions we made to this new edition. However, we are also approaching the end of the semester, and final’s week, which tends to coincide with various paper deadlines, and it is probably the least fun week of the year. Hence, I need to keep it relatively short, but that’s probably not a bad thing!

*\*What’s new?!*

Many readers and students told us how much they love the first 12 chapters as a comprehensive introduction to machine learning and Python’s scientific computing stack. To keep these chapters relevant, we went back and updated these chapters to support the latest versions of NumPy, SciPy, pandas, matplotlib, and scikit-learn (v0.22). Also, I kept a tab on all the readers’ questions I received over the years, which I used to refine sentences and paragraphs sections that were ambiguous, hard to read, or misleading. If you read the second edition, you probably won’t notice any apparent changes as there are only minor content additions (like the ColumnTransformer as one reader already pointed out :)).

One of the major Deep Learning-related events this year was the release of TensorFlow 2.0. Consequently, all the TensorFlow-related deep learning chapters (13-16) received a big overhaul. Since TensorFlow 2.0 introduced many new features and fundamental changes, we rewrote these chapters from scratch. Furthermore, we added a brand-new chapter on Generative Adversarial Networks, which are one of the hottest topics in deep learning research.

The first GAN paper just came up two years before we started working on the second edition. At that time, we weren’t sure whether GANs would stay an essential and relevant topic. However, without a doubt, GANs have evolved into one of the hottest and most widely used deep learning techniques. People use it for creating artwork and colorizing and improving the quality of photos. Even the video game modding communities picked up on GANs to recreate textures of old video games in higher resolutions. Nowadays, various scientific research areas make use of GANs; for example, cosmologists use GANs for the generation of gravitational lensing effects for studying the effects of dark matter in the universe, for example. I think it goes without speaking that an introduction to GANs was long overdue.

If you read the previous edition, you may remember the following figure from the first chapter:

![Whats new in the 3rd edition ch1](https://sebastianraschka.com/images/blog/2019/whats-new-in-the-3rd-edition/ch1.webp)

In this first chapter, we mentioned the major or common “three subcategories of machine learning:” unsupervised machine learning, supervised machine learning, and reinforcement learning. However, readers of the first two editions may remember that we always excused the lack of a reinforcement learning chapter as “out of the scope.” Not anymore! Based on the many requests we have received from readers, we are very excited to announce that we wrote a relatively comprehensive introduction to reinforcement learning (it’s a basic introduction, but it’s also 50 more pages of reinforcement learning than in previous editions ;)).

![Whats new in the 3rd edition ch18 1](https://sebastianraschka.com/images/blog/2019/whats-new-in-the-3rd-edition/ch18-1.webp)

In recent years, reinforcement learning has received a massive boost in attention. Thanks to impressive projects such as DeepMind’s AlphaGo and AlphaGo Zero, which beat the world’s best players in the strategy board game Go, reinforcement learning received very extensive news coverage. And just recently, reinforcement learning has been used to compete with the world’s top e-sports players in the real-time strategy video game StarCraft II. The chances are that many people have heard of these achievements of reinforcement learning in the news by now, and we hope that our new chapters can provide an accessible and practical introduction to this exciting field.

PS: As always, you can find all code examples on GitHub: <https://github.com/rasbt/python-machine-learning-book-3rd-edition>.

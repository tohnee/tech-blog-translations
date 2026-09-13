---
title: "AlphaGo Zero：从零开始"
title_en: "AlphaGo Zero: Starting from scratch"
source: https://deepmind.google/blog/alphago-zero-starting-from-scratch/
site: deepmind
date: 2017-10-18
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaGo Zero：从零开始

> 原文：[AlphaGo Zero: Starting from scratch](https://deepmind.google/blog/alphago-zero-starting-from-scratch/) · Google DeepMind

人工智能研究已经在从语音识别、图像分类到基因组学和药物发现的广泛领域中取得了快速进展。在许多情况下，这些是利用了大量人类专业知识和数据的专用系统。

然而，对某些问题而言，这些人类知识可能过于昂贵、过于不可靠，或者根本不存在。因此，AI 研究一个长期的抱负就是绕过这一步，创造出在最具挑战性的领域中无需任何人类输入即可达到超人表现的算法。在我们发表于《自然》（[Nature](https://www.nature.com/)）期刊的[最新论文](https://www.nature.com/articles/nature24270)中，我们展示了朝这一目标迈出的重要一步。

这篇论文介绍了 [AlphaGo](https://deepmind.com/research/alphago/) 的最新演进版本 AlphaGo Zero。AlphaGo 是第一个在古老的围棋运动中击败世界冠军的计算机程序，而 Zero 甚至更为强大，可以说是历史上最强的围棋棋手。

此前版本的 AlphaGo 最初是通过学习数千盘人类业余与职业对局来掌握围棋的。AlphaGo Zero 跳过了这一步，仅通过与自己对弈来学习下棋，从完全随机的走子起步。在此过程中，它迅速超越了人类的对弈水平，并以 100 比 0 的比分击败了此前[发表过的](http://www.nature.com/nature/journal/v529/n7587/full/nature16961.html?foxtrotcallback=true)击败世界冠军的 AlphaGo 版本。

![折线图，展示 40 天内各 AlphaGo 版本的 Elo 等级分对比，并用虚线标出 AlphaGo Lee（约 3500 Elo）和 AlphaGo Master（约 4750 Elo）的基线。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62266dad5dd02443ba577b4e_unnamed.gif)

它之所以能做到这一点，靠的是一种新颖的[强化学习](https://en.wikipedia.org/wiki/Reinforcement_learning)形式：AlphaGo Zero 成为自己的老师。这个系统一开始只有一个对围棋一无所知的神经网络。然后，它把这个神经网络与强大的搜索算法相结合，与自己对弈。随着对局的进行，神经网络被不断调整和更新，用以预测走子和每盘棋的最终胜者。

这个更新后的神经网络随后会与搜索算法重新结合，产生一个更强的新版本 AlphaGo Zero，然后整个过程重新开始。在每次迭代中，系统的性能都会小幅提升，自我博弈对局的质量也随之提高，从而造就越来越准确的神经网络和越来越强的 AlphaGo Zero 版本。

这一技术比以往版本的 AlphaGo 更强大，因为它不再受人类知识极限的束缚。相反，它能够白纸起步（tabula rasa），向世界上最强的棋手学习：AlphaGo 本身。
它还在其他一些值得注意的方面与此前的版本有所不同。

- AlphaGo Zero 只使用围棋盘上的黑白棋子作为输入，而此前版本的 AlphaGo 还包含少量人工设计的特征。
- 它只使用一个神经网络，而不是两个。早期版本的 AlphaGo 使用一个「策略网络（policy network）」来选择下一步怎么走，再用一个「价值网络（value network）」从每个局面预测对局的胜者。这两者在 AlphaGo Zero 中被合而为一，使其能够被更高效地训练和评估。
- AlphaGo Zero 不使用「rollouts（快速推演）」——其他围棋程序用来从当前棋盘局面预测哪位棋手会获胜的快速随机对局。相反，它依靠自身高质量的神经网络来评估局面。

所有这些差异都有助于提升系统的性能，并使其更具通用性。但真正让系统强大、高效得多的，是算法层面的改变。

![柱状图，对比各 AlphaGo 版本的功耗（TDP）：从 AlphaGo Fan（176 块 GPU，TDP 超过 40000）和 AlphaGo Lee（48 块 TPU，TDP 约 10000）大幅下降到 AlphaGo Master（4 块 TPU）和 AlphaGo Zero（4 块 TPU），后两者所需功耗极低。](https://lh3.googleusercontent.com/QFTNOIvGY2KRrSUlpDXrX1mt5IKUOyMhPaBFjgA6uLsEYklpR1O758s8Se7-RU-KEW2WuKvhdxojmLGCf359C60TvyhmVmBqB39yGGpEqiWGIF-Nfg=w1440)

得益于硬件的进步，以及近来的算法进展，AlphaGo 的能效不断攀升

仅仅经过三天的自我博弈训练，AlphaGo Zero 就以 100 比 0 干净利落地击败了此前[发表过的 AlphaGo 版本](https://ai.googleblog.com/2016/01/alphago-mastering-ancient-game-of-go.html)——后者曾[击败 18 次世界冠军得主李世石（Lee Sedol）](https://deepmind.com/alphago-korea)。经过 40 天的自我训练，AlphaGo Zero 变得更加强大，超越了被称为「Master（大师）」的 AlphaGo 版本，该版本曾击败世界顶尖棋手以及[世界排名第一的柯洁（Ke Jie）](https://deepmind.com/alphago-china)。

![柱状图，对比不同围棋程序的 Elo 等级分：Crazy Stone（约 1900）、AlphaGo Fan（约 3100）、AlphaGo Lee（约 3700）、AlphaGo Master（约 4800），以及以超过 5000 的最高等级分夺魁的 AlphaGo Zero。](https://lh3.googleusercontent.com/yq94Hk34eZy1mCKyTDtIkGeMyUD0Y2_-hfrFL3gS6GHFVfrJTZvkcsxt7kFWfo6NPGaYFe10FPydtNo9KTK_qbZW4W_Pnb6kSJlAidezrgU_M6zvmA8=w1440)

Elo 等级分——衡量围棋等竞技对弈中棋手相对水平高低的指标——展示了 AlphaGo 在发展过程中如何日益强大

在数百万盘 AlphaGo 对阵 AlphaGo 的对局过程中，该系统从零开始逐步学会围棋，在短短几天内就积累了数千年的围棋知识。AlphaGo Zero 还发现了新的知识，发展出非同寻常的策略和富有创造性的新招法，这些招法与它在对抗李世石和柯洁的对局中弈出的新颖手段遥相呼应，甚至更胜一筹。

![柱状图，对比不同围棋程序的 Elo 等级分，展示 AlphaGo Zero 以超过 5000 的最高等级分登顶。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62266eee4bfb80301e18f60b_Games.gif)

这些创造性的时刻让我们确信，AI 将成为人类智慧的放大器，帮助我们完成[我们的使命](https://deepmind.com/about/)——解决人类面临的一些最重要的挑战。

虽然现在还为时尚早，但 AlphaGo Zero 构成了朝这一目标迈出的关键一步。如果类似的技术能够应用于其他结构化问题，例如蛋白质折叠、降低能耗或寻找革命性的新材料，由此产生的突破有望对社会产生积极影响。

**说明**

阅读[论文](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ)

阅读配套的 [Nature News and Views 文章](https://www.nature.com/articles/550336a.epdf?shared_access_token=QbXlOw9nSIP_MS1moc_M0tRgN0jAjWel9jnR3ZoTv0PvinEKRXS2Dk736vL8i-Uo2-6AN8KRxOlLhDGorUgFzEgC3fwrX95r3LQ7u2FBwQ5axjmpMSZrWg4i6D7_g5rV5ze0zLhgo4jufsSKL-UZmw%3D%3D)

下载 [AlphaGo Zero 对局棋谱](https://www.alphago-games.com/)

阅读[更多关于 AlphaGo 的内容](https://deepmind.com/research/case-studies/alphago-the-story-so-far)

这项工作由 David Silver、Julian Schrittwieser、Karen Simonyan、Ioannis Antonoglou、Aja Huang、Arthur Guez、Thomas Hubert、Lucas Baker、Matthew Lai、Adrian Bolton、Yutian Chen、Timothy Lillicrap、Fan Hui、Laurent Sifre、George van den Driessche、Thore Graepel 和 Demis Hassabis 完成。

---
title: "面向 Sim2Real 迁移的域随机化"
title_en: "Domain Randomization for Sim2Real Transfer"
source: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/
crawled: 2026-09-08
translated: 2026-09-08
---

# 面向 Sim2Real 迁移的域随机化

> 原文：[Domain Randomization for Sim2Real Transfer](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/) · Lilian Weng（翁荔）

> 如果一个模型或策略主要在模拟器中训练、却要在真实机器人上工作，它必然会面对 sim2real 差距（reality gap）。*域随机化（Domain Randomization，DR）*是一个简单而强大的想法：通过随机化训练环境的属性来弥合这一差距。

在机器人学中，最难的问题之一是如何让模型迁移到现实世界。由于深度 RL 算法的样本效率低下、在真实机器人上收集数据的成本高昂，我们常常需要在模拟器中训练模型——理论上模拟器能提供无限量的数据。然而，模拟器与物理世界之间的现实差距（reality gap）常导致在物理机器人上失败。差距源于物理参数（如摩擦、kp、阻尼、质量、密度）的不一致，更致命的是不正确的物理建模（如软表面之间的碰撞）。

要弥合 sim2real 差距，我们需要改进模拟器使其更接近现实。有几条途径：

- **系统辨识（System identification）**
    - *系统辨识*是为物理系统建立数学模型；在 RL 语境中，数学模型就是模拟器。要让模拟器更真实，精心的校准必不可少。
    - 遗憾的是，校准很昂贵。而且同一台机器的许多物理参数可能因温度、湿度、摆放位置或随时间的磨损而发生显著变化。
- **域适应（Domain adaptation）**
    - *域适应（DA）*指一组迁移学习技术，通过任务模型施加的映射或正则化来更新模拟中的数据分布以匹配真实分布。
    - 许多 DA 模型，特别是图像分类或端到端基于图像的 RL 任务的模型，建立在对抗损失或 [GAN](https://lilianweng.github.io/posts/2017-08-20-gan/) 之上。
- **域随机化（Domain randomization）**
    - 借助*域随机化（DR）*，我们能够创建一系列属性随机化的模拟环境，并训练一个在所有环境中都能工作的模型。
    - 这个模型很可能能适应真实世界环境，因为真实系统被期望是训练变化丰富分布中的一个样本。

DA 与 DR 都是无监督的。与需要相当数量真实数据样本来捕捉分布的 DA 相比，DR 可能*只需要很少或完全不需要*真实数据。DR 是本文的重点。

![Approaches for sim2real transfer](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/sim2real-transfer.png)

*图 1：三种 sim2real 迁移途径的概念示意图。*

## 什么是域随机化？

为使定义更一般，把我们能完全访问的环境（如模拟器）称为**源域（source domain）**，把我们想把模型迁移到的环境称为**目标域（target domain）**（如物理世界）。训练发生在源域。我们可以在源域 $$e_\xi$$ 中控制一组 $$N$$ 个随机化参数，配置 $$\xi$$ 从随机化空间采样，$$\xi \in \Xi \subset \mathbb{R}^N$$。

策略训练期间，从施加了随机化的源域收集情节。于是策略暴露于多样的环境并学会泛化。策略参数 $$\theta$$ 的训练目标是最大化配置分布上平均的期望奖励 $$R(.)$$：

$$
\theta^* = \arg\max_\theta \mathbb{E}_{\xi \sim \Xi} [\mathbb{E}_{\pi_\theta, \tau \sim e_\xi} [R(\tau)]]
$$

其中 $$\tau_\xi$$ 是在以 $$\xi$$ 随机化的源域中收集的轨迹。在某种意义上，*"源域与目标域之间的差异被建模为源域中的可变性。"*（引自 [Peng et al. 2018](https://arxiv.org/abs/1710.06537)）

## 均匀域随机化

在 DR 的原始形式（[Tobin et al, 2017](https://arxiv.org/abs/1703.06907)；[Sadeghi et al. 2016](https://arxiv.org/pdf/1611.04201.pdf)）中，每个随机化参数 $$\xi_i$$ 被限制在一个区间内，$$\xi_i \in [\xi_i^\text{low}, \xi_i^\text{high}], i=1,\dots,N$$，每个参数在该范围内均匀采样。

随机化参数可以控制场景的外观，包括但不限于以下内容（见图 2）。在模拟且随机化的图像上训练的模型能够迁移到真实的非随机化图像。
- 物体的位置、形状和颜色，
- 材质纹理，
- 光照条件，
- 图像上添加的随机噪声，
- 模拟器中相机的位置、朝向和视场。

![Domain Randomization](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/DR.png)

*图 2：训练环境中捕捉的图像被随机化。（图片来源：[Tobin et al, 2017](https://arxiv.org/abs/1703.06907)）*

模拟器中的物理动力学也可以随机化（[Peng et al. 2018](https://arxiv.org/abs/1710.06537)）。研究表明，一个*循环*（recurrent）策略能适应不同的物理动力学，包括部分可观测的现实。一组物理动力学特征包括但不限于：
- 物体的质量和尺寸，
- 机器人身体的质量和尺寸，
- 关节的阻尼、kp、摩擦，
- PID 控制器的增益（P 项），
- 关节极限，
- 动作延迟，
- 观测噪声。

凭借视觉与动力学 DR，在 OpenAI Robotics，我们学到了一个能在真实灵巧机器人手上工作的策略（[OpenAI, 2018](https://arxiv.org/abs/1808.00177)）。我们的操作任务是教机器人手持续旋转一个物体以连续达成 50 个随机目标姿态。该任务的 sim2real 差距非常大，原因在于 (a) 机器人与物体之间同时存在大量接触，(b) 物体碰撞等运动的模拟不完美。起初，策略不丢物体几乎撑不过 5 秒。但在 DR 的帮助下，策略最终演化到在现实中出奇地好用。

<iframe width="560" height="315" src="https://www.youtube.com/embed/DKe8FumoD4E" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 域随机化为什么有效？

现在你可能会问，域随机化为什么这么有效？这想法听起来真的很简单。以下是我觉得最有说服力的两个非互斥解释。

### DR 作为优化

一种观点（[Vuong, et al, 2019](https://arxiv.org/abs/1903.11774)）是把 DR 中学习随机化参数视为*双层优化（bilevel optimization）*。假设我们能访问真实环境 $$e_\text{real}$$，随机化配置从由 $$\phi$$ 参数化的分布中采样，$$\xi \sim P_\phi(\xi)$$，我们想学习一个分布，在其上训练的策略 $$\pi_\theta$$ 能在 $$e_\text{real}$$ 中取得最大性能：

$$
\begin{aligned}
&\phi^* = \arg\min_{\phi} \mathcal{L}(\pi_{\theta^*(\phi)}; e_\text{real}) \\
\text{where } &\theta^*(\phi) = \arg\min_\theta \mathbb{E}_{\xi \sim P_\phi(\xi)}[\mathcal{L}(\pi_\theta; e_\xi)]
\end{aligned}
$$

其中 $$\mathcal{L}(\pi; e)$$ 是策略 $$\pi$$ 在环境 $$e$$ 中评估的损失函数。

尽管均匀 DR 中随机化范围是手工挑选的，它通常涉及领域知识以及基于迁移性能的多轮试错调整。本质上这是对 $$\phi$$ 的人工优化过程，以获得最优的 $$\mathcal{L}(\pi_{\theta^*(\phi)}; e_\text{real})$$。

下一节的引导式域随机化很大程度上受这一观点启发，旨在自动做双层优化、学习最佳参数分布。

### DR 作为元学习

在我们的学习灵巧操作项目（[OpenAI, 2018](https://arxiv.org/abs/1808.00177)）中，我们训练了一个跨不同环境动力学泛化的 LSTM 策略。我们观察到：一旦机器人完成了第一次旋转，后续成功所需的时间短得多。同时，没有记忆的前馈（FF）策略被证明无法迁移到物理机器人。两者都是策略动态学习并适应新环境的证据。

在某些方面，域随机化组合出一系列不同的任务。循环网络中的记忆赋予策略跨任务的[*元学习*](https://lilianweng.github.io/posts/2018-11-30-meta-learning/)能力，并进一步作用于真实世界设定。

## 引导式域随机化

朴素 DR 假设无法访问真实数据，因此随机化配置在模拟中尽可能宽泛、均匀地采样，寄希望于真实环境能被这一宽分布覆盖。有理由想一种更精细的策略——用*任务性能*、*真实数据*或*模拟器*的引导来替代均匀采样。

引导式 DR 的一个动机是通过避免在不现实的环境中训练模型来节省计算资源。另一个是避免因随机化分布过宽而出现不可行的解、从而阻碍策略成功学习。

### 面向任务性能的优化

设我们用不同的随机化参数 $$\xi \sim P_\phi(\xi)$$ 训练一族策略，其中 $$P_\xi$$ 是由 $$\phi$$ 参数化的 $$\xi$$ 的分布。之后我们决定把每一个都在目标域的下游任务上尝试（如在现实中控制机器人或在验证集上评估）以收集反馈。反馈告诉我们配置 $$\xi$$ 有多好，为优化 $$\phi$$ 提供信号。

<a name="AutoAugment" />受 [NAS](https://ai.google/research/pubs/pub45826) 启发，**AutoAugment**（[Cubuk, et al. 2018](https://arxiv.org/abs/1805.09501)）把为图像分类学习最佳数据增强操作（如剪切、旋转、反色等）的问题框定为 RL 问题。注意 AutoAugment 不是为 sim2real 迁移提出的，但属于按任务性能引导的 DR。单个增强配置在评估集上测试，性能提升被用作训练 PPO 策略的奖励。该策略为不同数据集输出不同的增强策略；例如，对 CIFAR-10，AutoAugment 主要挑选基于颜色的变换，而 ImageNet 偏好基于几何的变换。

[Ruiz (2019)](https://arxiv.org/abs/1810.02513) 把*任务反馈*当作 RL 问题中的*奖励*，提出了一种基于 RL 的方法"learning to simulate"来调整 $$\xi$$。训练一个策略来预测 $$\xi$$，用主任务验证数据上的性能度量作为奖励，奖励被建模为多维高斯。总体思想与 AutoAugment 类似，把 NAS 应用于数据生成。根据他们的实验，即使主任务模型未收敛，它仍能为数据生成策略提供合理的信号。

![Learning to simulate](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/learning-to-simulate.png)

*图 3："learning to simulate" 方法概览。（图片来源：[Ruiz (2019)](https://arxiv.org/abs/1810.02513)）*

进化算法是另一条路，*反馈*被当作引导进化的*适应度*（[Yu et al, 2019](https://openreview.net/forum?id=H1g6osRcFQ)）。该研究中，他们使用 [CMA-ES](https://en.wikipedia.org/wiki/CMA-ES)（协方差矩阵自适应进化策略），适应度是 $$\xi$$ 条件策略在目标环境中的性能。附录中，他们比较了 CMA-ES 与其他建模 $$\xi$$ 动态的方式，包括贝叶斯优化或神经网络。主要结论是这些方法不如 CMA-ES 稳定或样本高效。有趣的是，当把 $$P(\xi)$$ 建模为神经网络时，LSTM 明显优于 FF。

有人认为 sim2real 差距是外观差距与内容差距的组合；即大多数受 GAN 启发的 DA 模型关注外观差距。**Meta-Sim**（[Kar, et al. 2019](https://arxiv.org/abs/1904.11621)）旨在通过生成任务专属的合成数据集来弥合内容差距。Meta-Sim 以自动驾驶训练为例，因此场景可能非常复杂。此例中，合成场景由带属性（如位置、颜色）的对象层级以及对象间关系参数化。该层级由类似结构化域随机化（**SDR**；[Prakash et al., 2018](https://arxiv.org/abs/1810.10093)）的概率场景文法指定，并被假定预先已知。训练模型 $$G$$ 按如下步骤增强场景属性 $$s$$ 的分布：

1. 先学先验：预训练 $$G$$ 学恒等函数 $$G(s) = s$$。
2. 最小化真实与模拟数据分布之间的 MMD 损失。这涉及经过不可微渲染器的反向传播。论文通过对 $$G(s)$$ 的属性施加扰动来数值计算。
3. 在合成数据上训练、真实数据上评估时，最小化 REINFORCE 任务损失。同样，与 AutoAugment 非常相似。

遗憾的是，这一族方法并不适合 sim2real 场景。RL 策略或 EA 模型都需要大量真实样本。而在物理机器人上纳入实时反馈收集到训练循环中非常昂贵。是否愿意用真实数据收集换取更少的计算资源取决于你的任务。

### 匹配真实数据分布

用真实数据引导域随机化感觉很像做系统辨识或 DA。DA 背后的核心思想是改进合成数据以匹配真实数据分布。在真实数据引导的 DR 中，我们想学习使模拟器中状态分布接近真实世界状态分布的随机化参数 $$\xi$$。

**SimOpt** 模型（[Chebotar et al, 2019](https://arxiv.org/abs/1810.05687)）先在初始随机化分布 $$P_\phi(\xi)$$ 下训练得到策略 $$\pi_{\theta, P_\phi}$$。然后该策略被同时部署在模拟器和物理机器人上，分别收集轨迹 $$\tau_\xi$$ 和 $$\tau_\text{real}$$。优化目标是最小化模拟与真实轨迹之间的差异：

$$
\phi^* = \arg\min_{\phi}\mathbb{E}_{\xi \sim P_\phi(\xi)} [\mathbb{E}_{\pi_{\theta, P_\phi}} [D(\tau_\text{sim}, \tau_\text{real})]]
$$

其中 $$D(.)$$ 是基于轨迹的差异度量。与 "Learning to simulate" 论文一样，SimOpt 也必须解决如何让梯度穿过不可微模拟器的棘手问题。它用了一种叫[相对熵策略搜索](https://www.aaai.org/ocs/index.php/AAAI/AAAI10/paper/viewFile/1851/2264)的方法，详见论文。

![SimOpt](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/simopt.png)

*图 4：SimOpt 框架概览。（图片来源：[Chebotar et al, 2019](https://arxiv.org/abs/1810.05687)）*

**RCAN**（[James et al., 2019](https://arxiv.org/abs/1812.07252)）是 "Randomized-to-Canonical Adaptation Networks" 的缩写，是 DA 与 DR 用于端到端 RL 任务的一个漂亮组合。在模拟中训练一个图像条件 GAN（[cGAN](https://arxiv.org/abs/1611.07004)），把域随机化图像翻译为非随机化版本（即"规范版本/canonical version"）。之后用同一模型把真实图像翻译为相应的模拟版本，使智能体消费与其训练中遇到的相一致的观测。当然，其底层假设依然是：域随机化模拟图像的分布足够宽，能覆盖真实世界样本。

![RCAN](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/RCAN.png)

*图 5：RCAN 是一个图像条件生成器，能把域随机化或真实图像转换成相应的非随机化模拟器版本。（图片来源：[James et al., 2019](https://arxiv.org/abs/1812.07252)）*

RL 模型在模拟器中端到端训练做基于视觉的机械臂抓取。每个时间步都施加随机化，包括托盘隔板位置、待抓取物体、随机纹理，以及光照的位置、方向和颜色。规范版本是模拟器的默认外观。RCAN 尝试学习一个生成器

$$G$$：随机化图像 $$\to$$ {规范图像, 分割, 深度}

其中分割掩码与深度图像用作辅助任务。与均匀 DR 相比，RCAN 有更好的零样本迁移，不过两者都被证明不如只在真实图像上训练的模型。概念上，RCAN 的运作方向与 [GraspGAN](https://arxiv.org/abs/1709.07857) 相反——后者通过域适应把合成图像翻译为真实图像。

### 由模拟器中的数据引导

网络驱动的域随机化（[Zakharov et al., 2019](https://arxiv.org/abs/1904.02750)），也称 **DeceptionNet**，动机是学习哪些随机化对弥合图像分类任务的域差距真正有用。

随机化通过一组带编码器-解码器架构的欺骗（deception）模块施加。欺骗模块专门设计用于变换图像，如更换背景、添加畸变、改变光照等。另一个识别网络通过对变换后图像做分类来处理主任务。

训练分两步：
1. 固定识别网络，在反向传播中施加反向梯度来*最大化预测与标签之间的差异*。这样欺骗模块能学到最令人困惑的变换。
2. 固定欺骗模块，用被改动过的输入图像训练识别网络。

![DeceptionNet](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/deception-net.png)

*图 6：DeceptionNet 的工作方式。（图片来源：[Zakharov et al., 2019](https://arxiv.org/abs/1904.02750)）*

训练欺骗模块的反馈由下游分类器提供。但与上文[面向任务性能优化的章节](#optimization-for-task-performance)试图最大化任务性能不同，这些随机化模块旨在制造更难的样本。一大缺点是你需要为不同数据集或任务手工设计不同的欺骗模块，难以扩展。鉴于它是零样本的，其结果在 MNIST 和 LineMOD 上仍不如 SOTA DA 方法。

类似地，主动域随机化（Active domain randomization，**ADR**；[Mehta et al., 2019](https://arxiv.org/abs/1904.04762)）也依赖模拟数据来创建更难的训练样本。ADR 在给定随机化范围内搜索*信息量最大*的环境变化，其中*信息量*以策略在随机化与参考（原始、非随机化）环境实例中 rollout 的差异来度量。听起来有点像 [SimOpt](#match-real-data-distribution)？注意 SimOpt 度量模拟与真实 rollout 之间的差异，而 ADR 度量随机化与非随机化模拟之间的差异，避免了昂贵的真实数据收集。

![ADR](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/ADR.png)

*图 7：主动域随机化（ADR）的工作方式。（图片来源：[Mehta et al., 2019](https://arxiv.org/abs/1904.04762)）*

确切地说，训练按如下进行：
1. 给定一个策略，在参考环境与随机化环境上分别运行，收集两组轨迹。
2. 训练一个判别器模型来判断一条 rollout 轨迹相对于参考运行是否被随机化。预测的 $$\log p$$（被随机化的概率）用作奖励。随机化与参考 rollout 差异越大，预测越容易，奖励越高。
    - 直觉是：若一个环境简单，同一策略智能体能产生与参考环境相似的轨迹。那么模型应当通过鼓励不同的行为来奖励并探索困难环境。
3. 判别器给出的奖励被喂给 *Stein 变分策略梯度*（[SVPG](https://arxiv.org/abs/1704.02399)）粒子，输出一组多样的随机化配置。

ADR 的想法很有吸引力，但有两个小疑虑。运行随机策略时，轨迹间的相似性未必是度量环境难度的好方法。sim2real 结果遗憾地不那么激动人心，但论文指出其胜点在于 ADR 探索的随机化参数范围更小。

---

引用格式：
```
@article{weng2019DR,
  title   = "Domain Randomization for Sim2Real Transfer",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2019",
  url     = "http://lilianweng.github.io/lil-log/2019/05/04/domain-randomization.html"
}
```

总之，读完本文后，希望你能像我一样喜欢域随机化 :)。

## 参考文献

[1] Josh Tobin, et al. ["Domain randomization for transferring deep neural networks from simulation to the real world."](https://arxiv.org/pdf/1703.06907.pdf) IROS, 2017.

[2] Fereshteh Sadeghi and Sergey Levine. ["CAD2RL: Real single-image flight without a single real image."](https://arxiv.org/abs/1611.04201) arXiv:1611.04201 (2016).

[3] Xue Bin Peng, et al. ["Sim-to-real transfer of robotic control with dynamics randomization."](https://arxiv.org/abs/1710.06537) ICRA, 2018.

[4] Nataniel Ruiz, et al. ["Learning to Simulate."](https://openreview.net/forum?id=HJgkx2Aqt7) ICLR 2019

[5] OpenAI. ["Learning Dexterous In-Hand Manipulation."](https://arxiv.org/abs/1808.00177) arXiv:1808.00177 (2018).

[6] OpenAI Blog. ["Learning dexterity"](https://openai.com/blog/learning-dexterity/) July 30, 2018.

[7] Quan Vuong, et al. ["How to pick the domain randomization parameters for sim-to-real transfer of reinforcement learning policies?."](https://arxiv.org/abs/1903.11774) arXiv:1903.11774 (2019).

[8] Ekin D. Cubuk, et al. ["AutoAugment: Learning augmentation policies from data."](https://arxiv.org/abs/1805.09501) arXiv:1805.09501 (2018).

[9] Wenhao Yu et al. ["Policy Transfer with Strategy Optimization."](https://openreview.net/forum?id=H1g6osRcFQ) ICLR 2019

[10] Yevgen Chebotar et al. ["Closing the Sim-to-Real Loop: Adapting Simulation Randomization with Real World Experience."](https://arxiv.org/abs/1810.05687) Arxiv: 1810.05687 (2019).

[11] Stephen James et al. ["Sim-to-real via sim-to-sim: Data-efficient robotic grasping via randomized-to-canonical adaptation networks"](https://arxiv.org/abs/1812.07252) CVPR 2019.

[12] Bhairav Mehta et al. ["Active Domain Randomization"](https://arxiv.org/abs/1904.04762) arXiv:1904.04762

[13] Sergey Zakharov,et al. ["DeceptionNet: Network-Driven Domain Randomization."](https://arxiv.org/abs/1904.02750) arXiv:1904.02750 (2019).

[14] Amlan Kar, et al. ["Meta-Sim: Learning to Generate Synthetic Datasets."](https://arxiv.org/abs/1904.11621) arXiv:1904.11621 (2019).

[15] Aayush Prakash, et al. ["Structured Domain Randomization: Bridging the Reality Gap by Context-Aware Synthetic Data."](https://arxiv.org/abs/1810.10093) arXiv:1810.10093 (2018).

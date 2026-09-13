---
title: "Agent57: Outperforming the human Atari benchmark"
source: https://deepmind.google/blog/agent57-outperforming-the-human-atari-benchmark/
site: deepmind
date: 2020-03-31
authors: Adrià Puigdomènech, Bilal Piot, Steven Kapturowski, Pablo Sprechmann, Alex Vitvitskyi, Zhaohan Daniel Guo, Charles Blundell
crawled: 2026-09-13
---

The Atari57 suite of games is a long-standing benchmark to gauge agent performance across a wide range of tasks.

We’ve developed [Agent57,](https://arxiv.org/abs/2003.13350) the first deep reinforcement learning agent to obtain a score that is above the human baseline on all 57 Atari 2600 games. Agent57 combines an algorithm for efficient exploration with a meta-controller that adapts the exploration and long vs. short-term behaviour of the agent.

## How to measure Artificial General Intelligence?

At DeepMind, we’re interested in building agents that do well on a wide range of tasks. An agent that performs sufficiently well on a sufficiently wide range of tasks is classified as [intelligent](https://arxiv.org/pdf/0706.3639.pdf). Games are an excellent testing ground for building adaptive algorithms: they provide a rich suite of tasks which players must develop sophisticated behavioural strategies to master, but they also provide an easy progress metric – game score – to optimise against. The ultimate goal is not to develop systems that excel at games, but rather to use games as a stepping stone for developing systems that learn to excel at a broad set of challenges. Typically, human performance is taken as a baseline for what doing “sufficiently well” on a task means: the score obtained by an agent on each task can be measured relative to representative human performance, providing a human normalised score: 0% indicates that an agent performs at random, while 100% or above indicates the agent is performing at human level or better.

In 2012, [the Arcade Learning environment](https://arxiv.org/abs/1207.4708) – a suite of 57 Atari 2600 games (dubbed Atari57) – was proposed as a benchmark set of tasks: these canonical Atari games pose a broad range of challenges for an agent to master. The research community commonly uses this benchmark to measure progress in building successively more intelligent agents. It’s often desirable to summarise the performance of an agent on a wide range of tasks as a single number, and so average performance (either mean or median score across all games) on the Atari57 benchmark is often used to summarise an agents’ abilities. Average scores have progressively increased over time. Unfortunately, the average performance can fail to capture how many tasks an agent is doing well on, and so is not a good statistic for determining how general an agent is: it captures that an agent is doing sufficiently well, but not that it is doing sufficiently well on a sufficiently wide set of tasks. So although average scores have increased, until now, the number of above human games has not. As an illustrative example, consider a benchmark consisting of twenty tasks. Suppose agent A obtains a score of 500% on eight tasks, 200% on four tasks, and 0% on eight tasks (mean = 240%, median = 200%), while agent B obtains a score of 150% on all tasks (mean = median = 150%). On average, agent A performs better than agent B. However, agent B possesses a more general ability: it obtains human-level performance on more tasks than agent A.

![Two horizontal bar charts comparing the performance of Agent A and Agent B across 20 games. For Agent A, scores vary widely from 0 to 500, with a mean of 240, median of 200, and 5th percentile at 0. For Agent B, all scores are consistently at 150, making the 5th percentile, median, and mean all equal to 150. A pink dashed line marks the "Average Human" baseline at 100 on both charts.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274e3d1abb0e3acb26be8e_Fig201.svg)

Figure 1: Illustration of the mean, median and 5th percentile performance of two hypothetical agents on the same benchmark set of 20 tasks.

This issue is exacerbated if some tasks are much easier than others. By performing very well on very easy tasks, agent A can apparently outperform agent B, which performs well on both easy and hard tasks.

The median is less distorted by exceptional performance on a few easy games – it’s a more [robust statistic](https://en.wikipedia.org/wiki/Robust_statistics) than the mean for indicating the [center of a distribution](https://en.wikipedia.org/wiki/Central_tendency). However, in measuring generality, the tails of the distribution become more pertinent, particularly as the number of tasks becomes larger. For example, the measure of performance on the hardest 5th percentile of games can be much more representative of an agent’s degree of generality.

Researchers have focused on maximising agents’ average performance on the Atari57 benchmark since its inception, and average performance has significantly increased over the past eight years. But, like the illustrative example above, not all Atari games are equal, with some games being much easier than others. Instead of examining the average performance, if we examine the performance of agents on the bottom 5% of games, we see that not much has changed since 2012: in fact, agents published in 2019 were struggling on the same games with which agents published in 2012 struggled. Agent57 changes this, and is a more general agent in Atari57 than any agent since the inception of the benchmark. Agent57 finally obtains above human-level performance on the very hardest games in the benchmark set, as well as the easiest ones.

![A scatter plot showing the "Atari-57 5th percentile performance" over time from 2015 to 2020. The y-axis shows the human-normalised score, with a dashed purple line indicating the "Average Human" level at 100. Single-actor agents (A through E, in light teal) and distributed agents (F through J, in blue) are plotted by their publication date. Only Agent57 (J), plotted in early 2020, surpasses the human baseline with a score above 110, while previous agents score significantly lower.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274e5504f53c5ece33f088_Fig202.svg)

Figure 2. Agents that use a distributed setup are blue, whereas single-actor agents are teal. The 5th percentile analysis shows that state of the art algorithms such as MuZero and R2D2 perform dramatically below the human benchmark (purple dotted line), whereas Agent57 performs better than humans on the hardest Atari games.

## Agent57 ancestry

Back in 2012, DeepMind developed the [Deep Q-network agent](https://www.nature.com/articles/nature14236) (DQN) to tackle the Atari57 suite. Since then, the research community has developed many extensions and alternatives to DQN. Despite these advancements, however, all deep reinforcement learning agents have consistently failed to score in four games: Montezuma’s Revenge, Pitfall, Solaris and Skiing.

Montezuma’s Revenge and Pitfall require extensive exploration to obtain good performance. A core dilemma in learning is the [exploration-exploitation problem](http://incompleteideas.net/book/the-book.html): should one keep performing behaviours one knows works (exploit), or should one try something new (explore) to discover new strategies that might be even more successful? For example, should one always order their same favourite dish at a local restaurant, or try something new that might surpass the old favourite? Exploration involves taking many suboptimal actions to gather the information necessary to discover an ultimately stronger behaviour.

Solaris and Skiing are long-term credit assignment problems: in these games, it’s challenging to match the consequences of an agents’ actions to the rewards it receives. Agents must collect information over long time scales to get the feedback necessary to learn.

Playlist: Agent57 playing the four most challenging Atari57 games – Montezuma's Revenge, Pitfall, Solaris and Skiing

For Agent57 to tackle these four challenging games in addition to the other Atari57 games, several changes to DQN were necessary.

![A lineage diagram illustrating the evolutionary path from DQN in 2015 to Agent57 in 2020. It shows DQN (2015) leading to R2D2 (2019) via "DQN Improvements" (Double DQN, Prioritised Replay, Dueling Heads, Distributed) and "Short-Term Memory" (LSTM, GRU). R2D2 then evolves into Never Give Up (2019) by incorporating "Episodic Memory" (Memory Networks, Neural Episodic Control, Transformers) and "Exploration" techniques (including Curiosity, Intrinsic Motivation, and Density Models). Finally, Never Give Up combined with a "Meta-Controller" (PBT, Bandits, Meta Gradients, Adaptive Bandits) leads to the development of Agent57 in 2020.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274eaa75887b03a74748ef_Fig203.svg)

Figure 3. Conceptual advancements to DQN that have resulted in the development of more generally intelligent agents.

## DQN improvements

Early improvements to DQN enhanced its learning efficiency and stability, including [double DQN](https://arxiv.org/pdf/1509.06461.pdf), [prioritised experience replay](https://arxiv.org/pdf/1511.05952.pdf) and [dueling architecture](https://arxiv.org/pdf/1511.06581.pdf). These changes allowed agents to make more efficient and effective use of their experience.

## Distributed agents

Next, researchers introduced **distributed** variants of DQN, [Gorila DQN](https://arxiv.org/pdf/1507.04296.pdf) and [ApeX](https://openreview.net/pdf?id=H1Dy---0Z), that could be run on many computers simultaneously. This allowed agents to acquire and learn from experience more quickly, enabling researchers to rapidly iterate on ideas. Agent57 is also a distributed RL agent that decouples the data collection and the learning processes. Many actors interact with independent copies of the environment, feeding data to a central ‘memory bank’ in the form of a prioritized replay buffer. A learner then samples training data from this replay buffer, as shown in Figure 4, similar to how a person might recall memories to better learn from them. The learner uses these replayed experiences to construct loss functions, by which it estimates the cost of actions or events. Then, it updates the parameters of its neural network by minimizing losses. Finally, each actor shares the same network architecture as the learner, but with its own copy of the weights. The learner weights are sent to the actors frequently, allowing them to update their own weights in a manner determined by their individual priorities, as we’ll discuss later.

![A diagram showing the distributed reinforcement learning architecture of Agent57, consisting of three main components arranged in a triangle: "Actors" at the top, "Replay Buffer" at the bottom-right, and "Learner" at the bottom-left. Actors generate agent experiences (transitions and initial priorities) based on intrinsic motivation and feed them into the Replay Buffer. The Learner samples training data from the Replay Buffer using prioritized sampling, updates priorities back to the buffer, minimizes reinforcement learning and intrinsic motivation losses, and sends the updated network weights back to the Actors to complete the feedback loop.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274ed18c20e6cd21a3a90c_Fig204.svg)

Figure 4. Distributed setup for Agent 57.

## Short-term memory

Agents need to have memory in order to take into account previous observations into their decision making. This allows the agent to not only base its decisions on the present observation (which is usually partial, that is, an agent only sees some of its world), but also on past observations, which can reveal more information about the environment as a whole. Imagine, for example, a task where an agent goes from room to room in order to count the number of chairs in a building. Without memory, the agent can only rely on the observation of one room. With memory, the agent can remember the number of chairs in previous rooms and simply add the number of chairs it observes in the present room to solve the task. Therefore the role of memory is to aggregate information from past observations to improve the decision making process. In deep RL and deep learning, recurrent neural networks such as [Long-Short Term Memory](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.676.4320&rep=rep1&type=pdf) (LSTM) are used as short term memories.

Interfacing memory with behaviour is crucial for building systems that self-learn. In reinforcement learning, an agent can be an on-policy learner, which can only learn the value of its direct actions, or an off-policy learner, which can learn about optimal actions even when not performing those actions – e.g., it might be taking random actions, but can still learn what the best possible action would be. Off-policy learning is therefore a desirable property for agents, helping them learn the best course of action to take while thoroughly exploring their environment. Combining off-policy learning with memory is challenging because you need to know what you might remember when executing a different behaviour. For example, what you might choose to remember when looking for an apple (e.g., where the apple is located), is different to what you might choose to remember if looking for an orange. But if you were looking for an orange, you could still learn how to find the apple if you came across the apple by chance, in case you need to find it in the future. The first deep RL agent combining memory and off-policy learning was [Deep Recurrent Q-Network](https://arxiv.org/pdf/1507.06527.pdf) (DRQN). More recently, a significant speciation in the lineage of Agent57 occurred with [Recurrent Replay Distributed DQN](https://openreview.net/pdf?id=r1lyTjAqYX) (R2D2), combining a neural network model of short-term memory with off-policy learning and distributed training, and achieving a very strong average performance on Atari57. R2D2 modifies the replay mechanism for learning from past experiences to work with short term memory. All together, this helped R2D2 efficiently learn profitable behaviours, and **exploit** them for reward.

## Episodic memory

We designed [Never Give Up](https://openreview.net/pdf?id=Sye57xStvB) (NGU) to augment R2D2 with another form of memory: episodic memory. This enables NGU to detect when new parts of a game are encountered, so the agent can explore these newer parts of the game in case they yield rewards. This makes the agent’s behaviour (**exploration**) deviate significantly from the policy the agent is trying to learn (obtaining a high score in the game); thus, off-policy learning again plays a critical role here. NGU was the first agent to obtain positive rewards, without domain knowledge, on Pitfall, a game on which no agent had scored any points since the introduction of the Atari57 benchmark, and other challenging Atari games. Unfortunately, NGU sacrifices performance on what have historically been the “easier” games and so, on average, underperforms relative to R2D2.

## Intrinsic motivation methods to encourage directed exploration

In order to discover the most successful strategies, agents must explore their environment–but some exploration strategies are more efficient than others. With DQN, researchers attempted to address the exploration problem by using an undirected exploration strategy known as epsilon-greedy: with a fixed probability (epsilon), take a random action, otherwise pick the current best action. However, this family of techniques do not scale well to hard exploration problems: in the absence of rewards, they require a prohibitive amount of time to explore large state-action spaces, as they rely on undirected random action choices to discover unseen states. In order to overcome this limitation, many directed exploration strategies have been proposed. Among these, one strand has focused on developing **intrinsic motivation rewards** that encourage an agent to explore and visit as many states as possible by providing more dense “internal” rewards for novelty-seeking behaviours. Within that strand, we distinguish two types of rewards: firstly, long-term novelty rewards encourage visiting many states throughout training, across many episodes. Secondly, short-term novelty rewards encourage visiting many states over a short span of time (e.g., within a single episode of a game).

## Seeking novelty over long time scales

[Long-term novelty rewards](https://openreview.net/pdf?id=Sye57xStvB) signal when a previously unseen state is encountered in the agent’s lifetime, and is a function of the density of states seen so far in training: that is, it’s adjusted by how often the agent has seen a state similar to the current one relative to states seen overall. When the density is high (indicating that the state is familiar), the long term novelty reward is low, and vice versa. When all the states are familiar, the agent resorts to an undirected exploration strategy. However, learning density models of high dimensional spaces is fraught with problems due to the [curse of dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality). In practice, when agents use deep learning models to learn a density model, they suffer from [catastrophic forgetting](https://www.pnas.org/content/114/13/3521) (forgetting information seen previously as they encounter new experiences), as well as an inability to produce precise outputs for all inputs. For example, in Montezuma’s Revenge, unlike undirected exploration strategies, long-term novelty rewards allow the agent to surpass the human baseline. However, even the [best performing methods on Montezuma’s Revenge](https://arxiv.org/pdf/1810.12894.pdf) need to carefully train a density model at the right speed: when the density model indicates that the states in the first room are familiar, the agent should be able to consistently get to unfamiliar territory.

Playlist: DQN vs. Agent57 playing Montezuma's revenge

## Seeking novelty over short time scales

[Short-term novelty rewards](https://openreview.net/pdf?id=Sye57xStvB) can be used to encourage an agent to explore states that have not been encountered in its recent past. Recently, neural networks that mimic some properties of [episodic memory](https://arxiv.org/pdf/1703.01988.pdf) have been used to speed up learning in reinforcement learning agents. Because episodic memories are also thought to be important for [recognising novel experiences](https://link.springer.com/content/pdf/10.3758/BF03210977.pdf), we adapted these models to give Never Give Up a notion of short-term novelty. Episodic memory models are efficient and reliable candidates for computing short-term novelty rewards, as they can quickly learn a non-parametric density model that can be adapted on the fly (without needing to learn or adapt parameters of the model). In this case, the magnitude of the reward is determined by measuring the distance between the present state and previous states recorded in episodic memory.

However, not all notions of distance encourage meaningful forms of exploration. For example, consider the task of navigating a busy city with many pedestrians and vehicles. If an agent is programmed to use a notion of distance wherein every tiny visual variation is taken into account, that agent would visit a large number of different states simply by passively observing the environment, even standing still – a fruitless form of exploration. To avoid this scenario, the agent should instead learn features that are seen as important for exploration, such as controllability, and compute a distance with respect to those features only. Such models have previously been used for exploration, and combining them with episodic memory is one of the main advancements of the [Never Give Up exploration method](https://openreview.net/pdf?id=Sye57xStvB), which resulted in above-human performance in Pitfall!

Playlist: NGU vs. Agent57 playing Pitfall!

Never Give Up (NGU) used this short-term novelty reward based on [controllable states](https://arxiv.org/pdf/1705.05363.pdf), mixed with a long term novelty reward, using [Random Network Distillation](https://openai.com/blog/reinforcement-learning-with-prediction-based-rewards/). The mix was achieved by multiplying both rewards, where the long term novelty is bounded. This way the short-term novelty reward’s effect is preserved, but can be down-modulated as the agent becomes more familiar with the game over its lifetime. The other core idea of NGU is that it learns a family of policies that range from purely exploitative to highly exploratory. This is achieved by leveraging a distributed setup: by building on top of [R2D2](https://openreview.net/pdf?id=r1lyTjAqYX), actors produce experience with different policies based on different importance weighting on the total novelty reward. This experience is produced uniformly with respect to each weighting in the family.

## Meta-controller: learning to balance exploration with exploitation

Agent57 is built on the following observation: what if an agent can learn when it’s better to exploit, and when it’s better to explore? We introduced the notion of a meta-controller that adapts the exploration-exploitation trade-off, as well as a time horizon that can be adjusted for games requiring longer temporal credit assignment. With this change, Agent57 is able to get the best of both worlds: above human-level performance on both easy games and hard games.

Specifically, intrinsic motivation methods have two shortcomings:

- **Exploration:** Many games are amenable to policies that are purely exploitative, particularly after a game has been fully explored. This implies that much of the experience produced by exploratory policies in Never Give Up will eventually become wasteful after the agent explores all relevant states.
- **Time horizon:** Some tasks will require long time horizons (e.g. Skiing, Solaris), where valuing rewards that will be earned in the far future might be important for eventually learning a good exploitative policy, or even to learn a good policy at all. At the same time, other tasks may be slow and unstable to learn if future rewards are overly weighted. This trade-off is commonly controlled by the discount factor in reinforcement learning, where a higher discount factor enables learning from longer time horizons.

This motivated the use of an online adaptation mechanism that controls the amount of experience produced with different policies, with a variable-length time horizon and importance attributed to novelty. Researchers have tried tackling this with multiple methods, including [training a population of agents](https://arxiv.org/abs/1711.09846) with different hyperparameter values, [directly learning the values of the hyperparameters by gradient descent](https://arxiv.org/abs/1805.09801), or using a [centralized bandit to learn the value of hyperparameters](https://arxiv.org/abs/1912.06910).

We used a bandit algorithm to select which policy our agent should use to generate experience. Specifically, we trained a [sliding-window UCB bandit](https://arxiv.org/pdf/0805.3415.pdf) for each actor to select the degree of preference for exploration and time horizon its policy should have.

Playlist: NGU vs. Agent57 playing Skiing

## Agent57: putting it all together

To achieve Agent57, we combined our previous exploration agent, Never Give Up, with a meta-controller. This agent computes a mixture of long and short term intrinsic motivation to explore and learn a family of policies, where the choice of policy is selected by the meta-controller. The meta-controller allows each actor of the agent to choose a different trade-off between near vs. long term performance, as well as exploring new states vs. exploiting what’s already known (Figure 4). Reinforcement learning is a feedback loop: the actions chosen determine the training data. Therefore, the meta-controller also determines what data the agent learns from.

![A comparison table of Atari57 benchmark performance statistics for Agent57, NGU, R2D2, and MuZero. It shows that Agent57 is the only agent to achieve above human-level performance on all 57 games, with a 5th percentile human-normalized score (HNS) of 116.67%, while MuZero achieves the highest mean and median HNS but drops to a 0.03% score at the 5th percentile.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274f7abe6ea3d07da4b661_Fig205.svg)

## Conclusions and the future

With Agent57, we have succeeded in building a more generally intelligent agent that has above-human performance on all tasks in the Atari57 benchmark. It builds on our previous agent Never Give Up, and instantiates an adaptive meta-controller that helps the agent to know when to explore and when to exploit, as well as what time-horizon it would be useful to learn with. A wide range of tasks will naturally require different choices of both of these trade-offs, therefore the meta-controller provides a way to dynamically adapt such choices.

Agent57 was able to scale with increasing amounts of computation: the longer it trained, the higher its score got. While this enabled Agent57 to achieve strong general performance, it takes a lot of computation and time; the data efficiency can certainly be improved. Additionally, this agent shows better 5th percentile performance on the set of Atari57 games. This by no means marks the end of Atari research, not only in terms of data efficiency, but also in terms of general performance. We offer two views on this: firstly, analyzing the performance among percentiles gives us new insights on how general algorithms are. While Agent57 achieves strong results on the first percentiles of the 57 games and holds better mean and median performance than NGU or R2D2, as illustrated by [MuZero](https://arxiv.org/abs/1911.08265), it could still obtain a higher average performance. Secondly, all current algorithms are [far from achieving optimal performance](https://arxiv.org/abs/1908.04683) in some games. To that end, key improvements to use might be enhancements in the representations that Agent57 uses for exploration, planning, and credit assignment.

**Notes**

Read the paper [here](https://arxiv.org/abs/2003.13350).

Work done by: Adrià Puigdomènech, Bilal Piot, Steven Kapturowski, Pablo Sprechmann, Alex Vitvitskyi, Daniel Guo, Charles Blundell

Figure design by Paulo Estriga and Adam Cain

**References**

Agent57 lineage

DQN: Mnih, Volodymyr, et al. "[Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236)." Nature 518.7540 (2015): 529-533.Double DQN: van Hasselt, Hado, Arthur Guez, and David Silver.

"[Deep reinforcement learning with double Q-learning](https://arxiv.org/abs/1509.06461)." CoRR abs/1509.06461 (2015)." arXiv preprint arXiv:1509.06461 (2015).Dueling: Wang, Ziyu, et al.

"[Dueling network architectures for deep reinforcement learning](https://arxiv.org/abs/1511.06581)." arXiv preprint arXiv:1511.06581 (2015).Prioritised replay: Schaul, Tom, et al.

[P"rioritized experience replay.](https://arxiv.org/abs/1511.05952)" arXiv preprint arXiv:1511.05952 (2015).Apex: Horgan, Dan, et al.

"[Distributed prioritized experience replay](https://arxiv.org/abs/1803.00933)." arXiv preprint arXiv:1803.00933 (2018).R2D2: Kapturowski, Steven, et al.

"[Recurrent experience replay in distributed reinforcement learning](https://openreview.net/pdf?id=r1lyTjAqYX)." ICLR (2019).NGU: Badia, Adrià Puigdomènech, et al.

"[Never Give Up: Learning Directed Exploration Strategies](https://arxiv.org/abs/2002.06038)." ICLR (2020).

**Episodic Memory related**

Memory Networks: Weston, Jason, Sumit Chopra, and Antoine Bordes. "[Memory networks](https://arxiv.org/abs/1410.3916)." arXiv preprint arXiv:1410.3916 (2014).

Neural Episodic Control: Pritzel, Alexander, et al. ["Neural episodic control"](https://arxiv.org/abs/1703.01988)." Proceedings of the 34th International Conference on Machine Learning-Volume 70. JMLR. org, 2017. Transformer: Vaswani, Ashish, et al.

"[Attention is all you need](https://arxiv.org/abs/1706.03762)." Advances in neural information processing systems. 2017. Wayne, Greg, et al. "Unsupervised predictive memory in a goal-directed agent." arXiv preprint arXiv:1803.10760 (2018).

**Exploration related**

Curiosity: Schmidhuber, Jürgen. "A possibility for implementing curiosity and boredom in model-building neural controllers." Proc. of the international conference on simulation of adaptive behavior: From animals to animats. 1991.

Intrinsic motivation: Oudeyer, Pierre-Yves, Frdric Kaplan, and Verena V. Hafner. "[Intrinsic motivation systems for autonomous mental development.](http://www.pyoudeyer.com/ims.pdf)" IEEE transactions on evolutionary computation 11.2 (2007): 265-286.

Intrinsic motivation: Barto, Andrew G. "[Intrinsic motivation and reinforcement learning](https://link.springer.com/chapter/10.1007/978-3-642-32375-1_2)." Intrinsically motivated learning in natural and artificial systems. Springer, Berlin, Heidelberg, 2013. 17-47.

Visit counts: Bellemare, Marc, et al. "[Unifying count-based exploration and intrinsic motivation](https://arxiv.org/abs/1606.01868)." Advances in neural information processing systems. 2016.

Density models: Ostrovski, Georg, et al. "[Count-based exploration with neural density models](https://arxiv.org/abs/1703.01310)." Proceedings of the 34th International Conference on Machine Learning-Volume 70. JMLR. org, 2017.

Ex2: Fu, Justin, John Co-Reyes, and Sergey Levine. "[Ex2: Exploration with exemplar models for deep reinforcement learning](https://arxiv.org/abs/1703.01260)."

Advances in neural information processing systems. 2017. Hashing: Tang, Haoran, et al.

"[Exploration: A study of count-based exploration for deep reinforcement learning](https://arxiv.org/abs/1611.04717)." Advances in neural information processing systems. 2017. Random Network Distillation: Burda, Yuri, et al.

"[Exploration by random network distillation](https://arxiv.org/abs/1810.12894)." arXiv preprint arXiv:1810.12894 (2018).CoEx: Choi, Jongwook, et al.

"[Contingency-aware exploration in reinforcement learning](https://arxiv.org/abs/1811.01483)." arXiv preprint arXiv:1811.01483 (2018). Reachability: Savinov, Nikolay, et al.

"[Episodic curiosity through reachability](https://arxiv.org/abs/1810.02274)." ICLR, 2019.

Never Give Up: Puigdomènech Badia, Adrià, et al. "[Never Give Up: Learning Directed Exploration Strategies](https://arxiv.org/abs/2002.06038)." arXiv (2020): arXiv-2002.

**Meta-controller related**

Population-based training: Jaderberg, Max, et al. "[Population based training of neural networks](https://arxiv.org/abs/1711.09846)." arXiv preprint arXiv:1711.09846 (2017).

Meta-gradients: Xu, Zhongwen, Hado P. van Hasselt, and David Silver. "[Meta-gradient reinforcement learning](https://arxiv.org/abs/1805.09801)."

Advances in neural information processing systems. 2018. Bandits: Schaul, Tom, et al. "[Adapting Behaviour for Learning Progress.](https://arxiv.org/abs/1912.06910)" arXiv preprint arXiv:1912.06910 (2019).

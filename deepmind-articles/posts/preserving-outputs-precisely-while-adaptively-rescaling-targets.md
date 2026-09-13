---
title: "Preserving Outputs Precisely while Adaptively Rescaling Targets"
source: https://deepmind.google/blog/preserving-outputs-precisely-while-adaptively-rescaling-targets/
site: deepmind
date: 2018-09-13
authors: Hado van Hasselt, Matteo Hessel
crawled: 2026-09-13
---

Multi-task learning - allowing a single agent to learn how to solve many different tasks - is a longstanding objective for artificial intelligence research. Recently, there has been a lot of excellent progress, with agents like [DQN](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/) able to use the same algorithm to learn to play multiple games including Breakout and Pong. These algorithms were used to train individual expert agents for each task. As artificial intelligence research advances to more complex real world domains, building a single general agent - as opposed to multiple expert agents - to learn to perform multiple tasks will be crucial. However, so far, this has proven to be a significant challenge.

One reason is that there are often differences in the reward scales our reinforcement learning agents use to judge success, leading them to focus on tasks where the reward is arbitrarily higher. For example, in the Atari game Pong, the agent receives a reward of either -1, 0, or +1 per step. In contrast, an agent playing Ms. Pac-Man can obtain hundreds or thousands of points in a single step. Even if the size of individual rewards is comparable, the frequency of rewards can change over time as the agent gets better. This means agents tend to focus on those tasks which have large scores, leading to better performance on certain tasks, and far worse on others.

To resolve these kinds of issues, we developed [PopArt](https://arxiv.org/abs/1809.04474), a technique that can adapt the scale of scores in each game so the agent judges the games to be of equal learning value, no matter the scale of rewards available in each specific game. We applied a PopArt normalisation to a state-of-the-art reinforcement learning agent, resulting in a single agent that can play a whole set of 57 diverse Atari video games, with above-human median performance across the set.

Broadly speaking, deep learning relies on the weights of a neural network being updated so that its output moves closer to the desired target output. This also applies when neural networks are used in the context of deep reinforcement learning. PopArt works by estimating the mean and the spread of these targets (such as the score in a game). It then uses these statistics to normalise the targets before they are used to update the network’s weights. Using normalised targets makes learning more stable and robust to changes in scale and shift. To obtain accurate estimates - of expected future scores for example - the outputs of the network can then be rescaled back to the true target range by inverting the normalisation process. If done naively, each update to the statistics would change all unnormalised outputs, including those that were already very good. We prevent this from happening by updating the network in the opposite direction whenever we update the statistics, this can be done exactly. This means we get the benefit of well-scaled updates, while keeping the previously learnt outputs intact. It is for these reasons that we call our method PopArt: it works by Preserving Outputs Precisely while Adaptively Rescaling Targets.

## PopArt as an alternative to clipping rewards

Traditionally, researchers have overcome the problem of varying reward scales by using reward clipping in their reinforcement learning algorithms. This clips big and small scores at 1 or -1, roughly normalising the expected rewards. Although this makes learning easier, it also changes the goal of the agent. For instance, in Ms. Pac-Man the goal is to collect pellets, each of which is worth 10 points each, and eat ghosts worth between 200 and 1600 points. With clipped rewards, there is no apparent difference for the agent between eating a pellet or eating a ghost and results in agents that only eat pellets, and never bothers to chase ghosts, as [this video](https://videos.files.wordpress.com/1nYybrEH/clipped_pacman_dvd.mp4) shows. When we remove reward clipping and use PopArt’s adaptive normalisation to stabilise learning, it results in quite different behaviour, with the agent chasing ghosts, and achieving a higher score, as shown in [this video](https://videos.files.wordpress.com/0XtMJ12x/pacman_dvd.mp4).

## Multi-task deep reinforcement learning with PopArt

We applied PopArt to the Importance-weighted Actor-Learner Architecture (IMPALA), one of the most popular deep reinforcement learning agents used at DeepMind. In our experiments, PopArt greatly improved the performance of the agent compared to the baseline agent without PopArt. Both with clipped and unclipped rewards, the median score of the PopArt agent across games was above the human median. This is much higher than the baseline with clipped rewards, while the baseline with unclipped rewards fails to reach meaningful performance at all because it cannot effectively deal with the large variation in reward scales across games.

![Line graph comparing the performance of three multi-task reinforcement learning agents. The y-axis shows Median Normalised Score, and the x-axis shows Environment Frames up to 1.2e10. The PopArt-IMPALA (unclipped) agent, represented by a solid green line, achieves the highest score, plateauing near 100. The IMPALA (clipped) agent, shown as a dashed blue line, reaches a score of around 60. The IMPALA (unclipped) agent, shown as a solid blue line, fails to make progress and remains flat near zero.](https://lh3.googleusercontent.com/lkgdCuq8hHfpmVZJUrd1cFjdkoFtA6XKXCl_yMa5akdDgD1tKMRiGQvNvgIISTUJRAgJF90zS2VWZnbs1-jyAQ3MlwNB0dWoVlKVN__7lO-B4Z3rSg=w1440)

The median standardised performance across 57 Atari games. Each line corresponds to the median performance of a single agent that was trained to play all of these games with the same neural network. Solid lines indicate where reward clipping was used. The dashed line indicates unclipped rewards were used.

This is the first time we’ve seen superhuman performance on this kind of multi-task environment using a single agent, suggesting PopArt could provide some answers to the open research question of how to balance varied objectives without manually clipping or scaling them. Its ability to adapt the normalisation automatically while learning may become important as we apply AI to more complex multi-modal domains where an agent must learn to trade-off a number of different objectives with varying rewards.

**Notes**

For more details, please see our latest [paper](https://arxiv.org/abs/1809.04474) and the original [paper](https://arxiv.org/abs/1602.07714).

This work was done by Matteo Hessel, Hubert Soyer, Lasse Espeholt, Wojciech Czarnecki, Simon Schmitt, and Hado van Hasselt.

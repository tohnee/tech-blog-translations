---
title: "Scalable agent architecture for distributed training"
source: https://deepmind.google/blog/scalable-agent-architecture-for-distributed-training/
site: deepmind
date: 2018-02-05
authors: Hubert Soyer, Drew Purves, Lasse Espeholt
crawled: 2026-09-13
---

Deep Reinforcement Learning (DeepRL) has achieved remarkable success in a range of tasks, from continuous control problems in robotics to playing games like Go and Atari. The improvements seen in these domains have so far been limited to individual tasks where a separate agent has been tuned and trained for each task.

In our most recent work, we explore the challenge of training a single agent on many tasks.

Today we are releasing DMLab-30, a set of new tasks that span a large variety of challenges in a visually unified environment with a common action space. Training an agent to perform well on many tasks requires massive throughput and making efficient use of every data point. To this end, we have developed a new, highly scalable agent architecture for distributed training called Importance Weighted Actor-Learner Architecture that uses a new off-policy correction algorithm called V-trace.

## DMLab-30

DMLab-30 is a collection of new levels designed using our open source RL environment [DeepMind Lab](https://github.com/deepmind/lab). These environments enable any DeepRL researcher to test systems on a large spectrum of interesting tasks either individually or in a multi-task setting.

![A selection of environments created as part of DMLab-30. They feature walls, pillars, and other obstacles.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622679ec36bc1bb2eb6b021a_Tasks.gif)

The tasks are designed to be as varied as possible. They differ in the goals they target, from learning, to memory, to navigation. They vary visually, from brightly coloured, modern-styled texture, to the subtle brown and greens of a desert at dawn, midday, or by night. And they contain physically different settings, from open, mountainous terrain, to right-angled mazes, to open, circular rooms.

In addition, some of the environments include ‘bots’, with their own, internal, goal-oriented behaviours. Equally importantly, the goals and rewards differ across the different levels, from following language commands and using keys to open doors, foraging mushrooms, to plotting and following a complex irreversible path.

However, at a basic level, the environments are all the same in terms of their action and observation space allowing a single agent to be trained to act in every environment in this highly varied set. More details about the environments can be found on the [DeepMind Lab GitHub page](https://github.com/deepmind/lab).

## Importance-Weighted Actor-Learner Architectures

In order to tackle the challenging DMLab-30 suite, we developed a new distributed agent called Importance Weighted Actor-Learner Architecture that maximises data throughput using an efficient distributed architecture with [TensorFlow](https://www.tensorflow.org/).

Importance Weighted Actor-Learner Architecture is inspired by the popular [A3C](https://arxiv.org/abs/1602.01783) architecture which uses multiple distributed actors to learn the agent’s parameters. In models like this, each of the actors uses a clone of the policy parameters to act in the environment. Periodically, actors pause their exploration to share the gradients they have computed with a central parameter server that applies updates (see figure below).

![Diagram comparing three distributed reinforcement learning architectures: A3C, IMPALA (Single Learner), and IMPALA (Multiple Learners). A3C shows purple actors sending gradients and receiving parameters from a central parameter server. IMPALA architectures show blue actors sending observations and receiving parameters from one or multiple central grey learners.](https://lh3.googleusercontent.com/ND8sOkEin1P1vO7AbQHnVQwuyO2h41pQUjs_QihrdjslCL_mG6TIi69hTf0TIAHVkNq-F9CEDlUn7djOFC0L1dID3rIxZQo2iC2Eem32rvW34_XKfg=w1440)

Importance Weighted Actor-Learner Architecture actors on the other hand are not used to calculate gradients. Instead, they are just used to collect experience which is passed to a central learner that computes gradients, resulting in a model that has completely independent actors and learners. To take advantage of the scale of modern computing systems, Importance Weighted Actor-Learner Architectures can be implemented using a single learner machine or multiple learners performing synchronous updates between themselves. Separating the learning and acting in this way also has the advantage of increasing the throughput of the whole system since the actors no longer need to wait for the learning step like in architectures such as batched A2C. This allows us to train Importance Weighted Actor-Learner Architectures on interesting environments without suffering from variance in frame rendering-time or time consuming task restarts.

![Timeline comparison showing Batched A2C actors waiting in lockstep for a single backward pass, while IMPALA actors generate data asynchronously and continuously send it to a learner executing back-to-back forward and backward passes.](https://lh3.googleusercontent.com/oL04Fo2mjeqzKRuaWb7wuPJ8rrVXL_blD59Fz8B0Hj3_XQ2a1UCp8ZSKFtGEDMzWcgONUW3ZCCr_NhwxflhsAIyusQfoV6LNYA8xBN04WEhW6Ebw=w1440)

Learning is continuous with Importance Weighted Actor-Learner Architectures, unlike other architectures that need to pause at each learning step

However, decoupling the acting and learning causes the policy in the actor to lag behind the learner. In order to compensate for this difference we introduce a principled off-policy advantage actor critic formulation called V-trace which compensates for the trajectories obtained by actors being off policy. The details of the algorithm and its analysis can be found in our [paper](https://arxiv.org/abs/1802.01561).

![Line graph comparing training performance of IMPALA (blue line) versus A3C (purple line). The y-axis shows Mean Capped Normalised Score ranging from 0 to 60, and the x-axis shows Environment Frames up to 1e10. The IMPALA curve consistently rises faster and reaches a higher final score of approximately 50 compared to A3C's score of around 30.](https://lh3.googleusercontent.com/xiCotpILN14KXtEAfv9IcGH0VZu6ghMkB0EAGw8l8mY_qUxI2HN9b9FdbQGrn25F_z32RnRG7RG75WnxreUwRcW5DnxKeQQuaTbkgeiLR75YKVB_6lE=w1440)

Thanks to the optimised model of Importance Weighted Actor-Learner Architecture, it can process one-to-two orders of magnitude more experience compared to similar agents, making learning in challenging environments possible. We have compared Importance Weighted Actor-Learner Architectures with several popular actor-critic methods and have seen significant speed-ups. Additionally, the throughput using Importance Weighted Actor-Learner Architectures scales almost linearly with increasing number of actors and learners which shows that both the distributed agent model and the V-trace algorithm can handle very large scale experiments, even on the order of thousands of machines.

When it was tested on the DMLab-30 levels, Importance Weighted Actor-Learner Architecture was 10 times more data efficient and achieved double the final score compared to distributed A3C. Moreover, Importance Weighted Actor-Learner Architectures showed positive transfer from training in multi-task settings compared to training in single-task setting.

**Notes**

Read the full Importance Weighted Actor-Learner Architectures paper [here](https://arxiv.org/abs/1802.01561).

Explore DMLab-30 [here](https://github.com/deepmind/lab/tree/master/game_scripts/levels/contributed/dmlab30).

This work was done by Lasse Espeholt, Hubert Soyer, Remi Munos, Karen Simonyan, Volodymir Mnih, Tom Ward, Yotam Doron, Vlad Firoiu, Tim Harley, Iain Dunning, Shane Legg and Koray Kavukcuoglu

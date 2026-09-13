---
title: "Open sourcing TRFL: a library of reinforcement learning building blocks"
source: https://deepmind.google/blog/open-sourcing-trfl-a-library-of-reinforcement-learning-building-blocks/
site: deepmind
date: 2018-10-17
authors: Matteo Hessel, Miljan Martic, Diego de Las Casas, Gabriel Barth-Maron
crawled: 2026-09-13
---

Today we are open sourcing a [new library](https://github.com/deepmind/trfl/) of useful building blocks for writing reinforcement learning (RL) agents in TensorFlow. Named TRFL (pronounced ‘truffle’), it represents a collection of key algorithmic components that we have used internally for a large number of our most successful agents such as DQN, DDPG and the Importance Weighted Actor Learner Architecture.

A typical deep reinforcement learning agent consists of a large number of interacting components: at the very least, these include the environment and some deep network representing values or policies, but they often also include components such as a learned model of the environment, pseudo-reward functions or a replay system.

These parts tend to interact in subtle ways (often not well-documented in papers, as highlighted by [Henderson and colleagues](https://arxiv.org/pdf/1709.06560.pdf)), thus making it difficult to identify bugs in such large computational graphs. A recent [blog post by OpenAI](https://openai.com/blog/openai-baselines-dqn/) highlighted this issue by analysing some of the most popular open-source implementations of reinforcement learning agents and finding that six out of 10 “had subtle bugs found by a community member and confirmed by the author”.

One approach to addressing this issue, and helping those in the research community attempting to reproduce results from papers, is through open-sourcing complete agent implementations. For example, this is what we did recently with our [scalable distributed implementation of the v-trace agent](https://deepmind.com/blog/article/impala-scalable-distributed-deeprl-dmlab-30). These large agent codebases can be very useful for reproducing research, but also hard to modify and extend. A different and complementary approach is to provide reliable, well-tested implementations of common building blocks, that can be used in a variety of different RL agents. Moreover, having these core components abstracted away in a single library, with a consistent API, makes it simpler to combine ideas originating from various different publications.

The TRFL library includes functions to implement both classical RL algorithms as well as more cutting-edge techniques. The loss functions and other operations provided here are implemented in pure TensorFlow. They are not complete algorithms, but implementations of RL-specific mathematical operations needed when building fully-functional RL agents.

For value-based reinforcement learning we provide TensorFlow ops for learning in discrete action spaces, such as TD-learning, Sarsa, Q-learning and their variants, as well as ops for implementing continuous control algorithms, such as DPG. We also include ops for learning distributional value functions. These ops support batches, and return a loss that can be minimised by feeding it to a TensorFlow Optimiser. Some losses operate over batches of transitions (e.g. Sarsa, Q learning, ...), and others over batches of trajectories (e.g. Q lambda, Retrace, ...). For policy-based methods, we have utilities to easily implement both online methods such as A2C, as well as supporting off-policy correction techniques, such as v-trace. The computation of policy gradients in continuous action spaces is also supported. Finally, TRFL also provides an implementation of the auxiliary pseudo-reward functions used by UNREAL, which we have found to improve data efficiency in a variety of domains.

This is not a one-time release. Since this library is used extensively within DeepMind, we will continue to maintain it as well as add new functionalities over time. We are also eager to [receive contributions](https://github.com/deepmind/trfl/blob/master/CONTRIBUTING.md) to the library by the wider RL community.

This library was created by the Research Engineering team at DeepMind.

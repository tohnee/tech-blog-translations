---
title: "DeepMind Papers @ NIPS (Part 1)"
source: https://deepmind.google/blog/deepmind-papers-nips-part-1/
site: deepmind
date: 2016-12-02
authors: 
crawled: 2026-09-13
---

## Interaction Networks for Learning about Objects, Relations and Physics

**Authors:** Peter Battaglia, Razvan Pascanu, Matthew Lai, Danilo Rezende, Koray Kavukcuoglu

Reasoning about objects, relations, and physics is central to human intelligence, and a key goal of artificial intelligence. However many modern machine learning methods still face a trade-off between expressive structure and efficient performance.

We introduce “interaction networks”, which can reason about how objects in complex systems interact, supporting dynamical predictions, as well as inferences about the abstract properties of the system. Interaction networks are both expressive and efficient because they combine three powerful approaches: structured models, simulation, and deep learning. They take as input graph-structured data, perform object- and relation-centric reasoning in a way that is analogous to a simulation, and are implemented using deep neural networks. They are invariant to permutations of the entities and relations, which allows them to automatically generalize to systems of different sizes and structures than they have experienced during training.

In our experiments, we used interaction networks to implement the first general-purpose learnable physics engine. After training only on single step predictions, our model was able to simulate the physical trajectories of n-body, bouncing ball, and non-rigid string systems accurately over thousands of time steps. The same architecture was also able to infer underlying physical properties, such as potential energy.

Beyond physical reasoning, interaction networks may provide a powerful framework for AI approaches to scene understanding, social perception, hierarchical planning, and analogical reasoning.

For further details and related work, please see [the paper](https://arxiv.org/abs/1612.00222).

For applications of interaction networks to scene understanding and imagination-based decision-making, please see our submissions to ICLR 2017: [Discovering objects and their relations from entangled scene representations](https://openreview.net/forum?id=Bk2TqVcxe) and [Metacontrol for Adaptive Imagination-Based Optimization](https://openreview.net/forum?id=Bk8BvDqex)

**Check it out at NIPS:**Mon Dec 5th 06:00 - 09:30 PM @ Area 5+6+7+8 #48
Fri Dec 9th 08:00 - 6:30 PM @ Hilton Diag. Mar, Blrm. C

## Strategic Attentive Writer for Learning Macro-Actions

**Authors:** Alexander (Sasha) Vezhnevets, Volodymyr Mnih, Simon Osindero, Alex Graves, Oriol Vinyals, John Agapiou, Koray Kavukcuoglu

Learning temporally extended actions and temporal abstraction in general is a long standing problem in reinforcement learning. They facilitate learning by enabling structured exploration and economic computation. In this paper we present a novel deep recurrent neural network architecture that learns to build implicit plans in an end-to-end manner purely by interacting with an environment in a reinforcement learning setting. The network builds an internal plan, which is continuously updated upon observation of the next input from the environment. It can also partition this internal representation into contiguous sub-sequences by learning for how long the plan can be committed to – i.e. followed without replanning. Combining these properties, the proposed model, dubbed STRategic Attentive Writer (STRAW) can learn high-level, temporally abstracted macro-actions of varying lengths that are solely learnt from data without any prior information.

Watch the video [here](https://www.youtube.com/watch?v=niMOdSu3yio).

For further details and related work, please see [the paper](https://arxiv.org/pdf/1606.04695.pdf).

**Check it out at NIPS:**Mon Dec 5th 06:00 - 09:30 PM @ Area 5+6+7+8 #111

## Matching Networks for One Shot Learning

**Authors:** Oriol Vinyals, Charles Blundell, Timothy Lillicrap, Koray Kavukcuoglu, Daan Wierstra

Given just a few, or even a single, examples of an unseen class, it is possible to attain high classification accuracy on ImageNet using Matching Networks. The core architecture is simple and straightforward to train and performant across a range of image and text classification tasks.

![Diagram of a Matching Network architecture for one-shot learning, showing a support set of dog images mapped through function g_theta and a target image mapped through f_theta to compute attention over classes and output a prediction.](https://lh3.googleusercontent.com/iwF_oAw70rcv-PZlHyr3rEL353s7WqNB3DghzHk90NyFwkKSb7zDrK-tW5B1BKdAdBZItjxy-R31R_7lvski2OvHT6aIXOtD8vCQiUeQYquyXoVlk3I=w1440)

Matching Networks are trained in the same way as they are tested: by presenting a series of instantaneous one shot learning training tasks, where each instance of the training set is fed into the network in parallel. Matching Networks are then trained to classify correctly over many different input training sets. The effect is to train a network that can classify on a novel data set without the need for a single step of gradient descent.

For further details and related work, please see [the paper](https://arxiv.org/abs/1606.04080).

**Check it out at NIPS:**Mon Dec 5th 06:00 - 09:30 PM @ Area 5+6+7+8 #139

## Safe and efficient off-policy reinforcement learning

**Authors:** Remi Munos, Tom Stepleton, Anna Harutyunyan, Marc G. Bellemare

Our goal is to design a Reinforcement Learning (RL) algorithm with two desired properties. Firstly, to use off-policy data, which is important for exploration, when we use memory replay, or observe log-data. Secondly, to use multi-steps returns in order to propagate rewards faster and avoid accumulation of approximation/estimation errors. Both properties are crucial in deep RL.

We introduce the “Retrace” algorithm, which uses multi-steps returns and can safely and efficiently utilize any off-policy data. We show the convergence of this algorithm in both policy evaluation and optimal control settings.

As corollary we prove the convergence of Watkin’s Q(λ) to Q\* (which was an open problem since 1989).

Finally we report numerical results on the Atari domain that demonstrate the huge benefit of Retrace over competitive algorithms.

For further details and related work, please see [the paper](https://arxiv.org/abs/1606.02647).

**Check it out at NIPS:**Mon Dec 5th 06:00 - 09:30 PM @ Area 5+6+7+8 #151

## Blazing the trails before beating the path: Sample efficient Monte-Carlo planning

**Authors:** Jean-Bastien Grill (INRIA), Michal Valko (INRIA), Remi Munos

You are a robot and you live in a Markov decision process (MDP) with a finite or an infinite number of transitions from state-action to next states. You got brains and so you plan before you act. Luckily, your roboparents equipped you with a generative model to do some Monte-Carlo planning. The world is waiting for you and you have no time to waste. You want your planning to be efficient. Sample-efficient. Indeed, you want to exploit the possible structure of the MDP by exploring only a subset of states reachable by following near-optimal policies. You want guarantees on sample complexity that depend on a measure of the quantity of near-optimal states. You want something, that is an extension of Monte-Carlo sampling (for estimating an expectation) to problems that alternate maximization (over actions) and expectation (over next states). You want something simple to implement and computationally efficient. You want it all and you want it now. You want TrailBlazer.

For further details and related work, please see [the paper](https://papers.nips.cc/paper/6253-blazing-the-trails-before-beating-the-path-sample-efficient-monte-carlo-planning.pdf).

**Check it out at NIPS:**Tue Dec 6th 05:00 - 05:20 PM @ Area 3 (Oral) in Theory
Tue Dec 6th @ Area 5+6+7+8 #193

## Deep Exploration via Bootstrapped DQN

**Authors:** Ian Osband, Charles Blundell, Alex Pritzel and Benjamin Van Roy

Efficient exploration in complex environments remains a major challenge for reinforcement learning (RL). We’ve seen a lot of recent breakthroughs in RL, but many of these algorithms require huge amounts of data (millions of games) before they learn to make good decisions. In many real-world settings, such large amounts of data aren’t feasible.

One of the reasons these algorithms learn so slowly is that they do not gather the \*right\* data to learn about the problem. These algorithms use dithering (taking random actions) to explore their environment - which can be exponentially less efficient that \*deep\* exploration which prioritizes potentially informative policies over multiple timesteps. There is a large literature on algorithms for deep exploration for statistically efficient reinforcement learning. The problem is that none of these algorithms are computationally tractable with deep learning... until now.

Key breakthroughs in this paper include the following:

- We present the first practical reinforcement learning algorithm that combines deep learning with deep exploration: Bootstrapped DQN.
- We show that this algorithm can lead to exponentially faster learning.
- We present new state of the art results on Atari 2600.

For further details and related work, please see [the paper](https://papers.nips.cc/paper/6501-deep-exploration-via-bootstrapped-dqn) and our video playlist [here](https://www.youtube.com/playlist?list=PLdy8eRAW78uLDPNo1jRv8jdTx7aup1ujM).

**Check it out at NIPS:**Mon Dec 5th 06:00 - 09:30 PM @ Area 5+6+7+8 #79

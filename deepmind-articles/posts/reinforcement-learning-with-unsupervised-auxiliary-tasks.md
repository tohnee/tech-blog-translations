---
title: "Reinforcement learning with unsupervised auxiliary tasks"
source: https://deepmind.google/blog/reinforcement-learning-with-unsupervised-auxiliary-tasks/
site: deepmind
date: 2016-11-17
authors: Max Jaderberg, Vlad Mnih, Wojciech Marian Czarnecki
crawled: 2026-09-13
---

Our primary mission at DeepMind is to push the boundaries of AI, developing programs that can learn to solve any complex problem without needing to be taught how. Our reinforcement learning agents have achieved [breakthroughs in Atari 2600 games](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/) and the [game of Go](https://deepmind.com/research/case-studies/alphago-the-story-so-far). Such systems, however, can require a lot of data and a long time to learn so we are always looking for ways to improve our generic learning algorithms.

Our recent paper [“Reinforcement Learning with Unsupervised Auxiliary Tasks”](https://arxiv.org/pdf/1611.05397.pdf) introduces a method for greatly improving the learning speed and final performance of agents. We do this by augmenting the standard [deep reinforcement learning](https://deepmind.com/blog/article/deep-reinforcement-learning) methods with two main additional tasks for our agents to perform during training.

A visualisation of our agent in a Labyrinth maze foraging task can be seen below.

![A diagram showing the DeepMind UNREAL agent's visualization, divided into a "Live Play" panel on the left navigating a 3D Labyrinth maze, and an "Auxiliary Tasks" panel on the right illustrating Pixel Control, Reward Prediction, and Value Function Replay.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62228b56e2b4eb57fa1e7718_Reinforcement20Learning20with20Unsupervised20Auxi.gif)

The first task involves the agent learning how to control the pixels on the screen, which emphasises learning how your actions affect what you will see rather than just prediction. This is similar to how a baby might learn to control their hands by moving them and observing the movements. By learning to change different parts of the screen, our agent learns features of the visual input that are useful for playing the game and getting higher scores.

In the second task the agent is trained to predict the onset of immediate rewards from a short historical context. In order to better deal with the scenario where rewards are rare we present the agent with past rewarding and non-rewarding histories in equal proportion. By learning on rewarding histories much more frequently, the agent can discover visual features predictive of reward much faster.

The combination of these auxiliary tasks, together with our previous [A3C paper](https://deepmind.com/blog/article/deep-reinforcement-learning) is our new UNREAL agent (UNsupervised REinforcement and Auxiliary Learning). We tested this agent on a suite of 57 Atari games as well as a 3D environment called Labyrinth with 13 levels. In all the games, the same UNREAL agent is trained in the same way, on the raw image output from the game, to produce actions to maximise the score or reward of the agent in the game. The behaviour required to get game rewards is incredibly varied, from picking up apples in 3D mazes to playing Space Invaders - the same UNREAL algorithm learns to play these games often to human level and beyond.

In Labyrinth, the result of using the auxiliary tasks - controlling the pixels on the screen and predicting when reward is going to occur - means that UNREAL is able to learn over 10x faster than our previous best A3C agent, and reaches far better performance. We can now achieve 87% of expert human performance averaged across the Labyrinth levels we considered, with super-human performance on a number of them. On Atari the agent now achieves on average 9x human performance. We hope that this work will allow us to scale up our agents to ever more complex environments.

**Notes**

Read the paper: [Reinforcement Learning with Unsupervised Auxiliary Tasks](https://arxiv.org/pdf/1611.05397.pdf)

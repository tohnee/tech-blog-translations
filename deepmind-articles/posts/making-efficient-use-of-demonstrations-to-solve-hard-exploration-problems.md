---
title: "Making Efficient Use of Demonstrations to Solve Hard Exploration Problems"
source: https://deepmind.google/blog/making-efficient-use-of-demonstrations-to-solve-hard-exploration-problems/
site: deepmind
date: 2019-09-05
authors: Caglar Gülçehre, Tom Le Paine, Bobak Shahriari, Misha Denil, Matt Hoffman, Hubert Soyer, Richard Tanburn, Steven Kapturowski, Neil Rabinowitz, Duncan Williams, Gabriel Barth-Maron, Ziyu Wang, Nando de Freitas, Worlds team
crawled: 2026-09-13
---

![A grid of six gameplay screenshots displaying various 3D room environments from the Hard Eight task suite.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228bc30b71ebc05d2d0b6cb_Fig201.gif)

We propose a new agent, which we call Recurrent Replay Distributed DQN from Demonstrations (R2D3). R2D3 is designed to make efficient use of demonstrations to solve sparse reward tasks in partially observed environments with highly variable initial conditions. The architecture of the R2D3 agent is shown below. There are several actor processes, each running independent copies of the behavior against an instance of the environment. Each actor streams its experience to a shared agent replay buffer, where experience from all actors is aggregated and globally prioritized. The actors periodically request the latest network weights from the learner process in order to update their behavior.

![System architecture diagram of the R2D3 agent, showing actors streaming trajectories to an agent replay buffer, and a learner process sampling training batches from both the agent replay and a demo replay buffer to optimize via double Q-learning and update priorities.](https://lh3.googleusercontent.com/-u3hLQ-5nxjWDF8UoQ5nA7T9Em6wQjSv8-0IAXobJYXSkKBCVWe8JD_ETyaIrDGF1qXoNnaz0WzVtT43SO8YlPazA1brxciuFz9pqWGF-96o8pmHYQ=w1440)

As shown in the figure, R2D3 has two replay buffers: an agent replay and a demo replay buffer, which is populated with expert demonstrations of the task to be solved. Maintaining separate replay buffers for agent experience and expert demonstrations allows us to prioritize the sampling of agent and expert data separately. The learner process samples batches of data from both the agent and demo replay buffers simultaneously. The demo ratio (ρ) controls the proportion of data coming from the expert demonstrations vs from the agent’s own experience. The demo ratio is implemented at a batch level by randomly choosing whether to sample from the expert replay buffer independently with probability ρ. When ρ=0, R2D3 performs standard RL, when ρ=1, R2D3 performs batch RL on the data in demo buffer. The loss is optimized by the learner by using n-step double Q-learning (with n=5) and a dueling architecture.

In each replay buffer, we store fixed-length sequences of (s, a, r) tuples where adjacent sequences overlap by 40 time-steps. These sequences never cross episode boundaries. Given a single batch of trajectories we unroll both online and target networks on the same sequence of states to generate value estimates with the recurrent state initialized to zero.

## Hard Eight Task Suite

The tasks in the Hard Eight task suite require the agent to perform a sequence of high level skills in order to gain access to a large apple which gives the reward and terminates the episode. In the picture below, we give an example from the Baseball task. The agent must learn to execute these high level skills as a sequence of low level actions in the environment. The sequence of low-level actions can be quite long and consequently it is unlikely that the task will be solved by random exploration. Let us note that each step in this task involves interaction with physical objects in the environment which are shown in bold.

![Eight panels showing the illustrated process of finding a bat, picking it up, hitting a ball off a plinth, picking up the ball, activating a sensor, opening a door, walking through it, and collecting an apple.](https://lh3.googleusercontent.com/TGqG8Mg5GHgMWJvNSh-UtAlk95K86aojS1CWB5oJOY5a-DtMcuWbeGVJ-zM_V5Ryg8Rk-BJds7zCUIGhK3XDquQXRvPk2xJS3IGXmBe3YDtI1uOONg=w1440)

In the figure below, for each task the agent (blue triangle) must interact with objects in its environment in order to gain access to a large apple (red triangle) that provides reward. Our 3D environments are procedurally generated such that at every episode, the state of the world such as shapes of the objects, colors and positions are different. The environment is partially observable which means that the agent can only see the part of the environment at every timestep. Since the agent receives the reward only at the end of the episode and needs to execute a long sequence of actions, the exploration can be difficult. Furthermore, highly variable initial conditions and the objects that the agents can interact with can make the exploration even more difficult.

![Eight different 3D models, labelled baseball, drawbridge, navigate cubes, push blocks, remember sensor, throw across, wall sensor, and wall sensor stack. A red triangle and a blue triangle are visible in all environments.](https://lh3.googleusercontent.com/fSSdk1-SRlxfgbrdkEqM92h1wsXDy5hbEIfy26Wz0V8LENz0cEcJYWC1o7bt-lJxXo8bU9hDx1Oe1EIKZJWZIn8xon3wjGvbLRO9nv7RweuD82RCBQ=w1440)

## Human demonstrating tasks

Below is a playlist of eight videos of humans performing each of the tasks to demonstrate the steps involved.

## R2D3 on Hard Eight Tasks

Below is a playlist of eight representative videos of the R2D3 agent after training on each of these tasks.

## Additional R2D3 Results

We ran a few additional experiments - shown in the playlist below - to get more information about the tasks R2D3 did not solve, or solved incorrectly.

### Remember Sensor

This task requires a long memory, and has the longest episode length of any task in the suite. In an attempt to mitigate these issues, we trained the agent using a higher action repeat of 4 which reduces the episode length, and used stale lstm states instead of zero lstm states which provides information about earlier in the episode. This allows R2D3 to learn policies that display reasonable behavior.

### Throw Across

The demonstrations collected for this task had a very low success rate of 54%. We attempted to compensate for this by collecting an additional 30 demos. When we trained R2D3 with all 130 demos all seed solved the task.

### Wall Sensor Stack

The original Wall Sensor Stack environment had a bug that the R2D3 agent was able to exploit. We fixed the bug and verified the agent can learn the proper stacking behaviour.

**Notes**

We would like to thank the following members of the DeepMind Worlds Team for developing the tasks in this paper: Charlie Beattie, Gavin Buttimore, Adrian Collister, Alex Cullum, Charlie Deck, Simon Green, Tom Handley, Cédric Hauteville, Drew Purves, Richie Steigerwald and Marcus Wainwright.

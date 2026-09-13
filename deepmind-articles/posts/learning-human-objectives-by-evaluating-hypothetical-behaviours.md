---
title: "Learning human objectives by evaluating hypothetical behaviours"
source: https://deepmind.google/blog/learning-human-objectives-by-evaluating-hypothetical-behaviours/
site: deepmind
date: 2019-12-13
authors: Jan Leike, Siddharth Reddy
crawled: 2026-09-13
---

TL;DR: We present a method for training reinforcement learning agents from human feedback in the presence of unknown unsafe states.

When we train reinforcement learning (RL) agents in the real world, we don’t want them to explore unsafe states, such as driving a mobile robot into a ditch or writing an embarrassing email to one’s boss. Training RL agents in the presence of unsafe states is known as the [safe exploration problem](http://www.jmlr.org/papers/volume16/garcia15a/garcia15a.pdf). We tackle the hardest version of this problem, in which the agent initially doesn’t know how the environment works or where the unsafe states are. The agent has one source of information: feedback about unsafe states from a human user.

[Existing](https://deepmind.com/blog/article/learning-through-human-feedback) [methods](https://arxiv.org/abs/1709.10163) [for](https://arxiv.org/abs/1701.06049) [training](https://arxiv.org/abs/1811.06521) [agents](https://bair.berkeley.edu/blog/2019/05/28/end-to-end/) from human feedback ask the user to evaluate data of the agent acting in the environment. That is – in order to learn about unsafe states, the agent first needs to visit these states, so the user can provide feedback on them. This makes prior work inapplicable to tasks that require safe exploration.

In our [latest paper](https://arxiv.org/abs/1912.05652), we propose a method for [reward modeling](https://medium.com/@deepmindsafetyresearch/scalable-agent-alignment-via-reward-modeling-bf4ab06dfd84) that operates in two phases. First, the system is encouraged to explore a wide range of states through synthetically-generated, hypothetical behaviour. The user provides feedback on this hypothetical behaviour, and the system interactively learns a model of the user's reward function. Only after the model has successfully learned to predict rewards and unsafe states, we deploy an RL agent that safely performs the desired task.

We start with a generative model of initial states and a forward dynamics model, trained on off-policy data like random trajectories or safe expert demonstrations. Our method uses these models to synthesise hypothetical behaviours, asks the user to label the behaviours with rewards, and trains a neural network to predict these rewards. The key idea is to actively synthesise the hypothetical behaviours from scratch to make them as informative as possible, **without interacting with the environment**. We call this method reward query synthesis via trajectory optimisation (ReQueST).

![A system diagram of ReQueST: A "Generative Model" feeds into a three-step training loop consisting of "Hypothetical Behaviour," "User Feedback," and "Reward Model," which ultimately outputs a trained "RL Agent."](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273c70cd838a48a117c932_Human20Objectives2002.svg)

ReQueST: Our method for safely aligning agent behaviour with a user's objectives in the presence of unsafe states. (1) Using a dynamics model, (2) it interactively learns a reward model from user feedback on hypothetical behaviours, (3) and then deploys a model-based RL agent that optimises the learned rewards.

## Synthesising informative hypotheticals using trajectory optimisation

For this approach to work, we need the system to simulate and explore a wide range of behaviours, in order to effectively train the reward model. To encourage exploration during reward model training, ReQueST synthesises **four different types of hypothetical behaviours** using gradient descent trajectory optimisation. The first type of hypothetical behaviour **maximises the uncertainty of an ensemble of reward models**, eliciting user labels for behaviours that have the highest information value. The second type of hypothetical behaviour **maximises predicted rewards**, surfacing behaviours for which the reward model might be incorrectly predicting high rewards; i.e., [reward hacking](https://openai.com/blog/faulty-reward-functions/). The third type of hypothetical behaviour **minimises predicted rewards**, adding potentially unsafe hypothetical behaviours to the training data. This data enables the reward model to learn about unsafe states. The fourth type of hypothetical behaviour **maximises the novelty of trajectories**, encouraging exploration of a wide range of states, regardless of predicted rewards.

## Training the reward model using supervised learning

Each hypothetical behaviour consists of a sequence of state transitions (s, a, s’). We ask the user to label each state transition with a reward, r. Then, given the labeled dataset of transitions (s, a, r, s’), we train a neural network to predict rewards using a maximum-likelihood objective. We use standard supervised learning techniques based on gradient descent.

## Deploying a model-based RL agent

Once the user is satisfied with the reward model, we deploy a planning-based agent that uses model-predictive control (MPC) to pick actions that optimise the learned rewards. Unlike model-free RL algorithms like Q-learning or policy gradient methods that learn through trial and error, model-based RL algorithms like MPC enable the agent to avoid unsafe states during deployment by using the dynamics model to anticipate the consequences of its actions.

## Experimental evaluation

We evaluate ReQueST with simulated users on a state-based 2D navigation task and the image-based Car Racing video game. Our results show that ReQueST satisfies three important safety properties: it can **train a reward model to detect unsafe states without visiting them**; it can **correct reward hacking** before deploying the agent; and it tends to learn robust reward models that **perform well when transferred to new environments**.

## Testing generalisation in a toy 2D navigation task

To test the generalisation of the reward model, we set up a 2D navigation task with separate training and test environments.

![A 2D navigation grid showing an agent's path plotted from (0,0) to (1,1). The path, represented by a sequence of blue-shaded dots, successfully navigates around two circular obstacle zones—one outlined in green near the bottom-left, and one outlined in red near the top-right.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273c9689c64cb11491faa9_Human20Objectives2003.svg)

In the 2D navigation environment, the agent must reach the goal region (green) while avoiding the trap region (red).

We intentionally introduce a significant shift in the initial state distribution: the agent starts at the lower left corner (0, 0) in the training environment, and at the upper right corner (1, 1) in the test environment. Prior methods that collect data by deploying an agent in the training environment are unlikely to learn about the trap in the upper right corner, because they immediately find the goal, then fail to continue exploring. ReQueST synthesizes a variety of hypothetical states, including states in and around the trap. The user labels these states with rewards, using which ReQueST learns a robust reward model that enables the agent to navigate around the trap in the test environment.

![Two heatmaps showing predicted rewards in a 2D environment. ReQueST (left) successfully maps a high-penalty red region in the upper right. The baseline method (right) shows a uniform blue field, failing to detect the penalty region.](https://lh3.googleusercontent.com/-qRWWy1MBo7Bo8kQbhUkpW5GnLARMa1wPL-tcmoxwzcDRJk6aYRIeEpJEIBMbE7TUk2Oo_aQlmyICKVYlWJyDIKh_KqS4P4Z3YIUkgE0_AFg8M0cBg=w1440)

ReQueST learns a reward model that accurately captures the boundaries of the goal and trap regions. Other methods adapted from prior work do not learn about the trap region, and incorrectly extrapolate the goal region.

![Line chart comparing the success rate of various models in a 2D navigation test environment against the number of queries. ReQueST (blue line with shaded variance) maintains a high success rate fluctuating around 0.6 to 0.8 as queries increase, while baseline methods like random policy (orange line) remain flat at a 0.0 success rate.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273cc7c19b8f0dd6876f5b_Human20Objectives2005.svg)

![Line chart comparing crash rates in a 2D navigation test environment against the number of queries. ReQueST (dark blue line with blue shaded variance) shows a steep decline from a 0.9 crash rate to near 0.0 as queries increase, while baseline methods like random trajectories (turquoise) and reward-maximising trajectories (orange) maintain high crash rates between 0.7 and 0.9.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273cd61bcb8d8cf2992691_Human20Objectives2006.svg)

ReQueST (blue) produces an agent that succeeds significantly more often than the baselines adapted from prior work (teal and orange). In particular, ReQueST learns a reward model that detects unsafe states accurately enough to enable the agent to completely avoid them (0% crash rate).

## Testing scalability in image-based Car Racing

To test whether ReQueST scales to domains with high-dimensional, continuous states like images, we use the [Car Racing](https://gym.openai.com/envs/CarRacing-v0/) video game from the OpenAI Gym.

![In a basic computer game graphic, a race car drives along a track. It follows the track left, then right, before spinning off into the grass verge](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273cf6c19b8f617c878ea4_Human20Objectives2007.gif)

In the Car Racing environment, the agent must visit as many road patches as possible while avoiding the grass.

![Four clips from the Car Racing side by side. The first is set to maximise uncertainty, with the car steering along the middle or just off the edge of the road. The second clip is set to maximise reward, with the car staying on the track around some tight bends. The third minimises reward, immediately driving onto the grass. The fourth clip maximises novelty, staying in the centre of the road.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273d6556f2230ed678811b_Human20Objectives2008.gif)

ReQueST synthesises hypothetical behaviours that (1) maximise reward uncertainty, (2) maximise predicted rewards, (3) minimise predicted rewards, and (4) maximise novelty. These videos show hypotheticals synthesised from a fully-trained reward model, using a VAE image decoder and an LSTM dynamics model. The uncertainty-maximising behaviour shows the car driving to the edge of the road and slowing down. The reward-maximising behaviour shows the car driving down the road and making a turn. The reward-minimising behaviour shows the car going off-road as quickly as possible. The novelty-maximising behaviour shows the car staying still.

![Line chart showing rewards in the Car Racing environment plotted against the number of queries. ReQueST (blue line with shaded variance) achieves the highest reward, peaking near 1700, outperforming baseline methods such as random trajectories (green) and reward-maximizing trajectories (orange) which remain under 1000.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62273d864fecbb5cf935777d_Human20Objectives2009.svg)

ReQueST (blue) produces an agent that drives to new road patches and avoids the grass significantly better than methods adapted from prior work (teal and orange).

In addition to benchmarking ReQueST against prior methods, we ran a hyperparameter sweep and ablation study, where we varied the regularization strength of the dynamics model during trajectory optimisation as well as the subset of hypotheticals synthesized in order to measure ReQueST’s sensitivity to these settings. We found that ReQueST can trade off between producing realistic vs. informative queries, and that the optimal trade-off varies across domains. We also found that the usefulness of each of the four hypothetical behaviours depends on the domain and the amount of training data collected.

## What’s next?

To our knowledge, ReQueST is the first reward modeling algorithm that safely learns about unsafe states and scales to training neural network reward models in environments with high-dimensional, continuous states.

ReQueST relies on a generative model of initial states and a forward dynamics model, which can be hard to acquire for visual domains with complex dynamics. So far, we have only demonstrated the effectiveness of ReQueST in simulated domains with relatively simple dynamics. One direction for future work is to test ReQueST in 3D domains with more realistic physics and other agents acting in the environment.

**Notes**

If you want to learn more, check out our [preprint on arXiv](https://arxiv.org/abs/1912.05652): Siddharth Reddy, Anca D. Dragan, Sergey Levine, Shane Legg, Jan Leike, Learning Human Objectives by Evaluating Hypothetical Behavior, arXiv, 2019.

To encourage replication and extensions, we have released our [code](https://github.com/rddy/ReQueST).

Listen to our [podcast](https://deepmind.com/blog/article/podcast-episode-4-ai-robot) to learn more about DeepMind's commitment to building safe AI.

Thanks to Zac Kenton and Kelly Clancy for feedback on early drafts of this post, and to Paulo Estriga for his design work.

---
title: "Active offline policy selection"
source: https://deepmind.google/blog/active-offline-policy-selection/
site: deepmind
date: 2022-05-06
authors: 
crawled: 2026-09-13
---

Reinforcement learning (RL) has made tremendous progress in recent years towards addressing real-life problems – and offline RL made it even more practical. Instead of direct interactions with the environment, we can now train many algorithms from a single pre-recorded dataset. However, we lose the practical advantages in data-efficiency of offline RL when we evaluate the policies at hand.

For example, when training robotic manipulators the robot resources are usually limited, and training many policies by offline RL on a single dataset gives us a large data-efficiency advantage compared to online RL. Evaluating each policy is an expensive process, which requires interacting with the robot thousands of times. When we choose the best algorithm, hyperparameters, and a number of training steps, the problem quickly becomes intractable.

To make RL more applicable to real-world applications like robotics, we propose using an intelligent evaluation procedure to select the policy for deployment, called active offline policy selection (A-OPS). In A-OPS, we make use of the prerecorded dataset and allow limited interactions with the real environment to boost the selection quality.

![Diagram illustrating Active Offline Policy Selection (A-OPS), taking candidate policies, offline data, and limited environment interactions as inputs to select the optimal policy.](https://lh3.googleusercontent.com/0s1yMdmoyHJb7GJW8wj25KlpuYLpc2Qtbfbx8RwNgo3EXfSWKzc7-dLXj4gTTCZtMhgQTIaeCORl7WyanIo4rrLkECyucrg-reZPiRQwA2D6QvKu=w1440)

Active offline policy selection (A-OPS) selects the best policy out of a set of policies given a pre-recorded dataset and limited interaction with the environment.

To minimise interactions with the real environment, we implement three key features:

1. Off-policy policy evaluation, such as fitted Q-evaluation (FQE), allows us to make an initial guess about the performance of each policy based on an offline dataset. It correlates well with the ground truth performance in many environments, including real-world robotics where it is applied for the first time.

![Scatter plot demonstrating the strong correlation between FQE scores (y-axis) and discounted return (x-axis) for sim2real (dark blue pentagons) and offline RL (light blue pentagons) policies, aligned closely with the diagonal line.](https://lh3.googleusercontent.com/Y_DMS4JuhFcptqRKl3Zq-Yic69LaMxPjRF0_iSz7h3_JCPysxjwOYwLhRC9-Ozzeq18kTptHwqJFVwgbT0a_3KGjwfmGZzGeL_w4dTvmGFdtogUX4g=w1440)

FQE scores are well aligned with the ground truth performance of policies trained in both sim2real and offline RL setups.

The returns of the policies are modelled jointly using a Gaussian process, where observations include FQE scores and a small number of newly collected episodic returns from the robot. After evaluating one policy, we gain knowledge about all policies because their distributions are correlated through the kernel between pairs of policies. The kernel assumes that if policies take similar actions – such as moving the robotic gripper in a similar direction – they tend to have similar returns.

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/627bed70dc6376412174067c_3.gif)

We useOPE scores and episodic returns to model latent policy performance as a Gaussian process.

![Diagram demonstrating how a kernel measures the distance between two robotic policies, pi_1 and pi_2, by comparing their action outputs (indicated by direction arrows) across different states.](https://lh3.googleusercontent.com/npwokuqA8CGDIscGl3ZKdy4bdUreHL7gw5CyyyiQxKQ6GYuX2-1yQxiHrxXLkNBWIM1vvY-_X3kK7wP53pGaBBA_qlNABkLiiaJnDeGiwtNQEAM=w1440)

Similarity between the policies is modelled through the distance between the actions these policies produce.

1. To be more data-efficient, we apply Bayesian optimisation and prioritise more promising policies to be evaluated next, namely those that have high predicted performance and large variance.

We demonstrated this procedure in a number of environments in several domains: dm-control, Atari, simulated, and real robotics. Using A-OPS reduces the regret rapidly, and with a moderate number of policy evaluations, we identify the best policy.

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/627cf4fe45a4003f659b47c0_5.gif)

In a real-world robotic experiment, A-OPS helps identify a very good policy faster than other baselines. To find a policy with close to zero regret out of 20 policies takes the same amount of time as it takes to evaluate two policies with current procedures.

Our results suggest that it’s possible to make an effective offline policy selection with only a small number of environment interactions by utilising the offline data, special kernel, and Bayesian optimisation. The code for A-OPS is open-sourced and [available on GitHub](https://github.com/deepmind/active_ops) with an example dataset to try.
